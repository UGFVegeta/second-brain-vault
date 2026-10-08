#!/usr/bin/env python3
"""Mathe 7c – Übungsklassenarbeit zu KA 1 Rationale Zahlen.
Ähnliches Niveau wie die Arbeit, mehr Aufgaben, andere Reihenfolge, keine Karoflächen (Rechnen im Heft).
Gleicher Kopf und gleiche Aufgabenbalken wie die Arbeit, damit die Schüler das Aussehen kennen.
Danach dieselben Seiten als Lösung (pink ausgefüllt)."""
from fractions import Fraction as F
from pathlib import Path

import baue_ka1_7c as ka
from baue_ka1_7c import br

HIER = Path(__file__).parent
ZIEL = HIER / "Mathe 7c – Übungsklassenarbeit Nr. 1 Rationale Zahlen.html"
def _kreis(f):
    """Gleich große Kreise als SVG (die Zeichen ○ ◐ ● sind in Arial verschieden groß)."""
    innen = {"leer": "", "halb": '<path d="M8 1.5 A6.5 6.5 0 0 1 8 14.5 Z" fill="#1b1b1b"/>', "voll": '<circle cx="8" cy="8" r="6.5" fill="#1b1b1b"/>'}[f]
    return f'<svg class="kreis" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.6" fill="#fff" stroke="#1b1b1b" stroke-width="1.8"/>{innen}</svg>'


KREIS = [_kreis("leer"), _kreis("halb"), _kreis("voll")]

# ---------------------------------------------------------------- Aufgaben: (Term, Ergebnis-HTML, Wert zur Prüfung)
NR1 = [("−7", "3", "&lt;"), ("−12", "−21", "&gt;"), ("−3,5", "−3,05", "&lt;"), ("0", "−0,1", "&gt;"),
       ("−" + br("1", "2"), "−0,5", "="), ("−" + br("2", "3"), "−" + br("3", "4"), "&gt;"), ("−0,25", "−" + br("1", "4"), "="), ("4,1", "−4,9", "&gt;")]
assert -3.5 < -3.05 and F(-2, 3) > F(-3, 4) and F(-1, 4) == F("-0.25")

PUNKTE = [("A", -4.6), ("B", -1.5), ("C", 0.3), ("D", 5.8)]
EINTRAGEN = [("P", -4.5), ("Q", -1.2), ("R", 0.7), ("S", 3.4)]

NR3 = [("−14 + 9", 1), ("−8 + 20", 0), ("7 − 19", 1), ("−3,2 − 4,1", 1), ("−6 · (−9)", 0),
       ("12 · (−4)", 1), ("−56 : 8", 1), ("−72 : (−9)", 0), ("−2 · (−3) · (−5)", 1), ("−1,5 · 4 · (−2)", 0)]
assert [int(w < 0) for w in (-14 + 9, -8 + 20, 7 - 19, -3.2 - 4.1, -6 * -9, 12 * -4, -56 / 8, -72 / -9, -2 * -3 * -5, -1.5 * 4 * -2)] == [n for _, n in NR3]

NR4 = [("−38 + 64", "26", 26), ("−45 − 29", "−74", -74), ("17 − 53", "−36", -36), ("−81 + 27", "−54", -54),
       ("−2,4 + 5,1", "2,7", F("2.7")), ("−3,6 − 1,8", "−5,4", F("-5.4")), ("0,7 − 2,3", "−1,6", F("-1.6")), ("64 − 210", "−146", -146),
       ("−" + br("1", "3") + " + " + br("2", "3"), br("1", "3"), F(1, 3)),
       ("−" + br("3", "8") + " − " + br("1", "4"), "−" + br("5", "8"), F(-5, 8)),
       (br("1", "2") + " − " + br("5", "6"), "−" + br("1", "3"), F(-1, 3)),
       ("−1,25 − 0,75", "−2", -2)]
assert [w for *_, w in NR4] == [-38 + 64, -45 - 29, 17 - 53, -81 + 27, F("-2.4") + F("5.1"), F("-3.6") - F("1.8"), F("0.7") - F("2.3"), 64 - 210,
                                F(-1, 3) + F(2, 3), F(-3, 8) - F(1, 4), F(1, 2) - F(5, 6), F("-1.25") - F("0.75")]

NR5 = [("−7 · 8", "−56"), ("−9 · (−6)", "54"), ("63 : (−9)", "−7"), ("−84 : (−12)", "7"),
       ("−0,4 · 15", "−6"), ("−2,5 · (−4)", "10"), ("−3 · (−2) · (−5)", "−30"), ("4 · (−5) · (−3)", "60"),
       ("−1,2 : 3", "−0,4"), ("−4,8 : (−0,6)", "8"), ("−" + br("2", "3") + " · " + br("3", "4"), "−" + br("1", "2")),
       ("−" + br("3", "5") + " : " + br("3", "10"), "−2")]
assert (-7 * 8, -9 * -6, F(63) / -9, F(-84) / -12, F("-0.4") * 15, F("-2.5") * -4, -3 * -2 * -5, 4 * -5 * -3, F("-1.2") / 3, F("-4.8") / F("-0.6"),
        F(-2, 3) * F(3, 4), F(-3, 5) / F(3, 10)) == (-56, 54, -7, 7, -6, 10, -30, 60, F("-0.4"), 8, F(-1, 2), -2)

NR6 = [("−15 + 8 − 21 + 30 − 4", "−28 + 30 − 4 = −2", "1 P"),
       ("26 − 41 − 13 + 9", "−28 + 9 = −19", "1 P"),
       ("−3,5 + 7,2 − 4,5 − 1,2", "−8 + 6 = −2", "1,5 P"),
       ("14 − (9 − 20)", "14 − 9 + 20 = 25", "1,5 P"),
       ("−23 − (−6 + 15)", "−23 + 6 − 15 = −32", "2 P"),
       ("−7,5 − (2,5 − 10)", "−7,5 − 2,5 + 10 = 0", "2 P")]
assert (-15 + 8 - 21 + 30 - 4, 26 - 41 - 13 + 9, F("-3.5") + F("7.2") - F("4.5") - F("1.2"), 14 - (9 - 20), -23 - (-6 + 15), F("-7.5") - (F("2.5") - 10)) == (-2, -19, -2, 25, -32, 0)

assert -17 + 9 == -8 and -8 - 14 == -22 and -8 - (-22) == 14
assert 2480 - 680 == 1800 and F("-9.5") + 6 == F("-3.5") and 1800 + 540 == 2340 and F("-3.5") - F("8.5") == -12 and 2480 - 2340 == 140 and -12 - F("-9.5") == F("-2.5")


def balken(nr, stufe, punkte, text, l, bew=""):
    return (f'<div class="balken"><b>Nr. {nr} &nbsp;<span class="kr">{KREIS[stufe]}</span></b><span class="pk">____ / {punkte}</span></div>'
            f'<p class="anw">{text}' + (f' <span class="pkt">({bew})</span>' if l and bew else "") + "</p>")


def liste(terme, l, spalten=3, lsg=None):
    z = []
    for i, t in enumerate(terme):
        r = f' <span class="lsg">= {lsg[i]}</span>' if l and lsg else ""
        z.append(f'<span>{"abcdefghijkl"[i]}) &nbsp;{t}{r}</span>')
    return f'<div class="liste" style="grid-template-columns:repeat({spalten},1fr)">' + "".join(z) + "</div>"


THEMEN = [("Zahlen am Zahlenstrahl ablesen und eintragen", "S. 11 Nr. 3, 6 · S. 36 Nr. 3, 4 · S. 42 Nr. 1, 2"),
          ("Zahlen vergleichen und ordnen", "S. 15 Nr. 5 · S. 36 Nr. 2, 5 · S. 42 Nr. 3"),
          ("Addieren und Subtrahieren", "S. 18 Nr. 1–4 · S. 36 Nr. 6, 7, 8, 10 · S. 42 Nr. 4"),
          ("Mehrere Zahlen, Minusklammer", "S. 26 Nr. 8 · S. 36 Nr. 9 · S. 37 Nr. 20 a, b · S. 42 Nr. 6, 8 a"),
          ("Multiplizieren und Dividieren", "S. 28 Nr. 3 · S. 30 Nr. 6 · S. 37 Nr. 13, 14, 15 · S. 42 Nr. 5"),
          ("Sachaufgaben: Temperatur, Höhen, Kontostand", "S. 23 Nr. 9, 10 · S. 37 Nr. 24 · S. 42 Nr. 10")]


def themen():
    return ('<table class="themen"><tr><th>Das kommt in der Klassenarbeit dran</th><th>Hier übst du im Buch</th></tr>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in THEMEN)
            + '<tr><td colspan="2" class="tipp">Tipp: Der Rückspiegel auf S. 42 ist wie ein kleiner Test. Die Lösungen stehen hinten im Buch auf S. 222.</td></tr></table>')


def kopf(l):
    k = ka.kopf(l).replace("Klassenarbeit Nr. 1", "Übungsklassenarbeit zur Klassenarbeit Nr. 1").replace(f"/ {ka.GESAMT} Punkte", f"/ {GESAMT} Punkte")
    alt = "Ohne Rechenweg keine Punkte. Aufgabe in die Kästchen abschreiben, dann rechnen."
    neu = "Rechne im Heft: Aufgabe abschreiben, dann Schritt für Schritt rechnen. In der Arbeit gilt: Ohne Rechenweg keine Punkte."
    assert alt in k
    return k.replace(alt, neu)


def seite1(l):
    nr1 = "".join(f'<span class="vg">{"abcdefgh"[i]}) &nbsp;{a} <span class="kast">{z if l else ""}</span> {b}</span>' for i, (a, b, z) in enumerate(NR1))
    zs = ka.zahlenstrahl(l, PUNKTE, -6, 7).split('<div class="zsantw">')[0]
    zl = ('<div class="zsantw">' + "".join(f'<span><b>{b}:</b> <span class="lsg">{str(v).replace(".", ",").replace("-", "−")}</span></span>' for b, v in PUNKTE) + "</div>") if l else ""
    return (kopf(l) + themen()
            + balken(1, 0, 4, "Setze &lt;, &gt; oder = ein. Du darfst auf dem Blatt arbeiten.", l, "je ½ P")
            + '<div class="zeichen"><span><b>&lt;</b> &nbsp;ist kleiner als: &nbsp;−4 &lt; −1</span><span><b>&gt;</b> &nbsp;ist größer als: &nbsp;2 &gt; −3</span>'
              '<span class="tipp">Die Spitze zeigt immer auf die kleinere Zahl. Die kleinere Zahl liegt am Zahlenstrahl weiter links.</span></div>'
            + f'<div class="vgl vier">{nr1}</div>'
            + balken(2, 0, 2, "Welche Zahlen sind markiert? Schreibe sie ins Heft: A = …", l, "je ½ P") + zs + zl)


def seite2(l):
    nr4 = '<div class="liste pn5">' + "".join(
        f'<span>{"abcdefghij"[i]}) &nbsp;{t}' + (f' <span class="lsg">→ {"negativ" if n else "positiv"}</span>' if l else "") + "</span>" for i, (t, n) in enumerate(NR3)) + "</div>"
    ein = ka.zahlenstrahl(l, EINTRAGEN if l else [], -5, 5).split('<div class="zsantw">')[0]
    if l:
        ein = ein.replace('fill="#1b1b1b"/><line', f'fill="{ka.MAG}"/><line').replace('stroke="#1b1b1b" stroke-width="3"/><text', f'stroke="{ka.MAG}" stroke-width="3"/><text')
    werte = " &nbsp;&nbsp; ".join(f'<span class="nw">{b} = {str(v).replace(".", ",").replace("-", "−")}</span>' for b, v in EINTRAGEN)
    return (balken(3, 0, 2, f"Markiere die Zahlen mit einem Pfeil auf dem Zahlenstrahl.<br><b>{werte}</b>", l, "je ½ P") + ein
            + balken(4, 1, 5, "Ist das Ergebnis positiv oder negativ? Entscheide, ohne zu rechnen. Schreibe ins Heft: a) negativ …", l, "je ½ P") + nr4
            + balken(5, 1, 12, "Berechne.", l, "je 1 P")
            + liste([t for t, _, _ in NR4], l, 3, [r for _, r, _ in NR4])
            + balken(6, 1, 12, "Berechne.", l, "je 1 P")
            + liste([t for t, _ in NR5], l, 3, [r for _, r in NR5]))


def huetten(l):
    """Höhenprofil Bergstation – Almhütte – Gipfelhütte, schwarz-weiß für den Druck."""
    P = {"B": (110, 70), "A": (390, 175), "G": (650, 95)}
    o = ['<svg class="huette" viewBox="0 0 760 250" font-family="Arial, sans-serif">',
         '<defs><marker id="hp" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 Z" fill="#000"/></marker></defs>',
         '<path d="M0,240 L60,90 L110,70 L170,95 L390,175 L470,150 L650,95 L700,80 L760,140 L760,240 Z" fill="#eef1f5" stroke="#9aa3b0"/>']
    for a_, b_ in (("B", "A"), ("A", "G")):
        (x1, y1), (x2, y2) = P[a_], P[b_]
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2 - 10 if x2 > x1 else x2}" y2="{y2}" stroke="#000" stroke-width="3" marker-end="url(#hp)"/>')
    for x, y in P.values():
        o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#000" stroke="#fff" stroke-width="2"/>')
    t = lambda x, y, s_, w=400, f=19, c="#000", a="middle": o.append(f'<text x="{x}" y="{y}" font-size="{f}" font-weight="{w}" fill="{c}" text-anchor="{a}">{s_}</text>')
    M = ka.MAG
    t(110, 30, "Bergstation", 700, 21); t(110, 52, "2480 m · −9,5 °C")
    t(390, 212, "Almhütte", 700, 21); t(650, 40, "Gipfelhütte", 700, 21)
    t(390, 236, "1800 m · −3,5 °C" if l else "? m · ? °C", 700, 19, M if l else "#000")
    t(650, 64, "2340 m · −12 °C" if l else "? m · ? °C", 700, 19, M if l else "#000")
    t(250, 150, "−680 m", 700); t(250, 172, "+6 °C", 700)
    t(530, 175, "+540 m", 700, a="start"); t(530, 197, "−8,5 °C", 700, a="start")
    o.append("</svg>")
    return "".join(o)


def seite3(l):
    L = lambda t: f'<p class="lsg ltext">{t}</p>' if l else ""
    return (balken(7, 2, 9, "Berechne. Bei d) bis f) zuerst die Minusklammer auflösen.", l)
            + '<div class="liste" style="grid-template-columns:1fr 1fr">' + "".join(
                f'<span>{"abcdef"[i]}) &nbsp;{t}' + (f'<br><span class="lsg kl">= {r}</span> <span class="pkt">({p})</span>' if l else "") + "</span>"
                for i, (t, r, p) in enumerate(NR6)) + "</div>"
            + balken(8, 1, 3, "In Moskau zeigt das Thermometer morgens −17 °C. Bis zum Mittag steigt die Temperatur um 9 Grad, bis zum Abend fällt sie um 14 Grad.", l)
            + '<p class="anw">a) Wie warm ist es am Mittag? &nbsp; b) Wie warm ist es am Abend? &nbsp; c) Um wie viel Grad ist es am Abend kälter als am Mittag?</p>'
            + L("a) −17 + 9 = −8 °C &nbsp; b) −8 − 14 = −22 °C &nbsp; c) 14 Grad (von −8 bis −22) <span class='pkt'>(je 1 P)</span>")
            + balken(9, 2, 4, "Eine Skitour führt von der Bergstation über die Almhütte zur Gipfelhütte. "
                     "An den Pfeilen steht, wie sich Höhe und Temperatur unterwegs ändern.", l)
            + huetten(l)
            + '<p class="anw">a) In welcher Höhe liegt die Almhütte und welche Temperatur misst man dort?<br>'
            'b) In welcher Höhe liegt die Gipfelhütte und welche Temperatur misst man dort?<br>'
            'c) Vergleiche Bergstation und Gipfelhütte: Wie viele Meter liegt die Gipfelhütte tiefer, und wie viel Grad ist es dort kälter?</p>'
            + L("a) 2480 − 680 = 1800 m; &nbsp; −9,5 + 6 = −3,5 °C <span class='pkt'>(1 P)</span><br>"
                "b) 1800 + 540 = 2340 m; &nbsp; −3,5 − 8,5 = −12 °C <span class='pkt'>(1 P)</span><br>"
                "c) 2480 − 2340 = 140 m tiefer; &nbsp; von −9,5 °C auf −12 °C, also 2,5 Grad kälter <span class='pkt'>(2 P)</span>")
            + f'<div class="legende">{KREIS[0]} leicht &nbsp;&nbsp; {KREIS[1]} mittel &nbsp;&nbsp; {KREIS[2]} schwer</div>')


GESAMT = 4 + 2 + 2 + 5 + 12 + 12 + 9 + 3 + 4

EXTRA = """<style>
.vgl.vier{grid-template-columns:repeat(3,1fr)}
.liste{font-size:15pt;row-gap:2.6mm}
.pn5{grid-template-columns:repeat(2,1fr)}
.lsg{color:#E6007E;font-weight:700}.lsg.kl{font-size:13pt}
.ltext{font-size:13pt;line-height:1.6;margin:1mm 0 2mm}
.kr{font-weight:400}
.kreis{width:1.2em;height:1.2em;vertical-align:-.25em}
.nw{white-space:nowrap}
.zeichen{display:flex;flex-wrap:wrap;gap:1.5mm 12mm;border:.6pt dashed #555;padding:2mm 4mm;margin:0 0 3mm;font-size:13pt}
.zeichen b{font-size:16pt}.zeichen .tipp{flex-basis:100%;font-size:11.5pt}
.legende{margin-top:auto;font-size:11pt;color:#555}
.seite .zsantw{font-size:14pt}
.themen{width:100%;border-collapse:collapse;font-size:11pt;margin:0 0 1mm}
.themen th{background:#c8c8c8;border:.6pt solid #555;padding:1.4mm 3mm;text-align:left}
.themen td{border:.6pt solid #555;padding:1.2mm 3mm}.themen td.tipp{font-size:10pt;font-style:italic}
.huette{width:88%;display:block;margin:0 auto 1mm}
</style>"""


def druckfassung(l):
    """Nur Aufgaben (l=False) oder nur Lösung (l=True), ohne Leiste, für das PDF. Gibt (HTML, Seitenzahl) zurück."""
    seiten = [seite1, seite2, seite3]
    teil = "".join(f'<section class="seite">{s(l)}<div class="snr">Seite {i + 1} von {len(seiten)}</div></section>' for i, s in enumerate(seiten))
    return ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Mathe 7c – Übungsklassenarbeit Nr. 1 Rationale Zahlen</title>' + ka.CSS + EXTRA
            + '</head><body>' + teil + '</body></html>'), len(seiten)


def main():
    seiten = [seite1, seite2, seite3]
    teil = lambda l: "".join(f'<section class="seite">{s(l)}<div class="snr">Seite {i + 1} von {len(seiten)}</div></section>' for i, s in enumerate(seiten))
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Mathe 7c – Übungsklassenarbeit Nr. 1 Rationale Zahlen</title>' + ka.CSS + EXTRA + '</head><body>'
            '<div class="leiste"><b>Übungsklassenarbeit · Klasse 7c</b><a href="#arbeit">Aufgaben (3 Seiten)</a><a href="#loesung">Lösung (3 Seiten)</a>'
            f'<span>{GESAMT} Punkte · Rechnen im Heft</span></div>'
            '<div class="trenner" id="arbeit">Aufgaben</div>' + teil(False)
            + '<div class="trenner" id="loesung">Lösung</div>' + teil(True) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name, GESAMT, "Punkte")


if __name__ == "__main__":
    main()
