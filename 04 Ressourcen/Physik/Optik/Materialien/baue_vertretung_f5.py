#!/usr/bin/env python3
"""Vertretung Physik 7c, Do 19.11.2026: Wiederholungsblatt F5 Mondphasen und Finsternisse
(plus Einschub Jahreszeiten). Zwei Seiten Schülerblatt, Lösung = dasselbe Blatt ausgefüllt in Magenta.
Zeichnungen als berechnete SVG auf 5-mm-Karo (Einheiten im SVG = mm)."""
import math, re, subprocess, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
from folien_zeichnungen import phase_pfad  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAG = "#E6007E"
SONNE, SONNE_RAND = "#FFD34D", "#B98900"
ERDE, ERDE_RAND = "#CFE2F5", "#3B7CC4"
MOND, MOND_RAND = "#FFFFFF", "#66798E"
GRAU = "#9AA3AF"
BASIS = "Wiederholung F5 Mondphasen und Finsternisse"


# ------------------------------------------------------------ Hilfen
def kopf(loesung):
    lm = '<div class="loesung-marker">Lösung</div>' if loesung else ""
    return (f'<div class="kopf"><div><span class="chip">F5</span><h1>Wiederholung: Mondphasen und Finsternisse</h1></div>{lm}</div>'
            '<p class="hinweis" style="margin:2mm 0">○ leicht &nbsp;&nbsp; ◐ mittel &nbsp;&nbsp; ● schwer</p>')


def aufgabe(nr, titel, kreis):
    return f'<h2 class="aufgabe"><span class="nr">{nr}</span>{titel} <span class="kreis">{kreis}</span></h2>'


def luecken(text, loesung):
    """[[wort]] wird zur Lücke, in der Lösung zum Wort in Magenta."""
    if loesung:
        return re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span class="luecke loesungstext{" kurz" if len(m.group(1)) < 8 else ""}">{m.group(1)}</span>', text)
    return re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span class="luecke{" kurz" if len(m.group(1)) < 8 else ""}"></span>', text)


def linien(n, text, loesung):
    if loesung:
        return f'<p class="antwort loesungstext">{text}</p>'
    return '<div class="linien">' + '<div class="linie"></div>' * n + '</div>'


def karo(w, h):
    s = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>']
    s += [f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(5, w, 5)]
    s += [f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(5, h, 5)]
    return (f'<g stroke="#C9CED6" stroke-width="0.18">{"".join(s)}</g>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="none" stroke="#9AA3B0" stroke-width="0.3"/>')


def svg(w, h, inhalt):
    return (f'<svg class="feld" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif">{karo(w, h)}{inhalt}</svg>')


def txt(x, y, t, size=3.4, farbe="#3b4150", anker="middle", gewicht=500):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{farbe}" text-anchor="{anker}" font-weight="{gewicht}">{t}</text>'


def kreisform(x, y, r, fill, stroke, sw=0.35):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def muster(id_, abstand, farbe):
    return (f'<pattern id="{id_}" patternUnits="userSpaceOnUse" width="{abstand}" height="{abstand}" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="{abstand}" stroke="{farbe}" stroke-width="0.35"/></pattern>')


def gerade(p, q, x):
    """y-Wert der Geraden durch p und q an der Stelle x."""
    return p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0])


# ------------------------------------------------------------ Seite 1
def lueckentext_grundlagen(loesung):
    t = ("Der Mond ist keine [[Lichtquelle]], sondern ein [[beleuchteter Körper]]. Die Sonne beleuchtet immer genau "
         "eine [[Hälfte]] des Mondes. Weil der Mond die Erde umläuft, sehen wir von dieser hellen Hälfte unterschiedlich viel. "
         "Von Neumond bis zum nächsten Neumond vergehen etwa [[29,5]] Tage. "
         "Mit seiner Anziehungskraft sorgt der Mond auf der Erde für [[Ebbe]] und [[Flut]].")
    return aufgabe(1, "Warum sieht der Mond nicht immer gleich aus?", "○") + '<p class="frage">Fülle die Lücken aus.</p>' \
        + f'<p class="frage lt">{luecken(t, loesung)}</p>'


# Draufsicht: Sonne links, Erde in der Mitte, Mond läuft gegen den Uhrzeigersinn (Blick auf den Nordpol)
DRAUF_W, DRAUF_H = 170, 66
EX, EY, ER, BAHN, MR = 105, 33, 6.5, 22, 4.5
# (Buchstabe, Winkel in Grad mathematisch, Anteil am Umlauf f, Name). Neumond zur Sonne hin (links).
POSITIONEN = [("A", 180, 0.0, "Neumond"), ("B", 270, 0.25, "zunehmender Halbmond"),
              ("C", 0, 0.5, "Vollmond"), ("D", 90, 0.75, "abnehmender Halbmond")]


def draufsicht(loesung):
    s = []
    # Sonnenlicht von links
    for y in (8, 18, 28, 38, 48, 58):
        s.append(f'<line x1="6" y1="{y}" x2="40" y2="{y}" stroke="{SONNE_RAND}" stroke-width="0.45" marker-end="url(#pfeilgelb)"/>')
    s.append(txt(23, 63.5, "Sonnenlicht", 3.2, SONNE_RAND))
    # Bahn
    s.append(f'<circle cx="{EX}" cy="{EY}" r="{BAHN}" fill="none" stroke="#7C8592" stroke-width="0.35" stroke-dasharray="1.6 1.2"/>')
    # Umlaufrichtung: Pfeil unten rechts, gegen den Uhrzeigersinn (auf dem Bildschirm: unten nach rechts)
    a1, a2 = math.radians(-60), math.radians(-30)
    rr = BAHN + 4.5
    x1, y1 = EX + rr * math.cos(a1), EY - rr * math.sin(a1)
    x2, y2 = EX + rr * math.cos(a2), EY - rr * math.sin(a2)
    s.append(f'<path d="M{x1:.2f} {y1:.2f} A{rr} {rr} 0 0 0 {x2:.2f} {y2:.2f}" fill="none" stroke="#3b4150" stroke-width="0.4" marker-end="url(#pfeilgrau)"/>')
    s.append(txt(EX + 24, EY + 24, "Umlauf", 3.2, "#3b4150", "start"))
    # Erde: Tagseite links hell, Nachtseite rechts dunkel
    s.append(kreisform(EX, EY, ER, ERDE, ERDE_RAND))
    s.append(f'<path d="M{EX} {EY - ER} A{ER} {ER} 0 0 1 {EX} {EY + ER}Z" fill="#3B4A63" opacity="0.75"/>')
    s.append(kreisform(EX, EY, ER, "none", ERDE_RAND))
    s.append(txt(EX, EY + ER + 4, "Erde", 3.2, ERDE_RAND))
    # Monde
    for buchst, grad, f, name in POSITIONEN:
        a = math.radians(grad)
        mx, my = EX + BAHN * math.cos(a), EY - BAHN * math.sin(a)
        s.append(kreisform(mx, my, MR, MOND, MOND_RAND))
        if loesung:  # rechte Hälfte (sonnenabgewandt) dunkel
            s.append(f'<path d="M{mx:.2f} {my - MR:.2f} A{MR} {MR} 0 0 1 {mx:.2f} {my + MR:.2f}Z" fill="{GRAU}"/>')
            s.append(kreisform(mx, my, MR, "none", MOND_RAND))
        # Buchstabe außen neben dem Mond
        lx, ly = EX + (BAHN + 8.5) * math.cos(a), EY - (BAHN + 8.5) * math.sin(a) + 1.4
        s.append(txt(round(lx, 2), round(ly, 2), buchst, 4.2, "#14171c", "middle", 700))
    s.append(txt(167, 63.5, "Blick von oben auf den Nordpol", 3.0, "#66798E", "end"))
    defs = ('<defs><marker id="pfeilgelb" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto" markerUnits="userSpaceOnUse">'
            f'<path d="M0,0.6 L4.4,2.5 L0,4.4 Z" fill="{SONNE_RAND}"/></marker>'
            '<marker id="pfeilgrau" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto" markerUnits="userSpaceOnUse">'
            '<path d="M0,0.6 L4.4,2.5 L0,4.4 Z" fill="#3b4150"/></marker></defs>')
    return svg(DRAUF_W, DRAUF_H, defs + "".join(s))


def ansicht_kreis(f, loesung):
    if not loesung:
        return '<svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="26" fill="#FFFFFF" stroke="#14171c" stroke-width="1.2"/></svg>'
    hell = phase_pfad(30, 30, 26, f).replace('fill="#FFF6D8"', 'fill="#FFFFFF"')
    return (f'<svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="26" fill="{GRAU}"/>{hell}'
            '<circle cx="30" cy="30" r="26" fill="none" stroke="#14171c" stroke-width="1.2"/></svg>')


def mondphasen(loesung):
    phasen = "".join(
        f'<div class="phase"><div class="stellung"><b>{b}</b></div>{ansicht_kreis(f, loesung)}'
        f'<div class="name{" loesungstext" if loesung else ""}">{name if loesung else ""}</div></div>'
        for b, _, f, name in POSITIONEN)
    return (aufgabe(2, "Mondphasen zeichnen", "◐")
            + '<p class="frage"><b>a)</b> Die Sonne beleuchtet den Mond von links. Male bei jedem Mond A bis D die Hälfte dunkel aus, '
              'die kein Sonnenlicht bekommt.</p>'
            + draufsicht(loesung)
            + '<p class="frage"><b>b)</b> So sieht man den Mond von der Erde aus. Male in jedem Kreis den dunklen Teil aus '
              'und schreibe den Namen der Mondphase darunter.</p>'
            + f'<div class="phasen">{phasen}</div>')


# ------------------------------------------------------------ Seite 2: Finsternisse
FIN_W, FIN_H = 170, 50
SX, SY, SR = 15, 25, 12  # Sonne


def sonnenfinsternis(loesung):
    mx, mr = 95, 5          # Mond
    ex, er = 150, 17.5      # Erde
    s = [kreisform(SX, SY, SR, SONNE, SONNE_RAND), txt(SX, SY + SR + 5, "Sonne", 3.2, SONNE_RAND)]
    loes = ""
    if loesung:
        st, sb = (SX, SY - SR), (SX, SY + SR)
        mt, mb = (mx, SY - mr), (mx, SY + mr)
        xe = ex  # Strahlen enden an der Erdmitte, die Erde wird darüber gezeichnet (Schatten auf der Tagseite)
        # Kernschatten: Sonne oben -> Mond oben, Sonne unten -> Mond unten
        k_o, k_u = (xe, gerade(st, mt, xe)), (xe, gerade(sb, mb, xe))
        # Halbschatten-Grenzen: Sonne unten -> Mond oben, Sonne oben -> Mond unten
        h_o, h_u = (xe, gerade(sb, mt, xe)), (xe, gerade(st, mb, xe))
        loes += f'<defs>{muster("dicht", 0.9, MAG)}{muster("locker", 2.2, MAG)}</defs><g>'
        loes += f'<polygon points="{mt[0]},{mt[1]} {k_o[0]},{k_o[1]:.2f} {k_u[0]},{k_u[1]:.2f} {mb[0]},{mb[1]}" fill="url(#dicht)"/>'
        loes += f'<polygon points="{mt[0]},{mt[1]} {h_o[0]},{h_o[1]:.2f} {k_o[0]},{k_o[1]:.2f}" fill="url(#locker)"/>'
        loes += f'<polygon points="{mb[0]},{mb[1]} {h_u[0]},{h_u[1]:.2f} {k_u[0]},{k_u[1]:.2f}" fill="url(#locker)"/></g>'
        strahlen, enden = [], []
        for p, q in ((st, mt), (sb, mb), (sb, mt), (st, mb)):
            # Strahl bis zur Erdoberfläche (Schnitt Gerade/Kreis, linker Schnittpunkt) oder bis x = ex
            m = (q[1] - p[1]) / (q[0] - p[0]); c = p[1] - m * p[0]
            A, B, C = 1 + m * m, 2 * (m * (c - SY) - ex), ex * ex + (c - SY) ** 2 - er * er
            d = B * B - 4 * A * C
            xend = (-B - math.sqrt(d)) / (2 * A) if d >= 0 else ex
            strahlen.append(f'<line x1="{p[0]}" y1="{p[1]}" x2="{xend:.2f}" y2="{m * xend + c:.2f}" stroke="{MAG}" stroke-width="0.45"/>')
            enden.append((xend, m * xend + c))
        s.append(loes)
    s.append(kreisform(ex, SY, er, ERDE, ERDE_RAND))
    s.append(txt(ex, SY + er + 4.6, "Erde", 3.2, ERDE_RAND))
    if loesung:
        s += strahlen
        (x1, y1), (x2, y2) = enden[0], enden[1]   # Kernschatten trifft die Erde: dunkler Fleck
        s.append(f'<path d="M{x1:.2f} {y1:.2f} A{er} {er} 0 0 0 {x2:.2f} {y2:.2f}" fill="none" stroke="{MAG}" stroke-width="1.6"/>')
    s.append(kreisform(mx, SY, mr, MOND, MOND_RAND))
    s.append(txt(mx, SY + mr + 4.6, "Mond", 3.2, MOND_RAND))
    if loesung:
        s.append(txt(118, 12, "Halbschatten", 3.2, MAG, "middle", 700))
        s.append(txt(116, 40, "Kernschatten", 3.2, MAG, "middle", 700))
        s.append(f'<line x1="118" y1="37" x2="121" y2="26.5" stroke="{MAG}" stroke-width="0.3"/>')
    s.append(txt(30, 48, "nicht maßstabsgetreu", 2.8, "#66798E", "start"))
    satz = luecken("Bei einer Sonnenfinsternis steht der [[Mond]] zwischen [[Sonne]] und [[Erde]]. "
                   "Das kann nur bei [[Neumond]] passieren.", loesung)
    return (aufgabe(4, "Sonnenfinsternis", "◐")
            + '<p class="frage"><b>a)</b> Zeichne die Randstrahlen von der Sonne am Mond vorbei bis zur Erde. Schraffiere den Kernschatten.<br>'
              '<b>b)</b> <span class="kreis">●</span> Zeichne auch die Grenzen des Halbschattens ein und schraffiere ihn lockerer.</p>'
            + svg(FIN_W, FIN_H, "".join(s)) + f'<p class="frage lt">{satz}</p>')


def mondfinsternis(loesung):
    ex, er = 85, 10
    mx, mr = 150, 4
    s = [kreisform(SX, SY, SR, SONNE, SONNE_RAND), txt(SX, SY + SR + 5, "Sonne", 3.2, SONNE_RAND)]
    loes = ""
    if loesung:
        st, sb = (SX, SY - SR), (SX, SY + SR)
        et, eb = (ex, SY - er), (ex, SY + er)
        xe = 168
        o, u = (xe, gerade(st, et, xe)), (xe, gerade(sb, eb, xe))
        loes += f'<defs>{muster("dicht2", 0.9, MAG)}</defs>'
        loes += f'<polygon points="{et[0]},{et[1]} {o[0]},{o[1]:.2f} {u[0]},{u[1]:.2f} {eb[0]},{eb[1]}" fill="url(#dicht2)"/>'
        for p, q in ((st, et), (sb, eb)):
            loes += f'<line x1="{p[0]}" y1="{p[1]}" x2="{xe}" y2="{gerade(p, q, xe):.2f}" stroke="{MAG}" stroke-width="0.45"/>'
    s.append(loes)
    s.append(kreisform(ex, SY, er, ERDE, ERDE_RAND))
    s.append(txt(ex, SY + er + 4.6, "Erde", 3.2, ERDE_RAND))
    s.append(kreisform(mx, SY, mr, MOND, MOND_RAND))
    s.append(txt(mx, 41.5, "Mond", 3.2, MOND_RAND))
    if loesung:
        s.append(txt(118, 11.5, "Kernschatten der Erde", 3.2, MAG, "middle", 700))
    s.append(txt(30, 48, "nicht maßstabsgetreu", 2.8, "#66798E", "start"))
    satz = luecken("Bei einer Mondfinsternis steht die [[Erde]] zwischen [[Sonne]] und [[Mond]]. "
                   "Das kann nur bei [[Vollmond]] passieren.", loesung)
    return (aufgabe(5, "Mondfinsternis", "◐")
            + '<p class="frage">Zeichne die beiden Randstrahlen, die den Kernschatten der Erde begrenzen, und schraffiere ihn.</p>'
            + svg(FIN_W, FIN_H, "".join(s)) + f'<p class="frage lt">{satz}</p>')


def jahreszeiten(loesung):
    return (aufgabe(3, "Warum gibt es Jahreszeiten?", "◐")
            + '<p class="frage">Erkläre, warum es bei uns im Sommer wärmer ist als im Winter. '
              'Benutze die Wörter <b>Erdachse</b>, <b>geneigt</b>, <b>steil</b>, <b>flach</b> und <b>Fläche</b>.</p>'
            + linien(4, "Die Erdachse ist geneigt. Im Sommer ist unsere Nordhalbkugel zur Sonne geneigt. Die Sonne steht hoch, "
                        "ihre Strahlen fallen steil ein und erwärmen eine kleine Fläche stark. Im Winter fallen die Strahlen flach ein, "
                        "dieselbe Strahlung verteilt sich auf eine große Fläche, der Boden wird weniger erwärmt.", loesung))


def brille(loesung):
    return (aufgabe(6, "Mit oder ohne Brille?", "●")
            + '<p class="frage">Warum darf man eine Mondfinsternis ohne Schutzbrille ansehen, eine Sonnenfinsternis aber nicht?</p>'
            + linien(3, "Bei der Mondfinsternis schaut man auf den schwach beleuchteten Mond. Bei der Sonnenfinsternis blickt man "
                        "in die Sonne, schon ihr schmaler Rand ist so hell, dass er die Netzhaut dauerhaft schädigt.", loesung))


# ------------------------------------------------------------ Dokument
STIL = """
.hinweis{font-size:9pt;color:#66798E}
svg.feld{display:block;margin:1.5mm 0 2mm}
p.lt{line-height:2.05}
.luecke{min-width:30mm}.luecke.kurz{min-width:18mm}
p.antwort{margin:1mm 0 3mm;line-height:1.6;font-size:10.5pt}
.linien .linie{height:7mm}
.phase .stellung{min-height:0;font-size:11pt}
.phase svg{width:17mm;height:17mm}
h2.aufgabe{margin:3mm 0 1.2mm}
"""


def blatt(loesung):
    s1 = kopf(loesung) + ("" if loesung else '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>') \
        + lueckentext_grundlagen(loesung) + mondphasen(loesung) + jahreszeiten(loesung)
    s2 = sonnenfinsternis(loesung) + mondfinsternis(loesung) + brille(loesung)
    return f'<div class="seite">{s1}</div><div class="seite">{s2}</div>'


def dokument(titel, inhalt):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title>'
            f'<link rel="stylesheet" href="ab-vorlage.css"><style>{STIL}</style></head><body>{inhalt}</body></html>')


def drucke(html_name, pdf_name):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / pdf_name}",
                    "--virtual-time-budget=4000", f"file://{HIER / html_name}"], check=True, capture_output=True)
    print("gedruckt:", pdf_name)


if __name__ == "__main__":
    for html, pdf, loes in (("wiederholung-f5.html", f"{BASIS}.pdf", False),
                            ("wiederholung-f5-loesung.html", f"{BASIS} – Lösung.pdf", True)):
        (HIER / html).write_text(dokument(BASIS + (" – Lösung" if loes else ""), blatt(loes)), encoding="utf-8")
        drucke(html, pdf)
