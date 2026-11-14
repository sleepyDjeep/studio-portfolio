---
id: "babylon-adubar-crpg"
title: "Babylon: Final Days of Adubar — Mythic Bronze Age CRPG"
subtitle: "First-person Mesopotamian siege CRPG in Godot 4.7 built on a graph-based world-state ripple engine, one-way doom clock, and literal omen prophecies."
pillar: "02-games-engines"
entry_type: "project"
readiness: "active-build"
visibility: "main"
date_started: "2026-09-12"
date_updated: "2026-09-25"
tags:
  - "godot-4-7"
  - "crpg"
  - "world-state-graph"
  - "bronze-age"
  - "emergent-narrative"
  - "multimesh-streaming"
metrics:
  - label: "Source Code"
    value: "9,535 LOC"
  - label: "City Scale"
    value: "6 Besieged Quarters"
  - label: "Architecture"
    value: "5-Layer Downward Spine"
  - label: "Smoke Gate Scenes"
    value: "5 Verified Scenes"
  - label: "Design & Gate Docs"
    value: "24 Markdown Specs"
media:
  - src: "assets/media/babylon-adubar-crpg/adubar-district-map.png"
    kind: "authentic"
    caption: "Architectural district map of Bronze Age Adubar spanning all 6 siege-locked city quarters."
  - src: "assets/media/babylon-adubar-crpg/city-reference.png"
    kind: "authentic"
    caption: "Visual reference and world-state consequence sheet for Babylon: Final Days of Adubar."
diagram: ""
tech_stack:
  - "Godot 4.7 (Vulkan Forward+)"
  - "GDScript (5-Layer Strict Architecture)"
  - "MultiMeshInstance3D City Streamer"
  - "Graph Ripple Simulation Spine"
local_paths:
  - label: "Babylon Project Root"
    path: "file:///D:/Projects/Babylon"
  - label: "Session Handoff & Gate Ledger"
    path: "file:///D:/Projects/Babylon/CONTINUE.md"
  - label: "Adubar Architectural Map"
    path: "file:///D:/Projects/Babylon/babylon/reference/babylon_district_map.png"
run_commands:
  - label: "Launch Streamed 3D City Walk"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\Babylon\" res://content/city.tscn"
  - label: "Launch District Gallery & Smoke Scenes"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\Babylon\" res://content/dev/district_gallery.tscn"
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

*Babylon: Final Days of Adubar* is a first-person mythic Bronze Age CRPG set inside the besieged Mesopotamian city-state of Adubar during the final six days before its outer walls fall. The outcome is fixed—Adubar will break—so the game is about *how* you meet the end, who survives it, and which seam gives way first. Built in Godot 4.7 around three uncompromising design pillars (**Freedom**, **Consequence**, and **Strangeness**), every charged encounter (*Situation*) offers at least three structurally distinct ways forward, combat is never privileged above guile or ritual, saves advance alongside an irreversible siege clock so consequences cannot be save-scummed away, and Mesopotamian gods like **Ea** act as live agents inside the simulation.

Most narrative RPGs hardcode branching quests into brittle spaghetti trees that break the moment a player walks into a neighboring district out of order. We built *Babylon* on a strict five-layer downward-dependency architecture where the entire reusable CRPG simulation (`systems/`) knows zero Adubar character or place names: you can delete the `content/` folder completely and the underlying world-state graph, ripple propagator, siege clock, omen engine, and quarter-fall evaluator still compile cleanly—so clean that `world_state.gd`, `fall_system.gd`, and `demo_shell.gd` were extracted straight into `D:\Projects\_Shared_Library`.

## Real Example: How It Works in Practice

- **Input**: Walking down the cobalt-glazed Processional Way past the Ishtar Gate in `res://content/city.tscn`, you confront **The Priest's Silence** or **The Smugglers' Tunnel** in Quarter 1, choose to invoke the god **Ea** over the silent priest's head rather than forcing the palace guards, then cross into Quarter 2 (*The Cistern Dole*) and press `J` to inspect your Omen Ledger.
- **What Happens**: Your chosen approach mutates node fields inside `systems/world_state/` ("THE SPINE"), propagating typed edge ripples across faction standing (`palace.control`, `hungry_quarter.unrest`, `priest.authority`) and advancing the one-way `siege_clock/`. Because you invoked Ea directly, `omen_system.resolve()` flips the declared prophecy `silence_of_the_god` (*"the god's own voice will fall silent"*) from pending (`◇`) to **TWIST** (`◆`)—the god spoke, yet his mortal priest's voice still fell silent—triggering its own secondary ripple and re-judging `divine_favor/`. In Quarter 2, the Washerwoman NPC reads your Quarter 1 granary/priest state and gates which appeal options even exist at the Cistern. Each new day applies an inexorable siege escalation ripple (`unrest +0.08`, `palace.control -0.04`, `priest.authority -0.03`) until `FallSystem` (`systems/siege/fall_system.gd`) latches the first quarter to cross its deterministic ruin threshold and raises the narrative recap card on `DemoShell`.
- **Output**: A continuous, save-persistent (`v2` snapshot) first-person run across streamed Mesopotamian city quarters where every choice visibly reshapes NPC reactions, prophecy states, and which district collapses when the siege breaks.

## Where It Stands & Next Steps

*Babylon* is an **active-build** vertical slice at `D:\Projects\Babylon` (`320` files, `265.2 MB`, `9,535` LOC across `65` GDScript modules, `1` Python utility, `1` HTML visual reference sheet, `33` `.tscn` scenes, `51` PBR mudbrick and glazed-cobalt textures, and `24` design/gate Markdown specs). Phase `D-2` passed full live Godot 4.7 editor walk verification in Session 12—confirming uninterrupted cross-quarter `MultiMeshInstance3D` streaming, eliminated Ishtar Gate / Processional Way coplanar z-fighting (`y = -0.025` 2.5 cm datum offset), all four open Situations, and live `FULFIL / AVERT / TWIST` omen resolution. Phase `D-3` (*The Small Fall*, `DemoShell` title/ending loop, and mid-run quit-and-resume save hardening) is authored `100%` static-clean against our Godot 4.7 deprecation scanner alongside five smoke scenes (`worldstate_smoke.tscn`, `systems_smoke.tscn`, `content_smoke.tscn`, `fall_smoke.tscn`, and `district_gallery.tscn`).

Next steps to cross the public Demo Gate:
- Execute the 6-part live editor balance walk in `GATE_D3_WALK.md` to verify all three distinct quarter-fall endings (*Hungry Quarter* boil-over, *Royal District* grip collapse, and *Sacred Precinct* silence) plus mid-run `Continue your siege` teleport restoration.
- Swap greybox/procedural block props at `_model()` call sites for bespoke Mesopotamian ceramic, reed, and bronze `.glb` assets.
- Tune movement auto-step heights along InnerWalls rampart seams and lock skybox asset licensing ahead of standalone demo export.

## Under the Hood & Local Files

### Strict Five-Layer Downward Architecture
Documented in [README.md](file:///D:/Projects/Babylon/README.md), [concept.md](file:///D:/Projects/Babylon/content/design/concept.md), and [CONTINUE.md](file:///D:/Projects/Babylon/CONTINUE.md), dependencies point strictly downward so lower layers never reference upper layers:
- **Layer 0 (`addons/`) & Autoloads (`project.godot`)**: Registers `EventBus`, deterministic `RNG`, `GameManager`, and v2-compatible `SaveService`.
- **Layer 2 (`systems/`) — Reusable CRPG Engine**: Houses nine custom `Resource` schemas (`systems/data/`), the graph-and-ripple spine (`systems/world_state/`), `siege_clock/`, gated-approach `situation/`, graded and contested deterministic `stat_check/`, `faction/`, `divine_favor/`, three-way `omen/` prophecy resolution, and `systems/siege/fall_system.gd` (`FallSystem`).
- **Layer 3 (`ui/`) — Read-Only Views**: Consequence HUD feed, Omen Ledger (`J`), interactive Situation approach panel, and portable `ui/demo_shell.gd` (`DemoShell`, layer 200).
- **Layer 4 (`content/`) — Adubar Under Siege**: Populates the six quarters, three core NPCs, the god Ea, four intertwined Situations, four prophecies, and `city_streamer.gd` / `processional_way.gd` `MultiMeshInstance3D` architectural streaming.

### Key Local Files
- Root Config & Handoff Logs: [project.godot](file:///D:/Projects/Babylon/project.godot), [README.md](file:///D:/Projects/Babylon/README.md), [CONTINUE.md](file:///D:/Projects/Babylon/CONTINUE.md), [GATE_D2_WALK.md](file:///D:/Projects/Babylon/GATE_D2_WALK.md), [GATE_D3_WALK.md](file:///D:/Projects/Babylon/GATE_D3_WALK.md)
- Design & Reference Sheets: [concept.md](file:///D:/Projects/Babylon/content/design/concept.md), [babylon_district_map.png](file:///D:/Projects/Babylon/babylon/reference/babylon_district_map.png), [index.html](file:///D:/Projects/Babylon/babylon/reference/index.html)
- Simulation Spine & Content Directories: [systems](file:///D:/Projects/Babylon/systems), [ui](file:///D:/Projects/Babylon/ui), [content](file:///D:/Projects/Babylon/content)
