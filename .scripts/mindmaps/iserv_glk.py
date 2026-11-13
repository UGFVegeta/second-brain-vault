#!/usr/bin/env python3
"""Mindmap „IServ: Ablage und Links“ für Oskars GLK-Beitrag am 25.11.2026.
Quelle: Oskars Diktat vom 13.11.2026; Speicherstand aus der WebDAV-Anzeige auf Oskars Mac (13.11.2026).
Gestrichelt: Claudes Vorschläge, noch nicht abgestimmt. Keine Personennamen."""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "03 Bereiche/Schule & Unterricht/GLK 25.11.2026 – IServ Mindmap.excalidraw"
GRAU = "#475569"

m = Mindmap("IServ:\nablegen und\nverlinken")

# 1 Ausgangslage: Füllstandsbalken
zx, zy = m.ast(0, "1  Ausgangslage:\nSpeicher knapp", [
    ("Server zu 92 % voll", "785 GB gesamt, noch etwa 69 GB frei"),
    ("Rund 70 Lehrkräfte und alle Klassen", "jede zusätzliche Kopie zählt"),
    ("Unterrichtsmaterial auf IServ bleibt", "das ist in Ordnung"),
    ("Videos verlinken statt hochladen", "die größten Platzfresser", True),
])
col = m.farben[0][1]
m.rect(zx - 170, zy - 30, 340, 60, "#ffffff", col, 2)
m.rect(zx - 170, zy - 30, 313, 60, "#fecaca", "#dc2626", 1.5)
m.text(zx - 40, zy - 13, "92 %", 26, "#dc2626", w=80)
m.text(zx - 170, zy + 45, "0", 14, GRAU, w=20)
m.text(zx + 110, zy + 45, "785 GB", 14, GRAU, w=60)
m.text(zx - 120, zy - 90, "Füllstand am 13.11.", 16, col, w=240)

# 2 Grundregel: eine Datei, viele Links
zx, zy = m.ast(1, "2  Grundregel: einmal\nablegen, dann verlinken", [
    ("Keine Dateien und Bilder in Chats", "müllt zu, später nichts mehr auffindbar"),
    ("Keine Anhänge per Mail an viele", "20 Empfänger heißt 20 Kopien"),
    ("Die Datei liegt einmal im Ordner", "im Chat oder in der Mail steht nur der Link"),
    ("Ordner nicht umbenennen oder verschieben", "sonst gehen die Links ins Leere", True),
])
col = m.farben[1][1]
m.linie([(zx - 150, zy - 60), (zx - 90, zy - 60), (zx - 70, zy - 40), (zx - 70, zy + 60),
         (zx - 150, zy + 60), (zx - 150, zy - 60)], col, 2, fill="#ffedd5")
m.text(zx - 140, zy - 10, "Datei", 16, col, w=60)
for k, y in enumerate((zy - 110, zy, zy + 110)):
    m.ell(zx + 110, y, 28, "#ffffff", col, 2)
    m.text(zx + 95, y - 10, "Link", 14, col, w=34)
    m.pfeil([(zx - 64, zy + (k - 1) * 40), (zx + 78, y)], col, 1.5)

# 3 Für Schüler: Klassenordner als Baum
zx, zy = m.ast(2, "3  Für Schüler:\nder Klassenordner", [
    ("Einmal Zugriff auf die Klassengruppe holen", ""),
    ("Fachordner anlegen", "zum Beispiel 7c / Mathematik"),
    ("Alles an einem Ort", "die Klasse findet jedes Fach im selben Ordner"),
    ("Schreibrechte prüfen", "können Schüler Dateien löschen?", True),
])
col = m.farben[2][1]
m.rect(zx - 60, zy - 150, 120, 50, "#fef3c7", col, 2)
m.text(zx - 18, zy - 136, "7c", 20, col, w=36)
for k, fach in enumerate(("Mathematik", "Physik", "Deutsch")):
    y = zy - 40 + k * 80
    m.rect(zx - 40, y, 190, 46, "#ffffff", col, 1.5)
    m.text(zx - 30, y + 13, fach, 16, col, w=170)
    m.linie([(zx - 100, zy - 100), (zx - 100, y + 23), (zx - 40, y + 23)], col, 1.5)
m.linie([(zx - 60, zy - 125), (zx - 100, zy - 125), (zx - 100, zy - 100)], col, 1.5)

# 4 Link teilen: Adresszeile → Chat
zx, zy = m.ast(3, "4  Link teilen:\nzwei Wege", [
    ("Ordner-Link", "Ordner in IServ öffnen, Adresszeile kopieren"),
    ("Datei-Link", "Datei im Browser öffnen, Adresszeile kopieren"),
    ("In den Chat einfügen", "wird zum Link, ein Klick öffnet Ordner oder Datei"),
    ("Wirkt nur bei Zugriff", "der Link ersetzt keine Rechte"),
])
col = m.farben[3][1]
m.rect(zx - 180, zy - 130, 360, 50, "#ffffff", col, 2)
m.text(zx - 165, zy - 116, "https://…/iserv/file/…", 16, col, w=300)
m.pfeil([(zx, zy - 74), (zx, zy - 6)], col, 2)
m.text(zx + 12, zy - 56, "kopieren", 14, GRAU, w=80)
m.ell(zx, zy + 60, 0, "#fee2e2", col, 2, rx=150, ry=55)
m.text(zx - 120, zy + 48, "Klassenchat: Link", 18, col, "center", w=240)

# 5 Für Kollegen: Fachschaftsordner, drei Kollegen greifen auf einen Ordner zu
zx, zy = m.ast(4, "5  Für Kollegen:\nder Fachschaftsordner", [
    ("Fachschaft Mathematik / Klasse 10", "zum Beispiel Klassenarbeiten für die Parallelklassen"),
    ("Kein Versand mehr per Mail oder Chat", "alle wissen, wo es liegt"),
    ("Bei Bedarf Link in den Fachschaftschat", ""),
    ("Am Schuljahresende aufräumen", "alte Klassenordner, doppelte Dateien", True),
])
col = m.farben[4][1]
m.rect(zx - 80, zy - 40, 160, 90, "#ede9fe", col, 2)
m.text(zx - 70, zy - 10, "Fachschaft", 18, col, "center", w=140)
for x, y in ((zx - 140, zy - 140), (zx, zy - 150), (zx + 140, zy - 140)):
    m.ell(x, y, 22, "#c4b5fd", col, 1.5)
    m.pfeil([(x + (20 if x < zx else -20 if x > zx else 0), y + 24), (zx + (x - zx) // 3, zy - 46)], col, 1.5)
m.text(zx - 110, zy + 80, "einmal ablegen,\nalle finden es", 15, col, "center", w=220)

# 6 WebDAV: Laptop mit Laufwerk
zx, zy = m.ast(5, "6  IServ im Finder\nund Explorer (WebDAV)", [
    ("Adresse", "https://webdav.gdrs.schorndorf.de"),
    ("Mac: Finder, Gehe zu, Mit Server verbinden", ""),
    ("Windows: Explorer, Netzlaufwerk verbinden", ""),
    ("Einmal einrichten, dann wie ein Laufwerk", "etwas langsamer als lokale Dateien"),
    ("Kurzanleitung mit Bildern nach der GLK", "liegt dann selbst in IServ", True),
])
col = m.farben[5][1]
m.rect(zx - 130, zy - 110, 260, 160, "#ffffff", col, 2)
m.linie([(zx - 170, zy + 50), (zx + 170, zy + 50), (zx + 145, zy + 80), (zx - 145, zy + 80),
         (zx - 170, zy + 50)], col, 2, fill="#a7f3d0")
m.rect(zx - 90, zy - 75, 180, 90, "#d1fae5", col, 1.5)
m.text(zx - 80, zy - 45, "IServ-Laufwerk", 16, col, "center", w=160)

m.legende("Stand 13.11.2026\ndurchgezogen: vereinbart\ngestrichelt: Vorschlag")

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
m.speichern(ziel)
if len(sys.argv) > 2:
    m.vorschau(sys.argv[2])
