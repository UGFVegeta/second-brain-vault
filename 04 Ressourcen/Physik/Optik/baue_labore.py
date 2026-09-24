#!/usr/bin/env python3
"""Baut die Optik-Labore (Stil wie 'Schattenlabor Halbschatten.html') als eigenständige HTML-Dateien.
Schriften sind eingebettet (keine Google-Anfragen), jede Datei läuft offline und kann per Link/Moodle an Schüler gehen.
Aufruf: python3 baue_labore.py"""
import base64, re
from pathlib import Path

HIER = Path(__file__).parent
Q = HIER / "labore-quelle"
FONTS = HIER / "assets" / "fonts"


def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


FONT_CSS = (
    "@font-face{font-family:'Bricolage Grotesque';font-style:normal;font-weight:500 700;font-display:swap;"
    f"src:url(data:font/woff2;base64,{b64('brico.woff2')}) format('woff2')}}"
    "@font-face{font-family:'Source Sans 3';font-style:normal;font-weight:400 600;font-display:swap;"
    f"src:url(data:font/woff2;base64,{b64('sans.woff2')}) format('woff2')}}"
    "@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;"
    f"src:url(data:font/woff2;base64,{b64('mono400.woff2')}) format('woff2')}}"
    "@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:500;font-display:swap;"
    f"src:url(data:font/woff2;base64,{b64('mono500.woff2')}) format('woff2')}}\n")

FONT_LINKS = re.compile(r'<link rel="preconnect"[^>]*>\s*<link rel="preconnect"[^>]*>\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\s*')

SCHATTEN = HIER / "Schattenlabor Halbschatten.html"
_src = SCHATTEN.read_text(encoding="utf-8")
BASIS_CSS = _src[_src.index("<style>") + 7:_src.index("</style>")].replace(FONT_CSS, "")
EXTRA_CSS = (".sortgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}"
             ".opts.two{grid-template-columns:1fr 1fr}.copy .q p.qt{font-weight:600}")

HELFER, RAHMEN = (Q / "shell.js").read_text(encoding="utf-8").split("</script>\n<script>")


def seite(titel, brand, lab_js):
    n = len(re.findall(r'\{kicker:', lab_js))
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titel}</title>
<style>
{FONT_CSS}{BASIS_CSS}{EXTRA_CSS}
</style>
</head>
<body>
<div class="app" id="app">
  <div class="bar">
    <span class="brand">{brand}</span>
    <div class="tools">
      <span class="brand" id="counter">1 / {n}</span>
      <button class="btn" id="btnNotes" type="button" aria-pressed="false">Lehrkraft</button>
      <button class="btn" id="btnFs" type="button">Vollbild</button>
    </div>
  </div>
  <div class="progress" aria-hidden="true"><i id="bar"></i></div>
  <div class="main" id="main">
    <section class="copy" id="copy" aria-live="polite"></section>
    <section class="stagewrap" id="stagewrap">
      <div class="stage"><svg id="svg" viewBox="0 0 840 440" role="img" aria-label="Zeichnung"></svg></div>
      <div class="readout" id="readout"></div>
      <div id="ctrl"></div>
    </section>
  </div>
  <div class="foot">
    <button class="btn" id="prev" type="button">← Zurück</button>
    <div class="dots" id="dots"></div>
    <button class="btn primary" id="next" type="button">Weiter →</button>
  </div>
</div>
<script>{HELFER}</script>
<script>{lab_js}</script>
<script>{RAHMEN}</script>
</body>
</html>
"""


LABORE = [
    ("Sehlabor Lichtquellen.html", "Sehlabor", "Physik · Optik · Klasse 7 · Leitfrage 1", "sehlabor.js"),
    ("Körperlabor Licht trifft auf Körper.html", "Körperlabor", "Physik · Optik · Klasse 7 · Leitfrage 2", "koerperlabor.js"),
    ("Strahlenlabor Lichtausbreitung.html", "Strahlenlabor", "Physik · Optik · Klasse 7 · Leitfrage 3", "strahlenlabor.js"),
]

for datei, titel, brand, js in LABORE:
    html = seite(titel, brand, (Q / js).read_text(encoding="utf-8"))
    (HIER / datei).write_text(html, encoding="utf-8")
    print("geschrieben:", datei, f"({len(html) // 1024} KB)")

# Schattenlabor: Schriften einbetten statt von Google laden
if FONT_LINKS.search(_src):
    neu = FONT_LINKS.sub("", _src).replace("<style>", "<style>\n" + FONT_CSS, 1)
    SCHATTEN.write_text(neu, encoding="utf-8")
    print("Schattenlabor: Schriften eingebettet")

# Startseite mit allen Laboren (ein Link für die Schüler)
KARTEN = [
    ("Leitfrage 1", "Sehlabor", "Warum sehen wir überhaupt etwas? Sender, Empfänger, Lichtquellen und beleuchtete Körper.", "Sehlabor Lichtquellen.html"),
    ("Leitfrage 2", "Körperlabor", "Was passiert mit dem Licht, wenn es auf einen Körper trifft? Streuung, Absorption, Transmission.", "Körperlabor Licht trifft auf Körper.html"),
    ("Leitfrage 3", "Strahlenlabor", "Warum können wir nicht um die Ecke sehen? Blenden, Lichtbündel und das Lichtstrahlenmodell.", "Strahlenlabor Lichtausbreitung.html"),
    ("Leitfrage 4", "Schattenlabor", "Warum hat ein Schatten manchmal weiche Ränder? Kernschatten und Halbschatten.", "Schattenlabor Halbschatten.html"),
]
karten = "".join(
    f'<a class="karte" href="{href}"><span class="kicker">{k}</span><h2>{t}</h2><p>{d}</p><span class="los">Öffnen →</span></a>'
    for k, t, d, href in KARTEN)
start = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Optik-Labore</title>
<style>
{FONT_CSS}{BASIS_CSS}
.wrap{{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:18px}}
.wrap h1{{font-family:var(--font-d);font-weight:700;font-size:clamp(2rem,4.5vw,3.3rem);line-height:1.05;margin:4px 0 0}}
.wrap>p{{font-size:1.15rem;line-height:1.5;max-width:62ch;margin:0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}
.karte{{display:flex;flex-direction:column;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;color:var(--ink);text-decoration:none}}
.karte:hover{{border-color:var(--accent)}}
.karte h2{{font-family:var(--font-d);font-size:1.6rem;margin:0}}
.karte p{{margin:0;line-height:1.45;flex:1}}
.los{{font-family:var(--font-m);font-size:.85rem;color:var(--accent)}}
</style>
</head>
<body>
<div class="wrap">
<span class="brand">Physik · Optik · Klasse 7</span>
<h1>Optik-Labore</h1>
<p>Zu jeder Leitfrage ein Labor zum Ausprobieren. Du kannst Regler verschieben, Dinge umschalten und am Ende dein Wissen prüfen.</p>
<div class="grid">{karten}</div>
</div>
</body>
</html>
"""
(HIER / "Optik-Labore.html").write_text(start, encoding="utf-8")
print("geschrieben: Optik-Labore.html")
