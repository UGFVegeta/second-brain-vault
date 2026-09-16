#!/usr/bin/env python3
"""
Erzeugt die Wandkarten fuer den Stundenplan der Klasse 7C als HTML.
Aus der HTML wird mit Chrome headless ein PDF gedruckt (A4 quer).

    python3 wandkarten.py            -> Wandkarten 7C.html
    python3 wandkarten.py --symbole  -> zusaetzlich eine Symbol-Kontrollseite

Masse (Endmass nach dem Schneiden):
    Fachkarte    240 x 80 mm
    Tageskarte   240 x 40 mm
    Stundenkarte  70 x 80 mm
    Pausenkarte   70 x 31 mm
Alle Farbflaechen haben ringsum 3 mm Anschnitt, die Eckwinkel zeigen die Schnittlinie.

Farben nach der Heftfarben-Uebersicht der GDRS. Sport, Kunst und die
Klassenlehrerstunde stehen dort nicht und sind ergaenzt.
"""

import argparse
import pathlib

# --------------------------------------------------------------------------
# Symbole. viewBox 0 0 100 100, Fuellung currentColor,
# Aussparungen in der Kartenfarbe var(--bg).
# --------------------------------------------------------------------------
BG = 'style="fill:var(--bg)"'
FG = 'style="fill:currentColor"'
SFG = 'style="stroke:currentColor"'
SBG = 'style="stroke:var(--bg)"'

SYMBOLE = {
    "buch": f'''
      <path d="M47 24 C37 14,19 12,6 15 L6 76 C19 73,37 75,47 84 Z" {FG}/>
      <path d="M53 24 C63 14,81 12,94 15 L94 76 C81 73,63 75,53 84 Z" {FG}/>
      <path d="M14 30 L39 34 M14 42 L39 46 M14 54 L34 57" {SBG} stroke-width="4"
            stroke-linecap="round" fill="none" opacity=".6"/>
      <path d="M86 30 L61 34 M86 42 L61 46 M86 54 L66 57" {SBG} stroke-width="4"
            stroke-linecap="round" fill="none" opacity=".6"/>''',

    "geodreieck": f'''
      <path d="M6 74 L94 74 L50 26 Z" {FG}/>
      <path d="M27 74 A23 23 0 0 1 73 74" {SBG} stroke-width="4" fill="none"
            opacity=".8"/>
      <path d="M50 74 L50 51" {SBG} stroke-width="4" opacity=".8"/>
      <path d="M18 74 L18 67 M26 74 L26 63 M34 74 L34 67 M42 74 L42 63
               M58 74 L58 63 M66 74 L66 67 M74 74 L74 63 M82 74 L82 67"
            {SBG} stroke-width="3.5" stroke-linecap="round" opacity=".8"/>''',

    "sprechblase": f'''
      <path d="M12 12 L88 12 C93 12,96 15,96 20 L96 62 C96 67,93 70,88 70
               L44 70 L22 90 L26 70 L12 70 C7 70,4 67,4 62 L4 20
               C4 15,7 12,12 12 Z" {FG}/>
      <text x="50" y="55" text-anchor="middle" font-family="Helvetica,Arial"
            font-size="40" font-weight="700" {BG}>Hi</text>''',

    "gluehlampe": f'''
      <path d="M50 6 C32 6,18 20,18 38 C18 50,26 57,31 63 C34 67,35 71,35 75
               L65 75 C65 71,66 67,69 63 C74 57,82 50,82 38 C82 20,68 6,50 6 Z" {FG}/>
      <rect x="36" y="80" width="28" height="7" rx="3.5" {FG}/>
      <rect x="40" y="90" width="20" height="6" rx="3" {FG}/>
      <path d="M38 40 L45 33 L45 47 L52 33 L52 47 L59 40" {SBG} stroke-width="4"
            fill="none" stroke-linecap="round" stroke-linejoin="round"
            opacity=".75"/>''',

    "blatt": f'''
      <path d="M18 86 C18 46,46 16,88 12 C92 54,62 86,18 86 Z" {FG}/>
      <path d="M18 86 C36 66,58 44,86 22" {SBG} stroke-width="5" fill="none"
            stroke-linecap="round" opacity=".75"/>
      <path d="M34 70 L27 55 M34 70 L49 77 M48 56 L41 40 M48 56 L63 63
               M62 42 L56 27 M62 42 L76 49" {SBG} stroke-width="4"
            fill="none" stroke-linecap="round" opacity=".75"/>''',

    "globus": f'''
      <circle cx="50" cy="50" r="41" {FG}/>
      <g {SBG} stroke-width="4.5" fill="none" opacity=".75">
        <ellipse cx="50" cy="50" rx="18" ry="41"/>
        <path d="M9 50 L91 50"/>
        <path d="M17 28 C30 35,70 35,83 28"/>
        <path d="M17 72 C30 65,70 65,83 72"/>
      </g>''',

    "saeulen": f'''
      <path d="M50 8 L94 32 L6 32 Z" {FG}/>
      <rect x="6" y="36" width="88" height="7" rx="3" {FG}/>
      <rect x="14" y="47" width="12" height="33" rx="2" {FG}/>
      <rect x="35" y="47" width="12" height="33" rx="2" {FG}/>
      <rect x="53" y="47" width="12" height="33" rx="2" {FG}/>
      <rect x="74" y="47" width="12" height="33" rx="2" {FG}/>
      <rect x="4" y="84" width="92" height="9" rx="3" {FG}/>''',

    "diagramm": f'''
      <rect x="10" y="60" width="20" height="30" rx="3" {FG}/>
      <rect x="40" y="44" width="20" height="46" rx="3" {FG}/>
      <rect x="70" y="24" width="20" height="66" rx="3" {FG}/>''',

    "noten": f'''
      <path d="M36 74 L36 22 L84 12 L84 64" {SFG} stroke-width="7" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M36 20 L84 10 L84 26 L36 36 Z" {FG}/>
      <ellipse cx="25" cy="76" rx="14" ry="11" transform="rotate(-17 25 76)" {FG}/>
      <ellipse cx="73" cy="66" rx="14" ry="11" transform="rotate(-17 73 66)" {FG}/>''',

    "palette": f'''
      <path d="M50 10 C76 10,94 27,94 47 C94 60,83 65,74 65 C68 65,64 69,64 74
               C64 82,57 90,48 90 C24 90,6 71,6 49 C6 27,25 10,50 10 Z" {FG}/>
      <ellipse cx="66" cy="42" rx="9" ry="7" {BG}/>
      <circle cx="30" cy="34" r="8" {BG}/>
      <circle cx="49" cy="26" r="8" {BG}/>
      <circle cx="24" cy="57" r="8" {BG}/>
      <circle cx="40" cy="70" r="8" {BG}/>''',

    "topf": f'''
      <rect x="16" y="30" width="68" height="9" rx="4.5" {FG}/>
      <circle cx="50" cy="21" r="6.5" {FG}/>
      <path d="M20 44 L80 44 L74 84 C73.4 88,70 90.5,66 90.5 L34 90.5
               C30 90.5,26.6 88,26 84 Z" {FG}/>
      <rect x="4" y="50" width="14" height="8.5" rx="4" {FG}/>
      <rect x="82" y="50" width="14" height="8.5" rx="4" {FG}/>''',

    "zahnrad": f'''
      <g {FG}>
        <circle cx="50" cy="50" r="31"/>
        <rect x="43" y="5" width="14" height="17" rx="3"/>
        <rect x="43" y="5" width="14" height="17" rx="3" transform="rotate(45 50 50)"/>
        <rect x="43" y="5" width="14" height="17" rx="3" transform="rotate(90 50 50)"/>
        <rect x="43" y="5" width="14" height="17" rx="3" transform="rotate(135 50 50)"/>
        <rect x="43" y="5" width="14" height="17" rx="3" transform="rotate(180 50 50)"/>
        <rect x="43" y="5" width="14" height="17" rx="3" transform="rotate(225 50 50)"/>
        <rect x="43" y="5" width="14" height="17" rx="3" transform="rotate(270 50 50)"/>
        <rect x="43" y="5" width="14" height="17" rx="3" transform="rotate(315 50 50)"/>
      </g>
      <circle cx="50" cy="50" r="12" {BG}/>''',

    "kreuz": f'''
      <rect x="41" y="8" width="18" height="84" rx="4" {FG}/>
      <rect x="16" y="32" width="68" height="18" rx="4" {FG}/>''',

    "kompass": f'''
      <circle cx="50" cy="50" r="40" {FG}/>
      <circle cx="50" cy="50" r="30" {BG}/>
      <path d="M68 32 L57 57 L32 68 L43 43 Z" {FG}/>
      <circle cx="50" cy="50" r="5" {BG}/>''',

    "ball": f'''
      <circle cx="50" cy="50" r="40" {FG}/>
      <g {SBG} stroke-width="5" fill="none" opacity=".8">
        <path d="M50 10 L50 90"/>
        <path d="M10 50 L90 50"/>
        <path d="M22 22 C36 36,36 64,22 78"/>
        <path d="M78 22 C64 36,64 64,78 78"/>
      </g>''',

    "wellen": f'''
      <g {SFG} stroke-width="9" fill="none" stroke-linecap="round">
        <path d="M6 30 C18 18,30 42,42 30 C54 18,66 42,78 30 C86 22,90 26,94 29"/>
        <path d="M6 55 C18 43,30 67,42 55 C54 43,66 67,78 55 C86 47,90 51,94 54"/>
        <path d="M6 80 C18 68,30 92,42 80 C54 68,66 92,78 80 C86 72,90 76,94 79"/>
      </g>''',

    "monitor": f'''
      <rect x="6" y="14" width="88" height="60" rx="7" {FG}/>
      <rect x="14" y="22" width="72" height="44" rx="2" {BG}/>
      <path d="M38 80 L62 80 L65 92 L35 92 Z" {FG}/>
      <rect x="28" y="92" width="44" height="7" rx="3.5" {FG}/>
      <path d="M38 34 L28 44 L38 54 M62 34 L72 44 L62 54 M54 32 L46 56" {SFG}
            stroke-width="5" fill="none" stroke-linecap="round"
            stroke-linejoin="round"/>''',

    "personen": f'''
      <circle cx="50" cy="32" r="15" {FG}/>
      <path d="M24 88 C24 70,35 61,50 61 C65 61,76 70,76 88 Z" {FG}/>
      <circle cx="17" cy="42" r="11" {FG}/>
      <path d="M2 88 C2 74,8 66,17 66 C21 66,24 67,27 69
               C22 74,19 81,19 88 Z" {FG}/>
      <circle cx="83" cy="42" r="11" {FG}/>
      <path d="M98 88 C98 74,92 66,83 66 C79 66,76 67,73 69
               C78 74,81 81,81 88 Z" {FG}/>''',
}

# --------------------------------------------------------------------------
# Faecher der 7C. anzahl = Wochenstunden laut Stundenplan.
# gross: Schriftgroesse des Fachnamens in mm.
# --------------------------------------------------------------------------
FACHKARTEN = [
    dict(name="Deutsch", bg="#C2231C", sym="buch", gross=35, anzahl=4),
    dict(name="Mathematik", bg="#1B63A8", sym="geodreieck", gross=26, anzahl=4),
    dict(name="Englisch", bg="#F0C000", sym="sprechblase", gross=35, anzahl=3),
    dict(name="Physik", bg="#16181D", sym="gluehlampe", gross=35, anzahl=2),
    dict(name="Biologie", bg="#1F6B45", sym="blatt", gross=35, anzahl=1),
    dict(name="Geografie", bg="#7A5230", sym="globus", gross=32, anzahl=1),
    dict(name="Gemein-|schaftskunde", bg="#0E9C94", sym="saeulen", gross=23,
         anzahl=1),
    dict(name="WBS", bg="#0E9C94", sym="diagramm", gross=35, anzahl=2),
    dict(name="Musik", bg="#7CB342", sym="noten", gross=35, anzahl=1),
    dict(name="Informatik", bg="#6B7280", sym="monitor", gross=30, anzahl=2),
    dict(name="IF7 ME", bg="#6B7280", sym="monitor", gross=35, anzahl=2),
    dict(name="Kunst", bg="#A8329E", sym="palette", gross=35, anzahl=2),
    dict(name="Sport", bg="#E2691B", sym="ball", gross=35, anzahl=1),
    dict(name="Klassen-|lehrerstunde", bg="#2E3A4E", sym="personen", gross=24,
         anzahl=1),
]

GETEILTE_KARTEN = [
    dict(anzahl=3,
         links=dict(name="AES", bg="#E8629F", sym="topf", gross=25),
         rechts=dict(name="Technik", bg="#B02E72", sym="zahnrad", gross=25)),
    dict(anzahl=2,
         links=dict(name="Religion", bg="#7B4FA8", sym="kreuz", gross=26,
                    breite=55),
         rechts=dict(name="Ethik", bg="#A98BD1", sym="kompass", gross=26,
                     breite=45)),
    dict(anzahl=2,
         links=dict(name="Sport", bg="#E2691B", sym="ball", gross=19,
                    breite=42),
         rechts=dict(name="Schwimmen", bg="#1B9CD8", sym="wellen", gross=19,
                     breite=58)),
]

BLANKO = 2

TAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

STUNDEN = [
    ("1", "7:40", "8:25"), ("2", "8:25", "9:10"),
    ("3", "9:30", "10:15"), ("4", "10:15", "11:00"),
    ("5", "11:20", "12:05"), ("6", "12:05", "12:50"),
    ("7", "12:55", "13:40"), ("8", "13:45", "14:30"),
    ("9", "14:30", "15:15"),
]

PAUSEN = [
    ("Große Pause", "9:10 – 9:30"),
    ("Große Pause", "11:00 – 11:20"),
    ("Pause", "12:50 – 12:55"),
    ("Pause", "13:40 – 13:45"),
]

MARKEN = ('<i class="m tl"></i><i class="m tr"></i>'
          '<i class="m bl"></i><i class="m br"></i>')


DUNKEL = "#1C2230"


def _luminanz(hexfarbe):
    r, g, b = (int(hexfarbe[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def textfarbe(bg):
    """Weiss, solange der Kontrast fuer grosse Schrift reicht (3:1),
    sonst Dunkelblau. Betrifft die hellen Flaechen wie Gelb und Hellgruen."""
    return "#FFFFFF" if 1.05 / (_luminanz(bg) + 0.05) >= 3.0 else DUNKEL


def zusatzzeile(k):
    """Lehrerkuerzel und Raum sind bewusst leer: so bleiben die Karten
    ueber Schuljahre hinweg brauchbar. Wer sie doch will, traegt
    zusatz="..." beim Fach ein."""
    text = k.get("zusatz", "")
    return f'\n        <div class="zusatz">{text}</div>' if text else ""


def zeilen(name):
    """| trennt manuell umbrochene Zeilen."""
    return "<br>".join(name.split("|"))


def symbol(key):
    return f'<div class="sym"><svg viewBox="0 0 100 100" aria-hidden="true">{SYMBOLE[key]}</svg></div>'


def fachkarte(k):
    fg = k.get("fg") or textfarbe(k["bg"])
    return f'''
  <div class="karte fachkarte" style="--bg:{k['bg']};--fg:{fg}">
    {MARKEN}
    <div class="inhalt">
      {symbol(k['sym'])}
      <div class="txt">
        <div class="name" style="font-size:{k['gross']}mm">{zeilen(k['name'])}</div>{zusatzzeile(k)}
      </div>
    </div>
  </div>'''


def haelfte(h):
    fg = h.get("fg") or textfarbe(h["bg"])
    return f'''
    <div class="haelfte" style="--bg:{h['bg']};--fg:{fg};width:{h.get('breite', 50)}%">
      {symbol(h['sym'])}
      <div class="txt">
        <div class="name" style="font-size:{h.get('gross', 20)}mm">{zeilen(h['name'])}</div>{zusatzzeile(h)}
      </div>
    </div>'''


def geteilte_karte(k):
    return f'''
  <div class="karte fachkarte geteilt">
    {MARKEN}{haelfte(k['links'])}{haelfte(k['rechts'])}
  </div>'''


def blankokarte():
    return f'''
  <div class="karte fachkarte hell" style="--bg:#EFEADD;--fg:#1C2230">
    {MARKEN}
  </div>'''


def tageskarte(tag):
    return f'''
  <div class="karte tageskarte" style="--bg:#1C2230;--fg:#FFFFFF">
    {MARKEN}<div class="tag">{tag}</div>
  </div>'''


def stundenkarte(nr, von, bis):
    return f'''
    <div class="karte zeitkarte hell" style="--bg:#EAE4D6;--fg:#1C2230">
      {MARKEN}<div class="nr">{nr}</div><div class="von">{von}<br>{bis}</div>
    </div>'''


def pausenkarte(text, zeit):
    return f'''
    <div class="karte pausenkarte hell" style="--bg:#D8D2C1;--fg:#43402F">
      {MARKEN}<div class="pl">{text}</div><div class="pz">{zeit}</div>
    </div>'''


def blatt(inhalt, klasse=""):
    return f'<div class="blatt {klasse}">{inhalt}\n</div>\n'


def bauen():
    # ---- Fachkarten, zwei pro Blatt -------------------------------------
    karten = []
    for k in FACHKARTEN:
        karten += [fachkarte(k)] * k["anzahl"]
    for k in GETEILTE_KARTEN:
        karten += [geteilte_karte(k)] * k["anzahl"]
    karten += [blankokarte()] * BLANKO

    blaetter = []
    for i in range(0, len(karten), 2):
        paar = karten[i:i + 2]
        blaetter.append(blatt('<div style="height:8mm"></div>'.join(paar)))

    # ---- Tageskarten, drei pro Blatt ------------------------------------
    tagkarten = [tageskarte(t) for t in TAGE]
    for i in range(0, len(tagkarten), 3):
        gruppe = tagkarten[i:i + 3]
        blaetter.append(blatt('<div style="height:10mm"></div>'.join(gruppe),
                              "tage"))

    # ---- Stundenkarten, sechs pro Blatt; die Pausen auf das letzte Blatt -
    stk = [stundenkarte(*s) for s in STUNDEN]
    pk = [pausenkarte(*p) for p in PAUSEN]
    gruppen = [stk[i:i + 6] for i in range(0, len(stk), 6)]
    for nr, gruppe in enumerate(gruppen):
        reihen = [f'<div class="reihe">{"".join(gruppe[j:j + 3])}</div>'
                  for j in range(0, len(gruppe), 3)]
        if nr == len(gruppen) - 1:
            reihen += [f'<div class="reihe">{"".join(pk[j:j + 3])}</div>'
                       for j in range(0, len(pk), 3)]
        blaetter.append(blatt("".join(reihen), "zeiten"))

    return "".join(blaetter), len(karten)


def symbolseite():
    kacheln = []
    for key in SYMBOLE:
        kacheln.append(f'''
      <div class="probe">
        <div class="karte" style="--bg:#2E3A4E;--fg:#fff;width:52mm;height:52mm;
             display:flex;align-items:center;justify-content:center">
          <div class="sym" style="width:38mm;height:38mm">
            <svg viewBox="0 0 100 100">{SYMBOLE[key]}</svg>
          </div>
        </div>
        <div class="probename">{key}</div>
      </div>''')
    return ('<div class="blatt" style="display:block;padding:10mm">'
            '<div class="probenreihe">' + "".join(kacheln) + '</div></div>')


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#e9e5dc;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;
     color:#1c2230}
.blatt{width:297mm;height:210mm;background:#fff;margin:6mm auto;
       padding:15mm 25.5mm;display:flex;flex-direction:column;
       justify-content:center;box-shadow:0 3mm 14mm rgba(0,0,0,.15)}
.blatt.tage{padding:20mm 25.5mm}
.blatt.zeiten{padding:12mm 26.5mm}

.karte{position:relative;overflow:hidden;display:flex;align-items:center;
       background:var(--bg);color:var(--fg);--mark:rgba(255,255,255,.6)}
.karte.hell,.karte[style*="--fg:#1C2230"]{--mark:rgba(0,0,0,.35)}

.fachkarte{width:246mm;height:86mm}
.tageskarte{width:246mm;height:46mm}
.zeitkarte{width:76mm;height:86mm}
.pausenkarte{width:76mm;height:37mm}

.m{position:absolute;width:11mm;height:11mm;border:0 solid var(--mark);z-index:5}
.tl{top:3mm;left:3mm;border-top-width:.3mm;border-left-width:.3mm}
.tr{top:3mm;right:3mm;border-top-width:.3mm;border-right-width:.3mm}
.bl{bottom:3mm;left:3mm;border-bottom-width:.3mm;border-left-width:.3mm}
.br{bottom:3mm;right:3mm;border-bottom-width:.3mm;border-right-width:.3mm}

.inhalt{display:flex;align-items:center;gap:13mm;padding:0 16mm;width:100%}
.sym{width:50mm;height:50mm;flex:none}
.sym svg{width:100%;height:100%;display:block}
.txt{min-width:0}
.name{font-weight:700;line-height:.95;letter-spacing:-.015em}
.zusatz{font-size:8mm;font-weight:500;line-height:1;margin-top:4mm;opacity:.82;
        letter-spacing:.02em;white-space:nowrap}

.geteilt{padding:0}
.haelfte{height:100%;display:flex;flex-direction:column;
         justify-content:center;align-items:flex-start;gap:5mm;padding:0 12mm;
         background:var(--bg);color:var(--fg)}
.haelfte .sym{width:27mm;height:27mm}
.haelfte .zusatz{font-size:6.5mm;margin-top:2.5mm}

.tageskarte .tag{width:100%;text-align:center;font-size:21mm;font-weight:700;
                 letter-spacing:.14em;text-transform:uppercase}

.zeitkarte{flex-direction:column;justify-content:center;text-align:center}
.zeitkarte .nr{font-size:34mm;font-weight:700;line-height:.9}
.zeitkarte .von{font-size:8mm;font-weight:600;margin-top:5mm;line-height:1.25}
.pausenkarte{flex-direction:column;justify-content:center;text-align:center}
.pausenkarte .pl{font-size:6mm;font-weight:700;letter-spacing:.16em;
                 text-transform:uppercase}
.pausenkarte .pz{font-size:7.5mm;font-weight:600;margin-top:2.5mm}
.pausenkarte .m{width:6mm;height:6mm}

.reihe{display:flex;gap:8mm;align-items:flex-start}
.reihe+.reihe{margin-top:10mm}

.probenreihe{display:flex;flex-wrap:wrap;gap:6mm}
.probe{text-align:center}
.probename{font-size:4mm;margin-top:2mm;color:#555}

@media print{
  @page{size:A4 landscape;margin:0}
  body{background:#fff}
  .blatt{margin:0;box-shadow:none;page-break-after:always}
  .blatt:last-child{page-break-after:auto}
}
"""


def schreiben(pfad, inhalt, titel):
    html = (f'<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
            f'<title>{titel}</title>\n<style>{CSS}</style>\n</head>\n<body>\n'
            f'{inhalt}\n</body>\n</html>\n')
    pathlib.Path(pfad).write_text(html, encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--symbole", action="store_true",
                   help="zusaetzlich eine Symbol-Kontrollseite schreiben")
    p.add_argument("--ziel", default="Wandkarten 7C.html")
    args = p.parse_args()

    inhalt, anzahl = bauen()
    schreiben(args.ziel, inhalt, "Wandkarten 7C")
    seiten = inhalt.count('class="blatt')
    print(f"{anzahl} Fachkarten, {seiten} Seiten -> {args.ziel}")

    if args.symbole:
        schreiben("/tmp/symbole.html", symbolseite(), "Symbole")
        print("Symbol-Kontrollseite -> /tmp/symbole.html")
