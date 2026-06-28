# Aufgabenpool Generator – Anleitung

## Bestehende Themen
| Thema | Aufgaben |
|---|---|
| Trigonometrie | 14 |
| Quadratische Funktionen | 15 |
| Stochastik | 15 |
| Sachrechnen | 15 |
| Boxplot & Datenanalyse | 15 |
| Stereometrie | 15 |

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

- **`Pruefung.html` (Zufall):** themenübergreifender Prüfungssatz. Wahlthema + Schwierigkeit wählen → „🎲 Prüfungssatz erstellen" → 1 Wahlthema-Aufgabe + 5 gemischte, druckbar ohne Lösungen.
- **`Baukasten.html` (manuell):** visueller Katalog **aller** Aufgaben (mit Bild). 6–8 anklicken → „🖨️ Auswahl drucken". „✓ Als verwendet markieren" blendet sie dauerhaft aus (im Browser via `localStorage` gespeichert), „↺ Zurücksetzen" gibt wieder alle frei – so lassen sich für mehrere Schüler unterschiedliche Prüfungen ohne Doppelung bauen.
- Beide Seiten werden von **`build_exam.py`** erzeugt (sammelt alle Aufgaben aus den 6 Pools ein und bettet sie samt Figuren ein).
- **`index.html`:** Block „🎲 Prüfung erstellen" – Wahlthema + Schwierigkeit wählen, springt nach `Pruefung.html?thema=…&diff=…` (erstellt den Satz automatisch).
- **In jedem Pool (zum Üben *eines* Themas):** Panel „Prüfung" + Button **„🎲 6 Aufgaben ziehen"** – markiert 6 zufällige Aufgaben dieses Themas, dann „Auswahl drucken". Eingebaut über `patch_draw.py` (idempotent).

**Workflow nach Neubau/Änderung von Aufgaben** (Reihenfolge):
`gen_<thema>.py` → `patch_stars.py` → `patch_md_stars.py` → `patch_draw.py` → **`build_exam.py`**.
⚠️ Ein HTML-Neubau (z. B. `gen_stereo.py`) überschreibt die Injektionen → danach `patch_stars.py` und `patch_draw.py` erneut laufen lassen, anschließend `build_exam.py` (damit `Pruefung.html` die Änderungen enthält).

## Tipps für Token-Ersparnis
- **Aufgaben als reinen Text** eingeben – kein Foto/Screenshot
- **Neue Session pro Thema** – nach /clear keine alten Bilder mehr im Kontext
- **Sonnet** für Routine-Generierung reicht völlig
