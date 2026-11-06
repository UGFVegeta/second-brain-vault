---
tags: [mathematik, diagnose, dreiecke, klasse7]
status: aktiv
date: 2026-11-04
---

# Diagnose Dreiecke 7c: welche Aufgabe prüft was

Geschrieben am 04.11.2026, vor Kapitel 2 (Dreiecke, ab Woche 8). 20 Minuten, Vorder- und Rückseite A4, Version A und B (gleiche Aufgaben, andere Zahlen). Grundlage: Standpunkt Schnittpunkt 7, S. 43, dazu Nebenwinkel und Scheitelwinkel. Kreis ist gestrichen (kein Zirkel dabei).

Ablauf wie beim [[Grundlagen-Check Workflow|Grundlagen-Check]]: Nummer statt Name, Selbsteinschätzung mit Smileys pro Aufgabe, Blätter einscannen, Claude liest die Scans aus. **Drucken in Originalgröße (100 %, nicht „an Seite anpassen“)**, sonst stimmen die Längen und Winkel nicht.

Dateien: `Mathe 7c – Diagnose Dreiecke – Version A.pdf`, `… – Version B.pdf`, `… – Lösung.pdf` (Seiten 1–2 = A ausgefüllt, 3–4 = B ausgefüllt). Bauskript `baue_diagnose_dreiecke.py`.

| Nr. | Stufe | Prüft | Standpunkt | Lösung A | Lösung B |
|---|---|---|---|---|---|
| 1 | ○ | Längen messen (mm genau) | A | 7,3 cm; 4,6 cm | 6,8 cm; 5,2 cm |
| 2 | ○ | Strecke zeichnen | B | 5,4 cm | 6,3 cm |
| 3 | ○ | Winkelarten unterscheiden, Winkelnamen α bis ε | C | stumpf, spitz, überstumpf, recht, gestreckt | recht, überstumpf, spitz, gestreckt, stumpf |
| 4 | ◐ | Winkel messen, auch stumpf (richtige Skala am Geodreieck) | D | 35°; 118° | 52°; 143° |
| 5 | ◐ | Winkel zeichnen mit vorgegebenem Schenkel | E | 65°; 130° | 75°; 145° |
| 6 | ● | Nebenwinkel und Scheitelwinkel (180°-Idee, Grundlage für die Winkelsumme) | neu im Kapitel | 142; 38; 142 | 134; 46; 134 |
| 7 | ◐ | Senkrechte und Parallele mit dem Geodreieck | F | Zeichnung | Zeichnung |
| 8 | ◐ | Koordinatensystem selbst zeichnen (1 Einheit = 1 cm), Punkte eintragen, zum Dreieck verbinden | H | A(1\|1); B(8\|2); C(4\|5) | A(1\|2); B(8\|1); C(5\|5) |

Toleranz beim Auswerten: Längen ±1 mm, gemessene und gezeichnete Winkel ±2°.

Typische Fehler, auf die es ankommt: Nr. 4 und 5 falsche Skala am Geodreieck (62 statt 118, 50 statt 130); Nr. 1 und 2 Messen ab dem Rand statt ab 0; Nr. 7 Senkrechte „nach Augenmaß“ ohne Geodreieck.

## Auswertung und Förderung (04.11.2026)

- Auswertung mit Tabs: `Diagnose Dreiecke 7c – Auswertung.html` (Bauskript `baue_auswertung.py`). Rohdaten und Standard-Berichte: `Auswertung 7c/`.
- Klasse: Längen 88 %, Winkelarten 82 %, Koordinatensystem 42 %, Winkel zeichnen 15 %, Winkel messen 12 %, Nebenwinkel 10 %, Senkrechte und Parallele 6 %.
- Förderblätter: `Mathe 7c – Förderblätter Dreiecke – alle Nummern.pdf` (ein doppelseitiges Blatt pro Nummer), Lösungen zum Aushängen: `… – Lösungen.pdf`. Zuteilung: `Auswertung 7c/Zuteilung Förderaufgaben.md`.
- Offen: Bögen A03 und A07 (beide „3“), A11, B05 (ohne Nummer), B09 einer Nummer zuordnen (`Auswertung 7c/baue_json.py`, dann beide Skripte neu laufen lassen), danach in den Verlauf eintragen.
