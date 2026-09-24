---
tags: [ressource, physik, unterricht, klasse7, optik, interaktiv]
status: aktiv
date: 2026-09-24
---

# Optik-Labore

Interaktive Unterrichtsseiten im Stil des [[Schattenlabor Halbschatten|Schattenlabors]], eine pro Leitfrage. Zum Zeigen im Unterricht (was im Versuch nicht geht) und als Link für die Schüler zu Hause.

**Startseite:** [Optik-Labore.html](<Optik-Labore.html>) verlinkt alle vier Labore.

| Leitfrage | Labor | Inhalt |
|---|---|---|
| 1 Warum sehen wir überhaupt etwas? | [Sehlabor](<Sehlabor Lichtquellen.html>) | Lampe an/aus, Sender und Empfänger, Sehstrahl-Fehlvorstellung, Lichtquellen zuordnen, Fußgänger nachts (Kleidung, Abstand) |
| 2 Was passiert mit dem Licht, wenn es auf einen Körper trifft? | [Körperlabor](<Körperlabor Licht trifft auf Körper.html>) | Versuch W04 nachgestellt, sieben Körper mit Anteilen Streuung/Absorption/Transmission, raue vs. glatte Fläche |
| 3 Warum können wir nicht um die Ecke sehen? | [Strahlenlabor](<Strahlenlabor Lichtausbreitung.html>) | Ball hinter Mauer, Versuch W05 mit ein oder zwei Blenden, Spalt und Lichtbündel, Lichtstrahlenmodell, Nebel, Verkehrsspiegel |
| 4 Warum hat ein Schatten manchmal weiche Ränder? | [Schattenlabor](<Schattenlabor Halbschatten.html>) | zwei Lichtpunkte, Kern- und Halbschatten mit Reglern, Finsternisse als Ausblick |

Jedes Labor hat Kurz-Check, Zusammenfassung mit den Merksätzen der Folien und ein „Probier's aus“ (keine Hausaufgabe). Taste **L** blendet Hinweise für die Lehrkraft ein, **F** schaltet Vollbild, `#s3` am Ende der Adresse springt zu Folie 3.

## Technik

- Generator: `baue_labore.py`, Quellcode in `labore-quelle/` (`shell.js` = gemeinsamer Rahmen, je Labor eine JS-Datei). Das Schattenlabor ist eine eigene Datei und wird nur bei den Schriften angepasst.
- Schriften (Bricolage Grotesque, Source Sans 3, IBM Plex Mono, OFL) liegen in `assets/fonts/` und werden eingebettet. Die Seiten laden nichts nach und laufen offline, beim Öffnen über einen Schülerlink geht also keine IP-Adresse an Google.
- iCloud: `GDRS ICloud/Physik/Physik Klasse 7/Optik 2026-27/Labore/`. Die Stunden-HTMLs F2–F4 verlinken dorthin.
- Anteile im Körperlabor sind grobe Richtwerte (weißes Papier ≈ 80 % Streuung, schwarzer Karton ≈ 5 %, Glas ≈ 90 % Transmission).

## Für Schüler freigeben

Offen: über welche Plattform. Die Dateien sind eigenständige HTML-Seiten. H5P kann solche Seiten nur über den Inhaltstyp „Iframe Embedder“ einbinden, und der erlaubt HTML-Uploads erst, wenn der Admin sie freischaltet. Einfacher ist ein Link auf die Datei in der schulischen Lernplattform.
