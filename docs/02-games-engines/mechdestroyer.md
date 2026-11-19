---
id: "mechdestroyer"
title: "MechDestroyer: 3D Tactical Mecha Combat Simulator"
subtitle: "Original Godot 4.7 tactical mech simulator featuring a 76-chassis procedural roster, destructible urban blocks, diegetic cockpit optics, and 4-player co-op."
pillar: "02-games-engines"
entry_type: "project"
readiness: "active-build"
visibility: "main"
date_started: "2026-08-16"
date_updated: "2026-11-19"
tags:
  - "godot-4-7"
  - "mecha-simulator"
  - "cel-shading"
  - "destructible-environments"
  - "enet-multiplayer"
  - "procedural-3d"
metrics:
  - label: "Source Code"
    value: "86,348 LOC"
  - label: "Procedural Roster"
    value: "76 Chassis"
  - label: "3D Mech & Prop GLBs"
    value: "87 Models"
  - label: "Certified Test Suites"
    value: "117 / 117 Passing"
  - label: "E2E Assertions"
    value: "859 Passing"
  - label: "Static Script Audit"
    value: "160 / 160 Clean"
  - label: "Windows Export"
    value: "Reproducible"
  - label: "Executed Milestones"
    value: "33 Plans"
media:
  - src: "assets/media/mechdestroyer/combat-cockpit.png"
    kind: "authentic"
    caption: "Godot 4.7 capture of MechDestroyer tactical combat with cel-shaded chassis, diegetic cockpit HUD, and urban skyline."
  - src: "assets/media/mechdestroyer/betty-target-acquired.wav"
    kind: "audio"
    caption: "Cockpit Betty Annunciator Sample — Target Acquired tactical callout"
  - src: "assets/media/mechdestroyer/betty-heat-critical.wav"
    kind: "audio"
    caption: "Cockpit Betty Annunciator Sample — Reactor Heat Critical warning"
diagram: ""
tech_stack:
  - "Godot 4.7 (Vulkan Forward+)"
  - "GDScript"
  - "Godot Shader Language (GLSL)"
  - "ENet Authoritative Multiplayer"
  - "Blender 5.1 & TRELLIS 2"
  - "Python 3 Mesh & Audio Synthesis"
local_paths:
  - label: "MechDestroyer Project Root"
    path: "file:///D:/Projects/MechDestroyer"
  - label: "Kitbash Mech Scrapyard Blend"
    path: "file:///D:/Projects/MechDestroyer/Mech_Scrapyard.blend"
  - label: "Automated Test Suite Runner"
    path: "file:///D:/Projects/MechDestroyer/tests/run_all_tests.gd"
run_commands:
  - label: "Launch MechDestroyer in Godot 4.7"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --path \"D:\\Projects\\MechDestroyer\""
  - label: "Run Full Headless Test Suite"
    command: "\"D:\\SteamFiles\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe\" --headless --path \"D:\\Projects\\MechDestroyer\" -s res://tests/run_all_tests.gd"
memory_ids:
  - "5b4c5771-b2a2-4574-85b2-6f6abba4f999"
  - "bd6c8db6-abfa-4083-a5e3-87f35dd22180"
  - "ba113b98-1b3a-4b05-8f81-f3b718aae4db"
  - "b6886761-c3fa-472b-bd1d-67ec449e8f5f"
  - "abfaf312-b8e3-4b8e-b5a5-6aae8da5145d"
  - "3b086b41-3501-4c4f-84bc-a86fe511f932"
  - "a377e348-adf4-440b-b47b-b2e4403e94b9"
  - "b7112269-0eb9-4774-9cc6-c84ed50b484d"
  - "81f72148-b32e-492b-8004-059274c095d6"
  - "ff067e02-bdbd-41a3-abed-d21cde51da7e"
  - "54cc5e0d-5def-477f-a0b7-d0b45168c4b7"
  - "d1c2b92d-1d3c-4aa3-9cb4-9710a527b3ff"
  - "09e496a2-b998-4b59-92d7-9d9f5b520221"
  - "cefdc2cb-d982-4ca7-9ae7-1e679ed52d59"
  - "cfa36d26-4b0d-4d95-b951-3e7edec7fdab"
  - "84195120-bc77-4567-994e-8a2559bada3e"
  - "80add12d-dd4d-42f4-a8d6-a6c028bf5571"
  - "263acc6d-e55d-4e70-99db-1cc76fa99f42"
  - "6fbacf5c-42c8-41f1-af4c-3b57923b3013"
  - "8b42a61f-46b1-4a00-a613-cc433db53de8"
  - "0eea5469-3ea6-42a4-9393-712d4256cf5e"
  - "8f0ca0ca-d5d2-4972-8f47-352d5cc2f86c"
  - "b3b48955-7553-403b-9615-9599863dba84"
  - "d695d2f3-41cf-4b8f-bec9-fe39614d3e23"
  - "efe83425-a7ec-43f0-b385-2408bf7f0790"
  - "21ab21ee-0500-47d2-9267-f4542cd1c43e"
  - "b206ea03-5c7a-4ca6-a15d-214ccd7826b0"
  - "8f240390-7486-480c-a0e6-c3099fc89a21"
  - "7b3bb579-358c-445d-948f-b0c3b1eb6a9a"
  - "4b5fbaf0-e5a4-4232-a385-e2556e9cdefb"
  - "9a68dfa0-8c8e-40cb-8c92-592954ac8e9f"
  - "e904b7ac-9595-46bf-b0f2-c1e0aa4d3eaf"
  - "bc541701-05a8-4656-8783-fc30458650ae"
  - "d0d59c5b-f1d3-474a-a9f9-1837d2ee1c90"
  - "199ffc3e-6e8c-48ff-9b44-a976603fcb04"
  - "61f47070-3959-4824-bfbd-490e205c9035"
  - "546808bb-b027-4c99-8203-bf8dbaff2239"
  - "ed23bff9-42d7-4217-8a25-ee6cbbe1ea41"
  - "89cda4be-b687-410d-8881-90d16e3a3979"
  - "440ab9d2-c5b1-4fea-a364-d225b40266dc"
  - "f03eb7da-b6f8-4527-9645-5e3e3bc4df2c"
  - "af2016ae-e53e-4a8b-a4bf-47b94370b2cc"
  - "ba036f99-c817-46f0-8a83-2c4171a5f63a"
  - "b1d82b95-e1ae-4875-b534-ef7b51bb0189"
  - "71dc1ad5-92e9-48df-aa92-028812f44e98"
  - "797126b0-c879-4b19-90ba-5626e5dae544"
  - "416882ed-5a1c-4df0-8146-88159665c309"
  - "42a05a13-65ab-4fea-8986-8fe3c62ec02e"
  - "f29dc1e5-7eb1-41ae-bf97-b775ad71778d"
  - "49be9739-4bc2-4d0a-a2cd-16b903edd962"
  - "a6145e3d-92c3-4fdc-af64-0d152a4b795c"
  - "ce4820c8-3110-4b35-ba9c-38a319eb3eeb"
  - "812a57aa-76e8-4db2-946e-cf49927696a1"
  - "b0acb70e-b170-4ed7-8264-6c47d7e78358"
  - "2462022f-2b1c-4e67-9593-cb849d12280a"
  - "486b1734-a9a7-47fc-890c-cf0c88cbc2ea"
  - "200a4840-3686-4cc2-9f06-6111a0ebb6ea"
  - "6d322e83-732e-479a-8a54-1cae9f287e36"
  - "37e91881-dbe3-428b-b878-acc72e2d5904"
  - "ed6b0fa9-572f-4e79-be74-2433c2f2fc1c"
  - "443ba63c-6815-48d3-967c-48dceaab227f"
  - "c3499a7d-d51a-4369-9611-28805e83bb79"
  - "c408e730-ed8f-48d3-b802-4bf629c8bb2e"
  - "ee118dca-a423-4f05-bf79-513de8218c96"
  - "aa126e11-012c-47f8-9df1-850d6e31e98f"
  - "efd267e1-c1af-4823-904b-71e8953eb83d"
  - "7064ee7c-19a8-4a44-8353-3004970a8006"
  - "00ebd4f1-4283-4b09-b009-f85f1ee63538"
  - "9a24f37b-2ecd-48d4-8850-5c6d7ef3f19a"
  - "90160144-53ca-4738-b68a-e8271e63cea6"
  - "a1489f42-e03c-4e96-baed-edd1d5c38e27"
  - "66b2707d-abec-40a6-b77a-ab32ba4e941a"
  - "dd8bf625-b99a-4109-89c6-2b6fd1f329e5"
  - "dc8bc19b-fe86-439f-8996-b7829e023d2f"
  - "cbe6a4de-76a8-4ba7-ad82-5076f0d10c6a"
  - "c2163252-2bf3-407c-9b52-02c06f6c6146"
  - "8cbaefeb-2ca7-47aa-a719-3b8374502719"
  - "1367563e-c2a3-46d0-9c5d-fe66cc4da833"
  - "60fdefa8-6e38-4151-967d-48097fc67ff5"
  - "43356d03-9325-4891-b4cf-62799a9407aa"
  - "10bf78a9-d1eb-4c25-b3d5-e8a1231beab6"
  - "600e1212-8406-4439-a155-8bf468c8c1af"
  - "5642ee2f-9a89-4441-99a0-106416fbb547"
  - "07d4f367-f8ec-47c9-8f01-c42501645126"
  - "cbc1f33b-3e3a-493f-a2b0-ff101fabb1a8"
  - "251f7391-fe6a-4f13-9e24-73e10427beff"
  - "860d70c7-32c8-46f1-bfc8-d6300c9afd36"
  - "932f1d2d-0e2c-427c-95bb-47374f203c55"
  - "a4d5a1db-11d1-4028-ba51-3089366bcb4c"
  - "5325bd58-c2f2-4183-b53f-e843cd6557e7"
  - "0810e8a7-7158-4798-8be1-262c4a9940c8"
  - "a5b14fd4-942d-425d-ab4b-f19b31eced85"
  - "d2a67c0d-5403-4cec-aabc-20db39a00fe6"
  - "308b1b0d-f549-4c9d-a69b-666f9e1b2dab"
  - "ef370487-b9d0-4f76-b86d-07c6b5a069a3"
  - "2943bc8d-6263-4e68-83d6-6842caa28f13"
  - "45b94b9b-bcf2-464a-b76f-8328a5a3da32"
  - "4aca6fe7-c4a9-491c-acd2-007790e938ab"
  - "14aeee7a-43fe-47f1-888d-045f6da2f47e"
  - "3a1bcf52-6442-40d3-9b8f-9cb92c7d7db4"
  - "848e879f-65e4-4b2f-beaa-1a40dd88083a"
  - "7ad65732-0177-486f-97f6-25b8994da583"
  - "e338abac-dc6f-4b2b-836a-6769ac7d5af3"
  - "d4e8e36f-15a2-4f45-9c1f-d137362903c6"
  - "c8ca0d93-d5e8-438d-b9e1-8bb4420a3888"
  - "59696405-ece2-41b3-a27b-52f756eaf142"
  - "bce03ad4-d862-430b-971b-a731f7ac07ea"
  - "3de28c25-2917-4c2d-8ad2-184cdfb0d51f"
  - "3d666a57-2f67-47e6-85e4-5d71aca2815a"
  - "c5691a1f-b48c-4277-b3de-7af6b9142952"
  - "994b3674-8f7e-4535-9385-e8539a16926b"
  - "063b4040-f396-4d39-bf4d-6ca919196fc8"
  - "65c8864c-06ad-4324-b853-490654db97ea"
  - "ef49d31e-0cc1-40c9-b62c-2f3cee3bca94"
  - "948df57f-ec27-4176-ae94-7e1289c85643"
  - "98b0e0a4-cc0d-4d6c-82b4-3716d3a18a50"
  - "bbd2ff8e-8463-470d-b513-f23558bbee3f"
  - "9c30d4ed-6e2e-4545-b976-9426d24159ee"
  - "5a91d059-9b09-432f-9d48-426b4301ef13"
  - "0007216f-9aa3-466d-8bd2-66f4b4e9f59a"
  - "1b31242c-0335-45dc-9741-1c74d00bebca"
  - "c0addddd-2eac-4174-abad-6a1411d3a03b"
  - "bac297b5-1381-4a34-893e-f108d30a5723"
  - "db507977-1e02-4c05-a82a-af805948dff2"
  - "7b95572d-b589-430c-8238-eacc71f59dfe"
  - "a6c8fc57-4ad7-43a3-bcd1-3d54da769282"
  - "0cc22019-1fd5-4610-93c8-08dd1ebbfd68"
  - "44e06a84-b878-4164-a841-e59906d522aa"
  - "83f7bc53-8e50-4aa6-9e96-eb7ee51e6869"
  - "e1a8f6dc-6997-4d4e-9315-38749d36015d"
  - "902950d4-c6a0-4153-9315-b4a2f175b300"
  - "4725cdd2-a6e2-4c5d-99d2-ae1f4dd9d9d5"
  - "6f4e3625-9844-4c9b-8e6b-d13f0650cb43"
  - "8d2c983e-60b6-4f53-91ee-a139966e9ac1"
  - "618e1d8b-03c6-4740-9a97-b71fb47fc238"
  - "0431e403-f6ef-47b6-b7e0-b1659ea2a04a"
  - "b5da0236-0c5f-4097-adfe-78cd45a456b7"
  - "f1bcc136-9d48-49bd-8478-c9278d160d43"
  - "3ff14382-a7d7-4a99-b096-7832c2a0b533"
  - "53024523-0146-49f4-9ad6-46d1c791ee48"
  - "aeae02e5-7f85-4ed6-82e7-2cfa65ee1140"
  - "4c06da8c-e5f5-47f5-9abc-e00b33229769"
  - "89164272-1338-47a8-9a98-89867fe9c408"
  - "59c1d60f-9868-4edf-9bbb-563d9490bc67"
  - "cf43d6cb-c1e1-4f91-84d5-15d7ea62b560"
  - "2baf835a-25b4-410f-966c-3f1ff2430303"
  - "59b459d7-3670-42f4-a21b-4cd95448d3ef"
  - "c8b70c76-bc9f-4283-bbc6-6bf0ae19b8ee"
conversation_ids:
  - "eaebd7f3-6a79-4f5a-bd76-b740e50b4b53"
  - "b58561ad-cbd6-4d6e-a3cc-3b787e62b1e8"
  - "89e548b4-45ee-4c98-9fa3-11b0a1e1818a"
  - "a578a667-2dd8-447d-9904-910966aa3a2f"
  - "7a4f2f46-2f5b-482a-8a61-cddd583c4caa"
  - "7ebcdc5b-4143-4b22-9904-c93509a19dcc"
  - "4b323442-765b-41e3-a183-d51e6d6b79a6"
  - "d974faac-d0f7-4313-85eb-75dd5fa1bc41"
  - "34a0858f-8690-4bd7-8cf5-b2c326d608da"
  - "88f2f709-24c7-442e-b5af-c13266b6581b"
  - "42cc25cd-c0f5-4045-a77d-27444791e976"
  - "d4d0a371-7752-46dd-a936-b689806638fa"
  - "e54119bd-0c05-4718-806e-3ad707a4b620"
  - "0af3025f-7a23-4d9f-bfc9-b663ab0eb17b"
  - "0948514e-8cf5-4ba6-abf6-da3bd5da0f79"
  - "8bb9dcb9-0a57-4380-bc89-3ce227fbbe71"
  - "4b5bdc93-4963-4aa6-bfc8-458fe0de9858"
  - "43987bf6-72b4-4daf-a32e-4a3d4d1e80d4"
  - "6f4ceb7a-a1ff-4d1c-beba-d3aa259d8984"
  - "0dcbb5fe-3d5d-48ee-b3d3-fe980f8e3212"
  - "b8399915-0447-4834-b67c-902ea6c72e92"
  - "a9aa9c58-1f1f-4c33-a857-a675e258ae1e"
  - "1d5c6565-16df-4c88-9029-e07ae68b9738"
  - "e8df3b4b-dfd9-447f-9074-e441e3e63135"
---

## What It Is & Why It Matters

*MechDestroyer* is an original, commercially clean 3D tactical mecha simulator built natively in Godot 4.7 Forward+. You pilot 30-to-100-ton walking war machines from inside a physical 3D cockpit with decoupled `±120°` torso twist, throttle momentum, jump-jet thrust, localized 8-zone armor and internal structure paper-dolls, reactor heat curves, emergency coolant flushes, and cascading multi-story skyscraper collapses. Visuals pair 3-tone cel shading and post-process Sobel ink outlines with ground-level urban smog pierced by toggleable Thermal IR and Night Vision cockpit optics.

Early binary reverse-engineering experiments taught us how classic 1990s sims achieved mechanical weight, but shipping a commercial product required 100% original geometry, lore, audio, and code. Over 33 sequential engineering plans (`148` Unified Memory Bank architectural records), we expanded *MechDestroyer* into a full mercenary simulator—complete with a 76-chassis procedural walker roster, *MechWarrior 4*-inspired sized and typed hardpoint customization, a 32-layer `2048x2048` livery decal paint bay, Solaris-style gladiator arenas, VTOL and armored-convoy combined arms, and 2-to-4-player ENet online co-op.

## Real Example: How It Works in Practice

- **Input**: In the Hangar Loadout Builder (`LoadoutBuilderUI.gd`), you refit a 75-ton Heavy Sniper chassis with dual kinetic railguns, homing missiles, and `0.5`-ton jump jets, deploy via orbital DropShip into `UrbanAssassinationMission.tscn`, press `V` to switch your visor to Thermal IR through dense street smog, hold the Lance Command key to order wingmen to flank right, and core the lower stories of a sniper-occupied skyscraper.
- **What Happens**: Holding the command key triggers `CommandWheelHUD.gd`, dropping `Engine.time_scale` to `0.20` while you select `FLANK_RIGHT`; releasing restores real-time physics and dispatches lateral formation vectors to `WingmanAI.gd`. Firing railguns applies directional pitch kick to `CockpitController.gd` and spikes reactor temperature in `HeatSystem.gd`, prompting `BitchinBetty.gd` to play `heat_critical.wav` over multi-layer hydraulic actuator audio. When lower-floor structural HP on `DestructibleBuilding.gd` hits zero, upper stories fracture via `RigidBody3D` cascades, shake nearby cockpits based on mass and distance, and settle into `StaticBody3D` rubble mounds (`<=45°` slope) that mechs can climb for hull-down cover.
- **Output**: A playable 4-stage urban assassination vertical slice (`Infiltration -> Thermal ECM Jammers -> Plaza Ambush -> DropShip Boss`) backed by `87` `.glb` 3D models, `86` `.wav` tactical voice and weapon assets, `117` certified headless suites carrying `859` E2E assertions, and a byte-reproducible Windows export.

## Where It Stands & Next Steps

*MechDestroyer* is an **active-build** vertical slice with Phase 1 Milestones `M1` through `M5` and expansion Plans `#01` through `#33` verified in headless testing. On disk at `D:\Projects\MechDestroyer`, the project totals `1,802` files (`1.36 GB`) and `86,348` lines of code across `421` source files (`404` GDScript files at `79,952` LOC, `9` Python mesh/audio generators at `6,017` LOC, and `8` `.gdshader` shaders), plus `32` `.tscn` scenes, `82` `.tres` resources, and `119` test scripts in `tests/`.

The 2026-11-18 hardening pass closed the gap between "passes on the workstation" and "certified": `117 / 117` suites now pass a runner that fails on leaked objects or resources at exit, fails any suite that logs an assertion failure even when it exits `0`, and fails any suite that executes zero assertions. The static audit covers `160 / 160` scripts. `TEST_READY.md` records the run on Godot 4.7.2-stable and maps `859` E2E assertions across the four tiers. A reproducible Windows export now exists in `build/windows/` together with `SHA256SUMS.txt` and `BUILD_INFO.txt`, and `.github/workflows/tests.yml` runs the audit and the full suite on every push and pull request.

Next steps toward a public demo:
- Sign the exported Windows binary and add Linux and macOS presets so the same reproducible script covers all three desktop targets.
- Swap remaining kitbashed proxy props for baked `2048x2048` PBR meshes from `Mech_Scrapyard.blend` using the headless Cycles baker proven on *Kaiju Kiosk*.
- Run a 4-client WAN latency soak test on the `20 Hz` ENet snapshot interpolator and `200 ms` hitscan rewind buffer.

## Under the Hood & Local Files

### Simulation, Optics & Co-Op Networking Architecture
Key engineering decisions recorded in our Unified Memory Bank (`M0143`–`M0550`):
- **76-Chassis Procedural Roster & IK Stride**: `chassis_dna_library.gd` and Python mutators (`procedural_mesh_mutator.py`, plus 33 local Microsoft TRELLIS 2 2D-to-3D `.glb` chassis packed into [Mech_Scrapyard.blend](file:///D:/Projects/MechDestroyer/Mech_Scrapyard.blend)) generate Light, Medium, Heavy, and Assault silhouettes across reverse-joint avian and humanoid leg rigs with arm-convergence kinematics and leg-destruction limp states.
- **Cockpit Layer Isolation & Visor Shaders**: MFD screens (`MFDRadarDisplay.gd`) are isolated onto render Layer 20 to eliminate near-plane canopy clipping during heavy recoil trauma. Eight custom shaders in `assets/shaders/` handle 3-tone cel lighting (`cel_shader_3tone.gdshader`), Sobel outlines (`outline_sobel_postprocess.gdshader`), `thermal_ir_vision.gdshader`, `night_vision.gdshader`, and progressive windscreen canopy fractures.
- **Authoritative ENet Co-Op (`M0517`–`M0522`)**: Supports 2–4 players with `20 Hz` server snapshot interpolation, `200 ms` lag-compensated hitscan rewind for long-range railgun/laser fire, and live drop-in takeover of AI Lance mates.
- **4-Stem Dynamic Music & 46-WAV Cockpit Audio (`M0529`–`M0536`)**: Combines spatial weapon synthesis (`AudioManager.gd`) with layered footstep thuds, torso-servo whines, and 15 synthesized Betty cockpit callouts (`target_acquired.wav`, `heat_critical.wav`, `armor_critical.wav`).

### Verification & Release Pipeline (2026-11-18)

`tests/run_all_tests.gd` is now a gate, not a report. Every suite must exit clean and print the number of assertions it executed; a suite that logs `SCRIPT ERROR: Assertion failed` fails the run even if it called `quit(0)`, because Godot's `assert()` only aborts the calling function. The zero-leak gate fails any suite that leaves objects or resources alive at exit. Closing the last `12` suites required five distinct fixes:

1. Static `instance` self-references in `15` manager autoloads now clear themselves on `NOTIFICATION_PREDELETE`.
2. Tests that aborted before their `.free()` calls now track created nodes and free them on the exit path.
3. `queue_free()` followed by `quit()` in the same frame became immediate `free()` in five suites.
4. Projectiles, VFX and debris spawned with no scene root now parent to the spawner, so something owns and frees them.
5. `EnemyAIController` parents its `NavigationAgent3D` immediately instead of deferring it into an orphan.

On the release side, `tools/build.sh` exports from a clean output directory, fails the build if Godot logs any `ERROR:` while packing, writes `SHA256SUMS.txt` and `BUILD_INFO.txt`, and produces identical bytes across two clean builds of the same commit. A build is boot-checked with `./build/windows/MechDestroyer.exe --quit-after 300`. `tests/check_all_scripts.gd` and `tests/run_all_tests.gd` run in CI on a Windows runner with Godot 4.7.2-stable, a checksum-verified download, and the same leak and assertion rules.

### Key Local Files
- Project Config & Architecture Specs: [project.godot](file:///D:/Projects/MechDestroyer/project.godot), [PROJECT.md](file:///D:/Projects/MechDestroyer/PROJECT.md), [TEST_INFRA.md](file:///D:/Projects/MechDestroyer/TEST_INFRA.md), [TEST_READY.md](file:///D:/Projects/MechDestroyer/TEST_READY.md)
- Core Simulation & Cockpit Scripts: [src](file:///D:/Projects/MechDestroyer/src), [scripts](file:///D:/Projects/MechDestroyer/scripts), [scenes](file:///D:/Projects/MechDestroyer/scenes)
- 3D Models, Shaders & Betty Audio: [assets](file:///D:/Projects/MechDestroyer/assets), [Mech_Scrapyard.blend](file:///D:/Projects/MechDestroyer/Mech_Scrapyard.blend), [default_bus_layout.tres](file:///D:/Projects/MechDestroyer/default_bus_layout.tres)
- Headless Test Suite & Syntax Auditor: [run_all_tests.gd](file:///D:/Projects/MechDestroyer/tests/run_all_tests.gd), [check_all_scripts.gd](file:///D:/Projects/MechDestroyer/tests/check_all_scripts.gd), [TEST_READY.md](file:///D:/Projects/MechDestroyer/TEST_READY.md)
- Release & CI: [build.sh](file:///D:/Projects/MechDestroyer/tools/build.sh), [tests.yml](file:///D:/Projects/MechDestroyer/.github/workflows/tests.yml), [build/windows](file:///D:/Projects/MechDestroyer/build/windows)
