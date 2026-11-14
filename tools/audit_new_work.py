#!/usr/bin/env python3
"""
Incremental Living Portfolio Sync Detector (audit_new_work.py).
Scans live LanceDB (memories.lance), SQLite (conversation_summaries.db), and D:\\Projects\\
against data/master_manifest.json and reports any newly created memories, conversations,
or project folders not yet documented in Studio Portfolio.
"""

import json
import sqlite3
from pathlib import Path
import lancedb

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PORTFOLIO_ROOT / "data" / "master_manifest.json"
MEMORY_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\memory_db"
CONV_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\conversation_summaries.db"
PROJECTS_ROOT = Path(r"D:\Projects")
INCEPTION_DATE = "2026-08-16"


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"Manifest missing: {MANIFEST_PATH}")
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    known_memories = set(manifest.get("excluded_memories", {}).keys())
    known_convs = set(manifest.get("excluded_conversations", {}).keys())
    known_local_paths = set()

    for entry in manifest.get("entries", []):
        known_memories.update(entry.get("memory_ids", []))
        known_convs.update(entry.get("conversation_ids", []))
        for lp in entry.get("local_paths", []):
            p_str = lp.get("path", "") if isinstance(lp, dict) else str(lp)
            p_clean = p_str.replace("file:///", "").replace("\\", "/").rstrip("/").lower()
            if p_clean:
                known_local_paths.add(p_clean)

    # 1. Check LanceDB memories
    db = lancedb.connect(MEMORY_DB_PATH)
    df = db.open_table("memories").to_pandas()
    df = df[df["created_at"] >= INCEPTION_DATE].sort_values("created_at")
    new_memories = []
    for _, row in df.iterrows():
        mid = str(row["id"])
        if mid not in known_memories:
            new_memories.append({
                "id": mid,
                "created_at": str(row["created_at"])[:19],
                "category": str(row.get("category") or ""),
                "text": " ".join(str(row.get("text") or "").split())[:120],
            })

    # 2. Check SQLite top-level conversations
    conn = sqlite3.connect(CONV_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT conversation_id, title, preview, step_count, last_modified_time
        FROM conversation_summaries
        WHERE last_modified_time >= ?
          AND (nesting_depth IS NULL OR nesting_depth = 0)
          AND (parent_conversation_id IS NULL OR parent_conversation_id = '')
        ORDER BY last_modified_time ASC
        """,
        (INCEPTION_DATE,),
    )
    new_convs = []
    for r in cur.fetchall():
        cid = r["conversation_id"]
        if cid not in known_convs:
            new_convs.append({
                "id": cid,
                "modified": str(r["last_modified_time"])[:19],
                "steps": r["step_count"],
                "title": (r["title"] or r["preview"] or "(untitled)")[:80],
            })
    conn.close()

    # 3. Check D:\Projects folders
    ignore_names = {"Studio_Portfolio", "CLAUDE.md", "Video Project.mp4", "_Shared_Library",
                    "godot_deprecations_4.0_to_4.7.json", "godot_deprecations_4.0_to_4.7.yaml"}
    new_folders = []
    if PROJECTS_ROOT.exists():
        for item in sorted(PROJECTS_ROOT.iterdir()):
            if item.name in ignore_names or not item.is_dir():
                continue
            norm = str(item).replace("\\", "/").rstrip("/").lower()
            if not any(norm in kp or kp in norm for kp in known_local_paths):
                new_folders.append(str(item))

    print("=== STUDIO PORTFOLIO INCREMENTAL SYNC REPORT ===")
    print(f"Known Memories:      {len(known_memories):,}")
    print(f"Known Conversations: {len(known_convs):,}")
    print(f"New Unmapped Memories:      {len(new_memories)}")
    for m in new_memories[:20]:
        print(f"  + [{m['created_at']}] ({m['category']}) {m['id']} :: {m['text']}")
    print(f"New Unmapped Conversations: {len(new_convs)}")
    for c in new_convs[:20]:
        print(f"  + [{c['modified']}] steps={c['steps']} {c['id']} :: {c['title']}")
    print(f"Unmapped D:\\Projects Dirs:  {len(new_folders)}")
    for f in new_folders:
        print(f"  + {f}")

    if not new_memories and not new_convs and not new_folders:
        print("\nSTATUS: UP TO DATE (0 unmapped records).")
    else:
        print("\nSTATUS: NEW WORK DETECTED — add entries to docs/ and run tools/build_portfolio.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
