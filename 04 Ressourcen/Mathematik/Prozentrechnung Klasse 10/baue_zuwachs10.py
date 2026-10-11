#!/usr/bin/env python3
"""Mathe 10b, Woche 5, Stunde 1: Zuwachssparen (Mo 12.10.2026, Einzelstunde).
Einstieg (Oskar, 11.10.2026): sehr leichte Zinseszinsaufgabe (Geburtstagsgeld, 2000 €, 4 Jahre, 2 %), dann dieselbe Aufgabe
mit nur einer Änderung: jedes Jahr ein anderer Zinssatz (1,5 %, 2 %, 2,5 %, 3 %). Danach sechs Textaufgaben ○ ○ ◐ ◐ ● ●.
A4-Seiten wie Mathe 7c Woche 4: je Abschnitt eine Seite, direkt danach dieselbe Seite ausgefüllt. Merkheft im Rezept-Stil.
Schreibweise wie in der Zinseszins-Stunde: q = 1 + p/100, Kₙ = K₀ · qⁿ. Alle Zahlen werden hier berechnet und geprüft.
Aufruf: python3 baue_zuwachs10.py"""
import re
import sys
from math import prod
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER.parent / "Rationale Zahlen"))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_woche7 import merkbild, HEFT, UEB, box, EXTRA_CSS, LUECKE_LANG  # noqa: E402
from baue_woche4 import L, block, auftrag  # noqa: E402
from baue_uebung_ka1_7c import KREIS as _K  # noqa: E402  gleich große Kreise ○ ◐ ●
KREIS = [k.replace('<svg class="kreis"', '<svg class="kreis" width="20" height="20"') for k in _K]

NB = "\u202f"     # schmales geschütztes Leerzeichen: 5 000 €, 2,5 % brechen nie um
NAME = "Mathe 10b – Woche 5 – 1 Zuwachssparen"
A4 = True


def r2(x):
    return round(x + 1e-9, 2)


def eur(x):
    """2186.04 -> '2 186,04 €' (schmales Leerzeichen als Tausendertrenner)."""
    return f"{r2(x):,.2f}".replace(",", " ").replace(".", ",").replace(" ", NB) + NB + "€"


def pz(p):
    return f"{p:g}".replace(".", ",") + NB + "%"


def qtxt(p):
    return f"{1 + p / 100:.4f}".rstrip("0").replace(".", ",")


def verlauf(k0, saetze):
    """Kontostände Jahr für Jahr, ungerundet weitergerechnet und erst zum Anzeigen auf Cent gerundet.
    (Mit gerundeten Zwischenständen käme z. B. 2 164,87 € statt 2 164,86 € heraus, das passt dann nicht zur Kurzformel.)"""
    k, erg = k0, []
    for p in saetze:
        k = k * (1 + p / 100)
        erg.append(r2(k))
    return erg


# ================================================================ Einstieg: Geburtstagsgeld
K0 = 2000
A_SAETZE = [2, 2, 2, 2]
B_SAETZE = [1.5, 2, 2.5, 3]
A_STAND, B_STAND = verlauf(K0, A_SAETZE), verlauf(K0, B_SAETZE)
assert A_STAND == [2040.0, 2080.8, 2122.42, 2164.86] and B_STAND == [2030.0, 2070.6, 2122.37, 2186.04]
assert r2(K0 * 1.02 ** 4) == 2164.86 and r2(K0 * prod(1 + p / 100 for p in B_SAETZE)) == 2186.04

GESCHICHTE = (f"Lina bekommt zum 16. Geburtstag von ihren Großeltern <b>2{NB}000{NB}€</b>. "
              "Sie will das Geld <b>4 Jahre</b> anlegen, bis sie 20 ist. Die Bank macht ihr zwei Angebote.")


def tabelle(saetze, staende, l):
    zeilen = f'<tr><td>0</td><td></td><td></td><td>{eur(K0)}</td></tr>'
    for j, (p, k) in enumerate(zip(saetze, staende), 1):
        zeilen += (f'<tr><td>{j}</td><td>{pz(p)}</td><td>{L(qtxt(p)) if l else LUECKE_LANG}</td>'
                   f'<td>{L(eur(k)) if l else LUECKE_LANG}</td></tr>')
    return ('<table class="zt"><tr><th>Jahr</th><th>Zinssatz</th><th>Zinsfaktor q</th><th>Kontostand</th></tr>' + zeilen + "</table>")


def seite_a(l):
    kurz = (f'<p class="kurz">Kurz: K₄ = 2{NB}000 · 1,02<sup>4</sup> = ' + (L(eur(A_STAND[-1])) if l else LUECKE_LANG) + "</p>")
    return (f'<p class="gesch">{GESCHICHTE}</p>'
            + block("Angebot A: Jedes Jahr 2 % Zinsen (Zinseszins). Wie viel Geld hat Lina nach 4 Jahren?", tabelle(A_SAETZE, A_STAND, l) + kurz)
            + block("Schätze: Lohnt sich Angebot B mehr als A?",
                    f'<p class="gesch">Angebot B, das <b>Zuwachssparen</b>: Der Zinssatz steigt jedes Jahr. '
                    f'1. Jahr 1,5 %, 2. Jahr 2 %, 3. Jahr 2,5 %, 4. Jahr 3 %.</p>'
                    + (f'<p class="gesch">{L("Viele tippen auf A oder sind unsicher: B fängt kleiner an.")}</p>' if l else "")))


SCHRITTE_ZW = ["Zinssätze der einzelnen Jahre herausschreiben.", "Jeden Zinssatz in den Zinsfaktor umwandeln: q = 1 + p/100.",
               "K₀ mit allen Faktoren multiplizieren: Kₙ = K₀ · q₁ · q₂ · … · qₙ", "Auf Cent runden. Antwortsatz."]
WEITERE = [(1000, [1, 2, 3]), (500, [2, 3]), (3000, [1.5, 1.5, 2]), (1200, [0.5, 1, 1.5, 2]), (800, [3, 2, 1]), (2500, [1.2, 1.8, 2.4])]
MERK = merkbild("Zuwachssparen", [
    (1, f'<span class="txt">Zinssätze: 1,5 %; 2 %; 2,5 %; 3 %</span>'),
    (2, '<span class="txt">Faktoren: 1,015; 1,02; 1,025; 1,03</span>'),
    (3, '<span class="txt">K₄ =</span> 2000 · 1,015 · 1,02 · 1,025 · 1,03'),
    (4, f'≈ <b>2186,04</b><span class="txt">{NB}€</span>')],
    SCHRITTE_ZW,
    weitere=[(f"{k} · " + " · ".join(qtxt(p) for p in s), eur(k * prod(1 + p / 100 for p in s)), k * prod(1 + p / 100 for p in s))
             for k, s in WEITERE])
MERK = re.sub(r'(<div class="wz">[^<]*?) = ', r"\1 ≈ ", MERK)     # weitere Beispiele sind gerundet
VERGLEICH = (f'<div class="vgl10"><div><b>Zinseszins</b><br>immer derselbe Faktor<br>Kₙ = K₀ · qⁿ</div>'
             f'<div><b>Zuwachssparen</b><br>jedes Jahr ein eigener Faktor<br>Kₙ = K₀ · q₁ · q₂ · … · qₙ</div></div>')


def seite_b(l):
    kurz = (f'<p class="kurz">Kurz: K₄ = 2{NB}000 · 1,015 · 1,02 · 1,025 · 1,03 = ' + (L(eur(B_STAND[-1])) if l else LUECKE_LANG) + "</p>")
    vgl = ('<p class="kurz">Vergleich nach 4 Jahren: A ' + (L(eur(A_STAND[-1])) if l else LUECKE_LANG) + " &nbsp; B "
           + (L(eur(B_STAND[-1])) if l else LUECKE_LANG) + "</p>")
    rest = (f'<p class="gesch">{L(f"B bringt {eur(B_STAND[-1] - A_STAND[-1])} mehr. Nach 3 Jahren liegen beide fast gleich (2 122,37 € und 2 122,42 €), erst im 4. Jahr zieht B davon.")}</p>' if l else "")
    return (block("Angebot B: Zuwachssparen. Dieselbe Aufgabe, nur der Zinssatz ändert sich jedes Jahr.", tabelle(B_SAETZE, B_STAND, l) + kurz) + vgl + rest
            )


# ================================================================ Sechs Textaufgaben
def fest(t):
    """Zahl und Einheit bzw. Tausenderblöcke zusammenhalten."""
    t = re.sub(r"(\d) (%|€)", "\\1" + NB + "\\2", t)
    t = re.sub(r"\b([a-e]\)) ", "\\1\u00a0", t)
    return re.sub(r"(\d) (\d{3})", "\\1" + NB + "\\2", t)


def aufgabe(nr, stufe, text, loes, l):
    text, loes = fest(text), fest(loes)
    return (f'<div class="tx"><div class="txk"><b>{nr}</b> {KREIS[stufe]}</div><div>{text}'
            + (f'<div class="txl">{loes}</div>' if l else "") + "</div></div>")


A = {}
A["2"] = r2(1000 * 1.01 * 1.02 * 1.03)
A["3"] = r2(1500 * 1.01 * 1.015 * 1.02)
A4_S = [1.2, 1.6, 2.0, 2.4, 2.8]
A4_K = verlauf(2500, A4_S)
A4_Z = [r2(k - v) for k, v in zip(A4_K, [2500] + A4_K[:-1])]
A5_F, A5_Z = r2(4000 * 1.024 ** 4), r2(4000 * 1.015 * 1.02 * 1.028 * 1.036)
A6_K = verlauf(3000, [2, 2.5, 3])
A6_Z3, A6_ZG = r2(A6_K[2] - A6_K[1]), r2(A6_K[2] - 3000)
A7_S = [1, 1.5, 2, 2.5, 3, 3.5]
A7_K = r2(6000 * prod(1 + p / 100 for p in A7_S))
A8_K = verlauf(3000, [1.5, 2.5, 3.5, 4.5])
A9_K3 = r2(3000 * 1.015 * 1.02 * 1.03)
A9_K0 = r2(A9_K3 / (1.015 * 1.02 * 1.03))
A10_K3 = r2(5000 * 1.02 * 1.025 * 1.035)
A10_Q = A10_K3 / (5000 * 1.02 * 1.025)
A11_Q = prod(1 + p / 100 for p in B_SAETZE) ** 0.25
A12_K = r2(K0 * 1.03 * 1.025 * 1.02 * 1.015)
assert A9_K0 == 3000 and round(A10_Q, 4) == 1.035 and A5_Z > A5_F and A12_K == B_STAND[-1] and round((A11_Q - 1) * 100, 2) == 2.25

A4_TAB = ('<table class="zt klein"><tr><th>Jahr</th><th>Zinssatz</th><th>Zinsen</th><th>Kontostand</th></tr>'
          + "".join(f"<tr><td>{j}</td><td>{pz(p)}</td><td>{eur(z)}</td><td>{eur(k)}</td></tr>" for j, (p, z, k) in enumerate(zip(A4_S, A4_Z, A4_K), 1)) + "</table>")
ohne = lambda x: eur(x).replace(NB + "€", "")

AUFGABEN = [
    (1, 0, "Schreibe als Zinsfaktor q: &nbsp;a) 3 % &nbsp; b) 1,5 % &nbsp; c) 2,25 % &nbsp; d) 0,8 % &nbsp; e) 4,2 %",
     f"a) {L('1,03')} &nbsp; b) {L('1,015')} &nbsp; c) {L('1,0225')} &nbsp; d) {L('1,008')} &nbsp; e) {L('1,042')}"),
    (2, 0, f"1{NB}000{NB}€ werden 3 Jahre im Zuwachssparen angelegt: 1 %, 2 % und 3 %. Berechne das Endkapital.",
     f"K₃ = 1{NB}000 · 1,01 · 1,02 · 1,03 ≈ {L(eur(A['2']))}"),
    (3, 0, f"Jonas legt sein Konfirmationsgeld von 1{NB}500{NB}€ für 3 Jahre im Zuwachssparen an. Die Zinssätze: 1 %, 1,5 % und 2 %. "
           "Wie viel Geld hat er nach 3 Jahren?",
     f"K₃ = 1{NB}500 · 1,01 · 1,015 · 1,02 ≈ {L(eur(A['3']))}. Jonas hat nach 3 Jahren {eur(A['3'])}."),
    (4, 0, f"Emre hat im Sommer beim Ferienjob 2{NB}500{NB}€ verdient. Er nimmt einen Zuwachssparplan über 5 Jahre: "
           "1,2 %, 1,6 %, 2,0 %, 2,4 %, 2,8 %. Lege im Heft eine Tabelle an: Jahr, Zinssatz, Zinsen, Kontostand.",
     A4_TAB),
    (5, 1, f"Frau Keller will 4{NB}000{NB}€ für 4 Jahre anlegen. Bank 1 bietet jedes Jahr 2,4 % (Zinseszins). "
           "Bank 2 bietet Zuwachssparen mit 1,5 %, 2 %, 2,8 % und 3,6 %. Welches Angebot ist besser und um wie viel?",
     f"Bank 1: 4{NB}000 · 1,024<sup>4</sup> ≈ {eur(A5_F)}; Bank 2: 4{NB}000 · 1,015 · 1,02 · 1,028 · 1,036 ≈ {eur(A5_Z)}. "
     + L(f"Bank 2 ist um {eur(A5_Z - A5_F)} besser.")),
    (6, 1, f"Mia legt 3{NB}000{NB}€ für 3 Jahre an: 2 %, 2,5 % und 3 %. a) Wie viel Zinsen bekommt sie im 3. Jahr? "
           "b) Wie viel Zinsen bekommt sie insgesamt?",
     f"Kontostände: {eur(A6_K[0])}; {eur(A6_K[1])}; {eur(A6_K[2])}. a) {eur(A6_K[1])} · 0,03 ≈ {L(eur(A6_Z3))} "
     f"b) {eur(A6_K[2])} − 3{NB}000{NB}€ = {L(eur(A6_ZG))}"),
    (7, 1, f"Eine Bank wirbt: „Zuwachssparen über 6 Jahre: 1 %, 1,5 %, 2 %, 2,5 %, 3 %, 3,5 %.“ Herr Yilmaz legt 6{NB}000{NB}€ an. "
           "a) Wie viel Geld hat er nach 6 Jahren? b) Wie viel Zinsen sind das insgesamt?",
     f"a) 6{NB}000 · 1,01 · 1,015 · 1,02 · 1,025 · 1,03 · 1,035 ≈ {L(eur(A7_K))} &nbsp; b) {L(eur(A7_K - 6000))}"),
    (8, 1, f"Lea legt 3{NB}000{NB}€ im Zuwachssparen an: 1,5 %, 2,5 %, 3,5 %, 4,5 %. Nach 2 Jahren braucht sie das Geld für den Führerschein. "
           "a) Wie viel bekommt sie nach 2 Jahren? b) Wie viel hätte sie nach 4 Jahren gehabt? c) Wie viel Zinsen entgehen ihr?",
     f"a) 3{NB}000 · 1,015 · 1,025 ≈ {L(eur(A8_K[1]))} &nbsp; b) · 1,035 · 1,045 ≈ {L(eur(A8_K[3]))} &nbsp; c) {L(eur(A8_K[3] - A8_K[1]))}"),
    (9, 2, f"Tim hat sein Geld 3 Jahre im Zuwachssparen angelegt: 1,5 %, 2 % und 3 %. Jetzt hat er {eur(A9_K3)}. "
           "Wie viel Geld hat er am Anfang eingezahlt?",
     f"K₀ = {ohne(A9_K3)} : (1,015 · 1,02 · 1,03) ≈ {L(eur(A9_K0))}"),
    (10, 2, f"Ein Sparplan läuft 3 Jahre. Im 1. Jahr gibt es 2 %, im 2. Jahr 2,5 %. Aus 5{NB}000{NB}€ werden {eur(A10_K3)}. "
            "Welchen Zinssatz gab es im 3. Jahr?",
     f"q₃ = {ohne(A10_K3)} : (5{NB}000 · 1,02 · 1,025) ≈ 1,035, also {L('3,5 %')}"),
    (11, 2, "Linas Angebot B (1,5 %, 2 %, 2,5 %, 3 %) bringt nach 4 Jahren dasselbe wie ein fester Zinssatz. Wie hoch ist dieser feste Zinssatz?",
     f"q<sup>4</sup> = 1,015 · 1,02 · 1,025 · 1,03 ≈ 1,0930; q = ⁴√1,0930 ≈ 1,0225, also {L('etwa 2,25 %')}"),
    (12, 2, "Bank C bietet Lina dieselben Zinssätze, aber in umgekehrter Reihenfolge: 3 %, 2,5 %, 2 %, 1,5 %. Ist das besser, schlechter oder gleich? Begründe.",
     L(f"Gleich ({eur(A12_K)}): Beim Multiplizieren ist die Reihenfolge der Faktoren egal.")
     + " Aber: Wer vorzeitig kündigt, hat bei Bank C in den ersten Jahren mehr."),
]
print("Werte:", A, A4_K, A5_F, A5_Z, A6_K, A7_K, A8_K, A9_K3, A10_K3, round(A11_Q, 5))


def ab_seite(von, bis, l, kopf=False, druck=False):
    k = ('<div class="abkopf"><span>Name:</span><span>Datum:</span><span>Rechne im Heft. Merkheft daneben.</span></div>' if kopf else "")
    inhalt = (k + "".join(aufgabe(n, st, t, lo, l) for n, st, t, lo in AUFGABEN[von:bis])
              + ("" if kopf else f'<div class="legende10">{KREIS[0]} leicht &nbsp; {KREIS[1]} mittel &nbsp; {KREIS[2]} schwer</div>'))
    return f'<div class="ab{" l" if l else ""}">{inhalt}</div>' if druck else inhalt


def seite_leicht(l):
    return (auftrag(f"Übungsblatt Zuwachssparen. Rechne im Heft. Erst {KREIS[0]} Nr. 1 bis 4, dann {KREIS[1]}.", f"{KREIS[2]} Nr. 9 bis 12")
            + ab_seite(0, 4, l))


def seite_mittel(l):
    return auftrag(f"Übungsblatt weiter: {KREIS[1]} Nr. 5 bis 8.", f"{KREIS[2]} Nr. 9 bis 12") + ab_seite(4, 8, l)


def seite_schwer(l):
    return (auftrag(f"{KREIS[2]} Nr. 9 bis 12 für alle, die so weit sind. Hausaufgabe: bis Nr. 8 fertig.", "Nr. 11 und 12")
            + ab_seite(8, 12, l))


# Übungsblatt zum Drucken: 2 Seiten (doppelseitig), dazu dieselben Seiten ausgefüllt als Lösung
AB_NAME = "Mathe 10b – Zuwachssparen – Übungsblatt"
AB = [("Zuwachssparen – Übungsblatt", lambda l: ab_seite(0, 6, l, True, True)), ("Zuwachssparen – Übungsblatt (Rückseite)", lambda l: ab_seite(6, 12, l, druck=True))]


SEITEN = [("1 Das Geburtstagsgeld", seite_a), ("2 Zuwachssparen", seite_b), ("3 Übungsblatt: leicht", seite_leicht),
          ("4 Übungsblatt: mittel", seite_mittel), ("5 Übungsblatt: schwer und Hausaufgabe", seite_schwer)]
FOLIEN = [x for t, f in SEITEN for x in ((t, f(False)), (f"{t}: ausgefüllt", f(True)))]
FOLIEN.insert(4, ("Merkheft: Zuwachssparen", HEFT(MERK) + VERGLEICH))    # eigene Seite, sonst wird Seite 2 ausgefüllt zu lang
QUER = set()

EXTRA = EXTRA_CSS + """<style>
.gesch{font-size:20px;line-height:1.45;margin:4px 0 10px}
.kurz{font-size:21px;margin:10px 0 4px;white-space:nowrap}
.zt{border-collapse:collapse;font-size:20px;margin:4px 0}.zt th{background:#eef1f5;text-align:left}
.zt th,.zt td{border:1px solid #9aa3b0;padding:5px 12px;white-space:nowrap}.zt.klein{font-size:16px}.zt.klein th,.zt.klein td{padding:3px 9px}
.vgl10{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px;font-size:18px}.vgl10>div{border:1.5px solid #1b1b1b;border-radius:6px;padding:8px 12px}
.tx{display:grid;grid-template-columns:62px 1fr;gap:8px;font-size:18.5px;line-height:1.45;margin:0 0 14px}
.txk{font-size:20px;white-space:nowrap}.txl{margin-top:5px;font-size:17px}
.kreis{width:1.1em;height:1.1em;vertical-align:-.2em}
.abkopf{display:flex;gap:60px;border:1px solid #9aa3b0;padding:6px 10px;font-size:15px;margin:0 0 14px}.abkopf span:last-child{margin-left:auto;color:#555}
.ab .tx{font-size:20.5px;margin-bottom:26px}.ab.l .tx{margin-bottom:9px;font-size:19px}.ab.l .txl{font-size:16.5px}.ab.l .zt.klein{font-size:15px}.ab .txl{font-size:18px}.ab .zt.klein{font-size:17px}
.mb .mz{font-size:18px;white-space:nowrap}.mb .wz{font-size:15.5px;white-space:nowrap}
.legende10{font-size:14px;color:#555;margin-top:8px}
</style>"""

SCHRITTE = [("", "Das Geburtstagsgeld, Angebot A", 9, "Sehr leichte Zinseszinsaufgabe: Tabelle Jahr für Jahr, dann kurz mit 1,02⁴. Danach Angebot B nur vorlesen und schätzen lassen.", [1, 2]),
            ("", "Zuwachssparen, Merkheft", 11, "Dieselbe Tabelle, nur jedes Jahr ein anderer Faktor. Vergleich A und B. Merkheft mit Rezept und Vergleichskasten.", [3, 4, 5]),
            ("", "Übungsblatt", 25, "Blatt austeilen, im Heft rechnen: ○ Nr. 1 bis 4, dann ◐ Nr. 5 bis 8. Schnelle ● Nr. 9 bis 12. Zwischendurch besprechen.", [6, 7, 8, 9, 10, 11])]
assert sum(m for _, _, m, _, _ in SCHRITTE) == 45


def main():
    loes = "".join(box(t.replace(": ausgefüllt", ""), h) for t, h in FOLIEN if t.endswith("ausgefüllt"))
    bau_woche(HIER / f"{NAME}.html", "Woche 5, Stunde 1: Zuwachssparen", "Klasse 10b, Mathematik, Mo 12.10.2026, Einzelstunde",
              [("Drucken", f"{AB_NAME}.pdf, doppelseitig, für jeden ein Blatt. Lösung: {AB_NAME} – Lösung.pdf"), ("Sonst", "Taschenrechner."), ("Digital", f"Folien-PDF in Notability: {NAME}.pdf (iCloud, 04 Prozentrechnung).")],
              SCHRITTE, FOLIEN, tafel=box("Angebot B: Zuwachssparen", seite_b(True)), merkheft=box("Zuwachssparen", HEFT(MERK) + VERGLEICH),
              loesungen=loes, extra_css=EXTRA, verlauf="Die Stunde")
    print("geschrieben:", NAME)


if __name__ == "__main__":
    main()
