---
id: "oil-paint-frazetta-battletech-pipeline"
title: "Retro Paperback Oil-Paint & BattleTech Cover Pipeline"
subtitle: "Converts everyday photos and 3D mech renders into heavy-impasto 1970s sci-fi paperback oil paintings using a 5-stage local ComfyUI graph."
pillar: "04-creative-3d-media"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-10-05"
date_updated: "2026-10-06"
tags:
  - "comfyui"
  - "oil-painting"
  - "battletech-art"
  - "frazetta-lora"
  - "sdxl-inpainting"
metrics:
  - label: "Pipeline Stages"
    value: "5 Modular Passes"
  - label: "VRAM Footprint"
    value: "8 GB RTX 4060"
  - label: "Style LoRAs"
    value: "Frazetta + Sci-Fi Env"
  - label: "Base Checkpoint"
    value: "JuggernautXL Ragnarok"
media:
  - src: "assets/media/oil-paint-frazetta-battletech-pipeline/frazetta-oil-render.png"
    kind: "authentic"
    caption: "Heavy-impasto 1970s paperback oil painting synthesized locally via our 5-stage JuggernautXL + Frazetta LoRA pipeline."
diagram: ""
tech_stack:
  - "ComfyUI"
  - "JuggernautXL Ragnarok"
  - "Frazetta Impasto LoRA"
  - "ControlNet Depth & Lineart"
  - "IP-Adapter Plus SDXL"
  - "RemBG & SAM"
local_paths:
  - label: "Comfy"
    path: "file:///D:/Comfy"
  - label: "Frazetta Two-Pass Output"
    path: "file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/output/frazetta_2pass_final_00001_.png"
run_commands:
  - label: "Launch Portable ComfyUI (RTX 4060 FP16)"
    command: "\"D:\\Comfy\\ComfyUI_windows_portable\\run_nvidia_gpu_fast_fp16_accumulation.bat\""
memory_ids:
  - "c8162245-5b72-423e-9b2b-9c0a255f60fc"
  - "0494d268-1394-4e14-a4b0-c978efb7c962"
conversation_ids:
  - "0af1e174-9bb0-43f7-8508-ec31048073ea"
---

## What It Is & Why It Matters

Standard AI image-to-image filters treat "oil painting" like a thin Photoshop emboss effect. When you feed a real-world photograph or an untextured 3D mech blockout into a single-pass img2img node, low denoise preserves plastic smartphone lighting while high denoise melts the subject's pose, anatomy, and silhouette. Neither setting captures the physical paint thickness, dramatic chiaroscuro shadow pools, or warm canvas glazes of 1970s and 1980s sci-fi paperback covers.

We engineered this 5-stage ComfyUI SDXL workflow inside `D:\Comfy` to recreate authentic physical oil brushwork—combining Frank Frazetta's palette-knife impasto and chiaroscuro lighting, Gil Elvgren's warm glazing, and classic Jim Holloway / Christopher Moeller *BattleTech* cover composition. Running locally on an 8 GB RTX 4060, the graph separates silhouette preservation from medium synthesis so mundane apartment walls or flat viewport renders give way to smoky planetary horizons and tactile canvas texture.

Across our studio, this pipeline gives us a repeatable key-art factory for game box covers, retro manual illustrations, and stylized character portraits without relying on cloud APIs or generic digital airbrushing.

## Real Example: How It Works in Practice

- **Input**: A standard indoor reference photograph (or 3D mech viewport capture) paired with a classic Frazetta brushstroke reference (`_+Swords+Of+Mars+_+by+Frank+Frazetta+Painting+Print-56170715.webp`).
- **What Happens**:
  1. **Stage 1 — Subject Segmentation**: `RemBG` and Segment Anything (`SAM`) strip away everyday indoor backgrounds so the subject silhouette sits cleanly over a new latent environment canvas.
  2. **Stage 2 — Structural Pose Locking**: `ControlNet Depth` and `ControlNet Lineart` inspect the isolated subject and lock perspective, foreshortening, and gesture lines onto `juggernautXL_ragnarok` before any paint style is applied.
  3. **Stage 3 — Heavy Impasto & Backdrop Synthesis**: The graph injects `fr4z3tt4.safetensors` alongside `Scifi_Environment_Concept_Art_ANIMA.safetensors` and an `IP-Adapter Plus` style reference, replacing flat background pixels with smoky alien skies, industrial hangar silhouettes, and thick oil underpainting.
  4. **Stage 4 — Masked Sci-Fi Wardrobe & Prop Inpainting**: Targeted SAM region masks allow localized high-denoise inpainting to swap street clothes into retro flight suits, tactical harnesses, or mechanical limb details without disturbing facial likeness or posture.
  5. **Stage 5 — Unified Oil-Glaze Second Pass**: A full-canvas `0.38`–`0.45` denoise refinement pass unifies foreground figure and sci-fi horizon under shared directional rim lighting, warm burnt-umber shadows, and visible bristle ridges.
- **Output**: High-resolution paperback cover renders (`frazetta_cover_00001_.png` and `frazetta_2pass_final_00001_.png`) saved directly to `D:\Comfy\ComfyUI_windows_portable\ComfyUI\output\`.

## Where It Stands & Next Steps

The 5-stage workflow and all supporting SDXL checkpoints, ControlNets, and custom LoRAs are installed and verified inside `D:\Comfy\ComfyUI_windows_portable`. Both single-cover compositions (`frazetta_cover_00001_.png`) and two-pass glaze refinements (`frazetta_2pass_final_00001_.png`) execute cleanly within an 8 GB VRAM ceiling using ComfyUI's `--fast` FP16 accumulation launch profile.

Next steps to package this artistic pipeline for faster batch cover production:
- **Subgraph Packaging**: Collapse the 5-stage node chain into a single ComfyUI Subgraph template exposing just four top-level sliders (*Impasto Thickness*, *Backdrop Sci-Fi Scale*, *Chiaroscuro Contrast*, and *Glaze Pass Denoise*).
- **Automated Typography Safe-Zones**: Add a composition guide mask in Stage 1 that reserves upper-third negative space for classic 1980s embossed *BattleTech*-style title mastheads.
- **Direct Godot 3D Viewport Bridge**: Feed greybox mech captures straight from our Godot 4.7 scenes into Stage 2 `ControlNet Depth` to generate painted faction loading screens automatically.

## Under the Hood & Local Files

### Architectural Decisions & Engineering Fixes
- **Medium Pivot from Watercolor to Impasto Oil (`M0913` -> `M0917`)**: Early experiments tested soft watercolor washes (`M0913`), which lacked sufficient tonal weight for armored sci-fi and dramatic fantasy scenes. Switching the style stack to `fr4z3tt4.safetensors` paired with `juggernautXL_ragnarok` (`M0917`) delivered authentic palette-knife texture, deep shadow contrast, and warm oil glazes without turning skin tones muddy.
- **Decoupling Backdrop Replacement from Pose Retention**: Running high-strength style LoRAs directly over an unmasked room photo causes bookshelf and drywall edges to turn into accidental sci-fi clutter behind the character's head. Isolating the subject via `RemBG` + `SAM` prior to `ControlNet Depth/Lineart` conditioning lets the background hallucinate dramatic atmospheric perspective at `1.0` denoise while holding the foreground figure tight.
- **Two-Pass Glaze Cohesion**: Masked inpainting (Stage 4) frequently leaves subtle lighting seams around armor collars or cybernetic joints. Running a low-denoise global second pass with `IP-Adapter Plus` brushstroke weights knits every boundary into continuous canvas grain.

### Key Local Files
- Portable ComfyUI Fast FP16 Launcher: [run_nvidia_gpu_fast_fp16_accumulation.bat](file:///D:/Comfy/ComfyUI_windows_portable/run_nvidia_gpu_fast_fp16_accumulation.bat)
- Installed Oil & Sci-Fi LoRA Weights: [fr4z3tt4.safetensors](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/models/loras/fr4z3tt4.safetensors) | [Scifi_Environment_Concept_Art_ANIMA.safetensors](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/models/loras/Scifi_Environment_Concept_Art_ANIMA.safetensors)
- Brushwork Conditioning Reference: [_+Swords+Of+Mars+_+by+Frank+Frazetta+Painting+Print-56170715.webp](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/input/_+Swords+Of+Mars+_+by+Frank+Frazetta+Painting+Print-56170715.webp)
- Verified Two-Pass Oil Render Outputs: [frazetta_2pass_final_00001_.png](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/output/frazetta_2pass_final_00001_.png) | [frazetta_cover_00001_.png](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/output/frazetta_cover_00001_.png)
