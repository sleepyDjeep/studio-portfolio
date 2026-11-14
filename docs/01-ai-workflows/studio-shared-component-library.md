---
id: "studio-shared-component-library"
title: "Studio Shared Component & Shader Library"
subtitle: "Centralized 10,522-LOC catalog of battle-tested Godot 4.7 autoloads, anime cel-shaders, procedural 3D Python mesh generators, AI bridges, and public-records scrapers."
pillar: "01-ai-workflows"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-09-18"
date_updated: "2026-11-01"
tags:
  - "shared-library"
  - "godot-4.7"
  - "gdshader"
  - "procedural-3d"
  - "test-harness"
  - "code-reuse"
metrics:
  - label: "Extracted Source Code"
    value: "10,522 LOC"
  - label: "Reusable Code Modules"
    value: "68 Files"
  - label: "Godot Shaders"
    value: "4 (.gdshader)"
  - label: "Disk Footprint"
    value: "650 KB"
media: []
diagram: "assets/diagrams/studio-shared-component-library.svg"
tech_stack:
  - "GDScript (Godot 4.3+ / 4.7)"
  - "Godot Shader Language (GLSL)"
  - "Python 3 (Zero-Dep Stdlib)"
  - "TypeScript (Multi-LLM + ComfyUI)"
local_paths:
  - label: "Shared Component Library Root"
    path: "file:///D:/Projects/_Shared_Library"
  - label: "Master Component Catalog"
    path: "file:///D:/Projects/_Shared_Library/CATALOG.md"
run_commands:
  - label: "Generate Procedural 3D Weapon GLBs"
    command: "cd \"D:\\Projects\\_Shared_Library\\procedural_tools\" && python generate_weapons.py"
  - label: "Run Headless Godot Regression Template"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --headless -s \"D:\\Projects\\_Shared_Library\\game_systems\\master_test_runner.gd\""
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

After shipping our first half-dozen games, engines, and data platforms in August and September 2026, we noticed every new prototype needed the exact same foundational plumbing: a zero-coupling typed event bus, a headless Godot test runner that catches leaked orphan nodes, crisp anime cel-outline shaders, rapid placeholder `.glb` 3D weapon/tile meshes, and multi-provider local LLM/ComfyUI adapters. Rewriting those modules from scratch wasted hours and risked re-introducing bugs we had already solved elsewhere.

On September 18, 2026, we consolidated our cleanest, most battle-tested subsystems into **`D:\Projects\_Shared_Library`** (`10,522 LOC` across 68 source files, indexed in `CATALOG.md`). Every module in the library was extracted directly from a shipped or milestone-verified production build—including *Babylon*, *PocketRPG Studio*, *ShadowWarriorRoguelite*, *Aether Engine*, and *PropertyIntel*—and stripped of project-specific coupling so it drops cleanly into any new repository.

Having this shared kit on disk changes how fast our studio prototypes. A brand-new 3D action game or CRPG starts on minute one with deterministic graph state tracking (`world_state.gd`), millisecond-timed headless regression testing (`master_test_runner.gd`), procedural `.glb` arena geometry (`generate_level_tiles.py`), and stylized cel-shading (`AnimeCelShader.gdshader`) already wired and verified.

## Real Example: How It Works in Practice

- **Input**: Scaffolding a new first-person 3D Godot 4.7 combat prototype that needs immediate melee/ranged `.glb` weapon models, damage hit-flash feedback, cel-shaded outlines, and an automated CI test harness before custom art exists.
- **What Happens**:
  1. **Zero-Dependency 3D Asset Bootstrap**: Running `python generate_weapons.py` and `python generate_level_tiles.py` inside `procedural_tools/` uses pure Python standard-library binary glTF packing to emit ready-to-import `.glb` weapon meshes, modular walls, pillars, and stat scripts into an `output/` folder in seconds.
  2. **Architecture & Shader Drop-In**: Copying `event_bus.gd` and `demo_shell.gd` from `game_systems/` sets up decoupled typed signals and pause/start menus, while assigning `AnimeCelShader.gdshader`, `OutlinePass.gdshader`, and `HitFlash.gdshader` from `shaders_and_vfx/` provides stepped diffuse lighting, inverted-hull ink outlines, and `0.15s` tweened damage flashes.
  3. **Automated Leak & Timing Gate**: Attaching `master_test_runner.gd` runs every suite via `godot --headless`, recording per-suite millisecond execution budgets and asserting zero orphaned scene nodes on exit.
- **Output**: A playable, visually stylized, and headless-test-guarded Godot 4.7 vertical slice assembled in minutes without external asset downloads or third-party addon bloat.

## Where It Stands & Next Steps

The library is an active reusable studio catalog (`94` total files, `650 KB` on disk) spanning `8,073 LOC` across 50 Python scripts, `2,281 LOC` across 7 GDScript core systems, `159 LOC` across 4 `.gdshader` visual effects, and TypeScript AI adapter stubs, all documented with integration guides in `CATALOG.md`.

Next steps for the shared catalog:
- Promote *Kaiju Kiosk*'s `audit_asset_metrics.py` (GLB triangle/texel-density checker) and `ink_cel_manga.gdshader` halftone shader into `procedural_tools/` and `shaders_and_vfx/`.
- Add a lightweight `sync_component.py` CLI script that stamps semantic version headers into copied modules so downstream games can pull upstream fixes cleanly.

## Under the Hood & Local Files

### Five-Domain Module Breakdown
1. **Godot 4.3+ / 4.7 Game Systems (`game_systems/`)**:
   - `event_bus.gd` & `world_state.gd` (*Babylon*): Layer-decoupled typed signal bus and graph-node condition evaluator.
   - `fall_system.gd` & `demo_shell.gd` (*Babylon*): Data-driven threshold escalation (`EventBus.quarter_fell`) and universal title/pause/ending wrapper.
   - `master_test_runner.gd`, `playtest_runner.gd`, & `prpg_bundle_manager.gd` (*PocketRPG Studio*): Headless assertion runner with leak detection, automated playtest bot harness, and portable `.zip` project bundler.
2. **Stylized Shaders & VFX (`shaders_and_vfx/`)**: `AnimeCelShader.gdshader`, `HitFlash.gdshader`, `OutlinePass.gdshader`, and `RetroPostProcess.gdshader` (palette quantization + CRT scanlines from *ShadowWarriorRoguelite*).
3. **Procedural 3D Mesh Generators (`procedural_tools/`)**: Stdlib-only Python generators (`generate_weapons.py`, `generate_enemies.py`, `generate_level_tiles.py`, `generate_zany_bosses.py`).
4. **Multi-Provider AI Adapters (`ai_pipelines/aether_ai_suite/`)**: Unified client bridging LM Studio (`:1234`), Ollama (`:11434`), cloud LLMs, and ComfyUI binary WebSocket streams.
5. **Scraper & Alert Infrastructure (`data_scrapers/`)**: 50-state tax-deed/foreclosure vendor drivers (`nationwide_scrapers/`) plus Telegram/Slack alert and Excel/PDF dossier dispatchers (`alert_and_publishing_services/`).

### Key Local Files
- [CATALOG.md](file:///D:/Projects/_Shared_Library/CATALOG.md) — Master directory map and drop-in integration recipes.
- [event_bus.gd](file:///D:/Projects/_Shared_Library/game_systems/event_bus.gd) & [world_state.gd](file:///D:/Projects/_Shared_Library/game_systems/world_state.gd) — Decoupled signal and graph-state spine.
- [master_test_runner.gd](file:///D:/Projects/_Shared_Library/game_systems/master_test_runner.gd) — Headless Godot regression runner enforcing timing and zero-leak checks.
- [AnimeCelShader.gdshader](file:///D:/Projects/_Shared_Library/shaders_and_vfx/AnimeCelShader.gdshader) & [OutlinePass.gdshader](file:///D:/Projects/_Shared_Library/shaders_and_vfx/OutlinePass.gdshader) — Stepped cel-band and inverted-hull outline shaders.
- [generate_weapons.py](file:///D:/Projects/_Shared_Library/procedural_tools/generate_weapons.py) — Zero-dependency Python `.glb` 3D weapon mesh synthesizer.
- [public_domain_mashup_worlds.md](file:///D:/Projects/_Shared_Library/storytelling_ideas/public_domain_mashup_worlds.md) — 15 public-domain sci-fi/fantasy mashup game & fiction bibles plus a 4-axis remix matrix (`storytelling_ideas/`).
