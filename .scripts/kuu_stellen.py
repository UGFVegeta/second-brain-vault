#!/usr/bin/env python3
"""Prüft die Stellenteile des Amtsblatts 'Kultus und Unterricht' (BW) auf
Funktionsstellen im Raum Rems-Murr / Schulamtsbezirk Backnang.

Sucht vor allem Konrektorstellen an Realschulen und Schulverbünden, meldet
aber auch Rektorstellen, damit Kaskaden sichtbar werden.

Aufruf:
    python3 .scripts/kuu_stellen.py            # nur neue Hefte
    python3 .scripts/kuu_stellen.py --alle     # auch schon gesehene Hefte
    python3 .scripts/kuu_stellen.py --reset    # Merkliste leeren
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import urllib.request

INDEX = "https://km.baden-wuerttemberg.de/de/service/stellenangebote/kultus-und-unterricht"
BASIS = "https://km.baden-wuerttemberg.de"
STATE = os.path.expanduser("~/.config/claude-kuu/gesehen.txt")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"

# Postleitzahlen im Rems-Murr-Kreis und direktem Umfeld
PLZ = re.compile(r"\b(713\d\d|714\d\d|715\d\d|716\d\d|7353\d|7355\d|736\d\d)\b")
FUNKTION = re.compile(r"Konrektor|Rektor", re.I)


def hole(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def hefte() -> list[str]:
    """Liefert die PDF-Links der aktuellen Stellenteile."""
    html = hole(INDEX).decode("utf-8", "replace")
    roh = re.findall(r'href="([^"]*Kultus_und_Unterricht[^"]*\.pdf)"', html)
    links = []
    for l in roh:
        if l.startswith("http"):
            links.append(l)
        else:
            links.append(BASIS + l)
    return sorted(set(links))


def gesehen() -> set[str]:
    if not os.path.exists(STATE):
        return set()
    with open(STATE, encoding="utf-8") as f:
        return {z.strip() for z in f if z.strip()}


def merken(url: str) -> None:
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "a", encoding="utf-8") as f:
        f.write(url + "\n")


def treffer(pdf: bytes) -> list[str]:
    """Gibt Textblöcke zurück, die eine relevante PLZ und eine Funktion nennen."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf)
        pfad = tmp.name
    try:
        txt = subprocess.run(
            ["pdftotext", "-layout", pfad, "-"],
            capture_output=True, text=True, check=True,
        ).stdout
    finally:
        os.unlink(pfad)

    zeilen = txt.splitlines()
    gefunden = []
    for i, z in enumerate(zeilen):
        if not PLZ.search(z):
            continue
        block = "\n".join(zeilen[i:i + 4])
        if FUNKTION.search(block):
            gefunden.append(block.rstrip())
    return gefunden


def main() -> int:
    alle = "--alle" in sys.argv
    if "--reset" in sys.argv:
        if os.path.exists(STATE):
            os.unlink(STATE)
        print("Merkliste geleert.")
        return 0

    bekannt = set() if alle else gesehen()
    neu = [h for h in hefte() if h not in bekannt]

    if not neu:
        print("Keine neuen Hefte.")
        return 0

    for url in neu:
        name = url.rsplit("/", 1)[-1]
        try:
            gef = treffer(hole(url))
        except Exception as e:
            print(f"FEHLER bei {name}: {e}")
            continue

        print(f"\n=== {name} ===")
        if gef:
            print(f"{len(gef)} Treffer im Raum Rems-Murr:\n")
            for b in gef:
                print(b)
                print("-" * 60)
        else:
            print("Nichts im Raum Rems-Murr.")

        if not alle:
            merken(url)

    print(f"\nQuelle: {INDEX}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
