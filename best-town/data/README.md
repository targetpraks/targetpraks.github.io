# best-town data

Source data for the Best-Town Explorer (`../index.html`). The page inlines all of
this, so these files are the record of what it renders — regenerate or audit from
here rather than parsing the HTML.

## `top25-verified.json`
The three Top-25 leaderboards (together / Ricardo / Julie), 25 rows each, with
name, country, population, the three scores, and the scored astrocartography line
hits behind each score. Also carries `populations` — the verified population for
every place in the explorer, used for the 100,000 floor.

Scores are relocated-angle astrocartography: a natal planet within 4.0 deg of a
relocated angle is a hit, scored only at orb <= 3.0 deg, at
`planet_weight x angle_weight x (1.25 - orb/5)`. Combined = Ricardo + Julie.
Populations re-verified against each place's own Wikipedia article on 2026-09-15.

## `views-maps.json`
Pre-projected map geometry per view: coastline path, astro line paths, and
markers in pixel space, all on one shared frame so the three maps are comparable.
