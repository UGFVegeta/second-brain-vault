#!/usr/bin/env python3
"""Rezept Trigonometrie Mathe 10b, KURZFASSUNG zum gemeinsamen Mitschreiben (Fr 20.11.2026, etwa 20 min).
Oskar 19.11.: lange Fassung bleibt; die kurze in seinen Formulierungen, ohne sin/cos/tan-Erklärung
(kennt die Klasse), mit dem Tauschen beim Auflösen, so einfach, dass die Klasse sie ins Heft zeichnen kann.
Stil wie die Mindmaps: Kästen mit gebundenem Text, nur gerade, gebundene Pfeile, Ja links, Nein rechts.
Das PDF baut Trigonometrie Klasse 10/baue_rezept_trigo.py aus dieser Datei.
"""
import json
import math
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import Mindmap  # noqa: E402

ZIEL = VAULT / "04 Ressourcen/Mathematik/Trigonometrie Klasse 10/Mathe 10b – Rezept Trigonometrie – Kurzfassung.excalidraw"
BLAU, ROT, DUNKEL, GRAU = "#2563a8", "#c2185b", "#1e3a5f", "#475569"
SCHRITT = ("#f1f5f9", DUNKEL)
FRAGE = ("#fff4d6", "#b45309")

m = Mindmap("x")
weg = {m.mitte["id"]} | {e["id"] for e in m.E if e.get("containerId") == m.mitte["id"]}
m.E = [e for e in m.E if e["id"] not in weg]


def teil(name, start):
    """Elemente ab Index start als Teil `name` markieren (customData bleibt in Excalidraw erhalten);
    die Präsentation deckt die Teile damit einzeln auf."""
    for e in m.E[start:]:
        e["customData"] = {"teil": name}


def oben_buendig(kasten, abstand=12):
    t = next(e for e in m.E if e.get("containerId") == kasten["id"])
    t["verticalAlign"], t["y"] = "top", kasten["y"] + abstand


def nummer(x, y, nr):
    m.box(x - 24, y - 24, 48, 48, str(nr), 24, BLAU, BLAU, "ellipse", "#ffffff")


def schritt(nr, y, h, titel, rest="", x=60, w=780):
    m.gruppe = [f"s{nr}"]
    b = m.box(x, y, w, h, titel, 24, *SCHRITT, tcol=DUNKEL)
    if rest:
        oben_buendig(b)
        m.text(x, y + 50, rest, 20, "#374151", "center", w=w)
    nummer(x, y + h / 2, nr)
    m.gruppe = []
    return b


def pfeil(a, b, p, q, label=None, col=DUNKEL):
    m.gruppe = []
    arr = m.pfeil([p, q], col, 2.5, a, b)
    if label:
        fs = 20
        tw, th = len(label) * fs * 0.6, fs * 1.25
        m.text((p[0] + q[0]) / 2 - tw / 2, (p[1] + q[1]) / 2 - th / 2, label, fs, col, "center", arr, tw)
    return arr


def rechter(x, y, start, r=14):
    pts = [(x + r * math.cos(math.radians(start + k * 15)), y + r * math.sin(math.radians(start + k * 15))) for k in range(7)]
    m.linie(pts, ROT, 1.5)
    w = math.radians(start + 45)
    m.ell(x + r * .48 * math.cos(w), y + r * .48 * math.sin(w), 2.5, ROT, ROT, 1)


n = len(m.E); s0 = schritt(0, 0, 90, "Alles Gegebene in die Skizze eintragen", "Gesuchtes rot markieren"); teil("s0", n)
n = len(m.E); s1 = schritt(1, 140, 90, "Gibt es Winkel, die ich direkt erkenne?",
                           "Scheitel-, Neben-, Stufen-, Wechselwinkel; Winkelsumme 180°"); teil("s1", n)
n = len(m.E); pfeil(s0, s1, (450, 96), (450, 134)); teil("p01", n)

n = len(m.E)
m.gruppe = ["s2"]
f2 = m.box(240, 280, 420, 140, "Ist das Dreieck\nrechtwinklig?", 22, *FRAGE, typ="diamond", tcol="#1f2937")
m.box(282, 330, 40, 40, "2", 22, BLAU, BLAU, "ellipse", "#ffffff")
m.gruppe = []
teil("s2", n)
n = len(m.E); pfeil(s1, f2, (450, 236), (450, 274)); teil("p12", n)

n = len(m.E); ja = m.box(20, 480, 320, 260, "sin, cos\noder tan", 28, "#ecfdf5", "#047857", tcol="#047857"); teil("ja", n)
n = len(m.E)
m.gruppe = ["nein"]
nein = m.box(500, 480, 380, 260, "Höhe oder Rechendreieck\neinzeichnen", 22, "#fdf2f8", ROT, tcol=ROT)
oben_buendig(nein)
m.text(500, 548, "sodass ein rechtwinkliges\nDreieck entsteht", 17, "#1f2937", "center", w=380)
# Oskar 19.11.: Die Höhe darf nicht die einzige bekannte Seite teilen
m.text(500, 594, "nie die einzige bekannte\nSeite teilen", 17, ROT, "center", w=380)
m.linie([(600, 725), (780, 725), (660, 648), (600, 725)], "#1f2937", 2, fill="#ffffff")
m.linie([(660, 648), (660, 725)], ROT, 2, "dashed")
rechter(660, 725, 270)
m.gruppe = []
teil("nein", n)
n = len(m.E); pfeil(f2, ja, (234, 352), (180, 474), "Ja"); teil("pja", n)
n = len(m.E); pfeil(f2, nein, (666, 352), (690, 474), "Nein"); teil("pnein", n)

n = len(m.E); s3 = schritt(3, 795, 90, "Gleichung mit genau einer Unbekannten",
                           "zwei Seiten oder eine Seite und ein Winkel"); teil("s3", n)
n = len(m.E); pfeil(ja, s3, (180, 746), (180, 789)); teil("pja3", n)
n = len(m.E); pfeil(nein, s3, (690, 746), (690, 789)); teil("pnein3", n)
n = len(m.E); s4 = schritt(4, 935, 120, "Nach der Unbekannten auflösen",
                           "Unbekannte oben: mal Nenner; unten: tauschen\nzwei Nachkommastellen, auch bei Winkeln"); teil("s4", n)
n = len(m.E); pfeil(s3, s4, (450, 891), (450, 929)); teil("p34", n)

n = len(m.E); ff = m.box(290, 1105, 320, 120, "Alles\nberechnet?", 22, *FRAGE, typ="diamond", tcol="#1f2937"); teil("ff", n)
n = len(m.E); pfeil(s4, ff, (450, 1061), (450, 1099)); teil("p4f", n)
n = len(m.E); fertig = m.box(40, 1130, 180, 70, "Fertig", 22, "#ffffff", ROT, tcol=ROT, sw=3); teil("fertig", n)
n = len(m.E); zurueck = m.box(680, 1130, 200, 70, "zurück zu 1", 20, "#f8fafc", GRAU, tcol=GRAU); teil("zurueck", n)
n = len(m.E); pfeil(ff, fertig, (284, 1165), (226, 1165), "Ja"); teil("pfertig", n)
n = len(m.E); pfeil(ff, zurueck, (616, 1165), (674, 1165), "Nein"); teil("pzurueck", n)
m.mitte = s0

if __name__ == "__main__":
    ws = VAULT / ".obsidian/workspace.json"
    offen = json.loads(ws.read_text(encoding="utf-8")) if ws.exists() else {}
    offen.pop("lastOpenFiles", None)                     # nur offene Tabs zählen, nicht die Liste „zuletzt geöffnet“
    if ZIEL.name in json.dumps(offen, ensure_ascii=False):
        raise SystemExit(f"{ZIEL.name} ist in Obsidian offen, erst schließen.")
    m.speichern(ZIEL)
    if len(sys.argv) > 1:
        m.vorschau(sys.argv[1])
