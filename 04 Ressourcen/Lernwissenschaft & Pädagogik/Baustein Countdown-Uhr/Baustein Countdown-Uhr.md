---
tags: [baustein, unterricht, html]
status: aktiv
date: 2026-10-22
---

# Baustein Countdown-Uhr

Standard für Stunden-HTMLs (Oskar, 22.10.2026: „Immer dann, wenn die Gruppenarbeit folgt“): auf jeder Folie, nach der eine Arbeitsphase mit fester Zeit läuft, steht unten links eine Uhr, die Oskar mit Start startet und die die Klasse mitlesen kann.

## Bedienung
- Folie bekommt `data-timer="Minuten"` oder `data-timer="5,15"` (mehrere Voreinstellungen, die erste gilt zuerst). Beispiel Kluge Entscheidungen: Folie 7 `5,15` (Einzelarbeit, Austausch), Folie 14 `20` (Situationskarten), Folie 23 `12` (Sketch vorbereiten).
- Knöpfe: Start/Pause, ↺ zurück auf die Voreinstellung, −1 und +1 Minute, bei mehreren Voreinstellungen je ein Knopf. Taste U startet und pausiert.
- Die Uhr läuft weiter, wenn die Folie gewechselt wird (zum Beispiel auf die Regel-Folie). Die Zeit wird aus der Systemuhr berechnet und driftet nicht.
- In der letzten Minute wird die Zahl orange, bei 0:00 blinkt die Uhr rot und es gibt drei kurze Pieptöne.
- Die Zeiten kommen aus Oskars Ablaufblatt der Stunde, nicht aus dem Lehrerband.

## Einbau
CSS aus `uhr-baustein.css`, JS aus `uhr-baustein.js` (vor `tabStep`, nach dem Seitenleisten-Block); `show()` ruft am Ende `uSlide()`; im Tastenhandler `U` auf `uToggle()`. Die Uhr liegt innerhalb von `#stage`, bleibt also im Vollbild sichtbar.

Verwandt: [[Baustein Seitenleiste]], [[Baustein Gruppen-Generator]].
