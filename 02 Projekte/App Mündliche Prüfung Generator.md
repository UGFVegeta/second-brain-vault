---
tags: [projekt, idee, mathematik, app, pruefung]
status: idee
date: 2026-06-20
---

# App: Generator mündliche Prüfung (Mathematik)

> [!note] Status
> Idee / Backlog – **nicht nahe Zukunft.** Festgehalten am 2026-06-20, damit die Vision nicht verloren geht.

## Vision

Eine App, die automatisch eine **mündliche Mathe-Prüfung** zusammenstellt – aus mehreren Themen gemischt und gefiltert nach **Schwierigkeit / Notenstufe**. Auf Knopfdruck eine ausgewogene, individuelle Prüfung pro Schüler, statt sie von Hand zusammenzuklicken.

## Die 6 Themen

1. Stochastik
2. Trigonometrie
3. Stereometrie
4. Sachrechnen
5. Boxplot
6. Quadratische Funktionen

## Datenbasis (schon vorhanden)

- [[04 Ressourcen/Mathematik Prüfungsaufgaben/Trigonometrie Prüfungspool.md]] – Aufgaben als Bild + eingeklappte Lösung
- [[04 Ressourcen/Mathematik Prüfungsaufgaben/Stochastik Aufgabenpool.md]]
- HTML-Versionen vorhanden, Bilder im Ordner `Bilder/`
- Übrige Themen (Stereometrie, Sachrechnen, Boxplot, quadratische Funktionen) müssen noch als Pool aufgebaut werden.

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
