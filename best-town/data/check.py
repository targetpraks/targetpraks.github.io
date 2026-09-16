#!/usr/bin/env python3
"""
Deterministic gate for the best-town explorer builds.

Invoked by the builder-handoff runner with cwd = the git worktree of
targetpraks.github.io. Exit 0 = pass; non-zero = fail and the work is discarded.

Why this exists: the repo is a static site with no build step, so without a
declared gate the handoff ships with "Gate: NONE — nothing was verified". These
checks are the difference between "a PR exists" and "the PR is correct".

It covers BOTH deliverables:
  * the Europe sweep and its three per-person leaderboards (top25-verified.json)
  * the whole-world sweep and its world tab (world-verified.json)

This is the builder-facing copy, so it runs from the repo — everything it needs
sits beside it. The authoritative copy used by the handoff runner lives outside
the repo and cannot be edited by the change it checks.
"""
import json
import os
import re
import subprocess
import sys

PAGE = os.path.join("best-town", "index.html")          # relative to cwd = worktree
PS = "/Users/rmmacbook/.hermes/profiles/personal/scripts"
TRUTH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "top25-verified.json")
WORLD_TRUTH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "world-verified.json")
TOL = 0.05

EUROPE_TABS = ("top25", "england", "portugal", "spain", "italy", "greece", "rhodes")
VIEWS = ("together", "ricardo", "julie")
WORLD_ANCHORS = {"together": "Mississauga", "ricardo": "Rochester", "julie": "Plymouth"}

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
    """Every original region tab must survive intact."""
    for tab in EUROPE_TABS:
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
    """Europe deliverable: a 25-row table for Ricardo and one for Julie."""
    top = data.get("top25") or {}
    views = top.get("views")
    if not isinstance(views, dict):
        fail("DATA.top25.views missing — expected keys together / ricardo / julie")
        return
    for who in VIEWS:
        rows = views.get(who)
        if not isinstance(rows, list):
            fail("view %r missing or not a list" % who)
            continue
        if len(rows) != 25:
            fail("view %r has %d rows, expected 25" % (who, len(rows)))
            continue
        want = truth["views"][who]
        for i, (got, exp) in enumerate(zip(rows, want)):
            nm = got.get("n") or "?"
            if nm != exp["n"]:
                fail("view %s row %d: expected %r, got %r" % (who, i + 1, exp["n"], nm))
                continue
            ctry = (got.get("ctry") or "").strip()
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
        notes.append("europe view %s: 25 rows verified" % who)


def check_populations(data, truth):
    """Corrected populations live everywhere, and the floor recomputed from them."""
    pmap = truth["populations"]
    by_name = {}
    for tab, d in data.items():
        if not isinstance(d, dict):
            continue
        for t in d.get("towns", []):
            by_name.setdefault(t.get("n"), []).append((tab, t))

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
        if not isinstance(d, dict):
            continue
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
        fail("more than 6 wrong floor flags — floor not recomputed")


def check_ui(html, data):
    """Europe UI: Country column present, three views wired."""
    if not re.search(r"<th[^>]*>\s*Country\s*</th>", html, re.I):
        fail("no Country column in the table header template")
    js = "\n".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    if "views" not in js:
        fail("the page script never reads the views data")
    low = js.lower()
    for who in ("ricardo", "julie"):
        if who not in low:
            fail("view %r is not referenced anywhere in the page script" % who)


def check_world(data, truth):
    """World deliverable: three 25-row leaderboards anchored to the sweep's winners."""
    w = data.get("world")
    if not isinstance(w, dict):
        fail("DATA.world missing — the world tab was not added")
        return
    for k in ("label", "w", "h", "land", "lines", "markers", "views"):
        if k not in w:
            fail("DATA.world lost key %r" % k)
    if not w.get("land"):
        fail("DATA.world has no land path")
    if not w.get("lines"):
        fail("DATA.world has no astro lines")
    if not w.get("markers"):
        fail("DATA.world has no markers")
    if (w.get("w"), w.get("h")) != (1440, 720):
        fail("DATA.world frame is %sx%s, expected 1440x720" % (w.get("w"), w.get("h")))

    views = w.get("views")
    if not isinstance(views, dict):
        fail("DATA.world.views missing")
        return
    for who in VIEWS:
        rows = views.get(who)
        if not isinstance(rows, list):
            fail("world view %r missing or not a list" % who)
            continue
        if len(rows) != 25:
            fail("world view %r has %d rows, expected 25" % (who, len(rows)))
            continue
        if rows[0].get("n") != WORLD_ANCHORS[who]:
            fail("world view %r #1 is %r, expected %r — wrong sweep or wrong sort"
                 % (who, rows[0].get("n"), WORLD_ANCHORS[who]))
        want = truth["views"][who]
        for i, (got, exp) in enumerate(zip(rows, want)):
            nm = got.get("n") or "?"
            if nm != exp["n"]:
                fail("world %s row %d: expected %r, got %r" % (who, i + 1, exp["n"], nm))
                continue
            ctry = (got.get("ctry") or "").strip()
            if not ctry:
                fail("world %s row %d (%s): country is empty" % (who, i + 1, nm))
            elif ctry != exp["ctry"]:
                fail("world %s row %d (%s): country %r, expected %r" % (who, i + 1, nm, ctry, exp["ctry"]))
            for key in ("s", "r", "j"):
                if key in got and abs(float(got[key]) - float(exp[key])) > TOL:
                    fail("world %s row %d (%s): %s=%s, expected %s"
                         % (who, i + 1, nm, key, got[key], exp[key]))
            pk = got.get("popk")
            if pk is None:
                fail("world %s row %d (%s): no population" % (who, i + 1, nm))
            elif abs(float(pk) - float(exp["popk"])) > 0.6:
                fail("world %s row %d (%s): population %.1fk, expected %.1fk"
                     % (who, i + 1, nm, float(pk), float(exp["popk"])))
        notes.append("world view %s: 25 rows verified" % who)

    maps = data.get("maps") or {}
    for who in VIEWS:
        key = "world-" + who
        g = maps.get(key)
        if not isinstance(g, dict):
            fail("DATA.maps.%s missing" % key)
            continue
        if not g.get("land"):
            fail("DATA.maps.%s has no land path" % key)
        if not g.get("markers"):
            fail("DATA.maps.%s has no markers" % key)
        gw, gh = g.get("w"), g.get("h")
        for m in g.get("markers", []):
            if not (0 <= m.get("cx", -1) <= gw and 0 <= m.get("cy", -1) <= gh):
                fail("%s: marker %s outside the frame" % (key, m.get("label")))
                break
        for m in g.get("markers", []):
            if m.get("count", 1) > 1 and not m.get("members"):
                fail("%s: merged marker %s carries no member list" % (key, m.get("label")))
                break


def check_world_ui(html, data):
    """World tab reachable and wired, without disturbing the existing tabs."""
    m = re.search(r"const ORDER = \[(.*?)\]", html, re.S)
    if not m:
        fail("const ORDER not found")
    else:
        try:
            order = json.loads("[" + m.group(1) + "]")
        except Exception as e:
            order = None
            fail("ORDER is not parseable: %s" % e)
        if order:
            if "world" not in order:
                fail("ORDER does not contain the world tab")
            elif order.index("world") != 1:
                fail("world tab is at ORDER position %d, expected 1 (right after top25)"
                     % order.index("world"))
            for tab in EUROPE_TABS:
                if tab not in order:
                    fail("ORDER lost the %r tab" % tab)
    js = "\n".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    if "world" not in js.lower():
        fail("the page script never references the world tab")
    if not re.search(r"aria-label", js):
        fail("no aria-label in the page script — merged world markers must be inspectable")


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

    check_world(data, json.load(open(WORLD_TRUTH, encoding="utf-8")))
    check_world_ui(html, data)

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
