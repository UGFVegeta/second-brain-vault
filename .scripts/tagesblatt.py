#!/usr/bin/env python3
"""Tagesblatt für die Planer-Mappe: Heute (Termine, To-dos) und Morgen.

Aufruf:
  /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/tagesblatt.py [--datum 2026-11-02] [--demo]
Ausgabe: ~/Documents/Tagesblatt/Tagesblatt <Datum>.pdf (außerhalb des Vaults; To-dos enthalten Namen)

Quellen (nur lesend, lokal):
  Kalender:   Arbeit, Schule, Jahresterminplanung / DieWo (Privat, Familie, Sport bleiben draußen)
  To-dos:     Erinnerungen, Liste "Schule", nicht erledigt; fällig bis zum Tag oder ohne Datum
--demo nimmt erfundene Beispiel-To-dos und schreibt nach 04 Ressourcen/Planer/ (ohne Namen).
"""
import argparse
import os
import subprocess
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

from meeting_vorlagen import (BLUE, CW, GREY, INK, LINE, LM, ORANGE, RM, TEAL, H, W, box,
                              dots, tint)

HERE = os.path.dirname(os.path.abspath(__file__))
ARBEITS_KALENDER = {"Arbeit", "Schule", "Jahresterminplanung / DieWo"}
TODO_LISTE = "Schule"
STIL = "linien"   # oder "dots"
TAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September",
          "Oktober", "November", "Dezember"]

KAL = '''
set out to ""
set d0 to current date
set year of d0 to {y}
set month of d0 to {m}
set day of d0 to {d}
set time of d0 to 0
set d1 to d0 + (5 * days)
tell application "Calendar"
  repeat with calName in {{"Arbeit", "Schule", "Jahresterminplanung / DieWo"}}
    try
      set cal to calendar calName
      set evs to (every event of cal whose start date ≥ d0 and start date < d1)
      repeat with ev in evs
        set sd to start date of ev
        set ed to end date of ev
        set out to out & calName & tab & (year of sd) & "-" & (month of sd as integer) & "-" & (day of sd) & tab & (hours of sd) & ":" & (minutes of sd) & tab & (hours of ed) & ":" & (minutes of ed) & tab & (allday event of ev) & tab & (summary of ev) & linefeed
      end repeat
    end try
  end repeat
end tell
return out
'''

REM = '''
set out to ""
tell application "Reminders"
  tell list "{liste}"
    set rs to (reminders whose completed is false)
    repeat with r in rs
      set dd to due date of r
      set d to ""
      if dd is not missing value then
        set d to (year of dd as string) & "-" & text -2 thru -1 of ("0" & ((month of dd) as integer)) & "-" & text -2 thru -1 of ("0" & (day of dd))
      end if
      set out to out & d & tab & (name of r) & linefeed
    end repeat
  end tell
end tell
return out
'''


def hm(s):
    h, m = s.split(":")
    return f"{int(h):02d}:{int(m):02d}"


def kalender(tag):
    r = subprocess.run(["osascript", "-e", KAL.format(y=tag.year, m=tag.month, d=tag.day)],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    out = {}
    for line in r.stdout.splitlines():
        p = line.split("\t")
        if len(p) != 6 or p[0] not in ARBEITS_KALENDER:
            continue
        _, d, s, e, allday, t = p
        y, mo, dy = (int(x) for x in d.split("-"))
        out.setdefault(date(y, mo, dy), []).append(
            {"s": "ganztägig" if allday == "true" else hm(s), "e": hm(e), "t": t.strip(),
             "allday": allday == "true"})
    return out


def naechster_arbeitstag(tag):
    """Morgen-Spalte: am Freitag und Samstag der Montag, sonst der Folgetag."""
    n = tag + timedelta(days=1)
    while n.weekday() >= 5:
        n += timedelta(days=1)
    return n


def todos(tag):
    r = subprocess.run(["osascript", "-e", REM.format(liste=TODO_LISTE)],
                       capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    heute, morgen = [], []
    morgen_tag = naechster_arbeitstag(tag).isoformat()
    for line in r.stdout.splitlines():
        due, _, name = line.partition("\t")
        if not name.strip():
            continue
        if not due or due <= tag.isoformat():
            heute.append((due, name.strip()))
        elif due == morgen_tag:
            morgen.append((due, name.strip()))
    return [n for _, n in sorted(heute)], [n for _, n in sorted(morgen)]


DEMO_HEUTE = [
    "Vertretungsregelung für die Woche mit der Schulleitung klären",
    "Rückmeldung zur Streitschlichterausbildung an die Schulsozialarbeit",
    "Rücklauf Elternbrief Klassenpflegschaft mit dem Sekretariat prüfen",
    "Raum und Technik für die GLK am Donnerstag mit dem Hausmeister absprechen",
    "Fortbildungsanträge der Kollegen sammeln und ans Sekretariat geben",
]
DEMO_MORGEN = ["Stundenplanänderung bis 12 Uhr an die Kollegen schicken"]


def tagesliste(tag, kal):
    termine = kal.get(tag, [])
    ganz = [t for t in termine if t["allday"]]
    zeit = [t for t in termine if not t["allday"]]
    return ganz + sorted(zeit, key=lambda x: x["s"])


def zeile_zu_termin(text):
    """'14:30 Gespräch mit Herrn X' -> Termin; ohne Uhrzeit ganztägig."""
    text = " ".join(text.split())
    p = text.split(" ", 1)
    if len(p) == 2 and ":" in p[0] and p[0].replace(":", "").isdigit():
        return {"s": hm(p[0]), "e": hm(p[0]), "t": p[1], "allday": False}
    return {"s": "ganztägig", "e": "", "t": text, "allday": True}


def erzeugen(tag, kal, heute_todos, morgen_todos, extra_termine=(), extra_todos=(), pfad=None):
    """Baut das Blatt mit Ergänzungen aus dem Dashboard. Gibt den Pfad zurück."""
    kal = {k: list(v) for k, v in kal.items()}
    for z in extra_termine:
        if z.strip():
            kal.setdefault(tag, []).append(zeile_zu_termin(z))
    ht = list(heute_todos) + [z.strip() for z in extra_todos if z.strip()]
    if pfad is None:
        out = os.path.expanduser("~/Documents/Tagesblatt")
        os.makedirs(out, exist_ok=True)
        pfad = os.path.join(out, f"Tagesblatt {tag.isoformat()}.pdf")
    blatt(pfad, tag, kal, ht, morgen_todos, "linien")
    return pfad


def titel(tag):
    return f"{TAGE[tag.weekday()]}, {tag.day}. {MONATE[tag.month - 1]} {tag.year}"


def linie(c, x1, y, x2, y2=None):
    if STIL == "linien":
        c.line(x1, y, x2, y if y2 is None else y2)


def fit(c, text, font, size, maxw):
    while size > 6 and c.stringWidth(text, font, size) > maxw:
        size -= 0.5
    return size


def kopf(c, x, ytop, w, h, col, title, rechts=None):
    box(c, x, ytop, w, h, col, title, outline=True, dotted=(STIL == "dots"), lines=False)
    if rechts:
        c.setFillColor(col)
        c.setFont("Helvetica", 6.5)
        c.drawRightString(x + w - 8, ytop - 16, rechts)


def terminbox(c, x, ytop, w, h, col, title, items, size=11.5, step=22, min_step=17):
    kopf(c, x, ytop, w, h, col, title)
    kap = int((h - 34) // step)
    if len(items) > kap:
        step = max(min_step, (h - 34) / len(items))
        size = max(9.5, size - 1.5)
    yy = ytop - 18 - step
    tw = 42 if size > 10.5 else 38
    while yy > ytop - h + 4:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        linie(c, x + 8, yy, x + w - 8, yy)
        yy -= step
    yy = ytop - 18 - step
    for it in items:
        if yy < ytop - h + 4:
            break
        ganz = it["s"] == "ganztägig"
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", size - 2)
        c.drawString(x + 10, yy + 4.5, "ganztägig" if ganz else it["s"])
        tx = x + 10 + (tw + 22 if ganz else tw)
        c.setFillColor(INK)
        s = fit(c, it["t"], "Helvetica", size, x + w - 10 - tx)
        c.setFont("Helvetica", s)
        c.drawString(tx, yy + 4.5, it["t"])
        yy -= step


def todobox(c, x, ytop, w, h, col, title, items, size=11, line=20, wann=True):
    kopf(c, x, ytop, w, h, col, title, rechts=None)
    textw = w - 42 - (66 if wann else 8)
    if wann:
        c.setFillColor(col)
        c.setFont("Helvetica", 6.5)
        c.drawString(x + w - 62, ytop - 15, "wann?")
    slot = 2 * line + 6
    slots = int((h - 26) // slot)
    rest = len(items) - slots
    yy = ytop - 24
    for i in range(slots):
        y1 = yy - line
        y2 = y1 - line
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        linie(c, x + 26, y1, x + 26 + textw + 6, y1)
        linie(c, x + 26, y2, x + 26 + textw + 6, y2)
        if wann:
            linie(c, x + w - 62, y2, x + w - 8, y2)
        c.setStrokeColor(col)
        c.circle(x + 14, y1 + 5.5, 5, stroke=1, fill=0)
        if i < len(items):
            text = items[i]
            if i == slots - 1 and rest > 0:
                text = f"{items[i]}  (+ {rest} weitere in Erinnerungen)"
            zeilen = simpleSplit(text, "Helvetica", size, textw)[:2]
            c.setFillColor(INK)
            c.setFont("Helvetica", size)
            for k, z in enumerate(zeilen):
                c.drawString(x + 30, (y1, y2)[k] + 5, z)
        yy = y2 - 6


def blatt(path, tag, kal, heute_todos, morgen_todos, stil="linien"):
    global STIL
    STIL = stil
    morgen = naechster_arbeitstag(tag)
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(f"Tagesblatt {tag.isoformat()}")
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(LM, H - 50, "HEUTE")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Oblique", 14)
    c.drawString(LM + 86, H - 50, titel(tag))
    top = H - 68
    th = 150
    terminbox(c, LM, top, CW, th, BLUE, "Termine", tagesliste(tag, kal))
    y = top - th - 6
    dh = 256
    todobox(c, LM, y, CW, dh, ORANGE, "To-dos (Arbeit)", heute_todos)
    y -= dh + 8
    c.setFillColor(GREY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(LM, y - 13, "MORGEN")
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawString(LM + 70, y - 13, titel(morgen))
    y -= 20
    colw = (CW - 8) / 2
    mh = 150
    terminbox(c, LM, y, colw, mh, TEAL, "Termine", tagesliste(morgen, kal),
              size=10.5, step=20, min_step=16)
    todobox(c, LM + colw + 8, y, colw, mh, ORANGE, "To-dos", morgen_todos, size=10, line=17, wann=False)
    y -= mh + 6
    # Eingang
    eh = y - 28
    kopf(c, LM, y, CW, eh, GREY, "Eingang: Neues, Termine, Aufgaben (Wer? Wann?)", rechts="übertragen")
    yy = y - 18 - 21
    while yy > y - eh + 4:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        linie(c, LM + 8, yy, LM + CW - 40, yy)
        c.setStrokeColor(GREY)
        c.circle(LM + CW - 20, yy + 5, 4.5, stroke=1, fill=0)
        yy -= 21
    c.showPage()

    # Rückseite (Heftrand rechts, deshalb nach links gerückt): immer Dots, dazu ein Skizzenfeld
    STIL = "dots"
    bx = RM
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(bx, H - 46, "ABSCHLUSS UND OFFENES")
    top = H - 62
    kopf(c, bx, top, CW, 84, TEAL, "Feierabend: Was bleibt offen? Nächster Schritt und wann?")
    yy = top - 18 - 22
    while yy > top - 84 + 4:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        linie(c, bx + 8, yy, bx + CW - 8, yy)
        yy -= 22
    y = top - 84 - 8
    wh = 150
    kopf(c, bx, y, CW, wh, ORANGE, "Warte auf (Wer? Worauf? Seit wann? Nachfassen am)")
    yy = y - 18 - 22
    while yy > y - wh + 4:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        linie(c, bx + 8, yy, bx + CW - 8, yy)
        yy -= 22
    y -= wh + 8
    box(c, bx, y, CW, y - 30, GREY, "Skizze und Notizen: Zeichnung, Ablauf, Gesprächsplan", outline=True, dotted=True)
    c.showPage()
    c.save()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--datum", help="JJJJ-MM-TT, Standard: heute")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--stil", choices=["linien", "dots"], default="linien")
    a = ap.parse_args()
    tag = datetime.strptime(a.datum, "%Y-%m-%d").date() if a.datum else date.today()
    kal = kalender(tag)
    if a.demo:
        ht, mt = DEMO_HEUTE, DEMO_MORGEN
        out = os.path.join(HERE, "..", "04 Ressourcen", "Planer")
        name = f"Beispiel Tagesblatt {tag.isoformat()} {a.stil}.pdf"
    else:
        ht, mt = todos(tag)
        out = os.path.expanduser("~/Documents/Tagesblatt")
        name = f"Tagesblatt {tag.isoformat()}.pdf"
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, name)
    blatt(p, tag, kal, ht, mt, a.stil)
    print("fertig:", os.path.abspath(p))
