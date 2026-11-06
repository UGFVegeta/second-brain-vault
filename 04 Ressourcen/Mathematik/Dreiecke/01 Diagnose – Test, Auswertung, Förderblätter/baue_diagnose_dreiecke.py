"""Diagnose Dreiecke Mathe 7c (04.11.2026), Version A und B, Lösung als ausgefülltes Blatt.

Grundlage: Standpunkt Schnittpunkt 7, S. 43, plus Nebenwinkel/Scheitelwinkel.
Ganze Seite als SVG in Millimetern: feste Positionen für den Scan, Maße stimmen bei Druck in Originalgröße.
Aufruf: python3 baue_diagnose_dreiecke.py
"""
import base64
import math
import subprocess
import tempfile  # noqa: F401
from pathlib import Path

HIER = Path(__file__).parent
VAULT = HIER.parents[3]
LOGO = base64.b64encode((VAULT / "07 Anhänge" / "GDRS Logo.png").read_bytes()).decode()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
NAME = "Mathe 7c – Diagnose Dreiecke"

TEAL = "#0f7c80"
PINK = "#d6006e"
GRAU = "#e6e6e6"
FONT = "Helvetica, Arial, sans-serif"

V = {
    "A": dict(
        s1=[("A", "B", 73, -6), ("C", "D", 46, 4)],
        s2=54,
        wa=[(125, 20, "stumpf"), (40, 70, "spitz"), (230, -20, "überstumpf"), (90, 15, "recht"), (180, 0, "gestreckt")],
        w4=[(35, 5), (118, 15)],
        w5=[65, 130],
        w6=38,
        spiegel=False,
        pkt=[("A", 1, 1), ("B", 8, 2), ("C", 4, 5)],
    ),
    "B": dict(
        s1=[("A", "B", 68, -4), ("C", "D", 52, 6)],
        s2=63,
        wa=[(90, 30, "recht"), (240, 10, "überstumpf"), (50, 60, "spitz"), (180, 0, "gestreckt"), (135, 10, "stumpf")],
        w4=[(52, 10), (143, 5)],
        w5=[75, 145],
        w6=46,
        spiegel=True,
        pkt=[("A", 1, 2), ("B", 8, 1), ("C", 5, 5)],
    ),
}


def P(cx, cy, r, grad):
    t = math.radians(grad)
    return cx + r * math.cos(t), cy - r * math.sin(t)


def txt(x, y, s, size=4.2, w="normal", fill="#111", anchor="start", style="normal"):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" font-weight="{w}" '
            f'font-style="{style}" fill="{fill}" text-anchor="{anchor}">{s}</text>')


def linie(x1, y1, x2, y2, farbe="#111", w=0.35, extra=""):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{farbe}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def bogen(cx, cy, r, a1, a2, farbe="#c0392b", w=0.35):
    x1, y1 = P(cx, cy, r, a1)
    x2, y2 = P(cx, cy, r, a2)
    gross = 1 if (a2 - a1) % 360 > 180 else 0
    return f'<path d="M{x1:.2f} {y1:.2f} A{r} {r} 0 {gross} 0 {x2:.2f} {y2:.2f}" fill="none" stroke="{farbe}" stroke-width="{w}"/>'


def kreuz(x, y, farbe="#c0392b", g=1.3):
    return linie(x - g, y - g, x + g, y + g, farbe, 0.35) + linie(x - g, y + g, x + g, y - g, farbe, 0.35)


def karo(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#888" stroke-width="0.3"/>']
    for i in range(1, int(w // 5)):
        s.append(linie(x + 5 * i, y, x + 5 * i, y + h, "#c8c8c8", 0.15))
    for j in range(1, int(h // 5)):
        s.append(linie(x, y + 5 * j, x + w, y + 5 * j, "#c8c8c8", 0.15))
    return "".join(s)


def feld(x, y, w=24, h=9, inhalt=""):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#111" stroke-width="0.4"/>'
    if inhalt:
        s += txt(x + w / 2, y + h - 2.5, inhalt, 4.6, "bold", PINK, "middle")
    return s


def stufe(x, y, n):
    s = f'<circle cx="{x}" cy="{y}" r="2" fill="#fff" stroke="#333" stroke-width="0.4"/>'
    if n == 1:
        s += f'<path d="M{x} {y-2} A2 2 0 0 0 {x} {y+2} Z" fill="#333"/>'
    if n == 2:
        s += f'<circle cx="{x}" cy="{y}" r="2" fill="#333"/>'
    return s


def smiley(x, y, art):
    s = f'<circle cx="{x}" cy="{y}" r="2.6" fill="#fff" stroke="#333" stroke-width="0.3"/>'
    s += f'<circle cx="{x-0.9}" cy="{y-0.7}" r="0.3" fill="#333"/><circle cx="{x+0.9}" cy="{y-0.7}" r="0.3" fill="#333"/>'
    if art == 0:
        s += f'<path d="M{x-1.2} {y+0.6} Q{x} {y+1.8} {x+1.2} {y+0.6}" fill="none" stroke="#333" stroke-width="0.3"/>'
    elif art == 1:
        s += linie(x - 1.1, y + 1.1, x + 1.1, y + 1.1, "#333", 0.3)
    else:
        s += f'<path d="M{x-1.2} {y+1.6} Q{x} {y+0.4} {x+1.2} {y+1.6}" fill="none" stroke="#333" stroke-width="0.3"/>'
    return s


def balken(y, nr, st, text):
    s = f'<rect x="12" y="{y}" width="186" height="8" fill="{GRAU}"/>'
    s += txt(14, y + 5.8, f"Nr. {nr}", 4.8, "bold", TEAL)
    s += stufe(31, y + 4, st)
    s += txt(35.5, y + 5.6, text, 4.0)
    for i in range(3):
        s += smiley(181 + 6.5 * i, y + 4, i)
    return s


def rechter_winkel_zeichen(cx, cy, a1, farbe=PINK, r=4.5):
    """Rechter Winkel wie im Unterricht: Viertelkreis von a1 bis a1 + 90 Grad mit Punkt."""
    mx, my = P(cx, cy, r * 0.48, a1 + 45)
    return bogen(cx, cy, r, a1, a1 + 90, farbe, 0.4) + f'<circle cx="{mx:.2f}" cy="{my:.2f}" r="0.45" fill="{farbe}"/>'


def winkelbild(cx, cy, a1, a2, r_leg, name, r_bogen=6, farbe="#111"):
    """Winkel von Schenkel a1 bis a2 (gegen den Uhrzeigersinn), Bogen + Name."""
    s = linie(cx, cy, *P(cx, cy, r_leg, a1), farbe, 0.4) + linie(cx, cy, *P(cx, cy, r_leg, a2), farbe, 0.4)
    if (a2 - a1) % 360 == 90:
        s += rechter_winkel_zeichen(cx, cy, a1, "#c0392b")
    else:
        s += bogen(cx, cy, r_bogen, a1, a2)
    mx, my = P(cx, cy, r_bogen + 3.6, a1 + ((a2 - a1) % 360) / 2)
    s += txt(mx, my + 1.4, name, 4.2, "normal", "#c0392b", "middle", "italic")
    return s


def kopf(v):
    s = f'<rect x="12" y="10" width="186" height="11" fill="#d9d9d9"/>'
    s += txt(15, 17.6, "Mathematik 7c   Diagnose: Grundlagen für Dreiecke", 5.4, "bold")
    s += txt(160, 17.6, f"Version {v}", 5.4, "bold", TEAL)
    s += f'<image href="data:image/png;base64,{LOGO}" x="179" y="22" width="19" height="19"/>'
    s += txt(15, 30, "Nummer:", 4.4, "bold") + feld(35, 24, 22, 9)
    s += txt(66, 30, "Datum:", 4.4, "bold") + feld(82, 24, 38, 9)
    s += txt(15, 39, "Geodreieck und Bleistift. Ergebnisse in die Kästen, Zeichnungen genau in die Karofelder.", 3.5)
    s += stufe(16, 44.5, 0) + txt(19.5, 45.8, "leicht", 3.4) + stufe(34, 44.5, 1) + txt(37.5, 45.8, "mittel", 3.4)
    s += stufe(52, 44.5, 2) + txt(55.5, 45.8, "schwer", 3.4)
    s += txt(72, 45.8, "Kreuze bei jeder Aufgabe an:", 3.4)
    for i, w in enumerate(["sicher", "ging so", "unsicher"]):
        s += smiley(122 + 19 * i, 44.5, i) + txt(125.5 + 19 * i, 45.8, w, 3.2)
    return s


def seite1(v, L):
    d = V[v]
    s = kopf(v)
    # Nr. 1 Strecken messen
    y = 50
    s += balken(y, 1, 0, "Miss die Länge der Strecken.")
    for i, (p, q, laenge, neig) in enumerate(d["s1"]):
        yy = y + 18 + 14 * i
        x1, y1 = 22, yy
        x2, y2 = P(x1, y1, laenge, neig)
        s += linie(x1, y1, x2, y2, "#111", 0.4) + kreuz(x1, y1) + kreuz(x2, y2)
        s += txt(x1 - 4.5, y1 + 1.5, p, 4, "bold") + txt(x2 + 2.5, y2 + 1.5, q, 4, "bold")
        s += txt(132, yy + 2, f"{'ab'[i]})  {p}{q} =", 4.4) + feld(152, yy - 4.5, 22, 9, f"{laenge/10:.1f}".replace(".", ",") if L else "")
        s += txt(176, yy + 2, "cm", 4.4)
    # Nr. 2 Strecke zeichnen
    y = 98
    m = f"{d['s2']/10:.1f}".replace(".", ",")
    s += balken(y, 2, 0, f"Zeichne ab dem Punkt E eine Strecke EF mit der Länge {m} cm.")
    s += karo(12, y + 10, 186, 20)
    s += kreuz(27, y + 20) + txt(23, y + 17, "E", 4, "bold")
    if L:
        s += linie(27, y + 20, 27 + d["s2"], y + 20, PINK, 0.6) + kreuz(27 + d["s2"], y + 20, PINK) + txt(25 + d["s2"], y + 17, "F", 4, "bold", PINK)
    # Nr. 3 Winkelarten
    y = 136
    s += balken(y, 3, 0, "Welche Winkelart ist das? Schreibe sie in das Kästchen darunter.")
    worte = ["spitz", "recht", "stumpf", "gestreckt", "überstumpf"]
    for i, wo in enumerate(worte):
        s += f'<rect x="{24 + 33*i}" y="{y+11}" width="29" height="7" rx="1" fill="#fdf1d8" stroke="#e0b25c" stroke-width="0.3"/>'
        s += txt(38.5 + 33 * i, y + 16.2, wo, 3.6, "normal", "#1a5fa8", "middle", "italic")
    namen = ["α", "β", "γ", "δ", "ε"]
    for i, (gr, rot, art) in enumerate(d["wa"]):
        cx = 12 + 37.2 * i + 18.6
        cy = y + 42 if gr <= 180 else y + 37
        if gr == 180:
            cy = y + 44
        s += winkelbild(cx, cy, rot, rot + gr, 15, namen[i], 5)
        s += feld(cx - 16, y + 55, 32, 9, art if L else "")
        s += txt(cx - 15, y + 53, f"{namen[i]} ist", 3.2, "normal", "#555")
    # Nr. 4 Winkel messen
    y = 214
    s += balken(y, 4, 1, "Miss die Winkel α und β.")
    for i, (gr, rot) in enumerate(d["w4"]):
        cx = 30 + 93 * i if gr < 100 else 75 + 93 * i - 35
        cx = [24, 150][i] if gr < 100 else [70, 160][i]
        cy = y + 58
        s += winkelbild(cx, cy, rot, rot + gr, 52, ["α", "β"][i], 8)
        s += txt(30 + 93 * i, y + 71, f"{['α', 'β'][i]} =", 4.4) + feld(41 + 93 * i, y + 65.5, 22, 9, str(gr) if L else "") + txt(65 + 93 * i, y + 71, "°", 4.4)
    return s


def seite2(v, L):
    d = V[v]
    s = ""
    # Nr. 5 Winkel zeichnen
    y = 12
    s += balken(y, 5, 1, "Zeichne die Winkel. Scheitel S und der erste Schenkel sind vorgegeben.")
    for i, gr in enumerate(d["w5"]):
        x0 = 12 + 95 * i
        s += karo(x0, y + 10, 91, 55)
        s += txt(x0 + 2, y + 16, f"{'ab'[i]})  {['α', 'β'][i]} = {gr}°", 4.4, "bold")
        cx, cy = x0 + 40 + (5 if gr < 90 else 0), y + 60
        s += linie(cx, cy, cx + 45, cy, "#111", 0.45) + f'<circle cx="{cx}" cy="{cy}" r="0.7" fill="#111"/>' + txt(cx - 2, cy + 4.4, "S", 4, "bold")
        if L:
            s += linie(cx, cy, *P(cx, cy, 45, gr), PINK, 0.6) + bogen(cx, cy, 8, 0, gr, PINK, 0.45)
            mx, my = P(cx, cy, 12, gr / 2)
            s += txt(mx, my + 1.4, f"{gr}°", 3.8, "bold", PINK, "middle")
    # Nr. 6 Nebenwinkel / Scheitelwinkel
    y = 80
    a = d["w6"]
    s += balken(y, 6, 2, f"Zwei Geraden schneiden sich, α = {a}°. Bestimme β, γ und δ ohne Messen.")
    cx, cy, rot = 58, y + 30, 8
    for g in (rot, rot + a):
        s += linie(*P(cx, cy, 23, g), *P(cx, cy, 23, g + 180), "#111", 0.4)
    for nm, a1, a2 in (("α", rot, rot + a), ("β", rot + a, rot + 180), ("γ", rot + 180, rot + 180 + a), ("δ", rot + 180 + a, rot + 360)):
        r = 7 if (a2 - a1) < 90 else 5.5
        s += bogen(cx, cy, r, a1, a2)
        mx, my = P(cx, cy, r + 4, (a1 + a2) / 2)
        s += txt(mx, my + 1.4, nm, 4.2, "normal", "#c0392b", "middle", "italic")
    s += txt(106, y + 17, "Die Zeichnung ist nicht genau.", 3.3, "normal", "#555", style="italic")
    for i, (nm, w) in enumerate((("β", 180 - a), ("γ", a), ("δ", 180 - a))):
        xx, yy = 100 + 33 * i, y + 32
        s += txt(xx, yy + 2, f"{nm} =", 4.4) + feld(xx + 8.5, yy - 4.5, 16, 9, str(w) if L else "") + txt(xx + 25.5, yy + 2, "°", 4.4)
    # Nr. 7 Senkrechte und Parallele
    y = 130
    s += balken(y, 7, 1, "Zeichne  a) die Senkrechte h zu g durch A,  b) die Parallele k zu g durch B.")
    fy = y + 10
    s += karo(12, fy, 186, 55)
    s += f'<clipPath id="c7"><rect x="12" y="{fy}" width="186" height="55"/></clipPath>'

    def X(x):
        return 210 - x if d["spiegel"] else x
    s += linie(X(17), fy + 5, X(187), fy + 47.5, "#111", 0.45) + txt(X(184), fy + 42, "g", 4.4, "bold", "#111", "middle", "italic")
    ax, ay = 77, fy + 20
    bx, by = 147, fy + 12
    s += kreuz(X(ax), ay) + txt(X(ax - 4), ay + 1, "A", 4, "bold", anchor="middle")
    s += kreuz(X(bx), by) + txt(X(bx), by - 3, "B", 4, "bold", anchor="middle")
    if L:
        s += '<g clip-path="url(#c7)">'
        s += linie(X(ax + 4.5), ay - 18, X(ax - 8.5), ay + 34, PINK, 0.6) + txt(X(ax + 7.5), ay - 13, "h", 4.4, "bold", PINK, "middle", "italic")
        s += linie(X(bx - 140), by - 35, X(bx + 48), by + 12, PINK, 0.6) + txt(X(bx + 38), by + 5, "k", 4.4, "bold", PINK, "middle", "italic")
        s += '</g>'
        # rechter Winkel bei A
        tg = math.degrees(math.atan2(-1, 4))          # Richtung von g (nach rechts unten), Mathe-Winkel
        s += rechter_winkel_zeichen(X(ax), ay, tg if not d["spiegel"] else 180 - (tg + 90))
    # Nr. 8 Koordinatensystem
    y = 199
    s += balken(y, 8, 1, "Zeichne ein Koordinatensystem und trage die Punkte ein.")
    s += txt(16, y + 20, "; ".join(f"{n}({px}|{py})" for n, px, py in d["pkt"]), 4.6)
    s += txt(16, y + 28, "1 Einheit = 1 cm", 4.4, "bold")
    s += txt(16, y + 38, "Verbinde die Punkte", 4.2) + txt(16, y + 43.5, "zum Dreieck ABC.", 4.2)
    ox, oy = 92, y + 80
    s += karo(82, y + 10, 116, 80)
    if L:
        s += linie(ox, oy, ox + 102, oy, PINK, 0.5) + linie(ox, oy, ox, oy - 67, PINK, 0.5)
        s += f'<path d="M{ox+102} {oy} l-2.5 -1.2 v2.4 Z M{ox} {oy-67} l-1.2 2.5 h2.4 Z" fill="{PINK}"/>'
        s += txt(ox + 99, oy + 5, "x", 4, fill=PINK, style="italic") + txt(ox - 4.5, oy - 64, "y", 4, fill=PINK, style="italic")
        for k in range(0, 10):
            s += linie(ox + 10 * k, oy - 1, ox + 10 * k, oy + 1, PINK, 0.35) + txt(ox + 10 * k, oy + 4.6, str(k), 3.4, fill=PINK, anchor="middle")
        for k in range(1, 7):
            s += linie(ox - 1, oy - 10 * k, ox + 1, oy - 10 * k, PINK, 0.35) + txt(ox - 2.5, oy - 10 * k + 1.2, str(k), 3.4, fill=PINK, anchor="end")
    if L:
        pts = [(ox + 10 * px, oy - 10 * py) for _, px, py in d["pkt"]]
        s += f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{PINK}" stroke-width="0.6"/>'
        for (n, _, _), (a, b) in zip(d["pkt"], pts):
            s += kreuz(a, b, PINK) + txt(a + 1.8, b - 1.8, n, 4, "bold", PINK)
    return s


def seite(inhalt):
    return f'<svg class="s" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 297" width="210mm" height="297mm">{inhalt}</svg>'


def html(seiten):
    return ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Diagnose Dreiecke</title>'
            '<style>@page{size:A4;margin:0}html,body{margin:0;padding:0}svg.s{display:block;page-break-after:always}'
            'svg.s:last-child{page-break-after:auto}@media screen{body{background:#999}svg.s{background:#fff;margin:10px auto}}</style>'
            '</head><body>' + "".join(seite(x) for x in seiten) + '</body></html>')


def pdf(name, seiten):
    """HTML nur als Zwischenschritt im Temp-Ordner, im Vault landet nur die PDF."""
    import tempfile
    h = Path(tempfile.gettempdir()) / f"{name}.html"
    h.write_text(html(seiten), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={HIER / (name + '.pdf')}", h.as_uri()], check=True, capture_output=True)
    return HIER / f"{name}.pdf"


PDFS = [HIER / f"{NAME} – Version A.pdf", HIER / f"{NAME} – Version B.pdf", HIER / f"{NAME} – Lösung.pdf"]

if __name__ == "__main__":
    for v in "AB":
        print(pdf(f"{NAME} – Version {v}", [seite1(v, False), seite2(v, False)]).name)
    print(pdf(f"{NAME} – Lösung", [seite1("A", True), seite2("A", True), seite1("B", True), seite2("B", True)]).name)
