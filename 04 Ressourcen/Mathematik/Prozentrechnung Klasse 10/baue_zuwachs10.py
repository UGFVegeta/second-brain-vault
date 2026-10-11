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


BRUCH_P = '<span class="bruch"><span>p</span><span>100</span></span>'
SCHRITTE_ZW = ["Zinssätze der einzelnen Jahre herausschreiben.", f'Jeden Zinssatz in den Zinsfaktor umwandeln:<br><span class="nw">q = 1 + {BRUCH_P}</span>',
               'K₀ mit allen Faktoren multiplizieren:<br><span class="nw">Kₙ = K₀ · q₁ · q₂ · … · qₙ</span>', "Auf Cent runden. Antwortsatz."]
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


def aufgabe(nr, stufe, text, loes, l, bild=""):
    text, loes = fest(text), fest(loes)
    inhalt = f'<div>{text}' + (f'<div class="txl">{loes}</div>' if l else "") + "</div>"
    if bild:
        inhalt = f'<div class="mitbild">{inhalt}<div class="bild">{bild}</div></div>'
    return f'<div class="tx"><div class="txk"><b>{nr}</b> {KREIS[stufe]}</div>{inhalt}</div>'


def aufgaben(liste, l):
    return "".join(aufgabe(*t[:4], l, *t[4:]) for t in liste)


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


# ================================================================ Teil ohne Taschenrechner (Prozentrechnung, passend zur Klassenarbeit)
def kreisdiagramm(teile):
    """teile: [(Name, Prozent)] -> SVG-Kreisdiagramm in Graustufen mit Beschriftung im Feld."""
    from math import cos, sin, pi
    farben = ["#4a4f57", "#8d939c", "#c3c8cf", "#e9ecf0"]
    o, start, r, cx, cy = ['<svg viewBox="0 0 245 170" width="215">'], -90, 70, 85, 85
    for i, (name, pr) in enumerate(teile):
        ende = start + pr * 3.6
        x1, y1 = cx + r * cos(start * pi / 180), cy + r * sin(start * pi / 180)
        x2, y2 = cx + r * cos(ende * pi / 180), cy + r * sin(ende * pi / 180)
        o.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {1 if pr > 50 else 0} 1 {x2:.1f},{y2:.1f} Z" fill="{farben[i]}" stroke="#fff" stroke-width="2"/>')
        o.append(f'<rect x="165" y="{22 + i * 30}" width="12" height="12" fill="{farben[i]}" stroke="#555" stroke-width=".6"/>'
                 f'<text x="182" y="{32 + i * 30}" font-size="12">{name}</text>')
        start = ende
    return "".join(o) + "</svg>"


def preisschild(preis, rabatt):
    return (f'<svg viewBox="0 -6 200 126" width="180"><path d="M30,20 H180 V100 H30 L5,60 Z" fill="#fff" stroke="#1b1b1b" stroke-width="2.5"/>'
            f'<circle cx="24" cy="60" r="5" fill="none" stroke="#1b1b1b" stroke-width="2"/>'
            f'<text x="105" y="58" font-size="16" text-anchor="middle">Sneaker</text><text x="105" y="86" font-size="24" font-weight="700" text-anchor="middle">{preis}{NB}€</text>'
            f'<circle cx="166" cy="24" r="28" fill="#1b1b1b"/><text x="166" y="30" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">−{rabatt}{NB}%</text></svg>')


def balken(werte):
    """werte: [(Name, Zahl)] -> waagrechte Balken mit Zahl am Ende."""
    o = ['<svg viewBox="0 0 230 120" width="210">']
    for i, (name, w) in enumerate(werte):
        y = 10 + i * 36
        o.append(f'<text x="0" y="{y + 18}" font-size="13">{name}</text><rect x="62" y="{y}" width="{w * 11}" height="24" fill="#8d939c"/>'
                 f'<text x="{68 + w * 11}" y="{y + 17}" font-size="13" font-weight="700">{w}</text>')
    return "".join(o) + "</svg>"


def streifen(anteil, beschriftung):
    b = 200 * anteil / 100
    return (f'<svg viewBox="0 0 230 70" width="215"><rect x="10" y="12" width="200" height="30" fill="#fff" stroke="#1b1b1b" stroke-width="1.5"/>'
            f'<rect x="10" y="12" width="{b}" height="30" fill="#8d939c" stroke="#1b1b1b" stroke-width="1.5"/>'
            f'<text x="{10 + b / 2}" y="32" font-size="13" font-weight="700" text-anchor="middle">{anteil}{NB}%</text>'
            f'<text x="{10 + b / 2}" y="60" font-size="13" text-anchor="middle">{beschriftung}</text>'
            f'<text x="{10 + b + (200 - b) / 2}" y="60" font-size="13" text-anchor="middle">Gesamt: ?</text></svg>')


def kette():
    return ('<svg viewBox="0 0 240 70" width="225"><rect x="2" y="15" width="60" height="34" rx="5" fill="#fff" stroke="#1b1b1b" stroke-width="1.5"/>'
            '<text x="32" y="38" font-size="15" font-weight="700" text-anchor="middle">100 €</text>'
            '<path d="M66,32 H100" stroke="#1b1b1b" stroke-width="1.5" marker-end="url(#pf)"/><text x="83" y="12" font-size="12" text-anchor="middle">+10 %</text>'
            '<rect x="106" y="15" width="44" height="34" rx="5" fill="#fff" stroke="#1b1b1b" stroke-width="1.5"/><text x="128" y="38" font-size="15" text-anchor="middle">?</text>'
            '<path d="M154,32 H188" stroke="#1b1b1b" stroke-width="1.5" marker-end="url(#pf)"/><text x="171" y="12" font-size="12" text-anchor="middle">−10 %</text>'
            '<rect x="194" y="15" width="44" height="34" rx="5" fill="#fff" stroke="#1b1b1b" stroke-width="1.5"/><text x="216" y="38" font-size="15" text-anchor="middle">?</text>'
            '<defs><marker id="pf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#1b1b1b"/></marker></defs></svg>')


UMFRAGE = [("Bus", 50), ("Fahrrad", 25), ("zu Fuß", 15), ("Auto", 10)]
WAHL = [("Aylin", 12), ("Ben", 8), ("Carla", 5)]
assert sum(p for _, p in UMFRAGE) == 100 and 200 * 25 // 100 == 50 and 80 * 75 // 100 == 60 and 12 * 100 // 25 == 48
assert 34 * 100 // 40 == 85 and 90 * 100 // 30 == 300 and round(100 * 1.1 * 0.9, 2) == 99 and round(1000 * 1.05 ** 2, 2) == 1102.5

def ds(*zeilen, formel=""):
    """Dreisatz als Kette: ds(("100 %", "200 Schüler"), ("1 %", "2"), ...). Die Zeile mit 100 % wird markiert.
    Oskar (11.10.2026): Prozentaufgaben ohne mehrere Jahre immer mit dem Dreisatz lösen, das 100 % sichtbar machen;
    die Formel steht ergänzend darunter."""
    teile = []
    for a, b in zeilen:
        neu = a.startswith("neu ")
        a = a.replace("neu ", "")
        z = f"{a} ≙ {b}"
        teile.append(f'<span class="ds100">{"neues " if neu else ""}{z}</span>' if a.startswith("100") else f'<span class="dsz">{z}</span>')
    return ('<span class="ds">' + ' <span class="dsp">→</span> '.join(teile) + "</span>"
            + (f'<br><span class="dsf">Formel: {formel}</span>' if formel else ""))


OHNE_TR = [
    (13, 0, "200 Schülerinnen und Schüler wurden gefragt, wie sie zur Schule kommen. a) Wie viele kommen mit dem Fahrrad? "
            "b) Wie viele kommen zu Fuß? c) Welcher Anteil fährt Bus? Gib ihn als Bruch an.",
     ds(("100 %", "200 Schüler"), ("1 %", "2"), ("25 %", L("50 (Fahrrad)")), ("15 %", L("30 (zu Fuß)")))
     + f"<br>c) 50 % = {L('1/2')} &nbsp; <span class='dsf'>Formel: W = 200 · 0,25 = 50</span>", kreisdiagramm(UMFRAGE)),
    (14, 0, "Die Sneaker sind um 25 % reduziert. Wie viel kosten sie jetzt?",
     ds(("100 %", "80 € (alter Preis)"), ("1 %", "0,80 €"), ("75 %", L("60 €")), formel="80 € · 0,75 = 60 €"), preisschild(80, 25)),
    (15, 1, "Bei der Klassensprecherwahl wurden 25 Stimmen abgegeben. Wie viel Prozent der Stimmen hat jede Person bekommen?",
     ds(("100 %", "25 Stimmen"), ("4 %", "1 Stimme"), (L("48 %"), "12 (Aylin)"), (L("32 %"), "8 (Ben)"), (L("20 %"), "5 (Carla)"),
        formel="p % = 12 : 25 = 0,48 = 48 %"), balken(WAHL)),
    (16, 1, "Bei der Klassenfahrt sind 30 % der Kosten schon bezahlt, das sind 90 €. Wie viel kostet die Fahrt insgesamt?",
     ds(("30 %", "90 €"), ("10 %", "30 €"), ("100 %", L("300 €")), formel="G = 90 € : 0,3 = 300 €"), streifen(30, "90 €")),
    (17, 1, "Ben hat im Test 34 von 40 Aufgaben richtig. Wie viel Prozent sind das? Lea hat 18 von 20 richtig. Wer war besser?",
     "Ben: " + ds(("100 %", "40 Aufgaben"), ("2,5 %", "1 Aufgabe"), (L("85 %"), "34 Aufgaben"))
     + "<br>Lea: " + ds(("100 %", "20 Aufgaben"), ("5 %", "1 Aufgabe"), (L("90 %"), "18 Aufgaben"))
     + f" &nbsp; {L('Lea war besser.')}<br><span class='dsf'>Formel: p % = 34 : 40 = 0,85</span>"),
    (18, 2, "Eine Jacke kostet 100 €. Erst wird sie um 10 % teurer, dann um 10 % billiger. Kostet sie wieder 100 €? Begründe.",
     ds(("100 %", "100 €"), ("110 %", "110 €"))
     + "<br>" + ds(("neu 100 %", "110 €"), ("10 %", "11 €"), ("90 %", L("99 €")))
     + f"<br>{L('Nein.')} Nach der Erhöhung sind 110 € das neue 100 %. Die 10 % Rabatt werden von 110 € berechnet."
     + "<br><span class='dsf'>Formel: 100 € · 1,1 · 0,9 = 99 €</span>", kette()),
]


def otr_kopf():
    return '<div class="otr">Ohne Taschenrechner: Prozentrechnung wie in der Klassenarbeit</div>'


def ab_seite(von, bis, l, kopf=False, druck=False):
    k = ('<div class="abkopf"><span>Name:</span><span>Datum:</span><span>Rechne im Heft. Merkheft daneben.</span></div>' if kopf else "")
    liste = (AUFGABEN + OHNE_TR)[von:bis]
    otr = (lambda i, t: otr_kopf() if t[0] == 13 else "")
    inhalt = (k + "".join(otr(i, t) + aufgaben([t], l) for i, t in enumerate(liste))
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
AB = [("Zuwachssparen – Übungsblatt", lambda l: ab_seite(0, 9, l, True, True)), ("Zuwachssparen – Übungsblatt (Rückseite)", lambda l: ab_seite(9, 18, l, druck=True))]
AB_L = [("Zuwachssparen – Übungsblatt – Lösung (1)", lambda l: ab_seite(0, 6, l, True, True)),
        ("Zuwachssparen – Übungsblatt – Lösung (2)", lambda l: ab_seite(6, 12, l, druck=True)),
        ("Zuwachssparen – Übungsblatt – Lösung (3)", lambda l: ab_seite(12, 15, l, druck=True)),
        ("Zuwachssparen – Übungsblatt – Lösung (4)", lambda l: ab_seite(15, 18, l, druck=True))]


def seite_otr(l):
    return auftrag("Ohne Taschenrechner: Nr. 13 bis 18. Übung für die Klassenarbeit, auch zu Hause. Prozent: mit dem Dreisatz.", "Nr. 18") + ab_seite(12, 15, l)


def seite_otr2(l):
    return auftrag("Ohne Taschenrechner weiter: Nr. 16 bis 18. Immer fragen: Was sind die 100 %?", "Nr. 18") + ab_seite(15, 18, l)


SEITEN = [("1 Das Geburtstagsgeld", seite_a), ("2 Zuwachssparen", seite_b), ("3 Übungsblatt: leicht", seite_leicht),
          ("4 Übungsblatt: mittel", seite_mittel), ("5 Übungsblatt: schwer und Hausaufgabe", seite_schwer),
          ("6 Ohne Taschenrechner", seite_otr), ("7 Ohne Taschenrechner, Teil 2", seite_otr2)]
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
.ab .tx{font-size:19px;margin-bottom:16px}.ab.l .tx{margin-bottom:9px;font-size:19px}.ab.l .txl{font-size:16.5px}.ab.l .zt.klein{font-size:15px}.ab .txl{font-size:18px}.ab .zt.klein{font-size:17px}
.mb .mz{font-size:18px;white-space:nowrap}.mb .wz{font-size:15.5px;white-space:nowrap}
.ds{white-space:normal}.ds100{font-weight:700;border-bottom:2px solid #E6007E;white-space:nowrap}.dsz{white-space:nowrap}.dsp{color:#888}.dsf{color:#555;font-size:.92em}
.otr{border:2px solid #1b1b1b;border-radius:6px;padding:6px 12px;font-weight:700;font-size:18px;margin:14px 0 12px}
.mitbild{display:grid;grid-template-columns:1fr auto;gap:14px;align-items:start}.bild svg{display:block}
.mb{grid-template-columns:1.5fr 1fr}.mb .weitere{grid-template-columns:1fr}.mb .wz{font-size:17px}
.bruch{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:1em;line-height:1.1;margin:0 .1em}.bruch span:first-child{border-bottom:1.5px solid currentColor;padding:0 .2em}.nw{white-space:nowrap}
.legende10{font-size:14px;color:#555;margin-top:8px}
</style>"""

SCHRITTE = [("", "Das Geburtstagsgeld, Angebot A", 9, "Sehr leichte Zinseszinsaufgabe: Tabelle Jahr für Jahr, dann kurz mit 1,02⁴. Danach Angebot B nur vorlesen und schätzen lassen.", [1, 2]),
            ("", "Zuwachssparen, Merkheft", 11, "Dieselbe Tabelle, nur jedes Jahr ein anderer Faktor. Vergleich A und B. Merkheft mit Rezept und Vergleichskasten.", [3, 4, 5]),
            ("", "Übungsblatt", 25, "Blatt austeilen, im Heft rechnen: ○ Nr. 1 bis 4, dann ◐ Nr. 5 bis 8. Schnelle ● Nr. 9 bis 12. Ohne Taschenrechner Nr. 13 bis 18 als Übung für die Klassenarbeit, auch zu Hause.", [6, 7, 8, 9, 10, 11, 12, 13, 14, 15])]
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
