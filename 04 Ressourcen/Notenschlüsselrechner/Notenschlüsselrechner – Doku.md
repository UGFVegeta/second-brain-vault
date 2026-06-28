---
tags: [ressource, tool, noten, bewertung]
status: aktiv
date: 2026-06-17
---

# Notenschlüsselrechner (linear)

Eigenständige Browser-Apps (offline, ohne Internet) für Notenschlüssel. Per Doppelklick im Browser öffnen.

**Drei Werkzeuge:**
- [[Notenschlüsselrechner.html]] – schlicht. Oben **Umschalter**: „Freier Schlüssel" (kaufmännisch) ↔ „Realschulprüfung Mathematik" (amtlich, gesperrt).
- [[Notenschlüsselrechner GDRS.html]] – derselbe Rechner inkl. Umschalter im GDRS-Design.
- [[Notenschlüssel Realschulprüfung BW.html]] – **eigenes Tool nur für die Abschlussprüfung**, amtliche Rundung fest verdrahtet, kein Umschalter → eindeutig zum Weitergeben an Kollegen.

Im Modus „Realschulprüfung Mathematik" werden die Skalen-/Punkte-Felder gesperrt und auf den amtlichen Schlüssel gesetzt (50 P., Zehntelnoten, Abrundung zugunsten). Zurück auf „Freier Schlüssel" entsperrt wieder alles.

## Was die App kann

- **Schritt 1 – Notenskala:** beste/schlechteste Note frei wählbar; Notenschritt für die Tabelle (ganze, halbe, Viertel-, Zehntelnoten)
- **Schritt 2 – Punkte:** maximale Punktzahl + „Beste Note vergeben ab" (Punkt-Schwelle/Sockel); optional harter unterer Sockel
- **Ausgabe:** Einzelabfrage (Punkte → Note), Notenspiegel (Schwellen), volle Punkte-Noten-Tabelle, Drucken/PDF, CSV-Export

## Formel

Linearer Schlüssel, zwischen oberem Anker („Beste Note vergeben ab") und unterem Anker (0 Punkte bzw. „Schlechteste Note bis") wird linear interpoliert:

```
Note = beste Note + (schlechteste − beste) × (Schwelle − P) / (Schwelle − unterer Anker)
```

Beispiel (max 39, beste 1 ab 39, schlechteste 6 bei 0):

```
Note = 1 + 5 × (39 − P) / 39
```

Rundung: **kaufmännisch (½ aufrundend)** auf den gewählten Notenschritt.

## Verifikation

Am **17.06.2026** gegen eine Referenztabelle geprüft (max = 39 Punkte, Zehntelnoten, 0,5er-Schritte): **alle 48 Zeilen identisch** – von `39 → 1` über `23,5 → 3` und `15,5 → 4` bis `0 → 6`. Formel und Rundung stimmen exakt überein.

## Tool „Realschulprüfung BW"

Eigenständige Datei [[Notenschlüssel Realschulprüfung BW.html]] – nur Maximalpunktzahl eingeben (Mathematik: 50), sonst nichts einstellbar. Verwendet **fest** den amtlichen Schlüssel der schriftlichen Realschulabschlussprüfung BW (Zehntelnoten). Unterschied zur freien Variante: Es wird **nicht kaufmännisch gerundet, sondern auf die nächste Zehntelnote abgerundet** (zugunsten der Schüler):

```
Note = abrunden_auf_0,1( 1 + 5 × (Max − P) / Max ),  begrenzt auf 1,0 … 6,0
```

Beispiel: 49,5 Punkte → exakt 1,05 → amtlich **1,0** (kaufmännisch wäre es 1,1). Am 17.06.2026 gegen die amtliche Tabelle (Mathematik 2026, 50 P.) geprüft: alle Stichproben identisch.

## Diese Referenztabelle reproduzieren

In der App einstellen: Maximale Punktzahl **39**, Notenschritt **Zehntelnoten**, Punkte-Schritt **0,5**.
