#!/usr/bin/env python3
"""Lösungsfassung von Oskars Blatt „Radioaktiver Zerfall“ (Zerfallsreihen Np-237 und Th-232): Die leeren Kreise, Kästchen
und Zerfallsarten werden in Magenta ausgefüllt, direkt auf seinem Layout. Werte wie in der Buchlösung (dort ist Np mit Z = 94
gedruckt, richtig ist 93, so steht es auch auf dem Blatt).
Aufruf: python3 baue_zerfallsreihen_loesung.py  -> Materialien/Zerfallsreihen W05 (Oskar).pdf (Seite 1 Aufgabe, Seite 2 Lösung)"""
from pathlib import Path
import fitz

HIER = Path(__file__).parent
QUELLE = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik/Physik Klasse 10/Kernphysik/3. Arten radioaktiver Strahlung/Zerfallsreihen Aufgabe.pdf"
ZIEL = HIER / "Materialien" / "Zerfallsreihen W05 (Oskar).pdf"
FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
MAG = (0.9, 0.0, 0.49)

NP = [("Np", 237, 93), ("Pa", 233, 91), ("U", 233, 92), ("Th", 229, 90), ("Ra", 225, 88), ("Ac", 225, 89), ("Fr", 221, 87),
      ("At", 217, 85), ("Bi", 213, 83), ("Po", 213, 84), ("Pb", 209, 82), ("Bi", 209, 83), ("Tl", 205, 81)]
TH = [("Th", 232, 90), ("Ra", 228, 88), ("Ac", 228, 89), ("Th", 228, 90), ("Ra", 224, 88), ("Rn", 220, 86), ("Po", 216, 84),
      ("Pb", 212, 82), ("Bi", 212, 83), ("Tl", 208, 81), ("Pb", 208, 82)]


def zerfall(a, b):
    return "α" if b[1] == a[1] - 4 else "β"


def main():
    doc = fitz.open(str(QUELLE))
    doc.insert_pdf(fitz.open(str(QUELLE)))
    p = doc[1]
    p.insert_font(fontname="tnr", fontfile=FONT)
    dr = p.get_drawings()
    kreise = [g["rect"] for g in dr if 32 <= round(g["rect"].width) <= 35 and abs(g["rect"].width - g["rect"].height) < 1.5]
    boxen = [g["rect"] for g in dr if round(g["rect"].width) == 22 and round(g["rect"].height) == 22]
    klein = [g["rect"] for g in dr if round(g["rect"].width) == 15 and round(g["rect"].height) == 15]
    einmal = lambda rs: list({(round(r.x0), round(r.y0)): r for r in rs}.values())   # doppelt gezeichnete Rahmen nur einmal
    kreise, boxen, klein = einmal(kreise), einmal(boxen), einmal(klein)
    worte = p.get_text("words")
    belegt = lambda r: any(r.contains(fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)) for w in worte)

    def schreibe(r, text, groesse):
        breite = fitz.get_text_length(text, fontname="tnr", fontfile=FONT, fontsize=groesse) if False else len(text) * groesse * 0.5
        p.insert_text((r.x0 + r.width / 2 - breite / 2, r.y0 + r.height / 2 + groesse * 0.35), text, fontname="tnr", fontsize=groesse, color=MAG)

    leer = 0
    for spalte, reihe in ((lambda r: r.x0 < 300, NP), (lambda r: r.x0 > 300, TH)):
        ks = sorted([k for k in kreise if spalte(k)], key=lambda r: r.y0)
        for i, k in enumerate(ks):
            if i >= len(reihe):
                leer += 1
                continue
            sym, a, z = reihe[i]
            if not belegt(k):
                schreibe(k, sym, 17)
            ky = (k.y0 + k.y1) / 2
            nah = [b for b in boxen if spalte(b) and b.x1 <= k.x0 + 2 and k.x0 - b.x1 < 40 and abs((b.y0 + b.y1) / 2 - ky) < 22]
            for b in nah:
                if not belegt(b):
                    schreibe(b, str(a if (b.y0 + b.y1) / 2 < ky else z), 12)
            if i + 1 < len(reihe):
                for s in klein:
                    if spalte(s) and k.y1 - 5 < s.y0 < k.y1 + 40 and not belegt(s):
                        schreibe(s, zerfall(reihe[i], reihe[i + 1]), 12)
    p.insert_text((430, 38), "LÖSUNG", fontname="tnr", fontsize=13, color=MAG)
    doc.save(str(ZIEL))
    print("geschrieben:", ZIEL.name, "| Kreise ohne Kern in der Th-Reihe:", leer)


if __name__ == "__main__":
    main()
