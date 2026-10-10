#!/usr/bin/env python3
"""Baut das Modell aus echten Teilen (lego_wiesel_bau), schreibt die LDraw-Datei und rendert eine Bildtafel.
Aufruf: python3 lego_wiesel_bilder.py <ordner>   (schreibt Wieslauftalbahn.ldr, Teileliste.csv, Bildtafel.png dorthin)
"""
import os, sys, collections, csv
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ldr_render as R
import lego_wiesel_bau as B
import lego_wiesel_modell as V

HELV = '/System/Library/Fonts/HelveticaNeue.ttc'


def font(size, idx=0):
    return ImageFont.truetype(HELV, size, index=idx)


def decals():
    sd = V.side_decal()
    zt = 20.0 * V.KTOP * V.PL
    front = dict(img=sd['img'], ppu=sd['ppu'], O=(0, 0, zt), A=(20, 0, 0), B=(0, 0, -20), normal=(0, -1, 0))
    back = dict(img=sd['img'], ppu=sd['ppu'], O=(20.0 * B.L, 160, zt), A=(-20, 0, 0), B=(0, 0, -20), normal=(0, 1, 0))
    return [front, back]


def fit(im, w, h):
    r = min(w / im.width, h / im.height)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    B.build_all()
    ldr = os.path.join(outdir, 'Wieslauftalbahn.ldr')
    B.write_ldr(ldr)
    cnt = collections.Counter((p['pid'], p['col']) for p in B.placed)
    with open(os.path.join(outdir, 'Teileliste.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['LDraw-Teil', 'LDraw-Farbe', 'Anzahl'])
        for (pid, col), n in sorted(cnt.items()):
            w.writerow([pid, col, n])
    comps, _ = B.connectivity()
    parts = R.parse_model(ldr)
    dec = decals()
    v1 = R.render(parts, 20, 14, 1500, 2, decals=dec)
    v2 = R.render(parts, 200, 14, 1500, 2, decals=dec)
    vs = R.render(parts, 90, 0, 2600, 2, decals=dec, pad=20)
    vf = R.render(parts, 0, 0, 700, 2, decals=dec, pad=20)
    vt = R.render(parts, 90, 89.9, 2600, 2, decals=dec, pad=20)

    Wc = 2400
    sheet = Image.new('RGB', (Wc, 4000), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    d.text((70, 44), 'Wieslauftalbahn VT 451 (Regio-Shuttle RS1) als Lego-Modell', font=font(56, 1), fill=(20, 24, 32))
    d.text((70, 120), f'Entwurf aus echten Teilen, Maßstab ca. 1:45: 70 Noppen lang (ca. 56 cm), 8 breit, 26 Platten hoch.', font=font(28), fill=(90, 96, 104))
    d.text((70, 158), f'{len(B.placed)} Teile in {len(cnt)} Teile/Farb-Kombinationen. Ohne Räder (Drehgestell in Studio ergänzen). Wiesel und Schriftzüge sind Aufkleber, nicht aus Steinen.', font=font(28), fill=(90, 96, 104))
    y = 215
    a = fit(v1, 1130, 1000); b = fit(v2, 1130, 1000)
    sheet.paste(a, (70, y)); sheet.paste(b, (70 + 1130 + 40, y))
    y += max(a.height, b.height) + 30
    d.text((70, y), 'Seitenansicht', font=font(30), fill=(90, 96, 104)); y += 44
    s = fit(vs, Wc - 140, 520); sheet.paste(s, (70, y)); y += s.height + 30
    d.text((70, y), 'Vorderansicht', font=font(30), fill=(90, 96, 104))
    d.text((820, y), 'Draufsicht', font=font(30), fill=(90, 96, 104)); y += 44
    f = fit(vf, 640, 560); sheet.paste(f, (70, y))
    t = fit(vt, 1500, 300); sheet.paste(t, (820, y))
    y += max(f.height, t.height) + 40
    sheet = sheet.crop((0, 0, Wc, y))
    sheet.save(os.path.join(outdir, 'Bildtafel.png'))
    print('fertig:', sheet.size, 'Teile', len(B.placed), 'Komponenten', len(comps))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
