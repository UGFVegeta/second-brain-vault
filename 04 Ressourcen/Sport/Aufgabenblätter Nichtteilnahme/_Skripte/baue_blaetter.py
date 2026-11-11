#!/usr/bin/env python3
"""Aufgabenblätter für Schüler, die im Sportunterricht nicht mitmachen können.

Format: A4 doppelseitig. Vorderseite Infotext, Rückseite Aufgaben ○ ◐ ●.
Je Blatt zwei PDFs: Schülerfassung und Lösung (dasselbe Blatt, ausgefüllt in Magenta).

Aufruf:  python3 baue_blaetter.py
Neue Blätter: Funktion nach dem Muster von blatt_teller() schreiben und in BLAETTER eintragen.
"""
import shutil
import subprocess
from pathlib import Path

HIER = Path(__file__).resolve().parent
BASIS = HIER.parent
VAULT = BASIS.parents[2]
LOGO = VAULT / "07 Anhänge" / "GDRS Logo.png"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ICLOUD = (Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Schuljahr 26 27/Sport"
          / "Aufgabenblätter Nichtteilnahme")

ACC = "#1f6fb2"   # Überschriften
LOE = "#c2185b"   # Lösungsfarbe

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'Open Sans', Helvetica, Arial, sans-serif; font-size: 10.6pt; line-height: 1.42; color: #1b1b1b; }}
.seite {{ width: 210mm; height: 297mm; padding: 8mm 10mm 7mm 10mm; position: relative; overflow: hidden; page-break-after: always; }}
.seite:last-child {{ page-break-after: auto; }}
.kopf {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2.5px solid {ACC}; padding-bottom: 2.5mm; margin-bottom: 3.5mm; }}
.kopf .reihe {{ font-size: 8.5pt; color: #666; letter-spacing: .02em; }}
.kopf h1 {{ font-size: 19pt; margin: .5mm 0 1.5mm 0; color: {ACC}; line-height: 1.15; }}
.kopf .felder {{ font-size: 9pt; color: #444; display: flex; gap: 6mm; }}
.kopf .felder span.f {{ display: inline-block; border-bottom: 1px solid #999; min-width: 42mm; height: 4mm; }}
.kopf .felder span.k {{ min-width: 14mm; }}
.kopf img {{ width: 21mm; }}
.hinweis {{ background: #eef4fa; border-radius: 2mm; padding: 2mm 3mm; font-size: 9.6pt; margin-bottom: 3mm; }}
h2 {{ font-size: 12.5pt; color: {ACC}; margin: 3.2mm 0 1.2mm 0; border-bottom: 1px solid #c9d9ea; padding-bottom: .6mm; }}
h2 .buchst {{ display: inline-block; background: {ACC}; color: #fff; border-radius: 1.2mm; width: 6mm; text-align: center; margin-right: 2mm; font-size: 11pt; }}
p {{ margin: 0 0 1.6mm 0; }}
.zwei {{ display: flex; gap: 5mm; align-items: center; }}
.zwei > div {{ flex: 1; }}
.wichtig {{ border: 2px solid {ACC}; border-radius: 2.5mm; padding: 2.2mm 3.5mm; margin-top: 3mm; }}
.wichtig b.t {{ color: {ACC}; display: block; margin-bottom: .8mm; }}
.wichtig ul {{ margin: 0; padding-left: 5mm; }}
.ampel {{ display: inline-block; width: 3.2mm; height: 3.2mm; border-radius: 50%; vertical-align: -0.4mm; margin-right: 1mm; }}
table.info {{ border-collapse: collapse; width: 100%; font-size: 10pt; margin: 1mm 0 1.5mm 0; }}
table.info td, table.info th {{ border: 1px solid #bbb; padding: 1.1mm 2.2mm; }}
table.info th {{ background: #eef4fa; text-align: left; }}
.legende {{ display: flex; justify-content: space-between; align-items: center; font-size: 9pt; color: #444; margin-bottom: 2.5mm; }}
.legende svg {{ vertical-align: -3px; }}
.auf {{ margin-bottom: 3.4mm; }}
.auf .k {{ display: flex; align-items: flex-start; gap: 2mm; margin-bottom: 1.4mm; }}
.auf .nr {{ background: {ACC}; color: #fff; font-weight: 700; border-radius: 1.2mm; min-width: 6mm; text-align: center; font-size: 10pt; }}
.auf .txt {{ font-weight: 600; }}
.gap {{ display: inline-block; border: 1.3px solid #777; border-radius: 1.6mm; height: 6.2mm; vertical-align: middle; text-align: center; line-height: 5.8mm; color: {LOE}; font-weight: 600; font-size: 10pt; }}
.lines {{ position: relative; }}
.lines .l {{ border-bottom: 1px solid #9a9a9a; height: 7.5mm; }}
.lines .lt {{ position: absolute; left: 1mm; right: 1mm; top: 1.6mm; color: {LOE}; font-size: 10pt; line-height: 7.5mm; font-weight: 600; }}
table.rf {{ border-collapse: collapse; width: 100%; font-size: 10pt; }}
table.rf td {{ border-bottom: 1px solid #ddd; padding: .9mm 1.5mm; }}
table.rf td.x {{ width: 13mm; text-align: center; }}
.kreuz {{ display: inline-block; width: 4.6mm; height: 4.6mm; border: 1.3px solid #555; border-radius: 1mm; text-align: center; line-height: 4mm; color: {LOE}; font-weight: 700; }}
.spalten {{ display: grid; gap: 3mm; }}
.box {{ border: 1.3px solid #888; border-radius: 2mm; padding: 1.5mm 2.5mm; }}
.box .t {{ font-weight: 700; font-size: 9.6pt; margin-bottom: 1mm; }}
.loe {{ color: {LOE}; font-weight: 600; }}
.karo {{ background-image: linear-gradient(#cfd8e3 1px, transparent 1px), linear-gradient(90deg, #cfd8e3 1px, transparent 1px);
        background-size: 5mm 5mm; border: 1px solid #b8c4d2; position: relative; }}
.wortkasten {{ border: 1px dashed #888; border-radius: 2mm; padding: 1mm 3mm; font-size: 9.8pt; margin-bottom: 1.5mm; }}
.fuss {{ position: absolute; bottom: 6mm; left: 15mm; right: 15mm; font-size: 8pt; color: #888; display: flex; justify-content: space-between; }}
"""

FONT = '<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">'


# ------------------------------------------------------------------ Bausteine
def kreis(stufe, size=15):
    s = (f'<svg viewBox="0 0 20 20" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
         f'<circle cx="10" cy="10" r="8" fill="#fff" stroke="#333" stroke-width="1.6"/>')
    if stufe == 1:
        s += '<path d="M10 2 A8 8 0 0 0 10 18 Z" fill="#333"/>'
    elif stufe == 2:
        s += '<circle cx="10" cy="10" r="8" fill="#333"/>'
    return s + "</svg>"


def kopf(reihe, titel, logo=True):
    img = f'<img src="{LOGO.as_uri()}">' if logo else ""
    return (f'<div class="kopf"><div><div class="reihe">{reihe}</div><h1>{titel}</h1>'
            f'<div class="felder">Name <span class="f"></span> Klasse <span class="f k"></span> Datum <span class="f k"></span></div>'
            f'</div>{img}</div>')


def abschnitt(b, titel):
    return f'<h2><span class="buchst">{b}</span>{titel}</h2>'


def wichtig(punkte):
    li = "".join(f"<li>{p}</li>" for p in punkte)
    return f'<div class="wichtig"><b class="t">Das Wichtigste</b><ul>{li}</ul></div>'


def legende():
    return (f'<div class="legende"><span>Fang mit den {kreis(0,13)}-Aufgaben an. Du musst nicht alles schaffen.<br>'
            f'Gib das Blatt am Ende der Stunde ab.</span>'
            f'<span style="white-space:nowrap">{kreis(0,13)} leicht &nbsp; {kreis(1,13)} mittel &nbsp; {kreis(2,13)} schwer</span></div>')


def aufgabe(nr, stufe, text, inhalt):
    return (f'<div class="auf"><div class="k">{kreis(stufe)}<span class="nr">{nr}</span>'
            f'<span class="txt">{text}</span></div>{inhalt}</div>')


def gap(L, inhalt, breite=22):
    return f'<span class="gap" style="width:{breite}mm">{inhalt if L else ""}</span>'


def linien(L, n, text=""):
    ls = '<div class="l"></div>' * n
    t = f'<div class="lt">{text}</div>' if (L and text) else ""
    return f'<div class="lines">{ls}{t}</div>'


def richtig_falsch(L, saetze):
    """saetze: Liste (Satz, True/False)"""
    rows = '<tr><td></td><td class="x"><b>richtig</b></td><td class="x"><b>falsch</b></td></tr>'
    for s, w in saetze:
        r = "✗" if (L and w) else ""
        f = "✗" if (L and not w) else ""
        rows += (f'<tr><td>{s}</td><td class="x"><span class="kreuz">{r}</span></td>'
                 f'<td class="x"><span class="kreuz">{f}</span></td></tr>')
    return f'<table class="rf">{rows}</table>'


def fuss(text):
    return ""  # keine Fußzeilen (Platz für Inhalt)


def seite(inhalt):
    return f'<div class="seite">{inhalt}</div>'


# ------------------------------------------------------------------ Grafiken
def pyramide():
    """Ernährungspyramide, sechs Stufen, Ampelfarben, Portionen am Tag."""
    gruen, gelb, rot = "#7cc47a", "#f3d35b", "#e8706a"
    stufen = [  # von unten
        ("Getränke", "6", "#8fc9e8"),
        ("Gemüse 3   Obst 2", "5", gruen),
        ("Brot, Nudeln, Reis, Kartoffeln", "4", gruen),
        ("Milch, Käse 3   Fleisch, Fisch, Ei 1", "4", gelb),
        ("Öl, Butter", "2", gelb),
        ("Süßes", "1", rot),
    ]
    W, H, top, n = 380, 216, 70, len(stufen)
    bh = H / n
    out = [f'<svg viewBox="0 0 {W} {H+4}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="Open Sans, Helvetica, sans-serif">']

    def breite(y):  # y von oben
        return top + (W - top) * (y / H)

    for i, (txt, port, farbe) in enumerate(stufen):
        yb = H - i * bh
        yt = yb - bh
        wb, wt = breite(yb), breite(yt)
        pts = f"{(W-wb)/2},{yb} {(W+wb)/2},{yb} {(W+wt)/2},{yt} {(W-wt)/2},{yt}"
        out.append(f'<polygon points="{pts}" fill="{farbe}" stroke="#fff" stroke-width="2.5"/>')
        teile = txt.split("   ")
        fs = 11.5 if i < 4 else 11
        label = "   ".join(teile) if i != 3 else txt
        if i == 3:
            out.append(f'<text x="{W/2}" y="{yt+bh/2+4}" text-anchor="middle" font-size="10.5" font-weight="600">'
                       f'Milch, Käse <tspan font-weight="700">3</tspan><tspan dx="16">Fleisch, Fisch, Ei </tspan><tspan font-weight="700">1</tspan></text>')
        elif i == 1:
            out.append(f'<text x="{W/2}" y="{yt+bh/2+4}" text-anchor="middle" font-size="{fs}" font-weight="600">'
                       f'Gemüse <tspan font-weight="700">3</tspan><tspan dx="22">Obst </tspan><tspan font-weight="700">2</tspan></text>')
        else:
            out.append(f'<text x="{W/2}" y="{yt+bh/2+4}" text-anchor="middle" font-size="{fs}" font-weight="600">'
                       f'{label} <tspan font-weight="700">{port}</tspan></text>')
    out.append("</svg>")
    return "".join(out)


def teller():
    """Teller: halb Gemüse und Obst, Viertel Beilage, Viertel Eiweiß."""
    return ('<svg viewBox="0 0 150 150" width="100%" xmlns="http://www.w3.org/2000/svg" '
            'font-family="Open Sans, Helvetica, sans-serif" font-size="10.5" font-weight="600">'
            '<circle cx="75" cy="75" r="72" fill="#f4f4f4" stroke="#999" stroke-width="2"/>'
            '<path d="M75 75 L75 9 A66 66 0 0 0 75 141 Z" fill="#7cc47a"/>'
            '<path d="M75 75 L75 9 A66 66 0 0 1 141 75 Z" fill="#f2c46b"/>'
            '<path d="M75 75 L141 75 A66 66 0 0 1 75 141 Z" fill="#f3d35b"/>'
            '<text x="42" y="72" text-anchor="middle">Gemüse</text><text x="42" y="86" text-anchor="middle">und Obst</text>'
            '<text x="105" y="48" text-anchor="middle">Kartoffeln,</text><text x="105" y="61" text-anchor="middle">Nudeln, Reis</text>'
            '<text x="105" y="100" text-anchor="middle">Fleisch, Fisch,</text><text x="105" y="113" text-anchor="middle">Ei, Käse</text>'
            '</svg>')


def wuerfel(anzahl, pro_reihe=9, s=13, gapx=3):
    reihen = (anzahl + pro_reihe - 1) // pro_reihe
    w = pro_reihe * (s + gapx)
    h = reihen * (s + gapx)
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w*0.95:.0f}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(anzahl):
        x = (i % pro_reihe) * (s + gapx)
        y = (i // pro_reihe) * (s + gapx)
        out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="2" fill="#fff" stroke="#555" stroke-width="1.4"/>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ Blatt 1: Teller
def blatt_teller(L):
    reihe = "Sport ohne Mitmachen  |  Klasse 5 und 6  |  Essen und Trinken, Blatt 1"
    v = kopf(reihe, "Was auf den Teller gehört")
    v += '<div class="hinweis">Lies den Text in Ruhe. Die Aufgaben stehen auf der Rückseite.</div>'
    v += abschnitt("A", "Warum Essen wichtig ist")
    v += ('<p>Dein Körper braucht Essen wie ein Auto Benzin. Essen gibt dir Kraft zum Rennen, Springen und Denken. '
          'Außerdem baut es deinen Körper auf: Du wächst gerade, deine Knochen und Muskeln werden größer. '
          'Dafür braucht dein Körper jeden Tag viele verschiedene Lebensmittel.</p>')
    v += abschnitt("B", "Die Ernährungspyramide")
    v += ('<p>Die Ernährungspyramide zeigt, wie viel du von welchen Lebensmitteln essen solltest. '
          'Die Zahl in jeder Stufe sagt dir, wie viele Portionen du am Tag davon brauchst. '
          'Eine Portion ist ungefähr so groß wie deine Hand. Unten steht, wovon du viel brauchst. '
          'Je weiter oben, desto weniger.</p>')
    v += f'<div style="width:110mm;margin:.5mm auto .5mm auto">{pyramide()}</div>'
    v += ('<p>Die Farben funktionieren wie eine Ampel:<br>'
          '<span class="ampel" style="background:#7cc47a"></span><b>grün: reichlich.</b> Getränke wie Wasser und ungesüßter Tee, Gemüse, Obst, Brot, Nudeln, Reis, Kartoffeln.<br>'
          '<span class="ampel" style="background:#f3d35b"></span><b>gelb: mäßig.</b> Milch, Käse, Joghurt, Fleisch, Wurst, Fisch, Eier, Öl und Butter.<br>'
          '<span class="ampel" style="background:#e8706a"></span><b>rot: sparsam.</b> Süßigkeiten, Kuchen, Chips, Limo und Cola.</p>')
    v += abschnitt("C", "Ein guter Teller")
    v += ('<div class="zwei"><div><p>Für eine warme Mahlzeit kannst du dir einen Teller merken. '
          'Die <b>Hälfte</b> ist Gemüse oder Salat, dazu vielleicht etwas Obst als Nachtisch. '
          'Ein <b>Viertel</b> sind Kartoffeln, Nudeln, Reis oder Brot. '
          'Das letzte <b>Viertel</b> sind Fleisch, Fisch, Eier, Käse oder Bohnen. Dazu gibt es ein Glas Wasser.</p>'
          '<p>Verboten ist kein Lebensmittel. Ein Stück Schokolade ist in Ordnung. '
          'Es kommt darauf an, wie viel du davon isst und wie oft.</p></div>'
          f'<div style="flex:0 0 46mm">{teller()}</div></div>')
    v += wichtig(["Iss bunt und abwechslungsreich.",
                  "Viel von unten aus der Pyramide, wenig von oben.",
                  "Wasser ist das beste Getränk."])
    v += fuss("Vorderseite: Text")

    r = legende()
    r += aufgabe(1, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
        ("Von Süßigkeiten solltest du am meisten essen.", False),
        ("Eine Portion ist ungefähr so groß wie deine Hand.", True),
        ("Getränke stehen ganz unten in der Pyramide.", True),
        ("Fleisch und Wurst gehören in den gelben Bereich.", True),
        ("Schokolade ist verboten.", False),
    ]))
    lm = {"grün": ["Apfel", "Vollkornbrot", "Karotte", "Wasser", "Nudeln"],
          "gelb": ["Joghurt", "Fischstäbchen", "Käse", "Butter"],
          "rot": ["Gummibärchen", "Chips", "Cola"]}
    farben = {"grün": "#7cc47a", "gelb": "#f3d35b", "rot": "#e8706a"}
    alle = "Apfel, Gummibärchen, Vollkornbrot, Joghurt, Chips, Karotte, Fischstäbchen, Wasser, Cola, Nudeln, Käse, Butter"
    sp = ""
    for f, items in lm.items():
        inh = "<br>".join(items) if L else ""
        sp += (f'<div class="box" style="min-height:35mm"><div class="t"><span class="ampel" style="background:{farben[f]}"></span>{f}</div>'
               f'<div class="loe">{inh}</div></div>')
    r += aufgabe(2, 0, "Schreibe jedes Lebensmittel in die richtige Ampelfarbe.",
                 f'<div class="wortkasten">{alle}</div><div class="spalten" style="grid-template-columns:1fr 1fr 1fr">{sp}</div>')
    port = [("Getränke", 6), ("Gemüse", 3), ("Obst", 2), ("Brot, Nudeln", 4),
            ("Milch, Käse", 3), ("Fleisch, Fisch, Ei", 1), ("Öl, Butter", 2), ("Süßes", 1)]
    pp = "".join(f'<div>{n} {gap(L, z, 9)}</div>' for n, z in port)
    r += aufgabe(3, 0, "Wie viele Portionen am Tag? Schau in der Pyramide nach.",
                 f'<div class="spalten" style="grid-template-columns:repeat(4,1fr);row-gap:1.5mm;font-size:10pt">{pp}</div>')
    teil = ""
    if L:  # Lösung: Kreis geteilt und beschriftet
        teil = ('<path d="M50 50 L50 3 M50 50 L50 97 M50 50 L97 50" stroke="#c2185b" stroke-width="1.4"/>'
                '<text x="27" y="52" fill="#c2185b" font-size="8" text-anchor="middle">Brokkoli,</text>'
                '<text x="27" y="61" fill="#c2185b" font-size="8" text-anchor="middle">Karotten</text>'
                '<text x="73" y="32" fill="#c2185b" font-size="7.5" text-anchor="middle">Kartoffeln</text>'
                '<text x="73" y="76" fill="#c2185b" font-size="7.5" text-anchor="middle">Fisch</text>')
    kreis_svg = ('<svg viewBox="0 0 100 100" width="40mm" height="40mm" font-family="Open Sans, Helvetica, sans-serif" font-weight="600">'
                 f'<circle cx="50" cy="50" r="47" fill="#fff" stroke="#777" stroke-width="1.4"/>{teil}</svg>')
    r += aufgabe(4, 1, "Mein Teller: Teile den Kreis wie im Text auf und schreibe hinein, was du zu Mittag essen würdest. "
                       "Schreibe daneben, was du dazu trinkst und was es als Nachtisch gibt.",
                 f'<div style="display:flex;gap:5mm;align-items:flex-start">{kreis_svg}'
                 f'<div style="flex:1">{linien(L, 5, "Beispiel: Dazu trinke ich ein Glas Wasser. Als Nachtisch gibt es einen Apfel.")}</div></div>')
    r += aufgabe(5, 1, "Schreibe auf, was du heute gefrühstückt hast. Gib zu jedem Lebensmittel die Ampelfarbe an.",
                 linien(L, 2, "Beispiel: Müsli (grün) mit Milch (gelb), Banane (grün), Wasser (grün)"))
    r += aufgabe(6, 2, "Ein Freund isst mittags fast jeden Tag Pommes und trinkt Cola dazu. "
                       "Gib ihm zwei Tipps und begründe sie mit der Pyramide.",
                 linien(L, 3, "Trink Wasser statt Cola, denn Cola hat viel Zucker und steht rot ganz oben. "
                              "Iss mehr Gemüse dazu, es steht weit unten im grünen Bereich. Pommes sind sehr fettig, "
                              "besser öfter Kartoffeln oder Nudeln."))
    r += fuss("Rückseite: Aufgaben")
    return seite(v) + seite(r)


# ------------------------------------------------------------------ Blatt 2: Trinken
def blatt_trinken(L):
    reihe = "Sport ohne Mitmachen  |  Klasse 5 und 6  |  Essen und Trinken, Blatt 2"
    v = kopf(reihe, "Trinken beim Sport")
    v += '<div class="hinweis">Lies den Text in Ruhe. Die Aufgaben stehen auf der Rückseite.</div>'
    v += abschnitt("A", "Wasser in deinem Körper")
    v += ('<p>Dein Körper besteht zu mehr als der Hälfte aus Wasser. Das Wasser bringt Nährstoffe zu den Muskeln '
          'und zum Gehirn. Es hilft auch, deinen Körper zu kühlen.</p>'
          '<p>Beim Sport arbeiten deine Muskeln und werden warm. Damit dir nicht zu heiß wird, schwitzt du. '
          'Der Schweiß verdunstet auf der Haut und kühlt dich ab. In einer Sportstunde kannst du so '
          'bis zu einem halben Liter Wasser verlieren. Dieses Wasser musst du wieder trinken.</p>')
    v += abschnitt("B", "Wie viel und wann?")
    v += ('<p>Kinder in deinem Alter sollten jeden Tag gut einen Liter trinken. Das sind ungefähr 6 Gläser. '
          'An Sporttagen und bei Hitze brauchst du mehr.</p>'
          '<p>Warte nicht, bis du großen Durst hast. Trink schon <b>vor</b> dem Sport, '
          'in den <b>Pausen</b> ein paar kleine Schlucke und <b>nach</b> dem Sport noch einmal richtig.</p>'
          '<p>Wenn du zu wenig getrunken hast, merkst du das: Du hast Durst, wirst müde und schlapp, '
          'bekommst Kopfschmerzen oder kannst dich schlecht konzentrieren. Auch dunkelgelber Urin ist ein Zeichen.</p>')
    v += abschnitt("C", "Was trinken?")
    v += ('<p>Das beste Getränk ist Wasser. Es löscht den Durst und hat keinen Zucker. '
          'Ungesüßter Tee ist genauso gut. Viele andere Getränke enthalten sehr viel Zucker, auch Saft. '
          'Ein Stück Würfelzucker wiegt ungefähr <b>3 g</b>.</p>')
    tab = ('<table class="info"><tr><th>Getränk (eine Flasche, 0,5 Liter)</th><th>Zucker, etwa</th></tr>'
           '<tr><td>Wasser</td><td>0 g</td></tr><tr><td>Ungesüßter Tee</td><td>0 g</td></tr>'
           '<tr><td>Apfelschorle (halb Saft, halb Wasser)</td><td>24 g</td></tr>'
           '<tr><td>Eistee</td><td>33 g</td></tr><tr><td>Apfelsaft</td><td>51 g</td></tr>'
           '<tr><td>Cola</td><td>54 g</td></tr></table>')
    bsp = (f'<div style="font-size:9.6pt"><b>So viel Zucker steckt in einer Flasche Cola:</b><br>'
           f'54 g : 3 g = 18 Stück Würfelzucker<div style="margin-top:1.5mm">{wuerfel(18)}</div></div>')
    v += f'<div class="zwei" style="align-items:flex-start"><div>{tab}</div><div style="flex:0 0 62mm">{bsp}</div></div>'
    v += ('<p>Energydrinks sind für Kinder nicht geeignet. Sie enthalten viel Zucker und Koffein, '
          'das Herz schlägt dann schneller.</p>')
    v += wichtig(["Trink vor, während und nach dem Sport, nicht erst bei großem Durst.",
                  "Wasser und ungesüßter Tee sind die besten Getränke.",
                  "Saft, Eistee und Cola haben sehr viel Zucker."])
    v += fuss("Vorderseite: Text")

    r = legende()
    lt = ("Dein Körper besteht zu mehr als der {0} aus Wasser. Beim Sport {1} du. Der Schweiß {2} den Körper. "
          "Du solltest jeden Tag gut {3} trinken. Das beste Getränk ist {4}.")
    worte = ["Hälfte", "schwitzt", "kühlt", "einen Liter", "Wasser"]
    lt = lt.format(*[gap(L, w, 25) for w in worte])
    r += aufgabe(1, 0, "Setze die Wörter aus dem Kasten in die Lücken ein.",
                 '<div class="wortkasten">kühlt &nbsp;&nbsp; Wasser &nbsp;&nbsp; Hälfte &nbsp;&nbsp; einen Liter &nbsp;&nbsp; schwitzt</div>'
                 f'<p style="line-height:2.05">{lt}</p>')
    r += aufgabe(2, 0, "Woran merkst du, dass du zu wenig getrunken hast? Nenne drei Zeichen.",
                 linien(L, 2, "Durst, müde und schlapp, Kopfschmerzen, schlecht konzentriert, dunkelgelber Urin"))
    r += aufgabe(3, 0, "Wann trinkst du beim Sport? Kreuze an.", richtig_falsch(L, [
        ("vor dem Sport", True),
        ("in den Pausen ein paar kleine Schlucke", True),
        ("erst, wenn ich sehr großen Durst habe", False),
        ("nach dem Sport", True),
    ]))
    rech = [("Apfelschorle", "24 g : 3 g = 8"), ("Eistee", "33 g : 3 g = 11"), ("Apfelsaft", "51 g : 3 g = 17"), ("Wasser", "0")]
    rr = "".join(f'<div>{n}<br>{gap(L, e, 38)} Würfel</div>' for n, e in rech)
    r += aufgabe(4, 1, "Wie viele Stück Würfelzucker sind in einer Flasche? Rechne wie im Beispiel mit der Cola.",
                 f'<div class="spalten" style="grid-template-columns:repeat(4,1fr);font-size:10pt">{rr}</div>')
    zeich = ""
    if L:
        zeich = (f'<div style="position:absolute;left:5mm;top:4mm" class="loe">Apfelschorle: 8'
                 f'<div style="margin-top:1mm">{wuerfel(8, 8)}</div></div>'
                 f'<div style="position:absolute;left:92mm;top:4mm" class="loe">Apfelsaft: 17'
                 f'<div style="margin-top:1mm">{wuerfel(17, 9)}</div></div>')
    r += aufgabe(5, 1, "Zeichne für die Apfelschorle und den Apfelsaft die Zuckerwürfel als Kästchen ins Karofeld.",
                 f'<div class="karo" style="height:25mm">{zeich}</div>')
    r += aufgabe(6, 2, "Deine Freundin sagt: „Apfelsaft ist gesund, davon kann ich beim Sport so viel trinken, wie ich will.“ "
                       "Was antwortest du ihr? Begründe.",
                 linien(L, 3, "Apfelsaft hat fast so viel Zucker wie Cola, etwa 17 Würfel in einer Flasche. "
                              "Gegen den Durst beim Sport ist Wasser besser. Wenn Saft, dann als Schorle mit viel Wasser."))
    r += aufgabe(7, 0, "Was hast du gestern getrunken? Schreibe auf, wie viele Gläser es waren. Hast du genug getrunken?",
                 linien(L, 2, "Beispiel: 3 Gläser Wasser, 1 Glas Saft, 1 Tasse Tee. Das sind 5 Gläser, etwas zu wenig."))
    r += fuss("Rückseite: Aufgaben")
    return seite(v) + seite(r)


# ------------------------------------------------------------------ Blatt 3: Energie
def kachel(farbe, titel, rolle, text):
    return (f'<div style="border-radius:2.5mm;padding:2mm 3mm;background:{farbe}">'
            f'<div style="font-weight:700;font-size:11pt">{titel}</div>'
            f'<div style="font-weight:700;color:#333;font-size:9.6pt;margin-bottom:.8mm">{rolle}</div>'
            f'<div style="font-size:9.8pt;line-height:1.35">{text}</div></div>')


def blatt_energie(L):
    reihe = "Sport ohne Mitmachen  |  Klasse 5 und 6  |  Essen und Trinken, Blatt 3"
    v = kopf(reihe, "Energie für den Sport")
    v += '<div class="hinweis">Lies den Text in Ruhe. Die Aufgaben stehen auf der Rückseite.</div>'
    v += abschnitt("A", "Was im Essen steckt")
    v += ('<p>In unserem Essen stecken verschiedene Nährstoffe. Jeder Nährstoff hat im Körper eine eigene Aufgabe. '
          'Du kannst sie dir wie eine Baustelle vorstellen: Es braucht Treibstoff für die Maschinen, '
          'Baustoff für das Haus, einen Vorrat für später und Helfer, die alles am Laufen halten.</p>')
    v += ('<div class="spalten" style="grid-template-columns:1fr 1fr;margin:1.5mm 0 1mm 0">'
          + kachel("#d9efd8", "Kohlenhydrate", "der Treibstoff",
                   "geben schnell Energie für Muskeln und Gehirn. Sie stecken in Brot, Nudeln, Reis, Kartoffeln und Obst.")
          + kachel("#fbe9c2", "Eiweiß", "der Baustoff",
                   "baut Muskeln auf und repariert sie nach dem Sport. Es steckt in Milch, Käse, Quark, Fleisch, Fisch, Eiern, Bohnen und Linsen.")
          + kachel("#f6d9d6", "Fett", "der Vorrat",
                   "speichert Energie für später. Du brauchst nur wenig davon. Es steckt in Öl, Butter und Nüssen, versteckt auch in Wurst, Chips und Pommes.")
          + kachel("#dbe8f5", "Vitamine und Mineralstoffe", "die Helfer",
                   "halten dich gesund und machen die Knochen stark. Sie stecken vor allem in Obst, Gemüse und Milch.")
          + '</div>')
    v += abschnitt("B", "Vor dem Sport")
    v += ('<p>Die letzte große Mahlzeit isst du am besten <b>zwei bis drei Stunden</b> vor dem Sport. '
          'Mit vollem Bauch läuft und springt es sich schlecht, weil dein Körper noch mit Verdauen beschäftigt ist. '
          'Dann bekommst du schnell Seitenstechen oder dir wird übel.</p>'
          '<p>Kurz vorher reicht eine Kleinigkeit, zum Beispiel eine Banane oder ein Stück Brot. '
          'Mit ganz leerem Magen ist es aber auch nicht gut: Dann fehlt dir die Energie, du wirst schlapp und unkonzentriert. '
          'Deshalb ist ein Frühstück an einem Sporttag besonders wichtig.</p>')
    v += abschnitt("C", "Nach dem Sport")
    v += ('<p>Nach dem Sport trinkst du zuerst, denn beim Schwitzen hast du Wasser verloren. '
          'Bei der nächsten Mahlzeit braucht dein Körper zwei Dinge: Kohlenhydrate, um die leeren Speicher aufzufüllen, '
          'und Eiweiß, um die Muskeln zu reparieren. Gut sind zum Beispiel ein Käsebrot, Joghurt mit Obst '
          'oder Nudeln mit Hackfleischsoße.</p>')
    v += wichtig(["Kohlenhydrate sind der Treibstoff, Eiweiß ist der Baustoff.",
                  "Große Mahlzeit zwei bis drei Stunden vor dem Sport, kurz vorher nur eine Kleinigkeit.",
                  "Nach dem Sport erst trinken, dann Kohlenhydrate und Eiweiß essen."])
    v += fuss("Vorderseite: Text")

    r = legende()
    zu = [("Kohlenhydrate", "Treibstoff"), ("Eiweiß", "Baustoff"), ("Fett", "Vorrat"), ("Vitamine", "Helfer")]
    zz = "".join(f'<div>{n}<br>{gap(L, w, 34)}</div>' for n, w in zu)
    r += aufgabe(1, 0, "Welche Aufgabe hat der Nährstoff? Schreibe Treibstoff, Baustoff, Vorrat oder Helfer.",
                 f'<div class="spalten" style="grid-template-columns:repeat(4,1fr);font-size:10pt">{zz}</div>')
    lm = {"Kohlenhydrate": ["Reis", "Kartoffel", "Vollkornbrot"],
          "Eiweiß": ["Quark", "Ei", "Hähnchen"],
          "Fett": ["Butter", "Olivenöl"],
          "Vitamine": ["Paprika", "Orange"]}
    sp = ""
    for n, items in lm.items():
        inh = "<br>".join(items) if L else ""
        sp += f'<div class="box" style="min-height:24mm"><div class="t">{n}</div><div class="loe">{inh}</div></div>'
    r += aufgabe(2, 0, "Wovon steckt am meisten drin? Schreibe die Lebensmittel in die richtige Spalte.",
                 '<div class="wortkasten">Reis, Quark, Butter, Paprika, Kartoffel, Ei, Olivenöl, Orange, Hähnchen, Vollkornbrot</div>'
                 f'<div class="spalten" style="grid-template-columns:repeat(4,1fr)">{sp}</div>')
    r += aufgabe(3, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
        ("Direkt vor dem Sport isst man am besten eine große Portion Pommes.", False),
        ("Eine Banane ist ein guter Snack kurz vor dem Sport.", True),
        ("Eiweiß hilft, die Muskeln zu reparieren.", True),
        ("Wer ohne Frühstück zum Sport kommt, hat mehr Energie.", False),
        ("Nach dem Sport sollte man zuerst etwas trinken.", True),
    ]))
    plan = [("Frühstück um 7 Uhr", "Müsli mit Milch und Apfel"),
            ("Pause um 9:30 Uhr", "Banane, Wasser"),
            ("Mittagessen nach dem Sport", "Nudeln mit Soße, Salat, Wasser")]
    pp = "".join(f'<div class="box" style="min-height:19mm"><div class="t">{t}</div><div class="loe">{"Beispiel: " + b if L else ""}</div></div>'
                 for t, b in plan)
    r += aufgabe(4, 1, "Du hast heute in der 3. und 4. Stunde Sport. Plane, was du isst.",
                 f'<div class="spalten" style="grid-template-columns:repeat(3,1fr)">{pp}</div>')
    r += aufgabe(5, 1, "Warum ist es schlecht, mit vollem Bauch Sport zu machen? Erkläre mit eigenen Worten.",
                 linien(L, 2, "Der Körper ist noch mit Verdauen beschäftigt. Man bekommt Seitenstechen oder es wird einem übel."))
    r += aufgabe(6, 2, "Ein Junge sagt: „Ich esse nur noch Eiweiß, dann bekomme ich mehr Muskeln.“ Was ist daran falsch?",
                 linien(L, 3, "Eiweiß baut Muskeln auf, aber ohne Kohlenhydrate fehlt der Treibstoff. Dann ist er beim Sport schlapp "
                              "und kann gar nicht richtig trainieren. Er braucht alle Nährstoffe, also abwechslungsreich essen."))
    salat = [("TTEF", "Fett"), ("ßWEIIE", "Eiweiß"), ("NETAMIVI", "Vitamine"), ("NANABE", "Banane")]
    ss = "".join(f'<div><b style="letter-spacing:.15em">{w}</b><br>{gap(L, l, 34)}</div>' for w, l in salat)
    r += aufgabe(7, 0, "Buchstabensalat: Welches Wort aus dem Text ist gemeint?",
                 f'<div class="spalten" style="grid-template-columns:repeat(4,1fr);font-size:10pt">{ss}</div>')
    r += fuss("Rückseite: Aufgaben")
    return seite(v) + seite(r)


# ------------------------------------------------------------------ Bauen
BLAETTER = [
    ("Klasse 5 und 6/Essen und Trinken", "Essen und Trinken 1 – Was auf den Teller gehört", blatt_teller),
    ("Klasse 5 und 6/Essen und Trinken", "Essen und Trinken 2 – Trinken beim Sport", blatt_trinken),
    ("Klasse 5 und 6/Essen und Trinken", "Essen und Trinken 3 – Energie für den Sport", blatt_energie),
]


def html(body, titel, fs=10.6):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title>{FONT}'
            f'<style>{CSS} body {{ font-size: {fs}pt; }}</style></head><body>{body}</body></html>')


GROESSEN = (12.4, 12.0, 11.6, 11.2, 10.8, 10.6, 10.3, 10.0)  # Schrift so groß wie möglich, solange beide Seiten passen


def pdf(src, ziel):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={ziel}", src.as_uri()],
                   check=True, capture_output=True)


PRUEF_JS = """<script>
window.addEventListener('load', () => setTimeout(() => {
  const out = [];
  document.querySelectorAll('.seite').forEach((s, i) => {
    const top = s.getBoundingClientRect().top;
    let unten = 0;
    s.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height) unten = Math.max(unten, r.bottom - top); });
    out.push(Math.round(100 * unten / s.clientHeight));
  });
  document.body.setAttribute('data-fuell', out.join(','));
}, 1500));
</script>"""


def fuellstand(h):
    """Füllstand je Seite in Prozent der Seitenhöhe (über ca. 97 = zu voll)."""
    pr = h.with_name(h.stem + "_pruef.html")
    pr.write_text(h.read_text(encoding="utf-8").replace("</body>", PRUEF_JS + "</body>"), encoding="utf-8")
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=8000",
                          "--dump-dom", pr.as_uri()], capture_output=True, text=True).stdout
    pr.unlink()
    import re
    m = re.search(r'data-fuell="([^"]*)"', dom)
    return m.group(1) if m else "?"


def alle_blaetter():
    import stufe56
    liste = BLAETTER + stufe56.BLAETTER
    for modul in ("stufe78", "stufe910"):
        if (HIER / f"{modul}.py").exists():
            liste += __import__(modul).BLAETTER
    return liste


def main():
    import sys
    filt = sys.argv[1] if len(sys.argv) > 1 else ""
    tmp = HIER / "html"
    tmp.mkdir(exist_ok=True)
    for ordner, name, fn in alle_blaetter():
        if filt not in ordner + "/" + name:
            continue
        ziel = BASIS / ordner
        ziel.mkdir(parents=True, exist_ok=True)
        # passende Schriftgröße an der Lösung (der vollsten Fassung) bestimmen
        h = tmp / f"{name}_fit.html"
        oben = 12.4 if "5 und 6" in ordner else (11.6 if "7 und 8" in ordner else 11.2)  # Ältere: kleinere Höchstschrift
        for fs in [g for g in GROESSEN if g <= oben]:
            h.write_text(html(fn(True), name, fs), encoding="utf-8")
            werte = [int(x) for x in fuellstand(h).split(",") if x.isdigit()]
            if werte and max(werte) <= 97:
                break
        h.unlink()
        for L, suffix in ((False, ""), (True, " (Lösung)")):
            h = tmp / f"{name}{suffix}.html"
            h.write_text(html(fn(L), name + suffix, fs), encoding="utf-8")
            p = ziel / f"{name}{suffix}.pdf"
            pdf(h, p)
            kopie = ICLOUD / ordner
            kopie.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, kopie / p.name)  # zusätzlich in die Schul-iCloud
            info = f"  Schrift {fs} pt, Füllstand {fuellstand(h)} %" if L else ""
            print("gebaut:", p.relative_to(BASIS), info)
    import baue_uebersicht
    baue_uebersicht.main()  # Übersicht.html aktuell halten


if __name__ == "__main__":
    main()
