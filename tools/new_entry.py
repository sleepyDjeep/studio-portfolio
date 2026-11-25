#!/usr/bin/env python3
"""
Entry scaffold: write a new portfolio entry that already satisfies Gate 2.

    python tools/new_entry.py 02-games-engines my-new-game \
        --title "My New Game" --subtitle "One sentence on what it is." \
        --media "D:/captures/menu.png::Main menu at 1440p." \
        --diagram assets/diagrams/my-new-game.svg

What it does:
  * writes docs/<pillar>/<slug>.md with the frontmatter Gate 2 requires, using
    the enum values the page understands;
  * copies each --media file into assets/media/<slug>/ (or keeps it where it is
    when that is already the destination) and records the caption the page uses
    as alt text;
  * copies --diagram into assets/diagrams/<slug>.svg;
  * creates assets/media/<slug>/ and prints the baseline and rebuild commands.

A caption is mandatory for images because tools/verify_portfolio.py now requires
one; audio only needs a file. Sections start as explicit TODO placeholders long
enough to pass the 80-character rule, so the entry is valid while you write it.

Exit codes: 0 = written, 2 = bad arguments or an existing entry.
"""

import argparse
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PORTFOLIO_ROOT / "docs"
MANIFEST_PATH = PORTFOLIO_ROOT / "tools" / "public_manifest.json"
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
AUDIO_SUFFIXES = {".wav", ".mp3", ".ogg", ".flac"}

SECTIONS = (
    (
        "What It Is & Why It Matters",
        "TODO: Replace this placeholder. Say what the thing is and why it matters, "
        "in at least 80 characters so Gate 2 accepts the section until the real text lands.",
    ),
    (
        "Real Example: How It Works in Practice",
        "- **Input**: TODO: what the user provides.\n"
        "- **What Happens**: TODO: what the system does with it.\n"
        "- **Output**: TODO: what comes back.",
    ),
    (
        "Where It Stands & Next Steps",
        "TODO: Replace this placeholder with the current state and the next concrete "
        "step; the section needs at least 80 characters.",
    ),
    (
        "Under the Hood & Local Files",
        "TODO: Replace this placeholder with the real paths, commands and architecture "
        "notes; the section needs at least 80 characters.",
    ),
)


def fail(message: str) -> "argparse.Namespace":
    raise SystemExit(f"[new_entry] {message}")


def pillar_ids() -> set[str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {str(p["id"]) for p in manifest.get("pillars", []) if p.get("id") != "vault"}


def parse_media(spec: str) -> tuple[Path, str]:
    """`path::caption` -> (path, caption). The caption is required for images."""
    path_text, _, caption = spec.partition("::")
    path = Path(path_text.strip())
    if not path.is_file():
        fail(f"media file not found: {path}")
    return path, caption.strip()


def media_kind(path: Path) -> str:
    if path.suffix.lower() in AUDIO_SUFFIXES:
        return "audio"
    if "assets/concepts" in path.as_posix().lower():
        return "concept"
    return "authentic"


def place_media(source: Path, slug: str) -> tuple[str, str]:
    dest_dir = PORTFOLIO_ROOT / "assets" / "media" / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    if source.resolve() != dest.resolve():
        if dest.exists():
            fail(f"{dest.relative_to(PORTFOLIO_ROOT).as_posix()} already exists; rename the source")
        shutil.copy2(source, dest)
    return dest.relative_to(PORTFOLIO_ROOT).as_posix(), media_kind(source)


def place_diagram(source: Path, slug: str) -> str:
    if source.suffix.lower() != ".svg":
        fail(f"diagram must be an .svg (the page inlines it): {source}")
    dest_dir = PORTFOLIO_ROOT / "assets" / "diagrams"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slug}.svg"
    if source.resolve() != dest.resolve():
        if dest.exists():
            fail(f"{dest.relative_to(PORTFOLIO_ROOT).as_posix()} already exists")
        shutil.copy2(source, dest)
    return dest.relative_to(PORTFOLIO_ROOT).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a Gate 2-valid portfolio entry.")
    parser.add_argument("pillar", help="pillar folder id, e.g. 02-games-engines")
    parser.add_argument("slug", help="entry id and filename stem, lowercase and hyphenated")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--type", default="project", choices=["project", "workflow", "idea"])
    parser.add_argument(
        "--readiness",
        default="shipped",
        choices=["shipped", "active-build", "reusable-workflow", "blueprint"],
    )
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--tag", action="append", default=[], help="repeatable")
    parser.add_argument(
        "--media",
        action="append",
        default=[],
        metavar="PATH::CAPTION",
        help="repeatable; the caption after '::' is required for images",
    )
    parser.add_argument("--diagram", help="SVG path; copied to assets/diagrams/<slug>.svg")
    args = parser.parse_args()

    if args.pillar not in pillar_ids():
        fail(f"unknown pillar '{args.pillar}' (choose from {', '.join(sorted(pillar_ids()))})")
    if not SLUG_RE.match(args.slug):
        fail(f"slug '{args.slug}' must be lowercase letters, digits and hyphens")
    try:
        datetime.date.fromisoformat(args.date)
    except ValueError:
        fail(f"--date '{args.date}' is not YYYY-MM-DD")

    doc_path = DOCS_DIR / args.pillar / f"{args.slug}.md"
    if doc_path.exists():
        fail(f"{doc_path.relative_to(PORTFOLIO_ROOT).as_posix()} already exists")

    media = []
    for spec in args.media:
        source, caption = parse_media(spec)
        if not caption and media_kind(source) in {"authentic", "concept"}:
            fail(f"{source.name} needs a caption: --media \"{source}::what it shows\"")
        src, kind = place_media(source, args.slug)
        media.append({"src": src, "kind": kind, **({"caption": caption} if caption else {})})

    diagram = place_diagram(Path(args.diagram), args.slug) if args.diagram else ""
    if not media and not diagram:
        fail("an entry needs at least one --media or --diagram (Gate 2 requires a visual)")

    (PORTFOLIO_ROOT / "assets" / "media" / args.slug).mkdir(parents=True, exist_ok=True)

    meta = {
        "id": args.slug,
        "title": args.title,
        "subtitle": args.subtitle,
        "pillar": args.pillar,
        "entry_type": args.type,
        "readiness": args.readiness,
        "visibility": "main",
        "date_started": args.date,
        "date_updated": args.date,
    }
    if args.tag:
        meta["tags"] = args.tag
    if media:
        meta["media"] = media
    if diagram:
        meta["diagram"] = diagram

    body = "\n\n".join(f"## {heading}\n\n{text}" for heading, text in SECTIONS)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, default_flow_style=False)
    doc_path.write_text(f"---\n{frontmatter}---\n\n{body}\n", encoding="utf-8")

    relative = doc_path.relative_to(PORTFOLIO_ROOT).as_posix()
    print(f"[new_entry] wrote {relative}")
    if media:
        print(f"[new_entry] media in assets/media/{args.slug}/")
    if diagram:
        print(f"[new_entry] diagram {diagram}")
    print("\nNext:")
    print("  python tools/verify_portfolio.py --update-baseline")
    print("  python tools/update_portfolio.py")
    print(f"  git add {relative} assets/media/{args.slug} tools/expected_entries.json portfolio-data.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
