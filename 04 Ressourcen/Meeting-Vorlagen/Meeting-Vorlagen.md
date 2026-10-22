---
tags: [vorlage, schule, konrektor]
status: aktiv
date: 2026-10-22
---

# Meeting-Vorlagen

Eigene A4-Notizvorlagen für Notability und zum Ausdrucken, angelehnt an den Häfft-Block „Meeting Notes office life“. Vorderseite mit Struktur, Rückseite dotted.

Jede Vorlage gibt es in zwei Stilen:
- **getönt:** farbige Flächen wie beim Original
- **Rahmen:** weiß, nur farbiger Rahmen, Dots zum Schreiben. Druckt sauberer auf dem Kopierer.

| Vorlage | getönt | Rahmen |
|---|---|---|
| Konferenz / Sitzung | `Notizen Konferenz.pdf` | `Notizen Konferenz – Rahmen.pdf` |
| Gespräch zu zweit | `Notizen Gespräch zu zweit.pdf` | `Notizen Gespräch zu zweit – Rahmen.pdf` |
| Mentoring-Gespräch | `Notizen Mentoring-Gespräch.pdf` | `Notizen Mentoring-Gespräch – Rahmen.pdf` |

## Neu bauen oder vorausfüllen

Skript: `.scripts/meeting_vorlagen.py`

```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/meeting_vorlagen.py
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/meeting_vorlagen.py konferenz --rahmen --thema "GLK" --datum 27.10.2026 --top "Termine" --top "Verschiedenes"
```

Vorausgefüllte Kopien landen in `Ausgefüllt/`.

## Datenschutz

Nur leere Vorlagen und TOPs in den Vault. Ausgefüllte Bögen mit Namen von Schülern oder Kollegen nicht hier ablegen, auch nicht als Foto.
