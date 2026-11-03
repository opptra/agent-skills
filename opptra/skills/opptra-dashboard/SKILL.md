---
name: opptra-dashboard
description: >-
  Help users design and build internal dashboards and tools, hosted on Opptra
  Apps when that is genuinely the right fit. First gather requirements (who
  will use it, how many people, where the data lives), advise on the best
  technical approach in plain language (users are mostly non-technical), and
  build step by step in small usable slices rather than all at once. When
  Opptra Apps fits, build a single-file HTML dashboard that works in Claude
  preview and on Opptra (PREVIEW dual-mode, window.__OPPTRA__, proxy for
  secrets) with clear section banners and modular functional JavaScript.
  Nudge on maintenance/API costs where relevant. When the use case is too
  complex for this setup, recommend alternatives and suggest contacting
  ashish.mishra@opptra.com. Use opptra-design-system for visual styling.
  Do not create a GitHub app or run create-app.
---

# Opptra Dashboard Skill

Read `../opptra-design-system/SKILL.md` before writing styles. This is a
one-page tool, not a new repository.

## Phase 0 — Understand the requirement first (mandatory)

Do **not** jump straight into generating an HTML file. The people using this
skill are mostly **non-technical**; your first job is to be a good technical
advisor, not a code generator.

Before building anything:

1. **Restate the requirement** in one or two plain sentences so the user can
   confirm you understood it ("So you want a page where the team can see X
   and update Y — correct?").
2. **Gather the key attributes** — ask only the questions that change the
   design, and don't give advice or building steps until you have answers
   (or the user says "just assume"):
   - **Who** will use it — just the requester, their team, or the whole company?
   - **How many people**, roughly — 2, 20, 200? (changes how robust it must be)
   - **How often** — daily working tool, or occasional check-in?
   - **Where does the data live today?** (Google Sheet, another tool, nowhere yet)
   - Do users need to **change** data or just **see** it?
   - Roughly **how much data** — hundreds of rows or hundreds of thousands?
   - Does it need to **send emails, upload files, or talk to other systems**?
   - **Who will maintain it** after it's built — the requester, or nobody?

   Ask these conversationally, a few at a time — not as a form to fill in.
3. **Assess whether Opptra Apps is the right home** using the fit guide below.
4. **Tell the user your recommendation and why**, in plain language, before
   writing code. If Opptra is the wrong tool, say so honestly and suggest a
   better path — never force a requirement into Opptra just because this
   skill exists.
5. **Propose a step-by-step build plan** (see "Build in slices" below) instead
   of promising everything at once.

### What Opptra Apps actually is (so you can judge fit)

- Hosts **one single HTML file** per app (max 5 MB) behind company Google SSO.
- No server-side code of its own: all logic runs in the browser; data comes
  from Google Apps Script web apps, or vendor APIs called through Opptra's
  secret-keeping proxy (`/api/proxy/<connection>`).
- Non-secret settings are injected as `window.__OPPTRA__.config`; secrets stay
  server-side and are only used via the proxy.
- One URL per app (`/d/<slug>`). No sub-pages, no relative asset files, no
  zip/React/Vite builds, no database of its own.
- Publishing flow: upload → GitHub PR → merge → Mark live.

### Fit guide

**Good fit — recommend Opptra and build:**
- Internal dashboards: read and light-write views over Google Sheets
  (via Apps Script), vendor APIs (Freshdesk, etc.), or static/CSV data.
- Small team tools: trackers, review queues, calculators, report viewers,
  approval lists — where "one smart page" is enough.
- Anything where company-SSO access control and a shareable internal URL is
  the main hosting need.

**Workable with caveats — explain the trade-offs first:**
- Tools needing file upload → possible via Apps Script (base64 form POST to
  Drive), but slow for large files; say so.
- Tools with per-user saved preferences → possible via localStorage, but
  settings live per-browser, not per-account; say so.
- Heavier interactivity (kanban, schedulers) → fine while it fits comfortably
  in one file; warn that maintenance gets harder as the file grows.

**Poor fit — recommend an alternative, don't quietly build a degraded version:**
- Needs its own database, background jobs, or server-side logic.
- Needs real-time collaboration, websockets, or high data volume.
- Needs multiple pages/routes, its own login system, or external (non-company)
  users.
- Is really a product, not an internal tool.

For poor fits, name the better option in plain words (e.g. "this wants a real
web app with a database — Opptra hosts single pages, so it would fight you at
every step") and point them to escalation below.

**Never refuse to build.** Even for a poor fit, if the user understands the
limits and still wants an Opptra version, build the best honest subset —
often the first slice of their idea works fine on Opptra even when the full
vision doesn't. Your job is to guide, not gatekeep.

### Build in slices — never everything at once

Once fit is confirmed, break the requirement into **small technical cuts**
that each deliver something usable, and build them one at a time:

1. **Slice 1 — see the data.** A read-only view of their real data (from the
   Sheet, API, or pasted CSV). This alone is often 70% of the value and proves
   the data connection works.
2. **Slice 2 — act on the data.** The one or two most important write actions
   (update a status, add a row) — not every action they can imagine.
3. **Slice 3+ — extras.** Filters, charts, emails, file uploads, exports —
   added only after the earlier slices are live and actually used.

Rules for slicing:

- **Present the plan before building**: "First version shows X; once that
  works for you, we add Y" — and let the user reorder priorities.
- Each slice must be a **complete, uploadable dashboard** on its own — never
  ship half-wired buttons or "coming soon" placeholders.
- After each slice, tell the user to **upload and try it with real data**
  before requesting the next slice. Real usage changes priorities more than
  any planning conversation.
- If the user insists on everything at once, build it — but say plainly that
  going step by step would catch problems earlier and waste less of their time.

### Cost and maintenance nudges

Non-technical users rarely think about what a tool costs to keep alive.
Give small, honest nudges — not lectures — when relevant:

- **Maintenance effort**: "Every feature we add is something that can break
  later. This version needs someone to update the Apps Script if the Sheet
  columns change — usually a 5-minute fix, but someone has to own it."
- **Paid APIs**: if the tool calls a paid vendor API (per-request pricing,
  seat licences, AI/LLM calls), flag the rough cost driver: "Each refresh
  calls the API once per user — fine at 10 users, worth checking pricing
  at 200."
- **Quota limits**: Apps Script and free API tiers have daily quotas; heavy
  use by many users can hit them. Mention this when user count is high.
- **Growing complexity**: when a dashboard keeps gaining features, nudge:
  "This file is getting big — it still works, but changes now take longer
  and break more easily. Worth deciding what it really needs to do."

If cost or maintenance looks like a real concern rather than a nudge,
fold it into the escalation advice below.

### When to escalate

If the use case is complex, ambiguous after questioning, or keeps outgrowing
the single-file setup, tell the user:

> "This is getting beyond what a single Opptra dashboard handles well. For
> advice on the right setup, contact **ashish.mishra@opptra.com**."

Also suggest this contact when the user needs new proxy connections,
new secrets, permissions changes, or anything on the Opptra platform side
they cannot self-serve.

### Advising non-technical users

- Plain language first, jargon only when needed (and then explain it).
- Recommend the **simplest approach that will actually hold up** — sometimes
  that's "just use the Google Sheet directly" and no dashboard at all.
- One clear recommendation, not a menu of five options.
- Be upfront about limitations *before* building, not after.

---

## Phase 1 — Build (only after fit is confirmed)

Everything below applies once you and the user have agreed that an Opptra
single-file dashboard is the right approach.

## Branding

Read and follow **opptra-design-system** (`../opptra-design-system/SKILL.md`,
or https://opptra.github.io/opptra-design-system/SKILL.md) for colors,
typography, tokens, component families, and data states before inventing
dashboard styles.

- Apply those tokens inside the `<!-- === STYLES === -->` section.
- Do **not** skip the design system.
- Do **not** use `opptra-branding` for this HTML page. That skill is for
  decks, documents, emails, and charts.
- If the design-system files cannot be fetched, use the token names and
  values listed in `../opptra-design-system/SKILL.md` and say so.

## Rules

1. When building for Opptra, output **exactly one** `.html` file (no zip, no React/Vite project, no multi-file apps).
2. Use the **fixed section banners** below (same order, same labels) unless the user explicitly asks for a minimal one-pager.
3. Include a top-level `PREVIEW = { config, secrets }` object and dual-mode branching.
4. Put API keys / tokens **only** in `PREVIEW.secrets` — never scattered in the file.
5. Non-secret IDs/URLs go in `PREVIEW.config` (Drive folder id, Apps Script URL, domains, S3 links).
6. When `window.__OPPTRA__` exists (live on Opptra):
   - Read config from `window.__OPPTRA__.config`
   - Call secrets via `POST /api/proxy/<connection>` with `appId: window.__OPPTRA__.appId`
7. When `window.__OPPTRA__` is missing (Claude preview): use `PREVIEW` and call vendor APIs directly.
8. CDN libraries (Chart.js, etc.) are fine via `<script src="https://...">` in HEAD.
9. Live env values on Opptra are **per dashboard** in Postgres — not shared across modules.
10. Keep script code **modular and functional** (see Coding practices).
11. Follow **opptra-design-system** for visuals (see Branding above).

---

## Required file structure (strong default)

Use **one** `<style>` block and **one** main `<script>` block (plus optional CDN scripts in head).

Mark every section with these banners — **exact labels, this order**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- === HEAD / META === -->
  ...

  <!-- CDN scripts/styles if needed -->

  <!-- === STYLES === -->
  <style>...</style>
</head>
<body>
  <!-- === MARKUP === -->
  ...

  <script>
    /* === PREVIEW + CONFIG === */
    ...

    /* === DATA / API === */
    ...

    /* === RENDER / UI === */
    ...

    /* === INIT === */
    ...
  </script>
</body>
</html>
```

| Banner | What belongs here |
|--------|-------------------|
| `<!-- === HEAD / META === -->` | `charset`, `viewport`, `title`, optional description |
| CDN (optional, no banner required) | Chart.js, fonts, etc. |
| `<!-- === STYLES === -->` | All CSS for this dashboard — follow **opptra-design-system** |
| `<!-- === MARKUP === -->` | Semantic HTML: header, sections, empty states, containers with stable `id`s |
| `/* === PREVIEW + CONFIG === */` | `PREVIEW`, `ON_OPPTRA`, `config`, small pure helpers for reading settings |
| `/* === DATA / API === */` | `apiFetch`, loaders, parsers — **no DOM writes** |
| `/* === RENDER / UI === */` | Pure-ish render functions that take data → update DOM |
| `/* === INIT === */` | Wire events, call loaders, kick off the app |

**Minimal one-pager exception:** only if the user asks. Still keep `PREVIEW` + dual-mode; banners may be shortened but prefer keeping them.

---

## Coding practices (inside the single file)

### Modular + functional

- Prefer **small named functions** over one long script.
- **Separate concerns by section** (API vs render vs init) — do not fetch inside render helpers.
- Prefer **pure functions** where possible: `(input) => output` with no hidden DOM/globals.
- Use **`const` / `let`** — never `var`.
- Prefer **`async` / `await`** over raw `.then` chains.
- Avoid mutating shared state in place when a new object/array is clearer.
- Group related helpers under clear names (`loadTickets`, `normalizeTicket`, `renderTicketTable`).
- One responsibility per function; keep functions short enough to scan.

### DOM

- Stable element `id`s (e.g. `tickets-root`, `status-line`).
- Query once in INIT (`const el = document.getElementById(...)`) and pass elements into render fns, or re-query inside a dedicated `getEls()` helper.
- Show loading / empty / error states explicitly in MARKUP or render helpers.
- Keep zero, missing, stale, and restricted data distinct.

### Safety

- Never hardcode secrets outside `PREVIEW.secrets`.
- Escape or textContent-assign user/API strings when injecting into HTML (prefer `textContent` / `createElement` over raw `innerHTML` unless sanitized).
- Fail visibly: set an error message in the UI; do not fail silently.

### Accessibility (baseline)

- Real headings (`h1` → `h2`), labels on controls, buttons are `<button>`.
- Meaningful empty and error text for screen readers.

---

## Canonical template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- === HEAD / META === -->
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Opptra Dashboard</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:wght@300;600;700&family=Raleway:wght@400;500;600&display=swap" />

  <!-- === STYLES === -->
  <style>
    :root {
      --color-ink: #131A48;
      --color-text: #323642;
      --color-text-muted: #5A5A5A;
      --color-canvas: #FAFAF7;
      --color-surface: #FFFFFF;
      --color-border: #DDDEE4;
      --color-danger: #B42331;
      --font-heading: "Spectral", Georgia, serif;
      --font-body: "Raleway", "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: var(--font-body);
      background: var(--color-canvas);
      color: var(--color-text);
      line-height: 1.6;
    }
    h1 {
      font-family: var(--font-heading);
      color: var(--color-ink);
    }
    .wrap { max-width: 960px; margin: 0 auto; padding: 1.5rem; }
    .muted { color: var(--color-text-muted); font-size: 0.875rem; }
    .card {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: 0.75rem;
      padding: 1rem;
    }
    #status-line[data-state="error"] { color: var(--color-danger); }
  </style>
</head>
<body>
  <!-- === MARKUP === -->
  <div class="wrap">
    <header>
      <h1>My dashboard</h1>
      <p id="status-line" class="muted" data-state="loading">Loading…</p>
    </header>
    <section class="card" aria-label="Main content">
      <div id="main-root"></div>
    </section>
  </div>

  <script>
    /* === PREVIEW + CONFIG === */
    const PREVIEW = {
      config: {
        APPSCRIPT_URL: "https://script.google.com/macros/s/XXX/exec",
        FRESHDESK_DOMAIN: "acme.freshdesk.com",
      },
      secrets: {
        FRESHDESK_API_KEY: "preview-only-key",
      },
    };

    const ON_OPPTRA = Boolean(window.__OPPTRA__);
    const config = ON_OPPTRA ? window.__OPPTRA__.config : PREVIEW.config;

    function getSetting(key, fallback = "") {
      const value = config?.[key];
      return value == null || value === "" ? fallback : String(value);
    }

    /* === DATA / API === */
    async function apiFetch(connection, request) {
      if (ON_OPPTRA) {
        const res = await fetch("/api/proxy/" + connection, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-opptra-app-id": window.__OPPTRA__.appId,
          },
          body: JSON.stringify({
            appId: window.__OPPTRA__.appId,
            ...request,
          }),
        });
        if (!res.ok) {
          throw new Error("Proxy error " + res.status);
        }
        return res.json();
      }
      // Preview: implement vendor-specific call using PREVIEW.secrets
      throw new Error("Implement preview path for connection: " + connection);
    }

    async function loadDashboardData() {
      // Compose API calls here; return plain data objects only
      return {
        mode: ON_OPPTRA ? "opptra" : "preview",
        settings: { ...config },
      };
    }

    /* === RENDER / UI === */
    function setStatus(el, message, state) {
      el.textContent = message;
      el.dataset.state = state;
    }

    function renderMain(root, data) {
      root.replaceChildren();
      const pre = document.createElement("pre");
      pre.textContent = JSON.stringify(data, null, 2);
      root.appendChild(pre);
    }

    /* === INIT === */
    async function main() {
      const statusEl = document.getElementById("status-line");
      const root = document.getElementById("main-root");
      try {
        setStatus(statusEl, "Loading…", "loading");
        const data = await loadDashboardData();
        renderMain(root, data);
        setStatus(
          statusEl,
          data.mode === "opptra" ? "Live on Opptra" : "Claude preview",
          "ok",
        );
      } catch (err) {
        const message = err instanceof Error ? err.message : "Unknown error";
        setStatus(statusEl, message, "error");
      }
    }

    main();
  </script>
</body>
</html>
```

See `examples/sample-dashboard.html` for a fuller sample that follows the same layout.

---

## After Claude finishes

1. Download the HTML file.
2. Upload in Opptra → New dashboard.
3. Review Settings (auto-saved from PREVIEW).
4. Merge the GitHub PR, then Mark live.

Walk the user through these steps in plain language — assume they have never
merged a PR before. If anything in publishing, settings, or permissions is
unclear or blocked, direct them to **ashish.mishra@opptra.com**.
