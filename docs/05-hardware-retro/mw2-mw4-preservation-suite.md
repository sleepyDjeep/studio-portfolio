---
id: "mw2-mw4-preservation-suite"
title: "MechWarrior 2 & MechWarrior 4 Windows 11 Preservation Suite"
subtitle: "Binary-level WinMM proxy DLLs, kernel-time frame pacers, and DX7-to-DX11 wrappers making 1995–2002 retail MechWarrior trilogies run crash-free on Windows 11."
pillar: "05-hardware-retro"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-23"
date_updated: "2026-08-27"
tags:
  - "binary-preservation"
  - "reverse-engineering"
  - "win32-dll-proxy"
  - "mechwarrior"
  - "windows-11"
  - "directx"
metrics:
  - label: "WinMM Proxy Exports"
    value: "179 Functions"
  - label: "Patched MW2 Binaries"
    value: "1,217 Files"
  - label: "Playability Audit"
    value: "21 / 21 Checks"
  - label: "Preservation Memories"
    value: "51 Decisions"
media:
  - src: "assets/media/mw2-mw4-preservation-suite/mw2-trilogy-launcher.png"
    kind: "authentic"
    caption: "Windows 11 execution capture of the modernized 1995–1996 MechWarrior 2 Titanium Trilogy via our custom mw2mm.dll WinMM and KUSER_SHARED_DATA timer bridge."
diagram: ""
tech_stack:
  - "C / C++ (Win32 Proxy DLL)"
  - "C# (.NET Launcher & ISO Bridge)"
  - "x86 PE Binary Patching"
  - "CNC-DDraw (GLSL)"
  - "dgVoodoo2 (DX7-to-DX11)"
  - "XInput"
local_paths:
  - label: "RetroBat PC Preservation Host"
    path: "file:///E:/RetroBat"
  - label: "MW2 Verification Captures (Brain C041)"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/73ac2c71-bebe-478b-a754-51ed13b5302b"
  - label: "MW4 & Simpit Fixes (Brain C044)"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/26266f65-baf8-419d-947a-7a2bc538e679"
run_commands:
  - label: "Launch Preserved Classics via RetroBat"
    command: "\"E:\\RetroBat\\retrobat.exe\""
memory_ids:
  - "abf13474-bb76-4672-b5e6-72a4f5d48ff7"
  - "100b50b6-f7a7-4250-baf7-73e328f8cecc"
  - "f036d23d-4cc8-438e-ad15-8239c0cdd13e"
  - "6ae099a9-a998-424a-815d-a37e1401c6a5"
  - "eac8e590-0295-4f82-b63f-92a361830a8b"
  - "bf25c58e-219d-4ec4-b730-087dca277d1b"
  - "b2fa2c19-51f1-4683-84c8-fc13bdc712df"
  - "87b101c1-48fa-4137-9242-5caca4b7592f"
  - "f4c428df-9171-4b47-820c-5fe5c4542f71"
  - "e24cffb3-9474-4eb0-a455-ce8b7b7cebb9"
  - "76bb459c-e571-417a-91d6-06a24965c794"
  - "318f0a1c-7b25-484d-b4df-26c8f515a034"
  - "56c56df3-b95c-4006-bd3b-62d9070add1c"
  - "9dbe15f2-d97b-450b-932b-f22ff6011e1c"
  - "c622ec63-15e2-47d5-a4bb-b18875bc18a0"
  - "95f17d8f-7f16-4518-bbc3-58eb5f06b918"
  - "b6e5f4f8-7839-44b1-9009-1ef7e84ddf08"
  - "49cb90dd-aae6-4a3b-adac-00deb20e462f"
  - "a716fdd0-6960-4140-91a2-9d86e1288148"
  - "fd3125cf-4a1c-4a74-9fe0-0422afe046e9"
  - "78c43c4c-869a-41d6-b2ad-f0d8830f904c"
  - "b869c8bd-0ed0-475c-b379-5224f6bb5418"
  - "02f42fd4-1379-4034-a684-863ec47e80f2"
  - "ba8b9a18-1e18-41c0-a380-696799364151"
  - "bf54fed8-5f02-48d9-9320-f0d5aea5e5fb"
  - "6e53e3a5-8cdb-490c-88b6-2ef32d09e4a6"
  - "36aa1c9a-0e28-477e-81a3-48de9d2a24c6"
  - "be59dc1c-1356-4c5f-97d2-d9dc92e3a4ec"
  - "9f7af3dc-d66a-4094-b77f-e48d392fe01a"
  - "8a99adbe-5147-494b-b0a1-be48439b36ca"
  - "898f845e-4b44-4901-94e8-7cd51921172c"
  - "aea3fc00-e783-4d9b-a808-24c435b02d42"
  - "0562ea28-0a7f-4251-aa01-cabd245a108b"
  - "1feb3de3-451e-4790-a944-a096e86d4600"
  - "a5f2ad76-80c1-4980-9fb4-d81b1a287382"
  - "9dfeb868-4a5d-445b-b746-9c35b510514c"
  - "dfeb8d48-39d6-49ed-a5d4-2c130fa529ff"
  - "b991bed0-6fc5-4cbe-a3a1-5472d6308a28"
  - "53c0a468-911c-4af6-b746-9fde4ed570c7"
  - "7c68e154-0924-4c8d-b599-578d89aa17d6"
  - "1af33806-7360-423d-9daa-60a831197948"
  - "9c896e2b-4370-4de8-a6d2-e8d5687023c7"
  - "f233bb34-a0e6-4676-8b97-bd9bdae68b7d"
  - "06af51ea-6ed8-4ea1-9e46-45530c986408"
  - "e15be8ef-4daf-4c9c-9750-c60caba857c4"
  - "4a980153-73ef-4412-a492-eddc37268101"
  - "cf694ba9-7321-49f6-8396-8e30edd31870"
  - "655186a0-4461-48f1-8dcd-68a0b125d235"
  - "39c1d0cd-4011-4ec6-aeea-c58833c3dad2"
  - "a73f4700-5c2f-46b7-87ce-19e032ddf555"
  - "efc9086c-e54a-48d9-9efe-23caeb02e2ab"
conversation_ids:
  - "ad5f3aea-2d62-4365-bcf0-351a986061a2"
  - "6abc3109-5dff-482f-b5a1-65bf6a441c39"
  - "73ac2c71-bebe-478b-a754-51ed13b5302b"
  - "517523dc-e349-4d9c-8e7d-a90a821ea681"
  - "8756068a-7ced-49e7-8586-c4c2b66f8400"
  - "26266f65-baf8-419d-947a-7a2bc538e679"
  - "908dcf4f-7b1d-4bf5-ac84-cdbfc8718424"
---

## What It Is & Why It Matters

Original retail builds of the *MechWarrior 2 Titanium Trilogy* (1995–1998) and *MechWarrior 4 Trilogy* (2000–2002) fail immediately on Windows 11. Microsoft removed the legacy 32-bit MCI CD-audio subsystem, multi-gigahertz CPUs overflow 1990s frame-delta loops into `0xC0000005` heap crashes, and modern 240 Hz displays trigger integer divide-by-zero exceptions inside Microsoft's old GameOS hardware enumerator.

We engineered a binary-level preservation suite that keeps the original retail x86 executables intact while intercepting broken Win32, DirectDraw, Direct3D 7, and DirectInput calls in memory. Beyond rescuing six landmark mech simulations for modern PCs and gamepads, the binary reverse-engineering lessons from this sprint directly informed our clean-room Godot 4.7 mech architecture in *MechDestroyer*.

## Real Example: How It Works in Practice

- **Input**: A player clicks *MechWarrior 2: Ghost Bear's Legacy* (or *MechWarrior 4: Mercenaries*) on a Windows 11 laptop running an Intel Core i9-13900H, an RTX 4060 GPU, a 240 Hz screen, and an Xbox Series XInput controller—with zero physical CD-ROM drive attached.
- **What Happens**:
  1. Hex-patched PE binaries (`DRIVE_FIXED` mapped to `DRIVE_CDROM` across 1,217 executables/DLLs, alongside 1,826 mirrored `.bwd`/`.wtb` tables for `BATTLE.DLL`) bypass physical disc checks without requiring virtual ISO mounts.
  2. Our custom 179-export relocation-immune `mw2mm.dll` WinMM proxy intercepts legacy `mciSendCommandA` Redbook CD audio calls and streams `.ogg`/WAV soundtrack tracks directly through a modern `waveOut` mixer.
  3. Inside the same proxy, a kernel-time frame pacer reads `KUSER_SHARED_DATA` (`0x7FFE0000`) nanosecond ticks directly from user-mode shared memory, clamping simulation steps so fast CPUs never corrupt heap state or run jump-jets at 10x speed.
  4. `cnc-ddraw` upscales 256-color DirectDraw surfaces via GLSL shaders (preserving all 498 Smacker `.SMK` cutscenes) while a 125 Hz XInput-to-cursor/throttle bridge translates modern thumbsticks; for *MechWarrior 4*, `dgVoodoo2` translates DX7 to DX11 at `1080p/4K` while bypassing the `IGD9TRINITY32` refresh-rate divide-by-zero crash.
- **Output**: Crash-free `1080p/4K` combat across *31st Century Combat*, *Ghost Bear's Legacy*, *MW2: Mercenaries*, *Vengeance*, *Black Knight*, and *MW4: Mercenaries* with full Redbook music, FMV cutscenes, and `ModernFPS` controller/mouse profiles (`21/21` playability checks passing).

## Where It Stands & Next Steps

All six *MechWarrior 2* and *MechWarrior 4* trilogy titles passed 21/21 verification checks during our August 23–27, 2026 engineering sprint. Following our September 18 studio storage consolidation (`M0763` / `86b7d19f`), we reclaimed ~186 GB of redundant uncompressed staging trees (`D:\MW2_Trilogy_Runner` and unpacked ISO mirrors) after archiving the architectural rules in our Unified Memory Bank and consolidating active retro launches under `E:\RetroBat`.

Next steps if we revisit classic mech binary tooling:
- Package `mw2mm.dll` (`KUSER_SHARED_DATA` timer + MCI Redbook `.ogg` streamer) as a standalone drop-in GitHub release for other 1995–1999 Activision/Win95 CD-ROM sims (*Interstate '76*, *Heavy Gear*).
- Automate `ModernFPS` DirectInput7/8 `.plr` pilot profile injection for ultrawide `21:9` aspect ratios in *MechWarrior 4*.

## Under the Hood & Local Files

Three low-level Windows 11 bugs required surgical fixes documented across 51 Memory Bank records (`M0239`–`M0295`):
1. **Relocation-Immune WinMM Forwarding**: Standard ordinal forwarding in `winmm.dll` proxies can deadlock loader locks on Windows 11 24H2; `mw2mm.dll` exports all 179 symbols cleanly while hooking only `mciSendCommandA/W`, `mciSendStringA/W`, `timeGetTime`, and `joyGetPosEx`.
2. **Lock-Free `0x7FFE0000` Pacing**: Reading `InterruptTime` directly from `KUSER_SHARED_DATA` avoids kernel syscall overhead (`QueryPerformanceCounter`) inside tight 32-bit x86 spin-loops, eliminating `0xC0000005` race conditions during mission teardown.
3. **MW4 GameOS Enumeration & 240 Hz Fix**: Microsoft's GameOS engine divides display refresh constants into 16-bit integers and chokes on high-DPI/240 Hz modes (`IGD9TRINITY32`); `dgVoodoo2` virtualizes a 60 Hz DX7 adapter surface while outputting borderless `1080p/4K` DX11 frames to the RTX 4060, and our `DTLiteBridge.cs` utility dismounted 13 leftover `TITAN_MW2`/`GBL`/`MERCS` virtual drives (`E:`–`S:`) cleanly once No-CD PE patches were verified.

Reference artifacts and live retro environment:
- **Live Retro Gaming Host**: [RetroBat](file:///E:/RetroBat)
- **MW2 Proxy & Verification Artifacts**: [C041 Brain Session](file:///C:/Users/ogreb/.gemini/antigravity/brain/73ac2c71-bebe-478b-a754-51ed13b5302b)
- **MW4 dgVoodoo2 & Simpit Artifacts**: [C044 Brain Session](file:///C:/Users/ogreb/.gemini/antigravity/brain/26266f65-baf8-419d-947a-7a2bc538e679)
