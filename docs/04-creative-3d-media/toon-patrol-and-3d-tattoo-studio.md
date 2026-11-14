---
id: "toon-patrol-and-3d-tattoo-studio"
title: "Toon Patrol Flash & 3D Forearm Tattoo Studio"
subtitle: "Synthesizes multi-character New School tattoo flash sheets with paired thermal transfer stencils, then wraps vector linework onto an interactive 3D forearm mesh."
pillar: "04-creative-3d-media"
entry_type: "workflow"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-26"
date_updated: "2026-11-02"
tags:
  - "comfyui"
  - "tattoo-design"
  - "regional-ip-adapter"
  - "3d-uv-preview"
  - "threejs"
metrics:
  - label: "Isolated Characters"
    value: "3 Regional Masks"
  - label: "Flash Resolution"
    value: "896x1152 SDXL"
  - label: "Thermal Stencils"
    value: "8 Ready-to-Print PNGs"
  - label: "3D Limb Preview"
    value: "OBJ + Three.js + SVG"
media:
  - src: "assets/media/toon-patrol-and-3d-tattoo-studio/weasels-color-flash.png"
    kind: "authentic"
    caption: "Multi-character New School tattoo flash sheet synthesized locally via Regional IP-Adapter attention masks."
  - src: "assets/media/toon-patrol-and-3d-tattoo-studio/smartass-stencil.png"
    kind: "authentic"
    caption: "High-contrast black-and-white thermal transfer line stencil generated in parallel via ControlNet Canny."
diagram: ""
tech_stack:
  - "ComfyUI (SDXL + PonyV6XL)"
  - "Regional IP-Adapter Plus"
  - "ControlNet Canny SDXL"
  - "OpenCV"
  - "RemBG & VTracer"
  - "Three.js"
local_paths:
  - label: "Toon Patrol Flash & Stencils"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954"
  - label: "3D Forearm UV Tattoo Planner"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/d1456b5e-0f40-4627-bc2a-ea5bc6bcf4a9"
run_commands:
  - label: "Run Regional Multi-Character Flash Generator"
    command: "python \"C:\\Users\\ogreb\\.gemini\\antigravity\\brain\\bc74ecd4-2c87-4365-a651-d9800fecb954\\scratch\\generate_regional_conditioned_master.py\""
  - label: "Extract Thermal Stencil Linework"
    command: "python \"C:\\Users\\ogreb\\.gemini\\antigravity\\brain\\bc74ecd4-2c87-4365-a651-d9800fecb954\\scratch\\stencil_generator.py\""
memory_ids:
  - "c48f997d-4927-446a-a481-23869d6fca78"
  - "dc9d9f68-7b84-4e85-bd92-811faca89a2c"
conversation_ids:
  - "8d3b8c39-bd94-495b-b4e2-80028186afe6"
  - "55018cfc-a15c-4683-96a5-3b959de65488"
  - "d1456b5e-0f40-4627-bc2a-ea5bc6bcf4a9"
  - "bc74ecd4-2c87-4365-a651-d9800fecb954"
---

## What It Is & Why It Matters

Designing custom multi-character tattoo flash and testing how flat artwork wraps around a real human limb exposes two immediate walls. Cloud image generators routinely block homage prompts referencing classic 1980s animation characters, while standard local Stable Diffusion runs suffer from severe trait bleeding—putting one character's hat on another character's head whenever three distinct figures share a single canvas. Even after finishing a clean 2D flash sheet, judging how rectangular artwork distorts across a tapered forearm normally requires guesswork in the chair.

We built a two-part local tattoo engineering toolkit to solve both stages on our RTX 4060 workstation. The first pipeline runs against our local ComfyUI API (`http://127.0.0.1:8188`) to synthesize bold New School cartoon flash sheets—tested on a *Who Framed Roger Rabbit* Toon Patrol "Die Laughing" tribute—while simultaneously extracting crisp black-and-white line stencils formatted for thermal transfer copiers.

The second pipeline bridges 2D flash onto real 3D anatomy. Taking four rotational smartphone photos of a forearm alongside hand-drawn marker sketches, it strips backgrounds, stitches a wrap-around UV skin cylinder, converts sketches into infinitely scalable `.svg` vector tiles, and launches a live Three.js browser viewer so placement and wrap curvature can be inspected from every angle before ink touches skin.

## Real Example: How It Works in Practice

- **Input**: Three isolated cartoon character references (**Smart Ass** in his double-breasted cream zoot suit and pink fedora, **Psycho** in a straitjacket with a rising ghost spirit, and **Stupid** in a striped tee with propeller beanie, angel wings, and harp) plus four cardinal smartphone angles (front, back, left, right) of a forearm.
- **What Happens**:
  1. `prepare_assets.py` and `process_masks_and_canny.py` arrange the three characters onto an `896x1152` vertical composition (`layout_896x1152.png`), extract structural `canny_layout_896x1152.png` edge maps, and write three non-overlapping binary attention masks (`mask_smartass.png`, `mask_psycho.png`, `mask_stupid.png`).
  2. `generate_regional_conditioned_master.py` submits an API graph to ComfyUI running `ponyDiffusionV6XL` paired with `ControlNet Canny SDXL` (`0.65`–`0.75` strength) and three regionally masked `IP-Adapter Plus SDXL` (`CLIP-ViT-H-14`) conditioning nodes. Each weasel's wardrobe, props, and expression stay locked inside its own spatial zone with zero cross-character contamination.
  3. `stencil_generator.py` runs an OpenCV bilateral filter (`cv2.bilateralFilter`) to flatten color gradients while preserving ink contours, followed by adaptive Gaussian thresholding (`cv2.adaptiveThreshold`) to emit pure black-on-white thermal transfer line stencils alongside solo character cutouts.
  4. For 3D limb fitting, `rembg` isolates the four forearm angles, OpenCV crops limb contours and blends a cylindrical `arm_texture.png`, `VTracer` vectorizes four sketch motifs into tiled `.svg` decals, and a procedural mesh builder writes a tapered elliptical `arm_model.obj` wired into `tattoo_preview.html`.
- **Output**: Full-color flash sheets (`die_laughing_weasels_color_flash_v2.png`), matching thermal transfer line stencils (`die_laughing_weasels_tattoo_stencil_v2.png` plus solo color/stencil pairs for all three characters), tiled `.svg` vector stencils, an iPad Procreate / Blender-ready `arm_model.obj`, and an interactive Three.js 3D forearm orbit viewer.

## Where It Stands & Next Steps

Both workflows have shipped complete, print-ready outputs on disk. The Toon Patrol regional ComfyUI suite generated `16` final master and solo color/stencil PNGs inside `output\`, while the 3D limb planner produced a stitched UV wrap, `8` single and tiled `.svg` vector sheets, a standard `.obj` + `.mtl` limb mesh, and a self-contained Three.js HTML preview (`tattoo_preview.html`) verified in desktop browsers.

Next steps if we turn this internal studio toolkit into a reusable shop utility:
- **Interactive Decal Dragging in Three.js**: Add raycast UV gizmos inside `tattoo_preview.html` so `.svg` flash stencils can be dragged, scaled, and rotated live across the 3D forearm mesh in real time instead of reloading Blender or Procreate.
- **Curvature-Compensated Stencil Unwrapping**: Project the positioned 3D decal back into 2D paper space using inverse cylindrical distortion so a printed thermal stencil compensates for wrist-to-elbow taper automatically.
- **One-Click ComfyUI Stencil Node**: Wrap `stencil_generator.py` into our custom ComfyUI node pack so every flash render saves its paired thermal line sheet in a single queue execution.

## Under the Hood & Local Files

### Architectural Decisions & Engineering Fixes
- **Regional IP-Adapter Attention Masking (`M0341`–`M0342`)**: Prompting three named cartoon characters in a single SDXL latent causes global cross-attention layers to average colors (turning every suit pink or duplicating propeller hats). Binding separate `IPAdapterRegionalConditioning` nodes to `mask_smartass.png` (center-right), `mask_psycho.png` (bottom-left), and `mask_stupid.png` (top) restricts each `CLIP-ViT-H-14` embedding strictly to its assigned pixel coordinates while sharing lighting and New School ink outlines globally.
- **Dual-Branch Color & Thermal Linework**: Tattoo artists need saturated whip-shaded flash to judge palette balance, yet thermal stencil machines require crisp, unshaded binary linework. Driving both branches from the exact same `canny_layout_896x1152.png` structural map and post-processing via bilateral edge-preserving smoothing guarantees 1:1 pixel registration between the color reference and transfer stencil.
- **Zero-Cloud Limb Photogrammetry Alternative**: Full 40-photo Meshroom scans are overkill for cylindrical forearm placement. Approximating the forearm as a tapered elliptical cylinder mapped with four background-stripped cardinal photos builds a clean Procreate-compatible `.obj` in seconds rather than 25 minutes.

### Key Local Files
- Toon Patrol Walkthrough & Proof Sheets: [walkthrough.md](file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954/walkthrough.md)
- Regional IP-Adapter & Stencil Scripts: [generate_regional_conditioned_master.py](file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954/scratch/generate_regional_conditioned_master.py) | [process_masks_and_canny.py](file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954/scratch/process_masks_and_canny.py) | [stencil_generator.py](file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954/scratch/stencil_generator.py)
- Final Multi-Character & Solo Flash Outputs: [die_laughing_weasels_color_flash_v2.png](file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954/output/die_laughing_weasels_color_flash_v2.png) | [die_laughing_weasels_tattoo_stencil_v2.png](file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954/output/die_laughing_weasels_tattoo_stencil_v2.png) | [char_smartass_stencil.png](file:///C:/Users/ogreb/.gemini/antigravity/brain/bc74ecd4-2c87-4365-a651-d9800fecb954/output/char_smartass_stencil.png)
- 3D Forearm UV Model & Interactive Viewer: [tattoo_model_summary.md](file:///C:/Users/ogreb/.gemini/antigravity/brain/d1456b5e-0f40-4627-bc2a-ea5bc6bcf4a9/tattoo_model_summary.md) | [tattoo_preview.html](file:///C:/Users/ogreb/.gemini/antigravity/brain/d1456b5e-0f40-4627-bc2a-ea5bc6bcf4a9/scratch/tattoo_preview.html) | [arm_model.obj](file:///C:/Users/ogreb/.gemini/antigravity/brain/d1456b5e-0f40-4627-bc2a-ea5bc6bcf4a9/scratch/arm_model.obj)
