#!/usr/bin/env python3
"""
Wave 0 Deterministic Raw Ledger Extractor for Studio Portfolio.
Exports 100% of records since Unified Memory Bank inception (2026-08-16):
  1. data/raw/memories_dump.json
  2. data/raw/conversations_dump.json
  3. data/raw/filesystem_dump.json
"""

import json
import os
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import lancedb

PORTFOLIO_ROOT = Path(r"D:\Projects\Studio_Portfolio")
RAW_DIR = PORTFOLIO_ROOT / "data" / "raw"
MEMORY_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\memory_db"
CONV_DB_PATH = r"C:\Users\ogreb\.gemini\antigravity\conversation_summaries.db"
BRAIN_ROOT = Path(r"C:\Users\ogreb\.gemini\antigravity\brain")
INCEPTION_DATE = "2026-08-16"

SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".godot",
    ".import",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".next",
    "site-packages",
    "Lib",
    "Scripts",
    "Include",
    "$RECYCLE.BIN",
    "System Volume Information",
    "WindowsApps",
    "WpSystem",
    "WUDownloadCache",
    "Config.Msi",
}

BUILD_EXTS = {".exe", ".apk", ".pck", ".msi", ".zip", ".html", ".mp4", ".webm", ".wav", ".mp3", ".ogg", ".flac"}
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}
DOC_EXTS = {".md", ".txt", ".pdf", ".docx", ".json", ".yaml", ".yml", ".toml"}
CODE_EXTS = {".py", ".gd", ".cs", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".ps1", ".bat", ".sh", ".shader", ".gdshader"}


def safe_read_text(path: Path, max_chars: int = 2500) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return text[:max_chars]
    except Exception:
        return ""


def extract_memories() -> dict:
    db = lancedb.connect(MEMORY_DB_PATH)
    tbl = db.open_table("memories")
    df = tbl.to_pandas()
    df = df[df["created_at"] >= INCEPTION_DATE].sort_values("created_at")

    records = []
    by_workspace = Counter()
    by_category = Counter()
    by_month = Counter()

    for _, row in df.iterrows():
        ws = str(row.get("workspace_path") or "")
        cat = str(row.get("category") or "")
        created = str(row.get("created_at") or "")
        by_workspace[ws or "(empty)"] += 1
        by_category[cat or "(empty)"] += 1
        if len(created) >= 7:
            by_month[created[:7]] += 1

        records.append({
            "id": str(row["id"]),
            "created_at": created,
            "updated_at": str(row.get("updated_at") or ""),
            "category": cat,
            "scope": str(row.get("scope") or ""),
            "workspace_path": ws,
            "metadata_json": str(row.get("metadata_json") or "{}"),
            "text": str(row.get("text") or ""),
        })

    out = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "inception_filter": INCEPTION_DATE,
        "total_memories": len(records),
        "by_category": dict(by_category.most_common()),
        "by_month": dict(sorted(by_month.items())),
        "by_workspace": dict(by_workspace.most_common()),
        "memories": records,
    }
    out_path = RAW_DIR / "memories_dump.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Wave 0] Exported {len(records)} memories -> {out_path}")
    return out


def scan_brain_dir(cid: str) -> dict:
    bdir = BRAIN_ROOT / cid
    if not bdir.exists() or not bdir.is_dir():
        return {"exists": False, "artifacts": [], "media": [], "scratch_files": [], "has_transcript": False}

    artifacts = []
    media = []
    scratch_files = []
    has_transcript = (bdir / ".system_generated" / "logs" / "transcript.jsonl").exists()

    for root, dirs, files in os.walk(bdir):
        dirs[:] = [d for d in dirs if d != ".system_generated"]
        rel_root = Path(root).relative_to(bdir)
        is_scratch = rel_root.parts and rel_root.parts[0] in {"scratch", "browser_sandbox"}

        for f in sorted(files):
            if f.endswith(".metadata.json") or f.endswith(".resolved") or ".resolved." in f:
                continue
            fpath = Path(root) / f
            rel_str = str(fpath.relative_to(bdir)).replace("\\", "/")
            ext = fpath.suffix.lower()
            try:
                sz = fpath.stat().st_size
            except OSError:
                sz = 0

            if is_scratch:
                scratch_files.append({"rel_path": rel_str, "ext": ext, "size": sz})
                continue

            item = {"rel_path": rel_str, "abs_path": str(fpath).replace("\\", "/"), "ext": ext, "size": sz}
            if ext in MEDIA_EXTS or ext in {".mp4", ".webm", ".wav", ".mp3", ".html", ".pdf"}:
                media.append(item)
            if ext in {".md", ".txt", ".json", ".html"}:
                if ext == ".md":
                    snippet = safe_read_text(fpath, 600)
                    first_lines = [ln.strip() for ln in snippet.splitlines() if ln.strip()][:5]
                    item["heading_preview"] = " | ".join(first_lines)[:300]
                artifacts.append(item)

    return {
        "exists": True,
        "has_transcript": has_transcript,
        "artifacts": artifacts,
        "media": media,
        "scratch_files": scratch_files[:30],
    }


def extract_conversations() -> dict:
    conn = sqlite3.connect(CONV_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT conversation_id, title, preview, step_count, last_modified_time,
               workspace_uris, status, source, project_id, agent_name,
               parent_conversation_id, nesting_depth, killed, last_user_input_time, group_id
        FROM conversation_summaries
        WHERE last_modified_time >= ?
        ORDER BY last_modified_time ASC
        """,
        (INCEPTION_DATE,),
    )
    rows = [dict(r) for r in cur.fetchall()]

    # Fetch FTS snippets per conversation_id (first and last chunk for rich context)
    fts_map = defaultdict(list)
    cur.execute(
        """
        SELECT conversation_id, chunk_index, title, workspace, user_body, agent_body
        FROM conversations_fts
        WHERE last_modified_time >= ?
        ORDER BY chunk_index ASC
        """,
        (INCEPTION_DATE,),
    )
    for r in cur.fetchall():
        cid = r["conversation_id"]
        if len(fts_map[cid]) < 3:
            fts_map[cid].append({
                "chunk_index": r["chunk_index"],
                "title": (r["title"] or "")[:200],
                "workspace": (r["workspace"] or "")[:200],
                "user_snippet": (r["user_body"] or "")[:500],
                "agent_snippet": (r["agent_body"] or "")[:500],
            })

    conn.close()

    children_by_parent = defaultdict(list)
    for r in rows:
        pid = r.get("parent_conversation_id") or ""
        if pid:
            children_by_parent[pid].append({
                "conversation_id": r["conversation_id"],
                "agent_name": r.get("agent_name") or "",
                "preview": r.get("preview") or r.get("title") or "",
                "step_count": r.get("step_count") or 0,
                "nesting_depth": r.get("nesting_depth") or 0,
            })

    top_level = []
    nested = []

    for r in rows:
        cid = r["conversation_id"]
        depth = r.get("nesting_depth")
        is_top = (depth is None or int(depth) == 0) and not (r.get("parent_conversation_id") or "")

        try:
            ws_uris = json.loads(r.get("workspace_uris") or "[]")
        except Exception:
            ws_uris = [r.get("workspace_uris")] if r.get("workspace_uris") else []

        brain_info = scan_brain_dir(cid)
        entry = {
            "conversation_id": cid,
            "title": r.get("title") or "",
            "preview": r.get("preview") or "",
            "step_count": r.get("step_count") or 0,
            "last_modified_time": r.get("last_modified_time") or "",
            "last_user_input_time": r.get("last_user_input_time") or "",
            "workspace_uris": ws_uris,
            "status": r.get("status") or "",
            "agent_name": r.get("agent_name") or "",
            "parent_conversation_id": r.get("parent_conversation_id") or "",
            "nesting_depth": depth if depth is not None else 0,
            "child_runs": children_by_parent.get(cid, []),
            "fts_chunks": fts_map.get(cid, []),
            "brain": brain_info,
        }
        if is_top:
            top_level.append(entry)
        else:
            nested.append(entry)

    out = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "inception_filter": INCEPTION_DATE,
        "total_conversations_since_inception": len(rows),
        "top_level_count": len(top_level),
        "nested_subagent_count": len(nested),
        "top_level_conversations": top_level,
        "nested_subagent_runs": nested,
    }
    out_path = RAW_DIR / "conversations_dump.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        f"[Wave 0] Exported {len(top_level)} top-level conversations "
        f"(+{len(nested)} nested runs) -> {out_path}"
    )
    return out


def summarize_project_dir(path: Path, max_depth: int = 5, max_media: int = 60) -> dict:
    if not path.exists():
        return {"path": str(path), "exists": False}

    if path.is_file():
        ext = path.suffix.lower()
        return {
            "path": str(path).replace("\\", "/"),
            "exists": True,
            "is_file": True,
            "size": path.stat().st_size,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
            "ext": ext,
            "preview": safe_read_text(path, 1200) if ext in {".md", ".txt", ".json", ".yaml", ".py", ".bat"} else "",
        }

    ext_counts = Counter()
    total_files = 0
    total_bytes = 0
    test_files = []
    doc_files = []
    build_outputs = []
    media_files = []
    scenes_and_entries = []
    latest_mtime = 0.0
    earliest_mtime = None

    key_doc_names = {
        "readme.md", "claude.md", "agents.md", "plan.md", "architecture.md",
        "design.md", "project.godot", "package.json", "pyproject.toml",
    }

    for root, dirs, files in os.walk(path):
        rel_root = Path(root).relative_to(path)
        depth = len(rel_root.parts)
        if depth >= max_depth:
            dirs[:] = []
        else:
            dirs[:] = [
                d for d in dirs
                if d not in SKIP_DIRS
                and not d.startswith(".git")
                and d.lower() not in {"models", "checkpoints", "loras", "vae", "clip", "unet", "custom_nodes"}
            ]

        for f in sorted(files):
            fpath = Path(root) / f
            ext = fpath.suffix.lower()
            fname_low = f.lower()
            try:
                st = fpath.stat()
                sz = st.st_size
                mt = st.st_mtime
            except OSError:
                continue

            total_files += 1
            total_bytes += sz
            ext_counts[ext or "(no_ext)"] += 1
            if mt > latest_mtime:
                latest_mtime = mt
            if earliest_mtime is None or mt < earliest_mtime:
                earliest_mtime = mt

            rel_str = str(fpath.relative_to(path)).replace("\\", "/")
            abs_str = str(fpath).replace("\\", "/")

            if (
                fname_low.startswith("test_")
                or fname_low.endswith("_test.py")
                or fname_low.endswith("_test.gd")
                or ".test." in fname_low
                or ".spec." in fname_low
                or "tests/" in rel_str.lower()
            ) and ext in CODE_EXTS:
                test_files.append(rel_str)

            if fname_low in key_doc_names or (
                ext == ".md" and depth <= 2 and any(k in fname_low for k in ["readme", "plan", "exec", "spec", "summary", "guide", "pitch", "financial", "audit"])
            ):
                if len(doc_files) < 25:
                    doc_files.append({
                        "rel_path": rel_str,
                        "abs_path": abs_str,
                        "size": sz,
                        "preview": safe_read_text(fpath, 1500),
                    })

            if ext in BUILD_EXTS and sz > 0:
                if len(build_outputs) < 40:
                    build_outputs.append({
                        "rel_path": rel_str,
                        "abs_path": abs_str,
                        "ext": ext,
                        "size": sz,
                    })

            if ext in MEDIA_EXTS and sz > 1024:
                if len(media_files) < max_media:
                    media_files.append({
                        "rel_path": rel_str,
                        "abs_path": abs_str,
                        "ext": ext,
                        "size": sz,
                    })

            if ext in {".tscn", ".html"} and depth <= 3:
                if len(scenes_and_entries) < 30:
                    scenes_and_entries.append({
                        "rel_path": rel_str,
                        "abs_path": abs_str,
                        "ext": ext,
                        "size": sz,
                    })

    return {
        "path": str(path).replace("\\", "/"),
        "exists": True,
        "is_file": False,
        "total_files_scanned": total_files,
        "total_bytes_scanned": total_bytes,
        "earliest_mtime": datetime.fromtimestamp(earliest_mtime, tz=timezone.utc).isoformat() if earliest_mtime else None,
        "latest_mtime": datetime.fromtimestamp(latest_mtime, tz=timezone.utc).isoformat() if latest_mtime else None,
        "top_extensions": dict(ext_counts.most_common(15)),
        "test_file_count": len(test_files),
        "sample_test_files": test_files[:25],
        "key_docs": doc_files,
        "build_outputs": build_outputs,
        "scenes_and_html_entries": scenes_and_entries,
        "media_inventory": media_files,
    }


def extract_filesystem() -> dict:
    d_projects = {}
    proj_root = Path(r"D:\Projects")
    if proj_root.exists():
        for item in sorted(proj_root.iterdir()):
            if item.name == "Studio_Portfolio":
                continue
            d_projects[item.name] = summarize_project_dir(item, max_depth=5)

    d_toplevel_targets = [
        "FaceScanStudio",
        "Koala_Gabber_Phonk_170",
        "Comfy",
        "Tools",
        "ProjectMegaCity",
        "Console Gaming Stuff",
        "consolegamingstuff",
        "Fit Shit",
        "LocalAssistant",
        "TechWriter",
        "Babylon",
        "RetroBat_themes",
        "RetroBat_music",
        "RetroBat_decorations",
        "romsgames_ps1_gamecube_hub.html",
        "romsgames_universal_hub.html",
        "staging",
        "battletech_art.jpg",
        "enhanced_portrait_v2.jpg",
        "New folder",
    ]
    d_toplevel = {}
    for name in d_toplevel_targets:
        p = Path("D:\\") / name
        if p.exists():
            d_toplevel[name] = summarize_project_dir(p, max_depth=4 if name != "Comfy" else 3)

    # E:\ Emulation & RetroBat custom engineering
    e_drive_overview = {}
    e_root = Path("E:\\")
    if e_root.exists():
        e_drive_overview["top_level_folders"] = [
            p.name for p in sorted(e_root.iterdir()) if p.name != "System Volume Information"
        ]
        fw_path = e_root / "Firmware"
        if fw_path.exists():
            e_drive_overview["Firmware"] = summarize_project_dir(fw_path, max_depth=3)

        rb_root = e_root / "RetroBat"
        if rb_root.exists():
            rb_custom = {
                "root_scripts_and_configs": [],
                "tools": summarize_project_dir(rb_root / "tools", max_depth=4),
                "screenshots": summarize_project_dir(rb_root / "screenshots", max_depth=2),
                "custom_backgrounds": summarize_project_dir(rb_root / "custom_backgrounds", max_depth=2),
                "nsfw_media_summary": {
                    "exists": (rb_root / "nsfw_media").exists(),
                    "file_count": len(list((rb_root / "nsfw_media").rglob("*"))) if (rb_root / "nsfw_media").exists() else 0,
                },
            }
            for item in sorted(rb_root.iterdir()):
                if item.is_file() and item.suffix.lower() in {".py", ".bat", ".json", ".ini", ".txt", ".log"}:
                    rb_custom["root_scripts_and_configs"].append({
                        "name": item.name,
                        "abs_path": str(item).replace("\\", "/"),
                        "size": item.stat().st_size,
                        "preview": safe_read_text(item, 1200) if item.suffix.lower() in {".py", ".bat", ".json", ".txt"} else "",
                    })
            themes_dir = rb_root / "emulationstation" / ".emulationstation" / "themes"
            if themes_dir.exists():
                rb_custom["installed_themes"] = [p.name for p in sorted(themes_dir.iterdir()) if p.is_dir()]
            e_drive_overview["RetroBat"] = rb_custom

    # C:\Users\ogreb\.gemini & .summer
    c_ai_infra = {
        "memory_layer": summarize_project_dir(Path(r"C:\Users\ogreb\.gemini\antigravity\memory_layer"), max_depth=4),
        "scratch": summarize_project_dir(Path(r"C:\Users\ogreb\.gemini\antigravity\scratch"), max_depth=4),
        "config_skills": summarize_project_dir(Path(r"C:\Users\ogreb\.gemini\config\skills"), max_depth=3),
        "config_plugins": [
            p.name for p in sorted(Path(r"C:\Users\ogreb\.gemini\config\plugins").iterdir())
        ] if Path(r"C:\Users\ogreb\.gemini\config\plugins").exists() else [],
        "mcp_servers": [
            p.name for p in sorted(Path(r"C:\Users\ogreb\.gemini\antigravity\mcp").iterdir())
        ] if Path(r"C:\Users\ogreb\.gemini\antigravity\mcp").exists() else [],
        "summer_dir": summarize_project_dir(Path(r"C:\Users\ogreb\.summer"), max_depth=3),
        "godot_4_7_cli": {
            "path": r"D:/SteamFiles/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe",
            "exists": Path(r"D:\SteamFiles\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe").exists(),
        },
    }

    out = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "d_projects": d_projects,
        "d_toplevel": d_toplevel,
        "e_drive": e_drive_overview,
        "c_ai_infrastructure": c_ai_infra,
    }
    out_path = RAW_DIR / "filesystem_dump.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Wave 0] Exported filesystem inventory -> {out_path}")
    return out


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    mem = extract_memories()
    conv = extract_conversations()
    fs = extract_filesystem()
    print(
        f"\n[Wave 0 Complete] Memories={mem['total_memories']} | "
        f"Top-Level Convs={conv['top_level_count']} | "
        f"D:\\Projects entries={len(fs['d_projects'])}"
    )


if __name__ == "__main__":
    main()
