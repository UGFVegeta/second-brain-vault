#!/usr/bin/env python3
"""Helfer für den Übungssatz-Generator: SVG-Grafiken, HTML-Hüllen, Formatierung."""
import math

# ---------- Formatierung ----------

def fmt(x, dec=2):
    """Zahl deutsch formatieren, überflüssige Nullen weg."""
    s = f"{x:.{dec}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")

def geld(x):
    return f"{x:.2f}".replace(".", ",") + " €"

def tsd(n):
    """96000 -> 96 000"""
    return f"{n:,.0f}".replace(",", " ")

# ---------- HTML ----------

STYLE = """
body{font-family:Arial,Helvetica,sans-serif;font-size:14.5px;color:#111;margin:0;padding:10px 12px;background:#fff}
.inhalt{max-width:680px}
.kopfzeile{font-weight:bold;font-size:15px;margin:0 0 10px;padding-bottom:4px;border-bottom:2px solid #666}
.kopfzeile .p{float:right}
.fig{float:right;margin:0 0 10px 14px}
p{margin:7px 0;line-height:1.45}
ul{margin:6px 0;padding-left:22px}
li{margin:5px 0}
table{border-collapse:collapse;margin:8px 0}
td,th{border:1px solid #333;padding:3px 10px;text-align:center;font-size:13.5px}
table.frei td{border:none;text-align:left;padding:1px 8px}
.cb{display:inline-block;width:11px;height:11px;border:1.3px solid #333;vertical-align:middle}
.geg{margin:6px 0 6px 26px;line-height:1.75;font-family:Georgia,'Times New Roman',serif;font-style:italic}
.geg b{font-style:normal}
.ustrich{text-decoration:overline;font-style:italic;font-family:Georgia,serif}
.formel{font-family:Georgia,'Times New Roman',serif;font-style:italic}
h4{margin:12px 0 3px;font-size:14px}
.zw{color:#444}
.klar{clear:both}
.ergebnis{border:1.5px solid #333;display:inline-block;padding:2px 10px;margin:2px 0;font-weight:bold}
"""

def seite(titel, body):
    return ('<!DOCTYPE html>\n<html lang="de"><head><meta charset="utf-8"><title>'
            + titel + '</title><style>' + STYLE + '</style></head><body>'
            '<div class="inhalt">' + body + '<div class="klar"></div></div></body></html>\n')

def kopfzeile(satz, label, punkte, art):
    zusatz = "" if art == "a" else " – Lösung"
    return ('<div class="kopfzeile">Übungssatz ' + satz + ' · Aufgabe ' + label + zusatz +
            '<span class="p">(' + fmt(punkte, 1) + ' P)</span></div>')

def us(t):
    """Strecke mit Überstrich."""
    return '<span class="ustrich">' + t + '</span>'

# ---------- SVG-Bausteine ----------

def svg_quader_pyramide():
    return """<svg class="fig" width="260" height="180" viewBox="0 0 290 200">
<g stroke="#222" fill="none" stroke-width="1.3">
<rect x="15" y="120" width="105" height="44"/>
<path d="M15,120 L43,96 L148,96 L120,120"/>
<path d="M148,96 L148,140 L120,164"/>
<path d="M15,164 L43,140 L148,140" stroke-dasharray="4,3"/>
<path d="M43,96 L43,140" stroke-dasharray="4,3"/>
</g>
<text x="63" y="180" font-size="12" font-style="italic">a</text>
<text x="136" y="158" font-size="12" font-style="italic">b</text>
<text x="6" y="146" font-size="12" font-style="italic">c</text>
<g stroke="#222" fill="none" stroke-width="1.3">
<path d="M195,168 L255,168 L281,148 L221,148 Z"/>
<path d="M195,168 L238,26 L255,168"/>
<path d="M221,148 L238,26" stroke-dasharray="4,3"/>
<path d="M281,148 L238,26"/>
<path d="M238,26 L238,158" stroke-dasharray="2,3"/>
</g>
<text x="214" y="184" font-size="12" font-style="italic">a<tspan font-size="9" dy="3">Pyr</tspan></text>
</svg>"""

def _frac_svg(x, y, num, den):
    return (f'<text x="{x}" y="{y-3}" font-size="10" text-anchor="middle">{num}</text>'
            f'<line x1="{x-9}" y1="{y}" x2="{x+9}" y2="{y}" stroke="#222"/>'
            f'<text x="{x}" y="{y+10}" font-size="10" text-anchor="middle">{den}</text>')

def svg_baum(farben, kasten1, k2_branch, k2_sub):
    """Baumdiagramm 2 Stufen, 3 Farben.
    kasten1: Liste von 3 Einträgen: 'text', ('frac',n,d) oder None (leer).
    k2_branch/k2_sub: Position des leeren Kastens auf der 2. Stufe."""
    xs = [55, 165, 275]
    out = ['<svg class="fig" width="310" height="210" viewBox="0 0 330 230">']
    out.append('<g stroke="#222" stroke-width="1.1" fill="none">')
    for x in xs:
        out.append(f'<path d="M165,12 L{x},72"/>')
        for dx in (-40, 0, 40):
            out.append(f'<path d="M{x},90 L{x+dx},150"/>')
    out.append('</g>')
    bx = [104, 165, 228]
    for i, k in enumerate(kasten1):
        out.append(f'<rect x="{bx[i]-21}" y="26" width="42" height="26" fill="#fff" stroke="#222"/>')
        if isinstance(k, tuple):
            out.append(_frac_svg(bx[i], 39, k[1], k[2]))
        elif k:
            out.append(f'<text x="{bx[i]}" y="43" font-size="11" text-anchor="middle">{k}</text>')
    # leerer Kasten 2. Stufe
    k2x = xs[k2_branch] + (-40, 0, 40)[k2_sub] * 0.5 - 21
    out.append(f'<rect x="{k2x}" y="102" width="42" height="26" fill="#fff" stroke="#222"/>')
    out.append('<g font-size="12" text-anchor="middle">')
    for i, x in enumerate(xs):
        out.append(f'<circle cx="{x}" cy="81" r="10" fill="#fff" stroke="#222"/>'
                   f'<text x="{x}" y="85">{farben[i]}</text>')
        for j, dx in enumerate((-40, 0, 40)):
            out.append(f'<circle cx="{x+dx}" cy="160" r="9" fill="#fff" stroke="#222"/>'
                       f'<text x="{x+dx}" y="164" font-size="11">{farben[j]}</text>')
    out.append('</g></svg>')
    return "".join(out)

# Muster-Familien: Zellen (col,row) für Muster n
def cells_kreuz(n):
    c = [(0, 0)]
    for k in range(1, n + 1):
        c += [(k, 0), (-k, 0), (0, k), (0, -k)]
    return c

def cells_L(n):
    c = [(0, -r) for r in range(n + 1)]          # Säule Höhe n+1
    c += [(k, 0) for k in range(1, n + 1)]        # Zeile Länge n
    return c

def cells_T(n):
    c = [(k, 0) for k in range(-n, n + 1)]        # Zeile 2n+1
    c += [(0, r) for r in range(1, n + 1)]        # Stiel n
    return c

def cells_rahmen(n):
    s = n + 1
    c = []
    for k in range(s):
        c += [(k, 0), (k, s - 1)]
    for r in range(1, s - 1):
        c += [(0, r), (s - 1, r)]
    return sorted(set(c))

def cells_treppe(n):
    c = []
    for stufe in range(1, n + 1):
        for r in range(stufe):
            c.append((stufe - 1, -r))
    return c

def svg_muster(cells_fn, cell=13):
    out = ['<svg width="400" height="120" viewBox="0 0 420 130"><g fill="#4a4a4a">']
    x0 = 10
    label_pos = []
    for n in (1, 2, 3):
        cells = cells_fn(n)
        cols = [c for c, r in cells]
        rows = [r for c, r in cells]
        w = (max(cols) - min(cols) + 1) * cell
        basisx = x0 - min(cols) * cell
        basisy = 20 - min(rows) * cell
        for c, r in cells:
            out.append(f'<rect x="{basisx + c*cell}" y="{basisy + r*cell}" '
                       f'width="{cell-1}" height="{cell-1}"/>')
        label_pos.append((x0 + w / 2, 20 + (max(rows) - min(rows) + 1) * cell + 16, n))
        x0 += w + 46
    out.append('</g><g font-size="11" text-anchor="middle" fill="#111">')
    for x, y, n in label_pos:
        out.append(f'<text x="{x}" y="{min(y,124)}">({n}.)</text>')
    out.append('</g></svg>')
    return "".join(out)

def svg_boxplot(mn, q1, med, q3, mx, fehler, achse_max, schritt, einheit):
    """fehler: (element, gezeichneter_wert) mit element in min/q1/med/q3/max."""
    d = {"min": mn, "q1": q1, "med": med, "q3": q3, "max": mx}
    d[fehler[0]] = fehler[1]
    k = 500.0 / achse_max
    def x(v):
        return 30 + v * k
    o = ['<svg width="560" height="120" viewBox="0 0 560 125" style="border:1px solid #333;display:block;margin:6px 0">']
    o.append(f'<g stroke="#222" stroke-width="1.2" fill="none">'
             f'<line x1="{x(d["min"])}" y1="15" x2="{x(d["min"])}" y2="45"/>'
             f'<line x1="{x(d["min"])}" y1="30" x2="{x(d["q1"])}" y2="30"/>'
             f'<rect x="{x(d["q1"])}" y="12" width="{x(d["q3"])-x(d["q1"])}" height="36" fill="#ccc"/>'
             f'<line x1="{x(d["med"])}" y1="12" x2="{x(d["med"])}" y2="48" stroke-width="1.6"/>'
             f'<line x1="{x(d["q3"])}" y1="30" x2="{x(d["max"])}" y2="30"/>'
             f'<line x1="{x(d["max"])}" y1="15" x2="{x(d["max"])}" y2="45"/>'
             f'<line x1="25" y1="85" x2="545" y2="85"/>'
             f'<path d="M545,85 L536,81 M545,85 L536,89"/></g>')
    o.append('<g stroke="#222" stroke-width="1">')
    v = 0
    while v <= achse_max:
        o.append(f'<line x1="{x(v)}" y1="81" x2="{x(v)}" y2="89"/>')
        v += schritt
    o.append('</g><g font-size="11" text-anchor="middle">')
    v = 0
    while v <= achse_max:
        o.append(f'<text x="{x(v)}" y="103">{v}</text>')
        v += schritt * 2
    o.append(f'</g><text x="470" y="120" font-size="11">{einheit}</text></svg>')
    return "".join(o)

def svg_hbar(titel, kategorien, werte, maxwert):
    k = 180.0 / maxwert
    o = [f'<svg class="fig" width="290" height="{40+len(werte)*34}" viewBox="0 0 290 {50+len(werte)*34}">']
    o.append(f'<text x="145" y="14" font-size="12" font-weight="bold" text-anchor="middle">{titel}</text>')
    o.append('<g stroke="#bbb" stroke-width="1">')
    for gx in range(1, 5):
        o.append(f'<line x1="{95+gx*45}" y1="24" x2="{95+gx*45}" y2="{28+len(werte)*34}"/>')
    o.append('</g><g fill="#333">')
    for i, w in enumerate(werte):
        o.append(f'<rect x="95" y="{30+i*34}" width="{w*k}" height="24"/>')
    o.append('</g><g font-size="11" text-anchor="end">')
    for i, kat in enumerate(kategorien):
        o.append(f'<text x="90" y="{46+i*34}">{kat}</text>')
    o.append('</g><g font-size="10.5" fill="#fff" text-anchor="end">')
    for i, w in enumerate(werte):
        o.append(f'<text x="{95+w*k-5}" y="{46+i*34}">{w}</text>')
    o.append('</g></svg>')
    return "".join(o)

def svg_vbar(titel, jahre, werte, ymax, ystep, extrajahr):
    n = len(jahre) + 1
    o = ['<svg width="310" height="215" viewBox="0 0 310 215">']
    o.append(f'<text x="165" y="14" font-size="12" font-weight="bold" text-anchor="middle">{titel}</text>')
    o.append('<g stroke="#ccc" stroke-width="0.8">')
    y = ystep
    while y <= ymax:
        sy = 185 - 160 * y / ymax
        o.append(f'<line x1="60" y1="{sy}" x2="300" y2="{sy}"/>')
        y += ystep
    o.append('</g><g stroke="#222" stroke-width="1.2">'
             '<line x1="60" y1="20" x2="60" y2="185"/>'
             '<line x1="60" y1="185" x2="300" y2="185"/></g>')
    o.append('<g font-size="8.5" text-anchor="end" fill="#333">')
    y = 0
    while y <= ymax:
        sy = 188 - 160 * y / ymax
        o.append(f'<text x="56" y="{sy}">{tsd(y)}</text>')
        y += ystep * 2
    o.append('</g><g fill="#333">')
    bw = 26
    for i, w in enumerate(werte):
        h = 160 * w / ymax
        o.append(f'<rect x="{72+i*46}" y="{185-h}" width="{bw}" height="{h}"/>')
    o.append('</g><g font-size="8.5" text-anchor="middle">')
    for i, w in enumerate(werte):
        h = 160 * w / ymax
        o.append(f'<text x="{72+i*46+bw/2}" y="{180-h}">{tsd(w)}</text>')
    o.append('</g><g font-size="9.5" text-anchor="middle">')
    for i, j in enumerate(list(jahre) + [extrajahr]):
        o.append(f'<text x="{72+i*46+bw/2}" y="{198}">{j}</text>')
    o.append('</g></svg>')
    return "".join(o)

def svg_pie(titel, proz, labels):
    """4 Segmente ab 12 Uhr im Uhrzeigersinn."""
    farben = ["#1c1c1c", "#e8e8e8", "#555", "#aaa"]
    textf = ["#fff", "#111", "#fff", "#111"]
    cx, cy, r = 150, 108, 60
    o = ['<svg width="310" height="200" viewBox="0 0 310 200">']
    o.append(f'<text x="155" y="14" font-size="11.5" font-weight="bold" text-anchor="middle">{titel}</text>')
    winkel = 0
    o.append('<g stroke="#fff" stroke-width="1.2">')
    seg = []
    for i, p in enumerate(proz):
        a0 = winkel
        a1 = winkel + p * 3.6
        x0, y0 = cx + r * math.sin(math.radians(a0)), cy - r * math.cos(math.radians(a0))
        x1, y1 = cx + r * math.sin(math.radians(a1)), cy - r * math.cos(math.radians(a1))
        gross = 1 if p > 50 else 0
        o.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {gross} 1 {x1:.1f},{y1:.1f} Z" fill="{farben[i]}"/>')
        m = math.radians((a0 + a1) / 2)
        seg.append((cx + 0.62 * r * math.sin(m), cy - 0.62 * r * math.cos(m),
                    cx + 1.28 * r * math.sin(m), cy - 1.28 * r * math.cos(m)))
        winkel = a1
    o.append('</g><g font-size="10">')
    for i, (px, py, lx, ly) in enumerate(seg):
        o.append(f'<text x="{px:.0f}" y="{py:.0f}" fill="{textf[i]}" text-anchor="middle">{fmt(proz[i],1)} %</text>')
    o.append('</g><g font-size="9.5">')
    for i, (px, py, lx, ly) in enumerate(seg):
        anker = "start" if lx >= cx else "end"
        o.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anker}">{labels[i]}</text>')
    o.append('</g></svg>')
    return "".join(o)

def _pfad(f, x0, x1, sx, sy, schritt=0.25):
    pts = []
    x = x0
    while x <= x1 + 1e-9:
        pts.append(f"{sx(x):.1f},{sy(f(x)):.1f}")
        x += schritt
    return "M" + " L".join(pts)

def svg_grid_parabeln(funcs):
    """funcs: Liste (f, x0, x1, labelx, labeltext). Gitter x -6.5..6.5, y -4.5..8.5."""
    def sx(x): return (x + 6.5) * 20
    def sy(y): return (8.5 - y) * 20
    o = ['<svg class="fig" width="272" height="272" viewBox="-6 -6 272 272">']
    o.append('<g stroke="#c9c9c9" stroke-width="0.7">')
    for gx in range(-6, 7):
        if gx:
            o.append(f'<line x1="{sx(gx)}" y1="0" x2="{sx(gx)}" y2="260"/>')
    for gy in range(-4, 9):
        if gy:
            o.append(f'<line x1="0" y1="{sy(gy)}" x2="260" y2="{sy(gy)}"/>')
    o.append('</g><g stroke="#222" stroke-width="1.3">')
    o.append(f'<line x1="{sx(0)}" y1="0" x2="{sx(0)}" y2="260"/>')
    o.append(f'<line x1="0" y1="{sy(0)}" x2="260" y2="{sy(0)}"/>')
    o.append(f'<path d="M{sx(0)},0 L{sx(0)-4},8 M{sx(0)},0 L{sx(0)+4},8" fill="none"/>')
    o.append(f'<path d="M260,{sy(0)} L252,{sy(0)-4} M260,{sy(0)} L252,{sy(0)+4}" fill="none"/>')
    o.append('</g><g font-size="9" text-anchor="middle" fill="#333">')
    for gx in (-6, -4, -2, 2, 4, 6):
        o.append(f'<text x="{sx(gx)}" y="{sy(0)+11}">{gx}</text>')
    for gy in (-4, -2, 2, 4, 6, 8):
        o.append(f'<text x="{sx(0)-8}" y="{sy(gy)+3}">{gy}</text>')
    o.append(f'<text x="{sx(0)+8}" y="10" font-size="11" font-style="italic">y</text>')
    o.append(f'<text x="252" y="{sy(0)-8}" font-size="11" font-style="italic">x</text>')
    o.append('</g><g stroke="#222" stroke-width="1.6" fill="none">')
    for f, x0, x1, _, _ in funcs:
        o.append(f'<path d="{_pfad(f, x0, x1, sx, sy)}"/>')
    o.append('</g><g font-size="12" font-style="italic">')
    for f, x0, x1, lx, lt in funcs:
        o.append(f'<text x="{sx(lx)+4}" y="{sy(f(lx))-11}">{lt}</text>')
    o.append('</g></svg>')
    return "".join(o)

def _winkelbogen(px, py, v1, v2, r=20):
    a1 = math.atan2(v1[1], v1[0])
    a2 = math.atan2(v2[1], v2[0])
    x1, y1 = px + r * math.cos(a1), py + r * math.sin(a1)
    x2, y2 = px + r * math.cos(a2), py + r * math.sin(a2)
    diff = (a2 - a1) % (2 * math.pi)
    sweep = 1 if diff < math.pi else 0
    if not sweep:
        x1, y1, x2, y2 = x2, y2, x1, y1
    return f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x2:.1f},{y2:.1f}" stroke="#222" fill="none" stroke-width="1"/>'

def svg_trig_rechteck(w, h, e, f):
    """Rechteck ABCD (w x h), E auf AD (Höhe e ab A), F auf AB (Abstand f)."""
    k = 250.0 / w
    W, H = w * k, h * k
    ox, oy = 26, 18
    def P(x, y):
        return (ox + x * k, oy + H - y * k)
    A, B, C, D = P(0, 0), P(w, 0), P(w, h), P(0, h)
    E, F = P(0, e), P(f, 0)
    o = [f'<svg class="fig" width="{W+60:.0f}" height="{H+52:.0f}" viewBox="0 0 {W+60:.0f} {H+52:.0f}">']
    o.append(f'<g stroke="#222" stroke-width="1.4" fill="none">'
             f'<rect x="{ox}" y="{oy}" width="{W:.1f}" height="{H:.1f}"/>'
             f'<path d="M{E[0]:.1f},{E[1]:.1f} L{C[0]:.1f},{C[1]:.1f}"/>'
             f'<path d="M{E[0]:.1f},{E[1]:.1f} L{F[0]:.1f},{F[1]:.1f}"/>'
             f'<path d="M{F[0]:.1f},{F[1]:.1f} L{C[0]:.1f},{C[1]:.1f}"/></g>')
    # rechter Winkel bei F
    u = (E[0] - F[0], E[1] - F[1]); lu = math.hypot(*u); u = (u[0] / lu * 9, u[1] / lu * 9)
    v = (C[0] - F[0], C[1] - F[1]); lv = math.hypot(*v); v = (v[0] / lv * 9, v[1] / lv * 9)
    o.append(f'<path d="M{F[0]+u[0]:.1f},{F[1]+u[1]:.1f} L{F[0]+u[0]+v[0]:.1f},{F[1]+u[1]+v[1]:.1f} '
             f'L{F[0]+v[0]:.1f},{F[1]+v[1]:.1f}" stroke="#222" fill="none" stroke-width="1"/>')
    o.append(f'<circle cx="{F[0]+(u[0]+v[0])*0.55:.1f}" cy="{F[1]+(u[1]+v[1])*0.55:.1f}" r="1.2" fill="#222"/>')
    o.append(_winkelbogen(E[0], E[1], (F[0] - E[0], F[1] - E[1]), (C[0] - E[0], C[1] - E[1]), 22))
    mwx = E[0] + 30
    mwy = E[1] + 4
    o.append(f'<text x="{mwx:.0f}" y="{mwy:.0f}" font-size="13" font-style="italic">&epsilon;</text>')
    o.append(f'<g font-size="13">'
             f'<text x="{A[0]-14}" y="{A[1]+14}">A</text><text x="{B[0]+4}" y="{B[1]+14}">B</text>'
             f'<text x="{C[0]+4}" y="{C[1]-4}">C</text><text x="{D[0]-14}" y="{D[1]-4}">D</text>'
             f'<text x="{E[0]-14}" y="{E[1]+4}">E</text><text x="{F[0]-4}" y="{F[1]+16}">F</text></g></svg>')
    return "".join(o)

def svg_drachen(b, h, ex, gy, fx):
    """Rechteck ABCD (b x h), Drachen EGCF: E(ex|0), G(b|gy), C(b|h), F(fx|h)."""
    k = 250.0 / b
    W, H = b * k, h * k
    ox, oy = 26, 16
    def P(x, y):
        return (ox + x * k, oy + H - y * k)
    A, B, C, D = P(0, 0), P(b, 0), P(b, h), P(0, h)
    E, G, F = P(ex, 0), P(b, gy), P(fx, h)
    o = [f'<svg class="fig" width="{W+58:.0f}" height="{H+46:.0f}" viewBox="0 0 {W+58:.0f} {H+46:.0f}">']
    o.append(f'<g stroke="#222" stroke-width="1.4" fill="none">'
             f'<rect x="{ox}" y="{oy}" width="{W:.1f}" height="{H:.1f}"/>'
             f'<path d="M{E[0]:.1f},{E[1]:.1f} L{G[0]:.1f},{G[1]:.1f}"/>'
             f'<path d="M{E[0]:.1f},{E[1]:.1f} L{F[0]:.1f},{F[1]:.1f}"/></g>')
    o.append(_winkelbogen(E[0], E[1], (1, 0), (G[0] - E[0], G[1] - E[1]), 24))
    o.append(f'<text x="{E[0]+28:.0f}" y="{E[1]-8:.0f}" font-size="13" font-style="italic">&epsilon;</text>')
    o.append(_winkelbogen(F[0], F[1], (E[0] - F[0], E[1] - F[1]), (C[0] - F[0], C[1] - F[1]), 14))
    o.append(f'<text x="{F[0]+6:.0f}" y="{F[1]+22:.0f}" font-size="13" font-style="italic">&phi;</text>')
    o.append(f'<g font-size="13">'
             f'<text x="{A[0]-14}" y="{A[1]+14}">A</text><text x="{B[0]+4}" y="{B[1]+14}">B</text>'
             f'<text x="{C[0]+4}" y="{C[1]-3}">C</text><text x="{D[0]-14}" y="{D[1]-3}">D</text>'
             f'<text x="{E[0]-4}" y="{E[1]+16}">E</text><text x="{G[0]+5}" y="{G[1]+4}">G</text>'
             f'<text x="{F[0]-5}" y="{F[1]-5}">F</text></g></svg>')
    return "".join(o)

def svg_pyramide(seiten):
    """Skizze regelmäßige 5- oder 6-seitige Pyramide, Manteldreieck SBC grau, Winkel psi an S."""
    cx, cy, rx, ry, sx, sy = 150, 190, 95, 28, 150, 22
    n = seiten
    start = -90 + (180 / n)  # so dass eine Kante vorne liegt
    pts = []
    for i in range(n):
        a = math.radians(start + i * 360 / n)
        pts.append((cx + rx * math.sin(a), cy + ry * math.cos(a) * -1 + 0))
    # vorne = größte y
    idx = sorted(range(n), key=lambda i: -pts[i][1])
    b_i, c_i = sorted(idx[:2], key=lambda i: pts[i][0])
    o = ['<svg class="fig" width="280" height="235" viewBox="0 0 300 250">']
    o.append(f'<path d="M{sx},{sy} L{pts[b_i][0]:.1f},{pts[b_i][1]:.1f} '
             f'L{pts[c_i][0]:.1f},{pts[c_i][1]:.1f} Z" fill="#d8d8d8"/>')
    o.append('<g stroke="#222" stroke-width="1.3" fill="none">')
    for i in range(n):
        j = (i + 1) % n
        vorne = pts[i][1] > cy - 2 or pts[j][1] > cy - 2
        dash = '' if (i in (b_i, c_i) and j in (b_i, c_i)) or vorne else ' stroke-dasharray="4,3"'
        # sichtbar: Kanten deren beide Punkte y >= cy (vordere Hälfte)
        sicht = pts[i][1] >= cy - 4 and pts[j][1] >= cy - 4
        dash = '' if sicht else ' stroke-dasharray="4,3"'
        o.append(f'<path d="M{pts[i][0]:.1f},{pts[i][1]:.1f} L{pts[j][0]:.1f},{pts[j][1]:.1f}"{dash}/>')
    for i in range(n):
        dash = '' if pts[i][1] >= cy - 4 else ' stroke-dasharray="4,3"'
        o.append(f'<path d="M{sx},{sy} L{pts[i][0]:.1f},{pts[i][1]:.1f}"{dash}/>')
    o.append(f'<path d="M{sx},{sy} L{cx},{cy}" stroke-dasharray="2,3"/>')
    o.append('</g>')
    o.append(f'<text x="{cx-5}" y="{cy+4}" font-size="12">&times;</text>')
    mx = (pts[b_i][0] + pts[c_i][0]) / 2
    o.append(_winkelbogen(sx, sy, (pts[b_i][0] - sx, pts[b_i][1] - sy),
                          (pts[c_i][0] - sx, pts[c_i][1] - sy), 26))
    o.append(f'<text x="{sx+8}" y="{sy+42}" font-size="13" font-style="italic">&psi;</text>')
    o.append(f'<g font-size="13"><text x="{sx-4}" y="{sy-6}">S</text>'
             f'<text x="{pts[b_i][0]-2:.0f}" y="{pts[b_i][1]+16:.0f}">B</text>'
             f'<text x="{pts[c_i][0]+5:.0f}" y="{pts[c_i][1]+10:.0f}">C</text></g></svg>')
    return "".join(o)

def svg_koerper_vergleich():
    return """<svg class="fig" width="280" height="205" viewBox="0 0 300 220">
<g stroke="#222" stroke-width="1.3" fill="none">
<path d="M85,25 L37,86 L37,190 L133,190 L133,86 Z"/>
<line x1="37" y1="86" x2="133" y2="86" stroke-dasharray="4,3"/>
<line x1="85" y1="25" x2="85" y2="190" stroke-dasharray="2,3"/>
</g>
<path d="M85,47 A22,22 0 0 0 74,44" stroke="#222" fill="none" stroke-width="1"/>
<text x="72" y="58" font-size="12" font-style="italic">&delta;</text>
<text x="46" y="52" font-size="12" font-style="italic">s</text>
<g stroke="#222" stroke-width="1"><line x1="152" y1="25" x2="152" y2="190"/>
<line x1="147" y1="25" x2="157" y2="25"/><line x1="147" y1="190" x2="157" y2="190"/></g>
<text x="158" y="112" font-size="11" font-style="italic">h<tspan font-size="8" dy="3">ges</tspan></text>
<g stroke="#222" stroke-width="1"><line x1="37" y1="202" x2="133" y2="202"/>
<line x1="37" y1="197" x2="37" y2="207"/><line x1="133" y1="197" x2="133" y2="207"/></g>
<text x="81" y="216" font-size="12" font-style="italic">d</text>
<rect x="200" y="25" width="78" height="165" stroke="#222" fill="none" stroke-width="1.3"/>
<g stroke="#222" stroke-width="1"><line x1="200" y1="202" x2="278" y2="202"/>
<line x1="200" y1="197" x2="200" y2="207"/><line x1="278" y1="197" x2="278" y2="207"/></g>
<text x="235" y="216" font-size="12" font-style="italic">a</text>
<text x="284" y="112" font-size="11" font-style="italic">h<tspan font-size="8" dy="3">Pr</tspan></text>
</svg>"""

def svg_tunnel(H, W, tuer_h, tuer_b):
    k = 240.0 / W
    ox, gy = 15, 20 + H * k
    a = 4.0 * H / (W * W)
    def sx(x): return ox + (x + W / 2) * k
    def sy(y): return gy - y * k
    pts = []
    x = -W / 2
    while x <= W / 2 + 1e-9:
        pts.append(f"{sx(x):.1f},{sy(H - a * x * x):.1f}")
        x += W / 40
    o = [f'<svg width="{270+30}" height="{gy+22:.0f}" viewBox="0 0 300 {gy+22:.0f}">']
    o.append(f'<g stroke="#222" stroke-width="1.5" fill="none">'
             f'<path d="M{"M".join([""])}{"M" if False else ""}{"" }"/></g>')
    o[-1] = f'<g stroke="#222" stroke-width="1.5" fill="none"><path d="M{" L".join(pts)}"/>' \
            f'<line x1="{ox-6}" y1="{gy:.1f}" x2="{ox+W*k+8}" y2="{gy:.1f}"/></g>'
    o.append(f'<rect x="{sx(-tuer_b/2):.1f}" y="{sy(tuer_h):.1f}" width="{tuer_b*k:.1f}" '
             f'height="{tuer_h*k:.1f}" fill="none" stroke="#222" stroke-width="1" stroke-dasharray="5,3"/>')
    o.append(f'<g stroke="#222" stroke-width="1">'
             f'<line x1="{sx(-tuer_b/2)-8:.1f}" y1="{sy(tuer_h):.1f}" x2="{sx(-tuer_b/2)-8:.1f}" y2="{gy:.1f}"/>'
             f'<line x1="{sx(-tuer_b/2)-12:.1f}" y1="{sy(tuer_h):.1f}" x2="{sx(-tuer_b/2)-4:.1f}" y2="{sy(tuer_h):.1f}"/>'
             f'<line x1="{sx(-tuer_b/2)-12:.1f}" y1="{gy:.1f}" x2="{sx(-tuer_b/2)-4:.1f}" y2="{gy:.1f}"/></g>')
    o.append(f'<text x="{sx(-tuer_b/2)-46:.0f}" y="{(sy(tuer_h)+gy)/2+4:.0f}" font-size="11">{fmt(tuer_h)} m</text>')
    o.append('</svg>')
    return "".join(o)
