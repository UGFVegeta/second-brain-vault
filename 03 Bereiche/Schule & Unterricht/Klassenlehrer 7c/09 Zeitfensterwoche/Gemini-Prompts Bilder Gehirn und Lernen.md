---
tags: [schule, klassenlehrer, zeitfensterwoche, gemini]
status: aktiv
date: 2026-10-19
---

# Gemini-Prompts: Bilder für "Gehirn und Lernen" (Di 20.10.)

Zur HTML: [[Di 20.10. Gehirn und Lernen – Stunden]] (im selben Ordner, noch ohne Bilder).

## Ablauf

1. Jeden Prompt unten in der Gemini-App eingeben. **Den Stil-Block immer davor setzen.**
2. Das Ergebnis herunterladen und mit dem angegebenen Dateinamen in diesen Ordner legen (neben die HTML). Format JPG oder PNG, egal.
3. Sag mir Bescheid, ich baue sie ein und prüfe, wie es aussieht.

Falls ein Bild nicht passt, schreib mir, was stört. Ich passe den Prompt an.

## Stil-Block (immer davor setzen)

> Minimalistische Strichzeichnung im Stil eines modernen Lehrbuchs: gleichmäßig dicke dunkelblaue Linien (fast schwarz, Farbton #1C2230), keine Füllfarben, keine Schatten, keine Verläufe. Hintergrund einfarbig cremeweiß (#FCF8EF). Kein Text, keine Buchstaben, keine Zahlen im Bild. Freundlich und schlicht, für Siebtklässler, nicht kindisch und keine Karikatur.

Das entspricht deinen bisherigen Bildern aus "Lernen lernen" (Schwimmer, Controller, Konsumieren gegen Lernen).

## Die Prompts

### 1. `bild-treppe` (Querformat 4:3), Baustein "Aktiv statt nur zuhören"
Eine Treppe mit vier Stufen, von links unten nach rechts oben. Ein Jugendlicher steigt sie hinauf. Auf den Stufen je ein kleines Symbol: auf Stufe 1 ein Ohr, auf Stufe 2 ein aufgeschlagenes Buch, auf Stufe 3 ein Stift, der schreibt, auf Stufe 4 zwei sprechende Köpfe mit leeren Sprechblasen.

### 2. `bild-paeckchen` (Querformat 4:3), Baustein "Wie viel passt in den Kopf?"
Zweigeteiltes Bild mit gestrichelter Trennlinie in der Mitte. Links: ein Kopf im Profil, der überfordert wirkt (kleine Schweißtropfen), davor neun einzelne, lose verstreute Würfel ohne Beschriftung. Rechts: ein Kopf im Profil, der entspannt wirkt, davor ein einziges ordentliches Paket mit Schleife.

### 3. `bild-gefuehle` (Querformat 4:3), Baustein "Gefühle und Lernen"
Zweigeteiltes Bild mit gestrichelter Trennlinie. Links: ein Jugendlicher am Schreibtisch, der lächelt und entspannt arbeitet, über ihm eine kleine Sonne. Rechts: ein Jugendlicher mit hochgezogenen Schultern und angespanntem Gesicht am Schreibtisch, über ihm eine Gewitterwolke mit Blitz.

### 4. `bild-pfad` (Querformat 4:3), Baustein "Wie wir vergessen und behalten"
Drei Bilder nebeneinander in Draufsicht, mit Pfeilen dazwischen: ein schmaler Trampelpfad durch Gras, dann ein breiterer Weg, dann eine breite Straße mit Mittelstrich. Es soll sichtbar werden: je öfter man den Weg geht, desto breiter wird er.

### 5. `bild-hausbau` (Querformat 4:3), Baustein "Erst das Grundwissen"
Zweigeteiltes Bild mit gestrichelter Trennlinie. Links: eine leere Wiese, auf der nur Wasserrohre liegen, ein ratloser Jugendlicher mit Bauhelm kratzt sich am Kopf, darüber ein einfaches Kreuz. Rechts: ein Haus im Rohbau mit Fundament und Wänden, die Rohre laufen sauber hindurch, ein zufriedener Jugendlicher mit Bauhelm, darüber ein einfaches Häkchen.

### 6. `bild-netz` (Querformat 4:3), Baustein "Das Gehirn: ein Netz"
Zweigeteiltes Bild mit gestrichelter Trennlinie. Links: ein weitmaschiges Fischernetz mit einem großen Loch, ein Fisch schwimmt hindurch. Rechts: ein engmaschiges Netz, in dem sich ein Fisch verfangen hat. Die Knotenpunkte des Netzes als kleine Kreise (erinnert an Nervenzellen).

### 7. `bild-icons-runden` (Quadrat 1:1), vier Runden des Merk-Experiments
Vier einzelne Symbole in einem 2×2-Raster mit viel Abstand dazwischen, alle gleich groß und im selben Stil: oben links ein Ohr mit Schallwellen, oben rechts ein aufgeschlagenes Buch, unten links ein Auge, unten rechts eine Hand, die eine Bewegung macht (mit Bewegungsstrichen). Kein Rahmen um die Symbole. Ich schneide das später in vier Einzelbilder.

### 8. `bild-titel` (Breitformat 16:9), Titelfolie "Wie lernt dein Kopf?"
Ein Jugendlicher im Profil, nachdenklich, den Kopf leicht geneigt. Über dem Kopf eine große Gedankenblase. Aus ihr steigen nebeneinander auf: ein Puzzleteil, ein Netz, eine Treppe und ein Paket. Nur Symbole, keine Schrift.

### 9. `bild-karte` (Querformat 4:3), Folie "Und die Lerntypen?"
Zweigeteiltes Bild mit gestrichelter Trennlinie. Links: eine stilisierte Landkarte mit abstrakter Landform und mehreren Stecknadeln, ein Jugendlicher zeigt darauf. Rechts: nur ein Stapel Karteikarten, ein Jugendlicher schaut ratlos darauf. Die Landform soll erfunden und kein echtes Land sein.

## Was aus dem Original wie ersetzt wird

| Original | Neu | Grund |
|---|---|---|
| Gehirn mit linker und rechter Hälfte, Karikaturen der vier Lerntypen | entfällt | Hirnhälften-Mythos, Lerntypen |
| Symbole je Runde (Ohr, Buch, Auge, Sprechblase) | `bild-icons-runden` | Gleiche Idee, neuer Stil |
| 15 Bild-Folie "Sehen" und "Selber sagen" | Emojis in Runde 3 (schon in der HTML) | Sofort einsetzbar, keine Urheberrechtsfragen |
| Sinnes-Icons in Gruppe 1 | `bild-treppe` | Passt zum neuen Text (aktiv statt Sinne) |
| Gehirn von oben in Gruppe 2 | `bild-paeckchen` | Neuer Baustein |
| Zeichnung "verzweifelter Schüler" in Gruppe 3 | `bild-gefuehle` | Zeigt gutes und schlechtes Gefühl |
| Foto Baustelle in Gruppe 4 | `bild-pfad` | Pfad zur Straße direkt sichtbar |
| Sieb in Gruppe 5 | `bild-hausbau` | Original-Text mit Sieb und Hausbau, ich habe auf den Hausbau reduziert |
| Foto Fisch im Netz in Gruppe 6 | `bild-netz` | Gleiche Idee, einheitlicher Stil |
| Overhead-Projektor bei "Tipps zur Folie" | entfällt | Es wird auf A4 gearbeitet |
| Karikatur "Wir behalten ungefähr …" | entfällt | Lernpyramide |

## Nachtrag 19.10.2026: Bild für Runde 3 (Sehen)

`bild-sehen-raster` ersetzt die Emojis. Eine Tafel mit 12 Gegenständen im Raster 4 × 3, farbig im Anime-Stil (Apfel, Fahrrad, Schlüssel, Sonne, Hase, Auto, Buch, Zelt, Banane, Schere, Krone, Glocke). Die HTML schneidet daraus die zwölf Felder per CSS aus. Die Reihenfolge der Wörter in der Liste muss zur Reihenfolge im Raster passen, wenn die Wörter oder das Bild geändert werden.

Prompt (kurz): "Erstelle ein Bild im Querformat 4:3. Eine saubere Bilder-Tafel mit genau 12 einzelnen Gegenständen in einem gleichmäßigen Raster mit 4 Spalten und 3 Zeilen, jeder Gegenstand mittig in seiner Zelle, cremeweißer Hintergrund, farbige Illustration im Anime-Stil, kein Text. Zeile 1: roter Apfel, Fahrrad, goldener Schlüssel, Sonne. Zeile 2: Hase, rotes Auto, aufgeschlagenes Buch, Zelt. Zeile 3: Banane, Schere, Krone, Glocke. Keine Menschen, keine bekannten Figuren."
