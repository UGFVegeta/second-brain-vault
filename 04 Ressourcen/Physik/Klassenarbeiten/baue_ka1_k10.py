#!/usr/bin/env python3
"""Physik Klassenarbeit Nr. 1, Klasse 10, Kernphysik (W10, Woche ab 23.11.2026).
Stoff W01 bis W09: Atombau, Isotope, Nullrate, α/β/γ, Zerfallsgleichungen, Zerfallsreihe, Halbwertszeit, Aktivität.
40 Punkte, 45 Minuten, 4 Seiten. Aufbau wie Oskars frühere Arbeiten (Kopfkasten, Punkte je Aufgabe, Seitensummen).
Erzeugt drei HTML-Dateien: Arbeit, Lösung mit Erwartungshorizont, „Was muss ich wissen?“.
PDFs erst nach Freigabe: python3 baue_ka1_k10.py pdf"""
import re, subprocess, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent / "Kernphysik" / "Materialien"))
from baue_blaetter_k10 import EXTRA, kreis, nk, MAG  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CSS = "../Optik/Materialien/ab-vorlage.css"
NAME = "Klassenarbeit Nr. 1 Klasse 10 Kernphysik 2026"
KA_CSS = """<style>
.kabox{border:1pt solid #14171c;padding:3mm 4mm;margin-bottom:3mm;font-size:10pt}
.kabox .z1{display:flex;justify-content:space-between;font-weight:600;font-size:11.5pt;margin-bottom:3mm}
.kabox .z2{display:grid;grid-template-columns:2fr .8fr 1fr 1.3fr 1.6fr;gap:4mm}
.kabox .f{border-bottom:.6pt solid #14171c;padding-top:4mm;color:#66798E;font-size:8.5pt}
.hinweise{font-size:9pt;color:#3b4150;margin:0 0 1mm}
.pz{float:right;font-weight:600;font-size:10pt;color:#3b4150}
.summe{position:absolute;right:0;bottom:0;font-size:12pt;font-weight:600;border:1pt solid #14171c;padding:1mm 3mm}
.antw{border-bottom:.5pt solid #b8bec7;min-height:7mm}
.antw.loesungstext{border-bottom:none;min-height:0;margin:1mm 0 2mm}
.pkt{color:#66798E;font-weight:400;font-size:8.5pt}
.mc{width:100%;border-collapse:collapse;font-size:10pt;margin:1mm 0 3mm}
.mc td{border:.6pt solid #14171c;padding:1mm 2mm;vertical-align:top}
.mc td.q{font-weight:600;background:#EEF1F5}
.mc td.x{width:9mm;text-align:center;color:#E6007E;font-weight:700}
.pse{border-collapse:collapse;font-size:8.5pt;float:right;margin:0 0 2mm 5mm}
.pse td{border:.5pt solid #9AA3B0;padding:.4mm 1.6mm}.pse td.z{text-align:right}
.kette{display:flex;align-items:center;gap:2mm;margin:3mm 0 4mm;font-size:12pt}
.kette .k{border:.8pt solid #14171c;width:22mm;height:15mm;display:flex;align-items:center;justify-content:center}
.kette .p{display:flex;flex-direction:column;align-items:center;font-size:10pt;line-height:1}
.kette .p small{font-size:9pt}
.nsk{border-collapse:collapse;font-size:10pt;margin:2mm 0}.nsk td,.nsk th{border:.6pt solid #14171c;padding:1mm 3mm;text-align:center}
</style>"""


def pkt(n):
    return f'<span class="pz">{str(n).replace(".", ",")} P</span>'


def aufg(nr, stufe, text, punkte):
    return f'<h2 class="aufgabe">{pkt(punkte)}<span class="nr">{nr}</span>{kreis(stufe)}{text}</h2>'


def antwort(text, l, zeilen=2, bew=""):
    if l:
        return f'<p class="antw loesungstext">{text}' + (f' <span class="pkt">({bew})</span>' if bew else "") + "</p>"
    return '<div class="antw"></div>' * zeilen


def zelle(w, l, vorgabe=False):
    if vorgabe:
        return f'<td class="v">{w}</td>'
    return f'<td class="l">{w}</td>' if l else "<td></td>"


def seite(inhalt, summe):
    return inhalt + f'<div class="summe">&nbsp;&nbsp;&nbsp;&nbsp;/ {summe} P</div>'


def kopfbox(l):
    t = "Lösung und Erwartungshorizont" if l else ""
    return (f'<div class="kabox"><div class="z1"><span>Physik · Klassenarbeit Nr. 1 · Kernphysik</span><span style="color:{MAG}">{t}</span></div>'
            '<div class="z2"><div class="f">Name</div><div class="f">Klasse</div><div class="f">Datum</div>'
            '<div class="f">Punkte ____ von 40</div><div class="f">Note / Unterschrift</div></div></div>'
            f'<p class="hinweise">Zeit: 45 Minuten · Hilfsmittel: Taschenrechner · Den Auszug aus dem Periodensystem findest du auf Seite 2. '
            f'Schwierigkeit: {kreis(0)}leicht &nbsp; {kreis(1)}mittel &nbsp; {kreis(2)}schwer</p>')


# ------------------------------------------------------------------ Seite 1
def s1(l):
    zeilen = [(nk("Na", 23, 11), "11", "12", "11"), (nk("Cl", 37, 17), "17", "20", "17"), (nk("U", 238, 92), "92", "146", "92")]
    t = ('<table class="mess" style="width:100%"><tr><th>Nuklid</th><th>Protonen</th><th>Neutronen</th><th>Elektronen</th></tr>'
         + "".join(f'<tr><td class="v" style="font-size:12pt">{a}</td>{zelle(b, l)}{zelle(c, l)}{zelle(d, l)}</tr>' for a, b, c, d in zeilen)
         + f'<tr>{zelle(nk("Fe", 56, 26), l) if l else "<td></td>"}{zelle("26", 0, True)}{zelle("30", 0, True)}{zelle("26", 0, True)}</tr></table>')
    return seite(kopfbox(l)
        + aufg(1, 0, "Ergänze die Tabelle. In der letzten Zeile fehlt das Nuklid." + (' <span class="pkt">(je Zeile 1 P)</span>' if l else ""), 4) + t
        + aufg(2, 1, "Kohlenstoff-12 und Kohlenstoff-14 sind Isotope.", 3)
        + '<p class="frage">a) Erkläre, was Isotope sind.</p>' + antwort("Atome desselben Elements mit gleich vielen Protonen, aber unterschiedlich vielen Neutronen.", l, 2, "1 P")
        + '<p class="frage">b) Warum verhalten sich beide chemisch gleich?</p>' + antwort("Gleiche Protonenzahl, also gleich viele Elektronen in der Hülle. Die Chemie hängt nur von der Hülle ab.", l, 2, "1 P")
        + '<p class="frage">c) Welches der beiden Isotope ist radioaktiv?</p>' + antwort("Kohlenstoff-14", l, 1, "1 P")
        + aufg(3, 0, "Ein Zählrohr misst ohne Präparat fünfmal je eine Minute lang: 18, 25, 21, 22 und 19 Impulse.", 3)
        + '<p class="frage">a) Wie nennt man diese Strahlung?</p>' + antwort("Nullrate (Nulleffekt, Umgebungsstrahlung)", l, 1, "1 P")
        + '<p class="frage">b) Berechne den Mittelwert.</p>' + antwort("(18 + 25 + 21 + 22 + 19) : 5 = 105 : 5 = 21 Impulse pro Minute", l, 1, "1 P")
        + '<p class="frage">c) Nenne zwei Ursachen dieser Strahlung.</p>'
        + antwort("zwei von: Radon in der Luft, Gestein und Baustoffe (terrestrisch), Weltall (kosmisch), Kalium-40 im eigenen Körper", l, 1, "je ½ P"), 10)


# ------------------------------------------------------------------ Seite 2
PSE = [(26, "Fe", "Eisen"), (38, "Sr", "Strontium"), (39, "Y", "Yttrium"), (40, "Zr", "Zirconium"), (80, "Hg", "Quecksilber"), (81, "Tl", "Thallium"),
       (82, "Pb", "Blei"), (83, "Bi", "Bismut"), (84, "Po", "Polonium"), (86, "Rn", "Radon"), (88, "Ra", "Radium"), (89, "Ac", "Actinium"),
       (90, "Th", "Thorium"), (91, "Pa", "Protactinium"), (92, "U", "Uran")]


def s2(l):
    reihen = [("Was wird ausgesendet?", "Heliumkern (2 p, 2 n)", "Elektron", "energiereiche Strahlung (Welle)"),
              ("Ladung", "positiv (zweifach)", "negativ", "keine"),
              ("Ablenkung im elektrischen Feld", "leicht zum Minuspol", "stark zum Pluspol", "keine"),
              ("Was hält sie auf?", "ein Blatt Papier", "einige mm Aluminium", "dickes Blei schwächt nur")]
    t = ('<table class="mess" style="width:100%"><tr><th></th><th>α-Strahlung</th><th>β⁻-Strahlung</th><th>γ-Strahlung</th></tr>'
         + "".join(f'<tr><td class="v" style="text-align:left">{a}</td>{zelle(b, l)}{zelle(c, l)}{zelle(d, l)}</tr>' for a, b, c, d in reihen) + "</table>")
    pse = '<table class="pse"><tr><td colspan="3" style="font-weight:600">Auszug aus dem Periodensystem</td></tr>' + "".join(
        f'<tr><td class="z">{z}</td><td><b>{s}</b></td><td>{n}</td></tr>' for z, s, n in PSE) + "</table>"
    L = lambda s: f'<span class="loesungstext">{s}</span>' if l else '<span class="luecke"></span>'
    return seite(aufg(4, 0, "Vergleiche die drei Strahlungsarten." + (' <span class="pkt">(je Feld ½ P)</span>' if l else ""), 6) + t
        + aufg(5, 1, "Eine Strahlung wird im elektrischen Feld zum Minuspol abgelenkt. Hinter einem Blatt Papier misst man nur noch die Nullrate. Um welche Strahlung handelt es sich? Begründe.", 3)
        + antwort("α-Strahlung (1 P). Sie ist positiv geladen, deshalb wird sie zum Minuspol gezogen (1 P). Nur α-Teilchen werden schon von Papier gestoppt (1 P).", l, 3)
        + aufg(6, 1, "Vervollständige die Zerfallsgleichungen." + (' <span class="pkt">(je Teilchen 1 P)</span>' if l else ""), 4) + pse
        + f'<p class="gl">a) α-Zerfall: &nbsp; {nk("Po", 210, 84)} → {L(nk("Pb", 206, 82))} + {L(nk("He", 4, 2))}</p>'
        + f'<p class="gl">b) β⁻-Zerfall: &nbsp; {nk("Sr", 90, 38)} → {L(nk("Y", 90, 39))} + {L(nk("e", 0, "−1"))}</p>', 13)


# ------------------------------------------------------------------ Seite 3
def diagramm(l):
    W, H, x0, y0, sx, sy = 320, 170, 40, 148, 6.8, 0.128
    o = [f'<svg viewBox="0 0 {W} {H}" style="width:100%;height:100%">']
    for t in range(0, 41, 4):
        o.append(f'<line x1="{x0 + t * sx}" y1="{y0}" x2="{x0 + t * sx}" y2="{y0 - 1000 * sy}" stroke="#C9D0DA" stroke-width=".4"/>')
    for n in range(0, 1001, 100):
        o.append(f'<line x1="{x0}" y1="{y0 - n * sy:.1f}" x2="{x0 + 40 * sx}" y2="{y0 - n * sy:.1f}" stroke="#C9D0DA" stroke-width=".4"/>')
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x0 + 40 * sx + 6}" y2="{y0}" stroke="#14171c" stroke-width="1"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - 1000 * sy - 6}" stroke="#14171c" stroke-width="1"/>')
    for t in range(0, 41, 8):
        o.append(f'<text x="{x0 + t * sx}" y="{y0 + 9}" font-size="6.5" text-anchor="middle">{t}</text>')
    for n in range(0, 1001, 200):
        o.append(f'<text x="{x0 - 3}" y="{y0 - n * sy + 2:.1f}" font-size="6.5" text-anchor="end">{n}</text>')
    o.append(f'<text x="{x0 + 40 * sx}" y="{y0 + 18}" font-size="7" text-anchor="end">Zeit in Tagen</text><text x="{x0 + 4}" y="12" font-size="7">Anzahl der Iod-131-Kerne</text>')
    pts = " ".join(f"{x0 + t * sx:.1f},{y0 - 1000 * 0.5 ** (t / 8) * sy:.1f}" for t in [i * 0.5 for i in range(81)])
    o.append(f'<polyline points="{pts}" fill="none" stroke="#0B8FB8" stroke-width="1.6"/>')
    if l:
        for k in (1, 2):
            X, Y = x0 + 8 * k * sx, y0 - 1000 / 2 ** k * sy
            o.append(f'<line x1="{x0}" y1="{Y:.1f}" x2="{X:.1f}" y2="{Y:.1f}" stroke="{MAG}" stroke-width="1" stroke-dasharray="3 2"/>'
                     f'<line x1="{X:.1f}" y1="{Y:.1f}" x2="{X:.1f}" y2="{y0}" stroke="{MAG}" stroke-width="1" stroke-dasharray="3 2"/>')
    return "".join(o) + "</svg>"


def s3(l):
    k = lambda inhalt: f'<div class="k">{"<span class=loesungstext>" + inhalt + "</span>" if l else ""}</div>'
    pf = lambda a: f'<div class="p"><small>{a}</small>→</div>'
    kette = (f'<div class="kette"><div class="k">{nk("U", 238, 92)}</div>{pf("α")}{k(nk("Th", 234, 90))}{pf("β⁻")}{k(nk("Pa", 234, 91))}'
             f'{pf("β⁻")}{k(nk("U", 234, 92))}{pf("α")}{k(nk("Th", 230, 90))}</div>')
    return seite(aufg(7, 2, "Uran-238 zerfällt nacheinander durch α, β⁻, β⁻ und α. Trage die entstehenden Nuklide in die Kästchen ein." + (' <span class="pkt">(je Kästchen 1 P)</span>' if l else ""), 4)
        + kette
        + aufg(8, 1, "Das Diagramm zeigt den Zerfall von Iod-131.", 4)
        + f'<div class="zeichenfeld" style="height:78mm;background-image:none">{diagramm(l)}</div>'
        + '<p class="frage">a) Lies die Halbwertszeit von Iod-131 ab.</p>' + antwort("8 Tage", l, 1, "1 P")
        + '<p class="frage">b) Wie viele Kerne sind nach 24 Tagen noch vorhanden?</p>' + antwort("24 Tage sind 3 Halbwertszeiten: 1000 → 500 → 250 → 125 Kerne", l, 1, "1 P")
        + '<p class="frage">c) Zeichne die ersten beiden Halbwertszeiten in das Diagramm ein.</p>' + antwort("siehe gestrichelte Linien bei 500 und 250 Kernen", l, 0, "1 P")
        + '<p class="frage">d) Erkläre, warum die Kurve die Zeitachse nie erreicht.</p>'
        + antwort("In jeder Halbwertszeit zerfällt nur die Hälfte der noch vorhandenen Kerne, es bleibt also immer ein Rest übrig.", l, 2, "1 P"), 8)


# ------------------------------------------------------------------ Seite 4
MC = [("Was gibt die Massenzahl A an?", ["die Zahl der Protonen", "die Zahl der Protonen und Neutronen", "die Zahl der Elektronen", "die Masse in Gramm"], 1),
      ("Was zeigte Rutherfords Streuversuch?", ["Atome sind volle Kugeln", "Elektronen sitzen im Kern", "Das Atom ist fast leer, der Kern winzig", "Gold ist radioaktiv"], 2),
      ("Was passiert beim β⁻-Zerfall im Kern?", ["Ein Proton wird zum Neutron", "Ein Neutron wird zum Proton", "Der Kern verliert zwei Protonen", "Ein Elektron aus der Hülle fliegt weg"], 1),
      ("In welcher Einheit gibt man die Aktivität an?", ["Sievert", "Becquerel", "Impulse pro Minute", "Watt"], 1),
      ("Warum zeigt das Zählrohr weniger an, als Kerne zerfallen?", ["Es fängt nur die Strahlung auf, die in seine Richtung fliegt", "Die Strahlung wird in der Luft langsamer",
                                                                     "Es zählt nur α-Strahlung", "Das Präparat ist verbraucht"], 0)]


def s4(l):
    mc = '<table class="mc">' + "".join(
        f'<tr><td class="q" colspan="2">{i + 1}. {q}</td></tr>' + "".join(
            f'<tr><td>{o}</td><td class="x">{"✗" if (l and j == a) else ""}</td></tr>' for j, o in enumerate(opts)) for i, (q, opts, a) in enumerate(MC)) + "</table>"
    return seite(aufg(9, 1, "Rechne mit der Halbwertszeit.", 4)
        + f'<p class="frage">{kreis(1)}a) Radon-222 hat eine Halbwertszeit von 3,8 Tagen. Von 4000 Radonatomen, wie viele sind nach 11,4 Tagen noch da?</p>'
        + antwort("11,4 Tage : 3,8 Tage = 3 Halbwertszeiten (1 P). 4000 → 2000 → 1000 → 500 Atome (1 P).", l, 2)
        + f'<p class="frage">{kreis(2)}b) In einem Holzfund ist nur noch ein Sechzehntel des C-14 vorhanden (Halbwertszeit 5730 Jahre). Wie alt ist das Holz?</p>'
        + antwort("1/16 = (1/2)⁴, also 4 Halbwertszeiten (1 P). 4 · 5730 Jahre = 22 920 Jahre (1 P).", l, 2)
        + aufg(10, 0, "Kreuze an. Es ist jeweils genau eine Antwort richtig." + (' <span class="pkt">(je 1 P)</span>' if l else ""), 5) + mc, 9)


def notenschluessel():
    stufen = [("1", "36,5"), ("2", "28,5"), ("3", "20,5"), ("4", "12,5"), ("5", "4,5"), ("6", "0")]
    t = ('<table class="nsk"><tr><th>Note</th>' + "".join(f"<td>{n}</td>" for n, _ in stufen) + "</tr><tr><th>ab Punkten</th>"
         + "".join(f"<td>{p}</td>" for _, p in stufen) + "</tr></table>")
    return ('<div class="kopf"><div><span class="chip">KA 1</span><h1>Punkteverteilung und Notenschlüssel</h1></div><div class="loesung-marker">nur für dich</div></div>'
            '<table class="mess" style="width:100%"><tr><th>Seite</th><th>Aufgaben</th><th>Punkte</th><th>Stoff</th></tr>'
            '<tr><td>1</td><td>1 bis 3</td><td>10</td><td style="text-align:left">Nuklide, Isotope, Nullrate (W02, W03)</td></tr>'
            '<tr><td>2</td><td>4 bis 6</td><td>13</td><td style="text-align:left">α, β, γ, elektrisches Feld, Zerfallsgleichungen (W04, W05)</td></tr>'
            '<tr><td>3</td><td>7 und 8</td><td>8</td><td style="text-align:left">Zerfallsreihe, Halbwertszeit am Diagramm (W05, W07)</td></tr>'
            '<tr><td>4</td><td>9 und 10</td><td>9</td><td style="text-align:left">Rechnen mit der Halbwertszeit, Multiple Choice (W01 bis W09)</td></tr>'
            '<tr><td colspan="2"><b>Summe</b></td><td><b>40</b></td><td></td></tr></table>'
            '<p class="frage">Anforderung: 18 P leicht (○), 16 P mittel (◐), 6 P schwer (●, Aufgaben 7 und 9 b).</p>'
            '<h2 class="aufgabe">Notenschlüssel (Vorschlag)</h2>'
            '<p class="frage">Linear wie in deinem Notenschlüsselrechner: Note = 1 + 5 · (40 − P) : 40, kaufmännisch auf ganze Noten gerundet, halbe Punkte möglich.</p>'
            + t +
            '<h2 class="aufgabe">Hinweise zur Korrektur</h2><ul class="liste">'
            '<li>Aufgabe 1: pro Zeile 1 P nur, wenn alle drei Zahlen stimmen. Bei einem Fehler ½ P.</li>'
            '<li>Aufgabe 4: Bei der Abschirmung von γ auch „Blei, Beton“ werten. „Blei stoppt γ“ ohne „schwächt“ nur ½ P.</li>'
            '<li>Aufgabe 6 und 7: Folgefehler nicht doppelt abziehen. Symbol und beide Zahlen müssen stimmen, sonst ½ P.</li>'
            '<li>Aufgabe 8 b und 9: Ergebnis ohne Rechenweg höchstens die Hälfte der Punkte.</li></ul>')


def dokument(titel, seiten):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title><link rel="stylesheet" href="{CSS}">{EXTRA}{KA_CSS}</head><body>'
            + "".join(f'<div class="seite">{s}</div>' for s in seiten) + "</body></html>")


# ------------------------------------------------------------------ Was muss ich wissen?
THEMEN = [("Atombau", ["Kern mit Protonen und Neutronen, Hülle mit Elektronen", "Rutherfords Streuversuch: Das Atom ist fast leer", "Nuklidschreibweise, A = Z + N"], "W01, W02"),
          ("Isotope", ["Was Isotope sind, Beispiele H, C, U", "Protonen, Neutronen und Elektronen aus dem Nuklid ablesen"], "W02"),
          ("Zählrohr und Nullrate", ["Aufbau und Funktion des Zählrohrs", "Nullrate: Ursachen, Mittelwert berechnen"], "W03"),
          ("α-, β- und γ-Strahlung", ["Was ausgesendet wird, Ladung", "Ablenkung im elektrischen Feld, Reichweite, Abschirmung"], "W04, W05"),
          ("Zerfallsgleichungen", ["α- und β⁻-Zerfall aufstellen (oben und unten gleiche Summe)", "Zerfallsreihen mit dem Periodensystem"], "W05"),
          ("Halbwertszeit", ["Begriff erklären, Würfelmodell", "aus einem Diagramm ablesen und einzeichnen", "rechnen: Halbieren in Schritten, Anteil ↔ Zahl der Halbwertszeiten"], "W06, W07, W09"),
          ("Aktivität", ["Becquerel: Zerfälle pro Sekunde", "Warum das Zählrohr weniger anzeigt"], "W08")]


def wissen():
    zeilen = "".join(f'<tr><td class="v" style="text-align:left;width:40mm">{i + 1}. {t}</td><td style="text-align:left">' + "<br>".join("• " + p for p in ps)
                     + f'</td><td style="width:26mm">{w}</td></tr>' for i, (t, ps, w) in enumerate(THEMEN))
    return ('<div class="kopf"><div><span class="chip">KA 1</span><h1>Was muss ich für die 1. Physikarbeit wissen?</h1></div></div>'
            '<p class="frage">Klasse 10 · Kernphysik · 45 Minuten · Taschenrechner erlaubt, ein Auszug aus dem Periodensystem ist dabei.</p>'
            f'<table class="mess" style="width:100%"><tr><th>Thema</th><th>Das solltest du können</th><th>Stunde</th></tr>{zeilen}</table>'
            '<h2 class="aufgabe">So kannst du üben</h2><ul class="liste">'
            '<li>Übungsblatt aus W09 und die Blätter W02 bis W08 noch einmal ohne Lösung rechnen</li>'
            '<li>Kurz-Checks in den Laboren: Atomlabor, Strahlungslabor, Zerfallslabor (Link in IServ)</li>'
            '<li>Zerfallsgleichungen im Strahlungslabor üben, bis alle sechs sitzen</li></ul>')


if __name__ == "__main__":
    dateien = [(f"{NAME}.html", "Klassenarbeit Nr. 1 – Kernphysik", [s1(False), s2(False), s3(False), s4(False)]),
               (f"{NAME} – Lösung.html", "Klassenarbeit Nr. 1 – Lösung", [s1(True), s2(True), s3(True), s4(True), notenschluessel()]),
               (f"{NAME} – Was muss ich wissen.html", "Was muss ich wissen?", [wissen()])]
    for datei, titel, seiten in dateien:
        (HIER / datei).write_text(dokument(titel, seiten), encoding="utf-8")
        print("geschrieben:", datei)
        if "pdf" in sys.argv[1:]:
            pdf = HIER / datei.replace(".html", ".pdf")
            subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                            "--virtual-time-budget=4000", f"file://{HIER / datei}"], check=True, capture_output=True)
            print("gedruckt:", pdf.name)
