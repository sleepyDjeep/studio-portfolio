#!/usr/bin/env python3
"""
Wave 5 Automated Completeness, Link, Privacy & Anti-Slop Verifier (verify_portfolio.py).
Exits non-zero if ANY gate fails:
  1. 100% Corpus Coverage (live LanceDB memories >= 2026-08-16 & SQLite top-level conversations >= 2026-08-16)
  2. Every Entry Complete (4 Plain-English & Technical sections, concrete example, >=1 visual)
  3. 100% Valid Asset Paths (every image, SVG, audio in portfolio-data.js exists and >0 bytes)
  4. Zero AI-Slop Lexicon (regex scan across docs/**/*.md, index.html, app.js, styles.css, README.md, DESIGN.md)
  5. Git & Vault Hygiene (docs/vault/ and assets/vault/ gitignored and zero tracked files inside them)

Only gate 1 needs data/master_manifest.json and the local LanceDB/SQLite stores. Gates 2-5 read
nothing but the committed tree, so `--skip-coverage` runs them anywhere, CI included.
"""

import argparse
import datetime
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # tools/ is not a package
from frontmatter import FrontmatterError, split_document  # noqa: E402

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PORTFOLIO_ROOT / "docs"
MANIFEST_PATH = PORTFOLIO_ROOT / "data" / "master_manifest.json"
BUNDLE_PATH = PORTFOLIO_ROOT / "portfolio-data.js"
BASELINE_PATH = PORTFOLIO_ROOT / "tools" / "expected_entries.json"
MEMORY_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\memory_db"
CONV_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\conversation_summaries.db"
INCEPTION_DATE = "2026-08-16"

REQUIRED_SECTIONS = [
    "What It Is & Why It Matters",
    "Real Example: How It Works in Practice",
    "Where It Stands & Next Steps",
    "Under the Hood & Local Files",
]

# Gate 2 schema. Each rule exists because the failure it catches is otherwise
# silent or is reported as a traceback: `tags: "3d, scan"` compiles to one tag per
# character, a string `media` crashes the gate while iterating it, a misspelled
# `date_updated` falls back to the builder default, and an unknown `readiness`
# renders an unstyled badge and drops the entry from the readiness view.
ALLOWED_FRONTMATTER_KEYS = {
    "id", "title", "subtitle", "pillar", "entry_type", "readiness", "visibility",
    "date_started", "date_updated", "tags", "metrics", "media", "diagram",
    "tech_stack", "local_paths", "run_commands", "memory_ids", "conversation_ids",
}
ENTRY_TYPES = {"project", "workflow", "idea"}
READINESS_VALUES = {"shipped", "active-build", "reusable-workflow", "blueprint"}
VISIBILITY_VALUES = {"main", "vault"}
MEDIA_KINDS = {"authentic", "concept", "audio"}
TEXT_LIST_KEYS = ("tags", "tech_stack", "memory_ids", "conversation_ids")
OBJECT_LIST_KEYS = ("metrics", "local_paths", "run_commands")

# Soft budget, not a failure: the nightly live check downloads the whole payload
# once every four days, and a handful of 12 MB PNGs is what makes that slow.
ASSET_WARN_BYTES = 2 * 1024 * 1024

# Constructed cleanly to enforce the exact Wave 5 anti-slop lexicon gate
BANNED_PATTERNS = [
    r"\bdelve(?:s|d|ing)?\b",
    r"\btapestr(?:y|ies)\b",
    r"\btestament\b",
    r"\bpivotal\b",
    r"\bbeacon\b",
    r"\bvibrant\b",
    r"\bfoster(?:s|ed|ing)?\b",
    r"\bseamless(?:ly)?\b",
    r"\brobust\b",
    r"\bholistic(?:ally)?\b",
    r"\btransformative\b",
    r"\bunravel(?:s|ed|ing)?\b",
    r"\bglean(?:s|ed|ing)?\b",
    r"\bparamount\b",
    r"\bgame[- ]changer\b",
    r"\bdouble[- ]edged sword\b",
    r"navigating the landscape",
    r"in today['\u2019]s fast[- ]paced world",
    r"\bat its core\b",
]


def is_vault_doc(md_path: Path, meta: dict) -> bool:
    """Vault entries are local-only, so they never belong in the public baseline."""
    if str(meta.get("visibility") or "").strip().lower() == "vault":
        return True
    return "vault" in md_path.relative_to(DOCS_DIR).parts


def entry_id(md_path: Path, meta: dict) -> str:
    return str(meta.get("id") or md_path.stem).strip()


def parse_date(value: str) -> datetime.date | None:
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def validate_frontmatter(meta: dict, label: str) -> list[str]:
    """Gate 2 schema: required keys, known keys, types, enums and dates."""
    problems: list[str] = []
    for key in ("id", "title", "subtitle", "pillar", "entry_type", "readiness", "visibility"):
        if not str(meta.get(key) or "").strip():
            problems.append(f"Gate 2: Missing frontmatter '{key}' in {label}")

    for key in sorted(set(meta) - ALLOWED_FRONTMATTER_KEYS):
        problems.append(
            f"Gate 2: Unknown frontmatter key '{key}' in {label} "
            f"(known: {', '.join(sorted(ALLOWED_FRONTMATTER_KEYS))})"
        )

    for key, allowed in (
        ("entry_type", ENTRY_TYPES),
        ("readiness", READINESS_VALUES),
        ("visibility", VISIBILITY_VALUES),
    ):
        value = str(meta.get(key) or "").strip()
        if value and value not in allowed:
            problems.append(
                f"Gate 2: {key} '{value}' in {label} is not one of {sorted(allowed)}"
            )

    for key in TEXT_LIST_KEYS:
        value = meta.get(key)
        if value is None:
            continue
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            problems.append(
                f"Gate 2: '{key}' in {label} must be a list of strings, "
                f"got {type(value).__name__}"
            )
    for key in OBJECT_LIST_KEYS:
        value = meta.get(key)
        if value is None:
            continue
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            problems.append(
                f"Gate 2: '{key}' in {label} must be a list of mappings, "
                f"got {type(value).__name__}"
            )

    media = meta.get("media")
    if media is not None and not isinstance(media, list):
        problems.append(
            f"Gate 2: 'media' in {label} must be a list of items, got {type(media).__name__}"
        )
    for item in media if isinstance(media, list) else []:
        if not isinstance(item, dict):
            problems.append(f"Gate 2: media items in {label} must be mappings")
            continue
        kind = str(item.get("kind") or "").strip()
        src = str(item.get("src") or "").strip()
        if kind not in MEDIA_KINDS:
            problems.append(f"Gate 2: Invalid media kind '{kind}' in {label}")
        if not src:
            problems.append(f"Gate 2: Media item missing 'src' in {label}")
        if kind in {"authentic", "concept"} and not str(item.get("caption") or "").strip():
            problems.append(
                f"Gate 2: Image '{src or '(no src)'}' in {label} has no caption "
                f"(the page uses it as alt text)"
            )
        if "assets/concepts/" in src and kind != "concept":
            problems.append(f"Gate 2: Concept illustration must have kind='concept' in {label}")

    if meta.get("diagram") is not None and not isinstance(meta.get("diagram"), str):
        problems.append(
            f"Gate 2: 'diagram' in {label} must be a path string, "
            f"got {type(meta.get('diagram')).__name__}"
        )

    for key in ("date_started", "date_updated"):
        value = str(meta.get(key) or "").strip()
        if value and not parse_date(value):
            problems.append(f"Gate 2: {key} '{value}' in {label} is not a YYYY-MM-DD date")
    started = str(meta.get("date_started") or "").strip()
    updated = str(meta.get("date_updated") or "").strip()
    if parse_date(started) and parse_date(updated) and started > updated:
        problems.append(
            f"Gate 2: date_updated {updated} precedes date_started {started} in {label}"
        )

    return problems


def section_headings(body: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)]


def entry_fingerprint(meta: dict, body: str) -> dict:
    """What an entry is made of, so the baseline can notice half of it vanishing."""
    media = meta.get("media") if isinstance(meta.get("media"), list) else []
    return {
        "media": [
            str(item.get("src") or "").strip()
            for item in media
            if isinstance(item, dict) and str(item.get("src") or "").strip()
        ],
        "diagram": str(meta.get("diagram") or "").strip(),
        "sections": section_headings(body),
    }


def tracked_files() -> set[str] | None:
    """Every path in the git index, or None outside a checkout."""
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=str(PORTFOLIO_ROOT), capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    return {path for path in result.stdout.split("\0") if path}


def case_mismatch(rel: str) -> str | None:
    """Name the component whose case differs on disk, if any.

    Windows resolves 'Assets/Media/Foo.PNG' to the lowercase file; Pages, served
    from a case-sensitive filesystem, returns 404 for it. CI runs on Linux and
    catches that after the push, so the local gates have to look for it too.
    """
    current = PORTFOLIO_ROOT
    for part in Path(rel).parts:
        try:
            names = os.listdir(current)
        except OSError:
            return None
        if part not in names:
            near = next((name for name in names if name.lower() == part.lower()), None)
            if near:
                return f"does not match the case on disk (found '{near}')"
            return f"has no component '{part}' on disk"
        current = current / part
    return None


def asset_problems(label: str, rel: str, owner: str, tracked: set[str] | None) -> list[str]:
    """Gate 3 rule: the file needs bytes on disk *and* a place in the git index.

    Existence alone is not shipping. An asset caught by an ignore rule sits on the
    author's disk, passes every local check, and 404s on Pages.
    """
    rel = rel.replace("\\", "/").strip()
    problems = []
    if not rel:
        return [f"Gate 3: Empty {label} path for {owner}"]
    if rel.startswith("/") or re.match(r"^[A-Za-z]:", rel):
        return [f"Gate 3: Absolute {label} path '{rel}' for {owner}; use a repository-relative path"]
    if ".." in Path(rel).parts:
        return [f"Gate 3: {label} path '{rel}' for {owner} escapes the repository"]
    path = PORTFOLIO_ROOT / rel
    if not path.exists() or path.stat().st_size == 0:
        problems.append(f"Gate 3: Missing/empty {label} '{rel}' for {owner}")
    else:
        mismatch = case_mismatch(rel)
        if mismatch:
            problems.append(f"Gate 3: {label} '{rel}' for {owner} {mismatch}")
    if tracked is not None and rel not in tracked:
        problems.append(
            f"Gate 3: {label} '{rel}' is not tracked in git for {owner} "
            f"(an ignore rule or a forgotten add ships a 404 to Pages)"
        )
    return problems


def public_entry_details() -> tuple[dict[str, dict], list[str]]:
    """Every id that ships publicly mapped to its fingerprint, plus unparseable docs."""
    details: dict[str, dict] = {}
    problems = []
    for md_path in sorted(DOCS_DIR.rglob("*.md")):
        try:
            meta, body = split_document(md_path.read_text(encoding="utf-8"), str(md_path))
        except FrontmatterError as exc:
            problems.append(str(exc))
            continue
        if is_vault_doc(md_path, meta):
            continue
        details[entry_id(md_path, meta)] = entry_fingerprint(meta, body)
    return details, problems


def gate_corpus_coverage(failures: list) -> None:
    """Gate 1: every live memory and top-level conversation maps to an entry.

    Reads data/master_manifest.json and the local LanceDB/SQLite stores, so it only
    runs where those exist; --skip-coverage omits it everywhere else.
    """
    if not MANIFEST_PATH.exists():
        failures.append("Gate 1 (Coverage): data/master_manifest.json missing")
        return

    import lancedb  # imported here so gates 2-5 run on machines without it

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    accounted_memories = set(manifest.get("excluded_memories", {}).keys())
    accounted_convs = set(manifest.get("excluded_conversations", {}).keys())
    for entry in manifest.get("entries", []):
        accounted_memories.update(entry.get("memory_ids", []))
        accounted_convs.update(entry.get("conversation_ids", []))

    db = lancedb.connect(MEMORY_DB_PATH)
    df_mem = db.open_table("memories").to_pandas()
    live_mem_ids = set(df_mem[df_mem["created_at"] >= INCEPTION_DATE]["id"].astype(str).tolist())
    missing_mems = sorted(live_mem_ids - accounted_memories)
    if missing_mems:
        failures.append(f"Gate 1 (Memories): {len(missing_mems)} unaccounted memory IDs: {missing_mems[:5]}")

    conn = sqlite3.connect(CONV_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT conversation_id FROM conversation_summaries
        WHERE last_modified_time >= ?
          AND (nesting_depth IS NULL OR nesting_depth = 0)
          AND (parent_conversation_id IS NULL OR parent_conversation_id = '')
        """,
        (INCEPTION_DATE,),
    )
    live_conv_ids = {r[0] for r in cur.fetchall()}
    conn.close()
    missing_convs = sorted(live_conv_ids - accounted_convs)
    if missing_convs:
        failures.append(f"Gate 1 (Conversations): {len(missing_convs)} unaccounted top-level conversation IDs: {missing_convs[:5]}")

    print(
        f"[Gate 1] Memories accounted: {len(live_mem_ids - set(missing_mems))}/{len(live_mem_ids)} | "
        f"Top-level Conversations accounted: {len(live_conv_ids - set(missing_convs))}/{len(live_conv_ids)}"
    )

def main() -> int:
    parser = argparse.ArgumentParser(description="Run the portfolio verification gates.")
    parser.add_argument(
        "--skip-coverage",
        action="store_true",
        help="skip gate 1, which needs data/master_manifest.json and the local LanceDB and conversation databases",
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="rewrite tools/expected_entries.json from the current docs/ and exit; review and commit it",
    )
    args = parser.parse_args()

    if args.update_baseline:
        details, problems = public_entry_details()
        if problems:
            print("[baseline] refusing to write: these docs do not parse")
            for problem in problems:
                print(f"  [X] {problem}")
            return 1
        if not details:
            print("[baseline] refusing to write an empty baseline")
            return 1
        previous = {}
        if BASELINE_PATH.exists():
            previous = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        added = sorted(set(details) - set(previous.get("entries", [])))
        removed = sorted(set(previous.get("entries", [])) - set(details))
        BASELINE_PATH.write_text(
            json.dumps(
                {
                    "note": "Every id that must ship, with the media, diagram and headings it shipped with. Refresh after an entry is added, renamed or retired: python tools/verify_portfolio.py --update-baseline",
                    "count": len(details),
                    "entries": sorted(details),
                    "fingerprints": {slug: details[slug] for slug in sorted(details)},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"[baseline] wrote {BASELINE_PATH.relative_to(PORTFOLIO_ROOT).as_posix()} "
              f"with {len(details)} entries; review and commit it.")
        for label, slugs in (("added", added), ("removed", removed)):
            if slugs:
                print(f"[baseline] {label}: {', '.join(slugs)}")
        return 0

    failures = []

    # --- GATE 1: 100% Corpus Coverage (local databases only) ---
    if args.skip_coverage:
        print("[Gate 1] Skipped (--skip-coverage): corpus coverage needs the local memory databases.")
    else:
        gate_corpus_coverage(failures)

    # --- GATE 2: Every Entry Complete ---
    md_files = sorted(DOCS_DIR.rglob("*.md"))
    if not md_files:
        failures.append("Gate 2: Zero Markdown entries found under docs/")

    public_ids: list[str] = []
    public_details: dict[str, dict] = {}
    for md_path in md_files:
        raw = md_path.read_text(encoding="utf-8")
        try:
            meta, body = split_document(raw, str(md_path))
        except FrontmatterError as exc:
            failures.append(f"Gate 2: Invalid YAML frontmatter in {md_path.name}: {exc}")
            continue

        failures.extend(validate_frontmatter(meta, md_path.name))

        if not is_vault_doc(md_path, meta):
            public_ids.append(entry_id(md_path, meta))
            public_details[entry_id(md_path, meta)] = entry_fingerprint(meta, body)

        media = meta.get("media") if isinstance(meta.get("media"), list) else []
        diagram = str(meta.get("diagram") or "").strip()
        if not media and not diagram:
            failures.append(f"Gate 2: Entry {md_path.name} has zero visuals (neither media nor diagram)")

        for sec in REQUIRED_SECTIONS:
            m_sec = re.search(rf"^##\s+{re.escape(sec)}\s*$", body, flags=re.MULTILINE)
            if not m_sec:
                failures.append(f"Gate 2: Missing section '## {sec}' in {md_path.name}")
            else:
                after = body[m_sec.end():]
                next_h2 = re.search(r"^##\s+", after, flags=re.MULTILINE)
                sec_body = (after[:next_h2.start()] if next_h2 else after).strip()
                if len(sec_body) < 80:
                    failures.append(f"Gate 2: Section '## {sec}' too thin ({len(sec_body)} chars) in {md_path.name}")

    print(f"[Gate 2] Audited {len(md_files)} Markdown entries for structural & visual completeness.")

    # --- GATE 2 (BASELINE): no entry may vanish ---
    # Completeness of the docs that exist says nothing about the docs that used to.
    # tools/expected_entries.json is the committed record of what must be there.
    if not BASELINE_PATH.exists():
        failures.append("Gate 2 (Baseline): tools/expected_entries.json is missing")
    else:
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        expected = {str(slug) for slug in baseline.get("entries", [])}
        present = set(public_ids)
        for slug in sorted(expected - present):
            failures.append(
                f"Gate 2 (Baseline): entry '{slug}' is listed in tools/expected_entries.json "
                f"but no doc provides it (deleted, renamed, or unparseable)"
            )
        for slug in sorted(present - expected):
            failures.append(
                f"Gate 2 (Baseline): entry '{slug}' exists under docs/ but not in the baseline; "
                f"review it, then run: python tools/verify_portfolio.py --update-baseline"
            )
        recorded = baseline.get("fingerprints") or {}
        for slug in sorted(set(recorded) & set(public_details)):
            was, now = recorded[slug], public_details[slug]
            for src in was.get("media", []):
                if src not in now.get("media", []):
                    failures.append(
                        f"Gate 2 (Baseline): entry '{slug}' no longer references media '{src}' "
                        f"(restore it, or re-run --update-baseline if the removal is intended)"
                    )
            diagram = str(was.get("diagram") or "")
            if diagram and now.get("diagram") != diagram:
                failures.append(
                    f"Gate 2 (Baseline): entry '{slug}' no longer uses diagram '{diagram}' "
                    f"(restore it, or re-run --update-baseline if the removal is intended)"
                )
            for heading in was.get("sections", []):
                if heading not in now.get("sections", []):
                    failures.append(
                        f"Gate 2 (Baseline): entry '{slug}' lost section '## {heading}' "
                        f"(restore it, or re-run --update-baseline if the rename is intended)"
                    )

        listed = f"{len(expected)} expected, {len(present)} present"
        print(f"[Gate 2] Baseline: {listed}.")

    # --- GATE 3: 100% Valid Asset Paths in portfolio-data.js ---
    if not BUNDLE_PATH.exists():
        failures.append("Gate 3: portfolio-data.js does not exist")
    else:
        raw_js = BUNDLE_PATH.read_text(encoding="utf-8")
        prefix = "window.PORTFOLIO_DATA = "
        idx = raw_js.find(prefix)
        if idx == -1:
            failures.append("Gate 3: window.PORTFOLIO_DATA assignment missing in portfolio-data.js")
        else:
            json_str = raw_js[idx + len(prefix):].rstrip().rstrip(";")
            bundle = json.loads(json_str)
            tracked = tracked_files()
            if tracked is None:
                failures.append(
                    "Gate 3: not a git checkout, so whether these assets actually ship cannot be verified"
                )

            checked_assets = 0
            asset_sizes: list[tuple[str, int]] = []
            for e in bundle.get("entries", []):
                if e.get("diagram"):
                    checked_assets += 1
                    failures.extend(asset_problems("diagram", str(e["diagram"]), e["id"], tracked))
                for m in e.get("media", []):
                    checked_assets += 1
                    failures.extend(
                        asset_problems("media", str(m.get("src") or ""), e["id"], tracked)
                    )
            print(
                f"[Gate 3] Verified {checked_assets} asset paths in portfolio-data.js "
                f"(>0 bytes on disk, tracked in git)."
            )
            if tracked is not None:
                for e in bundle.get("entries", []):
                    rels = [e["diagram"]] if e.get("diagram") else []
                    rels += [m.get("src") for m in e.get("media", [])]
                    for rel in rels:
                        path = PORTFOLIO_ROOT / str(rel or "")
                        if path.is_file():
                            asset_sizes.append((str(rel), path.stat().st_size))
                total_mb = sum(size for _, size in asset_sizes) / 1048576
                heavy = sorted(
                    ((rel, size) for rel, size in asset_sizes if size > ASSET_WARN_BYTES),
                    key=lambda item: -item[1],
                )
                print(f"[Gate 3] Payload media: {total_mb:.1f} MB across {len(asset_sizes)} files.")
                if heavy:
                    print(
                        f"[Gate 3] Warning: {len(heavy)} asset(s) over "
                        f"{ASSET_WARN_BYTES / 1048576:.0f} MB (prefer WebP for new images):"
                    )
                    for rel, size in heavy[:5]:
                        print(f"    {size / 1048576:.1f} MB  {rel}")

    # --- GATE 4: Zero AI-Slop Lexicon ---
    scan_targets = list(DOCS_DIR.rglob("*.md")) + [
        PORTFOLIO_ROOT / "index.html",
        PORTFOLIO_ROOT / "app.js",
        PORTFOLIO_ROOT / "styles.css",
        PORTFOLIO_ROOT / "DESIGN.md",
        PORTFOLIO_ROOT / "README.md",
    ]
    combined_regex = re.compile("|".join(f"(?:{p})" for p in BANNED_PATTERNS), flags=re.IGNORECASE)
    slop_hits = []
    for target in scan_targets:
        if not target.exists():
            continue
        txt = target.read_text(encoding="utf-8")
        for line_no, line in enumerate(txt.splitlines(), start=1):
            for match in combined_regex.finditer(line):
                slop_hits.append(f"{target.relative_to(PORTFOLIO_ROOT)}:{line_no} -> '{match.group(0)}'")

    if slop_hits:
        failures.append(f"Gate 4 (Anti-Slop): {len(slop_hits)} banned word hits:\n    " + "\n    ".join(slop_hits[:15]))
    print(f"[Gate 4] Scanned {len([t for t in scan_targets if t.exists()])} files for banned AI-slop lexicon: {len(slop_hits)} hits.")

    # --- GATE 5: Git & Vault Hygiene ---
    # The trailing slashes matter: with the directory absent, `git check-ignore data`
    # cannot tell it is a directory and misses the `data/` rule. CI sees exactly that
    # state, since data/ is gitignored and never checked out.
    for vault_rel in ["docs/vault/", "assets/vault/", "portfolio-vault.js", "data/"]:
        chk = subprocess.run(
            ["git", "check-ignore", "-v", vault_rel],
            cwd=str(PORTFOLIO_ROOT),
            capture_output=True,
            text=True,
        )
        if chk.returncode != 0:
            failures.append(f"Gate 5 (Git Hygiene): '{vault_rel}' is NOT gitignored!")

        ls_tracked = subprocess.run(
            ["git", "ls-files", vault_rel],
            cwd=str(PORTFOLIO_ROOT),
            capture_output=True,
            text=True,
        )
        if ls_tracked.stdout.strip():
            failures.append(f"Gate 5 (Vault Leak): Tracked files found inside {vault_rel}: {ls_tracked.stdout.strip()}")

    # Verify zero Vault entries or slugs exist inside public portfolio-data.js
    if BUNDLE_PATH.exists():
        pub_txt = BUNDLE_PATH.read_text(encoding="utf-8")
        vault_dir = DOCS_DIR / "vault"
        vault_stems = [p.stem for p in vault_dir.glob("*.md")] if vault_dir.exists() else []
        for v_stem in vault_stems:
            if v_stem.lower() in pub_txt.lower():
                failures.append(f"Gate 5 (Public Bundle Leak): Vault slug '{v_stem}' found in portfolio-data.js!")
        if '"visibility": "vault"' in pub_txt:
            failures.append("Gate 5 (Public Bundle Leak): visibility='vault' entry found in portfolio-data.js!")

    print("[Gate 5] Verified Git ignore rules and zero Vault leaks in git ls-files or portfolio-data.js.")

    if failures:
        print("\n=== VERIFICATION FAILED ===")
        for f in failures:
            print(f"  [X] {f}")
        return 1

    print("\n=== ALL 5 PORTFOLIO VERIFICATION GATES PASSED (0 ERRORS) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
