#!/usr/bin/env python3
"""Laufzettel Coopertest Klasse 5 bis 10: A4 hochkant, zwei Schüler pro Blatt (Schneidelinie), eine Seite pro Klassenstufe.
Einer läuft, einer zählt und kreuzt nach jeder 200-m-Runde ein Kästchen an. Nach 12 Minuten wird gewechselt.
Die Notenwerte kommen aus ../LA Sprengeltabelle Remstal (männlich).md (vorerst nur Jungen).
Aufruf: python3 baue_coopertest_zettel.py  -> Coopertest Laufzettel Klasse 5 bis 10.html/.pdf und ein PDF pro Klassenstufe"""
import base64, re, subprocess, tempfile
from pathlib import Path

HIER = Path(__file__).parent
VAULT = HIER.parents[2]
TABELLE = HIER.parent / "LA Sprengeltabelle Remstal (männlich).md"
FONTS = VAULT / "04 Ressourcen/Physik/Kernphysik/Materialien/assets/fonts"
LOGO = VAULT / "07 Anhänge/GDRS Logo.png"
RUNDE = 200
KAESTCHEN = 16          # 16 Runden = 3200 m, reicht über die Note 1 in Klasse 10 (2850 m)
LEISTE = ["1", "1,5", "2", "2,5", "3", "3,5", "4", "4,5", "5"]   # ganze Noten, dazu die halben


def werte():
    """{Klasse: {Note: Meter}} aus der Sprengeltabelle (letzte Spalte = Coopertest)."""
    s = TABELLE.read_text(encoding="utf-8")
    out = {}
    for blk in re.split(r"\n## ", s)[1:]:
        m = re.match(r"Klasse (\d+)", blk)
        if not m:
            continue
        zeilen = [l.split("|") for l in blk.split("\n") if l.startswith("| ") and "Note" not in l and "---" not in l]
        out[int(m.group(1))] = {z[1].strip(): int(z[-2].strip().replace(" m", "")) for z in zeilen}
    return out


def runden(m):
    r, rest = divmod(m, RUNDE)
    return f"{r} Rd." if not rest else f"{r} Rd. + {rest} m"


def b64(p):
    return base64.b64encode(p.read_bytes()).decode()


def haelfte(kl, tab):
    k = "".join(f'<div class="k"><span class="nr">{i}</span><span class="m">{i * RUNDE} m</span></div>' for i in range(1, KAESTCHEN + 1))
    leiste = "".join(f'<td><b>{n}</b><br>{tab[n]} m<br><span>{runden(tab[n])}</span></td>' for n in LEISTE)
    return f"""<section class="zettel">
<div class="kopf"><img src="data:image/png;base64,{LOGO_B64}" alt=""><div class="titel">Coopertest · Klasse {kl}</div>
<div class="info">12 Minuten laufen · 1 Runde = {RUNDE} m</div></div>
<div class="felder"><div class="f w2">Name</div><div class="f">Klasse</div><div class="f w2">gezählt von</div><div class="f">Datum</div></div>
<p class="anl">Zähler: Nach jeder vollen Runde ein Kästchen ankreuzen. Nach 12 Minuten die angefangene Runde bis zur letzten 50-m-Markierung ankreuzen.</p>
<div class="gitter">{k}</div>
<div class="rest"><b>angefangene Runde:</b><span class="cb"></span>50 m<span class="cb"></span>100 m<span class="cb"></span>150 m</div>
<div class="erg"><span>volle Runden</span><i></i><span>× {RUNDE} m +</span><i class="s"></i><span>m =</span><i class="l"></i><span>m</span><span class="note">Note</span><i class="s"></i></div>
<table class="leiste"><tr><th>Orientierung</th>{leiste}</tr></table>
</section>"""


CSS = """
@font-face{font-family:"Open Sans";font-weight:400;src:url(data:font/woff2;base64,__F400__) format("woff2")}
@font-face{font-family:"Open Sans";font-weight:600;src:url(data:font/woff2;base64,__F600__) format("woff2")}
@font-face{font-family:"Open Sans";font-weight:700;src:url(data:font/woff2;base64,__F700__) format("woff2")}
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Open Sans",sans-serif;color:#1d1d1b}
.blatt{width:210mm;height:297mm;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.blatt:last-child{page-break-after:auto}
.zettel{height:148.5mm;padding:8mm 11mm 6mm;display:flex;flex-direction:column}
.schnitt{height:0;border-top:1px dashed #9aa5b1;position:relative}
.schnitt::before{content:"✂";position:absolute;left:6mm;top:-3.2mm;font-size:11pt;color:#9aa5b1;background:#fff;padding:0 1mm}
.kopf{display:flex;align-items:center;gap:3mm}.kopf img{width:10mm;height:10mm}
.titel{font-size:17pt;font-weight:700;flex:1}.info{font-size:10pt;color:#4a5563;font-weight:600}
.felder{display:grid;grid-template-columns:2fr 1fr;gap:2.5mm 6mm;margin-top:4mm}
.f{border-bottom:1px solid #1d1d1b;height:8.5mm;font-size:8pt;color:#66798E;display:flex;align-items:flex-start}
.anl{font-size:8.5pt;color:#4a5563;margin:3mm 0 2.5mm}
.gitter{display:grid;grid-template-columns:repeat(8,1fr);gap:2mm}
.k{border:1.4px solid #1d1d1b;border-radius:2mm;height:21mm;position:relative}
.k .nr{position:absolute;left:1.8mm;top:.8mm;font-size:11pt;font-weight:700}
.k .m{position:absolute;right:1.6mm;bottom:.8mm;font-size:6.8pt;color:#8a95a3}
.rest{display:flex;align-items:center;gap:2mm;font-size:10.5pt;margin-top:4.5mm}.rest b{font-weight:600;margin-right:1mm}
.cb{display:inline-block;width:4.6mm;height:4.6mm;border:1.4px solid #1d1d1b;border-radius:1mm;margin-left:3mm}
.erg{display:flex;align-items:flex-end;gap:2mm;font-size:10.5pt;margin-top:4.5mm}
.erg i{display:inline-block;border-bottom:1px solid #1d1d1b;width:14mm;height:6mm}.erg i.s{width:12mm}.erg i.l{width:22mm}
.erg .note{margin-left:auto;font-weight:600}
.leiste{margin-top:auto;border-collapse:collapse;width:100%;table-layout:fixed;font-size:6.8pt;color:#66798E;text-align:center}
.leiste th{font-weight:600;text-align:left;padding-right:2mm;width:17mm;vertical-align:middle}
.leiste td{border-left:1px solid #D9DFE7;padding:.6mm .5mm;line-height:1.3}.leiste td b{color:#4a5563;font-size:7.5pt}
.leiste td span{white-space:nowrap}
"""


LOGO_B64 = b64(LOGO)


def main():
    tab = werte()
    css = CSS
    for g in (400, 600, 700):
        css = css.replace(f"__F{g}__", b64(FONTS / f"opensans-{g}.woff2"))
    fehlt = [(kl, n) for kl in range(5, 11) for n in LEISTE if n not in tab.get(kl, {})]
    if fehlt:
        raise SystemExit(f"Werte fehlen in der Sprengeltabelle: {fehlt}")
    def dokument(klassen):
        seiten = "".join(f'<div class="blatt">{haelfte(kl, tab[kl])}<div class="schnitt"></div>{haelfte(kl, tab[kl])}</div>' for kl in klassen)
        return f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Coopertest Laufzettel</title><style>{css}</style></head><body>{seiten}</body></html>'

    def drucken(html_datei, pdf):
        subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", html_datei.as_uri()], check=True, capture_output=True)

    ziel = HIER / "Coopertest Laufzettel Klasse 5 bis 10.html"
    ziel.write_text(dokument(range(5, 11)), encoding="utf-8")
    drucken(ziel, ziel.with_suffix(".pdf"))
    print("geschrieben:", ziel.name, "und", ziel.with_suffix(".pdf").name)
    with tempfile.TemporaryDirectory() as tmp:     # einzelne Klassenstufen nur als PDF
        for kl in range(5, 11):
            h = Path(tmp) / f"k{kl}.html"
            h.write_text(dokument([kl]), encoding="utf-8")
            drucken(h, HIER / f"Coopertest Laufzettel Klasse {kl}.pdf")
    print("geschrieben: Coopertest Laufzettel Klasse 5.pdf bis Klasse 10.pdf")


if __name__ == "__main__":
    main()
