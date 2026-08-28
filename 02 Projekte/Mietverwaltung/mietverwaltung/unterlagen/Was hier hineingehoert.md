# Unterlagen

Hier kommt alles hinein, was es über die Wohnungen schon gibt. Claude liest es
aus und übernimmt die Angaben, statt sie abzufragen.

**Was sich verwerten lässt**

- Excel-Listen der Wohnungen und Mieter (`.xlsx`)
- Mietverträge als PDF, sofern sie Text enthalten und keine Scans sind
- Aufstellungen für den Steuerberater, Anlage V früherer Jahre
- Mieterlisten, Kautionsübersichten, Darlehensunterlagen
- CSV- oder Word-Dateien

**Was nicht geht**

- Eingescannte Verträge ohne Textebene. Das sind reine Bilder, daraus lässt
  sich nichts auslesen. Diese Angaben fragt Claude ab.
- Alte `.xls`-Dateien. Einmal in Excel als `.xlsx` speichern, dann geht es.

**Danach**

Claude sagen: „Lies meine Unterlagen ein." Er zeigt erst, was er verstanden
hat, und schreibt erst nach der Bestätigung in die Stammdaten.

Die Dateien bleiben auf diesem Rechner. Nach der Übernahme kann der Ordner
geleert werden, die Angaben stehen dann in `daten\`.
