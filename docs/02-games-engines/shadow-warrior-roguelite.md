---
id: "shadow-warrior-roguelite"
title: "Shadow Warrior Roguelite: Procedural Cyberpunk Arena FPS"
subtitle: "Fast-paced Godot 4.7 katana and boomer-shooter roguelite featuring 10 procedural 3D weapons, elemental cel-shaded VFX, and zero-WAV real-time synthwave audio."
pillar: "02-games-engines"
entry_type: "project"
readiness: "active-build"
visibility: "main"
date_started: "2026-09-10"
date_updated: "2026-09-20"
tags:
  - "godot-4-7"
  - "roguelite-fps"
  - "procedural-3d"
  - "synthwave-dsp"
  - "cel-shading"
  - "boomer-shooter"
metrics:
  - label: "Total Disk Size"
    value: "1.61 MB"
  - label: "Source Code"
    value: "15,939 LOC"
  - label: "Procedural Weapons"
    value: "10 3D GLBs"
  - label: "Automated Tests"
    value: "26 Test Files"
  - label: "Pre-Recorded WAVs"
    value: "0 (100% Live DSP)"
media:
  - src: "assets/media/shadow-warrior-roguelite/gameplay-capture.png"
    kind: "authentic"
    caption: "Live Godot 4.7 Forward+ capture of Shadow Warrior Roguelite featuring procedural 3D weaponry and cyberpunk arena lighting."
diagram: ""
tech_stack:
  - "Godot 4.7 (Vulkan Forward+)"
  - "GDScript"
  - "Godot AudioStreamGenerator DSP"
  - "Godot Shader Language (GLSL)"
  - "Python 3 Procedural GLB Generators"
local_paths:
  - label: "ShadowWarriorRoguelite Root"
    path: "file:///D:/Projects/ShadowWarriorRoguelite"
  - label: "Architecture & Feature Matrix"
    path: "file:///D:/Projects/ShadowWarriorRoguelite/PROJECT.md"
  - label: "End-to-End Test Runner"
    path: "file:///D:/Projects/ShadowWarriorRoguelite/tests/run_e2e_tests.py"
run_commands:
  - label: "Launch Game via PowerShell Helper"
    command: "powershell -ExecutionPolicy Bypass -File \"D:\\Projects\\ShadowWarriorRoguelite\\run_game.ps1\""
  - label: "Open Project in Godot 4.7"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\ShadowWarriorRoguelite\""
  - label: "Run End-to-End Test Suite"
    command: "python \"D:\\Projects\\ShadowWarriorRoguelite\\tests\\run_e2e_tests.py\""
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

*Shadow Warrior Roguelite* is a high-velocity first-person cyberpunk katana and arena shooter built in Godot 4.7 Forward+ that packs an entire 3D roguelite—10 weapons, enemy squads, multi-phase bosses, a safe-zone upgrade hub, anime cel-shading, elemental GPU particles, and a reactive synthwave soundtrack—into `1.61 MB` on disk. Between 10-floor arena runs, you regroup in a neon sanctuary with weaponsmith `Grizz` and operator `Vex`, spend harvested souls at the **CyberForge Upgrade Shrine** on double-jumps or elemental blade/ammo infusions (`fire`, `acid`, `cryo`, `shock`), and ride an elevator into procedurally assembled combat rooms.

Most 3D shooters balloon to gigabytes before gameplay feel is even locked in because teams import bloated third-party weapon meshes and static `.wav` libraries early. We built *Shadow Warrior Roguelite* to prove a procedural-first alternative: Python standard-library scripts generate all `17` `.glb` 3D weapon, enemy, boss, and modular room meshes mathematically, while Godot's `AudioStreamGenerator` synthesizes every synthwave bassline, drum stem, katana whoosh, and plasma blast in real time at zero bytes of audio disk overhead.

Several core shaders from this build (`AnimeCelShader.gdshader` and `HitFlash.gdshader`) proved clean enough that we extracted them directly into `D:\Projects\_Shared_Library` as studio-wide Godot 4.7 visual building blocks.

## Real Example: How It Works in Practice

- **Input**: You launch `run_game.ps1`, talk to `Grizz` in the Hub, spend `120` souls at `CyberForgeShrine.gd` to infuse your loadout with `cryo` frost crystals plus `150` souls for `double_jump`, step into `Elevator.gd`, and slide (`C`) + dash (`Shift`) into Floor 1 armed with the high-frequency **Katana** and **Shuriken Launcher**.
- **What Happens**: `GameManager.gd` transitions its 8-state finite state machine from `HUB` through `ELEVATOR_TRANSITION` to `COMBAT_LEVEL`, prompting `LevelGenerator.gd` to stitch modular floor, wall, doorway, and pillar `.glb` tiles and lock room doors behind active enemy waves (`PipeMutant` melee swarmers, `PlasmaGrunt` troopers, and laser-sighted `SniperCyborg` marksmen). As combat intensity rises, `DynamicMusicManager.gd` crossfades real-time `AudioStreamGenerator` synthwave layers from ambient hub pads into driving arpeggios, while `SynthesizedSFX.gd` pitch-bends procedural sword swings and hit thumps. Slashing enemies triggers `HitFlash.gdshader` white/red mesh flashes, spawns `GPUParticles3D` cryo frost shards, updates `DiegeticHUD.tscn` combo/soul counters, and evaluates special run endings (including a zero-hit, zero-upgrade base-katana mastery check in `GameManager.check_victory_conditions()`).
- **Output**: A crisp 1080p (`2x MSAA`) 3D cyberpunk movement shooter running directly from `99` compact scripts and `17` generated `.glb` assets with zero external asset packs.

## Where It Stands & Next Steps

*Shadow Warrior Roguelite* is in **active-build** integration at `D:\Projects\ShadowWarriorRoguelite` (`268` total files, `1.61 MB`, `15,939` LOC across `84` GDScript files, `10` Python procedural mesh generators, `4` `.gdshader` shaders, `1` PowerShell launcher, and `33` `.tscn` scenes). Milestones `M3` (complete UI & menu suite) and `M4` (dynamic `AudioStreamGenerator` synthwave and procedural SFX engine) are marked `DONE`, all `17` procedural `.glb` meshes and `10` weapon controllers are generated on disk, and `26` automated unit, shader/VFX stress, and E2E test scripts (`tests/run_e2e_tests.py`, `test_m2_challenger5_vfx_stress.gd`) verify subsystem contracts while Milestone `M5` core-loop polish continues.

Next steps to complete the vertical slice:
- Finish Milestone `M5` arena room-lock wave pacing and elevator floor-to-floor progression across all `10` run depths (`MAX_LEVELS = 10`).
- Run a high-poly bevel and Cycles curvature-bake pass on the 10 Python-generated weapon `.glb` viewmodels (`generate_weapons.py`) so first-person silhouettes read sharply under `AnimeCelShader.gdshader`.
- Export a tiny (`<40 MB`) standalone Windows demo binary showcasing the sub-2-megabyte procedural asset footprint.

## Under the Hood & Local Files

### Ten-Autoload Architecture, Procedural GLBs & Live DSP Audio
- **10 Autoload Singletons (`project.godot`)**: `AudioEngine`, `DynamicMusicManager`, `HubManager`, `WeaponXP`, `EnemyAbilityManager`, `EnvironmentManager`, `GameManager`, `DialogueManager`, `QuestManager`, and `InputManager` cleanly separate RPG meta-progression from per-frame arena combat.
- **Zero-Dependency Python 3D Mesh Factory**: Four standalone Python generators—[generate_weapons.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_weapons.py) (Katana, Plasma Rifle, Shuriken Launcher, Neon Plasma Shotgun, Railgun Sniper, Smart Pistol, Gravity Hammer, Arc Emitter, Sludge Thrower, Nano Swarm), [generate_enemies.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_enemies.py), [generate_zany_bosses.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_zany_bosses.py), and [generate_level_tiles.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_level_tiles.py)—emit valid binary glTF 2.0 `.glb` files directly into `weapons/`, `enemies/`, and `level/` without requiring Blender to be open.
- **Real-Time `AudioStreamGenerator` Synthwave & SFX**: `audio/AudioEngine.gd`, `DynamicMusicManager.gd`, and `SynthesizedSFX.gd` synthesize oscillators, noise bursts, envelopes, and filter sweeps into audio ring buffers on the fly, shifting musical intensity dynamically via `DynamicMusicManager.set_intensity(intensity)`.

### Key Local Files
- Engine & Architecture Definitions: [project.godot](file:///D:/Projects/ShadowWarriorRoguelite/project.godot), [PROJECT.md](file:///D:/Projects/ShadowWarriorRoguelite/PROJECT.md), [ORIGINAL_REQUEST.md](file:///D:/Projects/ShadowWarriorRoguelite/ORIGINAL_REQUEST.md), [TEST_INFRA.md](file:///D:/Projects/ShadowWarriorRoguelite/TEST_INFRA.md)
- Entry Scene & Launcher: [Main.tscn](file:///D:/Projects/ShadowWarriorRoguelite/Main.tscn), [Main.gd](file:///D:/Projects/ShadowWarriorRoguelite/Main.gd), [run_game.ps1](file:///D:/Projects/ShadowWarriorRoguelite/run_game.ps1)
- Procedural 3D Generators: [generate_weapons.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_weapons.py), [generate_enemies.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_enemies.py), [generate_level_tiles.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_level_tiles.py), [generate_zany_bosses.py](file:///D:/Projects/ShadowWarriorRoguelite/generate_zany_bosses.py)
- Subsystems & Shaders: [rpg/GameManager.gd](file:///D:/Projects/ShadowWarriorRoguelite/rpg/GameManager.gd), [audio](file:///D:/Projects/ShadowWarriorRoguelite/audio), [shaders](file:///D:/Projects/ShadowWarriorRoguelite/shaders), [weapons](file:///D:/Projects/ShadowWarriorRoguelite/weapons), [ui](file:///D:/Projects/ShadowWarriorRoguelite/ui)
