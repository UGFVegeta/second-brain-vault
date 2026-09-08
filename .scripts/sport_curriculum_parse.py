#!/usr/bin/env python3
"""Liest Curriculum und Sprengeltabelle aus dem Vault und gibt die Struktur als JSON aus.

Reiner Lesevorgang. Dient als Datenquelle fuer sport_curriculum_build.py.
"""
import json
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
CURRICULUM = VAULT / "04 Ressourcen/Sport/Sportcurriculum Realschule.md"
SPRENGEL = VAULT / "04 Ressourcen/Sport/LA Sprengeltabelle Remstal (männlich).md"


def strip_md(text):
    """Markdown-Auszeichnung in reinen Text plus Marker umwandeln."""
    text = text.strip()
    # **fett** und *kursiv* als Marker behalten, damit der Generator sie deuten kann
    return text


def parse_curriculum(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    klassen = []
    aktuell = None
    gruppe = None
    note = None

    for line in lines:
        m = re.match(r"^## Klasse (\d+)\s*$", line)
        if m:
            aktuell = {"klasse": int(m.group(1)), "gruppen": [], "note": None}
            klassen.append(aktuell)
            gruppe = None
            note = None
            continue
        if aktuell is None:
            continue
        if line.startswith("## "):  # naechster Abschnitt, Klassen sind durch
            aktuell = None
            continue

        # Hinweis-Callout am Ende von Klasse 10
        if line.startswith("> [!note]"):
            note = {"titel": line.split("]", 1)[1].strip(), "text": []}
            aktuell["note"] = note
            gruppe = None
            continue
        if note is not None and line.startswith(">"):
            inhalt = line.lstrip(">").strip()
            if inhalt:
                note["text"].append(inhalt)
            continue

        # Gruppenueberschrift innerhalb des example-Callouts: > **Turnen**
        m = re.match(r"^>\s*\*\*(.+?)\*\*\s*$", line)
        if m:
            gruppe = {"titel": m.group(1).strip(), "items": []}
            aktuell["gruppen"].append(gruppe)
            continue

        # Listenpunkt: > - Boden: Rolle vorwaerts ...
        m = re.match(r"^>\s*-\s+(.*)$", line)
        if m and gruppe is not None:
            gruppe["items"].append(strip_md(m.group(1)))
            continue

    for k in klassen:
        if k.get("note"):
            k["note"]["text"] = " ".join(k["note"]["text"])
    return klassen


def parse_tabellen(path):
    """Liefert je Klasse Kopfzeile und Datenzeilen der Sprengeltabelle."""
    lines = path.read_text(encoding="utf-8").splitlines()
    tabellen = {}
    klasse = None
    kopf = None
    zeilen = None
    sprint = None

    for line in lines:
        m = re.match(r"^## Klasse (\d+) · Sprint (\S+)\s*$", line)
        if m:
            if klasse is not None and kopf:
                tabellen[klasse] = {"kopf": kopf, "zeilen": zeilen, "sprint": sprint}
            klasse = int(m.group(1))
            sprint = m.group(2)
            kopf = None
            zeilen = []
            continue
        if klasse is None:
            continue
        if line.startswith("## "):
            if kopf:
                tabellen[klasse] = {"kopf": kopf, "zeilen": zeilen, "sprint": sprint}
            klasse = None
            continue
        if line.startswith("|"):
            zellen = [z.strip() for z in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r"-+", z) for z in zellen):
                continue
            if kopf is None:
                kopf = zellen
            else:
                zeilen.append(zellen)

    if klasse is not None and kopf:
        tabellen[klasse] = {"kopf": kopf, "zeilen": zeilen, "sprint": sprint}
    return tabellen


def parse_progression(path):
    """LA-Progressionstabelle aus dem Curriculum."""
    text = path.read_text(encoding="utf-8")
    block = re.search(r"## Leichtathletik – Progression\n(.*?)\n---", text, re.S)
    if not block:
        return None
    zeilen = []
    kopf = None
    for line in block.group(1).splitlines():
        if not line.startswith("|"):
            continue
        zellen = [z.strip() for z in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r"-+", z) for z in zellen):
            continue
        if kopf is None:
            kopf = zellen
        else:
            zeilen.append(zellen)
    return {"kopf": kopf, "zeilen": zeilen}


def parse_bereiche(path):
    """Inhaltsbereiche im Ueberblick, Emoji wird abgetrennt."""
    text = path.read_text(encoding="utf-8")
    block = re.search(r"## Inhaltsbereiche im Überblick\n(.*?)\n---", text, re.S)
    if not block:
        return []
    out = []
    for line in block.group(1).splitlines():
        if not line.startswith("|"):
            continue
        zellen = [z.strip() for z in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r"-+", z) for z in zellen) or zellen[0] == "Bereich":
            continue
        name = re.sub(r"^[^\wÄÖÜäöü]+", "", zellen[0]).strip()
        klassen = [int(k.strip()) for k in zellen[1].split(",")]
        out.append({"name": name, "klassen": klassen})
    return out


def parse_uebersicht(path):
    text = path.read_text(encoding="utf-8")
    block = re.search(r"## Übersicht\n(.*?)\n---", text, re.S)
    if not block:
        return {}
    out = {}
    for line in block.group(1).splitlines():
        if not line.startswith("|"):
            continue
        zellen = [z.strip() for z in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r"-+", z) for z in zellen) or zellen[0] == "Klasse":
            continue
        out[int(zellen[0])] = zellen[1]
    return out


def parse_abweichungen(path):
    """Disziplinen, die der Sprengel fuehrt, das Curriculum aber nicht bewertet."""
    text = path.read_text(encoding="utf-8")
    block = re.search(r"## ⚠️ Abweichungen zum Schul-Curriculum\n(.*)", text, re.S)
    if not block:
        return {}
    out = {}
    for line in block.group(1).splitlines():
        line = line.lstrip(">").strip()
        if not line.startswith("|"):
            continue
        zellen = [z.strip() for z in line.strip().strip("|").split("|")]
        if len(zellen) < 2 or zellen[0] == "Klasse" or all(re.fullmatch(r"-+", z) for z in zellen):
            continue
        klassen = [int(n) for n in re.findall(r"\d+", zellen[0])]
        if "–" in zellen[0] and len(klassen) == 2:  # Spanne wie "5–10"
            klassen = list(range(klassen[0], klassen[1] + 1))
        for k in klassen:
            out.setdefault(k, []).append({"disziplin": zellen[1], "status": zellen[2]})
    return out


def main():
    data = {
        "klassen": parse_curriculum(CURRICULUM),
        "uebersicht": parse_uebersicht(CURRICULUM),
        "progression": parse_progression(CURRICULUM),
        "bereiche": parse_bereiche(CURRICULUM),
        "tabellen": parse_tabellen(SPRENGEL),
        "abweichungen": parse_abweichungen(SPRENGEL),
    }
    json.dump(data, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
