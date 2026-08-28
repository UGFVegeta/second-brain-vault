# Bankanbindung

Es gibt drei Wege, die Kontoumsätze in die Verwaltung zu bekommen. Der erste
funktioniert sofort und immer, der zweite ist bequemer und braucht einen
Nachmittag Einrichtung, der dritte ist eine Rückfallebene.

## 1. CSV-Export (empfohlen für den Anfang)

Im Online-Banking die Umsätze eines Zeitraums als CSV exportieren, die Datei
in den Ordner `kontoauszuege\` legen, dann `2 Kontoauszug einlesen.bat`
anklicken.

Das dauert einmal im Monat etwa eine Minute. Die eigentliche Arbeit, also die
Zuordnung der Zahlungen zu den Mietverhältnissen, passiert danach ohnehin
automatisch. Der Unterschied zwischen CSV und Direktabruf ist nur diese eine
Minute.

Erkannt werden die Exportformate der gängigen Banken. Die Spalten werden
anhand ihrer Überschriften gefunden, es muss also nichts umbenannt werden.
Auch camt.052- und camt.053-XML werden gelesen.

Kommt die Meldung, dass keine Spalten für Datum und Betrag gefunden wurden:
die ersten Zeilen der Datei ansehen und Claude zeigen. Die Spaltennamen
werden dann in `skripte\umsaetze_importieren.py` in der Tabelle `SPALTEN`
ergänzt, das ist eine Zeile.

## 2. FinTS, direkt bei der Bank

FinTS (früher HBCI) ist der deutsche Standard für den Kontozugriff. Fast alle
Sparkassen, Volksbanken und viele Privatbanken unterstützen ihn. Es fällt kein
Drittanbieter an, die Daten gehen direkt von der Bank auf den eigenen Rechner.

### Einrichtung

**Schritt 1: Bibliothek installieren**

```
py -3 -m pip install fints
```

Die Bibliothek `fints` wird gepflegt, Stand August 2026 ist Version 5.0.0 vom
Januar 2026 aktuell.

**Schritt 2: Zugangsdaten hinterlegen**

```
py -3 skripte\fints_abruf.py
```

Beim ersten Lauf legt das Skript eine Vorlage an unter
`%USERPROFILE%\.mietverwaltung\fints.json`, also außerhalb des Projektordners.
Dort einzutragen sind:

- `blz` – Bankleitzahl
- `benutzerkennung` – der Anmeldename aus dem Online-Banking
- `endpunkt` – die FinTS-Adresse der Bank
- `produkt_id` – siehe unten, oft erst einmal leer lassen
- `konto_iban` – das Konto, auf dem die Mieten eingehen

**Die PIN kommt nicht in diese Datei.** Sie wird bei jedem Lauf abgefragt und
nirgends gespeichert.

Die FinTS-Adresse der eigenen Bank erfährt man am zuverlässigsten bei der Bank
selbst: in den Hilfeseiten des Online-Bankings, beim Kundenservice, oder über
eine Suche nach dem Banknamen zusammen mit „FinTS Zugang". Raten hilft hier
nicht weiter, jede Bank hat ihre eigene.

**Schritt 3: Abrufen**

```
py -3 skripte\fints_abruf.py 180
```

Holt die Umsätze der letzten 180 Tage und ordnet sie sofort zu.

### Was dabei schiefgehen kann

**Produkt-ID.** FinTS verlangt eigentlich eine bei der Deutschen
Kreditwirtschaft registrierte Kennung des zugreifenden Programms. Manche
Banken nehmen es damit locker, andere weisen unregistrierte Zugriffe ab. Ob
die eigene Bank mitspielt, zeigt erst der erste Verbindungsversuch. Wenn
nicht, kann man eine Produkt-ID bei der Deutschen Kreditwirtschaft
registrieren lassen; das ist ein Formularvorgang und dauert.

**Starke Kundenauthentifizierung.** Seit PSD2 verlangen Banken regelmäßig eine
TAN-Bestätigung für den Kontozugriff, üblicherweise alle 90 Tage. Dazwischen
läuft der Abruf ohne Zutun. Man muss sich also nicht wöchentlich anmelden,
aber ein paar Mal im Jahr kommt eine TAN-Abfrage.

**TAN-Verfahren.** Beim ersten Lauf fragt das Skript, welches Verfahren
verwendet werden soll (pushTAN, chipTAN, SMS). Das läuft über die
Standardabfrage der Bibliothek.

Wenn irgendetwas davon klemmt: Der CSV-Weg funktioniert weiterhin. Es ist kein
Zustand, in dem etwas kaputt wäre, sondern nur eine Bequemlichkeit weniger.

## 3. Open-Banking-Anbieter

Dienste wie Enable Banking oder Nordigen bieten Kontozugriff über eine
Web-Schnittstelle an. Für eine einzelne private Nutzung ist das meist der
umständlichste Weg, weil ein Konto beim Anbieter nötig ist und die
Kontodaten über dessen Server laufen.

Die Konditionen dieser Anbieter ändern sich häufig und ich habe sie nicht
geprüft. Wer diesen Weg gehen will, sollte die aktuellen Preise und
Nutzungsbedingungen selbst nachlesen, bevor er sich darauf verlässt.

Für die hier vorliegende Verwaltung spricht ohnehin wenig dafür: Bei zwei bis
drei Konten und einem monatlichen Rhythmus ist der CSV-Export schlicht
einfacher.

## Lohnt sich der Direktabruf überhaupt?

Die ehrliche Rechnung, weil die Frage regelmäßig aufkommt:

**Was der Direktabruf einspart:** den CSV-Export im Online-Banking. Das ist
einmal im Monat etwa eine Minute.

**Was er kostet:** einen Nachmittag Einrichtung, gelegentliche Pflege wenn die
Bank ihr TAN-Verfahren oder ihre Adresse ändert, und die Eigenschaft, dass er
irgendwann leise aufhören kann zu funktionieren, ohne dass es jemand merkt.

Bei einem monatlichen Rhythmus lohnt sich das nicht. Eine gesparte Minute im
Monat wiegt einen Einrichtungsnachmittag nicht auf.

**Wann es sich doch lohnt:** wenn die Umsätze nicht monatlich, sondern täglich
geholt werden sollen. Also wenn die Verwaltung von selbst melden soll, dass
eine Miete fehlt, dass jemand plötzlich 50 Euro zu wenig überweist oder dass
eine Zahlung doppelt kam. Täglich exportiert von Hand niemand. Ab diesem Punkt
trägt sich die Automatik, vorher nicht.

**Zwei Haken, die man vorher kennen sollte:**

- **Vollautomatisch gibt es nicht.** Seit PSD2 verlangt die Bank regelmäßig
  eine TAN, typischerweise alle 90 Tage. Ein geplanter Abruf bleibt an dieser
  Stelle stehen und wartet auf eine Eingabe. Das ist kein Fehler, sondern
  Vorschrift.
- **Unbeaufsichtigt heißt: PIN gespeichert.** Solange die PIN bei jedem Lauf
  eingegeben wird, kann kein Zeitplan sie automatisch abrufen. Wer wirklich
  jeden Morgen automatisch abrufen will, muss die PIN hinterlegen. Dann
  gehört sie in die Windows-Anmeldeinformationsverwaltung und nicht in eine
  Textdatei. Das ist eine bewusste Abwägung, keine Kleinigkeit.

**Fazit:** monatlich CSV, täglich FinTS. Und wenn automatisiert wird, dann
über FinTS und nicht über einen Open-Banking-Anbieter, weil die Kontodaten
so nicht über fremde Server laufen.

## Empfehlung

Mit CSV anfangen. Wenn das nach ein paar Monaten läuft und die eine Minute im
Monat wirklich stört, FinTS in Ruhe einrichten. Umgekehrt, also mit FinTS
starten und sich am ersten Abend mit Produkt-IDs und TAN-Verfahren
herumschlagen, verdirbt nur den Spaß an einer Sache, die sonst gut
funktioniert.
