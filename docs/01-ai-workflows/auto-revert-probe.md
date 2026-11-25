---
id: auto-revert-probe
title: Auto-Revert Probe
subtitle: A short-lived entry used to prove the daily publisher reverts its own push
  when the live check fails.
pillar: 01-ai-workflows
entry_type: workflow
readiness: shipped
visibility: main
date_started: '2026-11-25'
date_updated: '2026-11-25'
tags:
- testing
- revert
diagram: assets/diagrams/auto-revert-probe.svg
local_paths:
- label: Project root
  path: file:///D:/Projects/Studio_Portfolio/tools
---

## What It Is & Why It Matters

This entry exists only to prove the revert path of the daily publisher. It is written like a normal entry so every gate and the live check run exactly as they would for real work, and it is expected to disappear from the branch after the forced failure.

## Real Example: How It Works in Practice

- **Input**: a candidate passed with `--candidate` and a payload authored from the handoff.
- **What Happens**: the entry is written, the baseline and bundle are rebuilt, gates pass, and the commit is pushed with the auto marker.
- **Output**: the forced failure triggers a revert commit, so the branch returns to its previous content.

## Where It Stands & Next Steps

Nothing here is meant to survive. The point is that a failed live check leaves no half-applied entry, no orphan diagram and no dirty tree, and the ledger keeps the failed attempt instead of pretending the entry published.

## Under the Hood & Local Files

The switch is the environment variable `AUTO_ENTRY_FORCE_LIVE_FAILURE=1`, read only after a successful push. The revert uses `git revert --no-edit HEAD` followed by a push, and the ledger records the attempt in `data/intake/ledger.json`.
