# Studio Portfolio: project rules

"Add this to the studio portfolio" means this checklist. Work from the repository
root; `README.md` covers the rest.

1. **Doc** — `docs/<pillar>/<slug>.md`, with `pillar` set to that folder's id
   (`00-studio-primer`, `01-ai-workflows`, `02-games-engines`, `03-ventures-saas`,
   `04-creative-3d-media`, `05-hardware-retro`) and a unique `id` (the filename
   stem by default) that becomes the `#entry=<id>` URL.
2. **Frontmatter** — Gate 2 needs non-empty `id`, `title`, `subtitle`, `pillar`,
   `entry_type`, `readiness`, `visibility`. Use an existing `entry_type`
   (`project`, `workflow`, `idea`) and `readiness` (`shipped`, `active-build`,
   `reusable-workflow`, `blueprint`) so the badges and views recognize it.
3. **At least one visual** —
   - `media:` items with `src` and `kind` (`authentic`, `concept`, `audio`); the
     file must exist, be non-empty and be committed. Files under
     `assets/concepts/` must be `concept`. New files go in
     `assets/media/<slug>/`.
   - or `diagram: "assets/diagrams/<slug>.svg"`, inlined into the page and
     hashed, so it must exist and be committed.
4. **Four sections, exact headings, 80+ characters each**:
   `## What It Is & Why It Matters`,
   `## Real Example: How It Works in Practice`,
   `## Where It Stands & Next Steps`,
   `## Under the Hood & Local Files`.
   `**Input**:` / `**What Happens**:` / `**Output**:` in the example become the
   page's three example cards.
5. **Baseline** — a new id fails Gate 2 until recorded:
   `python tools/verify_portfolio.py --update-baseline`, then commit
   `tools/expected_entries.json`.
6. **Rebuild** — `python tools/update_portfolio.py` builds the bundle, runs all
   five gates, proves the bundle matches a clean rebuild, then snapshots the
   private manifest; it stops at the first failure. Without the local databases,
   add `--no-verify` and run `python tools/verify_portfolio.py --skip-coverage`.
7. **Commit** — doc, media, `tools/expected_entries.json` and the rebuilt
   `portfolio-data.js` together; the pre-commit hook rejects a stale bundle.
   `portfolio-data.js` is generated, never hand-edited. Push to `main`; a
   scheduled check samples the deployed bytes.

Private paths stay out of git and the bundle: `data/`, `docs/vault/`,
`assets/vault/`, `portfolio-vault.js` (Gate 5). Gate 4 rejects its slop lexicon
across `docs/`, `index.html`, `app.js`, `styles.css`, `DESIGN.md` and `README.md`.
Ask one question only when the artifact or pillar is genuinely unclear. Subagents
do not inherit these instructions, so pass the relevant lines to one you delegate.
