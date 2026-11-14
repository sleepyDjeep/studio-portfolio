---
id: "koala-gabber-phonk-pipeline"
title: "Koala Sampler DSP Synthesizer & Project Packager"
subtitle: "Synthesizes 13 royalty-free 24-bit/48kHz Gabber-Phonk stems from pure Python math and compiles a ready-to-play 172 BPM desktop Koala Sampler project."
pillar: "04-creative-3d-media"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-11-02"
date_updated: "2026-11-02"
tags:
  - "audio-dsp"
  - "python-synthesis"
  - "koala-sampler"
  - "gabber-phonk"
  - "procedural-audio"
metrics:
  - label: "Synthesized Stems"
    value: "13 WAVs (24-bit/48kHz)"
  - label: "DSP Engine"
    value: "832 LOC Pure Python"
  - label: "Sequencer Resolution"
    value: "4,096 Ticks / Beat"
  - label: "External Samples"
    value: "0 (100% Procedural)"
media:
  - src: "assets/concepts/koala-gabber-phonk-pipeline.png"
    kind: "concept"
    caption: "Concept Preview: 172 BPM pure-Python DSP waveform synthesizer and 64-pad .koala project packager."
  - src: "assets/media/koala-gabber-phonk-pipeline/01_909_Gabba_Kick_F1.wav"
    kind: "audio"
    caption: "Synthesized Stem 01 — Overdriven 172 BPM Rotterdam 909 Gabba Kick (F1, 24-bit/48kHz)"
  - src: "assets/media/koala-gabber-phonk-pipeline/12_Giallo_Ostinato_2Bar_172_Fm.wav"
    kind: "audio"
    caption: "Synthesized Stem 12 — 2-Bar 172 BPM F-Minor Giallo Harpsichord Ostinato"
diagram: ""
tech_stack:
  - "Python 3"
  - "NumPy"
  - "SciPy (scipy.signal)"
  - "Koala Sampler v1.0.4134"
  - "24-bit RIFF PCM"
local_paths:
  - label: "Koala_Gabber_Phonk_170"
    path: "file:///D:/Koala_Gabber_Phonk_170"
  - label: "Gabber_Phonk_170_Starter.koala"
    path: "file:///D:/Koala_Gabber_Phonk_170/Gabber_Phonk_170_Starter.koala"
run_commands:
  - label: "Synthesize Stems & Build .koala Project"
    command: "python \"D:\\Koala_Gabber_Phonk_170\\build_gabber_phonk_kit.py\""
  - label: "Launch Desktop Koala Sampler"
    command: "\"C:\\Program Files\\Koala 1.0.4134\\bin\\Koala.exe\""
memory_ids:
  - "38fa456e-b4d2-4b62-926c-a7fc4d872b24"
  - "3d172b1c-a9c2-4559-84e5-e4f07db5d53c"
  - "7c6dc737-0d59-49f4-b124-abb845238c7d"
  - "370a22b5-8245-47b2-b21c-7a56969cafa7"
conversation_ids: []
---

## What It Is & Why It Matters

Building fast, high-energy soundtrack kits for arcade action games or live beatmaking usually means digging through commercial splice packs—dragging sample-clearance headaches along with mismatched keys, inconsistent loudness, and manual pad mapping inside a sampler. Elf Audio's desktop Koala Sampler (`v1.0.4134`) is a tactile 64-pad performance instrument, yet populating its pads, mixer buses, FX racks, and multi-bar sequences by hand takes an hour per kit.

We reverse-engineered Koala Sampler's undocumented project directory and `.koala` archive format, then wrote an 832-line pure-math Python DSP synthesizer (`build_gabber_phonk_kit.py`) that generates an entire 172 BPM Rotterdam Gabber + Memphis Drift Phonk starter song from scratch. Zero external audio recordings are touched. Every kick transient, metallic cowbell, detuned Hoover lead, and Italian horror harpsichord loop is calculated straight from trigonometric oscillators, biquad IIR filters, and nonlinear waveshapers.

In under five seconds, a single script call renders 13 studio-grade 24-bit / 48 kHz stereo stems, wires four named mixer buses, programs four live patterns, installs the song directly into Koala's local library, and packs a portable `.koala` bundle ready for desktop or mobile import.

## Real Example: How It Works in Practice

- **Input**: Musical target parameters defined at the top of `build_gabber_phonk_kit.py`—`BPM = 172.0`, root key `F minor / F Phrygian` (`F1 = 43.65 Hz`), `SR = 48000` Hz—with zero audio files on disk.
- **What Happens**:
  1. Running `python build_gabber_phonk_kit.py` executes 13 dedicated NumPy/SciPy synthesis functions. For Stem 01 (`01_909_Gabba_Kick_F1.wav`), the script integrates a two-stage exponential pitch sweep (`+260 Hz` snap + `+72 Hz` punch settling onto `43.65 Hz`), layers a `2.4 kHz` bandpass transient click, carves `290 Hz` boxiness via a custom biquad peaking EQ, and slams the signal through asymmetrical waveshaper distortion.
  2. Additional synthesis engines build an industrial Tok punch kick, an `808` sub bass, a tempo-locked 1-beat reverse Gabber suck (`60 / 172 = 0.3488s`), a `DR-660` Memphis snare, `909` hats and warehouse ride, a dual-square `540 Hz / 800 Hz` `808` drift cowbell tuned to `F5`, a PWM-modulated Rotterdam Hoover Mentasm (`F2`), a Belgian New Beat minor chord stab, a 2-bar `F`-minor Giallo harpsichord ostinato, and a formant-filtered Memphis tape vocal chop.
  3. `write_wav_24bit_stereo` packs all 13 float64 stereo arrays into custom 3-byte little-endian `24-bit / 48 kHz` RIFF WAV files inside `D:\Koala_Gabber_Phonk_170\samples\`.
  4. The packager numbers pad stems `1.wav` through `13.wav`, writes pad color/choke/bus metadata into `sampler/sampler.json`, maps 4 named buses (`KICK + SUB`, `DRUMS + PERC`, `COWBL + RAVE`, `DEEP CHOPS`) in `mixer.json`, writes 4 multi-bar patterns at `4,096` ticks per beat into `sequence.json`, installs the live folder into `AppData\Local\Documents\Koala\songs\`, and zips `Gabber_Phonk_170_Starter.koala`.
- **Output**: `13` standalone 24-bit WAV stems (`3.80 MB`), an installed desktop Koala project pre-focused on the Sequence tab (`Sequence 2` full Gabber-Phonk drop armed so pressing `Space` plays immediately, with Pad 9 `808 COWBL` ready for chromatic keyboard riffs), and `Gabber_Phonk_170_Starter.koala` (`1.51 MB`).

## Where It Stands & Next Steps

The synthesizer and `.koala` project compiler are shipped and verified end-to-end on Windows (`15` files, `5.34 MB` in `D:\Koala_Gabber_Phonk_170`). Every synthesized WAV header, 4,096-tick sequencer event, choke group (Pads 6 & 7 hi-hat mute), mixer bus insert, and Samurai time-stretch flag loads cleanly inside desktop Koala Sampler `v1.0.4134` with zero clipping or schema warnings.

Next steps to expand this procedural audio engine across our game and music projects:
- **Multi-Genre Kit Generators**: Add parameterized preset modules (`160 BPM Jungle / Amen Break Slicer`, `128 BPM Electro-Industrial`, and `92 BPM Boom-Bap`) sharing the same `.koala` JSON serializer.
- **Direct Godot 4.7 Interactive Stem Exporter**: Emit a companion `.tres` loop-layer manifest alongside `.koala` archives so Godot combat encounters can crossfade `KICK + SUB`, `DRUMS + PERC`, and `COWBL + RAVE` stems dynamically based on player combo meter state.
- **CLI Seed & Key Randomizer**: Expose `--bpm`, `--root-midi`, and `--seed` flags so a single command generates endless key-matched starter kits on demand.

## Under the Hood & Local Files

### Architectural Decisions & Engineering Fixes
- **Reverse-Engineered `.koala` Schema & Sequencer Tick Math (`M0990`–`M0991`)**: Inspecting Elf Audio's desktop saves (`AppData\Local\Documents\Koala\songs\`) revealed that `.koala` files are standard ZIP archives housing root-level `song.json`, `sequence.json`, `mixer.json`, `fx.json`, and `sampler/sampler.json` + `<pad_index>.wav` (`0..63`). Sequencer events run at an exact PPQN of **`4,096` ticks per quarter-note beat** (`1,024` ticks per 16th note; `16,384` ticks per 4/4 bar) using `{timeOffset, num, subPad, pitch, length, vel, start, chance}` note dictionaries.
- **Custom 24-Bit Little-Endian PCM Packer (`M0992`)**: Python's standard-library `wave` module and `scipy.io.wavfile` frequently struggle with packed 3-byte (`int24`) stereo output without external C codecs. Writing `write_wav_24bit_stereo()` in pure NumPy—quantizing `[-1.0, 1.0]` floats to signed 32-bit integers and slicing the lower three little-endian bytes (`[:, :3]`) into a compliant RIFF `fmt ` + `data` stream—kept the generator 100% dependency-light.
- **Instant-Play Boot UX (`M0993`)**: Setting `"section": 1` in `song.json`, `"currSequenceId": 1` in `sequence.json`, and `"keyboardMode": true` / `"currSample": 8` in `sampler.json` boots Koala directly onto the armed main drop with chromatic `808` cowbell keys active under the user's fingers.

### Key Local Files
- Pure-Python DSP Synthesizer & Packager (`832` LOC): [build_gabber_phonk_kit.py](file:///D:/Koala_Gabber_Phonk_170/build_gabber_phonk_kit.py)
- Portable Koala Sampler Archive (`1.51 MB`): [Gabber_Phonk_170_Starter.koala](file:///D:/Koala_Gabber_Phonk_170/Gabber_Phonk_170_Starter.koala)
- Highlighted 24-Bit / 48 kHz Synthesized Stems: [01_909_Gabba_Kick_F1.wav](file:///D:/Koala_Gabber_Phonk_170/samples/01_909_Gabba_Kick_F1.wav) | [09_808_Drift_Cowbell_F5.wav](file:///D:/Koala_Gabber_Phonk_170/samples/09_808_Drift_Cowbell_F5.wav) | [10_Rotterdam_Hoover_Mentasm_F2.wav](file:///D:/Koala_Gabber_Phonk_170/samples/10_Rotterdam_Hoover_Mentasm_F2.wav) | [12_Giallo_Ostinato_2Bar_172_Fm.wav](file:///D:/Koala_Gabber_Phonk_170/samples/12_Giallo_Ostinato_2Bar_172_Fm.wav)
- Live Installed Koala Song Directory: [Gabber_Phonk_170_Starter](file:///C:/Users/ogreb/AppData/Local/Documents/Koala/songs/Gabber_Phonk_170_Starter)
