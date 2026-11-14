---
id: "universal-retro-catalog-hub"
title: "Universal 1,000-Title Retro Catalog & Discovery Hub"
subtitle: "Zero-dependency single-file HTML discovery dashboards indexing Top-50 master libraries across 20+ console and PC generations with Longplay previews and localStorage tracking."
pillar: "05-hardware-retro"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-18"
date_updated: "2026-10-14"
tags:
  - "retro-catalog"
  - "single-file-html"
  - "game-curation"
  - "vanilla-js"
  - "library-discovery"
metrics:
  - label: "Master Compendium"
    value: "1,000+ Curated Titles"
  - label: "Platform Generations"
    value: "20–22 Systems"
  - label: "Frontend Footprint"
    value: "2,456 LOC (2 HTML Apps)"
  - label: "External Dependencies"
    value: "0 Servers / 0 CDNs"
media:
  - src: "assets/media/universal-retro-catalog-hub/universal-hub.png"
    kind: "authentic"
    caption: "Live browser capture of the 20-platform, 1,000-title Universal Gaming & ROM Catalog Hub."
  - src: "assets/media/universal-retro-catalog-hub/ps1-gamecube-hub.png"
    kind: "authentic"
    caption: "Live browser capture of the dedicated PS1 & GameCube discovery hub with Longplay preview links and localStorage tracking."
diagram: ""
tech_stack:
  - "HTML5"
  - "CSS3 Custom Properties"
  - "Vanilla JavaScript (ES2022)"
  - "Browser localStorage API"
local_paths:
  - label: "Universal 20-Platform Catalog Hub"
    path: "file:///D:/romsgames_universal_hub.html"
  - label: "PS1 & GameCube Specialized Hub"
    path: "file:///D:/romsgames_ps1_gamecube_hub.html"
run_commands:
  - label: "Open Universal 1,000-Title Hub"
    command: "cmd /c start \"\" \"D:\\romsgames_universal_hub.html\""
  - label: "Open PS1 & GameCube Discovery Hub"
    command: "cmd /c start \"\" \"D:\\romsgames_ps1_gamecube_hub.html\""
memory_ids:
  - "99ab7b6f-0cc1-40a6-9ff0-5872baaa9360"
  - "4ec6be46-6160-4c9f-bab9-54ecd9fdaa6b"
  - "72297bdc-3f71-4164-a1c1-5af908775cb8"
  - "f76b225f-6e5c-44b5-8879-a553dc4624f0"
  - "f0177e1b-4706-4d01-b18b-869ceec92bfa"
  - "0f9cd774-16b8-419e-92c0-937e4ffc96d2"
  - "8c6f733f-5584-404c-8153-4387b3547823"
  - "32a58b01-aa9e-4b98-b951-3f81128097c7"
  - "035805e7-3bff-4034-96e3-5ae8af965567"
  - "7cf9f199-6e90-464a-95a1-829d81403d5a"
  - "f07cde51-e1bc-4a3f-b62d-e2e388e9cb90"
  - "04d26c98-821c-4195-96d3-7896ace8e8fc"
  - "d17c2578-d87a-4748-8513-044d92ee75b6"
  - "05f233ae-9039-44c6-b71e-5d220f5e4daa"
  - "db46e286-9a48-4049-bded-293e71f3a618"
  - "ad967d43-1865-4d05-83be-5e6e14e937ec"
  - "54c86ba8-af5a-4150-bae5-d042ff8f607f"
  - "1d572873-ec7b-424b-924a-eeabfa5c48ff"
  - "5076f5a0-d28d-4c8c-9abc-98cde0d87c70"
  - "b793f9e2-8292-4c70-8964-ba12cd47df34"
  - "f7681a4c-e195-4a7e-9a40-452f4a0e3c5f"
  - "73b81cb9-1783-4568-993c-6cab9d93841c"
  - "574d289b-b4b2-4af1-946f-35b8b9ffc6da"
  - "c289197b-ca4a-4d3a-a614-e81a60f9bc0e"
conversation_ids:
  - "734d4567-c5b0-4d4d-b027-109c77927d5f"
  - "ddf3ba04-5eee-46b7-94b2-f01a4e15826e"
---

## What It Is & Why It Matters

Building a multi-decade retro library usually ends in one of two traps: dumping 10,000 unplayable filler ROMs onto a drive so nobody can pick a game, or hunting across fragmented wikis every time you want to remember the best 4-player GameCube or Sega Saturn titles. We solved curation first by compiling a Systems-Architect-weighted Top-50 encyclopedia across 20 to 22 hardware generations (`1,000` to `1,100` curated classics, plus dedicated Top-50 2P/4P couch multiplayer and CPS-1/CPS-2/NeoGeo arcade manifests) and packaging the entire index into two instant-loading, single-file HTML discovery hubs on `D:\`.

Double-clicking either HTML file opens a dark-mode catalog right from `file:///` with zero backend servers, zero npm packages, and zero database setup. Every card pairs platform tags and genre notes with instant YouTube Longplay video lookups, verified archive search links, and persistent browser checkboxes so we could systematically audit and build out our living-room RetroBat collection without duplicate downloads.

## Real Example: How It Works in Practice

- **Input**: Opening `D:\romsgames_universal_hub.html` in any browser, filtering to **Sega Saturn** or **GameCube**, typing `"tactical"` or `"co-op"` in the instant search bar, and selecting five missing titles for verification.
- **What Happens**:
  1. Client-side JavaScript filters the embedded JSON manifest of 1,000+ curated titles in under 2 milliseconds, updating platform counters and completion progress bars live.
  2. Clicking a card's **Longplay Preview** button launches a targeted YouTube gameplay query so we can inspect mechanics and frame pacing in seconds before committing gigabytes of disk space.
  3. Clicking **Batch Open Selected** runs a staggered `1.5-second` tab timer (`setTimeout` queue) so browser popup blockers and upstream archive servers never rate-limit multi-item lookups.
  4. Checking off acquired titles writes completion state directly into `window.localStorage`, persisting progress across browser restarts.
- **Output**: Clean visual tracking across 20+ console generations, zero duplicate ISO/CHD collisions against existing `D:\` and `E:\` folders, and a curated 728-game living-room library where every single game earned its slot.

## Where It Stands & Next Steps

Both catalog applications are shipped and actively used on disk: `romsgames_universal_hub.html` (`480 KB`, `1,433 LOC`) covers 20 platforms and 1,000 core titles, while `romsgames_ps1_gamecube_hub.html` (`461 KB`, `1,023 LOC`) provides deep disc-era curation and batch tools for PlayStation and GameCube. In October 2026 (`C114`, `C117`), we extended the curation manifests with a library-matched Top-50 4-Player Couch Co-Op index and 17 Redump/MAME-verified CPS-1, CPS-2, and NeoGeo arcade fighters and beat-'em-ups.

Next steps to connect the web hubs even tighter to the local drives:
- Generate an optional local JSON manifest from `E:\RetroBat\roms\*\gamelist.xml` so the HTML hub auto-highlights titles already installed on `D:\` and `E:\` without manual checkbox clicks.
- Add a 4-player couch-party randomizer wheel filter inside `romsgames_universal_hub.html` for game nights.

## Under the Hood & Local Files

Across 24 Memory Bank entries (`M0742`–`M0762`, `M0846`–`M0848`), we standardized each platform's Top-50 manifest (DOS, Win9x, Modern PC, NES, SNES, GBA, N64, GameCube, Wii, Switch, NDS, 3DS, Saturn, Dreamcast, PS1, PS2, PS3, PS4, PSP, Original Xbox, Xbox 360, and current-gen benchmarks) around deep systemic mechanics rather than pure nostalgia sales charts. Both dashboards inline all CSS tokens, SVG icons, and structured game arrays inside standalone `.html` documents so they remain portable forever on any USB stick or offline drive.

Local files on `D:\`:
- **20-Platform 1,000-Title Master Hub (`1,433 LOC`, `480 KB`)**: [romsgames_universal_hub.html](file:///D:/romsgames_universal_hub.html)
- **PS1 & GameCube Specialized Discovery Hub (`1,023 LOC`, `461 KB`)**: [romsgames_ps1_gamecube_hub.html](file:///D:/romsgames_ps1_gamecube_hub.html)
