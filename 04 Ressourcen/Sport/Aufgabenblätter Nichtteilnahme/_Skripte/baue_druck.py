#!/usr/bin/env python3
"""Baut das Druckpaket: je Stufe eine Schülerdatei (Deckblatt 1x, dann jedes Blatt 5x hintereinander) und eine Lösungsdatei (mit Deckblatt, 1x).

Ablage: <Basis>/Druck/<Stufe>/ und gespiegelt in iCloud. Aufruf: python3 baue_druck.py
Alle Dateien haben gerade Seitenzahlen, damit beidseitiger Druck (lange Kante) nie eine Vorderseite auf die Rückseite des Vorgängers legt.
Neu bauen nach jeder Änderung an Blättern (erst baue_blaetter.py, dann dieses Skript).
"""
import shutil
import subprocess
import sys
from pathlib import Path

import baue_blaetter as bb

HIER = Path(__file__).resolve().parent
BASIS = HIER.parent
DRUCK = BASIS / "Druck"
ICLOUD_DRUCK = bb.ICLOUD / "Druck"
KOPIEN = 5
STUFEN = ["Klasse 5 und 6", "Klasse 7 und 8", "Klasse 9 und 10"]
THEMEN = ["Essen und Trinken", "Fair Play", "Herz, Puls und Ausdauer", "Training und Erholung",
          "Verletzungen vermeiden", "Regeln und Spielfeld"]
ACC = bb.ACC
LOE = bb.LOE

EXTRA_CSS = f"""
.deck {{ display:flex; flex-direction:column; height:100%; }}
.deck .top {{ display:flex; justify-content:space-between; align-items:flex-start; }}
.deck .top img {{ width: 42mm; }}
.deck .schule {{ font-size: 13pt; color:#555; margin-top:3mm; line-height:1.5; }}
.deck h1 {{ font-size: 42pt; line-height:1.1; color:{ACC}; margin: 30mm 0 4mm 0; }}
.deck h2.sub {{ font-size: 20pt; font-weight:600; margin:0 0 14mm 0; color:#333; border:none; padding:0; }}
.deck .stufe {{ display:inline-block; background:{ACC}; color:#fff; font-size: 28pt; font-weight:700; border-radius:3mm; padding:3mm 9mm; margin-bottom:16mm; }}
.deck .stufe.loe {{ background:{LOE}; }}
.deck .anl {{ border:2px solid {ACC}; border-radius:3mm; padding:8mm 10mm; font-size: 14.5pt; line-height:1.55; }}
.deck .anl.loe {{ border-color:{LOE}; }}
.deck .anl b.t {{ display:block; font-size: 16pt; color:{ACC}; margin-bottom:4mm; }}
.deck .anl.loe b.t {{ color:{LOE}; }}
.deck .anl ul {{ margin:0; padding-left:6mm; }}
.deck .anl li {{ margin-bottom:3mm; }}
.deck .leg {{ margin-top:12mm; font-size:14pt; color:#444; display:flex; gap:7mm; align-items:center; }}
.deck .fuss2 {{ margin-top:auto; font-size:10pt; color:#888; }}
.deck .nur {{ background:{LOE}; color:#fff; font-weight:700; font-size:20pt; letter-spacing:.06em; border-radius:2mm; padding:3mm 8mm; display:inline-block; margin-bottom:8mm; }}
.inh h2.t {{ font-size: 28pt; margin: 6mm 0 4mm 0; color:{ACC}; border:none; }}
.inh .raster {{ display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin-top:10mm; }}
.inh .th {{ border:1.5px solid #bcd0e6; border-radius:3mm; padding:6mm 8mm; }}
.inh .th.loe {{ border-color:#e8b5c8; }}
.inh .th b {{ display:block; color:{ACC}; font-size: 17pt; margin-bottom:3mm; }}
.inh .th.loe b {{ color:{LOE}; }}
.inh .th div {{ font-size: 14pt; line-height:1.9; display:flex; gap:3mm; }}
.inh .th div span {{ color:#777; min-width:4mm; }}
"""


def blatt_titel(stufe):
    """{thema: [(nr, titel)]} aus den vorhandenen PDF-Namen."""
    out = {}
    for th in THEMEN:
        liste = []
        for pdf in sorted((BASIS / stufe / th).glob("*.pdf")):
            if "(Lösung)" in pdf.name:
                continue
            nr, rest = pdf.stem.rsplit(" – ", 1)[0].rsplit(" ", 1)[1], pdf.stem.rsplit(" – ", 1)[1]
            liste.append((nr, rest))
        out[th] = liste
    return out


def deckblatt_html(stufe, loesung):
    kurz = stufe.replace("Klasse ", "Klasse ")
    cls = " loe" if loesung else ""
    logo = f'<img src="{bb.LOGO.as_uri()}">'
    if loesung:
        titel, sub = "Lösungen", "Aufgabenblätter für den Sportunterricht"
        kasten = ('<div class="anl loe"><b class="t">Hinweise für Lehrkräfte</b><ul>'
                  '<li>Jedes Lösungsblatt ist das Schülerblatt, mit den Antworten in Magenta ausgefüllt.</li>'
                  '<li>Bei Schreibaufgaben sind das Beispiele. Andere sinnvolle Antworten sind möglich.</li>'
                  '<li>Die Lösungen liegen nicht im Ordner für die Schüler, damit niemand abschreibt.</li>'
                  '<li>Am besten auf farbiges Papier drucken, dann verwechselt sie niemand mit den Schülerblättern.</li>'
                  '</ul></div>')
        nur = '<div class="nur">NUR FÜR LEHRKRÄFTE</div>'
    else:
        titel, sub = "Aufgabenblätter", "für den Sportunterricht, wenn du nicht mitmachen kannst"
        kasten = ('<div class="anl"><b class="t">So funktioniert es</b><ul>'
                  '<li>Wer wegen Verletzung oder Krankheit anwesend ist, aber nicht mitmachen kann, nimmt sich ein Blatt aus diesem Ordner.</li>'
                  '<li>Ein Blatt beschäftigt etwa eine Doppelstunde. Es muss nicht alles geschafft werden, die Aufgaben mit ○ kommen zuerst.</li>'
                  '<li>Alle nötigen Informationen stehen auf dem Blatt. Handy und Internet sind nicht nötig, ein eigener Stift schon.</li>'
                  '<li>Das Blatt wird am Ende der Stunde abgegeben. Es gibt keine Note.</li>'
                  '<li>Wer länger ausfällt, nimmt jedes Mal ein anderes Blatt.</li>'
                  '</ul></div>')
        nur = ""
    vorn = (f'<div class="deck"><div class="top"><div><div class="schule"><b>Gottlieb-Daimler-Realschule Schorndorf</b><br>'
            f'Fachschaft Sport, Schuljahr 2026/27</div></div>{logo}</div>'
            f'<h1>{titel}</h1><h2 class="sub">{sub}</h2>{nur}<div class="stufe{cls}">{stufe}</div>{kasten}'
            f'<div class="leg"><span>Schwierigkeit:</span><span>{bb.kreis(0, 18)} leicht</span><span>{bb.kreis(1, 18)} mittel</span>'
            f'<span>{bb.kreis(2, 18)} schwer</span></div></div>')
    th = blatt_titel(stufe)
    boxen = "".join(
        f'<div class="th{cls}"><b>{t}</b>' + "".join(f'<div><span>{n}</span>{ti}</div>' for n, ti in th[t]) + '</div>'
        for t in THEMEN)
    hinten = (f'<div class="inh"><h2 class="t">Inhalt: {stufe}</h2>'
              f'<div style="color:#555;font-size:13pt">{"Lösungen zu allen Blättern, in dieser Reihenfolge." if loesung else "Alle Blätter liegen nach Themen geordnet im Ordner."}</div>'
              f'<div class="raster">{boxen}</div></div>')
    return bb.seite(vorn) + bb.seite(hinten)


def als_pdf(body, titel, ziel):
    tmp = HIER / "html"
    tmp.mkdir(exist_ok=True)
    h = tmp / f"{titel}.html"
    h.write_text(bb.html(body, titel).replace("</style>", EXTRA_CSS + "</style>", 1), encoding="utf-8")
    bb.pdf(h, ziel)


def seiten(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int([z for z in out.splitlines() if z.startswith("Pages:")][0].split()[1])


def verbinde(quellen, ziel):
    subprocess.run(["qpdf", "--empty", "--pages", *[str(q) for q in quellen], "--", str(ziel)], check=True)


def main():
    filt = sys.argv[1] if len(sys.argv) > 1 else ""
    DRUCK.mkdir(exist_ok=True)
    for stufe in STUFEN:
        if filt not in stufe:
            continue
        ziel = DRUCK / stufe
        ziel.mkdir(exist_ok=True)
        for alt in ziel.glob("*.pdf"):  # nur eigene, erzeugte Dateien der Vorläufe
            alt.unlink()
        einzel = ziel / "_Einzelteile"
        einzel.mkdir(exist_ok=True)
        blaetter, loesungen = [], []
        for th in THEMEN:
            for pdf in sorted((BASIS / stufe / th).glob("*.pdf")):
                (loesungen if "(Lösung)" in pdf.name else blaetter).append(pdf)
        assert len(blaetter) == len(loesungen), (stufe, len(blaetter), len(loesungen))
        for pdf in blaetter + loesungen:
            assert seiten(pdf) == 2, pdf
        deck = einzel / f"Deckblatt {stufe}.pdf"
        deckl = einzel / f"Deckblatt Lösungen {stufe}.pdf"
        als_pdf(deckblatt_html(stufe, False), f"Deckblatt {stufe}", deck)
        als_pdf(deckblatt_html(stufe, True), f"Deckblatt Lösungen {stufe}", deckl)
        schueler = ziel / f"1 Schülerblätter {stufe} (Deckblatt 1x, jedes Blatt {KOPIEN}x, einmal drucken).pdf"
        verbinde([deck] + [p for p in blaetter for _ in range(KOPIEN)], schueler)
        loes = ziel / f"2 Lösungen {stufe} (mit Deckblatt, 1x drucken, farbiges Papier).pdf"
        verbinde([deckl] + loesungen, loes)
        n_s, n_l, n_d = seiten(schueler), seiten(loes), seiten(deck)
        assert n_d == 2 and n_s == 2 + 2 * KOPIEN * len(blaetter) and n_l == 2 + 2 * len(loesungen)
        print(f"{stufe}: {len(blaetter)} Blätter, Schülerdatei {n_s} Seiten ({n_s // 2} Blatt), "
              f"Lösungen {n_l} Seiten, {schueler.stat().st_size // 1024} KB")
    if bb.ICLOUD.exists():
        ICLOUD_DRUCK.mkdir(parents=True, exist_ok=True)
        for st in STUFEN:
            if filt in st:
                for alt in (ICLOUD_DRUCK / st).glob("*.pdf"):
                    alt.unlink()
        shutil.copytree(DRUCK, ICLOUD_DRUCK, dirs_exist_ok=True)
        print("iCloud:", ICLOUD_DRUCK)


if __name__ == "__main__":
    main()
