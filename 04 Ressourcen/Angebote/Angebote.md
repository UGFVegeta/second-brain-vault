---
tags: [werkzeug, einkauf]
status: aktiv
date: 2026-11-14
---

# Angebote-App

Sucht in den aktuellen Prospekten der Märkte rund um Rudersberg und zeigt die Favoriten. Öffnen: [[Angebote.html]] in Chrome.

## Wie es läuft

- Quelle ist marktguru (keine offizielle Schnittstelle, von Oskar am 14.11.2026 freigegeben). Ändert marktguru seine Schlüssel, fällt der Abruf aus. Dann die neuen Werte `apiKey` und `clientKey` aus dem Quelltext von marktguru.de in `.scripts/angebote_lib.py` eintragen.
- Der Dashboard-Dienst (`.scripts/dashboard_server.py`) holt die Favoriten einmal am Tag, sobald der Mac ab 6 Uhr wach ist. Er beantwortet auch die freie Suche und den Knopf „Jetzt aktualisieren“.
- Dateien hier im Ordner: `einstellungen.json` (Orte, ausgeblendete Märkte, Favoriten), `angebote_data.js` (letzter Abruf), `preise.json` (Preisverlauf).

## Grenzen

- Das Portal nennt die Kette, nicht die Filiale.
- Den Originalpreis liefert es selten. Die App merkt sich deshalb die Angebotspreise und zeigt nach einigen Wochen, ob es ein Produkt schon günstiger gab.
- Rossmann und dm fehlen bei marktguru. Wenn gewünscht, später direkt über die Rossmann-Seite anhängen.
- Einen Umkreis in km gibt es nicht, nur Orte (PLZ). Die Angebote sind fast immer kettenweit gleich, mehr Orte bringen wenig.

## Favoriten-Regeln in einstellungen.json

Name und Suchbegriff lassen sich in der App ändern. Feinere Regeln stehen nur in der Datei:

- `kategorien`: nur diese marktguru-Kategorien (Milch ohne Milchschokolade)
- `muss`: Regeln, die alle passen müssen (Kaffee: ganze Bohnen und 1 kg)
- `ohne`: Wörter, die rausfliegen (Bier ohne Weizen)

Beim Anzeigen stehen Kästen (ab 12 Flaschen) immer oben, sortiert nach Literpreis.

## Weitergabe-Version (Eltern, Windows)

`Angebote zum Weitergeben.html` ist eine einzelne Datei ohne Dienst und ohne Python: Sie fragt marktguru direkt aus dem Browser ab und speichert Einstellungen, letzten Abruf und Preisverlauf im Browser. Startwerte sind Oskars Favoriten und Orte. Nach Änderungen an Angebote.html oder einstellungen.json neu bauen: `python3 .scripts/angebote_weitergabe_bauen.py`. Auf dem iPad läuft eine lokale HTML-Datei nicht zuverlässig, dafür müsste die Seite online stehen.

Oben auf der Seite stehen Links zu den Prospekten der Märkte (geprüft 14.11.2026). Die Eltern nutzen nur die Datei am PC; sobald Oskar einen eigenen Server hat, kommt die Seite dorthin (dann auch fürs iPad).
