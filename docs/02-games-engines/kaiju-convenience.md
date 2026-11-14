---
id: "kaiju-convenience"
title: "Kaiju Kiosk & Neo-Tokyo Kombini 3D Asset Kit"
subtitle: "First-person Neo-Tokyo convenience store simulation game in Godot 4.7 paired with a 2,247-file commercial 3D asset and cel-shader kit."
pillar: "02-games-engines"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-17"
date_updated: "2026-09-21"
tags:
  - "godot-4-7"
  - "first-person-sim"
  - "cel-shading"
  - "blender-pbr"
  - "commercial-asset-kit"
  - "vulkan"
metrics:
  - label: "Source Code"
    value: "185,178 LOC"
  - label: "Demo Executable"
    value: "728.77 MB"
  - label: "Commercial Asset Kit"
    value: "2,247 Files"
  - label: "Headless Assertions"
    value: "7,544 Passing"
  - label: "10-Lens CV QA Score"
    value: "94.21 / 100"
media:
  - src: "assets/media/kaiju-convenience/store-exterior.png"
    kind: "authentic"
    caption: "1080p Godot 4.7 Vulkan capture of the Neo-Tokyo kombini storefront marquee at night."
  - src: "assets/media/kaiju-convenience/gondola-aisles.png"
    kind: "authentic"
    caption: "Stocked 32-item central gondola aisles rendered with stepped cel bands and comic ink outlines."
  - src: "assets/media/kaiju-convenience/cashier-checkout.png"
    kind: "authentic"
    caption: "Diegetic barcode checkout counter, steamed bun warmer, and overhead rack."
  - src: "assets/media/kaiju-convenience/kaiju-horizon.png"
    kind: "authentic"
    caption: "Skyline kaiju silhouette looming above the city block during a night-shift tremor event."
  - src: "assets/media/kaiju-convenience/aisles-dollhouse.png"
    kind: "authentic"
    caption: "Orthographic dollhouse render showcasing the packaged 2,247-file Neo-Tokyo Kombini commercial 3D asset kit."
diagram: ""
tech_stack:
  - "Godot 4.7.1 (Vulkan Forward+)"
  - "GDScript"
  - "Godot Shader Language (GLSL)"
  - "Blender 5.1 Headless Cycles"
  - "Python 3"
  - "SQLite CV QA Swarm"
local_paths:
  - label: "KaijuConvenience Project Root"
    path: "file:///D:/Projects/KaijuConvenience"
  - label: "Standalone Windows Demo"
    path: "file:///D:/Projects/KaijuConvenience/export/KaijuKiosk_Demo.exe"
  - label: "Commercial Kombini Asset Kit"
    path: "file:///D:/Projects/KaijuConvenience/export/neo_tokyo_kombini_kit"
run_commands:
  - label: "Launch Standalone Demo Binary"
    command: "\"D:\\Projects\\KaijuConvenience\\export\\KaijuKiosk_Demo.exe\""
  - label: "Open Project in Godot 4.7"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\KaijuConvenience\""
  - label: "Run Project & Asset Metric Gates"
    command: "python \"D:\\Projects\\KaijuConvenience\\tools\\verify_project.py\" && python \"D:\\Projects\\KaijuConvenience\\tools\\audit_asset_metrics.py\""
memory_ids:
  - "9fad9232-81a0-496d-a21c-a26eb5689a15"
  - "833a56cf-b10b-44a0-98f9-923f9a16a741"
  - "6102ef81-a947-485c-8252-d1338c401d4a"
  - "1d126a9d-a292-487b-a4f8-3fe3b5d619b8"
  - "f6ac936f-6a40-4f53-9910-82f35f40936d"
  - "477a69d4-b80e-4bdc-98e9-3ba38f04d2e2"
  - "6bba286e-c81e-4d35-a65f-a41918b9f9a1"
  - "5e55d38a-c318-4e3f-88c9-f525c229f40b"
  - "dba3d129-1088-4be2-bc4f-befc39cfa23f"
  - "cbaef0dc-da94-43fd-b904-c841868c3113"
  - "04bf3f59-096f-4da5-8e6f-2aeb07c6a8ba"
  - "8ef74f00-ae12-4a82-81eb-1832e4106859"
  - "c3186f6b-271d-4793-9c25-76454e35662d"
  - "c932e5be-2109-459a-ba3f-3087620f6652"
  - "189bb2fc-2dc0-432e-b532-ba30b5daad61"
  - "e2d7c7b2-faf6-4bcb-9071-f90adb52e8f9"
  - "068af9b2-9b97-4043-b69c-2ebd20900906"
  - "ff6f492d-1c98-4afa-bbc1-d6bf4b94a0f3"
  - "79ccd18b-2aaa-4e85-b825-354bc88d4fba"
  - "fe8f72a5-a056-48ef-8d16-8d02cb2b153f"
  - "9cb2f5f3-a7e5-4ac7-9384-8e14114b9d73"
  - "4d57eff6-098f-49ab-b636-a8143f4f8ed7"
  - "b4058bd3-33d6-43b8-885c-6a01edcb31a5"
  - "51afc223-7571-4e19-b5f4-d9e64001add3"
  - "bc0ad9c1-c2a0-4d07-890b-20ba6d7d5668"
  - "7bea5380-3ad8-4f83-807f-c92da8519697"
  - "3e38ff6c-c057-4ed8-ab07-d5fa41a81338"
  - "3de1224c-579b-450a-95bc-cdcf31f98ff2"
  - "883b9777-bef1-4c24-96b3-04ddd68d6d10"
  - "29a5d78a-30fc-43c4-95fb-237eaeccee8f"
  - "208836c0-626e-401f-b3aa-6c08858752b9"
  - "2feafee0-6fc8-4ec0-8ad4-84be463abcce"
  - "d37c2204-bece-40f2-af17-f5f261c305c2"
  - "f8b5762d-e4f9-46fb-861b-e43702bdbb37"
  - "c52149ae-417b-404b-b305-d9a560aa3e55"
  - "dd9738a8-d4ee-4e0d-9873-cbf4c3a9cdbd"
  - "a67f8704-5cdf-49d2-a06f-52acd1113106"
  - "d5f883cc-cb74-4253-8735-3cb5732726dd"
  - "07bd31e6-a9ad-4c9f-a5ea-cc98345bdd0b"
  - "dcc18fcb-d58e-47e8-8f7e-abc26f00278f"
  - "58735b76-919e-46c5-9876-ce49303d5172"
  - "99b0916b-802d-4a74-b6f3-f7701cef8a03"
  - "c2702e66-82a8-47f4-b575-9e62695ad5ba"
  - "da90b585-192f-4c4d-bc68-6bf3b34bc45e"
  - "b10df24c-00ce-4dc8-9f5b-3508b51e99fb"
  - "bbbf028d-2e38-4f38-9344-5b071caa32cf"
  - "2ddb61a4-b6a4-4432-a9af-dd7af70cfa3f"
  - "2303fe4b-dfb6-4760-88ec-58d6032c1e0c"
  - "067cfcc6-c47f-4392-a54c-ed908a39920a"
  - "2d12e274-08cd-420c-8ab3-9ad63da3fc5c"
  - "c15c212c-e17d-4400-b466-9ef58c3ca894"
  - "a4ec423b-eefc-4eed-a95b-3de5379af0a0"
  - "d5a55583-daef-4d0a-8ada-17796572d20b"
conversation_ids:
  - "466e98b4-8a32-4459-9b49-4a89691eed47"
  - "605f26a2-72e8-429e-b733-9134e06ffdc9"
  - "4e24697f-d1b1-4bdb-8e80-0f59861c340f"
  - "4039ed9d-9bd3-444a-bcb3-249c57f4898c"
  - "14a8df81-79fd-48fe-998f-daa91af788f8"
---

## What It Is & Why It Matters

*Kaiju Kiosk* (*Kaiju Convenience*) puts you behind the counter of a 24-hour Neo-Tokyo neighborhood convenience store during a 90-day season of monster sightings, rolling EMP blackouts, and seismic tremors. You unpack cardboard stock crates by hand, line up bento trays and energy drinks on four-tier gondolas, scan barcodes with a physical laser gun, make change at the cash drawer, and mop muddy footprints while a towering kaiju crosses the city horizon outside your front glass. Visuals blend low-polygon PlayStation 2 geometry with modern Vulkan physically based lighting, stepped cel-shading bands, and comic-book ink outlines inspired by *Jet Set Radio Future* and *Borderlands 3*.

We built *Kaiju Kiosk* to prove one studio thesis: a single 3D production pipeline can ship both a playable standalone game and an immediate-revenue commercial 3D asset pack from the exact same codebase. Every refrigerator, slushie dispenser, cashier counter, and snack pouch was engineered to strict marketplace topology, UV density, and texture-baking standards rather than throwaway prototype shortcuts.

That dual-product discipline also drove our studio's most thorough automated art-direction pipeline. Instead of eyeballing 974 3D models by hand, we built headless Blender 5.1 procedural kitbashing factories, GPU Cycles curvature-and-grime bakers, live WebSocket room-layout tools, and a 10-lens computer-vision audit swarm that graded 90-second Vulkan gameplay movies frame by frame until visual defects dropped to zero.

## Real Example: How It Works in Practice

- **Input**: You launch `KaijuKiosk_Demo.exe` into Night Shift Day 1, pick up a delivered `StockCrate` of chilled drinks and boxed meals at the backroom door, and trigger an evening seismic alert from `DisasterManager` while NPC commuters queue at the register.
- **What Happens**: `HandController` raycasts onto individual `soda_can.glb` and `bento_box.glb` meshes, snapping them onto `Shelf.gd` price-tag rails oriented along `+Z` toward the aisle. When the tremor hits, damped harmonic impulse curves rattle unanchored merchandise onto the linoleum, emergency sirens fire, and `DisasterManager` strobes the overhead fluorescents into an EMP blackout while `KaijuSkylineRenderer` marches an animated monster silhouette through searchlights outside. Customers bring items to `RegisterStation`, where `BarcodeScanner` casts a physical laser across each item's UV-mapped barcode, updates the store ledger in `GameManager`, and slides open the cash drawer for manual or card checkout.
- **Output**: A playable 7-day vertical-slice executable (`728.77 MB`) running at 1080p in Godot 4.7 Forward+ with ACES Filmic tonemapping, paired with a packaged commercial distribution folder (`2,247` files across `.glb`, `.fbx`, Godot `.tscn` prefabs, `2048x2048` channel-packed PBR maps, and turntable renders) ready for Itch.io and Fab at a `$19.99` full-kit tier plus a free 90-file community sample pack.

## Where It Stands & Next Steps

*Kaiju Kiosk* is **shipped** and certified across all seven production milestones (`M1` through `M7`). On disk at `D:\Projects\KaijuConvenience`, the project spans `8,657` files (`3.46 GB`) and `185,178` lines of handwritten source code across `618` files (`549` GDScript files, `40` Python pipeline tools, `25` `.gdshader` shaders, and `3` HTML studio/audit dashboards). Automated verification passes `28` headless test suites totaling `7,544` assertions (`67/67` release gates) with zero script or asset-metric regressions, and the 5-cycle autonomous computer-vision swarm raised the live walkthrough audit score from `90.29` to `94.21/100` across `2,160` rendered frames.

Next steps to expand commercial distribution:
- Publish the packaged `$19.99` *Neo-Tokyo Kombini & Shaders Kit* and 90-file Free Sample Pack storefront pages onto Itch.io and Epic Fab using the pre-rendered 1080p dollhouse and contact-sheet galleries.
- Expand the 7-day `OS.has_feature("demo")` slice into the full 90-day Steam Early Access campaign arc by wiring mid-season faction supply shortages and backroom generator upgrades into the live store ledger.
- Record a 60-second Steam store trailer cutting directly between calm barcode-scanning ASMR loops and full EMP kaiju tremor sequences.

## Under the Hood & Local Files

### Engine & Shader Architecture
The game runs on Godot 4.7.1 Stable (Forward+ Vulkan renderer) coordinated through six decoupled autoload singletons: `SignalBus`, `GameManager`, `AudioManager`, `SaveManager`, `WeatherManager`, and `TutorialManager`. Two custom shaders carry the signature comic-ink look:
- [ps2_cel_shader.gdshader](file:///D:/Projects/KaijuConvenience/shaders/ps2_cel_shader.gdshader) evaluates a 3-band stepped toon ramp, unpacks channel-packed `2048x2048` `_orm.png` textures (`R = Ambient Occlusion`, `G = Roughness`, `B = Metallic`), and supports dual-sided transparent bento lids via `cull_disabled` with backface normal inversion (`NORMAL = FRONT_FACING ? NORMAL : -NORMAL`).
- [ps2_outline.gdshader](file:///D:/Projects/KaijuConvenience/shaders/ps2_outline.gdshader) renders inverted-hull comic ink outlines clamped across `[0.3m, 30.0m]` camera distance while locking `depth_bias = 0.001` (`POSITION.z -= depth_bias * POSITION.w`) to prevent coplanar z-fighting on thin shelf price rails and magazine covers.

### Procedural Blender 5.1 PBR Factory & Dual-Gate QA
All hero store fixtures and merchandise were built and verified locally on an 8 GB RTX 4060 Laptop GPU:
- **Sub-Component Kitbashing**: [blender_components_library.py](file:///D:/Projects/KaijuConvenience/tools/blender_components_library.py) provides eight procedural `bmesh` sub-component factories (beveled handles, cooling louvers, POS touchscreens, keypad buttons, can pull-tabs, caster wheels, refrigeration compressors, and power cables) to assemble six hero stations (`cashier_counter`, `drink_cooler`, `gondola_shelf`, `slushie_machine`, `breaker_panel`, and `weapons`), enforcing `>1,200` triangles and hardened chamfer normals.
- **Headless Cycles GPU Baking**: [blender_pbr_baker.py](file:///D:/Projects/KaijuConvenience/tools/blender_pbr_baker.py) runs headless Blender 5.1 Cycles (accounting for Blender 5.1's renamed `Specular IOR Level` and `Transmission Weight` Principled BSDF sockets) to bake true geometric curvature edge wear, raytraced cavity grime, and micro-roughness into `2048x2048` `_albedo.png`, `_normal.png`, and `_orm.png` maps.
- **Merchandise Atlases & Dual-Gate Verification**: [generate_kombini_decals.py](file:///D:/Projects/KaijuConvenience/tools/generate_kombini_decals.py) authors 2K drink, snack, and bento atlases mapped with `<15%` UV texel-density variance. Gate 1 ([audit_asset_metrics.py](file:///D:/Projects/KaijuConvenience/tools/audit_asset_metrics.py)) checks manifold geometry, triangle counts (`>180` tris per prop), UV variance, and high-frequency Laplacian texture detail ($\sigma^2(\nabla^2 I) \ge 15.0$). Gate 2 ([adversarial_visual_judge.py](file:///D:/Projects/KaijuConvenience/tools/adversarial_visual_judge.py)) scores multi-angle 1080p turntables against a 10-point commercial rubric before [package_commercial_asset_kit.py](file:///D:/Projects/KaijuConvenience/tools/package_commercial_asset_kit.py) compiles the final marketplace archives.

### Key Local Files
- Project Configuration & Blueprint: [project.godot](file:///D:/Projects/KaijuConvenience/project.godot), [PROJECT.md](file:///D:/Projects/KaijuConvenience/PROJECT.md), [AUDIT_REPORT.md](file:///D:/Projects/KaijuConvenience/AUDIT_REPORT.md)
- Primary Entry Scene: [Main.tscn](file:///D:/Projects/KaijuConvenience/Main.tscn)
- Visual Review & Asset Dashboards: [gallery.html](file:///D:/Projects/KaijuConvenience/output/visual_review/gallery.html), [asset_health_dashboard.html](file:///D:/Projects/KaijuConvenience/output/visual_review/artist_audit/asset_health_dashboard.html), [index.html](file:///D:/Projects/KaijuConvenience/tools/studio/index.html)
- Shipped Executables & Packs: [KaijuKiosk_Demo.exe](file:///D:/Projects/KaijuConvenience/export/KaijuKiosk_Demo.exe), [neo_tokyo_kombini_kit](file:///D:/Projects/KaijuConvenience/export/neo_tokyo_kombini_kit)
