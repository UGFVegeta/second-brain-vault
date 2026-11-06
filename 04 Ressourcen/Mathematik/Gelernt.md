---
tags: [gelernt, mathematik]
---

# Mathematik: Gelernt

Eine Zeile pro Erkenntnis, neueste oben. Lang ausgeführte Gründe stehen im Claude-Gedächtnis, hier nur die Folge.

- 05.11.2026: Bei der Diagnose fehlten oder doppelten sich Nummern. Folge: nächste Diagnose mit vorgedruckten Nummern 1 bis 26, Zuteilung über den Sitzplan, A und B im Schachbrett, Stapel in Sitzreihenfolge (Details im Grundlagen-Check Workflow).
- 04.11.2026: Oskar findet in großen Themenordnern nichts mehr. Folge: Rationale Zahlen in Unterordner nach Woche, Übungstests, Klassenarbeit und `_Skripte/` aufgeteilt; neue Themen gleich so anlegen (Dreiecke: `01 Diagnose – Test, Auswertung, Förderblätter/`). Auswertungen nicht als lose HTMLs, sondern als eine HTML mit Tabs wie die Stunden (`Dreiecke/01 Diagnose – Test, Auswertung, Förderblätter/baue_auswertung.py`).
- 04.11.2026: Lösung Diagnose Dreiecke Nr. 7 hatte eine Senkrechte, die nicht senkrecht war, und das rechte-Winkel-Zeichen war eckig. Folge: rechter Winkel immer als Viertelkreis mit Punkt (`rechter_winkel_zeichen` in `Dreiecke/01 Diagnose – Test, Auswertung, Förderblätter/baue_diagnose_dreiecke.py`), Senkrechten in Lösungen rechnerisch prüfen (Skalarprodukt 0), nicht nach Augenmaß.
- 04.11.2026: Diagnose Dreiecke ausgewertet wie der Grundlagen-Check (Schlüssel `dreiecke` in `.scripts/grundlagen_check_schluessel.py`, Zeichenaufgaben beim Auslesen als r/f bewertet). Danach Förderblätter pro Nummer aus einem Pool von 21 Aufgaben (`Dreiecke/01 Diagnose – Test, Auswertung, Förderblätter/baue_foerderblaetter.py`), Lösung als ein Pool-Lösungsblatt.
- 04.11.2026: Diagnose Dreiecke 7c mit Mess- und Zeichenaufgaben als ganzseitige SVG in Millimetern gebaut (`Dreiecke/01 Diagnose – Test, Auswertung, Förderblätter/baue_diagnose_dreiecke.py`): feste Felder für den Scan, Maße stimmen nur bei Druck in Originalgröße. Ablauf wie Grundlagen-Check (Nummer, Smileys, A/B). Kein Zirkel dabei, also keine Kreisaufgaben ohne Vorankündigung.
- 02.11.2026: Lerntheke mit Rechnen auf dem Blatt hatte zu wenige Aufgaben. Folge: etwa doppelt so viele Aufgaben pro A4-Seite (12 ○ in vier Spalten, 8 ◐, 4 ●), darunter kleine Kästchenfelder (○ 2 Kästchen, ◐ und ● 4 Kästchen hoch); Rest kann Hausaufgabe werden. Vorrechenseiten (lange Beispiele) ganz kariert, Rezept nur beim ersten Beispiel. Im Unterricht läuft das Folien-PDF vom iPad, Seitenleiste und Uhr helfen nur am MacBook.
- 02.11.2026: Mathe-Stunden hatten bisher keine Seitenleiste und keine Uhr. Folge: `bau_woche(..., leiste=..., quer=...)` baut die Folien als A4-Seiten mit Seitenleiste und Countdown-Uhr aus den Bausteinen; neue Mathe-Stunden immer so bauen (erste: Woche 7, Stunde 2).
- 01.11.2026: Lange „Weitere Beispiele“ im Merkbild liefen in der HTML ineinander (Raster zu schmal, nowrap). Folge: bei langen Beispielen eine Spalte erzwingen und die ausgefüllte Seite in HTML und PDF ansehen, nicht nur im PDF.
- Erwartungswert: Einsatz immer abziehen, Lösung als eine Gleichung P·Gewinn + … − Einsatz, fair heißt E = 0.
- Prozent: per Dreisatz lösen, 100 % und „neues 100 %“ markieren, Formel nur kurz darunter.
- Rationale Zahlen: Subtraktion direkt über Bewegung am Zahlenstrahl einführen, Gegenzahl-Formalismus erst in Klasse 8.
- Klassenarbeit im Kurztest-Layout (Balken, Karofläche, A3-Broschüre), Schreibweise ohne Plus und Klammern wie im Unterricht.
- Merkheft und Übungsheft trennen: Merksätze ins Merkheft, alle Übungen ins Übungsheft.
- Wochentempo darf von der Parallelklasse abweichen, nur der KA-Termin zählt.
