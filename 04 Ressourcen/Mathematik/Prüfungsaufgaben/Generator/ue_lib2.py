#!/usr/bin/env python3
"""Zusätzliche SVG-Bausteine für die Typ-Varianten der Übungssätze."""
import math
from ue_lib import fmt, _winkelbogen

FARBE = {"w": ("#fff", "#333"), "g": ("#a9a9a9", "#555"), "s": ("#2a2a2a", "#111")}

def svg_behaelter(jars):
    """jars: Liste von (n_weiss, n_grau, n_schwarz). Vier Gläser mit Kugeln."""
    o = ['<svg width="560" height="150" viewBox="0 0 580 155">']
    for i, (nw, ng, ns) in enumerate(jars):
        x0 = 15 + i * 142
        o.append(f'<text x="{x0+55}" y="14" font-size="12" text-anchor="middle">Behälter {i+1}</text>')
        o.append(f'<rect x="{x0}" y="22" width="110" height="86" rx="12" fill="none" stroke="#333" stroke-width="1.4"/>')
        o.append(f'<line x1="{x0+8}" y1="30" x2="{x0+102}" y2="30" stroke="#333" stroke-width="1.2"/>')
        kugeln = ["w"] * nw + ["g"] * ng + ["s"] * ns
        for k, art in enumerate(kugeln):
            col = k % 5
            row = k // 5
            cx = x0 + 20 + col * 18
            cy = 92 - row * 18
            fill, stroke = FARBE[art]
            o.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        o.append(f'<rect x="{x0+48}" y="118" width="13" height="13" fill="none" stroke="#333" stroke-width="1.4"/>')
    o.append("</svg>")
    return "".join(o)

def svg_koerper_zylhk():
    """Achsenschnitt Zylinder mit aufgesetzter Halbkugel."""
    return """<svg class="fig" width="150" height="185" viewBox="0 0 160 195">
<g stroke="#222" stroke-width="1.4" fill="none">
<path d="M35,80 A45,45 0 0 1 125,80"/>
<rect x="35" y="80" width="90" height="90"/>
<line x1="35" y1="80" x2="125" y2="80" stroke-dasharray="4,3"/>
</g>
<g stroke="#222" stroke-width="1">
<line x1="140" y1="35" x2="140" y2="170"/><line x1="135" y1="35" x2="145" y2="35"/><line x1="135" y1="170" x2="145" y2="170"/>
<line x1="35" y1="182" x2="125" y2="182"/><line x1="35" y1="177" x2="35" y2="187"/><line x1="125" y1="177" x2="125" y2="187"/>
</g>
<text x="146" y="106" font-size="11" font-style="italic">h</text>
<text x="76" y="194" font-size="11" font-style="italic">d</text>
</svg>"""

def svg_koerper_wuerfelpyr():
    """Würfel mit aufgesetzter quadratischer Pyramide (Schrägbild)."""
    return """<svg class="fig" width="170" height="190" viewBox="0 0 180 200">
<g stroke="#222" stroke-width="1.3" fill="none">
<rect x="30" y="95" width="80" height="80"/>
<path d="M30,95 L55,72 L135,72 L110,95"/>
<path d="M135,72 L135,152 L110,175"/>
<path d="M30,175 L55,152 L135,152" stroke-dasharray="4,3"/>
<path d="M55,72 L55,152" stroke-dasharray="4,3"/>
<path d="M30,95 L82,18 L110,95"/>
<path d="M55,72 L82,18" stroke-dasharray="4,3"/>
<path d="M135,72 L82,18"/>
</g>
<text x="64" y="192" font-size="11" font-style="italic">a</text>
</svg>"""

def svg_quadrat_dreieck(a, winkel_deg):
    """Quadrat ABCD (A unten links), E auf BC, Linien AE und AC, Winkel bei A."""
    k = 190.0 / a
    W = a * k
    ox, oy = 26, 16
    A = (ox, oy + W)
    B = (ox + W, oy + W)
    C = (ox + W, oy)
    D = (ox, oy)
    be = a * math.tan(math.radians(winkel_deg))
    E = (ox + W, oy + W - be * k)
    o = [f'<svg class="fig" width="{W+62:.0f}" height="{W+46:.0f}" viewBox="0 0 {W+62:.0f} {W+46:.0f}">']
    o.append(f'<g stroke="#222" stroke-width="1.4" fill="none">'
             f'<rect x="{ox}" y="{oy}" width="{W:.1f}" height="{W:.1f}"/>'
             f'<path d="M{A[0]},{A[1]} L{E[0]:.1f},{E[1]:.1f}"/>'
             f'<path d="M{A[0]},{A[1]} L{C[0]},{C[1]}"/></g>')
    o.append(_winkelbogen(A[0], A[1], (1, 0), (E[0] - A[0], E[1] - A[1]), 30))
    o.append(f'<text x="{A[0]+34}" y="{A[1]-6}" font-size="13" font-style="italic">&alpha;</text>')
    o.append(f'<g font-size="13">'
             f'<text x="{A[0]-16}" y="{A[1]+14}">A</text><text x="{B[0]+5}" y="{B[1]+14}">B</text>'
             f'<text x="{C[0]+5}" y="{C[1]-3}">C</text><text x="{D[0]-16}" y="{D[1]-3}">D</text>'
             f'<text x="{E[0]+7}" y="{E[1]+4}">E</text></g></svg>')
    return "".join(o)

def svg_trapez(AB, BC, beta_deg, Ex, Cx, h):
    """Rechtwinkliges Trapez ABCD, E auf AB, gleichschenkliges Dreieck EBC."""
    k = 250.0 / AB
    ox, oy = 26, 16
    H = h * k
    def P(x, y):
        return (ox + x * k, oy + H - y * k)
    A, B = P(0, 0), P(AB, 0)
    C, D = P(Cx, h), P(0, h)
    E = P(Ex, 0)
    o = [f'<svg class="fig" width="{AB*k+58:.0f}" height="{H+48:.0f}" viewBox="0 0 {AB*k+58:.0f} {H+48:.0f}">']
    o.append(f'<g stroke="#222" stroke-width="1.4" fill="none">'
             f'<path d="M{A[0]},{A[1]} L{B[0]},{B[1]} L{C[0]:.1f},{C[1]:.1f} L{D[0]},{D[1]} Z"/>'
             f'<path d="M{E[0]:.1f},{E[1]} L{C[0]:.1f},{C[1]:.1f}"/></g>')
    o.append(f'<path d="M{A[0]+13},{A[1]} L{A[0]+13},{A[1]-13} L{A[0]},{A[1]-13}" stroke="#222" fill="none" stroke-width="1"/>')
    o.append(f'<circle cx="{A[0]+7}" cy="{A[1]-7}" r="1.2" fill="#222"/>')
    o.append(_winkelbogen(B[0], B[1], (-1, 0), (C[0] - B[0], C[1] - B[1]), 24))
    o.append(f'<text x="{B[0]-40}" y="{B[1]-8}" font-size="13" font-style="italic">&beta;</text>')
    o.append(f'<g font-size="13">'
             f'<text x="{A[0]-14}" y="{A[1]+15}">A</text><text x="{B[0]+4}" y="{B[1]+15}">B</text>'
             f'<text x="{C[0]-4:.0f}" y="{C[1]-5:.0f}">C</text><text x="{D[0]-14}" y="{D[1]-3}">D</text>'
             f'<text x="{E[0]-5:.0f}" y="{E[1]+15}">E</text></g></svg>')
    return "".join(o)

def svg_raeder(rad1, rad2):
    """Zwei Glücksräder; radN: Liste von Symbolen je Feld (gleich große Sektoren)."""
    o = ['<svg class="fig" width="300" height="160" viewBox="0 0 310 165">']
    for w, (cx, felder) in enumerate([(80, rad1), (230, rad2)]):
        n = len(felder)
        cy, r = 88, 58
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f4f4f4" stroke="#333" stroke-width="1.5"/>')
        for i in range(n):
            a = math.radians(-90 + i * 360.0 / n)
            o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + r*math.cos(a):.1f}" '
                     f'y2="{cy + r*math.sin(a):.1f}" stroke="#333" stroke-width="1"/>')
            m = math.radians(-90 + (i + 0.5) * 360.0 / n)
            o.append(f'<text x="{cx + 0.66*r*math.cos(m):.1f}" y="{cy + 0.66*r*math.sin(m)+5:.1f}" '
                     f'font-size="15" text-anchor="middle">{felder[i]}</text>')
        o.append(f'<path d="M{cx-7},{cy-r-9} L{cx+7},{cy-r-9} L{cx},{cy-r+4} Z" fill="#333"/>')
        o.append(f'<text x="{cx}" y="{cy+r+16}" font-size="11" text-anchor="middle">Rad {w+1}</text>')
    o.append("</svg>")
    return "".join(o)

def svg_wurf(a, c, x0, marken):
    """Wurfparabel y=ax²+c von x0 bis Landung; marken: Liste (x, beschriftung)."""
    xl = math.sqrt(-c / a)
    k = 16.0
    ox = 14 - x0 * k
    gy = 20 + c * k + 10
    def sx(x):
        return ox + x * k
    def sy(y):
        return gy - y * k
    pts = []
    x = x0
    while x <= xl + 1e-9:
        pts.append(f"{sx(x):.1f},{sy(a*x*x+c):.1f}")
        x += (xl - x0) / 40
    W = sx(xl) + 24
    o = [f'<svg width="{W:.0f}" height="{gy+22:.0f}" viewBox="0 0 {W:.0f} {gy+22:.0f}">']
    o.append(f'<g stroke="#222" stroke-width="1.5" fill="none"><path d="M{" L".join(pts)}"/>'
             f'<line x1="4" y1="{gy:.1f}" x2="{W-6:.0f}" y2="{gy:.1f}"/></g>')
    for mx, txt in marken:
        o.append(f'<line x1="{sx(mx):.1f}" y1="{gy:.1f}" x2="{sx(mx):.1f}" y2="{sy(a*mx*mx+c):.1f}" '
                 f'stroke="#555" stroke-width="1" stroke-dasharray="4,3"/>')
        o.append(f'<text x="{sx(mx):.1f}" y="{gy+14:.0f}" font-size="10" text-anchor="middle">{txt}</text>')
    o.append(f'<circle cx="{sx(x0):.1f}" cy="{sy(a*x0*x0+c):.1f}" r="3.5" fill="#222"/>')
    o.append("</svg>")
    return "".join(o)

def svg_pyramide_diag(a_label="A", c_label="C"):
    """Sechsseitige Pyramide mit Diagonaldreieck ACS (übernächste Ecken)."""
    cx, cy, rx, ry, sx, sy = 150, 190, 95, 28, 150, 22
    n = 6
    start = -90 + 30
    pts = []
    for i in range(n):
        a = math.radians(start + i * 360 / n)
        pts.append((cx + rx * math.sin(a), cy - ry * math.cos(a)))
    idx = sorted(range(n), key=lambda i: -pts[i][1])
    vorne = sorted(idx[:2], key=lambda i: pts[i][0])
    A_i = vorne[0]
    C_i = (A_i + 2) % n if pts[(A_i + 2) % n][0] > pts[A_i][0] else (A_i - 2) % n
    o = ['<svg class="fig" width="280" height="235" viewBox="0 0 300 250">']
    o.append(f'<path d="M{sx},{sy} L{pts[A_i][0]:.1f},{pts[A_i][1]:.1f} '
             f'L{pts[C_i][0]:.1f},{pts[C_i][1]:.1f} Z" fill="#d8d8d8"/>')
    o.append('<g stroke="#222" stroke-width="1.3" fill="none">')
    for i in range(n):
        j = (i + 1) % n
        sicht = pts[i][1] >= cy - 4 and pts[j][1] >= cy - 4
        dash = '' if sicht else ' stroke-dasharray="4,3"'
        o.append(f'<path d="M{pts[i][0]:.1f},{pts[i][1]:.1f} L{pts[j][0]:.1f},{pts[j][1]:.1f}"{dash}/>')
    for i in range(n):
        dash = '' if pts[i][1] >= cy - 4 else ' stroke-dasharray="4,3"'
        o.append(f'<path d="M{sx},{sy} L{pts[i][0]:.1f},{pts[i][1]:.1f}"{dash}/>')
    o.append(f'<path d="M{pts[A_i][0]:.1f},{pts[A_i][1]:.1f} L{pts[C_i][0]:.1f},{pts[C_i][1]:.1f}" stroke-dasharray="5,3"/>')
    o.append(f'<path d="M{sx},{sy} L{cx},{cy}" stroke-dasharray="2,3"/>')
    o.append('</g>')
    o.append(f'<text x="{cx-5}" y="{cy+4}" font-size="12">&times;</text>')
    o.append(f'<text x="{cx+6}" y="{(sy+cy)/2}" font-size="11" font-style="italic">h</text>')
    o.append(f'<g font-size="13"><text x="{sx-4}" y="{sy-6}">S</text>'
             f'<text x="{pts[A_i][0]-14:.0f}" y="{pts[A_i][1]+14:.0f}">{a_label}</text>'
             f'<text x="{pts[C_i][0]+6:.0f}" y="{pts[C_i][1]+10:.0f}">{c_label}</text></g></svg>')
    return "".join(o)

def svg_miniboxplot(mn, q1, med, q3, mx, amax, schritt, einheit, name):
    k = 460.0 / amax
    def x(v):
        return 40 + v * k
    o = [f'<svg width="560" height="98" viewBox="0 0 560 100">']
    o.append(f'<text x="6" y="34" font-size="11" font-weight="bold">{name}</text>')
    o.append(f'<g stroke="#222" stroke-width="1.2" fill="none">'
             f'<line x1="{x(mn)}" y1="14" x2="{x(mn)}" y2="38"/>'
             f'<line x1="{x(mn)}" y1="26" x2="{x(q1)}" y2="26"/>'
             f'<rect x="{x(q1)}" y="10" width="{x(q3)-x(q1)}" height="32" fill="#ccc"/>'
             f'<line x1="{x(med)}" y1="10" x2="{x(med)}" y2="42" stroke-width="1.6"/>'
             f'<line x1="{x(q3)}" y1="26" x2="{x(mx)}" y2="26"/>'
             f'<line x1="{x(mx)}" y1="14" x2="{x(mx)}" y2="38"/>'
             f'<line x1="36" y1="62" x2="540" y2="62"/>'
             f'<path d="M540,62 L531,58 M540,62 L531,66"/></g>')
    o.append('<g stroke="#222" stroke-width="1">')
    v = 0
    while v <= amax:
        o.append(f'<line x1="{x(v)}" y1="58" x2="{x(v)}" y2="66"/>')
        v += schritt
    o.append('</g><g font-size="10" text-anchor="middle">')
    v = 0
    while v <= amax:
        o.append(f'<text x="{x(v)}" y="80">{v}</text>')
        v += schritt * 2
    o.append(f'</g><text x="470" y="96" font-size="10">{einheit}</text></svg>')
    return "".join(o)
