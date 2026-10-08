# maio.os v2 — “daylight” visual kit

Asset kit for the light build. Drop-in: no build step, system fonts only, no CDN,
no raster images. Link `theme.css` **after** the page’s inline `<style>`.

## File map

| File | What it is |
|---|---|
| `theme.css` | Light theme: re-points all 19 of the page’s `:root` names, then re-skins the components. Link it after the inline `<style>`. |
| `logo.svg` | Horizontal `maio.os` wordmark, 320×96 — for light backgrounds, hero + topbar. |
| `glyph.svg` | Square mark, 64×64 viewBox — app icon / avatar. |
| `favicon.svg` | Same mark at 32×32 with a full-bleed plate — browser tab. |
| `icons.svg` | SVG sprite, 12 `<symbol>`s on a 24px grid, 1.75 stroke, `currentColor`. |
| `preview.html` | QA sheet — palette with live contrast scoring, type scale, all components. Serve it, don’t `file://` it (see caveat 1). |

## Logo variants

- **Topbar (20px line):** use `glyph.svg` at ~20–22px beside the live text
  wordmark (`#logo` already types `maio.os` in `--grot`). The glyph is the piece
  that has to survive tiny sizes; the wordmark text then carries the name.
- **Hero / boot:** `logo.svg` at 200–320px wide. It is drawn inside a 320×96
  viewBox with ~26px of built-in padding, so it never needs a wrapper box.
- **Tab:** `favicon.svg` — 32×32, full-bleed plate (the 64px glyph keeps a
  4px transparent inset and would look small in a tab).

## Variable names added

All 19 page names (`--bg --bg2 --panel --panel2 --line --line2 --ink --body --dim --dim2
--gold --gold-dim --ok --warn --bad --blue --grot --sans --mono`) are re-pointed, not
renamed. 27 new tokens, all clearly prefixed: `--cyber-cyan --cyber-magenta
--cyber-cyan-ink --cyber-magenta-ink --cyber-cyan-soft --cyber-magenta-soft --gold-bright
--gold-soft --venture --ok-soft --warn-soft --bad-soft --ok-line --warn-line --bad-line
--radius-xs --radius-sm --radius --radius-lg --radius-pill --hair --shadow-1..4 --ring --ring-gold`.

## Caveats

1. **Sprite + preview need http(s), not `file://`.** Chrome blocks cross-file
   `<use href="icons.svg#…">`; on `file://` the icon grid renders empty. The
   wordmark/glyph/favicon are fine either way.
2. **`--gold` is split.** `--gold` #82650F carries text (5.0:1); `--gold-bright`
   #C9A227 is the original brand accent, kept for fills, borders, logo.
3. **A dark plate on a light theme is deliberate.** The glyph/favicon carry a
   charcoal plate so the white `m` and gold node stay legible in a tab strip;
   drop the `<rect>` if a bare mark is ever needed.
4. Zero `!important`. The page’s mobile `.win{…!important}` geometry block is
   deliberately left untouched. Traffic lights go always-coloured (cartoon
   touch) — delete the `.wl` block to revert to grey-on-hover.
5. Contrast audited against `--panel2` (worst surface a text token can land
   on): every text token clears AA, worst is `--dim2` at 4.64:1.
