#!/usr/bin/env python3
"""Baut das Arbeitsblatt 'Addieren und Subtrahieren' (A4, Stil der Buchaufgaben, ohne Klammern) plus Lösungsblatt.

Schwierigkeit wie im Buch: ○ leicht, ◐ mittel, ● schwer.
Änderungen hier im Skript, dann `python3 baue_arbeitsblatt2.py`. PDFs per Chrome headless:
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="X.pdf" "X.html"
"""
from pathlib import Path

ACC = "#12909e"


def m(v):
    """Zahl mit typografischem Minus, Komma als Dezimalzeichen."""
    t = f"{abs(v):g}".replace(".", ",")
    return ("−" + t) if v < 0 else t


def frac(z, n, neg=False):
    s = "−" if neg else ""
    return f'{s}<span class="frac"><span>{z}</span><span class="u">{n}</span></span>'


def kreis(stufe):
    """stufe 0 leer, 1 halb, 2 voll"""
    r = 8
    base = (f'<svg class="lvl" viewBox="0 0 20 20" width="17" height="17" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="10" cy="10" r="{r}" fill="#fff" stroke="#333" stroke-width="1.5"/>')
    if stufe == 1:
        base += f'<path d="M10 2 A8 8 0 0 0 10 18 Z" fill="#333"/>'
    elif stufe == 2:
        base += f'<circle cx="10" cy="10" r="{r}" fill="#333"/>'
    return base + "</svg>"


# ------------------------------------------------------------------ Aufgaben
T1 = [("12 + 8", 20), ("−15 − 10", -25), ("−20 + 5", -15), ("18 − 6", 12),
      ("−14 + 9", -5), ("−7 − 7", -14), ("30 − 45", -15), ("−8 + 8", 0)]
T2 = [("28 − 10", 18), ("−15 + 20", 5), ("−30 + 20", -10), ("24 − 36", -12),
      ("−35 − 25", -60), ("16 − 20", -4), ("−55 + 35", -20), ("38 − 45", -7)]
T3 = [("−41 + 18", -23), ("52 − 79", -27), ("−36 − 45", -81),
      ("−68 + 90", 22), ("75 − 120", -45), ("−150 − 60", -210)]
T3_KARTEN = [-81, 22, -210, -27, -45, -23]
T4 = [("15 − 9 = 24", "15 − 9", 6), ("−20 + 12 = 8", "−20 + 12", -8), ("−18 − 7 = −11", "−18 − 7", -25),
      ("34 − 50 = 16", "34 − 50", -16), ("−2,5 − 1,5 = −1", "−2,5 − 1,5", -4)]
T5 = [("6,4 − 9,1", -2.7), ("−3,8 + 2,5", -1.3), ("−7,25 − 2,5", -9.75), ("−0,48 + 0,9", 0.42),
      (f"{frac(1,2,True)} + {frac(1,4)}", frac(1, 4, True)),
      (f"{frac(2,5,True)} − {frac(1,5)}", frac(3, 5, True)),
      (f"{frac(1,3)} − {frac(1,2)}", frac(1, 6, True)),
      (f"{frac(3,4,True)} − {frac(2,3)}", f'{frac(17,12,True)} = −1{frac(5,12)}')]
T6 = [("Morgens zeigt das Thermometer −7 °C. Bis mittags steigt die Temperatur um 11 °C, bis abends sinkt sie um 9 °C. "
       "Wie warm ist es abends?", "−7 + 11 − 9 = −5", "Abends sind es −5 °C."),
      ("Auf dem Konto sind −120 €. Es werden 250 € eingezahlt und danach 180 € abgebucht. "
       "Wie ist der Kontostand?", "−120 + 250 − 180 = −50", "Der Kontostand beträgt −50 €.")]


def buchstabe(i):
    return "abcdefgh"[i]


def spalten(items, cols, loesung=False, kurz=False):
    out = []
    for i, (t, r) in enumerate(items):
        res = m(r) if isinstance(r, (int, float)) else r
        rest = f'<b class="l">{res}</b>' if loesung else '<span class="blank"></span>'
        out.append(f'<div class="it"><span class="b">{buchstabe(i)})</span> {t} = {rest}</div>')
    return f'<div class="cols c{cols}">{"".join(out)}</div>'


def aufgabe(nr, stufe, text, inhalt):
    return (f'<div class="auf"><div class="kopf">{kreis(stufe)}<span class="nr">{nr}</span>'
            f'<span class="txt">{text}</span></div>{inhalt}</div>')


def blatt(loesung):
    a = []
    a.append(aufgabe(1, 0, "Berechne im Kopf.", spalten(T1, 4, loesung)))
    a.append(aufgabe(2, 0, "Überlege zuerst, ob das Ergebnis positiv oder negativ ist. Berechne dann.",
                     spalten(T2, 4, loesung)))
    karten = "".join(f'<span class="karte k{i % 3}">{m(v)}</span>' for i, v in enumerate(T3_KARTEN))
    a.append(aufgabe(3, 1, "Berechne. Das Ergebnis steht auf einem der Kärtchen.",
                     spalten(T3, 3, loesung) + ('' if loesung else f'<div class="karten">{karten}</div>')))
    z4 = []
    for i, (falsch, richtig, r) in enumerate(T4):
        rest = f'<b class="l">{richtig} = {m(r)}</b>' if loesung else '<span class="blank long"></span>'
        z4.append(f'<div class="it"><span class="b">{buchstabe(i)})</span> <span class="fehl">{falsch}</span>'
                  f'<span class="pf">&rarr;</span> {rest}</div>')
    a.append(aufgabe(4, 1, 'Hier hat sich ein <span class="rot">Fehler</span> eingeschlichen. Korrigiere.',
                     f'<div class="cols c2">{"".join(z4)}</div>'))
    a.append(aufgabe(5, 2, "Berechne. Achte beim Rechnen mit Brüchen auf gleiche Nenner.", spalten(T5, 2, loesung)))
    z6 = []
    for i, (t, rech, ant) in enumerate(T6):
        if loesung:
            z6.append(f'<div class="sach"><span class="b">{buchstabe(i)})</span> {t}<div class="ls"><b class="l">'
                      f'{rech}. {ant}</b></div></div>')
        else:
            z6.append(f'<div class="sach"><span class="b">{buchstabe(i)})</span> {t}<div class="ls">'
                      f'<span class="zl"></span><span class="zl"></span></div></div>')
    a.append(aufgabe(6, 2, "Löse die Sachaufgaben. Schreibe die Rechnung und einen Antwortsatz auf.", "".join(z6)))
    titel = "Addieren und Subtrahieren" + (" – Lösungen (nur für mich)" if loesung else "")
    name = '' if loesung else '<div class="name">Name: ______________________ &nbsp;&nbsp; Datum: ____________</div>'
    return f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title><style>{CSS}</style></head><body>
<div class="seite"><header><div><h1>{titel}</h1>
<div class="sub">Klasse 7c · Rationale Zahlen</div></div>{name}</header>
<div class="legende">Schwierigkeit: {kreis(0)} leicht &nbsp;&nbsp; {kreis(1)} mittel &nbsp;&nbsp; {kreis(2)} schwer</div>
{"".join(a)}</div></body></html>"""


CSS = f"""
@page{{size:A4;margin:11mm 13mm}}
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{margin:0;font:11.5pt/1.35 Helvetica,Arial,sans-serif;color:#1b1b1b}}
header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #1b1b1b;padding-bottom:5px}}
h1{{font-size:18pt;margin:0;color:{ACC}}}.sub{{color:#555;font-size:10pt}}
.name{{font-size:10.5pt;color:#333;white-space:nowrap}}
.legende{{font-size:10pt;color:#333;margin:6px 0 4px}}
.lvl{{vertical-align:-3px}}
.auf{{margin:7px 0 0;break-inside:avoid}}
.kopf{{display:flex;align-items:center;gap:6px;margin-bottom:3px}}
.nr{{font-size:15pt;font-weight:700;color:{ACC};min-width:16px}}
.txt{{font-size:11.5pt}}.rot{{color:#c0271c;font-weight:700}}
.cols{{display:grid;gap:4px 14px;padding-left:24px}}
.c4{{grid-template-columns:repeat(4,1fr)}}.c3{{grid-template-columns:repeat(3,1fr)}}.c2{{grid-template-columns:repeat(2,1fr)}}
.it{{white-space:nowrap;padding:2px 0}}
.b{{color:#333}}
.blank{{display:inline-block;width:17mm;border-bottom:1px solid #444;height:1em;vertical-align:baseline}}
.blank.long{{width:33mm}}
.l{{color:#1d5fa8}}
.fehl{{color:#333;font-size:11pt}}.pf{{margin:0 6px;color:#666}}
.karten{{padding:6px 0 2px 24px;display:flex;gap:10px}}
.karte{{display:inline-block;border:1px solid #9bc59b;background:#e1f1d9;padding:1px 10px;border-radius:2px;font-weight:600}}
.k0{{transform:rotate(-3deg)}}.k1{{transform:rotate(2deg)}}.k2{{transform:rotate(-1deg)}}
.sach{{padding:3px 0 0 24px}}.sach .ls{{padding:5px 0 0 0}}
.zl{{display:block;border-bottom:1px solid #999;height:20px;margin-bottom:6px}}
.zl+.zl{{}}
.frac{{display:inline-block;vertical-align:-.55em;text-align:center;font-size:.8em;margin:0 1px}}
.frac>span{{display:block;padding:0 .15em;line-height:1.1}}.frac .u{{border-top:1px solid #1b1b1b}}
"""

hier = Path(__file__).parent
(hier / "Rationale Zahlen 2 – Arbeitsblatt Plus und Minus.html").write_text(blatt(False), encoding="utf-8")
(hier / "Rationale Zahlen 2 – Arbeitsblatt Plus und Minus – Lösungen (nur für mich).html").write_text(blatt(True), encoding="utf-8")
print("geschrieben")
