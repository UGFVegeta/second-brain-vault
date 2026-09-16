---
tags: [mathematik, diagnostik, klasse-10]
date: 2026-09-16
status: abgeschlossen
---

# Grundlagen-Check 10b – Klasse 8-9 (16.09.2026)

Erster Durchlauf mit **zwei Versionen (A/B)**. 27 Bögen, davon 14 × Version A
und 13 × Version B. Nur Nummern, keine Namen.

## Was hier liegt

| Datei | Zweck |
|---|---|
| `ergebnisse_roh.py` | Handtranskription aller 27 Bögen + `VERSIONEN` + `UNSICHER` + `TERME_MANUELL` |
| `selbsteinschaetzung_roh.py` | Smiley-Einschätzung je Aufgabe |
| `baue_json.py` | baut daraus `ergebnisse_10b_komplett.json` |
| `Rückmeldungen Grundlagen Klasse 8-9.html` | Auswertung je Nummer + Klassenbild |
| `Praesentation.html` | Beamer-Ansicht für die Klasse (nur Klassenwerte) |
| `Schnipsel Grundlagen Klasse 8-9.pdf` | 3 Seiten, 10 Zettel je Seite, zum Austeilen |
| `Verlauf.html` / `verlauf.json` | Zeitreihe je Nummer über das Schuljahr |

Neu erzeugen nach einer Korrektur:

```bash
python3 baue_json.py
python3 ../../../../../.scripts/grundlagen_check_bericht.py ergebnisse_10b_komplett.json .
python3 ../../../../../.scripts/grundlagen_check_praesentation.py ergebnisse_10b_komplett.json . 10b
python3 ../../../../../.scripts/grundlagen_check_schnipsel.py ergebnisse_10b_komplett.json .
```

## Ergebnis in Kürze

208 von 567 Einzelantworten richtig (37 %). Nach Block, über alle Bögen
gerechnet (leere Kästchen zählen als nicht gekonnt):

- A · Terme und Gleichungen: 49 %
- C · Potenzen und Wurzeln: 44 %
- B · Lineare Funktionen: 31 %
- D · Pythagoras und Wahrscheinlichkeit: 16 %

Die Präsentation rechnet bewusst anders – dort zählen nur die tatsächlich
bearbeiteten Aufgaben (A 65 %, B 69 %, C 69 %, D 40 %). Der Unterschied
zwischen beiden Zahlen ist der eigentliche Befund: Block B und D wurden
großteils gar nicht erst angefasst.

**A und B sind gleich schwer ausgefallen:** Version A 36 %, Version B 38 %.
Der A/B-Standard verzerrt das Ergebnis also nicht.

## Offene Punkte aus dem Scan

- **Nummer 15 fehlt** – kein Bogen im Scan.
- **Nummer 24**: im Kopf ist B markiert, alle Antworten sind eindeutig A.
  Als A gewertet.
- **Nummer 6, 19, 5**: kein Versionskreuz im Kopf, Version aus den Antworten
  erschlossen (siehe `VERSIONEN_ERSCHLOSSEN`).
- `TERME_MANUELL` listet 11 Antworten, die mathematisch richtig oder fast
  richtig sind, vom Stringvergleich aber als falsch gezählt werden – vor dem
  Gespräch mit der Klasse kurz durchsehen.

## Fürs nächste Mal

- Im Kopf des Antwortbogens die Versionskreuze deutlicher machen oder vor
  dem Einsammeln einmal durchgehen. Drei fehlende Kreuze bei 27 Bögen.
- Bei C1 steht „Schreibe zuerst als eine Potenz" – mehrere Bögen sind bei der
  Potenz stehen geblieben und haben nicht ausgerechnet. Formulierung schärfen.
- Bei D2 Prozent oder Bruch explizit zulassen; beides kam vor.
