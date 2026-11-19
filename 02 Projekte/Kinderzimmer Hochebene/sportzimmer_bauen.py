#!/usr/bin/env python3
# Erzeugt den Grundriss Sportzimmer (gleicher Raum wie Kinderzimmer Hochebene), 1 cm = S px
# Aufruf: python3 sportzimmer_bauen.py "Sportzimmer – Grundriss.html"
import sys
S = 2.0
OX, OY = 110, 90          # Ursprung Innenecke links oben (Fensterwand oben)
W, L = 220, 317           # Raum innen (cm)
WALL = 14
PH = 225                  # Oberkante Hochebene
PY = 140                  # Treppe endet hier (Austritt)
PE = 107                  # Kante Hochebene im Raum, wie beim Kinderzimmer
SX = 160                  # Treppe 60 breit an der rechten Wand
TREAD, RISE, N = 20, 28, 7

def X(x): return OX + x * S
def Y(y): return OY + y * S
def r(x, y, w, h, cls="", extra=""):
    return f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" class="{cls}" {extra}/>'
def t(x, y, s, cls="lbl", extra=""):
    return f'<text x="{X(x):.1f}" y="{Y(y):.1f}" class="{cls}" {extra}>{s}</text>'
def tc(x, y, s, cls="lbl"):
    return t(x, y, s, cls, 'text-anchor="middle"')
def ln(x1, y1, x2, y2, cls="thin"):
    return f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" class="{cls}"/>'

def dim_h(x1, x2, y, label):
    o = [ln(x1, y, x2, y, "dim")]
    for x in (x1, x2):
        o.append(f'<line x1="{X(x)-4:.1f}" y1="{Y(y)+4:.1f}" x2="{X(x)+4:.1f}" y2="{Y(y)-4:.1f}" class="tick"/>')
    o.append(t((x1 + x2) / 2, y - 2.5, label, "dimt", 'text-anchor="middle"'))
    return "".join(o)

def dim_v(y1, y2, x, label):
    o = [ln(x, y1, x, y2, "dim")]
    for y in (y1, y2):
        o.append(f'<line x1="{X(x)-4:.1f}" y1="{Y(y)+4:.1f}" x2="{X(x)+4:.1f}" y2="{Y(y)-4:.1f}" class="tick"/>')
    cx, cy = X(x) - 6, Y((y1 + y2) / 2)
    o.append(f'<text x="{cx:.1f}" y="{cy:.1f}" class="dimt" text-anchor="middle" transform="rotate(-90 {cx:.1f} {cy:.1f})">{label}</text>')
    return "".join(o)

def shell():
    return "".join([
        f'<path class="wall" fill-rule="evenodd" d="M{X(-WALL)} {Y(-WALL)} H{X(W+WALL)} V{Y(L+WALL)} H{X(-WALL)} Z M{X(0)} {Y(0)} V{Y(L)} H{X(W)} V{Y(0)} Z"/>',
        r(19, -WALL, 96, WALL, "win"),
        ln(19, -WALL/2, 115, -WALL/2), ln(19, -WALL/2 - 2, 115, -WALL/2 - 2),
        r(62, L, 96, WALL, "opening")])

def door_swing():
    hx, leaf = 153, 86
    return (f'<line x1="{X(hx)}" y1="{Y(L)}" x2="{X(hx)}" y2="{Y(L-leaf)}" class="door"/>'
            f'<path d="M{X(hx-leaf)} {Y(L)} A{leaf*S} {leaf*S} 0 0 1 {X(hx)} {Y(L-leaf)}" class="swing"/>')

def outer_dims():
    return "".join([dim_h(0, W, -WALL - 24, "220"), dim_v(0, L, -WALL - 14, "317")])

def stair_lines(cls="thin"):
    return "".join(ln(SX, k * TREAD, W, k * TREAD, cls) for k in range(1, N))

# ---------------- UNTEN ----------------
def lower():
    o = [shell()]
    o.append(r(0, 0, SX, L, "rubber"))
    # kompaktes Laufband quer im offenen, hohen Teil
    o.append(r(5, 14, 150, 75, "dev"))
    o.append(r(30, 24, 118, 55, "belt"))
    o.append(r(7, 16, 20, 71, "console"))
    o.append(tc(89, 47, "Laufband kompakt", "lblw"))
    o.append(tc(89, 59, "150 × 75, klappbar", "smw"))
    o.append(tc(89, 70, "Blick zur hohen Wand", "smw"))
    # Ringe + Seil von der Decke (über dem Laufband)
    for (x, y) in [(60, 98), (90, 98)]:
        o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{4*S}" class="ring"/>')
    o.append(t(98, 101, "Ringe von der Decke", "tiny"))
    # Kante Hochebene + Klimmzugstange
    o.append(f'<path d="M{X(0)} {Y(PE)} H{X(SX)} V{Y(PY)} H{X(W)}" class="edge" fill="none"/>')
    o.append(r(0, PE, 160, 3, "bar"))
    o.append(t(110, 155, "Klimmzugstange an der Kante", "tiny"))
    # Rad auf der Rolle an der linken Wand
    o.append(r(4, 118, 55, 180, "dev2"))
    o.append(ln(31, 130, 31, 286, "bike"))
    o.append(ln(10, 140, 52, 140, "bike"))
    o.append(f'<circle cx="{X(31)}" cy="{Y(262)}" r="{14*S}" class="trainer"/>')
    o.append(tc(31, 196, "Rad auf", "sm"))
    o.append(tc(31, 206, "der Rolle", "sm"))
    o.append(tc(31, 217, "180 × 55", "tiny"))
    o.append(r(0, 108, 3, 40, "tv"))
    o.append(t(6, 124, "TV", "tiny"))
    # Hanteln + Fläche
    o.append(r(66, 116, 40, 40, "furn"))
    for (x, y) in [(76, 126), (96, 126), (76, 146), (96, 146)]:
        o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{5*S}" class="db"/>')
    o.append(t(110, 132, "Hanteln,", "sm"))
    o.append(t(110, 142, "Kettlebells", "sm"))
    o.append(r(66, 162, 90, 64, "mat"))
    o.append(tc(111, 197, "Fläche Kraft", "sm"))
    # Treppe: Schubladen, Nische, Schrank (wie Kinderzimmer)
    o.append(r(SX, 0, 60, 60, "furn"))
    for yy in (20, 40):
        o.append(ln(SX, yy, W, yy))
    o.append(tc(SX + 30, 27, "Schub-", "sm"))
    o.append(tc(SX + 30, 35, "laden", "sm"))
    o.append(r(SX, 60, 60, PY - 60, "niche"))
    o.append(tc(SX + 28, 92, "Bogennische:", "sm"))
    o.append(tc(SX + 28, 102, "Medaillen,", "sm"))
    o.append(tc(SX + 28, 112, "Laufschuhe", "sm"))
    o.append(r(SX, PY, 60, L - PY, "furn"))
    o.append(ln(SX + 30, PY, SX + 30, L))
    o.append(tc(SX + 30, PY + 64, "Schrank", "lbl"))
    o.append(tc(SX + 30, PY + 76, "Sportkleidung,", "sm"))
    o.append(tc(SX + 30, PY + 86, "Schwimmzeug", "sm"))
    o.append(r(SX, 0, 60, PY - 1, "over"))
    o.append(stair_lines("overl"))
    o.append(door_swing())
    o.append(dim_v(0, PE, -WALL - 34, "107 offen bis 4–5 m"))
    o.append(dim_v(PE, L, -WALL - 34, "210 unter Hochebene (2,10 m)"))
    o.append(dim_h(5, 155, -WALL - 10, "150 Laufband"))
    o.append(dim_h(SX, W, -WALL - 10, "60"))
    o.append(outer_dims())
    return "".join(o)

# ---------------- OBEN ----------------
def posts():
    o = []
    x = 3
    while x <= SX - 2:
        o.append(f'<rect x="{X(x)-2*S}" y="{Y(PE)-3*S}" width="{4*S}" height="{6*S}" class="post"/>'); x += 11
    y = 3
    while y <= PY - 6:
        o.append(f'<rect x="{X(SX)-3*S}" y="{Y(y)-2*S}" width="{6*S}" height="{4*S}" class="post"/>'); y += 11
    return "".join(o)

def upper():
    o = [shell()]
    o.append(r(0, 0, SX, PE, "void"))
    o.append(tc(SX / 2, PE / 2 - 6, "Luftraum", "lbl"))
    o.append(tc(SX / 2, PE / 2 + 6, "(unten das Laufband)", "sm"))
    o.append(f'<path d="M{X(0)} {Y(PE)} H{X(SX)} V{Y(PY)} H{X(W)} V{Y(L)} H{X(0)} Z" class="deck"/>')
    o.append(r(SX, 0, 60, PY, "stair"))
    o.append(stair_lines())
    o.append(f'<path d="M{X(SX+30)} {Y(8)} V{Y(PY+16)}" class="arrow" marker-end="url(#ah)"/>')
    o.append(tc(SX + 30, 4, "hoch", "sm"))
    # wo beim Kind das Bett liegt: Matte
    o.append(r(4, L - 66, 196, 62, "mat"))
    o.append(tc(102, L - 32, "Matte 190 × 60 (Stabi, Mobility)", "sm"))
    # Zugseile an den Lamellen
    o.append(f'<path d="M{X(55)} {Y(PE)} L{X(66)} {Y(152)} M{X(85)} {Y(PE)} L{X(74)} {Y(152)}" class="cord"/>')
    o.append(t(92, 128, "Zugseile an den Lamellen", "tiny"))
    o.append(t(92, 138, "(Schwimmen)", "tiny"))
    # Sitzsack, Pokale, Beamer
    o.append(f'<ellipse cx="{X(180)}" cy="{Y(200)}" rx="{28*S}" ry="{34*S}" class="bag"/>')
    o.append(tc(180, 203, "Sitzsack", "sm"))
    o.append(r(0, PE + 12, 36, 36, "furn"))
    o.append(tc(18, PE + 33, "Pokale", "tiny"))
    o.append(r(120, 205, 26, 16, "furn"))
    o.append(tc(133, 216, "Beamer", "tiny"))
    o.append(posts())
    o.append(f'<path d="M{X(150)} {Y(88)} H{X(10)}" class="arrow" marker-end="url(#ah)"/>')
    o.append(tc(80, 82, "Decke steigt: 4 m → 5 m", "sm"))
    o.append(tc(SX / 2, PE - 6, "Kanthölzer 4×6 bis zur Decke", "sm"))
    o.append(dim_v(PE, L, -WALL - 34, "210 Hochebene"))
    o.append(dim_v(0, PY, W + WALL + 10, "140 Treppe"))
    o.append(outer_dims())
    return "".join(o)

# ---------------- SCHNITT (entlang der hohen Wand, links) ----------------
def section():
    s = 1.0; ox, oy = 60, 30; H = 520
    def x(c): return ox + c * s
    def y(h): return oy + (H - h) * s
    o = []
    o.append(f'<line x1="{x(0)}" y1="{y(0)}" x2="{x(L)}" y2="{y(0)}" class="ground"/>')
    o.append(f'<line x1="{x(0)}" y1="{y(0)}" x2="{x(0)}" y2="{y(500)}" class="wl"/>')
    o.append(f'<line x1="{x(L)}" y1="{y(0)}" x2="{x(L)}" y2="{y(500)}" class="wl"/>')
    o.append(f'<line x1="{x(0)}" y1="{y(500)}" x2="{x(L)}" y2="{y(500)}" class="ceil"/>')
    o.append(f'<text x="{x(L/2)}" y="{y(500)-6}" class="sm" text-anchor="middle">Decke an der hohen Wand ca. 5 m</text>')
    # Laufband quer: im Schnitt nur 75 breit
    o.append(f'<rect x="{x(14)}" y="{y(20)}" width="{75*s}" height="{20*s}" class="devS"/>')
    rx = 52
    o.append(f'<circle cx="{x(rx)}" cy="{y(20+180-12)}" r="12" class="person"/>')
    o.append(f'<line x1="{x(rx)}" y1="{y(20+180-24)}" x2="{x(rx)}" y2="{y(20+90)}" class="personL"/>')
    o.append(f'<line x1="{x(rx)}" y1="{y(20+90)}" x2="{x(rx-14)}" y2="{y(22)}" class="personL"/>')
    o.append(f'<line x1="{x(rx)}" y1="{y(20+90)}" x2="{x(rx+14)}" y2="{y(40)}" class="personL"/>')
    o.append(f'<text x="{x(rx)}" y="{y(230)}" class="tiny" text-anchor="middle">Läufer frei nach oben</text>')
    # Ringe + Seil
    o.append(f'<line x1="{x(60)}" y1="{y(500)}" x2="{x(60)}" y2="{y(260)}" class="strap"/>')
    o.append(f'<circle cx="{x(60)}" cy="{y(253)}" r="7" class="ringS"/>')
    o.append(f'<text x="{x(70)}" y="{y(256)}" class="tiny">Ringe</text>')
    # Hochebene ab 107
    o.append(f'<rect x="{x(PE)}" y="{y(PH)}" width="{(L-PE)*s}" height="{15*s}" class="deckS"/>')
    o.append(f'<line x1="{x(PE)}" y1="{y(PH)}" x2="{x(PE)}" y2="{y(500)}" class="postS"/>')
    o.append(f'<text x="{x(PE)+8}" y="{y(196)}" class="tiny">Klimmzugstange</text>')
    o.append(f'<line x1="{x(PE)}" y1="{y(208)}" x2="{x(PE)+6}" y2="{y(208)}" class="wl"/>')
    # Rad auf der Rolle unter der Ebene
    o.append(f'<circle cx="{x(150)}" cy="{y(34)}" r="34" class="wheel"/>')
    o.append(f'<rect x="{x(250)}" y="{y(40)}" width="30" height="40" class="devS"/>')
    o.append(f'<path d="M{x(150)} {y(34)} L{x(190)} {y(95)} L{x(250)} {y(95)} L{x(265)} {y(40)} M{x(190)} {y(95)} L{x(180)} {y(110)} M{x(250)} {y(95)} L{x(240)} {y(105)}" class="bikeS"/>')
    o.append(f'<text x="{x(210)}" y="{y(150)}" class="sm" text-anchor="middle">Rad auf der Rolle</text>')
    o.append(f'<text x="{x(210)}" y="{y(136)}" class="tiny" text-anchor="middle">unter der Ebene, 2,10 m reicht</text>')
    o.append(f'<rect x="{x(PE)+8}" y="{y(PH)-4}" width="{196*s}" height="4" class="matS"/>')
    o.append(f'<text x="{x(212)}" y="{y(PH+120)}" class="tiny" text-anchor="middle">oben Kopfhöhe ca. 2,75 m</text>')
    for h, lab in [(0, "±0"), (210, "2,10"), (PH, "2,25"), (500, "ca. 5,00")]:
        o.append(f'<text x="{x(L)+10}" y="{y(h)+4}" class="dimt">{lab}</text>')
    o.append(f'<text x="{x(0)}" y="{y(0)+18}" class="sm">Fensterwand</text>')
    o.append(f'<text x="{x(L)}" y="{y(0)+18}" class="sm" text-anchor="end">Türwand</text>')
    w = x(L) + 60; h = y(0) + 30
    return f'<svg viewBox="0 0 {w:.0f} {h:.0f}" class="sec">{"".join(o)}</svg>'

def plan(inner):
    w = X(W + WALL) + 70; h = Y(L + WALL) + 60
    return f'''<svg viewBox="0 0 {w:.0f} {h:.0f}" class="plan">
<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1d1d1f"/></marker>
<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#c9b48f" stroke-width="2"/></pattern></defs>
{inner}</svg>'''

html = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sportzimmer Hochebene</title>
<style>
:root{{--ink:#1d1d1f;--mut:#6e6e73;--bg:#f6f5f2;--wood:#e6d3b0}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:28px 20px 60px}}
h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:17px;margin:0 0 8px}}
.sub{{color:var(--mut);margin:0 0 22px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.card{{background:#fff;border:1px solid #e3e0d9;border-radius:12px;padding:16px}}
svg{{width:100%;height:auto;display:block}} .sec{{max-width:560px;margin:0 auto}}
.wall{{fill:#2b2b2b}} .win{{fill:#fff;stroke:#2b2b2b}} .opening{{fill:#fff}}
.thin{{stroke:#555;stroke-width:1}} .door{{stroke:#2b2b2b;stroke-width:3}} .swing{{fill:none;stroke:#888;stroke-dasharray:4 3}}
.dim{{stroke:#8a8a8a;stroke-width:.8}} .tick{{stroke:#555;stroke-width:1.2}}
.dimt{{font-size:11px;fill:#444}} .lbl{{font-size:13px;fill:#1d1d1f;font-weight:600}} .sm{{font-size:11px;fill:#444}} .tiny{{font-size:9.5px;fill:#555}} .lblw{{font-size:13px;fill:#fff;font-weight:600}} .smw{{font-size:11px;fill:#eee}}
.rubber{{fill:#e4e4e4}} .furn{{fill:var(--wood);stroke:#8a6d3b;stroke-width:1.2}}
.dev{{fill:#cfd3d8;stroke:#2b2b2b;stroke-width:1.4}} .belt{{fill:#3a3a3a}} .console{{fill:#8b9096}}
.dev2{{fill:#dfe9f3;stroke:#2b5d8a;stroke-width:1.2;stroke-dasharray:5 3}} .bike{{stroke:#2b5d8a;stroke-width:3}} .trainer{{fill:#2b5d8a}}
.tv{{fill:#111}} .ring{{fill:none;stroke:#8a6d3b;stroke-width:3}} .rope{{fill:#c9a66b;stroke:#8a6d3b}}
.bar{{fill:#2b2b2b}} .db{{fill:#444}} .mat{{fill:#3f4a3c;opacity:.35;stroke:#3f4a3c}}
.edge{{stroke:#c0392b;stroke-width:1.4;stroke-dasharray:8 4}}
.overl{{stroke:#aaa;stroke-width:.8;stroke-dasharray:3 3}}
.void{{fill:#f2f2f2}} .deck{{fill:url(#hatch);stroke:#8a6d3b}} .stair{{fill:var(--wood);stroke:#8a6d3b}}
.post{{fill:#c8a878}} .cord{{stroke:#d35400;stroke-width:2;fill:none}} .bag{{fill:#6b6f75;opacity:.55;stroke:#444}}
.arrow{{stroke:#1d1d1f;stroke-width:1.5;fill:none}}
.ground{{stroke:#2b2b2b;stroke-width:3}} .wl{{stroke:#2b2b2b;stroke-width:2}} .ceil{{stroke:#999;stroke-dasharray:6 4}}
.deckS{{fill:var(--wood);stroke:#8a6d3b}} .postS{{stroke:#d9c09a;stroke-width:3}} .winS{{fill:#cfe3f3;stroke:#2b2b2b}}
.devS{{fill:#cfd3d8;stroke:#2b2b2b}} .devL{{stroke:#2b2b2b;stroke-width:3}} .person{{fill:none;stroke:#2b5d8a;stroke-width:2}} .personL{{stroke:#2b5d8a;stroke-width:2.5}}
.strap{{stroke:#c9a66b;stroke-width:1.5}} .ringS{{fill:none;stroke:#8a6d3b;stroke-width:3}} .ropeS{{stroke:#c9a66b;stroke-width:4}}
  .niche{{fill:#fff;stroke:#8a6d3b;stroke-width:1.2;stroke-dasharray:5 3}} .over{{fill:none;stroke:#555;stroke-width:1;stroke-dasharray:6 4}} .wheel{{fill:none;stroke:#2b5d8a;stroke-width:2.5}} .bikeS{{fill:none;stroke:#2b5d8a;stroke-width:2.5}} .furnS{{fill:var(--wood);stroke:#8a6d3b}} .matS{{fill:#3f4a3c}}
ul{{margin:6px 0 0;padding-left:18px}} li{{margin:3px 0}}
.open{{background:#fff8e6;border-color:#f0d58a}}
.vis2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .vis2 figure{{margin:0}} .vis2 img{{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:8px;display:block}} .vis2 figcaption{{text-align:center;color:var(--mut);margin-top:6px}}
@media (max-width:800px){{.grid,.vis2{{grid-template-columns:1fr}}}}
</style><body><main>
<h1>Sportzimmer mit Hochebene</h1>
<p class="sub">Gleicher Umbau wie beim Kinderzimmer (Hochebene, Treppe, Lamellen, Fronten, LEDs). Nur die Einrichtung ist getauscht, so kann das Zimmer später zum Sportzimmer werden. Maßstab, alle Maße in cm. Oben im Bild das Fenster, unten die Tür. Stand 19.11.2026.</p>
<div class="grid">
<div class="card"><h2>Untere Ebene</h2>{plan(lower())}</div>
<div class="card"><h2>Obere Ebene (Hochebene auf 2,25 m)</h2>{plan(upper())}</div>
</div>
<div class="card" style="margin-top:22px"><h2>So könnte es aussehen</h2><div class="vis2"><figure><img src="Sportzimmer – Ansicht.png" alt="Blick vom Fenster zur Tür"><figcaption>Blick vom Fenster zur Tür</figcaption></figure><figure><img src="Sportzimmer – Oben.png" alt="Blick oben auf der Hochebene"><figcaption>Oben: Blick von der obersten Stufe</figcaption></figure></div><p class="sub" style="margin:10px 0 0">KI-Bilder aus den Kinderzimmer-Bildern abgeleitet, nicht maßstäblich. Es gilt der Plan.</p></div>
<div class="card" style="margin-top:22px"><h2>Schnitt entlang der hohen Wand (links)</h2>{section()}</div>
<div class="grid" style="margin-top:22px">
<div class="card"><h2>Was bleibt, was sich ändert</h2><ul>
<li>Bleibt: Hochebene, Treppe mit Schubladen, Bogennische, Schrank, Lamellen bis zur Decke, LEDs, weiße Fronten, Fenster und Tür.</li>
<li>Spielteppich und Tisch raus, schwarze Gummimatten rein.</li>
<li>Im offenen, hohen Teil (107 × 160) passt nur ein kompaktes Laufband, quer gestellt: ca. 150 × 75 (z. B. Decathlon Compact Run 100). Ein großes Band mit 185 cm passt nicht, und unter die Ebene darf es nicht, weil man beim Laufen mit Band auf gut 2,10 m kommt.</li>
<li>Unter der Ebene an der linken Wand: Rad auf der Rolle, 2,10 m reichen zum Radfahren. Fernseher an der Wand davor.</li>
<li>Daneben Hanteln und eine kleine Fläche für Kraftübungen. Klimmzugstange an der Kante der Ebene.</li>
<li>Ringe hängen von der hohen Decke über dem Laufband, zum Laufen hochbinden.</li>
<li>Bogennische: Medaillen und Laufschuhe statt Kinderbücher. Schrank: Sportkleidung und Schwimmzeug.</li>
<li>Oben, wo das Bett lag: Matte, Zugseile an den Lamellen fürs Schwimmen, Sitzsack, Beamer auf die Schräge, Pokale statt Nachttisch.</li>
</ul></div>
<div class="card open"><h2>Ehrlich angemerkt</h2><ul>
<li>Das kompakte Laufband hat eine kürzere Lauffläche als ein normales. Für lockere Läufe okay, für schnelle Intervalle eher knapp.</li>
<li>Schwimm-Zugbank (Vasa SwimErg, ca. 259 × 71) passt nicht. Zugseile reichen.</li>
<li>Laufband und Rolle im Obergeschoss machen Trittschall. Dicke Gummimatten unter die Geräte.</li>
<li>Türlage weiter als mittig angenommen.</li>
</ul></div>
</div>
</main></body></html>'''

open(sys.argv[1], "w", encoding="utf-8").write(html)
print("ok")
