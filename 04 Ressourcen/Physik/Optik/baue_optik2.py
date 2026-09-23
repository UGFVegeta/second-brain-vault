#!/usr/bin/env python3
"""Baut 'Optik 2 – Licht trifft auf einen Körper – ALLES.html' (Klasse 7c, Physik, Doppelstunde Do 24.09.2026).

Standard wie bei Mathe (baue_stunde1/2.py): eine HTML mit Tabs, alles drin.
Änderungen: hier im Skript, dann `python3 baue_optik1.py`. PDFs erst nach Freigabe.
Quellen: Optik-I-Folien (Optik I.html/.pdf), Arbeitsblatt F1 (Materialien/lichtquellen.html),
Schulbuch Erlebnis Physik 7–9 (nur Seitenverweise, Fotos von Oskar), LEIFIphysik (nur als Anregung, eigene Formulierung).
"""
from pathlib import Path

INK, MUT, BL, GR = "#1b1b1b", "#5a5a5a", "#1a56a0", "#66798e"


# ---------------------------------------------------------------- kleine SVG-Bausteine
def sun(x, y, r=13):
    rays = "".join(
        f'<line x1="{x + (r + 3) * c:.1f}" y1="{y + (r + 3) * s:.1f}" x2="{x + (r + 9) * c:.1f}" y2="{y + (r + 9) * s:.1f}" '
        f'stroke="#b98900" stroke-width="2"/>'
        for c, s in [(1, 0), (.7, .7), (0, 1), (-.7, .7), (-1, 0), (-.7, -.7), (0, -1), (.7, -.7)])
    return f'{rays}<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd34d" stroke="#b98900" stroke-width="2"/>'


def candle(x, y):
    return (f'<rect x="{x - 6}" y="{y - 4}" width="12" height="28" fill="#f5e6c8" stroke="#777"/>'
            f'<path d="M{x} {y - 22} q7 9 0 17 q-7 -8 0 -17z" fill="#ffb02e" stroke="#c76b00"/>')


def bulb(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="13" fill="#fff2a8" stroke="#b98900" stroke-width="2"/>'
            f'<rect x="{x - 6}" y="{y + 12}" width="12" height="9" fill="#bbb" stroke="#777"/>')


def moon(x, y):
    return (f'<path d="M{x + 5} {y - 15} A15 15 0 1 0 {x + 5} {y + 15} A11 11 0 1 1 {x + 5} {y - 15} Z" '
            f'fill="#c9ced6" stroke="{GR}" stroke-width="2"/>')


def book(x, y):
    return (f'<rect x="{x - 18}" y="{y - 11}" width="36" height="24" fill="#8da6c2" stroke="{GR}" stroke-width="2"/>'
            f'<line x1="{x}" y1="{y - 11}" x2="{x}" y2="{y + 13}" stroke="{GR}" stroke-width="2"/>')


def tree(x, y):
    return (f'<rect x="{x - 3}" y="{y + 4}" width="6" height="18" fill="#8b5a2b"/>'
            f'<circle cx="{x}" cy="{y - 4}" r="15" fill="#5fae5f" stroke="#2f7a2f" stroke-width="2"/>')


def eye(x, y):
    return (f'<ellipse cx="{x}" cy="{y}" rx="17" ry="9" fill="#fff" stroke="{GR}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="5" fill="#8da6c2" stroke="{GR}" stroke-width="1.5"/>')


def pfeil(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#b98900" stroke-width="2.4" '
            f'marker-end="url(#sp)"/>')


DEFS = ('<defs><marker id="sp" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">'
        '<path d="M0,0 L8,4 L0,8 Z" fill="#b98900"/></marker></defs>')


def fig(svg, cap=""):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure>{svg}{c}</figure>'


TAFEL1 = (f'<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg" width="640">'
          f'<rect width="640" height="230" fill="#fff"/>'
          f'<text x="70" y="26" font-size="17" font-weight="700" fill="{INK}">Lichtquellen</text>'
          f'<text x="392" y="26" font-size="17" font-weight="700" fill="{INK}">beleuchtete Körper</text>'
          f'<line x1="320" y1="10" x2="320" y2="215" stroke="#c8d0dc" stroke-dasharray="5 5"/>'
          f'{sun(70, 90)}<text x="52" y="135" font-size="14">Sonne</text>'
          f'{candle(160, 82)}<text x="140" y="135" font-size="14">Kerze</text>'
          f'{bulb(250, 88)}<text x="222" y="135" font-size="14">Glühlampe</text>'
          f'{moon(390, 88)}<text x="372" y="135" font-size="14">Mond</text>'
          f'{book(480, 88)}<text x="464" y="135" font-size="14">Buch</text>'
          f'{tree(570, 82)}<text x="553" y="135" font-size="14">Baum</text>'
          f'<text x="40" y="180" font-size="14" fill="{MUT}">senden selbst Licht aus</text>'
          f'<text x="372" y="180" font-size="14" fill="{MUT}">werfen fremdes Licht zurück</text></svg>')

TAFEL_WEG = (f'<svg viewBox="0 0 640 170" xmlns="http://www.w3.org/2000/svg" width="640">{DEFS}'
             f'<rect width="640" height="170" fill="#fff"/>'
             f'{sun(60, 70)}<text x="22" y="120" font-size="14">Lichtquelle</text><text x="22" y="138" font-size="13" fill="{MUT}">(Sender)</text>'
             f'{pfeil(100, 70, 250, 70)}'
             f'{tree(300, 62)}<text x="245" y="120" font-size="14">beleuchteter Körper</text>'
             f'{pfeil(335, 72, 500, 72)}'
             f'{eye(550, 72)}<text x="518" y="120" font-size="14">Auge</text><text x="512" y="138" font-size="13" fill="{MUT}">(Empfänger)</text>'
             f'<text x="130" y="55" font-size="13" fill="#8a4b00">Licht trifft auf</text>'
             f'<text x="360" y="55" font-size="13" fill="#8a4b00">Licht wird zurückgeworfen</text></svg>')

CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;color:#1b1b1b;background:#fff}
.wrap{max-width:1000px;margin:0 auto;padding:0 22px}
header.kopf{padding:30px 0 12px;border-bottom:2px solid #1b1b1b}
h1{font-size:27px;margin:0 0 4px;line-height:1.2}.sub{color:#555;margin:0}
nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #d9d9d4;z-index:5}
nav .wrap{display:flex;gap:6px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
nav a{padding:5px 13px;border-radius:16px;text-decoration:none;color:#1b1b1b;font-size:14px;background:#f1f1ed}
nav a:hover{background:#e3e3dc}
section{padding:34px 0 8px;scroll-margin-top:50px}
h2{font-size:22px;margin:0 0 6px}.lead{color:#555;margin:0 0 16px}
h3{font-size:17px;margin:24px 0 8px}h4{margin:16px 0 6px;font-size:16.5px}
.ziel{background:#f5f5f1;border-radius:8px;padding:12px 16px;margin:16px 0}
.knapp{background:#fff6e0;border-left:4px solid #e0a100;padding:7px 12px;margin:10px 0 4px;font-size:15px}
.fehler{background:#fbeeee;border-left:4px solid #b3261e;padding:8px 14px;margin:16px 0}
.fehler ol{margin:6px 0 2px;padding-left:20px}
.warn{background:#fff6e0;border-left:4px solid #e0a100;padding:9px 14px;margin:8px 0;font-size:14.5px}
.opt{background:#eef3fb;border-left:4px solid #1a56a0;padding:9px 14px;margin:8px 0;font-size:14.5px}
.box{border:1px solid #d3d3cc;border-radius:9px;padding:6px 18px 12px;margin:14px 0}
.box h3{margin:10px 0 6px}.box ul{margin:6px 0;padding-left:20px}.box li{margin:5px 0}
figure{margin:10px 0 12px}figure svg{display:block;max-width:100%;height:auto;border:1px solid #c8d0dc}
figcaption{font-size:13.5px;color:#555;margin-top:4px}
.tafelblock{margin:18px 0 26px}
.tafelblock>h3{display:flex;justify-content:space-between;align-items:baseline;background:#eeeeea;border-left:5px solid #1b1b1b;padding:5px 12px;margin:0 0 10px;font-size:16.5px}
.tafelblock>h3 span{font-weight:400;font-size:13.5px;color:#555;font-style:italic}
.heft{border-left:5px solid #1b1b1b;padding-left:14px;margin:12px 0}
.uheft{border-left:5px dashed #1a56a0;padding-left:14px;margin:12px 0}
.merk{background:#eef3fb;border:1.5px solid #1a56a0;border-radius:6px;padding:8px 13px;margin:9px 0;font-weight:600}
.sprech{font-size:14.5px;color:#555;font-style:italic;margin:6px 0}
.zeige{background:#e7f3e7;border-left:4px solid #1d6b1d;padding:6px 12px;margin:0 0 10px;font-size:15px}
.heftseite{border:2px solid #1b1b1b;border-radius:4px;padding:18px 24px;margin:16px 0;background:#fff;box-shadow:4px 4px 0 #e3e3dc}
.heftseite h3{font-size:20px;margin:0 0 4px;text-decoration:underline}.heftseite p{margin:8px 0}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:15.5px}
th,td{border:1px solid #d3d3cc;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f5f5f1;font-weight:600}
.chip{display:inline-block;padding:1px 9px;border-radius:10px;font-size:12.5px;font-weight:600;white-space:nowrap}
.orange{background:#fdebd3;color:#8a4b00}.gruen{background:#dcf1dc;color:#1d6b1d}.alle{background:#e2ecf8;color:#1a56a0}
.chip.ueb{background:#e2ecf8;color:#1a56a0;border:1px dashed #1a56a0}.chip.mk{background:#eee;color:#1b1b1b;border:1px solid #1b1b1b}
.loes p{margin:5px 0}.kl{columns:2;column-gap:28px;margin:6px 0}.kl div{break-inside:avoid;margin:2px 0}
footer{margin-top:40px;padding:14px 0 40px;border-top:1px solid #d3d3cc;color:#666;font-size:13.5px}
.vt th:first-child,.vt td.mn{width:52px;text-align:right;white-space:nowrap;color:#555}
.vt tr.grp td{background:#eeeeea;font-weight:700;font-size:15.5px}
.vt tr.grp td span{float:right;font-weight:400;color:#555;font-size:14px}
.zeitleiste{display:flex;height:38px;border-radius:6px;overflow:hidden;margin:16px 0 4px;font-size:12.5px;border:1px solid #c9c9c2}
.zeitleiste div{display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.15;padding:0 3px}
.z0{background:#eeeeea}.z1{background:#e3eaf6}.z2{background:#d3dff2}.z3{background:#e3eaf6}.z4{background:#d3dff2}.z5{background:#e3eaf6}.z6{background:#eeeeea}
.baustein{margin:16px 0 22px}.bslabel{font-size:12.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#1a56a0;margin:0 0 4px}
.bsbox{background:#fff;border:1px dashed #9db4d6;border-radius:6px;padding:14px 18px}.bsbox figure{margin:0}.bsbox figure svg{border:none;width:100%}.bsbox p{margin:4px 0}.bsbox table{margin:4px 0}
.tip{background:#eef3fb;border-left:4px solid #1a56a0;padding:10px 14px;margin:14px 0;font-size:15px}
pre.prompt{white-space:pre-wrap;background:#f5f5f1;border:1px solid #d3d3cc;border-radius:6px;padding:10px 14px;font:13.5px/1.5 ui-monospace,Menlo,monospace}
@media print{nav{display:none}section{page-break-before:always}figure,.heftseite,.tafelblock{break-inside:avoid}body{font-size:11pt}}
"""

UE = '<span class="chip ueb">Übungsheft</span>'
MK = '<span class="chip mk">Merkheft</span>'
ALL = '<span class="chip alle">alle</span>'
ZUS = '<span class="chip orange">Zusatz</span>'
STIFT = "✎"


def grp(nr, titel, t0, t1):
    return f'<tr class="grp"><td colspan="4">{nr} · {titel}<span>Minute {t0}–{t1}</span></td></tr>'


def vz(m, was, buch, wer, e=False):
    return f'<tr><td class="mn">{m}′</td><td>{STIFT + " " if e else ""}{was}</td><td>{buch}</td><td>{wer}</td></tr>'


def zeitleiste(bloecke):
    tot = sum(m for m, _ in bloecke)
    z = "".join(f'<div class="z{i}" style="width:{m / tot * 100:.2f}%" title="{m} min">{n}<br>{m}′</div>'
                for i, (m, n) in enumerate(bloecke))
    return f'<div class="zeitleiste">{z}</div>'


# ================================================================== Bausteine für diese Stunde
# Physik: kein Merkheft/Übungsheft, nur EIN Heft oder Ordner. Keine Hausaufgaben.
HEFT = '<span class="chip mk">Heft</span>'


def vier_situationen():
    def r(x, y):  # Lichtstrahl ohne Marker
        return ""
    fallen = DEFS
    # Emission
    em = (f'<circle cx="80" cy="90" r="16" fill="#fff2a8" stroke="#b98900" stroke-width="2"/>'
          + "".join(f'<line x1="{80 + 22 * c:.1f}" y1="{90 + 22 * s:.1f}" x2="{80 + 40 * c:.1f}" y2="{90 + 40 * s:.1f}" '
                    f'stroke="#b98900" stroke-width="2.4"/>'
                    for c, s in [(1, 0), (.7, .7), (0, 1), (-.7, .7), (-1, 0), (-.7, -.7), (0, -1), (.7, -.7)]))
    # Streuung
    st = (f'<line x1="200" y1="125" x2="310" y2="125" stroke="{INK}" stroke-width="3"/>'
          f'{pfeil(205, 55, 250, 122)}'
          + "".join(pfeil(250, 122, x, 62) for x in (232, 262, 292)))
    # Absorption
    ab = (f'<rect x="440" y="70" width="44" height="60" fill="#3a3a3a" stroke="#111"/>'
          f'{pfeil(370, 100, 438, 100)}')
    # Transmission
    tr = (f'<rect x="590" y="65" width="26" height="70" fill="#d7ecf7" stroke="{GR}" stroke-width="2"/>'
          f'{pfeil(530, 100, 588, 100)}{pfeil(618, 100, 636, 100)}')
    lab = "".join(f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="{fw}" fill="{c}">{t}</text>'
                  for x, y, fs, fw, c, t in [
        (52, 20, 16, 700, INK, "Emission"), (55, 165, 13, 400, MUT, "Körper sendet Licht aus"),
        (200, 20, 16, 700, INK, "Streuung"), (172, 165, 13, 400, MUT, "Licht wird zurückgeworfen"),
        (356, 20, 16, 700, INK, "Absorption"), (352, 165, 13, 400, MUT, "Licht wird verschluckt"),
        (498, 20, 16, 700, INK, "Transmission"), (500, 165, 13, 400, MUT, "Licht geht hindurch")])
    return (f'<svg viewBox="0 0 680 190" xmlns="http://www.w3.org/2000/svg" width="680">{fallen}'
            f'<rect width="680" height="190" fill="#fff"/>{em}{st}{ab}{tr}{lab}</svg>')


VIER = vier_situationen()

# ================================================================== Vor der Stunde
GEMINI = ("Erstelle ein Bild mit einem Raster aus 6 Alltagsfotos (3 Spalten, 2 Zeilen, dünner weißer Rand dazwischen, "
          "keine Beschriftung, keine Wasserzeichen), realistischer Foto-Stil:\n"
          "1. Ein schwarzes T-Shirt auf einer Wäscheleine in der prallen Sonne\n"
          "2. Eine weiße Zimmerwand, von einer Lampe angestrahlt\n"
          "3. Ein sauberes Fenster mit Blick nach draußen\n"
          "4. Ein Badezimmerfenster aus Milchglas, dahinter nur Umrisse zu erkennen\n"
          "5. Eine Sonnenbrille auf einem Tisch im Sonnenlicht\n"
          "6. Ein zerknittertes Stück Alufolie, von einer Taschenlampe angestrahlt")

vorher = f"""
<section id="vorher"><h2>Vor der Stunde</h2>
<p class="lead">Klasse 7c · Doppelstunde Do 24.09.2026 (90 Minuten angenommen). Neu ist heute nur das Arbeitsblatt Lichtquellen,
danach geht es mit Leitfrage 2 weiter.</p>
<div class="tip"><b>So arbeitest du:</b> Notability mit leerer Karoseite, das MacBook mit dieser HTML daneben. Aus den Tabs „Tafelbild“ und
„Notability-Seite“ nimmst du nur, was du brauchst. Bilder: Bereich mit <b>Ctrl + Cmd + Shift + 4</b> aufnehmen (landet in der
Zwischenablage) und in Notability einfügen oder rüberziehen. Texte: markieren, kopieren. Jeder Baustein hat einen gestrichelten Rahmen, das ist die
Screenshot-Fläche. Komplette PDFs brauchst du nur für die Arbeitsblätter.</div>
<div class="box"><h3>Schon gehalten (Stand nach deiner Beschreibung)</h3>
<ul><li>Mindmap „Was ist Physik?“, naturwissenschaftliche Arbeitsweise, Fallversuch mit zwei Bällen.</li>
<li>Licht an/aus, „Wie sehen wir?“, Lichtquellen und beleuchtete Körper (Folien 1–11).</li>
<li><b>Ich nehme an:</b> Folie 12 (Antwort auf Leitfrage 1) und der Check 1 waren noch nicht dran. Falls doch, wird Block 2 kürzer.</li></ul></div>
<div class="box"><h3>Drucken und Kopieren</h3>
<ul><li><b>Arbeitsblatt Lichtquellen</b>, nur Seite 1 (Aufgaben), einmal pro Schüler.<br>
<span style="color:#555">iCloud: Physik/Physik Klasse 7/Optik 2026-27/F1 Lichtquellen (W03)/Arbeitsblatt F1.pdf</span></li>
<li><b>Versuchsblatt „Blatt, Karton, Glasscheibe“</b>, nur Seite 1, einmal pro Gruppe oder pro Schüler.<br>
<span style="color:#555">iCloud: …/F2 Licht trifft auf einen Koerper (W04)/Arbeitsblatt F2.pdf</span></li>
<li>Die Lösungsseiten bleiben bei dir (Tab „Lösungen“).</li></ul></div>
<div class="box"><h3>Digitales vorbereiten</h3>
<ul><li><b>Folien sind optional.</b> Willst du sie zeigen: <i>Optik I.pdf</i>, Seiten 10–21 (Tab „Folien“). Sonst reichen die Bausteine aus dem Tafelbild.</li></ul></div>
<div class="box"><h3>Raum und Material</h3>
<ul><li>Raum verdunkelbar.</li>
<li><b>Ray-Box(en)</b>, <b>weißes Blatt</b>, <b>schwarzer Karton</b>, <b>klare Glasscheibe</b>. Für jede Gruppe ein Set, wenn die Ray-Boxen reichen.
Sonst zeigst du den Versuch vorn und die Klasse beobachtet (Block 4 dann kürzer).</li>
<li>Optional: zerknitterte Alufolie und eine Taschenlampe für den Zusatz „Streuung an rauer Fläche“.</li></ul></div>
<div class="opt"><b>Optional: ein Gemini-Prompt für ein Alltagsbild zu Leitfrage 2 (6 Fotos in einem Bild).</b>
<pre class="prompt">{GEMINI}</pre>Die Stunde läuft auch ohne. Tab „Alltag“ hat die Beispiele als Tabelle.</div>
</section>
"""

# ================================================================== Verlauf
zeilen = "".join([
    grp(0, "Start", 0, 5),
    vz(5, "Ankommen. Rückblick in einem Satz: Wir sehen etwas, wenn Licht ins Auge fällt. Lichtquellen senden selbst Licht aus, "
          "beleuchtete Körper werfen fremdes Licht zurück. Folie 11 zur Erinnerung", "Folie 11", "Plenum"),
    grp(1, "Üben: Lichtquellen", 5, 30),
    vz(12, "Arbeitsblatt „Verschiedene Arten von Lichtquellen“: 11 Bilder benennen, L oder B umkreisen, Aufgaben 2 und 3",
       f"Arbeitsblatt {ALL}", f"Einzel<br>{HEFT}"),
    vz(5, "Kontrolle mit dem Partner, dann die Lösungsseite kurz zeigen", "Tab „Lösungen“", "Partner"),
    vz(8, "Alltagskarten: drei Beispiele von der Tabelle (z. B. Wolke, Rückstrahler, Katzenaugen). Erst überlegen, dann Handzeichen: "
          "Lichtquelle oder beleuchtet? Immer mit Begründung", "Tab „Alltag“ (Beamer)", "Partner, dann Plenum"),
    grp(2, "Sicherung: Leitfrage 1", 30, 40),
    vz(2, "Antwort auf Leitfrage 1 lesen und in eigenen Worten wiederholen lassen", "Folie 12", "Plenum"),
    vz(5, "Check zu Leitfrage 1: Handzeichen a–d, dann Lösung", "Folien 13–14", "Plenum"),
    vz(3, "Offene Fragen", "&ndash;", "Plenum"),
    grp(3, "Leitfrage 2: Einstieg", 40, 50),
    vz(4, "Folie „Beobachte“: dieselbe Lampe, drei Gegenstände (weißes Blatt, schwarzer Karton, Glasscheibe). "
          "Was passiert jeweils mit dem Licht?", "Folie 15", "Plenum"),
    vz(6, "Leitfrage 2 lesen. Vermutungen sammeln und an die Tafel schreiben, noch ohne Wertung. Material zeigen",
       "Folie 16, Material", "Plenum", True),
    grp(4, "Versuch: Blatt, Karton, Glasscheibe", 50, 75),
    vz(5, "Versuchsblatt austeilen, Versuchsbeschreibung lesen, Sicherheit (Ray-Box), Gruppen bilden", f"Versuchsblatt {ALL}", "Plenum"),
    vz(15, "Versuch durchführen. Beobachtung ins Feld auf dem Blatt schreiben. Zwei Minuten Zeit pro Material",
       "Ray-Box, Blatt, Karton, Glas", f"Gruppen<br>{HEFT}"),
    vz(5, "Beobachtungen sammeln: Tafel-Tabelle Gegenstand · Was sieht man? entsteht, Fachbegriff noch offen", "Tafelbild 2", "Plenum", True),
    grp(5, "Erarbeiten: Licht trifft auf einen Körper", 75, 85),
    vz(5, "Folie „3. Licht trifft auf einen Körper“ (leer): vier Situationen zeichnen, Fachbegriffe den Beobachtungen zuordnen",
       f"Folie 17 &rarr; Tafelbild 1", "Plenum", True),
    vz(3, "Merksatz ins Heft, Erklärung (Lückentext) auf dem Versuchsblatt ausfüllen", f"Tafelbild 1 &rarr; {HEFT}", "Einzel"),
    vz(2, "Antwort auf Leitfrage 2 lesen", "Folie 19", "Plenum"),
    grp(6, "Check", 85, 90),
    vz(5, "Check zu Leitfrage 2: Handzeichen, Lösung. Keine Hausaufgabe", "Folien 20–21", "Plenum"),
])

verlauf = f"""
<section id="verlauf"><h2>Verlauf</h2>
<p class="lead">90 Minuten. {STIFT} = wird ins {HEFT} geschrieben (Physik hat nur ein Heft oder einen Ordner). Keine Hausaufgaben.</p>
<div class="ziel"><b>Ziel:</b> Die Klasse ordnet Lichtquellen und beleuchtete Körper sicher zu. Sie beobachtet, was mit Licht an
einem weißen Blatt, einem schwarzen Karton und einer Glasscheibe passiert, und benennt Streuung, Absorption und Transmission.
<b>Nicht Ziel:</b> Spiegelung und Reflexionsgesetz (später), Farben.</div>
{zeitleiste([(5, "Start"), (25, "1 · Üben"), (10, "2 · Check 1"), (10, "3 · LF 2"), (25, "4 · Versuch"), (10, "5 · Tafel"), (5, "Check 2")])}
<table class="vt"><tr><th>Min</th><th>Was</th><th>Material</th><th>Wer</th></tr>{zeilen}</table>
<div class="knapp"><b>Wenn es knapp wird:</b> Alltagskarten auf eine Karte kürzen. Versuch als Demo vorn statt in Gruppen. Check 2 auf die
nächste Stunde schieben.</div>
<div class="fehler"><b>Worauf du achten kannst</b>
<ol>
<li>Der schwarze Karton „sieht schwarz aus“, also „wirft er schwarzes Licht zurück“. Besser: von ihm kommt (fast) kein Licht.</li>
<li>Bei der Glasscheibe wird „es geht durch“ und „es verschwindet“ verwechselt. Den Lichtfleck dahinter zeigen.</li>
<li>Streuung wird mit Spiegelung verwechselt. Das weiße Blatt wirft Licht in alle Richtungen zurück, die Spiegelung kommt später.</li>
<li>„Absorbieren“ heißt nicht „weg“: Der Karton wird dabei warm.</li>
</ol></div>
</section>
"""

# ================================================================== Folien
folien = f"""
<section id="folien"><h2>Folien</h2>
<p class="lead">Alle Folien gibt es schon in <i>Optik I.pdf</i>. Es entsteht kein neues PDF.</p>
<table><tr><th>Seite</th><th>Folie</th><th>Wann</th></tr>
<tr><td>10–11</td><td>2. Lichtquellen und beleuchtete Körper</td><td>Start, nur zur Erinnerung (Seite 11)</td></tr>
<tr><td>12</td><td>Antwort auf Leitfrage 1</td><td>Block 2</td></tr>
<tr><td>13–14</td><td>Check zu Leitfrage 1 mit Lösung (1) b, 2) c)</td><td>Block 2</td></tr>
<tr><td>15</td><td>Beobachte (Blatt, Karton, Glas)</td><td>Block 3</td></tr>
<tr><td>16</td><td>Leitfrage 2 mit Vermutungsfläche</td><td>Block 3</td></tr>
<tr><td>17–18</td><td>3. Licht trifft auf einen Körper (leer, gefüllt)</td><td>Block 5, hier entsteht das Tafelbild</td></tr>
<tr><td>19</td><td>Antwort auf Leitfrage 2</td><td>Block 5</td></tr>
<tr><td>20–21</td><td>Check zu Leitfrage 2 mit Lösung (1) a, 2) c)</td><td>Check am Ende</td></tr></table>
<div class="warn"><b>Zwei Marker passen nicht zu deinem Ablauf:</b> „AB austeilen: Lichtquellen“ steht auf Seite 13, du verteilst das Blatt aber
schon nach Seite 11. „AB austeilen: Licht trifft auf einen Körper“ steht auf Seite 20, du verteilst es vor dem Versuch (nach Seite 16).
Soll ich die beiden Marker auf Seite 11 und Seite 16 verschieben? Dann muss <i>Optik I.pdf</i> neu gebaut werden.</div>
</section>
"""

# ================================================================== Tafelbild
tafel = f"""
<section id="tafel"><h2>Tafelbild</h2>
<p class="lead">So sieht die Tafel am Ende aus. Alles ins {HEFT} (schwarzer Balken). Physik hat nur ein Heft oder einen Ordner.</p>
<div class="tafelblock"><h3>Vermutungen sammeln <span>Minute 44–50</span></h3>
<div class="zeige">Erst Folie „Leitfrage 2“ (Seite 16) zeigen.</div>
<div class="baustein"><div class="bslabel">Baustein · Überschrift und Leitfrage</div><div class="bsbox"><p><b>Leitfrage 2:</b> Was passiert mit dem Licht, wenn es auf einen Körper trifft?</p>
<p><b>Vermutungen:</b> <span style="color:#777">hier schreibst du, was die Klasse sagt (z. B. „das Licht prallt ab“, „es verschwindet“, „es geht durch“)</span></p></div></div></div>

<div class="tafelblock"><h3>Beobachtungen zum Versuch <span>Minute 70–75</span></h3>
<div class="baustein"><div class="bslabel">Baustein · Tabelle Beobachtungen</div><div class="bsbox"><table>
<tr><th>Gegenstand</th><th>Was sieht man?</th><th>Fachbegriff</th></tr>
<tr><td>weißes Blatt</td><td>heller, breiter Lichtfleck, man sieht ihn von überall</td><td>Streuung</td></tr>
<tr><td>schwarzer Karton</td><td>kein Lichtfleck, bleibt dunkel</td><td>Absorption</td></tr>
<tr><td>Glasscheibe</td><td>Licht geht (fast) ungehindert hindurch</td><td>Transmission</td></tr></table></div></div>
<p class="sprech">Die Spalte „Fachbegriff“ erst leer lassen und nach Folie 17 ausfüllen.</p></div>

<div class="tafelblock"><h3>Licht trifft auf einen Körper <span>Minute 75–80</span></h3>
<div class="zeige">Erst Folie „3. Licht trifft auf einen Körper“ (Seite 17, leer) zeigen.</div>
<div class="baustein"><div class="bslabel">Baustein · Bild: vier Situationen</div><div class="bsbox">{fig(VIER, "")}</div></div>
<div class="baustein"><div class="bslabel">Baustein · Merksatz</div><div class="bsbox"><p>Licht kann <b>ausgesendet</b> (Emission), <b>zurückgeworfen</b> (Streuung),
<b>verschluckt</b> (Absorption) oder <b>durchgelassen</b> (Transmission) werden.</p></div></div>
<p class="sprech">Vier Situationen zeichnen lassen oder als Bild rüberziehen. Danach die Beobachtungen aus der Tabelle zuordnen.</p></div>

<div class="tafelblock"><h3>Antwort auf Leitfrage 2 <span>Minute 83–85</span></h3>
<div class="baustein"><div class="bslabel">Baustein · Antworttext</div><div class="bsbox"><p>Das Licht wird zurückgeworfen (Streuung), verschluckt (Absorption) oder durchgelassen (Transmission).
Meist geschieht mehreres gleichzeitig. Sendet ein Körper selbst Licht aus, spricht man von Emission.</p></div></div></div>
</section>
"""

# ================================================================== Heftseite
heftseite = f"""
<section id="heft"><h2>Notability-Seite</h2>
<p class="lead">So soll die fertige Seite aussehen. Die Formulierungen stammen aus deinen Folien. Nimm dir daraus, was du brauchst.</p>
<div class="heftseite">
<h3>Licht trifft auf einen Körper</h3>
{fig(VIER, "")}
<p>Licht kann <b>ausgesendet</b> (Emission), <b>zurückgeworfen</b> (Streuung), <b>verschluckt</b> (Absorption) oder
<b>durchgelassen</b> (Transmission) werden. Meist geschieht mehreres gleichzeitig.</p>
<table><tr><th>weißes Blatt</th><td>Streuung</td></tr><tr><th>schwarzer Karton</th><td>Absorption</td></tr>
<tr><th>Glasscheibe</th><td>Transmission</td></tr></table>
</div></section>
"""

# ================================================================== Aufgaben
aufgaben = f"""
<section id="aufgaben"><h2>Aufgaben</h2>
<p class="lead">Alles findet im Unterricht statt, es gibt keine Hausaufgaben. {ALL} = Pflicht, {ZUS} = für Schnelle.</p>
<table><tr><th>Block</th><th>Wo</th><th>Niveau</th><th>Aufgabe</th></tr>
<tr><td>1</td><td>Arbeitsblatt Lichtquellen</td><td>{ALL}</td><td>11 Bilder: L oder B, weitere Beispiele, alt oder neu</td></tr>
<tr><td>1</td><td>Tab „Alltag“ (Teil 1)</td><td>{ALL}</td><td>Drei Alltagsbeispiele: Lichtquelle oder beleuchtet, mit Begründung</td></tr>
<tr><td>4</td><td>Versuchsblatt</td><td>{ALL}</td><td>Beobachtung zu Blatt, Karton, Glasscheibe, Erklärung als Lückentext</td></tr>
<tr><td>4</td><td>Tafel</td><td>{ALL}</td><td>Beobachtungen in die Tabelle, Fachbegriffe zuordnen</td></tr>
<tr><td>Zusatz</td><td>Z1</td><td>{ZUS}</td><td>Nenne je zwei Alltagsbeispiele für Streuung, Absorption und Transmission.</td></tr>
<tr><td>Zusatz</td><td>Z2</td><td>{ZUS}</td><td>Ein schwarzes T-Shirt wird in der Sonne heißer als ein weißes. Erkläre das mit dem Fachbegriff.</td></tr></table>
</section>
"""

# ================================================================== Alltag
def tabelle(zeilen_):
    return "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a, b, c in zeilen_)


alltag1 = [
    ("Wolke am Himmel", "beleuchtet", "Sie wirft Sonnenlicht zurück."),
    ("Mond", "beleuchtet", "Er wirft Sonnenlicht zurück."),
    ("Sterne am Nachthimmel", "Lichtquellen", "Sterne sind ferne Sonnen. Planeten wie die Venus sind beleuchtet."),
    ("Rückstrahler am Fahrrad oder Schulranzen", "beleuchtet", "Er leuchtet nur, wenn ein Scheinwerfer ihn anstrahlt."),
    ("Katzenaugen im Scheinwerferlicht", "beleuchtet", "Sie werfen das Scheinwerferlicht zurück."),
    ("Fahrrad-Rücklicht (LED)", "Lichtquelle", "Es leuchtet mit Batterie oder Dynamo."),
    ("Spiegel", "beleuchtet", "Er erzeugt kein Licht, er wirft Licht zurück."),
]
alltag2 = [
    ("Schwarzes T-Shirt in der Sonne", "Absorption", "Das Licht wird verschluckt, das Shirt erwärmt sich."),
    ("Weiße Wand", "Streuung", "Sie wirft Licht in alle Richtungen zurück, deshalb ist sie von überall zu sehen."),
    ("Fensterscheibe", "Transmission", "Der größte Teil des Lichts geht hindurch."),
    ("Milchglas (Badfenster)", "Transmission und Streuung", "Licht geht hindurch, wird aber zerstreut. Man erkennt nur Umrisse."),
    ("Sonnenbrille", "Absorption und Transmission", "Ein Teil des Lichts wird verschluckt, der Rest geht hindurch."),
    ("Solarkollektor mit dunkler Fläche", "Absorption", "Dunkle Flächen verschlucken viel Licht und werden dadurch warm."),
    ("Zerknitterte Alufolie", "Streuung", "Die raue Fläche wirft das Licht in viele Richtungen zurück."),
]

alltag = f"""
<section id="alltag"><h2>Alltag</h2>
<p class="lead">Angeregt durch LEIFIphysik (Wolke am Himmel, Nebel im Wald, Sehen im Zimmer) und dein Buch. Formulierungen sind eigene.
Für die Stunde reichen drei Zeilen aus Teil 1 und ein paar aus Teil 2.</p>
<h3>Teil 1: Lichtquelle oder beleuchtet? (Block 1)</h3>
<table><tr><th style="width:32%">Beispiel</th><th style="width:22%">Antwort</th><th>Begründung</th></tr>{tabelle(alltag1)}</table>
<h3>Teil 2: Streuung, Absorption oder Transmission? (Block 5 oder als Puffer)</h3>
<table><tr><th style="width:32%">Beispiel</th><th style="width:22%">Antwort</th><th>Begründung</th></tr>{tabelle(alltag2)}</table>
<h3>Denkfragen</h3>
<ol>
<li><b>D1</b> Im dunklen Zimmer machst du das Licht aus. Warum siehst du nichts mehr, obwohl die Möbel noch da sind?</li>
<li><b>D2</b> Warum tragen Kinder im Winter Reflexstreifen am Schulranzen?</li>
<li><b>D3</b> Warum siehst du den Strahl einer Taschenlampe im Nebel, aber nicht in klarer Luft? {ZUS}</li>
</ol></section>
"""

# ================================================================== Lösungen
loesungen = f"""
<section id="loesungen"><h2>Lösungen</h2>
<p class="lead">Selbst erstellt.</p>
<div class="loes">
<h4>Arbeitsblatt Lichtquellen, Aufgabe 1</h4>
<div class="kl"><div>Kerze: <b>L</b></div><div>Glühlampe: <b>L</b></div><div>Lagerfeuer: <b>L</b></div><div>Blitz: <b>L</b></div>
<div>Taschenlampe: <b>L</b></div><div>Sonne: <b>L</b></div><div>Mond: <b>B</b></div><div>Tafel: <b>B</b></div>
<div>Buch: <b>B</b></div><div>Zimmerpflanze: <b>B</b></div><div>Spielzeugauto: <b>B</b></div></div>
<h4>Arbeitsblatt Lichtquellen, Aufgabe 2 und 3</h4>
<p>2 a) z. B. Glühwürmchen, Polarlicht, Sterne. b) z. B. Feuerwerk, Bildschirm, Laser.<br>
3 Glühlampe und Taschenlampe (beide brauchen elektrischen Strom).</p>
<div class="warn"><b>Korrektur für Aufgabe 3:</b> Auf dem Blatt steht „erst seit etwa 200 Jahren“. Das ist zu ungenau, die Glühlampe gibt es
praktisch erst seit etwa 1880. Besser: „erst seit gut 100 Jahren“. Ich ändere das Blatt, sobald du es sagst.</div>
<h4>Check zu Leitfrage 1 und 2</h4><p>Check 1: 1) b, 2) c. Check 2: 1) a, 2) c.</p>
<h4>Versuchsblatt „Blatt, Karton, Glasscheibe“</h4>
<p><b>Beobachtung:</b> Auf dem weißen Blatt ist ein heller, breiter Lichtfleck zu sehen, das Licht wird in viele Richtungen zurückgeworfen.
Der schwarze Karton bleibt dunkel, das Licht wird verschluckt. Hinter der Glasscheibe ist der Lichtstrahl fast unverändert zu sehen.<br>
<b>Erklärung:</b> In viele Richtungen <b>gestreut</b>, größtenteils <b>absorbiert</b>, größtenteils <b>durchgelassen</b>.</p>
<h4>Zusatz</h4>
<p><b>Z1</b> Streuung: weiße Wand, Papier, Mond. Absorption: schwarze Kleidung, dunkler Asphalt, Solarkollektor. Transmission: Fensterglas, Wasser, klare Folie.<br>
<b>Z2</b> Das schwarze Shirt absorbiert mehr Licht. Die aufgenommene Energie erwärmt es. Das weiße Shirt streut mehr Licht zurück und bleibt kühler.</p>
<h4>Denkfragen</h4>
<p><b>D1</b> Ohne Lichtquelle gibt es kein Licht, das die Möbel zurückwerfen. Es gelangt kein Licht ins Auge.<br>
<b>D2</b> Die Streifen werfen das Scheinwerferlicht zurück, der Autofahrer sieht das Kind früher.<br>
<b>D3</b> Im Nebel werfen viele Wassertröpfchen das Licht in dein Auge, in klarer Luft trifft fast nichts dein Auge.</p>
</div></section>
"""

# ================================================================== Ausblick
buch = [
    ("S. 27", "Fahrrad: Vorderlicht, Rücklicht, Reflektoren als Aufgabe. Weg des Lichts beim Sehen", "Leitfrage 1, als eigene Aufgabe abgewandelt"),
    ("S. 28 A", "Sechs Fotos (Glühwürmchen, Vollmond, Radfahrer, Blitz, Freiheitsstatue, LED-Streifen) als Zuordnung", "Leitfrage 1, Folienidee"),
    ("S. 30–33", "Lichtbündel, Randstrahlen, Modell Lichtstrahl. Schülerversuche: Teelicht durch Gummischlauch, Weg des Lichts mit Alufolie und Rauch", "Leitfrage 3"),
    ("S. 34–37", "Schatten, Kern- und Halbschatten, drei Schülerversuche (C entspricht deinem Ray-Box-Versuch)", "Leitfrage 4"),
    ("S. 38–41", "Tag und Nacht, Mondphasen, Finsternisse, Modellversuche mit Globus, Lampe, Papierkugel", "Leitfrage 5"),
    ("S. 42–45", "Reflexion, Streuung, Absorption, Reflexionsgesetz. Versuche: glatte und zerknitterte Alufolie, Reflexionsgesetz mit Faden und Geodreieck", "Leitfrage 2 und 6"),
    ("S. 46–49", "Auf einen Blick und Lerncheck mit 25 Aufgaben", "Wiederholung, Klassenarbeit"),
]
buch_tab = "".join(f"<tr><td style='white-space:nowrap'>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in buch)

ausblick = f"""
<section id="ausblick"><h2>Ausblick</h2>
<p class="lead">Danach: Leitfrage 3 (Lichtausbreitung, Blende, Versuch mit Ray-Box und Blende).</p>
<h3>Was im Buch noch steckt</h3>
<p>Das Erlebnis-Physik-Buch (S. 26–49) ist deine Fundgrube, kein Schülerbuch. Ideen und Aufgaben werden abgewandelt und
in deine Folien oder Blätter gebaut. Reihenfolge im Buch weicht von deiner ab.</p>
<table><tr><th>Seite</th><th>Inhalt</th><th>Passt zu</th></tr>{buch_tab}</table>
<h3>Offen</h3>
<ul>
<li><b>Wie viele Ray-Boxen hast du?</b> Bei vier oder mehr Gruppenversuch, sonst Demo vorn.</li>
<li>Stimmt die Annahme, dass Folie 12 (Antwort Leitfrage 1) und Check 1 noch nicht dran waren?</li>
<li>Arbeitsblatt Lichtquellen, Aufgabe 3: Jahreszahl „200 Jahre“ (siehe „Lösungen“).</li>
<li>Marker „AB austeilen“ in <i>Optik I.pdf</i> passen nicht zu deinem Ablauf (siehe „Folien“).</li>
<li>Stoffverteilungsplan: Du liegst eine Woche vor dem Plan. Ich ziehe ihn auf Wunsch nach.</li>
</ul></section>
"""

html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Optik 2 – Licht trifft auf einen Körper</title><style>{CSS}</style></head><body>
<div class="wrap"><header class="kopf"><h1>Optik 2: Lichtquellen üben, Licht trifft auf einen Körper</h1>
<p class="sub">Klasse 7c · Physik · Doppelstunde Do 24.09.2026 · Leitfrage 1 Abschluss, Leitfrage 2 · alles in einer Datei</p></header></div>
<nav><div class="wrap"><a href="#vorher">Vor der Stunde</a><a href="#verlauf">Verlauf</a><a href="#folien">Folien</a>
<a href="#tafel">Tafelbild</a><a href="#heft">Notability-Seite</a><a href="#aufgaben">Aufgaben</a><a href="#alltag">Alltag</a>
<a href="#loesungen">Lösungen</a><a href="#ausblick">Ausblick</a></div></nav>
<div class="wrap">{vorher}{verlauf}{folien}{tafel}{heftseite}{aufgaben}{alltag}{loesungen}{ausblick}
<footer>Entwurf. Keine neuen PDFs vor deiner Freigabe. Generator: baue_optik2.py</footer></div></body></html>"""

ziel = Path(__file__).with_name("Optik 2 – Licht trifft auf einen Körper – ALLES.html")
ziel.write_text(html, encoding="utf-8")
print("geschrieben:", ziel, f"({len(html) // 1024} KB)")
