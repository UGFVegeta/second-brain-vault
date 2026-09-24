#!/usr/bin/env python3
"""Kernphysik-Folien im Labor-Stil B (heller Karo-Grund). Nutzt die Bausteine aus Optik/folien_zeichnungen.py.
Farben: Proton koralle, Neutron graublau, Elektron cyan; α orange, β cyan, γ violett.
Aufruf: python3 kern_zeichnungen.py -> ersetzt die Zeichnungen in Kernphysik.html (Seiten siehe ZEICHNUNGEN)."""
import math, re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent / "Optik"))
from folien_zeichnungen import Z, INK, GELB, ORANGE, CYAN  # noqa: E402

PROTON, NEUTRON, ELEKTRON, VIOLETT = "#E8604A", "#8FA3BD", "#0B8FB8", "#7A4BAF"


def teilchen(z, x, y, r, farbe):
    return z.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{farbe}" stroke="#FFFFFF" stroke-width="1"/>')


def kern(z, x, y, p, n, r=7, seed=3):
    """Kugelhaufen aus p Protonen und n Neutronen (Sonnenblumen-Anordnung, gemischt)."""
    farben = ["p"] * p + ["n"] * n
    s = seed
    for i in range(len(farben) - 1, 0, -1):          # deterministisch mischen
        s = (s * 9301 + 49297) % 233280
        j = s % (i + 1)
        farben[i], farben[j] = farben[j], farben[i]
    N = len(farben)
    for i, f in enumerate(farben):
        rr = r * 1.05 * math.sqrt(i + 0.5)
        a = i * 2.39996
        teilchen(z, x + rr * math.cos(a), y + rr * math.sin(a), r, PROTON if f == "p" else NEUTRON)
    return z


def elektron(z, x, y, r=5):
    return z.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 4}" fill="{ELEKTRON}" fill-opacity=".18"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{ELEKTRON}"/>')


def bahn(z, x, y, r):
    return z.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#9AAAC0" stroke-width="1.1" stroke-dasharray="4 4"/>')


def nuklid(z, x, y, sym, A, Zz, size=22, col=INK):
    """Nuklidschreibweise: A oben links, Z unten links, rechtsbündig vor dem Symbol bei x."""
    k = size * 0.55
    return z.add(f'<text x="{x - 2:.1f}" y="{y - size * 0.42:.1f}" font-family="PlexMono, Menlo, monospace" font-size="{k:.1f}" fill="{col}" text-anchor="end">{A}</text>'
                 f'<text x="{x - 2:.1f}" y="{y + size * 0.12:.1f}" font-family="PlexMono, Menlo, monospace" font-size="{k:.1f}" fill="{col}" text-anchor="end">{Zz}</text>'
                 f'<text x="{x:.1f}" y="{y:.1f}" font-family="Georgia, serif" font-size="{size}" fill="{col}">{sym}</text>')


def welle(z, x0, y, x1, col=VIOLETT, amp=6, lam=16, w=2.2):
    d = f"M{x0} {y}"
    x = x0
    while x < x1 - lam / 2:
        d += f" q{lam / 4} {-amp} {lam / 2} 0"
        amp = -amp
        x += lam / 2
    return z.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


# ---------------------------------------------------------------- Seiten
def stadion():
    z = Z("ks", 245)
    z.add('<ellipse cx="180" cy="130" rx="130" ry="82" fill="#E6F0DC" stroke="#9AAAC0" stroke-width="2"/>'
          '<ellipse cx="180" cy="130" rx="98" ry="58" fill="#D3E6C4"/>')
    z.glow(180, 130, 10)
    z.add(f'<circle cx="180" cy="130" r="3" fill="{PROTON}"/>')
    z.text(180, 34, "Modell: ein Fußballstadion", "middle", weight=600)
    z.text(180, 160, "Kern: eine Erbse", "middle", 9.5)
    z.text(180, 230, "Wäre das Atom so groß wie ein Stadion,", "middle", 9.5).text(180, 243, "wäre der Kern eine Erbse in der Mitte.", "middle", 9.5)
    z.pfeil(330, 130, 384, 130, "#66798E", 2)
    bahn(z, 500, 130, 78).add('')
    bahn(z, 500, 130, 48)
    kern(z, 500, 130, 3, 4, r=6)
    for a, rr in ((20, 78), (150, 48), (260, 78)):
        elektron(z, 500 + rr * math.cos(math.radians(a)), 130 - rr * math.sin(math.radians(a)))
    z.text(500, 34, "Atom", "middle", weight=600).text(590, 134, "Hülle")
    return z.svg()


def aufbau():
    z = Z("ka")
    bahn(z, 170, 106, 86)
    bahn(z, 170, 106, 54)
    kern(z, 170, 106, 3, 4, r=8)
    for a, rr in ((0, 54), (120, 54), (240, 86)):
        elektron(z, 170 + rr * math.cos(math.radians(a)), 106 - rr * math.sin(math.radians(a)), 6)
    for y, f, t in ((40, PROTON, "Proton, positiv geladen"), (70, NEUTRON, "Neutron, ungeladen")):
        teilchen(z, 330, y, 8, f)
        z.text(346, y + 4, t)
    elektron(z, 330, 100, 6)
    z.text(346, 104, "Elektron, negativ geladen")
    z.text(170, 204, "Kern: fast die ganze Masse", "middle", 9.5).text(170, 14, "Hülle: fast das ganze Volumen", "middle", 9.5)
    nuklid(z, 380, 168, "X", "A", "Z", 26)
    z.text(418, 146, "A = Massenzahl (Protonen + Neutronen)", size=9.5).text(418, 162, "Z = Kernladungszahl (Protonen)", size=9.5).text(418, 178, "X = Elementsymbol", size=9.5)
    return z.svg()


def isotope():
    z = Z("ki")
    for x in (212, 424):
        z.line(x, 18, x, 178, "#A3B7D3", 1, "5 4")
    for i, (name, n) in enumerate((("Wasserstoff", 0), ("Deuterium", 1), ("Tritium", 2))):
        x = 106 + i * 212
        bahn(z, x, 84, 46)
        kern(z, x, 84, 1, n, r=8, seed=5 + i)
        elektron(z, x + 46, 84, 6)
        z.text(x, 150, name, "middle", weight=600)
        nuklid(z, x - 6, 176, "H", 1 + n, 1, 20)
        z.text(x, 198, f"1 Proton, {n} Neutron{'en' if n != 1 else ''}", "middle", 9)
    z.text(318, 14, "alle drei sind Wasserstoff, denn alle haben genau 1 Proton", "middle", 9.5)
    return z.svg()


def zaehlrohr():
    z = Z("kz", 245)
    z.text(318, 40, "Das Zählrohr klickt, obwohl niemand etwas tut.", "middle", 11, 600)
    z.add('<rect x="130" y="72" width="170" height="108" rx="10" fill="#26324A"/><rect x="146" y="88" width="138" height="48" rx="4" fill="#0A1120"/>'
          '<text x="215" y="122" font-family="PlexMono, Menlo, monospace" font-size="24" fill="#6FE39A" text-anchor="middle">0023</text>'
          '<circle cx="168" cy="158" r="7" fill="#9FB2CF"/><circle cx="194" cy="158" r="7" fill="#9FB2CF"/>')
    z.add('<rect x="300" y="112" width="80" height="18" rx="9" fill="#9FB2CF"/><line x1="300" y1="121" x2="286" y2="121" stroke="#9FB2CF" stroke-width="3"/>')
    z.text(215, 200, "Zählgerät", "middle").text(340, 150, "Zählrohr", "middle")
    for (x, y) in ((470, 70), (520, 150), (560, 90), (430, 180), (600, 190)):
        z.glow(x, y, 10)
        z.add(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{VIOLETT}"/>')
    z.pfeil(470, 76, 388, 114, VIOLETT, 1.6, 7).pfeil(430, 176, 386, 128, VIOLETT, 1.6, 7)
    z.text(520, 224, "Strahlung aus der Umgebung", "middle", 9.5)
    return z.svg()


def radioaktivitaet():
    z = Z("kr")
    kern(z, 130, 100, 9, 12, r=7, seed=11)
    z.add('<circle cx="130" cy="100" r="44" fill="none" stroke="#E8604A" stroke-width="1.4" stroke-dasharray="3 4"/>')
    z.text(130, 166, "instabiler Kern", "middle", weight=600).text(130, 181, "zu viele oder zu wenige Neutronen", "middle", 9)
    z.pfeil(188, 100, 250, 100, "#66798E", 2).text(219, 90, "zerfällt", "middle", 9.5)
    kern(z, 316, 100, 8, 10, r=7, seed=13)
    z.text(316, 166, "stabilerer Kern", "middle", weight=600)
    z.pfeil(362, 84, 470, 54, ORANGE, 2.4)
    z.pfeil(362, 100, 470, 100, CYAN, 2.4)
    welle(z, 362, 118, 462, VIOLETT)
    z.pfeil(456, 124, 470, 146, VIOLETT, 2.2, 8)
    z.text(480, 58, "α-Strahlung").text(480, 104, "β-Strahlung").text(480, 152, "γ-Strahlung")
    z.text(318, 204, "Der Zeitpunkt für einen einzelnen Kern ist zufällig.", "middle", 9.5)
    return z.svg()


def abg():
    z = Z("kg")
    for x in (212, 424):
        z.line(x, 10, x, 202, "#A3B7D3", 1, "5 4")
    # alpha
    z.text(24, 29, "α-Zerfall", weight=600)
    kern(z, 60, 80, 6, 7, r=5.5, seed=21)
    z.pfeil(92, 80, 124, 80, "#66798E", 1.6, 7)
    kern(z, 152, 80, 4, 5, r=5.5, seed=22)
    kern(z, 172, 132, 2, 2, r=6, seed=7)
    z.pfeil(160, 122, 196, 104, ORANGE, 1.8, 7)
    z.text(150, 160, "Heliumkern", "middle", 9)
    z.text(16, 182, "A wird um 4 kleiner,", size=9).text(16, 195, "Z um 2 kleiner", size=9)
    # beta
    z.text(236, 29, "β⁻-Zerfall", weight=600)
    kern(z, 272, 80, 5, 8, r=5.5, seed=23)
    z.pfeil(304, 80, 336, 80, "#66798E", 1.6, 7)
    kern(z, 368, 80, 6, 7, r=5.5, seed=24)
    teilchen(z, 262, 126, 7, NEUTRON)
    z.pfeil(274, 126, 296, 126, "#66798E", 1.4, 6)
    teilchen(z, 308, 126, 7, PROTON)
    z.text(322, 130, "+", "middle")
    elektron(z, 340, 126, 5)
    z.text(228, 158, "Neutron wird zu Proton und Elektron", size=9)
    z.text(228, 182, "A bleibt gleich,", size=9).text(228, 195, "Z wird um 1 größer", size=9)
    # gamma
    z.text(448, 29, "γ-Strahlung", weight=600)
    kern(z, 484, 80, 5, 6, r=5.5, seed=25)
    z.add('<circle cx="484" cy="80" r="30" fill="none" stroke="#7A4BAF" stroke-width="1.4" stroke-dasharray="3 3"/>')
    z.text(484, 124, "angeregt", "middle", 9)
    z.pfeil(518, 80, 550, 80, "#66798E", 1.6, 7)
    kern(z, 584, 80, 5, 6, r=5.5, seed=25)
    welle(z, 456, 142, 600, VIOLETT)
    z.text(448, 164, "reine Energieabgabe", size=9).text(448, 182, "A und Z bleiben", size=9).text(448, 195, "unverändert", size=9)
    return z.svg()


def gleichungen():
    z = Z("kq")
    z.text(40, 30, "α-Zerfall von Uran-238", weight=600)
    for (x, s, A, Zz) in ((96, "U", 238, 92), (232, "Th", 234, 90), (344, "He", 4, 2)):
        nuklid(z, x, 76, s, A, Zz, 24)
    z.text(150, 72, "→", "middle", 20).text(300, 72, "+", "middle", 20)
    z.text(420, 64, "oben:  238 = 234 + 4", size=9.5).text(420, 80, "unten:  92 = 90 + 2", size=9.5)
    z.text(40, 118, "β⁻-Zerfall von Kohlenstoff-14", weight=600)
    for (x, s, A, Zz) in ((96, "C", 14, 6), (232, "N", 14, 7), (344, "e", 0, "−1")):
        nuklid(z, x, 164, s, A, Zz, 24)
    z.text(150, 160, "→", "middle", 20).text(300, 160, "+", "middle", 20)
    z.text(420, 152, "oben:  14 = 14 + 0", size=9.5).text(420, 168, "unten:  6 = 7 + (−1)", size=9.5)
    z.rect(40, 180, 556, 30, "#F4F7FA", 1, 3)
    z.text(52, 193, "1. Ausgangskern notieren   2. Teilchen der Strahlungsart anschreiben", size=9)
    z.text(52, 206, "3. obere und untere Zahlen ausgleichen   4. Element im Periodensystem ablesen", size=9)
    return z.svg()


def durchdringung():
    z = Z("kd")
    z.add('<path d="M30 128 h60 l-8 -30 h-44z" fill="#9FB2CF"/>')
    z.glow(60, 104, 16)
    z.text(60, 146, "Präparat", "middle", 9.5)
    z.rect(196, 30, 6, 146, "#F5E6C8").rect(342, 30, 14, 146, "#C6D1E1").rect(488, 30, 30, 146, "#4D5E77")
    z.text(199, 194, "Papier", "middle", 9.5).text(349, 194, "Aluminium", "middle", 9.5).text(503, 194, "Blei", "middle", 9.5)
    z.pfeil(92, 70, 194, 70, ORANGE, 2.4).formel(106, 60, "α")
    z.pfeil(92, 104, 340, 104, CYAN, 2.4).formel(106, 94, "β")
    welle(z, 92, 140, 488, VIOLETT)
    z.line(518, 140, 600, 140, VIOLETT, 1.2, None, .6)
    z.formel(106, 130, "γ")
    z.text(214, 66, "gestoppt", size=9.5).text(364, 100, "gestoppt", size=9.5)
    z.text(530, 124, "stark geschwächt,", size=9).text(530, 160, "aber nicht ganz weg", size=9)
    return z.svg()


ZEICHNUNGEN = {2: stadion, 5: aufbau, 7: isotope, 11: zaehlrohr, 14: radioaktivitaet, 16: abg, 18: gleichungen, 20: durchdringung}

if __name__ == "__main__":
    p = HIER / "Kernphysik.html"
    s = p.read_text(encoding="utf-8")
    teile = re.split(r'(<section class="folie[^"]*">.*?</section>)', s, flags=re.S)
    idx = [i for i, t in enumerate(teile) if t.startswith('<section class="folie')]
    for seite, fn in ZEICHNUNGEN.items():
        i = idx[seite - 1]
        teile[i] = re.sub(r"<svg.*?</svg>", lambda m: fn(), teile[i], count=1, flags=re.S)
    p.write_text("".join(teile), encoding="utf-8")
    print("Kernphysik.html ersetzt:", ", ".join(f"S. {k}" for k in ZEICHNUNGEN))
