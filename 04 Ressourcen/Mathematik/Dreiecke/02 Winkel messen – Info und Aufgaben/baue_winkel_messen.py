"""Winkel messen Mathe 7c (Klassenlehrerstunde 09.11.2026): Info-Blatt, Aufgabenblatt, Lösung als dasselbe Blatt.

Grundlage: Info_Winkel zeichnen.docx, Station 4 (zeichnen), Station 5 (berechnen), AB Winkel messen.
Ganze Seite als SVG in Millimetern, Winkel stimmen bei Druck in Originalgröße (100 %).
Aufruf: python3 baue_winkel_messen.py
"""
import math
import subprocess
import sys
import tempfile
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent / "01 Diagnose – Test, Auswertung, Förderblätter"))
from baue_diagnose_dreiecke import P, txt, linie, bogen, karo, feld, stufe, rechter_winkel_zeichen, TEAL, PINK, GRAU, LOGO, CHROME  # noqa: E402

NAME = "Mathe 7c – Winkel messen"
OBEN, UNTEN = 12, 287
GEO = "#b7dcdc"
SCHWARZ = "#111"


def bar(y, titel, zusatz=""):
    s = f'<rect x="12" y="{y}" width="186" height="8" fill="{GRAU}"/>' + txt(14, y + 5.8, titel, 4.8, "bold", TEAL)
    if zusatz:
        s += txt(196, y + 5.6, zusatz, 3.5, "normal", "#333", "end")
    return s


def nr(x, y, n, farbe=TEAL):
    return f'<circle cx="{x}" cy="{y}" r="2.3" fill="{farbe}"/>' + txt(x, y + 1.15, n, 3.2, "bold", "#fff", "middle")


def schritt(x, y, n, zeilen, size=3.7):
    s = nr(x + 2.3, y - 1.2, n)
    for i, z in enumerate(zeilen):
        s += txt(x + 6.5, y + i * (size + 1.1), z, size)
    return s


def aufgabe(y, n, st, text):
    s = f'<rect x="12" y="{y}" width="186" height="8" fill="{GRAU}"/>'
    s += txt(14, y + 5.8, f"Nr. {n}", 4.8, "bold", TEAL) + stufe(30.5, y + 4, st) + txt(35, y + 5.6, text, 4.0)
    return s


def kreis(cx, cy, r, farbe=SCHWARZ, w=0.35):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="none" stroke="{farbe}" stroke-width="{w}"/>'


def scheitel(x, y, name="S", dx=-1.5, dy=4.6):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.7" fill="#111"/>' + txt(x + dx, y + dy, name, 3.8, "bold", anchor="middle")


def seitentext(x, y, s, size, drehung, fill):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" fill="{fill}" '
            f'text-anchor="middle" transform="rotate({drehung} {x:.2f} {y:.2f})">{s}</text>')


def geodreieck(sx, sy, h):
    """Geodreieck mit langer Kante auf dem Schenkel, 0 auf dem Scheitel. Außen zählt von rechts nach links."""
    s = f'<path d="M{sx-h} {sy} L{sx+h} {sy} L{sx} {sy-h} Z" fill="#dff1f1" fill-opacity="0.75" stroke="{TEAL}" stroke-width="0.4"/>'
    s += linie(sx, sy, sx, sy - h + 16, GEO, 0.3)
    for i in range(1, 6):
        for v in (-1, 1):
            s += linie(sx + v * i * 9, sy, sx + v * i * 9, sy - 2.2, TEAL, 0.25) + (seitentext(sx + v * i * 9, sy - 3.1, str(i), 2.2, 0, TEAL) if i in (1, 2, 5) else "")
    s += linie(sx, sy, sx, sy - 3, TEAL, 0.4) + seitentext(sx, sy - 3.9, "0", 2.4, 0, TEAL)
    for a in range(5, 180, 5):
        lang = a % 10 == 0
        s += linie(*P(sx, sy, 37.6 if lang else 38.6, a), *P(sx, sy, 40, a), TEAL, 0.25)
        if lang:
            xa, ya = P(sx, sy, 34, a)
            xi, yi = P(sx, sy, 28.4, a)
            s += seitentext(xa, ya + 0.8, str(a), 2.4, 90 - a, "#0a5356") + seitentext(xi, yi + 0.8, str(180 - a), 2.4, 90 - a, "#6b8b8b")
    return s


def geo_klein(sx, sy, h=16):
    s = f'<path d="M{sx-h} {sy} L{sx+h} {sy} L{sx} {sy-h} Z" fill="#dff1f1" fill-opacity="0.75" stroke="{TEAL}" stroke-width="0.35"/>'
    s += bogen(sx, sy, h * 0.68, 0, 180, TEAL, 0.25)
    return s + linie(sx, sy, sx, sy - 2, TEAL, 0.4)


# ------------------------------------------------------------------ Info-Blatt

def art(x, y, name, bereich, a1, a2):
    cx, cy = x + 15.5, y + 17
    if name == "gestreckt":
        cx, cy = x + 15.5, y + 14
    if name == "überstumpf":
        cy = y + 11
    if name == "Vollwinkel":
        cy = y + 10
    s = linie(cx, cy, *P(cx, cy, 12, a1), "#111", 0.45)
    if name != "Vollwinkel":
        s += linie(cx, cy, *P(cx, cy, 12, a2), "#111", 0.45)
    if name == "rechter Winkel":
        s += rechter_winkel_zeichen(cx, cy, a1, TEAL)
    elif name == "Vollwinkel":
        s += kreis(cx, cy, 5, TEAL, 0.4)
    else:
        s += bogen(cx, cy, 5, a1, a2, TEAL, 0.4)
    s += txt(x + 15.5, y + 24.5, name, 3.5, "bold", anchor="middle") + txt(x + 15.5, y + 29, bereich, 3.2, "normal", "#333", "middle")
    return s


def geo_gedreht(cx, cy, h=17):
    """Geodreieck gedreht: lange Kante zeigt auf 60°, 0 auf S. Unten abgeschnitten wie in der Vorlage."""
    a, b, c = P(cx, cy, h, 60), P(cx, cy, h, 240), P(cx, cy, h, -30)
    i = f"c{cx:.0f}{cy:.0f}".replace(".", "")
    s = f'<clipPath id="{i}"><rect x="{cx - 20}" y="{cy - 22}" width="40" height="25.5"/></clipPath><g clip-path="url(#{i})">'
    s += f'<path d="M{a[0]:.2f} {a[1]:.2f} L{b[0]:.2f} {b[1]:.2f} L{c[0]:.2f} {c[1]:.2f} Z" fill="#dff1f1" fill-opacity="0.75" stroke="{TEAL}" stroke-width="0.35"/>'
    s += bogen(cx, cy, h * 0.68, -120, 60, TEAL, 0.25) + linie(cx, cy, *P(cx, cy, 2, -30), TEAL, 0.4) + "</g>"
    return s


def streifen(y, titel, dreh):
    """Eine Bilderreihe mit 5 Schritten, Beispiel 60°."""
    text = [("Schenkel", "zeichnen"), ("Scheitel S", "markieren")]
    text += ([("0 auf S, drehen", "bis Schenkel auf 60°"), ("An der langen", "Kante zeichnen")] if dreh
             else [("0 auf S legen,", "bei 60° Punkt setzen"), ("Punkt mit S", "verbinden")])
    text += [("Bogen und 60°", "eintragen")]
    s = txt(14, y + 13, titel, 3.8, "bold", TEAL)
    for i, (a, b) in enumerate(text):
        x0 = 12 + 37.2 * i
        cx, cy = x0 + 18, y + 31
        if i in (2, 3):
            s += geo_gedreht(cx, cy) if dreh else (geo_klein(cx, cy, 17) if i == 2 else "")
        s += linie(cx if i else cx - 1, cy, x0 + 36, cy, "#111", 0.5)
        if i:
            s += scheitel(cx, cy, "S", -4.8 if dreh and i in (2, 3) else -3, 1.6 if dreh and i in (2, 3) else 3)
        if i == 2 and dreh:
            s += kreis(cx + 11.56, cy, 1.7, PINK, 0.5) + txt(cx + 14.2, cy - 1.8, "60", 3.0, "bold", PINK)
        if i == 2 and not dreh:
            px, py = P(cx, cy, 11, 60)
            s += f'<circle cx="{px:.2f}" cy="{py:.2f}" r="0.8" fill="{PINK}"/>'
        if i >= 3:
            s += linie(cx, cy, *P(cx, cy, 22, 60), PINK if i == 3 else "#111", 0.5)
        if i == 4:
            s += bogen(cx, cy, 7, 0, 60, PINK, 0.5) + txt(*P(cx, cy, 11, 30), "60°", 3.1, "bold", PINK, "middle")
        s += nr(x0 + 2.8, y + 37.5, str(i + 1)) + txt(x0 + 6.5, y + 38.5, a, 3.3) + txt(x0 + 6.5, y + 42.6, b, 3.3)
    return s


def plakette(px, py, z, farbe, r, breit, drehung):
    return (f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r}" fill="#fff" stroke="{farbe}" stroke-width="{breit}"/>'
            + seitentext(px, py + 0.85, z, 2.5, drehung, farbe))


def messen_kante_erster(y):
    """Markier-Methode: lange Kante auf dem ersten Schenkel, ablesen am zweiten."""
    sx, sy = 72, y + 68
    s = geodreieck(sx, sy, 58) + linie(sx, sy, sx + 62, sy, "#111", 0.55)
    s += linie(sx, sy, *P(sx, sy, 62, 50), "#111", 0.55) + bogen(sx, sy, 11, 0, 50, PINK, 0.5)
    mx, my = P(sx, sy, 15, 25)
    s += txt(mx, my + 1.4, "α", 4.2, "bold", PINK, "middle", "italic")
    s += plakette(*P(sx, sy, 34, 50), "50", PINK, 3.2, 0.55, 40) + plakette(*P(sx, sy, 28.4, 50), "130", "#777", 2.9, 0.35, 40)
    s += scheitel(sx, sy) + txt(14, y + 13, "Markier-Methode", 3.8, "bold", TEAL)
    x, yy = 138, y + 20
    for n, z, d in (("1", ["Art schätzen: Hier spitz."], 10), ("2", ["0 genau auf S legen.", "Lange Kante auf den", "ersten Schenkel."], 19),
                    ("3", ["Am zweiten Schenkel", "ablesen: 50 und 130.", "Spitz, also 50."], 19)):
        s += schritt(x, yy, n, z)
        yy += d
    return s + nr(x + 2.3, yy - 1.2, "4") + txt(x + 6.5, yy, "α = 50°", 4.4, "bold", PINK)


def messen_gedreht(y):
    """Dreh-Methode: lange Kante auf dem zweiten Schenkel, ablesen am ersten."""
    sx, sy = 60, y + 53
    drehung = 130               # Bildschirm im Uhrzeigersinn: lange Kante links zeigt dann auf 50°
    assert (180 - drehung) == 50 and (130 - drehung) % 360 == 0   # Stelle außen 130, innen 50 liegt auf dem ersten Schenkel
    s = (f'<clipPath id="messdreh"><rect x="12" y="{y}" width="122" height="{53 + 20}"/></clipPath><g clip-path="url(#messdreh)">'
         f'<g transform="rotate({drehung} {sx} {sy})">' + geodreieck(sx, sy, 58) + '</g></g>')
    s += linie(sx, sy, sx + 68, sy, "#111", 0.55) + linie(sx, sy, *P(sx, sy, 66, 50), "#111", 0.55) + bogen(sx, sy, 11, 0, 50, PINK, 0.5)
    mx, my = P(sx, sy, 15, 25)
    s += txt(mx, my + 1.4, "α", 4.2, "bold", PINK, "middle", "italic")
    s += plakette(sx + 28.4, sy, "50", PINK, 3.2, 0.55, 0) + plakette(sx + 34.6, sy, "130", "#777", 2.9, 0.35, 0)
    s += scheitel(sx, sy, "S", -5, 1.6) + txt(14, y + 8, "Dreh-Methode", 3.8, "bold", TEAL)
    x, yy = 138, y + 12
    for n, z, d in (("1", ["Art schätzen: Hier spitz."], 10), ("2", ["0 genau auf S legen.", "Drehen, bis die lange", "Kante auf dem zweiten", "Schenkel liegt."], 24),
                    ("3", ["Am ersten Schenkel", "ablesen: 50 und 130.", "Spitz, also 50."], 19)):
        s += schritt(x, yy, n, z)
        yy += d
    return s + nr(x + 2.3, yy - 1.2, "4") + txt(x + 6.5, yy, "α = 50°", 4.4, "bold", PINK)


def ueberstumpf(y, messen):
    """Beispiel 240°, zwei Wege: über den Rest und über 180°."""
    s = bar(y, "Überstumpfe Winkel " + ("messen" if messen else "zeichnen"), "Beispiel: 240°")
    farbe = "#111" if messen else PINK
    cy = y + 25
    cx = 30
    s += linie(cx, cy, cx + 22, cy, "#111", 0.5) + linie(cx, cy, *P(cx, cy, 20, 240), farbe, 0.55) + bogen(cx, cy, 6, 0, 240, PINK, 0.5)
    s += bogen(cx, cy, 11, 240, 360, "#555", 0.3) + txt(*P(cx, cy, 15.5, 300), "120°", 3.1, "bold", "#555", "middle")
    s += txt(*P(cx, cy, 9.4, 120), "240°", 3.0, "bold", PINK, "middle") + scheitel(cx, cy, "S", 2.6, -1.4)
    x = 56
    s += txt(x, y + 13, "Mit dem Rest", 3.8, "bold")
    if messen:
        s += schritt(x, y + 19, "1", ["Rest messen: 120°"]) + schritt(x, y + 26, "2", ["360° − 120° = 240°"])
    else:
        s += schritt(x, y + 19, "1", ["360° − 240° = 120°"]) + schritt(x, y + 26, "2", ["120° im Uhrzeigersinn"]) + schritt(x, y + 33, "3", ["Bogen außen herum"])
    cx = 122
    s += linie(cx, cy, cx + 22, cy, "#111", 0.5) + linie(cx, cy, cx - 20, cy, "#555", 0.3, 'stroke-dasharray="1.5 1"')
    s += linie(cx, cy, *P(cx, cy, 20, 240), farbe, 0.55) + bogen(cx, cy, 11, 180, 240, "#555", 0.3)
    s += bogen(cx, cy, 6, 0, 240, PINK, 0.5) + txt(*P(cx, cy, 15, 212), "60°", 3.1, "bold", "#555", "middle") + scheitel(cx, cy, "S", 2.6, -1.4)
    x = 149
    s += txt(x, y + 13, "Mit 180°", 3.8, "bold")
    if messen:
        s += schritt(x, y + 19, "1", ["Nach links verlängern"]) + schritt(x, y + 26, "2", ["Stück messen: 60°"]) + schritt(x, y + 33, "3", ["180° + 60° = 240°"])
    else:
        s += schritt(x, y + 19, "1", ["240° = 180° + 60°"]) + schritt(x, y + 26, "2", ["Nach links verlängern"]) + schritt(x, y + 33, "3", ["60° dazu zeichnen"])
    return s


# Buchstaben als ein Schreibzug im Feld 10 x 15 mm, Grundlinie bei y = 10 (zweite Karolinie)
GRIECH = (
    ("Alpha", (8.3, 4.2), "M8.3 4.2 C7.2 7.5 5.6 10 3.8 10 C2 10 1.3 8.4 1.3 7 C1.3 5.4 2.4 4 3.9 4 C5.6 4 6.6 6.6 7.2 8.6 C7.5 9.6 8 10 8.8 10"),
    ("Beta", (2.5, 14), "M2.5 14 L2.5 3.5 C2.5 1.6 3.8 0.8 5.2 0.8 C7 0.8 7.8 2 7.8 3.2 C7.8 4.6 6.6 5.4 4.8 5.4 C7 5.4 8.6 6.4 8.6 8 C8.6 9.6 7 10.4 5.2 10.4 C4 10.4 3 9.8 2.5 9"),
    ("Gamma", (1.3, 4.3), "M1.3 4.3 C2.6 3.8 3.6 5 4.2 7 C4.8 9 5.1 11 5 12.6 C4.9 13.8 4.3 14.2 3.9 13.7 C3.4 13 4.2 10.5 5.2 8.5 C6 6.9 7 5.2 8.3 4"),
    ("Delta", (7.6, 1.6), "M7.6 1.6 C6.6 0.6 3.8 0.6 3.4 1.9 C3 3.2 7.8 4.6 7.8 7.2 C7.8 9 6.3 10.2 4.7 10.2 C3 10.2 1.6 8.9 1.6 7.3 C1.6 5.6 3.1 4.4 5 4.1"),
    ("Epsilon", (7.6, 4.7), "M7.6 4.7 C6.6 3.8 3 3.7 3 5.6 C3 6.6 4 7 5.8 7 C3.7 7 2.4 7.6 2.4 8.7 C2.4 10.4 6 10.6 7.8 9.4"),
)


def zug(x, y, d, farbe, breit, anteil=1.0):
    strich = f' pathLength="1" stroke-dasharray="{anteil} 1"' if anteil < 1 else ""
    return (f'<path transform="translate({x} {y})" d="{d}" fill="none" stroke="{farbe}" stroke-width="{breit}" '
            f'stroke-linecap="round" stroke-linejoin="round"{strich}/>')


def griechisch(y):
    s = bar(y, "Griechische Buchstaben für Winkel", "Nachspuren, dann mindestens 10-mal selbst schreiben")
    for i, (name, (sx, sy), d) in enumerate(GRIECH):
        yy = y + 12 + 20 * i
        s += zug(14, yy, d, "#111", 0.7) + txt(26, yy + 10, name, 4.8, "bold")
        s += karo(48, yy, 150, 15)
        for x, anteil in ((48, 1.0), (58, 0.5)):
            s += zug(x, yy, d, "#9a9a9a", 0.7, anteil)
            s += f'<circle cx="{x + sx}" cy="{yy + sy}" r="0.8" fill="{PINK}"/>'
    return s


def info():
    """Zwei Seiten: vorne messen, hinten zeichnen."""
    y = OBEN
    s = f'<rect x="12" y="{y}" width="186" height="11" fill="#d9d9d9"/>'
    s += txt(15, y + 7.6, "Mathematik 7c   Winkel messen und zeichnen: Info", 5.2, "bold")
    s += f'<image href="data:image/png;base64,{LOGO}" x="187" y="{y + 1}" width="9" height="9"/>'
    y += 14

    s += bar(y, "Winkelarten")
    for i, (n, b, a1, a2) in enumerate((("spitz", "unter 90°", 0, 45), ("rechter Winkel", "genau 90°", 0, 90), ("stumpf", "90° bis 180°", 0, 130),
                                        ("gestreckt", "genau 180°", 0, 180), ("überstumpf", "über 180°", 0, 240), ("Vollwinkel", "genau 360°", 0, 0))):
        s += art(12 + 31 * i, y + 9, n, b, a1, a2)
    y += 42

    s += bar(y, "Winkel messen", "Schenkel zu kurz? Verlängern.")
    s += messen_kante_erster(y) + messen_gedreht(y + 77)
    y += 153
    s += ueberstumpf(y, True)
    y += 42
    assert y <= UNTEN, y

    y = OBEN
    s2 = bar(y, "Winkel zeichnen", "immer gegen den Uhrzeigersinn")
    s2 += streifen(y, "Markier-Methode", False) + streifen(y + 37, "Dreh-Methode", True)
    y += 83
    s2 += ueberstumpf(y, False)
    y += 45
    s2 += griechisch(y)
    y += 12 + 20 * 5
    assert y <= UNTEN, y
    return [s, s2]


# ------------------------------------------------------------------ Bausteine Aufgaben

def wb(cx, cy, a1, g, leg, name, r=8):
    a2 = a1 + g
    s = linie(cx, cy, *P(cx, cy, leg, a1), "#111", 0.45) + linie(cx, cy, *P(cx, cy, leg, a2), "#111", 0.45)
    s += bogen(cx, cy, r, a1, a2, TEAL, 0.4)
    mx, my = P(cx, cy, r + 3.7, a1 + g / 2)
    return s + txt(mx, my + 1.4, name, 4.2, "normal", TEAL, "middle", "italic")


def einpassen(x, y, w, h, a1, g, leg):
    pts = [(0, 0)] + [P(0, 0, leg, a) for a in (a1, a1 + g)]
    if g > 180:
        pts += [(-11, -11), (11, 11)]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    assert x1 - x0 <= w and y1 - y0 <= h, (a1, g, x1 - x0, y1 - y0)
    return x + (w - (x1 - x0)) / 2 - x0, y + (h - (y1 - y0)) / 2 - y0


def art_von(g):
    return "spitz" if g < 90 else "recht" if g == 90 else "stumpf" if g < 180 else "gestreckt" if g == 180 else "überstumpf"


def messzeile(x, y, name, g, L):
    return (txt(x, y + 6, "Art", 3.6) + feld(x + 6.5, y, 22, 8.5, art_von(g) if L else "")
            + txt(x + 31, y + 6, f"{name} =", 4.2) + feld(x + 39, y, 13, 8.5, str(g) if L else "") + txt(x + 53, y + 6, "°", 4.2))


def nr1(y, L):
    s = aufgabe(y, 1, 0, "Art schätzen, dann messen. Zu kurz? Schenkel verlängern.")
    for i, (g, rot, n) in enumerate(((38, 0, "α"), (116, 0, "β"), (73, 0, "γ"))):
        x0 = 12 + 62 * i
        cx, cy = einpassen(x0 + 2, y + 10, 58, 39, rot, g, 40)
        s += wb(cx, cy, rot, g, 40, n, 8) + messzeile(x0 + 3, y + 51, n, g, L)
    return s, 61


def nr2(y, L):
    s = aufgabe(y, 2, 1, "Art schätzen, dann messen. Die Schenkel liegen schräg.")
    for i, (g, rot, n) in enumerate(((62, 105, "α"), (147, -12, "β"))):
        x0 = 12 + 93 * i
        cx, cy = einpassen(x0 + 3, y + 10, 87, 43, rot, g, 44)
        s += wb(cx, cy, rot, g, 44, n, 9) + messzeile(x0 + 18, y + 54, n, g, L)
    return s, 64


def nr3(y, L):
    s = aufgabe(y, 3, 2, "Miss den Rest und rechne 360° minus Rest.")
    for i, (g, rot, n) in enumerate(((215, 20, "α"), (290, -35, "β"))):
        x0 = 12 + 93 * i
        cx, cy = einpassen(x0 + 2, y + 10, 42, 37, rot, g, 26)
        s += wb(cx, cy, rot, g, 26, n, 6)
        x = x0 + 47
        s += txt(x, y + 22, "Rest =", 4.0) + feld(x + 13, y + 16, 13, 8.5, str(360 - g) if L else "") + txt(x + 27, y + 22, "°", 4.0)
        s += txt(x + 2.6, y + 36, f"{n} =", 4.2) + feld(x + 13, y + 30, 13, 8.5, str(g) if L else "") + txt(x + 27, y + 36, "°", 4.0)
    return s, 48


def panel(x0, y, g, sx, sy, ex, ey, kz, name, L, hoch, sol_len):
    """Karofeld 60 mm breit; S (sx, sy) und Schenkelende (ex, ey) liegen auf Karolinien."""
    for v in (sx, sy, ex, ey):
        assert v % 5 == 0, v
    s = karo(x0, y, 60, hoch) + txt(x0 + 2, y + 5.2, f"{kz})  {name} = {g}°", 3.8, "bold")
    px, py, qx, qy = x0 + sx, y + sy, x0 + ex, y + ey
    a1 = math.degrees(math.atan2(py - qy, qx - px))
    s += linie(px, py, qx, qy, "#111", 0.5) + scheitel(px, py, "S", 3 if 180 < g < 300 else -3, 4.6 if 180 < g < 300 else 3.4 if g != 180 else 4.2)
    if L:
        a2 = a1 + g
        u, v = P(px, py, sol_len, a2)
        assert x0 < u < x0 + 60 and y < v < y + hoch, (g, u, v)
        s += linie(px, py, u, v, PINK, 0.6) + bogen(px, py, 6.5, a1, a2, PINK, 0.45)
        w = a1 + g / 2
        s += txt(*P(px, py, 22 if g < 30 else 11 if g < 200 else 9.7, w), f"{g}°", 3.1, "bold", PINK, "middle")
    return s


ZX = (12, 75, 138)


def nr4(y, L):
    s = aufgabe(y, 4, 0, "Zeichne die Winkel gegen den Uhrzeigersinn. Beschrifte sie.")
    p = ((70, 20, 40, 55, 40, "a", 33), (125, 30, 40, 55, 40, "b", 33), (180, 30, 25, 55, 25, "c", 25))
    for x0, (g, sx, sy, ex, ey, kz, ln) in zip(ZX, p):
        s += panel(x0, y + 10, g, sx, sy, ex, ey, kz, "α", L, 45, ln)
    return s, 55


def nr5(y, L):
    s = aufgabe(y, 5, 1, "Zeichne die Winkel. Der Schenkel liegt schräg, das Geodreieck auch.")
    p = ((85, 15, 35, 55, 45, "a", 28), (20, 10, 40, 50, 25, "b", 38), (140, 30, 35, 55, 45, "c", 28))
    for x0, (g, sx, sy, ex, ey, kz, ln) in zip(ZX, p):
        s += panel(x0, y + 10, g, sx, sy, ex, ey, kz, "β", L, 45, ln)
    return s, 55


def nr6(y, L):
    s = aufgabe(y, 6, 2, "Zeichne die überstumpfen Winkel. Tipp: mit dem Rest oder mit 180°.")
    for x0, g, kz in zip(ZX, (200, 250, 310), "abc"):
        s += panel(x0, y + 10, g, 30, 20, 55, 20, kz, "γ", L, 40, 18)
    return s, 50


def rechenfeld(x, y, w, inhalt, L):
    s = karo(x, y, w, 10)
    if L:
        s += txt(x + w / 2, y + 4.1, inhalt, 3.3, "bold", PINK, "middle")
    return s


def nr7(y, L):
    s = aufgabe(y, 7, 0, "Berechne mit dem gestreckten Winkel. Notiere die Rechnung.")
    for i, (g, n) in enumerate(((50, "α"), (68, "β"), (133, "γ"), (90, "δ"))):
        x0 = 12 + 46.5 * i
        cx, cy = x0 + 23.25, y + 32
        s += linie(cx - 21, cy, cx + 21, cy, "#111", 0.45) + linie(cx, cy, *P(cx, cy, 20, g), "#111", 0.45)
        if g == 90:
            s += rechter_winkel_zeichen(cx, cy, 0, TEAL, 5) + txt(*P(cx, cy, 11, 28), "90°", 3.2, "bold", TEAL, "middle")
        else:
            s += bogen(cx, cy, 7.5, 0, g, TEAL, 0.4) + txt(*P(cx, cy, 11.6 if g < 100 else 11.8, g / 2 if g < 100 else g / 2 - 12), f"{g}°", 3.2, "bold", TEAL, "middle")
        s += bogen(cx, cy, 8.5 if g != 133 else 5.5, g, 180, "#111", 0.35)
        s += txt(*P(cx, cy, 13 if g != 133 else 10.5, (g + 180) / 2), n, 4.2, "normal", "#111", "middle", "italic")
        s += rechenfeld(x0 + 0.75, y + 34, 45, f"{n} = 180° − {g}° = {180 - g}°", L)
    return s, 44


def nr8(y, L):
    s = aufgabe(y, 8, 1, "Berechne mit dem Vollwinkel. Notiere die Rechnung.")
    for i, (a1, g) in enumerate(((0, 52), (0, 125), (195, 157))):
        x0 = 12 + 62 * i
        cx, cy = x0 + 31, y + 26
        s += linie(cx, cy, *P(cx, cy, 21, a1), "#111", 0.45) + linie(cx, cy, *P(cx, cy, 21, a1 + g), "#111", 0.45) + kreis(cx, cy, 13, TEAL, 0.4)
        s += txt(*P(cx, cy, 8.8, a1 + g / 2), f"{g}°", 3.4, "bold", TEAL, "middle")
        mx, my = P(cx, cy, 7.5, a1 + g + (360 - g) / 2)
        s += txt(mx, my + 1.4, "β", 4.4, "normal", "#111", "middle", "italic")
        s += rechenfeld(x0 + 6, y + 40.5, 50, f"β = 360° − {g}° = {360 - g}°", L)
    return s, 50.5


def nr9(y, L):
    s = aufgabe(y, 9, 2, "Berechne α, β, γ und δ mit dem Vollwinkel.")
    wa, wb_i, wc, vu = 34, 118, 17, 169        # innen bei A, B, C; unten bei V
    assert wa + wb_i + wc + (360 - vu) == 360
    a = (0, 0)
    v = (58, 0)
    r_vc = -(180 - vu)
    c = (v[0] + 52 * math.cos(math.radians(r_vc)), 52 * math.sin(math.radians(r_vc)))
    r_cv = r_vc + 180
    r_cb = r_cv - wc
    ca, sa = math.cos(math.radians(wa)), math.sin(math.radians(wa))
    cb, sb = math.cos(math.radians(r_cb)), math.sin(math.radians(r_cb))
    det = ca * sb - sa * cb
    t = (c[0] * sb - c[1] * cb) / det
    b = (t * ca, t * sa)
    ox, oy = 24, y + 44
    X = lambda p: (ox + p[0], oy - p[1])  # noqa: E731
    pts = [X(a), X(b), X(c), X(v)]
    d = "M" + " L".join(f"{p[0]:.2f} {p[1]:.2f}" for p in pts) + " Z"
    s += f'<path d="{d}" fill="#eef7f7" stroke="#111" stroke-width="0.45"/>'

    def richt(p, q):
        return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))

    rba, rbc = richt(b, a), richt(b, c)
    assert abs(((rbc - rba) % 360) - wb_i) < 0.01, (rba, rbc)
    for p, a1, g, r, rl, grad, rg, name in ((a, 0, wa, 16, 12.2, wa, 7.5, "α"), (b, rba, wb_i, 8, 11.5, wb_i, 7.5, "δ"), (c, r_cb, wc, 25, 21, wc, 7.5, "γ"), (v, 180, vu, 9, 12.8, vu, 7.5, "β")):
        cx, cy = X(p)
        s += bogen(cx, cy, r, a1, a1 + g, TEAL, 0.4) + txt(*P(cx, cy, rl, a1 + g / 2), f"{grad}°", 3.2, "bold", TEAL, "middle")
        s += bogen(cx, cy, rg, a1 + g, a1 + 360, "#111", 0.35)
        mx, my = P(cx, cy, 4, a1 + g + (360 - g) / 2)
        s += txt(mx, my + 1.4, name, 4.2, "normal", "#111", "middle", "italic")
    for i, (n, g) in enumerate((("α", wa), ("β", vu), ("γ", wc), ("δ", wb_i))):
        s += rechenfeld(146, y + 11 + 11.5 * i, 50, f"{n} = 360° − {g}° = {360 - g}°", L)
    for ax, ay in pts:
        assert 12 < ax < 142 and y + 8 < ay < y + 62, (ax, ay)
    return s, 58


def kopf(L):
    y = OBEN
    s = f'<rect x="12" y="{y}" width="186" height="11" fill="#d9d9d9"/>'
    s += txt(15, y + 7.6, "Mathematik 7c   Winkel messen, zeichnen, berechnen", 5.2, "bold")
    s += f'<image href="data:image/png;base64,{LOGO}" x="187" y="{y + 1}" width="9" height="9"/>'
    y += 16
    if L:
        s += txt(14, y + 1, "Lösung", 4.4, "bold", PINK)
    else:
        s += txt(14, y + 1, "Name: ______________________", 3.8)
    x = 118
    for st, t, d in ((0, "leicht", 20), (1, "mittel", 20), (2, "schwer", 0)):
        s += stufe(x, y, st) + txt(x + 3.2, y + 1.3, t, 3.5)
        x += d
    return s, OBEN + 21


GAP = 3


def blatt(L):
    k, y = kopf(L)
    s1 = k
    for f in (nr1, nr2, nr3, nr4):
        t, h = f(y, L)
        s1 += t
        y += h + GAP
    assert y - GAP <= UNTEN, y
    y = OBEN
    s2 = ""
    for f in (nr5, nr6, nr7, nr8, nr9):
        t, h = f(y, L)
        s2 += t
        y += h + GAP
    assert y - GAP <= UNTEN, y
    return [s1, s2]


# ------------------------------------------------------------------ PDF

def svg(innen):
    return f'<svg class="s" xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">{innen}</svg>'


def pdf(name, seiten):
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>' + name + '</title>'
            '<style>@page{size:A4;margin:0}html,body{margin:0;padding:0}svg.s{display:block;page-break-after:always}'
            'svg.s:last-child{page-break-after:auto}</style></head><body>' + "".join(svg(x) for x in seiten) + '</body></html>')
    h = Path(tempfile.gettempdir()) / f"{name}.html"
    h.write_text(html, encoding="utf-8")
    ziel = HIER / f"{name}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={ziel}", h.as_uri()],
                   check=True, capture_output=True)
    return ziel


if __name__ == "__main__":
    print(pdf(f"{NAME} – Info", info()).name)
    print(pdf(f"{NAME} – Aufgaben", blatt(False)).name)
    print(pdf(f"{NAME} – Lösung", blatt(True)).name)
