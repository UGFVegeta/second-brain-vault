---
tags: [ressource, mathematik, unterricht]
---

# Mathematik

## Einstieg: Wo liegt was (zuerst lesen)

Diese Karte gilt für jede neue Mathe-Sitzung. Pfade relativ zu `04 Ressourcen/Mathematik/`. iCloud = `~/Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/`.

### Mathe 7c (Schuljahr 26/27)
- **Stunden (HTML + Folien-PDF):** `Rationale Zahlen/`, Dateiname `Mathe 7c – Woche N – k Titel`. Aktuell bis Woche 5 (Rezept für gemischte Aufgaben). Gesamtübersicht: `Mathematik Klasse 7 – Übersicht.html`, gebaut von `baue_uebersicht_mathe7.py` (Liste `STUNDEN`, eigener Stand im Dict `EIGEN`).
- **Neue Stunde bauen:** Vorlage `mathe_woche_vorlage.py`, Beispiel `Rationale Zahlen/baue_woche7.py` (Merkbild, Rezept-Box, Lücken). Stil und Regeln: Rezept-Merkheft-Stil, kleine Schritte, Aufgaben nie umbrechen. Dazu das Claude-Gedächtnis (`rezept-merkheft-stil`, `mathe-wochenformat`, `mathe-konzept-kleine-schritte`) und `Mein Mathe-Konzept – Aufgaben in kleine Schritte zerlegen.md`.
- **Klassenarbeit 1:** `Rationale Zahlen/Mathe 7c – Klassenarbeit Nr. 1 … – Entwurf` (Bauskript `baue_ka1_7c.py`), Übungs-KA daneben (`baue_uebung_ka1_7c.py`). KA 3 (Terme, Wo 16) ist Oskars.
- **Stoffverteilung:** `Mathematik Klasse 7 – Stoffverteilungsplan Schule.html`, Original-Excel liegt nur in iCloud (`Schuljahr 26 27/Mathematik/Mathematik 7c/01 Organisatorisches/`), nicht in den Vault kopieren.
- **Schulbuch Schnittpunkt 7:** iCloud `GDRS ICloud/Mathematik/Klasse 7/Schnittpunkt 7/Schnittpunkt 7 BW/content/pages/page_N/Scale4.png`, Ordnernummer = Buchseite + 3. Aufgaben abtippen, nicht als Screenshot einbauen.
- **iCloud-Ablage:** `Schuljahr 26 27/Mathematik/Mathematik 7c/`, Themenordner `04 Rationale Zahlen`. Export aus dem Vault mit `export_icloud_mathe.py` (Framework-Python 3.12). Gesamt-HTML kommt in den Hauptordner der Klasse.

### Mathe 10b (Schuljahr 26/27)
- **Stunden:** `Prozentrechnung Klasse 10/`, Dateiname `Mathe 10b – Woche N – k Titel`. Aktuell Woche 4 (Zinsen, Zinseszins). Wiederholung Prozent: `Prozent Wdh 10b – …`. Übersicht: `Mathematik Klasse 10b – Übersicht.html` (`baue_uebersicht_mathe10.py`).
- **Übungs-Klassenarbeit Nr. 1 Prozent und Wahrscheinlichkeit:** `Prozentrechnung Klasse 10/Mathe 10b – Übungsklassenarbeit Nr. 1 …` (Bauskript `baue_uebung_ka1_10b.py`, Vergleich `baue_vergleich_ka1_10b.py`).
- **Stoffverteilung:** `Stoffverteilungsplan 26-27 Mathe 10.html/.pdf/.xlsx` (Bauskript `baue_stoffverteilung10.py`).
- **Prüfung:** mündliche Realschulprüfung, Aufgabenpools in `Prüfungsaufgaben/` (Skill `pruefungsaufgaben-generator`). Stochastik: `Stochastik/`, Quadratische Funktionen: `Quadratische Funktionen/`.
- **Lösungen zum Buch Schnittpunkt 10:** iCloud `GDRS ICloud/Mathematik/Schnittpunkt/Schnittpunkt 10/Lösungen …/` als PDF je Doppelseite (mit `pdftotext -layout` lesbar).
- **iCloud-Ablage:** `Schuljahr 26 27/Mathematik/Mathematik 10b/` (`03 Wahrscheinlichkeit`, `04 Prozentrechnung`). Notenliste liegt lose im Klassenordner.

### Immer
- Nach jeder neuen oder geänderten Stunde: `export_icloud_mathe.py` laufen lassen und sagen, was ersetzt wurde.
- Lösungen immer als dasselbe Blatt ausgefüllt. Unterrichtsmaterial immer mit Lösungen.
- Keine Schülernamen oder Noten im Vault.

## Überblick
Unterrichtsmaterial und Werkzeuge für den Mathematikunterricht (Realschule BW).

## Themenordner
- **Quadratische Funktionen/** – Merkhefte (z. B. Parabeln)
- **Prozent- und Zinsrechnung/** – [[Prozent nach dem Mastery-Prinzip (Klasse 7)]]: Didaktik-Konzept (Prozentstreifen, „über 1 %", Variation) plus Aufgabenset
- **Prüfungsaufgaben/** – Aufgabenpools & Generator für die mündliche Realschulprüfung (Trigonometrie, Quadratische Funktionen, Stochastik, Sachrechnen, Boxplot, Stereometrie, Kurzaufgaben), siehe `Generator/ANLEITUNG.md`
- **Arbeitsblätter/** – Wiederholungsblätter, nach Klassen sortiert. Grundlagen-Checks Klasse 5–6 und Klasse 6–9 (anonymer Antwortbogen, automatische Auswertung) in **Grundlagen-Check/**, siehe [[Arbeitsblätter/Grundlagen-Check/Grundlagen-Check Workflow|Grundlagen-Check Workflow]]

## Notizen
-
