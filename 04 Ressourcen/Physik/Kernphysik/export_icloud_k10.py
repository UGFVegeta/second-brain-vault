#!/usr/bin/env python3
"""Export Kernphysik Klasse 10 nach iCloud: GDRS ICloud/Physik/Physik Klasse 10/Kernphysik 2026-27/
Pro Stunde ein Ordner „Wxx Titel“ mit
  - Folien Wxx.pdf   (Beamer-Folien in der Reihenfolge der Stunde, Schülerblatt-Lösungen als A4-Seite dazwischen)
  - Stunde Wxx.html  (eigenständig: CSS und Bilder eingebettet, Links auf Blätter und Labore angepasst)
  - die Arbeitsblätter der Stunde als PDF
Dazu Labore/ (alle Labore), Begleitheft Kernspaltung in W16, Klassenarbeit Nr. 1 in „W10 Klassenarbeit“.
Aufruf: python3 export_icloud_k10.py"""
import base64, re, shutil, subprocess, sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

HIER = Path(__file__).parent
MAT = HIER / "Materialien"
OPTIK = HIER.parent / "Optik"
ZIEL = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik/Physik Klasse 10/Kernphysik 2026-27"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(OPTIK))
import baue_stunden_k10 as t1  # noqa: E402
import baue_stunden_k10_teil2 as t2  # noqa: E402

LABORE = sorted(p.name for p in HIER.glob("*labor*.html")) + ["Kernphysik-Labore.html"]


def stunden():
    from stunde_vorlage import mit_labor, labore_der_stunde, stilisiere
    for datei, h1, sub, _d, _m, sch, folge, hg, ab in t1.STUNDEN:
        yield datei, h1, sub, stilisiere(mit_labor(folge, sch, labore_der_stunde(hg, ab))[0], h1, sub)
    for kurz, h1, sub, _b, _m, sch, folge, hg, ab in t2.STUNDEN:
        yield f"Kernphysik – {kurz} – Stunde.html", h1, sub, stilisiere(mit_labor(folge, sch, labore_der_stunde(hg, ab))[0], h1, f"Klasse 10 · Physik · {sub}")


def einbetten(html):
    """CSS inline, Bilder (png/jpg) als data-URI, relativ zum Kernphysik-Ordner."""
    html = html.replace('<link rel="stylesheet" href="../Optik/folien.css">',
                        "<style>" + (OPTIK / "folien.css").read_text(encoding="utf-8") + "</style>")

    def ersetze(m):
        pfad = (HIER / m.group(2)).resolve()
        if not pfad.exists():
            return m.group(0)
        art = "png" if pfad.suffix == ".png" else "jpeg"
        return f'{m.group(1)}="data:image/{art};base64,{base64.b64encode(pfad.read_bytes()).decode()}"'
    return re.sub(r'(src|href)="((?:\.\./Optik/)?(?:Materialien/)?assets/[^"]+\.(?:png|jpg))"', ersetze, html)


def folien_pdf(folge, ziel):
    """Folien als Seiten; bei Schülerblättern die Lösungsseite (Seite 2) des PDFs, beim Begleitheft das Lösungsbild als Folie."""
    stapel, reihen = [], []
    for h in folge:
        if isinstance(h, tuple) and h[2] != t2.HEFT:
            reihen.append(("blatt", h[2]))
            continue
        html = h if not isinstance(h, tuple) else ('<section class="folie"><div style="position:absolute;inset:14pt;display:flex;'
                                                   'align-items:center;justify-content:center">' + re.sub(r'<div class="austeil">.*?</div>', "", h[1]).replace('class="blattbild', 'style="max-width:100%;max-height:376pt" class="x') + "</div></section>")
        reihen.append(("folie", len(stapel)))
        stapel.append(html)
    exp, tmp = HIER / "_export.html", HIER / "_export.pdf"
    exp.write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><link rel="stylesheet" href="../Optik/folien.css">'
                   f"<style>{t1.KERN_CSS}</style></head><body>" + "".join(stapel) + "</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tmp}",
                    "--virtual-time-budget=6000", exp.as_uri()], check=True, capture_output=True)
    fol = PdfReader(str(tmp))
    assert len(fol.pages) == len(stapel), (ziel.name, len(fol.pages), len(stapel))
    w = PdfWriter()
    for art, x in reihen:
        w.add_page(fol.pages[x] if art == "folie" else PdfReader(str(MAT / x)).pages[1])
    with open(ziel, "wb") as f:
        w.write(f)
    exp.unlink()
    tmp.unlink()
    return len(w.pages)


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    (ZIEL / "Labore").mkdir(exist_ok=True)
    for lab in LABORE:
        shutil.copy(HIER / lab, ZIEL / "Labore" / lab)
    for datei, h1, sub, folge in stunden():
        w = re.search(r"W\d\d", sub).group(0)
        ordner = ZIEL / f"{w} {h1.replace('Kernphysik: ', '').replace('?', '').replace(':', ' –')}"
        ordner.mkdir(exist_ok=True)
        html = (HIER / datei).read_text(encoding="utf-8")
        blaetter = {h[2] for h in folge if isinstance(h, tuple) and (MAT / h[2]).exists()}  # auch Blätter, die nur als Folie vorkommen
        for pdf in sorted(set(re.findall(r'href="Materialien/([^"]+\.pdf)"', html)) | blaetter):
            shutil.copy(MAT / pdf, ordner / pdf)
            html = html.replace(f'href="Materialien/{pdf}"', f'href="{pdf}"')
        for lab in LABORE:
            html = html.replace(f'href="{lab}"', f'href="../Labore/{lab}"')
        (ordner / f"Stunde {w}.html").write_text(einbetten(html), encoding="utf-8")
        n = folien_pdf(folge, ordner / f"Folien {w}.pdf")
        print(f"{ordner.name} | Folien: {n} | Blätter: {len(list(ordner.glob('*.pdf'))) - 1}")
    ka = ZIEL / "W10 Klassenarbeit Nr. 1"
    ka.mkdir(exist_ok=True)
    kad = HIER.parent / "Klassenarbeiten"
    for p in kad.glob("Klassenarbeit Nr. 1 Klasse 10 Kernphysik 2026*"):
        if p.suffix in (".pdf", ".html"):
            shutil.copy(p, ka / p.name)
    print("Labore:", len(LABORE), "| Klassenarbeit:", sorted(p.name for p in ka.iterdir()))


if __name__ == "__main__":
    main()
