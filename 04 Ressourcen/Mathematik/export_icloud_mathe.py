#!/usr/bin/env python3
"""Export Mathe 7c und 10b in die iCloud (GDRS ICloud/Schuljahr 26 27/Mathematik/…).
1. Fehlende Folien-PDFs bauen: Woche 2 (Merkheft-Folie „Plus und Minus“ in das bestehende Folien-PDF eingefügt),
   Woche 7 (gemischte Aufgaben), 10b Woche 4 (Zinsen, Zinseszins). Woche 3 baut baue_woche3.py selbst.
2. PDFs in die Themenordner kopieren. Was dort schon liegt und sich geändert hat, wandert vorher nach „_alt“.
3. Gesamt-HTML in den Hauptordner (Mathematik 7c bzw. Mathematik 10b): die Übersicht als EINE Datei, alle Stunden
   und Bilder eingebettet (iframe srcdoc, Bilder als data-URI), damit sie aus der iCloud heraus funktioniert.
Vorher die Bauskripte laufen lassen (baue_woche3.py, baue_woche7.py, baue_zins10.py, baue_uebersicht_mathe7/10.py).
Aufruf: python3 export_icloud_mathe.py"""
import base64, datetime, filecmp, json, re, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import unquote

from pypdf import PdfReader, PdfWriter

HIER = Path(__file__).resolve().parent
RZ = HIER / "Rationale Zahlen"
PZ = HIER / "Prozentrechnung Klasse 10"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Schuljahr 26 27/Mathematik"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(RZ))
sys.path.insert(0, str(PZ))
import baue_woche3 as w3  # noqa: E402
import baue_woche7 as w7  # noqa: E402
import baue_woche4 as w4  # noqa: E402
import baue_woche4_division as w4d  # noqa: E402
import baue_zins10 as z10  # noqa: E402
import baue_ka1_7c as ka1  # noqa: E402
import baue_zuwachs10 as zw10  # noqa: E402
import baue_uebung_ka1_7c as uka1  # noqa: E402
import baue_uebung_ka1_10b as uka10  # noqa: E402
from rezepte_rz import MERK_PLUSMINUS  # noqa: E402

CSS = w3.FCSS + w3.FOLIEN_CSS + w7.PDF_LUECKEN_CSS
import mathe_woche_vorlage as _v  # noqa: E402
A4_CSS = ("@page{size:A4;margin:0}@page quer{size:A4 landscape;margin:0}.seite.quer{page:quer;width:297mm}*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}"
          "body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;color:#1b1b1b;font-size:17px;line-height:1.4}"
          ".seite{width:210mm;padding:11mm 13mm;break-after:page}.seite:last-child{break-after:auto}"
          ".seite>h1{font-size:24px;margin:0 0 12px;border-bottom:2px solid #1b1b1b;padding-bottom:4px}"
          + _v.EXTRA.replace("<style>", "").replace("</style>", "") + w7.EXTRA_CSS.replace("<style>", "").replace("</style>", "")
          + ".mb{gap:22px}.mz{font-size:19px;margin:2px 0}.mz svg{max-width:330px}.mz-trenn{height:6px}.rezept{margin:0 0 10px;font-size:15px}.rezept h4{font-size:17px}.rs li{margin:2px 0}"
          ".block{margin:4px 0 12px}.block h4{font-size:16px;margin:0 0 4px}.ex.raster li{margin:1px 0}" + w7.PDF_LUECKEN_CSS)


def a4_zu_pdf(seiten, basis, ziel, quer=(), extra_css=""):
    """Seiten [(Titel, HTML)] als DIN-A4-Hochformat. Läuft eine Seite über, entsteht eine Seite mehr -> Abbruch.
    extra_css: zusätzliche Stile der Stunde (mit oder ohne <style>-Hülle)."""
    tmp_html, tmp_pdf = basis / "_export_a4.html", basis / "_export_a4.pdf"
    extra = extra_css.replace("<style>", "").replace("</style>", "")
    tmp_html.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><style>{A4_CSS}{extra}</style></head><body>'
                        + "".join(f'<div class="seite{" quer" if t in quer else ""}"><h1>{t}</h1>{h}</div>' for t, h in seiten) + "</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tmp_pdf}",
                    "--virtual-time-budget=4000", tmp_html.as_uri()], check=True, capture_output=True)
    n = len(PdfReader(str(tmp_pdf)).pages)
    assert n == len(seiten), (ziel.name, n, len(seiten), "eine Seite ist zu lang")
    shutil.move(tmp_pdf, ziel)
    tmp_html.unlink()
    return n


def folien_zu_pdf(folien, basis, ziel):
    """Folien [(Titel, HTML)] im Folienformat 13,333 × 7,5 in als PDF. basis = Ordner, gegen den Bildpfade aufgelöst werden."""
    tmp_html, tmp_pdf = basis / "_export_folien.html", basis / "_export_folien.pdf"
    tmp_html.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
                        + "".join(f'<div class="slide"><h1>{t}</h1>{h}</div>' for t, h in folien) + "</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tmp_pdf}",
                    "--virtual-time-budget=4000", tmp_html.as_uri()], check=True, capture_output=True)
    seiten = len(PdfReader(str(tmp_pdf)).pages)
    assert seiten == len(folien), (ziel.name, seiten, len(folien))      # keine Folie läuft über
    shutil.move(tmp_pdf, ziel)
    tmp_html.unlink()
    return seiten


def html_zu_pdf(html, n, ziel):
    """Fertiges HTML-Dokument (Klassenarbeit, Übungsarbeit) als PDF. n = erwartete Seitenzahl, sonst Abbruch."""
    tmp_html, tmp_pdf = ziel.parent / "_export_ka.html", ziel.parent / "_export_ka.pdf"
    tmp_html.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tmp_pdf}",
                    "--virtual-time-budget=4000", tmp_html.as_uri()], check=True, capture_output=True)
    seiten = len(PdfReader(str(tmp_pdf)).pages)
    assert seiten == n, (ziel.name, seiten, n, "eine Seite ist zu lang")
    shutil.move(tmp_pdf, ziel)
    tmp_html.unlink()
    return seiten


def woche2_pdf():
    """Bestehendes Folien-PDF Rationale Zahlen 2 + Merkheft-Folie „Plus und Minus“ nach Seite 1 (Wohin geht der Bogen?)."""
    alt = RZ / "Rationale Zahlen 2 – Folien für den Beamer.pdf"
    neu = RZ / "Mathe 7c – Woche 2 – Folien für den Beamer.pdf"
    merk = RZ / "_merk_pm.pdf"
    folien_zu_pdf([("Merkheft: Plus und Minus", w3.HEFT(MERK_PLUSMINUS))], RZ, merk)
    r, w = PdfReader(str(alt)), PdfWriter()
    w.add_page(r.pages[0])
    w.add_page(PdfReader(str(merk)).pages[0])
    for s in r.pages[1:]:
        w.add_page(s)
    with open(neu, "wb") as f:
        w.write(f)
    merk.unlink()
    return neu


def pdf_text(pfad):
    """Inhalt eines PDFs zum Vergleichen (neu gebaute PDFs unterscheiden sich sonst nur im Zeitstempel)."""
    r = PdfReader(str(pfad))
    return len(r.pages), [seite.extract_text() for seite in r.pages]


def ablegen(quelle, ordner):
    """PDF in den iCloud-Ordner; eine geänderte alte Fassung gleichen Namens kommt vorher nach _alt."""
    ordner.mkdir(parents=True, exist_ok=True)
    ziel = ordner / quelle.name
    if ziel.exists():
        if filecmp.cmp(quelle, ziel, shallow=False) or (quelle.suffix == ".pdf" and pdf_text(quelle) == pdf_text(ziel)):
            if not filecmp.cmp(quelle, ziel, shallow=False):
                shutil.copy2(quelle, ziel)        # gleicher Inhalt, nur neu gebaut: still ersetzen, nichts nach _alt
            return "unverändert"
        alt = ordner / "_alt" / quelle.name
        heute = datetime.date.fromtimestamp(ziel.stat().st_mtime) == datetime.date.today()
        if alt.exists() or heute:  # erste Fassung in _alt bleibt; heute selbst gebaute Zwischenstände werden nicht archiviert          # die erste (ursprüngliche) Fassung in _alt bleibt, Zwischenstände werden nicht archiviert
            shutil.copy2(quelle, ziel)
            return "ersetzt"
        alt.parent.mkdir(exist_ok=True)
        shutil.move(ziel, alt)
        shutil.copy2(quelle, ziel)
        return "ersetzt (alt in _alt)"
    shutil.copy2(quelle, ziel)
    return "neu"


def einbetten(html, basis):
    """Bilder (src="…png/jpg/svg") relativ zu basis als data-URI."""
    def ersetze(m):
        pfad = (basis / unquote(m.group(1))).resolve()
        if not pfad.exists():
            return m.group(0)
        art = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".webp": "image/webp"}[pfad.suffix.lower()]
        return f'src="data:{art};base64,{base64.b64encode(pfad.read_bytes()).decode()}"'
    return re.sub(r'src="(?!data:|https?:)([^"]+\.(?:png|jpe?g|svg|webp))"', ersetze, html, flags=re.I)


def gesamt_html(uebersicht, ziel):
    """Übersicht als eine Datei: jede Stunde als srcdoc eingebettet, Bilder als data-URI."""
    s = uebersicht.read_text(encoding="utf-8")
    m = re.search(r"const D=(\[.*?\]);\n", s, re.S)
    daten = json.loads(m.group(1))
    seiten = {}
    for e in daten:
        if e.get("datei"):
            datei = HIER / e["datei"]
            seiten[e["w"]] = einbetten(datei.read_text(encoding="utf-8"), datei.parent)
    js = "const SEITEN=" + json.dumps(seiten, ensure_ascii=False).replace("</", "<\\/") + ";\n"
    s = s.replace(m.group(0), m.group(0) + js, 1)
    alt = "r.src=encodeURI(s.datei); neu.href=encodeURI(s.datei);"
    assert alt in s
    s = s.replace(alt, "r.srcdoc=SEITEN[s.w]; neu.href=URL.createObjectURL(new Blob([SEITEN[s.w]],{type:'text/html'}));")
    ziel.write_text(s, encoding="utf-8")
    return len(seiten), len(s) // 1024


def main():
    # 1. PDFs bauen
    w4_pdf = RZ / f"{w4.NAME}.pdf"
    print("Woche 4:", a4_zu_pdf(w4.FOLIEN, RZ, w4_pdf, getattr(w4, "QUER", ())), "Seiten")
    w4d_pdfs = []
    for st in w4d.STUNDEN:
        ziel = RZ / f"{st['name']}.pdf"
        print(f"Woche 4, Stunde {st['nr']}:", a4_zu_pdf(st["folien"], RZ, ziel, st["quer"]), "Seiten")
        w4d_pdfs.append(ziel)
    w7_pdf = RZ / "Mathe 7c – Woche 5 – 1 Rezept für gemischte Aufgaben.pdf"   # Bauskript heißt noch baue_woche7.py
    print("Woche 5 (gemischte Aufgaben):", folien_zu_pdf(w7.FOLIEN, RZ, w7_pdf), "Seiten")
    w2 = woche2_pdf()
    print("Woche 2:", len(PdfReader(str(w2)).pages), "Seiten")
    ka_pdfs = []
    for mod, name in ((uka1, "Mathe 7c – Übungsklassenarbeit Nr. 1 Rationale Zahlen"), (ka1, "Mathe 7c – Klassenarbeit Nr. 1 Rationale Zahlen – Entwurf")):
        for l, zusatz in ((False, ""), (True, " – Lösung")):
            ziel = RZ / f"{name}{zusatz}.pdf"
            print(f"{ziel.name}:", html_zu_pdf(*mod.druckfassung(l), ziel), "Seiten")
            ka_pdfs.append(ziel)
    ka10_pdfs = []
    for l, zusatz in ((False, ""), (True, " – Lösung")):
        ziel = PZ / f"Mathe 10b – Übungsklassenarbeit Nr. 1 Prozent und Wahrscheinlichkeit{zusatz}.pdf"
        print(f"{ziel.name}:", html_zu_pdf(*uka10.druckfassung(l), ziel), "Seiten")
        ka10_pdfs.append(ziel)
    zw = PZ / f"{zw10.NAME}.pdf"
    print("10b Zuwachssparen:", a4_zu_pdf(zw10.FOLIEN, PZ, zw, zw10.QUER, zw10.EXTRA), "Seiten")
    zw_ab, zw_abl = PZ / f"{zw10.AB_NAME}.pdf", PZ / f"{zw10.AB_NAME} – Lösung.pdf"
    print("10b Übungsblatt:", a4_zu_pdf([(t, f(False)) for t, f in zw10.AB], PZ, zw_ab, (), zw10.EXTRA),
          "Seiten; Lösung:", a4_zu_pdf([(t + " – Lösung", f(True)) for t, f in zw10.AB], PZ, zw_abl, (), zw10.EXTRA), "Seiten")
    z1, z2 = PZ / "Mathe 10b – Woche 4 – 1 Zinsen kurz, Zinseszins.pdf", PZ / "Mathe 10b – Woche 4 – 2 Zinseszins, Zinssatz gesucht.pdf"
    print("10b Zinsen:", folien_zu_pdf(z10.FOLIEN_MI, PZ, z1), "Seiten; Zinseszins:", folien_zu_pdf(z10.FOLIEN_FR, PZ, z2), "Seiten")

    # 2. Ablegen
    rz_ordner = ICLOUD / "Mathematik 7c" / "04 Rationale Zahlen"
    pdfs_7 = [RZ / f"Mathe 7c – Woche 3 – {st['nr']} {st['titel']}.pdf" for st in w3.STUNDEN] + [w2, w4_pdf] + w4d_pdfs + [w7_pdf,
              RZ / "Rationale Zahlen 3 – Arbeitsblatt Klammern.pdf", RZ / "Rationale Zahlen 3 – Arbeitsblatt Klammern – Lösungen.pdf"] + ka_pdfs
    pz_ordner = ICLOUD / "Mathematik 10b" / "04 Prozentrechnung"   # bestehende Struktur in der iCloud
    pdfs_10 = sorted(PZ.glob("Prozent Wdh 10b – *.pdf")) + [z1, z2, zw, zw_ab, zw_abl] + ka10_pdfs
    for p in pdfs_7:
        print(f"  7c  {ablegen(p, rz_ordner):24s} {p.name}")
    for p in pdfs_10:
        print(f"  10b {ablegen(p, pz_ordner):24s} {p.name}")

    # 3. Gesamt-HTML in die Hauptordner
    for ueb, ordner in ((HIER / "Mathematik Klasse 7 – Übersicht.html", ICLOUD / "Mathematik 7c"),
                        (HIER / "Mathematik Klasse 10b – Übersicht.html", ICLOUD / "Mathematik 10b")):
        n, kb = gesamt_html(ueb, ordner / ueb.name)
        print(f"  Gesamt-HTML {ueb.name}: {n} Stunden eingebettet, {kb} KB")


if __name__ == "__main__":
    main()
