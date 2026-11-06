#!/usr/bin/env python3
"""Mathe 10b – Karoblätter für die Klassenarbeit Nr. 1, Teil ohne Taschenrechner.
Ein A4-Blatt, doppelseitig bedruckt (Vorder- und Rückseite), beide Seiten kariert (5 mm).
Das Raster liegt auf beiden Seiten an derselben Stelle (Rand 10 mm), damit Vorder- und Rückseite beim Duplexdruck deckungsgleich sind.
Aufruf: python3 baue_karoblaetter_ka1_10b.py   (Framework-Python 3.12 mit reportlab)"""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

HIER = Path(__file__).parent
ZIEL = HIER / "Mathe 10b – Klassenarbeit Nr. 1 – Teil ohne Taschenrechner – Karoblatt (doppelseitig).pdf"

B, H = A4
RAND = 10 * mm
RASTER = 5 * mm
LINIE = (0.725, 0.784, 0.847)      # #b9c8d8 wie in den Kästchenfeldern der anderen Arbeiten
RAHMEN = (0.624, 0.702, 0.784)     # #9fb3c8
GRAU = (0.784, 0.784, 0.784)       # #c8c8c8, graue Titelzeile wie im Kopf der Klassenarbeiten
DUNKEL = (0.333, 0.333, 0.333)


def karo(c, y_oben, y_unten):
    """Raster zwischen y_oben und y_unten (von unten gemessen), Breite = Seite minus Rand."""
    x0, x1 = RAND, B - RAND
    spalten = int((x1 - x0) / RASTER + 1e-6)
    zeilen = int((y_oben - y_unten) / RASTER + 1e-6)
    x1 = x0 + spalten * RASTER
    y_unten = y_oben - zeilen * RASTER
    c.setStrokeColorRGB(*LINIE)
    c.setLineWidth(0.25 * mm)
    for i in range(spalten + 1):
        c.line(x0 + i * RASTER, y_unten, x0 + i * RASTER, y_oben)
    for j in range(zeilen + 1):
        c.line(x0, y_unten + j * RASTER, x1, y_unten + j * RASTER)
    c.setStrokeColorRGB(*RAHMEN)
    c.setLineWidth(0.6)
    c.rect(x0, y_unten, x1 - x0, y_oben - y_unten)
    return zeilen, spalten


def kopf(c):
    """Titelzeile (grau) und Zeile mit Teil und Namensfeld; gibt die Unterkante zurück."""
    x0, x1 = RAND, B - RAND
    oben = H - RAND
    h1, h2 = 11 * mm, 10 * mm
    c.setLineWidth(0.6)
    c.setStrokeColorRGB(*DUNKEL)
    c.setFillColorRGB(*GRAU)
    c.rect(x0, oben - h1, x1 - x0, h1, fill=1, stroke=1)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont("Arial-Bold", 14)
    c.drawCentredString((x0 + x1) / 2, oben - h1 + 3.6 * mm, "Klassenarbeit Nr. 1 – Mathematik 10b")
    c.setFillColorRGB(1, 1, 1)
    c.rect(x0, oben - h1 - h2, x1 - x0, h2, fill=1, stroke=1)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont("Arial-Bold", 12)
    c.drawString(x0 + 3 * mm, oben - h1 - h2 + 3.3 * mm, "Teil ohne Taschenrechner")
    c.setFont("Arial", 11)
    c.drawString(x0 + 105 * mm, oben - h1 - h2 + 3.3 * mm, "Name:")
    c.setLineWidth(0.5)
    c.line(x0 + 118 * mm, oben - h1 - h2 + 3 * mm, x1 - 3 * mm, oben - h1 - h2 + 3 * mm)
    return oben - h1 - h2


def bauen():
    c = canvas.Canvas(str(ZIEL), pagesize=A4)
    c.setTitle("Mathe 10b – Klassenarbeit Nr. 1 – Teil ohne Taschenrechner – Karoblatt")
    c.setAuthor("Oskar Klein")
    # Vorderseite: Kopf, darunter Raster
    kopf(c)
    # Kopf ist 21 mm hoch, das Raster beginnt 25 mm unter dem Rand = 5 Kästchen, damit die Linien auf Vorder- und Rückseite genau übereinander liegen
    z1, s = karo(c, H - RAND - 25 * mm, RAND + 5 * mm)
    c.showPage()
    # Rückseite: nur Raster, gleiche Spalten
    z2, _ = karo(c, H - RAND, RAND + 5 * mm)
    c.showPage()
    c.save()
    print(ZIEL.name, "| Vorderseite", z1, "Zeilen,", s, "Spalten | Rückseite", z2, "Zeilen")


if __name__ == "__main__":
    bauen()
