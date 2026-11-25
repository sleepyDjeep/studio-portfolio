---
id: daily-auto-entry-pipeline
title: 'Daily Auto-Entry Pipeline: Unattended Portfolio Publishing'
subtitle: A scheduled job that finds undocumented studio work, authors one entry,
  rebuilds and publishes it, and reverts its own push if the live site disagrees.
pillar: 01-ai-workflows
entry_type: workflow
readiness: shipped
visibility: main
date_started: '2026-11-25'
date_updated: '2026-11-25'
tags:
- automation
- publishing
- gates
- github-pages
- scheduling
diagram: assets/diagrams/daily-auto-entry-pipeline.svg
local_paths:
- label: Project root
  path: file:///D:/Projects/Studio_Portfolio
---

## What It Is & Why It Matters

The portfolio used to depend on someone remembering to write an entry after each build. This pipeline turns that into a daily job: it reads the studio's own local record of work, picks one topic that is not yet documented, and produces a complete entry with the same frontmatter, four sections and diagram rules that hand-written entries follow. When no model key is configured it writes a handoff instead, containing the candidate facts, the exact prompt and the schema, so the entry can be authored in a chat and dropped back into the repo. The published site therefore stays a record of the studio's actual work without a person having to sit down and write every page.

## Real Example: How It Works in Practice

- **Input**: a run of `tools/daily_publish.py`, from Task Scheduler at 07:00 or by hand, with either an API key or an authored payload waiting in `data/intake/authored.json`.
- **What Happens**: intake groups unmapped memories, conversations and project folders, the entry is written and checked against the frontmatter schema, the baseline records the new id and its media, the bundle is rebuilt, gates 2-5 run, and the result is committed with the `[auto-entry]` marker and pushed. The push triggers the entry live check, which waits for Pages and hashes the new diagram or images.
- **Output**: either a live entry verified from the deployed site, or a reverted commit when the live check fails, with the attempt recorded in the ledger and the branch back at its previous content.

## Where It Stands & Next Steps

The pipeline is installed: keyless handoff, keyed generation, a scheduled 07:00 task, a seven-entry weekly cap, three attempts per candidate and a lock against overlapping runs. What it does not do yet is judge the quality of a candidate beyond the structural checks, so the next useful step is a review pass that compares an auto entry with a hand-written one and tightens the prompt or the filters where they diverge. Until then the ledger and the commit history are the audit trail for every page it adds.

## Under the Hood & Local Files

`tools/daily_publish.py` owns intake, the ledger, the lock, the commit, the push and the revert; `tools/auto_entry.py` owns the draft schema, validation, media copying and the SVG sanitiser. The handoff and authored payload live under `data/intake/`, which is gitignored, and the ledger is `data/intake/ledger.json`. A run is started with `python tools/daily_publish.py` or by the scheduled task `Studio Portfolio Daily Publish`, which calls `tools/run_daily.cmd`; logs land in `data/logs/`. Everything after the commit reuses the existing gates and the push-triggered live check, so there is no second set of rules for generated pages.
