#!/usr/bin/env python3
"""Mathe 7c, Woche 4, Stunde 1 (Di 06.10.2026, Doppelstunde): Wiederholung Subtraktion, dann Multiplizieren.
Rezept-Stil: Merkheft-Bild = Beispiel links mit Schrittnummern, Rezept rechts; Runden ○◐● mit Rezept daneben.
Oskars Rezept fürs Multiplizieren: erst die Vorzeichen anschauen, gleich -> Plus, verschieden -> Minus (Minus gewinnt),
das Vorzeichen hinschreiben, dann die Zahlen multiplizieren.
Buchaufgaben (S. 27, 28, 36, 42) abgetippt, nicht als Bildausschnitt (Oskar, 05.10.2026). Jede Lösung wird mit Python geprüft.
Aufruf: python3 baue_woche4.py"""
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_woche7 import merkbild, rezept_box, wert, zahl, HEFT, UEB, box, EXTRA_CSS, raster_stil, LUECKE  # noqa: E402
from rezepte_rz import MERK_PLUSMINUS, REZEPT_PM  # noqa: E402
from baue_woche3_rezeptstil import MERK as MERK_MK, REZEPT as REZEPT_MK  # noqa: E402

NAME = "Mathe 7c – Woche 4 – 1 Wiederholung Minusklammer, Multiplizieren"
L = lambda x: f'<span class="lsg">{x}</span>'


def pruefe(liste):
    """[(Aufgabe, erwartetes Ergebnis)] -> prüft mit Python und gibt [(Aufgabe, Ergebnis-Text)] zurück."""
    for a, e in liste:
        assert round(wert(a), 6) == round(e, 6), (a, wert(a), e)
    return [(a, zahl(e)) for a, e in liste]


def spalten(aufgaben, mit_loesung=False, n=2, gross=36):
    """Aufgabenliste im Raster; eine Aufgabe bricht nie um (n bleibt als Aufrufparameter, das Raster richtet sich nach dem Platz)."""
    texte = [f"{a} = {e if mit_loesung else ''}" for a, e in aufgaben]
    items = "".join(f"<li>{a} = {L(e) if mit_loesung else ''}</li>" for a, e in aufgaben)
    return f'<ol type="a" class="ex raster" style="{raster_stil(texte, gross)}">{items}</ol>'


def mit(titel, inhalt, rezept):
    return f'<div class="mit"><div><h4>{titel}</h4>{inhalt}</div>{rezept}</div>'


# ================================================================ Wiederholung Subtraktion
S36_7 = pruefe([("(+18) − (+13)", 5), ("(+27) − (−9)", 36), ("(−30) − (+25)", -55), ("(−14) − (−26)", 12),
                ("(−22) − (+32)", -54), ("(−43) − (−27)", -16), ("(−41) − (+28)", -69), ("(−57) − (−43)", -14)])
S36_8 = pruefe([("(−54) + (+26)", -28), ("(+51) − (+19)", 32), ("−34 + (−12)", -46), ("45 − (−15)", 60),
                ("−8 − (+12) + (−6)", -26), ("30 + (−20) − (−40)", 50)])
S42_4 = pruefe([("−32 + 24", -8), ("−15 + (−48)", -63), ("63 − (−27)", 90), ("−1,8 − (−0,9)", -0.9)])
WDH_HINWEIS = '<p style="font-size:20px;color:#66798e">Erst die Schreibweise vereinfachen: Minus vor einer negativen Zahl wird Plus, z. B. 45 − (−15) = 45 + 15.</p>'

S26_8 = pruefe([("−55 − (45 − 25) − 35", -110), ("(−55 − 45) − 25 − 35", -160), ("−55 − (45 − 25 − 35)", -40),
                ("−55 − 45 − (25 − 35)", -90), ("−(55 − 45) − 25 − 35", -70)])
# Wiederholung Minusklammer (Oskar, 05.10.2026): nur zwei Zahlen in der Minusklammer, eigene Aufgaben.
# (Aufgabe, aufgelöst, Ergebnis) – beide Formen werden mit Python geprüft.
MK_O = [("50 − (12 + 8)", "50 − 12 − 8", 30), ("40 − (15 − 5)", "40 − 15 + 5", 30), ("30 − (10 − 4)", "30 − 10 + 4", 24),
        ("25 − (7 + 3)", "25 − 7 − 3", 15), ("60 − (20 − 30)", "60 − 20 + 30", 70), ("18 − (6 + 14)", "18 − 6 − 14", -2),
        ("9 − (4 − 11)", "9 − 4 + 11", 16), ("35 − (40 + 5)", "35 − 40 − 5", -10)]
MK_M = [("−20 − (15 + 5)", "−20 − 15 − 5", -40), ("−12 − (8 − 30)", "−12 − 8 + 30", 10), ("18 − (−6 + 4)", "18 + 6 − 4", 20),
        ("−7 − (−3 − 9)", "−7 + 3 + 9", 5), ("4,5 − (1,5 − 3)", "4,5 − 1,5 + 3", 6), ("−2,5 − (−1,5 + 4)", "−2,5 + 1,5 − 4", -5)]
for _a, _b, _e in MK_O + MK_M:
    assert wert(_a) == wert(_b) == _e, _a


# Whiteboard-Einstieg (Oskar, 05.10.2026): 8 Aufgaben, Antwort nur eine Zahl, eine Zahl mit Vorzeichen oder nur ein Vorzeichen.
# (Frage-Art, Aufgabe, Antwort-Text, Kontrollwert oder None)
WB = [("Ergebnis", "7 − 12", "−5", -5), ("Ergebnis", "−9 + 15", "6", 6), ("Nur das Vorzeichen", "−25 + 18", "−", -7),
      ("Vorzeichen der 8 nach dem Auflösen", "20 − (5 − 8)", "+", None), ("Ergebnis", "12 − (4 − 9)", "17", 17)]
for _art, _a, _ant, _w in WB:
    if _w is not None:
        assert wert(_a) == _w, _a
        if _art == "Nur das Vorzeichen":
            assert (_ant == "−") == (_w < 0), _a
assert wert("20 − (5 − 8)") == wert("20 − 5 + 8")     # die 8 wird beim Auflösen zu + 8


def seite_wb(l):
    """Eine Querfolie mit allen 5 Aufgaben nebeneinander (Oskar deckt mit dem Pflaster-Tool in Notability die anderen ab)."""
    karten = "".join(f'<div class="wbk"><div class="wbn">{i}</div><div class="wba">{a}</div><div class="wbf">{art}</div>'
                     f'<div class="wbl">{L(ant) if l else LUECKE}</div></div>' for i, (art, a, ant, _) in enumerate(WB, 1))
    return f'<div class="wbq">{karten}</div>'


def mk_liste(liste, l):
    texte = [f"{a} = {b} = {zahl(e)}" if l else f"{a} =" for a, b, e in liste]
    items = "".join(f"<li>{a} = {b} = {L(zahl(e))}</li>" if l else f"<li>{a} =</li>" for a, b, e in liste)
    return f'<ol type="a" class="ex raster" style="{raster_stil(texte, 22)}">{items}</ol>'


# ================================================================ Muster entdecken (Buch S. 27, Tafel)
LINKS = [("4 · 4", 16), ("4 · 2", 8), ("4 · 0", 0), ("4 · (−2)", -8), ("4 · (−4)", -16), ("4 · (−8)", -32)]
RECHTS = [("4 · (−8)", -32), ("2 · (−8)", -16), ("0 · (−8)", 0), ("(−2) · (−8)", 16), ("(−4) · (−8)", 32), ("(−8) · (−8)", 64)]
for a, e in LINKS + RECHTS:
    assert wert(a) == e, a


def reihe(zeilen, offen_ab):
    return "".join(f'<div class="ausdruck" style="font-size:32px;margin:2px 0">{a} = {L(zahl(e)) if i >= offen_ab else zahl(e)}</div>' for i, (a, e) in enumerate(zeilen))


def reihe_leer(zeilen, offen_ab):
    return "".join(f'<div class="ausdruck" style="font-size:32px;margin:2px 0">{a} = {"" if i >= offen_ab else zahl(e)}</div>' for i, (a, e) in enumerate(zeilen))


MUSTER_A = (f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:30px"><div>{reihe_leer(LINKS, 3)}</div><div>{reihe_leer(RECHTS, 3)}</div></div>'
            '<p class="gross">Wie geht es weiter?</p>')
MUSTER_L = (f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:30px"><div>{reihe(LINKS, 3)}</div><div>{reihe(RECHTS, 3)}</div></div>'
            '<p class="gross">Links: jedes Mal 8 weniger. Rechts: jedes Mal 16 mehr.<br>Gleiche Vorzeichen: Plus. Verschiedene Vorzeichen: Minus.</p>')
ADDITION = ('<div class="ausdruck">3 · (−5) = (−5) + (−5) + (−5) = −15</div>'
            '<p>Mal ist eine verkürzte Addition, auch bei negativen Zahlen (Buch S. 27).</p>')
assert wert("3 · (−5)") == wert("(−5) + (−5) + (−5)") == -15

# ================================================================ Merkheft-Bild Multiplizieren
SCHRITTE_M = ["Vorzeichen anschauen.", "Gleich (+ und + oder − und −)? Plus hinschreiben. Verschieden? Minus hinschreiben, Minus gewinnt.",
              "Die Zahlen multiplizieren."]
MERK_M = merkbild("Multiplizieren", [
    [(1, '(−4) · (−7)<span class="klein">− und −: gleich</span>'), (2, '= <span class="rot">+</span>(4 · 7)'), (3, '= <b>28</b>')],
    [(1, '5 · (−8)<span class="klein">+ und −: verschieden</span>'), (2, '= <span class="rot">−</span>(5 · 8)'), (3, '= <b>−40</b>')],
], SCHRITTE_M, weitere=[
    ("(+3) · (+5)", '<span class="rot">+</span>15', 15), ("(−6) · (−9)", '<span class="rot">+</span>54', 54),
    ("(+7) · (−2)", '<span class="rot">−</span>14', -14), ("(−8) · (+4)", '<span class="rot">−</span>32', -32),
    ("(−0,5) · (−6)", '<span class="rot">+</span>3', 3), ("(−1) · 12", '<span class="rot">−</span>12', -12)])
REZEPT_M = rezept_box("Multiplizieren", SCHRITTE_M)

# ================================================================ Runden (Buch, abgetippt)
S27_1 = pruefe([("(−3) + (−3) + (−3) + (−3)", -12), ("(−7) + (−7) + (−7) + (−7) + (−7)", -35), ("(−10) + (−10) + (−10)", -30)])
S27_1_L = ["4 · (−3) = −12", "5 · (−7) = −35", "3 · (−10) = −30"]
S27_2 = pruefe([("(+5) · (−7)", -35), ("(−3) · (+8)", -24), ("(−2) · (−9)", 18), ("(−7) · (−6)", 42), ("(−9) · (+7)", -63), ("(+12) · (−3)", -36),
                ("(−8) · (+11)", -88), ("(+5) · (−15)", -75), ("(−9) · (−9)", 81), ("(−12) · (−20)", 240), ("(+6) · (−9)", -54), ("(−7) · (−7)", 49)])
# S. 28 Nr. 3: fehlendes Vorzeichen (■), Lösung = vollständige Aufgabe
S28_3 = [("(−7) · (+4) = ■28", "(−7) · (+4)", -28), ("(+12) · (−4) = ■48", "(+12) · (−4)", -48), ("(+12) · (■8) = −96", "(+12) · (−8)", -96),
         ("(■7) · (−6) = +42", "(−7) · (−6)", 42), ("(■14) · (−5) = +70", "(−14) · (−5)", 70), ("(−15) · (■9) = +135", "(−15) · (−9)", 135)]
for _, a, e in S28_3:
    assert wert(a) == e, a
S28_A = [("(+8) · (−4) = ■32", "(+8) · (−4)", -32), ("(−9) · (+3) = ■27", "(−9) · (+3)", -27), ("(+5) · (−12) = ■60", "(+5) · (−12)", -60),
         ("(−7) · (−7) = ■49", "(−7) · (−7)", 49)]
for _, a, e in S28_A:
    assert wert(a) == e, a
S28_B = pruefe([("(+7) · (+3)", 21), ("(+5) · (−9)", -45), ("(−8) · (+4)", -32), ("(−6) · (−10)", 60)])
S28_3D = pruefe([("(−2,5) · 3", -7.5), ("1,2 · (−4)", -4.8), ("(−0,5) · 1,8", -0.9), ("(−2,4) · (−0,5)", 1.2),
                 ("(−6,4) · (−1,5)", 9.6), ("(−3,2) · (−2,5)", 8), ("0,25 · (−8,0)", -2), ("(−1,6) · (−0,02)", 0.032)])
S28_7 = pruefe([("(−2) · (−3) · (−4)", -24), ("(−6) · 3 · (−8)", 144), ("8 · (−4) · (−2) · 5", 320), ("(−12) · 3 · 2 · (−5)", 360)])
S28_5 = pruefe([("(+15) · (−17)", -255), ("(−36) · 27", -972), ("(−28) · 32", -896), ("18 · (−25)", -450), ("53 · (−12)", -636), ("(−23) · (−79)", 1817)])
EXIT = pruefe([("(−6) · (−8)", 48), ("9 · (−4)", -36), ("(−3) · 2 · (−5)", 30)])


def ergaenze(liste, mit_loesung):
    if not mit_loesung:
        texte = [z.replace("■", LUECKE) for z, _, _ in liste]
        return f'<ol type="a" class="ex raster" style="{raster_stil(texte, 36)}">' + "".join(f"<li>{z}</li>" for z in texte) + "</ol>"
    texte = [f"{a} = {zahl(e)}" for _, a, e in liste]
    return f'<ol type="a" class="ex raster" style="{raster_stil(texte, 34)}">' + "".join(f"<li>{a} = {L(zahl(e))}</li>" for _, a, e in liste) + "</ol>"


MEHR = '<p style="font-size:20px;color:#66798e">Mehr als zwei Faktoren: immer zwei nacheinander.</p>'

# ================================================================ A4-Seiten (Oskar, 05.10.2026: wenige Seiten statt vieler Folien)
# Je Abschnitt eine A4-Seite mit Aufgaben, direkt danach dieselbe Seite ausgefüllt.
G = 22          # Schriftgröße der Aufgaben auf der A4-Seite


def block(titel, inhalt):
    return f'<div class="block"><h4>{titel}</h4>{inhalt}</div>'


def ergaenze_a4(liste, mit_loesung):
    if not mit_loesung:
        texte = [z.replace("■", LUECKE) for z, _, _ in liste]
        return f'<ol type="a" class="ex raster" style="{raster_stil(texte, G - 2)}">' + "".join(f"<li>{z}</li>" for z in texte) + "</ol>"
    texte = [f"{a} = {zahl(e)}" for _, a, e in liste]
    return f'<ol type="a" class="ex raster" style="{raster_stil(texte, G - 2)}">' + "".join(f"<li>{a} = {L(zahl(e))}</li>" for _, a, e in liste) + "</ol>"


def muster(loesung):
    zeile = lambda a, e, offen: f'<div class="ausdruck" style="font-size:{G}px;margin:2px 0">{a} = {(L(zahl(e)) if loesung else "") if offen else zahl(e)}</div>'
    links = "".join(zeile(a, e, i >= 3) for i, (a, e) in enumerate(LINKS))
    rechts = "".join(zeile(a, e, i >= 3) for i, (a, e) in enumerate(RECHTS))
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:30px"><div>{links}</div><div>{rechts}</div></div>'


# Auftrag oben auf jeder Übungsseite (Oskar, 05.10.2026): kein Merkheft/Rezept wiederholen, sondern sagen, was am Stück zu tun ist,
# darunter die Aufgaben zum Besprechen, und immer eine Aufgabe für Schnelle.
def auftrag(was, schnelle):
    return (f'<div class="auftrag"><div><b>Aufgabe:</b> {was}</div>'
            f'<div><b>Für Schnelle:</b> {schnelle}</div><div class="auftrag-k">Merkheft aufgeschlagen daneben legen.</div></div>')


# Schnelle-Aufgaben aus dem Buch (abgetippt, Lösungen geprüft)
S28_4 = [("(−12) · (+3)", -36, "K"), ("(−7) · (−9)", 63, "A"), ("(−8) · (+4)", -32, "N"), ("(−3) · (−12)", 36, "A"), ("(+9) · (−7)", -63, "D"), ("(−4) · (−8)", 32, "A")]
for _a, _e, _b in S28_4:
    assert wert(_a) == _e, _a
assert "".join(b for _, _, b in S28_4) == "KANADA"
from fractions import Fraction as _F
S28_4R = [("(−1/2) · 1/3", _F(-1, 6), "−1/6"), ("1/2 · (−4/5)", _F(-2, 5), "−2/5"), ("(−1/3) · (−3/4)", _F(1, 4), "1/4"), ("(−5/8) · (−24/10)", _F(3, 2), "3/2")]
for _a, _e, _t in S28_4R:
    assert abs(wert(_a) - float(_e)) < 1e-9, _a
S28_7R = [("(−2) · (−2)", 4), ("(−2) · (−2) · (−2)", -8), ("(−2) · (−2) · (−2) · (−2)", 16)]
for _a, _e in S28_7R:
    assert wert(_a) == _e, _a
assert (-2) ** 10 == 1024


def schnell_kanada(l):
    items = "".join(f"<li>{a} = {L(zahl(e) + ' ' + b) if l else ''}</li>" for a, e, b in S28_4)
    return (f'<ol type="a" class="ex raster" style="{raster_stil([a + " = −63 D" for a, _, _ in S28_4], G - 4)}">{items}</ol>'
            + (f'<p style="font-size:18px">Lösungswort: {L("KANADA")}</p>' if l else ""))


def schnell_brueche(l):
    items = "".join(f"<li>{a} = {L(t) if l else ''}</li>" for a, _, t in S28_4R)
    return f'<ol type="a" class="ex raster" style="{raster_stil([a + " = −2/5" for a, _, _ in S28_4R], G)}">{items}</ol>'


def schnell_reihe(l):
    items = "".join(f"<li>{a} = {L(zahl(e)) if l else ''}</li>" for a, e in S28_7R)
    rest = (f'<p style="font-size:18px">b) 10 Faktoren: {L("1024")}; c) gerade Anzahl Minus: {L("positiv")}, ungerade: {L("negativ")}</p>' if l else
            '<p style="font-size:18px">b) Setze bis 10 Faktoren fort. c) Wann ist das Ergebnis positiv, wann negativ?</p>')
    return f'<ol type="a" class="ex raster" style="{raster_stil([a + " = 16" for a, _ in S28_7R], G)}">{items}</ol>' + rest


def seite_wdh(l):
    return (auftrag("Übungsheft, alle 14 Aufgaben, erst ○, dann ◐.", "Buch S. 26 Nr. 8 (rechts), Jede Menge Minuszeichen")
            + UEB(block("○ Zwei Zahlen in der Minusklammer", mk_liste(MK_O, l))
                  + block("◐ Jetzt mit negativen Zahlen und Kommazahlen", mk_liste(MK_M, l))
                  + block("Für Schnelle: Buch S. 26 Nr. 8 (rechts)", spalten(S26_8, l, gross=G))))


def seite_muster(l):
    return (block("Buch S. 27: Wie geht es weiter?", muster(l))
            + ('<p style="font-size:20px">Links jedes Mal 8 weniger, rechts jedes Mal 16 mehr. Gleiche Vorzeichen: Plus. Verschiedene: Minus.</p>'
               + HEFT(MERK_M) if l else '<p style="font-size:22px">Wovon hängt das Vorzeichen des Ergebnisses ab?</p>'))


def seite_uebung1(l):
    s27_1 = (spalten(S27_1, l, gross=G) if not l else
             '<ol type="a" class="ex raster" style="' + raster_stil(S27_1_L, G) + '">' + "".join(f"<li>{L(x)}</li>" for x in S27_1_L) + "</ol>")
    return (auftrag("Übungsheft, Buch S. 27 Nr. 1, Nr. 2 und S. 28 Nr. 3.", "Buch S. 28 Nr. 4, das Lösungswort")
            + UEB(block("Buch S. 27 Nr. 1: Schreibe als Produkt und berechne.", s27_1)
                  + block("Buch S. 27 Nr. 2: Berechne im Kopf.", spalten(S27_2, l, gross=G))
                  + block("Buch S. 28 Nr. 3: Ergänze das fehlende Vorzeichen.", ergaenze_a4(S28_3, l))
                  + block("Für Schnelle: Buch S. 28 Nr. 4 (Lösungswort)", schnell_kanada(l))))


def seite_uebung2(l):
    return (auftrag("Übungsheft, Buch S. 28 Alles klar? A und B, dann S. 28 Nr. 3 (rechts).", "Buch S. 28 Nr. 4 (rechts), Brüche")
            + UEB(block("Buch S. 28 Alles klar? A: Ergänze das fehlende Vorzeichen.", ergaenze_a4(S28_A, l))
                  + block("Alles klar? B: Erst ohne Vorzeichen multiplizieren, dann das Vorzeichen setzen.", spalten(S28_B, l, gross=G))
                  + block("◐ Buch S. 28 Nr. 3 (rechts): Dezimalzahlen", spalten(S28_3D, l, gross=G))
                  + block("Für Schnelle: Buch S. 28 Nr. 4 (rechts)", schnell_brueche(l))))


def seite_exit(l):
    """Puffer-Seite (Oskar: nur wenn Zeit bleibt). Die Schüler sehen sie, deshalb kein „Exit-Ticket“ und kein „Puffer“ darauf."""
    return (auftrag("Übungsheft, Buch S. 28 Nr. 7, danach die Aufgaben unten.", "Buch S. 28 Nr. 7 (rechts), die Reihe mit (−2)")
            + UEB(block("Buch S. 28 Nr. 7: mehrere Faktoren, immer zwei nacheinander", spalten(S28_7, l, gross=G))
                  + block("Für Schnelle: Buch S. 28 Nr. 7 (rechts)", schnell_reihe(l))
                  + block("Weitere Aufgaben", spalten(EXIT, l, gross=G))
                  + block("Hausaufgabe: Buch S. 28 Nr. 5 (schriftlich)", spalten(S28_5, l, gross=G))))


SEITEN = [("Whiteboards", seite_wb), ("1 Wiederholung Minusklammer", seite_wdh), ("2 Multiplizieren: Wie geht es weiter?", seite_muster),
          ("3 Übung 1", seite_uebung1), ("4 Übung 2", seite_uebung2), ("5 Weitere Aufgaben und Hausaufgabe", seite_exit)]
FOLIEN = [x for t, f in SEITEN for x in ((t, f(False)), (f"{t}: ausgefüllt", f(True)))]
QUER = {"Whiteboards", "Whiteboards: ausgefüllt"}       # diese Seiten als Querfolie, der Rest A4 hochkant
A4 = True        # export_icloud_mathe.py baut daraus A4-Seiten statt Beamer-Folien

SCHRITTE = [
    ("", "Whiteboards: 5 Aufgaben", 8, "Eine Querfolie, die anderen Aufgaben mit dem Pflaster abdecken. Auf „Alle hoch“ zeigen alle gleichzeitig.", [1, 2]),
    ("", "Wiederholung Minusklammer", 15, "14 Aufgaben mit zwei Zahlen in der Minusklammer, Schnelle: S. 26 Nr. 8 rechts.", [3, 4]),
    ("", "Wie geht es weiter?", 8, "Beide Reihen von S. 27 fortsetzen lassen. Frage: Wovon hängt das Vorzeichen ab?", [5]),
    ("", "Merkheft: Multiplizieren", 8, "Steht auf der ausgefüllten Seite 2: Beispiel links, Rezept rechts, weitere Beispiele. Abschreiben.", [6]),
    ("", "Übung 1 ○", 20, "S. 27 Nr. 1, 2 und S. 28 Nr. 3, Schnelle: S. 28 Nr. 4 (KANADA). Merkheft offen.", [7, 8]),
    ("", "Übung 2 ○◐", 15, "Alles klar A und B, S. 28 Nr. 3 rechts, Schnelle: Nr. 4 rechts (Brüche).", [9, 10]),
    ("", "Puffer und Hausaufgabe", 16, "Nur wenn Zeit bleibt: S. 28 Nr. 7 und die weiteren Aufgaben. Sonst direkt die Hausaufgabe S. 28 Nr. 5.", [11, 12]),
]
assert sum(m for _, _, m, _, _ in SCHRITTE) == 90


def main():
    bau_woche(HIER / f"{NAME}.html", "Woche 4, Stunde 1: Wiederholung Minusklammer, Multiplizieren",
              "Klasse 7c, Mathematik, Di 06.10.2026, Doppelstunde, Buch S. 27 und 28",
              [("Drucken", "Nichts."), ("Digital", f"Folien-PDF in Notability: {NAME}.pdf (iCloud, 04 Rationale Zahlen)."),
               ("Sonst", "Mini-Whiteboards und Stifte austeilen. Buch mitbringen lassen. Dividieren kommt in der nächsten Stunde.")],
              SCHRITTE, FOLIEN,
              tafel=box("Erinnerung: Merkheft Minusklammer", MERK_MK) + box("Wie geht es weiter? (Buch S. 27)", MUSTER_L + ADDITION)
              + box("Tafelbild = Merkheft: Multiplizieren", MERK_M),
              merkheft=box("Multiplizieren", HEFT(MERK_M)),
              loesungen=box("Wiederholung Minusklammer", mk_liste(MK_O, True) + mk_liste(MK_M, True))
              + box("S. 27 Nr. 1", "<ol type='a' class='ex'>" + "".join(f"<li>{L(x)}</li>" for x in S27_1_L) + "</ol>")
              + box("S. 27 Nr. 2", spalten(S27_2, True)) + box("S. 28 Nr. 3", ergaenze(S28_3, True))
              + box("S. 28 Alles klar A und B", ergaenze(S28_A, True) + spalten(S28_B, True)) + box("S. 28 Nr. 3 rechts", spalten(S28_3D, True))
              + box("S. 28 Nr. 7", spalten(S28_7, True, n=1)) + box("Weitere Aufgaben (Puffer)", spalten(EXIT, True, n=1)) + box("Hausaufgabe S. 28 Nr. 5", spalten(S28_5, True)),
              extra_css=EXTRA_CSS, verlauf="Die Doppelstunde")


if __name__ == "__main__":
    main()
