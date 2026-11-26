---
id: propertyintel-discovery-engine
title: 'PropertyIntel: Distressed-Property Discovery Engine'
subtitle: An async scraper fleet and a 3,143-county catalog that turn tax-delinquent
  and off-market listings into one deduplicated workbook each week.
pillar: 03-ventures-saas
entry_type: project
readiness: active-build
visibility: main
date_started: '2026-08-14'
date_updated: '2026-08-26'
tags:
- real-estate
- data-pipeline
- web-scraping
- python
- async
- county-records
- saas
diagram: assets/diagrams/propertyintel-discovery-engine.svg
local_paths:
- label: Project root
  path: file:///D:/Projects/PropertyIntel
---

## What It Is & Why It Matters

PropertyIntel is the studio's discovery engine for distressed property: a Python pipeline that sweeps auction sites, county portals and code-enforcement listings, keeps what it finds, and condenses a week of searching into one workbook. It exists because the work it replaces is repetitive and easy to get wrong by hand. Eight sources publish tax-delinquent and off-market parcels in eight different shapes, and each of the 3,143 US county jurisdictions exposes its own portal and table layout. The pipeline holds that variety in one catalog, harvests the sources concurrently, and removes duplicate parcels before anything reaches a reader.

That matters beyond the spreadsheet. The same discovery layer produces the raw material for the studio's public-records products, so an improvement to a county adapter or to the deduplication step raises the quality of every downstream report instead of fixing one customer's export.

## Real Example: How It Works in Practice

- **Input**: a state, a single county id such as `tx_harris`, or no filter at all, plus the county catalog in `config/county_sources.json`.
- **What Happens**: `DiscoveryAgent` fans out to the eight platform adapters concurrently, `PlaywrightScraper` pages through county tables fifty rows at a time, and `QADedupAgent` hashes each address with SHA-256, falling back to the APN when a portal omits one. `PipelineOrchestrator` batches the sweep, and `AlertService` posts anything past the discount threshold to Telegram or Slack.
- **Output**: `./output/property_intelligence_master.xlsx` from `ExcelReportService`, a matching PDF from WeasyPrint, and normalized JSON from `PublisherAgent`. A full cycle is built around 1,000 or more unique records.

## Where It Stands & Next Steps

The five milestones are recorded as done in `PROJECT.md`: concurrent discovery, the nationwide county catalog, deep pagination, the orchestrator with its 1,000-record cycle, and a passing pytest regression suite. What is not done is keeping the county catalog honest over time. A portal that moves a table or renames a column breaks one adapter quietly, and the sweep still reports success with a thinner workbook.

The next step is a selector health check that fetches a sample page for each county and names the ones that fail before a sweep starts, so portal drift shows up as a specific county rather than a missing row. Until that lands, the runbook expects a person to read the first rows of every export.

## Under the Hood & Local Files

`src/agents/` holds `discovery_agent.py`, `orchestrator.py` and `publisher_agent.py`; `src/scrapers/` holds `base_scraper.py`, `playwright_scraper.py`, `master_scraper_fleet.py`, `nationwide_scrapers.py` and the eight platform adapters. `config/county_sources.json` is the county catalog, and `start_pipeline.py` is the entrypoint: `python start_pipeline.py --dry-run`, `--schedule` for the Monday 06:00 APScheduler job, or `--county tx_harris` for one jurisdiction. Deliverables land in `./output/property_intelligence_master.xlsx`, and `pytest tests/ -v` runs the suite.

`DEPLOYMENT.md` describes the FOSS stack the product runs beside: Listmonk for the newsletter, Kill Bill for the $25, $40 and $99 subscription tiers, PostgreSQL and MinIO in docker compose, with a Cloudflare tunnel in front of the API.
