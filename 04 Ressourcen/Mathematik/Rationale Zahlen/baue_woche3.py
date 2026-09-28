#!/usr/bin/env python3
"""Mathe 7c, Woche 3 (28.09. bis 02.10.2026): Plus und Minus üben, dann Rechenvorteile und Rechengesetze mit Namen.
Neues Wochenformat (mathe_woche_vorlage.py). Die Aufgaben der Montagsstunde kommen aus baue_stunde3.py.
Aufruf: python3 baue_woche3.py  -> Mathe 7c – Woche 3.html und Mathe 7c – Woche 3 – Folien für den Beamer.pdf"""
import subprocess, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche, aus_skript  # noqa: E402
from baue_stunde3 import HA, BLITZ, FOLIEN as FOLIEN_MO, FCSS, ueb_folie  # noqa: E402
import re  # noqa: E402

bogengerade, = aus_skript(HIER / "baue_stunde2.py", "bogengerade")
PDF = "Mathe 7c – Woche 3 – Folien für den Beamer.pdf"


def leere_gerade(von, bis, schritt=1, kpe=2, breite=None):
    """Nur der Zahlenstrahl zum Einzeichnen an der Tafel: ohne Bogen, ohne Startpunkt, ohne Lösung."""
    s = bogengerade(von, bis, von, 0, schritt=schritt, kpe=kpe, arc=False)
    s = re.sub(r'<circle [^>]*/><text [^>]*>[^<]*</text></svg>$', "</svg>", s)
    return s.replace('class="gerade"', f'class="gerade" style="width:{breite};height:auto"', 1) if breite else s


GERADEN = ('<div class="ausdruck">14 − 30 =</div>' + leere_gerade(-18, 16, schritt=2, breite="100%")
           + '<div class="ausdruck" style="margin-top:.25in">−3 − 9 =</div>' + leere_gerade(-14, 1, breite="90%"))
HA_PDF = HIER / "Rationale Zahlen 2 – Arbeitsblatt Plus und Minus – Lösungen (nur für mich).pdf"
BILDER = HIER / "bilder"


def ha_bilder():
    """Lösungsblatt als zwei Bildausschnitte (Aufgaben 1–3 und 4–6), ohne die Kopfzeile „nur für mich“."""
    from PIL import Image
    BILDER.mkdir(exist_ok=True)
    roh = BILDER / "_ha_loesung.png"
    subprocess.run(["pdftoppm", "-r", "250", "-png", "-singlefile", str(HA_PDF), str(roh.with_suffix(""))], check=True)
    im = Image.open(roh)
    f = im.width / 595                       # Grenzen in PDF-Punkten (A4 = 595 pt breit), gemessen mit pdftotext -bbox
    for name, (y0, y1) in {"ha-loesung-1-3.png": (96, 299), "ha-loesung-4-5.png": (299, 511), "ha-loesung-6.png": (511, 648)}.items():
        im.crop((int(30 * f), int(y0 * f), int(565 * f), int(y1 * f))).save(BILDER / name)
    roh.unlink()


def ha_folie(datei, hoehe):
    return f'<img src="bilder/{datei}" alt="" style="display:block;max-width:100%;max-height:{hoehe};margin:0 auto">'


FOLIEN = ([("Hausaufgabe: Lösungen 1 bis 3", ha_folie("ha-loesung-1-3.png", "5.6in")),
           ("Hausaufgabe: Lösungen 4 und 5", ha_folie("ha-loesung-4-5.png", "5.9in")),
           ("Hausaufgabe: Lösung 6", ha_folie("ha-loesung-6.png", "5.9in")),
           ("In welche Richtung geht der Bogen?", GERADEN)] + FOLIEN_MO[1:])

VORBEREITEN = [
    ("Mo, IF-Stunde", f"Nichts drucken. Folien in Notability: {PDF}. Strichliste mit Nr. 1 bis 6, je Halbgruppe eine Spalte. "
                      "Die Schüler brauchen das Arbeitsblatt (HA), das Übungsheft und einen Stift in anderer Farbe."),
    ("Di bis Do", '<span class="offen">noch offen, planen wir als Nächstes</span>'),
]

SCHRITTE = [
    ("Montag · IF-Stunde, je Halbgruppe gleich", "HA kontrollieren", 12,
     "Lösungen zeigen, jeder prüft selbst mit anderer Farbe. Handzeichen pro Aufgabe, Fehlerzahl ohne Namen notieren: "
     "erster Hinweis für die spätere Einteilung nach Leistung.", [1, 2, 3]),
    ("", "Bogen wiederholen", 4, "Zwei Minus-Aufgaben an der leeren Zahlengerade: Bogen live einzeichnen, dabei laut fragen, in welche Richtung er geht "
     "und ob er über die Null läuft. Lösung im Tafelbild.", [4]),
    ("", "Blitzrunde Minus", 6, "Acht Aufgaben, nur Ergebnisse ins Übungsheft, dann selbst abhaken. 7 oder 8 richtig: gleich mit ◐ starten.", [5, 6]),
    ("", "Üben ○◐●", 15, "Einstieg selbst wählen, Übungsheft. In der Halbgruppe ist Zeit für Einzelne.", [7, 8]),
    ("", "Geht das schneller?", 5, "Nur Ideen sammeln. Das ist die Brücke zu den Rechengesetzen.", [9, 10]),
    ("Dienstag · Doppelstunde", "Weiter üben", 0, '<span class="offen">noch offen</span>', []),
    ("Mittwoch und Donnerstag", "Rechengesetze benennen", 0,
     '<span class="offen">noch offen. Ziel laut Bildungsplan (Kl. 7/8/9, Teilkompetenz 9): Kommutativ- und Assoziativgesetz '
     'angeben und an Beispielen erläutern, nicht nur anwenden.</span>', []),
]

TAFEL = f"""<div class="box"><h3>Montag: die zwei typischen Fehler beim Minus</h3>
<p>Die leeren Zahlengeraden stehen auf Folie 4, du zeichnest die Bögen live ein. Bleibt an der Tafel, kommt nicht ins Merkheft. Immer fragen: In welche Richtung geht der Bogen?</p>
<div class="tafel"><div class="ausdruck">14 − 30 = <span class="lsg">−16</span> <span style="font-size:16px;font-weight:400">(nicht 16: der Bogen läuft über die Null)</span></div>
<figure>{bogengerade(-18, 16, 14, -30, schritt=2, kpe=2)}</figure>
<div class="ausdruck">−3 − 9 = <span class="lsg">−12</span> <span style="font-size:16px;font-weight:400">(nicht +6: ohne Klammer heißt Minus einfach nach links)</span></div>
<figure>{bogengerade(-14, 1, -3, -9, kpe=2)}</figure></div></div>
<div class="box"><h3>Dienstag bis Donnerstag</h3><p class="offen">noch offen</p></div>"""

MERKHEFT = """<div class="box"><h3>Montag</h3><p>Kein neuer Eintrag. Die Regeln zum Addieren und Subtrahieren stehen seit letzter Woche im Merkheft.</p></div>
<div class="box"><h3>Donnerstag: Rechengesetze</h3><p class="offen">noch offen. Geplant: Kommutativgesetz (Vertauschungsgesetz) und
Assoziativgesetz (Verbindungsgesetz) der Addition, jeweils mit Namen, Regel in Worten und einem Beispiel mit rationalen Zahlen.</p></div>"""

HA_TAB = "".join(f"<tr><td><b>{n}</b></td><td>{l}</td></tr>" for n, l in HA)
LOESUNGEN = f"""<div class="box"><h3>Hausaufgabe: Arbeitsblatt „Plus und Minus“</h3><table class="ha">{HA_TAB}</table>
<p>Ausführlich mit Rechenwegen: Rationale Zahlen 2 – Arbeitsblatt Plus und Minus – Lösungen (nur für mich).pdf</p></div>
<div class="box"><h3>Blitzrunde</h3><ol type="a" class="kl">{"".join(f"<li>{a} = <span class=lsg>{b}</span></li>" for a, b in BLITZ)}</ol></div>
<div class="box"><h3>Üben ○◐●</h3>{ueb_folie(True)}</div>"""


def main():
    ha_bilder()
    ziel = HIER / "Mathe 7c – Woche 3.html"
    bau_woche(ziel, "Woche 3: Plus und Minus üben, Rechengesetze",
              "Klasse 7c · Mathematik · 28.09. bis 02.10.2026 · Rationale Zahlen",
              VORBEREITEN, SCHRITTE, FOLIEN, TAFEL, MERKHEFT, LOESUNGEN)
    fol = HIER / "_folien_woche3.html"
    fol.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><style>{FCSS}</style></head><body>'
                   + "".join(f'<div class="slide"><h1>{t}</h1>{h}</div>' for t, h in FOLIEN) + "</body></html>", encoding="utf-8")
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={HIER / PDF}", fol.as_uri()], check=True, capture_output=True)
    fol.unlink()
    print("Folien-PDF:", PDF)


if __name__ == "__main__":
    main()
