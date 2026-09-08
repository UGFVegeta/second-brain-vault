#!/usr/bin/env python3
"""Legt das fertige Paket fuer die Schul-Cloud auf den Schreibtisch.

Erzeugt:
  Sportcurriculum 2026-27/
    Sportcurriculum Klasse 5 bis 10.html      interaktive Fassung
    Sportcurriculum Klasse 5 bis 10.pdf       alle Jahrgaenge, sieben Seiten
    Einzelne Klassen/Klasse 5.pdf ... 10.pdf  je ein Blatt
    Hinweise.txt

Aufruf:  python3 .scripts/sport_curriculum_export.py
Setzt voraus, dass Google Chrome installiert ist, es erzeugt die PDFs.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
QUELLE = VAULT / "04 Ressourcen/Sport/Sportcurriculum.html"
BUILD = Path(__file__).resolve().parent / "sport_curriculum_build.py"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

SCHULJAHR = "2026-27"
ZIEL = Path.home() / "Desktop" / f"Sportcurriculum {SCHULJAHR}"
KLASSEN = [5, 6, 7, 8, 9, 10]

HINWEISE = """Sportcurriculum der Sportfachschaft
Stand Schuljahr 2026/27

In diesem Ordner liegen dieselben Inhalte zweimal: einmal als PDF zum Lesen und
Drucken auf jedem Gerät, einmal als HTML zum Nachschlagen am Rechner.


Sportcurriculum Klasse 5 bis 10.pdf
Alle sechs Jahrgänge, jeder auf einer eigenen Seite, dahinter die beiden
Übersichten. Öffnet sich in IServ direkt im Browser, auch am Handy und Tablet.

Ordner "Einzelne Klassen"
Für jede Klassenstufe ein einzelnes Blatt, fertig zum Ausdrucken.

Sportcurriculum Klasse 5 bis 10.html
Die Fassung zum Klicken: oben die Klassenstufe wählen, dann stehen die Inhalte
und die Bewertungstabelle dieser Stufe nebeneinander. Zwei Druckknöpfe, einer
für die angezeigte Klasse, einer für das gesamte Curriculum.
In IServ über das Drei-Punkte-Menü der Datei auf "Öffnen" gehen. Wird die Datei
dabei stattdessen heruntergeladen, im Download-Ordner doppelklicken. Sie öffnet
sich dann im Browser und braucht kein Internet.


Die Bewertungstabellen stammen vom Sprengel Remstal, Stand 10.09.2011, und
gelten für Schüler (männlich).
"""


def bauen():
    subprocess.run([sys.executable, str(BUILD)], check=True)


def pdf(html_text, ziel, arbeit):
    """Eine HTML-Fassung nach PDF drucken."""
    tmp = arbeit / (ziel.stem + ".html")
    tmp.write_text(html_text, encoding="utf-8")
    subprocess.run(
        [str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={ziel}", tmp.as_uri()],
        check=True, capture_output=True,
    )
    seiten = len(re.findall(rb"/Type\s*/Page[^s]", ziel.read_bytes()))
    return seiten


def main():
    if not CHROME.exists():
        sys.exit("Google Chrome nicht gefunden, die PDFs koennen nicht erzeugt werden.")

    bauen()
    seite = QUELLE.read_text(encoding="utf-8")

    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    einzel = ZIEL / "Einzelne Klassen"
    einzel.mkdir(parents=True)

    # 1. interaktive Fassung
    name_html = ZIEL / "Sportcurriculum Klasse 5 bis 10.html"
    shutil.copy2(QUELLE, name_html)

    with tempfile.TemporaryDirectory() as tmpdir:
        arbeit = Path(tmpdir)

        # 2. alles als ein PDF
        alles = seite.replace("<body>", '<body data-druck="alles">', 1)
        n = pdf(alles, ZIEL / "Sportcurriculum Klasse 5 bis 10.pdf", arbeit)
        print(f"Gesamt-PDF: {n} Seiten")

        # 3. je Klasse ein Blatt
        for k in KLASSEN:
            eine = seite.replace("<body>", '<body data-druck="klasse">', 1)
            eine = eine.replace(
                f'<section class="klasse" id="klasse-{k}"',
                f'<section class="klasse drucken" id="klasse-{k}"',
            )
            n = pdf(eine, einzel / f"Klasse {k}.pdf", arbeit)
            print(f"  Klasse {k}: {n} Seite(n)")

    (ZIEL / "Hinweise.txt").write_text(HINWEISE, encoding="utf-8")

    groesse = sum(f.stat().st_size for f in ZIEL.rglob("*") if f.is_file())
    print(f"\nFertig: {ZIEL}  ({groesse/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
