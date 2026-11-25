---
id: "shadow-warrior-roguelite"
title: "NEON GRAVE: Ten-Floor Cyberpunk Roguelite (Working Title)"
subtitle: "Godot 4.7 first-person roguelite in pre-alpha: a ten-floor descent with a boss behind every door, built on procedurally generated GLBs, live-synthesized synthwave, and a 32-unit mission ledger that gates every step."
pillar: "02-games-engines"
entry_type: "project"
readiness: "active-build"
visibility: "main"
date_started: "2026-09-10"
date_updated: "2026-11-25"
tags:
  - "godot-4-7"
  - "roguelite-fps"
  - "procedural-3d"
  - "synthwave-dsp"
  - "cel-shading"
  - "mission-ledger"
metrics:
  - label: "Gate Baseline"
    value: "588 tests, 583 passing"
  - label: "Test Suites"
    value: "14 headless suites"
  - label: "Planned Boss Fights"
    value: "10 (4 bespoke)"
  - label: "Mission Ledger"
    value: "6 of 32 units (M0 complete)"
  - label: "Disk Footprint"
    value: "1.61 MB, zero audio WAVs"
media:
  - src: "assets/media/shadow-warrior-roguelite/gameplay-capture.png"
    kind: "authentic"
    caption: "Prototype capture from the September 2026 build: procedural weapon viewmodel, cyberpunk arena lighting and the cel-shaded look in Godot 4.7 Forward+. It predates the NEON GRAVE plan, so it shows the existing prototype rather than a finished 1.0 run."
diagram: ""
tech_stack:
  - "Godot 4.7 (Vulkan Forward+)"
  - "GDScript"
  - "Godot AudioStreamGenerator DSP"
  - "Godot Shader Language (GLSL)"
  - "Python 3 procedural GLB generators"
  - "PowerShell mission control and gate harness"
local_paths:
  - label: "Project Root"
    path: "file:///D:/Projects/ShadowWarriorRoguelite"
  - label: "1.0 Roadmap and Unit Ledger"
    path: "file:///D:/Projects/ShadowWarriorRoguelite/docs/mission/ROADMAP.md"
  - label: "Verified Current State"
    path: "file:///D:/Projects/ShadowWarriorRoguelite/docs/mission/FACTS.md"
run_commands:
  - label: "Open Project in Godot 4.7"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\ShadowWarriorRoguelite\""
  - label: "Fast Gate (boot probe, harness selftest, autopilot)"
    command: "powershell -NoProfile -ExecutionPolicy Bypass -File \"D:\\Projects\\ShadowWarriorRoguelite\\tools\\gate.ps1\" -Fast"
  - label: "Mission Status"
    command: "powershell -NoProfile -ExecutionPolicy Bypass -File \"D:\\Projects\\ShadowWarriorRoguelite\\tools\\mission.ps1\" status"
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

*NEON GRAVE* is the working title for a first-person roguelite in Godot 4.7 built on the *Shadow Warrior Roguelite* prototype in `D:\Projects\ShadowWarriorRoguelite`. The destination is one authored two-hour descent through ten floors of the Sprawl, a boss behind every door, and a hub with a Forge where each death converts into the next attempt: banked souls and weapon XP survive a death, carried souls do not, so every elevator ride is a wager. The aesthetic target is 90s OVA cel animation over a live-synthesized synthwave score, with zero audio WAV files on disk.

The project matters to the studio as a test of something harder than a demo: finishing a commercial 1.0 from a prototype that had drifted. The prototype already carries ten procedural weapons, seventeen generated GLB meshes, a hub with two NPCs and an elevator, and a shader set that other studio projects reuse. What it did not have was a trustworthy account of itself, so the first milestone rebuilt the foundation: a mission ledger of 32 units, a headless gate with a real baseline, a boot chain that reaches the main menu, and an autopilot that proves menu to hub.

## Real Example: How It Works in Practice

- **Input**: Run `godot --headless --path . -s tools/boot_probe.gd` in the project root, or let `tools/gate.ps1 -Fast` run it as step two. Both ask the same question: does the project's configured main scene reach the main menu on its own?
- **What Happens**: Godot loads `Boot.tscn`, the boot screen types its six-line sequence at 0.3 s per line, holds, fades, and calls `change_scene_to_file("res://ui/MainMenu.tscn")`. The transition result is checked: if the menu cannot load, the boot prints the error and exits 1 instead of sitting on a finished boot screen. The probe watches the current scene until `MainMenu` appears or 15 s pass, and the fast gate then runs ten harness tests plus an autopilot that presses Play and asserts the hub's player and generated `HubEnvironment`.
- **Output**: `[BOOT PROBE] PASS reached MainMenu in about 3.7 s`, exit 0, no `SCRIPT ERROR`; the gate prints `BOOT PROBE PASS`, `AUTOPILOT PASS` and an assertion line of 10 passed, 0 failed. A deliberately renamed `MainMenu.tscn` turns the same run into `[BOOT] cannot load ... (error 19)` and gate exit 2.

## Where It Stands & Next Steps

Pre-alpha, and the ledger says so plainly. Milestone M0 is complete at 6 of 32 units: repository truth, the gate harness, the boot chain, the documentation canon, mission control scripts, and the autopilot. No M1-or-later unit has started. The prototype still runs on a decorative state machine, has no victory path, no elevator save, and no boss implemented to the ten-fight ladder in the design docs; four known test failures and a nine-node leak are recorded and deferred rather than hidden. The measured baseline is 588 tests across 14 suites with 583 passing, one error, and no hangs.

Next is the M1 spine, one unit at a time with the ledger as the authority: make `GameManager.go_to(state)` the only scene transition, add a `RunState` that round-trips through a dictionary, turn the hub into a real scene, wire the elevator to a seeded floor builder, then make death bank souls and return to the hub. M1.7 closes when one headless process walks Boot, Menu, Hub, Elevator, Floor, Death and back to Hub with a printed route.

## Under the Hood & Local Files

- **Project root**: [D:\Projects\ShadowWarriorRoguelite](file:///D:/Projects/ShadowWarriorRoguelite), Godot 4.7.2, GDScript, ten autoloads, 17 procedurally generated `.glb` assets and four `.gdshader` files.
- **Mission control**: [ROADMAP.md](file:///D:/Projects/ShadowWarriorRoguelite/docs/mission/ROADMAP.md) holds the 32-unit ledger and the ten-floor design; [FACTS.md](file:///D:/Projects/ShadowWarriorRoguelite/docs/mission/FACTS.md) holds the verified present with numbered bugs; [STATE.md](file:///D:/Projects/ShadowWarriorRoguelite/docs/mission/STATE.md) carries the cursor and is rewritten by [mission.ps1](file:///D:/Projects/ShadowWarriorRoguelite/tools/mission.ps1) on every `done`.
- **Gate harness**: [gate.ps1](file:///D:/Projects/ShadowWarriorRoguelite/tools/gate.ps1) runs a boot smoke, the boot probe, and either the harness selftest with the autopilot (`-Fast`) or all 14 suites in separate processes (`-Full`); it returns 0 for a pass, 1 for failed tests, 2 for script errors, hangs or a failed boot probe.
- **Boot and autopilot probes**: [boot_probe.gd](file:///D:/Projects/ShadowWarriorRoguelite/tools/boot_probe.gd) and [autopilot.gd](file:///D:/Projects/ShadowWarriorRoguelite/tests/autopilot.gd). Audio stays synthesized by [AudioEngine.gd](file:///D:/Projects/ShadowWarriorRoguelite/audio/AudioEngine.gd) and [SynthesizedSFX.gd](file:///D:/Projects/ShadowWarriorRoguelite/audio/SynthesizedSFX.gd), which is why the disk footprint stays at 1.61 MB.
