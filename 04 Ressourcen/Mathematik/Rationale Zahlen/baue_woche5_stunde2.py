#!/usr/bin/env python3
"""Mathe 7c, Woche 5, Stunde 2: Übungsstunde (Doppelstunde) mit Whiteboard-Einstieg und Lerntheke.
Ablauf: Whiteboard-Runde (10 Kurzaufgaben), Fragen und Wiederholung, Lerntheke mit 5 Blättern, Abschluss.
Die Blätter folgen den Themenfeldern der Klassenarbeit (Zahlenstrahl und Vergleichen; Addieren und Subtrahieren;
Multiplizieren und Dividieren; Sachaufgaben), das fünfte Blatt mischt alles. Rechnen im Heft, die Lösungen hängen an der Wand.
Druck: Blatt 1 und 2 auf ein A4 quer, Blatt 3 und 4 auf ein A4 quer (in der Mitte durchschneiden), Blatt 5 ganzes A4 hoch.
Aufruf: python3 baue_woche5_stunde2.py
Erzeugt: Stunden-HTML, Folien-PDF, 3 Druck-PDFs, Lösungs-PDF zum Aushängen (alles in diesem Ordner)."""
import re
import shutil
import subprocess
import sys
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche  # noqa: E402
import baue_woche7 as w7  # noqa: E402
from baue_ka1_7c import br  # noqa: E402
from baue_uebung_ka1_7c import KREIS  # noqa: E402
from rezepte_rz import REZEPT_PM  # noqa: E402

from pypdf import PdfReader  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
NAME = "Mathe 7c – Woche 5 – 2 Übungsstunde Lerntheke"
MAG = "#E6007E"


# ---------------------------------------------------------------- Rechnen und Anzeigen in Schulschreibweise
# Terme stehen in Schulschreibweise: − · : und Komma, Brüche als {z/n}. wert() rechnet exakt nach.
def _num(m):
    if m[1]:
        return f"F({m[1]},{m[2]})"
    if m[3]:
        return f'F("{m[3]}.{m[4]}")'
    return f"F({m[5]})"


def wert(t):
    s = t.replace("−", "-").replace("·", "*").replace(":", "/")
    s = re.sub(r"\{(\d+)/(\d+)\}|(\d+),(\d+)|(\d+)", _num, s)
    return eval(s, {"F": F})


def zeig(t):
    return re.sub(r"\{(\d+)/(\d+)\}", lambda m: br(m[1], m[2]), t)


def zahl(x):
    """Ergebnis als Text: ganze Zahl, endlicher Dezimalbruch mit Komma, sonst Bruch (gekürzt)."""
    x = F(x)
    vz = "−" if x < 0 else ""
    x = abs(x)
    if x.denominator == 1:
        return vz + str(x.numerator)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d == 1:
        return vz + str(Decimal(x.numerator) / Decimal(x.denominator)).replace(".", ",")
    return vz + br(x.numerator, x.denominator)


BIN = re.compile(r"^(−?)(\d+(?:,\d+)?) ([+−·:]) (\()?(−?)(\d+(?:,\d+)?)\)?$")
PROD = re.compile(r"^(−?\d+(?:,\d+)?)( · \(?−?\d+(?:,\d+)?\)?){2,}$")


def hinweis(t):
    """Kurze Begründung zu Aufgaben mit zwei Zahlen oder einem Produkt, sonst leer."""
    m = BIN.match(t)
    if m:
        sa, a, op, _, sb, b = m.groups()
        A, B = wert(a), wert(b)
        if op in "+−":
            assert not sb
            if op == "+" and not sa:
                return f"beide positiv: {a} + {b} = {zahl(A + B)}"
            if op == "−" and not sa:
                if A >= B:
                    return f"{a} − {b} = {zahl(A - B)}"
                return f"{b} ist größer: {b} − {a} = {zahl(B - A)}, das Ergebnis ist negativ"
            if op == "+":
                if A < B:
                    return f"verschiedene Zeichen, {b} ist größer: {b} − {a} = {zahl(B - A)}, positiv"
                if A > B:
                    return f"verschiedene Zeichen, {a} ist größer: {a} − {b} = {zahl(A - B)}, negativ"
                return "gleich große Zahlen mit verschiedenen Zeichen: 0"
            return f"gleiche Zeichen: {a} + {b} = {zahl(A + B)}, das Minus bleibt"
        gleich = bool(sa) == bool(sb)
        rechnung = f"{a} {op} {b} = {zahl(A * B if op == '·' else A / B)}"
        return ("gleiche Vorzeichen, das Ergebnis ist positiv: " if gleich else "verschiedene Vorzeichen, das Ergebnis ist negativ: ") + rechnung
    if PROD.match(t):
        zahlen = [z.strip("() ") for z in t.split(" · ")]
        n = sum(z.startswith("−") for z in zahlen)
        betrag = " · ".join(z.lstrip("−") for z in zahlen)
        w = abs(wert(t))
        return (f"{n} Minuszeichen ({'gerade, also positiv' if n % 2 == 0 else 'ungerade, also negativ'}): {betrag} = {zahl(w)}")
    return ""


def weg(term, *schritte, hint=None):
    """Aufgabe mit Zwischenschritten. Jeder Schritt muss denselben Wert haben wie die Aufgabe."""
    w = wert(term)
    for s in schritte:
        assert wert(s) == w, (term, s, wert(s), w)
    teile = [zeig(s) for s in schritte]
    if "{" in term:     # Bruchaufgabe: das Ergebnis bleibt ein Bruch (gekürzt)
        end = ("−" if w < 0 else "") + (str(abs(w).numerator) if abs(w).denominator == 1 else br(abs(w).numerator, abs(w).denominator))
    else:
        end = zahl(w)
    if not teile or teile[-1] != end:
        teile.append(end)
    h = hint if hint is not None else (hinweis(term) if not schritte else "")
    return {"term": term, "kette": teile, "hint": h, "wert": w}


def A(term, *schritte, hint=None):
    return weg(term, *schritte, hint=hint)


# ---------------------------------------------------------------- Zahlenstrahl (für A5 groß genug beschriftet)
def strahl(lo, hi, punkte=(), farbe="#1b1b1b", beschriften=True):
    u, x0 = 940 / (hi - lo), 30
    X = lambda v: x0 + (float(v) - lo) * u
    o = ['<svg class="zs" viewBox="0 0 1000 128">',
         f'<line x1="{x0 - 20}" y1="76" x2="{x0 + 940 + 28}" y2="76" stroke="#000" stroke-width="3.5"/>',
         f'<path d="M{x0 + 940 + 40},76 l-18,-8 v16z" fill="#1b1b1b"/>']
    for i in range((hi - lo) * 10 + 1):
        h = 17 if i % 10 == 0 else (12 if i % 5 == 0 else 8)
        d = 4 if i % 10 == 0 else (3 if i % 5 == 0 else 2)
        o.append(f'<line x1="{X(lo + i / 10):.1f}" y1="{76 - h}" x2="{X(lo + i / 10):.1f}" y2="{76 + h}" stroke="#000" stroke-width="{d}"/>')
        if i % 10 == 0:
            o.append(f'<text x="{X(lo + i / 10):.1f}" y="122" font-size="34" font-weight="700" text-anchor="middle">{str(lo + i // 10).replace("-", "−")}</text>')
    for b, v in punkte:
        o.append(f'<path d="M{X(v):.1f},62 l-8,-14 h16z" fill="{farbe}"/><line x1="{X(v):.1f}" y1="26" x2="{X(v):.1f}" y2="50" stroke="{farbe}" stroke-width="3"/>'
                 f'<text x="{X(v):.1f}" y="20" font-size="32" font-weight="700" fill="{farbe}" text-anchor="middle">{b}</text>')
    o.append("</svg>")
    return "".join(o)


def dez(v):
    return zahl(F(str(v)))


# ---------------------------------------------------------------- Abschnitte (Aufgabengruppen) der Blätter
# kind: rechnen | vgl | ordnen | vz | strahl_ab | strahl_ein | knobel | sach
def abschnitt(kind, stufe, text, items, cols=2, **kw):
    return dict(kind=kind, stufe=stufe, text=text, items=items, cols=cols, **kw)


BLATT1 = ("Zahlenstrahl, Vergleichen, Ordnen", [
    abschnitt("strahl_ab", 0, "Welche Zahlen sind markiert? Schreibe A = … ins Heft.",
              [("A", "-4.2"), ("B", "-1.5"), ("C", "0.7"), ("D", "3.4")], lo=-5, hi=5),
    abschnitt("vgl", 0, "Setze &lt;, &gt; oder = ein.",
              [("−8", "5"), ("−15", "−9"), ("−2,4", "−2,04"), ("−0,3", "0"), ("−{2/5}", "−0,4"), ("−{1/2}", "−{2/3}")]),
    abschnitt("ordnen", 1, "Ordne der Größe nach. Beginne mit der kleinsten Zahl.",
              ["4; −9; 0; −3; 7", "−1,5; −1,05; 0,5; −0,15; 1,05"], cols=1),
    abschnitt("vz", 1, "Ist das Ergebnis positiv oder negativ? Entscheide ohne zu rechnen.",
              ["−21 + 13", "−5 + 18", "6 − 15", "−7 · (−8)", "9 · (−3)", "−4 · (−3) · (−2)"]),
    abschnitt("knobel", 2, "Knobeln.",
              [("Welche Zahl liegt genau in der Mitte zwischen −7 und 3?", "−2", "Von −7 bis 3 sind es 10 Schritte, die Hälfte ist 5. Von −7 aus 5 nach rechts: −2."),
               ("Wie viele ganze Zahlen liegen zwischen −4,5 und 2,5?", "7", "Das sind −4; −3; −2; −1; 0; 1; 2. Zusammen 7 Zahlen.")], cols=1),
])

BLATT2 = ("Addieren und Subtrahieren", [
    abschnitt("rechnen", 0, "Berechne.", [A(t) for t in ["−8 + 3", "5 − 9", "−6 − 4", "7 − 12", "−15 + 20", "14 − 30"]]),
    abschnitt("rechnen", 1, "Berechne.", [A(t) for t in ["−47 + 29", "−63 − 38", "24 − 81", "−3,7 + 8,2", "−6,4 − 2,9", "1,3 − 4,8"]]),
    abschnitt("rechnen", 1, "Berechne. Kürze, wenn es geht.", [
        A("−{1/4} + {3/4}", "{2/4}", "{1/2}", hint="Gleicher Nenner: im Zähler −1 + 3 = 2. Dann kürzen."),
        A("−{2/5} − {1/5}", "−{3/5}", hint="Gleicher Nenner, gleiche Zeichen: 2 + 1 = 3, das Minus bleibt."),
        A("{1/2} − {5/6}", "{3/6} − {5/6}", "−{2/6}", "−{1/3}", hint="Erst auf den Nenner 6 erweitern, dann 3 − 5 = −2, dann kürzen."),
        A("−{3/4} − {1/2}", "−{3/4} − {2/4}", "−{5/4}", hint="Auf den Nenner 4 erweitern, gleiche Zeichen: 3 + 2 = 5, das Minus bleibt.")]),
    abschnitt("rechnen", 2, "Berechne. Rechne in kleinen Schritten.", [
        A("−9 + 14 − 22 + 6 − 3", "−34 + 20", hint="Minus-Zahlen: 9 + 22 + 3 = 34. Plus-Zahlen: 14 + 6 = 20."),
        A("18 − 25 + 7 − 12 + 4", "−37 + 29", hint="Minus-Zahlen: 25 + 12 = 37. Plus-Zahlen: 18 + 7 + 4 = 29."),
        A("−4,5 + 8 − 2,5 − 6", "−13 + 8", hint="Minus-Zahlen: 4,5 + 2,5 + 6 = 13. Plus-Zahl: 8.")], cols=1),
    abschnitt("rechnen", 2, "Löse zuerst die Minusklammer auf.", [
        A("20 − (7 − 15)", "20 − 7 + 15", "13 + 15", hint="Minus vor der Klammer: alle Vorzeichen in der Klammer umdrehen."),
        A("−8 − (3 + 9)", "−8 − 3 − 9", "−11 − 9", hint="Minus vor der Klammer: aus + wird −."),
        A("−12 − (5 − 20)", "−12 − 5 + 20", "−17 + 20", hint="Minus vor der Klammer: aus − wird +.")], cols=1),
])

BLATT3 = ("Multiplizieren und Dividieren", [
    abschnitt("rechnen", 0, "Berechne.", [A(t) for t in ["−5 · 9", "−7 · (−4)", "6 · (−8)", "−3 · (−12)", "−9 · 6", "4 · (−11)"]]),
    abschnitt("rechnen", 1, "Berechne.", [A(t) for t in ["−42 : 6", "−56 : (−7)", "63 : (−9)", "−81 : (−9)", "−72 : 8", "45 : (−5)"]]),
    abschnitt("rechnen", 1, "Berechne.", [A(t) for t in ["−0,5 · 18", "−1,5 · (−6)", "−4,8 : 6", "−3,6 : (−0,9)"]]),
    abschnitt("rechnen", 2, "Berechne. Kürze, wenn es geht.", [
        A("−{1/2} · {3/4}", "−{3/8}", hint="Zähler mal Zähler, Nenner mal Nenner. Verschiedene Vorzeichen: negativ."),
        A("−{2/3} · (−{9/10})", "{18/30}", "{3/5}", hint="Gleiche Vorzeichen: positiv. 2 · 9 = 18 und 3 · 10 = 30, dann mit 6 kürzen."),
        A("−{3/5} : {9/10}", "−{3/5} · {10/9}", "−{30/45}", "−{2/3}", hint="Geteilt durch einen Bruch: mit dem Kehrbruch malnehmen. Dann kürzen."),
        A("{1/4} : (−{1/8})", "{1/4} · (−8)", "−{8/4}", "−2", hint="Der Kehrwert von −1/8 ist −8. Verschiedene Vorzeichen: negativ.")]),
    abschnitt("rechnen", 2, "Berechne. Achte zuerst auf das Vorzeichen.", [
        A("−3 · (−2) · 4 · (−1)", "6 · 4 · (−1)", "24 · (−1)", hint="Drei Minuszeichen: ungerade, also negativ."),
        A("−2 · 5 · (−4) · (−3)", "−10 · (−4) · (−3)", "40 · (−3)", hint="Drei Minuszeichen: ungerade, also negativ."),
        A("−48 : (−6) : 2", "8 : 2", hint="Von links nach rechts: −48 : (−6) = 8, dann 8 : 2."),
        A("60 : (−5) · (−2)", "−12 · (−2)", hint="Von links nach rechts: 60 : (−5) = −12, dann −12 · (−2).")], cols=1),
])

BLATT4 = ("Sachaufgaben", [
    abschnitt("sach", 0, "Temperatur.",
              [dict(text="Um 6 Uhr zeigt das Thermometer −5 °C, mittags 7 °C und abends −3 °C.",
                    teile=[("Um wie viel Grad ist es bis zum Mittag gestiegen?", "5 + 7", 12, "Grad", "Von −5 bis 0 sind es 5 Grad, von 0 bis 7 noch 7 Grad."),
                           ("Um wie viel Grad ist es vom Mittag bis zum Abend gefallen?", "7 + 3", 10, "Grad", "Von 7 bis 0 sind es 7 Grad, von 0 bis −3 noch 3 Grad.")])]),
    abschnitt("sach", 0, "Kontostand.",
              [dict(text="Frau Berg hat −85 € auf dem Konto. Sie zahlt 120 € ein. Danach bucht die Bank 64 € Miete ab.",
                    teile=[("Wie viel Euro sind nach der Einzahlung auf dem Konto?", "−85 + 120", 35, "€", "Verschiedene Zeichen, 120 ist größer: 120 − 85 = 35."),
                           ("Wie viel Euro sind nach der Abbuchung auf dem Konto?", "35 − 64", -29, "€", "64 ist größer als 35: 64 − 35 = 29, das Ergebnis ist negativ.")])]),
    abschnitt("sach", 1, "Tauchen.",
              [dict(text="Ein U-Boot taucht bis auf −120 m. Dann steigt es 45 m auf und sinkt danach 80 m.",
                    teile=[("In welcher Höhe ist das U-Boot nach dem Aufstieg?", "−120 + 45", -75, "m", "Verschiedene Zeichen, 120 ist größer: 120 − 45 = 75, negativ."),
                           ("In welcher Höhe ist es nach dem Sinken?", "−75 − 80", -155, "m", "Gleiche Zeichen: 75 + 80 = 155, das Minus bleibt."),
                           ("Wie viele Meter fehlen bis zum Meeresspiegel (0 m)?", "155", 155, "m", "Vom Stand −155 m bis 0 m sind es 155 m.")])]),
    abschnitt("sach", 2, "Kontoauszug.",
              [dict(text="Alter Kontostand −130 €. Gehalt 1280 €. Miete −540 €. Strom −68,50 €. Erstattung 35 €.",
                    teile=[("Schreibe eine Rechnung für den neuen Kontostand auf.", "−130 + 1280 − 540 − 68,5 + 35", F("576.5"), "€", "Alle Buchungen der Reihe nach. Rechnen: Plus-Zahlen 1280 + 35 = 1315; Minus-Zahlen 130 + 540 + 68,5 = 738,5; 1315 − 738,5 = 576,5."),
                           ("Wie viel Euro hat sie am Ende auf dem Konto?", "1315 − 738,5", F("576.5"), "€", "Das Ergebnis ist positiv: Sie hat 576,50 € auf dem Konto.")])]),
])

BLATT5 = ("Gemischte Aufgaben", [
    abschnitt("vgl", 0, "Setze &lt;, &gt; oder = ein.", [("−6", "−10"), ("−1,1", "−1,01"), ("−{3/4}", "−0,75"), ("0,2", "−5")], cols=2),
    abschnitt("rechnen", 0, "Berechne.", [A(t) for t in ["−18 + 7", "9 − 21", "−4 · 8", "−54 : (−6)", "−35 − 14", "12 · (−5)", "−28 + 40", "−63 : 7", "−9 − 17", "−7 · (−6)", "15 − 62", "−90 : (−15)"]], cols=3),
    abschnitt("rechnen", 1, "Berechne.", [
        A("−3,4 + 1,9"), A("−2,7 − 4,8"), A("−0,6 · 15"), A("−7,2 : (−0,8)"),
        A("−{1/2} + {1/3}", "−{3/6} + {2/6}", "−{1/6}", hint="Nenner 6: −3 + 2 = −1."),
        A("−{3/4} − {1/4}", "−{4/4}", hint="Gleicher Nenner, gleiche Zeichen: 3 + 1 = 4, also −{4/4} = −1."),
        A("−{2/3} · {3/8}", "−{6/24}", "−{1/4}", hint="Zähler mal Zähler, Nenner mal Nenner, dann kürzen."),
        A("{5/6} : (−{5/12})", "{5/6} · (−{12/5})", "−{60/30}", "−2", hint="Mit dem Kehrbruch malnehmen, verschiedene Vorzeichen: negativ.")]),
    abschnitt("rechnen", 1, "Berechne.", [
        A("−12 + 5 − 9 + 20 − 6", "−27 + 25", hint="Minus-Zahlen: 12 + 9 + 6 = 27. Plus-Zahlen: 5 + 20 = 25."),
        A("31 − 48 − 13 + 9", "−61 + 40", hint="Minus-Zahlen: 48 + 13 = 61. Plus-Zahlen: 31 + 9 = 40."),
        A("−5,5 + 9,2 − 3,7 + 1", "−9,2 + 10,2", hint="Minus-Zahlen: 5,5 + 3,7 = 9,2. Plus-Zahlen: 9,2 + 1 = 10,2.")], cols=1),
    abschnitt("rechnen", 2, "Verbinde die Rechenarten. Erst Klammern, dann Mal und Geteilt, dann Plus und Minus.", [
        A("−3 · 4 + 15", "−12 + 15", hint="Mal vor Plus: −3 · 4 = −12."),
        A("20 − 6 · (−2)", "20 + 12", hint="Erst 6 · (−2) = −12. Davor steht ein Minus, das Ergebnis wird also 20 + 12."),
        A("−24 : 6 − 5", "−4 − 5", hint="Geteilt vor Minus: −24 : 6 = −4."),
        A("(−8 + 3) · 4", "−5 · 4", hint="Klammer zuerst: −8 + 3 = −5."),
        A("18 − 3 · (4 − 9) − 20 : (−5)", "18 − 3 · (−5) − 20 : (−5)", "18 + 15 + 4", hint="Klammer: 4 − 9 = −5. Dann −3 · (−5) = 15 und −20 : (−5) = 4, mit Minus davor: + 4."),
        A("−2 · (−3 − 5) + 12 : (−3)", "−2 · (−8) + 12 : (−3)", "16 − 4", hint="Klammer: −3 − 5 = −8. Dann −2 · (−8) = 16 und 12 : (−3) = −4.")], cols=1),
    abschnitt("sach", 2, "Temperatur.",
              [dict(text="Morgens zeigt das Thermometer −7 °C. Die Temperatur steigt pro Stunde um 3 Grad.",
                    teile=[("Wie warm ist es nach 4 Stunden?", "−7 + 4 · 3", 5, "°C", "Erst Mal: 4 · 3 = 12 Grad Anstieg, dann −7 + 12 = 5."),
                           ("Danach fällt die Temperatur 6 Stunden lang um je 2 Grad. Wie warm ist es dann?", "5 − 6 · 2", -7, "°C", "Erst Mal: 6 · 2 = 12 Grad Abfall, dann 5 − 12 = −7.")])]),
])

BLAETTER = [BLATT1, BLATT2, BLATT3, BLATT4, BLATT5]

# ---------------------------------------------------------------- Rendern
def kr(stufe):
    return KREIS[stufe]


def kopfzeile(nr, titel, l):
    return (f'<div class="kopf"><b>{"Lösung zu " if l else ""}Blatt {nr}: {titel}</b>'
            f'<span>{"Lerntheke Rationale Zahlen" if not l else "Rechenweg und Hinweis"}</span></div>')


def balken(nr, ab):
    return f'<div class="bal"><b>Nr. {nr}</b><span class="kreis-wrap">{kr(ab["stufe"])}</span><span class="anw">{ab["text"]}</span></div>'


def sach_html(items, l):
    z = ""
    for it in items:
        z += f'<p class="stext">{it["text"]}</p>'
        for i, (frage, rech, erg, einh, hint) in enumerate(it["teile"]):
            assert wert(rech) == F(erg), (rech, erg)
            if l:
                z += (f'<div class="li"><span class="aufg">{"abc"[i]}) &nbsp;{frage}</span><div class="lsg">{zeig(rech)} = {zahl(erg)} {einh}</div>'
                      f'<div class="hint">{hint}</div></div>')
            else:
                z += f'<p class="sfrage">{"abc"[i]}) &nbsp;{frage}</p>'
    return z


def abschnitt_html(nr, ab, l):
    k, items, cols = ab["kind"], ab["items"], ab["cols"]
    kopf = balken(nr, ab)
    if k == "rechnen":
        if not l:
            body = f'<div class="rz c{cols}">' + "".join(f'<span>{"abcdefghijkl"[i]}) &nbsp;{zeig(it["term"])}</span>' for i, it in enumerate(items)) + "</div>"
        else:
            body = '<div class="lz">' + "".join(
                f'<div class="li"><span class="aufg">{"abcdefghijkl"[i]}) &nbsp;{zeig(it["term"])}</span> <span class="lsg">= {" = ".join(it["kette"])}</span>'
                + (f'<div class="hint">{it["hint"]}</div>' if it["hint"] else "") + "</div>" for i, it in enumerate(items)) + "</div>"
    elif k == "vgl":
        zs = []
        for i, (a, b) in enumerate(items):
            w1, w2 = wert(a), wert(b)
            z = "&lt;" if w1 < w2 else ("&gt;" if w1 > w2 else "=")
            zs.append(f'<span class="vg">{"abcdefgh"[i]}) &nbsp;{zeig(a)} <span class="kast">{z if l else ""}</span> {zeig(b)}</span>')
        body = f'<div class="rz c{cols} vgl">' + "".join(zs) + "</div>"
    elif k == "ordnen":
        zs = []
        for i, liste in enumerate(items):
            teile = [t.strip() for t in liste.split(";")]
            if l:
                sortiert = sorted(teile, key=wert)
                zs.append(f'<div class="li"><span class="aufg">{"abc"[i]}) &nbsp;{"; ".join(zeig(t) for t in teile)}</span>'
                          f'<div class="lsg">{" &lt; ".join(zeig(t) for t in sortiert)}</div></div>')
            else:
                zs.append(f'<div class="ord">{"abc"[i]}) &nbsp;{"; ".join(zeig(t) for t in teile)}</div>')
        body = '<div class="lz">' + "".join(zs) + "</div>" if l else "".join(zs)
    elif k == "vz":
        zs = []
        for i, t in enumerate(items):
            w = wert(t)
            vz = "negativ" if w < 0 else "positiv"
            if l:
                zs.append(f'<div class="li"><span class="aufg">{"abcdefgh"[i]}) &nbsp;{zeig(t)}</span> <span class="lsg">= {zahl(w)}, also {vz}</span>'
                          f'<div class="hint">{hinweis(t) or ""}</div></div>')
            else:
                zs.append(f'<span>{"abcdefgh"[i]}) &nbsp;{zeig(t)}</span>')
        body = '<div class="lz">' + "".join(zs) + "</div>" if l else f'<div class="rz c{cols}">' + "".join(zs) + "</div>"
    elif k == "strahl_ab":
        pk = [(b, F(v)) for b, v in items]
        body = f'<div class="zsw">{strahl(ab["lo"], ab["hi"], [(b, v) for b, v in pk])}</div>'
        if l:
            body += '<div class="lsg zl">' + "; &nbsp;".join(f'{b} = {zahl(v)}' for b, v in pk) + "</div>"
    elif k == "strahl_ein":
        pk = [(b, F(v)) for b, v in items]
        werte = "; &nbsp;".join(f'{b} = {zahl(v)}' for b, v in pk)
        body = f'<p class="stext"><b>{werte}</b></p>' + f'<div class="zsw">{strahl(ab["lo"], ab["hi"], pk if l else [], MAG)}</div>'
    elif k == "knobel":
        zs = []
        for i, (frage, erg, wie) in enumerate(items):
            if l:
                zs.append(f'<div class="li"><span class="aufg">{"abcd"[i]}) &nbsp;{frage}</span><div class="lsg">{erg}</div><div class="hint">{wie}</div></div>')
            else:
                zs.append(f'<p class="sfrage">{"abcd"[i]}) &nbsp;{frage}</p>')
        body = "".join(zs)
    elif k == "sach":
        body = sach_html(items, l)
    else:
        raise ValueError(k)
    return f'<div class="abs{" breit" if k.startswith("strahl") else ""}">{kopf}{body}</div>'


def blatt_inhalt(nr, l):
    titel, abs_ = BLAETTER[nr - 1]
    return kopfzeile(nr, titel, l) + "".join(abschnitt_html(i, ab, l) for i, ab in enumerate(abs_, 1)) \
        + (f'<div class="legende">{KREIS[0]} leicht &nbsp;&nbsp; {KREIS[1]} mittel &nbsp;&nbsp; {KREIS[2]} schwer'
           + ('' if l else ' &nbsp;&nbsp; Ins Heft rechnen, Lösung an der Wand.') + "</div>")


CSS = """<style>
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:#d9dde3;font-family:Arial,"Liberation Sans",Helvetica,sans-serif;color:#1b1b1b}
.paar{width:297mm;height:210mm;display:flex;margin:8mm auto;background:#fff;overflow:hidden}
.paar .blatt+.blatt{border-left:.4mm dashed #888}
.blatt{width:148.5mm;height:210mm;padding:7mm 8mm 6mm;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;background:#fff}
.voll{width:210mm;height:297mm;margin:8mm auto;padding:10mm 14mm 8mm;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;background:#fff}
.lblatt{width:210mm;height:297mm;margin:8mm auto;padding:9mm 12mm 8mm;background:#fff;overflow:hidden;display:flex;flex-direction:column;break-after:page}.lblatt:last-child{break-after:auto}
.kopf{display:flex;justify-content:space-between;align-items:baseline;gap:4mm;border-bottom:.8mm solid #1b1b1b;padding-bottom:1.2mm;margin-bottom:1.5mm}
.kopf b{font-size:14pt}.kopf span{font-size:11pt;color:#444;white-space:nowrap}
.lblatt .kopf b{color:#E6007E}
.abs{margin:0 0 1mm}.bal{display:flex;align-items:center;gap:2.5mm;border:.6pt solid #9a9a9a;padding:1mm 2.5mm;margin:0 0 1.6mm;font-size:12pt}
.bal b{font-size:12.5pt;white-space:nowrap}.bal .anw{line-height:1.2}
.kreis{width:1.2em;height:1.2em;vertical-align:-.25em}.kreis-wrap{display:inline-flex}
.rz{display:grid;row-gap:2.3mm;font-size:15pt;white-space:nowrap}
.rz.c1{grid-template-columns:1fr}.rz.c2{grid-template-columns:1fr 1fr}.rz.c3{grid-template-columns:1fr 1fr 1fr}.rz.c4{grid-template-columns:1fr 1fr 1fr 1fr}
.rz.vgl .vg{display:flex;align-items:center}
.kast{display:inline-flex;align-items:center;justify-content:center;width:9mm;height:10.5mm;border:.8pt solid #1b1b1b;margin:0 1.2mm;color:#E6007E;font-weight:700;font-size:13pt}
.br{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.85em;line-height:1.1;margin:0 .1em}
.br span:first-child{border-bottom:1.2px solid currentColor;padding:0 .15em}
.ord{font-size:15pt;margin:0 0 2.6mm;white-space:nowrap}
.zsw{margin:0 0 1mm}.zs{width:100%;display:block}
.stext{font-size:12.5pt;line-height:1.3;margin:0 0 1mm}.sfrage{font-size:12.5pt;line-height:1.3;margin:0 0 1.6mm}
.legende{font-size:11pt;color:#444}.legende .kreis{width:1.1em;height:1.1em}
.lsg{color:#E6007E;font-weight:700}
.lblatt .lz{columns:1}
.lblatt .abs{break-inside:avoid;margin:0 0 3mm}.lblatt .abs.breit{column-span:all}
.lblatt .li{margin:0 0 2mm;break-inside:avoid}
.aufg{font-size:14pt;font-weight:700}.lblatt .lsg{font-size:14pt}.hint{font-size:11.5pt;color:#E6007E;line-height:1.25;margin:0 0 0 7mm}
.zl{font-size:14pt;margin:1mm 0}
.lcols{columns:2;column-gap:9mm;flex:1}
.lblatt .legende{margin-top:auto}
@media print{body{background:#fff}.paar,.voll,.lblatt{margin:0}}
</style>"""


def dokument(titel, koerper, seitenformat):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title>'
            f'<style>@page{{size:{seitenformat};margin:0}}</style>{CSS}</head><body>{koerper}</body></html>')


def paar(a, b):
    return f'<div class="paar"><section class="blatt">{blatt_inhalt(a, False)}</section><section class="blatt">{blatt_inhalt(b, False)}</section></div>'


def voll(nr):
    return f'<section class="voll">{blatt_inhalt(nr, False)}</section>'


SPLIT = {3: 3, 5: 3}      # Lösung zu Blatt 5 braucht zwei Seiten: ab Abschnitt 4 auf Seite 2


def loesungsseiten(nr):
    """Lösungsseiten (A4 hoch): Kopf über beide Spalten, darunter die Abschnitte in zwei Spalten."""
    titel, abs_ = BLAETTER[nr - 1]
    teile = [(1, abs_)] if nr not in SPLIT else [(1, abs_[:SPLIT[nr]]), (SPLIT[nr] + 1, abs_[SPLIT[nr]:])]
    seiten = []
    for k, (start, a) in enumerate(teile):
        zusatz = f" (Seite {k + 1} von {len(teile)})" if len(teile) > 1 else ""
        seiten.append(f'<section class="lblatt">{kopfzeile(nr, titel, True).replace("</b>", zusatz + "</b>", 1)}<div class="lcols">'
                      + "".join(abschnitt_html(i, ab, True) for i, ab in enumerate(a, start))
                      + f'</div><div class="legende">{KREIS[0]} leicht &nbsp;&nbsp; {KREIS[1]} mittel &nbsp;&nbsp; {KREIS[2]} schwer</div></section>')
    return seiten


N_LSG = sum(len(loesungsseiten(i)) for i in range(1, 6))


# ---------------------------------------------------------------- Einstieg: Whiteboard-Runde
# (Aufgabe, "ergebnis" oder "vorzeichen")
WHITEBOARD = [("−4 · 5", "ergebnis"), ("−7 + 3", "ergebnis"), ("−2 · (−3) · (−4)", "vorzeichen"), ("8 − 15", "ergebnis"),
              ("−36 : (−9)", "ergebnis"), ("−5 − 8", "vorzeichen"), ("−2,5 · 4", "ergebnis"), ("10 − (4 − 9)", "ergebnis"),
              ("−6 · (−2) · 5", "vorzeichen"), ("−0,5 − 1,5", "ergebnis")]
assert [zahl(wert(t)) for t, _ in WHITEBOARD] == ["−20", "−4", "−24", "−7", "4", "−13", "−10", "15", "60", "−2"]


def wb_folie(i, l):
    t, art = WHITEBOARD[i]
    w = wert(t)
    frage = "Wie heißt das Ergebnis?" if art == "ergebnis" else "Nur das Vorzeichen: plus oder minus?"
    if art == "ergebnis":
        antwort = zahl(w)
    else:
        antwort = ("minus" if w < 0 else "plus") + f' <span class="wb-klein">(das Ergebnis ist {zahl(w)})</span>'
    return (f'<div class="wb-nr">Aufgabe {i + 1} von 10</div><div class="wb-term">{zeig(t)}</div>'
            + (f'<div class="wb-ans">= <span class="lsg">{antwort}</span></div>' if l else '<div class="wb-ans">&nbsp;</div>')
            + f'<div class="wb-chip {art}">{frage}</div>')


def whiteboard_folien():
    folien = []
    for i in range(10):
        folien.append((f"Whiteboard {i + 1}", wb_folie(i, False)))
        folien.append((f"Whiteboard {i + 1}: Lösung", wb_folie(i, True)))
    return folien


VORZEICHEN = ("<table class='vzt'><tr><th>Rechnung</th><th>Beispiel</th><th>Ergebnis</th></tr>"
              "<tr><td>plus mal plus</td><td>3 · 4 = 12</td><td><b>plus</b></td></tr>"
              "<tr><td>minus mal minus</td><td>−3 · (−4) = 12</td><td><b>plus</b></td></tr>"
              "<tr><td>plus mal minus</td><td>3 · (−4) = −12</td><td><b>minus</b></td></tr>"
              "<tr><td>minus mal plus</td><td>−3 · 4 = −12</td><td><b>minus</b></td></tr></table>"
              "<p class='wb-klein'>Beim Geteilt gilt dieselbe Regel. Bei mehreren Faktoren: Minuszeichen zählen. Gerade Anzahl: plus. Ungerade Anzahl: minus.</p>")

THEKE = ("<ol class='ex'><li>Such dir ein Blatt aus. Die Themen stehen an der Tafel.</li>"
         "<li>Rechne ins Heft: Aufgabe abschreiben, dann lösen.</li>"
         "<li>Die Lösungen hängen an der Wand. Kontrolliere selbst und verbessere mit Farbe.</li>"
         "<li>Fertig? Nimm das nächste Blatt. Blatt 5 mischt alle Themen.</li></ol>"
         "<p class='wb-klein'>○ leicht, ◐ mittel, ● schwer: Du musst nicht alle Aufgaben schaffen.</p>")

FOLIEN = whiteboard_folien() + [("Wiederholung: Plus und Minus", REZEPT_PM), ("Wiederholung: Mal und Geteilt", VORZEICHEN),
                                ("Wiederholung: Gemischte Aufgaben", w7.REZEPT), ("Die Lerntheke", THEKE)]
N_WB = 20

SCHRITTE = [
    ("", "Whiteboard-Runde", 10, "Zehn Kurzaufgaben, Schüler schreiben das Ergebnis oder nur das Vorzeichen aufs Whiteboard und halten es hoch. Danach gleich die Lösungsfolie.", [1]),
    ("", "Fragen der Schüler", 5, "Welche Themen sollen noch einmal drankommen? An der Tafel sammeln.", []),
    ("", "Wiederholung", 10, "Nach den Fragen: Plus und Minus, Mal und Geteilt, Rezept für gemischte Aufgaben. Folien nach Bedarf.", [21, 22, 23]),
    ("", "Lerntheke", 50, "Fünf Blätter liegen vorne, Lösungen hängen an der Wand. Ins Heft rechnen, selbst kontrollieren.", [24]),
    ("", "Abschluss", 10, "Rückmeldung: Wo hakt es noch? Fragen vor der Klassenarbeit sammeln.", []),
    ("", "Puffer", 5, "Zeit für Nachzügler und Aufräumen.", []),
]
assert sum(m for _, _, m, _, _ in SCHRITTE) == 90

EXTRA_CSS = w7.EXTRA_CSS + """<style>
.wb-nr{font-size:20px;color:#66798e;font-weight:700;letter-spacing:.04em}
.wb-term{font-size:84px;font-weight:700;margin:18px 0 22px}
.wb-ans{font-size:46px;font-weight:700;margin:6px 0 14px}.wb-chip{display:inline-block;font-size:30px;font-weight:700;border-radius:30px;padding:6px 26px}
.wb-chip.ergebnis{background:#eef3fb;border:2px solid #1a56a0}.wb-chip.vorzeichen{background:#fdeef6;border:2px solid #E6007E}
.wb-klein{font-size:22px;font-weight:400}
.vzt{border-collapse:collapse;font-size:32px}.vzt th,.vzt td{border:2px solid #1b1b1b;padding:8px 22px;text-align:left}.vzt th{background:#dfe3e8}
.ex li{font-size:30px;margin:12px 0}
.lbl{border:1px solid #cfd6df;border-radius:8px;margin:12px 0;padding:6px 12px}
.lbl h4{margin:6px 0}
.bal{display:flex;align-items:center;gap:10px;border:1px solid #9a9a9a;padding:4px 10px;margin:10px 0 6px;font-size:16px}
.li{margin:6px 0;font-size:18px}.aufg{font-weight:700}.hint{font-size:15px;color:#E6007E;margin-left:24px}
.kreis{width:1.2em;height:1.2em;vertical-align:-.25em}.zs{width:100%;max-width:640px;display:block}
.kast{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border:1.5px solid #1b1b1b;margin:0 6px;color:#E6007E;font-weight:700}
.rz{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:20px}.rz.vgl .vg{display:flex;align-items:center}
</style>"""

FOLIEN_CSS = """<style>
@page{size:13.333in 7.5in;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;color:#1b1b1b}
.slide{width:13.333in;height:7.5in;padding:.55in .8in;break-after:page;overflow:hidden;position:relative}
.slide:last-child{break-after:auto}
.slide .wb-nr{font-size:28px}.slide .wb-term{font-size:150px;margin:30px 0 0;line-height:1.1}.slide .wb-ans{font-size:110px;font-weight:700;margin:0 0 26px;line-height:1.2}.slide .wb-chip{font-size:42px;padding:10px 36px}
.slide .wb-klein{font-size:30px}.slide .vzt{font-size:44px}.slide .ex li{font-size:34px;margin:16px 0;white-space:normal}.slide .ex{padding-right:20px}
.slide .rezept{font-size:34px;padding:14px 34px 22px}.slide .rezept h4{font-size:42px}.slide .rs li{margin:12px 0}
.slide>h1{font-size:30px;margin:0 0 18px;border-bottom:3px solid #1b1b1b;padding-bottom:6px}
.lsg{color:#E6007E;font-weight:700}
.br{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.85em;line-height:1.05;margin:0 .1em}
.br span:first-child{border-bottom:1.5px solid currentColor;padding:0 .15em}
</style>"""


def folien_pdf(ziel):
    tmp, tmp_pdf = HIER / "_w5s2_folien.html", HIER / "_w5s2_folien.pdf"
    tmp.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">{FOLIEN_CSS}{EXTRA_CSS}</head><body>'
                   + "".join(f'<div class="slide"><h1>{t}</h1>{h}</div>' for t, h in FOLIEN) + "</body></html>", encoding="utf-8")
    pdf_aus(tmp, tmp_pdf)
    n = len(PdfReader(str(tmp_pdf)).pages)
    assert n == len(FOLIEN), ("Folie läuft über", n, len(FOLIEN))
    shutil.move(tmp_pdf, ziel)
    tmp.unlink()
    return n


def pdf_aus(html_datei, pdf):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=4000", html_datei.as_uri()], check=True, capture_output=True)


def pdf_bauen(titel, koerper, format_, seiten, ziel):
    tmp, tmp_pdf = HIER / "_w5s2_tmp.html", HIER / "_w5s2_tmp.pdf"
    tmp.write_text(dokument(titel, koerper, format_), encoding="utf-8")
    pdf_aus(tmp, tmp_pdf)
    n = len(PdfReader(str(tmp_pdf)).pages)
    tmp.unlink()
    assert n == seiten, (ziel.name, "Seitenzahl", n, seiten)
    shutil.move(tmp_pdf, ziel)
    return n


def pruefe_ueberlauf():
    """Misst jede Seite im Browser: nichts darf über den Seitenrand hinauslaufen."""
    teile = [("paar", paar(1, 2)), ("paar", paar(3, 4)), ("voll", voll(5))] + [("l", x) for i in range(1, 6) for x in loesungsseiten(i)]
    skript = ("<script>document.querySelectorAll('.blatt,.voll,.lblatt').forEach((s,i)=>{let c=s.querySelector('.lcols');let f=Math.max(s.scrollHeight-s.clientHeight,c?c.scrollWidth-c.clientWidth:0);"
              "let b=document.createElement('pre');b.className='mess';b.textContent='Seite '+i+' ueberlauf='+f;document.body.appendChild(b)})</script>")
    tmp = HIER / "_w5s2_mess.html"
    tmp.write_text(dokument("mess", "".join(t for _, t in teile), "A4") + skript, encoding="utf-8")
    aus = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=3000", "--dump-dom", tmp.as_uri()],
                         capture_output=True, text=True).stdout
    tmp.unlink()
    return re.findall(r'class="mess">([^<]*)', aus)


def ordner_lsg_html():
    return "".join(f'<div class="lbl"><h4>Blatt {i}: {BLAETTER[i - 1][0]}</h4>'
                   + "".join(abschnitt_html(k, ab, True) for k, ab in enumerate(BLAETTER[i - 1][1], 1)) + "</div>" for i in range(1, 6))


def main():
    ueber = pruefe_ueberlauf()
    print("Überlaufprüfung:", ueber)
    schlecht = [u for u in ueber if not u.endswith("=0")]
    assert not schlecht, schlecht
    pdf_bauen(f"{NAME} Blatt 1 und 2", paar(1, 2), "A4 landscape", 1, HIER / f"{NAME} – Lerntheke Blatt 1 und 2 (A4 quer, in der Mitte schneiden).pdf")
    pdf_bauen(f"{NAME} Blatt 3 und 4", paar(3, 4), "A4 landscape", 1, HIER / f"{NAME} – Lerntheke Blatt 3 und 4 (A4 quer, in der Mitte schneiden).pdf")
    pdf_bauen(f"{NAME} Blatt 5", voll(5), "A4", 1, HIER / f"{NAME} – Lerntheke Blatt 5 gemischt (A4 hoch).pdf")
    pdf_bauen(f"{NAME} Lösungen", "".join(x for i in range(1, 6) for x in loesungsseiten(i)), "A4", N_LSG, HIER / f"{NAME} – Lerntheke Lösungen zum Aushängen.pdf")
    print("Folien:", folien_pdf(HIER / f"{NAME} – Folien für den Beamer.pdf"), "Seiten")
    vb = [("Drucken", "Blatt 1 und 2 (A4 quer) 26×, Blatt 3 und 4 (A4 quer) 26×, Blatt 5 (A4 hoch) 26×. Die zwei Querblätter in der Mitte durchschneiden."),
          ("Aushang", "Lösungen zum Aushängen: 5 Seiten A4, einmal ausdrucken und an die Wand hängen (Reihenfolge Blatt 1 bis 5)."),
          ("Digital", f"Folien-PDF in Notability: {NAME} – Folien für den Beamer.pdf (20 Whiteboard-Folien, dann Wiederholung und Lerntheke)."),
          ("Material", "Mini-Whiteboards und Stifte für die Whiteboard-Runde, Klebeband für den Aushang."),
          ("Voraussetzung", "Alle Rechenarten sind eingeführt, Rezept für gemischte Aufgaben ist in Stunde 1 gelaufen.")]
    tafel = ('<div class="tafel"><h4>Tafel: Themenspeicher für die Lerntheke</h4><ol class="ex" style="font-size:22px">'
             "<li>Zahlenstrahl, Vergleichen, Ordnen</li><li>Addieren und Subtrahieren</li><li>Multiplizieren und Dividieren</li>"
             "<li>Sachaufgaben</li><li>Gemischte Aufgaben</li></ol><p>Daneben: Fragen der Schüler sammeln.</p></div>")
    merk = '<div class="box"><p>In dieser Stunde gibt es keinen neuen Merkheft-Eintrag. Die Merksätze stehen im Merkheft aus den Stunden davor.</p></div>'
    wb_l = "".join(f'<li>{zeig(t)} = <span class="lsg">{zahl(wert(t))}</span>{" (Vorzeichen: " + ("minus" if wert(t) < 0 else "plus") + ")" if art == "vorzeichen" else ""}</li>'
                   for t, art in WHITEBOARD)
    loes = f'<div class="box"><h3>Whiteboard-Runde</h3><ol type="a" class="ex">{wb_l}</ol></div><div class="box"><h3>Lerntheke: Lösungsblätter</h3>{ordner_lsg_html()}</div>'
    bau_woche(HIER / f"{NAME}.html", "Woche 5, Stunde 2: Übungsstunde mit Lerntheke",
              "Klasse 7c, Mathematik, Woche 5 vor der KA 1, Doppelstunde: Whiteboard-Runde, Wiederholung, Lerntheke mit fünf Blättern",
              vb, SCHRITTE, FOLIEN, tafel=tafel, merkheft=merk, loesungen=loes, extra_css=EXTRA_CSS)


if __name__ == "__main__":
    if "--messen" in sys.argv:
        print(pruefe_ueberlauf())
    else:
        main()
