# Mietverwaltung – zum Loslegen

Eine kleine Verwaltung für private Mietobjekte, die auf dem eigenen Rechner
läuft. Sie überwacht die Mieteingänge, meldet Rückstände, bereitet
Zahlungserinnerungen vor und sammelt übers Jahr die Zahlen für die Steuer.

Bedient wird sie im Gespräch mit Claude. Die drei Dateien mit den Nummern
vorne kann man aber auch einfach anklicken.

Wer lieber etwas Gedrucktes neben der Tastatur hat: **Einrichtung Schritt für
Schritt.pdf** im selben Ordner enthält denselben Ablauf auf drei Seiten, mit
einer Nachschlageseite für den Fall, dass etwas klemmt.

## Was gebraucht wird

Zwei Dinge, beide einmalig:

**1. Git for Windows.** Die Claude-Code-App unter Windows braucht es, um
lokale Sitzungen auszuführen. Sie verwendet die mitgelieferte Git-Bash als
Kommandozeile. Fehlt es, meldet die App „Git ist für lokale Sitzungen
erforderlich" und lässt sich nicht benutzen. In dem Fall im Dialog auf
**Git herunterladen** klicken, mit den Standardoptionen installieren und die
App neu starten. Alternativ direkt von https://git-scm.com/download/win.

Das hat nichts mit Versionsverwaltung zu tun. Man muss Git nicht bedienen und
nicht verstehen, es liefert nur die Kommandozeile.

Wichtig: Wenn die App stattdessen eine **Remote-Umgebung** anbietet, diese
nicht wählen. Diese Verwaltung ist darauf ausgelegt, dass Mieterdaten und
Kontoauszüge auf dem eigenen Rechner bleiben.

**2. Python.** Prüfen mit einem Doppelklick auf `1 Selbsttest.bat`. Kommt eine
Meldung, dass Python fehlt: von https://www.python.org/downloads/ installieren
und beim Setup **„Add Python to PATH" ankreuzen**. Ohne dieses Häkchen findet
Windows Python später nicht.

Sonst nichts. Keine Anmeldung, kein Konto, kein Server, keine laufenden Kosten.

## Die ersten Schritte

**1. Selbsttest**
Doppelklick auf `1 Selbsttest.bat`. Es rechnet einen erfundenen Beispielfall
durch und meldet, ob alles stimmt. Läuft das durch, funktioniert der Rest auch.

**2. Vorhandene Unterlagen hineinlegen**
Wer seine Wohnungen schon irgendwo stehen hat, muss sie nicht vorlesen. Alles
was es gibt, in den Ordner `unterlagen` legen: die Excel-Liste, Mietverträge
als PDF, die Aufstellung für den Steuerberater, eine Mieterliste.

Dann Claude Code in diesem Ordner starten und sagen:

> Lies meine Unterlagen ein.

Claude liest die Tabellen und Verträge, zeigt was er verstanden hat, und
übernimmt es nach Bestätigung. Danach fragt er nur noch das nach, was in den
Unterlagen nicht stand. Aus zwei Stunden Diktat werden so meist zwanzig
Minuten Durchsehen.

Eingescannte Verträge ohne Textebene sind reine Bilder, daraus lässt sich
nichts auslesen. Diese Angaben fragt Claude ab.

**Wenn es nichts Vorhandenes gibt**, einfach sagen:

> Lass uns meine Objekte erfassen.

Dann fragt Claude der Reihe nach ab: Haus, Wohnungen, Mieter, Kaltmiete,
Nebenkosten, Laufzeiten. Für 20 bis 30 Einheiten sollte man ein bis zwei
Stunden einplanen, man kann jederzeit aufhören und später weitermachen.

Zwei Angaben lohnen in beiden Fällen besonders: **Kaltmiete und Nebenkosten
getrennt**, und die **IBAN des Mieters**. Mit der IBAN ordnet das System
Zahlungen praktisch fehlerfrei zu.

**3. Kontoauszug einlesen**
Im Online-Banking die Umsätze der letzten Monate als CSV exportieren, die
Datei in den Ordner `kontoauszuege` legen, dann Doppelklick auf
`2 Kontoauszug einlesen.bat`.

Das Format spielt keine Rolle, die gängigen Banken werden erkannt. Denselben
Export mehrfach einzulesen schadet nicht, doppelte Buchungen werden erkannt.

**4. Dashboard ansehen**
Doppelklick auf `3 Dashboard oeffnen.bat`.

## Später: Bank direkt anbinden

Der CSV-Weg funktioniert immer und ist einmal im Monat eine Minute Arbeit.
Wer die Umsätze automatisch holen will, findet den Weg über FinTS in
`doku\Bankanbindung.md`. Ehrlich gesagt: Das ist kein Häkchen, sondern ein
Nachmittag Einrichtung, und ob es klappt, hängt an der eigenen Bank.

## Was Claude für einen macht

- Vorhandene Excel-Listen und Mietverträge auslesen und übernehmen
- Objekte, Wohnungen und Mietverhältnisse aufnehmen und pflegen
- Kontoauszüge einlesen und Zahlungen zuordnen
- Unklare Eingänge im Gespräch klären
- Rückstände zeigen, samt Verzugsdauer
- Zahlungserinnerungen und Mahnungen **entwerfen**
- Ausgaben für die Anlage V sortieren
- Fristen und Zinsbindungen im Blick behalten

## Was Claude nicht macht

**Verschicken.** Keine Mail geht raus, ohne dass man sie gelesen und selbst
verschickt hat. Das ist Absicht: In den Daten steht nie die ganze Geschichte.
Wer bar bezahlt hat, mit wem eine Stundung vereinbart ist, wer gerade wegen
eines Mangels mindert. Eine automatisch verschickte Mahnung in so einem Fall
kostet mehr Vertrauen, als die Automatik je einspart.

**Zugangsdaten eingeben.** PIN und TAN tippt man selbst, wenn das Skript
danach fragt. Sie werden nirgends gespeichert.

**Steuer- oder Rechtsberatung.** Claude sortiert Belege und rechnet
zusammen. Ob eine Kündigung zulässig ist oder wie eine Sanierung steuerlich
aufzuteilen ist, gehört zum Anwalt oder Steuerberater.

## Wo die Daten liegen

Alles in `daten\`, als lesbare Textdateien. Nichts davon verlässt den
Rechner. Es lohnt sich, diesen Ordner in die eigene Datensicherung
aufzunehmen, denn eine zweite Kopie gibt es nirgends.

Weil dort echte Mieterdaten stehen, gehört der Ordner nicht in eine
öffentliche Cloud und nicht in ein Git-Repository. Näheres in
`doku\Datenschutz.md`.
