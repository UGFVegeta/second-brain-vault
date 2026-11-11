---
tags: [sport, unterricht, arbeitsblatt]
status: aktiv
date: 2026-11-10
---

# Aufgabenblätter Nichtteilnahme

Aufgabenblätter für Schüler, die wegen Verletzung oder Erkältung im Sportunterricht anwesend sind, aber nicht mitmachen. Absprache der Sportfachschaft. Das ist keine Strafe, anders als der [[Abschreibtext Sportsachen vergessen]].

## Absprachen (Stand 10.11.2026)

- Format: ein A4-Blatt doppelseitig. Vorderseite Infotext, Rückseite Aufgaben ○ ◐ ●. Kein Handy, kein Internet, also steht alles nötige Wissen auf dem Blatt.
- Dauer etwa 50 Minuten (Doppelstunde). Niemand muss alles schaffen, ○-Aufgaben zuerst.
- Nur wenige Bilder, weil Platz für Info wichtiger ist. Bilder bei Bedarf aus Gemini (Oskar erzeugt sie), sonst einfache eigene Grafiken.
- Ordner in der Sporthalle nach Stufen: Klasse 5 und 6, Klasse 7 und 8, Klasse 9 und 10.
- Je Thema und Stufe mindestens drei verschiedene Blätter mit eigenem Schwerpunkt, damit es Auswahl gibt.
- Lehrkräfte sammeln die Blätter ein, es gibt keine Note.
- Lösung ist dasselbe Blatt ausgefüllt (Magenta).
- Keine Beobachtungsaufgaben (nichts, was voraussetzt, dass der Schüler das Spiel in der Halle verfolgt). Entschieden 10.11.2026.
- Blätter voll ausnutzen, schmale Ränder. Bei den Älteren (7/8 und besonders 9/10) wenig Ankreuzen, überwiegend Aufgaben, bei denen sie Text schreiben, dazu ein ausführlicher Infotext. Die sollen beschäftigt sein. (Oskar 10.11.2026)

## Durchschauen

`Übersicht.html` im Ordner (auch in iCloud): Stufe oben wählen, Blatt links anklicken, Vorder- und Rückseite nebeneinander. Pfeiltasten blättern, L schaltet die Lösung um, Klick aufs Bild öffnet das PDF. Die Vorschaubilder liegen in `_Vorschau/` (nicht im Git, werden vom Skript neu erzeugt).

## Themen (geplant)

1. Essen und Trinken
2. Fair Play und Verhalten
3. Herz, Puls und Ausdauer
4. Training und Erholung (Trainingsprinzipien, Schlaf)
5. Verletzungen vermeiden und richtig reagieren (Aufwärmen, Helfen und Sichern, PECH-Regel)
6. Regeln und Spielfeld (Sportart je nach Stufe)

## Stand (10.11.2026: 55 Blätter, je mit Lösung)

| Thema | Klasse 5 und 6 | Klasse 7 und 8 | Klasse 9 und 10 |
|---|---|---|---|
| Essen und Trinken | Was auf den Teller gehört; Trinken beim Sport; Energie für den Sport | Energie und Energiebedarf; Nährwerte lesen; Trinken und Sportgetränke | Energiebilanz; Ernährung für Sportler; Körperbild und Diäten |
| Fair Play | Was ist Fair Play; Gewinnen und verlieren; Miteinander im Team | Formelle und informelle Fairness; Schiedsrichter sein; Streit lösen | Doping; Respekt und Zivilcourage; Sportwetten und Spielmanipulation (ersetzt Inklusion und Paralympics) |
| Herz, Puls und Ausdauer | Dein Herz und dein Puls; Ausdauer; Was beim Rennen im Körper passiert | Herz und Kreislauf; Pulsbereiche; Coopertest verstehen | Energie für die Muskeln; Ausdauertraining planen; Anpassungen durch Training |
| Training und Erholung | Schlaf, deine Ladestation; Üben macht stärker; Bewegung und Erholung | Die motorischen Fähigkeiten; Trainingsprinzipien; Schlaf und Erholung | Krafttraining; Regeneration und Stress; Trainingsplanung |
| Verletzungen vermeiden | Aufwärmen; Sicher in der Halle; Wenn etwas passiert (PECH) | Sportverletzungen erkennen; Erste Hilfe und Notruf; Helfen und Sichern | Muskeln, Sehnen, Bänder; Erste Hilfe im Notfall; Vorbeugen |
| Regeln und Spielfeld | Handball, das Spielfeld; Handball, die Regeln; Werfen und Fangen | Basketball; Badminton; Fußball; Handball (Positionen, Abwehr, Regeln) | Volleyball, Regeln; Volleyball, Technik und Spiel; Leichtathletik, Wettkampfregeln |

Die Sportarten bei „Regeln und Spielfeld“ folgen dem Fachschafts-Curriculum (Kl. 6 Handball, Kl. 7/8 Basketball, Badminton, Fußball, Kl. 9/10 Volleyball, Kugelstoßen).
Einige Zahlen sind gerundete Richtwerte (Zucker in Getränken, Energieverbrauch, Nährwerte als Beispiel), auf den Blättern mit „etwa“ gekennzeichnet.

## Ablage und Bauen

- Vault: dieser Ordner, Unterordner `Klasse 5 und 6/<Thema>/` mit Schülerfassung und Lösung als PDF.
- iCloud: `GDRS ICloud/Schuljahr 26 27/Sport/Aufgabenblätter Nichtteilnahme/`, gleiche Struktur. Das Skript kopiert automatisch dorthin.
- Skript: `_Skripte/baue_blaetter.py` (HTML, dann PDF per Chrome headless), Inhalte in `stufe56.py`, `stufe78.py`, `stufe910.py` (Essen und Trinken 5/6 direkt in `baue_blaetter.py`). Aufruf mit Filter, z. B. `python3 baue_blaetter.py "Klasse 7 und 8"`.
- Das Skript wählt je Blatt die größte Schrift, bei der beide Seiten passen (5/6 bis 12,4 pt, 7/8 bis 11,6 pt, 9/10 bis 11,2 pt), und meldet den Füllstand je Seite.
