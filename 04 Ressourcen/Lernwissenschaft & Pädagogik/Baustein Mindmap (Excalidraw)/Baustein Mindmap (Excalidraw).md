---
tags: [baustein, unterricht, excalidraw]
status: aktiv
date: 2026-10-22
---

# Baustein: Mindmap-Zeichenfläche in der Stunden-HTML

Standard für künftige Stunden-HTMLs (Oskar, 22.10.2026). Auf Folien, bei denen Oskar mit der Klasse live sammelt (Beispiele, Ursachen, Ideen), steht kein fertiger Text, sondern ein Knopf **„Mindmap öffnen (M)“**. Er legt eine Excalidraw-Fläche über die Folie. Oskar schreibt und zeichnet mit Pencil auf dem iPad, die Fläche wird gespiegelt. Eine Fläche pro Datei, Oskar verschiebt sie zwischen den Folien.

Erstes Beispiel: `03 Bereiche/Schule & Unterricht/Klassenlehrer 7c/09 Zeitfensterwoche/Fr 23.10. Kluge Entscheidungen – Stunden.html` (Folie 4 und 5).

## Dateien in diesem Ordner

- `_excalidraw/`: Excalidraw 0.17.6 (UMD, MIT-Lizenz) mit React 18.3.1, Schriften und Sprachdateien. 5,5 MB, läuft offline. **Muss neben der Stunden-HTML liegen**, wie `_kv-…`.
- `mindmap-baustein.css`: Stil für Knopf und Overlay. Gehört in das `<style>` der HTML.
- `mindmap-baustein.js`: Logik. Gehört in das `<script>` **nach** dem Folien-Code (braucht `stage` und `i`) und vor `const start=…`.

## Einbauen

1. Ordner `_excalidraw` neben die neue Stunden-HTML kopieren.
2. CSS in den `<style>`-Block, JS in den `<script>`-Block (siehe oben).
3. In der Tastatur-Funktion der Folien direkt nach `const k=e.key;` einfügen:
   `if(mmOpen){ if(k==='m'&&!e.target.closest('.excalidraw-textEditorContainer, textarea, input')){ mmToggle(); e.preventDefault(); } return; }`
   `if(k.toLowerCase()==='m'){ mmToggle(); e.preventDefault(); return; }`
4. Auf jeder Folie mit Mindmap: `<button class="mmbtn" data-mm="a">Mindmap öffnen (M)</button>`. `data-mm` ist die Gruppe, `a` und `b` sind im Beispiel belegt.
5. Startelemente in `mmSeed()` anpassen: Gruppe a liegt bei x unter 1500, Gruppe b bei x ab 1500 (`mmGo` filtert nach Position, weil Excalidraw eigene IDs vergibt). Die Sprungknöpfe in `mmEl.innerHTML` beschriften.
6. Die Folie selbst bleibt leer oder zeigt nur Rahmen und Frage. Beispiele für Oskar gehören in Sprechzettel oder Anleitungen, nicht auf die Folie.

## Wissen

- Die Zeichnung steht in `localStorage` unter dem Schlüssel `kluge-mindmap-v1`. Für eine neue Stunde einen neuen Schlüssel setzen (`MM_KEY`), sonst erscheinen alte Zeichnungen.
- Zum Testen nicht per `file://` im eingebauten Browser, sondern über einen lokalen Server oder Chrome.
- Nicht geprüft: Apple Pencil auf dem iPad in Safari.
