---
version: alpha
name: Studio Portfolio
description: Partner-facing editorial guide and interactive portfolio indexing our studio's AI infrastructure, games, business ventures, creative pipelines, and hardware builds.
colors:
  background-primary: "#ffffff"
  background-secondary: "#f8fafc"
  background-subtle: "#f1f5f9"
  foreground-primary: "#0f172a"
  foreground-secondary: "#475569"
  foreground-muted: "#64748b"
  border-default: "#e2e8f0"
  border-strong: "#cbd5e1"
  accent-primary: "#2563eb"
  accent-hover: "#1d4ed8"
  accent-subtle: "#eff6ff"
  status-shipped: "#15803d"
  status-active: "#0369a1"
  status-blueprint: "#b45309"
  status-workflow: "#4338ca"
typography:
  sans:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
  mono:
    fontFamily: "'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, monospace"
  display:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "32px"
    lineHeight: "38px"
    fontWeight: 700
  heading:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "20px"
    lineHeight: "28px"
    fontWeight: 600
  body:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "15px"
    lineHeight: "24px"
    fontWeight: 400
  caption:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "13px"
    lineHeight: "18px"
    fontWeight: 500
rounded:
  sm: "6px"
  base: "10px"
  lg: "14px"
  pill: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  section: "48px"
---

## Overview

Studio Portfolio is a zero-build, offline-capable Partner & Collaborator Guide covering every software build, AI toolchain, business venture, creative pipeline, and hardware system created since August 2026. It defaults to a clean Editorial Light presentation with high typographic contrast, structural `1px` borders, and a single royal-blue interactive accent, paired with a one-click Dark Studio mode for low-light review.

## Colors

Surface hierarchy relies on crisp luminance steps (`{colors.background-primary}` cards over `{colors.background-secondary}` canvas) separated by `1px` structural borders (`{colors.border-default}`) rather than heavy drop shadows or colored fills. Reserve `{colors.accent-primary}` strictly for primary interactive affordances, active view tabs, focus rings, and links. Semantic readiness badges use restrained high-contrast foreground/border pairs rather than saturated neon pills.

## Themes

Editorial Light is the default mode on initial load unless overridden by user selection in `localStorage`. Dark Studio mode maps every semantic CSS custom property 1-to-1:

| Semantic Token | Editorial Light (Default) | Dark Studio Mode (`[data-theme="dark"]`) |
| :--- | :--- | :--- |
| `--bg-canvas` | `#f8fafc` | `#0b0f17` |
| `--bg-surface` | `#ffffff` | `#131a26` |
| `--bg-subtle` | `#f1f5f9` | `#1c2536` |
| `--text-primary` | `#0f172a` | `#f8fafc` |
| `--text-secondary` | `#475569` | `#94a3b8` |
| `--text-muted` | `#64748b` | `#64748b` |
| `--border-default` | `#e2e8f0` | `#1e293b` |
| `--border-strong` | `#cbd5e1` | `#334155` |
| `--accent-primary` | `#2563eb` | `#3b82f6` |
| `--accent-subtle` | `#eff6ff` | `#172554` |

## Typography

Apply `text-wrap: balance` on all page, pillar, card, and drawer headings, and `text-wrap: pretty` on all body paragraphs and descriptions. Apply `font-variant-numeric: tabular-nums` to all summary counters, dates, test counts, financial figures, and timeline markers so columns and pills never jitter. Do not alter letter-spacing (`tracking`) on body or heading text.

## Layout

Use a fluid container (`max-width: 1360px`, centered with responsive horizontal padding) and CSS Grid (`repeat(auto-fill, minmax(min(100%, 340px), 1fr))`) for project cards. Size full-height drawers and modals with `100dvh` (never `100vh`) and respect `env(safe-area-inset-*)` on mobile viewports (`390x844`). Maintain a strict fixed `z-index` scale: sticky header (`20`), slide-over backdrop (`40`), slide-over reader drawer (`50`), lightbox overlay (`60`).

## Elevation & Depth

Prefer `1px solid var(--border-default)` borders over shadows for resting cards. Use subtle neutral elevation (`0 1px 3px rgba(15, 23, 42, 0.06)`) on cards and a clean edge shadow (`-12px 0 32px rgba(15, 23, 42, 0.14)`) on the slide-over reader drawer. Never apply decorative colored glow shadows.

## Shapes

Cards use `{rounded.lg}` with overflow-clipped `16:9` media headers. Interactive buttons, search inputs, and code blocks use `{rounded.base}` or `{rounded.sm}`. Readiness tags, `Authentic` / `Concept Preview` media badges, and metric chips use `{rounded.pill}`.

## Components

- **Interactive Controls**: Every button, tab, theme toggle, drawer close control, and vault switch must provide a minimum `44px x 44px` hit target and a visible `:focus-visible` outline (`2px solid var(--accent-primary)`). Icon-only buttons require explicit `aria-label` attributes.
- **Media Preview Header**: Fixed `16:9` aspect ratio (`aspect-ratio: 16 / 9`) with `object-fit: cover` to prevent layout shift (`CLS = 0`). Overlay a high-contrast top-left badge distinguishing `Authentic Capture` from `Concept Preview`.
- **Slide-Over Reader & Lightbox**: Animate exclusively on compositor properties (`transform`, `opacity`) with `ease-out` timing `<= 200ms`, and disable motion when `@media (prefers-reduced-motion: reduce)` matches. Support `Escape` key and backdrop click dismissal, plus `#entry=<slug>` hash routing.
- **Under the Hood Drawer**: Native `<details>` / `<summary>` disclosure inside each entry reader containing embedded responsive SVG architecture diagrams (`currentColor` / theme-adaptive tokens), copyable CLI commands, Memory Bank decisions, and clickable `file:///` links.
- **Private Vault Switch**: Discrete footer control (`Show Private Vault (N)`), defaulting to `OFF` on every fresh load so zero `visibility: "vault"` DOM nodes, thumbnails, or search hits exist until explicitly toggled on.

## Do's and Don'ts

- **Do** lead every card and reader view with plain, concrete English and a structured `Input -> What Happens -> Output` walkthrough before technical architecture.
- **Do** badge every AI-illustrated blueprint thumbnail and lightbox caption with an unmistakable `Concept Preview` pill.
- **Don't** use purple, cyan, or multicolor gradients anywhere in backgrounds, borders, or text.
- **Don't** use decorative blurred glow blobs or pulsing animations.
- **Don't** animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`) or exceed `200ms` on UI transitions.
- **Don't** use `100vh` for viewport-height drawers or overlays; always use `100dvh`.
