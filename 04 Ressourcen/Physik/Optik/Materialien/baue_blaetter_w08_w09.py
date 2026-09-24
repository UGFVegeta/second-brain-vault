#!/usr/bin/env python3
"""Versuchsblätter W08 (Mondphasen im Modell) und W09 (Lochkamera), Aufbau wie W05/W06:
Versuchsbeschreibung + Skizze, Beobachtungsfeld, Lückentext, Lösungsseite in Magenta."""
import subprocess, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
from folien_zeichnungen import phase_pfad  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAG = "#E6007E"


def kopf(chip, titel, loesung=False):
    lm = '<div class="loesung-marker">Lösung</div>' if loesung else ""
    return f'<div class="kopf"><div><span class="chip">{chip}</span><h1>{titel}</h1></div>{lm}</div>'


def luecken(text, loesung):
    """[[wort]] wird zur Lücke (bzw. in der Lösung zum Lösungswort)."""
    import re
    return re.sub(r"\[\[(.+?)\]\]", (lambda m: f'<span class="luecke loesungstext">{m.group(1)}</span>') if loesung
                  else (lambda m: '<span class="luecke"></span>'), text)


def seite(inhalt):
    return f'<div class="seite">{inhalt}</div>'


def dokument(titel, seiten):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{titel}</title>'
            '<link rel="stylesheet" href="ab-vorlage.css"><style>'
            '</style></head><body>' + "".join(seiten) + '</body></html>')


def drucke(html_name, pdf_name):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HIER / pdf_name}",
                    "--virtual-time-budget=4000", f"file://{HIER / html_name}"], check=True, capture_output=True)
    print("gedruckt:", pdf_name)


# ============================================================ W08 Mondphasen im Modell
SKIZZE_W08 = '''<svg class="versuchsskizze" viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="18" cy="50" r="8" fill="#FFD34D" stroke="#B98900"/>
  <g stroke="#B98900" stroke-width="1.2"><line x1="30" y1="50" x2="40" y2="50"/><line x1="27" y1="40" x2="35" y2="34"/><line x1="27" y1="60" x2="35" y2="66"/></g>
  <circle cx="104" cy="50" r="11" fill="#E8ECF3" stroke="#66798E"/>
  <line x1="93" y1="50" x2="62" y2="50" stroke="#66798E" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="58" cy="50" r="6" fill="#FFFFFF" stroke="#66798E"/>
  <path d="M104 26 a24 24 0 0 0 -22 14" fill="none" stroke="#7C8592" stroke-width="1.2" marker-end="url(#pw8)"/>
  <defs><marker id="pw8" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#7C8592"/></marker></defs>
  <text x="6" y="74" font-size="8" fill="#66798E">Lampe</text><text x="8" y="84" font-size="8" fill="#66798E">(Sonne)</text>
  <text x="44" y="74" font-size="8" fill="#66798E">Kugel</text><text x="44" y="84" font-size="8" fill="#66798E">(Mond)</text>
  <text x="90" y="74" font-size="8" fill="#66798E">Kopf</text><text x="90" y="84" font-size="8" fill="#66798E">(Erde)</text>
  <text x="112" y="16" font-size="8" fill="#66798E">nach links</text><text x="112" y="25" font-size="8" fill="#66798E">drehen</text>
</svg>'''

STELLUNGEN = [("Du schaust zur Lampe.", 0.0, "Neumond"), ("Die Lampe ist rechts von dir.", 0.25, "zunehmender Halbmond"),
              ("Die Lampe ist hinter dir.", 0.5, "Vollmond"), ("Die Lampe ist links von dir.", 0.75, "abnehmender Halbmond")]


def kreis(f, loesung):
    if not loesung:
        return '<svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="26" fill="#FFFFFF" stroke="#14171c" stroke-width="1.2"/></svg>'
    hell = phase_pfad(30, 30, 26, f).replace('fill="#FFF6D8"', 'fill="#FFFFFF"')
    return (f'<svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="26" fill="#9AA3AF"/>{hell}'
            '<circle cx="30" cy="30" r="26" fill="none" stroke="#14171c" stroke-width="1.2"/></svg>')


def w08(loesung):
    phasen = "".join(
        f'<div class="phase"><div class="stellung">{st}</div>{kreis(f, loesung)}'
        f'<div class="name{" loesungstext" if loesung else ""}">{name if loesung else ""}</div></div>'
        for st, f, name in STELLUNGEN)
    lt = luecken("Die Lampe beleuchtet immer genau eine [[Hälfte]] der Kugel. Je nachdem, wo die Kugel steht, "
                 "siehst du von dieser hellen Hälfte [[unterschiedlich viel]]. Steht die Kugel genau hinter deinem Kopf "
                 "in seinem Schatten, wird sie dunkel. Das ist eine [[Mondfinsternis]].", loesung)
    return seite(
        kopf("W08", "F5 — Versuch: Mondphasen im Modell", loesung)
        + ("" if loesung else '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>')
        + '<div class="versuchskopf"><div><h2 class="aufgabe"><span class="nr">1</span>Versuchsbeschreibung</h2><ol class="liste">'
        '<li>Stecke die Styroporkugel auf einen Bleistift. Die Lampe vorne ist die Sonne, die Kugel der Mond, dein Kopf die Erde.</li>'
        '<li>Halte die Kugel mit ausgestrecktem Arm vor dein Gesicht, etwas höher als deinen Kopf.</li>'
        '<li>Drehe dich langsam nach links im Kreis. Die Kugel bleibt immer vor deinem Gesicht.</li>'
        '<li>Beobachte, wie viel von der beleuchteten Kugel du siehst.</li></ol></div>'
        + SKIZZE_W08.replace("pw8", "pw8l" if loesung else "pw8") + '</div>'
        + '<p class="frage"><b>Versuchsbeobachtung:</b> Male in jedem Kreis den dunklen Teil der Kugel aus und schreibe den Namen der Mondphase darunter.</p>'
        + f'<div class="phasen">{phasen}</div>'
        + '<h2 class="aufgabe"><span class="nr">2</span>Versuchserklärung</h2><p class="frage">Fülle die Lücken aus.</p>'
        + f'<p class="frage lt">{lt}</p>')


# ============================================================ W09 Lochkamera
SKIZZE_W09 = '''<svg class="versuchsskizze" viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="12" y="52" width="9" height="26" fill="#F0E2C0" stroke="#B9A87A"/>
  <path d="M16.5 52 q-6 -8 0 -17 q6 8 0 17z" fill="#FFD34D" stroke="#B98900"/>
  <rect x="64" y="30" width="86" height="44" fill="#EFEFEF" stroke="#555"/>
  <rect x="126" y="30" width="7" height="44" fill="#DCE9F2" stroke="#6E9BB8"/>
  <line x1="64" y1="51" x2="64" y2="53" stroke="#FFFFFF" stroke-width="2"/>
  <g stroke="#B98900" stroke-width="1"><line x1="16.5" y1="37" x2="129" y2="68"/><line x1="16.5" y1="77" x2="129" y2="36"/></g>
  <text x="56" y="24" font-size="8" fill="#66798E">Loch</text>
  <text x="96" y="90" font-size="8" fill="#66798E">Transparentpapier</text>
  <text x="4" y="92" font-size="8" fill="#66798E">Kerze</text>
</svg>'''


def w09(loesung):
    beob = ('<p class="beobachtungstext loesungstext">Das Bild steht auf dem Kopf. Je weiter das Papier vom Loch entfernt ist, '
            'desto größer wird das Bild. Ein kleineres Loch macht das Bild schärfer, aber dunkler.</p>') if loesung else ""
    lt = luecken("Weil sich Licht [[geradlinig]] ausbreitet, entsteht hinter dem Loch ein [[umgekehrtes]] Bild. "
                 "Je weiter das Transparentpapier vom Loch entfernt ist, desto [[größer]] wird das Bild. "
                 "Ein kleines Loch macht das Bild [[schärfer]], aber [[dunkler]].", loesung)
    return seite(
        kopf("W09", "Versuch: Beobachtungen mit der Lochkamera", loesung)
        + ("" if loesung else '<div class="namensfeld"><span>Name</span><span>Klasse</span><span class="kurz">Datum</span></div>')
        + '<div class="versuchskopf"><div><h2 class="aufgabe"><span class="nr">1</span>Versuchsbeschreibung</h2><ol class="liste">'
        '<li>Betrachte mit der Lochkamera hell erleuchtete Gegenstände (Fenster, Kerze).</li>'
        '<li>Verändere den Abstand zwischen Loch und Transparentpapier.</li>'
        '<li>Setze verschiedene Blenden an die Öffnung, also größere und kleinere Löcher.</li>'
        '<li>Beschreibe, wie sich Helligkeit, Schärfe und Größe des Bildes ändern.</li></ol></div>'
        + SKIZZE_W09 + '</div>'
        + '<p class="frage"><b>Versuchsbeobachtung:</b></p>'
        + f'<div class="zeichenfeld" style="height:40mm;">{beob}</div>'
        + '<h2 class="aufgabe"><span class="nr">2</span>Versuchserklärung</h2><p class="frage">Fülle die Lücken aus.</p>'
        + f'<p class="frage lt">{lt}</p>')


for html, pdf, titel, fn in (("mondphasen-modell.html", "Mondphasen im Modell W08.pdf", "Versuch Mondphasen im Modell – W08", w08),
                             ("lochkamera.html", "Lochkamera W09.pdf", "Versuch Lochkamera – W09", w09)):
    (HIER / html).write_text(dokument(titel, [fn(False), fn(True)]), encoding="utf-8")
    drucke(html, pdf)
