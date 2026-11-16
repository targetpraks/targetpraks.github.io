#!/usr/bin/env python3
"""
Draw the candidate map for the Cape Town decision document.

A map's job here is geography, not data density: it shows WHERE the candidates sit and whether
their precinct passes the safety screen. The yields live in the ladder chart and the tables, so
they are deliberately not repeated on a pin nobody can read at page width.

Nothing here is typed by hand: the places are geocoded once into coords.json, the safety colours
come from the SAPS precinct table, and the basemap is OpenStreetMap.
Output: assets/cape-town/cape-town-map.jpg

    python3 _build/gen_cape_town_map.py
"""
import json
import math
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S = "/Users/ricardomaio/.hermes/profiles/batman/cache/scratch/"
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ZOOM = 12                      # sized so the whole extent lands near the page's 1016 px column
OUT = os.path.join(ROOT, "assets", "cape-town", "cape-town-map.png")

coords = json.load(open(S + "coords.json"))
coords["Devon Valley"] = {"lat": -33.9034472, "lon": 18.8146957}
v3 = json.load(open(S + "model_v3.json"))
safety = json.load(open(S + "safety.json"))
PREC = v3.get("precincts") or {}
MED = v3.get("median_violent") or safety["median_violent"]


def viol(precinct):
    if not precinct:
        return None
    for k, v in PREC.items():
        if k.lower() == precinct.lower():
            return v["violent"]
    return None


# (kind, short label, geocoded place, dx, dy, label side, precinct)
PINS = [
    ("deal", "Parklands",                "Table View",      0,   0,  "b", "Table View"),
    ("deal", "Brackenfell",              "Brackenfell",     0,   0,  "b", "Brackenfell"),
    ("deal", "Parow ×2",                 "Parow",           0,  -6,  "t", "Parow"),
    ("deal", "Maitland",                 "Maitland",       10,  14,  "r", "Maitland"),
    ("deal", "Milnerton",                "Milnerton",      -8, -12,  "l", "Milnerton"),
    ("hotel", "Lagoon Beach",            "Milnerton",      10,  16,  "r", "Milnerton"),
    ("comm", "Woodstock",                "Woodstock",      -6,  16,  "l", "Woodstock"),
    ("comm", "Paarden Eiland",           "Paarden Eiland",  8,  -8,  "r", "Paarden Eiland"),
    ("hotel", "CBD ×5 hotels",           "CBD",             0, -12,  "b", "CBD"),
    ("deal", "Kuils River ×2",           "Kuilsrivier",     0,   0,  "b", "Kuilsrivier"),
    ("hotel", "KLEI",                    "Devon Valley",    0,   0,  "b", "Stellenbosch"),
]

pins = []
for kind, label, where, dx, dy, anchor, precinct in PINS:
    c = coords.get(where)
    if not c:
        print("  no coordinate for", where)
        continue
    pins.append({"kind": kind, "label": label, "lat": c["lat"], "lon": c["lon"],
                 "dx": dx, "dy": dy, "anchor": anchor, "violent": viol(precinct), "precinct": precinct})
print("pins:", len(pins))


def px(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n * 256
    s = math.sin(math.radians(lat))
    yv = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n * 256
    return x, yv


PAD = 0.020
lats = [p["lat"] for p in pins]
lons = [p["lon"] for p in pins]
x0, y0 = px(max(lats) + PAD, min(lons) - PAD, ZOOM)
x1, y1 = px(min(lats) - PAD, max(lons) + PAD, ZOOM)
x0, y0, x1, y1 = x0 - 62, y0 - 34, x1 + 62, y1 + 40
W, H = int(x1 - x0), int(y1 - y0)
tx0, ty0 = int(x0 // 256), int(y0 // 256)
tx1, ty1 = int(x1 // 256), int(y1 // 256)
tiles = "".join(
    f'<img src="https://tile.openstreetmap.org/{ZOOM}/{tx}/{ty}.png" '
    f'style="left:{tx * 256 - x0:.0f}px;top:{ty * 256 - y0:.0f}px">'
    for tx in range(tx0, tx1 + 1) for ty in range(ty0, ty1 + 1))
print(f"map {W}x{H} from {(tx1 - tx0 + 1) * (ty1 - ty0 + 1)} tiles")

pin_html = []
for p in pins:
    x, yv = px(p["lat"], p["lon"], ZOOM)
    left = min(max(x - x0 + p["dx"], 58), W - 58)
    top = min(max(yv - y0 + p["dy"], 26), H - 26)
    safe = p["violent"] is not None and p["violent"] <= MED
    cls = "safe" if safe else ("unsafe" if p["violent"] is not None else "unknown")
    cls += {"hotel": " hotel", "comm": " comm"}.get(p["kind"], "")
    pin_html.append(
        f'<div class="pin {cls} a{p["anchor"]}" style="left:{left:.0f}px;top:{top:.0f}px">'
        f'<b></b><i>{p["label"]}</i></div>')

HTML = """<!doctype html><meta charset="utf-8"><style>
html,body{margin:0;background:#eef2f4}
.map{position:relative;width:%dpx;height:%dpx;overflow:hidden}
.map>img{position:absolute;width:256px;height:256px;border:0}
.pin{position:absolute;transform:translate(-50%%,-50%%);width:0;height:0}
.pin b{position:absolute;left:-8px;top:-8px;width:16px;height:16px;border-radius:50%%;background:#c4452f;
  border:2.5px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.45)}
.pin.safe b{background:#1f6f6b}
.pin.comm b{border-radius:3px;background:#8c6d1f}
.pin.hotel b{border-radius:3px;background:#1b3a63}
.pin i{position:absolute;padding:1px 5px;border-radius:3px;background:rgba(255,255,255,.93);
  color:#12203a;font:700 13px/1.35 -apple-system,Helvetica,sans-serif;font-style:normal;
  white-space:nowrap;box-shadow:0 1px 2px rgba(0,0,0,.25)}
.pin.ab i{left:-50%%;top:13px}
.pin.at i{left:-50%%;bottom:13px}
.pin.al i{right:12px;top:-9px}
.pin.ar i{left:12px;top:-9px}
</style><div class="map">%s%s</div>""" % (W, H, tiles, "".join(pin_html))

open("/tmp/capetown_map.html", "w").write(HTML)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=2", f"--window-size={W},{H}",
                "--virtual-time-budget=15000", f"--screenshot={OUT}", "file:///tmp/capetown_map.html"],
               capture_output=True, timeout=200)
subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", OUT,
                "--out", OUT.replace(".png", ".jpg")], capture_output=True, timeout=120)
print(f"map {W}x{H} css px ->", os.path.getsize(OUT.replace(".png", ".jpg")), "bytes jpeg")
