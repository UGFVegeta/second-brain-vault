#!/usr/bin/env python3
"""Baut die fünf Kernphysik-Labore und die Startseite Kernphysik-Labore.html (ein Link für IServ).
Nutzt den Rahmen aus ../Optik/baue_labore.py. Aufruf: python3 baue_labore_k10.py"""
import sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent / "Optik"))
import baue_labore as b  # noqa: E402

LABORE = [
    ("Leitfrage 1", "Atomlabor", "Atomlabor Atombau und Isotope.html", "atomlabor.js",
     "Woraus besteht Materie? Zoom in das Atom, Rutherford, Atom bauen, Isotope, Nuklidkarte."),
    ("Leitfrage 2", "Strahlungslabor", "Strahlungslabor Radioaktivitaet.html", "strahlungslabor.js",
     "Warum zerfallen manche Kerne? Nullrate, Luftballon, α, β und γ, elektrisches Feld, Absorber, Bleidicke."),
    ("Leitfrage 3", "Zerfallslabor", "Zerfallslabor Halbwertszeit.html", "zerfallslabor.js",
     "Wie schnell zerfällt ein Stoff? Würfelmodell, Halbwertszeit, Aktivität, Alltag, C-14-Uhr."),
    ("Leitfrage 4", "Wirkungslabor", "Wirkungslabor Strahlung und Koerper.html", "wirkungslabor.js",
     "Was macht Strahlung mit dem Körper? Ionisation, Nebelkammer, Zelle, Jahresdosis, Schutz."),
    ("Leitfragen 5 und 6", "Kernenergielabor", "Kernenergielabor Spaltung und Fusion.html", "kernenergielabor.js",
     "Wie gewinnt man Energie aus dem Kern? Spaltung, Kettenreaktion, Reaktor, Kraftwerk, Fusion, Abfall."),
]

if __name__ == "__main__":
    for lf, name, datei, js, _ in LABORE:
        b.baue(HIER, datei, name, f"Physik · Kernphysik · Klasse 10 · {lf}", HIER / "labore-quelle" / js)
    karten = "".join(f'<a class="karte" href="{d}"><span class="kicker">{lf}</span><h2>{n}</h2><p>{t}</p><span class="los">Öffnen →</span></a>'
                     for lf, n, d, _, t in LABORE)
    html = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Kernphysik-Labore</title>
<style>
{b.FONT_CSS}{b.BASIS_CSS}
.wrap{{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:18px}}
.wrap h1{{font-family:var(--font-d);font-weight:700;font-size:clamp(2rem,4.5vw,3.3rem);line-height:1.05;margin:4px 0 0}}
.wrap>p{{font-size:1.15rem;line-height:1.5;max-width:62ch;margin:0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}
.karte{{display:flex;flex-direction:column;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;color:var(--ink);text-decoration:none}}
.karte:hover{{border-color:var(--accent)}}
.karte h2{{font-family:var(--font-d);font-size:1.6rem;margin:0}}
.karte p{{margin:0;line-height:1.45;flex:1}}
.los{{font-family:var(--font-m);font-size:.85rem;color:var(--accent)}}
</style></head><body>
<div class="wrap"><span class="brand">Physik · Kernphysik · Klasse 10</span><h1>Kernphysik-Labore</h1>
<p>Zu jeder Leitfrage ein Labor zum Ausprobieren. Hier siehst du, was man im Physikraum nicht zeigen kann: Atome, Zerfälle, Strahlung im Körper und Kernreaktionen.</p>
<div class="grid">{karten}</div></div></body></html>
"""
    (HIER / "Kernphysik-Labore.html").write_text(html, encoding="utf-8")
    print("geschrieben: Kernphysik-Labore.html")
