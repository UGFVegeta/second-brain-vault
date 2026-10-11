---
tags: [ressource, claude, mods]
date: 2026-10-11
status: aktiv
---

# Prompt: Mods auf einem zweiten Mac einrichten

Für einen anderen Mac mit eigenem Claude Code (z. B. für Lehrkräfte). In eine neue Claude-Code-Session einfügen. Claude wertet erst die eigenen Sessions aus, interviewt die Person, schlägt passende Mods vor und baut nur die ausgewählten, ohne Oskars Pfade. Siehe [[Zusammenarbeit mit Claude]].

```text
Ich möchte Claude Code mit „Mods“ an meine Arbeit anpassen. Ich bin Lehrerin, habe ein Claude-Pro-Abo und will vor allem Tokens und Limit sparen. Mein Mann hat das schon bei sich gemacht; unten steht, welche Mods sich bewährt haben und welche Fehler er dabei gemacht hat.

So gehst du vor:

SCHRITT 1 – Kennenlernen (noch nichts bauen)
- Werte zuerst meine bisherigen Claude-Code-Sessions aus (die Verläufe liegen unter ~/.claude/projects/). Schau, wofür ich Claude nutze, was ich oft wiederhole, wo ich korrigieren muss und wo viele Tokens draufgehen. Lies dabei keine Schülernamen oder Noten mit, sondern werte nur Muster und Häufigkeiten aus.
- Dann interviewe mich, immer nur 2 bis 3 Fragen auf einmal, bis du mich gut kennst. Mindestens: Welche Fächer und Klassen habe ich? Wie bereite ich Unterricht vor und was nervt mich dabei? Diktiere ich meine Nachrichten? Welche Apps nutze ich (Apple-Erinnerungen und ihre Listen, Kalender, Notizen, Browser)? Wo liegen meine Klassen- und Notenlisten? Bei welchen Aufgaben wäre mir Opus statt Sonnet wichtig? Wie oft stoße ich an das Limit?
- Fass danach in wenigen Sätzen zusammen, was du über meine Arbeitsweise verstanden hast, und lass mich korrigieren.

SCHRITT 2 – Vorschlag
- Schlag mir eine Auswahl aus dem Baukasten unten vor, angepasst auf meine Antworten, gern auch eigene Ideen. Als Tabelle: Mod, was er macht, was er mir bringt, Empfehlung ja/nein. Ich entscheide, was gebaut wird.

SCHRITT 3 – Bauen
- Lade zuerst den Skill zum Bauen von Mods (plugin-authoring) und lies die Typen, bevor du Code schreibst.
- Baue die gewählten Mods nacheinander, jeden in einem eigenen Ordner unter ~/.claude/mods/<name>/, prüfe jeden mit `claude plugin validate` und teste die Logik mit erfundenen Beispielen. Sag mir nach jedem Mod in zwei, drei Sätzen, was er macht.
- Am Ende sollen alle Ordner in ~/.claude/settings.json unter env → CLAUDE_CODE_PLUGIN_DIRS stehen (durch Doppelpunkt getrennt). Wenn du diese Datei nicht ändern darfst, gib mir den Befehl, ich führe ihn selbst aus.
- Schreib mir zum Schluss eine kurze Anleitung in die Notizen-App („Claude-Mods – Kurzanleitung“) und merk dir meine Antworten aus dem Interview für spätere Sessions.

BAUKASTEN (Vorschläge, nicht automatisch alles bauen)

A) „cockpit“ (eine Leiste über dem Eingabefeld, eine Zeile):
- Limit: 5-Stunden- und Wochenlimit als „X % genutzt, Reset in …“, Cache-Restzeit („warm, noch 42 min“ / „kalt“, Cache hält 60 min nach der letzten Antwort), Kontext in %. Farben: unter 50 % grün, ab 50 % gelb, ab 80 % rot. Hinweis-Toast bei 80 und 90 % Limit. Vor der ersten Antwort einer Session gibt es noch keine Werte: dann „Limit: Werte kommen mit der ersten Antwort“.
- Cache-Wächter: Schreibe ich nach mehr als 60 min Pause in eine Session mit mindestens 30.000 Tokens Kontext, Nachricht anhalten, Text zurück ins Eingabefeld legen und melden „Cache ist kalt, etwa N Tokens würden neu eingelesen. Nochmal Enter = trotzdem senden.“ Zweites Enter innerhalb 10 min geht durch. Letzte Antwortzeit pro Session in $.store merken (überlebt Neustart).
- /warmhalten 90: kurz vor Ablauf des Caches eine Mini-Nachricht schicken („bitte nur mit ok antworten“), bis die Zeit um ist; /warmhalten 0 beendet.
- Knopf „Zusammenfassen“ ab 50 % Kontext ($.session.compact), nur wenn Claude gerade nicht arbeitet.
- Modellwahl nur bei der ERSTEN Nachricht einer Session (ein Modellwechsel mittendrin verwirft den Cache): passt die Nachricht zu meinen Opus-Stichwörtern, anhalten und Knöpfe „Mit Opus senden“ / „Mit aktuellem Modell“ zeigen; nochmal Enter = aktuelles Modell. Opus nur zurückhaltend vorschlagen (verbraucht das Limit schneller).
- Denktiefe (Effort) ebenfalls nur bei der ersten Nachricht festlegen und per turn.step für die ganze Session halten: Opus-Fälle hoch, Routine (Postfach, Zwischenablage, nur Grammatik, „wo liegt …“) niedrig, sonst Standard. Anzeige in der Leiste, /denktiefe niedrig|mittel|hoch|standard zum Umstellen.
- Schutz vor Löschen: vor rm, rmdir, find -delete, git reset --hard/clean/restore/force push, endgültigem Löschen von Mails, AppleScript-delete und HTTP DELETE einen Dialog ($.ui.ask) mit „Ausführen“, „Für diese Session erlauben“, „Abbrechen“ und einer Vorschau (wie viele Dateien, wie groß). Ohne Dialog: /tmp, Scratchpad, Dateien mit _ vorn, _alt-Ordner. Heredoc-Inhalte (Python-Code) nicht prüfen, Shell-Variablen auflösen, Wörter mit Anführungszeichen richtig zusammenhalten. Bei Fehlern im Mod lieber nachfragen als durchlassen. Bei Ablehnung soll Claude nicht ausweichen, sondern mich fragen.

B) „alltag“:
- Beginnt eine Nachricht mit „Erinnere mich …“, „Erinnerung:“ oder „To-do:“ (eine Zeile, höchstens 250 Zeichen), nicht an Claude schicken, sondern per AppleScript direkt in Apple-Erinnerungen anlegen (im Hintergrund, Reminders braucht ~10 s; sofort Bestätigung, danach Toast). Erkennen: heute, morgen, übermorgen, Wochentage, 12.10., 18 Uhr, 7:30, früh/mittags/abends. Ohne Datum in die Inbox-Liste, mit Datum in die Standardliste, Vorsatz „Familie:“ in die Familienliste. Achtung: \b kennt kein „ü“ (übermorgen) → Unicode-Lookarounds.
- „Merk dir …“ NICHT abfangen.
- Panel /heute mit fälligen Erinnerungen und ✓ zum Abhaken. Kalender per AppleScript ist sehr langsam (bis 40 s) und braucht die laufende Kalender-App; nur einbauen, wenn es schnell genug geht.
- Knöpfe dürfen NIE selbst etwas an Claude abschicken, nur Text ins Eingabefeld legen ($.prompt.fill).

C) „namensschutz“ (Datenschutz für Schülernamen):
- Ein lokales Python-Skript (~/.config/claude-namen/namen_aufbauen.py) liest meine Klassen-, Noten- und Sportlisten (xlsx/csv, Spalten wie Name/Vorname/Nachname) und baut eine Tabelle Original → Platzhalter (z. B. „SuS-001“ für ganze Namen, „Name-042“ für Einzelwörter, „SuS-001r“ für „Nachname, Vorname“). Rechte 600. Das Skript gibt NUR Zahlen aus.
- WICHTIG: Du (Claude) liest weder die Listen noch die Tabelle und startest das Skript nicht selbst. Ich starte es im Terminal.
- Der Mod ersetzt Namen in meinen Nachrichten, in allen Werkzeug-Ergebnissen und im Startkontext durch die Platzhalter (auch mit Genitiv-s: „Lenas“ → „Name-001s“) und setzt sie nur in lokale Werkzeuge (Bash, Read, Write, Edit, Glob, Grep) wieder ein, nie in Websuche, Online-Dienste oder MCP. Platzhalter-Muster mit \d{3,}, nicht genau drei Ziffern. Bei Fehlern zurückhalten statt ungefiltert weitergeben. Ausnahmen-Datei für Wörter, die fälschlich ersetzt werden. Befehl /namensschutz-neu baut die Tabelle neu.
- Nicht abgedeckt sind PDFs und Bilder, die Claude direkt öffnet. Das sag mir bitte deutlich.

TECHNISCHE FALLEN (hat mein Mann schon erlebt)
- Kein Variablenname „h“: das ist die JSX-Fabrik, sonst „h is not a function“.
- Mehrere Mods zeichnen über dem Eingabefeld: jeder AbovePrompt-Hook muss `await next(e)` einbinden, sonst verdeckt einer den anderen.
- Pro Modul nur EIN prompt.submit-Hook ohne Matcher; mehrere Prüfungen in einen zusammenfassen.
- Funktionen, die $ bekommen, auf oberster Ebene deklarieren.
- turn.step ist ein Streaming-Event: `async function* ($, e, next) { return yield* next({...e, effort}) }`.
- Zum Prüfen das Claude aus der App nehmen (~/Library/Application Support/Claude/claude-code/<Version>/…/claude.app/Contents/MacOS/claude plugin validate), das `claude` im Terminal kann veraltet sein.
- Laufende Sessions laden Änderungen nicht nach: zum Testen eine neue Session öffnen.
```
