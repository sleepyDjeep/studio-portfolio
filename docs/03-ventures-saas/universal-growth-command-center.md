---
id: "universal-growth-command-center"
title: "Universal Growth & Intelligence Command Center"
subtitle: "Autonomous B2B social-intent listener, multi-platform copywriter, partner CRM, and scraper circuit-breaker plane running on port 8050."
pillar: "03-ventures-saas"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-08-23"
date_updated: "2026-08-27"
tags:
  - "growth-automation"
  - "social-listening"
  - "b2b-outreach"
  - "observability"
  - "openapi"
  - "saas-ops"
metrics:
  - label: "Wave 1 Investor Dispatch"
    value: "198 / 198 Delivered (25 Metros)"
  - label: "Buyer-Intent Scorer"
    value: "0–100 Scale (60+ Stage Gate)"
  - label: "B2B Partner Directory"
    value: "40+ REIA & Creator Targets"
  - label: "Control Plane Port"
    value: "HTTP :8050 + OpenAPI Spec"
media:
  - src: "assets/media/universal-growth-command-center/ugi-dashboard.png"
    kind: "authentic"
    caption: "Live browser capture of the Universal Growth & Intelligence Command Center interface (ugicommand.vectorfeedhq.com)."
diagram: ""
tech_stack:
  - "Python 3.13"
  - "REST & OpenAPI 3.1"
  - "SQLite"
  - "Resend Email API"
  - "Vanilla JS & CSS SPA"
  - "Cloudflare Pages"
local_paths:
  - label: "universal_growth_center"
    path: "file:///D:/Projects/PropertyIntel/universal_growth_center"
  - label: "CLI & Server Launcher"
    path: "file:///D:/Projects/PropertyIntel/run_growth_command_center.py"
run_commands:
  - label: "Start UGI Server (:8050)"
    command: "cd \"D:\\Projects\\PropertyIntel\" && python run_growth_command_center.py --server --port 8050"
  - label: "Check Telemetry & Quotas"
    command: "cd \"D:\\Projects\\PropertyIntel\" && python run_growth_command_center.py --status"
  - label: "Run Discovery & Draft Cycle"
    command: "cd \"D:\\Projects\\PropertyIntel\" && python run_growth_command_center.py --cycle"
memory_ids:
  - "a0b71bd1-f3e1-47c4-a93b-8c9457f1491a"
conversation_ids:
  - "7e41cc88-eaad-4f3b-8fde-00222cc908b9"
  - "cd5f1b26-4408-4808-a757-eabe804fcdf7"
  - "3116187a-85c0-4b2f-b4ce-6fc5fb64f395"
---

## What It Is & Why It Matters

Shipping seven niche public-records SaaS products creates an immediate operational bottleneck. Nobody wants to log into seven separate admin panels to check whether a county clerk changed an HTML table selector, and cold paid ads burn cash fast when targeting specialized buyers like tax-deed investors, probate attorneys, or property-tax consultants. We built the **Universal Growth & Intelligence Command Center (`UGICommand`)** at `ugicommand.vectorfeedhq.com` (and locally on port `:8050`) as a single, domain-agnostic control plane that pairs fleet observability with automated B2B customer acquisition.

On the marketing side, `UGICommand` replaces spray-and-pray outreach with an intent-scored pipeline. It scans public community discussions, scores each post from **0 to 100** for active buying pain, drafts platform-native responses tailored to the active product campaign, and holds every outbound message in a human-reviewed staging queue capped by strict daily persona quotas. Alongside organic social discovery, it manages a curated directory of **40+ Real Estate Investors Associations (REIAs), wholesaling educators, and niche YouTubers**, plus 1-to-1 transactional email dispatch.

On the infrastructure side, the same console acts as the nerve center for the 3,244-jurisdiction scraper fleet. Operators can inspect SHA-256 raw-record provenance hashes, monitor Silent-200 CAPTCHA quarantine queues, and flip 1-click county circuit breakers without touching code or restarting workers.

## Real Example: How It Works in Practice

- **Input**: An active campaign preset (for example, `PropertyIntel` distressed tax-sale data or `ProbateIntel` estate leads), public forum threads where investors complain about $600/month legacy data subscriptions or manual county clerk searches, and a 25-metro regional investor contact roster.
- **What Happens**:
  1. Running `python run_growth_command_center.py --cycle` triggers a discovery sweep across configured community feeds and evaluates every post through the **0–100 Buyer-Intent Scorer** based on urgency signals, competitor price mentions, and county workflow pain.
  2. Posts scoring **60 or higher** enter the SQLite staging queue (`growth_center.db`), where `growth_service.py` synthesizes multiple non-spammy, anti-AI-slop copy variants matched to the target platform's tone and enforces per-handle daily posting caps (`posts_today / daily_cap`).
  3. Through either the 4-tab web SPA (`:8050`) or the interactive terminal review loop (`--review`), the operator approves, edits, or rejects staged drafts in seconds (`[a] Approve Top Draft | [r] Reject All | [s] Skip`).
  4. For direct B2B partnerships and regional investor launches, the outbound dispatcher personalizes 1-to-1 emails referencing local metro auction spreads and logs delivery status row by row.
- **Output**: Staged, human-approved social replies, a structured 40+ partner CRM (`prospective_partners_and_buyers_directory.csv`), and a verified Wave 1 launch ledger (`outreach_campaign_execution_log.csv`) recording **198 / 198 successful 1-to-1 investor inbox deliveries** across 25 US metropolitan markets with zero bounce lockouts.

## Where It Stands & Next Steps

`UGICommand` is **shipped** and verified both as a local Python/REST control plane (`universal_growth_center/` on port `:8050`) and as a cloud-hosted operator interface at `ugicommand.vectorfeedhq.com`. Its backend exposes a complete OpenAPI 3.1 / Swagger specification (`openapi_spec.py`) so autonomous studio agents can query queue depth, inspect county circuit breakers, and stage campaign copy programmatically, verified across **76 dedicated control-plane unit tests** plus the broader **280 / 280** fleet end-to-end suite.

Concrete next steps:
- **Closed-Loop Stripe Attribution**: Pass hashed campaign and variant IDs through landing-page query parameters into Stripe Checkout metadata so `UGICommand` ranks social copy angles by paid conversion rate rather than click-throughs alone.
- **Automated REIA Sample Dossier Refresh**: Schedule monthly county deal sheets tailored to each of the 40+ partner REIAs' home counties so affiliate hosts receive fresh local auction previews before every monthly meetup.
- **Cross-Pillar Campaign Presets**: Add plug-in campaign profiles for non-real-estate studio launches, including the *Kaiju Kiosk* commercial 3D asset kit and *TechWriter* printable micro-guides.

## Under the Hood & Local Files

### Control Plane Architecture & Memory Bank Decisions

We designed `universal_growth_center/` as a decoupled package inside the `PropertyIntel` workspace so it carries zero hard-coded real-estate assumptions in its core state machine:

- **4-Stage Queue State Machine (`growth_service.py` — 74.9 KB)**: Every discovered lead progresses deterministically through `ingested -> staged (score >= 60) -> drafted -> approved -> dispatched`. Automated background jobs are architecturally barred from crossing the `drafted -> approved` boundary without explicit operator or authenticated API confirmation, preventing runaway bot posting.
- **Agent-First OpenAPI 3.1 Surface (`api_server.py` & `openapi_spec.py`)**: Rather than burying logic inside frontend callbacks, every telemetry counter, persona quota, campaign switcher, and scraper circuit-breaker control is backed by documented REST endpoints with live Swagger UI inspection.
- **Anti-Slop Copy Governance (`run_copy_pipeline.py`)**: Outbound copy templates enforce our studio-wide prose rules—banning LLM filler phrases, opening directly with county parcel counts and statutory citations, and formatting financial comparisons in plain numbers.
- **Origin-Verified Edge Security**: When bridged to cloud dashboards, origin requests validate shared WAF verification headers and rate limits before touching SQLite state *(secret tokens and tunnel IDs are stored strictly in local environment variables)*.

### Local Directory & Key Clickable Files

- **Package Root**: [universal_growth_center](file:///D:/Projects/PropertyIntel/universal_growth_center)
- **CLI & Server Launcher**: [run_growth_command_center.py](file:///D:/Projects/PropertyIntel/run_growth_command_center.py), [run_marketing_autopilot.py](file:///D:/Projects/PropertyIntel/run_marketing_autopilot.py), [run_copy_pipeline.py](file:///D:/Projects/PropertyIntel/run_copy_pipeline.py)
- **REST Server & OpenAPI 3.1 Schema**: [api_server.py](file:///D:/Projects/PropertyIntel/universal_growth_center/api/api_server.py), [openapi_spec.py](file:///D:/Projects/PropertyIntel/universal_growth_center/api/openapi_spec.py)
- **Core Scoring, Copy & Circuit-Breaker Service**: [growth_service.py](file:///D:/Projects/PropertyIntel/universal_growth_center/services/growth_service.py)
- **4-Tab Operator Web SPA**: [web/](file:///D:/Projects/PropertyIntel/universal_growth_center/web)
- **Playbook & Affiliation Strategy**: [MARKETING_PLAYBOOK.md](file:///D:/Projects/PropertyIntel/MARKETING_PLAYBOOK.md), [realestateinvesting.affiliation.md](file:///D:/Projects/PropertyIntel/realestateinvesting.affiliation.md)
