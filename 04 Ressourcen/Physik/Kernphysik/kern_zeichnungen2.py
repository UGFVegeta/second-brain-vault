#!/usr/bin/env python3
"""Kernphysik-Folien ab Leitfrage 3 (Folie 24 bis 71) im Labor-Stil B. Bausteine aus kern_zeichnungen.py.
Aufruf: python3 kern_zeichnungen2.py -> ersetzt die Zeichnungen in Kernphysik.html (Seiten siehe ZEICHNUNGEN2)."""
import math, re
from pathlib import Path
from kern_zeichnungen import Z, INK, GELB, ORANGE, CYAN, PROTON, NEUTRON, ELEKTRON, VIOLETT, teilchen, kern, elektron, bahn, nuklid, welle

HIER = Path(__file__).parent
GRAU, HELL, GRUEN, ROT, BLAU = "#66798E", "#9AAAC0", "#3FA34D", "#D8453B", "#3B7CC4"


def achsen(z, x0, y0, w, h, xl, yl):
    z.pfeil(x0, y0, x0 + w, y0, GRAU, 1.6, 8).pfeil(x0, y0, x0, y0 - h, GRAU, 1.6, 8)
    z.text(x0 + w, y0 - 8, xl, "end", 9.5).text(x0 + 6, y0 - h + 4, yl, size=9.5)


def kasten(z, x, y, w, h, fill, rand, titel="", zeilen=(), size=9):
    z.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{rand}" stroke-width="1.4"/>')
    if titel:
        z.text(x + 8, y + 16, titel, size=9.5, weight=600, halo=fill)
    for i, s in enumerate(zeilen):
        z.text(x + 8, y + (32 if titel else 16) + i * 13, s, size=size, halo=fill)
    return z


def wuerfel(z, x, y, a, augen, fill="#FFFFFF", punkt=INK):
    z.add(f'<rect x="{x}" y="{y}" width="{a}" height="{a}" rx="{a * .18:.1f}" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>')
    p = {1: [(.5, .5)], 2: [(.25, .25), (.75, .75)], 3: [(.25, .25), (.5, .5), (.75, .75)],
         6: [(.28, .22), (.28, .5), (.28, .78), (.72, .22), (.72, .5), (.72, .78)]}[augen]
    for u, v in p:
        z.add(f'<circle cx="{x + u * a:.1f}" cy="{y + v * a:.1f}" r="{a * .08:.1f}" fill="{punkt}"/>')


# ---------------------------------------------------------------- Leitfrage 3
def beobachte_wuerfel():
    z = Z("kw", 245)
    wuerfel(z, 60, 60, 42, 2)
    wuerfel(z, 116, 60, 42, 3)
    wuerfel(z, 172, 60, 42, 6, "#E8604A", "#FFFFFF")
    z.text(137, 128, "Eine Sechs heißt: „zerfallen“", "middle", 9.5).text(137, 142, "Dieser Würfel scheidet aus.", "middle", 9.5)
    x0, y0 = 300, 200
    achsen(z, x0, y0, 332, 170, "Wurf", "übrige Würfel")
    for n in range(9):
        v = 100 * (5 / 6) ** n
        h = v * 1.5
        z.rect(x0 + 12 + n * 33, y0 - h, 22, h, NEUTRON, 1, 2)
        z.text(x0 + 23 + n * 33, y0 - h - 5, f"{v:.0f}", "middle", 8.5)
        z.text(x0 + 23 + n * 33, y0 + 14, str(n), "middle", 8.5)
    z.text(137, 200, "100 Würfel, alle werfen gleichzeitig.", "middle", 9.5).text(137, 214, "Jede Runde fällt etwa ein Sechstel weg.", "middle", 9.5)
    return z.svg()


def halbwertszeit():
    z = Z("kh", 230)
    x0, y0, sx, sy = 70, 196, 9.6, 0.68
    achsen(z, x0, y0, 540, 180, "t in s", "")
    z.formel(x0 + 8, y0 - 170, "N")
    pts = " ".join(f"{x0 + t * sx:.1f},{y0 - 240 * 0.5 ** (t / 11) * sy:.1f}" for t in [i * 0.5 for i in range(0, 111)])
    z.add(f'<polyline points="{pts}" fill="none" stroke="{CYAN}" stroke-width="2.6"/>')
    for k in range(1, 4):
        t, n = 11 * k, 240 / 2 ** k
        X, Y = x0 + t * sx, y0 - n * sy
        z.line(x0, Y, X, Y, ROT, 1.2, "4 4").line(X, Y, X, y0, ROT, 1.2, "4 4")
        z.add(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="4" fill="{ROT}"/>')
        z.text(X + 7, Y - 6, f"nach {k} · 11 s: {n:.0f}", size=9)
        z.text(X, y0 + 14, str(t), "middle", 8.5)
        z.text(x0 - 6, Y + 3, f"{n:.0f}", "end", 8.5)
    z.text(x0 - 6, y0 - 240 * sy + 3, "240", "end", 8.5)
    z.text(430, 40, "Fluor-20", weight=600).text(430, 56, "Halbwertszeit 11 s", size=9.5).text(430, 70, "Start: 240 Kerne", size=9.5)
    z.text(430, 92, "Die Kurve erreicht nie null.", size=9)
    return z.svg()


def aktivitaet():
    z = Z("kt", 220)
    px, py = 150, 110
    z.add(f'<path d="M{px - 34} {py + 30} h68 l-9 -26 h-50z" fill="#9FB2CF"/>')
    z.glow(px, py, 26)
    for k in range(12):
        a = math.radians(k * 30 + 15)
        z.pfeil(px + 16 * math.cos(a), py + 16 * math.sin(a), px + 70 * math.cos(a), py + 70 * math.sin(a), VIOLETT, 1.5, 7)
    z.add(f'<rect x="248" y="96" width="90" height="26" rx="13" fill="#9FB2CF"/><rect x="244" y="96" width="8" height="26" rx="2" fill="#F5E6C8"/>')
    z.line(px + 18, py - 4, 244, 104, VIOLETT, 1.6, "3 3").line(px + 18, py + 4, 244, 116, VIOLETT, 1.6, "3 3")
    z.add('<rect x="380" y="78" width="130" height="64" rx="9" fill="#26324A"/><rect x="392" y="88" width="106" height="30" rx="3" fill="#0A1120"/>'
          '<text x="445" y="110" font-family="PlexMono, Menlo, monospace" font-size="17" fill="#6FE39A" text-anchor="middle">137/min</text>')
    z.line(338, 109, 380, 109, "#9FB2CF", 3)
    z.text(px, 196, "Aktivität A: alle Zerfälle pro Sekunde", "middle", 9.5, 600).text(px, 210, "1 Bq = 1 Zerfall pro Sekunde", "middle", 9)
    z.text(445, 166, "Zählrate: nur die Strahlung,", "middle", 9.5, 600).text(445, 180, "die ins Zählrohr fliegt", "middle", 9)
    z.text(295, 80, "Zählrohr", "middle", 9)
    return z.svg()


# ---------------------------------------------------------------- Leitfrage 4
def warnzeichen(z, x, y, r):
    z.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFD34D" stroke="{INK}" stroke-width="2"/>')
    for k in range(3):
        a0 = math.radians(-90 + k * 120 - 30)
        a1 = math.radians(-90 + k * 120 + 30)
        ri, ro = r * .28, r * .86
        z.add(f'<path d="M{x + ri * math.cos(a0):.1f} {y + ri * math.sin(a0):.1f} L{x + ro * math.cos(a0):.1f} {y + ro * math.sin(a0):.1f} '
              f'A{ro} {ro} 0 0 1 {x + ro * math.cos(a1):.1f} {y + ro * math.sin(a1):.1f} L{x + ri * math.cos(a1):.1f} {y + ri * math.sin(a1):.1f} '
              f'A{ri} {ri} 0 0 0 {x + ri * math.cos(a0):.1f} {y + ri * math.sin(a0):.1f}Z" fill="{INK}"/>')
    z.add(f'<circle cx="{x}" cy="{y}" r="{r * .18:.1f}" fill="{INK}"/>')


def beobachte_roentgen():
    z = Z("kb", 245)
    z.rect(110, 34, 150, 170, "#0A1120", 1, 8)
    finger = [(-38, 60, -8), (-18, 78, -3), (2, 82, 0), (22, 74, 4), (44, 44, 30)]
    cx, cy = 185, 170
    z.add(f'<path d="M{cx - 40} {cy + 30} q-6 -40 6 -62 h68 q12 22 6 62z" fill="#DCE6F2" opacity=".9"/>')
    for dx, L, rot in finger:
        z.add(f'<g transform="rotate({rot} {cx + dx} {cy - 30})"><rect x="{cx + dx - 6}" y="{cy - 30 - L}" width="12" height="{L}" rx="6" fill="#DCE6F2" opacity=".9"/>'
              f'<line x1="{cx + dx - 6}" y1="{cy - 30 - L * .45:.1f}" x2="{cx + dx + 6}" y2="{cy - 30 - L * .45:.1f}" stroke="#0A1120" stroke-width="1.5"/></g>')
    z.text(185, 226, "Röntgenbild beim Arzt", "middle", 9.5)
    warnzeichen(z, 450, 118, 70)
    z.text(450, 226, "Warnzeichen im Labor", "middle", 9.5)
    z.text(318, 124, "?", "middle", 30, 700, GRAU)
    return z.svg()


def ionisation():
    z = Z("kn")
    for (cx, ion) in ((150, False), (470, True)):
        bahn(z, cx, 104, 58)
        kern(z, cx, 104, 3, 3, r=7, seed=4)
        for a in (30, 150, 270):
            if ion and a == 30:
                z.add(f'<circle cx="{cx + 58 * math.cos(math.radians(a)):.1f}" cy="{104 - 58 * math.sin(math.radians(a)):.1f}" r="7" fill="none" stroke="{ELEKTRON}" stroke-dasharray="3 3"/>')
                continue
            elektron(z, cx + 58 * math.cos(math.radians(a)), 104 - 58 * math.sin(math.radians(a)))
    ex, ey = 150 + 58 * math.cos(math.radians(30)), 104 - 58 * math.sin(math.radians(30))
    z.pfeil(40, 20, ex - 8, ey - 4, ORANGE, 2.4)
    z.text(40, 14, "Strahlung", size=9.5)
    z.pfeil(250, 104, 360, 104, GRAU, 2)
    fx, fy = 470 + 58 * math.cos(math.radians(30)), 104 - 58 * math.sin(math.radians(30))
    z.pfeil(fx + 6, fy - 4, fx + 80, fy - 50, ELEKTRON, 1.8, 7)
    elektron(z, fx + 88, fy - 56)
    z.text(fx + 30, fy - 64, "herausgeschlagenes Elektron", "end", 9)
    z.text(470 + 26, 86, "+", size=18, weight=700, col=ROT)
    z.text(150, 196, "neutrales Atom", "middle", weight=600).text(470, 196, "Ion, positiv geladen", "middle", weight=600)
    return z.svg()


def zelle():
    z = Z("kc", 230)
    z.add('<ellipse cx="150" cy="112" rx="120" ry="86" fill="#F3EAD9" stroke="#C6B48E" stroke-width="2"/>'
          '<ellipse cx="150" cy="112" rx="46" ry="40" fill="#E5D9F2" stroke="#9C84C4" stroke-width="1.6"/>')
    d1 = " ".join(f"{120 + t * 3:.1f},{112 + 14 * math.sin(t * .55):.1f}" for t in range(21))
    d2 = " ".join(f"{120 + t * 3:.1f},{112 - 14 * math.sin(t * .55):.1f}" for t in range(21))
    z.add(f'<polyline points="{d1}" fill="none" stroke="{VIOLETT}" stroke-width="1.8"/><polyline points="{d2}" fill="none" stroke="{VIOLETT}" stroke-width="1.8"/>')
    for t in range(1, 20, 2):
        z.line(120 + t * 3, 112 + 14 * math.sin(t * .55), 120 + t * 3, 112 - 14 * math.sin(t * .55), "#C3B2DE", 1)
    z.pfeil(20, 20, 146, 104, ORANGE, 2.4)
    z.add(f'<path d="M146 104 l6 -8 l2 7 l8 -3 l-5 7 l7 3 l-9 1 z" fill="{ROT}"/>')
    z.text(150, 216, "Zelle mit Zellkern und DNA", "middle", 9.5)
    kasten(z, 330, 20, 290, 52, "#E4F2E3", GRUEN, "1  Reparatur", ["Die Zelle repariert den Schaden vollständig."])
    kasten(z, 330, 82, 290, 52, "#FFF2D6", "#E0A42A", "2  Zelltod", ["Die Zelle stirbt ab, der Körper ersetzt sie."])
    kasten(z, 330, 144, 290, 66, "#FBE3E0", ROT, "3  Veränderung", ["Die Zelle lebt verändert weiter.", "Jahre später kann daraus Krebs entstehen."])
    for y in (46, 108, 177):
        z.pfeil(272, 112, 326, y, GRAU, 1.4, 7)
    return z.svg()


def belastung():
    z = Z("kl", 235)
    x0, y0, s = 60, 190, 60
    achsen(z, x0, y0, 560, 170, "", "mSv pro Jahr")
    daten = [("Radon", 1.1, GRUEN), ("Boden", 0.4, GRUEN), ("Nahrung", 0.3, GRUEN), ("Weltall", 0.3, GRUEN),
             ("Medizin", 1.5, ROT), ("sonstiges", 0.01, ROT)]
    for i, (n, v, c) in enumerate(daten):
        x = x0 + 30 + i * 70 + (40 if i >= 4 else 0)
        z.rect(x, y0 - v * s * 1.5, 44, max(v * s * 1.5, 1.5), c, .85, 2)
        z.text(x + 22, y0 - v * s * 1.5 - 6, f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ","), "middle", 9)
        z.text(x + 22, y0 + 14, n, "middle", 8.5)
    for v in (0.5, 1.0, 1.5):
        z.text(x0 - 5, y0 - v * s * 1.5 + 3, str(v).replace(".", ","), "end", 8.5)
    z.text(175, 214, "natürlich: zusammen etwa 2,1 mSv", "middle", 9.5, 600, GRUEN)
    z.text(470, 214, "künstlich: etwa 1,5 mSv, fast nur Medizin", "middle", 9.5, 600, ROT)
    kasten(z, 220, 22, 180, 60, "#FFFFFF", HELL, "", ["Flug nach New York und", "zurück: etwa 0,1 mSv", "Röntgen Brustkorb: 0,02 mSv"], 8.5)
    z.text(620, 230, "Durchschnitt in Deutschland, Quelle: BfS", "end", 7.5, col=GRAU)
    return z.svg()


def schutz():
    z = Z("ku", 230)
    y = 44
    z.text(24, 22, "Schutz", weight=600)
    z.lampe(40, y + 4, VIOLETT, 5).pfeil(62, y + 4, 170, y + 4, GRAU, 1.6, 7)
    z.text(190, y, "Abstand halten").text(190, y + 14, "doppelter Abstand: ein Viertel", size=9)
    z.add(f'<circle cx="44" cy="{y + 58}" r="15" fill="#FFFFFF" stroke="{GRAU}" stroke-width="2"/>'
          f'<line x1="44" y1="{y + 58}" x2="44" y2="{y + 48}" stroke="{INK}" stroke-width="2"/><line x1="44" y1="{y + 58}" x2="52" y2="{y + 62}" stroke="{INK}" stroke-width="2"/>')
    z.text(190, y + 54, "Aufenthalt kurz halten").text(190, y + 68, "halbe Zeit: halbe Dosis", size=9)
    z.rect(30, y + 100, 30, 34, "#4D5E77", 1, 2)
    z.text(190, y + 112, "Abschirmen").text(190, y + 126, "Blei, Beton, Wasser", size=9)
    z.text(24, y + 164, "dazu: Aktivität klein halten, nichts in den Körper aufnehmen", size=9, col=GRAU)
    z.line(370, 14, 370, 216, "#A3B7D3", 1, "5 4")
    z.text(392, 22, "Anwendungen", weight=600)
    for i, (t, s) in enumerate((("Medizin", "Röntgen, Szintigramm, Strahlentherapie"), ("Technik", "Schweißnähte prüfen, Dicken messen"),
                                 ("Sterilisation", "Spritzen und Verbandszeug keimfrei machen"), ("Forschung", "Altersbestimmung mit C-14"))):
        z.text(392, 50 + i * 42, t, weight=600).text(392, 64 + i * 42, s, size=8.8)
    return z.svg()


# ---------------------------------------------------------------- Leitfrage 5
def beobachte_energie():
    z = Z("ke", 235)
    for r in range(3):
        for c in range(6):
            x, y = 40 + c * 44, 60 + r * 40
            z.add(f'<path d="M{x} {y} h38 l-4 26 h-30z" fill="#3B4150"/><circle cx="{x + 9}" cy="{y + 30}" r="4" fill="{GRAU}"/><circle cx="{x + 29}" cy="{y + 30}" r="4" fill="{GRAU}"/>')
            z.add(f'<path d="M{x + 2} {y} q17 -12 34 0z" fill="#14171c"/>')
    z.text(170, 190, "etwa 3000 t Steinkohle", "middle", weight=600).text(170, 205, "(hier nur ein Teil der Waggons)", "middle", 9)
    z.text(345, 120, "=", "middle", 28, 700, GRAU)
    z.rect(440, 104, 16, 16, "#9FB2CF", 1, 2)
    z.glow(448, 112, 22)
    z.rect(440, 104, 16, 16, "#9FB2CF", 1, 2)
    z.text(448, 190, "1 kg Uran-235", "middle", weight=600).text(448, 205, "vollständig gespalten", "middle", 9)
    z.text(318, 30, "gleich viel Wärme", "middle", 11, 600)
    return z.svg()


def spaltung():
    z = Z("kp", 240)
    teilchen(z, 30, 100, 8, NEUTRON)
    z.pfeil(42, 100, 84, 100, NEUTRON, 2)
    kern(z, 130, 100, 14, 20, r=6, seed=21)
    z.text(130, 168, "Uran-235", "middle", 9.5)
    z.pfeil(186, 100, 226, 100, GRAU, 2)
    z.add('<ellipse cx="282" cy="100" rx="52" ry="38" fill="none" stroke="#E8604A" stroke-width="1.4" stroke-dasharray="3 4"/>')
    kern(z, 282, 100, 14, 21, r=6, seed=22)
    z.text(282, 168, "Uran-236, instabil", "middle", 9.5)
    z.pfeil(338, 88, 410, 50, GRAU, 2).pfeil(338, 112, 410, 150, GRAU, 2)
    kern(z, 450, 48, 8, 11, r=6, seed=23)
    kern(z, 450, 156, 6, 9, r=6, seed=24)
    z.text(496, 30, "Barium-141").text(496, 186, "Krypton-92")
    for i, y in enumerate((80, 102, 124)):
        z.pfeil(340, 100, 540, y, "#8FA3BD", 1.2, 6)
        teilchen(z, 548, y, 6, NEUTRON)
    z.text(560, 104, "3 Neutronen", size=9)
    welle(z, 500, 212, 590, ORANGE)
    z.text(596, 216, "Energie", size=9.5)
    y = 226
    nuklid(z, 60, y, "n", 1, 0, 16).text(78, y, "+", size=12)
    nuklid(z, 112, y, "U", 235, 92, 16).text(136, y, "→", size=12)
    nuklid(z, 172, y, "Ba", 141, 56, 16).text(200, y, "+", size=12)
    nuklid(z, 236, y, "Kr", 92, 36, 16).text(262, y, "+ 3", size=12)
    nuklid(z, 296, y, "n", 1, 0, 16)
    z.text(330, y, "+ Energie", size=10)
    return z.svg()


def kettenreaktion():
    z = Z("kk", 225)
    z.text(24, 20, "kontrolliert: im Reaktor", weight=600)
    for i in range(4):
        x = 40 + i * 70
        kern(z, x, 70, 4, 5, r=5, seed=30 + i)
        if i < 3:
            z.pfeil(x + 16, 70, x + 54, 70, NEUTRON, 1.8, 7)
        z.pfeil(x + 6, 82, x - 6, 104, "#B8C4D6", 1.2, 6)
    z.text(24, 136, "Von den freien Neutronen löst im Mittel", size=9).text(24, 150, "genau eines die nächste Spaltung aus.", size=9)
    z.text(24, 164, "Die anderen fangen die Steuerstäbe ein.", size=9)
    z.text(24, 196, "gleichmäßige Leistung", weight=600, col=GRUEN)
    z.line(330, 10, 330, 214, "#A3B7D3", 1, "5 4")
    z.text(350, 20, "unkontrolliert: Kernwaffe", weight=600)
    lv = [[(380, 110)]]
    for g in range(1, 4):
        lv.append([(380 + g * 70, y0 + d) for (x, y0) in lv[-1] for d in (-46 / g ** 1.1, 46 / g ** 1.1)])
    for g in range(len(lv)):
        for (x, y) in lv[g]:
            kern(z, x, y, 2, 3, r=4, seed=40 + g)
            if g + 1 < len(lv):
                for (x2, y2) in lv[g + 1]:
                    if abs(y2 - y) < 50 / (g + 1) ** 1.1 + 1:
                        z.pfeil(x + 10, y, x2 - 10, y2, NEUTRON, 1.3, 6)
    for g in range(4):
        z.text(380 + g * 70, 222, str(2 ** g), "middle", 9)
    z.text(620, 222, "Spaltungen", "end", 8.5, col=GRAU)
    return z.svg()


def reaktor():
    z = Z("kv", 230)
    z.add('<rect x="40" y="40" width="190" height="160" rx="22" fill="#DCEBF7" stroke="#6E8FB5" stroke-width="3"/>')
    for i in range(6):
        z.rect(62 + i * 28, 96, 12, 90, "#E8604A", 1, 3)
    for i in range(5):
        z.rect(78 + i * 28, 20, 8, 110, "#3B4150", 1, 2)
    z.text(135, 16, "Steuerstäbe", "middle", 9)
    z.text(135, 218, "Brennstäbe im Wasser", "middle", 9)
    z.pfeil(230, 70, 300, 70, ROT, 2.4).pfeil(300, 170, 230, 170, BLAU, 2.4)
    z.add('<rect x="300" y="50" width="70" height="140" rx="30" fill="#EEF1F5" stroke="#66798E" stroke-width="2"/>')
    z.text(335, 206, "Dampferzeuger", "middle", 9)
    z.pfeil(370, 70, 440, 70, "#B8C4D6", 3)
    z.add('<path d="M440 50 L500 36 L500 104 L440 90 Z" fill="#9FB2CF"/>')
    z.text(470, 124, "Turbine", "middle", 9)
    z.line(500, 70, 530, 70, INK, 3)
    z.add(f'<circle cx="556" cy="70" r="24" fill="#FFD34D" stroke="{GELB}" stroke-width="2"/>')
    z.text(556, 74, "G", "middle", 12, 700)
    z.text(556, 112, "Generator", "middle", 9)
    kasten(z, 400, 144, 220, 66, "#FFFFFF", HELL, "", ["Steuerstäbe schlucken Neutronen.", "Das Wasser bremst die Neutronen", "(Moderator) und kühlt."], 8.8)
    return z.svg()


def kraftwerke():
    z = Z("kf", 225)
    for row, (titel, erst, farbe) in enumerate((("Kernkraftwerk", ["Kernenergie", "im Uran"], "#FBE3E0"), ("Kohlekraftwerk", ["chemische Energie", "der Kohle"], "#EEF1F5"))):
        y = 30 + row * 100
        z.text(24, y - 8, titel, weight=600)
        kasten(z, 24, y, 138, 44, farbe, ROT if row == 0 else GRAU, "", erst, 8.8)
        for i, t in enumerate(("Wärme, Dampf", "Bewegung (Turbine)", "elektrische Energie")):
            x = 200 + i * 145
            kasten(z, x, y, 120, 44, "#FFF8E5", "#E0A42A", "", [t], 8.8)
            z.pfeil(x - 34, y + 22, x - 4, y + 22, GRAU, 1.6, 7)
    z.text(318, 212, "Ab der Wärme sind beide Kraftwerke gleich aufgebaut.", "middle", 9.5, 600)
    return z.svg()


def fusion():
    z = Z("ku2", 230)
    kern(z, 60, 90, 1, 1, r=8, seed=2)
    z.text(60, 130, "Deuterium", "middle", 9)
    nuklid(z, 62, 158, "H", 2, 1, 18)
    z.text(110, 96, "+", "middle", 16)
    kern(z, 160, 90, 1, 2, r=8, seed=3)
    z.text(160, 130, "Tritium", "middle", 9)
    nuklid(z, 162, 158, "H", 3, 1, 18)
    z.pfeil(206, 90, 262, 90, GRAU, 2)
    kern(z, 310, 90, 2, 2, r=8, seed=5)
    z.text(310, 130, "Helium", "middle", 9)
    nuklid(z, 312, 158, "He", 4, 2, 18)
    z.text(360, 96, "+", "middle", 16)
    teilchen(z, 396, 90, 8, NEUTRON)
    z.text(396, 130, "Neutron", "middle", 9)
    welle(z, 420, 90, 480, ORANGE)
    z.text(450, 76, "Energie", "middle", 9)
    z.sonne(560, 80, 26)
    z.text(560, 140, "Sonne: etwa 15 Mio. °C", "middle", 9).text(560, 154, "im Inneren", "middle", 9)
    z.text(24, 198, "Kerne stoßen sich ab, weil beide positiv sind. Nur bei sehr hoher Temperatur kommen sie nah genug zusammen.", size=8.8)
    z.text(24, 214, "Auf der Erde braucht man über 100 Mio. °C, ein Kraftwerk gibt es noch nicht.", size=8.8)
    return z.svg()


# ---------------------------------------------------------------- Leitfrage 6
def beobachte_zeit():
    z = Z("kz2", 235)
    x0, x1 = 60, 560
    lg = lambda j: x0 + (x1 - x0) * math.log10(j) / 6
    z.pfeil(x0 - 20, 130, x1 + 20, 130, GRAU, 2, 9)
    for j, oben, unten, yu, an in ((1, "heute", "", 0, "middle"), (500, "500 Jahre", "Abfall bleibt rückholbar", 152, "middle"),
                                   (24000, "24 000 Jahre", "Halbwertszeit von Pu-239", 166, "middle"),
                                   (1000000, "1 Million Jahre", "so lange muss das Endlager sicher sein", 180, "end")):
        x = lg(j)
        z.add(f'<circle cx="{x:.1f}" cy="130" r="6" fill="#FFFFFF" stroke="{ROT}" stroke-width="2.2"/>')
        z.text(x, 112, oben, "middle", 9.5, 600)
        if unten:
            z.text(x + (8 if an == "end" else 0), yu, unten, an, 8.5)
    x = lg(4500)
    z.add(f'<circle cx="{x:.1f}" cy="130" r="5" fill="{GELB}"/>')
    z.text(x, 74, "zum Vergleich: die Pyramiden", "middle", 8.5, col=GRAU).text(x, 86, "sind etwa 4500 Jahre alt", "middle", 8.5, col=GRAU)
    z.line(x, 92, x, 124, GRAU, 1, "2 3")
    z.text(318, 30, "Zeitachse logarithmisch: jeder Abschnitt zehnmal so lang", "middle", 9, col=GRAU)
    return z.svg()


def abfall():
    z = Z("kx", 225)
    z.add('<rect x="30" y="60" width="150" height="100" rx="4" fill="#BFE3F5" stroke="#6E8FB5" stroke-width="2"/>')
    for i in range(5):
        z.rect(52 + i * 24, 84, 12, 70, "#E8604A", 1, 2)
    z.text(105, 50, "Abklingbecken", "middle", weight=600).text(105, 182, "im Kraftwerk, mehrere Jahre", "middle", 8.8)
    z.pfeil(188, 110, 226, 110, GRAU, 2)
    z.add('<path d="M236 160 V90 L310 60 L384 90 V160 Z" fill="#EEF1F5" stroke="#66798E" stroke-width="2"/>')
    for i in range(3):
        z.rect(256 + i * 36, 110, 26, 46, "#8FA3BD", 1, 6)
    z.text(310, 50, "Zwischenlager", "middle", weight=600).text(310, 182, "Castor-Behälter, Jahrzehnte", "middle", 8.8)
    z.pfeil(392, 110, 430, 110, GRAU, 2)
    z.rect(440, 40, 180, 20, "#A8C686", 1)
    z.rect(440, 60, 180, 110, "#D9C7A7", 1)
    z.line(530, 60, 530, 140, "#6E5A3C", 3)
    for i in range(4):
        z.rect(478 + i * 28, 142, 18, 18, "#8FA3BD", 1, 3)
    z.line(470, 140, 590, 140, "#6E5A3C", 2)
    z.text(530, 30, "Endlager tief im Gestein", "middle", weight=600).text(530, 182, "Salz, Ton oder Granit", "middle", 8.8)
    z.text(530, 196, "Standort wird noch gesucht", "middle", 8.8, col=ROT)
    return z.svg()


def argumente():
    z = Z("kg2", 230)
    dafuer = ["im Betrieb kaum CO₂", "sehr viel Energie aus wenig Brennstoff", "liefert Strom unabhängig vom Wetter", "Strahlung hilft in der Medizin"]
    dagegen = ["Abfall strahlt sehr lange", "noch kein Endlager in Betrieb", "schwere Unfälle möglich (Tschernobyl, Fukushima)", "hohe Kosten für Bau und Rückbau"]
    for x, t, liste, f, r in ((24, "spricht dafür", dafuer, "#E4F2E3", GRUEN), (328, "spricht dagegen", dagegen, "#FBE3E0", ROT)):
        z.add(f'<rect x="{x}" y="14" width="284" height="200" rx="8" fill="{f}" stroke="{r}" stroke-width="1.6"/>')
        z.text(x + 12, 36, t, weight=600, halo=f)
        for i, s in enumerate(liste):
            z.text(x + 12, 66 + i * 36, "• " + s, size=9.2, halo=f)
    return z.svg()


def c14():
    z = Z("kq", 230)
    z.rect(56, 110, 10, 60, "#8B5E34", 1, 2)
    z.add('<circle cx="61" cy="92" r="34" fill="#4B9A3B"/>')
    z.text(61, 190, "lebender Baum", "middle", 9).text(61, 204, "nimmt C-14 auf", "middle", 8.5)
    z.pfeil(120, 130, 176, 130, GRAU, 2).text(148, 120, "stirbt", "middle", 9)
    z.rect(196, 140, 46, 30, "#8B5E34", 1, 3)
    z.text(219, 190, "Holzfund", "middle", 9).text(219, 204, "kein Nachschub mehr", "middle", 8.5)
    x0, y0, sx, sy = 300, 180, 0.0165, 1.5
    achsen(z, x0, y0, 320, 160, "Jahre", "C-14 in %")
    pts = " ".join(f"{x0 + t * sx:.1f},{y0 - 100 * 0.5 ** (t / 5730) * sy:.1f}" for t in range(0, 18001, 300))
    z.add(f'<polyline points="{pts}" fill="none" stroke="{CYAN}" stroke-width="2.4"/>')
    for k in (1, 2, 3):
        X, Y = x0 + 5730 * k * sx, y0 - 100 / 2 ** k * sy
        z.line(X, Y, X, y0, ROT, 1, "4 4")
        z.text(X, y0 + 13, f"{5730 * k:,}".replace(",", " "), "middle", 8)
        z.text(X + 5, Y - 5, f"{100 / 2 ** k:g}".replace(".", ",") + " %", size=8.5)
    Xo = x0 + 5300 * sx
    z.add(f'<circle cx="{Xo:.1f}" cy="{y0 - 100 * 0.5 ** (5300 / 5730) * sy:.1f}" r="4.5" fill="{GELB}"/>')
    Yo = y0 - 100 * 0.5 ** (5300 / 5730) * sy
    z.line(Xo + 4, Yo - 4, 470, 52, GRAU, 1, "2 3").text(474, 50, "Ötzi: etwa 5300 Jahre", size=8.5)
    return z.svg()


ZEICHNUNGEN2 = {24: beobachte_wuerfel, 27: halbwertszeit, 29: aktivitaet, 33: beobachte_roentgen, 36: ionisation, 38: zelle,
                40: belastung, 42: schutz, 46: beobachte_energie, 49: spaltung, 51: kettenreaktion, 53: reaktor, 55: kraftwerke,
                57: fusion, 61: beobachte_zeit, 64: abfall, 66: argumente, 71: c14}

if __name__ == "__main__":
    p = HIER / "Kernphysik.html"
    s = p.read_text(encoding="utf-8")
    teile = re.split(r'(<section class="folie[^"]*">.*?</section>)', s, flags=re.S)
    idx = [i for i, t in enumerate(teile) if t.startswith('<section class="folie')]
    for seite, fn in ZEICHNUNGEN2.items():
        i = idx[seite - 1]
        teile[i] = re.sub(r"<svg.*?</svg>", lambda m: fn(), teile[i], count=1, flags=re.S)
    p.write_text("".join(teile), encoding="utf-8")
    print("Kernphysik.html ersetzt:", ", ".join(f"S. {k}" for k in ZEICHNUNGEN2))
