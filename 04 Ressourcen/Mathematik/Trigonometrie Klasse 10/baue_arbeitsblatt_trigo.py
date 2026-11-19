"""Arbeitsblatt Mathe 10b (19.11.2026, für Fr 20.11.): sin, cos oder tan festigen, EIN A4-Blatt vorne und hinten.
Oskar 19.11. (zweite Fassung): vorne 14 einfache Aufgaben, hinten 10 Hausaufgaben; je Dreieck + Karofeld, kein Text.
Oskar: möglichst viele rechtwinklige Dreiecke, jedes Mal die richtige Winkelfunktion mit einmal Umstellen;
Rückseite (Seite 4) als Hausaufgabe: 10 Aufgaben, bei denen man eine Höhe einzeichnen muss.
Seiten 1 bis 3: 33 Dreiecke in verschiedenen Lagen. sin, cos oder tan einkreisen, im Übungsheft rechnen,
Ergebnis eintragen. ○ Unbekannte oben (mal Nenner), ◐ Unbekannte unten (tauschen), ● Winkel gesucht.
Seite 4: ○ Höhe berechnen, ◐ c, α, β gegeben (Höhe nicht auf c!), ● b, c, α gegeben (Höhe teilt c, Pythagoras).
Lösung = dasselbe Blatt ausgefüllt. Alle Werte mit gerundeten Zwischenwerten wie im Heft, Asserts gegen exakte Werte.
Ausführen: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 baue_arbeitsblatt_trigo.py
"""
import math
import random
import re

from baue_loesung_s15_s16 import ROT, S, C, k, i, Skizze, dreieck, fuss, bruch
from baue_rezept_trigo import BLAU, drucke
from baue_aufgabe_rezept import kreise_einheitlich

NAME = "Mathe 10b – Arbeitsblatt sin, cos, tan üben und Höhe einzeichnen"
r2 = lambda x: round(x + 1e-9, 2)
T = lambda d: math.tan(math.radians(d))
deg = math.degrees


def eng(svg, rand=1.2):
    """viewBox auf das zuschneiden, was wirklich gezeichnet ist (Linien, Flächen, Bögen, Texte mit geschätzter Breite).
    Oskar 19.11.: Dreiecke sollen den Platz füllen, nicht im leeren Rand schwimmen."""
    xs, ys = [], []
    for m in re.finditer(r'x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', svg):
        x1, y1, x2, y2 = map(float, m.groups()); xs += [x1, x2]; ys += [y1, y2]
    for m in re.finditer(r'points="([^"]+)"', svg):
        for pt in m.group(1).split():
            x, y = map(float, pt.split(",")); xs.append(x); ys.append(y)
    for m in re.finditer(r'd="M([-\d.]+),([-\d.]+) A[\d.]+,[\d.]+ 0 0 1 ([-\d.]+),([-\d.]+)"', svg):
        x1, y1, x2, y2 = map(float, m.groups()); xs += [x1, x2]; ys += [y1, y2]
    for m in re.finditer(r'<text x="([-\d.]+)" y="([-\d.]+)" font-size="([\d.]+)"[^>]*>(.*?)</text>', svg):
        x, y, gr = float(m.group(1)), float(m.group(2)), float(m.group(3))
        n = len(re.sub("<[^>]+>", "", m.group(4)))
        w = n * gr * 0.56
        xs += [x - w / 2, x + w / 2]; ys += [y - gr * 0.85, y + gr * 0.25]
    x0, x1, y0, y1 = min(xs) - rand, max(xs) + rand, min(ys) - rand, max(ys) + rand
    w, h = x1 - x0, y1 - y0
    return re.sub(r'<svg viewBox="[^"]+" width="[\d.]+mm" height="[\d.]+mm"',
                  f'<svg viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" width="{w:.1f}mm" height="{h:.1f}mm"', svg, count=1)


def sicher(x):
    """Keine Grenzfälle beim Runden auf zwei Stellen (dritte Stelle nicht nahe 5)."""
    f = (x * 100) % 1
    return not (0.4 < f < 0.6)


# ---------------------------------------------------------------- Seiten 1 bis 3: rechtwinklige Dreiecke
# Typen: (bekannt, gesucht, Funktion). p = Ankathete, q = Gegenkathete, h = Hypotenuse, w = Winkel φ
TYPEN = {
    "q_aus_h": ("h", "q", "sin", "○"), "p_aus_h": ("h", "p", "cos", "○"), "q_aus_p": ("p", "q", "tan", "○"),
    "h_aus_q": ("q", "h", "sin", "◐"), "h_aus_p": ("p", "h", "cos", "◐"), "p_aus_q": ("q", "p", "tan", "◐"),
    "w_sin": ("qh", "w", "sin", "●"), "w_cos": ("ph", "w", "cos", "●"), "w_tan": ("qp", "w", "tan", "●"),
}
REIHE = (["q_aus_h", "p_aus_h", "q_aus_p", "q_aus_h", "p_aus_h"]          # ○ Unbekannte oben
         + ["h_aus_q", "h_aus_p", "p_aus_q", "h_aus_q", "p_aus_q"]        # ◐ Unbekannte unten
         + ["w_sin", "w_cos", "w_tan", "w_sin"])                          # ● Winkel gesucht


def aufgaben_rechtwinklig():
    rnd = random.Random(2011)
    A = []
    for nr, typ in enumerate(REIHE, 1):
        bekannt, ges, fn, kreis = TYPEN[typ]
        while True:
            w = rnd.randint(22, 68)
            if typ.startswith("w_"):
                h = rnd.randint(40, 120) / 10
                p, q = h * C(w), h * S(w)
                p, q = round(p, 1), round(q, 1)                     # gegebene Seiten mit einer Stelle
                if typ == "w_sin":
                    h = round(h, 1); erg = deg(math.asin(q / h)); geg = {"q": q, "h": h}
                elif typ == "w_cos":
                    h = round(h, 1); erg = deg(math.acos(p / h)); geg = {"p": p, "h": h}
                else:
                    erg = deg(math.atan(q / p)); geg = {"q": q, "p": p}
                if not (q < h if "h" in geg else True) or not (p < geg.get("h", 99)):
                    continue
                w_plot = erg
            else:
                g = rnd.randint(30, 120) / 10
                if bekannt == "h":
                    geg = {"h": g}
                    erg = g * (S(w) if ges == "q" else C(w))
                elif bekannt == "p":
                    geg = {"p": g}
                    erg = g * T(w) if ges == "q" else g / C(w)
                else:
                    geg = {"q": g}
                    erg = g / S(w) if ges == "h" else g / T(w)
                w_plot = w
            if 2.0 <= erg <= 90 and sicher(erg) and (typ.startswith("w_") or 2.0 <= erg <= 16):
                break
        A.append(dict(nr=nr, typ=typ, fn=fn, kreis=kreis, w=w, geg=geg, ges=ges, erg=r2(erg), w_plot=w_plot,
                      dreh=rnd.choice([0, 90, 180, 270]) + rnd.randint(-25, 25), spiegel=rnd.random() < 0.5))
    return A


RW = aufgaben_rechtwinklig()
assert len(RW) == 14


def sk_rw(a, loes, breite=50, hoehe=40):
    """Rechtwinkliges Dreieck: Scheitel V des Winkels φ, rechter Winkel bei R, dritte Ecke W; gedreht/gespiegelt."""
    w = a["w_plot"]
    g = a["geg"]
    h = g.get("h") or (g["q"] / S(w) if "q" in g else g["p"] / C(w))
    p, q = h * C(w), h * S(w)
    pts = [(0, 0), (p, 0), (p, q)]
    if a["spiegel"]:
        pts = [(-x, y) for x, y in pts]
    th = math.radians(a["dreh"])
    pts = [(x * math.cos(th) - y * math.sin(th), x * math.sin(th) + y * math.cos(th)) for x, y in pts]
    V, R, W = pts
    s = Skizze(dreieck(V, R, W), breite=breite, hoehe=hoehe)
    s.rechter(R, V, W, r=2.6)
    mark = lambda name: (k(g[name], 1) + " cm") if name in g else None
    for name, (P1, P2) in (("p", (V, R)), ("q", (R, W)), ("h", (V, W))):
        t = mark(name)
        if t:
            s.seite(P1, P2, t, ab=2.4)
        elif a["ges"] == name:
            s.seite(P1, P2, (k(a["erg"]) + " cm") if loes else "x", ROT, fett=True, ab=2.4)
    if a["ges"] == "w":
        # Oskar 19.11.: α muss im Winkel stehen, nah am Bogen: großer Bogen, α innen; in der Lösung der Wert knapp außen
        s.winkel(V, R, W, (k(a["erg"]) + "°") if loes else "α", ROT, r=7.5, rt=11.5 if loes else 4.8, fett=True)
    else:
        s.winkel(V, R, W, f"{a['w']}°", r=4.5, rt=8.5)
    return eng(s.svg())


# ---------------------------------------------------------------- Seite 4: Höhe einzeichnen (Hausaufgabe)
def ha_aufgaben():
    H = []
    # ○ Höhe berechnen: (gegebene Seite, Winkel, Höhe, Dreieck b, c, α zum Zeichnen)
    for nr, (seite, wert, winkel, wwert, hname, form) in enumerate([
            ("b", 6.5, "α", 48, "c", (6.5, 8.0, 48)),
            ("a", 7.2, "β", 56, "c", None),
            ("c", 8.4, "β", 62, "a", None),
            ("c", 7.6, "α", 41, "b", None)], 1):
        h = r2(wert * S(wwert))
        assert sicher(wert * S(wwert))
        H.append(dict(nr=nr, typ="h", kreis="○", seite=seite, wert=wert, winkel=winkel, wwert=wwert, hname=hname, h=h))
    # ◐ c, α, β gegeben, gesucht a (Höhe h_b) bzw. b (Höhe h_a); nie die einzige bekannte Seite c teilen
    for nr, (c, al, be, ges) in enumerate([(8.0, 53, 63, "a"), (7.5, 44, 71, "a"), (9.2, 58, 49, "b")], 5):
        ga = 180 - al - be
        if ges == "a":
            hw = c * S(al); hh = r2(hw); x = hh / S(ga); hname = "b"
        else:
            hw = c * S(be); hh = r2(hw); x = hh / S(ga); hname = "a"
        assert sicher(hw) and sicher(x)
        exakt = c * S(al) / S(ga) if ges == "a" else c * S(be) / S(ga)
        assert abs(r2(x) - exakt) < 0.015
        H.append(dict(nr=nr, typ="cab", kreis="◐", c=c, al=al, be=be, ga=ga, ges=ges, hname=hname, h=hh, x=r2(x)))
    # ● b, c, α gegeben, gesucht a: h_c, c₁ = AF, c₂ = FB, Pythagoras
    for nr, (b, c, al) in enumerate([(6.0, 8.5, 50), (5.8, 9.0, 38), (7.2, 7.8, 64)], 8):
        hcw, c1w = b * S(al), b * C(al)
        hc, c1 = r2(hcw), r2(c1w); c2 = r2(c - c1); a = math.sqrt(hc**2 + c2**2)
        assert sicher(hcw) and sicher(c1w) and sicher(a) and c1 < c       # F liegt zwischen A und B
        assert abs(r2(a) - math.sqrt(b**2 + c**2 - 2 * b * c * C(al))) < 0.015
        H.append(dict(nr=nr, typ="bca", kreis="●", b=b, c=c, al=al, hc=hc, c1=c1, c2=c2, a=r2(a)))
    return H


HA = ha_aufgaben()
SUB = lambda t: f"<tspan font-size='2.2' dy='0.8'>{t}</tspan>"


def sk_ha(a, loes, breite=62, hoehe=48):
    """Allgemeines Dreieck ABC (A links, B rechts, C oben); in der Lösung die Höhe blau mit Fußpunkt F."""
    if a["typ"] == "h":
        werte = {1: (8.0, 48, 6.5), 2: (8.2, None, None), 3: (8.4, None, None), 4: (7.6, 41, 6.9)}
        if a["nr"] == 1:
            P = dreieck((0, 0), (8.0, 0), (6.5 * C(48), 6.5 * S(48)))
        elif a["nr"] == 2:
            B = (8.2, 0); P = dreieck((0, 0), B, (8.2 - 7.2 * C(56), 7.2 * S(56)))
        elif a["nr"] == 3:
            B = (8.4, 0); P = dreieck((0, 0), B, (8.4 - 6.8 * C(62), 6.8 * S(62)))
        else:
            P = dreieck((0, 0), (7.6, 0), (7.0 * C(41), 7.0 * S(41)))
    elif a["typ"] == "cab":
        b_ex = a["c"] * S(a["be"]) / S(a["ga"])
        P = dreieck((0, 0), (a["c"], 0), (b_ex * C(a["al"]), b_ex * S(a["al"])))
    else:
        P = dreieck((0, 0), (a["c"], 0), (a["b"] * C(a["al"]), a["b"] * S(a["al"])))
    A_, B, Cc = P["A"], P["B"], P["C"]
    s = Skizze(P, breite=breite, hoehe=hoehe)
    ecke = {"a": (B, Cc), "b": (A_, Cc), "c": (A_, B)}
    fussvon = {"a": (A_, B, Cc), "b": (B, A_, Cc), "c": (Cc, A_, B)}         # Höhe h_x: von der Ecke gegenüber auf x

    def hoehe(name):
        von, q1, q2 = fussvon[name]
        F = fuss(von, q1, q2)
        s.linie(von, F, BLAU, 0.6, "1.4,0.9"); s.rechter(F, q1, von, r=2.6)
        s.seite(von, F, "h" + SUB(name), BLAU, aussen=False, ab=2.2, pos=0.68)
        return F

    if a["typ"] == "h":
        s.seite(*ecke[a["seite"]], f"{k(a['wert'], 1)} cm")
        wink = {"α": (A_, B, Cc), "β": (B, A_, Cc)}[a["winkel"]]
        s.winkel(*wink, f"{a['wwert']}°", r=4.2, rt=8.5)
        if loes:
            hoehe(a["hname"])
    elif a["typ"] == "cab":
        s.seite(A_, B, f"{k(a['c'], 1)} cm")
        s.winkel(A_, B, Cc, f"{a['al']}°", r=4.2, rt=8.5); s.winkel(B, A_, Cc, f"{a['be']}°", r=4.2, rt=8.5)
        s.seite(*ecke[a["ges"]], a["ges"], ROT, fett=True)
        if loes:
            hoehe(a["hname"])
    else:
        s.seite(A_, B, f"{k(a['c'], 1)} cm"); s.seite(A_, Cc, f"{k(a['b'], 1)} cm")
        s.winkel(A_, B, Cc, f"{a['al']}°", r=4.2, rt=8.5)
        s.seite(B, Cc, "a", ROT, fett=True)
        if loes:
            F = hoehe("c")
            x, y = s.m(*F); s.text(x - 2.6, y - 1.6, "F", gr=2.8)
    for n in "ABC":
        s.ecke(n)
    return eng(s.svg())


def ha_text(a):
    if a["typ"] == "h":
        return f"Berechne die Höhe h<sub>{a['hname']}</sub>."
    if a["typ"] == "cab":
        return f"Berechne die Seite {a['ges']}."
    return "Berechne die Seite a."


def ha_loesung(a):
    hn = i("h", a.get("hname", "c"))
    if a["typ"] == "h":
        von = {"a": "A", "b": "B", "c": "C"}[a["hname"]]
        return [f"{hn} von {von} aus einzeichnen",
                f"sin {a['wwert']}° = {bruch(hn, k(a['wert'], 1))} {um('⋅ ' + k(a['wert'], 1))}",
                f'<b class="erg">{hn} = {k(a["h"])} cm</b>']
    if a["typ"] == "cab":
        w1 = a["al"] if a["ges"] == "a" else a["be"]
        g = a["ges"]
        return [f"γ = 180° − {a['al']}° − {a['be']}° = {a['ga']}°",
                f"{hn} einzeichnen, nicht {i('h', 'c')}",
                f"sin {w1}° = {bruch(hn, k(a['c'], 1))} → {hn} = {k(a['h'])}",
                f"sin {a['ga']}° = {bruch(k(a['h']), g)} → {g} = {bruch(k(a['h']), 'sin ' + str(a['ga']) + '°')}",
                f'<b class="erg">{g} = {k(a["x"])} cm</b>']
    hc = i("h", "c")
    return [f"sin {a['al']}° = {bruch(hc, k(a['b'], 1))} → {hc} = {k(a['hc'])}",
            f"cos {a['al']}° = {bruch('AF', k(a['b'], 1))} → AF = {k(a['c1'])}",
            f"FB = {k(a['c'], 1)} − {k(a['c1'])} = {k(a['c2'])}",
            f"a = √<span class='wu'>{k(a['hc'])}² + {k(a['c2'])}²</span>",
            f'<b class="erg">a = {k(a["a"])} cm</b>']


def um(t):
    return f'<span class="um">| {t}</span>'


# ---------------------------------------------------------------- Seiten (Oskar 19.11.: ein A4-Blatt, vorne Übung, hinten Hausaufgabe;
# nur Dreieck und Karofeld zum Rechnen, kein Text, keine Antwortkästchen, kein sin/cos/tan zum Einkreisen)
FELD_RW = (10, 6)      # Rechenfeld Vorderseite in Kästchen (Breite, Höhe), 1 Kästchen = 5 mm
FELD_HA = (8, 9)      # Rechenfeld Rückseite


def feld(kaestchen, inhalt=""):
    b, h = kaestchen
    return f'<div class="karo" style="width:{b * 5}mm;height:{h * 5}mm">{inhalt}</div>'


def zelle_rw(a, loes):
    g, fn, w = a["geg"], a["fn"], a["w"]
    inhalt = ""
    if loes:
        z = lambda n: k(g[n], 1) if n in g else "x"
        zaehler, nenner = {"sin": ("q", "h"), "cos": ("p", "h"), "tan": ("q", "p")}[fn]
        if a["ges"] == "w":
            zeilen = [f"{fn} α = {bruch(z(zaehler), z(nenner))} {um(fn + '⁻¹')}", f"α = {k(a['erg'])}°"]
        else:
            zeilen = [f"{fn} {w}° = {bruch(z(zaehler), z(nenner))}"]
            if a["ges"] == zaehler:
                zeilen += [f"x = {z(nenner)} ⋅ {fn} {w}°"]
            else:
                zeilen += [f"x = {bruch(z(zaehler), f'{fn} {w}°')}"]
            zeilen += [f"x = {k(a['erg'])} cm"]
        inhalt = '<div class="rw">' + "".join(f"<div><span>{t}</span></div>" for t in zeilen) + "</div>"
    return (f'<div class="zelle"><div class="znr"><span class="kr">{a["kreis"]}</span>{a["nr"]}</div>'
            f'<div class="zsk">{sk_rw(a, loes)}</div>{feld(FELD_RW, inhalt)}</div>')


def zelle_ha(a, loes):
    text = {"h": f"h<sub>{a.get('hname', '')}</sub> = ?", "cab": f"{a.get('ges', '')} = ?", "bca": "a = ?"}[a["typ"]]
    inhalt = ('<div class="rw klein">' + "".join(f"<div><span>{t}</span></div>" for t in ha_loesung(a)) + "</div>") if loes else ""
    return (f'<div class="hzelle"><div class="znr"><span class="kr">{a["kreis"]}</span>{a["nr"]} '
            f'<span class="ges">{text}</span></div>'
            f'<div class="hsk">{sk_ha(a, loes)}</div>{feld(FELD_HA, inhalt)}</div>')


CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #fff; font-family: Helvetica, Arial, sans-serif; color: #222; }}
.seite {{ width: 210mm; height: 297mm; padding: 7mm 9mm 7mm; overflow: hidden; break-after: page; position: relative; }}
.seite:last-child {{ break-after: auto; }}
.balken {{ background: #d9d9d9; font-weight: 700; font-size: 11.5pt; padding: 1.6mm 3mm; display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 2.5mm; }}
.balken span {{ font-weight: 400; font-size: 9pt; }}
.raster {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2.4mm 4mm; }}
.zelle, .hzelle {{ display: flex; align-items: center; gap: 2mm; position: relative; border-bottom: 0.3mm solid #ddd; padding-bottom: 1.6mm; }}
.znr {{ position: absolute; left: 0; top: 0; font-weight: 700; font-size: 10.5pt; z-index: 2; }}
.znr .kr {{ margin-right: 1mm; }}
.ges {{ font-weight: 400; font-size: 9.5pt; color: {ROT}; margin-left: 1.5mm; }}
.zsk {{ flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; height: 33mm; padding-top: 3.5mm; }}
.zsk svg {{ max-height: 30mm; max-width: 100%; height: auto; width: auto; }}
.hsk {{ flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; height: 46mm; padding-top: 4.5mm; }}
.hsk svg {{ max-height: 41mm; max-width: 100%; height: auto; width: auto; }}
.karo {{ flex: none; background-color: #fff; border: 0.3mm solid #b8c2cf;
         background-image: linear-gradient(#cfd8e3 0.2mm, transparent 0.2mm), linear-gradient(90deg, #cfd8e3 0.2mm, transparent 0.2mm);
         background-size: 5mm 5mm; }}
.rw {{ color: {ROT}; font-size: 9pt; padding: 1mm 1.5mm; }}
.rw div {{ height: 9.4mm; display: flex; align-items: center; white-space: nowrap; }}
.rw.klein {{ font-size: 7.8pt; }}
.rw.klein div {{ height: 8.6mm; }}
.erg {{ color: {ROT}; }}
.um {{ color: #999; font-size: 0.9em; margin-left: 1mm; }}
.br {{ display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 0.92em; line-height: 1.1; margin: 0 0.4mm; }}
.br span:first-child {{ border-bottom: 0.25mm solid currentColor; padding: 0 0.5mm; }}
.wu {{ border-top: 0.25mm solid currentColor; padding: 0 0.4mm; }}
.fuss {{ position: absolute; bottom: 3.5mm; left: 9mm; right: 9mm; font-size: 7.5pt; color: #888; display: flex; justify-content: space-between; }}
@media screen {{ body {{ background: #888; }} .seite {{ background: #fff; margin: 6mm auto; box-shadow: 0 1mm 4mm #0005; }} }}
"""


def seite(titel, rechts, inhalt, n, loes):
    fl = "Mathe 10b; Trigonometrie; Arbeitsblatt" + ("; Lösung" if loes else "")
    return (f'<div class="seite"><div class="balken">Mathe 10b   {titel} <span>{rechts}</span></div>{inhalt}'
            f'<div class="fuss"><span>{fl}</span><span>Seite {n}</span></div></div>')


def baue(loes):
    L = "; Lösung" if loes else ""
    leg = "○ leicht; ◐ mittel; ● schwer" + L
    seiten = [
        seite("Trigonometrie: sin, cos, tan", leg, '<div class="raster">' + "".join(zelle_rw(a, loes) for a in RW) + "</div>", 1, loes),
        seite("Hausaufgabe bis Mo 23.11.: Höhe einzeichnen", leg,
              '<div class="raster">' + "".join(zelle_ha(a, loes) for a in HA) + "</div>", 2, loes),
    ]
    name = NAME + (" – Lösung" if loes else "")
    return name, kreise_einheitlich(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{name}</title>'
                                    f'<style>{CSS}</style></head><body>{"".join(seiten)}</body></html>')


if __name__ == "__main__":
    for loes in (False, True):
        drucke(*baue(loes), 2)
