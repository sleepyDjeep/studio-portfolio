---
id: "local-llm-vram-orchestration"
title: "8 GB VRAM Local LLM & GPU Time-Slicing Protocol"
subtitle: "Empirical VRAM cliff benchmarks and a 5-stage GPU handoff protocol that runs local LLMs, ComfyUI SDXL/SAM2, Blender Cycles, and Godot Vulkan on a single 8 GB RTX 4060."
pillar: "01-ai-workflows"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-08-26"
date_updated: "2026-09-18"
tags:
  - "vram-optimization"
  - "rtx-4060"
  - "lm-studio"
  - "comfyui"
  - "blender-cycles"
  - "godot-vulkan"
metrics:
  - label: "16k Context Speed"
    value: "29.2 tok/s (6.85 GB)"
  - label: "32k WDDM Spill Speed"
    value: "3.9 tok/s (8.98 GB)"
  - label: "Throughput Cliff"
    value: "7.5x Drop"
  - label: "Sequential GPU Stages"
    value: "5"
media: []
diagram: "assets/diagrams/local-llm-vram-orchestration.svg"
tech_stack:
  - "NVIDIA RTX 4060 Laptop (8 GB)"
  - "LM Studio v0.4.6 (Flash Attention)"
  - "ComfyUI (/free API)"
  - "Blender 5.1 Headless Cycles"
  - "Godot 4.7 Forward+ Vulkan"
local_paths:
  - label: "Local GGUF Model Store"
    path: "file:///D:/Models/LMStudio"
  - label: "ComfyUI Portable Pipeline"
    path: "file:///D:/Comfy"
run_commands:
  - label: "Flush ComfyUI VRAM via REST"
    command: "curl -X POST http://127.0.0.1:8188/free -H \"Content-Type: application/json\" -d \"{\\\"unload_models\\\": true, \\\"free_memory\\\": true}\""
  - label: "Inspect Live RTX 4060 VRAM Allocation"
    command: "nvidia-smi --query-gpu=memory.used,memory.free,memory.total --format=csv"
memory_ids:
  - "a37c281e-fd3d-47d7-9de3-684abb6b73de"
  - "6a8bf79a-1b4d-4182-bbd8-5f364364dadd"
  - "3dbc3afc-c724-482a-a1c2-6497d3aca880"
  - "5723136d-6c69-45a5-a27d-a3be3d676f8f"
conversation_ids: []
---

## What It Is & Why It Matters

Running local LLMs, SDXL/SAM-2.1 diffusion pipelines, GPU raytraced texture baking, and Vulkan 3D game engines simultaneously on an 8 GB NVIDIA GeForce RTX 4060 Laptop GPU will crash or crawl if left to default settings. Worse, Windows 11 does not always throw an obvious out-of-memory error when VRAM fills up. Instead, the Windows Display Driver Model (WDDM) silently pages excess tensor layers across the PCIe bus into shared system RAM, destroying generation speed by nearly an order of magnitude.

Between August 26 and September 18, 2026, we ran controlled memory and token-throughput benchmarks in LM Studio v0.4.6 (`Qwen2.5-7B-Instruct` `Q4_K_M`, `4.68 GB` weights, Flash Attention ON, plus `Llama-3.1-8B`) to map the exact GDDR6 cliff on our workstation. At a `16,384`-token context limit, total allocation stays at `6.85 GB` (`1.34 GB` free headroom), delivering `0.22s` time-to-first-token and `29.2 tokens/sec` pure GDDR6 throughput. Doubling context to `32,768` tokens pushes demand to `8.98 GB` (`9.38 GB` with unquantized fp16 KV cache), spilling `~1.4 GB` into system RAM and collapsing speed `7.5x` down to `3.9 tokens/sec`.

Using those hard numbers, we standardized a 5-stage sequential GPU time-slicing protocol. Instead of letting tools fight over 8 GB concurrently, automated scripts explicitly unload each resident GPU consumer before handing the card to the next stage—allowing a single mobile GPU to execute AAA-style multi-tool asset and game builds at `$0` cloud cost.

## Real Example: How It Works in Practice

- **Input**: An automated build cycle needs local LLM item descriptions and dialogue JSON, ComfyUI concept/sprite sheets, `2048x2048` Blender Cycles PBR normal/ambient-occlusion bakes, and a 90-second Godot 4.7 Vulkan Movie Maker walkthrough capture.
- **What Happens**:
  1. **Stage 1 — Local LLM Generation (`6.85 GB` Peak)**: LM Studio loads `Qwen2.5-7B` (`Q4_K_M`, `16,384` context, Flash Attention ON), generates structured JSON data at `29.2 tok/s`, and immediately unloads model weights back to `0 MB` VRAM.
  2. **Stage 2 — ComfyUI Synthesis (`~3.8–6.4 GB` Peak)**: ComfyUI executes SDXL or chunked 16-frame SAM-2.1/AnimateDiff graphs, then receives `POST http://127.0.0.1:8188/free` (`unload_models: true, free_memory: true`) plus explicit Python `gc.collect()` and `comfy.model_management.soft_empty_cache()` hooks that drop idle node leaks from `422 MB` to `0 MB`.
  3. **Stage 3 — Headless Blender 5.1 Cycles Bake**: `blender --background --python blender_pbr_baker.py` claims clean GDDR6 for OptiX/CUDA raytraced curvature, AO, and normal baking, exiting cleanly on completion.
  4. **Stage 4 — Godot 4.7 Vulkan Forward+ Execution**: Dedicated discrete GPU routing launches Godot 4.7 at full 60+ FPS (`1280x720` or `1080p`) to run headless/windowed integration tests or render `.mp4` Movie Maker walkthroughs.
  5. **Stage 5 — CPU/SQLite QA Analysis**: OpenCV metrics and ONNX `bge-small-en-v1.5` memory writes run strictly on CPU (`0 MB` VRAM), keeping GPU state clean for the next cycle.
- **Output**: Zero `CUDA out of memory` faults, zero `3.9 tok/s` WDDM PCIe thrashing, and deterministic multi-engine builds across *PocketRPG Studio*, *MechDestroyer*, and *Kaiju Kiosk*.

## Where It Stands & Next Steps

This orchestration protocol is a permanent studio standard stored in our Unified Memory Bank (`M0340`, `M0739–M0741`) and enforced across all local AI pipelines. Every custom ComfyUI node we authored later in October and November—including `SAM2VideoMaskPropagator` in `ComfyUI_FaceStyleTranspose`—incorporates automatic post-pass `gc.collect()` + `soft_empty_cache()` teardown directly in Python so idle VRAM returns to `0 MB`.

Next steps to refine GPU scheduling:
- Wrap our 5-stage VRAM check (`nvidia-smi` free-memory assertion + automatic `/free` + `lms unload --all`) into a reusable Python context manager inside `D:\Projects\_Shared_Library`.
- Benchmark 4-bit (`Q4_0` / `Q8_0`) KV-cache quantization in newer llama.cpp builds to test whether `24k`–`32k` context windows can stay below the `7.2 GB` safe GDDR6 ceiling without WDDM spill.

## Under the Hood & Local Files

### Benchmark Ledger & Driver Findings
- **Workstation GPU**: NVIDIA GeForce RTX 4060 Laptop GPU (`8,188 MiB` physical GDDR6) paired with Intel Iris Xe integrated graphics on Windows 11.
- **Discrete GPU Binding Rule**: Hybrid Optimus laptops occasionally bind headless OpenGL/Vulkan or D3D9-on-12 processes to Intel Iris Xe, causing `0xc0000374` heap corruptions or severe frame drops; all studio engines (`Godot`, `Blender`, `PCSX2`, `EmulationStation`) are explicitly pinned to the High-Performance NVIDIA processor.
- **CPU Offload Partitioning**: Any continuous background service—specifically LanceDB + FastEmbed (`BAAI/bge-small-en-v1.5`) and `u2net_human_seg` mask pre-processors—is pinned to CPU ONNX Runtime so `0 MB` of baseline VRAM is permanently occupied.

### Key Local Files
- [LMStudio](file:///D:/Models/LMStudio) — Local GGUF quantized weights repository (`Qwen2.5-7B`, `Hermes-3-Llama-3.1-8B`, Nomic embeddings).
- [run_nvidia_gpu.bat](file:///D:/Comfy/ComfyUI_windows_portable/run_nvidia_gpu.bat) — Local ComfyUI Portable launcher configured for 8 GB RTX 4060 memory management.
- [generate_assets.py](file:///D:/Comfy/generate_assets.py) — Automated ComfyUI API asset batcher using sequential queue polling and VRAM teardown.
- [blender_pbr_baker.py](file:///D:/Projects/KaijuConvenience/tools/blender_pbr_baker.py) — Headless Blender 5.1 Cycles GPU baker invoked during Stage 3 of the handoff loop.
