#!/usr/bin/env python3
"""Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen (eigene Fassung der Parallelarbeit, ca. 85 % übernommen).
Layout wie Oskars Kurztest Kl. 10: Aufgabenbalken oben, darunter Karofläche für die Rechnung.
4 A4-Seiten = ein gefaltetes A3-Blatt. Danach dieselben 4 Seiten als Lösung.
Nur HTML (Entwurf zum Besprechen), PDF erst nach Freigabe."""
from fractions import Fraction as F
from pathlib import Path

HIER = Path(__file__).parent
ZIEL = HIER / "Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Entwurf.html"
MAG = "#E6007E"
GESAMT = 37

# ---------------------------------------------------------------- Prüfung aller Lösungen
assert -55 + 95 == 40 and -57 - 75 == -132 and 26 - 44 == -18 and F("-1.5") + F("2.5") == 1
assert F(-103) - 3 == -106 and 48 - 147 == -99 and F(-3, 4) + F(1, 2) == F(-1, 4) and F(-2, 5) - F(1, 5) == F(-3, 5)
assert F(-35) / -7 == 5 and F(-28) / -7 == 4 and F(-5) * 6 == -30 and F(-2) * 5 * -4 == 40 and F("-0.5") * 12 == -6 and F(-48) / -6 == 8 and F(105) / -5 == -21
assert -23 + -17 - 59 + 22 - 7 == -84 and F("41.7") - F("2.7") + F("-0.9") + F("2.2") == F("40.3") and -18 - (7 - 15) == -10
assert -520 + 2770 - 780 - 35 - 210 + 20 == 1245 and 8848 - (-11022) == 19870 and -6857 - (-11022) == 4165
assert F(-1, 4) == F(-2, 8) and F(-3, 7) < F(4, 7) and -2 < F("-1.9") and F("-2.1") > F("-4.3")


def br(z, n):
    return f'<span class="br"><span>{z}</span><span>{n}</span></span>'


def k(x):
    """Zahl in Klammern."""
    return f"({x})"


def balken(nr, punkte, text=""):
    return (f'<div class="balken"><b>Nr. {nr}</b><span class="pk">____ / {punkte}</span></div>'
            + (f'<p class="anw">{text}</p>' if text else ""))


def karo(hoehe, loes, l):
    inhalt = f'<div class="loes">{loes}</div>' if l else ""
    stil = "flex:1" if hoehe is None else f"height:{hoehe}mm;flex:none"
    return f'<div class="karo" style="{stil}">{inhalt}</div>'


def box(w, l, breit=False):
    return f'<span class="kast{" breit" if breit else ""}">{w if l else ""}</span>'


def namenszeile():
    return '<div class="namen"><span>Name:</span><span>Klasse: 7c</span></div>'


# ---------------------------------------------------------------- Kopf (wie Original)
WOLKE = ('<svg class="wolke" viewBox="0 0 120 92"><g fill="#1b1b1b">'
         '<circle cx="34" cy="38" r="24"/><circle cx="62" cy="28" r="26"/><circle cx="90" cy="40" r="22"/>'
         '<circle cx="80" cy="62" r="22"/><circle cx="46" cy="64" r="22"/><circle cx="24" cy="56" r="16"/><circle cx="100" cy="58" r="14"/></g>'
         '<text x="62" y="44" fill="#fff" font-size="15" font-weight="700" text-anchor="middle">Viel</text>'
         '<text x="62" y="63" fill="#fff" font-size="15" font-weight="700" text-anchor="middle">Erfolg!</text></svg>')


def kopf(l):
    return (f'<div class="kopfwrap"><table class="kopf">'
            '<tr><td colspan="2" class="titel"><u>Klassenarbeit Nr. 1</u></td><td class="kl">Klasse 7</td></tr>'
            '<tr><td class="n">Name:</td><td colspan="2" class="n">Unterschrift:</td></tr>'
            f'<tr><td class="n">Punkte: <span class="pp">/ {GESAMT} Punkte</span></td><td class="n">Note:</td><td class="n">Ø</td></tr>'
            f'</table>{WOLKE}</div>'
            + ('<p class="loesmark">Lösung mit Punkteverteilung</p>' if l else "")
            + '<div class="hinweis">Ohne Rechenweg keine Punkte. Aufgabe in die Kästchen abschreiben, dann rechnen.</div>')


# ---------------------------------------------------------------- Seite 1
PUNKTE = [("A", -4.3), ("B", -2.5), ("C", -0.8), ("D", 1.6), ("E", 4.9), ("F", 7.2)]


def zahlenstrahl(l, punkte=None, lo=-5, hi=8):
    punkte = PUNKTE if punkte is None else punkte
    u, x0 = 1664 / (hi - lo), 60
    X = lambda v: x0 + (v - lo) * u
    o = ['<svg class="zs" viewBox="0 0 1790 190">',
         f'<line x1="{X(lo) - 30}" y1="120" x2="{X(hi) + 40}" y2="120" stroke="#000" stroke-width="4"/>',
         f'<path d="M{X(hi) + 52},120 l-20,-9 v18z" fill="#1b1b1b"/>']
    for i in range((hi - lo) * 10 + 1):
        v = lo + i / 10
        h = 26 if i % 10 == 0 else (19 if i % 5 == 0 else 13)
        dicke = 4.5 if i % 10 == 0 else (3.4 if i % 5 == 0 else 2.6)
        o.append(f'<line x1="{X(v):.1f}" y1="{120 - h}" x2="{X(v):.1f}" y2="{120 + h}" stroke="#000" stroke-width="{dicke}"/>')
        if i % 10 == 0:
            o.append(f'<text x="{X(v):.1f}" y="180" font-size="32" font-weight="700" text-anchor="middle">{str(round(v)).replace("-", "−")}</text>')
    for b, v in punkte:
        o.append(f'<path d="M{X(v):.1f},86 l-8,-14 h16z" fill="#1b1b1b"/><line x1="{X(v):.1f}" y1="40" x2="{X(v):.1f}" y2="74" stroke="#1b1b1b" stroke-width="3"/>'
                 f'<text x="{X(v):.1f}" y="30" font-size="30" font-weight="700" text-anchor="middle">{b}</text>')
    o.append("</svg>")
    antw = "".join(f'<span class="zw"><b>{b}:</b> {box(str(v).replace(".", ",").replace("-", "−"), l, True)}</span>' for b, v in punkte)
    return "".join(o) + f'<div class="zsantw">{antw}</div>'


NR2 = [("−11", "13", "&lt;"), ("−2,1", "−4,3", "&gt;"), ("−2", "−1,9", "&lt;"),
       ("−0,9", "0,9", "&lt;"), ("−" + br("1", "4"), "−" + br("2", "8"), "="), ("−" + br("3", "7"), br("4", "7"), "&lt;")]
NR3 = [("−25 + 30", 0), ("25 − 38", 1), ("9 − 15", 1), ("−1,5 − 2,4", 1),
       ("6 · (−7)", 1), ("−3,75 · (−2,98)", 0), ("−35 : (−7)", 0), ("−111 : 3", 1)]


def seite1(l):
    nr2 = "".join(f'<span class="vg">{"abcdef"[i]}) &nbsp;{a} {box(z, l)} {b}</span>' for i, (a, b, z) in enumerate(NR2))
    nr3 = ('<table class="pn"><tr><th>Aufgabe</th><th>Positiv</th><th>Negativ</th></tr>'
           + "".join(f'<tr><td>{a}</td><td class="x">{"✗" if l and n == 0 else ""}</td><td class="x">{"✗" if l and n == 1 else ""}</td></tr>' for a, n in NR3)
           + "</table>")
    return (kopf(l)
            + balken(1, 3, "Benenne die markierten Zahlen A bis F." + (' <span class="pkt">(je ½ P)</span>' if l else "")) + zahlenstrahl(l)
            + balken(2, 6, "Setze &lt;, &gt; oder = ein." + (' <span class="pkt">(je 1 P)</span>' if l else "")) + f'<div class="vgl">{nr2}</div>'
            + balken(3, 4, "Ist das Ergebnis positiv oder negativ? Kreuze an." + (' <span class="pkt">(je ½ P)</span>' if l else "")) + nr3)


# ---------------------------------------------------------------- Seite 2
NR4 = [("−55 + 95", "40"), ("−57 − 75", "−132"),
       ("26 − 44", "−18"), ("−1,5 + 2,5", "1"),
       ("−103 − 3", "−106"), ("48 − 147", "−99"),
       ("−" + br("3", "4") + " + " + br("1", "2"), "−" + br("3", "4") + " + " + br("2", "4") + " = −" + br("1", "4")),
       ("−" + br("2", "5") + " − " + br("1", "5"), "−" + br("3", "5"))]


def liste(aufg):
    return '<div class="liste">' + "".join(f'<span>{"abcdefgh"[i]}) &nbsp;{a}</span>' for i, a in enumerate(aufg)) + "</div>"


def loesliste(paare):
    return "".join(f'<div class="lz">{"abcdefgh"[i]}) &nbsp;{a} = {r}</div>' for i, (a, r) in enumerate(paare))


def seite2(l):
    return (balken(4, 8, "Berechne. Schreibe jede Aufgabe ab und rechne darunter." + (' <span class="pkt">(je 1 P)</span>' if l else ""))
            + liste([a for a, _ in NR4]) + karo(None, loesliste(NR4), l))


# ---------------------------------------------------------------- Seite 3
NR5 = [("−28 : (−7)", "4"), ("−5 · 6", "−30"), ("−2 · 5 · (−4)", "40 &nbsp;<i>(zwei Minus → plus; 2 · 5 · 4)</i>"),
       ("−0,5 · 12", "−6"), ("−48 : (−6)", "8"), ("105 : (−5)", "−21")]
NR6 = [("−23 − 17 − 59 + 22 − 7", "−106 + 22 = −84", "1,5 P"),
       ("41,7 − 2,7 − 0,9 + 2,2", "39 − 0,9 + 2,2 = 40,3", "1,5 P"),
       ("−18 − (7 − 15)", "−18 − 7 + 15 = −10 &nbsp;<i>(auch: −18 − (−8) = −10)</i>", "2 P")]


def seite3(l):
    l6 = "".join(f'<div class="lz">{"abc"[i]}) &nbsp;{a} = {r} <span class="pkt">({p})</span></div>' for i, (a, r, p) in enumerate(NR6))
    return (balken(5, 6, "Berechne." + (' <span class="pkt">(je 1 P)</span>' if l else "")) + liste([a for a, _ in NR5])
            + karo(92, loesliste(NR5), l)
            + balken(6, 5, "Berechne.")
            + '<div class="liste eins">' + "".join(f'<span>{"abc"[i]}) &nbsp;{a}</span>' for i, (a, _, _) in enumerate(NR6)) + "</div>"
            + karo(None, l6, l))


# ---------------------------------------------------------------- Seite 4
KONTO = [("Alter Kontostand", "−520,00 €"), ("Gehalt", "+2770,00 €"), ("Miete", "−780,00 €"), ("Telefonrechnung", "−35,00 €"),
         ("Versicherung", "−210,00 €"), ("Gutschrift (zu viel bezahlte Heizkosten)", "+20,00 €")]


def seite4(l):
    konto = ('<table class="konto"><tr><th colspan="2">Kontoauszug von Herrn Reuter</th></tr>'
             + "".join(f'<tr><td>{a}</td><td class="b">{b}</td></tr>' for a, b in KONTO) + "</table>")
    l7 = ('<div class="lz">a) &nbsp;−520 + 2770 − 780 − 35 − 210 + 20 <span class="pkt">(1 P)</span></div>'
          '<div class="lz">b) &nbsp;Plus: 2770 + 20 = 2790 &nbsp; Minus: 520 + 780 + 35 + 210 = 1545</div>'
          '<div class="lz">&nbsp;&nbsp;&nbsp;&nbsp;2790 − 1545 = 1245 &nbsp; Neuer Kontostand: <b>+1245,00 €</b> <span class="pkt">(2 P)</span></div>')
    l8 = ('<div class="lz">a) &nbsp;8848 + 11 022 = 19 870 m &nbsp;<i>(8848 m über und 11 022 m unter dem Meeresspiegel)</i> <span class="pkt">(1 P)</span></div>'
          '<div class="lz">b) &nbsp;11 022 − 6857 = 4165 m <span class="pkt">(1 P)</span></div>')
    return (balken(7, 3) + f'<div class="sach">{konto}<div><p class="anw">a) Notiere <u>eine</u> Rechnung für den neuen Kontostand.</p>'
            '<p class="anw">b) Welchen Betrag hat Herr Reuter jetzt auf dem Konto? Berechne schriftlich.</p></div></div>'
            + karo(88, l7, l)
            + balken(8, 2, "Der Mount Everest ist 8848 m hoch. Der Marianengraben ist mit 11 022 m die tiefste Stelle im Meer. "
                     "Das Nordpolarmeer ist an seiner tiefsten Stelle 6857 m tief.")
            + '<p class="anw">a) Wie groß ist der Höhenunterschied zwischen dem Gipfel des Mount Everest und dem Marianengraben?</p>'
            '<p class="anw">b) Wie viel tiefer ist der Marianengraben als das Nordpolarmeer?</p>'
            + karo(None, l8, l))


CSS = """<style>
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;background:#d9dde3;font-family:Arial,"Liberation Sans",Helvetica,sans-serif;color:#1b1b1b;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.leiste{position:sticky;top:0;z-index:5;background:#1b1b1b;color:#fff;padding:10px 18px;font-size:14px;display:flex;gap:18px;align-items:center}
.leiste a{color:#fff}
.seite{width:210mm;height:297mm;margin:10mm auto;background:#fff;padding:12mm 14mm 13mm;position:relative;overflow:hidden;display:flex;flex-direction:column;page-break-after:always;box-shadow:0 2px 10px rgba(0,0,0,.15)}
.snr{position:absolute;bottom:5mm;left:0;right:0;text-align:center;font-size:9pt;color:#888}
.seite>*{flex:none}.kopfwrap{position:relative;margin-bottom:4mm}
.kopf{width:150mm;border-collapse:collapse;font-size:10.5pt}
.kopf td{border:.6pt solid #555;padding:2.2mm 2.5mm;font-weight:700}
.kopf .titel{background:#c8c8c8;text-align:center;font-size:11pt;width:115mm}.kopf .kl{font-weight:400;text-align:center}
.kopf .pp{margin-left:18mm}
.wolke{position:absolute;right:0;top:-2mm;width:30mm}
.loesmark{position:absolute;top:5mm;left:14mm;color:#E6007E;font-weight:700;margin:0;font-size:10pt}
.hinweis{border:.6pt solid #9a9a9a;padding:2mm 3mm;font-weight:700;font-size:12pt;margin-bottom:4mm}
.balken{display:flex;justify-content:space-between;border:.6pt solid #9a9a9a;padding:1.8mm 3mm;margin:4mm 0 2mm;font-size:12.5pt}
.balken .pk{font-weight:700}
.anw{margin:1mm 0 2mm;font-size:12.5pt;line-height:1.4}
.pkt{color:#E6007E;font-weight:400;font-size:10pt}
.namen{display:flex;gap:60mm;border:.6pt solid #9a9a9a;padding:1.8mm 3mm;font-size:10.5pt}
.zs{width:100%;display:block;margin:1mm 0 0}
.zsantw{display:flex;justify-content:space-between;margin:2mm 0 1mm;font-size:13.5pt}
.zw{display:flex;align-items:center;gap:2mm}
.kast{display:inline-flex;align-items:center;justify-content:center;width:11mm;height:12mm;border:.8pt solid #1b1b1b;vertical-align:middle;color:#E6007E;font-weight:700;font-size:13pt;margin:0 1.5mm}
.kast.breit{width:19mm}
.vgl{display:grid;grid-template-columns:repeat(3,1fr);row-gap:4mm;font-size:15pt;margin:2mm 0 1mm;white-space:nowrap}
.vg{display:flex;align-items:center}
.br{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.85em;line-height:1.1;margin:0 .1em}
.br span:first-child{border-bottom:1.2px solid currentColor;padding:0 .15em}
.pn{align-self:flex-start;border-collapse:collapse;font-size:14.5pt;margin:2mm 0 0 8mm}
.pn th{background:#c8c8c8;border:.6pt solid #555;padding:1.6mm 4mm;text-align:left}
.pn td{border:.6pt solid #555;padding:0 4mm;height:9.4mm;min-width:66mm}
.pn td.x{min-width:24mm;text-align:center;color:#E6007E;font-weight:700;font-size:15pt}
.liste{display:grid;grid-template-columns:repeat(2,1fr);row-gap:3.5mm;font-size:15.5pt;margin:2mm 0 3mm;white-space:nowrap}
.liste.eins{grid-template-columns:1fr}
.karo{width:100%;border:.6pt solid #9fb3c8;background-color:#fff;
 background-image:linear-gradient(#b9c8d8 .25mm,transparent .25mm),linear-gradient(90deg,#b9c8d8 .25mm,transparent .25mm);
 background-size:5mm 5mm;background-position:-.25mm -.25mm;margin-bottom:2mm;position:relative}
.loes{padding:3mm 4mm;color:#E6007E;font-size:14pt;font-weight:700}
.lz{line-height:10mm;white-space:nowrap}.lz i{font-weight:400;font-size:10pt}
.lz .br{font-size:.8em;line-height:1}
.sach{display:grid;grid-template-columns:auto 1fr;gap:7mm;align-items:start;margin-bottom:5mm}
.konto{border-collapse:collapse;font-size:12.5pt}
.konto th{background:#c8c8c8;border:.6pt solid #555;padding:1.6mm 3mm;text-align:left}
.konto td{border:.6pt solid #555;padding:1.4mm 3mm}.konto td.b{text-align:right;white-space:nowrap}
.trenner{width:210mm;margin:14mm auto 0;font:700 20px Arial;color:#1b1b1b}
@media print{body{background:#fff}.leiste,.trenner{display:none}.seite{margin:0;box-shadow:none}}
</style>"""


def druckfassung(l):
    """Nur Aufgaben (l=False) oder nur Lösung (l=True), ohne Leiste, für das PDF. Gibt (HTML, Seitenzahl) zurück."""
    seiten = [seite1, seite2, seite3, seite4]
    teil = "".join(f'<section class="seite">{s(l)}<div class="snr">Seite {i + 1} von {len(seiten)}</div></section>' for i, s in enumerate(seiten))
    return ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen</title>' + CSS
            + '</head><body>' + teil + '</body></html>'), len(seiten)


def main():
    seiten = [seite1, seite2, seite3, seite4]
    teil = lambda l: "".join(f'<section class="seite">{s(l)}<div class="snr">Seite {i + 1} von 4</div></section>' for i, s in enumerate(seiten))
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Entwurf</title>' + CSS + '</head><body>'
            '<div class="leiste"><b>Klassenarbeit Nr. 1 · Klasse 7c · Entwurf</b><a href="#arbeit">Arbeit (4 Seiten)</a><a href="#loesung">Lösung (4 Seiten)</a>'
            f'<span>{GESAMT} Punkte · Druck: A3 als Broschüre, gefaltet</span></div>'
            '<div class="trenner" id="arbeit">Arbeit</div>' + teil(False)
            + '<div class="trenner" id="loesung">Lösung</div>' + teil(True) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name)


if __name__ == "__main__":
    main()
