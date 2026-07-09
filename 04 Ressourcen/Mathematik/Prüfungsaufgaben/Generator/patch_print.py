#!/usr/bin/env python3
import os
BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben"
files = ["Trigonometrie Aufgabenpool.html","Quadratische Funktionen Aufgabenpool.html",
         "Stochastik Aufgabenpool.html","Sachrechnen Aufgabenpool.html","Boxplot Aufgabenpool.html"]
EXTRA2 = """
 /* PRINT3 */
 @media print{
   h1{display:none !important}
   .card{min-height:86mm !important;padding:6mm 8mm !important}
   .fig svg{max-height:36mm !important}
 }
"""
for fn in files:
    p = os.path.join(BASE, fn)
    with open(p) as f:
        html = f.read()
    if "PRINT3" in html:
        print("skip:", fn); continue
    html = html.replace("</style>", EXTRA2 + "</style>", 1)
    with open(p, "w") as f:
        f.write(html)
    print("patched:", fn)
print("done")
