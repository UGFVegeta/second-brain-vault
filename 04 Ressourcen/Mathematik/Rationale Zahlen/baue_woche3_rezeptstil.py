#!/usr/bin/env python3
"""Vergleichsentwurf: Mathe 7c, Woche 3, Stunde 2 (Di 29.09.2026, Doppelstunde: Rechengesetze, Minusklammer) im Rezept-Stil.
Nicht für den Unterricht, nur zum Vergleich mit der echten Stunde (baue_woche3.py, Stunde 2). Die echte Stunde bleibt unverändert.
Umgesetzt ist Oskars Konzept (04 Ressourcen/Mathematik/Mein Mathe-Konzept ...): Muster entdecken lassen, erst Typ erkennen,
dann kleine feste Schritte (Rest abdecken, Term für Term umdrehen), Rezept mit Wenn-Dann, erst tun, dann Namen geben.
Alle Rechnungen und Zwischenschritte werden beim Bauen mit Python geprüft.
Aufruf: python3 baue_woche3_rezeptstil.py -> „Mathe 7c – Woche 3 – 2 Rechengesetze, Minusklammer – Rezept-Stil (Vergleich).html“"""
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_woche7 import wert, zeig, zahl, P, HEFT, UEB, box, EXTRA_CSS, weg_liste, reihe, rezept_box, merkbild  # noqa: E402

NAME = "Mathe 7c – Woche 3 – 2 Rechengesetze, Minusklammer – Rezept-Stil (Vergleich).html"


def gleich(*ausdruecke):
    assert len({wert(a) for a in ausdruecke}) == 1, ausdruecke


# ---------- Hausaufgabe (wie im Original: Buch S. 22 Nr. 9 links, Schreibweise vereinfachen) ----------
HA9 = [("(+9) - (+15)", "9 - 15"), ("(-28) - (-14)", "-28 + 14"), ("(+35) - (+25)", "35 - 25"),
       ("(-32) - (-40)", "-32 + 40"), ("(-1.5) - (+2.4)", "-1.5 - 2.4"), ("(+4.8) - (-6.4)", "4.8 + 6.4")]
for t, v in HA9:
    gleich(t, v)
HA9_A = ('<p class="gross">Vereinfache die Schreibweise und berechne.</p><ol type="a" class="ex">'
         + "".join(f"<li>{zeig(t).replace('.', ',')} =</li>" for t, _ in HA9) + "</ol>")
HA9_L = ('<ol type="a" class="ex">' + "".join(f'<li>{zeig(t).replace(".", ",")} = {zeig(v).replace(".", ",")} = <span class="lsg">{zahl(wert(v))}</span></li>'
                                              for t, v in HA9) + "</ol>"
         '<p>Bei b), d), f) steht ein Minus vor einer negativen Zahl: aus − (−14) wird + 14. Genau das passiert gleich in der Klammer.</p>')

# ---------- Muster entdecken ----------
MUSTER = [("50 - (12 + 8)", "50 - 12 - 8", 30), ("50 - (12 - 8)", "50 - 12 + 8", 46), ("30 - (-5 + 9)", "30 + 5 - 9", 26),
          ("100 - (40 - 15)", "100 - 40 + 15", 75), ("8 - (-2 - 6)", "8 + 2 + 6", 16), ("-12 - (8 - 30 + 4)", "-12 - 8 + 30 - 4", 6)]
for a, b, e in MUSTER:
    gleich(a, b)
    assert wert(a) == e
MUSTER_F = ('<ol type="a" class="ex">' + "".join(f'<li>{zeig(a)} = {zeig(b)} = <span class="lsg">{e}</span></li>'.replace("= −", "= −") for a, b, e in MUSTER)
            + '</ol><p class="gross">Was haben alle gemeinsam?</p>')
MUSTER_ANTWORT = ('<p><b>Antwort der Klasse:</b> Vor der Klammer steht ein Minus. Beim Auflösen dreht sich jedes Zeichen in der Klammer um: '
                  'aus Plus wird Minus, aus Minus wird Plus.</p>')
EINKAUF = ('<p class="gross">Du hast 50 €. Du kaufst Getränke für 12 € und bekommst 8 € Pfand zurück.</p>'
           '<div class="ausdruck">50 − (12 − 8) = 50 − 12 + 8 = <span class="lsg">46</span></div>'
           '<p class="gross">Warum wird aus − 8 in der Klammer + 8? Minus vor der Klammer heißt: alles abziehen, was drinsteht. '
           'Das Pfand ziehst du nicht ab, du bekommst es zurück.</p>')
gleich("50 - (12 - 8)", "50 - 12 + 8")

# ---------- Rezept vorführen ----------
B1 = ('<div class="schritt"><span class="sn">1</span>Minus vor der Klammer? Ja.'
      f'<div class="ausdruck">−12 {P("− (8 − 30 + 4)")}</div></div>'
      '<div class="schritt"><span class="sn">2</span>Abdecken, Term für Term umdrehen'
      '<div class="ausdruck">8 → <span class="lsg">− 8</span>; −30 → <span class="lsg">+ 30</span>; +4 → <span class="lsg">− 4</span></div>'
      '<div class="ausdruck">−12 − 8 + 30 − 4</div></div>'
      '<div class="schritt"><span class="sn">3</span>Rest'
      '<div class="ausdruck">−12 − 8 − 4 + 30 = −24 + 30 = <span class="lsg">6</span></div></div>')
gleich("-12 - (8 - 30 + 4)", "-12 - 8 + 30 - 4", "-12 - 8 - 4 + 30", "-24 + 30")
B2 = ('<div class="schritt"><span class="sn">1</span>Minus vor der Klammer? Ja.'
      f'<div class="ausdruck">50 {P("− (12 − 8 + 5)")}</div></div>'
      '<div class="schritt"><span class="sn">2</span>Umdrehen'
      '<div class="ausdruck">50 − 12 + 8 − 5</div></div>'
      '<div class="schritt"><span class="sn">3</span>Rest'
      '<div class="ausdruck">50 + 8 − 12 − 5 = 58 − 17 = <span class="lsg">41</span></div></div>')
gleich("50 - (12 - 8 + 5)", "50 - 12 + 8 - 5", "50 + 8 - 12 - 5", "58 - 17")

SCHRITTE_MK = ["Minus vor der Klammer?", "Alles davor abschreiben, dann Term für Term umdrehen.", "Gleiche Zeichen zusammen.", "Ausrechnen."]
REZEPT = rezept_box("Minusklammer", SCHRITTE_MK)
MERK = merkbild("Minusklammer",
                [(1, f'−12 {P("− (8 − 30 + 4)")}<span class="klein">Minus davor: ja</span>'),
                 (2, '= −12 <span class="rot">− 8 + 30 − 4</span>'),
                 (3, '= <span class="gelb">−12 − 8 − 4</span> + 30'),
                 (None, '= −24 + 30'),
                 (4, '= <b>6</b>')], SCHRITTE_MK)

# ---------- Üben 1: Minusklammer, Typ steht fest ----------
U1 = {"○": ["40 - (10 + 6)", "25 - (9 - 4)", "60 - (20 + 15 + 5)", "18 - (6 - 10)", "7 - (3 + 8)"],
      "◐": ["-15 - (8 - 20)", "30 - (12 - 7 + 5)", "-9 - (-4 + 6 - 11)", "45 - (-10 + 25) - 20", "-2.5 - (1.5 - 4)"],
      "●": ["-55 - (45 - 25) - 35", "14 - (3 - 9) - (8 - 20)", "-(6 - 11) - (-4 - 7) - 5", "70 - (25 - 40) - 30"]}
U1_E = {"○": [24, 20, 20, 22, -4], "◐": [-3, 20, 0, 10, 0], "●": [-110, 32, 11, 55]}
for k, liste in U1.items():
    assert [wert(a) for a in liste] == U1_E[k], k
U1_WEG_S = [("-55 - (45 - 25) - 35", "-55 - 45 + 25 - 35", "-55 - 45 - 35 + 25", "-135 + 25", "-110"),
            ("14 - (3 - 9) - (8 - 20)", "14 - 3 + 9 - 8 + 20", "14 + 9 + 20 - 3 - 8", "43 - 11", "32"),
            ("-(6 - 11) - (-4 - 7) - 5", "-6 + 11 + 4 + 7 - 5", "11 + 4 + 7 - 6 - 5", "22 - 11", "11"),
            ("70 - (25 - 40) - 30", "70 - 25 + 40 - 30", "70 + 40 - 25 - 30", "110 - 55", "55")]
for w in U1_WEG_S:
    gleich(*w)
def mit(titel, liste):
    return f'<div class="mit"><div><h4>{titel}</h4><ol type="a" class="ex">{reihe(liste)}</ol></div>{REZEPT}</div>'


def ergebnisse(liste):
    return '<ol type="a" class="ex">' + "".join(f'<li>{zeig(a)} = <span class="lsg">{zahl(wert(a))}</span></li>' for a in liste) + "</ol>"


U1_L = ('<div class="drei">' + "".join(f'<div><h4>{k}</h4><ol type="a">' + "".join(f'<li>{zeig(a)} = <span class="lsg">{zahl(wert(a))}</span></li>' for a in U1[k]) + "</ol></div>"
                                       for k in ("○", "◐", "●")) + "</div>")
U1_L_WEG = "".join(f'<div class="fnr">{"abcd"[i]})</div>' + weg_liste(w) for i, w in enumerate(U1_WEG_S))

# ---------- Rechengesetze: erst tun, dann Namen geben ----------
GESETZE = ('<div class="merk">Vertauschungsgesetz (Kommutativgesetz)<br><span style="font-weight:400">In einer Rechnung mit Plus und Minus '
           'darf man die Zahlen vertauschen. Das Zeichen vor der Zahl wandert mit.<br>−26 + 47 − 14 + 3 = 47 + 3 − 26 − 14</span></div>'
           '<div class="merk">Verbindungsgesetz (Assoziativgesetz)<br><span style="font-weight:400">In einer Rechnung mit Plus und Minus '
           'darf man Zahlen beliebig mit Klammern zusammenfassen.<br>47 + 3 − 26 − 14 = (47 + 3) + (−26 − 14) = 50 − 40 = 10</span></div>')
gleich("-26 + 47 - 14 + 3", "47 + 3 - 26 - 14", "(47 + 3) + (-26 - 14)", "50 - 40")
GES_F = HEFT(GESETZE)

# ---------- Klammer rückwärts setzen ----------
RUECK = [("90 - 25 - 35", "90 - (25 + 35)", 30), ("120 - 45 + 15 - 30", "120 - (45 - 15 + 30)", 60),
         ("64 - 18 - 22 - 14", "64 - (18 + 22 + 14)", 10), ("-5 - 12 + 7 - 8", "-5 - (12 - 7 + 8)", -18)]
for a, b, e in RUECK:
    gleich(a, b)
    assert wert(a) == e
SCHRITTE_RK = ["Ab welcher Zahl wird alles abgezogen?", "Minusklammer setzen, Zeichen in der Klammer umdrehen.", "Klammer ausrechnen.", "Ausrechnen."]
RUECK_B = merkbild("Klammer setzen",
                   [(1, f'87 {P("− 45 − 32 − 23")}'),
                    (2, '= 87 − <span class="rot">(45 + 32 + 23)</span>'),
                    (3, '= 87 − 100'),
                    (4, '= <b>−13</b>')], SCHRITTE_RK)
RUECK_F = ('<ol type="a" class="ex">'
           f'<li>90 − {P("25")} − 35 =</li><li>120 − {P("45")} + 15 − 30 =</li><li>64 − {P("18")} − 22 − 14 =</li><li>−5 − {P("12")} + 7 − 8 =</li></ol>')
RUECK_L = ('<ol type="a" class="ex">' + "".join(f'<li>{zeig(a)} = {zeig(b)} = <span class="lsg">{zahl(e)}</span></li>' for a, b, e in RUECK) + "</ol>")

# ---------- Fehler suchen, Üben 2, Exit ----------
FEHLER_A = '<div class="ausdruck">30 − (10 − 4) = 30 − 10 − 4 = 16</div><p class="gross">Stimmt das?</p>'
gleich("30 - (10 - 4)", "30 - 10 + 4", "24")
FEHLER_L = ('<div class="ausdruck">30 − (10 − 4) = 30 − 10 − 4 <span class="lsg">✗</span></div>'
            '<div class="ausdruck">30 − (10 − 4) = 30 − 10 + 4 = <span class="lsg">24</span></div>'
            '')
U2 = ["20 - (5 + 3) + 4", "20 + (5 - 3) + 4", "-7 - (-3 + 5)", "15 + (-6 + 2) - 10", "9 - (4 - 12) - (-2 + 5)"]
U2_E = [16, 26, -9, 1, 14]
assert [wert(a) for a in U2] == U2_E
U2_F = f'<div class="mit"><div><ol type="a" class="ex">{reihe(U2)}</ol></div>{REZEPT}</div>'
U2_L = ('<ol type="a" class="ex">' + "".join(f'<li>{zeig(a)} = <span class="lsg">{e}</span>{"  (Plusklammer, nichts ändern)" if i == 1 else ""}</li>'
                                              .replace("= <span", "= <span") for i, (a, e) in enumerate(zip(U2, U2_E))) + "</ol>")
EXIT = ["50 - (30 - 12 + 4)", "-8 - (-6 + 10 - 15)"]
EXIT_WEG = [("50 - (30 - 12 + 4)", "50 - 30 + 12 - 4", "50 + 12 - 30 - 4", "62 - 34", "28"),
            ("-8 - (-6 + 10 - 15)", "-8 + 6 - 10 + 15", "6 + 15 - 8 - 10", "21 - 18", "3")]
for w in EXIT_WEG:
    gleich(*w)
EXIT_F = f'<ol type="a" class="ex">{reihe(EXIT)}</ol>'
EXIT_L = "".join(f'<div class="fnr">{"ab"[i]})</div>' + weg_liste(w) for i, w in enumerate(EXIT_WEG))

FOLIEN = [
    ("Hausaufgabe: Buch S. 22 Nr. 9 links", HA9_A), ("Hausaufgabe: Lösungen", HA9_L),
    ("Was haben alle gemeinsam?", MUSTER_F),
    ("Merkheft: Minusklammer", HEFT(MERK)),
    ("Runde 1", UEB(mit("○ leicht", U1["○"]))), ("Runde 1: Lösungen", ergebnisse(U1["○"])),
    ("Runde 2", UEB(mit("◐ mittel", U1["◐"]))), ("Runde 2: Lösungen", ergebnisse(U1["◐"])),
    ("Runde 3", UEB(mit("● schwer", U1["●"]))), ("Runde 3: Lösungen", ergebnisse(U1["●"])),
    ("Die zwei Tricks haben Namen", GES_F),
    ("Merkheft: Klammer setzen", HEFT(RUECK_B)), ("Klammer setzen", UEB(RUECK_F)), ("Klammer setzen: Lösungen", RUECK_L),
    ("Wo steckt der Fehler?", UEB(FEHLER_A)), ("Wo steckt der Fehler? Lösung", FEHLER_L),
    ("Ja oder nein?", UEB(U2_F)), ("Ja oder nein? Lösungen", U2_L),
    ("Exit-Ticket", UEB(EXIT_F)), ("Exit-Ticket: Lösung", EXIT_L),
]
assert len(FOLIEN) == 20

SCHRITTE = [
    ("", "Hausaufgabe besprechen", 10, "Buch S. 22 Nr. 9 links. Bei b), d), f) auf das Minus vor der negativen Zahl zeigen.", [1, 2]),
    ("", "Muster entdecken", 6, "Sechs Gleichungen, nur fragen: Was haben alle gemeinsam?", [3]),
    ("", "Merkheft: Minusklammer", 12, "Beispiel Zeile für Zeile mit Abdecken, Rezept rechts mitschreiben. Alles ins Merkheft.", [4]),
    ("", "Runde 1 ○", 10, "Übungsheft, Merkheft daneben aufgeschlagen.", [5, 6]),
    ("", "Runde 2 ◐", 10, "Längere Klammern, negative Zahlen drin.", [7, 8]),
    ("", "Runde 3 ●", 10, "Mehrere Klammern. Schnelle starten hier.", [9, 10]),
    ("", "Rechengesetze benennen", 8, "Umsortiert und zusammengefasst haben wir schon. Jetzt die Namen ins Merkheft.", [11]),
    ("", "Merkheft: Klammer setzen", 10, "Das Rezept rückwärts, dann Aufgaben im Übungsheft.", [12, 13, 14]),
    ("", "Fehler suchen", 4, "Nur das erste Zeichen umgedreht.", [15, 16]),
    ("", "Ja oder nein?", 6, "Gemischt, ohne Hinweis.", [17, 18]),
    ("", "Exit-Ticket", 4, "Ohne Hilfe.", [19, 20]),
]
assert sum(m for _, _, m, _, _ in SCHRITTE) == 90


def main():
    vb = [("Drucken", "Nichts. Alles läuft über Folien und Übungsheft."),
          ("Digital", "Vergleichsentwurf. Folien-PDF gäbe es nur nach Freigabe."),
          ("Anders als die echte Stunde", "Statt Arbeitsblatt und Buchaufgaben ein festes Rezept mit Typ-Frage und Abdecken. Das Muster wird entdeckt, nicht vorgegeben. "
           "Die Rechengesetze kommen erst nach dem Tun, mit Namen. Das Arbeitsblatt entfällt, die Aufgaben stammen aus diesem Entwurf, nicht aus dem Buch."),
          ("Gleich geblieben", "Hausaufgabe, Pfand-Beispiel, die Namen der Gesetze (Bildungsplan), Merkheft und Übungsheft getrennt, Schwierigkeitskreise.")]
    bau_woche(HIER / NAME, "Woche 3, Stunde 2 im Rezept-Stil: Rechengesetze, Minusklammer",
              "Vergleichsentwurf, nicht für den Unterricht: so hätte die Doppelstunde vom Di 29.09.2026 im Rezept-Stil ausgesehen (90 Minuten)",
              vb, SCHRITTE, FOLIEN,
              tafel=box("Beispiel 1", B1) + box("Beispiel 2", B2) + box("Merkheft: Klammer setzen", HEFT(RUECK_B)) + box("Muster: Was haben alle gemeinsam?", MUSTER_F + MUSTER_ANTWORT + EINKAUF),
              merkheft=box("Minusklammer", HEFT(MERK)) + box("Rechengesetze", HEFT(GESETZE)) + box("Klammer setzen", HEFT(RUECK_B)),
              loesungen=box("Hausaufgabe Buch S. 22 Nr. 9 links", HA9_L) + box("Üben ○◐●", U1_L) + box("Üben ●: Rechenwege", U1_L_WEG)
              + box("Klammer setzen", RUECK_L) + box("Ja oder nein?", U2_L) + box("Exit-Ticket", EXIT_L),
              extra_css=EXTRA_CSS, verlauf="Die Doppelstunde")


if __name__ == "__main__":
    main()
