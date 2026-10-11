#!/usr/bin/env python3
"""Mathe 7c – Kurztest Rationale Zahlen, Gruppe A und B (ca. 15 bis 20 Minuten, je eine A4-Seite).
Gleicher Kopf, gleiche Aufgabenbalken und gleiche Kreise wie Klassenarbeit und Übungsklassenarbeit.
Danach dieselben Seiten als Lösung (pink ausgefüllt). Schrift wie in der Klassenarbeit: Aufgaben 15,5 pt, Text 12,5 pt."""
from fractions import Fraction as F
from pathlib import Path

import baue_ka1_7c as ka
import baue_uebung_ka1_7c as ue
from baue_ka1_7c import br

HIER = Path(__file__).parent
ZIEL = HIER / "Mathe 7c – Kurztest Rationale Zahlen.html"
GESAMT = 18


def m(x):
    return str(x).replace("-", "−").replace(".", ",")


# ---------------------------------------------------------------- Aufgaben je Gruppe
# Nr. 1: (links, rechts, Zeichen)
VGL = {
    "A": [("−9", "4", "&lt;"), ("−1,8", "−1,08", "&lt;"), ("−" + br("3", "5"), "−" + br("2", "3"), "&gt;"), ("−0,75", "−" + br("3", "4"), "=")],
    "B": [("6", "−11", "&gt;"), ("−2,3", "−3,2", "&gt;"), ("−" + br("5", "6"), "−" + br("2", "3"), "&lt;"), ("−0,25", "−" + br("1", "4"), "=")],
}
assert -9 < 4 and F("-1.8") < F("-1.08") and F(-3, 5) > F(-2, 3) and F("-0.75") == F(-3, 4)
assert 6 > -11 and F("-2.3") > F("-3.2") and F(-5, 6) < F(-2, 3) and F("-0.25") == F(-1, 4)

# Nr. 2 Addieren und Subtrahieren, Nr. 3 Multiplizieren und Dividieren: (Term, Ergebnis)
ADD = {
    "A": [("−27 + 45", "18"), ("−36 − 28", "−64"), ("19 − 52", "−33"), ("−3,4 + 1,9", "−1,5"),
          ("−" + br("2", "3") + " + " + br("1", "6"), "−" + br("1", "2"))],
    "B": [("−34 + 58", "24"), ("−47 − 25", "−72"), ("23 − 71", "−48"), ("−4,8 − 1,7", "−6,5"),
          ("−" + br("3", "4") + " + " + br("1", "8"), "−" + br("5", "8"))],
}
assert (-27 + 45, -36 - 28, 19 - 52, F("-3.4") + F("1.9"), F(-2, 3) + F(1, 6)) == (18, -64, -33, F("-1.5"), F(-1, 2))
assert (-34 + 58, -47 - 25, 23 - 71, F("-4.8") - F("1.7"), F(-3, 4) + F(1, 8)) == (24, -72, -48, F("-6.5"), F(-5, 8))

MAL = {
    "A": [("−6 · 7", "−42"), ("−8 · (−9)", "72"), ("56 : (−7)", "−8"), ("−2 · (−5) · (−3)", "−30"), ("−0,3 · 12", "−3,6")],
    "B": [("−9 · 4", "−36"), ("−7 · (−6)", "42"), ("−72 : (−8)", "9"), ("−3 · (−2) · (−4)", "−24"), ("−1,5 · (−6)", "9")],
}
assert (-6 * 7, -8 * -9, F(56, -7), -2 * -5 * -3, F("-0.3") * 12) == (-42, 72, -8, -30, F("-3.6"))
assert (-9 * 4, -7 * -6, F(-72, -8), -3 * -2 * -4, F("-1.5") * -6) == (-36, 42, 9, -24, 9)

# Nr. 4 mehrere Zahlen, Minusklammer: (Term, Zwischenschritt, Ergebnis)
MEHR = {
    "A": [("−12 + 7 − 18 + 20", "−30 + 27", "−3"), ("9 − (4 − 15)", "9 − 4 + 15", "20")],
    "B": [("−14 + 6 − 11 + 25", "−25 + 31", "6"), ("11 − (5 − 17)", "11 − 5 + 17", "23")],
}
assert (-12 + 7 - 18 + 20, 9 - (4 - 15), -30 + 27, 9 - 4 + 15) == (-3, 20, -3, 20)
assert (-14 + 6 - 11 + 25, 11 - (5 - 17), -25 + 31, 11 - 5 + 17) == (6, 23, 6, 23)

# Nr. 5 Sachaufgabe: Text, Fragen (Frage, Rechnung, Ergebnis)
SACH = {
    "A": ("In Oslo zeigt das Thermometer morgens −8 °C. Bis zum Mittag steigt die Temperatur um 5 Grad, bis zum Abend fällt sie um 11 Grad.",
          [("Wie warm ist es am Mittag?", "−8 + 5", "−3 °C"), ("Wie warm ist es am Abend?", "−3 − 11", "−14 °C")]),
    "B": ("In Kiruna zeigt das Thermometer abends −6 °C. Bis Mitternacht fällt die Temperatur um 9 Grad, bis zum Morgen steigt sie um 4 Grad.",
          [("Wie warm ist es um Mitternacht?", "−6 − 9", "−15 °C"), ("Wie warm ist es am Morgen?", "−15 + 4", "−11 °C")]),
}
assert (-8 + 5, -3 - 11, -6 - 9, -15 + 4) == (-3, -14, -15, -11)


# ---------------------------------------------------------------- Bausteine
def ul(inhalt, l, breit=30):
    """Antwortlinie; in der Lösung mit pinker Eintragung."""
    return f'<span class="ul" style="min-width:{breit}mm">{inhalt if l else ""}</span>'


def balken(nr, stufe, punkte, text, l, bew=""):
    return ue.balken(nr, stufe, punkte, text, l, bew)


def kopf(g, l):
    return (f'<div class="kopfwrap"><table class="kopf">'
            f'<tr><td colspan="2" class="titel"><u>Kurztest Rationale Zahlen</u> &nbsp;·&nbsp; Gruppe {g}</td><td class="kl">Klasse 7c</td></tr>'
            '<tr><td class="n">Name:</td><td colspan="2" class="n">Datum:</td></tr>'
            f'<tr><td class="n">Punkte: <span class="pp">/ {GESAMT} Punkte</span></td><td class="n">Note:</td><td class="n">Ø</td></tr>'
            f'</table>{ka.WOLKE}</div>'
            + ('<p class="loesmark">Lösung mit Punkteverteilung</p>' if l else "")
            + '<div class="hinweis">Ohne Rechenweg keine Punkte.</div>')


def seite(g, l):
    vgl = "".join(f'<span class="vg">{"abcd"[i]}) &nbsp;{a} <span class="kast">{z if l else ""}</span> {b}</span>' for i, (a, b, z) in enumerate(VGL[g]))

    def reihe(daten):
        return '<div class="az">' + "".join(
            f'<span>{"abcde"[i]}) &nbsp;{t} = {ul(r, l, 26)}</span>' for i, (t, r) in enumerate(daten)) + "</div>"

    mehr = '<div class="mz">' + "".join(
        f'<div>{"ab"[i]}) &nbsp;{t} = {ul(z, l, 52)} = {ul(r, l, 24)}</div>' for i, (t, z, r) in enumerate(MEHR[g])) + "</div>"
    text, fragen = SACH[g]
    sach = '<div class="sz">' + "".join(
        f'<div>{"ab"[i]}) &nbsp;{q} &nbsp;{ul(rech, l, 34)} = {ul(erg, l, 24)}</div>' for i, (q, rech, erg) in enumerate(fragen)) + "</div>"
    return (kopf(g, l)
            + balken(1, 0, 2, "Setze &lt;, &gt; oder = ein.", l, "je ½ P") + f'<div class="vgl2">{vgl}</div>'
            + balken(2, 1, 5, "Berechne.", l, "je 1 P") + reihe(ADD[g])
            + balken(3, 1, 5, "Berechne.", l, "je 1 P") + reihe(MAL[g])
            + balken(4, 2, 3, "Berechne. Bei b) zuerst die Minusklammer auflösen.", l, "a) 1 P, b) 2 P") + mehr
            + balken(5, 1, 3, text, l, "je 1,5 P") + sach
            + f'<div class="legende">{ue.KREIS[0]} leicht &nbsp;&nbsp; {ue.KREIS[1]} mittel &nbsp;&nbsp; {ue.KREIS[2]} schwer</div>')


CSS = """<style>
.seite{justify-content:space-between;padding-top:11mm;padding-bottom:12mm}
.seite>.balken{margin:3mm 0 1mm}
.seite>.anw{margin:0}
.vgl2{display:flex;justify-content:space-between;font-size:15.5pt;white-space:nowrap}
.vgl2 .kast{width:9mm;height:11mm;margin:0 1mm}
.az{display:grid;grid-template-columns:1fr 1fr;row-gap:1mm;font-size:15.5pt;white-space:nowrap}
.mz>div,.sz>div{font-size:15.5pt;white-space:nowrap}
.mz>div+div{margin-top:1mm}
.sz{display:grid;gap:1mm}
.sz>div{font-size:12.5pt;line-height:1.35}
.ul{display:inline-block;border-bottom:.8pt solid #1b1b1b;height:2.1em;line-height:2.1em;text-align:center;color:#E6007E;font-weight:700;vertical-align:bottom;padding:0 1mm;font-size:15.5pt}
.ul .br{font-size:.85em}
.legende{margin-top:3mm;font-size:12pt}
.loesmark{top:4mm}
.seite .hinweis{padding:1.4mm 3mm;margin-bottom:0}
.seite .kopfwrap{margin-bottom:0}
</style>"""


def druck(g, l):
    return f'<section class="seite" id="{"l" if l else "a"}{g}">{seite(g, l)}</section>'


def main():
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Mathe 7c – Kurztest Rationale Zahlen</title>' + ka.CSS + ue.EXTRA + CSS + '</head><body>'
            '<div class="leiste"><b>Kurztest · Klasse 7c</b><a href="#aA">Gruppe A</a><a href="#aB">Gruppe B</a>'
            '<a href="#lA">Lösung A</a><a href="#lB">Lösung B</a>'
            f'<span>{GESAMT} Punkte · ca. 15 bis 20 Minuten · je eine A4-Seite</span></div>'
            + druck("A", False) + druck("B", False) + druck("A", True) + druck("B", True) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name, GESAMT, "Punkte")


if __name__ == "__main__":
    main()
