---
id: "comfyui-face-video-svg-studio"
title: "ComfyUI Portrait, SAM-2.1 Video & Local Vector SVG Studio"
subtitle: "A custom ComfyUI node pack and four 8 GB VRAM production workflows for two-pass portrait restyling, flicker-free SAM-2.1 anime video rotoscoping, and offline Rust VTracer SVG vectorization."
pillar: "04-creative-3d-media"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-10-31"
date_updated: "2026-11-02"
tags:
  - "comfyui"
  - "sam-2-1"
  - "svg-vectorization"
  - "vtracer"
  - "8gb-vram"
metrics:
  - label: "Production Workflows"
    value: "4 Studio JSONs"
  - label: "SAM-2.1 Post-Pass VRAM"
    value: "0 MB Retained"
  - label: "Direct SVG Trace"
    value: "< 1s (0 VRAM)"
  - label: "Max Video Upload"
    value: "4,096 MB"
media:
  - src: "assets/media/comfyui-face-video-svg-studio/demo-restyle-transpose.png"
    kind: "authentic"
    caption: "Synthetic smoke-test output from our 65-node two-pass SDXL identity and brushstroke transpose workflow."
  - src: "assets/media/comfyui-face-video-svg-studio/demo-anime-video-strip.png"
    kind: "authentic"
    caption: "Frame strip from our 8GB-VRAM SAM-2.1 + AnimateDiff rotoscoped anime video stylizer."
diagram: ""
tech_stack:
  - "Python 3.13 / PyTorch 2.6"
  - "ComfyUI v0.29.0"
  - "SAM 2.1 (sam2.1-hiera-small)"
  - "InsightFace + DWPose"
  - "SDXL + IP-Adapter FaceID Plus v2"
  - "Rust VTracer 0.6.15"
  - "OpenCV CIE-LAB K-Means"
local_paths:
  - label: "ComfyUI_FaceStyleTranspose"
    path: "file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/ComfyUI_FaceStyleTranspose"
  - label: "Local_Image_To_Vector_SVG_Studio.json"
    path: "file:///D:/Comfy/Local_Image_To_Vector_SVG_Studio.json"
  - label: "IRL_Video_To_Anime_Comic_Costume_BG_Studio.json"
    path: "file:///D:/Comfy/IRL_Video_To_Anime_Comic_Costume_BG_Studio.json"
run_commands:
  - label: "Launch ComfyUI (4GB Upload + SVG Middleware)"
    command: "\"D:\\Comfy\\ComfyUI_windows_portable\\run_nvidia_gpu.bat\""
  - label: "Launch LosslessCut Companion Trimmer"
    command: "\"D:\\Tools\\LosslessCut\\LosslessCut.exe\""
memory_ids:
  - "cf69f70a-fdea-4406-b1a4-5474a5ca63e2"
  - "96d5446e-055f-4f0c-aa99-05c0d6b8033d"
  - "25c490ad-5280-4836-90c7-488157abfafe"
  - "c408ef98-a96b-441c-9617-97ecc3337b27"
  - "ec981e61-8e9c-4de4-b5f4-0dc1fb027eac"
  - "211e8ad2-c2d8-41e9-9e92-f33d15942ea4"
  - "e47f65ea-7420-459c-9286-51b5c19a2004"
  - "bf9a5ced-e261-4716-b771-42d306398984"
  - "aad00d80-dfb5-469b-8def-246567a0cef9"
  - "e103afb4-e3a2-47ea-b656-5f99b7f2d6f6"
  - "aca63c39-cb5b-40e6-aa53-2fbc4ffe3344"
conversation_ids:
  - "eb69aa6d-5574-4f28-8705-1d988b0887d8"
---

## What It Is & Why It Matters

Standard ComfyUI community workflows break down quickly under three everyday studio tasks on an 8 GB GPU: portrait identity transfer fails whenever an illustrated character tilts their head sideways, full-clip video stylization triggers instant out-of-memory crashes or shimmering backgrounds, and ComfyUI's built-in `RecraftV4` vector nodes demand paid cloud API credits.

We engineered a custom Python node pack (`ComfyUI_FaceStyleTranspose`, 2,400+ lines across `__init__.py`, `video_nodes.py`, and `vector_nodes.py`) powering four self-contained studio workflows in `D:\Comfy`. Every node was built around explicit VRAM barriers, CPU offloading, and lazy branch evaluation so heavy SDXL, ControlNet Union ProMax, InsightFace, and Meta SAM 2.1 models coexist on a single 8 GB RTX 4060 Laptop GPU without model-thrashing or cloud fees.

Together, these four workflows give our studio an offline creative suite covering brushwork-matched portrait restyling, rotoscoped live-action-to-anime video conversion, and sub-second Bézier `.svg` vector illustration tracing.

## Real Example: How It Works in Practice

- **Input**: Three distinct media tasks run through the studio pack: (1) a Renaissance oil painting paired with a synthetic freckled portrait reference, (2) a live-action video clip with a single hand-painted mask on Frame 0, and (3) a raster emblem targeted for crisp 6-color brand SVG export.
- **What Happens**:
  1. **Two-Pass Portrait & Brushstroke Transpose (`Art_Face_Transpose_And_Style_Studio.json`, 65 nodes)**: Pass 1 optionally restyles the full canvas via SDXL Union ControlNet ProMax (depth + lineart) and `IPAdapterPreciseStyleTransfer`. In Pass 2, `SmartFaceMaskSelector` sweeps `0°/90°/180°/270°` quadrants using 106-point `InsightFace` and 68-point GPU `DWPose` landmarks, `AutoUprightFaceCrop` losslessly rotates tilted `1024x1024` crops upright for `IPAdapterFaceID Plus v2` (tuning `weight_faceidv2` to `0.55` when locking original bangs and expression), and `AutoRestoreFaceCrop` rotates the painted crop back before stitching.
  2. **SAM-2.1 Flicker-Free Video Stylizer (`IRL_Video_To_Anime_Comic_Costume_BG_Studio.json`, 90 nodes)**: `ChunkedVideoGifLoader` streams bounded frame chunks at `0.48–0.65 MP`. `SAM2VideoMaskPropagator` tracks the Frame-0 mask across the clip at `~0.20s/frame` (`~422 MB` peak VRAM), saves cross-chunk `.npz` state, and immediately flushes `0 MB` idle GPU memory inside a `finally:` block. CPU `u2net_human_seg` neutralizes original clothing patterns, a single-pass Master Background Plate locks the scenery at 0% flicker, and `VideoChunkAssemblerSave` encodes deflickered `libx264` `.mp4` output.
  3. **Offline Rust Vectorizer (`Local_Image_To_Vector_SVG_Studio.json`)**: `LocalVectorPaletteControl` applies OpenCV bilateral edge-preserving smoothing, snaps colors via perceptual CIE-LAB K-Means or custom `#HEX` palettes, strips outer borders to transparency without erasing white eye highlights, and runs Rust `vtracer 0.6.15` spline fitting into `SaveSVGNode`.
- **Output**: Brushstroke-matched SDXL portrait composites (`demo-restyle-transpose.png`), temporally coherent anime video sequences (`demo-anime-video-strip.png`), and true `<path d="...">` scalable `.svg` files in `ComfyUI\output\svg\` that render inline right inside the ComfyUI node canvas.

## Where It Stands & Next Steps

All four studio workflow JSONs and the `ComfyUI_FaceStyleTranspose` custom node package are shipped, smoke-tested with synthetic SFW test suites, and wired into ComfyUI `v0.29.0` (alongside **LosslessCut v3.70.2** at `D:\Tools\LosslessCut\LosslessCut.exe` and `--max-upload-size 4096` in `run_nvidia_gpu.bat`).

Next steps to extend the studio suite:
- **Upstream ComfyUI PR Packaging**: Split our `SaveSVGNode` inline preview `aiohttp` middleware and `LocalImageToVectorSVG` CIE-LAB palette node into a standalone open-source custom node repository for ComfyUI Manager.
- **Audio-Reactive Keyframe Modulation**: Feed stem envelope peaks from our Python DSP audio tools into `ChunkedVideoGifLoader` to pulse comic-book halftone line weights on drum transients.
- **Batch Folder CLI Runner**: Add a headless Python wrapper around all four JSON workflows for overnight batch icon SVG vectorization and character portrait sheet generation.

## Under the Hood & Local Files

### Core Engineering Solutions (`M0979`–`M0989`)
- **Orientation-Invariant Face & Landmark Recovery (`M0982`)**: Standard `InsightFace det_10g` detectors fail whenever an illustrated character leans horizontally or upside down. `SmartFaceMaskSelector` cascades from multi-scale 106-point `buffalo_l` into shared-singleton TorchScript `DWPose Wholebody` (`yolox_l` + `dw-ll_ucoco_384_bs5`), verifying `mouth_y > brow_y` across all four `90°` lossless `torch.rot90` quadrants so SDXL never paints an upright face onto a tilted head.
- **Decoupling Identity from Expression & Hair (`M0981`)**: Inspecting `ProjPlusModel.forward` (`out = x + scale * perceiver_resampler(x, clip_embeds)`) proved that high `weight_faceidv2` (`1.35`) injects CLIP-Vision photo smiles and hairstyles over target art. Our `FaceTransposeModePreset` node drops shortcut weight to `0.55`, tightens `mask_expand_px` to `2px`, and raises DWPose landmark strength to `0.85` to swap bone structure while keeping bangs and expression intact.
- **Zero-Idle-VRAM Video Stage Barriers (`M0983`, `M0986`)**: By pairing `OUTPUT_IS_LIST = True` 1-frame execution streams with `INPUT_IS_LIST = True` CPU-RAM barriers (`VideoStreamToBatchBarrier`) and explicit `gc.collect()` + `torch.cuda.empty_cache()` teardown after `sam2.1-hiera-small` propagation, 90-node video graphs run inside `~3.8–4.5 GB` active VRAM.
- **ComfyUI v0.29.0 Bugfixes (`M0987`, `M0989`)**: ComfyUI `v0.29.0` shipped two upstream regressions: `server.py` crashed with `PIL.UnidentifiedImageError` when `/view` appended `&preview=webp` to `.svg` files and forced `application/octet-stream` downloads, while template `0.11.19` referenced a dropped `RecraftV4ImageToVectorNode`. We installed a git-clean `aiohttp` middleware (`_install_svg_preview_middleware` checking `Sec-Fetch-Dest: image`) and a forward-yielding `nodes_recraft_v4_compat.py` shim.

### Key Local Files
- Custom Node Package (3-Tier Face Detector & Lazy Routers): [__init__.py](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/ComfyUI_FaceStyleTranspose/__init__.py)
- Chunked Video, SAM-2.1 Propagator & Deflicker Engine: [video_nodes.py](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/ComfyUI_FaceStyleTranspose/video_nodes.py)
- Rust VTracer, CIE-LAB Palette Quantizer & SVG Middleware: [vector_nodes.py](file:///D:/Comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/ComfyUI_FaceStyleTranspose/vector_nodes.py)
- Studio Workflow 1 (2-Pass Portrait & Style): [Art_Face_Transpose_And_Style_Studio.json](file:///D:/Comfy/Art_Face_Transpose_And_Style_Studio.json)
- Studio Workflow 2 (Streaming Video/GIF Transpose): [Art_Face_Transpose_Video_GIF_Studio.json](file:///D:/Comfy/Art_Face_Transpose_Video_GIF_Studio.json)
- Studio Workflow 3 (Live-Action to Anime + Master BG): [IRL_Video_To_Anime_Comic_Costume_BG_Studio.json](file:///D:/Comfy/IRL_Video_To_Anime_Comic_Costume_BG_Studio.json)
- Studio Workflow 4 (Offline Image-to-SVG Studio): [Local_Image_To_Vector_SVG_Studio.json](file:///D:/Comfy/Local_Image_To_Vector_SVG_Studio.json)
