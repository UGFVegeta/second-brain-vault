#!/usr/bin/env python3
"""Wandelt die Bildschirmfotos (PNG) aus bilder_erzeugen.py in kleine WebP-Dateien für bilder/ um."""
import glob, os, sys
from PIL import Image
SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sp/shots"
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder")
os.makedirs(DST, exist_ok=True)
for p in sorted(glob.glob(SRC + "/*.png")):
    n = os.path.basename(p)[:-4]
    if n.startswith("_") or n == "druck": continue
    im = Image.open(p).convert("RGB")
    if im.width > 1500: im = im.resize((1300, round(im.height * 1300 / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, n + ".webp"), "WEBP", quality=80, method=6)
    print(n, im.size)
