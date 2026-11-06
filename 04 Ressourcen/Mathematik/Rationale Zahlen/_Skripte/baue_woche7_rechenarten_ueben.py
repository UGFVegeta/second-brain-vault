#!/usr/bin/env python3
"""Mathe 7c, Woche 7, Stunde 2: Verbindung der Rechenarten üben (Di 03.11.2026, 1./2. Stunde; 60 Minuten Stoff, danach 30 Minuten KA-Rückgabe und Verbesserung, die hier nicht vorbereitet wird).
Abschluss der Einheit Rationale Zahlen. Oskars Konzept (nicht verändern): 1. Whiteboard-Wiederholung, mindestens fünf Aufgaben,
gleiches Format wie gestern; 2. zwei lange Beispielaufgaben mit mehreren Blöcken und Klammer gemeinsam an der Tafel, Rezept
anwenden; 3. Lerntheke mit zwei eigenen A4-Blättern (○ ◐ ●), Lösung = dasselbe Blatt ausgefüllt; 4. Hausaufgabe zwei
Buchaufgaben (Schnittpunkt 7, S. 37 Nr. 19 und Nr. 23, abgetippt).
Erste Mathe-Stunde mit Seitenleiste und Countdown-Uhr (bau_woche(..., leiste=...), Bausteine aus Lernwissenschaft & Pädagogik).
Jede Lösung und jeder Zwischenschritt wird mit Python geprüft. Aufruf: python3 baue_woche7_rechenarten_ueben.py"""
import sys
from pathlib import Path
from ablage import ziel as rz_ziel, ordner as rz_ordner  # Ablage in Unterordner, siehe ablage.py

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parents[1]))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_woche7 import merkbild, wert, zahl, HEFT, UEB, P, box, rezept_box, EXTRA_CSS  # noqa: E402
from baue_woche4 import L, block  # noqa: E402
from baue_woche4_division import wb_seite  # noqa: E402
from baue_uebung_ka1_7c import KREIS  # noqa: E402
from baue_woche7_rechenarten import MERK, SCHRITTE, S33_7L, ERG, gleich  # noqa: E402

NAME = "Mathe 7c – Woche 7 – 2 Verbindung der Rechenarten üben"

# ================================================================ 1 Whiteboards (zwei Runden mit je fünf Karten)
WB1 = [("Ergebnis", "−8 · 7", "−56", -56), ("Ergebnis", "−45 : (−9)", "5", 5), ("Nur das Vorzeichen", "(−3) · 4 · (−2) · (−1)", "−", -24),
       ("Ergebnis", "−6 − 9", "−15", -15), ("Ergebnis", "5 − 3 · 4", "−7", -7)]
# Runde 2 zerlegt eine lange Aufgabe in kleine Teile (Karten 1 bis 4), Karte 5 ist eine neue Aufgabe
WB2 = [("Was rechnest du zuerst?", "18 − 3 · (2 − 6)", "(2 − 6)", None), ("Ergebnis", "2 − 6", "−4", -4),
       ("Ergebnis", "−3 · (−4)", "12", 12), ("Ergebnis", "18 − 3 · (2 − 6)", "30", 30), ("Ergebnis", "−20 : 5 − 2 · (−3)", "2", 2)]
assert wert("18 - 3*(-4)") == 18 + 12

# ================================================================ 2 Zwei lange Beispiele an der Tafel
BSP1 = [(1, '−15 + 4 · <span class="rot">(3 − 8)</span> − 36 : (−4)'),
        (None, '= −15 + 4 · <span class="rot">(−5)</span> − 36 : (−4)'),
        (2, f'= −15 {P("+ 4 · (−5)")} {P("− 36 : (−4)")}'),
        (3, '= −15 <span class="rot">− 20</span> <span class="rot">+ 9</span>'),
        (4, '= <span class="gelb">−15 − 20</span> + 9'),
        (None, '= −35 + 9'),
        (5, '= <b>−26</b>')]
BSP2 = [(1, '2 · (−7) − <span class="rot">(18 − 4 · 6)</span> + 30 : (−6)'),
        (None, '= 2 · (−7) − (18 <span class="rot">− 24</span>) + 30 : (−6)'),
        (None, '= 2 · (−7) − <span class="rot">(−6)</span> + 30 : (−6)'),
        (2, f'= {P("2 · (−7)")} {P("− (−6)")} {P("+ 30 : (−6)")}'),
        (3, '= <span class="rot">−14</span> <span class="rot">+ 6</span> <span class="rot">− 5</span>'),
        (4, '= <span class="gelb">−14 − 5</span> + 6'),
        (None, '= −19 + 6'),
        (5, '= <b>−13</b>')]


def seite_beispiel(bsp, mit_rezept=True):
    """Ganze Seite kariert (Oskar schreibt in Notability direkt darauf). Das Rezept steht nur bei Beispiel 1."""
    def seite(l):
        h = merkbild("Rezept", bsp if l else bsp[:1], SCHRITTE)   # der Titel ist die Überschrift des Rezeptkastens
        if not mit_rezept:
            h = h.replace(rezept_box("Rezept", SCHRITTE), "").replace('<div class="mb">', '<div class="mb" style="grid-template-columns:1fr">', 1)
            assert 'grid-template-columns:1fr' in h      # ohne Rezept volle Breite, sonst bricht die Aufgabe um
        return f'<div class="karoseite">{UEB(h)}</div>'
    return seite


# ================================================================ 3 Lerntheke: zwei A4-Blätter, gerechnet wird in den Kästchen auf dem Blatt
# (Aufgabe, [Rechenweg-Schritte]); jeder Schritt wird gegen die Aufgabe geprüft, der letzte ist das Ergebnis.
# Unter jeder Aufgabe ein Kästchenfeld (karo mm hoch): im Blatt leer, in der Lösung der Rechenweg in Magenta (dasselbe Blatt ausgefüllt).
# Oskar 02.11.: Nr. 1 braucht wenig Platz (eine Zeile = 2 Kästchen), Nr. 2 und Nr. 3 mindestens zwei Zeilen.
def nr(stufe, text, aufgaben, spalten, pro_zeile, zeilen, karo):
    for a, weg in aufgaben:
        gleich(a, *weg)
        assert -(-len(weg) // pro_zeile) <= zeilen, (a, "zu wenig Platz für den Rechenweg")
    assert karo / zeilen >= 5, "mindestens ein Kästchen pro Lösungszeile"
    return dict(stufe=stufe, text=text, aufgaben=aufgaben, spalten=spalten, pro=pro_zeile, zeilen=zeilen, karo=karo)


BLATT1 = ("Punkt vor Strich", [
    nr(0, "Markiere die Blöcke. Rechne dann.", [
        ("12 − 4 · 5", ["12 − 20", "−8"]), ("−9 + 18 : 3", ["−9 + 6", "−3"]), ("7 · (−2) + 20", ["−14 + 20", "6"]),
        ("−30 : 6 − 4", ["−5 − 4", "−9"]), ("16 − 3 · (−4)", ["16 + 12", "28"]), ("−5 − 24 : (−8)", ["−5 + 3", "−2"]),
        ("20 − 6 · 3", ["20 − 18", "2"]), ("−14 + 21 : 7", ["−14 + 3", "−11"]), ("9 · (−3) + 30", ["−27 + 30", "3"]),
        ("−48 : 8 − 7", ["−6 − 7", "−13"]), ("11 − 5 · (−2)", ["11 + 10", "21"]), ("−3 − 36 : (−9)", ["−3 + 4", "1"])], 4, 2, 1, 10),
    nr(1, "Zwei Blöcke. Rechne jeden Block einzeln.", [
        ("3 · (−5) + 8 · 2", ["−15 + 16", "1"]), ("−28 : 7 − 6 · (−3)", ["−4 + 18", "14"]),
        ("40 : (−8) − 2 · 9", ["−5 − 18", "−23"]), ("−6 · 4 + 45 : (−9)", ["−24 − 5", "−29"]),
        ("2 · (−9) + 7 · 3", ["−18 + 21", "3"]), ("−35 : 5 − 4 · (−4)", ["−7 + 16", "9"]),
        ("56 : (−7) − 3 · 6", ["−8 − 18", "−26"]), ("−5 · 5 + 64 : (−8)", ["−25 − 8", "−33"])], 2, 2, 1, 20),
    nr(2, "Drei Blöcke, auch mit Kommazahlen.", [
        ("0,5 · (−8) − 12 + 3 · (−2,5)", ["−4 − 12 − 7,5", "−16 − 7,5", "−23,5"]),
        ("−2,4 : 0,6 + 1,5 · 4 − 10", ["−4 + 6 − 10", "−4 − 10 + 6", "−14 + 6", "−8"]),
        ("1,5 · (−6) + 20 − 4 · 2,5", ["−9 + 20 − 10", "−9 − 10 + 20", "−19 + 20", "1"]),
        ("−7,2 : 0,9 − 3 + 0,5 · (−6)", ["−8 − 3 − 3", "−14"])], 2, 2, 2, 20),
])
BLATT2 = ("Mit Klammern", [
    nr(0, "Rechne zuerst die Klammer.", [
        ("(6 − 10) · 3", ["(−4) · 3", "−12"]), ("4 · (−2 + 7)", ["4 · 5", "20"]), ("(−18 + 6) : 4", ["(−12) : 4", "−3"]),
        ("20 − (3 − 9)", ["20 − (−6)", "26"]), ("−5 · (8 − 11)", ["−5 · (−3)", "15"]), ("(−7 − 8) : (−5)", ["(−15) : (−5)", "3"]),
        ("(4 − 9) · 2", ["(−5) · 2", "−10"]), ("6 · (−3 + 8)", ["6 · 5", "30"]), ("(−20 + 4) : 8", ["(−16) : 8", "−2"]),
        ("15 − (2 − 10)", ["15 − (−8)", "23"]), ("−2 · (5 − 12)", ["−2 · (−7)", "14"]), ("(−9 − 3) : (−4)", ["(−12) : (−4)", "3"])], 4, 2, 1, 10),
    nr(1, "Erst die Klammer, dann Punkt vor Strich.", [
        ("10 + 2 · (5 − 9)", ["10 + 2 · (−4)", "10 − 8", "2"]), ("−12 − (4 − 10) · 3", ["−12 − (−6) · 3", "−12 + 18", "6"]),
        ("30 : (−2 − 4) + 7", ["30 : (−6) + 7", "−5 + 7", "2"]), ("−4 · (3 − 7) − 20 : 5", ["−4 · (−4) − 20 : 5", "16 − 4", "12"]),
        ("8 + 3 · (2 − 6)", ["8 + 3 · (−4)", "8 − 12", "−4"]), ("−10 − (3 − 8) · 4", ["−10 − (−5) · 4", "−10 + 20", "10"]),
        ("24 : (−1 − 5) + 9", ["24 : (−6) + 9", "−4 + 9", "5"]), ("−3 · (2 − 9) − 18 : 6", ["−3 · (−7) − 18 : 6", "21 − 3", "18"])], 2, 2, 2, 20),
    nr(2, "Auch in der Klammer gilt Punkt vor Strich.", [
        ("25 − (2 + 3 · (−4)) · 2", ["25 − (2 − 12) · 2", "25 − (−10) · 2", "25 + 20", "45"]),
        ("−3 · (12 − 2 · 8) + 48 : (−6 − 2)", ["−3 · (12 − 16) + 48 : (−8)", "−3 · (−4) + 48 : (−8)", "12 − 6", "6"]),
        ("30 − (4 + 2 · (−7)) · 3", ["30 − (4 − 14) · 3", "30 − (−10) · 3", "30 + 30", "60"]),
        ("−2 · (20 − 3 · 9) + 36 : (−2 − 7)", ["−2 · (20 − 27) + 36 : (−9)", "−2 · (−7) + 36 : (−9)", "14 − 4", "10"])], 2, 1, 4, 20),
])


def blatt(b):
    titel, nummern = b

    def seite(l):
        h = ""
        for k, n in enumerate(nummern, 1):
            zellen = ""
            for i, (a, weg) in enumerate(n["aufgaben"]):
                teile = [weg[j:j + n["pro"]] for j in range(0, len(weg), n["pro"])]
                hz = min(10, n["karo"] / n["zeilen"])     # Zeilenhöhe der Lösung in mm, passend zum 5-mm-Raster
                rw = "".join(f'<div class="rw{" end" if t is teile[-1] else ""}" style="line-height:{hz - 0.15:g}mm{";font-size:14px" if hz < 8 else ""}">'
                             f'= {" = ".join(t)}</div>' for t in teile) if l else ""
                zellen += (f'<div class="lt-z"><div class="lt-a">{"abcdefghijkl"[i]}) &nbsp;{a}</div>'
                           f'<div class="karo" style="height:{n["karo"]}mm">{rw}</div></div>')
            h += (f'<div class="lt-nr"><b>Nr. {k}</b>{KREIS[n["stufe"]]}<span>{n["text"]}</span></div>'
                  f'<div class="lt-raster" style="grid-template-columns:repeat({n["spalten"]},1fr)">{zellen}</div>')
        return h + (f'<div class="lt-leg">{KREIS[0]} leicht &nbsp; {KREIS[1]} mittel &nbsp; {KREIS[2]} schwer'
                    f'&nbsp;&nbsp; Rechne in den Kästchen. Die Lösung liegt vorne.</div>')
    return seite


THEKE = ('<ol class="ex theke" style="font-size:24px;line-height:1.5"><li>Nimm Blatt 1. Rechne in den Kästchen auf dem Blatt.</li>'
         "<li>Markiere zuerst die Blöcke. Dann Schritt für Schritt.</li>"
         "<li>Fertig? Hol dir die Lösung vorne und kontrolliere. Fehler mit Farbe verbessern.</li>"
         "<li>Dann Blatt 2.</li></ol>"
         f'<p style="font-size:20px">{KREIS[0]} leicht &nbsp; {KREIS[1]} mittel &nbsp; {KREIS[2]} schwer: Du musst nicht alles schaffen.</p>'
         + rezept_box("Rezept", SCHRITTE))

# ================================================================ 4 Hausaufgabe: Buch S. 37 Nr. 19 und Nr. 23 (abgetippt)
S37_19 = [gleich("−6 − 55 : 11", "−6 − 5", "−11"),
          gleich("−10 − 25 : (−5) + 4", "−10 + 5 + 4", "−1"),
          gleich("−12 + 3 · (−7) − 18", "−12 − 21 − 18", "−51"),
          gleich("(−0,5) − 8 · (−0,2) + 3,3", "−0,5 + 1,6 + 3,3", "4,4"),
          gleich("19 + 27,5 : (−2,5) − 12 · 1,5", "19 − 11 − 18", "−10")]
S37_23 = [gleich("−4 + (10 − 72 : 6)", "−4 + (10 − 12)", "−4 + (−2)", "−6"),
          gleich("−100 : (44 − 27 · 2)", "−100 : (44 − 54)", "−100 : (−10)", "10"),
          gleich("−5 − (45 + 24 · (−2))", "−5 − (45 − 48)", "−5 − (−3)", "−2"),
          gleich("−1 − ((−78 + 63) : (−5))", "−1 − ((−15) : (−5))", "−1 − 3", "−4")]


def seite_ha(l):
    def liste(ws):
        if l:
            return "".join(f'<li>{w[0]} = {L(" = ".join(w[1:]))}</li>' for w in ws)
        return "".join(f"<li>{w[0]}</li>" for w in ws)
    return (block("Hausaufgabe ins Übungsheft: Buch S. 37 Nr. 19 und Nr. 23", "")
            + UEB(block("○ Buch S. 37 Nr. 19: Achte auf Punkt vor Strich.", f'<ol type="a" class="ex" style="font-size:21px;line-height:1.9">{liste(S37_19)}</ol>')
                  + block("◐ Buch S. 37 Nr. 23: Achte auf die Klammer. Berechne.", f'<ol type="a" class="ex" style="font-size:21px;line-height:1.9">{liste(S37_23)}</ol>')))


# Reserve: Hausaufgabe von gestern (Buch S. 33 Nr. 7 links), nur ausgefüllt
def seite_ha_gestern():
    return UEB(block("Buch S. 33 Nr. 7 (links)", "".join(
        f'<div class="ausdruck" style="font-size:22px">{"abcde"[i]}) {" = ".join(w[:-1])} = {L(ERG(w))}</div>' for i, w in enumerate(S33_7L))))


# ================================================================ Stunde
SEITEN = [("Whiteboards 1", wb_seite(WB1)), ("Whiteboards 2", wb_seite(WB2)),
          ("Beispiel 1", seite_beispiel(BSP1)), ("Beispiel 2", seite_beispiel(BSP2, mit_rezept=False))]
FOLIEN = [x for t, f in SEITEN for x in ((t, f(False)), (f"{t}: ausgefüllt", f(True)))]
B1, B2 = blatt(BLATT1), blatt(BLATT2)
FOLIEN += [("Lerntheke", THEKE),
           (f"Lerntheke Blatt 1: {BLATT1[0]}", B1(False)), (f"Lerntheke Blatt 1: {BLATT1[0]} – Lösung", B1(True)),
           (f"Lerntheke Blatt 2: {BLATT2[0]}", B2(False)), (f"Lerntheke Blatt 2: {BLATT2[0]} – Lösung", B2(True)),
           ("Hausaufgabe", seite_ha(False)), ("Hausaufgabe: ausgefüllt", seite_ha(True)),
           ("Hausaufgabe von gestern: ausgefüllt", seite_ha_gestern())]
# Druck (vom Export gebaut): die beiden Lerntheke-Blätter und ihre Lösungen, je eine A4-Seite
DRUCK_BLAETTER = [(t, h) for t, h in FOLIEN if t.startswith("Lerntheke Blatt") and not t.endswith("Lösung")]
DRUCK_LOESUNGEN = [(t, h) for t, h in FOLIEN if t.startswith("Lerntheke Blatt") and t.endswith("Lösung")]
assert len(DRUCK_BLAETTER) == len(DRUCK_LOESUNGEN) == 2
QUER = {"Whiteboards 1", "Whiteboards 1: ausgefüllt", "Whiteboards 2", "Whiteboards 2: ausgefüllt"}
LEISTE = ([("Wiederholung", "Whiteboards 1", None)] * 2 + [("Wiederholung", "Whiteboards 2", None)] * 2
          + [("Lange Aufgaben", "Beispiel 1", None)] * 2 + [("Lange Aufgaben", "Beispiel 2", None)] * 2
          + [("Lerntheke", "So geht's", 25)] + [("Lerntheke", "Blatt 1", None)] * 2 + [("Lerntheke", "Blatt 2", None)] * 2
          + [("Zum Schluss", "Hausaufgabe", None)] * 2 + [("Reserve", "HA von gestern", None)])

SCHRITTE_V = [
    ("", "Whiteboards 1: Grundlagen", 5, "Querfolie, die anderen Karten abdecken. Karte 5 zeigt, wer Punkt vor Strich schon sicher kann.", [1, 2]),
    ("", "Whiteboards 2: Eine Aufgabe in Teilen", 5, "Karte 1 bis 4 sind dieselbe Aufgabe in kleinen Schritten. Sagen: So zerlegt ihr jede lange Aufgabe.", [3, 4]),
    ("", "Beispiel 1 an der Tafel", 7, "Gemeinsam nach dem Rezept, Schüler sagen jeden Schritt an. Erst Schritt 1 und 2 (Klammer, Blöcke), dann rechnen. Ins Übungsheft.", [5, 6]),
    ("", "Beispiel 2 an der Tafel", 8, "In der Klammer gilt auch Punkt vor Strich. Das Minus vor der Klammer ist ein eigener Block. Ins Übungsheft.", [7, 8]),
    ("", "Lerntheke", 27, "Blatt 1 und 2 liegen vorne, je zwei Lösungsblätter daneben. Rechnen in den Kästchen auf dem Blatt, selbst kontrollieren. Uhr 25 Minuten. Wer nicht fertig wird: Rest als Hausaufgabe (statt oder zusätzlich zum Buch).", [9, 10, 12]),
    ("", "Hausaufgabe", 3, "Buch S. 37 Nr. 19 und Nr. 23 zeigen und aufschreiben lassen. Blätter ins Heft einkleben.", [14]),
    ("", "Puffer", 5, "Fragen zur Einheit sammeln. Bei Bedarf HA von gestern (S. 33 Nr. 7) zeigen: Reserve-Folie.", [16]),
    ("", "Klassenarbeit: Rückgabe und Verbesserung", 30, "Nicht hier vorbereitet.", []),
]
assert sum(m for _, _, m, _, _ in SCHRITTE_V[:-1]) == 60 and sum(m for _, _, m, _, _ in SCHRITTE_V) == 90

EXTRA = EXTRA_CSS + """<style>.weitere{grid-template-columns:1fr}
.lt-nr{display:flex;align-items:center;gap:9px;border:1px solid #9a9a9a;padding:3px 9px;margin:8px 0 4px;font-size:16px}.lt-nr b{font-size:17px;white-space:nowrap}
.lt-raster{display:grid;gap:1px 16px}.lt-z{min-width:0}
.lt-a{font-size:18px;font-weight:700;white-space:nowrap;line-height:6.5mm}
.karoseite{height:255mm;background-color:#fff;background-image:linear-gradient(#cbd4de 1px,transparent 1px),linear-gradient(90deg,#cbd4de 1px,transparent 1px);background-size:5mm 5mm;padding:2mm}
.karo{background-color:#fff;background-image:linear-gradient(#cbd4de 1px,transparent 1px),linear-gradient(90deg,#cbd4de 1px,transparent 1px);background-size:5mm 5mm;border:1px solid #cbd4de;margin-bottom:1mm;overflow:hidden}
.theke li{white-space:normal}
.karo .rw{color:#E6007E;font-weight:600;font-size:16px;padding-left:2mm;white-space:nowrap}.karo .rw.end{font-weight:800}
.lt-leg{font-size:14px;color:#444;margin-top:14px}.kreis{width:1.2em;height:1.2em;vertical-align:-.25em}
.lt-nr .kreis{width:1.25em;height:1.25em}
</style>"""


def main():
    loes = "".join(box(t.replace(": ausgefüllt", ""), f'<div class="seite-vorschau">{h}</div>') for t, h in FOLIEN
                   if t.endswith("ausgefüllt") or t.endswith("Lösung"))
    vb = [("Drucken", "Lerntheke Blatt 1 und Blatt 2 je einmal pro Schüler (A4 hoch, einseitig). Lösung Blatt 1 und Lösung Blatt 2 je zweimal, vorne auslegen."),
          ("Sonst", "Mini-Whiteboards und Stifte, Buch für die Hausaufgabe, Kleber zum Einkleben der Blätter."),
          ("Digital", f"Folien-PDF in Notability: {NAME}.pdf (iCloud, 04 Rationale Zahlen), kommt nach deiner Freigabe."),
          ("Tafel", "Beispiel 1 und 2 entstehen an der Tafel. Das Zielbild steht im Tab Tafelbild."),
          ("Einheit", "Letzte Stunde zu den rationalen Zahlen. Das Merkheft hat keinen neuen Eintrag, das Rezept von gestern liegt offen daneben.")]
    tafel = box("Beispiel 1 (ausgefüllt)", seite_beispiel(BSP1)(True)) + box("Beispiel 2 (ausgefüllt)", seite_beispiel(BSP2, mit_rezept=False)(True))
    merk = box("Kein neuer Eintrag. Zum Nachschauen: Verbindung der Rechenarten (von gestern)", HEFT(MERK))
    bau_woche(rz_ziel(f"{NAME}.html"), "Woche 7, Stunde 2: Verbindung der Rechenarten üben",
              "Klasse 7c, Mathematik, Di 03.11.2026, 1. und 2. Stunde (60 Minuten Stoff, danach 30 Minuten Klassenarbeit), Abschluss Rationale Zahlen",
              vb, SCHRITTE_V, FOLIEN, tafel=tafel, merkheft=merk, loesungen=loes, extra_css=EXTRA, verlauf="Die Stunde",
              leiste=LEISTE, quer=QUER)


if __name__ == "__main__":
    main()
