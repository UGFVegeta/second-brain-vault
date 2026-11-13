#!/usr/bin/env python3
"""Mindmap Physik Klasse 7c (Schuljahr 26/27).
Quellen: Stoffverteilungsplan Physik Klasse 7 2026-27.md, Stunden-HTMLs Leitfrage 1–5 und Lochkamera
(Antworten auf die Leitfragen). Stand 13.11.2026: Einstieg und Leitfragen 1–5 gemacht, ab Lochkamera geplant."""
import math
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "04 Ressourcen/Physik/Physik Klasse 7c – Mindmap.excalidraw"
GRAU = "#475569"
GELB, GELB_R = "#facc15", "#b45309"

m = Mindmap("Physik\nKlasse 7c")


def lampe(x, y, r=16):
    m.ell(x, y, r, GELB, GELB_R, 1.5)
    for k in range(8):
        w = k * math.pi / 4
        m.linie([(x + (r + 5) * math.cos(w), y + (r + 5) * math.sin(w)),
                 (x + (r + 13) * math.cos(w), y + (r + 13) * math.sin(w))], GELB_R, 1.5)


# 1 Licht und Sehen: Lampe → Gegenstand → Auge
zx, zy = m.ast(0, "1  Licht und Sehen\nWoche 1–4", [
    ("Einstieg: Fachraum und Messen", "Sicherheit; Größe, Maßzahl, Einheit"),
    ("F1 Warum sehen wir überhaupt etwas?", "Licht muss in unser Auge gelangen"),
    ("Lichtquellen, beleuchtete Körper", "Mond und Wolke werfen Sonnenlicht zurück"),
    ("F2 Licht trifft auf einen Körper", "Streuung, Absorption, Transmission; Emission"),
])
col = m.farben[0][1]
lampe(zx - 150, zy - 80)
m.ell(zx, zy + 40, 28, "#93c5fd", col, 1.5)
m.ell(zx + 150, zy - 70, 0, "#ffffff", col, 1.5, rx=30, ry=18)
m.ell(zx + 140, zy - 70, 8, col, col, 1)
m.pfeil([(zx - 128, zy - 60), (zx - 26, zy + 22)], GELB_R, 2)
m.pfeil([(zx + 24, zy + 22), (zx + 118, zy - 56)], GELB_R, 2)
m.text(zx - 180, zy - 130, "Lichtquelle", 14, GELB_R, w=100)
m.text(zx - 60, zy + 80, "beleuchteter Körper", 14, col, w=170)
m.text(zx + 125, zy - 120, "Auge", 14, col, w=40)

# 2 Ausbreitung und Schatten: zwei Lampen, Körper, Schirm
zx, zy = m.ast(1, "2  Ausbreitung, Schatten\nWoche 5–7", [
    ("F3 Warum sehen wir nicht um die Ecke?", "Licht breitet sich geradlinig aus"),
    ("Lichtstrahlenmodell, Blende", "Strahlen zeichnen; seitlich sichtbar nur mit Nebel"),
    ("F4 Warum hat ein Schatten weiche Ränder?", "mehrere oder ausgedehnte Lichtquellen"),
    ("Kern- und Halbschatten", "Halbschatten: mindestens eine Lampe leuchtet hinein"),
])
col = m.farben[1][1]
L1, L2 = (zx - 170, zy - 40), (zx - 170, zy + 40)
lampe(*L1, 12)
lampe(*L2, 12)
kx, ko, ku = zx + 60, zy - 50, zy + 50      # Körper: senkrechter Balken
sx = zx + 160                               # Schirm


def bis_schirm(L, p):
    t = (sx - L[0]) / (p[0] - L[0])
    return (sx, L[1] + t * (p[1] - L[1]))


for L in (L1, L2):
    for p in ((kx, ko), (kx, ku)):
        m.linie([L, (kx, p[1])], "#f59e0b", 1, "dashed")
        m.linie([(kx, p[1]), bis_schirm(L, p)], "#f59e0b", 1, "dashed")
m.rect(kx - 8, ko, 16, ku - ko, "#334155", "#0f172a", 1)
c, d = bis_schirm(L2, (kx, ko))[1], bis_schirm(L1, (kx, ku))[1]   # Rand des Halbschattens
a, b = bis_schirm(L1, (kx, ko))[1], bis_schirm(L2, (kx, ku))[1]   # Rand des Kernschattens
m.rect(sx, c, 14, d - c, "#cbd5e1", GRAU, 1)
m.rect(sx, a, 14, b - a, "#334155", "#0f172a", 1)
m.linie([(sx + 14, zy - 160), (sx + 14, zy + 160)], GRAU, 2)
m.pfeil([(sx - 30, zy - 150), (sx - 2, a + 4)], GRAU, 1)
m.text(sx - 110, zy - 175, "Kernschatten", 13, GRAU, w=100)
m.pfeil([(sx - 30, zy + 150), (sx - 2, d - 6)], GRAU, 1)
m.text(sx - 110, zy + 155, "Halbschatten", 13, GRAU, w=100)

# 3 Mond und Lochkamera: Sonne, Erde, Mond mit beleuchteter Hälfte
zx, zy = m.ast(2, "3  Mond, Lochkamera\nWoche 8–9", [
    ("F5 Warum sieht der Mond nicht gleich aus?", "Sonne beleuchtet eine Hälfte; Mond umläuft die Erde"),
    ("Sonnen- und Mondfinsternis", "Sonne, Erde und Mond auf einer Linie"),
    ("Jahreszeiten (Einschub)", "geneigte Erdachse: Strahlen steil oder flach"),
    ("Lochkamera", "Bild steht auf dem Kopf; Bau als Hausaufgabe", True),
])
col = m.farben[2][1]
lampe(zx - 160, zy, 30)
ex, ey = zx + 50, zy
m.ell(ex, ey, 0, "transparent", "#94a3b8", 1, rx=100, ry=100, style="dashed")
m.ell(ex, ey, 26, "#60a5fa", "#1e40af", 1.5)
for wg in (0, 90, 180, 270):
    mx, my = ex + 100 * math.cos(math.radians(wg)), ey - 100 * math.sin(math.radians(wg))
    m.ell(mx, my, 14, "#334155", "#0f172a", 1)
    halb = [(mx + 14 * math.cos(math.radians(t)), my - 14 * math.sin(math.radians(t))) for t in range(90, 271, 15)]
    m.linie(halb + [halb[0]], "#0f172a", 1, fill="#fde68a")   # zur Sonne hin beleuchtete Hälfte
m.text(zx - 190, zy + 50, "Sonne", 14, GELB_R, w=50)
m.text(ex - 22, ey + 32, "Erde", 14, "#1e40af", w=40)
m.text(ex + 22, ey - 112, "Mond", 14, GRAU, w=40)

# 4 Spiegel und Linsen: Reflexionsgesetz
zx, zy = m.ast(3, "4  Spiegel und Linsen\nWoche 10–16, KA 1", [
    ("F6 Was passiert am Spiegel?", "Einfallswinkel gleich Reflexionswinkel; Spiegelbild"),
    ("F7 Warum sieht der Strohhalm geknickt aus?", "Brechung und ihre Richtung"),
    ("F8 Wie vergrößert eine Lupe?", "Sammel- und Zerstreuungslinse; das Auge"),
    ("Kurz- und Weitsichtigkeit", "KA 1 in Woche 17: Optik I und II bis Linsen"),
], geplant=True)
col = m.farben[3][1]
sy = zy + 100
m.rect(zx - 170, sy, 340, 14, "#e2e8f0", GRAU, 1.5)
m.linie([(zx, sy), (zx, zy - 150)], GRAU, 1.5, "dashed")
m.pfeil([(zx - 150, zy - 120), (zx - 3, sy - 3)], "#dc2626", 2.5)
m.pfeil([(zx + 3, sy - 3), (zx + 150, zy - 120)], "#dc2626", 2.5)
m.text(zx - 50, sy - 70, "α", 20, col, w=14)
m.text(zx + 34, sy - 70, "α'", 20, col, w=24)
m.text(zx - 150, sy + 22, "Spiegel", 14, GRAU, w=70)
m.text(zx + 8, zy - 160, "Lot", 14, GRAU, w=30)

# 5 Farben und Akustik: Prisma mit Spektrum
zx, zy = m.ast(4, "5  Farben und Akustik\nWoche 19–24", [
    ("F9 Woher kommen die Farben?", "Prisma, Spektrum, Regenbogen"),
    ("Unsichtbares Licht, Farbaddition", "IR und UV; drei farbige Lampen"),
    ("F10 Wie entsteht Schall?", "Sender, Ausbreitung, Empfänger"),
    ("F11, F12 Tonhöhe, Lautstärke, Ohr", "Amplitude, Frequenz; Lärm schädigt das Gehör"),
], geplant=True)
col = m.farben[4][1]
P = [(zx - 60, zy + 90), (zx + 60, zy + 90), (zx, zy - 50)]
m.linie(P + [P[0]], col, 2, fill="#ede9fe")
m.linie([(zx - 180, zy + 40), (zx - 32, zy + 22)], "#94a3b8", 3)
m.text(zx - 180, zy + 50, "weißes Licht", 13, GRAU, w=110)
for k, f in enumerate(("#dc2626", "#f97316", "#facc15", "#16a34a", "#2563eb", "#7c3aed")):
    m.linie([(zx + 34, zy + 30 + k * 3), (zx + 180, zy - 30 + k * 26)], f, 2.5)

# 6 Magnetismus und Strom: Stabmagnet mit Feldlinien
zx, zy = m.ast(5, "6  Magnetismus, Strom\nWoche 25–37, KA 2", [
    ("Magnetpole, Magnetfeld", "Anziehung und Abstoßung; Feldlinien"),
    ("Kompass, Elementarmagnete", "Erdmagnetfeld; Magnetisieren"),
    ("Einfacher Stromkreis, Schaltungen", "Schaltsymbole; Leiter, Nichtleiter; Und, Oder"),
    ("Stromstärke und Spannung messen", "Gefahren des Stroms; KA 2 in Woche 36"),
], geplant=True)
col = m.farben[5][1]
m.rect(zx - 90, zy - 20, 90, 40, "#fca5a5", "#b91c1c", 1.5)
m.rect(zx, zy - 20, 90, 40, "#86efac", "#15803d", 1.5)
m.text(zx - 52, zy - 11, "N", 18, "#b91c1c", w=12)
m.text(zx + 40, zy - 11, "S", 18, "#15803d", w=12)
for h in (55, 95, 135):
    for s in (-1, 1):
        m.linie([(zx + 80 * math.cos(math.radians(t)) * (1 + h / 160),
                  zy + s * (20 + h * math.sin(math.radians(t)))) for t in range(180, -1, -10)],
                "#64748b", 1.2, "dashed")

m.legende("Stand 13.11.2026\ndurchgezogen: gemacht\ngestrichelt: geplant")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
