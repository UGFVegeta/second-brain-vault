#!/usr/bin/env python3
"""Blätter Optik II: W10 Reflexionsgesetz, W11 Der Spiegel, W12 Lichtbrechung am Halbzylinder, W13 Strahlengänge an Linsen.
Aufbau wie W05/W06 (Beschreibung + Skizze, Beobachtung, Lückentext, Lösungsseite in Magenta).
Versuchstexte aus Oskars Folien (Optik II S. 6, 28) und alten Blättern übernommen."""
import math, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
from baue_blaetter_w08_w09 import kopf, luecken, seite, dokument, drucke  # noqa: E402

MAG = "#E6007E"
NAME = '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>'
TAB_CSS = ('<style>.mess{border-collapse:collapse;margin:1mm 0 3mm;font-size:10pt}.mess th,.mess td{border:0.6pt solid #14171c;'
           'width:22mm;height:6.5mm;text-align:center}.mess th{background:#EEF1F5;font-weight:600}.mess td.l{color:' + MAG + ';font-weight:600}'
           '.zwei{display:flex;gap:8mm}.zwei>div{flex:1}</style>')


def tabelle(kopfzeile, zeilen, loesung, n):
    k = "".join(f"<th>{h}</th>" for h in kopfzeile)
    rows = ""
    for i in range(n):
        werte = zeilen[i] if loesung and i < len(zeilen) else [""] * len(kopfzeile)
        rows += "<tr>" + "".join(f'<td class="l">{w}</td>' for w in werte) + "</tr>"
    return f'<table class="mess"><tr>{k}</tr>{rows}</table>'


# ---------------------------------------------------------------- W10 Reflexionsgesetz
SK_W10 = '''<svg class="versuchsskizze" viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="92" cy="60" r="36" fill="#FFFFFF" stroke="#7C8592"/>
  <line x1="56" y1="60" x2="128" y2="60" stroke="#7C8592" stroke-width="0.6"/><line x1="92" y1="24" x2="92" y2="60" stroke="#7C8592" stroke-width="0.6" stroke-dasharray="2 2"/>
  <rect x="62" y="60" width="60" height="4" fill="#66798E"/>
  <rect x="14" y="14" width="22" height="12" rx="2" fill="#3B4A63" transform="rotate(38 25 20)"/>
  <line x1="33" y1="27" x2="92" y2="60" stroke="#E39B00" stroke-width="1.4"/><line x1="92" y1="60" x2="140" y2="33" stroke="#E39B00" stroke-width="1.4"/>
  <text x="4" y="46" font-size="8" fill="#66798E">Optikleuchte</text><text x="96" y="22" font-size="8" fill="#66798E">Lot</text>
  <text x="96" y="78" font-size="8" fill="#66798E">Spiegel</text><text x="60" y="96" font-size="8" fill="#66798E">Kreisscheibe</text>
</svg>'''


def w10(l):
    werte = [[f"{a}°", f"{a}°"] for a in (10, 20, 30, 40, 50, 60)]
    lt = luecken("Der Einfallswinkel α ist genauso groß wie der [[Reflexionswinkel]] β. Beide Winkel werden zum [[Lot]] gemessen.", l)
    return seite(kopf("W10", "F6 — Versuch: Das Reflexionsgesetz", l) + ("" if l else NAME)
        + '<p class="frage">Trifft Licht auf einen Spiegel, dann wird es reflektiert. Wovon hängt ab, in welche Richtung das auftreffende Licht abgelenkt wird?</p>'
        + '<div class="versuchskopf"><div><h2 class="aufgabe"><span class="nr">1</span>Versuchsbeschreibung</h2><ol class="liste">'
        '<li>Stelle an der Optikleuchte die Einspaltblende ein, sodass ein Lichtstrahl entsteht.</li>'
        '<li>Lege den Spiegel an die Grundlinie der Winkeleinteilung und richte den Strahl auf den Mittelpunkt der Kreisscheibe.</li>'
        '<li>Miss den Winkel α zwischen einfallendem Strahl und Lot, dann den Winkel β zwischen Lot und reflektiertem Strahl.</li>'
        '<li>Führe sechs Messungen mit verschiedenen Winkeln durch und trage sie in die Tabelle ein.</li></ol></div>' + SK_W10 + '</div>'
        + '<p class="frage"><b>Versuchsbeobachtung:</b>' + (' <span class="loesungstext">Beispielwerte, beim Messen ± 1°</span>' if l else '') + '</p>'
        + tabelle(["Einfallswinkel α", "Reflexionswinkel β"], werte, l, 6)
        + '<h2 class="aufgabe"><span class="nr">2</span>Versuchserklärung</h2><p class="frage">Fülle die Lücken aus.</p>'
        + f'<p class="frage lt">{lt}</p>')


# ---------------------------------------------------------------- W11 Der Spiegel
def figur(x, kopf_y, fuss_y, op=1.0, farbe="#3B4A63"):
    h = fuss_y - kopf_y; r = h * 0.09; cy = kopf_y + r
    return (f'<g opacity="{op}"><circle cx="{x}" cy="{cy:.1f}" r="{r:.1f}" fill="#FFFFFF" stroke="{farbe}" stroke-width="1.4"/>'
            f'<line x1="{x}" y1="{cy + r:.1f}" x2="{x}" y2="{cy + r + h * 0.42:.1f}" stroke="{farbe}" stroke-width="1.6"/>'
            f'<line x1="{x}" y1="{cy + r + h * 0.42:.1f}" x2="{x - r * 0.8:.1f}" y2="{fuss_y}" stroke="{farbe}" stroke-width="1.6"/>'
            f'<line x1="{x}" y1="{cy + r + h * 0.42:.1f}" x2="{x + r * 0.8:.1f}" y2="{fuss_y}" stroke="{farbe}" stroke-width="1.6"/>'
            f'<line x1="{x - r}" y1="{cy + r * 2.2:.1f}" x2="{x + r}" y2="{cy + r * 2.2:.1f}" stroke="{farbe}" stroke-width="1.6"/></g>')


def spiegel_zeichnung(l):
    P, W, kopf_y, fuss_y = 60, 150, 20, 170
    auge = kopf_y + 0.07 * (fuss_y - kopf_y)
    B = W + (W - P)
    o = [f'<svg viewBox="0 0 300 190" style="width:100%;height:100%">',
         f'<line x1="{W}" y1="6" x2="{W}" y2="184" stroke="#14171c" stroke-width="1.6"/>', figur(P, kopf_y, fuss_y),
         f'<circle cx="{P + 3}" cy="{auge:.1f}" r="1.4" fill="#14171c"/>',
         '<text x="40" y="186" font-size="8" fill="#66798E">Person</text><text x="154" y="186" font-size="8" fill="#66798E">Wand</text>']
    if l:
        oben, unten = (kopf_y + auge) / 2, (auge + fuss_y) / 2
        o.append(figur(B, kopf_y, fuss_y, farbe=MAG))
        o.append(f'<line x1="{W}" y1="{oben:.1f}" x2="{W}" y2="{unten:.1f}" stroke="{MAG}" stroke-width="4"/>')
        for yk in (kopf_y, fuss_y):
            ym = (yk + auge) / 2
            o.append(f'<line x1="{P}" y1="{yk}" x2="{W}" y2="{ym:.1f}" stroke="{MAG}" stroke-width="1"/>'
                     f'<line x1="{W}" y1="{ym:.1f}" x2="{P + 3}" y2="{auge:.1f}" stroke="{MAG}" stroke-width="1"/>'
                     f'<line x1="{W}" y1="{ym:.1f}" x2="{B}" y2="{yk}" stroke="{MAG}" stroke-width="1" stroke-dasharray="3 2"/>')
        o.append(f'<text x="{B - 18}" y="186" font-size="8" fill="{MAG}">Spiegelbild</text>')
    o.append("</svg>")
    return "".join(o)


def w11(l):
    lt = luecken("Der Spiegel muss mindestens [[halb so groß]] sein wie die Person. Seine Oberkante hängt auf halber Höhe zwischen "
                 "[[Augen]] und Scheitel. Der Abstand zur Wand spielt [[keine Rolle]].", l)
    return seite(kopf("W11", "F6 — Der Spiegel", l) + ("" if l else NAME)
        + '<p class="frage">Eine Person steht vor einer Wand und möchte einen Spiegel so aufhängen, dass sie sich von Kopf bis Fuß betrachten kann. '
          'Erinnere dich: Das Spiegelbild ist genauso groß wie der Betrachter. Er steht scheinbar (virtuell) ebenso weit hinter dem Spiegel wie der Betrachter davor.</p>'
        + '<h2 class="aufgabe"><span class="nr">1</span>Zeichne das Spiegelbild rechts neben der Wand in richtiger Entfernung und Größe.</h2>'
        + '<h2 class="aufgabe"><span class="nr">2</span>Finde heraus, wie hoch der Spiegel hängen und wie groß er mindestens sein muss. Zeichne dazu die Strahlengänge ein.</h2>'
        + f'<div class="zeichenfeld" style="height:92mm;">{spiegel_zeichnung(l)}</div>'
        + '<h2 class="aufgabe"><span class="nr">3</span>Ergänze.</h2>' + f'<p class="frage lt">{lt}</p>')


# ---------------------------------------------------------------- W12 Lichtbrechung am Halbzylinder
SK_W12 = '''<svg class="versuchsskizze" viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="92" cy="52" r="38" fill="#FFFFFF" stroke="#7C8592"/>
  <line x1="92" y1="14" x2="92" y2="90" stroke="#7C8592" stroke-width="0.6" stroke-dasharray="2 2"/>
  <path d="M62 52 A30 30 0 0 0 122 52 Z" fill="#CFE4F2" stroke="#6E9BB8"/>
  <rect x="14" y="10" width="22" height="12" rx="2" fill="#3B4A63" transform="rotate(38 25 16)"/>
  <line x1="36" y1="22" x2="92" y2="52" stroke="#E39B00" stroke-width="1.4"/><line x1="92" y1="52" x2="118" y2="88" stroke="#E39B00" stroke-width="1.4"/>
  <text x="2" y="42" font-size="8" fill="#66798E">Ray-Box</text><text x="96" y="12" font-size="8" fill="#66798E">Lot</text>
  <text x="124" y="72" font-size="8" fill="#66798E">Halbzylinder</text>
</svg>'''


def brechung(a, n1, n2):
    s = n1 * math.sin(math.radians(a)) / n2
    return f"{round(math.degrees(math.asin(s)))}°" if s <= 1 else "—"


def w12(l):
    t1 = [[f"{a}°", f"{a}°", brechung(a, 1.0, 1.5)] for a in (10, 20, 30, 40, 50)]
    t2 = [[f"{a}°", f"{a}°", brechung(a, 1.5, 1.0)] for a in (10, 20, 30, 40, 50)]
    lt = luecken("Geht Licht von Luft in Glas über, wird es [[zum Lot hin]] gebrochen. Geht es von Glas in Luft über, wird es "
                 "[[vom Lot weg]] gebrochen. Ein kleiner Teil des Lichts wird an der Grenzfläche immer [[reflektiert]].", l)
    hinweis = ('<p class="frage loesungstext">Beispielwerte für Glas. Bei 50° von Glas nach Luft gibt es keinen gebrochenen Strahl mehr, '
               'das ganze Licht wird reflektiert.</p>') if l else ""
    k = ["Einfalls&shy;winkel", "Reflexions&shy;winkel", "Brechungs&shy;winkel"]
    return seite(kopf("W12", "F7 — Versuch: Lichtbrechung am Halbzylinder", l) + ("" if l else NAME)
        + '<div class="versuchskopf"><div><h2 class="aufgabe"><span class="nr">1</span>Versuchsbeschreibung</h2><ol class="liste">'
        '<li>Lege den Halbzylinder auf die Winkelscheibe wie im Bild.</li>'
        '<li>Leuchte mit der Ray-Box aus fünf verschiedenen Winkeln auf die gerade Fläche des Halbzylinders. Der Lichtstrahl soll dabei immer durch den Mittelpunkt der Scheibe verlaufen.</li>'
        '<li>Wiederhole Schritt 2. Leuchte jetzt aber auf die runde Fläche des Halbzylinders. Der Lichtstrahl verläuft wieder durch den Mittelpunkt der Winkelscheibe.</li></ol>'
        '<p class="frage"><b>Achtung:</b> Der Lichtstrahl muss genau durch den Mittelpunkt der Scheibe gehen. Das Glas darf beim Drehen nicht verrutschen.</p></div>' + SK_W12 + '</div>'
        + '<p class="frage"><b>Versuchsbeobachtung:</b> Trage die Winkel in die Tabellen ein.</p>'
        + f'<div class="zwei"><div><p class="frage">1. Versuch: von Luft in Glas</p>{tabelle(k, t1, l, 5)}</div>'
          f'<div><p class="frage">2. Versuch: von Glas in Luft</p>{tabelle(k, t2, l, 5)}</div></div>' + hinweis
        + '<h2 class="aufgabe"><span class="nr">2</span>Versuchserklärung</h2><p class="frage">Fülle die Lücken aus.</p>'
        + f'<p class="frage lt">{lt}</p>')


# ---------------------------------------------------------------- W13 Strahlengänge an Linsen
def linse_feld(sammel, l):
    A, LX = 60, 120
    o = [f'<svg viewBox="0 0 240 120" style="width:100%;height:100%">']
    if l:
        o.append(f'<line x1="6" y1="{A}" x2="234" y2="{A}" stroke="{MAG}" stroke-width="0.8" stroke-dasharray="4 3"/>'
                 f'<line x1="{LX}" y1="6" x2="{LX}" y2="114" stroke="{MAG}" stroke-width="0.8" stroke-dasharray="4 3"/>')
        if sammel:
            o.append(f'<path d="M{LX} 22 Q{LX + 16} 60 {LX} 98 Q{LX - 16} 60 {LX} 22Z" fill="none" stroke="{MAG}" stroke-width="1.2"/>')
            F = LX + 60
            for y in (40, 60, 80):
                ye = y + (A - y) * (230 - LX) / (F - LX)
                o.append(f'<line x1="10" y1="{y}" x2="{LX}" y2="{y}" stroke="{MAG}" stroke-width="1.2"/><line x1="{LX}" y1="{y}" x2="230" y2="{ye:.1f}" stroke="{MAG}" stroke-width="1.2"/>')
            o.append(f'<circle cx="{F}" cy="{A}" r="2.2" fill="{MAG}"/><text x="{F - 3}" y="{A + 13}" font-size="10" font-style="italic" font-family="Georgia" fill="{MAG}">F</text>')
        else:
            o.append(f'<path d="M{LX - 10} 22 Q{LX} 60 {LX - 10} 98 L{LX + 10} 98 Q{LX} 60 {LX + 10} 22Z" fill="none" stroke="{MAG}" stroke-width="1.2"/>')
            F = LX - 60
            for y in (45, 60, 75):
                ye = A + (y - A) * (230 - F) / (LX - F)
                o.append(f'<line x1="10" y1="{y}" x2="{LX}" y2="{y}" stroke="{MAG}" stroke-width="1.2"/><line x1="{LX}" y1="{y}" x2="230" y2="{ye:.1f}" stroke="{MAG}" stroke-width="1.2"/>')
                if y != A:
                    o.append(f'<line x1="{LX}" y1="{y}" x2="{F}" y2="{A}" stroke="{MAG}" stroke-width="0.7" stroke-dasharray="2 2"/>')
            o.append(f'<circle cx="{F}" cy="{A}" r="2.2" fill="{MAG}"/><text x="{F - 3}" y="{A + 13}" font-size="10" font-style="italic" font-family="Georgia" fill="{MAG}">F</text>')
    o.append("</svg>")
    return "".join(o)


def w13(l):
    lt = luecken("Parallele Lichtstrahlen werden von der Sammellinse so gebrochen, dass sie sich in einem Punkt schneiden, dem [[Brennpunkt]]. "
                 "Hinter der Zerstreuungslinse laufen parallele Strahlen [[auseinander]]. Verlängert man sie nach hinten, "
                 "scheinen sie von einem Punkt vor der Linse zu kommen.", l)
    return seite(kopf("W13", "F8 — Versuch: Strahlengänge an Linsen", l) + ("" if l else NAME)
        + '<div class="versuchskopf"><div><h2 class="aufgabe"><span class="nr">1</span>Versuchsbeschreibung</h2><ol class="liste">'
        '<li>Zeichne eine gestrichelte waagrechte und eine senkrechte Achse in die Felder.</li>'
        '<li>Lege die Linse mittig auf die senkrechte Achse und stelle die Ray-Box auf drei parallele Strahlen.</li>'
        '<li>Lege die Ray-Box so, dass der mittlere Strahl auf der waagrechten Achse liegt.</li>'
        '<li>Zeichne die Strahlen vor und nach der Linse nach, entferne die Linse und verbinde sie.</li>'
        '<li>Führe den Versuch zuerst mit der Sammellinse, dann mit der Zerstreuungslinse durch.</li></ol></div></div>'
        + '<p class="frage"><b>Versuchsbeobachtung:</b></p>'
        + f'<p class="frage">Sammellinse</p><div class="zeichenfeld" style="height:48mm;">{linse_feld(True, l)}</div>'
        + f'<p class="frage">Zerstreuungslinse</p><div class="zeichenfeld" style="height:48mm;">{linse_feld(False, l)}</div>'
        + '<h2 class="aufgabe"><span class="nr">2</span>Versuchserklärung</h2><p class="frage">Fülle die Lücken aus.</p>'
        + f'<p class="frage lt">{lt}</p>')


if __name__ == "__main__":
    for html, pdf, titel, fn in (("reflexionsgesetz.html", "Reflexionsgesetz W10.pdf", "Versuch Reflexionsgesetz – W10", w10),
                                 ("der-spiegel.html", "Der Spiegel W11.pdf", "Der Spiegel – W11", w11),
                                 ("lichtbrechung.html", "Lichtbrechung W12.pdf", "Versuch Lichtbrechung – W12", w12),
                                 ("linsen.html", "Strahlengaenge an Linsen W13.pdf", "Versuch Strahlengänge an Linsen – W13", w13)):
        d = dokument(titel, [fn(False), fn(True)]).replace("</head>", TAB_CSS + "</head>")
        (HIER / html).write_text(d, encoding="utf-8")
        drucke(html, pdf)
