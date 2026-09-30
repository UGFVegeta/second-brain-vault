#!/usr/bin/env python3
"""Folien Prozentrechnen (Wdh) Klasse 10b: 3 Folien im Notability-Format (960 x 540 pt, wie die 7c-Folien) plus Lösungsfassung nur für den Lehrer.
Folie 1 Einstiegsaufgabe (Kreisdiagramm, Dreisatz und Formel), Folie 2 und 3 je zwei Aufgaben, bei denen das neue 100 % aus dem Diagramm herausgelesen wird.
Alle Ergebnisse werden hier nachgerechnet. Aufruf: python3 baue_folien.py -> 'Prozent Wdh 10b – Folien.pdf' und '… – Lösungen (nur für mich).pdf'"""
import math, subprocess
from fractions import Fraction
from pathlib import Path

HIER = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FARBEN = ["#c9d6ea", "#f3d9a4", "#cfe6cf", "#e8cfe0"]
ROT = "#b3261e"

# ---------------------------------------------------------------- Zahlen (mit Prüfung)
E_G = 240
E_TEILE = [("Bus", 40), ("Fahrrad", 25), ("zu Fuß", 20), ("Elterntaxi", 15)]
E_RAD = 60
assert sum(p for _, p in E_TEILE) == 100
assert E_RAD * 100 // 25 == E_G and E_G * 40 // 100 == 96 and Fraction(24, 96) == Fraction(1, 4) and Fraction(24, E_G) == Fraction(1, 10)

WAHL = [("Lena", 45), ("Tom", 35), ("Ali", 20)]
TOM = 126
assert sum(p for _, p in WAHL) == 100 and Fraction(TOM * 100, 35) == 360 and 360 * 20 // 100 == 72

KL = [("10a", 25, 40), ("10b", 40, 30)]  # Klasse, Schüler, Prozent Fahrrad
assert [s * p // 100 for _, s, p in KL] == [10, 12]

NOTEN = [("1–2", 6), ("3", 12), ("4", 9), ("5–6", 3)]
assert sum(n for _, n in NOTEN) == 30 and [n * 100 // 30 for _, n in NOTEN] == [20, 40, 30, 10]

VEREIN = [("Erwachsene", 50), ("Jugendliche", 30), ("Kinder", 20)]
assert sum(p for _, p in VEREIN) == 100 and 500 * 30 // 100 == 150 and 150 * 40 // 100 == 60 and Fraction(60, 500) == Fraction(12, 100)


# ---------------------------------------------------------------- Grafiken
def kreis(teile, gross=170, fs=15):
    cx = cy = gross + 10
    a0, s = -90, ""
    for i, (n, p) in enumerate(teile):
        a1 = a0 + p * 3.6
        x0, y0 = cx + gross * math.cos(math.radians(a0)), cy + gross * math.sin(math.radians(a0))
        x1, y1 = cx + gross * math.cos(math.radians(a1)), cy + gross * math.sin(math.radians(a1))
        s += (f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{gross},{gross} 0 {1 if p > 50 else 0} 1 {x1:.1f},{y1:.1f} Z" '
              f'fill="{FARBEN[i]}" stroke="#222" stroke-width="1.6"/>')
        am = math.radians((a0 + a1) / 2)
        tx, ty = cx + gross * .62 * math.cos(am), cy + gross * .62 * math.sin(am)
        s += (f'<text x="{tx:.1f}" y="{ty - 3:.1f}" text-anchor="middle" font-size="{fs}" font-weight="700">{n}</text>'
              f'<text x="{tx:.1f}" y="{ty + fs:.1f}" text-anchor="middle" font-size="{fs}">{p} %</text>')
        a0 = a1
    d = 2 * gross + 20
    return f'<svg width="{d}" height="{d}" viewBox="0 0 {d} {d}">{s}</svg>'


def stapel(teile, w=420, h=46):
    x, s = 6, ""
    for i, (n, p) in enumerate(teile):
        bw = (w - 12) * p / 100
        s += (f'<rect x="{x:.1f}" y="6" width="{bw:.1f}" height="{h}" fill="{FARBEN[i]}" stroke="#222" stroke-width="1.6"/>'
              f'<text x="{x + bw / 2:.1f}" y="{6 + h / 2 - 3}" text-anchor="middle" font-size="14" font-weight="700">{n}</text>'
              f'<text x="{x + bw / 2:.1f}" y="{6 + h / 2 + 14}" text-anchor="middle" font-size="14">{p} %</text>')
        x += bw
    return f'<svg width="{w}" height="{h + 12}" viewBox="0 0 {w} {h + 12}">{s}</svg>'


def zweibalken(w=420):
    s = ""
    x0, br = 46, w - 70
    for k, (n, _, p) in enumerate(KL):
        y = 14 + k * 46
        s += (f'<text x="0" y="{y + 20}" font-size="15" font-weight="700">{n}</text>'
              f'<rect x="{x0}" y="{y}" width="{br}" height="28" fill="#fff" stroke="#999" stroke-width="1"/>'
              f'<rect x="{x0}" y="{y}" width="{br * p / 100:.1f}" height="28" fill="{FARBEN[1]}" stroke="#222" stroke-width="1.6"/>'
              f'<text x="{x0 + br * p / 100 + 8:.1f}" y="{y + 20}" font-size="15" font-weight="700">{p} %</text>')
    for t in (0, 50, 100):
        s += (f'<line x1="{x0 + br * t / 100}" y1="6" x2="{x0 + br * t / 100}" y2="106" stroke="#bbb" stroke-dasharray="3 3"/>'
              f'<text x="{x0 + br * t / 100}" y="122" text-anchor="middle" font-size="12" fill="#666">{t} %</text>')
    return f'<svg width="{w}" height="128" viewBox="0 0 {w} 128">{s}</svg>'


def saeulen(w=420, h=150):
    s, mx = "", 12
    bw, ab = 62, 30
    for i, (n, z) in enumerate(NOTEN):
        x = 40 + i * (bw + ab)
        hh = (h - 40) * z / mx
        s += (f'<rect x="{x}" y="{h - 22 - hh:.1f}" width="{bw}" height="{hh:.1f}" fill="{FARBEN[i]}" stroke="#222" stroke-width="1.6"/>'
              f'<text x="{x + bw / 2}" y="{h - 27 - hh:.1f}" text-anchor="middle" font-size="15" font-weight="700">{z}</text>'
              f'<text x="{x + bw / 2}" y="{h - 5}" text-anchor="middle" font-size="14">Note {n}</text>')
    s += f'<line x1="32" y1="{h - 22}" x2="{w}" y2="{h - 22}" stroke="#222" stroke-width="1.4"/>'
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{s}</svg>'


# ---------------------------------------------------------------- Folien
CSS = f"""
@page{{size:960pt 540pt;margin:0}}
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{margin:0;padding:0}}
body{{font-family:Helvetica,Arial,sans-serif;color:#1b1b1b}}
.f{{width:960pt;height:540pt;padding:26pt 34pt;position:relative;overflow:hidden;page-break-after:always;break-after:page}}
.f:last-child{{page-break-after:auto;break-after:auto}}
h1{{font-size:26pt;margin:0 0 10pt}} h1 small{{font-size:14pt;color:#777;font-weight:400;margin-left:10pt}}
p{{margin:0 0 8pt;font-size:17pt;line-height:1.3}} .t{{font-size:17pt;line-height:1.3}}
.sub{{display:flex;gap:8pt;margin:0 0 8pt;font-size:17pt;line-height:1.3}}.sub b{{flex:none;width:22pt}}
.chart svg{{width:100%;height:auto}}
.two{{display:flex;gap:34pt;align-items:flex-start}}.two>div{{flex:1;min-width:0}}
h2{{font-size:21pt;margin:0 0 8pt}} .k{{color:#777}}
.rot{{color:{ROT};font-weight:700}} .l{{color:{ROT}}}
.spalten{{position:absolute;left:34pt;right:34pt;bottom:20pt;display:flex;gap:0;border-top:.8pt solid #ccc}}
.spalten>div{{flex:1;padding:8pt 12pt 0}} .spalten>div+div{{border-left:.8pt solid #ccc}}
.spalten h3{{margin:0 0 4pt;font-size:13pt;color:#999;font-weight:600}}
.spalten p{{font-size:14pt;margin:0 0 4pt}}
.lsg{{margin-top:8pt;font-size:15pt;line-height:1.35;color:{ROT}}} .lsg b{{color:{ROT}}}
"""


def folie1(lsg):
    _, r2, b = None, None, None
    if lsg:
        unten = f"""<div class="spalten" style="top:322pt"><div><h3>Dreisatz</h3>
<p class="l"><b>a)</b> 25 % ≙ 60 &nbsp;→&nbsp; 1 % ≙ 2,4 &nbsp;→&nbsp; 100 % ≙ <b>240</b></p>
<p class="l"><b>b)</b> 100 % ≙ 240 &nbsp;→&nbsp; 1 % ≙ 2,4 &nbsp;→&nbsp; 40 % ≙ <b>96</b></p>
<p class="l"><b>c)</b> 96 ≙ 100 % &nbsp;→&nbsp; 24 ≙ 24 · 100 % : 96 = <b>25 %</b> (Busfahrer = 100 %)<br>240 ≙ 100 % &nbsp;→&nbsp; 24 ≙ 24 · 100 % : 240 = <b>10 %</b> (alle = 100 %)</p></div>
<div><h3>Formel</h3>
<p class="l"><b>a)</b> G = W : p % = 60 : 0,25 = <b>240</b></p>
<p class="l"><b>b)</b> W = G · p % = 240 · 0,40 = <b>96</b></p>
<p class="l"><b>c)</b> p % = W : G = 24 : 96 = <b>25 %</b> (G = Busfahrer)<br>p % = 24 : 240 = <b>10 %</b> (G = alle Befragten)</p></div></div>"""
    else:
        unten = ('<div class="spalten" style="top:335pt"><div><h3>Dreisatz</h3></div><div><h3>Formel</h3></div></div>')
    return f"""<div class="f"><h1>Einstiegsaufgabe: Schulweg</h1>
<div class="two" style="align-items:center"><div style="flex:1.15">
<p>Schülerinnen und Schüler wurden befragt, wie sie zur Schule kommen. Das Kreisdiagramm zeigt das Ergebnis. <b>{E_RAD}</b> Befragte kommen mit dem Fahrrad.</p>
<div class="sub"><b>a)</b><span>Wie viele Schülerinnen und Schüler wurden insgesamt befragt?</span></div>
<div class="sub"><b>b)</b><span>Wie viele der Befragten kommen mit dem Bus?</span></div>
<div class="sub"><b>c)</b><span>24 der Busfahrer sind Fünftklässler. Wie viel Prozent <u>der Busfahrer</u> sind das? Wie viel Prozent <u>aller Befragten</u> sind das?</span></div></div>
<div style="flex:none;width:350pt;margin-top:-10pt">{kreis(E_TEILE, 165, 17)}</div></div>{unten}</div>"""


def folie2(lsg):
    a2 = f"""<h2>Aufgabe 2 <span class="k" style="font-size:12pt">Schülersprecherwahl</span></h2>
<p class="t">Der Balken zeigt die Stimmenanteile. Tom erhielt <b>{TOM}</b> Stimmen.</p><div class="chart">{stapel(WAHL)}</div>
<div class="sub t"><b>a)</b><span>Wie viele Stimmen wurden insgesamt abgegeben?</span></div>
<div class="sub t"><b>b)</b><span>Wie viele Stimmen erhielt Ali?</span></div>"""
    a3 = f"""<h2>Aufgabe 3 <span class="k" style="font-size:12pt">Fahrrad-Fahrer</span></h2>
<p class="t">Klasse 10a hat 25, Klasse 10b hat 40 Schüler. Die Balken zeigen, wie viel Prozent mit dem Fahrrad kommen.</p><div class="chart">{zweibalken()}</div>
<p class="t" style="margin-top:4pt">Timo sagt: „In der 10a fahren mehr Schüler mit dem Rad, weil 40 % mehr sind als 30 %.“ Stimmt das? Begründe mit einer Rechnung.</p>"""
    if lsg:
        a2 += (f'<div class="lsg"><b>a)</b> 35 % ≙ {TOM} → 1 % ≙ 3,6 → 100 % ≙ <b>360</b> (G = {TOM} : 0,35 = 360)<br>'
               f'<b>b)</b> 20 % von 360 = <b>72</b> Stimmen</div>')
        a3 += ('<div class="lsg">10a: 40 % von 25 = <b>10</b> Schüler, 10b: 30 % von 40 = <b>12</b> Schüler.<br>'
               'Timo hat nicht Recht: Die 100 % sind in den Klassen verschieden groß.</div>')
    return f'<div class="f"><div class="two"><div>{a2}</div><div>{a3}</div></div></div>'


def folie3(lsg):
    a4 = f"""<h2>Aufgabe 4 <span class="k" style="font-size:12pt">Klassenarbeit</span></h2>
<p class="t">Das Diagramm zeigt, wie oft jede Note in der Klassenarbeit vorkam.</p><div class="chart">{saeulen()}</div>
<div class="sub t"><b>a)</b><span>Wie viele Schüler haben mitgeschrieben?</span></div>
<div class="sub t"><b>b)</b><span>Wie viel Prozent hatten Note 3? Berechne auch die Prozentsätze der anderen Noten.</span></div>"""
    a5 = f"""<h2>Aufgabe 5 <span class="k" style="font-size:12pt">Sportverein</span></h2>
<p class="t">Ein Verein hat <b>500</b> Mitglieder. Das Kreisdiagramm zeigt, wie sie sich verteilen. Von den Jugendlichen sind 40 % Mädchen.</p>
<div class="chart" style="margin:2pt 0;width:58%">{kreis(VEREIN, 110, 13)}</div>
<div class="sub t"><b>a)</b><span>Wie viele Jugendliche gehören zum Verein?</span></div>
<div class="sub t"><b>b)</b><span>Wie viele Mädchen sind das?</span></div>
<div class="sub t"><b>c)</b><span>Wie viel Prozent <u>aller Mitglieder</u> sind Mädchen aus der Gruppe Jugendliche?</span></div>"""
    if lsg:
        a4 += ('<div class="lsg"><b>a)</b> 6 + 12 + 9 + 3 = <b>30</b> Schüler (das sind 100 %)<br>'
               '<b>b)</b> Note 3: 12 : 30 = <b>40 %</b>; Note 1–2: 6 : 30 = <b>20 %</b>; Note 4: 9 : 30 = <b>30 %</b>; Note 5–6: 3 : 30 = <b>10 %</b></div>')
        a5 += ('<div class="lsg"><b>a)</b> 30 % von 500 = <b>150</b> &nbsp; <b>b)</b> 40 % von 150 = <b>60</b><br>'
               '<b>c)</b> 60 : 500 = <b>12 %</b> aller Mitglieder (Jugendliche = 100 %: 40 %)</div>')
    return f'<div class="f"><div class="two"><div>{a4}</div><div>{a5}</div></div></div>'


def seite(lsg):
    titel = "Prozent Wdh 10b" + (" – Lösungen" if lsg else "")
    return f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title><style>{CSS}</style></head><body>{folie1(lsg)}{folie2(lsg)}{folie3(lsg)}</body></html>'.replace(" %", "&nbsp;%")


def main():
    for lsg, name in ((False, "Prozent Wdh 10b – Folien"), (True, "Prozent Wdh 10b – Folien – Lösungen (nur für mich)")):
        h = HIER / f"{name}.html"
        h.write_text(seite(lsg), encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / (name + '.pdf')}", h.as_uri()],
                       check=True, capture_output=True)
        print("geschrieben:", name + ".pdf")


if __name__ == "__main__":
    main()
