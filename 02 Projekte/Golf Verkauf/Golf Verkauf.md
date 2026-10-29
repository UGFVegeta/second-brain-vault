---
tags: [auto, familie, verkauf]
status: aktiv
date: 2026-10-26
---

# Golf 6 TDI verkaufen

Alles zum Verkauf des Golf 6 auf einen Blick. Fahrzeugdaten: [[Golf 6 Fahrzeugdaten]]. Hintergrund: [[BMW iX1 Auslieferung]], [[E-Fahrzeug Leasing finden]].

## Stand

- 26.10.2026: Inserat auf mobile.de online (Inseratsnummer 52872319159616). Zusätzlich gibt es ein eigenes Kleinanzeigen-Inserat über Julias Kleinanzeigen-Konto, dessen Nachrichten nicht in Oskars web.de-Postfach ankommen. Sie werden per Chrome abgelesen und von Hand in `kleinanzeigen.json` eingetragen, das Skript baut sie in die Übersicht ein. Nur gelegentlich spiegelt mobile.de eine Kleinanzeigen-Anfrage als Mail. AutoScout24: kein Inserat eingestellt.
- Erste Anfragen am Abend des 26.10. Anruf bei einem Interessenten ist für 27.10. um 9 Uhr vereinbart (Erinnerung 8:55 Uhr in Apple Erinnerungen, Liste Inbox).

## Preis

- Angebotspreis **5.500 € VB**. Untergrenze für Oskar: **4.500 €** (nicht nennen).
- Copart-Price-Finder vom 22.10.2026 (PDF in den Downloads): Durchschnitt 5.581 €, DAT Händler-Verkaufswert 5.259 €, ermittelter Verkaufswert 5.030 €, Händler-Einkaufswert 4.006 €.
- Zum Vergleich der Händlerankauf bei wirkaufendeinauto.de. Deren Mail vom 25.10. nannte den damaligen Preis als „gilt nur noch heute".

## Fahrzeug im Inserat

- VW Golf 6 2.0 TDI Style, 5-türig, 103 kW, Erstzulassung 11/2011, 6-Gang-Schaltgetriebe, Euro 5.
- 214.854 km (Stand 19.10., vor dem Einstellen am Tacho prüfen). Zahnriemen neu mit Rechnung, HU bis 07/2027, unfallfrei, Nichtraucher, zwei Vorbesitzer, zwei Schlüssel.
- **Keine Anhängerkupplung.** Die Anhängelast im Schein gilt nur für den Typ. Ein früherer Entwurf hatte das falsch.
- Im Kaufpreis: Thule Dachträger und vier Winterreifen, aufgezogen sind Sommerreifen.
- Alufelgen sind vorhanden, im Kleinanzeigen-Formular muss das Häkchen gesetzt werden. Scheckheft nur bei lückenlosem Nachweis anhaken.

## Dateien

- Anzeigentexte: [[Anzeigentext mobile.de und AutoScout24]] und [[Anzeigentext Kleinanzeigen]] (gleicher Inhalt, nur anders formatiert).
- Fotos: `~/Downloads/Golf Verkauf/Upload/`, 17 Bilder in Upload-Reihenfolge, Kennzeichen verpixelt, ohne Standortdaten.
- Anfragen-Übersicht: `Anfragen.html` in diesem Ordner, siehe unten.

## Anfragen-Übersicht (automatisch)

`.scripts/golf_anfragen.py` liest das web.de-Postfach nur lesend, gruppiert die Mails von kontakt.mobile.de pro Interessent und baut `Anfragen.html`. Die Anfragen landen im web.de-Ordner „Unbekannt", nicht im Posteingang. Der LaunchAgent `com.oskar.golf-anfragen` läuft alle 15 Minuten (Log: `~/Library/Logs/golf-anfragen.log`). Die HTML-Datei enthält Namen und Telefonnummern der Interessenten und ist deshalb gitignored, sie kommt nicht ins GitHub-Backup. In diese Notiz gehören keine Namen oder Nummern.

Manuell neu bauen:

```bash
python3 .scripts/golf_anfragen.py --text
```

## Ablauf mit Interessenten

- Nummer beim Anruf mit `#31#` vor der Rufnummer unterdrücken. Die eigene Nummer erst weitergeben, wenn ein Termin steht.
- Besichtigung und Probefahrt vor Ort, Oskar fährt mit. Ausweis zeigen lassen, Name und Anschrift notieren.
- Zahlung bar bei Übergabe oder als Überweisung, die schon auf dem Konto ist. Schlüssel erst danach.
- Kaufvertrag: ADAC-Muster für den Privatkauf, Sachmängelhaftung ausgeschlossen, Zubehör (Thule, Winterreifen, Schlüssel, Zahnriemen-Rechnung) eintragen, zwei Ausfertigungen.
- Warnzeichen: Kauf ohne Besichtigung, Anzahlung vorab, Spediteur holt ab, Preis über Angebot.

## Offen

- [ ] Winterreifen und Thule-Modell im Inserat ggf. genauer benennen
- [ ] Tachostand vor dem Einstellen aktualisieren
- [ ] Nach Verkauf: Inserate löschen, Abmeldung, Versicherung, Verkaufsnachweis
