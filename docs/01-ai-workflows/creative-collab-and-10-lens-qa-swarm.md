---
id: "creative-collab-and-10-lens-qa-swarm"
title: "3D Creative Studio & 10-Lens Computer-Vision QA Swarm"
subtitle: "Human-in-the-loop WebSocket layout tools, headless Blender 5.1 PBR baking, and a 10-lens SQLite computer-vision swarm auditing 2,160-frame Vulkan walkthroughs."
pillar: "01-ai-workflows"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-09-19"
date_updated: "2026-09-21"
tags:
  - "computer-vision-qa"
  - "blender-5.1"
  - "godot-vulkan"
  - "websockets"
  - "pbr-pipeline"
  - "sqlite"
metrics:
  - label: "Final CV Audit Score"
    value: "94.21 / 100"
  - label: "Walkthrough Audited"
    value: "2,160 Frames (90s)"
  - label: "Parallel QA Lenses"
    value: "10"
  - label: "Certified Release Gates"
    value: "67 / 67"
media:
  - src: "assets/media/creative-collab-and-10-lens-qa-swarm/bento-contact-sheet.png"
    kind: "authentic"
    caption: "Multi-angle Cycles PBR contact sheet produced automatically by Gate 2 of our headless Blender 5.1 prop pipeline."
  - src: "assets/media/creative-collab-and-10-lens-qa-swarm/asset-health-dashboard.png"
    kind: "authentic"
    caption: "Automated 3D asset health and triangle/UV metric audit dashboard generated during Kaiju Kiosk production."
diagram: "assets/diagrams/creative-collab-and-10-lens-qa-swarm.svg"
tech_stack:
  - "Blender 5.1 Headless (bmesh + Cycles)"
  - "Godot 4.7 Movie Maker (Vulkan)"
  - "Python + OpenCV + NumPy"
  - "SQLite (qa_swarm.db)"
  - "WebSockets (:8092 / :8093)"
local_paths:
  - label: "Kaiju Kiosk QA & Blender Tooling"
    path: "file:///D:/Projects/KaijuConvenience/tools"
  - label: "Visual Review & Contact Sheets"
    path: "file:///D:/Projects/KaijuConvenience/output/visual_review"
run_commands:
  - label: "Run Gate 1 Programmatic 3D Metric Audit"
    command: "python \"D:\\Projects\\KaijuConvenience\\tools\\audit_asset_metrics.py\""
  - label: "Run Gate 2 Adversarial Marketplace Judge"
    command: "python \"D:\\Projects\\KaijuConvenience\\tools\\adversarial_visual_judge.py\" --verbose"
memory_ids:
  - "2216de06-c0d6-4390-9008-63fab40db5aa"
  - "23ed4469-8e17-49d0-b431-c900c5e2fe62"
  - "224a0acb-e0e8-4e67-9fb9-d57a5cc1a440"
  - "67d8d5ee-be17-4e3d-ae67-5bbebaa9da6d"
  - "95f5ad4a-5181-459e-b382-8240874094ec"
  - "c9fdffed-f629-47b9-aeb9-2f6d28c615cd"
  - "23684b83-2e80-4c87-a7bd-e5dd84f82be2"
  - "8c0d7e03-ae1d-4a69-86c6-753b530b250d"
  - "b662ab93-f5e0-4ed6-9581-df4e2ccb1cf2"
  - "8f2ca33c-6dc9-4c96-981a-1d75f2ca0b96"
  - "401704dd-59ce-4d73-9907-c9f2d82bd951"
  - "a47fb2a9-aefc-4fa7-8a51-d233f82f3ff5"
  - "32bb20ed-fbbb-4569-b064-0c8af7330de6"
  - "1a024490-f840-4484-a359-0146a08d41b9"
  - "4bdf2715-345e-4124-bdc6-ecd4bdd5343c"
  - "105677ae-2934-4c70-ba17-84dc89963259"
  - "af8e50a8-febe-441a-be25-7ca7fdad6fe0"
  - "40a88fb3-1138-4592-96c8-97f536c9687f"
  - "0369e694-ad6b-40c2-bb1b-b2a77779b198"
  - "aa0c84fc-7b25-47a3-b8c5-a17f125000ef"
  - "87f88cfa-ead4-40d9-b91e-093ec51a2fbc"
  - "417a3338-42dc-490b-ae5a-2479a9661e65"
  - "80ab9e68-d405-481e-adba-9ad832297ffb"
  - "e2d9c030-aa62-4087-bc9f-18d44fad9dac"
  - "d0227f6a-7768-401b-a6ee-9f7168b12062"
conversation_ids: []
---

## What It Is & Why It Matters

Unit tests can verify whether a game's cash register adds numbers properly, yet they are completely blind to upside-down snack labels, stretched UV maps, flat primitive boxes masquerading as hero props, or pitch-black lighting corners. Between September 19 and September 21, 2026, while preparing *Kaiju Kiosk* and its `$19.99` commercial 3D asset pack, we engineered an end-to-end 3D creative collaboration studio and automated computer-vision QA swarm that holds procedural 3D scenes to commercial marketplace standards.

The workflow operates across three tightly coupled layers. First, our headless **Blender 5.1 PBR Factory** kitbashes detailed manifold `bmesh` props (chamfered bezels, handles, louvers, keypads) and bakes `2048x2048` Cycles Albedo, Normal, and channel-packed ORM textures—blocking any export that fails **Dual-Gate QA** (programmatic geometry/UV variance math followed by multi-angle contact-sheet grading). Second, three browser-based **WebSocket Creative Studios** let human art direction steer AI builders live: a Redline Annotation Canvas (`ws://localhost:8092`), a 2D-to-3D Room Layout Studio (`ws://localhost:8093`) that writes coordinates straight into Godot `.tscn` scenes, and a Multi-Deck Inspiration Studio extracting CIELAB k-means color palettes.

Third, once assets enter the game, our **10-Lens SQLite CV Remediation Swarm** boots Godot 4.7 Vulkan Movie Maker to record a deterministic 90-second (`2,160`-frame) walkthrough at `1280x720 @ 24 FPS`. Ten parallel computer-vision audit lenses inspect the frames for silhouette clarity, exposure balance, shelf density, outline continuity, and z-fighting, logging defects into `qa_swarm.db` until every regression is fixed.

## Real Example: How It Works in Practice

- **Input**: A newly generated convenience-store bento box (`bento_box.glb`) and cashier counter (`cashier_counter.glb`) staged inside `Main.tscn` for commercial pack certification.
- **What Happens**:
  1. **Gate 1 — Mathematical Mesh & PBR Audit (`audit_asset_metrics.py`)**: Inspects raw binary `.glb` buffers and `2048x2048` `.png` maps, verifying station meshes exceed `1,200` triangles, merchandise props exceed `180` triangles, UV island texel density coefficient of variation stays `< 0.15` (`15%`), and PBR Laplacian high-frequency variance (`sigma^2`) hits `>= 15.0` (proving genuine baked edge wear and AO grime rather than flat solid colors).
  2. **Gate 2 — Contact Sheet & Marketplace Rubric (`adversarial_visual_judge.py`)**: Renders multi-angle Cycles studio contact sheets (`bento_box_artist_contact_sheet.png`) and scores 10 commercial criteria—including canonical `+Z` aisle orientation and inverted-hull ink outlines—requiring an average `>= 9.0 / 10.0` with zero sub-`7.0` categories.
  3. **5-Cycle 10-Lens Walkthrough Swarm**: Godot renders `walkthrough_90s.mp4` (`2,160` frames); 10 CV lenses flag sparse gondola shelves and dark cooler corners in SQLite; builders populate 32-item 4-tier gondolas and cyan LED cooler strips, then re-run the capture.
- **Output**: *Kaiju Kiosk*'s composite CV audit score climbed across 5 remediation cycles from `90.29` to **`94.21 / 100`** with `0` defects, `67 / 67` release gates green, and a certified `2,247`-file commercial asset pack.

## Where It Stands & Next Steps

The entire Python, Blender 5.1, WebSocket, and SQLite QA toolchain (`23,120 LOC` across 40 Python scripts plus `6,119 LOC` across 3 HTML dashboards and studio frontends) is shipped on disk inside `D:\Projects\KaijuConvenience\tools\` and verified against `974` `.glb` models and `14` `.mp4` walkthrough captures. During development, we also documented and patched breaking Blender 5.1 Principled BSDF input socket renames (`Specular IOR Level` and `Transmission Weight`) in LanceDB so future headless bakes never fail on Blender 4-to-5 script migrations.

Next steps to generalize this workflow across future 3D titles:
- Extract `audit_asset_metrics.py`, `adversarial_visual_judge.py`, and the `ws://localhost:8093` `.tscn` Room Layout Studio into `D:\Projects\_Shared_Library` so *MechDestroyer* and *Babylon* can run identical 10-lens Movie Maker sweeps.
- Add automated frame-time and draw-call telemetry overlays into `qa_swarm.db` alongside the 10 visual quality lenses.

## Under the Hood & Local Files

### Dual-Gate & Swarm Architecture
- **Programmatic Thresholds (`audit_asset_metrics.py`)**: Enforces `STATION_MIN_TRIS = 1200`, `MERCHANDISE_MIN_TRIS = 180`, `MAX_TEXEL_CV = 0.15`, `MIN_PBR_LAPLACIAN_VAR = 15.0`, and `EXPECTED_PBR_RESOLUTION = (2048, 2048)` with strict non-zero exit codes on violation.
- **10-Point Commercial Rubric (`adversarial_visual_judge.py`)**: Scores Mesh Silhouette, Edge Chamfer/Bevel Stack, Canonical `+Z` UV Orientation, Texel Uniformity, Curvature+AO+ORM Depth, Stylized Ink Outlines, Operational Clutter, Manifold Normals, Collision Integrity, and Marketplace EULA Presentation.
- **Interactive WebSocket Studios (`tools/studio/`)**: Bridges human redline strokes (`:8092`) and top-down dollhouse furniture drags (`:8093`) directly to live scene transforms without opening the Godot editor UI.

### Key Local Files
- [audit_asset_metrics.py](file:///D:/Projects/KaijuConvenience/tools/audit_asset_metrics.py) — Gate 1 binary `.glb` triangle, UV texel variance, and OpenCV Laplacian texture auditor.
- [adversarial_visual_judge.py](file:///D:/Projects/KaijuConvenience/tools/adversarial_visual_judge.py) — Gate 2 10-criterion commercial marketplace evaluator.
- [blender_pbr_baker.py](file:///D:/Projects/KaijuConvenience/tools/blender_pbr_baker.py) & [blender_components_library.py](file:///D:/Projects/KaijuConvenience/tools/blender_components_library.py) — Headless Blender 5.1 procedural `bmesh` kitbasher and Cycles 2K PBR map baker.
- [asset_health_dashboard.html](file:///D:/Projects/KaijuConvenience/output/visual_review/artist_audit/asset_health_dashboard.html) — Visual audit report across every station and merchandise prop.
- [index.html](file:///D:/Projects/KaijuConvenience/tools/studio/index.html) — Browser-based creative studio frontend for redlining, palette extraction, and room layout editing.
