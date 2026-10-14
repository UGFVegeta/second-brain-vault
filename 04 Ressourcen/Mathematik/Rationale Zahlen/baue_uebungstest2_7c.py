#!/usr/bin/env python3
"""Mathe 7c – Übungstest 2 Rationale Zahlen (Gruppe A und B, 18 Punkte, ca. 15 bis 20 Minuten, je eine A4-Seite).
Gleicher Aufbau wie der erste Übungstest (baue_uebungstest_7c.py), andere Zahlen; Nr. 4 verbindet die Rechenarten
(Thema von Woche 5), Nr. 5 ist eine Sachaufgabe mit Etagen bzw. Tiefe.
Erzeugt HTML, vier PDFs (A, B, Lösung A, Lösung B) und ein Lösungsblatt „A und B“ (A4 quer)."""
import subprocess
import tempfile
from fractions import Fraction as F
from pathlib import Path

from pypdf import PdfReader, PdfWriter

import baue_ka1_7c as ka
import baue_uebung_ka1_7c as ue
import baue_uebungstest_7c as ut
from baue_ka1_7c import br

HIER = Path(__file__).resolve().parent
NAME = "Mathe 7c – Übungstest 2 Rationale Zahlen"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

ut.TITEL = "Übungstest 2 Rationale Zahlen"
ut.ANW4 = "Berechne. Erst die Klammer, dann Mal und Geteilt, dann Plus und Minus."
ut.BEW4 = "je 1,5 P"

ut.VGL.update({
    "A": [("−12", "−21", "&gt;"), ("−3,5", "−3,05", "&lt;"), ("−" + br("3", "4"), "−" + br("4", "5"), "&gt;"), ("−" + br("1", "8"), "−0,125", "=")],
    "B": [("5", "−15", "&gt;"), ("−4,5", "−4,05", "&lt;"), ("−" + br("3", "4"), "−" + br("5", "6"), "&gt;"), ("−0,2", "−" + br("1", "5"), "=")],
})
assert -12 > -21 and F("-3.5") < F("-3.05") and F(-3, 4) > F(-4, 5) and F("-0.125") == F(-1, 8)
assert 5 > -15 and F("-4.5") < F("-4.05") and F(-3, 4) > F(-5, 6) and F("-0.2") == F(-1, 5)

ut.ADD.update({
    "A": [("−38 + 61", "23"), ("−44 − 29", "−73"), ("17 − 60", "−43"), ("−2,6 + 1,4", "−1,2"),
          ("−" + br("1", "2") + " − " + br("1", "3"), "−" + br("5", "6"))],
    "B": [("−52 + 29", "−23"), ("−36 − 47", "−83"), ("21 − 75", "−54"), ("−3,8 + 5,3", "1,5"),
          ("−" + br("1", "4") + " − " + br("1", "2"), "−" + br("3", "4"))],
})
assert (-38 + 61, -44 - 29, 17 - 60, F("-2.6") + F("1.4"), F(-1, 2) - F(1, 3)) == (23, -73, -43, F("-1.2"), F(-5, 6))
assert (-52 + 29, -36 - 47, 21 - 75, F("-3.8") + F("5.3"), F(-1, 4) - F(1, 2)) == (-23, -83, -54, F("1.5"), F(-3, 4))

ut.MAL.update({
    "A": [("−7 · 8", "−56"), ("−9 · (−6)", "54"), ("72 : (−8)", "−9"), ("−4 · (−5) · (−2)", "−40"), ("−0,6 · 20", "−12")],
    "B": [("−6 · 9", "−54"), ("−8 · (−7)", "56"), ("−63 : (−7)", "9"), ("2 · (−5) · (−3)", "30"), ("−1,2 : 0,3", "−4")],
})
assert (-7 * 8, -9 * -6, F(72, -8), -4 * -5 * -2, F("-0.6") * 20) == (-56, 54, -9, -40, -12)
assert (-6 * 9, -8 * -7, F(-63, -7), 2 * -5 * -3, F("-1.2") / F("0.3")) == (-54, 56, 9, 30, -4)

ut.MEHR.update({
    "A": [("−3 · 4 + 15", "−12 + 15", "3"), ("18 − 2 · (−5)", "18 + 10", "28")],
    "B": [("−24 : 6 + 9", "−4 + 9", "5"), ("(−8 + 3) · (−4)", "−5 · (−4)", "20")],
})
assert (-3 * 4 + 15, -12 + 15, 18 - 2 * -5, 18 + 10) == (3, 3, 28, 28)
assert (F(-24, 6) + 9, -4 + 9, (-8 + 3) * -4, -5 * -4) == (5, 5, 20, 20)

ut.SACH.update({
    "A": ("Ein Fahrstuhl startet in der Tiefgarage auf Etage −2. Er fährt 7 Etagen nach oben und danach 4 Etagen nach unten.",
          [("Auf welcher Etage ist er nach der Fahrt nach oben?", "−2 + 7", "Etage 5"), ("Auf welcher Etage ist er danach?", "5 − 4", "Etage 1")]),
    "B": ("Ein Taucher ist in −8 m Tiefe. Er steigt 5 m auf und taucht danach 9 m ab.",
          [("In welcher Höhe ist er nach dem Aufstieg?", "−8 + 5", "−3 m"), ("In welcher Höhe ist er nach dem Abtauchen?", "−3 − 9", "−12 m")]),
})
assert (-2 + 7, 5 - 4, -8 + 5, -3 - 9) == (5, 1, -3, -12)

ZIEL = HIER / f"{NAME}.html"
ZIEL_AB = HIER / f"{NAME} – Lösung A und B.html"


def pdf(html, ziel):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={ziel}",
                    "--virtual-time-budget=3000", html.as_uri()], check=True, capture_output=True)


def main():
    kopfleiste = (f'<div class="leiste"><b>Übungstest 2, Klasse 7c</b><a href="#aA">Gruppe A</a><a href="#aB">Gruppe B</a>'
                  f'<a href="#lA">Lösung A</a><a href="#lB">Lösung B</a><span>{ut.GESAMT} Punkte; ca. 15 bis 20 Minuten; je eine A4-Seite</span></div>')
    seiten = ut.druck("A", False) + ut.druck("B", False) + ut.druck("A", True) + ut.druck("B", True)
    kopf = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{NAME}</title>' + ka.CSS + ue.EXTRA + ut.CSS)
    ZIEL.write_text(kopf + "</head><body>" + kopfleiste + seiten + "</body></html>", encoding="utf-8")
    ZIEL_AB.write_text(kopf + ut.CSS_AB + '</head><body><div class="paar"><div class="h">' + ut.druck("A", True)
                       + '</div><div class="h">' + ut.druck("B", True) + "</div></div></body></html>", encoding="utf-8")
    alle = Path(tempfile.mkdtemp()) / "alle.pdf"
    pdf(ZIEL, alle)
    r = PdfReader(str(alle))
    assert len(r.pages) == 4, ("Seitenzahl", len(r.pages))
    for i, name in enumerate([f"{NAME} A.pdf", f"{NAME} B.pdf", f"{NAME} A – Lösung.pdf", f"{NAME} B – Lösung.pdf"]):
        w = PdfWriter()
        w.add_page(r.pages[i])
        w.write(str(HIER / name))
    pdf(ZIEL_AB, HIER / f"{NAME} – Lösung A und B.pdf")
    assert len(PdfReader(str(HIER / f"{NAME} – Lösung A und B.pdf")).pages) == 1
    print("fertig:", NAME, "4 PDFs + Lösung A und B")


if __name__ == "__main__":
    main()
