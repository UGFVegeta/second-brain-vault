#!/usr/bin/env python3
"""Blätter Kernphysik Klasse 10, W01 bis W05 (dazu Wiederholung Atombau, schon vorhanden).
Aufbau wie in Klasse 7: Aufgabe/Versuch, Felder, Lückentext, Lösungsseite in Magenta.
Jede Aufgabe trägt einen Schwierigkeitskreis (○ leicht, ◐ mittel, ● schwer), Legende oben.
W03 übernimmt Oskars Lückentext zum Zählrohr wörtlich."""
import re, subprocess
from pathlib import Path

HIER = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAG = "#E6007E"
CSS = "../../Optik/Materialien/ab-vorlage.css"
EXTRA = ('<style>.nk{white-space:nowrap}.nk .az{display:inline-flex;flex-direction:column;font-size:.62em;line-height:1.05;text-align:right;'
         'vertical-align:.4em;margin-right:1px}.nk .s{font-family:Georgia,serif;font-size:1.15em}'
         '.mess{border-collapse:collapse;margin:1mm 0 3mm;font-size:10pt}.mess th,.mess td{border:0.6pt solid #14171c;padding:0.8mm 2mm;height:6.2mm;text-align:center}'
         '.mess th{background:#EEF1F5;font-weight:600}.mess td.l{color:' + MAG + ';font-weight:600}.mess td.v{font-weight:600}'
         '.gl{font-size:13pt;margin:1mm 0 2mm 4mm;line-height:1.9}.gl .luecke{min-width:14mm}'
         '.pf{display:inline-flex;flex-direction:column;align-items:center;line-height:1;margin:0 1.5mm;vertical-align:.55em}.pf small{font-size:.6em}'
         '.lvl{vertical-align:-3px;margin-right:2mm}.legende{font-size:9pt;color:#3b4150;margin:0 0 1mm;text-align:right}.legende .lvl{margin:0 1mm 0 3mm}'
         '.antw{border-bottom:0.5pt solid #b8bec7;min-height:6mm;margin:0 0 1mm}.antw.loesungstext{border-bottom:none;min-height:0;margin-bottom:2mm}</style>')
NAME = '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>'


def nk(sym, A, Z):
    return f'<span class="nk"><span class="az"><span>{A}</span><span>{Z}</span></span><span class="s">{sym}</span></span>'


def kreis(stufe):
    """stufe 0 leer, 1 halb, 2 voll (wie im Mathe-Arbeitsblatt)"""
    b = ('<svg class="lvl" viewBox="0 0 20 20" width="15" height="15" xmlns="http://www.w3.org/2000/svg">'
         '<circle cx="10" cy="10" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>')
    if stufe == 1:
        b += '<path d="M10 2 A8 8 0 0 0 10 18 Z" fill="#333"/>'
    elif stufe == 2:
        b += '<circle cx="10" cy="10" r="8" fill="#333"/>'
    return b + "</svg>"


LEGENDE = f'<div class="legende">Schwierigkeit:{kreis(0)}leicht{kreis(1)}mittel{kreis(2)}schwer</div>'


def aufg(nr, stufe, text):
    k = "" if stufe is None else kreis(stufe)
    return f'<h2 class="aufgabe"><span class="nr">{nr}</span>{k}{text}</h2>'


def antwort(text, l, zeilen=2):
    return f'<p class="antw loesungstext">{text}</p>' if l else '<div class="antw"></div>' * zeilen


def kopf(chip, titel, l):
    lm = '<div class="loesung-marker">Lösung</div>' if l else ""
    return f'<div class="kopf"><div><span class="chip">{chip}</span><h1>{titel}</h1></div>{lm}</div>' + ("" if l else NAME) + LEGENDE


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


# ---------------------------------------------------------------- W01 Atome enthalten elektrische Ladungen
SK_W01 = ('<svg class="versuchsskizze" viewBox="0 0 160 120">'
          '<rect x="22" y="8" width="44" height="10" rx="3" fill="#9FB2CF"/><rect x="56" y="18" width="9" height="12" fill="#9FB2CF"/>'
          '<path d="M60.5 30 C61 60 66 88 80 112" fill="none" stroke="#0B8FB8" stroke-width="2.4"/>'
          '<path d="M60.5 30 L60.5 112" fill="none" stroke="#0B8FB8" stroke-width="1" stroke-dasharray="2 3" opacity=".6"/>'
          '<ellipse cx="112" cy="64" rx="19" ry="23" fill="#E8604A"/><path d="M112 87 l-3 5 h6z" fill="#E8604A"/>'
          '<path d="M112 92 q-4 8 2 14 q5 6 0 12" fill="none" stroke="#66798E" stroke-width="0.8"/>'
          '<g fill="#fff" font-size="10" font-weight="700" text-anchor="middle"><text x="102" y="60">−</text><text x="116" y="54">−</text>'
          '<text x="108" y="74">−</text><text x="121" y="68">−</text></g>'
          '<line x1="10" y1="114" x2="150" y2="114" stroke="#66798E" stroke-width="1.2"/>'
          '<text x="8" y="44" font-size="7" fill="#66798E">Wasserstrahl</text><text x="96" y="30" font-size="7" fill="#66798E">Luftballon</text></svg>')


def w01(l):
    beob = ('<p class="beobachtungstext loesungstext">Versuch 1: Die Papierschnipsel springen zum Ballon hoch und bleiben zum Teil an ihm hängen.<br>'
            'Versuch 2: Der Wasserstrahl wird zum Ballon hin gebogen, ohne ihn zu berühren.</p>') if l else ""
    lt = luecken("Beim Reiben gehen [[Elektronen]] von der Wolle auf den Ballon über. Der Ballon ist danach [[negativ]] geladen, die Wolle [[positiv]]. "
                 "Elektronen lassen sich also aus Atomen [[herauslösen]]. Atome enthalten demnach elektrische Ladungen: [[negative]] Elektronen in der Hülle "
                 "und [[positive]] Ladung im Kern. Normalerweise gibt es von beiden gleich viel, das Atom ist nach außen [[neutral]].", l)
    return (kopf("W01", "F1 — Versuch: Atome enthalten elektrische Ladungen", l)
            + '<p class="frage">Was passiert, wenn man einen Luftballon an einem Wolltuch reibt?</p>'
            + '<div class="versuchskopf"><div>' + aufg(1, None, "Versuchsbeschreibung") + '<ol class="liste">'
            '<li><b>Versuch 1:</b> Reibe den aufgeblasenen Luftballon kräftig am Wolltuch. Halte ihn dann dicht über kleine Papierschnipsel.</li>'
            '<li><b>Versuch 2:</b> Öffne den Wasserhahn so weit, dass nur ein dünner Strahl fließt. Reibe den Ballon erneut und halte ihn seitlich nah an den Strahl, ohne ihn zu berühren.</li>'
            '</ol></div>' + SK_W01 + '</div>'
            + aufg(2, 0, "Beschreibe deine Beobachtung.") + f'<div class="zeichenfeld" style="height:24mm;">{beob}</div>'
            + aufg(3, 1, "Versuchserklärung: Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(4, 2, "Auch ein positiv geladener Glasstab zieht den Wasserstrahl an. Erkläre.")
            + antwort("Im Wasser verschieben sich die Ladungen: Die Seite zum Stab hin bekommt die entgegengesetzte Ladung und wird angezogen. "
                      "Das funktioniert mit positiver und mit negativer Ladung.", l, 3))


# ---------------------------------------------------------------- W02 Nuklide und Isotope
NUKLIDE = [("H", 1, 1), ("He", 4, 2), ("C", 12, 6), ("C", 14, 6), ("O", 16, 8), ("U", 235, 92), ("U", 238, 92)]


def w02(l):
    zeilen = [[nk(s, A, Z), Z, A - Z, Z] for s, A, Z in NUKLIDE]
    a3 = [("Kohlenstoff mit 7 Neutronen", "C-13", nk("C", 13, 6)), ("Natrium mit 12 Neutronen", "Na-23", nk("Na", 23, 11)),
          ("Helium mit 1 Neutron", "He-3", nk("He", 3, 2)), ("Eisen mit 30 Neutronen", "Fe-56", nk("Fe", 56, 26))]
    zeilen3 = "".join(f'<tr><td style="text-align:left">{t}</td>' + (f'<td class="l">{k}</td><td class="l">{n}</td>' if l else "<td></td><td></td>") + "</tr>"
                      for t, k, n in a3)
    lt = luecken("Die Massenzahl A ist die Summe aus der Zahl der [[Protonen]] Z und der Zahl der [[Neutronen]] N, also A = [[Z + N]]. "
                 "Isotope haben die gleiche Anzahl an [[Protonen]], aber eine unterschiedliche Anzahl an [[Neutronen]]. "
                 "In der Tabelle sind [[Kohlenstoff-12 und Kohlenstoff-14]] sowie [[Uran-235 und Uran-238]] Isotope.", l)
    return (kopf("W02", "F1 — Nuklide und Isotope", l)
            + aufg(1, 0, "Ergänze die Tabelle.")
            + tabelle(["Nuklid", "Protonen", "Neutronen", "Elektronen"], zeilen, l, vorgabe=1)
            + aufg(2, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(3, 1, "Schreibe in Kurzschreibweise und in Nuklidschreibweise. Nimm das Periodensystem zu Hilfe.")
            + f'<table class="mess" style="width:150mm"><tr><th style="text-align:left">Atom</th><th>Kurzschreibweise</th><th>Nuklid</th></tr>{zeilen3}</table>'
            + aufg(4, 1, "Ein Atomkern besteht aus 82 Protonen und 124 Neutronen. Um welches Nuklid handelt es sich?")
            + antwort(f"Z = 82, also Blei. A = 82 + 124 = 206. Das Nuklid ist Blei-206, {nk('Pb', 206, 82)}.", l, 1)
            + aufg(5, 2, "Uran-235 und Uran-238 kommen in der Natur gemischt vor. Warum lassen sie sich nicht chemisch trennen?")
            + antwort("Beide haben 92 Protonen und damit 92 Elektronen in der Hülle. Die chemischen Eigenschaften hängen nur von der Hülle ab, "
                      "deshalb verhalten sich beide gleich. Trennen kann man sie nur über ihre unterschiedliche Masse.", l, 2))


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
            + aufg(1, 0, "Beschrifte das Zählrohr.")
            + f'<div style="height:30mm;margin:0 0 1mm">{zaehlrohr_svg(l)}</div>'
            + aufg(2, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt1}</p>'
            + aufg(3, 0, "Versuch: Wir messen die Nullrate")
            + '<p class="frage">Das Zählrohr misst fünfmal je eine Minute lang, ohne Präparat. Trage die Impulse ein und berechne den Mittelwert.'
            + (' <span class="loesungstext">Beispielwerte</span>' if l else "") + '</p>'
            + tabelle(["Messzeit", "Impulse", "Impulse pro Minute"], werte, l, vorgabe=1)
            + f'<p class="frage">Mittelwert: {"<span class=\"loesungstext\">23,4 Impulse pro Minute</span>" if l else "<span class=\"luecke\"></span> Impulse pro Minute"}</p>'
            + aufg(4, 1, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt2}</p>'
            + aufg(5, 2, "Versuch: Ist ein Luftballon radioaktiv? (Lehrerversuch)")
            + '<p class="frage">Ein geriebener Luftballon hängt eine Weile im Raum. Dann wird die Luft abgelassen und die Hülle vor das Zählrohr gelegt. '
              'Die Zählrate liegt deutlich über der Nullrate und sinkt danach langsam wieder ab. Erkläre.</p>'
            + antwort("Die Luft enthält das radioaktive Gas Radon. Seine ebenfalls radioaktiven Folgeprodukte werden vom geladenen Ballon angezogen "
                      "und bleiben an ihm hängen. Sie zerfallen innerhalb von Minuten bis Stunden, deshalb sinkt die Zählrate wieder auf die Nullrate.", l, 2))


# ---------------------------------------------------------------- W04 Drei Arten radioaktiver Strahlung
def w04(l):
    zeilen = [["α-Strahlung", "Heliumkern (2 Protonen, 2 Neutronen)", "positiv", "schwach zum Minuspol", "wenige cm"],
              ["β⁻-Strahlung", "Elektron", "negativ", "stark zum Pluspol", "einige m"],
              ["γ-Strahlung", "Energie (Welle)", "keine", "keine Ablenkung", "sehr weit"]]
    kern_z = [["α-Strahlung", "−4", "−2"], ["β⁻-Strahlung", "bleibt", "+1"], ["γ-Strahlung", "bleibt", "bleibt"]]
    zuo = [(nk("Ra", 226, 88) + " → " + nk("Rn", 222, 86) + " + ?", "α"), (nk("Sr", 90, 38) + " → " + nk("Y", 90, 39) + " + ?", "β⁻"),
           (nk("Ba", "137m", 56) + " → " + nk("Ba", 137, 56) + " + ?", "γ")]
    z2 = "".join(f'<tr><td style="text-align:left;font-size:12pt">{g}</td>' + (f'<td class="l">{a}</td>' if l else "<td></td>") + "</tr>" for g, a in zuo)
    lt = luecken("Beim α-Zerfall verliert der Kern [[2 Protonen]] und [[2 Neutronen]]. Beim β⁻-Zerfall wandelt sich im Kern ein "
                 "[[Neutron]] in ein [[Proton]] um, dabei entsteht ein Elektron. Die γ-Strahlung ändert nur die [[Energie]] des Kerns.", l)
    return (kopf("W04", "F2 — Drei Arten radioaktiver Strahlung", l)
            + aufg(1, 0, "Ergänze die Tabelle.")
            + tabelle(["Art", "Was wird ausgesendet?", "Ladung", "Ablenkung im elektrischen Feld", "Reichweite in Luft"], zeilen, l, vorgabe=1)
            + aufg(2, 1, "Wie ändern sich Massenzahl und Kernladungszahl beim Zerfall?")
            + tabelle(["Art", "Massenzahl A", "Kernladungszahl Z"], kern_z, l, vorgabe=1)
            + aufg(3, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(4, 1, "Welche Strahlung wird hier ausgesendet?")
            + f'<table class="mess" style="width:130mm"><tr><th style="text-align:left">Zerfall</th><th>Strahlung</th></tr>{z2}</table>'
            + aufg(5, 2, "Eine Strahlung wird im elektrischen Feld nicht abgelenkt und kommt durch 5 mm Aluminium. Um welche Strahlung handelt es sich? Begründe.")
            + antwort("γ-Strahlung. Sie trägt keine Ladung und wird deshalb nicht abgelenkt. α- und β-Strahlung würden vom Aluminium gestoppt.", l, 2))


# ---------------------------------------------------------------- W05 Durchdringung und Zerfallsgleichungen
def w05(l):
    werte = [["α-Strahler", "hoch", "fast Nullrate", "fast Nullrate", "fast Nullrate"],
             ["β-Strahler", "hoch", "fast so hoch", "fast Nullrate", "fast Nullrate"],
             ["γ-Strahler", "hoch", "fast so hoch", "fast so hoch", "kleiner, aber über der Nullrate"]]
    lt = luecken("α-Strahlung wird schon von [[Papier]] gestoppt, β-Strahlung von einigen Millimetern [[Aluminium]]. "
                 "γ-Strahlung wird von dickem [[Blei]] nur geschwächt.", l)
    blei = [["0 cm", 800], ["1,3 cm", 400], ["2,6 cm", 200], ["3,9 cm", 100], ["5,2 cm", 50]]
    gl = [(nk("Po", 210, 84), "α", nk("Pb", 206, 82), nk("He", 4, 2)), (nk("K", 40, 19), "β⁻", nk("Ca", 40, 20), nk("e", 0, "−1")),
          (nk("Ra", 226, 88), "α", nk("Rn", 222, 86), nk("He", 4, 2))]
    zeilen = ""
    for a, art, b, c in gl:
        rechts = f'{b} + {c}' if l else '<span class="luecke"></span> + <span class="luecke"></span>'
        zeilen += f'<p class="gl">{art}-Zerfall: &nbsp; {a} → <span class="{"loesungstext" if l else ""}">{rechts}</span></p>'
    pf = lambda a: f'<span class="pf"><small>{a}</small>→</span>'
    reihe = (nk("U", 238, 92) + pf("α") + (f'<span class="loesungstext">{nk("Th", 234, 90)}</span>{pf("β⁻")}<span class="loesungstext">{nk("Pa", 234, 91)}</span>{pf("β⁻")}<span class="loesungstext">{nk("U", 234, 92)}</span>' if l else
             f'<span class="luecke"></span>{pf("β⁻")}<span class="luecke"></span>{pf("β⁻")}<span class="luecke"></span>'))
    return (kopf("W05", "F2 — Wie weit kommt die Strahlung?", l)
            + aufg(1, 0, "Versuch: Absorption (Lehrerversuch)")
            + '<p class="frage">Zwischen Präparat und Zählrohr werden nacheinander ein Blatt Papier, 5 mm Aluminium und einige Zentimeter Blei gestellt. Notiere, wie sich die Zählrate ändert.'
            + (' <span class="loesungstext">typische Beobachtung</span>' if l else "") + '</p>'
            + tabelle(["Präparat", "ohne Absorber", "Papier", "Aluminium", "Blei"], werte, l, vorgabe=1)
            + aufg(2, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(3, 1, "Eine Bleiplatte von 1,3 cm halbiert die γ-Strahlung. Ergänze die Zählrate (ohne Nullrate).")
            + '<div style="display:flex;gap:6mm;align-items:flex-start">'
            + tabelle(["Blei", "Impulse pro Minute"], blei[:1], True, vorgabe=2)[:-8] + tabelle(["", ""], blei[1:], l, vorgabe=1).split("</tr>", 1)[1]
            + '<div style="flex:1"><p class="frage">Wird die Zählrate hinter noch dickerem Blei irgendwann null?</p>'
            + antwort("Nein. Jede weitere Schicht halbiert nur, was noch ankommt. Die Strahlung wird immer schwächer, "
                      "aber nie ganz null. Irgendwann geht sie in der Nullrate unter.", l, 3) + '</div></div>'
            + aufg(4, 1, "Vervollständige die Zerfallsgleichungen.") + zeilen
            + aufg(5, 2, "Uran-238 zerfällt über mehrere Schritte. Ergänze die Zerfallsreihe.") + f'<p class="gl">{reihe}</p>')


def drucke(html, pdf):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / pdf}",
                    "--virtual-time-budget=4000", f"file://{HIER / html}"], check=True, capture_output=True)
    print("gedruckt:", pdf)


if __name__ == "__main__":
    for html, pdf, titel, fn in (("ladungen.html", "Atome enthalten elektrische Ladungen W01.pdf", "Atome enthalten elektrische Ladungen – W01", w01),
                                 ("nuklide.html", "Nuklide und Isotope W02.pdf", "Nuklide und Isotope – W02", w02),
                                 ("zaehlrohr.html", "Zaehlrohr und Nullrate W03.pdf", "Zählrohr und Nullrate – W03", w03),
                                 ("strahlungsarten.html", "Drei Strahlungsarten W04.pdf", "Drei Arten radioaktiver Strahlung – W04", w04),
                                 ("durchdringung.html", "Durchdringung und Zerfallsgleichungen W05.pdf", "Durchdringung und Zerfallsgleichungen – W05", w05)):
        (HIER / html).write_text(dokument(titel, [fn(False), fn(True)]), encoding="utf-8")
        drucke(html, pdf)
