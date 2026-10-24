---
tags: [baustein, unterricht, pdf]
status: aktiv
date: 2026-10-22
---

# Baustein Alles drucken

Standard für jede Stunden-HTML, bei der etwas kopiert werden muss (Oskar, 22.10.2026): im Tab **Kopiervorlagen** oben ein grüner Kasten „Alles auf einmal drucken“ mit einem Knopf, der **eine** PDF öffnet. Diese PDF enthält alle Kopiervorlagen in der Reihenfolge der Stunde, ein Druckauftrag, ein Knopfdruck. Alternativ speichert Oskar die PDF und druckt sie in der Schule.

## Regeln für die PDF
- Dateiname `<Datum> 0 Alles zum Drucken (doppelseitig, ein Auftrag).pdf`, liegt neben der Stunden-HTML im Vault und in der iCloud-Ablage der Stunde; der Knopf verlinkt relativ (Leerzeichen als `%20`).
- Alles als **ein doppelseitiger Auftrag** (Hochformat, lange Kante): Doppelseitiges mit echter Vorder- und Rückseite, einseitige Blätter bekommen eine leere Rückseite, damit nichts verrutscht.
- Klassensatz nur **einmal** aufnehmen; Oskar kopiert ihn am Kopierer so oft wie nötig.
- Abgedeckte Karten (z. B. Karte 10) werden mit einem weißen Rechteck in der PDF verdeckt, bei gespiegelter Rückseite auf der anderen Spalte.
- Die Zeile steht auch im Tab Material als Nummer 0, die Einzeldateien bleiben bestehen.
- Querformat-Blätter nur für Oskar (Regieblatt): Druckrichtung der Rückseite hängt vom Drucker ab, Variante mit um 180° gedrehten Rückseiten bereithalten.

## Bau (reportlab, Python 3.12)
Seiten des Scans mit `pdftoppm -r 200 -gray -jpeg` rendern, dann je Seite `drawImage`, Maske mit `rect`, leere Rückseite mit `showPage()`. Vorlage: Skript in der Sitzung vom 22.10.2026; Aufbau `page(img, mask)` und `blank()`.

Verwandt: [[Baustein Mindmap (Excalidraw)]], [[Baustein Gruppen-Generator]].
