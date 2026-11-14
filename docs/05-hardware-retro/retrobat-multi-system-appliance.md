---
id: "retrobat-multi-system-appliance"
title: "RetroBat 27-System Living-Room Console Appliance"
subtitle: "A 728-game living-room arcade and console appliance with 1-click CRT/party display switching, F10 CoreAudio isolation, and self-healing 6-controller profiles."
pillar: "05-hardware-retro"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-08"
date_updated: "2026-11-11"
tags:
  - "retro-gaming"
  - "emulation"
  - "windows-coreaudio"
  - "win32-csharp"
  - "ntfs-junctions"
  - "hardware-appliance"
metrics:
  - label: "Curated Library"
    value: "728 Games / 27 Systems"
  - label: "Custom Automation"
    value: "6,823 SFW LOC"
  - label: "Verified BIOS"
    value: "27 Files (0 Missing)"
  - label: "Controller Guard"
    value: "6 Heterogeneous Pads"
media:
  - src: "assets/concepts/retrobat-multi-system-appliance.png"
    kind: "concept"
    caption: "Concept Preview: Living-room 27-system appliance toggling between 4:3 CRT bezel solo play, 16:9 4-player party splitscreen, and F10 CoreAudio Theatre Mode."
  - src: "assets/media/retrobat-multi-system-appliance/xemu-console-capture.png"
    kind: "authentic"
    caption: "Hardware-accelerated console emulation capture integrated into the 27-system living-room library."
diagram: "assets/diagrams/retrobat-multi-system-appliance.svg"
tech_stack:
  - "Python 3.13"
  - "C# (.NET Win32 P/Invoke)"
  - "RetroBat v8.2.1"
  - "Windows CoreAudio (pycaw)"
  - "NTFS Directory Junctions"
  - "CHDman v5"
local_paths:
  - label: "RetroBat Appliance Root"
    path: "file:///E:/RetroBat"
  - label: "Theatre Mode Daemon"
    path: "file:///E:/RetroBat/tools/theatre_mode"
  - label: "Display Mode Switcher"
    path: "file:///E:/RetroBat/tools/mode_switcher"
  - label: "Dolphin Bezel Launcher"
    path: "file:///E:/RetroBat/tools/dolphin_bezel"
  - label: "Controller Guard"
    path: "file:///E:/RetroBat/tools/controller_guard"
run_commands:
  - label: "Toggle Solo CRT / 4P Party Mode"
    command: "\"E:\\RetroBat\\Toggle_Game_Mode.bat\""
  - label: "Launch F10 Theatre Mode Audio Daemon"
    command: "\"E:\\RetroBat\\theatre_mode.bat\""
  - label: "Run Full 27-System Readiness Audit"
    command: "python \"E:\\RetroBat\\tools\\verify_full_system_readiness.py\""
memory_ids:
  - "920c85e9-d8ff-4f8f-a503-9dd6dd92ef64"
  - "363a3a0d-2fe3-4b61-9f3a-395b360d4fef"
  - "0456443a-a549-4e4c-b243-c41686b7ab25"
  - "a28c17b8-b8ac-49b1-95ff-f0c2f4172a73"
  - "ba9f0a79-486b-47cd-a348-755ebfb4e920"
  - "01cdc616-2924-4adb-821a-397f86cd3165"
  - "54844b98-d272-43d9-a058-2cb28360dba4"
  - "88056f94-2628-401a-adca-a67f3123f610"
  - "e864d556-c302-4821-93c9-84ea4844ffef"
  - "6c36242f-40c1-41c4-8cdd-d38ece767209"
  - "ac705b4e-494d-463b-a1ef-72161d9e0464"
  - "c458c9a3-45fc-4427-8735-60964112839c"
  - "2671b8e7-4057-45ab-a0bc-e4eb57f0f05d"
  - "e59af233-604e-40b2-b078-1fde1e4915e9"
  - "99426c72-30eb-440d-829b-cefffc1d6f9a"
  - "b5e14705-1e1d-4c81-8481-3ed3aa2556d0"
  - "565e54bc-0230-4e68-9e16-3c18c869bec2"
  - "2a652347-85f9-4268-ae46-1a2a982fdc24"
  - "5358b324-513f-4da7-bc0f-01c6992b5dd7"
  - "dc36a6c0-a4e3-412f-a195-2fe80cc49f76"
  - "7f8bf2c2-408a-4a84-9135-88698e5ffb47"
  - "161e6b64-40b4-42bd-8bd8-42c36028b322"
  - "c43ee110-fc76-44e8-84a4-921cbd407073"
  - "77c1f33d-e22c-4be5-81b5-df416b824611"
  - "84a3882b-45cb-46da-9e8a-61a6a84393fc"
  - "0ef90d30-6ca1-4876-a1df-7cb1b49a7e95"
  - "9e1bc99b-139b-4bb5-838c-af3da1b960b9"
  - "ef433a19-22cb-444c-beab-bf073dab0247"
  - "e0f47387-953e-453b-b84a-1f79c582eacc"
  - "78f8ba93-6acb-45dc-9043-95d51e0aa834"
  - "b76bb376-176f-44c3-a0e4-558bbf809c22"
  - "8fd31e8c-8613-43f2-9e7c-990865b11049"
  - "f2ddf527-4450-42f8-86c7-85dcc0d0aa04"
  - "c24b2433-339e-43bd-a7d1-3c925a1cef66"
  - "65e6733e-5e31-4206-845f-046e5ceba059"
  - "6fd92536-d25b-40bf-9a0d-ddef616c310b"
  - "4996cb1c-64ef-48f2-857a-a332e87c6885"
  - "19b43e6f-5237-412a-842b-c0959a4439b5"
  - "01b2bcbd-48fe-4abb-b062-6b3dc526b87d"
  - "ed68f669-4a0a-492f-9149-4063e3143b58"
  - "6730ff28-b96c-4b46-8032-65a6e54fb852"
  - "c4f34b03-179f-4ea0-a851-ba9120e7ed23"
  - "28ed2523-4eaa-45bf-b38e-c750c94e4c8a"
  - "491f7dee-0917-4b93-b49f-004b95d77e75"
  - "4683f980-6825-429f-a9c5-2a3d2129f172"
  - "4b2ac537-f71e-439a-beb3-0fe6596f13a9"
  - "0606d283-6d65-4ff7-81bd-c058f8ebce92"
  - "7dc56ea3-22e8-4eb1-8f79-99b717ae54de"
  - "12eeea10-79c3-485d-a407-6a6f053691a2"
  - "967131e5-eafd-48d0-97a4-2ae5238a20ca"
  - "0b43954f-c873-4276-8358-9e4ab244eaad"
  - "e8beb707-bc99-44a4-92ba-faceaa6ded2a"
  - "6d9529ae-9dc4-4998-84fb-a2e69b4fb7f0"
  - "bad93801-3fbc-450f-90e9-1566572a5979"
  - "fbb5fa2a-bdbd-4ce6-8d58-7a968205229f"
  - "84e87ff0-e375-421d-b225-1ab00b8d88f5"
  - "c8fc1621-34d2-49f6-baa2-e03e2839ab3e"
  - "6d831cc5-5dd5-4319-9a53-5d92c3de8f22"
  - "01cab641-3113-42f1-a963-401bc8d913e6"
  - "8ec5d2a4-1b41-42fc-9d1a-2b938677f38d"
  - "28ed031e-a18a-4224-a593-b077b8df0f65"
  - "f87caded-e128-4691-86fd-fefe2501c67f"
  - "9366af20-608e-44ee-8015-b8178f6864df"
  - "ad8fb7bd-8866-4088-80a8-df6c2c06723c"
  - "5ee1ce93-93e6-48f1-ac47-082804306976"
  - "a5c369c7-f694-46dd-9a9b-dc4153f5c52a"
  - "29a14d02-ffa8-4e55-9547-b2991f0d2a90"
  - "0f35775c-f52b-4729-a791-6f467a85b258"
  - "f04c81b1-6dce-4da3-8b4a-684e181e4799"
  - "74b7169d-5f49-4076-a23e-3496a70b9e65"
  - "deed53e1-a2f3-4f64-9233-592527ad910b"
  - "02ec861b-ace2-49ab-8614-2c61f4f02dc1"
  - "65635003-a27a-4e85-957a-d47173cb8906"
  - "95309d55-d2a7-4635-849e-a556254da7c3"
  - "6a9941a3-23a9-4a64-84e3-6b9c46e8dd63"
  - "21acbeb8-8914-4714-b9d1-41adb7c59cc6"
  - "63c564e4-a8bd-44f7-a988-1fb5f649b552"
  - "38576f44-8503-4e0d-aa00-383dff26d705"
  - "588a9a76-42aa-48d9-97bb-9ef6d2d3bb5c"
  - "2ccb8e15-a50a-45df-a10e-3954f127391a"
  - "9f248c17-717b-4ec0-83f9-2174b5715996"
  - "d0b0d454-7d39-41ea-b207-f28cba9ebbe5"
conversation_ids:
  - "74fd5a86-2405-428b-aedc-704910f772ad"
  - "f07031f4-45e9-4254-aaa0-0c59f5852507"
  - "6046c682-eb09-4dbc-b580-a33adfcb880c"
  - "879ea8b0-dca2-4dc1-b621-b7f9d0f191bf"
  - "398b08ad-4526-45e7-b4fd-d0cbe647a3be"
  - "c0674ec2-7381-42d1-8bff-990bc0794819"
  - "61504091-55fb-4f11-b1f4-742bd8f83416"
  - "a9639ab1-8195-4843-b3e3-334c57474ab1"
  - "bdc0d833-d416-4365-83a8-ed209f868b47"
  - "48f1cd2a-fce7-4905-99dc-de18b4d61374"
  - "b6bbd621-e017-4deb-8be9-75e7b307c775"
  - "3e98c00e-6665-4cdf-8a63-f82aef4577c0"
  - "bd6eff97-022a-405e-8bf2-e1365ee39fc4"
  - "0571e561-27d3-4f46-9036-a1fc91961020"
  - "758312e4-3cc0-4836-bc40-c7d4ea5a3381"
---

## What It Is & Why It Matters

PC-based living-room emulation almost always breaks down the moment friends sit on the couch. Bluetooth gamepads scramble player order on reboot, standalone emulators pop up outside television bezels, and game audio drowns out a movie playing on a second screen. We built a custom Windows systems layer around RetroBat v8.2.1 (`E:\RetroBat`) that turns 27 arcade, handheld, computer, and console platforms—totaling 728 curated English titles—into a zero-keyboard living-room console appliance.

Instead of duplicating hundreds of gigabytes of disc images across constrained external storage, the appliance links multi-drive libraries on `D:\` and `E:\` into RetroBat using 21 zero-byte NTFS directory junctions. Over two months of living-room stress testing, we wrote 6,823 lines of custom SFW Python and Win32 C# tooling to eliminate every friction point we hit: Intel integrated GPU heap crashes, ampersand command-line bugs on USB HID paths, corrupted NES ROM headers, N64 interpreter slowdowns, and mixed-brand controller drift.

## Real Example: How It Works in Practice

- **Input**: Four players pick up a mixed pile of controllers—a Nintendo Switch Pro Controller, an 8BitDo Ultimate 2C (BLE), a Manba One wireless pad, and an Xbox Series pad—to play 4-player *Mario Kart: Double Dash!!* on the living-room TV while a movie streams in Chrome on the secondary display.
- **What Happens**:
  1. Clicking `Toggle_Game_Mode.bat` runs `mode_switcher.py`, switching the system from **Single-Player CRT Mode** (4:3 `Ckau-CRT-LightsOff-Unglazed` cabinet bezels) to **Multiplayer Party Mode** (16:9 widescreen patches, bezels stripped, 3x `1080p` internal scaling) and firing an HTTP `/reloadgames` call to EmulationStation.
  2. Before GameCube boots, `enforce_controller_profiles.py` audits `es_input.cfg`, `retroarch_controller.json`, and emulator `.rmp` files, stripping stale `xinput` driver locks and `-1` unbound button entries so all four controllers map deterministically.
  3. Pressing `[F10]` triggers `theatre_mode.py`, which walks the active Windows process tree via CoreAudio (`pycaw`) to mute EmulationStation, RetroArch, and child game binaries while keeping Chrome, VLC, MPV, and Plex unmuted on the second screen.
  4. When switching back to solo CRT play, our compiled Win32 wrapper `dolphin_launcher.exe` intercepts Qt6 `Dolphin.exe` via `user32.dll`, strips window borders, and snaps the render viewport cleanly into the off-center CRT glass cutout at `(X=219, Y=17, W=1171, H=881)`.
- **Output**: Instant 4-player 1080p splitscreen or pixel-locked 4:3 CRT bezel play with zero manual input remapping, zero desktop window chrome, and independent dual-screen audio isolation.

## Where It Stands & Next Steps

The appliance is shipped and runs daily across 27 active systems with 100% scraped boxart, marquee logos, and preview videos. Cryptographic MD5/SHA1 audits via `verify_full_system_readiness.py` confirm all 27 required firmware files in `E:\Firmware` report `0 missing` in `batocera-systems.exe`. After byte-offset flash forensics exposed counterfeit NAND on an earlier USB drive on November 4, 2026, the entire setup was rebuilt cleanly onto verified storage with CHD v5 lossless optical compression (`process_ps2.ps1`) and 75 staged EmulationStation themes linked via zero-byte junctions.

Next steps for the living-room rig:
- Add automatic per-game Switch Pro gyro passthrough profiles for light-gun arcade titles (Sega Model 2/3 and TeknoParrot).
- Expose the `mode_switcher.py` Solo CRT vs. 4P Party toggle directly inside the EmulationStation system carousel alongside the existing Theatre Mode trigger.
- Package the standalone C# bezel snapper (`dolphin_launcher.cs`) for Xemu and PCSX2 Qt windows that ignore standard RetroArch viewport overrides.

## Under the Hood & Local Files

Crash dump analysis early in the build (`emulationstation.exe.19652.dmp`) traced intermittent `0xc0000374` (`STATUS_HEAP_CORRUPTION`) crashes to Intel Iris Xe OpenGL texture cleanup (`glDeleteTextures`), which we permanently resolved by binding EmulationStation and all standalone emulators to the discrete NVIDIA RTX 4060 Laptop GPU. We also compiled console-free Win32 C# launchers (`snes_launcher.exe` and `dos_launcher.exe`) to bypass `cmd.exe` argument splitting when Bluetooth HID device instance paths contain `&` characters (`VID&022DC8`), repaired malformed iNES headers across classic NES ROMs, switched RMG/Mupen64Plus-Next off a 20x-slower `Pure Interpreter` override, and integrated 3dSen PC v0.9.11 (83 voxel NES profiles) plus DOSBox-Staging v0.83.0.

Key SFW engineering modules under [RetroBat](file:///E:/RetroBat):
- **CoreAudio Process-Tree Muter (`724 LOC`)**: [theatre_mode.py](file:///E:/RetroBat/tools/theatre_mode/theatre_mode.py) and [theatre_mode.bat](file:///E:/RetroBat/theatre_mode.bat) — global `[F10]` audio isolator with non-focus-stealing HUD toast notifications.
- **CRT vs. Splitscreen Mode Switcher (`496 LOC`)**: [mode_switcher.py](file:///E:/RetroBat/tools/mode_switcher/mode_switcher.py) and [Toggle_Game_Mode.bat](file:///E:/RetroBat/Toggle_Game_Mode.bat) — rewrites bezel, aspect-ratio, and widescreen-hack configs across 6 standalone/libretro systems.
- **Win32 Borderless Bezel Snapper (`443 LOC C#`)**: [dolphin_launcher.cs](file:///E:/RetroBat/tools/dolphin_bezel/dolphin_launcher.cs) — P/Invoke `EnumWindows`, `SetWindowLongPtrW`, and `SetWindowPos` viewport injector.
- **Self-Healing 6-Gamepad Guard (`159 LOC`)**: [enforce_controller_profiles.py](file:///E:/RetroBat/tools/controller_guard/enforce_controller_profiles.py) — repairs SDL2 GUIDs and `.rmp` mappings across Switch Pro, 8BitDo Ultimate 2C, PDP Faceoff, Manba One, and Xbox controllers.
- **Disk-Safe Resumable Scraper (`940 LOC`)**: [background_scraper.py](file:///E:/RetroBat/background_scraper.py) — multi-source metadata harvester with atomic `gamelist.xml` writes and a `<500 MB` free-space cutoff guard (credentials redacted in portfolio builds).
- **Cryptographic BIOS & Theme Tooling**: [install_retrobios.py](file:///E:/RetroBat/tools/install_retrobios.py), [verify_full_system_readiness.py](file:///E:/RetroBat/tools/verify_full_system_readiness.py), and [process_ps2.ps1](file:///D:/Tools/chdman/process_ps2.ps1).
