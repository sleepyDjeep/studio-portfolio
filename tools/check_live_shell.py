#!/usr/bin/env python3
"""
Live shell check: the deployed page, not just its data file.

tools/check_bundle_freshness.py proves the live portfolio-data.js matches docs/,
but it says nothing about the rest of the deploy. A Pages build that serves a 404
for app.js, styles.css or an image keeps the data check green while the atlas is
blank or full of broken tiles, so this script fetches the shell and a few
representative assets (one of each image type plus every sound clip) and requires
a 200 with the content type the page needs.

Assets are sampled from the committed portfolio-data.js, so the check follows the
real payload instead of a hardcoded path list. Media bytes are also hashed and
compared against the sha256 the bundle records for that path: a 200 of the right
type proves something is served, not that it is the file the page was built with.

    python tools/check_live_shell.py
    python tools/check_live_shell.py --base https://example.com/portfolio/

Exit codes: 0 = everything served correctly, 1 = a check failed.
"""

import argparse
import hashlib
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

# (suffix, required substring of Content-Type, how many to check: None = all).
# Images are sampled because there are hundreds; the four sound clips are all
# fetched because each is a few kilobytes. Audio matches on the type prefix
# because Pages serves the same .wav as either audio/wav or audio/x-wav.
ASSET_TYPES = [
    (".png", "image/png", 1),
    (".jpg", "image/jpeg", 1),
    (".svg", "image/svg+xml", 1),
    (".wav", "audio/", None),
]


def load_bundle(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    idx = raw.find(BUNDLE_PREFIX)
    if idx == -1:
        raise SystemExit(f"[shell] {path.name} has no {BUNDLE_PREFIX!r} assignment")
    return json.loads(raw[idx + len(BUNDLE_PREFIX):].rstrip().rstrip(";"))


def sample_assets(bundle: dict) -> list[tuple[str, str, str | None]]:
    """One asset per image type, every sound clip, with the recorded digest if any.

    Diagrams live inside the bundle as inline SVG, so their .svg file has no
    recorded sha256 and can only be checked for type and reachability.
    """
    entries = bundle.get("entries", [])
    media = [(str(m.get("src") or ""), m.get("sha256")) for e in entries for m in e.get("media", [])]
    diagrams = [(str(e.get("diagram")), None) for e in entries if e.get("diagram")]

    picked: list[tuple[str, str, str | None]] = []
    for suffix, content_type, limit in ASSET_TYPES:
        source = diagrams if suffix == ".svg" else media
        matches = [item for item in source if item[0].lower().endswith(suffix)]
        for path, digest in matches[:limit] if limit else matches:
            picked.append((path, content_type, digest))
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

    targets = [(path, ctype, (), None) for path, ctype, _ in SHELL]
    targets += [(path, ctype, (), digest) for path, ctype, digest in sample_assets(load_bundle(Path(args.bundle)))]
    failures = []
    drifted = []

    for path, expected_type, must_contain, expected_sha in targets:
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
            if expected_sha and body:
                served_sha = hashlib.sha256(body).hexdigest()
                if served_sha != expected_sha:
                    problems.append(
                        f"CONTENT DRIFTED: bundle records {expected_sha[:12]}, "
                        f"deploy serves {served_sha[:12]}"
                    )
                    drifted.append(path)

        if problems:
            print(f"[X] {label:<48} " + "; ".join(problems))
            failures.append(label)
        else:
            if expected_sha:
                digest = f"sha256 {expected_sha[:12]}"
            else:
                digest = "no digest in bundle" if path.startswith("assets/") else ""
            print(f"[ok] {label:<48} {status} {content_type:<28} {len(body):>9,} bytes  {digest}")

    print()
    if failures:
        print("=== LIVE SHELL IS NOT SERVING ===")
        for failure in failures:
            print(f"  [X] {failure}")
        print()
        if drifted:
            print("These assets are served with bytes the current bundle does not describe:")
            for path in drifted:
                print(f"  [DRIFT] {path}")
            print("Rebuild, commit, and let Pages redeploy:")
            print("  python tools/update_portfolio.py")
        else:
            print("The deploy is incomplete: the data file may be current while the page it feeds is not.")
        return 1

    hashed = sum(1 for target in targets if target[3])
    print(f"=== LIVE SHELL OK: {len(targets)} paths served as expected, "
          f"{hashed} byte-identical to the bundle ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
