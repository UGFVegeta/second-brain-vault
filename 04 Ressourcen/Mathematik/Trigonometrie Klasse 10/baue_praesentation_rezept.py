"""Präsentation zum Rezept Trigonometrie (Kurzfassung), Mathe 10b, Fr 20.11.2026, 1. Stunde (45 min).
Oskar 19.11.: Rezept per Klick aufdecken: erst 0, 1, 2 (gilt für alles), dann der Ja-Weg, danach der Nein-Weg;
rechts daneben läuft parallel das passende Beispiel. Die Klasse schreibt das Rezept von der Tafel ab, danach
rechnet Oskar die Aufgabe im Prüfungsstil in Notability vor (Klasse zeichnet ab und schreibt mit).
Hausaufgabe bis Mo 23.11.: Buch S. 16 Nr. 3 a und 4 a (linke Spalte), für Schnelle Nr. 4 b (links).

Das Flussdiagramm kommt aus der Excalidraw-Datei (Kurzfassung); die Teile werden über Gruppen und
Pfeilverbindungen erkannt, damit Änderungen in Obsidian erhalten bleiben. Folientechnik aus den Bausteinen
(Seitenleiste, Countdown-Uhr) in 04 Ressourcen/Lernwissenschaft & Pädagogik.
Ausführen: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 baue_praesentation_rezept.py
"""
import json
import re
import sys
import tempfile
from pathlib import Path

from baue_loesung_s15_s16 import ROT, C, S, k, i, Skizze, dreieck
from baue_rezept_trigo import (BLAU, EXCALIDRAW_KURZ, sk_a, sk_b, qa, al_a, be_a, b_a, ga_b, hb, a_b, b1, b2, b_b)
from baue_aufgabe_rezept import skizze as sk_aufgabe

HIER = Path(__file__).parent
VAULT = HIER.parents[2]
NAME = "Mathe 10b – Rezept Trigonometrie – Präsentation"
BAU = VAULT / "04 Ressourcen/Lernwissenschaft & Pädagogik"
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import svg_schreiben  # noqa: E402

TEILE = {"s0", "s1", "s2", "s3", "s4", "nein", "ja", "ff", "fertig", "zurueck", "p01", "p12", "pja", "pnein",
         "pja3", "pnein3", "p34", "p4f", "pfertig", "pzurueck"}


# ---------------------------------------------------------------- Flussdiagramm in Teile zerlegen
def teile_zuordnen(E):
    """Teil-Namen über Gruppen (s0 … s4, nein) und Pfeilverbindungen; schreibt customData.teil (nur im Speicher)."""
    teil = {}
    for e in E:
        for g in e.get("groupIds") or []:
            if g in ("s0", "s1", "s2", "s3", "s4", "nein"):
                teil[e["id"]] = g
    pfeile = [e for e in E if e["type"] == "arrow"]
    ende = lambda a, s: (a.get(s + "Binding") or {}).get("elementId")
    label = {e["containerId"]: e["text"].strip() for e in E if e["type"] == "text" and e.get("containerId")}
    for _ in range(3):
        for a in pfeile:
            ts, z = teil.get(ende(a, "start")), ende(a, "end")
            lab = label.get(a["id"], "")
            if z in teil or not z:
                continue
            if ts == "s2" and lab == "Ja":
                teil[z] = "ja"
            elif ts == "s4":
                teil[z] = "ff"
            elif ts == "ff":
                teil[z] = "fertig" if lab == "Ja" else "zurueck"
    namen = {("s0", "s1"): "p01", ("s1", "s2"): "p12", ("s2", "ja"): "pja", ("s2", "nein"): "pnein",
             ("ja", "s3"): "pja3", ("nein", "s3"): "pnein3", ("s3", "s4"): "p34", ("s4", "ff"): "p4f",
             ("ff", "fertig"): "pfertig", ("ff", "zurueck"): "pzurueck"}
    for a in pfeile:
        n = namen.get((teil.get(ende(a, "start")), teil.get(ende(a, "end"))))
        if n:
            teil[a["id"]] = n
    for e in E:
        if e["type"] == "text" and e.get("containerId") in teil:
            teil[e["id"]] = teil[e["containerId"]]
    fehlt = TEILE - set(teil.values())
    assert not fehlt, f"Im Excalidraw nicht gefunden: {fehlt}"
    for e in E:
        if e["id"] in teil:
            e["customData"] = {"teil": teil[e["id"]]}
    return E


def fluss_svg(nr):
    E = [e for e in json.loads(EXCALIDRAW_KURZ.read_text(encoding="utf-8"))["elements"] if not e.get("isDeleted")]
    teile_zuordnen(E)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "f.svg"
        svg_schreiben(E, p, gruppen=True)
        svg = p.read_text(encoding="utf-8")
    svg = re.sub(r'width="\d+" height="\d+"', 'class="fluss"', svg, count=1)
    return svg.replace('id="m"', f'id="m{nr}"').replace("url(#m)", f"url(#m{nr})")   # Pfeilspitze je Folie eigen


# ---------------------------------------------------------------- Beispiele
SUB = lambda t: f"<tspan font-size='2.2' dy='0.8'>{t}</tspan>"


def sk_b_ohne():
    """Beispiel (b) vor Schritt 2: nur das Gegebene, noch keine Höhe."""
    P = dreieck((0, 0), (9.0, 0), (b_b * C(50), b_b * S(50)))
    A, B, Cc = P["A"], P["B"], P["C"]
    s = Skizze(P, breite=66, hoehe=64)
    s.seite(A, B, "9,0 cm"); s.seite(B, Cc, "a", ROT, fett=True); s.seite(A, Cc, "b", ROT, fett=True)
    s.winkel(A, B, Cc, "50,0°", r=5, rt=10.5); s.winkel(B, A, Cc, "", r=5); bx, by = s.m(*B); s.text(bx + 1, by - 9, "70,0°", gr=2.8)
    for n in "ABC": s.ecke(n)
    return s.svg()


def br(z, n):
    return f'<span class="br"><span>{z}</span><span>{n}</span></span>'


def erg(t):
    return f'<b class="erg">{t}</b>'


def um(t):
    return f'<span class="um">| {t}</span>'


def z(nr, inhalt, zeige="", hl="", mit=""):
    """Eine Zeile im Beispiel = ein Klick. nr: Schritt aus dem Rezept oder '?' für die Fertig-Frage."""
    badge = f'<span class="nr">{nr}</span>' if nr != "?" else '<span class="nr frage">?</span>'
    a = f' data-zeige="{zeige}"' if zeige else ""
    a += f' data-hl="{hl}"' if hl else ""
    a += f' data-mit="{mit}"' if mit else ""
    return f'<div class="zl" data-step{a}>{badge}<div>{inhalt}</div></div>'


hb_, b1_, b2_ = i("h", "b"), i("b", "1"), i("b", "2")
NEIN_ZURUECK = "Alles berechnet? <b>Nein</b>: zurück zu 1"

ZEILEN_A = [
    z(0, "a = 5,0 cm; c = 9,0 cm; γ = 90° eintragen;<br>gesucht α, β, b rot", hl="s0", mit="skA"),
    z(1, "nur γ = 90° bekannt", hl="s1"),
    z(2, "rechtwinklig bei C: <b>Ja</b>", zeige="pja ja", hl="s2 ja"),
    z(3, f"α: sin α = {br('5,0', '9,0')}", zeige="pja3 s3", hl="s3"),
    z(4, f"sin α = {k(qa, 4)} {um('sin⁻¹')}<br>{erg(f'α = {k(al_a)}°')}", zeige="p34 s4", hl="s4"),
    z("?", NEIN_ZURUECK, zeige="p4f ff pzurueck zurueck", hl="ff zurueck"),
    "|",
    z(1, f"β = 180° − 90° − {k(al_a)}°<br>{erg(f'β = {k(be_a)}°')}", hl="s1"),
    z(3, f"b: cos {k(al_a)}° = {br('b', '9,0')} {um('⋅ 9,0')}", hl="s3"),
    z(4, f"b = 9,0 ⋅ cos {k(al_a)}°<br>{erg(f'b = {k(b_a)} cm')}", hl="s4"),
    z("?", f"Alles berechnet? <b>Ja</b>: fertig", zeige="pfertig fertig", hl="ff fertig"),
]
ZEILEN_B = [
    z(0, "c = 9,0 cm; α = 50,0°; β = 70,0° eintragen;<br>gesucht a und b rot", hl="s0", mit="skB0"),
    z(1, f"γ = 180° − 50,0° − 70,0°<br>{erg(f'γ = {k(ga_b)}°')}", hl="s1"),
    z(2, f"rechtwinklig? <b>Nein</b>: Höhe {hb_} von B<br>auf b, Fußpunkt F", zeige="pnein nein", hl="s2 nein", mit="skB1"),
    z(3, f"{hb_} im Dreieck ABF:<br>sin 50,0° = {br(hb_, '9,0')} {um('⋅ 9,0')}", zeige="pnein3", hl="s3"),
    z(4, f"{hb_} = 9,0 ⋅ sin 50,0°<br>{erg(f'{hb_} = {k(hb)} cm')}", hl="s4"),
    z("?", NEIN_ZURUECK, hl="ff zurueck"),
    "|",
    z(3, f"a im Dreieck FBC:<br>sin {k(ga_b)}° = {br(k(hb), 'a')} {um(f'a ↔ sin {k(ga_b)}°')}", hl="s3"),
    z(4, f"a = {br(k(hb), f'sin {k(ga_b)}°')} {erg(f'a = {k(a_b)} cm')}", hl="s4"),
    z("?", NEIN_ZURUECK, hl="ff zurueck"),
    z(3, f"{b1_}: cos 50,0° = {br(b1_, '9,0')} {um('⋅ 9,0')}", hl="s3"),
    z(4, f"{b1_} = 9,0 ⋅ cos 50,0° {erg(f'{b1_} = {k(b1)} cm')}", hl="s4"),
    z(3, f"{b2_}: cos {k(ga_b)}° = {br(b2_, k(a_b))} {um('⋅ ' + k(a_b))}", hl="s3"),
    z(4, f"{b2_} = {k(a_b)} ⋅ cos {k(ga_b)}° {erg(f'{b2_} = {k(b2)} cm')}", hl="s4"),
    z(4, f"b = {b1_} + {b2_} = {k(b1)} + {k(b2)}<br>{erg(f'b = {k(b_b)} cm')}", hl="s4"),
    z("?", "Alles berechnet? <b>Ja</b>: fertig", hl="ff fertig"),
]

ALLE = " ".join(sorted(TEILE))
BASIS_A = "s0 p01 s1 p12 s2"
BASIS_B = " ".join(sorted(TEILE - {"pnein", "nein", "pnein3"}))


def folie_beispiel(nr, tab, gruppe, titel, aufgabe, skizzen, zeilen, basis):
    sk = "".join(f'<div class="mit" data-name="{n}">{svg}</div>' for n, svg in skizzen)
    j = zeilen.index("|")
    sp = f'<div class="sp">{"".join(zeilen[:j])}</div><div class="sp">{"".join(zeilen[j + 1:])}</div>'
    return (f'<section class="slide rezept" data-tab="{tab}" data-group="{gruppe}" data-basis="{basis}">'
            f'<div class="links">{fluss_svg(nr)}</div>'
            f'<div class="rechts"><div class="kicker">{titel}</div>'
            f'<div class="kopf"><div class="aufg">{aufgabe}</div><div class="skizze">{sk}</div></div>'
            f'<div class="zeilen">{sp}</div></div></section>')


def folien():
    f = []
    # 1 Rezept: 0, 1, 2 gelten für alles
    f.append('<section class="slide rezept" data-tab="Rezept: 0, 1, 2" data-group="" data-basis="">'
             f'<div class="links">{fluss_svg(1)}</div>'
             '<div class="rechts titel"><div class="kicker">Mathe 10b; Trigonometrie</div>'
             '<h1>Rezept für Trigonometrie</h1><p class="unter">So gehst du bei jeder Aufgabe vor.</p>'
             '<span data-step data-zeige="s0" data-hl="s0"></span>'
             '<span data-step data-zeige="p01 s1" data-hl="s1"></span>'
             '<span data-step data-zeige="p12 s2" data-hl="s2"></span></div></section>')
    f.append(folie_beispiel(2, "Weg Ja: Beispiel (a)", "Zwei Wege", "Beispiel (a): rechtwinklig",
                            "Gegeben:<br>a = 5,0 cm; c = 9,0 cm<br>γ = 90°<br>Gesucht: α, β, b",
                            [("skA", sk_a())], ZEILEN_A, BASIS_A))
    f.append(folie_beispiel(3, "Weg Nein: Beispiel (b)", "Zwei Wege", "Beispiel (b): nicht rechtwinklig",
                            "Gegeben:<br>c = 9,0 cm<br>α = 50,0°; β = 70,0°<br>Gesucht: a, b",
                            [("skB0", sk_b_ohne()), ("skB1", sk_b())], ZEILEN_B, BASIS_B))
    f.append(f'<section class="slide rezept merk" data-tab="Ins Merkheft" data-group="Üben" data-basis="{ALLE}" data-timer="10">'
             f'<div class="links">{fluss_svg(4)}</div>'
             '<div class="rechts titel"><div class="kicker">Merkheft</div><h1>Abschreiben</h1>'
             '<p class="unter">Rezept mit Überschrift „Rezept für Trigonometrie“ ins Merkheft.<br>'
             'Kästen, Raute und Pfeile mit dem Lineal.</p></div></section>')
    f.append('<section class="slide aufgabe" data-tab="Aufgabe im Prüfungsstil" data-group="Üben">'
             '<div class="kicker">Gemeinsam in Notability: abzeichnen und mitschreiben</div>'
             '<div class="pa"><p>Im Dreieck ABC gilt:</p>'
             f'<div class="pa-reihe"><div class="werte">AC = 8,0 cm<br>α = 35,0°<br>ε = 130,0°</div><div class="pa-sk">{sk_aufgabe(False)}</div></div>'
             '<p><b>Berechnen Sie den Umfang des Dreiecks ABC.</b> <span class="klein">(Skizze nicht maßstabsgetreu)</span></p>'
             '<p class="klein">Für Schnelle: Berechnen Sie auch den Flächeninhalt.</p></div></section>')
    f.append('<section class="slide ha" data-tab="Hausaufgabe" data-group="Üben">'
             '<div class="kicker">Bis Montag, 23.11.</div><h1>Hausaufgabe</h1>'
             '<ul><li>Buch S. 16 Nr. 3 a (linke Spalte)</li><li>Buch S. 16 Nr. 4 a (linke Spalte)</li>'
             '<li class="klein2">Für Schnelle: S. 16 Nr. 4 b (linke Spalte)</li></ul>'
             '<p class="unter">Jede Aufgabe mit dem Rezept: Skizze, Winkel, rechtwinklig?, Gleichung, auflösen.</p></section>')
    return "".join(f)


# ---------------------------------------------------------------- Überblick
BLOECKE = [("Rezept zeigen: 0, 1, 2; Weg Ja; Weg Nein", 15, "#2563a8"), ("Ins Merkheft abschreiben", 10, "#047857"),
           ("Aufgabe im Prüfungsstil (Notability)", 17, "#b45309"), ("Hausaufgabe", 3, "#6b7280")]


def ueberblick():
    leiste = "".join(f'<div class="blk" style="flex:{m};background:{c}">{t}<span>{m} min</span></div>' for t, m, c in BLOECKE)
    zeilen, t0 = [], 0
    ablauf = [
        ("Rezept per Klick: erst 0, 1, 2 (gilt für alles). Dann Weg Ja mit Beispiel (a), dann Weg Nein mit Beispiel (b). "
         "Bei „Ja“ und „Nein“ zuerst die Klasse fragen, was wir dann machen, erst danach weiterklicken.", "Folien 1 bis 3"),
        ("Klasse schreibt das Rezept von der Tafel ins Merkheft ab (Uhr auf der Folie, 10 min).", "Folie 4; Kurzfassung als PDF"),
        ("Aufgabe im Prüfungsstil gemeinsam in Notability: Werte in die Skizze, dann Schritt für Schritt nach Rezept. "
         "Die Klasse zeichnet ab und schreibt mit.", "Folie 5; Aufgabe-PDF Seite 1 (Lösung Seite 2)"),
        ("Hausaufgabe bis Montag nennen.", "Folie 6"),
    ]
    for (t, m, _), (was, mat) in zip(BLOECKE, ablauf):
        zeilen.append(f"<tr><td>{t0}–{t0 + m}</td><td>{was}</td><td>{mat}</td></tr>")
        t0 += m
    return ('<div class="page"><h1>Mathe 10b, Fr 20.11.2026, 1. Stunde: Rezept für Trigonometrie</h1>'
            '<p class="sub">Erster Tag nach der Krankheit. Stand laut Vertretung: S. 16 Nr. 3 c und die Prüfungsaufgabe 2022 A2/1 '
            'gemeinsam gerechnet (Rest Hausaufgabe), allein war es noch zu schwierig.</p>'
            f'<div class="zeitleiste">{leiste}</div>'
            '<table class="abl"><tr><th>Min.</th><th>Was</th><th>Material</th></tr>' + "".join(zeilen) + "</table>"
            '<h2>Bei Zeitnot</h2><p>Beispiel (b) nur bis a rechnen (b<sub>1</sub>, b<sub>2</sub> weglassen) oder die Aufgabe im Prüfungsstil '
            'nur bis h<sub>c</sub> und den Rest als Hausaufgabe.</p>'
            '<h2>Hausaufgabe bis Mo 23.11.</h2><p>Schnittpunkt 10, S. 16 Nr. 3 a und Nr. 4 a (je linke Spalte); für Schnelle Nr. 4 b (linke Spalte). '
            'Gleicher Typ wie Beispiel (b): Höhe ist eingezeichnet, dann die Teildreiecke. '
            'Lösungen mit Schritten: <a href="Mathe 10b – Vertretung 18.11. – Dreieck mit stumpfem Winkel – Lösung mit Schritten.pdf">'
            'Lösung Vertretung 18.11.</a> (Nr. 3 a auf Seite 1, Nr. 4 a und b auf Seite 2).</p>'
            '<h2>Material</h2><ul>'
            '<li><a href="Mathe 10b – Rezept Trigonometrie – Kurzfassung zum Mitschreiben.pdf">Kurzfassung als PDF (Tafelbild)</a></li>'
            '<li><a href="Mathe 10b – Rezept Trigonometrie – Aufgabe im Prüfungsstil.pdf">Aufgabe im Prüfungsstil (Seite 1 Notability, Seite 2 Lösung)</a></li>'
            '<li><a href="Mathe 10b – Rezept Trigonometrie – Flussdiagramm mit zwei Beispielen.pdf">Lange Fassung mit beiden Beispielen</a></li>'
            '</ul></div>')


# ---------------------------------------------------------------- HTML
def baustein(ordner, datei):
    return (BAU / ordner / datei).read_text(encoding="utf-8")


CSS = """
:root{ --ink:#1c2230; --bg:#ffffff; --accent:#2563a8; --accent2:#2563a8; --muted:#6b7280; --line:#d9dee7; }
*{box-sizing:border-box; margin:0; padding:0}
html,body{min-height:100%}
body{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif; color:var(--ink); background:#e9edf3}
#tabs{display:flex; gap:8px; padding:12px 18px; background:#fff; border-bottom:1px solid var(--line); position:sticky; top:0; z-index:9}
#tabs button{font:inherit; font-size:15px; border:1px solid var(--line); background:#fff; padding:7px 16px; border-radius:20px; cursor:pointer}
#tabs button.on{background:var(--accent); border-color:var(--accent); color:#fff}
.panel{display:none} .panel.on{display:block}
.page{max-width:980px; margin:24px auto; background:#fff; padding:28px 34px; border-radius:12px; line-height:1.5}
.page h1{font-size:24px; margin-bottom:6px} .page h2{font-size:18px; margin:22px 0 6px} .page .sub{color:var(--muted)}
.page ul{margin-left:20px}
.zeitleiste{display:flex; gap:3px; margin:18px 0 10px; border-radius:8px; overflow:hidden}
.zeitleiste .blk{color:#fff; font-size:13px; padding:8px 10px; line-height:1.25}
.zeitleiste .blk span{display:block; font-weight:700}
.abl{border-collapse:collapse; width:100%; font-size:14.5px} .abl td,.abl th{border-bottom:1px solid var(--line); padding:7px 8px; text-align:left; vertical-align:top}
.abl td:first-child{white-space:nowrap; font-weight:700}
#p-folien{padding:14px}
#stage{container-type:size; position:relative; width:min(100%, calc((100vh - 130px) * 16 / 9)); aspect-ratio:16/9;
  background:var(--bg); border-radius:14px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.3); outline:none}
.slide{position:absolute; inset:0; padding:2cqw 3cqw; display:none}
.slide.active{display:flex}
[data-step]{opacity:0; transition:opacity .28s} [data-step].shown{opacity:1}
.kicker{font-size:1.15cqw; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); font-weight:700; margin-bottom:.8cqw}
#counter{position:absolute; bottom:1.2cqw; right:2cqw; font-size:1cqw; color:var(--muted)}
.ctrl{display:flex; gap:8px; align-items:center; font-size:13px; color:var(--muted)}
.ctrl button{font:inherit; padding:6px 12px; border:1px solid var(--line); border-radius:8px; background:#fff; cursor:pointer}
/* Rezept-Folien: links Flussdiagramm, rechts Beispiel */
.rezept{gap:2.5cqw; align-items:stretch}
.rezept .links{flex:0 0 auto; height:100%; display:flex; align-items:center}
.rezept svg.fluss{height:52cqw; width:auto; display:block}
.rezept .rechts{flex:1; min-width:0; display:flex; flex-direction:column}
.rechts.titel{justify-content:center}
.merk .links{order:2} .merk .rechts{padding-bottom:8cqw}
.rechts h1{font-size:4.2cqw; line-height:1.1; margin-bottom:1.2cqw}
.rechts .unter, .ha .unter{font-size:1.8cqw; color:var(--muted); line-height:1.4}
.aufg{font-size:1.55cqw; line-height:1.4}
.kopf{display:flex; gap:1.5cqw; align-items:flex-start; margin-bottom:1cqw}
.kopf .aufg{flex:1}
.skizze{position:relative; flex:0 0 30cqw; height:18cqw}
.skizze .mit{position:absolute; inset:0; background:#fff; opacity:0; transition:opacity .28s; display:flex; justify-content:center}
.skizze .mit.an{opacity:1}
.skizze svg{height:100%; width:auto}
.zeilen{flex:1; display:grid; grid-template-columns:1fr 1fr; gap:2cqw; min-height:0}
.zl{display:grid; grid-template-columns:2.6cqw 1fr; align-items:start; font-size:1.32cqw; line-height:1.45; margin-bottom:.55cqw}
.nr{display:inline-flex; width:2cqw; height:2cqw; border-radius:50%; background:var(--accent); color:#fff; font-weight:700;
    font-size:1.15cqw; align-items:center; justify-content:center}
.nr.frage{background:#b45309; border-radius:.3cqw; transform:rotate(45deg) scale(.82)} .nr.frage{font-size:0}
.nr.frage::after{content:"?"; font-size:1.3cqw; transform:rotate(-45deg)}
.erg{color:#c2185b} .um{color:#777; font-size:.88em; margin-left:.6cqw}
.br{display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; font-size:.9em; line-height:1.1; margin:0 .3cqw}
.br span:first-child{border-bottom:.12cqw solid #222; padding:0 .3cqw}
/* Teile des Flussdiagramms: verdeckt, aufgedeckt, gerade dran */
g[data-teil]{transition:opacity .35s}
g[data-teil].weg{opacity:0}
g[data-teil].hl{filter:drop-shadow(0 0 10px rgba(245,158,11,1)) drop-shadow(0 0 4px rgba(245,158,11,1))}
/* Aufgabe, Hausaufgabe */
.aufgabe, .ha{flex-direction:column; justify-content:center; padding:4cqw 7cqw}
.pa{font-size:2cqw; line-height:1.5}
.pa-reihe{display:flex; align-items:center; gap:4cqw; margin:1cqw 0}
.werte{font-size:2.4cqw; line-height:1.7}
.pa-sk svg{width:52cqw; height:auto}
.klein{font-size:1.4cqw; color:var(--muted)}
.ha h1{font-size:4.2cqw; margin-bottom:1.5cqw}
.ha ul{font-size:2.6cqw; line-height:1.7; margin:0 0 1.5cqw 3cqw} .ha .klein2{font-size:2cqw; color:var(--muted)}
"""

JS_KERN = """
  const tabBtns=[...document.querySelectorAll('#tabs button')];
  function tab(name){
    tabBtns.forEach(b=>b.classList.toggle('on', b.dataset.tab===name));
    document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on', p.id==='p-'+name));
    try{ history.replaceState(null,'','#'+name); }catch(e){}
    if(name==='folien') stage.focus();
  }
  tabBtns.forEach(b=>b.addEventListener('click',()=>tab(b.dataset.tab)));
  const stage=document.getElementById('stage');
  const slides=[...document.querySelectorAll('.slide')];
  const counter=document.getElementById('counter');
  let i=0, stepIdx=0;
"""

JS_REST = """
  const steps = n => [...slides[n].querySelectorAll('[data-step]')];
  /* Rezept: Teile des Flussdiagramms aufdecken und hervorheben, Skizzen im Beispiel wechseln */
  function rezeptSync(){
    const s=slides[i], svg=s.querySelector('svg.fluss');
    const sichtbar=new Set((s.dataset.basis||'').split(' ').filter(Boolean)), mit=new Set();
    let hl='';
    steps(i).forEach((el,k)=>{ if(k<stepIdx){
      (el.dataset.zeige||'').split(' ').filter(Boolean).forEach(t=>sichtbar.add(t));
      (el.dataset.mit||'').split(' ').filter(Boolean).forEach(t=>mit.add(t));
      if(el.dataset.hl) hl=el.dataset.hl; } });
    const hls=hl.split(' ');
    if(svg) svg.querySelectorAll('g[data-teil]').forEach(g=>{ g.classList.toggle('weg', !sichtbar.has(g.dataset.teil)); g.classList.toggle('hl', hls.includes(g.dataset.teil)); });
    s.querySelectorAll('.mit').forEach(el=>el.classList.toggle('an', mit.has(el.dataset.name)));
  }
  function applySteps(){
    steps(i).forEach((el,k)=>el.classList.toggle('shown', k < stepIdx));
    const n=steps(i).length;
    counter.textContent=(i+1)+' / '+slides.length+(n?'  –  '+stepIdx+'/'+n:'');
    rezeptSync();
  }
  function show(n, revealAll){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach((s,k)=>s.classList.toggle('active',k===i));
    stepIdx = revealAll ? steps(i).length : 0;
    applySteps(); updSide(); uSlide();
  }
  function next(){ if(stepIdx < steps(i).length){ stepIdx++; applySteps(); return; } show(i+1,false); }
  function prev(){ if(stepIdx > 0){ stepIdx--; applySteps(); return; } show(i-1,true); }
  function toggleFs(){ if(!document.fullscreenElement) present.requestFullscreen(); else document.exitFullscreen(); }
  document.addEventListener('keydown',e=>{
    if(!document.getElementById('p-folien').classList.contains('on')) return;
    const k=e.key;
    if(k.toLowerCase()==='u'){ uToggle(); e.preventDefault(); return; }
    if(k==='ArrowRight'||k===' '||k==='PageDown'){next();e.preventDefault();}
    else if(k==='ArrowLeft'||k==='PageUp'){prev();e.preventDefault();}
    else if(k==='ArrowDown'){tabStep(1);e.preventDefault();}
    else if(k==='ArrowUp'){tabStep(-1);e.preventDefault();}
    else if(k.toLowerCase()==='a'){show(i,true);e.preventDefault();}
    else if(k==='Home')show(0,false);
    else if(k==='End')show(slides.length-1,true);
    else if(k.toLowerCase()==='f'){ toggleFs(); }
    else if(k.toLowerCase()==='t'){ present.classList.toggle('nav-aus'); e.preventDefault(); }
  });
  stage.addEventListener('click',e=>{ const r=stage.getBoundingClientRect(); (e.clientX-r.left) < r.width/2 ? prev() : next(); });
  document.getElementById('prev').addEventListener('click',prev);
  document.getElementById('next').addEventListener('click',next);
  document.getElementById('fs').addEventListener('click',toggleFs);
  show(0,false);
  tab(location.hash==='#ueberblick'?'ueberblick':'folien');
"""


def baue():
    css = CSS + baustein("Baustein Seitenleiste", "seitenleiste-baustein.css") + baustein("Baustein Countdown-Uhr", "uhr-baustein.css")
    js = (JS_KERN + baustein("Baustein Seitenleiste", "seitenleiste-baustein.js")
          + baustein("Baustein Countdown-Uhr", "uhr-baustein.js")
          + "  function tabStep(d){ const ti=Math.max(0,Math.min(tabs.length-1,slides[i]._tab+d)); show(tabs[ti].idx[0],false); }\n"
          + JS_REST)
    if "function tabStep" in baustein("Baustein Seitenleiste", "seitenleiste-baustein.js"):
        js = js.replace("  function tabStep(d){ const ti=Math.max(0,Math.min(tabs.length-1,slides[i]._tab+d)); show(tabs[ti].idx[0],false); }\n", "", 1)
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{NAME}</title>'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><style>{css}</style></head><body>'
            '<div id="tabs"><button data-tab="ueberblick">Überblick</button><button data-tab="folien">Folien</button></div>'
            f'<div class="panel" id="p-ueberblick">{ueberblick()}</div>'
            '<div class="panel" id="p-folien"><div id="present"><nav id="side" aria-label="Abschnitte"></nav><div id="stagecol">'
            f'<div id="stage" tabindex="0">{folien()}<div id="dots"></div><div id="counter"></div></div>'
            '<div class="ctrl"><button id="prev">◀ zurück</button><button id="next">weiter ▶</button><button id="fs">Vollbild (F)</button>'
            '<span>Klick rechts oder → deckt den nächsten Schritt auf, ↑↓ Abschnitt, A zeigt alles, T Leiste, U Uhr</span></div>'
            '</div></div></div>'
            f'<script>{js}</script></body></html>')


if __name__ == "__main__":
    h = HIER / f"{NAME}.html"
    h.write_text(baue(), encoding="utf-8")
    print(h.name, f"{h.stat().st_size // 1024} KB")
