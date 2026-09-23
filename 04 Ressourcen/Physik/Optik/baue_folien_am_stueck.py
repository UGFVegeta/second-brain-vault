#!/usr/bin/env python3
"""Baut die schlanke Stunden-HTML mit echten Tabs (Umschalten statt Scrollen).
Tab 1 "Folien": die AUSGEFÜLLTEN Folien aus 'Optik I.html' am Stück (Folie = Tafelbild, keine Zeiten).
Seitenzahl = Seite in Optik I.pdf (eine Folie pro Seite). Aufruf: python3 baue_folien_am_stueck.py
"""
import re
from pathlib import Path

hier = Path(__file__).parent
quelle = (hier / "Optik I.html").read_text(encoding="utf-8")
folien = re.findall(r'<section class="folie[^"]*">.*?</section>', quelle, flags=re.S)
SEITEN = [11, 12, 13, 14, 15, 16, 18, 19, 20, 21]   # 17 (leere Fassung) bewusst weggelassen
TITEL = "Optik · Do 24.09.2026"

karten = []
for p in SEITEN:
    f = re.sub(r'\s*<div class="ab-hinweis">.*?</div>', "", folien[p - 1], flags=re.S)  # keine Marker
    karten.append(f'<div class="karte">{f}</div>')

alltag = [
    ("Wolke am Himmel", "beleuchtet", "wirft Sonnenlicht zurück"),
    ("Rückstrahler, Katzenaugen", "beleuchtet", "leuchten nur, wenn sie angestrahlt werden"),
    ("Fahrrad-Rücklicht (LED)", "Lichtquelle", "erzeugt selbst Licht"),
    ("Sterne / Planeten", "Sterne: Lichtquellen, Planeten: beleuchtet", "Sterne sind ferne Sonnen"),
    ("Schwarzes T-Shirt in der Sonne", "Absorption", "Licht wird verschluckt, das Shirt wird warm"),
    ("Weiße Wand", "Streuung", "Licht geht in alle Richtungen, Wand von überall sichtbar"),
    ("Fensterscheibe", "Transmission", "Licht geht (fast) ungehindert hindurch"),
    ("Milchglas (Badfenster)", "Transmission und Streuung", "hell, aber nur Umrisse erkennbar"),
]
alltag_tab = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a, b, c in alltag)

buch = [
    ("S. 27–28", "Fahrrad-Aufgabe, sechs Fotos zuordnen (Glühwürmchen, Vollmond, Blitz, LED …)", "Lichtquellen"),
    ("S. 33", "Teelicht durch Gummischlauch sehen, Weg des Lichts mit Alufolie und Rauch", "Lichtausbreitung"),
    ("S. 36–37", "Drei Schattenversuche (C = dein Ray-Box-Versuch)", "Schatten"),
    ("S. 40", "Globus, Lampe, Papierkugel: Tag und Nacht, Mondphasen", "Mond"),
    ("S. 45", "glatte und zerknitterte Alufolie, Reflexionsgesetz mit Faden", "Reflexion"),
    ("S. 48–49", "Lerncheck mit 25 Aufgaben", "Wiederholung"),
]
buch_tab = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in buch)

html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITEL}</title>
<link rel="stylesheet" href="folien.css">
<style>
body{{background:#e9eaee;margin:0;font:16px/1.5 -apple-system,"Helvetica Neue",Arial,sans-serif;color:#1b1b1b}}
header{{background:#fff;border-bottom:1px solid #d3d6dd;position:sticky;top:0;z-index:10}}
.in{{width:956px;max-width:100%;margin:0 auto;padding:0 8px}}
h1{{font-size:18px;margin:0;padding:12px 0 8px}}
.tabs{{display:flex;gap:6px;padding-bottom:10px}}
.tabs button{{border:0;background:#f0f1f4;padding:7px 16px;border-radius:16px;font:inherit;font-size:14.5px;cursor:pointer}}
.tabs button.on{{background:#1b1b1b;color:#fff}}
.tab{{display:none;padding:22px 0 60px}}.tab.on{{display:block}}
.karte{{width:956px;height:539px;margin:0 auto 22px;box-shadow:0 2px 10px rgba(0,0,0,.18)}}
.karte .folie{{page-break-after:auto}}
.card{{background:#fff;border-radius:10px;padding:14px 20px;margin:0 0 16px;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
.card h2{{font-size:16px;margin:0 0 6px}}.card ul{{margin:6px 0;padding-left:20px}}
a.btn{{display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;border-radius:16px;background:#eef3fb;color:#1a56a0;text-decoration:none;font-size:14.5px}}
table{{border-collapse:collapse;width:100%;font-size:15px}}td,th{{border-bottom:1px solid #e1e3e8;padding:6px 8px;text-align:left;vertical-align:top}}
.warn{{background:#fff6e0;border-left:4px solid #e0a100;padding:8px 12px;font-size:14.5px;margin-top:10px}}
</style></head><body>
<header><div class="in"><h1>{TITEL}</h1>
<div class="tabs"><button data-t="folien">Folien</button><button data-t="ab">Arbeitsblätter</button>
<button data-t="vorher">Vorher</button><button data-t="alltag">Alltag</button><button data-t="buch">Buch-Ideen</button></div></div></header>
<div class="in">
<div class="tab" id="t_folien">{''.join(karten)}</div>

<div class="tab" id="t_ab">
<div class="card"><h2>Arbeitsblatt Lichtquellen</h2>
<a class="btn" href="Materialien/Lichtquellen W03.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Lichtquelle (L): Kerze, Glühlampe, Lagerfeuer, Blitz, Taschenlampe, Sonne. Beleuchtet (B): Mond, Tafel, Buch, Zimmerpflanze, Spielzeugauto.
Aufgabe 2: z. B. Glühwürmchen, Polarlicht, Sterne / Feuerwerk, Bildschirm, Laser. Aufgabe 3: Glühlampe und Taschenlampe.</p>
<div class="warn">Aufgabe 3 sagt „erst seit etwa 200 Jahren“. Das ist zu ungenau (Glühlampe ab ca. 1880). Besser „gut 100 Jahre“. Ich ändere das Blatt auf Zuruf.</div></div>
<div class="card"><h2>Versuchsblatt Blatt, Karton, Glasscheibe</h2>
<a class="btn" href="Materialien/Licht trifft auf einen Koerper W04.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Weißes Blatt: heller, breiter Lichtfleck, Licht wird in viele Richtungen zurückgeworfen (<b>gestreut</b>). Schwarzer Karton: dunkel, Licht wird
<b>absorbiert</b>. Glasscheibe: Strahl dahinter fast unverändert, Licht wird <b>durchgelassen</b> (Transmission).</p></div>
</div>

<div class="tab" id="t_vorher"><div class="card"><h2>Vorher</h2><ul>
<li>Kopieren: Arbeitsblatt Lichtquellen (Seite 1), Versuchsblatt (Seite 1).</li>
<li>Material: Ray-Box(en), weißes Blatt, schwarzer Karton, klare Glasscheibe. Raum abdunkeln.</li>
<li>Die Folien laufen ab Folie 12. Folien 1–11 hast du schon gehalten.</li>
<li>Notability: leere Karoseite, Bilder per Screenshot (Ctrl + Cmd + Shift + 4) aus dem Tab „Folien“ holen.</li></ul></div></div>

<div class="tab" id="t_alltag"><div class="card"><h2>Alltagsbeispiele</h2>
<table><tr><th>Beispiel</th><th>Antwort</th><th>Warum</th></tr>{alltag_tab}</table></div></div>

<div class="tab" id="t_buch"><div class="card"><h2>Erlebnis Physik 7–9 (nur für dich)</h2>
<table><tr><th>Seite</th><th>Idee</th><th>Passt zu</th></tr>{buch_tab}</table></div></div>
</div>
<script>
const tabs=[...document.querySelectorAll('.tabs button')],secs=[...document.querySelectorAll('.tab')];
function show(id){{tabs.forEach(b=>b.classList.toggle('on',b.dataset.t===id));secs.forEach(s=>s.classList.toggle('on',s.id==='t_'+id));history.replaceState(null,'','#'+id);requestAnimationFrame(()=>window.scrollTo(0,0))}}
tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));
history.scrollRestoration='manual';show(secs.some(s=>s.id==='t_'+location.hash.slice(1))?location.hash.slice(1):'folien');
</script></body></html>"""

ziel = hier / "Optik – Do 24.09. – Stunde.html"
ziel.write_text(html, encoding="utf-8")
print("geschrieben:", ziel.name, f"({len(html) // 1024} KB), Folien:", len(karten))
