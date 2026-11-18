#!/usr/bin/env python3
"""Mathe 7c, Ausfall Do 19.11.2026: Übungsblatt (A4 Vorder- und Rückseite) zu Winkeln an Parallelen
und Dreiecksarten. Lösung = dasselbe Blatt ausgefüllt in Magenta. Figuren als berechnete SVG (Einheit mm).
Orientierung: Schnittpunkt 7, S. 46-52 (Aufgaben abgewandelt)."""
import math, re, subprocess
from pathlib import Path

HIER = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAG, ROT, BLAU, GRUEN, ORANGE, SCHWARZ = "#E6007E", "#D7263D", "#1F6FD1", "#1E9E52", "#E08A00", "#222"
BASIS = "Mathe 7c – Übungsblatt Winkel an Parallelen, Dreiecksarten"
L = False   # Lösung an/aus (wird in main gesetzt)


# ------------------------------------------------------------ Geometrie-Hilfen (math. Winkel, SVG-y nach unten)
def P(S, r, a):
    return (S[0] + r * math.cos(math.radians(a)), S[1] - r * math.sin(math.radians(a)))


def ang(S, Q):
    return math.degrees(math.atan2(-(Q[1] - S[1]), Q[0] - S[0])) % 360


def linie(p, q, f=SCHWARZ, b=0.5):
    return f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="{f}" stroke-width="{b}" stroke-linecap="round"/>'


def text(p, s, f=SCHWARZ, g=3.6, fett=False, anker="middle"):
    w = ' font-weight="700"' if fett else ""
    return f'<text x="{p[0]:.2f}" y="{p[1] + g * 0.35:.2f}" font-size="{g}" fill="{f}" text-anchor="{anker}"{w}>{s}</text>'


def sektor(S, a1, a2, f=ROT, r=6, fuell=True):
    """Winkelbogen von a1 gegen den Uhrzeigersinn bis a2."""
    d = (a2 - a1) % 360
    p, q = P(S, r, a1), P(S, r, a2)
    gross = 1 if d > 180 else 0
    fl = f'fill="{f}" fill-opacity="0.13"' if fuell else 'fill="none"'
    return (f'<path d="M{S[0]:.2f},{S[1]:.2f} L{p[0]:.2f},{p[1]:.2f} A{r},{r} 0 {gross} 0 {q[0]:.2f},{q[1]:.2f} Z" {fl} stroke="none"/>'
            f'<path d="M{p[0]:.2f},{p[1]:.2f} A{r},{r} 0 {gross} 0 {q[0]:.2f},{q[1]:.2f}" fill="none" stroke="{f}" stroke-width="0.5"/>')


def rechter_winkel(S, a1, f=ROT, r=4.2):
    """Viertelkreis mit Punkt, von a1 aus 90° gegen den Uhrzeigersinn."""
    return sektor(S, a1, a1 + 90, f, r) + f'<circle cx="{P(S, r * 0.45, a1 + 45)[0]:.2f}" cy="{P(S, r * 0.45, a1 + 45)[1]:.2f}" r="0.55" fill="{f}"/>'


def innen(V, Pp, Q):
    """Innenwinkel bei V zwischen VP und VQ: (Start, Ende, Größe) gegen den Uhrzeigersinn."""
    a1, a2 = ang(V, Pp), ang(V, Q)
    if (a2 - a1) % 360 > 180:
        a1, a2 = a2, a1
    return a1, a2, (a2 - a1) % 360


def striche(p, q, n, f=SCHWARZ):
    """n kleine Querstriche in der Mitte der Seite pq (gleich lange Seiten)."""
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    l = math.dist(p, q)
    ux, uy = (q[0] - p[0]) / l, (q[1] - p[1]) / l
    nx, ny = -uy, ux
    s = ""
    for i in range(n):
        o = (i - (n - 1) / 2) * 1.3
        c = (m[0] + ux * o, m[1] + uy * o)
        s += linie((c[0] - nx * 1.7, c[1] - ny * 1.7), (c[0] + nx * 1.7, c[1] + ny * 1.7), b=0.45, f=f)
    return s


def svg(w, h, inhalt, klasse="fig"):
    return (f'<svg class="{klasse}" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Avenir Next, Helvetica Neue, Arial, sans-serif">{inhalt}</svg>')


# ------------------------------------------------------------ Figur: zwei Parallelen und eine Schneidende
def parallelen(w, h, t, phi=0, abst=18, schnitt_x=None, labels=None, farben=None, namen=("g", "h"), r=6.5, lab_r=None):
    """Parallelen g (oben) und h (unten) in Richtung phi, Schneidende mit Winkel t zu den Parallelen.
    labels: {(0|1, sektor 0..3): text}; Sektor 0 = rechts oben, 1 = links oben, 2 = links unten, 3 = rechts unten."""
    labels, farben = labels or {}, farben or {}
    M = (w / 2, h / 2)
    def R(p):   # lokale Koordinaten (x rechts, y oben, Ursprung Mitte) -> SVG, gedreht um phi
        c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
        return (M[0] + p[0] * c - p[1] * s, M[1] - (p[0] * s + p[1] * c))
    sx = schnitt_x if schnitt_x is not None else 0
    S1 = (sx + (abst / 2) / math.tan(math.radians(t)) * 0, abst / 2)
    S1 = (sx + abst / 2 / math.tan(math.radians(t)), abst / 2)
    S2 = (sx - abst / 2 / math.tan(math.radians(t)), -abst / 2)
    lang = max(w, h)
    out = ""
    for yy, nm in ((abst / 2, namen[0]), (-abst / 2, namen[1])):
        out += linie(R((-lang, yy)), R((lang, yy)), b=0.55)
    # Schneidende weit genug
    d = (math.cos(math.radians(t)), math.sin(math.radians(t)))
    out += linie(R((S1[0] + d[0] * lang, S1[1] + d[1] * lang)), R((S2[0] - d[0] * lang, S2[1] - d[1] * lang)), b=0.55)
    grenzen = [(0, t), (t, 180), (180, 180 + t), (180 + t, 360)]
    for (i, k), lab in labels.items():
        S = R(S1 if i == 0 else S2)
        a1, a2 = grenzen[k]
        f = farben.get((i, k), ROT)
        out += sektor(S, a1 + phi, a2 + phi, f, r)
        mitte = (a1 + a2) / 2 + phi
        lr = lab_r or (r + 3.4 if (a2 - a1) < 50 else r * 0.62 if (a2 - a1) > 70 else r + 3.2)
        if (a2 - a1) >= 50:
            lr = lab_r or r * 0.62 + 0.4
        tf = MAG if lab.startswith("§") else f
        out += text(P(S, lr, mitte), lab.lstrip("§"), tf, g=3.2, fett=lab.startswith("§"))
    # Namen der Parallelen am rechten Rand
    for yy, nm in ((abst / 2, namen[0]), (-abst / 2, namen[1])):
        p = R((w / 2 - 6 if phi < 45 else h / 2 - 5, yy + 2.3))
        out += f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="3.4" font-style="italic">{nm}</text>'
    return svg(w, h, out)


# ------------------------------------------------------------ Figur: Dreieck aus zwei Winkeln
def dreieck_pkte(al, be, c, A=(0, 0), drehung=0):
    b = c * math.sin(math.radians(be)) / math.sin(math.radians(al + be))
    pA, pB = A, (A[0] + c * math.cos(math.radians(drehung)), A[1] - c * math.sin(math.radians(drehung)))
    pC = P(A, b, al + drehung)
    return pA, pB, pC


def tri_fig(w, h, al, be, c, winkel=None, gleich=(), rechts=None, eck=("A", "B", "C"), dreh=0, rand=None, zus="", r=5.5, lrf=None):
    """winkel: {'A'|'B'|'C': text}; gleich: [(seite, n)] mit seite 'a','b','c'; rechts: Ecke mit rechtem Winkel."""
    A, B, C = dreieck_pkte(al, be, c, drehung=dreh)
    xs, ys = [A[0], B[0], C[0]], [A[1], B[1], C[1]]
    k = min((w - 9) / (max(xs) - min(xs)), (h - 9) / (max(ys) - min(ys)))
    A, B, C = [((p[0] - min(xs)) * k, (p[1] - min(ys)) * k) for p in (A, B, C)]
    dx, dy = (w - (max(xs) - min(xs)) * k) / 2, (h - (max(ys) - min(ys)) * k) / 2
    A, B, C = [(p[0] + dx, p[1] + dy) for p in (A, B, C)]
    pk = {"A": (A, B, C), "B": (B, C, A), "C": (C, A, B)}
    out = f'<polygon points="{A[0]:.2f},{A[1]:.2f} {B[0]:.2f},{B[1]:.2f} {C[0]:.2f},{C[1]:.2f}" fill="#f4f6fa" stroke="{SCHWARZ}" stroke-width="0.55" stroke-linejoin="round"/>'
    seiten = {"a": (B, C), "b": (A, C), "c": (A, B)}
    for s, n in gleich:
        out += striche(*seiten[s], n)
    for e, lab in (winkel or {}).items():
        V, Q1, Q2 = pk[e]
        a1, a2, g = innen(V, Q1, Q2)
        if e == rechts:
            out += rechter_winkel(V, a1)
            if lab:
                out += text(P(V, 8, (a1 + a2) / 2), lab.lstrip("§"), MAG if lab.startswith("§") else ROT, g=3.0)
            continue
        rr = r
        out += sektor(V, a1, a2, ROT, rr)
        lr = lrf or (rr + 3.8 if g < 100 else rr + 2.6)
        out += text(P(V, lr, (a1 + a2) / 2), lab.lstrip("§"), MAG if lab.startswith("§") else ROT, g=3.0, fett=lab.startswith("§"))
    if rechts and rechts not in (winkel or {}):
        V, Q1, Q2 = pk[rechts]
        out += rechter_winkel(V, innen(V, Q1, Q2)[0])
    for name, V in zip(eck, (A, B, C)):
        if not name:
            continue
        S = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
        l = math.dist(S, V)
        out += text((V[0] + (V[0] - S[0]) / l * 3.2, V[1] + (V[1] - S[1]) / l * 3.2), name, g=3.3)
    return svg(w, h, out + zus)


# ------------------------------------------------------------ Bausteine fürs Blatt
def box(loes, breite=18):
    if L:
        return f'<span class="box" style="min-width:{breite}mm"><b class="m">{loes}</b></span>'
    return f'<span class="box" style="min-width:{breite}mm"></span>'


def zeile_lsg(loes, n=1):
    if L:
        return f'<div class="antw m">{loes}</div>'
    return '<div class="lin"></div>' * n


def kreuz(an):
    return f'<span class="cb">{"<b class=m>✕</b>" if (L and an) else ""}</span>'


def aufgabe(nr, titel, kreis):
    return f'<h2><span class="nr">{nr}</span><span class="kr">{kreis}</span>{titel}</h2>'


def kopf(seite):
    lm = '<span class="lmark">Lösung</span>' if L else ""
    if seite == 1:
        nf = "" if L else '<div class="name"><span>Name</span><span class="k">Datum</span></div>'
        return (f'<div class="kopf"><div><span class="chip">Mathe 7c</span><h1>Übungsblatt: Winkel an Parallelen, Dreiecksarten</h1></div>{lm}</div>'
                f'{nf}<p class="leg">○ leicht &nbsp; ◐ mittel &nbsp; ● schwer &nbsp;&nbsp; Alles ins Heft oder direkt aufs Blatt. Nicht messen, sondern begründen!</p>')
    return f'<div class="kopf"><div><span class="chip">Mathe 7c</span><h1>Rückseite: Dreiecksarten</h1></div>{lm}</div>'


# ------------------------------------------------------------ Seite 1: Winkel an Parallelen
def merk_parallelen():
    lab = {(0, 0): "α", (0, 1): "β", (0, 2): "γ", (0, 3): "δ", (1, 0): "α′", (1, 1): "β′", (1, 2): "γ′", (1, 3): "δ′"}
    far = {(0, 0): ROT, (1, 0): ROT, (0, 2): ROT, (1, 2): ROT, (0, 1): BLAU, (0, 3): BLAU, (1, 1): BLAU, (1, 3): BLAU}
    fig = parallelen(58, 34, 58, abst=18, labels=lab, farben=far, r=6)
    tab = ('<table class="paare"><tr><th>Paar</th><th>Lage</th><th>Größe</th><th>Beispiel</th></tr>'
           '<tr><td><b>Scheitelwinkel</b></td><td>gegenüber am selben Schnittpunkt</td><td>gleich groß</td><td>α = γ</td></tr>'
           '<tr><td><b>Nebenwinkel</b></td><td>nebeneinander am selben Schnittpunkt</td><td>zusammen 180°</td><td>α + β = 180°</td></tr>'
           '<tr><td><b>Stufenwinkel</b></td><td>gleiche Lage an beiden Schnittpunkten</td><td>gleich groß</td><td>α = α′</td></tr>'
           '<tr><td><b>Wechselwinkel</b></td><td>über Kreuz zwischen den Parallelen (Z-Form)</td><td>gleich groß</td><td>γ = α′</td></tr></table>')
    rez = ('<div class="rezept"><b>Rezept: fehlenden Winkel bestimmen</b><ol><li>Bekannten Winkel suchen.</li>'
           '<li>Paar benennen: Scheitel-, Neben-, Stufen- oder Wechselwinkel?</li>'
           '<li>Gleich groß übernehmen oder 180° minus rechnen.</li></ol>'
           '<span class="kl">An Parallelen (g || h) gibt es nur zwei Größen: die roten sind gleich, die blauen sind gleich, rot + blau = 180°.</span></div>')
    return (f'<div class="merk"><div class="mt">Merke: Winkel an Parallelen</div><div class="mrow">{fig}<div>{tab}{rez}</div></div></div>')


def a1():
    lab = {(0, 0): "α", (0, 1): "β", (0, 2): "γ", (0, 3): "δ", (1, 0): "α′", (1, 1): "β′", (1, 2): "γ′", (1, 3): "δ′"}
    fig = parallelen(54, 30, 118, abst=15, labels=lab, r=5.5)
    paare = [("α und γ", "Scheitelwinkel"), ("β und γ", "Nebenwinkel"), ("δ und δ′", "Stufenwinkel"),
             ("γ und α′", "Wechselwinkel"), ("β und β′", "Stufenwinkel"), ("δ und β′", "Wechselwinkel")]
    li = "".join(f'<div class="pz">{chr(97 + i)}) {p} sind {box(l, 27)}</div>' for i, (p, l) in enumerate(paare))
    return aufgabe(1, "Wie heißt das Winkelpaar? (g || h)", "○") + f'<div class="row">{fig}<div class="grid2">{li}</div></div>'


def a2():
    lab = {(0, 0): "62°", (0, 1): "β", (0, 2): "γ", (0, 3): "δ", (1, 0): "α′", (1, 1): "β′", (1, 2): "γ′", (1, 3): "δ′"}
    fig = parallelen(54, 32, 62, abst=16, labels=lab, r=5.5)
    werte = [("β", "118°", "Nebenwinkel von 62°"), ("γ", "62°", "Scheitelwinkel von 62°"), ("δ", "118°", "Scheitelwinkel von β"),
             ("α′", "62°", "Stufenwinkel von 62°"), ("β′", "118°", "Stufenwinkel von β"), ("γ′", "62°", "Wechselwinkel zu 62°… nein: Stufenwinkel von γ"),
             ("δ′", "118°", "Stufenwinkel von δ")]
    werte[5] = ("γ′", "62°", "Stufenwinkel von γ")
    rows = "".join(f'<tr><td>{n} =</td><td>{box(v, 14)}</td><td class="weil">weil {box(b, 52) if L else box("", 52)}</td></tr>' for n, v, b in werte)
    return (aufgabe(2, "Bestimme alle Winkel ohne Messen. Schreibe dazu, warum. (g || h)", "○")
            + f'<div class="row">{fig}<table class="wt">{rows}</table></div>')


def a3():
    fa = parallelen(50, 28, 40, abst=14, labels={(0, 1): "140°", (1, 0): "§x" if L else "x", (1, 1): "y"}, r=5.5)
    fb = parallelen(44, 34, 105, phi=78, abst=14, labels={(0, 3): "75°", (1, 1): "x", (1, 2): "y"}, r=5.5, namen=("g", "h"))
    la = f'x = {box("40°", 13)} weil {box("Nebenwinkel 180° − 140°, dann Stufenwinkel", 58)}<br>y = {box("140°", 13)} weil {box("Wechselwinkel zu δ (Scheitelwinkel von 140°)", 58)}'
    lb = f'x = {box("75°", 13)} weil {box("Wechselwinkel zu 75°", 40)}<br>y = {box("105°", 13)} weil {box("Nebenwinkel: 180° − 75°", 40)}'
    return (aufgabe(3, "Wie groß sind x und y? Begründe. (g || h)", "◐")
            + f'<div class="row"><div class="sub">a)</div>{fa}<div class="lsg">{la}</div></div>'
            + f'<div class="row"><div class="sub">b)</div>{fb}<div class="lsg">{lb}</div></div>')


def a4():
    # Dreieck ABC, A und B auf h, C auf g, g || h
    al, be, c = 48, 67, 32
    A, B, C = dreieck_pkte(al, be, c)
    w, h = 66, 32
    dx, dy = (w - c) / 2, h - 4
    A, B, C = [(p[0] + dx, p[1] + dy) for p in (A, B, C)]
    out = linie((2, A[1]), (w - 2, A[1]), b=0.55) + linie((2, C[1]), (w - 2, C[1]), b=0.55)
    out += f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#f4f6fa" stroke="{SCHWARZ}" stroke-width="0.55"/>'
    out += sektor(C, 180, ang(C, A), BLAU, 6) + text(P(C, 9.5, (180 + ang(C, A)) / 2), "48°", BLAU, 3.0)
    out += sektor(C, ang(C, B), 360, GRUEN, 6) + text(P(C, 9.5, (ang(C, B) + 360) / 2), "67°", GRUEN, 3.0)
    for V, Q1, Q2, n, f in ((A, B, C, "α", BLAU), (B, C, A, "β", GRUEN), (C, A, B, "γ", ROT)):
        a1, a2, _ = innen(V, Q1, Q2)
        out += sektor(V, a1, a2, f, 6) + text(P(V, 3.9 if n != "γ" else 3.8, (a1 + a2) / 2), n, f, 2.8)
    for n, V, o in (("A", A, (-2.5, 3)), ("B", B, (2.5, 3)), ("C", C, (0, -3))):
        out += text((V[0] + o[0], V[1] + o[1]), n, g=3.2)
    out += f'<text x="{w - 5}" y="{C[1] - 1.5}" font-size="3.4" font-style="italic">g</text><text x="{w - 5}" y="{A[1] - 1.5}" font-size="3.4" font-style="italic">h</text>'
    fig = svg(w, h, out)
    t = (f'α = {box("48°", 12)} weil {box("Wechselwinkel zu 48°", 38)}<br>'
         f'β = {box("67°", 12)} weil {box("Wechselwinkel zu 67°", 38)}<br>'
         f'γ = {box("65°", 12)} weil {box("48° + γ + 67° = 180° (gestreckter Winkel bei C)", 38)}<br>'
         f'Was zeigt die Figur? {box("Die Winkelsumme im Dreieck ist 180°.", 50)}')
    return (aufgabe(4, "Parallelen und Dreieck: Bestimme α, β und γ. (g || h)", "●")
            + f'<div class="row">{fig}<div class="lsg">{t}</div></div>')


# ------------------------------------------------------------ Seite 2: Dreiecksarten
def merk_dreiecke():
    arten = [
        ("gleichseitig", tri_fig(28, 19, 60, 60, 22, gleich=[("a", 1), ("b", 1), ("c", 1)], eck=("", "", "")),
         "alle 3 Seiten gleich", "alle Winkel 60°"),
        ("gleichschenklig", tri_fig(28, 19, 70, 70, 18, gleich=[("a", 1), ("b", 1)], winkel={"A": "", "B": ""}, eck=("", "", ""), r=4),
         "2 Schenkel gleich", "Basiswinkel gleich groß"),
        ("rechtwinklig", tri_fig(28, 19, 90, 34, 14, rechts="A", eck=("", "", "")),
         "Seiten verschieden", "ein Winkel 90°, die anderen zusammen 90°"),
        ("gleichschenklig-<br>rechtwinklig", tri_fig(28, 19, 45, 45, 26, rechts="C", gleich=[("a", 1), ("b", 1)], eck=("", "", "")),
         "2 Schenkel gleich", "90°, 45°, 45°"),
        ("allgemein<br>(verschiedenseitig)", tri_fig(28, 19, 38, 72, 24, eck=("", "", "")),
         "alle Seiten verschieden", "nur: Summe 180°"),
    ]
    k = "".join(f'<div class="art"><b>{n}</b>{f}<span>{s}</span><span>{w}</span></div>' for n, f, s, w in arten)
    rez = ('<div class="rezept quer"><b>Rezept: Dreiecksart erkennen</b><ol>'
           '<li><b>Seiten:</b> gleiche Striche zählen (oder gleiche Winkel suchen). Keine → verschiedenseitig, 2 → gleichschenklig, 3 → gleichseitig.</li>'
           '<li><b>Winkel:</b> fehlenden Winkel mit 180° ausrechnen, dann den größten Winkel ansehen. Unter 90° → spitzwinklig, genau 90° → rechtwinklig, über 90° → stumpfwinklig.</li></ol></div>')
    return f'<div class="merk"><div class="mt">Merke: Dreiecksarten</div><div class="arten">{k}</div>{rez}</div>'


def a5():
    dr = [  # Buchstabe, Figur, Seiten-Art, Winkel-Art, Begründung
        ("A", tri_fig(30, 27, 60, 60, 22, gleich=[("a", 1), ("b", 1), ("c", 1)], eck=("", "", "")), 2, 0, "3 gleiche Seiten, alle 60°"),
        ("B", tri_fig(30, 27, 45, 45, 26, rechts="C", gleich=[("a", 1), ("b", 1)], eck=("", "", "")), 1, 1, "2 gleiche Seiten, 90°"),
        ("C", tri_fig(42, 24, 30, 30, 30, winkel={"A": "30°", "B": "30°"}, eck=("", "", "")), 1, 2, "2 gleiche Winkel, 3. Winkel 120°"),
        ("D", tri_fig(30, 27, 90, 35, 14, rechts="A", winkel={"B": "35°"}, eck=("", "", "")), 0, 1, "90°, 35°, 55°: alle verschieden"),
        ("E", tri_fig(30, 27, 65, 65, 16, gleich=[("a", 1), ("b", 1)], winkel={"C": "50°"}, eck=("", "", "")), 1, 0, "Basiswinkel je 65°, alle unter 90°"),
        ("F", tri_fig(42, 24, 25, 40, 30, winkel={"A": "25°", "B": "40°"}, eck=("", "", "")), 0, 2, "3. Winkel 115°, alle verschieden"),
    ]
    figs = "".join(f'<div class="tf"><b>{b}</b>{f}</div>' for b, f, *_ in dr)
    kopfz = "".join(f"<th>{b}</th>" for b, *_ in dr)
    zeilen = ""
    for i, n in enumerate(("verschiedenseitig", "gleichschenklig", "gleichseitig")):
        zeilen += f"<tr><td>{n}</td>" + "".join(f"<td>{kreuz(s == i)}</td>" for _, _, s, _, _ in dr) + "</tr>"
    for i, n in enumerate(("spitzwinklig", "rechtwinklig", "stumpfwinklig")):
        zeilen += f'<tr{" class=trenn" if i == 0 else ""}><td>{n}</td>' + "".join(f"<td>{kreuz(w == i)}</td>" for _, _, _, w, _ in dr) + "</tr>"
    beg = "".join(f'<div class="bg">{b}: {box(t, 50)}</div>' for b, _, _, _, t in dr[2:4])
    return (aufgabe(5, "Welche Art ist es? Kreuze zweimal an: einmal nach Seiten, einmal nach Winkeln.", "○")
            + f'<div class="figs">{figs}</div><table class="kt"><tr><th></th>{kopfz}</tr>{zeilen}</table>'
            + f'<p class="klein">Begründe bei C und D in einem Satz:</p><div class="grid2">{beg}</div>')


def a6():
    def m(t, w):
        return f'<span class="mlab">{t}</span>'
    fa = tri_fig(40, 32, 70, 70, 16, gleich=[("a", 1), ("b", 1)], winkel={"C": "40°", "A": "§70°" if L else "α", "B": "§70°" if L else "β"}, eck=("A", "B", "C"), lrf=7)
    fb = tri_fig(40, 32, 45, 45, 28, rechts="C", gleich=[("a", 1), ("b", 1)], winkel={"A": "§45°" if L else "α", "B": "§45°" if L else "β"}, eck=("A", "B", "C"))
    fc = tri_fig(44, 26, 35, 35, 32, gleich=[("a", 1), ("b", 1)], winkel={"A": "35°", "B": "§35°" if L else "β", "C": "§110°" if L else "γ"}, eck=("A", "B", "C"))
    fd = tri_fig(36, 32, 60, 60, 22, gleich=[("a", 1), ("b", 1), ("c", 1)], winkel={"A": "§60°" if L else "α", "B": "§60°" if L else "β", "C": "§60°" if L else "γ"}, eck=("A", "B", "C"))
    t = [("a)", fa, f'α = {box("70°", 11)} β = {box("70°", 11)}', "180° − 40° = 140°, durch 2"),
         ("b)", fb, f'α = {box("45°", 11)} β = {box("45°", 11)}', "90° übrig, durch 2"),
         ("c)", fc, f'β = {box("35°", 11)} γ = {box("110°", 11)}', "Basiswinkel gleich, 180° − 70°"),
         ("d)", fd, f'α = β = γ = {box("60°", 11)}', "180° durch 3")]
    k = "".join(f'<div class="a6"><span class="sub">{s}</span>{f}<div>{z}</div><div class="klein m">{b if L else ""}</div></div>' for s, f, z, b in t)
    return aufgabe(6, "Bestimme die fehlenden Winkel ohne Messen.", "◐") + f'<div class="a6row">{k}</div>'


def a7():
    w, h = 60, 34
    al = 70
    c = 14
    A, B, C = dreieck_pkte(al, al, c)
    dx, dy = (w - c) / 2, h - 6
    A, B, C = [(p[0] + dx, p[1] + dy) for p in (A, B, C)]
    out = linie((2, A[1]), (w - 2, A[1]), b=0.55) + linie((2, C[1]), (w - 2, C[1]), b=0.55)
    out += f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#f4f6fa" stroke="{SCHWARZ}" stroke-width="0.55"/>'
    out += striche(A, C, 1) + striche(B, C, 1)
    out += sektor(C, 180, ang(C, A), BLAU, 6) + text(P(C, 9.5, (180 + ang(C, A)) / 2), "70°", BLAU, 3.0)
    for V, Q1, Q2, n in ((A, B, C, "α"), (B, C, A, "β"), (C, A, B, "γ")):
        a1, a2, _ = innen(V, Q1, Q2)
        out += sektor(V, a1, a2, ROT, 5) + text(P(V, 8.6, (a1 + a2) / 2), n, ROT, 2.8)
    for n, V, o in (("A", A, (-2.5, 3)), ("B", B, (2.5, 3)), ("C", C, (2.5, -2.5))):
        out += text((V[0] + o[0], V[1] + o[1]), n, g=3.2)
    out += f'<text x="{w - 5}" y="{C[1] - 1.5}" font-size="3.4" font-style="italic">g</text><text x="{w - 5}" y="{A[1] - 1.5}" font-size="3.4" font-style="italic">h</text>'
    t = (f'α = {box("70°", 12)} weil {box("Wechselwinkel zu 70°", 40)}<br>'
         f'β = {box("70°", 12)} weil {box("Basiswinkel, gleichschenklig", 40)}<br>'
         f'γ = {box("40°", 12)} weil {box("180° − 70° − 70°", 40)}<br>'
         f'Art: {box("gleichschenklig und spitzwinklig", 60)}')
    return (aufgabe(7, "Parallelen und Dreieck: Bestimme α, β, γ und die Dreiecksart. (g || h)", "●")
            + f'<div class="row">{svg(w, h, out)}<div class="lsg">{t}</div></div>')


def a8():
    s = [("Ein Dreieck kann zwei rechte Winkel haben.", "falsch", "90° + 90° = 180°, für den dritten Winkel bleibt nichts."),
         ("Jedes gleichseitige Dreieck ist auch gleichschenklig.", "wahr", "Es hat sogar 3 gleiche Seiten, also auch 2."),
         ("Ein rechtwinkliges Dreieck kann gleichschenklig sein.", "wahr", "Mit 90°, 45°, 45°."),
         ("Ein stumpfwinkliges Dreieck kann gleichseitig sein.", "falsch", "Gleichseitig heißt: alle Winkel 60°.")]
    r = "".join(f'<tr><td>{chr(97 + i)}) {a}</td><td>{box(wf, 13)}</td><td>{box(b, 66)}</td></tr>' for i, (a, wf, b) in enumerate(s))
    return aufgabe(8, "Wahr oder falsch? Begründe.", "●") + f'<table class="wf"><tr><th></th><th>wahr/falsch</th><th>weil</th></tr>{r}</table>'


STIL = """
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Avenir Next","Helvetica Neue",Arial,sans-serif;color:#222;font-size:9pt;line-height:1.25}
.seite{width:210mm;height:297mm;padding:9mm 11mm 8mm;overflow:hidden;page-break-after:always;position:relative}
.kopf{display:flex;justify-content:space-between;align-items:center;border-bottom:1.6px solid #1F4FA0;padding-bottom:1.5mm}
.kopf h1{display:inline;font-size:14pt;margin:0 0 0 2mm;color:#1F4FA0}
.chip{background:#1F4FA0;color:#fff;border-radius:3px;padding:.6mm 2mm;font-size:9pt;font-weight:700}
.lmark{color:#fff;background:#E6007E;padding:1mm 3mm;border-radius:3px;font-weight:700}
.name{display:flex;gap:4mm;margin-top:1.5mm}.name span{flex:1;border-bottom:1px solid #999;font-size:8pt;color:#777;padding-bottom:3mm}.name .k{flex:.35}
.leg{font-size:8.4pt;color:#555;margin:1.2mm 0 1.5mm}
.merk{border:1.4px solid #1F4FA0;border-radius:2.5mm;padding:1.6mm 2.5mm;background:#F3F7FD;margin-bottom:2mm}
.mt{font-weight:700;color:#1F4FA0;margin-bottom:1mm}
.mrow{display:flex;gap:3mm;align-items:center}
table{border-collapse:collapse}
.paare{font-size:8.3pt;width:100%}.paare td,.paare th{border:1px solid #c9d3e3;padding:.5mm 1.2mm;text-align:left}.paare th{background:#e4ecf8}
.rezept{margin-top:1.2mm;font-size:8.4pt}.rezept ol{margin:.5mm 0 .5mm 5mm;padding:0}.rezept .kl{color:#444;font-size:8.2pt}
.rezept.quer ol li{margin-bottom:.3mm}
h2{font-size:9.8pt;margin:1.6mm 0 .6mm;display:flex;align-items:baseline;gap:1.6mm}
.nr{background:#222;color:#fff;border-radius:50%;width:5.2mm;height:5.2mm;display:inline-flex;align-items:center;justify-content:center;font-size:8.6pt;flex:none}
.kr{font-size:11pt}
.row{display:flex;gap:4mm;align-items:center;margin-bottom:.8mm}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 4mm;flex:1}
.pz{white-space:nowrap}
.box{display:inline-block;border-bottom:1px solid #555;height:4.8mm;vertical-align:bottom;padding:0 1mm;line-height:5.2mm}
.m{color:#E6007E}.box .m{font-weight:600;font-size:8.6pt}
.wt td{padding:0 1mm;white-space:nowrap}.wt .weil{font-size:8.6pt}
.lsg{line-height:1.85;font-size:9pt}
.sub{font-weight:700;align-self:flex-start}
.arten{display:flex;gap:1.5mm}.art{flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;font-size:8pt;background:#fff;border:1px solid #c9d3e3;border-radius:2mm;padding:1mm}
.art b{font-size:8.4pt;min-height:7mm}.art span{display:block}
.figs{display:flex;justify-content:space-between;align-items:flex-end}.tf{text-align:center}.tf b{display:block}
.kt{width:100%;font-size:8.6pt;margin-top:1mm}.kt td,.kt th{border:1px solid #bbb;padding:0 1.5mm;text-align:center}.kt td:first-child{text-align:left;width:34mm}
.kt tr.trenn td{border-top:2px solid #555}
.cb{display:inline-block;width:3.6mm;height:3.6mm;border:1px solid #555;vertical-align:middle;line-height:3.4mm;font-size:8pt}
.klein{font-size:8.4pt;margin:1mm 0 .5mm}
.bg{white-space:nowrap}
.a6row{display:flex;justify-content:space-between;gap:2mm}.a6{display:flex;flex-direction:column;align-items:center;font-size:9pt;line-height:1.7}
.wf{width:100%;font-size:8.8pt}.wf td,.wf th{padding:0 1mm;text-align:left}
.antw{font-size:8.6pt}
"""


def blatt():
    s1 = kopf(1) + merk_parallelen() + a1() + a2() + a3() + a4()
    s2 = kopf(2) + merk_dreiecke() + a5() + a6() + a7() + a8()
    return f'<div class="seite">{s1}</div><div class="seite">{s2}</div>'


def main():
    global L
    for loes in (False, True):
        L = loes
        name = BASIS + (" – Lösung" if loes else "")
        html = HIER / f"{name}.html"
        html.write_text(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{name}</title><style>{STIL}</style></head>'
                        f'<body>{blatt()}</body></html>', encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / (name + '.pdf')}",
                        "--virtual-time-budget=3000", html.as_uri()], check=True, capture_output=True)
        print("gedruckt:", name)


if __name__ == "__main__":
    main()
