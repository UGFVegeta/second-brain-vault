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
3. **Abruf starten:** frei schreiben oder diktieren, dann selbst einschätzen (nochmal / schwer / gut / leicht), speichern.
4. **Feedback holen:** Claude-Code-Session öffnen, „Active Recall durchgehen" sagen. Claude bewertet die offenen Sessions, aktualisiert SR-Level und Fälligkeit und schreibt [[Muster]] fort.
5. **Wiederholen,** wenn das Dashboard ein Projekt als fällig zeigt.

Für projektübergreifende Fragen („Wo hänge ich immer?", „Fass zusammen, was ich diesen Monat gelernt habe") ebenfalls die Claude-Session nutzen.

## Server starten

```bash
python3 -m http.server 8744 --directory "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/03 Bereiche/Active Recall"
```

Oder über die Claude-Code-Session: „Active-Recall-App starten".

## Struktur

- `App/` – die Oberfläche (HTML/JS, keine externen Abhängigkeiten)
- `Projekte/<Name>/projekt.md` – Metadaten und SR-Status
- `Projekte/<Name>/referenz.md` – Grundlage fürs Feedback
- `Projekte/<Name>/uploads/` – hochgeladene PDFs und Bilder
- `Projekte/<Name>/sessions/*.md` – einzelne Abrufe mit Feedback
- [[Muster]] – wiederkehrende Schwächen über alle Projekte, von Claude gepflegt

## Spaced Repetition

SR-Level 0–6, Intervalle in Tagen: 1, 2, 4, 9, 19, 40, 85. Die App plant nach der Selbsteinschätzung vor. Claude korrigiert das Level nach dem tatsächlichen Abruf, wenn Selbstbild und Ergebnis auseinanderliegen.
