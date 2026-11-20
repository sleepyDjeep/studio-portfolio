#!/usr/bin/env python3
"""
Stale-bundle guard: fails when a portfolio-data.js no longer matches docs/ + assets/.

Why this exists: portfolio-data.js is generated, and GitHub Pages serves whatever
was committed. Editing a doc, diagram, or artwork without recompiling means the
live atlas keeps showing the old payload.

How it works: tools/build_portfolio.py is imported and re-run with its output
redirected into a temp directory, so the working tree is never touched. The fresh
payload is then compared against a bundle: the committed portfolio-data.js by
default, or another copy such as the live site through --bundle.

Ignored when comparing:
  - compiled_at, a wall-clock timestamp that changes on every build.
  - Values only the private manifest can supply (memory and conversation ids and
    counts), because data/ is gitignored and CI builds from the committed
    redacted tools/public_manifest.json instead.

Comparison covers every entry field, each media item (including the sha256 of the
file behind it), the payload summary, the pillar list, and the inception date.

Exit codes: 0 = bundle is current, 1 = bundle is stale, 2 = could not check.
"""

import argparse
import importlib.util
import json
import sys
import tempfile
import urllib.request
from pathlib import Path

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = PORTFOLIO_ROOT / "tools" / "build_portfolio.py"
MANIFEST_PATH = PORTFOLIO_ROOT / "data" / "master_manifest.json"
BUNDLE_PATH = PORTFOLIO_ROOT / "portfolio-data.js"
BUNDLE_PREFIX = "window.PORTFOLIO_DATA = "

# Populated by tools/build_portfolio.py from the private manifest only.
MANIFEST_ONLY_FIELDS = {
    "memory_ids",
    "conversation_ids",
    "memory_count",
    "conversation_count",
}

# Payload-level fields that are fully derived from docs/ + the manifest.
SHAPE_KEYS = ("inception_date", "pillars", "summary")


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


def read_bundle(ref: str) -> dict:
    """Load a bundle from a filesystem path or an http(s) URL."""
    if ref.startswith(("http://", "https://")):
        request = urllib.request.Request(ref, headers={"User-Agent": "studio-portfolio-freshness"})
        with urllib.request.urlopen(request, timeout=60) as response:
            return parse_bundle_text(response.read().decode("utf-8"))

    path = Path(ref)
    if not path.is_absolute():
        path = PORTFOLIO_ROOT / path
    return parse_bundle_text(path.read_text(encoding="utf-8"))


def rebuild_into(scratch: Path) -> dict:
    build = load_build_module()
    build.OUTPUT_JS_PATH = scratch / "portfolio-data.js"
    build.OUTPUT_VAULT_JS_PATH = scratch / "portfolio-vault.js"

    if build.compile_portfolio() != 0:
        raise RuntimeError("tools/build_portfolio.py failed to compile the bundle")

    if not build.OUTPUT_JS_PATH.exists():
        raise RuntimeError("tools/build_portfolio.py produced no portfolio-data.js")

    return parse_bundle_text(build.OUTPUT_JS_PATH.read_text(encoding="utf-8"))


def comparable(entry: dict) -> dict:
    return {k: v for k, v in entry.items() if k not in MANIFEST_ONLY_FIELDS}


def media_problems(entry_id: str, old_media: list, new_media: list) -> list:
    """Diff media items by src so a replaced file is named, not just 'media'."""
    old = {str(m.get("src")): m for m in old_media or []}
    new = {str(m.get("src")): m for m in new_media or []}
    problems = []

    for src in sorted(new.keys() - old.keys()):
        problems.append(f"{entry_id}: media[{src}] added")
    for src in sorted(old.keys() - new.keys()):
        problems.append(f"{entry_id}: media[{src}] removed")

    for src in sorted(old.keys() & new.keys()):
        changed = [k for k in new[src] if old[src].get(k) != new[src][k]]
        changed += [k for k in old[src] if k not in new[src]]
        if changed:
            problems.append(f"{entry_id}: media[{src}] {', '.join(sorted(set(changed)))}")

    return problems


def entry_problems(committed: dict, fresh: dict) -> list:
    problems = []

    for entry_id in sorted(fresh.keys() - committed.keys()):
        problems.append(
            f"{entry_id}: documented in docs/ but absent from the bundle (never compiled)"
        )

    for entry_id in sorted(committed.keys() - fresh.keys()):
        problems.append(
            f"{entry_id}: present in the bundle but no longer under docs/ (removed or renamed)"
        )

    for entry_id in sorted(fresh.keys() & committed.keys()):
        old, new = committed[entry_id], fresh[entry_id]
        changed = [k for k in new if k != "media" and old.get(k) != new[k]]
        changed += [k for k in old if k not in new]
        if changed:
            problems.append(f"{entry_id}: {', '.join(sorted(set(changed)))}")
        problems.extend(media_problems(entry_id, old.get("media"), new.get("media")))

    return problems


def shape_problems(committed: dict, fresh: dict) -> list:
    problems = []

    for key in SHAPE_KEYS:
        old, new = committed.get(key), fresh.get(key)
        if old == new:
            continue
        if isinstance(old, dict) and isinstance(new, dict):
            changed = [k for k in sorted(set(old) | set(new)) if old.get(k) != new.get(k)]
            problems.append(f"(payload) {key}: {', '.join(changed)}")
        else:
            problems.append(f"(payload) {key} differs")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail when a bundle no longer matches docs/ + assets/.")
    parser.add_argument(
        "--bundle",
        default=str(BUNDLE_PATH),
        help="bundle to check: a filesystem path or an http(s) URL (default: the committed portfolio-data.js)",
    )
    args = parser.parse_args()

    remote = args.bundle.startswith(("http://", "https://"))
    target = args.bundle

    if not remote:
        bundle_file = Path(target)
        if not bundle_file.is_absolute():
            bundle_file = PORTFOLIO_ROOT / bundle_file
        if not bundle_file.exists():
            print(f"[FAIL] Bundle not found: {target}", file=sys.stderr)
            print("       Run: python tools/update_portfolio.py", file=sys.stderr)
            return 1
        target = str(bundle_file)

    try:
        committed_bundle = read_bundle(target)
    except Exception as exc:  # network, 404, malformed payload
        print(f"[FAIL] Could not read {target}: {exc}", file=sys.stderr)
        return 2

    try:
        with tempfile.TemporaryDirectory() as tmp:
            fresh_bundle = rebuild_into(Path(tmp))
    except Exception as exc:  # surface any rebuild failure verbatim
        print(f"[FAIL] Could not rebuild the bundle: {exc}", file=sys.stderr)
        return 2

    committed = {e["id"]: comparable(e) for e in committed_bundle.get("entries", [])}
    fresh = {e["id"]: comparable(e) for e in fresh_bundle.get("entries", [])}

    problems = entry_problems(committed, fresh) + shape_problems(committed_bundle, fresh_bundle)

    if problems:
        count = len(problems)
        label = target if remote else Path(target).name
        print(f"=== {label} IS STALE ===")
        print(f"{count} difference{'s' if count != 1 else ''} from docs/ + assets/:\n")
        for problem in problems:
            print(f"  [X] {problem}")
        print()
        if remote:
            print("The live page is serving a payload older than the committed docs.")
            print("Rebuild, commit, and let Pages redeploy:")
            print("  python tools/update_portfolio.py")
        else:
            print("Regenerate the payload and commit it:")
            print("  python tools/update_portfolio.py")
            print("  git add portfolio-data.js && git commit")
        return 1

    note = "" if MANIFEST_PATH.exists() else " (built from tools/public_manifest.json)"
    print(f"[OK] {Path(target).name if not remote else target} is current: "
          f"{len(committed)} entries match docs/ + assets/{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
