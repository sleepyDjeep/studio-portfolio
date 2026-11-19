---
id: "stream-pack-chat-backend"
title: "Stream Pack Chat Relay & Backend"
subtitle: "Node relay and v1 event protocol that turn Twitch, Kick, YouTube, TikTok and bot traffic into one local WebSocket feed, with per-address rate limits and record/replay."
pillar: "01-ai-workflows"
entry_type: "workflow"
readiness: "shipped"
visibility: "main"
date_started: "2026-11-16"
date_updated: "2026-11-19"
tags:
  - "nodejs"
  - "websocket-relay"
  - "twitch-irc"
  - "event-protocol"
  - "rate-limiting"
  - "record-replay"
  - "streaming-backend"
metrics:
  - label: "Relay Source"
    value: "1,359 LOC"
  - label: "HTTP + WS Endpoints"
    value: "6 Routes"
  - label: "Ingest Budget"
    value: "20/s · burst 40"
  - label: "Protocol"
    value: "Envelope v1"
  - label: "Bridge Tests"
    value: "3 Suites"
media: []
diagram: "assets/diagrams/stream-pack-chat-backend.svg"
tech_stack:
  - "Node.js 20+ (ES modules)"
  - "ws WebSocket library"
  - "Twitch IRC over WSS (read-only)"
  - "JSONL event recording"
  - "GitHub Actions (bridge workflow)"
local_paths:
  - label: "Relay"
    path: "file:///D:/Projects/MarcoPoloLive/bridge/relay.mjs"
  - label: "Twitch IRC Adapter"
    path: "file:///D:/Projects/MarcoPoloLive/bridge/adapters/twitch_irc.mjs"
  - label: "Replay Tool"
    path: "file:///D:/Projects/MarcoPoloLive/bridge/replay.mjs"
  - label: "Bridge README & Protocol"
    path: "file:///D:/Projects/MarcoPoloLive/bridge/README.md"
  - label: "Platform Integration Spec"
    path: "file:///D:/Projects/MarcoPoloLive/docs/PLATFORM_INTEGRATION.md"
run_commands:
  - label: "Start the Relay"
    command: "cd \"D:\\Projects\\MarcoPoloLive\\bridge\" && npm install && npm start"
  - label: "Read a Real Twitch Channel (anonymous)"
    command: "cd \"D:\\Projects\\MarcoPoloLive\\bridge\" && TWITCH_CHANNEL=yourchannel npm run twitch"
  - label: "Record a Show"
    command: "cd \"D:\\Projects\\MarcoPoloLive\\bridge\" && RECORD=/tmp/show.jsonl npm start"
  - label: "Replay a Recording at Recorded Cadence"
    command: "cd \"D:\\Projects\\MarcoPoloLive\\bridge\" && node replay.mjs --file /tmp/show.jsonl"
  - label: "Run the Bridge Test Suites"
    command: "cd \"D:\\Projects\\MarcoPoloLive\\bridge\" && npm test"
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

The Stream Pack games never integrate with a streaming platform. They connect to one loopback WebSocket and read one JSON envelope. A small Node relay owns everything platform-specific: anonymous Twitch IRC, plain HTTP posts from Kick, YouTube or a phone, and the bots streamers already run (Streamer.bot, SAMMI, Firebot, Mix It Up). The result is one tested path from chat to gameplay, and platform churn stays inside an adapter instead of forcing a game rebuild.

That boundary matters for a shipped game. No OAuth token, client id or refresh flow lives inside the Godot binary; the Twitch adapter is deliberately read-only, so there is nothing to leak. The game can be handed to a host without platform secrets, and swapping Twitch for TikTok is a bridge change rather than a new build.

The relay also makes the games testable. The same `StreamLink` client consumes mock envelopes, a real relay feed and a recorded JSONL file, so a balance change can be replayed against identical audience behaviour instead of a fresh live show.

## Real Example: How It Works in Practice

- **Input**: A streamer with Streamer.bot already configured wants chat to drive *The Pull* without writing code. Their bot posts `{"user":"%user%","display":"%user%","text":"%message%"}` to `http://127.0.0.1:8787/event` on every message; the game connects to `ws://127.0.0.1:8787/game`.
- **What Happens**:
  1. The relay assigns an `id` if missing, caps chat text at 500 characters and usernames at 64, and rejects unknown shapes with `422` instead of forwarding them.
  2. A token bucket per client address admits events at `RELAY_RATE` (default 20/s) with a `RELAY_BURST` of 40. Over-budget events get `429 {"ok":false,"error":"rate limited"}` with `retry-after: 1`, and are never forwarded or recorded.
  3. Accepted events fan out to every connected game socket; a client whose send buffer is already large is skipped so one stalled socket cannot grow memory.
  4. `StreamLink` drops duplicate ids from a reconnect replay and hands the event to `Audience`, which turns chat text into seat votes on its next tick.
- **Output**: A live round driven entirely by an existing bot, with no game restart, no credentials in the game, and a bounded event rate even during a raid.

## Where It Stands & Next Steps

The bridge is **shipped** with the suite. `bridge/` is 1,359 lines across the relay, replay tool, Twitch adapter and three test suites, and `npm test` starts relays on free ports and checks the HTTP-to-WebSocket path, the ingest limits, and record/replay. CI installs the relay dependencies before the readiness gate so a clean checkout exercises the real socket path instead of skipping it.

What exists today: `POST /event` plus `/chat`, `/support` and `/control` aliases; `WS /game` and `WS /ingest`; `GET /health` and a manual chat page; dedupe by id; length caps; per-address token buckets; opt-in JSONL recording and cadence-preserving replay; optional `RELAY_TOKEN`; and a read-only Twitch adapter.

Next steps:
- Add Kick and YouTube adapters behind the same envelope, keeping each platform's parsing in one file.
- Add a hosted mode with per-stream tokens for streamers who do not run the game on the streaming PC.
- Extend replay with a compact summary (events, seats, votes) so balance runs can be compared without reading JSONL by hand.

## Under the Hood & Local Files

### Routes and the v1 Envelope

| Route | Purpose |
| --- | --- |
| `POST /event` | Universal ingest; any tool that can send JSON can drive the game |
| `POST /chat` `/support` `/control` | Same ingest with `type` implied |
| `WS /game` | The single socket every game client connects to |
| `WS /ingest` | Streaming ingest for adapters that prefer sockets |
| `GET /health` | `{ ok, protocol, games, mock }` |
| `GET /` | Manual chat box for testing |

One JSON object per event. `type` (`chat`, `support`, `presence`, `control`) is the only required discriminator; `v` is `1`; `id` provides dedupe; `user` is a stable platform id (`twitch:12345`) that seats and cooldowns key on; `display` is cosmetic; `text` is raw chat capped at 500 characters. Support events carry `amount`, `currency` and `kind`; control events carry `action` and `payload`.

### Ingest, Recording and Replay

- **Token bucket per address** on both `POST /event` and `WS /ingest`, so a reconnect loop or runaway adapter cannot flood the game. Defaults sit far above a real chat feed, and the recorder/replay fixtures still fit in one burst.
- **Opt-in recording** with `RECORD=<path>`: each accepted event becomes one JSON line `{"t": <ms>, "event": {...}}`. Rejected and oversized bodies are never recorded.
- **Replay (`bridge/replay.mjs`)**: validates the whole file first, prints `replay: line N: <reason>` and exits `1` before posting anything, then posts events in order at the recorded gaps. `REPLAY_URL`, `REPLAY_TOKEN` and `REPLAY_FAST=1` cover other relays, tokens and tests. The game can also mount a recording directly with `--replay=<file>`.

### Security and Failure Modes

- Binds `127.0.0.1` by default; `RELAY_TOKEN` adds `x-relay-token` or `?token=` when the port must be exposed.
- Chat text is treated as data: never evaluated, never rendered as markup, never used in a path or URL.
- If the relay is absent, `StreamLink` retries with backoff and the mock feed keeps the game playable; the shell reports link state so a mid-round stream drop degrades to "no votes" instead of a frozen round.
- [bridge/README.md](file:///D:/Projects/MarcoPoloLive/bridge/README.md) - endpoint table, envelope examples and the ten-minute bot integration.
- [PLATFORM_INTEGRATION.md](file:///D:/Projects/MarcoPoloLive/docs/PLATFORM_INTEGRATION.md) - per-platform paths, latency budget and the reasons the relay is not inside Godot.
