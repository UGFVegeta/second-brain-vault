#!/usr/bin/env python3
"""Materialliste Optik Klasse 7c: alles Material aus den Doppelstunden F1 bis F8, als Gesamtliste und nach Stunden.
Liest die Materialtabellen direkt aus dem Quelltext der Bauskripte (ohne sie auszuführen, sie bauen sonst die Stunden neu).
Noch nicht vorbereitete Stunden stehen ohne Material in der Liste. Feste Vorgaben stehen in VORGABE.
Aufruf: python3 baue_material_optik.py  -> Optik Klasse 7 – Material.html"""
import ast, re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
from material_vorlage import baue_materialliste  # noqa: E402


def dicts(datei):
    """Alle Material-Dicts (mit "demo") aus einem Skript, dazu die Aufrufe materialliste(..., "W03", ..., {...})."""
    t = ast.parse((HIER / datei).read_text(encoding="utf-8"))
    out = {}
    for n in ast.walk(t):
        try:
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) and isinstance(n.targets[0], ast.Name):
                d = ast.literal_eval(n.value)
                if "demo" in d:
                    out[n.targets[0].id] = d
            if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "materialliste":
                out[ast.literal_eval(n.args[1])] = ast.literal_eval(n.args[3])
        except (ValueError, IndexError):
            pass
    return out


M = {**dicts("export_icloud.py"), **dicts("baue_folien_am_stueck.py"), **dicts("baue_stunden_f3_f4.py"),
     **dicts("baue_stunden_f5_lk.py"), **dicts("baue_stunden_optik2.py")}

# gleiche Geräte zusammenführen, die Variante wandert in den Hinweis
NAME = {"Ray-Box mit Stromanschluss": ("Ray-Box", ""), "Ray-Box mit einem Spalt": ("Ray-Box", "mit einem Spalt"),
        "Ray-Box mit drei parallelen Strahlen": ("Ray-Box", "mit drei parallelen Strahlen"),
        "Kreisscheibe mit Winkeleinteilung": ("Winkelscheibe", "")}

ART = [
    ("Optik-Geräte aus der Sammlung", ["Ray-Box", "Optikleuchte mit Einspaltblende", "zweite Lichtquelle", "Blende mit Loch", "Schirm",
                                       "Winkelscheibe", "ebener Spiegel", "Halbzylinder aus Glas oder Acryl", "Sammellinse (Linsenprofil)",
                                       "Zerstreuungslinse (Linsenprofil)", "Lupen", "Sammellinse als Brennglas", "Tellurium beleuchtet (Phywe)",
                                       "helle Lampe ohne Schirm", "Glühlampe mit Fassung", "Spiegel und Taschenlampe", "Glasplatte, senkrecht aufgestellt"]),
    ("Für die Gruppen", ["weißes Blatt Papier", "schwarzer oder dunkler Karton", "klare Glasscheibe", "undurchsichtiger Körper",
                         "Styroporkugel, etwa 5 cm", "Bleistift oder Schaschlikspieß", "Geodreieck und Bleistift", "schwarzer Zeichenkarton"]),
    ("Bringen die Schüler mit", ["runde Chipsdose", "Transparent- oder Butterbrotpapier", "Zirkel, Schere, Lineal, Kleber oder Tesa"]),
    ("Einkaufen, Verbrauchsmaterial", ["zwei gleiche Teelichter", "Kerze mit Feuerzeug", "Feuerzeug", "Alufolie und Nadel", "Nagel (etwa 1 mm)"]),
    ("Sonstiges", []),
]

# Stand, den Oskar genannt hat (status: v = vorhanden, n = nicht vorhanden, b = bestellen, o = bestellt)
VORGABE = {}

STUNDEN = [  # id, Marke, Titel, Datei, Material-Schlüssel (None = noch nicht vorbereitet)
    ("F1", "F1", "Lichtquellen und beleuchtete Körper", "Optik 1 – Lichtquellen und beleuchtete Körper – ALLES.html", "W03"),
    ("F2", "F2", "Licht trifft auf einen Körper", "Optik – Do 24.09. – Stunde.html", "MATERIAL"),
    ("F3", "F3", "Lichtausbreitung und Blende", "Optik – Leitfrage 3 – Stunde.html", "F3_MATERIAL"),
    ("F4", "F4", "Kern- und Halbschatten", "Optik – Leitfrage 4 – Stunde.html", "F4_MATERIAL"),
    ("F5", "F5", "Mondphasen und Finsternisse", "Optik – Leitfrage 5 – Stunde.html", "F5_MATERIAL"),
    ("LK", "LK", "Lochkamera und Rückblick Optik I", "Optik – Lochkamera – Stunde.html", "LK_MATERIAL"),
    ("F6a", "F6", "Das Reflexionsgesetz", "Optik II – Reflexionsgesetz – Stunde.html", "R_MAT"),
    ("F6b", "F6", "Spiegelbild und Spiegelgröße", "Optik II – Spiegelbild – Stunde.html", "S_MAT"),
    ("F7", "F7", "Lichtbrechung", "Optik II – Lichtbrechung – Stunde.html", "B_MAT"),
    ("F8a", "F8", "Sammel- und Zerstreuungslinse", "Optik II – Linsen – Stunde.html", "L_MAT"),
    ("F8b", "F8", "Bildentstehung an der Sammellinse, Lupe, Auge", "", None),
    ("F8c", "F8", "Kurz- und Weitsichtigkeit, Wiederholung Optik", "", None),
    ("F9", "F9", "Farben: Prisma, Spektrum, Regenbogen", "", None),
    ("F9b", "F9", "Unsichtbares Licht, Farbaddition, Glasfaser", "", None),
]


def datum(datei):
    if not datei:
        return "noch nicht vorbereitet"
    sub = re.search(r'<p class="sub">([^<]*)', (HIER / datei).read_text(encoding="utf-8"))
    d = re.search(r"(Do \d\d\.\d\d\.\d{4})", sub.group(1)) if sub else None
    if not d:
        return ""
    return ("voraussichtlich " if "voraussichtlich" in sub.group(1) else "") + d.group(1)


liste = []
for sid, marke, titel, datei, key in STUNDEN:
    mat = M[key] if key else {"demo": [], "schueler": [], "hinweis": ""}
    zeilen = []
    for rolle, k in (("demo", "demo"), ("gruppe", "schueler")):
        for name, anz, hinweis in mat.get(k, []):
            neu, zusatz = NAME.get(name, (name, ""))
            zeilen.append({"name": neu, "anz": anz, "hinweis": ", ".join(x for x in (zusatz, hinweis) if x), "rolle": rolle})
    liste.append({"id": sid, "marke": marke, "titel": titel, "datum": datum(datei), "datei": datei, "zeilen": zeilen,
                  "hinweis": mat.get("hinweis", ""), "offen": key is None})

baue_materialliste(HIER / "Optik Klasse 7 – Material.html", "Material Optik 7", "Material Optik Klasse 7c",
                   "Alles, was in den Doppelstunden Optik I und II gebraucht wird.", liste, ART, VORGABE, "optik7-material", "Optik Klasse 7c")
