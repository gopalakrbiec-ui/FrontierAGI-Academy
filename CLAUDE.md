# FrontierAGI Academy — Claude Agent Context

## Project Type
Static educational website. No framework, no backend — one small Python script (`scripts/build.py`, see below) keeps shared markup in sync.
All pages are plain HTML/CSS/JS served as files.

## File Structure
```
FrontierAGI-Academy/
├── index.html              ← Home page (stays in root, always) — AGI research/progress hub
├── styles.css              ← All CSS (single file)
├── app.js                  ← All JS (single file)
├── pages/                  ← All sub-pages live here
│   ├── blog.html
│   ├── frontier-model-learning.html  ← the interactive mode-based LLM course (formerly index.html)
│   ├── frontier-timeline.html
│   ├── future-frontier.html
│   ├── llm-engineering.html
│   ├── ai-news.html
│   ├── india-ai.html
│   ├── china-ai.html
│   └── usa-ai.html
├── blog/                   ← Blog posts + manifest
│   ├── index.json          ← Post manifest (source of truth for all blog UI)
│   ├── _template.html      ← Copy this to create a new post
│   └── [slug].html         ← Individual post files
└── docs/
    └── CONTRIBUTING.md     ← How to add pages and posts
```

**Note (Sep 2026 restructure):** `index.html` used to BE the interactive mode-based LLM course.
That entire experience moved to `pages/frontier-model-learning.html` unchanged, and `index.html` is
now a separate AGI-research/progress homepage (hero, latest blog signal, the 3 startup lanes, deep
investigations, researcher's path, explore links). The navbar's "Learning Mode" panel and every
`?mode=X` link across the site point at `pages/frontier-model-learning.html`, not `index.html`.

## Path Rules (critical)
| File location | styles.css | app.js | index.html (homepage) | frontier-model-learning.html | Other pages |
|---|---|---|---|---|---|
| `index.html` (root) | `styles.css` | `app.js` | — | `pages/frontier-model-learning.html` | `pages/foo.html` |
| `pages/*.html` | `../styles.css` | `../app.js` | `../index.html` | `frontier-model-learning.html` (same dir) | `foo.html` (same dir) |
| `blog/*.html` | `../styles.css` | `../app.js` | `../index.html` | `../pages/frontier-model-learning.html` | `../pages/foo.html` |

## Navbar Architecture
Two-ribbon fixed navbar:
- Ribbon 1 (`.navbar-brand`, 46px): indigo gradient, logo only
- Ribbon 2 (`.navbar-main`, 48px): white, 4 tab buttons + 1 direct link
- Total navbar height: **94px** — all pages set `padding-top: 94px` on first element after nav

Nav tabs open slide-down panels (`.nav-panel`) — NOT CSS hover dropdowns.
Panel JS lives in `app.js`: `initNavPanels()`, `closeAllNavPanels()`.
Backdrop (`#navBackdrop`) closes panels on click.

### Nav panels inserted after `</nav>` in every HTML file:
```html
<div class="nav-backdrop" id="navBackdrop"></div>
<div class="nav-panel-wrap" id="navPanelWrap">
  <div class="nav-panel" id="navPanel-mode">...</div>
  <div class="nav-panel" id="navPanel-explore">...</div>
  <div class="nav-panel" id="navPanel-ecosystems">...</div>
  <div class="nav-panel" id="navPanel-blog">...</div>
</div>
```

## Learning Modes
8 modes: layman, graduate, researcher, team, startup, investor, founder, agentmode.
- Live on `pages/frontier-model-learning.html`: mode buttons use `onclick="setMode('mode')"` with `id="modeBtn_mode"`
- Everywhere else, mode links point AT that file: `href="../pages/frontier-model-learning.html?mode=X"` (from `blog/*.html`) or `href="frontier-model-learning.html?mode=X"` (from `pages/*.html`)
- Mode state persisted via `sessionStorage('llm-mode')`
- URL param `?mode=X` read on load in `app.js`

## Blog System
- Manifest: `blog/index.json` — add entry here to publish a post
- Template: `blog/_template.html` — copy and fill in
- Nav Recent Posts: `loadBlogNavPosts()` in `app.js` — reads manifest, populates `#blogNavMenu`
- Blog listing page: `pages/blog.html` — reads manifest, renders cards

### blog/index.json schema:
```json
{
  "slug": "post-slug",
  "title": "Post Title",
  "excerpt": "One-two sentence summary.",
  "author": "Author Name",
  "authorInitials": "AN",
  "date": "2026-06-22",
  "readTime": "5 min",
  "tags": ["Tag1", "Tag2"],
  "emoji": "🧠",
  "featured": false
}
```
Only one post should have `"featured": true` at a time.

### Article sidebar ("On this page")
`initArticleSidebarNav()` in `app.js` turns an article's section nav (`.agi-section-nav`, any `*-section-nav`, `.fde-nav`, `.sk-nav`, `.sb-nav`, `.phase-nav`, `.fr-toc`) into a sticky left sidebar with active-section highlight; articles with none get one built from 4+ `h2` headings. The wrap widens to 1040px on wide screens so the text column keeps its width. Keep a section-nav row near the top of new articles.

## CSS Conventions
- All CSS in `styles.css` — append new sections at the bottom with a banner comment
- CSS variables in `:root`: `--accent`, `--accent2`, `--accent3`, `--text`, `--border`, `--bg-card`, etc.
- Light theme only (no dark mode toggle)
- Mobile breakpoint at `768px`

## Adding a New Page
1. Copy an existing page from `pages/` as your template
2. Place the new file in `pages/`
3. If it belongs in the nav, edit `partials/nav.html` (never the generated block inside pages), then run `python3 scripts/build.py`
4. Paths: use `../styles.css`, `../app.js`, `../index.html` at top

## Build Step (`scripts/build.py`)
Still no framework — one Python script keeps shared markup in sync. Run it after ANY change (new post, manifest edit, nav edit):
```bash
python3 scripts/build.py          # rewrites generated blocks, sitemap.xml, robots.txt, 404.html, README table
python3 scripts/build.py --check  # what CI runs: fails if anything is stale or an internal link/anchor is broken
```
- Nav source of truth: `partials/nav.html` (`{{ROOT}}`/`{{PAGES}}`/`{{BLOG}}` path prefixes, `{{ACTIVE_x}}` tab markers). Pages hold it between `<!-- NAV:START -->`/`<!-- NAV:END -->` — never hand-edit that block.
- SEO block (`<!-- SEO:START -->…<!-- SEO:END -->`) after `<title>`: description, canonical, Open Graph, Twitter card. Blog posts take title/excerpt/date from `blog/index.json`; other pages use their first intro paragraph.
- Social preview image: `assets/og-default.png`.
- Series footer (`<!-- SERIES:START -->…<!-- SERIES:END -->`, before `</main>` in every post): prev/next links. A series = one homepage spotlight grid, in card order, so adding a card to the right grid on `index.html` is all it takes — build.py picks it up.
- `blog/series.json` (generated): every series with its short label, icon and ordered slugs. `pages/blog.html` builds its sidebar categories and card labels from it. Manifest `tags` are no longer used for navigation.
- Homepage "· N Articles" counts on spotlight tags are kept in sync automatically.
- `pages/idea-map.html`: the 3D "AI Idea Map" (dependency-free canvas renderer; reachable from the nav and the "See it in 3D" button, no longer on the homepage). Its data `blog/idea-graph.json` is generated by build.py from every `ar-card` in `blog/ai-research-*-papers.html` plus the hand-curated `data/idea-map.json` (research area per card, lineage links `[from, to, kind?]`, short labels, guided tours, and `core`: the ~120 key ideas shown by `idea-map.html?view=core`, the 3D map's `?embed=1` mode, and the default view of `idea-flow.html`). When a new "AI Research in YEAR" article is added, give each new card an area in `nodeArea` and at least one link — `--check` fails on unknown or unassigned cards.
- `pages/idea-flow.html` ("AI Idea Flow"): vertical SVG metro map, 2026 at the top down to 1950 (time flows upward) — one column per research area, one bubble per paper card (radius = number of cards built directly on it), curved flows origin → target, canvas particle streams down each line, interchange rings where parents come from 2+ areas, and a click-to-open family tree (bottom sheet on phones; phones default to 3 lines with a pick-up-to-3 chooser). `idea-flow.html?embed=1` is a chrome-free mode used by the homepage iframe in the AI Research Progress section. It reads the same `blog/idea-graph.json` as the 3D map (default view = all cards; the "Key ideas" toggle shows the `core` list bridged), so there is no extra data to maintain.
- `pages/lab-updates.html` ("Frontier Lab Updates"): every release/announcement from 13 frontier labs, Oct 2021 → Oct 2026, newest first. Source of truth: `data/lab-updates.json` (`labs`, `types`, `items` with `date` as `YYYY-MM-DD` or `YYYY-MM`, `lab`, `type`, `title`, `summary`, `facts`, `source`, `flagship`). build.py renders the cards into the page (`<!-- LABITEMS -->`), plus the homepage ticker strip (`<!-- LABSTRIP -->`, inside the hero) and the "Latest from the Labs" section (`<!-- LABLATEST -->`). To add an announcement: add one item with an https source, then run the build; `--check` rejects unknown labs/types, bad or out-of-range dates, missing sources and duplicate ids.
- `pages/rsi-evolution.html` ("RSI Evolution Map"): loop-anatomy explorer + three views (autonomy staircase L1–L5, "what gets rewritten" by 10 object families, research-vs-industry timeline). Data `data/rsi-papers.json` (524 papers, 14 industry cases) is generated by `python3 scripts/import_awesome_rsi.py` from the CC0 Awesome-RSI catalog (theseus-labs-rsi/awesome-rsi, survey arXiv:2609.11873) — keep the attribution box; `build.py --check` runs `validate_rsi()` on it. Post-cutoff months undercount because of the catalog's screening; industry figures are organisation-reported. `data/rsi-supplement.json` holds site-added papers (~70) for Jun–Oct 2026 that are NOT in the catalog: provisional level/family classified from titles, drawn as dashed dots with a "Site additions" toggle; entries are ignored automatically once the catalog covers the same arXiv id. `validate_rsi_supplement()` checks the structure. Keep the "provisional" labelling.
- **Paper discovery (weekly, `.github/workflows/discover-papers.yml`):** `scripts/discover_rsi_candidates.py` searches arXiv (CC0 metadata) for RSI-style papers missing from the catalog and supplement and writes `data/rsi-candidates.json` — CANDIDATES ONLY, no level/family; review them and move accepted ones into `data/rsi-supplement.json` with a rationale. `scripts/enrich_citations.py` writes OpenAlex citation counts to `data/paper-impact.json`; when that file exists the RSI map's pulsing rings mean "most cited" (papers under ~3 months old are not ranked) and the panel shows the count, otherwise it falls back to the in-catalog proxy. Both scripts need network access the authoring sandbox lacks (they have `--selftest`); the API response shapes were written untested against the live services, so check the first workflow run. OpenReview/conference flags and Hacker News votes were deliberately not added yet.
- `pages/model-releases.html` ("Model Release Map"): foundation / image / video / speech model releases across labs, Jun 2017 (the Transformer) → 13 Oct 2026. Pre-2022 rows have no `ref` (lab-updates starts Oct 2021). Three views: lab lanes (time vertical, lines join a model to the next in its family), open-vs-closed (first closed vs first open-weight release per capability tier, within this dataset) and cadence. Source of truth: `data/model-releases.json` (hand-curated; LLM rows carry `ref` = a verified id in `data/lab-updates.json`; `open` 1/2/0/null, `st` ga/preview/research, `sec` 1 = secondary source, `t` = tier milestone, `end` = retired date). Class prefix is `mx-` (`mr-` is taken in styles.css). `build.py --check` runs `validate_models()`. To add a release: append an item with an https source (mark `sec:1` if it is not the lab's own page), then run the build.
- `pages/hf-paper-themes.html` ("HF Paper Themes"): monthly top papers from Hugging Face Daily Papers grouped by theme (streams, month × theme heatmap, month bubbles with pulsing rings for the top 3). Data `data/hf-papers.json` is generated by `python3 scripts/import_hf_papers.py` (needs huggingface.co access; `--dump-dir` reads saved API JSON offline; `--relabel` re-runs the keyword theme rules in `THEMES`). Stores ids, titles, upvote/comment counts and our theme labels only. The page shows an empty state until the file exists, and is in the Explore nav (not on the homepage yet); the importer skips the current month unless `--include-current` (workflow input `include_current`; then it is flagged in `partial` and shown as in progress) and never saves a month with failed days (use --resume after rate limiting). `build.py --check` runs `validate_hf()`. Class prefix `hf-`.
- **Automation:** `.github/workflows/refresh-data-daily.yml` refreshes `data/hf-papers.json` (current month as in progress) and `data/rsi-papers.json` daily and commits them; failures open/comment on a `data-refresh` issue. `refresh-hf-papers.yml` is the manual full backfill. Scheduled workflows only run on the default branch. `data/model-releases.json` and `data/lab-updates.json` are hand-checked: a weekly Claude routine drafts updates as a pull request for review (never edit them from a script without sources).
- **AI Compute Stack series** (homepage `#grp-compute`, spotlight `sec-compute`, first block of the "01 · Build the Machine" section `#grp-build`, after "00 · Follow the Frontier"): power → private energy → factory → vs supercomputers → cooling & water → chips → supply chain → interconnect → memory → custom silicon → inference → edge devices → token prices → financing → China → space → pricing → beyond silicon (future of AI compute). New compute articles go in this grid (card order = series order); related posts owned by other series are linked under the spotlight, not carded. `pages/compute-stack.html` ("AI Compute Stack at a Glance", Explore nav, linked from the spotlight and Start Here) is the series hub: its layer data (headline number, bottleneck, ratings) is one JS array `L` taken from the articles — update it when a part is added or its headline figure changes.
- **Producing Intelligence series** (homepage `#grp-production`, spotlight `sec-production`, second block of "01 · Build the Machine", right after the AI Compute Stack): the next layer up, following Meta's Llama 3 405B end to end through one AI factory. Parts: software stack → data → planning the run → parallelism → running the run → post-training → evaluation → serving → operations, all nine published (Oct 2026). Hub: `pages/producing-intelligence.html` ("Producing Intelligence at a Glance", Explore nav, linked from the spotlight and Start Here); its stage data is one JS array `P` (slug, part, emoji, title, group, number, label, decision, risk, tools) — update it when a part changes. Badge text "Producing Intelligence · Part N"; each article carries a Llama 3 case-file box. Avoid repeating the existing how-llm-* explainers and frontier-lab-engineering posts; link to them.
- **Who Runs the AI Factory series** (homepage `#grp-whoruns`, spotlight `sec-whoruns`, third block of "01 · Build the Machine"): the AI factory software stack layer by layer through the role that owns it. All 12 parts published (Oct 2026). Hub: `pages/who-runs-the-ai-factory.html` ("Who Runs the AI Factory at a Glance", Explore nav, linked from the spotlight and Start Here); its layer data is one JS array `W` (slug, part, emoji, layer, group, role, owns, tools, failure, fact, handoff parts) plus `SV` skill ratings and `PO` postings — update them when a part changes. Parts: bring-up & firmware → OS & runtime → networking → storage → scheduling → kernels & compilers → training frameworks → data platform → experiment tooling → inference → observability & on-call → security. Badge "Who Runs the AI Factory · Part N"; every part has the stack map (Part N highlighted), role, tools, failure stories, handoffs and a career box. Meta is the main example; role descriptions must be grounded in real job postings or engineering talks. Link to Producing Intelligence and the Frontier Lab Engineering practicum instead of repeating them.
- **AI Factory Case Studies series** (homepage `#grp-cases`, spotlight `sec-cases`, fourth block of "01 · Build the Machine"): "Inside the Gigawatt Club", 10 parts (Oct 2026): Colossus → Stargate Abilene → Fairwater → Project Rainier → Meta Prometheus & Hyperion → Google TPU fleet → CoreWeave & neoclouds → China → sovereign projects → the bets compared. Class prefix `cs-` (reuses `wr-` base styles). Every part has the same case file, a 4-lane build timeline (`TL` array: confirmed / press / ⚠️ unverified / planned dots, calendar vs days toggle, vertical list on phones), "the bet", comparison table and "Reading the numbers". Hub: `pages/ai-factories.html` ("AI Factories at a Glance", Explore nav, linked from the spotlight and Start Here); its site data is one JS array `F` (plus map points `P` and timeline `T`) — update it when a part changes or a site's estimate moves. Disclose that Claude helps write the site when discussing Anthropic/Amazon/Google.
- **AI Factory as a Service series** (homepage `#grp-managed`, spotlight `sec-managed`, fifth block of "01 · Build the Machine"): how everyone outside Big Tech gets AI factories. 6 parts (Oct 2026): four routes (build/install/buy/rent) → hyperscalers on-premises (AWS AI Factories, Microsoft sovereign private cloud, Google Distributed Cloud, Oracle Dedicated Region) → NVIDIA's DSX blueprint & DSX Pod → hardware vendors (Dell, HPE, Supermicro, Lenovo) → customers by sector → economics (editable cost-per-useful-GPU-hour calculator, break-even curve, scorecard). Class prefix `ms-` on top of `cs-`/`wr-`. Part 1 holds the series map (`SER`). Hub: `pages/ai-factory-service.html` ("AI Factory as a Service at a Glance", Explore nav, linked from the spotlight and Start Here): arrays `RT` (routes), `PV` (providers), `CU` (customers with lat/lon), quiz `QS`, timeline `TLD` — update when a part changes. Label vendor claims (customer counts, ROI, build times) as such; the calculator is our own model. Bonus article (last card in the grid): `frontier-lab-startup-playbook` — training budget builder (6ND, MFU), serving/agent cost and runway calculators, India/Bangalore section (IndiaAI compute, ₹ prices at an assumed ₹88/$, RDI fund, Karnataka policy).
- **Inside the ML Layer series** (homepage `#grp-mllayer`, spotlight `sec-mllayer`, sixth block of "01 · Build the Machine", layer label "🧠 The ML Layer"): the AI factory's ML software component by component — map → frameworks → parallelism → kernels → post-training & RL → eval → inference engines → agent runtimes (8 parts planned). Class prefix `ml-`. Part 1 (`ml-layer-map`) holds the layer array `L`, lab × layer matrix `MX` and series map `SER`. Go deeper than Who Runs the AI Factory (roles) and link to it. A sibling "Inside the Data Layer" series (🗃️ The Data Layer) is planned as the seventh block.
- **Latest from the Academy** (homepage, right after the hero, `<!-- LATEST:START -->`): build.py renders the 8 newest posts from `blog/index.json` (by date, then manifest order), each with a dot trail of its series from `blog/series.json`. `app.js` records article visits in localStorage (`fa-read`) and fills the personal panel (new since last visit, continue your thread, reading trail) — browser-only, no server. `pages/threads.html` (Explore nav) shows every series as a metro line plus a month-by-month publishing history; note most posts are dated Sep 2026 (archive migration).
- `pages/start-here.html`: hand-curated reading tracks (new to AI / research / building). Update when a better entry point is published.

## Git Branch
Active development branch: `claude/trusting-mendel-u9s1oh`
Remote: `gopalakrbiec-ui/Claude_Project_3_LLM` (also mirrors to `gopalakrbiec-ui/FrontierAGI-Academy`)
