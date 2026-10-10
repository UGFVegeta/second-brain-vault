#!/usr/bin/env python3
"""LDraw-Vorschau-Renderer (orthografisch, Z-Buffer, Flat-Shading) mit Teilebibliothek aus BrickLink Studio.

Aufruf:
  ldr_render.py modell.ldr ausgabe.png [--view iso|front|side|back|top|iso2] [--width 1800] [--ss 2]
Als Modul:
  from ldr_render import load_model, render, part_info
"""
import os, sys, re, math, subprocess, tempfile, argparse
import numpy as np
from PIL import Image

LIB = '/Applications/Studio 2.0/ldraw'
HERE = os.path.dirname(os.path.abspath(__file__))
C_SRC = os.path.join(HERE, 'ldr_raster.c')
C_BIN = os.path.join(HERE, '.ldr_raster')
LOWRES = False

# ---------- Farben ----------
COLORS = {}


def _load_colors():
    pat = re.compile(r'!COLOUR\s+\S+\s+CODE\s+(\d+)\s+VALUE\s+#([0-9A-Fa-f]{6})\s+EDGE\s+#([0-9A-Fa-f]{6})')
    with open(os.path.join(LIB, 'LDConfig.ldr'), errors='ignore') as f:
        for line in f:
            m = pat.search(line)
            if m:
                c = int(m.group(1))
                v = m.group(2)
                COLORS[c] = tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


_load_colors()


def color_rgb(code):
    if code in COLORS:
        return COLORS[code]
    if code >= 0x2000000:
        v = code & 0xFFFFFF
        return ((v >> 16) & 255, (v >> 8) & 255, v & 255)
    return (160, 160, 160)


# ---------- Dateien ----------
_cache = {}


def find_file(name):
    n = name.replace('\\', '/').lower().strip()
    cands = []
    if LOWRES:
        cands.append(f'{LIB}/p/8/{n}')
    cands += [f'{LIB}/parts/{n}', f'{LIB}/p/{n}', f'{LIB}/{n}', f'{LIB}/parts/s/{n}', f'{LIB}/LEGO/parts/{n}', f'{LIB}/UnOfficial/parts/{n}']
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


def _xform(arr, M, t):
    return arr @ M.T + t


def load_file(name, path=None):
    """Liefert dict(tris (N,3,3), col (N,), stud (N,), lines (M,2,3)) in lokalen Koordinaten; Farbe 16 = erbt."""
    key = name.lower() if path is None else path
    if key in _cache:
        return _cache[key]
    p = path or find_file(name)
    res = dict(tris=np.zeros((0, 3, 3), np.float32), col=np.zeros(0, np.int32), stud=np.zeros(0, bool),
               lines=np.zeros((0, 2, 3), np.float32))
    if p is None:
        _cache[key] = res
        return res
    is_stud = os.path.basename(p).lower().startswith('stud')
    T, C, S, Ln = [], [], [], []
    with open(p, errors='ignore') as f:
        for raw in f:
            tok = raw.split()
            if not tok:
                continue
            t = tok[0]
            if t == '1' and len(tok) >= 15:
                col = int(tok[1])
                v = np.array(tok[2:14], dtype=np.float64)
                M = v[3:12].reshape(3, 3)
                tr = v[0:3]
                sub = load_file(' '.join(tok[14:]))
                if len(sub['tris']):
                    T.append(_xform(sub['tris'].reshape(-1, 3), M, tr).reshape(-1, 3, 3))
                    c = sub['col'].copy()
                    if col != 16:
                        c[c == 16] = col
                    C.append(c)
                    S.append(sub['stud'] | (os.path.basename(' '.join(tok[14:]).replace('\\', '/')).lower().startswith('stud')))
                if len(sub['lines']):
                    Ln.append(_xform(sub['lines'].reshape(-1, 3), M, tr).reshape(-1, 2, 3))
            elif t == '3' and len(tok) >= 11:
                col = int(tok[1]); v = np.array(tok[2:11], dtype=np.float64).reshape(3, 3)
                T.append(v[None]); C.append(np.array([col], np.int32)); S.append(np.array([is_stud]))
            elif t == '4' and len(tok) >= 14:
                col = int(tok[1]); v = np.array(tok[2:14], dtype=np.float64).reshape(4, 3)
                T.append(np.stack([v[[0, 1, 2]], v[[0, 2, 3]]])); C.append(np.array([col, col], np.int32))
                S.append(np.array([is_stud, is_stud]))
            elif t == '2' and len(tok) >= 8:
                v = np.array(tok[2:8], dtype=np.float64).reshape(2, 3)
                Ln.append(v[None])
    if T:
        res['tris'] = np.concatenate(T).astype(np.float32)
        res['col'] = np.concatenate(C)
        res['stud'] = np.concatenate(S)
    if Ln:
        res['lines'] = np.concatenate(Ln).astype(np.float32)
    _cache[key] = res
    return res


def parse_model(path):
    """Liest .ldr/.mpd (nur Hauptmodell, Typ-1-Zeilen). Gibt Liste (farbe, M(3x3), t(3), teilname)."""
    parts = []
    with open(path, errors='ignore') as f:
        for raw in f:
            tok = raw.split()
            if tok and tok[0] == '1' and len(tok) >= 15:
                col = int(tok[1])
                v = np.array(tok[2:14], dtype=np.float64)
                parts.append((col, v[3:12].reshape(3, 3), v[0:3], ' '.join(tok[14:])))
    return parts


def part_geometry(name, include_studs=True):
    g = load_file(name)
    if include_studs:
        return g['tris']
    return g['tris'][~g['stud']]


def part_info(name):
    """Koerper-Bounding-Box ohne Noppen in LDU: (min(3), max(3))."""
    g = load_file(name)
    tr = g['tris'][~g['stud']]
    if not len(tr):
        tr = g['tris']
    pts = tr.reshape(-1, 3)
    return pts.min(0), pts.max(0)


def build_scene(parts):
    T, C, Ln, LC = [], [], [], []
    for col, M, t, name in parts:
        g = load_file(name)
        if len(g['tris']):
            T.append(_xform(g['tris'].reshape(-1, 3), M, t).reshape(-1, 3, 3))
            c = g['col'].copy(); c[c == 16] = col
            C.append(c)
        if len(g['lines']):
            Ln.append(_xform(g['lines'].reshape(-1, 3), M, t).reshape(-1, 2, 3))
            LC.append(np.full(len(g['lines']), col, np.int32))
    tris = np.concatenate(T) if T else np.zeros((0, 3, 3), np.float32)
    cols = np.concatenate(C) if C else np.zeros(0, np.int32)
    lines = np.concatenate(Ln) if Ln else np.zeros((0, 2, 3), np.float32)
    lcols = np.concatenate(LC) if LC else np.zeros(0, np.int32)
    return tris, cols, lines, lcols


# ---------- Kamera ----------
VIEWS = {  # theta, phi
    'iso': (36, 20), 'iso2': (-140, 22), 'front': (0, 0), 'side': (90, 0), 'back': (180, 0), 'top': (90, 89.9),
    'front3q': (20, 14),
}


def cam(theta, phi):
    t, p = math.radians(theta), math.radians(phi)
    # LDraw (x, y runter, z) -> Welt (X=x, Y=z, Z=-y)
    r = np.array([math.sin(t), -math.cos(t), 0.0])
    u = np.array([math.sin(p) * math.cos(t), math.sin(p) * math.sin(t), math.cos(p)])
    d = np.array([math.cos(p) * math.cos(t), math.cos(p) * math.sin(t), -math.sin(p)])
    return r, u, d


def to_world(P):
    return np.stack([P[..., 0], P[..., 2], -P[..., 1]], -1)


def ensure_c():
    if not os.path.isfile(C_BIN) or os.path.getmtime(C_BIN) < os.path.getmtime(C_SRC):
        subprocess.check_call(['cc', '-O2', '-o', C_BIN, C_SRC])


def render(parts, theta=36, phi=20, width=1800, ss=2, bg=((246, 248, 250), (226, 231, 236)), pad=30, light=(0.45, 0.50, 0.75), decals=(), extent_parts=None):
    tris, cols, lines, lcols = build_scene(parts)
    if not len(tris):
        raise SystemExit('leeres Modell')
    r, u, d = cam(theta, phi)
    W3 = to_world(tris.reshape(-1, 3).astype(np.float64))
    sx = W3 @ r; sy = -(W3 @ u); sd = W3 @ d
    if extent_parts is not None:
        et = build_scene(extent_parts)[0]
        EW = to_world(et.reshape(-1, 3).astype(np.float64))
        ex, ey = EW @ r, -(EW @ u)
    else:
        ex, ey = sx, sy
    x0, x1, y0, y1 = ex.min() - pad, ex.max() + pad, ey.min() - pad, ey.max() + pad
    scale = width * ss / (x1 - x0)
    Wp, Hp = int(width * ss), int((y1 - y0) * scale)
    # Dreiecke
    n = len(tris)
    X = ((sx - x0) * scale).reshape(n, 3); Y = ((sy - y0) * scale).reshape(n, 3); Z = sd.reshape(n, 3)
    Wt = W3.reshape(n, 3, 3)
    nrm = np.cross(Wt[:, 1] - Wt[:, 0], Wt[:, 2] - Wt[:, 0])
    ln_ = np.linalg.norm(nrm, axis=1); ln_[ln_ == 0] = 1
    nrm = nrm / ln_[:, None]
    # zur Kamera drehen
    facing = (nrm @ d) > 0
    nrm[facing] *= -1
    L = np.array(light, dtype=np.float64)
    # Licht in Weltkoordinaten: x=rechts(Kamera), y=hoch, z=zum Betrachter
    Lw = L[0] * r + L[1] * u + L[2] * (-d)
    Lw /= np.linalg.norm(Lw)
    lam = np.clip(nrm @ Lw, 0, 1)
    base = np.array([color_rgb(int(c)) for c in range(0)], dtype=np.float64)
    uniq = np.unique(cols)
    lut = {int(c): np.array(color_rgb(int(c)), dtype=np.float64) for c in uniq}
    rgb = np.stack([lut[int(c)] for c in cols]) if n < 0 else None
    cidx = np.searchsorted(uniq, cols)
    ulut = np.stack([lut[int(c)] for c in uniq])
    rgb = ulut[cidx] * (0.58 + 0.50 * lam)[:, None]
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    tri_rec = np.zeros(n, dtype=[('v', '<f4', 9), ('c', 'u1', 4)])
    tri_rec['v'] = np.stack([X[:, 0], Y[:, 0], Z[:, 0], X[:, 1], Y[:, 1], Z[:, 1], X[:, 2], Y[:, 2], Z[:, 2]], 1)
    tri_rec['c'][:, :3] = rgb
    # Linien
    m = len(lines)
    if m:
        LW = to_world(lines.reshape(-1, 3).astype(np.float64))
        lx = ((LW @ r - x0) * scale).reshape(m, 2); ly = ((-(LW @ u) - y0) * scale).reshape(m, 2); lz = (LW @ d).reshape(m, 2)
        lin_rec = np.zeros(m, dtype=[('v', '<f4', 6), ('c', 'u1', 4)])
        lin_rec['v'] = np.stack([lx[:, 0], ly[:, 0], lz[:, 0], lx[:, 1], ly[:, 1], lz[:, 1]], 1)
        ecol = np.array([color_rgb(int(c)) for c in lcols], dtype=np.float64) * 0.38
        lin_rec['c'][:, :3] = np.clip(ecol, 0, 255).astype(np.uint8)
    else:
        lin_rec = np.zeros(0, dtype=[('v', '<f4', 6), ('c', 'u1', 4)])
    ensure_c()
    with tempfile.TemporaryDirectory() as td:
        fin, fout = os.path.join(td, 'in.bin'), os.path.join(td, 'out.rgb')
        with open(fin, 'wb') as f:
            f.write(np.array([Wp, Hp, n, m], dtype='<i4').tobytes())
            f.write(tri_rec.tobytes()); f.write(lin_rec.tobytes())
        subprocess.check_call([C_BIN, fin, fout])
        buf = np.fromfile(fout, dtype=np.uint8).reshape(Hp, Wp, 4)
    img = Image.new('RGB', (Wp, Hp))
    # Hintergrund-Verlauf
    grad = np.linspace(0, 1, Hp)[:, None, None]
    bgarr = (np.array(bg[0])[None, None, :] * (1 - grad) + np.array(bg[1])[None, None, :] * grad)
    bgarr = np.broadcast_to(bgarr, (Hp, Wp, 3))
    mask = buf[..., 3:4] > 0
    arr = np.where(mask, buf[..., :3], bgarr).astype(np.uint8)
    img = Image.fromarray(arr).convert('RGBA')
    for dec in decals:
        n = np.array(dec['normal'], dtype=float)
        if n @ d > -0.05:
            continue
        im, ppu = dec['img'], dec['ppu']
        O, A, B = [np.array(dec[k], dtype=float) for k in ('O', 'A', 'B')]
        o = np.array([O @ r - x0, -(O @ u) - y0]) * scale
        fa = np.array([A @ r, -(A @ u)]) * scale / ppu
        fb = np.array([B @ r, -(B @ u)]) * scale / ppu
        F = np.stack([fa, fb], 1)
        if abs(np.linalg.det(F)) < 1e-9:
            continue
        Fi = np.linalg.inv(F)
        c = -Fi @ o
        layer = im.transform((Wp, Hp), Image.AFFINE, (Fi[0, 0], Fi[0, 1], c[0], Fi[1, 0], Fi[1, 1], c[1]), resample=Image.BILINEAR)
        img = Image.alpha_composite(img, layer)
    return img.convert('RGB').resize((Wp // ss, Hp // ss), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ldr'); ap.add_argument('out')
    ap.add_argument('--view', default='iso'); ap.add_argument('--width', type=int, default=1800)
    ap.add_argument('--ss', type=int, default=2); ap.add_argument('--lowres', action='store_true')
    a = ap.parse_args()
    global LOWRES
    LOWRES = a.lowres
    th, ph = VIEWS[a.view]
    parts = parse_model(a.ldr)
    img = render(parts, th, ph, a.width, a.ss)
    img.save(a.out)
    print('gespeichert', a.out, img.size, 'Teile:', len(parts))


if __name__ == '__main__':
    main()
