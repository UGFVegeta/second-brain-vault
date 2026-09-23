#!/usr/bin/env python3
"""Exportiert die Stunde (baue_folien_am_stueck.py) nach iCloud: Folien F1/F2 als PDF, Arbeitsblätter,
Materialliste, Gesamt.pdf und eine eigenständige Stunden-HTML. Aufruf: python3 export_icloud.py"""
import base64, re, runpy, shutil, subprocess
from pathlib import Path
from pypdf import PdfReader, PdfWriter

hier = Path(__file__).parent
g = runpy.run_path(str(hier / "baue_folien_am_stueck.py"))
FOLGE = g["FOLGE"]
ICL = Path("/Users/oskarklein/Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik/Physik Klasse 7/Optik 2026-27")
F1, F2 = ICL / "F1 Lichtquellen (W03)", ICL / "F2 Licht trifft auf einen Koerper (W04)"
F3, F4 = ICL / "F3 Lichtausbreitung und Blende (W05)", ICL / "F4 Kern- und Halbschatten (W06-07)"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAT = hier / "Materialien"
BL = {"lq": MAT / "Lichtquellen W03.pdf", "w04": MAT / "Licht trifft auf einen Koerper W04.pdf"}


def hinweis(h, text):
    i = h.rindex("</section>")
    return h[:i] + f'<div class="ab-hinweis">📄 {text}</div>' + h[i:]


# 1) Folien (ohne Schülerblätter) als eine HTML drucken
extra = re.search(r"(\.atab\{.*?\}\.atab th\{.*?\})", open(hier / "Optik – Do 24.09. – Stunde.html", encoding="utf-8").read(), re.S).group(1)
seiten, reihen = [], []
for i, h in enumerate(FOLGE, 1):
    if isinstance(h, tuple):
        reihen.append(("blatt", "lq" if "blatt-lq" in h[1] else "w04"))
        continue
    if i == 1:
        h = hinweis(h, "Arbeitsblatt Lichtquellen austeilen")
    if i == 9:
        h = hinweis(h, "Versuchsblatt austeilen")
    reihen.append(("folie", len(seiten)))
    seiten.append(h)
exp = hier / "_export_folien.html"
exp.write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><link rel="stylesheet" href="folien.css"><style>'
               '.bildzone{position:absolute;left:40.16pt;top:74pt;width:636.48pt;height:268pt}.bildzone svg{width:100%;height:100%;display:block}'
               + extra + '</style></head><body>' + "".join(seiten) + "</body></html>", encoding="utf-8")
tmp = hier / "_folien.pdf"
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tmp}",
                "--virtual-time-budget=5000", f"file://{exp}"], check=True, capture_output=True)
fol = PdfReader(str(tmp))
assert len(fol.pages) == len(seiten), (len(fol.pages), len(seiten))


def seitenliste(von, bis):  # Stunde-Positionen von..bis (1-basiert) als Seitenobjekte
    out = []
    for art, x in reihen[von - 1:bis]:
        out.append(fol.pages[x] if art == "folie" else PdfReader(str(BL[x])).pages[1])
    return out


def schreibe(pfad, seiten_):
    w = PdfWriter()
    for s in seiten_:
        w.add_page(s)
    with open(pfad, "wb") as f:
        w.write(f)


optik1 = PdfReader(str(hier / "Optik I.pdf"))
schreibe(F1 / "Folien F1.pdf", list(optik1.pages[0:10]) + seitenliste(1, 7))
schreibe(F2 / "Folien F2.pdf", seitenliste(8, len(FOLGE)))

# 2) Arbeitsblätter (aktueller Stand)
for src, ziel in [(MAT / "Lichtquellen W03.pdf", F1 / "Arbeitsblatt F1.pdf"),
                  (MAT / "Licht trifft auf einen Koerper W04.pdf", F2 / "Arbeitsblatt F2.pdf"),
                  (MAT / "Lichtausbreitung und Blende W05.pdf", F3 / "Arbeitsblatt F3.pdf"),
                  (MAT / "Kern- und Halbschatten W06.pdf", F4 / "Arbeitsblatt F4.pdf")]:
    shutil.copyfile(src, ziel)

# 3) Materiallisten F1/F2 auf Stand bringen
def ml(ordner, von, nach):
    p = ordner / "Materialliste.html"
    s = p.read_text(encoding="utf-8")
    for a, b in zip(von, nach):
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={ordner / 'Materialliste.pdf'}",
                    "--virtual-time-budget=3000", f"file://{p}"], check=True, capture_output=True)


ml(F1, ['<tr><td>Büroklammer + flache Schale Wasser</td><td>für den Einstiegsversuch (naturwissenschaftliche Arbeitsweise)</td></tr>\n<tr><td>ein Tropfen Spülmittel</td><td>zerstört die Oberflächenspannung, Klammer sinkt</td></tr>'],
       ['<tr><td>zwei unterschiedlich schwere Bälle</td><td>für den Einstieg (naturwissenschaftliche Arbeitsweise, Fallversuch)</td></tr>'])
s2 = (F2 / "Materialliste.html").read_text(encoding="utf-8")
neu2 = re.sub(r"<h2>Demo-Material \(für dich\)</h2>.*?</div>",
              "<h2>Demo-Material (für dich)</h2>\n<table><tr><th>Material</th><th>Hinweis</th></tr><tr><td colspan=\"2\" class=\"leer\">nicht nötig</td></tr></table>\n"
              "<h2>Schülermaterial (pro Gruppe)</h2>\n<table><tr><th>Material</th><th>Hinweis</th></tr>"
              "<tr><td>Ray-Box mit Stromanschluss</td><td>1×</td></tr><tr><td>weißes Blatt Papier</td><td>1×</td></tr>"
              "<tr><td>schwarzer oder dunkler Karton</td><td>1× (dunkelblau, dunkelgrün oder Tonpapier gehen auch)</td></tr>"
              "<tr><td>klare Glasscheibe</td><td>1×, Kanten abkleben</td></tr></table>\n"
              "<div class=\"hinweis\">Raum abdunkeln. Versuchsblatt vor dem Versuch austeilen (Folie 3 in Folien F2).</div>", s2, flags=re.S)
(F2 / "Materialliste.html").write_text(neu2, encoding="utf-8")
ml(F2, [], [])

# 4) Gesamt.pdf neu
for o in (F1, F2, F3, F4):
    w = PdfWriter()
    for part in ["Materialliste.pdf", next(o.glob("Folien F*.pdf")).name, next(o.glob("Arbeitsblatt F*.pdf")).name]:
        w.append(str(o / part))
    with open(o / "Gesamt.pdf", "wb") as f:
        w.write(f)

# 5) Eigenständige Stunden-HTML (CSS und Bilder eingebettet, PDF-Links auf die iCloud-Dateien)
html = (hier / "Optik – Do 24.09. – Stunde.html").read_text(encoding="utf-8")
html = html.replace('<link rel="stylesheet" href="folien.css">', "<style>" + (hier / "folien.css").read_text(encoding="utf-8") + "</style>")


def data(m):
    pfad = hier / m.group(2)
    typ = "image/png" if pfad.suffix == ".png" else "image/jpeg"
    return f'{m.group(1)}="data:{typ};base64,{base64.b64encode(pfad.read_bytes()).decode()}"'


html = re.sub(r'(src|href)="((?:assets|Materialien/assets)/[^"]+\.(?:png|jpg))"', data, html)
html = html.replace('href="Materialien/Lichtquellen W03.pdf"', 'href="../F1 Lichtquellen (W03)/Arbeitsblatt F1.pdf"')
html = html.replace('href="Materialien/Licht trifft auf einen Koerper W04.pdf"', 'href="Arbeitsblatt F2.pdf"')
(F2 / "Stunde Do 24.09.html").write_text(html, encoding="utf-8")

exp.unlink(); tmp.unlink()
for o in (F1, F2):
    print(o.name, "| Folien:", len(PdfReader(str(next(o.glob('Folien F*.pdf')))).pages), "| Gesamt:", len(PdfReader(str(o / 'Gesamt.pdf')).pages))
print("Stunde-HTML:", (F2 / "Stunde Do 24.09.html").stat().st_size // 1024, "KB")
