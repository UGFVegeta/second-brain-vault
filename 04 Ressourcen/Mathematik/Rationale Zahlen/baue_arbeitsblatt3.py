#!/usr/bin/env python3
"""Arbeitsblatt „Klammern und Rechenvorteile“ (Woche 3, Schwerpunkt Minusklammer), A4, dazu die Lösungsfassung
(Lösungen blau im Blatt, taugt direkt als Folie zur Kontrolle). Stil wie baue_arbeitsblatt2.py, ohne Buch-Klammerschreibweise.
Alle Ergebnisse werden hier nachgerechnet (rechne), damit kein Rechenfehler auf dem Blatt steht.
Aufruf: python3 baue_arbeitsblatt3.py  -> Rationale Zahlen 3 – Arbeitsblatt Klammern.pdf und … – Lösungen.pdf"""
import re, subprocess, sys
from fractions import Fraction
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
from mathe_woche_vorlage import aus_skript  # noqa: E402

m, kreis, buchstabe = aus_skript(HIER / "baue_arbeitsblatt2.py", "m", "kreis", "buchstabe")
ACC = "#12909e"
NAME = "Rationale Zahlen 3 – Arbeitsblatt Klammern"


def rechne(t):
    """Wert eines Terms in Schulschreibweise (−, Komma) exakt als Bruch."""
    t = t.replace("−", "-").replace(",", ".")
    t = re.sub(r"(\d+(?:\.\d+)?)", r'Fraction("\1")', t)
    return eval(t, {"Fraction": Fraction})


def zahl(v):
    v = Fraction(v)
    return m(int(v)) if v.denominator == 1 else m(float(v))


def aufloesen(t):
    """Klammer auflösen: Plusklammer lässt die Zeichen, Minusklammer dreht alle Zeichen in der Klammer um."""
    # gezielte Umsetzung für genau eine Klammer im Term
    a, rest = t.split("(", 1)
    innen, b = rest.split(")", 1)
    a = a.rstrip()
    vor = a[-1] if a and a[-1] in "+−" else "+"
    a = a[:-1].rstrip() if a and a[-1] in "+−" else a
    teile = innen.strip().split(" ")
    if teile[0][0] not in "+−":
        teile = ["+", teile[0]] + teile[1:]
    elif len(teile[0]) > 1:
        teile = [teile[0][0], teile[0][1:]] + teile[1:]
    neu = []
    for j in range(0, len(teile), 2):
        z, w = teile[j], teile[j + 1]
        if vor == "−":
            z = "+" if z == "−" else "−"
        neu.append(f"{z} {w}")
    kette = " ".join(neu)
    if not a:
        kette = kette[2:] if kette.startswith("+ ") else "−" + kette[2:]
        s = f"{kette}{b}"
    else:
        s = f"{a} {kette}{b}"
    assert rechne(s) == rechne(t), (t, s)
    return s


# ------------------------------------------------------------------ Aufgaben
A1 = ["−14 + 52 − 6 + 8", "25 − 18 + 75", "−9 + 14 − 11", "47 − 26 + 53",
      "−38 + 19 − 62", "64 − 35 + 36 − 15", "−12 + 45 − 28 + 5", "2,5 − 7 + 7,5"]
A2 = [("−8 + 15 = 15 − 8", "Vertauschungsgesetz"), ("(−7 + 9) − 3 = −7 + (9 − 3)", "Verbindungsgesetz"),
      ("12 − 30 + 8 = 12 + 8 − 30", "Vertauschungsgesetz"), ("(−25 − 15) + 60 = −25 + (−15 + 60)", "Verbindungsgesetz"),
      ("−4 + 11 − 6 = 11 − 4 − 6", "Vertauschungsgesetz"), ("(13 + 7) − 20 = 13 + (7 − 20)", "Verbindungsgesetz")]
A3 = [("50 − 12 − 8", "50 − (12 + 8)"), ("100 − 36 − 14", "100 − (36 + 14)"), ("75 − 25 − 30 − 20", "75 − (25 + 30 + 20)"),
      ("40 − 17 − 13 − 25", "40 − (17 + 13 + 25)"), ("60 − 35 − 45", "60 − (35 + 45)"), ("9 − 2,5 − 1,5", "9 − (2,5 + 1,5)")]
A4 = ["20 + (15 − 10)", "20 − (15 − 10)", "20 − (15 + 10)", "20 − (−15 + 10)",
      "30 − (12 − 20)", "−8 − (4 + 6)", "−8 − (4 − 6)", "−8 − (−4 − 6)"]
A5 = ["45 − (20 − 15 + 5)", "−12 − (8 − 30 + 4)", "3,5 − (1,5 − 4)", "−0,6 − (−2,4 + 1)", "100 − (−25 − 25 + 50)", "−7 − (−7 − 7)"]
A6 = [("30 − (10 − 4) = 30 − 10 − 4 = 16", "30 − (10 − 4)"), ("12 − (−5 + 3) = 12 − 5 + 3 = 10", "12 − (−5 + 3)"),
      ("−6 − (2 + 9) = −6 − 2 + 9 = 1", "−6 − (2 + 9)"), ("25 + (−10 − 5) = 25 + 10 + 5 = 40", "25 + (−10 − 5)")]
A7 = [("20 − 8 + 5", 7, "20 − (8 + 5)"), ("15 − 9 − 4", 10, "15 − (9 − 4)"),
      ("−6 − 3 + 10", -19, "−6 − (3 + 10)"), ("40 − 12 − 8 + 5", 15, "40 − 12 − (8 + 5)")]
A8 = [("Tim hat 40 €. Er kauft ein Spiel für 25 € und eine Hülle für 7 €. Schreibe eine Rechnung mit Minusklammer. Wie viel Geld hat er noch?",
       "40 − (25 + 7) = 40 − 32 = 8", "Tim hat noch 8 €."),
      ("Auf Lenas Konto sind 15 €. Die Bank bucht 30 € ab, zahlt davon aber 12 € zurück. Schreibe eine Rechnung mit Minusklammer. Wie ist der Kontostand?",
       "15 − (30 − 12) = 15 − 30 + 12 = −3", "Der Kontostand ist −3 €.")]

# Prüfungen
for t, gesetz in A2:
    l, r = t.split(" = ")
    assert rechne(l) == rechne(r), t
for t, k in A3:
    assert rechne(t) == rechne(k), t
for t, soll, lsg in A7:
    assert rechne(lsg) == soll and rechne(t) != soll, t
for t, rech, _ in A8:
    teile = rech.split(" = ")
    assert len({rechne(x) for x in teile}) == 1, t


def reihe(items, cols, loesung, fn):
    out = []
    for i, it in enumerate(items):
        aufg, lsg = fn(it)
        rest = f'<b class="l">{lsg}</b>' if loesung else '<span class="blank"></span>'
        out.append(f'<div class="it"><span class="b">{buchstabe(i)})</span> {aufg} = {rest}</div>')
    return f'<div class="cols c{cols}">{"".join(out)}</div>'


def aufgabe(nr, stufe, text, inhalt, bsp=""):
    return (f'<div class="auf"><div class="kopf">{kreis(stufe)}<span class="nr">{nr}</span><span class="txt">{text}</span></div>'
            f'{f"<div class=bsp>{bsp}</div>" if bsp else ""}{inhalt}</div>')


def blatt(loesung):
    g = not loesung  # Schülerfassung: groß, mit Platz für den Rechenweg, auf zwei Seiten (Vorder-/Rückseite)
    a = [aufgabe(1, 0, "Rechne geschickt: Vertausche die Zahlen samt Zeichen und fasse passend zusammen.",
                 reihe(A1, 2 if g else 4, loesung, lambda t: (t, zahl(rechne(t))))),
         aufgabe(2, 0, "Welches Rechengesetz wurde benutzt? Schreibe den Namen dazu.",
                 '<div class="cols c1">' + "".join(
                     f'<div class="it"><span class="b">{buchstabe(i)})</span> {t} <span class="pf">&rarr;</span> '
                     + (f'<b class="l">{g}</b>' if loesung else '<span class="blank long"></span>') + "</div>"
                     for i, (t, g) in enumerate(A2)) + "</div>"),
         aufgabe(3, 0, "Fasse alle Zahlen, die abgezogen werden, in einer Minusklammer zusammen. Rechne dann.",
                 reihe(A3, 1 if g else 2, loesung, lambda x: (x[0], f"{x[1]} = {zahl(rechne(x[0]))}")),
                 bsp="Beispiel: 87 − 45 − 32 − 23 = 87 − (45 + 32 + 23) = 87 − 100 = −13"),
         ('<div class="umbruch"></div>' if g else "") + aufgabe(4, 1, "Löse die Klammer auf und rechne. Achtung: Ein Minus vor der Klammer dreht <b>alle</b> Zeichen in der Klammer um.",
                 reihe(A4, 2, loesung, lambda t: (t, f"{aufloesen(t)} = {zahl(rechne(t))}"))),
         aufgabe(5, 1, "Noch einmal, jetzt mit mehr Zahlen in der Klammer.",
                 reihe(A5, 2, loesung, lambda t: (t, f"{aufloesen(t)} = {zahl(rechne(t))}"))),
         aufgabe(6, 1, 'Hier hat sich ein <span class="rot">Fehler</span> eingeschlichen. Korrigiere.',
                 '<div class="cols c1">' + "".join(
                     f'<div class="it"><span class="b">{buchstabe(i)})</span> <span class="fehl">{f}</span> <span class="pf">&rarr;</span> '
                     + (f'<b class="l">{aufloesen(t)} = {zahl(rechne(t))}</b>' if loesung else '<span class="blank long2"></span>') + "</div>"
                     for i, (f, t) in enumerate(A6)) + "</div>"),
         aufgabe(7, 2, "Setze eine Klammer so, dass das Ergebnis stimmt.",
                 '<div class="cols c2">' + "".join(
                     f'<div class="it"><span class="b">{buchstabe(i)})</span> '
                     + (f'<b class="l">{lsg}</b>' if loesung else t) + f" = {zahl(soll)}</div>"
                     for i, (t, soll, lsg) in enumerate(A7)) + "</div>"),
         aufgabe(8, 2, "Löse die Sachaufgaben. Schreibe die Rechnung und einen Antwortsatz auf.",
                 "".join(f'<div class="sach"><span class="b">{buchstabe(i)})</span> {t}<div class="ls">'
                         + (f'<b class="l">{r}. {ant}</b>' if loesung else '<span class="zl"></span>' * 3) + "</div></div>"
                         for i, (t, r, ant) in enumerate(A8)))]
    titel = "Klammern und Rechenvorteile" + (" – Lösungen" if loesung else "")
    name = "" if loesung else '<div class="name">Name: ______________________ &nbsp;&nbsp; Datum: ____________</div>'
    return f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title><style>{CSS}{ENG if loesung else GROSS}</style></head><body>
<div class="seite"><header><div><h1>{titel}</h1><div class="sub">Klasse 7c, Rationale Zahlen</div></div>{name}</header>
<div class="legende">Schwierigkeit: {kreis(0)} leicht &nbsp;&nbsp; {kreis(1)} mittel &nbsp;&nbsp; {kreis(2)} schwer</div>
{"".join(a)}</div></body></html>"""


CSS = f"""
@page{{size:A4;margin:10mm 12mm}}
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{margin:0;font:11pt/1.3 Helvetica,Arial,sans-serif;color:#1b1b1b}}
header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #1b1b1b;padding-bottom:4px}}
h1{{font-size:17pt;margin:0;color:{ACC}}}.sub{{color:#555;font-size:10pt}}
.name{{font-size:10.5pt;color:#333;white-space:nowrap}}
.legende{{font-size:9.5pt;color:#333;margin:5px 0 2px}}
.lvl{{vertical-align:-3px}}
.auf{{margin:9px 0 0;break-inside:avoid}}
.kopf{{display:flex;align-items:center;gap:6px;margin-bottom:2px}}
.nr{{font-size:14pt;font-weight:700;color:{ACC};min-width:14px}}
.txt{{font-size:11pt}}.rot{{color:#c0271c;font-weight:700}}
.bsp{{padding-left:24px;font-size:10pt;color:#444;margin-bottom:2px}}
.cols{{display:grid;gap:3px 14px;padding-left:24px}}
.c4{{grid-template-columns:repeat(4,1fr)}}.c2{{grid-template-columns:repeat(2,1fr)}}.c1{{grid-template-columns:1fr}}
.it{{white-space:nowrap;padding:4px 0}}
.b{{color:#333}}
.blank{{display:inline-block;width:16mm;border-bottom:1px solid #444;height:1em}}
.blank.long{{width:40mm}}.blank.long2{{width:60mm}}
.c2 .blank{{width:48mm}}
.l{{color:#1d5fa8}}
.fehl{{color:#333}}.pf{{margin:0 5px;color:#666}}
.sach{{padding:2px 0 0 24px}}.sach .ls{{padding:4px 0 0}}
.zl{{display:block;border-bottom:1px solid #999;height:24px;margin-bottom:4px}}
"""


ENG = "body{font-size:10pt}.txt{font-size:10pt}.it{padding:1px 0}.auf{margin:4px 0 0}.kopf{margin-bottom:1px}.sach .ls{padding:1px 0 0}"  # Lösungsfassung etwas enger, damit sie auf eine Seite passt


# Schülerfassung: größere Schrift, hohe Zeilen mit Platz für den Rechenweg, Umbruch nach Aufgabe 3 (Vorder-/Rückseite)
GROSS = """
body{font-size:12.5pt}h1{font-size:20pt}.sub{font-size:11pt}.name{font-size:12pt}.legende{font-size:10.5pt;margin:7px 0 0}
.txt{font-size:12.5pt}.nr{font-size:16pt;min-width:18px}.bsp{font-size:11.5pt;padding-left:28px}
.auf{margin:12px 0 0}.kopf{gap:8px;margin-bottom:3px}
.cols{padding-left:28px;gap:0 22px}
.it{display:flex;align-items:flex-end;gap:6px;min-height:12.5mm;padding:0 0 1mm}
.c1 .it{min-height:11mm}
.blank,.blank.long,.blank.long2,.c2 .blank{flex:1;width:auto;min-width:18mm;display:block;height:1.2em;align-self:flex-end}
.umbruch{break-before:page;height:0}
.sach{padding:3px 0 0 28px}.zl{height:9.5mm;margin-bottom:0}
.sach .ls{padding:0}.sach{margin-bottom:5mm}
"""


def main():
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    for loesung, datei in ((False, NAME), (True, NAME + " – Lösungen")):
        h = HIER / f"{datei}.html"
        h.write_text(blatt(loesung), encoding="utf-8")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / (datei + '.pdf')}",
                        h.as_uri()], check=True, capture_output=True)
        print("geschrieben:", datei + ".pdf")


if __name__ == "__main__":
    main()
