#!/usr/bin/env python3
"""Stunden-HTML mit echten Tabs: Überblick | Folien | Arbeitsblätter | Ideen.
Folien = ausgefüllte Folien aus 'Optik I.html' (Seitenzahl = Seite in Optik I.pdf) PLUS neue Folien (Alltag/Buch) im gleichen Stil.
Folie = Tafelbild. Keine Zeiten. Neue Folien stehen nur hier, Optik I.html/.pdf bleiben unverändert bis zur Freigabe.
Aufruf: python3 baue_folien_am_stueck.py
"""
import re
from pathlib import Path

hier = Path(__file__).parent
quelle = (hier / "Optik I.html").read_text(encoding="utf-8")
folien = re.findall(r'<section class="folie[^"]*">.*?</section>', quelle, flags=re.S)
TITEL = "Optik · Do 24.09.2026"
INK, GR = "#111", "#66798E"


# ------------------------------------------------------------------ Icons für die neuen Folien
def sun(x, y, r=12):
    rays = "".join(f'<line x1="{x + (r + 3) * c:.1f}" y1="{y + (r + 3) * s:.1f}" x2="{x + (r + 9) * c:.1f}" y2="{y + (r + 9) * s:.1f}" stroke="#b98900" stroke-width="2"/>'
                   for c, s in [(1, 0), (.7, .7), (0, 1), (-.7, .7), (-1, 0), (-.7, -.7), (0, -1), (.7, -.7)])
    return f'{rays}<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd34d" stroke="#b98900" stroke-width="2"/>'


def star(x, y, r):
    import math
    pts = " ".join(f"{x + (r if i % 2 == 0 else r * .45) * math.sin(i * math.pi / 5):.1f},{y - (r if i % 2 == 0 else r * .45) * math.cos(i * math.pi / 5):.1f}" for i in range(10))
    return f'<polygon points="{pts}" fill="#ffd34d" stroke="#b98900"/>'


def bulb(x, y, fill="#fff2a8"):
    return (f'<circle cx="{x}" cy="{y}" r="13" fill="{fill}" stroke="#b98900" stroke-width="2"/>'
            f'<rect x="{x - 6}" y="{y + 12}" width="12" height="9" fill="#bbb" stroke="#777"/>')


def candle(x, y):
    return (f'<rect x="{x - 6}" y="{y - 4}" width="12" height="28" fill="#f5e6c8" stroke="#777"/>'
            f'<path d="M{x} {y - 22} q7 9 0 17 q-7 -8 0 -17z" fill="#ffb02e" stroke="#c76b00"/>')


def label(x, y, t, cls="klein"):
    fw = ' font-weight="600"' if cls == "" else ""
    return f'<text class="beschriftung {cls}" x="{x}" y="{y}"{fw}>{t}</text>'


def pfeil(x1, y1, x2, y2, col, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2.2"{d} marker-end="url(#p{col[1:]})"/>'


def marker(col):
    return (f'<marker id="p{col[1:]}" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">'
            f'<path d="M0,0 L8,4 L0,8 Z" fill="{col}"/></marker>')


def folie(titel, svg, merksatz):
    return (f'<section class="folie"><div class="titelband"><h1>{titel}</h1></div>'
            f'<div class="zeichenzone karo">{svg}</div><div class="merksatz">{merksatz}</div></section>')


# ---- Neu A: natürliche und künstliche Lichtquellen
import sys as _sys
_sys.path.insert(0, str(hier))
import folien_zeichnungen as _fz
A_svg = _fz.lichtquellen_arten()  # Labor-Stil B
A = folie("Natürliche und künstliche Lichtquellen", A_svg,
          "<b>Natürliche Lichtquellen</b> gibt es in der Natur. <b>Künstliche Lichtquellen</b> hat der Mensch gebaut.")

# ---- Neu B: Sehen und gesehen werden (Bild von Gemini, Pfeile und Beschriftung selbst gezeichnet)
def _pf(x1, y1, x2, y2, col, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="7" stroke-linecap="round"{d} '
            f'marker-end="url(#m{col[1:]})"/>')


def _mk(col):
    return (f'<marker id="m{col[1:]}" markerWidth="5" markerHeight="5" refX="3.2" refY="2.5" orient="auto">'
            f'<path d="M0,0 L5,2.5 L0,5 Z" fill="{col}"/></marker>')


def _lab(x, y, zeilen, lx, ly, w):
    h = 40 * len(zeilen) + 14
    t = "".join(f'<text x="{x + 14}" y="{y + 38 + 40 * i}" font-size="30" fill="#111" '
                f'font-family="Avenir Next, Helvetica, sans-serif">{z}</text>' for i, z in enumerate(zeilen))
    return (f'<line x1="{lx}" y1="{ly}" x2="{x + w / 2}" y2="{y + h if ly > y else y}" stroke="#333" stroke-width="2.5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="#333" stroke-width="2.5"/>{t}')


GELB, ROT, ORANGE = "#e0b400", "#d32f2f", "#ef7d00"
AUGE = (182, 338)
B_svg = (
    '<svg viewBox="0 60 1358 684" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">'
    f'<defs>{_mk(GELB)}{_mk(ROT)}{_mk(ORANGE)}</defs>'
    '<image href="assets/sehen-und-gesehen-werden.jpg" x="0" y="0" width="1358" height="744"/>'
    + _pf(606, 494, 1010, 446, GELB)
    + _pf(912, 563, AUGE[0] + 14, AUGE[1] + 8, ROT)
    + _pf(1016, 436, AUGE[0] + 16, AUGE[1] - 4, ORANGE, "22 16")
    + _lab(360, 110, ["Scheinwerfer:", "Lichtquelle"], 590, 482, 250)
    + _lab(20, 150, ["Auge des Fahrers", "(Empfänger)"], AUGE[0], AUGE[1] - 12, 270)
    + _lab(900, 110, ["Warnweste: beleuchtet,", "wirft Licht zurück"], 1055, 402, 350)
    + _lab(640, 612, ["Rücklicht: Lichtquelle"], 905, 575, 330)
    + '</svg>')
B = ('<section class="folie"><div class="titelband"><h1>Sehen und gesehen werden</h1></div>'
     f'<div class="bildzone">{B_svg}</div>'
     '<div class="merksatz tief">Das <b>Rücklicht</b> ist eine Lichtquelle. Die <b>Warnweste</b> ist ein beleuchteter Körper: '
     'Sie wirft das Scheinwerferlicht zurück ins Auge des Fahrers.</div></section>')

# ---- Neu D: Alltag zu Leitfrage 2
zeilen = [("schwarzes T-Shirt in der Sonne", "Absorption", "fast alles Licht wird verschluckt, das Shirt wird warm"),
          ("weiße Wand", "Streuung", "Licht geht in alle Richtungen, die Wand ist von überall zu sehen"),
          ("Fensterscheibe", "Transmission", "Licht geht (fast) ungehindert hindurch"),
          ("Milchglas (Badfenster)", "Transmission und Streuung", "hell, aber man erkennt nur Umrisse"),
          ("Sonnenbrille", "Absorption und Transmission", "ein Teil wird verschluckt, der Rest geht hindurch")]
D_tab = ('<table class="atab"><colgroup><col style="width:27%"><col style="width:29%"><col></colgroup><tr><th>im Alltag</th><th>was passiert</th><th>warum</th></tr>'
         + "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a, b, c in zeilen) + "</table>")
D = folie("Licht trifft auf einen Körper im Alltag", D_tab, "<b>Frage:</b> Wo passiert mehreres gleichzeitig?<br>"
          "<b style=\"color:#E6007E\">Antwort:</b> <span style=\"color:#E6007E\">Beim Milchglas (Transmission und Streuung) und bei der Sonnenbrille (Absorption und Transmission). Genau genommen fast überall: Auch die Fensterscheibe spiegelt ein wenig, und das schwarze T-Shirt streut einen kleinen Rest.</span>")


def basis(p):
    return re.sub(r'\s*<div class="ab-hinweis">.*?</div>', "", folien[p - 1], flags=re.S)


def ohne_merksatz(folie_html):
    return re.sub(r'\s*<div class="merksatz[^"]*">.*?</div>', "", folie_html, count=1, flags=re.S)


def austeilen(folie_html, text):
    i = folie_html.rindex("</section>")
    return folie_html[:i] + f'<div class="ab-hinweis">📄 {text}</div>' + folie_html[i:]


# ---- Neu V: Versuchsfolie Leitfrage 2 (ausgefüllt, im Stil von „Versuch: Kern- und Halbschatten“)
V_aufbau = (
    '<svg viewBox="0 0 300 142" xmlns="http://www.w3.org/2000/svg">'
    '<line x1="6" y1="118" x2="294" y2="118" stroke="#555" stroke-width="2"/>'
    '<rect x="14" y="80" width="62" height="34" fill="#8DA6C2" stroke="#66798E" stroke-width="1.5"/>'
    '<rect x="76" y="92" width="4" height="10" fill="#FFD34D" stroke="#B98900"/>'
    '<polygon points="80,93 196,90 196,104 80,101" fill="rgba(255,211,77,.45)"/>'
    '<rect x="196" y="52" width="9" height="66" fill="#fff" stroke="#333" stroke-width="1.5"/>'
    '<ellipse cx="195" cy="97" rx="4" ry="9" fill="#FFD34D" opacity=".8"/>'
    '<text class="beschriftung klein" x="16" y="72">Ray-Box</text>'
    '<text class="beschriftung klein" x="150" y="34">Blatt, Karton oder Glasscheibe</text>'
    '<text class="beschriftung klein" x="182" y="46">(nacheinander)</text>'
    '<text class="beschriftung klein" x="100" y="136">Lichtbündel</text>'
    '</svg>')
V = (
    '<section class="folie"><div class="titelband"><h1>Versuch: Licht trifft auf einen Körper</h1></div>'
    '<div class="versuch">'
    f'<div class="zelle"><h2>Aufbau</h2><div class="feld karo">{V_aufbau}</div></div>'
    '<div class="zelle"><h2>Beschreibung</h2><div class="feld"><ol>'
    '<li>Richte die Ray-Box auf ein weißes Blatt Papier.</li>'
    '<li>Richte die Ray-Box auf einen schwarzen Karton.</li>'
    '<li>Halte eine klare Glasscheibe in den Lichtweg.</li>'
    '<li>Beobachte jedes Mal, was mit dem Licht passiert.</li></ol></div></div>'
    '<div class="zelle"><h2>Beobachtung</h2><div class="feld">'
    'Weißes Blatt: heller, breiter Lichtfleck, von überall zu sehen. Schwarzer Karton: nur ein schwacher Lichtfleck. '
    'Glasscheibe: Das Licht geht fast ungehindert hindurch.</div></div>'
    '<div class="zelle"><h2>Ergebnis</h2><div class="feld">'
    'Das Blatt <b>streut</b> das Licht, der Karton <b>absorbiert</b> das meiste, die Glasscheibe <b>lässt es durch</b> (Transmission).'
    '</div></div></div></section>')

import subprocess
BLAETTER = {"lq": "Materialien/Lichtquellen W03.pdf", "w04": "Materialien/Licht trifft auf einen Koerper W04.pdf"}
for k, pdf in BLAETTER.items():   # Lösungsseite (Seite 2) als Bild, 1:1 wie das Schülerblatt
    subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", "2", "-l", "2", "-singlefile", str(hier / pdf),
                    str(hier / "Materialien" / "assets" / f"blatt-{k}-loesung")], check=True)


def blatt(k, hinweis):
    return ("blatt", f'<div class="austeil">📄 {hinweis}</div>'
            f'<img class="blattbild" src="Materialien/assets/blatt-{k}-loesung.png" alt="">')


FOLGE = [
    basis(11),
    blatt("lq", "Arbeitsblatt Lichtquellen austeilen"),
    A, B,
    basis(12), basis(13), basis(14),
    basis(15), basis(16),
    blatt("w04", "Versuchsblatt austeilen · Versuch in Gruppen"),
    ohne_merksatz(basis(18)), D,
    basis(19), basis(20), basis(21),
]
karten = "".join(
    (f'<div class="fnr">Folie {i} · Schülerblatt mit Lösung</div><div class="blattkarte" id="f{i}">{h[1]}</div>'
     if isinstance(h, tuple) else f'<div class="fnr">Folie {i}</div><div class="karte" id="f{i}">{h}</div>')
    for i, h in enumerate(FOLGE, 1))

SCHRITTE = [
    ("Lichtquellen", "Kurz wiederholen, Arbeitsblatt, dann natürlich und künstlich, sehen und gesehen werden.", [1, 2, 3, 4]),
    ("Check zu Leitfrage 1", "Antwort, Handzeichen, Lösung.", [5, 6, 7]),
    ("Leitfrage 2", "Dieselbe Lampe, drei Gegenstände. Vermutungen sammeln.", [8, 9]),
    ("Versuch", "Blatt, Karton, Glasscheibe in Gruppen, Versuchsblatt.", [10]),
    ("Erklären", "Vier Situationen zeichnen, Alltag mündlich, Antwort auf Leitfrage 2 ins Heft.", [11, 12, 13]),
    ("Check zu Leitfrage 2", "Handzeichen, Lösung.", [14, 15]),
]
zeit = "".join(f'<div class="z{i % 6}" style="flex:1">{i + 1} · {t}</div>' for i, (t, d, ks) in enumerate(SCHRITTE))
zeilen_u = "".join(
    f'<div class="schr"><span class="n">{i}</span><div><b>{t}</b><br><span class="m">{d}</span></div>'
    f'<div class="go">{"".join(f"<button data-go=f{k}>Folie {k}</button>" for k in ks)}</div></div>'
    for i, (t, d, ks) in enumerate(SCHRITTE, 1))


def chip(*nr):
    return "".join(f'<button class="fchip" data-go="f{n}">Folie {n}</button>' for n in nr)


hintergrund = f"""
<div class="box"><h3>Warum leuchtet etwas? {chip(1, 3)}</h3><ul>
<li><b>Heiße Körper glühen:</b> Sonne (Oberfläche etwa 5500 °C), Glühdraht (etwa 2500 °C), Kerzenflamme (bis etwa 1400 °C). Je heißer, desto heller und weißer.</li>
<li><b>Kalte Lichtquellen:</b> LED und Bildschirm erzeugen Licht elektrisch, ohne heiß zu werden. Das Glühwürmchen erzeugt Licht mit einer chemischen Reaktion im Körper (Biolumineszenz).</li>
<li><b>Mond:</b> Er wirft nur etwa ein Achtel des Sonnenlichts zurück. Er wirkt hell, weil der Nachthimmel dunkel ist.</li>
<li><b>Sterne und Planeten:</b> Sterne sind ferne Sonnen, also Lichtquellen. Planeten leuchten nicht selbst. Der „Abendstern“ ist die Venus, also ein beleuchteter Körper.</li>
<li><b>Typische Fehlvorstellungen:</b> Was hell ist, sei eine Lichtquelle (Mond, weiße Wand, Spiegel). Katzenaugen und Rückstrahler „leuchten“.</li></ul></div>

<div class="box"><h3>Sehen und gesehen werden {chip(4)}</h3><ul>
<li><b>Rückstrahler</b> werfen das Licht genau in die Richtung zurück, aus der es kommt. Deshalb sieht gerade der Autofahrer sie hell aufleuchten, ein Fußgänger daneben kaum.</li>
<li><b>Richtwerte bei Abblendlicht:</b> dunkle Kleidung ist erst auf etwa 25 m zu sehen, helle auf etwa 40 m, mit Reflektoren auf etwa 140 m. Die Zahlen werden von Verkehrssicherheitsverbänden genannt und schwanken je nach Quelle.</li>
<li>Guter Gesprächsanlass: Wer von euch hat Reflektoren an Jacke oder Ranzen?</li></ul></div>

<div class="box"><h3>Tipps zum Versuch {chip(10)}</h3><ul>
<li>Raum abdunkeln, sonst ist der Unterschied zwischen Blatt und Karton schwer zu sehen.</li>
<li>Ray-Box mit einem schmalen Spalt, flach auf den Tisch. Blatt und Karton senkrecht aufstellen.</li>
<li><b>Blatt:</b> Den Lichtfleck von links, rechts und von oben anschauen lassen. Er ist von überall zu sehen, das ist Streuung.</li>
<li><b>Karton:</b> Ganz dunkel wird der Fleck nicht. Auch schwarzer Karton streut einige Prozent des Lichts zurück, sonst könnte man ihn gar nicht sehen. Deshalb heißt es im Lückentext „größtenteils absorbiert“. Nach einer Minute die Hand auflegen lassen: Er wird warm, das absorbierte Licht ist nicht „weg“.</li>
<li><b>Glasscheibe:</b> Neben dem Lichtfleck dahinter ist auch ein schwaches Spiegelbild zu sehen. Das zeigt: Meist passiert mehreres gleichzeitig. Kanten der Scheibe abkleben.</li></ul></div>

<div class="box"><h3>Licht trifft auf einen Körper {chip(11, 12, 13)}</h3><ul>
<li><b>Streuung</b> ist eine ungeordnete Reflexion an einer rauen Oberfläche. Die regelmäßige Reflexion am Spiegel kommt später (Leitfrage 6).</li>
<li><b>Farben:</b> Ein roter Apfel absorbiert fast alle Farben des Lichts und streut vor allem Rot zurück. Weiß streut alle Farben, Schwarz absorbiert fast alle.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Licht „bleibt“ auf dem Gegenstand liegen. Schwarz werfe „schwarzes Licht“ zurück. Beim Glas „verschwindet“ das Licht.</li></ul></div>

<div class="box"><h3>Ideen aus Erlebnis Physik 7–9</h3>
<table class="t"><tr><th style="width:90px">Seite</th><th>Idee und so geht's</th><th style="width:130px">Passt zu</th></tr>
<tr><td>S. 26–29</td><td><b>Licht als Signal.</b> Ampel, leuchtendes Hundehalsband, Leuchtturm: Die Lichtquelle ist der Sender, das Auge der Empfänger.
Die Fernbedienung sendet unsichtbares Infrarotlicht, das man mit der Handykamera sichtbar machen kann.</td><td>Leitfrage 1</td></tr>
<tr><td>S. 45 A</td><td><b>Glatte und zerknitterte Alufolie.</b> Beide im dunklen Raum mit der Taschenlampe schräg anleuchten. Die glatte wirft einen hellen Fleck in eine Richtung
(Spiegelung), die zerknitterte leuchtet von überall schwach (Streuung). Material: Alufolie, Taschenlampe.</td><td>Leitfrage 2 (Zusatz), Leitfrage 6</td></tr>
<tr><td>S. 33 A</td><td><b>Teelicht durch einen Gummischlauch.</b> Durch den geraden Schlauch (etwa 15 cm) sieht man die Flamme, durch den gebogenen nicht. Licht breitet sich geradlinig aus.
Material: Teelicht, Feuerzeug, Gummischlauch.</td><td>Leitfrage 3</td></tr>
<tr><td>S. 33 B</td><td><b>Lichtwege sichtbar machen.</b> Kleine Löcher in Alufolie stechen, damit die Handylampe abdecken, Raum abdunkeln. Ein ausgepustetes Teelicht
gibt Rauch, in dem die geraden Lichtwege sichtbar werden. Material: Alufolie, Bleistift, Smartphone, Teelicht.</td><td>Leitfrage 3</td></tr>
<tr><td>S. 36–37</td><td><b>Schattenversuche.</b> Taschenlampe und Radiergummi auf gefaltetem Papier (Schattenbild, Je-desto-Satz). Zwei Taschenlampen auf einen Mitschüler an der Wand:
Wann gibt es zwei Schatten, wann nur einen? Der dritte Versuch entspricht deinem Ray-Box-Versuch.</td><td>Leitfrage 4</td></tr>
<tr><td>S. 40</td><td><b>Globus und Lampe.</b> Deutschland und Japan mit Knete markieren, den Globus drehen: Tag und Nacht. Eine Papierkugel am Faden kreist als Mond um den Globus: Mondphasen.</td><td>Leitfrage 5</td></tr>
<tr><td>S. 48–49</td><td><b>Lerncheck</b> mit 25 Aufgaben, gut als Aufgabenpool vor der Klassenarbeit.</td><td>Wiederholung</td></tr></table></div>
"""

import importlib.util as _iu
_spec = _iu.spec_from_file_location("stunde_vorlage", hier / "stunde_vorlage.py"); _sv = _iu.module_from_spec(_spec); _spec.loader.exec_module(_sv)
MATERIAL = {
    "demo": [],
    "schueler": [("Ray-Box mit Stromanschluss", "1×", "Versuch Folie 10"),
                 ("weißes Blatt Papier", "1×", ""),
                 ("schwarzer oder dunkler Karton", "1×", "dunkelblau, dunkelgrün oder Tonpapier gehen auch"),
                 ("klare Glasscheibe", "1×", "Kanten abkleben; Geodreieck geht auch")],
    "hinweis": "Raum abdunkeln.",
}
MATERIAL_HTML = _sv.material_tabellen(MATERIAL)

html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITEL}</title>
<link rel="stylesheet" href="folien.css">
<style>
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;color:#1b1b1b;background:#fff}}
.wrap{{max-width:1000px;margin:0 auto;padding:0 22px}}
header.kopf{{padding:30px 0 12px;border-bottom:2px solid #1b1b1b}}
h1{{font-size:27px;margin:0 0 4px;line-height:1.2}}.sub{{color:#555;margin:0}}
nav{{position:sticky;top:0;background:#fff;border-bottom:1px solid #d9d9d4;z-index:5}}
nav .wrap{{display:flex;gap:6px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}}
nav button{{border:0;padding:5px 13px;border-radius:16px;color:#1b1b1b;font:inherit;font-size:14px;background:#f1f1ed;cursor:pointer}}
nav button:hover{{background:#e3e3dc}}nav button.on{{background:#1b1b1b;color:#fff}}
.tab{{display:none;padding:26px 0 60px}}.tab.on{{display:block}}
h2{{font-size:22px;margin:0 0 10px}}
.box{{border:1px solid #d3d3cc;border-radius:9px;padding:8px 18px 12px;margin:14px 0}}.box h3{{margin:8px 0 6px;font-size:17px}}.box ul{{margin:6px 0;padding-left:20px}}.box li{{margin:5px 0}}
.zeitleiste{{display:flex;height:38px;border-radius:6px;overflow:hidden;margin:6px 0 14px;font-size:12.5px;border:1px solid #c9c9c2}}
.zeitleiste div{{display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.15;padding:0 4px}}
.z0{{background:#eeeeea}}.z1{{background:#e3eaf6}}.z2{{background:#d3dff2}}.z3{{background:#e3eaf6}}.z4{{background:#d3dff2}}.z5{{background:#eeeeea}}
.schr{{display:flex;align-items:center;gap:14px;padding:9px 0;border-bottom:1px solid #e6e6e0}}.schr:last-child{{border:0}}
.schr .n{{width:28px;height:28px;border-radius:50%;background:#1b1b1b;color:#fff;display:flex;align-items:center;justify-content:center;flex:none;font-weight:700;font-size:14px}}
.schr .m{{color:#555;font-size:15px}}.go{{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}}
.go button{{border:0;background:#e2ecf8;color:#1a56a0;border-radius:12px;padding:2px 10px;font-size:13px;cursor:pointer}}
.karte{{width:956px;max-width:100%;height:539px;margin:0 0 22px;border:1px solid #c8d0dc;scroll-margin-top:60px}}
.karte .folie{{page-break-after:auto}}
.atab{{position:absolute;left:10pt;right:10pt;top:6pt;border-collapse:collapse;font-size:10.5pt;line-height:1.25;background:rgba(255,255,255,.92);table-layout:fixed;width:calc(100% - 20pt)}}
.atab th,.atab td{{border-bottom:1px solid #d6dbe6;padding:3.5pt 7pt;text-align:left;vertical-align:top}}.atab th{{color:#66798e;font-size:10pt}}
a.btn{{display:inline-block;margin:4px 8px 4px 0;padding:5px 14px;border-radius:16px;background:#e2ecf8;color:#1a56a0;text-decoration:none;font-size:14.5px}}
table.t{{border-collapse:collapse;width:100%;font-size:15.5px}}.t td,.t th{{border:1px solid #d3d3cc;padding:7px 10px;text-align:left;vertical-align:top}}.t th{{background:#f5f5f1}}


.bildzone{{position:absolute;left:40.16pt;top:74pt;width:636.48pt;height:268pt}}.bildzone svg{{width:100%;height:100%;display:block}}
.fnr{{font-size:13px;color:#555;margin:0 0 4px;font-weight:600}}

.blattkarte{{width:620px;max-width:100%;margin:0 0 22px;scroll-margin-top:60px}}.blattbild{{display:block;width:100%;border:1px solid #c8d0dc}}
.austeil{{display:inline-block;background:#FF1F8A;color:#fff;font-size:13px;font-weight:600;padding:3px 10px;border-radius:4px;margin:0 0 6px}}
{_sv.MT_CSS}
.fchip{{border:0;background:#e2ecf8;color:#1a56a0;border-radius:12px;padding:1px 9px;font-size:12.5px;font-weight:600;cursor:pointer;margin-left:6px;vertical-align:2px}}
</style></head><body>
<div class="wrap"><header class="kopf"><h1>Optik: Lichtquellen und Licht trifft auf einen Körper</h1>
<p class="sub">Klasse 7c · Physik · Doppelstunde Do 24.09.2026</p></header></div>
<nav><div class="wrap tabs"><button data-t="ueb">Überblick</button><button data-t="folien">Folien</button><button data-t="hg">Hintergrund</button><button data-t="ab">Arbeitsblätter</button></div></nav>
<div class="wrap">
<div class="tab" id="t_ueb">
<div class="box"><h3>Drucken</h3><ul>
<li>Arbeitsblatt Lichtquellen: Seite 1, eins pro Schüler.</li>
<li>Versuchsblatt: Kopiervorlage „2 auf 1“, halbe Klassenstärke drucken und in der Mitte durchschneiden.</li>
<li>Folien und Lösungen: nicht drucken.</li></ul></div>
<div class="box"><h3>Material</h3>{MATERIAL_HTML}</div>
<div class="box"><h3>Die Stunde</h3><div class="zeitleiste">{zeit}</div>{zeilen_u}</div>
</div>

<div class="tab" id="t_folien">{karten}</div>

<div class="tab" id="t_hg">{hintergrund}</div>

<div class="tab" id="t_ab">
<div class="box"><h3>Arbeitsblatt Lichtquellen {chip(2)}</h3>
<a class="btn" href="Materialien/Lichtquellen W03.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Lichtquelle (L): Kerze, Glühlampe, Lagerfeuer, Blitz, Taschenlampe, Sonne. Beleuchtet (B): Mond, Tafel, Buch, Zimmerpflanze, Spielzeugauto.
Aufgabe 2: z. B. Glühwürmchen, Polarlicht, Sterne / Feuerwerk, Bildschirm, Laser. Aufgabe 3: Glühlampe und Taschenlampe.</p></div>
<div class="box"><h3>Versuchsblatt Licht trifft auf einen Körper {chip(10)}</h3>
<a class="btn" href="Materialien/Licht trifft auf einen Koerper W04.pdf">PDF öffnen</a><a class="btn" href="Materialien/Licht trifft auf einen Koerper W04 – 2 auf 1.pdf">Kopiervorlage 2 auf 1</a>
<p><b>Lösung:</b> Weißes Blatt: heller, breiter Lichtfleck, Licht wird in viele Richtungen zurückgeworfen (<b>gestreut</b>). Schwarzer Karton: nur ein schwacher Lichtfleck, das meiste Licht wird
<b>absorbiert</b>. Glasscheibe: Strahl dahinter fast unverändert, Licht wird <b>durchgelassen</b> (Transmission).</p></div>
<div class="box"><h3>Sehlabor und Körperlabor</h3>
<a class="btn" href="Sehlabor Lichtquellen.html">Sehlabor</a><a class="btn" href="Körperlabor Licht trifft auf Körper.html">Körperlabor</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Sehlabor: Sender und Empfänger, Lichtquellen zuordnen, Sehen und gesehen werden auf der Straße. Körperlabor: weitere Körper wie Butterbrotpapier oder Sonnenbrille, dazu die Aufteilung in Streuung, Absorption und Transmission. Beide sind auch für zu Hause geeignet.</p></div></div>
</div>
<script>
const tabs=[...document.querySelectorAll('nav button')],secs=[...document.querySelectorAll('.tab')];
function show(id){{tabs.forEach(b=>b.classList.toggle('on',b.dataset.t===id));secs.forEach(s=>s.classList.toggle('on',s.id==='t_'+id));history.replaceState(null,'','#'+id);requestAnimationFrame(()=>window.scrollTo(0,0))}}
tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));
document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{{show('folien');setTimeout(()=>document.getElementById(b.dataset.go).scrollIntoView(),60)}});
history.scrollRestoration='manual';
show(secs.some(s=>s.id==='t_'+location.hash.slice(1))?location.hash.slice(1):'ueb');
</script></body></html>"""

ziel = hier / "Optik – Do 24.09. – Stunde.html"
ziel.write_text(html, encoding="utf-8")
print("geschrieben:", ziel.name, f"({len(html) // 1024} KB), Folien:", len(FOLGE))
