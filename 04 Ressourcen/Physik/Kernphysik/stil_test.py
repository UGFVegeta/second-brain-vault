#!/usr/bin/env python3
"""Stil-Test V1: nimmt eine fertige Stunden-HTML, setzt body.stil-v1 + folien_stil_v1.css und formt die Titel
(kleine Kopfzeile + großer Titel). Original bleibt unverändert, Ausgabe „… (Stil-Test).html“.
Aufruf: python3 stil_test.py "Kernphysik – W06 Wuerfelmodell – Stunde.html" Kernphysik"""
import base64, re, sys
from pathlib import Path

HIER = Path(__file__).resolve().parent


def titel(h1, fach):
    m = re.fullmatch(r"Lösung: Check zu Leitfrage (\d+)", h1)
    if m:
        return f'<span class="eyebrow">Lösung · Check</span>Leitfrage {m.group(1)}'
    m = re.fullmatch(r"Check zu Leitfrage (\d+)", h1)
    if m:
        return f'<span class="eyebrow">Check · {fach}</span>Leitfrage {m.group(1)}'
    m = re.match(r"(\d+)\.\d+ ", h1)
    if m:
        return f'<span class="eyebrow">{fach} · Leitfrage {m.group(1)}</span>{h1}'
    return f'<span class="eyebrow">{fach}</span>{h1}'


def umbauen(html, fach):
    html = re.sub(r'(<div class="titelband">\s*<h1>)(.*?)(</h1>)', lambda m: m.group(1) + titel(m.group(2).strip(), fach) + m.group(3), html, flags=re.S)
    # CSS eingebettet, damit die Datei auch in Obsidian und nach dem Kopieren richtig aussieht
    optik = HIER.parent / "Optik"
    html = html.replace('<link rel="stylesheet" href="../Optik/folien.css">',
                        "<style>" + (optik / "folien.css").read_text(encoding="utf-8") + "</style><style>"
                        + (optik / "folien_stil_v1.css").read_text(encoding="utf-8") + "</style>", 1)
    # Bilder als data-URI, sonst fehlen sie in Obsidian
    def bild(m):
        pfad = (HIER / m.group(2)).resolve()
        if not pfad.exists():
            return m.group(0)
        art = "png" if pfad.suffix == ".png" else "jpeg"
        return f'{m.group(1)}="data:image/{art};base64,{base64.b64encode(pfad.read_bytes()).decode()}"'
    html = re.sub(r'(src)="([^"]+\.(?:png|jpg))"', bild, html)
    return re.sub(r"<body([^>]*)>", lambda m: f'<body{m.group(1)} class="stil-v1">' if "class=" not in m.group(1)
                  else m.group(0).replace('class="', 'class="stil-v1 '), html, count=1)


if __name__ == "__main__":
    quelle, fach = HIER / sys.argv[1], sys.argv[2]
    ziel = quelle.with_name(quelle.stem + " (Stil-Test).html")
    ziel.write_text(umbauen(quelle.read_text(encoding="utf-8"), fach), encoding="utf-8")
    print("geschrieben:", ziel.name)
