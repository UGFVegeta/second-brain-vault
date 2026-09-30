#!/usr/bin/env python3
"""Löst Oskars zweiseitiges Blatt „Halbwertszeit“ (Einzeichnen) auf seinem Original-Layout aus: Materialien/Halbwertszeit AB Einzeichnen (Oskar) – Lösung.pdf
Quelle: iCloud-Original liegt als Halbwertszeit AB Einzeichnen (Oskar).pdf im Materialien-Ordner. Magenta = Lösung.
Seite 1: Definition und Lückentext. Seite 2: Fluor-20-Kurve (225 Kerne, T = 11 s) und die Lücken zum zeitlichen Verlauf."""
import fitz
from pathlib import Path

HIER = Path(__file__).parent / "Materialien"
QUELLE = HIER / "Halbwertszeit AB Einzeichnen (Oskar).pdf"
ZIEL = HIER / "Halbwertszeit AB Einzeichnen (Oskar) – Lösung.pdf"
FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
MAG = (0.9, 0.0, 0.49)

d = fitz.open(QUELLE)
_font = fitz.Font(fontfile=FONT)


def fuelle(p, rect, text, groesse=13):
    r = fitz.Rect(rect)
    b = _font.text_length(text, fontsize=groesse)
    p.insert_text((r.x0 + max(2, (r.width - b) / 2), r.y0 + r.height / 2 + groesse * 0.33), text, fontname="tnr", fontfile=FONT, fontsize=groesse, color=MAG)


# ---- Seite 1
p = d[0]
p.insert_font(fontname="tnr", fontfile=FONT)
fuelle(p, (85, 497, 161, 528), "nicht")
fuelle(p, (272, 564, 379, 596), "Sekunde")
fuelle(p, (85, 603, 224, 635), "Millionen")
fuelle(p, (85, 672, 491, 703), "sichere Aussage")
# Definition in die Kästchen (Zeilen im Raster, je 2 Kästchen hoch); Raster liegt oben links
for zeile, text in enumerate(["Die Halbwertszeit T½ ist die Zeit, nach der", "die Hälfte aller Kerne zerfallen ist."]):
    p.insert_text((92, 148.4 + zeile * 25.4), text, fontname="tnr", fontsize=14, color=MAG)
p.insert_text((430, 38), "LÖSUNG", fontname="tnr", fontsize=13, color=MAG)

# ---- Seite 2
p = d[1]
p.insert_font(fontname="tnr", fontfile=FONT)
X0, DX = 117.1, 56.8 / 10      # t = 0 und Punkte je Sekunde
Y0, DY = 506.9, 1.42           # N = 0 und Punkte je Kern
N0, T = 225.0, 11.0
pts = [(X0 + t * DX, Y0 - N0 * 0.5 ** (t / T) * DY) for t in [i * 0.5 for i in range(0, 121)]]
shape = p.new_shape()
shape.draw_polyline(pts)
shape.finish(color=MAG, width=1.6, closePath=False)
for t in range(0, 61, 2):                                    # Messpunkte alle 2 s wie im Zerfallslabor
    n = N0 * 0.5 ** (t / T)
    shape.draw_circle((X0 + t * DX, Y0 - n * DY), 2.2)
shape.finish(color=MAG, fill=MAG, width=0.5)
for k in (1, 2, 3):                                          # Halbwertszeiten als gestrichelte Hilfslinien
    t, n = k * T, N0 * 0.5 ** k
    shape.draw_polyline([(X0, Y0 - n * DY), (X0 + t * DX, Y0 - n * DY), (X0 + t * DX, Y0)])
    shape.finish(color=MAG, width=0.7, dashes="[3 2] 0", closePath=False)
shape.commit()
fuelle(p, (335, 612, 404, 636), "Hälfte")
fuelle(p, (413, 612, 446, 636), "50 %", 12)
fuelle(p, (194, 647, 216, 671), "2")
fuelle(p, (275, 647, 356, 671), "Viertel")
fuelle(p, (365, 647, 398, 671), "25 %", 12)
fuelle(p, (194, 682, 216, 706), "3")
fuelle(p, (275, 682, 344, 706), "Achtel")
fuelle(p, (353, 682, 410, 706), "12,5 %", 12)
fuelle(p, (194, 717, 216, 741), "4")
fuelle(p, (272, 717, 330, 741), "6 %")
p.insert_text((430, 38), "LÖSUNG", fontname="tnr", fontsize=13, color=MAG)
d.save(ZIEL)
print("geschrieben:", ZIEL.name)
