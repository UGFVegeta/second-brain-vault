---
tags: [ressource, mathematik, unterricht, diagnose]
status: aktiv
erstellt: 2026-09-14
---

# Grundlagen-Check 7c, Schuljahr 2026/27

Laufende Auswertung für Oskars eigene Klasse 7c, siehe [[../Grundlagen-Check Workflow|Grundlagen-Check Workflow]] für den allgemeinen Ablauf. Nur Nummern, keine Namen.

## Stand

- **Teil 1** (Block A+B) geschrieben am 13./14.09.2026, ausgewertet am 14.09.2026. 25 Bögen, davon 24 mit lesbarer Nummer, ein Bogen ohne Nummer (Antworten trotzdem erfasst, siehe `ERGEBNISSE_OHNE_NUMMER` in `ergebnisse_roh.py`).
- **Teil 2** (Block C+D): noch offen.
- Nummer **1** und **8** fehlen beide unter den lesbaren Bögen – ungeklärt, ob der unnummerierte Bogen zu einer davon gehört oder ob ein Kind fehlte. Mit Anwesenheitsliste vom 14.09. abgleichen.
- Bei Nummer 25 stand versehentlich ein Vorname im Klasse-Feld statt „7c" – nirgends übernommen.

## Dateien

- `ergebnisse_roh.py` – von Hand aus dem Scan übertragene Rohantworten, mit Kommentaren zu unsicheren Stellen (`UNSICHER`-Liste am Ende)
- `selbsteinschaetzung_roh.py` – die „Ich?"-Smiley-Markierung je Aufgabe (sicher/ging so/unsicher), unsicherer gelesen als die Antworten selbst
- `baue_json.py` – baut `ergebnisse_7c_teil1.json` aus beiden Rohdateien
- `ergebnisse_7c_teil1.json` – Eingabedatei für `grundlagen_check_bericht.py`
- `Rückmeldungen Grundlagen Klasse 5-6.html` – erzeugter Bericht: Klassenübersicht, Diagramm Selbsteinschätzung-gegen-Ergebnis, Karte pro Nummer (mit Warnhinweis bei „sicher gefühlt, aber falsch"). Kopie liegt auch in iCloud unter `GDRS ICloud/Schuljahr 26 27/Mathematik/Mathematik 7c/`.
- `verlauf.json` – Mehrjahres-Speicher: pro Nummer die Gesamt-Prozentzahl jedes Testlaufs, wächst mit jedem weiteren Diagnosetest im Jahr
- `Verlauf.html` – aus `verlauf.json` erzeugte Übersicht, ein Diagramm pro Nummer. Bei nur einem Testlauf ein einzelner Punkt statt einer Linie, wächst zur echten Linie ab dem zweiten Test. Grundlage für die Diagnosegespräche im Januar. Kopie auch in iCloud.
- Originalscan: `~/Library/Mobile Documents/com~apple~CloudDocs/scans/Antwortbogen Grundlage Mathematik Klasse 5 bis 6 Teil - Ergebnisse Klasse 7c.pdf`

## Genauigkeit

Von Auge aus dem Scan gelesen, keine Software-OCR. Bei fünf Nummern (9, 16, 24, 25, 26) und dem unnummerierten Bogen war die Schrift mehrfach korrigiert oder verwischt – unklare Felder stehen als leer/„nicht bearbeitet", nicht geraten. Vor einer Präsentation diese Nummern gegen den Originalscan prüfen.

## Sobald Teil 2 vorliegt

1. Scan wie bei Teil 1 vorlegen, Antworten für Block C+D in `ergebnisse_roh.py` bei den bestehenden Nummern ergänzen (nicht neu anlegen). Selbsteinschätzung ebenso in `selbsteinschaetzung_roh.py`.
2. `baue_json.py` erneut laufen lassen, dann `grundlagen_check_bericht.py`.
3. Ergibt eine Rückmeldung über alle vier Blöcke statt nur A+B – das ist dann die Fassung fürs Coaching-Gespräch.
4. Mit `grundlagen_check_verlauf.py eintragen ...` (neues Test-Label, z. B. „Grundlagen 5-6 komplett") einen zweiten Punkt in `verlauf.json` eintragen. Ab dann zeigt `Verlauf.html` eine echte Linie statt eines einzelnen Punkts.

## Für jeden weiteren Diagnosetest im Jahr

Gleiches Muster, unabhängig vom Thema: neuer Lösungsschlüssel in `.scripts/grundlagen_check_schluessel.py`, `ergebnisse_roh.py` für den neuen Testlauf, `grundlagen_check_bericht.py` für die Rückmeldung, dann `grundlagen_check_verlauf.py eintragen` mit einem eigenen Test-Label und Datum – landet automatisch in derselben Zeitreihe wie Teil 1 und Teil 2, weil `verlauf.json` nur eine Gesamt-Prozentzahl je Testlauf braucht, keine gleichen Themenblöcke.
