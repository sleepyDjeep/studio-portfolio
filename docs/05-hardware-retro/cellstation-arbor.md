---
id: "cellstation-arbor"
title: "CellStation Arbor: 8-Bay Auto-Detecting Battery Station"
subtitle: "Bench charger designed as a superior alternative to the Ostation 2 Pro: eight bidirectional buck-boost slots identify NiMH, Li-ion, LiFePO4, 1.5 V lithium and lead-acid cells before any current flows."
pillar: "05-hardware-retro"
entry_type: "project"
readiness: "blueprint"
visibility: "main"
date_started: "2026-11-17"
date_updated: "2026-11-19"
tags:
  - "battery-charging"
  - "cellstation"
  - "chemistry-detection"
  - "buck-boost"
  - "esp32"
  - "solarpunk-enclosure"
  - "safety-electronics"
metrics:
  - label: "Charge Bays"
    value: "8 + 24 Storage"
  - label: "Detection Audit"
    value: "50 / 50 Correct"
  - label: "Unsafe Outcomes"
    value: "0"
  - label: "Per-Slot Stage"
    value: "LM51770 Buck-Boost"
  - label: "4-Slot BOM"
    value: "$214.53"
  - label: "Enclosure"
    value: "300 x 180 x 150 mm"
media: []
diagram: "assets/diagrams/cellstation-arbor.svg"
tech_stack:
  - "C firmware with an MCU-agnostic HAL"
  - "ESP32-S3 target"
  - "LM51770 4-switch buck-boost"
  - "INA228 / MCP4728 / 4PDT polarity"
  - "Python + SVG drawing set"
  - "Host cell simulation (14 archetypes)"
local_paths:
  - label: "Workstation Tools Context"
    path: "file:///D:/Tools/Scripts"
  - label: "Portfolio Diagram"
    path: "file:///D:/Projects/Studio_Portfolio/assets/diagrams/cellstation-arbor.svg"
run_commands:
  - label: "Build and Run the Detection Audit (cloud workspace)"
    command: "make clean && make sim"
  - label: "Regenerate the A2 Drawing Set (cloud workspace)"
    command: "make drawings && node tools/rasterize.js"
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

CellStation "Arbor" is an eight-bay bench charger built for one stubborn problem: a charger that guesses chemistry from voltage alone will eventually put lithium current into an alkaline cell. The commercial reference, the Ostation 2 Pro ($199.99, ASIN `B0G2WFZSQ8`), solves it by refusing almost everything - four bays, 24 storage slots, NiMH and its own Ecolast Li-ion only. Arbor is the opposite bet: identify a broad cell zoo correctly and refuse only what is genuinely unsafe.

The cell zoo is where the difficulty lives. A 14500 Li-ion is physically an AA but needs 4.20 V. A 1.5 V lithium AA needs 4.75-5.5 V at its terminals because a buck converter and charge controller live inside the cell. A NiMH needs delta-peak termination, a LiFePO4 cell tops out at 3.6 V, and an alkaline looks like an aged NiMH on voltage alone. Getting any of those wrong ranges from a ruined cell to a fire, so the station treats detection as a measurement problem, not a lookup table.

The physical design matches the ambition. The enclosure is a 300 x 180 x 150 mm solarpunk cabinet - ash and brass, borosilicate glass over the cells, moss and pots - with eight 62 x 18 mm wells on a 68 mm pitch, a rear console wedge, a 24-cell drawer at 22 mm pitch and a 40 mm exhaust fan. A five-sheet A2 drawing set (general arrangement, 1:1 charge deck, sections, exploded view, render) is generated from one shared dimension model so the drawings, render and firmware geometry cannot drift.

This is a **blueprint**: the design package, firmware and host simulation exist and pass their audit, but no board has been fabricated and nothing has been charged on real cells.

## Real Example: How It Works in Practice

- **Input**: Four loose cells go into the deck at once - an alkaline AA at 1.58 V, a NiMH AA at 1.21 V, a 14500 Li-ion at 3.62 V, and a 1.5 V lithium AA at 1.55 V.
- **What Happens**:
  1. Every slot starts with an open-circuit band. The 14500 lands in the Li-ion band; the two AAs land in the low-voltage band where alkaline and NiMH overlap; the 1.5 V lithium sits near the same band and must be separated from both.
  2. The low-voltage slots run a 40 mA current sweep in 43 steps from 0.9 V to 5.2 V, then a two-current DCIR pulse at 50 mA and 400 mA. Alkaline cells show 200-700 mOhm and a fast rebound; NiMH cells sit near 30-100 mOhm and relax slowly.
  3. The 1.5 V lithium cell fails the plain-cell model, so the slot applies a 60 mA, 150 ms handshake at 5 V. A buck cell accepts it and reports the internal controller; a primary cell does not, and is refused.
  4. Each classified slot receives its profile: 1.45 V delta-peak for NiMH, 4.20 V CC/CV for the 14500, 5.0 V CC/CV with a 5.55 V hard ceiling for the buck cell, and a refusal with a reason for the alkaline.
- **Output**: Three cells charging on the correct profile and one refused with a readable reason, with every slot's voltage, current, DCIR and accumulated charge on the deck display.

## Where It Stands & Next Steps

The design package is complete on paper and in simulation: a README with the specification and build tiers, five design documents covering chemistries, architecture, detection, safety and the bay-insert manufacturing pack, a four-slot BOM at **$214.53**, an eight-bay enclosure drawing set, C firmware with an MCU-agnostic HAL, and a host simulation that runs the real detection code against 14 cell archetypes.

The audit passes: **50 interviews, 0 misclassified, 0 unsafe outcomes, 0 compiler warnings** under `-Wall -Wextra`, with `make sim` returning 0. It also caught two real bugs before hardware: a full 1.60 V alkaline was misread as aged NiMH until the plateau ceiling moved to 1750 mV, and a 3.3 V Li-ion was assumed to be LiFePO4 until the relaxation-tail thresholds were retuned and the Li-ion polarization resistance raised to 0.15 ohm.

Not done yet:
- No PCB: the KiCad schematic and two-layer layout for the four-slot board are still the next deliverable.
- No ESP32 HAL or single-slot bring-up; the code has only run against the simulated source/sink.
- Deep-discharge precharge, reverse insertion and dirty-contact cases are outside the current audit.
- Nothing has been measured on real cells, and the enclosure drawings are concept geometry, not a fabrication release.

## Under the Hood & Local Files

### Per-Slot Power and Sensing

Each slot is a bidirectional four-switch buck-boost stage built on an **LM51770**, so a 1.5 V NiMH and a 5 V buck cell share the same bay without a second converter. Contacts are four-wire Kelvin pogo pins, which keeps contact resistance out of the DCIR measurement. An **INA228** provides 20-bit voltage/current telemetry and coulomb counting; an **MCP4728** DAC sets the voltage and current target per slot; a **4PDT relay** reverses polarity for a cell inserted backwards; an NTC sits against the cell body. An ESP32-S3 supervises the deck, display and Wi-Fi status endpoint.

Protection has two independent layers: an analogue window comparator that can clamp a slot without firmware, and a firmware supervisor that owns profiles, timers and refusal. The comparator reference tracks the **identified chemistry's absolute maximum**, not the active profile ceiling, because a 5.0 V buck profile and a 4.2 V Li-ion cell can share a bay.

| Identification | Comparator reference |
| --- | --- |
| Unknown / unclassified | 1.80 V |
| NiMH | 1.75 V |
| LiFePO4 | 3.70 V |
| Li-ion | 4.30 V |
| 1.5 V lithium (buck) | 5.55 V |

### Detection Sequence

1. **Open-circuit band** sorts the cell into roughly 1.5 V, 3.6 V, 4.2 V or pack ranges. Voltage alone is never sufficient.
2. **I-V sweep** at 40 mA over 0.9-5.2 V in 43 steps measures slope and knee.
3. **Two-current DCIR** at 50 mA and 400 mA separates NiMH from alkaline and estimates internal resistance.
4. **Plateau test** in the low-voltage band catches a full alkaline cell that would otherwise look like aged NiMH.
5. **Polarization-tail relaxation** in the 2.6-3.55 V band separates LiFePO4 from 3.3 V Li-ion.
6. **5 V handshake** at 60 mA for 150 ms identifies 1.5 V lithium cells that contain their own buck regulator.

Charge profiles cover CC/CV with current taper, NiMH delta-peak and dT/dt, precharge for deep-discharge, coulomb counting, and per-chemistry timeouts. The charge audit recorded NiMH delta-peak at 1492, 1505 and 1400 mV, Li-ion taper at 4197 mV, LiFePO4 taper at 3496 mV and 1.5 V lithium taper at 4970 mV.

### Enclosure and Drawing Set

One dimension model (`tools/geometry.py`) drives every sheet and the render: 300 x 180 x 150 mm envelope, 14 mm plinth, deck at 112 mm, eight 62 x 18 x 14 mm wells on a 68 mm pitch in two rows of four, a rear console wedge sloping 118 to 150 mm over 104-176 mm, a 24-cell drawer at 22 mm pitch, and a 40 mm rear fan with pierced side panels as the only intake. Sheets A-101 (general arrangement 1:2), A-102 (charge deck 1:1, with a 3:1 bay-insert detail), A-103 (sections), A-201 (exploded) and R-001 (render) are A2 landscape at 1 unit = 1 mm.

### Build Tiers and Files

- **Tier 0** (~$60): bench prototype, one slot, no enclosure.
- **Tier 1** (~$210): four-slot board, BOM at **$214.53**.
- **Tier 2** (~$330): eight-slot Arbor deck with the 24-cell drawer.
- **Documents**: `README.md`, `docs/01-chemistries.md`, `docs/02-architecture.md`, `docs/03-chemistry-detection.md`, `docs/04-safety-and-test-plan.md`, `docs/05-bay-insert-manufacturing.md`, `hardware/bom.csv`.
- **Firmware**: `firmware/include/{cell_types,hal,detect,profiles,charger,safety}.h` and `firmware/src/{detect,profiles,charger,safety}.c`.
- **Simulation**: `sim/{cell_model,sim_hal,sim_main}.c` with 14 archetype models and a `make sim` gate that fails on any unsafe outcome.
- [cellstation-arbor.svg](file:///D:/Projects/Studio_Portfolio/assets/diagrams/cellstation-arbor.svg) - power tree, slot sensing and detection flow.
