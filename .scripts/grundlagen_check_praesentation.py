#!/usr/bin/env python3
"""Baut aus einem Grundlagen-Check-Ergebnis eine Beamer-Ansicht für die ganze
Klasse: nur die Klassenebene (Themenblöcke + Selbsteinschätzung gegen
Ergebnis), großformatig, keine Nummern-Karten. Gedacht zum Projizieren im
Unterricht, nicht zum Ausdrucken.

Datenschutz: zeigt bewusst nichts auf Nummern-Ebene - das würde bei einer
Projektion vor der ganzen Klasse die Anonymität der einzelnen Antwortbögen
untergraben, auch ohne Namen.

Aufruf:
  python3 .scripts/grundlagen_check_praesentation.py <ergebnisse.json> <ausgabe-ordner>
"""
import html
import json
import sys
from pathlib import Path

from grundlagen_check_schluessel import TESTS, schluessel_fuer_nummer
from grundlagen_check_bericht import (
    werte_nummer_aus, block_quote, kreuztabelle, balken_svg,
    FARBE_RICHTIG, FARBE_FALSCH, FARBE_OFFEN,
)

# Ampelfarben nach denselben Schwellen wie stufe_text() in grundlagen_check_bericht.py,
# damit Beamer-Ansicht und Rückmeldungs-Karten dieselbe Sprache sprechen.
FARBE_WARNUNG = "#fab219"
FARBE_ERNST = "#ec835a"


def status_farbe(quote):
    if quote is None:
        return FARBE_OFFEN
    if quote >= 0.8:
        return FARBE_RICHTIG
    if quote >= 0.6:
        return FARBE_WARNUNG
    if quote >= 0.4:
        return FARBE_ERNST
    return FARBE_FALSCH


def svg_responsive(svg, max_breite):
    """Ersetzt feste width/height-Attribute eines <svg> durch CSS-Grenzen, damit
    Balken UND Beschriftung gemeinsam mit der Fensterbreite mitskalieren
    (SVG-Text skaliert mit dem viewBox, anders als HTML-Text)."""
    import re as _re
    return _re.sub(
        r'width="\d+(\.\d+)?" height="\d+(\.\d+)?"',
        f'width="100%" style="max-width:{max_breite}px"',
        svg, count=1,
    )


def balken_bloecke_svg(sortierte_bloecke, breite=1000):
    """Ein breiter horizontaler Balken pro Themenblock, groß beschriftet."""
    balken_h, luecke, rand_oben = 46, 22, 6
    label_breite = 400
    plot_breite = breite - label_breite - 90
    hoehe = rand_oben + len(sortierte_bloecke) * (balken_h + luecke)

    teile = []
    y = rand_oben
    for block, quote in sortierte_bloecke:
        farbe = status_farbe(quote)
        teile.append(
            f'<text x="0" y="{y + balken_h/2 + 7:.0f}" font-size="19" fill="#111">{html.escape(block)}</text>'
        )
        teile.append(
            f'<rect x="{label_breite}" y="{y}" width="{plot_breite}" height="{balken_h}" '
            f'rx="6" fill="#e1e0d9"/>'
        )
        if quote is not None:
            w = max(plot_breite * quote, 6)
            teile.append(
                f'<rect x="{label_breite}" y="{y}" width="{w:.1f}" height="{balken_h}" rx="6" fill="{farbe}"/>'
            )
            teile.append(
                f'<text x="{label_breite + plot_breite + 14}" y="{y + balken_h/2 + 8:.0f}" '
                f'font-size="22" font-weight="700" fill="#111">{quote*100:.0f}&#160;%</text>'
            )
        else:
            teile.append(
                f'<text x="{label_breite + 14}" y="{y + balken_h/2 + 7:.0f}" '
                f'font-size="16" fill="#888" font-style="italic">noch nicht bearbeitet</text>'
            )
        y += balken_h + luecke

    return (
        f'<svg viewBox="0 0 {breite} {hoehe}" width="100%" style="max-width:{breite}px" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ergebnis je Themenblock">'
        f'{"".join(teile)}</svg>'
    )


VORLAGE = """<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grundlagen-Check – Klasse</title>
<style>
  html {{ scroll-snap-type: y mandatory; }}
  body {{ font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; color:#111; margin:0; background:#fcfcfb; }}
  section {{
    min-height: 100vh; box-sizing: border-box; scroll-snap-align: start;
    display: flex; flex-direction: column; justify-content: center;
    padding: 6vh 6vw; border-bottom: 1px solid #e1e0d9;
  }}
  h1 {{ font-size: 3em; margin: 0 0 0.2em; }}
  h2 {{ font-size: 1.4em; margin: 0 0 1.2em; color:#52514e; font-weight: 500; }}
  .fund {{ font-size: 1.7em; font-weight: 700; margin: 0.8em 0 0.3em; }}
  .fund .zahl {{ color: {farbe_falsch}; }}
  .erklaerung {{ font-size: 1.15em; color:#333; max-width: 60ch; line-height:1.5; }}
  .legende {{ display:flex; gap:2em; margin-top:2em; font-size:1em; color:#333; flex-wrap:wrap; }}
  .legende span {{ display:inline-flex; align-items:center; gap:0.5em; }}
  .swatch {{ width:16px; height:16px; border-radius:4px; display:inline-block; }}
  .hinweis {{ font-size:0.9em; color:#898781; margin-top:2em; }}
  footer.seite {{ position: fixed; bottom: 1.2vh; right: 1.5vw; font-size:0.8em; color:#c3c2b7; }}
</style></head><body>

<section>
  <h1>{titel}</h1>
  <h2>Rückmeldung ohne Note &middot; {klasse}</h2>
  <p class="erklaerung">Was ihr aus Klasse 5 und 6 sicher könnt &ndash; und wo wir im Unterricht noch üben.</p>
</section>

<section>
  <h1>Ergebnis je Themenblock</h1>
  <h2>Über die ganze Klasse gemittelt</h2>
  {balken_bloecke}
  <div class="legende">
    <span><span class="swatch" style="background:{farbe_richtig}"></span>sicher</span>
    <span><span class="swatch" style="background:{farbe_warnung}"></span>größtenteils sicher</span>
    <span><span class="swatch" style="background:{farbe_ernst}"></span>noch unsicher</span>
    <span><span class="swatch" style="background:{farbe_falsch}"></span>braucht Übung</span>
  </div>
</section>

{selbst_slide}

<footer class="seite">nur Klassen-Gesamtwerte, keine Namen oder Nummern</footer>
</body></html>
"""

SELBST_VORLAGE = """<section>
  <h1>Wie sicher habt ihr euch gefühlt?</h1>
  <h2>Smiley-Einschätzung je Aufgabe gegen das tatsächliche Ergebnis</h2>
  {balken_svg}
  <p class="fund">Bei &bdquo;war ich mir sicher&ldquo; lag die Klasse trotzdem in
    <span class="zahl">{anteil:.0f}&#160;%</span> der Fälle daneben.</p>
  <p class="erklaerung">Das ist völlig normal &ndash; und die wichtigste Erkenntnis aus dem ganzen Test:
    Nicht wissen, dass man etwas nicht weiß, ist der Moment, an dem man am wenigsten übt. Deshalb lohnt sich
    ein zweiter Blick genau bei den Aufgaben, bei denen ihr euch sicher gefühlt habt.</p>
</section>
"""


def bauen(daten, ziel_ordner: Path, klasse: str):
    test = TESTS[daten["test"]]
    ergebnisse = daten["ergebnisse"]
    selbsteinschaetzung = daten.get("selbsteinschaetzung", {})
    schluessel_je_nummer = {n: schluessel_fuer_nummer(test, daten, n) for n in ergebnisse}
    schluessel_struktur = next(iter(schluessel_je_nummer.values())) if schluessel_je_nummer else {}

    block_quoten = {block: [] for block in schluessel_struktur}
    for nummer, antworten in ergebnisse.items():
        auswertung = werte_nummer_aus(antworten, schluessel_je_nummer[nummer])
        for block, eintraege in auswertung.items():
            q = block_quote(eintraege)
            if q is not None:
                block_quoten[block].append(q)
    klassen_mittel = {
        block: (sum(qs) / len(qs) if qs else None) for block, qs in block_quoten.items()
    }
    sortierte_bloecke = sorted(
        klassen_mittel.items(), key=lambda kv: (kv[1] is None, kv[1] if kv[1] is not None else 1)
    )

    selbst_slide = ""
    if selbsteinschaetzung:
        counts = kreuztabelle(ergebnisse, selbsteinschaetzung, schluessel_je_nummer)
        n_sicher_falsch = counts["sicher"]["falsch"]
        n_sicher_gesamt = sum(counts["sicher"].values())
        if n_sicher_gesamt:
            anteil = n_sicher_falsch / n_sicher_gesamt * 100
            diagramm = svg_responsive(balken_svg(counts, breite=700, hoehe=340), max_breite=760)
            selbst_slide = SELBST_VORLAGE.format(balken_svg=diagramm, anteil=anteil)

    seite = VORLAGE.format(
        titel=f"Grundlagen-Check &ndash; {html.escape(test['name'])}",
        klasse=html.escape(klasse),
        balken_bloecke=balken_bloecke_svg(sortierte_bloecke),
        selbst_slide=selbst_slide,
        farbe_richtig=FARBE_RICHTIG, farbe_warnung=FARBE_WARNUNG,
        farbe_ernst=FARBE_ERNST, farbe_falsch=FARBE_FALSCH,
    )

    ziel_ordner.mkdir(parents=True, exist_ok=True)
    ziel = ziel_ordner / "Praesentation.html"
    ziel.write_text(seite, encoding="utf-8")
    return ziel


def main():
    if len(sys.argv) not in (3, 4):
        print(__doc__)
        sys.exit(1)
    daten = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    klasse = sys.argv[3] if len(sys.argv) == 4 else "Klasse"
    ziel = bauen(daten, Path(sys.argv[2]), klasse)
    print(f"geschrieben: {ziel}")


if __name__ == "__main__":
    main()
