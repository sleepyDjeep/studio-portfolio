#!/usr/bin/env python3
"""
Negative controls for the portfolio gates (gate_self_test.py).

A gate that can no longer fail looks exactly like a gate that passes. This script
takes that seriously: it makes a throwaway copy of the tree, breaks exactly one
thing per case, and requires the matching check to exit non-zero with the message
that names the breakage. A case that stays green is the failure.

Cases:
  baseline             untouched copy: gates 2-5 and the freshness check both pass
  gate2_doc_section    drop a required '## ' heading from one entry
  gate2_frontmatter    replace a doc's closing '---' fence with '--'
  gate2_entry_missing  delete an entry doc outright (the baseline must notice)
  gate3_missing_asset  truncate an image the bundle references to zero bytes
  gate3_untracked_asset  drop that image from the git index while leaving it on disk
  gate4_slop           append a banned word to README.md
  gate5_vault_tracked  force-add a file under docs/vault/
  freshness_media      append one byte to a referenced image (still >0 bytes, so gate 3
                       stays green and only the media hash can catch it)
  freshness_doc        append a sentence to an entry without recompiling the bundle
  build_frontmatter    the same broken fence, but only the builder is asked: it must
                       refuse rather than compile the other 47 entries

Gate 1 (corpus coverage) has no case here: it needs the private
data/master_manifest.json and the local LanceDB/SQLite stores, so there is nothing
portable to break. Everything CI enforces is covered.

Each case runs on its own copy, so one break can never mask another. Copies use
hard links to keep the 135 MB assets/ tree cheap, and every mutation unlinks its
target before writing, so a break can never reach the real repo through the shared
inode. The scratch tree lives inside the project (same volume as assets/, which
hard links require) and is removed on the way out.

Exit codes: 0 = every control turned its check red, 1 = a control went green.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PREFIX = "window.PORTFOLIO_DATA = "
REQUIRED_SECTION = "Under the Hood & Local Files"
SCRATCH_PREFIX = ".gate-self-test-"

# Left out of the copies: history, the gitignored private tree, the local vault
# bundle and this script's own scratch dirs. Keeping data/ and the vault out means
# a case sees the same tree CI sees.
COPY_IGNORE = shutil.ignore_patterns(
    ".git",
    "data",
    "vault",
    "portfolio-vault.js",
    "__pycache__",
    "*.pyc",
    f"{SCRATCH_PREFIX}*",
)

COMMANDS = {
    "verify": [sys.executable, "tools/verify_portfolio.py", "--skip-coverage"],
    "freshness": [sys.executable, "tools/check_bundle_freshness.py"],
}


def _link_or_copy(src: str, dst: str) -> str:
    try:
        os.link(src, dst)
        return dst
    except OSError:  # different volume, or a filesystem without hard links
        return shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=COPY_IGNORE, copy_function=_link_or_copy)


def _writable_then_retry(func, path, _exc) -> None:
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        pass


def force_rmtree(root: Path) -> bool:
    """Remove a scratch tree, including the read-only object files git writes on Windows."""
    try:
        if sys.version_info >= (3, 12):
            shutil.rmtree(root, onexc=_writable_then_retry)
        else:
            shutil.rmtree(root, onerror=_writable_then_retry)
    except OSError:
        return False
    return not root.exists()


def init_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=str(root), check=True, capture_output=True)
    # Gate 3 reads the index, so a copy with nothing staged would fail it for the
    # wrong reason and make the baseline meaningless.
    subprocess.run(["git", "add", "-A"], cwd=str(root), check=True, capture_output=True)


def rewrite_text(path: Path, text: str) -> None:
    path.unlink()  # break the hard link first: never write through to the real file
    path.write_text(text, encoding="utf-8")


def rewrite_bytes(path: Path, data: bytes) -> None:
    path.unlink()
    path.write_bytes(data)


def docs(root: Path) -> list[Path]:
    return sorted((root / "docs").rglob("*.md"))


def first_doc(root: Path, containing: str | None = None) -> Path:
    for path in docs(root):
        text = path.read_text(encoding="utf-8")
        if containing is None or f"## {containing}" in text:
            return path
    raise RuntimeError(f"no doc found containing '## {containing}'")


def doc_id(path: Path) -> str:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        raise RuntimeError(f"{path.name} has no YAML frontmatter to read")
    return str((yaml.safe_load(parts[1]) or {}).get("id") or path.stem)


def load_bundle(root: Path) -> dict:
    raw = (root / "portfolio-data.js").read_text(encoding="utf-8")
    idx = raw.find(BUNDLE_PREFIX)
    if idx == -1:
        raise RuntimeError("portfolio-data.js has no window.PORTFOLIO_DATA assignment")
    return json.loads(raw[idx + len(BUNDLE_PREFIX):].rstrip().rstrip(";"))


def referenced_png(root: Path) -> str:
    bundle = load_bundle(root)
    for entry in bundle.get("entries", []):
        for media in entry.get("media", []):
            src = str(media.get("src") or "")
            if src.lower().endswith(".png"):
                return src
    raise RuntimeError("portfolio-data.js references no PNG media")


# --- one mutation per control ------------------------------------------------


def break_doc_section(root: Path) -> str:
    doc = first_doc(root, REQUIRED_SECTION)
    lines = doc.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [ln for ln in lines if ln.strip() != f"## {REQUIRED_SECTION}"]
    if len(kept) == len(lines):
        raise RuntimeError(f"'{REQUIRED_SECTION}' heading not found as its own line in {doc.name}")
    rewrite_text(doc, "".join(kept))
    return f"{doc.relative_to(root).as_posix()}: removed '## {REQUIRED_SECTION}'"


def break_frontmatter(root: Path) -> str:
    doc = first_doc(root)
    lines = doc.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise RuntimeError(f"{doc.name} does not start with a frontmatter fence")
    closing = next((i for i, ln in enumerate(lines[1:], start=1) if ln.strip() == "---"), None)
    if closing is None:
        raise RuntimeError(f"{doc.name} has no closing frontmatter fence")
    lines[closing] = "--\n"
    rewrite_text(doc, "".join(lines))
    return f"{doc.relative_to(root).as_posix()}: closing '---' fence became '--'"


def empty_referenced_asset(root: Path) -> str:
    src = referenced_png(root)
    path = root / src
    rewrite_bytes(path, b"")
    return f"{src}: truncated to 0 bytes"


def untrack_referenced_asset(root: Path) -> str:
    src = referenced_png(root)
    subprocess.run(
        ["git", "update-index", "--force-remove", "--", src],
        cwd=str(root),
        check=True,
        capture_output=True,
    )
    size = (root / src).stat().st_size
    return f"{src}: dropped from the git index, still on disk ({size} bytes)"


def add_slop(root: Path) -> str:
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")
    rewrite_text(readme, text.rstrip("\n") + "\n\nA holistic view of the whole studio.\n")
    return "README.md: appended a banned lexicon word ('holistic')"


def track_vault_file(root: Path) -> str:
    vault = root / "docs" / "vault"
    vault.mkdir(parents=True, exist_ok=True)
    leak = vault / "self-test-leak.md"
    leak.write_text("---\nid: self-test-leak\n---\n\nNever meant to be tracked.\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "-f", leak.relative_to(root).as_posix()],
        cwd=str(root),
        check=True,
        capture_output=True,
    )
    return f"{leak.relative_to(root).as_posix()}: force-added despite the ignore rule"


def delete_entry_doc(root: Path) -> str:
    doc = first_doc(root)
    ident = doc_id(doc)
    doc.unlink()
    return f"{doc.relative_to(root).as_posix()} (id {ident}): deleted outright"


def append_media_byte(root: Path) -> str:
    src = referenced_png(root)
    path = root / src
    data = path.read_bytes()
    rewrite_bytes(path, data + b"\x00")
    return f"{src}: appended 1 trailing byte ({len(data)} -> {len(data) + 1} bytes, still non-empty)"


def edit_doc_without_rebuild(root: Path) -> str:
    doc = first_doc(root)
    ident = doc_id(doc)
    text = doc.read_text(encoding="utf-8")
    rewrite_text(doc, text.rstrip("\n") + "\n\nThe self-test adds this line and skips the rebuild.\n")
    return f"{doc.relative_to(root).as_posix()} (id {ident}): appended a sentence, bundle untouched"


@dataclass(frozen=True)
class Control:
    name: str
    mutate: Callable[[Path], str]
    target: str
    marker: str


CONTROLS = [
    Control("gate2_doc_section", break_doc_section, "verify", "Gate 2: Missing section"),
    Control("gate2_frontmatter", break_frontmatter, "verify", "Invalid YAML frontmatter"),
    Control("gate2_entry_missing", delete_entry_doc, "verify", "Gate 2 (Baseline)"),
    Control("gate3_missing_asset", empty_referenced_asset, "verify", "Gate 3: Missing/empty media"),
    Control("gate3_untracked_asset", untrack_referenced_asset, "verify", "is not tracked in git"),
    Control("gate4_slop", add_slop, "verify", "Gate 4 (Anti-Slop)"),
    Control("gate5_vault_tracked", track_vault_file, "verify", "Gate 5 (Vault Leak)"),
    Control("freshness_media", append_media_byte, "freshness", "sha256"),
    Control("freshness_doc", edit_doc_without_rebuild, "freshness", "STALE"),
    Control("build_frontmatter", break_frontmatter, "freshness", "Could not rebuild"),
]


def run_check(root: Path, target: str) -> tuple[int, str]:
    proc = subprocess.run(
        COMMANDS[target],
        cwd=str(root),
        capture_output=True,
        text=True,
        errors="replace",
        timeout=600,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def excerpt(output: str, lines: int = 12) -> str:
    tail = [ln for ln in output.strip().splitlines() if ln.strip()][-lines:]
    return "\n".join(f"      {ln}" for ln in tail)


def main() -> int:
    scratch = Path(tempfile.mkdtemp(prefix=SCRATCH_PREFIX, dir=str(PORTFOLIO_ROOT)))
    problems: list[str] = []
    try:
        baseline = scratch / "_baseline"
        copy_tree(PORTFOLIO_ROOT, baseline)
        init_repo(baseline)

        # Without a green baseline, every control below would "pass" by default.
        for target in COMMANDS:
            code, output = run_check(baseline, target)
            state = "green" if code == 0 else f"RED (exit {code})"
            print(f"[baseline] {target}: {state}")
            if code != 0:
                problems.append(f"baseline {target} exited {code} on an untouched copy")
                print(excerpt(output))

        print()
        for control in CONTROLS:
            case_root = scratch / control.name
            copy_tree(baseline, case_root)
            init_repo(case_root)
            detail = control.mutate(case_root)
            code, output = run_check(case_root, control.target)
            matched = control.marker in output

            if code != 0 and matched:
                print(f"[control] {control.name}: {control.target} exit {code}, "
                      f"matched '{control.marker}' - OK")
                print(f"          {detail}")
            else:
                why = "stayed green" if code == 0 else f"exited {code} without '{control.marker}'"
                print(f"[control] {control.name}: {control.target} {why} - FAILED")
                print(f"          {detail}")
                print(excerpt(output))
                problems.append(f"control '{control.name}' did not turn its check red ({why})")
    finally:
        if not force_rmtree(scratch):
            print(f"[warn] could not fully remove the scratch tree: {scratch}", file=sys.stderr)

    print()
    if problems:
        print("=== A GATE HAS GONE QUIET ===")
        for problem in problems:
            print(f"  [X] {problem}")
        return 1

    print(f"=== ALL {len(CONTROLS)} CONTROLS TURNED THEIR CHECK RED (baseline green) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
