---
tags: [schule, noten, excel, dashboard, werkzeug]
status: aktiv
date: 2026-07-05
---

# Notenlisten und Noten-Dashboard

System für Notenverwaltung in Mathe und Physik: Excel-Vorlagen + lokales HTML-Dashboard. Alles liegt in **„GDRS ICloud/"** (iCloud), **nicht** im Vault – die Dateien enthalten später Schülernamen und Noten.

## Excel-Vorlagen

| Vorlage | Ort | Aufbau |
|---|---|---|
| Mathe 5–9 („Notenliste N Mathematik leer v2.xlsx") | Schuljahr 25 26/Mathematik/ | 6 Kurztests, 4 KAs, 4 Mü, ein Blatt |
| Mathe 10 | Schuljahr 25 26/Mathematik/ | wie 5–9 + Anmeldenote, Prüfungsnote, Abschlussnote |
| Physik 7–10 („Notenliste Physik N leer.xlsx") | Physik/ (jahresunabhängige Grundlagen) | 2 Kurztests, 2 KAs, 2 Mü, **7 Klassenblätter a–g** |

**Gewichtungen** (stehen als blaue, änderbare Zellen in Zeile 2 jeder Liste):
- Mathe: schriftlich 80 % / mündlich 20 %
- Physik: schriftlich ⅔ / mündlich ⅓
- Beide: 1 Kurztest zählt 0,5 Klassenarbeit (gewichteter Schnitt über die tatsächlich vorhandenen Noten)
- Klasse 10: Abschlussnote = Jahresleistung/Prüfung 50:50, **zweite Nachkommastelle abgeschnitten** (ABRUNDEN, 1,65 → 1,6)

**Eigenschaften:** Formeln in allen 30 Zeilen, leere Zeilen bleiben leer (keine #DIV/0!), Formelzellen per Blattschutz ohne Passwort gesperrt, Wechselschattierung, Ampel auf berechneten Endnoten (rot ≥ 4,5, grün ≤ 2,5), Zeugnis-Spalten erlauben Tendenznoten als Text („4-").

## Noten-Dashboard

Drei Dateien direkt in „GDRS ICloud/":
- **Noten-Dashboard.html** – eigenständige Ansicht (Kacheln pro Klasse → Tabelle, Notenverteilung, Klassenschnitt je Arbeit, Risikoliste). „In Excel bearbeiten"-Knopf nutzt das `ms-excel:`-URL-Schema.
- **Dashboard aktualisieren.command** – Doppelklick: liest alle Listen neu ein und öffnet das Dashboard.
- **build_dashboard.py** – das Skript. Scannt automatisch den **neuesten** „Schuljahr …"-Ordner, darin Mathematik/ und Physik/.

**Konventionen:**
- Blattname in Excel = Klassenname im Dashboard (Umbenennen wirkt nach Aktualisieren). Generische Blattnamen („Notenliste", „Tabelle1") ziehen die Klasse aus der Ziffer im Dateinamen.
- Nur Blätter mit mindestens einem Schülernamen erscheinen; Dateien mit `~$`-Präfix und leere Vorlagen werden ignoriert.
- Klasse-10-Listen werden am Spaltenformat erkannt (Anmeldenote/Prüfungsnote/Abschlussnote) und zeigen den Prüfungsteil mit.
- Das Skript rechnet Schnitte selbst (mit den Gewichten aus Zeile 2) – funktioniert auch, wenn Excel die Datei noch nie durchgerechnet hat.

**Jahres-Workflow:** Vorlage in den neuen Schuljahresordner kopieren, umbenennen, ungenutzte Klassenblätter löschen, Namen eintragen. Das Dashboard folgt automatisch dem neuesten Schuljahr-Ordner.

## Datenschutz

Gefüllte Listen und das Dashboard enthalten personenbezogene Daten: nicht weitergeben, nicht ins Vault, perspektivisch dienstlicher Speicher statt iCloud. Im Vault liegt nur diese Doku.
