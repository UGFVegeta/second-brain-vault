#!/usr/bin/env python3
"""Mindmap „Daten und Vergleichsarbeiten“: § 114 SchG, Lernstandserhebungen (VERA 3, Kompass 4, Lernstand 5, VERA 8),
Befragungen, Schuldatenblatt, Steuerung, Studien und Datenschutz.
Quellen: § 114 SchG (Stand 16.12.2025), Aufnahmeverordnung, Landesportal/IBBW (Notiz „Schularten, Übergänge und
Landesprogramme“, 13.11.2026). Gestrichelt: Oskars eigener Ansatz. Keine Personennamen."""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "03 Bereiche/Führung & Schulentwicklung/Daten und Vergleichsarbeiten – Mindmap.excalidraw"
GRAU = "#475569"

m = Mindmap("Daten und\nVergleichs-\narbeiten")

# 1 Rechtsgrundlage: Paragrafenzeichen
zx, zy = m.ast(0, "1  Pflicht nach\n§ 114 SchG", [
    ("Datengestützte Qualitätsentwicklung", "Pflicht für alle öffentlichen Schulen"),
    ("Referenzrahmen Schulqualität", "verbindliche Grundlage"),
    ("Interne Evaluation regelmäßig", "extern bei Bedarf durch das IBBW"),
    ("Teilnahme ist Pflicht", "Schulleitung, Lehrkräfte, Schüler"),
])
col = m.farben[0][1]
m.ell(zx, zy, 0, "#ffffff", col, 2.5, rx=120, ry=120)
m.text(zx - 70, zy - 50, "§ 114", 44, col, "center", w=140)
m.text(zx - 80, zy + 135, "Schulgesetz", 15, col, "center", w=160)

# 2 Lernstandserhebungen: Zeitstrahl Klasse 3 bis 8
zx, zy = m.ast(1, "2  Lernstandserhebungen\nwann was", [
    ("Lernstand 2", "Beginn Klasse 2, Deutsch und Mathe; Pflicht ab 2026/27"),
    ("VERA 3", "Klasse 3, Deutsch und Mathe, bundesweit"),
    ("Kompass 4", "Klasse 4, Deutsch und Mathe; zählt für den Übergang"),
    ("Lernstand 5", "Beginn Klasse 5, Deutsch und Mathe; seit 2015/16"),
    ("Lernstand 7", "Beginn Kl. 7; 2026/27 freiwillig, ab 2027/28 Pflicht"),
    ("VERA 8", "Klasse 8, Deutsch, Mathe, Englisch oder Französisch"),
])
col = m.farben[1][1]
ly = zy + 10
m.pfeil([(zx - 195, ly), (zx + 200, ly)], GRAU, 2)
for kl, lab, oben in (("2", "Lernstand 2", True), ("3", "VERA 3", False), ("4", "Kompass 4", True),
                      ("5", "Lernstand 5", False), ("7", "Lernstand 7", True), ("8", "VERA 8", False)):
    x = zx - 170 + (int(kl) - 2) * 58
    vera = lab.startswith("VERA")
    m.ell(x, ly, 12, "#ffffff" if vera else "#fed7aa", col, 2)
    m.text(x - 6, ly - 8, kl, 13, col, w=12)
    m.text(x - 45, ly - 60 if oben else ly + 30, lab, 13, col, "center", w=90)
m.text(zx - 100, ly + 75, "Klassenstufe", 14, GRAU, "center", w=200)
m.text(zx - 190, zy - 175, "gefüllt: Lernstand, Förderung\nleer: VERA, Unterrichtsentwicklung", 13, col, w=380)
m.text(zx - 190, zy + 120, "Alle ohne Noten, Rückmeldung\nbis auf Schülerebene", 13, col, w=380)

# 3 Befragungen: Sprechblasen
zx, zy = m.ast(2, "3  Befragungen\nSchüler und Lehrkräfte", [
    ("Zentrale Erhebungen des IBBW", "§ 114 Abs. 3 SchG"),
    ("Unterricht, Zusammenarbeit", "Schulklima, Wohlbefinden"),
    ("Schulleitung sieht die Klassenebene", "Lehrkräfte ihre eigenen Klassen"),
    ("Teilnahme ist Pflicht", "Auswertung im Landesverfahren"),
])
col = m.farben[2][1]
for x, y, lab in ((zx - 70, zy - 80, "Schüler"), (zx + 80, zy + 40, "Lehrkräfte")):
    m.ell(x, y, 0, "#ffffff", col, 2, rx=100, ry=52)
    m.linie([(x - 30, y + 46), (x - 55, y + 90), (x - 5, y + 50)], col, 2, fill="#ffffff")
    m.text(x - 55, y - 9, lab, 16, col, "center", w=110)

# 4 Schuldatenblatt: Blatt mit Balken
zx, zy = m.ast(3, "4  Schuldatenblatt\njährlich vom IBBW", [
    ("Statistik, Lernstände, Prüfungen", "dazu die Ergebnisse der Befragungen"),
    ("Schule, Klassenstufe, Bildungsgang", "aggregiert, mit Vergleichswerten"),
    ("Aufbau wie der Referenzrahmen", "drei Hauptbereiche"),
    ("Grundlage fürs Statusgespräch", "mit der Schulaufsicht"),
])
col = m.farben[3][1]
m.rect(zx - 110, zy - 150, 220, 290, "#ffffff", col, 2)
m.text(zx - 95, zy - 135, "Schuldatenblatt", 15, col, w=190)
for k, w in enumerate((150, 110, 170, 80)):
    m.rect(zx - 90, zy - 95 + k * 52, w, 30, "#fecaca", col, 1.5)

# 5 Steuerung: Kreislauf Daten → Ziele → Maßnahmen → Prüfen
zx, zy = m.ast(4, "5  Von Daten\nzu Taten", [
    ("Ergebnisse besprechen", "mit Schülern, Eltern, Lehrerkonferenz"),
    ("Statusgespräch mit Schulaufsicht", "Ziel- und Leistungsvereinbarung"),
    ("Fachberater Schulentwicklung", "ZSL begleitet die Schulen"),
    ("Mein Ansatz: Daten zu Taten", "Datengestützte Schulentwicklung v2", True),
])
col = m.farben[4][1]
pos = ((zx, zy - 120, "Daten"), (zx + 130, zy, "Ziele"), (zx, zy + 120, "Maß-\nnahmen"), (zx - 130, zy, "Prüfen"))
for x, y, lab in pos:
    m.ell(x, y, 0, "#ede9fe", col, 2, rx=58, ry=34)
    m.text(x - 50, y - (18 if "\n" in lab else 9), lab, 14, col, "center", w=100)
for (x1, y1, _), (x2, y2, _) in zip(pos, pos[1:] + pos[:1]):
    dx, dy = x2 - x1, y2 - y1
    m.pfeil([(x1 + dx * 0.42, y1 + dy * 0.42), (x1 + dx * 0.62, y1 + dy * 0.62)], col, 2)

# 6 Studien und Datenschutz: Schloss
zx, zy = m.ast(5, "6  Studien und\nDatenschutz", [
    ("PISA, IQB-Bildungstrend", "Stichproben, Pflicht bei Auswahl"),
    ("Daten pseudonymisiert", "§ 114 Abs. 5 SchG"),
    ("Löschen spätestens 2 Jahre", "nach dem Ende des Schulbesuchs"),
    ("IBBW ist Verantwortlicher", "im Sinne der DSGVO"),
])
col = m.farben[5][1]
m.linie([(zx - 60, zy - 20), (zx - 60, zy - 80), (zx - 40, zy - 120), (zx + 40, zy - 120), (zx + 60, zy - 80),
         (zx + 60, zy - 20)], col, 3)
m.rect(zx - 100, zy - 20, 200, 150, "#a7f3d0", col, 2.5)
m.ell(zx, zy + 40, 14, "#ffffff", col, 2)
m.rect(zx - 5, zy + 50, 10, 40, "#ffffff", col, 1.5)

m.legende("Stand 13.11.2026\ngeprüft an § 114 SchG\ngestrichelt: mein Ansatz")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
