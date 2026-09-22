#!/usr/bin/env python3
"""Erzeugt europa_pfad.txt: Küstenlinien/Ländergrenzen für die Wetterkarte (Folie 2).
Quelle: Natural Earth (gemeinfrei) über das npm-Paket world-atlas (countries-50m.json).
Einmalig ausführen: python3 europakarte_erzeugen.py <pfad/zu/countries-50m.json>
Projektion: Mercator, an die Lage der Städte in der Buchkarte angepasst (siehe baue_stunde1.py)."""
import json, math, sys
from pathlib import Path

AX, BX, AY, BY = 23.5117, 417.19, -1170.57, 1602.89   # x = AX*lon + BX ; y = AY*merc(lat) + BY
W, H, M = 1400, 850, 40


def merc(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def proj(lon, lat):
    return AX * lon + BX, AY * merc(max(min(lat, 85), -85)) + BY


def clip(poly, xmin, ymin, xmax, ymax):
    def edge(pts, inside, inter):
        out = []
        for i, p in enumerate(pts):
            q = pts[i - 1]
            if inside(p):
                if not inside(q):
                    out.append(inter(q, p))
                out.append(p)
            elif inside(q):
                out.append(inter(q, p))
        return out
    def ix(x):
        return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]))
    def iy(y):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y)
    for ins, it in ((lambda p: p[0] >= xmin, ix(xmin)), (lambda p: p[0] <= xmax, ix(xmax)),
                    (lambda p: p[1] >= ymin, iy(ymin)), (lambda p: p[1] <= ymax, iy(ymax))):
        if not poly:
            return []
        poly = edge(poly, ins, it)
    return poly


def main(pfad):
    topo = json.loads(Path(pfad).read_text())
    sc, tr = topo["transform"]["scale"], topo["transform"]["translate"]
    arcs = []
    for a in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx; y += dy
            pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)
    def arc(i):
        return arcs[i] if i >= 0 else arcs[~i][::-1]
    d = []
    for g in topo["objects"]["countries"]["geometries"]:
        polys = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"] if g["type"] == "MultiPolygon" else []
        for poly in polys:
            ring = []
            for i in poly[0]:
                p = arc(i)
                ring.extend(p if not ring else p[1:])
            pts = [proj(*p) for p in ring]
            pts = clip(pts, -M, -M, W + M, H + M)
            if len(pts) < 3:
                continue
            simp = [pts[0]]
            for p in pts[1:]:
                if abs(p[0] - simp[-1][0]) + abs(p[1] - simp[-1][1]) >= 2.6:
                    simp.append(p)
            if len(simp) < 3:
                continue
            area = abs(sum(simp[i][0] * simp[i - 1][1] - simp[i - 1][0] * simp[i][1] for i in range(len(simp)))) / 2
            if area < 25:
                continue
            d.append("M" + "L".join(f"{p[0]:.0f} {p[1]:.0f}" for p in simp) + "Z")
    out = Path(__file__).with_name("europa_pfad.txt")
    out.write_text("".join(d))
    print(out, len("".join(d)) // 1024, "KB,", len(d), "Ringe")


if __name__ == "__main__":
    main(sys.argv[1])
