#!/usr/bin/env python3
"""
Deterministic gate for the best-town explorer build.

Invoked by the builder-handoff runner with cwd = the git worktree of
targetpraks.github.io. Exit 0 = pass; non-zero = fail and the work is discarded.

Why this exists: the repo is a static site with no build step, so without a
declared gate the handoff ships with "Gate: NONE — nothing was verified". These
checks are the difference between "a PR exists" and "the PR is correct".

This is the builder-facing copy, so it runs from the repo. The authoritative
copy used by the handoff runner lives outside the repo and cannot be edited by
the change it checks.
"""
import json
import os
import re
import subprocess
import sys

PAGE = os.path.join("best-town", "index.html")          # relative to cwd = worktree
TRUTH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "top25-verified.json")
TOL = 0.05

fails = []
notes = []


def fail(msg):
    fails.append(msg)


def load():
    if not os.path.exists(PAGE):
        fail("missing %s" % PAGE)
        return None, None
    html = open(PAGE, encoding="utf-8").read()
    m = re.search(r"const DATA = (\{.*?\});\s*\nconst ORDER", html, re.S)
    if not m:
        fail("could not find the `const DATA = {...};` literal in %s" % PAGE)
        return html, None
    try:
        data = json.loads(m.group(1))
    except Exception as e:
        fail("DATA literal is not valid JSON: %s" % e)
        return html, None
    return html, data


def check_js_parses(html):
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not scripts:
        fail("no inline <script> found")
        return
    for i, s in enumerate(scripts):
        path = "/tmp/_gate_script_%d.js" % i
        open(path, "w", encoding="utf-8").write(s)
        rc = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        if rc.returncode != 0:
            fail("inline script %d fails `node --check`: %s" % (i, (rc.stderr or "").strip()[:400]))


def check_tabs(data):
    for tab in ("top25", "england", "portugal", "spain", "italy", "greece", "rhodes"):
        if tab not in data:
            fail("tab %r disappeared from DATA" % tab)
            continue
        d = data[tab]
        for k in ("label", "towns", "markers", "lines", "w", "h", "land"):
            if k not in d:
                fail("tab %r lost key %r" % (tab, k))
        if not d.get("towns"):
            fail("tab %r has no towns" % tab)


def check_views(data, truth):
    """The core deliverable: a 25-row table for Ricardo and one for Julie."""
    top = data.get("top25") or {}
    views = top.get("views")
    if not isinstance(views, dict):
        fail("DATA.top25.views missing — expected keys together / ricardo / julie")
        return
    for who in ("together", "ricardo", "julie"):
        rows = views.get(who)
        if not isinstance(rows, list):
            fail("view %r missing or not a list" % who)
            continue
        if len(rows) != 25:
            fail("view %r has %d rows, expected 25" % (who, len(rows)))
            continue
        want = truth["views"][who]
        for i, (got, exp) in enumerate(zip(rows, want)):
            nm = got.get("n") or got.get("name") or "?"
            if nm != exp["n"]:
                fail("view %s row %d: expected %r, got %r" % (who, i + 1, exp["n"], nm))
                continue
            ctry = (got.get("ctry") or got.get("country") or "").strip()
            if not ctry:
                fail("view %s row %d (%s): country is empty" % (who, i + 1, nm))
            elif ctry != exp["ctry"]:
                fail("view %s row %d (%s): country %r, expected %r" % (who, i + 1, nm, ctry, exp["ctry"]))
            for key in ("s", "r", "j"):
                if key in got and abs(float(got[key]) - float(exp[key])) > TOL:
                    fail("view %s row %d (%s): %s=%s, expected %s"
                         % (who, i + 1, nm, key, got[key], exp[key]))
            pk = got.get("popk")
            if pk is None:
                fail("view %s row %d (%s): no population" % (who, i + 1, nm))
            elif abs(float(pk) - float(exp["popk"])) > 0.6:
                fail("view %s row %d (%s): population %.1fk, expected %.1fk"
                     % (who, i + 1, nm, float(pk), float(exp["popk"])))
        notes.append("view %s: 25 rows verified against top25-verified.json" % who)


def check_populations(data, truth):
    """Corrected populations must be live everywhere, floor recomputed."""
    pmap = truth["populations"]
    by_name = {}
    for tab, d in data.items():
        for t in d.get("towns", []):
            by_name.setdefault(t["n"], []).append((tab, t))

    spot = ["Braga", "Coimbra", "Sintra", "Salamanca", "Swindon", "Eastbourne",
            "Lagos", "M\u00e9rida", "Vila Nova de Gaia", "Almada"]
    for n in spot:
        want = pmap.get(n)
        if want is None:
            fail("truth table has no population for %s" % n)
            continue
        rows = by_name.get(n)
        if not rows:
            fail("spot-check town %s is missing from every tab" % n)
            continue
        for tab, t in rows:
            pk = t.get("popk")
            if pk is None:
                fail("%s in %s has no population" % (n, tab))
            elif abs(float(pk) - float(want)) > 0.6:
                fail("%s in %s shows %.1fk, expected %.1fk" % (n, tab, float(pk), float(want)))

    bad = 0
    for tab, d in data.items():
        for t in d.get("towns", []):
            pk, fl = t.get("popk"), t.get("floor")
            if pk is None or fl is None:
                continue
            if bool(fl) != (float(pk) >= truth["floor_k"]):
                if bad < 6:
                    fail("floor flag wrong: %s in %s has popk=%.1f but floor=%s"
                         % (t["n"], tab, float(pk), fl))
                bad += 1
    if bad >= 6:
        fail("more than 6 wrong floor flags — floor not recomputed from corrected populations")


def check_ui(html, data):
    """The table renders Country, and the three views are wired into the UI."""
    if not re.search(r"<th[^>]*>\s*Country\s*</th>", html, re.I):
        fail("no Country column in the table header template")
    js = "\n".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    if "views" not in js:
        fail("the page script never reads DATA.top25.views")
    low = js.lower()
    for who in ("ricardo", "julie"):
        if who not in low:
            fail("view %r is not referenced anywhere in the page script" % who)
    if not re.search(r"\bview\b|\bviews\b", js, re.I):
        fail("no view switcher logic found in the page script")
    # each view's own map must exist and be internally consistent
    for who in ("together", "ricardo", "julie"):
        g = (data.get("maps") or {}).get("top25-" + who) or (data.get("maps") or {}).get(who)
        if not isinstance(g, dict):
            continue
        if not g.get("land"):
            fail("map for view %s has no land path" % who)
        if not g.get("markers"):
            fail("map for view %s has no markers" % who)
        W, H = g.get("w"), g.get("h")
        for m in g.get("markers", []):
            if not (0 <= m.get("cx", -1) <= W and 0 <= m.get("cy", -1) <= H):
                fail("map %s: marker %s is outside the frame" % (who, m.get("label")))
                break


def main():
    html, data = load()
    if html is None:
        print("\n".join("FAIL: " + f for f in fails))
        return 1
    check_js_parses(html)
    if data is None:
        print("\n".join("FAIL: " + f for f in fails))
        return 1
    truth = json.load(open(TRUTH, encoding="utf-8"))
    check_tabs(data)
    check_views(data, truth)
    check_populations(data, truth)
    check_ui(html, data)

    for n in notes:
        print("ok: " + n)
    if fails:
        print("\n%d check(s) FAILED:" % len(fails))
        for f in fails[:40]:
            print("FAIL: " + f)
        if len(fails) > 40:
            print("... and %d more" % (len(fails) - 40))
        return 1
    print("all best-town checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
