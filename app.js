/* ==========================================================================
   Studio Portfolio — Client Application (app.js)
   Zero-dependency, offline-first interactive controller
   ========================================================================== */

(function () {
  "use strict";

  const DATA = window.PORTFOLIO_DATA || {
    summary: {},
    pillars: [],
    entries: [],
  };

  if (window.location.protocol === "file:" && window.PORTFOLIO_VAULT_DATA) {
    const vp = window.PORTFOLIO_VAULT_DATA.pillars || [];
    const ve = window.PORTFOLIO_VAULT_DATA.entries || [];
    DATA.pillars = (DATA.pillars || []).concat(vp);
    DATA.entries = (DATA.entries || []).concat(ve);
  }

  const IS_HOSTED_WEB = window.location.protocol === "http:" || window.location.protocol === "https:";

  function adaptHtmlForHostedWeb(htmlStr) {
    if (!IS_HOSTED_WEB || !htmlStr) return htmlStr || "";
    return htmlStr
      .replace(/href="file:\/\/\/[^"]*story_worlds_atlas\.html"/gi, 'href="atlas.html"')
      .replace(/<a\s+href="file:\/\/\/[^"]*"[^>]*>(.*?)<\/a>/gi, '<code class="local-ref">$1</code>');
  }

  const READINESS_META = {
    "shipped": {
      label: "Shipped / Verified",
      desc: "Built, tested on disk or live-deployed, and verified ready to run.",
    },
    "reusable-workflow": {
      label: "Reusable Workflow",
      desc: "Repeatable multi-step pipelines, skills, and automated toolchains we reuse across builds.",
    },
    "active-build": {
      label: "Active Prototype",
      desc: "Working vertical slices and active codebases with core loops running locally.",
    },
    "blueprint": {
      label: "Master Blueprint",
      desc: "Detailed engineering specs, financial models, and hardware build plans ready for execution.",
    },
  };

  const TYPE_META = {
    "project": {
      label: "Projects & Platforms",
      short: "Project",
      desc: "Playable games, game engines, web platforms, 3D rigs, and physical hardware builds.",
    },
    "workflow": {
      label: "Reusable Workflows & Pipelines",
      short: "Workflow",
      desc: "Memory synchronization, ComfyUI asset factories, controller normalizers, and agent skills.",
    },
    "idea": {
      label: "Ideas, Ventures & Master Plans",
      short: "Idea & Plan",
      desc: "Executive business models, architectural specifications, and unbuilt system blueprints.",
    },
  };

  const state = {
    view: "pillars",           // pillars | readiness | type | timeline
    pillarFilter: "all",       // all | <pillar-id>
    query: "",
    vaultUnlocked: false,      // ALWAYS false on fresh page load
    activeEntryId: null,
    activeGalleryIndex: 0,
    lightboxItems: [],
    lightboxIndex: 0,
  };

  // DOM References
  const metaScheme = document.querySelector('meta[name="color-scheme"]');
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const themeBtnLabel = document.getElementById("themeBtnLabel");
  const searchInput = document.getElementById("searchInput");
  const clearSearchBtn = document.getElementById("clearSearchBtn");
  const viewTabs = Array.from(document.querySelectorAll(".view-tab"));
  const primerMount = document.getElementById("primerMount");
  const filterPillsMount = document.getElementById("filterPillsMount");
  const portfolioMount = document.getElementById("portfolioMount");
  const vaultToggleBtn = document.getElementById("vaultToggleBtn");
  const vaultToggleLabel = document.getElementById("vaultToggleLabel");

  const readerDialog = document.getElementById("readerDialog");
  const readerCrumbs = document.getElementById("readerCrumbs");
  const readerBody = document.getElementById("readerBody");
  const closeReaderBtn = document.getElementById("closeReaderBtn");
  const copyLinkBtn = document.getElementById("copyLinkBtn");

  const lightboxDialog = document.getElementById("lightboxDialog");
  const lightboxBadges = document.getElementById("lightboxBadges");
  const lightboxStage = document.getElementById("lightboxStage");
  const lightboxCaption = document.getElementById("lightboxCaption");
  const lightboxCounter = document.getElementById("lightboxCounter");
  const lightboxPrevBtn = document.getElementById("lightboxPrevBtn");
  const lightboxNextBtn = document.getElementById("lightboxNextBtn");
  const closeLightboxBtn = document.getElementById("closeLightboxBtn");

  // Utility helpers
  function esc(str) {
    const div = document.createElement("div");
    div.textContent = str == null ? "" : String(str);
    return div.innerHTML;
  }

  function formatMonthYear(isoDate) {
    if (!isoDate) return "";
    const parts = String(isoDate).slice(0, 10).split("-");
    if (parts.length < 2) return isoDate;
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const mIdx = Math.max(0, Math.min(11, parseInt(parts[1], 10) - 1));
    return `${months[mIdx]} ${parts[0]}`;
  }

  function formatFullMonth(ym) {
    const parts = String(ym).split("-");
    if (parts.length < 2) return ym;
    const months = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];
    const mIdx = Math.max(0, Math.min(11, parseInt(parts[1], 10) - 1));
    return `${months[mIdx]} ${parts[0]}`;
  }

  function getVisibleEntries() {
    return (DATA.entries || []).filter((e) => {
      if (!state.vaultUnlocked && e.visibility === "vault") return false;
      return true;
    });
  }

  function getFilteredEntries() {
    const q = state.query.trim().toLowerCase();
    return getVisibleEntries().filter((e) => {
      // Primer entry is featured at top in Pillars view when no search query is active
      if (state.view === "pillars" && !q && state.pillarFilter === "all" && e.pillar === "00-studio-primer") {
        return false;
      }
      if (state.view === "pillars" && state.pillarFilter !== "all" && e.pillar !== state.pillarFilter) {
        return false;
      }
      if (!q) return true;
      return (e.search_text || "").toLowerCase().includes(q);
    });
  }

  // Light-dismiss fallback for browsers without native <dialog closedby="any">
  function attachDialogBackdropFallback(dialogEl) {
    if (!("closedBy" in HTMLDialogElement.prototype)) {
      dialogEl.addEventListener("click", (event) => {
        if (event.target !== dialogEl) return;
        const rect = dialogEl.getBoundingClientRect();
        const inside =
          rect.top <= event.clientY &&
          event.clientY <= rect.top + rect.height &&
          rect.left <= event.clientX &&
          event.clientX <= rect.left + rect.width;
        if (!inside) {
          dialogEl.close();
        }
      });
    }
  }

  // Theme management
  function getCurrentScheme() {
    const c = metaScheme.content;
    if (c === "dark" || c === "light") return c;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function syncThemeLabel() {
    const cur = getCurrentScheme();
    themeBtnLabel.textContent = cur === "dark" ? "Editorial Light" : "Dark Studio";
  }

  function toggleTheme() {
    const next = getCurrentScheme() === "dark" ? "light" : "dark";
    metaScheme.content = next;
    try {
      localStorage.setItem("studio-color-scheme", next);
    } catch (e) {
      // Ignore storage restrictions on strict file:// profiles
    }
    syncThemeLabel();
  }

  // Summary Counters & Vault Switch Label
  function renderHeaderStats() {
    const visible = getVisibleEntries();
    const s = DATA.summary || {};
    const shipped = visible.filter((e) => e.readiness === "shipped").length;
    const workflows = visible.filter((e) => e.entry_type === "workflow" || e.readiness === "reusable-workflow").length;

    document.getElementById("statTotalEntries").textContent = visible.length.toLocaleString();
    document.getElementById("statShipped").textContent = shipped.toLocaleString();
    document.getElementById("statWorkflows").textContent = workflows.toLocaleString();
    document.getElementById("statMemories").textContent = (s.memories_indexed || 0).toLocaleString();
    document.getElementById("statSessions").textContent = (s.conversations_indexed || 0).toLocaleString();

    const vaultCount = (DATA.entries || []).filter((e) => e.visibility === "vault").length;
    vaultToggleBtn.hidden = vaultCount === 0;
    if (vaultCount > 0) {
      vaultToggleBtn.setAttribute("aria-pressed", state.vaultUnlocked ? "true" : "false");
      vaultToggleLabel.textContent = state.vaultUnlocked
        ? `Hide Private Vault (${vaultCount})`
        : `Show Private Vault (${vaultCount})`;
    }
  }

  // Studio Primer Hero Section
  function renderPrimer() {
    const primerEntry = (DATA.entries || []).find((e) => e.pillar === "00-studio-primer");
    if (!primerEntry || state.view !== "pillars" || state.query.trim() !== "") {
      primerMount.innerHTML = "";
      primerMount.hidden = true;
      return;
    }

    primerMount.hidden = false;
    const diagramMarkup = primerEntry.diagram_svg
      ? `<div class="primer-diagram-box">${primerEntry.diagram_svg}</div>`
      : primerEntry.media && primerEntry.media[0]
      ? `<div class="primer-diagram-box"><img src="${esc(primerEntry.media[0].src)}" alt="${esc(primerEntry.media[0].caption)}"></div>`
      : "";

    primerMount.innerHTML = `
      <details class="primer-card" open>
        <summary class="primer-summary">
          <div class="primer-summary-left">
            <span class="primer-badge">Start Here</span>
            <h2 class="primer-heading">${esc(primerEntry.title)}</h2>
          </div>
          <span class="primer-toggle-hint">Collapse / Expand Guide</span>
        </summary>
        <div class="primer-body">
          <div class="primer-copy">
            <p>${esc(primerEntry.subtitle)}</p>
            <p>
              Every project below runs on one shared studio loop: persistent LanceDB memory across Antigravity, LM Studio, and ComfyUI; wave-based specialist agents; and strict automated verification gates.
            </p>
            <div class="primer-actions">
              <button type="button" class="primary-btn" data-open-entry="${esc(primerEntry.id)}">
                Read Full Studio Primer →
              </button>
            </div>
          </div>
          ${diagramMarkup}
        </div>
      </details>
    `;
  }

  // Pillar Filter Pills (shown in Domain Pillars view)
  function renderFilterPills() {
    if (state.view !== "pillars") {
      filterPillsMount.innerHTML = "";
      filterPillsMount.hidden = true;
      return;
    }

    const visible = getVisibleEntries();
    const activePillars = (DATA.pillars || []).filter((p) => {
      if (p.id === "00-studio-primer") return state.query.trim() !== "";
      if (p.id === "vault" && !state.vaultUnlocked) return false;
      return visible.some((e) => e.pillar === p.id);
    });

    filterPillsMount.hidden = false;
    const pillsHtml = [
      `<button type="button" class="filter-pill ${state.pillarFilter === "all" ? "is-active" : ""}" data-pillar-filter="all">
        All Pillars <span class="tabular-nums">(${visible.filter((e) => e.pillar !== "00-studio-primer").length})</span>
      </button>`,
    ];

    for (const p of activePillars) {
      const cnt = visible.filter((e) => e.pillar === p.id).length;
      const isAct = state.pillarFilter === p.id ? "is-active" : "";
      pillsHtml.push(
        `<button type="button" class="filter-pill ${isAct}" data-pillar-filter="${esc(p.id)}">
          ${esc(p.short_title || p.title)} <span class="tabular-nums">(${cnt})</span>
        </button>`
      );
    }

    filterPillsMount.innerHTML = pillsHtml.join("");
  }

  // Card Thumbnail Builder
  function buildCardMediaHtml(entry) {
    const rMeta = READINESS_META[entry.readiness] || { label: entry.readiness };
    const rPill = `<span class="readiness-pill readiness--${esc(entry.readiness)}">${esc(rMeta.label)}</span>`;

    const imgMedia = (entry.media || []).find((m) => m.kind === "authentic" || m.kind === "concept");
    if (imgMedia) {
      const isConcept = imgMedia.kind === "concept";
      const badgeClass = isConcept ? "media-badge--concept" : "media-badge--authentic";
      const badgeText = isConcept ? "Concept Preview" : "Authentic Capture";
      return `
        <div class="card-media-wrap">
          <img src="${esc(imgMedia.src)}" alt="${esc(imgMedia.caption || entry.title)}" loading="lazy" decoding="async">
          <span class="media-badge ${badgeClass}">${badgeText}</span>
          ${rPill}
        </div>
      `;
    }

    if (entry.diagram_svg) {
      return `
        <div class="card-media-wrap">
          <div class="card-svg-thumb">${entry.diagram_svg}</div>
          <span class="media-badge media-badge--authentic">System Diagram</span>
          ${rPill}
        </div>
      `;
    }

    return `
      <div class="card-media-wrap">
        <span class="media-badge media-badge--authentic">Studio Entry</span>
        ${rPill}
      </div>
    `;
  }

  function buildCardHtml(entry) {
    const tMeta = TYPE_META[entry.entry_type] || { short: entry.entry_type };
    const topMetric = (entry.metrics && entry.metrics[0]) || null;
    const metricHtml = topMetric
      ? `<span class="metric-chip tabular-nums"><strong>${esc(topMetric.value)}</strong> ${esc(topMetric.label)}</span>`
      : `<span class="metric-chip tabular-nums"><strong>${entry.memory_count || 0}</strong> Memories</span>`;

    const vaultBadge = entry.visibility === "vault" ? `<span class="vault-pill">Private Vault</span>` : "";

    return `
      <article class="entry-card">
        <button type="button" class="card-trigger" data-open-entry="${esc(entry.id)}" aria-label="Open guide for ${esc(entry.title)}">
          ${buildCardMediaHtml(entry)}
          <div class="card-body">
            <div class="card-meta-top">
              <span class="type-tag">${esc(tMeta.short)}</span>
              ${vaultBadge}
              <span class="tabular-nums">${esc(formatMonthYear(entry.date_updated || entry.date_started))}</span>
            </div>
            <h3 class="card-title">${esc(entry.title)}</h3>
            <p class="card-subtitle">${esc(entry.subtitle)}</p>
            <div class="card-footer">
              ${metricHtml}
              <span class="open-affordance">Open Guide →</span>
            </div>
          </div>
        </button>
      </article>
    `;
  }

  function buildEmptyStateHtml() {
    return `
      <div class="empty-state">
        <h2>No matching portfolio entries</h2>
        <p>No documented projects, workflows, or plans matched "${esc(state.query)}".</p>
        <button type="button" class="primary-btn" id="resetFiltersBtn">Reset Search &amp; Filters</button>
      </div>
    `;
  }

  // Main Portfolio Mount Renderer across all 4 Views
  function renderPortfolio() {
    renderHeaderStats();
    renderPrimer();
    renderFilterPills();

    const entries = getFilteredEntries();
    if (entries.length === 0) {
      portfolioMount.innerHTML = buildEmptyStateHtml();
      const resetBtn = document.getElementById("resetFiltersBtn");
      if (resetBtn) {
        resetBtn.addEventListener("click", () => {
          state.query = "";
          state.pillarFilter = "all";
          searchInput.value = "";
          clearSearchBtn.hidden = true;
          renderPortfolio();
        });
      }
      return;
    }

    if (state.view === "pillars") {
      const sections = [];
      for (const p of DATA.pillars || []) {
        if (p.id === "vault" && !state.vaultUnlocked) continue;
        const group = entries.filter((e) => e.pillar === p.id);
        if (group.length === 0) continue;
        sections.push(`
          <section class="group-section" id="pillar-${esc(p.id)}">
            <header class="group-header">
              <div class="group-title-wrap">
                <h2 class="group-title">${esc(p.title)}</h2>
                <span class="group-count tabular-nums">${group.length}</span>
              </div>
              <p class="group-desc">${esc(p.description || "")}</p>
            </header>
            <div class="card-grid">
              ${group.map(buildCardHtml).join("")}
            </div>
          </section>
        `);
      }
      portfolioMount.innerHTML = sections.join("");
      return;
    }

    if (state.view === "readiness") {
      const order = ["shipped", "reusable-workflow", "active-build", "blueprint"];
      const sections = [];
      for (const rKey of order) {
        const group = entries.filter((e) => e.readiness === rKey);
        if (group.length === 0) continue;
        const meta = READINESS_META[rKey];
        sections.push(`
          <section class="group-section">
            <header class="group-header">
              <div class="group-title-wrap">
                <h2 class="group-title">${esc(meta.label)}</h2>
                <span class="group-count tabular-nums">${group.length}</span>
              </div>
              <p class="group-desc">${esc(meta.desc)}</p>
            </header>
            <div class="card-grid">
              ${group.map(buildCardHtml).join("")}
            </div>
          </section>
        `);
      }
      portfolioMount.innerHTML = sections.join("");
      return;
    }

    if (state.view === "type") {
      const order = ["project", "workflow", "idea"];
      const sections = [];
      for (const tKey of order) {
        const group = entries.filter((e) => e.entry_type === tKey);
        if (group.length === 0) continue;
        const meta = TYPE_META[tKey];
        sections.push(`
          <section class="group-section">
            <header class="group-header">
              <div class="group-title-wrap">
                <h2 class="group-title">${esc(meta.label)}</h2>
                <span class="group-count tabular-nums">${group.length}</span>
              </div>
              <p class="group-desc">${esc(meta.desc)}</p>
            </header>
            <div class="card-grid">
              ${group.map(buildCardHtml).join("")}
            </div>
          </section>
        `);
      }
      portfolioMount.innerHTML = sections.join("");
      return;
    }

    if (state.view === "timeline") {
      const sorted = [...entries].sort((a, b) => {
        const da = a.date_started || a.date_updated || "";
        const db = b.date_started || b.date_updated || "";
        return da.localeCompare(db);
      });
      const byMonth = new Map();
      for (const e of sorted) {
        const ym = String(e.date_started || e.date_updated || "2026-08").slice(0, 7);
        if (!byMonth.has(ym)) byMonth.set(ym, []);
        byMonth.get(ym).push(e);
      }

      const blocks = [];
      for (const [ym, group] of byMonth.entries()) {
        blocks.push(`
          <section class="timeline-month-block">
            <header class="group-header timeline-month-marker">
              <div class="group-title-wrap">
                <h2 class="group-title tabular-nums">${esc(formatFullMonth(ym))}</h2>
                <span class="group-count tabular-nums">${group.length} initiated</span>
              </div>
            </header>
            <div class="card-grid">
              ${group.map(buildCardHtml).join("")}
            </div>
          </section>
        `);
      }
      portfolioMount.innerHTML = `<div class="timeline-stream">${blocks.join("")}</div>`;
    }
  }

  // ==========================================================================
  // Slide-Over Reader Drawer & Lightbox
  // ==========================================================================

  function getVisualItemsForEntry(entry) {
    const items = [];
    for (const m of entry.media || []) {
      if (m.kind === "authentic" || m.kind === "concept") {
        items.push({
          type: "image",
          src: m.src,
          kind: m.kind,
          caption: m.caption || entry.title,
        });
      }
    }
    if (entry.diagram_svg) {
      items.push({
        type: "svg",
        svg: entry.diagram_svg,
        kind: "diagram",
        caption: `${entry.title} — System & Workflow Architecture Diagram`,
      });
    }
    return items;
  }

  function renderGalleryStage(entry) {
    const visuals = getVisualItemsForEntry(entry);
    const audios = (entry.media || []).filter((m) => m.kind === "audio");

    let visualHtml = "";
    if (visuals.length > 0) {
      const idx = Math.min(state.activeGalleryIndex, visuals.length - 1);
      const cur = visuals[idx];
      const isConcept = cur.kind === "concept";
      const badgeClass = isConcept ? "media-badge--concept" : "media-badge--authentic";
      const badgeLabel = isConcept
        ? "Concept Preview"
        : cur.kind === "diagram"
        ? "System Diagram"
        : "Authentic Capture";

      const innerMedia =
        cur.type === "svg"
          ? `<div class="svg-stage-inline">${cur.svg}</div>`
          : `<img src="${esc(cur.src)}" alt="${esc(cur.caption)}">`;

      const thumbsHtml =
        visuals.length > 1
          ? `<div class="gallery-thumbs">
              ${visuals
                .map((v, i) => {
                  const activeCls = i === idx ? "is-active" : "";
                  const thumbInner =
                    v.type === "svg"
                      ? `<span style="font-size:11px;font-weight:700;padding:4px;display:flex;height:100%;align-items:center;justify-content:center;">Diagram</span>`
                      : `<img src="${esc(v.src)}" alt="Thumbnail ${i + 1}">`;
                  return `<button type="button" class="thumb-btn ${activeCls}" data-gallery-idx="${i}" aria-label="View visual ${i + 1}">${thumbInner}</button>`;
                })
                .join("")}
            </div>`
          : "";

      visualHtml = `
        <div class="gallery-main-stage">
          <button type="button" class="gallery-zoom-btn" data-open-lightbox="${idx}" aria-label="Open full-screen zoom view">
            ${innerMedia}
          </button>
          <span class="media-badge ${badgeClass}">${badgeLabel}</span>
          <span class="zoom-hint-pill">Click to Zoom</span>
        </div>
        <p class="gallery-caption">${esc(cur.caption)}</p>
        ${thumbsHtml}
      `;
    }

    let audioHtml = "";
    if (audios.length > 0) {
      audioHtml = `
        <div class="audio-players-block">
          ${audios
            .map(
              (a) => `
              <div class="audio-card">
                <span class="audio-card-label">${esc(a.caption || "Authentic Studio Audio Sample")}</span>
                <audio controls preload="metadata" src="${esc(a.src)}"></audio>
              </div>
            `
            )
            .join("")}
        </div>
      `;
    }

    if (!visualHtml && !audioHtml) return "";
    return `<div class="reader-gallery">${visualHtml}${audioHtml}</div>`;
  }

  function openEntryReader(entryId, updateHash = true) {
    const entry = (DATA.entries || []).find((e) => e.id === entryId);
    if (!entry) return;
    if (entry.visibility === "vault" && !state.vaultUnlocked) return;

    state.activeEntryId = entry.id;
    state.activeGalleryIndex = 0;

    const pillarObj = (DATA.pillars || []).find((p) => p.id === entry.pillar);
    const rMeta = READINESS_META[entry.readiness] || { label: entry.readiness };
    const tMeta = TYPE_META[entry.entry_type] || { short: entry.entry_type };

    readerCrumbs.innerHTML = `
      <span class="studio-pill">${esc(pillarObj ? pillarObj.short_title || pillarObj.title : entry.pillar)}</span>
      <span class="readiness-pill readiness--${esc(entry.readiness)}">${esc(rMeta.label)}</span>
      ${entry.visibility === "vault" ? `<span class="vault-pill">Private Vault</span>` : ""}
    `;

    const metricsHtml =
      entry.metrics && entry.metrics.length
        ? `<div class="reader-metrics-grid tabular-nums">
            ${entry.metrics
              .map(
                (m) => `
                <div class="reader-metric-box">
                  <span class="reader-metric-val">${esc(m.value)}</span>
                  <span class="reader-metric-lbl">${esc(m.label)}</span>
                </div>
              `
              )
              .join("")}
          </div>`
        : "";

    const ipo = entry.example_ipo || {};
    const hasIpoCards = ipo.input && ipo.process && ipo.output;
    const ipoCardsHtml = hasIpoCards
      ? `<div class="ipo-grid">
          <div class="ipo-step">
            <span class="ipo-step-label">1. Input</span>
            <div class="prose-block">${adaptHtmlForHostedWeb(ipo.input)}</div>
          </div>
          <div class="ipo-step">
            <span class="ipo-step-label">2. What Happens</span>
            <div class="prose-block">${adaptHtmlForHostedWeb(ipo.process)}</div>
          </div>
          <div class="ipo-step">
            <span class="ipo-step-label">3. Output</span>
            <div class="prose-block">${adaptHtmlForHostedWeb(ipo.output)}</div>
          </div>
        </div>`
      : "";

    const stackHtml =
      entry.tech_stack && entry.tech_stack.length
        ? `<div class="stack-chips">
            ${entry.tech_stack.map((s) => `<span class="stack-chip">${esc(s)}</span>`).join("")}
          </div>`
        : "";

    const visuals = getVisualItemsForEntry(entry);
    const svgIdx = visuals.findIndex((v) => v.type === "svg");
    const diagramBlockHtml = entry.diagram_svg
      ? `<div class="hood-diagram-card">
          <div class="hood-diagram-header">
            <strong>System &amp; Workflow Diagram</strong>
            <button type="button" class="ghost-btn" data-open-lightbox="${svgIdx >= 0 ? svgIdx : 0}">
              Zoom Diagram
            </button>
          </div>
          ${entry.diagram_svg}
        </div>`
      : "";

    const cmdsHtml =
      entry.run_commands && entry.run_commands.length
        ? `<div>
            <h3 style="font-size:0.875rem;margin-bottom:8px;">Launch &amp; Verification Commands</h3>
            <div class="cmd-list">
              ${entry.run_commands
                .map(
                  (c) => `
                  <div class="cmd-row">
                    <div class="cmd-info">
                      <span class="cmd-label">${esc(c.label)}</span>
                      <code class="cmd-code">${esc(c.command)}</code>
                    </div>
                    <button type="button" class="ghost-btn" data-copy-cmd="${esc(c.command)}">Copy</button>
                  </div>
                `
                )
                .join("")}
            </div>
          </div>`
        : "";

    const pathsHtml =
      entry.local_paths && entry.local_paths.length
        ? `<div>
            <h3 style="font-size:0.875rem;margin-bottom:8px;">Workspace &amp; Interactive Artifact Links</h3>
            <div class="path-list">
              ${entry.local_paths
                .map((lp) => {
                  const label = lp.label || "Local Path";
                  const rawHref = lp.path || "";
                  const cleanPath = rawHref.replace(/^file:\/\/\//i, "");
                  if (IS_HOSTED_WEB && /story_worlds_atlas\.html$/i.test(rawHref)) {
                    return `
                      <div class="path-row">
                        <a href="atlas.html" target="_blank" rel="noopener noreferrer"><strong>${esc(label)} (Live Web Atlas →)</strong></a>
                        <span class="path-mono">atlas.html</span>
                      </div>
                    `;
                  }
                  if (IS_HOSTED_WEB && /^file:\/\/\//i.test(rawHref)) {
                    return `
                      <div class="path-row">
                        <span><strong>${esc(label)}</strong> <code class="path-mono">${esc(cleanPath)}</code></span>
                        <button type="button" class="ghost-btn" data-copy-cmd="${esc(cleanPath)}">Copy Path</button>
                      </div>
                    `;
                  }
                  return `
                    <div class="path-row">
                      <a href="${esc(rawHref)}" target="_blank" rel="noopener noreferrer"><strong>${esc(label)}</strong></a>
                      <span class="path-mono">${esc(cleanPath)}</span>
                    </div>
                  `;
                })
                .join("")}
            </div>
          </div>`
        : "";

    const rawSec = entry.sections_html || {};
    const sec = {
      "What It Is & Why It Matters": adaptHtmlForHostedWeb(rawSec["What It Is & Why It Matters"]),
      "Real Example: How It Works in Practice": adaptHtmlForHostedWeb(rawSec["Real Example: How It Works in Practice"]),
      "Where It Stands & Next Steps": adaptHtmlForHostedWeb(rawSec["Where It Stands & Next Steps"]),
      "Under the Hood & Local Files": adaptHtmlForHostedWeb(rawSec["Under the Hood & Local Files"]),
    };

    readerBody.innerHTML = `
      <h2 id="readerTitle" class="reader-title">${esc(entry.title)}</h2>
      <p class="reader-subtitle">${esc(entry.subtitle)}</p>
      <div class="reader-meta-strip tabular-nums">
        <span>Type: <strong>${esc(tMeta.short)}</strong></span>
        <span>Started: <strong>${esc(entry.date_started)}</strong></span>
        <span>Updated: <strong>${esc(entry.date_updated)}</strong></span>
        <span>Memories Linked: <strong>${entry.memory_count || 0}</strong></span>
        <span>Sessions Consolidated: <strong>${entry.conversation_count || 0}</strong></span>
      </div>

      ${metricsHtml}
      <div id="readerGalleryMount">${renderGalleryStage(entry)}</div>

      <section class="reader-section">
        <h3 class="reader-section-title">What It Is &amp; Why It Matters</h3>
        <div class="prose-block">${sec["What It Is & Why It Matters"] || ""}</div>
      </section>

      <section class="reader-section">
        <h3 class="reader-section-title">Real Example: How It Works in Practice</h3>
        ${ipoCardsHtml}
        <div class="prose-block">${sec["Real Example: How It Works in Practice"] || ""}</div>
      </section>

      <section class="reader-section">
        <h3 class="reader-section-title">Where It Stands &amp; Next Steps</h3>
        <div class="prose-block">${sec["Where It Stands & Next Steps"] || ""}</div>
      </section>

      <details class="hood-drawer">
        <summary class="hood-summary">
          <span>Under the Hood &amp; Local Files</span>
          <span class="hood-chevron">Architecture, Diagram, Commands &amp; Paths ↓</span>
        </summary>
        <div class="hood-content">
          ${stackHtml}
          ${diagramBlockHtml}
          ${cmdsHtml}
          ${pathsHtml}
          <div class="prose-block">${sec["Under the Hood & Local Files"] || ""}</div>
          <div class="ledger-provenance tabular-nums">
            Source Markdown: <code>${esc(entry.doc_path)}</code> ·
            Indexed ${entry.memory_count || 0} LanceDB memory records &amp; ${entry.conversation_count || 0} top-level Antigravity sessions.
          </div>
        </div>
      </details>
    `;

    if (!readerDialog.open) {
      readerDialog.showModal();
    }
    readerBody.scrollTop = 0;

    if (updateHash) {
      history.replaceState(null, "", `#entry=${encodeURIComponent(entry.id)}`);
    }
  }

  function openLightbox(entry, startIndex) {
    const items = getVisualItemsForEntry(entry);
    if (!items.length) return;
    state.lightboxItems = items;
    state.lightboxIndex = Math.max(0, Math.min(startIndex, items.length - 1));
    updateLightboxStage();
    if (!lightboxDialog.open) {
      lightboxDialog.showModal();
    }
  }

  function updateLightboxStage() {
    const items = state.lightboxItems;
    if (!items.length) return;
    const cur = items[state.lightboxIndex];

    const isConcept = cur.kind === "concept";
    const badgeClass = isConcept ? "media-badge--concept" : "media-badge--authentic";
    const badgeText = isConcept
      ? "Concept Preview — AI-Generated Blueprint Illustration"
      : cur.kind === "diagram"
      ? "System Architecture Diagram"
      : "Authentic Capture";

    lightboxBadges.innerHTML = `<span class="readiness-pill ${badgeClass}" style="position:static;">${esc(badgeText)}</span>`;
    lightboxStage.innerHTML =
      cur.type === "svg"
        ? cur.svg
        : `<img src="${esc(cur.src)}" alt="${esc(cur.caption)}">`;
    lightboxCaption.textContent = cur.caption;
    lightboxCounter.textContent = `${state.lightboxIndex + 1} / ${items.length}`;

    const multi = items.length > 1;
    lightboxPrevBtn.hidden = !multi;
    lightboxNextBtn.hidden = !multi;
  }

  // ==========================================================================
  // Event Listeners & Initialization
  // ==========================================================================

  themeToggleBtn.addEventListener("click", toggleTheme);

  viewTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const nextView = tab.getAttribute("data-view");
      state.view = nextView;
      viewTabs.forEach((t) => {
        const active = t === tab;
        t.classList.toggle("is-active", active);
        t.setAttribute("aria-selected", active ? "true" : "false");
      });
      renderPortfolio();
    });
  });

  searchInput.addEventListener("input", () => {
    state.query = searchInput.value;
    clearSearchBtn.hidden = state.query.length === 0;
    renderPortfolio();
  });

  clearSearchBtn.addEventListener("click", () => {
    state.query = "";
    searchInput.value = "";
    clearSearchBtn.hidden = true;
    searchInput.focus();
    renderPortfolio();
  });

  // '/' shortcut to focus search when not typing in an input
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput && !readerDialog.open && !lightboxDialog.open) {
      const tag = (document.activeElement && document.activeElement.tagName) || "";
      if (tag !== "INPUT" && tag !== "TEXTAREA") {
        e.preventDefault();
        searchInput.focus();
      }
    }
    if (lightboxDialog.open && state.lightboxItems.length > 1) {
      if (e.key === "ArrowLeft") {
        state.lightboxIndex = (state.lightboxIndex - 1 + state.lightboxItems.length) % state.lightboxItems.length;
        updateLightboxStage();
      } else if (e.key === "ArrowRight") {
        state.lightboxIndex = (state.lightboxIndex + 1) % state.lightboxItems.length;
        updateLightboxStage();
      }
    }
  });

  // Delegated clicks inside main content
  document.getElementById("mainContent").addEventListener("click", (e) => {
    const openBtn = e.target.closest("[data-open-entry]");
    if (openBtn) {
      openEntryReader(openBtn.getAttribute("data-open-entry"));
      return;
    }
    const pillBtn = e.target.closest("[data-pillar-filter]");
    if (pillBtn) {
      state.pillarFilter = pillBtn.getAttribute("data-pillar-filter");
      renderPortfolio();
    }
  });

  // Delegated clicks inside Reader Drawer
  readerBody.addEventListener("click", (e) => {
    const entry = (DATA.entries || []).find((x) => x.id === state.activeEntryId);
    if (!entry) return;

    const thumbBtn = e.target.closest("[data-gallery-idx]");
    if (thumbBtn) {
      state.activeGalleryIndex = parseInt(thumbBtn.getAttribute("data-gallery-idx"), 10) || 0;
      const mount = document.getElementById("readerGalleryMount");
      if (mount) mount.innerHTML = renderGalleryStage(entry);
      return;
    }

    const zoomBtn = e.target.closest("[data-open-lightbox]");
    if (zoomBtn) {
      const idx = parseInt(zoomBtn.getAttribute("data-open-lightbox"), 10) || 0;
      openLightbox(entry, idx);
      return;
    }

    const copyCmdBtn = e.target.closest("[data-copy-cmd]");
    if (copyCmdBtn) {
      const cmd = copyCmdBtn.getAttribute("data-copy-cmd") || "";
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(cmd).then(() => {
          const orig = copyCmdBtn.textContent;
          copyCmdBtn.textContent = "Copied";
          setTimeout(() => { copyCmdBtn.textContent = orig; }, 1400);
        });
      }
    }
  });

  closeReaderBtn.addEventListener("click", () => readerDialog.close());
  readerDialog.addEventListener("close", () => {
    state.activeEntryId = null;
    if (window.location.hash.startsWith("#entry=")) {
      history.replaceState(null, "", window.location.pathname + window.location.search);
    }
  });

  copyLinkBtn.addEventListener("click", () => {
    if (!state.activeEntryId) return;
    const url = `${window.location.href.split("#")[0]}#entry=${encodeURIComponent(state.activeEntryId)}`;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(() => {
        const orig = copyLinkBtn.textContent;
        copyLinkBtn.textContent = "Link Copied";
        setTimeout(() => { copyLinkBtn.textContent = orig; }, 1400);
      });
    }
  });

  closeLightboxBtn.addEventListener("click", () => lightboxDialog.close());
  lightboxPrevBtn.addEventListener("click", () => {
    if (!state.lightboxItems.length) return;
    state.lightboxIndex = (state.lightboxIndex - 1 + state.lightboxItems.length) % state.lightboxItems.length;
    updateLightboxStage();
  });
  lightboxNextBtn.addEventListener("click", () => {
    if (!state.lightboxItems.length) return;
    state.lightboxIndex = (state.lightboxIndex + 1) % state.lightboxItems.length;
    updateLightboxStage();
  });

  // Private Vault Toggle (OFF on every page load)
  vaultToggleBtn.addEventListener("click", () => {
    state.vaultUnlocked = !state.vaultUnlocked;
    if (!state.vaultUnlocked && state.pillarFilter === "vault") {
      state.pillarFilter = "all";
    }
    if (!state.vaultUnlocked && readerDialog.open) {
      const curEntry = (DATA.entries || []).find((x) => x.id === state.activeEntryId);
      if (curEntry && curEntry.visibility === "vault") {
        readerDialog.close();
      }
    }
    renderPortfolio();
  });

  function checkHashRoute() {
    const hash = window.location.hash || "";
    if (hash.startsWith("#entry=")) {
      const slug = decodeURIComponent(hash.slice("#entry=".length));
      openEntryReader(slug, false);
    }
  }

  window.addEventListener("hashchange", checkHashRoute);

  // Boot
  attachDialogBackdropFallback(readerDialog);
  attachDialogBackdropFallback(lightboxDialog);
  syncThemeLabel();
  renderPortfolio();
  checkHashRoute();
})();
