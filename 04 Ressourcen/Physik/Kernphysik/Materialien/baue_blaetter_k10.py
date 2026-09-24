#!/usr/bin/env python3
"""Blätter Kernphysik Klasse 10, W02 bis W05 (W01 = Wiederholung Atombau, schon vorhanden).
Aufbau wie in Klasse 7: Aufgabe/Versuch, Felder, Lückentext, Lösungsseite in Magenta.
W03 übernimmt Oskars Lückentext zum Zählrohr wörtlich."""
import re, subprocess
from pathlib import Path

HIER = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAG = "#E6007E"
CSS = "../../Optik/Materialien/ab-vorlage.css"
EXTRA = ('<style>.nk{white-space:nowrap}.nk .az{display:inline-flex;flex-direction:column;font-size:.62em;line-height:1.05;text-align:right;'
         'vertical-align:-.42em;margin-right:1px}.nk .s{font-family:Georgia,serif;font-size:1.15em}'
         '.mess{border-collapse:collapse;margin:1mm 0 3mm;font-size:10pt}.mess th,.mess td{border:0.6pt solid #14171c;padding:1mm 2mm;height:7mm;text-align:center}'
         '.mess th{background:#EEF1F5;font-weight:600}.mess td.l{color:' + MAG + ';font-weight:600}.mess td.v{font-weight:600}'
         '.gl{font-size:13pt;margin:2mm 0 4mm 4mm;line-height:2.2}.gl .luecke{min-width:14mm}</style>')
NAME = '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>'


def nk(sym, A, Z):
    return f'<span class="nk"><span class="az"><span>{A}</span><span>{Z}</span></span><span class="s">{sym}</span></span>'


def kopf(chip, titel, l):
    lm = '<div class="loesung-marker">Lösung</div>' if l else ""
    return f'<div class="kopf"><div><span class="chip">{chip}</span><h1>{titel}</h1></div>{lm}</div>' + ("" if l else NAME)


def luecken(text, l):
    return re.sub(r"\[\[(.+?)\]\]", (lambda m: f'<span class="luecke loesungstext">{m.group(1)}</span>') if l else (lambda m: '<span class="luecke"></span>'), text)


def tabelle(kopfzeile, zeilen, l, vorgabe=0):
    """zeilen: Listen mit Werten; die ersten `vorgabe` Spalten stehen immer da, der Rest nur in der Lösung."""
    k = "".join(f"<th>{h}</th>" for h in kopfzeile)
    rows = "".join("<tr>" + "".join(
        (f'<td class="v">{w}</td>' if j < vorgabe else (f'<td class="l">{w}</td>' if l else "<td></td>")) for j, w in enumerate(z)) + "</tr>" for z in zeilen)
    return f'<table class="mess"><tr>{k}</tr>{rows}</table>'


def dokument(titel, seiten):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title><link rel="stylesheet" href="{CSS}">{EXTRA}</head><body>'
            + "".join(f'<div class="seite">{s}</div>' for s in seiten) + "</body></html>")


# ---------------------------------------------------------------- W02 Nuklide und Isotope
NUKLIDE = [("H", 1, 1), ("He", 4, 2), ("C", 12, 6), ("C", 14, 6), ("O", 16, 8), ("U", 235, 92), ("U", 238, 92)]


def w02(l):
    zeilen = [[nk(s, A, Z), Z, A - Z, Z] for s, A, Z in NUKLIDE]
    a3 = [("Kohlenstoff mit 7 Neutronen", nk("C", 13, 6)), ("Sauerstoff mit 10 Neutronen", nk("O", 18, 8)), ("Kalium (Z = 19) mit 21 Neutronen", nk("K", 40, 19))]
    zeilen3 = "".join(f'<tr><td style="text-align:left">{t}</td>' + (f'<td class="l">{n}</td>' if l else "<td></td>") + "</tr>" for t, n in a3)
    lt = luecken("Isotope haben die gleiche Anzahl an [[Protonen]], aber eine unterschiedliche Anzahl an [[Neutronen]]. "
                 "In der Tabelle sind [[Kohlenstoff-12 und Kohlenstoff-14]] sowie [[Uran-235 und Uran-238]] Isotope.", l)
    return (kopf("W02", "F1 — Nuklide und Isotope", l)
            + '<h2 class="aufgabe"><span class="nr">1</span>Ergänze die Tabelle.</h2>'
            + tabelle(["Nuklid", "Protonen", "Neutronen", "Elektronen"], zeilen, l, vorgabe=1)
            + '<h2 class="aufgabe"><span class="nr">2</span>Ergänze.</h2>' + f'<p class="frage lt">{lt}</p>'
            + '<h2 class="aufgabe"><span class="nr">3</span>Schreibe in Nuklidschreibweise. Nimm das Periodensystem zu Hilfe.</h2>'
            + f'<table class="mess" style="width:120mm"><tr><th style="text-align:left">Atom</th><th>Nuklid</th></tr>{zeilen3}</table>')


# ---------------------------------------------------------------- W03 Zählrohr und Nullrate
def zaehlrohr_svg(l):
    lab = ["dünne Folie", "Gas", "Metalldraht", "Metallrohr"]
    o = ['<svg viewBox="0 0 300 110" style="width:100%;height:100%">',
         '<rect x="70" y="30" width="190" height="50" rx="4" fill="#EEF1F5" stroke="#14171c" stroke-width="1.2"/>',
         '<rect x="66" y="30" width="5" height="50" fill="#F5E6C8" stroke="#14171c" stroke-width="0.8"/>',
         '<line x1="80" y1="55" x2="286" y2="55" stroke="#14171c" stroke-width="1.4"/>',
         '<g stroke="#7A4BAF" stroke-width="1.2"><line x1="16" y1="42" x2="62" y2="52"/><line x1="16" y1="62" x2="62" y2="58"/></g>',
         '<text x="4" y="30" font-size="7" fill="#66798E">Strahlung</text>']
    pos = [(68, 30, 60, 8), (150, 38, 150, 8), (240, 55, 250, 8), (180, 80, 180, 104)]
    for i, (x, y, tx, ty) in enumerate(pos):
        o.append(f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty + (-3 if ty < 50 else -8)}" stroke="#66798E" stroke-width="0.6"/>')
        o.append(f'<text x="{tx}" y="{ty}" font-size="8" text-anchor="middle" fill="{MAG if l else "#14171c"}">{lab[i] if l else str(i + 1) + " ________"}</text>')
    o.append("</svg>")
    return "".join(o)


def w03(l):
    lt1 = luecken("Gelangt radioaktive Strahlung in das [[Zählrohr]], erzeugt sie dort kleine Stromstöße, die [[Impulse]] genannt werden. "
                  "Das Zählwerk [[zählt]] und verstärkt diese, dass bei jedem Impuls ein [[Knacken]] im Lautsprecher zu hören ist. "
                  "Die Summe aller Impulse in 1 Minute heißt [[Impulsrate]]. Je [[höher]] diese ist, desto [[stärker]] ist die radioaktive Strahlung, "
                  "die von dem radioaktiven Material ausgeht.", l)
    werte = [["1 min", 22, 22], ["1 min", 27, 27], ["1 min", 19, 19], ["1 min", 25, 25], ["1 min", 24, 24]]
    lt2 = luecken("Auch ohne Präparat misst das Zählrohr Impulse. Diese Umgebungsstrahlung heißt [[Nullrate]] oder Nulleffekt. "
                  "Ursachen sind die Eigenstrahlung des [[menschlichen Körpers]], die [[terrestrische]] Strahlung aus Boden und Baustoffen "
                  "und die [[kosmische]] Strahlung aus dem Weltall.", l)
    return (kopf("W03", "F2 — Das Zählrohr und die Nullrate", l)
            + '<h2 class="aufgabe"><span class="nr">1</span>Beschrifte das Zählrohr.</h2>'
            + f'<div style="height:38mm;margin:1mm 0 2mm">{zaehlrohr_svg(l)}</div>'
            + '<h2 class="aufgabe"><span class="nr">2</span>Fülle die Lücken aus.</h2>' + f'<p class="frage lt">{lt1}</p>'
            + '<h2 class="aufgabe"><span class="nr">3</span>Versuch: Wir messen die Nullrate</h2>'
            + '<p class="frage">Das Zählrohr misst fünfmal je eine Minute lang, ohne Präparat. Trage die Impulse ein und berechne den Mittelwert.'
            + (' <span class="loesungstext">Beispielwerte</span>' if l else "") + '</p>'
            + tabelle(["Messzeit", "Impulse", "Impulse pro Minute"], werte, l, vorgabe=1)
            + f'<p class="frage">Mittelwert: {"<span class=\"loesungstext\">23,4 Impulse pro Minute</span>" if l else "<span class=\"luecke\"></span> Impulse pro Minute"}</p>'
            + '<h2 class="aufgabe"><span class="nr">4</span>Fülle die Lücken aus.</h2>' + f'<p class="frage lt">{lt2}</p>')


# ---------------------------------------------------------------- W04 Drei Arten radioaktiver Strahlung
def w04(l):
    zeilen = [["α-Strahlung", "Heliumkern (2 Protonen, 2 Neutronen)", "positiv", "−4", "−2"],
              ["β⁻-Strahlung", "Elektron", "negativ", "bleibt", "+1"],
              ["γ-Strahlung", "Energie (Welle)", "keine", "bleibt", "bleibt"]]
    zuo = [(nk("Ra", 226, 88) + " → " + nk("Rn", 222, 86) + " + ?", "α"), (nk("Sr", 90, 38) + " → " + nk("Y", 90, 39) + " + ?", "β⁻"),
           (nk("Ba", "137m", 56) + " → " + nk("Ba", 137, 56) + " + ?", "γ")]
    z2 = "".join(f'<tr><td style="text-align:left;font-size:12pt">{g}</td>' + (f'<td class="l">{a}</td>' if l else "<td></td>") + "</tr>" for g, a in zuo)
    lt = luecken("Beim α-Zerfall verliert der Kern [[2 Protonen]] und [[2 Neutronen]]. Beim β⁻-Zerfall wandelt sich im Kern ein "
                 "[[Neutron]] in ein [[Proton]] um, dabei entsteht ein Elektron. Die γ-Strahlung ändert nur die [[Energie]] des Kerns.", l)
    return (kopf("W04", "F2 — Drei Arten radioaktiver Strahlung", l)
            + '<h2 class="aufgabe"><span class="nr">1</span>Ergänze die Tabelle.</h2>'
            + tabelle(["Art", "Was wird ausgesendet?", "Ladung", "Massenzahl A", "Kernladungszahl Z"], zeilen, l, vorgabe=1)
            + '<h2 class="aufgabe"><span class="nr">2</span>Fülle die Lücken aus.</h2>' + f'<p class="frage lt">{lt}</p>'
            + '<h2 class="aufgabe"><span class="nr">3</span>Welche Strahlung wird hier ausgesendet?</h2>'
            + f'<table class="mess" style="width:130mm"><tr><th style="text-align:left">Zerfall</th><th>Strahlung</th></tr>{z2}</table>')


# ---------------------------------------------------------------- W05 Durchdringung und Zerfallsgleichungen
def w05(l):
    werte = [["α-Strahler", "hoch", "fast Nullrate", "fast Nullrate", "fast Nullrate"],
             ["β-Strahler", "hoch", "fast so hoch", "fast Nullrate", "fast Nullrate"],
             ["γ-Strahler", "hoch", "fast so hoch", "fast so hoch", "kleiner, aber über der Nullrate"]]
    lt = luecken("α-Strahlung wird schon von [[Papier]] gestoppt, β-Strahlung von einigen Millimetern [[Aluminium]]. "
                 "γ-Strahlung wird von dickem [[Blei]] nur geschwächt.", l)
    gl = [(nk("Po", 210, 84), "α", nk("Pb", 206, 82), nk("He", 4, 2)), (nk("K", 40, 19), "β⁻", nk("Ca", 40, 20), nk("e", 0, "−1")),
          (nk("Ra", 226, 88), "α", nk("Rn", 222, 86), nk("He", 4, 2))]
    zeilen = ""
    for a, art, b, c in gl:
        rechts = f'{b} + {c}' if l else '<span class="luecke"></span> + <span class="luecke"></span>'
        zeilen += f'<p class="gl">{art}-Zerfall: &nbsp; {a} → <span class="{"loesungstext" if l else ""}">{rechts}</span></p>'
    return (kopf("W05", "F2 — Wie weit kommt die Strahlung?", l)
            + '<h2 class="aufgabe"><span class="nr">1</span>Versuch: Absorption (Lehrerversuch)</h2>'
            + '<p class="frage">Zwischen Präparat und Zählrohr werden nacheinander ein Blatt Papier, 5 mm Aluminium und einige Zentimeter Blei gestellt. Notiere, wie sich die Zählrate ändert.'
            + (' <span class="loesungstext">typische Beobachtung</span>' if l else "") + '</p>'
            + tabelle(["Präparat", "ohne Absorber", "Papier", "Aluminium", "Blei"], werte, l, vorgabe=1)
            + '<h2 class="aufgabe"><span class="nr">2</span>Fülle die Lücken aus.</h2>' + f'<p class="frage lt">{lt}</p>'
            + '<h2 class="aufgabe"><span class="nr">3</span>Vervollständige die Zerfallsgleichungen.</h2>' + zeilen)


def drucke(html, pdf):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / pdf}",
                    "--virtual-time-budget=4000", f"file://{HIER / html}"], check=True, capture_output=True)
    print("gedruckt:", pdf)


if __name__ == "__main__":
    for html, pdf, titel, fn in (("nuklide.html", "Nuklide und Isotope W02.pdf", "Nuklide und Isotope – W02", w02),
                                 ("zaehlrohr.html", "Zaehlrohr und Nullrate W03.pdf", "Zählrohr und Nullrate – W03", w03),
                                 ("strahlungsarten.html", "Drei Strahlungsarten W04.pdf", "Drei Arten radioaktiver Strahlung – W04", w04),
                                 ("durchdringung.html", "Durchdringung und Zerfallsgleichungen W05.pdf", "Durchdringung und Zerfallsgleichungen – W05", w05)):
        (HIER / html).write_text(dokument(titel, [fn(False), fn(True)]), encoding="utf-8")
        drucke(html, pdf)
