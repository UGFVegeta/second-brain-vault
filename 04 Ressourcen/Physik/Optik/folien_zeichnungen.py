#!/usr/bin/env python3
"""Folien-Zeichnungen im Labor-Stil auf hellem Karo (Variante B, festgelegt 24.09.2026).
Leuchtende Lampen, farbige Strahlen, abgestufte Schatten, Begriffe in IBM Plex Mono, Formelzeichen kursiv mit Index.
Randstrahlen werden berechnet, nicht geschätzt.
Aufruf: python3 folien_zeichnungen.py  -> ersetzt die Zeichnungen in 'Optik I.html' (Seiten siehe ZEICHNUNGEN)."""
import math, re
from pathlib import Path

HIER = Path(__file__).parent
GELB, ORANGE, CYAN = "#E39B00", "#E8641B", "#0B8FB8"
INK, KOERPER, SCHIRM, WAND, KERN, HALB = "#101A2B", "#9FB2CF", "#FFE29A", "#4D5E77", 0.78, 0.28


class Z:
    """Sammelt SVG-Teile; pre = eindeutiger Präfix für ids (mehrere Folien in einem Dokument)."""
    def __init__(self, pre, h=212):
        self.pre, self.h, self.o = pre, h, []
        self.o.append(f'<defs><radialGradient id="{pre}gl"><stop offset="0" stop-color="#FFE7A0" stop-opacity=".95"/>'
                      f'<stop offset="1" stop-color="#FFC53D" stop-opacity="0"/></radialGradient>'
                      f'<linearGradient id="{pre}wa" x1="0" x2="1"><stop offset="0" stop-color="#FFC53D" stop-opacity=".32"/>'
                      f'<stop offset="1" stop-color="#FFC53D" stop-opacity=".05"/></linearGradient>'
                      f'<radialGradient id="{pre}ball" cx=".35" cy=".35" r=".75"><stop offset="0" stop-color="#FF9C7A"/>'
                      f'<stop offset="1" stop-color="#B8391F"/></radialGradient></defs>')

    def add(self, s): self.o.append(s); return self
    def poly(self, pts, fill, op): return self.add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" fill-opacity="{op}"/>')
    def rect(self, x, y, w, h, fill, op=1, rx=0): return self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}"/>')
    def line(self, x1, y1, x2, y2, col=GELB, w=2.2, dash=None, op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round"{d}/>')

    def pfeil(self, x1, y1, x2, y2, col=GELB, w=2.2, s=9):
        dx, dy = x2 - x1, y2 - y1
        l = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / l, dy / l
        bx, by = x2 - ux * s, y2 - uy * s
        self.line(x1, y1, bx + ux * 1, by + uy * 1, col, w)
        return self.poly([(x2, y2), (bx - uy * s * .45, by + ux * s * .45), (bx + uy * s * .45, by - ux * s * .45)], col, 1)

    def lampe(self, x, y, ring=GELB, r=6.5):
        return self.add(f'<circle cx="{x}" cy="{y}" r="{r * 3.1:.1f}" fill="url(#{self.pre}gl)"/>'
                        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF3C4" stroke="{ring}" stroke-width="2.5"/>')

    def wash(self, x, y, w, h): return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{self.pre}wa)" opacity=".75"/>')

    def text(self, x, y, s, anchor="start", size=10.5, weight=500, col=INK, halo="#FFFFFF"):
        return self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="PlexMono, Menlo, monospace" font-size="{size}" font-weight="{weight}" '
                        f'fill="{col}" text-anchor="{anchor}" paint-order="stroke" stroke="{halo}" stroke-width="3" stroke-linejoin="round">{s}</text>')

    # ---- Symbole
    def glow(self, x, y, r): return self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{self.pre}gl)"/>')

    def sonne(self, x, y, r=14):
        self.glow(x, y, r * 2.6)
        for k in range(8):
            a = math.radians(k * 45)
            self.line(x + (r + 4) * math.cos(a), y + (r + 4) * math.sin(a), x + (r + 10) * math.cos(a), y + (r + 10) * math.sin(a), GELB, 2)
        return self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFD34D" stroke="{GELB}" stroke-width="2"/>')

    def gluehlampe(self, x, y, fill="#FFF3C4", ring=GELB):
        self.glow(x, y, 34)
        return self.add(f'<circle cx="{x}" cy="{y}" r="13" fill="{fill}" stroke="{ring}" stroke-width="2"/>'
                        f'<rect x="{x - 6}" y="{y + 12}" width="12" height="9" rx="1.5" fill="#9FB2CF"/>')

    def kerze(self, x, y):
        self.glow(x, y - 14, 26)
        return self.add(f'<rect x="{x - 6}" y="{y - 4}" width="12" height="28" rx="1.5" fill="#F5E6C8" stroke="#C6B48E"/>'
                        f'<path d="M{x} {y - 24} q8 10 0 18 q-8 -8 0 -18z" fill="#FFB627" stroke="{ORANGE}" stroke-width="1.2"/>')

    def stern(self, x, y, r):
        self.glow(x, y, r * 2.4)
        pts = [(x + (r if i % 2 == 0 else r * .45) * math.sin(i * math.pi / 5), y - (r if i % 2 == 0 else r * .45) * math.cos(i * math.pi / 5)) for i in range(10)]
        return self.poly(pts, "#FFD34D", 1)

    def ball(self, x, y, r, stiel=False):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#D2553A"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#{self.pre}ball)"/>')
        if stiel:
            self.add(f'<path d="M{x} {y - r} q4 -12 14 -14" fill="none" stroke="#4B7A2B" stroke-width="2.5" stroke-linecap="round"/>')
        return self

    def auge(self, x, y, blick=-1, s=1.0):
        w, h = 24 * s, 15 * s
        return self.add(f'<path d="M{x - w:.1f} {y} Q{x} {y - h * 1.5:.1f} {x + w:.1f} {y} Q{x} {y + h * 1.5:.1f} {x - w:.1f} {y}Z" fill="#FFFFFF" stroke="#66798E" stroke-width="1.5"/>'
                        f'<circle cx="{x + blick * 8 * s:.1f}" cy="{y}" r="{9 * s:.1f}" fill="#3B7CC4"/><circle cx="{x + blick * 9 * s:.1f}" cy="{y}" r="{4.2 * s:.1f}" fill="#05080F"/>')

    def deckenlampe(self, x, y, top=0):
        self.line(x, top, x, y - 16, "#66798E", 1.6)
        self.add(f'<path d="M{x - 16} {y - 4} h32 l-7 -12 h-18z" fill="#9FB2CF"/>')
        return self.lampe(x, y, r=7)

    def formel(self, x, y, zeichen, index="", anchor="start", col=INK):
        i = f'<tspan font-size="9" dy="3.5" font-style="normal">{index}</tspan>' if index else ""
        return self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Georgia, \'Times New Roman\', serif" font-style="italic" font-size="14" '
                        f'fill="{col}" text-anchor="{anchor}" paint-order="stroke" stroke="#FFFFFF" stroke-width="3">{zeichen}{i}</text>')

    def svg(self, w=636): return f'<svg viewBox="0 0 {w} {self.h}" xmlns="http://www.w3.org/2000/svg">' + "".join(self.o) + "</svg>"


def gerade(L, P, x):
    """y-Wert der Geraden durch L und P an der Stelle x."""
    return L[1] + (P[1] - L[1]) * (x - L[0]) / (P[0] - L[0])


# ---------------------------------------------------------------- Leitfrage 3
def beobachte_mauer():
    z = Z("bm", 245)
    z.rect(20, 192, 596, 2, "#C6D1E1")
    z.rect(300, 22, 150, 170, WAND, 1, 3)
    for y in range(44, 192, 22):
        z.rect(300, y, 150, 2, "#3B4A63")
    z.ball(510, 170, 22)
    # Person
    z.add('<circle cx="130" cy="96" r="15" fill="#C9B6A0"/><rect x="118" y="112" width="24" height="46" rx="6" fill="#3B4A63"/>'
          '<line x1="124" y1="158" x2="118" y2="190" stroke="#3B4A63" stroke-width="7" stroke-linecap="round"/>'
          '<line x1="136" y1="158" x2="142" y2="190" stroke="#3B4A63" stroke-width="7" stroke-linecap="round"/>')
    z.line(146, 94, 296, 94, "#66798E", 1.6, "5 5").line(146, 94, 296, 148, "#66798E", 1.6, "5 5")
    z.text(375, 14, "Mauer", "middle").text(510, 214, "Ball", "middle").text(130, 214, "Beobachter", "middle").text(170, 84, "Blickrichtung")
    return z.svg()


def ausbreitung():
    z = Z("ab")
    L, X, S0, S1, R = (60, 106), 324, 91, 121, 616
    z.poly([L, (X, 8), (X, 204)], "#FFC53D", .16)
    for ang in (135, 180, 225, 90, 270):
        a = math.radians(ang)
        z.line(L[0], L[1], L[0] + 44 * math.cos(a), L[1] - 44 * math.sin(a))
    for y in (14, 46, 78, 134, 166, 198):
        z.line(L[0], L[1], X, y)
    yT, yB = gerade(L, (X, S0), R), gerade(L, (X, S1), R)
    z.poly([(X, S0), (R, yT), (R, yB), (X, S1)], "#FFC53D", .3)
    z.line(L[0], L[1], R, yT).line(L[0], L[1], R, yB).line(L[0], L[1], R, L[1])
    z.rect(X, 8, 10, S0 - 8, WAND).rect(X, S1, 10, 204 - S1, WAND)
    z.lampe(*L)
    z.text(24, 140, "Lichtquelle").text(120, 30, "divergentes Lichtbündel")
    z.text(344, 198, "Blende").text(352, 170, "Spalt").line(350, 164, 334, 112, "#66798E", 1.2)
    z.text(440, 62, "nahezu paralleles").text(440, 76, "Lichtbündel")
    return z.svg()


def modell():
    z = Z("mo")
    z.text(60, 30, "Wirklichkeit: Lichtbündel", weight=600).text(368, 30, "Modell: Lichtstrahlen", weight=600)
    z.poly([(60, 94), (268, 74), (268, 138), (60, 118)], "#FFC53D", .45)
    z.line(60, 94, 268, 74, GELB, 1.6).line(60, 118, 268, 138, GELB, 1.6)
    z.lampe(52, 106)
    z.pfeil(286, 106, 342, 106, "#66798E", 2).text(314, 96, "Modell", "middle", 9.5)
    for y in (72, 106, 140):
        z.pfeil(368, 106 + (y - 106) * 0.0, 600, y)
    z.lampe(360, 106)
    z.text(404, 178, "Ein Lichtstrahl hat keine Breite.", size=9.5).text(404, 192, "Er zeigt nur die Richtung des Lichts.", size=9.5)
    return z.svg()


# ---------------------------------------------------------------- Leitfrage 4
def schatten_panel(z, lampen, OX, OT, OB, SX, top=24, bot=188):
    """Körper bei OX (Mitte), Schirm bei SX. lampen = [(L, farbe)]. Zeichnet Schatten exakt."""
    ys = [(gerade(L, (OX, OT), SX), gerade(L, (OX, OB), SX)) for L, _ in lampen]
    z.wash(lampen[0][0][0], top, SX - lampen[0][0][0], bot - top)
    if len(lampen) == 1:
        a, b = ys[0]
        z.poly([(OX, OT), (SX, a), (SX, b), (OX, OB)], "#05080F", .22)
        z.rect(SX, a, 12, b - a, "#05080F", KERN)
        for (L, c) in lampen:
            z.line(*L, SX, a, c).line(*L, SX, b, c)
    else:
        (a1, b1), (a2, b2) = ys
        k0, k1 = max(a1, a2), min(b1, b2)
        z.poly([(OX, OT), (SX, min(a1, a2)), (SX, k0)], "#05080F", HALB)
        z.poly([(OX, OB), (SX, max(b1, b2)), (SX, k1)], "#05080F", HALB)
        z.poly([(OX, OT), (SX, k0), (SX, k1), (OX, OB)], "#05080F", KERN)
        for (L, c), (a, b) in zip(lampen, ys):
            z.line(*L, SX, a, c).line(*L, SX, b, c)
    z.rect(OX - 6, OT, 12, OB - OT, KOERPER, 1, 2)
    z.rect(SX, top - 8, 12, bot - top + 16, SCHIRM)
    if len(lampen) == 1:
        a, b = ys[0]
        z.rect(SX, a, 12, b - a, "#05080F", KERN)
    else:
        z.rect(SX, min(a1, a2), 12, k0 - min(a1, a2), "#05080F", HALB).rect(SX, k1, 12, max(b1, b2) - k1, "#05080F", HALB)
        z.rect(SX, k0, 12, k1 - k0, "#05080F", KERN)
    for L, c in lampen:
        z.lampe(*L, ring=c)
    return ys


def beobachte_lampen():
    z = Z("bl", 245)
    schatten_panel(z, [((58, 100), GELB)], 155, 76, 124, 268)
    z.line(318, 12, 318, 200, "#A3B7D3", 1, "5 4")
    schatten_panel(z, [((376, 84), ORANGE), ((376, 118), CYAN)], 475, 76, 124, 588)
    z.text(163, 220, "eine Lampe", "middle", weight=600).text(482, 220, "zwei Lampen", "middle", weight=600)
    return z.svg()


def schattenraum():
    z = Z("sr")
    L, OX, OT, OB, SX = (60, 106), 250, 78, 134, 520
    (a, b), = schatten_panel(z, [(L, GELB)], OX, OT, OB, SX, 10, 202)
    for y in (18, 196):
        z.line(*L, SX, y)
    z.text(24, 136, "Lichtquelle").text(OX, OB + 20, "Körper", "middle").text(390, 110, "Schattenraum", "middle")
    z.text(SX + 20, (a + b) / 2 + 4, "Schattenbild").text(SX + 6, 206, "Schirm", "middle")
    return z.svg()


def kern_halbschatten():
    z = Z("kh")
    L1, L2, OX, OT, OB, SX = (60, 84), (60, 132), 290, 78, 134, 505
    ((a1, b1), (a2, b2)) = schatten_panel(z, [(L1, ORANGE), (L2, CYAN)], OX, OT, OB, SX, 12, 200)
    z.formel(32, L1[1] + 5, "L", "1").formel(32, L2[1] + 5, "L", "2")
    z.text(OX, OB + 20, "undurchsichtiger Körper", "middle")
    z.text(SX + 22, (a2 + a1) / 2 + 4, "Halbschatten").text(SX + 22, (a1 + b2) / 2 + 4, "Kernschatten").text(SX + 22, (b2 + b1) / 2 + 4, "Halbschatten")
    return z.svg()



# ---------------------------------------------------------------- Einstieg, Leitfrage 1 und 2
def einstieg_baelle():
    z = Z("eb", 245)
    z.add('<defs><radialGradient id="ebgrau" cx=".35" cy=".35" r=".75"><stop offset="0" stop-color="#DDE5F0"/><stop offset="1" stop-color="#66798E"/></radialGradient></defs>')
    z.rect(100, 210, 440, 3, "#C6D1E1")
    for x in (200, 440):
        z.line(x, 96, x, 200, "#9AAAC0", 1.6, "4 5")
        z.pfeil(x, 172, x, 198, "#9AAAC0", 1.6, 7)
    z.add('<circle cx="200" cy="62" r="28" fill="#A9B6C8"/><circle cx="200" cy="62" r="28" fill="url(#ebgrau)"/>')
    z.ball(440, 62, 15)
    z.text(200, 22, "schwerer", "middle", weight=600).text(440, 22, "leichter", "middle", weight=600)
    z.text(320, 236, "Kommen sie gleichzeitig an?", "middle", 11, 600)
    return z.svg()


def beobachte_licht_an():
    z = Z("la", 245)
    z.rect(40, 30, 250, 160, "#0A1120", 1, 8)
    z.add('<circle cx="165" cy="130" r="30" fill="#141C28" stroke="#27344A" stroke-width="2"/>')
    z.text(165, 136, "?", "middle", 14, 600, "#9AAAC0", "#0A1120")
    z.line(165, 30, 165, 58, "#27344A", 1.6)
    z.add('<circle cx="165" cy="66" r="7" fill="#1D283A" stroke="#4D5E77" stroke-width="2"/>')
    z.rect(346, 30, 250, 160, "#FFFBEF", 1, 8).add('<rect x="346" y="30" width="250" height="160" rx="8" fill="none" stroke="#C6D1E1"/>')
    for dx in (-22, 0, 22):
        z.pfeil(471, 74, 471 + dx * 0.9, 98, GELB, 2, 7)
    for (x2, y2) in ((392, 118), (550, 118), (400, 176), (544, 176)):
        z.line(471 + (x2 - 471) * .42, 130 + (y2 - 130) * .42, x2, y2, GELB, 1.4, op=.55)
    z.ball(471, 130, 30, stiel=True)
    z.deckenlampe(471, 66, 30)
    z.text(165, 214, "Licht aus", "middle", weight=600).text(471, 214, "Licht an", "middle", weight=600)
    return z.svg()


def wie_sehen():
    z = Z("ws")
    L, A, E = (70, 58), (278, 146), (520, 100)
    z.deckenlampe(*L, 0)
    for dy in (-24, 0, 24):
        z.pfeil(L[0] + 6, L[1] + 6, A[0] - 26, A[1] + dy * .6 - 8, GELB, 2)
    for (x2, y2) in ((330, 70), (380, 196), (250, 202), (200, 186)):
        z.line(A[0], A[1], x2, y2, GELB, 1.4, op=.5)
    z.ball(*A, 28, stiel=True)
    z.pfeil(A[0] + 28, A[1] - 8, E[0] - 30, E[1] + 2, GELB, 2.6)
    z.auge(*E, -1, 1.05)
    z.text(96, 62, "Lichtquelle (Sender)").text(A[0], 196, "Gegenstand", "middle").text(E[0], 140, "Auge (Empfänger)", "middle")
    z.text(120, 118, "1. Licht trifft den Gegenstand", size=9.5).text(330, 104, "2. Licht wird zurückgeworfen", size=9.5)
    return z.svg()


def lichtquellen_beleuchtet():
    z = Z("lb")
    z.line(318, 16, 318, 196, "#A3B7D3", 1.2, "6 4")
    z.text(159, 26, "Lichtquellen", "middle", weight=600).text(477, 26, "beleuchtete Körper", "middle", weight=600)
    z.sonne(70, 82, 16).kerze(161, 92).gluehlampe(248, 80)
    z.add('<path d="M392 58 a28 28 0 1 0 0 52 a22 22 0 1 1 0 -52 z" fill="#DDE3EC" stroke="#9AAAC0"/>')
    z.add('<path d="M452 64 h32 v44 h-32 z M484 64 h32 v44 h-32 z" fill="#FFFFFF" stroke="#66798E"/>')
    z.add('<rect x="576" y="92" width="9" height="24" rx="1" fill="#8B5A2B"/><circle cx="580.5" cy="82" r="21" fill="#5E9B45"/>')
    for x, t in ((70, "Sonne"), (161, "Kerze"), (248, "Glühlampe"), (392, "Mond"), (484, "Buch"), (580, "Baum")):
        z.text(x, 142, t, "middle", 9.5)
    z.text(159, 176, "senden selbst Licht aus", "middle", 9.5).text(477, 176, "werfen fremdes Licht zurück", "middle", 9.5)
    return z.svg()


def beobachte_drei_koerper():
    z = Z("dk", 245)
    L = (318, 44)
    for cx in (120, 318, 516):
        z.pfeil(L[0], L[1] + 8, cx, 108, GELB, 2.2)
    z.deckenlampe(*L, 6)
    z.rect(80, 112, 80, 60, "#FFFFFF", 1, 2).add('<rect x="80" y="112" width="80" height="60" rx="2" fill="none" stroke="#9AAAC0"/>')
    z.rect(278, 112, 80, 60, "#15171C", 1, 2)
    z.rect(476, 112, 80, 60, "#9FD4F2", .35, 2).add('<rect x="476" y="112" width="80" height="60" rx="2" fill="none" stroke="#6E9BB8"/>')
    z.text(120, 196, "weißes Blatt", "middle").text(318, 196, "schwarzer Karton", "middle").text(516, 196, "Glasscheibe", "middle")
    return z.svg()


def vier_moeglichkeiten():
    z = Z("vm")
    for x in (159, 318, 477):
        z.line(x, 16, x, 180, "#A3B7D3", 1, "5 4")
    # Emission
    z.glow(80, 88, 40)
    for k in range(8):
        a = math.radians(k * 45)
        z.pfeil(80 + 20 * math.cos(a), 88 + 20 * math.sin(a), 80 + 42 * math.cos(a), 88 + 42 * math.sin(a), GELB, 2, 6)
    z.add(f'<circle cx="80" cy="88" r="14" fill="#FFF3C4" stroke="{GELB}" stroke-width="2.5"/>')
    # Streuung
    z.pfeil(172, 62, 213, 86, GELB, 2.2)
    for ang in (140, 165, 190, 215):
        a = math.radians(ang)
        z.pfeil(214, 88, 214 + 40 * math.cos(a), 88 + 40 * math.sin(a), GELB, 1.8, 6)
    z.rect(216, 56, 14, 64, "#FFFFFF", 1, 2).add('<rect x="216" y="56" width="14" height="64" rx="2" fill="none" stroke="#9AAAC0"/>')
    # Absorption
    z.pfeil(332, 70, 371, 80, GELB, 2.2).pfeil(332, 104, 371, 98, GELB, 2.2)
    z.add('<circle cx="382" cy="89" r="24" fill="#FF7A59" fill-opacity=".18"/>')
    for dx in (-8, 0, 8):
        z.add(f'<path d="M{382 + dx} 50 q5 -7 0 -14 q-5 -7 0 -14" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-linecap="round"/>')
    z.rect(374, 56, 16, 66, "#15171C", 1, 2)
    # Transmission
    z.pfeil(494, 76, 608, 76, GELB, 2.2).pfeil(494, 104, 608, 104, GELB, 2.2)
    z.rect(532, 52, 13, 76, "#9FD4F2", .35, 2).add('<rect x="532" y="52" width="13" height="76" rx="2" fill="none" stroke="#6E9BB8"/>')
    for x, t, u in ((80, "Emission", "Körper sendet Licht aus"), (238, "Streuung", "Licht wird zurückgeworfen"),
                    (398, "Absorption", "Licht wird verschluckt"), (556, "Transmission", "Licht geht hindurch")):
        z.text(x, 162, t, "middle", 11, 600).text(x, 180, u, "middle", 9)
    return z.svg()


def lichtquellen_arten():
    """Neue Folie 'Natürliche und künstliche Lichtquellen' (in baue_folien_am_stueck.py)."""
    z = Z("na")
    z.line(318, 10, 318, 200, "#A3B7D3", 1.2, "5 5")
    z.text(159, 24, "natürliche Lichtquellen", "middle", weight=600).text(477, 24, "künstliche Lichtquellen", "middle", weight=600)
    z.sonne(48, 84, 13)
    z.glow(126, 88, 26).poly([(132, 64), (118, 90), (127, 90), (120, 112), (140, 82), (130, 82)], "#FFD34D", 1)
    z.stern(196, 78, 9).stern(214, 98, 7)
    z.glow(282, 90, 18).add('<ellipse cx="270" cy="88" rx="10" ry="5" fill="#4B7A2B"/><circle cx="282" cy="90" r="7" fill="#F3FF8A"/>')
    z.gluehlampe(372, 84).kerze(444, 84).gluehlampe(516, 84, "#EAF6FF", CYAN)
    z.add('<circle cx="597" cy="85" r="30" fill="#6FB1E8" fill-opacity=".18"/><rect x="574" y="70" width="46" height="30" rx="2" fill="#26324A"/>'
          '<rect x="578" y="74" width="38" height="22" fill="#6FB1E8"/><line x1="597" y1="100" x2="597" y2="108" stroke="#26324A" stroke-width="3"/>')
    for x, t in ((48, "Sonne"), (126, "Blitz"), (205, "Sterne"), (276, "Glühwürmchen"), (372, "Glühlampe"), (444, "Kerze"), (516, "LED-Lampe"), (597, "Bildschirm")):
        z.text(x, 136, t, "middle", 9.5)
    z.text(159, 176, "gibt es in der Natur", "middle", 9.5).text(477, 176, "hat der Mensch gebaut", "middle", 9.5)
    return z.svg()


# ---------------------------------------------------------------- Leitfrage 5 und Lochkamera
HELL, DUNKEL, ERDE = "#FFF6D8", "#3B4A63", "#3B7CC4"


def phase_pfad(x, y, r, f):
    """Beleuchteter Teil des Mondes, von der Erde (Nordhalbkugel) aus gesehen. f = Anteil am Umlauf (0 Neumond, 0.25 zunehmender Halbmond, 0.5 Vollmond)."""
    f %= 1
    if f < 0.005 or f > 0.995:
        return ""
    k = math.cos(2 * math.pi * f)
    rechts = f < 0.5
    rx = abs(k) * r
    s1 = 1 if rechts else 0
    if k > 0:   # Sichel: Ellipse schneidet in die helle Seite
        s2 = 0 if rechts else 1
    else:       # Dreiviertel: Ellipse wölbt sich in die dunkle Seite
        s2 = 1 if rechts else 0
    return (f'<path d="M{x:.1f} {y - r:.1f} A{r:.1f} {r:.1f} 0 0 {s1} {x:.1f} {y + r:.1f} '
            f'A{max(rx, .01):.1f} {r:.1f} 0 0 {s2} {x:.1f} {y - r:.1f}Z" fill="{HELL}"/>')


def mond_ansicht(z, x, y, r, f):
    z.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{DUNKEL}"/>' + phase_pfad(x, y, r, f))
    return z.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#9AAAC0" stroke-width="1"/>')


def mond_von_oben(z, x, y, r, licht_links=True):
    """Mond in der Draufsicht: die zur Sonne gewandte Hälfte ist hell."""
    s = 0 if licht_links else 1
    return z.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{DUNKEL}"/>'
                 f'<path d="M{x} {y - r} A{r} {r} 0 0 {s} {x} {y + r}Z" fill="{HELL}"/>'
                 f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#9AAAC0" stroke-width="1"/>')


def erde(z, x, y, r, nacht_rechts=True):
    z.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{ERDE}"/>')
    s = 1 if nacht_rechts else 0
    return z.add(f'<path d="M{x} {y - r} A{r} {r} 0 0 {s} {x} {y + r}Z" fill="#05080F" fill-opacity=".35"/>')


def beobachte_mond():
    z = Z("bo", 245)
    z.rect(40, 22, 556, 156, "#0A1120", 1, 10)
    for sx, sy in ((90, 48), (200, 40), (330, 52), (470, 38), (556, 60), (150, 150), (410, 156), (270, 148)):
        z.add(f'<circle cx="{sx}" cy="{sy}" r="1.5" fill="#FFFFFF" fill-opacity=".7"/>')
    for i, f in enumerate((0.0, 0.25, 0.5, 0.75)):
        x = 112 + i * 142
        mond_ansicht(z, x, 100, 28, f)
        z.text(x, 204, f"{i + 1}. Woche", "middle")
    return z.svg()


def mondbahn():
    z = Z("mb")
    E, R = (330, 106), 78
    for y in (26, 66, 106, 146, 186):
        z.pfeil(14, y, 118, y, GELB, 2, 8)
    z.text(14, 14, "Sonnenlicht")
    z.add(f'<circle cx="{E[0]}" cy="{E[1]}" r="{R}" fill="none" stroke="#9AAAC0" stroke-width="1.2" stroke-dasharray="5 4"/>')
    erde(z, *E, 20)
    for (dx, dy) in ((-R, 0), (0, R), (R, 0), (0, -R)):
        mond_von_oben(z, E[0] + dx, E[1] + dy, 11)
    # Umlauf gegen den Uhrzeigersinn (Blick von oben): links -> unten -> rechts -> oben
    a1, a2, RR = math.radians(62), math.radians(24), R + 18
    z.add(f'<path d="M{E[0] + RR * math.cos(a1):.1f} {E[1] + RR * math.sin(a1):.1f} A{RR} {RR} 0 0 0 {E[0] + RR * math.cos(a2):.1f} {E[1] + RR * math.sin(a2):.1f}" fill="none" stroke="#66798E" stroke-width="1.6"/>')
    ex, ey = E[0] + RR * math.cos(a2), E[1] + RR * math.sin(a2)
    z.poly([(ex + 3, ey - 9), (ex - 5, ey + 1), (ex + 6, ey + 2)], "#66798E", 1)
    z.text(E[0] + 104, E[1] + 76, "Umlauf")
    z.text(E[0], E[1] + 4, "Erde", "middle", 9, col="#FFFFFF", halo=ERDE)
    z.text(E[0] - R - 16, E[1] + 30, "Neumond", "end")
    z.text(E[0] + 18, E[1] + R + 16, "zunehmender Mond")
    z.text(E[0] + R + 18, E[1] + 4, "Vollmond")
    z.text(E[0] + 18, E[1] - R - 4, "abnehmender Mond")
    z.text(622, 204, "Blick von oben auf den Nordpol", "end", 9)
    return z.svg()


def mondphasen():
    z = Z("mp")
    namen = (("Neumond", ""), ("zunehmender", "Halbmond"), ("Vollmond", ""), ("abnehmender", "Halbmond"))
    for i, f in enumerate((0.0, 0.25, 0.5, 0.75)):
        x = 80 + i * 142
        mond_ansicht(z, x, 84, 34, f)
        z.text(x, 144, namen[i][0], "middle")
        if namen[i][1]:
            z.text(x, 158, namen[i][1], "middle")
    z.pfeil(46, 184, 598, 184, "#66798E", 1.6, 9)
    z.text(322, 202, "etwa 29,5 Tage", "middle", 10)
    return z.svg()


def tangenten(S, rs, K, rk):
    """Randstrahlen für Kern- und Halbschatten (Näherung über oberste und unterste Punkte)."""
    kern = ((S[0], S[1] - rs), (K[0], K[1] - rk)), ((S[0], S[1] + rs), (K[0], K[1] + rk))
    halb = ((S[0], S[1] - rs), (K[0], K[1] + rk)), ((S[0], S[1] + rs), (K[0], K[1] - rk))
    return kern, halb


def sonnenfinsternis():
    z = Z("sf")
    S, M, E = (40, 106), (360, 106), (560, 106)
    rs, rm, re_ = 40, 14, 34
    (k1, k2), (h1, h2) = tangenten(S, rs, M, rm)
    apex_x = S[0] + (S[1] - rs - (S[1])) / ((k1[1][1] - k1[0][1]) / (k1[1][0] - k1[0][0])) * -1
    ax = k1[0][0] + (S[1] - k1[0][1]) * (k1[1][0] - k1[0][0]) / (k1[1][1] - k1[0][1])
    X = E[0] - re_ + 6
    yh1, yh2 = gerade(h1[0], h1[1], X), gerade(h2[0], h2[1], X)
    z.poly([(M[0], M[1] - rm), (X, yh2), (X, yh1), (M[0], M[1] + rm)], "#05080F", HALB)
    z.poly([(M[0], M[1] - rm), (ax, S[1]), (M[0], M[1] + rm)], "#05080F", KERN)
    for a, b in (k1, k2):
        z.line(*a, ax, S[1], GELB, 1.8)
    for a, b in (h1, h2):
        z.line(*a, X, gerade(a, b, X), GELB, 1.8)
    z.add(f'<circle cx="{S[0]}" cy="{S[1]}" r="{rs * 1.6}" fill="url(#sfgl)"/><circle cx="{S[0]}" cy="{S[1]}" r="{rs}" fill="#FFD34D"/>')
    z.add(f'<circle cx="{M[0]}" cy="{M[1]}" r="{rm}" fill="#9AAAC0"/>')
    erde(z, *E, re_, nacht_rechts=True)
    z.add(f'<circle cx="{E[0] - re_ + 3}" cy="{E[1]}" r="3.5" fill="#05080F"/>')
    z.text(S[0], 170, "Sonne", "middle").text(M[0], 142, "Mond", "middle").text(E[0], 164, "Erde", "middle")
    z.text(400, 86, "Kernschatten").text(410, 180, "Halbschatten").line(450, 172, 480, 140, "#66798E", 1.2)
    z.text(622, 204, "nicht maßstabsgetreu", "end", 9)
    return z.svg()


def mondfinsternis():
    z = Z("mf")
    S, E, M = (40, 106), (330, 106), (520, 106)
    rs, re_, rm = 40, 26, 11
    (k1, k2), (h1, h2) = tangenten(S, rs, E, re_)
    X = 610
    yk1, yk2 = gerade(*k1, X), gerade(*k2, X)
    yh1, yh2 = gerade(*h1, X), gerade(*h2, X)
    z.poly([(E[0], E[1] - re_), (X, yh2), (X, yh1), (E[0], E[1] + re_)], "#05080F", HALB)
    z.poly([(E[0], E[1] - re_), (X, yk1), (X, yk2), (E[0], E[1] + re_)], "#05080F", KERN)
    for a, b in (k1, k2):
        z.line(*a, X, gerade(a, b, X), GELB, 1.8)
    z.add(f'<circle cx="{S[0]}" cy="{S[1]}" r="{rs * 1.6}" fill="url(#mfgl)"/><circle cx="{S[0]}" cy="{S[1]}" r="{rs}" fill="#FFD34D"/>')
    erde(z, *E, re_, nacht_rechts=True)
    z.add(f'<circle cx="{M[0]}" cy="{M[1]}" r="{rm}" fill="#8A4A3A"/>')
    z.text(S[0], 170, "Sonne", "middle").text(E[0], 156, "Erde", "middle").text(M[0], 140, "Mond", "middle")
    z.text(400, 66, "Kernschatten der Erde").line(446, 72, 456, 96, "#66798E", 1.2)
    z.text(622, 204, "nicht maßstabsgetreu", "end", 9)
    return z.svg()


def lochkamera():
    z = Z("lk")
    A, LX, SX = 106, 300, 480
    top, fuss = (62, 58), (62, 152)
    z.line(40, A, 500, A, "#9AAAC0", 1, "4 4")
    z.wash(40, 14, LX - 40, 184)
    for P, c in ((top, ORANGE), (fuss, CYAN)):
        y = gerade(P, (LX + 4, A), SX)
        z.line(*P, SX, y, c, 2.2)
    yt, yf = gerade(top, (LX + 4, A), SX), gerade(fuss, (LX + 4, A), SX)
    z.rect(LX, 14, 9, A - 4 - 14, WAND).rect(LX, A + 4, 9, 198 - A - 4, WAND)
    z.rect(SX, 14, 12, 186, SCHIRM)
    # Kerze
    z.glow(62, 76, 30)
    z.add('<rect x="52" y="96" width="20" height="56" rx="2" fill="#F5E6C8" stroke="#C6B48E"/>'
          f'<path d="M62 96 q-13 -18 0 -38 q13 20 0 38z" fill="#FFB627" stroke="{ORANGE}" stroke-width="1.2"/>')
    # Bild (umgekehrt, maßstäblich)
    h = (yt - yf)
    sk = h / (152 - 58)
    by0 = yf
    z.add(f'<g transform="translate({SX + 6:.1f} {yt:.1f}) scale({sk:.3f} {-sk:.3f}) translate(-62 -58)">'
          '<rect x="52" y="96" width="20" height="56" rx="2" fill="#F5E6C8" stroke="#C6B48E"/>'
          f'<path d="M62 96 q-13 -18 0 -38 q13 20 0 38z" fill="#FFB627" stroke="{ORANGE}" stroke-width="1.2"/></g>')
    z.text(62, 176, "Gegenstand", "middle").text(LX + 4, 10, "Lochblende", "middle").text(SX + 6, 212, "Schirm", "middle")
    z.text(SX + 24, (yt + yf) / 2 - 4, "Bild").text(SX + 24, (yt + yf) / 2 + 10, "(umgekehrt)")
    z.text(110, 40, "Spitze oben").text(330, 172, "trifft unten auf").text(330, 186, "den Schirm")
    return z.svg()


def sicheln():
    z = Z("si")
    z.text(24, 30, "Bei einer Sonnenfinsternis sind die Lichtflecken unter einem Baum", size=11.5)
    z.text(24, 48, "nicht rund, sondern kleine Sicheln. Warum?", size=11.5)
    z.add('<rect x="300" y="146" width="12" height="46" rx="1" fill="#8B5A2B"/><circle cx="306" cy="120" r="40" fill="#5E9B45"/>')
    for gx, gy in ((290, 108), (320, 126), (300, 136)):
        z.add(f'<circle cx="{gx}" cy="{gy}" r="3" fill="#FFF6D8"/>')
    z.rect(60, 194, 516, 3, "#C8A57A")
    for x in (150, 220, 400, 470):
        z.glow(x, 186, 16)
        z.add(f'<path transform="rotate(180 {x} 184)" d="M{x} {192} a9 9 0 1 0 0 -16 a7 7 0 1 1 0 16z" fill="#FFD34D" stroke="{GELB}" stroke-width=".8"/>')
    z.glow(560, 70, 30)
    z.add(f'<path d="M560 52 a18 18 0 1 0 0 36 a14 14 0 1 1 0 -36z" fill="#FFD34D" stroke="{GELB}" stroke-width="1.2"/>')
    z.text(560, 108, "Sonne", "middle", 9).text(560, 120, "(Finsternis)", "middle", 9)
    z.text(185, 172, "Lichtflecken auf dem Boden", "middle", 9.5)
    return z.svg()


ZEICHNUNGEN = {1: einstieg_baelle, 6: beobachte_licht_an, 9: wie_sehen, 11: lichtquellen_beleuchtet, 15: beobachte_drei_koerper, 18: vier_moeglichkeiten,
               22: beobachte_mauer, 25: ausbreitung, 27: modell, 31: beobachte_lampen, 34: schattenraum, 36: kern_halbschatten,
               42: beobachte_mond, 45: mondbahn, 47: mondphasen, 49: sonnenfinsternis, 51: mondfinsternis, 56: lochkamera, 61: sicheln}

if __name__ == "__main__":
    p = HIER / "Optik I.html"
    s = p.read_text(encoding="utf-8")
    teile = re.split(r'(<section class="folie[^"]*">.*?</section>)', s, flags=re.S)
    idx = [i for i, t in enumerate(teile) if t.startswith('<section class="folie')]
    for seite, fn in ZEICHNUNGEN.items():
        i = idx[seite - 1]
        teile[i] = re.sub(r"<svg.*?</svg>", lambda m: fn(), teile[i], count=1, flags=re.S)
    p.write_text("".join(teile), encoding="utf-8")
    print("ersetzt:", ", ".join(f"S. {k}" for k in ZEICHNUNGEN))
