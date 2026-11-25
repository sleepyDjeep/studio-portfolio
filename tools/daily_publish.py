#!/usr/bin/env python3
"""
Daily autonomous publish: find new studio work, write one entry, rebuild, commit,
push, and verify it on the live site. Reverts its own commit if the live check
fails.

    python tools/daily_publish.py            # one entry at most
    python tools/daily_publish.py --dry-run  # pick a candidate, write its facts JSON only

The source material (LanceDB memories, conversation summaries, project folders) is
local and private, so this runs on this machine, not in CI. A value for
A model key is optional: with OPENAI_API_KEY in the environment or .env the run
asks the endpoint directly. Without one it writes data/intake/handoff.json (the
candidate facts plus the exact prompt and schema) and exits 0; a payload authored
from that handoff at data/intake/authored.json is used on the next run and then
removed. With neither, it skips cleanly rather than failing every day.

Guardrails: refuses a dirty tree, takes a lock, caps publishing at seven auto
entries per week, retries a candidate at most three times, and refuses drafts with
placeholders, banned phrases or unsafe SVG. Everything else is enforced by the
existing gates and the push-triggered entry live check.

Exit codes: 0 = published or nothing to do, 1 = a failure that needs attention.
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.parse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auto_entry import DRAFT_SCHEMA, build_prompt  # noqa: E402

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PORTFOLIO_ROOT / "data"
INTAKE_DIR = DATA_DIR / "intake"
LOG_DIR = DATA_DIR / "logs"
LEDGER_PATH = INTAKE_DIR / "ledger.json"
LOCK_PATH = DATA_DIR / "daily.lock"
MANIFEST_PATH = DATA_DIR / "master_manifest.json"
MEMORY_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\memory_db"
CONV_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\conversation_summaries.db"
PROJECTS_ROOT = Path(r"D:\Projects")
INCEPTION_DATE = "2026-08-16"
WEEKLY_LIMIT = 7
MAX_ATTEMPTS = 3
LOCK_STALE_SECONDS = 6 * 3600
IGNORE_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", "venv", ".venv",
    "__pycache__", ".cache", "target", "bin", "obj",
}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
IGNORE_FOLDERS = {"Studio_Portfolio", "_Shared_Library", "New folder"}


def load_env() -> None:
    env_path = PORTFOLIO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def log(message: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    print(line)
    with open(LOG_DIR / f"daily-{date.today().isoformat()}.log", "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def run(command: list[str], capture: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        command, cwd=str(PORTFOLIO_ROOT), capture_output=capture, text=True,
        encoding="utf-8", errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if output.strip():
        log(output.strip()[-2000:])
    return result


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(PORTFOLIO_ROOT), capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    ).stdout.strip()


def acquire_lock() -> bool:
    if LOCK_PATH.exists():
        age = time.time() - LOCK_PATH.stat().st_mtime
        if age < LOCK_STALE_SECONDS:
            log(f"another run holds the lock ({int(age)}s old); exiting")
            return False
        log("removing a stale lock")
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCK_PATH.write_text(f"{os.getpid()} {datetime.now().isoformat()}", encoding="utf-8")
    return True


def load_ledger() -> dict:
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {"done": {}, "attempts": {}}


def save_ledger(ledger: dict) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def weekly_auto_commits() -> int:
    since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    out = git("log", f"--since={since}", "--grep=\\[auto-entry\\]", "--format=%H")
    return len([line for line in out.splitlines() if line.strip()])


def known_material() -> tuple[set[str], set[str], set[str]]:
    # The manifest is local-only, so a fresh checkout (or a machine that has never
    # run the build) has no record of what is already published. An unattended run
    # must still proceed from the empty set instead of crashing.
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    memories = set(manifest.get("excluded_memories", {}).keys())
    conversations = set(manifest.get("excluded_conversations", {}).keys())
    paths = set()
    for entry in manifest.get("entries", []):
        memories.update(entry.get("memory_ids", []))
        conversations.update(entry.get("conversation_ids", []))
        for item in entry.get("local_paths", []):
            raw = item.get("path", "") if isinstance(item, dict) else str(item)
            clean = normalize_path(raw)
            if clean:
                paths.add(clean)
    return memories, conversations, paths


def normalize_path(raw: str) -> str:
    text = urllib.parse.unquote(str(raw or "")).replace("\\", "/").rstrip("/").lower()
    text = re.sub(r"^file:/+", "", text)
    return text


def file_uri_to_path(raw: str) -> str:
    return urllib.parse.unquote(str(raw or "")).replace("file:///", "").replace("file://", "")


def scan_images(folder: Path, limit: int = 6) -> list[Path]:
    found: list[tuple[float, Path]] = []
    if not folder.exists() or not folder.is_dir():
        return []
    for path in folder.rglob("*"):
        if len(path.relative_to(folder).parts) > 4:
            continue
        if any(part.lower() in IGNORE_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in IMAGE_SUFFIXES and path.is_file():
            try:
                if path.stat().st_size >= 20 * 1024:
                    found.append((path.stat().st_mtime, path))
            except OSError:
                continue
    found.sort(reverse=True)
    return [path for _, path in found[:limit]]


def read_readme(folder: Path) -> str:
    for name in ("README.md", "readme.md", "README.txt"):
        candidate = folder / name
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8", errors="replace")[:4000]
    return ""


def gather_candidates() -> list[dict]:
    import lancedb

    memories, conversations, known_paths = known_material()
    candidates: dict[str, dict] = {}

    def bucket(key: str, workspace: str) -> dict:
        return candidates.setdefault(key, {
            "workspace": workspace, "memory_ids": [], "conversation_ids": [],
            "texts": [], "conversations": [], "earliest": "", "latest": "",
        })

    db = lancedb.connect(MEMORY_DB_PATH)
    frame = db.open_table("memories").to_pandas()
    frame = frame[frame["created_at"] >= INCEPTION_DATE]
    for _, row in frame.iterrows():
        memory_id = str(row["id"])
        if memory_id in memories:
            continue
        workspace = str(row.get("workspace_path") or "").replace("\\", "/")
        key = f"ws:{workspace.lower()}" if workspace else f"mem:{memory_id}"
        item = bucket(key, workspace)
        item["memory_ids"].append(memory_id)
        text = " ".join(str(row.get("text") or "").split())
        if text:
            item["texts"].append(text[:600])
        created = str(row.get("created_at") or "")[:19]
        item["earliest"] = earlier(item["earliest"], created)
        item["latest"] = max(item["latest"], created)

    connection = sqlite3.connect(f"file:{CONV_DB_PATH}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        """
        SELECT conversation_id, title, preview, step_count, last_modified_time, workspace_uris
        FROM conversation_summaries
        WHERE last_modified_time >= ?
          AND (nesting_depth IS NULL OR nesting_depth = 0)
          AND (parent_conversation_id IS NULL OR parent_conversation_id = '')
        """,
        (INCEPTION_DATE,),
    ).fetchall()
    connection.close()
    for row in rows:
        conversation_id = row["conversation_id"]
        if conversation_id in conversations:
            continue
        uris = []
        try:
            uris = json.loads(row["workspace_uris"] or "[]")
        except json.JSONDecodeError:
            pass
        workspace = file_uri_to_path(uris[0]) if uris else ""
        key = f"ws:{workspace.lower()}" if workspace else f"conv:{conversation_id}"
        item = bucket(key, workspace)
        item["conversation_ids"].append(conversation_id)
        item["conversations"].append(
            f"{row['title'] or row['preview'] or 'untitled'} ({row['step_count']} steps)"
        )
        modified = str(row["last_modified_time"])[:19]
        item["earliest"] = earlier(item["earliest"], modified)
        item["latest"] = max(item["latest"], modified)

    if PROJECTS_ROOT.exists():
        for folder in sorted(PROJECTS_ROOT.iterdir()):
            if not folder.is_dir() or folder.name in IGNORE_FOLDERS:
                continue
            norm = normalize_path(str(folder))
            if any(norm in known or known in norm for known in known_paths):
                continue
            readme = read_readme(folder)
            if not readme:
                continue
            item = bucket(f"ws:{norm}", str(folder))
            item["texts"].append(f"Project folder {folder} with a README.")
            item["latest"] = item["earliest"] = datetime.fromtimestamp(
                folder.stat().st_mtime
            ).strftime("%Y-%m-%dT%H:%M:%S")

    result = []
    for key, item in candidates.items():
        significant = (
            len(item["memory_ids"]) >= 3
            or any("steps" in conv and int(re.search(r"\((\d+) steps\)", conv).group(1)) >= 20
                   for conv in item["conversations"])
            or key.startswith("dir:")
        )
        if not significant:
            continue
        item["key"] = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
        item["title"] = workspace_name(item["workspace"])
        result.append(item)
    result.sort(key=lambda item: item.get("latest") or "", reverse=True)
    return result


def earlier(current: str, value: str) -> str:
    if not value:
        return current
    if not current or value < current:
        return value
    return current


def workspace_name(workspace: str) -> str:
    text = str(workspace or "").strip().rstrip("/\\")
    return Path(text).name if text else ""


def build_facts(candidate: dict) -> dict:
    workspace = Path(candidate["workspace"]) if candidate.get("workspace") else None
    images = scan_images(workspace) if workspace and workspace.is_dir() else []
    return {
        "project_dir": str(workspace) if workspace and workspace.is_dir() else "",
        "texts": candidate.get("texts", [])[:25],
        "conversations": candidate.get("conversations", [])[:15],
        "readme": read_readme(workspace) if workspace and workspace.is_dir() else "",
        "images": [str(path) for path in images],
    }


def discard_local_entry() -> None:
    """Undo everything this run wrote, without touching the rest of the tree."""
    run(["git", "reset", "--hard", "HEAD"])
    run(["git", "clean", "-fd", "--", "docs", "assets"])


def publish(candidate: dict, dry_run: bool, draft_path: Path | None = None) -> int:
    facts = build_facts(candidate)
    candidate = {**candidate, "facts": facts}
    INTAKE_DIR.mkdir(parents=True, exist_ok=True)
    candidate_path = INTAKE_DIR / "candidate.json"
    candidate_path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    log(f"candidate {candidate['key']}: {candidate.get('title') or '(untitled)'} "
        f"({len(candidate.get('memory_ids', []))} memories, "
        f"{len(candidate.get('conversation_ids', []))} conversations, "
        f"{len(facts['images'])} images)")
    if dry_run:
        log("dry run: facts written, nothing generated or published")
        return 0

    command = [sys.executable, "tools/auto_entry.py", "--candidate", str(candidate_path)]
    if draft_path is not None:
        command += ["--draft", str(draft_path)]
    result = run(command)
    if result.returncode != 0:
        return 1

    # Gate 3 checks the index, not just the disk, so the new files must be staged
    # before the gates run. The run starts from a clean tree, so a failure here
    # can safely discard exactly what this run wrote.
    run(["git", "add", "docs", "assets"])
    if run([sys.executable, "tools/verify_portfolio.py", "--update-baseline"]).returncode != 0:
        discard_local_entry()
        return 1
    if run([sys.executable, "tools/update_portfolio.py", "--no-verify"]).returncode != 0:
        discard_local_entry()
        return 1
    if run([sys.executable, "tools/verify_portfolio.py", "--skip-coverage"]).returncode != 0:
        discard_local_entry()
        return 1

    changed = [line[3:] for line in git("status", "--porcelain").splitlines() if line.strip()]
    log(f"changed paths: {', '.join(changed)}")
    run(["git", "add", "docs", "assets", "tools/expected_entries.json", "portfolio-data.js"])
    message = f"Add {candidate.get('title') or candidate['key']} to the portfolio [auto-entry]"
    body = (f"Generated from {len(candidate['memory_ids'])} memories and "
            f"{len(candidate['conversation_ids'])} conversations in "
            f"{candidate.get('workspace') or 'an unknown workspace'}.\n\n"
            f"Candidate {candidate['key']}; revert this commit if the entry is wrong.")
    if run(["git", "commit", "-m", message, "-m", body]).returncode != 0:
        discard_local_entry()
        return 1
    base = git("rev-parse", "HEAD^")
    head = git("rev-parse", "HEAD")
    if run(["git", "push", "origin", "main"]).returncode != 0:
        log("push rejected; rebasing onto origin/main and retrying once")
        if run(["git", "pull", "--rebase", "origin", "main"]).returncode != 0:
            log("could not rebase onto origin/main; discarding the local auto entry")
            run(["git", "rebase", "--abort"])
            run(["git", "reset", "--hard", "origin/main"])
            return 1
        if run([sys.executable, "tools/update_portfolio.py", "--no-verify"]).returncode != 0:
            run(["git", "reset", "--hard", "origin/main"])
            return 1
        run(["git", "add", "portfolio-data.js"])
        run(["git", "commit", "--amend", "--no-edit"])
        if run(["git", "push", "origin", "main"]).returncode != 0:
            log("push failed again; discarding the local auto entry")
            run(["git", "reset", "--hard", "origin/main"])
            return 1
        base = git("rev-parse", "HEAD^")
        head = git("rev-parse", "HEAD")
    log(f"pushed {head[:8]}; verifying on the live site")
    forced_failure = os.environ.get("AUTO_ENTRY_FORCE_LIVE_FAILURE") == "1"
    if forced_failure:
        log("[test] AUTO_ENTRY_FORCE_LIVE_FAILURE=1: treating the live check as failed")
        check_code = 1
    else:
        check_command = [sys.executable, "tools/check_live_push.py", "--base", base, "--head", head,
                         "--timeout", "600"]
        live_url = os.environ.get("PORTFOLIO_LIVE_URL", "").strip()
        if live_url:
            check_command += ["--base-url", live_url]
        check = run(check_command, capture=False)
        check_code = check.returncode
    if check_code != 0:
        log("live check failed; reverting the auto entry")
        if run(["git", "revert", "--no-edit", "HEAD"]).returncode == 0:
            run(["git", "push", "origin", "main"])
        return 1
    log("live check passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish one new studio entry per day.")
    parser.add_argument("--dry-run", action="store_true", help="pick a candidate and write its facts only")
    parser.add_argument("--candidate", help="use this candidate JSON instead of the intake scan")
    args = parser.parse_args()

    load_env()
    if not acquire_lock():
        return 0
    try:
        if git("status", "--porcelain"):
            log("working tree is dirty; refusing to publish over unrelated changes")
            return 1
        if run(["git", "pull", "--rebase", "origin", "main"]).returncode != 0:
            log("could not update from origin/main; not publishing")
            return 1
        if not args.dry_run and weekly_auto_commits() >= WEEKLY_LIMIT:
            log(f"skipped: {WEEKLY_LIMIT} auto entries already published this week")
            return 0

        ledger = load_ledger()
        if args.candidate:
            candidate = json.loads(Path(args.candidate).read_text(encoding="utf-8"))
            if not candidate.get("key"):
                log("candidate file has no key; refusing")
                return 1
        else:
            candidate = next(
                (
                    item for item in gather_candidates()
                    if item["key"] not in ledger["done"]
                    and ledger["attempts"].get(item["key"], 0) < MAX_ATTEMPTS
                ),
                None,
            )
        if not candidate:
            log("no unpublished candidates")
            return 0

        INTAKE_DIR.mkdir(parents=True, exist_ok=True)
        handoff_path = INTAKE_DIR / "handoff.json"
        authored_path = INTAKE_DIR / "authored.json"
        draft_path = None
        if authored_path.exists():
            try:
                payload = json.loads(authored_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                payload = {}
            if str(payload.get("candidate_key") or "") == candidate["key"]:
                draft_path = authored_path
                log("using the session-authored payload")
            else:
                log("ignoring an authored payload written for a different candidate")

        key_present = bool(os.environ.get("OPENAI_API_KEY", "").strip())
        if draft_path is None and not key_present and not args.dry_run:
            facts = build_facts(candidate)
            candidate_with_facts = {**candidate, "facts": facts}
            handoff_path.write_text(
                json.dumps(
                    {
                        "candidate_key": candidate["key"],
                        "created": datetime.now().isoformat(timespec="seconds"),
                        "candidate": candidate_with_facts,
                        "schema": DRAFT_SCHEMA,
                        "prompt": build_prompt(candidate_with_facts),
                        "instructions": (
                            "Write one JSON object in this schema, plus \"candidate_key\": "
                            f"\"{candidate['key']}\", to data/intake/authored.json, then run "
                            "tools/daily_publish.py again. The payload is validated before publishing."
                        ),
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            log(f"no key and no authored payload: wrote {handoff_path.relative_to(PORTFOLIO_ROOT).as_posix()}")
            log("author the payload, then re-run; nothing was published")
            return 0

        code = publish(candidate, args.dry_run, draft_path)
        if code == 0 and not args.dry_run:
            ledger["done"][candidate["key"]] = {
                "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "workspace": candidate.get("workspace", ""),
            }
            for path in (handoff_path, authored_path):
                path.unlink(missing_ok=True)
        elif code != 0:
            ledger["attempts"][candidate["key"]] = ledger["attempts"].get(candidate["key"], 0) + 1
        save_ledger(ledger)
        return code
    finally:
        try:
            LOCK_PATH.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
