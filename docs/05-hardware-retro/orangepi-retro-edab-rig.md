---
id: orangepi-retro-edab-rig
title: Orange Pi Zero 2W Retro Gaming & Custom E-Nail Rig
subtitle: Bespoke e-rig parts sourcing guide paired with a modular OpenSCAD chassis sled, RP2040-Zero PID safety
  firmware, and RetroArch CVBS telemetry.
pillar: 05-hardware-retro
entry_type: project
readiness: blueprint
visibility: main
date_started: '2026-11-12'
date_updated: '2026-11-13'
tags:
- hardware-engineering
- openscad-cad
- rp2040-firmware
- orange-pi-zero-2w
- pid-thermal-control
- bespoke-enclosures
metrics:
- label: Internal Sled
  value: 192 × 114 × 38 mm
- label: PID Temp Range
  value: 380°F – 580°F
- label: Gamepad Matrix
  value: 15-Switch 1N4148
- label: Thermal Cutoff
  value: 650°F + 60s Watchdog
media:
- src: assets/media/orangepi-retro-edab-rig/chassis-layout-preview.png
  kind: authentic
  caption: Verified 2D CAD top-view layout exported from chassis_sled.scad showing the 3.5-inch 4:3 CVBS window,
    arcade stick, 6-button arc, 7x M3 mounting ears, and lower-center PEEK hot well.
- src: assets/concepts/orangepi-retro-edab-rig.png
  kind: concept
  caption: 'Concept Preview: Modular charcoal ASA/PETG electronics sled and machined tan PEEK ceramic-bucket well
    beside a carved walnut outer shell with brass M3 inserts.'
- src: assets/concepts/erig-demos/demo-01-walnut-whip-action.png
  kind: concept
  caption: 'Concept Preview — Product Demo 1 (Live Action): Oiled walnut and brass outer shell running 16-bit pixel
    gameplay on the 3.5-inch 4:3 CVBS screen while the machined PEEK ceramic well glows amber above the straight
    borosilicate whip tube.'
- src: assets/concepts/erig-demos/demo-02-smoked-resin-cutaway.png
  kind: concept
  caption: 'Concept Preview — Product Demo 2 (Internal Cutaway): Semi-transparent smoked resin bezel revealing the
    192x114x38 mm charcoal ASA sled, dual Keystone 18650 bays, RP2040-Zero safety MCU, Orange Pi Zero 2W, and isolated
    PEEK hot well.'
- src: assets/concepts/erig-demos/demo-03-dual-shell-artisan-lineup.png
  kind: concept
  caption: 'Concept Preview — Product Demo 3 (Modular Lineup): Portable carved-walnut handheld unit alongside a
    cast-amber/slate resin tabletop dock using the same internal sled mated via a 30 mm silicone collar to a Puffco-compatible
    borosilicate bubbler.'
diagram: assets/diagrams/orangepi-retro-edab-rig.svg
tech_stack:
- OpenSCAD Parametric CAD
- Orange Pi Zero 2W (H618 1GB)
- RP2040-Zero (C++ / PlatformIO)
- MAX31855 + K-Type Thermocouple
- Virgin PEEK + Borosilicate Airpath
- Python 3 RetroArch UDP OSD
local_paths:
- label: Project Hardware & Firmware Root
  path: file:///D:/Projects/OrangePi_EDab_Handheld
- label: Parametric OpenSCAD Chassis Sled
  path: file:///D:/Projects/OrangePi_EDab_Handheld/chassis_sled.scad
- label: Mechanical & Layer Stack Spec
  path: file:///D:/Projects/OrangePi_EDab_Handheld/MECHANICAL_SPEC.md
- label: Complete Wiring & Star-Ground Map
  path: file:///D:/Projects/OrangePi_EDab_Handheld/WIRING_SCHEMATIC.md
- label: RP2040-Zero Gamepad + PID Firmware
  path: file:///D:/Projects/OrangePi_EDab_Handheld/firmware/rp2040_edab/src/main.cpp
- label: Orange Pi RetroArch OSD Daemon
  path: file:///D:/Projects/OrangePi_EDab_Handheld/orangepi/dab_hud.py
- label: Product Demonstration Renders (3 Views)
  path: file:///D:/Projects/OrangePi_EDab_Handheld/renders
run_commands:
- label: Export Printable Sled Body STL via OpenSCAD CLI
  command: openscad -o "D:\Projects\OrangePi_EDab_Handheld\sled_body.stl" -D "part=\"sled_body\"" "D:\Projects\OrangePi_EDab_Handheld\chassis_sled.scad"
- label: Build RP2040-Zero Firmware via PlatformIO
  command: cd "D:\Projects\OrangePi_EDab_Handheld\firmware\rp2040_edab" && pio run
memory_ids:
- 8e423ebb-0267-4582-8649-c8a3120a0e3e
conversation_ids:
- 053ac32c-39e3-42df-b7b0-899323f06658
---

## What It Is & Why It Matters

Building custom artisan e-nail dab rigs—hand-carved hardwood, cast resin, or 3D-printed pieces in both handheld and tabletop styles—runs into two immediate engineering walls: **where to source standardized, replaceable OEM heating cores** without factory alumina-sintering tooling, and **how to keep `400°F–580°F` concentrator heat and reclaim completely isolated** from wood, resin, lithium cells, and computing electronics.

We first mapped the complete DIY and small-batch OEM supply chain (comparing Divine Tribe / SZ Crossing V5 3D alumina buckets, JCVAP rebuildable Peak-style ICA chambers, Lookah 710-thread quartz coils, Varitube/ModMaker spring-loaded 510 decks, Evolv DNA80C/100C boards, and Puffco Peak `29–30 mm` silicone glass sockets). We then ran a full `/grill-me` hardware design lock and engineered our flagship **Orange Pi Zero 2W Retro Gaming & E-Dab Rig** at `D:\Projects\OrangePi_EDab_Handheld\`: a standardized **`192 × 114 × 38 mm` internal ASA/PETG + machined PEEK chassis sled** combining a 4:3 retro console with a hardware-failsafe PID e-nail that bolts cleanly into interchangeable carved wood, cast resin, or printed shells via seven `M3` mounting ears.

## Real Example: How It Works in Practice

Here is what happens electrically, thermally, and on screen during a live gaming and preheat session:

- **Input**: While playing a 16-bit arcade title on the `3.5"` 4:3 composite TFT using the Neo Geo Pocket-style clicky microswitch thumbstick and 6-button Sega arc, you slide the right-edge **Hardware Arm/Lock Switch** closed, roll the side **Temperature Thumbwheel** (`GP26` ADC) to `485°F`, and double-tap the recessed **Fire** button (`GP14`).
- **What Happens**: Even though the heater draws pulsed power from a removable dual-18650 `2S` (`6.2V–8.4V`) sled, a dedicated `5V/3A+` synchronous buck converter and single-point **Star Ground** isolate the **Orange Pi Zero 2W** (`Allwinner H618`) from voltage sag and switching noise. Independently of Linux, the **RP2040-Zero** co-processor reads a spring-loaded K-type thermocouple pressed against the drop-in ceramic bucket via `SPI1` (`MAX31855`), clamps PWM duty cycle on `GP15` so RMS cup voltage never exceeds `4.20V` (`~35–40W`), and drives an 8-LED `WS2812B` ring around the machined **PEEK** well (`2.0 mm` radial air gap from the printed sled). Over internal USB-CDC (`/dev/ttyACM0`), `dab_hud.py` streams `250 ms` JSON telemetry into RetroArch's UDP port `55355`.
- **Output**: RetroArch flashes a crisp non-blocking overlay (`HEAT 412F -> 485F | 7.8V`, then `READY 485F (485F) | 7.7V`) across the 4:3 screen while your game keeps running at `60 FPS`, vapor travels straight down a removable `10 mm` OD borosilicate/316L bottom whip tube for zero-bend iso cleaning, and a `60 s` session timer + `650°F` overtemp trip + `2,000 ms` hardware watchdog guarantee heater shutoff even if Linux is powered off or frozen.

## Where It Stands & Next Steps

All **CAD, mechanical specs, Star-Ground wiring schematics, RP2040 C++ firmware, and Linux OSD daemon files** are authored and verified on disk at [OrangePi_EDab_Handheld](file:///D:/Projects/OrangePi_EDab_Handheld) (`860+ LOC` across OpenSCAD, C++, Python, and technical specs, plus verified `2D` CAD geometry render [layout_preview.png](file:///D:/Projects/OrangePi_EDab_Handheld/layout_preview.png)).

**Current Deliverables on Disk**:
1. **OEM Parts & Artisan Enclosure Sourcing Matrix**: Vetted suppliers for **SZ Crossing / Divine Tribe V5 & Core 2.1** 3D heated alumina cups (`ineedhemp.com`, `discountenails.com`), **JCVAP** rebuildable ICA chambers, **Lookah** 710-thread coils, **Varitube VT510-V2 / ModMaker MM510** spring-loaded connectors, **Keystone 1042** 18650 sleds, **ABR Imagery / Mountain Glass** borosilicate tubing, and platinum-cure silicone airpath seals.
2. **Parametric 6-Target OpenSCAD Sled ([chassis_sled.scad](file:///D:/Projects/OrangePi_EDab_Handheld/chassis_sled.scad))**: Exports `sled_body`, `front_bezel`, `battery_door`, `peek_well` (CNC lathe reference: `Ø32 mm` OD, `Ø23 mm` ID bore, `Ø36 mm` sled pocket for a `2 mm` air gap), `outer_cutout_template` (`192.6 × 114.6 mm` wood-routing/resin jig with 7× `M3` drill guides), and full `assembly`.
3. **Star-Ground & BTL-Safe Audio Schematic ([WIRING_SCHEMATIC.md](file:///D:/Projects/OrangePi_EDab_Handheld/WIRING_SCHEMATIC.md))**: Maps all 20 castellated edge pins on the `RP2040-Zero` (zero underside pad soldering), the `4×4` `1N4148` anti-ghosting switch matrix, the physical MOSFET Gate interrupt (`Arm Switch -> 100Ω -> Gate` with `10kΩ` pulldown + `SS34` flyback diode), and a split `MAX97220` headphone + `PAM8403` `/SHDN`-muted speaker topology that avoids Bridge-Tied Load ground shorts on the switched `3.5 mm` TRS jack.
4. **Product Demonstration Render Suite ([renders/](file:///D:/Projects/OrangePi_EDab_Handheld/renders))**: Three 16:9 industrial product visualizations covering live carved-walnut whip operation, a smoked-resin internal ASA sled cutaway, and the modular handheld + cast-resin tabletop bubbler lineup.
5. **Firmware & RetroArch Telemetry Stack**: PlatformIO C++ firmware ([main.cpp](file:///D:/Projects/OrangePi_EDab_Handheld/firmware/rp2040_edab/src/main.cpp)) + Armbian `systemd` UDP OSD service ([dab_hud.py](file:///D:/Projects/OrangePi_EDab_Handheld/orangepi/dab_hud.py)).

**Next Steps**:
1. Print the `sled_body` and `front_bezel` test fit in ASA, machine the virgin `PEEK` insulator sleeve, and bench-test `2S` RMS voltage clamping across a `0.48 Ω` V5 ceramic cup with a multimeter and K-type probe before mounting the Orange Pi.
2. Route the first oiled walnut handheld shell and cast-resin tabletop dock using the exported `outer_cutout_template` STL jig.

## Under the Hood & Local Files

### Key Hardware & Safety Decisions
- **Why Split 2S Heater Power from a Dedicated 5V/3A Buck**: Driving a `35W` ceramic heater from a shared `5V` boost rail brown-outs Linux SBCs. Pulling heater current straight from two high-drain `18650` cells in `2S` (`16 AWG` silicone leads + `10A` heater fuse) while feeding the Orange Pi Zero 2W (`Pins 2 & 4`), audio amp, and LEDs from a separate `5V/3A+` synchronous buck eliminates `5V` rail sag.
- **Why Dynamic RMS Duty Clamping (`MAX_CUP_VRMS = 4.20V`)**: Standard V5 / Core 2.1 cups are wound for single-cell (`3.7V–4.2V`) resistance (`~0.45–0.50 Ω`). On an `8.4V` charged `2S` pack, unthrottled `100%` duty would quadruple power (`~145W`) and crack the glaze; `main.cpp` continuously samples `VBATT_SENSE` (`GP28` `100kΩ/22kΩ` divider) and caps `maxDuty = (4.20 / packVoltage)^2` (`~25%–47%` max PWM) while locking out below `6.20V` (`3.1V/cell`).
- **Why CVBS Composite + 24-Pin Expansion Board**: Tapping the official 24-pin expansion board's `CVBS TV-Out` (`Sleeve`) and `LINEOUT_L/R` (`Tip/Ring1`) drives an inexpensive `$8–$12` `3.5"` 4:3 automotive/retro TFT with zero SPI framebuffer CPU overhead and leaves GPIO/USB free for the `RP2040-Zero` composite HID + CDC link.
- **Why Straight-Shot Bottom Vapor Path**: Routing a straight `10 mm` OD borosilicate or `316L` stainless tube vertically out the bottom of the PEEK well through high-temperature silicone O-rings keeps hot reclaim out of the electronics cavity and lets a single pipe cleaner or iso soak clear the entire vapor path in seconds.

### Local Repository Files
- [chassis_sled.scad](file:///D:/Projects/OrangePi_EDab_Handheld/chassis_sled.scad) — Parametric OpenSCAD source (`415 LOC`) with 6 STL export modes including the wood/resin router template.
- [MECHANICAL_SPEC.md](file:///D:/Projects/OrangePi_EDab_Handheld/MECHANICAL_SPEC.md) — Exact `X/Y/Z` millimeter stackup (`Z = 0..38 mm`), button arc coordinates, and PEEK `2 mm` air-gap tolerances.
- [WIRING_SCHEMATIC.md](file:///D:/Projects/OrangePi_EDab_Handheld/WIRING_SCHEMATIC.md) — `2S` Star-Ground power tree, castellated `RP2040-Zero` pin table, `4×4` `1N4148` diode matrix, and BTL-safe audio muting circuit.
- [main.cpp](file:///D:/Projects/OrangePi_EDab_Handheld/firmware/rp2040_edab/src/main.cpp) — `338 LOC` C++ firmware implementing USB HID 12-button + hat gamepad scanning, `MAX31855` PID loop (`Kp=3.2, Ki=0.08, Kd=1.4`), hardware watchdog, and `WS2812B` status ring.
- [platformio.ini](file:///D:/Projects/OrangePi_EDab_Handheld/firmware/rp2040_edab/platformio.ini) — `earlephilhower` `rpipico` PlatformIO build config with `Adafruit MAX31855` and `Adafruit NeoPixel`.
- [dab_hud.py](file:///D:/Projects/OrangePi_EDab_Handheld/orangepi/dab_hud.py), [dab-hud.service](file:///D:/Projects/OrangePi_EDab_Handheld/orangepi/dab-hud.service), & [README_SETUP.md](file:///D:/Projects/OrangePi_EDab_Handheld/orangepi/README_SETUP.md) — Armbian `tvout` setup guide and `systemd` daemon bridging `/dev/ttyACM0` telemetry to RetroArch's `127.0.0.1:55355` OSD socket.
