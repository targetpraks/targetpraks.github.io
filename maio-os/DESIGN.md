# Design System: Maio OS

<!-- Generated from the shipped v5 section-workspace code (index.html, assets/theme.css,
     assets/workspace.css, assets/icons.svg) following the Google Stitch DESIGN.md format.
     Tokens are normative; prose explains how to apply them. -->

---
name: Maio OS
description: The household cockpit — projects, agents, documents, and machine vitals in one light workspace.
colors:
  paper: "#F7F4EC"
  surface-window: "#FDFBF5"
  surface-card: "#FFFFFF"
  surface-sunken: "#F1ECDF"
  line-hairline: "#E6DFD2"
  line-strong: "#D9D0BE"
  ink: "#23262E"
  text-body: "#444B5A"
  text-dim: "#565E6C"
  text-dim2: "#616A78"
  gold-text: "#82650F"
  gold-edge: "#9A7B10"
  gold-brand: "#C9A227"
  gold-soft: "#FBF5E3"
  status-ok: "#127248"
  status-warn: "#8A5807"
  status-bad: "#B02A2A"
  accent-cyan-ink: "#096E7B"
  accent-magenta-ink: "#C2184F"
typography:
  display:
    fontFamily: "'Avenir Next','Segoe UI',system-ui,-apple-system,'Helvetica Neue',sans-serif"
    fontSize: "32px (29px ≤760px)"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-1px"
  headline:
    fontFamily: "'Avenir Next','Segoe UI',system-ui,sans-serif"
    fontSize: "17px (16px ≤760px)"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.3px"
  title:
    fontFamily: "'Avenir Next','Segoe UI',system-ui,sans-serif"
    fontSize: "14–15px"
    fontWeight: 600
    lineHeight: 1.35
  body:
    fontFamily: "system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
    fontSize: "13–14px"
    fontWeight: 400
    lineHeight: "1.55–1.8"
  label:
    fontFamily: "system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif"
    fontSize: "11px minimum, 12px preferred"
    fontWeight: "500–650"
    letterSpacing: "uppercase group titles 0.8–1.3px"
  mono:
    fontFamily: "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
    fontSize: "0.72rem floor"
rounded:
  xs: "7px"
  sm: "10px (workspace components flatten to 8px/5px/6px)"
  md: "14px"
  lg: "18px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "14px"
  lg: "28px"
  xl: "36px"
  section-gap: "36px between overview sections"
components:
  button-primary:
    backgroundColor: "{colors.gold-brand}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "9px 15px"
  button-secondary:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "6px 10px"
  card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.text-body}"
    rounded: "8px"
    padding: "18–20px"
  input-search:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "6px"
    height: "44px"
---

## Overview

**Creative North Star: "The Daylight Desk"**

Maio OS reads like a tidy paper desk in afternoon light: warm paper surfaces, one muted-gold
accent, chunky-but-soft outlines, and content that sits directly on the page. There is no
desktop metaphor anywhere in the interface — no floating windows, no pop-up search, no
dock. Every kind of work has a fixed section; a record opens in the main content area with
a breadcrumb back to its parent. Navigation is persistent (sidebar on desktop, attached nav
row on phones) and never floats above content.

Density is generous rather than squeezed: rows breathe (78px project rows, 17px section
paddings), everything is ≥11px, and the whole page fits inside the viewport shell (the
shell scrolls, chrome does not). Snapshot data and live data must stay visually
distinguishable; gaps render as honest empty states, never invented content.

**Key Characteristics:**
- Warm paper `#F7F4EC` with gold `#C9A227` as the only strong accent (text-safe gold `#82650F` for text).
- System font stacks only; zero external requests; one local CSS file + one SVG sprite.
- Single gold focus outline; no cyan halo on headings or page titles.
- Fixed section workspace with bookmarkable routes (`#overview`, `#projects`, `#project:…`, `#agent:…`, `#file:…`, `#desk` remains an alias of Overview).
- Status colour is data, not decoration: green/amber/red pills and dots reflect real probe results.

## Colors

The palette is warm neutral paper with a single muted-gold accent; status colours are
darkened past AA on every surface they can land on.

### Primary
- **Brand Gold** (`#C9A227`, graphic): fills, meter ink, the logo accent, selected-state tint. Never body text.
- **Text-Safe Gold** (`#82650F`): the accent when it carries text — links, selected nav, chip labels (5.0:1 on paper).
- **Gold Edge** (`#9A7B10`): borders and focus/hover edges (3.7:1, graphic only).

### Secondary (small doses only)
- **Cyan Ink** (`#096E7B`): read-only badge text; the retired cyan halo no longer appears on focus.
- **Magenta Ink** (`#C2184F`): vault badge text on soft magenta.

### Tertiary (status)
- **OK Green** (`#127248`): healthy services, "fresh" data stamp.
- **Warn Amber** (`#8A5807`): "check" states, stale snapshot notes.
- **Bad Red** (`#B02A2A`): down services, failed actions.

### Neutral
- **Paper** (`#F7F4EC`): page background.
- **Window** (`#FDFBF5`): window/panel body one step up.
- **Card** (`#FFFFFF`): cards, inputs, bars.
- **Sunken** (`#F1ECDF`): hover fills, monogram avatars, meter tracks.
- **Hairline** (`#E6DFD2`) / **Strong Line** (`#D9D0BE`): separators and outlines.
- **Ink** (`#23262E`): headings and primary text (13.8:1).
- **Body** (`#444B5A`): paragraph text (7.9:1).
- **Dim / Dim2** (`#565E6C` / `#616A78`): metadata, captions (≥5.0:1).

### Named Rules
**The One Gold Rule.** Gold appears once per glance: the selected nav row, the primary
button, or the focused action — never several competing gold fills on one screen.

## Typography

**Display Font:** Avenir Next → Segoe UI → system-ui (brand + headings)
**Body Font:** system-ui → -apple-system → Segoe UI → Roboto (body, labels, controls)
**Label/Mono Font:** SF Mono → Menlo → Consolas (paths, pids, machine metadata)

**Character:** Humanist system sans throughout; the mono voice is reserved for machine
truth (file paths, ports, pids) so it never competes with prose.

### Hierarchy
- **Display** (600, 32px, 1.2, −1px): the page title of each section. 29px ≤760px.
- **Headline** (600, 17px, −0.3px): overview card headings and section h2s.
- **Title** (600, 14px): card/row titles (project names, agent names).
- **Body** (400, 13–14px, 1.55–1.8): paragraphs, row copy, descriptions.
- **Label** (500–650, 11px floor / 12px preferred): nav metadata, badges, source notes; uppercase 11px for nav group titles (Workspace / Work / Knowledge / System).

### Named Rules
**The 11px Floor Rule.** No operational text below 11px; mono metadata sits at 0.72rem.
Keyboard hints like `⌘ K` stay text at 11px.

## Layout

A two-column shell grid: persistent sidebar (228px; 198px ≤1150px) + main shell. The main
shell is a fixed-height flex column — topbar (min 68px), then the scrolling workspace
(`#workspace` is the only scroller). Content is capped at 1400px and centred; generous
padding (38px 36px, tighter steps at 1150/760px).

- **Overview:** 12-col feel via `grid-template-columns: 1fr 285px` (310px ≥1600px, 240px ≤1150px, single column ≤950px with the summary rail becoming a 2-up grid).
- **Content sections:** card grids (auto-fill, min 250–280px), library grid ≥270px.
- **≤760px (phones):** the app becomes a column. The sidebar becomes the attached nav:
  brand on its own line, then a single snap-scrolling chip rail of all 13 sections
  (groups dissolved, titles hidden, 44px chips, 18px edge fade, current chip scrolled
  into view). The rail stays above the scrolling content and never widens the document.
  Safe-area insets respected; every control ≥44px.
- **Folded apps:** Wheel of Life and Top 8 render as full-height frames (`/wheel`,
  `/top8/`) **only on the companion origin**; elsewhere they show the honest
  "lives on the local companion" note. Same gate covers `local.js`, `/api/fix*` and vault
  reads — see *Section model* below.
- **Rhythm:** 36px between overview sections, 32px page-heading margin, 14px card gaps.

## Section model and routes

| Route | Section | Group | Data |
|---|---|---|---|
| `#overview` (and `#desk`) | Overview | Workspace | snapshot + live mix |
| `#search` | Search | Workspace | index built from all sections |
| `#projects` / `#project:<name>[@n]` | Projects → detail | Work | snapshot |
| `#kanban` | Kanban | Work | companion live, snapshot fallback |
| `#agents` / `#agent:<name>` | Agents → detail | Work | snapshot |
| `#reports` / `#report:<q>` / `#docs:<q>` | Library (Machine/Public/Docs) | Knowledge | snapshot + companion |
| `#prds` | PRDs | Knowledge | snapshot |
| `#vault` | Vault | Knowledge | companion only (read-only) |
| `#machine` | Machine | System | companion only |
| `#stack` | Stack | System | snapshot probes + companion actions |
| `#wheel` | Wheel of Life | Life | companion only |
| `#top8` | Top 8 | Life | companion only |
| `#about` | About | System | static |
| `#file:<rel>` | File reader | Knowledge | companion only |

`detail` and `file` are the shell's two reused views (never addressable without a subject).
Unknown or malformed fragments fall back to Overview. Every route is bookmarkable and
participates in ordinary Back/Forward history.

## Elevation & Depth

Flat-by-default with a whisper of ambient shadow; hierarchy comes from outlines and
tonal steps, not floating geometry. Cards rest on paper with a hairline border and at
most `--shadow-1` (`0 1px 2px / 0 2px 8px` at 5% ink). Depth only appears as a response:
hover lifts a card one tonal step (`#FCFBF7`) and gold-warms its border; panel chrome
(boot, topbar) carries soft `--shadow-2`. No drop shadows under text or rows.

### Shadow Vocabulary
- **Ambient-low** (`--shadow-1: 0 1px 2px rgba(35,38,46,.05), 0 2px 8px rgba(35,38,46,.05)`): resting cards, buttons.
- **Lift** (`--shadow-2: 0 6px 18px rgba(35,38,46,.08), …`): hover/panel chrome only.

### Named Rules
**The No-Floating-Windows Rule.** Nothing floats above the page: no window chrome, no
pop-up search, no overlay panes. Search is a section; details open in the main content
area. (The `.win` / `.dockbtn` / `.desklet` rules survive in `theme.css` only because
`assets/preview.html`, the kit QA sheet, renders them as specimens — no page in the
workspace uses them. The retired page-chrome ids `#dock`, `#scroller`, `.menubtn`,
`#cmdbar*` and `#vitals` are gone.)

## Shapes

Chunky-warm rounding at small scale: controls 5–7px, cards 8–10px, panels 14–18px, chips
and badges fully pill-shaped. Outlines are a consistent 1px hairline (`#E6DFD2`) with a
stronger 1.5px (`--hair`, `#D9D0BE`) on inputs and buttons. Rows separate by hairlines,
not boxes; the workspace reads as lists on paper. Icons use the local 24px sprite
(`assets/icons.svg#i-*`, 1.75 stroke, round caps) — decorative arrows/detail marks are
sprite symbols (`i-arrow-right`, `i-arrow-up-right`, `i-copy`), never Unicode glyphs.

## Components

### Buttons
- **Shape:** rounded rect (5px in the workspace kit; 10px in the theme kit), 1.5px border, 34–44px min height.
- **Primary:** gold gradient `#DFBC4C→#C9A227`, ink text, pressed state drops 2px.
- **Secondary/ghost:** white on hairline (hover warms to gold-soft); ghost is borderless text.
- **Danger:** white/red-outline at rest, solid red fill on hover (e.g. Trim RAM confirm path).
- **Focus:** 2px gold outline, 2px offset; no halo.
- **Small (`btn.sm`, `.copy`, `.obtn`):** 11px mono/sans, 34px min height, icon via sprite.

### Chips
- **Style:** pill radius (5px in workspace kit), white/tinted surface, hairline border, 12px label.
- **State:** `on` = gold-soft background, gold text, gold edge (Library shelves, project family filters).

### Cards / Containers
- **Corner Style:** 8px.
- **Background:** white on paper.
- **Shadow Strategy:** none at rest in the workspace kit (flat tonal layering); hover shows
  a gold-warmed border and one-step lift; theme-kit cards keep `--shadow-1`.
- **Border:** 1px hairline.
- **Internal Padding:** 18–20px; rows 13–17px vertical.

### Inputs / Fields
- **Style:** white, 1.5px strong-line border, 6px radius, 44px min height, 13px text.
- **Focus:** gold edge + soft gold ring (`--ring-gold`), no cyan halo.
- **Filter variant:** same box inside sections; label via aria from placeholder.

### Navigation
- **Desktop sidebar:** brand mark, caption, grouped links (sprite icon + 13px label +
  count), warm-neutral surface, selected = gold-tinted row with deep-gold text.
- **Topbar:** breadcrumbs (group / current) left, snapshot stamp + search button (with
  `⌘ K` kbd hint) right.
- **Phones (≤760px):** one attached chip rail (~125px tall, 15% of a 390×844 screen).
  Groups dissolve (`display:contents`), group titles hide, and all 13 sections become
  44px chips in a single horizontally snap-scrolling row with an 18px edge fade. The
  current chip is scrolled into view on every route change, the fade is dropped while the
  rail holds focus, and the rail's 5px vertical padding keeps every 2px focus ring whole.
  The rail never widens the document (measured 0px overflow); counts hide.
- **Breadcrumbs:** current page in ink; parent is a gold link; slash separators in hairline tone.

### Status primitives (signature)
- **Pills/dots:** green/amber/red from real probe/state data; the snapshot stamp
  (`#genned`) shows "Snapshot · <age>" or "Live local data" so provenance is always visible.
- **Notes:** gold notebox (info) / amber warnbox (warnings), 12–13px.
- **Empty states:** dim text on plain background, always honest ("No projects have been
  indexed yet."), never padded with invented records.

## Do's and Don'ts

### Do:
- **Do** keep zero external requests: system font stacks, local `theme.css` +
  `workspace.css`, one local SVG sprite for all icons.
- **Do** keep the 11px type floor (12px preferred for operational labels) and re-check
  density at 390px after size changes.
- **Do** keep a strong gold focus outline everywhere; headings/page titles may drop the
  rounded halo but never the visible outline.
- **Do** mark data provenance: snapshot age stamps, live badges, honest empty states.
- **Do** keep routes bookmarkable; `#desk` opens Overview; Back/Forward follow section history.

### Don't:
- **Don't** reintroduce floating windows, a dock, or pop-up search; the section workspace
  replaced them (v5) and legacy window geometry is ignored.
- **Don't** use decorative Unicode glyphs (→ ▸ ✦ ⚡ ⧉ ↗) in UI copy — use the sprite
  (`i-arrow-right`, `i-arrow-up-right`, `i-copy`, `i-bolt`, …). Keyboard hints like `⌘ K`
  are text, not icons.
- **Don't** apply the cyan `--ring` halo to focus; it is retired (searchbox uses
  `--ring-gold`). Cyan/magenta appear only as small labelled badge doses.
- **Don't** edit `data.js` by hand — a launchd job regenerates it every 6 hours.
- **Don't** set type below 11px or ship text in `#C9A227` on paper (graphic gold only).

## Finish Review — v5 (2026-10-20)

**Verdict: ship.** The section workspace renders complete and coherent at both required
sizes with zero uncaught JavaScript errors; all five review findings are fixed or
accounted for.

**Review method:** inline substitution for the finish-reviewer role (harness has no
subagent): reviewed the rendered page at 1440×900 and 390×844 in Chromium against the
craft floor, the brief's five findings, and PRODUCT.md's contracts; captures below.
Reviewed input not covered: the real local companion payload (the static build at :9122
correctly degrades to snapshot states; the live build on :9111 still serves the old
desktop checkout, so the live layer was tested by stubbing `local.js` + `/api/fix/log`).

### Checks (all pass)
- **Sections render:** Overview · Projects (79) · Kanban · Agents (39) · Library (200/97/143) · PRDs (63) · Vault · Machine · Stack (9 probes) · About · Search — every section opens, records render, `aria-current` follows. (The later `Life` additions — Wheel of Life and Top 8 — are covered in the audit pass below.)
- **Console:** zero uncaught/page errors on desktop and phone after a full walk incl. `#project:garden-plan`, `#agent:beast`, Back/Forward. Remaining console items are two documented environmental facts on the static rig: `local.js` 404 (absent by design) and the origin-gated `/api/fix/log` CORS refusal — both land in honest empty states ("action history needs the local server"); zero errors remain when the local layer is stubbed.
- **History:** browser Back/Forward follows section + detail history (`#desk` ⇄ `#agent:beast` verified).
- **Phone:** the nav rail stays attached above the scrolling content (top: 0 while the workspace scrolls); no horizontal scroll at 390px on any section (workspace/page/document all 0px overscroll), and the rail's own horizontal scroll stays inside itself.
- **Focus:** cyan halo removed from `:focus-visible`; keyboard focus is a 2px gold outline everywhere (page titles 2px gold, offset 4px; `#workspace` focus keeps a gold outline); searchbox focus = gold edge + `--ring-gold`. No `outline:none` without a replacement.
- **Icons:** decorative `→ ▸ ✦ ☆ ◫ ▣ ▤ ▦ ⚙ ◉ ✎ 📖 ✳ ⚡ ⧉ ↻ ↗` replaced with sprite symbols; sprite carries `i-copy`, `i-arrow-right`, `i-arrow-up-right` (added in the same stroke/grid/stroke-width); `<use href="assets/icons.svg#…">` now 30+ in-page occurrences. `⌘ K` stays text.
- **Type floor:** no `10px` declarations remain; operational labels raised to 11px (`nav-group-title`, `profile`, `kbd`, `activity-avatar`, `pcard .fam` 9px→11px, inline `.fam`/`.tagprd`/`sheet`/`vk` 0.6rem→0.72rem, mono metadata 0.62–0.68rem→0.72–0.75rem). Density re-checked at 390px: nothing overflows; every interactive control measures ≥44px (the nav chips included).
- **Honest data:** stale-snapshot warns, `Snapshot · 1 day old` stamp, machine cards degrade to plain empty cards, fix-log shows "action history needs the local server" — no invented numbers anywhere. Library `&mdash;`/`&amp;` visible in three public titles is a data-generator double-encoding in `data.js` (regenerated every 6 h; hand-editing is forbidden) — flagged, not patched.

### Files changed (all inside `maio-os/`)
- `index.html` — sprite-icon marks in every renderer + button-label restores; `icon:` glyph fields emptied; type floor raised; P2.5/P5 About copy rewritten to the section model (no floating-window remnant language); File empty-state line uses the sprite arrow.
- `assets/icons.svg` — added `i-copy`, `i-arrow-right`, `i-arrow-up-right` (24-grid, 1.75 stroke).
- `assets/workspace.css` — six `10px` → `11px` (nav-group-title ×2, profile-avatar, profile span, kbd, activity-avatar), `.pcard .fam` 9px→11px; `#workspace`/`.page-title` focus-visible rules with gold outline and no halo; `.search-result .nav-icon` 12px inside the phone grid lane.
- `assets/theme.css` — global `:focus-visible` halo removed; searchbox focus = gold edge + `--ring-gold`; `--ring` marked retired; comment updated.

### Captures
- `.impeccable/review/desktop.png` — Overview, 1440×900 (1.25× DPR)
- `.impeccable/review/desktop-projects.png`, `desktop-library.png`, `desktop-machine.png` (settled empty state), `desktop-about.png`, `desktop-about-history.png` — 1440×900
- `.impeccable/review/mobile.png` — Overview, 390×844 (1.25× DPR)
- `.impeccable/review/mobile-scrolled.png` — nav attached after 500px scroll; `mobile-projects.png`, `mobile-library.png`, `mobile-kanban.png`, `mobile-search.png` — 390×844

Work left uncommitted as instructed; server on 127.0.0.1:9122 stopped with the session.
## Audit & Fix Pass (2026-10-21)

Second pass over the shipped workspace after the `Life` group (Wheel of Life, Top 8) landed.
Method: static read of every renderer/handler, then Chromium measurements at 1440×900 and
390×844 (contrast sweep, control sizes, heading outline, accessible names, overflow, console).

### Defects found and fixed

| # | Defect | Impact | Fix |
|---|---|---|---|
| 1 | `Life` sections framed `/wheel` and `/top8/` with an `<iframe>` on **every** origin | On the public Pages build the frame swallowed a 404 behind a blank box — a section that silently pretends to work | `appFrame()` now renders the same honest "lives on the local companion" notebox used by Machine/Vault whenever `ON_COMPANION` is false |
| 2 | Agent portrait fallback used an inline `onerror` whose JSON payload broke the attribute in two (`onerror="…textContent:` + stray `ad"}))"`) | A missing cast portrait left a broken-image box forever; the monogram fallback never ran | `data-mono` attribute + one capture-phase `error` listener that swaps in the monogram (verified: 38 imgs → 37 imgs + 1 monogram) |
| 3 | Copy buttons restored their label with `textContent` after copying | The first clipboard action permanently deleted the sprite copy glyph | `innerHTML` snapshot/restore (verified: svg present → absent during "Copied" → restored) |
| 4 | `local.js` probe and `/api/fix/log` fetch fired from every origin | Two guaranteed console errors (404 + CORS refusal) on any non-companion build | Both gated behind `ON_COMPANION`; status starts honestly `absent`. Console is now **completely clean** |
| 5 | Card titles used `<h5>` directly under `<h1>` | Heading-level jump (H1→H5) for screen-reader navigation, on Machine and Kanban | Card titles are `<h2 class="card-title">`; both CSS layers retargeted |
| 6 | Phone nav grew to **345px (41% of a 390×844 screen)** once `Life` added a 5th group | A third of the viewport spent on chrome before any content | Single attached chip rail: `flex-wrap: nowrap` + horizontal snap scroll + edge fade + active-chip scroll-into-view → **111px (13%)** |
| 7 | Overview `Go to your vault` / activity titles were 17–19px tall on phones | Untappable by thumb (below the 44px guideline) | 44px min-height inline-flex targets in the phone block (all interactive controls now ≥36px, most 44px) |
| 8 | `.btn:focus-visible` used `--cyber-cyan-ink` | Off-palette focus ring contradicting the documented gold system | Gold outline, matching every other control |
| 9 | Library titles printed generator entities literally (`&mdash;`, `&amp;`) | 13 public-shelf titles read "…ceiling &mdash; comparison" | `decodeEntities()` at the card boundary (single pass, unknown/out-of-range entities preserved, output still `esc()`-escaped). `data.js` untouched |
| 10 | Dead legacy-desktop CSS (`.win*`, `#dock`, `.dockbtn`, `#cmdbar`, `.desklet`, `#vitals`) and dead JS (`renderDetail`, `fileHref`, `LSERVER`, `ENRICH_PRDS`, unused `#vitals` branches) | ~24 CSS blocks of unreachable rules; duplicate origin resolver | Removed; `assets/preview.html` keeps its own layout copies and still renders |

### Verified after the pass
- All 13 sections render (Projects 79 · Agents 39 · Library 97 on Public · PRDs 63 · Stack 23 tiles · Search 12 section rows); Wheel/Top 8 show the companion note off-origin.
- **Zero** console messages and zero page errors on desktop and phone across the full walk.
- No horizontal overflow anywhere: document and workspace `scrollWidth − clientWidth = 0` at both sizes, all sections.
- Phone rail stays attached above the scrolling content; the current chip is auto-scrolled into view on deep links (`#about` → `scrollLeft 819`, chip fully visible).
- Contrast sweep (WCAG AA against the resolved background, every leaf text node in sidebar/topbar/workspace): **0 failures**.
- Accessible names: 0 unnamed interactive controls; 0 images without `alt`; 0 duplicate ids.
- Stylesheets carry `?v=v5` so a deploy cannot serve a stale `workspace.css` (this pass hit exactly that).

### Captures (this pass)
- `.impeccable/review/desktop.png`, `desktop-library.png`, `desktop-agents.png`, `desktop-machine.png`, `desktop-wheel.png` — 1440×900
- `.impeccable/review/mobile.png`, `mobile-wheel.png`, `mobile-audit-nav.png` — 390×844

### Correction to this pass (same day)
Three items were re-opened and fixed after review:

- **Vault results were keyboard-unreachable.** `.vres` is `role="button"` — a div gets no
  synthesised click, and the keydown delegate only matched `.pcard`. The delegate now
  handles `.pcard[data-project]` and `.vres[data-vopen]` (Enter + Space), and the comment
  above it states the real rule instead of claiming role=button suffices.
- **Rail focus rings were clipped.** `overflow-y:hidden` with 1px padding sliced the
  2px/5px ring, and the edge fade half-transparented a chip focused in the last 18px.
  Padding is now `5px 18px 5px 0` and `:focus-within` drops the mask. Verified by tabbing
  through all 13 chips at 390px: **0 clipped rings**.
- **Chips were 36px, below the documented 44px floor.** Now 44px (rail height 125px, 15%
  of a 390×844 screen), and the control sweep threshold was corrected to test `<44`
  instead of `<36` — it reported 0 undersized controls at 44px.
- **Over-deleted theme rules restored.** `.win`, `.winbar`, `.winbody`, `.winresize`,
  `.win.max`, `.desklet`, `.dockbtn*`, `.docksep` are rendered by `assets/preview.html`
  (the kit QA sheet); deleting them silently shrank its window mock (winbar 40px→35px,
  resize gradient gone). Restored; the genuinely orphaned page chrome (`#dock`,
  `#scroller`, `.menubtn`, `#cmdbar*`, `#vitals`, plus their dead JS branches) stays removed.
  Preview verified: winbar 41px, gradients and radii intact.

### Known limits
- The companion-only paths (`/wheel`, `/top8/`, `/api/fix*`, `/files/*`, vault reads) cannot be
  exercised from a static server; they are verified only as honest fallbacks. Live behaviour
  depends on `maio-os-local/server.mjs`, which serves a different checkout.
- `data.js` remains generator-owned; entity decoding is a display-layer repair, not a data fix.
