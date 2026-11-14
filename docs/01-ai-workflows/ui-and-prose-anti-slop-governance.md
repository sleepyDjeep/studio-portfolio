---
id: "ui-and-prose-anti-slop-governance"
title: "UI, Prose & Engine Anti-Slop Governance"
subtitle: "Three studio-wide quality guardrails that strip generic AI gradients, synthetic filler copywriting, and deprecated Godot 4.x API hallucinations before they ship."
pillar: "01-ai-workflows"
entry_type: "workflow"
readiness: "reusable-workflow"
visibility: "main"
date_started: "2026-08-23"
date_updated: "2026-11-12"
tags:
  - "design-governance"
  - "ui-skills-mcp"
  - "anti-slop"
  - "godot-4.7"
  - "compiler-guardrails"
metrics:
  - label: "Governance Layers"
    value: "3"
  - label: "Godot APIs Mapped"
    value: "4.0 -> 4.7"
  - label: "Deprecation Dataset"
    value: "68 KB JSON/YAML"
  - label: "Allowed Filler Hits"
    value: "0"
media: []
diagram: "assets/diagrams/ui-and-prose-anti-slop-governance.svg"
tech_stack:
  - "UI Skills MCP"
  - "Markdown Agent Skills"
  - "CSS Custom Properties"
  - "JSON / YAML Guardrail Schemas"
  - "Regex Verification Gates"
local_paths:
  - label: "Global /ui Skill"
    path: "file:///C:/Users/ogreb/.gemini/config/skills/ui"
  - label: "Global Prose Skill"
    path: "file:///C:/Users/ogreb/.gemini/config/skills/prose"
  - label: "Godot 4.0-4.7 Deprecations JSON"
    path: "file:///D:/Projects/godot_deprecations_4.0_to_4.7.json"
  - label: "Root GDScript Guardrail"
    path: "file:///D:/Projects/CLAUDE.md"
run_commands:
  - label: "Inspect Godot Deprecation Entries"
    command: "python -c \"import json; d=json.load(open('D:/Projects/godot_deprecations_4.0_to_4.7.json')); print(len(d['deprecations']), 'guarded API changes')\""
memory_ids:
  - "ef4919d0-2930-4e5b-8893-76e01910d62d"
  - "61c9258e-ad1c-4465-89ed-f97b1e8a3471"
  - "3386fef6-caaf-43bf-b8b4-c61ec5c24b20"
conversation_ids: []
---

## What It Is & Why It Matters

Left unguarded, large language models converge on three unmistakable failure modes: web pages covered in glowing purple-and-cyan SaaS cards, documentation stuffed with cheerleading transitions and repetitive three-part slogans, and game scripts calling engine methods removed two versions ago. Between August 23 and August 25, 2026, we codified three mandatory studio guardrails that intercept all three failure modes at authoring time.

First, our global `/ui` skill connects every frontend task directly to the `ui-skills` MCP catalog (`ibelick/baseline-ui`, `ibelick/create-design-md`, `mengto/landing-page`, and `mengto/pricing-page`). It bans cookie-cutter three-column gradient cards and floating decorative blobs, replacing them with high-contrast structural borders, monospace tabular numerals (`tabular-nums`), dynamic viewport sizing (`100dvh`), balanced headings (`text-wrap: balance`), and minimum `44px` touch targets.

Second, our global `prose` skill enforces strict editorial rules adapted from `jalaalrd/anti-ai-slop-writing` and `realrossmanngroup/no_ai_slop_writing_rules`, paired with automated regex scanners that reject any document containing overused AI filler verbs, theatrical metaphors, throat-clearing praise, or formulaic "not X, it's Y" contrasts. Third, for game engineering, we built a machine-readable `godot_deprecations_4.0_to_4.7` dataset (`.json` and `.yaml`) paired with root `CLAUDE.md` instructions so coding agents never emit obsolete Godot 4.0–4.6 symbols when targeting Godot 4.7.

## Real Example: How It Works in Practice

- **Input**: An agent is tasked with building a pricing comparison page for `PropertyIntel` (`property.vectorfeedhq.com`) in the morning and writing a `Skeleton3D` procedural bone-ik controller in Godot 4.7 for `MechDestroyer` in the afternoon.
- **What Happens**:
  1. **UI Governance Pass**: Before writing HTML or CSS, the `/ui` directive queries `ui-skills` MCP (`baseline-ui` and `pricing-page`), applying clean Maven-inspired light structural borders, `JetBrains Mono` `tabular-nums` alignment on `$25 / $40 / $99` pricing tiers, and restrained micro-interactions without neon glow clutter.
  2. **Copywriting Gate**: All landing-page copy and documentation pass through the `prose` standard—opening directly with county counts (`3,143` US counties) and concrete mechanisms, varying sentence length deliberately, and passing a zero-tolerance banned-lexicon check.
  3. **Compiler API Lookup**: Before writing GDScript, the agent reads `godot_deprecations_4.0_to_4.7.json`, sees that `Skeleton3D.bone_pose_changed` was replaced in Godot 4.3 by `skeleton_updated` (with the bone-index callback parameter dropped, flagged `safe_blind_apply: false`), and writes clean Godot 4.7 syntax on the first pass.
- **Output**: Human-grade web typography on `property.vectorfeedhq.com`, crisp partner-ready technical prose with zero synthetic clichés, and GDScript modules that compile cleanly in headless Godot 4.7 without deprecation warnings.

## Where It Stands & Next Steps

All three governance layers are active reusable workflows wired into `~/.gemini/config/skills/` and `D:\Projects\`. Every web dashboard in the VectorFeedHQ 8-app fleet, our interactive business simulators (*Guadalupe Loop Biosystems* and *Artisan Timber Co.*), all 6+ Godot 4.7 codebases, and all 44 entries in this Studio Portfolio are governed by these exact rules—including an automated Wave 5 regex gate verifying `0` banned prose hits across the entire repository.

Next steps to extend the governance suite:
- Extend `godot_deprecations_4.0_to_4.7.json` with a companion Blender `4.x -> 5.1` Python API migration file capturing Principled BSDF socket renames (`Specular IOR Level`, `Transmission Weight`) and `bgl`-to-`gpu` shader module replacements.
- Package our CSS token baseline and prose regex linter into a pre-commit CLI check inside `D:\Tools\Scripts`.

## Under the Hood & Local Files

### Technical Enforcement Mechanisms
- **`/ui` MCP Directives (`ui/SKILL.md`)**: Enforces semantic HTML5, CSS `clamp()` fluid typography, container queries, subtle `#e2e8f0` / `#1e293b` structural hairlines, and zero bloated CSS framework dependencies unless requested.
- **Asymmetric Prose Rhythm (`prose/SKILL.md`)**: Eliminates cheerleading openers, wrap-up summaries, mechanical triplets, and banned synthetic vocabulary, requiring active voice and exact quantitative nouns.
- **Token-Aware GDScript Migration (`godot_deprecations_4.0_to_4.7.json`)**: Every entry documents `class`, `member`, `change`, `replacement`, `gdscript_breaking`, `changed_in`, official migration guide + GitHub PR URLs, and a structured `autofix` object (`regex_find`, `regex_replace`, and `safe_blind_apply` boolean warning against class-name collisions like `Timer.process_callback` vs `AnimationTree.process_callback` or inverted booleans like `GraphEdit.show_arrange_button`).

### Key Local Files
- [SKILL.md](file:///C:/Users/ogreb/.gemini/config/skills/ui/SKILL.md) — Global `/ui` skill specification binding frontend tasks to `ui-skills` MCP.
- [SKILL.md](file:///C:/Users/ogreb/.gemini/config/skills/prose/SKILL.md) — Anti-AI-slop editorial ruleset enforced across studio copy and documentation.
- [CLAUDE.md](file:///D:/Projects/CLAUDE.md) — Workspace-root agent rule mandating deprecation lookups prior to GDScript edits.
- [godot_deprecations_4.0_to_4.7.json](file:///D:/Projects/godot_deprecations_4.0_to_4.7.json) — `35 KB` machine-readable JSON deprecation database with PR provenance and `safe_blind_apply` regex metadata.
- [godot_deprecations_4.0_to_4.7.yaml](file:///D:/Projects/godot_deprecations_4.0_to_4.7.yaml) — `33 KB` human-scannable YAML mirror of the Godot 4.0–4.7 API migration ledger.
