---
tags: [ressource, sport, turnen, dreikampf]
---

# Dreikampf Turnen (Klasse 7 bis 10)

Übersicht der Übungen Ü2 bis Ü6 für den Turn-Dreikampf mit Bildreihen, Regeln und Notenschlüssel. Wertung: 3 aus 5 Geräten (Boden, Reck, Barren, Balancieren, Sprung). Pro Gerät eine Übung Ü2 bis Ü6 mit 2 bis 6 Punkten, dazu bis zu 3 Zusatzpunkte für die Ausführung. Die Summe der drei Geräte ergibt die Note (Tabelle unten).

## Dateien in diesem Ordner
- `dreikampf-turnen.html`: die Seite mit zwei Reitern. Reiter „Karten“ (Vorder- und Rückseite, A4 quer, zum Laminieren) und Reiter „Wahlübungen“ (Vorschlag: Elemente selbst wählen, Wahlzettel mit Punkten und Note). Braucht den Ordner `bilder/` daneben.
- `dreikampf-turnen-vorder-rueckseite.pdf`: die zwei Kartenseiten als PDF.
- `bilder/`: Bildreihen je Gerät und Stufe (`boden-ue2.png` bis `sprung-ue7.png`, Ü7 nur im Wahl-Reiter) Die Bilder sind aus dem BJS-Handbuch mit nachgezogener Kontur (Schwarz-Weiß-Druck).
- `build.mjs` baut die HTML aus den Übungsdaten, `noten.json` ist der Notenschlüssel. Neu bauen: im Ordner `node build.mjs` ausführen. Die Übungen und Texte stehen oben im Skript (Objekt `D`).
- `Quelle/`: BJS-Handbuch Gerätturnen (Auszug, Stand 04/26) als PDF, aus dem Übungen und Bilder stammen.

## Notenschlüssel (Summe der 3 Geräte, Jungen)
Quelle: iCloud `GDRS ICloud/Schuljahr 26 27/Sport/Notenlisten/Geräteturnen/Notenliste Geräteturnen Klasse N 26-27.xlsx` und `.pdf`, unten auf jedem Blatt. Für Klasse 5 und 6 steht dort keine Punkt-Note-Tabelle.

Note 1,0 ab: Klasse 7 = 20 Punkte, Klasse 8 = 21, Klasse 9 = 22, Klasse 10 = 23. Danach geht es in Halbpunkt-Schritten mit Zehntelnoten abwärts bis 0 Punkte = 6,0. Die vollständige Tabelle steht in `noten.json` und auf der Rückseite der Karte.

## Offen
- Die Kippe in den Grätschsitz (Barren Ü5) fehlt im Handbuch. Auf der Karte steht die Original-Zeichnung vom alten Plakat (`bilder/barren-kippe.png`, aus dem Foto freigestellt). Versuche mit Gemini, ChatGPT und einer Montage aus Handbuch-Figuren (`compose_kippe.py`) wurden verworfen.
- Sprung Ü6: Das Handbuchbild zeigt eine Figur mit Kopftuch und wird nicht verwendet. Stattdessen steht dort das Ü5-Bild mit grünem Shirt (gleiche Bewegung).
- Bildgrößen: Die Bilder füllen den freien Platz in der Zelle automatisch (Funktion `fit()` in `build.mjs`).
- Ü5 Barren: Das Handbuch nennt „Zweimaliger Vor- und Rückschwung …“, das alte Plakat „Schwingen im Stütz“. Auf der Karte steht die Handbuch-Fassung, ergänzt um die Kippe.
- Schulinterne Regel: Beim Barren Ü6 ist statt des Oberarmstands die Oberarmrolle (Rolle vorwärts über die Holme) erlaubt. Das steht nicht im BJS-Handbuch und ist auf der Karte als „Bei uns erlaubt“ gekennzeichnet.
- Ablauf der Kippe in den Grätschsitz (Barren Ü5, nach Oskar): Der Schüler steht am Ende des Barrens zwischen den Holmen auf dem Boden, jede Hand greift einen Holm von außen. Er kippt mit engem Hüftwinkel, dann schwingen die Beine gestreckt nach oben und weiter in den Grätschsitz auf den Holmen. Bildreihe dazu steht noch aus, bis dahin das Plakat-Bild.
- Sprung Ü5 zeigt einen Kasten quer, Sprung Ü6 einen Sprungtisch (Gerät jeweils aus den BJS-Bildern Ü2 und Ü7 in das Ü5-Bild eingesetzt, Skript `compose_sprung.py`). Das Handbuchbild zu Ü6 mit Kopftuch wird nicht verwendet.
