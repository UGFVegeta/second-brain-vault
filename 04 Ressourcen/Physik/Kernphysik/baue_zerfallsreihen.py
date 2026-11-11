#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Oskars Blatt „Radioaktiver Zerfall“ (Zerfallsreihen Np-237 und Th-232), umgebaut am 11.11.2026.

Aufgabe 2 braucht den langen Erklärtext nicht mehr. Die rechte Spalte ist jetzt aufgebaut wie die linke:
  - steht die Zerfallsart am Pfeil, berechnen die Schüler das neue Element,
  - ist das nächste Element schon gegeben, bestimmen sie die Zerfallsart (Kästchen am Pfeil).
Der überzählige zwölfte Kreis rechts fällt weg (die Reihe Th-232 bis Pb-208 hat 11 Kerne).
Dazu: Schwierigkeitskreise (Aufgabe 1 ○, Aufgabe 2 ◐) mit Legende, „Thalium“ korrigiert zu „Thallium“.
Schrift: Oskars eingebettete Minion Pro, damit alles aussieht wie das Original. Lösung in Magenta auf demselben Blatt.

Das Original in iCloud bleibt unverändert, es wird nur gelesen.
Aufruf: python3 baue_zerfallsreihen.py
  -> Materialien/Zerfallsreihen (Oskar).pdf            (Seite 1 Aufgabe, Seite 2 Lösung, für die Stunden-HTML)
  -> Materialien/Zerfallsreihen (Oskar) – Aufgabe.pdf  und  … – Lösung.pdf  (einzeln, für iCloud)"""
from pathlib import Path
import fitz

HIER = Path(__file__).parent
MAT = HIER / "Materialien"
QUELLE = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik/Physik Klasse 10/Kernphysik/3. Arten radioaktiver Strahlung/Zerfallsreihen Aufgabe.pdf"
ZIEL = MAT / "Zerfallsreihen (Oskar).pdf"
ZIEL_A = MAT / "Zerfallsreihen (Oskar) – Aufgabe.pdf"
ZIEL_L = MAT / "Zerfallsreihen (Oskar) – Lösung.pdf"

SCHWARZ = (0.137, 0.122, 0.125)          # Farbe des Originals (#231F20)
GRAU = (0.38, 0.38, 0.42)
MAG = (0.9, 0.0, 0.49)

PS = {"Au": 79, "Hg": 80, "Tl": 81, "Pb": 82, "Bi": 83, "Po": 84, "At": 85, "Rn": 86, "Fr": 87, "Ra": 88, "Ac": 89,
      "Th": 90, "Pa": 91, "U": 92, "Np": 93}

NP = [("Np", 237, 93), ("Pa", 233, 91), ("U", 233, 92), ("Th", 229, 90), ("Ra", 225, 88), ("Ac", 225, 89), ("Fr", 221, 87),
      ("At", 217, 85), ("Bi", 213, 83), ("Po", 213, 84), ("Pb", 209, 82), ("Bi", 209, 83), ("Tl", 205, 81)]
TH = [("Th", 232, 90), ("Ra", 228, 88), ("Ac", 228, 89), ("Th", 228, 90), ("Ra", 224, 88), ("Rn", 220, 86), ("Po", 216, 84),
      ("Pb", 212, 82), ("Bi", 212, 83), ("Tl", 208, 81), ("Pb", 208, 82)]

# Rechte Spalte, Aufgabe 2. Index = Kern in TH (0 … 10), Pfeil i führt von Kern i zu Kern i+1.
TH_KERN_GEGEBEN = {0, 3, 6, 9, 10}       # Symbol, Massenzahl und Ordnungszahl stehen da
TH_PFEIL_GEGEBEN = {0, 1, 3, 6, 7}       # α/β steht am Pfeil, sonst Kästchen zum Bestimmen
# Wie links (Fr-221 → □ → □ → Bi-213) gibt es eine Doppellücke: Ra-224 → □ → □ → Po-216.

# Geometrie der rechten Spalte im Original (pt), gemessen mit get_drawings
RX_KREIS, KREIS_D = 503.9, 33.9
KREIS_Y = [65.9, 125.4, 185.7, 245.3, 305.6, 365.1, 425.4, 484.9, 546.0, 605.5, 667.4, 727.0]
RX_BOX, BOX = 479.4, 22.0
RX_KLEIN, KLEIN = 526.1, 14.8
# weiß überdeckt: Pfeil 11 mit Kästchen, Kreis 12, seine Kästchen A und Z (Kreis 11 endet bei 701,3)
WEG = [fitz.Rect(503.0, 701.9, 545.0, 762.5), fitz.Rect(477.5, 718.0, 503.0, 770.5)]
KLEIN_Y = [161.7, 220.7, 280.4, 340.5, 400.0, 460.3, 519.8, 581.7, 640.5, 702.4]   # Pfeile 1 … 10


def pruefe_reihe(reihe):
    for (s1, a1, z1), (s2, a2, z2) in zip(reihe, reihe[1:]):
        assert PS[s1] == z1 and PS[s2] == z2, (s1, s2)
        assert (a2, z2) in ((a1 - 4, z1 - 2), (a1, z1 + 1)), f"{s1}-{a1} → {s2}-{a2} ist weder α noch β"


def zerfall(a, b):
    return "α" if b[1] == a[1] - 4 else "β"


def spans(p):
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            yield from l["spans"]


def kreis_symbol(p, mitte, r, art):
    """Schwierigkeitskreis als Vektor: 0 leer, 1 halb (links gefüllt), 2 voll."""
    sh = p.new_shape()
    if art == 1:
        import math
        pts = [fitz.Point(mitte.x + r * math.cos(math.radians(w)), mitte.y - r * math.sin(math.radians(w))) for w in range(90, 271, 10)]
        sh.draw_polyline(pts)
        sh.finish(color=None, fill=SCHWARZ, closePath=True)
    sh.draw_circle(mitte, r)
    sh.finish(color=SCHWARZ, fill=SCHWARZ if art == 2 else None, width=0.9)
    sh.commit()


def baue_aufgabe(doc):
    p = doc[0]
    reg = doc.extract_font(250)[3]       # BBMLVQ+MinionPro-Regular (Teilmenge aus dem Original)
    minion = fitz.Font(fontbuffer=reg)

    def schreibe(pos, text, gr, farbe=SCHWARZ, font="minion"):
        fehlt = [c for c in text if c != " " and not minion.has_glyph(ord(c))]
        assert not fehlt, f"Glyphen fehlen in der Minion-Teilmenge: {fehlt}"
        p.insert_text(pos, text, fontname=font, fontsize=gr, color=farbe)

    sp = list(spans(p))
    rechts = lambda t: next(fitz.Point(s["origin"]) for s in sp if s["text"].strip() == t and s["origin"][0] > 470)   # rechte Spalte
    th_sym, th_a, th_z, alpha1 = rechts("Th"), rechts("232"), rechts("90"), rechts("α")
    zeile1 = next(fitz.Point(s["origin"]) for s in sp if s["text"].startswith("Th-232 ist radioaktiv"))
    thal = next(s for s in sp if s["text"].startswith("Thalium"))

    # 1) Alter Text Aufgabe 2 und „Thalium“ entfernen, Grafik bleibt (graphics=0)
    # Rechtecke knapp halten: Geschwärzt wird jedes Zeichen, dessen Kasten das Rechteck berührt (Überschrift endet bei 223,7)
    p.add_redact_annot(fitz.Rect(138, 228, 462, 380), fill=False)
    tb = fitz.Rect(thal["bbox"])
    p.add_redact_annot(fitz.Rect(tb.x0, tb.y0 + 8, tb.x1, tb.y1 - 8), fill=False)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)

    # 2) Rechte Spalte: Kästchen weg, wo die Zerfallsart jetzt dasteht; zwölften Kreis samt Pfeil und Kästchen weg
    for i in TH_PFEIL_GEGEBEN - {0}:
        y = KLEIN_Y[i - 1]
        p.add_redact_annot(fitz.Rect(RX_KLEIN - 1.5, y - 1.5, RX_KLEIN + KLEIN + 1.5, y + KLEIN + 1.5), fill=False)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED)
    # Kreis 12 samt Pfeil und Kästchen lässt sich per Schwärzung nicht entfernen (zusammenhängender Pfad), deshalb weiß überdecken
    for r in WEG:
        p.draw_rect(r, color=None, fill=(1, 1, 1), overlay=True)

    p.insert_font(fontname="minion", fontbuffer=reg)     # erst nach den Schwärzungen, die bauen die Ressourcen neu

    # 3) Neuer kurzer Text Aufgabe 2 im Zeilenraster des Originals
    text = ("Th-232 ist radioaktiv. Stelle die Zerfallsreihe für Thorium auf. Gehe vor wie in Aufgabe 1. "
            "Berechne das neue Element aus der Zerfallsart am Pfeil oder bestimme die Zerfallsart aus dem "
            "gegebenen neuen Element. Verwende dazu die Tabelle.")   # ohne Komma: die Minion-Teilmenge hat keins
    zeilen, z = [], ""
    for w in text.split():
        if minion.text_length(f"{z} {w}".strip(), 12) > 314:
            zeilen.append(z)
            z = w
        else:
            z = f"{z} {w}".strip()
    zeilen.append(z)
    for k, zl in enumerate(zeilen):
        schreibe((zeile1.x, zeile1.y + k * 14.4), zl, 12)
    unten = zeile1.y + (len(zeilen) - 1) * 14.4

    schreibe(fitz.Point(thal["origin"]), "Thallium", thal["size"])

    # 4) Schwierigkeitskreise hinter den Überschriften, Legende unter Aufgabe 2
    kreis_symbol(p, fitz.Point(199.5, 119.8), 4.6, 0)
    kreis_symbol(p, fitz.Point(199.5, 215.8), 4.6, 1)
    x, y = zeile1.x, unten + 24
    schreibe((x, y), "Schwierigkeit", 9, GRAU)
    x += minion.text_length("Schwierigkeit", 9) + 9
    for art, wort in enumerate(("leicht", "mittel", "schwer")):
        kreis_symbol(p, fitz.Point(x + 3.2, y - 3.1), 3.4, art)
        schreibe((x + 9.5, y), wort, 9, GRAU)
        x += 9.5 + minion.text_length(wort, 9) + 10

    # 5) Rechte Spalte füllen: gegebene Kerne und Zerfallsarten
    for i in TH_KERN_GEGEBEN - {0}:
        s, a, zz = TH[i]
        dy = KREIS_Y[i] - KREIS_Y[0]
        mitte = RX_KREIS + KREIS_D / 2
        schreibe((mitte - minion.text_length(s, 19) / 2, th_sym.y + dy), s, 19)
        schreibe((th_a.x, th_a.y + dy), str(a), 12)
        schreibe((th_z.x, th_z.y + dy), str(zz), 12)
    for i in TH_PFEIL_GEGEBEN - {0}:
        schreibe((alpha1.x, alpha1.y + KREIS_Y[i] - KREIS_Y[0]), zerfall(TH[i], TH[i + 1]), 12)
    return minion


def baue_loesung(doc, minion):
    """Alle leeren Kreise, Kästchen und Pfeil-Kästchen in Magenta füllen (Erkennung wie im alten Lösungsskript)."""
    p = doc[0]
    p.insert_font(fontname="minion", fontbuffer=doc.extract_font(250)[3])
    dr = p.get_drawings()
    einmal = lambda rs: [r for r in {(round(r.x0), round(r.y0)): r for r in rs}.values() if not any(w.contains(r) for w in WEG)]
    kreise = einmal([g["rect"] for g in dr if 32 <= round(g["rect"].width) <= 35 and abs(g["rect"].width - g["rect"].height) < 1.5])
    boxen = einmal([g["rect"] for g in dr if round(g["rect"].width) == 22 and round(g["rect"].height) == 22])
    klein = einmal([g["rect"] for g in dr if round(g["rect"].width) == 15 and round(g["rect"].height) == 15])
    worte = p.get_text("words")
    belegt = lambda r: any(r.contains(fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)) for w in worte)

    def mittig(r, text, gr):
        b = minion.text_length(text, gr)
        p.insert_text((r.x0 + r.width / 2 - b / 2, r.y0 + r.height / 2 + gr * 0.33), text, fontname="minion", fontsize=gr, color=MAG)

    gefuellt = 0
    for spalte, reihe in ((lambda r: r.x0 < 300, NP), (lambda r: r.x0 > 300, TH)):
        ks = sorted([k for k in kreise if spalte(k)], key=lambda r: r.y0)
        assert len(ks) == len(reihe), f"{len(ks)} Kreise, aber {len(reihe)} Kerne"
        for i, k in enumerate(ks):
            sym, a, z = reihe[i]
            if not belegt(k):
                mittig(k, sym, 17)
                gefuellt += 1
            ky = (k.y0 + k.y1) / 2
            for b in [b for b in boxen if spalte(b) and b.x1 <= k.x0 + 2 and k.x0 - b.x1 < 40 and abs((b.y0 + b.y1) / 2 - ky) < 22]:
                if not belegt(b):
                    mittig(b, str(a if (b.y0 + b.y1) / 2 < ky else z), 12)
            if i + 1 < len(reihe):
                for s in klein:
                    if spalte(s) and k.y1 - 5 < s.y0 < k.y1 + 40 and not belegt(s):
                        mittig(s, zerfall(reihe[i], reihe[i + 1]), 12)
    p.insert_text((436, 30), "LÖSUNG", fontname="hebo", fontsize=12, color=MAG)   # Ö fehlt in der Minion-Teilmenge
    return gefuellt


def main():
    pruefe_reihe(NP)
    pruefe_reihe(TH)
    aufgabe = fitz.open(str(QUELLE))
    minion = baue_aufgabe(aufgabe)
    aufgabe.save(str(ZIEL_A), garbage=3, deflate=True)

    loesung = fitz.open(str(ZIEL_A))
    n = baue_loesung(loesung, minion)
    loesung.save(str(ZIEL_L), garbage=3, deflate=True)

    beide = fitz.open(str(ZIEL_A))
    beide.insert_pdf(fitz.open(str(ZIEL_L)))
    beide.save(str(ZIEL), garbage=3, deflate=True)
    print("geschrieben:", ZIEL.name, "|", ZIEL_A.name, "|", ZIEL_L.name, "| Kreise in der Lösung gefüllt:", n)


if __name__ == "__main__":
    main()
