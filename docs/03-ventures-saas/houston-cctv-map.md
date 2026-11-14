---
id: "houston-cctv-map"
title: "Houston Live CCTV & Traffic Camera Intelligence Map"
subtitle: "Zero-API-key geospatial operations map clustering 1,077 Greater Houston freeway and public cameras at 60 FPS with a 2x2 live monitoring wall."
pillar: "03-ventures-saas"
entry_type: "project"
readiness: "shipped"
visibility: "main"
date_started: "2026-09-09"
date_updated: "2026-09-09"
tags:
  - "geospatial-gis"
  - "fastapi"
  - "maplibre-gl"
  - "real-time-feeds"
  - "civic-intelligence"
  - "zero-api-key"
metrics:
  - label: "Active Camera Nodes"
    value: "1,077 Indexed Feeds"
  - label: "Freeway Coverage"
    value: "1,066 Houston TranStar Cams"
  - label: "Operator Video Wall"
    value: "2x2 Live Matrix + 6-Frame Burst"
  - label: "External API Cost"
    value: "$0 (Zero Billing Keys)"
media:
  - src: "assets/media/houston-cctv-map/live-map-dashboard.png"
    kind: "authentic"
    caption: "Live capture of the Houston CCTV Geospatial Intelligence Map clustering 1,077 TranStar and public cameras with a 2x2 live feed matrix."
diagram: ""
tech_stack:
  - "Python 3.13 & FastAPI"
  - "httpx Async Proxy"
  - "SQLite Spatial Cache"
  - "MapLibre GL JS"
  - "CartoDB Dark Matter Vector Tiles"
  - "BeautifulSoup4"
local_paths:
  - label: "houston_cctv_map"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map"
  - label: "One-Command Launcher"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/run.py"
  - label: "Automated Test Suite"
    path: "file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/test_suite.py"
run_commands:
  - label: "Initialize DB & Launch Map (:8000)"
    command: "cd \"C:\\Users\\ogreb\\.gemini\\antigravity\\scratch\\houston_cctv_map\" && python run.py"
  - label: "Run 4-Battery Verification Suite"
    command: "cd \"C:\\Users\\ogreb\\.gemini\\antigravity\\scratch\\houston_cctv_map\" && python test_suite.py"
memory_ids:
  - "4f28730f-7db6-4ed8-8904-064ef186d33b"
conversation_ids:
  - "848dcac9-8e86-4cbc-b60a-9fd5d86a60fd"
---

## What It Is & Why It Matters

Checking real-time road, weather, or flood conditions across Greater Houston normally means clicking one tiny highway icon at a time inside dated municipal web tables while fighting broken popups and cross-origin browser blocks. Commercial geospatial dashboards solve the UI problem, but they require metered Mapbox or Google Maps API keys that rack up charges as soon as map tiles and live refreshes scale. We built the **Houston Live CCTV & Traffic Camera Intelligence Map** in a single focused sprint on September 9, 2026 to prove we could stand up a zero-cost, 60 FPS civic-intelligence map with a single Python command.

Running locally on `http://localhost:8000`, the application discovers and indexes **1,077 active camera endpoints** across the Houston metropolitan area—combining **1,066 official Houston TranStar freeway cameras** (spanning I-10 Katy and East, I-45 North and Gulf, I-69/US-59, Loop 610, Beltway 8, US-290, SH-288, SH-225, and SH-99 Grand Parkway) with **11 public skyline and street-level MJPEG webcams**.

Rather than forcing the user to open and close single-camera modals, the dark-mode operator interface pairs GPU-accelerated vector clustering with instant cross-street search, multi-frame motion burst playback, and a **docked 2x2 simultaneous monitoring wall** so four highway interchanges can be watched side by side during storms, evacuations, or rush-hour incidents.

## Real Example: How It Works in Practice

- **Input**: One terminal command (`python run.py`), followed by typing `"I-45"` or `"610"` into the debounced corridor search bar and pinning four major interchanges to the live monitoring dock.
- **What Happens**:
  1. On startup, `run.py` initializes `backend/cameras.db` in SQLite, executes `transtar.py` and `web_crawler.py` to scrape and geocode 1,077 active Houston camera coordinates, boots the FastAPI server on port `8000`, and opens the browser.
  2. The frontend (`static/app.js`) loads **MapLibre GL JS** over free **CartoDB Dark Matter** vector tiles (`$0` API keys) and requests `/api/cameras?geojson=true`, grouping dense downtown and loop interchanges into color-coded count clusters that expand smoothly at 60 FPS as you zoom.
  3. Clicking any marker or pinning up to four cameras into the floating 2x2 matrix routes image and stream requests through FastAPI's asynchronous `httpx` proxy (`/api/cameras/{id}/snapshot?frame=1..6` and `/api/cameras/{id}/stream`), stripping upstream hotlink/CORS restrictions and substituting a clean inline SVG status card if a municipal roadside camera goes dark.
  4. For TranStar cameras that publish sequential motion buffers, the client's **Burst Motion Engine** cycles frames `1..6` in a continuous loop, turning static roadside JPEGs into fluid traffic-flow animations.
- **Output**: A live, zero-CORS tactical traffic wall streaming four simultaneous freeway interchanges alongside an interactive 1,077-node Greater Houston vector map.

## Where It Stands & Next Steps

The project is **shipped** and self-contained at `C:\Users\ogreb\.gemini\antigravity\scratch\houston_cctv_map`, totaling **1,932 lines of source code** across 8 Python modules (`979 LOC`) and 3 vanilla frontend files (`953 LOC`). All **4 automated test batteries** in `test_suite.py`—covering SQLite spatial CRUD, live TranStar/webcam extraction, FastAPI GeoJSON/filter endpoints, and upstream snapshot proxy fallback behavior—pass out of the box.

Concrete next steps if promoted from a local utility to a public or multi-metro civic tool:
- **NWS Radar & Bayou Flood-Gauge Overlay**: Layer free NOAA/NWS NEXRAD precipitation tiles and Harris County Flood Control District (`HCFCD`) creek-stage gauges onto the MapLibre canvas so operators can correlate flooded underpasses visually with rising bayou sensors.
- **Multi-Metro TxDOT Adapter**: Parameterize `transtar.py` to ingest statewide TxDOT ITS camera feeds for Austin, San Antonio, and Dallas–Fort Worth from a dropdown metro selector.
- **Local Vision Congestion Tagging**: Run periodic 4-camera matrix snapshots through a lightweight local vision classifier to flag stalled-lane queues automatically without human watching.

## Under the Hood & Local Files

### Technical Architecture & Design Choices

- **Zero-Key Vector Tile Stack (`static/app.js` & `static/index.html`)**: By pairing open-source `MapLibre GL JS` with public `CartoDB Dark Matter` vector styles and GeoJSON source clustering, the map renders over a thousand interactive camera nodes with zero account registration, billing tokens, or rate-limit surprises.
- **Async `httpx` CORS & Burst Proxy (`backend/app.py`)**: Municipal camera servers frequently serve mixed HTTP content, omit `Access-Control-Allow-Origin` headers, or drop connections under load. Routing `/snapshot` and `/stream` through an async FastAPI proxy normalizes headers, supports `?frame=1..6` TranStar motion-burst indexing, and guarantees the browser UI never hangs on a dead socket.
- **Indexed SQLite Corridor Store (`backend/db.py`)**: Camera metadata—roadway, cross street, cardinal direction, latitude/longitude, feed type, and source—persists locally in SQLite so subsequent launches boot instantaneously and `POST /api/sync` can refresh camera rosters in the background without interrupting active 2x2 video streams.

### Local Directory & Key Clickable Files

- **Project Root**: [houston_cctv_map](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map) (`1,932 LOC`)
- **Documentation & Dependencies**: [README.md](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/README.md), [requirements.txt](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/requirements.txt)
- **Single-Command Runner & Test Harness**: [run.py](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/run.py), [test_suite.py](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/test_suite.py)
- **FastAPI Proxy & SQLite Index**: [app.py](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/backend/app.py), [db.py](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/backend/db.py)
- **Camera Ingestion Scrapers**: [transtar.py](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/backend/scrapers/transtar.py), [web_crawler.py](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/backend/scrapers/web_crawler.py)
- **MapLibre GL Frontend & 2x2 Matrix**: [index.html](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/static/index.html), [app.js](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/static/app.js), [styles.css](file:///C:/Users/ogreb/.gemini/antigravity/scratch/houston_cctv_map/static/styles.css)
