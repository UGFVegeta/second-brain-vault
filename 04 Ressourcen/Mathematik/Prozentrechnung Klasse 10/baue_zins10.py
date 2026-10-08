#!/usr/bin/env python3
"""Mathe 10b, Woche 4 (05. bis 09.10.2026, Montag Ausflug). Schwerpunkt Zinseszins, Zinsen nur kompakt (Oskar, 04.10.2026).
Mi (Doppelstunde): Zinsen kurz (Jahres-, Monats-, Tageszinsen in einem Merkheft-Bild, eine Runde), dann Zinseszins mit Oskars
Einstieg (1 € im Jahr 0 zu 2 %, Erbe 2026, schätzen), Endkapital und Anfangskapital.
Fr (Einzelstunde): Zinssatz gesucht (n-te Wurzel), gemischte Runde.
Rezept-Stil: Merkheft-Bild = Beispiel links mit Schrittnummern, Rezept rechts; Runden mit Buchaufgaben als Originalausschnitt
(Oskars Buchfotos S. 86 bis 90, Ordner „Buchausschnitte Zinsen“), Rezept daneben. Schreibweise wie im Buch:
Z = K · p %, Z = K · p % · t/360 (1 Monat = 30 Tage), q = 1 + p/100, Kₙ = K₀ · qⁿ.
Alle Lösungen werden hier berechnet und mit assert geprüft. Nur HTML, Folien-PDF erst nach Freigabe.
Aufruf: python3 baue_zins10.py"""
import re, sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER.parent / "Rationale Zahlen"))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_woche7 import merkbild, rezept_box, HEFT, UEB, box, EXTRA_CSS, raster_stil, LUECKE, LUECKE_LANG  # noqa: E402

NB = " "
BUCH = "Buchausschnitte Zinsen"


def zahl(x, nachkomma=None):
    """Deutsche Schreibweise: Leerzeichen als Tausendertrenner, Komma; ganze Beträge ohne ,00."""
    x = round(x + 1e-9, 2)
    if nachkomma is None:
        nachkomma = 0 if x == int(x) else 2
    return f"{x:,.{nachkomma}f}".replace(",", " ").replace(".", ",").replace(" ", NB)


def genau(x, n):
    """Ohne vorheriges Runden auf Cent, n Nachkommastellen, nachgestellte Nullen weg."""
    return f"{x:.{n}f}".rstrip("0").rstrip(".").replace(".", ",")


cent = lambda x: f"{zahl(x, 2)}{NB}€"
L = lambda x: f'<span class="lsg">{x}</span>'
r2 = lambda x: round(x + 1e-9, 2)
tag = lambda k, p, t: k * p / 100 * t / 360          # Buch: Z = K · p % · t/360


G = lambda x: LUECKE_LANG if x == "" else x      # Lücke als leeres Kästchen zum Reinschreiben


def tabelle(kopf, zeilen):
    return ('<table class="ha" style="font-size:24px;text-align:center"><tr><td></td>' + "".join(f"<td><b>{k}</b></td>" for k in kopf) + "</tr>"
            + "".join(f'<tr><td style="text-align:left"><b>{n}</b></td>' + "".join(f"<td>{G(x)}</td>" for x in werte) + "</tr>" for n, werte in zeilen) + "</table>")


def abc(liste, spalten=2):
    """Aufgaben im Raster, keine Aufgabe bricht um."""
    return f'<ol type="a" class="ex raster" style="{raster_stil(liste, 28)}">' + "".join(f"<li>{x}</li>" for x in liste) + "</ol>"


# Buchaufgaben abgetippt (Oskar, 05.10.2026: keine Bildausschnitte, die sind auf dem Beamer unscharf)
TEXT = {
    "S86 Einstieg Ethan": (f'<div style="font-size:26px;line-height:1.5"><p>Ethan will 1{NB}200{NB}€ für ein Jahr anlegen. Er hat drei Angebote:</p>'
                           f'<ul><li>Sein Vater zahlt ihm nach einem Jahr 1{NB}215{NB}€ zurück.</li><li>Die Bank zahlt 0,5{NB}% Zinsen.</li>'
                           f'<li>Eine riskantere Anlage in britischen Pfund lässt 1,4{NB}% Zuwachs erwarten.</li></ul>'
                           '<p><b>Berechne für alle drei Angebote, wie viel Geld Ethan nach einem Jahr hat. Wofür würdest du dich entscheiden?</b></p></div>'),
    "S86 Nr1": "<p><b>S. 86 Nr. 1</b> Berechne die Zinsen für den angegebenen Zeitraum.</p>" + abc(
        [f"K = 590{NB}€; p % = 6{NB}%; t = 1 Jahr", f"K = 4{NB}200{NB}€; p % = 0,9{NB}%; t = 1 Jahr", f"K = 2{NB}500{NB}€; p % = 2,4{NB}%; t = 81 Tage",
         f"K = 3{NB}850{NB}€; p % = 8,9{NB}%; t = 72 Tage", f"K = 15{NB}000{NB}€; p % = 1,3{NB}%; t = 4 Monate"], 1),
    "S87 A": "<p><b>S. 87 A</b> Berechne den fehlenden Wert.</p>" + tabelle("abcde", [
        ("Kapital", [f"2{NB}000{NB}€", f"24{NB}600{NB}€", "", f"17{NB}500{NB}€", f"6{NB}800{NB}€"]),
        ("Zinssatz", [f"1,2{NB}%", "", f"9,9{NB}%", "", f"0,8{NB}%"]),
        ("Zeitraum", ["5 Monate", "81 Tage", "28 Tage", "18 Tage", ""]),
        ("Zinsen", ["", f"66,42{NB}€", f"98,56{NB}€", f"77,00{NB}€", f"10,88{NB}€"])]),
    "S87 B": f"<p><b>S. 87 B</b> Herr Klein überzieht sein Girokonto 12 Tage um 3{NB}200{NB}€. Der Zinssatz liegt bei 12{NB}%. Wie viel Zinsen zahlt er?</p>",
    "S89 Nr1-2": ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:30px"><div><p><b>S. 89 Nr. 1</b> Bestimme q.</p>'
                  + abc([f"p % = 3{NB}%", f"p % = 2,8{NB}%", f"p % = 12,5{NB}%", f"p % = 0,8{NB}%"]) + '</div><div><p><b>Nr. 2</b> Bestimme p %.</p>'
                  + abc(["q = 1,09", "q = 1,025", "q = 1,158", "q = 1,007"]) + "</div></div>"),
    "S89 Nr3": "<p><b>S. 89 Nr. 3</b> Berechne das Endkapital.</p>" + abc(
        [f"K₀ = 7{NB}000{NB}€; p % = 1,6{NB}%; 5 Jahre", f"K₀ = 2{NB}500{NB}€; p % = 1,3{NB}%; 8 Jahre",
         f"K₀ = 20{NB}000{NB}€; p % = 2,4{NB}%; 4 Jahre", f"K₀ = 20{NB}000{NB}€; p % = 3,6{NB}%; 4 Jahre"], 1),
    "S89 Nr4": "<p><b>S. 89 Nr. 4</b> Berechne, welches Anfangskapital angelegt wurde.</p>" + abc(
        [f"p % = 1,2{NB}%; 3 Jahre; K₃ = 518,22{NB}€", f"p % = 1,1{NB}%; 8 Jahre; K₈ = 2{NB}182,93{NB}€", f"p % = 0,9{NB}%; 5 Jahre; K₅ = 8{NB}889,45{NB}€"], 1),
    "S89 Nr6-7 links": (f'<p class="gross"><b>S. 89 Nr. 6</b> Berechne den fehlenden Wert: K₀ = 3{NB}750{NB}€; p % = 0,9{NB}%; n = 5 Jahre</p>'
                        f'<p class="gross"><b>Nr. 7</b> Frau Mai legt 5{NB}000{NB}€ zu 1,3{NB}% für sechs Jahre an. Wie viel hat sie dann?</p>'),
    "S89 Nr6-7 rechts": (f'<p class="gross"><b>S. 89 ◐6</b> Berechne den fehlenden Wert: K₀ = 5{NB}500{NB}€; K₁₂ = 6{NB}422,08{NB}€</p>'
                         f'<p class="gross"><b>◐7</b> Max legt 12{NB}000{NB}€ an. Nach 5 Jahren erhält er 12{NB}991,22{NB}€. Zu welchem Zinssatz?</p>'),
    "S89 Nr5": "<p><b>S. 89 Nr. 5</b> Berechne den Zinsfaktor, bestimme den Zinssatz. Die Laufzeit beträgt jeweils 8 Jahre.</p>" + abc(
        [f"K₀ = 1{NB}500,00{NB}€; Kₙ = 1{NB}598,73{NB}€", f"K₀ = 1{NB}800,00{NB}€; Kₙ = 1{NB}980,23{NB}€",
         f"K₀ = 36{NB}000,00{NB}€; Kₙ = 41{NB}522,62{NB}€", f"K₀ = 55{NB}000,00{NB}€; Kₙ = 66{NB}948,43{NB}€"], 1),
    "S89 A": "<p><b>S. 89 A</b> Berechne die fehlenden Größen.</p>" + tabelle("abcde", [
        ("K₀", [f"900,00{NB}€", f"3{NB}000,00{NB}€", "", "", f"820{NB}000,00{NB}€"]), ("p %", ["", f"1,4{NB}%", "", f"1,35{NB}%", ""]),
        ("q", ["1,012", "", "1,022", "", ""]), ("n", ["12 Jahre", "8 Jahre", "9 Jahre", "9 Jahre", "5 Jahre"]),
        ("Kₙ", ["", "", f"18{NB}853,40{NB}€", f"75{NB}594,22{NB}€", f"923{NB}237,92{NB}€"])]),
    "S90 Nr8": (f'<p class="gross"><b>S. 90 Nr. 8</b> Herr Bleul verspricht seinem Sohn, ihm nach 5 Jahren 10{NB}000{NB}€ zu schenken. '
                f'Welchen Betrag muss er jetzt anlegen, wenn das Geld mit 1,1{NB}% verzinst wird?</p>'),
    "S90 Nr10": (f'<p class="gross"><b>S. 90 Nr. 10</b> Zum 18. Geburtstag bekommt Aylin einen Sparbrief über 2{NB}823,71{NB}€. Der Zinssatz beträgt 1,6{NB}%.</p>'
                 '<ol type="a" class="ex" style="font-size:26px"><li>Der Sparbrief wurde vor 4 Jahren mit einer einmaligen Zahlung angelegt. Berechne das Anfangskapital.</li>'
                 f'<li>Aylin möchte für eine Reise 3{NB}000{NB}€ haben. Es gibt keine Ein- oder Auszahlungen. Nach wie vielen Jahren kann sie fahren? Probiere.</li></ol>'),
}


def bild(name, breite=None):
    """Früher Bildausschnitt, jetzt der abgetippte Aufgabentext (Name bleibt als Schlüssel)."""
    return f'<div style="margin:0 0 14px">{TEXT[name]}</div>'


def runde(titel, bilder, rezept=None):
    """Runde: abgetippte Buchaufgaben links, Rezept als Kasten daneben."""
    inhalt = f'<h4>{titel}</h4>{"".join(bilder)}'
    return f'<div class="mit"><div>{inhalt}</div>{rezept}</div>' if rezept else inhalt


def liste(zeilen, klein=False):
    """Aufzählung a), b) …; haben die Zeilen schon eigene Nummern (z. B. „6)“, „a)“), dann ohne zusätzliche Buchstaben."""
    eigene = all(re.match(r"^(◐|●)?\d*\s?[a-e]?\)", z) for z in zeilen)
    stil = ("font-size:20px;" if klein else "") + ("list-style:none;padding-left:0;" if eigene else "")
    return f'<ol type="a" class="ex" style="{stil}">' + "".join(f"<li>{z}</li>" for z in zeilen) + "</ol>"


# ================================================================ Zinsen (kompakt)
assert 1215 - 1200 == 15 and 15 / 1200 == 0.0125 and r2(1200 * 0.005) == 6 and r2(1200 * 0.014) == 16.8
ETHAN_L = (f'<div class="ausdruck">Vater: 15{NB}€ mehr, das sind 1,25{NB}%</div>'
           f'<div class="ausdruck">Bank: 1{NB}200 · 0,005 = {L("6 €")}</div>'
           f'<div class="ausdruck">Pfund: 1{NB}200 · 0,014 = {L("16,80 €")} (aber Risiko)</div>'
           '<p class="gross">Neue Namen: Grundwert = <b>Kapital K</b>, Prozentwert = <b>Zinsen Z</b>, Prozentsatz = <b>Zinssatz p %</b></p>')

REZ_J = ["K, p % und t herausschreiben. 1 Monat = 30 Tage, 1 Jahr = 360 Tage.",
         "Ein Jahr: Z = K · p %. Weniger: Z = K · p % · t/360",
         "K, p % oder t gesucht? Einsetzen und teilen.", "Ausrechnen, Antwortsatz."]
MERK_J = merkbild("Zinsen", [
    [(1, f'<span class="txt">K = 1{NB}200{NB}€; p % = 2,5{NB}%; t = 1 Jahr</span>'),
     (2, '<span class="txt">Z = K · p % =</span> 1200 · 0,025'), (4, f'= <b>30</b><span class="txt">{NB}€</span>')],
    [(1, f'<span class="txt">K = 3{NB}600{NB}€; p % = 2{NB}%; t = 75 Tage</span>'),
     (2, '<span class="txt">Z = K · p % · t/360 =</span> 3600 · 0,02 · 75 : 360'), (4, f'= <b>15</b><span class="txt">{NB}€</span>')],
], REZ_J)
RZ_J = rezept_box("Zinsen", REZ_J)

N1 = [(590, 6, 360), (4200, 0.9, 360), (2500, 2.4, 81), (3850, 8.9, 72), (15000, 1.3, 120)]
N1_Z = [r2(tag(k, p, t)) for k, p, t in N1]
assert N1_Z == [35.4, 37.8, 13.5, 68.53, 65]
N1_L = [f"{zahl(k)} · {genau(p / 100, 4)}{'' if t == 360 else f' · {t} : 360'} = {L(cent(z))}" for (k, p, t), z in zip(N1, N1_Z)]
N1_L[4] += " (4 Monate = 120 Tage)"
A = [tag(2000, 1.2, 150), 66.42 * 360 / (24600 * 81), 98.56 * 360 / (0.099 * 28), 77 * 360 / (17500 * 18), 10.88 * 360 / (6800 * 0.008)]
assert r2(A[0]) == 10 and r2(A[1] * 100) == 1.2 and r2(A[2]) == 12800 and r2(A[3] * 100) == 8.8 and r2(A[4]) == 72 and r2(tag(3200, 12, 12)) == 12.8
A_L = [f"Z = 2{NB}000 · 0,012 · 150 : 360 = {L('10,00 €')}", f"p % = 66,42 · 360 : (24{NB}600 · 81) = {L('1,2 %')}",
       f"K = 98,56 · 360 : (0,099 · 28) = {L('12 800 €')}", f"p % = 77 · 360 : (17{NB}500 · 18) = {L('8,8 %')}",
       f"t = 10,88 · 360 : (6{NB}800 · 0,008) = {L('72 Tage')}"]
B_L = f"B) 3{NB}200 · 0,12 · 12 : 360 = {L('12,80 €')}"

# ================================================================ Zinseszins: Endkapital und Anfangskapital
ERBE, EINFACH = 1.02 ** 2026, 1 + 2026 * 0.02
PRO_MENSCH = ERBE / 8e9
assert r2(EINFACH) == 41.52 and 2.65e17 < ERBE < 2.66e17 and 3.3e7 < PRO_MENSCH < 3.4e7
assert [round(1.02 ** j, 6) for j in range(4)] == [1, 1.02, 1.0404, 1.061208]
TAB = [(j, 1.02 ** j, 1.02 ** (j - 1) * 0.02 if j else None) for j in range(4)]
TAB_HTML = ('<table class="ha" style="font-size:22px;max-width:640px"><tr><td><b>Jahr</b></td><td><b>Zinsen (2 %)</b></td><td><b>Kontostand</b></td></tr>'
            + "".join(f"<tr><td>{j}</td><td>{'' if z is None else genau(z, 6) + NB + '€'}</td><td>{genau(k, 6) if j else '1,00'}{NB}€</td></tr>"
                      for j, k, z in TAB) + "</table>")

REZ_Z = ["K₀, p %, n und Kₙ herausschreiben: Was ist gesucht?", "Zinsfaktor q = 1 + p/100",
         "Kₙ gesucht: Kₙ = K₀ · qⁿ. K₀ gesucht: K₀ = Kₙ : qⁿ", "Taschenrechner, auf Cent runden."]
MERK_Z = merkbild("Zinseszins", [
    [(1, f'<span class="txt">K₀ = 2{NB}000{NB}€; p % = 2{NB}%; n = 3; gesucht: K₃</span>'), (2, '<span class="txt">q = 1 + 2/100 = 1,02</span>'),
     (3, '<span class="txt">K₃ = K₀ · q³ =</span> 2000 · 1,02<sup>3</sup>'), (4, f'≈ <b>2122,42</b><span class="txt">{NB}€</span>')],
    [(1, f'<span class="txt">K₃ = 2{NB}122,42{NB}€; p % = 2{NB}%; n = 3; gesucht: K₀</span>'), (2, '<span class="txt">q = 1,02</span>'),
     (3, '<span class="txt">K₀ = K₃ : q³ =</span> 2122,42 : 1,02<sup>3</sup>'), (4, f'≈ <b>2000</b><span class="txt">{NB}€</span>')],
], REZ_Z)
RZ_Z = rezept_box("Zinseszins", REZ_Z)

NR1_L = [f"3 %: q = {L('1,03')}", f"2,8 %: q = {L('1,028')}", f"12,5 %: q = {L('1,125')}", f"0,8 %: q = {L('1,008')}"]
NR2_L = [f"q = 1,09: {L('9 %')}", f"1,025: {L('2,5 %')}", f"1,158: {L('15,8 %')}", f"1,007: {L('0,7 %')}"]
NR3 = [(7000, 1.6, 5), (2500, 1.3, 8), (20000, 2.4, 4), (20000, 3.6, 4)]
NR3_E = [r2(k * (1 + p / 100) ** n) for k, p, n in NR3]
assert NR3_E == [7578.21, 2772.14, 21990.23, 23039.29]
NR3_L = [f"{zahl(k)} · {genau(1 + p / 100, 4)}<sup>{n}</sup> ≈ {L(cent(e))}" for (k, p, n), e in zip(NR3, NR3_E)]
NR4 = [(518.22, 1.2, 3), (2182.93, 1.1, 8), (8889.45, 0.9, 5)]
NR4_E = [r2(kn / (1 + p / 100) ** n) for kn, p, n in NR4]
assert NR4_E == [500, 2000, 8500]
NR4_L = [f"K₀ = {zahl(kn)} : {genau(1 + p / 100, 4)}<sup>{n}</sup> ≈ {L(cent(e))}" for (kn, p, n), e in zip(NR4, NR4_E)]
HA_MI = [r2(3750 * 1.009 ** 5), r2(5000 * 1.013 ** 6)]
assert HA_MI == [3921.81, 5402.9]
HA_MI_L = [f"6) K₅ = 3{NB}750 · 1,009<sup>5</sup> ≈ {L('3 921,81 €')}", f"7) K₆ = 5{NB}000 · 1,013<sup>6</sup> ≈ {L('5 402,90 €')}"]

# ================================================================ Freitag: Zinssatz gesucht
REZ_P = ["K₀, Kₙ und n herausschreiben.", "qⁿ = Kₙ : K₀", "q = n-te Wurzel daraus (Taschenrechner).", "p % = (q − 1) · 100"]
assert abs((5412.16 / 5000) ** 0.25 - 1.02) < 1e-6
MERK_P = merkbild("Zinssatz gesucht", [
    (1, f'<span class="txt">K₀ = 5{NB}000{NB}€; K₄ = 5{NB}412,16{NB}€; n = 4</span>'),
    (2, '<span class="txt">q⁴ = 5 412,16 : 5 000 = 1,082432</span>'),
    (3, '<span class="txt">q = ⁴√1,082432 ≈</span> 1,02'),
    (4, '<span class="txt">p % = (1,02 − 1) · 100 = 2 %</span>')], REZ_P)
RZ_P = rezept_box("Zinssatz gesucht", REZ_P)
NR5 = [(1500, 1598.73), (1800, 1980.23), (36000, 41522.62), (55000, 66948.43)]
NR5_Q = [(kn / k0) ** (1 / 8) for k0, kn in NR5]
assert [round(q, 3) for q in NR5_Q] == [1.008, 1.012, 1.018, 1.025]
NR5_L = [f"q = ⁸√({zahl(kn)} : {zahl(k0)}) ≈ {genau(q, 4)}; p % ≈ {L(genau((q - 1) * 100, 2) + ' %')}" for (k0, kn), q in zip(NR5, NR5_Q)]
AK = [r2(900 * 1.012 ** 12), r2(3000 * 1.014 ** 8), r2(18853.40 / 1.022 ** 9), r2(75594.22 / 1.0135 ** 9)]
assert AK == [1038.51, 3352.93, 15500, 67000] and abs((923237.92 / 820000) ** (1 / 5) - 1.024) < 1e-6
AK_L = [f"a) p % = 1,2 %; K₁₂ = 900 · 1,012<sup>12</sup> ≈ {L('1 038,51 €')}", f"b) q = 1,014; K₈ = 3{NB}000 · 1,014<sup>8</sup> ≈ {L('3 352,93 €')}",
        f"c) p % = 2,2 %; K₀ = 18{NB}853,40 : 1,022<sup>9</sup> ≈ {L('15 500 €')}", f"d) q = 1,0135; K₀ = 75{NB}594,22 : 1,0135<sup>9</sup> ≈ {L('67 000 €')}",
        f"e) q = ⁵√(923{NB}237,92 : 820{NB}000) ≈ 1,024; p % = {L('2,4 %')}"]
RE67 = [(6422.08 / 5500) ** (1 / 12), (12991.22 / 12000) ** (1 / 5)]
assert [round(q, 4) for q in RE67] == [1.013, 1.016]
RE67_L = [f"◐6) q = ¹²√(6{NB}422,08 : 5{NB}500) ≈ 1,013; p % = {L('1,3 %')}", f"◐7) q = ⁵√(12{NB}991,22 : 12{NB}000) ≈ 1,016; p % = {L('1,6 %')}"]
HA8, HA10A = 10000 / 1.011 ** 5, 2823.71 / 1.016 ** 4
HA10B = next(n for n in range(1, 30) if 2823.71 * 1.016 ** n >= 3000)
assert r2(HA8) == 9467.69 and r2(HA10A) == 2650 and HA10B == 4
HA_FR_L = [f"8) K₀ = 10{NB}000 : 1,011<sup>5</sup> ≈ {L('9 467,69 €')}", f"10 a) K₀ = 2{NB}823,71 : 1,016<sup>4</sup> ≈ {L('2 650,00 €')}",
           f"10 b) nach 3 Jahren 2{NB}961,43{NB}€, nach 4 Jahren 3{NB}008,81{NB}€: {L('nach 4 Jahren')}"]

# ================================================================ Folien und Verlauf
FOLIEN_MI = [
    ("Ethan will 1 200 € anlegen (Buch S. 86)", bild("S86 Einstieg Ethan", "62%")),
    ("Ethan: Lösung", ETHAN_L),
    ("Merkheft: Zinsen", HEFT(MERK_J)),
    ("Zinsen üben", UEB(runde("Buch S. 86 Nr. 1 und S. 87 Alles klar? A, B", [bild("S86 Nr1"), bild("S87 B")], RZ_J))),
    ("Zinsen üben: Alles klar A", UEB(runde("Buch S. 87 Alles klar? A", [bild("S87 A")]))),
    ("Zinsen: Lösungen", liste(N1_L, klein=True) + liste(A_L, klein=True) + f"<p>{B_L}</p>"),
    ("Ein Euro im Jahr 0", f'<p class="gross">Im Jahr 0 legt jemand 1{NB}€ zu 2{NB}% Zinsen an.<br>Seine Nachkommen erben das Geld im Jahr 2026.</p>'
                           '<p class="gross"><b>Schätze: Wie viel Geld ist es?</b> Schreib deine Schätzung ins Übungsheft.</p>'),
    ("Mit den Zinsen von eben", f'<div class="ausdruck">Jedes Jahr: 1 · 0,02 = 0,02{NB}€</div>'
                                f'<div class="ausdruck">2026 Jahre: 1 + 2026 · 0,02 = {L(cent(EINFACH))}</div><p class="gross">Stimmt das?</p>'),
    ("Die Zinsen bekommen auch Zinsen", TAB_HTML + '<p class="gross">Was passiert jedes Jahr mit dem Kontostand?</p>'),
    ("Merkheft: Zinseszins", HEFT(MERK_Z)),
    ("Runde 1", UEB(runde("○ Buch S. 89 Nr. 1 und 2 (im Kopf)", [bild("S89 Nr1-2")], RZ_Z))),
    ("Runde 1: Lösungen", liste(NR1_L) + liste(NR2_L)),
    ("Runde 2", UEB(runde("○ Buch S. 89 Nr. 3", [bild("S89 Nr3")], RZ_Z))), ("Runde 2: Lösungen", liste(NR3_L)),
    ("Runde 3", UEB(runde("◐ Buch S. 89 Nr. 4", [bild("S89 Nr4")], RZ_Z))), ("Runde 3: Lösungen", liste(NR4_L)),
    ("Auflösung: das Erbe", f'<div class="ausdruck">1 · 1,02<sup>2026</sup> ≈ {L("265 000 000 000 000 000 €")}</div>'
                            '<p class="gross">Das sind 265 Billiarden Euro. Bei 8 Milliarden Menschen bekäme jeder rund 33 Millionen Euro.</p>'
                            '<p class="gross">Ohne Zinseszins: 41,52 €. Warum gibt es diese Erben trotzdem nicht?</p>'),
    ("Hausaufgabe: Buch S. 89 Nr. 6 und 7 (links)", UEB(bild("S89 Nr6-7 links"))),
    ("Hausaufgabe: Lösungen", liste(HA_MI_L)),
]
SCHRITTE_MI = [
    ("", "Zinsen: Ethan (S. 86)", 6, "Mit Prozentwissen lösen, dann die neuen Namen.", [1, 2]),
    ("", "Merkheft: Zinsen", 6, "Ein Bild für Jahres-, Monats- und Tageszinsen.", [3]),
    ("", "Zinsen üben", 13, "S. 86 Nr. 1, S. 87 A und B. Mehr nicht.", [4, 5, 6]),
    ("", "Zinseszins: schätzen", 5, "1 € im Jahr 0, Erbe 2026. Jeder schreibt eine Zahl auf.", [7]),
    ("", "Mit einfachen Zinsen", 3, "41,52 €. Kurz stehen lassen.", [8]),
    ("", "Jahr für Jahr", 7, "Tabelle gemeinsam füllen. Ziel: jedes Jahr mal 1,02.", [9]),
    ("", "Merkheft: Zinseszins", 10, "Endkapital und Anfangskapital, Beispiel links, Rezept rechts.", [10]),
    ("", "Runde 1 ○", 6, "S. 89 Nr. 1 und 2 im Kopf.", [11, 12]),
    ("", "Runde 2 ○", 13, "S. 89 Nr. 3, Taschenrechner.", [13, 14]),
    ("", "Runde 3 ◐", 13, "S. 89 Nr. 4, K₀ gesucht.", [15, 16]),
    ("", "Auflösung und Hausaufgabe", 8, "Erbe ausrechnen, mit den Schätzungen vergleichen. HA: S. 89 Nr. 6 und 7 links.", [17, 18, 19]),
]
assert sum(m for _, _, m, _, _ in SCHRITTE_MI) == 90

FOLIEN_FR = [
    ("Hausaufgabe: Lösungen", liste(HA_MI_L)),
    ("Merkheft: Zinssatz gesucht", HEFT(MERK_P)),
    ("Runde 1", UEB(runde("◐ Buch S. 89 Nr. 5", [bild("S89 Nr5")], RZ_P))), ("Runde 1: Lösungen", liste(NR5_L)),
    ("Runde 2: alles gemischt", UEB(runde("Buch S. 89 Alles klar? A (Merkheft offen lassen)", [bild("S89 A")]))), ("Runde 2: Lösungen", liste(AK_L)),
    ("Runde 3", UEB(runde("● Buch S. 89 Nr. 6 und 7 (rechts)", [bild("S89 Nr6-7 rechts")], RZ_P))), ("Runde 3: Lösungen", liste(RE67_L)),
    ("Hausaufgabe: Buch S. 90 Nr. 8 und 10", UEB(bild("S90 Nr8") + bild("S90 Nr10"))),
    ("Hausaufgabe: Lösungen", liste(HA_FR_L)),
]
SCHRITTE_FR = [
    ("", "Hausaufgabe kontrollieren", 5, "S. 89 Nr. 6 und 7 links.", [1]),
    ("", "Merkheft: Zinssatz gesucht", 10, "Neu ist nur die Wurzel. Taschenrechner-Taste zeigen.", [2]),
    ("", "Runde 1 ◐", 12, "S. 89 Nr. 5.", [3, 4]),
    ("", "Runde 2 gemischt", 13, "S. 89 Alles klar A: erst entscheiden, was gesucht ist.", [5, 6]),
    ("", "Runde 3 ● und Hausaufgabe", 5, "Schnelle: Nr. 6 und 7 rechts. HA: S. 90 Nr. 8 und 10.", [7, 8, 9, 10]),
]
assert sum(m for _, _, m, _, _ in SCHRITTE_FR) == 45


def main():
    bau_woche(HIER / "Mathe 10b – Woche 4 – 1 Zinsen kurz, Zinseszins.html", "Woche 4, Stunde 1: Zinsen kurz, Zinseszins",
              "Klasse 10b, Mathematik, Mi 07.10.2026, Doppelstunde (Montag Ausflug), Buch S. 86 bis 89",
              [("Drucken", "Nichts."), ("Digital", "Folien-PDF in Notability: Mathe 10b – Woche 4 – 1 Zinsen kurz, Zinseszins.pdf (iCloud, 04 Prozentrechnung)."), ("Sonst", "Buch und Taschenrechner mit Potenztaste.")],
              SCHRITTE_MI, FOLIEN_MI,
              tafel=box("Tafelbild = Merkheft: Zinsen", MERK_J) + box("Jahr für Jahr (bleibt an der Tafel)", TAB_HTML) + box("Tafelbild = Merkheft: Zinseszins", MERK_Z),
              merkheft=box("Zinsen", HEFT(MERK_J)) + box("Zinseszins", HEFT(MERK_Z)),
              loesungen=box("S. 86 Nr. 1", liste(N1_L)) + box("S. 87 Alles klar A und B", liste(A_L) + f"<p>{B_L}</p>")
              + box("Einstieg Erbe", f'<p>Ohne Zinseszins: {cent(EINFACH)}. Mit Zinseszins: 1,02<sup>2026</sup> ≈ 2,65 · 10<sup>17</sup> € '
                                     f'(rund {zahl(PRO_MENSCH / 1e6, 0)} Millionen € pro Mensch bei 8 Milliarden Menschen).</p>')
              + box("S. 89 Nr. 1 und 2", liste(NR1_L) + liste(NR2_L)) + box("S. 89 Nr. 3", liste(NR3_L)) + box("S. 89 Nr. 4", liste(NR4_L))
              + box("Hausaufgabe S. 89 Nr. 6 und 7 links", liste(HA_MI_L)), extra_css=EXTRA_CSS, verlauf="Die Doppelstunde")
    bau_woche(HIER / "Mathe 10b – Woche 4 – 2 Zinseszins, Zinssatz gesucht.html", "Woche 4, Stunde 2: Zinseszins, Zinssatz gesucht",
              "Klasse 10b, Mathematik, Fr 09.10.2026, Einzelstunde, Buch S. 89 und 90",
              [("Drucken", "Nichts."), ("Digital", "Folien-PDF in Notability: Mathe 10b – Woche 4 – 2 Zinseszins, Zinssatz gesucht.pdf (iCloud, 04 Prozentrechnung)."), ("Sonst", "Buch und Taschenrechner mit Wurzeltaste.")],
              SCHRITTE_FR, FOLIEN_FR, tafel=box("Tafelbild = Merkheft", MERK_P), merkheft=box("Zinssatz gesucht", HEFT(MERK_P)),
              loesungen=box("S. 89 Nr. 5", liste(NR5_L)) + box("S. 89 Alles klar A", liste(AK_L)) + box("S. 89 Nr. 6 und 7 rechts", liste(RE67_L))
              + box("Hausaufgabe S. 90 Nr. 8 und 10", liste(HA_FR_L)), extra_css=EXTRA_CSS)


if __name__ == "__main__":
    main()
