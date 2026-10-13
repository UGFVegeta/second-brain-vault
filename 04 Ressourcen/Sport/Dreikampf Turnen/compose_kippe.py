"""Baut die Bildreihe "Kippe in den Grätschsitz" aus den offiziellen BJS-Figuren (Ü7 Barren und Ü4 Barren).
Aufruf im Projektordner: python3 compose_kippe.py
Braucht alt/bilder-original/barren-ue7.png und barren-ue4.png (unveränderte Bilder aus dem BJS-Handbuch).
Schreibt alt/bilder-original/barren-kippe.png (ohne Kontur) und bilder/barren-kippe.png (mit Kontur)."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np
from collections import Counter

a = Image.open('alt/bilder-original/barren-ue7.png').convert('RGBA')
b = Image.open('alt/bilder-original/barren-ue4.png').convert('RGBA')
A = np.asarray(a)
row = [tuple(A[122, x][:3]) for x in range(923) if A[122, x][3] > 250 and A[122, x][0] > 200 and A[122, x][1] > 120]
rail_col = tuple(int(v) for v in Counter(row).most_common(1)[0][0])
mat_col = tuple(int(v) for v in A[200, 300][:3])

S = a.crop((548, 100, 583, 192)).transpose(Image.FLIP_LEFT_RIGHT)  # Stand am Boden, Hände am Holm, schaut in Bewegungsrichtung
K1 = a.crop((153, 56, 357, 134))                 # Kippen, Beine hoch (Ü7)
k1 = np.asarray(K1).copy(); k1[70:, 197:, 3] = 0  # Reste der Nachbarfigur
K1 = Image.fromarray(k1, 'RGBA')
SHIFT = 33                                        # vierte Figur ganz unter den Holm
f6 = K1.crop((94, 19, 148, 77))                   # Phase mit engem Hüftwinkel (Ü7)
f6a = np.asarray(f6).astype(int).copy()
f6a[np.abs(f6a[:, :, :3] - np.array(rail_col)).sum(axis=2) < 22, 3] = 0   # Holmreste entfernen
rr, gg, bb_ = f6a[:, :, 0], f6a[:, :, 1], f6a[:, :, 2]
orange = (rr > 195) & (bb_ < 175) & (gg > 110) & ((rr - bb_) > 50)
orange[:38, :] = False; orange[54:, :] = False        # nur die Zeilen des Holms
f6a[orange, 3] = 0
f6 = Image.fromarray(f6a.astype('uint8'), 'RGBA')
k1 = np.asarray(K1).copy(); k1[19:77, 94:148, 3] = 0
K1 = Image.fromarray(k1, 'RGBA')
ext = Image.new('RGBA', (K1.width, K1.height + 44), (0, 0, 0, 0))
ext.alpha_composite(K1, (0, 0))
ext.alpha_composite(f6, (94, 19 + SHIFT))
K1 = ext
K2 = a.crop((357, 56, 372, 86))                  # Fußspitze und Pfeil
sit = b.crop((205, 45, 286, 142))                # Grätschsitz (Ü4), an Ü7-Figur angepasst
arr = np.asarray(sit).astype(int).copy()


def swap(arr, src, dst, tol):
    d = np.abs(arr[:, :, :3] - np.array(src)).sum(axis=2)
    m = (d < tol) & (arr[:, :, 3] > 0)
    arr[m, :3] = dst


swap(arr, (250, 210, 194), (172, 120, 98), 60)
swap(arr, (86, 52, 36), (8, 8, 8), 70)
arr[82:, :16, 3] = 0
arr[:68, 40:, 3] = 0
s = 0.85
sit = Image.fromarray(arr.astype('uint8'), 'RGBA')
sit = sit.resize((int(sit.width * s), int(sit.height * s)), Image.LANCZOS)

GAP = 14
xS = 10
xK = xS + S.width + GAP
xSit = xK + K1.width + K2.width + GAP - 6
W = xSit + sit.width + 12
cv = Image.new('RGBA', (W, 207), (0, 0, 0, 0))
d = ImageDraw.Draw(cv)
d.rectangle((0, 120, W - 1, 123), fill=rail_col + (255,))
d.rectangle((4, 124, 9, 189), fill=(91, 168, 216, 255))
d.rectangle((W - 12, 124, W - 7, 189), fill=(91, 168, 216, 255))
d.rectangle((0, 189, W - 1, 206), fill=mat_col + (255,))
# Holm beginnt erst vor dem Barren: der erste Junge steht davor und greift die Holmenden
xRail = xS + S.width - 8
cv.paste((0, 0, 0, 0), (0, 120, xRail, 124))
cv.paste((0, 0, 0, 0), (4, 124, 10, 190))
d.rectangle((xRail + 2, 124, xRail + 7, 189), fill=(91, 168, 216, 255))
cv.alpha_composite(S, (xS, 100))
cv.alpha_composite(K1, (xK, 56))
cv.alpha_composite(K2, (xK + K1.width, 56))
skin = (172, 120, 98, 255)
for ax, bx in ((xK + 94 + 17, xK + 94 + 20), (xK + 94 + 25, xK + 94 + 28)):   # Arme von der vierten Figur zum Holm
    d.line((ax, 123, bx, 100 + SHIFT + 4), fill=skin, width=3)
    d.ellipse((ax - 2, 120, ax + 3, 125), fill=skin)
cv.alpha_composite(sit, (xSit, 122 - int((122 - 45) * s) - 1))
cv = cv.crop(cv.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
cv.save('alt/bilder-original/barren-kippe.png')

big = cv.resize((cv.width * 2, cv.height * 2), Image.LANCZOS)
Am = big.getchannel('A').point(lambda v: 255 if v > 40 else 0)
outer = Am.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(0.7)).point(lambda v: 255 if v > 110 else 0)
base = Image.new('RGBA', big.size, (20, 22, 30, 0))
base.putalpha(outer)
comp = Image.new('RGB', big.size, 'white')
comp.paste(big, mask=big.getchannel('A'))
g = comp.convert('L').filter(ImageFilter.GaussianBlur(0.8))
e = g.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 32 else 0).filter(ImageFilter.MaxFilter(3))
e = ImageChops.multiply(e, Am)
res = Image.alpha_composite(base, big)
dark = Image.new('RGBA', big.size, (20, 22, 30, 255))
Image.composite(dark, res, e).save('bilder/barren-kippe.png')
print('ok', cv.size)
