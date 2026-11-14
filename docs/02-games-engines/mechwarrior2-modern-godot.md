---
id: "mechwarrior2-modern-godot"
title: "MechWarrior 2 Clean-Room Godot 4.7 Engine & PRJ Parser"
subtitle: "Native GDScript binary archive parser and clean-room Godot 4.7 recreation bridging 1995 MechWarrior 2 Trilogy assets into 60+ FPS widescreen, HOTAS, and Tri-Mode shaders."
pillar: "02-games-engines"
entry_type: "project"
readiness: "active-build"
visibility: "main"
date_started: "2026-08-23"
date_updated: "2026-08-23"
tags:
  - "godot-4-7"
  - "clean-room-engine"
  - "binary-parser"
  - "retro-modernization"
  - "hotas"
  - "mecha"
metrics:
  - label: "Headless Assertions"
    value: "172,200 Passing"
  - label: "Automated Suites"
    value: "46 Test Suites"
  - label: "Smacker FMVs Indexed"
    value: "479 Cutscenes"
  - label: "Visual Modes"
    value: "3 Live Renderers"
media:
  - src: "assets/concepts/mechwarrior2-modern-godot.png"
    kind: "concept"
    caption: "Concept Preview: Clean-room Godot 4.7 binary archive parser rendering 1995 WTB geometry across 1995 Flat, 1997 3Dfx Glide, and Modern Cel-Shaded modes."
diagram: "assets/diagrams/mechwarrior2-modern-godot.svg"
tech_stack:
  - "Godot 4.7"
  - "GDScript Binary Stream Parsers"
  - "Godot Shader Language (Tri-Mode)"
  - "HOTAS / XInput / Android Gyro"
local_paths:
  - label: "Consolidated Mecha Engine Workspace"
    path: "file:///D:/Projects/MechDestroyer"
run_commands:
  - label: "Launch Consolidated Godot 4.7 Mecha Workspace"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\MechDestroyer\""
memory_ids:
  - "5f9e8724-e9aa-48ea-8b7f-474974ab1e17"
  - "26959511-386f-42fd-8f20-64fc719d0e6d"
  - "0b277e36-1d80-4fb6-bf96-3e69178a1797"
  - "7ec16225-de0c-403a-a1d6-e8eb1463da92"
  - "afed1f5b-105b-4587-8360-f61375523d79"
  - "57b71200-6032-4bcc-a9a4-a1c1e088f71f"
  - "8c8e38bf-d15a-4387-82ab-939ff7b10af7"
  - "8f8aac48-bb97-4992-bceb-3fb5d644bf6d"
  - "f3121325-465f-4aa9-a2f9-54cd7a4af60f"
  - "e8502692-f87e-4f6e-8f30-a33cb85402d5"
  - "3be41037-4ca2-4b51-a62f-e91de0b4c796"
  - "9cff326b-f261-434b-86a5-5530b3cf96dc"
  - "797da380-e4b7-4c6a-a5af-2aef534f1b82"
  - "a9a42773-c4b8-49fe-b39e-f096cd9e1862"
  - "5fe66376-432a-4c65-bf85-37867b8bfc81"
  - "91c9c0d0-d20c-4d11-8a74-25a0456a6bc7"
  - "3e4aab58-c03d-4d18-906e-ccb112b683c1"
  - "08b98f36-c0ca-42bb-8c7e-ef781fd70dd8"
  - "8fe7a714-920e-4ccc-aa09-1df441ab950a"
  - "081363c7-87c5-463a-9654-6ff8ed7098f9"
  - "6a0faf5e-81f4-4e68-b727-1047e8abca3c"
  - "3684e6a5-fb8d-495d-acfd-c3df1190cbab"
  - "70c2a5cd-5083-42b5-a4e4-f6ac6b7329a6"
  - "d9df19f7-59ab-4994-91b0-44f66fa68ec3"
  - "6b9ef7af-0dbe-4c4d-a668-d06fe5dda457"
  - "1a95a8c9-81d9-4e0f-b1e2-407711cfad7f"
  - "b1388d45-d9d6-47ec-a8be-3964bced350f"
  - "ecde1602-507c-4e52-b235-1110e97f42ec"
  - "96932e5c-1be5-481c-992f-352426f92115"
  - "067f12f7-5a90-4ac2-8918-091ae46487fa"
  - "02846772-c601-47c2-9506-54d08770aed8"
  - "0742689a-4adc-40a0-ae5f-c7c7aa4a4188"
  - "429cc243-b037-49e1-ad2e-52a2ee95e7b8"
  - "025397e7-73f3-4531-bd22-f1effdb580ba"
  - "0d4012a3-1c40-4567-9785-a5663aea8c64"
  - "2f7fa24e-2e44-4679-b83c-62f623025bee"
  - "abae53f6-6011-4763-ad6f-e4b2684968bd"
  - "5140c7bf-a043-46f7-ae01-3acf12544a7f"
conversation_ids:
  - "112875e4-2f75-4bd3-a50d-64b396b83d38"
  - "99887603-5511-40e7-b51e-42ce5c32c845"
  - "0163fae5-f4bf-456e-8d80-6dd20d7114f0"
---

## What It Is & Why It Matters

*MechWarrior 2 Clean-Room Godot 4.7 Engine* is a native GDScript binary archive reader and clean-room simulation runtime built to parse original 1995–1996 Activision `MW2.PRJ` data containers—spanning *31st Century Combat*, *Ghost Bear's Legacy*, and *Mercenaries*—directly into modern 60+ FPS widescreen Vulkan without shipping a single byte of proprietary copyrighted data. By pointing the parser at a player's legally owned retail CD or ISO archive, the engine reconstructs 1995 `WTB` 3D mech and terrain geometry, `BWD` mission scripts, `SHP` HUD bitmaps, `XMI` music, `SND` PCM sound effects, and `479` Smacker `.SMK` briefings inside Godot 4.7.

Running 1995 DOS and Windows 95 sims natively on Windows 11 240 Hz laptops normally forces an ugly trade-off: either wrestle with CPU-speed heap crashes in legacy executables or lose authentic mission geometry. We built this clean-room Godot parser alongside our Windows 11 DLL preservation wrapper (`mw2-mw4-preservation-suite`) to compare both approaches head-to-head—and to extract exact binary table truths about torso kinematics, heat-sink dissipation, and mission scripting that directly informed our standalone commercial game, *MechDestroyer*.

## Real Example: How It Works in Practice

- **Input**: A user supplies their retail `MW2.PRJ` archive from *MechWarrior 2: 31st Century Combat* alongside a USB HOTAS throttle-and-rudder setup (or an Android phone running the virtual gyro/touch cockpit) and launches a Clan Jade Falcon trial mission.
- **What Happens**: Native `FileAccess` binary readers walk the `MW2.PRJ` directory header and indexed symbol tables, decoding chunked `WTB` vertex/polygon records into Godot `ArrayMesh` surfaces, interpreting `BWD` binary world tags to place navpoints and enemy stars, and routing `.SMK` video streams into the in-engine HoloCinema briefing player. During combat, pressing the **Tri-Mode Visual Switcher** hotkey swaps materials on the fly between three eras: `1995 Flat-Shaded` (authentic 256-color indexed software polygons), `1997 3Dfx Glide` (bilinear texture filtering with classic horizon fog), and `Modern Cel-Shaded` (PBR metallic response with comic ink outlines).
- **Output**: Smooth 60+ FPS widescreen mech simulation with zero 1995 timer division-by-zero crashes, full multi-axis HOTAS deadzone curves, XInput gamepad mapping, and mobile gyro aiming—verified across `172,200` automated binary-parsing assertions.

## Where It Stands & Next Steps

This project stands as an **active-build** architectural core whose binary-parsing test suites (`46` headless suites, `172,200` passing assertions documented in `38` Unified Memory Bank entries `M0200`–`M0237`) completed verification on August 23, 2026. During our September 18 workstation storage audit (`M0763`–`M0767`), we intentionally retired `~186 GB` of extracted retail ISO staging folders (`MW2xtracted` and `MW2_Trilogy_Runner` temp mounts) so our active `D:\Projects` drive focused exclusively on IP-clean original games (`D:\Projects\MechDestroyer`) while keeping retail-disc preservation inside our dedicated `mw2-mw4-preservation-suite` runner.

Next steps if we package this clean-room engine as an open-source preservation release:
- Publish the standalone zero-asset `MW2.PRJ` / `WTB` / `BWD` GDScript parser modules as a clean MIT-licensed Godot 4.7 addon with an automatic retail-ISO path autodetector.
- Wire full `XMI` General MIDI soundfont synthesis directly into Godot's `AudioStreamGenerator` so soundtracks play without external SoundCanvas wrappers.
- Add side-by-side split-viewport comparison mode allowing players to view `1995 Flat-Shaded` on the left half of the screen and `Modern Cel-Shaded` on the right in real time.

## Under the Hood & Local Files

### Clean-Room Binary Format Decoders & Tri-Mode Pipeline
Every format decoder (`M0200`–`M0237`) was written in pure GDScript without external C++ DLL dependencies so the runtime stays cross-platform across Windows desktop and Android:
- **`MW2.PRJ` Virtual Filesystem**: Parses master archive headers, four-character folder tags (`CEL`, `WTB`, `BWD`, `SHP`, `SND`, `XMI`), and local byte offsets with zero-copy slice views for fast mission streaming.
- **`WTB` Geometry & `BWD` World Builders**: Converts legacy fixed-point 16/32-bit coordinate vertices and face normal tables into Godot 4.7 `SurfaceTool` / `ArrayMesh` hierarchies while interpreting `BWD` binary opcodes for terrain tiles, ambient planet skies, mech limb joints, and mission objectives.
- **HoloCinema `.SMK` Player & Input Abstraction**: Indexes all `479` trilogy Smacker cutscenes for clan hall briefings and unifies 6-axis HOTAS joysticks, split throttle quadrants, rudder pedals, XInput controllers, and Android accelerometer/touch cockpit overlays under one action router.
- **Strategic Consolidation**: As recorded in studio portfolio strategy memory `86b7d19f`, reusable simulation kinematics, 8-zone armor grids, and cel-shader pipelines pioneered here live onward inside [MechDestroyer](file:///D:/Projects/MechDestroyer), while original Win95 retail executable patching is documented under `05-hardware-retro` (`mw2-mw4-preservation-suite`).

### Key Local Files
- Consolidated Mecha Simulation Workspace: [MechDestroyer](file:///D:/Projects/MechDestroyer), [PROJECT.md](file:///D:/Projects/MechDestroyer/PROJECT.md)
- Shared Cel & Visor Shader Lineage: [assets/shaders](file:///D:/Projects/MechDestroyer/assets/shaders)
- Studio Deprecation & Consolidation Guardrails: [godot_deprecations_4.0_to_4.7.json](file:///D:/Projects/godot_deprecations_4.0_to_4.7.json)
