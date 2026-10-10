#!/usr/bin/env python3
"""Stoffverteilungsplan Physik 10 (Schuljahr 2026/27), grober Plan ohne Wochen und Daten, optisch wie der alte Plan von 2020
(gelbe Kopfzeile, farbige Blockleiste, schwarze Ferienbalken, Bilder). Baut HTML und PDF (A4, 2 Seiten) und legt das PDF in die iCloud.
Aufruf: python3 baue_stoffverteilung10.py"""
import base64, shutil, subprocess
from pathlib import Path

HIER = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik/Physik Klasse 10/Organisation"
NAME = "Stoffverteilungsplan Klasse 10 2026-27"

GRUEN, BRAUN, BLAU, ROT = "#3fae49", "#a0652b", "#00aeef", "#d2232a"

# Seite 1 und 2: Folge aus Blöcken, Ferienbalken (schwarz) und Hinweisbalken (grau, kein Unterricht für die 10er).
# ("block", Name, Farbe, Schriftgröße, [Zeile oder (Zeile, Termin)])
# Grundlage der Wochen: Rahmendaten Schuljahr 2026-27 (Ferien), Kalender (Berlinfahrt, Eurocom), Infoblatt Elternabend 10b (Prüfungen).
SEITE1 = [
    ("block", "Atomphysik", GRUEN, 13, ["Atombau und Isotope", "Zählrohr und Nullrate", "Alpha-, Beta- und Gamma-Strahlung",
                                        "Zerfallsgleichungen, Zerfallsreihen und Durchdringung"]),
    ("info", "Berlinfahrt der 10er, kein Unterricht"),
    ("ferien", "Herbstferien"),
    ("block", "Kernphysik", GRUEN, 13, ["Zufall beim Zerfall", "Halbwertszeit", "Aktivität und Übungen zur Halbwertszeit",
                                        "Klassenarbeit 1 und Besprechung", "Ionisierende Strahlung und Wirkung auf den Körper", "Puffer"]),
    ("ferien", "Weihnachtsferien"),
    ("block", "Kernenergie", GRUEN, 10.5, ["Schutz vor Strahlung und Anwendungen", "Kernspaltung und Kettenreaktion",
                                           "Kernreaktor, Kernkraftwerk und Kernfusion"]),
    ("ferien", "Faschingsferien"),
    ("block", "Kernenergie", GRUEN, 10.5, ["Übungen zur Kernenergie", ("Radioaktiver Abfall und Endlagersuche", "Eurocom Mo bis Mi"),
                                           "Nutzen und Risiko abwägen", "Rückblick und Altersbestimmung (C-14)"]),
    ("info", "Praktische Prüfungen AES/T, kein Unterricht"),
    ("block", "Wärme", BRAUN, 8, ["Teilchenmodell und Aggregatzustände"]),
    ("ferien", "Osterferien"),
]
SEITE2 = [
    ("ferien", "Osterferien"),
    ("block", "Wärmelehre", BRAUN, 11.5, ["Temperatur, Temperaturskalen und absoluter Nullpunkt", "Ausdehnung von Festkörpern, Flüssigkeiten und Gasen",
                                          ("Spezifische Wärmekapazität und Grundgleichung der Wärmelehre", "vorher Prüfungen, kein Unterricht")]),
    ("ferien", "Pfingstferien"),
    ("block", "Wärme", BRAUN, 12, ["Wärmeleitung, Wärmeströmung und Wärmestrahlung", "Wärmedämmung und Klassenarbeit 2"]),
    ("block", "Klima", BLAU, 13, ["Treibhauseffekt und Klimaschutz", "Erneuerbare Energien und Wirkungsgrad"]),
    ("info", "Mündliche Prüfungen und Schuljahresende, kein Unterricht"),
    ("ferien", "Sommerferien"),
]
FUSS = "Wochen nur ungefähr. Ferien und Termine nach Schulkalender, Kalender GDRS und Infoblatt Elternabend 10b. Für Physik bleiben nach den Osterferien etwa sechs bis sieben Unterrichtswochen."


def bild(name):
    p = HIER / "assets" / name
    typ = "png" if name.endswith("png") else "jpeg"
    return f"data:image/{typ};base64,{base64.b64encode(p.read_bytes()).decode()}"


def tabelle(teile):
    z = ['<table><tr class="kopf"><th class="band"></th><th class="inhalt">Inhalt</th><th class="termine">Termine</th></tr>']
    for t in teile:
        if t[0] in ("ferien", "info"):
            z.append(f'<tr class="{t[0]}"><td colspan="3">{t[1]}</td></tr>')
            continue
        _, name, farbe, gr, zeilen = t
        for i, text in enumerate(zeilen):
            text, termin = text if isinstance(text, tuple) else (text, "")
            band = f'<td class="band" rowspan="{len(zeilen)}" style="background:{farbe};font-size:{gr}pt{';color:#fff' if gr < 9 else ''}"><span>{name}</span></td>' if i == 0 else ""
            z.append(f'<tr class="z">{band}<td class="inhalt">{text}</td><td class="termine">{termin}</td></tr>')
    z.append("</table>")
    return "".join(z)


CSS = """
@page { size: A4; margin: 0 }
* { box-sizing: border-box }
html, body { margin: 0; padding: 0; font-family: "Minion Pro", "Palatino", "Palatino Linotype", Georgia, serif; color: #111 }
.seite { position: relative; width: 210mm; height: 297mm; padding: 17mm 18.4mm 0; page-break-after: always; overflow: hidden }
.seite:last-child { page-break-after: auto }
h1 { margin: 0 0 4mm; text-align: center; font-weight: 400; font-size: 22pt }
table { width: 100%; border-collapse: collapse; table-layout: fixed }
th.band, td.band { width: 14.5mm }
th.inhalt { width: auto } th.termine, td.termine { width: 26mm }
tr.kopf th { background: #fff200; border: 0.7pt solid #111; font-weight: 400; font-size: 14pt; height: 7.6mm }
tr.z td { border: 0.7pt solid #111; height: 7.7mm; font-size: 8.6pt; padding: 0 2mm; line-height: 1.12; vertical-align: middle }
td.band { border: 0.7pt solid #111; padding: 0; text-align: center; vertical-align: middle; color: #1b1b1b; position: relative }
td.band span { display: block; transform: rotate(-90deg); white-space: nowrap; width: 0; margin: 0 auto; overflow: visible; text-align: center }
td.band span { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%) rotate(-90deg); width: auto }
td.termine { font-size: 7pt; line-height: 1.1 }
tr.info td { background: #6d6e71; color: #fff; text-align: center; font-size: 9.5pt; height: 6.4mm; border: 0.7pt solid #6d6e71 }
.fuss { position: absolute; left: 18.4mm; right: 18.4mm; bottom: 10mm; font-size: 8pt; color: #555 }
tr.ferien td { background: #231f20; color: #fff; text-align: center; font-size: 13pt; height: 7.6mm; border: 0.7pt solid #231f20 }
.bild { position: absolute }
"""


def seite(teile, bilder, fuss=""):
    return f'<div class="seite"><h1>Stoffverteilungsplan Physik 10 GDRS</h1>{tabelle(teile)}{bilder}<div class="fuss">{fuss}</div></div>'


def bauen():
    b1 = (f'<img class="bild" src="{bild("warnzeichen.png")}" style="left:152mm;top:40mm;width:31mm">'
          f'<img class="bild" src="{bild("gasmaske.png")}" style="left:157mm;top:99mm;width:23mm">')
    b2 = (f'<img class="bild" src="{bild("kupferspirale.jpg")}" style="left:20mm;top:214mm;width:25mm">'
          f'<img class="bild" src="{bild("atombombe.jpg")}" style="left:52mm;top:224mm;width:46mm">'
          f'<img class="bild" src="{bild("einstein.jpg")}" style="left:96mm;top:166mm;width:84mm">'
          f'<img class="bild" src="{bild("endlager.jpg")}" style="left:20mm;top:168mm;width:72mm">')
    html = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{NAME}</title><style>{CSS}</style></head><body>'
            f'{seite(SEITE1, b1)}{seite(SEITE2, b2, FUSS)}</body></html>')
    h = HIER / f"{NAME}.html"
    h.write_text(html, encoding="utf-8")
    pdf = HIER / f"{NAME}.pdf"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "--virtual-time-budget=4000", h.as_uri()],
                   check=True, capture_output=True)
    return h, pdf


if __name__ == "__main__":
    h, pdf = bauen()
    print("geschrieben:", h.name, "|", pdf.name)
    if "--icloud" in __import__("sys").argv:
        shutil.copy(pdf, ICLOUD / pdf.name)
        print("iCloud:", ICLOUD / pdf.name)
