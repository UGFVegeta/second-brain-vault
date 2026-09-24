---
tags: [ressource, physik, unterricht, klasse7, optik, halbschatten, interaktiv]
status: aktiv
date: 2026-09-24
fach: Physik
klasse: 7 Realschule
thema: Optik I – Kern- und Halbschatten
---

# Schattenlabor: Kern- und Halbschatten

Animierte, interaktive Unterrichtsseite zu Leitfrage 4 **„Warum hat ein Schatten manchmal weiche Ränder?“** (Stoffverteilungsplan Klasse 7, W06 und W07, Bildungsplan 3.1.3 (3)).

**Datei:** [Schattenlabor Halbschatten.html](<Schattenlabor Halbschatten.html>) (im Browser öffnen, eine einzelne Datei ohne Build-Schritt)

Ergänzt die Folien `Optik I` und die Stunde `Optik – Leitfrage 4 – Stunde.html`. Passt als Einstieg oder Sicherung, ersetzt aber nicht das Paar-Prinzip (Arbeitsseite leer, Vorlagenseite gefüllt) fürs Notability-Tafelbild.

## Ablauf (9 Folien)

1. Einstieg: Hand über dem Tisch, scharfer und weicher Schattenrand, Vermutungen sammeln
2. Licht breitet sich geradlinig aus (punktförmige Lichtquelle, scharfer Schatten)
3. Zwei Lichtpunkte A und B: zwei Schatten, Überlappung = kein Licht
4. Kernschatten, Halbschatten, voll beleuchteter Bereich
5. Experiment mit Reglern (Lampengröße, Abstand Lampe–Gegenstand, Abstand Gegenstand–Wand), Breiten live in cm, Je-desto-Regeln per Klick
6. Alltag: vier Schatten im Stadion (Flutlicht, Buchidee S. 35), Spieler verschiebbar, Lupe mit Schattenlängen
7. Anwendung: Sonnen- und Mondfinsternis (Kernschatten, Halbschatten, nicht maßstabsgetreu)
8. Kurz-Check mit 4 Fragen und Sofort-Rückmeldung
9. Zusammenfassung und „Probier's aus“

## Bedienung

- Pfeiltasten oder Buttons: weiter und zurück
- **F**: Vollbild
- **L**: Hinweise für die Lehrkraft ein- und ausblenden
- Sprungmarke: `#s5` am Ende der Adresse öffnet direkt Folie 5

## Merksätze

- Eine punktförmige Lichtquelle wirft nur einen Kernschatten mit scharfem Rand.
- Eine ausgedehnte Lichtquelle wirft Kernschatten und Halbschatten.
- Je größer die Lampe und je weiter die Wand vom Gegenstand entfernt ist, desto breiter der Halbschatten.

## Technik

- Schatten werden aus den Randstrahlen berechnet (Funktion `geom()`, 1 Einheit = 0,1 cm), die Zeichnung ist ein SVG (`build()`), die Folien stehen im Array `scenes`.
- Schriften sind seit 24.09.2026 eingebettet (keine Google-Anfragen, läuft offline). Begriffe an Folien angeglichen (Körper, Schirm), Hausaufgabe entfernt, letzte Folie heißt „Zusammenfassung“ mit „Probier's aus“.
- Gehört zu den [[Optik-Labore]]n (Sehlabor, Körperlabor, Strahlenlabor, Schattenlabor).
- Ausgangsversion als Artifact: https://claude.ai/artifact/WijdaccDkExrD7H62PdrJr

## Ideen zum Weiterbauen

- [ ] Folie zur Mondfinsternis (Erde wirft Schatten auf den Mond)
- [ ] Arbeitsblatt mit Randstrahlen-Konstruktion zum Nachzeichnen
- [ ] Einbindung in Bildungs-Dashboard (`.scripts/bildungs_dashboard_bauen.py`)
