#!/usr/bin/env python3
"""Rezept Trigonometrie Mathe 10b als Flussdiagramm in Excalidraw (19.11.2026, für Fr 20.11.).
Inhalt nach Oskars Diktat: 0 Skizze, 1 Winkel erkennen, 2 rechtwinklig? (Ja links, Nein rechts),
3 Gleichung mit einer Unbekannten, 4 auflösen (zwei Nachkommastellen, auch Winkel), Fertig?
Stil wie die Mindmaps: Kästen mit gebundenem Text, nur gerade Pfeile, an beiden Enden gebunden.
Das PDF (Trigonometrie Klasse 10/baue_rezept_trigo.py) liest diese Datei und übernimmt die Grafik,
Änderungen in Obsidian landen so beim nächsten Bau auch im PDF.
Datei nie überschreiben, solange sie in Obsidian offen ist (Prüfung unten).
"""
import json
import math
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "04 Ressourcen/Mathematik/Trigonometrie Klasse 10/Mathe 10b – Rezept Trigonometrie – Flussdiagramm.excalidraw"
BLAU, ROT, DUNKEL, GRAU = "#2563a8", "#c2185b", "#1e3a5f", "#475569"
SCHRITT = ("#f1f5f9", DUNKEL)
FRAGE = ("#fff4d6", "#b45309")
JA = ("#ecfdf5", "#047857")
NEIN = ("#fdf2f8", ROT)

m = Mindmap("x")
weg = {m.mitte["id"]} | {e["id"] for e in m.E if e.get("containerId") == m.mitte["id"]}
m.E = [e for e in m.E if e["id"] not in weg]          # keine Mitte-Ellipse, das hier ist ein Ablauf


def oben_buendig(kasten, abstand=14):
    """Gebundenen Titel oben in den Kasten setzen (Platz für die Zeichnung darunter)."""
    t = next(e for e in m.E if e.get("containerId") == kasten["id"])
    t["verticalAlign"], t["y"] = "top", kasten["y"] + abstand


def schritt(nr, y, h, s, x=60, w=960):
    """Titel (erste Zeile) gebunden und oben, die übrigen Zeilen als Text darunter in derselben Gruppe."""
    titel, rest = s.split("\n", 1)
    m.gruppe = [f"s{nr}"]
    b = m.box(x, y, w, h, titel, 24, *SCHRITT, tcol=DUNKEL)
    oben_buendig(b, 12)
    m.text(x, y + 50, rest, 20, "#374151", "center", w=w)
    m.box(x - 24, y + h / 2 - 24, 48, 48, str(nr), 24, BLAU, BLAU, "ellipse", "#ffffff")
    m.gruppe = []
    return b


def pfeil(a, b, p, q, label=None, col=DUNKEL):
    m.gruppe = []
    arr = m.pfeil([p, q], col, 2.5, a, b)
    if label:
        fs = 20
        tw, th = len(label) * fs * 0.6, fs * 1.25
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        m.text(mx - tw / 2, my - th / 2, label, fs, col, "center", arr, tw)
    return arr


def rechter(x, y, start, r=16):
    """Viertelkreis mit Punkt; start = Richtung des ersten Schenkels in Grad (Bildschirm, y nach unten)."""
    pts = [(x + r * math.cos(math.radians(start + k * 15)), y + r * math.sin(math.radians(start + k * 15))) for k in range(7)]
    m.linie(pts, ROT, 1.5)
    w = math.radians(start + 45)
    m.ell(x + r * .48 * math.cos(w), y + r * .48 * math.sin(w), 2.5, ROT, ROT, 1)


def bruch(x, y, z, n, fs=16, b=145, col="#1f2937"):
    m.text(x, y - fs * 1.25 - 2, z, fs, col, "center", w=b)
    m.linie([(x, y), (x + b, y)], col, 1.5)
    m.text(x, y + 3, n, fs, col, "center", w=b)


# ---------------------------------------------------------------- 0, 1
s0 = schritt(0, 0, 120, "Alles Gegebene in die Skizze eintragen\n"
                        "Werte stehen oft links neben der Figur: direkt ins Dreieck schreiben.\n"
                        "Gesuchtes rot markieren. Eigene Zeichnung: gut, kostet aber Zeit.")
s1 = schritt(1, 170, 140, "Winkel suchen, die du direkt erkennst\n"
                          "Scheitel-, Neben-, Stufen-, Wechselwinkel\n"
                          "Winkelsumme im Dreieck: 180°\n"
                          "Gefundene Winkel gleich eintragen.")
pfeil(s0, s1, (540, 126), (540, 164))

# ---------------------------------------------------------------- 2 rechtwinklig?
m.gruppe = ["s2"]
f2 = m.box(320, 360, 440, 180, "Ist das Dreieck\nrechtwinklig?", 24, *FRAGE, typ="diamond", tcol="#1f2937")
m.box(371, 426, 48, 48, "2", 24, BLAU, BLAU, "ellipse", "#ffffff")
m.gruppe = []
pfeil(s1, f2, (540, 316), (540, 354))

# Ja: sin, cos, tan
m.gruppe = ["ja"]
ja = m.box(0, 610, 540, 310, "sin, cos oder tan", 26, *JA, tcol=JA[1])
oben_buendig(ja)
P, Q, R = (30, 850), (170, 850), (170, 710)
m.linie([P, Q, R, P], "#1f2937", 2, fill="#ffffff")
rechter(Q[0], Q[1], 180)
m.linie([(P[0] + 40 * math.cos(math.radians(a)), P[1] + 40 * math.sin(math.radians(a))) for a in range(-45, 1, 9)], "#1f2937", 1.5)
m.text(78, 822, "α", 18, "#1f2937", w=12)
m.text(20, 745, "Hypotenuse", 15, GRAU, w=90)
m.text(178, 770, "Gegenkathete", 15, GRAU, w=108)
m.text(55, 856, "Ankathete", 15, GRAU, w=81)
for k, (fn, z, n) in enumerate((("sin", "Gegenkathete", "Hypotenuse"), ("cos", "Ankathete", "Hypotenuse"),
                                ("tan", "Gegenkathete", "Ankathete"))):
    y = 705 + k * 65
    m.text(305, y - 11, f"{fn} α =", 18, "#1f2937", w=76)
    bruch(385, y, z, n)
m.text(20, 885, "zwei Seiten bekannt, dritte gesucht: Pythagoras", 15, GRAU, "center", w=500)

# Nein: Höhe einzeichnen
m.gruppe = ["nein"]
nein = m.box(600, 610, 480, 310, "Höhe oder Rechendreieck\neinzeichnen", 24, *NEIN, tcol=NEIN[1])
oben_buendig(nein)
m.text(620, 690, "so, dass ein rechtwinkliges\nDreieck entsteht; auch bei\nTrapez, Fünfeck …", 18, "#1f2937", "center", w=440)
m.linie([(630, 890), (800, 890), (700, 790), (630, 890)], "#1f2937", 2, fill="#ffffff")
m.linie([(700, 790), (700, 890)], ROT, 2, "dashed")
rechter(700, 890, 270)
m.linie([(850, 890), (1050, 890), (1000, 795), (900, 795), (850, 890)], "#1f2937", 2, fill="#ffffff")
m.linie([(1000, 795), (1000, 890)], ROT, 2, "dashed")
rechter(1000, 890, 180)
m.gruppe = []
pfeil(f2, ja, (326, 452), (270, 604), "Ja")
pfeil(f2, nein, (754, 452), (840, 604), "Nein")

# ---------------------------------------------------------------- 3, 4
s3 = schritt(3, 980, 115, "Gleichung mit genau einer Unbekannten aufstellen\n"
                          "Im rechtwinkligen Dreieck: zwei Seiten oder eine Seite und ein Winkel\n"
                          "Das Gesuchte steht möglichst in der Gleichung.")
pfeil(ja, s3, (270, 926), (270, 974))
pfeil(nein, s3, (840, 926), (840, 974))
s4 = schritt(4, 1145, 165, "Nach der Unbekannten auflösen\n"
                           "Unbekannte oben im Bruch: mal Nenner (| ⋅ 9,0)\n"
                           "Unbekannte unten im Bruch: tauschen (| a ↔ sin 60°)\n"
                           "Winkel gesucht: sin⁻¹, cos⁻¹, tan⁻¹ (Rechner auf DEG)\n"
                           "Ergebnis mit zwei Nachkommastellen, auch bei Winkeln")
pfeil(s3, s4, (540, 1101), (540, 1139))

# ---------------------------------------------------------------- fertig?
m.gruppe = ["fertig"]
ff = m.box(350, 1360, 380, 160, "Alles Gesuchte\nberechnet?", 22, *FRAGE, typ="diamond", tcol="#1f2937")
m.gruppe = []
pfeil(s4, ff, (540, 1316), (540, 1354))
fertig = m.box(0, 1395, 270, 90, "Fertig:\nErgebnis mit Einheit", 19, "#ffffff", ROT, tcol=ROT, sw=3)
zurueck = m.box(810, 1385, 270, 110, "Neuen Wert in die\nSkizze eintragen,\nweiter bei Schritt 1", 18, "#f8fafc", GRAU, tcol=GRAU)
pfeil(ff, fertig, (344, 1440), (276, 1440), "Ja")
pfeil(ff, zurueck, (736, 1440), (804, 1440), "Nein")
m.mitte = s0                                      # für die Überlappungsprüfung des Generators

if __name__ == "__main__":
    offen = json.loads((VAULT / ".obsidian/workspace.json").read_text()) if (VAULT / ".obsidian/workspace.json").exists() else {}
    if ZIEL.name in json.dumps(offen, ensure_ascii=False):
        raise SystemExit(f"{ZIEL.name} ist in Obsidian offen, erst schließen.")
    m.speichern(ZIEL)
    if len(sys.argv) > 1:
        m.vorschau(sys.argv[1])
