#!/usr/bin/env python3
"""
Stale-bundle guard: fails when portfolio-data.js no longer matches docs/ + assets/.

Why this exists: portfolio-data.js is generated, and GitHub Pages serves whatever
was committed. Editing a doc or diagram without recompiling means the live atlas
silently keeps showing the old payload.

How it works: tools/build_portfolio.py is imported and re-run with its output
redirected into a temp directory, so the working tree is never touched. The fresh
payload is then compared against the committed portfolio-data.js.

Two things are deliberately ignored when comparing:
  - compiled_at, a wall-clock timestamp that changes on every build.
  - Fields that come only from data/master_manifest.json (memory/conversation
    ids and counts). data/ is gitignored, so CI has no manifest; ignoring these
    keeps the same check meaningful both locally and in CI. When the manifest is
    missing, a stub manifest is used so the build can still run.

Exit codes: 0 = bundle is current, 1 = bundle is stale, 2 = the rebuild failed.
"""

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = PORTFOLIO_ROOT / "tools" / "build_portfolio.py"
MANIFEST_PATH = PORTFOLIO_ROOT / "data" / "master_manifest.json"
BUNDLE_PATH = PORTFOLIO_ROOT / "portfolio-data.js"
BUNDLE_PREFIX = "window.PORTFOLIO_DATA = "

# Populated by tools/build_portfolio.py from data/master_manifest.json only.
MANIFEST_ONLY_FIELDS = {
    "memory_ids",
    "conversation_ids",
    "memory_count",
    "conversation_count",
}

STUB_MANIFEST = {"inception_date": "2026-08-16", "pillars": [], "entries": []}


def load_build_module():
    spec = importlib.util.spec_from_file_location("build_portfolio", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_bundle_text(text: str) -> dict:
    idx = text.find(BUNDLE_PREFIX)
    if idx == -1:
        raise ValueError(f"{BUNDLE_PREFIX!r} assignment missing")
    payload = text[idx + len(BUNDLE_PREFIX):].rstrip()
    if payload.endswith(";"):
        payload = payload[:-1]
    return json.loads(payload)


def rebuild_into(scratch: Path) -> tuple[dict, bool]:
    """Recompile the public bundle into `scratch`. Returns (bundle, used_stub_manifest)."""
    build = load_build_module()

    used_stub = not MANIFEST_PATH.exists()
    if used_stub:
        stub_path = scratch / "master_manifest.json"
        stub_path.write_text(json.dumps(STUB_MANIFEST), encoding="utf-8")
        build.MANIFEST_PATH = stub_path

    build.OUTPUT_JS_PATH = scratch / "portfolio-data.js"
    build.OUTPUT_VAULT_JS_PATH = scratch / "portfolio-vault.js"

    if build.compile_portfolio() != 0:
        raise RuntimeError("tools/build_portfolio.py failed to compile the bundle")

    if not build.OUTPUT_JS_PATH.exists():
        raise RuntimeError("tools/build_portfolio.py produced no portfolio-data.js")

    return parse_bundle_text(build.OUTPUT_JS_PATH.read_text(encoding="utf-8")), used_stub


def comparable(entry: dict) -> dict:
    return {k: v for k, v in entry.items() if k not in MANIFEST_ONLY_FIELDS}


def main() -> int:
    if not BUNDLE_PATH.exists():
        print(f"[FAIL] {BUNDLE_PATH.name} is missing. Run: python tools/build_portfolio.py")
        return 1

    committed_bundle = parse_bundle_text(BUNDLE_PATH.read_text(encoding="utf-8"))

    try:
        with tempfile.TemporaryDirectory() as tmp:
            fresh_bundle, used_stub = rebuild_into(Path(tmp))
    except Exception as exc:  # surface any rebuild failure verbatim
        print(f"[FAIL] Could not rebuild the bundle: {exc}", file=sys.stderr)
        return 2

    committed = {e["id"]: comparable(e) for e in committed_bundle.get("entries", [])}
    fresh = {e["id"]: comparable(e) for e in fresh_bundle.get("entries", [])}

    problems = []

    for entry_id in sorted(fresh.keys() - committed.keys()):
        problems.append(
            f"{entry_id}: documented in docs/ but absent from portfolio-data.js "
            "(new entry never compiled)"
        )

    for entry_id in sorted(committed.keys() - fresh.keys()):
        problems.append(
            f"{entry_id}: still in portfolio-data.js but no longer exists under docs/ "
            "(removed or renamed entry never recompiled)"
        )

    for entry_id in sorted(fresh.keys() & committed.keys()):
        old, new = committed[entry_id], fresh[entry_id]
        changed = [k for k in new if old.get(k) != new[k]]
        changed += [k for k in old if k not in new]
        if changed:
            problems.append(f"{entry_id}: {', '.join(sorted(set(changed)))}")

    if problems:
        count = len(problems)
        print("=== portfolio-data.js IS STALE ===")
        print(f"{count} entr{'y differs' if count == 1 else 'ies differ'} from docs/ + assets/:\n")
        for problem in problems:
            print(f"  [X] {problem}")
        print("\nRegenerate the payload and commit it:")
        print("  python tools/build_portfolio.py")
        print("  git add portfolio-data.js && git commit")
        return 1

    note = " (stub manifest: data/master_manifest.json not present)" if used_stub else ""
    print(
        f"[OK] portfolio-data.js is current: {len(committed)} entries match docs/ + assets/{note}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
