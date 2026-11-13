#!/usr/bin/env python3
"""Mindmap Mathematik Klasse 7c (Schuljahr 26/27).
Quellen: Stoffverteilungsplan Schule (Spalte „Bei dir 7c“), baue_uebersicht_mathe7.py (gehaltene Stunden),
Rezepte aus den Stunden-HTMLs Woche 2–8. Stand 13.11.2026: Rationale Zahlen fertig, Dreiecke laufen."""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "04 Ressourcen/Mathematik/Mathematik Klasse 7c – Mindmap.excalidraw"
GRAU = "#475569"

m = Mindmap("Mathematik\nKlasse 7c")

# 1 Rationale Zahlen: Zahlenstrahl mit 2 − 5 = −3
zx, zy = m.ast(0, "1  Rationale Zahlen\nWoche 1–7, KA 1", [
    ("Start: Grundlagen-Check", "Brüche sind Zahlen; Dezimalbrüche wiederholt"),
    ("Plus und Minus am Zahlenstrahl", "Plus rechts, Minus links; über 0 wechselt das Zeichen"),
    ("Minusklammer", "Minus davor: Term für Term umdrehen"),
    ("Mal, Geteilt, gemischte Aufgaben", "gleiche Zeichen +, verschiedene −; Punkt vor Strich"),
])
col = m.farben[0][1]
u, y0 = 34, zy + 40
m.pfeil([(zx - 5.6 * u, y0), (zx + 5.6 * u, y0)], GRAU, 1.5)
for k in range(-5, 6):
    m.linie([(zx + k * u, y0 - 8), (zx + k * u, y0 + 8)], GRAU, 1.5 if k else 2.5)
    if k % 2 == 0 or k in (-3,):
        lab = str(k).replace("-", "−")
        m.text(zx + k * u - len(lab) * 4.5, y0 + 14, lab, 15, col if k == -3 else GRAU, w=len(lab) * 9)
m.ell(zx + 2 * u, y0, 6, col, col, 1)
m.pfeil([(zx + 2 * u, y0 - 40), (zx - 3 * u, y0 - 40)], "#dc2626", 2.5)
m.text(zx - 50, y0 - 100, "2 − 5 = −3", 18, col, w=100)
m.text(zx - 30, y0 - 66, "5 nach links", 13, "#dc2626", w=110)

# 2 Dreiecke: Dreieck mit Winkelsumme
zx, zy = m.ast(1, "2  Dreiecke\nWoche 8–12, KA 2", [
    ("Winkel messen, Diagnose Dreiecke", "Geodreieck, beide Methoden; Förderblätter"),
    ("Winkel an Geraden, Winkelsumme", "daneben: 180° minus, sonst gleich; Dreieck 180°"),
    ("Dreiecksformen, Konstruktion", "nach Seiten und Winkeln; Konstruieren ab Woche 9", True),
    ("Thaleskreis, Höhen, Mittelsenkrechte", "Winkelhalbierende; danach Puffer und KA 2", True),
])
col = m.farben[1][1]
A, B, C = (zx - 160, zy + 80), (zx + 150, zy + 80), (zx - 40, zy - 110)
m.linie([A, B, C, A], col, 2.5, fill="#ffedd5")
m.text(A[0] + 22, A[1] - 30, "α", 20, col, w=14)
m.text(B[0] - 40, B[1] - 30, "β", 20, col, w=14)
m.text(C[0] - 6, C[1] + 26, "γ", 20, col, w=14)
m.text(zx - 110, zy + 100, "α + β + γ = 180°", 18, col, w=170)

# 3 Terme: Kacheln 3x + 2x = 5x
zx, zy = m.ast(2, "3  Terme\nWoche 13–17, KA 3", [
    ("Terme und Variablen", "Variable als Platzhalter für eine Zahl"),
    ("Addieren und Subtrahieren", "nur Gleichartiges zusammenfassen"),
    ("Multiplizieren und Dividieren", "Zahlen mal Zahlen, Variablen mal Variablen"),
    ("Klammern, Ausmultiplizieren", "Minusklammer wie bei den Zahlen; KA 3 Woche 16"),
], geplant=True)
col = m.farben[2][1]
s, xx = 44, zx - 180
for k in range(5):
    if k == 3:
        m.text(xx + 4, zy - 52, "+", 22, col, w=16)
        xx += 30
    m.rect(xx, zy - 64, s, s, "#fde68a", col, 1.5)
    m.text(xx + 16, zy - 54, "x", 20, col, w=12)
    xx += s + 8
m.text(zx - 110, zy + 10, "3x + 2x = 5x", 22, col, w=160)
m.text(zx - 130, zy + 60, "aber: 3x + 2 bleibt", 16, GRAU, w=180)

# 4 Gleichungen: Waage 2x + 1 = 7
zx, zy = m.ast(3, "4  Gleichungen\nWoche 19–22", [
    ("Lösen durch Probieren", "Welche Zahl passt?"),
    ("Äquivalenzumformungen", "auf beiden Seiten dasselbe rechnen"),
    ("Gleichungen mit Klammern", "erst Klammern auflösen, dann umformen"),
    ("Mit Gleichungen Fragen beantworten", "Sachaufgaben; Üben"),
], geplant=True)
col = m.farben[3][1]
by = zy - 20
m.linie([(zx - 170, by), (zx + 170, by)], GRAU, 2.5)
m.linie([(zx, by - 12), (zx, by + 120)], GRAU, 2.5)
m.linie([(zx - 50, by + 120), (zx + 50, by + 120)], GRAU, 2.5)
for k, lab in enumerate(("x", "x", "1")):
    m.rect(zx - 160 + k * 46, by - 44, 40, 40, "#fecaca" if lab == "x" else "#ffffff", col, 1.5)
    m.text(zx - 146 + k * 46, by - 36, lab, 20, col, w=12)
m.rect(zx + 90, by - 44, 60, 40, "#ffffff", col, 1.5)
m.text(zx + 114, by - 36, "7", 20, col, w=12)
m.text(zx - 150, by - 100, "2x + 1 = 7   | − 1", 18, col, w=190)

# 5 Zuordnungen: Gerade durch 0 und Hyperbel
zx, zy = m.ast(4, "5  Zuordnungen\nWoche 23–27, KA 4", [
    ("Proportionale Zuordnung", "doppelt so viel, doppelt so teuer"),
    ("Dreisatz", "über 1 rechnen: teilen, dann malnehmen"),
    ("Antiproportionale Zuordnung", "doppelt so viele, halb so lange"),
    ("Umgekehrter Dreisatz", "Üben; KA 4 vor dem Schullandheim"),
], geplant=True)
col = m.farben[4][1]
gx, gy, gw, gh = zx - 150, zy + 130, 300, 250
m.pfeil([(gx, gy), (gx + gw + 20, gy)], GRAU, 1.5)
m.pfeil([(gx, gy), (gx, gy - gh - 10)], GRAU, 1.5)
m.linie([(gx, gy), (gx + gw - 40, gy - gh + 30)], col, 2.5)
m.linie([(gx + gw * k / 40 + 25, gy - min(gh - 20, 2400 / (gw * k / 40 + 25) * 2)) for k in range(41)],
        "#0f766e", 2.5, "dashed")
m.text(gx + 140, gy - gh + 10, "proportional", 14, col, w=110)
m.text(gx + 175, gy - 60, "antiproportional", 14, "#0f766e", w=135)

# 6 Prozent, Vierecke: Prozentstreifen und Parallelogramm
zx, zy = m.ast(5, "6  Prozent, Vierecke\nWoche 30–35", [
    ("Absoluter und relativer Vergleich", "Anteile vergleichen statt Anzahlen"),
    ("Prozentsatz, Prozentwert, Grundwert", "Dreisatz über 1 %, 100 % markieren"),
    ("Prozentdiagramme", "Streifen- und Kreisdiagramm"),
    ("Vierecke", "Haus der Vierecke; Winkelsumme, Konstruktion"),
], geplant=True)
col = m.farben[5][1]
sx, sy, sw = zx - 160, zy - 90, 320
m.rect(sx, sy, sw, 40, "#ffffff", col, 1.5)
m.rect(sx, sy, sw * 0.25, 40, "#6ee7b7", col, 1.5)
m.text(sx - 10, sy - 26, "0 %", 14, GRAU, w=30)
m.text(sx + sw * 0.25 - 18, sy - 26, "25 %", 14, col, w=36)
m.text(sx + sw - 30, sy - 26, "100 %", 14, col, w=45)
m.text(sx + sw - 92, sy + 48, "Grundwert", 14, col, w=90)
m.linie([(zx - 110, zy + 120), (zx + 70, zy + 120), (zx + 120, zy + 40), (zx - 60, zy + 40), (zx - 110, zy + 120)],
        col, 2.5, fill="#d1fae5")

m.legende("Stand 13.11.2026\ndurchgezogen: gemacht\ngestrichelt: geplant")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
