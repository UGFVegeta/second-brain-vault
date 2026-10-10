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
    (1, 1, "Glücksrad mit gleich großen Feldern, zweimal drehen, a) zweimal dieselbe Farbe, b) Summe der Zahlen.",
     "6 statt 4 Felder, Summe 7 statt 10, Farben schwarz/grau/weiß."),
    (2, 2, "Baumdiagramm lesen, Aussagen ankreuzen, auch falsche rechnerisch begründen. Falle mit dem Prozentzeichen.",
     "3 weiße und 7 schwarze Kugeln, 4 Aussagen mit eigenen Zahlen; die Aussage „gleichzeitig gezogen“ fehlt."),
    (3, 3, "a) Preissenkung in Prozent aus altem und neuem Preis.",
     "120 € auf 90 €. Dazu neu b): zwei Rabatte hintereinander (25 % und 20 %), die man nicht addieren darf."),
    (4, 4, "Feste Zinssätze für 3 Jahre, Zinssatz fürs 4. Jahr gesucht, gleichbleibender Zinssatz mit demselben Endkapital. Säulenbild.",
     "8 000 € statt 5 000 €, Sätze 0,8 / 1,2 / 1,6 %. Zusätzlich a) Kapital nach 3 Jahren als Zwischenschritt."),
    (None, 5, "Nichts, die Aufgabe ist zusätzlich.",
     "Zwei Bankangebote vergleichen (wechselnde Sätze gegen gleichbleibender Satz mit Bonus). Übt das Multiplizieren der Zinsfaktoren, Vorbild Nachtermin 2015 P6."),
    (5, 6, "Zwei Kreisdiagramme, Prozent von Prozent, Anteil an der Gesamtmenge in Prozent.",
     "Altersgruppen einer Stadt statt Erdoberfläche; rechnet mit Einwohnerzahlen, nicht mit km². Ohne die falsche Prozentsumme des Originals."),
    (6, 7, "Zwei Züge nacheinander aus Kategorien, „Hälfte davon“, mit Zurücklegen, Gegenereignis „keiner“, „genau einer“.",
     "Lern-App statt Playlist. Zusätzlich a) und b) ohne Zurücklegen (Original nur mit Zurücklegen)."),
    (7, 8, "Tombola, Erwartungswert, Spiel fair machen durch Änderung eines Gewinnwerts.",
     "600 Lose, 1,50 € Einsatz, andere Gewinne. c) neu: Hauptgewinn so ändern, dass der Veranstalter 0,50 € pro Los verdient."),
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
            '<div class="kopfzeile"><div>Original (KA-Vorschlag, 20 P)</div><div>Übungsklassenarbeit (36 P)</div></div>'
            + "".join(zeilen) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name, len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
