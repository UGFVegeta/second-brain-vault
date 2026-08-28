---
name: umsaetze-importieren
description: Liest Kontoauszüge ein, ordnet Zahlungen den Mietverhältnissen zu und klärt unklare Fälle im Gespräch. Nutze diesen Skill bei „Kontoauszug einlesen", „Umsätze importieren", „neue Zahlungen", „Zuordnungen prüfen", „wer hat bezahlt" oder wenn im Dashboard Einträge unter „Zu prüfen" stehen.
---

# Kontoumsätze einlesen und zuordnen

## Ablauf

1. Fragen, wo die Exportdatei liegt. Üblicher Weg: im Online-Banking die
   Umsätze als CSV exportieren und in den Ordner `kontoauszuege\` legen.
2. `py -3 skripte\umsaetze_importieren.py` ausführen. Ohne Argument liest es
   alles aus `kontoauszuege\`, mit Dateipfad nur diese eine Datei.
3. Das Skript meldet, wie viele Buchungen eindeutig zugeordnet wurden und
   welche offen sind. Doppelte Buchungen werden automatisch erkannt, derselbe
   Export darf also gefahrlos mehrfach eingelesen werden.
4. Die offenen Fälle gemeinsam durchgehen (siehe unten).
5. `py -3 skripte\dashboard_bauen.py` und Ergebnis zeigen.

## Wenn die Bank ein unbekanntes Format liefert

Das Skript erkennt die Spalten anhand der Überschriften und deckt damit die
gängigen Banken ab. Kommt trotzdem ein Fehler „finde keine Spalten für Datum
und Betrag", dann öffne die ersten Zeilen der Datei, schau dir die
Überschriften an und ergänze sie in `skripte\umsaetze_importieren.py` in der
Tabelle `SPALTEN`. Das ist eine Zeile Arbeit, keine Umbauaktion.

## Unklare Zuordnungen klären

Buchungen mit Status `vorschlag` oder `unklar` musst du mit dem Vermieter
klären. Zeig sie einzeln mit Datum, Betrag, Absender und Verwendungszweck und
frag, zu wem sie gehören.

Wenn die Antwort feststeht, trag in `daten/zahlungen.json` bei der Buchung ein:

```json
"mv_id": "mv-003",
"monat": "2026-08",
"bestaetigt": true
```

`"bestaetigt": true` ist wichtig: Damit rührt die automatische Zuordnung diese
Buchung nie wieder an, auch beim nächsten Import nicht.

Bei Ausgaben stattdessen eine Kategorie setzen, die in der Anlage V
weiterverwendbar ist:

```json
"kategorie": "Instandhaltung"
```

Übliche Kategorien: Instandhaltung, Verwaltung, Versicherung, Grundsteuer,
Betriebskosten, Zinsen, Tilgung, Sonstiges. Tilgung ist steuerlich keine
Werbungskost, Zinsen schon. Halte die beiden deshalb auseinander.

## Wiederkehrende Fälle dauerhaft lösen

Taucht derselbe Mieter immer wieder als unklar auf, liegt meist die IBAN nicht
im Mietverhältnis. Trag sie in `daten/mietverhaeltnisse.json` unter
`iban_mieter` nach, dann ist der Fall für immer erledigt.

Zahlt jemand regelmäßig vom Konto des Partners, gehört diese IBAN ins Feld
`iban_mieter` oder als zweite IBAN in `notizen` mit einem Hinweis.

## Was du nicht tun sollst

Zahlungsstände nicht von Hand in Ordnung bringen, indem du Beträge anpasst.
Wenn die Zahlen nicht stimmen, stimmt entweder die Sollmiete nicht oder es
fehlt eine Buchung. Beides klärt sich mit einer Rückfrage, nicht durch
Nachbessern in der Datei.
