"""Mathe 7c, Woche 8, Stunde 2: Winkel an Geraden und Winkelsumme (Di 10.11.2026, Doppelstunde, 90 Minuten).

Keine Arbeitsblätter: nur Merkheft, Übungsheft, Buch S. 46 bis 49. Aufgaben abgetippt, Figuren mit stimmenden Winkeln gerechnet.
Aufruf: python3 baue_stunde_geraden_summe.py
"""
import math
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
MATHE = HIER.parents[1]
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(MATHE))
sys.path.insert(0, str(MATHE / "Rationale Zahlen" / "_Skripte"))
from mathe_woche_vorlage import aus_skript, bau_woche  # noqa: E402

EXTRA_W7, rezept_box = aus_skript(MATHE / "Rationale Zahlen" / "_Skripte" / "baue_woche7.py", "EXTRA_CSS", "rezept_box")
NAME = "Mathe 7c – Woche 8 – 2 Winkel an Geraden, Winkelsumme"
ROT, BLAU, LILA, GRUEN, PINK, SCHWARZ = "#d2232a", "#1a78c2", "#8e2a8e", "#3f9a2f", "#E6007E", "#111"
SCHRIFT = "Helvetica, Arial, sans-serif"


def P(x, y, r, a):
    t = math.radians(a)
    return x + r * math.cos(t), y - r * math.sin(t)


def linie(p, q, f=SCHWARZ, b=0.55, extra=""):
    return f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="{f}" stroke-width="{b}" stroke-linecap="round" {extra}/>'


def text(p, s, f=SCHWARZ, g=3.8, fett=True, kursiv=False, anker="middle"):
    return (f'<text x="{p[0]:.2f}" y="{p[1] + g * 0.36:.2f}" font-size="{g}" text-anchor="{anker}" font-family="{SCHRIFT}" fill="{f}"'
            f'{" font-weight=" + chr(34) + "700" + chr(34) if fett else ""}{" font-style=" + chr(34) + "italic" + chr(34) if kursiv else ""}>{s}</text>')


def bogen(S, r, a1, a2, f=ROT, b=0.65, fuell="none"):
    p, q = P(*S, r, a1), P(*S, r, a2)
    gross = 1 if (a2 - a1) % 360 > 180 else 0
    start = f"M{S[0]:.2f} {S[1]:.2f} L" if fuell != "none" else "M"
    ende = " Z" if fuell != "none" else ""
    return f'<path d="{start}{p[0]:.2f} {p[1]:.2f} A{r} {r} 0 {gross} 0 {q[0]:.2f} {q[1]:.2f}{ende}" fill="{fuell}" stroke="{f}" stroke-width="{b}"/>'


def winkel(S, a1, a2, name, f=ROT, r=7.5, g=3.8):
    """Bogen von a1 nach a2 gegen den Uhrzeigersinn, Name auf der Winkelhalbierenden, bei schmalen Winkeln außerhalb des Bogens."""
    s = (a2 - a1) % 360
    lang = len(name) >= 3
    rt = r + (5 if lang else 3) if s < 42 else (r * 0.62 if not lang else r * 0.7)
    if lang and s >= 42:
        r = max(r, 10)
        rt = 6.9
    grad = name.endswith("°")
    return bogen(S, r, a1, a2, f) + text(P(*S, rt, a1 + s / 2), name, f, g, kursiv=not grad)


def gerade(S, a, zurueck, vor, f=SCHWARZ):
    return linie(P(*S, zurueck, a + 180), P(*S, vor, a), f)


def sektoren(S, t, l, namen, r=7.5, g=3.8):
    """Vier Winkel im Schnittpunkt. t und l: Richtungen der beiden Geraden mit t < l < t + 180.
    Reihenfolge gegen den Uhrzeigersinn: (t, l), (l, t+180), (t+180, l+180), (l+180, t+360)."""
    assert t < l < t + 180
    strahlen = [t, l, t + 180, l + 180, t + 360]
    s = ""
    for i, n in enumerate(namen):
        if n:
            name, f = n if isinstance(n, tuple) else (n, ROT)
            s += winkel(S, strahlen[i], strahlen[i + 1], name, f, r, g)
    return s


def svg(inhalt, x0, y0, b, h, breite=None):
    w = breite or b
    return f'<svg style="width:{w}mm;height:{w * h / b:.2f}mm;display:block;max-width:100%" viewBox="{x0} {y0} {b} {h}" xmlns="http://www.w3.org/2000/svg">{inhalt}</svg>'


def schnitt(p, a, q, b):
    """Schnittpunkt der Geraden durch p mit Richtung a und durch q mit Richtung b."""
    d1, d2 = P(0, 0, 1, a), P(0, 0, 1, b)
    n = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((q[0] - p[0]) * d2[1] - (q[1] - p[1]) * d2[0]) / n
    return p[0] + t * d1[0], p[1] + t * d1[1]


def dreieck(alpha, beta, c, ang, ecken=("A", "B", "C"), rand=7, extra=None, r=7.0, xplus=(0, 0)):
    """Dreieck mit Grundseite c (mm) und gerechneten Winkeln. ang: {'A': (Text, Farbe), ...}."""
    gamma = 180 - alpha - beta
    assert gamma > 0
    A, B = (0, 0), (c, 0)
    b = c * math.sin(math.radians(beta)) / math.sin(math.radians(gamma))
    C = P(*A, b, alpha)
    a1 = math.degrees(math.atan2(-(A[1] - C[1]), A[0] - C[0])) % 360
    a2 = math.degrees(math.atan2(-(B[1] - C[1]), B[0] - C[0])) % 360
    assert abs((a2 - a1) % 360 - gamma) < 1e-6
    s = f'<polygon points="0,0 {c},0 {C[0]:.2f},{C[1]:.2f}" fill="none" stroke="{SCHWARZ}" stroke-width="0.6" stroke-linejoin="round"/>'
    for e, S, u, v in (("A", A, 0, alpha), ("B", B, 180 - beta, 180), ("C", C, a1, a2)):
        if e in ang:
            s += winkel(S, u, v, ang[e][0], ang[e][1], r)
    s += text((-3, 2.3), ecken[0], g=3.4, fett=False) + text((c + 3, 2.3), ecken[1], g=3.4, fett=False) + text((C[0], C[1] - 3), ecken[2], g=3.4, fett=False)
    if extra:
        s += extra(A, B, C)
    xs = [0, c, C[0]]
    ys = [0, C[1]]
    x0, x1, y0, y1 = min(xs) - rand - xplus[0], max(xs) + rand + xplus[1], min(ys) - rand, max(ys) + rand
    return svg(s, round(x0, 2), round(y0, 2), round(x1 - x0, 2), round(y1 - y0, 2))


L = '<span class="luecke" contenteditable="true" spellcheck="false"></span>'
LL = '<span class="luecke lang" contenteditable="true" spellcheck="false"></span>'


def lk(l, w, lang=False):
    return f'<span class="luecke{" lang" if lang else ""}">{w}</span>' if l else (LL if lang else L)


def felder(l, paare, spalten=4):
    return (f'<div class="felder" style="grid-template-columns:repeat({spalten},max-content)">'
            + "".join(f'<span class="feld">{n} = {lk(l, w)}</span>' for n, w in paare) + "</div>")


def auftrag(was, schnelle):
    return f'<div class="auftrag zweit"><div><b>Aufgabe:</b> {was}</div><div><b>Für Schnelle:</b> {schnelle}</div></div>'


# ================================================================ Seite 1: Entdecken
def karo(b, h):
    """Kästchen wie im Heft: 5 mm, Zeichnung im Maßstab 1:1."""
    f = "#cbd4de"
    return "".join(linie((x, 0), (x, h), f, 0.2) for x in range(0, b + 1, 5)) + "".join(linie((0, y), (b, y), f, 0.2) for y in range(0, h + 1, 5))


def entdecken(l):
    b, h_ = 125, 85
    S = (60, 42)
    f1 = karo(b, h_) + gerade(S, -12, 55, 58) + gerade(S, 43, 50, 50) + sektoren(S, -12, 43, ["α", "β", "γ", "δ"], 11, 5)
    t = 62
    g, h = (75, 25), (75 - 30 / math.tan(math.radians(t)), 55)     # g und h auf Karolinien, 3 cm = 6 Kästchen
    f2 = (karo(b, h_) + gerade(g, 180, 45, 70) + gerade(h, 180, 60, 55) + linie(P(*h, 26, t + 180), P(*g, 22, t))
          + sektoren(g, t, 180, ["β", "γ", "δ", "α"], 10, 4.6) + sektoren(h, t, 180, ["β′", "γ′", "δ′", "α′"], 10, 4.6)
          + text((118, 21.5), "g", g=4.6, fett=False, kursiv=True) + text((118, 51.5), "h", g=4.6, fett=False, kursiv=True))
    was1 = '<p class="ergebnis lsg">Gegenüber: gleich groß. Daneben: zusammen 180°.</p>' if l else '<p class="ergebnis">Was fällt auf?</p>'
    was2 = '<p class="ergebnis lsg">Nur zwei Größen: 62° und 118°.</p>' if l else '<p class="ergebnis">Welche Winkel sind gleich groß?</p>'
    return (f'<div class="uheft zw2"><div><div class="auftrag"><b>Aufgabe:</b> Ins Übungsheft zwei Geraden zeichnen, die sich schneiden. Alle vier Winkel messen.</div>'
            f'{svg(f1, 0, 0, b, h_)}{felder(l, [("α", "55°"), ("β", "125°"), ("γ", "55°"), ("δ", "125°")], 4)}{was1}</div>'
            f'<div><div class="auftrag"><b>Aufgabe:</b> Zwei parallele Geraden g und h im Abstand von 3 cm zeichnen. Darüber eine schräge Gerade. Alle acht Winkel messen.</div>'
            f'{svg(f2, 0, 0, b, h_)}{felder(l, [("α", "62°"), ("β", "118°"), ("γ", "62°"), ("δ", "118°"), ("α′", "62°"), ("β′", "118°"), ("γ′", "62°"), ("δ′", "118°")], 4)}{was2}</div></div>')


# ================================================================ Merkheft 1
def mini(art):
    S1, S2 = (10, 27), (31, 15)
    t = math.degrees(math.atan2(-(S2[1] - S1[1]), S2[0] - S1[0]))
    if art in ("scheitel", "neben"):
        S = (22, 18)
        s = gerade(S, -22, 21, 21) + gerade(S, 24, 21, 21)
        namen = [("α", ROT), None, ("γ", ROT), None] if art == "scheitel" else [("α", BLAU), ("β", BLAU), None, None]
        return svg(s + sektoren(S, -22, 24, namen, 9), 0, 0, 44, 36, 48)
    s = gerade(S1, 78, 13, 13) + gerade(S2, 78, 13, 13) + linie(P(*S1, 8, t + 180), P(*S2, 10, t))
    s += text((P(*S1, 13, 78)[0] + 3, 15), "g", g=3.3, fett=False, kursiv=True) + text((P(*S2, 13, 78)[0] + 3.2, 3), "h", g=3.3, fett=False, kursiv=True)
    if art == "stufen":
        s += sektoren(S1, t, 78, [("α", LILA), None, None, None], 9) + sektoren(S2, t, 78, [("α′", LILA), None, None, None], 9)
    else:
        s += sektoren(S1, t, 78, [("α", GRUEN), None, None, None], 9) + sektoren(S2, t, 78, [None, None, ("γ′", GRUEN), None], 9)
    return svg(s, 0, 0, 44, 40, 48)


def merk_geraden():
    t, g_a = 8, 73
    S1, S2 = (24, 26), P(24, 26, 50, 8)
    s = (gerade(S1, g_a, 22, 23) + gerade(S2, g_a, 22, 23) + linie(P(*S1, 17, t + 180), P(*S2, 17, t))
         + sektoren(S1, t, g_a, [("65°", SCHWARZ), "β", "γ", "δ"], 7.5) + sektoren(S2, t, g_a, ["α′", "β′", "γ′", "δ′"], 7.5)
         + text((P(*S1, 22, g_a)[0] + 3, 5), "g", g=3.5, fett=False, kursiv=True) + text((P(*S2, 22, g_a)[0] + 3.5, 0), "h", g=3.5, fett=False, kursiv=True)
         + text((53, 49), "g || h", g=3.4, fett=False))
    karten = [("scheitel", ROT, "Scheitelwinkel", "gegenüber", "gleich groß", "γ = α"), ("neben", BLAU, "Nebenwinkel", "daneben", "zusammen 180°", "α + β = 180°"),
              ("stufen", LILA, "Stufenwinkel", "gestuft", "gleich groß", "α = α′"), ("wechsel", GRUEN, "Wechselwinkel", "über Kreuz", "gleich groß", "α = γ′")]
    oben = "".join(f'<div class="wk"><b style="color:{f}">{n}</b>{mini(a)}<div>{wo}</div><div><b>{r}</b></div><div style="color:{f};font-weight:700">{gl}</div></div>'
                   for a, f, n, wo, r, gl in karten)
    links = ('<div class="bsp">' + svg(s, 0, -3, 92, 56, 84) + '<div><div class="mz"><span class="sn">1</span><span>Bekannt: α = 65°</span></div>'
             '<div class="mz"><span class="sn">2</span><span>β liegt daneben: Nebenwinkel</span></div>'
             '<div class="mz"><span class="sn">3</span><span>β = 180° − 65° = <span class="rot">115°</span></span></div></div></div>')
    rez = rezept_box("Winkel an Geraden", ["Bekannten Winkel suchen.", "Lage prüfen: gegenüber, daneben, gestuft oder über Kreuz?", "Daneben: 180° minus. Sonst: gleich groß."])
    w = ["γ gegenüber von α: γ = 65°", "δ gegenüber von β: δ = 115°", "α′ gestuft zu α: α′ = 65°", "γ′ über Kreuz zu α: γ′ = 65°", "β′ gestuft zu β: β′ = 115°", "δ′ über Kreuz zu β: δ′ = 115°"]
    assert 180 - 65 == 115
    return (f'<div class="heft"><div class="wk4">{oben}</div><p class="merkk">Stufen- und Wechselwinkel sind nur bei parallelen Geraden (g || h) gleich groß.</p>'
            f'<div class="mb"><div>{links}</div>{rez}</div><div class="weitere"><div class="weitere-t">Weitere Beispiele</div>' + "".join(f'<div class="wz">{x}</div>' for x in w) + "</div></div>")


# ================================================================ Übung Geraden
def fig_paar(t, l, abst, namen1, namen2, labels, x0, y0, b, h, S1, zur=(14, 14), lin=(16, 16), r=7, breite=None):
    S2 = P(*S1, abst, t)
    enden = (P(*S1, zur[0], t + 180), P(*S2, zur[1], t)) if abst > 0 else (P(*S2, zur[1], t + 180), P(*S1, zur[0], t))
    s = (gerade(S1, l, *lin) + gerade(S2, l, *lin) + linie(*enden)
         + sektoren(S1, t, l, namen1, r) + sektoren(S2, t, l, namen2, r) + labels(S1, S2))
    return svg(s, x0, y0, b, h, breite)


def zeile(l, davor, w, danach=""):
    return f'<div class="azeile">{davor} {lk(l, w, True)} {danach}</div>'


def g_lab(S1, S2, l, d=(15, 3), p=(30, 44)):
    q1, q2 = P(*S1, 16, l + 180), P(*S2, 16, l + 180)
    return (text((q1[0] + d[0] - 12, q1[1] + 3), "g", g=3.4, fett=False, kursiv=True) + text((q2[0] + d[0] - 12, q2[1] + 3), "h", g=3.4, fett=False, kursiv=True)
            + text(p, "g || h", g=3.3, fett=False))


def blk(titel, fig, rechts, unten=""):
    return f'<div class="blk"><div class="nr">{titel}</div><div class="blk-i">{fig}<div class="blk-r">{rechts}</div></div>{unten}</div>'


def stapel(titel, fig, unten):
    return f'<div class="stapel"><div class="nr">{titel}</div><div class="mitte3">{fig}</div>{unten}</div>'


def uebung_geraden(l):
    N = ["α", "β", "γ", "δ"]
    NS = ["α′", "β′", "γ′", "δ′"]
    n1 = fig_paar(-3, 33, 46, N, NS, lambda a, b: g_lab(a, b, 33, p=(38, 40)), 0, 0, 82, 45, (16, 20), zur=(12, 14), breite=80)
    n2 = fig_paar(-3, 27, 46, [("30°", SCHWARZ), "β", "γ", "δ"], NS, lambda a, b: g_lab(a, b, 27, p=(38, 40)), 0, 0, 82, 45, (16, 20), zur=(12, 14), breite=80)
    a_ = fig_paar(-20, 31, 50, N, NS, lambda a, b: g_lab(a, b, 31, p=(46, 12)), 0, 0, 82, 52, (15, 15), zur=(12, 12), breite=68)
    b_ = fig_paar(17, 127, 50, [None, ("70°", SCHWARZ), "γ", "δ"], ["α′", "β′", None, "δ′"], lambda a, b: g_lab(a, b, 127, d=(16, 3), p=(50, 45)), 0, 0, 82, 54, (17, 40), zur=(12, 12), breite=62)
    z = lambda t, w: f'<div class="azeile">{t} {lk(l, w, True)}</div>'
    a1 = '<div class="zeilen2">' + "".join(z(t, w) for t, w in (("a) α und γ", "Scheitelwinkel"), ("b) α′ und α", "Stufenwinkel"), ("c) β und δ", "Scheitelwinkel"), ("d) β′ und δ", "Wechselwinkel"))) + "</div>"
    a2 = '<div class="zeilen2">' + "".join(f'<div class="azeile klein2">{v} {lk(l, w)} sind {n}.</div>' for v, w, n in (("a) β und", "δ", "Scheitelwinkel"), ("b) γ und", "β, δ", "Nebenwinkel"), ("c) α und", "α′", "Stufenwinkel"), ("d) δ und", "β′", "Wechselwinkel"))) + "</div>"
    bb = '<div class="azeile2 klein2">b) Zwei Möglichkeiten für δ′:' + (' <span class="lsg">Scheitelwinkel von β′, Stufenwinkel von δ.</span>' if l else "") + "</div>"
    return (auftrag("Buch S. 46 Nr. 1, Nr. 2 und S. 47 Nr. A ins Übungsheft.", "Buch S. 47 Nr. B")
            + '<div class="uheft zw2 kompakt">'
            + stapel("○ S. 46 Nr. 1: Wie heißen die zwei Winkel?", n1, a1)
            + stapel("○ S. 46 Nr. 2: Wie groß sind die Winkel?", n2, felder(l, [("β", "150°"), ("γ", "30°"), ("δ", "150°"), ("α′", "30°"), ("β′", "150°"), ("γ′", "30°"), ("δ′", "150°")], 4))
            + stapel("S. 47 Nr. A: Gib den richtigen Winkel an.", a_, a2)
            + stapel("S. 47 Nr. B: Für Schnelle", b_, felder(l, [("γ", "110°"), ("δ", "70°"), ("α′", "110°"), ("β′", "70°"), ("δ′", "70°")], 3) + bb)
            + "</div>")


def weitere_geraden(l):
    a = fig_paar(34.3, 169.3, -36, [("135°", SCHWARZ), None, "α", None], ["β", None, None, None],
                 lambda s1, s2: text(P(*s1, 30, -10.7), "g", g=3.4, fett=False, kursiv=True) + text(P(*s2, 31, -10.7), "h", g=3.4, fett=False, kursiv=True),
                 0, 0, 82, 54, (50, 17), zur=(15, 15), lin=(28, 19), r=8, breite=92)
    b = fig_paar(-10, 90, 42, [("β", ROT), None, None, ("80°", SCHWARZ)], [None, "α", None, None],
                 lambda s1, s2: text((s1[0] + 3, 47), "g", g=3.4, fett=False, kursiv=True) + text((s2[0] + 3, 54), "h", g=3.4, fett=False, kursiv=True),
                 0, 0, 82, 56, (16, 24), zur=(11, 18), lin=(21, 21), r=8, breite=88)
    # orange Nr. 5: g, h senkrecht, i, k fallen mit 20 Grad
    gA, hA = (20, 16), (58, 16 + 38 * math.tan(math.radians(20)))
    gB, hB = (20, 42), (58, 42 + 38 * math.tan(math.radians(20)))
    n5 = (gerade(gA, -20, 13, 53) + gerade(gB, -20, 13, 53) + linie((20, 5), (20, 57)) + linie((58, 16), (58, 75))
          + winkel(gA, 270, 340, "γ") + winkel(hA, 270, 340, "β") + winkel(gB, 90, 160, "δ") + winkel(gB, 340, 450, "ε")
          + winkel(hB, 90, 160, "70°", SCHWARZ) + winkel(hB, 340, 450, "α")
          + text((8, 8), "i", g=3.4, fett=False, kursiv=True) + text((7, 33), "k", g=3.4, fett=False, kursiv=True) + text((23, 57), "g", g=3.4, fett=False, kursiv=True) + text((61, 74), "h", g=3.4, fett=False, kursiv=True))
    # grün Nr. 4: Viereck
    g_, h_, k_ = 9, 9, 74
    Pu = (24, 56)
    Q = P(*Pu, 42, h_)
    R = P(*Pu, 40, k_)
    T = schnitt(R, g_, Q, k_)
    vk = (f'<polygon points="{Pu[0]:.2f},{Pu[1]:.2f} {Q[0]:.2f},{Q[1]:.2f} {T[0]:.2f},{T[1]:.2f} {R[0]:.2f},{R[1]:.2f}" fill="#fde2ae"/>'
          + gerade(R, g_, 17, 56) + gerade(Pu, h_, 17, 58) + gerade(Pu, k_, 9, 50) + gerade(Q, k_, 9, 50)
          + winkel(Pu, 9, 74, "65°", SCHWARZ) + winkel(Q, 74, 189, "β") + bogen(Q, 6, 9, 74, BLAU) + winkel(T, 189, 254, "γ") + winkel(R, 254, 369, "δ")
          + text((P(*R, 15, 189)[0], P(*R, 15, 189)[1] - 3), "g", g=3.4, fett=False, kursiv=True) + text((P(*Pu, 15, 189)[0], P(*Pu, 15, 189)[1] + 4), "h", g=3.4, fett=False, kursiv=True)
          + text((P(*Pu, 8, 254)[0] + 3, P(*Pu, 8, 254)[1]), "i", g=3.4, fett=False, kursiv=True) + text((P(*Q, 8, 254)[0] + 3.5, P(*Q, 8, 254)[1]), "k", g=3.4, fett=False, kursiv=True))
    b4 = ('<div class="azeile2 lsg">β = 115°: Nebenwinkel vom blauen Winkel, der ist als Stufenwinkel 65°.<br>γ = 65°: Wechselwinkel zum blauen Winkel.<br>δ = 115°: Nebenwinkel von einem 65°-Stufenwinkel.</div>' if l
          else felder(l, [("β", ""), ("γ", ""), ("δ", "")], 2) + '<div class="azeile2">Begründe.</div>')
    n55 = '<div class="azeile2 lsg">Nr. 5: 90° und 120° (Nebenwinkel 60°).</div>' if l else ""
    return (auftrag("Buch S. 47 orange Nr. 3 und Nr. 5 ins Übungsheft.", "Buch S. 47 grün Nr. 4 und Nr. 5")
            + '<div class="uheft zw2">'
            + blk("○ S. 47 orange Nr. 3 a): Wie groß sind α und β?", a, felder(l, [("α", "135°"), ("β", "135°")], 1))
            + blk("○ S. 47 orange Nr. 3 b)", b, felder(l, [("α", "80°"), ("β", "100°")], 1))
            + blk("◐ S. 47 orange Nr. 5 (i || k, g || h)", svg(n5, 0, 0, 82, 78, 78), felder(l, [("α", "110°"), ("β", "70°"), ("γ", "70°"), ("δ", "70°"), ("ε", "110°")], 2))
            + blk("Für Schnelle: S. 47 grün Nr. 4 (g || h, i || k)", svg(vk, 0, 0, 86, 76, 70), b4 + n55)
            + "</div>")


# ================================================================ Einstieg Winkelsumme
def fuell_dreieck():
    F = {"α": "#fbd5d5", "β": "#cfe3f6", "γ": "#fdeeb0"}
    al, be = 50, 60
    c = 62
    b = c * math.sin(math.radians(be)) / math.sin(math.radians(70))
    C = P(0, 0, b, al)
    return F, al, be, c, C


def ecken(l):
    F, al, be, c, C = fuell_dreieck()
    d = (f'<polygon points="0,0 {c},0 {C[0]:.2f},{C[1]:.2f}" fill="none" stroke="{SCHWARZ}" stroke-width="0.6" stroke-linejoin="round"/>'
         + bogen((0, 0), 11, 0, al, ROT, 0.5, F["α"]) + text(P(0, 0, 7.3, al / 2), "α", ROT, kursiv=True)
         + bogen((c, 0), 11, 180 - be, 180, BLAU, 0.5, F["β"]) + text(P(c, 0, 7.3, 180 - be / 2), "β", BLAU, kursiv=True)
         + bogen(C, 11, 180 + al, 180 + al + 70, "#b38600", 0.5, F["γ"]) + text(P(*C, 7.3, 180 + al + 35), "γ", "#8a6700", kursiv=True))
    dd = svg(d, -6, round(C[1] - 5, 2), c + 12, round(-C[1] + 10, 2), 105 if l else 165)
    if not l:
        return ('<div class="uheft"><div class="auftrag"><b>Aufgabe:</b> Auf Schmierpapier ein großes Dreieck zeichnen. Winkel bunt markieren. Die drei Ecken abreißen und an einem Punkt zusammenlegen.</div>'
                f'<div class="mitte">{dd}</div><p class="ergebnis" style="font-size:28px;text-align:center">Was fällt auf?</p></div>')
    O = (40, 26)
    leg = (bogen(O, 22, 0, be, BLAU, 0.5, F["β"]) + bogen(O, 22, be, be + 70, "#b38600", 0.5, F["γ"]) + bogen(O, 22, be + 70, 180, ROT, 0.5, F["α"])
           + linie((6, 26), (74, 26), SCHWARZ, 0.7) + text(P(*O, 14, be / 2), "β", BLAU, g=4.6, kursiv=True) + text(P(*O, 14, be + 35), "γ", "#8a6700", g=4.6, kursiv=True) + text(P(*O, 14, be + 70 + 25), "α", ROT, g=4.6, kursiv=True))
    C2 = (C[0] + 10, 0)
    A2, B2 = (10, -C[1]), (c + 10, -C[1])
    w = (linie((C2[0] - 28, 0), (C2[0] + 34, 0), SCHWARZ, 0.6) + f'<polygon points="{A2[0]},{A2[1]:.2f} {B2[0]},{B2[1]:.2f} {C2[0]:.2f},0" fill="none" stroke="{SCHWARZ}" stroke-width="0.6" stroke-linejoin="round"/>'
         + winkel(A2, 0, al, "α", ROT, 8) + winkel(B2, 180 - be, 180, "β", BLAU, 8)
         + winkel(C2, 180, 180 + al, "α′", ROT, 11) + winkel(C2, 180 + al, 250 + al, "γ", "#8a6700", 11) + winkel(C2, 300, 360, "β′", BLAU, 11)
         + text((C2[0], -3), "C", g=3.4, fett=False) + text((A2[0] - 3, A2[1] + 2), "A", g=3.4, fett=False) + text((B2[0] + 3, B2[1] + 2), "B", g=3.4, fett=False))
    return ('<div class="uheft"><div class="auftrag"><b>Aufgabe:</b> Auf Schmierpapier ein großes Dreieck zeichnen. Winkel bunt markieren. Die drei Ecken abreißen und an einem Punkt zusammenlegen.</div>'
            f'<div class="zw2"><div class="mitte2">{dd}</div><div class="mitte2">{svg(leg, 0, 0, 80, 30, 118)}<p class="ergebnis lsg" style="font-size:24px;text-align:center">Die drei Ecken ergeben einen gestreckten Winkel: 180°.</p></div></div></div>'
            f'<h4 style="font-size:20px;margin:3mm 0 1mm">Warum? Parallele durch C</h4><div class="fig-rechts">{svg(w, 0, -6, 92, round(-C[1] + 12, 2), 92)}'
            '<div class="warum2"><div>Wechselwinkel:</div><div class="lsg">α′ = α</div><div class="lsg">β′ = β</div><div style="margin-top:3mm">Gestreckter Winkel bei C:</div><div class="lsg">α + γ + β = 180°</div></div></div>')


# ================================================================ Merkheft 2
BSP = [("α = 90°, β = 35°", 90, 35, "γ", 55), ("α = 120°, γ = 25°", 120, 25, "β", 35), ("β = 48°, γ = 62°", 48, 62, "α", 70),
       ("α = 20°, β = 20°", 20, 20, "γ", 140), ("α = 60°, β = 60°", 60, 60, "γ", 60), ("α = 38,5°, β = 41,5°", 38.5, 41.5, "γ", 100)]
for _t, _a, _b, _n, _e in BSP:
    assert 180 - _a - _b == _e, _t


def merk_summe():
    fig = dreieck(65, 45, 82, {"A": ("65°", SCHWARZ), "B": ("45°", SCHWARZ), "C": ("γ", ROT)}, rand=8)
    assert 65 + 45 == 110 and 180 - 110 == 70
    links = ('<div class="bsp">' + fig + '<div><div class="mz"><span class="sn">1</span><span>Gesucht: γ</span></div>'
             '<div class="mz"><span class="sn">2</span><span>65° + 45° = <span class="gelb">110°</span></span></div>'
             '<div class="mz"><span class="sn">3</span><span>γ = 180° − <span class="gelb">110°</span> = <span class="rot">70°</span></span></div>'
             '<div class="mz"><span class="sn">4</span><span>Probe: 65° + 45° + 70° = 180°</span></div></div></div>')
    rez = rezept_box("Fehlender Winkel im Dreieck", ["Was fehlt?", "Die zwei bekannten Winkel addieren.", "Von 180° abziehen.", "Probe: Alle drei ergeben 180°."])
    w = "".join(f'<div class="wz">{t}: {n} = {str(e)}°</div>' for t, _, _, n, e in BSP)
    return ('<div class="heft merk2"><div class="merksatz">In jedem Dreieck gilt: α + β + γ = 180°</div>'
            f'<div class="mb"><div>{links}</div>{rez}</div><div class="weitere"><div class="weitere-t">Weitere Beispiele</div>{w}</div></div>')


# ================================================================ Übung Winkelsumme
def uebung_summe(l):
    S, R = SCHWARZ, ROT
    n1 = [("a)", dreieck(60, 75, 31, {"A": ("60°", S), "B": ("75°", S), "C": ("γ", R)}, rand=6, r=5.5), "γ", "45°"),
          ("b)", dreieck(25, 120, 42, {"A": ("α", R), "B": ("120°", S), "C": ("35°", S)}, rand=6, r=5.5), "α", "25°"),
          ("c)", dreieck(54, 36, 44, {"A": ("54°", S), "B": ("36°", S), "C": ("γ", R)}, rand=6, r=5.5), "γ", "90°"),
          ("d)", dreieck(70, 70, 24, {"A": ("70°", S), "B": ("β", R), "C": ("40°", S)}, rand=6, r=5), "β", "70°")]
    assert 180 - 60 - 75 == 45 and 180 - 120 - 35 == 25 and 180 - 54 - 36 == 90 and 180 - 70 - 40 == 70
    reihe = "".join(f'<div class="dz"><div class="dfig"><b>{a}</b>{f}</div><div class="feld">{n} = {lk(l, e)}</div></div>' for a, f, n, e in n1)
    fA = dreieck(48, 62, 32, {"A": ("48°", S), "B": ("62°", S), "C": ("γ", R)}, rand=6, r=6)
    fB = dreieck(25, 20, 40, {"A": ("α", R), "B": ("20°", S), "C": ("135°", S)}, rand=6, r=6)
    f3 = dreieck(48, 35, 36, {"A": ("48°", S), "B": ("β", R), "C": ("97°", S)}, rand=6, r=6)
    assert 180 - 48 - 62 == 70 and 180 - 20 - 135 == 25 and 180 - 97 - 48 == 35
    T = [("60°", "50°", None, 70), ("52°", None, "67°", 61), (None, "11°", "16°", 153), ("71°", None, "89°", 20), ("137°", "42°", None, 1)]
    for a, b, g, e in T:
        s = sum(int(x[:-1]) for x in (a, b, g) if x)
        assert 180 - s == e, (a, b, g)
    tz = lambda i, name: f"<tr><th>{name}</th>" + "".join(f'<td>{r[i] if r[i] else lk(l, str(r[3]) + "°")}</td>' for r in T) + "</tr>"
    tab = '<table class="wt"><tr><th></th><th>a)</th><th>b)</th><th>c)</th><th>d)</th><th>e)</th></tr>' + tz(0, "α") + tz(1, "β") + tz(2, "γ") + "</table>"
    return (auftrag("Buch S. 48 Nr. 1, S. 49 Nr. A und orange Nr. 3, Nr. 4 ins Übungsheft.", "Buch S. 48 Nr. 2: Dreieck abzeichnen, messen, mit der Winkelsumme prüfen.")
            + '<div class="uheft">'
            f'<div class="nr">○ S. 48 Nr. 1: Berechne den fehlenden Winkel.</div><div class="dr4">{reihe}</div>'
            '<div class="zeile3"><div><div class="nr">S. 49 Nr. A und orange Nr. 3: Berechne den fehlenden Winkel.</div><div class="dr3">'
            f'<div class="dz"><div class="dfig"><b>A a)</b>{fA}</div><div class="feld">γ = {lk(l, "70°")}</div></div>'
            f'<div class="dz"><div class="dfig"><b>A b)</b>{fB}</div><div class="feld">α = {lk(l, "25°")}</div></div>'
            f'<div class="dz"><div class="dfig"><b>Nr. 3</b>{f3}</div><div class="feld">β = {lk(l, "35°")}</div></div></div></div>'
            f'<div><div class="nr">○ S. 49 orange Nr. 4: Ein Winkel fehlt.</div>{tab}</div></div></div>')


def weitere_summe(l):
    S, R = SCHWARZ, ROT

    def aus_a(A, B, C):
        return linie((-16, 0), (0, 0), S, 0.6) + winkel(A, 55, 180, "125°", S, 8)

    def aus_b(A, B, C):
        return (linie((-18, 0), (0, 0), S, 0.6) + linie((30, 0), (48, 0), S, 0.6)
                + winkel(A, 110, 180, "70°", S, 8) + winkel(B, 0, 140, "140°", S, 8))

    fa = dreieck(55, 40, 40, {"A": ("α", R), "B": ("40°", S), "C": ("γ", R)}, rand=7, extra=aus_a, r=6, xplus=(12, 0))
    fb = dreieck(110, 40, 30, {"A": ("α", R), "B": ("β", R), "C": ("γ", R)}, rand=7, extra=aus_b, r=6, xplus=(13, 13))
    assert 180 - 125 == 55 and 180 - 55 - 40 == 85 and 180 - 70 == 110 and 180 - 140 == 40 and 180 - 110 - 40 == 30
    # orange Nr. 6: abgeschnittene Ecken
    a, b = 44, 61
    c = 90
    gam = 180 - a - b
    assert 180 - 77 - 59 == 44 and 180 - 71 - 48 == 61 and 180 - 44 - 61 == 75
    A, B = (0, 0), (c, 0)
    C = P(*A, c * math.sin(math.radians(b)) / math.sin(math.radians(gam)), a)
    P1 = (22, 0)
    P2 = P(*A, 22 * math.sin(math.radians(59)) / math.sin(math.radians(77)), a)
    Q1 = (c - 20, 0)
    Q2 = P(*B, 20 * math.sin(math.radians(48)) / math.sin(math.radians(71)), 180 - b)
    rich = lambda p, q: math.degrees(math.atan2(p[1] - q[1], q[0] - p[0])) % 360
    assert abs((rich(P2, P1) - (a - 103)) % 360) < 1e-6 and abs((rich(Q2, Q1) - (180 - b + 109)) % 360) < 1e-6
    # Riss oben: fest vorgegebene Zacken zwischen P2' und Q2'
    h = 0.62
    U = (P2[0] + (C[0] - P2[0]) * h, P2[1] + (C[1] - P2[1]) * h)
    V = (Q2[0] + (C[0] - Q2[0]) * h, Q2[1] + (C[1] - Q2[1]) * h)
    z = [0.8, -1.1, 0.5, -0.7, 1.2, -0.9, 0.7, -1.2, 0.6]
    riss = [(U[0] + (V[0] - U[0]) * (i + 1) / 10, U[1] + (V[1] - U[1]) * (i + 1) / 10 + z[i]) for i in range(9)]
    pts = [P1, Q1, Q2, V] + riss[::-1] + [U, P2]
    poly = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    grau = "#9aa3ad"
    innen = lambda S, u, v, n: bogen(S, 5, u, v, BLAU) + text(P(*S, 10, (u + v) / 2), n, BLAU, 3.5)
    f6 = (f'<polygon points="0,0 {c},0 {C[0]:.2f},{C[1]:.2f}" fill="none" stroke="{grau}" stroke-width="0.4"/>'
          f'<polygon points="{poly}" fill="#dfe7f2" stroke="{S}" stroke-width="0.6" stroke-linejoin="round"/>'
          + innen(P1, 0, 121, "121°") + innen(Q1, 48, 180, "132°") + innen(P2, a - 103, a, "103°") + innen(Q2, 180 - b, 180 - b + 109, "109°"))
    if l:
        f6 += (text((10, -3), "44°", PINK, 3.5) + text((c - 8, -3), "61°", PINK, 3.5) + text((C[0], C[1] + 8), "75°", PINK, 3.5))
    return (auftrag("Buch S. 49 orange Nr. 5 und Nr. 6 ins Übungsheft.", "Buch S. 49 grün Nr. 6")
            + '<div class="uheft zw2"><div><div class="nr">◐ S. 49 orange Nr. 5: Berechne die fehlenden Winkel.</div><div class="zw">'
            f'<div><b>a)</b>{fa}{felder(l, [("α", "55°"), ("γ", "85°")], 2)}</div><div><b>b)</b>{fb}{felder(l, [("α", "110°"), ("β", "40°"), ("γ", "30°")], 2)}</div></div>'
            '<div class="azeile2">Mit welcher Art von Winkeln hast du die Lösung gefunden?' + (' <span class="lsg">Nebenwinkel.</span>' if l else "") + "</div>"
            '<div class="nr" style="margin-top:4mm">Für Schnelle: S. 49 grün Nr. 6</div>'
            '<div class="azeile2">Ein Dreieck hat die Winkel α = 38,7° und β = 45,7°. a) Berechne γ. b) Runde die drei Winkel auf ganze Grad. Erkläre, was dir auffällt.</div>'
            + ('<div class="azeile2 lsg">γ = 95,6°. Gerundet: 39° + 46° + 96° = 181°. Durch das Runden stimmt die Summe nicht mehr.</div>' if l else "")
            + '</div><div><div class="nr">◐ S. 49 orange Nr. 6: Zwei Ecken wurden abgeschnitten, die dritte abgerissen. Wie groß waren die Winkel des Dreiecks?</div>'
            f'{svg(f6, -6, round(C[1] - 4, 2), c + 12, round(-C[1] + 9, 2), 118)}{felder(l, [("links", "44°"), ("rechts", "61°"), ("oben", "75°")], 3)}</div></div>')


EXTRA = EXTRA_W7 + """<style>
.luecke.lang{min-width:39mm!important}
.zw2{display:grid;grid-template-columns:1fr 1fr;gap:4mm 6mm}.zw2>div{min-width:0}
.blk-i{display:flex;gap:3mm;align-items:center}.blk-i svg{flex:none}.blk-r{min-width:0}
.blk .luecke.lang{min-width:36mm!important;font-size:15px}.blk .feld{font-size:18px}.klein2{font-size:14.5px!important}
.bsp{display:flex;gap:5mm;align-items:center}
.auftrag.zweit{display:flex;gap:0 9mm;flex-wrap:wrap;padding:4px 13px}
.kompakt .luecke{height:10mm!important;margin:.5mm 2mm!important}
.stapel{min-width:0}.mitte3{display:flex;justify-content:center}.zeilen2{display:grid;grid-template-columns:1fr 1fr;gap:0 3mm}.stapel .felder{justify-content:center}
.stapel .luecke.lang{min-width:39mm!important;font-size:15px}
.zeile3{display:grid;grid-template-columns:1fr auto;gap:5mm;margin-top:3mm;align-items:start}
.merk2 .mz{margin:3mm 0}.merk2 .weitere{margin-top:7mm}.merk2 .wz{font-size:19px!important}.merk2 .merksatz{padding:14px;font-size:36px}
.sgrid{display:grid;grid-template-columns:1fr auto;gap:3mm 6mm}
.mitte2{display:flex;flex-direction:column;align-items:center;justify-content:center}
.auftrag{background:#f4f6f9;border:2px solid #1b1b1b;border-radius:8px;padding:6px 13px;margin:0 0 9px;font-size:17px}
.felder{display:grid;gap:1mm 7mm;align-items:center}.feld{font-size:19px;font-weight:700;white-space:nowrap}
.fig-rechts{display:flex;gap:9mm;align-items:center;justify-content:center;margin:2mm 0}
.mitte{display:flex;justify-content:center;margin:1mm 0 2mm}
.ergebnis{font-size:20px;font-weight:700;margin:2mm 0}
.lsg{color:#E6007E;font-weight:700}
.wk4{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}.wk{text-align:center;font-size:16px;line-height:1.25}.wk svg{margin:1mm auto}.wk>b:first-child{font-size:17px}
.merkk{margin:3mm 0;font-size:16px;font-weight:600}
.merksatz{font-size:32px;font-weight:800;text-align:center;border:2.5px solid #1a56a0;background:#eef3fb;border-radius:8px;padding:9px;margin:0 0 5mm}
.wz{font-size:18px!important}.weitere{grid-template-columns:repeat(2,1fr)!important}
.zw{display:grid;grid-template-columns:1fr 1fr;gap:3mm 7mm}.zw>div{min-width:0}.zw .felder{gap:.5mm 3mm}.zw .feld{font-size:17px}.nr{font-weight:700;font-size:16px;margin:0 0 1mm}.zw .nr{font-size:14.5px}
.azeile{font-size:17px;white-space:nowrap;margin:.5mm 0}.azeile2{font-size:16px;margin-top:1mm}
.dr4{display:grid;grid-template-columns:repeat(4,auto);gap:3mm;justify-content:space-between;align-items:end}.dr3{display:grid;grid-template-columns:repeat(3,auto);gap:3mm;justify-content:space-between;align-items:end}
.dz{display:flex;flex-direction:column;align-items:center}.dfig{display:flex;gap:1mm;align-items:flex-start}.dfig b{white-space:nowrap}
#t_tafel .mb,#t_merk .mb,.heft .mb{grid-template-columns:2.7fr 1fr;gap:5mm}.heft .weitere{grid-template-columns:repeat(3,1fr)!important;margin-top:3mm}.heft .wz{font-size:16.5px!important}.heft .mz span:last-child{white-space:nowrap}.dfig svg{max-width:none!important;flex:none}
table.wt{border-collapse:collapse;font-size:18px;margin-top:1mm}.wt td,.wt th{border:1px solid #9aa3ad;padding:0 1mm;text-align:center;height:14mm;min-width:15mm}.wt th{background:#eef1f5}.wt tr:first-child th{height:8mm}
.wt .luecke{margin:0!important}
.warum2{font-size:19px;font-weight:600;line-height:1.5}
</style>"""

FOLIEN = [
    ("Zwei Geraden: Was fällt auf?", entdecken(False)),
    ("Zwei Geraden: Was fällt auf? (ausgefüllt)", entdecken(True)),
    ("Merkheft: Winkel an Geraden", merk_geraden()),
    ("Winkel an Geraden üben", uebung_geraden(False)),
    ("Winkel an Geraden üben (ausgefüllt)", uebung_geraden(True)),
    ("Weitere Aufgaben: Winkel an Geraden", weitere_geraden(False)),
    ("Weitere Aufgaben: Winkel an Geraden (ausgefüllt)", weitere_geraden(True)),
    ("Dreieck: Ecken abreißen", ecken(False)),
    ("Dreieck: Ecken abreißen (ausgefüllt)", ecken(True)),
    ("Merkheft: Winkelsumme im Dreieck", merk_summe()),
    ("Winkelsumme üben", uebung_summe(False)),
    ("Winkelsumme üben (ausgefüllt)", uebung_summe(True)),
    ("Weitere Aufgaben und Hausaufgabe", weitere_summe(False)),
    ("Weitere Aufgaben und Hausaufgabe (ausgefüllt)", weitere_summe(True)),
]
QUER = {t for t, _ in FOLIEN}
LEISTE = [("Winkel an Geraden", "Entdecken", 8), ("Winkel an Geraden", "Entdecken", None), ("Winkel an Geraden", "Merkheft", None),
          ("Winkel an Geraden", "Üben", 15), ("Winkel an Geraden", "Üben", None), ("Winkel an Geraden", "Weitere", 10), ("Winkel an Geraden", "Weitere", None),
          ("Winkelsumme", "Ecken abreißen", 5), ("Winkelsumme", "Ecken abreißen", None), ("Winkelsumme", "Merkheft", None),
          ("Winkelsumme", "Üben", 15), ("Winkelsumme", "Üben", None), ("Winkelsumme", "Weitere", 10), ("Winkelsumme", "Weitere", None)]

SCHRITTE = [
    ("", "Winkel messen und entdecken", 12, "Übungsheft. Zwei Geraden, dann Parallelen. Werte eintragen, Klasse sagt, was auffällt.", [1, 2]),
    ("", "Merkheft: Winkel an Geraden", 12, "Vier Winkelpaare mit Bild und Beispiel abschreiben, Paare farbig.", [3]),
    ("", "Üben ○", 15, "S. 46 Nr. 1, 2 und S. 47 Nr. A. Schnelle: Nr. B. Merkheft offen.", [4, 5]),
    ("", "Weitere Aufgaben", 10, "S. 47 orange Nr. 3 und Nr. 5. Schnelle: grün Nr. 4 und 5.", [6, 7]),
    ("", "Ecken abreißen", 8, "Schmierpapier. Ecken an einem Punkt zusammenlegen. Danach die Parallele durch C: Wechselwinkel zeigen, warum es immer 180° sind.", [8, 9]),
    ("", "Merkheft: Winkelsumme", 8, "Merksatz, Beispiel und Rezept abschreiben.", [10]),
    ("", "Üben ○", 15, "S. 48 Nr. 1, S. 49 Nr. A, orange Nr. 3 und 4. Schnelle: S. 48 Nr. 2.", [11, 12]),
    ("", "Weitere Aufgaben, Puffer", 10, "S. 49 orange Nr. 5 und 6. Schnelle: grün Nr. 6. Rest kann Hausaufgabe werden.", [13, 14]),
]
assert sum(s[2] for s in SCHRITTE) == 90


def box(t, h):
    return f'<div class="box"><h3>{t}</h3>{h}</div>'


def main():
    vb = [("Drucken", "Nichts. Keine Arbeitsblätter: Merkheft, Übungsheft und Buch."),
          ("Mitbringen", "Geodreieck, Buntstifte, Schmierpapier zum Abreißen (ein Blatt pro Schüler)."),
          ("Digital", "Folien-PDF aufs iPad (alle Seiten quer), an den Kästchen schreibst du die Werte der Klasse hinein."),
          ("Raum", "Doppelstunde, 90 Minuten. Mittwoch geht es mit Dreiecksformen (S. 50) weiter.")]
    merk = box("Eintrag 1: Winkel an Geraden", merk_geraden()) + box("Eintrag 2: Winkelsumme im Dreieck", merk_summe())
    tafel = merk
    loes = "".join(box(t, h) for t, h in FOLIEN if "ausgefüllt" in t)
    ziel = HIER / f"{NAME}.html"
    bau_woche(ziel, "Woche 8, Stunde 2: Winkel an Geraden, Winkelsumme", "Klasse 7c, Mathematik, Di 10.11.2026, Doppelstunde (90 Minuten)",
              vb, SCHRITTE, FOLIEN, tafel=tafel, merkheft=merk, loesungen=loes, extra_css=EXTRA, verlauf="Die Stunde", leiste=LEISTE, quer=QUER)


if __name__ == "__main__":
    main()
