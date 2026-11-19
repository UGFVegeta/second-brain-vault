"""Rezept Trigonometrie als Flussdiagramm, Mathe 10b, Fr 20.11.2026 (Oskars erster Tag nach der Krankheit).
Seite 1: Flussdiagramm nach Oskars Diktat (⓪ Skizze, ① Winkel erkennen, ② rechtwinklig? Ja links / Nein rechts,
③ Gleichung mit einer Unbekannten, ④ auflösen, zwei Nachkommastellen, auch bei Winkeln; Schleife zurück zu ①).
Das Flussdiagramm kommt aus der Excalidraw-Datei daneben (gebaut von .scripts/mindmaps/rezept_trigo10b.py,
danach in Obsidian änderbar); dieses Skript liest sie bei jedem Bau neu ein.
Seite 2: zwei Beispiele komplett durchgerechnet, jeder Schritt mit der Nummer aus dem Rezept.
Beispiel (b) ist ein eigenes, einfaches Dreieck. Die Prüfungsaufgabe 2022 A2/1 (Hausaufgabe) ist zu verschachtelt
(gleichschenkliges Teildreieck, zweite Höhe).
Alle Werte mit Asserts geprüft (Sinussatz als Gegenprobe). Rechter Winkel = Viertelkreis mit Punkt.
Ausführen: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 baue_rezept_trigo.py
"""
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from baue_loesung_s15_s16 import CHROME, ROT, S, C, k, bruch, i, Skizze, dreieck, fuss

HIER = Path(__file__).parent
NAME = "Mathe 10b – Rezept Trigonometrie – Flussdiagramm mit zwei Beispielen"
BLAU = "#2563a8"
r2 = lambda x: round(x + 1e-9, 2)

# ---------------------------------------------------------------- Rechnung
# (a) rechtwinklig bei C: a = 5,0 cm; c = 9,0 cm; gesucht α, β, b
qa = round(5.0 / 9.0, 4); al_a = r2(math.degrees(math.asin(5.0 / 9.0))); be_a = r2(180 - 90 - al_a)
b_a = r2(9.0 * C(al_a))
assert (qa, al_a, be_a, b_a) == (0.5556, 33.75, 56.25, 7.48)
assert r2(math.sqrt(9.0**2 - 5.0**2)) == b_a                       # Gegenprobe Pythagoras
# (b) c = 9,0 cm; α = 50,0°; β = 70,0°; gesucht a, b (Höhe h_b von B auf b, Fußpunkt F)
ga_b = r2(180 - 50 - 70); hb = r2(9.0 * S(50)); a_b = r2(hb / S(ga_b))
b1 = r2(9.0 * C(50)); b2 = r2(a_b * C(ga_b)); b_b = r2(b1 + b2)
assert (ga_b, hb, a_b, b1, b2, b_b) == (60, 6.89, 7.96, 5.79, 3.98, 9.77)
assert r2(9.0 * S(50) / S(60)) == a_b and r2(9.0 * S(70) / S(60)) == b_b   # Gegenprobe Sinussatz


# ---------------------------------------------------------------- Flussdiagramm aus Excalidraw
EXCALIDRAW = HIER / "Mathe 10b – Rezept Trigonometrie – Flussdiagramm.excalidraw"   # gebaut von .scripts/mindmaps/rezept_trigo10b.py
EXCALIDRAW_KURZ = HIER / "Mathe 10b – Rezept Trigonometrie – Kurzfassung.excalidraw"  # gebaut von .scripts/mindmaps/rezept_trigo10b_kurz.py
NAME_KURZ = "Mathe 10b – Rezept Trigonometrie – Kurzfassung zum Mitschreiben"


def flussdiagramm(quelle=EXCALIDRAW):
    """Liest die Excalidraw-Datei (auch nach Änderungen in Obsidian) und gibt sie als SVG zurück."""
    sys.path.insert(0, str(HIER.parents[2] / ".scripts"))
    from mindmap_excalidraw import svg_schreiben
    E = [e for e in json.loads(quelle.read_text(encoding="utf-8"))["elements"] if not e.get("isDeleted")]
    with tempfile.TemporaryDirectory() as d:
        pfad = Path(d) / "fluss.svg"
        svg_schreiben(E, pfad)
        svg = pfad.read_text(encoding="utf-8")
    svg = re.sub(r'width="\d+" height="\d+"', 'style="width:100%;height:100%"', svg, count=1)
    return svg


# ---------------------------------------------------------------- Beispiele
SUB = lambda t: f"<tspan font-size='2.2' dy='0.8'>{t}</tspan>"


def sk_a():
    w = math.degrees(math.asin(5.0 / 9.0)); bx = math.sqrt(9.0**2 - 5.0**2)      # exakt, damit der rechte Winkel stimmt
    P = dreieck((0, 0), (9.0, 0), (bx * C(w), bx * S(w)))
    A, B, Cc = P["A"], P["B"], P["C"]
    s = Skizze(P, breite=66, hoehe=44)
    s.rechter(Cc, A, B, r=3.4)
    s.seite(A, B, "9,0 cm"); s.seite(B, Cc, "5,0 cm"); s.seite(A, Cc, "b", ROT, fett=True)
    s.winkel(A, B, Cc, "α", ROT, r=5, rt=9, fett=True); s.winkel(B, A, Cc, "β", ROT, r=5, rt=8.5, fett=True)
    for n in "ABC": s.ecke(n)
    return s.svg()


def sk_b():
    P = dreieck((0, 0), (9.0, 0), (b_b * C(50), b_b * S(50)))
    A, B, Cc = P["A"], P["B"], P["C"]
    F = fuss(B, A, Cc)
    s = Skizze(P, breite=66, hoehe=64)
    s.linie(B, F, BLAU, 0.6, "1.4,0.9"); s.rechter(F, A, B, r=3.4)
    s.seite(A, B, "9,0 cm"); s.seite(B, Cc, "a", ROT, fett=True)
    s.seite(A, F, "b" + SUB("1"), ROT, fett=True); s.seite(F, Cc, "b" + SUB("2"), ROT, fett=True)
    s.seite(B, F, "h" + SUB("b"), BLAU, aussen=False, ab=2.6, pos=0.5)
    s.winkel(A, B, Cc, "50,0°", r=5, rt=10.5); s.winkel(B, A, Cc, "", r=5); bx, by = s.m(*B); s.text(bx + 1, by - 9, "70,0°", gr=2.8)
    s.winkel(Cc, A, B, "γ", ROT, r=4.5, rt=8, fett=True)
    x, y = s.m(*F); s.text(x - 3.2, y - 1.5, "F", gr=3.0)
    for n in "ABC": s.ecke(n)
    return s.svg()


def nr(n):
    return f'<span class="nr">{n}</span>'


def zeile(n, *teile):
    return f'<div class="zl">{nr(n) if n != "" else "<span></span>"}<div>{"".join(f"<div>{t}</div>" for t in teile)}</div></div>'


def erg(t):
    return f'<b class="erg">{t}</b>'


def um(t):
    return f'<span class="um">| {t}</span>'


def weiter(t="Fertig? Nein: weiter bei ①"):
    return f'<div class="weiter">{t}</div>'


hb_ = i("h", "b"); b1_ = i("b", "1"); b2_ = i("b", "2")


def beispiel_a():
    links = [
        zeile(0, "a = 5,0 cm; c = 9,0 cm; γ = 90°", "eintragen; gesucht α, β, b rot"),
        zeile(1, "nur γ = 90° bekannt"),
        zeile(2, "rechtwinklig bei C: <b>Ja</b>", "also sin, cos oder tan"),
        zeile(3, "α: 5,0 cm liegt α gegenüber,", "9,0 cm ist die Hypotenuse",
              f"sin α = {bruch('5,0', '9,0')}"),
        zeile(4, f"sin α = {k(qa, 4)} {um('sin⁻¹')}", erg(f"α = {k(al_a)}°")),
    ]
    rechts = [
        weiter(),
        zeile(1, f"β = 180° − 90° − {k(al_a)}°", erg(f"β = {k(be_a)}°")),
        zeile(3, "b: b liegt an α (Ankathete)", f"cos {k(al_a)}° = {bruch('b', '9,0')} {um('⋅ 9,0')}"),
        zeile(4, f"b = 9,0 ⋅ cos {k(al_a)}°", erg(f"b = {k(b_a)} cm")),
        weiter("Fertig? <b>Ja</b>"),
    ]
    return ('<section><h2><span class="bsp">Beispiel (a)</span> rechtwinkliges Dreieck: direkt mit sin, cos oder tan</h2>'
            f'<div class="reihe"><div class="sk">{sk_a()}</div><div class="spalte">{"".join(links)}</div>'
            f'<div class="spalte">{"".join(rechts)}</div></div>'
            f'<div class="ergebnis">Ergebnis: α = {k(al_a)}°; β = {k(be_a)}°; b = {k(b_a)} cm</div></section>')


def beispiel_b():
    links = [
        zeile(0, "c = 9,0 cm; α = 50,0°; β = 70,0°", "eintragen; gesucht a und b rot"),
        zeile(1, "Winkelsumme:", f"γ = 180° − 50,0° − 70,0°", erg(f"γ = {k(ga_b)}°")),
        zeile(2, "rechtwinklig? <b>Nein</b>", f"Höhe {hb_} von B auf b einzeichnen,", "Fußpunkt F. Jetzt gibt es",
              "zwei rechtwinklige Dreiecke:", "ABF und FBC", f"<span class='achtung'>nicht {i('h', 'c')}: c ist die einzige</span>",
              "<span class='achtung'>bekannte Seite</span>"),
        zeile(3, f"{hb_} im Dreieck ABF:", f"sin 50,0° = {bruch(hb_, '9,0')} {um('⋅ 9,0')}"),
        zeile(4, f"{hb_} = 9,0 ⋅ sin 50,0°", erg(f"{hb_} = {k(hb)} cm")),
    ]
    rechts = [
        weiter(),
        zeile(3, "a im Dreieck FBC:", f"sin {k(ga_b)}° = {bruch(k(hb), 'a')} {um(f'a ↔ sin {k(ga_b)}°')}"),
        zeile(4, f"a = {bruch(k(hb), f'sin {k(ga_b)}°')}", erg(f"a = {k(a_b)} cm")),
        weiter(),
        zeile(3, f"{b1_} im Dreieck ABF:", f"cos 50,0° = {bruch(b1_, '9,0')} {um('⋅ 9,0')}"),
        zeile(4, f"{b1_} = 9,0 ⋅ cos 50,0°", erg(f"{b1_} = {k(b1)} cm")),
        zeile(3, f"{b2_} im Dreieck FBC:", f"cos {k(ga_b)}° = {bruch(b2_, k(a_b))} {um('⋅ ' + k(a_b))}"),
        zeile(4, f"{b2_} = {k(a_b)} ⋅ cos {k(ga_b)}°", erg(f"{b2_} = {k(b2)} cm")),
        zeile("", f"b = {b1_} + {b2_} = {k(b1)} + {k(b2)}", erg(f"b = {k(b_b)} cm")),
        weiter("Fertig? <b>Ja</b>"),
    ]
    return ('<section><h2><span class="bsp">Beispiel (b)</span> nicht rechtwinklig: Höhe einzeichnen, dann die Teildreiecke</h2>'
            f'<div class="reihe"><div class="sk">{sk_b()}</div><div class="spalte">{"".join(links)}</div>'
            f'<div class="spalte">{"".join(rechts)}</div></div>'
            f'<div class="ergebnis">Ergebnis: a = {k(a_b)} cm; b = {k(b_b)} cm</div></section>')


CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #fff; font-family: Helvetica, Arial, sans-serif; color: #222; }}
.seite {{ width: 210mm; height: 297mm; padding: 8mm 10mm 6mm; overflow: hidden; break-after: page; position: relative; }}
.seite:last-child {{ break-after: auto; }}
.balken {{ background: #d9d9d9; font-weight: 700; font-size: 12pt; padding: 2mm 3mm; display: flex; justify-content: space-between; align-items: baseline; }}
.balken span {{ font-weight: 400; font-size: 9.5pt; }}
.fluss {{ margin: 4mm auto 0; width: 182mm; height: 255mm; }}
.fluss.kurz {{ margin-top: 10mm; width: 178mm; height: 235mm; }}
section {{ border-bottom: 0.3mm solid #ccc; padding: 3mm 0 3mm; }}
h2 {{ font-size: 12pt; margin: 0 0 2mm; }}
.bsp {{ color: {BLAU}; margin-right: 1.5mm; }}
.reihe {{ display: flex; gap: 4mm; align-items: flex-start; }}
.sk {{ flex: 0 0 auto; }}
.spalte {{ flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 1.6mm; }}
.zl {{ display: grid; grid-template-columns: 6mm 1fr; align-items: start; font-size: 10pt; line-height: 1.45; white-space: nowrap; }}
.nr {{ display: inline-flex; width: 4.6mm; height: 4.6mm; border-radius: 50%; background: {BLAU}; color: #fff; font-weight: 700;
       font-size: 8.5pt; align-items: center; justify-content: center; margin-top: 0.4mm; }}
.weiter {{ font-size: 9pt; color: #555; border-top: 0.25mm dashed #aaa; padding-top: 0.8mm; }}
.weiter:first-child {{ border-top: none; padding-top: 0; }}
.erg {{ color: {ROT}; }}
.achtung {{ color: {ROT}; }}
.um {{ color: #777; font-size: 9pt; margin-left: 1.5mm; }}
.br {{ display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 9.5pt; line-height: 1.15; margin: 0 0.6mm; }}
.br span:first-child {{ border-bottom: 0.25mm solid #222; padding: 0 0.8mm; }}
.ergebnis {{ font-size: 11pt; color: {ROT}; font-weight: 700; margin-top: 2mm; }}
.fuss {{ position: absolute; bottom: 5mm; left: 10mm; right: 10mm; font-size: 7.5pt; color: #888; display: flex; justify-content: space-between; }}
@media screen {{ body {{ background: #888; }} .seite {{ background: #fff; margin: 6mm auto; box-shadow: 0 1mm 4mm #0005; }} }}
"""


def seite(titel, rechts, inhalt, n):
    return (f'<div class="seite"><div class="balken">Mathe 10b   {titel} <span>{rechts}</span></div>{inhalt}'
            f'<div class="fuss"><span>Mathe 10b; Trigonometrie; Rezept</span><span>Seite {n}</span></div></div>')


def baue():
    s1 = seite("Trigonometrie: So gehst du bei jeder Aufgabe vor", "Rezept als Flussdiagramm",
               f'<div class="fluss">{flussdiagramm()}</div>', 1)
    s2 = seite("Trigonometrie: Das Rezept an zwei Beispielen", "Nummern = Schritte aus dem Rezept",
               beispiel_a() + beispiel_b(), 2)
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{NAME}</title><style>{CSS}</style></head>'
            f'<body>{s1}{s2}</body></html>')


def baue_kurz():
    """Kurzfassung (Oskar 19.11.): eine Seite, die Klasse schreibt sie gemeinsam mit ihm ins Merkheft."""
    s = seite("Trigonometrie: So gehst du bei jeder Aufgabe vor", "Merkheft",
              f'<div class="fluss kurz">{flussdiagramm(EXCALIDRAW_KURZ)}</div>', 1)
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{NAME_KURZ}</title><style>{CSS}</style></head>'
            f'<body>{s}</body></html>').replace("Mathe 10b; Trigonometrie; Rezept</span><span>Seite 1", "Mathe 10b; Trigonometrie; Rezept</span><span>")


def drucke(name, inhalt, seiten_soll):
    html = HIER / f"{name}.html"
    pdf = HIER / f"{name}.pdf"
    html.write_text(inhalt, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=3000", html.as_uri()], check=True, capture_output=True)
    from pypdf import PdfReader
    n = len(PdfReader(str(pdf)).pages)
    print(html.name, "|", pdf.name, "| Seiten:", n)
    assert n == seiten_soll, f"{n} Seiten statt {seiten_soll}"


def main():
    drucke(NAME, baue(), 2)
    drucke(NAME_KURZ, baue_kurz(), 1)


if __name__ == "__main__":
    main()
