#!/usr/bin/env python3
"""Mathe 7c, Woche 7, Stunde 1: Verbindung der Rechenarten (Mo 02.11.2026, IF-Stunde, zweimal je eine halbe Klasse, je 45 Minuten).
Buch Schnittpunkt 7, Kapitel 8, S. 31 bis 33. Oskars Konzept: erst Klammer, dann Punkt vor Strich, dann jeden Block mit der
Vorzeichenregel, dann gleiche Zeichen zusammen (Vertauschungsgesetz). Aufgaben so leicht wie möglich, in Einzelteile zerlegt.
Gleiches Vorgehen wie baue_woche4_division.py: A4-Seiten, je Abschnitt eine Seite und direkt danach dieselbe Seite ausgefüllt;
Whiteboard-Einstieg als Querfolie; Merkheft-Bild mit Beispiel links, Rezept rechts und weiteren Beispielen; Übungsseiten mit
„Aufgabe:“ und „Für Schnelle:“, Buchaufgaben abgetippt. Das Verteilungsgesetz (Ausmultiplizieren) und die Rechenvorteile beim Malnehmen (Seite „Geschickt vertauschen“, S. 33 Nr. 7 rechts,
schon vorbereitet als seite_vertauschen und S33_7R) kommen erst in der nächsten Stunde.
Jede Lösung und jeder Zwischenschritt wird mit Python geprüft. Aufruf: python3 baue_woche7_rechenarten.py"""
import sys
from pathlib import Path
from ablage import ziel as rz_ziel, ordner as rz_ordner  # Ablage in Unterordner, siehe ablage.py

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parents[1]))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_woche7 import merkbild, wert, zahl, HEFT, UEB, P, box, EXTRA_CSS, LUECKE, LUECKE_LANG  # noqa: E402
from baue_woche4 import L, pruefe, spalten, block, auftrag, G  # noqa: E402
from baue_woche4_division import wb_seite  # noqa: E402

NAME = "Mathe 7c – Woche 7 – 1 Verbindung der Rechenarten"


def gleich(*zeilen):
    """Rechenweg: alle Zeilen müssen denselben Wert haben."""
    w = {round(wert(z), 9) for z in zeilen}
    assert len(w) == 1, (zeilen, w)
    return zeilen


# ================================================================ 1 Whiteboards
WB = [("Ergebnis", "(−7) · (−6)", "42", 42), ("Ergebnis", "36 : (−4)", "−9", -9), ("Nur das Vorzeichen", "(−2) · (−3) · (−5)", "−", -30),
      ("Ergebnis", "−9 + 4", "−5", -5), ("Ergebnis", "6 + 4 · 2", "14", 14)]

# ================================================================ 2 Was zuerst? und Merkheft
FRAGE = "12 − 3 · (−2)"
A_WEG = ("12 − 3 = 9", "9 · (−2) = −18")
assert wert("12 - 3") == 9 and wert("9*(-2)") == -18
B_WEG = gleich(FRAGE, f"12 {P('− 3 · (−2)')}", "12 + 6", "18")[1:]    # ab der markierten Zeile, sonst steht die Aufgabe doppelt da

SCHRITTE = ["Klammer? Innen zuerst.", "Punkt vor Strich: Mal- und Geteilt-Blöcke markieren. Das Zeichen davor gehört dazu.",
            "Jeden Block rechnen: gleiche Zeichen +, verschiedene −.", "Strich: gleiche Zeichen zusammen (Vertauschungsgesetz).", "Ausrechnen."]
MERK = merkbild("Verbindung der Rechenarten", [
    (1, '20 − 3 · <span class="rot">(2 − 6)</span> + 18 : (−3)'),
    (None, '= 20 − 3 · <span class="rot">(−4)</span> + 18 : (−3)'),
    (2, f'= 20 {P("− 3 · (−4)")} {P("+ 18 : (−3)")}'),
    (3, '= 20 <span class="rot">+ 12</span> <span class="rot">− 6</span>'),
    (4, '= <span class="gelb">20 + 12</span> − 6'),
    (None, '= 32 − 6'),
    (5, '= <b>26</b>'),
], SCHRITTE, weitere=[
    ("9 − 4 · (−2)", '9 <span class="rot">+ 8</span> = 17', 17),
    ("−5 + 24 : (−6)", '−5 <span class="rot">− 4</span> = −9', -9),
    ("3 · (−4) − 10", '<span class="rot">−12</span> − 10 = −22', -22),
    ("−7 − 2,5 · (−2)", '−7 <span class="rot">+ 5</span> = −2', -2),
    ("30 : (−5) + 2 · (−3)", '<span class="rot">−6</span> <span class="rot">− 6</span> = −12', -12),
    ("(1 − 5) · 3 + 4", '<span class="rot">(−4)</span> · 3 + 4 = −12 + 4 = −8', -8)])


def seite_zuerst(l):
    zeile = lambda name, weg, ok: (f'<tr><td class="u-d">{name}</td><td>{"<br>".join(weg)}</td>'
                                   f'<td class="u-p">richtig?</td><td>{L(ok) if l else LUECKE}</td></tr>')
    tab = (f'<table class="umkehr" style="font-size:{G + 2}px">'
           + zeile("Rechnung A", A_WEG, "✗") + zeile("Rechnung B", ("3 · (−2) = −6", "12 − (−6) = 18"), "✓") + "</table>")
    assert wert("3*(-2)") == -6 and wert("12-(-6)") == 18
    kopf = (f'<div class="ausdruck" style="font-size:40px;margin:6px 0 14px">{FRAGE}</div>'
            + block("Zwei rechnen dieselbe Aufgabe. Wer hat recht?", tab))
    if l:
        return (kopf + f'<p style="font-size:22px">B: Punkt vor Strich, zuerst der Block: {" = ".join(B_WEG)}</p>' + HEFT(MERK))
    return kopf


# ================================================================ 3 Übung 1 ○ (eigene Aufgaben, so leicht wie möglich)
UEB1 = pruefe([("10 − 2 · 3", 4), ("−8 + 3 · (−2)", -14), ("15 : (−3) + 9", 4), ("7 − 4 · (−2)", 15),
               ("−12 : 4 − 6", -9), ("2 · (−6) + 5 · 3", 3), ("4 · (5 − 8) + 10", -2), ("−20 + (3 − 7) · (−3)", -8)])


def seite_uebung1(l):
    return (auftrag("Übungsheft, Aufgaben a) bis h). Jeden Block einzeln rechnen.", "Gleich weiter mit Buch S. 33 Nr. 7 (links).")
            + UEB(block("○ Rechne nach dem Rezept.", spalten(UEB1, l, gross=G + 2))))


# ================================================================ 4 Geschickt vertauschen
VT = [gleich("(−4) · 17 · (−25)", "(−4) · (−25) · 17", "100 · 17", "1700"),
      gleich("(−2) · 3,7 · 5", "(−2) · 5 · 3,7", "(−10) · 3,7", "−37"),
      gleich("−12 + 30 − 8", "−12 − 8 + 30", "−20 + 30", "10")]


def seite_vertauschen(l):
    zeilen = "".join(f'<li>{w[0]} = {L(" = ".join(w[1:])) if l else LUECKE_LANG}</li>' for w in VT)
    kopf = block("Welche zwei Zahlen rechnest du zuerst? Rechne geschickt.",
                 f'<ol type="a" class="ex" style="font-size:{G + 4}px;line-height:2.1">{zeilen}</ol>')
    return kopf + HEFT(MERK_VT) if l else kopf


MERK_VT = ('<div class="merk" style="font-size:20px">Vertauschungsgesetz: Die Zahlen dürfen die Plätze tauschen. Das Vorzeichen wandert mit.</div>'
           '<div class="ausdruck" style="font-size:20px;white-space:nowrap">Gute Partner: 2 · 5 = 10; 4 · 25 = 100; 2,5 · 4 = 10; 0,5 · 2 = 1</div>'
           f'<div class="ausdruck">{" = ".join(VT[0])}</div><div class="ausdruck">{" = ".join(VT[2])}</div>')
assert wert("2*5") == 10 and wert("4*25") == 100 and wert("2.5*4") == 10 and wert("0.5*2") == 1


# ================================================================ 5 Übung 2 ◐: Buch S. 33 Nr. 7 links und rechts
S33_7L = [gleich("(−22) + 2,5 · (−10)", "−22 − 25", "−47"),
          gleich("(−60) : (−12) + 12", "5 + 12", "17"),
          gleich("−25 − 88 : (−11) + 13", "−25 + 8 + 13", "−4"),
          gleich("75 − (15 − 65) · (−2) + 25", "75 − (−50) · (−2) + 25", "75 − 100 + 25", "0"),
          gleich("120 − (144 : (−12) + 24) · 12", "120 − (−12 + 24) · 12", "120 − 12 · 12", "120 − 144", "−24")]
S33_7R = [gleich("13 · (−5) · 20", "13 · (−100)", "−1300"),
          gleich("(−2) · 1,2 · 0,5", "(−2) · 0,5 · 1,2", "(−1) · 1,2", "−1,2"),
          gleich("(−4) · 7,5 · (−25)", "(−4) · (−25) · 7,5", "100 · 7,5", "750"),
          gleich("(−1,25) · (−0,7) · 8", "(−1,25) · 8 · (−0,7)", "(−10) · (−0,7)", "7"),
          gleich("(−50) · 30 · (−25) · (−2) · 4", "(−50) · (−2) · (−25) · 4 · 30", "100 · (−100) · 30", "−300000")]
ERG = lambda w: zahl(wert(w[-1])).replace("300000", "300 000")


def seite_uebung2(l):
    return (auftrag("Übungsheft, Buch S. 33 Nr. 7 (links).",
                    "Buch S. 33 Nr. 11 (links): Setze eine Klammer so, dass das Ergebnis stimmt.")
            + UEB(block("◐ Buch S. 33 Nr. 7 (links): Achte auf Punkt vor Strich.", spalten([(w[0], ERG(w)) for w in S33_7L], l, gross=G + 2))))


# Für Schnelle (nur Lösungen): S. 33 Nr. 11 links, Klammer so setzen, dass das Ergebnis stimmt
S33_11L = [("(−5) · 3 − 9 = 30", "(−5) · (3 − 9)", 30), ("−28 − 21 : 7 = −7", "(−28 − 21) : 7", -7),
           ("(−2) · 8 − 4 · 5 = −100", "((−2) · 8 − 4) · 5", -100), ("32 − 6 · (−5) + 10 = 2", "32 − 6 · ((−5) + 10)", 2)]
for _a, _k, _e in S33_11L:
    assert wert(_k) == _e and wert(_a.split(" = ")[0]) != _e, _k

# ================================================================ 6 Weitere Aufgaben (Puffer): S. 33 Nr. 8 links und rechts
S33_8L = [("(10 − 3) · (−4) = 22", "10 − 3 · (−4)", 22), ("(12 − 16) : (−4) = 16", "12 − 16 : (−4)", 16),
          ("5 − (24 : 6 + 2) = 2", "5 − 24 : (6 + 2)", 2), ("3 − (54 : (−9)) − 18 = 5", "3 − 54 : ((−9) − 18)", 5)]
for _a, _k, _e in S33_8L:
    assert wert(_k) == _e and wert(_a.split(" = ")[0]) != _e, _k
S33_8R = [gleich("2,5 · 3 − 7,5 : 1,5 + (−0,5) · 3", "7,5 − 5 − 1,5", "1"),
          gleich("4 · (2,8 − 4,2) − (2,2 − 9,8)", "4 · (−1,4) − (−7,6)", "−5,6 + 7,6", "2"),
          gleich("5 · ((−1,2 + 0,7) − (−2,8 + 2,1)) + 2", "5 · (−0,5 + 0,7) + 2", "5 · 0,2 + 2", "3"),
          gleich("6,5 + 2,5 : (4,8 − 0,5 · 7,2 − 2,2)", "6,5 + 2,5 : (−1)", "6,5 − 2,5", "4")]


def seite_rest(l):
    liste = "".join(f'<li>{L(k) + " = " + a.split(" = ")[1] if l else a}</li>' for a, k, _ in S33_8L)
    return (auftrag("Übungsheft, Buch S. 33 Nr. 8 (links): Die Klammer sitzt falsch. Schreibe die Aufgabe richtig ab.",
                    "Buch S. 33 Nr. 8 (rechts): Die Ergebnisse sind 1, 2, 3 und 4.")
            + UEB(block("◐ Buch S. 33 Nr. 8 (links): Korrigiere die Klammer, damit das Ergebnis stimmt.",
                        f'<ol type="a" class="ex" style="font-size:{G + 2}px;line-height:2">{liste}</ol>')
                  + block("● Für Schnelle: Buch S. 33 Nr. 8 (rechts)", spalten([(w[0], ERG(w)) for w in S33_8R], l, gross=G))))


# ================================================================ Stunde
SEITEN = [("Whiteboards", wb_seite(WB)), ("2 Was zuerst?", seite_zuerst), ("3 Übung 1", seite_uebung1),
          ("4 Übung 2", seite_uebung2), ("5 Weitere Aufgaben", seite_rest)]
# Einfach schlägt komplex (Oskar, 01.11.2026): Die Seite „Geschickt vertauschen“ und Nr. 7 rechts (Rechenvorteile beim Malnehmen)
# kommen in die nächste Stunde; das Vertauschungsgesetz steht hier nur im Rezept-Schritt 4.
FOLIEN = [x for t, f in SEITEN for x in ((t, f(False)), (f"{t}: ausgefüllt", f(True)))]
QUER = {"Whiteboards", "Whiteboards: ausgefüllt"}

SCHRITTE_V = [
    ("", "Whiteboards: Mal, Geteilt, Plus", 5, "Querfolie, die anderen mit dem Pflaster abdecken. Karte 5 zeigt, wer schon Punkt vor Strich kann.", [1, 2]),
    ("", "Was zuerst?", 4, "Rechnung A und B, Hände hoch: Wer hat recht? Sagen: Mal und Geteilt binden stärker, wie ein Block.", [3]),
    ("", "Merkheft: Verbindung der Rechenarten", 13, "Beispiel Zeile für Zeile, Rest abdecken. Sagen: Das Zeichen vor dem Block gehört zum Block. Bei Schritt 4: Das ist das Vertauschungsgesetz, kennt ihr schon.", [4]),
    ("", "Übung 1 ○", 12, "Acht leichte Aufgaben, Merkheft offen. Herumgehen, Blöcke markieren lassen. Dann besprechen.", [5, 6]),
    ("", "Übung 2 ◐", 9, "Buch S. 33 Nr. 7 links. Schnelle: Nr. 11 links.", [7, 8]),
    ("", "Puffer", 2, "Nur wenn Zeit bleibt: S. 33 Nr. 8. Sonst Lösungen von Übung 2 zeigen.", [9, 10]),
]
assert sum(m for _, _, m, _, _ in SCHRITTE_V) == 45

EXTRA = EXTRA_CSS + "<style>.weitere{grid-template-columns:1fr}</style>"   # weitere Beispiele sind lang: eine Spalte, sonst laufen sie ineinander


def main():
    loes = "".join(box(t.replace(": ausgefüllt", ""), h) for t, h in FOLIEN if t.endswith("ausgefüllt"))
    wege = lambda ws: "".join(f'<div class="ausdruck" style="font-size:20px">{"abcde"[i]}) {" = ".join(w[:-1])} = {L(ERG(w))}</div>' for i, w in enumerate(ws))
    loes += box("Rechenwege S. 33 Nr. 7 (links)", wege(S33_7L))
    loes += box("Für Schnelle: S. 33 Nr. 11 (links)", "".join(f'<div class="ausdruck" style="font-size:20px">{"abcd"[i]}) {L(k)} = {zahl(e)}</div>'
                                                             for i, (_, k, e) in enumerate(S33_11L)))
    loes += box("Für Schnelle: Rechenwege S. 33 Nr. 8 (rechts)", wege(S33_8R))
    vb = [("Drucken", "Nichts."), ("Sonst", "Mini-Whiteboards und Stifte, Buch."),
          ("Digital", f"Folien-PDF in Notability: {NAME}.pdf (iCloud, 04 Rationale Zahlen)."),
          ("Zweimal", "Dieselbe Stunde in der 5. und 6. Stunde mit je einer halben Klasse. Die KA-Verbesserung kommt später.")]
    bau_woche(rz_ziel(f"{NAME}.html"), "Woche 7, Stunde 1: Verbindung der Rechenarten",
              "Klasse 7c, Mathematik, Mo 02.11.2026, IF-Stunde mit halber Klasse (zweimal), Buch S. 31 bis 33",
              vb, SCHRITTE_V, FOLIEN,
              tafel=box("Was zuerst? (ausgefüllt mit Merkheft)", seite_zuerst(True)),
              merkheft=box("Verbindung der Rechenarten", HEFT(MERK)),
              loesungen=loes, extra_css=EXTRA, verlauf="Die Stunde")


if __name__ == "__main__":
    main()
