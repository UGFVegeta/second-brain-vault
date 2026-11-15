"""Lösung Schnittpunkt 10, S. 15 A und B, S. 16 Nr. 3 rechts, S. 16 Nr. 5 links (für Schnelle).
Rechnet alle Werte mit Asserts nach und baut HTML + PDF (eine A4-Seite).
Schreibweise wie Oskars Handlösung zu S. 15 Nr. 2: nummerierte Schritte, gesuchte Größe als Überschrift,
Gleichung mit Umformung rechts (| ·9,0), Ergebnis mit Einheit. Rechter Winkel = Viertelkreis mit Punkt.
Ausführen: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 baue_loesung_s15_s16.py
"""
import math
import re
import subprocess
from pathlib import Path

HIER = Path(__file__).parent
NAME = "Mathe 10b – Lösung Buch S. 15 A, B und S. 16 Nr. 3, 5"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROT = "#c2185b"

S = lambda d: math.sin(math.radians(d))
C = lambda d: math.cos(math.radians(d))
aS = lambda x: math.degrees(math.asin(x))
r2 = lambda x: round(x + 1e-9, 2)
r1 = lambda x: round(x + 1e-9, 1)


def k(x, n=2):
    """Zahl mit Komma."""
    return f"{x:.{n}f}".replace(".", ",")


# ---------------------------------------------------------------- Rechnung (gerundete Zwischenwerte wie im Heft)
R = {}
# S. 15 A: α = 40,3°, β = 63,5°, c = 9,0 cm; gesucht γ, a
g = r1(180 - 40.3 - 63.5); hb = r2(9.0 * S(40.3)); a = r2(hb / S(g))
assert (g, hb) == (76.2, 5.82) and r1(a) == 6.0          # Buch: γ = 76,2°; h_b = 5,82; a = 6,0
R["A"] = dict(g=g, hb=hb, a=a)
# S. 15 B: b = 7,5 cm, c = 6,0 cm, α = 48,4°; gesucht A, a
hc = r2(7.5 * S(48.4)); c1 = r2(7.5 * C(48.4)); c2 = r2(6.0 - c1); a = r2(math.sqrt(hc**2 + c2**2)); A = r2(0.5 * 6.0 * hc)
assert (hc, c1, c2) == (5.61, 4.98, 1.02) and r1(a) == 5.7 and r1(A) == 16.8   # Buch: 16,8 cm²; 5,7 cm
R["B"] = dict(hc=hc, c1=c1, c2=c2, a=a, A=A)
# S. 16 Nr. 3 a: c = 6,4 cm, a = 5,3 cm, γ = 62,8°; gesucht b, α, β
hb = r2(5.3 * S(62.8)); b2 = r2(5.3 * C(62.8)); b1 = r2(math.sqrt(6.4**2 - hb**2)); b = r2(b1 + b2)
q = round(hb / 6.4, 4); al = r1(aS(q)); be = r1(180 - al - 62.8)
assert (hb, b2, b1) == (4.71, 2.42, 4.33) and r1(b) == 6.8 and (al, be) == (47.4, 69.8)  # Buch
R["3a"] = dict(hb=hb, b2=b2, b1=b1, b=b, q=q, al=al, be=be)
# S. 16 Nr. 3 b: b = 5,8 cm (Schülerbuch; Buchlösung rechnet mit 5,4), c = 7,4 cm, γ = 72,4°; gesucht a, α, β
ha = r2(5.8 * S(72.4)); a2 = r2(5.8 * C(72.4)); a1 = r2(math.sqrt(7.4**2 - ha**2)); a = r2(a1 + a2)
q = round(ha / 7.4, 4); be = r1(aS(q)); al = r1(180 - be - 72.4)
assert (ha, a2, a1, a, be, al) == (5.53, 1.75, 4.92, 6.67, 48.4, 59.2)
# Gegenprobe mit den Werten der Buchlösung (b = 5,4): h_a 5,15; a 6,94; β 44,1°; α 63,5°
_ha = r2(5.4 * S(72.4)); _a = r2(r2(math.sqrt(7.4**2 - _ha**2)) + r2(5.4 * C(72.4)))
assert (_ha, _a, r1(aS(_ha / 7.4))) == (5.15, 6.94, 44.1)
R["3b"] = dict(ha=ha, a2=a2, a1=a1, a=a, q=q, be=be, al=al)
# S. 16 Nr. 3 c: b = 4,4 cm, a = 8,4 cm, α = 115°; gesucht c, β
al2 = 180 - 115; hc = r2(4.4 * S(al2)); cx = r2(math.sqrt(8.4**2 - hc**2)); x = r2(4.4 * C(al2)); c = r2(cx - x)
q = round(hc / 8.4, 4); be = r1(aS(q))
assert (al2, hc, cx, x) == (65, 3.99, 7.39, 1.86) and r1(c) == 5.5 and be == 28.4   # Buch: c = 5,53 ≈ 5,5; β = 28,4°
R["3c"] = dict(al2=al2, hc=hc, cx=cx, x=x, c=c, q=q, be=be)
# S. 16 Nr. 5 a: c = 7,5 cm, a = 6,8 cm, β = 36,0°
hc = r2(6.8 * S(36.0)); A1 = r2(0.5 * 7.5 * hc); A2 = r2(0.5 * 6.8 * 7.5 * S(36.0))
assert hc == 4.00 and r1(A1) == r1(A2) == 15.0
R["5a"] = dict(hc=hc, A1=A1, A2=A2)
# S. 16 Nr. 5 b: b = 4,8 cm, a = 4,3 cm, γ = 65,9°
ha = r2(4.8 * S(65.9)); A1 = r2(0.5 * 4.3 * ha); A2 = r2(0.5 * 4.3 * 4.8 * S(65.9))
assert ha == 4.38 and r1(A1) == r1(A2) == 9.4                        # Buch: 9,42 cm²
R["5b"] = dict(ha=ha, A1=A1, A2=A2)


# ---------------------------------------------------------------- Skizzen (SVG in mm)
def dreieck(A, B, C):
    """Koordinaten in cm, A, B, C als (x, y) mit y nach oben."""
    return {"A": A, "B": B, "C": C}


def pkt_aus(c, alpha, b):
    """A = (0,0), B = (c,0), C über Winkel α und Länge b."""
    return dreieck((0, 0), (c, 0), (b * C(alpha), b * S(alpha)))


def fuss(P, Q1, Q2):
    """Lotfußpunkt von P auf die Gerade Q1Q2."""
    dx, dy = Q2[0] - Q1[0], Q2[1] - Q1[1]
    t = ((P[0] - Q1[0]) * dx + (P[1] - Q1[1]) * dy) / (dx * dx + dy * dy)
    F = (Q1[0] + t * dx, Q1[1] + t * dy)
    assert abs((P[0] - F[0]) * dx + (P[1] - F[1]) * dy) < 1e-9   # Senkrechte geprüft (Skalarprodukt 0)
    return F


class Skizze:
    def __init__(self, P, extra=(), breite=48, hoehe=28):
        self.P = dict(P)
        pts = list(self.P.values()) + list(extra)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        self.s = min((breite - 18) / (max(xs) - min(xs)), (hoehe - 10) / (max(ys) - min(ys)))
        self.x0, self.y1 = min(xs), max(ys)
        self.w, self.h = (max(xs) - min(xs)) * self.s + 18, (max(ys) - min(ys)) * self.s + 10
        self.teile = []
        self.mitte = self.m(*[sum(p[i] for p in list(P.values())[:3]) / 3 for i in (0, 1)])

    def m(self, x, y):
        return (9 + (x - self.x0) * self.s, 5 + (self.y1 - y) * self.s)

    def linie(self, p, q, farbe="#222", w=0.45, strich=""):
        (x1, y1), (x2, y2) = self.m(*p), self.m(*q)
        d = f' stroke-dasharray="{strich}"' if strich else ""
        self.teile.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{farbe}" stroke-width="{w}"{d}/>')

    def text(self, x, y, t, farbe="#222", gr=3.1, fett=False):
        f = ' font-weight="700"' if fett else ""
        self.teile.append(f'<text x="{x:.2f}" y="{y + 1.1:.2f}" font-size="{gr}" fill="{farbe}" text-anchor="middle"{f}>{t}</text>')

    def ecke(self, n, dx=0, dy=0):
        x, y = self.m(*self.P[n])
        vx, vy = x - self.mitte[0], y - self.mitte[1]
        L = math.hypot(vx, vy)
        self.text(x + vx / L * 3 + dx, y + vy / L * 3 + dy, n, gr=3.2)

    def seite(self, p, q, t, farbe="#222", ab=2.6, fett=False, aussen=True, pos=0.5):
        (x1, y1), (x2, y2) = self.m(*p), self.m(*q)
        mx, my = x1 + (x2 - x1) * pos, y1 + (y2 - y1) * pos
        nx, ny = -(y2 - y1), x2 - x1
        L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
        if ((mx - self.mitte[0]) * nx + (my - self.mitte[1]) * ny < 0) == aussen:
            nx, ny = -nx, -ny
        breite = len(re.sub("<[^>]+>", "", t)) * 1.7      # Textbreite in mm (grob)
        ab = ab + abs(nx) * breite / 2                      # schräge Seiten: Text weiter weg
        self.text(mx + nx * ab, my + ny * ab, t, farbe, fett=fett)

    def winkel(self, ecke, p, q, t, farbe="#222", r=4.2, rt=7.6, fett=False):
        x, y = self.m(*ecke)
        w1 = math.atan2(self.m(*p)[1] - y, self.m(*p)[0] - x)
        w2 = math.atan2(self.m(*q)[1] - y, self.m(*q)[0] - x)
        d = (w2 - w1) % (2 * math.pi)
        if d > math.pi:
            w1, w2, d = w2, w1, 2 * math.pi - d
        x1, y1 = x + r * math.cos(w1), y + r * math.sin(w1)
        x2, y2 = x + r * math.cos(w1 + d), y + r * math.sin(w1 + d)
        self.teile.append(f'<path d="M{x1:.2f},{y1:.2f} A{r},{r} 0 0 1 {x2:.2f},{y2:.2f}" fill="none" stroke="{farbe}" stroke-width="0.4"/>')
        wm = w1 + d / 2
        self.text(x + rt * math.cos(wm), y + rt * math.sin(wm), t, farbe, gr=2.8, fett=fett)

    def rechter(self, F, p, q, r=2.8):
        """Viertelkreis mit Punkt zwischen den Richtungen F→p und F→q."""
        x, y = self.m(*F)
        w1 = math.atan2(self.m(*p)[1] - y, self.m(*p)[0] - x)
        w2 = math.atan2(self.m(*q)[1] - y, self.m(*q)[0] - x)
        d = (w2 - w1) % (2 * math.pi)
        if d > math.pi:
            w1, d = w2, 2 * math.pi - d
        assert abs(d - math.pi / 2) < 1e-6
        x1, y1 = x + r * math.cos(w1), y + r * math.sin(w1)
        x2, y2 = x + r * math.cos(w1 + d), y + r * math.sin(w1 + d)
        wm = w1 + d / 2
        self.teile.append(f'<path d="M{x1:.2f},{y1:.2f} A{r},{r} 0 0 1 {x2:.2f},{y2:.2f}" fill="none" stroke="#c0392b" stroke-width="0.4"/>'
                          f'<circle cx="{x + r * .48 * math.cos(wm):.2f}" cy="{y + r * .48 * math.sin(wm):.2f}" r="0.42" fill="#c0392b"/>')

    def svg(self):
        A, B, Cc = (self.m(*self.P[n]) for n in "ABC")
        flaeche = (f'<polygon points="{A[0]:.2f},{A[1]:.2f} {B[0]:.2f},{B[1]:.2f} {Cc[0]:.2f},{Cc[1]:.2f}" '
                   f'fill="#eef5e6" stroke="#222" stroke-width="0.5"/>')
        return (f'<svg viewBox="0 0 {self.w:.1f} {self.h:.1f}" width="{self.w:.1f}mm" height="{self.h:.1f}mm" '
                f'font-family="Helvetica, Arial, sans-serif">' + flaeche + "".join(self.teile) + "</svg>")


def sk_A():
    P = pkt_aus(9.0, 40.3, 9.0 * S(63.5) / S(76.2))
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(B, A, Cc)
    s = Skizze(P)
    s.linie(B, F); s.rechter(F, A, B)
    s.linie(B, Cc, ROT, 0.8)
    s.seite(A, B, "9,0 cm"); s.seite(B, Cc, "a", ROT, fett=True); s.seite(A, Cc, "b")
    s.seite(B, F, "h<tspan font-size='2' dy='0.8'>b</tspan>", aussen=False, ab=1.6, pos=0.78)
    s.winkel(A, B, Cc, "40,3°", rt=8.5); s.winkel(B, A, Cc, "63,5°", rt=8); s.winkel(Cc, A, B, "γ", ROT, rt=6.5, fett=True)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_B():
    P = pkt_aus(6.0, 48.4, 7.5)
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(Cc, A, B)
    s = Skizze(P)
    s.linie(Cc, F); s.rechter(F, B, Cc)
    s.linie(B, Cc, ROT, 0.8)
    s.seite(A, Cc, "7,5 cm"); s.seite(B, Cc, "a", ROT, fett=True)
    s.seite(A, F, "c<tspan font-size='2' dy='0.8'>1</tspan>", ab=2.6); s.seite(F, B, "c<tspan font-size='2' dy='0.8'>2</tspan>", ab=2.6)
    s.seite(Cc, F, "h<tspan font-size='2' dy='0.8'>c</tspan>", aussen=False, ab=2.2)
    x, y = s.m(3.0, 0); s.text(x, y + 7.2, "6,0 cm")
    s.winkel(A, B, Cc, "48,4°", rt=8.5)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_3a():
    P = pkt_aus(6.4, 47.39, 6.75)
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(B, A, Cc)
    s = Skizze(P)
    s.linie(B, F); s.rechter(F, A, B)
    s.linie(A, Cc, ROT, 0.8)
    s.seite(A, B, "6,4 cm"); s.seite(B, Cc, "5,3 cm")
    s.seite(A, F, "b<tspan font-size='2' dy='0.8'>1</tspan>", ROT); s.seite(F, Cc, "b<tspan font-size='2' dy='0.8'>2</tspan>", ROT)
    s.seite(B, F, "h<tspan font-size='2' dy='0.8'>b</tspan>", aussen=False, ab=2.2)
    s.winkel(A, B, Cc, "α", ROT, rt=7, fett=True); s.winkel(B, A, Cc, "β", ROT, rt=6.5, fett=True); s.winkel(Cc, A, B, "62,8°", rt=8.5)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_3b():
    P = pkt_aus(7.4, 59.2, 5.8)
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(A, B, Cc)
    s = Skizze(P)
    s.linie(A, F); s.rechter(F, B, A)
    s.linie(B, Cc, ROT, 0.8)
    s.seite(A, B, "7,4 cm"); s.seite(A, Cc, "5,8 cm")
    s.seite(F, B, "a<tspan font-size='2' dy='0.8'>1</tspan>", ROT); s.seite(Cc, F, "a<tspan font-size='2' dy='0.8'>2</tspan>", ROT)
    s.seite(A, F, "h<tspan font-size='2' dy='0.8'>a</tspan>", aussen=False, ab=1.6, pos=0.6)
    s.winkel(A, B, Cc, "α", ROT, rt=6.5, fett=True); s.winkel(B, A, Cc, "β", ROT, rt=6.5, fett=True); s.winkel(Cc, A, B, "72,4°", r=2.6, rt=6.4)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_3c():
    P = pkt_aus(5.53, 115, 4.4)
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(Cc, A, B)
    s = Skizze(P, extra=[F], breite=56)
    s.linie(F, A, "#222", 0.45, "1.2,0.8"); s.linie(Cc, F); s.rechter(F, A, Cc)
    s.linie(A, B, ROT, 0.8)
    s.seite(A, Cc, "4,4 cm", aussen=False, pos=0.55, ab=3.2); s.seite(B, Cc, "8,4 cm", pos=0.4)
    s.seite(A, B, "c", ROT, fett=True); s.seite(F, A, "x", ab=2.6)
    s.seite(Cc, F, "h<tspan font-size='2' dy='0.8'>c</tspan>", ab=2.6, pos=0.72)
    s.winkel(A, B, Cc, "115°", rt=7.5); s.winkel(A, F, Cc, "α'", rt=6.2)
    s.winkel(B, A, Cc, "β", ROT, rt=8, fett=True)
    for n in "ABC": s.ecke(n)
    x, y = s.m(*F); s.text(x, y + 3.6, "F", gr=2.8)
    return s.svg()


def sk_5a():
    P = pkt_aus(7.5, 180 - 36 - 59.0, 0)  # Platzhalter, wird unten ersetzt
    B = (7.5, 0); A = (0, 0); Cc = (7.5 - 6.8 * C(36), 6.8 * S(36))
    P = dreieck(A, B, Cc)
    F = fuss(Cc, A, B)
    s = Skizze(P, breite=40, hoehe=27)
    s.linie(Cc, F, ROT, 0.7); s.rechter(F, B, Cc)
    s.seite(A, B, "7,5 cm"); s.seite(B, Cc, "6,8 cm")
    s.seite(Cc, F, "h<tspan font-size='2' dy='0.8'>c</tspan>", ROT, aussen=False, ab=2.2)
    s.winkel(B, A, Cc, "36,0°", r=3.5, rt=9)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_5b():
    Cc = (0, 0); B = (4.3, 0); A = (4.8 * C(65.9), 4.8 * S(65.9))
    P = dreieck(A, B, Cc)
    F = fuss(A, B, Cc)
    s = Skizze(P, breite=30, hoehe=26)
    s.linie(A, F, ROT, 0.7); s.rechter(F, B, A)
    s.seite(Cc, B, "4,3 cm"); s.seite(A, Cc, "4,8 cm")
    s.seite(A, F, "h<tspan font-size='2' dy='0.8'>a</tspan>", ROT, aussen=False, ab=1.8, pos=0.3)
    s.winkel(Cc, A, B, "65,9°", r=3, rt=8.5)
    for n in "ABC": s.ecke(n)
    return s.svg()


# ---------------------------------------------------------------- Textbausteine
def bruch(z, n):
    return f'<span class="br"><span>{z}</span><span>{n}</span></span>'


def i(name, idx):
    return f"{name}<sub>{idx}</sub>"


NR = "①②③④⑤⑥⑦"


def schritt(nr, kopf, *zeilen):
    z = "".join(f"<div>{t}</div>" for t in zeilen)
    return f'<div class="sch"><div class="kopf">{NR[nr - 1]} {kopf}</div>{z}</div>'


def erg(t):
    return f'<b class="erg">{t}</b>'


def um(t):
    return f'<span class="um">| {t}</span>'


def aufgabe(titel, svg, schritte, ergebnis, hinweis=""):
    """Eine Aufgabe: Skizze links, Schritte rechts, Ergebnis darunter."""
    h = f'<div class="hinweis">{hinweis}</div>' if hinweis else ""
    return (f'<section><h2>{titel}</h2><div class="zeile"><div class="sk">{svg}</div>'
            f'<div class="schritte">{"".join(schritte)}</div></div>'
            f'<div class="ergebnis">Ergebnis: {ergebnis}</div>{h}</section>')


def baue():
    a, b_, c3a, c3b, c3c, f5a, f5b = (R[x] for x in ("A", "B", "3a", "3b", "3c", "5a", "5b"))
    hb, hc, ha = i("h", "b"), i("h", "c"), i("h", "a")
    teile = []
    teile.append(aufgabe("S. 15 A", sk_A(), [
        schritt(1, "γ:", "γ = 180° − 40,3° − 63,5°", erg(f"γ = {k(a['g'], 1)}°")),
        schritt(2, f"{hb}:", f"sin 40,3° = {bruch(hb, '9,0')} {um('· 9,0')}", f"9,0 · sin 40,3° = {hb}", erg(f"{hb} = {k(a['hb'])} cm")),
        schritt(3, "a:", f"sin {k(a['g'], 1)}° = {bruch(k(a['hb']), 'a')} {um('a ↔ sin')}",
                f"a = {bruch(k(a['hb']), 'sin ' + k(a['g'], 1) + '°')}", erg(f"a = {k(a['a'])} cm")),
    ], f"γ = {k(a['g'], 1)}°; a = {k(a['a'])} cm ≈ {k(a['a'], 1)} cm"))

    teile.append(aufgabe("S. 15 B", sk_B(), [
        schritt(1, f"{hc}:", f"sin 48,4° = {bruch(hc, '7,5')} {um('· 7,5')}", erg(f"{hc} = {k(b_['hc'])} cm")),
        schritt(2, f"{i('c', 1)}:", f"cos 48,4° = {bruch(i('c', 1), '7,5')} {um('· 7,5')}", erg(f"{i('c', 1)} = {k(b_['c1'])} cm")),
        schritt(3, f"{i('c', 2)}:", f"{i('c', 2)} = 6,0 − {k(b_['c1'])}", erg(f"{i('c', 2)} = {k(b_['c2'])} cm")),
        schritt(4, "a:", f"a = √<span class='wu'>{k(b_['hc'])}² + {k(b_['c2'])}²</span>", erg(f"a = {k(b_['a'])} cm")),
        schritt(5, "A:", f"A = {bruch(1, 2)} · c · {hc}", f"A = {bruch(1, 2)} · 6,0 · {k(b_['hc'])}", erg(f"A = {k(b_['A'])} cm²")),
    ], f"A = {k(b_['A'])} cm² ≈ {k(b_['A'], 1)} cm²; a = {k(b_['a'])} cm ≈ {k(b_['a'], 1)} cm"))

    teile.append(aufgabe("S. 16 Nr. 3 a", sk_3a(), [
        schritt(1, f"{hb}:", f"sin 62,8° = {bruch(hb, '5,3')} {um('· 5,3')}", erg(f"{hb} = {k(c3a['hb'])} cm")),
        schritt(2, f"{i('b', 2)}:", f"cos 62,8° = {bruch(i('b', 2), '5,3')} {um('· 5,3')}", erg(f"{i('b', 2)} = {k(c3a['b2'])} cm")),
        schritt(3, f"{i('b', 1)}:", f"{i('b', 1)} = √<span class='wu'>6,4² − {k(c3a['hb'])}²</span>", erg(f"{i('b', 1)} = {k(c3a['b1'])} cm")),
        schritt(4, "b:", f"b = {k(c3a['b1'])} + {k(c3a['b2'])}", erg(f"b = {k(c3a['b'])} cm")),
        schritt(5, "α:", f"sin α = {bruch(k(c3a['hb']), '6,4')}", f"sin α = {k(c3a['q'], 4)}", erg(f"α = {k(c3a['al'], 1)}°")),
        schritt(6, "β:", f"β = 180° − {k(c3a['al'], 1)}° − 62,8°", erg(f"β = {k(c3a['be'], 1)}°")),
    ], f"b = {k(c3a['b'])} cm ≈ {k(c3a['b'], 1)} cm; α = {k(c3a['al'], 1)}°; β = {k(c3a['be'], 1)}°"))

    teile.append(aufgabe("S. 16 Nr. 3 b", sk_3b(), [
        schritt(1, f"{ha}:", f"sin 72,4° = {bruch(ha, '5,8')} {um('· 5,8')}", erg(f"{ha} = {k(c3b['ha'])} cm")),
        schritt(2, f"{i('a', 2)}:", f"cos 72,4° = {bruch(i('a', 2), '5,8')} {um('· 5,8')}", erg(f"{i('a', 2)} = {k(c3b['a2'])} cm")),
        schritt(3, f"{i('a', 1)}:", f"{i('a', 1)} = √<span class='wu'>7,4² − {k(c3b['ha'])}²</span>", erg(f"{i('a', 1)} = {k(c3b['a1'])} cm")),
        schritt(4, "a:", f"a = {k(c3b['a1'])} + {k(c3b['a2'])}", erg(f"a = {k(c3b['a'])} cm")),
        schritt(5, "β:", f"sin β = {bruch(k(c3b['ha']), '7,4')}", f"sin β = {k(c3b['q'], 4)}", erg(f"β = {k(c3b['be'], 1)}°")),
        schritt(6, "α:", f"α = 180° − {k(c3b['be'], 1)}° − 72,4°", erg(f"α = {k(c3b['al'], 1)}°")),
    ], f"a = {k(c3b['a'])} cm ≈ {k(c3b['a'], 1)} cm; β = {k(c3b['be'], 1)}°; α = {k(c3b['al'], 1)}°",
        "Im Buch steht AC = 5,8 cm. Die Buchlösung rechnet mit 5,4 cm und kommt deshalb auf a = 6,9 cm; β = 44,1°; α = 63,5°."))

    teile.append(aufgabe("S. 16 Nr. 3 c", sk_3c(), [
        schritt(1, "α':", "α' = 180° − 115°", erg(f"α' = {c3c['al2']},0°")),
        schritt(2, f"{hc}:", f"sin 65,0° = {bruch(hc, '4,4')} {um('· 4,4')}", erg(f"{hc} = {k(c3c['hc'])} cm")),
        schritt(3, "x:", f"cos 65,0° = {bruch('x', '4,4')} {um('· 4,4')}", erg(f"x = {k(c3c['x'])} cm")),
        schritt(4, "x + c:", f"x + c = √<span class='wu'>8,4² − {k(c3c['hc'])}²</span>", erg(f"x + c = {k(c3c['cx'])} cm")),
        schritt(5, "c:", f"c = {k(c3c['cx'])} − {k(c3c['x'])}", erg(f"c = {k(c3c['c'])} cm")),
        schritt(6, "β:", f"sin β = {bruch(k(c3c['hc']), '8,4')}", f"sin β = {k(c3c['q'], 4)}", erg(f"β = {k(c3c['be'], 1)}°")),
    ], f"c = {k(c3c['c'])} cm ≈ {k(c3c['c'], 1)} cm; β = {k(c3c['be'], 1)}°",
        "Die Höhe h<sub>c</sub> liegt außerhalb, weil α stumpf ist: c bis zum Fußpunkt F verlängern."))

    paar = []
    paar.append(aufgabe("Für Schnelle: S. 16 Nr. 5 a", sk_5a(), [
        schritt(1, f"1. Weg {hc}:", f"sin 36,0° = {bruch(hc, '6,8')} {um('· 6,8')}", erg(f"{hc} = {k(f5a['hc'])} cm")),
        schritt(2, "A:", f"A = {bruch(1, 2)} · 7,5 · {k(f5a['hc'])}", erg(f"A = {k(f5a['A1'])} cm²")),
        schritt(3, "2. Weg A:", f"A = {bruch(1, 2)} · a · c · sin β", f"A = {bruch(1, 2)} · 6,8 · 7,5 · sin 36,0°", erg(f"A = {k(f5a['A2'])} cm² ≈ {k(f5a['A2'], 1)} cm²")),
    ], f"A = {k(f5a['A1'], 1)} cm²"))

    paar.append(aufgabe("Für Schnelle: S. 16 Nr. 5 b", sk_5b(), [
        schritt(1, f"1. Weg {ha}:", f"sin 65,9° = {bruch(ha, '4,8')} {um('· 4,8')}", erg(f"{ha} = {k(f5b['ha'])} cm")),
        schritt(2, "A:", f"A = {bruch(1, 2)} · 4,3 · {k(f5b['ha'])}", erg(f"A = {k(f5b['A1'])} cm²")),
        schritt(3, "2. Weg A:", f"A = {bruch(1, 2)} · a · b · sin γ", f"A = {bruch(1, 2)} · 4,3 · 4,8 · sin 65,9°", erg(f"A = {k(f5b['A2'])} cm²")),
    ], f"A = {k(f5b['A1'])} cm² ≈ {k(f5b['A1'], 1)} cm²"))
    teile.append('<div class="paar">' + "".join(paar) + "</div>")

    css = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ overflow: hidden; }}
body {{ margin: 0; background: #fff; font-family: Helvetica, Arial, sans-serif; color: #222; }}
.seite {{ width: 210mm; min-height: 297mm; padding: 6mm 9mm 4mm; }}
.balken {{ background: #d9d9d9; font-weight: 700; font-size: 11pt; padding: 1.6mm 3mm; display: flex; justify-content: space-between; }}
.balken span {{ font-weight: 400; font-size: 9pt; }}
section {{ border-bottom: 0.3mm solid #ccc; padding: 1mm 0 1mm; break-inside: avoid; }}
h2 {{ font-size: 9.5pt; margin: 0; break-after: avoid; }}
.zeile {{ display: flex; gap: 2.5mm; align-items: flex-start; }}
.sk {{ flex: 0 0 52mm; display: flex; justify-content: center; }}
.schritte {{ flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2mm 2.5mm; }}
.sch {{ font-size: 8pt; line-height: 1.28; white-space: nowrap; }}
.kopf {{ font-weight: 700; }}
.erg {{ color: {ROT}; }}
.um {{ white-space: nowrap; color: #777; font-size: 7.5pt; margin-left: 1mm; }}
.br {{ display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 7.6pt; line-height: 1.15; margin: 0 0.4mm; }}
.br span:first-child {{ border-bottom: 0.25mm solid #222; padding: 0 0.6mm; }}
.wu {{ border-top: 0.25mm solid #222; padding: 0 0.4mm; }}
.ergebnis {{ font-size: 8.6pt; color: {ROT}; font-weight: 700; margin-top: 0.6mm; }}
.paar {{ display: flex; gap: 3mm; }}
.paar section {{ flex: 1; }}
.paar .sk {{ flex: 0 0 auto; }}
.paar .zeile {{ gap: 1.5mm; }}
.paar .schritte {{ grid-template-columns: 0.75fr 1.25fr; grid-template-rows: auto auto; grid-auto-flow: column; gap: 0.6mm 1.5mm; }}
.paar .sch {{ font-size: 7.6pt; }}
.hinweis {{ font-size: 7.6pt; color: #555; margin-top: 0.4mm; }}
@media screen {{ body {{ background: #888; }} .seite {{ background: #fff; margin: 6mm auto; box-shadow: 0 1mm 4mm #0005; }} }}
"""
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{NAME}</title><style>{css}</style></head><body>'
            f'<div class="seite"><div class="balken">Mathe 10b   Trigonometrie: Lösungen <span>Schnittpunkt 10, S. 15 A, B; S. 16 Nr. 3 rechts; Nr. 5 links</span></div>'
            + "".join(teile) + "</div></body></html>")


def main():
    html = HIER / f"{NAME}.html"
    pdf = HIER / f"{NAME}.pdf"
    html.write_text(baue(), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=3000", html.as_uri()], check=True, capture_output=True)
    from pypdf import PdfReader
    n = len(PdfReader(str(pdf)).pages)
    print(html.name, "|", pdf.name, "| Seiten:", n)
    assert n == 1, "passt nicht auf eine Seite"


if __name__ == "__main__":
    main()
