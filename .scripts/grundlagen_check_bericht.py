#!/usr/bin/env python3
"""Wertet einen Grundlagen-Check aus und erzeugt:

  1. Eine Rückmeldung pro Nummer (für das Coaching-Gespräch), gruppiert nach
     Themenblock, ohne Note.
  2. Eine Klassenübersicht: wie viel Prozent pro Themenblock richtig war,
     schwächster Block zuerst - als Grundlage für Unterrichtsschwerpunkte.
  3. Optional, wenn Selbsteinschätzungs-Daten mitgegeben werden: ein Diagramm,
     das zeigt, ob "sicher gefühlt" auch "richtig war" bedeutet hat - über die
     ganze Klasse und je Nummer als Warnhinweis bei Selbstüberschätzung.

Datenschutz: Diese Datei sieht nur Nummern, nie Namen. Die Zuordnung
Nummer -> Name bleibt bei Oskar, auf Papier oder außerhalb dieses Ordners.

Eingabe: eine JSON-Datei mit den eingelesenen Antworten, Format:
{
  "test": "5-6",                     // oder "6-9", siehe grundlagen_check_schluessel.py
  "ergebnisse": {
    "07": {"A1": {"a": "8292", "b": "3146", ...}, "A4": {"a": "1,2,3,4,6,8,12,24", ...}, ...},
    "12": {...}
  },
  "selbsteinschaetzung": {            // optional, pro Aufgabe (nicht pro Teilaufgabe)
    "07": {"A1": "sicher", "A2": "unsicher", ...},   // Werte: sicher/ging_so/unsicher
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

from grundlagen_check_schluessel import TESTS, schluessel_fuer_nummer

TOLERANZ = 0.006

# Statusfarben, validiert (siehe dataviz-Skill, references/palette.md).
FARBE_RICHTIG = "#0ca30c"
FARBE_FALSCH = "#d03b3b"
FARBE_OFFEN = "#9a9992"
KONFIDENZ_REIHENFOLGE = ["sicher", "ging_so", "unsicher"]
KONFIDENZ_LABEL = {"sicher": "War ich mir sicher", "ging_so": "Ging so", "unsicher": "War ich unsicher"}


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


def aufgabe_status(antworten_aufgabe, teile):
    """Status einer ganzen Aufgabe (z. B. 'A1' mit Teilaufgaben a,b), fuer den
    Vergleich mit der Selbsteinschaetzung, die pro Aufgabe erfasst wird, nicht
    pro Teilaufgabe. "richtig" heisst: alles Bearbeitete war richtig, mindestens
    ein Teil bearbeitet. "falsch" heisst: mindestens ein bearbeiteter Teil war
    falsch. "offen" heisst: nichts bearbeitet."""
    ergebnisse_teil = [pruefe((antworten_aufgabe or {}).get(teil), erwartet)
                        for teil, erwartet in teile.items()]
    if all(r is None for r in ergebnisse_teil):
        return "offen"
    if any(r is False for r in ergebnisse_teil):
        return "falsch"
    return "richtig"


# --- Selbsteinschaetzung vs. Ergebnis ---------------------------------------

def kreuztabelle(ergebnisse, selbsteinschaetzung, schluessel_je_nummer):
    """counts[konfidenz][status] = Anzahl Aufgaben (ueber alle Nummern), bei
    denen die Nummer diese Selbsteinschaetzung angekreuzt hat.
    schluessel_je_nummer: {nummer: schluessel} - bei Tests ohne A/B-Varianten
    fuer jede Nummer derselbe Schluessel, sonst je nach Version."""
    counts = {k: {"richtig": 0, "falsch": 0, "offen": 0} for k in KONFIDENZ_REIHENFOLGE}
    for nummer, antworten in ergebnisse.items():
        einschaetzung = selbsteinschaetzung.get(nummer, {})
        for aufgaben in schluessel_je_nummer[nummer].values():
            for aufgabe, teile in aufgaben.items():
                konf = einschaetzung.get(aufgabe)
                if konf not in counts:
                    continue
                status = aufgabe_status(antworten.get(aufgabe), teile)
                counts[konf][status] += 1
    return counts


def ueberschaetzung_je_nummer(ergebnisse, selbsteinschaetzung, schluessel_je_nummer):
    """Anzahl Aufgaben pro Nummer, die als 'sicher' markiert waren, aber falsch
    ausfielen - der konkrete Hinweis fuers Coaching-Gespraech."""
    ergebnis = {}
    for nummer, antworten in ergebnisse.items():
        einschaetzung = selbsteinschaetzung.get(nummer, {})
        treffer = []
        for aufgaben in schluessel_je_nummer[nummer].values():
            for aufgabe, teile in aufgaben.items():
                if einschaetzung.get(aufgabe) != "sicher":
                    continue
                if aufgabe_status(antworten.get(aufgabe), teile) == "falsch":
                    treffer.append(aufgabe)
        ergebnis[nummer] = treffer
    return ergebnis


def balken_svg(counts, breite=460, hoehe=260):
    """100%-gestapeltes Balkendiagramm: 3 Balken (sicher/ging so/unsicher),
    gestapelt richtig/falsch/offen. Duenne Balken, gerundete Aussenkanten,
    2px Fuge zwischen den Segmenten, Legende, direkte Beschriftung."""
    rand_unten, rand_oben, rand_links = 62, 14, 6
    plot_h = hoehe - rand_unten - rand_oben
    n = len(KONFIDENZ_REIHENFOLGE)
    balken_breite = 64
    luecke = (breite - 2 * rand_links - n * balken_breite) / (n - 1)

    teile = []
    for i, konf in enumerate(KONFIDENZ_REIHENFOLGE):
        werte = counts[konf]
        gesamt = sum(werte.values())
        x = rand_links + i * (balken_breite + luecke)
        if gesamt == 0:
            teile.append(
                f'<text x="{x + balken_breite/2:.0f}" y="{rand_oben + plot_h/2:.0f}" '
                f'text-anchor="middle" font-size="9.5" fill="#9a9992">keine Daten</text>'
            )
        else:
            y = rand_oben + plot_h
            for status, farbe in (("richtig", FARBE_RICHTIG), ("falsch", FARBE_FALSCH), ("offen", FARBE_OFFEN)):
                anteil = werte[status] / gesamt
                seg_h = anteil * plot_h
                if seg_h <= 0:
                    continue
                y -= seg_h
                radius = 4 if (status == "richtig" and y <= rand_oben + 0.5) else 0
                teile.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{balken_breite}" height="{max(seg_h-1.5,0):.1f}" '
                    f'rx="{radius}" fill="{farbe}"><title>{KONFIDENZ_LABEL[konf]}: {status} '
                    f'({werte[status]} von {gesamt}, {anteil*100:.0f}%)</title></rect>'
                )
                if seg_h > 16:
                    teile.append(
                        f'<text x="{x + balken_breite/2:.0f}" y="{y + seg_h/2 + 3.5:.0f}" '
                        f'text-anchor="middle" font-size="9" fill="#fff" font-weight="600">'
                        f'{anteil*100:.0f}%</text>'
                    )
        teile.append(
            f'<text x="{x + balken_breite/2:.0f}" y="{rand_oben + plot_h + 14:.0f}" '
            f'text-anchor="middle" font-size="9.5" fill="#333">{KONFIDENZ_LABEL[konf]}</text>'
        )
        teile.append(
            f'<text x="{x + balken_breite/2:.0f}" y="{rand_oben + plot_h + 26:.0f}" '
            f'text-anchor="middle" font-size="8.5" fill="#888">n={gesamt}</text>'
        )

    legende_y = hoehe - 6
    legende = (
        f'<g font-size="9" fill="#333">'
        f'<rect x="{rand_links}" y="{legende_y-9}" width="9" height="9" rx="2" fill="{FARBE_RICHTIG}"/>'
        f'<text x="{rand_links+13}" y="{legende_y-1}">richtig</text>'
        f'<rect x="{rand_links+70}" y="{legende_y-9}" width="9" height="9" rx="2" fill="{FARBE_FALSCH}"/>'
        f'<text x="{rand_links+83}" y="{legende_y-1}">falsch</text>'
        f'<rect x="{rand_links+140}" y="{legende_y-9}" width="9" height="9" rx="2" fill="{FARBE_OFFEN}"/>'
        f'<text x="{rand_links+153}" y="{legende_y-1}">nicht bearbeitet</text>'
        f'</g>'
    )

    return (
        f'<svg viewBox="0 0 {breite} {hoehe}" width="{breite}" height="{hoehe}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Selbsteinschätzung gegen tatsächliches Ergebnis">'
        f'{"".join(teile)}{legende}</svg>'
    )


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
  .selbst {{ margin: 0 0 8mm; border: 0.6pt solid #999; border-radius: 2mm; padding: 4mm 5mm; page-break-inside: avoid; }}
  .selbst h3 {{ margin: 0 0 1mm; font-size: 11pt; }}
  .selbst p {{ margin: 0 0 3mm; font-size: 9.3pt; color: #555; }}
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
  .warnung {{ margin-top: 1.5mm; font-size: 9.6pt; color: #b3261e; }}
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

{selbstabschnitt}

{karten}

<footer>Erzeugt aus den anonymisierten Antwortbögen (nur Nummern). Zuordnung Nummer &rarr; Name liegt außerhalb dieser Datei.</footer>
</body></html>
"""


def bauen(daten, ziel_ordner: Path):
    test = TESTS[daten["test"]]
    ergebnisse = daten["ergebnisse"]
    selbsteinschaetzung = daten.get("selbsteinschaetzung", {})
    schluessel_je_nummer = {n: schluessel_fuer_nummer(test, daten, n) for n in ergebnisse}
    # Block-Namen/Struktur sind zwischen A/B-Varianten identisch (nur die
    # Zahlen unterscheiden sich) - fuer Ueberschriften reicht eine Variante.
    schluessel_struktur = next(iter(schluessel_je_nummer.values())) if schluessel_je_nummer else {}

    # Klassenuebersicht: Quote je Block ueber alle Nummern
    block_quoten = {block: [] for block in schluessel_struktur}
    pro_nummer = {}
    for nummer, antworten in ergebnisse.items():
        auswertung = werte_nummer_aus(antworten, schluessel_je_nummer[nummer])
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

    # Selbsteinschaetzung vs. Ergebnis, nur wenn Daten vorhanden
    selbstabschnitt = ""
    ueberschaetzt = {}
    if selbsteinschaetzung:
        counts = kreuztabelle(ergebnisse, selbsteinschaetzung, schluessel_je_nummer)
        ueberschaetzt = ueberschaetzung_je_nummer(ergebnisse, selbsteinschaetzung, schluessel_je_nummer)
        n_sicher_falsch = counts["sicher"]["falsch"]
        n_sicher_gesamt = sum(counts["sicher"].values())
        selbstabschnitt = (
            '<div class="selbst"><h3>Selbsteinschätzung gegen Ergebnis</h3>'
            '<p>Je Aufgabe verglichen mit dem angekreuzten Smiley. '
            f'Bei „War ich mir sicher" lag die Klasse in {n_sicher_falsch} von {n_sicher_gesamt} '
            'Aufgaben trotzdem daneben – das sind die Stellen, an denen jemand nicht weiß, dass er es nicht weiß.</p>'
            f'{balken_svg(counts)}</div>'
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
        warnung = ""
        treffer = ueberschaetzt.get(nummer) or []
        if treffer:
            liste = ", ".join(treffer)
            warnung = (
                f'<div class="warnung">Sicher gefühlt, aber falsch: {html.escape(liste)} '
                f'– lohnt einen genaueren Blick im Gespräch.</div>'
            )
        karten.append(
            f'<div class="karte"><h3>Nummer {html.escape(nummer)}</h3>{"".join(zeilen)}{fokus}{warnung}</div>'
        )

    seite = VORLAGE.format(
        titel=f"Grundlagen-Check – {test['name']}",
        untertitel="Rückmeldung ohne Note · nur Nummern, keine Namen",
        klassenzeilen=klassenzeilen,
        selbstabschnitt=selbstabschnitt,
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
