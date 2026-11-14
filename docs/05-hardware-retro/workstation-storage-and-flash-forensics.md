---
id: "workstation-storage-and-flash-forensics"
title: "Workstation Storage Hygiene, Kernel Audit & NAND Flash Forensics"
subtitle: "Reclaimed 356.32 GB across workstation drives, eliminated a 7.3M Windows kernel handle leak, and built byte-offset binary probes exposing counterfeit NAND flash."
pillar: "05-hardware-retro"
entry_type: "workflow"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-29"
date_updated: "2026-11-04"
tags:
  - "storage-forensics"
  - "nand-flash"
  - "windows-internals"
  - "kernel-handles"
  - "ntfs-junctions"
  - "system-hygiene"
metrics:
  - label: "Storage Reclaimed"
    value: "+356.32 GB Total"
  - label: "Kernel Leak Fixed"
    value: "7.3M Leaked Handles"
  - label: "Apps Audited"
    value: "227 via UserAssist"
  - label: "Fake NAND Caught"
    value: "44.38 GiB Cliff Found"
media: []
diagram: "assets/diagrams/workstation-storage-and-flash-forensics.svg"
tech_stack:
  - "Python 3.13 (Raw Binary Offset Probing)"
  - "PowerShell & Batch Automation"
  - "Windows UserAssist Registry Telemetry"
  - "Voidtools Everything CLI (es.exe)"
  - "NTFS Reparse Points & Robocopy"
local_paths:
  - label: "Workstation Cleanup & Audit Scripts"
    path: "file:///D:/Tools/Scripts"
  - label: "227-App Bloatware Audit Report (C099)"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/cc5f5f1c-7677-4661-a99f-e0d5a2157fa6/software_inventory_and_bloatware_audit.md"
  - label: "Byte-Offset Flash Forensics Session (C128)"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/brain/3e98c00e-6665-4cdf-8a63-f82aef4577c0"
run_commands:
  - label: "Inspect Workstation Maintenance Scripts"
    command: "explorer \"D:\\Tools\\Scripts\""
memory_ids:
  - "e86bd1ca-aec7-4d57-b262-635835e4abf7"
  - "ebd8193a-0649-4754-b331-d66aab614346"
  - "86b7d19f-df3c-4aa3-9072-30bf7406653c"
  - "770189c9-63bd-4409-8e5e-4496af365ef3"
  - "85c91870-198a-4e07-85c6-2d723c1deba8"
conversation_ids:
  - "580b7f35-626a-4346-b383-90f9973a31b1"
  - "cc5f5f1c-7677-4661-a99f-e0d5a2157fa6"
  - "aba381c1-e328-45e7-bdef-1ab2d9435184"
---

## What It Is & Why It Matters

Running local LLMs, ComfyUI diffusion pipelines, Blender 5.1, Godot 4.7, and multi-hundred-gigabyte game archives on one laptop exposes every weak link in Windows storage and memory management. Over three forensic sprints between August and November 2026, our studio workstation hit three deceptive hardware and OS traps: a mysterious multi-gigabyte non-paged pool slowdown, a `C:\` OS drive suffocating at `7.0 GB` free, and silent binary corruption (`emulationstation.exe` zeroing out) on an external `"512 GB"` USB SSD.

We built a repeatable systems-forensics toolkit (`D:\Tools\Scripts\` plus raw Python disk probes) that diagnosed and fixed all three root causes with mathematical certainty. That work reclaimed **356.32 GB** of fast NVMe space (`+118.43 GB` on `C:\` and `+237.89 GB` on `D:\`), eliminated a **7.3-million kernel handle leak**, and caught two separate counterfeit flash drives red-handed before permanent project loss could occur.

## Real Example: How It Works in Practice

- **Input**: An external USB storage drive (`Generic STORAGE DEVICE`, labeled `512 GB`) begins corrupting newly copied executables even though Windows Explorer and `chkdsk` report over `400 GB` of healthy free capacity.
- **What Happens**:
  1. First, when cloning `E:\` to `F:\` (`C127`), we caught why drive usage suddenly ballooned by `+30 GB`: formatting a target volume as `exFAT` destroys NTFS directory junctions unless `Robocopy /SJ /SL` is used on an NTFS target, causing linked folders to expand into physical duplicate bytes.
  2. Next (`C128`), when binaries still corrupted past the ~48 GB mark, we wrote a deterministic Python byte-offset forensic probe that bypassed filesystem caches, stamped unique cryptographic block markers at progressive LBA byte offsets, flushed hardware buffers, and read the raw sectors back.
  3. Up to **`44.38 GiB` (`47.65 GB`)**, every sector returned valid data; at the exact byte boundary past `44.38 GiB`, the USB bridge controller silently discarded writes and returned all-zero `0x00` pages—proving firmware capacity spoofing on a cheap 48 GB NAND die. We ran the same partition/offset audit (`C118`) on a suspect `"2 TB"` USB 3.0 microSDXC card (`Disk 3`), exposing hidden Linux SBC GPT partitions and spoofed LBA reporting.
- **Output**: Immediate quarantine of both counterfeit flash drives, zero lost studio source code, and a clean migration onto verified physical storage using zero-byte NTFS junctions.

## Where It Stands & Next Steps

All workstation hygiene rules and scripts are shipped and active on disk:
- **7.3M Handle Leak Eliminated (`C072`)**: Traced `AcerSystemCentralService` (`3.3M` handles), `AcerCentralService` (`3.1M` handles), and MediaTek `mtkbtsvc` (`900K` handles) accumulating across fake "shutdowns" because Windows Fast Startup hibernates the kernel session instead of cold-resetting it.
- **227-App `UserAssist` Telemetry Audit (`C099`)**: Decoded ROT13 Windows `UserAssist` registry execution counters across 6 months of real usage, purging OEM adware (`SweetLabs App Explorer`, `Planet9 Stub`, `Acer Jumpstart`) and deprecated `Summer Engine` (`3.55 GB`) while keeping essential `NitroSense` fan curves intact.
- **Strict Drive Tiering (`M0428`, `M0763`–`M0766`)**: Enforced an OS-only `C:\` rule, consolidated active Godot/AI builds (`KaijuConvenience`, `MechDestroyer`, `Babylon`, `PocketRPG Studio`, `PropertyIntel`, `TechWriter`, `Aether Engine`, `LocalAssistant`) onto `D:\Projects` (`732 GB` free on `1.8 TB` NVMe), and extracted shared code into `D:\Projects\_Shared_Library`.

Next steps for workstation ops:
- Wrap the Python LBA cliff-detector script into a standalone 1-click CLI utility (`verify_flash_media.py`) inside `D:\Tools\Scripts\` so every newly purchased SD card or USB drive gets tested before formatting.
- Schedule a monthly headless task checking process handle counts above `50,000` to catch third-party driver regressions automatically.

## Under the Hood & Local Files

Standard disk speed utilities like CrystalDiskMark (`bench_ef.py`) only write a `1 GiB` test file near the beginning of a partition—which sits comfortably inside the real 32–48 GB NAND chip soldered onto counterfeit drives, letting fake drives pass benchmark tests at full speed. Only strided LBA marker verification across the entire advertised byte span exposes fake controller translation tables without waiting hours for a sequential `h2testw` pass. Similarly, querying `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist` ROT13 keys gave us objective launch counts before uninstalling any of the 227 applications on the machine.

Local maintenance scripts and forensic artifacts:
- **System Cleanup & Registry Automation (`9 scripts`)**: [Scripts](file:///D:/Tools/Scripts) — includes [Purge_C_Root_Clutter.bat](file:///D:/Tools/Scripts/Purge_C_Root_Clutter.bat), [Purge_OEM_Bloatware.bat](file:///D:/Tools/Scripts/Purge_OEM_Bloatware.bat), [Purge_GlobalProtect_Reg.bat](file:///D:/Tools/Scripts/Purge_GlobalProtect_Reg.bat), [Unblock_Port_24766.bat](file:///D:/Tools/Scripts/Unblock_Port_24766.bat), [inspect_gog.py](file:///D:/Tools/Scripts/inspect_gog.py), and [update_gog_paths.py](file:///D:/Tools/Scripts/update_gog_paths.py).
- **227-Application Bloatware & `UserAssist` Audit**: [software_inventory_and_bloatware_audit.md](file:///C:/Users/ogreb/.gemini/antigravity/brain/cc5f5f1c-7677-4661-a99f-e0d5a2157fa6/software_inventory_and_bloatware_audit.md)
- **NAND Flash `44.38 GiB` Byte-Offset Forensics**: [C128 Brain Session](file:///C:/Users/ogreb/.gemini/antigravity/brain/3e98c00e-6665-4cdf-8a63-f82aef4577c0)
