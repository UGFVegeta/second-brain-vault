#!/usr/bin/env python3
"""Bauanleitung (PDF) fuer das Wiesel-Modell: je Lage ein Schritt, neue Teile farbig, bisheriges gedaempft.
Aufruf: python3 lego_wiesel_anleitung.py <ausgabe.pdf>
"""
import os, sys, re, collections
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import io


def jpg(img, q=84):
    buf = io.BytesIO(); img.convert('RGB').save(buf, 'JPEG', quality=q); buf.seek(0)
    return ImageReader(buf)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ldr_render as R
import lego_wiesel_bau as B

KIND_DE = {'boden': 'Boden', 'wand': 'Seitenwände', 'kopf': 'Stirnseite', 'scheibe': 'Frontscheibe', 'pfosten': 'Seitenpfosten',
           'dach': 'Dach', 'kante': 'Dachkanten', 'klima': 'Klimaanlage', 'unterflur': 'Unterflur', 'drehgestell': 'Drehgestellrahmen',
           'lampe': 'Scheinwerfer', 'lampe_fliese': 'Scheinwerfer-Fliesen', 'anzeige': 'Zugziel-Anzeige'}
COLNAME = {}
for line in open(os.path.join(R.LIB, 'LDConfig.ldr'), errors='ignore'):
    m = re.search(r'!COLOUR\s+(\S+)\s+CODE\s+(\d+)', line)
    if m:
        COLNAME[int(m.group(2))] = m.group(1).replace('_', ' ')
COL_DE = {'Black': 'Schwarz', 'Blue': 'Blau', 'Yellow': 'Gelb', 'White': 'Weiß', 'Light Bluish Gray': 'Hellgrau', 'Dark Bluish Gray': 'Dunkelgrau',
          'Dark Blue': 'Dunkelblau'}


def partname(pid):
    try:
        with open(R.find_file(pid + '.dat'), errors='ignore') as f:
            return re.sub(r'\s+', ' ', f.readline()[2:].strip())
    except Exception:
        return pid


def muted(col):
    r, g, b = R.color_rgb(col)
    k = 0.55
    r, g, b = [int(v * (1 - k) + 208 * k) for v in (r, g, b)]
    return 0x2000000 | (r << 16) | (g << 8) | b


def as_parts(items, mute=False):
    return [(muted(p['col']) if mute else p['col'], p['M'], p['t'], p['pid'] + '.dat') for p in items]


_thumb = {}


def thumb(pid, col):
    key = (pid, col)
    if key not in _thumb:
        part = [(col, np.eye(3), np.zeros(3), pid + '.dat')]
        _thumb[key] = R.render(part, 36, 28, 150, 3, pad=6, bg=((250, 251, 252), (238, 241, 244)))
    return _thumb[key]


def main(out):
    B.build_all()
    steps = collections.defaultdict(list)
    for p in B.placed:
        steps[p['k0'] if p['kind'] != 'lampe_fliese' else 7].append(p)
    groups, cur, curn = [], [], 0
    for k in sorted(steps):
        cur.append(k); curn += len(steps[k])
        if curn >= 12:
            groups.append(cur); cur, curn = [], 0
    if cur:
        if groups and curn < 6:
            groups[-1] += cur
        else:
            groups.append(cur)
    ks = list(range(len(groups)))
    allparts = as_parts(B.placed)
    N = len(ks)
    W, H = landscape(A4)
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle('Bauanleitung Wieslauftalbahn VT 451 (Lego)')
    M = 26

    # Deckblatt
    sheet = Image.open(os.path.join(os.path.dirname(out), 'Bildtafel.png')) if os.path.exists(os.path.join(os.path.dirname(out), 'Bildtafel.png')) else None
    c.setFont('Helvetica-Bold', 26); c.drawString(M, H - 50, 'Wieslauftalbahn VT 451 (Regio-Shuttle RS1)')
    c.setFont('Helvetica', 13)
    c.drawString(M, H - 72, f'Lego-Modell, Maßstab ca. 1:45, 70 Noppen lang (ca. 56 cm), 8 breit. {len(B.placed)} Teile in {N} Bauschritten.')
    if sheet:
        r = min((W - 2 * M) / sheet.width, (H - 130) / sheet.height)
        c.drawImage(jpg(sheet), M, 40, sheet.width * r, sheet.height * r)
    c.setFont('Helvetica', 9)
    c.drawString(M, 24, 'Entwurf, nicht als Gesamtmodell gebaut. Räder und Drehgestell fehlen, Wiesel und Schriftzüge sind Aufkleber.')
    c.showPage()

    done = []
    # Kamera: feste Ausschnitte ueber das ganze Modell
    for i, k in enumerate(ks, 1):
        new = [p for kk in groups[k] for p in steps[kk]]
        parts_all = as_parts(done, mute=True) + as_parts(new)
        v1 = R.render(parts_all, 20, 16, 1300, 2, extent_parts=allparts, pad=12)
        v2 = R.render(parts_all, 200, 16, 1300, 2, extent_parts=allparts, pad=12)
        kinds = collections.Counter(p['kind'] for p in new)
        title = ', '.join(KIND_DE.get(kk, kk) for kk, _ in kinds.most_common())
        c.setFont('Helvetica-Bold', 17); c.drawString(M, H - 40, f'Schritt {i} von {N}')
        c.setFont('Helvetica', 11); c.setFillGray(0.35)
        lv = groups[k]; lab = f'Lage {lv[0]}' if len(lv) == 1 else f'Lage {lv[0]} bis {lv[-1]}'
        c.drawString(M + 150, H - 40, f'{lab}: {title}   ({len(new)} neue Teile)')
        c.setFillGray(0)
        wimg = (W - 2 * M - 14) / 2
        for j, v in enumerate((v1, v2)):
            r = wimg / v.width
            c.drawImage(jpg(v), M + j * (wimg + 14), H - 62 - v.height * r, wimg, v.height * r)
        ytab = H - 62 - max(v1.height, v2.height) * (wimg / v1.width) - 10
        # Teiletabelle
        cnt = collections.Counter((p['pid'], p['col']) for p in new)
        items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
        n = len(items)
        cell = 74 if n <= 22 else 60
        percol = int((W - 2 * M) // (cell + 8))
        c.setFont('Helvetica-Bold', 9); c.drawString(M, ytab, 'Neue Teile')
        x = M; y = ytab - 8
        for (pid, col), num in items:
            if x + cell > W - M + 1:
                x = M; y -= cell + 30
            if y - cell < 20:
                c.showPage(); y = H - 60; x = M
            th = thumb(pid, col)
            rr = (cell - 6) / max(th.width, th.height)
            c.drawImage(jpg(th, 90), x, y - th.height * rr, th.width * rr, th.height * rr)
            c.setFont('Helvetica-Bold', 9); c.drawString(x, y - cell + 2, f'{num}x')
            cname = COL_DE.get(COLNAME.get(col, str(col)), COLNAME.get(col, str(col)))
            c.setFont('Helvetica', 6.5); c.drawString(x, y - cell - 7, f'{pid}  {cname}'[:20])
            c.drawString(x, y - cell - 14, partname(pid.split('c0')[0] if pid.endswith(('c01', 'c02')) else pid)[:26])
            x += cell + 8
        done += new
        c.showPage()

    # Gesamtteileliste
    cntall = collections.Counter((p['pid'], p['col']) for p in B.placed)
    items = sorted(cntall.items(), key=lambda kv: (kv[0][0], kv[0][1]))
    c.setFont('Helvetica-Bold', 17); c.drawString(M, H - 40, f'Alle Teile ({len(B.placed)} Stück, {len(items)} Teile/Farb-Kombinationen)')
    cell = 60; per = int((W - 2 * M) // (cell + 8))
    x = M; y = H - 60
    for (pid, col), num in items:
        if x + cell > W - M + 1:
            x = M; y -= cell + 28
        if y - cell < 24:
            c.showPage(); y = H - 40; x = M
        th = thumb(pid, col)
        rr = (cell - 6) / max(th.width, th.height)
        c.drawImage(jpg(th, 90), x, y - th.height * rr, th.width * rr, th.height * rr)
        c.setFont('Helvetica-Bold', 9); c.drawString(x, y - cell + 2, f'{num}x')
        cname = COL_DE.get(COLNAME.get(col, str(col)), COLNAME.get(col, str(col)))
        c.setFont('Helvetica', 6.5); c.drawString(x, y - cell - 7, f'{pid}  {cname}'[:20])
        c.drawString(x, y - cell - 14, partname(pid.split('c0')[0] if pid.endswith(('c01', 'c02')) else pid)[:26])
        x += cell + 8
    c.showPage()
    c.save()
    print('PDF:', out, 'Schritte', N, 'Teile', len(B.placed))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'Bauanleitung.pdf')
