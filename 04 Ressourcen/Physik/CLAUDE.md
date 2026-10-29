# Physik: Anleitung für Claude

Zuerst lesen: [[Physik]] (Themenordner, Dashboard, Planung). Dort stehen Stoffverteilung und Jahresplanung. Nur die Dateien lesen, die die Aufgabe braucht.

## Aufbau einer Stunde (Klasse 7 Optik, Klasse 10 Kernphysik)
- Eine Stunden-HTML mit echten Tabs: Überblick, Folien, Heft, Hintergrund, Arbeitsblätter. Folie ist gleich Tafelbild, nie getrennt. Keine Zeiten, kein Verlauf, kein Merkheft, keine Hausaufgaben.
- Unterricht ohne Arbeitsblatt, Schüler zeichnen mit. Leere Zwillingsfolie nur dort, wo Oskar wirklich vorzeichnet. Blätter nur als Alternative im Tab, Ausnahmen: Spiegel, Spiegelbild, Auge, Zerfallsreihen.
- Eine Versuchsfolie pro Versuch (Material, Durchführung, ohne Beobachtung). Beobachte-Folien nehmen das Ergebnis nie vorweg.
- Leitfragen bleiben Fragen, Aussagesätze nur auf Ergebnisfolien. Hefteinträge nummerieren pro Leitfrage („4.1 …“).
- Material als Tabelle Demo (für dich) / Schülerversuch (pro Gruppe).
- Passt ein Labor, steht es sichtbar auf Folie, im Überblick und im Heft.
- Das Buch „Erlebnis Physik“ ist Oskars Fundgrube: Ideen abwandeln, nie Text kopieren, nie als Schüleraufgabe angeben.
- Erst Oskars Konzept erfragen, dann mit dem Buch abgleichen.

## Stil
- Folienstil V1: schwarzer Kopfbalken, weißer Grund, Fußzeile, Check als Kacheln A–D mit eigener Lösungsfolie. Steckt in `Optik/folien.css` (`stil-v1`) und `stilisiere()` in `Optik/stunde_vorlage.py`.
- Zeichnungen im Labor-Stil auf hellem Karo (`folien_zeichnungen.py`, `kern_zeichnungen*.py`). Diagramme als berechnete SVG, Konventionen in `00 Kontext/Physik-Diagramme Konventionen.md`.
- Jede Aufgabe auf Blättern mit Schwierigkeitskreisen ○ ◐ ●, Lösung immer als dasselbe Blatt ausgefüllt.
- Strahlenwerte nach BfS, nicht nach Buch.

## Nach jeder Änderung
- Stunde bauen (`Optik/baue_stunden_*.py`, Kernphysik `baue_stunden_k10*.py`), PDFs auch mit `sips -s format png` prüfen, nicht nur mit pdftoppm.
- Export nach iCloud erst nach Freigabe durch Oskar (`export_icloud.py`, `Kernphysik/export_icloud_k10.py`).
- Neue Stunden im Bildungs-Dashboard eintragen (`.scripts/bildungs_dashboard_bauen.py`). Stoffverteilung geändert: `python3 .scripts/stundenkontext_bauen.py`.
- HTML in Chrome zeigen (`.scripts/chrome_zeigen.py`).
- Keine Schülernamen oder Noten im Vault.

## Gelernt
Siehe [[Gelernt]].
