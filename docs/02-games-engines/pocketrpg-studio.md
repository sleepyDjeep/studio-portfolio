---
id: "pocketrpg-studio"
title: "PocketRPG Studio: Touch-First Mobile 2D/2.5D RPG Maker"
subtitle: "Android and desktop RPG creation suite in Godot 4.7 packing five genre engines, touch map painting, pixel-art authoring, and portable cartridge sharing."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-28"
date_updated: "2026-09-07"
tags:
  - "godot-4-7"
  - "android"
  - "rpg-maker"
  - "touch-ui"
  - "pixel-art"
  - "2-5d-dungeon"
metrics:
  - label: "Shipped APK Size"
    value: "58.30 MB"
  - label: "Headless Assertions"
    value: "1,183 Passing"
  - label: "Bundled 2D Assets"
    value: "1,380 PNGs"
  - label: "Genre Engines"
    value: "5 Playable Modes"
  - label: "Core Source Code"
    value: "26,459 LOC"
media:
  - src: "assets/media/pocketrpg-studio/studio-hub.png"
    kind: "authentic"
    caption: "PocketRPG Studio v1.0 touch-first launcher hub with 5 RPG genre engines and creation workflows."
  - src: "assets/media/pocketrpg-studio/s24-wireless-live.png"
    kind: "authentic"
    caption: "Live Wireless ADB screen capture from a Samsung Galaxy S24 Ultra running the exported 58.3 MB PocketRPG APK."
  - src: "assets/media/pocketrpg-studio/art-forward-station.png"
    kind: "authentic"
    caption: "Built-in Pixel Studio and Asset Reworking Station with paper-doll character layering."
diagram: ""
tech_stack:
  - "Godot 4.7 (GL Compatibility Mobile)"
  - "GDScript"
  - "Android SDK & Wireless ADB"
  - "Python 3 Batch Asset Remixing"
  - "ComfyUI 2D Asset Workflows"
local_paths:
  - label: "PocketRPG Studio Project Root"
    path: "file:///D:/Projects/RPG Projects"
  - label: "Shipped Android APK Builds"
    path: "file:///D:/Projects/RPG Projects/export"
  - label: "Multi-Genre Pixel Asset Packs"
    path: "file:///D:/Projects/RPG Projects/assets/packs"
run_commands:
  - label: "Launch Studio Hub on Desktop"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\RPG Projects\""
  - label: "Run Master Headless Test Suite"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --headless --path \"D:\\Projects\\RPG Projects\" -s res://tests/master_test_runner.gd"
  - label: "Install APK to Paired Android Phone"
    command: "adb install -r \"D:\\Projects\\RPG Projects\\export\\PocketRPG_Studio.apk\""
memory_ids:
  - "3db3dff9-df84-44a4-9ade-396088c9e62b"
  - "146b142c-0e3c-44eb-894e-d1c9950f2246"
  - "d351a05c-feb7-43a7-8237-e1d8e7974488"
  - "cce5c334-951d-4984-abe9-b2b65ff84e7f"
  - "eeef8977-16ac-4a58-bbdd-502b331b9c23"
  - "587862f1-29fd-45a9-b244-c919211bc589"
  - "16651645-d86c-46c4-920f-d3c21d9032fe"
  - "a3ea4d9c-c6bf-4830-9ee9-2d9e62766773"
  - "246c963a-5e4d-4be4-9517-3fed51dcf181"
  - "04ea7248-8128-40ce-aeb2-a62381fefa0a"
  - "3a74664f-3df1-4af6-8ece-5c6fabc41d9b"
  - "f3d01190-4e9f-417c-a15b-b5397e20dc96"
  - "5966253c-6f7b-469b-b1b6-8a5eb7783f50"
  - "f16d003f-7ec8-42d0-bb4e-e32fafefa247"
  - "78788334-3870-43e0-aef6-537d9ed56050"
  - "c274630b-9dc3-4509-bb99-04de0f0a45ba"
  - "de9e2811-cf61-4463-b8b2-2c16f8057904"
  - "7a142e11-b752-4895-842a-4eeb4dd5244d"
  - "44d57ae8-cb28-4cef-9f76-424aa9c89d1d"
  - "d39db670-7eb6-4e8e-bf47-22590073710a"
  - "45596f55-d930-4775-a31a-89fab747a54d"
  - "96e633df-e3b8-4b05-bbd3-3059c3e086a6"
  - "f6916d13-f4ec-419c-8a98-d7a1ce668077"
  - "433a43b6-9549-444d-80cd-dfe186167c6c"
  - "01b2383d-f770-49e2-8804-f94ab29d4c35"
  - "55f69a19-0d38-41d3-a392-fc0ca6af1924"
  - "1c1d824d-1fee-4325-885f-f0b051dbd75d"
  - "9df6b1a9-9a9b-46f3-b61d-7118408cc54d"
  - "79bc3c71-9bc4-4648-aab9-81c19122ef82"
  - "6c23ad7c-d744-4a77-9f6a-0c64c7a63db6"
  - "c9d010f3-a614-4043-9c61-8ad02f890eb6"
  - "842f5ca0-10b2-4cb3-b039-bfdc3d8bbf6b"
  - "6e00ef51-6619-4a05-ae3a-2fc320a3c8a8"
  - "0de6e1e6-2c3b-4bec-86ce-937b6619b32b"
  - "9493673f-9ea9-4cb2-8845-1c8209b2580d"
  - "79677efb-66ae-449d-a5f9-c57df3ef6922"
  - "5e5f3f09-6532-4727-8c81-5525afb48f52"
  - "aa0a8678-4f51-4f77-9b16-fca5d8c4cce0"
  - "54251ad2-4308-4d17-831e-d780cf636e79"
  - "cdd456ec-0df9-41d5-86c3-6d0528a5fcb3"
  - "5b88b3d4-a5f7-4b55-9c09-197a98942977"
  - "77804840-3bb2-4b5e-9b21-5af4e9501ae9"
  - "d426bd75-8356-44a9-a519-59bee53b94f1"
  - "be12ee1a-ad1c-4a53-a512-e58477b9cc49"
  - "9f821535-d089-43d7-8901-3960657dffc2"
  - "e608ec9c-8420-4a72-867e-d26f6e9a1a9f"
  - "4686a33f-7699-4d23-a2fc-70d1555a222b"
  - "3c87c075-0bd0-4838-b67c-54896df53c38"
  - "43770d53-614d-4fa0-bc0d-29590440414a"
  - "66636a04-6eef-4d9b-9b25-44365baaf4cc"
  - "0891ab98-cbeb-4a18-9986-e831c8f7bc68"
  - "0c6e6590-f44b-4bfe-b7af-25e87853e302"
  - "816faaf6-8fd8-4483-830a-3d5acdafed48"
  - "2a25335c-6e07-4b97-b019-3682d71fb891"
  - "279cf806-4bb1-413f-889f-d440909e9e28"
  - "ed34ac94-e8ec-405e-8cd0-f1b8bfa9c26a"
  - "4f159da4-eded-4a9a-a1e1-664470fc7731"
  - "ae738154-14c8-470d-af8d-16b15fd2f55c"
  - "0589196a-b459-4f78-b989-da028a6d9fae"
  - "898e9bd7-33ab-4b59-bbb6-e4748378dd58"
  - "9fa72e76-263f-479f-8020-2726fba2b5dd"
  - "b5c74b4a-3434-4105-ac3e-a92617e008fe"
  - "22412b37-dca1-4cc7-9ceb-73169552a0f9"
  - "db8350dc-2528-4da7-b6b6-dd5c4b957893"
  - "95900392-8097-44e2-a7c1-8c697db3f8bb"
  - "66c469cc-efed-46c0-ac88-9ada953f621a"
  - "ae3facc1-61cf-46ab-9267-80f6b63bd97f"
  - "f3ff7f19-8486-4c9e-ab3f-1d660290c87c"
  - "da6fecd5-7388-4e12-a4b5-d5e7ae4d1eb4"
  - "336fa2b4-2305-418d-bb0d-98db851c8aa3"
  - "1f84ca96-fd35-48f5-ac94-61adad4f05af"
  - "78bc64f3-deb4-479f-9e60-32f4045a41d1"
  - "b8efbc66-132e-4163-a7e0-11c4c42bf31b"
  - "22280979-6332-4b81-bf55-93e4f7b44121"
  - "c6bb3f87-4a45-4ca0-9b07-b5e6bc7dd43d"
  - "97218b5b-d9ed-4bd9-916a-0e8f18ee5208"
  - "c11f9943-017b-44cd-8fa1-58dd64c29c91"
  - "67ed2762-5472-46e7-a060-cee5ed952a99"
  - "e56068d4-1af8-40a1-b8ef-1d0e5c66e8c8"
  - "0f4ca598-4071-41f0-841b-9d3fe2bb5491"
  - "a8d35921-deb2-4f4b-9216-ee2ee899b3a6"
  - "22487f6a-deb2-4e06-9253-417d8fbb9206"
  - "7bfa8be5-75fd-495c-a20b-cdd8a3c29792"
  - "07da146a-554f-43a4-be5e-0bf5c3a35f88"
  - "41332922-b0b0-40e9-a0d7-0e1eca2f4e06"
  - "75debc92-87e7-4350-b474-72ac2c0de0ac"
  - "b173c7f7-2d3e-4628-aff4-82c52ecee04a"
conversation_ids:
  - "789359de-cb70-4e18-a7b9-9fdeb4303c98"
  - "a70efcf3-bc0a-4740-8b3e-cdfc46075985"
  - "e1b90f33-3d33-48c4-84b1-f4e424e4326f"
  - "ab041875-7fe0-4c89-a009-685325444d58"
---

## What It Is & Why It Matters

*PocketRPG Studio* (`v1.0.0`) brings the full creation loop of *RPG Maker MZ* onto an Android touchscreen without tiny desktop dropdown menus or keyboard shortcuts. Built in Godot 4.7 and tested live over Wireless ADB on a Samsung Galaxy S24 Ultra, it lets creators build, paint, script, score, and playtest five distinct RPG genres right with their thumbs: Classic Turn-Based JRPG, Tactical Grid SRPG / Isometric CRPG, Action RPG, Monster Tamer / Mystery Narrative, and a first-person 2.5D segmented dungeon crawler inspired by *Wizardry* and *Etrian Odyssey*.

Desktop game-creation tools fall apart on phones because mouse-hover inspectors and nested modal dialogs are miserable on a 6.8-inch glass screen. We designed *PocketRPG Studio* from thumb ergonomics upward—combining an 8-way `RadialThumbMenu`, two-finger pinch-and-pan map painting with automatic corner/edge tile matching, snap-together visual event cards, a built-in Paper-Doll pixel-art editor, and six selectable sci-fi UI skins (*Tron/Ares*, *UNSC*, *RobCo*, *LCARS*, *Matrix*, and *Hitchhiker's*).

To ensure creators never start from an empty canvas, we also paired the engine with our local ComfyUI 2D remix factory—bundling `1,380` ready-to-use `.png` spritesheets, 8-direction walk cycles, 48 steampunk monster battlers, portraits, and autotile packs across genres like `clockwork_ruins`, `cyberpunk_neon`, `cosmic_horror`, and `gothic_fantasy`.

## Real Example: How It Works in Practice

- **Input**: On a Samsung Galaxy S24 Ultra running `PocketRPG_Studio.apk`, you tap **Story First** or **Art Forward** on `studio_hub.tscn`, select the *First-Person 2.5D Grid Dungeon Crawler* preset with the `clockwork_ruins` asset pack, drag your thumb across the touch grid to paint a corridor, and drop a Boss Encounter card at the end of the hall.
- **What Happens**: The 4-state touch Map Painter evaluates all eight neighbors around every painted cell using a 47-tile Wang blob bitmask, automatically placing matching stone corners and walls across a 3-layer Undo/Redo stack. Opening the **Built-in Pixel Studio** lets you layer armored Paper-Doll parts onto a character sheet, while the **Chiptune Wave-Synth** generates a custom encounter alarm `.wav` in memory. Snapping 11-type visual Event Sequencer cards (`Dialogue`, `Give Item`, `Camera Shake`, `Start Battle`, `Branch Flag`) onto the tile wires the encounter without typing a line of code. Tapping **Playtest** switches immediately into the live 2.5D perspective dungeon viewport; tapping **Export** compresses maps, custom sprites, synth audio, and event graphs into a single `.prpg` ZIP/Base64 cartridge.
- **Output**: A playable RPG project running at 60 FPS on Android or Windows, packaged into a portable `.prpg` file you can send over Discord or text message and open on any other copy of *PocketRPG Studio*.

## Where It Stands & Next Steps

*PocketRPG Studio* `v1.0.0` is **shipped** with three compiled Android packages on disk inside `D:\Projects\RPG Projects\export\`: `PocketRPG_Studio.apk` (`58.30 MB`), `PocketRPG_Studio_debug.apk` (`55.73 MB`), and `PocketRPG_Studio_release.apk` (`50.76 MB`). Across `3,628` project files (`187.0 MB`), the codebase totals `26,459` lines of handwritten GDScript and Python (`57` `.gd` scripts, `13` `.py` asset tools, and `39` `.tscn` scenes), backed by `1,380` `.png` art assets and `39` `.wav` audio files. Headless verification passes `1,183` automated assertions (`0` failures) via `tests/master_test_runner.gd`—a test harness clean enough that we extracted it into `D:\Projects\_Shared_Library` for reuse across future Godot projects.

Next steps for *PocketRPG Studio*:
- Wire an optional on-device small language model endpoint (benchmarked for Snapdragon 8 Gen 3 phones during our S24 Ultra evaluation) so the *Story First* World Bible DM workflow can draft branching NPC dialogue completely offline on the handset.
- Add a peer-to-peer local Wi-Fi Cartridge Arcade browser inside `studio_hub.tscn` so two phones on the same network can swap `.prpg` worlds with one tap.
- Prepare Google Play Store signing keys and store listing screenshots for public Android release.

## Under the Hood & Local Files

### Ergonomic Mobile Architecture & Five Genre Runtimes
Guided by `87` architectural decisions stored in our Unified Memory Bank (`M0473`–`M0632`), *PocketRPG Studio* targets Godot 4.7's `gl_compatibility` mobile renderer at a landscape `1280x720` logical canvas with dynamic safe-area scaling and touch-emulated desktop parity:
- **Unified Engine Context & Preset Templates**: `engine_context.gd` and `template_presets.gd` decouple project data schemas from genre execution, allowing one `.prpg` data model (`prpg_bundle_manager.gd`) to drive turn-based front-view JRPG battles, tactical SRPG movement ranges, real-time top-down hitboxes, monster-capture party rosters, or segmented 2.5D ray/quad dungeon corridors.
- **Three Entry Workflows**: New users choose between *Art Forward* (reworking and layering sprites first), *Story First* (generating factions, towns, and quests via `ai_assist_service.gd`), or *Advanced* (jumping straight into the multi-layer tile, database, and event-card workbench).
- **Bundled Multi-Genre RTP**: Python batch pipelines (`batch_remix_progress.log` and `assets/comfy_workflows/`) transformed CC0 silhouettes via dual-conditioned IP-Adapter + ControlNet ComfyUI passes and `16/32`-color nearest-neighbor quantization into cohesive multi-genre packs (`clockwork_ruins`, `cosmic_horror`, `cyberpunk_neon`, `eldritch_abyss`, `gothic_fantasy`).

### Key Local Files
- Project Config & Specification: [project.godot](file:///D:/Projects/RPG Projects/project.godot), [export_presets.cfg](file:///D:/Projects/RPG Projects/export_presets.cfg), [ORIGINAL_REQUEST.md](file:///D:/Projects/RPG Projects/ORIGINAL_REQUEST.md)
- Shipped Android Builds: [PocketRPG_Studio.apk](file:///D:/Projects/RPG Projects/export/PocketRPG_Studio.apk), [PocketRPG_Studio_release.apk](file:///D:/Projects/RPG Projects/export/PocketRPG_Studio_release.apk), [PocketRPG_Studio_debug.apk](file:///D:/Projects/RPG Projects/export/PocketRPG_Studio_debug.apk)
- Scenes, Scripts & Asset Libraries: [scenes](file:///D:/Projects/RPG Projects/scenes), [scripts](file:///D:/Projects/RPG Projects/scripts), [packs](file:///D:/Projects/RPG Projects/assets/packs), [comfy_workflows](file:///D:/Projects/RPG Projects/assets/comfy_workflows)
- Automated Test Harness: [tests](file:///D:/Projects/RPG Projects/tests)
