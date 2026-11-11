#!/usr/bin/env python3
"""Mathe 10b – Klassenarbeit Nr. 1 NACHTERMIN (Prozent und Wahrscheinlichkeit): Lösung mit Punkten.
Vorlage: ../Klassenarbeit Nr. 1 – Lösung mit Punkten/baue_ka1_loesung_punkte.py (Layout und CSS übernommen).
Lösungstext hellblau, Punkte rot. Seite 1 = Teil A1 (ohne Taschenrechner), Seite 2 und 3 = Teil A2.
Punktsummen je Aufgabe laut Aufgabenblatt (A1 1 + 2 + 2, A2 3 + 3 + 3 + 5, zusammen 19 P);
die Verteilung innerhalb einer Aufgabe ist ein Vorschlag, keine Handlösung.
Aufruf: python3 baue_ka1_nachtermin_loesung_punkte.py   (schreibt HTML und PDF neben das Skript)"""
import subprocess
from fractions import Fraction as F
from pathlib import Path

from pypdf import PdfReader

HIER = Path(__file__).resolve().parent
NAME = "Mathe 10b – Klassenarbeit Nr. 1 Nachtermin Prozent und Wahrscheinlichkeit – Lösung mit Punkten"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ------------------------------------------------------------------ Zahlen prüfen
# 1: Netz hat 2, 3, 1 und drei leere Flächen -> 2, 2, 3 ergänzen
netz = [2, 3, 1, 2, 2, 3]
assert F(netz.count(2), 6) ** 2 == F(9, 36) and F(netz.count(3), 6) ** 2 == F(4, 36)
# 2: 50 Kugeln, 60 % schwarz
assert 50 * F(60, 100) == 30 and F(50, 10) == 5
assert F(30, 50) * F(20, 50) * 2 == F(1200, 2500) == F(12, 25) and F(12, 25) * 100 == 48
# 3: 300 € +20 %, dann -15 %
assert 300 * F(120, 100) == 360 and 360 * F(85, 100) == 306 and F(360, 100) == F(36, 10)
# 4: Plus-Bank
K0 = 5620.67 / (1.008 * 1.010 * 1.013)
assert f"{K0:.2f}" == "5450.00"
K2 = 5450 * 1.008 * 1.010
assert f"{K2:.2f}" == "5548.54" and f"{K2 * 0.013:.2f}" == "72.13" and f"{5450 * 1.008 * 1.010 * 1.013:.2f}" == "5620.67"
q = (5650 / 5450) ** (1 / 3)
assert round(q, 4) == 1.0121 and round(5450 * 1.0121 ** 3) == 5650
# 5: Lostrommel 5 × M, 3 × L, 2 × U (aus der Grafik gezählt), ohne Zurücklegen
assert 5 + 3 + 2 == 10
assert 1 - F(5, 10) * F(4, 9) == F(70, 90) == F(7, 9) and f"{7 / 9 * 100:.1f}" == "77.8"
assert F(8, 10) * F(7, 9) == F(56, 90) == F(28, 45) and f"{28 / 45 * 100:.1f}" == "62.2"
# 6: Onlinewerbung
assert 2082 + 547 + 3277 + 683 + 895 == 7484 and 2195 + 614 + 3352 + 713 + 915 == 7789
assert f"{7789 / 7484 * 100:.2f}" == "104.08"
assert f"{895 / 109.5:.4f}" == "8.1735" and f"{895 / 1.095:.2f}" == "817.35"
assert f"{614 * 1.1225 ** 5:.2f}" == "1094.21"
# 7: Glücksrad rot 90°, grün 180°, blau = weiß = 45°
assert 90 + 180 + 45 + 45 == 360
r, g, b, w = F(90, 360), F(180, 360), F(45, 360), F(45, 360)
assert (r, g, b, w) == (F(1, 4), F(1, 2), F(1, 8), F(1, 8))
assert w * g * 2 == F(2, 16) == F(1, 8) and float(F(1, 8)) * 100 == 12.5
assert 1 - r * r == F(15, 16) and float(F(15, 16)) * 100 == 93.75
assert 1 - (1 - b) ** 2 == F(15, 64) and F(15, 64) * 5 - 1 == F(11, 64) and round(float(F(11, 64)), 2) == 0.17
# Punkte laut Aufgabenblatt: A1 = 1 + 2 + 2, A2 = 3 + 3 + 3 + 5, zusammen 19
P = {1: 1, 2: 1 + 1, 3: 1 + 1, 4: 1 + 1 + 1, 5: 1.5 + 1.5, 6: 1 + 1 + 1, 7: 1 + 1 + 1 + 1 + 1}
assert (P[1], P[2], P[3], P[4], P[5], P[6], P[7]) == (1, 2, 2, 3, 3, 3, 5)
assert sum(P.values()) == 19 and P[1] + P[2] + P[3] == 5 and P[4] + P[5] + P[6] + P[7] == 14


# ------------------------------------------------------------------ Bausteine
def f(a, b):
    return f'<span class="f"><span>{a}</span><span>{b}</span></span>'


def pt(x):
    """Rote Punktzahl im Kreis, wie in Oskars Korrektur."""
    return f'<span class="p">{str(x).replace(".", ",")}</span>'


def pkt(x):
    return str(x).replace(".", ",").replace(",0", "") + " P"


def kopf(nr, text=""):
    s = P[nr]
    s = int(s) if s == int(s) else s
    return f'<div class="bal"><b>Aufgabe {nr}</b><span class="t">{text}</span><span class="sum">{pkt(s)}</span></div>'


def zeile(*teile, p=None, cls=""):
    return f'<div class="z {cls}">' + "".join(teile) + (f'<span class="pr">{pt(p)}</span>' if p is not None else "") + "</div>"


def dr(links, rechts, cls="ein", p=None):
    """Eine Dreisatz-Zeile: Wert ≙ Prozent."""
    return zeile(f'<span class="gl">{links}</span> <span class="sy">≙</span> {rechts}', cls=cls, p=p)


def netz_svg():
    """Würfelnetz wie auf dem Blatt; gegebene Augen schwarz, ergänzte Augen blau."""
    a, r = 46, 5.5
    felder = {  # (Spalte, Zeile): (Augenzahl, ergänzt?)
        (0, 1): (2, False), (1, 1): (3, False), (2, 1): (1, False),
        (2, 0): (2, True), (3, 1): (3, True), (2, 2): (2, True)}
    augen = {1: [(.5, .5)], 2: [(.27, .27), (.73, .73)], 3: [(.25, .25), (.5, .5), (.75, .75)]}
    s = [f'<svg viewBox="0 0 {4 * a + 8} {3 * a + 8}" class="netz">']
    for (c, z), (n, neu) in felder.items():
        x, y = 4 + c * a, 4 + z * a
        s.append(f'<rect x="{x}" y="{y}" width="{a}" height="{a}" rx="6" class="nf"/>')
        for u, v in augen[n]:
            s.append(f'<circle cx="{x + u * a:.1f}" cy="{y + v * a:.1f}" r="{r}" class="{"an" if neu else "ag"}"/>')
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ Seiten
def seite1():
    a1 = (kopf(1)
          + '<div class="a1">' + netz_svg()
          + '<div>'
          + zeile("P(2; 2) = ", f(9, 36), " = ", f(3, 6), " · ", f(3, 6), " &nbsp;→ 3-mal die 2")
          + zeile("P(3; 3) = ", f(4, 36), " = ", f(2, 6), " · ", f(2, 6), " &nbsp;→ 2-mal die 3")
          + zeile("ergänzen: 2, 2 und 3", p=1)
          + '</div></div>')
    a2 = (kopf(2, "je 1 P")
          + zeile("a)", cls="teil")
          + dr("50", "<u>100 %</u>")
          + dr("5", "10 %")
          + dr("<u>30</u>", "60 %")
          + zeile("<u>30 schwarze Kugeln</u>", p=1, cls="ein")
          + zeile("b) P(s, w) + P(w, s) = ", f(30, 50), " · ", f(20, 50), " · 2 = ", f(1200, 2500), " = ", f(12, 25),
                  " = <u>48 %</u>", p=1))
    a3 = (kopf(3)
          + dr("300", "<u>100 %</u>")
          + dr("3", "1 %")
          + dr("360", "120 %")
          + zeile("Preis nach der Erhöhung: 360 €", p=1, cls="ein")
          + dr("360", "<u>100 %</u> &nbsp;(neues 100 %)")
          + dr("3,6", "1 %")
          + dr("<u>306</u>", "85 %")
          + zeile("Preis am „Black Friday“: <u>306,00 €</u>", p=1, cls="ein"))
    return a1 + a2 + a3


def seite2():
    a4 = (kopf(4, "je 1 P")
          + zeile("angelegt:", cls="teil")
          + zeile("K<sub>0</sub> · 1,008 · 1,010 · 1,013 = 5620,67 &nbsp; | : 1,008 &nbsp; | : 1,010 &nbsp; | : 1,013", cls="ein")
          + zeile("K<sub>0</sub> = <u>5450,00 €</u>", p=1, cls="ein")
          + zeile("Zinsen im 3. Jahr:", cls="teil")
          + zeile("5450 · 1,008 · 1,010 = K<sub>2</sub> = 5548,54 €", cls="ein")
          + dr("5548,54", "<u>100 %</u>")
          + dr("TR", "1 %")
          + dr("<u>72,13 €</u>", "1,3 %")
          + zeile("(Probe: 5620,67 − 5548,54 = 72,13)", p=1, cls="ein")
          + zeile("Maxi-Bank:", cls="teil")
          + zeile("5450 · q<sup>3</sup> = 5650 &nbsp; | : 5450 &nbsp; | <sup>3</sup>√", cls="ein")
          + zeile("q = 1,0121", cls="ein")
          + zeile("↳ p % = <u>1,21 %</u>", p=1, cls="ein"))
    a5 = (kopf(5, "je 1,5 P")
          + '<div class="gegeben">5 × M<br>3 × L<br>2 × U<br>ohne Zurücklegen</div>'
          + zeile("P(höchstens 1 × M) = 1 − P(M, M)")
          + zeile("= 1 − ", f(5, 10), " · ", f(4, 9), " = 1 − ", f(20, 90), " = ", f(70, 90), " = ", f(7, 9),
                  " ≈ <u>77,8 %</u>", p=1.5, cls="ein")
          + zeile("P(kein U) = P(nicht U, nicht U)")
          + zeile("= ", f(8, 10), " · ", f(7, 9), " = ", f(56, 90), " = ", f(28, 45), " ≈ <u>62,2 %</u>", p=1.5, cls="ein"))
    return a4 + a5


def seite3():
    a6 = (kopf(6, "je 1 P")
          + zeile("Zuwachs:", cls="teil")
          + dr("7484", "<u>100 %</u>")
          + dr("1", "TR")
          + dr("7789", "104,08 %")
          + zeile("Zuwachs um <u>4,08 %</u>", p=1, cls="ein")
          + zeile("Bannerwerbung 2019:", cls="teil")
          + dr("895 Mio €", "109,5 %")
          + dr("TR", "1 %")
          + dr("<u>817,35 Mio €</u>", "<u>100 %</u> &nbsp;(2019)", p=1)
          + zeile("Social-Media-Werbung 2026:", cls="teil")
          + zeile("614 · 1,1225<sup>5</sup> = 1094,21 &nbsp;→ <u>1094,21 Mio €</u>", p=1, cls="ein"))
    a7 = (kopf(7)
          + zeile("rot 90°, grün 180°, blau 45°, weiß 45°")
          + zeile("P(r) = ", f(1, 4), " &nbsp; P(g) = ", f(1, 2), " &nbsp; P(b) = ", f(1, 8), " &nbsp; P(w) = ", f(1, 8),
                  p=1, cls="ein")
          + zeile("P(w, g) + P(g, w) = ", f(1, 8), " · ", f(1, 2), " · 2 = ", f(2, 16), " = ", f(1, 8),
                  " = <u>12,5 %</u>", p=1)
          + zeile("P(höchstens 1 × rot) = 1 − P(r, r) = 1 − ", f(1, 4), " · ", f(1, 4), " = 1 − ", f(1, 16),
                  " = ", f(15, 16), " = <u>93,75 %</u>", p=1)
          + zeile("Glücksspiel:", cls="teil")
          + zeile("P(mind. 1 × blau) = 1 − P(nicht b, nicht b) = 1 − ", f(7, 8), " · ", f(7, 8), " = 1 − ", f(49, 64),
                  " = ", f(15, 64), p=1, cls="ein")
          + zeile("E = ", f(15, 64), " · 5 − 1 = ", f(11, 64), " ≈ 0,17 € = <u>+17 ct</u>", cls="ein")
          + zeile("E &gt; 0: Im Mittel gewinnt man 17 ct pro Spiel. <u>Mitspielen lohnt sich.</u>", p=1, cls="ein"))
    return a6 + a7


CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
:root{--bl:#2f86cf;--rot:#d6001c;--dk:#1b1b1b}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;color:var(--bl);font-weight:600}
.seite{width:210mm;height:297mm;padding:12mm 15mm;break-after:page;overflow:hidden;position:relative}
.seite:last-child{break-after:auto}
h1{font-size:19px;margin:0 0 3px;color:var(--dk);display:flex;justify-content:space-between;align-items:baseline}
h1 .r{color:var(--rot)}
.sub{font-size:13px;color:#555;font-weight:500;margin:0 0 10px;border-bottom:2px solid var(--dk);padding-bottom:6px}
.bal{display:flex;align-items:baseline;gap:12px;background:#eef2f6;border-left:5px solid var(--dk);padding:4px 10px;margin:14px 0 6px;color:var(--dk);font-size:17px}
.bal .t{color:#666;font-weight:500;font-size:13px}.bal .sum{margin-left:auto;color:var(--rot);font-weight:800;font-size:19px}
.z{display:block;font-size:var(--fs);line-height:1.2;margin:var(--gap) 0;position:relative;padding-right:56px;min-height:1.4em}
.z.ein{padding-left:28px}.z.ein2{padding-left:44px}
.z .pr{position:absolute;right:4px;top:50%;transform:translateY(-50%)}
.z.teil{margin-bottom:0;margin-top:calc(var(--gap) + 4px)}
.p{display:inline-block;min-width:1.9em;text-align:center;color:var(--rot);font-weight:800;font-size:.82em;border:2px solid var(--rot);border-radius:50%;padding:1px 3px;background:#fff;line-height:1.15}
.f{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 3px;line-height:1.1;font-size:.95em}
.f>span:first-child{border-bottom:2px solid currentColor;padding:0 3px 1px}.f>span:last-child{padding:1px 3px 0}
.gl{display:inline-block;min-width:3em}
.gegeben{font-size:var(--fs);line-height:1.25;margin:4px 0 8px 28px}
.a1{display:flex;align-items:center;gap:22px}.a1>div{flex:1}
.netz{width:210px;height:auto;flex:none}
.nf{fill:#fff;stroke:var(--dk);stroke-width:1.6}.ag{fill:var(--dk)}.an{fill:var(--bl)}
span.sy{font-family:'Arial Unicode MS','STIXGeneral',serif;font-size:1.25em;margin:0 3px}
sub,sup{font-size:.7em;line-height:0}
.s1{--fs:19px;--gap:7px}.s2{--fs:19px;--gap:7px}.s3{--fs:18px;--gap:6px}
"""


def html():
    gesamt = "Gesamt 19 P: A1 5 P + A2 14 P."
    kopf1 = ('<h1><span>Mathe 10b – Klassenarbeit Nr. 1 Nachtermin – Lösung</span><span class="r">Teil A1: 5 P</span></h1>'
             f'<div class="sub">Teil A1 (ohne Taschenrechner, 20 min). {gesamt} Punktsumme je Aufgabe laut Blatt, rote Punkte = Vorschlag zur Verteilung. '
             'Beim Korrigieren: Haken = 1 P, Haken mit Strich im unteren Drittel = 0,5 P.</div>')
    kopf2 = ('<h1><span>Mathe 10b – Klassenarbeit Nr. 1 Nachtermin – Lösung</span><span class="r">Teil A2: 14 P</span></h1>'
             f'<div class="sub">Aufgaben 4 und 5. {gesamt}</div>')
    kopf3 = ('<h1><span>Mathe 10b – Klassenarbeit Nr. 1 Nachtermin – Lösung</span><span class="r">Teil A2: 14 P</span></h1>'
             f'<div class="sub">Aufgaben 6 und 7. {gesamt}</div>')
    seiten = [("s1", kopf1 + seite1()), ("s2", kopf2 + seite2()), ("s3", kopf3 + seite3())]
    return ('<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>' + NAME + '</title><style>' + CSS + '</style></head><body>'
            + "".join(f'<div class="seite {c}">{h}</div>' for c, h in seiten) + "</body></html>")


if __name__ == "__main__":
    h = HIER / f"{NAME}.html"
    pdf = HIER / f"{NAME}.pdf"
    h.write_text(html(), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=4000", h.as_uri()], check=True, capture_output=True)
    n = len(PdfReader(str(pdf)).pages)
    assert n == 3, f"{n} Seiten statt 3"
    print(pdf, n, "Seiten")
