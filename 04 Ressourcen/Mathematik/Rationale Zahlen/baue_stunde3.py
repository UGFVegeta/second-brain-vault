#!/usr/bin/env python3
"""Rationale Zahlen 3: IF-Stunde am Montag (halbe Klasse, zweimal hintereinander gleich), Plus und Minus üben.
HA-Kontrolle Arbeitsblatt „Plus und Minus“, Blitzrunde Subtraktion, Übung ○◐● ins Übungsheft, Vorschau Rechenvorteile.
Kein neues Blatt: Die Aufgaben stehen auf den Folien. Stil und CSS wie baue_stunde2.py (CSS wird von dort gelesen, ohne es auszuführen).
Aufruf: python3 baue_stunde3.py  -> Rationale Zahlen 3 – IF-Stunde Üben – ALLES.html, Folien-HTML und Folien-PDF"""
import ast, re, subprocess
from pathlib import Path

HIER = Path(__file__).parent


def css_aus(datei, name):
    for n in ast.parse((HIER / datei).read_text(encoding="utf-8")).body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == name:
            return ast.literal_eval(n.value)


CSS = css_aus("baue_stunde2.py", "CSS") + """
.br{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.85em;line-height:1.05;margin:0 .1em}
.br span:first-child{border-bottom:1.5px solid currentColor;padding:0 .15em}
.spalten{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.spalten h4{margin:0 0 6px}
.spalten ol{margin:0;padding-left:22px}.spalten li{margin:4px 0}
.lsg{color:#b3261e;font-weight:700}
"""
UE = '<span class="chip ueb">Übungsheft</span>'
KREIS = {0: "○", 1: "◐", 2: "●"}


def br(z, n, minus=False):
    return f'{"−" if minus else ""}<span class="br"><span>{z}</span><span>{n}</span></span>'


# ------------------------------------------------------------------ Aufgaben (Aufgabe, Lösung)
HA = [  # Hausaufgabe: Arbeitsblatt Plus und Minus, nur Ergebnisse für die Kontrolle
    ("1", "a) 20; b) −25; c) −15; d) 12; e) −5; f) −14; g) −15; h) 0"),
    ("2", "a) 18; b) 5; c) −10; d) −12; e) −60; f) −4; g) −20; h) −7"),
    ("3", "a) −23; b) −27; c) −81; d) 22; e) −45; f) −210"),
    ("4", "a) 6; b) −8; c) −25; d) −16; e) −4"),
    ("5", f"a) −2,7; b) −1,3; c) −9,75; d) 0,42; e) {br(1, 4, True)}; f) {br(3, 5, True)}; g) {br(1, 6, True)}; h) {br(17, 12, True)} = −1{br(5, 12)}"),
    ("6", "a) −7 + 11 − 9 = −5, abends −5 °C; b) −120 + 250 − 180 = −50, Kontostand −50 €"),
]
BLITZ = [("5 − 12", "−7"), ("−4 − 7", "−11"), ("12 − 25", "−13"), ("−25 − 25", "−50"),
         ("0 − 17", "−17"), ("−8 − 0,5", "−8,5"), ("1,5 − 4", "−2,5"), ("−12 − 18", "−30")]
UEB = {
    0: [("9 − 15", "−6"), ("−6 − 8", "−14"), ("20 − 35", "−15"), ("−12 − 12", "−24"),
        ("7 − 21", "−14"), ("−30 − 5", "−35"), ("4 − 13", "−9"), ("−1 − 19", "−20")],
    1: [("3,5 − 7", "−3,5"), ("−4,2 − 1,8", "−6"), ("45 − 80", "−35"), ("−2,5 − 7,5", "−10"),
        ("0,3 − 1", "−0,7"), ("−6,4 − 0,6", "−7"), (f"{br(1, 2)} − {br(3, 4)}", br(1, 4, True)), (f"{br(1, 3, True)} − {br(1, 3)}", br(2, 3, True))],
    2: [("12 − 20 − 7", "−15"), ("−5 − 8 + 20 − 30", "−23"),
        ("+ oder −? 8 ☐ 15 ☐ 4 = −11", "8 − 15 − 4 = −11"), ("+ oder −? −3 ☐ 7 ☐ 12 = 2", "−3 − 7 + 12 = 2"),
        ("U-Boot bei −120 m: Es steigt 45 m, dann sinkt es 80 m. Wo ist es jetzt?", "−120 + 45 − 80 = −155, bei −155 m"),
        ("Aufzug im 2. Stock: 3 Stockwerke runter, dann noch 1. Wo hält er?", "2 − 3 − 1 = −2, im 2. Untergeschoss")],
}
TEASER = ("Rechne möglichst geschickt: −17 + 36 − 3 + 4", "−17 − 3 = −20 und 36 + 4 = 40, also −20 + 40 = 20")


def liste(xs, loes=False):
    """Kurze Rechenaufgaben: Lösung direkt dahinter; Text- und Einsetzaufgaben: Lösung in der Zeile darunter."""
    def kurz(a):
        return len(re.sub(r"<[^>]+>", "", a)) < 30 and "☐" not in a
    def li(a, b):
        if not loes:
            return f"<li>{a}</li>"
        return f"<li>{a} = <span class=lsg>{b}</span></li>" if kurz(a) else f"<li>{a}<br><span class=lsg>{b}</span></li>"
    return "<ol type='a'>" + "".join(li(a, b) for a, b in xs) + "</ol>"


def ueb_folie(loes):
    sp = "".join(f'<div><h4>{KREIS[k]} {["leicht", "mittel", "schwer"][k]}</h4>{liste(UEB[k], loes)}</div>' for k in (0, 1, 2))
    return f'<div class="spalten">{sp}</div>'


# ------------------------------------------------------------------ Verlauf
def grp(nr, titel, t0, t1):
    return f'<tr class="grp"><td colspan="4">{nr} · {titel}<span>Minute {t0}–{t1}</span></td></tr>'


def vz(m, was, mat, wer):
    return f'<tr><td class="mn">{m}′</td><td>{was}</td><td>{mat}</td><td>{wer}</td></tr>'


VERLAUF = "".join([
    grp(0, "Start", 0, 3),
    vz(3, "Ankommen, Ziel ansagen: „Heute wird Plus und Minus sicher, besonders das Minus.“", "Übungsheft, Arbeitsblatt (HA)", "Plenum"),
    grp(1, "Hausaufgabe kontrollieren", 3, 18),
    vz(6, "Folie 1 zeigen. Jeder kontrolliert sein Blatt selbst mit andersfarbigem Stift, falsch = Kringel.", "Folie 1", "einzeln"),
    vz(4, "Handzeichen pro Aufgabe: „Wer hatte bei Nr. 2 mindestens einen Fehler?“ Die Zahl pro Aufgabe notierst du dir, ohne Namen.", "Strichliste", "Plenum"),
    vz(5, "Die zwei Aufgaben mit den meisten Fehlern an der Zahlengerade vorrechnen lassen (Bogen nach links und rechts).", "Tafel", "Plenum"),
    grp(2, "Blitzrunde Subtraktion", 18, 25),
    vz(5, "Folie 2: acht Aufgaben, nur Minus. Ergebnis ins Übungsheft, ohne Rechenweg, ein Tempo für alle.", f"Folie 2 · {UE}", "einzeln"),
    vz(2, "Folie 3: Lösungen, selbst abhaken. Wer 7 oder 8 richtig hat, darf gleich mit ◐ starten.", "Folie 3", "einzeln"),
    grp(3, "Üben nach Schwierigkeit", 25, 40),
    vz(15, "Folie 4: Jeder wählt seinen Einstieg (○, ◐ oder ●) und rechnet ins Übungsheft. Du gehst herum, in der Halbgruppe ist Zeit für Einzelne.",
       f"Folie 4 · {UE}", "einzeln"),
    grp(4, "Kontrolle und Vorschau", 40, 45),
    vz(3, "Folie 5: Lösungen zeigen, selbst kontrollieren.", "Folie 5", "einzeln"),
    vz(2, "Folie 6: Wer findet einen schnellen Weg? Nur Ideen sammeln, das ist der Einstieg am Donnerstag (Rechenvorteile).", "Folie 6 (Lösung Folie 7)", "Plenum"),
])

HA_TAB = "".join(f"<tr><td><b>{n}</b></td><td>{l}</td></tr>" for n, l in HA)
BLITZ_A = "<ol type='a' class='kl'>" + "".join(f"<li>{a} =</li>" for a, _ in BLITZ) + "</ol>"
BLITZ_L = "<ol type='a' class='kl'>" + "".join(f"<li>{a} = <span class=lsg>{b}</span></li>" for a, b in BLITZ) + "</ol>"

FOLIEN = [
    ("Hausaufgabe: Lösungen", f"<table>{HA_TAB}</table>"),
    ("Blitzrunde: nur Minus", BLITZ_A),
    ("Blitzrunde: Lösungen", BLITZ_L),
    ("Üben: Wähle deinen Einstieg", ueb_folie(False)),
    ("Üben: Lösungen", ueb_folie(True)),
    ("Geht das schneller?", f'<div class="ausdruck">{TEASER[0].split(": ")[1]}</div><p>{TEASER[0].split(":")[0]}. Wie würdest du vorgehen?</p>'),
    ("Geht das schneller? Lösung", f'<div class="ausdruck">{TEASER[0].split(": ")[1]} = <span class="lsg">20</span></div><p>{TEASER[1]}.</p>'
     '<p>Die Zahlen samt Zeichen umsortieren, dann gehen die Rechnungen glatt auf. Am Donnerstag lernen wir, wie diese Rechengesetze heißen.</p>'),
]


def seite():
    folien = "".join(f'<div class="folie"><h3>Folie {i} · {t}</h3>{inh}</div>' for i, (t, inh) in enumerate(FOLIEN, 1))
    vorher = f"""<section id="vorher"><h2>Vor der Stunde</h2>
<p class="lead">Montag, IF-Stunde: 5. und 6. Stunde je eine Klassenhälfte, beide Male derselbe Ablauf.</p>
<div class="nichts"><b>Nichts zu drucken.</b> Alle Aufgaben stehen auf den Folien, gerechnet wird im Übungsheft.</div>
<h3>Digital vorbereiten</h3><table><tr><th>Was</th><th>Wo, wie</th></tr>
<tr><td>Folien in Notability importieren</td><td>Rationale Zahlen 3 – Folien für den Beamer.pdf</td></tr>
<tr><td>Strichliste für die HA-Fehler</td><td>Zettel mit Nr. 1 bis 6, je Halbgruppe eine Spalte. Ergibt einen ersten Hinweis für die spätere Einteilung nach Leistung.</td></tr></table>
<h3>Im Raum</h3><ul><li>Beamer und Spiegelung vom iPad</li><li>Die Schüler haben: Arbeitsblatt (HA), Übungsheft, zweiten Stift in anderer Farbe</li></ul></section>"""
    verlauf = f"""<section id="verlauf"><h2>Verlauf</h2><p class="lead">45 Minuten, halbe Klasse. Beim zweiten Durchgang gleich.</p>
<table class="vt"><tr><th>Min</th><th>Was</th><th>Material</th><th>Wer</th></tr>{VERLAUF}</table>
<div class="warn"><b>Typische Fehler beim Minus:</b> Bei 14 − 30 wird 16 statt −16 gerechnet (Bogen läuft über die Null). Bei −3 − 9 wird −3 + 9 gerechnet
(„minus minus gibt plus“, gilt hier nicht, weil keine Klammer dasteht). Immer fragen: In welche Richtung geht der Bogen?</div></section>"""
    return f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rationale Zahlen 3 – IF-Stunde Üben</title><style>{CSS}</style></head><body>
<div class="wrap"><header class="kopf"><h1>Rationale Zahlen 3: Plus und Minus üben</h1>
<p class="sub">Klasse 7c · Mo 28.09.2026, IF-Stunde (zwei Halbgruppen) · Woche 3 · alles in einer Datei</p></header></div>
<nav><div class="wrap"><a href="#vorher">Vor der Stunde</a><a href="#verlauf">Verlauf</a><a href="#folien">Folien mit Lösungen</a></div></nav>
<div class="wrap">{vorher}{verlauf}
<section id="folien"><h2>Folien mit Lösungen</h2><p class="lead">Als PDF für den Beamer: Rationale Zahlen 3 – Folien für den Beamer.pdf</p>{folien}</section>
<footer>Generator: baue_stunde3.py</footer></div></body></html>"""


FCSS = """@page{size:13.333in 7.5in;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:-apple-system,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#1b1b1b}
.slide{width:13.333in;height:7.5in;padding:.45in .7in;page-break-after:always;overflow:hidden;font-size:27px;line-height:1.45}
.slide:last-child{page-break-after:auto}h1{font-size:44px;margin:0 0 .25in}
table{border-collapse:collapse;width:100%;font-size:29px}td{padding:10px 14px;border-bottom:1px solid #ddd;vertical-align:top}
.kl{columns:2;column-gap:1in;font-size:34px}.kl li{margin:.08in 0}
.spalten{display:grid;grid-template-columns:repeat(3,1fr);gap:.35in;font-size:22px;line-height:1.35}.spalten h4{font-size:27px;margin:0 0 .08in}
.spalten ol{margin:0;padding-left:30px}.spalten li{margin:3px 0}
.ausdruck{font-size:52px;font-weight:700;margin:.3in 0 .2in}.lsg{color:#b3261e;font-weight:700}
.br{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.8em;line-height:1.05;margin:0 .1em}
.br span:first-child{border-bottom:2px solid currentColor;padding:0 .15em}"""


def main():
    ziel = HIER / "Rationale Zahlen 3 – IF-Stunde Üben – ALLES.html"
    ziel.write_text(seite(), encoding="utf-8")
    fol = HIER / "Folien – IF-Stunde Üben.html"
    fol.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>Folien IF-Stunde</title><style>{FCSS}</style></head><body>'
                   + "".join(f'<div class="slide"><h1>{t}</h1>{inh}</div>' for t, inh in FOLIEN) + "</body></html>", encoding="utf-8")
    pdf = HIER / "Rationale Zahlen 3 – Folien für den Beamer.pdf"
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", fol.as_uri()], check=True, capture_output=True)
    print("geschrieben:", ziel.name, "·", fol.name, "·", pdf.name)


if __name__ == "__main__":
    main()
