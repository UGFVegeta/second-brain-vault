# Kontoauszüge

In diesen Ordner kommen die Exportdateien aus dem Online-Banking.

- **CSV** aller gängigen Banken wird erkannt, die Spalten werden anhand der
  Überschriften gefunden. Nichts umbenennen, nichts umsortieren.
- **camt.052 / camt.053 als XML** wird ebenfalls gelesen.

Danach `2 Kontoauszug einlesen.bat` anklicken oder Claude sagen:
„Lies die neuen Kontoauszüge ein."

Dieselbe Datei mehrfach einzulesen ist unproblematisch. Buchungen werden an
Datum, Betrag, IBAN und Verwendungszweck wiedererkannt und nicht doppelt
gezählt. Die Dateien können nach dem Einlesen liegen bleiben oder gelöscht
werden, die Buchungen stehen dann in `daten\zahlungen.json`.
