#!/usr/bin/env python3
"""Baut aus den Vault-Notizen eine einzelne, in sich geschlossene HTML-Datei.

Quelle:  04 Ressourcen/Sport/Sportcurriculum Realschule.md
         04 Ressourcen/Sport/LA Sprengeltabelle Remstal (männlich).md
Ziel:    04 Ressourcen/Sport/Sportcurriculum.html

Die Zieldatei laeuft ohne Server, ohne Netz und ohne externe Schriften,
damit sie in der Schul-Cloud liegen und dort direkt geoeffnet werden kann.

Aufruf:  python3 .scripts/sport_curriculum_build.py
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
ZIEL = VAULT / "04 Ressourcen/Sport/Sportcurriculum.html"
PARSER = Path(__file__).resolve().parent / "sport_curriculum_parse.py"

SCHULJAHR = "2026/27"
SCHULE = "Sportfachschaft Realschule"
QUELLE_TABELLE = "Sprengel Remstal, Stand 10.09.2011"
SPRENGELSCHULEN = (
    "Friedrich-Schiller-Gymnasium Fellbach · Gustav-Stresemann-Gymnasium Fellbach · "
    "Burggymnasium Schorndorf · Max-Planck-Gymnasium Schorndorf · Salier-Gymnasium Waiblingen · "
    "Staufer-Gymnasium Waiblingen · Remstalgymnasium Weinstadt"
)


def e(text):
    return html.escape(str(text), quote=True)


def markup(text):
    """**fett** und *kursiv* aus dem Markdown in Auszeichnung uebersetzen."""
    out = e(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"\*(.+?)\*", r'<span class="nb">\1</span>', out)
    return out


def daten():
    roh = subprocess.run(
        [sys.executable, str(PARSER)], capture_output=True, text=True, check=True
    ).stdout
    return json.loads(roh)


# --- Bausteine ---------------------------------------------------------------

def bahnleiste(d):
    teile = []
    for k in d["klassen"]:
        nr = k["klasse"]
        erst = " ist-aktiv" if nr == 5 else ""
        teile.append(
            f'<button class="bahn{erst}" role="tab" id="tab-{nr}" aria-controls="klasse-{nr}" '
            f'aria-selected="{"true" if nr == 5 else "false"}" tabindex="{"0" if nr == 5 else "-1"}" '
            f'data-klasse="{nr}">'
            f'<span class="sr">Klasse </span><span class="bahn-nr">{nr}</span>'
            f"</button>"
        )
    return (
        '<div class="bahnband-innen">'
        '<p class="bahn-marke" aria-hidden="true">Klassenstufe</p>'
        '<div class="bahnen" role="tablist" aria-label="Klassenstufe wählen">'
        + "".join(teile)
        + "</div></div>"
    )


def inhalte(k):
    gruppen = []
    for g in k["gruppen"]:
        zusatz = (
            f' <span class="nb">{e(g["zusatz"])}</span>' if g.get("zusatz") else ""
        )
        if g["items"]:
            punkte = "".join(f"<li>{markup(i)}</li>" for i in g["items"])
            rumpf = f"<ul>{punkte}</ul>"
            leer = ""
        else:
            # Bereich ohne Ausdifferenzierung im Curriculum
            rumpf = ""
            leer = " ist-knapp"
        gruppen.append(
            f'<section class="gruppe{leer}"><h4>{markup(g["titel"])}{zusatz}</h4>{rumpf}</section>'
        )
    block = "".join(gruppen)
    if k.get("note"):
        block += (
            f'<aside class="vermerk"><h4>{e(k["note"]["titel"])}</h4>'
            f'<p>{markup(k["note"]["text"])}</p></aside>'
        )
    return block


def tabelle(nr, t):
    if not t:
        return '<p class="leer">Fuer diese Klasse liegt keine Bewertungstabelle vor.</p>'
    kopf = "".join(f"<th scope=\"col\">{e(z)}</th>" for z in t["kopf"])
    zeilen = []
    for row in t["zeilen"]:
        note = row[0]
        ganz = " ist-ganz" if re.fullmatch(r"[1-6]", note) else ""
        zellen = f'<th scope="row" class="note">{e(note)}</th>'
        zellen += "".join(f"<td>{e(z)}</td>" for z in row[1:])
        zeilen.append(f'<tr class="zeile{ganz}">{zellen}</tr>')
    return (
        f'<div class="tabellenfeld"><table class="noten">'
        f"<caption>Bewertung Klasse {nr}, Schüler (männlich)</caption>"
        f"<thead><tr>{kopf}</tr></thead><tbody>{''.join(zeilen)}</tbody></table></div>"
        f'<p class="wisch">Tabelle seitlich wischen, die Notenspalte bleibt stehen.</p>'
    )


def hinweise(nr, abweichungen):
    """Was der Sprengel zusaetzlich fuehrt und was davon bei uns gilt."""
    eintraege = abweichungen.get(str(nr), [])
    zeilen = []
    for a in eintraege:
        if "optional" in a["status"].lower():
            zeilen.append(
                f'<li><b>{e(a["disziplin"])}</b> läuft optional mit, je nach Lehrkraft.</li>'
            )
        elif a["status"].startswith("nur "):
            zeilen.append(
                f'<li>Der Sprengel führt zusätzlich <b>{e(a["disziplin"])}</b>. '
                f'Bei uns bewertet wird {e(a["status"])}.</li>'
            )
        else:
            # Status wie "nicht aufgeführt": kein Satzbaustein, eigene Formulierung
            zeilen.append(
                f'<li>Der Sprengel führt zusätzlich <b>{e(a["disziplin"])}</b>. '
                f"Bei uns steht das nicht im Curriculum und wird nicht bewertet.</li>"
            )
    liste = f"<ul class=\"hinweise\">{''.join(zeilen)}</ul>" if zeilen else ""
    return (
        f'<p class="quelle">Quelle: {e(QUELLE_TABELLE)}. Die Werte gelten für '
        f"Schüler (männlich).</p>{liste}"
    )


def klassenpanels(d):
    panels = []
    for k in d["klassen"]:
        nr = k["klasse"]
        t = d["tabellen"].get(str(nr))
        panels.append(
            f'<section class="klasse" id="klasse-{nr}" role="tabpanel" aria-labelledby="tab-{nr}" '
            f'data-klasse="{nr}">'
            f'<header class="klasse-kopf">'
            f"<h2>Klasse {nr}</h2>"
            f'<p class="schwer">{e(d["uebersicht"].get(str(nr), ""))}</p>'
            f'<button class="druck" data-druck="klasse" data-nr="{nr}">'
            f"{DRUCKER}Klasse {nr} drucken</button>"
            f"</header>"
            f'<div class="spalten">'
            f'<div class="inhalt"><h3>Verbindliche Inhalte</h3>{inhalte(k)}</div>'
            f'<div class="bewertung"><h3>Bewertungstabelle Leichtathletik</h3>{tabelle(nr, t)}'
            f"{hinweise(nr, d.get('abweichungen', {}))}</div>"
            f"</div></section>"
        )
    return "".join(panels)


def progression(d):
    p = d["progression"]
    if not p:
        return ""
    kopf = "".join(f'<th scope="col">{e(z)}</th>' for z in p["kopf"])
    zeilen = []
    for row in p["zeilen"]:
        zellen = f'<th scope="row">{markup(row[0])}</th>'
        for z in row[1:]:
            zellen += f"<td>{marker(z)}</td>"
        zeilen.append(f"<tr>{zellen}</tr>")
    return (
        f'<div class="tabellenfeld"><table class="progression">'
        f"<thead><tr>{kopf}</tr></thead><tbody>{''.join(zeilen)}</tbody></table></div>"
        f'<p class="legende">{PUNKT_VOLL} verbindlich &nbsp; {PUNKT_OFFEN} optional '
        f'&nbsp; <span class="strich">–</span> nicht vorgesehen</p>'
    )


def marker(zelle):
    roh = re.sub(r"\*.*?\*", "", zelle).strip()
    if roh == "✓":
        rest = re.search(r"\*(.+?)\*", zelle)
        zusatz = f' <span class="nb">{e(rest.group(1))}</span>' if rest else ""
        return f'{PUNKT_VOLL}<span class="sr">verbindlich</span>{zusatz}'
    if roh == "○":
        return f'{PUNKT_OFFEN}<span class="sr">optional</span>'
    if roh in ("–", "-", ""):
        return '<span class="strich" aria-label="nicht vorgesehen">–</span>'
    return markup(zelle)


def bereiche(d):
    klassen = [5, 6, 7, 8, 9, 10]
    kopf = "".join(f'<th scope="col">{k}</th>' for k in klassen)
    zeilen = []
    for b in d["bereiche"]:
        zellen = f'<th scope="row">{markup(b["name"])}</th>'
        for k in klassen:
            if k in b["klassen"]:
                zellen += f'<td>{PUNKT_VOLL}<span class="sr">Klasse {k}: ja</span></td>'
            else:
                zellen += '<td><span class="strich">–</span><span class="sr">nein</span></td>'
        zeilen.append(f"<tr>{zellen}</tr>")
    return (
        f'<div class="tabellenfeld"><table class="matrix">'
        f'<thead><tr><th scope="col">Bereich</th>{kopf}</tr></thead>'
        f"<tbody>{''.join(zeilen)}</tbody></table></div>"
        f'<p class="legende">{PUNKT_VOLL} im Jahrgang vorgesehen &nbsp; '
        f'<span class="strich">–</span> nicht vorgesehen</p>'
    )


# --- gezeichnete Marken ------------------------------------------------------

DRUCKER = (
    '<svg class="ikon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" '
    'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M6.5 9V3.5h11V9"/>'
    '<rect x="3.5" y="9" width="17" height="7.5" rx="1.5"/>'
    '<path d="M6.5 14.5h11v6h-11z" fill="var(--grund)"/><path d="M17 11.8h1.2"/></svg>'
)

PUNKT_VOLL = (
    '<svg class="punkt" viewBox="0 0 12 12" width="9" height="9" aria-hidden="true">'
    '<circle cx="6" cy="6" r="4.5" fill="currentColor"/></svg>'
)

PUNKT_OFFEN = (
    '<svg class="punkt" viewBox="0 0 12 12" width="9" height="9" aria-hidden="true">'
    '<circle cx="6" cy="6" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
)


# --- Seite -------------------------------------------------------------------

VORLAGE = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sportcurriculum Realschule · Klasse 5 bis 10</title>
<style>
:root{
  --grund:#F5F7F4; --papier:#FFFFFF; --tinte:#111C17; --gedaempft:#4A5A52;
  --feld:#17453A; --feld-tief:#0E2E26; --feld-hell:#E4EDE7; --linie:#CBD5CE;
  --signal:#A8322A; --kalk:#FFFFFF;
  --schrift: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --masz: 1120px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--grund);color:var(--tinte);font-family:var(--schrift);
  font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
::selection{background:var(--feld);color:var(--kalk)}
:focus-visible{outline:2.5px solid var(--signal);outline-offset:2px;border-radius:2px}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0}
.nb{color:var(--gedaempft);font-style:normal;font-size:.92em}

/* Kopfband, Kalklinie auf Rasen */
.kopf{background:var(--feld);color:var(--kalk);
  background-image:linear-gradient(var(--feld),var(--feld)),
    repeating-linear-gradient(90deg,transparent 0 118px,rgba(255,255,255,.05) 118px 120px);
  background-blend-mode:normal}
.kopf-innen{max-width:var(--masz);margin:0 auto;padding:26px 24px 22px;
  display:flex;flex-wrap:wrap;gap:18px;align-items:flex-end;justify-content:space-between}
.kopf h1{margin:0;font-size:clamp(1.6rem,1.15rem + 1.8vw,2.5rem);font-weight:800;
  letter-spacing:-.028em;line-height:1.05}
.kopf .unter{margin:6px 0 0;color:#BFD4C9;font-size:.92rem;letter-spacing:.01em}
.kopf-akt{display:flex;gap:10px;flex-wrap:wrap}

/* Knoepfe */
button{font:inherit;cursor:pointer}
.druck{display:inline-flex;align-items:center;gap:7px;padding:9px 14px;border-radius:7px;
  border:1.5px solid var(--linie);background:var(--papier);color:var(--tinte);
  font-size:.88rem;font-weight:600;letter-spacing:.005em;
  transition:background .16s ease-out,border-color .16s ease-out,transform .16s ease-out}
.druck:hover{background:var(--feld-hell);border-color:var(--feld)}
.druck:active{transform:translateY(1px)}
.kopf-akt .druck{background:transparent;color:var(--kalk);border-color:rgba(255,255,255,.4)}
.kopf-akt .druck:hover{background:rgba(255,255,255,.12);border-color:var(--kalk)}
.kopf-akt .druck .ikon path[fill]{fill:var(--feld)}
.ikon{flex:none}

/* Bahnleiste, sechs Jahrgaenge als sechs Bahnen */
.bahnband{position:sticky;top:0;z-index:5;background:var(--feld-tief);
  box-shadow:0 1px 0 rgba(0,0,0,.25)}
.bahnband-innen{max-width:var(--masz);margin:0 auto;padding:0 24px;
  display:flex;align-items:stretch;gap:20px}
.bahn-marke{margin:0;align-self:center;color:#8FB0A2;font-size:.7rem;font-weight:600;
  text-transform:uppercase;letter-spacing:.14em;white-space:nowrap}
.bahnen{flex:1;display:grid;grid-template-columns:repeat(6,1fr);gap:1px;
  background:rgba(255,255,255,.14)}
.bahn{position:relative;border:0;background:var(--feld-tief);color:#B9D0C6;
  padding:11px 8px 12px;display:block;
  transition:background .18s cubic-bezier(.2,.7,.3,1),color .18s ease-out}
.bahn::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;
  background:var(--signal);transform:scaleX(0);transform-origin:left;
  transition:transform .34s cubic-bezier(.16,.84,.24,1)}
.bahn:hover{background:#143B31;color:var(--kalk)}
.bahn.ist-aktiv{background:var(--papier);color:var(--tinte)}
.bahn.ist-aktiv::after{transform:scaleX(1)}
.bahn-nr{display:block;font-size:1.5rem;font-weight:800;letter-spacing:-.035em;
  line-height:1.1;font-variant-numeric:tabular-nums}

/* Inhalt */
main{max-width:var(--masz);margin:0 auto;padding:0 24px 64px}
.klasse{background:var(--papier);border:1px solid var(--linie);border-top:0;
  padding:26px 26px 30px;scroll-margin-top:72px}
/* Ohne JavaScript bleiben alle Jahrgaenge sichtbar, das Skript blendet sie erst aus. */
.klasse + .klasse{border-top:1px solid var(--linie);margin-top:20px}
.js .klasse + .klasse{border-top:0;margin-top:0}
.klasse-kopf{display:flex;flex-wrap:wrap;align-items:baseline;gap:12px 18px;
  padding-bottom:16px;margin-bottom:22px;border-bottom:1.5px solid var(--tinte)}
.klasse-kopf h2{margin:0;font-size:1.9rem;font-weight:800;letter-spacing:-.03em;line-height:1}
.schwer{margin:0;color:var(--gedaempft);font-size:.94rem;flex:1 1 240px}
.klasse-kopf .druck{margin-left:auto}
.spalten{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:34px}
.inhalt,.bewertung{min-width:0}
.spalten h3{margin:0 0 16px;font-size:.76rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.1em;color:var(--gedaempft)}
.gruppe{margin:0 0 20px}
.gruppe.ist-knapp{margin-bottom:14px}
.gruppe h4{margin:0 0 7px;font-size:1rem;font-weight:700;letter-spacing:-.01em}
.gruppe ul{margin:0;padding:0;list-style:none}
.gruppe li{position:relative;padding:3px 0 3px 17px;font-size:.95rem}
.gruppe li::before{content:"";position:absolute;left:2px;top:12px;width:6px;height:1.5px;
  background:var(--feld)}
.vermerk{background:var(--feld-hell);padding:14px 16px;border-radius:6px;margin-top:24px}
.vermerk h4{margin:0 0 5px;font-size:.9rem;font-weight:700}
.vermerk p{margin:0;font-size:.9rem;color:var(--gedaempft)}

/* Tabellen */
.tabellenfeld{overflow-x:auto;-webkit-overflow-scrolling:touch;
  border:1px solid var(--linie);border-radius:6px;background:var(--papier)}
.tabellenfeld::-webkit-scrollbar{height:9px}
.tabellenfeld::-webkit-scrollbar-thumb{background:var(--linie);border-radius:5px}
.tabellenfeld::-webkit-scrollbar-thumb:hover{background:var(--gedaempft)}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
caption{text-align:left;padding:10px 12px;font-size:.8rem;color:var(--gedaempft);
  border-bottom:1px solid var(--linie)}
th,td{padding:5px 11px;text-align:right;font-size:.88rem;white-space:nowrap}
thead th{background:var(--feld);color:var(--kalk);font-weight:600;font-size:.78rem;
  letter-spacing:.02em;position:sticky;top:0}
tbody th,tbody td{border-top:1px solid #EAEFEB}
.noten .note{text-align:left;font-weight:700;width:1%}
.noten .ist-ganz td,.noten .ist-ganz th{background:#F2F6F3;font-weight:600}
.noten tbody tr:hover td,.noten tbody tr:hover th{background:var(--feld-hell)}
.progression th[scope=row],.matrix th[scope=row]{text-align:left;font-weight:600;
  white-space:normal;min-width:130px}
.progression td,.matrix td{text-align:center;color:var(--feld)}
.matrix thead th{text-align:center}
.strich{color:#9AA8A0}
.punkt{vertical-align:-1px}
.legende{margin:10px 2px 0;font-size:.8rem;color:var(--gedaempft)}
.legende .punkt{color:var(--feld)}
.quelle{margin:12px 2px 0;font-size:.78rem;color:var(--gedaempft);line-height:1.45}
.hinweise{margin:8px 2px 0;padding:0;list-style:none}
.hinweise li{position:relative;padding:2px 0 2px 15px;font-size:.78rem;
  color:var(--gedaempft);line-height:1.45}
.hinweise li::before{content:"";position:absolute;left:1px;top:11px;width:5px;height:1.5px;
  background:var(--gedaempft)}
.hinweise b{color:var(--tinte);font-weight:600}
.leer{color:var(--gedaempft);font-size:.9rem}

/* Gesamtblick */
.gesamt{margin-top:38px}
.gesamt h2{font-size:1.35rem;font-weight:800;letter-spacing:-.02em;margin:0 0 4px}
.gesamt p.hin{margin:0 0 18px;color:var(--gedaempft);font-size:.92rem}
.gesamt-block{background:var(--papier);border:1px solid var(--linie);border-radius:8px;
  padding:22px 24px 24px;margin-bottom:22px}
.gesamt-block h3{margin:0 0 14px;font-size:1rem;font-weight:700;letter-spacing:-.01em}

footer{border-top:1.5px solid var(--linie);margin-top:10px;padding:22px 0 0;
  color:var(--gedaempft);font-size:.82rem;line-height:1.6}
footer b{color:var(--tinte)}

@media (max-width:860px){
  .spalten{grid-template-columns:minmax(0,1fr);gap:26px}
  .bahnband-innen{padding:0 14px;gap:0}
  .bahn-marke{display:none}
  .bahn{padding:9px 8px 10px;text-align:center}
  .bahn-nr{font-size:1.32rem}
  main{padding:0 14px 48px}
  .klasse{padding:20px 16px 24px}
  .klasse-kopf .druck{margin-left:0;width:100%;justify-content:center}
  .kopf-innen{padding:20px 14px 18px}
  .kopf-akt .druck{width:100%;justify-content:center}
  /* Note bleibt beim seitlichen Wischen stehen */
  .noten th.note{position:sticky;left:0;background:var(--papier);
    box-shadow:1px 0 0 var(--linie)}
  .noten .ist-ganz th.note{background:#F2F6F3}
  .wisch{display:block}
}
.wisch{display:none;margin:7px 2px 0;font-size:.76rem;color:var(--gedaempft)}
@media (prefers-reduced-motion:reduce){
  *{transition-duration:.01ms !important;animation-duration:.01ms !important}
}

/* Druck */
@media print{
  @page{size:A4;margin:14mm 12mm}
  html,body{background:#fff;font-size:10.5pt}
  .bahnband,.kopf-akt,.druck,.wisch,.tabellenfeld::-webkit-scrollbar{display:none !important}
  .noten th.note{position:static;box-shadow:none}
  .kopf{background:#fff;color:#000;border-bottom:2pt solid #000}
  .kopf-innen{padding:0 0 8pt;max-width:none;display:block}
  .kopf h1{font-size:17pt}
  .kopf .unter{color:#333;margin-top:3pt}
  main{max-width:none;padding:0}
  .klasse{border:0;padding:0;margin:0 0 10pt;break-inside:auto}
  .klasse[hidden]{display:block}
  .js .klasse + .klasse{margin-top:0}
  .klasse-kopf{border-bottom:1pt solid #000;padding-bottom:5pt;margin-bottom:10pt}
  .klasse-kopf h2{font-size:14pt}
  .spalten{grid-template-columns:minmax(0,.78fr) minmax(0,1.22fr);gap:12pt}
  .gruppe li::before{background:#000}
  .tabellenfeld{overflow:visible;border:.5pt solid #666;border-radius:0}
  thead th{background:#E8E8E8 !important;color:#000 !important;
    -webkit-print-color-adjust:exact;print-color-adjust:exact;position:static;
    white-space:normal;vertical-align:bottom;line-height:1.15}
  .noten .ist-ganz td,.noten .ist-ganz th{background:#F2F2F2 !important;
    -webkit-print-color-adjust:exact;print-color-adjust:exact}
  th,td{padding:2pt 4.5pt;font-size:8.4pt}
  table{width:100%;table-layout:auto}
  caption{padding:5pt 6pt;font-size:8pt}
  .vermerk{background:#F2F2F2 !important;-webkit-print-color-adjust:exact;
    print-color-adjust:exact;border:.5pt solid #999}
  .progression td,.matrix td{color:#000}
  .gesamt-block{border:.5pt solid #999;border-radius:0;padding:10pt 12pt;break-inside:avoid}
  footer{margin-top:12pt;padding-top:8pt;border-top:.5pt solid #999;font-size:8pt}
  /* eine Klasse drucken */
  body[data-druck="klasse"] .klasse:not(.drucken){display:none !important}
  body[data-druck="klasse"] .gesamt{display:none !important}
  /* alles drucken, jede Klasse auf eigener Seite */
  body[data-druck="alles"] .klasse{break-before:page}
  body[data-druck="alles"] .klasse:first-of-type{break-before:auto}
  body[data-druck="alles"] .gesamt{break-before:page}
}
</style>
</head>
<body>
<!--
THESIS: Ein Sportcurriculum wird nach Jahrgang gelesen, nicht als Fliesstext. Wer die 8er hat,
sieht Inhalte und Bewertungstabelle zusammen. Verweigert wird das lange Scrolldokument.
OWN-WORLD: Die Laufbahn. Sechs Jahrgaenge als sechs Bahnen, Kalkweiss auf tiefem Rasengruen,
Papier fuer den Inhalt, Bahnenrot nur als Markierung der aktiven Bahn. Linien statt Karten.
STORY: Der Kollege waehlt seine Klasse, liest die verbindlichen Inhalte, prueft die Noten-
werte und druckt entweder sein Blatt oder das gesamte Curriculum fuer den Ordner.
FIRST VIEWPORT: Gruenes Kopfband mit Titel und Stand, darunter die Bahnleiste 5 bis 10 mit
grossen Ziffern, darunter zweispaltig links Inhalte, rechts die Bewertungstabelle.
FORM: Jahrgangsregister statt Dokumentgliederung.
FINISH: unreviewed und undokumentiert ist unfertig; der Bau endet mit Pruefung im Browser,
Druckkontrolle und einem Vermerk in der Vault-Notiz.
-->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <h1>Sportcurriculum Klasse 5 bis 10</h1>
      <p class="unter">__SCHULE__ · Bildungsplan Baden-Württemberg · Stand Schuljahr __SCHULJAHR__</p>
    </div>
    <div class="kopf-akt">
      <button class="druck" data-druck="alles">__DRUCKER__Gesamtes Curriculum drucken</button>
    </div>
  </div>
</header>

<nav class="bahnband" aria-label="Klassenstufen">
__BAHNEN__
</nav>

<main>
__PANELS__

  <section class="gesamt" aria-label="Gesamtübersicht">
    <h2>Über alle Jahrgänge</h2>
    <p class="hin">Die beiden Tabellen zeigen den Aufbau über die sechs Schuljahre hinweg.</p>

    <div class="gesamt-block">
      <h3>Leichtathletik, Steigerung der Anforderungen</h3>
      __PROGRESSION__
    </div>

    <div class="gesamt-block">
      <h3>Inhaltsbereiche nach Klassenstufe</h3>
      __BEREICHE__
    </div>
  </section>

  <footer>
    <p><b>Curriculum:</b> gemeinsam erarbeitet von der Sportfachschaft, orientiert am Bildungsplan
    Baden-Württemberg für die Realschule. Ab Klasse 9 bestimmt die Lehrkraft das Angebot
    zunehmend eigenständig.</p>
    <p><b>Bewertungstabellen:</b> __QUELLE__. Sie gelten für Schüler (männlich).
    Beteiligte Sprengelschulen: __SCHULEN__</p>
    <p>Stand: Schuljahr __SCHULJAHR__</p>
  </footer>
</main>

<script>
(function(){
  document.documentElement.className += " js";

  var bahnen = Array.prototype.slice.call(document.querySelectorAll(".bahn"));
  var panels = Array.prototype.slice.call(document.querySelectorAll(".klasse"));

  function zeige(nr, fokus, stumm){
    bahnen.forEach(function(b){
      var an = b.dataset.klasse === String(nr);
      b.classList.toggle("ist-aktiv", an);
      b.setAttribute("aria-selected", an ? "true" : "false");
      b.tabIndex = an ? 0 : -1;
      if(an && fokus){ b.focus(); }
    });
    panels.forEach(function(p){
      p.hidden = p.dataset.klasse !== String(nr);
    });
    if(stumm){ return; }
    try{ history.replaceState(null, "", "#klasse-" + nr); }catch(err){}
  }

  bahnen.forEach(function(b){
    b.addEventListener("click", function(){ zeige(b.dataset.klasse, false); });
  });

  document.querySelector(".bahnen").addEventListener("keydown", function(ev){
    var i = bahnen.indexOf(document.activeElement);
    if(i < 0){ return; }
    var ziel = null;
    if(ev.key === "ArrowRight"){ ziel = (i + 1) % bahnen.length; }
    if(ev.key === "ArrowLeft"){ ziel = (i - 1 + bahnen.length) % bahnen.length; }
    if(ev.key === "Home"){ ziel = 0; }
    if(ev.key === "End"){ ziel = bahnen.length - 1; }
    if(ziel === null){ return; }
    ev.preventDefault();
    zeige(bahnen[ziel].dataset.klasse, true);
  });

  // Druck
  function drucken(modus, nr){
    panels.forEach(function(p){
      p.classList.toggle("drucken", modus === "klasse" && p.dataset.klasse === String(nr));
    });
    document.body.dataset.druck = modus;
    window.print();
  }
  window.addEventListener("afterprint", function(){
    delete document.body.dataset.druck;
    panels.forEach(function(p){ p.classList.remove("drucken"); });
  });
  document.addEventListener("click", function(ev){
    var b = ev.target.closest("[data-druck]");
    if(!b || b.tagName !== "BUTTON"){ return; }
    drucken(b.dataset.druck, b.dataset.nr);
  });

  // Einstieg ueber Adresszeile, z. B. .../Sportcurriculum.html#klasse-8
  var start = (location.hash.match(/^#klasse-(\d+)$/) || [])[1];
  if(!start || !document.getElementById("klasse-" + start)){ start = "5"; }
  zeige(start, false, true);
})();
</script>
</body>
</html>
"""


def main():
    d = daten()
    seite = VORLAGE
    ersetzungen = {
        "__SCHULE__": e(SCHULE),
        "__SCHULJAHR__": e(SCHULJAHR),
        "__QUELLE__": e(QUELLE_TABELLE),
        "__SCHULEN__": e(SPRENGELSCHULEN),
        "__DRUCKER__": DRUCKER,
        "__BAHNEN__": bahnleiste(d),
        "__PANELS__": klassenpanels(d),
        "__PROGRESSION__": progression(d),
        "__BEREICHE__": bereiche(d),
    }
    for schluessel, wert in ersetzungen.items():
        seite = seite.replace(schluessel, wert)

    ZIEL.write_text(seite, encoding="utf-8")
    print(f"geschrieben: {ZIEL.relative_to(VAULT)}  ({len(seite)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
