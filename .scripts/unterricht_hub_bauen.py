#!/usr/bin/env python3
"""Baut die Unterrichts-Anlaufstelle in Obsidian: Notiz (Master) und Canvas (vertikal).

Ablage: 03 Bereiche/Schule & Unterricht/Unterricht – Hub.md und .canvas
Neue Werkzeuge unten in BEREICHE eintragen, dann: python3 .scripts/unterricht_hub_bauen.py
HTML-Dateien werden als file://-Links eingebaut, Obsidian öffnet sie im Browser.
"""
import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

VAULT = Path(__file__).resolve().parent.parent
ZIEL = VAULT / "03 Bereiche/Schule & Unterricht"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Schuljahr 26 27"

M = "04 Ressourcen/Mathematik/"
P = "04 Ressourcen/Physik/"
S = "04 Ressourcen/Sport/"
L = "04 Ressourcen/Lernwissenschaft & Pädagogik/"
K = "03 Bereiche/Schule & Unterricht/Klassenlehrer 7c/"

# (Titel, Canvas-Farbe, [(Text, Ziel)]); Ziel: Vault-Pfad (.html/.pdf → Datei-Link, .md/.excalidraw → Wikilink),
# absoluter Pfad (iCloud-Ordner) oder None für reinen Text.
BEREICHE = [
    ("Planung", "4", [
        ("Bildungs-Dashboard: Stunden mit Status", "04 Ressourcen/Bildungs-Dashboard.html"),
        ("Stoffverteilung Mathe 7", M + "Mathematik Klasse 7 – Stoffverteilungsplan Schule.html"),
        ("Stoffverteilung Mathe 10", M + "Stoffverteilungsplan 26-27 Mathe 10.html"),
        ("Stoffverteilung Physik 7", P + "Stoffverteilungsplan Physik Klasse 7 2026-27.md"),
        ("Stoffverteilung Physik 10", P + "Stoffverteilung/Stoffverteilungsplan Klasse 10 2026-27.html"),
        ("Mein Stundenplan", "04 Ressourcen/Lernwissenschaft & Pädagogik/Stundenplan 7C.html"),
    ]),
    ("Mathe 7c", "#2563eb", [
        ("Mindmap Mathe 7c", M + "Mathematik Klasse 7c – Mindmap.excalidraw"),
        ("Übersicht aller Stunden", M + "Mathematik Klasse 7 – Übersicht.html"),
        ("Dreiecke: Diagnose und Auswertung", M + "Dreiecke/01 Diagnose – Test, Auswertung, Förderblätter/Diagnose Dreiecke 7c – Auswertung.html"),
        ("Einstiegskarte Mathe", M + "Mathematik.md"),
        ("Mein Mathe-Konzept: kleine Schritte", M + "Mein Mathe-Konzept – Aufgaben in kleine Schritte zerlegen.md"),
        ("Grundlagen-Check", M + "Arbeitsblätter/Grundlagen-Check/Grundlagen-Check Workflow.md"),
        ("iCloud Mathematik 7c", str(ICLOUD / "Mathematik/Mathematik 7c")),
    ]),
    ("Mathe 10b", "#2563eb", [
        ("Mindmap Mathe 10b", M + "Mathematik Klasse 10b – Mindmap.excalidraw"),
        ("Übersicht aller Stunden", M + "Mathematik Klasse 10b – Übersicht.html"),
        ("Prüfungsaufgaben: Startseite", M + "Prüfungsaufgaben/index.html"),
        ("Prüfungs-Baukasten", M + "Prüfungsaufgaben/Baukasten.html"),
        ("Übungsprüfung (Stil 2024)", M + "Prüfungsaufgaben/Übungsprüfung Mathematik (Stil 2024).html"),
        ("iCloud Mathematik 10b", str(ICLOUD / "Mathematik/Mathematik 10b")),
    ]),
    ("Physik 7c", "#111111", [
        ("Mindmap Physik 7c", P + "Physik Klasse 7c – Mindmap.excalidraw"),
        ("Optik Klasse 7: Übersicht", P + "Optik/Optik Klasse 7 – Übersicht.html"),
        ("Optik Klasse 7: Material", P + "Optik/Optik Klasse 7 – Material.html"),
        ("Optik-Labore (Simulationen)", P + "Optik/Optik-Labore.html"),
        ("Physik Dashboard (Jahresplan, Versuche)", P + "Physik Dashboard.html"),
        ("Einstiegskarte Physik", P + "Physik.md"),
    ]),
    ("Physik 10", "#111111", [
        ("Mindmap Kernphysik 10", P + "Kernphysik/Kernphysik Klasse 10 – Mindmap.excalidraw"),
        ("Kernphysik Klasse 10: Übersicht", P + "Kernphysik/Kernphysik Klasse 10 – Übersicht.html"),
        ("Kernphysik Klasse 10: Material", P + "Kernphysik/Kernphysik Klasse 10 – Material.html"),
        ("Kernphysik-Labore (Simulationen)", P + "Kernphysik/Kernphysik-Labore.html"),
        ("Physik MC Generator", P + "Prüfungsaufgaben/Physik MC Generator.html"),
    ]),
    ("Sport", "2", [
        ("Einstiegskarte Sport", S + "Sport.md"),
        ("Sportcurriculum Klasse 5 bis 10", S + "Sportcurriculum.html"),
        ("Dreikampf Turnen", S + "Dreikampf Turnen/dreikampf-turnen.html"),
        ("Coopertest Laufzettel", S + "Coopertest/Coopertest Laufzettel Klasse 5 bis 10.html"),
        ("LA Sprengeltabelle Remstal", S + "LA Sprengeltabelle Remstal (männlich).md"),
        ("Schulschwimmen: Bestimmungen", S + "Schwimmen/Schulschwimmen BW – Zusammenfassung der Bestimmungen.md"),
        ("iCloud Sport 26/27 (Notenlisten, Gruppen)", str(ICLOUD / "Sport")),
    ]),
    ("Klassenlehrer 7c", "6", [
        ("Überblick: was wann", K + "00 Überblick – was wann.html"),
        ("Materialliste 7c", K + "Materialliste Klasse 7c 2026-27.html"),
        ("Klassenführung: Regeln und Rituale", L + "Klassenführung – Regeln und Rituale Klasse 7.md"),
        ("Bereichsnotiz Schule & Unterricht", "03 Bereiche/Schule & Unterricht/Schule & Unterricht.md"),
    ]),
    ("Werkzeuge", "1", [
        ("Sitzplan-Generator", "04 Ressourcen/Sitzplan/Sitzplan.html"),
        ("Notenschlüsselrechner", "04 Ressourcen/Notenschlüsselrechner/Notenschlüsselrechner.html"),
        ("Notenschlüsselrechner GDRS", "04 Ressourcen/Notenschlüsselrechner/Notenschlüsselrechner GDRS.html"),
        ("Notenschlüssel Realschulprüfung", "04 Ressourcen/Notenschlüsselrechner/Notenschlüssel Realschulprüfung BW.html"),
        ("Whiteboard-Blatt kariert", L + "Whiteboard-Blatt – karierte Seite.html"),
        ("Gelbe und rote Karten", L + "Gelbe und rote Karten – Druckvorlage.html"),
        ("Bausteine für Stunden-HTMLs (Seitenleiste, Uhr, Gruppen)", L + "Lernwissenschaft & Pädagogik.md"),
    ]),
    ("Lernen", "4", [
        ("Einstiegskarte Lernen", L + "Lernen.md"),
        ("Lernen lernen: Präsentation", L + "Lernen lernen – Präsentation.html"),
        ("Mastery-Routinen", L + "Mastery-Routinen im Unterricht (Klasse 7).md"),
        ("Active Recall App", "03 Bereiche/Active Recall/App/index.html"),
    ]),
]


def link(text, ziel):
    if ziel is None:
        return text
    if ziel.endswith(".md"):
        return f"[[{ziel[:-3]}|{text}]]"
    if ziel.endswith(".excalidraw"):  # Mindmaps öffnen in Obsidian, nicht im Browser
        if not (VAULT / ziel).exists():
            print("FEHLT:", ziel)
        return f"[[{ziel}|{text}]]"
    pfad = Path(ziel) if ziel.startswith("/") else VAULT / ziel
    if not pfad.exists():
        print("FEHLT:", ziel)
    return f"[{text}](file://{quote(str(pfad))})"


def block(titel, eintraege):
    return f"## {titel}\n" + "\n".join(f"- {link(t, z)}" for t, z in eintraege)


def wochen():
    """Tabelle „diese und nächste Woche“ aus dem Stundenkontext des Schul-Cockpits."""
    quelle = Path.home() / ".claude/mods/schul-cockpit/stundenkontext.json"
    try:
        daten = json.loads(quelle.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "Wochenplan nicht lesbar: `python3 .scripts/stundenkontext_bauen.py` laufen lassen."
    tag = date.today()
    if tag.weekday() >= 5:  # am Wochenende schon die kommende Woche zeigen
        tag += timedelta(days=7 - tag.weekday())
    klassen = daten.get("klassen", {})
    alle = sorted({w["von"] for ws in klassen.values() for w in ws})
    laufend = [v for v in alle if date.fromisoformat(v) <= tag < date.fromisoformat(v) + timedelta(days=7)]
    kommend = [v for v in alle if date.fromisoformat(v) > tag]
    spalten = (laufend + kommend)[:2]
    if not spalten:
        return "Kein Wochenplan mehr für dieses Schuljahr."

    def kopf(v):
        nr = next(w["nr"] for ws in klassen.values() for w in ws if w["von"] == v)
        d = date.fromisoformat(v)
        name = "Diese Woche" if v in laufend else "Nächste Woche" if v == spalten[-1] and laufend else "Kommende Woche"
        return f"{name}: W{nr} ab {d:%d.%m.}"

    zeilen = ["| | " + " | ".join(kopf(v) for v in spalten) + " |", "|---|" + "---|" * len(spalten)]
    for klasse, ws in klassen.items():
        nach_datum = {w["von"]: w for w in ws}
        zellen = []
        for v in spalten:
            w = nach_datum.get(v)
            text = w["thema"] if w else "–"
            if w and w.get("termine"):
                text += f" **({w['termine']})**"
            zellen.append(text.replace("|", "/"))
        zeilen.append(f"| **{klasse}** | " + " | ".join(zellen) + " |")
    for f in daten.get("frei", []):
        if f["von"] <= tag.isoformat() <= f["bis"]:
            zeilen.insert(0, f"Gerade frei: {f['was']}\n")
    return "\n".join(zeilen)


TABELLE = wochen()
heute = date.today().strftime("%d.%m.%Y")
kopf = (f"Eine Anlaufstelle für den Unterricht: Fächer, Werkzeuge, Ablage. Stand {heute}. "
        "Links auf HTML-Dateien öffnen im Browser. Neues trägt Claude in "
        "`.scripts/unterricht_hub_bauen.py` ein und baut Notiz und Canvas neu.")

md = ["---", "tags: [hub, unterricht, schule]", "status: aktiv", f"date: {date.today()}", "---", "",
      "# Unterricht – Hub", "", kopf, "",
      "Dieselben Inhalte als Pinnwand in Spalten: [[Unterricht – Hub.canvas]]. "
      "Als Seite im Browser (Claude-Artifact, privat, Momentaufnahme): "
      "https://claude.ai/artifact/FEnXLpLuY43fkVGJN3xDef", "",
      "## Diese und nächste Woche", "", TABELLE, ""]
for titel, _, eintraege in BEREICHE:
    md += [block(titel, eintraege), ""]
(ZIEL / "Unterricht – Hub.md").write_text("\n".join(md), encoding="utf-8")

# Canvas: in die Breite, oben der Kopf über alle Spalten, darunter Bereiche nebeneinander
BREITE, LUECKE, PRO_ZEILE = 400, 40, 5
zeilen = [BEREICHE[i:i + PRO_ZEILE] for i in range(0, len(BEREICHE), PRO_ZEILE)]
gesamt = PRO_ZEILE * BREITE + (PRO_ZEILE - 1) * LUECKE
nodes, y = [], 0
nodes.append({"id": "kopf", "type": "text", "x": 0, "y": y, "width": gesamt, "height": 130,
              "text": "# Unterricht\n" + kopf})
y += 130 + LUECKE
h_tab = 110 + 48 * TABELLE.count("\n")
nodes.append({"id": "wochen", "type": "text", "x": 0, "y": y, "width": gesamt, "height": h_tab,
              "color": "4", "text": "## Diese und nächste Woche\n" + TABELLE})
y += h_tab + LUECKE
n = 0
for zeile in zeilen:
    h = 70 + 34 * max(len(e) for _, _, e in zeile)
    for spalte, (titel, farbe, eintraege) in enumerate(zeile):
        nodes.append({"id": f"b{n}", "type": "text", "x": spalte * (BREITE + LUECKE), "y": y,
                      "width": BREITE, "height": h, "color": farbe, "text": block(titel, eintraege)})
        n += 1
    y += h + LUECKE
(ZIEL / "Unterricht – Hub.canvas").write_text(
    json.dumps({"nodes": nodes, "edges": []}, ensure_ascii=False, indent=1), encoding="utf-8")
print("gebaut:", ZIEL / "Unterricht – Hub.md", "und .canvas")
