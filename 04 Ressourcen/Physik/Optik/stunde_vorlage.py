#!/usr/bin/env python3
"""Gemeinsame Bausteine für die Physik-Stunden-HTMLs (Optik 7c).
Aussehen = 'Optik – Do 24.09. – Stunde.html' (CSS wird von dort übernommen).
bau_stunde(...) schreibt die HTML im Vault, exportiere(...) die PDFs/HTML nach iCloud."""
import base64, re, shutil, subprocess
from pathlib import Path
from pypdf import PdfReader, PdfWriter

HIER = Path(__file__).parent
MAT = HIER / "Materialien"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ICL = Path("/Users/oskarklein/Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik/Physik Klasse 7/Optik 2026-27")
FOLIEN = re.findall(r'<section class="folie[^"]*">.*?</section>', (HIER / "Optik I.html").read_text(encoding="utf-8"), flags=re.S)
_REF = (HIER / "Optik – Do 24.09. – Stunde.html").read_text(encoding="utf-8")
MT_CSS = (".box h4{margin:12px 0 4px;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#66798e}"
          "table.mt{border-collapse:collapse;width:100%;font-size:15.5px;margin:0 0 6px;table-layout:fixed}"
          ".mt th{text-align:left;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:#66798e;border-bottom:1.5px solid #1b1b1b;padding:5px 8px}"
          ".mt td{border-bottom:1px solid #e3e5ea;padding:6px 8px;vertical-align:top}.mt td.anz{white-space:nowrap;font-weight:600}"
          ".mt td.leer{color:#8da6c2;font-style:italic}.mhinweis{margin:10px 0 4px;padding:8px 12px;border:1px solid #FF1F8A;background:#fff6fa;font-size:15px}")
_css = _REF[_REF.index("<style>\n*{box-sizing"):_REF.index("</style></head>")]
CSS = _css + ("" if "table.mt" in _css else MT_CSS) + "</style>"


def material_tabellen(material):
    """material = {"demo": [(Material, Anzahl, Hinweis)], "schueler": [...], "hinweis": "..."}"""
    def tab(xs):
        rows = "".join(f'<tr><td>{a}</td><td class="anz">{b}</td><td>{c}</td></tr>' for a, b, c in xs) \
            or '<tr><td colspan="3" class="leer">nicht nötig</td></tr>'
        return f'<table class="mt"><tr><th style="width:40%">Material</th><th style="width:90px">Anzahl</th><th>Hinweis</th></tr>{rows}</table>'
    h = f'<div class="mhinweis">{material["hinweis"]}</div>' if material.get("hinweis") else ""
    return (f'<h4>Demo (für dich)</h4>{tab(material.get("demo", []))}'
            f'<h4>Schülerversuch (pro Gruppe)</h4>{tab(material.get("schueler", []))}{h}')


# ------------------------------------------------------------------ Folien
def basis(p):
    """Ausgefüllte Folie aus Optik I (Seitenzahl = Seite in Optik I.pdf), ohne alte Austeil-Marker."""
    return re.sub(r'\s*<div class="ab-hinweis">.*?</div>', "", FOLIEN[p - 1], flags=re.S)


def ohne_merksatz(h):
    return re.sub(r'\s*<div class="merksatz[^"]*">.*?</div>', "", h, count=1, flags=re.S)


def mit_hinweis(h, text):
    i = h.rindex("</section>")
    return h[:i] + f'<div class="ab-hinweis">📄 {text}</div>' + h[i:]


def tabellenfolie(titel, zeilen, kopf=("im Alltag", "was man sieht", "warum"), frage=""):
    tab = ('<table class="atab"><colgroup><col style="width:27%"><col style="width:29%"><col></colgroup><tr>'
           + "".join(f"<th>{k}</th>" for k in kopf) + "</tr>"
           + "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a, b, c in zeilen) + "</table>")
    ms = f'<div class="merksatz"><b>Frage:</b> {frage}</div>' if frage else ""
    return f'<section class="folie"><div class="titelband"><h1>{titel}</h1></div><div class="zeichenzone karo">{tab}</div>{ms}</section>'


def versuchsfolie(titel, aufbau_svg, schritte, beobachtung, ergebnis):
    """Versuch im Stil deiner Folie „Versuch: Kern- und Halbschatten“ (ausgefüllt)."""
    li = "".join(f"<li>{s}</li>" for s in schritte)
    return ('<section class="folie">' f'<div class="titelband"><h1>{titel}</h1></div><div class="versuch">'
            f'<div class="zelle"><h2>Aufbau</h2><div class="feld karo">{aufbau_svg}</div></div>'
            f'<div class="zelle"><h2>Beschreibung</h2><div class="feld"><ol>{li}</ol></div></div>'
            f'<div class="zelle"><h2>Beobachtung</h2><div class="feld">{beobachtung}</div></div>'
            f'<div class="zelle"><h2>Ergebnis</h2><div class="feld">{ergebnis}</div></div></div></section>')


def blatt(pdf_name, key, hinweis):
    """Lösungsseite (Seite 2) des Schülerblatts als Bild, 1:1 wie auf dem Blatt."""
    subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", "2", "-l", "2", "-singlefile", str(MAT / pdf_name),
                    str(MAT / "assets" / f"blatt-{key}-loesung")], check=True)
    return ("blatt", f'<div class="austeil">📄 {hinweis}</div>'
                     f'<img class="blattbild" src="Materialien/assets/blatt-{key}-loesung.png" alt="">', pdf_name)


def chip(*nr):
    return "".join(f'<button class="fchip" data-go="f{n}">Folie {n}</button>' for n in nr)


# ------------------------------------------------------------------ HTML
def bau_stunde(datei, h1, sub, drucken, material, schritte, folge, hintergrund, blaetter_boxen):
    karten = "".join(
        (f'<div class="fnr">Folie {i} · Schülerblatt mit Lösung</div><div class="blattkarte" id="f{i}">{h[1]}</div>'
         if isinstance(h, tuple) else f'<div class="fnr">Folie {i}</div><div class="karte" id="f{i}">{h}</div>')
        for i, h in enumerate(folge, 1))
    zeit = "".join(f'<div class="z{i % 6}" style="flex:1">{i + 1} · {t}</div>' for i, (t, d, ks) in enumerate(schritte))
    zeilen = "".join(
        f'<div class="schr"><span class="n">{i}</span><div><b>{t}</b><br><span class="m">{d}</span></div>'
        f'<div class="go">{"".join(f"<button data-go=f{k}>Folie {k}</button>" for k in ks)}</div></div>'
        for i, (t, d, ks) in enumerate(schritte, 1))
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h1}</title>
<link rel="stylesheet" href="folien.css">
{CSS}</head><body>
<div class="wrap"><header class="kopf"><h1>{h1}</h1>
<p class="sub">{sub}</p></header></div>
<nav><div class="wrap tabs"><button data-t="ueb">Überblick</button><button data-t="folien">Folien</button><button data-t="hg">Hintergrund</button><button data-t="ab">Arbeitsblätter</button></div></nav>
<div class="wrap">
<div class="tab" id="t_ueb">
<div class="box"><h3>Drucken</h3><ul>{li(drucken)}</ul></div>
<div class="box"><h3>Material</h3>{material_tabellen(material)}</div>
<div class="box"><h3>Die Stunde</h3><div class="zeitleiste">{zeit}</div>{zeilen}</div>
</div>
<div class="tab" id="t_folien">{karten}</div>
<div class="tab" id="t_hg">{hintergrund}</div>
<div class="tab" id="t_ab">{blaetter_boxen}</div>
</div>
<script>
const tabs=[...document.querySelectorAll('nav button')],secs=[...document.querySelectorAll('.tab')];
function show(id){{tabs.forEach(b=>b.classList.toggle('on',b.dataset.t===id));secs.forEach(s=>s.classList.toggle('on',s.id==='t_'+id));history.replaceState(null,'','#'+id);requestAnimationFrame(()=>window.scrollTo(0,0))}}
tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));
document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{{show('folien');setTimeout(()=>document.getElementById(b.dataset.go).scrollIntoView(),60)}});
history.scrollRestoration='manual';
show(secs.some(s=>s.id==='t_'+location.hash.slice(1))?location.hash.slice(1):'ueb');
</script></body></html>"""
    (HIER / datei).write_text(html, encoding="utf-8")
    print("geschrieben:", datei, f"({len(html) // 1024} KB), Folien:", len(folge))


# ------------------------------------------------------------------ Kopiervorlage 2 auf 1
def zwei_auf_eins(html_name, pdf_name, feld="27mm", extra_css=""):
    src = (MAT / html_name).read_text(encoding="utf-8")
    a = src.index('<div class="seite">')
    b = src.index('<div class="seite">', a + 10)
    inner = src[a + len('<div class="seite">'):src.rindex("</div>", a, b)]
    inner = re.sub(r'<p class="frage">([^<]*<span class="luecke)', r'<p class="frage lt">\1', inner)
    zweit = inner.replace('id="', 'id="b_').replace("url(#", "url(#b_")
    css = ("<style>@page{size:A4 portrait;margin:0}html,body{margin:0}"
           ".haelfte{box-sizing:border-box;width:210mm;height:148.5mm;padding:8mm 13mm 6mm;overflow:hidden;position:relative;font-size:10pt;line-height:1.35}"
           ".haelfte + .haelfte{border-top:0.6pt dashed #7C8592;overflow:visible}"
           ".schere{position:absolute;left:4mm;top:-3.2mm;font-size:9pt;color:#7C8592;background:#fff;padding:0 1mm}"
           ".haelfte .kopf{padding-bottom:1.5mm;margin-bottom:2.5mm}.haelfte .kopf h1{font-size:13pt}"
           ".haelfte .namensfeld{margin-bottom:1mm;font-size:9pt}.haelfte h2.aufgabe{margin:2.5mm 0 1mm;font-size:10.5pt}"
           ".haelfte ol.liste{margin:0 0 1mm}.haelfte ol.liste li{margin-bottom:0.6mm}"
           ".haelfte .versuchskopf .versuchsskizze{flex:0 0 38mm;width:38mm;height:28mm;margin-top:5mm}"
           ".haelfte p.frage{margin:0 0 1mm}.haelfte .zeichenfeld{height:" + feld + "!important;margin:1mm 0 1mm}"
           ".haelfte .lt{line-height:2.25}.haelfte .luecke{min-width:36mm}" + extra_css + "</style>")
    tmp = MAT / ("_2auf1_" + html_name)
    tmp.write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><link rel="stylesheet" href="ab-vorlage.css">'
                   + css + f'</head><body><div class="haelfte">{inner}</div><div class="haelfte"><span class="schere">✂</span>{zweit}</div></body></html>',
                   encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={MAT / pdf_name}",
                    "--virtual-time-budget=4000", f"file://{tmp}"], check=True, capture_output=True)
    tmp.unlink()
    n = len(PdfReader(str(MAT / pdf_name)).pages)
    print("Kopiervorlage:", pdf_name, "Seiten:", n)
    return n


# ------------------------------------------------------------------ Export nach iCloud
def exportiere(folge, ordner, folien_pdf, ab_pdf, stunde_html, html_name, links):
    """Folien-PDF (Schülerblatt-Lösungen als A4-Seiten dazwischen), eigenständige HTML, Gesamt.pdf."""
    seiten, reihen = [], []
    for i, h in enumerate(folge):
        if isinstance(h, tuple):
            reihen.append(("blatt", h[2]))
            if seiten and reihen[-2][0] == "folie" and "ab-hinweis" not in seiten[-1]:
                seiten[-1] = mit_hinweis(seiten[-1], "Versuchsblatt austeilen")
            continue
        reihen.append(("folie", len(seiten)))
        seiten.append(h)
    extra = re.search(r"(\.atab\{.*?\}\.atab th\{.*?\})", CSS, re.S).group(1)
    exp, tmp = HIER / "_export.html", HIER / "_export.pdf"
    exp.write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><link rel="stylesheet" href="folien.css"><style>'
                   + extra + '</style></head><body>' + "".join(seiten) + "</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tmp}",
                    "--virtual-time-budget=5000", f"file://{exp}"], check=True, capture_output=True)
    fol = PdfReader(str(tmp))
    assert len(fol.pages) == len(seiten), (len(fol.pages), len(seiten))
    w = PdfWriter()
    for art, x in reihen:
        w.add_page(fol.pages[x] if art == "folie" else PdfReader(str(MAT / x)).pages[1])
    with open(ordner / folien_pdf, "wb") as f:
        w.write(f)
    exp.unlink(); tmp.unlink()
    # eigenständige HTML
    html = (HIER / html_name).read_text(encoding="utf-8")
    html = html.replace('<link rel="stylesheet" href="folien.css">', "<style>" + (HIER / "folien.css").read_text(encoding="utf-8") + "</style>")
    html = re.sub(r'(src|href)="((?:assets|Materialien/assets)/[^"]+\.(?:png|jpg))"',
                  lambda m: f'{m.group(1)}="data:image/{"png" if m.group(2).endswith("png") else "jpeg"};base64,'
                            f'{base64.b64encode((HIER / m.group(2)).read_bytes()).decode()}"', html)
    for alt, neu in links.items():
        html = html.replace(f'href="{alt}"', f'href="{neu}"')
    (ordner / stunde_html).write_text(html, encoding="utf-8")
    # Gesamt.pdf
    w = PdfWriter()
    for part in ["Materialliste.pdf", folien_pdf, ab_pdf]:
        w.append(str(ordner / part))
    with open(ordner / "Gesamt.pdf", "wb") as f:
        w.write(f)
    print(ordner.name, "| Folien:", len(PdfReader(str(ordner / folien_pdf)).pages), "| Gesamt:",
          len(PdfReader(str(ordner / "Gesamt.pdf")).pages), "|", stunde_html)


def materialliste(ordner, chip_text, titel, material):
    def tab(xs):
        rows = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a, b, c in xs) \
            or '<tr><td colspan="3" class="leer">nicht nötig</td></tr>'
        return f'<table style="table-layout:fixed"><tr><th style="width:40%">Material</th><th style="width:22mm">Anzahl</th><th>Hinweis</th></tr>{rows}</table>'
    p = ordner / "Materialliste.html"
    s = p.read_text(encoding="utf-8")
    kopf = s[:s.index("<h1>")]
    hw = f'<div class="hinweis">{material["hinweis"]}</div>' if material.get("hinweis") else ""
    p.write_text(kopf + f'<h1><span class="chip">{chip_text}</span>{titel} — Materialliste</h1>\n'
                 f'<h2>Demo-Material (für dich)</h2>\n{tab(material.get("demo", []))}\n'
                 f'<h2>Schülerversuch (pro Gruppe)</h2>\n{tab(material.get("schueler", []))}\n{hw}\n</body></html>', encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={ordner / 'Materialliste.pdf'}",
                    "--virtual-time-budget=3000", f"file://{p}"], check=True, capture_output=True)
