"""Förderblätter Dreiecke 7c: Aufgabenpool (21 Aufgaben) + ein Blatt (A4 doppelseitig) pro Nummer.

Grundlage: Auswertung der Diagnose vom 04.11.2026 (Auswertung 7c/ergebnisse_dreiecke.json).
Zuteilung: Bereich unter 50 % → ○ und ◐, Bereich unter 100 % → ◐, Rest der zwei Seiten → ● und Vorgriff.
Aufruf: python3 baue_foerderblaetter.py   (Drucken in Originalgröße, 100 %)
"""
import itertools
import json
import math
import sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(HIER.parents[3] / ".scripts"))
from baue_diagnose_dreiecke import (P, txt, rechter_winkel_zeichen, linie, bogen, kreuz, karo, feld, stufe, winkelbild,  # noqa: E402
                                    pdf, TEAL, PINK, GRAU, LOGO)
from grundlagen_check_bericht import werte_nummer_aus, block_quote  # noqa: E402
from grundlagen_check_schluessel import TESTS, schluessel_fuer_nummer  # noqa: E402

AUSW = HIER / "Auswertung 7c"
NAME = "Mathe 7c – Förderblätter Dreiecke"
OBEN, UNTEN = 12, 287
ZAEHLER = itertools.count()
WG = 12   # Steigungswinkel der schrägen Geraden g in S2 und S3


def balken(y, kz, st, text):
    s = f'<rect x="12" y="{y}" width="186" height="8" fill="{GRAU}"/>'
    s += txt(14, y + 5.8, kz, 4.8, "bold", TEAL) + stufe(27, y + 4, st) + txt(31.5, y + 5.6, text, 4.0)
    return s


def zahl(x):
    return str(x).replace(".", ",")


# ------------------------------------------------------------------ Aufgaben
# Jede Aufgabe: (Kürzel, Bereich, Stufe, Höhe in mm, Funktion(y, L) -> svg)

def l1(y, L):
    s = balken(y, "L1", 0, "Miss die Länge der Strecken.")
    for i, (m, w) in enumerate(((57, 3), (82, -4), (39, 8))):
        yy = y + 16 + 10 * i
        x2, y2 = P(22, yy, m, w)
        s += linie(22, yy, x2, y2, "#111", 0.4) + kreuz(22, yy) + kreuz(x2, y2)
        s += txt(140, yy + 1.5, f"{'abc'[i]})", 4.2) + feld(148, yy - 4, 22, 8, zahl(m / 10) if L else "") + txt(172, yy + 1.5, "cm", 4.2)
    return s


def l2(y, L):
    s = balken(y, "L2", 1, "Zeichne ab dem Punkt eine Strecke mit der Länge  a) 4,8 cm  b) 9,3 cm.")
    s += karo(12, y + 10, 186, 25)
    for i, m in enumerate((48, 93)):
        yy = y + 17.5 + 10 * i
        s += kreuz(30, yy) + txt(20, yy + 1.5, "ab"[i] + ")", 4, "bold")
        if L:
            s += linie(30, yy, 30 + m, yy, PINK, 0.6) + kreuz(30 + m, yy, PINK)
    return s


def w1(y, L):
    s = balken(y, "W1", 0, "Welche Winkelart ist das? Schreibe sie in das Kästchen.")
    werte = [(35, "spitz"), (90, "recht"), (145, "stumpf"), (180, "gestreckt"),
             (260, "überstumpf"), (89, "spitz"), (91, "stumpf"), (300, "überstumpf")]
    for i, (g, art) in enumerate(werte):
        x, yy = 14 + 46.5 * (i % 4), y + 14 + 12 * (i // 4)
        s += txt(x + 11, yy + 5.6, f"{g}°", 4.4, "bold", anchor="end") + feld(x + 13, yy, 30, 8, art if L else "")
    return s


def w2(y, L):
    s = balken(y, "W2", 1, "Stumpf oder überstumpf? Schau genau, wo der Bogen ist.")
    for i, (g, rot, art) in enumerate(((120, 10, "stumpf"), (240, -30, "überstumpf"), (160, 5, "stumpf"), (300, -60, "überstumpf"))):
        cx = 12 + 46.5 * i + 23
        s += winkelbild(cx, y + 30, rot, rot + g, 15, "αβγδ"[i], 5)
        s += feld(cx - 16, y + 47, 32, 8, art if L else "")
    return s


def messen(y, L, kz, st, text, winkel):
    s = balken(y, kz, st, text)
    for i, (g, rot) in enumerate(winkel):
        cx = (30 + 93 * i) if g < 90 else [62, 150][i]
        cy = y + 52
        nm = "αβ"[i]
        if g > 180:
            cx, cy = 75, y + 40
        s += winkelbild(cx, cy, rot, rot + g, 50 if g < 90 else (45 if g <= 180 else 34), nm, 8)
        if g > 180:
            s += txt(130, y + 42, f"{nm} =", 4.4) + feld(141, y + 36.5, 22, 9, str(g) if L else "") + txt(165, y + 42, "°", 4.4)
        else:
            s += txt(30 + 93 * i, y + 66, f"{nm} =", 4.4) + feld(41 + 93 * i, y + 60.5, 22, 9, str(g) if L else "") + txt(65 + 93 * i, y + 66, "°", 4.4)
    return s


def m1(y, L):
    return messen(y, L, "M1", 0, "Miss die Winkel. Lege die 0 des Geodreiecks genau auf den Scheitel.", [(28, 12), (63, 4)])


def m2(y, L):
    return messen(y, L, "M2", 1, "Miss die Winkel. Größer als 90°? Dann die andere Skala nehmen.", [(107, 8), (152, 6)])


def m3(y, L):
    s = messen(y, L, "M3", 2, "Miss den überstumpfen Winkel. Tipp: Miss den Rest und rechne 360° minus Rest.", [(235, 20)])
    return s


def zeichnen(y, L, kz, st, text, winkel, hoch=50):
    s = balken(y, kz, st, text)
    for i, g in enumerate(winkel):
        x0 = 12 + 95 * i
        s += karo(x0, y + 10, 91, hoch)
        s += txt(x0 + 2, y + 16, f"{'ab'[i]})  {'αβ'[i]} = {g}°", 4.4, "bold")
        cx = x0 + (20 if g < 90 else 45)
        cy = y + 10 + hoch - 5 if g <= 180 else y + 10 + hoch / 2
        s += linie(cx, cy, cx + 42, cy, "#111", 0.45) + f'<circle cx="{cx}" cy="{cy}" r="0.7" fill="#111"/>' + txt(cx - 2, cy + 4.4, "S", 4, "bold")
        if L:
            s += linie(cx, cy, *P(cx, cy, 40 if g <= 180 else 28, g), PINK, 0.6) + bogen(cx, cy, 7, 0, g, PINK, 0.45)
            mx, my = P(cx, cy, 11.5, g / 2)
            s += txt(mx, my + 1.4, f"{g}°", 3.6, "bold", PINK, "middle")
    return s


def z1(y, L):
    return zeichnen(y, L, "Z1", 0, "Zeichne die Winkel. Scheitel S und der erste Schenkel sind vorgegeben.", [40, 75])


def z2(y, L):
    return zeichnen(y, L, "Z2", 1, "Zeichne die Winkel. Achte auf die richtige Skala am Geodreieck.", [115, 160])


def z3(y, L):
    s = zeichnen(y, L, "Z3", 2, "Zeichne den überstumpfen Winkel. Tipp: 360° minus Winkel an die andere Seite.", [220], 50)
    s += txt(110, y + 25, "Rechne zuerst:", 4.0) + txt(110, y + 33, "360° − 220° =", 4.2) + feld(138, y + 27.5, 18, 8, "140" if L else "") + txt(158, y + 33, "°", 4.2)
    return s


def kreuzung(cx, cy, a, rot=8, lang=24):
    s = ""
    for g in (rot, rot + a):
        s += linie(*P(cx, cy, lang, g), *P(cx, cy, lang, g + 180), "#111", 0.4)
    for nm, a1, a2 in (("α", rot, rot + a), ("β", rot + a, rot + 180), ("γ", rot + 180, rot + 180 + a), ("δ", rot + 180 + a, rot + 360)):
        r = 7 if (a2 - a1) < 90 else 5.5
        s += bogen(cx, cy, r, a1, a2)
        mx, my = P(cx, cy, r + 4, (a1 + a2) / 2)
        s += txt(mx, my + 1.4, nm, 4.2, "normal", "#c0392b", "middle", "italic")
    return s


def n1(y, L):
    s = balken(y, "N1", 0, "Nebenwinkel ergänzen sich zu 180°. Berechne den Nebenwinkel β.")
    cx, cy = 40, y + 32
    s += linie(16, cy, 66, cy, "#111", 0.4) + linie(cx, cy, *P(cx, cy, 24, 50), "#111", 0.4)
    s += bogen(cx, cy, 7, 0, 50) + bogen(cx, cy, 5.5, 50, 180)
    s += txt(*P(cx, cy, 11, 25), "α", 4.2, "normal", "#c0392b", "middle", "italic") + txt(*P(cx, cy, 9.5, 120), "β", 4.2, "normal", "#c0392b", "middle", "italic")
    for i, a in enumerate((40, 115, 90, 63)):
        x, yy = 82 + 58 * (i % 2), y + 14 + 12 * (i // 2)
        s += txt(x, yy + 5.6, f"α = {a}°   β =", 4.2) + feld(x + 30, yy, 16, 8, str(180 - a) if L else "") + txt(x + 47.5, yy + 5.6, "°", 4.2)
    return s


def n2(y, L):
    s = balken(y, "N2", 1, "Zwei Geraden schneiden sich, α = 55°. Berechne β, γ und δ.")
    s += kreuzung(50, y + 30, 55)
    s += txt(100, y + 16, "Scheitelwinkel sind gleich groß, Nebenwinkel ergeben 180°.", 3.3, "normal", "#555", style="italic")
    for i, (nm, w) in enumerate((("β", 125), ("γ", 55), ("δ", 125))):
        x = 100 + 33 * i
        s += txt(x, y + 32, f"{nm} =", 4.4) + feld(x + 8.5, y + 25.5, 16, 9, str(w) if L else "") + txt(x + 25.5, y + 32, "°", 4.4)
    return s


def n3(y, L):
    s = balken(y, "N3", 2, "Zwei Geraden schneiden sich, β = 128°. Berechne α, γ und δ.")
    s += kreuzung(50, y + 30, 52, rot=-5)
    for i, (nm, w) in enumerate((("α", 52), ("γ", 52), ("δ", 128))):
        x = 100 + 33 * i
        s += txt(x, y + 32, f"{nm} =", 4.4) + feld(x + 8.5, y + 25.5, 16, 9, str(w) if L else "") + txt(x + 25.5, y + 32, "°", 4.4)
    return s


def rechter_winkel(x, y, u, n, farbe=PINK):
    """u, n: SVG-Richtungen der beiden Schenkel. Zeichen: Viertelkreis mit Punkt."""
    tu, tn = math.degrees(math.atan2(-u[1], u[0])), math.degrees(math.atan2(-n[1], n[0]))
    start = tu if round((tn - tu) % 360) == 90 else tn
    return rechter_winkel_zeichen(x, y, start, farbe)


def s1(y, L):
    s = balken(y, "S1", 0, "Zeichne mit dem Geodreieck die Senkrechte zu g  a) durch A,  b) durch P.")
    fy = y + 10
    s += karo(12, fy, 186, 40)
    s += linie(17, fy + 30, 193, fy + 30, "#111", 0.45) + txt(188, fy + 27, "g", 4.4, "bold", style="italic")
    s += kreuz(60, fy + 30) + txt(56, fy + 36, "A", 4, "bold") + kreuz(140, fy + 10) + txt(143, fy + 9, "P", 4, "bold")
    if L:
        s += linie(60, fy + 2, 60, fy + 38, PINK, 0.6) + linie(140, fy + 2, 140, fy + 38, PINK, 0.6)
        s += rechter_winkel(60, fy + 30, (1, 0), (0, -1)) + rechter_winkel(140, fy + 30, (1, 0), (0, -1))
    return s


def schraeg(y, L, kz, st, text, loesung):
    s = balken(y, kz, st, text)
    fy = y + 10
    cid = f"c{kz}{next(ZAEHLER)}"
    s += karo(12, fy, 186, 50) + f'<clipPath id="{cid}"><rect x="12" y="{fy}" width="186" height="50"/></clipPath>'
    m = math.tan(math.radians(WG))   # g steigt schräg, nicht am Karo ausgerichtet
    gx = lambda x: fy + 46 - (x - 17) * m  # noqa: E731
    s += linie(17, gx(17), 193, gx(193), "#111", 0.45) + txt(188, gx(188) + 6, "g", 4.4, "bold", style="italic")
    s += loesung(fy, gx, cid)
    return s


def s2(y, L):
    def los(fy, gx, cid):
        ax, bx, by = 70, 142, fy + 5
        s = kreuz(ax, gx(ax)) + txt(ax - 2, gx(ax) + 6, "A", 4, "bold") + kreuz(bx, by) + txt(bx + 2.5, by - 1.5, "B", 4, "bold")
        if L:
            u, n = (math.cos(math.radians(WG)), -math.sin(math.radians(WG))), (-math.sin(math.radians(WG)), -math.cos(math.radians(WG)))
            s += f'<g clip-path="url(#{cid})">'
            s += linie(ax - 60 * n[0], gx(ax) - 60 * n[1], ax + 60 * n[0], gx(ax) + 60 * n[1], PINK, 0.6)
            s += linie(bx - 150 * u[0], by - 150 * u[1], bx + 80 * u[0], by + 80 * u[1], PINK, 0.6) + "</g>"
            s += rechter_winkel(ax, gx(ax), u, n) + txt(ax - 10, fy + 6, "h", 4.4, "bold", PINK, style="italic") + txt(108, by + 2.5, "k", 4.4, "bold", PINK, style="italic")
        return s
    return schraeg(y, L, "S2", 1, "Zeichne die Senkrechte h zu g durch A und die Parallele k zu g durch B.", los)


def s3(y, L):
    def los(fy, gx, cid):
        if not L:
            return ""
        u = (math.cos(math.radians(WG)), -math.sin(math.radians(WG)))
        n = (-math.sin(math.radians(WG)), -math.cos(math.radians(WG)))
        s = f'<g clip-path="url(#{cid})">'
        for d in (20, -20):
            x0, y0 = 105 + d * n[0], gx(105) + d * n[1]
            s += linie(x0 - 120 * u[0], y0 - 120 * u[1], x0 + 120 * u[0], y0 + 120 * u[1], PINK, 0.6)
        x0, y0 = 105, gx(105)
        s += linie(x0, y0, x0 + 20 * n[0], y0 + 20 * n[1], PINK, 0.35, 'stroke-dasharray="1.2 1"') + "</g>"
        s += txt(x0 + 10 * n[0] + 2, y0 + 10 * n[1], "2 cm", 3.4, "bold", PINK)
        return s
    return schraeg(y, L, "S3", 2, "Zeichne alle Parallelen zu g, die von g genau 2 cm Abstand haben.", los)


def kosy(ox, oy, nx, ny, farbe="#111"):
    s = linie(ox, oy, ox + 10 * nx + 6, oy, farbe, 0.45) + linie(ox, oy, ox, oy - 10 * ny - 6, farbe, 0.45)
    s += f'<path d="M{ox+10*nx+6} {oy} l-2.5 -1.2 v2.4 Z M{ox} {oy-10*ny-6} l-1.2 2.5 h2.4 Z" fill="{farbe}"/>'
    s += txt(ox + 10 * nx + 4, oy + 5, "x", 4, fill=farbe, style="italic") + txt(ox - 4.5, oy - 10 * ny - 4, "y", 4, fill=farbe, style="italic")
    for k in range(0, nx + 1):
        s += linie(ox + 10 * k, oy - 1, ox + 10 * k, oy + 1, farbe, 0.35) + txt(ox + 10 * k, oy + 4.6, str(k), 3.4, fill=farbe, anchor="middle")
    for k in range(1, ny + 1):
        s += linie(ox - 1, oy - 10 * k, ox + 1, oy - 10 * k, farbe, 0.35) + txt(ox - 2.5, oy - 10 * k + 1.2, str(k), 3.4, fill=farbe, anchor="end")
    return s


def punkte(ox, oy, pts, farbe, verbinden=True):
    xy = [(ox + 10 * px, oy - 10 * py) for _, px, py in pts]
    s = ""
    if verbinden:
        s += f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in xy)}" fill="none" stroke="{farbe}" stroke-width="0.5"/>'
    for (n, _, _), (a, b) in zip(pts, xy):
        s += kreuz(a, b, farbe) + txt(a + 1.8, b - 1.8, n, 4, "bold", farbe)
    return s


def k1(y, L):
    s = balken(y, "K1", 0, "Zeichne ein Koordinatensystem (1 Einheit = 1 cm) und trage die Punkte ein.")
    pts = [("A", 2, 1), ("B", 7, 3), ("C", 3, 6)]
    s += txt(16, y + 20, "A(2|1); B(7|3); C(3|6)", 4.6)
    s += txt(16, y + 30, "Erst nach rechts (x),", 4.0) + txt(16, y + 36, "dann nach oben (y).", 4.0)
    s += txt(16, y + 46, "Verbinde zum Dreieck ABC.", 4.0)
    s += karo(97, y + 10, 101, 80)
    if L:
        s += kosy(107, y + 80, 8, 6, PINK) + punkte(107, y + 80, pts, PINK)
    return s


def k2(y, L):
    s = balken(y, "K2", 1, "Lies die Koordinaten der Punkte ab.")
    ox, oy = 107, y + 75
    pts = [("P", 1, 4), ("Q", 6, 2), ("R", 4, 5), ("S", 7, 0)]
    s += karo(97, y + 10, 101, 75) + kosy(ox, oy, 8, 5) + punkte(ox, oy, pts, "#111", False)
    for i, (n, px, py) in enumerate(pts):
        yy = y + 16 + 13 * i
        s += txt(16, yy + 5.6, n, 4.4, "bold") + txt(22, yy + 5.6, "(", 5) + feld(25, yy, 12, 8, str(px) if L else "")
        s += txt(38.5, yy + 5.6, "|", 5) + feld(41, yy, 12, 8, str(py) if L else "") + txt(54, yy + 5.6, ")", 5)
    return s


def k3(y, L):
    s = balken(y, "K3", 2, "A(1|1), B(6|1) und C(6|4) sind Ecken eines Rechtecks ABCD. Zeichne es.")
    ox, oy = 107, y + 65
    s += karo(97, y + 10, 101, 65) + kosy(ox, oy, 8, 4)
    s += txt(16, y + 22, "Welche Koordinaten hat D?", 4.2) + txt(16, y + 33, "D(", 5) + feld(23, y + 27.5, 12, 8, "1" if L else "")
    s += txt(36.5, y + 33, "|", 5) + feld(39, y + 27.5, 12, 8, "4" if L else "") + txt(52, y + 33, ")", 5)
    if L:
        s += punkte(ox, oy, [("A", 1, 1), ("B", 6, 1), ("C", 6, 4), ("D", 1, 4)], PINK)
    return s


def d1(y, L):
    s = balken(y, "D1", 2, "Ausblick: Miss alle drei Winkel im Dreieck und addiere sie. Was fällt dir auf?")
    A, B = (35, y + 66), (103, y + 66)
    a, b = 48, 67
    # C als Schnitt der Schenkel
    ta, tb = math.tan(math.radians(a)), math.tan(math.radians(b))
    cx = (A[0] * ta + B[0] * tb) / (ta + tb)
    C = (cx, A[1] - (cx - A[0]) * ta)
    s += f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]:.2f},{C[1]:.2f}" fill="none" stroke="#111" stroke-width="0.45"/>'
    s += txt(A[0] - 5, A[1] + 2, "A", 4, "bold") + txt(B[0] + 2, B[1] + 2, "B", 4, "bold") + txt(C[0] - 1.5, C[1] - 2, "C", 4, "bold")
    s += bogen(*A, 7, 0, a) + bogen(*B, 7, 180 - b, 180) + bogen(C[0], C[1], 6, 180 + a, 360 - b)
    s += txt(*P(*A, 10.5, a / 2), "α", 4, "normal", "#c0392b", "middle", "italic") + txt(*P(*B, 10.5, 180 - b / 2), "β", 4, "normal", "#c0392b", "middle", "italic")
    s += txt(C[0], C[1] + 11, "γ", 4, "normal", "#c0392b", "middle", "italic")
    for i, (nm, w) in enumerate((("α", a), ("β", b), ("γ", 180 - a - b))):
        yy = y + 16 + 11 * i
        s += txt(140, yy + 5.6, f"{nm} =", 4.4) + feld(150, yy, 18, 8, str(w) if L else "") + txt(170, yy + 5.6, "°", 4.4)
    s += txt(140, y + 54.6, "Summe =", 4.4) + feld(160, y + 49, 18, 8, "180" if L else "") + txt(180, y + 54.6, "°", 4.4)
    return s


def d2(y, L):
    s = balken(y, "D2", 2, "Ausblick: Zeichne das Dreieck ABC mit c = AB = 7 cm, α = 40° und β = 65°.")
    s += karo(12, y + 10, 186, 55)
    A = (52, y + 55)
    s += kreuz(*A) + txt(A[0] - 6, A[1] + 1.5, "A", 4, "bold")
    if L:
        B = (A[0] + 70, A[1])
        ta, tb = math.tan(math.radians(40)), math.tan(math.radians(65))
        cx = (A[0] * ta + B[0] * tb) / (ta + tb)
        C = (cx, A[1] - (cx - A[0]) * ta)
        s += f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]:.2f},{C[1]:.2f}" fill="none" stroke="{PINK}" stroke-width="0.6"/>'
        s += txt(B[0] + 2, B[1] + 1.5, "B", 4, "bold", PINK) + txt(C[0] - 1.5, C[1] - 2, "C", 4, "bold", PINK)
        s += bogen(*A, 8, 0, 40, PINK) + bogen(*B, 8, 115, 180, PINK)
    return s


POOL = [
    ("L1", "L", 0, 44, l1), ("L2", "L", 1, 38, l2),
    ("W1", "W", 0, 40, w1), ("W2", "W", 1, 58, w2),
    ("M1", "M", 0, 74, m1), ("M2", "M", 1, 74, m2), ("M3", "M", 2, 78, m3),
    ("Z1", "Z", 0, 63, z1), ("Z2", "Z", 1, 63, z2), ("Z3", "Z", 2, 63, z3),
    ("N1", "N", 0, 42, n1), ("N2", "N", 1, 46, n2), ("N3", "N", 2, 46, n3),
    ("S1", "S", 0, 53, s1), ("S2", "S", 1, 63, s2), ("S3", "S", 2, 63, s3),
    ("K1", "K", 0, 93, k1), ("K2", "K", 1, 85, k2), ("K3", "K", 2, 75, k3),
    ("D1", "D", 2, 72, d1), ("D2", "D", 2, 65, d2),
]
AUFG = {a[0]: a for a in POOL}
BEREICH = {"L": "Längen messen und zeichnen", "W": "Winkelarten", "M": "Winkel messen", "Z": "Winkel zeichnen",
           "N": "Nebenwinkel und Scheitelwinkel", "S": "Senkrechte und Parallele", "K": "Koordinatensystem"}
WICHTIG = "MZSNKWL"     # Reihenfolge bei Gleichstand: was für Dreiecke am meisten zählt
REIHE = "LWMZNSKD"      # Reihenfolge auf dem Blatt
ABSTAND = 5


# ------------------------------------------------------------------ Auswertung und Zuteilung

def auswerten():
    d = json.loads((AUSW / "ergebnisse_dreiecke.json").read_text(encoding="utf-8"))
    test = TESTS["dreiecke"]
    out = {}
    for nr, antw in d["ergebnisse"].items():
        r = werte_nummer_aus(antw, schluessel_fuer_nummer(test, d, nr))
        quoten = {}
        for kurz, name in BEREICH.items():
            e = r[name]
            quoten[kurz] = sum(1 for _, s in e if s == "richtig") / len(e)   # leer zählt wie nicht gekonnt
        status = {}
        for name, e in r.items():
            for itemid, s in e:
                status[itemid] = s
        out[nr] = dict(version=d["versionen"][nr], quoten=quoten, status=status)
    return out


def verteilen(seiten_hoehen, auswahl):
    """Aufgaben in Blatt-Reihenfolge auf die Seiten legen. None, wenn es nicht passt."""
    seiten, frei, i = [[]], seiten_hoehen[0], 0
    for kz in sorted(auswahl, key=lambda k: (REIHE.index(AUFG[k][1]), AUFG[k][2])):
        h = AUFG[kz][3]
        if h > frei:
            i += 1
            if i >= len(seiten_hoehen):
                return None
            seiten.append([])
            frei = seiten_hoehen[i]
        seiten[-1].append(kz)
        frei -= h + ABSTAND
    return seiten


KOPF_H = 66


def zuteilen(quoten):
    sortiert = sorted(BEREICH, key=lambda b: (quoten[b], WICHTIG.index(b)))
    wunsch = []
    for b in sortiert:
        if quoten[b] < 0.5:
            wunsch += [f"{b}1", f"{b}2"]
        elif quoten[b] < 1:
            wunsch += [f"{b}2"]
    extra = [f"{b}3" for b in sorted(BEREICH, key=lambda b: -quoten[b]) if f"{b}3" in AUFG and quoten[b] >= 0.5] + ["D1", "D2"]
    platz = [UNTEN - OBEN - KOPF_H, UNTEN - OBEN]
    auswahl = []
    for kz in wunsch + extra:
        if verteilen(platz, auswahl + [kz]) is not None:
            auswahl.append(kz)
    return auswahl, verteilen(platz, auswahl)


# ------------------------------------------------------------------ Blätter

DIAG = [("1", "Längen messen", ["N1a", "N1b"]), ("2", "Strecke zeichnen", ["N2a"]), ("3", "Winkelarten", [f"N3{c}" for c in "abcde"]),
        ("4", "Winkel messen", ["N4a", "N4b"]), ("5", "Winkel zeichnen", ["N5a", "N5b"]), ("6", "Nebenwinkel", ["N6b", "N6c", "N6d"]),
        ("7", "Senkrechte, Parallele", ["N7a", "N7b"]), ("8", "Koordinatensystem", ["N8a", "N8b"])]


def symbol(x, y, art):
    if art == "richtig":
        return f'<path d="M{x-2.2} {y} l1.6 1.8 l3 -3.8" fill="none" stroke="#1d7a2e" stroke-width="0.7"/>'
    if art == "teils":
        return f'<circle cx="{x}" cy="{y}" r="2" fill="none" stroke="#c77800" stroke-width="0.6"/><path d="M{x} {y-2} A2 2 0 0 1 {x} {y+2} Z" fill="#c77800"/>'
    if art == "falsch":
        return linie(x - 1.8, y - 1.8, x + 1.8, y + 1.8, "#b3261e", 0.7) + linie(x - 1.8, y + 1.8, x + 1.8, y - 1.8, "#b3261e", 0.7)
    return linie(x - 1.8, y, x + 1.8, y, "#888", 0.6)


def kopf(nr, info, auswahl):
    s = f'<rect x="12" y="{OBEN}" width="186" height="11" fill="#d9d9d9"/>'
    s += txt(15, OBEN + 7.6, "Mathematik 7c   Förderblatt Dreiecke: Grundlagen", 5.2, "bold")
    s += txt(150, OBEN + 7.6, f"Nummer {nr}", 5.2, "bold", TEAL)
    s += f'<image href="data:image/png;base64,{LOGO}" x="184" y="{OBEN + 13}" width="14" height="14"/>'
    y = OBEN + 18
    s += txt(14, y, "Dein Ergebnis in der Diagnose vom 04.11.:", 4.0, "bold")
    s += symbol(118, y - 1.3, "richtig") + txt(121.5, y, "richtig", 3.2) + symbol(137, y - 1.3, "teils") + txt(140.5, y, "zum Teil", 3.2)
    s += symbol(157, y - 1.3, "falsch") + txt(160.5, y, "falsch", 3.2) + symbol(172, y - 1.3, "leer") + txt(175.5, y, "leer", 3.2)
    for i, (n, name, items) in enumerate(DIAG):
        x = 14 + 21 * i
        st = [info["status"].get(it, "offen") for it in items]
        art = "richtig" if all(z == "richtig" for z in st) else "leer" if all(z == "offen" for z in st) else "teils" if any(z == "richtig" for z in st) else "falsch"
        s += f'<rect x="{x}" y="{y + 3}" width="19.5" height="15" rx="1" fill="#fff" stroke="#bbb" stroke-width="0.3"/>'
        s += txt(x + 2, y + 8, f"Nr. {n}", 3.3, "bold", TEAL) + symbol(x + 15.5, y + 6.8, art)
        s += txt(x + 9.75, y + 15, name if len(name) < 13 else name.split(",")[0], 2.6, anchor="middle")
    q = info["quoten"]
    kann = [BEREICH[b] for b in "LWMZNSK" if q[b] == 1]
    ueben = [BEREICH[b] for b in sorted(BEREICH, key=lambda b: (q[b], WICHTIG.index(b))) if q[b] < 1][:2]
    y += 25
    if kann:
        s += txt(14, y, '<tspan font-weight="bold">Das kannst du schon: </tspan>' + ", ".join(kann) + ".", 3.8)
        y += 6
    if ueben:
        s += txt(14, y, '<tspan font-weight="bold">Daran arbeitest du jetzt: </tspan>' + " und ".join(ueben) + ".", 3.8)
        y += 6
    s += txt(14, y, "Löse die Aufgaben der Reihe nach. Kontrolliere selbst mit dem Lösungsblatt, gesucht wird nach dem Kürzel (z. B. M2).", 3.3, "normal", "#444")
    s += txt(14, y + 5, "Deine Aufgaben: " + "; ".join(auswahl), 3.3, "bold", "#444")
    return s


def blatt(nr, info, auswahl, seiten):
    out = []
    for i, ids in enumerate(seiten + [[]] * (2 - len(seiten))):
        s = kopf(nr, info, auswahl) if i == 0 else ""
        y = OBEN + KOPF_H if i == 0 else OBEN
        for kz in ids:
            s += AUFG[kz][4](y, False)
            y += AUFG[kz][3] + ABSTAND
        if i == 1:
            s += txt(198, 292, f"Nummer {nr}", 3.0, "normal", "#888", "end")
        out.append(s)
    return out


def loesungsblatt():
    seiten, s, y = [], txt(14, OBEN + 5, "Mathematik 7c   Förderaufgaben Dreiecke: Lösungen (alle Aufgaben)", 5.0, "bold"), OBEN + 10
    for kz, *_ in POOL:
        h = AUFG[kz][3]
        if y + h > UNTEN:
            seiten.append(s)
            s, y = "", OBEN
        s += AUFG[kz][4](y, True)
        y += h + ABSTAND
    seiten.append(s)
    return seiten


def nummer_sort(n):
    return (0, int(n)) if n.isdigit() else (1, n)


if __name__ == "__main__":
    daten = auswerten()
    alle, zeilen = [], []
    for nr in sorted(daten, key=nummer_sort):
        auswahl, seiten = zuteilen(daten[nr]["quoten"])
        alle += blatt(nr, daten[nr], auswahl, seiten)
        zeilen.append(f"| {nr} | {daten[nr]['version']} | " + "; ".join(auswahl) + " |")
        print(f"{nr:>4}  {', '.join(auswahl)}")
    print(pdf(f"{NAME} – alle Nummern", alle).name, len(alle), "Seiten")
    print(pdf(f"{NAME} – Lösungen", loesungsblatt()).name)
    (AUSW / "Zuteilung Förderaufgaben.md").write_text(
        "---\ntags: [mathematik, diagnose, dreiecke]\ndate: 2026-11-04\n---\n\n# Zuteilung Förderaufgaben Dreiecke 7c\n\n"
        "Erzeugt von `baue_foerderblaetter.py`. Bogen-IDs (A03, A07, A11, B05, B09) stehen für unklare Nummern, "
        "Zuordnung in `Auswertung 7c/baue_json.py` eintragen und beide Skripte neu laufen lassen.\n\n"
        "| Nummer | Version | Aufgaben |\n|---|---|---|\n" + "\n".join(zeilen) + "\n", encoding="utf-8")
