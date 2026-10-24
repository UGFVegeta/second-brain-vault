---
tags: [baustein, unterricht, html]
status: aktiv
date: 2026-10-22
---

# Baustein Seitenleiste

Standard für **jede** Stunden-HTML mit Folien (Oskar, 22.10.2026: „Ab jetzt immer“): links neben der Folie eine Leiste mit den Abschnitten der Stunde, direkt anklickbar, Vorbild ist die Elternabend-Präsentation (`Elternabend 10b – Präsentation.html`, iCloud `Elternabend 10b`). Die Punkte hinter jedem Abschnitt sind die Folien darin, der aktuelle Punkt ist gefüllt. Die Punktreihe am unteren Folienrand entfällt.

## Aufbau
- Jede `<section class="slide">` trägt `data-tab="Abschnittsname"` und `data-group="Gruppenname"` (Gruppe leer lassen, wenn der Abschnitt allein steht). Aufeinanderfolgende Folien mit gleichem `data-tab` bilden einen Abschnitt mit Punkten.
- Gruppen sind die Teile der Stunde, in Schreibschrift als Überschrift, die Abschnitte darunter eingerückt.
- Tasten: Pfeil links/rechts Schritt (deckt auch schrittweise auf), Pfeil hoch/runter nächster Abschnitt, T Leiste aus/ein, F Vollbild (die Leiste bleibt im Vollbild sichtbar, T blendet sie aus).
- Markup: `<div id="present"><nav id="side"></nav><div id="stagecol"> Bühne, Steuerknöpfe, Hinweiskasten </div></div>`, Vollbild läuft auf `#present`.
- Zuordnung in der Kluge-Entscheidungen-Stunde: 12 Abschnitte in 4 Gruppen (Teil 1 bis Teil 4) plus Start und Zum Mitnehmen.

## Einbau
CSS aus `seitenleiste-baustein.css`, JS aus `seitenleiste-baustein.js` (nach `let i=0, stepIdx=0;`, `show()` ruft `updSide()` am Ende, ↑↓ rufen `tabStep(±1)`).
Knöpfe auf Folien (Gruppen auslosen, Mindmap) nie unten rechts, dort steht der Folienzähler: Gruppenknopf oben rechts, groß und gefüllt, damit Oskar ihn nicht übersieht.

Beispiel: `03 Bereiche/Schule & Unterricht/Klassenlehrer 7c/09 Zeitfensterwoche/Fr 23.10. Kluge Entscheidungen – Stunden.html`. Verwandt: [[Baustein Gruppen-Generator]], [[Baustein Mindmap (Excalidraw)]], [[Baustein Alles drucken]].
