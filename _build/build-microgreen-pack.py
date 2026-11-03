#!/usr/bin/env python3
"""Build the TLF microgreen pack: web page + A3 wall sheets + A4 grow-room forms.

Sources (no invented figures):
  TLF franchise model brief  -> 80 trays, 2 cycles/month, 200-300 g/tray, 10-14 days,
                                5-10 cm, 18-24 C, 40-60 % RH, packaging, cold chain
  TLF grow machine spec      -> lights 18/6, pump 10 min 08:00 + 16:00, fans 10 min/30
  PSU Extension              -> 10-15 g seed per tray, 136 g/tray average, yield table,
                                41 F storage, damping-off, sub-irrigation
  Bootstrap Farmer cheat sheet (trade practice, marked *)  -> per-variety seed rate,
                                soak, blackout, days to cut
  * = trade practice, not yet measured in this room.
"""
import pathlib, html

OUT = pathlib.Path("/Volumes/Hiksemi 1TB/DevMini/targetpraks.github.io")

PURPLE = "#330072"
CYAN   = "#10AEAA"
LILAC  = "#E6DFED"
MID    = "#5C348D"
TEAL   = "#077169"

def _sub(css: str) -> str:
    for k, v in (("%(P)s", PURPLE), ("%(C)s", CYAN), ("%(L)s", LILAC), ("%(M)s", MID), ("%(T)s", TEAL)):
        css = css.replace(k, v)
    return css.replace("%%", "%")

# ----------------------------------------------------------------------------
# content
# ----------------------------------------------------------------------------
STAGES = [
    dict(
        num="01", title="Set up and sow", when="Day 0", whensub="one tray at a time",
        steps=[
            ("01", "Clean the tray",
             "Wash it, sanitise with food-safe sanitiser, rinse, dry it upside down. A tray that still smells of the last crop is the next crop lost.",
             "A dirty tray fails quietly — the mould shows on day four, not on day nought."),
            ("02", "Fill the medium",
             "Coco coir or a hemp mat, pre-moistened before it goes in. Level it to the rim, then firm it flat with the press.",
             "Firm, not compacted. A hard tray roots on the surface instead of into it."),
            ("03", "Weigh the seed",
             "Weigh by variety, never by eye: 15–20 g for a brassica, 30–35 g radish, 200–275 g pea, 450 g wheatgrass. Every rate is on the variety sheet.",
             "Seed by eye is how one tray comes up thin and the next one moulds."),
            ("04", "Sow to the edges",
             "Edges first, then the middle, so the last of the seed lands where the hand is not yet tired. Even coverage is the whole game.",
             "A bare strip at the edge is a bare strip in the punnet."),
            ("05", "Mist, dome, tag",
             "One light mist, dome on, tag on the tray: variety, sow date, tray count, section. Then into the dark stack.",
             "An untagged tray cannot be traced to a sow date or to a client. Nothing leaves the room untagged."),
        ],
        pull="One tray, one tag, one sow date. The tag is the only thing that survives all the way to the punnet.",
        diagram="sow",
    ),
    dict(
        num="02", title="Blackout", when="Days 1–3", whensub="stacked, damp, dark",
        steps=[
            ("06", "Stack and weight",
             "Stack four high with a weight on top, or one dome per tray. The weight presses the roots down and pushes the stems up.",
             "No weight and the crop comes up wearing seed coats on every leaf."),
            ("07", "Keep it damp, not wet",
             "Lift the stack and mist two or three times a day. Damp to the back of the hand, never standing water.",
             "Standing water plus warmth is damping-off. It shows as a bald patch, never as a warning."),
            ("08", "Check it even",
             "By day three the tray is an even mat of pale stems. Patchy now is patchy at the cut.",
             "Slow varieties are not three-day trays. Beet, chard, basil, coriander and chives run longer — read the variety sheet."),
        ],
        pull="Three days of dark, then light. Not five, not one — and not the same three days for every variety.",
        diagram="stack",
        card=("When the stack goes wrong", "Three signs, and what each one is telling you", [
            ("A bald patch on one tray", "Seed went on thin, or the mist missed the middle. It will not fill in — cut around it and log the tray."),
            ("Grey fuzz, or a sour smell", "Too wet, too warm, or no air. Out of the room in a bag, sealed, and do not open it to look. Wipe the level it stood on."),
            ("Pale, stretched stems", "Too warm and too crowded. It still grows and it still sells, but it is a leggy tray — cut it early and note the temperature."),
        ]),
    ),
    dict(
        num="03", title="Into the light", when="Day 4 until cut", whensub="12–16 hours a day under LED",
        steps=[
            ("09", "Move it under the light",
             "Off the stack, under the tubes, canopy close. Twelve to sixteen hours a day colours the leaf without stretching the stem.",
             "The machine runs the lights 18 on, 6 off. The protocol says 12–16. Pick one, write it on the wall and hold it — do not split the difference."),
            ("10", "Water from below",
             "Sub-irrigation keeps the leaves dry, and dry leaves are the whole trick. Let the tray drink, then pour off what is left.",
             "Water on the canopy at this stage is a mould tray by Friday."),
            ("11", "Mist less as it closes",
             "Two or three times a day at first, less as the canopy fills. The room sits at 40–60 % humidity — let the room do half the work.",
             "A closed canopy holds its own moisture. Keep misting it and it rots from the middle out."),
            ("12", "The morning five",
             "Temperature, humidity, air, water, and anything growing that is not a microgreen. Written down, every morning, before anything else.",
             "18–24 °C and 40–60 % humidity. A still room in a warm week is a mould week."),
            ("13", "Read the variety, not the calendar",
             "Radish is cut at day 5 or 6. Basil takes 20 to 25. The tray tells you: full colour, first true leaf just showing, stem firm.",
             "Past the first true leaf most varieties lose the flavour you are charging for."),
        ],
        pull="Light makes the colour, air makes the stem, and the variety decides the day.",
        diagram="light",
    ),
    dict(
        num="04", title="Cut", when="Day 10–14", whensub="sharp, clean, weighed",
        steps=[
            ("14", "Cut clean, one pass",
             "Sharp scissors or a knife, 1–2 cm above the medium, one clean pass. Do not tear it and do not pull it.",
             "A torn stem bleeds and the punnet goes limp a day early. Change the blade, not the pressure."),
            ("15", "Weigh every tray",
             "Grams on the sheet, tray by tray. The model says 200–300 g a tray; the research average is 136 g. The room's own number is the only one that pays.",
             "An unweighed tray hides a thin crop until the invoice."),
            ("16", "Straight into the cold",
             "Into the cold room at 5 °C, covered, in the same hour it was cut. Not a warm tray on a bench, not even for a minute.",
             "Two hours on a bench is two days off the shelf life."),
        ],
        pull="Cut height is the yield. One centimetre higher is a punnet that looks full and weighs light.",
        diagram="cut",
        card=("A thin tray, and why", "Four things to check before you blame the seed", [
            ("The seed was weighed", "Grams on the scale, not a scoop. Half a tray of seed is half a tray of greens, every time."),
            ("The blackout was long enough", "Variety sheet, not habit. Beet, coriander and chives want days more than a brassica does."),
            ("The light hours held", "Twelve to sixteen, or the machine's eighteen — one setting, held for the whole cycle, not changed mid-tray."),
            ("The water came from below", "A tray that dried at the roots on day five never catches up. Weigh it anyway and write the number down."),
        ]),
    ),
    dict(
        num="05", title="Pack and send", when="Same day", whensub="cold from the bench to the door",
        steps=[
            ("17", "Pack, weigh, label",
             "100 g clear clamshell for retail; 250 g or 500 g food-grade bag for wholesale. Variety, weight, harvest date and batch code on every one.",
             "The batch code is the same code that was on the tray. If it is not, the trail stops at the pack bench."),
            ("18", "Cold to the door",
             "Cold room to client in under two hours, insulated bag, ice pack. Tuesday and Friday harvests leave the same day.",
             "An hour in a warm car undoes the cold room."),
        ],
        pull="Five to seven days in a fridge. One day in a warm car.",
        diagram="cold",
        card=("Clear and clean, the same afternoon", "A tray that is cut is a tray that is washed before the room closes", [
            ("The spent tray goes out", "Medium and roots to compost, mat to the bin, and out of the room — never beside the rack."),
            ("The tray is washed", "Washed, sanitised, rinsed, dried upside down, and back on the rack in its place."),
            ("The level is wiped", "Shelf wiped, floor swept, and anything mouldy out of the room the same hour it was found."),
            ("The room is shut down properly", "Lights off, fans on their cycle, tank checked, door closed. The next shift starts from a clean room or it starts behind."),
        ]),
    ),
]

# variety reference: seed rate per 10x20 tray, soak, blackout, days to cut
# (Bootstrap Farmer cheat sheet — trade practice)
VARIETIES = [
    ("Fast · cut in 5–12 days", [
        ("Radish (Daikon, Sango)", "30–35 g", "none", "2–3 d", "5–12", "Peak crunch at day 5–6"),
        ("Kale (Vates, Red Russian)", "15–20 g", "none", "2–3 d", "6–10", "Base green for a salad"),
        ("Kohlrabi (Purple Vienna)", "15–20 g", "none", "2–3 d", "6–10", "Purple stems, cheap seed"),
        ("Mustard, mizuna", "10–15 g", "none", "3–5 d", "8–12", "Spicy; runs cooler"),
        ("Broccoli", "15–20 g", "none", "2–3 d", "8–12", "The easiest tray in the room"),
        ("Cabbage, pak choi", "15–20 g", "none", "2–3 d", "8–12", "Purple pak choi needs less light"),
        ("Cress, curled", "20 g", "none", "4–5 d", "8–12", "Mucilaginous — mist light, 3× a day"),
        ("Chia", "10–15 g", "none", "3–5 d", "8–12", "Mucilaginous — sow thin"),
        ("Buckwheat", "100 g", "4–8 h", "3–5 d", "8–12", "Rinse well, husks must come off"),
    ]),
    ("Medium · cut in 10–14 days", [
        ("Beetroot (Bulls Blood, Detroit)", "20–30 g", "4–8 h", "4–5 d", "10–14", "Harvest low to keep the red stem"),
        ("Swiss chard (all stems)", "20–30 g", "4–8 h", "4–5 d", "10–14", "Poor in hydroponics — soil tray"),
        ("Amaranth (Red Garnet)", "15 g", "none", "5–6 d", "12–14", "Wants warmth; burns in direct light"),
        ("Lettuce", "15–20 g", "none", "2–3 d", "10–12", "Petite; colour follows the light"),
        ("Sorrel, red-veined", "3 g", "none", "3–5 d", "10–12", "Expensive seed — sow sparse"),
        ("Fennel", "20–30 g", "none", "3–4 d + 2–3", "16–20", "Husks cling; grow it long enough"),
        ("Parsley", "15–20 g", "none", "4–5 d", "16+", "Slow to germinate, soil only"),
    ]),
    ("Slow · cut in 16–25 days", [
        ("Basil (Genovese, Dark Opal)", "10 g", "none", "4–7 d", "20–25", "Mucilaginous; keep it damp"),
        ("Coriander", "30–40 g", "2–4 h", "stack 7 d", "21–28", "Split seed germinates faster"),
        ("Chives, spring onion", "40–50 g", "none", "4 d + 2–3", "21", "Slow; can give a second cut"),
    ]),
    ("Heavy seed · soak first", [
        ("Pea shoots", "200–275 g", "6–12 h", "stack 3–5 d", "8–12", "Pre-sprout 12–24 h; 12 days max"),
        ("Sunflower (black oil)", "150 g", "6–12 h", "2–3 + 2–3", "8–12", "Pre-sprout 12–24 h; soil only"),
        ("Wheatgrass", "450 g", "4–8 h", "2 d", "8–10", "Juicing only; mould-prone, keep cool"),
    ]),
]

JOURNAL = [
    ("Sow", "5–6 trays", "every day, one in one out"),
    ("Stack, weight, mist", "the trays sown 1–3 days ago", "twice or three times a day"),
    ("Move to the light", "the trays that have finished blackout", "every morning"),
    ("Cut, weigh, pack", "the trays that are ready", "every morning, into the cold"),
    ("Clear and clean", "every tray cut that day", "straight after the cut"),
]

# PSU Extension measured yields, 10-15 g seed per tray, 2-week cycle
YIELDS = [
    ("Mustard (Red Rain)", 201, True), ("Hon Tsai Tai", 181, True), ("Mizuna", 176, True),
    ("Pac Choi", 170, True), ("Basil", 165, False), ("Persian cress", 164, True),
    ("Sorrel", 163, True), ("Kale (Russian)", 155, False), ("Arugula", 148, True),
    ("Kohlrabi (Purple)", 126, False), ("Radish (Daikon)", 122, False),
    ("Chinese cabbage (Kogane)", 120, False), ("Kale (Toscano)", 118, False),
    ("Tatsoi", 115, False), ("Shungiku", 114, False), ("Red cabbage", 106, False),
    ("Ruby red chard", 71, False), ("Cilantro", 47, False),
]

# ----------------------------------------------------------------------------
# small svg parts
# ----------------------------------------------------------------------------
def svg_rack(w=560, h=300):
    """Elevation of the 5-rack room: 5 racks x 4 tiers x 4 trays = 80 places."""
    out = [f'<svg viewBox="0 0 560 300" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Five racks of four tiers, four trays to a tier: eighty tray places">']
    w_rack, gap = 96, 14
    x0, y0, rack_h = 12, 40, 210
    for r in range(5):
        x = x0 + r * (w_rack + gap)
        out.append(f'<rect x="{x}" y="{y0}" width="{w_rack}" height="{rack_h}" fill="none" stroke="{PURPLE}" stroke-width="2.6"/>')
        for t in range(4):
            ty = y0 + 12 + t * 48
            out.append(f'<line x1="{x}" y1="{ty+34}" x2="{x+w_rack}" y2="{ty+34}" stroke="{PURPLE}" stroke-width="1.6" opacity=".45"/>')
            for c in range(4):
                tx = x + 6 + c * 21
                out.append(f'<rect x="{tx}" y="{ty+18}" width="18" height="14" fill="{LILAC}" stroke="{PURPLE}" stroke-width="1.1"/>')
                out.append(f'<line x1="{tx+3}" y1="{ty+13}" x2="{tx+15}" y2="{ty+13}" stroke="{CYAN}" stroke-width="2.6" opacity=".75"/>')
        out.append(f'<text x="{x+w_rack/2}" y="{y0+rack_h+20}" text-anchor="middle" font-family="Montserrat, Helvetica, sans-serif" font-size="10" font-weight="700" letter-spacing="0.12em" fill="{MID}">RACK {r+1}</text>')
    out.append(f'<line x1="12" y1="{y0+rack_h+34}" x2="548" y2="{y0+rack_h+34}" stroke="{PURPLE}" stroke-width="1" opacity=".35"/>')
    out.append('</svg>')
    return "".join(out)


def svg_cycle():
    """Day 0 to 14, one tray. Light runs to the cut; the cut window overlaps it."""
    W, H = 1080, 190
    x0, x1 = 24, W - 24
    span = 14.0
    scale = (x1 - x0) / span
    def px(d): return x0 + d * scale
    segs = [("Sow", 0, 1, CYAN, "#fff", "day 0"),
            ("Blackout", 1, 4, MID, "#fff", "days 1–3, dark, stacked"),
            ("Light", 4, 14, LILAC, PURPLE, "day 4 to the cut, 12–16 h a day")]
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="One tray takes fourteen days: sow day 0, blackout days 1 to 3, light from day 4, cut in a window from day 10 to 14">']
    for label, a, b, fill, txt, sub in segs:
        w = (b - a) * scale
        out.append(f'<rect x="{px(a):.1f}" y="24" width="{w:.1f}" height="58" fill="{fill}"/>')
        cx = px(a) + w / 2
        out.append(f'<text x="{cx:.1f}" y="50" text-anchor="middle" font-family="American Typewriter, Georgia, serif" '
                   f'font-size="17" font-weight="700" fill="{txt}">{label}</text>')
        out.append(f'<text x="{cx:.1f}" y="68" text-anchor="middle" font-family="Montserrat, Helvetica, sans-serif" '
                   f'font-size="10.5" fill="{txt}" opacity=".92">{sub}</text>')
    # the cut window bracket, days 10-14
    ya = 92
    out.append(f'<path d="M{px(10):.1f} {ya} L{px(10):.1f} {ya+14} L{px(14):.1f} {ya+14} L{px(14):.1f} {ya}" '
               f'fill="none" stroke="{PURPLE}" stroke-width="1.8"/>')
    out.append(f'<text x="{(px(10)+px(14))/2:.1f}" y="{ya+30}" text-anchor="middle" '
               f'font-family="American Typewriter, Georgia, serif" font-size="13" font-weight="700" fill="{PURPLE}">'
               f'the cut window</text>')
    out.append(f'<text x="{(px(10)+px(14))/2:.1f}" y="{ya+47}" text-anchor="middle" font-family="Montserrat, Helvetica, sans-serif" '
               f'font-size="10.5" fill="{MID}">day 10 to 14, by variety</text>')
    out.append(f'<line x1="{x0}" y1="160" x2="{x1}" y2="160" stroke="{PURPLE}" stroke-width="1.2" opacity=".5"/>')
    for d in (0, 1, 4, 10, 14):
        out.append(f'<line x1="{px(d):.1f}" y1="155" x2="{px(d):.1f}" y2="165" stroke="{PURPLE}" stroke-width="1.2"/>')
        out.append(f'<text x="{px(d):.1f}" y="180" text-anchor="middle" font-family="Montserrat, Helvetica, sans-serif" '
                   f'font-size="10.5" fill="{MID}">day {d}</text>')
    out.append('</svg>')
    return "".join(out)


def _box(x, y, w, h, fill="#fff", stroke=PURPLE, sw=2, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"/>'


def _lab(x, y, t, size=11, fill=None, anchor="start", weight="500", fam="Montserrat, Helvetica, sans-serif"):
    fill = fill or MID
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{t}</text>')


def diagram(kind):
    """Functional line drawings. No decoration: each one answers a question on the sheet."""
    if kind == "sow":
        return ('<svg viewBox="0 0 640 250" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A tray in section: medium, seed line, dome">'
                + _box(60, 150, 520, 46, "#fff") +
                f'<rect x="66" y="156" width="508" height="26" fill="{LILAC}"/>' +
                f'<line x1="66" y1="156" x2="574" y2="156" stroke="{CYAN}" stroke-width="5"/>' +
                _lab(60, 214, "10 × 20 in tray · medium level and firmed · seed broadcast to the edges") +
                f'<path d="M66 150 C66 60, 574 60, 574 150" fill="none" stroke="{MID}" stroke-width="2.4" stroke-dasharray="7 6"/>' +
                _lab(320, 96, "humidity dome, on until day 3", 12, MID, "middle") +
                f'<line x1="300" y1="156" x2="300" y2="120" stroke="{CYAN}" stroke-width="1.6"/>' +
                _lab(310, 132, "seed line — one even layer", 11, TEAL, "start") +
                f'<line x1="60" y1="196" x2="580" y2="196" stroke="{PURPLE}" stroke-width="1" opacity=".4"/>' +
                _lab(60, 236, "seed per tray, by variety: 3 g sorrel · 15–20 g brassica · 30–35 g radish · 200–275 g pea", 10.5, MID) +
                '</svg>')
    if kind == "stack":
        out = ['<svg viewBox="0 0 640 260" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Four trays stacked with a weight on top, under a dome">']
        for i in range(4):
            y = 200 - i * 38
            out.append(_box(160, y, 320, 30, "#fff", PURPLE, 2))
            out.append(f'<rect x="166" y="{y+5}" width="308" height="12" fill="{LILAC}"/>')
        out.append(_box(230, 36, 180, 26, PURPLE, PURPLE, 2))
        out.append(_lab(320, 54, "WEIGHT", 12, "#fff", "middle", "700"))
        out.append(f'<line x1="320" y1="62" x2="320" y2="86" stroke="{MID}" stroke-width="1.8"/>')
        out.append(f'<path d="M320 86 l-6 -9 l12 0 z" fill="{MID}"/>')
        out.append(_lab(320, 118, "four high, never more", 11.5, MID, "middle"))
        out.append(_lab(500, 196, "damp, not wet", 12, TEAL, "middle", "700"))
        out.append(_lab(500, 214, "mist 2–3× a day", 11, MID, "middle"))
        out.append(_lab(500, 230, "dark, 18–24 °C", 11, MID, "middle"))
        out.append(f'<line x1="452" y1="176" x2="480" y2="176" stroke="{TEAL}" stroke-width="1.6"/>')
        out.append(_lab(160, 252, "every tray in the stack carries its own tag — the stack is not a place to lose one", 10.5, MID))
        out.append('</svg>')
        return "".join(out)
    if kind == "light":
        out = ['<svg viewBox="0 0 640 250" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tray under an LED tube with a timer strip for lights, water and fans">']
        out.append(_box(90, 40, 300, 22, PURPLE, PURPLE, 2))
        out.append(_lab(240, 56, "LED TUBE", 11.5, "#fff", "middle", "700"))
        out.append(f'<line x1="240" y1="62" x2="240" y2="86" stroke="{CYAN}" stroke-width="1.4" stroke-dasharray="4 4"/>')
        out.append(_lab(250, 84, "canopy close", 10.5, TEAL))
        out.append(_box(120, 170, 240, 32, "#fff"))
        out.append(f'<rect x="126" y="176" width="228" height="14" fill="{LILAC}"/>')
        # canopy strokes
        for i in range(11):
            x = 132 + i * 20
            out.append(f'<path d="M{x} 176 q4 -26 2 -40" stroke="{CYAN}" stroke-width="2" fill="none"/>')
        out.append(_lab(120, 224, "water from below, leaves dry", 11, MID))
        # timer strips
        out.append(_lab(420, 110, "THE MACHINE", 10, MID, "start", "700"))
        strips = [("lights", "18 h on · 6 h off", 40, CYAN),
                  ("pump", "10 min at 08:00 and 16:00", 30, MID),
                  ("fans", "10 min in every 30", 20, TEAL)]
        for i, (name, txt, n, col) in enumerate(strips):
            y = 128 + i * 44
            out.append(_lab(420, y, name, 10.5, PURPLE, "start", "700"))
            out.append(_lab(420, y + 13, txt, 10, MID))
            out.append(f'<line x1="420" y1="{y+22}" x2="{420+n*2.4}" y2="{y+22}" stroke="{col}" stroke-width="5"/>')
        out.append('</svg>')
        return "".join(out)
    if kind == "cut":
        out = ['<svg viewBox="0 0 640 250" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cut height one to two centimetres above the medium">']
        out.append(_box(120, 170, 400, 34, "#fff"))
        out.append(f'<rect x="126" y="176" width="388" height="16" fill="{LILAC}"/>')
        for i in range(18):
            x = 132 + i * 21
            out.append(f'<path d="M{x} 176 q3 -44 1 -66" stroke="{CYAN}" stroke-width="2.2" fill="none"/>')
        out.append(f'<line x1="110" y1="120" x2="530" y2="120" stroke="{PURPLE}" stroke-width="2" stroke-dasharray="8 5"/>')
        out.append(_lab(530, 116, "cut line", 11, PURPLE, "end", "700"))
        out.append(f'<line x1="560" y1="170" x2="560" y2="120" stroke="{PURPLE}" stroke-width="1.4"/>')
        out.append(f'<line x1="552" y1="170" x2="568" y2="170" stroke="{PURPLE}" stroke-width="1.4"/>')
        out.append(f'<line x1="552" y1="120" x2="568" y2="120" stroke="{PURPLE}" stroke-width="1.4"/>')
        out.append(_lab(560, 150, "1–2 cm", 10.5, PURPLE, "middle", "700"))
        out.append(_lab(120, 226, "one clean pass, sharp blade — a torn stem is a punnet that goes limp early", 10.5, MID))
        out.append('</svg>')
        return "".join(out)
    if kind == "cold":
        out = ['<svg viewBox="0 0 640 200" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Same day cold chain: cut, pack, cold room, door, client">']
        labels = [("08:00", "cut"), ("09:00", "pack and weigh"), ("10:00", "cold room, 5 °C"),
                  ("13:00", "insulated bag"), ("same day", "client")]
        x = 30
        for i, (t, l) in enumerate(labels):
            out.append(_box(x, 60, 104, 52, "#fff"))
            out.append(_lab(x + 52, 82, t, 11.5, PURPLE, "middle", "700"))
            out.append(_lab(x + 52, 100, l, 9.5, MID, "middle"))
            if i < len(labels) - 1:
                out.append(f'<line x1="{x+104}" y1="86" x2="{x+126}" y2="86" stroke="{CYAN}" stroke-width="2.4"/>')
            x += 126
        out.append(_lab(30, 140, "under two hours from the cold room to the client; Tuesday and Friday harvests go out the same day", 10.5, MID))
        out.append(_lab(30, 162, "5–7 days in a fridge. One day in a warm car. The cold chain is the product.", 12, TEAL, "start", "700"))
        out.append('</svg>')
        return "".join(out)
    raise ValueError(kind)


# ----------------------------------------------------------------------------
# print sheets (A3)
# ----------------------------------------------------------------------------
SHEET_CSS = _sub("""
@page { size: 297mm 420mm; margin: 0; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #fff; color: %(P)s;
  font-family: Montserrat, "Helvetica Neue", Helvetica, Arial, sans-serif; }
.sheet { width: 297mm; height: 420mm; overflow: hidden; background: #fff;
  display: flex; flex-direction: column;
  page-break-after: always; break-after: page; }
.sheet:last-child { page-break-after: auto; break-after: auto; }

.band { flex: none; background: %(P)s; color: %(L)s; padding: 15mm 16mm 11mm; position: relative; }
.band .kicker { font-size: 8pt; letter-spacing: .32em; text-transform: uppercase; color: %(C)s; font-weight: 700; }
.band h1 { font-family: "American Typewriter", Georgia, serif; font-weight: 700; font-size: 52pt;
  line-height: .94; margin: 5mm 0 0; letter-spacing: -.02em; }
.band .when { margin-top: 5mm; font-size: 13pt; color: #C8B8E0; }
.band .when b { color: %(C)s; font-weight: 700; }
.band .num { position: absolute; right: 16mm; top: 10mm; font-family: "American Typewriter", Georgia, serif;
  font-size: 104pt; line-height: .8; color: %(C)s; font-weight: 700; }
.sheet.tight .band { padding-bottom: 8mm; }
.sheet.tight .band h1 { font-size: 40pt; }

.body { flex: 1 1 auto; min-height: 0; padding: 10mm 16mm 0; display: flex; flex-direction: column; }
.foot { flex: none; margin: 5mm 16mm 8mm; display: flex; justify-content: space-between;
  font-size: 7.5pt; letter-spacing: .14em; text-transform: uppercase; color: %(M)s;
  border-top: .4mm solid rgba(51,0,114,.22); padding-top: 3.5mm; }
.foot b { color: %(P)s; }

.plate { flex: none; background: #fff; border: .5mm solid rgba(51,0,114,.25); padding: 5mm 7mm 3.5mm; margin-bottom: 6mm; }
.plate svg { display: block; width: 100%; height: 58mm; margin: 0 auto; }
.plate.map svg { height: auto; max-height: 118mm; }
.plate .cap { font-size: 8.5pt; color: %(M)s; margin-top: 2mm; }

ol.steps { list-style: none; margin: 0; padding: 0; }
.step { display: grid; grid-template-columns: 17mm 1fr; gap: 5mm; padding: 4.4mm 0;
  border-bottom: .4mm solid rgba(51,0,114,.16); }
.step:first-child { padding-top: 0; }
.step:last-child { border-bottom: 0; }
.step .n { font-family: "American Typewriter", Georgia, serif; font-weight: 700; font-size: 21pt; color: %(C)s; line-height: 1; }
.step h2 { font-family: "American Typewriter", Georgia, serif; font-weight: 700; font-size: 18pt;
  line-height: 1.05; margin: 0 0 2.2mm; letter-spacing: -.01em; }
.step p { margin: 0; font-size: 12.5pt; line-height: 1.36; }
.step p.watch { margin-top: 1.6mm; font-size: 10.6pt; line-height: 1.3; color: %(M)s; }
.step p.watch b { color: %(T)s; }

.body.spread { justify-content: space-between; }
.body.spread .pull { margin: 0; }
.airy .plate svg { height: 84mm; }
.airy .step { padding: 6.2mm 0; }
.airy .step h2 { font-size: 21pt; }
.airy .step p { font-size: 14.2pt; }
.airy .step p.watch { font-size: 11.8pt; }
.airy .step .n { font-size: 24pt; }
.airy .stagecard { padding: 6mm 7mm; }
.airy .stagecard h3 { font-size: 15.5pt; }
.airy .stagecard li { font-size: 10.8pt; }
.stagecard { margin: 5mm 0 0; background: %(L)s; padding: 4.5mm 6mm; }
.stagecard .eyebrow { font-size: 7pt; letter-spacing: .24em; text-transform: uppercase; color: %(T)s; font-weight: 700; margin: 0 0 1.5mm; }
.stagecard h3 { font-family: "American Typewriter", Georgia, serif; font-size: 13.5pt; margin: 0 0 3mm; line-height: 1.1; }
.stagecard ul { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm 7mm; }
.stagecard li { font-size: 9.6pt; line-height: 1.35; }
.stagecard li b { color: %(P)s; }
.pull { margin: auto 0 4mm; padding: 4.5mm 7mm; border-left: 2mm solid %(C)s; background: %(L)s;
  font-family: "American Typewriter", Georgia, serif; font-size: 16pt; line-height: 1.3; color: %(P)s; }

table { border-collapse: collapse; width: 100%%; }
th { text-align: left; font-size: 7.5pt; letter-spacing: .14em; text-transform: uppercase; color: %(M)s;
  padding: 0 3mm 2mm 0; border-bottom: .7mm solid %(P)s; }
td { padding: 2.3mm 3mm 2.3mm 0; font-size: 10.5pt; border-bottom: .3mm solid rgba(51,0,114,.16); vertical-align: top; }
td.n { font-variant-numeric: tabular-nums; font-weight: 700; white-space: nowrap; }
tr.grp td { font-family: "American Typewriter", Georgia, serif; font-weight: 700; font-size: 11pt;
  color: %(C)s; background: rgba(230,223,237,.55); padding: 2.4mm 3mm; border-bottom: 0; letter-spacing: .01em; }
.note { font-size: 8.5pt; line-height: 1.45; color: %(M)s; margin-top: 4mm; }
.note b { color: %(P)s; }

.twocol { display: grid; grid-template-columns: 1fr 1fr; gap: 12mm; }
.whitecard { background: %(L)s; padding: 7mm 8mm; }
.whitecard .eyebrow { font-size: 7.5pt; letter-spacing: .28em; text-transform: uppercase; color: %(T)s; font-weight: 700; margin: 0 0 3mm; }
.whitecard h3 { font-family: "American Typewriter", Georgia, serif; font-size: 16pt; margin: 0 0 3mm; line-height: 1.1; }
.whitecard p, .whitecard li { font-size: 10.5pt; line-height: 1.42; margin: 0 0 2.2mm; }
.whitecard ol { margin: 0; padding-left: 5mm; }
""")


def sheet(i, total, title, body_html, foot_label, sheet_class=""):
    return (f'<section class="sheet{sheet_class}"><div class="band">'
            f'<p class="kicker">The Local Farmer · Microgreen room</p>{title}</div>'
            f'{body_html}'
            f'<div class="foot"><span><b>{foot_label}</b></span><span>Sheet {i} of {total}</span></div></section>')


def build_sheets():
    n = 8
    out = [f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f'<title>The microgreen process — TLF wall sheets</title>'
           f'<link rel="preconnect" href="https://fonts.googleapis.com">'
           f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           f'<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">'
           f'<style>{SHEET_CSS}</style></head><body>']

    # ---- sheet 1: the map
    s1 = f'''<div class="body">
      <p style="font-size:12.5pt;line-height:1.5;max-width:200mm;margin:0 0 7mm">{("Five stages, eighteen steps, ten to fourteen days. One stage to a sheet, on the wall where the work happens, in the order it happens.")}</p>
      <div style="display:flex;gap:10mm;margin:0 0 8mm;padding:5mm 0;border-top:.4mm solid rgba(255,255,255,.3);border-bottom:.4mm solid rgba(255,255,255,.3)">
        {''.join(f'<div style="flex:1"><div style="font-family:&quot;American Typewriter&quot;,Georgia,serif;font-size:23pt;color:{CYAN};font-weight:700;line-height:1;white-space:nowrap">{v}</div><div style="font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:#B9A9D6;margin-top:2mm">{k}</div></div>' for v,k in [("80","tray places"),("200–300 g","the model, a tray"),("136 g","the measured average"),("10–14","days to cut"),("5","stages")])}
      </div>
      <div class="plate map">{svg_rack()}<p class="cap">Five racks, four tiers, four trays to a tier: eighty places. One tray in and one tray out every day, so the room turns over once every twelve to fifteen days.</p></div>
      <p class="note" style="font-size:9pt;margin-bottom:7mm"><b>One tray in, one tray out.</b> Eighty places divided by a twelve-day cycle is six or seven trays a day; by a fifteen-day cycle, five. The growth model runs two cycles a month — a hundred and sixty trays. The sow log is what settles it.</p>
      <div class="twocol" style="margin-top:auto">
        <div class="whitecard"><p class="eyebrow">The five stages</p>
          <ol>
            <li><b>Set up and sow</b> — day 0, one tray at a time</li>
            <li><b>Blackout</b> — days 1–3, stacked, damp, dark</li>
            <li><b>Into the light</b> — day 4 until the cut</li>
            <li><b>Cut</b> — day 10–14, sharp, clean, weighed</li>
            <li><b>Pack and send</b> — same day, cold to the door</li>
          </ol></div>
        <div class="whitecard"><p class="eyebrow">The machine does three things</p>
          <p><b>Lights</b> 18 hours on, 6 off. <b>Pump</b> ten minutes at 08:00 and again at 16:00. <b>Fans</b> ten minutes in every thirty.</p>
          <p style="margin-bottom:0">The room runs at 18–24 °C and 40–60 % humidity. Everything else on these eight sheets is hands.</p></div>
      </div>
    </div>'''
    out.append(sheet(1, n,
        '<h1>The microgreen<br>process</h1><p class="when"><b>One tray, ten to fourteen days</b> · five stages, on the wall</p>'
        '<div class="num">01</div>', s1, "The map · sheets 1–8"))

    # ---- sheet 2: the cycle
    rows = "".join(f'<tr><td><b>{a}</b></td><td class="n">{b}</td><td>{c}</td></tr>' for a,b,c in JOURNAL)
    ymax = max(y for _, y, _ in YIELDS)
    ybars = "".join(
        f'<tr><td>{name}</td><td class="n">{g} g</td>'
        f'<td><span style="display:inline-block;height:3.2mm;width:{g/ymax*62:.1f}mm;background:{CYAN if g >= 150 else LILAC};border:.2mm solid {PURPLE}"></span></td></tr>'
        for name, g, fast in YIELDS)
    s2 = f'''<div class="body">
      <div class="plate">{svg_cycle()}<p class="cap">One tray from sow to cut. The clock starts when the seed goes down, not when it comes into the light.</p></div>
      <div class="twocol">
        <div>
          <p class="eyebrow" style="font-size:7.5pt;letter-spacing:.28em;text-transform:uppercase;color:{TEAL};font-weight:700;margin:0 0 3mm">The day, in five jobs</p>
          <table><thead><tr><th>Job</th><th>How many</th><th>When</th></tr></thead><tbody>{rows}</tbody></table>
          <p class="note">One person, every day, five things. A tray moves one step further down the line each day, so the same hands sow, mist, lift, cut and pack without ever doubling back.</p>
        </div>
        <div>
          <p class="eyebrow" style="font-size:7.5pt;letter-spacing:.28em;text-transform:uppercase;color:{TEAL};font-weight:700;margin:0 0 3mm">What a tray actually gives</p>
          <table><thead><tr><th>Green</th><th>Grams a tray</th><th></th></tr></thead><tbody>{ybars}</tbody></table>
          <p class="note">Measured at Penn State over 14 to 28 cycles a tray, ten to fifteen grams of seed, two weeks, no supplemental light: <b>136 g average, 47 to 201 g</b>. Bar marked in cyan is over 150 g. The growth model carries 200–300 g a tray — that is the number to beat, not the number to plan on until the room has weighed fifty trays.</p>
        </div>
      </div>
    </div>'''
    out.append(sheet(2, n,
        '<h1>The cycle,<br>one tray</h1><p class="when"><b>Day 0 to day 14</b> · and what a tray is worth in grams</p>'
        '<div class="num">02</div>', s2, "The cycle · one tray in, one tray out"))

    # ---- sheets 3-7: stages
    for idx, st in enumerate(STAGES):
        steps = "".join(
            f'<li class="step"><span class="n">{a}</span><div><h2>{b}</h2><p>{c}</p>'
            f'<p class="watch"><b>Watch</b> · {d}</p></div></li>' for a,b,c,d in st["steps"])
        card = ""
        if st.get("card"):
            eyebrow, ctitle, items = st["card"]
            lis = "".join(f'<li><b>{a}</b> · {b}</li>' for a, b in items)
            card = (f'<div class="stagecard"><p class="eyebrow">{eyebrow}</p>'
                    f'<h3>{ctitle}</h3><ul>{lis}</ul></div>')
        airy = " airy" if len(st["steps"]) <= 3 else ""
        body = (f'<div class="body spread"><div class="plate">{diagram(st["diagram"])}</div>'
                f'<ol class="steps">{steps}</ol>{card}'
                f'<p class="pull">{st["pull"]}</p></div>')
        title = (f'<h1>{st["title"]}</h1><p class="when"><b>{st["when"]}</b> · {st["whensub"]}</p>'
                 f'<div class="num">{st["num"]}</div>')
        out.append(sheet(3+idx, n, title, body, f'{st["title"]} · steps {st["steps"][0][0]}–{st["steps"][-1][0]}', airy))

    # ---- sheet 8: varieties
    vrows = []
    for group, items in VARIETIES:
        vrows.append(f'<tr class="grp"><td colspan="6">{group}</td></tr>')
        for name, seed, soak, dark, days, note in items:
            vrows.append(f'<tr><td><b>{name}</b></td><td class="n">{seed}</td><td>{soak}</td>'
                         f'<td class="n">{dark}</td><td class="n">{days}</td><td>{note}</td></tr>')
    s8 = f'''<div class="body">
      <p style="font-size:10.5pt;line-height:1.45;margin:0 0 5mm;max-width:230mm">Seed rate is grams of dry seed for one 10 × 20 inch tray. Soak is before sowing. Blackout is days in the dark, stacked or domed. Days is sow to cut. Where a variety is not on this sheet it has not been grown here yet — write its line in by hand and the sheet stays true.</p>
      <table>
        <thead><tr><th style="width:52mm">Variety</th><th style="width:26mm">Seed a tray</th><th style="width:26mm">Soak</th><th style="width:24mm">Blackout</th><th style="width:20mm">Days</th><th>Note</th></tr></thead>
        <tbody>{''.join(vrows)}</tbody>
      </table>
      <p class="note">Rates, soaks and blackout days are trade practice from the Bootstrap Farmer cheat sheet, not yet measured in this room — treat them as the starting point and overwrite them with what the trays do. Seed rate sanity-checks against Penn State Extension, who sow <b>10–15 g</b> a tray for the brassicas and get 47–201 g back. Heavy seed — pea, sunflower, wheatgrass — is weighed, not counted: it is ten to twenty times the brassica rate.</p>
    </div>'''
    out.append(sheet(8, n,
        '<h1>The variety<br>sheet</h1><p class="when"><b>Twenty-two greens</b> · rate, soak, blackout, days</p>'
        '<div class="num">08</div>', s8, "Reference · the variety sheet", " tight"))

    out.append("</body></html>")
    (OUT/"tlf-microgreen-wall-sheets.html").write_text("".join(out))
    return OUT/"tlf-microgreen-wall-sheets.html"


# ----------------------------------------------------------------------------
# A4 forms
# ----------------------------------------------------------------------------
FORM_CSS = _sub("""
@page { size: 210mm 297mm; margin: 0; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #fff; color: %(P)s;
  font-family: Montserrat, "Helvetica Neue", Helvetica, Arial, sans-serif; }
.sheet { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; padding: 12mm 12mm 0; }
.sheet:last-child { page-break-after: auto; }
.head { border-bottom: .7mm solid %(P)s; padding-bottom: 4mm; margin-bottom: 6mm; display: flex; justify-content: space-between; align-items: flex-end; }
.head .kicker { font-size: 6.8pt; letter-spacing: .3em; text-transform: uppercase; color: %(T)s; font-weight: 700; margin: 0 0 2mm; }
.head h1 { font-family: "American Typewriter", Georgia, serif; font-size: 24pt; margin: 0; line-height: 1; letter-spacing: -.01em; }
.head .tag { font-size: 6.8pt; letter-spacing: .14em; text-transform: uppercase; color: %(M)s; text-align: right; }
.head .tag b { color: %(C)s; font-size: 15pt; font-family: "American Typewriter", Georgia, serif; display: block; letter-spacing: 0; }
.sub { font-size: 8.6pt; color: %(M)s; line-height: 1.4; margin: 0 0 4mm; }
table { border-collapse: collapse; width: 100%%; }
th { font-size: 6.6pt; letter-spacing: .12em; text-transform: uppercase; color: %(M)s; text-align: left;
  padding: 0 2mm 1.6mm; border-bottom: .5mm solid %(P)s; font-weight: 700; }
td { border: .25mm solid rgba(51,0,114,.32); border-left: 0; border-right: 0; height: 12.4mm; padding: 1.5mm 2mm; font-size: 9pt; }
table.grided td { border: .25mm solid rgba(51,0,114,.32); }
.checkbox { display: inline-block; width: 4.2mm; height: 4.2mm; border: .35mm solid %(P)s; vertical-align: -0.6mm; }
.foot { position: absolute; left: 12mm; right: 12mm; bottom: 9mm; display: flex; justify-content: space-between;
  font-size: 6.6pt; letter-spacing: .14em; text-transform: uppercase; color: %(M)s;
  border-top: .3mm solid rgba(51,0,114,.3); padding-top: 3mm; }
.box { border: .35mm solid rgba(51,0,114,.5); padding: 4mm 5mm; }
.notes { margin-top: 5mm; border: .35mm solid rgba(51,0,114,.5); padding: 4mm 5mm 2mm; }
.notes .lab { font-size: 6.8pt; letter-spacing: .14em; text-transform: uppercase; color: %(M)s; margin-bottom: 2.5mm; }
.notes .line { height: 8.4mm; border-bottom: .25mm solid rgba(51,0,114,.32); }
.hint { font-size: 7.6pt; color: %(M)s; line-height: 1.4; }
""")


def form(i, total, kicker, title, tag, tagline, body, foot):
    return (f'<section class="sheet"><div class="head"><div><p class="kicker">{kicker}</p><h1>{title}</h1></div>'
            f'<div class="tag">{tagline}<b>{tag}</b></div></div>{body}'
            f'<div class="foot"><span><b>{foot}</b></span><span>Form {i} of {total} · The Local Farmer</span></div></section>')


def build_forms():
    n = 4
    out = [f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f'<title>The microgreen grow room — TLF forms</title>'
           f'<link rel="preconnect" href="https://fonts.googleapis.com">'
           f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           f'<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">'
           f'<style>{FORM_CSS}</style></head><body>']

    # 1 — the morning check (laminate, one a week)
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    checks = [
        ("Temperature", "18–24 °C, read at tray height"),
        ("Humidity", "40–60 %, and the room feels damp not wet"),
        ("Air", "fans running, 10 minutes in every 30"),
        ("Water", "tank level, pump wet, no standing water in a tray"),
        ("Anything that is not a microgreen", "mould, flies, a sour smell, a bald tray"),
    ]
    rows = "".join(
        f'<tr><td style="width:52mm"><b>{a}</b><div class="hint">{b}</div></td>'
        + "".join('<td style="text-align:center"><span class="checkbox"></span></td>' for _ in days) + '</tr>'
        for a,b in checks)
    body1 = f'''<p class="sub">Five things, every morning, before anything else. Hang it by the door and mark it with a dry-wipe pen — one sheet does a week, wipe it on Sunday night. A skipped day costs a tray three weeks from now.</p>
      <table class="grided"><thead><tr><th>Check</th>{''.join(f'<th style="text-align:center;width:15mm">{d}</th>' for d in days)}</tr></thead><tbody>{rows}</tbody></table>
      <div class="box" style="margin-top:6mm"><div class="hint" style="margin-bottom:2mm"><b style="color:{PURPLE}">Write the two numbers down</b> — the thermometer and the hygrometer, once a day. The controller log is not the room.</div>
        <table class="grided"><thead><tr><th>Reading</th>{''.join(f'<th style="text-align:center;width:15mm">{d}</th>' for d in days)}</tr></thead>
        <tbody><tr><td style="width:52mm">°C at tray height</td>{''.join('<td></td>' for _ in days)}</tr>
        <tr><td>% humidity</td>{''.join('<td></td>' for _ in days)}</tr></tbody></table></div>
      <div class="notes"><div class="lab">Notes — what changed, and what you did about it</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
      <div class="box" style="margin-top:5mm"><div class="hint"><b style="color:{PURPLE}">If it is wrong today:</b> mould in one tray — out of the room in a bag, do not open it to look; a bald patch — check the mist and the warmth; a still room — fans before heat, always.</div></div>'''
    out.append(form(1, n, "The Local Farmer · microgreen room", "The morning check", "FORM 01", "five things · every day", body1, "The morning check"))

    # 2 — sow log
    sow_rows = "".join(
        '<tr><td style="width:20mm"></td><td></td><td style="width:16mm"></td><td style="width:20mm"></td><td style="width:18mm"></td><td style="width:24mm"></td><td></td></tr>'
        for _ in range(14))
    body2 = f'''<p class="sub">One line a sowing. Variety, how many trays, and which section they went into — stock order, scheduled growth, or ad hoc. The blackout-out date is the day the stack comes apart; count it forward from the sow date by the variety sheet, not by habit.</p>
      <table class="grided"><thead><tr><th>Sow date</th><th>Variety</th><th>Trays</th><th>Section</th><th>Grams seed</th><th>Out of blackout</th><th>Initials</th></tr></thead><tbody>{sow_rows}</tbody></table>
      <div class="box" style="margin-top:5mm"><div class="hint"><b style="color:{PURPLE}">Sections:</b> SO stock order · SG scheduled growth · AH ad hoc. Every tray carries its tag from this line — variety, sow date, tray count — and the tag travels to the punnet.</div></div>'''
    out.append(form(2, n, "The Local Farmer · microgreen room", "The sow log", "FORM 02", "one line a sowing", body2, "Sow log · fortnight sheet"))

    # 3 — harvest and dispatch
    harv_rows = "".join(
        '<tr><td style="width:18mm"></td><td></td><td style="width:13mm"></td><td style="width:17mm"></td>'
        '<td style="width:26mm"></td><td style="width:22mm"></td><td style="width:19mm"></td><td></td></tr>'
        for _ in range(14))
    body3 = f'''<p class="sub">Cut, weighed, packed, out. The grams are the number the room lives on — the model says 200–300 g a tray and the research average is 136 g, so the only figure worth arguing about is this column.</p>
      <table class="grided"><thead><tr><th>Date</th><th>Variety</th><th>Trays</th><th>Total g</th><th>g a tray</th><th>Packed as</th><th>Batch code</th><th>To</th></tr></thead><tbody>{harv_rows}</tbody></table>
      <div class="box" style="margin-top:5mm"><div class="hint"><b style="color:{PURPLE}">Packed as:</b> 100 g clamshell · 250 g bag · 500 g bag. <b style="color:{PURPLE}">Cold:</b> in the cold room inside the hour, 5 °C, covered. <b style="color:{PURPLE}">Out:</b> under two hours door to door, Tuesday and Friday harvests the same day.</div></div>
      <div class="box" style="margin-top:4mm"><div class="hint"><b style="color:{PURPLE}">Clear and clean, the same afternoon:</b> spent tray out — medium and roots to compost, mat to the bin, never beside the rack · tray washed, sanitised, dried upside down · level wiped · floor swept · anything mouldy gone from the room.</div></div>'''
    out.append(form(3, n, "The Local Farmer · microgreen room", "Harvest and dispatch", "FORM 03", "cut · weigh · pack · send", body3, "Harvest and dispatch"))

    # 4 — weekly deep clean
    items = [
        ("Racks and shelves", "Wipe every level, top to bottom, sanitiser then dry"),
        ("Trays and domes", "Every tray in the room washed and sanitised, not only the empty ones"),
        ("Lights", "Dust off the tubes — a dusty tube is a dim tray"),
        ("Fans and filters", "Grilles off, washed, dried, back on"),
        ("Floor and drains", "Sweep, wash, sanitiser down the drain"),
        ("Walls and door handles", "Wipe down to shoulder height"),
        ("Water tank", "Drain, scrub, refill, check the float switches"),
        ("Tools", "Scissors, knives, press, harvest board — washed and sharpened"),
        ("Cold room", "Wipe shelves, check the temperature against the thermometer"),
        ("Packaging", "Count stock, check labels and batch-code pen"),
        ("Seed store", "Closed, dry, labelled, nothing open on the bench"),
        ("Waste out", "Green waste off the property, not in the yard bin"),
    ]
    clean_rows = "".join(
        f'<tr><td style="width:6mm"><span class="checkbox"></span></td><td style="width:52mm"><b>{a}</b></td>'
        f'<td>{b}</td><td style="width:18mm"></td><td style="width:14mm"></td></tr>' for a,b in items)
    body4 = f'''<p class="sub">Once a week, the whole room, in this order — top down, dry to wet, and the waste last. Daily is the floor, the bench and the tools. Sign the week off at the bottom: an unsigned clean is a clean nobody did.</p>
      <table class="grided"><thead><tr><th></th><th>What</th><th>How</th><th>Done</th><th>Init.</th></tr></thead><tbody>{clean_rows}</tbody></table>
      <div class="notes"><div class="lab">Anything found, and what was done</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
      <div class="box" style="margin-top:4mm"><div class="hint"><b style="color:{PURPLE}">Week of</b> __________________ &nbsp;·&nbsp; <b style="color:{PURPLE}">Deep clean done by</b> __________________ &nbsp;·&nbsp; <b style="color:{PURPLE}">Checked by</b> __________________</div></div>'''
    out.append(form(4, n, "The Local Farmer · microgreen room", "The weekly clean", "FORM 04", "once a week · top down", body4, "Weekly deep clean"))

    out.append("</body></html>")
    (OUT/"tlf-microgreen-grow-room-forms.html").write_text("".join(out))
    return OUT/"tlf-microgreen-grow-room-forms.html"


# ----------------------------------------------------------------------------
# web page
# ----------------------------------------------------------------------------
def build_web():
    css = _sub("""
:root { --purple:%(P)s; --cyan:%(C)s; --lilac:%(L)s; --mid:%(M)s; --teal:%(T)s; }
* { box-sizing: border-box; }
body { margin:0; background:#fff; color:var(--purple);
  font-family: Montserrat, "Helvetica Neue", Helvetica, Arial, sans-serif; -webkit-font-smoothing:antialiased; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 28px; }
.kicker { font-size: 11px; letter-spacing: .32em; text-transform: uppercase; color: var(--cyan); font-weight: 700; margin: 0 0 18px; }
.hero { background: var(--purple); color: var(--lilac); padding: 76px 0 54px; }
.hero h1 { font-family: "American Typewriter", Georgia, serif; font-size: clamp(46px, 7.4vw, 92px); line-height: .94;
  letter-spacing: -.03em; margin: 0 0 26px; color: #fff; font-weight: 700; }
.hero .lede { font-size: 20px; line-height: 1.45; max-width: 44ch; color: #D9CEEA; margin: 0 0 34px; }
.hero .meta { display:flex; flex-wrap:wrap; gap: 26px 40px; justify-content: space-between; padding-top: 22px; border-top: 1px solid rgba(255,255,255,.28); }
.hero .meta span { flex: 1 1 0; min-width: 140px; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: #B9A9D6; }
.hero .meta b { display:block; font-family:"American Typewriter",Georgia,serif; font-size: 30px; letter-spacing:-.01em; color: var(--cyan); margin-bottom: 4px; }
section { padding: 54px 0; }
.eyebrow { font-size: 11px; letter-spacing:.3em; text-transform:uppercase; color: var(--teal); font-weight:700; margin:0 0 16px; }
h2.big { font-family:"American Typewriter",Georgia,serif; font-size: clamp(28px,3.4vw,42px); line-height:1.06; margin:0 0 14px; letter-spacing:-.02em; }
.sub { font-size: 17px; line-height:1.6; color:#4A3A66; max-width: 68ch; margin: 0 0 28px; }
.plate { border:1px solid rgba(51,0,114,.22); padding: 18px 20px 12px; background:#fff; }
.plate svg { display:block; width:100%; height:auto; }
.plate figcaption { font-size: 13px; color: var(--mid); margin-top: 10px; line-height:1.5; }
.cards { display:grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap: 18px; }
.card { background: var(--lilac); padding: 24px 26px; }
.card h3 { font-family:"American Typewriter",Georgia,serif; font-size: 20px; margin:0 0 10px; }
.card p { font-size: 14.5px; line-height:1.55; margin:0; }
table { border-collapse: collapse; width: 100%%; }
th { text-align:left; font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--mid);
  padding: 0 12px 8px 0; border-bottom: 2px solid var(--purple); }
td { padding: 9px 12px 9px 0; font-size: 14.5px; border-bottom:1px solid rgba(51,0,114,.14); vertical-align: top; }
td.n { font-variant-numeric: tabular-nums; font-weight:700; white-space:nowrap; }
.stage { border-top: 1px solid rgba(51,0,114,.2); }
.stage .grid { display:grid; grid-template-columns: 210px 1fr; gap: 34px; align-items:start; }
.stage .num { font-family:"American Typewriter",Georgia,serif; font-size: 46px; color: var(--cyan); line-height:1; font-weight:700; }
.stage h2 { font-family:"American Typewriter",Georgia,serif; font-size: 34px; margin: 2px 0 8px; letter-spacing:-.02em; line-height:1.05; }
.stage .when { font-size: 13px; color: var(--mid); margin:0; }
.stage .when b { color: var(--teal); }
ol.steps { list-style:none; margin: 0; padding:0; }
.step { display:grid; grid-template-columns: 34px 1fr; gap: 16px; padding: 18px 0; border-bottom:1px solid rgba(51,0,114,.14); }
.step:last-child { border-bottom:0; }
.step .n { font-family:"American Typewriter",Georgia,serif; font-weight:700; color: var(--cyan); font-size: 17px; padding-top: 3px; }
.step h3 { font-family:"American Typewriter",Georgia,serif; font-size: 20px; margin:0 0 6px; }
.step p { margin:0; font-size: 15.5px; line-height:1.55; }
.step p.watch { margin-top: 7px; font-size: 13.5px; color: var(--mid); }
.step p.watch b { color: var(--teal); }
.pull { margin: 22px 0 0; padding: 20px 24px; border-left: 4px solid var(--cyan); background: var(--lilac);
  font-family:"American Typewriter",Georgia,serif; font-size: 21px; line-height:1.35; }
.pack { background: var(--purple); color: var(--lilac); padding: 54px 0; }
.pack h2 { color:#fff; font-family:"American Typewriter",Georgia,serif; font-size: 34px; margin:0 0 12px; }
.pack p { color:#D9CEEA; font-size:16px; line-height:1.6; max-width: 70ch; }
.pack a { color: var(--cyan); text-decoration:none; border-bottom:1px solid var(--cyan); }
.foot { padding: 34px 0 60px; font-size: 13px; color: var(--mid); line-height:1.6; }
.foot ul { margin: 10px 0 0; padding-left: 18px; }
.foot li { margin-bottom: 8px; }
""")

    def stage_html(i, st):
        steps = "".join(f'<li class="step"><span class="n">{a}</span><div><h3>{b}</h3><p>{c}</p>'
                        f'<p class="watch"><b>Watch</b> · {d}</p></div></li>' for a,b,c,d in st["steps"])
        return (f'<section class="stage" id="stage-{st["num"]}"><div class="wrap"><div class="grid">'
                f'<div><div class="num">{st["num"]}</div><h2>{st["title"]}</h2>'
                f'<p class="when"><b>{st["when"]}</b> · {st["whensub"]}</p></div>'
                f'<div><ol class="steps">{steps}</ol><p class="pull">{st["pull"]}</p></div>'
                f'</div></div></section>')

    journal = "".join(f'<tr><td><b>{a}</b></td><td class="n">{b}</td><td>{c}</td></tr>' for a,b,c in JOURNAL)
    vrows = []
    for group, items in VARIETIES:
        vrows.append(f'<tr><td colspan="5" style="background:var(--lilac);font-family:\'American Typewriter\',Georgia,serif;font-weight:700;padding:9px 12px">{group}</td></tr>')
        for name, seed, soak, dark, days, note in items:
            vrows.append(f'<tr><td><b>{name}</b><br><span style="color:var(--mid);font-size:13px">{note}</span></td>'
                         f'<td class="n">{seed}</td><td>{soak}</td><td class="n">{dark}</td><td class="n">{days}</td></tr>')

    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The microgreen process, step by step — The Local Farmer</title>
<meta name="description" content="Eighteen steps of the TLF microgreen process: sow, three days of blackout, ten days under light, cut, weigh, pack and send. Every rate and every day written out.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <p class="kicker">The Local Farmer · microgreen room</p>
  <h1>The microgreen<br>process</h1>
  <p class="lede">Five stages, eighteen steps, ten to fourteen days a tray. Every rate and every day written out — for the wall, where the work happens.</p>
  <div class="meta"><span><b>80</b>tray places</span><span><b>10–14</b>days to cut</span><span><b>136 g</b>a tray, measured</span><span><b>5 °C</b>the cold room</span><span><b>5–7</b>days of shelf life</span></div>
</div></header>

<section><div class="wrap">
  <p class="eyebrow">One tray, in days</p>
  <figure class="plate" style="margin:0">{svg_cycle()}
  <figcaption>One tray from sow to cut. The clock starts when the seed goes down, not when it comes into the light — and the variety, not the calendar, decides the day.</figcaption></figure>
</div></section>

<section><div class="wrap" style="padding-top:0">
  <div class="cards">
    <div class="card"><h3>What the room gives</h3><p>Five racks, four tiers, four trays to a tier: eighty places. One tray in and one tray out every day. The growth model runs two cycles a month — 160 trays — and carries 200–300 g a tray.</p></div>
    <div class="card"><h3>What the research says</h3><p>Penn State measured 136 g a tray on average across 18 greens and 14 to 28 cycles, on 10–15 g of seed: 47 g for coriander at the floor, 201 g for Red Rain mustard at the top.</p></div>
    <div class="card"><h3>What the machine does</h3><p>Lights 18 hours on, 6 off. Pump 10 minutes at 08:00 and again at 16:00. Fans 10 minutes in every 30. Room 18–24 °C and 40–60 % humidity. The rest is hands.</p></div>
  </div>
</div></section>

<section style="background:var(--lilac)"><div class="wrap">
  <p class="eyebrow">The day, in five jobs</p>
  <h2 class="big">One person, every day, five things</h2>
  <p class="sub">A tray moves one step further down the line each day, so the same hands sow, mist, lift, cut and pack without ever doubling back. Miss a day and it is not one tray you lose — it is the whole line that stops moving.</p>
  <table><thead><tr><th>Job</th><th>How many</th><th>When</th></tr></thead><tbody>{journal}</tbody></table>
</div></section>

{''.join(stage_html(i, st) for i, st in enumerate(STAGES))}

<section style="background:var(--lilac)"><div class="wrap">
  <p class="eyebrow">Reference</p>
  <h2 class="big">Twenty-two greens, one sheet</h2>
  <p class="sub">Grams of dry seed for one 10 × 20 inch tray, whether it wants a soak, days in the dark, and days from sow to cut. Rates and blackout days are trade practice, not yet measured in this room: start here, then overwrite them with what the trays do.</p>
  <table><thead><tr><th>Variety</th><th>Seed a tray</th><th>Soak</th><th>Blackout</th><th>Days</th></tr></thead><tbody>{''.join(vrows)}</tbody></table>
</div></section>

<div class="pack"><div class="wrap">
  <h2>On the wall and on the clipboard</h2>
  <p>The whole process is printed as eight A3 sheets for the grow room, and the four daily forms are on A4. Laminated at the bench, they take a dry-wipe pen; printed on the clipboard, they take a pencil.</p>
  <p style="margin-top:22px">
    <a href="the-microgreen-process-sheets.pdf">The eight wall sheets (PDF, A3)</a> &nbsp;·&nbsp;
    <a href="the-microgreen-grow-room-forms.pdf">The four forms (PDF, A4)</a>
  </p>
</div></div>

<div class="foot"><div class="wrap">
  <b>Where the numbers come from</b>
  <ul>
    <li><b>The TLF franchise model brief</b> — eighty tray places on five racks, two cycles a month, 200–300 g a tray, a 10–14 day cycle, 5–10 cm at the cut, 18–24 °C, 40–60 % humidity, the 100 g clamshell and the 250/500 g bag, cold pack the same day, 5–7 days of shelf life.</li>
    <li><b>The TLF grow machine spec</b> (MAMI / ACDC build) — lights 18 on and 6 off, the pump at 08:00 and 16:00 for ten minutes, fans ten minutes in every thirty.</li>
    <li><b>Penn State Extension, <i>Growing Microgreens</i></b> — 10–15 g of seed a tray, 136 g average yield with the full per-crop table, harvest at 1.5–3 inches, damping-off as the one real disease, sub-irrigation, and 41 °F storage holding 10–14 days against 2–4 at room temperature.</li>
    <li><b>The Bootstrap Farmer microgreen cheat sheet</b> — the per-variety seeding rates, soak times, blackout days and days to cut used on the variety sheet. Trade practice, not a trial result.</li>
  </ul>
  <p style="margin-top:18px"><b>One conflict left open on purpose.</b> The machine runs the lights 18 hours on and 6 off; the growing protocol says 12–16 hours. Both are in the record and they are not the same instruction. Pick one, run it for a full cycle, and write the result on the wall sheet — until then the pack tells the truth about the disagreement instead of hiding it.</p>
</div></div>
</body></html>'''
    (OUT/"tlf-microgreen-process-steps.html").write_text(page)
    return OUT/"tlf-microgreen-process-steps.html"


if __name__ == "__main__":
    for f in (build_web(), build_sheets(), build_forms()):
        print(f, f.stat().st_size)
