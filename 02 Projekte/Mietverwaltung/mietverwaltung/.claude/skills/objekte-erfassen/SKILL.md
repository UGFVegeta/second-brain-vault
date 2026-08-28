---
name: objekte-erfassen
description: Erfasst Objekte, Wohneinheiten, Mietverhältnisse, Darlehen und Fristen im Gespräch und schreibt sie nach daten/. Nutze diesen Skill, wenn der Vermieter sagt „lass uns meine Objekte erfassen", „neue Wohnung anlegen", „neuer Mieter", „Mietvertrag eintragen", „Darlehen erfassen", „Frist eintragen" oder wenn daten/objekte.json noch leer ist.
---

# Objekte und Mietverhältnisse erfassen

Du führst durch die Ersterfassung. Der Vermieter sitzt daneben und hat seine
Unterlagen vor sich. Deine Aufgabe ist, ihm das Tippen abzunehmen und die
Daten sauber in die JSON-Dateien zu schreiben.

## Zuerst: nicht abfragen, was schon irgendwo steht

**Bevor du die erste Frage stellst, frag diese:** Ob seine Wohnungen schon
irgendwo erfasst sind, in einer Excel-Liste, einer Aufstellung für den
Steuerberater oder in den Mietverträgen. Wenn ja, geht es mit dem Skill
[unterlagen-uebernehmen](../unterlagen-uebernehmen/SKILL.md) weiter: Er legt
die Dateien in den Ordner `unterlagen\`, du liest sie aus und fragst
hinterher nur noch die Lücken ab.

Das ist der Unterschied zwischen zwei Stunden Diktat und zwanzig Minuten
Durchsehen. Nutz ihn, bevor du anfängst abzufragen.

Der Rest dieser Anleitung gilt für das, was übrig bleibt: Objekte ohne
Unterlagen, spätere Ergänzungen, ein neuer Mieter zwischendurch.

## Haltung

Frag ein Objekt nach dem anderen ab, nicht alles auf einmal. Bei 20 bis 30
Einheiten ist das ein längeres Gespräch, das ist normal. Mach nach jedem
fertigen Objekt eine kurze Bestätigung und schreib sofort in die Datei, damit
bei einer Unterbrechung nichts verloren geht.

**Erfinde keine Zahlen.** Wenn eine Angabe fehlt, schreib `null` und merk sie
dir für eine Nachfrage am Ende. Eine geschätzte Kaltmiete ist schlimmer als
gar keine, weil sie später als bare Münze genommen wird.

## Reihenfolge

1. **Objekt**: Bezeichnung (Straße und Hausnummer reichen), Ort, Typ,
   Kaufpreis und Kaufdatum falls bekannt.
2. **Einheiten** des Objekts: Bezeichnung (WE 1, EG links, Haus), Wohnfläche,
   Zimmerzahl. Auch leerstehende Einheiten anlegen, sonst stimmt die Quote nicht.
3. **Mietverhältnis** je vermieteter Einheit, siehe unten.
4. **Darlehen** je Objekt, falls finanziert.
5. **Fristen**: Heizungswartung, Legionellenprüfung, Rauchmelder, Ablesung.

Darlehen und Fristen können auch später kommen. Mietverhältnisse nicht, die
sind der Kern.

## Beim Mietverhältnis besonders wichtig

- **Kaltmiete und Nebenkostenvorauszahlung getrennt** erfassen. Für die
  Zuordnung zählt die Summe, für die Nebenkostenabrechnung braucht es die
  Aufteilung. Wenn der Vermieter nur die Warmmiete weiß: Kaltmiete
  eintragen, `nebenkosten_voraus` auf `null`, nachfragen vermerken.
- **IBAN des Mieters**, wenn greifbar. Das ist das stärkste Merkmal für die
  automatische Zuordnung. Steht sie nicht im Vertrag, findet sie sich auf dem
  letzten Kontoauszug. Fehlt sie, funktioniert die Zuordnung trotzdem über
  Name und Betrag, nur etwas unschärfer.
- **Mietart**: `frei`, `staffel` oder `index`. Bei Staffel- und Indexmiete
  zusätzlich in `notizen`, was vereinbart ist.
- **letzte_erhoehung**: Datum der letzten Mieterhöhung. Daraus ergibt sich,
  wann die nächste rechtlich möglich ist.

## Feldnamen

Halte dich exakt an die Struktur in `daten/beispiel/`. Schau dort nach, bevor
du schreibst. IDs in Kleinbuchstaben mit Bindestrich, abgeleitet aus der
Bezeichnung (`Gartenstr. 12` wird `gartenstr-12`, die zweite Einheit darin
`gartenstr-12-we2`). Mietverhältnisse werden fortlaufend nummeriert:
`mv-001`, `mv-002`.

Bestehende Einträge nicht überschreiben, sondern ergänzen. Vor dem Schreiben
die vorhandene Datei lesen.

## Wenn die Sitzung lang wird

Bei 30 Einheiten kann eine Sitzung an ihre Grenze kommen. Das ist kein
Problem, solange nach jedem Objekt sofort geschrieben wird. Dann gilt:

- Neue Sitzung öffnen und „Weiter erfassen" sagen.
- `py -3 skripte\pruefen.py` zeigt den Stand.
- Ab dort weitermachen.

Sag ihm das am Anfang einmal. Wer weiß, dass nichts verloren gehen kann,
arbeitet ruhiger und muss nicht durchhalten.

## Nach jedem Objekt

Kurz vorlesen, was du eingetragen hast, in einem Satz. Nicht als Tabelle, das
ermüdet. Beispiel: „Gartenstr. 12 mit drei Einheiten, davon zwei vermietet,
zusammen 1700 Euro Sollmiete im Monat. Passt das?"

## Am Ende

1. `py -3 skripte\pruefen.py` laufen lassen. Das findet Tippfehler,
   doppelte IDs und Einheiten ohne Mietverhältnis.
2. Offene Nachfragen sammeln und vorlesen.
3. `py -3 skripte\dashboard_bauen.py` und das Dashboard öffnen.

## Datenschutz

Hier entstehen echte Mieterdaten: Namen, Kontoverbindungen, Zahlungsverhalten.
Diese Daten bleiben auf diesem Rechner. Lade sie nirgendwohin hoch, verschick
sie nicht, und nimm sie nicht in Zusammenfassungen auf, die den Rechner
verlassen. Wenn du einen Beispielfall zeigen willst, nimm die erfundenen
Namen aus `daten/beispiel/`.
