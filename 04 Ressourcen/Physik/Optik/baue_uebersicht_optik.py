#!/usr/bin/env python3
"""Übersicht aller Optik-Stunden Klasse 7c: links die Doppelstunden, rechts die gewählte Stunde. Ändert an den Stunden nichts.
Termine nur, wo sie in den Stunden selbst stehen. Noch nicht vorbereitete Themen aus dem Stoffverteilungsplan sind ausgegraut.
Aufruf: python3 baue_uebersicht_optik.py  -> Optik Klasse 7 – Übersicht.html"""
import re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
from uebersicht_vorlage import baue_uebersicht  # noqa: E402


def e(eid, marke, titel, datei="", art=""):
    sub, datum = "", ""
    if datei:
        s = (HIER / datei).read_text(encoding="utf-8")
        m = re.search(r'<p class="sub">([^<]*)', s)
        sub = m.group(1) if m else ""
        d = re.search(r"(Do \d\d\.\d\d\.\d{4})", sub)
        datum = ("voraussichtlich " if "voraussichtlich" in sub else "") + d.group(1) if d else ""
    return {"id": eid, "marke": marke, "titel": titel, "sub": sub, "datum": datum, "datei": datei, "art": art}


optik1 = [
    e("F1", "F1", "Lichtquellen und beleuchtete Körper", "Optik 1 – Lichtquellen und beleuchtete Körper – ALLES.html"),
    e("F2", "F2", "Licht trifft auf einen Körper", "Optik – Do 24.09. – Stunde.html"),
    e("F3", "F3", "Lichtausbreitung und Blende", "Optik – Leitfrage 3 – Stunde.html"),
    e("F4", "F4", "Kern- und Halbschatten", "Optik – Leitfrage 4 – Stunde.html"),
    e("F5", "F5", "Mondphasen und Finsternisse", "Optik – Leitfrage 5 – Stunde.html"),
    e("LK", "LK", "Lochkamera und Rückblick Optik I", "Optik – Lochkamera – Stunde.html"),
]
optik2 = [
    e("F6a", "F6", "Das Reflexionsgesetz", "Optik II – Reflexionsgesetz – Stunde.html"),
    e("F6b", "F6", "Spiegelbild und Spiegelgröße", "Optik II – Spiegelbild – Stunde.html"),
    e("F7", "F7", "Lichtbrechung", "Optik II – Lichtbrechung – Stunde.html"),
    e("F8a", "F8", "Sammel- und Zerstreuungslinse", "Optik II – Linsen – Stunde.html"),
    e("F8b", "F8", "Bildentstehung an der Sammellinse, Lupe, Auge", art="offen"),
    e("F8c", "F8", "Kurz- und Weitsichtigkeit, Wiederholung Optik", art="offen"),
]
ka = [e("KA1", "KA", "Klassenarbeit 1: Optik I und II bis Linsen", art="offen")]
farben = [
    e("F9", "F9", "Farben: Prisma, Spektrum, Regenbogen", art="offen"),
    e("F9b", "F9", "Unsichtbares Licht, Farbaddition, Glasfaser", art="offen"),
]
for x in ka:
    x["art"] = "ka"

links = [("Optik-Labore (Startseite für IServ)", "Optik-Labore.html"), ("Foliensatz Optik I", "Optik I.html"), ("Foliensatz Optik II", "Optik II.html"),
         ("F2 alles in einer Datei", "Optik 2 – Licht trifft auf einen Körper – ALLES.html"), ("Schattenlabor", "Schattenlabor Halbschatten.html"), ("Übersicht Kernphysik Klasse 10", "../Kernphysik/Kernphysik Klasse 10 – Übersicht.html")]

baue_uebersicht(HIER / "Optik Klasse 7 – Übersicht.html", "Optik Klasse 7c", "Alle Doppelstunden Optik · 2026/27",
                [("Optik I", optik1), ("Optik II", optik2), ("Klassenarbeit", ka), ("Farben", farben)], links, "optik7-stunde")
