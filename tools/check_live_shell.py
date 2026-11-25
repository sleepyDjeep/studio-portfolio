#!/usr/bin/env python3
"""
Live shell check: the deployed page, not just its data file.

tools/check_bundle_freshness.py proves the live portfolio-data.js matches docs/,
but it says nothing about the rest of the deploy. A Pages build that serves a 404
for app.js, styles.css or an image keeps the data check green while the atlas is
blank or full of broken tiles, so this script fetches the shell, every sound clip
and a slice of the images and diagrams the payload references, requiring a 200
with the content type the page needs.

Assets come from the committed portfolio-data.js, so the check follows the real
payload instead of a hardcoded path list. Media bytes are also hashed and compared
against the sha256 the bundle records for that path: a 200 of the right type
proves something is served, not that it is the file the page was built with.

Hashing every image would pull about 141 MB each run, so the images and diagrams
are split into four slices and one slice is hashed per day, chosen from the UTC
date. Over four consecutive days the whole payload is covered, and the run prints
which slice it took. The sound clips are hashed every run because all four add up
to less than a megabyte.

    python tools/check_live_shell.py
    python tools/check_live_shell.py --base https://example.com/portfolio/
    python tools/check_live_shell.py --full     # every asset in one run
    python tools/check_live_shell.py --slice 3  # a specific slice of four

Exit codes: 0 = everything served correctly, 1 = a check failed.
"""

import argparse
import datetime
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
DEFAULT_SLICES = 4

# (path, required substring of Content-Type, substrings the body must contain)
SHELL = [
    ("", "text/html", ("app.js", "styles.css")),
    ("app.js", "javascript", ()),
    ("styles.css", "text/css", ()),
    ("portfolio-data.js", "javascript", ()),
]

# Extension -> required substring of Content-Type. Audio matches on the prefix
# because Pages serves the same .wav as either audio/wav or audio/x-wav.
CONTENT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".wav": "audio/",
}


def load_bundle(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    idx = raw.find(BUNDLE_PREFIX)
    if idx == -1:
        raise SystemExit(f"[shell] {path.name} has no {BUNDLE_PREFIX!r} assignment")
    return json.loads(raw[idx + len(BUNDLE_PREFIX):].rstrip().rstrip(";"))


def asset_targets(bundle: dict) -> list[tuple[str, str | None, str | None]]:
    """Every media file and diagram the payload references, sorted, with its digest.

    The same image can be used by several entries, so paths are deduplicated.
    Diagrams are rendered from the inlined SVG, but the file itself still ships
    and the builder records its sha256, so it is compared like any media file.
    """
    found: dict[str, str | None] = {}
    for entry in bundle.get("entries", []):
        for item in entry.get("media", []):
            src = str(item.get("src") or "")
            if src and src not in found:
                found[src] = item.get("sha256")
        diagram = entry.get("diagram")
        if diagram and str(diagram) not in found:
            found[str(diagram)] = entry.get("diagram_sha256")

    targets = []
    for path in sorted(found):
        targets.append((path, CONTENT_TYPES.get(Path(path).suffix.lower()), found[path]))
    return targets


def split_targets(targets):
    """Sound clips are cheap enough for every run; everything else takes turns."""
    always = [target for target in targets if (target[1] or "").startswith("audio/")]
    rotating = [target for target in targets if not (target[1] or "").startswith("audio/")]
    return always, rotating


def pick_slice(rotating, slices: int, index: int):
    """Interleaved slices: consecutive days never overlap, together they cover all."""
    return rotating[index::slices]


def fetch(url: str) -> tuple[int, str, bytes]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "studio-portfolio-live-shell", "Cache-Control": "no-cache"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.status, response.headers.get("Content-Type", ""), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", "") if exc.headers else "", b""
    except urllib.error.URLError as exc:
        print(f"[shell] could not reach {url}: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch the deployed shell and a slice of its assets, asserting each is served.")
    parser.add_argument("--base", default=DEFAULT_BASE, help=f"site root URL (default: {DEFAULT_BASE})")
    parser.add_argument("--bundle", default=str(BUNDLE_PATH), help="local bundle to sample asset paths from")
    parser.add_argument("--slices", type=int, default=DEFAULT_SLICES, help=f"rotating slices to split the assets into (default: {DEFAULT_SLICES})")
    parser.add_argument("--slice", type=int, help="1-based slice to check instead of the one the date selects")
    parser.add_argument("--full", action="store_true", help="check every asset in this run instead of one slice")
    args = parser.parse_args()

    if args.full:
        slices = 1
        index = 0
    else:
        slices = args.slices
        if slices < 1:
            parser.error("--slices must be at least 1")
        if args.slice is not None:
            if not 1 <= args.slice <= slices:
                parser.error(f"--slice must be between 1 and {slices}")
            index = args.slice - 1
        else:
            # The UTC date picks the slice, so a manual rerun of the same day and
            # the scheduled run look at the same assets.
            index = datetime.datetime.now(datetime.timezone.utc).toordinal() % slices

    base = args.base if args.base.endswith("/") else args.base + "/"
    stamp = os.environ.get("GITHUB_RUN_ID") or str(int(time.time()))

    always, rotating = split_targets(asset_targets(load_bundle(Path(args.bundle))))
    chosen = pick_slice(rotating, slices, index)
    if slices == 1:
        print(f"[slate] hashing all {len(rotating)} images and diagrams plus {len(always)} sound clips")
    else:
        print(f"[slate] slice {index + 1}/{slices}: {len(chosen)} of {len(rotating)} images and diagrams "
              f"plus {len(always)} sound clips; the other {len(rotating) - len(chosen)} follow on the next {slices - 1} runs")

    targets = [(path, ctype, (), None) for path, ctype, _ in SHELL]
    targets += [(path, ctype, (), digest) for path, ctype, digest in always + chosen]
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
            if expected_type and expected_type not in lowered:
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
            elif path.startswith("assets/"):
                digest = "no digest in bundle"
            else:
                digest = ""
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
    span = "all assets" if slices == 1 else f"slice {index + 1}/{slices} of {len(rotating)} assets"
    print(f"=== LIVE SHELL OK: {len(targets)} paths served as expected, "
          f"{hashed} byte-identical to the bundle ({span}) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
