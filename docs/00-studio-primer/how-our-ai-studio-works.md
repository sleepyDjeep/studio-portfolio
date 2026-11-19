---
id: how-our-ai-studio-works
title: How Our AI Studio Works
subtitle: Our end-to-end operating system for turning raw ideas into verified software, games, hardware blueprints, and business
  models on a single local workstation.
pillar: 00-studio-primer
entry_type: workflow
readiness: shipped
visibility: main
date_started: '2026-08-16'
date_updated: '2026-11-19'
tags:
- studio-primer
- multi-agent-orchestration
- lancedb
- godot-4.7
- local-first-ai
metrics:
- label: Indexed Memories
  value: 1,024
- label: Audited Sessions
  value: '139'
- label: Shipped & Active Entries
  value: 48 Public
- label: Marginal Cloud GPU Cost
  value: $0
media:
- src: assets/concepts/how-our-ai-studio-works.png
  kind: concept
  caption: 'Concept Preview: Overview of our 4-surface LanceDB memory sync, wave-based specialist agents, RTX 4060 GPU scheduling,
    and automated QA gates.'
diagram: assets/diagrams/how-our-ai-studio-works.svg
tech_stack:
- Google Antigravity IDE
- LanceDB + FastEmbed ONNX
- Godot 4.7 Forward+
- LM Studio + ComfyUI
- Blender 5.1 Headless
- Python 3.13
local_paths:
- label: Antigravity Studio Root
  path: file:///C:/Users/ogreb/.gemini/antigravity
- label: Studio Portfolio Repository
  path: file:///D:/Projects/Studio_Portfolio
- label: Active Projects Drive
  path: file:///D:/Projects
run_commands:
- label: Inspect Memory Bank Stats
  command: agy-memory stats
- label: Launch Portfolio Viewer
  command: python "D:\Projects\Studio_Portfolio\scripts\serve_portfolio.py"
memory_ids:
- 38ed07f2-1fdc-4a78-aeaa-f3cbb59b2dde
- d8420cde-f24e-4d98-9dbe-0965bf858c01
- 1727a66b-d35e-41ee-a599-b995d2e90356
- 04832327-fd29-44e7-acfa-6309612b5ce0
- 1064b50b-e332-4756-81c5-85fb1bbace34
- bbc67af9-a4c2-411d-82b1-94c2a6ad4ae3
- 2f89c6ab-a332-4985-8a49-4cd55f3e6a28
- b704d156-6310-4f7f-9306-5f1003617d2c
- 68685cf3-3c67-414b-9989-fe93811a00f2
- 3bf01e6a-7b41-4660-a00a-fb5957fd6e50
- 586386e6-6a15-4b1e-bad0-f4ebe739e2aa
- 329c4b8e-50d4-41b3-91ac-b232a289ffc5
- a0204d7d-d870-446c-9c63-26be647dd39e
- 8985c70a-b524-450a-901c-9dc39350984f
- c3a4208c-a920-4480-a5d4-13b034124f2c
- 3a5f8a9e-d474-4c81-9ce2-36537bdf952e
- 44530b61-d984-4939-952c-0d09960fc3eb
- a490ffb9-653e-4da8-8c8d-2d1c675f4188
- 32e3f2ac-5e83-4a7e-b43c-2e9fdb739ab0
- cb3caf06-eb2d-4a89-8811-167ba275d685
- 18c41ba8-b0b1-41a5-9381-00d17b1870cc
conversation_ids:
- 6b75cdd6-3bc3-48e8-bbb9-b9eb979bd951
- e49d7a48-445a-4a68-ada7-8e54abcefb40
---

## What It Is & Why It Matters

Since August 16, 2026, our studio has built 48 public software systems, playable games, custom engines, nationwide SaaS scrapers, and physical hardware blueprints from a single Windows 11 workstation. Most solo or two-person teams stall out when context evaporates between chat threads or when AI tools generate plausible-looking code that collapses on launch. We solved both bottlenecks by engineering a repeatable studio operating pipeline before scaling up production.

Every major project begins with a structured `/grill-me` architectural interview—up to 100 rapid-fire engineering and design questions that lock down scope, data schemas, failure modes, and aesthetic rules before a single line of code is written. Those answers go straight into a shared local LanceDB vector database (`1,020` indexed memories) that synchronizes in real time across our IDE, command line, local LLMs in LM Studio, and image/3D graphs in ComfyUI. When we switch from writing GDScript physics in the morning to generating PBR textures in the afternoon, every tool already knows the exact visual palette, polygon budget, and naming conventions.

Execution runs in disciplined, wave-based swarms of specialist agents followed by adversarial quality gates. Builders never grade their own homework. Every milestone must pass headless automated assertions—such as `172,200` assertions in our *MechWarrior 2* engine recreation or `7,544` assertions plus a 10-lens computer-vision video audit in *Kaiju Kiosk*—before an independent Challenger agent certifies the build.

## Real Example: How It Works in Practice

- **Input**: A raw one-sentence pitch on September 18, 2026 to turn an early convenience-store prototype into *Kaiju Kiosk*, a stylized Neo-Tokyo night-shift simulator paired with a standalone commercial 3D asset pack.
- **What Happens**:
  1. **Memory & Scope Lock**: The coordinator queries LanceDB for prior studio shader preferences, locks the target engine to native Godot 4.7 Forward+, and establishes a dual-deliverable plan (playable `.exe` vertical slice plus a `$19.99` marketplace kit).
  2. **Wave-Based Parallel Production**: Specialist subagents work in non-overlapping file shards—one builds headless Blender 5.1 Python scripts to kitbash and bake `2048x2048` Cycles PBR textures, another writes the stepped manga cel-shader and barcode-scanner physics, and a third builds live WebSocket redline and room-layout tools.
  3. **Sequential 8 GB GPU Time-Slicing**: To avoid out-of-memory crashes on our 8 GB RTX 4060 Laptop GPU, the pipeline unloads LM Studio weights, clears ComfyUI cache, runs headless Blender Cycles bakes, and then boots Godot Vulkan Movie Maker to record a deterministic 90-second (`2,160`-frame) walkthrough video.
  4. **Adversarial Verification**: Ten computer-vision audit lenses inspect every frame of the walkthrough video in SQLite while a separate Challenger agent runs `28` headless test suites.
- **Output**: A shipped `728.77 MB` standalone Windows executable (`KaijuKiosk_Demo.exe`), a `2,247`-file commercial 3D asset pack, `7,544` passing assertions, and a certified `94.21/100` visual audit score with zero critical defects.

## Where It Stands & Next Steps

Our studio operating infrastructure is shipped and used daily across all six public portfolio pillars (`139` top-level engineering sessions and `1,024` persistent memories). The last five days alone produced two shipped Godot 4.7 titles - *HydroHavoc* with a browser demo on day one, and the seven-game *MarcoPoloLive* suite plus its standalone chat relay - while *MechDestroyer* moved to a reproducible, CI-gated Windows export with `117 / 117` suites passing a zero-leak runner. Two hardware blueprints also entered the catalog: a solar automatic chicken feeder for the Guadalupe Loop flock and a universal auto-detecting battery charger station for the bench. Storage governance is strictly enforced after a September 18 workstation audit reclaimed `356.32 GB` across drives, isolating `C:\` strictly for Windows OS services while routing active codebases to `D:\Projects` (`732 GB` free NVMe space) and large emulation archives to `E:\` via zero-byte NTFS junctions. We also completed our engine standardization pivot on August 28 and September 18, retiring early Summer Engine experiments (`3.55 GB` reclaimed) in favor of pure Godot 4.7 paired with `godot-mcp` and 38 `godot-prompter` skills.

Next steps for the studio operating layer:
- Add automated post-commit hooks that re-run `master_manifest.json` catalog compilation whenever a project's test count or export binary updates on `D:\Projects`.
- Expand the headless Challenger verification harness to capture automated WebGL2 frame-time telemetry for browser-hosted builds alongside Godot Vulkan captures.
- Package our `/grill-me` 100-question specification templates into a standalone CLI generator inside `D:\Tools\Scripts`.

## Under the Hood & Local Files

### Workstation & Toolchain Profile
- **Hardware Envelope**: Intel Core i9-13900H (14 cores / 20 threads), 16 GB system RAM, NVIDIA GeForce RTX 4060 Laptop GPU (`8 GB GDDR6` dedicated VRAM), Windows 11.
- **4-Surface Memory Synchronization**: Powered by `memory_layer` (`BAAI/bge-small-en-v1.5` 384-dim CPU ONNX embeddings consuming `0 MB` GPU VRAM) bridging Antigravity IDE (`mcp_server.py`), terminal (`agy-memory`), LM Studio (`127.0.0.1:11234` OpenAI reverse proxy), and ComfyUI custom nodes.
- **MCP & Skill Ecosystem**: 8 configured MCP servers (`antigravity-memory`, `comfyui` with 38 graph/VRAM tools, `godot` with 12 project tools, `godot-ai` with 37 live scene/shader/test tools, `ui-skills`, `lmstudio`, `science_biomolecular_structure_viewer_mcp`, and archived `summer-engine`) backed by global anti-slop `/ui` and `prose` governance skills.
- **System Hygiene Scripts**: Custom PowerShell and batch utilities in `D:\Tools\Scripts` eliminate OEM kernel handle leaks (`7.3M` handles diagnosed across `AcerSystemCentralService` and Fast Startup), disable redundant drive indexing, and verify flash storage capacity at the raw byte-offset level.

### Key Local Files
- [master_manifest.json](file:///D:/Projects/Studio_Portfolio/data/master_manifest.json) — Canonical studio ledger linking all `1,020` memories and `137` conversations across our 6 pillars.
- [pyproject.toml](file:///C:/Users/ogreb/.gemini/antigravity/memory_layer/pyproject.toml) — Package definition for our zero-cloud Python 3.13 persistent memory engine.
- [CLAUDE.md](file:///D:/Projects/CLAUDE.md) — Root Godot 4.7 compiler guardrail directive enforced across GDScript workspaces.
- [CATALOG.md](file:///D:/Projects/_Shared_Library/CATALOG.md) — Cross-project registry of reusable GDScript autoloads, shaders, procedural 3D scripts, and scrapers.
- [Unblock_Port_24766.bat](file:///D:/Tools/Scripts/Unblock_Port_24766.bat) — Automated workstation firewall utility inside our `D:\Tools\Scripts` maintenance suite.
