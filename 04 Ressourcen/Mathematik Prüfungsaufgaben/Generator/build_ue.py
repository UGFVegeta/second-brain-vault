#!/usr/bin/env python3
"""Generator für 5 Übungssätze (A–E) im Format der RSA-Prüfung BW ab 2021.

Jeder Aufgabentyp ist parametrisiert, rechnet seine Lösung selbst und
verifiziert die Konsistenz (assert). Ausgabe: Einzelseiten pro Aufgabe
(Aufgabe + Lösung), Komplettdokument je Satz, Einträge für daten.js.
"""
import math
import json
import re
from fractions import Fraction as Fr
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from ue_lib import (fmt, geld, tsd, seite, kopfzeile, us, svg_quader_pyramide,
                    svg_baum, svg_muster, cells_kreuz, cells_L, cells_T,
                    cells_rahmen, cells_treppe, svg_boxplot, svg_hbar,
                    svg_vbar, svg_pie, svg_grid_parabeln, svg_trig_rechteck,
                    svg_drachen, svg_pyramide, svg_koerper_vergleich, svg_tunnel)

ARCHIV = Path("/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik Prüfungsaufgaben/Prüfungsarchiv")
UE = ARCHIV / "uebung"
UE.mkdir(exist_ok=True)

TRIG = "Trigonometrie & ebene Geometrie"
KOERPER = "Körperberechnung"
FUNK = "Quadratische Funktionen"
STOCH = "Stochastik & Daten"
ALG = "Algebra & Gleichungen"
SACH = "Sachrechnen & Prozente"
MUSTER = "Muster & Folgen"

def T(label, punkte, themen, slugrest, aufg, loes, snippet):
    return dict(label=label, punkte=punkte, themen=themen, slugrest=slugrest,
                aufg=aufg, loes=loes, snippet=snippet)

# ================= A1 =================

def t_a1_1(p):
    a, b, c, ap = p
    V = a * b * c
    h = Fr(3 * V, ap * ap)
    assert h.denominator in (1, 2), h
    aufg = (svg_quader_pyramide() +
        "<p>Das Volumen eines Quaders und das Volumen einer quadratischen "
        "Pyramide sind gleich groß.</p><p>Für den Quader gilt:</p>"
        f'<div class="geg">a = {a} cm<br>b = {b} cm<br>c = {c} cm</div>'
        "<p>Für die quadratische Pyramide gilt:</p>"
        f'<div class="geg">a<sub>Pyr</sub> = {ap} cm</div>'
        "<p><b>Berechnen Sie die Höhe der quadratischen Pyramide.</b></p>")
    loes = (f"<p>V<sub>Quader</sub> = {a} · {b} · {c} = {V} cm³</p>"
        f"<p>V<sub>Pyr</sub> = ⅓ · a² · h &nbsp;→&nbsp; {V} = ⅓ · {ap*ap} · h</p>"
        f'<p><span class="ergebnis">h = {fmt(float(h),1)} cm</span></p>')
    return T("A1/1", 1.5, [KOERPER], "a1_p1", aufg, loes,
             "Volumen von Quader und quadratischer Pyramide gleich – Höhe berechnen.")

def t_a1_2(p):
    N, n1, n2, n3, farben, namen, wer = p
    assert n1 + n2 + n3 == N
    proz1 = Fr(n1, N)
    k1 = f"{int(proz1*100)} %" if (proz1 * 100).denominator == 1 else None
    l3 = Fr(n3, N)
    # 2. Stufe: Farbe 2 nochmal (Index 1)
    l2 = Fr(n2 - 1, N - 1)
    aufg = (svg_baum(farben, [k1, ("frac", n2, N), None], 1, 1) +
        f"<p>In einem Beutel liegen {namen[0]} ({farben[0]}), {namen[1]} ({farben[1]}) "
        f"und {namen[2]} ({farben[2]}) Kugeln.<br>Es sind insgesamt {N} Kugeln, "
        "die alle gleich groß sind.<br>"
        f"{wer} zieht zwei Kugeln ohne Zurücklegen.</p>"
        "<p><b>Ergänzen Sie in den beiden leeren Feldern die "
        "Wahrscheinlichkeitsangaben.</b> ✎</p>")
    loes = (f"<p>1. Stufe, Feld {farben[2]}: "
        f'<span class="ergebnis">{l3.numerator}/{l3.denominator}</span> '
        f'<span class="zw">[{n3} von {N} Kugeln]</span></p>'
        f"<p>2. Stufe, Feld {farben[1]} → {farben[1]}: "
        f'<span class="ergebnis">{l2.numerator}/{l2.denominator}</span> '
        f'<span class="zw">[nach dem ersten Zug: {n2-1} {namen[1]} von {N-1} Kugeln]</span></p>')
    return T("A1/2", 1, [STOCH], "a1_p2", aufg, loes,
             "Baumdiagramm (Ziehen ohne Zurücklegen) – leere Felder ergänzen.")

def t_a1_3(p):
    d = p  # zweistellige Zahl, z.B. 36
    terme = [(f"0,00{d} · 10<sup>6</sup>", d * 100),
             (f"0,0{d} · 10<sup>4</sup>", d * 10),
             (f"{d//10},{d%10} · 10<sup>5</sup>", d * 10000),
             (f"{d}0 · 10<sup>2</sup>", d * 1000)]
    werte = [w for _, w in terme]
    assert werte[2] == max(werte) and werte.count(max(werte)) == 1
    buchst = ["A", "B", "C", "D"]
    zeile = " &emsp;&emsp; ".join(f"({buchst[i]})&nbsp; {t}" for i, (t, _) in enumerate(terme))
    aufg = ("<p>Gegeben sind vier Terme in Zehnerpotenzschreibweise.</p>"
        f'<p class="formel" style="margin-left:18px">{zeile}</p>'
        "<p><b>Welcher Term hat den größten Wert?<br>"
        "Geben Sie diesen ohne Zehnerpotenzschreibweise an.</b></p>")
    loes = (f'<p>Term (C): <span class="ergebnis">{tsd(werte[2])}</span></p>'
        f'<p class="zw">[(A) {tsd(werte[0])} · (B) {tsd(werte[1])} · (D) {tsd(werte[3])}]</p>')
    return T("A1/3", 1, [ALG], "a1_p3", aufg, loes,
             "Zehnerpotenzen vergleichen – größten Term angeben.")

MUSTER_FAM = {
    "kreuz":  (cells_kreuz,  lambda n: 4 * n + 1, "s = 4n + 1", "s = (2n + 1) + 2n", ["s = 2n + 3", "s = 5n − 1"]),
    "L":      (cells_L,      lambda n: 2 * n + 1, "s = 2n + 1", "s = (n + 1) + n",   ["s = 3n − 1", "s = 2n + 2"]),
    "T":      (cells_T,      lambda n: 3 * n + 1, "s = 3n + 1", "s = (2n + 1) + n",  ["s = 4n − 1", "s = 3n + 2"]),
    "rahmen": (cells_rahmen, lambda n: 4 * n,     "s = 4n",     "s = (n + 1)² − (n − 1)²", ["s = 4n + 4", "s = 3n + 1"]),
    "treppe": (cells_treppe, lambda n: n * (n + 1) // 2, "s = n · (n + 1) : 2", "s = (n² + n) : 2", ["s = 2n − 1", "s = n²"]),
}

def t_a1_4(p):
    fam, nfrag, wer = p
    cells_fn, formel, r1, r2, falsch = MUSTER_FAM[fam]
    for n in (1, 2, 3):
        assert len(cells_fn(n)) == formel(n), (fam, n)
    ziel = formel(nfrag)
    zeilen = []
    for txt, ok in [(r1, True), (falsch[0], False), (r2, True), (falsch[1], False)]:
        zeilen.append(f'<tr><td class="formel" style="text-align:left">{txt}</td>'
                      '<td style="border:none"><span class="cb"></span></td>'
                      '<td style="border:none"><span class="cb"></span></td></tr>')
    aufg = (f"<p>{wer} hat die ersten drei Muster aus Plättchen gelegt.</p>"
        + svg_muster(cells_fn) +
        f"<p>a)&nbsp; <b>Wie viele Plättchen werden für das {nfrag}. Muster benötigt?<br>"
        "&emsp;&nbsp;&nbsp;Begründen Sie Ihre Antwort.</b></p>"
        "<p>b)&nbsp; Welche beiden Formeln beschreiben die Anzahl der Plättchen richtig?<br>"
        "&emsp;&nbsp;&nbsp;<b>Kreuzen Sie jeweils richtig oder falsch an.</b> ✎<br>"
        '&emsp;&nbsp;&nbsp;<span style="font-size:12.5px">(n = Stelle des Musters, '
        's = Anzahl der Plättchen)</span></p>'
        '<table style="margin-left:20px"><tr><td style="border:none"></td>'
        '<th style="border:none;font-weight:normal">richtig</th>'
        '<th style="border:none;font-weight:normal">falsch</th></tr>' + "".join(zeilen) + "</table>")
    folge = ", ".join(str(formel(n)) for n in (1, 2, 3, 4))
    loes = (f'<p>a) <span class="ergebnis">{ziel} Plättchen</span> '
        f'<span class="zw">[Folge: {folge}, … bzw. Formel {r1} mit n = {nfrag}]</span></p>'
        f"<p>b) richtig: <b>{r1}</b> und <b>{r2}</b> · falsch: {falsch[0]}, {falsch[1]} "
        f'<span class="zw">[Probe mit n = 1 und n = 2]</span></p>')
    return T("A1/4", 2, [MUSTER], "a1_p4", aufg, loes,
             "Plättchen-Muster fortsetzen und Formeln prüfen (richtig/falsch).")

def t_a1_5(p):
    funk, winkel = p
    f = math.cos if funk == "cos" else math.sin
    zeilen = []
    ergs = []
    for w in winkel:
        v = f(math.radians(w))
        assert abs(v) > 0.05
        ergs.append("positiv" if v > 0 else "negativ")
        zeilen.append(f'<tr><td class="formel" style="border-left:none;border-right:none">{funk} {w}°</td>'
                      '<td style="border-left:none;border-right:none"><span class="cb"></span></td>'
                      '<td style="border-left:none;border-right:none"><span class="cb"></span></td></tr>')
    aufg = (f"<p><b>Welcher {'Kosinuswert' if funk=='cos' else 'Sinuswert'} ist positiv, "
        "welcher negativ? Kreuzen Sie an.</b> ✎</p>"
        '<table><tr><td style="border:none"></td>'
        '<th style="font-weight:normal;border-top:none;border-left:none;border-right:none">positiv</th>'
        '<th style="font-weight:normal;border-top:none;border-left:none;border-right:none">negativ</th></tr>'
        + "".join(zeilen) + "</table>")
    loes = "<p>" + " · ".join(f"{funk} {w}° <b>{e}</b>" for w, e in zip(winkel, ergs)) + "</p>"
    return T("A1/5", 1, [TRIG], "a1_p5", aufg, loes,
             f"Vorzeichen von {funk}-Werten am Einheitskreis ankreuzen.")

def t_a1_6(p):
    kontext, einheit, daten, fehler_el, fehler_wert, neu, achse_max, schritt, wer = p
    daten = sorted(daten)
    assert len(daten) == 19
    q1, med, q3 = daten[4], daten[9], daten[14]
    korrekt = {"min": daten[0], "q1": q1, "med": med, "q3": q3, "max": daten[-1]}
    assert korrekt[fehler_el] != fehler_wert
    alle = sorted(daten + list(neu))
    med_neu = alle[10]
    stimmt = (med_neu == med)
    eltxt = {"min": "Minimum", "q1": "untere Quartil", "med": "Zentralwert (Median)",
             "q3": "obere Quartil", "max": "Maximum"}[fehler_el]
    aufg = (f"<p>{wer} hat {kontext} gemessen und der Größe nach sortiert.</p>"
        f'<div style="border:1px solid #333;padding:5px 10px;margin:8px 0;font-size:13.5px">'
        f"Messwerte (in {einheit}):<br><br>" + " | ".join(str(v) for v in daten) + "</div>"
        f"<p>Mit dieser Rangliste wurde der folgende Boxplot erstellt.</p>"
        + svg_boxplot(daten[0], q1, med, q3, daten[-1], (fehler_el, fehler_wert),
                      achse_max, schritt, einheit) +
        f"<p>a)&nbsp; Beim Erstellen des Boxplots ist ein Fehler passiert.<br>"
        "&emsp;&nbsp;&nbsp;<b>Beschreiben Sie diesen Fehler.</b></p>"
        f"<p>b)&nbsp; Zwei weitere Messwerte kommen hinzu: {neu[0]} {einheit} und {neu[1]} {einheit}.<br>"
        f"&emsp;&nbsp;&nbsp;{wer} behauptet: „Der Zentralwert ändert sich dadurch nicht.“<br>"
        "&emsp;&nbsp;&nbsp;<b>Überprüfen Sie diese Behauptung und begründen Sie.</b></p>")
    if stimmt:
        begr = (f"Die Behauptung <b>stimmt</b>: Ein neuer Wert liegt unterhalb, einer oberhalb "
                f"des Zentralwerts – der Median bleibt {med} {einheit} (11. von 21 Werten).")
        assert (neu[0] < med) != (neu[1] < med) or med_neu == med
    else:
        begr = (f"Die Behauptung <b>stimmt nicht</b>: Beide neuen Werte liegen auf derselben "
                f"Seite – der Median verschiebt sich von {med} auf {med_neu} {einheit}.")
    loes = (f"<p>a) Das {eltxt} ist falsch eingezeichnet: gezeichnet {fehler_wert} {einheit}, "
        f"richtig <b>{korrekt[fehler_el]} {einheit}</b>.</p>"
        f"<p>b) {begr}</p>"
        f'<p class="zw">[n = 19: Q1 = {q1}, Median = {med}, Q3 = {q3}]</p>')
    return T("A1/6", 2, [STOCH], "a1_p6", aufg, loes,
             f"Boxplot zu {kontext} – Fehler finden, Behauptung zum Zentralwert prüfen.")

def t_a1_7(p):
    titel, gesamt, kats, werte, frage_i, sub, wer = p
    assert sum(werte) == gesamt
    anteil = Fr(werte[frage_i], gesamt)
    assert (anteil * 100).denominator == 1
    p1, p2, txt1, txt2, sub_i = sub
    z1v = werte[sub_i] * p1 / 100.0
    z2v = z1v * p2 / 100.0
    assert abs(z1v - round(z1v)) < 1e-9 and abs(z2v - round(z2v)) < 1e-9
    z1, z2 = round(z1v), round(z2v)
    aufg = (svg_hbar(titel, kats, werte, max(werte)) +
        f"<p>{gesamt} Schülerinnen und Schüler wurden befragt (siehe Diagramm).</p>"
        f"<p>a)&nbsp; <b>Geben Sie den prozentualen Anteil der Befragten an, "
        f"die „{kats[frage_i]}“ gewählt haben.</b></p>"
        f"<p>b)&nbsp; {p1} % der Befragten, die „{kats[sub_i]}“ gewählt haben, {txt1}.<br>"
        f"&emsp;&nbsp;&nbsp;Davon {txt2} {p2} %.</p>"
        f"<p style='margin-left:20px'><b>Berechnen Sie diese Anzahl.</b></p>")
    loes = (f'<p>a) <span class="ergebnis">{int(anteil*100)} %</span> '
        f'<span class="zw">[{werte[frage_i]} von {gesamt}]</span></p>'
        f'<p>b) <span class="ergebnis">{z2}</span> '
        f'<span class="zw">[{p1} % von {werte[sub_i]} = {z1}; {p2} % von {z1} = {z2}]</span></p>')
    return T("A1/7", 1.5, [STOCH, SACH], "a1_p7", aufg, loes,
             f"Balkendiagramm „{titel}“ – Prozentanteil und verschachtelte Prozente.")

# ================= A2 =================

def t_a2_1(p):
    h, L, eps_deg = p
    eps = math.radians(eps_deg)
    EF = L * math.cos(eps)
    FC = L * math.sin(eps)
    wf2 = FC * FC - h * h
    assert wf2 > 0.1, "FC zu kurz"
    wf = math.sqrt(wf2)
    best = None
    f_ = 0.001
    while f_ < EF:
        e2 = EF * EF - f_ * f_
        e_ = math.sqrt(e2)
        w_ = f_ + wf
        res = w_ * w_ + (h - e_) ** 2 - L * L
        if best is None or abs(res) < abs(best[0]):
            best = (res, f_, e_, w_)
        f_ += 0.0002
    res, f_, e_, w_ = best
    assert abs(res) < 0.01 and 0.3 < e_ < h - 0.3 and f_ < w_ - 0.3, (res, e_, w_)
    u = 2 * (w_ + h)
    aufg = (svg_trig_rechteck(w_, h, e_, f_) +
        "<p>Im Rechteck ABCD gilt:</p>"
        f'<div class="geg">{us("BC")} = {fmt(h,1)} cm<br>{us("CE")} = {fmt(L,1)} cm<br>'
        f"&epsilon; = {fmt(eps_deg,1)}°</div>"
        "<p><b>Berechnen Sie den Umfang des Rechtecks ABCD.</b></p>")
    loes = ("<p>Rechtwinkliges Dreieck EFC (rechter Winkel bei F):</p>"
        f'<p class="zw">EF = CE · cos ε = {fmt(EF)} cm · FC = CE · sin ε = {fmt(FC)} cm</p>'
        f'<p class="zw">BF = √(FC² − BC²) = {fmt(wf)} cm · '
        f"AF = √(EF² − AE²) mit AE über EC: AE = {fmt(e_)} cm → AF = {fmt(f_)} cm</p>"
        f'<p class="zw">AB = AF + FB = {fmt(f_)} + {fmt(wf)} = {fmt(w_)} cm</p>'
        f'<p><span class="ergebnis">u = 2 · (AB + BC) ≈ {fmt(u,1)} cm</span></p>')
    return T("A2/1", 4, [TRIG], "a2_p1", aufg, loes,
             "Rechteck mit einbeschriebenem rechtwinkligem Dreieck – Umfang berechnen.")

def t_a2_2(p):
    n, BS, psi_deg = p
    psi = math.radians(psi_deg)
    a = 2 * BS * math.sin(psi / 2)
    hs = BS * math.cos(psi / 2)
    if n == 6:
        ha = (a / 2) * math.sqrt(3)
    else:
        ha = (a / 2) / math.tan(math.pi / n)
    hk2 = hs * hs - ha * ha
    assert hk2 > 4, "Pyramide zu flach"
    hk = math.sqrt(hk2)
    G = n * a * ha / 2
    V = G * hk / 3
    nname = "sechsseitigen" if n == 6 else "fünfseitigen"
    aufg = (svg_pyramide(n) +
        f"<p>Eines der Manteldreiecke der regelmäßigen {nname} Pyramide "
        "ist grau gefärbt.</p><p>Es gilt:</p>"
        f'<div class="geg">{us("BS")} = {fmt(BS,1)} cm<br>&psi; = {fmt(psi_deg,1)}°</div>'
        "<p><b>Berechnen Sie das Volumen der Pyramide.</b></p>")
    loes = (f'<p class="zw">BC = 2 · BS · sin(ψ/2) = {fmt(a)} cm · '
        f"h<sub>s</sub> = BS · cos(ψ/2) = {fmt(hs)} cm</p>"
        f'<p class="zw">Inkreisradius h<sub>a</sub> = {fmt(ha)} cm · '
        f"Körperhöhe h = √(h<sub>s</sub>² − h<sub>a</sub>²) = {fmt(hk)} cm</p>"
        f'<p class="zw">Grundfläche G = {n} · (BC · h<sub>a</sub> / 2) = {fmt(G,1)} cm²</p>'
        f'<p><span class="ergebnis">V = G · h / 3 ≈ {fmt(round(V),0)} cm³</span></p>')
    return T("A2/2", 3.5, [KOERPER, TRIG], "a2_p2", aufg, loes,
             f"Regelmäßige {nname} Pyramide – Volumen aus Kante und Spitzenwinkel.")

def t_a2_3(p):
    kA, cA, u, e, pq, py = p
    # (A) y = -kA x² + cA -> p3 ; (B) y=(x+u)²+e -> p2 ; (C) y=x²+px+q -> p1
    px_, qx = pq
    sx = -px_ / 2.0
    sy = qx - px_ * px_ / 4.0
    m = (py - sy) / (0 - sx)
    assert abs(m - round(m)) < 1e-9, m
    m = round(m)
    fA = lambda x: -kA * x * x + cA
    fB = lambda x: (x + u) ** 2 + e
    fC = lambda x: x * x + px_ * x + qx
    def xgrenzen(f):
        lo = hi = None
        x = -6.4
        while x <= 6.4:
            if -4.4 <= f(x) <= 8.4:
                if lo is None:
                    lo = x
                hi = x
            x += 0.05
        return lo, hi
    gA, gB, gC = xgrenzen(fA), xgrenzen(fB), xgrenzen(fC)
    vB, vC = -u, sx
    def klemm(x, g):
        return max(g[0] + 0.3, min(g[1] - 0.5, x))
    # p2-Label am Außenast auf der Scheitelseite, p1 auf der Gegenseite,
    # p3 (nach unten geöffnet) auf der von p2 abgewandten Seite nahe der Spitze
    # Label in die offene "Schüssel" direkt über dem jeweiligen Scheitel,
    # p3 (nach unten geöffnet) knapp über die Spitze, versetzt zur y-Achse
    lx1 = klemm(vC + 0.3, gC)
    lx2 = klemm(vB + 0.3, gB)
    lx3 = -0.9 if vB >= 0 else 0.9
    funcs = [(fC, gC[0], gC[1], lx1, "p<tspan font-size=\"9\" dy=\"2\">1</tspan>"),
             (fB, gB[0], gB[1], lx2, "p<tspan font-size=\"9\" dy=\"2\">2</tspan>"),
             (fA, gA[0], gA[1], lx3, "p<tspan font-size=\"9\" dy=\"2\">3</tspan>")]
    def sgn(v, mit_plus=True):
        return (("+ " if v >= 0 else "− ") if mit_plus else ("" if v >= 0 else "−")) + fmt(abs(v))
    tA = f"y = −{fmt(kA)}x² + {fmt(cA)}"
    tB = f"y = (x {sgn(u)})² + e"
    tC = f"y = x² {sgn(px_)}x {sgn(qx)}"
    aufg = (svg_grid_parabeln(funcs) +
        "<p>Gegeben sind drei Funktionsgleichungen und drei Graphen.</p>"
        f'<p class="formel">(A)&nbsp; {tA}<br>(B)&nbsp; {tB}<br>(C)&nbsp; {tC}</p>'
        "<ul><li><b>Welcher Graph gehört zu welcher Funktionsgleichung? "
        "Begründen Sie Ihre Entscheidung.</b></li>"
        "<li><b>Bestimmen Sie den Wert für e mithilfe des Schaubildes.</b></li></ul>"
        f"<p>Die Gerade g verläuft durch den Scheitelpunkt S<sub>1</sub> von p<sub>1</sub> "
        f"und durch den Punkt P(0|{fmt(py)}).</p>"
        "<ul><li><b>Bestimmen Sie die Funktionsgleichung der Geraden g.</b></li></ul>")
    loes = (f"<p>(A) → p<sub>3</sub> <span class='zw'>[nach unten geöffnet]</span> · "
        f"(B) → p<sub>2</sub> <span class='zw'>[Scheitel bei x = {fmt(-u)}]</span> · "
        f"(C) → p<sub>1</sub> <span class='zw'>[Scheitelform: S<sub>1</sub>({fmt(sx)}|{fmt(sy)})]</span></p>"
        f'<p>e = <b>{fmt(e)}</b> <span class="zw">[y-Wert des Scheitels von p<sub>2</sub>]</span></p>'
        f'<p><span class="ergebnis">g: y = {fmt(m)}x {sgn(py)}</span> '
        f'<span class="zw">[m = ({fmt(py)} − ({fmt(sy)})) / (0 − {fmt(sx)}) = {fmt(m)}]</span></p>')
    return T("A2/3", 3.5, [FUNK], "a2_p3", aufg, loes,
             "Drei Parabeln zuordnen, Parameter e ablesen, Gerade durch den Scheitel.")

def t_a2_4(p):
    kontext, typen, n1, n2, n3, wer = p
    N = n1 + n2 + n3
    assert N == 20
    p33 = Fr(n3 * (n3 - 1), N * (N - 1))
    p11 = Fr(n1 * (n1 - 1), N * (N - 1))
    ph1 = 1 - p11
    pk2 = Fr((N - n2) * (N - n2 - 1), N * (N - 1))
    tab = ('<table><tr><th>' + kontext[1] + '</th>' +
           "".join(f"<td>{t}</td>" for t in typen) + "</tr>"
           f"<tr><th>Anzahl</th><td>{n1}</td><td>{n2}</td><td>{n3}</td></tr></table>")
    aufg = (f"<p>{kontext[0]}</p>" + tab +
        f"<p>{wer} zieht zwei davon gleichzeitig.</p>"
        "<p>Wie groß ist die Wahrscheinlichkeit, dass</p>"
        f"<ul><li><b>zweimal „{typen[2]}“ gezogen wird?</b></li>"
        f"<li><b>höchstens einmal „{typen[0]}“ gezogen wird?</b></li>"
        f"<li><b>„{typen[1]}“ nicht gezogen wird?</b></li></ul>")
    def zf(fr):
        return f"{fr.numerator}/{fr.denominator} ≈ {float(fr)*100:.1f} %".replace(".", ",")
    loes = (f"<p>P(zweimal {typen[2]}) = <b>{zf(p33)}</b> "
        f'<span class="zw">[{n3}/{N} · {n3-1}/{N-1}]</span></p>'
        f"<p>P(höchstens einmal {typen[0]}) = <b>{zf(ph1)}</b> "
        f'<span class="zw">[1 − {n1}/{N} · {n1-1}/{N-1}]</span></p>'
        f"<p>P(kein {typen[1]}) = <b>{zf(pk2)}</b> "
        f'<span class="zw">[{N-n2}/{N} · {N-n2-1}/{N-1}]</span></p>')
    return T("A2/4", 3, [STOCH], "a2_p4", aufg, loes,
             "Zwei Ziehungen ohne Zurücklegen – drei Wahrscheinlichkeiten berechnen.")

def t_a2_5(p):
    a, b, c, d, e = p
    # (x+a)(x+b) − (x+c)² = x(x+d) + e
    # LHS = (a+b-2c)x + ab - c²  ; RHS = x² + dx + e
    A1 = a + b - 2 * c
    B1 = a * b - c * c
    # 0 = x² + (d - A1)x + (e - B1)
    P = d - A1
    Q = e - B1
    disc = P * P - 4 * Q
    w = int(round(math.sqrt(disc)))
    assert w * w == disc and (P + w) % 2 == 0, "keine ganzzahlige Lösung"
    x1 = (-P - w) // 2
    x2 = (-P + w) // 2
    assert x1 != x2
    for x in (x1, x2):
        assert (x + a) * (x + b) - (x + c) ** 2 == x * (x + d) + e
    def t(v):
        return f"+ {v}" if v >= 0 else f"− {-v}"
    gl = (f"(x {t(a)})(x {t(b)}) − (x {t(c)})² = x(x {t(d)}) {t(e)}")
    aufg = ("<p>Lösen Sie die Gleichung.</p>"
        f'<p class="formel" style="text-align:center;font-size:16px;margin:16px 0">{gl}</p>')
    loes = (f'<p class="zw">Links ausmultiplizieren: {A1}x {t(B1)} · '
        f"Rechts: x² {t(d)}x {t(e)}</p>"
        f'<p class="zw">0 = x² {t(P)}x {t(Q)}</p>'
        f'<p><span class="ergebnis">L = {{{min(x1,x2)}; {max(x1,x2)}}}</span></p>')
    return T("A2/5", 3, [ALG], "a2_p5", aufg, loes,
             "Gleichung mit Binomen lösen – Lösungsmenge bestimmen.")

def t_a2_6(p):
    titel, jahre, werte, extrajahr, plus_proz, a_von, a_bis, kreis_titel, proz, labels, teil_i, teil_abs, teil_name = p
    anstieg = Fr(werte[a_bis] - werte[a_von], werte[a_von]) * 100
    assert anstieg.denominator == 1
    neu = werte[-1] * (100 + plus_proz) // 100
    assert werte[-1] * (100 + plus_proz) % 100 == 0
    grund = werte[-1] * proz[teil_i] // 100
    assert werte[-1] * proz[teil_i] % 100 == 0
    ant = Fr(teil_abs, grund) * 100
    assert ant.denominator == 1
    ymax = ((max(max(werte), neu) // 20000) + 1) * 20000
    aufg = ('<div class="fig">' + svg_vbar(titel, jahre, werte, ymax, ymax // 8, extrajahr)
        + svg_pie(kreis_titel, proz, labels) + "</div>"
        f"<p>Das Diagramm zeigt die Entwicklung: {titel}.</p>"
        f"<ul><li><b>Um wie viel Prozent ist die Anzahl von {jahre[a_von]} bis "
        f"{jahre[a_bis]} insgesamt gestiegen?</b></li></ul>"
        f"<p>Im Jahr {extrajahr} stieg die Anzahl um {plus_proz} % gegenüber dem Vorjahr.</p>"
        f"<ul><li><b>Zeichnen Sie die Säule des Jahres {extrajahr} in das Diagramm ein.</b> ✎</li></ul>"
        f"<p>Das Kreisdiagramm zeigt die Verteilung im Jahr {jahre[-1]}. "
        f"Auf „{labels[teil_i]}“ entfallen dabei {tsd(teil_abs)} {teil_name}.</p>"
        f"<ul><li><b>Berechnen Sie den prozentualen Anteil von {tsd(teil_abs)} an "
        f"der Gruppe „{labels[teil_i]}“.</b></li></ul>")
    loes = (f'<p>a) <span class="ergebnis">{int(anstieg)} %</span> '
        f'<span class="zw">[({tsd(werte[a_bis])} − {tsd(werte[a_von])}) / {tsd(werte[a_von])}]</span></p>'
        f'<p>b) Säule {extrajahr}: <b>{tsd(neu)}</b> '
        f'<span class="zw">[{tsd(werte[-1])} · {fmt(1+plus_proz/100)}]</span></p>'
        f'<p>c) <span class="ergebnis">{int(ant)} %</span> '
        f'<span class="zw">[{proz[teil_i]} % von {tsd(werte[-1])} = {tsd(grund)}; '
        f"{tsd(teil_abs)} / {tsd(grund)}]</span></p>")
    return T("A2/6", 3, [STOCH, SACH], "a2_p6", aufg, loes,
             f"Säulen- und Kreisdiagramm „{titel}“ – prozentuale Veränderungen.")

# ================= Wahlteil B =================

def t_b1a(p):
    AB, BE, eps_deg = p
    BC = BE  # 45°-Konstruktion
    eps = math.radians(eps_deg)
    ex = AB - BE
    gb = BE * math.tan(eps)
    EG = BE / math.cos(eps)
    bec = 45.0
    fdir = math.radians(bec + (bec - eps_deg))
    fx = ex + EG * math.cos(fdir)
    fy = EG * math.sin(fdir)
    assert abs(fy - BC) < 0.01 and 0.3 < fx < AB - 0.3, (fy, fx)
    phi = 90 + eps_deg
    AE = ex
    u = AE + EG + fx + BC
    aufg = (svg_drachen(AB, BC, ex, gb, fx) +
        "<p>Im Rechteck ABCD liegt das Drachenviereck EGCF.</p><p>Es gilt:</p>"
        f'<div class="geg">{us("AB")} = {fmt(AB,1)} cm<br>{us("BC")} = {fmt(BC,1)} cm<br>'
        f'{us("BE")} = {fmt(BE,1)} cm<br>&epsilon; = {fmt(eps_deg,1)}°</div>'
        "<ul><li><b>Berechnen Sie den Winkel &phi;.</b></li>"
        "<li><b>Berechnen Sie den Umfang des Vierecks AEFD.</b></li></ul>")
    loes = (f'<p class="zw">Winkel BEC = 45° [BE = BC] · Winkel GEF = 2 · (45° − ε) = {fmt(2*(45-eps_deg),1)}° · '
        "Winkel GCF = 90°</p>"
        f'<p><span class="ergebnis">φ = (360° − 90° − {fmt(2*(45-eps_deg),1)}°) : 2 = {fmt(phi,1)}°</span></p>'
        f'<p class="zw">GB = BE · tan ε = {fmt(gb)} cm · EG = EF = BE / cos ε = {fmt(EG)} cm · '
        f"FD = {fmt(fx)} cm · AE = {fmt(AE)} cm · DA = {fmt(BC,1)} cm</p>"
        f'<p><span class="ergebnis">u<sub>AEFD</sub> ≈ {fmt(u,1)} cm</span></p>')
    return T("B1a", 5, [TRIG], "b_1a", aufg, loes,
             "Drachenviereck im Rechteck – Winkel φ und Umfang des Restvierecks.")

def t_b1b(p):
    s1x, n1, n2, ax, ay, wer = p
    s2x = (n1 + n2) / 2.0
    sy = -((n2 - n1) / 2.0) ** 2
    m = (ay - sy) / (ax - s1x)
    assert abs(m - round(m)) < 1e-9
    m = round(m)
    cg = sy - m * s1x
    d = abs(s2x - s1x)
    xs = (s2x**2 - s1x**2) / (2 * (s2x - s1x))
    ysP = (xs - s1x) ** 2 + sy
    gxs = m * xs + cg
    stimmt = abs(gxs - ysP) < 1e-9
    def t(v):
        return f"+ {fmt(v)}" if v >= 0 else f"− {fmt(-v)}"
    aufg = ("<p>Die Parabeln p<sub>1</sub> und p<sub>2</sub> sind zwei nach oben geöffnete "
        "verschobene Normalparabeln.<br>"
        f"Die Parabel p<sub>1</sub> hat den Scheitelpunkt S<sub>1</sub>({fmt(s1x)}|{fmt(sy)}).<br>"
        f"Die Parabel p<sub>2</sub> schneidet die x-Achse in N<sub>1</sub>({n1}|0) und N<sub>2</sub>({n2}|0).</p>"
        "<ul><li><b>Bestimmen Sie die Funktionsgleichungen von p<sub>1</sub> und p<sub>2</sub>.</b></li></ul>"
        f"<p>Die Gerade g verläuft durch S<sub>1</sub> und den Punkt A({fmt(ax)}|{fmt(ay)}).</p>"
        "<ul><li><b>Berechnen Sie die Funktionsgleichung von g.</b></li></ul>"
        "<p>Der Punkt S<sub>2</sub> ist der Scheitelpunkt der Parabel p<sub>2</sub>.</p>"
        "<ul><li><b>Berechnen Sie die Entfernung zwischen S<sub>1</sub> und S<sub>2</sub>.</b></li></ul>"
        f"<p>{wer} behauptet: „Die Parabeln p<sub>1</sub> und p<sub>2</sub> sowie die Gerade g "
        "schneiden sich in einem gemeinsamen Punkt.“</p>"
        "<ul><li><b>Überprüfen Sie diese Behauptung. Begründen Sie Ihre Antwort rechnerisch.</b></li></ul>")
    urteil = ("Die Behauptung <b>stimmt</b>: g verläuft durch P." if stimmt else
              f"Die Behauptung <b>stimmt nicht</b>: g({fmt(xs)}) = {fmt(gxs)} ≠ {fmt(ysP)}.")
    loes = (f"<p>p<sub>1</sub>: y = (x {t(-s1x)})² {t(sy)} · "
        f"p<sub>2</sub>: y = (x − {n1})(x − {n2}) = (x {t(-s2x)})² {t(sy)} "
        f'<span class="zw">[S<sub>2</sub>({fmt(s2x)}|{fmt(sy)})]</span></p>'
        f'<p>g: y = {fmt(m)}x {t(cg)} <span class="zw">[m = ({fmt(ay)} − ({fmt(sy)})) / '
        f"({fmt(ax)} − {fmt(s1x)})]</span></p>"
        f'<p>Entfernung S<sub>1</sub>S<sub>2</sub> = <b>{fmt(d)} LE</b> '
        '<span class="zw">[gleiche y-Koordinate]</span></p>'
        f"<p>p<sub>1</sub> ∩ p<sub>2</sub>: x = {fmt(xs)} → P({fmt(xs)}|{fmt(ysP)}). {urteil}</p>")
    return T("B1b", 5, [FUNK], "b_1b", aufg, loes,
             "Zwei Normalparabeln, Gerade durch den Scheitel – Behauptung rechnerisch prüfen.")

def t_b2a(p):
    k, q = p
    b = 1 - k
    disc = b * b + 4 * (k + q)
    w = int(round(math.sqrt(disc)))
    assert w * w == disc and (-b + w) % 2 == 0
    xq = (-b + w) // 2
    xp = (-b - w) // 2
    sx = -b / 2.0
    sy = sx * sx + b * sx - k
    pq_len = xq - xp
    hoeh = q - sy
    A = pq_len * hoeh / 2
    def t(v):
        return f"+ {fmt(v)}" if v >= 0 else f"− {fmt(-v)}"
    aufg = (f"<p>Die Gerade g hat die Funktionsgleichung y = x − {k}.<br>"
        "Sie schneidet die x-Achse im Punkt A und die y-Achse im Punkt B.</p>"
        "<ul><li><b>Bestimmen Sie die Koordinaten der Punkte A und B.</b></li></ul>"
        "<p>Durch die Punkte A und B verläuft die nach oben geöffnete verschobene "
        "Normalparabel p.</p>"
        "<ul><li><b>Berechnen Sie die Funktionsgleichung der Parabel p und die "
        "Koordinaten ihres Scheitelpunktes S.</b></li></ul>"
        f"<p>Die Punkte P(x<sub>P</sub>|{q}) und Q(x<sub>Q</sub>|{q}) liegen auf der Parabel p. "
        "Sie bilden zusammen mit dem Scheitelpunkt S das Dreieck PSQ.</p>"
        "<ul><li><b>Berechnen Sie den Flächeninhalt des Dreiecks PSQ.</b></li></ul>")
    loes = (f"<p>A({k}|0), B(0|−{k})</p>"
        f"<p>p: y = x² {t(b)}x {t(-k)} "
        f'<span class="zw">[c = −{k} wegen B; Punktprobe mit A → b = {b}]</span> · '
        f"S({fmt(sx)}|{fmt(sy)})</p>"
        f'<p class="zw">y = {q}: x² {t(b)}x {t(-k-q)} = 0 → P({xp}|{q}), Q({xq}|{q})</p>'
        f'<p><span class="ergebnis">A = ½ · {pq_len} · {fmt(hoeh)} = {fmt(A)} FE</span></p>')
    return T("B2a", 5, [FUNK], "b_2a", aufg, loes,
             "Gerade, Parabel durch Achsenschnittpunkte, Dreieck mit dem Scheitel.")

def t_b2b(p):
    s, delta_deg, hges = p
    delta = math.radians(delta_deg)
    r = s * math.sin(delta)
    hk = s * math.cos(delta)
    hz = hges - hk
    assert hz > 1, hz
    d = 2 * r
    O1 = math.pi * r * r + 2 * math.pi * r * hz + math.pi * r * s
    a = d
    O2 = 2 * a * a + 4 * a * hges
    diff = O2 - O1
    aufg = (svg_koerper_vergleich() +
        "<p>Die Abbildung zeigt den Achsenschnitt eines zusammengesetzten Körpers "
        "und den Parallelschnitt eines quadratischen Prismas.<br>"
        "Der zusammengesetzte Körper besteht aus einem Zylinder und einem "
        "aufgesetzten Kegel.</p><p>Es gilt:</p>"
        f'<div class="geg">s = {fmt(s,1)} cm<br>&delta; = {fmt(delta_deg,1)}°<br>'
        f"h<sub>ges</sub> = {fmt(hges,1)} cm<br>h<sub>ges</sub> = h<sub>Prisma</sub></div>"
        "<p>Der Durchmesser d des zusammengesetzten Körpers ist genauso lang wie "
        "die Grundkante a des quadratischen Prismas.</p>"
        "<ul><li><b>Berechnen Sie die Differenz der Oberflächeninhalte der beiden "
        "Körper.</b></li></ul>")
    loes = (f'<p class="zw">r = s · sin δ = {fmt(r)} cm · h<sub>Kegel</sub> = s · cos δ = {fmt(hk)} cm · '
        f"h<sub>Zyl</sub> = {fmt(hz)} cm</p>"
        f'<p class="zw">O<sub>Körper</sub> = πr² + 2πr·h<sub>Zyl</sub> + πrs ≈ {fmt(O1,1)} cm²</p>'
        f'<p class="zw">a = d = {fmt(d)} cm · O<sub>Prisma</sub> = 2a² + 4a·h ≈ {fmt(O2,1)} cm²</p>'
        f'<p><span class="ergebnis">Differenz ≈ {fmt(diff,0)} cm²</span></p>')
    return T("B2b", 5, [KOERPER], "b_2b", aufg, loes,
             "Zylinder mit Kegel gegen quadratisches Prisma – Differenz der Oberflächen.")

def t_b3a(p):
    kontext, dinge, nx, ny, nz, g1, g2, g3, wer = p
    N = nx + ny + nz
    assert N == 10
    pxx = Fr(ny * (ny - 1), N * (N - 1))
    pyy = Fr(nz * (nz - 1), N * (N - 1))
    pxy = Fr(2 * ny * nz, N * (N - 1))
    E = pxx * Fr(int(g1 * 100), 100) + pyy * Fr(int(g2 * 100), 100) + pxy * Fr(int(g3 * 100), 100) - 1
    fair = (1 - (pyy * Fr(int(g2 * 100), 100) + pxy * Fr(int(g3 * 100), 100))) / pxx
    fair_f = float(fair)
    assert abs(fair_f * 2 - round(fair_f * 2)) < 1e-9, fair_f  # ganz- oder halbzahlig
    tab = ('<table class="fig"><tr><th>Ereignis</th><th>Gewinn</th></tr>'
           f"<tr><td>zweimal {dinge[1]}</td><td>{geld(g1)}</td></tr>"
           f"<tr><td>zweimal {dinge[2]}</td><td>{geld(g2)}</td></tr>"
           f"<tr><td>{dinge[1]} und {dinge[2]}</td><td>{geld(g3)}</td></tr>"
           '<tr><td colspan="2">Einsatz 1,00 €</td></tr></table>')
    aufg = (tab + f"<p>{kontext}<br>"
        f"Im Behälter liegen {nx} {dinge[0]}, {ny} {dinge[1]} und {nz} {dinge[2]}. "
        f"{wer} zieht zweimal nacheinander, ohne zurückzulegen.</p>"
        f"<ul><li><b>Berechnen Sie die Wahrscheinlichkeit für das Ereignis "
        f"„zweimal {dinge[1]}“.</b></li></ul>"
        "<p>Für ein Glücksspiel wird der abgebildete Gewinnplan verwendet.</p>"
        "<ul><li><b>Berechnen Sie den Erwartungswert.</b></li></ul>"
        "<p>Der Gewinnplan soll so verändert werden, dass das Spiel fair wird. "
        f"Dazu soll nur der Gewinn von „zweimal {dinge[1]}“ verändert werden.</p>"
        f"<ul><li><b>Wie hoch muss der Gewinn für „zweimal {dinge[1]}“ sein?</b></li></ul>")
    def zf(fr):
        return f"{fr.numerator}/{fr.denominator}"
    loes = (f"<p>P(zweimal {dinge[1]}) = <b>{zf(pxx)} ≈ {float(pxx)*100:.1f} %</b> "
        f'<span class="zw">[{ny}/10 · {ny-1}/9]</span></p>'.replace(".", ",")
        + f"<p>E = {zf(pxx)} · {geld(g1)} + {zf(pyy)} · {geld(g2)} + {zf(pxy)} · {geld(g3)} − 1 € = "
        f"<b>{float(E):+.2f} €</b></p>".replace(".", ",")
        + f'<p><span class="ergebnis">Fairer Gewinn: {geld(fair_f)}</span> '
        f'<span class="zw">[0 = {zf(pxx)} · x + {zf(pyy)} · {geld(g2)} + {zf(pxy)} · {geld(g3)} − 1 €]</span></p>')
    return T("B3a", 5, [STOCH], "b_3a", aufg, loes,
             "Glücksspiel – Wahrscheinlichkeit, Erwartungswert und fairer Gewinn.")

def t_b3b(p):
    kontext, obj, H, W, h1, b2 = p
    a = 4.0 * H / (W * W)
    x1q = (H - h1) / a
    x1 = math.sqrt(x1q)
    assert abs(x1 - round(x1)) < 1e-9, x1
    x1 = round(x1)
    A1 = 2 * x1 * h1
    h2 = H - a * (b2 / 2.0) ** 2
    A2 = b2 * h2
    groesser = "Vorschlag 1" if A1 > A2 else "Vorschlag 2"
    aufg = (f"<p>{kontext} Die Form lässt sich mit der Funktionsgleichung "
        '<span class="formel">y = ax² + c</span> beschreiben.</p>'
        + svg_tunnel(H, W, h1, 2 * x1) +
        f"<p>Die maximale Höhe beträgt {fmt(H)} m, die Breite am Boden {fmt(W)} m.</p>"
        "<ul><li><b>Geben Sie eine mögliche Funktionsgleichung an.</b></li></ul>"
        f"<p>In die Vorderseite soll {obj} mittig eingebaut werden. "
        "Dazu werden zwei Vorschläge geprüft.</p>"
        f"<p>Vorschlag 1: Höhe {fmt(h1)} m – die beiden oberen Eckpunkte berühren den "
        "Parabelbogen (siehe Abbildung).</p>"
        "<ul><li><b>Berechnen Sie den Flächeninhalt dieser Fläche.</b></li></ul>"
        f"<p>Vorschlag 2: Breite {fmt(b2)} m.</p>"
        "<ul><li><b>Berechnen Sie die größtmögliche Höhe dieser Fläche.</b></li>"
        "<li><b>Welche der beiden Flächen ist größer? Berechnen Sie.</b></li></ul>")
    loes = (f'<p>y = −{fmt(a)}x² + {fmt(H)} <span class="zw">[S(0|{fmt(H)}); '
        f"Nullstellen bei ±{fmt(W/2)}]</span></p>"
        f"<p>Vorschlag 1: {fmt(h1)} = −{fmt(a)}x² + {fmt(H)} → x = ±{x1} → Breite {2*x1} m, "
        f"<b>A<sub>1</sub> = {fmt(A1)} m²</b></p>"
        f"<p>Vorschlag 2: größtmögliche Höhe y({fmt(b2/2)}) = <b>{fmt(h2)} m</b> → "
        f"A<sub>2</sub> = {fmt(A2)} m²</p>"
        f'<p><span class="ergebnis">{groesser} ist größer.</span></p>')
    return T("B3b", 5, [FUNK], "b_3b", aufg, loes,
             f"Parabelförmige Öffnung – Funktionsgleichung und zwei Flächen-Vorschläge.")

# ================= Parametersätze =================

SAETZE = {
"A": dict(
    a1_1=(6, 5, 2, 6),
    a1_2=(25, 10, 8, 7, ("r", "g", "b"), ("rote", "grüne", "blaue"), "Finja"),
    a1_3=36,
    a1_4=("kreuz", 6, "Timo"),
    a1_5=("cos", (70, 170, 250)),
    a1_6=("die Weitsprung-Ergebnisse ihrer Klasse", "cm",
          [250, 260, 260, 280, 280, 290, 300, 300, 310, 320, 330, 330, 340, 350, 350, 360, 380, 400, 420],
          "q1", 300, (270, 430), 450, 50, "Jana"),
    a1_7=("Beliebteste Pausensnacks", 500, ["Brezel", "Obst", "Müsliriegel", "Sonstige"],
          [200, 125, 100, 75], 2, (60, 20, "sind Mädchen", "bringen ihr Obst von zu Hause mit", 1), "—"),
    a2_1=(5.2, 8.4, 47.0),
    a2_2=(6, 11.0, 36.0),
    a2_3=(0.25, 4, 3, -2, (-4, 3), 3),
    a2_4=(("Beim Kartenspiel „Drachenburg“ liegen 20 Karten verdeckt auf dem Tisch.", "Kartentyp"),
          ["Drache", "Zauberer", "Ritter"], 9, 7, 4, "Mia"),
    a2_5=(1, -4, -3, -5, 2),
    a2_6=("Freibad Sonnenau – Besucher", (2021, 2022, 2023, 2024),
          [80000, 96000, 120000, 126000], 2025, 15, 0, 2, "Besucher 2024 nach Alter",
          [25, 30, 25, 20], ["bis 17 Jahre", "18–39 Jahre", "40–59 Jahre", "ab 60 Jahre"],
          0, 18900, "Mädchen"),
    b1a=(10.2, 6.0, 25.0),
    b1b=(1, 2, 6, 3, 2, "Lena"),
    b2a=(4, 6),
    b2b=(10.4, 38.0, 15.0),
    b3a=("Beim Schulfest bietet die Klasse 10b ein Greifspiel an.",
         ("rote Kugeln", "goldene Kugeln", "silberne Kugeln"), 4, 3, 3, 5.0, 3.0, 2.0, "Ein Spieler"),
    b3b=("Die Vorderseite eines Gewächshaustunnels hat annähernd die Form einer Parabel.",
         "eine rechteckige Türfläche", 8, 16, 6, 12),
),
"B": dict(
    a1_1=(8, 3, 2, 4),
    a1_2=(20, 8, 7, 5, ("r", "ge", "b"), ("rote", "gelbe", "blaue"), "Malte"),
    a1_3=42,
    a1_4=("L", 7, "Aylin"),
    a1_5=("sin", (40, 140, 220)),
    a1_6=("die Schulweg-Zeiten ihrer Klasse", "min",
          [10, 12, 12, 14, 15, 16, 18, 18, 19, 20, 22, 22, 24, 25, 26, 28, 30, 34, 38],
          "q3", 28, (24, 35), 40, 5, "Lea"),
    a1_7=("Gewählte Ausflugsziele", 400, ["Freizeitpark", "Zoo", "Museum", "Sonstige"],
          [160, 100, 80, 60], 1, (45, 25, "fahren zum ersten Mal dorthin", "kommen aus Klasse 5", 0), "—"),
    a2_1=(4.8, 7.9, 51.0),
    a2_2=(5, 10.4, 42.0),
    a2_3=(0.5, 3, -4, -3, (2, -2), 1),
    a2_4=(("An einer Losbude liegen 20 Lose in einer Trommel.", "Losart"),
          ["Niete", "Trostpreis", "Hauptgewinn"], 10, 7, 3, "Ben"),
    a2_5=(2, -5, -4, -6, 4),
    a2_6=("Stadtbücherei – Ausleihen", (2021, 2022, 2023, 2024),
          [60000, 75000, 90000, 96000], 2025, 25, 0, 2, "Ausleihen 2024 nach Bereich",
          [40, 25, 20, 15], ["Kinderbücher", "Romane", "Sachbücher", "Sonstiges"],
          0, 9600, "Comic-Ausleihen"),
    b1a=(11.4, 6.4, 22.0),
    b1b=(-1, 1, 5, 1, 2, "Jonas"),
    b2a=(3, 5),
    b2b=(9.6, 42.0, 14.0),
    b3a=("Auf dem Sommerfest wird ein Beutelspiel angeboten.",
         ("weiße Steine", "goldene Steine", "blaue Steine"), 3, 4, 3, 3.0, 2.0, 1.5, "Eine Spielerin"),
    b3b=("Der Querschnitt eines Foliengewächshauses ist annähernd parabelförmig.",
         "eine rechteckige Türfläche", 9, 12, 5, 10),
),
"C": dict(
    a1_1=(5, 4, 3, 6),
    a1_2=(25, 5, 10, 10, ("s", "w", "gr"), ("schwarze", "weiße", "graue"), "Nora"),
    a1_3=57,
    a1_4=("T", 8, "Deniz"),
    a1_5=("sin", (75, 195, 285)),
    a1_6=("die Sprünge beim Seilspringen (30 Sekunden)", "Sprünge",
          [35, 38, 40, 42, 44, 45, 46, 48, 50, 52, 54, 55, 56, 58, 60, 62, 65, 68, 72],
          "med", 55, (46, 66), 80, 10, "Mara"),
    a1_7=("Lieblings-Haustiere", 250, ["Hund", "Katze", "Nager", "Sonstige"],
          [100, 75, 50, 25], 2, (60, 20, "haben das Tier selbst", "haben es aus dem Tierheim", 1), "—"),
    a2_1=(5.6, 9.2, 44.0),
    a2_2=(6, 12.0, 32.0),
    a2_3=(0.25, 5, 2, -4, (-6, 7), 4),
    a2_4=(("In einer Kiste liegen 20 Trikots in drei Farben.", "Farbe"),
          ["Rot", "Blau", "Gelb"], 10, 6, 4, "Elif"),
    a2_5=(3, -6, -2, -4, -18),
    a2_6=("Fahrradverleih – Ausleihen", (2021, 2022, 2023, 2024),
          [40000, 50000, 60000, 72000], 2025, 10, 0, 2, "Ausleihen 2024 nach Radtyp",
          [25, 35, 25, 15], ["E-Bike", "Tourenrad", "Mountainbike", "Sonstige"],
          0, 4500, "Ausleihen an Touristen"),
    b1a=(9.6, 5.5, 28.0),
    b1b=(-1, 0, 6, 1, -1, "Selin"),
    b2a=(5, 7),
    b2b=(11.2, 35.0, 16.0),
    b3a=("Beim Vereinsfest gibt es ein Muschelspiel.",
         ("Steine", "Muscheln", "Perlen"), 4, 4, 2, 3.0, 5.0, 2.0, "Ein Spieler"),
    b3b=("Ein Brückenbogen über einem Fußweg ist annähernd parabelförmig.",
         "eine rechteckige Durchfahrt", 10, 20, 7.5, 12),
),
"D": dict(
    a1_1=(6, 4, 2, 4),
    a1_2=(25, 6, 9, 10, ("r", "g", "b"), ("rote", "grüne", "blaue"), "Paul"),
    a1_3=73,
    a1_4=("rahmen", 7, "Mia"),
    a1_5=("cos", (55, 125, 305)),
    a1_6=("die Wurfweiten beim Schlagballwurf", "m",
          [16, 17, 17, 18, 19, 20, 21, 22, 22, 23, 24, 25, 26, 27, 28, 29, 31, 33, 36],
          "max", 33, (18, 21), 40, 5, "Timon"),
    a1_7=("Weg zur Schule", 600, ["Bus", "Fahrrad", "zu Fuß", "Sonstige"],
          [240, 180, 120, 60], 1, (35, 25, "fahren weniger als 10 Minuten", "haben einen Sitzplatz", 0), "—"),
    a2_1=(4.5, 7.2, 49.0),
    a2_2=(5, 11.5, 38.0),
    a2_3=(2, 4, -3, -1, (4, 1), 3),
    a2_4=(("In einem Regal stehen 20 Bücher aus drei Genres.", "Genre"),
          ["Krimi", "Fantasy", "Comic"], 8, 8, 4, "Emma"),
    a2_5=(2, -7, -5, -4, -25),
    a2_6=("Konzertbesucher Stadthalle", (2021, 2022, 2023, 2024),
          [30000, 32000, 40000, 48000], 2025, 5, 1, 3, "Besucher 2024 nach Alter",
          [20, 30, 30, 20], ["bis 25 Jahre", "26–45 Jahre", "46–65 Jahre", "ab 66 Jahre"],
          1, 3600, "Dauerkarten-Besitzer"),
    b1a=(10.8, 6.2, 24.0),
    b1b=(0, 2, 6, 1, -2, "Felix"),
    b2a=(2, 4),
    b2b=(8.8, 40.0, 13.0),
    b3a=("Auf dem Herbstmarkt wird ein Kastanienspiel gespielt.",
         ("Kastanien", "goldene Nüsse", "silberne Nüsse"), 4, 3, 3, 4.0, 4.0, 1.5, "Eine Spielerin"),
    b3b=("Der Eingang eines Festzelts hat annähernd Parabelform.",
         "ein rechteckiges Tor", 4, 8, 3, 6),
),
"E": dict(
    a1_1=(9, 4, 2, 6),
    a1_2=(25, 15, 6, 4, ("r", "g", "b"), ("rote", "gelbe", "blaue"), "Luis"),
    a1_3=81,
    a1_4=("treppe", 7, "Hanna"),
    a1_5=("cos", (80, 200, 340)),
    a1_6=("die Zeiten über 1 km im Sportunterricht", "s",
          [222, 228, 230, 235, 238, 240, 244, 248, 250, 252, 256, 258, 262, 265, 268, 272, 280, 290, 300],
          "q1", 244, (236, 274), 320, 40, "Ali"),
    a1_7=("Lieblings-Sportarten", 800, ["Fußball", "Schwimmen", "Turnen", "Sonstige"],
          [320, 200, 160, 120], 1, (40, 12.5, "spielen im Verein", "sind Torhüter", 0), "—"),
    a2_1=(6.0, 9.6, 42.0),
    a2_2=(6, 10.5, 40.0),
    a2_3=(0.5, 6, 4, -2, (-2, -1), 2),
    a2_4=(("In einer Box liegen 20 Sammelfiguren aus drei Serien.", "Serie"),
          ["Tiere", "Fahrzeuge", "Roboter"], 11, 5, 4, "Ida"),
    a2_5=(1, -6, -4, -6, -4),
    a2_6=("Podcast „Schulfunk“ – Abrufe", (2021, 2022, 2023, 2024),
          [150000, 180000, 225000, 240000], 2025, 5, 0, 2, "Abrufe 2024 nach Altersgruppe",
          [30, 35, 20, 15], ["bis 19 Jahre", "20–39 Jahre", "40–59 Jahre", "ab 60 Jahre"],
          0, 18000, "Abrufe über Smart Speaker"),
    b1a=(12.0, 7.0, 20.0),
    b1b=(1, 3, 7, 3, 2, "Noah"),
    b2a=(6, 8),
    b2b=(10.0, 36.0, 15.0),
    b3a=("Beim Schulfest der 10c gibt es ein Angelspiel.",
         ("Fische", "goldene Sterne", "silberne Sterne"), 4, 3, 3, 6.0, 2.0, 2.0, "Ein Spieler"),
    b3b=("Die Vorderseite einer Lagerhalle hat annähernd die Form einer Parabel.",
         "ein rechteckiges Rolltor", 8, 20, 6, 16),
),
}

GENS = [("a1_1", t_a1_1), ("a1_2", t_a1_2), ("a1_3", t_a1_3), ("a1_4", t_a1_4),
        ("a1_5", t_a1_5), ("a1_6", t_a1_6), ("a1_7", t_a1_7),
        ("a2_1", t_a2_1), ("a2_2", t_a2_2), ("a2_3", t_a2_3), ("a2_4", t_a2_4),
        ("a2_5", t_a2_5), ("a2_6", t_a2_6),
        ("b1a", t_b1a), ("b1b", t_b1b), ("b2a", t_b2a), ("b2b", t_b2b),
        ("b3a", t_b3a), ("b3b", t_b3b)]

TEIL = {"a1": "A1 – ohne Taschenrechner", "a2": "A2 – mit Taschenrechner", "b": "Wahlteil B"}

def teil_von(slugrest):
    return TEIL[slugrest.split("_")[0]]

def sortkey(label):
    m = re.match(r'^(A1|A2)/(\d+)$', label)
    if m:
        return f"{m.group(1)}_{int(m.group(2)):03d}"
    m = re.match(r'^B(\d)([ab])$', label)
    return f"B{int(m.group(1)):03d}{m.group(2)}"

def main():
    eintraege = []
    for satz in "ABCDE":
        params = SAETZE[satz]
        tasks = []
        for key, gen in GENS:
            try:
                t = gen(params[key])
            except AssertionError as ex:
                print(f"!! Satz {satz} {key}: Verifikation fehlgeschlagen: {ex}")
                raise
            tasks.append(t)
        summe_a1 = sum(t["punkte"] for t in tasks if t["label"].startswith("A1"))
        summe_a2 = sum(t["punkte"] for t in tasks if t["label"].startswith("A2"))
        assert summe_a1 == 10 and summe_a2 == 20, (satz, summe_a1, summe_a2)
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
        # Komplettdokument
        teile_html = []
        akt_teil = None
        for t in tasks:
            tl = teil_von(t["slugrest"])
            if tl != akt_teil:
                teile_html.append(f'<h2 style="border-bottom:2px solid #333;padding-bottom:4px;margin:26px 0 10px">{tl}</h2>')
                akt_teil = tl
            teile_html.append(kopfzeile(satz, t["label"], t["punkte"], "a") + t["aufg"] + '<div class="klar"></div>')
        teile_html.append('<h2 style="border-bottom:2px solid #333;padding-bottom:4px;margin:26px 0 10px;page-break-before:always">Lösungen (für die Lehrkraft)</h2>')
        for t in tasks:
            teile_html.append(kopfzeile(satz, t["label"], t["punkte"], "l") + t["loes"] + '<div class="klar"></div>')
        titel = f"Übungssatz {satz} – Format RSA-Prüfung BW (ab 2021)"
        kompl = seite(titel, f'<h1 style="font-size:19px">{titel}</h1>'
                      '<p style="color:#555;font-size:12.5px">Eigenständig erstelltes Übungsmaterial '
                      '– zur freien Verwendung. A1: 10 P (ohne Taschenrechner) · A2: 20 P · '
                      'Wahlteil B: zwei von drei Aufgaben (20 P).</p>' + "".join(teile_html))
        (UE / f"satz_{satz}_komplett.html").write_text(kompl, encoding="utf-8")
        print(f"Satz {satz}: {len(tasks)} Aufgaben ok (A1 {summe_a1} P, A2 {summe_a2} P, B {sum(t['punkte'] for t in tasks if t['label'].startswith('B'))} P)")

    # daten.js aktualisieren
    src = (ARCHIV / "daten.js").read_text(encoding="utf-8")
    m = re.search(r'const AUFGABEN = (\[.*\]);', src, re.S)
    daten = json.loads(m.group(1))
    daten = [e for e in daten if not e.get("satz")]
    daten += eintraege
    (ARCHIV / "daten.js").write_text(
        src[:m.start(1)] + json.dumps(daten, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    print(f"daten.js: {len(daten)} Einträge gesamt, davon {len(eintraege)} Übungsaufgaben")

if __name__ == "__main__":
    main()
