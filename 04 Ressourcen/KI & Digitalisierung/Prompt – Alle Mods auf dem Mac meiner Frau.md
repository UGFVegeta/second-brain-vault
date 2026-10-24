---
tags: [ressource, claude, mods]
date: 2026-10-21
status: aktiv
---

# Prompt: Alle Mods auf dem Mac meiner Frau

Überarbeitete Fassung von [[Prompt – Mods auf einem zweiten Mac einrichten]] (Stand 21.10.2026). Unterschied zur ersten Fassung: Es werden standardmäßig alle fünf Mods gebaut, die Oskar hat (Stand heute inkl. Ablage, Namen-Anzeige, Stunden-Check, Diktat-Korrektur, Stundenkontext, Heute-Leiste). Alle Rückfragen laufen als Klick-Fragen (AskUserQuestion), freier Text nur, wo es nicht anders geht. In eine neue Claude-Code-Session auf dem Mac der Frau einfügen, Modell Opus mit hohem Effort empfohlen (viel Code, einmalig).

```text
Ich möchte, dass mein Claude Code dieselben „Mods“ hat wie das meines Mannes. Ich bin Lehrerin, habe ein Claude-Pro-Abo und will vor allem Tokens und Limit sparen. Mein Mann hat fünf Mods gebaut und sie über Wochen ausprobiert. Unten steht, was jeder kann und welche Fehler dabei passiert sind. Du baust sie für mich neu und passt sie an meine Arbeit an. Nimm nichts von seinen Pfaden, Namen oder Ordnern an, alles Persönliche fragst du bei mir ab.

WIE DU MIT MIR REDEST
- Stell alle Rückfragen mit dem Werkzeug AskUserQuestion, also als Klick-Auswahl, 2 bis 4 Fragen pro Runde, Antworten als Optionen, wo es geht (bei mehreren möglichen Antworten Mehrfachauswahl). Tipp-Text nur für Dinge, die ich selbst benennen muss (Ordnerpfade, Listennamen, Verhörer beim Diktieren).
- Frag nichts, was du selbst nachsehen kannst. Wenn ich bei einer Frage unsicher bin, schlag eine Voreinstellung vor und markier sie als empfohlen.
- Schreib kurz und in einfachem Deutsch. Sag nach jedem fertigen Mod in zwei, drei Sätzen, was er macht.

SCHRITT 0 – Bestandsaufnahme (nichts ändern)
- Schau nach, ob unter ~/.claude/mods/ schon etwas liegt und was in ~/.claude/settings.json unter env → CLAUDE_CODE_PLUGIN_DIRS steht. Bestehendes nie überschreiben, sondern vorher sichern.
- Prüf, welche Apps ich nutze: Erinnerungen, Kalender, Notizen, Mail, Browser, und welches Python da ist (python3 --version).
- Lade den Skill zum Bauen von Mods (plugin-authoring) und lies die Typen, bevor du Code schreibst.

SCHRITT 1 – Kennenlernen
- Werte zuerst meine bisherigen Claude-Code-Sessions aus (Verläufe unter ~/.claude/projects/). Schau, wofür ich Claude nutze, was ich wiederhole, wo ich korrigieren muss und wo viele Tokens draufgehen. Lies keine Schülernamen oder Noten mit, nur Muster und Häufigkeiten.
- Dann stell mir die Fragen per Klick. Mindestens:
  1. Fächer und Klassen (Mehrfachauswahl, dazu „Anderes“).
  2. Wo liegt mein Unterrichtsmaterial? (iCloud-Ordner, Vault/Notizen-Ordner, anderer Ordner; Pfad per Texteingabe.)
  3. Wo liegen Klassen-, Noten- und Sportlisten (Ordner, Dateiformat xlsx oder csv)?
  4. Wie heißen meine Erinnerungs-Listen, und welche ist die Standardliste? Welche Liste ist für Familie, welche für Schule, welche für schnelle Einfälle ohne Datum?
  5. Diktiere ich meine Nachrichten? Wenn ja, welche Wörter versteht die Diktierfunktion regelmäßig falsch (Texteingabe, lieber zu viele als zu wenige)?
  6. Bei welchen Aufgaben soll Opus statt Sonnet laufen (Mehrfachauswahl: Elternbriefe mit heiklem Inhalt, Bewerbungen und Konzepte, neue Unterrichtseinheiten, Gutachten, Anderes)? Wie wichtig ist mir, dass das Limit geschont wird?
  7. Wie oft stoße ich an das Limit (selten, manchmal, oft)?
  8. Habe ich Skripte, die Material in einen Cloud-Ordner exportieren (Ja, nennen / Nein)? Davon hängt der Export-Wächter ab.
  9. Welche Prüfungen soll der Stunden-Check bei frisch geänderten Unterrichtsmaterialien machen (Mehrfachauswahl, zum Beispiel: Lösungsblatt vorhanden, Schwierigkeitskreise ○ ◐ ● auf Arbeitsblättern, bestimmte Schreibregeln, Anderes)?
  10. Will ich ein Befinden-Tracking (abends Knöpfe 1 bis 5, schreibt in eine Notiz) und einen Gesundheits-Check an bestimmten Wochentagen? (Ja / Nein / Später.)
  11. Welche Mods will ich nicht? Standard: alle fünf, ich streiche nur, was ich nicht brauche.
- Fass danach in wenigen Sätzen zusammen, was du über meine Arbeitsweise verstanden hast, und lass mich per Klick bestätigen oder korrigieren.

SCHRITT 2 – Vorschlag
- Zeig mir eine Tabelle: Mod, was er macht, was er mir bringt, angepasst auf meine Antworten. Ich bestätige per Klick, was gebaut wird (Standard: alle fünf). Eigene Ideen sind willkommen.

SCHRITT 3 – Bauen
- Jeden Mod in einen eigenen Ordner ~/.claude/mods/<name>/, mit .claude-plugin/plugin.json und hooks/register.tsx (bzw. .ts, wenn keine Oberfläche nötig ist). Jeden mit `claude plugin validate` prüfen und die Logik mit erfundenen Beispielen testen.
- Am Ende alle Ordner in ~/.claude/settings.json unter env → CLAUDE_CODE_PLUGIN_DIRS eintragen (durch Doppelpunkt getrennt, Beispiel: ~/.claude/mods/schul-cockpit:~/.claude/mods/ablage). Wenn du diese Datei nicht ändern darfst (das blockiert der automatische Modus oft), gib mir den fertigen Befehl in einem eigenen Codeblock, ich führe ihn selbst im Terminal aus.
- Schreib mir zum Schluss eine kurze Anleitung in die Notizen-App („Claude-Mods – Kurzanleitung“: was jeder Mod kann, welche Befehle es gibt, wo die Einstellungsdateien liegen) und merk dir meine Antworten aus dem Interview für spätere Sessions.
- Sag mir, dass ich eine neue Session öffnen muss: laufende Sessions laden Mods nicht nach.

DIE FÜNF MODS

1) „schul-cockpit“ (Leiste über dem Eingabefeld, eine Zeile, Farben unter 50 % grün, ab 50 % gelb, ab 80 % rot)
- Limit: 5-Stunden- und Wochenlimit als „X % genutzt, Reset in …“, dazu Cache-Restzeit („warm, noch 42 min“ oder „kalt“; Cache hält 60 min nach der letzten Antwort) und Kontext in %. Toast bei 80 und 90 % Limit. Vor der ersten Antwort einer Session gibt es noch keine Werte, dann „Limit: Werte kommen mit der ersten Antwort“. Toast 10 min vor Cache-Ende, wenn der Kontext mindestens 20 % beträgt.
- Cache-Wächter: Schreibe ich nach mehr als 60 min Pause in eine Session mit mindestens 30.000 Tokens Kontext, die Nachricht anhalten, den Text zurück ins Eingabefeld legen und melden „Cache ist kalt, etwa N Tokens würden neu eingelesen. Nochmal Enter = trotzdem senden.“ Zweites Enter innerhalb 10 min geht durch. Letzte Antwortzeit pro Session in $.store merken (überlebt Neustart).
- /warmhalten N: kurz vor Ablauf des Caches eine Mini-Nachricht schicken („bitte nur mit ok antworten“), wenn mehr als 52 min seit der letzten Antwort vergangen sind, bis N Minuten um sind; /warmhalten 0 beendet.
- Knopf „Zusammenfassen“ ab 50 % Kontext ($.session.compact), nur wenn Claude gerade nicht arbeitet.
- Modellwahl nur bei der ERSTEN Nachricht einer Session (ein Modellwechsel mittendrin verwirft den Cache): passt die Nachricht zu meinen Opus-Stichwörtern aus Frage 6, anhalten und Knöpfe „Mit Opus senden“ und „Mit aktuellem Modell“ zeigen; nochmal Enter = aktuelles Modell. Opus nur zurückhaltend vorschlagen.
- Denktiefe (Effort) ebenfalls nur bei der ersten Nachricht festlegen und per turn.step für die ganze Session halten: Opus-Fälle hoch, Routine (Postfach, Zwischenablage, nur Grammatik, „wo liegt …“) niedrig, sonst Standard. Anzeige in der Leiste, /denktiefe niedrig|mittel|hoch|standard zum Umstellen.
- Schutz vor Löschen: vor rm, rmdir, unlink, find -delete, git reset --hard, git clean, git restore, git branch -D, force push, endgültigem Löschen von Mails (IMAP expunge), AppleScript-delete und HTTP DELETE einen Dialog ($.ui.ask) mit „Ausführen“, „Für diese Session erlauben“ (gilt pro Grund bis Session-Ende) und „Abbrechen“, dazu eine Vorschau (Anzahl Dateien, Größe, drei Beispielnamen). Ohne Dialog: /tmp, Scratchpad (auch über Variablen), Dateien mit _ vorn, Inhalte von _alt-Ordnern, Heredoc-Inhalte (Python-Code nicht prüfen). Shell-Variablen auflösen, Wörter mit Anführungszeichen richtig zusammenhalten. Bei Fehlern im Mod lieber nachfragen als durchlassen. Bei Ablehnung soll Claude nicht ausweichen, sondern mich fragen; die Meldung heißt „Vom Schutz-Mod gestoppt …“.
- Export-Wächter (nur wenn ich in Frage 8 Ja gesagt habe): nach jeder Antwort per `find -mmin` prüfen, ob in meinen Material-Ordnern etwas geändert wurde, das noch nicht per Export-Skript in den Cloud-Ordner ging; dann eine Leiste mit Knopf, der den Export startet. Nur echte Dateiänderungen zählen, nicht Bash-Befehle, in denen zufällig ein Ordnername vorkommt, und Dateien, die ein Export in derselben Antwort selbst erzeugt, nicht erneut melden. Neue Themenordner trägt man in einer Liste BEREICHE oben im Code nach.
- Stunden-Check: nach jeder Antwort (turn.complete) per `find -mmin` frisch geänderte Stunden-HTMLs in meinen Material-Ordnern prüfen (ohne Dateien mit _ vorn und ohne Übersichtsseiten), und zwar genau die Regeln aus Frage 9. Ergebnis als ✓/✗-Zeile in der Leiste; offene Punkte gehen bei der nächsten Nachricht unsichtbar als context an Claude, der sie dann behebt und kurz sagt, was er behoben hat.
- Diktat-Korrektur: Regeln in ~/.claude/mods/schul-cockpit/diktat.json als Liste aus regulärem Ausdruck (muster) und richtigem Wort (ersatz), startend mit meinen Verhörern aus Frage 5 (zum Beispiel Klot → Claude). Wörter, die auch richtig vorkommen können, nicht ersetzen. Ergänzen soll ich selbst können.
- Stundenkontext: wenn ich eine meiner Klassen oder Fächer erwähne, einmal pro Session und Klasse einen kurzen Kontext (aktuelle Woche, Thema, nächste Woche, Termine, Ferien oder Ausfall der nächsten 3 Wochen) aus ~/.claude/mods/schul-cockpit/stundenkontext.json mitgeben. Die Datei baut ein kleines Python-Skript aus meinen Stoffverteilungsplänen; frag mich, wo die liegen, und baue das Skript so, dass ich es nach Änderungen neu laufen lassen kann.

2) „ablage“
- Panel „Ablage“ (Befehl /ablage) mit allen Dateien, die in der Session per Write, Edit oder SendUserFile berührt wurden. Markiert, wo sie liegen (Notizen-Ordner, Cloud-Ordner, Scratchpad), mit Knöpfen „Öffnen“ und „Im Finder“.
- Öffnet am Ende jeder Antwort neue oder geänderte HTML-Dateien aus meinen Ordnern selbst im Browser (höchstens 4, vorhandenen Tab neu laden statt neuen öffnen, wenn das geht). Solange der Mod aktiv ist, soll Claude HTML nicht zusätzlich per `open -a` öffnen, sonst gibt es doppelte Tabs. Welchen Browser ich nutze, weißt du aus Schritt 0.

3) „alltag“
- Beginnt eine Nachricht mit „Erinnere mich …“, „Erinnerung: …“ oder „To-do: …“ (eine Zeile, höchstens 250 Zeichen), nicht an Claude schicken, sondern per AppleScript direkt in Apple-Erinnerungen anlegen. Im Hintergrund (Reminders braucht etwa 10 s), sofort eine Bestätigung, danach ein Toast. Datum erkennen: heute, morgen, übermorgen, Wochentage, 12.10., 18 Uhr, 7:30, früh/mittags/abends. Ohne Datum in meine Liste für schnelle Einfälle, mit Datum in die Standardliste, Vorsatz „Familie:“ oder „für die Familie“ in die Familienliste, „Schule:“ in die Schulliste (Listennamen aus Frage 4). Achtung: \b erkennt kein „ü“ (übermorgen), deshalb Unicode-Lookarounds nehmen.
- „Merk dir …“ NICHT abfangen, das ist ein Befehl für Claude.
- Leiste „Heute“ (Termine des Tages, fällige Erinnerungen live, alle 15 Minuten aktualisieren) und Panel /heute mit ✓ zum Abhaken. Kalender per AppleScript ist sehr langsam (bis 40 s) und braucht die laufende Kalender-App; die App vorher starten, nur einbauen, wenn es schnell genug geht, sonst die Termine aus einer Datei lesen, die ein Skript dreimal am Tag aktualisiert.
- Nur wenn ich in Frage 10 Ja gesagt habe: ab 18 Uhr Befinden-Knöpfe 1 bis 5 (schreibt eine Zeile in die von mir genannte Notiz, neueste oben), Knöpfe „Daily Note“, „Offenes → Erinnerungen“ und an den von mir genannten Wochentagen ein Gesundheits-Check-Knopf.
- Knöpfe dürfen NIE selbst etwas an Claude abschicken, nur Text ins Eingabefeld legen ($.prompt.fill).
- Beide Mods mit Leisten (schul-cockpit und alltag) müssen die Leiste des anderen mit einbinden (`await next(e)`).

4) „namensschutz“ (Datenschutz für Schülernamen)
- Ein lokales Python-Skript (~/.config/claude-namen/namen_aufbauen.py) liest meine Klassen-, Noten- und Sportlisten (xlsx oder csv, Spalten wie Name, Vorname, Nachname) aus den Ordnern aus Frage 3 und baut eine Tabelle Original → Platzhalter (zum Beispiel „SuS-001“ für ganze Namen, „Name-042“ für Einzelwörter, „SuS-001r“ für „Nachname, Vorname“). Dateirechte 600. Das Skript gibt NUR Zahlen aus.
- WICHTIG: Du liest weder die Listen noch die Tabelle und startest das Skript nicht selbst. Ich starte es im Terminal, gib mir den Befehl.
- Der Mod ersetzt Namen in meinen Nachrichten, in allen Werkzeug-Ergebnissen und im Startkontext durch die Platzhalter (auch mit Genitiv-s, „Name-967s“ → „Name-001s“) und setzt sie nur in lokalen Werkzeugen (Bash, Read, Write, Edit, Glob, Grep) wieder ein, nie in Websuche, Online-Diensten oder MCP, und nicht in Dateien, die in den Notizen-Ordner geschrieben werden. Platzhalter-Muster mit \d{3,}, nicht genau drei Ziffern. Bei Fehlern zurückhalten statt ungefiltert weitergeben. Eine Ausnahmen-Datei (ausnahmen.txt) für Wörter, die fälschlich ersetzt werden. Befehl /namensschutz-neu baut die Tabelle neu.
- Nicht abgedeckt sind PDFs und Bilder, die Claude direkt öffnet, und Namen außerhalb meiner Listen (zum Beispiel Kolleginnen und Kollegen). Das sag mir bitte deutlich.

5) „namen-anzeige“
- Zeigt mir im Chat die echten Namen statt der Platzhalter, nur auf dem Bildschirm (ui.render auf AssistantMessage), anhand derselben Tabelle wie der Namensschutz. Claude und das Transkript bleiben bei den Platzhaltern. Damit ich nicht denke, der Schutz sei kaputt.
- Wenn Claude für mich Texte in die Zwischenablage legt, geht das über Bash (pbcopy), dort werden die echten Namen eingesetzt. Zum Prüfen nicht pbpaste ausgeben lassen, nur Längen oder Ja/Nein.

TECHNISCHE FALLEN (mein Mann hat sie schon erlebt)
- Kein Variablenname „h“: das ist die JSX-Fabrik, sonst „h is not a function“.
- Mehrere Mods zeichnen über dem Eingabefeld: jeder AbovePrompt-Hook muss `await next(e)` einbinden, sonst verdeckt einer den anderen.
- Pro Modul nur EIN prompt.submit-Hook ohne Matcher; mehrere Prüfungen in einen zusammenfassen.
- Funktionen, die $ bekommen, auf oberster Ebene deklarieren.
- turn.step ist ein Streaming-Event: `async function* ($, e, next) { return yield* next({...e, effort}) }`.
- Zum Prüfen das Claude aus der App nehmen (~/Library/Application Support/Claude/claude-code/<Version>/…/claude.app/Contents/MacOS/claude plugin validate), das `claude` im Terminal kann veraltet sein.
- Für Skripte mit Excel- oder API-Zugriff das Python nehmen, das die nötigen Pakete hat (nicht blind das System-python3).
- Laufende Sessions laden Änderungen nicht nach: zum Testen immer eine neue Session öffnen.
- Zum Entwickeln darf ein Mod zuerst in einem Entwicklungsordner liegen, dauerhaft gehört er nach ~/.claude/mods/ und in CLAUDE_CODE_PLUGIN_DIRS.
```

## Gegenüber der ersten Fassung neu

- Standard ist „alle fünf Mods“, nicht „Auswahl aus dem Baukasten“.
- Klick-Fragen (AskUserQuestion) statt offenem Interview.
- Neu dabei: Mod „ablage“, Mod „namen-anzeige“, Stunden-Check, Diktat-Korrektur, Stundenkontext, Leiste „Heute“ mit Befinden-Knöpfen, Export-Wächter.
- Persönliche Dinge (Fächer, Pfade, Listennamen, Prüfregeln, Verhörer) fragt der Prompt ab, statt Oskars Werte zu übernehmen.
