#!/usr/bin/env python3
"""Sammelt alle Versuchsfolien (Material, Aufbau, Durchführung) der Stunden in ein PDF je Fach für IServ:
Physik Klasse 7/Optik 2026-27/Versuche Optik (für IServ).pdf und Physik Klasse 10/Kernphysik 2026-27/Versuche Kernphysik (für IServ).pdf
Aufruf: python3 export_versuche.py   (nach dem Bauen der Stunden)"""
import re, subprocess
from pathlib import Path

HIER = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ICL = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik"
OPTIK = ["Optik – Do 24.09. – Stunde.html", "Optik – Leitfrage 3 – Stunde.html", "Optik – Leitfrage 4 – Stunde.html",
         "Optik – Leitfrage 5 – Stunde.html", "Optik – Lochkamera – Stunde.html"]
OPTIK += sorted(p.name for p in (HIER / "Optik").glob("Optik II – * – Stunde.html"))
KERN = sorted(p.name for p in (HIER / "Kernphysik").glob("Kernphysik – W*Stunde.html"))


def sammle(ordner, dateien):
    out = []
    for d in dateien:
        s = (ordner / d).read_text(encoding="utf-8")
        folien = s[s.index('id="t_folien"'):s.index('id="t_heft"')]
        out += re.findall(r'<section class="folie vbeschreibung[^"]*"[^>]*>.*?</section>', folien, re.S)
    return out


def drucke(folien, css, ziel, ordner):
    tmp = ordner / "_versuche.html"
    tmp.write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><link rel="stylesheet" href="folien.css">' + css +
                   "</head><body>" + "".join(folien) + "</body></html>", encoding="utf-8")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={ziel}", "--virtual-time-budget=5000", tmp.as_uri()],
                   check=True, capture_output=True)
    tmp.unlink()
    print(ziel.name, "|", len(folien), "Versuche")


if __name__ == "__main__":
    drucke(sammle(HIER / "Optik", OPTIK), "", ICL / "Physik Klasse 7/Optik 2026-27/Versuche Optik (für IServ).pdf", HIER / "Optik")
    kern = HIER / "Kernphysik"
    drucke(sammle(kern, KERN), "", ICL / "Physik Klasse 10/Kernphysik 2026-27/Versuche Kernphysik (für IServ).pdf", HIER / "Optik")
