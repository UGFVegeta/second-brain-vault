#!/usr/bin/env python3
"""Mathe 10b – Übungsklassenarbeit zu KA 1 (Prozent, Zinsen, Wahrscheinlichkeit).
Gleiches Layout wie die Übungs-KA der 7c: Kopf, Tabelle "Das kommt dran | Hier übst du", Schwierigkeitskreise,
Rechnen im Heft. Danach dieselben Seiten als Lösung (pink ausgefüllt).
Bewusst anderes Zufallsgerät, andere Darstellung und anderer Kontext als im KA-Vorschlag, aber dieselben Fertigkeiten.
Alle Zahlen werden unten geprüft."""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "Rationale Zahlen"))
import baue_ka1_7c as ka  # noqa: E402  (CSS, Wolke, Bruch-Helfer)
from baue_ka1_7c import br  # noqa: E402

ZIEL = HIER / "Mathe 10b – Übungsklassenarbeit Nr. 1 Prozent und Wahrscheinlichkeit.html"
MAG = ka.MAG

# ---------------------------------------------------------------- Prüfung aller Zahlen
# Nr. 1 Münze dreimal
assert F(1, 2) ** 3 == F(1, 8) and 3 * F(1, 2) ** 3 == F(3, 8) and 1 - F(1, 8) == F(7, 8)
# Nr. 2 Kugeln 3 rot, 5 grün, gleichzeitig (ohne Zurücklegen)
assert F(3, 8) + F(5, 8) == 1 and F(2, 7) + F(5, 7) == 1 and F(3, 7) + F(4, 7) == 1
pk = {"rr": F(3, 8) * F(2, 7), "rg": F(3, 8) * F(5, 7), "gr": F(5, 8) * F(3, 7), "gg": F(5, 8) * F(4, 7)}
assert sum(pk.values()) == 1 and pk["rg"] + pk["gr"] == F(15, 28) and 1 - pk["gg"] == F(9, 14)
assert f"{float(F(15, 28)) * 100:.1f}" == "53.6" and f"{float(F(9, 14)) * 100:.1f}" == "64.3"
# Nr. 3
assert 360 / 1.2 == 300 and 80 * 0.75 * 0.8 == 48 and 1 - 48 / 80 == 0.4
# Nr. 4
assert 20000 * 0.55 == 11000 and 20000 * 0.30 == 6000 and 20000 * 0.15 == 3000 and 55 + 30 + 15 == 100
assert f"{11000 * 1.016 ** 6:.2f}" == "12099.15"
assert f"{3000 * 1.017 ** 5:.2f}" == "3263.82" and round((3263.82 / 3000) ** 0.2, 4) == 1.017
assert f"{6000 * 1.004 * 1.006 * 1.009:.2f}" == "6114.69"
# Nr. 5 Städte
assert 13750 / 12500 == 1.1 and 8400 * 0.95 == 7980 and 9240 / 1.12 == 8250 and 9240 - 8250 == 990 and 13750 - 12500 == 1250
# Nr. 6 Glücksrad (Winkel 180, 90, 60, 30)
w = [F(180, 360), F(90, 360), F(60, 360), F(30, 360)]
assert w == [F(1, 2), F(1, 4), F(1, 6), F(1, 12)] and sum(w) == 1 and sum(x * x for x in w) == F(25, 72) and 1 - F(11, 12) ** 2 == F(23, 144)
assert f"{float(F(25, 72)) * 100:.1f}" == "34.7" and f"{float(F(23, 144)) * 100:.1f}" == "16.0"
# Nr. 7 Würfelspiel: E = Σ P · Gewinn − Einsatz
E7 = F(1, 36) * 10 + F(5, 36) * 3 + F(30, 36) * 0 - 1
assert E7 == F(-11, 36) and f"{float(E7):.2f}" == "-0.31"
assert F(1, 36) * 21 + F(5, 36) * 3 - 1 == 0 and F(1, 36) * 12 + F(5, 36) * 3 - 1 == F(-1, 4)
# Nr. 8 Kugeln 2 gold, 3 blau, 5 weiß, zwei ohne Zurücklegen, Einsatz 1,50 €
pgg, pbb, pww = F(2, 10) * F(1, 9), F(3, 10) * F(2, 9), F(5, 10) * F(4, 9)
assert pgg == F(1, 45) and pbb == F(1, 15) and pww == F(2, 9) and pbb + pww == F(13, 45)
E8 = pgg * 18 + (pbb + pww) * 3 - F(3, 2)
assert F(1, 45) * 18 + F(13, 45) * 3 == F(19, 15) and E8 == F(-7, 30) and f"{float(E8):.2f}" == "-0.23" and round(float(E8) * 100, 2) == -23.33
GESAMT = 4 + 5 + 3 + 7 + 4 + 4 + 6 + 5
assert GESAMT == 38



# ---------------------------------------------------------------- Bausteine
def _kreis(f):
    innen = {"leer": "", "halb": '<path d="M8 1.5 A6.5 6.5 0 0 1 8 14.5 Z" fill="#1b1b1b"/>', "voll": '<circle cx="8" cy="8" r="6.5" fill="#1b1b1b"/>'}[f]
    return f'<svg class="kreis" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.6" fill="#fff" stroke="#1b1b1b" stroke-width="1.8"/>{innen}</svg>'


KREIS = [_kreis("leer"), _kreis("halb"), _kreis("voll")]


def balken(nr, stufe, punkte, text=""):
    return (f'<div class="balken"><b>Nr. {nr} &nbsp;<span class="kr">{KREIS[stufe]}</span></b><span class="pk">____ / {punkte}</span></div>'
            + (f'<p class="anw">{text}</p>' if text else ""))


def L(l, html):
    return f'<p class="lsg ltext">{html}</p>' if l else ""


def P_(t):
    return f' <span class="pkt">({t})</span>'


def kopf(l):
    return (f'<div class="kopfwrap"><table class="kopf">'
            '<tr><td colspan="2" class="titel"><u>Übungsklassenarbeit zur Klassenarbeit Nr. 1</u></td><td class="kl">Klasse 10</td></tr>'
            '<tr><td class="n">Name:</td><td colspan="2" class="n">Unterschrift:</td></tr>'
            f'<tr><td class="n">Punkte: <span class="pp">/ {GESAMT} Punkte</span></td><td class="n">Note:</td><td class="n">Ø</td></tr>'
            f'</table>{ka.WOLKE}</div>'
            + ('<p class="loesmark">Lösung mit Punkteverteilung</p>' if l else "")
            + '<div class="hinweis">Rechne im Heft: Aufgabe abschreiben, dann Schritt für Schritt rechnen. In der Arbeit gilt: Ohne Rechenweg keine Punkte.</div>')


THEMEN = [("Wahrscheinlichkeit: Münzen, Würfel, Glücksrad", "S. 140–142"),
          ("Baumdiagramm, mit und ohne Zurücklegen", "S. 144–146 (S. 145 Nr. 6, S. 146 Nr. 8)"),
          ("Erwartungswert, faires Spiel", "S. 147–149 · S. 154 Nr. 29, 31"),
          ("Prozentsatz, Prozentwert, Grundwert, Kreisdiagramme", "Aufgabenblatt „Prozent Wdh 10b“"),
          ("Zinsen und Zinseszins", "S. 86–87 · S. 88–89 Nr. 1–4"),
          ("Zinssatz gesucht, Anfangskapital gesucht", "S. 89 Nr. 5–7 und A · S. 90 Nr. 8, 10"),
          ("Wechselnde Zinssätze, Angebote vergleichen", "S. 100–101 (zwei Banken) · kommt in Woche 5"),
          ("Mehr üben: Abschlussprüfungen (Prüfungsarchiv)",
           "Wahrsch.: 2015 P4, 2021 A1/3a, 2022 B/3a, 2023 A1/2 · Erwartungswert: 2012 W4a, 2013 W4a, 2017 W4a · Prozent: 2016 P8, 2018 P4, 2019 P4, 2020 P7 · Zins: 2013 P6")]


def themen():
    return ('<table class="themen"><tr><th>Das kommt in der Klassenarbeit dran</th><th>Hier übst du im Buch (Schnittpunkt 10)</th></tr>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in THEMEN)
            + '<tr><td colspan="2" class="tipp">Tipp: Teil A1 ohne Taschenrechner (Nr. 1 bis 3). Die Buchlösungen findest du im Lösungsheft.</td></tr></table>')


# ---------------------------------------------------------------- Grafiken (schwarz-weiß für den Druck)
def _bruch(x, y, z, n, f=15, c="#1b1b1b"):
    return (f'<text x="{x}" y="{y - 3}" font-size="{f}" text-anchor="middle" fill="{c}">{z}</text>'
            f'<line x1="{x - 12}" y1="{y + 1}" x2="{x + 12}" y2="{y + 1}" stroke="{c}" stroke-width="1.3"/>'
            f'<text x="{x}" y="{y + f - 1}" font-size="{f}" text-anchor="middle" fill="{c}">{n}</text>')


def baum(l):
    """Baumdiagramm 3 rote (○), 5 grüne (●) Kugeln, zwei gleichzeitig. Drei Werte fehlen (in der Lösung pink)."""
    o = ['<svg class="baum" viewBox="0 0 460 250" font-family="Arial, sans-serif">']

    def kugel(x, y, schwarz):
        o.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{"#1b1b1b" if schwarz else "#fff"}" stroke="#1b1b1b" stroke-width="2"/>')

    def ast(x0, y0, x1, y1, z, n, links, fehlt=False):
        o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#1b1b1b" stroke-width="1.6"/>')
        mx, my = (x0 + x1) / 2 + (-26 if links else 26), (y0 + y1) / 2
        o.append(f'<rect x="{mx - 18}" y="{my - 16}" width="36" height="36" fill="#fff" stroke="#1b1b1b" stroke-width="1.2"/>')
        if not fehlt:
            o.append(_bruch(mx, my + 1, z, n, 14))
        elif l:
            o.append('<g class="lsg">' + _bruch(mx, my + 1, z, n, 14, MAG) + '</g>')

    ast(230, 8, 120, 85, 3, 8, True)
    ast(230, 8, 340, 85, 5, 8, False, True)
    kugel(120, 98, False)
    kugel(340, 98, True)
    ast(120, 111, 55, 190, 2, 7, True)
    ast(120, 111, 185, 190, 5, 7, False, True)
    ast(340, 111, 275, 190, 3, 7, True, True)
    ast(340, 111, 405, 190, 4, 7, False)
    for x1, s in zip((55, 185, 275, 405), (False, True, False, True)):
        kugel(x1, 205, s)
    o.append("</svg>")
    return "".join(o)


def torte(teile, titel, r=56, breite=260):
    """teile: [(Prozent, Beschriftung, Füllung, Schriftfarbe)]"""
    cx, cy = breite / 2, 98
    o = [f'<svg class="torte" viewBox="0 0 {breite} 205" font-family="Arial, sans-serif">',
         f'<text x="{cx}" y="16" font-size="13" font-weight="700" text-anchor="middle">{titel}</text>']
    w = -90.0
    for p, name, fill, tc in teile:
        a0, a1 = math.radians(w), math.radians(w + 3.6 * p)
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        gross = 1 if p > 50 else 0
        o.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {gross} 1 {x1:.1f},{y1:.1f} Z" fill="{fill}" stroke="#1b1b1b" stroke-width="1.6"/>')
        am = (a0 + a1) / 2
        o.append(f'<text x="{cx + r * 0.62 * math.cos(am):.1f}" y="{cy + r * 0.62 * math.sin(am) + 5:.1f}" font-size="13" font-weight="700" fill="{tc}" text-anchor="middle">{p} %</text>')
        lx, ly = cx + (r + 12) * math.cos(am), cy + (r + 12) * math.sin(am)
        anker = "start" if math.cos(am) > 0.15 else ("end" if math.cos(am) < -0.15 else "middle")
        o.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" font-size="11.5" text-anchor="{anker}">{name}</text>')
        w += 3.6 * p
    o.append("</svg>")
    return "".join(o)


def rad_winkel():
    """Glücksrad mit ungleich großen Sektoren, Mittelpunktswinkel 180°, 90°, 60°, 30°."""
    cx = cy = 100
    r = 80
    teile = [(180, "rot", "#1b1b1b", "#fff"), (90, "blau", "#b4b4b4", "#000"), (60, "gelb", "#ffffff", "#000"), (30, "grün", "#6e6e6e", "#fff")]
    o = ['<svg class="rad" viewBox="0 0 200 215" font-family="Arial, sans-serif">']
    w = -90.0
    for g, name, fill, tc in teile:
        a0, a1 = math.radians(w), math.radians(w + g)
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        o.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {1 if g > 180 else 0} 1 {x1:.1f},{y1:.1f} Z" fill="{fill}" stroke="#1b1b1b" stroke-width="2"/>')
        am = math.radians(w + g / 2)
        rr = 0.62 * r if g > 40 else 0.74 * r
        o.append(f'<text x="{cx + rr * math.cos(am):.1f}" y="{cy + rr * math.sin(am) + 4:.1f}" font-size="{13 if g > 40 else 10}" font-weight="700" fill="{tc}" text-anchor="middle">{g}°</text>')
        w += g
    o.append('<path d="M100,12 L88,-2 L112,-2 Z" fill="#fff" stroke="#1b1b1b" stroke-width="2" transform="translate(0,8)"/>')
    o.append('<circle cx="100" cy="100" r="4" fill="#fff" stroke="#1b1b1b" stroke-width="2"/></svg>')
    return "".join(o)


# ---------------------------------------------------------------- Seiten
def seite1(l):
    return (kopf(l) + themen()
            + '<div class="teil">Teil A1 · ohne Taschenrechner</div>'
            + balken(1, 0, 4, "Eine Münze wird dreimal nacheinander geworfen (K = Kopf, Z = Zahl).")
            + '<p class="anw">a) Wie groß ist die Wahrscheinlichkeit für dreimal Kopf?<br>'
              'b) Wie groß ist die Wahrscheinlichkeit, dass genau zweimal Zahl fällt?<br>'
              'c) Wie groß ist die Wahrscheinlichkeit, dass mindestens einmal Kopf fällt?</p>'
            + L(l, f"a) P(K, K, K) = {br(1, 2)} · {br(1, 2)} · {br(1, 2)} = {br(1, 8)}" + P_("1 P")
                + f"<br>b) Pfade mit genau zwei Z: ZZK, ZKZ, KZZ. Jeder hat die Wahrscheinlichkeit {br(1, 8)}, also P = 3 · {br(1, 8)} = {br(3, 8)} = 37,5 %" + P_("2 P")
                + f"<br>c) Gegenereignis „dreimal Zahl“: P = 1 − {br(1, 8)} = {br(7, 8)} = 87,5 %" + P_("1 P")))


def seite2(l):
    return (balken(2, 1, 5, "In einem Beutel liegen 3 rote (○) und 5 grüne (●) Kugeln. Es werden zwei Kugeln gleichzeitig gezogen. "
                              "Im Baumdiagramm fehlen drei Wahrscheinlichkeiten.")
            + '<div class="baumzeile">' + baum(l) + '</div>'
            + '<p class="anw">a) Ergänze die drei fehlenden Wahrscheinlichkeiten im Baumdiagramm.<br>'
              'b) Mit welcher Wahrscheinlichkeit haben die beiden Kugeln unterschiedliche Farben?<br>'
              'c) Mit welcher Wahrscheinlichkeit ist mindestens eine der beiden Kugeln rot?</p>'
            + L(l, f"a) {br(5, 8)}, {br(5, 7)} und {br(3, 7)}. Die Wahrscheinlichkeiten an einem Verzweigungspunkt ergeben zusammen 1; es wird ohne Zurücklegen gezogen, deshalb 7 im Nenner." + P_("1 P")
                + f"<br>b) P(○, ●) + P(●, ○) = {br(3, 8)} · {br(5, 7)} + {br(5, 8)} · {br(3, 7)} = {br(15, 56)} + {br(15, 56)} = {br(30, 56)} = {br(15, 28)} ≈ 53,6 %" + P_("2 P")
                + f"<br>c) Gegenereignis „zweimal grün“: P = 1 − {br(5, 8)} · {br(4, 7)} = 1 − {br(20, 56)} = {br(36, 56)} = {br(9, 14)} ≈ 64,3 %" + P_("2 P"))
            + balken(3, 1, 3, "")
            + '<p class="anw">a) Ein Handy wurde um 20 % teurer und kostet jetzt 360 €. Wie viel Euro hat es vorher gekostet?</p>'
            + L(l, "a) 120 % ≙ 360 € → 1 % ≙ 3 € → <u>100 %</u> ≙ 300 €. (Der alte Preis ist das 100 %.) Formel: 360 € : 1,2 = 300 €" + P_("1 P"))
            + '<p class="anw">b) Ein Paar Sneaker kostet 80 €. Der Preis wird erst um 25 % gesenkt. Danach wird der neue Preis nochmals um 20 % gesenkt. '
              'Marie sagt: „Die Sneaker sind jetzt insgesamt 45 % billiger.“ Hat sie recht? Begründe mit einer Rechnung.</p>'
            + L(l, "b) <u>100 %</u> ≙ 80 € → 75 % ≙ 60 €; <u>neues 100 %</u> ≙ 60 € → 80 % ≙ 48 €. "
                   "Gespart 32 €: <u>100 %</u> ≙ 80 € → 1 % ≙ 0,80 € → 32 € ≙ 40 %. Marie hat nicht recht: Die zweite Senkung rechnet vom neuen 100 % (60 €), "
                   "deshalb dürfen die Prozentsätze nicht addiert werden. Formel: 80 € · 0,75 · 0,8 = 48 €" + P_("2 P")))


def seite3(l):
    return ('<div class="teil">Teil 2 · mit Taschenrechner</div>'
            + balken(4, 1, 7, "Herr Berg erbt 20 000 € und verteilt das Geld nach dem Kreisdiagramm auf drei Anlagen.")
            + '<div class="saeulzeile">'
            + torte([(55, "Festgeld", "#b4b4b4", "#000"), (30, "Tagesgeld", "#ffffff", "#000"), (15, "Sparbrief", "#1b1b1b", "#fff")], "Aufteilung der 20 000 €", 52, 300)
            + '<div class="radtext"><p>a) Wie viel Euro legt er in Festgeld, Tagesgeld und Sparbrief an?</p>'
              '<p>b) Das Festgeld wird 6 Jahre lang mit 1,6 % verzinst, die Zinsen werden mitverzinst. Wie hoch ist das Kapital dann?</p>'
              '<p>c) Der Sparbrief wächst in 5 Jahren auf 3 263,82 €. Welcher Zinssatz gilt (gleichbleibend)?</p>'
              '<p>d) Beim Tagesgeld gelten 0,4 %, 0,6 % und 0,9 % in den drei Jahren. Wie viel Euro sind nach 3 Jahren darauf?</p></div></div>'
            + L(l, "a) <u>100 %</u> ≙ 20 000 € → 1 % ≙ 200 € → 55 % ≙ 11 000 € (Festgeld), 30 % ≙ 6 000 € (Tagesgeld), 15 % ≙ 3 000 € (Sparbrief)" + P_("1 P")
                + "<br>b) K₆ = 11 000 · 1,016⁶ ≈ 12 099,15 €" + P_("2 P")
                + "<br>c) q⁵ = 3 263,82 : 3 000 ≈ 1,0879 → q = ⁵√1,0879 ≈ 1,017, also p % = 1,7 %" + P_("2 P")
                + "<br>d) K₃ = 6 000 · 1,004 · 1,006 · 1,009 ≈ 6 114,69 €" + P_("2 P"))
            + balken(5, 1, 4, "Die Tabelle zeigt die Einwohnerzahlen von drei Städten. Von jeder Stadt fehlt eine Angabe.")
            + '<table class="angebot staedte"><tr><th>Stadt</th><th>Einwohner 2010</th><th>Veränderung</th><th>Einwohner 2020</th></tr>'
              f'<tr><td>Altdorf</td><td>12 500</td><td>?</td><td>13 750</td></tr>'
              f'<tr><td>Bergheim</td><td>8 400</td><td>−5 %</td><td>?</td></tr>'
              f'<tr><td>Cella</td><td>?</td><td>+12 %</td><td>9 240</td></tr></table>'
            + '<p class="anw">a) Um wie viel Prozent hat Altdorf zugenommen?<br>'
              'b) Wie viele Einwohner hatte Bergheim im Jahr 2020?<br>'
              'c) Wie viele Einwohner hatte Cella im Jahr 2010?<br>'
              'd) Eine Zeitung schreibt: „Altdorf ist am stärksten gewachsen, denn dort sind die meisten Einwohner dazugekommen.“ '
              'Vergleiche Altdorf und Cella. Stimmt die Aussage für die prozentuale Zunahme?</p>'
            + L(l, "a) <u>100 %</u> ≙ 12 500 → 1 % ≙ 125 → 13 750 ≙ 110 %, also +10 % (13 750 : 12 500 = 1,1)" + P_("1 P")
                + "<br>b) <u>100 %</u> ≙ 8 400 → 1 % ≙ 84 → 95 % ≙ 7 980 Einwohner (8 400 · 0,95)" + P_("1 P")
                + "<br>c) 112 % ≙ 9 240 → 1 % ≙ 82,5 → <u>100 %</u> ≙ 8 250 Einwohner (9 240 : 1,12)" + P_("1 P")
                + "<br>d) Altdorf: +1 250 (+10 %), Cella: +990 (+12 %). Absolut liegt Altdorf vorn, prozentual Cella. Die Aussage stimmt nur absolut." + P_("1 P")))


def seite4(l):
    return (balken(6, 2, 4, "Ein Glücksrad hat vier Sektoren mit den Mittelpunktswinkeln 180° (rot), 90° (blau), 60° (gelb) und 30° (grün). "
                              "Es wird zweimal gedreht.")
            + '<div class="radzeile">' + rad_winkel()
            + '<div class="radtext"><p>a) Gib für jede Farbe die Wahrscheinlichkeit als Bruch an.</p>'
              '<p>b) Wie groß ist die Wahrscheinlichkeit, dass beide Drehungen dieselbe Farbe ergeben?</p>'
              '<p>c) Wie groß ist die Wahrscheinlichkeit, dass mindestens einmal grün erscheint?</p></div></div>'
            + L(l, f"a) rot {br(180, 360)} = {br(1, 2)}; blau {br(1, 4)}; gelb {br(1, 6)}; grün {br(1, 12)}" + P_("1 P")
                + f"<br>b) P = {br(1, 2)}² + {br(1, 4)}² + {br(1, 6)}² + {br(1, 12)}² = {br(1, 4)} + {br(1, 16)} + {br(1, 36)} + {br(1, 144)} = {br(50, 144)} = {br(25, 72)} ≈ 34,7 %" + P_("2 P")
                + f"<br>c) Gegenereignis „kein grün“: P = 1 − {br(11, 12)}² = 1 − {br(121, 144)} = {br(23, 144)} ≈ 16,0 %" + P_("1 P"))
            + balken(7, 2, 6, "Bei einem Würfelspiel werden zwei Würfel gleichzeitig geworfen. Der Einsatz pro Spiel beträgt 1,00 €.")
            + '<table class="angebot lose"><tr><th>Ergebnis</th><th>Gewinn (Auszahlung)</th></tr>'
              '<tr><td>zweimal die 6</td><td>10,00 €</td></tr><tr><td>anderer Pasch (zwei gleiche Zahlen)</td><td>3,00 €</td></tr>'
              '<tr><td>alle anderen Ergebnisse</td><td>kein Gewinn</td></tr></table>'
            + '<p class="anw">a) Berechne den Erwartungswert (Gewinn pro Spiel aus Sicht des Spielers, Einsatz abziehen).<br>'
              'b) Das Spiel soll fair werden. Dazu soll nur der Gewinn für „zweimal die 6“ geändert werden. Wie hoch muss er sein?<br>'
              'c) Der Veranstalter möchte pro Spiel durchschnittlich 0,25 € verdienen. Dazu ändert er nur den Gewinn für „zweimal die 6“. Wie hoch muss er dann sein?</p>'
            + L(l, f"a) P(zweimal 6) = {br(1, 36)}, P(anderer Pasch) = {br(5, 36)}, P(sonst) = {br(30, 36)}. "
                   f"E = {br(1, 36)} · 10 € + {br(5, 36)} · 3 € + {br(30, 36)} · 0 € − 1,00 € = {br(25, 36)} € − 1,00 € = −{br(11, 36)} € ≈ −0,31 € (der Spieler verliert im Mittel 0,31 € pro Spiel)" + P_("2 P")
                + f"<br>b) Fair: E = 0. {br(1, 36)} · x + {br(5, 36)} · 3 € − 1,00 € = 0 → x + 15 = 36 → x = 21 €" + P_("2 P")
                + f"<br>c) Der Veranstalter verdient 0,25 €, also E = −0,25 €. {br(1, 36)} · x + {br(5, 36)} · 3 € − 1,00 € = −0,25 € → x + 15 = 27 → x = 12 €" + P_("2 P")))


def seite5(l):
    return (balken(8, 2, 5, "Beim Sommerfest gibt es ein Kugelspiel. Im Beutel liegen 2 goldene, 3 blaue und 5 weiße Kugeln. "
                            "Der Spieler zieht zwei Kugeln nacheinander ohne Zurücklegen. Der Einsatz pro Spiel beträgt 1,50 €.")
            + '<table class="angebot lose"><tr><th>Ergebnis</th><th>Gewinn (Auszahlung)</th></tr>'
              '<tr><td>zweimal gold</td><td>18,00 €</td></tr><tr><td>zwei blaue oder zwei weiße Kugeln</td><td>3,00 €</td></tr>'
              '<tr><td>alle anderen Ergebnisse</td><td>kein Gewinn</td></tr></table>'
            + '<p class="anw">a) Berechne die Wahrscheinlichkeiten der drei Ergebnisse und den Erwartungswert (Einsatz abziehen).<br>'
              'b) Wie hoch dürfte der Einsatz höchstens sein, damit das Spiel für den Spieler nicht ungünstig ist?<br>'
              'c) Tim sagt: „Wenn ich 100 Spiele spiele, verliere ich etwa 25 €.“ Hat er recht? Begründe mit deinem Ergebnis aus a).</p>'
            + L(l, f"a) P(gold, gold) = {br(2, 10)} · {br(1, 9)} = {br(1, 45)}; P(blau, blau) = {br(3, 10)} · {br(2, 9)} = {br(1, 15)}; P(weiß, weiß) = {br(5, 10)} · {br(4, 9)} = {br(2, 9)}. "
                   f"Zwei gleiche (nicht gold): {br(1, 15)} + {br(2, 9)} = {br(13, 45)}. P(sonst) = {br(31, 45)}" + P_("2 P")
                + f"<br>E = {br(1, 45)} · 18 € + {br(13, 45)} · 3 € + {br(31, 45)} · 0 € − 1,50 € = {br(19, 15)} € − 1,50 € = −{br(7, 30)} € ≈ −0,23 €" + P_("1 P")
                + f"<br>b) Nicht ungünstig heißt E ≥ 0. Die mittlere Auszahlung beträgt {br(19, 15)} € ≈ 1,27 €. Der Einsatz dürfte höchstens 1,27 € betragen." + P_("1 P")
                + "<br>c) 100 · (−0,23 €) ≈ −23 €. Tim verliert im Mittel etwa 23 €, also ungefähr, aber nicht genau 25 €. Seine Aussage stimmt etwa, ist aber ungenau." + P_("1 P"))
            + '<div class="legende">' + f'{KREIS[0]} leicht &nbsp;&nbsp; {KREIS[1]} mittel &nbsp;&nbsp; {KREIS[2]} schwer</div>')


SEITEN = [seite1, seite2, seite3, seite4, seite5]

EXTRA = """<style>
.kr{font-weight:400}.kreis{width:1.2em;height:1.2em;vertical-align:-.25em}
.lsg{color:#E6007E;font-weight:700}.lsg.kl{font-size:11.5pt}
.ltext{font-size:12.5pt;line-height:1.5;margin:1mm 0 2mm}
.themen{width:100%;border-collapse:collapse;font-size:10.5pt;margin:0 0 3mm}
.themen th{background:#c8c8c8;border:.6pt solid #555;padding:1.3mm 3mm;text-align:left}
.themen td{border:.6pt solid #555;padding:1.1mm 3mm}.themen td.tipp{font-size:10pt;font-style:italic}
.teil{font-weight:700;font-size:13pt;text-decoration:underline;margin:3mm 0 1mm}
.radzeile,.saeulzeile{display:flex;gap:8mm;align-items:center;margin:1mm 0 2mm}
.rad{width:52mm;flex:none}.saeulzeile .torte{width:76mm;flex:none}
.radtext{font-size:12.5pt;line-height:1.4}.radtext p{margin:0 0 2.5mm}
.baumzeile{display:flex;justify-content:center;margin:1mm 0 2mm}.baum{width:122mm}
.angebot{border-collapse:collapse;font-size:12.5pt;margin:2mm 0 2mm}
.angebot th{background:#c8c8c8;border:.6pt solid #555;padding:1.6mm 4mm;text-align:left}
.angebot td{border:.6pt solid #555;padding:2mm 4mm;line-height:1.5;vertical-align:top}
.angebot.lose td:first-child{min-width:78mm}
.staedte td,.staedte th,.lose td,.lose th{padding:1mm 4mm}
.saeulzeile .radtext p{margin:0 0 1.6mm}
.saeulzeile .radtext{font-size:12pt;line-height:1.3}
.legende{margin-top:auto;font-size:11pt;color:#555}
</style>"""


def teil(l):
    return "".join(f'<section class="seite">{s(l)}<div class="snr">Seite {i + 1} von {len(SEITEN)}</div></section>' for i, s in enumerate(SEITEN))


def druckfassung(l):
    return ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Mathe 10b – Übungsklassenarbeit Nr. 1 Prozent und Wahrscheinlichkeit</title>'
            + ka.CSS + EXTRA + '</head><body>' + teil(l) + '</body></html>'), len(SEITEN)


def main():
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Mathe 10b – Übungsklassenarbeit Nr. 1 Prozent und Wahrscheinlichkeit</title>' + ka.CSS + EXTRA + '</head><body>'
            f'<div class="leiste"><b>Übungsklassenarbeit · Klasse 10b</b><a href="#arbeit">Aufgaben ({len(SEITEN)} Seiten)</a><a href="#loesung">Lösung ({len(SEITEN)} Seiten)</a>'
            f'<span>{GESAMT} Punkte · Rechnen im Heft · Entwurf</span></div>'
            '<div class="trenner" id="arbeit">Aufgaben</div>' + teil(False)
            + '<div class="trenner" id="loesung">Lösung</div>' + teil(True) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name, GESAMT, "Punkte")


if __name__ == "__main__":
    main()
