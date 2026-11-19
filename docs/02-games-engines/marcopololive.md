---
id: "marcopololive"
title: "MarcoPoloLive: Seven-Game Streamer Game Suite"
subtitle: "Godot 4.7 suite where six chat teams and one blindfolded streamer play seven shared-audience mini games under one intermission shell, packaged as reproducible Windows, Linux and macOS releases."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-11-16"
date_updated: "2026-11-19"
tags:
  - "godot-4-7"
  - "streaming-games"
  - "game-suite"
  - "broadcast-overlay"
  - "spatial-audio"
  - "reproducible-builds"
  - "ci-cd"
metrics:
  - label: "Shipped Games"
    value: "7 in One Suite"
  - label: "GDScript"
    value: "20,567 LOC"
  - label: "Release Targets"
    value: "5 (Win/Linux/macOS)"
  - label: "Commits in 3 Days"
    value: "86"
  - label: "Broadcast Layouts"
    value: "16:9 + 9:16"
media:
  - src: "assets/media/marcopololive/broadcast-layout.png"
    kind: "authentic"
    caption: "Live Marco Polo broadcast frame: top-down pool with six swimmers and the blind hunter, first-person inset, six-team roster and the chat ticker on the right rail."
diagram: "assets/diagrams/marcopololive-stream-pack.svg"
tech_stack:
  - "Godot 4.7 (Forward+)"
  - "GDScript"
  - "GitHub Actions (Linux xvfb + macOS)"
  - "Bash release packaging"
local_paths:
  - label: "MarcoPoloLive Project Root"
    path: "file:///D:/Projects/MarcoPoloLive"
  - label: "Game Registry"
    path: "file:///D:/Projects/MarcoPoloLive/games/games.json"
  - label: "Release Build Script"
    path: "file:///D:/Projects/MarcoPoloLive/dev/build_release.sh"
  - label: "Readiness Gate"
    path: "file:///D:/Projects/MarcoPoloLive/dev/run_preflight_matrix.sh"
  - label: "Chat Backend & Relay (companion entry)"
    path: "file:///D:/Projects/MarcoPoloLive/bridge/relay.mjs"
run_commands:
  - label: "Play the Suite Through the Launcher"
    command: "cd \"D:\\Projects\\MarcoPoloLive\" && node dev/play.mjs"
  - label: "Run a Specific Game in 9:16"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\MarcoPoloLive\" -- --game=the_pull --layout=9:16"
  - label: "Build a Reproducible Windows Release"
    command: "cd \"D:\\Projects\\MarcoPoloLive\" && GODOT=\"D:/SteamFiles/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe\" bash dev/build_release.sh"
  - label: "Verify Two Exports Are Byte-Identical"
    command: "cd \"D:\\Projects\\MarcoPoloLive\" && GODOT=\"D:/SteamFiles/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe\" bash dev/build_release.sh --check"
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

MarcoPoloLive is a game suite, not a single title. Marco Polo leads it: the streamer is blindfolded and hunts six chat-controlled swimmers by directional audio alone. Six more games reuse the same six-seat audience, the same scoring language and the same broadcast shell: *The Pull* drags the streamer's body across a disc, *The Architect* lets chat build a death course, *The Volley* turns six reticles into a shared aiming problem, *What Time Is It?* is a wolf-and-stealth timing game, *The Impression* is typed charades, and *Mother, May I?* is a permission economy.

That shared layer is the reason the suite works as a show. Seats persist across games, votes normalize so a 100-viewer team and a three-viewer team pull with the same maximum force, and every game reports its own metric instead of a shared point total. Between rounds the shell freezes the finished game and shows an intermission card with the result, per-game records, team form and a `!vote` for the next title, so a streamer can hand an hour to chat without teaching a new rule set each round.

The chat and relay side is documented separately in **Stream Pack Chat Relay & Backend**, because it is replaceable on its own: the games speak one WebSocket protocol and never learn that Twitch, Kick or a bot exists.

## Real Example: How It Works in Practice

- **Input**: A host starts `play.cmd` before a show. Chat is on Twitch, the layout is 9:16 for a TikTok restream, and the first round is *The Pull* with a five-round series.
- **What Happens**:
  1. The launcher starts the local relay, waits for its port, then launches the packaged game and stops the relay when the game exits.
  2. The shell loads `games/games.json`, mounts `the_pull.tscn`, seats viewers into six teams, rotates seats one team along at round start, and passes votes into the game's real `Audience` model.
  3. The game awards points by its own metric; the shell writes the completed round to `user://stream_pack_history.json` through a temporary file and a `.bak` copy, then shows the intermission card with the series standing and the next-game vote.
  4. `--layout=9:16 --capture-output` opens the portrait frame at the full 1080 x 1920 canvas, so OBS captures a native source instead of an upscaled preview.
- **Output**: A five-round show with six seated teams, a live chat-driven round, persisted history, a ranked series card and a portrait feed that never left the game process.

## Where It Stands & Next Steps

The suite is **shipped**: seven games, a streamer console, preflight and rehearsal modes, and packaged releases for Windows, Linux and macOS. The repository (`github.com/sleepyDjeep/marco-polo-live`) went from its first commit on 2026-11-16 to 86 commits by 2026-11-18. On disk it is 56 GDScript files and 20,567 LOC, plus the dev harnesses that drive every game to its end condition headlessly.

Verification that exists today: a strict zero-leak audio check, a nine-mode readiness gate under xvfb with software Mesa, the OBS window smoke test that asserts sizes, borderless flags and on-screen positions, the legibility probe at 16:9 and 9:16, and a deprecation ledger check. CI installs the pinned Godot 4.7.2 and its export templates, so packaging runs on the runner instead of skipping.

Next steps:
- Complete a real two-hour Twitch show and record the first human playtest notes for the remaining games.
- Add VR audience input, the one item still marked planned in the feature table.
- Ship a second locale through the existing `tr()` key catalog once the English label-fit gate is stable.

## Under the Hood & Local Files

### Shared Audience and Broadcast Shell

- **One audience model (`addons/stream_pack/audience.gd`)**: six seats, join and team commands, vote cooldowns, command grammar and team lock during rounds. Seat rotation is on by default and its phase is persisted with each round, so a relaunch resumes the cycle instead of resetting everyone to Team 1.
- **Two frames, one simulation (`broadcast_output.gd`)**: `--dual-output` opens a second native window with its own reflowed HUD and arena camera; the secondary window is unfocusable so keyboard play stays on the primary. `--capture-output` removes preview scaling for OBS.
- **Intermission and series**: the shell holds a championship card, computes standings as each team's average share of the points available per round, shows `SERIES DRAWN` on a dead heat, and keeps seasons across restarts with `--season=<tag>`.
- **History and export**: `stream_pack_history.json` is capped at 5,000 rounds, keeps all-time records separately, and is written atomically with a backup. The console's **EXPORT** writes JSON and CSV to `user://exports`; rows never contain platform user ids, display names or chat messages.
- **Localisation gate**: every card, console and preflight string resolves through `addons/stream_pack/strings.gd` and `locale/en.po`. The legibility probe mounts the card and panels with real content, checks each label's minimum text size against its room at both layouts, and requires every catalog key to resolve through the registered translation.

### Release and CI Pipeline

- **Five export targets (`dev/build_release.sh`)**: Windows, Linux, macOS universal `.app` plus DMG, and single-file Windows/Linux builds with the pack embedded. Each target is byte-reproducible; `--check` exports twice and compares hashes, including a digest over the macOS bundle's sorted file hashes. `BUILD.txt` records engine version, commit, sha256 and sizes.
- **Boot proof**: the script boots the host artifact headless from a directory containing only that artifact and requires a round to start and the process to exit clean. The macOS DMG is mounted read-only and must contain the app bundle and the Applications shortcut; signing and notarization run from optional `MACOS_*` secrets and record `SKIPPED` when absent instead of claiming success.
- **Readiness gate**: packages the host's sidecar and single-file releases plus macOS on every run, runs the reproducibility check, the leak and harness runs, the relay round trip and the window smoke test. The Linux parse job has a 25-minute budget because packaging now lives inside it.
- [README.md](file:///D:/Projects/MarcoPoloLive/README.md) - feature table, controls for all seven games and packaging notes.
- [games.json](file:///D:/Projects/MarcoPoloLive/games/games.json) - registry rows with per-game layouts, streamer keys and chat verbs.
