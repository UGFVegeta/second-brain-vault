---
tags: [projekt, lego, wieslauftalbahn]
status: aktiv
date: 2026-10-10
---

# Lego Wieslauftalbahn (WEG VT 451, Regio-Shuttle RS1)

Ziel: Bauplan und Teileliste für ein Lego-Modell des Wiesel-Triebwagens nach echten Fotos. Optik wie ein sauberes MOC (Vorbild: ICE-4-MOC von lesdiy.de): glatte Flächen, gerundetes Dach, geneigte Front, nichts Klobiges.

## Stand (10.10.2026)
- Maßstab ca. 1:45: 70 Noppen lang (ca. 56 cm), 8 breit, 26 Platten hoch.
- Entwurf aus echten Teilen, 603 Teile, ohne Räder. In BrickLink Studio geprüft: 0 Stabilitätsprobleme, 0 lose Teile (38 Hinweise zur Klemmkraft, vor allem Dachkante und Nase). Wunschliste 50 Positionen.
- Nase im Stil des ICE-Vorbilds überarbeitet: durchgehende Frontscheibe (Windscreen 2x6x2 mit Glas, 13760c01), 65°-Schrägen als Seitenpfosten, runde Scheinwerfer auf Seitennoppen-Steinen (87087), Dachkanten mit Kurvenschrägen (15068), Dachmitte mit Fliesen.
- Import in Studio: Datei, Import, Import Model (nicht Öffnen). Danach Model, Release Submodel, um Einzelteile zu bekommen.

## Dateien
- `Wieslauftalbahn.ldr`: Modell für BrickLink Studio (Datei, Öffnen). Schritte nach Plattenlage.
- `Teileliste.csv`: LDraw-Teilenummern und LDraw-Farbcodes. Für die Bestellung besser in Studio exportieren (BrickLink-Wunschliste).
- `Bildtafel.png`: Ansichten mit Wiesel und Schriftzügen.
- `Bauanleitung.pdf`: 16 Bauschritte mit neuen Teilen je Schritt (Teilebilder), Gesamtteileliste am Ende.
- `Wunschliste BrickLink.xml`: von Studio exportiert (50 Positionen, 603 Teile), direkt bei BrickLink als Wunschliste hochladbar.
- `Wieslauftalbahn.mpd`: ältere Studio-Speicherung von 10:10 (alter Stand mit hellgrauer Scheibe), veraltet.
- `Frühe Entwürfe/`: erste Voxel-Konzeptbilder (zu klobig, verworfen).
- Skripte in `.scripts/`: `lego_wiesel_bilder.py` (alles bauen und rendern), `lego_wiesel_bau.py` (Modell), `ldr_render.py` und `ldr_raster.c` (Vorschau-Renderer mit Teilebibliothek aus Studio), `lego_wiesel_modell.py` (Voxel-Farbvorlage der Seitenwand).

## Offen
- Wiesel, Schriftzüge und Wappen sind Aufkleber (Eigendruck), nicht aus Steinen.
- Räder und Drehgestelle fehlen bewusst. Passende Räder (Durchmesser ca. 4,5 Platten) mit sauberer Aufhängung habe ich nicht gefunden, die Bahnräder 4180c01/c02 sind zu groß und kollidieren mit dem Boden. In Studio ein Drehgestell ergänzen.
- Studio-Farbprüfung: alle Teile in den gewählten Farben lieferbar, nachdem die Frontscheibe von Dunkelgrau auf Dunkelblau umgestellt wurde. Preis und Lagerbestand bei Händlern noch nicht geprüft.
- Heck ist von der Front gespiegelt, dafür gibt es kein Foto. Nase in der Draufsicht noch eckig, Seitenwände nicht mit Fliesen verkleidet (dafür wäre aufwendige Seitenbauweise nötig).
- ICE-Vorbild (lesdiy MOC-75541, Itrains, 6188 Teile, 499,99 EUR, nur PDF) dient nur als Stilbild, keine Vorlage.
- Drehgestell aus Studio-Bestand ergänzen, danach Bauanleitung und Wunschliste neu erzeugen.
