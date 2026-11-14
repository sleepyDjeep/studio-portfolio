---
id: "techwriter-publishing-studio"
title: "TechWriter: Zero-Dependency Micro-Guide Publishing Studio"
subtitle: "Local Python stdlib research, demand-kill validation, hazard scanning, and multi-marketplace packaging studio for printable technical reference guides."
pillar: "03-ventures-saas"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-05"
date_updated: "2026-09-20"
tags:
  - "digital-publishing"
  - "local-llm"
  - "fact-checking"
  - "zero-dependency-python"
  - "human-in-the-loop-qa"
  - "printable-guides"
metrics:
  - label: "Handwritten Codebase"
    value: "8,001 LOC (0 pip Packages)"
  - label: "Pipeline Architecture"
    value: "Stages 0–6 + 3 Human QA Stops"
  - label: "Seeded Niche Pipelines"
    value: "7 Verticals (2 Packaged)"
  - label: "Release Bundles Built"
    value: "EPUB + 4 Marketplace ZIPs + HTML"
media:
  - src: "assets/media/techwriter-publishing-studio/studio-dashboard.png"
    kind: "authentic"
    caption: "Live capture of the zero-dependency TechWriter web control panel running locally on port 8766."
  - src: "assets/media/techwriter-publishing-studio/mini-painting-guide.png"
    kind: "authentic"
    caption: "Fixed-layout printable reference guide generated and verified through TechWriter's accuracy gates."
diagram: ""
tech_stack:
  - "Python 3.13 Standard Library"
  - "LM Studio Local HTTP Inference"
  - "Qwen3-30B-A3B MoE Models"
  - "Fixed-Layout Print HTML & EPUB"
  - "Vanilla JS Dark Studio UI (:8766)"
local_paths:
  - label: "TechWriter Root"
    path: "file:///D:/TechWriter"
  - label: "Studio Junction"
    path: "file:///D:/Projects/TechWriter"
  - label: "Mini Painting Printable Guide"
    path: "file:///D:/TechWriter/guides/mini_painting/05_final/guide_fixed_layout.html"
  - label: "Bioactive Terrarium Marketplace Releases"
    path: "file:///D:/TechWriter/guides/bioactive_terrarium/06_publishing"
run_commands:
  - label: "Launch Web Studio (:8766)"
    command: "\"D:\\TechWriter\\run_app.bat\""
  - label: "List Niche Registry & Status"
    command: "cd \"D:\\TechWriter\" && python -m guide.orchestrator list"
  - label: "Run Hazard & Claim Scanner"
    command: "cd \"D:\\TechWriter\" && python -m guide.orchestrator scan --file guides/mini_painting/03_drafts/full_draft.md"
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

Printable technical micro-guides and benchtop cheat sheets fail on factual wrongness, never on prose style. If a fiction paragraph hallucinates a minor detail, nobody notices; if a hardware restoration or chemistry cheat sheet invents a curing ratio or battery recovery step, it ruins equipment or starts a fire. We built **TechWriter** (`D:\TechWriter`, running locally on port `:8766` against LM Studio) to turn local open-weight models into a disciplined, source-cited technical publishing line with zero third-party Python dependencies.

Most AI publishing scripts optimize for unattended volume: pick a keyword, generate 40 pages in one pass, and upload. TechWriter flips that incentives loop upside down. Stage 0 exists specifically to **kill weak product ideas** before a single outline is drafted. A candidate niche cannot advance unless it clears four non-negotiable arithmetic checks: documented user pain across at least 8 distinct problem clusters, clear superiority over free online calculators or wikis, proof that buyers already pay for adjacent guides, and manageable physical liability. During testing, `sim_racing` scored highest on raw hobbyist enthusiasm—and Stage 0 killed it outright because six free interactive setup calculators already beat any static printable PDF.

Even after a niche earns a `BUILD` verdict, automated Python code cannot advance past `QA Stop 1` (market validation), `QA Stop 2` (claim-by-claim source and expert accuracy audit), or `QA Stop 3` (marketplace disclosure and pre-launch check). Every numeric measurement requires two independent cited sources, and every draft passes through a deterministic physical-hazard scanner before human eyes ever review layout spreads.

## Real Example: How It Works in Practice

- **Input**: Thirty real beginner and intermediate community troubleshooting posts harvested into the `mini_painting` or `bioactive_terrarium` workspace, competitor product listings, and curated primary reference extracts.
- **What Happens**:
  1. **Stage 0 (Harvest & Arithmetic Verdict)**: Python deduplicates the harvested posts by source ID while the local `Qwen3-Coder-30B-A3B-Instruct` model *proposes* problem groupings without writing to the official worksheet. The human operator assigns final theme counts (preventing an eager LLM from merging two weak topics to fake the 8-theme threshold), fills in competitor gap notes, and runs `validation.verdict()`.
  2. **Stage 1–2 (Spread Outlining & Two-Source Drafting)**: Once the operator clicks `QA Stop 1` approval (`RunState.mark()` throws an exception if code tries to mark human stops automatically), TechWriter plans 12 to 14 fixed-layout spreads plus a 1-page printable benchtop quick-reference sheet, tagging any unverified measurement with `[NEEDS SOURCE]` until backed by two independent citations.
  3. **Stage 3 (Deterministic Safety & Claim Audit)**: `safety.py` scans every spread against blocked hazard patterns—built after an internal 17-model benchmark caught three separate local LLMs recommending opening and re-electrolyting lithium-ion cells, an acute fire hazard relevant to `retro_handheld` guides. Medium- and high-liability guides block packaging until a formal expert-review JSON record is logged and `QA Stop 2` is signed off.
  4. **Stage 4–6 (Packaging, Honest Disclosure & Metrics)**: The bundler compiles print-ready fixed-layout HTML spreads, 1-page reference cards, `.epub` ebooks, marketplace `.zip` kits, and an explicit `ai_mode: generated` disclosure file matching Amazon KDP and Etsy's August 11, 2026 rules.
- **Output**: Verified, ready-to-list release artifacts on disk—including `guides/mini_painting/05_final/guide_fixed_layout.html` and `quick_reference.html`, plus `guides/bioactive_terrarium/05_final/bioactive_terrarium.epub` and four platform-specific release archives (`etsy_release.zip`, `kdp_release.zip`, `lemonsqueezy_release.zip`, and `payhip_release.zip`).

## Where It Stands & Next Steps

TechWriter is **shipped** and verified across all seven pipeline stages (`00_validation` through `06_publishing`) at `D:\TechWriter` (mirrored via NTFS junction at `D:\Projects\TechWriter`). The entire application—12-tab dark web control panel (`app/index.html` + `local_workflow_web.py` on `127.0.0.1:8766`), CLI orchestrator (`guide/orchestrator.py`), LLM role router, and safety scanner—runs in **8,001 lines of pure Python 3 standard library and vanilla HTML/JS** (`0` `pip` packages, `0` build steps). Seven niche workspaces are seeded (`mini_painting`, `bioactive_terrarium`, `retro_handheld`, `ai_character_consistency`, `cosplay_patterns`, `mushroom_cultivation`, and the killed `sim_racing` benchmark), with end-to-end packaged builds completed for both `bioactive_terrarium` and `mini_painting`.

Concrete next steps to take the first retail SKU live:
- **Wire UI Call Sites for Interactive Source & Spread Editing**: Connect the written `prompts.spread_prompt()`, `prompts.claim_check_prompt()`, and `safety.can_package()` functions directly to interactive per-spread buttons inside the Draft and Accuracy web tabs so operators never drop down to CLI commands mid-book.
- **Lock Print-to-PDF Toolchain**: Decide between keeping the zero-pip mandate via automated headless Chromium print-to-PDF (`A4` + `US Letter` CSS `@page` rules) or adding an isolated `ReportLab` / `WeasyPrint` export helper.
- **Publish Niche #1 (`mini_painting`) on Payhip / Lemon Squeezy**: Run a fresh 30-post manual paste harvest (respecting Reddit's commercial API terms documented in `docs/DECISIONS.md`), release the 1-page printable quick-reference card as a free attribution lead magnet, and list the complete fixed-layout guide.

## Under the Hood & Local Files

### Engineering Decisions & Local Model Governance

- **100% Python Standard Library Constraint**: Every HTTP server route, YAML/JSON state parser, LM Studio client, and ZIP/EPUB packager uses built-in Python 3 modules. Cloning the folder onto any Windows machine and clicking `run_app.bat` boots the full studio immediately without virtual-environment rot.
- **Measured Model Blacklist (`README.md` & `config.yaml`)**: Rather than trusting leaderboard scores, we routed roles (`research`, `structure`, `draft`, `editor`) based on empirical failure testing across 17 local models. Three popular models are permanently banned in code comments and config: `google/gemma-3-4b` (fluent prose that answered unasked questions and gave lithium-fire battery advice), `merlin-research_merlin-agent` (hallucinated high confidence while confusing lithium dendrites with PCB corrosion), and `qwen/qwen3.5-9b` (exhausted 100% of token budgets inside reasoning tags with zero output).
- **Zero-Leak Localhost Credential Isolation**: Because `GET /api/config` sends `config.yaml` to the browser UI, API keys are architecturally barred from `config.yaml` and stored exclusively in gitignored `guide/credentials.json` (or environment variables), with the server reporting only boolean presence (`true`/`false`) to the frontend.

### Local Directory & Key Clickable Files

- **Studio Root**: [TechWriter](file:///D:/TechWriter) (`230` files, `949 KB` total footprint)
- **Architecture, Decisions & Handoff Notes**: [README.md](file:///D:/TechWriter/README.md), [HANDOFF.md](file:///D:/TechWriter/HANDOFF.md), [00_BUILD_PLAN.md](file:///D:/TechWriter/docs/00_BUILD_PLAN.md)
- **Web Server & CLI Entrypoints**: [run_app.bat](file:///D:/TechWriter/run_app.bat), [local_workflow_web.py](file:///D:/TechWriter/local_workflow_web.py), [orchestrator.py](file:///D:/TechWriter/guide/orchestrator.py)
- **Validation, Gate & Hazard Modules**: [validation.py](file:///D:/TechWriter/guide/validation.py), [safety.py](file:///D:/TechWriter/guide/safety.py), [stages.py](file:///D:/TechWriter/guide/stages.py), [data.py](file:///D:/TechWriter/guide/data.py), [prompts.py](file:///D:/TechWriter/guide/prompts.py)
- **Packaged Guide Deliverables**:
  - [mini_painting Fixed-Layout Guide](file:///D:/TechWriter/guides/mini_painting/05_final/guide_fixed_layout.html)
  - [mini_painting 1-Page Quick Reference](file:///D:/TechWriter/guides/mini_painting/05_final/quick_reference.html)
  - [bioactive_terrarium EPUB](file:///D:/TechWriter/guides/bioactive_terrarium/05_final/bioactive_terrarium.epub)
  - [bioactive_terrarium Marketplace Bundles](file:///D:/TechWriter/guides/bioactive_terrarium/06_publishing)
