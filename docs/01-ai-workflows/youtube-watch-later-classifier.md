---
id: "youtube-watch-later-classifier"
title: "YouTube Watch Later Classifier & Trusted-Types Sorter"
subtitle: "Zero-API-key Python oEmbed classifier and CSP-compliant browser console HUD that sorted a 2,378-video Google Takeout backlog into thematic playlists."
pillar: "01-ai-workflows"
entry_type: "workflow"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-18"
date_updated: "2026-08-18"
tags:
  - "browser-automation"
  - "python"
  - "trusted-types-csp"
  - "google-takeout"
  - "data-classification"
metrics:
  - label: "Videos Processed"
    value: "2,378"
  - label: "Target Playlists"
    value: "22 - 25"
  - label: "Parallel Workers"
    value: "35 Threads"
  - label: "YouTube API Quota Used"
    value: "0 Units"
media: []
diagram: "assets/diagrams/youtube-watch-later-classifier.svg"
tech_stack:
  - "Python 3 (ThreadPoolExecutor)"
  - "YouTube oEmbed JSON"
  - "Vanilla JS (Trusted-Types DOM)"
  - "Tampermonkey Userscript"
local_paths:
  - label: "Python Takeout Classifier"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/classify_watch_later.py"
  - label: "Trusted-Types Browser Console HUD"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/youtube_sorter_console.js"
  - label: "Classification Summary Report"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/classification_summary.md"
run_commands:
  - label: "Run Multi-Threaded Takeout Classifier"
    command: "python \"C:\\Users\\ogreb\\.gemini\\antigravity\\scratch\\classify_watch_later.py\""
memory_ids:
  - "1d892310-5bf1-494a-b2b2-1a063813bc9f"
conversation_ids:
  - "92f7a972-84bb-4600-9191-0dfefdbf6d9e"
---

## What It Is & Why It Matters

Once a YouTube Watch Later queue crosses two thousand saved videos, it stops functioning as a reading list and turns into an unsearchable archive. Worse, Google's official YouTube Data API v3 restricts programmatic access to the private `WL` Watch Later playlist ID and burns strict daily quota units on playlist insertions, while modern Chromium enforces `Trusted-Types` Content Security Policy (CSP) headers on `youtube.com` that instantly crash traditional `innerHTML` userscripts.

On August 18, 2026, we built a two-stage local classification and DOM-sorting workflow (`classify_watch_later.py` paired with `youtube_sorter_console.js`) to clear a `2,378`-video Watch Later export without touching OAuth tokens or API quotas. Stage 1 ingests the raw Google Takeout Watch Later CSV, resolves every live video's title and channel name at high speed via YouTube's public `oembed` endpoint using a 35-worker Python thread pool, flags deleted/private deadweight, and maps each video into thematic user playlists.

Stage 2 runs directly inside the logged-in browser tab on `https://www.youtube.com/playlist?list=WL`. Built 100% with imperative DOM nodes (`document.createElement` and `textContent`, zero `innerHTML` strings) so YouTube's `TrustedHTML` CSP gate never blocks execution, it mounts a floating dark-mode control HUD that loads `classified_videos.json`, clicks through YouTube's native "Save to playlist" menus at human-safe intervals, and optionally removes each filed item from Watch Later.

## Real Example: How It Works in Practice

- **Input**: A Google Takeout `Watch later-videos.csv` containing `2,378` bare video IDs accumulated over several years, plus `25` existing thematic playlists on the account (`general history`, `gamedev godot`, `warhammer40k`, `modeling and animation`, `Woodworking`, etc.).
- **What Happens**:
  1. **35-Thread oEmbed Enrichment (`classify_watch_later.py`)**: Queries `youtube.com/oembed` concurrently with incremental checkpoints every 100 videos into `metadata_cache.json` (`495 KB`), separating active videos from `192` (`8.1%`) unavailable/deleted entries.
  2. **Channel + Regex Topic Matching**: Evaluates channel-author allowlists (e.g., `GDQuest`, `Sebastian Lague`, `Forgotten Weapons`, `Fall of Civilizations`, `Blender Guru`) and word-boundary regexes across 22–25 topic buckets, writing `classified_videos.json` (`512 KB`) and `classification_summary.md`.
  3. **Trusted-Types Browser Filing (`youtube_sorter_console.js`)**: Pasting the script into DevTools Console (or running via Tampermonkey) opens `#yt-wl-sorter-panel`, imports `classified_videos.json`, and steps down the live Watch Later DOM list with a tunable `1.8s` (`1,000–4,000 ms`) pace slider and Pause/Stop controls.
- **Output**: `2,378` videos audited (`328` routed to `general history`, `180` to `Films`, `146` to `Gaming Lists`, `146` to `modern and historical weapons`, `70` to `true crime`, `60` to `Esoterics and magic`, `33` to `Elder Scrolls`, plus specialized dev/craft queues) and automated live cleanup of `playlist?list=WL`.

## Where It Stands & Next Steps

Both stages are shipped and verified on disk inside `C:\Users\ogreb\.gemini\antigravity\scratch\` (`995 LOC` combined across `classify_watch_later.py` and `youtube_sorter_console.js`, plus the companion Tampermonkey wrapper `youtube_watch_later_sorter.user.js`, cached `metadata_cache.json`, and `classified_videos.json`).

Next steps if re-running on future Takeout exports:
- Route the remaining `1,051` long-tail `Uncategorized` titles through our zero-VRAM `BAAI/bge-small-en-v1.5` ONNX embedder (`memory_layer`) to cluster ambiguous video titles semantically without hand-writing new regexes.
- Add a one-click JSON export button inside the browser HUD to save newly skipped or manually re-tagged videos back to disk.

## Under the Hood & Local Files

### Engineering Highlights
- **Zero-Quota Metadata Harvesting (`classify_watch_later.py`)**: Uses Python `urllib.request` + `ThreadPoolExecutor(max_workers=35)` against `https://www.youtube.com/oembed?...&format=json`, distinguishing HTTP `401/403/404` (`unavailable`) from transient network errors while checkpointing JSON every 100 items.
- **Strict Trusted-Types CSP Compliance (`youtube_sorter_console.js`)**: Modern YouTube throws `TypeError: Failed to set the 'innerHTML' property on 'Element': This document requires 'TrustedHTML' assignment`. Every HUD widget—live Sorted/Skipped/Processed counters, range slider, file-picker input, and action buttons—is constructed cleanly via `document.createElement()` and `.textContent`.

### Key Local Files
- [classify_watch_later.py](file:///C:/Users/ogreb/.gemini/antigravity/scratch/classify_watch_later.py) — `466 LOC` multi-threaded Google Takeout CSV parser, oEmbed fetcher, and rule-based playlist classifier.
- [youtube_sorter_console.js](file:///C:/Users/ogreb/.gemini/antigravity/scratch/youtube_sorter_console.js) — `529 LOC` Trusted-Types-safe interactive YouTube DOM sorter HUD.
- [youtube_watch_later_sorter.user.js](file:///C:/Users/ogreb/.gemini/antigravity/scratch/youtube_watch_later_sorter.user.js) — Persistent Tampermonkey userscript build of the sorter panel.
- [classification_summary.md](file:///C:/Users/ogreb/.gemini/antigravity/scratch/classification_summary.md) — Exact 2,378-video distribution table across playlists.
- [classified_videos.json](file:///C:/Users/ogreb/.gemini/antigravity/scratch/classified_videos.json) — `512 KB` video-ID-to-playlist mapping payload consumed by the browser HUD.
