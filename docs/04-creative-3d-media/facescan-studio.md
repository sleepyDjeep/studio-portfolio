---
id: "facescan-studio"
title: "FaceScan Studio: Open-Source Facial Photogrammetry & 53-Shape Rig"
subtitle: "Turns a 25-second smartphone video into a 4K-textured Blender 5.1 character head wired with all 53 Apple ARKit facial expression blendshapes—using zero paid software."
pillar: "04-creative-3d-media"
entry_type: "project"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-11-11"
date_updated: "2026-11-11"
tags:
  - "photogrammetry"
  - "blender-5-1"
  - "meshroom"
  - "arkit-blendshapes"
  - "open-source-3d"
metrics:
  - label: "Facial Blendshapes"
    value: "53 ARKit / FACS"
  - label: "Commercial Cost"
    value: "$0 (100% FOSS)"
  - label: "Baked Texture"
    value: "4096x4096 Albedo"
  - label: "Automation Code"
    value: "1,209 LOC"
media:
  - src: "assets/concepts/facescan-studio.png"
    kind: "concept"
    caption: "Concept Preview: Technical breakdown of Meshroom dense photogrammetry wrapping onto a 53-ARKit blendshape topology in Blender 5.1."
diagram: "assets/diagrams/facescan-studio.svg"
tech_stack:
  - "Python 3"
  - "AliceVision Meshroom"
  - "Blender 5.1"
  - "USC ICT-FaceKit"
  - "MPFB2 v2.0.18"
  - "SoftWrap (GPU Patched)"
  - "FFmpeg"
local_paths:
  - label: "FaceScanStudio"
    path: "file:///D:/FaceScanStudio"
  - label: "ICT_Master_Rigged_Head.blend"
    path: "file:///D:/FaceScanStudio/tools/ICT_Master_Rigged_Head.blend"
run_commands:
  - label: "Stage 1: Run Meshroom Photogrammetry"
    command: "\"D:\\FaceScanStudio\\01_Run_Meshroom_Photogrammetry.bat\""
  - label: "Stage 2: Wrap & Open Rig in Blender 5.1"
    command: "\"D:\\FaceScanStudio\\02_Import_Scan_and_Open_Blender.bat\""
memory_ids:
  - "d3cd29e4-16d5-4b0b-8711-718621565830"
  - "053759e4-6b83-4e37-a81c-ef0a708b30fc"
  - "3a3a14ad-8b44-4f07-a8da-7895ca0f8582"
conversation_ids: []
---

## What It Is & Why It Matters

Turning a real human actor into an animatable 3D character head usually forces indie teams into expensive per-seat plugins like KeenTools FaceBuilder, Wrap4D, or cloud-locked MetaHuman pipelines. Raw photogrammetry scans look accurate as static statues, yet their chaotic triangle soup cannot blink, smile, or speak. FaceScan Studio solves that gap locally on our workstation at zero licensing cost.

We assembled a two-button, 100% open-source character rigging pipeline inside `D:\FaceScanStudio` that bridges smartphone capture directly into Blender 5.1. By pairing AliceVision Meshroom's dense Structure-from-Motion solver with the University of Southern California's open-source `ICT-FaceKit` morphable model, any captured likeness inherits clean animation quad topology and all 53 Apple ARKit / Facial Action Coding System (FACS) blendshapes automatically.

To make the workflow practical on modern Blender 5.1 builds, we also modernized the open-source SoftWrap topology transfer add-on—porting its viewport overlay shaders off Blender's removed `bgl` OpenGL wrapper onto the modern Vulkan-ready `gpu` module—and built a custom sidebar panel (`facescan_studio_panel.py`) for one-click expression testing and 4K Cycles texture baking.

## Real Example: How It Works in Practice

- **Input**: A 25-second 4K 60 FPS smartphone video (or 40 to 60 still photos) recorded 5 to 6 feet from a subject at `2x` optical zoom under even indirect daylight, dropped into `D:\FaceScanStudio\01_Input_Photos_or_Video`.
- **What Happens**:
  1. Launching `01_Run_Meshroom_Photogrammetry.bat` runs `step1_prepare_photos_or_video.py`, which probes clip duration via `ffprobe` and calls `ffmpeg` (`-qscale:v 1`) to extract ~65 crisp, evenly spaced JPEG frames free of selfie barrel distortion.
  2. `step2_run_meshroom.py` invokes `meshroom_batch.exe` on our RTX 4060 GPU, computing camera poses, depth maps, and a high-density `texturedMesh.obj` scan inside `02_Meshroom_Project\Output_Scan`.
  3. Launching `02_Import_Scan_and_Open_Blender.bat` opens our pre-compiled `ICT_Master_Rigged_Head.blend` template in Blender 5.1, imports the raw Meshroom scan, and binds a weighted `Face_Wrap_Mask` vertex group (`Shrinkwrap` + 10-iteration `Corrective Smooth` modifiers) so the front facial mask snaps onto the scan while keeping the ear sockets, cranium, and neck clean.
  4. Inside Blender's `N`-panel, the artist refines landmark alignment via GPU-patched `SoftWrap`, clicks **Bake 4K Texture from Meshroom Scan** inside our `FaceScan Studio` tab to project photographic skin detail onto clean UVs via GPU Cycles, and tests 9 one-click expression presets (*Warm Smile*, *Big Laugh*, *Wink Smirk*, *Surprised*, *Skeptical*).
- **Output**: A clean-quad Blender 5.1 character head rigged with 53 functional ARKit shape keys (`eyeBlink_L/R`, `jawOpen`, `mouthSmile_L/R`, `browDown_L/R`), a 4096x4096 baked albedo skin map, subsurface-scattering Principled BSDF materials, and a 50mm transparent-film Cycles camera ready for character export or compositing.

## Where It Stands & Next Steps

FaceScan Studio is installed, verified, and ready for repeatable character production (`206` files across `489.9 MB`, `1,209` lines of custom Python and batch automation). All four open-source pillars—AliceVision Meshroom `v2023.3.0`, `MPFB2 v2.0.18` (for full-body, eyeball, teeth, and Rigify bone generation), our Blender 5.1 `gpu`-patched `SoftWrap` add-on, and the 53-shape `ICT_Master_Rigged_Head.blend` template—are wired and operational on disk.

Next steps to expand this pipeline for our Godot 4.7 game projects:
- **Automated Normal & Roughness Baking**: Extend the one-click Cycles baker to emit tangent-space pore normal maps and specular cavity maps alongside the 4K albedo pass.
- **Direct Godot 4.7 `.glb` Character Exporter**: Add an operator button to `facescan_studio_panel.py` that applies the non-destructive shrinkwrap base while re-computing all 53 relative shape keys for direct glTF 2.0 import into Godot `MeshInstance3D` blendshape tracks.
- **Live Webcam ARKit Retargeting**: Connect MediaPipe Face Landmarker (`52` blendshape stream) over UDP into Blender and Godot so a standard webcam can puppet the rigged head at 60 FPS.

## Under the Hood & Local Files

### Architectural Decisions & Engineering Fixes
- **Zero-Trial Open-Source Stack (`M1017`–`M1018`)**: Commercial topology wrappers lock blendshape transfer behind recurring licenses or watermarked trials. We bypassed them by pre-compiling USC's `ICT-FaceKit` (`generic_neutral_mesh.obj` + `vertex_indices.json` + 53 FACS morph `.obj` targets) via `foreach_get` / `foreach_set` vertex buffer copies in `build_master_ict_head.py`—building the master rig 10x faster than standard `join_shapes` operators.
- **Blender 5.1 `bgl` -> `gpu` Port**: Legacy `SoftWrap` crashed on Blender 5.1 startup because the deprecated `bgl` OpenGL wrapper was removed in Blender 4.0+. Patching `draw_3d.py` to compile built-in `UNIFORM_COLOR` / `3D_SMOOTH_COLOR` shaders via Blender's `gpu` and `gpu_extras.batch` APIs restored interactive point-pinning in viewport space.
- **Z-Falloff Vertex Masking**: Photogrammetry from a 180-degree frontal arc leaves noisy geometry behind the ears and under the chin. `step3_setup_blender_rig.py` computes a smooth Z-axis weight ramp (`(v.co.z + 2.5) / 4.0` for `z > -2.5` and `y > -8.5`) so `Shrinkwrap` conforms the expressive facial mask without crumpling the skull or neck seam.

### Key Local Files
- Workspace Root & Guide: [README_WORKFLOW.md](file:///D:/FaceScanStudio/README_WORKFLOW.md)
- One-Click Batch Launchers: [01_Run_Meshroom_Photogrammetry.bat](file:///D:/FaceScanStudio/01_Run_Meshroom_Photogrammetry.bat) | [02_Import_Scan_and_Open_Blender.bat](file:///D:/FaceScanStudio/02_Import_Scan_and_Open_Blender.bat)
- Frame Extractor & Video Probe: [step1_prepare_photos_or_video.py](file:///D:/FaceScanStudio/scripts/step1_prepare_photos_or_video.py)
- Meshroom CLI/GUI Orchestrator: [step2_run_meshroom.py](file:///D:/FaceScanStudio/scripts/step2_run_meshroom.py)
- Pre-Baked 53-ARKit Template Builder: [build_master_ict_head.py](file:///D:/FaceScanStudio/scripts/build_master_ict_head.py) | [ICT_Master_Rigged_Head.blend](file:///D:/FaceScanStudio/tools/ICT_Master_Rigged_Head.blend)
- Automated Shrinkwrap & 4K Bake Scene Builder: [step3_setup_blender_rig.py](file:///D:/FaceScanStudio/scripts/step3_setup_blender_rig.py)
