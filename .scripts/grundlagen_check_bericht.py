#!/usr/bin/env python3
"""Wertet einen Grundlagen-Check aus und erzeugt zwei Ausgaben:

  1. Eine Rückmeldung pro Nummer (für das Coaching-Gespräch), gruppiert nach
     Themenblock, ohne Note.
  2. Eine Klassenübersicht: wie viel Prozent pro Themenblock richtig war,
     schwächster Block zuerst - als Grundlage für Unterrichtsschwerpunkte.

Datenschutz: Diese Datei sieht nur Nummern, nie Namen. Die Zuordnung
Nummer -> Name bleibt bei Oskar, auf Papier oder außerhalb dieses Ordners.

Eingabe: eine JSON-Datei mit den eingelesenen Antworten, Format:
{
  "test": "5-6",                     // oder "6-9", siehe grundlagen_check_schluessel.py
  "ergebnisse": {
    "07": {"A1": {"a": "8292", "b": "3146", ...}, "A4": {"a": "1,2,3,4,6,8,12,24", ...}, ...},
    "12": {...}
  }
}
Die Aufgaben- und Teilaufgaben-Schlüssel müssen zu den Aufgaben im jeweiligen
Lösungsschlüssel passen (siehe grundlagen_check_schluessel.py). Fehlt eine
Teilaufgabe oder ist sie leer, zählt sie als "nicht bearbeitet", nicht als falsch.

Aufruf:
  python3 .scripts/grundlagen_check_bericht.py <ergebnisse.json> <ausgabe-ordner>

Baut zusaetzlich ein Beispiel mit erfundenen Nummern, wenn ohne Argumente
aufgerufen (siehe unten, main_beispiel()).
"""
import html
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

from grundlagen_check_schluessel import TESTS

TOLERANZ = 0.006


# --- Antworten interpretieren ------------------------------------------------

def _zu_zahl(s):
    """Versucht, eine Zahl aus einem Antworttext zu lesen (Komma als Dezimaltrennzeichen,
    Einheiten und Vorzeichen-Buchstaben wie 'x=' werden abgestreift)."""
    s = s.strip().lower()
    s = re.sub(r"^[a-z]\s*=\s*", "", s)  # "x=8" -> "8"
    s = re.sub(r"[a-zA-Zµ°%²³]+$", "", s).strip()  # Einheiten am Ende weg
    s = s.replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _zu_bruchwert(s):
    """Bruch oder gemischte Zahl als Zahlenwert, z. B. '1 1/4' oder '5/4' -> 1.25."""
    s = s.strip()
    m = re.fullmatch(r"(-?\d+)\s+(\d+)\s*/\s*(\d+)", s)
    if m:
        ganz, z, n = map(int, m.groups())
        vz = -1 if ganz < 0 else 1
        return ganz + vz * Fraction(z, n)
    m = re.fullmatch(r"(-?\d+)\s*/\s*(\d+)", s)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    return None


def wert(s):
    """Bester Zahlenwert einer Antwort, egal ob Dezimalzahl oder Bruch. None wenn nicht lesbar."""
    if s is None:
        return None
    z = _zu_zahl(s)
    if z is not None:
        return z
    b = _zu_bruchwert(s)
    if b is not None:
        return float(b)
    return None


def normalisiere_text(s):
    s = s.strip().lower()
    s = s.replace("²", "^2").replace("³", "^3")
    s = s.replace("·", "").replace("*", "")
    s = re.sub(r"\s+", "", s)
    return s


def ist_leer(s):
    return s is None or not str(s).strip()


def pruefe(antwort_roh, erwartet):
    """Liefert True/False/None (None = nicht bearbeitet oder nicht lesbar)."""
    if ist_leer(antwort_roh):
        return None
    roh = str(antwort_roh)

    if isinstance(erwartet, set):
        gefunden = set(re.findall(r"\d+", roh))
        return gefunden == erwartet

    if isinstance(erwartet, list):
        tokens = [t for t in re.split(r"[<,;\s]+", roh) if t]
        if len(tokens) != len(erwartet):
            return None
        soll = [wert(x) for x in erwartet]
        ist = [wert(x) for x in tokens]
        if None in soll or None in ist:
            return None
        return all(abs(a - b) < TOLERANZ for a, b in zip(soll, ist))

    if isinstance(erwartet, tuple):
        for option in erwartet:
            r = pruefe(roh, option)
            if r:
                return True
        return False

    if isinstance(erwartet, (int, float)):
        v = wert(roh)
        if v is None:
            return False
        return abs(v - erwartet) < TOLERANZ

    if isinstance(erwartet, str):
        if erwartet in ("<", ">", "="):
            return roh.strip() == erwartet
        return normalisiere_text(roh) == normalisiere_text(erwartet)

    return None


# --- Auswertung pro Nummer ---------------------------------------------------

def werte_nummer_aus(antworten, schluessel):
    """antworten: {Aufgabe: {Teil: roh}}. Liefert pro Block eine Liste von
    (itemid, status) mit status in {"richtig","falsch","offen"}."""
    ergebnis = {}
    for block, aufgaben in schluessel.items():
        eintraege = []
        for aufgabe, teile in aufgaben.items():
            for teil, erwartet in teile.items():
                roh = (antworten.get(aufgabe) or {}).get(teil)
                r = pruefe(roh, erwartet)
                status = "offen" if r is None else ("richtig" if r else "falsch")
                itemid = f"{aufgabe}{teil}" if len(teil) == 1 else f"{aufgabe} ({teil})"
                eintraege.append((itemid, status))
        ergebnis[block] = eintraege
    return ergebnis


def block_quote(eintraege):
    bearbeitet = [s for _, s in eintraege if s != "offen"]
    if not bearbeitet:
        return None
    richtig = sum(1 for s in bearbeitet if s == "richtig")
    return richtig / len(bearbeitet)


# --- Ausgabe: Ruckmeldungen pro Nummer + Klassenuebersicht -----------------

def stufe_text(quote):
    if quote is None:
        return "nicht bearbeitet"
    if quote >= 0.8:
        return "sicher"
    if quote >= 0.6:
        return "größtenteils sicher"
    if quote >= 0.4:
        return "noch unsicher"
    return "braucht Übung"


def stufe_klasse(quote):
    """Stabiler CSS-Klassenname, unabhaengig von Umlauten im Anzeigetext."""
    if quote is None:
        return "nicht-bearbeitet"
    if quote >= 0.8:
        return "sicher"
    if quote >= 0.6:
        return "groesstenteils-sicher"
    if quote >= 0.4:
        return "noch-unsicher"
    return "braucht-uebung"


VORLAGE = """<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<title>Grundlagen-Check – Rückmeldungen</title>
<style>
  @page {{ size: A4; margin: 14mm; }}
  body {{ font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10.5pt; color:#111; margin:0; }}
  h1 {{ font-size: 15pt; margin: 0 0 2mm; }}
  h2 {{ font-size: 11pt; margin: 0 0 3mm; color:#444; font-weight: normal; }}
  .uebersicht {{ margin: 0 0 8mm; }}
  .uebersicht table {{ border-collapse: collapse; width: 100%; }}
  .uebersicht th, .uebersicht td {{ border: 0.6pt solid #999; padding: 1.6mm 2.5mm; text-align: left; font-size: 9.5pt; }}
  .uebersicht th {{ background: #eee; }}
  .karte {{ border: 1pt solid #000; border-radius: 2mm; padding: 5mm 6mm; margin-bottom: 6mm; page-break-inside: avoid; }}
  .karte h3 {{ margin: 0 0 3mm; font-size: 12.5pt; }}
  .zeile {{ display:flex; justify-content:space-between; gap:4mm; margin: 1mm 0; font-size: 10pt; }}
  .zeile .stufe {{ font-weight: 600; }}
  .stufe.sicher {{ color: #1a7a3c; }}
  .stufe.groesstenteils-sicher {{ color: #6b7a1a; }}
  .stufe.noch-unsicher {{ color: #a06a00; }}
  .stufe.braucht-uebung {{ color: #b3261e; }}
  .stufe.nicht-bearbeitet {{ color: #666; font-style: italic; }}
  .fokus {{ margin-top: 3mm; font-size: 9.6pt; color:#333; }}
  footer {{ margin-top: 6mm; font-size: 8pt; color:#666; }}
</style></head><body>

<h1>{titel}</h1>
<h2>{untertitel}</h2>

<div class="uebersicht">
  <table>
    <tr><th>Themenblock</th><th>Klasse gesamt richtig</th></tr>
    {klassenzeilen}
  </table>
</div>

{karten}

<footer>Erzeugt aus den anonymisierten Antwortbögen (nur Nummern). Zuordnung Nummer &rarr; Name liegt außerhalb dieser Datei.</footer>
</body></html>
"""


def bauen(daten, ziel_ordner: Path):
    test = TESTS[daten["test"]]
    schluessel = test["schluessel"]
    ergebnisse = daten["ergebnisse"]

    # Klassenuebersicht: Quote je Block ueber alle Nummern
    block_quoten = {block: [] for block in schluessel}
    pro_nummer = {}
    for nummer, antworten in ergebnisse.items():
        auswertung = werte_nummer_aus(antworten, schluessel)
        pro_nummer[nummer] = auswertung
        for block, eintraege in auswertung.items():
            q = block_quote(eintraege)
            if q is not None:
                block_quoten[block].append(q)

    klassen_mittel = {
        block: (sum(qs) / len(qs) if qs else None) for block, qs in block_quoten.items()
    }
    # schwaechster Block zuerst
    sortierte_bloecke = sorted(
        klassen_mittel.items(), key=lambda kv: (kv[1] is None, kv[1] if kv[1] is not None else 1)
    )
    klassenzeilen = "\n".join(
        f'<tr><td>{html.escape(b)}</td><td>{"—" if q is None else f"{q*100:.0f} %"}</td></tr>'
        for b, q in sortierte_bloecke
    )

    karten = []
    for nummer in sorted(ergebnisse):
        auswertung = pro_nummer[nummer]
        zeilen = []
        quoten = []
        for block, eintraege in auswertung.items():
            q = block_quote(eintraege)
            if q is not None:
                quoten.append((block, q))
            klasse = stufe_klasse(q)
            zeilen.append(
                f'<div class="zeile"><span>{html.escape(block)}</span>'
                f'<span class="stufe {klasse}">{stufe_text(q)}'
                f'{"" if q is None else f" ({q*100:.0f} %)"}</span></div>'
            )
        schwaechste = sorted(quoten, key=lambda bq: bq[1])[:2]
        fokus = ""
        if schwaechste:
            namen = ", ".join(b.split(" · ", 1)[-1] for b, _ in schwaechste)
            fokus = f'<div class="fokus">Fokus fürs Gespräch: {html.escape(namen)}</div>'
        karten.append(
            f'<div class="karte"><h3>Nummer {html.escape(nummer)}</h3>{"".join(zeilen)}{fokus}</div>'
        )

    seite = VORLAGE.format(
        titel=f"Grundlagen-Check – {test['name']}",
        untertitel="Rückmeldung ohne Note · nur Nummern, keine Namen",
        klassenzeilen=klassenzeilen,
        karten="\n".join(karten),
    )

    ziel_ordner.mkdir(parents=True, exist_ok=True)
    ziel = ziel_ordner / f"Rückmeldungen {test['name']}.html"
    ziel.write_text(seite, encoding="utf-8")
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
