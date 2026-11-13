#!/usr/bin/env python3
"""Gemeinsamer Generator für Excalidraw-Mindmaps im Stil „Kernphysik Klasse 10“ (13.11.2026).

Aufbau: dunkle Ellipse in der Mitte, sechs Äste in die Breite (drei oben, drei unten, je eigene Farbe),
je Ast ein großer Kasten mit vier Punkt-Kästen (Text fest gebunden über containerId) und rechts eine
kleine Zeichnung. Kasten, Punkte und Zeichnung tragen eine gemeinsame groupId. Verbindungen nur als
gerade, an beiden Enden gebundene Pfeile (Mitte → Ast → Kasten). Keine frei stehenden Texte außer
Beschriftungen in Zeichnungen.

Geplantes (noch nicht unterrichtet) wird gestrichelt gezeichnet: ganzer Ast mit geplant=True,
einzelne Punkte mit drittem Eintrag True: ("Titel", "Unterzeile", True).

Benutzung (siehe .scripts/mindmaps/*.py):

    from mindmap_excalidraw import Mindmap
    m = Mindmap("Mathematik\\nKlasse 7c")
    zx, zy = m.ast(0, "1  Rationale Zahlen", [("Punkt", "Unterzeile"), ...])
    m.ell(zx, zy, 10, "#fff")            # Zeichnung um den Mittelpunkt (zx, zy) des freien Felds
    ...
    m.legende("Stand 13.11.2026\\ndurchgezogen: gemacht\\ngestrichelt: geplant")
    m.speichern(pfad)                    # prüft vorher (Text passt, Pfeile gebunden, nichts ragt raus)
    m.vorschau(png)                      # SVG + Chrome headless → PNG

Zeichenfeld rechts neben den Punkten: etwa 400 × 380 px um (zx, zy).
"""
import json
import random
import subprocess
import html as _html
from pathlib import Path

FS_CH = 0.6        # Zeichenbreite je fontSize (fontFamily 3, monospace)
FARBEN = [("#dbeafe", "#1e40af"), ("#fed7aa", "#c2410c"), ("#fef3c7", "#b45309"),
          ("#fee2e2", "#dc2626"), ("#ddd6fe", "#6d28d9"), ("#a7f3d0", "#047857")]
XS = [-1250, 0, 1250]   # Mittelpunkte der Äste
AY = 260                # Abstand der Äste von der Mitte (oben −, unten +)
PUNKT_H, PUNKT_ABSTAND, PUNKT_B = 80, 92, 625
KASTEN_B = 1090
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


class Mindmap:
    def __init__(self, titel, seed=7, farben=FARBEN):
        random.seed(seed)
        self.E, self.gruppe, self.farben = [], [], farben
        self.aeste, self.kaesten = {}, {}
        self.mitte = self.box(-230, -75, 460, 150, titel, 34, "#1e293b", "#0f172a", "ellipse", "#ffffff")

    # ------------------------------------------------------------ Grundelemente
    def base(self, t, x, y, w, h, **k):
        d = dict(id=k.pop("id", f"e{len(self.E)}"), type=t, x=x, y=y, width=w, height=h, angle=0,
                 strokeColor=k.pop("stroke", "#1e3a5f"), backgroundColor=k.pop("fill", "transparent"),
                 fillStyle="solid", strokeWidth=k.pop("sw", 2), strokeStyle=k.pop("style", "solid"), roughness=0,
                 opacity=100, groupIds=list(self.gruppe), frameId=None, roundness=k.pop("round", None),
                 seed=random.randint(1, 2**31), version=1, versionNonce=random.randint(1, 2**31), isDeleted=False,
                 boundElements=[], updated=1, link=None, locked=False)
        d.update(k)
        self.E.append(d)
        return d

    def text(self, x, y, s, fs=18, col="#374151", align="left", cont=None, w=None):
        """Freier Text nur für Beschriftungen in Zeichnungen; sonst über box() gebunden."""
        zeilen = s.split("\n")
        ww = w or max(len(z) for z in zeilen) * fs * FS_CH
        hh = len(zeilen) * fs * 1.25
        d = self.base("text", x, y, ww, hh, stroke=col, sw=1, text=s, originalText=s, fontSize=fs, fontFamily=3,
                      textAlign=align, verticalAlign="middle" if cont else "top",
                      containerId=cont["id"] if cont else None, lineHeight=1.25, baseline=int(fs))
        if cont:
            cont["boundElements"].append({"type": "text", "id": d["id"]})
        return d

    def box(self, x, y, w, h, s, fs, fill, stroke, typ="rectangle", tcol="#1f2937", style="solid", sw=2):
        b = self.base(typ, x, y, w, h, fill=fill, stroke=stroke, sw=sw, style=style,
                      round={"type": 3} if typ == "rectangle" else {"type": 2})
        zeilen = s.split("\n")
        tw, th = max(len(z) for z in zeilen) * fs * FS_CH, len(zeilen) * fs * 1.25
        self.text(x + (w - tw) / 2, y + (h - th) / 2, s, fs, tcol, "center", b, tw)
        return b

    def ell(self, cx, cy, r, fill, stroke="#1e3a5f", sw=1.5, rx=None, ry=None, style="solid"):
        rx, ry = rx or r, ry or r
        return self.base("ellipse", cx - rx, cy - ry, 2 * rx, 2 * ry, fill=fill, stroke=stroke, sw=sw, style=style)

    def rect(self, x, y, w, h, fill, stroke="#1e3a5f", sw=1.5, style="solid"):
        return self.base("rectangle", x, y, w, h, fill=fill, stroke=stroke, sw=sw, style=style)

    def pfeil(self, pts, col="#1e3a5f", sw=2, a=None, b=None, style="solid", head="arrow"):
        x0, y0 = pts[0]
        rel = [[px - x0, py - y0] for px, py in pts]
        xs, ys = [p[0] for p in rel], [p[1] for p in rel]
        d = self.base("arrow", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke=col, sw=sw, style=style,
                      points=rel, lastCommittedPoint=None, startArrowhead=None, endArrowhead=head, round={"type": 2},
                      startBinding={"elementId": a["id"], "focus": 0, "gap": 6} if a else None,
                      endBinding={"elementId": b["id"], "focus": 0, "gap": 6} if b else None)
        for el in (a, b):
            if el:
                el["boundElements"].append({"type": "arrow", "id": d["id"]})
        return d

    def linie(self, pts, col="#64748b", sw=1.5, style="solid", fill="transparent"):
        """Achsen, Kurven, Formen in Zeichnungen (verbindet nichts)."""
        x0, y0 = pts[0]
        rel = [[px - x0, py - y0] for px, py in pts]
        xs, ys = [p[0] for p in rel], [p[1] for p in rel]
        return self.base("line", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke=col, sw=sw, style=style, fill=fill,
                         points=rel, lastCommittedPoint=None, startArrowhead=None, endArrowhead=None, round=None,
                         polygon=pts[0] == pts[-1] and len(pts) > 2)   # geschlossen = Fläche, wird gefüllt

    # ------------------------------------------------------------ Mindmap-Bausteine
    def ast(self, i, titel, punkte, geplant=False, fs=17):
        """Ast i (0–2 oben, 3–5 unten) mit Titelkasten, Pfeil aus der Mitte, großem Kasten und Punkten.
        Gibt den Mittelpunkt des freien Zeichenfelds rechts zurück; danach gezeichnete Elemente gehören
        zur Gruppe des Astes, bis der nächste Ast beginnt."""
        hell, col = self.farben[i]
        stil = "dashed" if geplant else "solid"
        self.gruppe = []
        x, y = XS[i % 3], -AY if i < 3 else AY
        oben = i < 3
        b = self.box(x - 190, y - 55, 380, 110, titel, 22, hell, col, style=stil)
        self.aeste[i] = b
        if i % 3 == 1:
            self.pfeil([(0, -75 if oben else 75), (0, y + (55 if oben else -55))], col, 2.5, self.mitte, b, stil)
        else:
            sx = -200 if i % 3 == 0 else 200
            self.pfeil([(sx, -40 if oben else 40), (x, y + (55 if oben else -55))], col, 2.5, self.mitte, b, stil)

        n = len(punkte)
        H = n * PUNKT_ABSTAND + 28
        ky = b["y"] - 60 - H if oben else b["y"] + b["height"] + 60
        self.gruppe = [f"ast{i}"]
        kasten = self.base("rectangle", x - 560, ky, KASTEN_B, H, fill=hell, stroke=col, sw=2, style=stil,
                           round={"type": 3})
        self.kaesten[i] = kasten
        for k, p in enumerate(punkte):
            t, sub = p[0], p[1]
            pg = geplant or (len(p) > 2 and p[2])
            s = f"{t}\n{sub}" if sub else t
            self.box(x - 545, ky + 16 + k * PUNKT_ABSTAND, PUNKT_B, PUNKT_H, s, fs, "#ffffff", col, tcol=col,
                     style="dashed" if pg else "solid", sw=1.5 if pg else 2)
        self.gruppe = []
        if oben:
            self.pfeil([(x, b["y"]), (x, ky + H)], col, 2.5, b, kasten, stil)
        else:
            self.pfeil([(x, b["y"] + b["height"]), (x, ky)], col, 2.5, b, kasten, stil)
        self.gruppe = [f"ast{i}"]
        return x + 305, ky + H / 2

    def legende(self, s, x=-810, y=-48, w=300, h=96):
        """Kleiner Erklärkasten links neben der Mitte (zwischen den Pfeilen)."""
        self.gruppe = []
        return self.box(x, y, w, h, s, 15, "#f8fafc", "#94a3b8", sw=1.5)

    # ------------------------------------------------------------ Prüfen, Speichern, Vorschau
    def pruefen(self):
        fehler = []
        nach_id = {e["id"]: e for e in self.E}
        for e in self.E:
            if e["type"] == "text" and e.get("containerId"):
                c = nach_id[e["containerId"]]
                breite = max(len(z) for z in e["text"].split("\n")) * e["fontSize"] * FS_CH
                platz = c["width"] - (40 if c["type"] == "rectangle" else c["width"] * 0.3)
                if breite > platz:
                    fehler.append(f"Text zu breit ({breite:.0f} > {platz:.0f}): {e['text']!r}")
                if e["height"] > c["height"] - 8:
                    fehler.append(f"Text zu hoch: {e['text']!r}")
            if e["type"] == "arrow" and not e["groupIds"]:
                if not (e["startBinding"] and e["endBinding"]):
                    fehler.append(f"Verbindungspfeil {e['id']} nicht an beiden Enden gebunden")
            if e["type"] == "text" and not e.get("containerId") and not e["groupIds"]:
                fehler.append(f"Frei stehender Text außerhalb einer Zeichnung: {e['text']!r}")
        # Zeichnungen und Punkte bleiben im Kasten
        for i, k in self.kaesten.items():
            for e in self.E:
                if e is k or e["groupIds"] != [f"ast{i}"]:
                    continue
                x0, y0, x1, y1 = rahmen(e)
                if (x0 < k["x"] - 1 or y0 < k["y"] - 1 or x1 > k["x"] + k["width"] + 1
                        or y1 > k["y"] + k["height"] + 1):
                    fehler.append(f"Ast {i + 1}: Element {e['id']} ({e['type']}) ragt aus dem Kasten")
        # Kästen und Äste überlappen sich nicht
        gross = list(self.kaesten.values()) + list(self.aeste.values()) + [self.mitte]
        for a in range(len(gross)):
            for b in range(a + 1, len(gross)):
                p, q = gross[a], gross[b]
                if (p["x"] < q["x"] + q["width"] and q["x"] < p["x"] + p["width"]
                        and p["y"] < q["y"] + q["height"] and q["y"] < p["y"] + p["height"]):
                    fehler.append(f"Überlappung: {p['id']} und {q['id']}")
        return fehler

    def speichern(self, pfad):
        fehler = self.pruefen()
        for f in fehler:
            print("FEHLER:", f)
        if fehler:
            raise SystemExit("Nicht gespeichert, erst die Fehler beheben.")
        doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": self.E,
               "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
        Path(pfad).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(self.E)} Elemente → {pfad}")

    def vorschau(self, png):
        """Rendert die Mindmap grob als SVG und nimmt sie mit Chrome headless als PNG auf
        (der Renderer des Excalidraw-Skills hängt beim Laden von esm.sh)."""
        svg = Path(png).with_suffix(".svg")
        b, h = svg_schreiben(self.E, svg)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size={b},{h}",
                        f"--screenshot={png}", svg.as_uri()], capture_output=True, timeout=60)
        print("Vorschau:", png)


def rahmen(e):
    """Tatsächlicher Rahmen; bei Linien und Pfeilen aus den Punkten (die dürfen negativ sein)."""
    if e["type"] in ("line", "arrow"):
        xs = [e["x"] + p[0] for p in e["points"]]
        ys = [e["y"] + p[1] for p in e["points"]]
        return min(xs), min(ys), max(xs), max(ys)
    return e["x"], e["y"], e["x"] + e["width"], e["y"] + e["height"]


def svg_schreiben(E, pfad, skala=1.6):
    r = [rahmen(e) for e in E]
    x0, y0 = min(a[0] for a in r) - 40, min(a[1] for a in r) - 40
    x1, y1 = max(a[2] for a in r) + 40, max(a[3] for a in r) + 40
    b, h = int((x1 - x0) / skala), int((y1 - y0) / skala)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" width="{b}" height="{h}">'
         '<defs><marker id="m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
         'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>'
         f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#fff"/>']
    for e in E:
        fill = e["backgroundColor"] if e["backgroundColor"] != "transparent" else "none"
        st = f'stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}"'
        if e["strokeStyle"] == "dashed":
            st += ' stroke-dasharray="8 6"'
        t = e["type"]
        if t == "rectangle":
            o.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["width"]}" height="{e["height"]}" '
                     f'rx="{12 if e.get("roundness") else 0}" fill="{fill}" {st}/>')
        elif t == "ellipse":
            o.append(f'<ellipse cx="{e["x"] + e["width"] / 2}" cy="{e["y"] + e["height"] / 2}" '
                     f'rx="{e["width"] / 2}" ry="{e["height"] / 2}" fill="{fill}" {st}/>')
        elif t in ("line", "arrow"):
            p = " ".join(f'{e["x"] + a},{e["y"] + c}' for a, c in e["points"])
            mk = ' marker-end="url(#m)"' if t == "arrow" and e.get("endArrowhead") else ""
            f = fill if t == "line" and e.get("polygon") else "none"
            o.append(f'<polyline points="{p}" fill="{f}" {st}{mk}/>')
        elif t == "text":
            a = {"left": "start", "center": "middle", "right": "end"}[e["textAlign"]]
            xx = e["x"] + (e["width"] / 2 if a == "middle" else e["width"] if a == "end" else 0)
            for k, z in enumerate(e["text"].split("\n")):
                o.append(f'<text x="{xx}" y="{e["y"] + e["fontSize"] * (1.25 * k + 1)}" font-family="Menlo,monospace" '
                         f'font-size="{e["fontSize"]}" fill="{e["strokeColor"]}" text-anchor="{a}">{_html.escape(z)}</text>')
    Path(pfad).write_text("".join(o) + "</svg>", encoding="utf-8")
    return b, h
