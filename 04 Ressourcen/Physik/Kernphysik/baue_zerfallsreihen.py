#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Oskars Blatt „Radioaktiver Zerfall“ (Zerfallsreihen Np-237 und Th-232), umgebaut am 11.11.2026.

Aufgabe 2 braucht den langen Erklärtext nicht mehr. Die rechte Spalte ist jetzt aufgebaut wie die linke:
  - steht die Zerfallsart am Pfeil, berechnen die Schüler das neue Element,
  - ist das nächste Element schon gegeben, bestimmen sie die Zerfallsart (Kästchen am Pfeil).
Der überzählige zwölfte Kreis rechts fällt weg (die Reihe Th-232 bis Pb-208 hat 11 Kerne).
Dazu: Schwierigkeitskreise (Aufgabe 1 ○, Aufgabe 2 ◐) mit Legende, „Thalium“ korrigiert zu „Thallium“.
Schrift: Oskars eingebettete Minion Pro, damit alles aussieht wie das Original. Lösung in Magenta auf demselben Blatt.

Das Original in iCloud bleibt unverändert, es wird nur gelesen.
Rückseite (11.11.2026, Oskars Wunsch): die beiden anderen Reihen. Aufgabe 3 ◐ U-238 ab Ra-226 (setzt das Heftbeispiel fort),
Aufgabe 4 ◐ U-235, Aufgabe 5 ● Massenzahl durch 4: warum es genau vier Zerfallsreihen gibt.
Aufruf: python3 baue_zerfallsreihen.py
  -> Materialien/Zerfallsreihen (Oskar) – Aufgabe.pdf  und  … – Lösung.pdf  (je Vorder- und Rückseite, für iCloud und Druck)
  -> Materialien/Zerfallsreihen (Oskar).pdf  (Vorderseite leer, Vorderseite Lösung, Rückseite leer, Rückseite Lösung; für die Stunden-HTML)"""
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


# ---------------------------------------------------------------- Rückseite (11.11.2026): die beiden anderen Reihen
TIMES = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
TIMES_B = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
U238 = [("Ra", 226, 88), ("Rn", 222, 86), ("Po", 218, 84), ("Pb", 214, 82), ("Bi", 214, 83), ("Po", 214, 84),
        ("Pb", 210, 82), ("Bi", 210, 83), ("Po", 210, 84), ("Pb", 206, 82)]          # Fortsetzung des Heftbeispiels ab Ra-226
U235 = [("U", 235, 92), ("Th", 231, 90), ("Pa", 231, 91), ("Ac", 227, 89), ("Th", 227, 90), ("Ra", 223, 88), ("Rn", 219, 86),
        ("Po", 215, 84), ("Pb", 211, 82), ("Bi", 211, 83), ("Tl", 207, 81), ("Pb", 207, 82)]
# Doppellücken nur dort, wo beide Schritte gleich sind (αα), sonst wäre die Reihenfolge α/β nicht eindeutig.
U238_KERN, U238_PFEIL = {0, 3, 7, 9}, {0, 3, 4, 5, 7}            # Rn-222 → □ → □ → Pb-214: zweimal α
U235_KERN, U235_PFEIL = {0, 3, 7, 10, 11}, {0, 1, 3, 4, 7, 8}     # Ra-223 → □ → □ → Po-215: zweimal α
D, DY, Y0 = 33.9, 60.1, 65.9        # Kreisdurchmesser, Abstand, erster Kreis (wie die rechte Spalte vorne)
TEXT_X, TEXT_B = 141.2, 314


class Schrift:
    """Minion-Teilmenge aus Oskars PDF, fehlende Zeichen (Komma, ä, M, W …) zeichenweise aus Times New Roman."""
    def __init__(self, p, reg, bold):
        self.p = p
        self.f = {"mr": fitz.Font(fontbuffer=reg), "mb": fitz.Font(fontbuffer=bold), "tr": fitz.Font(fontfile=TIMES), "tb": fitz.Font(fontfile=TIMES_B)}
        p.insert_font(fontname="mr", fontbuffer=reg)
        p.insert_font(fontname="mb", fontbuffer=bold)
        p.insert_font(fontname="tr", fontfile=TIMES)
        p.insert_font(fontname="tb", fontfile=TIMES_B)

    def laeufe(self, text, fett):
        m, t = ("mb", "tb") if fett else ("mr", "tr")
        out = []
        for c in text:
            name = m if (c == " " or self.f[m].has_glyph(ord(c))) else t
            if out and out[-1][0] == name:
                out[-1][1] += c
            else:
                out.append([name, c])
        return out

    def breite(self, text, gr, fett=False):
        return sum(self.f[n].text_length(t, gr) for n, t in self.laeufe(text, fett))

    def schreibe(self, x, y, text, gr, farbe=SCHWARZ, fett=False):
        for n, t in self.laeufe(text, fett):
            self.p.insert_text((x, y), t, fontname=n, fontsize=gr, color=farbe)
            x += self.f[n].text_length(t, gr)

    def absatz(self, x, y, text, gr, breite, farbe=SCHWARZ, zeilenabstand=14.4):
        zeilen, z = [], ""
        for w in text.split():
            if self.breite(f"{z} {w}".strip(), gr) > breite:
                zeilen.append(z)
                z = w
            else:
                z = f"{z} {w}".strip()
        zeilen.append(z)
        for k, zl in enumerate(zeilen):
            self.schreibe(x, y + k * zeilenabstand, zl, gr, farbe)
        return y + (len(zeilen) - 1) * zeilenabstand


def spalte(p, sch, kx, reihe, kern_geg, pfeil_geg, loesung):
    """Eine Spalte wie vorne: Kreis, links Kästchen für Massen- und Ordnungszahl, Pfeil mit α/β oder Kästchen."""
    mx = kx + D / 2
    for i, (sym, a, z) in enumerate(reihe):
        y = Y0 + i * DY
        p.draw_circle((mx, y + D / 2), D / 2, color=SCHWARZ, width=1)
        boxen = (fitz.Rect(kx - 24.5, y - 1.8, kx - 2.5, y + 20.2), fitz.Rect(kx - 24.5, y + 25.4, kx - 2.5, y + 47.4))
        for b in boxen:
            p.draw_rect(b, color=SCHWARZ, width=1)
        if i in kern_geg:
            sch.schreibe(mx - sch.breite(sym, 19) / 2, y + 20.3, sym, 19)
            sch.schreibe(kx - 22.2, y - 1.8 + 13.8, str(a), 12)
            sch.schreibe(kx - 22.2, y + 25.4 + 13.8, str(z), 12)
        elif loesung:
            sch.schreibe(mx - sch.breite(sym, 17) / 2, y + 22.9, sym, 17, MAG)
            for b, wert in zip(boxen, (a, z)):
                sch.schreibe(b.x0 + 11 - sch.breite(str(wert), 12) / 2, b.y0 + 15, str(wert), 12, MAG)
        if i + 1 < len(reihe):
            yn = y + DY
            p.draw_line((mx, y + D + 0.5), (mx, yn - 5.6), color=SCHWARZ, width=1)
            p.draw_polyline([(mx - 2.55, yn - 7.2), (mx + 2.55, yn - 7.2), (mx, yn - 0.3), (mx - 2.55, yn - 7.2)], color=None, fill=SCHWARZ)
            art = zerfall(reihe[i], reihe[i + 1])
            if i in pfeil_geg:
                sch.schreibe(mx + 4.7, y + D + 9.3, art, 12)
            else:
                k = fitz.Rect(mx + 5.25, y + D + 2.4, mx + 20.05, y + D + 17.2)
                p.draw_rect(k, color=SCHWARZ, width=1)
                if loesung:
                    sch.schreibe(k.x0 + 7.4 - sch.breite(art, 12) / 2, k.y0 + 11, art, 12, MAG)


def baue_rueckseite(doc, vorne, reg, bold, loesung):
    """Hängt die Rückseite an doc an. vorne: fertige Vorderseite (eigenes Dokument), daraus Titel und Tabelle 1:1."""
    p = doc.new_page(width=vorne[0].rect.width, height=vorne[0].rect.height)
    for clip in (fitz.Rect(205, 30, 390, 66), fitz.Rect(170, 416, 377, 712)):      # Titel, Elementtabelle
        p.show_pdf_page(clip, vorne, 0, clip=clip)
    p.draw_rect(fitz.Rect(36.5, 36.5, 558.5, 817.9), color=SCHWARZ, width=2)
    sch = Schrift(p, reg, bold)
    sch.schreibe(71.3, 47.5, "Aufgabe 3", 12, fett=True)
    sch.schreibe(446.9, 47.5, "Aufgabe 4", 12, fett=True)
    spalte(p, sch, 85.5, U238, U238_KERN, U238_PFEIL, loesung)
    spalte(p, sch, 503.9, U235, U235_KERN, U235_PFEIL, loesung)

    y = 92
    for nr, stufe, text in (
            (3, 1, "Die Zerfallsreihe von U-238 kennst du aus dem Heft bis Ra-226. Setze sie fort bis zum stabilen Blei. Gehe vor wie in Aufgabe 2."),
            (4, 1, "U-235 ist radioaktiv. Stelle die Zerfallsreihe für U-235 auf. Gehe vor wie in Aufgabe 2."),
            (5, 2, "Teile in allen vier Reihen die Massenzahlen durch 4 und notiere den Rest. Was fällt dir auf? Erkläre damit, warum es genau vier Zerfallsreihen gibt.")):
        sch.schreibe(TEXT_X, y, f"Aufgabe {nr}", 12, fett=True)
        kreis_symbol(p, fitz.Point(TEXT_X + sch.breite(f"Aufgabe {nr}", 12, True) + 8.3, y - 4.2), 4.6, stufe)
        y = sch.absatz(TEXT_X, y + 14.4, text, 12, TEXT_B) + 28
    linien = [y - 6 + k * 22 for k in range(4)]
    for ly in linien:
        p.draw_line((TEXT_X, ly), (TEXT_X + TEXT_B, ly), color=GRAU, width=0.5)
    assert linien[-1] < 410, f"Aufgabe 5 ragt in die Tabelle ({linien[-1]:.0f})"
    if loesung:
        reste = {name: {a % 4 for _, a, _ in r} for name, r in (("Np", NP), ("Th", TH), ("U-238", U238), ("U-235", U235))}
        assert all(len(v) == 1 for v in reste.values()) and len({min(v) for v in reste.values()}) == 4, reste
        r = {k: min(v) for k, v in reste.items()}
        txt = (f"Der Rest bleibt in jeder Reihe gleich: Th {r['Th']}, Np {r['Np']}, U-238 {r['U-238']}, U-235 {r['U-235']}. "
               "Bei α sinkt die Massenzahl um 4, bei β bleibt sie gleich. Der Rest ändert sich also nie. "
               "Es gibt nur vier mögliche Reste, deshalb vier Reihen.")
        ende = sch.absatz(TEXT_X, linien[0] - 3, txt, 10.5, TEXT_B, MAG, zeilenabstand=22)
        assert ende <= linien[-1], "Lösung Aufgabe 5 zu lang"
        sch.schreibe(436, 30, "LÖSUNG", 12, MAG, fett=True)
    return p


def main():
    for r in (NP, TH, U238, U235):
        pruefe_reihe(r)
    quelle = fitz.open(str(QUELLE))
    reg, bold = quelle.extract_font(250)[3], quelle.extract_font(251)[3]

    aufgabe = fitz.open(str(QUELLE))
    minion = baue_aufgabe(aufgabe)
    vorne = fitz.open("pdf", aufgabe.tobytes())
    loesung = fitz.open("pdf", aufgabe.tobytes())
    n = baue_loesung(loesung, minion)

    baue_rueckseite(aufgabe, vorne, reg, bold, loesung=False)
    baue_rueckseite(loesung, vorne, reg, bold, loesung=True)
    aufgabe.save(str(ZIEL_A), garbage=3, deflate=True)
    loesung.save(str(ZIEL_L), garbage=3, deflate=True)

    # Für die Stunden-HTML: Seite 1 Vorderseite leer, Seite 2 Vorderseite Lösung, Seite 3 Rückseite leer, Seite 4 Rückseite Lösung
    beide = fitz.open()
    for s in (0, 1):
        beide.insert_pdf(aufgabe, from_page=s, to_page=s)
        beide.insert_pdf(loesung, from_page=s, to_page=s)
    beide.save(str(ZIEL), garbage=3, deflate=True)
    print("geschrieben:", ZIEL.name, "|", ZIEL_A.name, "|", ZIEL_L.name, "| Kreise vorne in der Lösung gefüllt:", n)


if __name__ == "__main__":
    main()
