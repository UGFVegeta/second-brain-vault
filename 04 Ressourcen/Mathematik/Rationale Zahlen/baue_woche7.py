#!/usr/bin/env python3
"""Mathe 7c, Woche 7: Gemischte Aufgaben nach Rezept (Verbinden der Rechenarten). Eine Stunde, 45 Minuten.
Setzt Oskars Konzept um (04 Ressourcen/Mathematik/Mein Mathe-Konzept – Aufgaben in kleine Schritte zerlegen.md):
erst den Typ erkennen, dann kleine feste Schritte, Rezept mit Wenn-Dann. Wochenformat wie baue_woche3.py.
Alle Ergebnisse werden beim Bauen mit Python nachgerechnet (assert), auch jeder Zwischenschritt.
Aufruf: python3 baue_woche7.py  -> „Mathe 7c – Woche 7 – 1 Rezept für gemischte Aufgaben.html“ (nur HTML, Folien-PDF erst nach Freigabe)"""
import re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
from mathe_woche_vorlage import bau_woche  # noqa: E402

NAME = "Mathe 7c – Woche 5 – 1 Rezept für gemischte Aufgaben.html"


# ---------- Rechnen und Anzeigen ----------
def wert(s):
    """Wert eines Ausdrucks in ASCII-Schreibweise (HTML-Markierungen werden ignoriert)."""
    s = s.replace("<sup>", "**(").replace("</sup>", ")")
    s = re.sub(r"<[^>]+>", "", s).replace("−", "-").replace("·", "*").replace("÷", "/").replace(":", "/")
    s = re.sub(r"(\d),(\d)", r"\1.\2", s)                     # Dezimalkomma
    return round(eval(s), 9)


LUECKE = '<span class="luecke" contenteditable="true" spellcheck="false"></span>'   # in der HTML beschreibbar, im PDF leer
LUECKE_LANG = '<span class="luecke lang" contenteditable="true" spellcheck="false"></span>'   # für Zahlen mit Einheit (z. B. 12 800 €)
# Im PDF (Notability, Stift) haben die Kästchen feste Größen in mm, siehe PDF_LUECKEN_CSS.
PDF_LUECKEN_CSS = (".luecke{min-width:14mm!important;height:13mm!important;vertical-align:middle!important;margin:1mm 2mm!important}"
                   ".luecke.lang{min-width:32mm!important}.wbl .luecke{min-width:30mm!important;height:20mm!important}")    # leeres Kästchen zum Reinschreiben (Oskar: kein schwarzes ■)


def raster_stil(texte, gross):
    """Spaltenraster, in dem keine Aufgabe umbricht: Spaltenbreite nach der längsten Aufgabe (ca. 0,5 em je Zeichen)."""
    laenge = max(len(re.sub(r"<[^>]+>", "", t.replace(LUECKE_LANG, "■■■■■■■■").replace(LUECKE, "■■■"))) for t in texte)
    return f'font-size:{gross}px;grid-template-columns:repeat(auto-fill,minmax({laenge * 0.58 + 2.5:.1f}em,1fr))'


def zeig(s):
    """ASCII-Ausdruck -> Anzeige mit echtem Minus, Malpunkt und Geteilt-Zeichen (Tags bleiben)."""
    teile = re.split(r"(<[^>]+>)", s)
    return "".join(t if t.startswith("<") else t.replace("-", "−").replace("*", "·").replace("/", "÷") for t in teile)


def zahl(x):
    x = round(x, 9)
    t = str(int(x)) if x == int(x) else str(x).replace(".", ",")
    return t.replace("-", "−")


def weg(*schritte):
    """Rechenweg: mehrere Zeilen, alle müssen denselben Wert haben. Gibt HTML zurück."""
    w = {wert(s) for s in schritte}
    assert len(w) == 1, (schritte, w)
    z = [f'<div class="ausdruck">{"" if i else ""}{"= " if i else ""}{zeig(s)}</div>' for i, s in enumerate(schritte)]
    z[-1] = z[-1].replace("</div>", "</div>", 1)
    return "".join(z), w.pop()


def ergebnis(aufgabe, *schritte):
    html, v = weg(aufgabe, *schritte)
    return html.rsplit("</div>", 1)[0] + f' <span class="lsg">(Ergebnis: {zahl(v)})</span></div>'


P = lambda s: f'<span class="pb">{s}</span>'          # Mal-/Geteilt-Block markieren
HEFT = lambda h: f'<div class="heft">{h}</div>'        # schwarzer Balken: Merkheft
UEB = lambda h: f'<div class="uheft">{h}</div>'        # blau gestrichelt: Übungsheft

# ---------- Aufgaben ----------
BLITZ = [("6·(−4)", "6*(-4)"), ("−5·(−7)", "-5*(-7)"), ("−36 ÷ 9", "-36/9"), ("48 ÷ (−6)", "48/(-6)"),
         ("−2,5·4", "-2.5*4"), ("−1,2·(−5)", "-1.2*(-5)"), ("−7,5 ÷ (−5)", "-7.5/(-5)"), ("0,4·(−30)", "0.4*(-30)")]
BLITZ_L = [(a, zahl(wert(e))) for a, e in BLITZ]
assert [b for _, b in BLITZ_L] == ["−24", "35", "−4", "−8", "−10", "6", "1,5", "−12"]

BSP1 = "5 - 3*(-4) + 18/(-6)"
BSP2 = "15 - 2*(6 - 9) + 24/(-3)"
BSP3 = "-12 - (8 - 30 + 4)"

UEB_O = ["8 - 3*4", "-6 + 20/(-4)", "2*(-5) - 7", "-18/3 + 10", "4 - 2*(-3)"]
UEB_M = ["-7 + 3*(-5) - 4*(-2)", "12 - 24/(-6) + 5", "-2*(-9) - 15/3 - 20", "3*(-4) - 2*(-6) + 1", "-30/5 - 4*(-3) + 9"]
UEB_S = ["5*(-3) - (4 - 2*6)", "-(7 - 3*4) + 20/(-5)", "36/(-9) - 2*(-7) - (5 - 11)", "-18/(3 - 9) - 4*(2 - 5)"]
# Zwischenschritte der schweren Aufgaben, jeweils vom Original bis zum Ergebnis
UEB_S_WEG = [("5*(-3) - (4 - 2*6)", "5*(-3) - (4 - 12)", "5*(-3) - (-8)", "-15 + 8", "-7"),
             ("-(7 - 3*4) + 20/(-5)", "-(7 - 12) + 20/(-5)", "-(-5) + 20/(-5)", "5 - 4", "1"),
             ("36/(-9) - 2*(-7) - (5 - 11)", "36/(-9) - 2*(-7) - (-6)", "-4 + 14 + 6", "16"),
             ("-18/(3 - 9) - 4*(2 - 5)", "-18/(-6) - 4*(-3)", "3 + 12", "15")]
UEB_ERG = {"o": ["-4", "-11", "-17", "4", "10"], "m": ["-14", "21", "-7", "1", "15"]}
for liste, key in ((UEB_O, "o"), (UEB_M, "m")):
    assert [round(wert(a)) for a in liste] == [int(x) for x in UEB_ERG[key]], key
for w in UEB_S_WEG:
    assert len({wert(s) for s in w}) == 1, w

FEHLER = "8 - 2*(-3)"
EXIT = ["7 - 3*(-4) + 10/(-5)", "-2*(-6) - (9 - 4*3)"]
EXIT_WEG = [("7 - 3*(-4) + 10/(-5)", "7 + 12 - 2", "17"), ("-2*(-6) - (9 - 4*3)", "-2*(-6) - (9 - 12)", "12 - (-3)", "12 + 3", "15")]
for w in EXIT_WEG:
    assert len({wert(s) for s in w}) == 1, w
assert [wert(a) for a in EXIT] == [17, 15]

# ---------- Beispielrechnungen (Tafel und Folie) ----------
B1_MARK = f'5 {P("− 3·(−4)")} {P("+ 18 ÷ (−6)")}'
B1 = ('<div class="schritt"><span class="sn">1</span>Blöcke markieren'
      f'<div class="ausdruck">{B1_MARK}</div></div>'
      '<div class="schritt"><span class="sn">2</span>Jeder Block einzeln'
      '<div class="ausdruck">− 3·(−4): gleich, <span class="lsg">+ 12</span></div>'
      '<div class="ausdruck">+ 18 ÷ (−6): verschieden, <span class="lsg">− 3</span></div></div>'
      '<div class="schritt"><span class="sn">3</span>Rest'
      '<div class="ausdruck">5 + 12 − 3 = <span class="lsg">14</span></div></div>')
assert wert(BSP1) == 14 and wert("5 + 12 - 3") == 14
B2 = ('<div class="schritt"><span class="sn">1</span>Klammer zuerst'
      f'<div class="ausdruck">15 − 2·{P("(6 − 9)")} + 24 ÷ (−3)</div><div class="ausdruck">= 15 − 2·(−3) + 24 ÷ (−3)</div></div>'
      '<div class="schritt"><span class="sn">2</span>Jeder Block einzeln'
      '<div class="ausdruck">− 2·(−3): gleich, <span class="lsg">+ 6</span></div>'
      '<div class="ausdruck">+ 24 ÷ (−3): verschieden, <span class="lsg">− 8</span></div></div>'
      '<div class="schritt"><span class="sn">3</span>Rest'
      '<div class="ausdruck">15 + 6 − 8 = <span class="lsg">13</span></div></div>')
assert wert(BSP2) == 13 and wert("15 + 6 - 8") == 13
B3 = ('<div class="schritt"><span class="sn">1</span>Minusklammer auflösen, alles umdrehen'
      '<div class="ausdruck">−12 − (8 − 30 + 4) = −12 − 8 + 30 − 4</div></div>'
      '<div class="schritt"><span class="sn">2</span>Rest'
      '<div class="ausdruck">−12 − 8 − 4 + 30 = −24 + 30 = <span class="lsg">6</span></div></div>')
assert wert(BSP3) == 6 and wert("-12 - 8 + 30 - 4") == 6 and wert("-24 + 30") == 6

def rezept_box(titel, schritte):
    """Rezept als nummerierte Kurzbefehle, wie in Oskars Tafelbild (Bruchgleichungen)."""
    return f'<div class="rezept"><h4>{titel}</h4><ol class="rs">' + "".join(f"<li>{x}</li>" for x in schritte) + "</ol></div>"


def merkbild(titel, zeilen, schritte, weitere=None):
    """Merkheft-Bild wie an der Tafel: links das Beispiel Zeile für Zeile, Schrittnummer vorne, rechts das Rezept.
    zeilen: [(Schrittnummer oder None, HTML)] oder mehrere Beispiele als Liste solcher Listen.
    Innerhalb eines Beispiels müssen alle Rechenzeilen denselben Wert haben (wird geprüft); Zeilen nur mit
    Zeichnung oder Hinweis (class="klein") werden dabei übersprungen."""
    beispiele = zeilen if zeilen and isinstance(zeilen[0], list) else [zeilen]
    links = ""
    for k, bsp in enumerate(beispiele):
        werte = set()
        for _, h in bsp:
            ausdruck = re.sub(r'<span class="(?:klein|txt)">.*?</span>|<svg.*?</svg>|<figure.*?</figure>', "", h, flags=re.S)
            ausdruck = re.sub(r"<(?!/?sup)[^>]+>", "", ausdruck).lstrip("=≈ ").strip()
            ausdruck = ("≈" if "≈" in h else "") + ausdruck
            if ausdruck:
                werte.add(ausdruck)
        rund = any("≈" in a for a in werte)            # gerundete Zeile: auf Cent vergleichen
        werte = {round(wert(a.replace("≈", "").strip()), 2 if rund else 9) for a in werte}
        assert len(werte) == 1, (titel, k, werte)
        links += ('<div class="mz-trenn"></div>' if k else "") + "".join(
            f'<div class="mz">{f"<span class=sn>{n}</span>" if n else "<span class=leer></span>"}<span>{h}</span></div>' for n, h in bsp)
    if weitere:     # weitere Beispiele, je eine Zeile: (Aufgabe, Ergebnis-HTML, Ergebniswert) – Oskar: mindestens 6 Beispiele im Merkheft
        for a, _, e in weitere:
            assert round(wert(a), 6) == round(e, 6), (titel, a, wert(a), e)
        links += ('<div class="weitere"><div class="weitere-t">Weitere Beispiele</div>'
                  + "".join(f'<div class="wz">{a} = {h}</div>' for a, h, _ in weitere) + "</div>")
    return f'<div class="mb"><div>{links}</div>{rezept_box(titel, schritte)}</div>'


REZEPT = rezept_box("Gemischte Aufgaben", ["Klammer? Innen zuerst. Minus davor und nur + und − drin: umdrehen.", "Mal- und Geteilt-Blöcke markieren.",
                                           "Jeden Block rechnen: gleiche Zeichen +, verschiedene −.", "Gleiche Zeichen zusammen.", "Ausrechnen."])
MERK = merkbild("Gemischte Aufgaben",
                [(1, '15 − 2·<span class="rot">(6 − 9)</span> + 24 ÷ (−3)'),
                 (None, '= 15 − 2·<span class="rot">(−3)</span> + 24 ÷ (−3)'),
                 (2, f'= 15 {P("− 2·(−3)")} {P("+ 24 ÷ (−3)")}'),
                 (3, '= 15 <span class="rot">+ 6</span> <span class="rot">− 8</span>'),
                 (4, '= <span class="gelb">15 + 6</span> − 8'),
                 (None, '= 21 − 8'),
                 (5, '= <b>13</b>')],
                ["Klammer? Innen zuerst. Minus davor und nur + und − drin: umdrehen.", "Mal- und Geteilt-Blöcke markieren.",
                 "Jeden Block rechnen: gleiche Zeichen +, verschiedene −.", "Gleiche Zeichen zusammen.", "Ausrechnen."])

EXTRA_CSS = """<style>
.pb{border-bottom:3px solid #E6007E;padding-bottom:1px}
.schritt{margin:10px 0;padding:6px 0 4px}.schritt .ausdruck{margin:4px 0 4px 28px;font-size:22px}
.sn{display:inline-flex;width:24px;height:24px;border-radius:50%;background:#1b1b1b;color:#fff;font-weight:700;font-size:13px;align-items:center;justify-content:center;margin-right:8px}
.rezept{background:#eef3fb;border:2px solid #1a56a0;border-radius:8px;padding:6px 18px 12px;margin:10px 0}
.rezept h4{margin:8px 0 4px;font-size:20px}.rezept .r0{font-weight:700;margin:4px 0 8px}
.rz{margin:8px 0}.rz ul{margin:2px 0 0;padding-left:22px}.rz li{margin:2px 0}
.warum{font-size:.92em;color:#334a66;margin:10px 0 0}
.mb{display:grid;grid-template-columns:1.25fr 1fr;gap:26px;align-items:start}.mz{display:flex;align-items:center;gap:10px;font-size:24px;font-weight:700;margin:7px 0}.mz .sn{flex:none;margin:0}.leer{width:24px;flex:none}.mz-trenn{height:14px}.mz svg{max-width:100%;height:auto}
.rot{color:#d2232a}.gelb{background:#fde68a;border-radius:3px;padding:0 3px}.txt{font-weight:400}.klein{font-size:15px;font-weight:400;color:#66798e;margin-left:10px}.rs{margin:4px 0 0;padding-left:22px}.rs li{margin:6px 0}
.luecke.lang{min-width:4.5em}.luecke{display:inline-flex;align-items:center;justify-content:center;min-width:1.9em;height:2.3em;font-weight:700;color:#E6007E;outline:none;white-space:nowrap;cursor:text;border:2px solid #1b1b1b;border-radius:4px;vertical-align:-.75em;margin:2px 4px;background:#fff}.weitere{margin:12px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(13em,1fr));gap:2px 24px}.weitere-t{grid-column:1/-1;font-size:13px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#66798e}.wz{font-size:22px;font-weight:700;white-space:nowrap}.wbq{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px}.wbk{border:2px solid #1b1b1b;border-radius:12px;padding:14px 10px;text-align:center;display:flex;flex-direction:column;justify-content:space-between;align-items:center;min-height:74mm}.wbn{font-weight:700;color:#66798e;font-size:20px}.wba{font-size:46px;font-weight:700;white-space:nowrap}.wbf{font-size:17px;color:#4a5563}.wbl{font-size:60px;font-weight:700;min-height:1.2em}.wbl .luecke{width:1.9em;height:2.3em;border-width:3px}.auftrag{border:2px solid #1a56a0;background:#eef3fb;border-radius:8px;padding:8px 14px;margin:0 0 12px;font-size:18px;line-height:1.5}.auftrag-k{font-size:14px;color:#4a5563}.umkehr{border-collapse:collapse;width:100%}.umkehr td{padding:8px 6px;border-bottom:1px solid #e3e5ea;white-space:nowrap}.umkehr .u-m{color:#4a5563}.umkehr .u-p{font-size:15px;color:#66798e}.umkehr .u-d{font-weight:700}.ex li{white-space:nowrap}.block{margin:6px 0 18px}.block h4{margin:0 0 6px;font-size:18px}.ex.raster{display:grid;column-gap:30px;row-gap:2px;list-style-position:inside;padding-left:0}.ex.raster li{margin:3px 0}
.mit{display:grid;grid-template-columns:1.25fr 1fr;gap:22px;align-items:start}.mit .rezept{margin:0;font-size:15px}.mit .ex{font-size:24px}.mit h4{margin:0 0 6px}
.drei{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.drei h4{margin:0 0 6px}.drei ol{margin:0;padding-left:26px;font-size:22px;line-height:1.7}
</style>"""


def box(t, h):
    return f'<div class="box"><h3>{t}</h3>{h}</div>'


def reihe(liste, grosz=True):
    return "".join(f"<li>{zeig(a)} =</li>" for a in liste)


# ---------- Folien ----------
BLITZ_A = '<ol type="a" class="kl">' + "".join(f"<li>{a} =</li>" for a, _ in BLITZ) + "</ol>"
BLITZ_LF = '<ol type="a" class="kl">' + "".join(f'<li>{a} = <span class="lsg">{b}</span></li>' for a, b in BLITZ_L) + "</ol>"
VIEL = '<div class="ausdruck">15 − 2·(6 − 9) + 24 ÷ (−3)</div><p class="gross">Was zuerst?</p>'
FEHLER_A = f'<div class="ausdruck">{zeig(FEHLER)} = 6·(−3) = −18</div><p class="gross">Stimmt das?</p>'
assert wert(FEHLER) == 14
FEHLER_L = ('<div class="ausdruck">8 − 2·(−3) = 6·(−3) <span class="lsg">✗</span></div>'
            '<div class="ausdruck">8 <span class="pb">− 2·(−3)</span> = 8 + 6 = <span class="lsg">14</span></div>')
EXIT_A = f'<ol type="a" class="ex">{reihe(EXIT)}</ol>'


def weg_liste(w):
    """Rechenweg in einer Zeile (passt auch auf eine Folie, wenn mehrere Aufgaben untereinander stehen)."""
    return (f'<div class="ausdruck" style="font-size:24px">{" = ".join(zeig(s) for s in w[:-1])} = '
            f'<span class="lsg">{zahl(wert(w[-1]))}</span></div>')


def mit(titel, liste):
    """Aufgabenrunde links, das Rezept als kurzer Kasten daneben."""
    return f'<div class="mit"><div><h4>{titel}</h4><ol type="a" class="ex">{reihe(liste)}</ol></div>{REZEPT}</div>'


def ergebnisse(liste):
    return '<ol type="a" class="ex">' + "".join(f'<li>{zeig(a)} = <span class="lsg">{zahl(wert(a))}</span></li>' for a in liste) + "</ol>"


EXIT_L = "".join(f'<div class="fnr">{"ab"[i]})</div>' + weg_liste(w) for i, w in enumerate(EXIT_WEG))
UEB_L_S = "".join(f'<div class="fnr">{"abcd"[i]})</div>' + weg_liste(w) for i, w in enumerate(UEB_S_WEG))

FOLIEN = [
    ("Blitzrunde: Mal und Geteilt", UEB(BLITZ_A)),
    ("Blitzrunde: Lösungen", BLITZ_LF),
    ("Auf den ersten Blick viel", VIEL),
    ("Merkheft: Gemischte Aufgaben", HEFT(MERK)),
    ("Runde 1", UEB(mit("○ leicht", UEB_O))),
    ("Runde 1: Lösungen", ergebnisse(UEB_O)),
    ("Runde 2", UEB(mit("◐ mittel", UEB_M))),
    ("Runde 2: Lösungen", ergebnisse(UEB_M)),
    ("Runde 3", UEB(mit("● schwer", UEB_S))),
    ("Runde 3: Lösungen", UEB_L_S),
    ("Wo steckt der Fehler?", UEB(FEHLER_A)),
    ("Wo steckt der Fehler? Lösung", FEHLER_L),
    ("Exit-Ticket", UEB(EXIT_A)),
    ("Exit-Ticket: Lösung", EXIT_L),
]

SCHRITTE = [
    ("", "Blitzrunde Mal und Geteilt", 5, "Nur Ergebnisse ins Übungsheft. Sitzt die Vorzeichenregel?", [1, 2]),
    ("", "Auf den ersten Blick viel", 3, "Lange Aufgabe zeigen, nur fragen: Was zuerst?", [3]),
    ("", "Merkheft: Beispiel und Rezept", 10, "Beispiel Zeile für Zeile vorrechnen, Rest abdecken, Rezept rechts mitschreiben. Alles ins Merkheft.", [4]),
    ("", "Runde 1 ○", 7, "Übungsheft, Merkheft daneben aufgeschlagen.", [5, 6]),
    ("", "Runde 2 ◐", 8, "Mehr Blöcke in einer Aufgabe.", [7, 8]),
    ("", "Runde 3 ●", 7, "Jetzt mit Klammer. Wer fertig ist, geht gleich hierher.", [9, 10]),
    ("", "Fehler suchen", 2, "Der Klassiker: von links nach rechts gerechnet.", [11, 12]),
    ("", "Exit-Ticket", 3, "Ohne Hilfe.", [13, 14]),
]
assert sum(m for _, _, m, _, _ in SCHRITTE) == 45


def main():
    vb = [("Drucken", "Nichts."),
          ("Digital", "Folien-PDF in Notability: Mathe 7c – Woche 5 – 1 Rezept für gemischte Aufgaben.pdf (iCloud, 04 Rationale Zahlen)."),
          ("Voraussetzung", "Mal und Geteilt mit Vorzeichenregel sind eingeführt, die Minusklammer ist bekannt.")]
    bau_woche(HIER / NAME, "Woche 5, Stunde 1: Rezept für gemischte Aufgaben",
              "Klasse 7c, Mathematik, Woche 5 vor der KA 1, nach Multiplizieren und Dividieren (Verbinden der Rechenarten), eine Stunde",
              vb, SCHRITTE, FOLIEN,
              tafel=box("Tafelbild = Merkheft", MERK) + box("Falls ein zweites Beispiel nötig ist (ohne Klammer)", B1) + box("Falls Zeit: nur Minusklammer", B3),
              merkheft=box("Gemischte Aufgaben", HEFT(MERK)),
              loesungen=box("Blitzrunde", BLITZ_LF) + box("Runde 1 ○", ergebnisse(UEB_O)) + box("Runde 2 ◐", ergebnisse(UEB_M)) + box("Runde 3 ●", UEB_L_S) + box("Exit-Ticket", EXIT_L),
              extra_css=EXTRA_CSS)


if __name__ == "__main__":
    main()
