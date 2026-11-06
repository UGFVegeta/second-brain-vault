"""Ablage für Rationale Zahlen: welche Datei in welchen Unterordner gehört.

Rationale Zahlen/
  Woche 1 und 2/, Woche 3/, Woche 4/, Woche 5/, Woche 7/   Stunden (HTML, Folien, Arbeitsblätter)
  Übungstests/                                              Übungstests und Übungsklassenarbeit
  Klassenarbeit/                                            KA 1 mit Gruppe B und Kästchen-Fassung
  _Skripte/                                                 Bauskripte, Bilder, Zwischendateien
"""
import re
from pathlib import Path

SKRIPTE = Path(__file__).resolve().parent
RZ = SKRIPTE.parent


def ordner_name(name):
    kurz = _kurz(name)
    return ORDNER.get(kurz, kurz)


def _kurz(name):
    n = Path(name).name
    if n.startswith("_"):
        return "_Skripte"
    if "Übungstest" in n or "Übungsklassenarbeit" in n:
        return "Übungstests"
    if "Klassenarbeit Nr. 1" in n:
        return "Klassenarbeit"
    m = re.search(r"Woche (\d+)", n)
    if m:
        w = int(m.group(1))
        return "Woche 1 und 2" if w <= 2 else f"Woche {w}"
    if n.startswith("Rationale Zahlen 3") or "IF-Stunde" in n:
        return "Woche 3"
    return "Woche 1 und 2"


ORDNER = {'Woche 1 und 2': '01 Woche 1 und 2 – Zahlen unter Null, Addieren, Subtrahieren',
          'Woche 3': '02 Woche 3 – Minusklammer, Rechengesetze',
          'Woche 4': '03 Woche 4 – Multiplizieren, Dividieren',
          'Woche 5': '04 Woche 5 – Gemischte Aufgaben, Lerntheke',
          'Woche 7': '05 Woche 7 – Verbindung der Rechenarten',
          'Übungstests': '06 Übungstests 1 und 2, Übungs-KA',
          'Klassenarbeit': '07 Klassenarbeit Nr. 1 (Gruppe A und B)'}


def ordner(name):
    p = RZ / ordner_name(name)
    p.mkdir(exist_ok=True)
    return p


def ziel(name):
    """Pfad, unter dem eine Ausgabedatei liegt (zum Schreiben und Lesen)."""
    return ordner(name) / Path(name).name
