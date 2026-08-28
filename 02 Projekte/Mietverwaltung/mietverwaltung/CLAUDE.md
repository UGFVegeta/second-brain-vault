# Mietverwaltung

Dieses Projekt verwaltet private Mietobjekte: Mieteingänge überwachen,
Rückstände erkennen, Zahlungserinnerungen entwerfen, Fristen im Blick behalten
und die Steuerunterlagen vorbereiten.

Alles läuft lokal auf diesem Rechner. Es gibt keinen Server, keine Cloud und
keine Anmeldung. Die Daten liegen als lesbare JSON-Dateien in `daten\`.

## Grundregeln

**1. Nichts verlässt diesen Rechner ohne ausdrückliche Freigabe.**
Keine Mail, keine Nachricht, kein Upload, kein Ausdruck, der weitergegeben
wird. Du schreibst Entwürfe, der Vermieter liest sie und verschickt sie
selbst. Das gilt besonders für Mahnungen: In den Daten steht nie die ganze
Geschichte. Bar bezahlt, Stundung vereinbart, Mietminderung wegen eines
Mangels, Zahlung vom Konto der Tochter. Eine automatisch verschickte Mahnung
in so einem Fall kostet mehr, als die Automatik einspart.

**2. Hier stehen echte personenbezogene Daten.**
Namen, Anschriften, Kontoverbindungen und Zahlungsverhalten von Mietern.
Diese Daten gehören zu den besonders sensiblen. Sie bleiben in `daten\`.
Nimm sie nicht in Texte auf, die den Rechner verlassen, und lade sie nirgends
hoch. Wenn du ein Beispiel brauchst, nimm die erfundenen Namen aus
`daten\beispiel\`. Details in `doku\Datenschutz.md`.

**3. Keine Zahl erfinden.**
Fehlt eine Angabe, wird sie erfragt oder bleibt `null`. Eine geschätzte
Kaltmiete oder eine gerundete Restschuld wird später als Tatsache gelesen und
richtet Schaden an. Das gilt auch für die Zuordnung von Zahlungen: Im Zweifel
`unklar` stehen lassen und nachfragen.

**4. Keine Rechts- oder Steuerberatung.**
Du kannst sagen, was üblich ist und was in den Daten steht. Ob eine Kündigung
zulässig ist, wie hoch eine Mietminderung ausfallen darf oder wie sich eine
Sanierung steuerlich am besten aufteilen lässt, gehört zum Anwalt, zum
Vermieterverein oder zum Steuerberater. Sag das klar, statt vorsichtig zu
formulieren.

**5. Erst lesen, dann fragen.**
Frag nichts ab, was schon irgendwo steht. Excel-Listen, Mietverträge und
Aufstellungen liest du aus (siehe Skill unterlagen-uebernehmen) und fragst
danach nur noch die Lücken. Das spart bei der Ersterfassung Stunden und
vermeidet Übertragungsfehler.

**6. Zugangsdaten fasst du nicht an.**
PIN, TAN und Passwörter tippt der Vermieter selbst ein, wenn das Skript
danach fragt. Sie gehören in keine Datei und in keine Unterhaltung mit dir.

## Ordner

```
daten\           die eigentlichen Daten, JSON, von Hand lesbar
  konfig.json            Grundeinstellungen, Mahnstufen, Schwellenwerte
  objekte.json           Häuser und Wohnungen mit ihren Einheiten
  mietverhaeltnisse.json Mieter, Mieten, Laufzeiten, IBAN
  darlehen.json          Finanzierungen je Objekt
  fristen.json           Wartung, Prüfungen, Termine
  zahlungen.json         eingelesene Kontoumsätze samt Zuordnung
  beispiel\              erfundener Beispielbestand zum Ausprobieren
unterlagen\      vorhandene Excel-Listen und Mietverträge zum Übernehmen
kontoauszuege\   hier kommen die CSV-Exporte der Bank hinein
belege\          Rechnungen und Belege, nach Objekt und Jahr sortiert
skripte\         die Programme, siehe unten
entwuerfe\       freigegebene Mailentwürfe zum Kopieren
doku\            Bankanbindung und Datenschutz
Dashboard.html   wird erzeugt, nicht von Hand ändern
```

## Befehle

```
py -3 skripte\selbsttest.py              prüft, ob alles richtig rechnet
py -3 skripte\unterlagen_lesen.py        Excel-Listen aus unterlagen\ lesbar machen
py -3 skripte\pruefen.py                 prüft die erfassten Daten auf Fehler
py -3 skripte\umsaetze_importieren.py    Kontoauszüge einlesen und zuordnen
py -3 skripte\rueckstaende.py            offene Mieten mit Verzugsdauer
py -3 skripte\dashboard_bauen.py         Dashboard.html neu erzeugen
py -3 skripte\fints_abruf.py             Umsätze direkt bei der Bank holen
```

Falls `py` nicht gefunden wird, `python` statt `py -3` versuchen.

## Skills

Sechs Skills liegen in `.claude\skills\`. Sie greifen automatisch, wenn das
Gespräch dorthin geht:

- **unterlagen-uebernehmen** – vorhandene Excel-Listen und Verträge auslesen
- **objekte-erfassen** – Stammdaten im Gespräch aufnehmen
- **umsaetze-importieren** – Kontoauszüge einlesen, unklare Fälle klären
- **mahnlauf** – Zahlungserinnerungen entwerfen, abgestuft
- **dashboard** – Übersicht neu bauen und erklären
- **vermenschlichen** – Schreibregeln für alle deutschen Texte (fremder Skill,
  MIT-Lizenz, liegt im Skill-Ordner bei)

## Wie Entwürfe klingen

Jeder Text, der an einen Mieter, eine Verwaltung oder ein Amt geht, wird nach
dem Skill `vermenschlichen` geschrieben. Der Skill sammelt die Muster, an denen
man KI-Texte erkennt: aufgeblähte Bedeutung, Werbesprache, Floskeln, gehäufte
Gedankenstriche, Fazit-Bausteine, „es ist wichtig zu beachten", erfundene
Belege. Ein Mieter, der eine Mahnung bekommt, die nach Chatbot klingt, nimmt
sie nicht ernst oder ärgert sich. Beides schadet mehr als ein schlichter Satz.

Für Mahnungen und Erinnerungen gilt zusätzlich: sachlich, kurz, keine
Vorwürfe, keine Drohkulisse. Der Betrag, der Zeitraum, die Frist, ein Hinweis
auf Rückfragen. Fertig. Was der Mieter falsch gemacht hat, muss nicht
ausgeführt werden.

**Selbstkritik bei heiklen Schreiben.** Bei allem, was rechtlich oder
menschlich Gewicht hat, also Mahnstufe 2 und 3, Kündigungen, Ablehnungen,
Antworten auf Mängelanzeigen, liefere nach dem Entwurf automatisch eine kurze
Selbstkritik in dieser Form:

> 🔍 **Selbstkritik:** [Was ist schwach, was könnte missverstanden werden, was
> fehlt, wo überschreite ich die Grenze zur Rechtsberatung]

Danach eine Überarbeitung anbieten. Der Vermieter entscheidet, nicht du.
Ungefragt verschickt wird ohnehin nichts, siehe Grundregel 1.

**Eigener Ton, über die Zeit.** Wie der Vermieter selbst schreibt, steht
anfangs nirgends. Wenn er einen Entwurf ändert, halte fest, was er geändert
hat, und schreib es nach `doku\Schreibstil.md`. Nach ein paar Monaten passen
die Entwürfe dann von selbst und müssen nicht mehr nachbearbeitet werden.

## Lange Sitzungen

Bei der Ersterfassung von 20 bis 30 Einheiten kann eine Sitzung an ihre Grenze
kommen. Damit das nichts kostet:

- **Nach jedem Objekt sofort in die Datei schreiben**, nicht am Ende alles
  zusammen. Eine abgebrochene Sitzung verliert dann nichts.
- **Verträge nicht auf Vorrat lesen.** Eine Excel-Liste mit 30 Einheiten sind
  rund 1.500 Tokens, also nichts. Ein zehnseitiger Mietvertrag als PDF liegt
  bei grob 10.000 bis 16.000. Öffne einen Vertrag nur, wenn eine bestimmte
  Angabe fehlt, zieh sie heraus, schreib sie weg, weiter.
- **Wiedereinstieg** ist immer möglich: neue Sitzung, „Weiter erfassen",
  `py -3 skripte\pruefen.py` zeigt den Stand.
- **Erst ein Objekt komplett durch die ganze Kette**, dann der Rest. Klemmt
  etwas an der Zuordnung, merkt man es nach einem Objekt statt nach dreißig.

## Der monatliche Ablauf

Einmal im Monat, wenn die Mieten durch sind:

1. Umsätze im Online-Banking als CSV exportieren, Datei nach `kontoauszuege\`.
2. `py -3 skripte\umsaetze_importieren.py`
3. Unklare Zuordnungen gemeinsam klären.
4. `py -3 skripte\rueckstaende.py`, offene Posten besprechen.
5. Bei Bedarf Zahlungserinnerungen entwerfen und vorlegen.
6. `py -3 skripte\dashboard_bauen.py` und Ergebnis zeigen.

Das dauert bei rund 30 Einheiten wenige Minuten, solange die Stammdaten
gepflegt sind.

## Wie die Zuordnung funktioniert

Jeder Zahlungseingang wird gegen jedes aktive Mietverhältnis bewertet:
identische IBAN 60 Punkte, Mietername im Text bis 30, passender Betrag bis 25,
Objektname im Verwendungszweck 15, das Wort Miete 5. Ab 70 Punkten gilt die
Zuordnung als sicher, zwischen 40 und 69 als Vorschlag, darunter bleibt sie
offen. Die Schwellen stehen in `daten\konfig.json`.

Als bezahlt zählt nur, was sicher zugeordnet oder bestätigt wurde. Ein
ungeprüfter Vorschlag zählt nicht mit.

Den Abrechnungsmonat sucht das Skript zuerst im Verwendungszweck
(`Miete 08/2026`, `August 2026`). Steht dort nichts, gilt der Buchungsmonat.
Wird gegen Monatsende überwiesen und ist dieser Monat schon beglichen, wird
die Zahlung dem Folgemonat zugeordnet, weil das bei Daueraufträgen der
Normalfall ist.

## Wenn etwas nicht stimmt

Zahlen im Dashboard nie durch Anpassen der Daten geradebiegen. Stimmt eine
Summe nicht, fehlt entweder eine Buchung oder die Sollmiete ist veraltet.
Beides klärt eine Rückfrage. `py -3 skripte\pruefen.py` findet die häufigsten
Ursachen von selbst.
