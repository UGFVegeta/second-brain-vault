#!/usr/bin/env python3
import os

BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben"

diffs = {
 "Trigonometrie Aufgabenpool.html": {1:2,2:1,3:2,4:3,5:3,6:2,7:1,8:1,9:2,10:2,11:2,12:1,13:3,14:3},
 "Quadratische Funktionen Aufgabenpool.html": {1:2,2:3,3:1,4:1,5:2,6:2,7:2,8:2,9:2,10:1,11:1,12:2,13:2,14:2,15:3},
 "Stochastik Aufgabenpool.html": {1:2,2:2,3:1,4:2,5:3,6:1,7:3,8:2,9:2,10:1,11:1,12:2,13:3,14:3,15:2},
 "Sachrechnen Aufgabenpool.html": {1:1,2:3,3:2,4:1,5:2,6:1,7:2,8:2,9:3,10:2,11:2,12:1,13:3,14:1,15:3},
 "Boxplot Aufgabenpool.html": {1:2,2:2,3:1,4:2,5:3,6:3,7:3,8:2,9:2,10:2,11:1,12:3,13:2,14:2,15:2},
}

EXTRA_CSS = """
 .stars{font-size:14px;letter-spacing:2px;color:#e8a800;margin-left:10px;white-space:nowrap}
 .stars .s0{color:#d4d8dc}
 @media print{
   .stars{display:none !important}
   .grid{grid-template-columns:1fr !important;gap:0 !important}
   .card{min-height:86mm;break-inside:avoid;page-break-inside:avoid;padding:7mm 9mm !important;margin:0 !important}
   .fig svg{max-height:46mm !important}
   .prob{min-height:0 !important}
 }
"""

def stars(d):
    return (f'<span class="stars" title="Schwierigkeit {d} von 3">'
            + '★' * d + '<span class="s0">' + '★' * (3 - d) + '</span></span>')

for fn, dmap in diffs.items():
    p = os.path.join(BASE, fn)
    with open(p) as f:
        html = f.read()
    if 'class="stars"' in html:
        print("skip (already patched):", fn)
        continue
    html = html.replace('</style>', EXTRA_CSS + '</style>', 1)
    for n, d in dmap.items():
        needle = f'<span class="num">Aufgabe {n}</span></div>'
        repl = f'<span class="num">Aufgabe {n}</span>{stars(d)}</div>'
        if needle not in html:
            print("  WARN: not found Aufgabe", n, "in", fn)
        html = html.replace(needle, repl, 1)
    with open(p, "w") as f:
        f.write(html)
    print("patched:", fn)
print("done")
