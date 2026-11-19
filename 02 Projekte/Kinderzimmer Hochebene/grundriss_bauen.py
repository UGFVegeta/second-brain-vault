#!/usr/bin/env python3
# Erzeugt den Grundriss Kinderzimmer Hochebene (1 cm = S px)
import sys
S = 2.0
OX, OY = 110, 90          # Ursprung Innenecke links oben (Fensterwand oben)
W, L = 220, 317           # Raum innen (cm)
WALL = 14                 # Wandstärke gezeichnet (cm)
PH = 225                  # Oberkante Hochebene
PY = 140                  # Kante Hochebene an der Treppe (Abstand von Fensterwand)
PE = 107                  # Kante Hochebene im Raum (links der Treppe)
SX = 160                  # Treppe innen-Kante (Treppenbreite 60)
TREAD, RISE, N = 20, 28, 7  # 8 Stufen + Austritt = 9 Steigungen

def X(x): return OX + x * S
def Y(y): return OY + y * S
def r(x, y, w, h, cls="", extra=""):
    return f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" class="{cls}" {extra}/>'
def t(x, y, s, cls="lbl", extra=""):
    return f'<text x="{X(x):.1f}" y="{Y(y):.1f}" class="{cls}" {extra}>{s}</text>'
def ln(x1, y1, x2, y2, cls="thin"):
    return f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" class="{cls}"/>'

def dim_h(x1, x2, y, label, off=0):
    """horizontale Maßkette bei y (cm, kann negativ = außerhalb)"""
    o = []
    o.append(ln(x1, y, x2, y, "dim"))
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
    o = []
    # Wände
    o.append(f'<path class="wall" fill-rule="evenodd" d="M{X(-WALL)} {Y(-WALL)} H{X(W+WALL)} V{Y(L+WALL)} H{X(-WALL)} Z M{X(0)} {Y(0)} V{Y(L)} H{X(W)} V{Y(0)} Z"/>')
    # Fenster (oben)
    o.append(r(19, -WALL, 96, WALL, "win"))
    o.append(ln(19, -WALL/2, 115, -WALL/2, "thin"))
    o.append(ln(19, -WALL/2 - 2, 115, -WALL/2 - 2, "thin"))
    # Tür (unten), 96 mit Rahmen, mittig angenommen
    o.append(r(62, L, 96, WALL, "opening"))
    return "".join(o)

def door_swing():
    # Bänder rechts (Rad-Seite), geht nach innen auf
    hx = 153; leaf = 86
    o = [f'<line x1="{X(hx)}" y1="{Y(L)}" x2="{X(hx)}" y2="{Y(L-leaf)}" class="door"/>',
         f'<path d="M{X(hx-leaf)} {Y(L)} A{leaf*S} {leaf*S} 0 0 1 {X(hx)} {Y(L-leaf)}" class="swing"/>']
    return "".join(o)

def outer_dims():
    o = []
    o.append(dim_h(0, W, -WALL - 24, "220"))
    o.append(dim_h(0, 19, -WALL - 10, "19"))
    o.append(dim_h(19, 115, -WALL - 10, "96 Fenster"))
    o.append(dim_h(115, W, -WALL - 10, "101 (gem.)"))
    o.append(dim_v(0, L, -WALL - 14, "317"))
    o.append(dim_h(0, 62, L + WALL + 12, "ca. 62"))
    o.append(dim_h(62, 158, L + WALL + 12, "96 Tür m. Rahmen"))
    o.append(dim_h(158, W, L + WALL + 12, "ca. 62"))
    return "".join(o)

def stair_lines(cls="thin"):
    o = []
    for k in range(1, N):
        o.append(ln(SX, k * TREAD, W, k * TREAD, cls))
    return "".join(o)

# ---------------- UNTEN ----------------
def lower():
    o = [shell()]
    # Spielteppich
    o.append(f'<circle cx="{X(105)}" cy="{Y(62)}" r="{40*S}" class="rug"/>')
    o.append(t(105, 64, "Spielteppich", "lbl", 'text-anchor="middle"'))
    # Spieltisch an der Wand gegenüber
    o.append(r(0, 25, 50, 110, "table"))
    o.append(t(25, 86, "Spiel-", "sm", 'text-anchor="middle"'))
    o.append(t(25, 95, "tisch", "sm", 'text-anchor="middle"'))
    o.append(t(25, 104, "50×110", "tiny", 'text-anchor="middle"'))
    # Schubladen unter Stufen 1-3
    o.append(r(SX, 0, 60, 60, "furn"))
    for yy in (20, 40):
        o.append(ln(SX, yy, W, yy, "thin"))
    o.append(t(SX + 30, 27, "Schub-", "sm", 'text-anchor="middle"'))
    o.append(t(SX + 30, 35, "laden", "sm", 'text-anchor="middle"'))
    # Nische
    o.append(r(SX, 60, 60, PY - 60, "niche"))
    for yy in range(64, 134, 9):
        o.append(r(W - 12, yy, 10, 7, "book"))
    o.append(t(SX + 26, 96, "Lese-", "lbl", 'text-anchor="middle"'))
    o.append(t(SX + 26, 105, "nische", "lbl", 'text-anchor="middle"'))
    # Kleiderschrank unter Hochebene
    o.append(r(SX, PY, 60, L - PY, "furn"))
    o.append(ln(SX + 30, PY, SX + 30, L, "thin"))
    o.append(t(SX + 30, PY + 64, "Kleider-", "lbl", 'text-anchor="middle"'))
    o.append(t(SX + 30, PY + 73, "schrank", "lbl", 'text-anchor="middle"'))
    o.append(t(SX + 30, PY + 84, "bis 210 hoch", "sm", 'text-anchor="middle"'))
    # Treppe darüber (gestrichelt)
    o.append(r(SX, 0, 60, PY - 1, "over"))
    o.append(stair_lines("overl"))
    # Kante Hochebene darüber
    o.append(f'<path d="M{X(0)} {Y(PE)} H{X(SX)} V{Y(PY)} H{X(W)}" class="edge" fill="none"/>')
    o.append(t(54, PE + 8, "Kante Hochebene darüber (UK 2,10 m)", "sm"))
    o.append(t(4, PE + 108, "Eingang, Durchgangshöhe 2,10 m", "sm"))
    for yy in (145, 180, 215, 250, 285):
        o.append(ln(4, yy, SX - 4, yy, "led"))
    o.append(t(54, PE + 20, "LED-Leisten in der Untersicht (quer)", "tiny"))
    o.append(door_swing())
    # Steckdosen / Schalter (ca., aus Fotos)
    for (x, y) in [(150, 2), (50, L - 2)]:
        o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="5" class="sock"/>')
    o.append(t(140, 10, "Steckd.", "tiny", 'text-anchor="end"'))
    o.append(t(42, L - 6, "Steckd. + Schalter", "tiny", 'text-anchor="end"'))
    # Maße innen
    o.append(dim_v(0, 60, W + WALL + 10, "60"))
    o.append(dim_v(60, PY, W + WALL + 10, "80"))
    o.append(dim_v(PY, L, W + WALL + 10, "177"))
    o.append(dim_v(0, PE, SX - 12, "107 offen"))
    o.append(dim_h(SX, W, -WALL - 38, "60 Treppe"))
    o.append(outer_dims())
    return "".join(o)

# ---------------- OBEN ----------------
def posts():
    o = []
    # entlang Kante Hochebene (x 0..160) und offene Treppenseite (y 0..177)
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
    o.append(t(SX / 2, PE / 2 - 6, "Luftraum", "lbl", 'text-anchor="middle"'))
    o.append(t(SX / 2, PE / 2 + 6, "(Blick nach unten)", "sm", 'text-anchor="middle"'))
    o.append(f'<path d="M{X(0)} {Y(PE)} H{X(SX)} V{Y(PY)} H{X(W)} V{Y(L)} H{X(0)} Z" class="deck"/>')
    # Treppe
    o.append(r(SX, 0, 60, PY, "stair"))
    o.append(stair_lines())
    o.append(f'<path d="M{X(SX+30)} {Y(8)} V{Y(PY+16)}" class="arrow" marker-end="url(#ah)"/>')
    o.append(t(SX + 30, 4, "hoch", "sm", 'text-anchor="middle"'))
    # Bett, Nachttisch
    o.append(r(0, L - 120, 200, 120, "bed"))
    o.append(r(4, L - 114, 30, 108, "pillow"))
    o.append(t(110, L - 57, "Bett 120 × 200", "lbl", 'text-anchor="middle"'))
    o.append(r(0, PE + 12, 36, 36, "furn"))
    o.append(t(18, PE + 33, "Nachtt.", "tiny", 'text-anchor="middle"'))
    o.append(t(95, PE + 50, "Spielfläche oben 160 × 90", "sm", 'text-anchor="middle"'))
    o.append(posts())
    o.append(f'<path d="M{X(150)} {Y(88)} H{X(10)}" class="arrow" marker-end="url(#ah)"/>')
    o.append(t(80, 82, "Decke steigt: 4 m → 5 m", "sm", 'text-anchor="middle"'))
    o.append(t(SX / 2, PE - 6, "Kanthölzer 4×6 bis zur Decke", "sm", 'text-anchor="middle"'))
    # Maße
    o.append(dim_v(PE, L - 120, W + WALL + 10, "90"))
    o.append(dim_v(L - 120, L, W + WALL + 10, "120"))
    o.append(dim_v(0, PY, W + WALL + 10, "140 Treppe"))
    o.append(dim_v(PE, L, -WALL - 30, "210 Hochebene"))
    o.append(dim_h(0, 200, L - 126, "200"))
    o.append(outer_dims())
    return "".join(o)

# ---------------- SCHNITT ----------------
def section():
    s = 1.2; ox, oy = 70, 40; H = 420
    def x(c): return ox + c * s
    def y(h): return oy + (H - h) * s
    o = []
    o.append(f'<line x1="{x(0)}" y1="{y(0)}" x2="{x(L)}" y2="{y(0)}" class="ground"/>')
    o.append(f'<line x1="{x(0)}" y1="{y(0)}" x2="{x(0)}" y2="{y(400)}" class="wl"/>')
    o.append(f'<line x1="{x(L)}" y1="{y(0)}" x2="{x(L)}" y2="{y(400)}" class="wl"/>')
    o.append(f'<line x1="{x(0)}" y1="{y(400)}" x2="{x(L)}" y2="{y(400)}" class="ceil"/>')
    o.append(f'<text x="{x(L/2)}" y="{y(400)-6}" class="sm" text-anchor="middle">Decke an der Treppenwand ca. 4 m (niedrigste Seite)</text>')
    # Stufen
    pts = [f"{x(0)},{y(0)}"]
    for k in range(1, N + 1):
        pts.append(f"{x((k-1)*TREAD)},{y(k*RISE)}"); pts.append(f"{x(k*TREAD)},{y(k*RISE)}")
    pts.append(f"{x(PY)},{y(PH)}")
    o.append(f'<polyline points="{" ".join(pts)}" class="stp"/>')
    # Hochebene
    o.append(f'<rect x="{x(PE)}" y="{y(PH)}" width="{(PY-PE)*s}" height="{15*s}" class="deckS" style="fill:none;stroke-dasharray:4 3"/>')
    o.append(f'<rect x="{x(PY)}" y="{y(PH)}" width="{(L-PY)*s}" height="{15*s}" class="deckS"/>')
    # Stangen
    for c in range(0, PY, 11):
        o.append(f'<line x1="{x(c)+0.5}" y1="{y(c//TREAD*RISE+RISE if c<PY else PH)}" x2="{x(c)+0.5}" y2="{y(400)}" class="postS"/>')
    o.append(f'<line x1="{x(PY)}" y1="{y(PH)}" x2="{x(PY)}" y2="{y(400)}" class="postS"/>')
    # Bett
    o.append(f'<rect x="{x(L-120)}" y="{y(PH+20)}" width="{120*s}" height="{20*s}" class="bed"/>')
    # Tür
    o.append(f'<rect x="{x(L)-4}" y="{y(200)}" width="4" height="{200*s}" class="doorS"/>')
    # Nische
    ax0, ax1, ah = 66, 134, 90   # Bogenöffnung 68 breit, 90 hoch
    rr = (ax1 - ax0) / 2
    o.append(f'<path d="M{x(ax0)} {y(0)} V{y(ah-rr)} A{rr*s} {rr*s} 0 0 1 {x(ax1)} {y(ah-rr)} V{y(0)}" class="nicheS"/>')
    o.append(f'<text x="{x(121)}" y="{y(40)}" class="sm" text-anchor="middle">Lesenische</text>')
    o.append(f'<text x="{x(121)}" y="{y(28)}" class="tiny" text-anchor="middle">Bogen 68 × 90</text>')
    for k in range(1, N + 1):
        o.append(f'<line x1="{x((k-1)*TREAD)+2}" y1="{y(k*RISE)+3}" x2="{x(k*TREAD)-2}" y2="{y(k*RISE)+3}" class="ledS"/>')
    o.append(f'<line x1="{x(PY)+4}" y1="{y(210)+3}" x2="{x(L)-4}" y2="{y(210)+3}" class="ledS"/>')
    o.append(f'<text x="{x(40)}" y="{y(300)}" class="tiny">gelb = LED</text>')
    o.append(f'<text x="{x(40)}" y="{y(8)}" class="tiny" text-anchor="middle">Schubl.</text>')
    o.append(f'<text x="{x(247)}" y="{y(110)}" class="sm" text-anchor="middle">Kleiderschrank / Eingang</text>')
    # Höhenkoten
    for h, lab in [(0, "±0"), (112, "1,12"), (210, "2,10"), (PH, "2,25"), (400, "ca. 4,00")]:
        o.append(f'<text x="{x(L)+10}" y="{y(h)+4}" class="dimt">{lab}</text>')
    o.append(f'<text x="{x(0)}" y="{y(0)+18}" class="sm">Fenster</text>')
    o.append(f'<text x="{x(L)}" y="{y(0)+18}" class="sm" text-anchor="end">Tür</text>')
    o.append(f'<text x="{x(PY+60)}" y="{y(PH+70)}" class="sm" text-anchor="middle">Kopfhöhe hier ca. 1,75 m</text>')
    w = x(L) + 60; h = y(0) + 30
    return f'<svg viewBox="0 0 {w:.0f} {h:.0f}" class="sec">{"".join(o)}</svg>'

def plan(svg_inner):
    w = X(W + WALL) + 70; h = Y(L + WALL) + 60
    return f'''<svg viewBox="0 0 {w:.0f} {h:.0f}" class="plan">
<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1d1d1f"/></marker>
<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#c9b48f" stroke-width="2"/></pattern></defs>
{svg_inner}</svg>'''

html = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kinderzimmer Hochebene</title>
<style>
:root{{--ink:#1d1d1f;--mut:#6e6e73;--bg:#fbfaf7;--wood:#efe4cf}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:28px 20px 60px}}
h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:17px;margin:0 0 8px}}
.sub{{color:var(--mut);margin:0 0 22px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.card{{background:#fff;border:1px solid #e6e3dc;border-radius:12px;padding:16px}}
svg{{width:100%;height:auto;display:block}} .sec{{max-width:620px;margin:0 auto}}
.wall{{fill:#2b2b2b}} .win{{fill:#fff;stroke:#2b2b2b;stroke-width:1}} .opening{{fill:#fff}}
.thin{{stroke:#555;stroke-width:1}} .door{{stroke:#2b2b2b;stroke-width:3}} .swing{{fill:none;stroke:#888;stroke-width:1;stroke-dasharray:4 3}}
.dim{{stroke:#8a8a8a;stroke-width:.8}} .tick{{stroke:#555;stroke-width:1.2}}
.dimt{{font-size:11px;fill:#444}} .lbl{{font-size:13px;fill:#1d1d1f;font-weight:600}} .sm{{font-size:11px;fill:#555}} .tiny{{font-size:9.5px;fill:#555}}
.rug{{fill:#f3e7d3;stroke:#d8c3a0}} .furn{{fill:var(--wood);stroke:#8a6d3b;stroke-width:1.2}}
.niche{{fill:#fff;stroke:#8a6d3b;stroke-width:1.2;stroke-dasharray:5 3}} .table{{fill:#f6efe2;stroke:#8a6d3b}}
.over{{fill:none;stroke:#555;stroke-width:1;stroke-dasharray:6 4}} .overl{{stroke:#aaa;stroke-width:.8;stroke-dasharray:3 3}}
.edge{{stroke:#c0392b;stroke-width:1.4;stroke-dasharray:8 4}} .sock{{fill:#fff;stroke:#c0392b;stroke-width:1.5}}
.void{{fill:#f2f2f2}} .deck{{fill:url(#hatch);stroke:#8a6d3b}} .stair{{fill:var(--wood);stroke:#8a6d3b}}
.bed{{fill:#fff;stroke:#1d1d1f;stroke-width:1.4}} .pillow{{fill:#eee;stroke:#999}} .post{{fill:#c8a878}} .book{{fill:#9fc5b0;stroke:#6a8f7a}} .led{{stroke:#f2b705;stroke-width:2.5}} .ledS{{stroke:#f2b705;stroke-width:2.5}}
.arrow{{stroke:#1d1d1f;stroke-width:1.5;fill:none}}
.ground{{stroke:#2b2b2b;stroke-width:3}} .wl{{stroke:#2b2b2b;stroke-width:2}} .ceil{{stroke:#999;stroke-dasharray:6 4}}
.stp{{fill:var(--wood);stroke:#8a6d3b;stroke-width:1.4}} .deckS{{fill:var(--wood);stroke:#8a6d3b}} .postS{{stroke:#d9c09a;stroke-width:3}}
.doorS{{fill:#999}} .nicheS{{fill:#fff;stroke:#8a6d3b;stroke-dasharray:4 3}}
ul{{margin:6px 0 0;padding-left:18px}} li{{margin:3px 0}}
.open{{background:#fff8e6;border-color:#f0d58a}}
.vis{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}} .vis figure,.vis2 figure{{margin:0}} .vis2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .vis2 img{{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:8px;display:block}} .vis2 figcaption{{text-align:center;color:var(--mut);margin-top:6px}} .vis img{{width:100%;border-radius:8px;display:block}} .vis figcaption{{text-align:center;color:var(--mut);margin-top:6px}}
@media (max-width:800px){{.grid,.vis,.vis2{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>Kinderzimmer mit Hochebene</h1>
<p class="sub">Grundriss im Maßstab, alle Maße in cm. Oben im Bild liegt das Fenster, unten die Tür. Stand 18.11.2026, Entwurf 2.</p>
<div class="grid">
<div class="card"><h2>Untere Ebene</h2>{plan(lower())}</div>
<div class="card"><h2>Obere Ebene (Hochebene auf 2,25 m)</h2>{plan(upper())}</div>
</div>
<div class="card" style="margin-top:22px"><h2>So könnte es aussehen (Variante Weiß)</h2><div class="vis2"><figure><img src="Variante Weiß.png" alt="Blick vom Fenster zur Tür"><figcaption>Blick vom Fenster zur Tür</figcaption></figure><figure><img src="Von oben.png" alt="Blick von der obersten Stufe auf die Hochebene"><figcaption>Oben: Blick von der obersten Treppenstufe</figcaption></figure></div><p class="sub" style="margin:10px 0 0">KI-Bilder, nicht maßstäblich. Die Maße gelten nur im Plan oben.</p></div>
<div class="card" style="margin-top:22px"><h2>Deko-Ideen (gleicher Einbau, alles Weiß bleibt)</h2><div class="vis"><figure><img src="Deko Bagger und Dinos.png" alt="Bagger, Traktoren, Dinos"><figcaption>Bagger, Traktoren, Dinos</figcaption></figure><figure><img src="Deko Sonne Mond Sterne.png" alt="Sonne, Mond, Sterne"><figcaption>Sonne, Mond, Sterne</figcaption></figure><figure><img src="Deko Prinzessin Einhorn Feen.png" alt="Prinzessin, Einhorn, Feen, Ballett"><figcaption>Prinzessin, Einhorn, Feen, Ballett</figcaption></figure></div><p class="sub" style="margin:10px 0 0">KI-Bilder aus dem Originalbild abgeleitet, nur die Deko ist neu.</p></div>
<div class="card" style="margin-top:22px"><h2>Schnitt entlang der Treppenwand</h2>{section()}</div>
<div class="grid" style="margin-top:22px">
<div class="card"><h2>Eckdaten</h2><ul>
<li>Hochebene ca. 7 m²: neben der Treppe 160 × 210 tief, an der Treppe 60 × 177. Oberkante 2,25 m, Unterkante 2,10 m (Tür passt drunter). Am Fenster bleiben 107 cm offen, dort kommt das Licht nach unten.</li>
<li>Treppe 60 breit an der rechten Wand, 8 Steigungen à 28 cm, Auftritt 20 cm. Das ist steil (ca. 54°), so wie eine Raumspartreppe. Griffleiste an der Wand und Handlauf an den Kanthölzern einplanen.</li>
<li>Unter Stufe 1 bis 3: Schubladen. Unter Stufe 4 bis 7: Lesenische mit Bogenöffnung (ca. 68 breit, 90 hoch, 60 tief) für Kinderbücher.</li><li>Spieltisch an der gegenüberliegenden Wand (50 × 120), später Schreibtisch.</li>
<li>Unter der Hochebene rechts: Kleiderschrank 60 tief bis zur Türwand. Die Tür schlägt dagegen auf, Türstopper vorsehen.</li>
<li>Dachschräge quer zum Raum: an der Treppenwand ca. 4 m (oben ca. 1,75 m Kopfhöhe), an der gegenüberliegenden Wand ca. 5 m (oben ca. 2,75 m). Kopfende des Betts deshalb auf die hohe Seite.</li><li>Kanthölzer 4 × 6 cm in hellem Holz bis zur Decke, an Ebenenkante und offener Treppenseite, alle 11 cm (Lücke 7 cm, kleinkindtauglich).</li><li>LED-Streifen unter jeder Stufenkante und quer in der Untersicht der Hochebene (Balken parallel zur Türwand).</li><li>Fronten von Treppe und Schrank in Weiß (entschieden), Stufen und Lamellen in sehr hellem Holz.</li>
</ul></div>
<div class="card open"><h2>Noch offen / angenommen</h2><ul>

<li>Türlage: als mittig angenommen (je ca. 62). Bitte nachmessen.</li>
<li>Fenster: 19 + 96 + 101 = 216, der Raum misst 220. 4 cm fehlen, einmal nachmessen.</li>
<li>Steckdosen nur ungefähr aus den Fotos. Kein Heizkörper zu sehen, vermutlich Fußbodenheizung.</li>
<li>Treppe rechts, Bett 120 × 200 quer an der Türwand (Kopfende auf der hohen Seite).</li>
</ul></div>
</div>
</main></body></html>'''

open(sys.argv[1], "w", encoding="utf-8").write(html)
print("ok")
