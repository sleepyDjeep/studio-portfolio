---
id: "aether-engine"
title: "Aether Engine: Browser & Mobile AI-First 2D/2.5D Game Studio"
subtitle: "Custom Fastify, WebGL2, and Lua 5.4 WebAssembly game engine with an embedded Architect-Coder-Doctor AI ensemble and 2-second Android APK exporter."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-07"
date_updated: "2026-09-09"
tags:
  - "game-engine"
  - "lua-wasm"
  - "webgl2"
  - "multi-agent-ai"
  - "typescript"
  - "android-export"
metrics:
  - label: "Total Source Code"
    value: "85,392 LOC"
  - label: "Sprite Batcher"
    value: "10,000+ @ 60 FPS"
  - label: "Crash Hotfix Latency"
    value: "< 2 Seconds"
  - label: "Automated Tests"
    value: "603+ Passing"
  - label: "APK Export Speed"
    value: "2 Seconds"
media:
  - src: "assets/media/aether-engine/studio-ide-live.png"
    kind: "authentic"
    caption: "Live capture of Aether Engine Studio v0.1.0 running on localhost:8080 with WebGL2 canvas, Lua 5.4 IDE, and Tri-Agent AI dock."
  - src: "assets/media/aether-engine/lua-engine-ui.jpg"
    kind: "authentic"
    caption: "Early UI architecture exploration for Aether Engine's integrated Lua workbench."
diagram: "assets/diagrams/aether-engine.svg"
tech_stack:
  - "TypeScript 5.7"
  - "Node.js & Fastify 5.2"
  - "Wasmoon (Lua 5.4 WASM)"
  - "WebGL2"
  - "Ace Editor & luaparse AST"
  - "ComfyUI WebSocket Bridge"
  - "Vitest"
local_paths:
  - label: "AI Gamebuilder Engine Root"
    path: "file:///D:/Projects/AI Gamebuilder Engine"
  - label: "Compiled Studio UI"
    path: "file:///D:/Projects/AI Gamebuilder Engine/dist/server/views/studio.html"
  - label: "Bundled Game Projects"
    path: "file:///D:/Projects/AI Gamebuilder Engine/projects"
run_commands:
  - label: "Start Production Studio Server (Port 8080)"
    command: "cd \"D:\\Projects\\AI Gamebuilder Engine\" && npm start"
  - label: "Start Live-Watch Dev Server"
    command: "cd \"D:\\Projects\\AI Gamebuilder Engine\" && npm run dev"
  - label: "Run Full Vitest Verification Suite"
    command: "cd \"D:\\Projects\\AI Gamebuilder Engine\" && npx vitest run"
memory_ids:
  - "9da9becc-c7b6-4f36-b11d-034804de2a26"
  - "b6258532-23b6-498b-b0ca-a8153b2ef0e4"
  - "6b0a0c28-41c9-48ae-bed8-7c1ae74e2f81"
  - "bfe03ff4-df9f-46d9-a026-711422fbe2ff"
  - "8d161ab8-ce82-4d88-a2dd-532121bc21d0"
  - "03a4e706-57ba-4084-8e8b-61d75f0825b2"
  - "99f5458e-bcc5-4cfc-b7bb-be78b4832f02"
  - "a9003ca3-c883-46fd-9d2c-34048ef1e540"
  - "b6e543d7-5456-41b4-a3dc-2a7e450083d2"
  - "00402a9e-811d-41e4-b488-23bebbce28e9"
  - "22031a7b-0cff-4236-a94b-804fa5ab5aa7"
  - "586c9c6f-d865-4539-8f4f-312b6b512d05"
  - "76af1c6a-25fe-424e-8c62-104d97e8c8c6"
  - "d7ca6bda-1752-41b1-8a62-d4676d37b1f5"
  - "37af1d37-42a3-488b-979a-a11492cb8e61"
  - "68d3ad82-d6bb-4531-9c25-982a4fe4dfc9"
  - "34f6a523-7aa1-447e-a1b6-270bce7fb167"
  - "48649d33-6109-4473-9cad-55d8b98a1c08"
  - "231e7fb7-3e47-4c39-8a04-9ad7a0e262e5"
  - "82273ab7-3b7e-41da-8370-b0b3fd58828b"
  - "b370ac5c-641e-4a5f-b60f-aa5967197bd9"
  - "9e5ca183-d5dc-41b9-88c0-fd660e184527"
  - "54c7a902-4635-4c66-8000-a89acc6f88a5"
  - "e617d5eb-e65f-4f29-bd35-3b03401b6a44"
  - "56210021-001e-4b29-a07c-3cec0261e294"
  - "de782240-eec7-4ea3-ab8d-343e1ab019e6"
  - "d6a6ab95-8ecc-4624-ae26-c26549264245"
  - "a8f157cc-c59e-4632-935d-c70c07d7502f"
  - "0f5a2eeb-95af-40f0-a500-10b450140210"
  - "20d69b72-e42a-4503-860b-c85da7b0fbe3"
  - "59514681-0e4f-4850-a6f8-ca2dabf7fba5"
  - "344af57a-65f7-4abd-ad2e-5b81edac4f4e"
  - "674756f3-1991-4c47-84c0-44deb3e3251a"
  - "bdc5444a-c327-4c78-8266-f246b874bd80"
  - "8aabecd1-58c6-48df-bea1-a80c6257f15e"
  - "a5cf452b-e6e1-4928-8912-91a83e634b9e"
  - "7687a9fd-3712-4e0f-9c06-696e4b81194f"
  - "20ea50db-fa5d-4aa4-8ef4-566fc75b3623"
  - "16840ae9-52cd-431c-b02d-6257edd78fe7"
  - "e0d2f887-43ec-4a3a-88c1-29bfd7053638"
  - "20e36870-eab2-40ec-9df5-bf6a4d120b96"
  - "423f28e0-3fc6-43a6-a91e-34294ece615c"
  - "e334a67c-4e82-4e12-90c6-6a272299c847"
  - "c5c683b4-9e7f-4f30-92d1-0aa4ba8e3866"
  - "54fd8d26-5b48-4ab6-82ee-649478262ff0"
  - "9d750e34-d209-4709-bd92-fbf91252c4b7"
  - "a484aff8-12ce-40f6-b052-d92ab26f409c"
  - "1b3cb637-9fcf-48ab-accc-23f9e6bf9ae9"
  - "a870755e-0fa1-4b4b-a12d-1a8b1bad114a"
  - "2c448ff4-628b-4000-8078-beb2469594a4"
  - "f84af6e0-a9cc-4dc9-b522-7fcd17836a00"
  - "73e93e16-2864-4ed1-b582-e569cf5ba0ad"
  - "d5b0a1ef-0232-4eda-897c-ae610a72cd3e"
  - "bd2972ae-97b0-40d8-ab69-ee02719b3583"
  - "d60c87b2-64f5-4b10-8c14-7bfcac037bc3"
  - "e3c9310e-4443-4a53-869a-9691bba22ccf"
  - "676e8826-537b-471e-b74e-3f9931b2adbc"
  - "90db5c17-d3dc-4cd7-9ae4-3e84f642e872"
  - "36e59ba3-bef9-47c9-8d27-deb3407cbacd"
  - "138edc7d-4a1e-4762-b208-18b102b80265"
  - "bea414c9-dcd2-48ef-9dbc-8ffb45f97f36"
  - "ffe30ffc-be7e-4a89-9232-d070e73fddb1"
  - "8b1d1b7d-bbd0-4137-b27e-8d49067910ad"
  - "70bfea57-3d09-4b15-a14d-17de58c392d2"
  - "df45ed9f-4df4-4b3b-8c01-a23a4ac69fce"
  - "3bf2a9e0-8901-4a0e-9439-deb52faf9788"
  - "82d25149-ea8b-40a0-94d7-033368b09a29"
  - "3f222a75-cf11-422e-b39b-8ee7a4be0e62"
  - "fdb23518-6fae-4df4-8ec4-032769e6cb4e"
  - "251267a5-ebda-41e6-b057-58eabee04540"
  - "49947e0b-f2de-4f5d-b494-b8cda98ba902"
  - "46df87ab-d731-4e95-b419-690f16a93721"
  - "111f13e7-cc53-48e8-aee9-d85d4c645457"
  - "6a6c2a85-d384-4d4b-a024-7f69e07b2208"
  - "e1a436c2-02b2-4069-9c44-9ee4e844e406"
  - "03527173-16e5-4824-80fd-7c822b156fa4"
  - "135d771b-51c7-4228-957d-03c4f36e93b4"
  - "14efd40a-b2b8-4c9f-831b-1052a5b615d1"
  - "b049f056-8496-44ab-bd7a-edc5ad56b3df"
  - "4bb525b8-85f9-41e6-a99e-df3cfb2c60c6"
  - "456e4d78-f4fc-4d82-a07d-a469a18d33c9"
  - "46633367-757c-4e6c-b224-7a80919070f5"
  - "fca3752e-86e1-4a99-9ac8-698464701b58"
  - "9de2fdaf-7606-4589-b300-c8b5f8bc97b5"
conversation_ids:
  - "2397f716-5e07-44d1-9b7b-bcb7790dbc26"
  - "ebdca03f-c1ff-4d20-b8bc-09ed3ab14f5c"
  - "27e4ba52-dd88-49f4-8d45-ba51ff3819b4"
  - "c3d9326b-8e8c-49fd-b2c1-b94299d7e8e1"
  - "300d648f-d6a2-4987-af7e-44eb2cee4898"
  - "3ee1d58b-1a43-4e8c-9afe-f139b087118c"
---

## What It Is & Why It Matters

*Aether Engine* (`v0.1.0`) is a custom cross-platform 2D and 2.5D game engine built from scratch so a solo creator can design, code, paint, playtest, and export complete games inside a desktop browser or paired Android phone. Instead of bolting an external chat sidebar onto a heavy native editor, *Aether Engine* embeds a three-agent AI team directly into the runtime loop alongside a sandboxed Lua 5.4 WebAssembly virtual machine, a high-throughput WebGL2 renderer, a 4-layer tilemap painter, a procedural WebAudio synthesizer, and a ComfyUI sprite generator.

Traditional game engines slow down rapid arcade prototyping in two places: context-heavy scripting APIs that confuse local language models, and multi-gigabyte Android SDK toolchains required just to test touch controls on a phone. *Aether Engine* eliminates both bottlenecks. Games use clean `init()`, `update(dt)`, and `draw()` Lua 5.4 hooks indexed into a compact syntax graph so local LLMs edit exact functions without blowing out token budgets, while a pure-Node binary APK injector packages playable Android builds in two seconds without installing Gradle or Android Studio.

Within our studio portfolio, *Aether Engine* serves as both a standalone creative product and the live runtime foundation for 11 bundled starter and flagship games—including our competitive cyberpunk puzzle-battler *Neon Breach*, `boomer_shooter_starter`, `cyber_arena`, `final_fantasy_clone`, and `forest_knight`.

## Real Example: How It Works in Practice

- **Input**: You boot `npm start` on `http://localhost:8080`, scan the terminal QR code to pair your phone over LAN as a live touch controller, and prompt the Studio AI dock: *"Create a top-down cyber-knight arena with 47-tile stone walls, laser sfx, and dashing."* You then deliberately introduce a nil-index bug on line 42 of `main.lua` during live play.
- **What Happens**: The **Architect** agent decomposes the prompt into scene and script tasks using the `luaparse` AST symbol graph; the **Coder** agent writes the Lua 5.4 modules and triggers `sfxr` laser presets; and if local ComfyUI (`127.0.0.1:8188`) is online, the WebSocket bridge generates a sprite sheet, strips backgrounds, and runs an 8-way breadth-first-search alpha-contour slicer to extract animation frames with grounded bottom-center pivots. When your manual edit throws a `RUNTIME_ERROR` over WebSocket, the **Runtime Doctor** agent catches the Lua stack trace, generates a targeted AST hunk patch (`HOT_PATCH`), and hot-reloads the fixed script in under two seconds (`14.3 ms` median fixture latency) without resetting your playtest session.
- **Output**: A live 60 FPS WebGL2 game synchronized simultaneously across your PC monitor and mobile PWA touch screen, exportable in one click as an Itch.io-ready HTML5 `.zip`, a standalone Windows `.exe` bundle, or a signed Android `.apk` injected in two seconds.

## Where It Stands & Next Steps

*Aether Engine* `v0.1.0` is **shipped** with all `61` planned specification features across Milestones `M1` through `M4` plus `M-Final` adversarial hardening marked `DONE`. On disk at `D:\Projects\AI Gamebuilder Engine`, the repository contains `835` non-vendor files (`4.84 MB` excluding `node_modules`) and `85,392` lines of code (`64,019` handwritten TypeScript, Lua, and HTML lines across `369` files, plus `21,373` compiled JavaScript lines in `dist/`). Verification covers `63` Vitest test and fixture files (`603+` unit, integration, and end-to-end tests passing across Tiers 1–5).

Next steps for `v0.2.0`:
- Add deterministic rollback netcode helpers on top of the existing Fastify WebSocket room relay so fast-twitch 2D brawlers require zero custom state-sync boilerplate.
- Expose visual shader-uniform sliders in `studio.html` for the built-in CRT curvature, scanline, and bloom post-processing passes.
- Publish the standalone HTML5 template player as an embeddable NPM micro-package for one-command static portfolio hosting.

## Under the Hood & Local Files

### Core Runtime, Rendering & 2.5D Subsystems
Before writing engine code, we built interactive HTML architecture evaluators (`backend_picker.html` and `runtime_picker.html`, recorded across `84` Unified Memory Bank decisions `M0633`–`M0717`) to benchmark runtime stacks:
- **Fastify 5.2 + Wasmoon Lua 5.4 VM**: The server binds `0.0.0.0:8080` with bidirectional `@fastify/websocket` state sync and file-watcher hot-reload. Client-side Lua 5.4 runs inside a `<200 KB` `wasmoon` WebAssembly sandbox using a `60 Hz` deterministic fixed-timestep accumulator and explicit `lua.global.close()` memory ceiling guards.
- **WebGL2 Instanced Sprite Batcher & Dual 2.5D Raycasters**: Dynamic quad batching renders `10,000+` sprites at `60+ FPS` in 1–2 draw calls with toggleable integer pixel snapping (`1x–4x`) or smooth filtering, trauma-decay camera shake, and GPU particles. Alongside 4-layer orthogonal and `2:1` diamond isometric tilemaps (with 47-tile bitmask autotiling, foot Y-sorting, BSP dungeons, and cellular automata caves), the engine includes two 2.5D software/WebGL raycasters: a *Wolfenstein 3D* DDA grid caster and a *DOOM*-style portal-sector renderer with variable floor and ceiling heights.
- **Spatial Hash + SAT 2D Physics**: Broadphase spatial hashing paired with Separating Axis Theorem collision resolution handles triggers, raycasts, and one-way platforms.

### Tri-Agent AI, ComfyUI Slicer & Zero-SDK APK Exporter
- **AST Symbol Graph & Multi-Provider LLM Adapter**: `luaparse` indexes every Lua hook, entity, and global symbol so the Architect, Coder, and Runtime Doctor agents exchange minimal structured diffs across local LM Studio (`127.0.0.1:1234`), Ollama (`127.0.0.1:11434`), Gemini, Claude, or OpenAI—plus deterministic offline Mock LLM fixtures for zero-cost CI runs.
- **ComfyUI Binary Preview & BFS Island Slicer**: Speaks ComfyUI's 8-byte binary WebSocket preview protocol, applies Euclidean retro palette quantization (`16` or `32` colors), and runs 8-way connected-component alpha labeling via `pngjs` to emit `.meta.json` animation sheets automatically.
- **Zero-SDK Android APK Injector**: Modifies Android binary XML manifests, injects Lua/asset payloads into a pre-built WebView APK template, and computes V1 JAR cryptographic signatures purely in Node.js in ~2 seconds (with an optional full Android Studio Gradle project generator).

### Key Local Files
- Architecture & Test Specs: [PROJECT.md](file:///D:/Projects/AI Gamebuilder Engine/PROJECT.md), [ORIGINAL_REQUEST.md](file:///D:/Projects/AI Gamebuilder Engine/ORIGINAL_REQUEST.md), [TEST_INFRA.md](file:///D:/Projects/AI Gamebuilder Engine/TEST_INFRA.md), [TEST_READY.md](file:///D:/Projects/AI Gamebuilder Engine/TEST_READY.md)
- Build & Test Configs: [package.json](file:///D:/Projects/AI Gamebuilder Engine/package.json), [tsconfig.json](file:///D:/Projects/AI Gamebuilder Engine/tsconfig.json), [vitest.config.ts](file:///D:/Projects/AI Gamebuilder Engine/vitest.config.ts)
- Compiled Server & Studio Workbench: [index.js](file:///D:/Projects/AI Gamebuilder Engine/dist/server/index.js), [studio.html](file:///D:/Projects/AI Gamebuilder Engine/dist/server/views/studio.html)
- Bundled Starter & Flagship Projects: [projects](file:///D:/Projects/AI Gamebuilder Engine/projects)
