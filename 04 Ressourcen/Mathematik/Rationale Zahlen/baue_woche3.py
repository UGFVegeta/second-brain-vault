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
from baue_stunde3 import HA, BLITZ, FOLIEN, FCSS, ueb_folie  # noqa: E402

bogengerade, = aus_skript(HIER / "baue_stunde2.py", "bogengerade")
PDF = "Mathe 7c – Woche 3 – Folien für den Beamer.pdf"

VORBEREITEN = [
    ("Mo, IF-Stunde", f"Nichts drucken. Folien in Notability: {PDF}. Strichliste mit Nr. 1 bis 6, je Halbgruppe eine Spalte. "
                      "Die Schüler brauchen das Arbeitsblatt (HA), das Übungsheft und einen Stift in anderer Farbe."),
    ("Di bis Do", '<span class="offen">noch offen, planen wir als Nächstes</span>'),
]

SCHRITTE = [
    ("Montag · IF-Stunde, je Halbgruppe gleich", "HA kontrollieren", 15,
     "Lösungen zeigen, jeder prüft selbst mit anderer Farbe. Handzeichen pro Aufgabe, Fehlerzahl ohne Namen notieren: "
     "erster Hinweis für die spätere Einteilung nach Leistung. Die zwei häufigsten Fehler an der Zahlengerade vorrechnen lassen.", [1]),
    ("", "Blitzrunde Minus", 7, "Acht Aufgaben, nur Ergebnisse ins Übungsheft, dann selbst abhaken. 7 oder 8 richtig: gleich mit ◐ starten.", [2, 3]),
    ("", "Üben ○◐●", 15, "Einstieg selbst wählen, Übungsheft. In der Halbgruppe ist Zeit für Einzelne.", [4, 5]),
    ("", "Geht das schneller?", 5, "Nur Ideen sammeln. Das ist die Brücke zu den Rechengesetzen.", [6, 7]),
    ("Dienstag · Doppelstunde", "Weiter üben", 0, '<span class="offen">noch offen</span>', []),
    ("Mittwoch und Donnerstag", "Rechengesetze benennen", 0,
     '<span class="offen">noch offen. Ziel laut Bildungsplan (Kl. 7/8/9, Teilkompetenz 9): Kommutativ- und Assoziativgesetz '
     'angeben und an Beispielen erläutern, nicht nur anwenden.</span>', []),
]

TAFEL = f"""<div class="box"><h3>Montag: die zwei typischen Fehler beim Minus</h3>
<p>Bleibt an der Tafel, kommt nicht ins Merkheft. Immer fragen: In welche Richtung geht der Bogen?</p>
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
