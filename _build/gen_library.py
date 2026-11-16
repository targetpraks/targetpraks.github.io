#!/usr/bin/env python3
"""
Build library.html — the index of every page published to targetpraks.github.io.

Every figure and every card comes from the files themselves: the title is the file's own
<title>, the summary is its own first real paragraph, the date is its own filename, the
screenshot is its own rendering. Nothing is typed by hand, so the index cannot drift from
the site.

    python3 _build/gen_library.py            # rebuild library.html
    python3 _build/gen_library.py --shoot    # also shoot any missing screenshots

Run from anywhere; paths are resolved from this file's location.
"""
import hashlib
import html as H
import json
import os
import re
import subprocess
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "assets", "lib")
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SKIP_NAMES = {"jump.html", "library.html"}
SKIP_REL = {"index.html"}
HIDDEN_DIRS = ("graphify-out", "_build", "assets", "node_modules", ".git")

TAGS = [
    ("investments", r"invest|cape-town|rental|yield|bond|airbnb|hotel|algarve|property|finance|portfolio|wealth|money"),
    ("papa-pasta", r"papa|pasta|menu|kitchen|supplier|rfq|espetada|souvlaki|braai"),
    ("infinity-brands", r"infinity|clickup|cliq|zoho|brand|gsd|dashboard|constellation|agenticos"),
    ("donatello", r"donatello|school|therapist|facilitator"),
    ("3d-print", r"3d-print|print-queue|filament|creality|dummy-13|bambu|slicer"),
    ("agents", r"agent|skill|paperclip|scrooge|bruce|beast|scribe|hermes|character-sheet|profile"),
    ("household", r"household|roster|almanac|wheel|garden|plumber|solar|inverter"),
    ("health", r"health|medical|breastfeed|sleep|baby"),
    ("stack", r"stack|backup|health-check|watchtower|deploy|docker|colima|server|migration"),
]


def key(rel):
    return hashlib.sha1(rel.encode()).hexdigest()[:12]


def page_files():
    out = []
    for name in os.listdir(ROOT):
        if name.endswith(".html") and name not in SKIP_NAMES and name not in SKIP_REL:
            out.append(name)
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in HIDDEN_DIRS and not d.startswith(".")]
        if os.path.abspath(dirpath) == ROOT:
            continue
        for name in filenames:
            if name.endswith(".html") and name not in SKIP_NAMES:
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(set(out))


def find_date(rel):
    base = os.path.basename(rel)
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", base)
    if m:
        return "%s-%s-%s" % m.groups()
    m = re.search(r"(20\d\d)-(\d\d)(?!-)", base)
    if m:
        return "%s-%s" % m.groups()
    return None


def read_meta(rel):
    path = os.path.join(ROOT, rel)
    raw = open(path, encoding="utf-8", errors="ignore").read()
    t = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    title = H.unescape(re.sub(r"\s+", " ", t.group(1))).strip() if t else ""
    if not title:
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S | re.I)
        title = H.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else ""
    if not title:
        title = os.path.basename(rel)[:-5].replace("-", " ").title()
    summary = ""
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S | re.I)
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", body, re.S | re.I):
        txt = H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1)))).strip()
        if len(txt) > 70 and not re.match(r"^(published|generated|download|source)", txt, re.I):
            summary = txt
            break
    tags = [name for name, pat in TAGS if re.search(pat, (rel + " " + title).lower())]
    return {
        "file": rel,
        "title": title,
        "summary": summary,
        "date": find_date(rel),
        "bytes": os.path.getsize(path),
        "mtime": int(os.path.getmtime(path)),
        "tags": tags,
        "thumb": key(rel) + ".jpg" if os.path.exists(os.path.join(LIB, key(rel) + ".jpg")) else None,
    }


def shoot(rel):
    jpg = os.path.join(LIB, key(rel) + ".jpg")
    if os.path.exists(jpg):
        return "skip"
    os.makedirs(LIB, exist_ok=True)
    tmp = "/tmp/libshot"
    os.makedirs(tmp, exist_ok=True)
    png = os.path.join(tmp, key(rel) + ".png")
    profile = "/tmp/libchrome/" + key(rel)
    url = "file://" + os.path.join(ROOT, rel).replace(" ", "%20").replace("#", "%23")
    try:
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=900,563",
                        "--user-data-dir=" + profile, "--screenshot=" + png, url],
                       capture_output=True, timeout=45)
    except subprocess.TimeoutExpired:
        subprocess.run(["pkill", "-f", profile], capture_output=True)
        subprocess.run(["rm", "-rf", profile], capture_output=True)
        return "timeout"
    if not os.path.exists(png):
        return "fail"
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "62",
                    "-Z", "560", png, "--out", jpg], capture_output=True)
    os.remove(png)
    subprocess.run(["rm", "-rf", profile], capture_output=True)
    return "ok"


def m0(n):
    return str(int(round(n))).replace(",", " ")


def kb(n):
    return "%s KB" % m0(n / 1024.0)


def pretty(day):
    import datetime
    try:
        d = datetime.date(*[int(x) for x in day.split("-")])
    except Exception:
        return day
    return d.strftime("%A %-d %B %Y")


def short(day):
    import datetime
    try:
        d = datetime.date(*[int(x) for x in day.split("-")])
    except Exception:
        return day
    return d.strftime("%-d %b %Y")


def card(it, big=False):
    href = H.escape(it["file"])
    title = H.escape(it["title"])
    summ = H.escape(it["summary"][:220]) + ("…" if len(it["summary"]) > 220 else "")
    if it["thumb"]:
        img = ('<img src="assets/lib/%s" alt="" loading="lazy" decoding="async">'
               % it["thumb"])
    else:
        img = '<div class="noimg"><span>no screenshot</span></div>'
    tags = "".join('<span class="t">%s</span>' % H.escape(t) for t in it["tags"][:2])
    cls = "card big" if big else "card"
    return """    <a class="%s" href="%s">
      <div class="shot">%s</div>
      <div class="cap">
        <h3>%s</h3>
        %s
        <p class="meta">%s · %s %s</p>
      </div>
    </a>""" % (cls, href, img, title, ('<p class="sum">%s</p>' % summ) if summ else "",
               kb(it["bytes"]), pretty(it["date"]).split(" ", 1)[1] if it["date"] and len(it["date"]) == 10 else "undated", tags)


def main():
    want_shoot = "--shoot" in sys.argv
    files = page_files()
    if want_shoot:
        missing = [f for f in files if not os.path.exists(os.path.join(LIB, key(f) + ".jpg"))]
        print("shooting %d missing screenshots" % len(missing), flush=True)
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(6) as ex:
            res = list(ex.map(shoot, missing))
        print("  ", Counter(res), flush=True)
    items = [read_meta(f) for f in files]
    dated = [i for i in items if i["date"] and len(i["date"]) == 10]
    dated.sort(key=lambda i: (i["date"], i["mtime"]), reverse=True)
    monthly = [i for i in items if i["date"] and len(i["date"]) == 7]
    monthly.sort(key=lambda i: i["mtime"], reverse=True)
    undated = sorted([i for i in items if not i["date"]], key=lambda i: i["mtime"], reverse=True)

    days = []
    for it in dated:
        if not days or days[-1][0] != it["date"]:
            days.append((it["date"], []))
        days[-1][1].append(it)

    newest = dated[:3]
    blocks = []
    blocks.append('<div class="grid three">\n%s\n  </div>' % "\n".join(card(i, True) for i in newest))
    for day, group in days:
        tiles = "\n".join(card(i) for i in group)
        blocks.append("""  <section class="day" data-m="%s">
    <h2><span>%s</span><em>%s %s</em></h2>
    <div class="grid">
%s
    </div>
  </section>""" % (day[:7], pretty(day), len(group), "page" if len(group) == 1 else "pages", tiles))
    if monthly or undated:
        rest = monthly + undated
        blocks.append("""  <section class="day" data-m="older">
    <h2><span>Older, and undated</span><em>%s pages</em></h2>
    <div class="grid">
%s
    </div>
  </section>""" % (len(rest), "\n".join(card(i) for i in rest)))

    months = Counter(i["date"][:7] for i in dated)
    chips = "".join('<button class="chip" data-m="%s">%s <b>%d</b></button>' % (m, m, n)
                    for m, n in sorted(months.items(), reverse=True))
    total_mb = sum(i["bytes"] for i in items) / 1048576.0
    payload = json.dumps([{k: i[k] for k in ("file", "title", "summary", "date", "tags")} for i in items],
                         ensure_ascii=False)

    doc = TEMPLATE % {
        "count": m0(len(items)),
        "days": m0(len(days)),
        "mb": "%.0f" % total_mb,
        "shots": m0(sum(1 for i in items if i["thumb"])),
        "first": short(dated[-1]["date"]) if dated else "—",
        "last": short(dated[0]["date"]) if dated else "—",
        "chips": chips,
        "blocks": "\n".join(blocks),
        "payload": payload,
        "built": __import__("datetime").datetime.now().strftime("%-d %B %Y, %H:%M"),
    }
    out = os.path.join(ROOT, "library.html")
    open(out, "w", encoding="utf-8").write(doc)
    print("wrote %s | %s chars | %s pages | %s screenshots"
          % (out, m0(len(doc)), m0(len(items)), m0(sum(1 for i in items if i["thumb"]))))


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Library — every page published to targetpraks.github.io</title>
<style>
:root{
  --paper:#fdfaf3; --card:#ffffff; --ink:#12203a; --ink2:#4a5568; --ink3:#8b95a5;
  --line:#e6ddc9; --navy:#1b3a63; --coral:#c2543f; --gold:#a8791c; --teal:#2c6f6a;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%}
body{margin:0;background:var(--paper);color:var(--ink);
  font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px 80px}
header.top{border-bottom:2px solid var(--ink);margin-bottom:26px;padding:30px 0 18px}
.kicker{font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--coral);
  font-weight:700;margin:0 0 10px}
h1{font:700 clamp(32px,5vw,52px)/1.05 Georgia,"Times New Roman",serif;margin:0 0 12px;letter-spacing:-.5px}
.standfirst{font-size:17px;color:var(--ink2);max-width:66ch;margin:0}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 0}
.stat{background:var(--card);border:2px solid var(--line);border-radius:12px;padding:10px 14px;min-width:104px}
.stat b{display:block;font:700 22px/1.1 Georgia,serif;color:var(--navy)}
.stat span{font-size:11.5px;color:var(--ink3);letter-spacing:.04em}
.bar{position:sticky;top:0;z-index:9;background:rgba(253,250,243,.96);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);padding:12px 0;margin:6px 0 26px}
.tools{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
input[type=search]{flex:1 1 280px;min-height:46px;padding:0 14px;border:2px solid var(--line);
  border-radius:11px;background:#fff;font:inherit;color:var(--ink)}
input[type=search]:focus{outline:none;border-color:var(--navy)}
.chip{border:2px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;
  padding:9px 13px;font:600 13px/1 inherit;cursor:pointer}
.chip b{color:var(--ink3);font-weight:600}
.chip.on{background:var(--navy);border-color:var(--navy);color:#fff}
.chip.on b{color:rgba(255,255,255,.75)}
.day{margin:34px 0 0}
.day h2{display:flex;align-items:baseline;gap:12px;border-bottom:1px solid var(--line);
  padding:0 0 8px;margin:0 0 16px;font:700 19px/1.2 Georgia,serif;color:var(--navy)}
.day h2 em{font:400 12.5px/1 inherit;color:var(--ink3);font-style:normal;letter-spacing:.05em;
  text-transform:uppercase}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.grid.three{grid-template-columns:repeat(auto-fill,minmax(300px,1fr));margin-bottom:8px}
.card{display:flex;flex-direction:column;background:var(--card);border:2px solid var(--line);
  border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;
  transition:transform .09s ease,border-color .09s ease,box-shadow .09s ease}
.card:hover{transform:translateY(-2px);border-color:var(--navy);
  box-shadow:0 10px 24px rgba(18,32,58,.10)}
.shot{aspect-ratio:16/10;background:#f3eee2;overflow:hidden;border-bottom:1px solid var(--line)}
.shot img{width:100%%;height:100%%;object-fit:cover;object-position:top center;display:block}
.noimg{width:100%%;height:100%%;display:flex;align-items:center;justify-content:center;
  color:var(--ink3);font-size:12px}
.cap{padding:11px 13px 13px;display:flex;flex-direction:column;gap:5px}
.cap h3{margin:0;font:650 14.5px/1.32 inherit;color:var(--ink)}
.big .cap h3{font-size:16px}
.sum{margin:0;font-size:12.8px;line-height:1.42;color:var(--ink2);
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.meta{margin:2px 0 0;font-size:11.5px;color:var(--ink3);letter-spacing:.03em}
.t{display:inline-block;background:#f2ede0;color:#6b5a33;border-radius:5px;padding:1px 6px;
  margin-left:6px;font-size:10.5px;letter-spacing:.04em;text-transform:uppercase;font-weight:700}
.hidden{display:none !important}
.empty{display:none;padding:60px 0;text-align:center;color:var(--ink3)}
footer{margin-top:60px;border-top:2px solid var(--ink);padding-top:16px;color:var(--ink3);font-size:12.5px}
@media(max-width:560px){
  .wrap{padding:0 15px 60px}
  .grid,.grid.three{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:11px}
  .cap h3{font-size:13px}.sum{display:none}
  h1{font-size:31px}
}
@media print{
  .bar,.tools{display:none}
  .grid{grid-template-columns:repeat(3,1fr)}
  .card{break-inside:avoid}
  body{background:#fff}
}
</style>
</head>
<body>
<div class="wrap">

<header class="top">
  <p class="kicker">targetpraks.github.io · the external site</p>
  <h1>The Library</h1>
  <p class="standfirst">Every page the agents have published, newest first, with a picture of each one.
  Click any card to read the page itself. Nothing on this index is typed by hand — titles, dates,
  summaries and screenshots are read from the published files each time it is rebuilt.</p>
  <div class="stats">
    <div class="stat"><b>%(count)s</b><span>pages</span></div>
    <div class="stat"><b>%(days)s</b><span>days with work</span></div>
    <div class="stat"><b>%(shots)s</b><span>screenshots</span></div>
    <div class="stat"><b>%(mb)s MB</b><span>of HTML</span></div>
    <div class="stat"><b>%(first)s</b><span>first page</span></div>
    <div class="stat"><b>%(last)s</b><span>latest page</span></div>
  </div>
</header>

<div class="bar">
  <div class="tools">
    <input type="search" id="q" placeholder="Search %(count)s pages — title, summary, tag…" autocomplete="off">
    <button class="chip on" data-m="all">All</button>
    %(chips)s
  </div>
</div>

%(blocks)s

<p class="empty" id="none">Nothing matches that. Try a shorter word.</p>

<footer>
  Rebuilt %(built)s · generator <code>_build/gen_library.py</code> · every card is a real page on this site.
</footer>
</div>

<script type="application/json" id="idx">%(payload)s</script>
<script>
(function(){
  var q=document.getElementById('q'), none=document.getElementById('none');
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  var month='all';
  var cards=[].slice.call(document.querySelectorAll('.card'));
  function norm(s){return (s||'').toLowerCase()}
  cards.forEach(function(c){
    c.dataset.s=norm(c.textContent+' '+(c.getAttribute('href')||''));
  });
  function apply(){
    var term=norm(q.value.trim()); var shown=0;
    cards.forEach(function(c){
      var sec=c.closest('.day');
      var ok=(month==='all'|| (sec&&sec.dataset.m===month) || month==='older'&&sec&&sec.dataset.m==='older');
      if(ok&&term) ok=c.dataset.s.indexOf(term)>-1;
      c.classList.toggle('hidden',!ok); if(ok) shown++;
    });
    [].slice.call(document.querySelectorAll('.day')).forEach(function(sec){
      var any=sec.querySelectorAll('.card:not(.hidden)').length;
      sec.classList.toggle('hidden', any===0);
    });
    none.style.display=shown?'none':'block';
    document.querySelector('.grid.three').classList.toggle('hidden',!!term||month!=='all');
  }
  q.addEventListener('input',apply);
  chips.forEach(function(b){b.addEventListener('click',function(){
    chips.forEach(function(x){x.classList.remove('on')});
    b.classList.add('on'); month=b.dataset.m; apply();
    window.scrollTo({top:document.querySelector('.bar').offsetTop-4,behavior:'smooth'});
  })});
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
