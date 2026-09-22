#!/usr/bin/env python3
"""Baut 'Rationale Zahlen 1 – Zahlen unter Null – ALLES.html' (Klasse 7c, Doppelstunde).

Alles in einer Datei: Verlauf, Tafelbild, Merkheft, Aufgaben, Lösungen.
Änderungen: hier im Skript, dann `python3 baue_stunde1.py`. PDF gibt es nur von den Folien (die sehen die Schüler):
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="Folien – Zahlen unter Null.pdf" "Folien – Zahlen unter Null.html"
Zahlengeraden sind SVG mit eigenem Karo (1 Kästchen = 20 px = 5 mm im Heft),
damit die Einteilung wie im Heft aufs Kästchen aufgeht.
"""
from pathlib import Path

K = 20
NEG, POS, INK, MUT = "#b3261e", "#1a56a0", "#1b1b1b", "#5a5a5a"
_uid = [0]


def num(v, plus=True):
    if isinstance(v, str):
        return v
    v = round(v, 6)
    t = f"{abs(v):g}".replace(".", ",")
    if v < 0:
        return "−" + t
    if v > 0 and plus:
        return "+" + t
    return t


def frac(a, b):
    return f'<span class="frac"><span>{a}</span><span class="u">{b}</span></span>'


def stift(g=16):
    return (f'<svg class="stift" viewBox="0 0 24 24" width="{g}" height="{g}" '
            'xmlns="http://www.w3.org/2000/svg"><path d="M3 21 L4.8 16.2 L16 5 L19 8 L7.8 19.2 Z" '
            'fill="none" stroke="#1b1b1b" stroke-width="1.9" stroke-linejoin="round"/>'
            '<path d="M14 7 L17 10" stroke="#1b1b1b" stroke-width="1.9"/></svg>')


def marke(v, *txt, lvl=0, anker="middle", unten=False):
    return dict(v=v, txt=list(txt) if txt else [num(v)], lvl=lvl, anker=anker, unten=unten)


def gerade(von, bis, schritt=1, kpe=2, teile=1, lab=1, marken=()):
    """Zahlengerade auf Karo. von/bis liegen auf Hauptstrichen, schritt = Wert je Hauptstrich,
    kpe = Kästchen je Hauptstrich, teile = Unterteilung, lab = jeder wievielte Strich beschriftet."""
    _uid[0] += 1
    uid = _uid[0]
    pad = 2
    n = round((bis - von) / schritt)
    W = (2 * pad + n * kpe) * K

    def X(v):
        return (pad + (v - von) / schritt * kpe) * K

    for m in marken:
        assert von - 1e-9 <= m["v"] <= bis + 1e-9, (m, von, bis)
    oben = [m for m in marken if not m["unten"]]
    unt = [m for m in marken if m["unten"]]
    zeilen = max([len(m["txt"]) for m in marken] or [1])
    lvls = 1 + max([m["lvl"] for m in oben] or [0])
    lvl_h = 16 * zeilen + 10
    top_k = -(-(26 + lvls * lvl_h) // K)
    ax = top_k * K
    bot_k = -(-(36 + (44 if unt else 0)) // K)
    H = (top_k + bot_k) * K
    s = [f'<svg class="gerade" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'xmlns="http://www.w3.org/2000/svg" font-family="Helvetica, Arial, sans-serif">',
         f'<defs><pattern id="k{uid}" width="{K}" height="{K}" patternUnits="userSpaceOnUse">'
         f'<path d="M{K} 0H0V{K}" fill="none" stroke="#c8d0dc" stroke-width="1"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="{H}" fill="url(#k{uid})"/>',
         f'<path d="M{W} 0V{H}H0" fill="none" stroke="#c8d0dc"/>',
         f'<line x1="{K}" y1="{ax}" x2="{W - K}" y2="{ax}" stroke="#222" stroke-width="1.7"/>',
         f'<polygon points="{W - K},{ax} {W - K - 10},{ax - 5} {W - K - 10},{ax + 5}" fill="#222"/>',
         f'<polygon points="{K},{ax} {K + 10},{ax - 5} {K + 10},{ax + 5}" fill="#222"/>']
    for i in range(n * teile + 1):
        v = von + i * schritt / teile
        x = X(v)
        major = i % teile == 0
        h = (10 if abs(v) < 1e-9 else 7) if major else 3.5
        sw = 2.2 if abs(v) < 1e-9 else 1.3
        s.append(f'<line x1="{x:.1f}" y1="{ax - h}" x2="{x:.1f}" y2="{ax + h}" stroke="#222" stroke-width="{sw}"/>')
        if major and (i // teile) % lab == 0:
            wt = "700" if abs(v) < 1e-9 else "400"
            s.append(f'<text x="{x:.1f}" y="{ax + 24}" text-anchor="middle" font-size="12.5" '
                     f'font-weight="{wt}" fill="{INK}">{num(v)}</text>')
    for m in marken:
        v, col = m["v"], (NEG if m["v"] < -1e-9 else POS if m["v"] > 1e-9 else INK)
        x = X(v)
        dx = {"middle": 0, "end": 3, "start": -3}[m["anker"]]
        nl = len(m["txt"])
        if m["unten"]:
            by = ax + 58
            s.append(f'<line x1="{x:.1f}" y1="{ax + 6}" x2="{x:.1f}" y2="{by - 14}" stroke="{col}" stroke-width="1.2"/>')
            s.append(f'<circle cx="{x:.1f}" cy="{ax}" r="4.8" fill="#fff" stroke="{col}" stroke-width="2"/>')
        else:
            by = ax - 24 - m["lvl"] * lvl_h
            s.append(f'<line x1="{x:.1f}" y1="{ax - 4}" x2="{x:.1f}" y2="{by + 5}" stroke="{col}" stroke-width="1.2"/>')
            s.append(f'<circle cx="{x:.1f}" cy="{ax}" r="4.8" fill="{col}" stroke="#fff" stroke-width="1"/>')
        for j, t in enumerate(m["txt"]):
            y = by - (nl - 1 - j) * 16
            last = j == nl - 1
            s.append(f'<text x="{x + dx:.1f}" y="{y}" text-anchor="{m["anker"]}" '
                     f'font-size="{13.5 if last else 12}" font-weight="{700 if last else 400}" '
                     f'fill="{col if last else MUT}">{t}</text>')
    s.append("</svg>")
    return "".join(s)


def fig(svg, cap=""):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f"<figure>{svg}{c}</figure>"


# ---------------------------------------------------------------- Abbildungen
SKI = [(-8.5, "06:00"), (-6.2, "08:00"), (-4.0, "10:00"), (-1.8, "20:00"),
       (-0.8, "12:00"), (0.7, "18:00"), (3.2, "14:00"), (3.5, "16:00")]
_LV = [0, 1, 0, 1, 0, 1, 0, 1]
_AN = ["middle"] * 6 + ["end", "start"]


def ski(mit_zeit=True, unten=True):
    ms = []
    for (v, z), l, a in zip(SKI, _LV, _AN):
        w = "−4,0" if v == -4.0 else num(v)
        ms.append(marke(v, z, w, lvl=l, anker=a) if mit_zeit else marke(v, w, lvl=l, anker=a))
    if unten:
        ms.append(marke(-0.5, "−½ = −0,5", unten=True))
    return gerade(-9, 4, 1, 3, 1, 1, ms)


def einf(von, bis, werte, **kw):
    return gerade(von, bis, marken=[marke(v, t) for v, t in werte], **kw)


F_3A = gerade(-10, 7, 1, 2, 2, 1, [marke(v) for v in (-8, 5, -4, -10, 7, 0, -2)])
F_3B = gerade(-6, 5, 1, 2, 2, 1, [marke(v) for v in (-4.5, 1.5, -6, 5, -2.5, 3.5, -1)])
F_6A = gerade(-50, 40, 10, 2, 2, 1, [marke(v) for v in (-20, 5, 25, -35, -5, 40, -50)])
F_6B = gerade(-120, 120, 20, 2, 2, 1, [marke(v) for v in (120, -50, -90, 40, -110, 80)])
F_6C = gerade(-5000, 2500, 500, 2, 2, 2, [marke(v) for v in (-1500, 2000, -4500, 500, -500)])
F_6D = gerade(-10, 6, 1, 2, 2, 1, [marke(v, num(v)) for v in (-3.5, 5.5, -7, -9.5, 0.5, -2.5)])
F_6E = gerade(-2, 2, 1, 8, 4, 1, [marke(-0.75, "−3/4"), marke(0.5, "+1/2"), marke(1.25, "+5/4"),
                                   marke(-0.25, "−1/4"), marke(-2, "−2"), marke(0.75, "+3/4")])
STAEDTE = [(-13, "Oslo", 0), (-10, "Moskau", 1), (-8, "Warschau", 0), (-5, "Berlin", 1),
           (-3, "Wien", 0), (-2, "Stuttgart", 1), (1, "Paris", 0), (2, "London", 1)]
F_STADT = gerade(-14, 3, 1, 2, 1, 1, [marke(v, n, num(v), lvl=l) for v, n, l in STAEDTE])
F_BUCH = gerade(-5, 2, 1, 4, 2, 1, [marke(v) for v in (-4.5, -3.2, -0.5, 1.5)])
F_SALZ = gerade(-40, 160, 20, 2, 1, 2, [marke(-40, "Salzlager", "−40 m"), marke(155, "Ort", "+155 m")])

# ---------------------------------------------------------------- Bausteine
CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;color:#1b1b1b;background:#fff}
.wrap{max-width:1000px;margin:0 auto;padding:0 22px}
header.kopf{padding:30px 0 12px;border-bottom:2px solid #1b1b1b;margin-bottom:0}
h1{font-size:27px;margin:0 0 4px;line-height:1.2}.sub{color:#555;margin:0}
nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #d9d9d4;z-index:5}
nav .wrap{display:flex;gap:6px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
nav a{padding:5px 13px;border-radius:16px;text-decoration:none;color:#1b1b1b;font-size:14px;background:#f1f1ed}
nav a:hover{background:#e3e3dc}
section{padding:34px 0 8px;scroll-margin-top:50px}
h2{font-size:22px;margin:0 0 6px}h2+.lead{margin-top:0}
.lead{color:#555;margin:0 0 16px}
h3{font-size:17px;margin:26px 0 8px}
.ziel{background:#f5f5f1;border-radius:8px;padding:12px 16px;margin:16px 0}
.zeitleiste{display:flex;height:38px;border-radius:6px;overflow:hidden;margin:16px 0 4px;font-size:12.5px;border:1px solid #c9c9c2}
.zeitleiste div{display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.15;padding:0 3px}
.z0{background:#eeeeea}.z1{background:#e3eaf6}.z2{background:#d3dff2}.z3{background:#e3eaf6}.z4{background:#d3dff2}.z5{background:#eeeeea}
.bl{border:1px solid #d3d3cc;border-radius:9px;margin:16px 0;overflow:hidden}
.bl>header{display:flex;align-items:center;gap:12px;background:#f5f5f1;padding:9px 16px;border-bottom:1px solid #d3d3cc}
.bl .nr{width:28px;height:28px;border-radius:50%;background:#1b1b1b;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;font-size:14px}
.bl h3{margin:0;font-size:17px;flex:1}.bl .min{color:#555;font-size:14px;white-space:nowrap}
.bl .body{padding:6px 18px 12px}
.bl ul{margin:8px 0;padding-left:20px}.bl li{margin:6px 0}
.t{display:inline-block;min-width:52px;color:#555;font-size:13.5px}
.knapp{background:#fff6e0;border-left:4px solid #e0a100;padding:7px 12px;margin:10px 0 4px;font-size:15px}
.fehler{background:#fbeeee;border-left:4px solid #b3261e;padding:8px 14px;margin:16px 0}
.fehler ol{margin:6px 0 2px;padding-left:20px}
.nicht{color:#555;font-size:15px;margin:10px 0}
.stift{vertical-align:-2px;margin:0 2px}
.frac{display:inline-block;vertical-align:-.55em;text-align:center;font-size:.85em}
.frac>span{display:block;padding:0 .18em;line-height:1.15}.frac .u{border-top:1px solid #1b1b1b}
figure{margin:10px 0 12px}figure svg{display:block;max-width:100%;height:auto;border:1px solid #c8d0dc}
figcaption{font-size:13.5px;color:#555;margin-top:4px}
.tafelblock{margin:18px 0 26px}
.tafelblock>h3{display:flex;justify-content:space-between;align-items:baseline;background:#eeeeea;border-left:5px solid #1b1b1b;padding:5px 12px;margin:0 0 10px;font-size:16.5px}
.tafelblock>h3 span{font-weight:400;font-size:13.5px;color:#555;font-style:italic}
.heft{border-left:5px solid #1b1b1b;padding-left:14px;margin:12px 0}
.merk{background:#eef3fb;border:1.5px solid #1a56a0;border-radius:6px;padding:8px 13px;margin:9px 0;font-weight:600}
.merk.neg{border-color:#b3261e;background:#fbeeee}
.sprech{font-size:14.5px;color:#555;font-style:italic;margin:6px 0}
.uheft{border-left:5px dashed #1a56a0;padding-left:14px;margin:12px 0}
.chip.ueb{background:#e2ecf8;color:#1a56a0;border:1px dashed #1a56a0}
.chip.mk{background:#eee;color:#1b1b1b;border:1px solid #1b1b1b}
.legende{border:1px solid #c9c9c2;border-radius:6px;padding:7px 12px;font-size:14.5px;margin:12px 0}
.aufg{font-size:16.5px;font-weight:600;margin:6px 0}
.neg{color:#b3261e;font-weight:600}.pos{color:#1a56a0;font-weight:600}
.heftseite{border:2px solid #1b1b1b;border-radius:4px;padding:18px 24px;margin:16px 0;background:#fff;box-shadow:4px 4px 0 #e3e3dc}
.heftseite h3{font-size:20px;margin:0 0 4px;text-decoration:underline}
.heftseite p{margin:8px 0}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:15.5px}
th,td{border:1px solid #d3d3cc;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f5f5f1;font-weight:600}
.chip{display:inline-block;padding:1px 9px;border-radius:10px;font-size:12.5px;font-weight:600;white-space:nowrap}
.orange{background:#fdebd3;color:#8a4b00}.gruen{background:#dcf1dc;color:#1d6b1d}.alle{background:#e2ecf8;color:#1a56a0}
.loes{margin:8px 0 18px}.loes h4{margin:18px 0 6px;font-size:16.5px}
.loes p{margin:5px 0}
.kl{columns:2;column-gap:28px;margin:6px 0}.kl div{break-inside:avoid;margin:2px 0}
footer{margin-top:40px;padding:14px 0 40px;border-top:1px solid #d3d3cc;color:#666;font-size:13.5px}

.vt th:first-child,.vt td.mn{width:52px;text-align:right;white-space:nowrap;color:#555}
.vt td:nth-child(3){width:30%}.vt td:nth-child(4){width:15%;white-space:nowrap}
.vt tr.grp td{background:#eeeeea;font-weight:700;font-size:15.5px}
.vt tr.grp td span{float:right;font-weight:400;color:#555;font-size:14px}
.zeige{background:#e7f3e7;border-left:4px solid #1d6b1d;padding:6px 12px;margin:0 0 10px;font-size:15px}
.folie{border:2px solid #1b1b1b;border-radius:10px;padding:14px 20px 8px;margin:18px 0}
.folie h3{margin:0 0 10px;font-size:21px}.folie h3 span{font-weight:400;font-size:14px;color:#555;margin-left:8px}
.banner svg,.banner img{display:block;width:100%;height:auto;border-radius:8px}
.nichts{background:#e7f3e7;border-left:4px solid #1d6b1d;padding:9px 14px;margin:8px 0}
.chips{display:grid;grid-template-columns:repeat(8,1fr);gap:8px;margin:10px 0 12px}
.chips div{border:1px solid #d3d3cc;border-radius:8px;text-align:center;padding:5px 2px 7px;background:#fbfbf9}
.chips small{display:block;color:#555;font-size:12.5px}.chips b{font-size:18px;white-space:nowrap}
.fragen{font-size:19px;line-height:1.45;margin:10px 0 8px;padding-left:24px}.fragen li{margin:6px 0}
svg.karte{display:block;max-width:100%;height:auto;margin:6px 0}
@media (max-width:760px){.chips{grid-template-columns:repeat(4,1fr)}}
@media print{nav{display:none}section{page-break-before:always}.bl,figure,.heftseite,.tafelblock{break-inside:avoid}body{font-size:11pt}}
"""

BLOECKE = [(4, "Start"), (9, "1 · Skitag"), (20, "2 · Zahlengerade"),
           (25, "3 · Selbst zeichnen"), (24, "4 · Vergleichen"), (8, "5 · Ausstieg")]


def zeitleiste():
    tot = sum(m for m, _ in BLOECKE)
    z = "".join(f'<div class="z{i}" style="width:{m / tot * 100:.2f}%" title="{m} min">{n}<br>{m}′</div>'
                for i, (m, n) in enumerate(BLOECKE))
    return f'<div class="zeitleiste">{z}</div>'


def bl(nr, titel, t0, t1, inhalt, knapp=None):
    k = f'<div class="knapp"><b>Wenn es knapp wird:</b> {knapp}</div>' if knapp else ""
    return (f'<div class="bl"><header><div class="nr">{nr}</div><h3>{titel}</h3>'
            f'<div class="min">Minute {t0}–{t1} · {t1 - t0} min</div></header>'
            f'<div class="body">{inhalt}{k}</div></div>')


def li(*a):
    return "<li>" + "".join(a) + "</li>"


def t(m):
    return f'<span class="t">{m} min</span>'


E = stift()
UE = '<span class="chip ueb">Übungsheft</span>'
MK = '<span class="chip mk">Merkheft</span>'

# ---------------------------------------------------------------- Folien
def _tanne(x, y, h):
    w = h * 0.55
    return (f'<g transform="translate({x} {y})"><rect x="{-w * 0.08:.1f}" y="{-h * 0.12:.1f}" width="{w * 0.16:.1f}" '
            f'height="{h * 0.14:.1f}" fill="#5b4632"/>'
            f'<polygon points="0,{-h} {-w / 2:.1f},{-h * 0.5:.1f} {w / 2:.1f},{-h * 0.5:.1f}" fill="#2f6b45"/>'
            f'<polygon points="0,{-h * 0.72:.1f} {-w * 0.62:.1f},{-h * 0.16:.1f} {w * 0.62:.1f},{-h * 0.16:.1f}" fill="#2a5e3d"/>'
            f'<polygon points="0,{-h} {-w * 0.22:.1f},{-h * 0.8:.1f} {w * 0.22:.1f},{-h * 0.8:.1f}" fill="#fff"/></g>')


def _kappe(p):
    return f'<polygon points="{p}" fill="#fff"/>'


def skibild():
    """Eigene Skipisten-Grafik (Berge, Piste, Skifahrer), Banner 1280 x 270."""
    a = ['<svg class="skibild" viewBox="0 0 1280 270" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">',
         '<defs><linearGradient id="himmel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb8ec"/>'
         '<stop offset="1" stop-color="#e6f2fc"/></linearGradient></defs>',
         '<rect width="1280" height="270" fill="url(#himmel)"/>',
         '<circle cx="1090" cy="62" r="52" fill="#ffe08a" opacity=".45"/><circle cx="1090" cy="62" r="32" fill="#ffd45c"/>',
         '<g fill="#fff" opacity=".95"><ellipse cx="330" cy="58" rx="46" ry="15"/><ellipse cx="366" cy="48" rx="34" ry="16"/>'
         '<ellipse cx="300" cy="52" rx="28" ry="12"/></g>',
         '<path d="M0 190 L90 120 L150 155 L250 60 L350 150 L430 105 L520 165 L640 75 L740 150 L840 100 L950 160 '
         'L1060 90 L1170 150 L1280 105 L1280 270 L0 270Z" fill="#9fb6d3"/>',
         _kappe("250,60 228,92 244,86 252,98 264,84 274,90"), _kappe("640,75 616,110 632,104 642,116 654,102 664,108"),
         _kappe("1060,90 1038,122 1052,116 1062,126 1074,114 1084,120"), _kappe("430,105 414,128 426,124 434,132 444,122"),
         _kappe("840,100 824,124 836,120 844,128 854,118"),
         '<path d="M0 235 L130 170 L240 215 L380 150 L520 220 L680 165 L820 225 L980 160 L1120 225 L1280 175 '
         'L1280 270 L0 270Z" fill="#c6d5e8"/>',
         _kappe("380,150 362,178 374,173 382,184 394,171 402,177"), _kappe("680,165 664,190 674,186 682,194 692,184"),
         _kappe("980,160 962,188 974,183 982,193 994,181 1002,186"), _kappe("130,170 114,196 124,192 132,200 142,190"),
         '<path d="M0 232 C260 215 520 250 820 258 S1170 250 1280 236 L1280 270 L0 270Z" fill="#fff"/>',
         '<path d="M0 252 C260 236 520 262 820 266 S1170 262 1280 250 L1280 270 L0 270Z" fill="#e4edf7"/>',
         '<g fill="none" stroke="#d3e0f0" stroke-width="3" stroke-linecap="round"><path d="M130 238 C200 230 260 244 330 240"/>'
         '<path d="M880 250 C950 244 1010 254 1090 250"/><path d="M430 246 C500 250 560 254 640 256"/></g>',
         '<g fill="none" stroke="#c3d3e6" stroke-width="2.5" stroke-linecap="round"><path d="M520 251 C600 258 650 250 700 252"/>'
         '<path d="M520 257 C600 264 650 256 700 258"/></g>']
    for x, y, h in ((48, 250, 70), (100, 256, 92), (150, 250, 58), (1170, 246, 74), (1222, 254, 96), (1262, 248, 62)):
        a.append(_tanne(x, y, h))
    a.append('<g transform="translate(770 222) rotate(6)">'
             '<ellipse cx="0" cy="34" rx="58" ry="4.5" fill="#cfdcec"/>'
             '<line x1="-48" y1="28" x2="46" y2="21" stroke="#2b2b2b" stroke-width="5" stroke-linecap="round"/>'
             '<path d="M-14 24 L-2 2 L14 14 L20 21" stroke="#1f2a44" stroke-width="11" fill="none" '
             'stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M-2 4 L7 -24" stroke="#3c9a3c" stroke-width="20" stroke-linecap="round"/>'
             '<path d="M6 -19 L28 -5" stroke="#3c9a3c" stroke-width="8" stroke-linecap="round"/>'
             '<line x1="30" y1="-5" x2="52" y2="24" stroke="#444" stroke-width="2.5"/>'
             '<circle cx="15" cy="-39" r="10" fill="#ececec" stroke="#8a8a8a" stroke-width="1.5"/>'
             '<rect x="17" y="-43" width="9" height="7" rx="2.5" fill="#2b4a6b"/></g>')
    a.append("</svg>")
    return "".join(a)


def skichips(einheit=" °C"):
    return "".join(
        f'<div><small>{z} Uhr</small><b class="{"neg" if v < 0 else "pos"}">'
        f'{("−4,0" if v == -4.0 else num(v))}{einheit}</b></div>'
        for v, z in sorted(SKI, key=lambda q: q[1]))


def skifoto():
    """Foto (KI-generiert, Gemini) als Banner, eingebettet als data-URI. Datei: skitag_banner.jpg"""
    import base64
    d = base64.b64encode((Path(__file__).parent / "skitag_banner.jpg").read_bytes()).decode()
    return f'<img class="skifoto" src="data:image/jpeg;base64,{d}" alt="Drei Jugendliche beim Skifahren">'


import sys
sys.path.insert(0, str(Path(__file__).parent))
from europakarte_erzeugen import proj, W as KW, H as KH

# Lage: echte Länge/Breite, Werte aus der Wetterkarte im Buch (S. 14). Anker: r = Text rechts vom Punkt, l = links.
STADT = {
    "Oslo": (10.75, 59.91, -13, "r"), "St. Petersburg": (30.31, 59.93, -7, "l"), "Moskau": (37.62, 55.75, -10, "l"),
    "London": (-0.13, 51.51, 2, "l"), "Berlin": (13.40, 52.52, -5, "r"), "Warschau": (21.01, 52.23, -8, "r"),
    "Stuttgart": (9.18, 48.78, -2, "l"), "Paris": (2.35, 48.86, 1, "l"), "Wien": (16.37, 48.21, -3, "r"),
    "Madrid": (-3.70, 40.42, 11, "r"), "Lissabon": (-9.14, 38.72, 15, "l"), "Malaga": (-4.42, 36.72, 17, "r"),
    "Nizza": (7.26, 43.70, 12, "l"), "Rom": (12.50, 41.90, 12, "r"), "Belgrad": (20.46, 44.79, 6, "r"),
    "Istanbul": (28.98, 41.01, 14, "r"), "Palma": (2.65, 39.57, 12, "r"), "Athen": (23.73, 37.98, 16, "r"),
    "Palermo": (13.36, 38.12, 13, "r"),
}


def _hull(pts):
    pts = sorted(set(pts))
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def wetterkarte():
    land = (Path(__file__).parent / "europa_pfad.txt").read_text()
    pos = {n: proj(lo, la) for n, (lo, la, v, a) in STADT.items()}
    kalt = _hull([pos[n] for n, (lo, la, v, a) in STADT.items() if v < 0])
    hull = "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in kalt) + "Z"
    s = [f'<svg class="karte" viewBox="0 0 {KW} {KH}" xmlns="http://www.w3.org/2000/svg" '
         'font-family="Helvetica, Arial, sans-serif" width="100%">',
         f'<defs><clipPath id="kc"><rect width="{KW}" height="{KH}" rx="10"/></clipPath></defs>',
         f'<rect width="{KW}" height="{KH}" rx="10" fill="#cfe0f3"/>',
         '<g clip-path="url(#kc)">',
         f'<path d="{land}" fill="#f4f1e8" stroke="#a9a99f" stroke-width="1.3" stroke-linejoin="round"/>',
         f'<g opacity=".4"><path d="{hull}" fill="#b98ad6" stroke="#b98ad6" stroke-width="110" '
         'stroke-linejoin="round"/></g>', '</g>']
    for n, (lo, la, v, a) in STADT.items():
        x, y = pos[n]
        col = NEG if v < 0 else POS
        dx, anc = (18, "start") if a == "r" else (-18, "end")
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}" stroke="#fff" stroke-width="2.5"/>')
        s.append(f'<text x="{x + dx:.0f}" y="{y - 2:.0f}" text-anchor="{anc}" font-size="27" fill="#222" '
                 f'stroke="#f4f1e8" stroke-width="5" paint-order="stroke">{n}</text>')
        s.append(f'<text x="{x + dx:.0f}" y="{y + 32:.0f}" text-anchor="{anc}" font-size="34" font-weight="700" '
                 f'fill="{col}" stroke="#f4f1e8" stroke-width="5" paint-order="stroke">{num(v, plus=False)}</text>')
    s.append("</svg>")
    return "".join(s)


folien = f"""
<section id="folien"><h2>Folien</h2>
<p class="lead">Zeigst du am Beamer, bevor du an der Tafel anfängst. Die Schüler müssen dafür nicht ins Buch schauen.
Beide Folien sind nach dem Buch nachgebaut (S. 10 und S. 14), damit sie scharf sind.</p>
<div class="folie"><h3>Folie 1 · Skitag <span>vor Block 1</span></h3>
<div class="banner">{skifoto()}</div><div class="chips">{skichips()}</div>
<ul class="fragen"><li>Wann ist der Schnee hart gefroren, wann eher weich oder matschig?</li>
<li>Hüttenwirt Franz sagt: „Über Nacht bekommen wir wieder Neuschnee.“ Kann das sein? Achtet auf den Temperaturverlauf.</li></ul></div>
<div class="folie"><h3>Folie 2 · Wetterkarte <span>vor Block 4</span></h3>
{wetterkarte()}
<ul class="fragen"><li>In welchen Städten liegt die Temperatur über dem Gefrierpunkt, in welchen darunter?</li>
<li>Wo ist es kälter als in Berlin? Wo wärmer als in Stuttgart?</li></ul></div>
</section>
"""


# ---------------------------------------------------------------- Vor der Stunde (Drucken, Vorbereiten)
DRUCK = []      # (Was, Anzahl, Hinweis) - leer = nichts zu drucken
DIGITAL = [
    ("Folien in Notability importieren", "Rationale Zahlen 1 – Folien für den Beamer.pdf (iCloud, Mathematik 7c, 04 Rationale Zahlen)"),
    ("Leere Skitag-Gerade auf Karo vorbereiten", "1 °C = 3 Kästchen, von −9 bis +4, Null markiert, Striche ohne Zahlen"),
    ("Lösungsbuch bereit", "S. 11 Nr. 3, 4, 6 · S. 12 Nr. 8, 9 · S. 15 Nr. 5"),
]
RAUM = ["Beamer und Spiegelung vom iPad", "Die Klasse hat: Buch, Übungsheft (kariert), Merkheft, Stift"]

if DRUCK:
    _druck = ("<table><tr><th>Ausdrucken / kopieren</th><th>Anzahl</th><th>Hinweis</th></tr>"
              + "".join(f"<tr><td>{a}</td><td>{n}</td><td>{h}</td></tr>" for a, n, h in DRUCK) + "</table>")
else:
    _druck = '<div class="nichts"><b>Nichts zu drucken.</b> Alles kommt aus Buch, Heften und Folien.</div>'

vorher = f"""
<section id="vorher"><h2>Vor der Stunde</h2>
<p class="lead">Was du vorher tun musst. Steht hier etwas unter „Drucken", muss es vor der Stunde ausgedruckt oder kopiert sein.</p>
<h3>Drucken und kopieren</h3>{_druck}
<h3>Digital vorbereiten</h3>
<table><tr><th>Was</th><th>Wo, wie</th></tr>{"".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in DIGITAL)}</table>
<h3>Im Raum</h3><ul>{"".join(f"<li>{r}</li>" for r in RAUM)}</ul>
</section>
"""

# ---------------------------------------------------------------- Verlauf (Tabelle)
ORA = "<span class='chip orange'>orange</span>"
GRU = "<span class='chip gruen'>grün</span>"
ALL = "<span class='chip alle'>alle</span>"


def grp(nr, titel, t0, t1):
    return f'<tr class="grp"><td colspan="4">{nr} · {titel}<span>Minute {t0}–{t1}</span></td></tr>'


def vz(m, was, buch, wer, e=False):
    return f'<tr><td class="mn">{m}′</td><td>{E + " " if e else ""}{was}</td><td>{buch}</td><td>{wer}</td></tr>'


zeilen = "".join([
    grp(0, "Start", 0, 4),
    vz(4, "Ankommen, Ziel ansagen", "Übungsheft (kariert), Merkheft, Stift. Buch bleibt zu.", "Plenum"),
    grp(1, "Skitag", 4, 13),
    vz(3, "<b>Folie 1</b> zeigen, acht Temperaturen vorlesen lassen", "Folie 1", "Plenum"),
    vz(3, "Wann ist der Schnee hart, wann weich? Sortieren nach dem Vorzeichen", "Folie 1", "Plenum"),
    vz(1, "Neuschnee über Nacht? (20 Uhr: −1,8 °C, fallend)", "Folie 1", "Plenum"),
    vz(2, "Behauptung „−8,5 ist größer als −1,8“ an die Tafel, abstimmen, <b>nicht auflösen</b>", "Tafel", "Plenum"),
    grp(2, "Zahlengerade nach links", 13, 33),
    vz(6, "Skitag-Gerade (leer vorbereitet, 1 °C = 3 Kästchen). Klasse ruft die Werte, du trägst ein", "Tafel", "Lehrer, Plenum"),
    vz(2, "Wo liegt −8,5, wo −1,8? Nur die Lage. Dann −½ eintragen", "Tafel", "Plenum"),
    vz(11, "Gerade abzeichnen (6 min), drei Merksätze (5 min)", f"Tafel &rarr; {MK}", "Einzel, abschreiben", True),
    vz(2, "Vorzeichen zu Alltagsangaben", f"Buch S. 11 Nr. 4 a) bis f), {ALL}", "mündlich"),
    grp(3, "Selbst zeichnen", 33, 58),
    vz(3, "Aufgabe lesen. Frage: Wie viele Kästchen ist 1 wert?", f"Buch S. 11 Nr. 3 a), {ALL}", "Plenum"),
    vz(14, "Zahlengerade zeichnen. Danach freie Wahl",
       f"S. 11 Nr. 3 a) {ALL}<br>dann S. 11 Nr. 3 b) {ORA} oder S. 11 Nr. 6 a), d) {GRU}", f"<b>Einzel</b><br>{UE}"),
    vz(5, "Tauschen und kontrollieren, Musterlösung aufdecken", "Tafel", "Partner"),
    vz(3, "Wer hat anders eingeteilt und trotzdem richtig?", "&ndash;", "Plenum"),
    vz("+", "Wer früh fertig ist", f"S. 11 Nr. 6 e) oder S. 12 Nr. 8 {GRU}", "Einzel"),
    grp(4, "Vergleichen", 58, 82),
    vz(4, "<b>Folie 2</b> zeigen. Über/unter 0 °C, kälter als Berlin, wärmer als Stuttgart (Falle: Wien)", "Folie 2", "Plenum"),
    vz(5, "Fünf Vergleiche mit &lt; und &gt; schreiben, z. B. Moskau &ndash; Berlin", "Folie 2", f"<b>Einzel</b><br>{UE}"),
    vz(7, "Merksatz gemeinsam formulieren, dann abschreiben. Behauptung aus Block 1 auflösen",
       f"Tafel &rarr; {MK}", "Plenum, abschreiben", True),
    vz(8, "Zeichen &lt; oder &gt; einsetzen. Kontrolle über die Tafel",
       f"Buch S. 15 Nr. 5 links {ORA} oder rechts {GRU}", f"<b>Einzel</b><br>{UE}"),
    grp(5, "Ausstieg", 82, 90),
    vz(3, "Ausstiegsfrage: −7 oder −2, ein Satz", "Tafel", f"Einzel<br>{UE}"),
    vz(2, "Hausaufgabe ansagen (Termin in Untis)", f"Buch S. 12 Nr. 9 links {ORA}<br>Rest von S. 15 Nr. 5", f"Zu Hause<br>{UE}"),
    vz(3, "Puffer, Aufräumen", "&ndash;", "&ndash;"),
])

verlauf = f"""
<section id="verlauf"><h2>Verlauf</h2>
<p class="lead">Dienstag, 1. und 2. Stunde, 90 Minuten. Alles aus dem Mathebuch, es wird nichts gedruckt.
{E} = wird ins {MK} geschrieben. Alle Übungen kommen ins {UE}. Die Schreibzeit steckt in den Minuten.</p>
<div class="ziel"><b>Ziel:</b> Negative Zahlen liegen links von der Null. Die Klasse teilt eine Zahlengerade selbst sinnvoll ein und vergleicht
zwei rationale Zahlen über ihre Lage: weiter links heißt kleiner. <b>Nicht Ziel:</b> Rechnen mit negativen Zahlen, das kommt nächste Woche.</div>
{zeitleiste()}
<table class="vt"><tr><th>Min</th><th>Was</th><th>Buch und Material</th><th>Wer</th></tr>{zeilen}</table>
<div class="knapp"><b>Wenn es knapp wird:</b> Block 3 nur S. 11 Nr. 3 a), dafür die Besprechung ausführlich. Block 4: S. 15 Nr. 5 wird Hausaufgabe.</div>
<div class="fehler"><b>Worauf du achten kannst</b>
<ol>
<li>„−12 &gt; −5, weil 12 &gt; 5.“ Der größte Stolperstein. Nicht erklären, auf die Gerade zeigen lassen.</li>
<li>Das Vorzeichen fällt weg: −3,5 landet bei +3,5.</li>
<li>Kleinste und größte Zahl vorher nicht angeschaut, die Gerade passt nicht aufs Blatt.</li>
<li>Ungleiche Abstände. Kästchen zählen statt Lineal.</li>
<li>−2,5 liegt zwischen −2 und −3, nicht zwischen −2 und −1.</li>
</ol></div>
<p class="nicht"><b>Bewusst nicht dabei:</b> Rechnen mit negativen Zahlen, Betrag, S. 12 Nr. 9 rechts (Kontoauszug, braucht Addition).</p>
</section>
"""

# ---------------------------------------------------------------- Tafelbild
tafel = f"""
<section id="tafel"><h2>Tafelbild</h2>
<p class="lead">So sieht die Tafel am Ende aus. Die Geraden sind auf Karo gezeichnet, ein Kästchen ist ein Kästchen im Heft.
Kursiv steht, was du sagst. Gezeichnet wird von oben nach unten.</p>
<div class="legende">{E} <b>Dicker schwarzer Balken</b> = wird ins {MK} abgeschrieben.<br><b>Gestrichelter blauer Balken</b> = Übung, kommt ins {UE}. Alles ohne Balken bleibt an der Tafel.</div>

<div class="tafelblock"><h3>1 · Skitag <span>Minute 4–13</span></h3>
<p class="zeige">▶ Erst <b>Folie 1</b> zeigen, dann die Tafel anfangen.</p>
<p><span class="neg">Minus</span> = unter 0 °C: Schnee hart (6, 8, 10 Uhr)<br>
<span class="pos">Plus</span> = über 0 °C: Schnee weich (14, 16, 18 Uhr)</p>
<p class="aufg">−8,5 ist größer als −1,8. &nbsp; Stimmt? &nbsp; Ja: ___ &nbsp; Nein: ___</p>
<p class="sprech">Offen lassen. Die Strichliste bleibt bis Block 4 stehen.</p></div>

<div class="tafelblock"><h3>2 · Zahlen unter Null <span>Minute 13–33</span></h3>
<div class="heft">{fig(ski(True), "1 °C = 3 Kästchen. Die Uhrzeit steht nur an der Tafel, das Merkheft bekommt nur die Zahlen.")}
<div class="merk"><span class="neg">Negative Zahlen</span> sind kleiner als null und liegen auf der Zahlengeraden links von der Null. Vorzeichen −.</div>
<div class="merk"><span class="pos">Positive Zahlen</span> sind größer als null und liegen rechts von der Null. Vorzeichen +.</div>
<div class="merk">Ganze Zahlen, Brüche und Dezimalzahlen, positiv und negativ, heißen zusammen <b>rationale Zahlen</b> (ℚ).</div></div>
<p class="sprech">Beim Eintragen laut denken. −0,5 zuletzt eintragen, mit der Frage „Gibt es auch −½?“. Die Null liegt fest, das hat man so vereinbart: Gefrierpunkt, Meeresspiegel.</p>
<p>S. 11 Nr. 4 mündlich: +15 °C · −22,5 °C · −38 m · +1258 m · +384,00 € · −2165,00 €</p></div>

<div class="tafelblock"><h3>3 · Selbst zeichnen <span>Minute 33–58</span></h3>
<div class="uheft"><p class="aufg">{UE} S. 11 Nr. 3 a) Zeichne eine Zahlengerade und markiere: −8; +5; −4; −10; +7; 0; −2</p>
<p class="sprech">Erst kleinste und größte Zahl anschauen. Wie viele Kästchen ist 1 wert?</p>
<p>Danach {ORA} S. 11 Nr. 3 b) oder {GRU} S. 11 Nr. 6 a), d), ebenfalls ins Übungsheft.</p></div>
{fig(F_3A, "Musterlösung, erst nach der Einzelarbeit aufdecken. 1 = 2 Kästchen. Mit 1 Kästchen geht es genauso.")}</div>

<div class="tafelblock"><h3>4 · Vergleichen <span>Minute 58–82</span></h3>
<p class="zeige">▶ Erst <b>Folie 2</b> (Wetterkarte) zeigen, dann die Tafel anfangen.</p>
{fig(F_STADT, "Wetterkarte S. 14. 1 = 2 Kästchen. Die Städte nach und nach eintragen lassen.")}
<div class="uheft"><p class="aufg">{UE} Schreibe fünf Vergleiche mit &lt; und &gt; auf.</p>
<p>Zum Beispiel: Moskau kälter als Berlin: −10 &lt; −5 &nbsp;·&nbsp; Wien kälter als Stuttgart: −3 &lt; −2 &nbsp;·&nbsp; Paris wärmer als Wien: +1 &gt; −3 &nbsp;·&nbsp; London wärmer als Oslo: +2 &gt; −13</p></div>
<div class="heft">
<div class="merk">Auf der Zahlengeraden sind die rationalen Zahlen der Größe nach geordnet.<br>
Von zwei Zahlen liegt die <b>kleinere weiter links</b>, die <b>größere weiter rechts</b>.<br>
<span style="font-weight:400">Zeichen: &lt; kleiner als &nbsp; &gt; größer als &nbsp; = gleich</span></div>
{fig(F_BUCH, "Beispiel aus dem Buch S. 14. 1 = 4 Kästchen.")}
<p>−4,5 &lt; −3,2 &nbsp;&nbsp;(−4,5 liegt links von −3,2)<br>+1,5 &gt; −0,5 &nbsp;&nbsp;(+1,5 liegt rechts von −0,5)</p>
<div class="merk neg">Achtung: −12 &lt; −5, obwohl 12 &gt; 5.</div></div>
<p class="aufg">Zu Block 1: −8,5 &lt; −1,8 &nbsp;✔ &nbsp;Die Behauptung war falsch.</p>
<div class="uheft"><p class="aufg">{UE} S. 15 Nr. 5: Setze das Zeichen &lt; oder &gt; ein.</p>
<p>{ORA} links, ganze Zahlen &nbsp;oder&nbsp; {GRU} rechts, Dezimalzahlen. Selbst entscheiden.</p></div></div>

<div class="tafelblock"><h3>5 · Ausstieg <span>Minute 82–90</span></h3>
<div class="uheft"><p class="aufg">{UE} Welche Zahl ist größer, −7 oder −2? Erkläre mit der Zahlengeraden.</p>
<p><b>Hausaufgabe</b> (auch {UE}): S. 12 Nr. 9 links · Rest von S. 15 Nr. 5</p></div></div>
</section>
"""

# ---------------------------------------------------------------- Merkheft
merkheft = f"""
<section id="merkheft"><h2>Merkheft</h2>
<p class="lead">Das schreiben die Schüler ab, in dieser Reihenfolge. Zwei Teile: der erste in Block 2, der zweite in Block 4.</p>
<div class="heftseite">
<h3>Zahlen unter Null</h3>
{fig(ski(False, False), "Skitag: Die acht Temperaturen. 1 °C = 3 Kästchen. Über die Punkte schreiben, die Uhrzeit weglassen.")}
<p><span class="neg">Negative Zahlen</span> sind kleiner als null und liegen auf der Zahlengeraden links von der Null. Sie haben das Vorzeichen −.</p>
<p><span class="pos">Positive Zahlen</span> sind größer als null und liegen rechts von der Null. Sie haben das Vorzeichen +.</p>
<p>Ganze Zahlen, Brüche und Dezimalzahlen, positiv und negativ, heißen zusammen <b>rationale Zahlen</b> (ℚ).</p>
</div>
<div class="heftseite">
<h3>Rationale Zahlen vergleichen</h3>
<p>Auf der Zahlengeraden sind die rationalen Zahlen der Größe nach geordnet. Von zwei Zahlen liegt die kleinere weiter links, die größere weiter rechts.</p>
<p>Zeichen: &lt; kleiner als, &gt; größer als, = gleich</p>
{fig(F_BUCH, "1 = 4 Kästchen")}
<p>−4,5 &lt; −3,2 &nbsp;&nbsp; +1,5 &gt; −0,5</p>
<p><b>Achtung:</b> −12 &lt; −5, obwohl 12 &gt; 5.</p>
</div>
</section>
"""

# ---------------------------------------------------------------- Aufgaben
aufgaben = f"""
<section id="aufgaben"><h2>Aufgaben</h2>
<p class="lead">Alles steht im Buch. Alle Übungen kommen ins <span class="chip ueb">Übungsheft</span>, Merksätze ins <span class="chip mk">Merkheft</span>. Farbe = Niveau im Buch. <span class="chip orange">orange</span> ist die linke, leichtere Spalte,
<span class="chip gruen">grün</span> die rechte, schwerere. <span class="chip alle">alle</span> sind die Aufgaben über beiden Spalten.</p>
<table><tr><th>Block</th><th>Buch</th><th>Niveau</th><th>Aufgabe</th></tr>
<tr><td>1</td><td>Folie 1 (Buch S. 10)</td><td><span class="chip alle">alle</span></td><td>Skitag: hart oder weich, Hüttenwirt. Mündlich.</td></tr>
<tr><td>2</td><td>S. 11 Nr. 4</td><td><span class="chip alle">alle</span></td><td>Schreibe mit dem Vorzeichen + oder −. Mündlich, a bis f.</td></tr>
<tr><td>3</td><td>S. 11 Nr. 3 a)</td><td><span class="chip alle">alle</span></td><td>Zeichne eine Zahlengerade und markiere: −8; +5; −4; −10; +7; 0; −2</td></tr>
<tr><td>3</td><td>S. 11 Nr. 3 b)</td><td><span class="chip orange">orange</span></td><td>−4,5; +1,5; −6; +5; −2,5; +3,5; −1</td></tr>
<tr><td>3</td><td>S. 11 Nr. 6</td><td><span class="chip gruen">grün</span></td><td>Zeichne eine Zahlengerade, überlege dir eine günstige Einteilung. Zuerst a) und d).</td></tr>
<tr><td>3</td><td>S. 12 Nr. 8</td><td><span class="chip gruen">grün</span></td><td>Für Schnelle: Salzbergwerk, Tipp 20 m sind 1 cm.</td></tr>
<tr><td>4</td><td>Folie 2 (Buch S. 14)</td><td><span class="chip alle">alle</span></td><td>Wetterkarte, drei Fragen mündlich, dann fünf Vergleiche ins Übungsheft.</td></tr>
<tr><td>4</td><td>S. 15 Nr. 5 links</td><td><span class="chip orange">orange</span></td><td>Setze das Zeichen &lt; oder &gt; ein, ganze Zahlen.</td></tr>
<tr><td>4</td><td>S. 15 Nr. 5 rechts</td><td><span class="chip gruen">grün</span></td><td>Setze das Zeichen &lt; oder &gt; ein, Dezimalzahlen.</td></tr>
<tr><td>HA</td><td>S. 12 Nr. 9 links</td><td><span class="chip orange">orange</span></td><td>Zwei Zahlen sind von der Null gleich weit entfernt. Wie heißen sie bei Abstand 6, 20, 3, 0,4?</td></tr>
<tr><td>HA</td><td>S. 15 Nr. 5</td><td>beide</td><td>Was in der Stunde nicht fertig wurde.</td></tr></table>
<p class="nicht">Nichts zu drucken. Für die Tafel: S. 11 Nr. 3 a) und die Ausstiegsfrage abschreiben, der Rest steht im Buch.</p>
</section>
"""

# ---------------------------------------------------------------- Lösungen
loesungen = f"""
<section id="loesungen"><h2>Lösungen</h2>
<p class="lead">Selbst gerechnet, noch nicht mit dem digitalen Lösungsbuch abgeglichen. Geraden auf Karo, 1 Kästchen = 5 mm im Heft.</p>
<div class="loes">
<h4>Block 1 · Skitag (S. 10)</h4>
<p><b>Hart</b> ist der Schnee bei Minus: 6, 8, 10 Uhr, knapp auch 12 Uhr (−0,8 °C) und 20 Uhr (−1,8 °C). <b>Weich</b> ist er bei Plus: 14, 16, 18 Uhr (+0,7 °C um 18 Uhr ist nur knapp darüber).<br>
<b>Neuschnee:</b> Ja, kann sein. Um 20 Uhr sind es −1,8 °C und die Temperatur fällt seit 16 Uhr.<br>
<b>Behauptung:</b> −8,5 ist nicht größer als −1,8. −8,5 liegt weiter links, also −8,5 &lt; −1,8.</p>
<h4>S. 11 Nr. 4</h4>
<div class="kl"><div>a) +15 °C</div><div>b) −22,5 °C</div><div>c) −38 m</div><div>d) +1258 m</div><div>e) +384,00 €</div><div>f) −2165,00 €</div></div>
<h4>S. 11 Nr. 3 a)</h4>{fig(F_3A, "1 = 2 Kästchen, 17 Einheiten = 34 Kästchen. Mit 1 Kästchen je Einheit sind es 17 Kästchen, auch richtig.")}
<h4>S. 11 Nr. 3 b)</h4>{fig(F_3B, "1 = 2 Kästchen, halbe Einheiten = 1 Kästchen.")}
<h4>S. 11 Nr. 6 (grün)</h4>
{fig(F_6A, "a) 10 = 2 Kästchen, also 5 = 1 Kästchen.")}
{fig(F_6B, "b) 20 = 2 Kästchen, also 10 = 1 Kästchen.")}
{fig(F_6C, "c) 500 = 2 Kästchen, also 250 = 1 Kästchen. Beschriftet ist jeder zweite Strich.")}
{fig(F_6D, "d) 1 = 2 Kästchen, also 0,5 = 1 Kästchen. Die −7,0 ist die −7.")}
{fig(F_6E, "e) 1 = 8 Kästchen, also ein Viertel = 2 Kästchen. Viertel und Halbe passen bei 8 Kästchen je Einheit genau.")}
<h4>S. 12 Nr. 8 (Salzbergwerk)</h4>
{fig(F_SALZ, "a) 20 m = 2 Kästchen (1 cm). +155 liegt bei 15,5 Kästchen rechts der Null, −40 bei 4 Kästchen links.")}
<p>b) 195 m. 40 m bis zur Meereshöhe, dann noch 155 m bis zur Erdoberfläche.</p>
<h4>S. 14 · Wetterkarte</h4>
<p><b>Über dem Gefrierpunkt:</b> London (2), Paris (1), Madrid (11), Lissabon (15), Malaga (17), Nizza (12), Rom (12), Belgrad (6), Istanbul (14), Palma (12), Athen (16), Palermo (13).<br>
<b>Darunter:</b> Oslo (−13), St. Petersburg (−7), Moskau (−10), Berlin (−5), Warschau (−8), Stuttgart (−2), Wien (−3).<br>
<b>Kälter als Berlin (−5):</b> Oslo, St. Petersburg, Moskau, Warschau.<br>
<b>Wärmer als Stuttgart (−2):</b> London, Paris und alle Städte mit Plus. <b>Wien nicht</b>, −3 &lt; −2.</p>
<h4>S. 15 Nr. 5</h4>
<p><span class="chip orange">orange</span></p>
<div class="kl"><div>a) 12 &gt; −5</div><div>b) −4 &lt; 7</div><div>c) −6 &lt; −4</div><div>d) −9 &gt; −11</div><div>e) −21 &lt; −12</div><div>f) −99 &lt; −88</div></div>
<p><span class="chip gruen">grün</span></p>
<div class="kl"><div>a) −7,6 &lt; 6,7</div><div>b) 1,8 &gt; −2,2</div><div>c) −2,4 &gt; −4,2</div><div>d) −7,6 &lt; −6,7</div><div>e) −5,67 &gt; −6,75</div><div>f) −0,57 &gt; −0,75</div></div>
<h4>Ausstiegsfrage</h4>
<p>−2 ist größer. Auf der Zahlengeraden liegt −2 weiter rechts als −7.</p>
<h4>Hausaufgabe · S. 12 Nr. 9 links</h4>
<div class="kl"><div>a) +6 und −6</div><div>b) +20 und −20</div><div>c) +3 und −3</div><div>d) +0,4 und −0,4</div></div>
</div></section>
"""

# ---------------------------------------------------------------- Ausblick
ausblick = """
<section id="ausblick"><h2>Ausblick</h2>
<p class="lead">Nach dem Stoffverteilungsplan 26/27 für Klasse 7. Die Spalte „Vorschlag" ist ein Entwurf, noch nicht besprochen.
Montag sind zwei Halbgruppen, jede bekommt in der 5. oder 6. Stunde dieselbe Stunde.</p>
<div class="ziel"><b>Wo wir stehen:</b> Woche 1 (Bruchrechnung mit Dezimalbrüchen) ist erledigt. Die Doppelstunde am Dienstag deckt die Woche 2
(Rationale Zahlen, Anordnung auf der Zahlengeraden) ab und zieht das Vergleichen aus Woche 3 schon vor. Das gibt etwas Luft.</div>
<table><tr><th>Woche</th><th>Datum</th><th>Thema laut Plan</th><th>Vorschlag</th></tr>
<tr><td>2</td><td>21.9.–25.9.</td><td>Rationale Zahlen: ganze Zahlen, rationale Zahlen, Anordnung auf der Zahlengeraden</td>
<td><b>Di (Doppelstunde):</b> diese Vorbereitung.<br><b>Mi:</b> Ordnen und Vergleichen üben (S. 15 Nr. 2, 6 · S. 12 Nr. 7 rechts, Fehlersuche).<br><b>Do:</b> Abstand zur Null, Zahl in der Mitte (S. 12 Nr. 9 bis 11), Kurzcheck.</td></tr>
<tr><td>3</td><td>28.9.–2.10.</td><td>Rationale Zahlen vergleichen und ordnen, Addition</td>
<td><b>Mo (IF, zweimal):</b> Einstieg Addition am Zahlenstrahl (Modell „laufende Glühbirne“ aus den Unterlagen).<br><b>Di:</b> Addition, Regeln finden und Merksätze.<br><b>Mi, Do:</b> Addition üben.</td></tr>
<tr><td>4</td><td>5.10.–9.10.</td><td>Subtraktion</td>
<td><b>Mo (IF):</b> Subtraktion als Gegenzahl-Addition am Zahlenstrahl.<br><b>Di:</b> Subtraktion, Merksätze.<br><b>Mi, Do:</b> Addition und Subtraktion gemischt üben.</td></tr>
<tr><td>5</td><td>12.10.–16.10.</td><td>Rechenvorteile, Multiplikation und Division</td>
<td>Sehr voll: eine Woche für Rechenvorteile <i>und</i> Multiplikation/Division. Frühzeitig Zeitpuffer prüfen.</td></tr>
<tr><td>6</td><td>19.10.–23.10.</td><td>Zeitfenster</td>
<td>Klassenarbeit 1 (Parallelarbeit einer anderen Lehrkraft). Hier Wiederholung und Vorbereitung einplanen.</td></tr>
<tr><td colspan="4"><i>Herbstferien 27.10.–31.10. Danach Woche 7: Verbinden der Rechenarten, Woche 8: Üben. Klassenarbeit 3 (deine) steht in Woche 16, Ende Januar, zum Thema Terme.</i></td></tr></table>
<h3>Offen</h3>
<ul><li>Buch S. 13 fehlt in den Scans, ich habe sie nicht benutzt.</li>
<li>Die Lösungen oben sind selbst gerechnet. Einmal mit dem digitalen Lösungsbuch gegenlesen, besonders S. 11 Nr. 6 (Einteilung ist Geschmack, die Lage der Punkte nicht).</li>
<li>Die Zeiten gehen von 90 Minuten ohne Pause aus.</li></ul>
</section>
"""

html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rationale Zahlen 1 – Zahlen unter Null</title><style>{CSS}</style></head><body>
<div class="wrap"><header class="kopf"><h1>Rationale Zahlen 1: Zahlen unter Null</h1>
<p class="sub">Klasse 7c · Doppelstunde am Dienstag · Buch S. 10–15 · alles in einer Datei</p></header></div>
<nav><div class="wrap"><a href="#vorher">Vor der Stunde</a><a href="#verlauf">Verlauf</a><a href="#folien">Folien</a><a href="#tafel">Tafelbild</a><a href="#merkheft">Merkheft</a>
<a href="#aufgaben">Aufgaben</a><a href="#loesungen">Lösungen</a><a href="#ausblick">Ausblick</a></div></nav>
<div class="wrap">{vorher}{verlauf}{folien}{tafel}{merkheft}{aufgaben}{loesungen}{ausblick}
<footer>Entwurf. PDFs erst nach Freigabe. Generator: baue_stunde1.py</footer></div></body></html>"""

ziel = Path(__file__).with_name("Rationale Zahlen 1 – Zahlen unter Null – ALLES.html")
ziel.write_text(html, encoding="utf-8")
print("geschrieben:", ziel, f"({len(html) // 1024} KB)")

# ---------------------------------------------------------------- Folien als eigene Datei (für PDF, Beamer)
FCSS = """
@page{size:13.333in 7.5in;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;padding:0}
body{font-family:-apple-system,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#1b1b1b;background:#fff}
.slide{width:13.333in;height:7.5in;padding:.42in .6in .3in;page-break-after:always;overflow:hidden;position:relative}
.slide:last-child{page-break-after:auto}
h1{font-size:48px;margin:0 0 .14in;line-height:1.1}
.neg{color:#b3261e}.pos{color:#1a56a0}
.s1{padding:0}
.banner{position:relative;height:320px}.banner img{display:block;width:100%;height:320px;object-fit:cover}
.titel{position:absolute;right:.6in;top:.22in;font-size:54px;font-weight:800;color:#fff;text-shadow:0 2px 10px rgba(0,40,90,.55)}
.chips{display:grid;grid-template-columns:repeat(8,1fr);gap:12px;padding:16px .35in 0}
.chips div{border:2px solid #cfcfc8;border-radius:12px;text-align:center;padding:7px 0 9px;background:#fbfbf9}
.chips small{display:block;color:#555;font-size:19px}.chips b{font-size:31px;white-space:nowrap}
.s1 .fragen{padding:.3in .6in 0 1.05in}
.fragen{font-size:34px;line-height:1.3;margin:0;padding-left:.45in}.fragen li{margin:.1in 0}
.zwei{display:flex;gap:.4in;align-items:flex-start}
.zwei svg{width:9.3in;height:auto;flex:none;border-radius:10px}
.zwei .fragen{font-size:31px;padding-left:.28in;margin-top:.1in}
"""
folien_html = f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>Folien – Zahlen unter Null</title>
<style>{FCSS}</style></head><body>
<div class="slide s1"><div class="banner">{skifoto()}<div class="titel">Skitag</div></div>
<div class="chips">{skichips()}</div>
<ul class="fragen"><li>Wann ist der Schnee hart gefroren, wann eher weich?</li>
<li>Hüttenwirt Franz: „Über Nacht bekommen wir wieder Neuschnee.“ Kann das sein?</li></ul></div>
<div class="slide"><h1>Wetterkarte</h1>
<div class="zwei">{wetterkarte()}
<ul class="fragen"><li>Über oder unter dem Gefrierpunkt?</li><li>Wo ist es kälter als in Berlin?</li><li>Wo ist es wärmer als in Stuttgart?</li></ul></div></div>
</body></html>"""
Path(__file__).with_name("Folien – Zahlen unter Null.html").write_text(folien_html, encoding="utf-8")
print("Folien-HTML geschrieben (PDF: Chrome headless --print-to-pdf, siehe Docstring)")
