#!/usr/bin/env python3
"""Mathe 7c, Ausfallzeit 19.-22.11.2026: Arbeitsblatt „Mit dem Zirkel umgehen“ (A4 Vorder- und Rückseite).
Vom Kreis über den Kreisbogen zum Schnittpunkt zweier Bögen und am Ende zum ersten Dreieck (Vorbereitung Buch S. 53).
Lösung = dasselbe Blatt mit Konstruktion in Magenta. SVG in mm, Punkte auf dem 5-mm-Karo: in Originalgröße drucken."""
import math, subprocess
from pathlib import Path

HIER = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAG, BLAU, GRUEN, SCHWARZ = "#E6007E", "#1F6FD1", "#1E9E52", "#222"
BASIS = "Mathe 7c – Arbeitsblatt Zirkel üben"
L = False


def P(S, r, a):
    return (S[0] + r * math.cos(math.radians(a)), S[1] - r * math.sin(math.radians(a)))


def linie(p, q, f=SCHWARZ, b=0.5):
    return f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="{f}" stroke-width="{b}" stroke-linecap="round"/>'


def text(p, s, f=SCHWARZ, g=3.6, fett=False):
    return f'<text x="{p[0]:.2f}" y="{p[1] + g * 0.35:.2f}" font-size="{g}" fill="{f}" text-anchor="middle"{" font-weight=\"700\"" if fett else ""}>{s}</text>'


def punkt(p, name, o=(0, -3.6), f=SCHWARZ):
    """Punkt als kleines Kreuz mit Namen."""
    d = 1.3
    return (linie((p[0] - d, p[1] - d), (p[0] + d, p[1] + d), f, 0.45) + linie((p[0] - d, p[1] + d), (p[0] + d, p[1] - d), f, 0.45)
            + text((p[0] + o[0], p[1] + o[1]), name, f, 3.4, True))


def kreis(M, r, f=MAG, b=0.45):
    return f'<circle cx="{M[0]:.2f}" cy="{M[1]:.2f}" r="{r:.2f}" fill="none" stroke="{f}" stroke-width="{b}"/>'


def bogen(M, r, a_mitte, breite=28, f=MAG):
    p, q = P(M, r, a_mitte - breite), P(M, r, a_mitte + breite)
    return f'<path d="M{p[0]:.2f},{p[1]:.2f} A{r},{r} 0 0 0 {q[0]:.2f},{q[1]:.2f}" fill="none" stroke="{f}" stroke-width="0.45"/>'


def ang(S, Q):
    return math.degrees(math.atan2(-(Q[1] - S[1]), Q[0] - S[0]))


def schnitt(A, ra, B, rb, oben=True):
    d = math.dist(A, B)
    a = (ra ** 2 - rb ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(ra ** 2 - a ** 2)
    ux, uy = (B[0] - A[0]) / d, (B[1] - A[1]) / d
    m = (A[0] + a * ux, A[1] + a * uy)
    p1, p2 = (m[0] - h * uy, m[1] + h * ux), (m[0] + h * uy, m[1] - h * ux)
    return min(p1, p2, key=lambda p: p[1]) if oben else max(p1, p2, key=lambda p: p[1])


def karo(w, h):
    s = [f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(5, w, 5)]
    s += [f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(5, h, 5)]
    return (f'<rect width="{w}" height="{h}" fill="#fff"/><g stroke="#D3D8DF" stroke-width="0.16">{"".join(s)}</g>'
            f'<rect width="{w}" height="{h}" fill="none" stroke="#9AA3B0" stroke-width="0.3"/>')


def svg(w, h, inhalt, gitter=True):
    return (f'<svg width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Avenir Next, Helvetica Neue, Arial, sans-serif">{karo(w, h) if gitter else ""}{inhalt}</svg>')


def aufgabe(nr, titel, kreis_):
    return f'<h2><span class="nr">{nr}</span><span class="kr">{kreis_}</span>{titel}</h2>'


def box(loes, breite=18):
    return f'<span class="box" style="min-width:{breite * 1.35:.0f}mm">{f"<b class=m>{loes}</b>" if L else ""}</span>'


# ------------------------------------------------------------ Merkkasten
def zirkel_bild():
    """Zirkel auf dem Lineal: Spitze bei 0, Mine bei 3 cm (Skizze, Maßstab 1:1 beim Lineal)."""
    w, h = 62, 34
    y0 = 26
    s = f'<rect x="4" y="{y0}" width="54" height="7" fill="#FFF6D6" stroke="#B98900" stroke-width="0.35" rx="0.8"/>'
    for i in range(0, 51):
        x = 6 + i
        l = 2.6 if i % 10 == 0 else 1.7 if i % 5 == 0 else 1
        s += linie((x, y0), (x, y0 + l), "#8A6A00", 0.18)
        if i % 10 == 0:
            s += text((x, y0 + 4.6), str(i // 10), "#8A6A00", 2.4)
    spitze, mine = (6, y0), (36, y0)
    kopf = (21, 4)
    s += linie(kopf, spitze, "#5B6575", 1.2) + linie(kopf, mine, "#5B6575", 1.2)
    s += f'<circle cx="{kopf[0]}" cy="{kopf[1]}" r="1.8" fill="#5B6575"/>' + linie((21, 2.2), (21, -1), "#5B6575", 1.6)
    s += linie((35.4, y0 - 2.5), mine, "#2B2B2B", 1.0)
    s += text((10.5, 13), "Spitze", BLAU, 2.8, True) + text((33, 13), "Mine", BLAU, 2.8, True)
    s += f'<path d="M6,{y0 - 1} Q21,{y0 - 8} 36,{y0 - 1}" fill="none" stroke="{GRUEN}" stroke-width="0.4" stroke-dasharray="1 0.8"/>'
    s += text((21, y0 - 6.4), "3 cm", GRUEN, 2.8, True)
    return svg(w, h, s, gitter=False)


def merk():
    rez = ('<div class="rezept"><b>Rezept: Kreisbogen um A mit 3 cm</b><ol>'
           '<li>Zirkel am Lineal einstellen: Spitze auf 0, Mine auf 3 cm.</li>'
           '<li>Spitze genau in den Punkt A stechen.</li>'
           '<li>Nur oben am Griff anfassen und drehen. Nicht an den Beinen drücken, sonst verstellt er sich.</li>'
           '<li>Für einen Kreisbogen nur ein Stück drehen, für einen Kreis ganz herum.</li></ol>'
           '<span class="kl">Jeder Punkt auf dem Bogen ist genau 3 cm von A entfernt. Das ist der ganze Trick beim Konstruieren.</span></div>')
    return f'<div class="merk"><div class="mt">Merke: So geht der Zirkel</div><div class="mrow">{zirkel_bild()}{rez}</div></div>'


# ------------------------------------------------------------ Aufgaben
def a1():
    w, h = 85, 60
    M = (40, 30)
    s = punkt(M, "M", (0, -3.5))
    for a in (30, 150, 270):
        p = P(M, 20, a)
        s += f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="1" fill="{BLAU}"/>'
    for a in (90, 210, 330):
        p = P(M, 25, a)
        s += f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="1" fill="{GRUEN}"/>'
    if L:
        s += kreis(M, 20) + kreis(M, 25)
    return (aufgabe(1, "Kreise um M", "○")
            + '<p class="auf">a) Öffne den Zirkel auf <b>2 cm</b> und zeichne einen Kreis um M. Er muss durch alle <b style="color:#1F6FD1">blauen</b> Punkte gehen.<br>'
              'b) Dasselbe mit <b>2,5 cm</b>. Jetzt durch die <b style="color:#1E9E52">grünen</b> Punkte.</p>' + svg(w, h, s))


def a2():
    w, h = 85, 50
    A = (10, 42)
    s = linie(A, (80, 42), b=0.5) + linie(A, P(A, 70, 40), b=0.5) + punkt(A, "A", (-3, 2.5))
    if L:
        B, C = P(A, 40, 0), P(A, 30, 40)
        s += bogen(A, 40, 0, 14) + bogen(A, 30, 40, 14) + punkt(B, "B", (0, 4), MAG) + punkt(C, "C", (-3, -2.5), MAG)
    return (aufgabe(2, "Strecken mit dem Zirkel abtragen", "○")
            + '<p class="auf">a) Zeichne einen Kreisbogen um A mit <b>4 cm</b> über die waagrechte Linie. Wo er die Linie trifft, liegt <b>B</b>.<br>'
              'b) Genauso mit <b>3 cm</b> auf der schrägen Linie. Dort liegt <b>C</b>.<br>c) Prüfe mit dem Lineal: AB = '
            + box("4 cm", 12) + ' AC = ' + box("3 cm", 12) + '</p>' + svg(w, h, s))


def a3():
    w, h = 186, 62
    A, B = (65, 31), (115, 31)
    s = punkt(A, "Baum A", (-1, 4.5)) + punkt(B, "Brunnen B", (1, 4.5))
    if L:
        C1, C2 = schnitt(A, 30, B, 30, True), schnitt(A, 30, B, 30, False)
        s += kreis(A, 30, "#E6007E") + bogen(B, 30, ang(B, C1), 18) + bogen(B, 30, ang(B, C2), 18)
        s += punkt(C1, "S", (0, -3.5), MAG) + punkt(C2, "S", (0, 5), MAG)
    return (aufgabe(3, "Schatzsuche: zwei Kreisbögen schneiden sich", "◐")
            + '<p class="auf">Der Schatz liegt genau <b>3 cm</b> vom Baum A und genau <b>3 cm</b> vom Brunnen B entfernt.<br>'
              'a) Zeichne einen Kreis um A mit 3 cm. Auf diesem Kreis liegen alle Stellen, die 3 cm von A entfernt sind.<br>'
              'b) Zeichne einen Kreisbogen um B mit 3 cm. Wo sich Kreis und Bogen schneiden, liegt der Schatz. Markiere mit S.<br>'
              'c) Wie viele Stellen kommen in Frage? ' + box("2 Stellen (oben und unten)", 44) + '</p>' + svg(w, h, s))


def a4():
    w, h = 60, 60
    M = (30, 30)
    s = punkt(M, "M", (0, 4.2))
    if L:
        r = 20
        s += f'<defs><clipPath id="bl"><circle cx="{M[0]}" cy="{M[1]}" r="{r}"/></clipPath></defs>' + kreis(M, r)
        s += '<g clip-path="url(#bl)">' + "".join(kreis(P(M, r, a), r) for a in range(90, 450, 60)) + "</g>"
    return (aufgabe(4, "Kreisblume", "◐")
            + '<div class="row">' + svg(w, h, s) + '<p class="auf">Der Zirkel bleibt die ganze Zeit auf <b>2 cm</b>.<br>'
              '① Kreis um M.<br>② Stich irgendwo <b>auf</b> den Kreis ein und zeichne einen Bogen, der von Kreisrand zu Kreisrand geht.<br>'
              '③ Stich dort ein, wo der Bogen den Kreis trifft, und zeichne den nächsten Bogen.<br>④ So weiter, bis du wieder am Anfang bist.<br>'
              'Wie viele Blätter hat deine Blume? ' + box("6", 10) + '<br><span class="kl">Tipp: Wenn die Blume nicht aufgeht, hat sich der Zirkel verstellt.</span></p></div>')


def dreieck_feld(ab, ra, rb, w=90, h=52):
    A = (15, h - 12)
    B = (15 + ab * 10, h - 12)
    s = linie(A, B, b=0.6) + punkt(A, "A", (-3, 2.5)) + punkt(B, "B", (3, 2.5)) + text(((A[0] + B[0]) / 2, A[1] + 4.5), f"{ab} cm", g=3)
    if L:
        C = schnitt(A, ra * 10, B, rb * 10, True)
        s += bogen(A, ra * 10, ang(A, C), 12) + bogen(B, rb * 10, ang(B, C), 12)
        s += linie(A, C, MAG, 0.6) + linie(B, C, MAG, 0.6) + punkt(C, "C", (0, -3.6), MAG)
    return svg(w, h, s)


def a5():
    return (aufgabe(4, "Dein erstes Dreieck: alle Seiten 4 cm", "●")
            + '<div class="row">' + dreieck_feld(4, 4, 4) + '<p class="auf">① Kreisbogen um A mit <b>4 cm</b> nach oben.<br>② Kreisbogen um B mit <b>4 cm</b>.<br>'
              '③ Der Schnittpunkt ist <b>C</b>.<br>④ Verbinde C mit A und mit B.<br>'
              'Miss die Winkel: ' + box("alle 60°", 18) + '<br>Das Dreieck ist ' + box("gleichseitig", 26) + '</p></div>')


def a6():
    return (aufgabe(5, "Dreieck mit 5 cm, 4 cm und 3 cm", "●")
            + '<div class="row">' + dreieck_feld(5, 4, 3, 90, 50) + '<p class="auf">Gegeben ist AB = 5 cm. C soll <b>4 cm</b> von A und <b>3 cm</b> von B entfernt sein.<br>'
              '① Bogen um A mit 4 cm.<br>② Bogen um B mit 3 cm.<br>③ Schnittpunkt C, dann verbinden.<br>'
              'Miss den Winkel bei C: γ = ' + box("90°", 12) + '<br>Was fällt dir auf? ' + box("Das Dreieck ist rechtwinklig.", 40) + '</p></div>')


def a7():
    w, h = 186, 56
    s = ""
    if L:
        A, B = (60, 47), (120, 47)
        C = schnitt(A, 50, B, 40, True)
        s += linie(A, B, MAG, 0.6) + punkt(A, "A", (-3, 2.5), MAG) + punkt(B, "B", (3, 2.5), MAG)
        s += bogen(A, 50, ang(A, C), 12) + bogen(B, 40, ang(B, C), 12)
        s += linie(A, C, MAG, 0.6) + linie(B, C, MAG, 0.6) + punkt(C, "C", (0, -3.6), MAG)
    return (aufgabe(6, "Jetzt ganz allein", "●")
            + '<p class="auf">Zeichne ein Dreieck mit AB = <b>6 cm</b>, AC = <b>5 cm</b> und BC = <b>4 cm</b>. '
              'Fang mit der Strecke AB an, dann zwei Kreisbögen wie in Aufgabe 4 und 5.</p>' + svg(w, h, s))


def kopf(seite):
    lm = '<span class="lmark">Lösung</span>' if L else ""
    if seite == 1:
        nf = "" if L else '<div class="name"><span>Name</span><span class="k">Datum</span></div>'
        return (f'<div class="kopf"><div><span class="chip">Mathe 7c</span><h1>Mit dem Zirkel umgehen</h1></div>{lm}</div>{nf}'
                '<p class="leg">○ leicht &nbsp; ◐ mittel &nbsp; ● schwer &nbsp;&nbsp; Du brauchst: Zirkel, spitzen Bleistift, Lineal oder Geodreieck. '
                'Zeichne direkt auf das Blatt.</p>')
    return f'<div class="kopf"><div><span class="chip">Mathe 7c</span><h1>Rückseite: Vom Kreisbogen zum Dreieck</h1></div>{lm}</div>'


def kreise_einheitlich(html):
    """○ ◐ ● als gleich große SVG-Kreise (Schriftzeichen sind je nach Font verschieden groß)."""
    def k(art):
        f = {"○": "", "◐": '<path d="M5,1 A4,4 0 0 0 5,9 Z" fill="#222"/>', "●": '<circle cx="5" cy="5" r="4" fill="#222"/>'}[art]
        return (f'<svg width="3.4mm" height="3.4mm" viewBox="0 0 10 10" style="vertical-align:-0.5mm"><title>{art}</title>'
                f'<circle cx="5" cy="5" r="4" fill="none" stroke="#222" stroke-width="1.1"/>{f}</svg>')
    for z in "○◐●":
        html = html.replace(z, k(z))
    return html


STIL = """
@page{size:A4;margin:9mm 11mm 8mm}*{box-sizing:border-box}
body{margin:0;font-family:"Avenir Next","Helvetica Neue",Arial,sans-serif;color:#222;font-size:12.0pt;line-height:1.45}
.seite{page-break-after:always}.blk{break-inside:avoid}
.kopf{display:flex;justify-content:space-between;align-items:center;border-bottom:1.6px solid #1F4FA0;padding-bottom:1.5mm}
.kopf h1{display:inline;font-size:16.0pt;margin:0 0 0 2mm;color:#1F4FA0}
.chip{background:#1F4FA0;color:#fff;border-radius:3px;padding:.6mm 2mm;font-size:10.3pt;font-weight:700}
.lmark{color:#fff;background:#E6007E;padding:1mm 3mm;border-radius:3px;font-weight:700}
.name{display:flex;gap:4mm;margin-top:1.5mm}.name span{flex:1;border-bottom:1px solid #999;font-size:9.1pt;color:#777;padding-bottom:3mm}.name .k{flex:.35}
.leg{font-size:9.6pt;color:#555;margin:1.2mm 0 1.5mm}
.merk{border:1.4px solid #1F4FA0;border-radius:2.5mm;padding:1.8mm 3mm;background:#F3F7FD;margin-bottom:1mm}
.mt{font-weight:700;color:#1F4FA0;margin-bottom:1mm}.mrow{display:flex;gap:4mm;align-items:center}
.rezept{font-size:10.1pt}.rezept ol{margin:.5mm 0 .8mm 5mm;padding:0}.kl{color:#555;font-size:9.6pt}
h2{font-size:11.4pt;margin:2.4mm 0 .8mm;display:flex;align-items:baseline;gap:1.6mm}
.nr{background:#222;color:#fff;border-radius:50%;width:5.2mm;height:5.2mm;display:inline-flex;align-items:center;justify-content:center;font-size:9.8pt;flex:none}
.kr{font-size:12.6pt}.auf{margin:0 0 1.2mm}
.zwei{display:flex;gap:6mm}.zwei>div{flex:1}
.row{display:flex;gap:5mm;align-items:center}
.box{display:inline-block;border-bottom:1px solid #555;height:9.5mm;vertical-align:bottom;padding:0 1mm;line-height:12mm}
.m{color:#E6007E;font-weight:600}
.hinweis{font-size:9.1pt;color:#777;margin-top:2mm}
"""


def blatt():
    b = lambda *t: "".join(f'<div class="blk">{x}</div>' for x in t)
    hin = '<p class="hinweis">Drucke das Blatt in Originalgröße (100 %), sonst stimmen die Zentimeter nicht.</p>'
    seiten = [kopf(1) + b(merk()) + f'<div class="zwei blk"><div>{a1()}</div><div>{a2()}</div></div>' + b(a3()), kopf(2) + b(a5(), a6(), a7()) + hin]
    return "".join(f'<div class="seite">{x}</div>' for x in seiten)


def main():
    global L
    for loes in (False, True):
        L = loes
        name = BASIS + (" – Lösung" if loes else "")
        html = HIER / f"{name}.html"
        html.write_text(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{name}</title><style>{STIL}</style></head>'
                        f'<body>{kreise_einheitlich(blatt())}</body></html>', encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / (name + '.pdf')}",
                        "--virtual-time-budget=3000", html.as_uri()], check=True, capture_output=True)
        print("gedruckt:", name)


if __name__ == "__main__":
    main()
