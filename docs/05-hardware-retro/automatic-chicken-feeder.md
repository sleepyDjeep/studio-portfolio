---
id: "automatic-chicken-feeder"
title: "30-Hen Automatic Feeder: ESP32 Auger with Hot-Swap 18650s"
subtitle: "Post-mounted feeder that holds a week of feed for 30 laying hens, dispenses four weighed 900 g portions a day from a 50 L hopper, and runs on two 18650s you can swap one at a time against a third on a bench charger."
pillar: "05-hardware-retro"
entry_type: "project"
readiness: "blueprint"
visibility: "main"
date_started: "2026-11-18"
date_updated: "2026-11-19"
tags:
  - "poultry"
  - "auger-feeder"
  - "esp32-c3"
  - "18650"
  - "hot-swap"
  - "load-cell"
  - "off-grid"
metrics:
  - label: "Flock Served"
    value: "30 Hens"
  - label: "Daily Ration"
    value: "3.6 kg / Day"
  - label: "Hopper"
    value: "50 L / 32 kg"
  - label: "Portions"
    value: "4 x 900 g"
  - label: "Battery Endurance"
    value: "~16 Days at 20 C"
  - label: "Indicative BOM"
    value: "~EUR 220"
media: []
diagram: "assets/diagrams/automatic-chicken-feeder.svg"
tech_stack:
  - "ESP32-C3 (Arduino / PlatformIO)"
  - "LM66200 dual ideal-diode OR"
  - "TPS63802 3.3 V buck-boost"
  - "TPS61088 12 V boost + DRV8871"
  - "HX711 + four 50 kg load cells"
  - "INA219 current sense"
local_paths:
  - label: "Portfolio Diagram"
    path: "file:///D:/Projects/Studio_Portfolio/assets/diagrams/automatic-chicken-feeder.svg"
run_commands:
  - label: "Build and Upload Firmware (design workspace)"
    command: "cd firmware && pio run -t upload"
  - label: "Serial Calibration Monitor"
    command: "cd firmware && pio device monitor"
memory_ids: []
conversation_ids: []
---

## What It Is & Why It Matters

This is a single post-mounted feeder sized from one number: **30 hens x 120 g/day = 3.6 kg of feed per day**, or 25.2 kg a week. A 50 L sealed hopper holds about 32 kg, so one 25 kg sack refills it with a week's margin. Feed moves through a 25 mm coil-spring auger running 30 degrees uphill into a 1.4 m ring trough with 3.77 m of eating edge - 12.6 cm per hen, just over the 12 cm welfare figure.

The power arrangement is the part worth copying. Two protected 18650s sit in the feeder behind a dual ideal-diode OR, and a third waits on a bench charger indoors. You can pull either cell at any moment; the other carries the load without a reset, and the fresh cell cannot back-charge the weaker one. A weekly visit is one sack of feed, one cell swap and a trough scrub. The refill interval is set by the hopper, not the battery: the pack lasts about 16 days at 20 C, comfortably more than the seven days of feed.

Portions are closed-loop on **mass**, not time. The hopper rests on four 50 kg load cells through an HX711, so the firmware runs the auger until 900 g has actually left the hopper. The same scale detects an empty hopper (mass stops falling), and an INA219 backs it up with motor current for a jam (current rising, no mass leaving). A timer-based feeder cannot tell the difference between a full trough and a blocked tube; this one can.

The design is deliberately low-tech where it can be. The auger is a pellet-stove spring inside 32 mm PVC split into two halves for clearing. The worm gear self-locks and the tube stays packed when power drops, so nothing free-flows onto the ground. No feed is dispensed at night, which keeps the trough empty when rodents are active.

This is a **blueprint**: the design document and firmware exist and the firmware compiles for the ESP32-C3, but no feeder has been built and no motor, load cell or cell has been attached to it.

## Real Example: How It Works in Practice

- **Input**: A Wednesday morning visit with one 25 kg sack. The hopper reads 28.4 kg, the fitted cell reads 3.78 V, the spare 4.19 V.
- **What Happens**:
  1. Pour the sack into the 50 L hopper through the lid at 1.30 m. The firmware wakes at sunrise + 30 min and computes the first 900 g portion from the load-cell mass.
  2. It enables the 12 V boost, soft-starts the DRV8871, and runs the auger at about 240 g/min. The spring lifts feed 30 degrees uphill and drops it onto the centre cone, where four radial vanes spread a 4 mm ribbon around the ring.
  3. The scale reaches a 900 g delta in roughly four minutes and the firmware stops the motor, then sleeps until sunrise + 3 h 30.
  4. If the current climbs past 1.2 A while mass is static, the feeder stops, reverse-jogs for one second, retries up to three times, then reports a jam instead of pretending it fed the flock.
  5. Pull the fitted cell: the LM66200 switches to the second cell in microseconds. Put the pulled cell on the charger and the charged spare into the empty slot. Nothing reboots; the schedule survives in RTC memory.
- **Output**: Four weighed meals, a consumption log, an empty-hopper warning days before it matters, and a feeder that keeps running through a cell swap or a power cut.

## Where It Stands & Next Steps

The design package is complete: a README with requirements, feed and power calculations, electrical architecture, mechanical dimensions, commissioning steps, weekly routine and failure-mode table; a PlatformIO project for the ESP32-C3 with the full feeder firmware; a power-tree diagram; and an indicative BOM at about **EUR 220**.

The firmware compiles clean for `esp32-c3-devkitm-1` and links to a 376 KB binary. Two review fixes landed before the thread closed: the calibrated auger rate now actually drives the dispense safety timeout, and a stale empty branch in the mass read was removed. The code has never run on hardware.

Not done yet:
- No build: the frame, hopper, auger and trough are dimensioned concepts, not a tested machine.
- No measured auger throughput, motor current or energy; the 200-320 g/min and ~370 mAh/day figures are calculated, with roughly 30% spread depending on feed.
- No proper schematic with component values and reference designators - the thread's net list names connections but is not yet a buildable drawing.
- The reduced-complexity option (timed auger runs, no load cells) was requested but not written.
- The SVG was checked geometrically but never rendered.

The two numbers to record first on a real build are the auger's grams per second and the motor's running current; everything else is calibrated from those.

## Under the Hood & Local Files

### Feed Path

- **Hopper**: 50 L sealed HDPE/PP bin, 480 x 480 mm footprint, 350 mm straight side plus a 200 mm cone, hinged gasketed lid at 1.30 m. The cone is 55-60 degrees with a 70 mm outlet and a 60 mm agitator paddle on the auger shaft to break arches.
- **Auger**: 25 mm OD coil-spring pellet auger, 900 mm long, inside 32 mm grey PVC split into two halves. It runs 30 degrees uphill from the 0.95 m outlet to a 1.35 m drop head.
- **Drive**: 12 V worm gearmotor at about 80 rpm loaded, rated 0.5 Nm against an estimated 0.15 Nm demand; 8 mm flexible jaw coupling. The coupling and a separate hopper sub-frame keep motor vibration out of the load cells.
- **Trough**: 1.4 m outer ring, 150 mm wide, 80 mm deep, floor at 300 mm; 3.77 m of edge. A 350 mm centre cone with four vanes spreads each portion; a 1.6 m polycarbonate hood sits 400 mm above the lip with a 100 mm feeding slot. Six 10 mm drain holes; the ring lifts off in two halves.

### Power and Hot Swap

Plain parallel holders are unsafe: a 4.20 V cell beside a 3.70 V one drives a cross-charge limited only by cell and wiring resistance, tens of amps inside a plastic box. Instead each slot feeds a **TI LM66200** dual ideal-diode OR (or two LM66100s), which selects the higher cell and blocks reverse current. Each slot has a 2 A PTC; the load has a 5 A fuse. Cells are protected 3500 mAh NCR18650GA/35E-class, same model and age, charged only on a bench charger - never inside the feeder.

- **3.3 V rail**: TPS63802 buck-boost, so the ESP32 stays regulated down to 2.5 V input.
- **12 V rail**: TPS61088-based boost with an enable pin, switched off between meals; left on, an MT3608-class module idles at milliamps and flattens the pack in weeks.
- **Motor stage**: DRV8871 with a current limit set near 3 A, roughly three times the ~1 A running current, so cold feed does not trip it but a real jam does.
- **Sensing**: four 50 kg half-bridge load cells under the hopper platform (200 kg range, 60 kg full) into an HX711 at 80 Hz; INA219 on the motor supply; gated 1 M/1 M dividers on each cell so battery sensing does not leak.

Budget is about **370 mAh/day at 3.7 V**, with the motor at roughly 99% of it, because the auger only runs about 15 minutes a day. Two 3500 mAh cells give about 16 days at 20 C; cold weather and stiff feed are why the design keeps a week of margin rather than relying on the pack.

### Firmware and Schedule

`firmware/` is PlatformIO with the Arduino framework. The ESP32-C3 deep-sleeps on the RTC timer, wakes for four meals tied to sunrise and sunset (sunrise + 30 min, sunrise + 3 h 30, sunset - 4 h, sunset - 2 h), computes sun times on-device from latitude and longitude, and caps sleep at four hours so clock drift cannot run away. Twice a day it joins WiFi, syncs NTP and posts a small JSON status. A meal is skipped if the RTC meal mask already records it for the day, so a reset cannot double-feed.

`dispenseGrams()` enables the boost, soft-starts the motor, then loops on the HX711 mass until the target delta is reached. Its timeout is derived from the calibrated grams-per-second rate (2.5x expected run + 20 s), but mass is always the master: a wrong rate can only end a portion early, never overfeed. Jams are disambiguated by current and flow - current above 1.2 A after a 2.5 s grace, or no mass change for 9 s.

Serial calibration at 115200 baud: `t` tare, `c` calibrate with 5.000 kg, `f` feed one portion now, `r` run 30 s and store grams/second, `i` print voltages, mass, last result and schedule.

### BOM and Open Items

Indicative EUR pricing: ESP32-C3 board 4, LM66200 3, TPS63802 4, 12 V boost 5, DRV8871 5, gearmotor 14, auger and tube 12, coupling 5, load cells 10, HX711 2, INA219 2, three protected 18650s 18, holders 2, charger 20, PTCs 1, hopper 25, trough and hood 30, post and frame 35, IP65 enclosure 12, misc 11 - about **EUR 220**, plus one 25 kg sack a week.

Failure modes are covered explicitly: auger jam (current limit, reverse-jog, alarm), hopper bridge (wide cone, paddle), cell pulled or flat (ideal-diode OR), total power loss (worm gear self-locks, tube stays packed), rain (hood and drains), rodents (no night feed, glands, clear post), and both cells flat (low-voltage alarm weeks ahead). The honest gap is that all of it is desk engineering until the first build records real auger rate and motor current.

- [automatic-chicken-feeder.svg](file:///D:/Projects/Studio_Portfolio/assets/diagrams/automatic-chicken-feeder.svg) - feed path, power tree and weekly cell rotation.
