---
tags: [projekt, immobilien, claude-code]
status: aktiv
date: 2026-08-15
---

# Mietverwaltung

Ein Freund und Kollege verwaltet 20 bis 30 Wohnungen und Häuser und suchte
eine KI-Lösung dafür. Erste Empfehlung im Juni war dedizierte Software plus
Claude für Kommunikation und Dokumente (siehe [[05 Daily Notes/2026-06-08]]).
Daraus ist ein eigenes, lauffähiges System geworden, das sich selbst betreiben
lässt.

Das Paket ist bewusst allgemein gehalten und nicht auf eine Person
zugeschnitten. Es lässt sich genauso an andere weitergeben.

**Termin: Montag, 17.08.2026.** Ziel: gemeinsam einrichten und echte Objekte
erfassen.

## Was übergeben wird

Der Ordner `mietverwaltung/` ist das fertige Paket. Er wird komplett auf den
Zielrechner kopiert, dort startet man Claude Code darin und legt los.

- `START HIER.md` plus gedruckte Anleitung als PDF, beides für den Anwender
- `CLAUDE.md` mit den Anweisungen und Grundregeln für Claude
- sechs Skills in `.claude/skills/`: unterlagen-uebernehmen, objekte-erfassen,
  umsaetze-importieren, mahnlauf, dashboard, vermenschlichen (letzterer fremd,
  MIT-Lizenz von LOGIN-TB, ergänzt am 17.08.2026 für den Ton der Entwürfe)
- `doku/Schreibstil.md` als leere Vorlage, in die Claude die Stilkorrekturen
  des Vermieters über die Zeit einträgt
- acht Python-Skripte, ohne Fremdbibliotheken lauffähig
- drei .bat-Dateien zum Anklicken für Selbsttest, Import und Dashboard
- Beispieldatensatz mit erfundenen Namen zum Vorführen
- Doku zu Bankanbindung und Datenschutz

Die alte Demo liegt daneben als [[Demo als Gespraechsgrundlage.html]]. Die ist
weiterhin gut, um zu zeigen, wo es hingehen kann, aber sie ist eine Attrappe.
Das Paket ist das Echte.

## Was es kann

Vorhandene Excel-Listen und Mietverträge auslesen und in die Stammdaten
übernehmen, statt alles abzufragen. Der xlsx-Leser ist selbst gebaut und
kommt ohne Fremdbibliothek aus, inklusive Rückrechnung der Excel-Datumszahlen.
PDFs liest Claude Code ohnehin direkt, solange sie nicht eingescannt sind.

Kontoauszüge einlesen (CSV der gängigen Banken und camt-XML), Zahlungen
automatisch den Mietverhältnissen zuordnen, Teilzahlungen und Rückstände
erkennen, Zahlungserinnerungen abgestuft entwerfen, Ausgaben für die Anlage V
sammeln, Darlehen und Fristen im Blick behalten, Dashboard bauen.

Die Zuordnung arbeitet mit einem Punktesystem: IBAN 60, Mietername 30, Betrag
25, Objektname 15. Ab 70 Punkten gilt sie als sicher. Ungeprüfte Vorschläge
zählen bewusst nicht als bezahlt.

## Was es bewusst nicht kann

Verschicken. Kein Versand, ohne dass der Text gelesen und von Hand
abgeschickt wurde. Grund: In den Daten steht nie die ganze Geschichte, und eine
automatische Mahnung an jemanden, der bar bezahlt hat, kostet mehr als die
Automatik einspart.

## Ablauf am Montag

1. Ordner kopieren, `1 Selbsttest.bat` anklicken. Falls Python fehlt: von
   python.org installieren, **„Add Python to PATH" ankreuzen**. Das ist die
   einzige Stelle, an der es hakeln kann.
2. Die vorhandenen Dateien nach `unterlagen/` kopieren, „Lies meine
   Unterlagen ein". Zunächst **nur ein Objekt** vollständig machen.
3. Echten Kontoauszug einlesen und Dashboard öffnen. Das ist der Test: Landen
   die Mieten dieses Objekts sauber? Klemmt die Zuordnung, merkt man es nach
   einem Objekt statt nach dreißig.
4. Danach den Rest der Liste in einem Durchgang übernehmen und die Lücken
   abfragen.

Reihenfolge bewusst so: erst ein Durchstich durch die ganze Kette, dann Masse.
Nach Schritt 3 kann man jederzeit aufhören, Schritt 4 geht auch allein.

**Zur Token-Frage:** Die Excel-Liste ist billig, 30 Einheiten sind gemessen
5.125 Zeichen, also rund 1.500 Tokens. Sie zu stückeln bringt nichts. Teuer
sind nur Mietverträge als PDF, grob 10.000 bis 16.000 Tokens pro Vertrag.
Deshalb ist Claude angewiesen, Verträge nie auf Vorrat zu lesen, sondern nur
bei einer konkreten Lücke und dann einzeln. Jedes fertige Objekt wird sofort
geschrieben, ein Abbruch kostet also nichts: neue Sitzung, „Weiter erfassen",
`pruefen.py` zeigt den Stand.

## Bankanbindung, ehrlich

Nicht per Klick. FinTS braucht Zugangsdaten, TAN-Verfahren und meist eine bei
der Deutschen Kreditwirtschaft registrierte Produkt-ID; manche Banken weisen
unregistrierte Zugriffe ab. Ob die jeweilige Bank mitspielt, zeigt erst der
Versuch. Das Modul liegt fertig bei, ist aber ein eigener Nachmittag.

Der CSV-Weg funktioniert dagegen mit jeder Bank sofort und kostet einmal im
Monat eine Minute. Deshalb ist er als Standardweg eingerichtet. Bibliotheken
geprüft am 15.08.2026: `fints` 5.0.0 (Januar 2026) und `mt-940` 5.0.0 (Juni
2026) werden beide gepflegt.

## Offen

- Nebenkostenabrechnung ist noch nicht gebaut. Das ist der nächste große
  Brocken und der mit der größten Zeitersparnis.
- Mieterhöhungs- und Index-Radar fehlt ebenfalls, wäre aber überschaubar,
  weil der Verbraucherpreisindex frei abrufbar ist.
- Beides erst angehen, wenn die Grundlage ein paar Wochen im Einsatz war.

## Datenschutz

Echte Mieterdaten bleiben auf dem jeweiligen Rechner und kommen nicht in
dieses Vault. Das Paket enthält nur erfundene Beispieldaten.
