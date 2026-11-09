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


def sektoren(S, t, l, namen, r=7.5):
    """Vier Winkel im Schnittpunkt. t und l: Richtungen der beiden Geraden mit t < l < t + 180.
    Reihenfolge gegen den Uhrzeigersinn: (t, l), (l, t+180), (t+180, l+180), (l+180, t+360)."""
    assert t < l < t + 180
    strahlen = [t, l, t + 180, l + 180, t + 360]
    s = ""
    for i, n in enumerate(namen):
        if n:
            name, f = n if isinstance(n, tuple) else (n, ROT)
            s += winkel(S, strahlen[i], strahlen[i + 1], name, f, r)
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
    return f'<div class="auftrag"><div><b>Aufgabe:</b> {was}</div><div><b>Für Schnelle:</b> {schnelle}</div></div>'


# ================================================================ Seite 1: Entdecken
def entdecken(l):
    S = (34, 25)
    f1 = (gerade(S, -12, 32, 32) + gerade(S, 43, 29, 29) + sektoren(S, -12, 43, ["α", "β", "γ", "δ"]))
    g, t = (42, 11), 62
    h = P(*g, 26, t + 180)
    f2 = (gerade(g, 180, 36, 30) + gerade(h, 180, 36, 30) + linie(P(*h, 13, t + 180), P(*g, 11, t))
          + sektoren(g, t, 180, ["β", "γ", "δ", "α"], 6.5) + sektoren(h, t, 180, ["β′", "γ′", "δ′", "α′"], 6.5)
          + text((74, 11), "g", g=3.6, fett=False, kursiv=True) + text((74, h[1]), "h", g=3.6, fett=False, kursiv=True))
    was1 = ('<p class="ergebnis lsg">Gegenüber: gleich groß. Nebeneinander: zusammen 180°.</p>' if l else '<p class="ergebnis">Was fällt auf?</p>')
    was2 = ('<p class="ergebnis lsg">Nur zwei Größen: 62° und 118°. Zusammen 180°.</p>' if l else '<p class="ergebnis">Welche Winkel sind gleich groß?</p>')
    return (f'<div class="uheft"><div class="auftrag"><b>Aufgabe:</b> Ins Übungsheft zwei Geraden zeichnen, die sich schneiden. Alle vier Winkel messen.</div>'
            f'<div class="fig-rechts">{svg(f1, 0, 0, 68, 50)}<div>{felder(l, [("α", "55°"), ("β", "125°"), ("γ", "55°"), ("δ", "125°")], 2)}</div></div>{was1}'
            f'<div class="auftrag" style="margin-top:7mm"><b>Aufgabe:</b> Zwei Karolinien als Parallelen g und h, darüber eine schräge Gerade. Alle acht Winkel messen.</div>'
            f'<div class="fig-rechts">{svg(f2, 0, 0, 78, 62)}<div>{felder(l, [("α", "62°"), ("β", "118°"), ("γ", "62°"), ("δ", "118°"), ("α′", "62°"), ("β′", "118°"), ("γ′", "62°"), ("δ′", "118°")], 2)}</div></div>{was2}</div>')


# ================================================================ Merkheft 1
def mini(art):
    S1, S2 = (10, 27), (31, 15)
    t = math.degrees(math.atan2(-(S2[1] - S1[1]), S2[0] - S1[0]))
    if art in ("scheitel", "neben"):
        S = (22, 18)
        s = gerade(S, -22, 21, 21) + gerade(S, 24, 21, 21)
        namen = [("α", ROT), None, ("γ", ROT), None] if art == "scheitel" else [("α", BLAU), ("β", BLAU), None, None]
        return svg(s + sektoren(S, -22, 24, namen, 7), 0, 0, 44, 36)
    s = gerade(S1, 78, 13, 13) + gerade(S2, 78, 13, 13) + linie(P(*S1, 8, t + 180), P(*S2, 10, t))
    s += text((P(*S1, 13, 78)[0] + 3, 15), "g", g=3.3, fett=False, kursiv=True) + text((P(*S2, 13, 78)[0] + 3.2, 3), "h", g=3.3, fett=False, kursiv=True)
    if art == "stufen":
        s += sektoren(S1, t, 78, [("α", LILA), None, None, None], 6.5) + sektoren(S2, t, 78, [("α′", LILA), None, None, None], 6.5)
    else:
        s += sektoren(S1, t, 78, [("α", GRUEN), None, None, None], 6.5) + sektoren(S2, t, 78, [None, None, ("γ′", GRUEN), None], 6.5)
    return svg(s, 0, 0, 44, 40)


def merk_geraden():
    t, g_a = 8, 73
    S1, S2 = (24, 26), P(24, 26, 50, 8)
    s = (gerade(S1, g_a, 22, 23) + gerade(S2, g_a, 22, 23) + linie(P(*S1, 17, t + 180), P(*S2, 17, t))
         + sektoren(S1, t, g_a, [("65°", SCHWARZ), "β", "γ", "δ"], 7.5) + sektoren(S2, t, g_a, ["α′", "β′", "γ′", "δ′"], 7.5)
         + text((P(*S1, 22, g_a)[0] + 3, 5), "g", g=3.5, fett=False, kursiv=True) + text((P(*S2, 22, g_a)[0] + 3.5, 0), "h", g=3.5, fett=False, kursiv=True)
         + text((53, 49), "g ∥ h", g=3.4, fett=False))
    karten = [("scheitel", ROT, "Scheitelwinkel", "gegenüber", "gleich groß", "γ = α"), ("neben", BLAU, "Nebenwinkel", "daneben", "zusammen 180°", "α + β = 180°"),
              ("stufen", LILA, "Stufenwinkel", "gestuft", "gleich groß", "α = α′"), ("wechsel", GRUEN, "Wechselwinkel", "über Kreuz", "gleich groß", "α = γ′")]
    oben = "".join(f'<div class="wk"><b style="color:{f}">{n}</b>{mini(a)}<div>{wo}</div><div><b>{r}</b></div><div style="color:{f};font-weight:700">{gl}</div></div>'
                   for a, f, n, wo, r, gl in karten)
    links = (svg(s, 0, -3, 92, 56) + '<div class="mz"><span class="sn">1</span><span>Bekannt: α = 65°</span></div>'
             '<div class="mz"><span class="sn">2</span><span>β liegt daneben: Nebenwinkel</span></div>'
             '<div class="mz"><span class="sn">3</span><span>β = 180° − 65° = <span class="rot">115°</span></span></div>')
    rez = rezept_box("Winkel an Geraden", ["Bekannten Winkel suchen.", "Lage prüfen: gegenüber, daneben, gestuft oder über Kreuz?", "Daneben: 180° minus. Sonst: gleich groß."])
    w = ["γ gegenüber von α: γ = 65°", "δ gegenüber von β: δ = 115°", "α′ gestuft zu α: α′ = 65°", "γ′ über Kreuz zu α: γ′ = 65°", "β′ gestuft zu β: β′ = 115°", "δ′ über Kreuz zu β: δ′ = 115°"]
    assert 180 - 65 == 115
    return (f'<div class="heft"><div class="wk4">{oben}</div><p class="merkk">Bei g ∥ h gelten Stufen- und Wechselwinkel. Im Schnittpunkt liegen vier Winkel.</p>'
            f'<div class="mb"><div>{links}</div>{rez}</div><div class="weitere"><div class="weitere-t">Weitere Beispiele</div>' + "".join(f'<div class="wz">{x}</div>' for x in w) + "</div></div>")


# ================================================================ Übung Geraden
def fig_paar(t, l, abst, namen1, namen2, labels, x0, y0, b, h, S1, zur=(14, 14), lin=(16, 16), r=7):
    S2 = P(*S1, abst, t)
    s = (gerade(S1, l, *lin) + gerade(S2, l, *lin) + linie(P(*S1, zur[0], t + 180), P(*S2, zur[1], t))
         + sektoren(S1, t, l, namen1, r) + sektoren(S2, t, l, namen2, r) + labels(S1, S2))
    return svg(s, x0, y0, b, h)


def zeile(l, davor, w, danach=""):
    return f'<div class="azeile">{davor} {lk(l, w, True)} {danach}</div>'


def g_lab(S1, S2, l, d=(15, 3), p=(30, 44)):
    q1, q2 = P(*S1, 16, l + 180), P(*S2, 16, l + 180)
    return (text((q1[0] + d[0] - 12, q1[1] + 3), "g", g=3.4, fett=False, kursiv=True) + text((q2[0] + d[0] - 12, q2[1] + 3), "h", g=3.4, fett=False, kursiv=True)
            + text(p, "g ∥ h", g=3.3, fett=False))


def uebung_geraden(l):
    N = ["α", "β", "γ", "δ"]
    NS = ["α′", "β′", "γ′", "δ′"]
    n1 = fig_paar(-3, 33, 46, N, NS, lambda a, b: g_lab(a, b, 33, p=(38, 40)), 0, 0, 82, 45, (16, 20), zur=(12, 14))
    n2 = fig_paar(-3, 27, 46, [("30°", SCHWARZ), "β", "γ", "δ"], NS, lambda a, b: g_lab(a, b, 27, p=(38, 40)), 0, 0, 82, 45, (16, 20), zur=(12, 14))
    a_ = fig_paar(-20, 31, 50, N, NS, lambda a, b: g_lab(a, b, 31, p=(46, 12)), 0, 0, 82, 52, (15, 15), zur=(12, 12))
    b_ = fig_paar(17, 127, 50, [None, ("70°", SCHWARZ), "γ", "δ"], ["α′", "β′", None, "δ′"], lambda a, b: g_lab(a, b, 127, d=(16, 3), p=(50, 45)), 0, 0, 82, 54, (17, 40), zur=(12, 12))
    return (auftrag("Buch S. 46 Nr. 1, Nr. 2 und S. 47 Nr. A ins Übungsheft.", "Buch S. 47 Nr. B")
            + '<div class="uheft zw">'
            f'<div><div class="nr">○ S. 46 Nr. 1: Wie heißen die zwei Winkel?</div>{n1}'
            + zeile(l, "a) α und γ sind", "Scheitelwinkel") + zeile(l, "b) α′ und α sind", "Stufenwinkel") + zeile(l, "c) β und δ sind", "Scheitelwinkel") + zeile(l, "d) β′ und δ sind", "Wechselwinkel")
            + f'</div><div><div class="nr">○ S. 46 Nr. 2: Wie groß sind die Winkel?</div>{n2}'
            + felder(l, [("β", "150°"), ("γ", "30°"), ("δ", "150°"), ("α′", "30°"), ("β′", "150°"), ("γ′", "30°"), ("δ′", "150°")], 2)
            + f'</div><div><div class="nr">S. 47 Nr. A: Gib den richtigen Winkel an.</div>{a_}'
            + f'<div class="azeile">a) β und {lk(l, "δ")} sind Scheitelwinkel.</div><div class="azeile">b) γ und {lk(l, "β, δ")} sind Nebenwinkel.</div>'
            + f'<div class="azeile">c) α und {lk(l, "α′")} sind Stufenwinkel.</div><div class="azeile">d) δ und {lk(l, "β′")} sind Wechselwinkel.</div>'
            + f'</div><div><div class="nr">S. 47 Nr. B: Für Schnelle</div>{b_}'
            + felder(l, [("γ", "110°"), ("δ", "70°"), ("α′", "110°"), ("β′", "70°"), ("δ′", "70°")], 3)
            + '<div class="azeile2">b) Zwei Möglichkeiten für δ′:' + ('<br><span class="lsg">Scheitelwinkel von β′ oder Stufenwinkel von δ.</span>' if l else "") + "</div></div></div>")


def weitere_geraden(l):
    a = fig_paar(34.3, 169.3, -36, [("135°", SCHWARZ), None, "α", None], ["β", None, None, None],
                 lambda s1, s2: text(P(*s1, 31, -10.7), "g", g=3.4, fett=False, kursiv=True) + text(P(*s2, 34, -10.7), "h", g=3.4, fett=False, kursiv=True),
                 0, 0, 82, 54, (40, 19), zur=(17, 16), lin=(28, 30), r=8)
    b = fig_paar(-10, 90, 42, [("β", ROT), None, None, ("80°", SCHWARZ)], [None, "α", None, None],
                 lambda s1, s2: text((s1[0] + 3, 47), "g", g=3.4, fett=False, kursiv=True) + text((s2[0] + 3, 54), "h", g=3.4, fett=False, kursiv=True),
                 0, 0, 82, 56, (16, 24), zur=(11, 18), lin=(21, 21), r=8)
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
    b4 = ('<div class="azeile2 lsg">β = 115°: Nebenwinkel vom blauen Winkel, der ist als Stufenwinkel 65°.<br>γ = 65°: Stufen- und Scheitelwinkel.<br>δ = 115°: Nebenwinkel von 65°.</div>' if l
          else felder(l, [("β", ""), ("γ", ""), ("δ", "")], 3) + '<div class="azeile2">Begründe.</div>')
    return (auftrag("Buch S. 47 orange Nr. 3 und Nr. 5 ins Übungsheft.", "Buch S. 47 grün Nr. 4 und Nr. 5")
            + '<div class="uheft zw">'
            f'<div><div class="nr">○ S. 47 orange Nr. 3 a): Wie groß sind α und β?</div>{a}{felder(l, [("α", "135°"), ("β", "135°")], 2)}</div>'
            f'<div><div class="nr">○ S. 47 orange Nr. 3 b)</div>{b}{felder(l, [("α", "80°"), ("β", "100°")], 2)}</div>'
            f'<div><div class="nr">◐ S. 47 orange Nr. 5 (i ∥ k, g ∥ h)</div>{svg(n5, 0, 0, 82, 78, 72)}{felder(l, [("α", "110°"), ("β", "70°"), ("γ", "70°"), ("δ", "70°"), ("ε", "110°")], 3)}</div>'
            f'<div><div class="nr">Für Schnelle: S. 47 grün Nr. 4 (g ∥ h, i ∥ k)</div>{svg(vk, 0, 0, 86, 76, 76)}{b4}'
            + ('<div class="azeile2 lsg">Nr. 5: 90° und 120° (Nebenwinkel 60°).</div>' if l else "")
            + "</div></div>")


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
    dd = svg(d, -6, round(C[1] - 5, 2), c + 12, round(-C[1] + 10, 2), 82)
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
         + winkel(C2, 180, 180 + al, "α′", ROT, 8) + winkel(C2, 180 + al, 250 + al - 0, "γ", "#8a6700", 8) + winkel(C2, 300, 360, "β′", BLAU, 8)
         + text((C2[0], -3), "C", g=3.4, fett=False) + text((A2[0] - 3, A2[1] + 2), "A", g=3.4, fett=False) + text((B2[0] + 3, B2[1] + 2), "B", g=3.4, fett=False))
    return ('<div class="uheft"><div class="auftrag"><b>Aufgabe:</b> Auf Schmierpapier ein großes Dreieck zeichnen. Winkel bunt markieren. Die drei Ecken abreißen und an einem Punkt zusammenlegen.</div>'
            f'<div class="fig-rechts">{dd}{svg(leg, 0, 0, 80, 30, 88)}</div><p class="ergebnis lsg" style="font-size:26px;text-align:center">Die drei Ecken ergeben einen gestreckten Winkel: 180°.</p></div>'
            f'<h4 style="font-size:20px;margin:8mm 0 2mm">Warum? Parallele durch C</h4><div class="fig-rechts">{svg(w, 0, -6, 92, round(-C[1] + 12, 2))}'
            '<div class="warum2"><div>Wechselwinkel:</div><div class="lsg">α′ = α</div><div class="lsg">β′ = β</div><div style="margin-top:3mm">Gestreckter Winkel bei C:</div><div class="lsg">α + γ + β = 180°</div></div></div>')


# ================================================================ Merkheft 2
BSP = [("α = 90°, β = 35°", 90, 35, "γ", 55), ("α = 120°, γ = 25°", 120, 25, "β", 35), ("β = 48°, γ = 62°", 48, 62, "α", 70),
       ("α = 20°, β = 20°", 20, 20, "γ", 140), ("α = 60°, β = 60°", 60, 60, "γ", 60), ("α = 38,5°, β = 41,5°", 38.5, 41.5, "γ", 100)]
for _t, _a, _b, _n, _e in BSP:
    assert 180 - _a - _b == _e, _t


def merk_summe():
    fig = dreieck(65, 45, 70, {"A": ("65°", SCHWARZ), "B": ("45°", SCHWARZ), "C": ("γ", ROT)}, rand=8)
    assert 65 + 45 == 110 and 180 - 110 == 70
    links = (fig + '<div class="mz"><span class="sn">1</span><span>Gesucht: γ</span></div>'
             '<div class="mz"><span class="sn">2</span><span>65° + 45° = <span class="gelb">110°</span></span></div>'
             '<div class="mz"><span class="sn">3</span><span>γ = 180° − <span class="gelb">110°</span> = <span class="rot">70°</span></span></div>'
             '<div class="mz"><span class="sn">4</span><span>Probe: 65° + 45° + 70° = 180°</span></div>')
    rez = rezept_box("Fehlender Winkel im Dreieck", ["Was fehlt?", "Die zwei bekannten Winkel addieren.", "Von 180° abziehen.", "Probe: Alle drei ergeben 180°."])
    w = "".join(f'<div class="wz">{t}: {n} = {str(e)}°</div>' for t, _, _, n, e in BSP)
    return ('<div class="heft"><div class="merksatz">In jedem Dreieck gilt: α + β + γ = 180°</div>'
            f'<div class="mb"><div>{links}</div>{rez}</div><div class="weitere"><div class="weitere-t">Weitere Beispiele</div>{w}</div></div>')


# ================================================================ Übung Winkelsumme
def uebung_summe(l):
    S, R = SCHWARZ, ROT
    n1 = [("a)", dreieck(60, 75, 22, {"A": ("60°", S), "B": ("75°", S), "C": ("γ", R)}, rand=6, r=5.5), "γ", "45°"),
          ("b)", dreieck(25, 120, 26, {"A": ("α", R), "B": ("120°", S), "C": ("35°", S)}, rand=6, r=5.5), "α", "25°"),
          ("c)", dreieck(54, 36, 30, {"A": ("54°", S), "B": ("36°", S), "C": ("γ", R)}, rand=6, r=5.5), "γ", "90°"),
          ("d)", dreieck(70, 70, 17, {"A": ("70°", S), "B": ("β", R), "C": ("40°", S)}, rand=6, r=5), "β", "70°")]
    assert 180 - 60 - 75 == 45 and 180 - 120 - 35 == 25 and 180 - 54 - 36 == 90 and 180 - 70 - 40 == 70
    reihe = "".join(f'<div class="dz"><div class="dfig"><b>{a}</b>{f}</div><div class="feld">{n} = {lk(l, e)}</div></div>' for a, f, n, e in n1)
    fA = dreieck(48, 62, 38, {"A": ("48°", S), "B": ("62°", S), "C": ("γ", R)}, rand=6, r=6)
    fB = dreieck(25, 20, 46, {"A": ("α", R), "B": ("20°", S), "C": ("135°", S)}, rand=6, r=6)
    f3 = dreieck(48, 35, 46, {"A": ("48°", S), "B": ("β", R), "C": ("97°", S)}, rand=6, r=6)
    assert 180 - 48 - 62 == 70 and 180 - 20 - 135 == 25 and 180 - 97 - 48 == 35
    T = [("60°", "50°", None, 70), ("52°", None, "67°", 61), (None, "11°", "16°", 153), ("71°", None, "89°", 20), ("137°", "42°", None, 1)]
    for a, b, g, e in T:
        s = sum(int(x[:-1]) for x in (a, b, g) if x)
        assert 180 - s == e, (a, b, g)
    tz = lambda i, name: f"<tr><th>{name}</th>" + "".join(f'<td>{r[i] if r[i] else lk(l, str(r[3]) + "°")}</td>' for r in T) + "</tr>"
    tab = '<table class="wt"><tr><th></th><th>a)</th><th>b)</th><th>c)</th><th>d)</th><th>e)</th></tr>' + tz(0, "α") + tz(1, "β") + tz(2, "γ") + "</table>"
    return (auftrag("Buch S. 48 Nr. 1, S. 49 Nr. A und orange Nr. 3, Nr. 4 ins Übungsheft.", "Buch S. 48 Nr. 2: Dreieck abzeichnen, messen, mit der Winkelsumme prüfen.")
            + '<div class="uheft"><div class="nr">○ S. 48 Nr. 1: Berechne den fehlenden Winkel.</div>'
            f'<div class="dr4">{reihe}</div>'
            '<div class="nr" style="margin-top:3mm">S. 49 Nr. A und orange Nr. 3: Berechne den fehlenden Winkel.</div>'
            f'<div class="dr3"><div class="dz"><div class="dfig"><b>A a)</b>{fA}</div><div class="feld">γ = {lk(l, "70°")}</div></div>'
            f'<div class="dz"><div class="dfig"><b>A b)</b>{fB}</div><div class="feld">α = {lk(l, "25°")}</div></div>'
            f'<div class="dz"><div class="dfig"><b>Nr. 3</b>{f3}</div><div class="feld">β = {lk(l, "35°")}</div></div></div>'
            f'<div class="nr" style="margin-top:3mm">○ S. 49 orange Nr. 4: Ein Winkel fehlt. Berechne.</div>{tab}</div>')


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
    c = 78
    gam = 180 - a - b
    assert 180 - 77 - 59 == 44 and 180 - 71 - 48 == 61 and 180 - 44 - 61 == 75
    A, B = (0, 0), (c, 0)
    C = P(*A, c * math.sin(math.radians(b)) / math.sin(math.radians(gam)), a)
    P1 = (14, 0)
    P2 = P(*A, 14 * math.sin(math.radians(59)) / math.sin(math.radians(77)), a)
    Q1 = (c - 13, 0)
    Q2 = P(*B, 13 * math.sin(math.radians(48)) / math.sin(math.radians(71)), 180 - b)
    # Riss oben: fest vorgegebene Zacken zwischen P2' und Q2'
    h = 0.62
    U = (P2[0] + (C[0] - P2[0]) * h, P2[1] + (C[1] - P2[1]) * h)
    V = (Q2[0] + (C[0] - Q2[0]) * h, Q2[1] + (C[1] - Q2[1]) * h)
    z = [0.8, -1.1, 0.5, -0.7, 1.2, -0.9, 0.7, -1.2, 0.6]
    riss = [(U[0] + (V[0] - U[0]) * (i + 1) / 10, U[1] + (V[1] - U[1]) * (i + 1) / 10 + z[i]) for i in range(9)]
    pts = [P1, Q1, Q2, V] + riss[::-1] + [U, P2]
    poly = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    grau = "#9aa3ad"
    f6 = (f'<polygon points="0,0 {c},0 {C[0]:.2f},{C[1]:.2f}" fill="none" stroke="{grau}" stroke-width="0.4"/>'
          f'<polygon points="{poly}" fill="#dfe7f2" stroke="{S}" stroke-width="0.6" stroke-linejoin="round"/>'
          + winkel(P1, 0, 121, "121°", BLAU, 6) + winkel(Q1, 180 - 132, 180, "132°", BLAU, 6)
          + winkel(P2, 180 + a + 0, 180 + a + 103, "103°", BLAU, 6) + winkel(Q2, 360 - b - 109, 360 - b, "109°", BLAU, 6))
    if l:
        f6 += (text((7.6, -2.6), "44°", PINK, 3.4) + text((c - 5.8, -2.4), "61°", PINK, 3.4) + text((C[0], C[1] + 7), "75°", PINK, 3.4))
    return (auftrag("Buch S. 49 orange Nr. 5 und Nr. 6 ins Übungsheft.", "Buch S. 49 grün Nr. 6")
            + '<div class="uheft"><div class="nr">◐ S. 49 orange Nr. 5: Berechne die fehlenden Winkel.</div><div class="zw">'
            f'<div><b>a)</b>{fa}{felder(l, [("α", "55°"), ("γ", "85°")], 2)}</div><div><b>b)</b>{fb}{felder(l, [("α", "110°"), ("β", "40°"), ("γ", "30°")], 3)}</div></div>'
            '<div class="azeile2">Mit welcher Art von Winkeln hast du die Lösung gefunden?' + (' <span class="lsg">Nebenwinkel.</span>' if l else "") + "</div>"
            '<div class="nr" style="margin-top:3mm">◐ S. 49 orange Nr. 6: Zwei Ecken wurden abgeschnitten, die dritte abgerissen. Wie groß waren die Winkel des Dreiecks?</div>'
            f'<div class="fig-rechts">{svg(f6, -6, round(C[1] - 4, 2), c + 12, round(-C[1] + 9, 2), 90)}<div>{felder(l, [("links", "44°"), ("rechts", "61°"), ("oben", "75°")], 1)}</div></div>'
            '<div class="nr" style="margin-top:3mm">Für Schnelle: S. 49 grün Nr. 6</div>'
            '<div>Ein Dreieck hat die Winkel α = 38,7° und β = 45,7°. a) Berechne γ. b) Runde die drei Winkel auf ganze Grad. Erkläre, was dir auffällt.</div>'
            + ('<div class="azeile2 lsg">γ = 95,6°. Gerundet: 39° + 46° + 96° = 181°. Durch das Runden stimmt die Summe nicht mehr.</div>' if l else "") + "</div>")


EXTRA = EXTRA_W7 + """<style>
.luecke.lang{min-width:39mm!important}
.auftrag{background:#f4f6f9;border:2px solid #1b1b1b;border-radius:8px;padding:6px 13px;margin:0 0 9px;font-size:17px}
.felder{display:grid;gap:1mm 7mm;align-items:center}.feld{font-size:19px;font-weight:700;white-space:nowrap}
.fig-rechts{display:flex;gap:9mm;align-items:center;justify-content:center;margin:2mm 0}
.mitte{display:flex;justify-content:center;margin:14mm 0 8mm}
.ergebnis{font-size:20px;font-weight:700;margin:2mm 0}
.lsg{color:#E6007E;font-weight:700}
.wk4{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}.wk{text-align:center;font-size:16px;line-height:1.25}.wk svg{margin:1mm auto}.wk>b:first-child{font-size:17px}
.merkk{margin:3mm 0;font-size:16px;font-weight:600}
.merksatz{font-size:29px;font-weight:800;text-align:center;border:2.5px solid #1a56a0;background:#eef3fb;border-radius:8px;padding:9px;margin:0 0 7mm}
.wz{font-size:18px!important}.weitere{grid-template-columns:repeat(2,1fr)!important}
.zw{display:grid;grid-template-columns:1fr 1fr;gap:3mm 7mm}.nr{font-weight:700;font-size:16px;margin:0 0 1mm}
.azeile{font-size:17px;white-space:nowrap;margin:.5mm 0}.azeile2{font-size:16px;margin-top:1mm}
.dr4{display:grid;grid-template-columns:repeat(4,auto);gap:3mm;justify-content:space-between;align-items:end}.dr3{display:grid;grid-template-columns:repeat(3,auto);gap:3mm;justify-content:space-between;align-items:end}
.dz{display:flex;flex-direction:column;align-items:center}.dfig{display:flex;gap:1mm;align-items:flex-start}.dfig svg{max-width:none}
table.wt{border-collapse:collapse;font-size:18px;margin-top:1mm}.wt td,.wt th{border:1px solid #9aa3ad;padding:0 7mm;text-align:center;height:15mm}.wt th{background:#eef1f5}.wt tr:first-child th{height:8mm}
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
QUER = set()
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
          ("Digital", "Folien-PDF aufs iPad, an den Kästchen schreibst du die Werte der Klasse hinein."),
          ("Raum", "Doppelstunde, 90 Minuten. Mittwoch geht es mit Dreiecksformen (S. 50) weiter.")]
    merk = box("Eintrag 1: Winkel an Geraden", merk_geraden()) + box("Eintrag 2: Winkelsumme im Dreieck", merk_summe())
    tafel = merk
    loes = "".join(box(t, h) for t, h in FOLIEN if "ausgefüllt" in t)
    ziel = HIER / f"{NAME}.html"
    bau_woche(ziel, "Woche 8, Stunde 2: Winkel an Geraden, Winkelsumme", "Klasse 7c, Mathematik, Di 10.11.2026, Doppelstunde (90 Minuten)",
              vb, SCHRITTE, FOLIEN, tafel=tafel, merkheft=merk, loesungen=loes, extra_css=EXTRA, verlauf="Die Stunde", leiste=LEISTE, quer=QUER)


if __name__ == "__main__":
    main()
