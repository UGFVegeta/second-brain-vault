#!/usr/bin/env python3
"""Lokale Datei in Chrome zeigen, ohne Tabs zu stapeln.

Ist die Datei schon in einem Tab offen: diesen Tab neu laden und nach vorne holen,
weitere Tabs mit derselben Datei schließen. Sonst: neu öffnen.
Aufruf: python3 .scripts/chrome_zeigen.py <pfad> [<pfad> ...]
"""
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote, unquote


def osa(skript):
    return subprocess.run(["osascript", "-e", skript], capture_output=True, text=True).stdout.strip()


def chrome_laeuft():
    return osa('application "Google Chrome" is running') == "true"


def tabs():
    """[(fenster, tab, url)] aller Chrome-Tabs, Indizes 1-basiert."""
    roh = osa('set out to ""\ntell application "Google Chrome"\nrepeat with w from 1 to count of windows\n'
              'repeat with t from 1 to count of tabs of window w\nset out to out & w & (ASCII character 9) & t & (ASCII character 9) & (URL of tab t of window w) & (ASCII character 10)\n'
              'end repeat\nend repeat\nend tell\nreturn out')
    erg = []
    for z in roh.splitlines():
        teile = z.split("\t")
        if len(teile) == 3:
            erg.append((int(teile[0]), int(teile[1]), teile[2]))
    return erg


def ohne_anker(url):
    return unicodedata.normalize("NFC", unquote(url.split("#")[0].split("?")[0]))


def zeige(pfad):
    p = Path(pfad).resolve()
    ziel = unicodedata.normalize("NFC", "file://" + str(p))
    treffer = [(w, t) for w, t, u in tabs() if ohne_anker(u) == ziel] if chrome_laeuft() else []
    if not treffer:
        subprocess.run(["open", "-a", "Google Chrome", str(p)])
        return "geöffnet"
    w0, t0 = treffer[0]
    # Doppelte von hinten schließen, damit die Indizes stimmen
    for w, t in sorted(treffer[1:], reverse=True):
        osa(f'tell application "Google Chrome" to close tab {t} of window {w}')
    if any(w == w0 and t < t0 for w, t in treffer[1:]):
        t0 -= sum(1 for w, t in treffer[1:] if w == w0 and t < t0)
    osa(f'tell application "Google Chrome"\nset active tab index of window {w0} to {t0}\n'
        f'tell tab {t0} of window {w0} to reload\nset index of window {w0} to 1\nactivate\nend tell')
    return f"neu geladen ({len(treffer) - 1} doppelte geschlossen)" if len(treffer) > 1 else "neu geladen"


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(Path(a).name, "→", zeige(a))
