#!/usr/bin/env python3
"""
Daily autonomous publish: find new studio work, write one entry, rebuild, commit,
push, and verify it on the live site. Reverts its own commit if the live check
fails.

    python tools/daily_publish.py            # one entry at most
    python tools/daily_publish.py --dry-run  # pick a candidate, write its facts JSON only

The source material (LanceDB memories, conversation summaries, project folders) is
local and private, so this runs on this machine, not in CI. A model key is
optional: with OPENAI_API_KEY in the environment or .env the run asks the endpoint
directly, and an authored payload at data/intake/authored.json is used without one.

data/intake/handoff.json is both the way out and the way back in. A run that finds
a candidate writes the facts, the exact prompt and the schema there; an LLM (or a
session with no key at all) fills in data/intake/authored.json with the matching
candidate_key; the next run publishes from those two files and then removes them.
A handoff payload is itself a candidate, so the keyless path works even when the
local scan finds nothing to publish.

A run that cannot produce an entry is an error, never a quiet success. No intake
candidate, an unreadable handoff or authored payload, a payload written for a
different candidate and a candidate with neither a key nor an authored payload all
exit 1 and log one explicit ERROR line saying what is missing. Only the deliberate
guards (lock already held, weekly cap reached, --dry-run) exit 0 without publishing.

Guardrails: refuses a dirty tree, takes a lock, caps publishing at seven auto
entries per week, retries a candidate at most three times, and refuses drafts with
placeholders, banned phrases or unsafe SVG. Everything else is enforced by the
existing gates and the push-triggered entry live check.

Exit codes: 0 = published, a dry run, or a deliberate skip (lock, weekly cap);
1 = a failure that needs attention, including an intake that cannot produce an
entry. The scheduled task relies on this: a silent zero is what let the site sit
unchanged for days.
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
HANDOFF_PATH = INTAKE_DIR / "handoff.json"
AUTHORED_PATH = INTAKE_DIR / "authored.json"
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
# Matched against folder.name.lower() with '-' folded to '_', so every casing and
# spelling of a portfolio checkout (this repo is both Studio_Portfolio and
# studio-portfolio on this disk) is excluded. A stale second clone is not studio
# work and must not become an entry.
IGNORE_FOLDERS = {"studio_portfolio", "_shared_library", "new_folder"}


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


class IntakeError(RuntimeError):
    """The intake is in a state where no entry can be produced."""


def relative(path: Path) -> str:
    return path.relative_to(PORTFOLIO_ROOT).as_posix()


def load_handoff() -> dict | None:
    """A handoff payload is a candidate in its own right.

    It carries the facts, the prompt and the schema, so the run that consumes it
    needs neither a model key nor a successful local scan. Without this, the
    keyless path could write a handoff but never publish from it.
    """
    if not HANDOFF_PATH.exists():
        return None
    try:
        payload = json.loads(HANDOFF_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise IntakeError(f"{relative(HANDOFF_PATH)} is not valid JSON: {exc}") from exc
    candidate = payload.get("candidate")
    if not isinstance(candidate, dict) or not str(candidate.get("key") or "").strip():
        raise IntakeError(f"{relative(HANDOFF_PATH)} has no candidate with a key")
    candidate.setdefault("source", "handoff")
    return candidate


def write_handoff(candidate: dict) -> Path:
    facts = candidate.get("facts") if isinstance(candidate.get("facts"), dict) else build_facts(candidate)
    candidate_with_facts = {**candidate, "facts": facts}
    HANDOFF_PATH.parent.mkdir(parents=True, exist_ok=True)
    HANDOFF_PATH.write_text(
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
    return HANDOFF_PATH


def scanned_candidate(ledger: dict) -> dict | None:
    try:
        items = gather_candidates()
    except Exception as exc:  # missing databases, an unreadable table, a broken path
        raise IntakeError(
            f"the local scan cannot run ({type(exc).__name__}: {exc})"
        ) from exc
    return next(
        (
            item for item in items
            if item["key"] not in ledger["done"]
            and ledger["attempts"].get(item["key"], 0) < MAX_ATTEMPTS
        ),
        None,
    )


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
            if not folder.is_dir() or folder.name.lower().replace("-", "_") in IGNORE_FOLDERS:
                continue
            norm = normalize_path(str(folder))
            # Only a path recorded for this folder, or one inside it, means the
            # folder is documented. A recorded parent (the projects root itself)
            # must not hide every folder under it.
            if any(known == norm or known.startswith(norm + "/") for known in known_paths):
                continue
            readme = read_readme(folder)
            if not readme:
                continue
            item = bucket(f"ws:{norm}", str(folder))
            item["from_folder"] = True
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
            or item.get("from_folder")
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
    # A handoff candidate already carries the facts it was written with; keep them
    # and only fill in what the local workspace can still contribute.
    provided = candidate.get("facts") if isinstance(candidate.get("facts"), dict) else {}
    facts = build_facts(candidate)
    facts.update({key: value for key, value in provided.items() if value})
    candidate = {**candidate, "facts": facts}
    INTAKE_DIR.mkdir(parents=True, exist_ok=True)
    candidate_path = INTAKE_DIR / "candidate.json"
    candidate_path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    origin = "handoff payload" if candidate.get("source") == "handoff" else "intake scan"
    log(f"candidate {candidate['key']} from the {origin}: {candidate.get('title') or '(untitled)'} "
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
    if candidate.get("source") == "handoff":
        body = ("Generated from the session-authored handoff payload for "
                f"{candidate.get('workspace') or 'an unknown workspace'}.\n\n"
                f"Candidate {candidate['key']}; revert this commit if the entry is wrong.")
    else:
        body = (f"Generated from {len(candidate.get('memory_ids', []))} memories and "
                f"{len(candidate.get('conversation_ids', []))} conversations in "
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
    check = run([sys.executable, "tools/check_live_push.py", "--base", base, "--head", head,
                 "--timeout", "600"], capture=False)
    if check.returncode != 0:
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
            log(f"skipped: the configured cap of {WEEKLY_LIMIT} auto entries this week is reached")
            return 0

        ledger = load_ledger()
        if args.candidate:
            candidate = json.loads(Path(args.candidate).read_text(encoding="utf-8"))
            if not candidate.get("key"):
                log("ERROR: no entry produced: the candidate file has no key")
                return 1
        else:
            try:
                candidate = load_handoff()
                if candidate is None:
                    candidate = scanned_candidate(ledger)
                elif candidate["key"] in ledger["done"]:
                    log(f"the handoff candidate {candidate['key']} is already published; ignoring it")
                    candidate = scanned_candidate(ledger)
                else:
                    log(f"using the handoff payload as the candidate ({candidate['key']})")
            except IntakeError as exc:
                log(f"ERROR: no entry produced: {exc}")
                return 1
        if not candidate:
            log(
                "ERROR: no entry produced: data/intake/handoff.json is missing and the local "
                "scan found nothing undocumented to publish"
            )
            return 1

        INTAKE_DIR.mkdir(parents=True, exist_ok=True)
        draft_path = None
        if AUTHORED_PATH.exists():
            try:
                payload = json.loads(AUTHORED_PATH.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                log(f"ERROR: no entry produced: data/intake/authored.json is not valid JSON: {exc}")
                return 1
            authored_key = str(payload.get("candidate_key") or "")
            if authored_key == candidate["key"]:
                draft_path = AUTHORED_PATH
                log("using the session-authored payload")
            else:
                log(
                    f"authored payload is for candidate {authored_key or '(none)'}, "
                    f"not {candidate['key']}; not using it"
                )

        key_present = bool(os.environ.get("OPENAI_API_KEY", "").strip())
        if draft_path is None and not key_present and not args.dry_run:
            handoff_path = write_handoff(candidate)
            log(f"wrote {relative(handoff_path)} with the facts, prompt and schema")
            log(
                "ERROR: no entry produced: OPENAI_API_KEY is not set and there is no authored "
                f"payload for candidate {candidate['key']}; author data/intake/authored.json "
                "with that candidate_key and re-run"
            )
            return 1

        code = publish(candidate, args.dry_run, draft_path)
        if code == 0 and not args.dry_run:
            ledger["done"][candidate["key"]] = {
                "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "workspace": candidate.get("workspace", ""),
            }
            for path in (HANDOFF_PATH, AUTHORED_PATH):
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
