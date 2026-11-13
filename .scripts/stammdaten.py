#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Stammdaten nachschlagen und ergänzen, ohne die ganze Datei zu lesen.

Datei: iCloud Drive / Privat / Wichtige Dokumente / Stammdaten.md (nicht im Vault, nicht auf GitHub).

  python3 .scripts/stammdaten.py suche <Begriff>            gibt nur passende Zeilen aus
  python3 .scripts/stammdaten.py setze <Abschnitt> <Name> <Wert>   fügt "- Name: Wert" im Abschnitt ein
                                                                   (gleicher Name wird ersetzt)
Abschnitte: Dienst und Beruf, Bank und Finanzen, Versicherungen, Auto und Wohnen, Sonstiges
"""
import sys
from pathlib import Path

DATEI = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Privat/Wichtige Dokumente/Stammdaten.md"


def suche(begriff):
    treffer = [z for z in DATEI.read_text(encoding="utf-8").splitlines() if z.startswith("- ") and begriff.lower() in z.lower()]
    print("\n".join(treffer) if treffer else "Nichts gefunden.")


def setze(abschnitt, name, wert):
    zeilen = DATEI.read_text(encoding="utf-8").splitlines()
    kopf = f"## {abschnitt}"
    if kopf not in zeilen:
        sys.exit(f"Abschnitt unbekannt: {abschnitt}")
    neu = f"- {name}: {wert}"
    i = zeilen.index(kopf) + 1
    j = i
    while j < len(zeilen) and not zeilen[j].startswith("## "):
        if zeilen[j].lower().startswith(f"- {name.lower()}:"):
            zeilen[j] = neu
            DATEI.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
            return print("ersetzt:", name)
        j += 1
    ende = j
    while ende > i and not zeilen[ende - 1].strip():
        ende -= 1
    zeilen.insert(ende, neu)
    if j == len(zeilen) or zeilen[ende + 1:ende + 2] and zeilen[ende + 1].startswith("## "):
        zeilen.insert(ende + 1, "")
    DATEI.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print("eingetragen:", name)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "suche":
        suche(a[1])
    elif len(a) == 4 and a[0] == "setze":
        setze(*a[1:])
    else:
        sys.exit(__doc__)
