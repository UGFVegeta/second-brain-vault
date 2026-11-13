#!/usr/bin/env python3
"""Mindmap „Schularten und Übergänge“ (Grundschule, Werkrealschule, Realschule, Übergang 4→5, MVO, Förderung).
Quellen: Notiz „Schularten, Übergänge und Landesprogramme“ (13.11.2026), Rechtsquellen im Vault. Keine Personennamen."""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "03 Bereiche/Führung & Schulentwicklung/Schularten und Übergänge – Mindmap.excalidraw"
GRAU = "#475569"

m = Mindmap("Schularten\nund Übergänge")

# 1 Grundschule: Treppe Juniorklasse → Klasse 4
zx, zy = m.ast(0, "1  Grundschule\nKlasse 1 bis 4", [
    ("Juniorklassen seit 2026/27", "ein Jahr vor Klasse 1, § 5b SchG"),
    ("Sprachfördergruppen vor der Einschulung", "Pflicht bei Bedarf, § 5c SchG"),
    ("Versetzung ab Klasse 2 nach 3", "Klasse 1 nach 2 ohne Entscheidung"),
    ("Ganztagsanspruch seit 2026/27", "für Klasse 1, wächst auf, § 8c SchG"),
])
col = m.farben[0][1]
for k, lab in enumerate(("J", "1", "2", "3", "4")):
    x, y = zx - 190 + k * 76, zy + 100 - k * 45
    m.rect(x, y, 70, 100 + k * 45 - 60, "#ffffff" if k else "#dbeafe", col, 1.5)
    m.text(x + 27, y + 8, lab, 20, col, w=16)
m.text(zx - 190, zy + 150, "J = Juniorklasse", 14, GRAU, w=200)

# 2 Übergang 4 → 5: drei Wege zum Gymnasium
zx, zy = m.ast(1, "2  Übergang von\nKlasse 4 nach 5", [
    ("Empfehlung G, M oder E", "Klassenkonferenz, Vorsitz Schulleitung"),
    ("Richtwerte Deutsch und Mathe", "E ab 2,5 (keins über 3,0); M ab 3,0"),
    ("Kompass 4", "zentrale Messung, zählt nicht fürs Zeugnis"),
    ("Gymnasium: eines von dreien reicht", "Empfehlung E, Kompass 4 oder Potenzialtest"),
    ("Werkreal-, Realschule, GMS", "die Eltern entscheiden frei"),
])
col = m.farben[1][1]
for k, lab in enumerate(("Empfehlung", "Kompass 4", "Potenzial-\ntest")):
    y = zy - 150 + k * 95
    m.rect(zx - 190, y, 150, 64, "#ffffff", col, 1.5)
    m.text(zx - 182, y + 32 - (18 if "\n" in lab else 9), lab, 15, col, "center", w=134)
    m.pfeil([(zx - 38, y + 32), (zx + 52, zy - 55)], col, 1.5)
m.rect(zx + 55, zy - 90, 140, 70, "#ffedd5", col, 2)
m.text(zx + 62, zy - 66, "Gymnasium", 16, col, "center", w=126)
m.text(zx + 40, zy + 20, "eins reicht", 15, col, "center", w=170)

# 3 Werkrealschule: sinkende Säulen
zx, zy = m.ast(2, "3  Werkrealschule\nKlasse 5 bis 9 oder 10", [
    ("Hauptschulabschluss nach 9 oder 10", "§ 6 Abs. 2 SchG"),
    ("Werkrealschulabschluss läuft aus", "letzter Jahrgang Klasse 5 in 2024/25"),
    ("Unter 16 in Klasse 5", "regionale Schulentwicklung, § 30b SchG"),
    ("Rems-Murr: nur noch drei", "eine davon in Rudersberg"),
])
col = m.farben[2][1]
for k, h in enumerate((200, 160, 120, 80, 46)):
    m.rect(zx - 170 + k * 70, zy + 110 - h, 50, h, "#fef3c7", col, 1.5)
m.linie([(zx - 190, zy + 110), (zx + 190, zy + 110)], GRAU, 1.5)
m.pfeil([(zx - 150, zy - 140), (zx + 160, zy + 10)], "#dc2626", 2, style="dashed")
m.text(zx - 150, zy + 125, "Anmeldungen sinken", 15, col, w=200)

# 4 Realschule: Gabelung nach Klasse 5
zx, zy = m.ast(3, "4  Realschule\nKlasse 5 bis 10", [
    ("Klasse 5: Orientierungsstufe", "bewertet wird auf Niveau M"),
    ("Ende Klasse 5: M oder G", "nach den Versetzungsanforderungen"),
    ("M: Realschulabschluss nach 10", "G: Hauptschulabschluss nach 9"),
    ("Im Verbund mit Werkrealschule nur M", "wer auf G wechselt, geht in die WRS"),
])
col = m.farben[3][1]
m.rect(zx - 190, zy - 30, 110, 60, "#fee2e2", col, 2)
m.text(zx - 180, zy - 10, "Klasse 5", 16, col, "center", w=90)
m.pfeil([(zx - 78, zy - 10), (zx + 40, zy - 100)], col, 2)
m.pfeil([(zx - 78, zy + 10), (zx + 40, zy + 100)], col, 2)
m.rect(zx + 45, zy - 140, 145, 70, "#ffffff", col, 2)
m.text(zx + 52, zy - 124, "Niveau M\nbis Kl. 10", 15, col, "center", w=131)
m.rect(zx + 45, zy + 70, 145, 70, "#ffffff", col, 1.5, style="dashed")
m.text(zx + 52, zy + 86, "Niveau G\nim Verbund: WRS", 14, col, "center", w=131)

# 5 Wechsel zwischen Schularten: Leiter mit drei Ebenen
zx, zy = m.ast(4, "5  Wechsel zwischen\nSchularten (MVO)", [
    ("Drei Ebenen", "G: WRS, RS, GMS; M: RS, GMS; E: Gym, GMS"),
    ("Zum Halbjahr oder Schuljahresende", "Klasse 5 nur zum Schuljahresende"),
    ("In Klasse 9 und 10 nur zum Schuljahresbeginn", "Abschlussklassen, § 2 MVO"),
    ("Realschule G nach M", "D, M, Fremdsprache gut; Schnitt 3,0"),
])
col = m.farben[4][1]
m.linie([(zx - 120, zy + 150), (zx - 120, zy - 150)], col, 2.5)
m.linie([(zx + 20, zy + 150), (zx + 20, zy - 150)], col, 2.5)
for k, lab in enumerate(("G", "M", "E")):
    y = zy + 100 - k * 100
    m.linie([(zx - 120, y), (zx + 20, y)], col, 2.5)
    m.text(zx + 40, y - 14, lab, 24, col, w=20)
m.pfeil([(zx + 110, zy + 90), (zx + 110, zy - 90)], col, 1.5)
m.pfeil([(zx + 150, zy - 90), (zx + 150, zy + 90)], col, 1.5)
m.text(zx + 90, zy + 115, "hoch\nund runter", 13, GRAU, "center", w=90)

# 6 Förderung: Netz um das Kind
zx, zy = m.ast(5, "6  Förderung", [
    ("SprachFit und Juniorklassen", "Sprachförderung von Kita bis Grundschule"),
    ("Startchancen 2024 bis 2034", "rund 540 Schulen in BW; Geld und Personal"),
    ("Rückenwind und Starke BASIS!", "Deutsch und Mathe, Klasse 1 bis 8"),
    ("LRS, Rechenschwäche, Nachteilsausgleich", "VwV besonderer Förderbedarf"),
    ("Inklusion", "SBBZ und Sonderpädagogischer Dienst"),
])
col = m.farben[5][1]
m.ell(zx, zy, 34, "#a7f3d0", col, 2)
m.text(zx - 26, zy - 9, "Kind", 15, col, "center", w=52)
for k, (dx, dy, lab) in enumerate(((-130, -130, "Sprache"), (130, -130, "Lesen,\nRechnen"),
                                   (-140, 120, "Personal"), (140, 120, "Inklusion"))):
    m.ell(zx + dx, zy + dy, 0, "#ffffff", col, 1.5, rx=62, ry=34)
    m.text(zx + dx - 55, zy + dy - (18 if "\n" in lab else 9), lab, 14, col, "center", w=110)
    m.pfeil([(zx + dx * 0.55, zy + dy * 0.55), (zx + dx * 0.3, zy + dy * 0.3)], col, 1.5)

m.legende("Stand 13.11.2026\nRecht geprüft am Vault-Text\nRS = Realschule")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
