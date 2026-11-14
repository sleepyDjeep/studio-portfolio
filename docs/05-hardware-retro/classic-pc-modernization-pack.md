---
id: "classic-pc-modernization-pack"
title: "Classic PC Shooter Modernization Pack (1995–2007)"
subtitle: "Native 64-bit source ports, d3d9on12 discrete GPU routing, high-refresh interpolation, and gyro controller engineering for Halo, Jedi Knight, and Half-Life 2."
pillar: "05-hardware-retro"
entry_type: "workflow"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-29"
date_updated: "2026-10-14"
tags:
  - "pc-preservation"
  - "source-ports"
  - "d3d9on12"
  - "gyro-aiming"
  - "halo"
  - "star-wars-jedi-knight"
metrics:
  - label: "Modernized Campaigns"
    value: "7 Landmark Shooters"
  - label: "Native 64-Bit Ports"
    value: "3 Engine Rebuilds"
  - label: "Target Frame Rate"
    value: "120–240 Hz Interpolated"
  - label: "Controller Upgrade"
    value: "Switch Pro Gyro + Flick"
media:
  - src: "assets/media/classic-pc-modernization-pack/halo-ce-running.png"
    kind: "authentic"
    caption: "Halo: Combat Evolved running natively on Windows 11 RTX 4060 with SafeDisc bypass and Chimera high-refresh interpolation."
  - src: "assets/media/classic-pc-modernization-pack/halo-2-running.png"
    kind: "authentic"
    caption: "Halo 2 Project Cartographer running crash-free via d3d9on12 discrete GPU routing."
diagram: ""
tech_stack:
  - "Direct3D 9On12 (d3d9on12)"
  - "Chimera Interpolation Mod"
  - "Project Cartographer"
  - "The Force Engine (TFE)"
  - "OpenJKDF2 & OpenJK (x64)"
  - "Steam Input Gyro API"
local_paths:
  - label: "Modernized PC Games Directory"
    path: "file:///D:/Games"
  - label: "RetroBat Windows Game Junctions"
    path: "file:///E:/RetroBat/roms/windows"
  - label: "Halo CE & Halo 2 Verification Session (C106)"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/6046c682-eb09-4dbc-b580-a33adfcb880c"
run_commands:
  - label: "Open Modernized PC Library Folder"
    command: "explorer \"D:\\Games\""
memory_ids:
  - "d5f734a1-f4d1-4bc1-a204-ff7c9f94f71a"
  - "5f44ba23-34f5-4272-a20c-c45ae1e4f962"
  - "45f40b03-fadb-4764-90c0-135b003e3bbb"
  - "075dab96-73d3-4d71-88d8-746a72637334"
  - "9e532740-9db3-4e05-898c-887ca9220183"
  - "1ca257d2-0006-4674-bcfa-30b6efff0722"
  - "a45faae4-dae8-4aa3-a107-5f18eeed41bc"
  - "86326f99-3c11-4d8a-a25b-b920e09aa5e9"
  - "9202cba7-c897-4251-8751-aabd1e1bfdb3"
conversation_ids: []
---

## What It Is & Why It Matters

Golden-era PC shooters from 1995 through 2007 suffer from three distinct Windows 11 failure modes: blocked kernel DRM drivers (`secdrv.sys` SafeDisc on *Halo: Combat Evolved*), broken hybrid-laptop GPU adapter handoffs (Games for Windows Live era Direct3D 9EX crashes on Optimus laptops in *Halo 2*), and locked 30 FPS animation ticks or 4:3 FOV clamping across classic LucasArts engines. Rather than running heavy virtual machines, we built a repeatable modernization workflow across `D:\Games` that pairs clean 64-bit engine source ports, DirectX 12 translation layers, and modern gyro-aiming profiles.

Every modernized title launches cleanly at native high refresh rates on our RTX 4060 workstation and links straight into our RetroBat Windows carousel via zero-byte shortcuts—giving 25-year-old PC classics the exact responsiveness of a 2026 release.

## Real Example: How It Works in Practice

- **Input**: Retail/GOG installations of *Halo: Combat Evolved* (2003), *Halo 2 Vista / Project Cartographer* (2007), the 4-game *Star Wars: Jedi Knight* saga (*Dark Forces*, *Jedi Knight: DF2 + Mysteries of the Sith*, *Jedi Outcast*, *Jedi Academy*), and *Half-Life 2 (20th Anniversary)* on a hybrid Intel Iris Xe + NVIDIA RTX 4060 Windows 11 laptop.
- **What Happens**:
  1. **Halo CE**: Replaces the dead SafeDisc DRM stub with patched v1.0.10 binaries and injects **Chimera**, unlocking 30-FPS-locked keyframe animations into interpolated `120–240 Hz` motion with proper horizontal widescreen FOV scaling.
  2. **Halo 2**: Hybrid Optimus laptops crash on launch when *Halo 2* queries legacy D3D9 adapters across iGPU/dGPU boundaries; routing the executable through Windows 11's **`d3d9on12`** translation layer binds rendering deterministically onto the discrete RTX 4060 GPU.
  3. **Star Wars Jedi Knight Quad-Pack**: Keeps original `.GOB`, `.GOO`, and `.PK3` game archives untouched while swapping in native 64-bit engines—**The Force Engine (TFE)** for *Dark Forces*, **OpenJKDF2** for *Dark Forces II* & *Mysteries of the Sith*, and **OpenJK** for *Jedi Outcast* & *Jedi Academy*.
  4. **Half-Life 2 Gyro Modernization**: Configures native Nintendo Switch Pro Controller 6-axis IMU gyro aiming (paired with right-stick camera sweeps) for precision couch FPS play without mouse-and-keyboard desk ergonomics.
- **Output**: Seven classic PC campaigns running natively on Windows 11 at modern widescreen resolutions and high refresh rates, verified live with zero startup crashes.

## Where It Stands & Next Steps

All four shooter modernization tracks are deployed and verified on `D:\Games` (`M0862`–`M0865`, `M0888`–`M0889`, `M0954`–`M0955`), alongside disk staging verification for upcoming tactical releases (`M0920`). Both *Halo: Combat Evolved* and *Halo 2* were captured running live on the RTX 4060 pipeline during session `C106`, and their `.lnk` launchers sit directly inside RetroBat's `windows` system shelf.

Next steps for expanding this PC preservation pack:
- Apply the same `d3d9on12` + Vulkan `DXVK` Optimus-routing matrix to early Direct3D 8/9 immersive sims (*Deus Ex: Invisible War*, *Thief: Deadly Shadows*, and *F.E.A.R.*).
- Export our Switch Pro gyro + flick-stick profile template into `D:\Projects\_Shared_Library` so any source-port shooter inherits consistent sensitivity curves in one copy.

## Under the Hood & Local Files

Our Unified Memory Bank records (`M0862`–`M0865`) document a subtle hybrid-laptop pitfall: forcing an older 32-bit Direct3D 9 executable to "High Performance NVIDIA GPU" inside Windows Graphics Settings still fails when the game's internal adapter ordinal (`Adapter 0` vs `Adapter 1`) mismatches the panel mux connected to Intel Iris Xe. Routing D3D9 calls over `d3d9on12` hands adapter selection to DXGI 1.6 on DirectX 12, eliminating the ordinal mismatch without third-party injector DLL conflicts. For the LucasArts lineage (`M0888`–`M0889`), separating original asset `.PK3`/`.GOB` archives from 64-bit source-port binaries (`tfe.exe`, `openjkdf2-64.exe`, `openjk_sp.x86_64.exe`) preserves 100% vanilla campaign scripting while adding hardware perspective-correct rendering and modern RawInput mouse polling.

Key local directories and verification captures:
- **Installed PC Classics & Source Ports**: [Games](file:///D:/Games)
- **RetroBat Windows Carousel Integration**: [windows](file:///E:/RetroBat/roms/windows)
- **Live Windows 11 Execution Captures (`halo_running.png`, `halo2_running.png`)**: [C106 Brain Artifacts](file:///C:/Users/ogreb/.gemini/antigravity/brain/6046c682-eb09-4dbc-b580-a33adfcb880c)
