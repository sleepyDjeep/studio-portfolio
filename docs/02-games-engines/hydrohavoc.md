---
id: "hydrohavoc"
title: "HydroHavoc: Streaming Puzzle Game with Shallow-Water Physics"
subtitle: "Godot 4.7.2 successor to Wetrix where chat buys polyomino hazards, 3D props float on a 32x32 shallow-water field, and one build renders both 16:9 and 9:16 broadcast layouts."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-11-14"
date_updated: "2026-11-14"
tags:
  - "godot-4-7"
  - "streaming-game"
  - "fluid-simulation"
  - "webassembly"
  - "twitch-bits"
  - "tiktok-live"
  - "buoyancy-physics"
metrics:
  - label: "Source Code"
    value: "1,640 LOC"
  - label: "GDScript Modules"
    value: "9 Files"
  - label: "Fluid Grid"
    value: "32 x 32 SWE"
  - label: "Playable Builds"
    value: "Windows + Web"
  - label: "First Release"
    value: "2026-11-14"
media:
  - src: "assets/media/hydrohavoc/gameplay-landscape.png"
    kind: "authentic"
    caption: "Godot 4.7.2 capture of HydroHavoc in 16:9 mode: flooded heightfield terrain, floating gift crate and rubber ducks, and a polyomino piece queued over the lake."
  - src: "assets/media/hydrohavoc/gameplay-props-slice.png"
    kind: "authentic"
    caption: "Floating-prop physics slice: single-point buoyancy clamping props to the moving water surface while stream alerts and the VIP gifter throne run on the HUD."
  - src: "assets/media/hydrohavoc/gameplay-vertical-9x16.png"
    kind: "authentic"
    caption: "Native 9:16 portrait capture (720x1280) of the TikTok Live layout, with the arena stacked above the compact score and alert rail."
diagram: "assets/diagrams/hydrohavoc.svg"
tech_stack:
  - "Godot 4.7.2 (Forward+ / Mobile / Web)"
  - "Typed GDScript"
  - "Godot Shader Language (GLSL)"
  - "HTML5 + WebAssembly export"
  - "Procedural GLB props"
local_paths:
  - label: "HydroHavoc Project Root"
    path: "file:///D:/Projects/HydroHavoc"
  - label: "Shallow-Water Simulation"
    path: "file:///D:/Projects/HydroHavoc/scripts/core/fluid_sim.gd"
  - label: "Floating Prop Manager"
    path: "file:///D:/Projects/HydroHavoc/scripts/props/prop_manager.gd"
  - label: "Windows Release Build"
    path: "file:///D:/Projects/HydroHavoc/build/windows/HydroHavoc.exe"
  - label: "Browser Demo"
    path: "file:///D:/Projects/HydroHavoc/docs/index.html"
run_commands:
  - label: "Launch HydroHavoc in Godot 4.7"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\HydroHavoc\""
  - label: "Run the Packaged Windows Build"
    command: "\"D:\\Projects\\HydroHavoc\\build\\windows\\HydroHavoc.exe\""
memory_ids:
  - "11bebfee-af96-43e5-bf8a-8134c06bfbd2"
  - "9d99e337-5814-4263-af10-7e0d368da375"
  - "a91d2536-a568-4c7e-86f6-6f0cf7215baf"
  - "c9aaa671-42cc-4306-9018-6857f4d50299"
conversation_ids:
  - "50640adf-2e04-4226-93a2-6052a9ea5f35"
---

## What It Is & Why It Matters

HydroHavoc takes the 1998 N64 water-puzzle loop of *Wetrix* and rebuilds it for live audiences: the streamer places walls, trenches, drops, fireballs, bombs and sponges on a grid, while chat spends Bits and TikTok gifts to trigger disasters on the same field. The twist is that the terrain is simulated, not painted. A 32 x 32 shallow-water-equations heightfield conserves mass frame to frame, so a dam built in the wrong place does not just look wrong - it drains the lake and ends the run.

The game was built in a single day on Godot 4.7.2 and shipped with two playable artifacts: a 110 MB Windows executable and a 39.5 MB WebAssembly build published through GitHub Pages. That short path mattered because the studio wanted a streaming title that a host could open in a browser during a call, with no install and no backend. Everything runs client-side from a static folder.

Two design decisions carry the project. First, the broadcast is a first-class output: pressing `T` swaps the HUD and camera framing between a 16:9 widescreen cut and a native 720 x 1280 portrait cut, so the same session can feed Twitch, Kick, YouTube or TikTok Live without a second build. Second, the audience is physical: gift crates carry the donor's name and tier, rubber ducks drift with surface flow and score bonus points when boiled into steam, and heavy anchors sink to divert currents.

## Real Example: How It Works in Practice

- **Input**: During a live TikTok session a viewer sends a Galaxy gift while the streamer is rotating a Downer trench over a half-full lake; the streamer has `1`, `2` and `3` bound to Flash Freeze, Solar Ray and Seismic Anchor, and the broadcast is running in 9:16.
- **What Happens**:
  1. `stream_event_manager.gd` normalizes the gift into a tiered event, raises the alert banner, promotes the donor to the VIP gifter throne and forwards the disaster payload.
  2. `piece_manager.gd` keeps the polyomino queue and rotation state, so the incoming event resolves against the piece currently hovering over the grid rather than a stale cursor position.
  3. `fluid_sim.gd` advects flux across the 32 x 32 grid and `water_mesh_builder.gd` rebuilds the surface mesh; `prop_manager.gd` clamps each floating prop to the new surface height with single-point buoyancy, so the spawned crate rides the wave instead of clipping through it.
  4. `game_hud.gd` reflows the alerts, score rail and ability cooldowns into the portrait layout, while the 3D camera keeps the arena in the upper third of the frame.
- **Output**: A single Godot process producing a vertical broadcast with a named donor crate bobbing on a disturbed lake, an active disaster alert, and the piece queue still playable - no restart, no second scene, no re-export.

## Where It Stands & Next Steps

HydroHavoc is **shipped**: both builds exist on disk and the repository (`github.com/sleepyDjeep/HydroHavoc`) carries the initial release plus the GitHub Pages demo commit, both dated 2026-11-14. The project is 9 GDScript modules (1,640 LOC) and 2 GLSL shaders, with `terrain.gdshader` and `water.gdshader` handling the surface look.

What is real today: the fluid field, all six polyomino classes, three emergency abilities, four floating prop classes, the mock stream test dock for Bits and TikTok gifts, both aspect-ratio layouts, the Windows export and the browser build.

Next steps:
- Wire the relay used by our other streaming title (MarcoPoloLive) so real Twitch and Kick events replace the mock dock without changing the audience model.
- Add a per-round water budget so long sessions cannot starve the heightfield into a permanent flood.
- Capture a 60-second vertical clip from the packaged build for the storefront and press kit.

## Under the Hood & Local Files

### Simulation and Rendering

- **Shallow Water Equations (`scripts/core/fluid_sim.gd`)**: explicit heightfield update over a 32 x 32 grid. Each step computes flux between neighbours, applies damping, and rejects negative depth, which keeps the water surface stable at the frame rates used for the broadcast. The README records the measured cost as under 3% CPU on the target laptop.
- **Mesh rebuilds (`terrain_mesh_builder.gd`, `water_mesh_builder.gd`)**: both meshes are regenerated from the heightfield once per update instead of relying on vertex shaders, so collision and visual surface stay in sync and props can sample the same data.
- **Floating props (`scripts/props/floating_prop.gd`, `prop_manager.gd`)**: four classes - rubber ducks, viewer gift crates, sinking anchors and the streamer mascot GLB. Buoyancy is a single surface sample plus mass-scaled drift, which is enough to read as floating without a rigid-body solver.
- **Dual layouts (`scripts/ui/game_hud.gd`)**: one HUD scene with two anchor sets; the toggle changes canvas stretch, camera framing and panel order. The portrait capture in `assets/media/hydrohavoc/` was taken at 720 x 1280 from the running build.

### Build Artifacts

- `build/windows/HydroHavoc.exe` (110.6 MB) and `HydroHavoc-Windows-x64.zip` (39.5 MB).
- `build/web/index.html` with `index.wasm` (39.5 MB) and `index.pck`, mirrored into `docs/` for GitHub Pages.
- [README.md](file:///D:/Projects/HydroHavoc/README.md) - controls, build locations and the architecture map.
- [project.godot](file:///D:/Projects/HydroHavoc/project.godot) - Godot 4.7 Forward+ configuration.
