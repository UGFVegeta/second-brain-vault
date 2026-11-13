#!/usr/bin/env python3
"""Mindmap „Weg in die Schulleitung“.
Quellen: Schulleitung – Hub.md, Führung & Schulentwicklung.md (vier Säulen, multiprofessionelle Teams),
Active Recall/Schulleitung/Wissen (Verfahren, Schulrecht 02–09, Schulentwicklung, Schulzentrum Rudersberg).
Keine Personennamen. Stand 13.11.2026."""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "03 Bereiche/Führung & Schulentwicklung/Schulleitung – Mindmap.excalidraw"
GRAU = "#475569"

m = Mindmap("Weg in die\nSchulleitung")

# 1 Verfahren: vier Modul-Kacheln, C und D markiert
zx, zy = m.ast(0, "1  Das Verfahren\nvier Module", [
    ("A  Unterrichtsanalyse mit Beratung", "fremde Stunde, nicht affines Fach"),
    ("B  Strukturiertes Interview", "etwa 45 Min.; Schulspezifika der Ausschreibung"),
    ("C  Präsentation", "15 Min. Vorbereitung, etwa 10 Min. Vortrag"),
    ("D  Schwierige Alltagssituation", "Rollenspiel oder Fallanalyse"),
])
col = m.farben[0][1]
for k, b in enumerate("ABCD"):
    x, y = zx - 130 + (k % 2) * 140, zy - 120 + (k // 2) * 130
    rot = b in "CD"
    m.rect(x, y, 110, 100, "#fee2e2" if rot else "#ffffff", "#dc2626" if rot else col, 2)
    m.text(x + 43, y + 30, b, 32, "#dc2626" if rot else col, w=24)
m.text(zx - 135, zy + 145, "C und D: in Fellbach schwierig", 14, "#dc2626", w=270)

# 2 Schulrecht Schüler: Stufen von pädagogisch bis Ordnungsmaßnahme
zx, zy = m.ast(1, "2  Schulrecht:\nSchüler", [
    ("Erziehungs- und Ordnungsmaßnahmen", "§ 90 SchG: erst pädagogisch, verhältnismäßig"),
    ("Aufsichtspflicht", "nach Alter, Reife und Gefahrenquelle"),
    ("Noten und Versetzung", "NVO: höchstens eine KA am Tag, drei pro Woche"),
    ("Schulpflicht und Veranstaltungen", "Krankmeldung spätestens am zweiten Tag"),
])
col = m.farben[1][1]
x0, y0, st = zx - 170, zy + 110, 110
m.linie([(x0, y0), (x0 + st, y0), (x0 + st, y0 - 70), (x0 + 2 * st, y0 - 70), (x0 + 2 * st, y0 - 140),
         (x0 + 3 * st, y0 - 140), (x0 + 3 * st, y0), (x0, y0)], col, 2.5, fill="#ffedd5")
for k, lab in enumerate(("pädagogisch", "Nachsitzen", "Ordnungs-\nmaßnahme")):
    m.text(x0 + k * st + 6, y0 - 70 * k - 26 - (18 if "\n" in lab else 0), lab, 14, col, w=100)
m.text(zx - 60, zy - 150, "§ 90 SchG", 20, col, w=110)

# 3 Schulrecht Schule: wer beaufsichtigt, wer trägt
zx, zy = m.ast(2, "3  Schulrecht:\nSchule", [
    ("Konferenzen", "GLK: ganze Schule; beschlussfähig über die Hälfte"),
    ("Eltern und Datenschutz", "Erziehungsgemeinschaft; Pflegschaft je Halbjahr"),
    ("Leitung und Dienstrecht", "§ 41 SchG: Pläne, Hausrecht, Unterrichtsbesuche"),
    ("Schulträger und Schulaufsicht", "Gemeinde zahlt; Schulamt hat Fach- und Dienstaufsicht"),
])
col = m.farben[2][1]
for lab, x, y in (("Regierungs-\npräsidium", zx - 70, zy - 160), ("Schulamt", zx - 70, zy - 50),
                  ("Schule", zx - 70, zy + 60), ("Gemeinde", zx + 90, zy + 60)):
    m.rect(x - 60, y, 120, 54, "#ffffff", col, 1.5)
    zl = lab.split("\n")
    m.text(x - 55, y + 27 - len(zl) * 9, lab, 14, col, "center", w=110)
m.pfeil([(zx - 70, zy - 104), (zx - 70, zy - 56)], col, 1.5)
m.pfeil([(zx - 70, zy + 6), (zx - 70, zy + 54)], col, 1.5)
m.pfeil([(zx + 28, zy + 87), (zx - 4, zy + 87)], GRAU, 1.5, style="dashed")
m.text(zx + 70, zy + 122, "Schulträger", 13, GRAU, w=100)
m.text(zx + 5, zy - 100, "Aufsicht", 13, col, w=70)

# 4 Vier Säulen: Tempel
zx, zy = m.ast(3, "4  Meine vier Säulen", [
    ("Prozesssteuerung", "Vertretungsplanung, Poolstunden"),
    ("Datengestützte Qualitätsentwicklung", "Von Daten zu Taten, Modell Schildkamp"),
    ("Rechtssichere Administration", "§ 90 in sechs Schritten, Checkliste"),
    ("Digitale Konsolidierung, Profil", "Berufsorientierung, Kooperationen"),
])
col = m.farben[3][1]
m.linie([(zx - 170, zy - 80), (zx, zy - 150), (zx + 170, zy - 80), (zx - 170, zy - 80)], col, 2, fill="#fecaca")
for k in range(4):
    x = zx - 150 + k * 85
    m.rect(x, zy - 70, 44, 160, "#ffffff", col, 1.5)
    m.text(x + 16, zy - 2, str(k + 1), 18, col, w=12)
m.rect(zx - 180, zy + 95, 360, 24, "#fecaca", col, 2)

# 5 Schulentwicklung: drei Professionen, ein Ziel
zx, zy = m.ast(4, "5  Schulentwicklung", [
    ("Bildungsreform ab 2025/26", "Basiskompetenzen, neue Pflichtfächer"),
    ("Ganztag", "Anspruch in der Grundschule ab 2026/27"),
    ("Unterricht beraten", "kriteriengeleitet beobachten und beraten"),
    ("Multiprofessionelle Teams", "Lehrkraft, Sonderpädagogik, Schulsozialarbeit"),
])
col = m.farben[4][1]
m.ell(zx, zy, 0, "#ede9fe", col, 2, rx=80, ry=42)
m.text(zx - 60, zy - 18, "Ausbildungs-\nreife", 15, col, "center", w=120)
for x, y, lab in ((zx - 130, zy - 120, "Lehrkraft"), (zx + 130, zy - 120, "Sonder-\npädagogik"),
                  (zx, zy + 125, "Schul-\nsozialarbeit")):
    m.ell(x, y, 22, "#c4b5fd", col, 1.5)
    hoch = y > zy
    m.pfeil([(x + (0 if hoch else (24 if x < zx else -24)), y + (-26 if hoch else 18)),
             (zx + (0 if hoch else (-50 if x < zx else 50)), zy + (46 if hoch else -40))], col, 1.5)
    if hoch:
        m.text(x + 30, y - 18, lab, 13, col, w=110)
    else:
        m.text(x - 55, y + 26, lab, 13, col, "center", w=110)

# 6 Ziel und Zeitplan: Zeitstrahl
zx, zy = m.ast(5, "6  Ziel und Zeitplan", [
    ("Schulzentrum Rudersberg", "Verbund aus Grund-, Werkreal- und Realschule"),
    ("Themen vor Ort", "Werkrealschule sichern; Realschule nur Niveau M"),
    ("Schulrecht-Lernplan", "Wochen bis Februar 2027; Fälle mit Lösungen"),
    ("Module C und D üben ab 11.01.", "Ausschreibung frühestens Februar 2027", True),
])
col = m.farben[5][1]
ly = zy + 10
m.pfeil([(zx - 180, ly), (zx + 190, ly)], GRAU, 2)
for k, (x, oben, unten) in enumerate(((zx - 150, "jetzt", "Nov. 2026"), (zx + 10, "C und D", "Jan. 2027"),
                                      (zx + 150, "Aus-\nschreibung", "Feb. 2027"))):
    m.ell(x, ly, 9, col if k == 0 else "#ffffff", col, 2, style="solid" if k == 0 else "dashed")
    m.text(x - 50, ly - 30 - (18 if "\n" in oben else 0), oben, 14, col, "center", w=100)
    m.text(x - 50, ly + 18, unten, 13, GRAU, "center", w=100)

m.legende("Stand 13.11.2026\ndurchgezogen: erarbeitet\ngestrichelt: geplant")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
