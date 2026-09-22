#!/usr/bin/env python3
"""Baut '00 Stunden – Übersicht.html' direkt im Ordner Stunden/: eine Seite mit
einem Tab je Themenordner (01 ... 08), die alle 'Ordner mit Übersicht' und
darunter alle 'Ordner mit Übersicht' aus den Unterordnern auflistet. Ein
Ordner "hat eine Übersicht", wenn dort eine 00 Übersicht.html liegt (gebaut
mit icloud_docx_uebersicht.py). Reine Verlinkung, kein Inhalt wird kopiert.

Aufruf: python3 icloud_docx_hub.py <Stunden-Ordner>
"""
import html
import sys
import urllib.parse
from pathlib import Path


def baum(ordner: Path, basis: Path, tiefe=0):
    """Liste <li> fuer diesen Ordner (wenn er eine Übersicht hat) + Kinder."""
    eig = ordner / "00 Übersicht.html"
    kinder = sorted(
        [p for p in ordner.iterdir() if p.is_dir() and not p.name.startswith(".")],
        key=lambda p: p.name.lower(),
    )
    kind_html = "".join(baum(k, basis, tiefe + 1) for k in kinder)
    if not eig.exists() and not kind_html:
        return ""
    rel = ordner.relative_to(basis)
    href = urllib.parse.quote(str(rel / "00 Übersicht.html")) if eig.exists() else None
    label = html.escape(ordner.name)
    if href:
        zeile = f'<a class="ordner" href="{href}">{label}</a>'
    else:
        zeile = f'<span class="ordner leer">{label}</span>'
    if kind_html:
        return f"<li>{zeile}<ul>{kind_html}</ul></li>"
    return f"<li>{zeile}</li>"


CSS = """
*{box-sizing:border-box}
body{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;margin:0;color:#1b1b1b;background:#fff}
.wrap{max-width:900px;margin:0 auto;padding:0 22px 60px}
header{padding:26px 0 10px;border-bottom:2px solid #1b1b1b}
h1{font-size:24px;margin:0 0 4px}
.sub{color:#555;margin:0;font-size:14px}
nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #d9d9d4;z-index:5;
overflow-x:auto;white-space:nowrap}
nav .n{display:flex;gap:6px;padding:9px 0;max-width:900px;margin:0 auto;padding-left:22px;padding-right:22px}
nav button{padding:5px 13px;border-radius:16px;border:1px solid #d9d9d4;background:#f1f1ed;
font-size:13.5px;cursor:pointer;color:#1b1b1b}
nav button.aktiv{background:#1b1b1b;color:#fff;border-color:#1b1b1b}
section{display:none;padding-top:18px}
section.aktiv{display:block}
ul{list-style:none;margin:0;padding-left:0}
section>ul{padding-left:0}
li{margin:3px 0}
li ul{padding-left:22px;border-left:1.5px solid #e2e2da;margin-left:5px}
a.ordner{display:inline-block;padding:4px 9px;border-radius:6px;color:#154a8a;
text-decoration:none;font-size:15px}
a.ordner:hover{background:#eef3fb}
span.leer{display:inline-block;padding:4px 9px;color:#999;font-size:15px}
</style>
"""


def main():
    basis = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    themen = sorted(
        [p for p in basis.iterdir() if p.is_dir() and not p.name.startswith(".")],
        key=lambda p: p.name.lower(),
    )
    tabs, sektionen = [], []
    for i, t in enumerate(themen):
        inhalt = baum(t, basis)
        if not inhalt:
            continue
        aktiv = " aktiv" if i == 0 or (not tabs) else ""
        tid = f"t{len(tabs)}"
        tabs.append(f'<button data-t="{tid}" class="{aktiv.strip()}">{html.escape(t.name)}</button>')
        sektionen.append(f'<section id="{tid}" class="{aktiv.strip()}"><ul>{inhalt}</ul></section>')
    if tabs:
        tabs[0] = tabs[0].replace('class=""', 'class="aktiv"') if 'class=""' in tabs[0] else tabs[0]

    seite = f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">
<title>Stunden – Übersicht</title><style>{CSS}</style></head><body>
<div class="wrap"><header><h1>Mathematik Klasse 7 &ndash; Stunden</h1>
<p class="sub">Ein Klick pro Ordner statt Word zu öffnen. Graue Namen haben (noch) keine Übersicht.</p></header></div>
<nav><div class="n">{"".join(tabs)}</div></nav>
<div class="wrap">{"".join(sektionen)}</div>
<script>
document.querySelectorAll('nav button').forEach(function(b){{
  b.addEventListener('click', function(){{
    document.querySelectorAll('nav button').forEach(x=>x.classList.remove('aktiv'));
    document.querySelectorAll('section').forEach(x=>x.classList.remove('aktiv'));
    b.classList.add('aktiv');
    document.getElementById(b.dataset.t).classList.add('aktiv');
  }});
}});
</script>
</body></html>"""
    ziel = basis / "00 Stunden – Übersicht.html"
    ziel.write_text(seite, encoding="utf-8")
    print("geschrieben:", ziel, "|", len(tabs), "Tabs")


if __name__ == "__main__":
    main()
