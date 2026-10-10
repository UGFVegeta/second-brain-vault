#!/usr/bin/env python3
"""Konzeptbild v2: Lego-Modell Wieslauftalbahn (WEG VT 451, Regio-Shuttle RS1), Maßstab ca. 1:45, 8 Noppen breit.

Modell = Raster aus 1 Noppe x 1 Noppe x 1 Platte. Render = Voxel-Painter-Algorithmus.
Aufruf: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 lego_wiesel_modell.py <ausgabe.png>
"""
import math, sys
from PIL import Image, ImageDraw, ImageFont

PL = 0.4          # Plattenhöhe in Noppen
L = 70            # Länge in Noppen
Wd = 8            # Breite in Noppen
KTOP = 26         # Höhe in Platten

Y   = (242, 205, 55)
B   = (0, 85, 191)
G   = (108, 110, 104)
LG  = (160, 165, 169)
K   = (24, 28, 32)
WIN = (52, 66, 80)
LAMP = (255, 244, 190)
SLEEP = (120, 112, 104)

vox = {}


def box(x0, x1, y0, y1, k0, k1, col):
    for i in range(x0, x1):
        for j in range(y0, y1):
            for k in range(k0, k1):
                vox[(i, j, k)] = col


# ---------- Gleis ----------
for x in range(-6, L + 7, 2):
    box(x, x + 1, 0, Wd, -2, -1, SLEEP)
box(-6, L + 7, 1, 2, -1, 0, G)
box(-6, L + 7, 6, 7, -1, 0, G)

# ---------- Fahrwerk (Räder kommen als Aufkleber) ----------
AXLES = (11, 16, L - 1 - 16, L - 1 - 11)
box(AXLES[0] - 1, AXLES[1] + 2, 2, 6, 2, 4, G)
box(AXLES[2] - 1, AXLES[3] + 2, 2, 6, 2, 4, G)
box(22, 47, 2, 6, 3, 5, G)            # Unterflurgeräte
box(25, 33, 2, 6, 2, 3, G)
box(37, 45, 2, 6, 2, 3, G)

# ---------- Wagenkasten ----------
box(0, L, 0, Wd, 5, 6, B)             # blauer Streifen unten
box(0, L, 0, Wd, 6, 23, Y)            # Kasten k6..22
box(0, L, 1, Wd - 1, 23, 24, Y)       # Dachrundung 1
box(0, L, 2, Wd - 2, 24, 25, Y)       # Dachrundung 2
box(1, L - 1, 3, 5, 24, 25, LG)       # Dachmitte
box(10, 18, 2, 6, 25, 26, LG)         # Klimageräte
box(52, 60, 2, 6, 25, 26, LG)
box(31, 37, 3, 5, 25, 26, (214, 218, 220))

SIDE_Y = (0, Wd - 1)


def side_col(x, kind, k0=10, k1=18):
    for y in SIDE_Y:
        for k in range(k0, k1):
            vox[(x, y, k)] = kind


def glazing(first, last):
    for x in range(first, last + 1):
        n = (x - first) % 4
        side_col(x, K if (n == 3 and x != last) else WIN)


glazing(4, 19)         # Fahrerkabine + erste Fenstergruppe
glazing(27, 48)        # Mittelteil
glazing(57, 61)        # hintere Fenstergruppe

# Einstiege: blaue Rahmen, gelbe Türflügel, Fenster mittig
for d0 in (20, 50):
    for y in SIDE_Y:
        for k in range(6, 23):
            vox[(d0, y, k)] = B
            vox[(d0 + 5, y, k)] = B
        for x in range(d0, d0 + 6):
            for k in range(18, 23):
                vox[(x, y, k)] = B
        for x in (d0 + 2, d0 + 3):
            for k in range(11, 17):
                vox[(x, y, k)] = WIN


# ---------- Stirnseiten ----------
def front(xs, step):
    for k in range(5, 9):
        for y in range(Wd):
            vox[(xs, y, k)] = B
    for y in range(Wd):
        vox[(xs, y, 9)] = K if 2 <= y <= 5 else B
    for y in range(Wd):
        vox[(xs, y, 10)] = K if 2 <= y <= 5 else (Y if y in (0, Wd - 1) else B)
    for y in (1, 6):
        vox[(xs, y, 7)] = LAMP
    for y in (3, 4):
        vox[(xs, y, 7)] = K
        vox[(xs, y, 8)] = K
    for k in range(11, 22):                 # geneigte Frontscheibe
        off = 1 if k <= 16 else 2
        for y in range(1, Wd - 1):
            for dd in range(off):
                vox.pop((xs + step * dd, y, k), None)
            vox[(xs + step * off, y, k)] = WIN
    cx0, cx1 = (xs - 1, xs) if step == 1 else (xs + 1, xs + 2)
    box(cx0, cx1, 3, 5, 2, 4, G)             # Kupplung


front(0, +1)
front(L - 1, -1)


# ---------- Projektion ----------
def proj(P, t, p):
    x, y, z = P
    sx = x * math.sin(t) - y * math.cos(t)
    up = x * math.sin(p) * math.cos(t) + y * math.sin(p) * math.sin(t) + z * math.cos(p)
    return sx, -up


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def circle3(cx, cy, z, r, n=14):
    return [(cx + r * math.cos(2 * math.pi * a / n), cy + r * math.sin(2 * math.pi * a / n), z) for a in range(n)]


def render(theta, phi, S, SS, decals=(), pad=1.5, bg=((246, 248, 250), (226, 231, 236))):
    t, p = math.radians(theta), math.radians(phi)
    xs, ys = [], []
    for (i, j, k) in vox:
        for di in (0, 1):
            for dj in (0, 1):
                for dk in (0, 1):
                    a, b = proj((i + di, j + dj, (k + dk) * PL), t, p)
                    xs.append(a); ys.append(b)
    x0, x1 = min(xs) - pad, max(xs) + pad
    y0, y1 = min(ys) - pad - 0.4, max(ys) + pad
    W, H = int((x1 - x0) * S * SS), int((y1 - y0) * S * SS)
    sc = S * SS
    img = Image.new('RGB', (W, H))
    gd = ImageDraw.Draw(img)
    for yy in range(H):
        f = yy / H
        gd.line([(0, yy), (W, yy)], fill=tuple(int(bg[0][c] * (1 - f) + bg[1][c] * f) for c in range(3)))
    img = img.convert('RGBA')
    d = ImageDraw.Draw(img)

    def scr(P):
        a, b = proj(P, t, p)
        return ((a - x0) * sc, (b - y0) * sc)

    ln = max(1, SS // 2)
    for (i, j, k) in sorted(vox, key=lambda q: (-q[0], -q[1], q[2])):
        col = vox[(i, j, k)]
        z0, z1 = k * PL, (k + 1) * PL
        edge = lambda c: shade(c, 0.80)
        if (i, j - 1, k) not in vox:
            poly = [scr((i, j, z0)), scr((i + 1, j, z0)), scr((i + 1, j, z1)), scr((i, j, z1))]
            c = shade(col, 0.92)
            d.polygon(poly, fill=c, outline=edge(c), width=ln)
        if (i - 1, j, k) not in vox:
            poly = [scr((i, j, z0)), scr((i, j + 1, z0)), scr((i, j + 1, z1)), scr((i, j, z1))]
            c = shade(col, 0.76)
            d.polygon(poly, fill=c, outline=edge(c), width=ln)
        if (i, j, k + 1) not in vox:
            poly = [scr((i, j, z1)), scr((i + 1, j, z1)), scr((i + 1, j + 1, z1)), scr((i, j + 1, z1))]
            c = shade(col, 1.06)
            d.polygon(poly, fill=c, outline=edge(c), width=ln)
            hs = 0.17
            for step in range(5):
                zz = z1 + hs * step / 4
                d.polygon([scr(q) for q in circle3(i + 0.5, j + 0.5, zz, 0.3)],
                          fill=shade(col, 0.82 if step < 4 else 1.12),
                          outline=shade(col, 0.7) if step == 4 else None)

    dvec = (math.cos(p) * math.cos(t), math.cos(p) * math.sin(t), -math.sin(p))
    for dec in decals:
        n = dec['normal']
        if n[0] * dvec[0] + n[1] * dvec[1] + n[2] * dvec[2] > -0.05:
            continue
        im, ppu = dec['img'], dec['ppu']
        O, A, Bd = dec['O'], dec['A'], dec['B']
        oo = scr(O)
        fa = proj(A, t, p); fb = proj(Bd, t, p)
        Fm = [[fa[0] * sc / ppu, fb[0] * sc / ppu], [fa[1] * sc / ppu, fb[1] * sc / ppu]]
        det = Fm[0][0] * Fm[1][1] - Fm[0][1] * Fm[1][0]
        if abs(det) < 1e-9:
            continue
        inv = [[Fm[1][1] / det, -Fm[0][1] / det], [-Fm[1][0] / det, Fm[0][0] / det]]
        a_, b_ = inv[0]; d_, e_ = inv[1]
        c_ = -(a_ * oo[0] + b_ * oo[1]); f_ = -(d_ * oo[0] + e_ * oo[1])
        layer = im.transform((W, H), Image.AFFINE, (a_, b_, c_, d_, e_, f_), resample=Image.BILINEAR)
        img = Image.alpha_composite(img, layer)
    return img.convert('RGB').resize((W // SS, H // SS), Image.LANCZOS)


# ---------- Aufkleber ----------
def font(path, size, idx=0):
    try:
        return ImageFont.truetype(path, size, index=idx)
    except Exception:
        return ImageFont.load_default()


SCRIPT = '/System/Library/Fonts/SnellRoundhand.ttc'
HELV = '/System/Library/Fonts/HelveticaNeue.ttc'
BLUE_TXT = (46, 95, 168)


def wiesel(w, h):
    S0 = 3
    im = Image.new('RGBA', (400 * S0, 500 * S0), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = lambda pts: [(x * S0, y * S0) for x, y in pts]
    fur, cream = (178, 104, 52), (246, 224, 190)
    d.line(s([(110, 480), (60, 430), (40, 360), (80, 320), (125, 330)]), fill=fur, width=44 * S0, joint='curve')
    d.line(s([(60, 395), (45, 360), (70, 328)]), fill=cream, width=40 * S0, joint='curve')
    d.rounded_rectangle([x * S0 for x in (130, 255, 290, 500)], radius=20 * S0, fill=(250, 250, 250))
    d.polygon(s([(130, 275), (205, 270), (195, 500), (130, 500)]), fill=(138, 142, 148))
    d.polygon(s([(290, 275), (215, 270), (225, 500), (290, 500)]), fill=(138, 142, 148))
    d.polygon(s([(198, 275), (222, 275), (226, 360), (210, 378), (194, 360)]), fill=(44, 112, 208))
    d.rectangle([x * S0 for x in (130, 440, 290, 468)], fill=(122, 74, 40))
    d.rectangle([x * S0 for x in (196, 440, 224, 468)], fill=(222, 190, 90))
    d.line(s([(135, 290), (112, 380), (140, 440)]), fill=(250, 250, 250), width=30 * S0, joint='curve')
    d.ellipse([x * S0 for x in (118, 424, 160, 466)], fill=fur)
    d.line(s([(285, 290), (330, 280), (352, 232)]), fill=(250, 250, 250), width=30 * S0, joint='curve')
    d.ellipse([x * S0 for x in (332, 180, 384, 240)], fill=fur)
    for fx in (340, 355, 370):
        d.ellipse([x * S0 for x in (fx, 168, fx + 16, 196)], fill=fur)
    d.ellipse([x * S0 for x in (120, 90, 310, 250)], fill=fur)
    d.ellipse([x * S0 for x in (112, 95, 160, 140)], fill=fur); d.ellipse([x * S0 for x in (120, 103, 152, 134)], fill=cream)
    d.ellipse([x * S0 for x in (250, 95, 298, 140)], fill=fur); d.ellipse([x * S0 for x in (258, 103, 290, 134)], fill=cream)
    d.ellipse([x * S0 for x in (150, 170, 270, 262)], fill=cream)
    d.ellipse([x * S0 for x in (196, 178, 224, 196)], fill=(40, 30, 30))
    for ex in (172, 232):
        d.ellipse([x * S0 for x in (ex, 135, ex + 26, 165)], fill=(255, 255, 255))
        d.ellipse([x * S0 for x in (ex + 8, 143, ex + 20, 162)], fill=(30, 20, 20))
    d.arc([x * S0 for x in (180, 195, 240, 235)], 20, 160, fill=(80, 40, 30), width=3 * S0)
    for sy in (205, 215, 225):
        d.line(s([(160, sy), (110, sy - 8)]), fill=(255, 255, 255), width=2 * S0)
        d.line(s([(260, sy), (310, sy - 8)]), fill=(255, 255, 255), width=2 * S0)
    d.pieslice([x * S0 for x in (128, 28, 292, 150)], 180, 360, fill=(44, 108, 190))
    d.rectangle([x * S0 for x in (128, 90, 292, 118)], fill=(20, 24, 32))
    d.ellipse([x * S0 for x in (120, 106, 300, 134)], fill=(20, 24, 32))
    d.text((165 * S0, 58 * S0), 'WEG', font=font(HELV, 34 * S0, 1), fill=(255, 255, 255))
    return im.resize((w, h), Image.LANCZOS)


def wappen(w, h, kind):
    S0 = 4
    im = Image.new('RGBA', (w * S0, h * S0), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W0, H0 = w * S0, h * S0
    outline = [(0.05 * W0, 0.02 * H0), (0.95 * W0, 0.02 * H0), (0.95 * W0, 0.55 * H0), (0.5 * W0, 0.98 * H0), (0.05 * W0, 0.55 * H0)]
    base = {'rm': (250, 220, 70), 'rud': (250, 250, 250), 'sdf': (205, 40, 40)}[kind]
    d.polygon(outline, fill=base)
    if kind == 'rm':
        d.polygon([(0.2 * W0, 0.02 * H0), (0.55 * W0, 0.02 * H0), (0.8 * W0, 0.75 * H0), (0.6 * W0, 0.85 * H0)], fill=(30, 85, 175))
    if kind == 'rud':
        d.polygon([(0.05 * W0, 0.5 * H0), (0.95 * W0, 0.5 * H0), (0.5 * W0, 0.98 * H0)], fill=(70, 160, 90))
    if kind == 'sdf':
        d.line([(0.2 * W0, 0.3 * H0), (0.8 * W0, 0.8 * H0)], fill=(245, 205, 60), width=int(0.1 * W0))
        d.line([(0.8 * W0, 0.3 * H0), (0.2 * W0, 0.8 * H0)], fill=(245, 205, 60), width=int(0.1 * W0))
    d.polygon(outline, outline=(40, 40, 40), width=2 * S0 // 2)
    return im.resize((w, h), Image.LANCZOS)


def side_decal(ppu=36):
    ztop = KTOP * PL
    W, H = int(L * ppu), int(ztop * ppu)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    X = lambda x: int(x * ppu)
    Z = lambda z: int((ztop - z) * ppu)
    # Lower Band k6..9 = z 2.4..4.0; Fenster k10..17 = z 4.0..7.2; oberes Band bis 9.2
    mh = int((7.2 - 2.45) * ppu)
    mw = int(mh * 0.8)
    im.alpha_composite(wiesel(mw, mh), (X(35.0), Z(7.2)))
    d = ImageDraw.Draw(im)
    d.text((X(27.3), Z(3.95)), "Ich bin's Wiesel!", font=font(SCRIPT, int(1.05 * ppu)), fill=BLUE_TXT)
    d.text((X(40.6), Z(9.15)), 'Willkommen an Bord!', font=font(SCRIPT, int(1.1 * ppu)), fill=BLUE_TXT)
    for n, kind in enumerate(('rm', 'rud', 'sdf')):
        im.alpha_composite(wappen(int(1.0 * ppu), int(1.2 * ppu), kind), (X(41.5 + n * 1.5), Z(3.95)))
    return {'img': im, 'ppu': ppu, 'O': (0, 0, ztop), 'A': (1, 0, 0), 'B': (0, 0, -1), 'normal': (0, -1, 0)}


def wheel_decal(ppu=48):
    W, H = int(L * ppu), int(2.0 * ppu)
    im = Image.new('RGBA', (W * 1, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for ax in AXLES:
        cx, cy, r = int((ax + 0.5) * ppu), int(H - 1.0 * ppu), int(1.0 * ppu)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(26, 28, 32))
        r2 = int(0.72 * ppu)
        d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(92, 96, 102))
        r3 = int(0.22 * ppu)
        d.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=(150, 154, 158))
    return {'img': im, 'ppu': ppu, 'O': (0, 1, 2.0), 'A': (1, 0, 0), 'B': (0, 0, -1), 'normal': (0, -1, 0)}


def front_decal(ppu=60):
    W, H = int(4 * ppu), int(0.8 * ppu)
    im = Image.new('RGBA', (W, H), (14, 16, 18, 255))
    d = ImageDraw.Draw(im)
    f = font('/System/Library/Fonts/Courier.ttc', int(0.45 * ppu))
    txt = "Ich bin's Wiesel"
    tw = d.textlength(txt, font=f)
    d.text(((W - tw) / 2, H * 0.14), txt, font=f, fill=(170, 235, 140))
    return {'img': im, 'ppu': ppu, 'O': (-0.001, 6, 11 * PL), 'A': (0, -1, 0), 'B': (0, 0, -1), 'normal': (-1, 0, 0)}


def main(out):
    decs = [side_decal(), wheel_decal(), front_decal()]
    iso = render(36, 20, 26, 2, decs)
    side = render(90, 0, 18, 2, decs, pad=0.8)
    frnt = render(0, 0, 40, 2, decs, pad=0.8)

    Wc = 2200
    sheet = Image.new('RGB', (Wc, 1900), (255, 255, 255))
    ft = font(HELV, 54, 1); fs = font(HELV, 30); fm = font(HELV, 26)
    d = ImageDraw.Draw(sheet)
    d.text((70, 44), 'Wieslauftalbahn VT 451 (Regio-Shuttle RS1) als Lego-Modell', font=ft, fill=(20, 24, 32))
    d.text((70, 118), 'Konzeptbild v2, Maßstab ca. 1:45: 70 Noppen lang (ca. 56 cm), 8 breit, 26 Platten hoch (ca. 8,7 Steine)', font=fs, fill=(90, 96, 104))

    def fit(im, maxw, maxh):
        r = min(maxw / im.width, maxh / im.height)
        return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)

    iso_f = fit(iso, Wc - 140, 940)
    sheet.paste(iso_f, ((Wc - iso_f.width) // 2, 180))
    y = 180 + iso_f.height + 30
    d.text((70, y), 'Seitenansicht', font=fs, fill=(90, 96, 104))
    side_f = fit(side, 1500, 380)
    sheet.paste(side_f, (70, y + 46))
    d.text((1650, y), 'Vorderansicht', font=fs, fill=(90, 96, 104))
    fr_f = fit(frnt, 480, 400)
    sheet.paste(fr_f, (1650, y + 46))
    yb = y + 46 + max(side_f.height, fr_f.height) + 24
    d.text((70, yb), 'Gelb und Blau nach den Fotos. Fenster, Türen und Wiesel sind eine Näherung, Teile und Stabilität sind noch nicht geprüft.', font=fm, fill=(120, 126, 134))
    sheet = sheet.crop((0, 0, Wc, yb + 70))
    sheet.save(out)
    print('gespeichert', out, sheet.size, 'Voxel:', len(vox))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'lego_wiesel_konzept.png')
