#!/usr/bin/env python3
"""Baut das Druckset für Oskars analoge Planer-Mappe (A4, Ringordner oder Dokumentmappe).

Aufruf: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/planer_bauen.py
Ausgabe: 04 Ressourcen/Planer/Planer – Druckset.pdf
Inhalt: Deckblatt, Inhaltsverzeichnis, Register-Trennblätter mit Reiter und je eine Muster-Vorlage.
Alles leer: keine Namen, keine Daten. Vorlagen aus meeting_vorlagen.py, Rahmen-Stil.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
import meeting_vorlagen as m
from meeting_vorlagen import (W, H, LM, RM, CW, GAP, BLUE, TEAL, ORANGE, GREY, LINE, INK,
                              header, box, todo, strip, dots, back, rating, tint)

PURPLE = HexColor("#8B7FB8")
GREEN = HexColor("#5F9E78")
WHITE = HexColor("#FFFFFF")

REGISTER = [
    ("1", "Planung", BLUE, "Woche, Tag, To-dos", ["Wochenplan", "Tagesplan", "To-do-Liste"]),
    ("2", "Konferenzen", TEAL, "Sitzungen, GLK, Dienstbesprechungen", ["Notizen Konferenz"]),
    ("3", "Gespräche", ORANGE, "Gespräche zu zweit, Elterngespräche", ["Notizen Gespräch zu zweit"]),
    ("4", "Mentoring", GREEN, "Mentoring-Gespräche mit Schülern", ["Notizen Mentoring-Gespräch"]),
    ("5", "Projekte", PURPLE, "Konzepte, Vorhaben, Ideen", ["Projektseite"]),
    ("6", "Notizen", GREY, "Freie Seiten, Dots", ["Notizseite (Dots)"]),
]


def tab(c, idx, col, label):
    """Reiter am rechten Rand, gestaffelt."""
    n = len(REGISTER)
    h = 92
    gap = 8
    y_top = H - 60 - idx * (h + gap)
    x = W - 40
    c.setFillColor(col)
    c.roundRect(x, y_top - h, 30, h, 5, stroke=0, fill=1)
    c.saveState()
    c.translate(x + 19, y_top - h / 2)
    c.rotate(90)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(0, -3.5, label)
    c.restoreState()


def deckblatt(c):
    c.setTitle("Planer")
    c.setFillColor(tint(BLUE, 0.14))
    c.rect(0, H * 0.45, W, H * 0.2, stroke=0, fill=1)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.2)
    c.line(0, H * 0.65, W, H * 0.65)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 44)
    c.drawString(LM + 20, H * 0.54, "PLANER")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Oblique", 15)
    c.drawString(LM + 22, H * 0.49, "Schule, Gespräche, Projekte")
    y = H * 0.28
    for lab, val in [("Name", ""), ("Schuljahr", "2026/27")]:
        c.setFillColor(GREY)
        c.setFont("Helvetica", 9)
        c.drawString(LM + 20, y + 3, lab)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(LM + 80, y, W - 90, y)
        if val:
            c.setFillColor(INK)
            c.setFont("Helvetica", 12)
            c.drawString(LM + 84, y + 3, val)
        y -= 30
    c.showPage()
    c.showPage()  # Rückseite leer


def inhalt(c):
    header(c, "Inhaltsverzeichnis", [], title="PLANER")
    y = H - 110
    for nr, name, col, sub, sheets in REGISTER:
        c.setFillColor(col)
        c.circle(LM + 14, y + 4, 13, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(LM + 14, y - 1, nr)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(LM + 40, y + 2, name)
        c.setFillColor(GREY)
        c.setFont("Helvetica", 9)
        c.drawString(LM + 40, y - 11, sub)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(LM + 40, y - 20, W - RM, y - 20)
        y -= 52
    c.showPage()
    # Rückseite: eigenes Verzeichnis
    header(c, "Eigenes Verzeichnis", [], title="PLANER")
    cols = [("Datum", 0.0, 0.15), ("Register", 0.15, 0.32), ("Thema / Seite", 0.32, 1.0)]
    top = H - 84
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(BLUE)
    for lab, a, b in cols:
        c.drawString(LM + a * CW + 4, top - 8, lab)
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.8)
    c.line(LM, top - 14, LM + CW, top - 14)
    yy = top - 14 - 20
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    while yy > 40:
        c.line(LM, yy, LM + CW, yy)
        yy -= 20
    c.showPage()


def trennblatt(c, idx):
    nr, name, col, sub, sheets = REGISTER[idx]
    tab(c, idx, col, f"{nr}  {name}")
    c.setFillColor(tint(col, 0.14))
    c.rect(LM, H * 0.55, CW - 30, 150, stroke=0, fill=1)
    c.setStrokeColor(col)
    c.setLineWidth(1.2)
    c.line(LM, H * 0.55 + 150, LM + CW - 30, H * 0.55 + 150)
    c.setFillColor(col)
    c.setFont("Helvetica-Bold", 72)
    c.drawString(LM + 20, H * 0.55 + 62, nr)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(LM + 85, H * 0.55 + 70, name)
    c.setFillColor(GREY)
    c.setFont("Helvetica", 11)
    c.drawString(LM + 87, H * 0.55 + 48, sub)
    c.showPage()
    c.showPage()  # Rückseite leer


def wochenplan(c):
    header(c, "Wochenplan", ["Woche (KW)", "von", "bis"], title="PLANER")
    top = H - 84
    box(c, LM, top, CW, 62, BLUE, "Wochenziele", outline=True, dotted=False, step=14)
    colw = (CW - GAP) / 2
    rowh, gap = 203, 6
    y = top - 62 - gap
    tage = [("Montag", BLUE), ("Dienstag", TEAL), ("Mittwoch", BLUE),
            ("Donnerstag", TEAL), ("Freitag", BLUE), ("Samstag / Sonntag", GREY)]
    for i, (t, col) in enumerate(tage):
        r, k = divmod(i, 2)
        box(c, LM + k * (colw + GAP), y - r * (rowh + gap), colw, rowh, col, t,
            step=16, outline=True, dotted=False)
    strip(c, 54, 24, "Nächste Woche / Mitnehmen", outline=True)
    back(c)
    c.showPage()


def tagesplan(c):
    header(c, "Tagesplan", ["Datum", "Wochentag"], title="PLANER")
    top = H - 84
    colw = (CW - GAP) / 2
    # Befinden
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.8)
    c.roundRect(LM, top - 30, CW, 30, 4, stroke=1, fill=0)
    rating(c, LM + 8, top - 13, "Befinden (1 schlecht, 5 gut)", colw)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(LM + colw + 8, top - 10, "Schlaf (Std.)")
    c.setStrokeColor(LINE)
    c.line(LM + colw + 60, top - 12, LM + colw + 110, top - 12)
    # Termine links mit Zeitleiste
    ty = top - 38
    th = 380
    box(c, LM, ty, colw, th, BLUE, "Termine", outline=True, dotted=False, lines=False)
    yy = ty - 32
    stunde = 7
    c.setFont("Helvetica", 7)
    while yy > ty - th + 6:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(LM + 26, yy, LM + colw - 8, yy)
        c.setFillColor(GREY)
        c.drawString(LM + 8, yy + 3, f"{stunde}")
        yy -= 24
        stunde += 1
    # Top 3 rechts
    box(c, LM + colw + GAP, ty, colw, 120, ORANGE, "Top 3 heute", outline=True, dotted=False,
        numbered=True, step=28)
    box(c, LM + colw + GAP, ty - 126, colw, th - 126, TEAL, "Notizen", outline=True)
    # To-dos unten
    todo(c, ty - th - 8, ty - th - 8 - 40, title="To-dos", who="Wer?", when="Bis wann?", outline=True)
    strip(c, 54 - 14, 24, "Morgen / Mitnehmen", outline=True)
    back(c)
    c.showPage()


def todoliste(c):
    header(c, "To-do-Liste", ["Bereich / Thema", "Datum"], title="PLANER")
    todo(c, H - 84, H - 84 - 54, title="To-dos", who="Wer?", when="Bis wann?", outline=True)
    back(c)
    c.showPage()


def projekt(c):
    header(c, "Projektseite", ["Projekt", "Start", "Ende"], title="PLANER")
    top = H - 84
    box(c, LM, top, CW, 80, PURPLE, "Ziel", outline=True, dotted=False)
    box(c, LM, top - 88, CW, 150, BLUE, "Schritte / Meilensteine", outline=True, dotted=False, numbered=True)
    box(c, LM, top - 246, CW, 120, TEAL, "Beteiligte / Absprachen", outline=True, dotted=False)
    todo(c, top - 374, 132, title="Nächste Schritte", outline=True)
    box(c, LM, top - 514, CW, top - 514 - 54, GREY, "Notizen", outline=True)
    strip(c, 54, 24, "Nächster Check", outline=True)
    back(c)
    c.showPage()


def notizseite(c):
    header(c, "Notizen", ["Thema", "Datum"])
    dots(c, LM, 30, CW, H - 130)
    c.showPage()
    dots(c, LM, 30, CW, H - 60)
    c.showPage()


def bauen(path):
    c = canvas.Canvas(path, pagesize=A4)
    deckblatt(c)
    inhalt(c)
    sheets = {
        0: [wochenplan, tagesplan, todoliste],
        1: [lambda c: m.konferenz(None, outline=True, c=c)],
        2: [lambda c: m.zweiergespraech(None, outline=True, c=c)],
        3: [lambda c: m.mentoring(None, outline=True, c=c)],
        4: [projekt],
        5: [notizseite],
    }
    for i in range(len(REGISTER)):
        trennblatt(c, i)
        for f in sheets[i]:
            f(c)
    c.setTitle("Planer – Druckset")
    c.save()


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "04 Ressourcen", "Planer")
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, "Planer – Druckset.pdf")
    bauen(p)
    print("fertig:", os.path.abspath(p))
