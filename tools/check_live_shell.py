#!/usr/bin/env python3
"""
Live shell check: the deployed page, not just its data file.

tools/check_bundle_freshness.py proves the live portfolio-data.js matches docs/,
but it says nothing about the rest of the deploy. A Pages build that serves a 404
for app.js, styles.css or an image keeps the data check green while the atlas is
blank or full of broken tiles, so this script fetches the shell and a few
representative assets and requires a 200 with the content type the page needs.

Assets are sampled from the committed portfolio-data.js, so the check follows the
real payload instead of a hardcoded path list.

    python tools/check_live_shell.py
    python tools/check_live_shell.py --base https://example.com/portfolio/

Exit codes: 0 = everything served correctly, 1 = a check failed.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = PORTFOLIO_ROOT / "portfolio-data.js"
BUNDLE_PREFIX = "window.PORTFOLIO_DATA = "
DEFAULT_BASE = "https://sleepydjeep.github.io/studio-portfolio/"

# (path, required substring of Content-Type, substrings the body must contain)
SHELL = [
    ("", "text/html", ("app.js", "styles.css")),
    ("app.js", "javascript", ()),
    ("styles.css", "text/css", ()),
    ("portfolio-data.js", "javascript", ()),
]

ASSET_TYPES = [(".png", "image/png"), (".jpg", "image/jpeg"), (".svg", "image/svg+xml")]


def load_bundle(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    idx = raw.find(BUNDLE_PREFIX)
    if idx == -1:
        raise SystemExit(f"[shell] {path.name} has no {BUNDLE_PREFIX!r} assignment")
    return json.loads(raw[idx + len(BUNDLE_PREFIX):].rstrip().rstrip(";"))


def sample_assets(bundle: dict) -> list[tuple[str, str]]:
    """One asset per media type the payload actually references."""
    entries = bundle.get("entries", [])
    media = [str(m.get("src") or "") for e in entries for m in e.get("media", [])]
    diagrams = [str(e.get("diagram") or "") for e in entries if e.get("diagram")]

    picked: list[tuple[str, str]] = []
    for suffix, content_type in ASSET_TYPES:
        source = diagrams if suffix == ".svg" else media
        match = next((path for path in source if path.lower().endswith(suffix)), None)
        if match:
            picked.append((match, content_type))
    return picked


def fetch(url: str) -> tuple[int, str, bytes]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "studio-portfolio-live-shell", "Cache-Control": "no-cache"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, response.headers.get("Content-Type", ""), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", "") if exc.headers else "", b""
    except urllib.error.URLError as exc:
        print(f"[shell] could not reach {url}: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch the deployed shell and sample assets, asserting each is served.")
    parser.add_argument("--base", default=DEFAULT_BASE, help=f"site root URL (default: {DEFAULT_BASE})")
    parser.add_argument("--bundle", default=str(BUNDLE_PATH), help="local bundle to sample asset paths from")
    args = parser.parse_args()

    base = args.base if args.base.endswith("/") else args.base + "/"
    stamp = os.environ.get("GITHUB_RUN_ID") or str(int(time.time()))

    targets = list(SHELL) + [(path, ctype, ()) for path, ctype in sample_assets(load_bundle(Path(args.bundle)))]
    failures = []

    for path, expected_type, must_contain in targets:
        label = path or "index.html"
        status, content_type, body = fetch(f"{base}{path}?run={stamp}")
        lowered = content_type.lower()

        problems = []
        if status != 200:
            # One reason is enough: a 404 tells you nothing about the content type.
            problems.append(f"HTTP {status} (expected 200)")
        else:
            if expected_type not in lowered:
                problems.append(f"Content-Type '{content_type or '<none>'}' (expected '{expected_type}')")
            if not body:
                problems.append("empty body")
            for needle in must_contain:
                if needle.encode() not in body:
                    problems.append(f"body never mentions '{needle}'")

        if problems:
            print(f"[X] {label:<48} " + "; ".join(problems))
            failures.append(label)
        else:
            print(f"[ok] {label:<48} {status} {content_type:<28} {len(body):>9,} bytes")

    print()
    if failures:
        print("=== LIVE SHELL IS NOT SERVING ===")
        for failure in failures:
            print(f"  [X] {failure}")
        print()
        print("The deploy is incomplete: the data file may be current while the page it feeds is not.")
        return 1

    print(f"=== LIVE SHELL OK: {len(targets)} paths served with the expected content types ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
