---
tags: [ressource, mathematik, unterricht, diagnose]
status: aktiv
erstellt: 2026-09-14
---

# Grundlagen-Check 7c, Schuljahr 2026/27

Laufende Auswertung für Oskars eigene Klasse 7c, siehe [[../Grundlagen-Check Workflow|Grundlagen-Check Workflow]] für den allgemeinen Ablauf. Nur Nummern, keine Namen.

## Stand

- **Teil 1** (Block A+B) geschrieben am 13./14.09.2026. 25 Bögen, davon 24 mit lesbarer Nummer, ein Bogen ohne Nummer.
- **Teil 2** (Block C+D) geschrieben am 15.09.2026. 23 Bögen aus dem ersten Scan plus 2 weitere (Nummer 16 und 18) aus einem separaten Nachtrags-Scan, den Oskar nachgereicht hat – insgesamt 25 Teil-2-Bögen. Beide Teile sind zu einer Rückmeldung über alle vier Blöcke zusammengeführt (`ergebnisse_7c_komplett.json`).
- Teil 1 und Teil 2 hatten nicht exakt dieselben Kinder anwesend:
  - In Teil 1, aber **nicht** in Teil 2: nur noch Nummer **12** – zeigt im Bericht „nicht bearbeitet" bei Block C/D.
  - In Teil 2, aber **nicht** in Teil 1: Nummer **1** – löst die alte Teil-1-Lücke auf, zeigt dort „nicht bearbeitet" bei Block A/B.
  - Zwei Teil-2-Bögen hatten statt einer Ziffer nur eine schwer lesbare Schleife im Nummernfeld – vorläufig als **8** und **9** eingetragen (9 gab es schon aus Teil 1). **Vor einer echten Verwendung unbedingt gegen die Originalbögen prüfen**, siehe `UNSICHER` in `ergebnisse_roh.py`.
  - Ein weiterer Bogen war zunächst als Nummer „29" gelesen worden (verwechselte Schleife/Ziffer) – Oskar hat korrigiert: das ist **Nummer 21**, die schon aus Teil 1 bekannt war. Es gibt also keine Nummer 29.
- Bei Nummer 25 (Teil 1) stand versehentlich ein Vorname im Klasse-Feld statt „7c" – nirgends übernommen.
- Die alte reine Teil-1-JSON (`ergebnisse_7c_teil1.json`) ist überholt und liegt im Papierkorb; `ergebnisse_7c_komplett.json` ist die aktuelle Eingabedatei.

## Dateien

- `ergebnisse_roh.py` – von Hand aus den Scans übertragene Rohantworten, Teil 1 (A/B) und Teil 2 (C/D) pro Nummer zusammengeführt, mit Kommentaren zu unsicheren Stellen (`UNSICHER`-Liste am Ende, inkl. der 8/9-Verwechslungsgefahr und der fehlenden Nummern je Teil)
- `selbsteinschaetzung_roh.py` – die „Ich?"-Smiley-Markierung je Aufgabe (sicher/ging so/unsicher) für beide Teile, unsicherer gelesen als die Antworten selbst
- `baue_json.py` – baut `ergebnisse_7c_komplett.json` aus beiden Rohdateien
- `ergebnisse_7c_komplett.json` – Eingabedatei für `grundlagen_check_bericht.py` (alle vier Blöcke, alle 27 bekannten Nummern)
- `Rückmeldungen Grundlagen Klasse 5-6.html` – erzeugter Bericht: Klassenübersicht über alle vier Blöcke, Diagramm Selbsteinschätzung-gegen-Ergebnis, Karte pro Nummer (mit Warnhinweis bei „sicher gefühlt, aber falsch"). Kopie in iCloud unter `GDRS ICloud/Schuljahr 26 27/Mathematik/Mathematik 7c/Grundlagen-Check 7c – Rückmeldungen.html`.
- `Praesentation.html` – Beamer-Ansicht für die ganze Klasse (`.scripts/grundlagen_check_praesentation.py`): nur Klassen-Gesamtwerte, keine Nummern-Ebene. Kopie auch in iCloud.
- `Schnipsel Grundlagen Klasse 5-6.pdf` (+ `.html`) – ein kleiner Zettel pro Nummer zum Ausschneiden und Austeilen (`.scripts/grundlagen_check_schnipsel.py`): Gesamtergebnis, Themenblöcke, Selbsteinschätzung-Vergleich. 2 Spalten x 5 Zeilen pro A4-Seite, gepunktete Schnittlinien (einmal senkrecht, viermal waagrecht). Kopie auch in iCloud.
- `verlauf.json` / `Verlauf.html` – Mehrjahres-Speicher und Übersicht, ein Diagramm pro Nummer. Enthält bisher **einen** Testlauf „Grundlagen 5-6" (2026-09-15) mit der Gesamt-Prozentzahl über alle vier Blöcke. Teil 1 und Teil 2 zählen bewusst **nicht** als zwei eigene Punkte in der Zeitreihe – sie sind derselbe Diagnosetest, nur an zwei Tagen geschrieben. Ein zweiter echter Punkt kommt erst mit dem nächsten, inhaltlich neuen Diagnosetest im Jahr. Kopie auch in iCloud.
- Originalscans: `~/Library/Mobile Documents/com~apple~CloudDocs/scans/Antwortbogen Grundlage Mathematik Klasse 5 bis 6 Teil - Ergebnisse Klasse 7c.pdf` (Teil 1), `15092026_1 D ● Größen und Geometrie.pdf` (Teil 2, 23 Bögen) und `15092026_Antwortbogen - Grundlagen Mathematik Klasse 5 bis 6 ● T.pdf` (Teil 2, Nachtrag: Nummer 16 und 18)

## Genauigkeit

Von Auge aus den Scans gelesen, keine Software-OCR. Unklare Felder stehen als leer/„nicht bearbeitet", nicht geraten. Teil 2 hatte spürbar mehr durchgestrichene/korrigierte Antworten als Teil 1 – vor einer wichtigen Verwendung (Gespräch, Präsentation) die in `UNSICHER` gelisteten Nummern gegen die Originalscans prüfen. Besonders wichtig: die 8/9-Zuordnung und Nummer 29 (neu, unklarer Vorname im Klasse-Feld).

## Für jeden weiteren Diagnosetest im Jahr

Gleiches Muster, unabhängig vom Thema: neuer Lösungsschlüssel in `.scripts/grundlagen_check_schluessel.py`, eigene `ergebnisse_roh.py`-Einträge für den neuen Testlauf, `grundlagen_check_bericht.py` für die Rückmeldung, dann `grundlagen_check_verlauf.py eintragen` mit einem eigenen Test-Label und Datum – landet automatisch in derselben Zeitreihe, weil `verlauf.json` nur eine Gesamt-Prozentzahl je Testlauf braucht, keine gleichen Themenblöcke. Nur wenn ein Test wie hier in mehreren Teilen an verschiedenen Tagen schreibt, zählt das als **ein** Testlauf, nicht mehrere – erst nach dem letzten Teil in den Verlauf eintragen.
