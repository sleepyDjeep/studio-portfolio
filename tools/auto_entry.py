#!/usr/bin/env python3
"""
Turn one intake candidate into a portfolio entry.

Two modes:

    python tools/auto_entry.py --candidate candidate.json --draft draft.json
    python tools/auto_entry.py --candidate candidate.json          # asks the LLM

The draft mode exists so the writer, the validation and the SVG sanitiser can be
tested without a model. The LLM mode sends only the candidate's facts (memory
texts, conversation titles, README head, image names) to the configured
OpenAI-compatible endpoint and expects a single JSON object back.

Environment for LLM mode:
  OPENAI_API_KEY    required
  OPENAI_BASE_URL   optional, e.g. https://freebuff.com/api/v1/paid
  AUTO_ENTRY_MODEL  optional, default gpt-4o-mini

Generated entries go through the same gates as hand-written ones; this tool only
refuses earlier (placeholders, invented section names, missing captions, unsafe
SVG) so a weak draft never reaches the commit step.
"""

import argparse
import json
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parent
PORTFOLIO_ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from verify_portfolio import (  # noqa: E402
    BANNED_PATTERNS,
    ENTRY_TYPES,
    READINESS_VALUES,
    REQUIRED_SECTIONS,
)
from new_entry import SLUG_RE, pillar_ids  # noqa: E402

PLACEHOLDERS = re.compile(r"\b(TODO|TBD|lorem ipsum|placeholder|insert here|FIXME)\b", re.I)
BANNED = re.compile("|".join(f"(?:{pattern})" for pattern in BANNED_PATTERNS), re.I)
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MIN_SECTION_CHARS = 120

DRAFT_SCHEMA = """{
  "slug": "lowercase-hyphenated-id",
  "title": "Entry title",
  "subtitle": "One sentence, specific",
  "pillar": "one of the pillar ids",
  "entry_type": "project|workflow|idea",
  "readiness": "shipped|active-build|reusable-workflow|blueprint",
  "tags": ["3-8 short tags"],
  "sections": {
    "What It Is & Why It Matters": "150-400 words, facts only",
    "Real Example: How It Works in Practice": "**Input**: ... **What Happens**: ... **Output**: ...",
    "Where It Stands & Next Steps": "current state and the next concrete step",
    "Under the Hood & Local Files": "real paths, commands and architecture"
  },
  "media": [{"file": "basename-of-a-provided-image", "caption": "what it shows"}],
  "diagram_svg": "<svg ...>...</svg>"
}"""


def log(message: str) -> None:
    print(f"[auto-entry] {message}")


def sanitize_svg(svg: str) -> str:
    """The SVG is inlined into the page, so strip anything executable or remote."""
    text = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    text = re.sub(r"<script.*?</script\s*>", "", text, flags=re.S | re.I)
    text = re.sub(r"<foreignObject.*?</foreignObject\s*>", "", text, flags=re.S | re.I)
    text = re.sub(r"\son[a-z]+\s*=\s*(\"[^\"]*\"|'[^']*')", "", text, flags=re.I)
    text = re.sub(r"\s(href|xlink:href)\s*=\s*(\"|')https?://[^\"']*(\"|')", "", text, flags=re.I)
    text = re.sub(r"javascript:", "", text, flags=re.I)
    text = text.strip()
    if not text.startswith("<svg"):
        raise SystemExit("[auto-entry] diagram_svg does not start with <svg")
    try:
        ET.fromstring(text)
    except ET.ParseError as exc:
        raise SystemExit(f"[auto-entry] diagram_svg is not valid XML: {exc}")
    return text


def build_prompt(candidate: dict) -> str:
    facts = candidate.get("facts", {})
    lines = [
        "Write one portfolio entry for a personal AI studio's living atlas.",
        "Use only the facts below. Do not invent metrics, dates, customers or outcomes.",
        "If a fact is missing, describe the work that is evidenced instead of guessing.",
        "",
        f"Workspace: {candidate.get('workspace') or 'unknown'}",
        f"Project folder: {facts.get('project_dir') or 'none'}",
        f"Suggested title: {candidate.get('title') or 'invent from the facts'}",
        f"Earliest date: {candidate.get('earliest') or ''}",
        "",
        "Memory notes:",
    ]
    for text in facts.get("texts", []):
        lines.append(f"- {text}")
    lines.append("")
    lines.append("Conversations:")
    for item in facts.get("conversations", []):
        lines.append(f"- {item}")
    if facts.get("readme"):
        lines.append("")
        lines.append("README head:")
        lines.append(facts["readme"][:4000])
    images = facts.get("images", [])
    if images:
        lines.append("")
        lines.append("Local images available (use basenames in media):")
        for image in images:
            lines.append(f"- {Path(image).name}")
    lines += [
        "",
        f"Allowed pillars: {', '.join(sorted(pillar_ids()))}",
        f"Allowed entry_type: {', '.join(sorted(ENTRY_TYPES))}",
        f"Allowed readiness: {', '.join(sorted(READINESS_VALUES))}",
        "Each section must be at least 120 characters, factual, and free of TODO/placeholder text.",
        "Use 'authentic' screenshots when images are provided; otherwise return a clean, "
        "theme-adaptive SVG diagram (no scripts, no external links) in diagram_svg and no media.",
        "",
        "Reply with one JSON object exactly in this shape, nothing else:",
        DRAFT_SCHEMA,
    ]
    return "\n".join(lines)


def ask_llm(candidate: dict) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "[auto-entry] OPENAI_API_KEY is not set; nothing was published. "
            "Put it in .env (loaded by daily_publish.py) or the environment."
        )
    from openai import OpenAI

    model = os.environ.get("AUTO_ENTRY_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key, base_url=os.environ.get("OPENAI_BASE_URL") or None)
    response = client.chat.completions.create(
        model=model,
        temperature=0.4,
        messages=[
            {"role": "system", "content": "You write accurate technical portfolio entries. Reply with JSON only."},
            {"role": "user", "content": build_prompt(candidate)},
        ],
    )
    text = (response.choices[0].message.content or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[auto-entry] model did not return JSON: {exc}: {text[:300]}")


def validate(draft: dict, images: dict[str, str]) -> list[str]:
    problems = []
    for key in ("slug", "title", "subtitle", "pillar", "entry_type", "readiness", "sections"):
        if not draft.get(key):
            problems.append(f"missing {key}")
    slug = str(draft.get("slug") or "")
    if slug and not SLUG_RE.match(slug):
        problems.append(f"slug '{slug}' is not lowercase-hyphenated")
    if draft.get("pillar") and draft["pillar"] not in pillar_ids():
        problems.append(f"pillar '{draft['pillar']}' is unknown")
    if draft.get("entry_type") and draft["entry_type"] not in ENTRY_TYPES:
        problems.append(f"entry_type '{draft['entry_type']}' is not allowed")
    if draft.get("readiness") and draft["readiness"] not in READINESS_VALUES:
        problems.append(f"readiness '{draft['readiness']}' is not allowed")

    sections = draft.get("sections") or {}
    for heading in REQUIRED_SECTIONS:
        text = str(sections.get(heading) or "").strip()
        if len(text) < MIN_SECTION_CHARS:
            problems.append(f"section '{heading}' is {len(text)} chars, needs {MIN_SECTION_CHARS}")
        if PLACEHOLDERS.search(text):
            problems.append(f"section '{heading}' contains a placeholder")
        if BANNED.search(text):
            problems.append(f"section '{heading}' uses a banned phrase: {BANNED.search(text).group(0)}")

    tags = draft.get("tags") or []
    if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        problems.append("tags must be a list of strings")
    if len(tags) > 8:
        problems.append(f"{len(tags)} tags; keep it to 8 or fewer")

    for item in draft.get("media") or []:
        name = str(item.get("file") or "")
        if name not in images:
            problems.append(f"media file '{name}' was not offered to the model")
        if not str(item.get("caption") or "").strip():
            problems.append(f"media '{name}' has no caption")
    if not draft.get("media") and not draft.get("diagram_svg"):
        problems.append("no media and no diagram")
    return problems


def write_entry(draft: dict, candidate: dict, images: dict[str, str]) -> Path:
    slug = str(draft["slug"]).strip()
    doc_path = PORTFOLIO_ROOT / "docs" / str(draft["pillar"]) / f"{slug}.md"
    if doc_path.exists():
        raise SystemExit(f"[auto-entry] {doc_path.name} already exists; pick a new slug")

    media = []
    media_dir = PORTFOLIO_ROOT / "assets" / "media" / slug
    for item in draft.get("media") or []:
        source = Path(images[str(item["file"])])
        media_dir.mkdir(parents=True, exist_ok=True)
        dest = media_dir / source.name
        if not dest.exists():
            shutil.copy2(source, dest)
        media.append({
            "src": dest.relative_to(PORTFOLIO_ROOT).as_posix(),
            "kind": "authentic",
            "caption": str(item["caption"]).strip(),
        })

    diagram = ""
    if not media and draft.get("diagram_svg"):
        diagram_dir = PORTFOLIO_ROOT / "assets" / "diagrams"
        diagram_dir.mkdir(parents=True, exist_ok=True)
        diagram_path = diagram_dir / f"{slug}.svg"
        diagram_path.write_text(sanitize_svg(str(draft["diagram_svg"])), encoding="utf-8")
        diagram = diagram_path.relative_to(PORTFOLIO_ROOT).as_posix()

    workspace = str(candidate.get("workspace") or "").strip()
    meta = {
        "id": slug,
        "title": str(draft["title"]).strip(),
        "subtitle": str(draft["subtitle"]).strip(),
        "pillar": draft["pillar"],
        "entry_type": draft["entry_type"],
        "readiness": draft["readiness"],
        "visibility": "main",
        "date_started": str(candidate.get("earliest") or "")[:10] or "2026-08-16",
        "date_updated": str(candidate.get("latest") or "")[:10] or "2026-11-25",
        "tags": [str(tag)[:40] for tag in (draft.get("tags") or [])][:8],
    }
    if media:
        meta["media"] = media
    if diagram:
        meta["diagram"] = diagram
    if workspace:
        path = workspace.replace("\\", "/")
        if re.match(r"^[A-Za-z]:", path):
            path = f"file:///{path}"
        meta["local_paths"] = [{"label": "Project root", "path": path}]

    body = "\n\n".join(
        f"## {heading}\n\n{str(draft['sections'][heading]).strip()}" for heading in REQUIRED_SECTIONS
    )
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(
        "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n\n" + body + "\n",
        encoding="utf-8",
    )
    log(f"wrote {doc_path.relative_to(PORTFOLIO_ROOT).as_posix()}")
    return doc_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one entry from an intake candidate.")
    parser.add_argument("--candidate", required=True, help="candidate JSON written by daily_publish.py")
    parser.add_argument("--draft", help="JSON draft to use instead of calling a model (testing)")
    args = parser.parse_args()

    candidate = json.loads(Path(args.candidate).read_text(encoding="utf-8"))
    image_paths = [str(path) for path in candidate.get("facts", {}).get("images", [])]
    images = {Path(path).name: path for path in image_paths}
    draft = json.loads(Path(args.draft).read_text(encoding="utf-8")) if args.draft else ask_llm(candidate)
    problems = validate(draft, images)
    if problems:
        print("[auto-entry] draft rejected:")
        for problem in problems:
            print(f"  [X] {problem}")
        return 1
    write_entry(draft, candidate, images)
    return 0


if __name__ == "__main__":
    sys.exit(main())
