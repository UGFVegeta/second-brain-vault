#!/usr/bin/env python3
"""Gruppe B der Klassenarbeit in der Kästchen-Variante: nimmt das Layout der Variante von Gruppe A
(Mathe 7c – … – Entwurf mit Variante.html, Tab B) und setzt die Aufgaben aus baue_ka1_7c_B.py ein.
Schreibt eine Druck-HTML (nur Aufgaben, 4 A4-Seiten) und die Gruppe-B-Lösung als eigene HTML."""
import re
from pathlib import Path
H = Path(__file__).parent
VAR_A = (H / "Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Entwurf mit Variante.html").read_text(encoding="utf-8")
GEN_B = (H / "Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Gruppe B – Entwurf.html").read_text(encoding="utf-8")

arbeit_b = GEN_B[GEN_B.index('<div class="trenner" id="arbeit">'):GEN_B.index('<div class="trenner" id="loesung"')]
# Block aus Variante A
i = VAR_A.index('<div id="tabB"')
block = VAR_A[i:VAR_A.index('<script>', i)]

def ers(muster, neu, text, flags=re.S):
    r, n = re.subn(muster, lambda m: neu, text, count=1, flags=flags)
    assert n == 1, muster
    return r

def stueck(muster, quelle):
    m = re.search(muster, quelle, flags=re.S)
    assert m, muster
    return m.group(0)

# Kopf
block = block.replace('<u>Klassenarbeit Nr. 1</u>', '<u>Klassenarbeit Nr. 1 (Gruppe B)</u>')
# Nr. 1 Zahlenstrahl samt Antwortzeile, Nr. 2, Nr. 3
for muster in (r'<svg class="zs".*?</svg><div class="zsantw">.*?</div>(?=<div class="balken"><b>Nr. 2)',
               r'<div class="vgl">.*?</div>(?=<div class="snr">)',
               r'<table class="pn">.*?</table>'):
    block = ers(muster, stueck(muster, arbeit_b), block)

# Nr. 4, 5, 6: Aufgaben der Zeilen nacheinander ersetzen
listen = re.findall(r'<div class="liste[^"]*">(.*?)</div>(?=<div class="karo")', arbeit_b, flags=re.S)
items = []
for l in listen:
    items += re.findall(r'<span>([a-h]\) &nbsp;.*?)</span>(?=<span>[a-h]\)|$)', l, flags=re.S)
assert len(items) == 17, len(items)
it = iter(items)
def zeile(m):
    x = next(it)
    return f'<div class="au"><div class="zeile{" bruch" if "class=\"br\"" in x else ""}">{x}</div></div>'
block, n = re.subn(r'<div class="au"><div class="zeile[^"]*">.*?</div></div>', zeile, block, flags=re.S)
assert n == 17, n

# Nr. 7 und 8
muster7 = r'<div class="sach">.*?</div></div>(?=<div class="karo")'
block = ers(muster7, stueck(muster7, arbeit_b), block)
muster8 = r'<div class="balken"><b>Nr. 8</b>.*?(?=<div class="karo")'
block = ers(muster8, stueck(muster8, arbeit_b), block)

# Druck-HTML: nur dieser Block sichtbar
head = VAR_A[:VAR_A.index('<body>') + 6]
head = head.replace('</style>', '#tabA,.tabs,.leiste{display:none !important}#tabB{display:block !important}</style>', 1)
head = head.replace('<title>Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Entwurf</title>', '<title>Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Gruppe B</title>')
block = block.replace('<div id="tabB" hidden>', '<div id="tabB">')
(H / "_ka_B_kaestchen_druck.html").write_text(head + block + '</body></html>', encoding="utf-8")
print("ok")
