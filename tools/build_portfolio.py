#!/usr/bin/env python3
"""
Studio Portfolio Zero-Fragility Compiler (<1s runtime).
Parses docs/**/*.md + data/master_manifest.json, validates referenced assets,
renders clean semantic HTML per section, and writes portfolio-data.js so
index.html runs directly via file:// with zero server and zero CORS errors.
"""

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PORTFOLIO_ROOT / "docs"
MANIFEST_PATH = PORTFOLIO_ROOT / "data" / "master_manifest.json"
OUTPUT_JS_PATH = PORTFOLIO_ROOT / "portfolio-data.js"
OUTPUT_VAULT_JS_PATH = PORTFOLIO_ROOT / "portfolio-vault.js"

REQUIRED_SECTIONS = [
    "What It Is & Why It Matters",
    "Real Example: How It Works in Practice",
    "Where It Stands & Next Steps",
    "Under the Hood & Local Files",
]


def render_inline_md(text: str) -> str:
    """Convert inline Markdown (code spans, links, bold, italic) safely to HTML."""
    tokens = []

    def stash(fragment: str) -> str:
        key = f"\x00TOK{len(tokens)}\x00"
        tokens.append(fragment)
        return key

    # 1. Inline code `...`
    def repl_code(m: re.Match) -> str:
        return stash(f"<code>{html.escape(m.group(1))}</code>")

    text = re.sub(r"`([^`]+)`", repl_code, text)

    # 2. Links [label](url)
    def repl_link(m: re.Match) -> str:
        label = html.escape(m.group(1))
        url = html.escape(m.group(2), quote=True)
        return stash(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, text)

    # Escape remaining HTML characters
    text = html.escape(text)

    # 3. Bold **...**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # 4. Italic *...*
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    # Restore stashed HTML tokens
    for idx, frag in enumerate(tokens):
        text = text.replace(f"\x00TOK{idx}\x00", frag)

    return text


def render_markdown_to_html(md_text: str) -> str:
    """Zero-dependency Markdown block parser producing clean semantic HTML."""
    lines = md_text.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            escaped_code = html.escape("\n".join(code_lines))
            lang_attr = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{lang_attr}>{escaped_code}</code></pre>")
            continue

        # Horizontal rule
        if stripped in {"---", "***", "___"}:
            out.append("<hr>")
            i += 1
            continue

        # Headings H3 / H4 inside sections
        m_head = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if m_head:
            level = min(max(len(m_head.group(1)), 2), 5)
            out.append(f"<h{level}>{render_inline_md(m_head.group(2).strip())}</h{level}>")
            i += 1
            continue

        # GFM Table
        if "|" in stripped and i + 1 < n and re.match(r"^\|?[\s:-]+\|[\s|:-]*$", lines[i + 1].strip()):
            header_cells = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # skip header + separator
            body_rows = []
            while i < n and "|" in lines[i].strip() and lines[i].strip():
                row_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                body_rows.append(row_cells)
                i += 1
            thead = "".join(f"<th>{render_inline_md(c)}</th>" for c in header_cells)
            tbody_parts = []
            for r in body_rows:
                tds = "".join(f"<td>{render_inline_md(c)}</td>" for c in r)
                tbody_parts.append(f"<tr>{tds}</tr>")
            out.append(
                f'<div class="table-wrap"><table><thead><tr>{thead}</tr></thead>'
                f'<tbody>{"".join(tbody_parts)}</tbody></table></div>'
            )
            continue

        # Blockquote
        if stripped.startswith(">"):
            bq_lines = []
            while i < n and lines[i].strip().startswith(">"):
                bq_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append(f"<blockquote><p>{render_inline_md(' '.join(bq_lines))}</p></blockquote>")
            continue

        # Unordered list
        if re.match(r"^[-*+]\s+", stripped):
            items = []
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i]):
                item_txt = re.sub(r"^\s*[-*+]\s+", "", lines[i]).strip()
                i += 1
                while i < n and lines[i].startswith("  ") and not re.match(r"^\s*[-*+\d]+[.)]?\s+", lines[i]):
                    item_txt += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{render_inline_md(item_txt)}</li>")
            out.append(f"<ul>{''.join(items)}</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                item_txt = re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip()
                i += 1
                while i < n and lines[i].startswith("  ") and not re.match(r"^\s*[-*+\d]+[.)]?\s+", lines[i]):
                    item_txt += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{render_inline_md(item_txt)}</li>")
            out.append(f"<ol>{''.join(items)}</ol>")
            continue

        # Paragraph
        para_lines = [stripped]
        i += 1
        while (
            i < n
            and lines[i].strip()
            and not lines[i].strip().startswith(("```", "#", ">", "- ", "* ", "+ "))
            and not re.match(r"^\d+\.\s+", lines[i].strip())
            and not (
                "|" in lines[i]
                and i + 1 < n
                and re.match(r"^\|?[\s:-]+\|[\s|:-]*$", lines[i + 1].strip())
            )
        ):
            para_lines.append(lines[i].strip())
            i += 1
        out.append(f"<p>{render_inline_md(' '.join(para_lines))}</p>")

    return "\n".join(out)


def parse_markdown_entry(md_path: Path) -> dict:
    raw = md_path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"{md_path}: Missing YAML frontmatter opening '---'")

    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{md_path}: Unclosed YAML frontmatter")

    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()

    # Split body by ## headings
    section_map = {}
    current_heading = None
    buf = []

    for line in body.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current_heading is not None:
                section_map[current_heading] = "\n".join(buf).strip()
            current_heading = m.group(1).strip()
            buf = []
        else:
            buf.append(line)

    if current_heading is not None:
        section_map[current_heading] = "\n".join(buf).strip()

    sections_rendered = {}
    sections_raw = {}
    for sec in REQUIRED_SECTIONS:
        raw_sec = section_map.get(sec, "")
        sections_raw[sec] = raw_sec
        sections_rendered[sec] = render_markdown_to_html(raw_sec)

    # Also extract structured Input / What Happens / Output steps if present in Real Example
    example_raw = sections_raw.get("Real Example: How It Works in Practice", "")
    example_steps = extract_ipo_steps(example_raw)

    return {
        "meta": meta,
        "doc_path": str(md_path.relative_to(PORTFOLIO_ROOT)).replace("\\", "/"),
        "sections_raw": sections_raw,
        "sections_html": sections_rendered,
        "example_ipo": example_steps,
    }


def extract_ipo_steps(example_md: str) -> dict:
    """Extract structured Input -> What Happens -> Output blocks when labeled."""
    patterns = {
        "input": r"(?:^|\n)\s*(?:[-*]\s*)?\*\*Input(?:\s*\([^)]*\))?\*\*\s*:\s*(.+?)(?=(?:\n\s*(?:[-*]\s*)?\*\*(?:What Happens|Process|Output))|\Z)",
        "process": r"(?:^|\n)\s*(?:[-*]\s*)?\*\*(?:What Happens|Process)(?:\s*\([^)]*\))?\*\*\s*:\s*(.+?)(?=(?:\n\s*(?:[-*]\s*)?\*\*Output)|\Z)",
        "output": r"(?:^|\n)\s*(?:[-*]\s*)?\*\*Output(?:\s*\([^)]*\))?\*\*\s*:\s*(.+?)(?=\n\n###|\Z)",
    }
    res = {}
    for key, pat in patterns.items():
        m = re.search(pat, example_md, flags=re.DOTALL | re.IGNORECASE)
        if m:
            res[key] = render_markdown_to_html(m.group(1).strip())
    return res


def compile_portfolio() -> int:
    if not MANIFEST_PATH.exists():
        print(f"[ERROR] Manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_by_id = {e["id"]: e for e in manifest.get("entries", [])}

    md_files = sorted(DOCS_DIR.rglob("*.md"))
    compiled_entries = []
    errors = []

    for md_path in md_files:
        try:
            parsed = parse_markdown_entry(md_path)
        except Exception as exc:
            errors.append(str(exc))
            continue

        meta = parsed["meta"]
        slug = str(meta.get("id") or md_path.stem)
        m_entry = manifest_by_id.get(slug, {})

        # Merge authoritative memory_ids & conversation_ids from master_manifest if present
        memory_ids = m_entry.get("memory_ids") or meta.get("memory_ids") or []
        conversation_ids = m_entry.get("conversation_ids") or meta.get("conversation_ids") or []

        media_list = meta.get("media") or []
        diagram_rel = str(meta.get("diagram") or "").strip()

        # Inline SVG markup if diagram exists so it adapts cleanly via CSS on file://
        diagram_svg = ""
        if diagram_rel:
            diag_path = PORTFOLIO_ROOT / diagram_rel
            if not diag_path.exists() or diag_path.stat().st_size == 0:
                errors.append(f"{slug}: Missing or empty diagram '{diagram_rel}'")
            elif diag_path.suffix.lower() == ".svg":
                diagram_svg = diag_path.read_text(encoding="utf-8")

        for m_item in media_list:
            src = str(m_item.get("src") or "").strip()
            if not src:
                errors.append(f"{slug}: Media item missing 'src'")
                continue
            asset_path = PORTFOLIO_ROOT / src
            if not asset_path.exists() or asset_path.stat().st_size == 0:
                errors.append(f"{slug}: Missing or empty media asset '{src}'")

        compiled_entries.append({
            "id": slug,
            "doc_path": parsed["doc_path"],
            "title": str(meta.get("title") or slug),
            "subtitle": str(meta.get("subtitle") or ""),
            "pillar": str(meta.get("pillar") or md_path.parent.name),
            "entry_type": str(meta.get("entry_type") or "project"),
            "readiness": str(meta.get("readiness") or "shipped"),
            "visibility": str(meta.get("visibility") or ("vault" if "vault" in parsed["doc_path"] else "main")),
            "date_started": str(meta.get("date_started") or "2026-08-16"),
            "date_updated": str(meta.get("date_updated") or "2026-11-12"),
            "tags": list(meta.get("tags") or []),
            "metrics": list(meta.get("metrics") or []),
            "media": media_list,
            "diagram": diagram_rel,
            "diagram_svg": diagram_svg,
            "tech_stack": list(meta.get("tech_stack") or []),
            "local_paths": list(meta.get("local_paths") or []),
            "run_commands": list(meta.get("run_commands") or []),
            "memory_count": len(memory_ids),
            "conversation_count": len(conversation_ids),
            "memory_ids": memory_ids,
            "conversation_ids": conversation_ids,
            "example_ipo": parsed["example_ipo"],
            "sections_html": parsed["sections_html"],
            "search_text": " ".join([
                str(meta.get("title") or ""),
                str(meta.get("subtitle") or ""),
                " ".join(str(t) for t in (meta.get("tags") or [])),
                " ".join(str(t) for t in (meta.get("tech_stack") or [])),
                parsed["sections_raw"].get("What It Is & Why It Matters", ""),
                parsed["sections_raw"].get("Real Example: How It Works in Practice", ""),
                parsed["sections_raw"].get("Where It Stands & Next Steps", ""),
            ]),
        })

    if errors:
        print("[BUILD ERRORS]", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    # Deterministic ordering: pillar order, then shipped/active/workflow/blueprint, then date_updated desc
    pillar_order = {p["id"]: idx for idx, p in enumerate(manifest.get("pillars", []))}
    readiness_order = {"shipped": 0, "reusable-workflow": 1, "active-build": 2, "blueprint": 3}
    compiled_entries.sort(
        key=lambda e: (
            pillar_order.get(e["pillar"], 99),
            readiness_order.get(e["readiness"], 9),
            e["title"].lower(),
        )
    )

    main_entries = [e for e in compiled_entries if e["visibility"] == "main"]
    vault_entries = [e for e in compiled_entries if e["visibility"] == "vault"]
    main_pillars = [p for p in manifest.get("pillars", []) if p.get("id") != "vault"]
    vault_pillars = [p for p in manifest.get("pillars", []) if p.get("id") == "vault"]

    bundle = {
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "inception_date": manifest.get("inception_date", "2026-08-16"),
        "summary": {
            "total_entries": len(main_entries),
            "main_entries": len(main_entries),
            "vault_entries": 0,
            "memories_indexed": manifest.get("reconciliation", {}).get("wave0_memory_count", 0),
            "conversations_indexed": manifest.get("reconciliation", {}).get("wave0_top_conversation_count", 0),
            "shipped_count": sum(1 for e in main_entries if e["readiness"] == "shipped"),
            "workflow_count": sum(1 for e in main_entries if e["entry_type"] == "workflow" or e["readiness"] == "reusable-workflow"),
            "active_count": sum(1 for e in main_entries if e["readiness"] == "active-build"),
            "blueprint_count": sum(1 for e in main_entries if e["readiness"] == "blueprint"),
        },
        "pillars": main_pillars,
        "entries": main_entries,
    }

    js_payload = (
        "// Auto-generated by tools/build_portfolio.py — public web-safe bundle (0 Vault entries).\n"
        "window.PORTFOLIO_DATA = "
        + json.dumps(bundle, indent=2, ensure_ascii=False)
        + ";\n"
    )
    OUTPUT_JS_PATH.write_text(js_payload, encoding="utf-8")

    if vault_entries:
        vault_payload = (
            "// Local-only gitignored Vault bundle — never committed or deployed.\n"
            "window.PORTFOLIO_VAULT_DATA = "
            + json.dumps({"pillars": vault_pillars, "entries": vault_entries}, indent=2, ensure_ascii=False)
            + ";\n"
        )
        OUTPUT_VAULT_JS_PATH.write_text(vault_payload, encoding="utf-8")
    elif OUTPUT_VAULT_JS_PATH.exists():
        OUTPUT_VAULT_JS_PATH.unlink()

    print(
        f"[build_portfolio] Compiled {len(main_entries)} public entries -> {OUTPUT_JS_PATH.name} "
        f"(+{len(vault_entries)} local-only entries -> gitignored {OUTPUT_VAULT_JS_PATH.name})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(compile_portfolio())
