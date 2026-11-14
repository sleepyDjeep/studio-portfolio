---
id: "nanobanana-concept-art-factory"
title: "Nano Banana Multi-Shot Concept-Art & Hardware Variant Factory"
subtitle: "Reusable JSON-driven batch illustration pipeline producing 51 widescreen world-building triads, hardware cutaways, and standalone HTML visual atlases at zero local VRAM cost."
pillar: "04-creative-3d-media"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-11-13"
date_updated: "2026-11-13"
tags:
  - "concept-art-pipeline"
  - "nano-banana"
  - "storytelling-atlas"
  - "industrial-design-renders"
  - "batch-automation"
  - "zero-vram"
metrics:
  - label: "Verified Batch"
    value: "51 Widescreen PNGs"
  - label: "Story Triads"
    value: "15 Worlds × 3 Shots"
  - label: "Hardware Variants"
    value: "6 Product & I/O Renders"
  - label: "Local GPU Load"
    value: "0 MB VRAM"
media:
  - src: "assets/concepts/story-worlds/01-the-redoubt-protocol-01_establishing.png"
    kind: "concept"
    caption: "Concept Preview (Story Triad Sample — Establishing): Eight-mile iron Last Redoubt pyramid glowing with amber Earth-Current tiers against night-land rift mist."
  - src: "assets/concepts/erig-demos/demo-02-smoked-resin-cutaway.png"
    kind: "concept"
    caption: "Concept Preview (Hardware Cutaway Sample): Smoked-resin bezel revealing the 192×114×38 mm ASA sled, dual 18650 cells, RP2040-Zero, Orange Pi Zero 2W, and PEEK hot well."
  - src: "assets/concepts/s21u-configs/config-b-kvm-crashcart-hardware-lab.png"
    kind: "concept"
    caption: "Concept Preview (Hardware I/O Variant Sample): S21U-DECK MK.I Server Crash-Cart & Hardware Lab layout with anodized KVM/RJ45/SMA/Phoenix/CAN bulkhead bay."
diagram: "assets/diagrams/nanobanana-concept-art-factory.svg"
tech_stack:
  - "Nano Banana (gemini-3.1-flash-image Subagents)"
  - "Python 3 + Pillow Image Compiler"
  - "JSON Prompt Matrices"
  - "Idempotent Markdown Gallery Injector"
  - "Zero-Server HTML5 <dialog> Visual Atlas"
local_paths:
  - label: "Concept-Art Workflow Scripts & Matrices"
    path: "file:///D:/Projects/_Shared_Library/concept_art_workflows"
  - label: "Batch Distributor & Atlas Compiler"
    path: "file:///D:/Projects/_Shared_Library/concept_art_workflows/run_concept_workflow.py"
  - label: "45-Shot Story World Matrix"
    path: "file:///D:/Projects/_Shared_Library/concept_art_workflows/prompt_matrices/story_worlds_45.json"
  - label: "6-Shot Hardware Demo & Config Matrix"
    path: "file:///D:/Projects/_Shared_Library/concept_art_workflows/prompt_matrices/hardware_demos_6.json"
  - label: "Standalone 45-Render Story Worlds Atlas"
    path: "file:///D:/Projects/_Shared_Library/storytelling_ideas/story_worlds_atlas.html"
run_commands:
  - label: "Audit Render Coverage Against 51 Target Prefixes"
    command: "python \"D:\\Projects\\_Shared_Library\\concept_art_workflows\\run_concept_workflow.py\" --artifact-dir \"C:\\Users\\ogreb\\.gemini\\antigravity\\brain\\e49d7a48-445a-4a68-ada7-8e54abcefb40\" --status-only"
  - label: "Compile PNGs, Markdown Triads & Standalone HTML Atlas"
    command: "python \"D:\\Projects\\_Shared_Library\\concept_art_workflows\\run_concept_workflow.py\" --artifact-dir \"C:\\Users\\ogreb\\.gemini\\antigravity\\brain\\e49d7a48-445a-4a68-ada7-8e54abcefb40\""
memory_ids:
  - "26dd6581-d643-4ad0-9594-f5706b9770f8"
conversation_ids:
  - "e49d7a48-445a-4a68-ada7-8e54abcefb40"
---

## What It Is & Why It Matters

Generating 50+ cohesive widescreen (`16:9`) concept illustrations and industrial product renders locally on an `8 GB` laptop GPU takes roughly 35–50 minutes of uninterrupted SDXL queue time while locking VRAM away from Godot, Blender, or desktop tools. Running ad-hoc single prompts in chat, on the other hand, leaves files scattered in temporary folders with inconsistent naming and manual copy-pasting into documentation.

We built the **Nano Banana Multi-Shot Concept-Art & Hardware Variant Factory** inside `D:\Projects\_Shared_Library\concept_art_workflows\` to turn multi-entry visual development into a repeatable, zero-VRAM studio pipeline. Structured JSON matrices define deterministic filename prefixes, literary-era or industrial-CAD art direction, and exact shot roles; paced parallel `image-generator` subagents render `1376 × 768` (`16:9`) plates in the cloud in a few minutes; and `run_concept_workflow.py` audits slot completion, converts and distributes optimized PNGs across project and portfolio folders, injects Markdown pitch tables, and compiles a standalone `file://` HTML visual atlas.

## Real Example: How It Works in Practice

Here is how we executed our **51-render visual production batch** across both game world-building and custom hardware engineering:

- **Input**: Two versioned JSON matrices—[story_worlds_45.json](file:///D:/Projects/_Shared_Library/concept_art_workflows/prompt_matrices/story_worlds_45.json) (`15` public-domain mashup worlds × a **3-Shot Pitch Triad**: `01_establishing` architecture, `02_character` cast portrait, and `03_gameplay` diegetic action with zero fake UI text) and [hardware_demos_6.json](file:///D:/Projects/_Shared_Library/concept_art_workflows/prompt_matrices/hardware_demos_6.json) (`3` product demonstration renders for the **Orange Pi Retro E-Dab Rig** + `3` enclosure/I/O configurations for the **S21U-DECK MK.I Cyberdeck**).
- **What Happens**: Parallel `image-generator` subagents (`gemini-3.1-flash-image`) render widescreen `16:9` plates using era-specific media styles (Piranesi iron engravings, 1927 Art Deco noir, Moebius ink-and-wash, ukiyo-e woodblock, CAD smoked-resin cutaways, and studio benchtop photography). Running `run_concept_workflow.py --status-only` verifies `51/51` prefix coverage, and running the full compiler normalizes RGB PNGs via Pillow and writes idempotent HTML/Markdown blocks.
- **Output**:
  1. **45 Story World Renders** mirrored into `_Shared_Library/storytelling_ideas/concept_art/<world-slug>/`, embedded as 15 inline 3-column tables inside [public_domain_mashup_worlds.md](file:///D:/Projects/_Shared_Library/storytelling_ideas/public_domain_mashup_worlds.md), compiled into [story_worlds_atlas.html](file:///D:/Projects/_Shared_Library/storytelling_ideas/story_worlds_atlas.html) (instant search, genre filters, Editorial Light / Dark Studio toggle, and native `<dialog>` lightbox), and wired into the Studio Portfolio.
  2. **3 Orange Pi E-Dab Product Renders** (carved walnut live whip demo, smoked-resin internal sled cutaway, and handheld + resin tabletop bubbler lineup) saved to `D:\Projects\OrangePi_EDab_Handheld\renders\` and the portfolio gallery.
  3. **3 S21U Cyberdeck Layout & I/O Renders** (Apache 2800 HOSAS Simpit, 60% Keyboard + Bulkhead Server KVM Crash-Cart, and Slim Aluminum/Carbon `13.3"` Field Tablet-Deck) wired directly into `s21u-cyberdeck-mk1`.

## Where It Stands & Next Steps

The workflow is **production-verified across all 51 renders** and indexed in `_Shared_Library/CATALOG.md` for immediate reuse on any future game design bible, hardware enclosure study, or pitch deck.

**Next Steps**:
1. Add a `--matrix <custom.json>` CLI flag when spinning up dedicated 12-shot environment/prop sheets for whichever mashup world enters Godot 4.7 greybox production first.
2. Pair Nano Banana concept plates with our local ComfyUI ControlNet/Depth pass only when pixel-locked orthographic 3D modelling turnarounds are needed.

## Under the Hood & Local Files

### Key Pipeline Engineering Rules
- **Paced Shard Concurrency (`<= 3–4` Active Subagents)**: Empirical testing during our 51-image run showed that firing 9 simultaneous `image-generator` shards triggers transient per-minute `HTTP 429 RESOURCE_EXHAUSTED` burst rejections on shards 8–9, whereas waves of `2–4` concurrent subagents (`3–6` sequential images per agent) complete cleanly with zero local GPU load.
- **Deterministic Prefix Reconciliation**: Subagent `generate_image` calls append a millisecond timestamp (`<ImageName>_<timestamp>.jpg`). `run_concept_workflow.py` globs `<prefix>_*` and selects the newest verified artifact per slot, making partial retries with `--status-only` deterministic and duplicate-free.
- **Idempotent Sentinel Blocks**: Markdown triad tables are wrapped in `<!-- CONCEPT_TRIAD_START:<num> --> ... <!-- CONCEPT_TRIAD_END:<num> -->` HTML comments so re-running the compiler after regenerating a single shot updates the Markdown cleanly without duplicating galleries.

### Key Workflow Files
- [run_concept_workflow.py](file:///D:/Projects/_Shared_Library/concept_art_workflows/run_concept_workflow.py) — Status auditor, Pillow PNG converter, Markdown gallery injector, and standalone HTML5 atlas compiler.
- [story_worlds_45.json](file:///D:/Projects/_Shared_Library/concept_art_workflows/prompt_matrices/story_worlds_45.json) & [hardware_demos_6.json](file:///D:/Projects/_Shared_Library/concept_art_workflows/prompt_matrices/hardware_demos_6.json) — Structured prompt and caption metadata for all 51 renders.
- [README.md](file:///D:/Projects/_Shared_Library/concept_art_workflows/README.md) — Quick-start CLI reference and concurrency pacing rules.
- [story_worlds_atlas.html](file:///D:/Projects/_Shared_Library/storytelling_ideas/story_worlds_atlas.html) — Zero-server `ibelick/baseline-ui` visual explorer for all 15 worlds and 45 concept plates.
