#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut aus den Diagrammen + Text eine HTML-Datei fuer den PDF-Export (Chrome)."""
import base64, os

BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude"
ANH = f"{BASE}/07 Anhänge"
OUT_HTML = f"{BASE}/.scripts/escooter_print.html"

def img(name):
    with open(f"{ANH}/{name}", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{b64}" alt="{name}">'

html = f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">
<style>
@page {{ size: A4 portrait; margin: 16mm 14mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; color:#1a1a1a; font-size: 12.5pt; line-height: 1.45; }}
h1 {{ font-size: 20pt; margin: 0 0 4px; }}
h2 {{ font-size: 14.5pt; margin: 18px 0 6px; border-bottom: 2px solid #1f77b4; padding-bottom: 3px; color:#10406b; }}
.sub {{ color:#666; font-size: 10.5pt; margin-bottom: 14px; }}
img {{ width: 100%; max-width: 165mm; display:block; margin: 6px auto; border:1px solid #ddd; border-radius:6px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 11pt; margin: 6px 0; }}
th, td {{ border: 1px solid #bbb; padding: 4px 7px; text-align: center; }}
th {{ background: #eef3f8; }}
td.l, th.l {{ text-align: left; }}
.muted {{ color:#666; font-size: 10pt; }}
.box {{ border-radius: 8px; padding: 9px 13px; margin: 9px 0; font-size: 11.5pt; }}
.info {{ background:#eef5fb; border-left: 5px solid #1f77b4; }}
.tip  {{ background:#eefaf0; border-left: 5px solid #2ca02c; }}
.warn {{ background:#fdf3ec; border-left: 5px solid #e07b1f; }}
.box b {{ display:block; margin-bottom:2px; }}
.formula {{ font-style: italic; background:#f6f6f6; padding:1px 6px; border-radius:4px; }}
.scoot {{ color:#1f77b4; font-weight:bold; }}
.lauf  {{ color:#d62728; font-weight:bold; }}
ul {{ margin: 4px 0 4px 18px; padding:0; }}
li {{ margin: 2px 0; }}
.avoid {{ break-inside: avoid; }}
.pb {{ break-before: page; }}
.merk {{ background:#f4f6f8; border:1px dashed #99a; border-radius:8px; padding:9px 13px; margin-top:14px; font-size:11.5pt; }}
</style></head><body>

<h1>Versuch: E-Scooter vs. Schüler – Bewegungsdiagramme</h1>
<div class="sub">Physik · Klasse 9 Realschule · Thema: Bewegungen (s-t-, v-t- und a-t-Diagramm)</div>

<h2>1. Versuchsaufbau</h2>
<p>Auf einer <b>100-m-Bahn</b> wird alle <b>10 m die Zeit gestoppt</b>. Verglichen werden zwei „Fahrzeuge":</p>
<ul>
<li><span class="scoot">E-Scooter</span> – 3 Messfahrten (t₁, t₂, t₃), alle einzeln in den Diagrammen</li>
<li><span class="lauf">Schüler (gelaufen)</span> – 1 Messung (t₄)</li>
</ul>
<div class="box info"><b>Warum drei Messungen?</b>Der E-Scooter wurde dreimal gemessen, um die Zuverlässigkeit (Reproduzierbarkeit) zu prüfen und Messfehler einzuschätzen. In der Tabelle steht zusätzlich der Mittelwert (Ø).</div>

<h2>2. Messwerte <span class="muted">(Zeiten in Sekunden)</span></h2>
<table class="avoid">
<tr><th class="l">Weg s</th><th>10 m</th><th>20 m</th><th>30 m</th><th>40 m</th><th>50 m</th><th>60 m</th><th>70 m</th></tr>
<tr><td class="l">t₁ (Scooter)</td><td>3,6</td><td>5,0</td><td>7,3</td><td>8,7</td><td>10,7</td><td>12,1</td><td>14,0</td></tr>
<tr><td class="l">t₂ (Scooter)</td><td>2,1</td><td>4,3</td><td>6,8</td><td>8,2</td><td>9,9</td><td>11,8</td><td>13,6</td></tr>
<tr><td class="l">t₃ (Scooter)</td><td>2,6</td><td>4,5</td><td>6,8</td><td>8,2</td><td>10,1</td><td>12,0</td><td>13,8</td></tr>
<tr style="background:#eef5fb"><td class="l"><b>Ø Scooter</b></td><td><b>2,8</b></td><td><b>4,6</b></td><td><b>7,0</b></td><td><b>8,4</b></td><td><b>10,2</b></td><td><b>12,0</b></td><td><b>13,8</b></td></tr>
<tr><td class="l">t₄ (Schüler)</td><td>2,2</td><td>3,1</td><td>4,7</td><td>5,8</td><td>7,0</td><td>8,0</td><td>9,3</td></tr>
</table>

<h2>3. s-t-Diagramm (Weg-Zeit)</h2>
<div class="avoid">{img("E-Scooter s-t-Diagramm.png")}</div>
<ul>
<li>Die <b>drei Scooter-Läufe liegen dicht beieinander</b> → die Messung ist gut reproduzierbar.</li>
<li>Alle Kurven sind <b>annähernd Geraden</b> → die Bewegung ist (nach dem Anfahren) <b>gleichförmig</b>.</li>
<li>Die Gerade des <span class="lauf">Schülers</span> ist <b>steiler</b> → er ist <b>schneller</b>.</li>
<li>Die <b>Steigung</b> der s-t-Geraden ist die Geschwindigkeit: <span class="formula">v = Δs / Δt</span></li>
</ul>

<h2 class="pb">4. v-t-Diagramm (Geschwindigkeit-Zeit)</h2>
<p>Für jeden 10-m-Abschnitt: <span class="formula">v = Δs / Δt = 10 m / Δt</span></p>
<div class="avoid">{img("E-Scooter v-t-Diagramm.png")}</div>
<ul>
<li>Die Geschwindigkeit bleibt nach dem Start ungefähr <b>konstant</b> (Punkte schwanken nur → Messfehler).</li>
<li><span class="scoot">E-Scooter:</span> v ≈ 5,6 m/s ≈ <b>20 km/h</b></li>
<li><span class="lauf">Schüler:</span> v ≈ 8,7 m/s ≈ <b>31 km/h</b></li>
</ul>
<div class="box tip"><b>Verbindung zur Realität</b>E-Scooter sind in Deutschland gesetzlich auf <b>20 km/h</b> gedrosselt – unser Messwert trifft das fast genau! Der sprintende Schüler war kurzzeitig sogar schneller.</div>

<h2 class="pb">5. a-t-Diagramm (Beschleunigung-Zeit)</h2>
<p>Beschleunigung: <span class="formula">a = Δv / Δt</span></p>
<div class="avoid">{img("E-Scooter a-t-Diagramm.png")}</div>
<ul>
<li>Die Werte liegen <b>nahe bei a = 0</b> (grüner Bereich) → Bestätigung: <b>gleichförmige Bewegung</b>.</li>
<li>Bei gleichförmiger Bewegung ist die Beschleunigung <b>null</b>, weil sich die Geschwindigkeit nicht ändert.</li>
<li>Echte Beschleunigung gab es vor allem beim <b>Anfahren</b> – diese kurze Phase war mit der Handstoppuhr kaum erfassbar.</li>
</ul>

<h2>6. Ergebnis / Fazit</h2>
<table class="avoid">
<tr><th class="l"></th><th>E-Scooter</th><th>Schüler</th></tr>
<tr><td class="l">Geschwindigkeit</td><td>≈ 5,6 m/s (20 km/h)</td><td>≈ 8,7 m/s (31 km/h)</td></tr>
<tr><td class="l">Strecke 70 m in</td><td>≈ 13,8 s</td><td>9,3 s</td></tr>
<tr><td class="l">Bewegungsart</td><td>gleichförmig</td><td>gleichförmig</td></tr>
</table>
<p>➡️ <b>Beide bewegen sich (nach dem Anfahren) gleichförmig.</b> Der Schüler war über die gemessene Strecke schneller als der gedrosselte E-Scooter.</p>
<div class="box warn"><b>Messfehler – wichtig</b>Die Zeiten wurden <b>von Hand</b> gestoppt. Die Reaktionszeit (~0,2–0,3 s) ist groß im Vergleich zu den kurzen Abschnittszeiten (~1–2 s). Deshalb schwanken die Punkte im v-t- und a-t-Diagramm stark, obwohl die Bewegung fast gleichförmig ist. Genauer: <b>Lichtschranken</b>.</div>

<div class="merk">
<b>Merksätze</b>
<ul>
<li>s-t-Diagramm Gerade ⇒ gleichförmige Bewegung; Steigung = Geschwindigkeit.</li>
<li>v-t-Diagramm waagerechte Linie ⇒ konstante Geschwindigkeit.</li>
<li>a-t-Diagramm auf der Nulllinie ⇒ keine Beschleunigung (a = 0).</li>
<li><span class="formula">v = Δs / Δt</span> &nbsp;&nbsp; <span class="formula">a = Δv / Δt</span></li>
</ul>
</div>

</body></html>"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(OUT_HTML)
