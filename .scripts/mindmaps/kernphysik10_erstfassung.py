#!/usr/bin/env python3
"""Mindmap Kernphysik Klasse 10 als .excalidraw (Inhalte aus Kernphysik.html, Merksätze der sechs Leitfragen)."""
import json, sys, random

random.seed(7)
E = []
GRUPPE = []   # aktuelle Gruppe: Kasten, Punkte und Zeichnung eines Astes bewegen sich zusammen
FS_CH = 0.6  # Zeichenbreite je fontSize (fontFamily 3, monospace)


def base(t, x, y, w, h, **k):
    d = dict(id=k.pop("id", f"e{len(E)}"), type=t, x=x, y=y, width=w, height=h, angle=0,
             strokeColor=k.pop("stroke", "#1e3a5f"), backgroundColor=k.pop("fill", "transparent"),
             fillStyle="solid", strokeWidth=k.pop("sw", 2), strokeStyle=k.pop("style", "solid"), roughness=0,
             opacity=100, groupIds=list(GRUPPE), frameId=None, roundness=k.pop("round", None), seed=random.randint(1, 2**31),
             version=1, versionNonce=random.randint(1, 2**31), isDeleted=False, boundElements=[], updated=1,
             link=None, locked=False)
    d.update(k)
    E.append(d)
    return d


def text(x, y, s, fs=18, col="#374151", align="left", cont=None, w=None):
    zeilen = s.split("\n")
    ww = w or max(len(z) for z in zeilen) * fs * FS_CH
    hh = len(zeilen) * fs * 1.25
    d = base("text", x, y, ww, hh, stroke=col, sw=1, text=s, originalText=s, fontSize=fs, fontFamily=3,
             textAlign=align, verticalAlign="middle" if cont else "top", containerId=cont["id"] if cont else None,
             lineHeight=1.25, baseline=int(fs))
    if cont:
        cont["boundElements"].append({"type": "text", "id": d["id"]})
    return d


def box(x, y, w, h, s, fs, fill, stroke, typ="rectangle", tcol="#1f2937"):
    b = base(typ, x, y, w, h, fill=fill, stroke=stroke, round={"type": 3} if typ == "rectangle" else {"type": 2})
    zeilen = s.split("\n")
    tw, th = max(len(z) for z in zeilen) * fs * FS_CH, len(zeilen) * fs * 1.25
    text(x + (w - tw) / 2, y + (h - th) / 2, s, fs, tcol, "center", b, tw)
    return b


def ell(cx, cy, r, fill, stroke="#1e3a5f", sw=1.5, rx=None, ry=None, style="solid"):
    rx, ry = rx or r, ry or r
    return base("ellipse", cx - rx, cy - ry, 2 * rx, 2 * ry, fill=fill, stroke=stroke, sw=sw, style=style)


def rect(x, y, w, h, fill, stroke="#1e3a5f", sw=1.5):
    return base("rectangle", x, y, w, h, fill=fill, stroke=stroke, sw=sw)


def pfeil(pts, col="#1e3a5f", sw=2, a=None, b=None, style="solid", head="arrow"):
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    xs, ys = [p[0] for p in rel], [p[1] for p in rel]
    d = base("arrow", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke=col, sw=sw, style=style, points=rel,
             lastCommittedPoint=None, startArrowhead=None, endArrowhead=head, round={"type": 2},
             startBinding={"elementId": a["id"], "focus": 0, "gap": 6} if a else None,
             endBinding={"elementId": b["id"], "focus": 0, "gap": 6} if b else None)
    for el in (a, b):
        if el:
            el["boundElements"].append({"type": "arrow", "id": d["id"]})
    return d


def linie(pts, col="#64748b", sw=1.5, style="solid"):
    """Achsen/Kurven in Zeichnungen (nicht verbindend)."""
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    xs, ys = [p[0] for p in rel], [p[1] for p in rel]
    return base("line", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke=col, sw=sw, style=style, points=rel,
                lastCommittedPoint=None, startArrowhead=None, endArrowhead=None, round=None)


# ---------------------------------------------------------------- Farben je Leitfrage
F = [("#dbeafe", "#1e40af"), ("#fed7aa", "#c2410c"), ("#fef3c7", "#b45309"),
     ("#fee2e2", "#dc2626"), ("#ddd6fe", "#6d28d9"), ("#a7f3d0", "#047857")]
PROTON, NEUTRON, ELEKTRON = "#f87171", "#cbd5e1", "#3b82f6"

# ---------------------------------------------------------------- Mitte
mitte = box(-230, -75, 460, 150, "Kernphysik\nKlasse 10", 34, "#1e293b", "#0f172a", "ellipse", "#ffffff")

# Äste: oben LF1–3, unten LF4–6 (in die Breite)
XS = [-1250, 0, 1250]
AST = []
TITEL = ["1  Woraus besteht\nMaterie?", "2  Warum zerfallen\nmanche Kerne?", "3  Wie schnell zerfällt\nein Stoff?",
         "4  Was macht Strahlung\nmit dem Körper?", "5  Energie aus\ndem Atomkern", "6  Nutzen und Risiko:\nWie entscheiden wir?"]
for i, t in enumerate(TITEL):
    x, y = XS[i % 3], -260 if i < 3 else 260
    b = box(x - 190, y - 55, 380, 110, t, 22, F[i][0], F[i][1])
    AST.append(b)
    if i % 3 == 1:
        pfeil([(0, -75 if i < 3 else 75), (0, y + (55 if i < 3 else -55))], F[i][1], 2.5, mitte, b)
    else:
        sx = -200 if i % 3 == 0 else 200
        pfeil([(sx, -40 if i < 3 else 40), (x, y + (55 if i < 3 else -55))], F[i][1], 2.5, mitte, b)

# ---------------------------------------------------------------- Detailblöcke
def block(i, x, y, zeilen, fs=17):
    """Großer Kasten je Ast mit vier Punkt-Kästen (Text fest im Kasten) und Platz für die Zeichnung rechts.
    Ein gerader, an beiden Enden gebundener Pfeil vom Ast zum großen Kasten."""
    global GRUPPE
    b, (hell, col) = AST[i], F[i]
    X = b["x"] + b["width"] / 2
    oben = b["y"] < 0
    H = 4 * 92 + 28
    ky = b["y"] - 60 - H if oben else b["y"] + b["height"] + 60
    GRUPPE = [f"ast{i}"]
    kasten = base("rectangle", X - 560, ky, 1090, H, fill=hell, stroke=col, sw=2, round={"type": 3})
    for k, (titel, sub) in enumerate(zeilen):
        box(X - 545, ky + 16 + k * 92, 625, 80, f"{titel}\n{sub}", fs, "#ffffff", col, tcol=col)
    GRUPPE = []
    if oben:
        pfeil([(X, b["y"]), (X, ky + H)], col, 2.5, b, kasten)
    else:
        pfeil([(X, b["y"] + b["height"]), (X, ky)], col, 2.5, b, kasten)
    GRUPPE = [f"ast{i}"]


# LF1 Atombau (oben links): Zeichnung Atom + Punkte
X1, Y1 = -1250, -260
block(0, X1 - 540, Y1 - 520, [
    ("Kern: Protonen (+) und Neutronen", "winzig, schwer, fast die ganze Masse"),
    ("Hülle: Elektronen (−)", "fast leer; Atom nach außen neutral"),
    ("A = Z + N", "Massenzahl = Protonen + Neutronen"),
    ("Isotope", "gleiches Z, anderes N; z. B. U-235 und U-238"),
])
# Atom-Zeichnung
ax, ay = X1 + 330, Y1 - 360
ell(ax, ay, 0, "transparent", "#94a3b8", 1, rx=120, ry=50, style="dashed")
ell(ax, ay, 0, "transparent", "#94a3b8", 1, rx=50, ry=110, style="dashed")
for dx, dy, c in ((-9, -7, PROTON), (7, -8, NEUTRON), (-8, 8, NEUTRON), (8, 7, PROTON), (0, 0, PROTON)):
    ell(ax + dx, ay + dy, 9, c, "#475569", 1)
ell(ax + 120, ay, 8, ELEKTRON, "#1e40af", 1)
ell(ax - 120, ay, 8, ELEKTRON, "#1e40af", 1)
ell(ax, ay - 110, 8, ELEKTRON, "#1e40af", 1)
text(ax - 75, ay + 125, "p  n  e⁻", 15, "#64748b", "center", w=150)

# LF2 Radioaktivität (oben Mitte): Durchdringung
X2, Y2 = 0, -260
block(1, X2 - 540, Y2 - 520, [
    ("Instabile Kerne zerfallen spontan", "wann genau: reiner Zufall"),
    ("α: Heliumkern (2p + 2n)", "A − 4, Z − 2"),
    ("β⁻: Neutron wird Proton + Elektron", "A gleich, Z + 1;  γ: nur Energie"),
    ("Zerfallsgleichung, Zerfallsreihe", "U-238 → Th-234 + α;  oben und unten gleich"),
])
# Durchdringung: Quelle, Papier, Alu, Blei
qx, qy = X2 + 150, Y2 - 420
ell(qx, qy + 60, 16, "#facc15", "#b45309", 1.5)
text(qx - 60, qy + 88, "Präparat", 14, "#475569", w=68)
for k, (nm, xx, w, c) in enumerate((("Papier", 60, 6, "#f8fafc"), ("Alu", 130, 14, "#cbd5e1"), ("Blei", 210, 30, "#64748b"))):
    rect(qx + xx, qy, w, 120, c, "#475569", 1)
    text(qx + xx + w / 2 - len(nm) * 4.2, qy + 128, nm, 14, "#475569", w=len(nm) * 8.4)
for k, (nm, stop, c) in enumerate((("α", 58, "#c2410c"), ("β", 128, "#1e40af"), ("γ", 290, "#6d28d9"))):
    yy = qy + 25 + k * 35
    pfeil([(qx + 18, yy), (qx + stop, yy)], c, 2)
    text(qx + 20, yy - 22, nm, 16, c, w=12)

# LF3 Halbwertszeit (oben rechts): Kurve
X3, Y3 = 1250, -260
block(2, X3 - 540, Y3 - 520, [
    ("Halbwertszeit T", "nach T ist die Hälfte der Kerne zerfallen"),
    ("immer halbieren, nicht gleichmäßig", "100 % → 50 % → 25 % → 12,5 %"),
    ("Aktivität A in Becquerel (Bq)", "Zerfälle pro Sekunde; Zählrohr misst die Zählrate"),
    ("Würfelmodell, Bierschaum", "Nullrate vorher abziehen"),
])
gx, gy, gw, gh = X3 + 190, Y3 - 190, 280, 230   # Ursprung unten links
pfeil([(gx, gy), (gx + gw + 20, gy)], "#475569", 1.5)
pfeil([(gx, gy), (gx, gy - gh - 20)], "#475569", 1.5)
text(gx - 20, gy - gh - 48, "N", 16, "#475569", w=12)
text(gx + gw + 10, gy + 6, "t", 16, "#475569", w=12)
pts = [(gx + k * gw / 40, gy - gh * 0.5 ** (k / 10)) for k in range(41)]
linie(pts, F[2][1], 2.5)
for k, lab in ((1, "T"), (2, "2T"), (3, "3T")):
    px, py = gx + k * gw / 4, gy - gh * 0.5 ** k
    linie([(px, gy), (px, py), (gx, py)], "#94a3b8", 1, "dashed")
    text(px - 10, gy + 6, lab, 14, "#475569", w=24)
text(gx - 50, gy - gh - 8, "100 %", 12, "#64748b", w=40)
text(gx - 42, gy - gh / 2 - 8, "50 %", 12, "#64748b", w=34)

# LF4 Körper (unten links): Ionisation
X4, Y4 = -1250, 260
block(3, X4 - 540, Y4 + 120, [
    ("ionisierend", "schlägt Elektronen aus Atomen: Ion entsteht"),
    ("trifft die DNA im Zellkern", "Zelle repariert, stirbt ab oder verändert sich (Krebs)"),
    ("Dosis in Millisievert (mSv)", "natürlich 2,1 mSv; Medizin etwa 1,5 mSv pro Jahr"),
    ("Schutz: Abstand, kurze Zeit, Abschirmung", "Nutzen: Medizin, Sterilisation, Werkstoffprüfung"),
])
ix, iy = X4 + 340, Y4 + 300
pfeil([(ix - 140, iy - 60), (ix - 30, iy - 8)], "#6d28d9", 2.5)
text(ix - 160, iy - 92, "γ", 18, "#6d28d9", w=12)
ell(ix, iy, 26, "#fecaca", "#b91c1c", 1.5)
text(ix - 8, iy - 12, "+", 20, "#b91c1c", w=16)
ell(ix + 105, iy - 55, 8, ELEKTRON, "#1e40af", 1)
pfeil([(ix + 28, iy - 14), (ix + 92, iy - 48)], "#1e40af", 1.5, style="dashed")
text(ix - 22, iy + 34, "Ion", 15, "#b91c1c", w=30)
text(ix + 90, iy - 85, "e⁻", 15, "#1e40af", w=20)

# LF5 Spaltung (unten Mitte)
X5, Y5 = 0, 260
block(4, X5 - 540, Y5 + 120, [
    ("Kernspaltung", "Neutron trifft U-235: 2 Bruchstücke, Energie, 2–3 Neutronen"),
    ("Kettenreaktion", "genau 1 wirksames Neutron: kontrolliert; mehr: Lawine"),
    ("Reaktor", "Brennstäbe, Steuerstäbe, Moderator, Kühlmittel"),
    ("Kernfusion", "leichte Kerne verschmelzen; Energiequelle der Sonne"),
])
sx, sy = X5 + 250, Y5 + 300
ell(sx - 120, sy, 7, NEUTRON, "#475569", 1)
pfeil([(sx - 110, sy), (sx - 40, sy)], "#475569", 1.5)
ell(sx, sy, 34, "#86efac", "#047857", 1.5)
text(sx - 28, sy - 10, "U-235", 14, "#065f46", w=56)
for dy, nm in ((-80, "Ba"), (80, "Kr")):
    pfeil([(sx + 30, sy + dy / 4), (sx + 105, sy + dy)], "#047857", 1.5)
    ell(sx + 125, sy + dy, 20, "#bbf7d0", "#047857", 1.2)
    text(sx + 112, sy + dy - 9, nm, 14, "#065f46", w=26)
for k in range(3):
    yy = sy - 22 + k * 22
    pfeil([(sx + 36, sy + (k - 1) * 8), (sx + 115, yy)], "#94a3b8", 1)
    ell(sx + 122, yy, 6, NEUTRON, "#475569", 1)
text(sx + 150, sy - 12, "+ Energie", 15, "#b45309", w=80)

# LF6 Abwägen (unten rechts)
X6, Y6 = 1250, 260
block(5, X6 - 540, Y6 + 120, [
    ("Radioaktiver Abfall", "Abklingbecken, Zwischenlager; Endlager wird noch gesucht"),
    ("eine Million Jahre sicher", "Suche nach einem Endlager in Deutschland"),
    ("Argumente abwägen", "Fakt oder Meinung? Größenordnungen nennen"),
    ("Altersbestimmung mit C-14", "fester Zerfall als Uhr: Holz, Knochen, Mumien"),
])
wx, wy = X6 + 340, Y6 + 300
linie([(wx - 90, wy - 60), (wx + 90, wy - 60)], "#475569", 2.5)
linie([(wx, wy - 75), (wx, wy + 55)], "#475569", 2.5)
linie([(wx - 40, wy + 55), (wx + 40, wy + 55)], "#475569", 2.5)
rect(wx - 115, wy - 60, 50, 32, "#a7f3d0", "#047857", 1.2)
rect(wx + 65, wy - 60, 50, 32, "#fee2e2", "#dc2626", 1.2)
text(wx - 116, wy - 22, "Nutzen", 14, "#047857", w=52)
text(wx + 63, wy - 22, "Risiko", 14, "#dc2626", w=52)

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": E,
       "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
open(sys.argv[1], "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1))
print(len(E), "Elemente")
