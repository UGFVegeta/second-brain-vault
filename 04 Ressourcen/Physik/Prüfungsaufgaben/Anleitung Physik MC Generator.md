---
tags: [physik, unterricht, tool, multiple-choice]
status: aktiv
date: 2026-07-03
---

# Anleitung Physik MC Generator

Die App [Physik MC Generator.html](Physik%20MC%20Generator.html) erstellt Multiple-Choice-Arbeitsblätter für Physik Klasse 7–10 (Realschule BW) als druckfertige A4-Blätter mit Lösungsblatt. Sie läuft komplett offline im Browser – einfach die HTML-Datei doppelklicken (öffnet sich in Safari/Chrome).

## Was die App kann

- **Eingebauter Fragenpool**: ca. 90 Fragen, sortiert nach Klasse und Thema (orientiert am Bildungsplan BW):
	- Klasse 7: Optik, Akustik, Magnetismus
	- Klasse 8: Elektrischer Strom, Energie, Wärmelehre
	- Klasse 9: Bewegungen, Kräfte, Elektrik (Ohmsches Gesetz)
	- Klasse 10: Radioaktivität & Kernphysik, Elektromagnetismus & Induktion, Energieversorgung
- **Einstellbar**: Anzahl Aufgaben, Antwortmöglichkeiten pro Frage (3–6), Anzahl richtiger Antworten (genau 1, 2, 3 oder gemischt), Punkte-Anzeige, ein- oder zweispaltiges Layout
- **Variation**: Jede Frage hat mehr Antworten hinterlegt als angezeigt werden – bei jedem „Neu generieren" entstehen andere Kombinationen. Einzelne Fragen lassen sich per 🔄 austauschen oder per ✕ entfernen (Buttons erscheinen beim Überfahren mit der Maus).
- **Fragen selbst auswählen**: Über „☑️ Fragen selbst auswählen…" bekommst du alle Fragen der gewählten Themen als Liste mit Lösungen angezeigt und hakst genau die an, die aufs Blatt sollen – statt zufälliger Auswahl. Bereits auf dem Blatt liegende Fragen sind vorangehakt.
- **Nur-Aufgaben-Modus für Klassenarbeiten**: Häkchen bei „Nur Aufgaben – ohne Kopf & Hinweis" blendet Kopfzeile und Hinweistext aus. Mit „Erste Aufgabennummer" stellst du ein, bei welcher Nummer die Zählung beginnt (z. B. 4, wenn der MC-Teil in der Klassenarbeit nach Aufgabe 3 kommt). So druckst du einen Baustein, den du direkt in eine Klassenarbeit einfügen kannst.
- **Punkte pro Frage**: Standardmäßig zählt jede Frage 1 Punkt (Oskars Regel für MC-Teile). Umschaltbar auf „= Anzahl richtiger Antworten".
- **Titel anklicken und direkt umbenennen** (z. B. „Klassenarbeit Nr. 2 – Optik").
- **Drucken/PDF**: Button „Drucken" → im Druckdialog „Als PDF sichern". Das Lösungsblatt kommt automatisch auf eine eigene Seite (abschaltbar).
- **Seitenumfang**: einspaltig passen ca. 5–7 Aufgaben auf eine A4-Seite, zweispaltig ca. 10–13. Für zwei Seiten entsprechend mehr Aufgaben wählen.

## Fragen zu YouTube-Videos und Filmen

Die App kann selbst keine Fragen erfinden – das übernehme ich (Claude). Der Workflow:

1. Mir in einer Session sagen: *„Schau dir dieses Video an: [URL] und erstelle 8 MC-Fragen dazu für Klasse 8 im JSON-Format für den Physik MC Generator."* (Ich kann Videos direkt anschauen und transkribieren.)
2. Ich liefere die Fragen im passenden JSON-Format.
3. In der App auf **„Eigene Fragen…"** klicken, JSON einfügen, importieren. Die Fragen erscheinen als eigenes Thema mit ★ in der Themenliste und bleiben dauerhaft im Browser gespeichert.

Alternativ kann ich neue Fragen auch **fest in die App einbauen** (in den Pool in der HTML-Datei) – dann sind sie unabhängig vom Browser gespeichert. Einfach sagen: *„Bau die Fragen fest in den Physik MC Generator ein."*

**JSON-Format für eigene Fragen:**

```json
[
  {
    "klasse": 8,
    "thema": "Film: Strom aus der Steckdose",
    "frage": "Was wird im Film als Stromquelle gezeigt?",
    "richtig": ["Eine Batterie"],
    "falsch": ["Ein Magnet", "Eine Glühlampe", "Ein Schalter", "Ein Dynamo"]
  }
]
```

Tipp: Pro Frage mehr Falschantworten (4–5) und wo sinnvoll mehrere richtige angeben – dann kann die App bei jeder Generierung variieren.

## Zusammenspiel mit tutory.de

tutory hat **keine Import-Schnittstelle** für fertige MC-Fragen (Stand Juli 2026, geprüft im tutory-Maschinenraum). Der Multiple-Choice-Baustein dort kann Fragen nur per eingebauter ChatGPT-Funktion neu generieren (mit Bezug auf eine Webseite oder einen Infotext-Baustein) – vorhandene Fragen einspielen geht nicht. Zwei praktikable Wege:

1. **Claude tippt die Fragen in tutory ein**: tutory im Chrome öffnen (eingeloggt), Claude-Chrome-Erweiterung verbinden, dann Claude bitten, die gewünschten Fragen aus dem Generator in den MC-Baustein des Arbeitsblatts einzutragen. Claude bedient den tutory-Editor dabei direkt im Browser.
2. **Baustein-Weg über den Generator**: „Nur Aufgaben"-Modus + passende Startnummer drucken und als eigene Seite an die tutory-Klassenarbeit anhängen. Punkte stimmen dank „1 Punkt pro Frage"-Modus überein.

## Pool erweitern

Den eingebauten Pool erweitere ich auf Zuruf, z. B.: *„Erstelle 10 neue Fragen zu Druck und Auftrieb für Klasse 9 und bau sie in den Physik MC Generator ein."* Wichtig: Eigene Fragen (★) sind pro Browser gespeichert – vor einem Browserwechsel über „Eigene Fragen exportieren" sichern.

Verwandt: [[App Mündliche Prüfung Generator]] und die Mathematik-Werkzeuge in `04 Ressourcen/Mathematik/Prüfungsaufgaben/`.
