"""Auswertung Diagnose Dreiecke 7c als EINE HTML mit Tabs (wie die Stunden-HTMLs).

Tabs: Klasse | Aufgaben | Selbsteinschätzung | Nummern | Förderung | Für die Klasse (Beamer, ohne Nummern).
Daten: Auswertung 7c/ergebnisse_dreiecke.json, Zuteilung aus baue_foerderblaetter.py.
Aufruf: python3 baue_auswertung.py
"""
import json
import sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(HIER.parents[1]))
from baue_foerderblaetter import auswerten, zuteilen, POOL, BEREICH, DIAG, AUSW, nummer_sort  # noqa: E402
from mathe_woche_vorlage import OPTIK_CSS, PRAES_CSS, praesentation  # noqa: E402

ZIEL = HIER / "Diagnose Dreiecke 7c – Auswertung.html"   # neben den PDFs, damit die Links auch in iCloud gehen
STUFE = ["○", "◐", "●"]
GRUEN, ORANGE, ROT, GRAU = "#1d7a2e", "#c77800", "#b3261e", "#9aa3ad"

FEHLER = {
    "1": "Meist richtig. Einzelne lesen 7,5 oder 8 cm ab: vermutlich ab dem Linealrand statt ab 0 gemessen.",
    "2": "Fast alle richtig. In Version B zwei Strecken etwa 2 mm zu lang.",
    "3": "Häufigster Fehler: stumpf und überstumpf vertauscht. Vereinzelt recht und stumpf verwechselt.",
    "4": "Viele leer. Falsche Skala am Geodreieck (36° statt 143°, 37° statt 118°). Mehrere messen in cm (5,2; 4,6; 0,6).",
    "5": "Falsche Skala: der Nebenwinkel wird gezeichnet (35° statt 145°, 50° statt 130°). Schenkel nicht am Scheitel S angesetzt. Einige zeichnen 90°.",
    "6": "Kaum jemand nutzt die 180°-Idee, Werte sind oft geraten. Den Scheitelwinkel γ = α erkennen einige.",
    "7": "Senkrechte wird als Verbindung A–B oder zum Ende von g gezeichnet. Einige richten sich am Karo aus statt an g. Parallele gelingt eher als Senkrechte.",
    "8": "x und y vertauscht (B und C landen falsch). Einheit 1 Kästchen statt 1 cm. Achsen ohne Zahlen.",
}
FOLGERUNG = [
    "Vor der Winkelsumme: Geodreieck mit beiden Skalen gezielt üben (messen und zeichnen, zuerst schätzen: spitz oder stumpf?).",
    "Senkrechte mit dem Geodreieck einmal vormachen: Mittellinie auf g, Kante durch den Punkt. Danach Parallele.",
    "Nebenwinkel als „zusammen 180°“ einführen, das ist die Brücke zur Winkelsumme im Dreieck.",
    "Koordinatensystem kurz wiederholen: erst x nach rechts, dann y nach oben, 1 cm = 2 Kästchen.",
]


def art_aus(status, items):
    st = [status.get(i, "offen") for i in items]
    if all(z == "richtig" for z in st):
        return "richtig"
    if all(z == "offen" for z in st):
        return "leer"
    return "teils" if any(z == "richtig" for z in st) else "falsch"


SYM = {"richtig": f'<span class="s" style="color:{GRUEN}">✓</span>', "teils": f'<span class="s" style="color:{ORANGE}">◑</span>',
       "falsch": f'<span class="s" style="color:{ROT}">✗</span>', "leer": f'<span class="s" style="color:{GRAU}">–</span>'}


def balken(werte, breite=640, gross=False):
    """werte: [(Name, Anteil 0..1)]. Horizontale Balken, Ampelfarbe."""
    zh, fs = (54, 20) if gross else (34, 14)
    lab = 300 if gross else 230
    h = zh * len(werte) + 10
    s = f'<svg viewBox="0 0 {breite} {h}" style="width:100%;max-width:{breite}px">'
    for i, (n, q) in enumerate(werte):
        y = 5 + zh * i
        farbe = GRUEN if q >= .75 else ORANGE if q >= .5 else "#e0a100" if q >= .25 else ROT
        bw = (breite - lab - 60) * q
        s += f'<text x="{lab-10}" y="{y+zh*.62}" font-size="{fs}" text-anchor="end" fill="#1b1b1b">{n}</text>'
        s += f'<rect x="{lab}" y="{y+zh*.18}" width="{breite-lab-60}" height="{zh*.6}" rx="4" fill="#eef1f5"/>'
        s += f'<rect x="{lab}" y="{y+zh*.18}" width="{bw:.1f}" height="{zh*.6}" rx="4" fill="{farbe}"/>'
        s += f'<text x="{lab+bw+8:.1f}" y="{y+zh*.62}" font-size="{fs}" font-weight="700" fill="#1b1b1b">{q*100:.0f} %</text>'
    return s + "</svg>"


FARBE = {"richtig": "#2e7d32", "teils": "#e8a317", "falsch": "#c62828", "leer": "#e3e6ea"}
TEXTF = {"richtig": "#fff", "teils": "#1b1b1b", "falsch": "#fff", "leer": "#6b7280"}
ZEICHEN = {"richtig": "✓", "teils": "◑", "falsch": "✗", "leer": "–"}
WORT = {"richtig": "richtig", "teils": "zum Teil", "falsch": "falsch", "leer": "leer"}
SMILEY = {"sicher": "🙂", "ging_so": "😐", "unsicher": "🙁"}
SMWORT = {"sicher": "sicher", "ging_so": "ging so", "unsicher": "unsicher"}


def legende_ergebnis():
    return '<div class="leg">' + "".join(
        f'<span><i style="background:{FARBE[k]};color:{TEXTF[k]}">{ZEICHEN[k]}</i>{WORT[k]}</span>' for k in FARBE) + \
        '<span><i class="rand"></i>„sicher“ angekreuzt, aber nicht richtig</span></div>'


def kacheln(werte):
    return '<div class="kacheln">' + "".join(f'<div class="kachel"><b>{z}</b><span>{t}</span></div>' for z, t in werte) + "</div>"


KURZ = ["Längen", "Strecke", "Winkelarten", "messen", "zeichnen", "Nebenwinkel", "Senkrechte", "Koord."]


def klassenbild(nummern, daten, sel):
    """Heatmap: Zeilen Nummern (beste oben), Spalten die 8 Aufgaben, Rand = sicher, aber daneben."""
    def punkte(nr):
        return sum({"richtig": 1, "teils": .5}.get(art_aus(daten[nr]["status"], it), 0) for _, _, it in DIAG)
    reihen = sorted(nummern, key=lambda nr: -punkte(nr))
    cw, ch, lx, top = 62, 24, 70, 44
    w, h = lx + cw * 8 + 110, top + ch * len(reihen) + 8
    s = f'<svg viewBox="0 0 {w} {h}" style="width:100%;max-width:{w}px" font-family="-apple-system,Helvetica,Arial">'
    for j, (a, name, _) in enumerate(DIAG):
        x = lx + cw * j + cw / 2
        s += f'<text x="{x}" y="16" font-size="12" font-weight="700" text-anchor="middle" fill="#1b1b1b">Nr. {a}</text>'
        s += f'<text x="{x}" y="31" font-size="9.5" text-anchor="middle" fill="#6b7280">{KURZ[j]}</text>'
    s += f'<text x="{lx + cw * 8 + 12}" y="31" font-size="9.5" fill="#6b7280">Punkte von 8</text>'
    for i, nr in enumerate(reihen):
        y = top + ch * i
        s += f'<text x="{lx - 10}" y="{y + 16}" font-size="12.5" font-weight="700" text-anchor="end" fill="#1b1b1b">{nr}</text>'
        for j, (a, name, it) in enumerate(DIAG):
            art = art_aus(daten[nr]["status"], it)
            sm = sel.get(nr, {}).get(f"N{a}")
            daneben = sm == "sicher" and art != "richtig"
            x = lx + cw * j
            tip = f"Nummer {nr}, Nr. {a} {name}: {WORT[art]}" + (f"; Smiley: {SMWORT[sm]}" if sm else "; kein Smiley")
            s += (f'<g><title>{tip}</title><rect x="{x + 1}" y="{y + 1}" width="{cw - 2}" height="{ch - 2}" rx="4" fill="{FARBE[art]}"'
                  + (' stroke="#111" stroke-width="2.4"' if daneben else "") + "/>"
                  f'<text x="{x + cw / 2}" y="{y + 16.5}" font-size="13" font-weight="700" text-anchor="middle" fill="{TEXTF[art]}">{ZEICHEN[art]}</text></g>')
        p = punkte(nr)
        bx = lx + cw * 8 + 12
        s += f'<rect x="{bx}" y="{y + 7}" width="70" height="10" rx="3" fill="#eef1f5"/><rect x="{bx}" y="{y + 7}" width="{70 * p / 8:.1f}" height="10" rx="3" fill="#1a56a0"/>'
        s += f'<text x="{bx + 76}" y="{y + 16}" font-size="11" fill="#1b1b1b">{p:g}</text>'
    return s + "</svg>"


def matrix(nummern, daten, sel):
    """Selbsteinschätzung (Zeilen) gegen Ergebnis (Spalten), Anteile je Zeile."""
    zeilen = ["sicher", "ging_so", "unsicher"]
    spalten = ["richtig", "teils", "falsch", "leer"]
    z = {(r, c): 0 for r in zeilen for c in spalten}
    for nr in nummern:
        for a, _, it in DIAG:
            sm = sel.get(nr, {}).get(f"N{a}")
            if sm in zeilen:
                z[(sm, art_aus(daten[nr]["status"], it))] += 1
    t = '<table class="matrix"><tr><th></th>' + "".join(f'<th><i style="background:{FARBE[c]};color:{TEXTF[c]}">{ZEICHEN[c]}</i> {WORT[c]}</th>' for c in spalten) + "<th>Kreuze</th></tr>"
    for r in zeilen:
        summe = sum(z[(r, c)] for c in spalten) or 1
        t += f'<tr><th>{SMILEY[r]} {SMWORT[r]}</th>'
        for c in spalten:
            q = z[(r, c)] / summe
            t += f'<td style="background:rgba(26,86,160,{0.08 + 0.8 * q:.2f});color:{"#fff" if q > .45 else "#1b1b1b"}" title="{SMWORT[r]} und {WORT[c]}: {z[(r, c)]} von {summe}"><b>{q * 100:.0f} %</b><span>{z[(r, c)]}</span></td>'
        t += f'<td class="c">{summe}</td></tr>'
    return t + "</table>"


def hantel(nummern, daten, sel, gross=False):
    """Je Aufgabe: Anteil richtig bei „sicher“ gegen „ging so/unsicher“."""
    w, lx, top, zh = (1000, 300, 40, 56) if gross else (760, 190, 30, 34)
    fs, fa, rp = (20, 15, 10) if gross else (12.5, 10.5, 6.5)
    breite = w - lx - 60
    s = f'<svg viewBox="0 0 {w} {top + zh * 8 + 10}" style="width:100%;max-width:{w}px" font-family="-apple-system,Helvetica,Arial">'
    for k in range(0, 101, 25):
        x = lx + breite * k / 100
        s += f'<line x1="{x}" y1="{top - 8}" x2="{x}" y2="{top + zh * 8}" stroke="#e3e6ea"/><text x="{x}" y="{top - 12}" font-size="{fa}" text-anchor="middle" fill="#6b7280">{k} %</text>'
    for i, (a, name, it) in enumerate(DIAG):
        y = top + zh * i + zh / 2
        werte = []
        for gruppe in (("sicher",), ("ging_so", "unsicher")):
            g = [nr for nr in nummern if sel.get(nr, {}).get(f"N{a}") in gruppe]
            r = sum(art_aus(daten[nr]["status"], it) == "richtig" for nr in g)
            werte.append((r / len(g) if g else None, r, len(g)))
        s += f'<text x="{lx - 12}" y="{y + 4}" font-size="{fs}" text-anchor="end" fill="#1b1b1b"><tspan font-weight="700">Nr. {a}</tspan> {name}</text>'
        xs = [lx + breite * q for q, _, _ in werte if q is not None]
        if len(xs) == 2:
            s += f'<line x1="{xs[0]}" y1="{y}" x2="{xs[1]}" y2="{y}" stroke="#9aa3ad" stroke-width="2"/>'
        for (q, r, nn), farbe, wort in zip(werte, ("#1a56a0", "#e8a317"), ("sicher", "ging so / unsicher")):
            if q is None:
                continue
            x = lx + breite * q
            s += f'<g><title>Nr. {a}, {wort}: {r} von {nn} richtig</title><circle cx="{x}" cy="{y}" r="11" fill="transparent"/><circle cx="{x}" cy="{y}" r="{rp}" fill="{farbe}" stroke="#fff" stroke-width="2"/></g>'
    return s + "</svg>"


def stapel(nummern, daten):
    """Je Aufgabe ein 100-%-Balken: richtig, zum Teil, falsch, leer (nur Klassenwerte)."""
    w, lx, top, zh = 1000, 250, 6, 58
    breite = w - lx - 10
    s = f'<svg viewBox="0 0 {w} {top + zh * 8}" style="width:100%" font-family="-apple-system,Helvetica,Arial">'
    for i, (a, name, it) in enumerate(DIAG):
        y = top + zh * i
        z = {k: 0 for k in FARBE}
        for nr in nummern:
            z[art_aus(daten[nr]["status"], it)] += 1
        s += f'<text x="{lx - 14}" y="{y + 32}" font-size="20" text-anchor="end" fill="#1b1b1b"><tspan font-weight="700">Nr. {a}</tspan> {name}</text>'
        x = lx
        for k in ("richtig", "teils", "falsch", "leer"):
            bw = breite * z[k] / len(nummern)
            if bw:
                s += (f'<g><title>Nr. {a}: {WORT[k]} {z[k]} von {len(nummern)}</title><rect x="{x:.1f}" y="{y + 10}" width="{max(bw - 3, 1):.1f}" height="36" rx="5" fill="{FARBE[k]}"/>'
                      + (f'<text x="{x + bw / 2:.1f}" y="{y + 34}" font-size="18" font-weight="700" text-anchor="middle" fill="{TEXTF[k]}">{z[k]}</text>' if bw > 30 else "") + "</g>")
            x += bw
    return s + "</svg>"


def bauen():
    daten = auswerten()
    roh = json.loads((AUSW / "ergebnisse_dreiecke.json").read_text(encoding="utf-8"))
    sel = roh.get("selbsteinschaetzung", {})
    nummern = sorted(daten, key=nummer_sort)
    n = len(nummern)
    zut = {nr: zuteilen(daten[nr]["quoten"])[0] for nr in nummern}

    # Klasse
    klasse = sorted(((BEREICH[b], sum(daten[nr]["quoten"][b] for nr in nummern) / n) for b in BEREICH), key=lambda x: -x[1])
    sicher_alle = [(nr, a_, it) for nr in nummern for a_, _, it in DIAG if sel.get(nr, {}).get(f"N{a_}") == "sicher"]
    daneben_alle = [x for x in sicher_alle if art_aus(daten[x[0]]["status"], x[2]) != "richtig"]
    anteil = len(daneben_alle) / len(sicher_alle) if sicher_alle else 0
    t_klasse = (kacheln([(n, "Bögen ausgewertet"), (f"{klasse[0][1]*100:.0f} %", f"stärkster Bereich: {klasse[0][0]}"),
                         (f"{klasse[-1][1]*100:.0f} %", f"schwächster Bereich: {klasse[-1][0]}"),
                         (f"{anteil*100:.0f} %", "„sicher“ angekreuzt, aber nicht richtig")])
                + f'<div class="box"><h3>Ergebnis je Bereich ({n} Bögen, leer zählt als nicht gekonnt)</h3>{balken(klasse)}</div>'
                + f'<div class="box"><h3>Klassenbild: jede Nummer, jede Aufgabe</h3><p class="hinweis">Sortiert nach Punkten, beste oben. Maus über ein Feld zeigt Ergebnis und Smiley.</p>{legende_ergebnis()}{klassenbild(nummern, daten, sel)}</div>'
                '<div class="box"><h3>Was daraus für die Einheit folgt</h3><ol>' + "".join(f"<li>{x}</li>" for x in FOLGERUNG) + "</ol></div>")

    # Aufgaben
    zeilen = ""
    for nr_a, name, items in DIAG:
        z = {"richtig": 0, "teils": 0, "falsch": 0, "leer": 0}
        for nr in nummern:
            z[art_aus(daten[nr]["status"], items)] += 1
        zeilen += (f'<tr><td><b>Nr. {nr_a}</b><br>{name}</td><td class="c">{z["richtig"]}</td><td class="c">{z["teils"]}</td>'
                   f'<td class="c">{z["falsch"]}</td><td class="c">{z["leer"]}</td><td>{FEHLER[nr_a]}</td></tr>')
    t_aufg = ('<div class="box"><h3>Ergebnis je Diagnose-Aufgabe und typische Fehler</h3><table class="ha"><tr><th>Aufgabe</th>'
              f'<th>{SYM["richtig"]}</th><th>{SYM["teils"]}</th><th>{SYM["falsch"]}</th><th>{SYM["leer"]}</th><th>Typische Fehler</th></tr>{zeilen}</table>'
              '<p class="hinweis">Zeichnungen (Nr. 2, 5, 7, 8) sind aus dem Scan beurteilt, Winkel auf etwa ±3° genau.</p></div>')

    # Selbsteinschätzung
    pro_nr = sorted(((nr, sum(1 for x in daneben_alle if x[0] == nr)) for nr in nummern), key=lambda x: -x[1])
    liste = "".join(f'<div class="zeile"><b>{nr}</b><div class="mini"><i style="width:{k*28}px"></i></div><span>{k}</span></div>' for nr, k in pro_nr if k)
    t_sel = (kacheln([(len(sicher_alle), "Kreuze bei „sicher“"), (len(daneben_alle), "davon nicht ganz richtig"), (f"{anteil*100:.0f} %", "Fehleinschätzung bei „sicher“")])
             + '<div class="box"><h3>Gefühl gegen Ergebnis (alle Aufgaben, alle Kinder)</h3><p class="hinweis">Jede Zeile ergibt 100 %. Gut eingeschätzt heißt: '
             'bei „sicher“ viel Grün, bei „unsicher“ eher Rot oder leer.</p>' + matrix(nummern, daten, sel) + '</div>'
             + '<div class="box"><h3>Je Aufgabe: Wie oft war es richtig?</h3><div class="leg"><span><i style="background:#1a56a0"></i>wer „sicher“ angekreuzt hat</span>'
             '<span><i style="background:#e8a317"></i>wer „ging so“ oder „unsicher“ angekreuzt hat</span></div>' + hantel(nummern, daten, sel)
             + '<p class="hinweis">Liegen beide Punkte nah beieinander oder ist Blau links, hilft das Gefühl bei dieser Aufgabe nicht weiter.</p></div>'
             + f'<div class="box"><h3>Wer hat sich bei welcher Zahl von Aufgaben überschätzt?</h3><p class="hinweis">Anzahl der Aufgaben mit „sicher“, die nicht ganz richtig waren. Gut fürs Einzelgespräch.</p><div class="liste">{liste}</div></div>'
             + '<p class="hinweis">Die Smileys sind aus dem Scan gelesen, viele Kinder haben zwei angemalt. Nur als Tendenz nutzen.</p>')

    # Nummern
    karten = ""
    for nr in nummern:
        d = daten[nr]
        zeile = ""
        for a, _, it in DIAG:
            art, sm = art_aus(d["status"], it), sel.get(nr, {}).get(f"N{a}")
            rand = " daneben" if sm == "sicher" and art != "richtig" else ""
            zeile += (f'<div class="zelle"><span>Nr. {a}</span><i class="feld{rand}" style="background:{FARBE[art]};color:{TEXTF[art]}">{ZEICHEN[art]}</i>'
                      f'<em title="{SMWORT.get(sm, "kein Smiley")}">{SMILEY.get(sm, "–")}</em></div>')
        karten += (f'<div class="nkarte"><div class="kk"><b>{nr}</b><span>Version {d["version"]}</span></div><div class="reihe">{zeile}</div>'
                   f'<div class="foerd">Förderblatt: {"; ".join(zut[nr])}</div></div>')
    t_num = ('<div class="box"><h3>Ergebnis pro Nummer</h3><p class="hinweis">Unter jedem Feld der Smiley des Kindes. Bogen-IDs (A03, A07, A11, B05, B09) stehen für noch unklare Nummern.</p>' + legende_ergebnis()
             + f'<div class="karten">{karten}</div></div>')

    # Förderung
    wie_oft = {kz: sum(kz in zut[nr] for nr in nummern) for kz, *_ in POOL}
    themen = {kz: f.__doc__ or "" for kz, *_, f in POOL}
    zeilen = "".join(f'<tr><td><b>{kz}</b></td><td class="c">{STUFE[st]}</td><td>{BEREICH.get(b, "Ausblick Dreiecke")}</td><td class="c">{wie_oft[kz]}</td></tr>'
                     for kz, b, st, _h, _f in POOL)
    t_foerd = ('<div class="box"><h3>Förderblätter</h3><p>Ein doppelseitiges A4-Blatt pro Nummer. Bereich unter 50 % gibt ○ und ◐, unter 100 % ◐, '
               'Restplatz ● und Ausblick. Lösungen zum Aushängen, gesucht wird nach dem Kürzel.</p><p>'
               '<a href="Mathe 7c – Förderblätter Dreiecke – alle Nummern.pdf">Förderblätter (alle Nummern)</a> &nbsp; '
               '<a href="Mathe 7c – Förderblätter Dreiecke – Lösungen.pdf">Lösungen zum Aushängen</a> &nbsp; '
               '<a href="Mathe 7c – Diagnose Dreiecke – Lösung.pdf">Lösung der Diagnose</a></p>'
               f'<table class="ha"><tr><th>Kürzel</th><th>Stufe</th><th>Bereich</th><th>wie oft verteilt</th></tr>{zeilen}</table></div>')
    del themen

    # Präsentation für die Klasse: nur Werte der ganzen Klasse, keine Nummern
    gb = (f'<div class="gross"><div class="gb"><i style="width:{(1-anteil)*100:.1f}%;background:#2e7d32">richtig {(1-anteil)*100:.0f} %</i>'
          f'<i style="width:{anteil*100:.1f}%;background:#c62828">daneben {anteil*100:.0f} %</i></div><span>alle Kreuze bei „sicher“</span></div>')
    legsel = ('<div class="leg gr"><span><i style="background:#1a56a0"></i>„sicher“ angekreuzt</span>'
              '<span><i style="background:#e8a317"></i>„ging so“ oder „unsicher“ angekreuzt</span></div>')
    karten3 = "".join(f'<div class="tipp"><b>{t}</b><p>{x}</p></div>' for t, x in (
        ("Winkel messen und zeichnen", "Erst schätzen: spitz oder stumpf? Dann die passende Skala am Geodreieck ablesen."),
        ("Senkrechte", "Mittellinie des Geodreiecks genau auf g legen, die Kante läuft durch den Punkt."),
        ("Koordinatensystem", "Erst x nach rechts, dann y nach oben. 1 cm sind 2 Kästchen.")))
    folien = [
        ("Diagnose Dreiecke: Was ihr schon könnt", kacheln([(n, "Bögen ausgewertet"), (f"{klasse[0][1]*100:.0f} %", klasse[0][0]),
                                                            (f"{klasse[1][1]*100:.0f} %", klasse[1][0])])
         + '<p class="kern">Das ist keine Note. Es zeigt uns, wo wir mit den Dreiecken ansetzen.</p>'),
        ("So steht die Klasse", balken(klasse, 1000, True)),
        ("Aufgabe für Aufgabe", legende_ergebnis().replace('<span><i class="rand"></i>„sicher“ angekreuzt, aber nicht richtig</span>', "") + stapel(nummern, daten)),
        ("Gefühl und Ergebnis", '<p class="kern klein">Jede Zeile ergibt 100 %. Gut eingeschätzt heißt: bei „sicher“ viel Grün.</p>' + matrix(nummern, daten, sel)),
        ("Sicher, aber daneben", gb + f'<p class="kern">Bei „sicher“ lagt ihr in {anteil*100:.0f} % der Fälle trotzdem daneben. Genau dort lohnt sich ein zweiter Blick.</p>'),
        ("Wo hilft das Gefühl?", legsel + hantel(nummern, daten, sel, True)),
        ("Typische Stolperstellen", f'<div class="tipps">{karten3}</div>'),
        ("Dein Förderblatt", '<ol class="schritte"><li>Oben steht dein Ergebnis aus der Diagnose.</li><li>Bearbeite die Aufgaben der Reihe nach, mit Geodreieck und Bleistift.</li>'
         '<li>Kontrolliere selbst am Lösungsblatt. Gesucht wird nach dem Kürzel, zum Beispiel M2.</li></ol>'
         '<p class="kern">○ leicht &nbsp; ◐ mittel &nbsp; ● schwer</p>'),
    ]
    leiste = [("Ergebnis", "Start", None), ("Ergebnis", "Bereiche", None), ("Ergebnis", "Aufgaben", None),
              ("Selbsteinschätzung", "Gefühl und Ergebnis", None), ("Selbsteinschätzung", "Sicher, aber daneben", None), ("Selbsteinschätzung", "Je Aufgabe", None),
              ("Wie geht es weiter", "Stolperstellen", None), ("Wie geht es weiter", "Förderblatt", None)]
    praes_html, praes_js = praesentation(folien, leiste, {t for t, _ in folien}, "Diagnose Dreiecke")
    t_praes = '<p class="hinweis">Nur Werte der ganzen Klasse, keine Nummern. Zum Zeigen: F für Vollbild, T blendet die Leiste aus.</p>' + praes_html

    tabs = [("klasse", "Klasse", t_klasse), ("aufg", "Aufgaben", t_aufg), ("sel", "Selbsteinschätzung", t_sel),
            ("num", "Nummern", t_num), ("foerd", "Förderung", t_foerd), ("folien", "Präsentation", t_praes)]
    css = """<style>
th{text-align:left;padding:6px 8px;border-bottom:2px solid #d9dfe7;font-size:14px}.c{text-align:center}.s{font-weight:700;font-size:17px}
.hinweis{color:#6b7280;font-size:13.5px}.karten{display:grid;align-items:start;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}
.nkarte{border:1px solid #d9dfe7;border-radius:8px;padding:10px 12px}.kk{display:flex;justify-content:space-between;margin-bottom:6px}
.kk b{font-size:20px}.kk span{color:#6b7280;font-size:13px}.reihe{display:grid;grid-template-columns:repeat(8,1fr);gap:3px}
.zelle{text-align:center;font-size:11px;color:#6b7280}.zelle .s{display:block;font-size:18px}.foerd{margin-top:7px;font-size:13.5px}
.kacheln{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:0 0 14px}.kachel{background:#f6f8fb;border:1px solid #d9dfe7;border-radius:10px;padding:14px 16px}.kachel b{display:block;font-size:34px;line-height:1.1}.kachel span{color:#4b5563;font-size:13.5px}.leg{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:#4b5563;margin:4px 0 10px}.leg i{display:inline-block;min-width:18px;height:18px;border-radius:4px;margin-right:6px;vertical-align:-4px;text-align:center;font-style:normal;font-weight:700;font-size:12px;line-height:18px}.leg i.rand{background:#fff;border:2.4px solid #111;box-sizing:border-box}table.matrix{border-collapse:separate;border-spacing:4px;width:100%;max-width:760px}.matrix th{font-size:13.5px;border:0;text-align:left}.matrix th i{display:inline-block;width:18px;height:18px;border-radius:4px;text-align:center;font-style:normal;line-height:18px;font-size:12px}.matrix td{border-radius:6px;padding:10px;text-align:center}.matrix td b{display:block;font-size:20px}.matrix td span{font-size:12px;opacity:.85}.liste{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:4px 20px}.zeile{display:flex;align-items:center;gap:10px;font-size:14px}.zeile b{width:44px;text-align:right}.mini i{display:block;height:12px;border-radius:3px;background:#c62828}.zelle .feld{display:block;margin:2px auto;width:28px;height:22px;border-radius:4px;font-style:normal;font-weight:700;line-height:22px}.zelle .feld.daneben{outline:2.4px solid #111;outline-offset:-2px}.zelle em{display:block;font-style:normal;font-size:14px;color:#4b5563}.gross{margin:26px 0 6px;max-width:1000px}.gb{display:flex;height:54px;border-radius:8px;overflow:hidden;gap:3px}.gb i{display:flex;align-items:center;padding-left:14px;color:#fff;font-style:normal;font-weight:700;font-size:20px;white-space:nowrap}.gross span{color:#4b5563;font-size:15px}#stage .seite{font-size:22px}#stage .seite>h1{font-size:34px}#stage .kachel b{font-size:56px}#stage .kachel span{font-size:20px}#stage .kern{font-size:28px}#stage .kern.klein{font-size:22px;margin:0 0 14px}#stage .matrix td b{font-size:30px}#stage .matrix th{font-size:20px}#stage .matrix td span{font-size:16px}#stage .leg{font-size:19px}#stage .leg i{min-width:24px;height:24px;line-height:24px;font-size:16px}.tipps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:20px}.tipp{background:#f6f8fb;border:1px solid #d9dfe7;border-radius:12px;padding:20px}.tipp b{font-size:24px}.tipp p{font-size:22px;margin:10px 0 0}.schritte{font-size:28px;line-height:1.5;margin-top:20px}.schritte li{margin:10px 0}.beamer{padding:20px 0}.beamer h2{font-size:34px;margin:0 0 20px}.kern{font-size:24px;margin-top:24px;max-width:900px}
</style>"""
    html = (f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Diagnose Dreiecke 7c – Auswertung</title>{OPTIK_CSS}{PRAES_CSS}{css}</head><body>'
            '<div class="wrap"><header class="kopf"><h1>Diagnose Dreiecke 7c: Auswertung</h1>'
            f'<p class="sub">geschrieben am 04.11.2026; {n} Bögen (12 × A, 12 × B); ohne Note, nur Nummern</p></header></div>'
            '<nav><div class="wrap tabs">' + "".join(f'<button data-t="{i}">{t}</button>' for i, t, _ in tabs) + '</div></nav><div class="wrap">'
            + "".join(f'<div class="tab" id="t_{i}">{inhalt}</div>' for i, _, inhalt in tabs) + "</div><script>"
            "const tabs=[...document.querySelectorAll('nav button')],secs=[...document.querySelectorAll('.tab')];"
            "function show(id){tabs.forEach(b=>b.classList.toggle('on',b.dataset.t===id));secs.forEach(s=>s.classList.toggle('on',s.id==='t_'+id));"
            "history.replaceState(null,'','#'+id);window.scrollTo(0,0)}tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));"
            "document.addEventListener('keydown',e=>{const i=tabs.findIndex(b=>b.classList.contains('on'));if(tabs[i]&&tabs[i].dataset.t==='folien')return;"
            "if(e.key==='ArrowRight'&&i<tabs.length-1)show(tabs[i+1].dataset.t);if(e.key==='ArrowLeft'&&i>0)show(tabs[i-1].dataset.t)});"
            "show((location.hash||'#klasse').slice(1));</script>" + praes_js + "</body></html>")
    ZIEL.write_text(html, encoding="utf-8")
    return ZIEL


if __name__ == "__main__":
    print(bauen().name)
