---
id: "neon-breach"
title: "Neon Breach: Competitive Cyberpunk Puzzle-Battler"
subtitle: "Two-player networked cyberpunk puzzle-battler built on Aether Engine with WebGL2 CRT shaders, Fairlight oscilloscope stages, and asymmetric gamepad haptics."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-09"
date_updated: "2026-09-15"
tags:
  - "aether-engine"
  - "puzzle-battler"
  - "lua"
  - "multiplayer"
  - "webaudio-dsp"
  - "cyberpunk"
metrics:
  - label: "Automated Tests"
    value: "689 Passing"
  - label: "NetWar Tick Rate"
    value: "15 Hz Authoritative"
  - label: "Animated Stages"
    value: "5 Hacker Dens"
  - label: "Input Targets"
    value: "Keyboard, XInput, Touch"
media:
  - src: "assets/media/neon-breach/hacker-den-hybrid.jpg"
    kind: "authentic"
    caption: "Hacker Den competitive puzzle-battler stage layout with encrypted IC block board and telemetry HUD."
  - src: "assets/media/neon-breach/hacker-den-crt.jpg"
    kind: "authentic"
    caption: "Green-phosphor Fairlight CMI CRT oscilloscope stage visual designed for Neon Breach."
diagram: ""
tech_stack:
  - "Aether Engine v0.1.0"
  - "Lua 5.4 (Wasmoon WASM)"
  - "WebGL2 Custom Renderer"
  - "Fastify WebSockets (15 Hz NetWar)"
  - "WebAudio API & Cyber-DSP Synth"
  - "HTML5 Gamepad Haptics API"
local_paths:
  - label: "Neon Breach Project Directory"
    path: "file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach"
  - label: "Standalone Browser Bundle"
    path: "file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/standalone_game.js"
  - label: "Lua Combat & Board Scripts"
    path: "file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts"
run_commands:
  - label: "Launch Aether Engine & Open Neon Breach"
    command: "cd \"D:\\Projects\\AI Gamebuilder Engine\" && npm start"
  - label: "Run Engine + Neon Breach Verification Suite"
    command: "cd \"D:\\Projects\\AI Gamebuilder Engine\" && npx vitest run"
memory_ids:
  - "e28345cf-b18b-4a26-ba6e-44fab85e5b4c"
  - "0c1ead89-6907-4481-88e4-396fb7db88fc"
  - "27f6e040-fa93-4856-9389-79b1975e1f8e"
  - "b0a699d3-f28c-439b-8adb-4eb150e4849a"
  - "1d0d841b-0a97-4d9c-944c-5186784abc85"
  - "f99f02fc-91df-494b-bf57-6721eb156931"
  - "96dd38f3-883a-4f41-99c5-b57f3d5f602a"
  - "f9e98536-a0ac-4771-81f8-32e088a9b974"
  - "1b57c01a-7b03-4f56-bc0a-3cc8eda22d24"
  - "67d7cacf-0c98-4180-81fc-5f66efcce5b9"
  - "daf45bb8-218f-440a-8012-389f9814cd8f"
  - "e4b3e63c-6b7d-44a1-bb2b-8f264a4b845b"
  - "50913486-b2c0-45e2-8b62-9a188738a845"
  - "f27ecb1c-34ef-4e6d-bf26-58f4f5ea7b1d"
  - "4b91b3d6-24da-4d8e-8ba4-c4c07027e454"
  - "c1aacda1-2657-42a3-aa23-a1482accfb17"
conversation_ids:
  - "95f05262-5f48-4f5a-8c46-510784b99049"
  - "36bd5be2-b25a-4b68-9b31-7b7bd4d7ad23"
  - "5b041038-d029-4b6b-9d18-6d958d4ce600"
---

## What It Is & Why It Matters

*Neon Breach* is a high-speed, two-player cyberpunk puzzle-battler built natively inside *Aether Engine*. Players race to align falling microchip integrated-circuit (`IC`) blocks, trigger laser-trace chain clears, charge an **EMP Overdrive** meter, and dump encrypted firewall garbage blocks onto their rival's board—either against a tactical AI hacker or head-to-head over networked **NetWar** rooms. Every match plays out across five animated *Hacker Den* stages, highlighted by a live green-phosphor *Fairlight CMI* CRT oscilloscope waveform pulsing in sync with a procedural synth soundtrack.

A custom game engine is only as credible as the games shipped on top of it. Immediately after finishing *Aether Engine* `v0.1.0`, we created *Neon Breach* as a demanding flagship title to stress-test every subsystem at once: deterministic Lua 5.4 board physics, WebGL2 particle bursts, low-latency WebSocket multiplayer, procedural WebAudio DSP synthesis, Bluetooth gamepad rumble, and LAN QR mobile pairing.

Building a commercial-grade arcade battler exposed real-world edge cases that synthetic unit tests rarely catch—such as asymmetric Xbox dual-motor rumble envelopes during multi-chain clears, touch-swipe drop thresholds on mobile screens, and authoritative board-state reconciliation over Wi-Fi.

## Real Example: How It Works in Practice

- **Input**: Player 1 opens *Neon Breach* on PC (`http://localhost:8080`) with an Xbox wireless controller connected, while Player 2 scans the on-screen LAN QR code on an Android phone paired to a Bluetooth gamepad to join the same NetWar room. Player 1 rotates and hard-drops an encrypted `IC` piece to complete a 4-chain trace clear, then hits the **EMP Overdrive** trigger.
- **What Happens**: `tetromino.lua` and `board.lua` evaluate lock-delay frames, wall-kick tables, and laser-trace adjacency inside the `60 Hz` Lua 5.4 WASM loop. `combat.lua` converts the 4-chain combo plus EMP Overdrive charge into a staggered row of locked firewall blocks transmitted over the `15 Hz` authoritative Fastify WebSocket relay to Player 2's board. Simultaneously, `audio_synth.js` fires a procedural WebAudio bass drop and triggers a processed Cyber-DSP announcer callout (`"EMP BREACH DETECTED"`), `renderer.lua` spikes the Fairlight CMI phosphor oscilloscope trace and bursts neon GPU particles (`particles.lua`), and `gamepad.js` drives high-frequency right-motor shimmer followed by a heavy left-motor sub-thump on both controllers.
- **Output**: Synchronized 60 FPS competitive puzzle combat across desktop and mobile browsers with zero external audio/ROM dependencies, exportable as a standalone web bundle (`standalone_game.js`) or 2-second Android APK.

## Where It Stands & Next Steps

*Neon Breach* is **shipped** inside `D:\Projects\AI Gamebuilder Engine\projects\neon_breach` and verified end-to-end across desktop browser, Android mobile touch/Bluetooth, and multi-client NetWar WebSocket sessions. Automated testing grew from `659` to `689` passing tests (`0` failures) covering piece rotation kicks, deterministic garbage-queue math, AI rival heuristics, gamepad deadzones, and WebSocket room state recovery.

Next steps to take *Neon Breach* further:
- Add an asynchronous Daily Seed Score Attack leaderboard persisted to a lightweight SQLite table on the Fastify host.
- Expand the Cyber-DSP Voice Lab (`VOICE_SCRIPT.md`) with distinct rival character voice banks for each of the five Hacker Den stages.
- Package a dedicated standalone Itch.io HTML5 page with instant 1-click invite links via Cloudflare Tunnel for WAN matches outside the local Wi-Fi network.

## Under the Hood & Local Files

### Modular Lua 5.4 & Hybrid JS Architecture
Recorded across `16` Unified Memory Bank architectural entries (`M0718`–`M0733`), *Neon Breach* cleanly splits deterministic game rules in Lua 5.4 from browser hardware peripherals in JavaScript:
- **Deterministic Puzzle & Combat Core**: [main.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/main.lua) orchestrates game states, stage selection, and telemetry HUD updates; [tetromino.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/tetromino.lua) and [board.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/board.lua) handle 7-bag piece generation, SRS wall kicks, and encrypted IC node clearing; [combat.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/combat.lua) manages combo multipliers, garbage cancellation/countering, and EMP Overdrive meters; and [rival.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/rival.lua) runs a multi-tier heuristic AI opponent for solo play.
- **Fairlight CRT Stages & Particle Telemetry**: [renderer.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/renderer.lua), [palette.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/palette.lua), and [particles.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/particles.lua) render five distinct cyberpunk Hacker Den themes—including the procedural green-phosphor Fairlight CMI CRT oscilloscope grid—without relying on heavy pre-rendered video files.
- **Gamepad Haptics, Touch Gestures & Cyber-DSP Audio**: [gamepad.js](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/gamepad.js) auto-detects XInput and Android Bluetooth controllers, mapping D-pad DAS/ARR repeat rates and firing dual-actuator `vibrationActuator.playEffect("dual-rumble", ...)` envelopes. [input_gestures.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/input_gestures.lua) translates mobile touch drags, taps, and flicks into crisp grid moves, while [audio_synth.js](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/audio_synth.js) and [VOICE_SCRIPT.md](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/VOICE_SCRIPT.md) drive the real-time WebAudio synth soundtrack and ring-modulated announcer callouts.

### Key Local Files
- Project Manifest & Standalone Entry: [project.json](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/project.json), [standalone_game.js](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/standalone_game.js)
- Lua Gameplay Modules: [main.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/main.lua), [board.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/board.lua), [combat.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/combat.lua), [tetromino.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/tetromino.lua), [rival.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/rival.lua), [renderer.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/renderer.lua)
- Audio, Voice & Hardware Input: [audio_synth.js](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/audio_synth.js), [gamepad.js](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/gamepad.js), [input_gestures.lua](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/scripts/input_gestures.lua), [VOICE_SCRIPT.md](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/VOICE_SCRIPT.md), [voice](file:///D:/Projects/AI Gamebuilder Engine/projects/neon_breach/assets/voice)
