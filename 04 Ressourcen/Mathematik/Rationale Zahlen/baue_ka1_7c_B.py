#!/usr/bin/env python3
"""Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen (eigene Fassung der Parallelarbeit, ca. 85 % übernommen).
Layout wie Oskars Kurztest Kl. 10: Aufgabenbalken oben, darunter Karofläche für die Rechnung.
4 A4-Seiten = ein gefaltetes A3-Blatt. Danach dieselben 4 Seiten als Lösung.
Nur HTML (Entwurf zum Besprechen), PDF erst nach Freigabe."""
from fractions import Fraction as F
from pathlib import Path

HIER = Path(__file__).parent
ZIEL = HIER / "Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Gruppe B – Entwurf.html"
MAG = "#E6007E"
GESAMT = 37

# ---------------------------------------------------------------- Prüfung aller Lösungen
assert -65 + 90 == 25 and -48 - 86 == -134 and 32 - 51 == -19 and F("-2.5") + F("4.5") == 2
assert F(-107) - 4 == -111 and 53 - 151 == -98 and F(-3, 8) + F(1, 4) == F(-1, 8) and F(-3, 7) - F(2, 7) == F(-5, 7)
assert F(-42) / -6 == 7 and F(-45) / -9 == 5 and F(-7) * 4 == -28 and F(-3) * 5 * -2 == 30 and F("-0.5") * 14 == -7 and F(-54) / -6 == 9 and F(135) / -5 == -27
assert -31 - 19 - 48 + 26 - 9 == -81 and F("36.4") - F("1.4") - F("0.8") + F("2.3") == F("36.5") and -14 - (6 - 13) == -7
assert -460 + 2640 - 720 - 29 - 185 + 35 == 1281 and 5895 + 11022 == 16917 and 11022 - 5109 == 5913
assert F(-1, 3) == F(-2, 6) and F(-2, 9) < F(5, 9) and -3 < F("-2.8") and F("-3.2") > F("-5.6")


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
            '<tr><td colspan="2" class="titel"><u>Klassenarbeit Nr. 1 (Gruppe B)</u></td><td class="kl">Klasse 7</td></tr>'
            '<tr><td class="n">Name:</td><td colspan="2" class="n">Unterschrift:</td></tr>'
            f'<tr><td class="n">Punkte: <span class="pp">/ {GESAMT} Punkte</span></td><td class="n">Note:</td><td class="n">Ø</td></tr>'
            f'</table>{WOLKE}</div>'
            + ('<p class="loesmark">Lösung mit Punkteverteilung</p>' if l else "")
            + '<div class="hinweis">Ohne Rechenweg keine Punkte. Aufgabe in die Kästchen abschreiben, dann rechnen.</div>')


# ---------------------------------------------------------------- Seite 1
PUNKTE = [("A", -4.7), ("B", -2.9), ("C", -1.3), ("D", 2.4), ("E", 5.6), ("F", 7.4)]


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


NR2 = [("−9", "14", "&lt;"), ("−3,2", "−5,6", "&gt;"), ("−3", "−2,8", "&lt;"),
       ("−0,7", "0,7", "&lt;"), ("−" + br("1", "3"), "−" + br("2", "6"), "="), ("−" + br("2", "9"), br("5", "9"), "&lt;")]
NR3 = [("−18 + 24", 0), ("21 − 34", 1), ("7 − 12", 1), ("−2,5 − 1,6", 1),
       ("8 · (−5)", 1), ("−4,25 · (−3,02)", 0), ("−42 : (−6)", 0), ("−114 : 3", 1)]


def hilfsfeld():
    """Karofeld direkt nach dem Kopf: Platz für einen oder zwei selbst gezeichnete Zahlenstrahlen als Hilfe (ca. 8 cm hoch)."""
    return ('<div class="hilfe"><span>Platz für deine Zahlenstrahlen</span></div>'
            '<div class="karo" style="height:80mm;flex:none"></div>')


def seite1(l):
    nr2 = "".join(f'<span class="vg">{"abcdef"[i]}) &nbsp;{a} {box(z, l)} {b}</span>' for i, (a, b, z) in enumerate(NR2))
    return (kopf(l) + hilfsfeld()
            + balken(1, 3, "Benenne die markierten Zahlen A bis F." + (' <span class="pkt">(je ½ P)</span>' if l else "")) + zahlenstrahl(l)
            + balken(2, 6, "Setze &lt;, &gt; oder = ein." + (' <span class="pkt">(je 1 P)</span>' if l else "")) + f'<div class="vgl">{nr2}</div>')


def nr3_block(l):
    """Nr. 3 steht seit dem Hilfsfeld auf Seite 2."""
    nr3 = ('<table class="pn"><tr><th>Aufgabe</th><th>Positiv</th><th>Negativ</th></tr>'
           + "".join(f'<tr><td>{a}</td><td class="x">{"✗" if l and n == 0 else ""}</td><td class="x">{"✗" if l and n == 1 else ""}</td></tr>' for a, n in NR3)
           + "</table>")
    return balken(3, 4, "Ist das Ergebnis positiv oder negativ? Kreuze an." + (' <span class="pkt">(je ½ P)</span>' if l else "")) + nr3


# ---------------------------------------------------------------- Seite 2
NR4 = [("−65 + 90", "25"), ("−48 − 86", "−134"),
       ("32 − 51", "−19"), ("−2,5 + 4,5", "2"),
       ("−107 − 4", "−111"), ("53 − 151", "−98"),
       ("−" + br("3", "8") + " + " + br("1", "4"), "−" + br("3", "8") + " + " + br("2", "8") + " = −" + br("1", "8")),
       ("−" + br("3", "7") + " − " + br("2", "7"), "−" + br("5", "7"))]


def liste(aufg):
    return '<div class="liste">' + "".join(f'<span>{"abcdefgh"[i]}) &nbsp;{a}</span>' for i, a in enumerate(aufg)) + "</div>"


def loesliste(paare):
    return "".join(f'<div class="lz">{"abcdefgh"[i]}) &nbsp;{a} = {r}</div>' for i, (a, r) in enumerate(paare))


def seite2(l):
    return (nr3_block(l) + balken(4, 8, "Berechne. Schreibe jede Aufgabe ab und rechne darunter." + (' <span class="pkt">(je 1 P)</span>' if l else ""))
            + liste([a for a, _ in NR4]) + karo(None, loesliste(NR4), l))


# ---------------------------------------------------------------- Seite 3
NR5 = [("−45 : (−9)", "5"), ("−7 · 4", "−28"), ("−3 · 5 · (−2)", "30 &nbsp;<i>(zwei Minus → plus; 3 · 5 · 2)</i>"),
       ("−0,5 · 14", "−7"), ("−54 : (−6)", "9"), ("135 : (−5)", "−27")]
NR6 = [("−31 − 19 − 48 + 26 − 9", "−107 + 26 = −81", "1,5 P"),
       ("36,4 − 1,4 − 0,8 + 2,3", "35 − 0,8 + 2,3 = 36,5", "1,5 P"),
       ("−14 − (6 − 13)", "−14 − 6 + 13 = −7 &nbsp;<i>(auch: −14 − (−7) = −7)</i>", "2 P")]


def seite3(l):
    l6 = "".join(f'<div class="lz">{"abc"[i]}) &nbsp;{a} = {r} <span class="pkt">({p})</span></div>' for i, (a, r, p) in enumerate(NR6))
    return (balken(5, 6, "Berechne." + (' <span class="pkt">(je 1 P)</span>' if l else "")) + liste([a for a, _ in NR5])
            + karo(92, loesliste(NR5), l)
            + balken(6, 5, "Berechne.")
            + '<div class="liste eins">' + "".join(f'<span>{"abc"[i]}) &nbsp;{a}</span>' for i, (a, _, _) in enumerate(NR6)) + "</div>"
            + karo(None, l6, l))


# ---------------------------------------------------------------- Seite 4
KONTO = [("Alter Kontostand", "−460,00 €"), ("Gehalt", "+2640,00 €"), ("Miete", "−720,00 €"), ("Telefonrechnung", "−29,00 €"),
         ("Versicherung", "−185,00 €"), ("Gutschrift (zu viel bezahlte Heizkosten)", "+35,00 €")]


def seite4(l):
    konto = ('<table class="konto"><tr><th colspan="2">Kontoauszug von Frau Winter</th></tr>'
             + "".join(f'<tr><td>{a}</td><td class="b">{b}</td></tr>' for a, b in KONTO) + "</table>")
    l7 = ('<div class="lz">a) &nbsp;−460 + 2640 − 720 − 29 − 185 + 35 <span class="pkt">(1 P)</span></div>'
          '<div class="lz">b) &nbsp;Plus: 2640 + 35 = 2675 &nbsp; Minus: 460 + 720 + 29 + 185 = 1394</div>'
          '<div class="lz">&nbsp;&nbsp;&nbsp;&nbsp;2675 − 1394 = 1281 &nbsp; Neuer Kontostand: <b>+1281,00 €</b> <span class="pkt">(2 P)</span></div>')
    l8 = ('<div class="lz">a) &nbsp;5895 + 11 022 = 16 917 m &nbsp;<i>(5895 m über und 11 022 m unter dem Meeresspiegel)</i> <span class="pkt">(1 P)</span></div>'
          '<div class="lz">b) &nbsp;11 022 − 5109 = 5913 m <span class="pkt">(1 P)</span></div>')
    return (balken(7, 3) + f'<div class="sach">{konto}<div><p class="anw">a) Notiere <u>eine</u> Rechnung für den neuen Kontostand.</p>'
            '<p class="anw">b) Welchen Betrag hat Frau Winter jetzt auf dem Konto? Berechne schriftlich.</p></div></div>'
            + karo(88, l7, l)
            + balken(8, 2, "Der Kilimandscharo ist 5895 m hoch. Der Marianengraben ist mit 11 022 m die tiefste Stelle im Meer. "
                     "Das Mittelmeer ist an seiner tiefsten Stelle 5109 m tief.")
            + '<p class="anw">a) Wie groß ist der Höhenunterschied zwischen dem Gipfel des Kilimandscharo und dem Marianengraben?</p>'
            '<p class="anw">b) Wie viel tiefer ist der Marianengraben als das Mittelmeer?</p>'
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
.hilfe{border:.6pt solid #9a9a9a;border-bottom:0;padding:1.2mm 3mm;font-size:11pt;font-weight:700;background:#e9e9e9}
.hilfe+.karo{margin-bottom:4mm}
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
.pn td{border:.6pt solid #555;padding:0 4mm;height:8.4mm;min-width:66mm}
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
            '<div class="leiste"><b>Klassenarbeit Nr. 1 (Gruppe B); Klasse 7c; Entwurf</b><a href="#arbeit">Arbeit (4 Seiten)</a><a href="#loesung">Lösung (4 Seiten)</a>'
            f'<span>{GESAMT} Punkte; Druck: A3 als Broschüre, gefaltet</span></div>'
            '<div class="trenner" id="arbeit">Arbeit</div>' + teil(False)
            + '<div class="trenner" id="loesung">Lösung</div>' + teil(True) + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    print("geschrieben:", ZIEL.name)


if __name__ == "__main__":
    main()
