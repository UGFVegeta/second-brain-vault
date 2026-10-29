---
tags: [vorlage, planer, schule]
status: aktiv
date: 2026-10-28
---

# Planer (analoge Mappe)

A4-Dokumentmappe oder Ringordner mit Register, gebaut aus den [[04 Ressourcen/Meeting-Vorlagen/Meeting-Vorlagen|Meeting-Vorlagen]]. Datei: `Planer – Druckset.pdf` (32 Seiten, doppelseitig drucken, Rückseiten sind dotted oder leer).

| Register | Inhalt |
|---|---|
| Vorne | Deckblatt, Inhaltsverzeichnis, Rückseite: eigenes Verzeichnis (Datum, Register, Thema) |
| 1 Planung | Wochenplan, Tagesplan (mit Befinden und Schlaf), To-do-Liste |
| 2 Konferenzen | Notizen Konferenz |
| 3 Gespräche | Notizen Gespräch zu zweit |
| 4 Mentoring | Notizen Mentoring-Gespräch |
| 5 Projekte | Projektseite |
| 6 Notizen | Dots-Seite |

Jedes Register hat ein Trennblatt mit Reiter am rechten Rand (Lochung links). Reiter auf festerem Papier drucken oder gekaufte Register zusätzlich nutzen.

## A5-Fassung

`Planer – Druckset A5.pdf` ist ein eigenes A5-Layout (nicht skaliert): Schreibzeilen etwa 7 mm, Heftrand links 17 mm, auf Rückseiten gespiegelt. Gleiche Register und Seiten wie in A4. Die Lochung ist nicht eingedruckt; Löcher stanzen oder Papier in der Mappe lochen. Skript: `.scripts/planer_a5.py`.

## Neu bauen (A4)

```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/planer_bauen.py
```

Skript: `.scripts/planer_bauen.py`, nutzt `.scripts/meeting_vorlagen.py`.

## Datenschutz

Nur leere Vorlagen im Vault. Ausgefüllte Seiten mit Namen nicht ablegen, auch nicht als Foto.

## Tagesblatt (Vorderseite der Mappe)

Ein A4-Blatt pro Tag: Heute (Arbeitstermine, To-dos, Eingang), Morgen (am Freitag der Montag), Rückseite mit Dots, Feierabend, „Warte auf“ und Skizzenfeld. Vorderseite liniert, Rückseite Dots. Nur Arbeit: Kalender Arbeit, Schule, Jahresterminplanung / DieWo; To-dos aus der Erinnerungen-Liste „Schule“. Kein Unterricht, kein Befinden.

**Morgens:** Dashboard-Dienst starten (`04 Ressourcen/Dashboard-Dienst starten.command`), Lebens-Dashboard öffnen, Karte „Tagesblatt“: Termine prüfen („Sind alle drin?“), Fehlendes ergänzen, „Tagesblatt erzeugen“. Das PDF öffnet sich in Vorschau, doppelseitig drucken (Wenden an der langen Kante). Ablage: `~/Documents/Tagesblatt/` (außerhalb des Vaults, weil Namen drinstehen können).

**Abends:** Foto vom Blatt an Claude, Skill `tagesblatt-abgleich`: Erledigtes abhaken, Eingang in Erinnerungen und Kalender übertragen, Verschobenes neu terminieren. Claude zeigt erst den Vorschlag, schreibt nach Freigabe. Auf dem Blatt nur Kürzel oder Funktionen, keine Klarnamen (der Namensschutz deckt Bilder nicht ab).

Skripte: `.scripts/tagesblatt.py` (Blatt), `.scripts/dashboard_server.py` (Schnittstelle fürs Dashboard), `.scripts/tagesblatt_abgleich.py` (Erinnerungen/Kalender schreiben). Beispiele: `Beispiel Tagesblatt 2026-11-02 linien.pdf`, Vergleich der Stile in `Tagesblatt Varianten.html`.
