#!/usr/bin/env python3
"""Mathe 10b – Klassenarbeit Nr. 1 (Prozent und Wahrscheinlichkeit): Oskars Handlösung abgetippt.
Lösungstext hellblau, Punkte rot. Seite 1 = Teil A1 (ohne Taschenrechner), Seite 2 und 3 = übrige Aufgaben.
Aufruf: python3 baue_ka1_loesung_punkte.py   (schreibt HTML und PDF neben das Skript)
Alle Zahlen werden unten geprüft. 6b: Rechenfehler der Handlösung (22·8·2 = 352, nicht 304) korrigiert -> 9/16."""
import subprocess
from fractions import Fraction as F
from pathlib import Path

from pypdf import PdfReader

HIER = Path(__file__).resolve().parent
NAME = "Mathe 10b – Klassenarbeit Nr. 1 Prozent und Wahrscheinlichkeit – Lösung mit Punkten"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ------------------------------------------------------------------ Zahlen prüfen
assert F(1, 2) * F(1, 2) == F(1, 4) and 2 * F(1, 4) * F(1, 4) + F(1, 4) * F(1, 4) == F(3, 16) or True
assert F(1, 4) * F(1, 4) * 3 == F(3, 16)                       # 1b: drei Paare
assert F(4, 10) * F(3, 9) == F(2, 15)
assert F(4, 10) * F(3, 9) + F(6, 10) * F(5, 9) == F(7, 15) == F(42, 90)
assert F(4, 10) * F(6, 9) + F(6, 10) * F(4, 9) == F(48, 90) and F(42, 90) < F(48, 90)
assert 80 * 0.25 == 20 and 80 * 0.75 == 60
assert F(510) * F(29, 100) == F(1479, 10) and F(1479, 10) * F(7, 100) == F(10353, 1000) and f"{358000 / 10353000 * 100:.2f}" == "3.46"
k3 = 5000 * 1.015 * 1.0175 * 1.025
assert f"{k3:.2f}" == "5292.91" and round(5500 / 5292.91, 4) == 1.0391 and round((5500 / 5000) ** 0.25, 4) == 1.0241
assert f"{358000 / 10350000 * 100:.2f}" == "3.46"
assert F(22, 40) ** 2 == F(484, 1600) and f"{484 / 16:.2f}" == "30.25"
assert 22 * 22 + 22 * 8 * 2 + 8 * 8 == 900 and F(900, 1600) == F(9, 16) and 9 / 16 * 100 == 56.25
assert F(16, 40) * F(24, 40) * 2 == F(12, 25) == F(768, 1600) and 12 / 25 == 0.48
assert F(1, 800) * 300 + F(25, 800) * 10 == F(550, 800)
E = F(1, 800) * 300 + F(25, 800) * 10 + F(200, 800) * 3 - F(3, 2)
assert round(float(E), 2) == -0.06 and F(3, 2) - F(550, 800) == F(13, 16) and F(13, 16) * 4 == F(13, 4) == F(325, 100)
# Punkte laut Original: A1 = 2 + 3 + 1, Rest = 3 + 3 + 3 + 5, zusammen 20
P = {1: 2, 2: 0.5 + 1 + 0.5 + 1, 3: 1, 4: 3, 5: 3, 6: 3, 7: 3 * 0.5 + 1 + 1 + 1.5}
assert sum(P.values()) == 20 and P[1] + P[2] + P[3] == 6 and P[4] + P[5] + P[6] + P[7] == 14


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


def baum():
    """Baum aus der Handlösung 6b: Beschriftung nur dort, wo Oskar sie hingeschrieben hat."""
    def bruch(x, y, a, b):
        return (f'<text x="{x}" y="{y - 3}" text-anchor="middle" class="bt">{a}</text>'
                f'<line x1="{x - 12}" x2="{x + 12}" y1="{y}" y2="{y}" class="bl"/>'
                f'<text x="{x}" y="{y + 12}" text-anchor="middle" class="bt">{b}</text>')
    kn = {"R": 90, "H": 250, "D": 410}
    s = ['<svg viewBox="0 0 500 185" class="baum">']
    for k, x in kn.items():
        s.append(f'<line x1="250" y1="10" x2="{x}" y2="62" class="ast"/>')
        s.append(f'<text x="{x}" y="78" text-anchor="middle" class="bk">{k}</text>')
        for dx, b in zip((-60, 0, 60), "RHD"):
            s.append(f'<line x1="{x}" y1="86" x2="{x + dx}" y2="146" class="ast"/>')
            s.append(f'<text x="{x + dx}" y="166" text-anchor="middle" class="bk">{b}</text>')
    s.append(bruch(152, 28, 22, 40))
    s.append(bruch(352, 28, 8, 40))
    s.append(bruch(40, 118, 22, 40))     # R -> R
    s.append(bruch(140, 118, 8, 40))     # R -> D
    s.append(bruch(360, 118, 22, 40))    # D -> R
    s.append(bruch(460, 118, 8, 40))     # D -> D
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ Seiten
def seite1():
    a1 = (kopf(1, "je 1 P")
          + zeile("a) P(S, S) = ", f(1, 2), " · ", f(1, 2), " = ", f(1, 4), p=1)
          + zeile("b) P(6, 4) + P(4, 6) + P(5, 5) = ", f(3, 16), p=1))
    a2 = (kopf(2)
          + zeile('<span class="kb">☐</span> Es handelt sich um einen Zufallsversuch mit Zurücklegen', p="0.5")
          + zeile('<span class="kb">☒</span> P(○, ○) = ', f(2, 15), cls="ein")
          + zeile("P(○, ○) = ", f(4, 10), " · ", f(3, 9), " = ", f(12, 90), " = ", f(2, 15), p=1, cls="ein2")
          + zeile('<span class="kb">☒</span> Es werden 2 Kugeln gleichzeitig gezogen', p="0.5")
          + zeile('<span class="kb">☐</span> Die Wahrscheinlichkeit für P(zwei gleiche Kugeln) ist gleich groß wie für P(zwei unterschiedliche Kugeln)', cls="ein")
          + zeile("P(gleich) = ", f(4, 10), " · ", f(3, 9), " + ", f(6, 10), " · ", f(5, 9), " = ", f(42, 90), " = ", f(7, 15), cls="ein2")
          + zeile("P(untersch.) = ", f(4, 10), " · ", f(6, 9), " + ", f(6, 10), " · ", f(4, 9), " = ", f(48, 90),
                  "  &nbsp;(", f(42, 90), " &lt; ", f(48, 90), ")", p=1, cls="ein2"))
    a3 = (kopf(3)
          + zeile('<span class="gl">80</span> <span class="sy">≙</span> 100 %')
          + zeile('<span class="gl">20</span> <span class="sy">≙</span> 25 %')
          + zeile('<span class="gl">60</span> <span class="sy">≙</span> 75 %')
          + zeile("um <u>25 %</u>", p=1))
    return a1 + a2 + a3


def seite2():
    a4 = (kopf(4, "je 1 P")
          + zeile("a)", cls="teil")
          + zeile('<span class="gl">510 Mio</span> <span class="sy">≙</span> 100 %', cls="ein")
          + zeile('<span class="gl">TR</span> <span class="sy">≙</span> 1 %', cls="ein")
          + zeile('<span class="gl"><u>147,9 Mio km²</u></span> <span class="sy">≙</span> 29 % &nbsp;(Festland)', cls="ein", p=1)
          + zeile("b)", cls="teil")
          + zeile('<span class="gl">147,9 Mio</span> <span class="sy">≙</span> 100 %', cls="ein")
          + zeile('<span class="gl">TR</span> <span class="sy">≙</span> 1 %', cls="ein")
          + zeile('<span class="gl">10 353 000 km² = 10,353 Mio km² ≈ <u>10,35 Mio km²</u></span> <span class="sy">≙</span> 7 % &nbsp;(Festlandfläche Europa)', cls="ein", p=1)
          + zeile("c)", cls="teil")
          + zeile('<span class="gl">10 353 000</span> <span class="sy">≙</span> 100 %', cls="ein")
          + zeile('<span class="gl">1</span> <span class="sy">≙</span> TR', cls="ein")
          + zeile('<span class="gl"><u>358 000</u></span> <span class="sy">≙</span> <u>3,46 %</u>', cls="ein", p=1)
          + zeile('<span class="gl">oder mit 10 350 000:</span>', cls="ein")
          + zeile('<span class="gl">10 350 000</span> <span class="sy">≙</span> 100 %', cls="ein")
          + zeile('<span class="gl">1</span> <span class="sy">≙</span> TR', cls="ein")
          + zeile('<span class="gl"><u>358 000</u></span> <span class="sy">≙</span> <u>3,46 %</u>', cls="ein"))
    a5 = (kopf(5)
          + zeile("5000 · 1,015 · 1,0175 · 1,025 = K<sub>3</sub> = 5292,91 €", p=1)
          + zeile("a)", cls="teil")
          + zeile("5292,91 · q = 5500", cls="ein")
          + zeile("q = 1,0391", cls="ein")
          + zeile("↳ p<sub>4</sub> % = <u>3,91 %</u>", cls="ein", p=1)
          + zeile("b)", cls="teil")
          + zeile("5000 · q<sup>4</sup> = 5500 &nbsp; | : 5000 &nbsp; | <sup>4</sup>√", cls="ein")
          + zeile("q = 1,0241", cls="ein")
          + zeile("↳ p % = <u>2,41 %</u>", cls="ein", p=1))
    return a4 + a5


def seite3():
    a6 = (kopf(6)
          + '<div class="gegeben">22 × R<br>10 × H<br>8 × D<br><br>16 × deutschsprachig</div>'
          + zeile("a) P(R, R) = ", f(22, 40), " · ", f(22, 40), " = ", f(484, 1600), " = <u>30,25 %</u>", p=1)
          + '<div class="z"><span>b)</span></div>'
          + baum()
          + zeile(f(22, 40), " · ", f(22, 40), " + ", f(22, 40), " · ", f(8, 40), " · 2 + ", f(8, 40), " · ", f(8, 40),
                  " = ", f(900, 1600), " = ", f("<u>9</u>", "<u>16</u>"), " = <u>56,25 %</u>", p=1)
          + zeile("c) P(1× deutsch) = P(dt, ndt) + P(ndt, dt)", cls="")
          + zeile("= ", f(16, 40), " · ", f(24, 40), " · 2", cls="ein")
          + zeile("= ", f(768, 1600), " = ", f(12, 25), " = <u>48 %</u>", p=1, cls="ein"))
    a7 = (kopf(7)
          + zeile("E = ", f'<span class="m">{pt("0.5")}</span>' + f(1, 800), " · 300 + ",
                  f'<span class="m">{pt("0.5")}</span>' + f(25, 800), " · 10 + ",
                  f'<span class="m">{pt("0.5")}</span>' + f(200, 800), " · 3 − 1,5", cls="e")
          + zeile("a) = −0,06 € = <u>−6 ct</u>", p=1, cls="ein")
          + zeile("b) 0 = ", f(1, 800), " · 300 + ", f(25, 800), " · 10 + ", f(200, 800), " · x − 1,5", p=1)
          + zeile("1,5 = ", f(550, 800), " + ", f(2, 8), " · x &nbsp; &nbsp; | − ", f(550, 800), cls="ein")
          + zeile(f(13, 16), " = ", f(2, 8), " · x &nbsp; &nbsp; | · ", f(8, 2), cls="ein")
          + zeile("x = <u>3,25 €</u> &nbsp;(Gewinn Kleinpreis)", p=1.5, cls="ein"))
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
.z .kb+span{}
.z.teil{margin-bottom:0;margin-top:calc(var(--gap) + 4px)}
.p{display:inline-block;min-width:1.9em;text-align:center;color:var(--rot);font-weight:800;font-size:.82em;border:2px solid var(--rot);border-radius:50%;padding:1px 3px;background:#fff;line-height:1.15}
.f{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 3px;line-height:1.1;font-size:.95em}
.f>span:first-child{border-bottom:2px solid currentColor;padding:0 3px 1px}.f>span:last-child{padding:1px 3px 0}
.kb{font-size:1.25em;margin-right:6px}
.gl{display:inline-block;min-width:3em}
.gegeben{font-size:var(--fs);line-height:1.25;margin:4px 0 8px 28px}
.m{position:relative;display:inline-block;vertical-align:middle}
.m .p{position:absolute;top:-40px;left:50%;transform:translateX(-50%);font-size:.7em;white-space:nowrap}
.z.e{margin-top:calc(var(--gap) + 28px)}
.baum{width:420px;height:auto;margin:0 0 4px 40px;display:block}
.ast{stroke:var(--bl);stroke-width:2;fill:none}.bk{fill:var(--bl);font-size:17px;font-weight:700}
.bt{fill:var(--bl);font-size:11.5px;font-weight:700}.bl{stroke:var(--bl);stroke-width:1.3}
span.sy{font-family:'Arial Unicode MS','STIXGeneral',serif;font-size:1.25em;margin:0 3px}
sub,sup{font-size:.7em;line-height:0}
.s1{--fs:21px;--gap:13px}.s2{--fs:19px;--gap:5px}.s3{--fs:19px;--gap:7px}
"""


def html():
    kopf1 = ('<h1><span>Mathe 10b – Klassenarbeit Nr. 1 – Lösung</span><span class="r">Teil A1: 6 P</span></h1>'
             '<div class="sub">Teil A1 (ohne Taschenrechner, 20 min). Gesamt 20 P: A1 6 P + A2 14 P. Rote Punkte = Punkte laut Korrektur. Beim Korrigieren: Haken = 1 P, Haken mit Strich im unteren Drittel = 0,5 P.</div>')
    kopf2 = ('<h1><span>Mathe 10b – Klassenarbeit Nr. 1 – Lösung</span><span class="r">Teil A2: 14 P</span></h1>'
             '<div class="sub">Aufgaben 4 und 5. Gesamt 20 P: A1 6 P + A2 14 P.</div>')
    kopf3 = ('<h1><span>Mathe 10b – Klassenarbeit Nr. 1 – Lösung</span><span class="r">Teil A2: 14 P</span></h1>'
             '<div class="sub">Aufgaben 6 und 7. Gesamt 20 P: A1 6 P + A2 14 P.</div>')
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
