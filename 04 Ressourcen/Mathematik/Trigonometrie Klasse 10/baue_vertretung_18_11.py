"""Vertretungsstunde Mathe 10b, Mi 18.11.2026 (45 min): Schnittpunkt 10, S. 16/17, Berechnungen am allgemeinen Dreieck.
Kern: S. 16 Nr. 3 c rechts (stumpfer Winkel, Höhe außerhalb) gemeinsam, danach Übungen ○ ◐ ● und Zusatz.
Baut zwei PDFs: Lösung mit Schritten (für die Vertretung) und Ablaufnotiz. Kein Schülerblatt: Aufgaben aus dem Buch, die Klasse schreibt alles selbst ins Heft (Oskar 17.11.).
Die Funktion schuelerblatt() bleibt nur als Reserve, wird nicht mehr gebaut.
Werte mit Asserts gegen die Buchlösung geprüft. Rechenweg wie in baue_loesung_s15_s16.py: nur sin, cos, Pythagoras.
Ausführen: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 baue_vertretung_18_11.py
"""
import math
import subprocess
from pathlib import Path

from baue_loesung_s15_s16 import (CHROME, ROT, S, C, aS, r1, r2, k, bruch, i, schritt, erg, um,
                                  Skizze, pkt_aus, fuss, dreieck)

import baue_loesung_s15_s16 as _basis
_basis.NR = "①②③④⑤⑥⑦⑧⑨"
HIER = Path(__file__).parent
TITEL = "Mathe 10b – Vertretung 18.11. – Dreieck mit stumpfem Winkel"
N_SCH = f"{TITEL} – Schülerblatt"
N_LOE = f"{TITEL} – Lösung mit Schritten"
N_ABL = f"{TITEL} – Ablauf für die Vertretung"
N_SCHL = f"{TITEL} – Schülerblatt Lösung"
LOES = {}
SUB = lambda t: f"<tspan font-size='2' dy='0.8'>{t}</tspan>"

# ---------------------------------------------------------------- Rechnung
R = {}
# 1) S. 16 Nr. 3 c rechts: b = 4,4 cm, a = 8,4 cm, α = 115°; gesucht c, β
al2 = 65; hc = r2(4.4 * S(al2)); x = r2(4.4 * C(al2)); cx = r2(math.sqrt(8.4**2 - hc**2)); c = r2(cx - x)
q = round(hc / 8.4, 4); be = r1(aS(q))
assert (hc, x, cx, c, be) == (3.99, 1.86, 7.39, 5.53, 28.4)          # Buch: 3,99; 1,85; 7,38; 5,53; 28,4°
R[1] = dict(hc=hc, x=x, cx=cx, c=c, q=q, be=be, ga=r1(180 - 115 - be))
# 2) S. 16 Nr. 3 a links: c = 8,5 cm, a = 8,2 cm, β = 47,0°; gesucht h_c, b, α
hc = r2(8.2 * S(47)); c2 = r2(8.2 * C(47)); c1 = r2(8.5 - c2); b = r2(math.sqrt(hc**2 + c1**2))
q = round(hc / b, 4); al = r1(aS(q))
assert (hc, c2, c1) == (6.0, 5.59, 2.91) and r1(b) == 6.7 and al == 64.1   # Buch: 6,0; 5,59; 2,91; 6,7; 64,1°
R[2] = dict(hc=hc, c2=c2, c1=c1, b=b, q=q, al=al)
# 3) S. 16 Nr. 5 rechts: Flächeninhalt mit A = ½ ⋅ a ⋅ b ⋅ sin γ
A_a = r2(0.5 * 7.1 * 5.9 * S(65.1)); A_b = r2(0.5 * 12.4 * 9.5 * S(52.3))
al_c = r1(180 - 47.7 - 51.9); A_c = r2(0.5 * 8.4 * 9.8 * S(al_c))
assert (r1(A_a), r1(A_b), al_c, r1(A_c)) == (19.0, 46.6, 80.4, 40.6)    # Buch
R[3] = dict(A_a=A_a, A_b=A_b, al_c=al_c, A_c=A_c)
# 4 a) S. 16 Nr. 4 a links: a = 6,9 cm, β = 36,7°, γ = 77,7°, Höhe h_b; gesucht b, c, α
al = r1(180 - 36.7 - 77.7); hb = r2(6.9 * S(77.7)); b2 = r2(6.9 * C(77.7)); cc = r2(hb / S(al))
b1 = r2(math.sqrt(cc**2 - hb**2)); bb = r2(b1 + b2)
assert (al, hb, b2, cc) == (65.6, 6.74, 1.47, 7.40) and r1(bb) == 4.5    # Buch: 65,6°; 6,74; 1,47; 7,40; b = 4,53
R["4a"] = dict(al=al, hb=hb, b2=b2, c=cc, b1=b1, b=bb)
# 4 b) S. 16 Nr. 4 b links: b = 5,0 cm, α = 60,9°, γ = 68,4°, Höhe h_a; gesucht a, c, β
be4 = r1(180 - 60.9 - 68.4); ha = r2(5.0 * S(68.4)); a2 = r2(5.0 * C(68.4)); c4 = r2(ha / S(be4))
a1 = r2(math.sqrt(c4**2 - ha**2)); a4 = r2(a1 + a2)
assert (be4, ha, a2, c4, a1) == (50.7, 4.65, 1.84, 6.01, 3.81) and r1(a4) == 5.7   # Buch: 50,7°; 4,65; 1,84; 6,01; 3,81; 5,65
R["4b"] = dict(be=be4, ha=ha, a2=a2, c=c4, a1=a1, a=a4)
# 5) S. 16 Nr. 7 links: AB = 8,0 cm, α = 20,6°, rechter Winkel bei B, M Mitte von AB; gesucht A und u von AMC
BC = r1(8.0 * math.tan(math.radians(20.6))); AC = r2(math.sqrt(8.0**2 + BC**2)); MC = r2(math.sqrt(4.0**2 + BC**2)); u = r2(4.0 + MC + AC); A7 = r2(0.5 * 4.0 * BC)
assert (AC, BC, MC, A7) == (8.54, 3.0, 5.0, 6.0) and r1(u) == 17.5      # Buch: 8,54; 3,0; 5,0; 17,5; 6,0
R[5] = dict(AC=AC, BC=BC, MC=MC, u=u, A=A7)
# 6) S. 17 Nr. 8 links: 3,0 cm und 5,0 cm mit 68° bzw. 112° dazwischen
Ao = r2(0.5 * 3.0 * 5.0 * S(68)); Au = r2(0.5 * 3.0 * 5.0 * S(112))
assert Ao == Au == 6.95
R[6] = dict(Ao=Ao, Au=Au)
# 7) S. 17 Nr. 10 links: AB = 3,1 km, α = 28°, β = 126°; gesucht Umfang
ga = 180 - 28 - 126; hb7 = r2(3.1 * S(28)); AD = r2(3.1 * C(28)); a7 = r2(hb7 / S(ga))
CD = r2(math.sqrt(a7**2 - hb7**2)); b7 = r2(AD + CD); u7 = r2(3.1 + a7 + b7)
assert (ga, hb7, AD, a7, CD, b7, u7) == (26, 1.46, 2.74, 3.33, 2.99, 5.73, 12.16)   # Buch: 12,16 km
R[7] = dict(ga=ga, hb=hb7, AD=AD, a=a7, CD=CD, b=b7, u=u7)


# ---------------------------------------------------------------- Skizzen
def sk_1(loes, breite=78, hoehe=36):
    P = pkt_aus(5.53, 115, 4.4)
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(Cc, A, B)
    s = Skizze(P, extra=[F, (F[0] - 0.3, 0)], breite=breite, hoehe=hoehe)
    if loes:
        s.linie(F, A, "#222", 0.45, "1.2,0.8"); s.linie(Cc, F, ROT, 0.6); s.rechter(F, A, Cc)
        s.seite(F, A, "x", ab=2.6)
        s.seite(Cc, F, "h" + SUB("c"), ROT, ab=2.6, pos=0.6)
        s.winkel(A, F, Cc, "α'", rt=6.2)
        x_, y_ = s.m(*F); s.text(x_, y_ + 3.6, "F", gr=2.8)
    s.linie(A, B, ROT, 0.8)
    s.seite(A, Cc, "4,4 cm", aussen=False, pos=0.55, ab=4.2); s.seite(B, Cc, "8,4 cm", pos=0.4)
    s.seite(A, B, "c", ROT, fett=True)
    s.winkel(A, B, Cc, "115°", rt=7.5)
    s.winkel(B, A, Cc, "β", ROT, rt=8, fett=True)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_2(loes, breite=46, hoehe=30):
    B = (8.5, 0); P = dreieck((0, 0), B, (8.5 - 8.2 * C(47), 8.2 * S(47)))
    A, Cc = P["A"], P["C"]
    F = fuss(Cc, A, B)
    s = Skizze(P, breite=breite, hoehe=hoehe)
    s.linie(Cc, F, ROT, 0.6); s.rechter(F, B, Cc)
    s.linie(A, Cc, ROT, 0.8)
    s.seite(B, Cc, "8,2 cm"); s.seite(A, Cc, "b", ROT, fett=True)
    s.seite(Cc, F, "h" + SUB("c"), ROT, aussen=False, ab=2.4, pos=0.45)
    if loes:
        s.seite(A, F, "c" + SUB("1"), ab=2.6); s.seite(F, B, "c" + SUB("2"), ab=2.6)
        x_, y_ = s.m(4.25, 0); s.text(x_, y_ + 7.2, "8,5 cm")
    else:
        s.seite(A, B, "8,5 cm")
    s.winkel(A, B, Cc, "α", ROT, rt=6.5, fett=True); s.winkel(B, A, Cc, "47,0°", rt=8.5)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_4a(loes, breite=44, hoehe=28):
    B = (7.40, 0); P = dreieck((0, 0), B, (7.40 - 6.9 * C(36.7), 6.9 * S(36.7)))
    A, Cc = P["A"], P["C"]
    F = fuss(B, A, Cc)
    s = Skizze(P, breite=breite, hoehe=hoehe)
    s.linie(B, F); s.rechter(F, A, B)
    s.linie(A, Cc, ROT, 0.8); s.linie(A, B, ROT, 0.8)
    s.seite(B, Cc, "6,9 cm"); s.seite(A, B, "c", ROT, fett=True)
    if loes:
        s.seite(A, F, "b" + SUB("1"), ROT); s.seite(F, Cc, "b" + SUB("2"), ROT)
    else:
        s.seite(A, Cc, "b", ROT, fett=True)
    s.seite(B, F, "h" + SUB("b"), aussen=False, ab=2.2, pos=0.55)
    s.winkel(A, B, Cc, "α", ROT, rt=6.5, fett=True); s.winkel(B, A, Cc, "", r=3.4); bx, by = s.m(*B); s.text(bx - 12, by - 1.6, "36,7°", gr=2.8)
    s.winkel(Cc, A, B, "77,7°", r=2.6, rt=7)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_4b(loes, breite=40, hoehe=28):
    P = dreieck((0, 0), (6.01, 0), (5.0 * C(60.9), 5.0 * S(60.9)))
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(A, B, Cc)
    s = Skizze(P, breite=breite, hoehe=hoehe)
    s.linie(A, F); s.rechter(F, B, A)
    s.linie(B, Cc, ROT, 0.8); s.linie(A, B, ROT, 0.8)
    s.seite(A, Cc, "5,0 cm"); s.seite(A, B, "c", ROT, fett=True)
    if loes:
        s.seite(F, B, "a" + SUB("1"), ROT); s.seite(Cc, F, "a" + SUB("2"), ROT)
    else:
        s.seite(B, Cc, "a", ROT, fett=True)
    s.seite(A, F, "h" + SUB("a"), aussen=False, ab=1.8, pos=0.6)
    s.winkel(A, B, Cc, "", r=3.4); ax, ay = s.m(*A); s.text(ax + 12, ay - 1.6, "60,9°", gr=2.8); s.winkel(B, A, Cc, "β", ROT, rt=6.5, fett=True)
    s.winkel(Cc, A, B, "68,4°", r=2.6, rt=6.8)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_5(loes, breite=50, hoehe=22):
    BC = 8.0 * S(20.6) / C(20.6)
    P = dreieck((0, 0), (8.0, 0), (8.0, BC))
    A, B, Cc = P["A"], P["B"], P["C"]
    M = (4.0, 0)
    s = Skizze(P, breite=breite, hoehe=hoehe)
    (ax, ay), (mx, my), (cx_, cy_) = s.m(*A), s.m(*M), s.m(*Cc)
    s.teile.append(f'<polygon points="{ax:.2f},{ay:.2f} {mx:.2f},{my:.2f} {cx_:.2f},{cy_:.2f}" fill="#f6d5d0" stroke="none"/>')
    s.linie(M, Cc, "#222", 0.5); s.rechter(B, A, Cc)
    s.winkel(A, B, Cc, "α", rt=7)
    s.text(mx, my + 3.6, "M", gr=3.0)
    if loes:
        s.seite(A, M, "4,0", ab=2.6); s.seite(M, B, "4,0", ab=2.6)
        s.seite(B, Cc, f"{k(R[5]['BC'], 1)}", ROT); s.seite(A, Cc, f"{k(R[5]['AC'])}", ROT)
        x_, y_ = s.m((M[0] + Cc[0]) / 2, (M[1] + Cc[1]) / 2); s.text(x_ + 2.5, y_ + 3, f"{k(R[5]['MC'], 1)}", ROT)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_7(breite=48, hoehe=26):
    P = pkt_aus(3.1, 28, R[7]["b"])
    A, B, Cc = P["A"], P["B"], P["C"]
    D = fuss(B, A, Cc)
    s = Skizze(P, breite=breite, hoehe=hoehe)
    s.linie(B, D, ROT, 0.6); s.rechter(D, A, B)
    s.seite(A, B, "3,1 km"); bdx, bdy = s.m((B[0] + D[0]) / 2, (B[1] + D[1]) / 2); s.text(bdx + 3.2, bdy + 0.6, "h" + SUB("b"), ROT)
    s.seite(A, D, f"{k(R[7]['AD'])}", ROT); s.seite(D, Cc, f"{k(R[7]['CD'])}", ROT)
    s.seite(B, Cc, f"a = {k(R[7]['a'])}", ROT, pos=0.55)
    s.winkel(A, B, Cc, "28°", rt=8); s.winkel(B, A, Cc, "126°", r=2.6, rt=6.8); s.winkel(Cc, A, B, "26°", r=5, rt=9.5)
    x_, y_ = s.m(*D); s.text(x_ - 1.5, y_ - 2.5, "D", gr=2.8)
    for n in "ABC": s.ecke(n)
    return s.svg()


# ---------------------------------------------------------------- gemeinsame Teile
KREIS = {"○": "○", "◐": "◐", "●": "●"}
CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #fff; font-family: Helvetica, Arial, sans-serif; color: #222; }}
.seite {{ width: 210mm; height: 297mm; padding: 8mm 11mm 6mm; overflow: hidden; break-after: page; position: relative; }}
.seite:last-child {{ break-after: auto; }}
.balken {{ background: #d9d9d9; font-weight: 700; font-size: 11pt; padding: 1.8mm 3mm; display: flex; justify-content: space-between; align-items: baseline; }}
.balken span {{ font-weight: 400; font-size: 9pt; }}
.legende {{ font-size: 8.5pt; color: #555; margin: 1.5mm 0 1mm; }}
.auf {{ border-bottom: 0.3mm solid #ccc; padding: 1.8mm 0 1.8mm; break-inside: avoid; }}
.auf h2 {{ font-size: 10.5pt; margin: 0 0 1mm; }}
.auf h2 .q {{ font-weight: 400; font-size: 8.5pt; color: #666; margin-left: 1.5mm; }}
.auf h2 .kr {{ font-size: 11pt; margin-right: 1mm; }}
.txt {{ font-size: 10pt; line-height: 1.4; }}
.reihe {{ display: flex; gap: 4mm; align-items: flex-start; }}
.reihe > .txt {{ flex: 1; }}
.sk {{ flex: 0 0 auto; display: flex; justify-content: center; }}
.luecke {{ display: inline-block; width: 26mm; border-bottom: 0.3mm solid #222; height: 4.5mm; vertical-align: bottom; }}
.weg {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.6mm 6mm; font-size: 10pt; margin-top: 1.5mm; }}
.weg div {{ line-height: 1.55; }}
.weg b {{ display: inline-block; min-width: 5mm; }}
.zwei {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 1mm; }}
.luecke.voll {{ color: {ROT}; font-weight: 700; text-align: center; }}
.loes {{ margin-top: 1.5mm; padding: 1.5mm 2mm; border-left: 0.8mm solid {ROT}; background: #fdf3f6; }}
.loes .sch {{ font-size: 8.6pt; }}
.zwei .loes .schritte {{ grid-template-columns: 1fr 1fr; }}
.zusatz {{ background: #f3f3f3; padding: 1mm 2.5mm; margin-top: 2mm; }}
.tipp {{ font-size: 8.5pt; color: #555; }}
.br {{ display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 0.9em; line-height: 1.15; margin: 0 0.4mm; }}
.br span:first-child {{ border-bottom: 0.25mm solid #222; padding: 0 0.6mm; }}
.wu {{ border-top: 0.25mm solid #222; padding: 0 0.4mm; }}
.erg {{ color: {ROT}; }}
.um {{ white-space: nowrap; color: #777; font-size: 0.9em; margin-left: 1mm; }}
.sch {{ font-size: 9pt; line-height: 1.32; white-space: nowrap; }}
.kopf {{ font-weight: 700; }}
.schritte {{ flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5mm 3mm; }}
.ergebnis {{ font-size: 9.5pt; color: {ROT}; font-weight: 700; margin-top: 1mm; }}
.warum {{ color: #555; font-size: 8.6pt; white-space: normal; }}
.gross .sch {{ font-size: 10.5pt; }}
.gross .schritte {{ grid-template-columns: 1fr 1fr; gap: 1.6mm 6mm; }}
.kasten {{ border: 0.4mm solid {ROT}; padding: 2mm 3mm; font-size: 9.5pt; line-height: 1.45; margin-top: 2.5mm; }}
.fuss {{ position: absolute; bottom: 5mm; left: 11mm; right: 11mm; font-size: 7.5pt; color: #888; display: flex; justify-content: space-between; }}
@media screen {{ body {{ background: #888; }} .seite {{ background: #fff; margin: 6mm auto; box-shadow: 0 1mm 4mm #0005; }} }}
"""


def seite(inhalt, fuss_links, nr):
    return f'<div class="seite">{inhalt}<div class="fuss"><span>{fuss_links}</span><span>Seite {nr}</span></div></div>'


def kopf(rechts):
    return f'<div class="balken">Mathe 10b   Trigonometrie: Berechnungen am allgemeinen Dreieck <span>{rechts}</span></div>'


def auf(nr, kreis, quelle, inhalt):
    k_ = f'<span class="kr">{kreis}</span>' if kreis else ""
    return f'<div class="auf"><h2>{k_}Aufgabe {nr}<span class="q">{quelle}</span></h2>{inhalt}</div>'


def html(name, seiten):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{name}</title><style>{CSS}</style></head>'
            f'<body>{"".join(seiten)}</body></html>')


L = '<span class="luecke"></span>'
hc_, hb_, ha_ = i("h", "c"), i("h", "b"), i("h", "a")
Q = "(Schnittpunkt 10, S. {})"


# ---------------------------------------------------------------- Schülerblatt
def schuelerblatt(loes=False):
    F = lambda v: f'<span class="luecke voll">{v}</span>' if loes else L
    X = lambda nr: f'<div class="loes">{LOES[nr]}</div>' if loes else ''
    a1 = auf(1, "", "Hausaufgabe, gemeinsam besprechen " + Q.format("16 Nr. 3 c, rechte Spalte"),
             '<div class="reihe"><div class="txt">Berechne die Seite <b>c</b> und den Winkel <b>β</b>.<br>'
             'Gegeben: b = 4,4 cm; a = 8,4 cm; α = 115°.<br><br>'
             'Das Problem: α ist stumpf. Die Höhe h<sub>c</sub> von C aus trifft die Seite c nicht.<br>'
             '<b>Trick:</b> c über A hinaus verlängern, von C das Lot fällen. Den Fußpunkt nennen wir F, '
             'die Strecke von F bis A nennen wir x.</div>'
             f'<div class="sk">{sk_1(loes, 100, 46)}</div></div>'
             '<div class="weg">'
             f'<div><b>①</b> Höhe h<sub>c</sub>, F und x in die Skizze einzeichnen</div>'
             f'<div><b>②</b> α\' = 180° − 115° = {F('65,0°')}</div>'
             f'<div><b>③</b> h<sub>c</sub>: sin α\' = {bruch(hc_, "4,4")} &nbsp; h<sub>c</sub> = {F('3,99 cm')}</div>'
             f'<div><b>④</b> x: cos α\' = {bruch("x", "4,4")} &nbsp; x = {F('1,86 cm')}</div>'
             f'<div><b>⑤</b> x + c = √<span class="wu">8,4² − h<sub>c</sub>²</span> = {F('7,39 cm')}</div>'
             f'<div><b>⑥</b> c = (x + c) − x = {F('5,53 cm')}</div>'
             f'<div><b>⑦</b> β: sin β = {bruch(hc_, "8,4")} &nbsp; β = {F('28,4°')}</div>'
             f'<div>Ergebnis: c = {F('5,5 cm')}; β = {F('28,4°')}</div>'
             '</div>')
    a2 = auf(2, "○", Q.format("16 Nr. 3 a, linke Spalte"),
             '<div class="reihe"><div class="txt">Berechne die rot markierten Größen h<sub>c</sub>, b und α. '
             'Beginne mit der Länge h<sub>c</sub>.<br>Gegeben: c = 8,5 cm; a = 8,2 cm; β = 47,0°.<br>'
             '<span class="tipp">Tipp: Die Höhe teilt c in c<sub>1</sub> (bei A) und c<sub>2</sub> (bei B).</span></div>'
             f'<div class="sk">{sk_2(loes, 72, 48)}</div></div>' + X(2))
    a3 = auf(3, "○", Q.format("16 Nr. 5, rechte Spalte"),
             '<div class="txt">Berechne den Flächeninhalt des Dreiecks ABC. Eine Planfigur hilft dir.<br>'
             'a) a = 7,1 cm; b = 5,9 cm; γ = 65,1° &nbsp;&nbsp; b) a = 12,4 cm; c = 9,5 cm; β = 52,3°<br>'
             'c) b = 8,4 cm; c = 9,8 cm; β = 47,7°; γ = 51,9°<br>'
             '<span class="tipp">Formel: A = ½ ⋅ a ⋅ b ⋅ sin γ (zwei Seiten und der Winkel dazwischen). '
             'Bei c) fehlt dir zuerst der Winkel zwischen b und c.</span></div>' + X(3))
    a4 = auf(4, "◐", Q.format("16 Nr. 4, linke Spalte"),
             '<div class="txt">Berechne die rot markierten Größen. Beginne mit der Länge der eingezeichneten Höhe.</div>'
             '<div class="zwei">'
             f'<div><div class="txt">a) a = 6,9 cm; β = 36,7°; γ = 77,7°<br>gesucht: α, b, c</div><div class="sk">{sk_4a(loes, 86, 54)}</div>' + X('4 a') + '</div>'
             f'<div><div class="txt">b) b = 5,0 cm; α = 60,9°; γ = 68,4°<br>gesucht: β, a, c</div><div class="sk">{sk_4b(loes, 76, 54)}</div>' + X('4 b') + '</div>'
             '</div>')
    a5 = auf(5, "●", Q.format("16 Nr. 7, linke Spalte"),
             '<div class="reihe"><div class="txt">Der Punkt M halbiert die Strecke AB. '
             'Berechne den Flächeninhalt und den Umfang des Dreiecks AMC (rot).<br>'
             'Gegeben: AB = 8,0 cm; α = 20,6°; bei B ist ein rechter Winkel.</div>'
             f'<div class="sk">{sk_5(loes, 84, 36)}</div></div>' + X(5))
    a6 = auf(6, "◐", "Zusatz für Schnelle " + Q.format("17 Nr. 8, linke Spalte"),
             '<div class="txt">Zwei Dreiecke haben beide die Seiten 3,0 cm und 5,0 cm. '
             'Beim ersten Dreieck ist der Winkel zwischen ihnen 68°, beim zweiten 112°. '
             'Rosi behauptet, dass beide Dreiecke den gleichen Flächeninhalt haben. Hat Rosi recht? Begründe.<br>'
             '<span class="tipp">Tipp: Je näher γ bei 90° liegt, desto näher liegt sin γ bei 1.</span></div>' + X(6))
    a7 = auf(7, "●", "Zusatz für Schnelle " + Q.format("17 Nr. 10, linke Spalte"),
             '<div class="txt">Für eine Segelregatta ist im Bodensee ein Dreieckskurs ABC vorgesehen: '
             'AB = 3,1 km; α = 28°; β = 126°. Bestimme die Gesamtlänge des Kurses.<br>'
             '<span class="tipp">Tipp: Planfigur zeichnen. β ist stumpf wie in Aufgabe 1. '
             'Zeichne die Höhe von B auf die Seite AC ein.</span></div>' + (f'<div class="reihe"><div class="sk">{sk_7(58, 30)}</div>{X(7)}</div>' if loes else ''))
    leg = '<div class="legende">○ leicht &nbsp; ◐ mittel &nbsp; ● schwer &nbsp;&nbsp; Aufgaben 2 bis 5 rechnest du im Übungsheft, der Reihe nach. Die Lösungen liegen später vorne aus. Taschenrechner auf DEG!</div>'
    fl = "Mathe 10b; Vertretung 18.11." + ("; Lösung" if loes else "")
    kp = kopf("Mi 18.11.2026" + (", Lösung" if loes else ""))
    if loes:
        return html(N_SCHL, [seite(kp + leg + a1 + a2, fl, 1), seite(kp + a3 + a4, fl, 2),
                             seite(kp + a5 + '<div class="zusatz">' + a6 + a7 + "</div>", fl, 3)])
    s1 = seite(kp + leg + a1 + a2 + a3, fl, 1)
    s2 = seite(kp + a4 + a5 + '<div class="zusatz">' + a6 + a7 + "</div>", fl, 2)
    return html(N_SCH, [s1, s2])


# ---------------------------------------------------------------- Lösungsblatt
def sch_w(nr, kopf_, zeilen, warum=""):
    """Schritt mit kurzer Begründung für die Vertretung."""
    w = f'<div class="warum">{warum}</div>' if warum else ""
    return schritt(nr, kopf_, *zeilen)[:-6] + w + "</div>"


def loesung():
    r = R[1]
    s1 = [
        sch_w(1, "Höhe einzeichnen", ["c über A hinaus verlängern,", "Lot von C: Fußpunkt F, Strecke FA = x"],
              "Das Dreieck FBC ist rechtwinklig, das Dreieck FAC auch."),
        sch_w(2, "α':", ["α' = 180° − 115°", erg("α' = 65,0°")], "Nebenwinkel von α im kleinen Dreieck FAC."),
        sch_w(3, f"{hc_}:", [f"sin 65,0° = {bruch(hc_, '4,4')} {um('⋅ 4,4')}", f"{hc_} = 4,4 ⋅ sin 65,0°", erg(f"{hc_} = {k(r['hc'])} cm")],
              "Im Dreieck FAC: h<sub>c</sub> ist Gegenkathete, 4,4 cm die Hypotenuse."),
        sch_w(4, "x:", [f"cos 65,0° = {bruch('x', '4,4')} {um('⋅ 4,4')}", "x = 4,4 ⋅ cos 65,0°", erg(f"x = {k(r['x'])} cm")],
              "Im Dreieck FAC: x ist Ankathete."),
        sch_w(5, "x + c:", [f"x + c = √<span class='wu'>8,4² − {k(r['hc'])}²</span>", erg(f"x + c = {k(r['cx'])} cm")],
              "Pythagoras im großen Dreieck FBC: 8,4 cm ist die Hypotenuse."),
        sch_w(6, "c:", [f"c = {k(r['cx'])} − {k(r['x'])}", erg(f"c = {k(r['c'])} cm")], "x wieder abziehen."),
        sch_w(7, "β:", [f"sin β = {bruch(k(r['hc']), '8,4')}", f"sin β = {k(r['q'], 4)}", erg(f"β = {k(r['be'], 1)}°")],
              "Im großen Dreieck FBC: h<sub>c</sub> liegt β gegenüber. Taste sin⁻¹."),
        sch_w(8, "Probe (wer mag):", [f"γ = 180° − 115° − {k(r['be'], 1)}°", erg(f"γ = {k(r['ga'], 1)}°")],
              "Winkelsumme. γ wird hier nicht verlangt."),
    ]
    teil1 = ('<div class="auf gross"><h2>S. 16 Nr. 3 c rechts<span class="q">gemeinsam: so steht es am Ende an der Tafel und im Heft</span></h2>'
             f'<div class="reihe"><div class="sk">{sk_1(True, 92, 38)}</div></div>'
             f'<div class="schritte" style="margin-top:2mm">{"".join(s1)}</div>'
             f'<div class="ergebnis">Ergebnis: c = {k(r["c"])} cm ≈ {k(r["c"], 1)} cm; β = {k(r["be"], 1)}°</div>'
             '<div class="kasten"><b>So vorgehen:</b> erst die Skizze groß an die Tafel, dann fragen: '
             '„Wo liegt die Höhe von C aus?“ Die Klasse merkt, dass sie die Seite c nicht trifft. '
             'Dann c verlängern und h<sub>c</sub> einzeichnen lassen. Jeden Schritt kurz selbst rechnen lassen '
             '(1 bis 2 Minuten), dann vergleichen und an die Tafel. '
             'Merksatz für die Klasse: <b>Erst die Höhe, dann die rechtwinkligen Dreiecke suchen, dann sin, cos oder Pythagoras.</b><br>'
             '<b>Typische Fehler:</b> Taschenrechner auf RAD statt DEG. Mit 115° statt 65° gerechnet. '
             'Bei ⑤ 8,4² + h<sub>c</sub>² statt minus. Bei ⑥ x vergessen abzuziehen. '
             'Die Buchlösung hat x = 1,85 und c + x = 7,38 (anders gerundet), c = 5,53 cm stimmt.</div></div>')

    # Seite 2: übrige Aufgaben kurz
    r2_, r3, a, b, r5, r6, r7 = R[2], R[3], R["4a"], R["4b"], R[5], R[6], R[7]

    def kurz(nr, kreis, quelle, svg, schritte, ergebnis, hinweis=""):
        h = f'<div class="warum">{hinweis}</div>' if hinweis else ""
        skd = f'<div class="sk">{svg}</div>' if svg else ""
        k_ = f'<span class="kr">{kreis}</span>'
        LOES[nr] = f'<div class="schritte">{"".join(schritte)}</div><div class="ergebnis">Ergebnis: {ergebnis}</div>{h}'
        return (f'<div class="auf"><h2>{k_}{quelle}</h2>'
                f'<div class="reihe">{skd}<div class="schritte">{"".join(schritte)}</div></div>'
                f'<div class="ergebnis">Ergebnis: {ergebnis}</div>{h}</div>')

    t = []
    t.append(kurz(2, "○", "S. 16 Nr. 3 a links", sk_2(True, 54, 34), [
        schritt(1, f"{hc_}:", f"sin 47,0° = {bruch(hc_, '8,2')} {um('⋅ 8,2')}", erg(f"{hc_} = {k(r2_['hc'])} cm")),
        schritt(2, f"{i('c', 2)}:", f"cos 47,0° = {bruch(i('c', 2), '8,2')} {um('⋅ 8,2')}", erg(f"{i('c', 2)} = {k(r2_['c2'])} cm")),
        schritt(3, f"{i('c', 1)}:", f"{i('c', 1)} = 8,5 − {k(r2_['c2'])}", erg(f"{i('c', 1)} = {k(r2_['c1'])} cm")),
        schritt(4, "b:", f"b = √<span class='wu'>{k(r2_['hc'])}² + {k(r2_['c1'])}²</span>", erg(f"b = {k(r2_['b'])} cm")),
        schritt(5, "α:", f"sin α = {bruch(k(r2_['hc']), k(r2_['b']))}", erg(f"α = {k(r2_['al'], 1)}°")),
    ], f"{hc_} = {k(r2_['hc'], 1)} cm; b = {k(r2_['b'], 1)} cm; α = {k(r2_['al'], 1)}°"))
    t.append(kurz(3, "○", "S. 16 Nr. 5 rechts", "", [
        schritt(1, "a)", f"A = {bruch(1, 2)} ⋅ 7,1 ⋅ 5,9 ⋅ sin 65,1°", erg(f"A = {k(r3['A_a'], 1)} cm²")),
        schritt(2, "b)", f"A = {bruch(1, 2)} ⋅ 12,4 ⋅ 9,5 ⋅ sin 52,3°", erg(f"A = {k(r3['A_b'], 1)} cm²")),
        schritt(3, "c)", f"α = 180° − 47,7° − 51,9° = {k(r3['al_c'], 1)}°", f"A = {bruch(1, 2)} ⋅ 8,4 ⋅ 9,8 ⋅ sin {k(r3['al_c'], 1)}°", erg(f"A = {k(r3['A_c'], 1)} cm²")),
    ], f"a) {k(r3['A_a'], 1)} cm²; b) {k(r3['A_b'], 1)} cm²; c) {k(r3['A_c'], 1)} cm²"))
    t.append(kurz("4 a", "◐", "S. 16 Nr. 4 a links", sk_4a(True, 58, 36), [
        schritt(1, "α:", "α = 180° − 36,7° − 77,7°", erg(f"α = {k(a['al'], 1)}°")),
        schritt(2, f"{hb_}:", f"sin 77,7° = {bruch(hb_, '6,9')} {um('⋅ 6,9')}", erg(f"{hb_} = {k(a['hb'])} cm")),
        schritt(3, f"{i('b', 2)}:", f"cos 77,7° = {bruch(i('b', 2), '6,9')} {um('⋅ 6,9')}", erg(f"{i('b', 2)} = {k(a['b2'])} cm")),
        schritt(4, "c:", f"sin {k(a['al'], 1)}° = {bruch(k(a['hb']), 'c')}", f"c = {bruch(k(a['hb']), 'sin ' + k(a['al'], 1) + '°')}", erg(f"c = {k(a['c'])} cm")),
        schritt(5, f"{i('b', 1)}:", f"{i('b', 1)} = √<span class='wu'>{k(a['c'])}² − {k(a['hb'])}²</span>", erg(f"{i('b', 1)} = {k(a['b1'])} cm")),
        schritt(6, "b:", f"b = {k(a['b1'])} + {k(a['b2'])}", erg(f"b = {k(a['b'])} cm")),
    ], f"α = {k(a['al'], 1)}°; b = {k(a['b'], 1)} cm; c = {k(a['c'], 1)} cm", "Buchlösung: b = 4,53 cm (rechnet b<sub>1</sub> mit tan, Rundung)."))
    t.append(kurz("4 b", "◐", "S. 16 Nr. 4 b links", sk_4b(True, 52, 36), [
        schritt(1, "β:", "β = 180° − 60,9° − 68,4°", erg(f"β = {k(b['be'], 1)}°")),
        schritt(2, f"{ha_}:", f"sin 68,4° = {bruch(ha_, '5,0')} {um('⋅ 5,0')}", erg(f"{ha_} = {k(b['ha'])} cm")),
        schritt(3, f"{i('a', 2)}:", f"cos 68,4° = {bruch(i('a', 2), '5,0')} {um('⋅ 5,0')}", erg(f"{i('a', 2)} = {k(b['a2'])} cm")),
        schritt(4, "c:", f"sin {k(b['be'], 1)}° = {bruch(k(b['ha']), 'c')}", erg(f"c = {k(b['c'])} cm")),
        schritt(5, f"{i('a', 1)}:", f"{i('a', 1)} = √<span class='wu'>{k(b['c'])}² − {k(b['ha'])}²</span>", erg(f"{i('a', 1)} = {k(b['a1'])} cm")),
        schritt(6, "a:", f"a = {k(b['a1'])} + {k(b['a2'])}", erg(f"a = {k(b['a'])} cm")),
    ], f"β = {k(b['be'], 1)}°; a = {k(b['a'], 1)} cm; c = {k(b['c'], 1)} cm"))
    t.append(kurz(5, "●", "S. 16 Nr. 7 links", sk_5(True, 56, 26), [
        schritt(1, "BC:", f"tan 20,6° = {bruch('BC', '8,0')} {um('⋅ 8,0')}", erg(f"BC = {k(r5['BC'], 1)} cm")),
        schritt(2, "AC:", f"AC = √<span class='wu'>8,0² + {k(r5['BC'], 1)}²</span>", erg(f"AC = {k(r5['AC'])} cm")),
        schritt(3, "MC:", f"MC = √<span class='wu'>4,0² + {k(r5['BC'], 1)}²</span>", erg(f"MC = {k(r5['MC'], 1)} cm")),
        schritt(4, "u:", f"u = 4,0 + {k(r5['MC'], 1)} + {k(r5['AC'])}", erg(f"u = {k(r5['u'])} cm")),
        schritt(5, "A:", f"A = {bruch(1, 2)} ⋅ AM ⋅ BC", f"A = {bruch(1, 2)} ⋅ 4,0 ⋅ {k(r5['BC'], 1)}", erg(f"A = {k(r5['A'], 1)} cm²")),
    ], f"u ≈ {k(r5['u'], 1)} cm; A = {k(r5['A'], 1)} cm²", "Ohne tan: AC = 8,0 : cos 20,6° = 8,55 cm, dann BC = AC ⋅ sin 20,6°. Die Höhe von AMC ist BC (außerhalb, wie bei Nr. 3 c)."))
    t.append(kurz(6, "◐", "Zusatz, S. 17 Nr. 8 links", "", [
        schritt(1, "oben:", f"A = {bruch(1, 2)} ⋅ 3,0 ⋅ 5,0 ⋅ sin 68°", erg(f"A = {k(r6['Ao'])} cm²")),
        schritt(2, "unten:", f"A = {bruch(1, 2)} ⋅ 3,0 ⋅ 5,0 ⋅ sin 112°", erg(f"A = {k(r6['Au'])} cm²")),
        schritt(3, "Begründung:", "68° + 112° = 180°,", "also sin 68° = sin 112°"),
    ], "Rosi hat recht, beide Dreiecke haben 6,95 cm²."))
    t.append(kurz(7, "●", "Zusatz, S. 17 Nr. 10 links", sk_7(58, 30), [
        schritt(1, "γ:", "γ = 180° − 28° − 126°", erg(f"γ = {R[7]['ga']}°")),
        schritt(2, f"{hb_}:", f"sin 28° = {bruch(hb_, '3,1')} {um('⋅ 3,1')}", erg(f"{hb_} = {k(r7['hb'])} km")),
        schritt(3, "AD:", f"cos 28° = {bruch('AD', '3,1')}", erg(f"AD = {k(r7['AD'])} km")),
        schritt(4, "a:", f"sin 26° = {bruch(k(r7['hb']), 'a')}", erg(f"a = {k(r7['a'])} km")),
        schritt(5, "CD:", f"CD = √<span class='wu'>{k(r7['a'])}² − {k(r7['hb'])}²</span>", erg(f"CD = {k(r7['CD'])} km")),
        schritt(6, "u:", f"b = {k(r7['AD'])} + {k(r7['CD'])} = {k(r7['b'])}", f"u = 3,1 + {k(r7['a'])} + {k(r7['b'])}", erg(f"u = {k(r7['u'])} km")),
    ], f"Der Kurs ist {k(r7['u'])} km lang."))

    p1 = seite(kopf("Lösung für die Vertretung, Mi 18.11.2026") + teil1 + t.pop(0) + t.pop(0), "Mathe 10b; Vertretung 18.11.; Lösung", 1)
    p2 = seite(kopf("Lösung der Übungsaufgaben") + "".join(t), "Mathe 10b; Vertretung 18.11.; Lösung", 2)
    return html(N_LOE, [p1, p2])


# ---------------------------------------------------------------- Ablauf
def ablauf():
    zeilen = [
        ("vorher", "Nichts kopieren: Alle Aufgaben stehen im Buch (Schnittpunkt 10, S. 16 und 17). Die Klasse schreibt alles selbst ins Übungsheft. "
                   "Die Lösung mit Schritten ist für Sie, Seite 1 ist das fertige Tafelbild zu Nr. 3 c."),
        ("0 bis 3 min", "Taschenrechner auf DEG prüfen lassen (Probe: sin 30° = 0,5). "
                        "Hinweis an die Klasse: So eine Aufgabe kommt im Kurztest am Mi 25.11."),
        ("3 bis 18 min", "<b>S. 16 Nr. 3 c rechts gemeinsam an der Tafel.</b> War Hausaufgabe, die meisten haben sie nicht geschafft. "
                         "Skizze groß anzeichnen, fragen, wo die Höhe von C aus liegt, c verlängern, h<sub>c</sub> einzeichnen. "
                         "Dann die Schritte ② bis ⑦ einzeln: kurz selbst rechnen lassen, vergleichen, an die Tafel. "
                         "Die Klasse schreibt Skizze und Rechnung vollständig ins Heft. "
                         "Wer nicht mitrechnen will, macht gleich mit den Übungsaufgaben weiter. "
                         "Die Lösungen der übrigen Hausaufgaben müssen nicht gezeigt werden, sie stehen in IServ."),
        ("18 bis 43 min", "<b>Einzelarbeit im Übungsheft</b>, der Reihe nach: ○ S. 16 Nr. 3 a links; ○ S. 16 Nr. 5 rechts; "
                          "◐ S. 16 Nr. 4 a und b links; ● S. 16 Nr. 7 links. Für Schnelle: S. 17 Nr. 8 und Nr. 10 links. "
                          "Ab etwa 35 min kann Seite 2 der Lösung vorne zur Selbstkontrolle ausliegen."),
        ("43 bis 45 min", "Kurz zusammenfassen: Erst die Höhe, dann die rechtwinkligen Dreiecke, dann sin, cos oder Pythagoras. "
                          "Was nicht fertig ist, bis zur nächsten Mathestunde fertig rechnen."),
    ]
    tab = "".join(f'<tr><td class="zeit">{z}</td><td>{t}</td></tr>' for z, t in zeilen)
    inhalt = (kopf("Ablauf, Mi 18.11.2026, 45 min") +
              '<div class="txt" style="margin:3mm 0 2mm">Thema: Berechnungen am allgemeinen Dreieck (Schnittpunkt 10, S. 16). '
              'Die Klasse kennt sin, cos und Pythagoras im rechtwinkligen Dreieck und hat schon Dreiecke über eine eingezeichnete Höhe berechnet. '
              'Neu ist der stumpfe Winkel, bei dem die Höhe außerhalb liegt (S. 16 Nr. 3 c war Hausaufgabe, viele werden daran gescheitert sein).</div>'
              f'<table class="abl">{tab}</table>'
              '<div class="txt" style="margin-top:3mm">Material: Buch, Übungsheft, Taschenrechner; Lösung mit Schritten für Sie (2 Seiten). '
              'Vielen Dank fürs Übernehmen!</div>')
    css_extra = ('<style>.abl {{ border-collapse: collapse; width: 100%; font-size: 10.5pt; line-height: 1.45; }}'
                 '.abl td {{ border-bottom: 0.3mm solid #ccc; padding: 2mm 2mm; vertical-align: top; }}'
                 '.abl .zeit {{ white-space: nowrap; font-weight: 700; width: 30mm; }}</style>').replace("{{", "{").replace("}}", "}")
    return html(N_ABL, [css_extra + seite(inhalt, "Mathe 10b; Vertretung 18.11.", 1)])


def drucke(name, inhalt, seiten_soll):
    h = HIER / f"{name}.html"
    p = HIER / f"{name}.pdf"
    h.write_text(inhalt, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={p}",
                    "--virtual-time-budget=3000", h.as_uri()], check=True, capture_output=True)
    from pypdf import PdfReader
    n = len(PdfReader(str(p)).pages)
    print(p.name, "| Seiten:", n)
    assert n == seiten_soll, f"{name}: {n} Seiten statt {seiten_soll}"


if __name__ == "__main__":
    drucke(N_LOE, loesung(), 2)
    drucke(N_ABL, ablauf(), 1)
