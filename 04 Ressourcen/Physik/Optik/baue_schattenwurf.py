#!/usr/bin/env python3
"""Rückseite zum Versuchsblatt W06 (F4, Kern- und Halbschatten): „Schattenwurf“ nach Oskars Vorlage, neu gezeichnet.
Fünf Situationen mit Lampe(n), Hindernis(sen) und Schirm. Die Schüler zeichnen die Randstrahlen ein, schraffieren
die Schattenräume und füllen die Lücken. Alle Schatten sind aus der Geometrie berechnet (Strahlensatz), nicht geschätzt.
Aufruf: python3 baue_schattenwurf.py
  -> Materialien/Schattenwurf W06 Rückseite.pdf (Seite 1 Aufgaben, Seite 2 Lösung)
  -> Materialien/Kern- und Halbschatten W06 – Druck doppelseitig.pdf (Vorderseite Versuch, Rückseite Schattenwurf)"""
import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter

HIER = Path(__file__).parent
MAT = HIER / "Materialien"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 260, 125            # Zeichenfläche (viewBox)
XL, XO, XS = 18, 120, 238  # Lampen, Hindernisse, Schirm
INK, KS, HS = "#14171c", "#6f7784", "#c9ced6"

# (Lampen-y, Hindernisse als (oben, unten), Lückentext Aufgabe, Lückentext Lösung)
SITUATIONEN = [
    ([62], [(50, 74)],
     'Der Schatten auf dem Schirm ist {L1}, denn dieses Gebiet erhält kein Licht von der Lichtquelle.', ["Kernschatten"]),
    ([40, 84], [(55, 69)],
     'Die Schatten oben und unten sind {L1}, denn das jeweilige Gebiet erhält Licht nur von einer Lichtquelle. '
     'Die zweite Lichtquelle sendet kein Licht in dieses Gebiet.', ["Halbschatten"]),
    ([50, 74], [(48, 76)],
     'Der Schatten in der Mitte heißt {L1}, denn dieses Gebiet erhält von keiner Lichtquelle Licht. '
     'Oben und unten entsteht {L2}.', ["Kernschatten", "Halbschatten"]),
    ([62], [(40, 50), (74, 84)],
     'Es gibt zwei Bereiche mit {L1} und {L2} Bereiche, die Licht haben.', ["Kernschatten", "drei"]),
    ([54, 70], [(42, 56), (68, 82)],
     'Es entstehen mehrere {L1} und {L2}. Zwischen den Hindernissen gibt es einen Bereich, der Licht von {L3} erhält.',
     ["Halbschatten", "Kernschatten", "beiden Lichtquellen"]),
]


def auf_schirm(yl, y):
    """Punkt auf dem Schirm, den der Strahl von der Lampe (XL, yl) durch (XO, y) trifft."""
    return yl + (y - yl) * (XS - XL) / (XO - XL)


def schirm_abschnitte(lampen, hindernisse):
    """Schirm in Abschnitte teilen; pro Abschnitt zählen, wie viele Lampen verdeckt sind."""
    grenzen = {0.0, float(H)}
    schatten = []
    for yl in lampen:
        s = [(auf_schirm(yl, a), auf_schirm(yl, b)) for a, b in hindernisse]
        schatten.append(s)
        for a, b in s:
            grenzen |= {min(max(a, 0), H), min(max(b, 0), H)}
    g = sorted(grenzen)
    out = []
    for a, b in zip(g, g[1:]):
        if b - a < 0.5:
            continue
        m = (a + b) / 2
        verdeckt = sum(any(x <= m <= y for x, y in s) for s in schatten)
        out.append((a, b, verdeckt))
    return out


def zeichnung(lampen, hindernisse, loesung):
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="c"><rect x="0" y="0" width="{XS}" height="{H}"/></clipPath></defs>']
    if loesung:
        o.append('<g clip-path="url(#c)">')
        for yl in lampen:          # Schattenraum jeder Lampe halbdurchsichtig: wo zwei übereinanderliegen, wird es dunkler (Kernschatten)
            for a, b in hindernisse:
                o.append(f'<polygon points="{XO},{a} {XS},{auf_schirm(yl, a):.1f} {XS},{auf_schirm(yl, b):.1f} {XO},{b}" '
                         f'fill="{KS if len(lampen) == 1 else "#8a929e"}" fill-opacity="{0.75 if len(lampen) == 1 else 0.42}"/>')
        for yl in lampen:          # Randstrahlen
            for a, b in hindernisse:
                for y in (a, b):
                    o.append(f'<line x1="{XL}" y1="{yl}" x2="{XS}" y2="{auf_schirm(yl, y):.1f}" stroke="#FF1F8A" stroke-width="0.9"/>')
        o.append("</g>")
        for a, b, n in schirm_abschnitte(lampen, hindernisse):
            if n == 0:
                continue
            txt = "KS" if n == len(lampen) else "HS"
            o.append(f'<text x="{XS + 5}" y="{(a + b) / 2 + 3:.1f}" font-size="8" font-weight="700" fill="#FF1F8A" '
                     f'font-family="Avenir Next, Helvetica, Arial">{txt}</text>')
    o.append(f'<line x1="{XS}" y1="2" x2="{XS}" y2="{H - 2}" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<text x="{XS - 3}" y="{H - 3}" font-size="6.5" text-anchor="end" fill="#66798e" font-family="Avenir Next, Helvetica, Arial">Schirm</text>')
    for a, b in hindernisse:
        o.append(f'<rect x="{XO - 1.8}" y="{a}" width="3.6" height="{b - a}" fill="{INK}"/>')
    for yl in lampen:
        o.append(f'<circle cx="{XL}" cy="{yl}" r="6" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
                 f'<path d="M{XL - 4.2} {yl - 4.2} L{XL + 4.2} {yl + 4.2} M{XL + 4.2} {yl - 4.2} L{XL - 4.2} {yl + 4.2}" stroke="{INK}" stroke-width="1.2"/>')
    o.append("</svg>")
    return "".join(o)


def seite(loesung):
    zeilen = ""
    for i, (lampen, hind, text, woerter) in enumerate(SITUATIONEN, 1):
        t = text
        for k, w in enumerate(woerter, 1):
            t = t.replace("{L%d}" % k, f'<span class="luecke loesungstext">{w}</span>' if loesung else '<span class="luecke"></span>')
        zeilen += (f'<tr><td class="bild"><span class="nrk">{"abcde"[i - 1]}</span>{zeichnung(lampen, hind, loesung)}</td>'
                   f'<td class="txt"><p class="frage">{t}</p></td></tr>')
    kopf = ('<div class="kopf"><div><span class="chip">W06</span><h1>F4 — Schattenwurf</h1></div>'
            + ('<div class="loesung-marker">Lösung</div>' if loesung else "") + "</div>")
    name = "" if loesung else '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>'
    legende = ('<p class="hinweis">⊗ Lichtquelle &nbsp;&nbsp; ▌ undurchsichtiger Körper &nbsp;&nbsp; | Schirm'
               + (' &nbsp;&nbsp; <b style="color:#FF1F8A">KS</b> Kernschatten, <b style="color:#FF1F8A">HS</b> Halbschatten' if loesung else "") + "</p>")
    return f"""<div class="seite">{kopf}{name}
<h2 class="aufgabe"><span class="nr">5</span>Schatten zeichnen</h2>
<p class="frage">Zeichne die Randstrahlen ein und schraffiere die Schattenräume. Den Kernschatten schraffierst du dichter als den Halbschatten.
Ergänze die Lücken mit den passenden Fachbegriffen.</p>{legende}
<table class="sw">{zeilen}</table></div>"""


CSS = """<style>
table.sw{width:100%;border-collapse:collapse;margin-top:2mm}
table.sw td{border:0.6pt solid #b9c0ca;vertical-align:middle;padding:1.5mm 2.5mm}
table.sw td.bild{width:88mm;position:relative}
table.sw td.bild svg{width:85mm;height:41mm;display:block}
table.sw .nrk{position:absolute;left:1.5mm;top:1mm;font-size:9pt;font-weight:600;color:#66798e}
table.sw td.txt p.frage{line-height:2.1;margin:0}
table.sw .luecke{min-width:30mm}
p.hinweis{font-size:9pt;color:#66798e;margin:1mm 0 0}
</style>"""


def main():
    html = MAT / "schattenwurf.html"
    html.write_text(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Schattenwurf – W06 Rückseite</title>'
                    f'<link rel="stylesheet" href="ab-vorlage.css">{CSS}</head><body>{seite(False)}{seite(True)}</body></html>', encoding="utf-8")
    pdf = MAT / "Schattenwurf W06 Rückseite.pdf"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "--virtual-time-budget=4000",
                    html.as_uri()], check=True, capture_output=True)
    n = len(PdfReader(str(pdf)).pages)
    print("geschrieben:", pdf.name, f"({n} Seiten)")
    druck = PdfWriter()
    druck.add_page(PdfReader(str(MAT / "Kern- und Halbschatten W06.pdf")).pages[0])
    druck.add_page(PdfReader(str(pdf)).pages[0])
    ziel = MAT / "Kern- und Halbschatten W06 – Druck doppelseitig.pdf"
    with open(ziel, "wb") as f:
        druck.write(f)
    print("geschrieben:", ziel.name, "(Vorderseite Versuch, Rückseite Schattenwurf)")
    for lampen, hind, _, _ in SITUATIONEN:
        print("  ", len(lampen), "Lampe(n):", [("KS" if n == len(lampen) else "HS" if n else "Licht", round(a), round(b))
                                              for a, b, n in schirm_abschnitte(lampen, hind)])


if __name__ == "__main__":
    main()
