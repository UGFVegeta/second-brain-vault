#!/usr/bin/env python3
"""Baut aus einem Grundlagen-Check-Ergebnis eine Schnipsel-Seite zum Ausschneiden:
ein kleiner Zettel pro Nummer mit Gesamtergebnis, Themenblöcken und dem
Selbsteinschätzung-Vergleich - zum direkten Aushändigen an die Schüler.

Layout: 2 Spalten x 5 Zeilen pro A4-Seite (10 Zettel), gepunktete Schnittlinien.
Einmal senkrecht (zwischen den Spalten) und viermal waagrecht (zwischen den
Zeilen) schneiden, dann liegt pro Nummer ein Schnipsel vor.

Aufruf:
  python3 .scripts/grundlagen_check_schnipsel.py <ergebnisse.json> <ausgabe-ordner>

Erzeugt eine HTML-Datei; PDF-Export separat über Headless-Chrome
(--print-to-pdf), siehe Workflow-Doku.
"""
import html
import json
import sys
from pathlib import Path

from grundlagen_check_schluessel import TESTS
from grundlagen_check_bericht import werte_nummer_aus, block_quote, aufgabe_status
from grundlagen_check_verlauf import gesamt_quote
from grundlagen_check_praesentation import status_farbe, FARBE_OFFEN

PRO_SEITE = 10  # 2 Spalten x 5 Zeilen


def kurzname(block: str) -> str:
    """'A · Grundrechenarten und Rechenregeln' -> 'A'"""
    return block.split(" ", 1)[0]


def selbst_zeile(nummer, ergebnisse, selbsteinschaetzung, schluessel):
    """('3 von 8 sicher gefühlt, aber falsch', hat_daten) - None-Text wenn keine
    Selbsteinschaetzungs-Daten fuer diese Nummer vorliegen."""
    einschaetzung = selbsteinschaetzung.get(nummer)
    if not einschaetzung:
        return None
    antworten = ergebnisse.get(nummer, {})
    sicher_gesamt = 0
    sicher_falsch = 0
    for aufgaben in schluessel.values():
        for aufgabe, teile in aufgaben.items():
            if einschaetzung.get(aufgabe) != "sicher":
                continue
            sicher_gesamt += 1
            if aufgabe_status(antworten.get(aufgabe), teile) == "falsch":
                sicher_falsch += 1
    if sicher_gesamt == 0:
        return None
    return sicher_falsch, sicher_gesamt


VORLAGE = """<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<title>Grundlagen-Check – Schnipsel</title>
<style>
  @page {{ size: A4; margin: 8mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; margin: 0; color: #111; }}
  .seite {{
    display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(5, 1fr);
    width: 100%; height: 281mm; page-break-after: always;
  }}
  .seite:last-child {{ page-break-after: auto; }}
  .zettel {{
    border: 1px dashed #999; padding: 3mm 4mm; display: flex; flex-direction: column;
    justify-content: center; position: relative; overflow: hidden;
  }}
  .zettel.leer {{ border-style: dashed; }}
  .kopf {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.5mm; }}
  .nummer {{ font-size: 12pt; font-weight: 700; color: #333; }}
  .titel {{ font-size: 7.5pt; color: #999; }}
  .gesamt {{ font-size: 24pt; font-weight: 800; line-height: 1; margin: 1mm 0; }}
  .gesamt .label {{ font-size: 8pt; font-weight: 500; color: #888; margin-left: 1.5mm; }}
  .bloecke {{ display: flex; gap: 3mm; font-size: 8.5pt; margin: 1mm 0; }}
  .bloecke span {{ font-weight: 700; }}
  .selbst {{ font-size: 8pt; margin-top: 1mm; }}
  .selbst.warnung {{ color: {farbe_falsch}; font-weight: 600; }}
  .selbst.ok {{ color: #666; }}
  .fuss {{ font-size: 6.5pt; color: #aaa; margin-top: 1.5mm; }}
</style></head><body>
{seiten}
</body></html>
"""


def zettel_html(nummer, gesamt, bloecke, selbst):
    farbe = status_farbe(gesamt)
    gesamt_text = f'{gesamt*100:.0f}&#160;%' if gesamt is not None else '&#8212;'
    bloecke_html = "".join(
        f'<div>{html.escape(kurzname(b))}: <span style="color:{status_farbe(q)}">'
        f'{"&#8212;" if q is None else f"{q*100:.0f}%"}</span></div>'
        for b, q in bloecke
    )
    if selbst is None:
        selbst_html = ""
    else:
        falsch, gesamt_n = selbst
        if falsch == 0:
            selbst_html = (
                f'<div class="selbst ok">Bei „sicher gefühlt" ({gesamt_n}x) '
                f'immer richtig.</div>'
            )
        else:
            selbst_html = (
                f'<div class="selbst warnung">Sicher gefühlt, aber falsch: '
                f'{falsch} von {gesamt_n}.</div>'
            )
    return (
        f'<div class="zettel">'
        f'<div class="kopf"><span class="nummer">Nr. {html.escape(nummer)}</span>'
        f'<span class="titel">Grundlagen-Check</span></div>'
        f'<div class="gesamt" style="color:{farbe}">{gesamt_text}'
        f'<span class="label">gesamt</span></div>'
        f'<div class="bloecke">{bloecke_html}</div>'
        f'{selbst_html}'
        f'<div class="fuss">ohne Note &middot; nur zur eigenen Info</div>'
        f'</div>'
    )


def bauen(daten, ziel_ordner: Path):
    test = TESTS[daten["test"]]
    schluessel = test["schluessel"]
    ergebnisse = daten["ergebnisse"]
    selbsteinschaetzung = daten.get("selbsteinschaetzung", {})

    zettel = []
    for nummer in sorted(ergebnisse, key=int):
        antworten = ergebnisse[nummer]
        auswertung = werte_nummer_aus(antworten, schluessel)
        gesamt = gesamt_quote(auswertung)
        bloecke = [(b, block_quote(e)) for b, e in auswertung.items()]
        selbst = selbst_zeile(nummer, ergebnisse, selbsteinschaetzung, schluessel)
        zettel.append(zettel_html(nummer, gesamt, bloecke, selbst))

    seiten = []
    for i in range(0, len(zettel), PRO_SEITE):
        gruppe = zettel[i:i + PRO_SEITE]
        # Leerzellen auffuellen, damit die Schnittlinien auch auf der letzten
        # Seite ein sauberes 2x5-Raster ergeben.
        gruppe += ['<div class="zettel leer"></div>'] * (PRO_SEITE - len(gruppe))
        seiten.append(f'<div class="seite">{"".join(gruppe)}</div>')

    seite_html = VORLAGE.format(seiten="\n".join(seiten), farbe_falsch="#d03b3b")

    ziel_ordner.mkdir(parents=True, exist_ok=True)
    ziel = ziel_ordner / f"Schnipsel {test['name']}.html"
    ziel.write_text(seite_html, encoding="utf-8")
    return ziel


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    daten = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    ziel = bauen(daten, Path(sys.argv[2]))
    print(f"geschrieben: {ziel}")


if __name__ == "__main__":
    main()
