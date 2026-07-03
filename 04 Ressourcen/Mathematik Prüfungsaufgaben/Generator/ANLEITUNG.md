# Aufgabenpool Generator – Anleitung

## Bestehende Themen
| Thema | Aufgaben |
|---|---|
| Trigonometrie | 20 |
| Quadratische Funktionen | 20 |
| Stochastik | 20 |
| Sachrechnen | 15 |
| Boxplot & Datenanalyse | 15 |
| Stereometrie | 15 |
| Kurzaufgaben (Zeitfüller) | 20 |

> **Kurzaufgaben (Zeitfüller):** kurze Zusatzaufgaben für die letzten Minuten (Sinus-Vorzeichen/-Vergleich, Wurzeln ergänzen, wissenschaftliche Schreibweise, Gleichungen, binomische Formeln, Potenzgesetze). Erzeugt mit `gen_kurz.py`. Bewusst **aus dem zufälligen Prüfungssatz (`Pruefung.html`) ausgeschlossen** (`EXAM_EXCLUDE` in `build_exam.py`), im **Baukasten aber wählbar**. Mathe-Darstellung (Wurzeln/Brüche/Box) per CSS – die Klassen liegen in `gen_kurz.py` (`MATH_CSS`) und in `build_exam.py` (`MATH_CSS_EXAM`).

## Neues Thema anlegen

**In einer neuen Session** einfach folgendes sagen:

> Erstelle einen neuen Aufgabenpool für mündliche Prüfungen zum Thema **[THEMA]**.
> Vorlage und Skripte liegen unter `04 Ressourcen/Mathematik Prüfungsaufgaben/Generator/`.
> 15 Aufgaben, HTML + .md, Schwierigkeitsterne, Druck 3/Seite – genau wie die bestehenden Pools.
>
> Aufgaben:
> 1. [Aufgabe] → Lösung: [Lösung]
> 2. …

## Schwierigkeitssterne
Jede Aufgabe bekommt 1–3 Sterne (★). Sie erscheinen **sowohl im HTML als auch im `.md`**:
- **HTML:** neben der Aufgabennummer – via `patch_stars.py` (Druck-CSS inklusive).
- **`.md`:** als Zeile `*Schwierigkeit: ★★☆*` direkt unter der Überschrift – via `patch_md_stars.py`.

Bei einem neuen Pool werden die Sterne direkt mitgebaut (siehe `gen_stereo.py` als Vorlage – Sterne in HTML **und** `.md`). Bestehende Pools lassen sich mit den beiden `patch_*`-Skripten nachrüsten (sie überspringen bereits gepatchte Dateien).

## Prüfungsgenerator
Eure mündliche Prüfung mit **Wahlthema**: **1 Aufgabe zum Wahlthema** (intensiver gefragt) + **5 gemischte** aus allen Themen.

- **`Pruefung.html` (Zufall):** themenübergreifender Prüfungssatz. Wahlthema + Schwierigkeit + Anzahl wählen → „🎲 Prüfungssatz erstellen" → 1 Wahlthema-Aufgabe + 5 gemischte aus **5 verschiedenen anderen Themen** (Themen-Balance), aufsteigend nach Schwierigkeit sortiert. Schwierigkeit wahlweise exakt (★/★★/★★★) oder **„⚖️ ausgewogen"** (2·★, 2·★★, 2·★★★ pro Satz). **Serien-Modus:** bis zu 10 Sätze auf einmal ohne Aufgaben-Überschneidung (z. B. 8 Sätze für 8 Schüler) – jeder Satz mit Name/Datum-Zeile und beim Druck auf eigener Seite. **Verwendet-Abgleich:** nutzt denselben `localStorage`-Speicher wie der Baukasten; „verwendete ausschließen" (Standard: an) überspringt bereits markierte Aufgaben, **„✓ Satz als verwendet markieren"** sperrt die gezogenen Aufgaben für künftige Sätze und den Baukasten, „↺" gibt alle wieder frei. Zwei Druck-Buttons: **„🖨️ Drucken (Schüler)"** ohne Lösungen und **„🖨️ Mit Lösung (Lehrer)"** als Lösungsblatt.
- **`Baukasten.html` (manuell):** visueller Katalog **aller** Aufgaben (mit Bild). 6–8 anklicken → zwei Druck-Buttons: **„🖨️ Drucken (Schüler)"** (ohne Lösung) und **„🖨️ Mit Lösung (Lehrer)"** (gleiche Auswahl, mit Lösungsbox je Aufgabe). „✓ Als verwendet markieren" blendet sie dauerhaft aus (im Browser via `localStorage` gespeichert), „↺ Zurücksetzen" gibt wieder alle frei – so lassen sich für mehrere Schüler unterschiedliche Prüfungen ohne Doppelung bauen.
- **Lösungs-Druck technisch:** `build_exam.py` zieht beim Einsammeln neben dem Aufgabentext auch den Inhalt des `<div class="sol">` jeder Karte (Feld `sol` in `DATA`). Beim Lehrer-Druck wird er als grüne `.solbox` unter der Aufgabe eingeblendet – funktioniert automatisch für alle Pools, nichts extra nötig.
- Beide Seiten werden von **`build_exam.py`** erzeugt (sammelt alle Aufgaben aus den 6 Pools ein und bettet sie samt Figuren ein). **`build_exam.py` aktualisiert außerdem automatisch die Zähler-Badges, die Gesamtsumme und das Datum in `index.html`** – nach jedem Hinzufügen von Aufgaben einfach `build_exam.py` laufen lassen, dann stimmen die Zahlen überall.
- **`index.html`:** Block „🎲 Prüfung erstellen" – Wahlthema + Schwierigkeit + Anzahl wählen, springt nach `Pruefung.html?thema=…&diff=…&num=…` (erstellt die Sätze automatisch).
- **In jedem Pool (zum Üben *eines* Themas):** Panel „Prüfung" + Button **„🎲 6 Aufgaben ziehen"** – markiert 6 zufällige Aufgaben dieses Themas, dann „Auswahl drucken". Eingebaut über `patch_draw.py` (idempotent).

**Workflow nach Neubau/Änderung von Aufgaben** (Reihenfolge):
`gen_<thema>.py` → `patch_stars.py` → `patch_md_stars.py` → `patch_draw.py` → **`build_exam.py`**.
⚠️ Ein HTML-Neubau (z. B. `gen_stereo.py`) überschreibt die Injektionen → danach `patch_stars.py` und `patch_draw.py` erneut laufen lassen, anschließend `build_exam.py` (damit `Pruefung.html` die Änderungen enthält).

## Tipps für Token-Ersparnis
- **Aufgaben als reinen Text** eingeben – kein Foto/Screenshot
- **Neue Session pro Thema** – nach /clear keine alten Bilder mehr im Kontext
- **Sonnet** für Routine-Generierung reicht völlig
