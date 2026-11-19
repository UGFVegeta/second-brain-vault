"""Aufgabe im Prüfungsstil zum Rezept Trigonometrie, Mathe 10b, Fr 20.11.2026.
Oskar 19.11.: nach dem gemeinsamen Aufschreiben des Rezepts (Kurzfassung) eine Aufgabe in diesem Stil lösen.
Eigene Aufgabe, die jeden Schritt braucht: ⓪ Werte stehen links neben der Figur, ① β als Nebenwinkel von ε,
② nicht rechtwinklig: Höhe h_c, ③④ zweimal durch die Schleife, einmal mal Nenner, einmal tauschen.
Seite 1: Aufgabe + Karofläche zum Mitschreiben (Notability). Seite 2: dasselbe Blatt ausgefüllt.
Werte mit Asserts geprüft (Sinussatz als Gegenprobe). Rechter Winkel = Viertelkreis mit Punkt.
Ausführen: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 baue_aufgabe_rezept.py
"""
import math

from baue_loesung_s15_s16 import ROT, S, C, k, bruch, i, Skizze, dreieck, fuss
from baue_rezept_trigo import BLAU, CSS, zeile, erg, um, weiter, drucke

NAME = "Mathe 10b – Rezept Trigonometrie – Aufgabe im Prüfungsstil"
r2 = lambda x: round(x + 1e-9, 2)

# ---------------------------------------------------------------- Rechnung
# AC = 8,0 cm; α = 35,0°; Außenwinkel ε = 130,0° bei B; gesucht Umfang u (und für Schnelle A)
be = r2(180 - 130); ga = r2(180 - 35 - be)
hc = r2(8.0 * S(35)); AF = r2(8.0 * C(35))
BC = r2(hc / S(be)); FB = r2(BC * C(be)); AB = r2(AF + FB)
u = r2(AB + BC + 8.0); A = r2(0.5 * AB * hc)
assert (be, ga, hc, AF, BC, FB, AB, u, A) == (50, 95, 4.59, 6.55, 5.99, 3.85, 10.40, 24.39, 23.87)
assert r2(8.0 * S(35) / S(50)) == BC and r2(8.0 * S(95) / S(50)) == AB       # Gegenprobe Sinussatz
SUB = lambda t: f"<tspan font-size='2.2' dy='0.8'>{t}</tspan>"


def skizze(loes):
    ab = 8.0 * S(95) / S(50)                                    # exakt, damit die Höhe senkrecht steht
    P = dreieck((0, 0), (ab, 0), (8.0 * C(35), 8.0 * S(35)))
    A_, B, Cc = P["A"], P["B"], P["C"]
    E = (ab + 2.6, 0)
    s = Skizze(P, extra=[E], breite=92, hoehe=46)
    s.linie(B, E)
    if loes:
        F = fuss(Cc, A_, B)
        s.linie(Cc, F, BLAU, 0.6, "1.4,0.9"); s.rechter(F, B, Cc, r=3.4)
        s.seite(Cc, F, "h" + SUB("c"), BLAU, aussen=False, ab=3, pos=0.45)
        x, y = s.m(*F); s.text(x, y + 3.8, "F", gr=3.0)
        s.seite(A_, Cc, "8,0 cm"); s.seite(B, Cc, "BC", ROT, fett=True)
        s.seite(A_, F, "AF", ROT, fett=True, ab=3.2); s.seite(F, B, "FB", ROT, fett=True, ab=3.2)
        s.winkel(A_, B, Cc, "35,0°", r=6, rt=12); s.winkel(B, E, Cc, "130,0°", r=4.5, rt=10)
        s.winkel(B, A_, Cc, "β", ROT, r=4.5, rt=8, fett=True)
    else:
        s.winkel(A_, B, Cc, "α", r=6, rt=10); s.winkel(B, E, Cc, "ε", r=4.5, rt=8.5)
    s.ecke("A"); s.ecke("C"); s.ecke("B", dx=-2.2, dy=1.2)
    return s.svg()


def aufgabe(loes):
    werte = "AC = 8,0 cm<br>α = 35,0°<br>ε = 130,0°"
    return ('<div class="pa"><div class="pa-kopf"><span class="kr">◐</span> Aufgabe <span class="q">im Prüfungsstil</span></div>'
            '<div class="pa-txt" style="margin-top:2mm">Im Dreieck ABC gilt:</div>'
            f'<div class="pa-reihe"><div class="werte">{werte}</div><div class="pa-sk">{skizze(loes)}</div></div>'
            '<div class="pa-txt"><b>Berechnen Sie den Umfang des Dreiecks ABC.</b> '
            '<span class="leg">(Skizze nicht maßstabsgetreu)</span></div>'
            '<div class="pa-txt schnell"><span class="kr">○</span> Für Schnelle: Berechnen Sie auch den Flächeninhalt.</div>'
            '<div class="leg">○ leicht; ◐ mittel; ● schwer</div></div>')


hc_ = i("h", "c")
ZURUECK = "Fertig? Nein: zurück zu 1"


def loesung():
    links = [
        zeile(0, "AC = 8,0 cm; α = 35,0°; ε = 130,0°", "in die Skizze; gesucht: u (rot),", "dafür fehlen AB und BC"),
        zeile(1, "β ist Nebenwinkel von ε:", "β = 180° − 130,0°", erg(f"β = {k(be)}°"),
              "Winkelsumme:", f"γ = 180° − 35,0° − {k(be)}°", erg(f"γ = {k(ga)}°")),
        zeile(2, "rechtwinklig? <b>Nein</b>", f"Höhe {hc_} von C auf AB,", "Fußpunkt F: Dreiecke AFC und FBC"),
        zeile(3, f"{hc_} im Dreieck AFC:", f"sin 35,0° = {bruch(hc_, '8,0')} {um('⋅ 8,0')}"),
        zeile(4, f"{hc_} = 8,0 ⋅ sin 35,0°", erg(f"{hc_} = {k(hc)} cm")),
    ]
    rechts = [
        weiter(ZURUECK),
        zeile(3, "AF im Dreieck AFC:", f"cos 35,0° = {bruch('AF', '8,0')} {um('⋅ 8,0')}"),
        zeile(4, "AF = 8,0 ⋅ cos 35,0°", erg(f"AF = {k(AF)} cm")),
        zeile(3, "BC im Dreieck FBC:", f"sin {k(be)}° = {bruch(k(hc), 'BC')} {um(f'BC ↔ sin {k(be)}°')}"),
        zeile(4, f"BC = {bruch(k(hc), f'sin {k(be)}°')}", erg(f"BC = {k(BC)} cm")),
        zeile(3, "FB im Dreieck FBC:", f"cos {k(be)}° = {bruch('FB', k(BC))} {um('⋅ ' + k(BC))}"),
        zeile(4, f"FB = {k(BC)} ⋅ cos {k(be)}°", erg(f"FB = {k(FB)} cm")),
        zeile("", f"AB = AF + FB = {k(AF)} + {k(FB)}", erg(f"AB = {k(AB)} cm")),
        zeile("", f"u = AB + BC + AC = {k(AB)} + {k(BC)} + 8,0", erg(f"u = {k(u)} cm")),
        weiter("Fertig? <b>Ja</b>"),
    ]
    return (f'<div class="reihe loes"><div class="spalte">{"".join(links)}</div><div class="spalte">{"".join(rechts)}</div></div>'
            f'<div class="ergebnis">Ergebnis: u = {k(u)} cm</div>'
            f'<div class="schnell-l"><span class="kr">○</span> Für Schnelle: A = {bruch(1, 2)} ⋅ AB ⋅ {hc_} = '
            f'{bruch(1, 2)} ⋅ {k(AB)} ⋅ {k(hc)} &nbsp;{erg(f"A = {k(A)} cm²")}</div>')


EXTRA = f"""
.pa {{ border: 0.4mm solid #333; padding: 3mm 4mm; margin-top: 4mm; background: #fff; }}
.pa-kopf {{ font-weight: 700; font-size: 12pt; }}
.pa-kopf .q {{ font-weight: 400; font-size: 9.5pt; color: #666; }}
.kr {{ margin-right: 1.5mm; }}
.leg {{ font-size: 8.5pt; color: #666; font-weight: 400; }}
.pa-reihe {{ display: flex; align-items: center; gap: 8mm; margin: 2mm 0; }}
.werte {{ font-size: 13pt; line-height: 1.7; flex: 0 0 34mm; }}
.pa-sk {{ flex: 1; display: flex; justify-content: center; }}
.pa-txt {{ font-size: 12pt; line-height: 1.5; }}
.schnell {{ font-size: 10.5pt; margin-top: 1.5mm; color: #444; }}
.karo {{ position: absolute; left: 10mm; right: 10mm; bottom: 12mm; top: 104mm;
         background-color: #fff;
         background-image: linear-gradient(#c9d3df 0.2mm, transparent 0.2mm), linear-gradient(90deg, #c9d3df 0.2mm, transparent 0.2mm);
         background-size: 5mm 5mm; border: 0.3mm solid #c9d3df; }}
.loes {{ margin-top: 4mm; }}
.loes .zl {{ font-size: 11pt; }}
.schnell-l {{ font-size: 10.5pt; margin-top: 2.5mm; }}
"""


def seite(titel, inhalt, n):
    return (f'<div class="seite"><div class="balken">Mathe 10b   Trigonometrie: {titel} <span>Fr 20.11.2026</span></div>{inhalt}'
            f'<div class="fuss"><span>Mathe 10b; Trigonometrie; Aufgabe zum Rezept</span><span>Seite {n}</span></div></div>')


def baue():
    s1 = seite("Aufgabe zum Rezept", aufgabe(False) + '<div class="karo"></div>', 1)
    s2 = seite("Aufgabe zum Rezept, Lösung", aufgabe(True) + loesung(), 2)
    return kreise_einheitlich(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{NAME}</title><style>{CSS}{EXTRA}</style></head>'
                              f'<body>{s1}{s2}</body></html>')


def kreise_einheitlich(html):
    """○ ◐ ● als gleich große SVG-Kreise (wie Dreiecke/06 Zirkel üben …/baue_zirkel.py; Schriftzeichen sind verschieden groß)."""
    def kr(art):
        f = {"○": "", "◐": '<path d="M5,1 A4,4 0 0 0 5,9 Z" fill="#222"/>', "●": '<circle cx="5" cy="5" r="4" fill="#222"/>'}[art]
        return (f'<svg width="3.6mm" height="3.6mm" viewBox="0 0 10 10" style="vertical-align:-0.5mm"><title>{art}</title>'
                f'<circle cx="5" cy="5" r="4" fill="none" stroke="#222" stroke-width="1.1"/>{f}</svg>')
    kopf, rumpf = html.split("<body>", 1)
    for z in "○◐●":
        rumpf = rumpf.replace(z, kr(z))
    return kopf + "<body>" + rumpf


if __name__ == "__main__":
    drucke(NAME, baue(), 2)
