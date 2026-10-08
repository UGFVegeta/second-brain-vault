#!/usr/bin/env python3
"""Mathe 7c, Woche 4, Stunde 2 und 3: Dividieren (Mi 07.10.2026, Einzelstunde) und Dividieren üben (Do 08.10.2026, Einzelstunde).
Gleiches Vorgehen wie Stunde 1 (baue_woche4.py): A4-Seiten, je Abschnitt eine Seite und direkt danach dieselbe Seite ausgefüllt;
Whiteboard-Einstieg als Querfolie (5 Aufgaben, Antwort nur Zahl, Zahl mit Vorzeichen oder Vorzeichen); Merkheft-Bild mit Beispiel links,
Rezept rechts und mindestens 6 Beispielen; Übungsseiten mit „Aufgabe:“ und „Für Schnelle:“, Buchaufgaben abgetippt (S. 29, 30, 37, 42);
letzte Seite „Weitere Aufgaben und Hausaufgabe“. Hausaufgabe mischt Multiplizieren und Dividieren (Oskar, 06.10.2026).
Jede Lösung wird mit Python geprüft. Aufruf: python3 baue_woche4_division.py"""
import sys
from fractions import Fraction
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_woche7 import merkbild, rezept_box, wert, zahl, HEFT, UEB, box, EXTRA_CSS, raster_stil, LUECKE, LUECKE_LANG  # noqa: E402
from baue_woche4 import L, pruefe, spalten, block, auftrag, ergaenze_a4, G  # noqa: E402


def wb_seite(liste):
    """Whiteboard-Querfolie: 5 Karten, die anderen deckt Oskar mit dem Pflaster ab."""
    for art, a, ant, w in liste:
        if w is not None:
            assert wert(a) == w, a
            if art == "Nur das Vorzeichen":
                assert (ant == "−") == (w < 0), a
    def seite(l):
        karten = "".join(f'<div class="wbk"><div class="wbn">{i}</div><div class="wba"{' style="font-size:34px"' if len(a) > 14 else ''}>{a}</div><div class="wbf">{art}</div>'
                         f'<div class="wbl">{L(ant) if l else LUECKE}</div></div>' for i, (art, a, ant, _) in enumerate(liste, 1))
        return f'<div class="wbq">{karten}</div>'
    return seite


# ================================================================ gemeinsame Teile
SCHRITTE_D = ["Vorzeichen anschauen.", "Gleich (+ und + oder − und −)? Plus hinschreiben. Verschieden? Minus hinschreiben, Minus gewinnt.",
              "Die Zahlen dividieren."]
MERK_D = merkbild("Dividieren", [
    [(1, '(−56) : (−8)<span class="klein">− und −: gleich</span>'), (2, '= <span class="rot">+</span>(56 : 8)'), (3, '= <b>7</b>')],
    [(1, '72 : (−9)<span class="klein">+ und −: verschieden</span>'), (2, '= <span class="rot">−</span>(72 : 9)'), (3, '= <b>−8</b>')],
], SCHRITTE_D, weitere=[
    ("(+48) : (+6)", '<span class="rot">+</span>8', 8), ("(−36) : (−4)", '<span class="rot">+</span>9', 9),
    ("(+45) : (−5)", '<span class="rot">−</span>9', -9), ("(−63) : (+7)", '<span class="rot">−</span>9', -9),
    ("(−4,8) : (+8)", '<span class="rot">−</span>0,6', -0.6), ("(+2,5) : (−1)", '<span class="rot">−</span>2,5', -2.5)])

# ================================================================ Mittwoch: Dividieren einführen
WB_MI = [("Ergebnis", "(−6) · (−7)", "42", 42), ("Ergebnis", "(+8) · (−5)", "−40", -40), ("Nur das Vorzeichen", "(−3) · (−4) · (−2)", "−", -24),
         ("Ergebnis", "(−0,5) · (+8)", "−4", -4), ("Nur das Vorzeichen", "(−9) · (+7)", "−", -63)]

# Einstieg (Oskar, 06.10.2026): keine Umkehraufgaben, sondern die Regel vom Multiplizieren direkt übertragen.
# Erst nur das Vorzeichen setzen, dann rechnen. Alle Vorzeichenkombinationen kommen vor.
UEBERTRAG = [("(−24) : (−6)", 4), ("35 : (−7)", -5), ("(−48) : 8", -6), ("(+56) : (+8)", 7), ("(−63) : (−9)", 7), ("(+40) : (−5)", -8)]
for _a, _e in UEBERTRAG:
    assert wert(_a) == _e, _a


def seite_uebertrag(l):
    zeilen = "".join(f'<tr><td class="u-d">{a}</td><td class="u-p">Vorzeichen</td><td>{L("+" if e > 0 else "−") if l else LUECKE}</td>'
                     f'<td class="u-p">Ergebnis</td><td class="u-d">{L(zahl(e)) if l else LUECKE_LANG}</td></tr>' for a, e in UEBERTRAG)
    tab = f'<table class="umkehr" style="font-size:{G + 4}px">{zeilen}</table>'
    kopf = block("Gilt die Regel vom Multiplizieren auch beim Dividieren? Erst das Vorzeichen, dann rechnen.", tab)
    if l:
        return kopf + '<p style="font-size:20px">Ja: Gleiche Regel wie beim Multiplizieren.</p>' + HEFT(MERK_D)
    return kopf


S29_1 = pruefe([("(+12) : (−3)", -4), ("(−18) : (+6)", -3), ("(−35) : (−7)", 5), ("(−32) : (−8)", 4),
                ("(−48) : (−6)", 8), ("(−42) : (+7)", -6), ("(+63) : (−9)", -7), ("(−72) : (−12)", 6)])
S29_2 = pruefe([("(−27) : (+3)", -9), ("(+64) : (−8)", -8), ("(−49) : (−7)", 7), ("(−75) : (−5)", 15)])
S29_2_V = ["−27 : 3", "−64 : 8", "49 : 7", "75 : 5"]
for (a, e), v in zip(S29_2, S29_2_V):
    assert zahl(wert(v)) == e, v
S30_4 = [("(+48) : (+8)", 6, "S"), ("(+54) : (−9)", -6, "U"), ("(−35) : (+7)", -5, "R"), ("(−32) : (−8)", 4, "F"), ("(+63) : (−9)", -7, "E"), ("(+81) : (−9)", -9, "R")]
for a, e, _ in S30_4:
    assert wert(a) == e, a
assert "".join(b for *_, b in S30_4) == "SURFER"


def s29_2_liste(l):
    texte = [f"{a} = {v} = {e}" for (a, e), v in zip(S29_2, S29_2_V)]
    items = "".join(f"<li>{a} = {f'{v} = ' + L(e) if l else ''}</li>" for (a, e), v in zip(S29_2, S29_2_V))
    return f'<ol type="a" class="ex raster" style="{raster_stil(texte, G)}">{items}</ol>'


def surfer(l):
    items = "".join(f"<li>{a} = {L(zahl(e) + ' ' + b) if l else ''}</li>" for a, e, b in S30_4)
    return (f'<ol type="a" class="ex raster" style="{raster_stil([a + " = −6 U" for a, _, _ in S30_4], G)}">{items}</ol>'
            + '<p style="font-size:18px">Kärtchen: −7 E; 4 F; −6 U; 6 S; −9 R; −5 R</p>'
            + (f'<p style="font-size:18px">Lösungswort: {L("SURFER")}</p>' if l else ""))


def seite_uebung_mi(l):
    return (auftrag("Übungsheft, Buch S. 29 Nr. 1 und Nr. 2.", "Buch S. 30 Nr. 4, das Lösungswort")
            + UEB(block("Buch S. 29 Nr. 1: Dividiere im Kopf.", spalten(S29_1, l, gross=G))
                  + block("Buch S. 29 Nr. 2: Vereinfache zunächst die Schreibweise. Berechne dann.", s29_2_liste(l))
                  + block("Für Schnelle: Buch S. 30 Nr. 4 (Lösungswort)", surfer(l))))


# Hausaufgabe Mittwoch: Multiplizieren und Dividieren gemischt (Buch S. 37 Nr. 13 und 14)
S37_13 = pruefe([("9 · (−7)", -63), ("(−8) · 6", -48), ("11 · (−8)", -88), ("(−12) · (−5)", 60), ("21 · (−11)", -231), ("(−25) · (−16)", 400)])
S37_14 = pruefe([("(−36) : 3", -12), ("54 : (−6)", -9), ("(−84) : (−7)", 12), ("(−125) : 5", -25), ("160 : (−8)", -20), ("(−270) : (−9)", 30)])
S29_3 = pruefe([("96 : (−6)", -16), ("(−112) : 4", -28), ("(−175) : (−7)", 25), ("264 : (−8)", -33)])


def seite_rest_mi(l):
    return (auftrag("Übungsheft, Buch S. 29 Nr. 3, danach die Hausaufgabe.", "Buch S. 30 Nr. 4 fertig machen")
            + UEB(block("Buch S. 29 Nr. 3: Dividiere schriftlich. Achte zunächst nicht auf die Vorzeichen.", spalten(S29_3, l, gross=G))
                  + block("Hausaufgabe: Buch S. 37 Nr. 13 (Multipliziere)", spalten(S37_13, l, gross=G))
                  + block("Hausaufgabe: Buch S. 37 Nr. 14 (Dividiere)", spalten(S37_14, l, gross=G))))


# ================================================================ Donnerstag: Dividieren üben
WB_DO = [("Ergebnis", "(−42) : (−6)", "7", 7), ("Ergebnis", "(+56) : (−8)", "−7", -7), ("Nur das Vorzeichen", "(−81) : (−9)", "+", 9),
         ("Ergebnis", "(−12) · (−3)", "36", 36), ("Ergebnis", "(−0,9) : (+3)", "−0,3", -0.3)]

S30_A = [("(+35) : (−7) = ■5", "(+35) : (−7)", -5), ("(−64) : (+8) = ■8", "(−64) : (+8)", -8), ("(■42) : (+7) = −6", "(−42) : (+7)", -6),
         ("(−88) : (■11) = 8", "(−88) : (−11)", 8)]
for _, a, e in S30_A:
    assert wert(a) == e, a
S30_B = pruefe([("(−77) : 11", -7), ("72 : (−9)", -8), ("(−56) : (−7)", 8), ("(−84) : (−12)", 7)])
S30_7 = [("72 : ■ = −9", "72 : (−8)", -9, "−8"), ("(−72) : ■ = −9", "(−72) : 8", -9, "8"), ("■ : 7 = −8", "(−56) : 7", -8, "−56"),
         ("■ : (−7) = 9", "(−63) : (−7)", 9, "−63"), ("(−48) : ■ = 12", "(−48) : (−4)", 12, "−4"), ("■ : (−12) = −4", "48 : (−12)", -4, "48")]
for _, a, e, _z in S30_7:
    assert wert(a) == e, a
S30_8R = [("16 ■ (−8) ■ (−2) = 4", "16 : (−8) · (−2)", 4), ("16 ■ (−8) ■ (−2) = 64", "16 · (−8) : (−2)", 64),
          ("16 ■ (−8) ■ (−2) = 1", "16 : (−8) : (−2)", 1), ("16 ■ (−8) ■ (−2) = 256", "16 · (−8) · (−2)", 256)]
for _, a, e in S30_8R:
    assert wert(a) == e, a


def luecken(liste, l, loesung):
    texte = [z for z, *_ in liste]
    if not l:
        return (f'<ol type="a" class="ex raster" style="{raster_stil([t.replace("■", LUECKE) for t in texte], G - 2)}">'
                + "".join(f"<li>{z.replace('■', LUECKE)}</li>" for z in texte) + "</ol>")
    lt = [loesung(x) for x in liste]
    return f'<ol type="a" class="ex raster" style="{raster_stil(lt, G - 2)}">' + "".join(f"<li>{x}</li>" for x in lt) + "</ol>"


def liste_einfach(zeilen):
    """Einfache Liste ohne Raster (bricht sauber über Seiten, wenn große Kästchen drin sind)."""
    return f'<ol type="a" class="ex" style="font-size:{G - 2}px;line-height:1.9">' + "".join(f"<li>{z}</li>" for z in zeilen) + "</ol>"


def seite_uebung_do1(l):
    return (auftrag("Übungsheft, Buch S. 30 Alles klar? A und B, dann Nr. 7.", "Buch S. 30 Nr. 8 (rechts), Rechenzeichen einsetzen")
            + UEB(block("Buch S. 30 Alles klar? A: Ergänze das fehlende Vorzeichen.", luecken(S30_A, l, lambda x: f"{x[1]} = {L(zahl(x[2]))}"))
                  + block("Alles klar? B: Dividiere.", spalten(S30_B, l, gross=G))
                  + block("Buch S. 30 Nr. 7: Setze die richtige Zahl ein.", luecken(S30_7, l, lambda x: f"{x[1]} = {zahl(x[2])}  ({L(x[3])})"))
                  + block("Für Schnelle: Buch S. 30 Nr. 8 (rechts): Setze · und : richtig ein.", liste_einfach([z.replace("■", LUECKE) for z, *_ in S30_8R] if not l else [f"{a} = {L(zahl(e))}" for _, a, e in S30_8R]))))


S30_4R = pruefe([("(−90) : 6", -15), ("105 : (−15)", -7), ("(−99) : 11", -9), ("(−108) : (−12)", 9)])
S30_6R = pruefe([("4446 : (−6)", -741), ("9768 : (−11)", -888), ("(−7776) : 9", -864), ("(−9468) : 12", -789),
                 ("(−0,72) : 6", -0.12), ("9,5 : (−0,5)", -19), ("(−5,12) : (−0,8)", 6.4), ("(−19,6) : (−0,7)", 28)])
S30_7R = [("3/5 : (−1/2)", Fraction(-6, 5)), ("2/5 : (−2/3)", Fraction(-3, 5)), ("(−2/3) : 4/9", Fraction(-3, 2)), ("(−3/5) : (−9/10)", Fraction(2, 3))]
F = Fraction     # Bruch : Bruch ausdrücklich rechnen (wert() würde 4/9 nicht als einen Bruch lesen)
assert [F(3, 5) / F(-1, 2), F(2, 5) / F(-2, 3), F(-2, 3) / F(4, 9), F(-3, 5) / F(-9, 10)] == [e for _, e in S30_7R]
bruch = lambda f: ("−" if f < 0 else "") + f"{abs(f.numerator)}/{f.denominator}"


def seite_uebung_do2(l):
    br = "".join(f"<li>{a} = {L(bruch(e)) if l else ''}</li>" for a, e in S30_7R)
    return (auftrag("Übungsheft, Buch S. 30 Nr. 4 (rechts) und Nr. 6 (rechts).", "Buch S. 30 Nr. 7 (rechts), Brüche: mit dem Kehrbruch multiplizieren")
            + UEB(block("◐ Buch S. 30 Nr. 4 (rechts): Berechne im Kopf.", spalten(S30_4R, l, gross=G))
                  + block("◐ Buch S. 30 Nr. 6 (rechts): Dividiere schriftlich.", spalten(S30_6R, l, gross=G))
                  + block("Für Schnelle: Buch S. 30 Nr. 7 (rechts)",
                          f'<ol type="a" class="ex raster" style="{raster_stil([a + " = −3/2" for a, _ in S30_7R], G)}">{br}</ol>')))


# Weitere Aufgaben und Hausaufgabe Donnerstag: Multiplizieren und Dividieren gemischt
S30_6 = pruefe([("(−267) : 3", -89), ("392 : (−7)", -56), ("2328 : (−4)", -582), ("(−5706) : 9", -634), ("(−2856) : (−8)", 357), ("(−2574) : (−11)", 234)])
S42_5 = pruefe([("(−12) · 6", -72), ("7,5 · (−5)", -37.5), ("104 : (−8)", -13), ("(−28,8) : (−3)", 9.6)])
S37_15 = pruefe([("(−7,2) · 0,5", -3.6), ("(−7,2) − 0,5", -7.7), ("(−7,2) + 0,5", -6.7), ("(−7,2) : 0,5", -14.4)])


def seite_rest_do(l):
    return (auftrag("Übungsheft, Buch S. 30 Nr. 6, danach die Hausaufgabe.", "Buch S. 30 Nr. 8 (Temperaturen)")
            + UEB(block("Buch S. 30 Nr. 6: Dividiere schriftlich.", spalten(S30_6, l, gross=G))
                  + block("Hausaufgabe: Buch S. 42 Nr. 5 (Multipliziere oder dividiere)", spalten(S42_5, l, gross=G))
                  + block("Hausaufgabe: Buch S. 37 Nr. 15 (Welches Ergebnis passt? Rechne alle vier.)", spalten(S37_15, l, gross=G))))


# S. 30 Nr. 8 (für Schnelle, Lösung nur im Lösungen-Tab): durchschnittliche Temperaturänderung pro Stunde
T8A, T8B = (-48.9 - 6.7) / 10, (9.4 - (-47.8)) / 24
assert round(T8A, 2) == -5.56 and round(T8B, 2) == 2.38

# ================================================================ Stunden
STUNDEN = [
    dict(nr=2, titel="Dividieren", wann="Mi 07.10.2026, Einzelstunde",
         seiten=[("Whiteboards", wb_seite(WB_MI)), ("2 Dividieren", seite_uebertrag), ("3 Übung", seite_uebung_mi),
                 ("4 Weitere Aufgaben und Hausaufgabe", seite_rest_mi)],
         schritte=[("", "Whiteboards: 5 Aufgaben Multiplizieren", 6, "Querfolie, die anderen mit dem Pflaster abdecken, auf „Alle hoch“ zeigen.", [1, 2]),
                   ("", "Gilt die Regel auch hier?", 7, "Sechs Geteiltaufgaben: erst nur das Vorzeichen setzen, dann rechnen. Gleiche Regel wie beim Mal.", [3]),
                   ("", "Merkheft: Dividieren", 8, "Steht auf der ausgefüllten Seite: Beispiel links, Rezept rechts, weitere Beispiele.", [4]),
                   ("", "Übung", 16, "S. 29 Nr. 1 und 2, Schnelle: S. 30 Nr. 4 (SURFER). Dann besprechen.", [5, 6]),
                   ("", "Puffer und Hausaufgabe", 8, "Nur wenn Zeit bleibt: S. 29 Nr. 3. HA: S. 37 Nr. 13 und 14 (Mal und Geteilt gemischt).", [7, 8])],
         vorbereiten=[("Drucken", "Nichts."), ("Sonst", "Mini-Whiteboards und Stifte, Buch.")],
         tafel=box("Gilt die Regel auch beim Dividieren?", seite_uebertrag(True)), merkheft=box("Dividieren", HEFT(MERK_D))),
    dict(nr=3, titel="Dividieren üben", wann="Do 08.10.2026, Einzelstunde",
         seiten=[("Whiteboards", wb_seite(WB_DO)), ("2 Übung 1", seite_uebung_do1), ("3 Übung 2", seite_uebung_do2),
                 ("4 Weitere Aufgaben und Hausaufgabe", seite_rest_do)],
         schritte=[("", "Whiteboards: 5 Aufgaben Mal und Geteilt", 6, "Querfolie wie am Mittwoch.", [1, 2]),
                   ("", "Übung 1", 17, "Alles klar A und B, Nr. 7. Schnelle: Nr. 8 rechts. Merkheft offen.", [3, 4]),
                   ("", "Übung 2 ◐", 15, "S. 30 Nr. 4 und 6 rechts. Schnelle: Nr. 7 rechts (Brüche).", [5, 6]),
                   ("", "Puffer und Hausaufgabe", 7, "Nur wenn Zeit bleibt: S. 30 Nr. 6. HA: S. 42 Nr. 5 und S. 37 Nr. 15.", [7, 8])],
         vorbereiten=[("Drucken", "Nichts."), ("Sonst", "Mini-Whiteboards und Stifte, Buch.")],
         tafel=box("Erinnerung: Merkheft Dividieren", MERK_D), merkheft=box("Kein neuer Eintrag", "<p>Dividieren steht seit Mittwoch im Merkheft.</p>")),
]
for st in STUNDEN:
    assert sum(m for _, _, m, _, _ in st["schritte"]) == 45, st["titel"]
    st["name"] = f"Mathe 7c – Woche 4 – {st['nr']} {st['titel']}"
    st["folien"] = [x for t, f in st["seiten"] for x in ((t, f(False)), (f"{t}: ausgefüllt", f(True)))]
    st["quer"] = {"Whiteboards", "Whiteboards: ausgefüllt"}

EXTRA = EXTRA_CSS          # .umkehr steht in baue_woche7.EXTRA_CSS (auch für die A4-PDFs)


def main():
    for st in STUNDEN:
        loes = "".join(box(t.replace(": ausgefüllt", ""), h) for t, h in st["folien"] if t.endswith("ausgefüllt"))
        bau_woche(HIER / f"{st['name']}.html", f"Woche 4, Stunde {st['nr']}: {st['titel']}", f"Klasse 7c, Mathematik, {st['wann']}, Buch S. 29, 30, 37 und 42",
                  st["vorbereiten"] + [("Digital", f"Folien-PDF in Notability: {st['name']}.pdf (iCloud, 04 Rationale Zahlen).")],
                  st["schritte"], st["folien"], tafel=st["tafel"], merkheft=st["merkheft"],
                  loesungen=loes + (box("Für Schnelle: S. 30 Nr. 8 (Temperaturen)",
                                        f"<p>a) (−48,9 − 6,7) : 10 ≈ {L('−5,56 °C pro Stunde')}; b) (9,4 + 47,8) : 24 ≈ {L('2,38 °C pro Stunde')}</p>")
                                    if st["nr"] == 3 else ""),
                  extra_css=EXTRA, verlauf="Die Stunde")


if __name__ == "__main__":
    main()
