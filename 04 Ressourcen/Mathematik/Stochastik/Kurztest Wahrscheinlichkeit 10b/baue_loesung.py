#!/usr/bin/env python3
"""Lösungsblatt zum Kurztest Wahrscheinlichkeit 10b, rechnet alle Werte aus den Parametern selbst nach.
Aufruf: python3 baue_loesung.py B   -> 'Kurztest Wahrscheinlichkeit 10b B – Lösung.html/.pdf' (A liefert zur Kontrolle die Werte der A-Fassung)."""
import subprocess, sys
from fractions import Fraction
from pathlib import Path

HIER = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Parameter je Version: Kugeln mit 1/2/3; Karten (Kreuz, Pik, Herz, Karo); Gewinn Karo, Gewinn Herz, Sophie (Karo), Einsatz
V = {
    "A": dict(k=(11, 17, 22), karten=(6, 1, 3, 2), g_karo=10, g_herz=5, g_sophie=20),
    "B": dict(k=(13, 19, 18), karten=(4, 2, 4, 2), g_karo=12, g_herz=4, g_sophie=24),
    "C": dict(k=(15, 12, 23), karten=(5, 3, 2, 2), g_karo=15, g_herz=8, g_sophie=30),
}


def de(x, n=3):
    return f"{float(x):.{n}f}".replace(".", ",")


def F(n, d):
    return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'


def Fr(x):
    x = Fraction(x)
    return F(x.numerator, x.denominator)


def rechne(p):
    k1, k2, k3 = p["k"]
    assert k1 + k2 + k3 == 50
    k = [k1, k2, k3]
    zweite = [[k[j] - (1 if i == j else 0) for j in range(3)] for i in range(3)]  # Zähler im 2. Zug
    gleich = sum(k[i] * (k[i] - 1) for i in range(3))
    groesser = sum(k[i] * k[j] for i in range(3) for j in range(3) if i > j)  # erste Zahl (i) größer als zweite (j)
    zweimal3 = k3 * (k3 - 1)
    kr, pk, he, ka = p["karten"]
    assert kr + pk + he + ka == 12
    s, r = kr + pk, he + ka
    return dict(k=k, zweite=zweite, gleich=gleich, groesser=groesser, zweimal3=zweimal3,
                s=s, r=r, rs=2 * s * r, ka=ka, he=he,
                nK=ka * (ka - 1), nH=he * (he - 1))


def tree(R):
    cent = [130, 380, 630]
    t = '<svg viewBox="0 0 760 345" style="width:76%;display:block;margin:0 auto" fill="none" stroke="#222" stroke-width="1.3">'
    for c in cent:
        t += f'<line x1="380" y1="12" x2="{c}" y2="127"/>'
    t += '<g fill="#111" stroke="none" font-size="17" text-anchor="middle">'
    for x, y, n in [(248, 52, R["k"][0]), (380, 52, R["k"][1])]:
        t += (f'<rect x="{x-22}" y="{y}" width="44" height="46" fill="#fff"/><text x="{x}" y="{y+18}">{n}</text>'
              f'<line x1="{x-14}" y1="{y+23}" x2="{x+14}" y2="{y+23}" stroke="#111" stroke-width="1"/><text x="{x}" y="{y+41}">50</text>')
    t += '</g><rect x="482" y="50" width="52" height="42" fill="#fff"/>'
    t += (f'<g stroke="none" font-size="17" text-anchor="middle"><text x="508" y="66" fill="#c00">{R["k"][2]}</text>'
          '<line x1="494" y1="71" x2="522" y2="71" stroke="#c00" stroke-width="1"/><text x="508" y="89" fill="#c00">50</text></g>')
    for i, c in enumerate(cent):
        t += f'<circle cx="{c}" cy="140" r="13" fill="#fff"/><text x="{c}" y="145.5" font-size="15" text-anchor="middle" fill="#111" stroke="none">{i+1}</text>'
        for j, dx in enumerate((-80, 0, 80)):
            x = c + dx
            t += f'<line x1="{c}" y1="153" x2="{x}" y2="212"/><rect x="{x-30}" y="212" width="60" height="42" fill="#fff"/>'
            t += (f'<g fill="#c00" stroke="none" font-size="14" text-anchor="middle"><text x="{x}" y="229">{R["zweite"][i][j]}</text>'
                  f'<line x1="{x-13}" y1="234" x2="{x+13}" y2="234" stroke="#c00" stroke-width="1"/><text x="{x}" y="248">49</text></g>')
            t += f'<line x1="{x}" y1="254" x2="{x}" y2="305"/><circle cx="{x}" cy="318" r="13" fill="#fff"/><text x="{x}" y="323.5" font-size="15" text-anchor="middle" fill="#111" stroke="none">{j+1}</text>'
    return t + "</svg>"


CSS = """<style>
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; }
  html { background: #d8d8d8; }
  body { margin: 0; font-family: "Open Sans","Helvetica Neue",Arial,sans-serif; font-size: 10.5pt; color: #111; line-height: 1.5; }
  .page { width: 210mm; min-height: 297mm; margin: 8mm auto; background: #fff; padding: 13mm 15mm; page-break-after: always; }
  @media print { html { background: none; } .page { margin: 0; } }
  h1 { font-size: 15pt; margin: 0 0 1mm; } h2 { font-size: 12pt; margin: 5mm 0 1.5mm; border-bottom: .3mm solid #222; padding-bottom: .5mm; }
  .sub { color:#666; font-size: 9.5pt; margin-bottom: 2mm; }
  p { margin: 0 0 1.4mm; } .p { float: right; color:#555; font-size: 9.5pt; }
  .fr { display:inline-flex; flex-direction:column; align-items:center; vertical-align:middle; font-size: 9.5pt; line-height: 1.15; margin: 0 .6mm; }
  .fr span:first-child { border-bottom: .25mm solid #111; padding: 0 .8mm; }
  .erg { background:#e9f4e9; padding: 0 1.5mm; font-weight:600; }
</style>"""


def blatt(ver):
    p = V[ver]
    R = rechne(p)
    k = R["k"]
    P = lambda n, d=2450: F(n, d)
    gl = " + ".join(f"{F(k[i], 50)}·{F(k[i]-1, 49)}" for i in range(3))
    pf = [(1, 0), (2, 0), (2, 1)]  # (erste, zweite) Index: 2|1, 3|1, 3|2
    gr = " + ".join(f"{F(k[i], 50)}·{F(k[j], 49)}" for i, j in pf)
    e_plan = Fraction(p["g_karo"] * R["nK"] + p["g_herz"] * R["nH"], 132)
    e_soph = Fraction(p["g_sophie"] * R["nK"] + p["g_herz"] * R["nH"], 132)
    kr, pk, he, ka = p["karten"]
    schluss = ("<b>Er hat also nicht Recht</b>, er macht keinen Verlust." if e_soph < 1
               else "<b>Er hat also Recht</b>, er macht dann Verlust.")
    titel = f"Kurztest Nr. 1 Wahrscheinlichkeit 10b, Version {ver} – Lösung"
    datum = "Nachschreiber" if ver == "C" else "30.09.2026"
    return f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title>{CSS}</head><body>
<div class="page">
<h1>{titel}</h1>
<div class="sub">{datum} · 10 Punkte · Punkteverteilung ist ein Vorschlag, Werte gerundet auf drei Stellen.</div>

<h2>Aufgabe 1 <span class="p">5 P</span></h2>
<p><b>a) Baumdiagramm</b> (2 P): Von 50 Kugeln tragen {k[0]} die Zahl 1, {k[1]} die Zahl 2, also 50 − {k[0]} − {k[1]} = {k[2]} die Zahl 3. Im zweiten Zug fehlt eine Kugel (Nenner 49), und die gezogene Zahl ist einmal weniger da. Die roten Werte sind einzutragen.</p>
{tree(R)}
<p><b>b) Gleiche Zahl</b> (1 P): P = {gl} = {P(R["gleich"])} = <span class="erg">{Fr(Fraction(R["gleich"], 2450))} ≈ {de(Fraction(R["gleich"], 2450))}</span> ({de(Fraction(R["gleich"], 2450) * 100, 1)} %)</p>
<p><b>c) Erste Zahl größer als die zweite</b> (1 P): Pfade (2|1), (3|1), (3|2): P = {gr} = {P(R["groesser"])} = <span class="erg">{Fr(Fraction(R["groesser"], 2450))} ≈ {de(Fraction(R["groesser"], 2450))}</span> ({de(Fraction(R["groesser"], 2450) * 100, 1)} %)</p>
<p><b>d) Höchstens eine 3</b> (1 P): Gegenereignis „zweimal die 3“: P(3|3) = {F(k[2], 50)}·{F(k[2]-1, 49)} = {P(R["zweimal3"])}. Also P(höchstens eine 3) = 1 − {P(R["zweimal3"])} = <span class="erg">{Fr(1 - Fraction(R["zweimal3"], 2450))} ≈ {de(1 - Fraction(R["zweimal3"], 2450))}</span> ({de((1 - Fraction(R["zweimal3"], 2450)) * 100, 1)} %)</p>
</div>

<div class="page">
<h2 style="margin-top:0">Aufgabe 2 <span class="p">5 P</span></h2>
<p><b>a) Rot und schwarz</b> (1 P): Es gibt {R["s"]} schwarze ({kr} + {pk}) und {R["r"]} rote ({he} + {ka}) Karten. Beide Reihenfolgen zählen:<br>
P = 2 · {F(R["s"], 12)}·{F(R["r"], 11)} = {F(R["rs"], 132)} = <span class="erg">{Fr(Fraction(R["rs"], 132))} ≈ {de(Fraction(R["rs"], 132))}</span> ({de(Fraction(R["rs"], 132) * 100, 1)} %)</p>
<p><b>b) Erwartungswert</b> (2 P): Zunächst die Wahrscheinlichkeiten der Gewinnfälle:<br>
P(zweimal Karo) = {F(ka, 12)}·{F(ka-1, 11)} = {F(R["nK"], 132)} = {Fr(Fraction(R["nK"], 132))}<br>
P(zweimal Herz) = {F(he, 12)}·{F(he-1, 11)} = {F(R["nH"], 132)} = {Fr(Fraction(R["nH"], 132))}<br>
Mittlere Auszahlung: E = {p["g_karo"]} € · {Fr(Fraction(R["nK"], 132))} + {p["g_herz"]} € · {Fr(Fraction(R["nH"], 132))} + 0 € · (Rest) = {Fr(e_plan)} € <span class="erg">≈ {de(e_plan, 2)} €</span><br>
Die Spieler bekommen im Mittel {de(e_plan, 2)} € pro Spiel zurück, zahlen aber 1,00 € Einsatz. Der Betreiber gewinnt im Schnitt etwa {de(1 - e_plan, 2)} € pro Spiel (Erwartungswert für die Spieler: −{de(1 - e_plan, 2)} €).</p>
<p><b>c) Sophies Vorschlag</b> (2 P): Neuer Erwartungswert der Auszahlung:<br>
E = {p["g_sophie"]} € · {Fr(Fraction(R["nK"], 132))} + {p["g_herz"]} € · {Fr(Fraction(R["nH"], 132))} = {Fr(e_soph)} € <span class="erg">≈ {de(e_soph, 2)} €</span><br>
Das liegt {"immer noch unter" if e_soph < 1 else "über"} dem Einsatz von 1,00 €. Der Betreiber {"gewinnt im Schnitt weiterhin" if e_soph < 1 else "verliert im Schnitt"} etwa {de(abs(1 - e_soph), 2)} € pro Spiel. {schluss}</p>

<h2>Hinweise</h2>
<p>Die Aufgaben stammen aus der Abschlussprüfung 2014 (P8) und 2015 (W4a). Teil d) bei Aufgabe 1 ist ergänzt, damit die Pflichtteil-Aufgabe 5 statt 4 Punkte wert ist.</p>
<p>Bei b) gelten auch Bruch- und Dezimalwerte. Wer den Erwartungswert als Reingewinn des Spielers angibt (−{de(1 - e_plan, 2)} €), soll die volle Punktzahl bekommen, wenn er den Einsatz mit einrechnet und richtig schließt.</p>
</div>
</body></html>"""


def kontrolle():
    a = rechne(V["A"])
    assert (a["gleich"], a["groesser"], a["zweimal3"], a["rs"]) == (844, 803, 462, 70)
    assert Fraction(V["A"]["g_karo"] * a["nK"] + V["A"]["g_herz"] * a["nH"], 132) == Fraction(25, 66)
    print("Kontrolle A ok (844, 803, 462, 35/66, 25/66)")


def main():
    kontrolle()
    ver = sys.argv[1] if len(sys.argv) > 1 else "B"
    name = f"Kurztest Wahrscheinlichkeit 10b {ver} – Lösung"
    h = HIER / f"{name}.html"
    h.write_text(blatt(ver), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={HIER / (name + '.pdf')}", h.as_uri()], check=True, capture_output=True)
    print("geschrieben:", name + ".pdf")


if __name__ == "__main__":
    main()
