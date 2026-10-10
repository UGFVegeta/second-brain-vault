#!/usr/bin/env python3
"""Mathe 10b – Übungsklassenarbeit zu KA 1 (Prozent, Zinsen, Wahrscheinlichkeit).
Gleiches Layout wie die Übungs-KA der 7c: Kopf, Tabelle "Das kommt dran | Hier übst du", Schwierigkeitskreise,
Rechnen im Heft. Danach dieselben Seiten als Lösung (pink ausgefüllt). Alle Zahlen werden unten geprüft."""
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
# Nr. 1
assert F(3, 6) * F(3, 6) == F(1, 4)
assert sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7) == 6 and F(6, 36) == F(1, 6)
# Nr. 2 (3 weiße, 7 schwarze Kugeln, ohne Zurücklegen)
assert F(7, 10) * F(6, 9) == F(7, 15) and F(3, 10) * F(2, 9) == F(1, 15) and round(float(F(1, 15)) * 100, 2) == 6.67
assert F(3, 10) * F(7, 9) == F(7, 30) == F(7, 10) * F(3, 9)
# Nr. 3
assert 90 / 120 == 0.75 and 80 * 0.75 * 0.8 == 48 and 1 - 48 / 80 == 0.4
# Nr. 4
K0, P = 8000, (0.8, 1.2, 1.6)
K3 = K0 * math.prod(1 + p / 100 for p in P)
q4 = 8500 / K3
assert f"{K3:.2f}" == "8291.34" and f"{(q4 - 1) * 100:.2f}" == "2.52"
q_m = (8500 / 8000) ** 0.25
assert f"{(q_m - 1) * 100:.2f}" == "1.53"
# Nr. 5
A = 15000 * math.prod(1 + p / 100 for p in (0.9, 1.2, 1.5, 2.1))
B4 = 15000 * 1.014 ** 4
B = B4 * 1.005
assert f"{A:.2f}" == "15872.84" and f"{B4:.2f}" == "15857.81" and f"{B4 * 0.005:.2f}" == "79.29" and f"{B:.2f}" == "15937.09"
assert f"{B - A:.2f}" == "64.25"
# Nr. 6
assert 48000 * 0.20 == 9600 and 9600 * 0.55 == 5280 and 5280 / 48000 == 0.11 and 48000 * 0.22 == 10560 and 2640 / 10560 == 0.25 and 2640 / 48000 == 0.055
# Nr. 7
assert F(9, 25) * F(8, 24) == F(3, 25) and F(15, 25) * F(14, 24) == F(7, 20) and 5 + 3 == 8
assert round(2 * 0.32 * 0.68, 4) == 0.4352
# Nr. 8
assert 200 + 10 * 20 + 100 * 3 == 700 and round(700 / 600, 2) == 1.17 and 600 * 1.5 == 900 and (900 - 200 - 200) / 100 == 5 and 600 * 1.0 - 200 - 300 == 100
GESAMT = 4 + 4 + 3 + 6 + 4 + 4 + 5 + 6
assert GESAMT == 36


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


THEMEN = [("Wahrscheinlichkeit: Glücksrad, Augensumme", "S. 140–142"),
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
def gluecksrad():
    cx = cy = 100
    r = 82
    fills = ["#1b1b1b", "#b4b4b4", "#1b1b1b", "#b4b4b4", "#ffffff", "#b4b4b4"]
    texte = ["#fff", "#000", "#fff", "#000", "#000", "#000"]
    o = ['<svg class="rad" viewBox="0 0 200 215" font-family="Arial, sans-serif">']
    for i in range(6):
        a0, a1 = math.radians(-90 + 60 * i), math.radians(-90 + 60 * (i + 1))
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        o.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z" fill="{fills[i]}" stroke="#1b1b1b" stroke-width="2"/>')
        am = (a0 + a1) / 2
        o.append(f'<text x="{cx + 52 * math.cos(am):.1f}" y="{cy + 52 * math.sin(am) + 8:.1f}" font-size="24" font-weight="700" fill="{texte[i]}" text-anchor="middle">{i + 1}</text>')
    o.append('<path d="M100,12 L88,-2 L112,-2 Z" fill="#fff" stroke="#1b1b1b" stroke-width="2" transform="translate(0,8)"/>')
    o.append('<circle cx="100" cy="100" r="4" fill="#fff" stroke="#1b1b1b" stroke-width="2"/></svg>')
    return "".join(o)


def _bruch(x, y, z, n, f=15, c="#1b1b1b"):
    return (f'<text x="{x}" y="{y - 3}" font-size="{f}" text-anchor="middle" fill="{c}">{z}</text>'
            f'<line x1="{x - 12}" y1="{y + 1}" x2="{x + 12}" y2="{y + 1}" stroke="{c}" stroke-width="1.3"/>'
            f'<text x="{x}" y="{y + f - 1}" font-size="{f}" text-anchor="middle" fill="{c}">{n}</text>')


def baum():
    o = ['<svg class="baum" viewBox="0 0 460 250" font-family="Arial, sans-serif">']

    def kugel(x, y, schwarz):
        o.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{"#1b1b1b" if schwarz else "#fff"}" stroke="#1b1b1b" stroke-width="2"/>')

    def ast(x0, y0, x1, y1, z, n, links):
        o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#1b1b1b" stroke-width="1.6"/>')
        mx, my = (x0 + x1) / 2 + (-26 if links else 26), (y0 + y1) / 2
        o.append(f'<rect x="{mx - 18}" y="{my - 16}" width="36" height="36" fill="#fff" stroke="#1b1b1b" stroke-width="1.2"/>')
        o.append(_bruch(mx, my + 1, z, n, 14))

    ast(230, 8, 120, 85, 3, 10, True)
    ast(230, 8, 340, 85, 7, 10, False)
    kugel(120, 98, False)
    kugel(340, 98, True)
    for (x0, xs, zs) in ((120, (55, 185), ((2, 9), (7, 9))), (340, (275, 405), ((3, 9), (6, 9)))):
        for j, (x1, (z, n)) in enumerate(zip(xs, zs)):
            ast(x0, 111, x1, 190, z, n, j == 0)
    for x1, s in zip((55, 185, 275, 405), (False, True, False, True)):
        kugel(x1, 205, s)
    o.append("</svg>")
    return "".join(o)


def saeulen():
    o = ['<svg class="saeulen" viewBox="0 0 330 190" font-family="Arial, sans-serif">',
         '<polygon points="6,168 322,168 300,184 28,184" fill="#8a8a8a"/>']
    for i, (h, t) in enumerate(((38, "0,8 %"), (46, "1,2 %"), (56, "1,6 %"), (110, "?"))):
        x = 22 + i * 76
        o.append(f'<rect x="{x}" y="{168 - h}" width="42" height="{h}" fill="#fff" stroke="#1b1b1b" stroke-width="2"/>')
        o.append(f'<text x="{x + 21}" y="{168 - h + 24}" font-size="{26 if t == "?" else 14}" font-weight="700" text-anchor="middle">{t}</text>')
        o.append(f'<text x="{x + 21}" y="181" font-size="11" text-anchor="middle">{i + 1}. Jahr</text>')
    o.append('<text x="164" y="14" font-size="13" text-anchor="middle" font-style="italic">Zinsen werden mitverzinst.</text></svg>')
    return "".join(o)


def torte(teile, titel, r=56):
    """teile: [(Prozent, Beschriftung, Füllung, Schriftfarbe)]"""
    cx, cy = 130, 98
    o = [f'<svg class="torte" viewBox="0 0 260 205" font-family="Arial, sans-serif">',
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


def kaestchen(l, text):
    return f'<span class="kast breit">{text if l else ""}</span>'


# ---------------------------------------------------------------- Seiten
def seite1(l):
    return (kopf(l) + themen()
            + '<div class="teil">Teil A1 · ohne Taschenrechner</div>'
            + balken(1, 0, 4, "Die sechs Sektoren des Glücksrads sind gleich groß. Sie sind schwarz, grau oder weiß gefärbt und mit den Zahlen 1 bis 6 beschriftet. "
                              "Das Glücksrad wird zweimal gedreht.")
            + '<div class="radzeile">' + gluecksrad()
            + '<div class="radtext"><p>a) Wie groß ist die Wahrscheinlichkeit, dass das Glücksrad zweimal auf einem grauen Feld stehen bleibt?</p>'
              '<p>b) Die Zahlen der beiden angezeigten Felder werden addiert. Berechne die Wahrscheinlichkeit für die Summe 7.</p></div></div>'
            + L(l, f"a) 3 graue Felder von 6: P(grau) = {br(1, 2)}. P(grau, grau) = {br(1, 2)} · {br(1, 2)} = {br(1, 4)} = 25 %" + P_("2 P")
                + f"<br>b) Paare mit Summe 7: (1|6), (2|5), (3|4), (4|3), (5|2), (6|1), das sind 6 von 36 Möglichkeiten. P = {br(6, 36)} = {br(1, 6)} ≈ 16,7 %" + P_("2 P")))


def seite2(l):
    stm = [("Es handelt sich um einen Zufallsversuch mit Zurücklegen.", "falsch",
            "Nach der ersten Kugel steht im zweiten Zug der Nenner 9 statt 10. Es wird also ohne Zurücklegen gezogen."),
           (f"P(●, ●) = {br(7, 15)}", "richtig", f"P(●, ●) = {br(7, 10)} · {br(6, 9)} = {br(42, 90)} = {br(7, 15)}"),
           ("P(○, ○) = 0,0667 %", "falsch", f"P(○, ○) = {br(3, 10)} · {br(2, 9)} = {br(6, 90)} = {br(1, 15)} ≈ 0,0667 = 6,67 %. Das Prozentzeichen stimmt nicht."),
           ("P(○, ●) ist genauso groß wie P(●, ○).", "richtig", f"P(○, ●) = {br(3, 10)} · {br(7, 9)} = {br(7, 30)} und P(●, ○) = {br(7, 10)} · {br(3, 9)} = {br(7, 30)}")]
    zeilen = "".join(
        f'<div class="aussage"><span class="kast kl2">{"✗" if (l and r == "richtig") else ""}</span> {t}'
        + (f'<br><span class="lsg kl">→ {r}: {b}</span>' if l else "") + "</div>"
        for t, r, b in stm)
    return (balken(2, 1, 4, "Welche Aussagen passen zu diesem Baumdiagramm? Kreuze die zutreffenden Aussagen an. Begründe rechnerisch, auch bei den falschen Aussagen.")
            + '<div class="baumzeile">' + baum() + '</div>' + f'<div class="aussagen">{zeilen}</div>'
            + L(l, "je 1 P: Aussagen 2 und 4 sind zutreffend. In der Arbeit zählt die Begründung mit.")
            + balken(3, 1, 3, "Eine Jacke kostet 120 €. Im Schlussverkauf kostet sie nur noch 90 €.")
            + '<p class="anw">a) Um wie viel Prozent wurde der Preis gesenkt?</p>'
            + L(l, f"a) 90 : 120 = 0,75, also wurde der Preis um 25 % gesenkt." + P_("1 P"))
            + '<p class="anw">b) Ein Paar Sneaker kostet 80 €. Der Preis wird erst um 25 % gesenkt. Danach wird der neue Preis nochmals um 20 % gesenkt. '
              'Marie sagt: „Die Sneaker sind jetzt insgesamt 45 % billiger.“ Hat sie recht? Begründe mit einer Rechnung.</p>'
            + L(l, "b) 80 € · 0,75 = 60 €; 60 € · 0,8 = 48 €. Gespart: 32 € von 80 € = 40 %. Marie hat nicht recht: Die Prozentsätze dürfen nicht addiert werden. "
                   "(Faktor 0,75 · 0,8 = 0,6)" + P_("2 P")))


def seite3(l):
    return ('<div class="teil">Teil 2 · mit Taschenrechner</div>'
            + balken(4, 1, 6, "Frau Aydin möchte 8 000,00 € für 4 Jahre anlegen. Für die ersten drei Jahre sind die Zinssätze fest, "
                              "über den Zinssatz im 4. Jahr will die Bank noch verhandeln. Die Zinsen werden mitverzinst.")
            + '<div class="saeulzeile">' + saeulen()
            + '<div class="radtext"><p>a) Wie groß ist das Kapital nach 3 Jahren?</p>'
              '<p>b) Nach 4 Jahren sollen es 8 500,00 € sein. Welchen Zinssatz müsste die Bank für das 4. Jahr anbieten?</p>'
              '<p>c) Bei welchem jährlich gleichbleibenden Zinssatz hätte sie nach 4 Jahren dasselbe Endkapital?</p></div></div>'
            + L(l, "a) K₃ = 8 000 · 1,008 · 1,012 · 1,016 ≈ 8 291,34 €" + P_("2 P")
                + "<br>b) q₄ = 8 500 : 8 291,34 ≈ 1,0252, also p % ≈ 2,52 %" + P_("2 P")
                + "<br>c) q⁴ = 8 500 : 8 000 = 1,0625 → q = ⁴√1,0625 ≈ 1,0153, also p % ≈ 1,53 %" + P_("2 P"))
            + balken(5, 1, 4, "Familie Wolf legt 15 000,00 € für 4 Jahre an und vergleicht zwei Angebote. Zinsen werden mitverzinst.")
            + '<table class="angebot"><tr><th>Opti-Bank</th><th>Plus-Bank</th></tr>'
              '<tr><td>1. Jahr: 0,9 %<br>2. Jahr: 1,2 %<br>3. Jahr: 1,5 %<br>4. Jahr: 2,1 %</td>'
              '<td>gleichbleibend 1,4 % für alle 4 Jahre<br>Zusätzlich: Bonus von 0,5 % des Endkapitals<br>nach Ablauf der 4 Jahre</td></tr></table>'
            + '<p class="anw">Für welches Angebot sollte sich Familie Wolf entscheiden? Begründe durch Rechnung.</p>'
            + L(l, "Opti-Bank: K₄ = 15 000 · 1,009 · 1,012 · 1,015 · 1,021 ≈ 15 872,84 €" + P_("1 P")
                + "<br>Plus-Bank: K₄ = 15 000 · 1,014⁴ ≈ 15 857,81 €; Bonus 0,5 % davon ≈ 79,29 €, zusammen ≈ 15 937,09 €" + P_("2 P")
                + "<br>Antwort: Die Plus-Bank ist um etwa 64,25 € besser." + P_("1 P")))


def seite4(l):
    teile_l = [(22, "unter 20", "#ffffff", "#000"), (58, "20 bis 64", "#b4b4b4", "#000"), (20, "ab 65", "#1b1b1b", "#fff")]
    teile_r = [(55, "Frauen", "#b4b4b4", "#000"), (45, "Männer", "#ffffff", "#000")]
    return (balken(6, 0, 4, "In der Stadt Neustadt leben 48 000 Einwohner. Das linke Diagramm zeigt die Altersgruppen. "
                            "Das rechte Diagramm zeigt, wie sich die Einwohner ab 65 Jahren auf Frauen und Männer verteilen.")
            + '<div class="tortenzeile">' + torte(teile_l, "Einwohner (48 000)") + torte(teile_r, "Einwohner ab 65") + "</div>"
            + '<p class="anw">a) Berechne, wie viele Einwohner 65 Jahre oder älter sind.<br>'
              'b) Berechne, wie viele Frauen ab 65 es in Neustadt gibt.<br>'
              'c) Wie viel Prozent aller Einwohner sind Frauen ab 65?<br>'
              'd) Im Stadtteil Nord leben 2 640 Einwohner unter 20 Jahren. Wie viel Prozent aller Einwohner der Stadt sind das?</p>'
            + L(l, "a) 20 % von 48 000 = 9 600" + P_("1 P") + "<br>b) 55 % von 9 600 = 5 280" + P_("1 P")
                + f"<br>c) 5 280 : 48 000 = 0,11 = 11 %" + P_("1 P") + "<br>d) 2 640 : 48 000 = 0,055 = 5,5 %" + P_("1 P"))
            + balken(7, 2, 5, "In einer Lern-App sind 25 Aufgaben gespeichert: 10 Prozentaufgaben, 9 Zinsaufgaben und 6 Wahrscheinlichkeitsaufgaben. "
                              "Die Hälfte der Prozentaufgaben und ein Drittel der Zinsaufgaben sind schwer, alle Wahrscheinlichkeitsaufgaben sind leicht. "
                              "Die App wählt zufällig zwei Aufgaben nacheinander aus.")
            + '<p class="anw"><b>Eine Aufgabe kommt nur einmal dran</b> (ohne Zurücklegen):<br>'
              'a) Wie groß ist die Wahrscheinlichkeit für zwei Zinsaufgaben?<br>'
              'b) Wie groß ist die Wahrscheinlichkeit, dass keine der beiden Aufgaben eine Prozentaufgabe ist?<br>'
              '<b>Eine Aufgabe darf noch einmal drankommen</b> (mit Zurücklegen):<br>'
              'c) Wie groß ist die Wahrscheinlichkeit, dass genau eine der beiden Aufgaben schwer ist?</p>'
            + L(l, f"a) {br(9, 25)} · {br(8, 24)} = {br(72, 600)} = 0,12 = 12 %" + P_("2 P")
                + f"<br>b) 15 von 25 sind keine Prozentaufgaben: {br(15, 25)} · {br(14, 24)} = {br(210, 600)} = 0,35 = 35 %" + P_("1 P")
                + f"<br>c) schwer: 5 + 3 = 8 von 25, also P(schwer) = 0,32. P = 2 · 0,32 · 0,68 = 0,4352 ≈ 43,5 %" + P_("2 P")))


def seite5(l):
    return (balken(8, 2, 6, "Beim Schulfest werden 600 Lose verkauft. Ein Los kostet 1,50 €. Es wird ein Los gezogen.")
            + '<table class="angebot lose"><tr><th>Verteilung der Lose</th><th>Wert des Gewinns</th></tr>'
              '<tr><td>1 Hauptgewinn</td><td>200 €</td></tr><tr><td>10 Gutscheine</td><td>je 20 €</td></tr>'
              '<tr><td>100 Trostpreise</td><td>je 3 €</td></tr><tr><td>restliche Lose sind Nieten</td><td>kein Gewinn</td></tr></table>'
            + '<p class="anw">a) Berechne den Erwartungswert (mittlere Auszahlung pro Los).<br>'
              'b) Das Spiel soll fair werden. Dazu soll nur der Wert der Trostpreise erhöht werden. Wie viel Euro müsste ein Trostpreis dann wert sein?<br>'
              'c) Der Veranstalter möchte pro Los im Durchschnitt 0,50 € verdienen. Dazu ändert er nur den Hauptgewinn. Wie hoch muss der Hauptgewinn sein?</p>'
            + L(l, f"a) E = (1 · 200 € + 10 · 20 € + 100 · 3 €) : 600 = 700 € : 600 ≈ 1,17 €. Im Mittel zahlt der Veranstalter 1,17 € pro Los aus und nimmt 1,50 € ein." + P_("2 P")
                + "<br>b) Fair heißt: E = 1,50 €. Das sind 600 · 1,50 € = 900 € Auszahlung insgesamt. 900 € − 200 € − 200 € = 500 €, geteilt durch 100 Trostpreise: 5 €." + P_("2 P")
                + "<br>c) Auszahlung im Mittel 1,00 € pro Los, das sind 600 € insgesamt. 600 € − 200 € − 300 € = 100 € für den Hauptgewinn." + P_("2 P"))
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
.rad{width:52mm;flex:none}.saeulen{width:84mm;flex:none}
.radtext{font-size:12.5pt;line-height:1.4}.radtext p{margin:0 0 2.5mm}
.baumzeile{display:flex;justify-content:center;margin:1mm 0 2mm}.baum{width:122mm}
.aussagen{display:grid;grid-template-columns:1fr 1fr;gap:3mm 6mm;margin:1mm 0 2mm;font-size:12pt}
.aussage{line-height:1.4}.kast.kl2{width:7mm;height:7mm;font-size:13pt;margin:0 1.5mm 0 0;vertical-align:-1.5mm}
.angebot{border-collapse:collapse;font-size:12.5pt;margin:2mm 0 2mm}
.angebot th{background:#c8c8c8;border:.6pt solid #555;padding:1.6mm 4mm;text-align:left}
.angebot td{border:.6pt solid #555;padding:2mm 4mm;line-height:1.5;vertical-align:top}
.angebot.lose td:first-child{min-width:68mm}
.tortenzeile{display:flex;justify-content:center;gap:4mm;margin:0 0 1mm}.torte{width:62mm}
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
            '<div class="leiste"><b>Übungsklassenarbeit · Klasse 10b</b><a href="#arbeit">Aufgaben (5 Seiten)</a><a href="#loesung">Lösung (5 Seiten)</a>'
            f'<span>{GESAMT} Punkte · Rechnen im Heft · Entwurf</span></div>'
            '<div class="trenner" id="arbeit">Aufgaben</div>' + teil(False)
            + '<div class="trenner" id="loesung">Lösung</div>' + teil(True) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name, GESAMT, "Punkte")


if __name__ == "__main__":
    main()
