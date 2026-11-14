---
id: "unified-memory-bank"
title: "Unified Cross-System AI Memory Bank"
subtitle: "Zero-VRAM local vector database that synchronizes architectural decisions and coding preferences in real time across Antigravity IDE, CLI, LM Studio, and ComfyUI."
pillar: "01-ai-workflows"
entry_type: "workflow"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-16"
date_updated: "2026-11-12"
tags:
  - "lancedb"
  - "mcp-server"
  - "onnx-cpu"
  - "lm-studio"
  - "comfyui"
metrics:
  - label: "Stored Memories"
    value: "1,020"
  - label: "GPU VRAM Used"
    value: "0 MB"
  - label: "Source Code"
    value: "1,604 LOC"
  - label: "Live Surfaces"
    value: "4"
media:
  - src: "assets/concepts/unified-memory-bank.png"
    kind: "concept"
    caption: "Concept Preview: Zero-VRAM CPU ONNX embedding and LanceDB vector store synchronizing Antigravity IDE, CLI, LM Studio (:11234 proxy), and ComfyUI custom nodes."
diagram: "assets/diagrams/unified-memory-bank.svg"
tech_stack:
  - "Python 3.13"
  - "LanceDB"
  - "FastEmbed (bge-small-en-v1.5)"
  - "FastMCP"
  - "Starlette + Uvicorn"
local_paths:
  - label: "Memory Layer Source Package"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/memory_layer"
  - label: "LanceDB Vector Store"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/memory_db"
  - label: "ComfyUI Memory Node Pack"
    path: "file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/ComfyUI-Antigravity-Memory/memory_nodes.py"
run_commands:
  - label: "Search Memories via CLI"
    command: "agy-memory search \"Godot 4.7 shader rules\""
  - label: "Run Pytest Verification Suite"
    command: "cd \"C:\\Users\\ogreb\\.gemini\\antigravity\\memory_layer\" && pytest tests/ -v"
  - label: "Start LM Studio Memory Proxy"
    command: "memory-proxy"
memory_ids:
  - "b644fee1-6b23-47d4-89ae-8cfda8a78a28"
conversation_ids:
  - "208ecc92-ff99-4ead-b0aa-52e709a9e1c5"
  - "3dd9b4a5-c23f-4de2-a939-1f05526a1a3a"
---

## What It Is & Why It Matters

AI coding assistants, local chat models, and node-based image generators normally operate with total amnesia of one another. If we decide inside our code editor that a game uses a brass-and-slate color palette or targets Godot 4.7, neither LM Studio nor ComfyUI knows that rule five minutes later unless we paste prompts by hand. On August 16, 2026—day one of our studio—we built the Unified Memory Bank (`memory_layer`) so every local AI tool reads and writes to a single persistent brain.

The system stores architectural decisions, user preferences, reusable code patterns, and asset rules inside a local serverless LanceDB vector database (`memory_db`). Crucially, we engineered the embedding engine to run 100% on the CPU using ONNX Runtime (`BAAI/bge-small-en-v1.5`). Because vector indexing and similarity lookups consume `0 MB` of GPU VRAM, any agent can query or store memories mid-render without stealing a single megabyte from ComfyUI SDXL graphs, LM Studio weights, or Godot Vulkan viewports.

Four live integration surfaces connect directly to this single store: an MCP stdio server for Antigravity IDE, the `agy-memory` developer CLI, a transparent OpenAI-compatible HTTP reverse proxy on port `11234` for LM Studio clients, and three custom graph nodes inside ComfyUI. An automatic semantic deduplicator (`>= 0.95` similarity threshold) updates existing records in place rather than piling up near-identical notes.

## Real Example: How It Works in Practice

- **Input**: During an LM Studio benchmark session, we establish a hardware rule: cap local 7B/8B models at `16,384` context tokens to avoid Windows WDDM shared-RAM spillover on our 8 GB RTX 4060 GPU. Later, a local Python script sends a chat request to `http://127.0.0.1:11234/v1/chat/completions` asking how to configure a local coding model.
- **What Happens**:
  1. **Capture & Deduplicate**: Antigravity calls `store_memory` via FastMCP (`mcp_server.py`). `MemoryManager` embeds the text into a 384-float vector on CPU, checks LanceDB for existing records in the same `(scope, workspace)` with `similarity >= 0.95`, and commits a clean `project_decision` UUID record.
  2. **Transparent Proxy Interception**: When the downstream client hits port `11234`, `proxy.py` intercepts the OpenAI payload, embeds the user's latest prompt on CPU, and queries LanceDB (`limit=3`).
  3. **Context Injection**: Hits scoring `similarity >= 0.55` are formatted into a `--- RELEVANT PERSISTENT MEMORIES ---` block and prepended to the `system` message before forwarding the stream to LM Studio on `127.0.0.1:1234`.
- **Output**: LM Studio streams back a Server-Sent Events (`text/event-stream`) response citing our exact `16,384`-token / `6.85 GB` VRAM ceiling automatically, with zero manual prompt copying and `0 MB` of extra GPU memory overhead.

## Where It Stands & Next Steps

The Unified Memory Bank is shipped and battle-tested in daily studio production. Across three months of work, it has accumulated `1,020` verified records (`1,604 LOC` across 17 Python modules) backed by `8` automated `pytest` suites testing CLI commands, workspace path normalization, in-place deduplication, ComfyUI node execution, and streaming proxy injection. In addition to the four core surfaces, our standalone `D:\LocalAssistant` ("AetherCore") imports `MemoryManager` directly in Python as a fifth live consumer.

Next steps to take it further:
- Add hybrid BM25 lexical + dense vector reciprocal-rank fusion so exact hex codes, port numbers, and file basenames rank alongside semantic concepts.
- Build a lightweight read-only web inspector tab inside the Studio Portfolio to browse memory timelines and category distributions visually.
- Add optional automatic TTL expiration for transient `task_context` entries while keeping `project_decision` and `user_preference` records permanent.

## Under the Hood & Local Files

### Architecture & Storage Design
- **LanceDB Schema (`db.py`)**: Serverless table `memories` storing `id` (UUID4), `text`, `vector` (`384`-dim float32), `category` (`user_preference | project_decision | code_pattern | task_context | general_fact`), `scope` (`global | workspace`), normalized forward-slash `workspace` path, `created_at`, `updated_at`, and `metadata_json`.
- **In-Place Semantic Deduplication (`core.py`)**: Converts LanceDB L2 `_distance` into normalized similarity via `1.0 / (1.0 + _distance)`. Any write scoring `>= 0.95` within the same `(scope, workspace)` updates the existing row and timestamp in place.
- **ComfyUI Custom Nodes (`memory_nodes.py`)**: Registers `AntigravityMemorySearch`, `AntigravityMemoryStore`, and `AntigravityMemoryFilter` directly inside ComfyUI's Python 3.13 runtime under `Antigravity/Memory`, letting image workflows pull art-direction rules straight into CLIP conditioning or write successful LoRA weights back to LanceDB.

### Key Local Files
- [pyproject.toml](file:///C:/Users/ogreb/.gemini/antigravity/memory_layer/pyproject.toml) — `uv_build` package manifest exposing `agy-memory`, `memory-mcp`, and `memory-proxy` console entrypoints.
- [core.py](file:///C:/Users/ogreb/.gemini/antigravity/memory_layer/src/memory_layer/core.py) — `MemoryManager` orchestration, scope filtering, and `>= 0.95` L2 similarity deduplication.
- [embeddings.py](file:///C:/Users/ogreb/.gemini/antigravity/memory_layer/src/memory_layer/embeddings.py) — Zero-VRAM CPU ONNX wrapper around FastEmbed `BAAI/bge-small-en-v1.5`.
- [proxy.py](file:///C:/Users/ogreb/.gemini/antigravity/memory_layer/src/memory_layer/proxy.py) — Async Starlette/Uvicorn reverse proxy (`127.0.0.1:11234` -> `:1234`) with SSE streaming and `>= 0.55` memory injection.
- [memory_nodes.py](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/ComfyUI-Antigravity-Memory/memory_nodes.py) — Custom ComfyUI node pack sharing live LanceDB access with the IDE and CLI.
- [SKILL.md](file:///C:/Users/ogreb/.gemini/config/skills/memory-layer/SKILL.md) — Global agent operating directive requiring pre-task memory search and post-decision persistence.
