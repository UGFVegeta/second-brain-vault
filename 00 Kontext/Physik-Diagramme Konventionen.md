---
tags: [kontext, physik, zeichnen, konventionen]
status: aktiv
date: 2026-07-13
---

# Physik-Diagramme Konventionen

Wie Claude für Oskar Physik-Versuche und -Diagramme zeichnet. Am 2026-07-13 an einem Kräfteparallelogramm erarbeitet und von Oskar als „perfekt" bestätigt.

## Grundprinzip

Physik-Zeichnungen entstehen als **berechnete SVG-Konstruktionen**, nicht als KI-Bilder. Vorteil: geometrisch exakt (Pfeile treffen, Achsen gerade, Zahlen stimmen), sofort, kostenlos, skalierbar und direkt ins Merkheft / in Klassenarbeiten einbaubar. Für technisch-schematische Physik ist das der KI-Bildgenerierung (z. B. FigureLabs) überlegen – siehe [[Zusammenarbeit mit Claude]].

## Konkrete Regeln

- **Formelzeichen kursiv**, in Serifenschrift (physikalische Konvention für Größen).
- **Echte tiefgestellte Indizes**: F₁, F₂, F_res (per SVG-`tspan`, nicht Unicode-Basteln).
- **Alle gleichartigen Größen identisch aufgebaut** – gleiche Schrift, Größe, Stil. Nur die **Farbe** unterscheidet und passt zum jeweiligen Vektor/Pfeil. Kein Ausreißer (der erste Fehler war: ein Label hatte versehentlich die Pfeil-Kontur → sah anders aus).
- **Beschriftungen neben, nicht auf den Linien** platzieren, sauber ausgerichtet (mittig unter horizontalen Pfeilen, seitlich neben schrägen).
- **Pfeilspitzen in Pfeilfarbe**; Vektoren enden knapp **vor** dem Zielpunkt, damit die Spitze nicht über die Ecke schießt.
- **Resultierende = F_res**, Angriffspunkt = A.
- **Dark-Mode-tauglich** (Farben hellen im Dunkelmodus auf).
- Zielniveau: **BW-Realschule**, Merkheft-/Klassenarbeit-tauglich.

## Zusammenspiel

Passt zur bestehenden SVG-Pipeline im Vault (u. a. der Prüfungsaufgaben-Generator, der SVG-Figuren erzeugt). Bei neuen Versuchsaufbauten (Stromkreise, schiefe Ebene, Optik) diese Regeln automatisch anwenden.
