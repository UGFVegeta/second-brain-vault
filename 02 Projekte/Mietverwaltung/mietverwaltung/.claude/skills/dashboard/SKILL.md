---
name: dashboard
description: Baut das Dashboard neu und erklärt die Zahlen darin. Nutze diesen Skill bei „Dashboard", „Übersicht", „wie steht es", „Stand der Mieten", „Auswertung" oder immer dann, wenn sich Daten geändert haben.
---

# Dashboard bauen und erklären

## Bauen

```
py -3 skripte\dashboard_bauen.py
```

Das erzeugt `Dashboard.html` im Hauptordner. Danach die Datei öffnen:

```
start Dashboard.html
```

Nach jeder Datenänderung neu bauen, sonst zeigt die Datei einen alten Stand.
Das Dashboard rechnet nichts selbst, es stellt nur dar, was in `daten\` steht.

## Was drinsteht

- **Kopfzahlen**: Sollmiete pro Monat, Eingänge des laufenden Monats, offener
  Betrag, Verhältnis vermietete zu vorhandenen Einheiten.
- **Zahlungsstatus**: laufender Monat je Mietverhältnis.
- **Rückstände**: offene Monate der letzten zwölf, aber nur für den Zeitraum,
  für den auch Kontoumsätze vorliegen.
- **Zu prüfen**: Eingänge, die nicht sicher zugeordnet werden konnten.
- **Mieteingänge**: Monatsverlauf des laufenden Jahres.
- **Ausgaben**: nach Kategorie, Grundlage für die Werbungskosten.
- **Darlehen**: Restschuld und Zinsbindung, Warnung unter 18 Monaten Restlaufzeit.
- **Fristen**: was in den nächsten Monaten ansteht.

## Beim Erklären

Nur zählen, was gezählt werden darf. Als bezahlt gilt eine Miete, wenn die
Zuordnung sicher war oder jemand sie bestätigt hat. Ein unbestätigter
Vorschlag zählt nicht mit, sonst gilt eine Miete als eingegangen, die niemand
geprüft hat.

Fehlen Monate im Rückstandsblock, liegt das meist nicht an unbezahlten Mieten,
sondern an fehlenden Kontodaten. Das gehört dazugesagt.

Der Knopf „Belegliste herunterladen" erzeugt eine CSV aller Buchungen des
laufenden Jahres. Das ist die einzige Funktion im Dashboard, die etwas tut,
und sie funktioniert wirklich. Alles andere im Dashboard ist Anzeige.
