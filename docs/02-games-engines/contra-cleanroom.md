---
id: "contra-cleanroom"
title: "Operation Vulture: 1988 NES Contra Clean-Room Remake"
subtitle: "Zero-ROM-asset Godot 4.7 recreation of the 8-stage 1988 NES run-and-gun campaign with procedural pixel art, live 2A03 APU chiptune synthesis, and 2P co-op."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-11-02"
date_updated: "2026-11-02"
tags:
  - "godot-4-7"
  - "clean-room-remake"
  - "nes-2a03-apu"
  - "crt-shader"
  - "local-coop"
  - "run-and-gun"
metrics:
  - label: "Source Code"
    value: "6,597 LOC"
  - label: "Headless Assertions"
    value: "154 / 154 Passing"
  - label: "Campaign Length"
    value: "8 Full Stages"
  - label: "Internal Viewport"
    value: "480x270 @ 60 Hz"
  - label: "Ripped ROM Bytes"
    value: "0 Bytes"
media:
  - src: "assets/media/contra-cleanroom/operation-vulture.png"
    kind: "authentic"
    caption: "Live Godot 4.7 capture of Operation Vulture (Contra Clean-Room) running at 480x270 internal resolution with aperture-grille CRT shader."
diagram: ""
tech_stack:
  - "Godot 4.7"
  - "GDScript (22 Modules)"
  - "Real-Time 2A03 NES APU Synth"
  - "Godot Shader Language (CRT Post-FX)"
local_paths:
  - label: "Contra Clean-Room Project Root"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom"
  - label: "Campaign & Controls Guide"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/README.md"
  - label: "2A03 NES Chiptune Synthesizer"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/scripts/autoloads/audio_manager.gd"
run_commands:
  - label: "Quick Launch Game"
    command: "\"C:\\Users\\ogreb\\.gemini\\antigravity\\scratch\\contra_cleanroom\\run_game.bat\""
  - label: "Run 154-Assertion Headless Verification"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --headless --path \"C:\\Users\\ogreb\\.gemini\\antigravity\\scratch\\contra_cleanroom\" res://tests/verify_suite.tscn"
memory_ids:
  - "d488a190-a2eb-4f07-89b9-02ecb404d121"
conversation_ids: []
---

## What It Is & Why It Matters

*Operation Vulture* is a 100% clean-room Godot 4.7 recreation of the 1988 NES 8-stage run-and-gun campaign—engineered with zero extracted ROM graphics, zero sampled audio rips, and modern high-refresh display responsiveness. Every commando animation frame, exploding suspension bridge, behind-the-back 3D fortress corridor, and alien boss is constructed procedurally in GDScript (`pixel_art_bank.gd`), while a custom software Ricoh 2A03 audio synthesizer (`audio_manager.gd`) generates two pulse channels, a triangle bassline, and a linear-feedback-shift-register noise drum track live on the CPU.

Classic 8-bit action games feel sluggish or blurry when emulated poorly on modern 165 Hz widescreen monitors, yet distributing modified ROM hacks carries obvious copyright traps. Building *Operation Vulture* from mathematical first principles gave us a legally clean, self-contained executable template that pairs `60 Hz` deterministic arcade hitboxes with `165 Hz` visual physics interpolation, instant `F4` switching between `16:9` widescreen and `4:3` arcade cabinet framing, and a toggleable `F3` 270p aperture-grille CRT shader.

## Real Example: How It Works in Practice

- **Input**: Two players plug in XInput gamepads (or share a split keyboard), launch `run_game.bat`, enter `Up, Up, Down, Down, Left, Right, Left, Right, B, A` on the Title Screen to unlock the classic 30-lives reserve, and drop into **Stage 01 — Jungle Garrison** followed by **Stage 02 — Fortress Base 1**.
- **What Happens**: Player controllers evaluate crisp 8-way aim vectors, somersault jump arcs, river-submerge ducking, and `Down + Jump` one-way ledge drops inside a pixel-snapped `480x270` internal viewport, shooting down flying power-up capsules to equip the 5-way Spread Gun (`S`), Rapid Laser (`L`), Fireball (`F`), or Machine Gun (`M`). Crossing the jungle suspension bridges triggers sequential timed chain-detonations ahead of the **Defense Wall Mk-I** boss; clearing Stage 01 transitions directly into `pseudo3d_stage.gd`, switching camera math to a behind-the-back depth corridor with electric laser barriers, rolling floor mines, and the **Cybernetic Terminal Eye** boss. Throughout the run, `crt_post.gdshader` applies scanline beam bloom and phosphor mask subpixels while `audio_manager.gd` sequences live 2A03 square-wave leads and DPCM/noise percussion bursts. If Player 2 runs out of reserves mid-fight, pressing `Fire` borrows a spare stock from Player 1 on the fly.
- **Output**: A complete, playable 8-stage co-op arcade campaign—culminating in the **Emperor Xenomorph Heart** lair, Island Helicopter Escape sequence, and Loop 2+ Hard Corps difficulty—verified by `154` passing headless assertions.

## Where It Stands & Next Steps

*Operation Vulture* is **shipped** and playable on disk at `C:\Users\ogreb\.gemini\antigravity\scratch\contra_cleanroom` (`6,597` lines of code across `22` GDScript modules, `2` `.gdshader` shaders, and `1` batch launcher). Every stage (`Jungle Garrison`, `Fortress Base 1`, `Cascading Waterfall`, `Fortress Base 2`, `Frozen Tundra`, `Thermal Reactor`, `Fortress Hangar`, and `Xenomorph Hive`), boss state machine, weapon pickup, co-op life-steal mechanic, and audio channel passes `154 / 154` automated checks in `res://tests/verify_suite.tscn`.

Next steps to expand or integrate:
- Bundle *Operation Vulture* directly into our living-room `E:\RetroBat` console appliance under custom Windows/Godot Ports so 2-player couch co-op launches straight from a gamepad.
- Add local JSON replay recording (leveraging the deterministic `60 Hz` input tick) so 1-credit speedruns play back as attract-mode demos on the title screen.
- Export a single-file WebAssembly HTML5 build for instant browser playtesting.

## Under the Hood & Local Files

### Procedural Pixel Bank, Pseudo-3D Corridors & 2A03 APU Synthesis
Recorded under Unified Memory Bank entry `M0994` and session `C126`, the project is organized into clean `autoloads/`, `data/`, `entities/`, `stages/`, and `ui/` packages:
- **Procedural Sprite & Tile Synthesis (`scripts/data/`)**: Generates indexed retro palettes and multi-frame character, turret, boss, and environment `ImageTexture` sheets at startup so zero external `.png` sprite rips are stored on disk.
- **Hybrid 2D + Pseudo-3D Stage Architecture (`scripts/stages/`)**: Combines horizontal scrolling stages, upward-ratcheting vertical cliff climbs (Stage 03 *Cascading Waterfall* with **Gromaides Alien Colossus** segmented tentacles), timed hydraulic ceiling crushers (Stage 07), and perspective-projected z-depth corridors (`pseudo3d_stage.gd` for Stages 02 and 04).
- **Real-Time 2A03 NES APU (`scripts/autoloads/audio_manager.gd`)**: Synthesizes variable duty-cycle (`12.5%`, `25%`, `50%`, `75%`) pulse oscillators, quantized 4-bit triangle bass waves, and metallic/periodic LFSR noise envelopes directly into Godot's audio stream buffer.
- **CRT & Hit-Flash Shaders (`assets/shaders/`)**: [crt_post.gdshader](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/assets/shaders/crt_post.gdshader) models subtle barrel curvature, 270p scanlines, and RGB aperture-grille triads, paired with [hit_flash.gdshader](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/assets/shaders/hit_flash.gdshader) for instant boss damage feedback.

### Key Local Files
- Project Config, Guide & Quick Launcher: [project.godot](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/project.godot), [README.md](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/README.md), [run_game.bat](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/run_game.bat)
- Main Scene & Audio Bus: [main.tscn](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/scenes/main.tscn), [default_bus_layout.tres](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/default_bus_layout.tres)
- Scripts & Shaders: [audio_manager.gd](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/scripts/autoloads/audio_manager.gd), [scripts](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/scripts), [crt_post.gdshader](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/assets/shaders/crt_post.gdshader), [hit_flash.gdshader](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/assets/shaders/hit_flash.gdshader)
- Automated Verification Suite: [tests](file:///C:/Users/ogreb/.gemini/antigravity/scratch/contra_cleanroom/tests)
