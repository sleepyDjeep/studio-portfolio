---
id: s21u-cyberdeck-mk1
title: 'S21U-DECK MK.I: Snapdragon 888 Steel-Toolbox Field Cyberdeck & KVM Crash-Cart'
subtitle: Complete electrical, thermal, and mechanical blueprint repurposing a broken-screen Galaxy S21 Ultra inside
  a vintage 20 in steel Craftsman toolbox with Hall HOSAS sticks and 5 USB co-processors.
pillar: 05-hardware-retro
entry_type: idea
readiness: blueprint
visibility: main
date_started: '2026-10-27'
date_updated: '2026-11-20'
tags:
- cyberdeck
- hardware-engineering
- samsung-dex
- rp2040
- esp32-s3
- hosas
metrics:
- label: All-New Retail BOM
  value: $608.11 (sourced, live links)
- label: Net Scavenged Cost
  value: ~$470 (After Salvage)
- label: Battery Capacity
  value: 51.8 Wh pack (70.3 Wh w/ phone)
- label: Hardware Co-MCUs
  value: 5 (ESP32-S3 + 3x RP2040 + CANable)
media:
- src: assets/renders/s21u-box-reference.webp
  kind: concept
  caption: 'Housing reference — the actual unit: ribbed grey steel body, twin draw latches, centre padlock hasp, red Craftsman badge and a riveted piano hinge. It forced the twin front plates, the backer plates and the lid subframe.'
- src: assets/renders/s21u-deck-revb-steel.png
  kind: concept
  caption: 'Housing concept — the 20 × 9 × 9 in ribbed Craftsman box as it actually looks: twin draw latches, centre padlock hasp and red badge on the front wall, flaking paint, and the 10.1-inch panel on a riveted subframe in the lid. Part placement is indicative; the assembly sheet carries the dimensions.'
- src: assets/renders/s21u-deck-revb-deck.png
  kind: concept
  caption: 'Deck concept, looking down into the open box — 488 × 208 mm plate at the rim with Hall grips stowed in the left-hand wells, 60% keyboard, trackpad, rear power strip and a connector plate on the right. Indicative only: the cut sheet fixes the zoning and the twin plates that flank the hasp.'
- src: assets/concepts/s21u-cyberdeck-mk1.png
  kind: concept
  caption: 'Concept Preview: S21U-DECK MK.I ruggedized Apache 2800 cyberdeck with 10.1-inch DeX display, fold-out
    Hall HOSAS sticks, ortho keyboard, and 4-MCU diagnostic bay.'
- src: assets/concepts/s21u-configs/config-a-apache-hosas-simpit.png
  kind: concept
  caption: 'Concept Preview — Layout A (HOSAS Simpit & Retro Deck): Apache 2800 hardcase with 10.1-inch DeX display,
    fold-out dual Hall-effect flight sticks in -36 mm side wells flanking a 40% ortho keyboard, and front 3.5 mm
    TRRS + dual USB gamepad I/O.'
- src: assets/concepts/s21u-configs/config-b-kvm-crashcart-hardware-lab.png
  kind: concept
  caption: 'Concept Preview — Layout B (Server KVM & Hardware Lab): 60% tactile keyboard + optical thumb trackball
    paired with a top anodized bulkhead patch bay (HDMI-IN KVM, RJ45, SMA 2.4 GHz whip, 8-pin sigrok logic terminal,
    GX12 CAN socket, kill-switches, and INA226 OLED).'
- src: assets/concepts/s21u-configs/config-c-slim-aluminum-field-tablet.png
  kind: concept
  caption: 'Concept Preview — Layout C (Modular Field Tablet-Deck): 13.3-inch CNC aluminum and carbon-fiber kickstand
    slate with detachable magnetic keyboard and rear open-bay coldplate dock (finned heatsink + 5015 blower on stripped
    S21U board + dual 100W USB-C PD / microSD / SDR rail).'
diagram: assets/diagrams/s21u-cyberdeck-mk1.svg
tech_stack:
- Snapdragon 888 (Samsung DeX / Termux:X11 / Winlator)
- IP2368 100W Bi-Directional USB-PD PPS
- ESP32-S3 (Bruce / Marauder RF)
- 3x RP2040-Zero (KVM HID + 120 MHz sigrok Logic)
- CANable STM32 (SocketCAN / SLCAN)
- Ginfull Hall-Effect HOSAS Gimbals
local_paths:
- label: S21U-DECK MK.I Master Blueprint & BOM
  path: file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1
- label: Cost-Optimized BOM (CSV)
  path: file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1/BOM.csv
- label: Wiring & Power Diagram (SVG)
  path: file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1/assets/s21u-deck-wiring.svg
- label: Assembly & Cut Sheet (SVG)
  path: file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1/assets/s21u-deck-assembly.svg
- label: Enclosure Reference Photo (actual unit)
  path: file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1/assets/reference
- label: 3 Layout & I/O Configuration Illustrations
  path: file:///D:/Projects/Studio_Portfolio/assets/concepts/s21u-configs
run_commands: []
memory_ids:
- 5b0fe59d-fb6b-4927-956c-50d8cdcc9f13
- 1a8a41ee-457d-44ba-adcd-6330a1f702d3
- 57af16ac-7320-4e52-9130-4aa9759b5ac5
- 1df26189-c5f5-4934-8a89-f8a975f758e1
conversation_ids:
- 8b7beecf-a694-42b2-8f48-ee4a02784f98
---

## What It Is & Why It Matters

Replacing a cracked curved AMOLED assembly on an older flagship phone often costs more than the phone is worth, leaving a fast 8-core Snapdragon 888 / Adreno 660 computer (`12 GB` LPDDR5, UFS 3.1) sitting in a drawer. At the same time, US-variant Samsung phones (`SM-G998U`) enforce a hardware-locked Knox bootloader—blocking custom Linux kernels for Wi-Fi packet injection, USB HID gadget emulation (`/dev/hidg0`), or native SocketCAN automotive diagnostics.

We designed **S21U-DECK MK.I** inside a used 20 in Sears Craftsman steel mechanics toolbox (`$608.11` 100% buy-new retail from live listings, `$499.53` with parts-bin scavenging, or **`~$470` net** after selling the pulled 108 MP OEM camera module on eBay). Instead of fighting the locked bootloader, our bus topology offloads physical-layer RF, BIOS KVM keyboard/mouse injection, 120 MHz logic analysis, and OBD-II CAN bus traffic onto five dedicated co-processors (`$20.80` combined) over an internally powered USB 2.0 hub—leaving the Snapdragon 888 dedicated to Samsung DeX on a `10.1"` IPS touchscreen, Mesa Turnip Vulkan emulation, Winlator x86_64 PC games, and `Termux:X11` Debian Linux.

## Real Example: How It Works in Practice

- **Input**: Walk up to a headless rack server that refuses to boot into its OS (or sit down in the field to fly a 6-DOF space/mech sim) and unlatch the steel box lid.
- **What Happens**:
  1. Flipping the rear master toggle powers the `RTD2660` `10.1" 1280x800` IPS panel and `Mini560 5V 5A` peripheral rail while the `IP2368` 100W bidirectional board negotiates `25W–45W` USB-PD **PPS ("Pause USB Power Delivery")** direct rail bypass—powering the S21 Ultra motherboard without cooking or cycling its internal battery, cooled by a `100x60x10mm` finned aluminum coldplate and `5015` side-exhaust blower.
  2. **Headless Server KVM Mode**: Plugging a target machine into the flush `HDMI-IN` (`MS2109/MS2130` 1080p60 UVC capture) and `KVM-USB` ports streams the remote server's BIOS screen into a DeX window while typing on the deck streams keystrokes over a VBUS-isolated `921.6 kbps` UART bridge (`RP2040 #1` to `RP2040 #2`) acting as a hardware BIOS USB keyboard/mouse.
  3. **Hardware/RF Field Mode**: `ESP32-S3` (wired to a lid SMA whip antenna) handles 2.4 GHz Wi-Fi/BLE auditing, `RP2040 #3` (`sigrok-pico` + `TXS0108E` `1.8V–5V` level shifter) captures 24-channel digital logic off an 8-pin Phoenix terminal block, `CANable` reads vehicle CAN frames via a `GX12-4P` aviation plug, and a `7mm` UVC macro scope inspects SMD solder joints live.
  4. **Flight/Mech Sim Mode**: Unfolding the twin Hall-effect sticks out of `-36mm` side stowage wells engages a `1mm` PTFE friction clutch on the Left-Y axis for smooth non-centering throttle control alongside 6-DOF right-stick pitch/roll/aiming.
- **Output**: Four field instruments—Linux/DeX workstation, isolated BIOS KVM crash-cart, electronics/CAN/RF diagnostic bench, and HOSAS simpit—packed inside a single steel toolbox for `~$470` net after camera salvage.

## Where It Stands & Next Steps

This entry is a complete, fabrication-ready engineering blueprint (`300+ lines` of schematics, cut dimensions, pinouts, and pre-teardown software checklists in `s21u_cyberdeck_master_blueprint.md`). Every subsystem—including laser-cut `3mm` matte black cast acrylic plate coordinates (`488 x 208 mm` inside the `508 x 229 x 229 mm` steel tub; the Apache 2800/3800 cut charts remain as housing alternates), Z-height clearances, and two mandatory `+5V` VBUS isolation cuts—has been verified against off-the-shelf component specs.

Next steps when moving from blueprint to physical bench assembly:
- Run the 5-step **Pre-Teardown Software Lock-In** on the S21 Ultra over external HDMI *before* heating the back glass (`Auto Blocker -> OFF`, `Disable adb authorization timeout -> ON`, `DeX Auto-Start -> ON`, `Pause USB PD` check, and blind USB keyboard BFU PIN unlock test).
- Test-cut the `488 x 208 mm` deck faceplate in cardboard first to verify tub taper, hinge knock-over and lid clearance inside the steel toolbox before cutting `3mm` stock.
- Drill nothing until the front wall is mapped: the twin `100 x 50 mm` patch plates must clear the centre padlock hasp, the red badge and both draw latches, and every hole has to land on a flat band between the body ribs.
- 3D-print the left and right `-36mm` HOSAS stowage pockets in ABS/ASA and bond the perimeter `M3` cleats with methyl-methacrylate structural plastic adhesive.

## Under the Hood & Local Files

### Three Earlier Layout Studies (superseded by the steel box)
These predate Rev B and are kept as exploration history: we illustrated three distinct physical form factors and I/O patch-bay layouts around the same stripped Snapdragon 888 coldplate + USB-PD PPS core (all available in the visual gallery above):
- **Configuration A — Apache 2800 HOSAS Simpit & Retro Deck**: Clamshell IP65 hardcase with lid-mounted `10.1"` DeX display, fold-out dual Ginfull Hall-effect flight sticks in `-36 mm` side wells flanking a 40% ortholinear keyboard, and front `3.5 mm` TRRS + dual USB gamepad ports.
- **Configuration B — Server Crash-Cart & Hardware Diagnostic Lab Deck**: Swaps flight gimbals for a 60% tactile mechanical keyboard + optical thumb trackball and crowns the deck with a brushed anodized bulkhead patch bay (`HDMI-IN` UVC KVM, `RJ45` GbE, brass `SMA` 2.4 GHz whip, green 8-pin `sigrok` logic terminal block, `GX12` CAN socket, guarded rail kill-switches, and `INA226` OLED power monitor).
- **Configuration C — Slim Aluminum/Carbon `13.3"` Field Tablet-Deck**: Hardcase-free CNC aluminum and carbon-fiber kickstand slate (`13.3"` touchscreen + magnetic pogo keyboard) with a rear ventilated coldplate module (`100×60×10 mm` heatsink + `5015` blower) and side rail (`2× 100W` USB-C PD, microSD, `3.5 mm` DAC, and SMA SDR port).

Two electrical protection rules captured in our Memory Bank (`M0971`–`M0974`) prevent common DIY cyberdeck failures:
1. **Hub VBUS Backfeed Cut**: Cutting the `+5V` red conductor on the upstream USB 2.0 data cable feeding the internal 7-port peripheral hub—and powering that hub strictly from the `Mini560 5V 5A` buck converter—ensures high-draw peripherals never destabilize the USB-C hub's PD/PPS handshake with the Snapdragon 888.
2. **Galvanic/VBUS KVM Isolation**: Connecting `RP2040 #1` (Deck Supervisor + `INA226`/`SSD1306` OLED power monitor) to `RP2040 #2` (Target USB HID emulator) strictly via `TX/RX` (`330 Ω` current-limiting series resistors) + `GND` with `VBUS` severed ensures a faulty external server power supply can never back-feed `5V` into the cyberdeck's internal rails.

Local blueprint and reference files:
- **Master Engineering Blueprint, Mermaid Diagrams & 21-Line BOM**: [s21u_cyberdeck_master_blueprint.md](file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1/s21u_cyberdeck_master_blueprint.md)
- **Cost-Optimized BOM (CSV)**: [BOM.csv](file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1/BOM.csv) — 27 priced lines, `$608.11` retail / `$499.53` scavenged, every line linked to a live vendor listing
- **Build Log**: [BUILD_LOG.md](file:///C:/Users/ogreb/.config/freebuff-desktop/local-projects/40c5eaf3-fb9d-4d2c-9e87-3e6c65b6cecc/s21u-cyberdeck-mk1/BUILD_LOG.md)
- **Assembly & Cut Sheet (published copy)**: [s21u-deck-assembly.svg](file:///D:/Projects/Studio_Portfolio/assets/diagrams/s21u-deck-assembly.svg) — true-scale 1.2 px/mm side section, 1.15 px/mm deck view, cut list and build sequence
