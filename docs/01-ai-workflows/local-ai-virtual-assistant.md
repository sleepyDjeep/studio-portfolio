---
id: "local-ai-virtual-assistant"
title: "AetherCore Local AI Virtual Assistant"
subtitle: "Private, zero-cloud desktop web assistant running on localhost:8888 with 11 native tools, live DuckDuckGo search, PDF PII redaction, and shared LanceDB memory."
pillar: "01-ai-workflows"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-18"
date_updated: "2026-09-18"
tags:
  - "local-assistant"
  - "fastapi"
  - "websockets"
  - "lm-studio"
  - "pii-redaction"
  - "rag"
metrics:
  - label: "Source Code"
    value: "2,818 LOC"
  - label: "Native Agent Tools"
    value: "11"
  - label: "Test Suites"
    value: "2"
  - label: "Cloud API Calls"
    value: "0"
media:
  - src: "assets/media/local-ai-virtual-assistant/aethercore-studio.png"
    kind: "authentic"
    caption: "Live capture of AetherCore Local Assistant dark-studio web interface running on localhost:8888 with local tool-calling enabled."
diagram: ""
tech_stack:
  - "Python 3"
  - "FastAPI + WebSockets"
  - "LM Studio (Hermes-3 / Llama-3.1-8B)"
  - "DuckDuckGo Search (ddgs)"
  - "pypdf + BeautifulSoup4"
  - "Nomic Embeddings + LanceDB"
local_paths:
  - label: "LocalAssistant Root"
    path: "file:///D:/LocalAssistant"
  - label: "Projects Junction"
    path: "file:///D:/Projects/LocalAssistant"
run_commands:
  - label: "Launch AetherCore Web Studio"
    command: "\"D:\\LocalAssistant\\start_assistant.bat\""
  - label: "Run Automated Verification Suites"
    command: "cd \"D:\\LocalAssistant\" && python test_assistant.py && python test_tool_calling.py"
memory_ids: []
conversation_ids:
  - "eea204c0-133e-4519-896c-6e33f44faa95"
---

## What It Is & Why It Matters

Commercial chat interfaces lock live web browsing, PDF document analysis, file generation, and persistent memory behind monthly subscriptions while shipping every uploaded document to remote servers. On September 18, 2026, we built **AetherCore** (`D:\LocalAssistant`) to bring that entire tool-calling workflow onto our own hardware with zero cloud telemetry.

AetherCore pairs a custom dark-studio vanilla JavaScript frontend on `http://127.0.0.1:8888` with a FastAPI WebSocket backend (`/ws/chat`) connected to local 8B instruction models (`Hermes-3-Llama-3.1-8B` and `Meta-Llama-3.1-8B-Instruct`) served by LM Studio on port `1234`. Instead of acting as a passive text box, the assistant runs a multi-step autonomous tool loop across 11 native local capabilities—searching the live web via DuckDuckGo, scraping clean Markdown from articles, downloading files, running guarded shell commands, performing local vector RAG over workspace folders, and reading/writing our studio-wide LanceDB memory bank.

We also built a dedicated privacy shield directly into its document reader. Whenever AetherCore ingests a local PDF or text contract via `digest_document`, built-in regex scrubbers automatically mask Social Security numbers, phone numbers, email addresses, API keys, and custom user-supplied terms before the text ever enters the model's context window.

## Real Example: How It Works in Practice

- **Input**: Drop a multi-page PDF vendor agreement into `D:\LocalAssistant\documents\` and ask in the localhost:8888 chat UI: *"Summarize the termination clauses in this PDF with PII stripped, check live web benchmarks for standard notice periods, and save a clean Markdown brief to my workspace."*
- **What Happens**:
  1. **PII-Redacted PDF Ingestion**: `AssistantAgent` invokes `digest_document(filepath="vendor_agreement.pdf", redact_pii=True)`. `pypdf` extracts page text while regex filters replace SSNs (`[REDACTED_SSN]`), emails, phones, and `Bearer`/`sk-` secrets (`[REDACTED_SECRET]`), reporting the exact redaction count.
  2. **Live Web Research**: In the next turn of the tool loop, the model calls `web_search` via `ddgs` and `fetch_webpage` via `httpx` + `BeautifulSoup4` (stripping `<script>`, `<nav>`, and `<footer>` noise) to pull clean reference text.
  3. **Artifact Creation & Dock Sync**: The model calls `write_file` to save `termination_brief.md` inside `WORKSPACE_DIR`. FastAPI's `/api/files` endpoint immediately surfaces the new file with size and timestamp metadata in the UI's right-hand artifact dock for 1-click download.
- **Output**: A streaming Markdown breakdown in the WebSocket chat pane, a sanitized summary file (`termination_brief.md`) downloadable from the UI dock, and optional long-term rule storage in `~/.gemini/antigravity/memory_db`.

## Where It Stands & Next Steps

AetherCore is shipped and verified on disk at `D:\LocalAssistant` (mirrored via NTFS junction at `D:\Projects\LocalAssistant`), totaling `2,818 LOC` across 11 handwritten Python, JavaScript, CSS, HTML, and batch files (`494 KB` total footprint). Both automated verification suites—`test_assistant.py` and `test_tool_calling.py`—pass end-to-end against live LM Studio endpoints.

Next steps to expand the assistant:
- Add voice input/output hooks connecting our local Faster-Whisper STT and Kokoro TTS engines for hands-free desktop dictation.
- Persist Nomic document chunk embeddings in a dedicated LanceDB table inside `D:\LocalAssistant\documents` so large multi-PDF folders do not re-embed on every `rag_search` call.
- Add a one-click VRAM unload button in the top status bar (`POST` to LM Studio management CLI) before launching heavy ComfyUI or Godot Vulkan sessions.

## Under the Hood & Local Files

### Architecture & 11-Tool Registry
- **Backend & Health Caching (`server.py`)**: FastAPI app serving static assets, `/ws/chat` bi-directional token/tool streaming, `/api/files` workspace artifact browser, and a 10-second cached `/api/status` probe monitoring LM Studio model readiness and LanceDB memory counts.
- **Autonomous Tool Loop (`agent.py` & `tools.py`)**: Exposes OpenAI-schema function definitions for 11 tools:
  1. `web_search` (live DuckDuckGo text search)
  2. `fetch_webpage` (HTML-to-clean-text scraper with 4,000-char windowing)
  3. `download_file` (streaming `httpx` downloader to `DOWNLOADS_DIR`)
  4. `read_file` / 5. `write_file` / 6. `list_directory` (sandboxed workspace I/O)
  7. `digest_document` (`pypdf` + regex PII/token redactor)
  8. `run_shell` (30s timeout `subprocess.run` blocking destructive `format`/`rd` commands)
  9. `search_memory` / 10. `store_memory` (direct `MemoryManager` bridge to studio LanceDB)
  11. `rag_search` (paragraph chunker + local LM Studio `/embeddings` cosine search)

### Key Local Files
- [server.py](file:///D:/LocalAssistant/server.py) — FastAPI + WebSocket server, `/api/status` health cache, and `/api/files` artifact dock endpoints.
- [agent.py](file:///D:/LocalAssistant/agent.py) — Multi-turn LM Studio chat and tool-execution state machine.
- [tools.py](file:///D:/LocalAssistant/tools.py) — Implementation and JSON schemas for all 11 local tools, PII regex scrubbers, and LanceDB memory bridge.
- [index.html](file:///D:/LocalAssistant/static/index.html) — Dark-studio web interface paired with [app.js](file:///D:/LocalAssistant/static/app.js) and [style.css](file:///D:/LocalAssistant/static/style.css).
- [test_assistant.py](file:///D:/LocalAssistant/test_assistant.py) & [test_tool_calling.py](file:///D:/LocalAssistant/test_tool_calling.py) — End-to-end API and tool-invocation test suites.
