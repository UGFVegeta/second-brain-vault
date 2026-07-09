#!/usr/bin/env python3
# Ergänzt Schwierigkeitssterne in den .md-Aufgabenpools (analog patch_stars.py fürs HTML).
import os, re

BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben"

md_diffs = {
 "Trigonometrie Prüfungspool.md": {1:2,2:1,3:2,4:3,5:3,6:2,7:1,8:1,9:2,10:2,11:2,12:1,13:3,14:3},
 "Quadratische Funktionen Aufgabenpool.md": {1:2,2:3,3:1,4:1,5:2,6:2,7:2,8:2,9:2,10:1,11:1,12:2,13:2,14:2,15:3},
 "Stochastik Aufgabenpool.md": {1:2,2:2,3:1,4:2,5:3,6:1,7:3,8:2,9:2,10:1,11:1,12:2,13:3,14:3,15:2},
 "Sachrechnen Aufgabenpool.md": {1:1,2:3,3:2,4:1,5:2,6:1,7:2,8:2,9:3,10:2,11:2,12:1,13:3,14:1,15:3},
 "Boxplot Aufgabenpool.md": {1:2,2:2,3:1,4:2,5:3,6:3,7:3,8:2,9:2,10:2,11:1,12:3,13:2,14:2,15:2},
}

def stars(d):
    return "★" * d + "☆" * (3 - d)

for fn, dmap in md_diffs.items():
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        print("FEHLT:", fn); continue
    with open(p) as f:
        md = f.read()
    if "*Schwierigkeit:" in md:
        print("skip (schon vorhanden):", fn); continue
    added = 0
    for n, d in dmap.items():
        pat = re.compile(rf'(##\s*Aufgabe {n}\b[^\n]*\n)')
        new, cnt = pat.subn(rf'\1*Schwierigkeit: {stars(d)}*\n', md, count=1)
        if cnt:
            md = new; added += 1
        else:
            print(f"  WARN: '## Aufgabe {n}' nicht gefunden in {fn}")
    with open(p, "w") as f:
        f.write(md)
    print(f"patched: {fn} ({added}/{len(dmap)} Aufgaben)")
print("done")
