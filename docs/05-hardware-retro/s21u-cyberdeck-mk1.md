---
id: s21u-cyberdeck-mk1
title: 'S21U-DECK MK.I: Sub-$200 Snapdragon 888 Field Cyberdeck & KVM Crash-Cart'
subtitle: Complete electrical, thermal, and mechanical blueprint repurposing a broken-screen Galaxy S21 Ultra inside
  an Apache 2800 hardcase with Hall HOSAS sticks and 4 USB co-MCUs.
pillar: 05-hardware-retro
entry_type: idea
readiness: blueprint
visibility: main
date_started: '2026-10-27'
date_updated: '2026-11-13'
tags:
- cyberdeck
- hardware-engineering
- samsung-dex
- rp2040
- esp32-s3
- hosas
metrics:
- label: All-New Retail BOM
  value: $195.75 (<$200 Cap)
- label: Net Scavenged Cost
  value: ~$118 (After Salvage)
- label: Battery Capacity
  value: 70.3 Wh + PPS Bypass
- label: Hardware Co-MCUs
  value: 4 (ESP32-S3 + 3x RP2040)
media:
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
  path: file:///C:/Users/ogreb/.gemini/antigravity/brain/8b7beecf-a694-42b2-8f48-ee4a02784f98/s21u_cyberdeck_master_blueprint.md
- label: Enclosure Reference Photos (C121)
  path: file:///C:/Users/ogreb/.gemini/antigravity/brain/8b7beecf-a694-42b2-8f48-ee4a02784f98/scratch
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

We designed **S21U-DECK MK.I** inside a weatherproof Harbor Freight Apache 2800 hardcase (`$195.75` 100% buy-new retail, `$148.19` with parts-bin scavenging, or **`~$118` net** after selling the pulled 108 MP OEM camera module on eBay). Instead of fighting the locked bootloader, our bus topology offloads physical-layer RF, BIOS KVM keyboard/mouse injection, 120 MHz logic analysis, and OBD-II CAN bus traffic onto four dedicated microcontrollers (`$16.70` combined) over an internally powered USB 2.0 hub—leaving the Snapdragon 888 dedicated to Samsung DeX on a `10.1"` IPS touchscreen, Mesa Turnip Vulkan emulation, Winlator x86_64 PC games, and `Termux:X11` Debian Linux.

## Real Example: How It Works in Practice

- **Input**: Walk up to a headless rack server that refuses to boot into its OS (or sit down in the field to fly a 6-DOF space/mech sim) and unlatch the Apache 2800 lid.
- **What Happens**:
  1. Flipping the rear master toggle powers the `RTD2660` `10.1" 1280x800` IPS panel and `Mini560 5V 5A` peripheral rail while the `IP2368` 100W bidirectional board negotiates `25W–45W` USB-PD **PPS ("Pause USB Power Delivery")** direct rail bypass—powering the S21 Ultra motherboard without cooking or cycling its internal battery, cooled by a `100x60x10mm` finned aluminum coldplate and `5015` side-exhaust blower.
  2. **Headless Server KVM Mode**: Plugging a target machine into the flush `HDMI-IN` (`MS2109/MS2130` 1080p60 UVC capture) and `KVM-USB` ports streams the remote server's BIOS screen into a DeX window while typing on the deck streams keystrokes over a VBUS-isolated `921.6 kbps` UART bridge (`RP2040 #1` to `RP2040 #2`) acting as a hardware BIOS USB keyboard/mouse.
  3. **Hardware/RF Field Mode**: `ESP32-S3` (wired to a lid SMA whip antenna) handles 2.4 GHz Wi-Fi/BLE auditing, `RP2040 #3` (`sigrok-pico` + `TXS0108E` `1.8V–5V` level shifter) captures 24-channel digital logic off an 8-pin Phoenix terminal block, `CANable` reads vehicle CAN frames via a `GX12-4P` aviation plug, and a `7mm` UVC macro scope inspects SMD solder joints live.
  4. **Flight/Mech Sim Mode**: Unfolding the twin Hall-effect sticks out of `-36mm` side stowage wells engages a `1mm` PTFE friction clutch on the Left-Y axis for smooth non-centering throttle control alongside 6-DOF right-stick pitch/roll/aiming.
- **Output**: Four field instruments—Linux/DeX workstation, isolated BIOS KVM crash-cart, electronics/CAN/RF diagnostic bench, and HOSAS simpit—packed inside a single IP65 hardcase under `$200`.

## Where It Stands & Next Steps

This entry is a complete, fabrication-ready engineering blueprint (`306 lines` of schematics, cut dimensions, pinouts, and pre-teardown software checklists in `s21u_cyberdeck_master_blueprint.md`). Every subsystem—including laser-cut `3mm` matte black cast acrylic plate coordinates (`298 x 224 mm`, `R10` corners for Apache 2800; `374 x 266 mm` for Apache 3800), Z-height clearances, and two mandatory `+5V` VBUS isolation cuts—has been verified against off-the-shelf component specs.

Next steps when moving from blueprint to physical bench assembly:
- Run the 5-step **Pre-Teardown Software Lock-In** on the S21 Ultra over external HDMI *before* heating the back glass (`Auto Blocker -> OFF`, `Disable adb authorization timeout -> ON`, `DeX Auto-Start -> ON`, `Pause USB PD` check, and blind USB keyboard BFU PIN unlock test).
- Test-cut the `298 x 224 mm` deck faceplate in cardboard first to verify the `~1.5°` molded draft angle inside the Apache 2800 tub before cutting `3mm` cast acrylic.
- 3D-print the left and right `-36mm` HOSAS stowage pockets in ABS/ASA and bond the perimeter `M3` cleats with methyl-methacrylate structural plastic adhesive.

## Under the Hood & Local Files

### Three Modular Layout & I/O Configurations
We illustrated three distinct physical form factors and I/O patch-bay layouts around the same stripped Snapdragon 888 coldplate + USB-PD PPS core (all available in the visual gallery above):
- **Configuration A — Apache 2800 HOSAS Simpit & Retro Deck**: Clamshell IP65 hardcase with lid-mounted `10.1"` DeX display, fold-out dual Ginfull Hall-effect flight sticks in `-36 mm` side wells flanking a 40% ortholinear keyboard, and front `3.5 mm` TRRS + dual USB gamepad ports.
- **Configuration B — Server Crash-Cart & Hardware Diagnostic Lab Deck**: Swaps flight gimbals for a 60% tactile mechanical keyboard + optical thumb trackball and crowns the deck with a brushed anodized bulkhead patch bay (`HDMI-IN` UVC KVM, `RJ45` GbE, brass `SMA` 2.4 GHz whip, green 8-pin `sigrok` logic terminal block, `GX12` CAN socket, guarded rail kill-switches, and `INA226` OLED power monitor).
- **Configuration C — Slim Aluminum/Carbon `13.3"` Field Tablet-Deck**: Hardcase-free CNC aluminum and carbon-fiber kickstand slate (`13.3"` touchscreen + magnetic pogo keyboard) with a rear ventilated coldplate module (`100×60×10 mm` heatsink + `5015` blower) and side rail (`2× 100W` USB-C PD, microSD, `3.5 mm` DAC, and SMA SDR port).

Two electrical protection rules captured in our Memory Bank (`M0971`–`M0974`) prevent common DIY cyberdeck failures:
1. **Hub VBUS Backfeed Cut**: Cutting the `+5V` red conductor on the upstream USB 2.0 data cable feeding the internal 7-port peripheral hub—and powering that hub strictly from the `Mini560 5V 5A` buck converter—ensures high-draw peripherals never destabilize the USB-C hub's PD/PPS handshake with the Snapdragon 888.
2. **Galvanic/VBUS KVM Isolation**: Connecting `RP2040 #1` (Deck Supervisor + `INA226`/`SSD1306` OLED power monitor) to `RP2040 #2` (Target USB HID emulator) strictly via `TX/RX` (`330 Ω` current-limiting series resistors) + `GND` with `VBUS` severed ensures a faulty external server power supply can never back-feed `5V` into the cyberdeck's internal rails.

Local blueprint and reference files:
- **Master Engineering Blueprint, Mermaids & 20-Line BOM**: [s21u_cyberdeck_master_blueprint.md](file:///C:/Users/ogreb/.gemini/antigravity/brain/8b7beecf-a694-42b2-8f48-ee4a02784f98/s21u_cyberdeck_master_blueprint.md)
- **Hardcase Reference Geometry**: [scratch](file:///C:/Users/ogreb/.gemini/antigravity/brain/8b7beecf-a694-42b2-8f48-ee4a02784f98/scratch)
