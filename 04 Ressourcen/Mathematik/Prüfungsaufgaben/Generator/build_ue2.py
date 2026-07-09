#!/usr/bin/env python3
"""Übungssatz-Generator v2: rotiert unterschiedliche Aufgabentypen pro Position,
damit die Sätze A–E sich wie die echten Jahrgänge 2021–2026 unterscheiden."""
import math
import json
import re
from fractions import Fraction as Fr
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from ue_lib import (fmt, geld, tsd, seite, kopfzeile, us, svg_grid_parabeln)
from ue_lib2 import (svg_behaelter, svg_koerper_zylhk, svg_koerper_wuerfelpyr,
                     svg_quadrat_dreieck, svg_trapez, svg_raeder, svg_wurf,
                     svg_pyramide_diag, svg_miniboxplot)
import build_ue as v1
from build_ue import (T, TRIG, KOERPER, FUNK, STOCH, ALG, SACH, MUSTER,
                      SAETZE, ARCHIV, UE, teil_von, sortkey)

CB = '<span class="cb"></span>'

# ---------- neue A1-Typen ----------

def t_koerper_ankreuz(p):
    variante = p
    if variante == "zylhk":
        fig = svg_koerper_zylhk()
        einl = ("Ein Körper besteht aus einem Zylinder mit aufgesetzter Halbkugel "
                "(siehe Abbildung). Der Oberflächeninhalt O<sub>gesamt</sub> dieses "
                "Körpers soll berechnet werden.")
        zeilen = [("O<sub>gesamt</sub> = A<sub>Kreis</sub> + M<sub>Zylinder</sub> + ½ · O<sub>Kugel</sub>", True),
                  ("O<sub>gesamt</sub> = O<sub>Zylinder</sub> + O<sub>Halbkugel</sub>", False),
                  ("O<sub>gesamt</sub> = &pi;r² + M<sub>Zylinder</sub> + 2&pi;r²", True)]
        begr = "Bei der zweiten Formel würden die Schnittflächen doppelt gezählt."
    else:
        fig = svg_koerper_wuerfelpyr()
        einl = ("Auf einen Würfel wurde eine quadratische Pyramide aufgesetzt "
                "(siehe Abbildung). Der Oberflächeninhalt O<sub>gesamt</sub> dieses "
                "Körpers soll berechnet werden.")
        zeilen = [("O<sub>gesamt</sub> = 5 · a² + M<sub>Pyramide</sub>", True),
                  ("O<sub>gesamt</sub> = O<sub>Würfel</sub> + M<sub>Pyramide</sub>", False),
                  ("O<sub>gesamt</sub> = O<sub>Würfel</sub> − a² + M<sub>Pyramide</sub>", True)]
        begr = ("Bei der zweiten Formel würde die verdeckte Deckfläche des Würfels "
                "mitgezählt.")
    rows = "".join(
        f'<tr><td class="formel" style="text-align:left">{t}</td>'
        f'<td style="border:none">{CB}</td><td style="border:none">{CB}</td></tr>'
        for t, _ in zeilen)
    aufg = (fig + f"<p>{einl}</p>"
        "<p><b>Kreuzen Sie jeweils richtig oder falsch an.</b> ✎</p>"
        '<table><tr><td style="border:none"></td>'
        '<th style="border:none;font-weight:normal">richtig</th>'
        '<th style="border:none;font-weight:normal">falsch</th></tr>' + rows + "</table>")
    loes = ("<p>" + " · ".join(f"Zeile {i+1}: <b>{'richtig' if ok else 'falsch'}</b>"
                                for i, (t, ok) in enumerate(zeilen)) + "</p>"
            f'<p class="zw">[{begr}]</p>')
    return T("A1/1", 1.5, [KOERPER], "a1_p1", aufg, loes,
             "Zusammengesetzter Körper – Oberflächenformeln richtig/falsch ankreuzen.")

def t_behaelter(p):
    jars, frage_frac, wer = p
    gesamt = sum(sum(j) for j in jars)
    weiss = sum(j[0] for j in jars)
    richtig = [i + 1 for i, j in enumerate(jars) if Fr(j[0], sum(j)) == frage_frac]
    assert richtig, "kein Behälter passt"
    p2 = Fr(weiss, gesamt) * Fr(weiss - 1, gesamt - 1)
    aufg = ("<p>Vier Behälter sind mit gleich großen Kugeln gefüllt. "
        "Die Kugeln sind weiß, grau und schwarz gefärbt.</p>"
        + svg_behaelter(jars) +
        f"<p>a)&nbsp; Aus den Behältern wird jeweils eine Kugel gezogen.<br>"
        f"&emsp;&nbsp;&nbsp;<b>Kreuzen Sie an, für welche Behälter gilt: "
        f"P(weiß) = {frage_frac.numerator}/{frage_frac.denominator}.</b> ✎</p>"
        f"<p>b)&nbsp; Anschließend werden alle Kugeln in einen großen Behälter gelegt. "
        f"{wer} zieht zwei Kugeln ohne Zurücklegen.<br>"
        "&emsp;&nbsp;&nbsp;<b>Berechnen Sie die Wahrscheinlichkeit, zwei weiße "
        "Kugeln zu ziehen.</b></p>")
    loes = (f"<p>a) Behälter {' und '.join(map(str, richtig))} "
        f'<span class="zw">[{" · ".join(f"B{i+1}: {j[0]}/{sum(j)}" for i, j in enumerate(jars))}]</span></p>'
        f"<p>b) P(zwei weiße) = {weiss}/{gesamt} · {weiss-1}/{gesamt-1} = "
        f'<span class="ergebnis">{p2.numerator}/{p2.denominator}</span></p>')
    return T("A1/1", 1.5, [STOCH], "a1_p1", aufg, loes,
             "Vier Behälter mit Kugeln – P(weiß) ankreuzen, zwei Kugeln ohne Zurücklegen.")

def t_gleichung_faktor(p):
    x1, x2 = p
    def t(v):
        return f"− {v}" if v >= 0 else f"+ {-v}"
    gl = f"(x {t(x1)})(x {t(x2)}) = 0"
    for x in (x1, x2):
        assert (x - x1) * (x - x2) == 0
    aufg = ("<p>Lösen Sie die Gleichung.</p>"
        f'<p class="formel" style="font-size:16px;margin:14px 0 14px 26px">{gl}</p>')
    loes = (f'<p><span class="ergebnis">L = {{{min(x1,x2)}; {max(x1,x2)}}}</span> '
        '<span class="zw">[Ein Produkt ist null, wenn einer der Faktoren null ist.]</span></p>')
    return T("A1/3", 1, [ALG], "a1_p3", aufg, loes,
             "Gleichung in faktorisierter Form – Lösungsmenge angeben.")

def t_sin_ergaenzen(p):
    w1, w2 = p
    e1, e2 = 180 - w1, 180 - w2
    assert 0 < e1 < 360 and 0 < e2 < 360 and e1 != w1 and e2 != w2
    kasten = '<span style="display:inline-block;border:1.4px solid #333;min-width:52px;height:20px;vertical-align:middle"></span>'
    aufg = ("<p>Tragen Sie einen weiteren Winkel aus dem Bereich von 0° bis 360° ein, "
        "so dass die Gleichung stimmt.</p> ✎"
        f'<p class="formel" style="margin-left:26px;line-height:2.2">'
        f"a)&nbsp; sin {w1}° = sin {kasten}<br>"
        f"b)&nbsp; sin {w2}° = sin {kasten}</p>")
    loes = (f"<p>a) sin {w1}° = sin <b>{e1}°</b> · b) sin {w2}° = sin <b>{e2}°</b> "
        '<span class="zw">[sin α = sin (180° − α)]</span></p>')
    return T("A1/5", 1, [TRIG], "a1_p5", aufg, loes,
             "Winkel mit gleichem Sinuswert ergänzen (0° bis 360°).")

def t_prozent_tabelle(p):
    kontext, einheit, j0, w0, w1, p2_, p3_, wer = p
    assert w1 * 100 % w0 == 0
    p1_ = w1 * 100 // w0 - 100
    w2 = w1 * (100 + p2_) // 100
    assert w1 * (100 + p2_) % 100 == 0
    w3 = w2 * (100 + p3_) // 100
    assert w2 * (100 + p3_) % 100 == 0
    def pfeil(txt):
        return f'<td style="border:none;font-size:12px">⟶ {txt}</td>'
    kasten = '<span style="display:inline-block;border:1.4px solid #333;min-width:46px;height:18px;vertical-align:middle"></span>'
    aufg = (f"<p>Die Tabelle zeigt {kontext} in den Jahren {j0} und {j0+1}.</p>"
        f'<table><tr><th>Jahr</th><td>{j0}</td><td>{j0+1}</td><td>{j0+2}</td><td>{j0+3}</td></tr>'
        f"<tr><th>{einheit}</th><td>{tsd(w0)}</td><td>{tsd(w1)}</td>"
        f"<td>{kasten}</td><td>{kasten}</td></tr>"
        f'<tr><td style="border:none"></td><td style="border:none"></td>'
        + pfeil(kasten) + pfeil(f"{p2_:+d} %".replace("-", "−")) + pfeil(f"{p3_:+d} %") + "</tr></table>"
        f"<p>a)&nbsp; <b>Um wie viel Prozent nahm die Anzahl von {j0} bis {j0+1} zu?<br>"
        "&emsp;&nbsp;&nbsp;Tragen Sie das Ergebnis in das freie Feld ein.</b> ✎</p>"
        f"<p>b)&nbsp; <b>Berechnen Sie die Anzahl der Jahre {j0+2} und {j0+3} anhand der "
        "angegebenen prozentualen Veränderungen. Tragen Sie die Ergebnisse ein.</b> ✎</p>")
    loes = (f'<p>a) <span class="ergebnis">+{p1_} %</span> '
        f'<span class="zw">[{tsd(w1)} / {tsd(w0)} = {fmt(w1/w0)}]</span></p>'
        f"<p>b) {j0+2}: <b>{tsd(w2)}</b> · {j0+3}: <b>{tsd(w3)}</b></p>")
    return T("A1/7", 1.5, [SACH], "a1_p7", aufg, loes,
             f"Tabelle mit Prozent-Pfeilen – {kontext} fortschreiben.")

def t_parabel_ablesen(p):
    kA, cA, g_m, g_c, p2s, p2c = p
    fA = lambda x: -kA * x * x + cA
    lo = -math.sqrt((cA + 4.2) / kA)
    funcs = [(fA, lo, -lo, 0.5, "p<tspan font-size=\"9\" dy=\"2\">1</tspan>")]
    def sgn(v):
        return ("+ " if v >= 0 else "− ") + fmt(abs(v))
    aufg = (svg_grid_parabeln(funcs) +
        "<p>a)&nbsp; Das Schaubild zeigt die Parabel p<sub>1</sub>.<br>"
        "&emsp;&nbsp;&nbsp;<b>Bestimmen Sie die Funktionsgleichung von p<sub>1</sub>.</b> ✎</p>"
        "<p>b)&nbsp; <b>Zeichnen Sie die Gerade g und die Parabel p<sub>2</sub> "
        "in das Koordinatensystem ein.</b> ✎</p>"
        f'<p class="formel" style="margin-left:26px">g:&nbsp; y = '
        f'{"" if g_m == 1 else ("−" if g_m == -1 else fmt(g_m))}x {sgn(g_c)}<br>'
        f"p<sub>2</sub>:&nbsp; y = (x {sgn(-p2s)})² {sgn(p2c)}</p>")
    loes = (f'<p>a) <span class="ergebnis">p<sub>1</sub>: y = −{fmt(kA)}x² + {fmt(cA)}</span> '
        f'<span class="zw">[Scheitel S(0|{fmt(cA)}), nach unten geöffnet, Streckfaktor an '
        "Gitterpunkten ablesen]</span></p>"
        f"<p>b) g: Gerade durch (0|{fmt(g_c)}) mit Steigung {fmt(g_m)} · "
        f"p<sub>2</sub>: verschobene Normalparabel mit Scheitel ({fmt(p2s)}|{fmt(p2c)})</p>")
    return T("A1/6", 2, [FUNK], "a1_p6", aufg, loes,
             "Parabel aus dem Schaubild ablesen, Gerade und zweite Parabel einzeichnen.")

# ---------- neue A2-Typen ----------

def t_quadrat_dreieck(p):
    a, alpha = p
    be = a * math.tan(math.radians(alpha))
    assert be < a - 0.3
    ae = a / math.cos(math.radians(alpha))
    ec = a - be
    ac = a * math.sqrt(2)
    u = ae + ec + ac
    aufg = (svg_quadrat_dreieck(a, alpha) +
        "<p>Im Quadrat ABCD liegt der Punkt E auf der Seite " + us("BC") + ".</p>"
        "<p>Es gilt:</p>"
        f'<div class="geg">a = {fmt(a,1)} cm<br>&alpha; = {fmt(alpha,1)}°</div>'
        "<p><b>Berechnen Sie den Umfang des Dreiecks AEC.</b></p>")
    loes = (f'<p class="zw">BE = a · tan α = {fmt(be)} cm · '
        f"AE = a / cos α = {fmt(ae)} cm</p>"
        f'<p class="zw">EC = a − BE = {fmt(ec)} cm · AC = a · √2 = {fmt(ac)} cm</p>'
        f'<p><span class="ergebnis">u ≈ {fmt(u,1)} cm</span></p>')
    return T("A2/1", 4, [TRIG], "a2_p1", aufg, loes,
             "Quadrat mit Punkt E – Umfang des einbeschriebenen Dreiecks AEC.")

def t_zylinder_halbkugel(p):
    kontext, h, d, beschicht, frage2_art, menge, ergiebigkeit = p
    r = d / 2.0
    hz = h - r
    assert hz > 0.5
    M = 2 * math.pi * r * hz
    HK = 2 * math.pi * r * r
    O = M + HK
    aufg = (svg_koerper_zylhk() +
        f"<p>{kontext} hat eine Höhe h von {fmt(h)} cm und einen Durchmesser d "
        f"von {fmt(d)} cm.<br>Die Form besteht annähernd aus einem Zylinder mit "
        f"aufgesetzter Halbkugel. {beschicht}</p>"
        "<ul><li><b>Wie viele cm² werden beschichtet? Berechnen Sie.</b></li></ul>")
    if frage2_art == "anzahl":
        n = int(menge / O)
        aufg += (f"<p>{tsd(int(menge))} cm² können mit {ergiebigkeit} beschichtet werden.</p>"
            f"<ul><li><b>Wie viele Stück können damit vollständig beschichtet werden? "
            "Berechnen Sie.</b></li></ul>")
        f2 = (f"<p><b>{n} Stück</b> "
            f'<span class="zw">[{tsd(int(menge))} / {fmt(O,1)} ≈ {fmt(menge/O,1)}, abrunden]</span></p>')
    else:
        ges = menge * O
        f2 = (f"<p><b>≈ {fmt(ges/10000,2)} m²</b> "
            f'<span class="zw">[{menge} · {fmt(O,1)} cm² = {tsd(round(ges))} cm²]</span></p>')
        aufg += (f"<ul><li><b>Wie viel m² werden für {menge} Stück insgesamt benötigt? "
            "Berechnen Sie.</b></li></ul>")
    loes = (f'<p class="zw">r = {fmt(r)} cm · h<sub>Zyl</sub> = h − r = {fmt(hz)} cm</p>'
        f'<p class="zw">M<sub>Zyl</sub> = 2πr·h<sub>Zyl</sub> = {fmt(M)} cm² · '
        f"O<sub>HK</sub> = 2πr² = {fmt(HK)} cm²</p>"
        f'<p><span class="ergebnis">O ≈ {fmt(O,1)} cm²</span></p>' + f2)
    return T("A2/2", 3.5, [KOERPER], "a2_p2", aufg, loes,
             "Zylinder mit Halbkugel – Oberfläche und Materialbedarf.")

def t_raeder(p):
    rad1, rad2, sym_x, sym_y, wer = p
    n1, n2 = len(rad1), len(rad2)
    syms = sorted(set(rad1 + rad2))
    def anteil(rad, s):
        return Fr(rad.count(s), len(rad))
    p_gleich = sum(anteil(rad1, s) * anteil(rad2, s) for s in syms)
    px1, px2 = anteil(rad1, sym_x), anteil(rad2, sym_x)
    p_genau_x = px1 * (1 - px2) + (1 - px1) * px2
    py1, py2 = anteil(rad1, sym_y), anteil(rad2, sym_y)
    p_hoech_y = 1 - py1 * py2
    aufg = (svg_raeder(rad1, rad2) +
        f"<p>{wer} dreht zwei Glücksräder, die sich unabhängig voneinander drehen "
        "(alle Felder eines Rades sind gleich groß). Nach dem Stehenbleiben zeigt "
        "jedes Rad auf ein Symbol.</p>"
        "<p>Berechnen Sie die Wahrscheinlichkeit für folgende Ereignisse:</p>"
        "<ul><li><b>zwei gleiche Symbole</b></li>"
        f"<li><b>genau einmal das Symbol {sym_x}</b></li>"
        f"<li><b>höchstens einmal das Symbol {sym_y}</b></li></ul>")
    def zf(fr):
        return f"{fr.numerator}/{fr.denominator} ≈ {float(fr)*100:.1f} %".replace(".", ",")
    loes = (f"<p>P(zwei gleiche) = <b>{zf(p_gleich)}</b></p>"
        f"<p>P(genau einmal {sym_x}) = <b>{zf(p_genau_x)}</b></p>"
        f"<p>P(höchstens einmal {sym_y}) = <b>{zf(p_hoech_y)}</b> "
        f'<span class="zw">[1 − P(zweimal {sym_y})]</span></p>')
    return T("A2/4", 3, [STOCH], "a2_p4", aufg, loes,
             "Zwei unabhängige Glücksräder – drei Wahrscheinlichkeiten.")

def t_lgs(p):
    a1, b1, c1, a2, b2, c2 = p
    det = a1 * b2 - a2 * b1
    assert det != 0
    x = Fr(c1 * b2 - c2 * b1, det)
    y = Fr(a1 * c2 - a2 * c1, det)
    assert x.denominator == 1 and y.denominator == 1
    def gl(a, b, c):
        bt = f"+ {b}y" if b >= 0 else f"− {-b}y"
        return f"{a}x {bt} = {c}"
    aufg = ("<p>Lösen Sie das Gleichungssystem.</p>"
        f'<p class="formel" style="margin-left:30px;font-size:16px;line-height:1.9">'
        f"I&nbsp;&nbsp;&nbsp;{gl(a1,b1,c1)}<br>II&nbsp;&nbsp;{gl(a2,b2,c2)}</p>")
    loes = (f'<p><span class="ergebnis">x = {x}; y = {y}</span> '
        f'<span class="zw">[z.&thinsp;B. Additions- oder Einsetzungsverfahren, '
        f"Probe in I und II]</span></p>")
    return T("A2/5", 3, [ALG], "a2_p5", aufg, loes,
             "Lineares Gleichungssystem lösen.")

def t_boxplot_vergleich(p):
    kontext, einheit, amax, schritt, name1, d1, name2, d2, aussagen = p
    aufg = (f"<p>{kontext} Die Ergebnisse sind in den beiden Boxplots dargestellt "
        "(je 25 Schülerinnen und Schüler).</p>"
        + svg_miniboxplot(*d1, amax, schritt, einheit, name1)
        + svg_miniboxplot(*d2, amax, schritt, einheit, name2) +
        "<p><b>Kreuzen Sie das jeweils Zutreffende an.</b> ✎</p>"
        '<table><tr><td style="border:none"></td><th>stimmt</th><th>stimmt nicht</th>'
        '<th>Entscheidung nicht möglich</th></tr>'
        + "".join(f'<tr><td style="text-align:left;font-size:13px">{a}</td>'
                  f"<td>{CB}</td><td>{CB}</td><td>{CB}</td></tr>"
                  for a, _ in aussagen) + "</table>")
    loes = "<p>" + "<br>".join(f"{i+1}. <b>{erg}</b> – {a}"
                               for i, (a, erg) in enumerate(aussagen)) + "</p>"
    return T("A2/6", 3, [STOCH], "a2_p6", aufg, loes,
             "Zwei Boxplots vergleichen – Aussagen bewerten.")

# ---------- neue B-Typen ----------

def t_trapez_flaeche(p):
    AB, BC, beta = p
    b = math.radians(beta)
    h = BC * math.sin(b)
    Cx = AB - BC * math.cos(b)
    Ex = (AB * AB - Cx * Cx - h * h) / (2 * (AB - Cx))
    assert 0.5 < Ex < AB - 0.5
    EB = AB - Ex
    EC = math.hypot(Cx - Ex, h)
    assert abs(EB - EC) < 1e-9
    A = (Ex + Cx) / 2 * h
    aufg = (svg_trapez(AB, BC, beta, Ex, Cx, h) +
        "<p>Im rechtwinkligen Trapez ABCD liegt das gleichschenklige Dreieck EBC "
        f"({us('EB')} = {us('EC')}).</p><p>Es gilt:</p>"
        f'<div class="geg">{us("AB")} = {fmt(AB,1)} cm<br>{us("BC")} = {fmt(BC,1)} cm<br>'
        f"&beta; = {fmt(beta,1)}°</div>"
        "<ul><li><b>Berechnen Sie den Flächeninhalt des Vierecks AECD.</b></li></ul>")
    loes = (f'<p class="zw">h = AD = BC · sin β = {fmt(h)} cm · '
        f"DC = AB − BC · cos β = {fmt(Cx)} cm</p>"
        f'<p class="zw">Gleichschenkligkeit: EB = EC → AE = {fmt(Ex)} cm '
        f"[EB = {fmt(EB)} cm]</p>"
        f'<p><span class="ergebnis">A = (AE + DC) / 2 · h ≈ {fmt(A,1)} cm²</span> '
        '<span class="zw">[Trapez AECD]</span></p>')
    return T("B1a", 5, [TRIG], "b_1a", aufg, loes,
             "Rechtwinkliges Trapez mit gleichschenkligem Dreieck – Fläche des Vierecks AECD.")

def t_pyramide_umfang(p):
    a, h = p
    AC = a * math.sqrt(3)
    SA = math.sqrt(a * a + h * h)
    u = AC + 2 * SA
    aufg = (svg_pyramide_diag() +
        "<p>In einer regelmäßigen sechsseitigen Pyramide liegt das Dreieck ACS "
        "(A und C sind übernächste Eckpunkte der Grundfläche, S ist die Spitze).</p>"
        "<p>Es gilt:</p>"
        f'<div class="geg">a = {fmt(a,1)} cm<br>h = {fmt(h,1)} cm</div>'
        "<ul><li><b>Berechnen Sie den Umfang des Dreiecks ACS.</b></li></ul>")
    loes = (f'<p class="zw">Diagonale AC = a · √3 = {fmt(AC)} cm '
        "[Sechseck: übernächste Ecken]</p>"
        f'<p class="zw">Abstand Mittelpunkt–Ecke = a → SA = SC = √(a² + h²) = {fmt(SA)} cm</p>'
        f'<p><span class="ergebnis">u = AC + 2 · SA ≈ {fmt(u,1)} cm</span></p>')
    return T("B2b", 5, [KOERPER, TRIG], "b_2b", aufg, loes,
             "Sechsseitige Pyramide – Umfang des Diagonaldreiecks ACS.")

def t_karten_behauptung(p):
    kontext, typen, n1, n2, n3, k_umdrehen, sicher_typ, g1, g2, g3, wer, name = p
    N = n1 + n2 + n3
    counts = {typen[0]: n1, typen[1]: n2, typen[2]: n3}
    nicht = N - counts[sicher_typ]
    stimmt = k_umdrehen > nicht
    p11 = Fr(n1 * (n1 - 1), N * (N - 1))
    p22 = Fr(n2 * (n2 - 1), N * (N - 1))
    p12 = Fr(2 * n1 * n2, N * (N - 1))
    E = p11 * Fr(int(g1 * 100), 100) + p22 * Fr(int(g2 * 100), 100) + p12 * Fr(int(g3 * 100), 100) - 1
    fair = (1 - (p22 * Fr(int(g2 * 100), 100) + p12 * Fr(int(g3 * 100), 100))) / p11
    fair_f = float(fair)
    assert abs(fair_f * 2 - round(fair_f * 2)) < 1e-9, fair_f
    tab = ('<table class="fig"><tr><th>Ereignis</th><th>Gewinn</th></tr>'
           f"<tr><td>zweimal {typen[0]}</td><td>{geld(g1)}</td></tr>"
           f"<tr><td>zweimal {typen[1]}</td><td>{geld(g2)}</td></tr>"
           f"<tr><td>{typen[0]} und {typen[1]}</td><td>{geld(g3)}</td></tr>"
           '<tr><td colspan="2">Einsatz 1,00 €</td></tr></table>')
    aufg = (tab + f"<p>{kontext} {N} gleich große Karten sind mit drei Symbolen bedruckt "
        f"({n1}-mal {typen[0]}, {n2}-mal {typen[1]}, {n3}-mal {typen[2]}). "
        "Die Karten werden gemischt und verdeckt auf den Tisch gelegt.</p>"
        f"<p>{name} behauptet: „Wenn ich {k_umdrehen} Karten umdrehe, ist auf jeden Fall "
        f"eine Karte mit {sicher_typ} dabei.“</p>"
        "<ul><li><b>Überprüfen Sie diese Behauptung. Begründen Sie Ihre Antwort.</b></li></ul>"
        f"<p>Für ein Gewinnspiel werden zwei Karten ohne Zurücklegen aufgedeckt. "
        "Es gilt der abgebildete Gewinnplan.</p>"
        "<ul><li><b>Berechnen Sie den Erwartungswert.</b></li></ul>"
        f"<p>Das Spiel soll fair werden. Dazu wird nur der Gewinn für "
        f"„zweimal {typen[0]}“ verändert.</p>"
        f"<ul><li><b>Wie hoch muss dieser Gewinn sein? Berechnen Sie.</b></li></ul>")
    urteil = ("stimmt" if stimmt else "stimmt nicht")
    def zf(fr):
        return f"{fr.numerator}/{fr.denominator}"
    loes = (f"<p>Es gibt {nicht} Karten ohne {sicher_typ}. "
        f"{'Bei ' + str(k_umdrehen) + ' Karten muss also mindestens eine dabei sein – die Behauptung <b>stimmt</b>.' if stimmt else 'Die Behauptung <b>stimmt nicht</b>.'}</p>"
        + f"<p>E = {zf(p11)} · {geld(g1)} + {zf(p22)} · {geld(g2)} + {zf(p12)} · {geld(g3)} − 1 € = "
        f"<b>{float(E):+.2f} €</b></p>".replace(".", ",")
        + f'<p><span class="ergebnis">Fairer Gewinn: {geld(fair_f)}</span></p>')
    return T("B3a", 5, [STOCH], "b_3a", aufg, loes,
             "Symbolkarten – Behauptung prüfen, Erwartungswert, faires Spiel.")

def t_wurfparabel(p):
    kontext, einl, xa, ya, c, hind, ziel_frage, ziel_antwort, marken = p
    a = (ya - c) / (xa * xa)
    assert abs(a * 1000 - round(a * 1000)) < 1e-6
    xh, hh, hname, erwartet_drueber = hind
    yh = a * xh * xh + c
    assert (yh > hh) == erwartet_drueber
    def sgn(v):
        return ("+ " if v >= 0 else "− ") + fmt(abs(v))
    aufg = (f"<p>{kontext}</p>" + svg_wurf(a, c, xa, marken) +
        f"<p>{einl} Die Flugbahn ist annähernd parabelförmig und lässt sich mit "
        '<span class="formel">y = ax² + c</span> beschreiben (x, y in m; der höchste '
        "Punkt liegt bei x = 0).</p>"
        "<ul><li><b>Berechnen Sie eine mögliche Funktionsgleichung der Parabel.</b></li>"
        f"<li><b>Kommt der Ball über {hname} ({fmt(hh)} m hoch, bei x = {fmt(xh)})? "
        "Begründen Sie rechnerisch.</b></li>"
        f"<li><b>{ziel_frage}</b></li></ul>")
    loes = (f'<p>y = {fmt(a)}x² {sgn(c)} '
        f'<span class="zw">[Scheitel S(0|{fmt(c)}); Punkt ({fmt(xa)}|{fmt(ya)}) einsetzen → a = {fmt(a)}]</span></p>'
        f"<p>y({fmt(xh)}) = {fmt(yh)} m {'&gt;' if yh > hh else '&lt;'} {fmt(hh)} m → "
        f"der Ball kommt {'darüber' if yh > hh else 'nicht darüber'}.</p>"
        f"<p>{ziel_antwort}</p>")
    return T("B3b", 5, [FUNK], "b_3b", aufg, loes,
             "Wurfparabel – Funktionsgleichung, Hindernis und Zielpunkt prüfen.")

# ---------- Rotationsplan ----------

def V(key):
    """Parameter aus dem v1-Satz übernehmen."""
    return key

PLAN = {
"A": {  # entspricht weitgehend dem bisherigen Satz A
    "a1_p1": (v1.t_a1_1, SAETZE["A"]["a1_1"]),
    "a1_p2": (v1.t_a1_2, SAETZE["A"]["a1_2"]),
    "a1_p3": (v1.t_a1_3, SAETZE["A"]["a1_3"]),
    "a1_p4": (v1.t_a1_4, SAETZE["A"]["a1_4"]),
    "a1_p5": (v1.t_a1_5, SAETZE["A"]["a1_5"]),
    "a1_p6": (v1.t_a1_6, SAETZE["A"]["a1_6"]),
    "a1_p7": (v1.t_a1_7, SAETZE["A"]["a1_7"]),
    "a2_p1": (v1.t_a2_1, SAETZE["A"]["a2_1"]),
    "a2_p2": (v1.t_a2_2, SAETZE["A"]["a2_2"]),
    "a2_p3": (v1.t_a2_3, SAETZE["A"]["a2_3"]),
    "a2_p4": (v1.t_a2_4, SAETZE["A"]["a2_4"]),
    "a2_p5": (v1.t_a2_5, SAETZE["A"]["a2_5"]),
    "a2_p6": (v1.t_a2_6, SAETZE["A"]["a2_6"]),
    "b_1a": (v1.t_b1a, SAETZE["A"]["b1a"]),
    "b_1b": (v1.t_b1b, SAETZE["A"]["b1b"]),
    "b_2a": (v1.t_b2a, SAETZE["A"]["b2a"]),
    "b_2b": (v1.t_b2b, SAETZE["A"]["b2b"]),
    "b_3a": (v1.t_b3a, SAETZE["A"]["b3a"]),
    "b_3b": (v1.t_b3b, SAETZE["A"]["b3b"]),
},
"B": {
    "a1_p1": (t_koerper_ankreuz, "zylhk"),
    "a1_p2": (v1.t_a1_2, SAETZE["B"]["a1_2"]),
    "a1_p3": (t_gleichung_faktor, (5, -2)),
    "a1_p4": (v1.t_a1_4, SAETZE["B"]["a1_4"]),
    "a1_p5": (t_sin_ergaenzen, (40, 170)),
    "a1_p6": (t_parabel_ablesen, (0.5, 2, 1, -1, 1, -2)),
    "a1_p7": (t_prozent_tabelle, ("die Mitgliederzahlen eines Sportvereins",
              "Mitglieder", 2022, 5000, 5500, -20, 5, "—")),
    "a2_p1": (t_quadrat_dreieck, (8.4, 25.0)),
    "a2_p2": (t_zylinder_halbkugel, ("Eine Holz-Spielfigur", 9.0, 6.0,
              "Die Figur wird bis auf die Standfläche lackiert.",
              "anzahl", 1500, "100 ml Lack")),
    "a2_p3": (v1.t_a2_3, SAETZE["B"]["a2_3"]),
    "a2_p4": (t_raeder, (["●", "●", "▲", "▲", "★", "★"],
                          ["●", "●", "▲", "▲", "★", "★"], "★", "●", "Ben")),
    "a2_p5": (t_lgs, (3, 2, 7, 5, -2, 1)),
    "a2_p6": (v1.t_a2_6, SAETZE["B"]["a2_6"]),
    "b_1a": (t_trapez_flaeche, (14.6, 10.8, 34.0)),
    "b_1b": (v1.t_b1b, SAETZE["B"]["b1b"]),
    "b_2a": (v1.t_b2a, SAETZE["B"]["b2a"]),
    "b_2b": (t_pyramide_umfang, (6.0, 9.0)),
    "b_3a": (t_karten_behauptung, ("Beim Spielenachmittag wird ein Kartenspiel angeboten.",
             ("Sonne", "Mond", "Stern"), 3, 3, 4, 7, "Stern", 4.0, 3.0, 2.0, "—", "Claas")),
    "b_3b": (t_wurfparabel, ("Bei einem Volleyball-Aufschlag verlässt der Ball die Hand "
             "in einer Höhe von 1,0 m (bei x = −4). Am höchsten Punkt erreicht er 5,0 m.",
             "Der Aufschlag wird von der Grundlinie ausgeführt.",
             -4, 1.0, 5.0, (1, 2.43, "das Netz", True),
             "Der Ball darf höchstens 9 m hinter dem Netz landen. Prüfen Sie rechnerisch, "
             "ob der Ball im Feld landet.",
             "Landung: 0 = −0,25x² + 5 → x = √20 ≈ 4,5 → der Ball landet ca. 3,5 m "
             "hinter dem Netz, also <b>im Feld</b>.",
             [(1, "Netz")])),
},
"C": {
    "a1_p1": (t_behaelter, ([(2, 3, 3), (1, 4, 3), (1, 2, 1), (1, 2, 2)], Fr(1, 4), "Nora")),
    "a1_p2": (v1.t_a1_2, SAETZE["C"]["a1_2"]),
    "a1_p3": (v1.t_a1_3, SAETZE["C"]["a1_3"]),
    "a1_p4": (v1.t_a1_4, SAETZE["C"]["a1_4"]),
    "a1_p5": (v1.t_a1_5, SAETZE["C"]["a1_5"]),
    "a1_p6": (v1.t_a1_6, SAETZE["C"]["a1_6"]),
    "a1_p7": (v1.t_a1_7, SAETZE["C"]["a1_7"]),
    "a2_p1": (t_quadrat_dreieck, (7.5, 32.0)),
    "a2_p2": (v1.t_a2_2, SAETZE["C"]["a2_2"]),
    "a2_p3": (v1.t_a2_3, SAETZE["C"]["a2_3"]),
    "a2_p4": (v1.t_a2_4, SAETZE["C"]["a2_4"]),
    "a2_p5": (v1.t_a2_5, SAETZE["C"]["a2_5"]),
    "a2_p6": (t_boxplot_vergleich, ("Beim Standweitsprung treten die Klassen 10a und "
              "10b gegeneinander an.", "Weite in cm", 250, 25,
              "Klasse 10a", (150, 170, 185, 200, 225),
              "Klasse 10b", (155, 170, 180, 190, 220),
              [("Der weiteste Sprung gelang in der Klasse 10a.", "stimmt"),
               ("Mindestens 50 % der Klasse 10b erreichten 180 cm oder mehr.", "stimmt"),
               ("Die durchschnittliche Weite der Klasse 10a betrug 185 cm.", "Entscheidung nicht möglich"),
               ("Mindestens 75 % der Klasse 10a sprangen 200 cm oder weiter.", "stimmt nicht")])),
    "b_1a": (v1.t_b1a, SAETZE["C"]["b1a"]),
    "b_1b": (v1.t_b1b, SAETZE["C"]["b1b"]),
    "b_2a": (v1.t_b2a, SAETZE["C"]["b2a"]),
    "b_2b": (v1.t_b2b, SAETZE["C"]["b2b"]),
    "b_3a": (v1.t_b3a, SAETZE["C"]["b3a"]),
    "b_3b": (v1.t_b3b, SAETZE["C"]["b3b"]),
},
"D": {
    "a1_p1": (t_koerper_ankreuz, "wuerfelpyr"),
    "a1_p2": (v1.t_a1_2, SAETZE["D"]["a1_2"]),
    "a1_p3": (t_gleichung_faktor, (-6, 3)),
    "a1_p4": (v1.t_a1_4, SAETZE["D"]["a1_4"]),
    "a1_p5": (t_sin_ergaenzen, (65, 150)),
    "a1_p6": (t_parabel_ablesen, (0.5, -3, -1, 2, -1, -3)),
    "a1_p7": (t_prozent_tabelle, ("die Verkaufszahlen von Saisonkarten",
              "Saisonkarten", 2022, 4000, 5000, -10, 20, "—")),
    "a2_p1": (v1.t_a2_1, SAETZE["D"]["a2_1"]),
    "a2_p2": (t_zylinder_halbkugel, ("Eine Abdeckkappe für Zaunpfosten", 12.0, 8.0,
              "Die Kappe wird außen vollständig beschichtet (bis auf die Unterseite).",
              "menge", 25, "")),
    "a2_p3": (v1.t_a2_3, SAETZE["D"]["a2_3"]),
    "a2_p4": (t_raeder, (["●", "●", "▲", "★"], ["●", "▲", "▲", "★"], "▲", "★", "Emma")),
    "a2_p5": (t_lgs, (2, 3, 12, 4, -1, 10)),
    "a2_p6": (v1.t_a2_6, SAETZE["D"]["a2_6"]),
    "b_1a": (t_trapez_flaeche, (13.2, 9.6, 38.0)),
    "b_1b": (v1.t_b1b, SAETZE["D"]["b1b"]),
    "b_2a": (v1.t_b2a, SAETZE["D"]["b2a"]),
    "b_2b": (t_pyramide_umfang, (5.5, 8.0)),
    "b_3a": (t_karten_behauptung, ("Auf dem Schulfest gibt es ein Umdreh-Spiel.",
             ("Kreis", "Quadrat", "Dreieck"), 2, 4, 4, 9, "Kreis", 8.0, 2.0, 2.0, "—", "Merve")),
    "b_3b": (t_wurfparabel, ("Bei einem Freistoß verlässt der Ball den Boden (bei x = −6). "
             "Am höchsten Punkt erreicht er 4,5 m.",
             "Der Freistoß wird flach über eine Mauer geschossen.",
             -6, 0.0, 4.5, (-2, 2.3, "die Mauer", True),
             "Die Torlinie liegt bei x = 6. In welcher Höhe erreicht der Ball die "
             "Torlinie? Beurteilen Sie.",
             "y(6) = −0,125 · 36 + 4,5 = 0 → der Ball kommt <b>genau auf der Torlinie</b> "
             "auf dem Boden auf.",
             [(-2, "Mauer"), (6, "Torlinie")])),
},
"E": {
    "a1_p1": (t_behaelter, ([(1, 1, 2), (1, 2, 2), (1, 1, 1), (1, 1, 2)], Fr(1, 4), "Luis")),
    "a1_p2": (v1.t_a1_2, SAETZE["E"]["a1_2"]),
    "a1_p3": (t_gleichung_faktor, (8, -4)),
    "a1_p4": (v1.t_a1_4, SAETZE["E"]["a1_4"]),
    "a1_p5": (v1.t_a1_5, SAETZE["E"]["a1_5"]),
    "a1_p6": (v1.t_a1_6, SAETZE["E"]["a1_6"]),
    "a1_p7": (t_prozent_tabelle, ("die Abo-Zahlen eines Schülermagazins",
              "Abos", 2022, 20000, 22000, -15, 10, "—")),
    "a2_p1": (t_quadrat_dreieck, (9.0, 28.0)),
    "a2_p2": (v1.t_a2_2, SAETZE["E"]["a2_2"]),
    "a2_p3": (v1.t_a2_3, SAETZE["E"]["a2_3"]),
    "a2_p4": (t_raeder, (["♥", "♥", "★", "★", "●"], ["♥", "♥", "★", "★", "●"], "●", "♥", "Ida")),
    "a2_p5": (v1.t_a2_5, SAETZE["E"]["a2_5"]),
    "a2_p6": (t_boxplot_vergleich, ("Beim 1000-m-Lauf treten die Klassen 10c und 10d "
              "gegeneinander an.", "Zeit in s", 320, 40,
              "Klasse 10c", (210, 230, 245, 260, 300),
              "Klasse 10d", (215, 225, 240, 265, 290),
              [("Die schnellste Zeit wurde in der Klasse 10c gelaufen.", "stimmt"),
               ("Mindestens die Hälfte der Klasse 10d brauchte höchstens 225 s.", "stimmt nicht"),
               ("Ein Viertel der Klasse 10c brauchte 260 s oder mehr.", "stimmt"),
               ("Die durchschnittliche Zeit der Klasse 10d betrug 240 s.", "Entscheidung nicht möglich")])),
    "b_1a": (t_trapez_flaeche, (15.0, 10.2, 32.0)),
    "b_1b": (v1.t_b1b, SAETZE["E"]["b1b"]),
    "b_2a": (v1.t_b2a, SAETZE["E"]["b2a"]),
    "b_2b": (v1.t_b2b, SAETZE["E"]["b2b"]),
    "b_3a": (v1.t_b3a, SAETZE["E"]["b3a"]),
    "b_3b": (t_wurfparabel, ("Bei einem Freiwurf verlässt der Basketball die Hände "
             "in einer Höhe von 2,0 m (bei x = −2). Am höchsten Punkt erreicht er 4,0 m.",
             "Der Wurf erfolgt aus dem Stand.",
             -2, 2.0, 4.0, (1.5, 3.05, "den Korbring", False),
             "In welcher Entfernung vom höchsten Punkt würde der Ball auf dem Boden "
             "aufkommen? Berechnen Sie.",
             "0 = −0,5x² + 4 → x = √8 ≈ 2,8 → der Ball käme ca. <b>2,8 m hinter dem "
             "höchsten Punkt</b> auf.",
             [(1.5, "Korb")])),
},
}

SLOTS = ["a1_p1", "a1_p2", "a1_p3", "a1_p4", "a1_p5", "a1_p6", "a1_p7",
         "a2_p1", "a2_p2", "a2_p3", "a2_p4", "a2_p5", "a2_p6",
         "b_1a", "b_1b", "b_2a", "b_2b", "b_3a", "b_3b"]

def main():
    eintraege = []
    for satz in "ABCDE":
        tasks = []
        for slot in SLOTS:
            fn, params = PLAN[satz][slot]
            try:
                t = fn(params)
            except AssertionError as ex:
                print(f"!! Satz {satz} {slot} ({fn.__name__}): {ex}")
                raise
            assert t["slugrest"] == slot, (satz, slot, t["slugrest"])
            tasks.append(t)
        s_a1 = sum(t["punkte"] for t in tasks if t["label"].startswith("A1"))
        s_a2 = sum(t["punkte"] for t in tasks if t["label"].startswith("A2"))
        assert s_a1 == 10 and s_a2 == 20, (satz, s_a1, s_a2)
        typen = [PLAN[satz][s][0].__name__ for s in SLOTS]
        for t in tasks:
            a_name = f"a_{satz}_{t['slugrest']}.html"
            l_name = f"l_{satz}_{t['slugrest']}.html"
            (UE / a_name).write_text(seite(
                f"Übungssatz {satz} · {t['label']}",
                kopfzeile(satz, t["label"], t["punkte"], "a") + t["aufg"]), encoding="utf-8")
            (UE / l_name).write_text(seite(
                f"Übungssatz {satz} · {t['label']} – Lösung",
                kopfzeile(satz, t["label"], t["punkte"], "l") + t["loes"]), encoding="utf-8")
            eintraege.append({
                "slug": f"ue{satz.lower()}_{t['slugrest']}",
                "jahr": 0, "satz": satz,
                "teil": teil_von(t["slugrest"]),
                "label": t["label"], "sort": sortkey(t["label"]),
                "themen": t["themen"],
                "aufgabe": f"uebung/{a_name}", "loesung": f"uebung/{l_name}",
                "snippet": t["snippet"],
                "ba": [700, 900, 0], "bl": [700, 700, 0],
            })
        teile_html = []
        akt = None
        for t in tasks:
            tl = teil_von(t["slugrest"])
            if tl != akt:
                teile_html.append(f'<h2 style="border-bottom:2px solid #333;padding-bottom:4px;margin:26px 0 10px">{tl}</h2>')
                akt = tl
            teile_html.append(kopfzeile(satz, t["label"], t["punkte"], "a") + t["aufg"] + '<div class="klar"></div>')
        teile_html.append('<h2 style="border-bottom:2px solid #333;padding-bottom:4px;margin:26px 0 10px;page-break-before:always">Lösungen (für die Lehrkraft)</h2>')
        for t in tasks:
            teile_html.append(kopfzeile(satz, t["label"], t["punkte"], "l") + t["loes"] + '<div class="klar"></div>')
        titel = f"Übungssatz {satz} – Format RSA-Prüfung BW (ab 2021)"
        (UE / f"satz_{satz}_komplett.html").write_text(seite(
            titel, f'<h1 style="font-size:19px">{titel}</h1>'
            '<p style="color:#555;font-size:12.5px">Eigenständig erstelltes Übungsmaterial '
            '– zur freien Verwendung. A1: 10 P (ohne Taschenrechner) · A2: 20 P · '
            'Wahlteil B: zwei von drei Aufgaben (20 P).</p>' + "".join(teile_html)),
            encoding="utf-8")
        print(f"Satz {satz} ok · Typen: {', '.join(sorted(set(typen)))[:110]}")

    src = (ARCHIV / "daten.js").read_text(encoding="utf-8")
    m = re.search(r'const AUFGABEN = (\[.*\]);', src, re.S)
    daten = json.loads(m.group(1))
    daten = [e for e in daten if not e.get("satz")]
    daten += eintraege
    (ARCHIV / "daten.js").write_text(
        src[:m.start(1)] + json.dumps(daten, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    # Variation pro Position ausweisen
    print("\nTyp-Rotation je Position:")
    for slot in SLOTS:
        typen = [PLAN[s][slot][0].__name__.replace("t_", "").replace("v1.", "") for s in "ABCDE"]
        print(f"  {slot}: " + " | ".join(typen))
    print(f"\ndaten.js: {len(daten)} Einträge, davon {len(eintraege)} Übungsaufgaben")

if __name__ == "__main__":
    main()
