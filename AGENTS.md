# Studio Portfolio: project rules

The atlas is a static GitHub Pages site generated from `docs/`. `README.md` has
the long version; this file is what "Add this to the studio portfolio" resolves
to. Work from the repository root and finish the checklist before reporting back.

## "Add this to the studio portfolio"

1. **Entry doc** at `docs/<pillar>/<slug>.md`. The filename stem is the
   frontmatter `id` and the URL anchor. Pillars: `00-studio-primer`,
   `01-ai-workflows`, `02-games-engines`, `03-ventures-saas`,
   `04-creative-3d-media`, `05-hardware-retro`.
2. **Frontmatter** — Gate 2 requires `id`, `title`, `subtitle`, `pillar`,
   `entry_type`, `readiness`, `visibility`; fill `date_started`, `date_updated`,
   `tags`, `metrics`, `tech_stack`, `local_paths` and `run_commands` with real
   values, and include at least one visual:
   - `media:` items with `src`, `kind` (`authentic`, `concept` or `audio`) and a
     `caption`; put the files in `assets/media/<slug>/`. A file under
     `assets/concepts/` must use `kind: "concept"`.
   - or `diagram: "assets/diagrams/<slug>.svg"`; the builder inlines the SVG and
     hashes the file, so it must exist on disk.
3. **Four sections, exact headings, 80+ characters each**:
   `## What It Is & Why It Matters`,
   `## Real Example: How It Works in Practice`,
   `## Where It Stands & Next Steps`,
   `## Under the Hood & Local Files`.
   In the example, label `**Input**:`, `**What Happens**:` and `**Output**:` so
   the builder can build the interactive example.
4. **Baseline** — a new public id fails Gate 2 until it is recorded:
   `python tools/verify_portfolio.py --update-baseline`, then commit
   `tools/expected_entries.json`. Adding media or text to an existing entry needs
   no baseline change.
5. **Rebuild** — `python tools/update_portfolio.py` runs the builder, the
   verifier (all five gates), the bundle freshness comparison and the private
   manifest snapshot. Without the local memory databases, add `--no-verify` and
   then run `python tools/verify_portfolio.py --skip-coverage` yourself.
6. **Commit** — the doc, its media, `tools/expected_entries.json` and the
   regenerated `portfolio-data.js` in one commit. The pre-commit hook rejects a
   bundle older than the docs. Push to `main`; the live check verifies the deploy.

## Boundaries

- `data/`, `docs/vault/`, `assets/vault/` and `portfolio-vault.js` are private and
  gitignored. Never put them in a commit, a bundle or an asset path; Gate 5 fails
  on a vault leak. A `visibility: vault` entry stays local.
- Write plainly. Gate 4 rejects a fixed list of AI filler words (see
  `BANNED_PATTERNS` in `tools/verify_portfolio.py`) across every doc, `README.md`
  and the page shell.
- Never edit `portfolio-data.js` by hand; it is generated. Every rebuild rewrites
  `compiled_at`, so commit only when the content changed.
- Ask one question only when the artifact or its pillar is genuinely unclear.
  Otherwise pick the closest pillar and say what you assumed.
- This checklist is for adding an entry. Changing the site itself (`app.js`,
  `styles.css`, `index.html`) is a normal code change, not this phrase.
