#!/usr/bin/env python3
"""Mindmap Mathematik Klasse 10b (Schuljahr 26/27).
Quellen: Stoffverteilungsplan 26-27 Mathe 10, baue_uebersicht_mathe10.py (gehaltene Stunden), Rezepte aus den
Stunden-HTMLs (Prozent Wdh, Zinsen, Zinseszins, Zuwachssparen), Stochastik-Übung und Kurztest.
Stand 13.11.2026: Wahrscheinlichkeit, Prozent und KA 1 gemacht; ab Trigonometrie geplant."""
import math
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "04 Ressourcen/Mathematik/Mathematik Klasse 10b – Mindmap.excalidraw"
GRAU = "#475569"

m = Mindmap("Mathematik\nKlasse 10b")

# 1 Wahrscheinlichkeit: Baumdiagramm zweistufig
zx, zy = m.ast(0, "1  Wahrscheinlichkeit\nWoche 1–3, Kurztest", [
    ("Basiswissen, Zufall", "Wahrscheinlichkeit als Anteil"),
    ("Zweistufige Versuche", "Baumdiagramm; mit und ohne Zurücklegen"),
    ("Pfadregeln", "entlang multiplizieren, Pfade addieren"),
    ("Erwartungswert mit Einsatz", "P · Gewinn + … − Einsatz; fair heißt E = 0"),
])
col = m.farben[0][1]
r = (zx - 170, zy)
m.ell(*r, 6, col, col, 1)
for k1, (dy1, l1) in enumerate(((-90, "r"), (90, "b"))):
    p1 = (zx - 30, zy + dy1)
    m.linie([r, p1], col, 2)
    m.text((r[0] + p1[0]) / 2 - 16, (r[1] + p1[1]) / 2 - 24, l1, 16, col, w=12)
    m.ell(*p1, 5, col, col, 1)
    for dy2, l2 in ((-40, "r"), (40, "b")):
        p2 = (zx + 110, zy + dy1 + dy2)
        m.linie([p1, p2], col, 1.5)
        m.text(p2[0] + 10, p2[1] - 10, l1 + l2, 15, col, w=24)
m.text(zx - 150, zy + 140, "P(rr) = P(r) · P(r)", 15, GRAU, w=180)

# 2 Prozent und Zinsen: Kapital wächst mit q
zx, zy = m.ast(1, "2  Prozent und Zinsen\nWoche 3–7, KA 1", [
    ("Prozent wiederholt", "Was ist 100 %? W = G · p %; G und p % umgestellt"),
    ("Vermehrter und verminderter Grundwert", "Rabatt, Skonto"),
    ("Zinsen und Zinseszins", "Kₙ = K₀ · qⁿ mit q = 1 + p/100"),
    ("Zinssatz gesucht, Zuwachssparen", "n-te Wurzel; alle Zinsfaktoren malnehmen"),
])
col = m.farben[1][1]
bx, by = zx - 150, zy + 100
m.linie([(bx - 10, by), (bx + 300, by)], GRAU, 1.5)
for k in range(4):
    h = 90 * 1.3 ** k
    m.rect(bx + k * 75, by - h, 50, h, "#fdba74", col, 1.5)
    m.text(bx + k * 75 + 12, by + 8, f"K{'₀₁₂₃'[k]}", 16, col, w=24)
    if k:
        m.text(bx + k * 75 - 26, by - h - 26, "·q", 15, col, w=20)

# 3 Trigonometrie: rechtwinkliges Dreieck, Seiten von α aus
zx, zy = m.ast(2, "3  Trigonometrie\nWoche 8–10", [
    ("sin, cos, tan im rechtwinkligen Dreieck", "Seitenverhältnisse"),
    ("Beliebige Dreiecke, Vielecke", "in rechtwinklige Teildreiecke zerlegen"),
    ("Trigonometrie im Raum", "Strecken und Winkel in Körpern"),
    ("Sinus am Einheitskreis", "Woche 10"),
], geplant=True)
col = m.farben[2][1]
A, B, C = (zx - 170, zy + 90), (zx + 130, zy + 90), (zx + 130, zy - 90)
m.linie([A, B, C, A], col, 2.5, fill="#fef9c3")
rw = 26   # rechter Winkel bei B: Viertelkreis mit Punkt
m.linie([(B[0] - rw * math.cos(t * math.pi / 40), B[1] - rw * math.sin(t * math.pi / 40)) for t in range(21)], col, 1.5)
m.ell(B[0] - 10, B[1] - 10, 2.5, col, col, 1)
m.text(A[0] + 36, A[1] - 26, "α", 18, col, w=12)
m.text(zx - 60, B[1] + 8, "Ankathete", 14, GRAU, w=80)
m.text(B[0] + 8, zy - 8, "Gegen-\nkathete", 14, GRAU, w=60)
m.text(zx - 130, zy - 40, "Hypotenuse", 14, GRAU, w=90)
m.text(zx - 160, zy - 150, "sin α = Gegenkathete : Hypotenuse", 13, col, w=280)

# 4 Körper: Pyramide mit Höhe
zx, zy = m.ast(3, "4  Körper\nWoche 11–15, KA 2", [
    ("Pyramide: Volumen und Oberfläche", "sechsseitig und n-seitig"),
    ("Kegel und Kugel", "Volumen und Oberfläche"),
    ("Zusammengesetzte Körper", "Wiederholung Prisma; KA 2 am 18.12."),
    ("Streckenzüge auf Körpern", "Woche 15"),
], geplant=True)
col = m.farben[3][1]
p = [(zx - 140, zy + 90), (zx + 80, zy + 90), (zx + 150, zy + 30), (zx - 70, zy + 30)]
S = (zx + 5, zy - 140)
m.linie([p[0], p[1], p[2]], col, 2)
m.linie([p[2], p[3], p[0]], col, 1.5, "dashed")
for q in p:
    m.linie([q, S], col, 2 if q != p[3] else 1.5, "solid" if q != p[3] else "dashed")
M = (zx + 5, zy + 60)
m.linie([S, M], GRAU, 1.5, "dashed")
m.text(M[0] + 8, zy - 30, "h", 18, GRAU, w=12)
m.text(zx - 150, zy + 110, "V = ⅓ · G · h", 18, col, w=150)

# 5 Daten und Potenzen: Boxplot
zx, zy = m.ast(4, "5  Daten, Potenzen\nWoche 16–18, KA 3", [
    ("Daten und Boxplot", "Median, Quartile, Spannweite"),
    ("Potenzen mit ganzen Exponenten", "gleiche Basis"),
    ("Potenzen mit gleichem Exponenten", "Woche 18"),
    ("Wissenschaftliche Schreibweise", "KA 3 am 4.2."),
], geplant=True)
col = m.farben[4][1]
ay = zy - 20
m.linie([(zx - 170, ay), (zx - 110, ay)], col, 2)
m.rect(zx - 110, ay - 30, 170, 60, "#ede9fe", col, 2)
m.linie([(zx - 30, ay - 30), (zx - 30, ay + 30)], col, 3)
m.linie([(zx + 60, ay), (zx + 170, ay)], col, 2)
for x in (zx - 170, zx + 170):
    m.linie([(x, ay - 16), (x, ay + 16)], col, 2)
m.text(zx - 50, ay - 56, "Median", 14, col, w=56)
m.text(zx - 160, ay + 56, "2,5 · 10⁶ = 2 500 000", 17, GRAU, w=210)

# 6 Funktionen und Prüfung: Parabel und Gerade
zx, zy = m.ast(5, "6  Funktionen, Prüfung\nWoche 19–28, KA 4", [
    ("Wiederholung: LGS und Gleichungen", "Bruchgleichungen, quadratische Gleichungen"),
    ("Geraden: y = mx + b", "Punktprobe, Punkt-Steigungs-Form"),
    ("Parabeln", "y = ax² + c; Normalform, Scheitelform, Nullstellen"),
    ("Abschlussprüfung Do 29.4.", "KA 4 am 6.4.; Prüfungsvorbereitung"),
], geplant=True)
col = m.farben[5][1]
ox, oy, e = zx - 20, zy + 70, 30
m.pfeil([(ox - 160, oy), (ox + 180, oy)], GRAU, 1.5)
m.pfeil([(ox, oy + 60), (ox, oy - 200)], GRAU, 1.5)
m.linie([(ox + e * t / 4, oy - e * ((t / 4 - 1) ** 2 - 1.5)) for t in range(-6, 15)], col, 2.5)
m.linie([(ox - 150, oy - 10), (ox + 170, oy - 150)], "#0f766e", 2)
m.ell(ox + e, oy + 1.5 * e, 4, col, col, 1)
m.text(ox + e + 8, oy + 1.5 * e - 4, "S", 14, col, w=12)
m.text(ox - 150, oy - 190, "y = mx + b", 14, "#0f766e", w=90)

m.legende("Stand 13.11.2026\ndurchgezogen: gemacht\ngestrichelt: geplant")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
