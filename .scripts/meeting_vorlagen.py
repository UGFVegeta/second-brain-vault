#!/usr/bin/env python3
"""Baut die Notiz-Vorlagen (A4, Vorder- und Rückseite) für Notability und Druck.

Aufruf: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/meeting_vorlagen.py
Ausgabe: 04 Ressourcen/Meeting-Vorlagen/*.pdf
Die Vorlagen sind leer: keine Namen, keine Daten.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas

W, H = A4
LM, RM = 58, 30          # links Rand für die Lochung
CW = W - LM - RM
GAP = 8

BLUE = HexColor("#6E86B5")
TEAL = HexColor("#2AA0A8")
ORANGE = HexColor("#E98A52")
GREY = HexColor("#7A8190")
DOT = HexColor("#C5CBD6")
LINE = HexColor("#C9D0DC")


def tint(col, a=0.14):
    return Color(1 - (1 - col.red) * a, 1 - (1 - col.green) * a, 1 - (1 - col.blue) * a)


def dots(c, x, y, w, h, step=14.17):
    c.setFillColor(DOT)
    yy = y + h - step / 2
    while yy > y:
        xx = x + step / 2
        while xx < x + w:
            c.circle(xx, yy, 0.55, stroke=0, fill=1)
            xx += step
        yy -= step


INK = HexColor("#2E3440")


def header(c, kind, fields, values=None):
    values = values or {}
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(LM, H - 52, "NOTIZEN")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(LM + 100, H - 52, kind)
    # Felder rechts
    fx = LM + 255
    fw = W - RM - fx
    n = len(fields)
    y = H - 36
    per_row = 2 if n > 2 else 1
    colw = (fw - (per_row - 1) * 10) / per_row
    for i, f in enumerate(fields):
        col, row = i % per_row, i // per_row
        x = fx + col * (colw + 10)
        yy = y - row * 17
        c.setFillColor(GREY)
        c.setFont("Helvetica", 6.5)
        c.drawString(x, yy + 2, f)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        lx = x + c.stringWidth(f, "Helvetica", 6.5) + 3
        c.line(lx, yy, x + colw, yy)
        if values.get(f):
            c.setFillColor(INK)
            size = 8.5
            while size > 6 and c.stringWidth(values[f], "Helvetica", size) > x + colw - lx - 4:
                size -= 0.5
            c.setFont("Helvetica", size)
            c.drawString(lx + 2, yy + 2, values[f])


def frame(c, x, ytop, w, h, col, outline):
    """Getönte Fläche mit Kopflinie, oder (outline) nur farbiger Rahmen auf Weiß."""
    if outline:
        c.setStrokeColor(col)
        c.setLineWidth(0.8)
        c.roundRect(x, ytop - h, w, h, 4, stroke=1, fill=0)
        return
    c.setFillColor(tint(col))
    c.rect(x, ytop - h, w, h, stroke=0, fill=1)
    c.setStrokeColor(col)
    c.setLineWidth(1.1)
    c.line(x, ytop, x + w, ytop)


def box(c, x, ytop, w, h, col, title, lines=True, step=15, numbered=False,
        outline=False, entries=None, dotted=None):
    """dotted: Dots statt Linien; Standard im Rahmen-Stil ja, sonst nein."""
    frame(c, x, ytop, w, h, col, outline)
    c.setFillColor(col)
    c.circle(x + 12, ytop - 13, 5.5, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFFFFF"))
    c.circle(x + 12, ytop - 13, 2, stroke=0, fill=1)
    c.setFillColor(col)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 22, ytop - 16, title)
    if outline if dotted is None else dotted:
        dots(c, x + 3, ytop - h + 3, w - 6, h - 28)
    elif lines:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        yy = ytop - 32
        k = 1
        while yy > ytop - h + 4:
            c.setStrokeColor(LINE)
            c.line(x + (16 if numbered else 8), yy, x + w - 8, yy)
            if numbered:
                c.setFillColor(col)
                c.setFont("Helvetica-Bold", 6.5)
                c.drawString(x + 8, yy + 3, str(k))
            if entries and k <= len(entries):
                c.setFillColor(INK)
                c.setFont("Helvetica", 8.5)
                c.drawString(x + (20 if numbered else 10), yy + 3, entries[k - 1])
            yy -= step
            k += 1


def todo(c, ytop, h, col=ORANGE, title="To-dos", who="Wer?", when="Bis wann?", outline=False):
    x, w = LM, CW
    frame(c, x, ytop, w, h, col, outline)
    c.setFillColor(col)
    c.circle(x + 12, ytop - 13, 5.5, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFFFFF"))
    c.circle(x + 12, ytop - 13, 2, stroke=0, fill=1)
    c.setFillColor(col)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 22, ytop - 16, title)
    c1 = x + w * 0.50
    c2 = x + w * 0.74
    c3 = x + w * 0.90
    c.setFont("Helvetica", 6.5)
    c.drawString(c1 + 4, ytop - 16, who)
    c.drawString(c2 + 4, ytop - 16, when)
    c.drawString(c3 + 2, ytop - 16, "erledigt")
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    yy = ytop - 32
    while yy > ytop - h + 6:
        c.line(x + 8, yy, c1 - 4, yy)
        c.line(c1 + 4, yy, c2 - 4, yy)
        c.line(c2 + 4, yy, c3 - 4, yy)
        c.setStrokeColor(col)
        c.circle(c3 + 18, yy + 4, 4.2, stroke=1, fill=0)
        c.setStrokeColor(LINE)
        yy -= 17


def strip(c, ytop, h, label, outline=False, value=None):
    """Zeile mit Beschriftung und Schreiblinie."""
    if outline:
        c.setStrokeColor(BLUE)
        c.setLineWidth(0.8)
        c.roundRect(LM, ytop - h, CW, h, 4, stroke=1, fill=0)
    else:
        c.setFillColor(tint(BLUE))
        c.rect(LM, ytop - h, CW, h, stroke=0, fill=1)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(LM + 8, ytop - h + h / 2 - 2.5, label)
    lx = LM + 8 + c.stringWidth(label, "Helvetica-Bold", 7.5) + 6
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(lx, ytop - h + 7, LM + CW - 8, ytop - h + 7)
    if value:
        c.setFillColor(INK)
        c.setFont("Helvetica", 8.5)
        c.drawString(lx + 2, ytop - h + 9, value)


def back(c):
    c.showPage()
    dots(c, LM, 30, CW, H - 60)


def konferenz(path, fill=None, outline=False):
    fill = fill or {}
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Notizen Konferenz")
    header(c, "Konferenz / Sitzung", ["Gremium / Thema", "Datum", "Uhrzeit", "Ort", "Leitung", "Protokoll"],
           {"Gremium / Thema": fill.get("thema"), "Datum": fill.get("datum"),
            "Uhrzeit": fill.get("uhrzeit"), "Ort": fill.get("ort")})
    colw = (CW - GAP) / 2
    top = H - 84
    box(c, LM, top, colw, 160, BLUE, "Tagesordnung", numbered=True, entries=fill.get("tops"),
        outline=outline, dotted=False)
    box(c, LM + colw + GAP, top, colw, 160, TEAL, "Anwesend / entschuldigt", outline=outline)
    notes(c, 284, top - 160 - 8, outline)
    box(c, LM, 276, CW, 80, BLUE, "Beschlüsse", outline=outline, dotted=False)
    todo(c, 190, 130, outline=outline)
    strip(c, 54, 24, "Nächster Termin / offen fürs nächste Mal", outline=outline, value=fill.get("naechster"))
    back(c)
    c.save()


def notes(c, bottom, top, outline):
    """Freie Notizfläche: im Rahmen-Stil mit Rahmen, sonst nur Dots."""
    if outline:
        box(c, LM, top, CW, top - bottom, GREY, "Notizen", outline=True)
    else:
        dots(c, LM, bottom, CW, top - bottom)


def zweiergespraech(path, fill=None, outline=False):
    fill = fill or {}
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Notizen Gespräch")
    header(c, "Gespräch zu zweit", ["Mit", "Datum", "Uhrzeit", "Anlass"],
           {"Mit": fill.get("mit"), "Datum": fill.get("datum"),
            "Uhrzeit": fill.get("uhrzeit"), "Anlass": fill.get("thema")})
    colw = (CW - GAP) / 2
    top = H - 84
    box(c, LM, top, colw, 125, BLUE, "Themen", entries=fill.get("tops"), outline=outline, dotted=False)
    box(c, LM + colw + GAP, top, colw, 125, TEAL, "Meine Fragen / Vorbereitung", outline=outline)
    notes(c, 198, top - 125 - 8, outline)
    todo(c, 190, 130, title="Vereinbarungen / To-dos", outline=outline)
    strip(c, 54, 24, "Nächstes Gespräch / Wiedervorlage", outline=outline)
    back(c)
    c.save()


def rating(c, x, y, label, w):
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x, y + 8, label)
    cx = x
    for i in range(1, 6):
        c.setStrokeColor(BLUE)
        c.setLineWidth(0.7)
        c.setFillColor(HexColor("#FFFFFF"))
        c.circle(cx + 7 + (i - 1) * 17, y - 5, 6, stroke=1, fill=1)
        c.setFillColor(GREY)
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(cx + 7 + (i - 1) * 17, y - 7.2, str(i))


def mentoring(path, outline=False):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Notizen Mentoring-Gespräch")
    header(c, "Mentoring-Gespräch", ["Name", "Klasse", "Datum", "Uhrzeit"])
    # Skala
    top = H - 84
    if outline:
        c.setStrokeColor(BLUE)
        c.setLineWidth(0.8)
        c.roundRect(LM, top - 34, CW, 34, 4, stroke=1, fill=0)
    else:
        c.setFillColor(tint(BLUE))
        c.rect(LM, top - 34, CW, 34, stroke=0, fill=1)
    third = CW / 3
    rating(c, LM + 8, top - 15, "Wohlfühlen (1 gut, 5 schlecht)", third)
    rating(c, LM + third + 8, top - 15, "Lernen / Leistung", third)
    rating(c, LM + 2 * third + 8, top - 15, "Klassengemeinschaft", third)
    colw = (CW - GAP) / 2
    row_h, gap = 98, 6
    y = top - 34 - gap
    cells = [
        ("Wie geht es dir in der Klasse und in der Schule?", BLUE),
        ("Lernen: Was läuft gut? Wo hakt es?", TEAL),
        ("Arbeitsweise: Hausaufgaben, Heft, Material, Zeit", TEAL),
        ("Klassengemeinschaft: mit wem, was stört", BLUE),
        ("Ziele bis zum Halbjahr", BLUE),
        ("Was brauchst du von mir und von den Lehrkräften?", TEAL),
    ]
    for i, (t, col) in enumerate(cells):
        r, k = divmod(i, 2)
        box(c, LM + k * (colw + GAP), y - r * (row_h + gap), colw, row_h, col, t,
            step=14.5, outline=outline)
    y = y - 3 * (row_h + gap)
    todo(c, y, 112, title="Vereinbarungen", who="Wer?", when="Bis wann?", outline=outline)
    y -= 118
    box(c, LM, y, CW, y - 60, BLUE, "Sonstiges / Rückmeldung an mich", outline=outline)
    strip(c, 54, 24, "Nächstes Gespräch", outline=outline)
    back(c)
    c.save()


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Ohne Argumente: leere Vorlagen bauen. "
                                "Mit 'konferenz' oder 'gespraech': vorausgefüllte Kopie.")
    p.add_argument("art", nargs="?", choices=["konferenz", "gespraech"])
    p.add_argument("--thema")
    p.add_argument("--datum")
    p.add_argument("--uhrzeit")
    p.add_argument("--ort")
    p.add_argument("--mit")
    p.add_argument("--naechster")
    p.add_argument("--top", action="append", dest="tops", help="mehrfach angeben, in Reihenfolge")
    p.add_argument("--rahmen", action="store_true", help="Rahmen-Variante statt getönter Flächen")
    a = p.parse_args()

    out = os.path.join(os.path.dirname(__file__), "..", "04 Ressourcen", "Meeting-Vorlagen")
    os.makedirs(out, exist_ok=True)
    if a.art:
        fill = {k: v for k, v in vars(a).items() if v and k not in ("art", "rahmen")}
        filled = os.path.join(out, "Ausgefüllt")
        os.makedirs(filled, exist_ok=True)
        name = " ".join(x for x in [a.datum, a.thema or a.art.capitalize()] if x).replace("/", "-")
        path = os.path.join(filled, name + ".pdf")
        (konferenz if a.art == "konferenz" else zweiergespraech)(path, fill, outline=a.rahmen)
        print("fertig:", os.path.abspath(path))
    else:
        for suffix, o in [("", False), (" – Rahmen", True)]:
            konferenz(os.path.join(out, f"Notizen Konferenz{suffix}.pdf"), outline=o)
            zweiergespraech(os.path.join(out, f"Notizen Gespräch zu zweit{suffix}.pdf"), outline=o)
            mentoring(os.path.join(out, f"Notizen Mentoring-Gespräch{suffix}.pdf"), outline=o)
        print("fertig:", os.path.abspath(out))
