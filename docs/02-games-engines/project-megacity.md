---
id: "project-megacity"
title: "Project MegaCity: Anthil Metropolis — Dystopian Minecraft RPG Server"
subtitle: "Judge Dredd-inspired cyberpunk multiplayer RPG server on Minecraft 1.20.1 Forge with 42 Lua city-terminal scripts, 6 procedural arcologies, and CGNAT tunnel routing."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-10-06"
date_updated: "2026-10-07"
tags:
  - "minecraft-forge"
  - "multiplayer-rpg"
  - "lua-computercraft"
  - "worldbuilding"
  - "cyberpunk"
  - "networking"
metrics:
  - label: "Custom Source Code"
    value: "10,817 LOC"
  - label: "Lua City Terminals"
    value: "42 Scripts"
  - label: "City Footprint"
    value: "435 Buildings + 6 Arcologies"
  - label: "Client Modpack"
    value: "93 MB ZIP"
  - label: "World Bible"
    value: "30 Design Pillars"
media:
  - src: "assets/media/project-megacity/anthil-pitch-deck.png"
    kind: "authentic"
    caption: "Interactive HTML executive pitch deck for Project MegaCity: Anthil Metropolis (Minecraft 1.20.1 Forge RPG server)."
diagram: ""
tech_stack:
  - "Minecraft 1.20.1 (Forge 47.3.0)"
  - "Lua (CC:Tweaked & KubeJS)"
  - "Python 3 Schematic Generators"
  - "Playit.gg & Cloudflare DNS SRV"
  - "HTML5 / CSS / JS Pitch Deck"
local_paths:
  - label: "ProjectMegaCity Root"
    path: "file:///D:/ProjectMegaCity"
  - label: "Interactive HTML Pitch Deck"
    path: "file:///D:/ProjectMegaCity/PITCH_DECK_ANTHIL_METROPOLIS.html"
  - label: "Executive PDF Pitch Packet"
    path: "file:///D:/ProjectMegaCity/Anthil_Metropolis_Pitch_Packet.pdf"
run_commands:
  - label: "Open Interactive Pitch Deck"
    command: "cmd /c start \"\" \"D:\\ProjectMegaCity\\PITCH_DECK_ANTHIL_METROPOLIS.html\""
  - label: "Start Forge 1.20.1 RPG Server"
    command: "\"D:\\ProjectMegaCity\\START_SERVER.bat\""
  - label: "Start Playit.gg CGNAT Public Tunnel"
    command: "\"D:\\ProjectMegaCity\\START_PLAYIT_TUNNEL.bat\""
memory_ids:
  - "cdf472dc-06df-4a0b-8d7a-f88c35671971"
  - "78eedd4c-53c1-4b0b-b67a-c28e2c48be67"
  - "bcb3069e-659e-4fef-9a70-70472daf2a28"
  - "ed7120e0-ca11-4c3b-8d21-ba151954180d"
  - "a459588b-53df-4361-a20a-42d20623143e"
  - "f6005177-d06b-4b6f-a3b5-a77bbfae9f05"
  - "c240aef4-a04c-4d0a-a051-960498704c20"
  - "424bbb39-9bf7-4984-9c71-96b3f7c10e4b"
  - "d12f218e-a762-4da4-a237-37a937eb74a9"
  - "d494dfaf-a023-4e86-95f3-20e776461a58"
  - "ba7f6659-59d8-4e0f-b6ea-92199bb1f135"
  - "504664ed-52f3-4a05-9c21-29210517e9de"
  - "02a5f711-fcda-441f-a7cb-e7d3b8bcca73"
  - "54f49f2e-f6f9-40ce-b29c-981d5e1a747d"
  - "fe9f4bce-058f-448e-8493-d200c2befe03"
  - "0c246065-619f-4fd8-9d9b-5948573d68cd"
  - "64b01bd6-0f97-4847-a9d3-bd97fbeaadc3"
  - "5995606a-82be-49c2-9773-7766e4a51dcc"
  - "3ebf4498-1fbe-4673-991b-9e528c5546d2"
  - "44867bab-caa9-4cb3-b052-7799738b29ec"
  - "6bf4de6e-ee5a-447e-bd79-22e66d2ec51d"
conversation_ids:
  - "e95a171a-a23f-4de0-abbd-d86414c56804"
  - "147bf757-e03a-4480-8f50-b2e3c46c2b81"
---

## What It Is & Why It Matters

*Project MegaCity: Anthil Metropolis* turns Minecraft 1.20.1 Forge into a grimdark, *Judge Dredd*-meets-*Cyberpunk* vertical arcology RPG server hosted straight from our local workstation without monthly cloud-server bills or residential router port-forwarding. Players inhabit a 435-building metropolis split across three vertical class strata—corporate *Upper Spires*, overcrowded *Sector Hab-Blocks*, and irradiated *Sump Slums*—choosing allegiances between **Street Judges**, **Block Barons**, and **Sump Mutants** with custom ballistic firearms, cybernetic limb implants, wall-running parkour, physical coin economies, and Lua-driven law-enforcement terminals.

Ambitious modded multiplayer servers usually collapse before launch for three reasons: vague lore that leaves builders guessing, bloated client modpacks that stutter on mid-range GPUs, and residential ISP Carrier-Grade NAT (`CGNAT`) blocking incoming player connections. We solved all three in a single 48-hour sprint—locking a 30-pillar Master World Bible and 10-slide interactive executive pitch deck first, curating a high-FPS `93 MB` Embeddium/FerriteCore client bundle, generating six monumental WorldEdit `.schem` megatowers via Python, and routing public traffic through a `Playit.gg` tunnel bound to a clean Cloudflare DNS `SRV` domain (`mc.vectorfeedhq.com`).

## Real Example: How It Works in Practice

- **Input**: You launch `START_SERVER.bat` and `START_PLAYIT_TUNNEL.bat` on the host machine, hand a friend `ProjectMegaCity_Client_Modpack.zip` plus the interactive `PITCH_DECK_ANTHIL_METROPOLIS.html` briefing, and have them connect in Minecraft 1.20.1 to `mc.vectorfeedhq.com` as a newly inducted Street Judge patrolling Sector-01 Hab-Block.
- **What Happens**: Cloudflare's `SRV` record resolves `mc.vectorfeedhq.com` transparently to the active `Playit.gg` tunnel endpoint without exposing home IP addresses or opening residential firewall ports. Inside the `313 MB` *Anthil* world map, `42` custom Lua scripts (`8,414` LOC across `CC:Tweaked` terminals and server hooks) drive Warrant/Wanted dispatch boards, sector lockdown bulkheads, and vending kiosks backed by `Lightman's Currency`. Drawing a `TAC:Z` firearm (configured with multi-mode Judge *Lawgiver* ballistics) while vaulting across neon skybridges via `ParCool` and `Cyberware` implants triggers dynamic faction reputation shifts and wanted-level responses from `CustomNPCs` patrols.
- **Output**: A self-hosted, low-latency multiplayer cyberpunk RPG city server with bundled JDK 17 runtime, 1-click world swap/restore batch tools (`LOAD_ANTHIL_AS_SERVER_WORLD.bat`), a distributable `93 MB` client modpack, and a presentation-ready HTML + PDF investor/community pitch kit.

## Where It Stands & Next Steps

*Project MegaCity* is **shipped** and self-contained on disk at `D:\ProjectMegaCity` (`1,052` files, `1.84 GB` total footprint). Handwritten code spans `10,817` lines across `73` files (`42` `.lua` city-system scripts totaling `8,414` LOC, `17` Python schematic and modpack automation scripts totaling `912` LOC, `1` `1,167`-line interactive HTML5 pitch deck, and `13` PowerShell/Batch server orchestration scripts), alongside `34` Markdown lore and architecture documents, `1,344` `.ogg` custom audio assets, `Anthil_Cyberpunk_City.zip` (`313 MB`), and `ProjectMegaCity_Client_Modpack.zip` (`93 MB`).

Next steps for Season 1 live community play:
- Paste the six Python-generated WorldEdit `.schem` megatowers (*Hall of Justice*, *Sector-01 Hab-Block*, *OmniCorp Arcology*, *Neon Slums Market*, *Sump Refinery*, and *Mag-Lev Station*) into outer ring expansion plots and wire `FTB Quests` onboarding chapters inside each lobby.
- Add automated nightly incremental world backups from `D:\ProjectMegaCity\Server` to cold archive storage with a 7-snapshot rolling retention window.
- Publish a PrismLauncher / Modrinth `.mrpack` manifest alongside `ProjectMegaCity_Client_Modpack.zip` for automatic client updates.

## Under the Hood & Local Files

### Modpack Stack, Procedural `.schem` Builders & CGNAT Networking
Documented across `21` Unified Memory Bank entries (`M0921`–`M0941`) and sessions `C111`–`C112`:
- **Performance-Hardened Forge 1.20.1 Stack (`Client_Staging/mods/`)**: Pairs heavy systemic gameplay mods (`TAC:Z` firearms, `Cyberware` / `Robotic Parts`, `Create`, `Immersive Engineering`, `CustomNPCs`, `ParCool`, `Lightman's Currency`, `FramedBlocks`, `Effortless Building`, `Simple Voice Chat`) with aggressive client/server memory and frame-time optimizers (`Embeddium 0.3.31`, `ModernFix 5.27.85`, `FerriteCore 6.0.1`).
- **Python WorldEdit `.schem` Megastructure Generators (`Tools/` & `Schematics/`)**: `17` Python automation scripts procedurally generate multi-floor brutalist arcology shells, neon signage ribs, interior atrium shafts, and block palettes directly into Sponge/WorldEdit `.schem` binary NBT files.
- **42-Script Lua City OS**: Powers diegetic green/amber `CC:Tweaked` computer terminals across Judge precinct desks, citizen ID checkpoints, bounty terminals, and automated transit gates.
- **Zero-Port-Forward Tunneling**: Combines local `playit.exe` TCP tunneling with a Cloudflare `_minecraft._tcp.mc.vectorfeedhq.com` `SRV` record so players join a clean memorable hostname despite ISP CGNAT restrictions.

### Key Local Files
- Executive Pitch & Lore Suite: [PITCH_DECK_ANTHIL_METROPOLIS.html](file:///D:/ProjectMegaCity/PITCH_DECK_ANTHIL_METROPOLIS.html), [Anthil_Metropolis_Pitch_Packet.pdf](file:///D:/ProjectMegaCity/Anthil_Metropolis_Pitch_Packet.pdf), [PITCH_DECK_SUMMARY.md](file:///D:/ProjectMegaCity/PITCH_DECK_SUMMARY.md)
- Server & Tunnel Launchers: [START_SERVER.bat](file:///D:/ProjectMegaCity/START_SERVER.bat), [START_PLAYIT_TUNNEL.bat](file:///D:/ProjectMegaCity/START_PLAYIT_TUNNEL.bat), [LOAD_ANTHIL_AS_SERVER_WORLD.bat](file:///D:/ProjectMegaCity/LOAD_ANTHIL_AS_SERVER_WORLD.bat), [RESTORE_ORIGINAL_SERVER_WORLD.bat](file:///D:/ProjectMegaCity/RESTORE_ORIGINAL_SERVER_WORLD.bat)
- Distributable World & Client Archives: [Anthil_Cyberpunk_City.zip](file:///D:/ProjectMegaCity/Anthil_Cyberpunk_City.zip), [ProjectMegaCity_Client_Modpack.zip](file:///D:/ProjectMegaCity/ProjectMegaCity_Client_Modpack.zip)
- Mod Staging, Schematics & Automation Tools: [Client_Staging](file:///D:/ProjectMegaCity/Client_Staging), [Schematics](file:///D:/ProjectMegaCity/Schematics), [Server](file:///D:/ProjectMegaCity/Server), [Tools](file:///D:/ProjectMegaCity/Tools)
