#!/usr/bin/env python3
"""Begleitheft „Kernspaltung und Kettenreaktion“ für W16 bis W18 (Entwurf).
Grundlage: Oskars Arbeitsblatt „Kettenreaktion“ (Fragen als Überschriften, Zeichnen, Einsetzen, Schreiben im Wechsel).
Neu geordnet nach den drei Stunden, fachlich nachgeschärft, Dominoversuch und Kraftwerk/Fusion ergänzt.
Aufruf: python3 baue_begleitheft_kernspaltung.py  -> Begleitheft Kernspaltung.html (Schülerseiten + Lösungsseiten)"""
import math, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
from kern_zeichnungen import Z, INK, ORANGE, PROTON, NEUTRON, kern, teilchen, welle, nuklid  # noqa: E402
from baue_blaetter_k10 import MAG, NAME, kreis, nk, luecken, dokument  # noqa: E402

GRAU, BLAU = "#66798E", "#3B7CC4"
HEFT_CSS = ('<style>.abs{display:flex;justify-content:space-between;align-items:baseline;color:#1F8FB0;font-size:13pt;font-weight:600;'
            'border-bottom:.8pt solid #14171c;margin:4.5mm 0 2mm;padding-bottom:.6mm}.abs .w{font-size:8pt;color:#8A94A3;font-weight:600;letter-spacing:.05em}'
            '.abs .lvl{margin-right:1.5mm}.bild{margin:1mm 0 2mm}.bild svg{width:100%;height:auto;display:block}'
            '.zwei{display:flex;gap:4mm;align-items:stretch}.zwei>div{flex:1}.klein{font-size:9pt;color:#3b4150}'
            '.lt{line-height:2.1}.antw{border-bottom:.5pt solid #b8bec7;min-height:6.5mm}.antw.loesungstext{border-bottom:none;min-height:0;margin:0 0 1.5mm}'
            '.titel{font-size:19pt;font-weight:700;margin:0 0 1mm}.untertitel{font-size:10pt;color:#3b4150;margin:0 0 2mm}'
            '.stunde{font-size:8.5pt;font-weight:700;letter-spacing:.08em;color:#fff;background:#66798E;display:inline-block;padding:.8mm 2.5mm;border-radius:2pt;margin-top:3mm}</style>')


def abschnitt(nr, titel, stufe, stunde=""):
    return f'<div class="abs"><span>{kreis(stufe)}{nr} {titel}</span><span class="w">{stunde}</span></div>'


def antwort(text, l, zeilen=2):
    return f'<p class="antw loesungstext">{text}</p>' if l else '<div class="antw"></div>' * zeilen


def feld(inhalt, h):
    return f'<div class="zeichenfeld" style="height:{h}mm;margin:1mm 0 2mm">{inhalt}</div>'


def pfeil(z, x1, y1, x2, y2, col, w=1.8, s=7):
    return z.pfeil(x1, y1, x2, y2, col, w, s)


def neutron(z, x, y, col=NEUTRON):
    return z.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}" stroke="#FFFFFF" stroke-width="1"/>')


def blitz(z, x, y, col):
    pts = []
    for k in range(16):
        r = 22 if k % 2 == 0 else 10
        a = math.radians(k * 22.5)
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    return z.poly(pts, col, .55)


# ------------------------------------------------------------------ Zeichnungen
def kette(l):
    """Vier Felder wie in Oskars Blatt. Die Kerne sind vorgegeben, Neutronen und Pfeile zeichnen die Schüler."""
    z = Z("bh1", 250)
    for x in (140, 280, 420):
        z.line(x, 10, x, 214, "#A3B7D3", 1.2)
    kern(z, 85, 110, 9, 12, r=5, seed=3)
    z.add('<ellipse cx="210" cy="110" rx="36" ry="30" fill="none" stroke="#E8604A" stroke-width="1.3" stroke-dasharray="3 3"/>')
    kern(z, 210, 110, 9, 13, r=5, seed=4)
    kern(z, 350, 64, 5, 7, r=5, seed=5)
    kern(z, 350, 160, 4, 6, r=5, seed=6)
    for y in (40, 110, 180):
        kern(z, 470, y, 5, 7, r=4, seed=int(y))
        kern(z, 575, y - 16, 3, 4, r=4, seed=int(y) + 1)
        kern(z, 575, y + 16, 3, 3, r=4, seed=int(y) + 2)
    for i, (x, t) in enumerate(((70, "Neutron trifft Uran-235"), (210, "Kern wird instabil"), (350, "Kern spaltet sich"), (528, "Kettenreaktion"))):
        z.add(f'<circle cx="{x - (55 if i == 0 else 60 if i < 3 else 100)}" cy="20" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="1.2"/>')
        z.text(x - (55 if i == 0 else 60 if i < 3 else 100), 24, str(i + 1), "middle", 10, 600)
        z.text(x, 236, t, "middle", 9)
    if l:
        neutron(z, 20, 110, MAG).pfeil(28, 110, 58, 110, MAG, 1.6, 6)
        for y in (86, 110, 134):
            z.pfeil(376, 110, 408, y, MAG, 1.4, 6)
            neutron(z, 412, y, MAG)
        blitz(z, 350, 112, MAG)
        z.text(350, 120, "Energie", "middle", 8.5, 600, MAG)
        for y in (40, 110, 180):
            neutron(z, 428, y, MAG).pfeil(436, y, 454, y, MAG, 1.4, 5)
            z.pfeil(488, y, 560, y - 12, "#E8604A", 1, 5).pfeil(488, y, 560, y + 12, "#E8604A", 1, 5)
            for d in (-8, 0, 8):
                neutron(z, 610, y + d * 2.2, MAG)
        z.text(528, 212, "mehr Spaltungen in jedem Schritt", "middle", 8.5, 500, MAG)
    return z.svg()


def kuehlturm(z, x, y):
    z.add(f'<path d="M{x - 26} {y + 60} Q{x - 14} {y + 20} {x - 20} {y} H{x + 20} Q{x + 14} {y + 20} {x + 26} {y + 60}Z" fill="#E1E7EF" stroke="{GRAU}" stroke-width="1.4"/>')
    for k, dx in enumerate((-10, 2, 12)):
        z.add(f'<circle cx="{x + dx}" cy="{y - 10 - k * 6}" r="{9 + k * 2}" fill="#F2F4F7" stroke="#C9D0DA"/>')


def pilz(z, x, y):
    z.add(f'<path d="M{x - 8} {y + 64} Q{x - 4} {y + 30} {x - 8} {y + 14} H{x + 8} Q{x + 4} {y + 30} {x + 8} {y + 64}Z" fill="#E8B79A"/>'
          f'<ellipse cx="{x}" cy="{y}" rx="34" ry="20" fill="#E8B79A" stroke="#C98B6A"/><ellipse cx="{x}" cy="{y + 66}" rx="30" ry="6" fill="#E8B79A"/>')


def kontrolliert(l):
    z = Z("bh2", 150)
    if l:
        for i in range(5):
            x = 40 + i * 100
            kern(z, x, 70, 3, 4, r=4, seed=10 + i)
            if i < 4:
                z.pfeil(x + 12, 70, x + 86, 70, MAG, 1.6, 6)
            z.pfeil(x + 4, 80, x - 6, 108, "#A3B7D3", 1.1, 5)
            z.rect(x - 16, 112, 8, 22, "#3B4150", 1, 1)
        z.text(240, 30, "je Spaltung bleibt genau 1 Neutron wirksam", "middle", 9, 600, MAG)
        z.text(240, 146, "die übrigen fangen Steuerstäbe ein", "middle", 8.5, 500, MAG)
    return z.svg(480)


def unkontrolliert(l):
    z = Z("bh3", 150)
    if l:
        lv = [[(40, 75)]]
        for g in range(1, 4):
            lv.append([(40 + g * 125, y + d) for (_, y) in lv[-1] for d in (-34 / g, 34 / g)])
        for g in range(len(lv)):
            for (x, y) in lv[g]:
                kern(z, x, y, 2, 3, r=3.4, seed=20 + g)
                if g + 1 < len(lv):
                    for (x2, y2) in lv[g + 1]:
                        if abs(y2 - y) < 36 / (g + 1) + 1:
                            z.pfeil(x + 8, y, x2 - 8, y2, MAG, 1.2, 5)
        for g in range(4):
            z.text(40 + g * 125, 146, str(2 ** g), "middle", 9, 600, MAG)
    return z.svg(480)


def reaktor(l):
    z = Z("bh4", 252)
    z.add('<rect x="30" y="20" width="330" height="200" rx="16" fill="#DCEBF7" stroke="#6E8FB5" stroke-width="2.2"/>')
    for x in (70, 170, 270):
        z.rect(x, 50, 44, 150, "#FFE7A0", 1, 4)
        z.add(f'<rect x="{x}" y="50" width="44" height="150" rx="4" fill="none" stroke="#C9A43A" stroke-width="1.2"/>')
        for k in range(5):
            z.add(f'<circle cx="{x + 22}" cy="{66 + k * 28}" r="7" fill="#F4B942" stroke="#B8860B" stroke-width=".8"/>')
    for x in (128, 228):
        z.rect(x, 20, 12, 130, "#3B4150", 1, 2)
    for x, y in ((124, 175), (150, 190), (224, 170), (250, 95)):
        z.add(f'<circle cx="{x}" cy="{y}" r="3" fill="#FFFFFF" stroke="{BLAU}" stroke-width=".8"/>')
    z.add(f'<polyline points="112,166 126,180 138,164 150,184 158,176" fill="none" stroke="{ORANGE}" stroke-width="1.4"/>')
    neutron(z, 162, 180)
    kern(z, 322, 120, 2, 3, r=4, seed=33)
    kern(z, 336, 140, 2, 2, r=4, seed=34)
    marken = [(70, 150, 12, 150, "Brennstab mit Uran"), (140, 28, 164, 8, "Steuerstab"), (146, 205, 150, 240, "Wasser (Moderator und Kühlmittel)"),
              (162, 186, 200, 240, "abgebremstes Neutron"), (292, 60, 292, 8, "Uran-235-Kern"), (340, 140, 380, 116, "Spaltprodukte"),
              (358, 200, 380, 228, "Reaktordruckbehälter")]
    for i, (x, y, cx, cy, t) in enumerate(marken):
        z.line(x, y, cx, cy, GRAU, .8)
        z.add(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#FFFFFF" stroke="{INK}" stroke-width="1"/>')
        z.text(cx, cy + 4, str(i + 1), "middle", 9, 600)
        ly = 26 + i * 31
        z.text(420, ly, f"{i + 1}.", size=9.5, weight=600)
        if l:
            z.text(438, ly, t, size=9, weight=600, col=MAG)
        else:
            z.line(438, ly + 3, 630, ly + 3, "#b8bec7", .8)
    return z.svg()


def moderator(l):
    z = Z("bh5", 150)
    for i in range(34):
        x, y = 200 + (i % 9) * 26 + (i // 9 % 2) * 12, 20 + (i // 9) * 32
        z.add(f'<circle cx="{x}" cy="{y}" r="5" fill="#FFFFFF" stroke="{BLAU}" stroke-width="1"/>')
    z.text(310, 146, "Wasser", "middle", 8.5)
    kern(z, 60, 75, 7, 9, r=4, seed=41)
    z.text(60, 146, "Spaltung", "middle", 8.5)
    kern(z, 560, 75, 7, 9, r=4, seed=42)
    z.text(560, 146, "neuer Uran-235-Kern", "middle", 8.5)
    neutron(z, 100, 75)
    z.pfeil(108, 75, 180, 75, ORANGE, 2.6, 8)
    z.text(140, 64, "schnell", "middle", 8.5)
    if l:
        z.add(f'<polyline points="186,75 212,52 238,86 262,60 290,92 318,70 344,100 372,74 398,96 426,80 452,84" fill="none" stroke="{MAG}" stroke-width="1.4"/>')
        neutron(z, 470, 84, MAG)
        z.pfeil(476, 84, 530, 78, MAG, 1.4, 6)
        z.text(500, 66, "langsam", "middle", 8.5, 600, MAG)
    return z.svg()



# ------------------------------------------------------------------ Oskars eigene Zeichnungen (aus seinem Blatt „Kettenreaktion“)
B = "assets/kettenreaktion/"


def img(datei, breite="100%", extra=""):
    return f'<img src="{B}{datei}" style="width:{breite};display:block{extra}" alt="">'


def kette_bild(l):
    """Oskars Vier-Felder-Bild, in der Lösung mit Neutronen in Magenta darüber (Koordinaten im Bild: 1702 x 1300)."""
    o = ['<svg viewBox="0 0 1702 1300" style="position:absolute;inset:0;width:100%;height:100%">',
         '<rect x="10" y="420" width="40" height="80" fill="#FFFFFF"/>']
    if l:
        def n(x, y): o.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{MAG}"/>')
        def a(x1, y1, x2, y2):
            dx, dy = x2 - x1, y2 - y1
            L = (dx * dx + dy * dy) ** .5
            ux, uy = dx / L, dy / L
            o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2 - ux * 22:.0f}" y2="{y2 - uy * 22:.0f}" stroke="{MAG}" stroke-width="7" stroke-linecap="round"/>'
                     f'<polygon points="{x2},{y2} {x2 - ux * 34 - uy * 16:.0f},{y2 - uy * 34 + ux * 16:.0f} {x2 - ux * 34 + uy * 16:.0f},{y2 - uy * 34 - ux * 16:.0f}" fill="{MAG}"/>')
        n(35, 600); a(55, 600, 98, 600)
        for (x2, y2) in ((860, 440), (900, 800), (760, 930)):
            a(640, 620, x2, y2); n(x2 + 18, y2 + (-12 if y2 < 600 else 12))
        for y in (190, 590, 1050):
            n(1050, y); a(1068, y, 1075, y) if False else a(1068, y, 1080, y)
            for dy in (-70, 10, 90):
                a(1450, y + (dy if y != 1050 else dy - 20), 1560, y + dy * 1.5 + (0 if y != 1050 else -20)); n(1580, y + dy * 1.5 + (0 if y != 1050 else -20))
    o.append("</svg>")
    return f'<div style="position:relative;width:128mm;margin:1mm auto 2mm">{img("kettenreaktion-felder.png")}{"".join(o)}</div>'


def zeichnen_neben_bild(bild, loesung_svg, h=40):
    return (f'<div class="zwei" style="margin:1mm 0 2mm"><div style="flex:0 0 38mm">{img(bild)}</div>'
            f'<div>{feld(loesung_svg, h)}</div></div>')


def reaktor_bild(l):
    teile = ["Uran-235 (spaltbar)", "Uran-238", "Spaltprodukte", "Steuerstab (Regelstab)", "Brennstab", "Weg eines Neutrons", "Wasser (Moderator)"]
    zeilen = "".join(f'<div style="display:flex;gap:2mm;align-items:baseline;margin-bottom:1.2mm"><b style="width:5mm">{i + 1}.</b>'
                     f'<div style="flex:1">{antwort(t, l, 1)}</div></div>' for i, t in enumerate(teile))
    return f'<div class="zwei" style="margin:1mm 0 2mm;align-items:center"><div style="flex:0 0 66mm">{img("reaktor.png")}</div><div>{zeilen}</div></div>'

# ------------------------------------------------------------------ Seiten
def seite1(l):
    lm = '<div class="loesung-marker">Lösung</div>' if l else ""
    L = lambda s: f'<span class="luecke loesungstext">{s}</span>' if l else '<span class="luecke"></span>'
    energie = (f'<p class="frage lt">Bei vollständiger Verbrennung oder Spaltung liefert 1 kg Steinkohle etwa {L("8")} kWh Wärme, 1 kg Erdöl etwa {L("12")} kWh '
               f'und 1 kg Uran-235 rund {L("23 Millionen")} kWh. Für dieselbe Wärme wie 1 kg Uran-235 braucht man also etwa {L("3000")} Tonnen Kohle. '
               f'Uran hat eine viel größere {L("Energiedichte")} als alle anderen Brennstoffe.</p>')
    lt1 = luecken("1938 beschossen [[Otto Hahn]] und Fritz Straßmann in Berlin Uran (92 Protonen) mit langsamen [[Neutronen]]. Sie wollten Elemente erzeugen, "
                  "die [[schwerer]] sind als Uran. Stattdessen fanden sie das viel leichtere [[Barium]]. Die Erklärung lieferte Lise Meitner, die kurz zuvor "
                  "aus Deutschland fliehen musste: Der Urankern war [[gespalten]] worden. Gespalten wurde nur das Isotop [[Uran-235]].", l)
    return (f'<div class="kopf"><div><span class="chip">W16–W18</span><h1>Kernspaltung und Kettenreaktion</h1></div>{lm}</div>'
            + ("" if l else NAME)
            + f'<div class="legende">Schwierigkeit:{kreis(0)}leicht{kreis(1)}mittel{kreis(2)}schwer</div>'
            + '<span class="stunde">STUNDE 1 · DIE KERNSPALTUNG</span>'
            + abschnitt(1, "Wie viel Energie steckt im Uran?", 0, "W16") + energie
            + abschnitt(2, "Atome lassen sich spalten", 0, "W16") + f'<p class="frage lt">{lt1}</p>'
            + abschnitt(3, "Wie funktioniert eine Kettenreaktion?", 1, "W16")
            + '<p class="frage">Zeichne in die Felder 1, 3 und 4 die Neutronen mit Pfeilen ein.</p>'
            + kette_bild(l))


def seite2(l):
    L = lambda s: f'<span class="luecke loesungstext">{s}</span>' if l else '<span class="luecke"></span>'
    gl = (f'<p class="gl" style="font-size:12.5pt">{nk("n", 1, 0)} + {nk("U", 235, 92)} → {nk("U", 236, 92)} → {nk("Ba", 141, 56)} + {nk("Kr", 92, 36)} + 3 {nk("n", 1, 0)} + Energie</p>'
          if l else "")
    lt3 = luecken("Bei jeder Kernspaltung werden [[2 oder 3]] Neutronen frei. Sie sind sehr schnell, etwa 20 000 km/s. Uran-235 wird aber vor allem von "
                  "[[langsamen]] Neutronen gespalten. Trifft ein Neutron einen weiteren Kern, entstehen wieder [[2 oder 3]] Neutronen. "
                  "Bei jeder Spaltung wird eine große Menge [[Energie]] frei.", l)
    lt4 = (f'<p class="frage lt">Uran-235 hat {L("143")} Neutronen (Massenzahl 235 − {L("92")} Protonen). Uran-238 hat {L("146")} Neutronen '
           f'(Massenzahl 238 − {L("92")} Protonen). Beide sind also {L("Isotope")} des Urans. Natürliches Uran besteht zu über 99 % aus {L("Uran-238")}, '
           f'nur 0,7 % sind Uran-235. Der Unterschied: Uran-235 wird schon von {L("langsamen")} Neutronen gespalten, Uran-238 praktisch nicht.</p>')
    lt5 = luecken("Neutronen haben [[keine]] Ladung. Deshalb werden sie vom positiv geladenen Atomkern nicht [[abgestoßen]] und von elektrischen Feldern nicht "
                  "[[abgelenkt]]. Sie treffen den Kern wie kleine Torpedos.", l)
    return (abschnitt("", "Reaktionsgleichung einer Kernspaltung", 1, "W16")
            + '<p class="frage">Schreibe die Gleichung zu deiner Zeichnung auf. Beispiel: Es entstehen Barium-141 und Krypton-92.</p>'
            + feld(gl, 16)
            + f'<p class="frage lt">{lt3}</p>'
            + abschnitt(4, "Warum Uran-235 und nicht Uran-238?", 1, "W16")
            + f'<div style="float:right;width:30mm;margin:0 0 1mm 4mm;text-align:center">{img("uranerz.png")}<span class="klein">Uranerz</span></div>' + lt4
            + abschnitt(5, "Warum nimmt man Neutronen für die Spaltung?", 0, "W16") + f'<p class="frage lt">{lt5}</p>'
            + '<span class="stunde">STUNDE 2 · DIE KETTENREAKTION</span>'
            + abschnitt(6, "Versuch: Kettenreaktion mit Dominosteinen", 1, "W17")
            + '<ol class="liste"><li><b>Schritt 1:</b> Stellt die Steine in einer Reihe auf und stoßt den ersten an.</li>'
              '<li><b>Schritt 2:</b> Baut so um, dass jeder Stein zwei weitere umwirft. Stoßt nur einen Stein an.</li>'
              '<li><b>Schritt 3:</b> Nehmt aus dem Aufbau von Schritt 2 so viele Steine heraus, dass immer gleich viele Steine fallen.</li></ol>'
            + '<p class="frage">Welcher Schritt passt zu einem Kraftwerk, welcher zu einer Bombe? Begründe.</p>'
            + antwort("Schritt 3 passt zum Kraftwerk: Es fallen immer gleich viele Steine, die Reaktion läuft gleichmäßig. "
                      "Schritt 2 passt zur Bombe: Die Zahl der fallenden Steine verdoppelt sich immer wieder, alles passiert in kürzester Zeit.", l, 3))


def seite3(l):
    L = lambda s: f'<span class="luecke loesungstext">{s}</span>' if l else '<span class="luecke"></span>'
    lt8 = (f'<p class="frage lt">Eine Kettenreaktion läuft nur, wenn genug spaltbares Material zusammen ist. Die kleinste Menge dafür heißt {L("kritische Masse")}. '
           f'Für eine Kugel aus reinem Uran-235 sind das etwa 50 kg, also eine Kugel mit etwa 17 cm Durchmesser. '
           f'Weil Natururan nur 0,7 % Uran-235 enthält, wird es in Anreicherungsanlagen {L("angereichert")}. '
           f'Für ein Kraftwerk reichen 3 bis 5 % Uran-235, für eine Bombe braucht man etwa 90 %. '
           f'Deshalb kann ein Kernkraftwerk {L("nicht")} wie eine Atombombe explodieren.</p>')
    lt9 = luecken("Im Reaktor steckt kein reines Uran-235, sondern [[angereichertes Uran]]. Es sitzt in fingerdicken Metallröhren, den [[Brennstäben]]. "
                  "Die Brennstäbe stehen im [[Wasser]]. Zwischen die Brennstäbe lassen sich Steuerstäbe aus [[Bor]] oder Cadmium schieben. "
                  "Sie fangen Neutronen ein und [[regeln]] so die Kettenreaktion. Ganz hineingefahren stoppen sie die Kettenreaktion.", l)
    return (abschnitt(7, "Was ist eine kontrollierte Kettenreaktion?", 1, "W17")
            + '<p class="frage">Zeichne rechts neben das Kraftwerk, wie die Kettenreaktion abläuft. Erkläre in einem Satz.</p>'
            + zeichnen_neben_bild("kernkraftwerk.png", kontrolliert(l))
            + antwort("Von den freien Neutronen löst im Mittel genau eines die nächste Spaltung aus, die Leistung bleibt gleich.", l, 1)
            + abschnitt(8, "Was ist eine unkontrollierte Kettenreaktion?", 1, "W17")
            + '<p class="frage">Zeichne rechts, wie die Kettenreaktion abläuft, wenn jede Spaltung zwei neue Spaltungen auslöst.</p>'
            + zeichnen_neben_bild("atompilz.png", unkontrolliert(l))
            + antwort("Die Zahl der Spaltungen verdoppelt sich in jedem Schritt. In Bruchteilen einer Sekunde wird riesig viel Energie frei.", l, 1)
            + abschnitt(9, "Was ist die kritische Masse?", 2, "W17") + lt8
            + abschnitt(10, "Wie läuft die Kettenreaktion im Reaktor?", 0, "W17") + f'<p class="frage lt">{lt9}</p>')


def seite4(l):
    L = lambda s: f'<span class="luecke loesungstext">{s}</span>' if l else '<span class="luecke" style="min-width:34mm"></span>'
    kette_e = f'<p class="frage lt">Kernenergie → {L("Wärme (innere Energie)")} → {L("Bewegungsenergie (Turbine)")} → {L("elektrische Energie")}</p>'
    fus = f'<p class="gl" style="font-size:12.5pt">{nk("H", 2, 1)} + {nk("H", 3, 1)} → {L(nk("He", 4, 2)) if l else L("")} + {L(nk("n", 1, 0)) if l else L("")} + Energie</p>'
    return ('<span class="stunde">STUNDE 3 · DAS KERNKRAFTWERK</span>'
            + abschnitt(11, "Wie ist der Kernreaktor aufgebaut?", 0, "W18")
            + '<p class="frage">Beschrifte die Teile 1 bis 7.</p>' + reaktor_bild(l)
            + abschnitt(12, "Welche Aufgaben hat das Wasser?", 1, "W18")
            + '<p class="frage">Die Bilder zeigen: schnelle Neutronen aus einer Spaltung, das Wasser, langsame Neutronen am nächsten Kern. Nenne drei Aufgaben des Wassers.</p>'
            + f'<div style="width:120mm;margin:1mm auto 2mm">{img("wasser-moderator.png")}</div>'
            + "".join(f'<div style="display:flex;gap:2mm;align-items:baseline"><span>{i}.</span><div style="flex:1">{antwort(t, l, 1)}</div></div>'
                      for i, t in ((1, "Moderator: bremst die schnellen Neutronen ab, damit sie Uran-235 spalten können"),
                                   (2, "Kühlmittel: transportiert die Wärme aus dem Reaktor zum Dampferzeuger"),
                                   (3, "Abschirmung: hält einen Teil der Strahlung zurück")))
            + abschnitt(13, "Vom Reaktor zum Strom", 1, "W18")
            + '<p class="frage">Ergänze die Energieumwandlungen. Ab der Wärme arbeitet ein Kohlekraftwerk genauso.</p>' + kette_e
            + abschnitt(14, "Ausblick: Kernfusion", 2, "W18")
            + '<p class="frage">In der Sonne verschmelzen leichte Kerne. Ergänze die Gleichung der Fusion von Deuterium und Tritium.</p>' + fus)


if __name__ == "__main__":
    seiten_s = [seite1(False), seite2(False), seite3(False), seite4(False)]
    seiten_l = [seite1(True), seite2(True), seite3(True), seite4(True)]
    html = dokument("Begleitheft Kernspaltung und Kettenreaktion", seiten_s + seiten_l).replace("</head>", HEFT_CSS + "</head>")
    (HIER / "Begleitheft Kernspaltung.html").write_text(html, encoding="utf-8")
    print("geschrieben: Begleitheft Kernspaltung.html")
