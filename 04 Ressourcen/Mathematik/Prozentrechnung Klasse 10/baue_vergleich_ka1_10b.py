#!/usr/bin/env python3
"""Vergleich: KA-Vorschlag (links, Original als Bildausschnitt) und Übungsklassenarbeit (rechts), Aufgabe für Aufgabe.
Framework-Python 3.12 (Pillow). Original-PDF: ~/Downloads/KA1-Prozent und Wahrscheinlichkeit.pdf"""
import base64
import io
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

import baue_uebung_ka1_10b as u

HIER = Path(__file__).resolve().parent
ZIEL = HIER / "Mathe 10b – Vergleich Original und Übungsklassenarbeit.html"
PDF = Path.home() / "Downloads" / "KA1-Prozent und Wahrscheinlichkeit.pdf"
S = 1.5  # 150 dpi
REG = {1: (1, 295, 592), 2: (1, 592, 945), 3: (1, 945, 1169), 4: (2, 262, 618), 5: (2, 618, 1150), 6: (3, 100, 470), 7: (3, 555, 860)}


def original_bilder():
    out = {}
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "150", "-png", str(PDF), f"{d}/o"], check=True)
        for k, (p, a, b) in REG.items():
            im = Image.open(f"{d}/o-{p}.png")
            c = im.crop((int(70 * S), int(a * S), int(755 * S), min(im.size[1], int(b * S)))).convert("L")
            buf = io.BytesIO()
            c.save(buf, "PNG", optimize=True)
            out[k] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return out


def aufgaben(l):
    """Nr. -> HTML-Fragment der Übungs-KA (von Balken zu Balken)."""
    res = {}
    for s in u.SEITEN:
        teile = re.split(r'(?=<div class="balken">)', s(l))[1:]
        for t in teile:
            nr = int(re.search(r"Nr\. (\d)", t).group(1))
            res[nr] = re.sub(r'<div class="teil">.*?</div>', "", t)
    return res


# (Original-Aufgabe oder None, Übungs-Nr., Gleich, Anders)
PAARE = [
    (1, 1, "Mehrstufiges Zufallsexperiment ohne Taschenrechner, Wahrscheinlichkeiten als Bruch, Pfadregel.",
     "Münze statt Glücksrad: dreimal werfen, Pfade zählen, Gegenereignis „mindestens einmal“. Keine Augensumme."),
    (2, 2, "Baumdiagramm lesen und mit Wahrscheinlichkeiten arbeiten, Ziehen ohne Zurücklegen (gleichzeitig).",
     "Baumdiagramm ergänzen statt Aussagen ankreuzen. Neue Kugelzahlen (3 rot, 5 grün). Fragen: unterschiedliche Farben, mindestens eine rote."),
    (3, 3, "Prozentrechnung im Alltag ohne Taschenrechner.",
     "Grundwert gesucht (Preiserhöhung um 20 %) statt Prozentsatz, dazu zwei Rabatte hintereinander."),
    (4, 4, "Zinsen und Zinseszins, Zinssatz gesucht, wechselnde Zinssätze. Daten kommen aus einer Grafik.",
     "Kreisdiagramm statt Säulenbild: Betrag aufteilen (Prozent von), dann drei Anlagen mit eigener Frage (Endkapital, Zinssatz gesucht, wechselnde Zinssätze)."),
    (5, 5, "Prozentrechnung mit Prozentsatz, Prozentwert und Grundwert, Vergleich in Prozent.",
     "Tabelle mit Einwohnerzahlen statt zwei Kreisdiagrammen. Jede Stadt hat eine andere gesuchte Größe. d) Absolut und prozentual unterscheiden."),
    (6, 6, "Zweifaches Zufallsexperiment mit mehreren Ausgängen, Wahrscheinlichkeiten mit Zurücklegen.",
     "Glücksrad mit ungleich großen Sektoren (Mittelpunktswinkel) statt Playlist. Fragen: gleiche Farbe, mindestens einmal grün."),
    (7, 7, "Erwartungswert berechnen, Spiel fair machen, einen Gewinnwert ändern.",
     "Würfelspiel mit zwei Würfeln statt Tombola, mit Einsatz: E = Summe aus Wahrscheinlichkeit · Gewinn, minus Einsatz. c) Veranstalter will 0,25 € verdienen."),
    (None, 8, "Nichts, die Aufgabe ist zusätzlich.",
     "Zweiter Erwartungswert mit Einsatz, verbunden mit Ziehen ohne Zurücklegen (Wahrscheinlichkeiten aus dem Baum). b) Einsatz für ein faires Spiel, c) Aussage über 100 Spiele prüfen."),
]

CSS = """<style>
body{background:#e9ecf0;padding-bottom:20mm}
.leiste{position:sticky;top:0;z-index:5;background:#1b1b1b;color:#fff;padding:10px 18px;font-size:14px;display:flex;gap:18px;align-items:center}
.leiste button{font:inherit;padding:4px 12px;border-radius:6px;border:0;cursor:pointer}
.kopfzeile,.paar{width:min(1500px,96vw);margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:6mm}
.kopfzeile{margin-top:8mm;font:700 17px Arial;color:#1b1b1b}.kopfzeile div{padding:2mm 3mm;background:#d4d9e0;border-radius:4px}
.paar{margin-top:8mm}
.zelle{background:#fff;padding:6mm 7mm;box-shadow:0 2px 10px rgba(0,0,0,.12);overflow:hidden;min-width:0}
.zelle img{width:100%;display:block}
.zelle .leer{color:#777;font-style:italic;padding:12mm 0;text-align:center}
.titel{grid-column:1/-1;font:700 15px Arial;color:#1b1b1b;margin:0}
.notiz{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font:13.5px/1.45 Arial;color:#1b1b1b}
.notiz div{background:#fff;border-left:4px solid #888;padding:2mm 4mm}.notiz .g{border-color:#2a8a4a}.notiz .a{border-color:#E6007E}
body:not(.zeige) .lsg,body:not(.zeige) .pkt,body:not(.zeige) .loesmark{display:none}
body:not(.zeige) .kast{color:transparent}
.zelle .balken{margin-top:0}
</style>"""


def main():
    orig = original_bilder()
    uf = aufgaben(True)
    zeilen = []
    for o, n, gleich, anders in PAARE:
        links = f'<img src="{orig[o]}" alt="Original Aufgabe {o}">' if o else '<div class="leer">kein Gegenstück im Original</div>'
        titel = f"Original Aufgabe {o} ↔ Übung Nr. {n}" if o else f"Nur in der Übung: Nr. {n}"
        zeilen.append(f'<div class="paar"><p class="titel">{titel}</p><div class="zelle">{links}</div><div class="zelle">{uf[n]}</div>'
                      f'<div class="notiz"><div class="g"><b>Gleich:</b> {gleich}</div><div class="a"><b>Anders:</b> {anders}</div></div></div>')
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Mathe 10b – Vergleich Original und Übungsklassenarbeit</title>' + u.ka.CSS + u.EXTRA + CSS + '</head><body>'
            '<div class="leiste"><b>Original und Übungsklassenarbeit, Aufgabe für Aufgabe</b>'
            '<button onclick="document.body.classList.toggle(\'zeige\')">Lösungen der Übung ein/aus</button></div>'
            '<div class="kopfzeile"><div>Original (KA-Vorschlag, 20 P)</div><div>Übungsklassenarbeit (38 P)</div></div>'
            + "".join(zeilen) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name, len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
