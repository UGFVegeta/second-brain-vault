#!/usr/bin/env python3
"""Baut das Druckset der Planer-Mappe in echtem A5 (eigenes Layout, nicht skaliert).

Aufruf: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/planer_a5.py
Ausgabe: 04 Ressourcen/Planer/Planer – Druckset A5.pdf
Zeilenabstand 19 bis 22 pt (rund 7 mm) zum Handschreiben. Heftrand links 17 mm auf der Vorderseite,
auf Rückseiten gespiegelt (Rückseite liegt beim Umblättern mit dem Rand rechts).
Alles leer: keine Namen, keine Daten.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.colors import HexColor
import meeting_vorlagen as m
from meeting_vorlagen import BLUE, TEAL, ORANGE, GREY, LINE, INK, tint, dots, rating, box, strip
from planer_bauen import REGISTER, PURPLE, GREEN, WHITE

W, H = A5
M_BIND = 48      # Heftrand (Lochung) in pt, ca. 17 mm
M_OUT = 22
CW = W - M_BIND - M_OUT
GAP = 6
STEP = 20        # Schreibzeile
TOP = H - 74

# Die Helfer aus meeting_vorlagen lesen diese Werte zur Laufzeit
m.W, m.H, m.LM, m.RM, m.CW = W, H, M_BIND, M_OUT, CW


def header(c, kind, fields):
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(M_BIND, H - 38, "PLANER")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(M_BIND + c.stringWidth("PLANER", "Helvetica-Bold", 16) + 10, H - 38, kind)
    if not fields:
        return
    n = len(fields)
    gap = 12
    colw = (CW - (n - 1) * gap) / n
    for i, f in enumerate(fields):
        x = M_BIND + i * (colw + gap)
        c.setFillColor(GREY)
        c.setFont("Helvetica", 7)
        c.drawString(x, H - 56, f)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(x + c.stringWidth(f, "Helvetica", 7) + 3, H - 57, x + colw, H - 57)


def back(c):
    """Rückseite gespiegelt: Heftrand rechts."""
    c.showPage()
    dots(c, M_OUT, 24, CW, H - 48)
    c.showPage()


def todo(c, ytop, h, title="To-dos", step=22, outline=True, col=ORANGE):
    x, w = M_BIND, CW
    m.frame(c, x, ytop, w, h, col, outline)
    c.setFillColor(col)
    c.circle(x + 11, ytop - 12, 5, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.circle(x + 11, ytop - 12, 1.8, stroke=0, fill=1)
    c.setFillColor(col)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 20, ytop - 15, title)
    c1, c2, c3 = x + w * 0.52, x + w * 0.76, x + w * 0.91
    c.setFont("Helvetica", 6.5)
    c.drawString(c1 + 3, ytop - 15, "Wer?")
    c.drawString(c2 + 3, ytop - 15, "Bis wann?")
    c.drawString(c3 + 1, ytop - 15, "fertig")
    yy = ytop - 18 - step
    while yy > ytop - h + 4:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x + 7, yy, c1 - 3, yy)
        c.line(c1 + 3, yy, c2 - 3, yy)
        c.line(c2 + 3, yy, c3 - 3, yy)
        c.setStrokeColor(col)
        c.circle(c3 + 14, yy + 5, 4.5, stroke=1, fill=0)
        yy -= step


def lined(c, x, ytop, w, h, col, title, numbered=False, dotted=False):
    box(c, x, ytop, w, h, col, title, step=STEP, numbered=numbered, outline=True, dotted=dotted)


def bottom_strip(c, label):
    strip(c, 24 + 22, 22, label, outline=True)


def deckblatt(c):
    c.setTitle("Planer A5")
    c.setFillColor(tint(BLUE, 0.14))
    c.rect(0, H * 0.45, W, H * 0.2, stroke=0, fill=1)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.2)
    c.line(0, H * 0.65, W, H * 0.65)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(M_BIND + 10, H * 0.54, "PLANER")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Oblique", 13)
    c.drawString(M_BIND + 12, H * 0.49, "Schule, Gespräche, Projekte")
    y = H * 0.27
    for lab, val in [("Name", ""), ("Schuljahr", "2026/27")]:
        c.setFillColor(GREY)
        c.setFont("Helvetica", 8.5)
        c.drawString(M_BIND + 10, y + 3, lab)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(M_BIND + 60, y, W - 50, y)
        if val:
            c.setFillColor(INK)
            c.setFont("Helvetica", 11)
            c.drawString(M_BIND + 64, y + 3, val)
        y -= 28
    c.showPage()
    c.showPage()


def inhalt(c):
    header(c, "Inhaltsverzeichnis", [])
    y = H - 100
    for nr, name, col, sub, sheets in REGISTER:
        c.setFillColor(col)
        c.circle(M_BIND + 13, y + 4, 12, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(M_BIND + 13, y - 0.5, nr)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(M_BIND + 36, y + 2, name)
        c.setFillColor(GREY)
        c.setFont("Helvetica", 8.5)
        c.drawString(M_BIND + 36, y - 10, sub)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(M_BIND + 36, y - 18, W - M_OUT, y - 18)
        y -= 48
    c.showPage()
    # Rückseite gespiegelt
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(M_OUT, H - 38, "EIGENES VERZEICHNIS")
    cols = [("Datum", 0.0, 0.17), ("Reg.", 0.17, 0.27), ("Thema / Seite", 0.27, 1.0)]
    top = H - 60
    c.setFont("Helvetica-Bold", 7.5)
    for lab, a, b in cols:
        c.drawString(M_OUT + a * CW + 3, top - 8, lab)
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.8)
    c.line(M_OUT, top - 14, M_OUT + CW, top - 14)
    yy = top - 14 - 22
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    while yy > 26:
        c.line(M_OUT, yy, M_OUT + CW, yy)
        yy -= 22
    c.showPage()


def tab(c, idx, col, label):
    h, gap = 80, 6
    y_top = H - 40 - idx * (h + gap)
    x = W - 32
    c.setFillColor(col)
    c.roundRect(x, y_top - h, 24, h, 4, stroke=0, fill=1)
    c.saveState()
    c.translate(x + 15, y_top - h / 2)
    c.rotate(90)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(0, -3, label)
    c.restoreState()


def trennblatt(c, idx):
    nr, name, col, sub, sheets = REGISTER[idx]
    tab(c, idx, col, f"{nr}  {name}")
    y0 = H * 0.55
    c.setFillColor(tint(col, 0.14))
    c.rect(M_BIND, y0, CW - 26, 120, stroke=0, fill=1)
    c.setStrokeColor(col)
    c.setLineWidth(1.2)
    c.line(M_BIND, y0 + 120, M_BIND + CW - 26, y0 + 120)
    c.setFillColor(col)
    c.setFont("Helvetica-Bold", 58)
    c.drawString(M_BIND + 14, y0 + 48, nr)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(M_BIND + 62, y0 + 56, name)
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9)
    c.drawString(M_BIND + 63, y0 + 38, sub)
    c.showPage()
    c.showPage()


def wochenplan(c):
    header(c, "Wochenplan", ["Woche (KW)", "von", "bis"])
    lined(c, M_BIND, TOP, CW, 52, BLUE, "Wochenziele")
    tage = [("Montag", BLUE), ("Dienstag", TEAL), ("Mittwoch", BLUE),
            ("Donnerstag", TEAL), ("Freitag", BLUE), ("Samstag / Sonntag", GREY)]
    y = TOP - 52 - GAP
    avail = y - (24 + 22 + 22 + GAP)
    rowh = (avail - 5 * GAP) / 6
    for t, col in tage:
        lined(c, M_BIND, y, CW, rowh, col, t)
        y -= rowh + GAP
    bottom_strip(c, "Nächste Woche / Mitnehmen")
    back(c)


def tagesplan(c):
    header(c, "Tagesplan", ["Datum", "Wochentag"])
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.8)
    c.roundRect(M_BIND, TOP - 30, CW, 30, 4, stroke=1, fill=0)
    rating(c, M_BIND + 8, TOP - 16, "Befinden (1 schlecht, 5 gut)", CW / 2)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 7)
    x2 = M_BIND + CW / 2 + 10
    c.drawString(x2, TOP - 12, "Schlaf (Std.)")
    c.setStrokeColor(LINE)
    c.line(x2 + 48, TOP - 14, x2 + 90, TOP - 14)
    colw = (CW - GAP) / 2
    y = TOP - 30 - GAP
    th = 215
    box(c, M_BIND, y, colw, th, BLUE, "Termine", outline=True, dotted=False, lines=False)
    yy, stunde = y - 34, 8
    c.setFont("Helvetica", 7)
    while yy > y - th + 6:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(M_BIND + 22, yy, M_BIND + colw - 6, yy)
        c.setFillColor(GREY)
        c.drawString(M_BIND + 7, yy + 3, str(stunde))
        yy -= 18
        stunde += 1
    box(c, M_BIND + colw + GAP, y, colw, 108, ORANGE, "Top 3 heute", outline=True, dotted=False,
        numbered=True, step=26)
    box(c, M_BIND + colw + GAP, y - 108 - GAP, colw, th - 108 - GAP, TEAL, "Notizen", outline=True)
    y -= th + GAP
    todo(c, y, y - (24 + 22 + GAP) , title="To-dos", step=21)
    bottom_strip(c, "Morgen / Mitnehmen")
    back(c)


def todoliste(c):
    header(c, "To-do-Liste", ["Bereich / Thema", "Datum"])
    todo(c, TOP, TOP - 24, step=24)
    back(c)


def konferenz(c):
    header(c, "Konferenz / Sitzung", ["Gremium / Thema", "Datum", "Uhrzeit", "Ort"])
    colw = (CW - GAP) / 2
    lined(c, M_BIND, TOP, colw, 130, BLUE, "Tagesordnung", numbered=True)
    box(c, M_BIND + colw + GAP, TOP, colw, 130, TEAL, "Anwesend / entschuldigt", outline=True)
    y = TOP - 130 - GAP
    box(c, M_BIND, y, CW, 150, GREY, "Notizen", outline=True)
    y -= 150 + GAP
    lined(c, M_BIND, y, CW, 70, BLUE, "Beschlüsse")
    y -= 70 + GAP
    todo(c, y, y - (24 + 22 + GAP), title="To-dos", step=22)
    bottom_strip(c, "Nächster Termin / offen")
    back(c)


def gespraech(c):
    header(c, "Gespräch zu zweit", ["Mit", "Datum", "Uhrzeit", "Anlass"])
    colw = (CW - GAP) / 2
    lined(c, M_BIND, TOP, colw, 105, BLUE, "Themen")
    box(c, M_BIND + colw + GAP, TOP, colw, 105, TEAL, "Meine Fragen / Vorbereitung", outline=True)
    y = TOP - 105 - GAP
    box(c, M_BIND, y, CW, 175, GREY, "Notizen", outline=True)
    y -= 175 + GAP
    todo(c, y, y - (24 + 22 + GAP), title="Vereinbarungen / To-dos", step=22)
    bottom_strip(c, "Nächstes Gespräch / Wiedervorlage")
    back(c)


def mentoring(c):
    header(c, "Mentoring-Gespräch", ["Name", "Klasse", "Datum", "Uhrzeit"])
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.8)
    c.roundRect(M_BIND, TOP - 32, CW, 32, 4, stroke=1, fill=0)
    third = CW / 3
    rating(c, M_BIND + 6, TOP - 14, "Wohlfühlen", third)
    rating(c, M_BIND + third + 6, TOP - 14, "Lernen / Leistung", third)
    rating(c, M_BIND + 2 * third + 6, TOP - 14, "Klassengemeinschaft", third)
    colw = (CW - GAP) / 2
    row_h = 74
    cells = [("Wie geht es dir in Klasse und Schule?", BLUE),
             ("Lernen: Was läuft, wo hakt es?", TEAL),
             ("Arbeitsweise: HA, Heft, Material", TEAL),
             ("Klasse: mit wem, was stört", BLUE),
             ("Ziele bis zum Halbjahr", BLUE),
             ("Was brauchst du von uns?", TEAL)]
    y = TOP - 32 - GAP
    for i, (t, col) in enumerate(cells):
        r, k = divmod(i, 2)
        box(c, M_BIND + k * (colw + GAP), y - r * (row_h + GAP), colw, row_h, col, t,
            outline=True)
    y -= 3 * (row_h + GAP)
    todo(c, y, 104, title="Vereinbarungen", step=22)
    y -= 104 + GAP
    box(c, M_BIND, y, CW, y - (24 + 22 + GAP), BLUE, "Sonstiges / Rückmeldung an mich", outline=True)
    bottom_strip(c, "Nächstes Gespräch")
    back(c)


def projekt(c):
    header(c, "Projektseite", ["Projekt", "Start", "Ende"])
    lined(c, M_BIND, TOP, CW, 62, PURPLE, "Ziel")
    y = TOP - 62 - GAP
    lined(c, M_BIND, y, CW, 128, BLUE, "Schritte / Meilensteine", numbered=True)
    y -= 128 + GAP
    lined(c, M_BIND, y, CW, 84, TEAL, "Beteiligte / Absprachen")
    y -= 84 + GAP
    todo(c, y, 112, title="Nächste Schritte", step=22)
    y -= 112 + GAP
    box(c, M_BIND, y, CW, y - (24 + 22 + GAP), GREY, "Notizen", outline=True)
    bottom_strip(c, "Nächster Check")
    back(c)


def notizseite(c):
    header(c, "Notizen", ["Thema", "Datum"])
    dots(c, M_BIND, 24, CW, H - 100)
    c.showPage()
    dots(c, M_OUT, 24, CW, H - 48)
    c.showPage()


def bauen(path):
    c = canvas.Canvas(path, pagesize=A5)
    deckblatt(c)
    inhalt(c)
    sheets = {0: [wochenplan, tagesplan, todoliste], 1: [konferenz], 2: [gespraech],
              3: [mentoring], 4: [projekt], 5: [notizseite]}
    for i in range(len(REGISTER)):
        trennblatt(c, i)
        for f in sheets[i]:
            f(c)
    c.setTitle("Planer A5 – Druckset")
    c.save()


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "04 Ressourcen", "Planer")
    p = os.path.join(out, "Planer – Druckset A5.pdf")
    bauen(p)
    print("fertig:", os.path.abspath(p))
