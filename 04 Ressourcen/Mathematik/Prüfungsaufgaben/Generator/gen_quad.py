#!/usr/bin/env python3
import os, math

OUT = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben/Bilder"
os.makedirs(OUT, exist_ok=True)

UNIT = 26
M = 24
GRID = "#d8e4ee"
AXIS = "#333333"
TICK = "#666666"

def coord_svg(curves, xmin, xmax, ymin, ymax, labels=None):
    """curves: list of dicts {f, color, width(optional)}; labels: list {x,y,text,color}"""
    w = (xmax - xmin) * UNIT + 2 * M
    h = (ymax - ymin) * UNIT + 2 * M
    def X(x): return M + (x - xmin) * UNIT
    def Y(y): return M + (ymax - y) * UNIT
    s = []
    s.append(f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
             f'xmlns="http://www.w3.org/2000/svg" font-family="Arial,Helvetica,sans-serif">')
    s.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>')
    s.append(f'<clipPath id="plot"><rect x="{X(xmin)}" y="{Y(ymax)}" '
             f'width="{(xmax-xmin)*UNIT}" height="{(ymax-ymin)*UNIT}"/></clipPath>')
    # grid
    x = xmin
    while x <= xmax + 0.001:
        s.append(f'<line x1="{X(x):.1f}" y1="{Y(ymin):.1f}" x2="{X(x):.1f}" y2="{Y(ymax):.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        x += 1
    y = ymin
    while y <= ymax + 0.001:
        s.append(f'<line x1="{X(xmin):.1f}" y1="{Y(y):.1f}" x2="{X(xmax):.1f}" y2="{Y(y):.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        y += 1
    # axes
    s.append(f'<line x1="{X(xmin):.1f}" y1="{Y(0):.1f}" x2="{X(xmax)+8:.1f}" y2="{Y(0):.1f}" '
             f'stroke="{AXIS}" stroke-width="1.6"/>')
    s.append(f'<line x1="{X(0):.1f}" y1="{Y(ymin):.1f}" x2="{X(0):.1f}" y2="{Y(ymax)-8:.1f}" '
             f'stroke="{AXIS}" stroke-width="1.6"/>')
    # arrowheads
    ax, ay = X(xmax) + 8, Y(0)
    s.append(f'<polygon points="{ax},{ay} {ax-7},{ay-4} {ax-7},{ay+4}" fill="{AXIS}"/>')
    bx, by = X(0), Y(ymax) - 8
    s.append(f'<polygon points="{bx},{by} {bx-4},{by+7} {bx+4},{by+7}" fill="{AXIS}"/>')
    s.append(f'<text x="{ax-2:.1f}" y="{ay+16:.1f}" font-size="12" fill="{AXIS}">x</text>')
    s.append(f'<text x="{bx+8:.1f}" y="{by+4:.1f}" font-size="12" fill="{AXIS}">y</text>')
    # tick labels
    x = xmin
    while x <= xmax + 0.001:
        if int(round(x)) != 0:
            s.append(f'<text x="{X(x):.1f}" y="{Y(0)+13:.1f}" font-size="9" fill="{TICK}" '
                     f'text-anchor="middle">{int(round(x))}</text>')
        x += 1
    y = ymin
    while y <= ymax + 0.001:
        if int(round(y)) != 0:
            s.append(f'<text x="{X(0)-6:.1f}" y="{Y(y)+3.5:.1f}" font-size="9" fill="{TICK}" '
                     f'text-anchor="end">{int(round(y))}</text>')
        y += 1
    s.append(f'<text x="{X(0)-6:.1f}" y="{Y(0)+13:.1f}" font-size="9" fill="{TICK}" text-anchor="end">0</text>')
    # curves (clipped)
    s.append(f'<g clip-path="url(#plot)">')
    for c in curves:
        f = c["f"]; col = c["color"]; sw = c.get("width", 2.6)
        N = 600
        pts = []
        for i in range(N + 1):
            xv = xmin + (xmax - xmin) * i / N
            try:
                yv = f(xv)
            except Exception:
                continue
            yv = max(ymin - 3, min(ymax + 3, yv))
            pts.append(f"{X(xv):.2f},{Y(yv):.2f}")
        s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" '
                 f'stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
    s.append('</g>')
    # curve labels
    if labels:
        for lb in labels:
            s.append(f'<text x="{X(lb["x"]):.1f}" y="{Y(lb["y"]):.1f}" font-size="15" '
                     f'font-weight="bold" fill="{lb["color"]}">{lb["text"]}</text>')
    s.append('</svg>')
    return "\n".join(s)

def eq_card(eq):
    """Simple card with an equation for the 'quadratisch ergaenzen' tasks."""
    w, h = 330, 110
    s = []
    s.append(f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
             f'xmlns="http://www.w3.org/2000/svg" font-family="Georgia,\'Times New Roman\',serif">')
    s.append(f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="12" '
             f'fill="#f7fafd" stroke="#9cc3dd" stroke-width="2"/>')
    s.append(f'<text x="{w/2}" y="{h/2+12}" font-size="34" fill="#173b5e" '
             f'text-anchor="middle">{eq}</text>')
    s.append('</svg>')
    return "\n".join(s)

def write(name, content):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(content + "\n")
    print("wrote", name)

# ---------- Zuordnung 1 (Quad-Aufgabe-01) ----------
c1 = [
    {"f": lambda x: 0.5*x + 3,        "color": "#2563eb"},  # (1) Gerade steigend
    {"f": lambda x: x*x + 4*x + 3,    "color": "#d0392b"},  # (2) S(-2|-1)
    {"f": lambda x: 0.5*x*x + 3,      "color": "#2e9e5b"},  # (3) S(0|3) breit
    {"f": lambda x: x*x - 4*x + 3,    "color": "#e08a1e"},  # (4) S(2|-1)
    {"f": lambda x: -0.5*x + 3,       "color": "#7c3aed"},  # (5) Gerade fallend
]
l1 = [
    {"x": 3.1, "y": 4.7, "text": "A", "color": "#2563eb"},
    {"x": -4.3, "y": 4.3, "text": "B", "color": "#d0392b"},
    {"x": 2.4, "y": 6.2, "text": "C", "color": "#2e9e5b"},
    {"x": 4.3, "y": 4.0, "text": "D", "color": "#e08a1e"},
    {"x": -4.4, "y": 5.6, "text": "E", "color": "#7c3aed"},
]
write("Quad-Aufgabe-01.svg", coord_svg(c1, -6, 6, -2, 7, l1))

# ---------- Zuordnung 2 (Quad-Aufgabe-02) ----------
c2 = [
    {"f": lambda x: (x+3)**2 - 2,     "color": "#d0392b"},  # A  S(-3|-2)
    {"f": lambda x: x + 2,            "color": "#2563eb"},  # B  Gerade
    {"f": lambda x: (x+1)**2 - 3,     "color": "#7c3aed"},  # C  S(-1|-3)
    {"f": lambda x: 2*x*x - 3,        "color": "#e08a1e"},  # D  S(0|-3) eng
    {"f": lambda x: -0.5*x,           "color": "#0d9488"},  # E  Gerade fallend
    {"f": lambda x: -(x-1)**2 + 3,    "color": "#2e9e5b"},  # F  S(1|3) nach unten
]
l2 = [
    {"x": -4.8, "y": 1.6, "text": "A", "color": "#d0392b"},
    {"x": 2.4, "y": 4.6, "text": "B", "color": "#2563eb"},
    {"x": 0.7, "y": 3.0, "text": "C", "color": "#7c3aed"},
    {"x": 1.5, "y": 4.7, "text": "D", "color": "#e08a1e"},
    {"x": -5.0, "y": 2.7, "text": "E", "color": "#0d9488"},
    {"x": 1.6, "y": 2.7, "text": "F", "color": "#2e9e5b"},
]
write("Quad-Aufgabe-02.svg", coord_svg(c2, -6, 5, -4, 5, l2))

# ---------- Ablesen (Quad-Aufgabe-03..09) ----------
BLUE = "#2563eb"
ablesen = [
    ("03", lambda x: (x-2)**2 - 3,      -4, 6, -4, 6),
    ("04", lambda x: (x+1)**2 - 4,      -6, 4, -5, 6),
    ("05", lambda x: -(x-1)**2 + 4,     -4, 6, -6, 5),
    ("06", lambda x: 0.5*(x-1)**2 - 2,  -5, 6, -3, 6),
    ("07", lambda x: 2*(x+1)**2 - 3,    -5, 4, -4, 6),
    ("08", lambda x: -(x+2)**2 + 3,     -6, 3, -6, 4),
    ("09", lambda x: 0.5*(x+2)**2 - 4,  -6, 4, -5, 5),
]
for num, f, xa, xb, ya, yb in ablesen:
    write(f"Quad-Aufgabe-{num}.svg",
          coord_svg([{"f": f, "color": BLUE}], xa, xb, ya, yb))

# ---------- Quadratisch ergaenzen (Quad-Aufgabe-10..15) ----------
eqs = [
    ("10", "y = x² − 6x + 7"),
    ("11", "y = x² + 4x + 1"),
    ("12", "y = x² − 2x − 3"),
    ("13", "y = x² + 6x + 5"),
    ("14", "y = x² − 8x + 13"),
    ("15", "y = 2x² − 4x + 5"),
]
for num, eq in eqs:
    write(f"Quad-Aufgabe-{num}.svg", eq_card(eq))

print("done")
