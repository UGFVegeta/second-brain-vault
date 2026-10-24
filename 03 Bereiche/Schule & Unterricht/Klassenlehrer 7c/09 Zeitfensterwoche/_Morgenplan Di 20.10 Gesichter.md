---
tags: [schule, klassenlehrer, zeitfensterwoche, arbeitsplan]
status: abgeschlossen
date: 2026-10-19
---

# Morgenplan Di 20.10.2026: Gesichter in die Bilder, Folien und Druckdateien neu

**Erledigt am 20.10.2026 morgens.** Sechs Bilder mit Gesichtern (`gesicht-*.jpg`) sind in der HTML, die Druckdateien liegen in iCloud, die Fassung ohne Gesichter in `_alt`. Die Karte ist neu im Stil der anderen.

Oskar öffnet um 6 Uhr den Mac und sagt Claude, dass es losgehen soll. Die Stunde "Gehirn und Lernen" ist am selben Tag, 4. bis 6. Stunde, Raum 1.24. Dieser Plan reicht, auch wenn die Sitzung neu beginnt.

## Beschlossen (Oskar, 19.10.)

- Alle neun neuen Bilder (`neu-*.jpg`) sind schon in der HTML. Das Karten-Bild ist noch das alte (`bild-karte.jpg`).
- Heute früh: Gesichter ergänzen, einsetzen, Folien und Druckdateien neu erzeugen.
- Gesichter minimal: zwei kleine Punkte als Augen, ein kurzer Strich als Mund. Stimmung über den Mund (Lächeln, sorgenvoll). Schräge Ansicht und Stil bleiben.
- Das Gemini-Konto (bezahltes Plus-Konto, in Chrome eingeloggt) darf dafür benutzt werden. Etwa 12 bis 15 Bilder, das verbraucht das Tageskontingent. Limit war am 19.10. aufgebraucht, Reset 20.10. um 00:07.
- Nie auf "Upgrade" oder Abo-Knöpfe klicken.

## Welche Bilder bekommen Gesichter

Titel, Treppe, Päckchen, Gefühle, Hausbau, Karte (neu erzeugen, es gibt noch kein Bild im neuen Stil). **Ohne Gesichter bleiben:** Pfad (sehr kleine Figuren), Netz, Runden-Symbole, Bilder-Tafel für Runde 3.

## Ablauf

1. **Gemini prüfen:** Chrome-Erweiterung, `https://gemini.google.com/app`. Läuft das Limit wieder? Wenn Gemini "Limit erreicht" meldet, abbrechen und Oskar sagen. Fallback: Die Druckdateien ohne Gesichter liegen schon in iCloud.
2. **Variante A (bevorzugt): vorhandenes Bild bearbeiten lassen.** Das Bild `neu-*.jpg` hochladen (Tool `file_upload`) und schreiben: "Ergänze nur minimale Gesichter (zwei kleine Punkte als Augen, kurzer Strich als Mund, Stimmung: …). Alles andere exakt unverändert lassen." Das erhält die Komposition. Wenn das Ergebnis verändert aussieht: Variante B.
3. **Variante B: neu erzeugen** mit dem Stil-Block unten, ein gemeinsamer Chat, damit der Stil einheitlich bleibt.
4. **Prüfen:** Jedes Bild ansehen (Gesichter nicht verzerrt, Farben zart, Stil gleich wie die anderen). Kein Text im Bild.
5. **Ablegen:** Bild nach `~/Downloads` herunterladen, dann ins Stunden-Verzeichnis (Vault `…/Klassenlehrer 7c/09 Zeitfensterwoche/`) als `gesicht-<name>.jpg` (zum Beispiel `gesicht-titel.jpg`), auf 1.400 px Breite verkleinern (`sips -Z 1400 -s format jpeg -s formatOptions 82`).
6. **HTML umstellen:** In `Di 20.10. Gehirn und Lernen – Stunden.html` die Namen `neu-titel.jpg`, `neu-treppe.jpg`, `neu-paeckchen.jpg`, `neu-gefuehle.jpg`, `neu-hausbau.jpg` auf `gesicht-…jpg` ändern. Die Karte: `bild-karte.jpg` durch `gesicht-karte.jpg` ersetzen. `neu-pfad`, `neu-netz`, `neu-icons`, `neu-raster` bleiben.
7. **Prüfen im Browser:** lokaler Server (`python3 -m http.server 8765` im Ordner), Folien 1, 7, 15 und die Schülerblätter ansehen. Jedes der sieben Blätter muss genau 1123 px hoch sein (eine A4-Seite).
8. **Druckdateien neu erzeugen** mit Chrome headless (Parameter `?print=merk` und `?print=gruppen`), ohne das Kommando `timeout` (gibt es unter macOS nicht):
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --user-data-dir=/tmp/chrome_pdf_x --virtual-time-budget=8000 --print-to-pdf=OUT.pdf "file:///…/Di%2020.10.%20Gehirn%20und%20Lernen%20%E2%80%93%20Stunden.html?print=gruppen"`
   Merk-Blatt = 1 Seite, Gruppenblätter = 6 Seiten.
9. **Nach iCloud** (`GDRS ICloud/Schuljahr 26 27/Klassenlehrer/09 Zeitfensterwoche/`): `Di 20.10. Merk-Experiment Blatt.pdf` und `Di 20.10. Gruppenblätter 1 bis 6.pdf`. Die Dateien "(ohne Gesichter)" dort nach `_alt` verschieben und nicht löschen.
10. **Überblick** `00 Überblick – was wann` bleibt gültig (Dateinamen der Stunde gleich). Nur anpassen, wenn sich Dateinamen ändern.
11. **Oskar Bescheid sagen:** Was fertig ist, wo es liegt, was er heute ausdrucken muss (Merk-Blatt 26 Stück, Gruppenblätter ein Satz).

## Typische Stolpersteine bei Gemini (am 19.10. erlebt)

- Der erste Prompt nach dem Laden wird manchmal nicht abgeschickt. Nach dem Tippen kurz prüfen, ob der Text im Feld steht, dann Enter.
- Manchmal antwortet Gemini nur mit Text ("Ich kann dabei nicht helfen …"). Prompt mit "Erstelle bitte ein Bild im Querformat …" neu senden.
- Der Download-Knopf heißt `Bild in Originalgröße herunterladen`. Per JavaScript den letzten Knopf klicken: `document.querySelectorAll('button[aria-label="Bild in Originalgröße herunterladen"]')`.
- Nach dem Klick 10 bis 15 Sekunden warten und in `~/Downloads` nach neuen Dateien `Gemini_Generated_Image_*` suchen (Marker mit `touch` setzen, `find -newer`). Vorsicht, dort liegen viele ältere Gemini-Dateien von Oskar. Nur Dateien nehmen, die neuer als der Marker sind, und nur, wenn genau eine neu ist.
- Das Tool `wait` erlaubt höchstens 10 Sekunden.

## Stil-Block (für Variante B, gleicher Stil wie `neu-*`)

> Saubere, ruhige Strichzeichnung im Stil moderner Illustrations-Richtlinien: gleichmäßige, glatte Linien in weichem Dunkelgrau (#333333), geometrisch mit klaren Ecken und abgerundeten Linienenden, nicht gekritzelt, wenig Details. Figuren nur Linie ohne Farbfüllung, mit minimaler Mimik: zwei kleine Punkte als Augen und ein kurzer Strich als Mund. Leichte Dreidimensionalität: Möbel und Gegenstände in sanfter 3/4-Ansicht mit sichtbarer Tiefe, aber nicht zu schräg. Farbe nur als zarter Pastellton (etwa 25 bis 30 Prozent) in Form einer leicht versetzten Fläche, die nicht exakt in den Linien liegt, ausschließlich auf Gegenständen und in sinnvollen Farben: Sonne zartes Gelb, Gewitterwolke dunkelgrau, Holz und Tische zartes Holzbeige, Pflanzen zartes Grün, Wasser und Fische zartes Blau, Papier ungefüllt, Dach, Pakete und Ziegel zartes Orange. Keine Schatten, keine Verläufe, keine Rasterpunkte. Hintergrund cremeweiß (#FCF8EF). Kein Text, keine Buchstaben, keine Zahlen. Neue, eigene Figuren, vollständig im Bild.

## Motive mit Gesichtern

1. **Titel (16:9):** Eine Figur im Halbprofil, nachdenklich, Hand am Kinn, leichte Mimik (Augenpunkte, ruhiger Mund). Darüber eine geschlossene, pillenförmige Gedankenblase mit vier Symbolen: Puzzleteil (grün), Netz (blau), Treppe (beige), Paket (orange).
2. **Treppe (4:3):** Isometrische Treppe mit vier Stufen von links unten nach rechts oben (Holzbeige), eine Figur mit zuversichtlichem Gesicht steigt hinauf. Auf den Stufen: Ohr mit Schallwellen, aufgeschlagenes Buch, Stift (schreibt), zwei sprechende Köpfe mit leeren Sprechblasen.
3. **Päckchen (4:3):** Zweigeteilt mit gestrichelter Trennlinie. Links eine Figur mit überfordertem Gesicht, Hände am Kopf, Schweißtropfen, neun lose Würfel davor. Rechts eine entspannte Figur mit Lächeln auf einem Hocker, ein ordentliches Paket mit Schleife (Orange).
4. **Gefühle (4:3):** Zweigeteilt. Links Figur am Schreibtisch mit Heft und Stift, Lächeln, ruhige Haltung, zarte gelbe Sonne darüber. Rechts Figur am Schreibtisch, gebeugt, sorgenvoller Mund, dunkelgraue Gewitterwolke mit gelbem Blitz. Tische Holzbeige, Stühle zartes Blau, leichte 3/4-Ansicht.
5. **Hausbau (4:3):** Zweigeteilt. Links Figur mit gelbem Bauhelm und ratlosem Gesicht, kratzt sich am Kopf, leere grüne Wiese mit Wasserrohren, darüber ein Kreuz. Rechts Figur mit gelbem Bauhelm und zufriedenem Lächeln vor dem Rohbau eines Hauses (Orange) mit sauber verlegten Rohren, darüber ein Häkchen.
6. **Karte (4:3, neu):** Zweigeteilt. Links eine stilisierte, erfundene Landkarte (zartes Grün und Blau) mit mehreren roten Stecknadeln, eine Figur mit freudigem Gesicht zeigt darauf. Rechts nur ein Stapel Karteikarten (zartes Gelb), eine Figur mit ratlosem Gesicht schaut darauf.

## Stand der Dateien (19.10. abends)

- Vault-Ordner: `Di 20.10. Gehirn und Lernen – Stunden.html` (Folien, Merk-Experiment, Schülerblätter, Aufschrieb, Ausdrucken), `neu-*.jpg` (neun Bilder ohne Gesichter), `bild-*.jpg` (frühere Strichzeichnungen), `_anime-*`, `_retro-*`, `_mix-*`, `_skizze-*`, `_pastell-*` (Testvarianten), `_Stilvergleich.html`, `Gemini-Prompts Bilder Gehirn und Lernen.md`.
- iCloud `09 Zeitfensterwoche`: zwei PDFs "(ohne Gesichter)" als Sicherheit.
- Die Testbilder und `_Stilvergleich.html` sind Arbeitsdateien. Nach Oskars Entscheidung fragen, ob sie gelöscht werden sollen (nie ungefragt löschen).
