#!/usr/bin/env python3
import os

OUT = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik Prüfungsaufgaben/Bilder"
os.makedirs(OUT, exist_ok=True)

BOX_FILL = "#eef4fb"
BOX_STROKE = "#33415c"
MED = "#c0392b"
GRID = "#d8e4ee"

def fmt(v):
    return str(int(v)) if float(v).is_integer() else str(v).replace(".", ",")

def boxchart(rows, vmin, vmax, step, unitlabel="", width=600):
    """rows: list of (label, stats(min,q1,med,q3,max) or None, fill). Empty list -> blank axis."""
    ML, MR = 46, 56
    plotw = width - ML - MR
    rowh, rowgap, toppad = 50, 16, 16
    axis_gap = 16
    def X(v): return ML + (v - vmin) / (vmax - vmin) * plotw
    if rows:
        block = len(rows) * rowh + (len(rows) - 1) * rowgap
    else:
        block = 120
    axisY = toppad + block + axis_gap
    height = axisY + 36
    s = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
         f'xmlns="http://www.w3.org/2000/svg" font-family="Arial,Helvetica,sans-serif">']
    s.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>')
    # faint vertical gridlines
    v = vmin
    while v <= vmax + 1e-6:
        s.append(f'<line x1="{X(v):.1f}" y1="{toppad-4}" x2="{X(v):.1f}" y2="{axisY:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        v += step
    # rows
    for i, (label, st, fill) in enumerate(rows):
        cy = toppad + i * (rowh + rowgap) + rowh / 2
        if st is not None:
            mn, q1, med, q3, mx = st
            top, bot = cy - rowh / 2, cy + rowh / 2
            cap = rowh * 0.34
            # whisker
            s.append(f'<line x1="{X(mn):.1f}" y1="{cy:.1f}" x2="{X(mx):.1f}" y2="{cy:.1f}" '
                     f'stroke="{BOX_STROKE}" stroke-width="1.8"/>')
            for vv in (mn, mx):
                s.append(f'<line x1="{X(vv):.1f}" y1="{cy-cap:.1f}" x2="{X(vv):.1f}" y2="{cy+cap:.1f}" '
                         f'stroke="{BOX_STROKE}" stroke-width="2"/>')
            # box
            s.append(f'<rect x="{X(q1):.1f}" y="{top:.1f}" width="{X(q3)-X(q1):.1f}" height="{rowh:.1f}" '
                     f'fill="{fill}" stroke="{BOX_STROKE}" stroke-width="2"/>')
            # median
            s.append(f'<line x1="{X(med):.1f}" y1="{top:.1f}" x2="{X(med):.1f}" y2="{bot:.1f}" '
                     f'stroke="{MED}" stroke-width="3"/>')
        if label:
            s.append(f'<text x="{width-MR+10:.1f}" y="{cy+6:.1f}" font-size="20" font-weight="bold" '
                     f'fill="{BOX_STROKE}">{label}</text>')
    # axis
    s.append(f'<line x1="{X(vmin):.1f}" y1="{axisY:.1f}" x2="{X(vmax)+10:.1f}" y2="{axisY:.1f}" '
             f'stroke="#1a1a1a" stroke-width="1.8"/>')
    ax = X(vmax) + 10
    s.append(f'<polygon points="{ax},{axisY:.1f} {ax-8},{axisY-4:.1f} {ax-8},{axisY+4:.1f}" fill="#1a1a1a"/>')
    v = vmin
    while v <= vmax + 1e-6:
        s.append(f'<line x1="{X(v):.1f}" y1="{axisY:.1f}" x2="{X(v):.1f}" y2="{axisY+6:.1f}" '
                 f'stroke="#1a1a1a" stroke-width="1.6"/>')
        s.append(f'<text x="{X(v):.1f}" y="{axisY+22:.1f}" font-size="13" fill="#333" '
                 f'text-anchor="middle">{fmt(v)}</text>')
        v += step
    if unitlabel:
        s.append(f'<text x="{ax+4:.1f}" y="{axisY+6:.1f}" font-size="14" fill="#333">{unitlabel}</text>')
    s.append('</svg>')
    return "\n".join(s)

def write(name, content):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(content + "\n")
    print("wrote", name)

B = BOX_FILL
# given boxplots
write("Box-Aufgabe-01.svg", boxchart([("", (10,35,50,70,95), B)], 0, 100, 10, "Punkte"))
write("Box-Aufgabe-02.svg", boxchart([("", (5,20,30,45,55), B)], 0, 60, 5, "min"))
write("Box-06.svg", boxchart([("(1)", (0,52.5,75,127.5,180), B), ("(2)", (0,60,90,150,180), B)], 0, 180, 15, "min"))
write("Box-07-given.svg", boxchart([("(1)", (0,52.5,75,127.5,180), B), ("(2)", (0,60,90,150,180), B), ("(3)", None, B)], 0, 180, 15, "min"))
write("Box-07-loesung.svg", boxchart([("A", (0,15,60,157.5,180), "#e6f0e6")], 0, 180, 15, "min"))
write("Box-08.svg", boxchart([("(B)", (20,40,90,120,175), B), ("(C)", (20,40,90,110,175), B)], 0, 180, 20, "kg"))
write("Box-09.svg", boxchart([("", (0,10,15,40,60), B)], 0, 60, 10, "min"))
write("Box-11.svg", boxchart([("", (12,25,40,55,80), B)], 0, 80, 10, "Punkte"))
write("Box-13.svg", boxchart([("A", (3,5,7,8,10), B), ("B", (1,4,7,11,13), B)], 0, 14, 2, ""))
write("Box-14.svg", boxchart([("", (1,3,6,12,30), B)], 0, 30, 5, "min"))
# empty axes (zum Zeichnen)
write("Box-03-axis.svg", boxchart([], 0, 16, 2, ""))
write("Box-04-axis.svg", boxchart([], 0, 14, 2, ""))
write("Box-05-axis.svg", boxchart([], 0, 60, 10, "€"))
write("Box-10-axis.svg", boxchart([], 0, 16, 2, ""))
write("Box-12-axis.svg", boxchart([], 0, 12, 1, "h"))
write("Box-15-axis.svg", boxchart([], 0, 24, 2, ""))
# solution boxplots
G = "#e6f0e6"
write("Box-03-loesung.svg", boxchart([("", (3,6,9,12,15), G)], 0, 16, 2, ""))
write("Box-04-loesung.svg", boxchart([("", (2,4.5,7.5,9,13), G)], 0, 14, 2, ""))
write("Box-05-loesung.svg", boxchart([("", (0,15,27.5,35,60), G)], 0, 60, 10, "€"))
write("Box-10-loesung.svg", boxchart([("", (4,6.5,9,12,15), G)], 0, 16, 2, ""))
write("Box-12-loesung.svg", boxchart([("", (1,4.5,6,7,11), G)], 0, 12, 1, "h"))
write("Box-15-loesung.svg", boxchart([("", (5,9,13,16.5,22), G)], 0, 24, 2, ""))
print("done")
