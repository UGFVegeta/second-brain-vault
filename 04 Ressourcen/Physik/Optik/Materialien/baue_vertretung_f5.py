#!/usr/bin/env python3
"""Vertretung Physik 7c, Do 19.11.2026: Wiederholungsblatt zur letzten Stunde
(Einschub Jahreszeiten, Tag und Nacht, Leitfrage 5 bis 5.1 „Wo steht der Mond?“).
Finsternisse und die Mondphasen von der Erde aus kommen erst noch, deshalb nicht auf dem Blatt.
Zwei Seiten Schülerblatt, Lösung = dasselbe Blatt ausgefüllt in Magenta.
Zeichnungen als berechnete SVG auf 5-mm-Karo (Einheiten im SVG = mm)."""
import math, re, subprocess
from pathlib import Path

HIER = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAG = "#E6007E"
SONNE, SONNE_RAND = "#FFD34D", "#B98900"
ERDE, ERDE_RAND = "#CFE2F5", "#3B7CC4"
MOND, MOND_RAND = "#FFFFFF", "#66798E"
GRAU = "#9AA3AF"
TITEL = "Wiederholung: Tag und Nacht, Jahreszeiten, Mond"
BASIS = "Wiederholung F5 Tag und Nacht, Jahreszeiten, Mond"


# ------------------------------------------------------------ Hilfen
def kopf(loesung):
    lm = '<div class="loesung-marker">Lösung</div>' if loesung else ""
    return (f'<div class="kopf"><div><span class="chip">F5</span><h1>{TITEL}</h1></div>{lm}</div>'
            '<p class="hinweis" style="margin:2mm 0">○ leicht &nbsp;&nbsp; ◐ mittel &nbsp;&nbsp; ● schwer</p>')


def aufgabe(nr, titel, kreis):
    return f'<h2 class="aufgabe"><span class="nr">{nr}</span>{titel} <span class="kreis">{kreis}</span></h2>'


def luecken(text, loesung):
    """[[wort]] wird zur Lücke, in der Lösung zum Wort in Magenta. Gleiche Breite in Blatt und Lösung."""
    def ers(m):
        kurz = " kurz" if len(m.group(1)) < 8 else ""
        return (f'<span class="luecke loesungstext{kurz}">{m.group(1)}</span>' if loesung
                else f'<span class="luecke{kurz}"></span>')
    return re.sub(r"\[\[(.+?)\]\]", ers, text)


def linien(n, text, loesung):
    if loesung:
        return f'<p class="antwort loesungstext" style="min-height:{n * 7}mm">{text}</p>'
    return '<div class="linien">' + '<div class="linie"></div>' * n + '</div>'


def karo(w, h):
    s = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>']
    s += [f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(5, w, 5)]
    s += [f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(5, h, 5)]
    return (f'<g stroke="#C9CED6" stroke-width="0.18">{"".join(s)}</g>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="none" stroke="#9AA3B0" stroke-width="0.3"/>')


DEFS = ('<defs><marker id="pfeilgelb" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto" markerUnits="userSpaceOnUse">'
        f'<path d="M0,0.6 L4.4,2.5 L0,4.4 Z" fill="{SONNE_RAND}"/></marker>'
        '<marker id="pfeilgrau" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto" markerUnits="userSpaceOnUse">'
        '<path d="M0,0.6 L4.4,2.5 L0,4.4 Z" fill="#3b4150"/></marker></defs>')


def svg(w, h, inhalt):
    return (f'<svg class="feld" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif">{DEFS}{karo(w, h)}{inhalt}</svg>')


def txt(x, y, t, size=3.4, farbe="#3b4150", anker="middle", gewicht=500):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{farbe}" text-anchor="{anker}" font-weight="{gewicht}">{t}</text>'


def kreisform(x, y, r, fill, stroke, sw=0.35):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def rechte_haelfte_dunkel(x, y, r, farbe=GRAU):
    """Sonne von links: die rechte Hälfte bekommt kein Licht."""
    return f'<path d="M{x:.2f} {y - r:.2f} A{r} {r} 0 0 1 {x:.2f} {y + r:.2f}Z" fill="{farbe}"/>'


def sonnenlicht(ys, x1=6, x2=38, label_y=None):
    s = [f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{SONNE_RAND}" stroke-width="0.45" marker-end="url(#pfeilgelb)"/>' for y in ys]
    if label_y is not None:
        s.append(txt((x1 + x2) / 2, label_y, "Sonnenlicht", 3.2, SONNE_RAND))
    return "".join(s)


def drehpfeil(cx, cy, r, von, bis):
    """Pfeil auf einem Kreisbogen, gegen den Uhrzeigersinn (Winkel mathematisch, in Grad)."""
    a1, a2 = math.radians(von), math.radians(bis)
    x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
    x2, y2 = cx + r * math.cos(a2), cy - r * math.sin(a2)
    return (f'<path d="M{x1:.2f} {y1:.2f} A{r} {r} 0 0 0 {x2:.2f} {y2:.2f}" fill="none" stroke="#3b4150" '
            'stroke-width="0.4" marker-end="url(#pfeilgrau)"/>')


# ------------------------------------------------------------ 1 Richtig oder falsch
AUSSAGEN = [
    ("Die Erde dreht sich in 24 Stunden einmal um ihre eigene Achse.", True),
    ("Die Erde braucht für einen Umlauf um die Sonne einen Monat.", False),
    ("Die Erdachse ist geneigt.", True),
    ("Im Sommer ist die Erde näher an der Sonne als im Winter.", False),
    ("Im Winter verteilen sich die Sonnenstrahlen auf eine größere Fläche und erwärmen sie weniger.", True),
    ("Wenn bei uns Sommer ist, ist auf der Südhalbkugel Winter.", True),
    ("Der Mond ist eine Lichtquelle, er leuchtet selbst.", False),
    ("Der Mond läuft in etwa einem Monat einmal um die Erde.", True),
]


def richtig_falsch(loesung):
    def kaestchen(an):
        return f'<span class="kasten">{"✗" if (loesung and an) else ""}</span>'
    zeilen = "".join(f'<tr><td>{t}</td><td class="rf">{kaestchen(r)}</td><td class="rf">{kaestchen(not r)}</td></tr>'
                     for t, r in AUSSAGEN)
    return (aufgabe(1, "Richtig oder falsch? Kreuze an.", "○")
            + f'<table class="rftab"><tr><th></th><th>richtig</th><th>falsch</th></tr>{zeilen}</table>')


# ------------------------------------------------------------ 2 Tag und Nacht
def tag_und_nacht(loesung):
    W, H = 170, 42
    ex, ey, er = 98, 21, 14
    s = [sonnenlicht((7, 16, 25, 34), label_y=40)]
    s.append(kreisform(ex, ey, er, ERDE, ERDE_RAND))
    if loesung:
        s.append(rechte_haelfte_dunkel(ex, ey, er, "#7F8A9A"))
        s.append(kreisform(ex, ey, er, "none", ERDE_RAND))
        s.append(txt(ex - 7, ey + 1.3, "Tag", 3.8, MAG, "middle", 700))
        s.append(txt(ex + 7.5, ey + 1.3, "Nacht", 3.8, "#FFFFFF", "middle", 700))
        # Sonnenaufgang: oben auf der Grenze zwischen Tag und Nacht (Drehung gegen den Uhrzeigersinn)
        s.append(f'<g stroke="{MAG}" stroke-width="0.6"><line x1="{ex - 1.6}" y1="{ey - er - 1.6}" x2="{ex + 1.6}" y2="{ey - er + 1.6}"/>'
                 f'<line x1="{ex - 1.6}" y1="{ey - er + 1.6}" x2="{ex + 1.6}" y2="{ey - er - 1.6}"/></g>')
        s.append(txt(ex + 4, ey - er - 1.2, "Sonnenaufgang", 3.0, MAG, "start", 700))
    s.append(f'<circle cx="{ex}" cy="{ey}" r="0.8" fill="#14171c"/>')
    s.append(txt(ex, ey + 4.5, "Nordpol", 2.6, "#14171c"))
    s.append(drehpfeil(ex, ey, er + 4, -60, -20))
    s.append(txt(ex + 21, ey + 12, "Drehung", 3.0, "#3b4150", "start"))
    s.append(txt(167, 40, "Blick von oben auf den Nordpol", 3.0, "#66798E", "end"))
    return (aufgabe(3, "Tag und Nacht", "◐")
            + '<p class="frage"><b>a)</b> Die Sonne scheint von links. Male die Hälfte der Erde dunkel aus, die kein Sonnenlicht bekommt. '
              'Schreibe <b>Tag</b> und <b>Nacht</b> in die richtige Hälfte.<br>'
              '<b>b)</b> <span class="kreis">●</span> Die Erde dreht sich in Pfeilrichtung. Markiere mit einem Kreuz einen Ort, '
              'an dem gerade die Sonne aufgeht.</p>'
            + svg(W, H, "".join(s)))


# ------------------------------------------------------------ 3 Steile und flache Sonnenstrahlen
def strahlenbuendel(x_mitte, boden, hoehe_grad, sonne_abstand, n=5, breite=10.0, loesung=False):
    """Paralleles Bündel mit fester Breite (senkrecht zu den Strahlen), trifft bei boden auf."""
    e = math.radians(hoehe_grad)
    dx, dy = math.cos(e), math.sin(e)            # Richtung nach rechts unten
    fuss = breite / math.sin(e)                  # beleuchtete Länge auf dem Boden
    s = []
    for i in range(n):
        xb = x_mitte - fuss / 2 + i * fuss / (n - 1)
        laenge = sonne_abstand - 6
        s.append(f'<line x1="{xb - dx * laenge:.2f}" y1="{boden - dy * laenge:.2f}" x2="{xb:.2f}" y2="{boden}" '
                 f'stroke="{SONNE_RAND}" stroke-width="0.45"/>')
    sx, sy = x_mitte - dx * sonne_abstand, boden - dy * sonne_abstand
    s.append(kreisform(sx, sy, 4.5, SONNE, SONNE_RAND))
    if loesung:
        s.append(f'<line x1="{x_mitte - fuss / 2:.2f}" y1="{boden}" x2="{x_mitte + fuss / 2:.2f}" y2="{boden}" stroke="{MAG}" stroke-width="1.6"/>')
    return "".join(s), fuss


def steil_und_flach(loesung):
    W, H, boden = 170, 44, 34
    s = []
    teil1, _ = strahlenbuendel(50, boden, 62, 30, loesung=loesung)
    teil2, _ = strahlenbuendel(140, boden, 24, 52, loesung=loesung)
    s.append(teil1 + teil2)
    for x1, x2 in ((5, 80), (90, 165)):
        s.append(f'<line x1="{x1}" y1="{boden}" x2="{x2}" y2="{boden}" stroke="#14171c" stroke-width="0.5"/>')
    s.append(f'<line x1="85" y1="2" x2="85" y2="{H - 2}" stroke="#7C8592" stroke-width="0.35" stroke-dasharray="1.6 1.2"/>')
    s.append(txt(82, 6, "Sommer: Sonne steht hoch", 3.0, "#14171c", "end", 600))
    s.append(txt(167, 6, "Winter: Sonne steht tief", 3.0, "#14171c", "end", 600))
    s.append(txt(5, 42, "Erdboden", 2.8, "#66798E", "start"))
    if loesung:
        s.append(txt(50, 40.5, "kleine Fläche: stark erwärmt", 3.0, MAG, "middle", 700))
        s.append(txt(140, 40.5, "große Fläche: schwach erwärmt", 3.0, MAG, "middle", 700))
    satz = luecken("Im Sommer fallen die Sonnenstrahlen [[steil]] ein und treffen eine [[kleine]] Fläche. "
                   "Im Winter fallen sie [[flach]] ein. Dieselbe Strahlung verteilt sich auf eine [[große]] Fläche. "
                   "Jeder Quadratmeter Boden wird deshalb [[weniger]] erwärmt.", loesung)
    return (aufgabe(4, "Steile und flache Sonnenstrahlen", "◐")
            + '<p class="frage">Beide Strahlenbündel sind gleich breit. Markiere in beiden Bildern rot die Fläche auf dem Boden, '
              'die von den Strahlen getroffen wird. Schreibe darunter, ob sie stark oder schwach erwärmt wird.</p>'
            + svg(W, H, "".join(s)) + f'<p class="frage lt">{satz}</p>')


# ------------------------------------------------------------ 4 Jahreszeiten
def jahreszeiten(loesung):
    return (aufgabe(5, "Warum gibt es Jahreszeiten?", "◐")
            + '<p class="frage"><b>a)</b> Erkläre, warum es bei uns im Sommer wärmer ist als im Winter. '
              'Benutze die Wörter <b>Erdachse</b>, <b>geneigt</b>, <b>steil</b>, <b>flach</b> und <b>Fläche</b>.</p>'
            + linien(4, "Die Erdachse ist geneigt. Im Sommer ist unsere Nordhalbkugel zur Sonne geneigt. Die Sonne steht hoch, "
                        "ihre Strahlen fallen steil ein und erwärmen eine kleine Fläche stark. Im Winter fallen die Strahlen flach ein, "
                        "dieselbe Strahlung verteilt sich auf eine große Fläche, der Boden wird weniger erwärmt.", loesung)
            + '<p class="frage"><b>b)</b> <span class="kreis">●</span> Im Juni ist in Australien Winter. Erkläre.</p>'
            + linien(2, "Australien liegt auf der Südhalbkugel. Im Juni ist die Südhalbkugel von der Sonne weg geneigt, "
                        "die Strahlen fallen dort flach ein.", loesung))


# ------------------------------------------------------------ 5 Wo steht der Mond?
def mond_bahn(loesung):
    W, H = 170, 74
    ex, ey, er, bahn, mr = 108, 36, 7, 26, 4.8
    s = [sonnenlicht((9, 21, 33, 45, 57), label_y=68)]
    s.append(f'<circle cx="{ex}" cy="{ey}" r="{bahn}" fill="none" stroke="#7C8592" stroke-width="0.35" stroke-dasharray="1.6 1.2"/>')
    s.append(drehpfeil(ex, ey, bahn + 4.5, -60, -28))
    s.append(txt(ex + 26, ey + 28, "Umlauf", 3.0, "#3b4150", "start"))
    s.append(kreisform(ex, ey, er, ERDE, ERDE_RAND))
    if loesung:
        s.append(rechte_haelfte_dunkel(ex, ey, er, "#7F8A9A"))
        s.append(kreisform(ex, ey, er, "none", ERDE_RAND))
    s.append(txt(ex, ey + er + 4, "Erde", 3.2, ERDE_RAND))
    for grad in (180, 270, 0, 90):
        a = math.radians(grad)
        mx, my = ex + bahn * math.cos(a), ey - bahn * math.sin(a)
        s.append(kreisform(mx, my, mr, MOND, MOND_RAND))
        if loesung:
            s.append(rechte_haelfte_dunkel(mx, my, mr))
            s.append(kreisform(mx, my, mr, "none", MOND_RAND))
    s.append(txt(ex - bahn - 7.5, ey + 1.2, "Mond", 3.0, MOND_RAND, "end"))
    s.append(txt(167, 71, "Blick von oben auf den Nordpol", 3.0, "#66798E", "end"))
    satz = luecken("Der Mond ist keine [[Lichtquelle]], sondern ein [[beleuchteter Körper]]. Die Sonne beleuchtet immer "
                   "genau eine [[Hälfte]]. Hell ist immer die Seite, die zur [[Sonne]] zeigt. Auf seiner Bahn um die Erde "
                   "sehen wir davon [[unterschiedlich viel]].", loesung)
    return (aufgabe(2, "Wo steht der Mond?", "○")
            + '<p class="frage">Der Mond läuft um die Erde, die Sonne scheint von links. Male bei der Erde und bei jedem Mond '
              'die Hälfte dunkel aus, die kein Sonnenlicht bekommt.</p>'
            + svg(W, H, "".join(s)) + f'<p class="frage lt">{satz}</p>')


# ------------------------------------------------------------ Dokument
STIL = """
html,body{font-size:11.0pt !important;line-height:1.5}h2.aufgabe{font-size:11.9pt}.hinweis{font-size:9.6pt}table.rftab,table.rftab td{font-size:11.0pt}p.antwort{font-size:11.0pt}.kopf h1{font-size:15.6pt}

.hinweis{font-size:8.2pt;color:#66798E}
svg.feld{display:block;margin:1.5mm 0 2mm}
p.lt{line-height:2.05}
.luecke{min-width:42mm;height:8mm;vertical-align:bottom}.luecke.kurz{min-width:26mm}.luecke.loesungstext{height:auto}
p.antwort{margin:1mm 0 3mm;line-height:1.6;font-size:9.6pt}
.linien .linie{height:8.5mm}
h2.aufgabe{margin:3mm 0 1.2mm}
table.rftab{border-collapse:collapse;width:100%;font-size:9.2pt;margin:1mm 0 2mm}
table.rftab th{font-size:7.8pt;font-weight:600;color:#66798E;text-align:center;padding:0 0 1mm;width:16mm}
table.rftab th:first-child{width:auto}
table.rftab td{border-bottom:0.4pt solid #dfe2e7;padding:0.9mm 1mm}
table.rftab td.rf{text-align:center}
.kasten{display:inline-block;width:4.6mm;height:4.6mm;border:0.5pt solid #14171c;line-height:4.4mm;
        text-align:center;color:#E6007E;font-weight:700;font-size:9.2pt}
"""


def blatt(loesung):
    s1 = kopf(loesung) + ("" if loesung else '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>') \
        + richtig_falsch(loesung) + mond_bahn(loesung)
    s2 = tag_und_nacht(loesung) + steil_und_flach(loesung) + jahreszeiten(loesung)
    return f'<div class="seite">{s1}</div><div class="seite">{s2}</div>'


def kreise_einheitlich(html):
    """○ ◐ ● als gleich große SVG-Kreise (Schriftzeichen sind je nach Font verschieden groß)."""
    def k(art):
        f = {"○": "", "◐": '<path d="M5,1 A4,4 0 0 0 5,9 Z" fill="#222"/>', "●": '<circle cx="5" cy="5" r="4" fill="#222"/>'}[art]
        return (f'<svg width="3.4mm" height="3.4mm" viewBox="0 0 10 10" style="vertical-align:-0.5mm"><title>{art}</title>'
                f'<circle cx="5" cy="5" r="4" fill="none" stroke="#222" stroke-width="1.1"/>{f}</svg>')
    for z in "○◐●":
        html = html.replace(z, k(z))
    return html



def dokument(titel, inhalt):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title>'
            f'<link rel="stylesheet" href="ab-vorlage.css"><style>{STIL}</style></head><body>{kreise_einheitlich(inhalt)}</body></html>')


def drucke(html_name, pdf_name):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / pdf_name}",
                    "--virtual-time-budget=4000", f"file://{HIER / html_name}"], check=True, capture_output=True)
    print("gedruckt:", pdf_name)


if __name__ == "__main__":
    for html, pdf, loes in (("wiederholung-f5.html", f"{BASIS}.pdf", False),
                            ("wiederholung-f5-loesung.html", f"{BASIS} – Lösung.pdf", True)):
        (HIER / html).write_text(dokument(BASIS + (" – Lösung" if loes else ""), blatt(loes)), encoding="utf-8")
        drucke(html, pdf)
