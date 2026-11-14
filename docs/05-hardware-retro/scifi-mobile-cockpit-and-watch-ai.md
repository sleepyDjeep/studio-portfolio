---
id: "scifi-mobile-cockpit-and-watch-ai"
title: "Sci-Fi Android Cockpit Launchers & Private Smartwatch Voice AI"
subtitle: "Non-root Steel Battalion VT mecha and Hitchhiker's Guide CRT mobile OS cockpits paired with a Tailscale-routed local RTX 4060 smartwatch voice assistant."
pillar: "05-hardware-retro"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-26"
date_updated: "2026-10-07"
tags:
  - "android-customization"
  - "klwp"
  - "steel-battalion"
  - "hitchhikers-guide"
  - "wearable-ai"
  - "tailscale"
metrics:
  - label: "Custom OS Themes"
    value: "2 Interactive Cockpits"
  - label: "Display Target"
    value: "1080x2400 @ 120 Hz OLED"
  - label: "Cloud Subscriptions"
    value: "$0 (100% Local AI)"
  - label: "Root Required"
    value: "None (Nova + KLWP + HFP)"
media:
  - src: "assets/media/scifi-mobile-cockpit-and-watch-ai/steel-battalion-cockpit.jpg"
    kind: "authentic"
    caption: "Custom Steel Battalion 2-stage VT mecha startup cockpit theme built for Moto G Stylus 5G (Nova + KLWP Pro)."
  - src: "assets/media/scifi-mobile-cockpit-and-watch-ai/hitchhikers-sub-etha.jpg"
    kind: "authentic"
    caption: "Custom Hitchhiker's Guide Sub-Etha amber/green CRT live telemetry mobile interface."
diagram: ""
tech_stack:
  - "Nova Launcher + KLWP Pro State Machines"
  - "Android Bluetooth HFP / SCO Audio"
  - "Tailscale WireGuard Mesh"
  - "Faster-Whisper STT & Kokoro/XTTS-v2"
  - "Local Qwen / Llama LLM + Obsidian Vault"
local_paths:
  - label: "Moto G Stylus Cockpit Guides & Renders (C111)"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804"
  - label: "Steel Battalion VT Cockpit Guide"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804/steel_battalion_setup_guide.md"
  - label: "Hitchhiker's Guide Sub-Etha Theme Guide"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804/hitchhikers_guide_setup_guide.md"
run_commands: []
memory_ids:
  - "7c8ff54f-1a14-4775-b08b-0860da3ffd70"
  - "d84dd875-272f-415a-b6d2-820f42ed3243"
  - "0e0fb892-74a6-4967-879a-c910071e60a8"
  - "0f8853d4-a299-43dc-abf3-482a2c1a2a6c"
  - "f7ebd706-a40d-45da-b170-44c3f84e1106"
conversation_ids: []
---

## What It Is & Why It Matters

Modern smartphones pack `120 Hz` OLED panels and rich hardware sensors yet force everyone onto identical grids of rounded corporate icons and cloud-tethered voice assistants that harvest microphone audio. Across two mobile engineering sessions (`M0855`–`M0859`), we transformed an unrooted **Motorola Moto G Stylus 5G** and a budget Bluetooth speakerphone smartwatch into tactile, retro-futuristic personal terminals backed by our home RTX 4060 AI workstation.

On the visual side, we built two complete **Nova Launcher + KLWP Pro** live-telemetry interfaces (`1080x2400`): a 2-stage **Steel Battalion 2nd-Gen Vertical Tank (VT)** mecha ignition console and a source-faithful **Hitchhiker's Guide to the Galaxy** Sub-Etha electronic book. On the voice side, we architected a zero-subscription wrist-to-homelab loop that routes Bluetooth watch audio through Android over Tailscale to local Whisper STT, local Qwen/Llama inference, Obsidian Markdown vault tools, and neural TTS playback.

## Real Example: How It Works in Practice

- **Input**: Picking up the locked Moto G Stylus 5G (or tapping the **EMERGENCY EJECT / Voice** switch / smartwatch speakerphone button while away from home on LTE/5G).
- **What Happens**:
  1. **Stage 1 Cold Standby (`$si(locked)=1`)**: In the *Steel Battalion* theme, the lock screen displays dim red cabin standby lighting (`SYSTEM OFFLINE - AWAITING IGNITION SEQUENCE`) with guarded safety switches; in the *Hitchhiker's* theme, the pulsing amber **"DON'T PANIC"** cover idles while Cosmic Cutie's vector rings rotate on a 12-second loop.
  2. **Stage 2 Ignition & Live Telemetry (`$si(locked)=0`)**: Unlocking fires the cockpit online—mapping real Android sensors onto 3 CRT monitors (`FUEL: $bi(level)$%`, `HYDRAULIC: $round(rm(used)/rm(tot)*100)$% PSI` RAM load, `REACTOR TEMP: $bi(temp)$°C`, step-counter ground speed, 360-degree radar sweep, and storage `ARMOR INTEGRITY`), or engaging 3D gyroscope starfield parallax and diagnostic charging/Wi-Fi/low-battery bezel LEDs on the Sub-Etha terminal.
  3. **Tactile Switch App Bays**: Transparent `1x1` zones on a `10x10` dockless Nova grid bind physical console toggles (`COMM SYSTEM`, `DATA LINK`, `OPTICAL SENSOR`, `FCS`, `WEAPON 1` -> Obsidian, `EMERGENCY EJECT` -> Flashlight or Voice Assistant).
  4. **Private Wrist/Mobile Voice Loop**: Speaking into a budget Bluetooth HFP/SCO smartwatch mic streams audio through a Kotlin Android foreground service over our **Tailscale WireGuard mesh** to the home RTX 4060 (`Faster-Whisper STT -> Local Qwen/Llama + Obsidian Vault read/write -> Kokoro / XTTS-v2 TTS`), returning spoken answers straight to the wrist speaker.
- **Output**: A diegetic mecha or Sub-Etha mobile cockpit running at `120 Hz` with zero root modifications and private home-GPU voice intelligence anywhere with cell coverage.

## Where It Stands & Next Steps

Both custom `1080x2400` cockpit themes (`Steel_Battalion_VT_Cockpit_{LockScreen,HomeScreen}.jpg` and `hitchhikers_authentic_wallpaper_1790529907115.jpg`) alongside complete KLWP formula sheets and `10x10` Nova touch-zone coordinate maps were shipped and transferred directly onto the Moto G Stylus 5G (`C111`). The Tailscale smartwatch voice architecture (`M0855`) is specified end-to-end and pairs cleanly with our shipped `D:\LocalAssistant` FastAPI/WebSocket backend.

Next steps for the mobile/wearable stack:
- Wire KLWP HTTP `$wg(...)` JSON polling over Tailscale so a fourth Sub-Monitor on the *Steel Battalion* home screen displays live RTX 4060 VRAM temperature and active studio task status from home.
- Package the Kotlin Bluetooth SCO -> Tailscale WebSocket audio relay into a signed sideloadable `.apk` pointed directly at `D:\LocalAssistant` (`:8888/ws/chat`).

## Under the Hood & Local Files

Achieving animated lock-and-home state transitions on modern Android without rooting or draining the battery relies on binding **KLWP** as both system wallpaper targets and driving visibility layers off `$si(locked)$` rather than running background screen-overlay services (`SYSTEM_ALERT_WINDOW`). For the *Hitchhiker's Guide* interface (`M0856`–`M0857`), we synthesized three distinct historical eras into one coherent chassis: the 1979 novel's Cosmic Cutie mascot, Rod Lord's 1981 BBC neon-green phosphor wireframe star charts, and the 2005 film's bolted dark-metal hardware bezel with reactive green/amber/red status LEDs (`$if(bi(charging)=1, 1, 0)$`). For the smartwatch voice architecture (`M0855`), using standard Bluetooth Hands-Free Profile (`HFP/SCO`) lets any `$25–$40` speakerphone watch act as a dumb wireless mic/speaker peripheral—bypassing proprietary WearOS cloud sandboxes completely.

Local guides and authentic `1080x2400` theme renders:
- **Steel Battalion 2-Stage VT Cockpit Manual & Formulas**: [steel_battalion_setup_guide.md](file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804/steel_battalion_setup_guide.md)
- **Hitchhiker's Guide Sub-Etha Terminal Manual & Formulas**: [hitchhikers_guide_setup_guide.md](file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804/hitchhikers_guide_setup_guide.md)
- **High-Res Theme Assets (`C111` Brain Directory)**: [steel_battalion_vt_cockpit_1790530710523.jpg](file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804/steel_battalion_vt_cockpit_1790530710523.jpg), [steel_battalion_vt_lockscreen_1790530754741.jpg](file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804/steel_battalion_vt_lockscreen_1790530754741.jpg), and [hitchhikers_authentic_wallpaper_1790529907115.jpg](file:///C:/Users/ogreb/.gemini/antigravity/brain/e95a171a-a23f-4de0-abbd-d86414c56804/hitchhikers_authentic_wallpaper_1790529907115.jpg)
