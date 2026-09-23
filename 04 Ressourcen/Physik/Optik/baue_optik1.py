#!/usr/bin/env python3
"""Baut 'Optik 1 – Lichtquellen und beleuchtete Körper – ALLES.html' (Klasse 7c, Physik, Doppelstunde Do 24.09.2026).

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


# ================================================================== Vor der Stunde
GEMINI = ("Erstelle ein Bild mit einem Raster aus 6 Alltagsfotos (3 Spalten, 2 Zeilen, dünner weißer Rand dazwischen, "
          "keine Beschriftung, keine Wasserzeichen), realistischer Foto-Stil, einheitliche Bildqualität:\n"
          "1. Eine Wolke am Abendhimmel, von der tief stehenden Sonne angestrahlt\n"
          "2. Ein Sternenhimmel mit Halbmond über einer dunklen Landschaft\n"
          "3. Ein Kind mit Schulranzen mit Reflexstreifen im Scheinwerferlicht eines Autos am Straßenrand, dunkle Straße\n"
          "4. Die Augen einer Katze, die im Scheinwerferlicht nachts hell aufleuchten\n"
          "5. Ein Autoscheinwerfer im Nebel, der Lichtstrahl ist von der Seite gut sichtbar\n"
          "6. Ein dunkles Kinderzimmer mit eingeschalteter Schreibtischlampe, die Möbel sind schwach beleuchtet")

vorher = f"""
<section id="vorher"><h2>Vor der Stunde</h2>
<p class="lead">Klasse 7c · Doppelstunde Do 24.09.2026 (90 Minuten angenommen) · zweiter Teil von Leitfrage 1.</p>
<div class="box"><h3>Rückblick auf letzte Woche</h3>
<ul><li>Mindmap „Was ist Physik?“, naturwissenschaftliche Arbeitsweise, Fallversuch mit zwei Bällen (beide gleich schnell).</li>
<li>Optik gestartet: Licht an/aus, „Wie sehen wir?“ ausgefüllt (Licht von einem Gegenstand muss ins Auge gelangen,
Lichtquelle = Sender, Auge = Empfänger).</li>
<li><b>Heute:</b> Folie 2 „Lichtquellen und beleuchtete Körper“, Arbeitsblatt, Alltagsbeispiele, Check zu Leitfrage 1.
Am Ende der Blick auf Leitfrage 2.</li></ul></div>
<div class="box"><h3>Drucken und Kopieren</h3>
<ul><li><b>Arbeitsblatt Lichtquellen</b>, nur die Aufgabenseite (Seite 1), einmal pro Schüler. Die Lösungsseite bleibt bei dir.
<br><span style="color:#555">iCloud: Physik/Physik Klasse 7/Optik 2026-27/F1 Lichtquellen (W03)/Arbeitsblatt F1.pdf</span></li>
<li>Alltagsbeispiele werden nicht kopiert, sie laufen über Beamer/Tafel (Tab „Alltag“).</li></ul></div>
<div class="box"><h3>Digitales vorbereiten</h3>
<ul><li><b>Folien</b> nach Notability: <i>Optik I.pdf</i>, Seiten 8–16 (Tab „Folien“). Alternativ Folien F1.pdf Seiten 8–14 und Folien F2.pdf Seiten 1–2.</li>
<li>Optional: Bild „Alltag“ als Folie (Prompt unten). Ohne Bild geht die Stunde genauso, die Tabelle im Tab „Alltag“ reicht.</li></ul></div>
<div class="box"><h3>Raum und Material</h3>
<ul><li>Raum verdunkelbar. Für den Einstieg: <b>Glühlampe mit Fassung</b> (an der Wand oder Tisch vorn), <b>Taschenlampe</b>.</li>
<li>Bereit legen: <b>Spiegel</b> (Kontrollfrage „Ist ein Spiegel eine Lichtquelle?“), ein Heft oder Buch zum Anleuchten.</li>
<li>Erlebnis Physik 7–9: Buchseiten 26–29 (Sehen, Lichtquellen). <b>Nur nötig, wenn die Klasse das Buch hat</b> (siehe „Offen“).</li></ul></div>
<div class="opt"><b>Optional: ein Gemini-Prompt für ein Alltagsbild (6 Fotos in einem Bild).</b>
<pre class="prompt">{GEMINI}</pre>
Bild danach in <code>07 Anhänge/</code> ablegen, dann baue ich es als Folie ein.</div>
</section>
"""

# ================================================================== Verlauf
zeilen = "".join([
    grp(0, "Start", 0, 5),
    vz(5, "Ankommen. Zwei Fragen mündlich: „Wann sehen wir einen Gegenstand?“ (wenn Licht von ihm ins Auge fällt) und "
          "„Was ist Sender, was Empfänger?“. Auf Wunsch 30 Sekunden Geschichte: Manche Griechen glaubten, das Auge "
          "sende Sehstrahlen aus", "Folien 8–9 (Wiederholung)", "Plenum"),
    grp(1, "Einstieg: Dunkelraum-Demo", 5, 15),
    vz(4, "Raum verdunkeln, nur die Glühlampe vorn an. Dann Taschenlampe: erst an die Wand, dann auf ein Heft und auf "
          "eine Schülerhand. Was seht ihr, wenn ich das Heft anleuchte?", "Glühlampe + Fassung, Taschenlampe", "Plenum"),
    vz(6, "Sammeln: Was leuchtet selbst (Lampe, Taschenlampe), was wird nur angeleuchtet (Heft, Hand, Wand)? "
          "Kennt jemand Namen dafür? Vermutungen an die Tafel, noch ohne Wertung", "Tafel", "Plenum"),
    grp(2, "Erarbeiten: Lichtquellen und beleuchtete Körper", 15, 35),
    vz(5, "Folie „2. Lichtquellen und beleuchtete Körper“ (leer). Tafelbild entsteht: links Sonne, Kerze, Glühlampe, "
          "rechts Mond, Buch, Baum. Schüler zeichnen mit", "Folie 10 &rarr; Tafelbild 1", "Plenum", True),
    vz(5, "Merksatz mit Überschrift ins Merkheft", f"Tafelbild 1 &rarr; {MK}", "Plenum, abschreiben", True),
    vz(5, "Lesen: Buchtext „Selbstleuchtende Körper / Beleuchtete Körper“ und den gelben Merkkasten. Auftrag: zwei "
          "Beispiele unterstreichen, die noch nicht an der Tafel stehen", "Buch S. 27", "Einzel"),
    vz(5, "Ergänzen: natürliche und künstliche Lichtquellen. Sonderfall Mond: „Der Mond leuchtet doch nachts?“ "
          "(er wirft Sonnenlicht zurück)", f"Tafelbild 2 &rarr; {MK}", "Plenum", True),
    grp(3, "Üben und Alltag", 35, 65),
    vz(10, "Arbeitsblatt „Verschiedene Arten von Lichtquellen“: 11 Bilder benennen, L oder B umkreisen, Aufgaben 2 und 3",
       f"Arbeitsblatt {ALL}", f"Einzel<br>{UE}"),
    vz(5, "Kontrolle mit dem Partner, dann Lösungsseite kurz an der Wand zeigen (Bilder mit L/B)", "Tab „Lösungen“", "Partner"),
    vz(10, "Alltagsbeispiele: fünf Karten von der Tabelle (Wolke, Sterne, Rückstrahler, Katzenaugen, Nebel). "
           "Erst zu zweit überlegen, dann Handzeichen: Lichtquelle oder beleuchtet? Immer mit Begründung",
       "Tab „Alltag“ (Beamer)", "Partner, dann Plenum"),
    vz(5, "Zwei Denkfragen: „Warum siehst du im dunklen Zimmer nichts?“ und „Warum tragen Kinder Reflexstreifen?“",
       "Tab „Alltag“ D1, D4", "Plenum"),
    grp(4, "Sicherung", 65, 75),
    vz(2, "Antwort auf Leitfrage 1 lesen lassen und zusammenfassen", "Folie 12", "Plenum"),
    vz(5, "Check zu Leitfrage 1: Handzeichen a–d, dann Lösung", "Folien 13–14", "Plenum"),
    vz(3, "Offene Fragen, Merkheft kurz vergleichen", "&ndash;", "Plenum"),
    grp(5, "Ausblick auf Leitfrage 2", 75, 85),
    vz(5, "Folie „Beobachte“: Licht trifft auf ein weißes Blatt, einen schwarzen Karton, eine Glasscheibe. "
          "Was fällt euch auf?", "Folie 15", "Plenum"),
    vz(3, "Leitfrage 2: Vermutungen sammeln, noch nicht auflösen", "Folie 16", "Plenum", True),
    vz(2, "Hausaufgabe ansagen", f"S. 27 Nr. 2 und Nr. 3 {UE}", "Zu Hause"),
    grp(6, "Puffer", 85, 90),
    vz(5, "Merkheft vollständig? Aufräumen. Reserve für alles, was länger gedauert hat", "&ndash;", "alle"),
])

verlauf = f"""
<section id="verlauf"><h2>Verlauf</h2>
<p class="lead">90 Minuten. {STIFT} = wird ins {MK} geschrieben. Alle Übungen kommen ins {UE}.</p>
<div class="ziel"><b>Ziel:</b> Die Klasse unterscheidet selbstleuchtende Körper (Lichtquellen) und beleuchtete Körper, nennt
natürliche und künstliche Lichtquellen und begründet die Zuordnung an Alltagsbeispielen. <b>Nicht Ziel:</b> Reflexion und
Streuung genauer erklären, das folgt in Leitfrage 2 und später.</div>
{zeitleiste([(5, "Start"), (10, "1 · Einstieg"), (20, "2 · Erarbeiten"), (30, "3 · Üben + Alltag"), (10, "4 · Check"),
            (10, "5 · LF 2"), (5, "Puffer")])}
<table class="vt"><tr><th>Min</th><th>Was</th><th>Buch und Material</th><th>Wer</th></tr>{zeilen}</table>
<div class="knapp"><b>Wenn es knapp wird:</b> Buchtext (Minute 25–30) streichen, Alltagsbeispiele auf drei Karten kürzen,
Ausblick auf Leitfrage 2 auf die nächste Stunde schieben.</div>
<div class="fehler"><b>Worauf du achten kannst</b>
<ol>
<li>Der <b>Mond</b> wird für eine Lichtquelle gehalten, weil er hell aussieht.</li>
<li><b>Hell</b> wird mit <b>selbstleuchtend</b> verwechselt: ein weißes Blatt oder ein Spiegel wirkt hell, erzeugt aber kein Licht.</li>
<li><b>Rückstrahler</b> und <b>Katzenaugen</b> „leuchten“ nur, wenn sie angestrahlt werden. Das Wort „leuchten“ ruhig hinterfragen.</li>
<li>Manche Kinder denken noch, das Auge sende etwas aus. Kurz zurückführen auf „Licht muss ins Auge gelangen“.</li>
</ol></div>
</section>
"""

# ================================================================== Folien
folien = f"""
<section id="folien"><h2>Folien</h2>
<p class="lead">Alle Folien gibt es schon in <i>Optik I.pdf</i> (Seitenzahlen unten). In den Ordnern F1 und F2 liegen dieselben Seiten als Auszug. Es entsteht kein neues PDF.</p>
<table><tr><th>Seite</th><th>Folie</th><th>Wann</th></tr>
<tr><td>8–9</td><td>1. Wie sehen wir? (leer, gefüllt)</td><td>Start, nur zum Zeigen</td></tr>
<tr><td>10</td><td>2. Lichtquellen und beleuchtete Körper (Zeichenfläche leer)</td><td>Erarbeiten, hier entsteht das Tafelbild</td></tr>
<tr><td>11</td><td>2. Lichtquellen und beleuchtete Körper (gefüllt)</td><td>Zur Kontrolle nach dem Zeichnen</td></tr>
<tr><td>12</td><td>Antwort auf Leitfrage 1</td><td>Sicherung</td></tr>
<tr><td>13</td><td>Check zu Leitfrage 1 (Marker: Arbeitsblatt austeilen)</td><td>Sicherung. Das Blatt ist schon verteilt.</td></tr>
<tr><td>14</td><td>Lösung Check: 1) b, 2) c</td><td>Nach dem Handzeichen</td></tr>
<tr><td>15</td><td>Beobachte (Licht auf Blatt, Karton, Glas)</td><td>Ausblick Leitfrage 2</td></tr>
<tr><td>16</td><td>Leitfrage 2 mit Vermutungsfläche</td><td>Ausblick, Vermutungen sammeln</td></tr></table>
<div class="warn"><b>Hinweis:</b> Der Marker „AB austeilen“ steht auf Seite 13, du willst das Blatt aber schon im Block 3
verteilen. Wenn dich das stört, sage Bescheid, dann verschiebe ich den Marker auf Seite 11.</div>
</section>
"""

# ================================================================== Tafelbild
tafel = f"""
<section id="tafel"><h2>Tafelbild</h2>
<p class="lead">So sieht die Tafel am Ende aus. Schwarzer Balken = {MK}, gestrichelt blau = {UE}.</p>
<div class="tafelblock"><h3>Lichtquellen und beleuchtete Körper <span>Minute 15–25</span></h3>
<div class="zeige">Erst Folie „2. Lichtquellen und beleuchtete Körper“ (Seite 10, leer) zeigen.</div>
<div class="heft">
{fig(TAFEL1, "Zwei Spalten. Sonne, Kerze, Glühlampe zuerst zeichnen lassen, dann Mond, Buch, Baum.")}
<div class="merk"><b>Lichtquellen</b> senden selbst Licht aus (Selbstleuchter).<br>
<b>Beleuchtete Körper</b> senden nur Licht aus, das sie von einer Lichtquelle bekommen haben.</div></div>
<p class="sprech">Frage vor dem Zeichnen an die Klasse: „Was gehört links, was rechts?“ Den Mond bewusst rechts
stehen lassen und begründen lassen.</p></div>

<div class="tafelblock"><h3>Natürlich und künstlich <span>Minute 30–35</span></h3>
<div class="heft"><table>
<tr><th style="width:170px">natürliche Lichtquellen</th><td>Sonne, Sterne, Blitz, Glühwürmchen</td></tr>
<tr><th>künstliche Lichtquellen</th><td>Glühlampe, LED, Kerze, Bildschirm</td></tr></table>
<div class="merk">Natürliche Lichtquellen gibt es in der Natur. Künstliche Lichtquellen hat der Mensch gebaut.</div></div></div>

<div class="tafelblock"><h3>Weg des Lichts <span>zur Wiederholung, Minute 65–70</span></h3>
<div class="heft">
{fig(TAFEL_WEG, "Nur zeigen, wenn die Klasse den Weg noch nicht sicher beschreiben kann. Passt zur Hausaufgabe Nr. 3.")}
</div></div>

<div class="tafelblock"><h3>Arbeitsblatt und Alltag <span>Minute 35–65</span></h3>
<div class="uheft"><p>Das Arbeitsblatt wird eingeklebt und dort gelöst. Die Alltagsbeispiele mündlich, nur die Begründung von
einem Beispiel in einem Satz ins Übungsheft.</p></div></div>
</section>
"""

# ================================================================== Merkheft
merkheft = f"""
<section id="merkheft"><h2>Merkheft</h2>
<p class="lead">Das schreiben die Schüler ab. Die Formulierung des Merksatzes stammt aus deiner Folie.</p>
<div class="heftseite">
<h3>Lichtquellen und beleuchtete Körper</h3>
{fig(TAFEL1, "")}
<p><b>Lichtquellen</b> senden selbst Licht aus (Selbstleuchter).<br>
<b>Beleuchtete Körper</b> senden nur Licht aus, das sie von einer Lichtquelle bekommen haben.</p>
<p><b>Natürliche Lichtquellen:</b> Sonne, Sterne, Blitz, Glühwürmchen<br>
<b>Künstliche Lichtquellen:</b> Glühlampe, LED, Kerze, Bildschirm</p>
</div></section>
"""

# ================================================================== Aufgaben
aufgaben = f"""
<section id="aufgaben"><h2>Aufgaben</h2>
<p class="lead">{ALL} = Pflicht, {ZUS} = für Schnelle oder zu Hause. Buchseiten aus Erlebnis Physik 7–9.</p>
<table><tr><th>Wann</th><th>Wo</th><th>Niveau</th><th>Aufgabe</th></tr>
<tr><td>Block 3</td><td>Arbeitsblatt</td><td>{ALL}</td><td>11 Bilder: Lichtquelle (L) oder beleuchteter Körper (B), weitere Beispiele, alt oder neu</td></tr>
<tr><td>Block 3</td><td>Tab „Alltag“</td><td>{ALL}</td><td>Fünf Alltagsbeispiele mit Begründung</td></tr>
<tr><td>HA</td><td>Buch S. 27 Nr. 2</td><td>{ALL}</td><td>Fahrrad: Vorderlicht, Rücklicht, Reflektoren den Körperarten zuordnen</td></tr>
<tr><td>HA</td><td>Buch S. 27 Nr. 3</td><td>{ALL}</td><td>Weg des Lichts beschreiben, um einen beleuchteten Körper zu sehen (mit Fachbegriffen)</td></tr>
<tr><td>Zusatz</td><td>Buch S. 28 A Nr. 1, 2</td><td>{ZUS}</td><td>Sechs Bilder in Tabelle einordnen, weitere Beispiele ergänzen</td></tr>
<tr><td>Zusatz</td><td>Buch S. 27 Nr. 1</td><td>{ZUS}</td><td>Ampel: Sender und Empfänger, Bedeutung der drei Farben</td></tr>
<tr><td>Zusatz</td><td>Buch S. 29 Nr. 1–4</td><td>{ZUS}</td><td>Sender und Empfänger im Alltag (Fernbedienung, Blaulicht, Feueralarm)</td></tr></table>
<p class="sprech">Nichts weiter zu drucken als das Arbeitsblatt. Das Buch nur, wenn die Klasse es hat.</p>
</section>
"""

# ================================================================== Alltag
alltag_zeilen = [
    ("Wolke am Himmel", "beleuchtet", "Sie wirft Sonnenlicht zurück. Ohne Sonne wäre sie dunkel."),
    ("Sonne", "Lichtquelle (natürlich)", "Sie erzeugt selbst Licht."),
    ("Mond", "beleuchtet", "Er wirft Sonnenlicht zurück. Buch S. 27."),
    ("Sterne am Nachthimmel", "Lichtquellen (natürlich)", "Sterne sind ferne Sonnen. Planeten (z. B. Venus) sind dagegen beleuchtet."),
    ("Smartphone-Display, eingeschaltet", "Lichtquelle (künstlich)", "Es erzeugt selbst Licht. Ausgeschaltet ist es dunkel."),
    ("Fahrrad-Rücklicht (LED)", "Lichtquelle (künstlich)", "Es leuchtet mit Batterie oder Dynamo."),
    ("Rückstrahler am Fahrrad oder Schulranzen", "beleuchtet", "Er leuchtet nur, wenn ein Scheinwerfer ihn anstrahlt. Buch S. 27 Nr. 2."),
    ("Katzenaugen im Scheinwerferlicht", "beleuchtet", "Sie leuchten nicht selbst, sie werfen das Scheinwerferlicht zurück."),
    ("Glühwürmchen", "Lichtquelle (natürlich)", "Das Tier erzeugt selbst Licht. Buch S. 28 Bild A."),
    ("Freiheitsstatue, nachts von Scheinwerfern angestrahlt", "beleuchtet", "Die Scheinwerfer sind die Lichtquellen. Buch S. 28 Bild E."),
    ("Möbel im Zimmer, Deckenlampe an", "beleuchtet", "Die Lampe ist die Lichtquelle, die Möbel werfen ihr Licht zurück."),
    ("Spiegel", "beleuchtet", "Er erzeugt kein Licht, er wirft Licht zurück (Check 2, Antwort b ist falsch)."),
    ("Autoscheinwerfer im Nebel: der Strahl ist von der Seite zu sehen", "die Nebeltröpfchen sind beleuchtet",
     "Winzige Wassertröpfchen werfen Licht in dein Auge. In klarer Luft siehst du den Strahl kaum. Vorgriff auf Leitfrage 3, freiwillig."),
]
alltag_tab = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a, b, c in alltag_zeilen)

alltag = f"""
<section id="alltag"><h2>Alltag</h2>
<p class="lead">Mehr Alltagsbezug, angeregt durch die Aufgabenpools bei LEIFIphysik (Wolke am Himmel, Nebel im Wald,
Sehen im Zimmer, Sternenhimmel) und das Schulbuch. Formulierungen sind eigene. Für die Stunde reichen fünf Zeilen.</p>
<table><tr><th style="width:32%">Beispiel</th><th style="width:24%">Lichtquelle oder beleuchtet?</th><th>Begründung</th></tr>{alltag_tab}</table>
<h3>Denkfragen</h3>
<ol>
<li><b>D1</b> Im dunklen Zimmer machst du das Licht aus. Warum siehst du plötzlich nichts mehr, obwohl alle Möbel noch da sind?</li>
<li><b>D2</b> Ein Radfahrer trägt eine Stirnlampe und eine Warnweste. Was davon ist Lichtquelle, was beleuchteter Körper?</li>
<li><b>D3</b> Warum siehst du den Lichtstrahl einer Taschenlampe im Nebel, aber nicht in klarer Luft? {ZUS}</li>
<li><b>D4</b> Warum tragen Kinder im Winter Reflexstreifen am Schulranzen? Buch S. 44 B. {ZUS}</li>
<li><b>D5</b> Kann ein Körper gleichzeitig Lichtquelle und beleuchteter Körper sein? Beispiel? {ZUS}</li>
</ol>
</section>
"""

# ================================================================== Lösungen
loesungen = f"""
<section id="loesungen"><h2>Lösungen</h2>
<p class="lead">Selbst erstellt, nicht mit einem Lösungsbuch abgeglichen. Die Buchaufgaben sind nach den Fotos gelesen.</p>
<div class="loes">
<h4>Arbeitsblatt, Aufgabe 1</h4>
<div class="kl"><div>Kerze: <b>L</b></div><div>Glühlampe: <b>L</b></div><div>Lagerfeuer: <b>L</b></div><div>Blitz: <b>L</b></div>
<div>Taschenlampe: <b>L</b></div><div>Sonne: <b>L</b></div><div>Mond: <b>B</b></div><div>Tafel: <b>B</b></div>
<div>Buch: <b>B</b></div><div>Zimmerpflanze: <b>B</b></div><div>Spielzeugauto: <b>B</b></div></div>
<h4>Arbeitsblatt, Aufgabe 2 und 3</h4>
<p>2 a) z. B. Glühwürmchen, Polarlicht, Sterne. b) z. B. Feuerwerk, Bildschirm, Laser.<br>
3 Glühlampe und Taschenlampe (beide brauchen elektrischen Strom).</p>
<div class="warn"><b>Korrektur für Aufgabe 3:</b> Auf dem Blatt steht „erst seit etwa 200 Jahren“. Das ist zu ungenau, die
Glühlampe gibt es praktisch erst seit etwa 1880. Besser: „erst seit gut 100 Jahren“. Ich ändere das Blatt, sobald du es sagst.</div>
<h4>Check zu Leitfrage 1</h4><p>1) b &nbsp; 2) c</p>
<h4>Buch S. 27 Nr. 1 (Ampel)</h4>
<p>a) Sender: die Ampel. Empfänger: die Autofahrer (ihre Augen).<br>
b) Rot: anhalten. Gelb: Achtung, die Ampel schaltet gleich um (auf Rot). Grün: fahren.</p>
<h4>Buch S. 27 Nr. 2 (Fahrrad)</h4>
<p>Selbstleuchtend: Vorderlicht und Rücklicht. Beleuchtet: die Reflektoren, sie leuchten nur, wenn ein Scheinwerfer sie anstrahlt.</p>
<h4>Buch S. 27 Nr. 3 (Weg des Lichts)</h4>
<p>Die Lichtquelle (Sender) sendet Licht aus. Es trifft auf den beleuchteten Körper. Der Körper wirft einen Teil des Lichts
zurück. Dieses Licht gelangt in das Auge (Empfänger), und wir sehen den Körper.</p>
<h4>Buch S. 28 A Nr. 1 und 2</h4>
<p>Nach den Bildunterschriften: Glühwürmchen, Gewitterblitz und LED-Streifen sind Lichtquellen. Vollmond, Radfahrer mit
Warnwesten und Freiheitsstatue sind beleuchtete Körper. Nr. 2: freie Beispiele, z. B. Kerze, Sonne, Buch, Baum.</p>
<h4>Denkfragen</h4>
<p><b>D1</b> Ohne Lichtquelle gibt es kein Licht, das die Möbel zurückwerfen könnten. Es gelangt kein Licht ins Auge.<br>
<b>D2</b> Stirnlampe: Lichtquelle. Warnweste und Radfahrer: beleuchtet.<br>
<b>D3</b> Im Nebel werfen die vielen Wassertröpfchen das Licht in dein Auge, in klarer Luft trifft fast nichts dein Auge.<br>
<b>D4</b> Die Streifen werfen das Scheinwerferlicht zurück, der Autofahrer sieht das Kind früher.<br>
<b>D5</b> Ja, z. B. ein Mensch mit eingeschalteter Stirnlampe: Die Lampe erzeugt Licht, der Mensch wirft fremdes Licht zurück.</p>
</div></section>
"""

# ================================================================== Ausblick
buch = [
    ("S. 29 Im Alltag", "Sender-Empfänger: Fernbedienung (Infrarot), Leuchtturm und Seezeichen", "Zusatz zu Leitfrage 1"),
    ("S. 30–31", "Licht breitet sich geradlinig aus, Lichtbündel, Randstrahlen, Modell Lichtstrahl", "Leitfrage 3"),
    ("S. 32", "Methode „Modelle bewerten“: Vor- und Nachteile des Modells Lichtstrahl", "Leitfrage 3 (Modell)"),
    ("S. 33 A, B", "Schülerversuche: Teelicht durch Gummischlauch sehen, Weg des Lichts mit Alufolie und Rauch", "Leitfrage 3, sehr einfach"),
    ("S. 34–35", "Licht und Schatten, Schattenraum und Schattenbild, Kern- und Halbschatten mit zwei Lampen", "Leitfrage 4"),
    ("S. 36 A, S. 37 B, C", "Schülerversuche: Schattenbild, Überlagerung, Halbschatten und Kernschatten (C ist dein Ray-Box-Versuch)", "Leitfrage 4"),
    ("S. 38–39, 40", "Tag und Nacht, Mondphasen, Modellversuche mit Globus, Lampe, Papierkugel", "Leitfrage 5"),
    ("S. 41", "Mond- und Sonnenfinsternis mit Positionsbildern", "Leitfrage 5"),
    ("S. 42–43", "Reflexion, Streuung, Absorption, Reflexionsgesetz", "Leitfrage 2 und 6"),
    ("S. 45 A, B", "Schülerversuche: glatte und zerknitterte Alufolie, Reflexionsgesetz mit Faden und Geodreieck", "Leitfrage 2 und 6"),
    ("S. 46–49", "Auf einen Blick, Lerncheck mit 25 Aufgaben", "Wiederholung und Klassenarbeit"),
]
buch_tab = "".join(f"<tr><td style='white-space:nowrap'>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in buch)

ausblick = f"""
<section id="ausblick"><h2>Ausblick</h2>
<p class="lead">Nach dieser Stunde: Leitfrage 2 (Licht trifft auf einen Körper), dann Leitfrage 3 (Lichtausbreitung).</p>
<h3>Was im Buch noch steckt (Erlebnis Physik 7–9)</h3>
<p>Die Buchreihenfolge ist anders als deine (Reflexion steht erst hinten). Als Fundgrube passt es trotzdem gut:</p>
<table><tr><th>Seite</th><th>Inhalt</th><th>Passt zu</th></tr>{buch_tab}</table>
<h3>Offen</h3>
<ul>
<li><b>Hat die Klasse das Buch?</b> Wenn nicht, streiche die Buch-Hausaufgabe und nimm Nr. 2/3 als Kopie oder von der Tafel.</li>
<li>Lösungen sind nicht mit einem Lösungsbuch abgeglichen, nur nach den Fotos gelesen.</li>
<li>Arbeitsblatt Aufgabe 3 hat die Jahreszahl „200 Jahre“ (siehe Tab „Lösungen“).</li>
<li>Stoffverteilungsplan: Du bist eine Woche vor dem Plan (Einstieg statt „Messen“ in Woche 2). Wenn du willst, ziehe ich den Plan nach.</li>
<li>90 Minuten sind angenommen. Sag Bescheid, falls es eine Einzelstunde ist, dann streiche ich Alltag und Ausblick.</li>
</ul></section>
"""

html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Optik 1 – Lichtquellen und beleuchtete Körper</title><style>{CSS}</style></head><body>
<div class="wrap"><header class="kopf"><h1>Optik 1: Lichtquellen und beleuchtete Körper</h1>
<p class="sub">Klasse 7c · Physik · Doppelstunde Do 24.09.2026 · Leitfrage 1 · alles in einer Datei</p></header></div>
<nav><div class="wrap"><a href="#vorher">Vor der Stunde</a><a href="#verlauf">Verlauf</a><a href="#folien">Folien</a>
<a href="#tafel">Tafelbild</a><a href="#merkheft">Merkheft</a><a href="#aufgaben">Aufgaben</a><a href="#alltag">Alltag</a>
<a href="#loesungen">Lösungen</a><a href="#ausblick">Ausblick</a></div></nav>
<div class="wrap">{vorher}{verlauf}{folien}{tafel}{merkheft}{aufgaben}{alltag}{loesungen}{ausblick}
<footer>Entwurf. Keine neuen PDFs vor deiner Freigabe. Generator: baue_optik1.py</footer></div></body></html>"""

ziel = Path(__file__).with_name("Optik 1 – Lichtquellen und beleuchtete Körper – ALLES.html")
ziel.write_text(html, encoding="utf-8")
print("geschrieben:", ziel, f"({len(html) // 1024} KB)")
