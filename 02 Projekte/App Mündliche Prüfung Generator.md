---
tags: [projekt, mathematik, app, pruefung]
status: aktiv
date: 2026-06-20
updated: 2026-07-05
---

# App: Generator mündliche Prüfung (Mathematik)

> [!success] Status
> **Fertig (Beta).** App läuft als HTML-Datei, 125 Aufgaben in 7 Themen. Kollegenanleitung erstellt: [[02 Projekte/Mündliche Prüfung App - Anleitung für Kollegen]]
>
> **Update 2026-07-05:** Eintippbare Felder für **Vorname** und **Zielnote** – erscheinen auf beiden Ausdrucken, damit klar ist welche gedruckte Prüfung zu wem gehört. Im Zufallsgenerator (`Pruefung.html`) direkt in der Kopfzeile jedes Satzes, im Baukasten (`Baukasten.html`) als zwei Felder in der Werkzeugleiste neben den Druck-Buttons. Eingaben werden nicht gespeichert (Datenschutz).
>
> **Update 2026-07-02:** Zufallsgenerator überarbeitet – Themen-Balance (5 gemischte aus 5 verschiedenen Themen, aufsteigend sortiert), Schwierigkeitsprofil „⚖️ ausgewogen" (2·★, 2·★★, 2·★★★), Serien-Modus (bis 10 überschneidungsfreie Sätze auf einmal, je Satz eigene Druckseite mit Name/Datum-Zeile) und verwendet-Abgleich mit dem Baukasten (gemeinsamer Speicher, „✓ Satz als verwendet markieren"). Details in [[04 Ressourcen/Mathematik/Prüfungsaufgaben/Generator/ANLEITUNG.md]].

## Vision

Eine App, die automatisch eine **mündliche Mathe-Prüfung** zusammenstellt – aus mehreren Themen gemischt und gefiltert nach **Schwierigkeit / Notenstufe**. Auf Knopfdruck eine ausgewogene, individuelle Prüfung pro Schüler, statt sie von Hand zusammenzuklicken.

## Die 6 Themen

1. Stochastik
2. Trigonometrie
3. Stereometrie
4. Sachrechnen
5. Boxplot
6. Quadratische Funktionen

## Datenbasis (vollständig)

Alle 7 Pools sind aufgebaut (125 Aufgaben, Stand 2026-07-02): Trigonometrie (20), Quadratische Funktionen (20), Stochastik (20), Sachrechnen (15), Boxplot & Datenanalyse (15), Stereometrie (15), Kurzaufgaben/Zeitfüller (20). Jeweils als `.md` (Bild + eingeklappte Lösung, z.B. [[04 Ressourcen/Mathematik/Prüfungsaufgaben/Trigonometrie Prüfungspool.md]]) und als HTML-Pool, Bilder im Ordner `Bilder/`. Aktuelle Zahlen stehen immer in der Tabelle in [[04 Ressourcen/Mathematik/Prüfungsaufgaben/Generator/ANLEITUNG.md]].

## Kernerkenntnis / wichtigster Vorarbeitsschritt

Die eigentliche Arbeit ist **nicht das Programmieren**, sondern das **strukturierte Taggen des Aufgabenpools.** Aktuell liegen Aufgaben als Bild + Fließtext-Lösung – nicht maschinen-filterbar.

Pro Aufgabe brauchen wir Metadaten, z.B.:

```
Thema: Trigonometrie | Untertyp: Kosinussatz | Schwierigkeit: 3/5 | Notenbereich: 2-3 | Bild: Trig-Aufgabe-01.png
```

Sobald die Daten strukturiert sind, ist die App fast nur noch: Auswahl + Würfeln + Zusammenstellen.

## Mögliche Schritte (wenn es soweit ist)

1. Datenmodell festlegen (Felder: Thema, Untertyp, Schwierigkeit, Notenbereich, Bild, Lösung)
2. Bestehende Pools schrittweise mit Metadaten anreichern (geht auch ganz ohne App, direkt im Vault)
3. Fehlende Themen-Pools aufbauen
4. App bauen – guter Anlass für ein Spec-Driven-Framework (GSD light / Superpowers)

## Werkzeug-Notiz

Für die Umsetzung wäre **GSD** (`open-gsd/gsd-core`, leichtgewichtig) ein guter Einstieg, alternativ Superpowers (umfangreicher). Siehe Gespräch vom 2026-06-20.
