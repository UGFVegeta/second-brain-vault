#!/usr/bin/env python3
"""Wieslauftalbahn VT 451 (Regio-Shuttle RS1) als Lego-Modell aus echten Teilen -> LDraw-Datei + Teileliste.

Gitter: x = Laenge (Front bei 0), y = Breite (0..7), k = Platten nach oben (Schienenoberkante k=0).
LDraw: X = 20*x, Z = 20*y, Y = -8*k (Y zeigt nach unten).
Aufruf: python3 lego_wiesel_bau.py <ausgabe.ldr> [stueckliste.csv]
"""
import os, sys, math, collections, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ldr_render as R
import lego_wiesel_modell as V   # Voxel-Entwurf: liefert die Farbverteilung der Seitenwand

L, W = 70, 8
K_DECK = 5          # Bodenplatte (blau) = Schuerze
K_WALL0, K_WALL1 = 6, 22     # Seitenwand k6..k22
K_ROOF_DECK = 23
CODE = {V.Y: 14, V.B: 1, V.WIN: 72, V.K: 0, V.G: 72, V.LG: 71, V.LAMP: 15}
YEL, BLU, BLK, DBG, LBG, WHT, DKB = 14, 1, 0, 72, 71, 15, 272

BR = {1: '3005', 2: '3004', 3: '3622', 4: '3010', 6: '3009', 8: '3008'}       # Steine 1xN
PL = {1: '3024', 2: '3023', 3: '3623', 4: '3710', 6: '3666', 8: '3460'}       # Platten 1xN

placed = []      # dict(pid, col, x0, y0, k0, wx, wy, hp, mat, t, studs(set of (x,y)), kind)
occ = {}         # (x,y,k) -> index in placed


# ---------- Platzierung ----------
def rotmat(r):
    c, s = [(1, 0), (0, 1), (-1, 0), (0, -1)][r % 4]
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)


_info = {}


def info(pid):
    if pid not in _info:
        lo, hi = R.part_info(pid + '.dat')
        g = R.load_file(pid + '.dat')
        tr = g['tris'][~g['stud']]
        pts = tr.reshape(-1, 3) if len(tr) else g['tris'].reshape(-1, 3)
        top = pts[pts[:, 1] <= lo[1] + 0.5]
        c = (lo + hi) / 2
        hd = np.array([top[:, 0].mean() - c[0], top[:, 2].mean() - c[2]]) if len(top) else np.zeros(2)
        st = g['tris'][g['stud']]
        stc = st.mean(1) if len(st) else np.zeros((0, 3))
        _info[pid] = dict(lo=lo, hi=hi, c=c, hd=hd, stud_centers=stc)
    return _info[pid]


def choose_rot(pid, wx, wy, hp, high=None, side=None):
    inf = info(pid)
    ext = inf['hi'] - inf['lo']
    best = None
    for r in range(4):
        Rm = rotmat(r)
        e = np.abs(Rm @ ext)
        if abs(e[0] - 20 * wx) < 1.5 and abs(e[2] - 20 * wy) < 1.5 and abs(ext[1] - 8 * hp) < 1.5:
            if side is not None:
                sd = Rm @ np.array([0, 0, -1.0])      # Seitennoppe zeigt lokal nach -z
                if sd[0] * side[0] + sd[2] * side[1] < 0.9:
                    continue
            score = 0.0
            if high is not None and np.linalg.norm(inf['hd']) > 1:
                hd = Rm @ np.array([inf['hd'][0], 0, inf['hd'][1]])
                score = hd[0] * high[0] + hd[2] * high[1]
            if best is None or score > best[0] + 1e-6:
                best = (score, r)
    if best is None:
        raise ValueError(f'{pid}: Masse {ext/ [20,8,20]} passen nicht zu {wx}x{wy}x{hp}')
    if high is not None and np.linalg.norm(inf['hd']) > 1 and best[0] < 1:
        raise ValueError(f'{pid}: Neigung passt nicht zur Richtung {high}')
    return best[1]


def put(pid, col, x0, y0, k0, wx, wy, hp, high=None, kind='teil', check=True, side=None):
    """Teil in Zellen [x0,x0+wx) x [y0,y0+wy) x [k0,k0+hp) setzen."""
    r = choose_rot(pid, wx, wy, hp, high, side)
    Rm = rotmat(r)
    inf = info(pid)
    target = np.array([20 * (x0 + wx / 2), -8 * (k0 + hp / 2), 20 * (y0 + wy / 2)])
    t = target - Rm @ inf['c']
    # Noppenzellen aus der Geometrie
    studs = set()
    for sc in inf['stud_centers']:
        p = Rm @ sc + t
        if p[1] < -8 * (k0 + hp) + 6 and abs(p[1] + 8 * (k0 + hp)) < 6.5:    # nur Noppen oben
            studs.add((int(math.floor(p[0] / 20)), int(math.floor(p[2] / 20))))
    idx = len(placed)
    cells = [(x, y, k) for x in range(x0, x0 + wx) for y in range(y0, y0 + wy) for k in range(k0, k0 + hp)]
    if check:
        for c in cells:
            if c in occ:
                raise ValueError(f'Kollision bei {c}: {pid} mit {placed[occ[c]]["pid"]}')
    for c in cells:
        occ[c] = idx
    placed.append(dict(pid=pid, col=col, x0=x0, y0=y0, k0=k0, wx=wx, wy=wy, hp=hp, M=Rm, t=t, studs=studs, kind=kind))
    return idx


# ---------- Seitenwand (1 Noppe dick) packen ----------
def partition(n, start, prev_seams, lens):
    """Zerlegt Laenge n in Stuecke aus lens; minimiert Stueckzahl, meidet Fugen der Lage darunter."""
    INF = 10 ** 9
    best = [INF] * (n + 1); back = [0] * (n + 1)
    best[0] = 0
    for i in range(1, n + 1):
        for l in lens:
            if l <= i and best[i - l] < INF:
                seam_pen = 6 if (start + i - l) in prev_seams and i - l > 0 else 0
                c = best[i - l] + 1 + seam_pen
                if c < best[i]:
                    best[i] = c; back[i] = l
    out = []; i = n
    while i > 0:
        out.append(back[i]); i -= back[i]
    out.reverse()
    return out


def wall_cells(y):
    cells = {}
    for k in range(K_WALL0, K_WALL1 + 1):
        for x in range(L):
            rel = min(x, L - 1 - x)
            if (rel <= 1 and 11 <= k <= 16) or (rel <= 2 and k >= 17):
                continue                    # hier sitzt die geneigte Front
            v = V.vox.get((x, 0, k))
            col = CODE.get(v, YEL) if v is not None else YEL
            if rel == 0 and k <= 9:
                col = BLU
            cells[(x, k)] = col
    return cells


def pack_wall(y):
    cells = wall_cells(y)
    done = set(); seams = collections.defaultdict(set)
    kmin = min(k for _, k in cells); kmax = max(k for _, k in cells)
    for k in range(kmin, kmax + 1):
        def brickable(x):
            c = cells.get((x, k))
            return c is not None and all(cells.get((x, k + d)) == c and (x, k + d) not in done for d in range(3))
        xs = sorted(x for (x, kk) in cells if kk == k and (x, k) not in done)
        i = 0
        while i < len(xs):
            x = xs[i]; col = cells[(x, k)]; bk = brickable(x)
            j = i
            while j + 1 < len(xs) and xs[j + 1] == xs[j] + 1 and cells[(xs[j + 1], k)] == col and brickable(xs[j + 1]) == bk:
                j += 1
            run = xs[i:j + 1]
            lens = sorted(BR if bk else PL, reverse=True)
            sizes = partition(len(run), run[0], seams[k - 1], lens)
            p = run[0]
            for n in sizes:
                if bk:
                    put(BR[n], col, p, y, k, n, 1, 3, kind='wand')
                    for xx in range(p, p + n):
                        for d in range(3):
                            done.add((xx, k + d))
                    for d in range(3):
                        seams[k + d].add(p)
                else:
                    put(PL[n], col, p, y, k, n, 1, 1, kind='wand')
                    for xx in range(p, p + n):
                        done.add((xx, k))
                    seams[k].add(p)
                p += n
            i = j + 1


# ---------- Hilfsfunktionen fuer die Stirnseiten ----------
def end_put(pid, col, front, xr, wxr, y0, wy, k0, hp, high_rel=None, kind='kopf', side_out=False):
    """xr = Abstand von der Stirnflaeche nach innen (negativ = davor), wxr = Tiefe in x."""
    if front:
        x0 = xr; high = (high_rel, 0) if high_rel is not None else None
        hv = None if high_rel is None else (high_rel, 0)
    else:
        x0 = L - xr - wxr
        hv = None if high_rel is None else (-high_rel, 0)
    sd = ((-1, 0) if front else (1, 0)) if side_out else None
    return put(pid, col, x0, y0, k0, wxr, wy, hp, high=hv, kind=kind, side=sd)


def lamp_tile(front, yy):
    """Runde Fliese 1x1 (98138) weiss, auf die Seitennoppe des 4070 gesteckt, Front nach aussen."""
    if front:
        M = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]], dtype=float); X = -8.0
    else:
        M = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float); X = 20.0 * L + 8.0
    t = np.array([X, -62.0, 20.0 * yy + 10])
    placed.append(dict(pid='98138', col=WHT, x0=-1, y0=yy, k0=7, wx=1, wy=1, hp=1, M=M, t=t, studs=set(), kind='lampe_fliese'))


def build_end(front):
    e = lambda *a, **kw: end_put(*a, front=front, **kw)
    # Stossfaenger (unter Deck), Fliese darauf, Kupplung
    e('3795', BLU, xr=-1, wxr=2, y0=1, wy=6, k0=4, hp=1)
    e('6636', BLU, xr=-1, wxr=1, y0=1, wy=6, k0=5, hp=1)
    e('3022', DBG, xr=-2, wxr=2, y0=3, wy=2, k0=3, hp=1)
    # k6..8 : Steine mit Scheinwerfern und Gitter
    k = 6
    e('87087', BLU, xr=0, wxr=1, y0=1, wy=1, k0=k, hp=3, kind='lampe', side_out=True)
    e('3005', BLU, xr=0, wxr=1, y0=2, wy=1, k0=k, hp=3)
    e('3004', BLK, xr=0, wxr=1, y0=3, wy=2, k0=k, hp=3)
    e('3005', BLU, xr=0, wxr=1, y0=5, wy=1, k0=k, hp=3)
    e('87087', BLU, xr=0, wxr=1, y0=6, wy=1, k0=k, hp=3, kind='lampe', side_out=True)
    for yy in (1, 6):
        lamp_tile(front, yy)
    # k9 : Zugzielanzeiger (schwarze Platte 2x4) + blaue 1x2
    e('3023', BLU, xr=0, wxr=2, y0=1, wy=1, k0=9, hp=1)
    e('3020', BLK, xr=0, wxr=2, y0=2, wy=4, k0=9, hp=1, kind='anzeige')
    e('3023', BLU, xr=0, wxr=2, y0=6, wy=1, k0=9, hp=1)
    # k10 : Platte 2x6 verbindet
    e('3795', BLU, xr=0, wxr=2, y0=1, wy=6, k0=10, hp=1)
    # Armaturenwand hinter der Scheibe (traegt die obere Schraege) k6..16 bei xr=2
    for kk in (6, 9, 12):
        e('3009', DBG, xr=2, wxr=1, y0=1, wy=6, k0=kk, hp=3)
    for kk in (15, 16):
        e('3666', DBG, xr=2, wxr=1, y0=1, wy=6, k0=kk, hp=1)
    # Frontscheibe unten (k11..16) und oben (k17..22): 65-Grad-Schraegen
    # eine durchgehende Scheibe (Windscreen 2x6x2 mit Glas) je Stufe statt drei Schraegen
    e('13760c01', DKB, xr=0, wxr=2, y0=1, wy=6, k0=11, hp=6, high_rel=+1, kind='scheibe')
    e('13760c01', DKB, xr=1, wxr=2, y0=1, wy=6, k0=17, hp=6, high_rel=+1, kind='scheibe')
    for y0 in (0, 7):
        e('60481', YEL, xr=0, wxr=2, y0=y0, wy=1, k0=11, hp=6, high_rel=+1, kind='pfosten')
        e('60481', YEL, xr=1, wxr=2, y0=y0, wy=1, k0=17, hp=6, high_rel=+1, kind='pfosten')


# ---------- Boden, Dach, Fahrwerk ----------
def build_deck():
    for i in range(17):                              # 17 x Platte 4x8 quer
        put('3035', BLU, 4 * i, 0, K_DECK, 4, 8, 1, kind='boden')
    put('3034', BLU, 68, 0, K_DECK, 2, 8, 1, kind='boden')


def build_underfloor():
    for x in (22, 30, 38):
        put('3035', DBG, x, 2, 4, 8, 4, 1, kind='unterflur')
    for x0 in (10, 52):
        put('3034', DBG, x0, 3, 4, 8, 2, 1, kind='drehgestell')


def build_roof():
    # Dachdeck k23: 4x8 quer ueber die ganze Breite, von x=2 bis 67
    for i in range(16):
        put('3035', YEL, 2 + 4 * i, 0, K_ROOF_DECK, 4, 8, 1, kind='dach')
    put('3034', YEL, 66, 0, K_ROOF_DECK, 2, 8, 1, kind='dach')
    # Gerundete Dachkanten: 15068 (2x2), hohe Seite zur Mitte
    for i in range(33):
        put('15068', YEL, 2 + 2 * i, 0, 24, 2, 2, 2, high=(0, +1), kind='kante')
        put('15068', YEL, 2 + 2 * i, 6, 24, 2, 2, 2, high=(0, -1), kind='kante')
    # Dachmitte k24 (Platten) und k25 (Fliesen); Klimageraete als Platte+Fliese hoeher
    ac = [(12, 8), (52, 8)]
    for i in range(8):
        put('3035', LBG, 2 + 8 * i, 2, 24, 8, 4, 1, kind='dach')
    put('3020', LBG, 66, 2, 24, 2, 4, 1, kind='dach')

    def in_ac(x, w):
        return any(a <= x and x + w <= a + b for a, b in ac)
    x = 2
    segs = [(2, 2)] + [(4 + 4 * i, 4) for i in range(15)] + [(64, 4)]
    for x, w in segs:
        for y in (2, 4):
            if in_ac(x, w):
                continue
            if w == 2:
                put('3068b', LBG, x, y, 25, 2, 2, 1, kind='dach')
            else:
                put('87079', LBG, x, y, 25, 4, 2, 1, kind='dach')
    for a, b in ac:
        put('3035', LBG, a, 2, 25, 8, 4, 1, kind='klima')
        for dx in (0, 4):
            for y in (2, 4):
                put('87079', WHT, a + dx, y, 26, 4, 2, 1, kind='klima')


def build_wheels():
    for ax in (11, 16, L - 1 - 16, L - 1 - 11):
        for yy in (1, 6):
            pid = '2927'
            inf = info(pid)
            Rm = rotmat(0)
            target = np.array([20 * ax + 10, -18.0, 20 * yy + 10])
            t = target - Rm @ inf['c']
            placed.append(dict(pid=pid, col=BLK, x0=ax, y0=yy, k0=0, wx=1, wy=1, hp=4, M=Rm, t=t, studs=set(), kind='rad'))


# ---------- Verbindungspruefung ----------
def connectivity():
    parts = [i for i, p in enumerate(placed) if p['kind'] not in ('rad', 'lampe_fliese')]
    parent = {i: i for i in parts}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    by_bottom = collections.defaultdict(list)       # (x,y,k_bottom) -> teil
    for i in parts:
        p = placed[i]
        for x in range(p['x0'], p['x0'] + p['wx']):
            for y in range(p['y0'], p['y0'] + p['wy']):
                by_bottom[(x, y, p['k0'])].append(i)
    edges = 0
    for i in parts:
        p = placed[i]
        ktop = p['k0'] + p['hp']
        for (x, y) in p['studs']:
            for j in by_bottom.get((x, y, ktop), []):
                if j != i:
                    a, b = find(i), find(j)
                    if a != b:
                        parent[a] = b
                    edges += 1
    comps = collections.defaultdict(list)
    for i in parts:
        comps[find(i)].append(i)
    return sorted(comps.values(), key=len, reverse=True), edges


# ---------- Ausgabe ----------
def write_ldr(path):
    order = sorted(range(len(placed)), key=lambda i: (placed[i]['k0'], placed[i]['kind'] in ('rad', 'lampe_fliese'), i))
    lines = ['0 Wieslauftalbahn VT 451 (Regio-Shuttle RS1), Massstab ca. 1:45', '0 Name: Wieslauftalbahn.ldr', '0 Author: Claude fuer Oskar Klein', '']
    lastk = None
    for i in order:
        p = placed[i]
        if lastk is not None and p['k0'] != lastk:
            lines.append('0 STEP')
        lastk = p['k0']
        M, t = p['M'], p['t']
        m = ' '.join(f'{v:g}' for v in M.flatten())
        lines.append(f"1 {p['col']} {t[0]:.1f} {t[1]:.1f} {t[2]:.1f} {m} {p['pid']}.dat")
    lines.append('0 STEP')
    open(path, 'w').write('\n'.join(lines) + '\n')


def build_all():
    build_deck()
    for y in (0, 7):
        pack_wall(y)
    build_end(True); build_end(False)
    build_underfloor(); build_roof()      # Raeder/Drehgestelle: bewusst nicht enthalten (siehe Notiz)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'wiesel.ldr'
    build_all()
    comps, edges = connectivity()
    print(f'Teile: {len(placed)}  (ohne Raeder und Lampenfliesen {sum(1 for p in placed if p["kind"] not in ("rad", "lampe_fliese"))}),  Verbindungen: {edges}')
    print('Zusammenhangskomponenten:', [len(c) for c in comps[:8]], '... gesamt', len(comps))
    if len(comps) > 1:
        for c in comps[1:6]:
            kinds = collections.Counter(placed[i]['kind'] for i in c)
            print('  lose Gruppe', len(c), dict(kinds), 'bei', placed[c[0]]['x0'], placed[c[0]]['y0'], placed[c[0]]['k0'])
    write_ldr(out)
    cnt = collections.Counter((p['pid'], p['col']) for p in placed)
    csvp = sys.argv[2] if len(sys.argv) > 2 else None
    if csvp:
        with open(csvp, 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['LDraw-Teil', 'LDraw-Farbe', 'Anzahl'])
            for (pid, col), n in sorted(cnt.items()):
                w.writerow([pid, col, n])
    print('Teiletypen:', len(cnt))


if __name__ == '__main__':
    main()
