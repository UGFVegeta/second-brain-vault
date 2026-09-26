#!/usr/bin/env python3
"""Materialliste Kernphysik Klasse 10: alles Material aus den Stunden W01 bis W22, als Gesamtliste und nach Stunden.
Liest die Materialtabellen aus baue_stunden_k10.py und baue_stunden_k10_teil2.py. Status (vorhanden, bestellen, bestellt)
lässt sich im Browser anklicken und bleibt im Browser gespeichert. Feste Vorgaben stehen unten in VORGABE.
Aufruf: python3 baue_material_k10.py  -> Kernphysik Klasse 10 – Material.html"""
import re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
import baue_stunden_k10 as t1  # noqa: E402
import baue_stunden_k10_teil2 as t2  # noqa: E402

# gleiche Dinge mit verschiedenen Namen zusammenführen
NAME = {"Luftballon, aufgeblasen": "Luftballon", "Wolltuch oder Wollpullover": "Wolltuch", "Präparatesatz": "Präparate α, β, γ"}

ART = [
    ("Präparate (nur Lehrkraft)", ["Präparate α, β, γ", "γ-Präparat"]),
    ("Geräte aus der Sammlung", ["Geiger-Müller-Zählrohr mit Zählgerät", "Elektroskop", "Nebelkammer", "Absorber: Papier, Aluminium 5 mm, Bleiplatten",
                                 "Messzylinder 250 ml", "Stoppuhr", "Lineal oder Maßband"]),
    ("Für die Gruppen", ["Würfel", "Würfelbecher oder Schale", "Dominosteine", "Wolltuch", "Lineal", "Lappen"]),
    ("Einkaufen, kurz vor der Stunde", ["Luftballon", "Malzbier", "Trockeneis", "Isopropanol", "Diätsalz (Kaliumchlorid)"]),
    ("Sonstiges", []),
]

# Stand, den Oskar genannt hat (status: v = vorhanden, n = nicht vorhanden, b = bestellen, o = bestellt). Alles andere steht auf „noch nicht geprüft“.
VORGABE = {"Nebelkammer": {"status": "n", "notiz": "zu teuer, wird nicht bestellt"},
            "Würfel": {"status": "o", "notiz": "500 Stück bestellt (09/2026)"}}

stunden = []
for datei, h1, sub, _d, mat, *_ in t1.STUNDEN:
    stunden.append((datei, h1, sub, mat))
for kurz, h1, sub, _b, mat, *_ in t2.STUNDEN:
    stunden.append((f"Kernphysik – {kurz} – Stunde.html", h1, "Klasse 10 · Physik · " + sub, mat))

liste = []
for datei, h1, sub, mat in stunden:
    w = re.search(r"W\d\d", sub).group(0)
    woche = re.search(r"Woche ab ([\d.]+)", sub).group(1)
    zeilen = []
    for rolle, key in (("demo", "demo"), ("gruppe", "schueler")):
        for name, anz, hinweis in mat.get(key, []):
            zeilen.append({"name": NAME.get(name, name), "anz": anz, "hinweis": hinweis, "rolle": rolle})
    liste.append({"w": w, "woche": woche, "titel": h1.replace("Kernphysik: ", ""), "datei": datei, "zeilen": zeilen, "hinweis": mat.get("hinweis", "")})
liste.sort(key=lambda s: s["w"])

sys.path.insert(0, str(HIER.parent / "Optik"))
from material_vorlage import baue_materialliste  # noqa: E402

for s in liste:
    s["id"], s["marke"], s["datum"] = s["w"], s["w"], "Woche ab " + s["woche"]
baue_materialliste(HIER / "Kernphysik Klasse 10 – Material.html", "Material Kernphysik 10", "Material Kernphysik Klasse 10",
                   "Alles, was in den Stunden W01 bis W22 gebraucht wird.", liste, ART, VORGABE, "k10-material", "Kernphysik Klasse 10")
