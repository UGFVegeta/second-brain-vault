"""Baut die Sprung-Bilder Ü5 (Kasten quer) und Ü6 (Sprungtisch) aus den BJS-Bildern.
Aufruf im Projektordner: python3 compose_sprung.py
Braucht alt/bilder-original/sprung-ue5.png (Bock), sprung-ue2.png (Kasten), sprung-ue7.png (Sprungtisch).
Schreibt alt/bilder-original/sprung-ue5-kasten.png und sprung-ue6-sprungtisch.png (ohne Kontur) sowie
bilder/sprung-ue5.png und bilder/sprung-ue6.png (mit Kontur)."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

D = 'alt/bilder-original/'
u5 = Image.open(D + 'sprung-ue5.png').convert('RGBA')
u2 = np.asarray(Image.open(D + 'sprung-ue2.png').convert('RGBA'))
u7 = Image.open(D + 'sprung-ue7.png').convert('RGBA')
W, H = u5.size
a5 = np.asarray(u5).astype(int)


def near(rgb, col, tol):
    return np.abs(rgb - np.array(col)).sum(axis=2) < tol


# --- Bock aus dem Ü5-Bild entfernen (Polster, Beine, Füße; auch die blasse Kopie) ---
rgb = a5[:, :, :3]
mask = np.zeros((H, W), bool)
for (x0, x1) in ((205, 340), (390, 505)):
    reg = np.zeros((H, W), bool)
    reg[95:256, x0:x1] = True
    pad = near(rgb, (201, 135, 85), 45)
    leg = near(rgb, (245, 186, 128), 45) | near(rgb, (232, 177, 121), 45)
    shin = near(rgb, (191, 191, 191), 30) | near(rgb, (230, 230, 230), 20) | near(rgb, (205, 205, 205), 30)
    foot = near(rgb, (87, 87, 86), 35)
    low = np.zeros((H, W), bool); low[200:, :] = True
    mask |= reg & (pad | leg | ((shin | foot) & low))
mask[108:256, 390:498] = True                       # echter Bock: alles weg (keine Figur in diesem Bereich)
ghost = np.zeros((H, W), bool); ghost[95:256, 205:340] = True
mask |= ghost & (a5[:, :, 3] < 200)                  # blasse Kopie des Bocks (halbtransparent)
holes = a5.copy()
holes[mask, 3] = 0
base = Image.fromarray(holes.astype('uint8'), 'RGBA')


def kasten(cx, alpha):
    """Kasten quer (Seitenansicht), Farben aus dem Ü2-Bild."""
    body = tuple(int(v) for v in u2[240, 400][:3])
    cap = tuple(int(v) for v in u2[201, 400][:3])
    stripe = tuple(int(v) for v in u2[262, 400][:3])
    foot = tuple(int(v) for v in u2[288, 495][:3])
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, x1, top, bot = cx - 40, cx + 40, 100, 246
    d.rectangle((x0, top, x1, bot - 10), fill=body + (255,))
    for yy in (top + 50, top + 100):
        d.rectangle((x0, yy, x1, yy + 2), fill=stripe + (255,))
    d.rectangle((x0 - 2, top, x1 + 2, top + 9), fill=cap + (255,))
    d.rectangle((x0 + 2, bot - 10, x0 + 16, bot), fill=foot + (255,))
    d.rectangle((x1 - 16, bot - 10, x1 - 2, bot), fill=foot + (255,))
    if alpha < 255:
        a = np.asarray(lay).astype(int)
        a[:, :, 3] = a[:, :, 3] * alpha // 255
        lay = Image.fromarray(a.astype('uint8'), 'RGBA')
    return lay


def sprungtisch(cx, alpha, scale=1.17):
    """Sprungtisch aus dem Ü7-Bild herausgelöst (nur Geräte-Farben)."""
    box = (280, 165, 410, 298)
    reg = np.asarray(u7.crop(box)).astype(int).copy()
    rgb7 = reg[:, :, :3]
    tan = near(rgb7, (220, 184, 138), 45)
    blue = near(rgb7, (85, 165, 215), 55) | near(rgb7, (60, 135, 180), 55) | near(rgb7, (0, 74, 166), 60)
    grey = near(rgb7, (225, 225, 230), 40) | near(rgb7, (190, 190, 195), 40)
    keep = (tan | blue | grey) & (reg[:, :, 3] > 100)
    reg[~keep, 3] = 0
    t = Image.fromarray(reg.astype('uint8'), 'RGBA')
    t = t.resize((int(t.width * scale), int(t.height * scale)), Image.LANCZOS)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # Fuß des Sprungtischs auf Bodenhöhe 250, Oberkante des Tisches auf etwa 100
    ox = cx - t.width // 2 - int(15 * scale)
    oy = 250 - t.height
    lay.alpha_composite(t, (ox, oy))
    if alpha < 255:
        a = np.asarray(lay).astype(int)
        a[:, :, 3] = a[:, :, 3] * alpha // 255
        lay = Image.fromarray(a.astype('uint8'), 'RGBA')
    return lay


def outline(img, out):
    big = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    A = big.getchannel('A').point(lambda v: 255 if v > 150 else 0)
    outer = A.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(0.7)).point(lambda v: 255 if v > 110 else 0)
    b = Image.new('RGBA', big.size, (20, 22, 30, 0)); b.putalpha(outer)
    comp = Image.new('RGB', big.size, 'white'); comp.paste(big, mask=big.getchannel('A'))
    g = comp.convert('L').filter(ImageFilter.GaussianBlur(0.8))
    e = g.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 32 else 0).filter(ImageFilter.MaxFilter(3))
    e = ImageChops.multiply(e, A)
    res = Image.alpha_composite(b, big)
    Image.composite(Image.new('RGBA', big.size, (20, 22, 30, 255)), res, e).save(out)


def compose(app_func, name_raw, name_out, green=False):
    fig = base
    if green:
        a = np.asarray(base).astype(int).copy()
        for src, tol in (((84, 166, 222), 70), ((80, 160, 208), 60), ((85, 165, 215), 60)):
            m = near(a[:, :, :3], src, tol) & (a[:, :, 3] > 0)
            a[m, :3] = (125, 158, 40)
        fig = Image.fromarray(a.astype('uint8'), 'RGBA')
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    lay.alpha_composite(app_func(445, 255))
    lay.alpha_composite(fig)
    lay.save(D + name_raw)
    outline(lay, 'bilder/' + name_out)


compose(kasten, 'sprung-ue5-kasten.png', 'sprung-ue5.png')
compose(sprungtisch, 'sprung-ue6-sprungtisch.png', 'sprung-ue6.png', green=True)
print('ok')

# gleiche Kontur-Regel für die übrigen Sprung-Bilder (blasse Geräte ohne dicken Rand)
for n in ('sprung-ue2', 'sprung-ue3', 'sprung-ue4', 'sprung-ue7'):
    outline(Image.open(D + n + '.png').convert('RGBA'), 'bilder/' + n + '.png')
print('ok 2')
