#!/usr/bin/env python3
"""Mindmap „Landesprogramme und Hilfen“ mit Blick auf Konflikte zwischen Schülern, Lehrkräften und Eltern.
Quellen: Notiz „Schularten, Übergänge und Landesprogramme“ (13.11.2026) mit Quellenliste. Keine Personennamen."""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "03 Bereiche/Führung & Schulentwicklung/Landesprogramme und Hilfen – Mindmap.excalidraw"
GRAU = "#475569"

m = Mindmap("Landesprogramme\nund Hilfen")

# 1 stark.stärker.WIR.: drei Ebenen als Pyramide
zx, zy = m.ast(0, "1  stark.stärker.WIR.\nPräventionsrahmen", [
    ("Landeskonzept seit 2011", "nach Winnenden und Wendlingen"),
    ("Gewalt, Sucht, Gesundheit", "auf Ebene Schule, Klasse, Einzelne"),
    ("Jede Schule wählt Schritte und Tempo", "Rahmen, kein fertiges Programm"),
    ("Präventionsbeauftragte des ZSL", "Päd. Tag, Elternabend, Zertifikat"),
])
col = m.farben[0][1]
m.linie([(zx - 180, zy + 130), (zx + 180, zy + 130), (zx, zy - 150), (zx - 180, zy + 130)], col, 2, fill="#dbeafe")
m.linie([(zx - 120, zy + 37), (zx + 120, zy + 37)], col, 1.5)
m.linie([(zx - 60, zy - 56), (zx + 60, zy - 56)], col, 1.5)
m.text(zx - 50, zy + 72, "Schule", 16, col, "center", w=100)
m.text(zx - 50, zy - 20, "Klasse", 16, col, "center", w=100)
m.text(zx - 40, zy - 100, "Einzelne", 13, col, "center", w=80)

# 2 Konflikte und Mobbing: zwei Streitende, eine Vermittlung
zx, zy = m.ast(1, "2  Konflikte\nund Mobbing", [
    ("Mobbing stoppen", "Teil von stark.stärker.WIR., Klasse 1 bis 13"),
    ("Beratungslehrkraft", "an den meisten Schulen, auch bei Mobbing"),
    ("Schulpsychologische Beratungsstelle", "beim ZSL, für Einzelfälle und Lehrkräfte"),
    ("Klassenrat, Streitschlichtung", "schulinterne Bausteine"),
    ("Erst pädagogisch, dann § 90 SchG", "Erziehungs- und Ordnungsmaßnahmen"),
])
col = m.farben[1][1]
m.ell(zx - 130, zy - 60, 30, "#fed7aa", col, 2)
m.ell(zx + 130, zy - 60, 30, "#fed7aa", col, 2)
m.pfeil([(zx - 96, zy - 70), (zx - 20, zy - 70)], "#dc2626", 2)
m.pfeil([(zx + 96, zy - 50), (zx + 20, zy - 50)], "#dc2626", 2)
m.ell(zx, zy + 90, 34, "#ffffff", col, 2)
m.pfeil([(zx - 110, zy - 30), (zx - 30, zy + 66)], col, 1.5, style="dashed")
m.pfeil([(zx + 110, zy - 30), (zx + 30, zy + 66)], col, 1.5, style="dashed")
m.text(zx - 80, zy + 132, "Vermittlung", 15, col, "center", w=160)

# 3 Krisen und Schutz: Schild
zx, zy = m.ast(2, "3  Krisen und Schutz", [
    ("Krisenteam ist Pflicht", "VwV Krisenereignisse vom 08.03.2024"),
    ("Leitung hat die Schulleitung", "Krisenplan nach Muster des Ministeriums"),
    ("Polizei: Referat Prävention", "Beratung durch das Polizeipräsidium"),
    ("Schutzkonzept gegen sexualisierte Gewalt", "Pflicht für alle Schulen seit 2025"),
])
col = m.farben[2][1]
m.linie([(zx - 120, zy - 140), (zx + 120, zy - 140), (zx + 120, zy + 10), (zx, zy + 140),
         (zx - 120, zy + 10), (zx - 120, zy - 140)], col, 2.5, fill="#fef3c7")
m.text(zx - 90, zy - 60, "Krisenteam\nKrisenplan\nSchutzkonzept", 16, col, "center", w=180)

# 4 Eltern: Dreieck Schüler, Eltern, Schule
zx, zy = m.ast(3, "4  Eltern", [
    ("Erziehungsgemeinschaft", "§ 55 SchG: gemeinsame Verantwortung"),
    ("Elternbeirat und Klassenpflegschaft", "Elternbeiratsverordnung"),
    ("Interkulturelle Elternmentoren", "Elternstiftung BW; vermitteln bei Konflikten"),
    ("Seminare der Elternstiftung", "für Elternvertreter"),
])
col = m.farben[3][1]
for x, y, lab in ((zx, zy - 130, "Kind"), (zx - 140, zy + 100, "Eltern"), (zx + 140, zy + 100, "Schule")):
    m.ell(x, y, 0, "#ffffff", col, 2, rx=58, ry=32)
    m.text(x - 50, y - 9, lab, 15, col, "center", w=100)
m.pfeil([(zx - 30, zy - 96), (zx - 115, zy + 66)], col, 1.5, head="arrow")
m.pfeil([(zx + 30, zy - 96), (zx + 115, zy + 66)], col, 1.5, head="arrow")
m.pfeil([(zx - 80, zy + 100), (zx + 80, zy + 100)], col, 2, head="arrow")
m.text(zx - 70, zy + 140, "§ 55 SchG", 15, col, "center", w=140)

# 5 Zeig, was du kannst!: Stern
zx, zy = m.ast(4, "5  Zeig, was du kannst!\nStärken sichtbar", [
    ("Pflicht in Klasse 8 oder 9", "WRS, HS, RS, GMS und SBBZ"),
    ("Etwa drei Schüler, ein echtes Produkt", "mit Bezug zur eigenen Lebenswelt"),
    ("Vier Phasen", "Thema, Durchführung, Vorstellung, Reflexion"),
    ("Reflexion 30 %, Fach 25 %", "Stärken-Bescheinigung zum Zeugnis"),
    ("Schulleitung legt den Zeitraum fest", "mit den Gremien"),
])
col = m.farben[4][1]
import math  # noqa: E402
pts = []
for k in range(11):
    r = 130 if k % 2 == 0 else 55
    a = -math.pi / 2 + k * math.pi / 5
    pts.append((zx + r * math.cos(a), zy - 10 + r * math.sin(a)))
m.linie(pts, col, 2, fill="#ede9fe")
m.text(zx - 60, zy + 140, "Stärken zum Zeugnis", 14, col, "center", w=120)

# 6 Unterstützer im Team: Netzwerk
zx, zy = m.ast(5, "6  Unterstützung\nim Team", [
    ("Schulsozialarbeit", "Träger meist Gemeinde; Land fördert über KVJS"),
    ("Schulpsychologie und Beratungslehrkraft", ""),
    ("Sonderpädagogischer Dienst", "berät die allgemeine Schule"),
    ("Startchancen, Säule III", "Personal für multiprofessionelle Teams"),
])
col = m.farben[5][1]
m.ell(zx, zy, 36, "#a7f3d0", col, 2)
m.text(zx - 30, zy - 9, "Schule", 15, col, "center", w=60)
for dx, dy, lab in ((-140, -110, "Sozial-\narbeit"), (140, -110, "Schul-\npsychologie"),
                    (-140, 110, "Sonder-\npädagogik"), (140, 110, "Polizei")):
    m.ell(zx + dx, zy + dy, 0, "#ffffff", col, 1.5, rx=62, ry=36)
    m.text(zx + dx - 55, zy + dy - (18 if "\n" in lab else 9), lab, 13, col, "center", w=110)
    m.pfeil([(zx + dx * 0.62, zy + dy * 0.62), (zx + dx * 0.3, zy + dy * 0.3)], col, 1.5)

m.legende("Stand 13.11.2026\nQuellen in der Notiz\nWRS = Werkrealschule")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
