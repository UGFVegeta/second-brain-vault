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
