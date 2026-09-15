#!/usr/bin/env python3
"""Führt über mehrere Grundlagen-Checks / Diagnosetests im Schuljahr Buch, je
Nummer, und zeigt die Entwicklung als kleines Diagramm - Grundlage für die
Diagnosegespräche.

Ein "Testlauf" ist ein einzelner Durchgang (z. B. "Grundlagen 5-6 Teil 1" im
September, ein Themencheck im November, ...). Jeder Testlauf liefert pro
Nummer eine Gesamt-Prozentzahl (über alle in diesem Testlauf ausgewerteten
Aufgaben), damit verschiedene Testläufe zu unterschiedlichen Themen trotzdem
in einer Zeitreihe vergleichbar bleiben.

Datenschutz: nur Nummern, wie bei grundlagen_check_bericht.py.

Ablauf:
  1. Nach jedem Testlauf grundlagen_check_bericht.py normal laufen lassen.
  2. Dann diesen Befehl, um den Testlauf in den Verlauf einzutragen:
     python3 .scripts/grundlagen_check_verlauf.py eintragen \\
         <ergebnisse.json> <verlauf.json> <"Test-Label"> <YYYY-MM-DD>
  3. Übersicht erzeugen:
     python3 .scripts/grundlagen_check_verlauf.py bauen <verlauf.json> <ausgabe-ordner>

verlauf.json wird angelegt, falls es noch nicht existiert, und sonst ergänzt.
Ein erneuter Eintrag mit demselben Test-Label + Datum ersetzt den alten
(sicher bei erneutem Lauf nach einer Korrektur).
"""
import json
import sys
from pathlib import Path

from grundlagen_check_schluessel import TESTS, schluessel_fuer_nummer
from grundlagen_check_bericht import werte_nummer_aus, block_quote


def gesamt_quote(auswertung):
    """Ein Prozentwert ueber alle Bloecke eines Testlaufs hinweg, damit
    unterschiedliche Testlaeufe (verschiedene Themen) vergleichbar bleiben."""
    bearbeitet = 0
    richtig = 0
    for eintraege in auswertung.values():
        for _, status in eintraege:
            if status == "offen":
                continue
            bearbeitet += 1
            if status == "richtig":
                richtig += 1
    if bearbeitet == 0:
        return None
    return richtig / bearbeitet


def lade_verlauf(pfad: Path):
    if pfad.exists():
        return json.loads(pfad.read_text(encoding="utf-8"))
    return {"verlauf": {}}


def eintragen(ergebnisse_pfad: Path, verlauf_pfad: Path, test_label: str, datum: str):
    daten = json.loads(ergebnisse_pfad.read_text(encoding="utf-8"))
    test = TESTS[daten["test"]]
    ergebnisse = daten["ergebnisse"]

    verlauf = lade_verlauf(verlauf_pfad)
    eintraege_gesamt = verlauf.setdefault("verlauf", {})

    aktualisiert = 0
    for nummer, antworten in ergebnisse.items():
        schluessel = schluessel_fuer_nummer(test, daten, nummer)
        auswertung = werte_nummer_aus(antworten, schluessel)
        quote = gesamt_quote(auswertung)
        bloecke = {b: block_quote(e) for b, e in auswertung.items()}

        liste = eintraege_gesamt.setdefault(nummer, [])
        # gleicher Testlauf (Label+Datum) wird ersetzt, nicht dupliziert
        liste[:] = [e for e in liste if not (e["test"] == test_label and e["datum"] == datum)]
        liste.append({
            "datum": datum,
            "test": test_label,
            "gesamt_prozent": None if quote is None else round(quote * 100),
            "bloecke": {b: (None if q is None else round(q * 100)) for b, q in bloecke.items()},
        })
        liste.sort(key=lambda e: e["datum"])
        aktualisiert += 1

    verlauf_pfad.parent.mkdir(parents=True, exist_ok=True)
    verlauf_pfad.write_text(json.dumps(verlauf, ensure_ascii=False, indent=1), encoding="utf-8")
    return aktualisiert


# --- Darstellung --------------------------------------------------------

def sparkline_svg(eintraege, breite=280, hoehe=70):
    """Kleines Liniendiagramm der Gesamt-Prozentzahl über die Zeit. Bei nur
    einem Eintrag ein einzelner Punkt mit Hinweistext statt einer Linie -
    eine Linie durch einen Punkt würde Entwicklung vortäuschen, die es
    noch nicht gibt."""
    punkte = [e for e in eintraege if e["gesamt_prozent"] is not None]
    rand = 8
    plot_w = breite - 2 * rand
    plot_h = hoehe - 2 * rand - 14  # Platz fuer Datumsbeschriftung unten

    if not punkte:
        return '<p style="font-size:9pt;color:#888;font-style:italic;">Noch keine auswertbaren Daten.</p>'

    if len(punkte) == 1:
        p = punkte[0]
        return (
            f'<svg viewBox="0 0 {breite} {hoehe}" width="{breite}" height="{hoehe}">'
            f'<circle cx="{rand+6}" cy="{rand + plot_h/2:.0f}" r="4" fill="#2a78d6"/>'
            f'<text x="{rand+16}" y="{rand + plot_h/2 + 4:.0f}" font-size="11" fill="#111">'
            f'{p["gesamt_prozent"]}&#160;% ({html_escape(p["test"])})</text>'
            f'<text x="{rand}" y="{hoehe-3}" font-size="8" fill="#888">{p["datum"]} · '
            f'weitere Punkte folgen mit dem nächsten Test</text>'
            f'</svg>'
        )

    xs = [rand + i * (plot_w / (len(punkte) - 1)) for i in range(len(punkte))]
    ys = [rand + plot_h - (p["gesamt_prozent"] / 100) * plot_h for p in punkte]
    pfad = " ".join(f'{"M" if i == 0 else "L"}{x:.1f},{y:.1f}' for i, (x, y) in enumerate(zip(xs, ys)))

    punkte_svg = []
    for i, (x, y, p) in enumerate(zip(xs, ys, punkte)):
        punkte_svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#2a78d6">'
            f'<title>{p["datum"]} · {html_escape(p["test"])}: {p["gesamt_prozent"]}%</title></circle>'
        )
        if i == 0 or i == len(punkte) - 1:
            punkte_svg.append(
                f'<text x="{x:.1f}" y="{y-7:.1f}" font-size="9" text-anchor="middle" '
                f'fill="#111" font-weight="600">{p["gesamt_prozent"]}%</text>'
            )

    return (
        f'<svg viewBox="0 0 {breite} {hoehe}" width="{breite}" height="{hoehe}">'
        f'<path d="{pfad}" fill="none" stroke="#2a78d6" stroke-width="2" stroke-linecap="round"/>'
        f'{"".join(punkte_svg)}'
        f'<text x="{xs[0]:.1f}" y="{hoehe-3}" font-size="8" fill="#888" text-anchor="start">{punkte[0]["datum"]}</text>'
        f'<text x="{xs[-1]:.1f}" y="{hoehe-3}" font-size="8" fill="#888" text-anchor="end">{punkte[-1]["datum"]}</text>'
        f'</svg>'
    )


def html_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


VORLAGE = """<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<title>Grundlagen-Check – Verlauf übers Jahr</title>
<style>
  @page {{ size: A4; margin: 14mm; }}
  body {{ font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10.5pt; color:#111; margin:0; }}
  h1 {{ font-size: 15pt; margin: 0 0 2mm; }}
  h2 {{ font-size: 11pt; margin: 0 0 6mm; color:#444; font-weight: normal; }}
  .karte {{ border: 1pt solid #000; border-radius: 2mm; padding: 4mm 6mm; margin-bottom: 5mm; page-break-inside: avoid; }}
  .karte h3 {{ margin: 0 0 2mm; font-size: 12pt; }}
  footer {{ margin-top: 6mm; font-size: 8pt; color:#666; }}
</style></head><body>

<h1>Grundlagen-Check – Verlauf übers Jahr</h1>
<h2>Gesamtergebnis je Testlauf, nur Nummern. Grundlage für die Diagnosegespräche.</h2>

{karten}

<footer>Erzeugt aus dem Verlauf-Speicher (nur Nummern). Zuordnung Nummer &rarr; Name liegt außerhalb dieser Datei.</footer>
</body></html>
"""


def bauen(verlauf_pfad: Path, ziel_ordner: Path):
    verlauf = lade_verlauf(verlauf_pfad)
    karten = []
    for nummer in sorted(verlauf.get("verlauf", {}), key=lambda n: int(n)):
        eintraege = verlauf["verlauf"][nummer]
        karten.append(
            f'<div class="karte"><h3>Nummer {html_escape(nummer)}</h3>{sparkline_svg(eintraege)}</div>'
        )

    seite = VORLAGE.format(karten="\n".join(karten))
    ziel_ordner.mkdir(parents=True, exist_ok=True)
    ziel = ziel_ordner / "Verlauf.html"
    ziel.write_text(seite, encoding="utf-8")
    return ziel


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    befehl = sys.argv[1]
    if befehl == "eintragen":
        if len(sys.argv) != 6:
            print(__doc__)
            sys.exit(1)
        n = eintragen(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5])
        print(f"{n} Nummern in {sys.argv[3]} eingetragen.")
    elif befehl == "bauen":
        if len(sys.argv) != 4:
            print(__doc__)
            sys.exit(1)
        ziel = bauen(Path(sys.argv[2]), Path(sys.argv[3]))
        print(f"geschrieben: {ziel}")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
