---
tags: [bereich, active-recall, lernen]
status: aktiv
date: 2026-08-29
---

# Active Recall

Werkzeug zum Lernen aus Büchern, Skripten und Texten über aktives Abrufen mit Rückmeldung.

## Prinzip

Nach dem Lesen die Quelle schließen und aus dem Kopf aufschreiben oder diktieren, was hängengeblieben ist. Danach Feedback: Was fehlt, was ist falsch, was ist unpräzise. Es geht nicht um die Eins-zu-eins-Wiedergabe, sondern um die zentralen Aussagen und ihre Zusammenhänge.

Belegt ist das gut. Abrufen schlägt Wiederlesen und Markieren deutlich (Testing-Effekt, Roediger & Karpicke 2006). Feedback nach dem Abruf verstärkt den Effekt. Verteilte Wiederholung über Tage und Wochen (Spacing) hält das Wissen. Die Selbsteinschätzung vor dem Abgleich trainiert die eigene Kalibrierung mit. Die Quellenangaben stammen aus dem Gedächtnis, für eine belastbare Fassung müsste man sie prüfen.

## So läuft es

1. **App öffnen.** Server starten (siehe unten), dann `http://localhost:8744/App/` in Chrome. Beim ersten Mal den Ordner `03 Bereiche/Active Recall` freigeben.
2. **Neues Projekt** anlegen: Titel, Quelle (Text einfügen oder PDF/Bild hochladen), optional Umfang.
3. **Abruf starten:** frei schreiben oder per WhisperBar ins Feld diktieren, dann selbst einschätzen (nochmal / schwer / gut / leicht), speichern.
4. **Feedback holen:**
   - Bei Text-Referenzen: in der App auf „Feedback von Claude holen". Läuft direkt, Ergebnis steht nach ~30 Sekunden in der Session.
   - Bei PDF/Bild beim ersten Mal: Claude-Code-Session öffnen, „Active Recall durchgehen" sagen (Claude liest die Datei aus). Danach geht auch hier der Knopf.
5. **Wiederholen,** wenn das Dashboard ein Projekt als fällig zeigt.

Für [[Muster]] (wiederkehrende Schwächen) und projektübergreifende Fragen („Wo hänge ich immer?", „Fass zusammen, was ich diesen Monat gelernt habe") die Claude-Session nutzen. Der App-Knopf pflegt [[Muster]] nicht.

## Server starten

Einmalig, damit der Feedback-Knopf funktioniert:

```bash
claude setup-token
```

Dann jeweils:

```bash
python3 "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/03 Bereiche/Active Recall/server.py"
```

Oder über die Claude-Code-Session: „Active-Recall-App starten". Der Server nutzt beim Feedback dein Claude-Abo-Kontingent, kein API-Key.

## Schulleitung (seit 08.11.2026)

Eigener Bereich der App für das Überprüfungsverfahren: `http://localhost:8744/App/schulleitung.html`. Vorbild war die Übersichtlichkeit von RemNote, die Inhalte kommen aus dem Vault.

- **Heute:** laufende Woche aus dem [[Lernplan Schulrecht bis Februar 2027]], nächster Fall, fällige Karten, Mindmap, Audio.
- **Fälle:** Antwort tippen oder mit WhisperBar diktieren, Rückmeldung nach dem 6-Schritte-Schema, Nachfragen im selben Gespräch. Die Gespräche landen in `Schulleitung/Gespräche/`.
- **Karten:** Fakten mit Tipp, Erklärung und Fundstelle. Bei Unklarem Claude fragen. Eine Datei je Lernplan-Woche 1 bis 9, dazu Grundschule, Werkrealschule und Verbund, Schulzentrum Rudersberg. „Heute“ bietet nur die Karten der laufenden Woche an.
- **Mindmaps:** Excalidraw in der App oder Foto der Handskizze, danach Abgleich mit Claude. Dateien in `Schulleitung/Mindmaps/`. Der Editor lädt beim ersten Öffnen aus dem Netz.
- **Wissen:** Suche über alles; Seiten zu Schulzentrum, allen Lernplan-Themen, Verfahren und Schulentwicklung; alle zwölf Rechtstexte im Wortlaut; Skript und Kurzübersicht. Seiten liegen in `Schulleitung/Wissen/<Gruppe>/`, Gesetze und alte Unterlagen werden live aus `04 Ressourcen/Schulrecht/` gelesen.

Karten und neue Fälle sind Markdown und lassen sich direkt bearbeiten: `Schulleitung/Karten/*.md`, `Schulleitung/Fälle Verbund.md`. Der Lernstand steht in `Schulleitung/stand.json`.

Die Rückmeldung läuft über die Claude-Kommandozeile mit Sonnet. Sie braucht einmal `claude auth login` im Terminal und verbraucht Pro-Kontingent, keine API. Karten, Tipps auf Karten, Mindmap-Editor und Wissen funktionieren auch ohne Anmeldung.

## Struktur

- `App/` – die Oberfläche (HTML/JS, keine externen Abhängigkeiten)
- `Projekte/<Name>/projekt.md` – Metadaten und SR-Status
- `Projekte/<Name>/referenz.md` – Grundlage fürs Feedback
- `Projekte/<Name>/uploads/` – hochgeladene PDFs und Bilder
- `Projekte/<Name>/sessions/*.md` – einzelne Abrufe mit Feedback
- [[Muster]] – wiederkehrende Schwächen über alle Projekte, von Claude gepflegt

## Spaced Repetition

SR-Level 0–6, Intervalle in Tagen: 1, 2, 4, 9, 19, 40, 85. Die App plant nach der Selbsteinschätzung vor. Claude korrigiert das Level nach dem tatsächlichen Abruf, wenn Selbstbild und Ergebnis auseinanderliegen.
