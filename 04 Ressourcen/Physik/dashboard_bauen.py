#!/usr/bin/env python3
"""
Baut das Physik-Dashboard fuer Klasse 7.

Liest die Foliensaetze (Optik I, Optik II, Akustik) und den Stoffverteilungsplan
und erzeugt daraus eine einzelne HTML-Datei zum Nachschlagen. Uebernommen werden
nur die gefuellten Vorlagenseiten, die leeren Arbeitsseiten fallen weg.

Aufruf:  python3 dashboard_bauen.py
"""

import re, html, pathlib

BASIS = pathlib.Path(__file__).parent
ZIEL = BASIS / "Physik Dashboard.html"

SAETZE = [
    ("optik1", "Optik I", "Licht, Ausbreitung, Schatten, Astronomie", BASIS / "Optik/Optik I.html"),
    ("optik2", "Optik II", "Reflexion, Brechung, Linsen, Farben", BASIS / "Optik/Optik II.html"),
    ("akustik", "Akustik", "Schall und Hören (E-Niveau)", BASIS / "Akustik/Akustik.html"),
]

PLAN = BASIS / "Stoffverteilungsplan Physik Klasse 7 2026-27.md"

# Phywe-Versuche, zugeordnet zu den Wochen des Stoffverteilungsplans
VERSUCHE = [
    ("W04", "Durchsichtige und undurchsichtige Stoffe", "P1063300", "TESS", "Schülerversuch"),
    ("W05", "Geradlinige Ausbreitung des Lichts", "P1063200", "TESS", "Schülerversuch"),
    ("W06/W07", "Schatten (Kern- und Halbschatten)", "P1063400", "TESS", "Schülerversuch"),
    ("W08", "Mond- und Sonnenfinsternis (mit der Leuchtbox)", "P1063500", "TESS", "Demo"),
    ("W10", "Reflexion des Lichts", "P1063600", "TESS", "Schülerversuch"),
    ("W11", "Bilder am Planspiegel", "P1063800", "TESS", "Schülerversuch"),
    ("W12", "Brechung beim Übergang Luft zu Glas", "P1064300", "TESS", "Schülerversuch"),
    ("W12", "Brechung beim Übergang Glas zu Luft", "P1064700", "TESS", "Schülerversuch"),
    ("W12", "Brechung beim Übergang Luft zu Wasser", "P1064500", "TESS", "Schülerversuch"),
    ("W13", "Strahlengang und Brennweite bei einer Konvexlinse", "P1065300", "TESS", "Stationen"),
    ("W13", "Strahlengang und Brennweite bei einer Konkavlinse", "P1065500", "TESS", "Stationen"),
    ("W15", "Bildkonstruktion an Konvexlinsen", "P1065400", "TESS", "Stationen"),
    ("W15", "Funktionsweise des menschlichen Auges", "P1066700", "TESS", "Stationen"),
    ("W16", "Kurzsichtigkeit und ihre Korrektur", "P1066800", "TESS", "Stationen"),
    ("W16", "Weitsichtigkeit und ihre Korrektur", "P1066900", "TESS", "Stationen"),
    ("W19", "Brechung an einem Prisma", "P1065000", "TESS", "Stationen"),
    ("Zusatz", "Totalreflexion und Grenzwinkel", "P1064800", "TESS", "passt zur Glasfaser-Folie"),
    ("Zusatz", "Umlenkprisma", "P1065100", "TESS", "Anwendung Totalreflexion"),
    ("Zusatz", "Lichtdurchgang durch planparallele Platte", "P1064900", "TESS", "Vertiefung"),
    ("Zusatz", "Chromatische Linsenfehler", "P1066000", "TESS", "Vertiefung Farben"),
]

FEHLT = [
    ("Akustik", "Stimmgabel, Oszilloskop mit Mikrofon, Monochord, Vakuumglocke mit Klingel"),
    ("Magnetismus", "Stabmagnete, Eisenfeilspäne, Kompassnadeln, Spule"),
    ("Stromkreis", "Experimentierkästen, Vielfachmessgeräte"),
    ("Farbmischung", "Farbmischungs-Zubehör für die Leuchtbox (separat nachzurüsten)"),
]


def txt(s):
    """HTML-Tags raus, Entities aufloesen, Weissraum normalisieren."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", html.unescape(s)).strip()
    s = re.sub(r"\s+([.,;:!?)])", r"\1", s)     # Leerzeichen vor Satzzeichen
    s = re.sub(r"\(\s+", "(", s)
    return s


def parse_satz(pfad):
    """Zerlegt einen Foliensatz in Leitfragen-Abschnitte mit ihren Inhalten."""
    roh = pfad.read_text(encoding="utf-8")
    seiten = re.findall(r"<section class=\"folie[^\"]*\">(.*?)</section>", roh, flags=re.S)
    abschnitte, aktuell = [], None

    for s in seiten:
        titel_m = re.search(r"<div class=\"titelband\"><h1>(.*?)</h1></div>", s, flags=re.S)
        frage_m = re.search(r"<div class=\"nr\">(.*?)</div>\s*<h2>(.*?)</h2>", s, flags=re.S)
        svg_m = re.search(r"(<svg .*?</svg>)", s, flags=re.S)
        merk_m = re.search(r"<div class=\"merksatz[^\"]*\">(.*?)</div>", s, flags=re.S)

        # Leitfrage eroeffnet einen neuen Abschnitt
        if frage_m and txt(frage_m.group(1)).lower().startswith("leitfrage"):
            aktuell = {"nr": txt(frage_m.group(1)), "frage": txt(frage_m.group(2)),
                       "antwort": "", "inhalte": [], "checks": [], "loesung": ""}
            abschnitte.append(aktuell)
            continue

        if aktuell is None:      # alles vor der ersten Leitfrage (Kapiteltitel)
            continue

        # Antwortseite
        if frage_m and "antwort" in txt(frage_m.group(1)).lower():
            a = re.search(r"<div class=\"antwortzone\">(.*?)</div>", s, flags=re.S)
            if a:
                aktuell["antwort"] = txt(a.group(1))
            continue

        titel = txt(titel_m.group(1)) if titel_m else ""

        # Check-Seite
        if "class=\"check\"" in s:
            for auf in re.findall(r"<div class=\"aufgabe\">(.*?)</div>\s*</div>", s + "</div>", flags=re.S):
                frage = re.search(r"<p>(.*?)</p>", auf, flags=re.S)
                opts = re.findall(r"<li>(.*?)</li>", auf, flags=re.S)
                if frage:
                    aktuell["checks"].append((txt(frage.group(1)), [txt(o) for o in opts]))
            continue

        if titel.lower().startswith("lösung"):
            l = re.search(r"<div class=\"loesung\">(.*?)</div>", s, flags=re.S)
            if l:
                aktuell["loesung"] = txt(l.group(1))
            continue

        # Versuchsseite: nur die gefuellte Fassung (Beobachtung ausgefuellt)
        if "class=\"versuch\"" in s:
            felder = re.findall(r"<h2>(.*?)</h2>\s*<div class=\"feld[^\"]*\">(.*?)</div>", s, flags=re.S)
            gefuellt = {txt(k): v for k, v in felder}
            if txt(gefuellt.get("Beobachtung", "")):
                aktuell["inhalte"].append({
                    "art": "versuch", "titel": titel,
                    "svg": svg_m.group(1) if svg_m else "",
                    "beschreibung": txt(gefuellt.get("Beschreibung", "")),
                    "beobachtung": txt(gefuellt.get("Beobachtung", "")),
                    "ergebnis": txt(gefuellt.get("Ergebnis", "")),
                })
            continue

        # Inhaltsseite: nur die Vorlagenfassung, also die mit Zeichnung
        if svg_m and "zeichenzone" in s:
            aktuell["inhalte"].append({
                "art": "inhalt", "titel": titel,
                "svg": svg_m.group(1),
                "merksatz": txt(merk_m.group(1)) if merk_m else "",
            })
    return abschnitte


def md(s):
    """Markdown-Fettschrift und Anfuehrungszeichen fuer HTML aufbereiten."""
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s.replace("„", "&bdquo;").replace("“", "&ldquo;")


def parse_plan(pfad):
    """Holt die Wochenzeilen aus den beiden Tabellen des Stoffverteilungsplans."""
    zeilen = []
    for z in pfad.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(W\d\d)\s*\|(.*)", z)
        if m:
            sp = [md(t.strip()) for t in m.group(2).split("|")]
            zeilen.append((m.group(1), sp[0], sp[1], sp[2], sp[3], sp[4], sp[5]))
    return zeilen


CSS = """
:root{--bg:#0e1218;--card:#151a23;--card2:#1c2330;--line:#222a38;
--t1:#e8ecf2;--t2:#c6cdd8;--t3:#8b94a3;--t4:#657084;
--blue:#5aa2f0;--purple:#a78bfa;--green:#2dd4a7;--amber:#f0b954;
--pink:#f27ba8;--red:#f0716b;--shadow:0 1px 3px rgba(0,0,0,.4)}
html.light{--bg:#eef1f6;--card:#fff;--card2:#e9edf3;--line:#dde2ea;
--t1:#1c222c;--t2:#3d4654;--t3:#6b7586;--t4:#97a0af;
--blue:#2a78d6;--purple:#7c5cd6;--green:#149d76;--amber:#b97f14;
--pink:#d4537e;--red:#d84b45;--shadow:0 1px 3px rgba(20,30,50,.09)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--t1);
font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;padding:26px 20px 70px;line-height:1.45}
.wrap{max-width:1180px;margin:0 auto}
header{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
h1{font-size:25px;margin:0;font-weight:650;letter-spacing:-.015em}
.badge{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--amber);
background:color-mix(in srgb,var(--amber) 13%,transparent);
border:1px solid color-mix(in srgb,var(--amber) 32%,transparent);border-radius:9px;padding:3px 10px}
#themeBtn{margin-left:auto;background:var(--card);color:var(--t2);border:1px solid var(--line);
border-radius:10px;padding:4px 12px;font-size:12.5px;cursor:pointer}
.subtitle{font-size:13px;color:var(--t3);margin:5px 0 18px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:10px;margin-bottom:16px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:11px 15px;box-shadow:var(--shadow)}
.stat .lbl{font-size:11.5px;color:var(--t3)}
.stat .val{font-size:22px;font-weight:650;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat .sub{font-size:11px;color:var(--t4)}
.tabs-io>input{position:absolute;opacity:0;width:0;height:0;pointer-events:none}
nav.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}
nav.tabs label{background:var(--card);border:1px solid var(--line);color:var(--t3);border-radius:11px;
padding:7px 15px;font-size:13px;cursor:pointer;user-select:none}
nav.tabs label:hover{color:var(--t1);border-color:var(--t4)}
section.tab{display:none}
h2.frage{font-size:17px;margin:26px 0 4px;font-weight:640;letter-spacing:-.01em}
h2.frage .nr{font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;
color:var(--purple);display:block;margin-bottom:2px}
.antwort{background:color-mix(in srgb,var(--green) 10%,var(--card));border:1px solid
color-mix(in srgb,var(--green) 30%,var(--line));border-radius:12px;padding:10px 14px;font-size:13.5px;
color:var(--t2);margin:8px 0 16px}
.karte{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;
margin-bottom:12px;box-shadow:var(--shadow)}
.karte h3{margin:0 0 8px;font-size:15px;font-weight:620}
.karte h3 .art{font-size:10.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;
color:var(--amber);margin-left:8px}
.bild{background:#fff;border-radius:10px;padding:8px;overflow:hidden}
.bild svg{width:100%;height:auto;display:block}
.merk{font-size:13px;color:var(--t2);margin-top:9px;padding-left:11px;border-left:3px solid var(--pink)}
.vfeld{font-size:12.5px;color:var(--t2);margin-top:8px}
.vfeld b{color:var(--t1)}
details{margin-top:10px;font-size:12.5px;color:var(--t3)}
details summary{cursor:pointer;color:var(--blue)}
details ol{margin:6px 0 0 0;padding-left:20px}
details li{margin-bottom:2px}
table{width:100%;border-collapse:collapse;font-size:12.5px;background:var(--card);
border:1px solid var(--line);border-radius:13px;overflow:hidden;box-shadow:var(--shadow)}
th{text-align:left;padding:8px 11px;color:var(--t3);font-weight:600;font-size:11.5px;
text-transform:uppercase;letter-spacing:.03em;border-bottom:1px solid var(--line);background:var(--card2)}
td{padding:8px 11px;border-bottom:1px solid var(--line);color:var(--t2);vertical-align:top}
tr:last-child td{border-bottom:none}
td.w{color:var(--t1);font-weight:600;white-space:nowrap;font-variant-numeric:tabular-nums}
td.nr{font-variant-numeric:tabular-nums;color:var(--amber);white-space:nowrap}
.blk{display:inline-block;font-size:11px;padding:1px 8px;border-radius:7px;white-space:nowrap;
background:var(--card2);color:var(--t3);border:1px solid var(--line)}
.blk.optik{color:var(--blue);border-color:color-mix(in srgb,var(--blue) 35%,transparent)}
.blk.akustik{color:var(--purple);border-color:color-mix(in srgb,var(--purple) 35%,transparent)}
.blk.magnet{color:var(--green);border-color:color-mix(in srgb,var(--green) 35%,transparent)}
.blk.strom{color:var(--amber);border-color:color-mix(in srgb,var(--amber) 35%,transparent)}
.blk.ka{color:var(--red);border-color:color-mix(in srgb,var(--red) 35%,transparent)}
.hinweis{font-size:12.5px;color:var(--t3);margin:14px 0 0;padding:11px 14px;background:var(--card);
border:1px solid var(--line);border-radius:12px}
/* Stile der Folien-SVGs, damit die Zeichnungen hier genauso aussehen */
svg .licht{stroke:#E8B400;stroke-width:1.4;fill:none}
svg .koerper{fill:#6E6E6E;stroke:#333;stroke-width:1}
svg .hilfslinie{stroke:#999;stroke-width:.8;stroke-dasharray:4 3;fill:none}
svg .beschriftung{font-family:-apple-system,Helvetica,sans-serif;font-size:11px;fill:#111}
svg .beschriftung.klein{font-size:9.5px}
svg .kursiv{font-style:italic}
"""


def bau():
    saetze = [(k, n, u, parse_satz(p)) for k, n, u, p in SAETZE if p.exists()]
    plan = parse_plan(PLAN)
    seiten = sum(len(a["inhalte"]) for _, _, _, absch in saetze for a in absch)
    fragen = sum(len(absch) for _, _, _, absch in saetze)

    o = []
    o.append('<!doctype html><html lang="de"><head><meta charset="utf-8">')
    o.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    o.append("<title>Physik Klasse 7 | Dashboard</title><style>" + CSS + "</style></head><body><div class='wrap'>")
    o.append('<header><h1>Physik Klasse 7</h1><span class="badge">Schuljahr 2026/27</span>'
             '<button id="themeBtn">Hell / Dunkel</button></header>')
    o.append('<div class="subtitle">Nachschlagewerk zu Jahresplanung, Inhalten und Versuchen. '
             'Erzeugt aus den Foliensätzen, ohne die leeren Zeichenseiten.</div>')

    o.append('<div class="stats">')
    for lbl, val, sub in [("Unterrichtswochen", "39", "18 + 21"), ("Stunden brutto", "78", "rund 68 planbar"),
                          ("Leitfragen", str(fragen), "durchnummeriert"),
                          ("Inhaltsseiten", str(seiten), "mit Zeichnung"),
                          ("Phywe-Versuche", str(len([v for v in VERSUCHE if v[0] != "Zusatz"])), "zugeordnet")]:
        o.append(f'<div class="stat"><div class="lbl">{lbl}</div><div class="val">{val}</div>'
                 f'<div class="sub">{sub}</div></div>')
    o.append("</div>")

    reiter = [("plan", "Jahresplan")] + [(k, n) for k, n, _, _ in saetze] + [("versuche", "Versuche")]
    o.append('<div class="tabs-io">')
    for i, (k, _) in enumerate(reiter):
        o.append(f'<input type="radio" name="tab" id="t-{k}"{" checked" if i == 0 else ""}>')
    o.append("<style>")
    for k, _ in reiter:
        o.append(f'#t-{k}:checked ~ nav.tabs label[for="t-{k}"]{{background:var(--card2);color:var(--t1);'
                 f'border-color:var(--blue);font-weight:600}}')
        o.append(f"#t-{k}:checked ~ #s-{k}{{display:block}}")
    o.append("</style>")
    o.append('<nav class="tabs">')
    for k, n in reiter:
        o.append(f'<label for="t-{k}">{n}</label>')
    o.append("</nav>")

    # Jahresplan
    o.append('<section class="tab" id="s-plan"><table><tr><th>Woche</th><th>ab</th><th>Block</th>'
             "<th>Thema</th><th>Bildungsplan</th><th>Folien</th></tr>")
    farbe = {"Optik I": "optik", "Optik II": "optik", "Akustik": "akustik", "Magnetismus": "magnet",
             "Stromkreis": "strom", "Klassenarbeit": "ka"}
    for nr, datum, block, thema, bp, folien, _material in plan:
        cls = farbe.get(block, "")
        o.append(f'<tr><td class="w">{nr}</td><td class="w">{datum}</td>'
                 f'<td><span class="blk {cls}">{block}</span></td><td>{thema}</td>'
                 f'<td>{bp}</td><td>{folien}</td></tr>')
    o.append("</table></section>")

    # Foliensaetze
    for k, name, unter, absch in saetze:
        o.append(f'<section class="tab" id="s-{k}"><div class="subtitle">{name}: {unter}</div>')
        for a in absch:
            o.append(f'<h2 class="frage"><span class="nr">{a["nr"]}</span>{a["frage"]}</h2>')
            if a["antwort"]:
                o.append(f'<div class="antwort">{a["antwort"]}</div>')
            for c in a["inhalte"]:
                if c["art"] == "inhalt":
                    o.append(f'<div class="karte"><h3>{c["titel"]}</h3>'
                             f'<div class="bild">{c["svg"]}</div>'
                             + (f'<div class="merk">{c["merksatz"]}</div>' if c["merksatz"] else "")
                             + "</div>")
                else:
                    o.append(f'<div class="karte"><h3>{c["titel"]}<span class="art">Versuch</span></h3>'
                             + (f'<div class="bild">{c["svg"]}</div>' if c["svg"] else "")
                             + f'<div class="vfeld"><b>Durchführung:</b> {c["beschreibung"]}</div>'
                             + f'<div class="vfeld"><b>Beobachtung:</b> {c["beobachtung"]}</div>'
                             + f'<div class="vfeld"><b>Ergebnis:</b> {c["ergebnis"]}</div></div>')
            if a["checks"]:
                o.append("<details><summary>Check-Fragen anzeigen"
                         + (f' (Lösung: {a["loesung"]})' if a["loesung"] else "") + "</summary>")
                for frage, opts in a["checks"]:
                    o.append(f"<div style='margin-top:8px'><b>{frage}</b><ol type='a'>"
                             + "".join(f"<li>{x}</li>" for x in opts) + "</ol></div>")
                o.append("</details>")
        o.append("</section>")

    # Versuche
    o.append('<section class="tab" id="s-versuche"><table><tr><th>Woche</th><th>Versuch</th>'
             "<th>Artikel-Nr.</th><th>Set</th><th>Form</th></tr>")
    for w, n, nr, satz, form in VERSUCHE:
        o.append(f'<tr><td class="w">{w}</td><td>{n}</td><td class="nr">{nr}</td>'
                 f"<td>{satz}</td><td>{form}</td></tr>")
    o.append("</table>")
    o.append('<div class="hinweis"><b>Nicht durch die Optiksets abgedeckt:</b><br>'
             + "<br>".join(f"{b}: {m}" for b, m in FEHLT) + "</div>")
    o.append("</section></div>")

    o.append("""<script>
const b=document.getElementById('themeBtn'),r=document.documentElement;
if(localStorage.getItem('phys-theme')==='light')r.classList.add('light');
b.onclick=()=>{r.classList.toggle('light');
localStorage.setItem('phys-theme',r.classList.contains('light')?'light':'dark');};
</script></div></body></html>""")

    ZIEL.write_text("\n".join(o), encoding="utf-8")
    print(f"gebaut: {ZIEL.name}")
    print(f"  {fragen} Leitfragen, {seiten} Inhaltsseiten, {len(plan)} Wochen, {len(VERSUCHE)} Versuche")


if __name__ == "__main__":
    bau()
