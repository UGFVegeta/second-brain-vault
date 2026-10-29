# Sitzplan-Generator: Anleitung für Claude

Eine einzelne Offline-HTML: `Sitzplan.html`, kein Server, keine KI, Daten nur im Browser (localStorage). Dazu `Handbuch.html`, gebaut aus `Handbuch-Quelle/` mit `handbuch_bauen.py`. Funktionsübersicht: `Sitzplan Funktionen.excalidraw.md`.

## Harte Regeln
- Keine Schülernamen im Vault. Sicherungen `Sitzplaene-*.json` sind gitignored und gehören in den iCloud-Schulordner.
- Ausdruck darf nie den Dateipfad zeigen (`@page margin:0` plus Body-Padding 11 mm). Er nennt weder Variante noch Wunschpunkte oder Schlösser, nur Klasse, Raum, Stand, Blickrichtung. Nach jeder Druckänderung per Headless-Chrome-PDF prüfen.
- Lehrerregeln haben Vorrang vor Schülerwünschen (1e6 gegen 1000 Punkte).
- Alle Links/Rechts-Angaben in Dialogen gelten vom Pult aus. Standardansicht ist die Lehrersicht (Tafel unten).
- Fenster und Tür standardmäßig aus.

## Oskars Vorlieben
- Läuft auf dem kleinen MacBook-Bildschirm: Oberfläche muss bei etwa 1000×560 funktionieren (einzeilige Werkzeugleiste, Selteneres im „⋯“-Menü).
- Tische möglichst groß, Raum nie unter 20 px pro Kästchen, wenig Rand links/rechts. Lehrertisch bleibt 1,50 × 0,75 m.
- Grüner Punkt oben rechts am Namen, keine grünen Stühle.
- Moduswechsel Tische/Schüler muss auffallen (Chip über dem Raum).
- Speicherort wählt Oskar selbst („Sichern unter“).

## Nach Änderungen
- JS-Falle: `render()`/`init()` nie vor den `const`-Hilfsfunktionen aufrufen, Bootstrap ans Skriptende.
- Neue Funktion: im Handbuch ergänzen (`Handbuch-Quelle/`), `handbuch_bauen.py` laufen lassen, HTML in Chrome zeigen (`.scripts/chrome_zeigen.py`).

## Gelernt
Siehe [[Gelernt]].
