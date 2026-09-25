#!/usr/bin/env python3
"""Eine Übersichtsseite für alle Kernphysik-Stunden Klasse 10: links die Wochen, rechts die gewählte Stunde (iframe).
Liest die Stundenliste aus baue_stunden_k10.py und baue_stunden_k10_teil2.py, ändert an den Stunden nichts.
Aufruf: python3 baue_uebersicht_k10.py  -> Kernphysik Klasse 10 – Übersicht.html"""
import re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
import baue_stunden_k10 as t1  # noqa: E402
import baue_stunden_k10_teil2 as t2  # noqa: E402

KA = "../Klassenarbeiten/Klassenarbeit Nr. 1 Klasse 10 Kernphysik 2026"

stunden = []
for datei, h1, sub, *_ in t1.STUNDEN:
    stunden.append({"datei": datei, "titel": h1.replace("Kernphysik: ", ""), "sub": sub})
for kurz, h1, sub, *_ in t2.STUNDEN:
    stunden.append({"datei": f"Kernphysik – {kurz} – Stunde.html", "titel": h1.replace("Kernphysik: ", ""), "sub": sub})
for s in stunden:
    s["w"] = re.search(r"W\d\d", s["sub"]).group(0)
    s["woche"] = re.search(r"Woche ab ([\d.]+)", s["sub"]).group(1)

extra = [
    {"w": "W10", "woche": "23.11.2026", "titel": "Klassenarbeit Nr. 1", "datei": KA + ".html", "sub": "Klassenarbeit · Atombau, Zerfall, Halbwertszeit", "art": "ka"},
    {"w": "W11", "woche": "30.11.2026", "titel": "Besprechung der Klassenarbeit", "datei": KA + " – Lösung.html", "sub": "Rückgabe · Lösung und Erwartungshorizont", "art": "ka"},
    {"w": "W14", "woche": "21.12.2026", "titel": "Puffer (verkürzte Woche)", "datei": "", "sub": "Nacharbeiten oder vorziehen", "art": "puffer"},
]
alle = sorted(stunden + extra, key=lambda s: s["w"])

GRUPPEN = [("Leitfrage 1 · Woraus besteht Materie?", "W01", "W03"), ("Leitfrage 2 · Warum zerfallen Kerne?", "W04", "W06"),
           ("Leitfrage 3 · Wie schnell zerfällt ein Stoff?", "W07", "W09"), ("Klassenarbeit", "W10", "W11"),
           ("Leitfrage 4 · Strahlung und Körper", "W12", "W15"), ("Leitfrage 5 · Energie aus dem Kern", "W16", "W19"),
           ("Leitfrage 6 · Nutzen und Risiko", "W20", "W21"), ("Rückblick", "W22", "W22")]

sys.path.insert(0, str(HIER.parent / "Optik"))
from uebersicht_vorlage import baue_uebersicht  # noqa: E402

gruppen = [(t, [{"id": s["w"], "marke": s["w"], "titel": s["titel"], "sub": s["sub"], "datum": "ab " + s["woche"],
                 "datei": s["datei"], "art": s.get("art", "")} for s in alle if a <= s["w"] <= b]) for t, a, b in GRUPPEN]
zusatz = [("Kernphysik-Labore (Startseite für IServ)", "Kernphysik-Labore.html"), ("Foliensatz Kernphysik (alle Folien)", "Kernphysik.html"),
          ("Begleitheft Kernspaltung (PDF)", "Materialien/Begleitheft Kernspaltung.pdf"), ("Klassenarbeit Nr. 1", KA + ".html"),
          ("Was muss ich wissen? (KA 1)", KA + " – Was muss ich wissen.html"), ("Übersicht Optik Klasse 7", "../Optik/Optik Klasse 7 – Übersicht.html")]
baue_uebersicht(HIER / "Kernphysik Klasse 10 – Übersicht.html", "Kernphysik Klasse 10", "Alle Stunden W01 bis W22 · 2026/27", gruppen, zusatz, "k10-woche")
