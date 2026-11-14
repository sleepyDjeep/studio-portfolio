---
id: "lineart-to-3d-trellis2-pipeline"
title: "2D Lineart to 3D Mech Factory (Microsoft TRELLIS 2)"
subtitle: "Bridges flat black-and-white mech sketches into textured 3D GLB models on 8 GB VRAM by injecting volumetric shading before running Microsoft TRELLIS 2."
pillar: "04-creative-3d-media"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-09-01"
date_updated: "2026-09-02"
tags:
  - "comfyui"
  - "trellis-2"
  - "2d-to-3d"
  - "mecha"
  - "blender"
metrics:
  - label: "Generated 3D Mechs"
    value: "33 Textured GLBs"
  - label: "GPU Budget"
    value: "8 GB VRAM"
  - label: "Pipeline Stages"
    value: "4 Automated Passes"
  - label: "Kitbash Scene"
    value: "Mech_Scrapyard.blend"
media:
  - src: "assets/media/lineart-to-3d-trellis2-pipeline/mech-input-clean.png"
    kind: "authentic"
    caption: "Isolated shaded mech concept prepared by our ControlNet + Rembg stage prior to Microsoft TRELLIS 2 3D GLB mesh generation."
diagram: "assets/diagrams/lineart-to-3d-trellis2-pipeline.svg"
tech_stack:
  - "ComfyUI"
  - "Microsoft TRELLIS 2"
  - "ControlNet Lineart"
  - "ComfyUI-rembg"
  - "Blender 5.1 Headless"
  - "Python 3.13 / PyTorch 2.6"
local_paths:
  - label: "Comfy"
    path: "file:///D:/Comfy"
  - label: "README_START_HERE.md"
    path: "file:///D:/Comfy/README_START_HERE.md"
  - label: "Blender_LowPoly_Cheatsheet.md"
    path: "file:///D:/Comfy/Blender_LowPoly_Cheatsheet.md"
run_commands:
  - label: "Launch ComfyUI 3D Server"
    command: "\"D:\\Comfy\\ComfyUI_windows_portable\\run_nvidia_gpu.bat\""
  - label: "Pack Generated GLBs into Blender Grid"
    command: "blender --background --python \"C:\\Users\\ogreb\\.gemini\\antigravity\\brain\\d7d03869-c33e-4015-aa25-7f2724f39d88\\scratch\\import_glbs.py\""
memory_ids:
  - "f91bec21-cd10-457b-ad11-8352d4c9d9c3"
conversation_ids:
  - "d7d03869-c33e-4015-aa25-7f2724f39d88"
---

## What It Is & Why It Matters

Image-to-3D neural generators such as Microsoft TRELLIS 2 and Tencent Hunyuan3D-2 infer three-dimensional depth from lighting gradients, ambient occlusion, and specular highlights. When fed a flat black-and-white ink drawing—like classic tabletop mech technical readouts—those models misread white paper inside the silhouette as flat surfaces or empty holes, extruding thin cardboard-like slabs instead of articulated armor volumes.

We built this local four-stage workflow inside `D:\Comfy` to turn unshaded 2D mech lineart into game-ready 3D `.glb` meshes on an 8 GB RTX 4060 Laptop GPU without paying per-model fees to commercial cloud services like Meshy or Tripo. Instead of asking the 3D solver to guess depth from bare ink lines, an upstream diffusion pass paints physically plausible metallic bevels and directional lighting straight inside the locked ink contours first.

That single intermediate step unlocked rapid chassis prototyping for *MechDestroyer* and our broader 3D asset kits. Across one automated batch session, the pipeline converted flat multi-mech concept sheets into 33 textured `.glb` battlemechs and arranged them into a unified Blender kitbash yard (`Mech_Scrapyard.blend`).

## Real Example: How It Works in Practice

- **Input**: A multi-character black-and-white mech concept sheet containing unshaded ink line drawings of bipedal and reverse-joint walkers.
- **What Happens**:
  1. **Sheet Slicing (`slice_mechs.py`)**: A Python preprocessor detects bounding contours on the composite sketch sheet and crops individual mech drawings into padded square frames.
  2. **Volumetric Shading Injection (`shading_workflow.json`)**: ComfyUI runs Stable Diffusion 1.5 paired with **ControlNet Lineart** to lock every armor panel seam and weapon barrel in place while rendering directional studio lighting, gunmetal gradients, and recessed joint shadows across the hull.
  3. **Alpha Isolation (`ComfyUI-rembg`)**: The shaded concept image passes directly into a `Rembg` segmentation node, stripping background backdrop gradients into a clean RGBA cutout (`mech-input-clean.png`) so background pixels never fuse onto the 3D hull.
  4. **3D Mesh & Texture Synthesis (`mech_trellis.json`)**: `Trellis2ImageToShape` reconstructs a watertight 3D sparse-voxel geometry from the shaded silhouette, `Trellis2ShapeToTexturedMesh` bakes UV-mapped PBR surface colors onto the mesh, and headless Blender (`import_glbs.py`) imports every `.glb` onto a `2.0m`-spaced inspection grid.
- **Output**: 33 standalone textured `.glb` 3D mech files written to `D:\Comfy\ComfyUI_windows_portable\ComfyUI\output\` (such as `mech_output_10_shaded_20260831_233650.glb`), plus the master `D:\MechDestroyer\Mech_Scrapyard.blend` kitbash file ready for low-poly decimation and hardpoint rigging.

## Where It Stands & Next Steps

The workflow is production-tested and reusable (`35` total `.glb` mech and prop meshes currently stored in `ComfyUI\output\`, alongside root automation scripts `run_decimate.py`, `generate_assets.py`, and `blender-mcp-addon.py` in `D:\Comfy`). Both TRELLIS 2 and the `Hunyuan3D-2` mini/turbo wrappers are configured to stay within an 8 GB VRAM ceiling using 32 GB system RAM weight offloading.

Concrete next steps for expanding the 3D factory:
- **Automated Symmetrize & Decimate Pass**: Chain `D:\Comfy\run_decimate.py` directly onto the end of `batch_enqueue.py` so newly generated 80k-triangle TRELLIS meshes automatically drop to `3,000–8,000` triangles with mirrored X-axis hard-surface normals.
- **8-Zone Limb Segmentation Hook**: Pipe finished `.glb` hulls directly into *MechDestroyer*'s bounding-box slicer (`Head`, `CT`, `LT`, `RT`, `LA`, `RA`, `LL`, `RL`) for instant cockpit and limb-destruction setup.
- **Multi-View Ortho Conditioning**: Add a zero-1-to-3 orthogonal back-view synthesis branch so rear reactor vents and jump-jet packs match front-view armor density without manual kitbashing.

## Under the Hood & Local Files

### Key Engineering Fixes & Architecture (`M0551`, `C075`)
- **PyTorch 2.6 Custom Op Schema Fix (`patch_typing.py`)**: During setup on Python 3.13 + PyTorch `2.6.0+cu124`, the Pixi-isolated `trellis2-nodes` environment crashed on startup inside `comfy_kitchen` (`backends/eager/na.py`, `backends/triton/na.py`, `backends/cuda/__init__.py`) because `torch.library.infer_schema` rejected lowercase PEP-585 `list[int]` and `list[bool]` annotations on custom CUDA neighborhood-attention operators. Rewriting those annotations to `typing.List[int]` and `typing.List[bool]` brought the entire TRELLIS 2 CUDA/Triton stack online cleanly.
- **8 GB VRAM Split Execution**: Running SD1.5 ControlNet shading, `Rembg`, and TRELLIS 2 shape-plus-texture synthesis sequentially via ComfyUI's REST queue (`POST http://127.0.0.1:8188/prompt`) allows ComfyUI's model manager to evict the 2D diffusion checkpoint before allocating sparse 3D attention tensors.
- **Optional BlenderMCP Socket Bridge**: `D:\Comfy\blender-mcp-addon.py` exposes a local TCP control socket (`localhost:9876`) so local LM Studio models or Antigravity agents can trigger decimation, flat-shading, and UV baking inside Blender without manual GUI clicks.

### Key Local Files
- 3D Pipeline Root & Guides: [README_START_HERE.md](file:///D:/Comfy/README_START_HERE.md) | [Blender_LowPoly_Cheatsheet.md](file:///D:/Comfy/Blender_LowPoly_Cheatsheet.md) | [BlenderMCP_Setup.md](file:///D:/Comfy/BlenderMCP_Setup.md)
- Decimation & MCP Scripts: [run_decimate.py](file:///D:/Comfy/run_decimate.py) | [blender-mcp-addon.py](file:///D:/Comfy/blender-mcp-addon.py) | [generate_assets.py](file:///D:/Comfy/generate_assets.py)
- Batch TRELLIS 2 & Shading Scripts: [shading_workflow.json](file:///C:/Users/ogreb/.gemini/antigravity/brain/d7d03869-c33e-4015-aa25-7f2724f39d88/scratch/shading_workflow.json) | [mech_trellis.json](file:///C:/Users/ogreb/.gemini/antigravity/brain/d7d03869-c33e-4015-aa25-7f2724f39d88/scratch/mech_trellis.json) | [patch_typing.py](file:///C:/Users/ogreb/.gemini/antigravity/brain/d7d03869-c33e-4015-aa25-7f2724f39d88/scratch/patch_typing.py) | [import_glbs.py](file:///C:/Users/ogreb/.gemini/antigravity/brain/d7d03869-c33e-4015-aa25-7f2724f39d88/scratch/import_glbs.py)
- Sample Generated 3D Mesh: [mech_output_10_shaded_20260831_233650.glb](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/output/mech_output_10_shaded_20260831_233650.glb)
