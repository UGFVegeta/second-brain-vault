#!/usr/bin/env python3
"""Erzeugt in jedem Ordner mit Word-Dateien eine '00 Übersicht.html', die den
Inhalt aller Word-Dateien (und, als reine Verlinkung, sonstiger Dateien) dieses
Ordners zeigt - ohne den Inhalt zu verändern. Nutzt mammoth (docx -> HTML),
weil mammoth im Gegensatz zu pandoc auch Inhalte aus Textboxen extrahiert, die
in diesen Unterrichtsvorbereitungen fast durchgehend verwendet werden.

Aufruf: python3 icloud_docx_uebersicht.py <Basisordner> [<Basisordner> ...]

Legt NICHTS an, löscht NICHTS, ändert KEINE bestehende Datei - schreibt pro
Ordner nur die eine neue Datei '00 Übersicht.html' (überschreibt eine eigene
vorherige Version bei erneutem Lauf).
"""
import base64
import html
import re
import sys
import traceback
from pathlib import Path

import mammoth

CSS = """
body{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;max-width:900px;
margin:0 auto;padding:28px 24px 60px;color:#1b1b1b;line-height:1.5}
h1{font-size:26px;margin:0 0 4px}
.pfad{color:#666;font-size:13.5px;margin:0 0 22px}
.hinweis{background:#f5f5f1;border-radius:8px;padding:10px 14px;font-size:13.5px;
color:#555;margin-bottom:26px}
.datei{border-top:3px solid #1b1b1b;margin:34px 0 0;padding-top:6px}
.datei h2{font-size:19px;background:#eee;padding:5px 10px;border-radius:5px;
display:inline-block}
.inhalt{margin-top:10px}
.inhalt table{border-collapse:collapse;margin:10px 0;width:100%}
.inhalt td,.inhalt th{border:1px solid #ccc;padding:5px 8px;vertical-align:top;
font-size:14.5px}
.inhalt img{max-width:100%;height:auto}
.fehler{color:#b3261e;font-style:italic}
.warnung{background:#fff6e0;border-left:4px solid #e0a100;padding:7px 12px;margin:8px 0;font-size:14px}
.warnung a{color:#8a5a00;font-weight:600}
.formel-platzhalter{display:inline-block;background:#fdf0d5;border:1px dashed #c9922c;border-radius:4px;padding:0 6px;color:#8a5a00;font-size:13px}
.weitere{margin-top:36px;padding-top:14px;border-top:1px solid #ddd;font-size:14px}
.weitere a{color:#1a56a0}
"""


import shutil
import subprocess

SOFFICE = shutil.which("soffice") or "/opt/homebrew/bin/soffice"


def pdf_erzeugen(docx_pfad: Path):
    """Erzeugt per LibreOffice (rein Kommandozeile, kein Fenster) ein PDF neben der
    docx: '<Name> (Formelansicht).pdf'. Nutzt eine vorhandene Datei erneut, wenn sie
    neuer ist als die docx. None bei Fehler."""
    ziel = docx_pfad.with_name(f"{docx_pfad.stem} (Formelansicht).pdf")
    if ziel.exists() and ziel.stat().st_mtime >= docx_pfad.stat().st_mtime:
        return ziel
    if not SOFFICE or not Path(SOFFICE).exists():
        return None
    try:
        subprocess.run(
            [SOFFICE, "--headless", "--norestore", "--convert-to", "pdf",
             "--outdir", str(docx_pfad.parent), str(docx_pfad)],
            check=True, capture_output=True, timeout=60,
        )
        roh = docx_pfad.with_suffix(".pdf")
        if roh.exists():
            roh.replace(ziel)
            return ziel
    except Exception:
        return None
    return None


def pdf_als_bilder(pdf_pfad: Path) -> str:
    """Rendert jede Seite des PDF als PNG (150 dpi) und gibt sie als eingebettete
    <img>-Tags zurueck - fuer Dateien, deren Formeln sich nicht als Text lesen lassen."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        praefix = str(Path(tmp) / "seite")
        try:
            subprocess.run(
                ["pdftoppm", "-r", "150", "-png", str(pdf_pfad), praefix],
                check=True, capture_output=True, timeout=60,
            )
        except Exception:
            return ""
        bilder = sorted(Path(tmp).glob("seite-*.png"))
        teile = []
        for b in bilder:
            data = base64.b64encode(b.read_bytes()).decode("ascii")
            teile.append(f'<img class="seitenbild" src="data:image/png;base64,{data}" alt="Seite">')
        return "".join(teile)


def bild_einbetten(image):
    with image.open() as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return {"src": f"data:{image.content_type};base64,{data}"}


def docx_zu_html(pfad: Path):
    with open(pfad, "rb") as f:
        result = mammoth.convert_to_html(
            f, convert_image=mammoth.images.img_element(bild_einbetten)
        )
    formeln_kaputt = any(
        "x-wmf" in m.message or "x-emf" in m.message or "OLEObject" in m.message
        for m in result.messages
    )
    return result.value, formeln_kaputt


def bauen(ordner: Path, basis: Path):
    docx_dateien = sorted(
        [p for p in ordner.iterdir() if p.is_file() and p.suffix.lower() == ".docx"
         and not p.name.startswith("~$")],
        key=lambda p: (p.stem.lower() != "ablauf", p.name.lower()),
    )
    andere = sorted(
        [p for p in ordner.iterdir() if p.is_file()
         and p.suffix.lower() in (".pptx", ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".heic")],
        key=lambda p: p.name.lower(),
    )
    if not docx_dateien and not andere:
        return None

    teile = []
    fehler = 0
    for d in docx_dateien:
        titel = html.escape(d.stem)
        warnung = ""
        try:
            inhalt, formeln_kaputt = docx_zu_html(d)
            if not inhalt.strip():
                inhalt = '<p class="fehler">(Datei enthält keinen per Skript lesbaren Text.)</p>'
            if formeln_kaputt:
                pdf_pfad = pdf_erzeugen(d)
                bild_html = pdf_als_bilder(pdf_pfad) if pdf_pfad else ""
                if bild_html:
                    inhalt = bild_html
                    warnung = ('<p class="warnung">&#9888; Diese Datei enthält Formeln (MathType). '
                               'Sie wird deshalb als Bild angezeigt, nicht als Text.</p>')
                else:
                    link = html.escape(d.name)
                    warnung = (f'<p class="warnung">&#9888; Diese Datei enthält Formeln (MathType), die hier '
                               f'nicht angezeigt werden können. '
                               f'<a href="{link}">Original in Word öffnen</a></p>')
        except Exception as e:
            inhalt = f'<p class="fehler">Konnte nicht gelesen werden: {html.escape(str(e))}</p>'
            fehler += 1
        teile.append(f'<div class="datei"><h2>{titel}</h2>{warnung}<div class="inhalt">{inhalt}</div></div>')

    weitere = ""
    if andere:
        links = "".join(
            f'<li><a href="{html.escape(str(a.name))}">{html.escape(a.name)}</a></li>'
            for a in andere
        )
        weitere = f'<div class="weitere"><b>Weitere Dateien in diesem Ordner:</b><ul>{links}</ul></div>'

    rel = ordner.relative_to(basis.parent)
    seite = f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">
<title>{html.escape(ordner.name)}</title><style>{CSS}</style></head><body>
<h1>{html.escape(ordner.name)}</h1>
<p class="pfad">{html.escape(str(rel))}</p>
<div class="hinweis">Automatisch aus den Word-Dateien dieses Ordners erzeugt, Inhalt unverändert.
Reihenfolge: Ablauf zuerst, dann alphabetisch.</div>
{"".join(teile)}
{weitere}
</body></html>"""
    ziel = ordner / "00 Übersicht.html"
    ziel.write_text(seite, encoding="utf-8")
    return len(docx_dateien), fehler


def main():
    basen = [Path(p) for p in sys.argv[1:]]
    if not basen:
        print(__doc__)
        sys.exit(1)
    gesamt_ordner = gesamt_docx = gesamt_fehler = 0
    fehlerhafte_dateien = []
    for basis in basen:
        for ordner in [basis] + [p for p in sorted(basis.rglob("*")) if p.is_dir()]:
            try:
                ergebnis = bauen(ordner, basis)
            except Exception:
                print("FEHLER in Ordner:", ordner)
                traceback.print_exc()
                continue
            if ergebnis:
                n, f = ergebnis
                gesamt_ordner += 1
                gesamt_docx += n
                gesamt_fehler += f
                if f:
                    fehlerhafte_dateien.append(str(ordner))
    print(f"{gesamt_ordner} Übersicht.html geschrieben, {gesamt_docx} Word-Dateien verarbeitet, "
          f"{gesamt_fehler} nicht lesbar.")
    if fehlerhafte_dateien:
        print("Ordner mit Lesefehlern:")
        for o in fehlerhafte_dateien:
            print(" -", o)


if __name__ == "__main__":
    main()
