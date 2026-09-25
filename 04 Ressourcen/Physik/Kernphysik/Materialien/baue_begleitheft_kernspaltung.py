#!/usr/bin/env python3
"""Begleitheft „Kernspaltung und Kettenreaktion“ für W16 bis W18 (Entwurf).
Grundlage und Layout: Oskars Tutory-Arbeitsblatt „Kettenreaktion“ (Open Sans, blaue Fragen-Überschriften mit Linie,
Lücken als abgerundete Kästchen, Bilder in voller Breite, Karofelder, Kopfzeile Name/Titel/Datum, Fußzeile Physik/O.Klein/Seite).
Oskars eigene Zeichnungen liegen in assets/kettenreaktion/.
Aufruf: python3 baue_begleitheft_kernspaltung.py  -> Begleitheft Kernspaltung.html (5 Schülerseiten + 5 Lösungsseiten)"""
import base64, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
from kern_zeichnungen import Z, kern  # noqa: E402
from baue_blaetter_k10 import MAG, kreis, nk  # noqa: E402

B = "assets/kettenreaktion/"
TITEL = "Kernspaltung und Kettenreaktion"
BLAU = "#2F87C3"


def font(w):
    return base64.b64encode((HIER / "assets" / "fonts" / f"opensans-{w}.woff2").read_bytes()).decode()


CSS = ("<style>" + "".join(f"@font-face{{font-family:'Open Sans';font-weight:{w};src:url(data:font/woff2;base64,{font(w)}) format('woff2')}}" for w in (400, 600, 700)) + f"""
@page{{size:A4;margin:9mm 14mm 8mm 14mm}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:'Open Sans',Helvetica,Arial,sans-serif;font-size:10.5pt;color:#1d1d1b;line-height:1.45}}
.seite{{position:relative;height:274mm;page-break-after:always;overflow:hidden}}
.seite:last-child{{page-break-after:auto}}
section.abs{{break-inside:avoid;page-break-inside:avoid}}h2{{break-after:avoid}}
.kz{{display:grid;grid-template-columns:1fr 1fr 1fr;font-size:9pt;margin-bottom:5mm}}
.kz span:nth-child(2){{text-align:center}}.kz span:nth-child(3){{text-align:right;padding-right:22mm}}
.fz{{position:absolute;left:0;right:0;bottom:0;display:grid;grid-template-columns:1fr 1fr 1fr;font-size:9pt}}
.fz span:nth-child(2){{text-align:center}}.fz span:nth-child(3){{text-align:right}}
h2{{font-size:13.5pt;font-weight:400;color:{BLAU};border-bottom:.8pt solid #1d1d1b;margin:3.2mm 0 1.8mm;padding-bottom:.3mm;display:flex;justify-content:space-between;align-items:baseline}}
h2 .w{{font-size:8pt;color:#9aa3ae;font-weight:600}}h2 .lvl{{vertical-align:-2px;margin-right:1.5mm}}
.stunde{{font-size:8pt;font-weight:700;letter-spacing:.06em;color:#fff;background:#8DA6C2;display:inline-block;padding:.6mm 2.4mm;border-radius:2pt;margin-top:1mm}}
p{{margin:0 0 .8mm}}.lt{{line-height:2.25}}ul.pkt{{margin:0;padding-left:5mm;line-height:2.25}}ul.pkt li{{margin:0}}
.box{{display:inline-block;height:7.2mm;border:.9pt solid #1d1d1b;border-radius:5px;vertical-align:middle;margin:0 1.2mm;text-align:center;
     line-height:6.8mm;font-weight:600;color:{MAG};font-size:9.5pt;white-space:nowrap;overflow:hidden}}
.zeile{{display:flex;align-items:center;gap:2mm;margin:1.4mm 0}}.zeile b{{font-weight:400;min-width:5mm}}.zeile .box{{flex:1;margin:0;text-align:left;padding:1.2mm 2.5mm;height:auto;min-height:7.6mm;line-height:1.3;white-space:normal}}
.karo{{border:.8pt solid #555;background-color:#fff;background-image:linear-gradient(#8a8a8a .5pt,transparent .5pt),linear-gradient(90deg,#8a8a8a .5pt,transparent .5pt);
      background-size:5mm 5mm;background-position:-.25pt -.25pt;position:relative}}
.karo svg{{position:absolute;inset:0;width:100%;height:100%}}
.nk{{white-space:nowrap}}.nk .az{{display:inline-flex;flex-direction:column;font-size:.62em;line-height:1.05;text-align:right;vertical-align:.4em;margin-right:1px}}
.nk .s{{font-family:Georgia,serif;font-size:1.15em}}
.gl{{font-size:12.5pt}}.gl .box{{min-width:18mm}}
.bildzeile{{display:flex;gap:5mm;align-items:stretch;margin:1mm 0 2mm}}
ol.liste{{margin:0 0 1mm;padding-left:6mm}}.lsg{{color:{MAG};font-weight:600;font-size:10pt}}
.legende{{font-size:8.5pt;color:#555;text-align:right;margin:-3mm 0 0}}.legende .lvl{{vertical-align:-2px;margin:0 1mm 0 3mm}}
</style>""")


# ------------------------------------------------------------------ Bausteine
def L(antwort, l, breite=None):
    """Lücke als abgerundetes Kästchen, Breite nach Länge der Antwort (gleich in Schüler- und Lösungsfassung)."""
    import re
    rein = re.sub(r"<[^>]+>", "", antwort)
    w = max(breite or 0, 18, round(len(rein) * 2.0 + 6))
    return f'<span class="box" style="width:{w}mm">{antwort if l else ""}</span>'


def zeile(nr, antwort, l):
    marke = f"{nr}." if str(nr).isdigit() else f"{nr}:"
    return f'<div class="zeile"><b>{marke}</b><span class="box">{antwort if l else ""}</span></div>'


def h(nr, titel, stufe, stunde=""):
    return f'<h2><span>{nr} {titel}</span><span class="w">{kreis(stufe)}</span></h2>'


def img(datei, stil="width:100%"):
    return f'<img src="{B}{datei}" style="{stil};display:block" alt="">'


def seite(inhalt, nr, n, l):
    kz = (f'<div class="kz"><span>{"Lösung" if l else "Name:"}</span><span>{TITEL}</span><span>{"" if l else "Datum:"}</span></div>')
    fz = f'<div class="fz"><span>Physik</span><span>O.Klein</span><span>Seite {nr}/{n}</span></div>'
    return f'<div class="seite">{kz}{inhalt}{fz}</div>'


# ------------------------------------------------------------------ Lösungszeichnungen
def kette_bild(l):
    """Oskars Vier-Felder-Bild in voller Breite, in der Lösung mit Neutronen (Bildkoordinaten 1702 x 1300)."""
    o = ['<svg viewBox="0 0 1702 1190" style="position:absolute;inset:0;width:100%;height:100%">',
         '<rect x="10" y="420" width="40" height="80" fill="#FFFFFF"/>']
    if l:
        def n(x, y): o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="{MAG}"/>')

        def a(x1, y1, x2, y2):
            dx, dy = x2 - x1, y2 - y1
            d = (dx * dx + dy * dy) ** .5
            ux, uy = dx / d, dy / d
            o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2 - ux * 22:.0f}" y2="{y2 - uy * 22:.0f}" stroke="{MAG}" stroke-width="7" stroke-linecap="round"/>'
                     f'<polygon points="{x2},{y2} {x2 - ux * 34 - uy * 16:.0f},{y2 - uy * 34 + ux * 16:.0f} {x2 - ux * 34 + uy * 16:.0f},{y2 - uy * 34 - ux * 16:.0f}" fill="{MAG}"/>')
        n(35, 600); a(55, 600, 98, 600)
        for (x2, y2) in ((860, 440), (900, 800), (760, 930)):
            a(640, 620, x2, y2); n(x2 + 18, y2 + (-12 if y2 < 600 else 12))
        for y in (190, 590, 1050):
            n(1050, y); a(1068, y, 1080, y)
            for dy in (-70, 10, 90):
                y1 = y + (dy if y != 1050 else dy - 20)
                y2 = y + dy * 1.5 + (0 if y != 1050 else -20)
                a(1450, y1, 1560, y2); n(1580, y2)
    o.append("</svg>")
    return f'<div style="position:relative;margin:1mm 0 2mm">{img("kettenreaktion-felder.png")}{"".join(o)}</div>'


def kontrolliert_svg(l):
    z = Z("bh2", 170)
    if l:
        for i in range(4):
            x = 50 + i * 110
            kern(z, x, 80, 3, 4, r=5, seed=10 + i)
            if i < 3:
                z.pfeil(x + 15, 80, x + 93, 80, MAG, 2, 7)
            z.pfeil(x + 5, 92, x - 6, 124, "#A3B7D3", 1.4, 6)
            z.rect(x - 20, 128, 9, 26, "#3B4150", 1, 1)
        z.text(210, 34, "je Spaltung bleibt 1 Neutron wirksam", "middle", 11, 600, MAG)
        z.text(210, 166, "die übrigen schlucken Steuerstäbe", "middle", 10, 500, MAG)
    return z.svg(420)


def unkontrolliert_svg(l):
    z = Z("bh3", 170)
    if l:
        lv = [[(40, 85)]]
        for g in range(1, 4):
            lv.append([(40 + g * 115, y + d) for (_, y) in lv[-1] for d in (-38 / g, 38 / g)])
        for g in range(len(lv)):
            for (x, y) in lv[g]:
                kern(z, x, y, 2, 3, r=4, seed=20 + g)
                if g + 1 < len(lv):
                    for (x2, y2) in lv[g + 1]:
                        if abs(y2 - y) < 40 / (g + 1) + 1:
                            z.pfeil(x + 9, y, x2 - 9, y2, MAG, 1.5, 6)
        for g in range(4):
            z.text(40 + g * 115, 166, str(2 ** g), "middle", 11, 700, MAG)
    return z.svg(420)


EIG_KONTROLLIERT = ["Im Mittel löst genau ein Neutron pro Spaltung die nächste Spaltung aus.",
                    "Steuerstäbe fangen die überschüssigen Neutronen ein.",
                    "Die Energie wird gleichmäßig über lange Zeit frei und als Wärme genutzt.",
                    "Das Uran ist nur schwach angereichert (3 bis 5 % Uran-235).",
                    "Man findet sie im Kernkraftwerk."]
EIG_UNKONTROLLIERT = ["Jede Spaltung löst 2 bis 3 neue Spaltungen aus, die Zahl wächst lawinenartig.",
                      "In Bruchteilen einer Sekunde wird riesig viel Energie frei: eine Explosion.",
                      "Nötig ist fast reines Uran-235 (etwa 90 %) über der kritischen Masse.",
                      "Sie lässt sich nicht steuern oder stoppen.",
                      "Man findet sie in der Atombombe."]


def eigenschaften(liste, l):
    if not l:
        return ""
    return ('<ul style="margin:0;padding:2.5mm 3mm 0 7mm;font-size:9pt;line-height:1.35;color:' + MAG + ';font-weight:600;position:relative;background:rgba(255,255,255,.75)">'
            + "".join(f"<li>{e}</li>" for e in liste) + "</ul>")


def bild_mit_karo(bild, svg, h_mm=62):
    return (f'<div class="bildzeile"><div style="flex:0 0 42%;display:flex;align-items:center;justify-content:center">{img(bild, f"max-width:100%;max-height:{h_mm}mm;width:auto")}</div>'
            f'<div class="karo" style="flex:1;height:{h_mm}mm">{svg}</div></div>')


def energie_bild():
    """Gemini-Bild (2000 x 661) mit Beschriftung: jede Menge allein liefert so viel Wärme wie 1 kg Uran-235."""
    t = lambda x, y, s, size=40, w=700, anchor="middle": (f'<text x="{x}" y="{y}" font-family="Open Sans" font-size="{size}" font-weight="{w}" '
                                                          f'text-anchor="{anchor}" fill="#1d1d1b" paint-order="stroke" stroke="#fff" stroke-width="10">{s}</text>')
    o = ['<svg viewBox="0 0 2000 661" style="position:absolute;inset:0;width:100%;height:100%">',
         t(540, 640, "1 kg Uran-235"),
         t(705, 215, "ca. 2000 t Erdöl"), t(1085, 245, "ca. 3000 t Steinkohle"), t(1505, 140, "ca. 5500 t Holz"),
         t(900, 330, "oder", 46, 600), t(1275, 330, "oder", 46, 600), "</svg>"]
    return (f'<div style="position:relative;width:160mm;margin:1.5mm auto 0">{img("energiedichte.jpg")}{"".join(o)}</div>'
            '<p style="text-align:center;font-size:9.5pt;margin:0">Jede dieser Mengen liefert allein so viel Wärme wie 1&nbsp;kg Uran-235.</p>')


# ------------------------------------------------------------------ Seiten
def s1(l):
    return ('<span class="stunde">STUNDE 1 · DIE KERNSPALTUNG</span>'
            f'<div class="legende">Schwierigkeit:{kreis(0)}leicht{kreis(1)}mittel{kreis(2)}schwer</div>'
            + h(1, "Wie viel Energie steckt im Uran?", 0, "W16")
            + f'<img src="{B}warnzeichen.png" style="float:right;width:13mm;margin:-12mm 0 0 3mm" alt="">'
            + f'<p class="lt">Bei vollständiger Verbrennung bzw. Spaltung lassen sich aus 1 kg Steinkohle ca. {L("8", l, 14)} kWh, aus 1 kg Erdöl ca. {L("12", l, 14)} kWh '
              f'und aus 1 kg Uran-235 rund {L("23&#8239;000&#8239;000", l, 34)} kWh Wärme gewinnen. Für dieselbe Wärme wie 1 kg Uran-235 braucht man etwa {L("3000", l, 18)} Tonnen Kohle. '
              f'Uran hat eine viel größere {L("Energiedichte", l)} als alle anderen Brennstoffe.</p>'
            + energie_bild()
            + h(2, "Atome lassen sich spalten", 0, "W16")
            + '<ul class="pkt">'
              f'<li>1938 beschossen {L("Otto Hahn", l)} und Fritz Straßmann in Berlin Uran (92 Protonen) mit langsamen {L("Neutronen", l)}.</li>'
              f'<li>Sie wollten Elemente erschaffen, die {L("schwerer", l)} als Uran sind.</li>'
              f'<li>Sie fanden jedoch das viel leichtere Element {L("Barium", l)}.</li>'
              f'<li>Lise Meitner, die kurz zuvor aus Deutschland fliehen musste, lieferte die Erklärung: Der Urankern wurde {L("gespalten", l)}. '
              f'Gespalten wurde nur das Isotop {L("Uran-235", l)}.</li></ul>'
            + h(3, "Warum Uran-235 und nicht Uran-238?", 1, "W16")
            + f'<div style="float:right;width:28mm;margin:0 0 0 4mm;text-align:center">{img("uranerz.png")}<span style="font-size:8pt">Uranerz</span></div>'
            + f'<p class="lt">Uran-235 hat {L("143", l, 14)} Neutronen (Massenzahl 235 − {L("92", l, 14)} Protonen).<br>'
              f'Uran-238 hat {L("146", l, 14)} Neutronen (Massenzahl 238 − {L("92", l, 14)} Protonen).<br>'
              f'Beide sind {L("Isotope", l)} des Urans. Natururan besteht zu über 99 % aus {L("Uran-238", l)}, nur 0,7 % sind Uran-235. '
              f'Uran-235 wird schon von {L("langsamen", l)} Neutronen gespalten, Uran-238 praktisch nicht.</p>'
            + h(4, "Warum werden Neutronen zur Kernspaltung benutzt?", 0, "W16")
            + f'<ul class="pkt"><li>Neutronen haben {L("keine", l, 18)} Ladung.</li>'
              f'<li>Sie werden vom positiv geladenen Atomkern nicht {L("abgestoßen", l)} und von elektrischen Feldern nicht {L("abgelenkt", l)}.</li>'
              '<li>Sie werden wie kleine Torpedos auf den Atomkern geschossen.</li></ul>')


def s2(l):
    gl = (f'<p class="gl" style="margin:0;padding:3mm 3mm 0;color:{MAG};font-weight:600;position:relative">{nk("n", 1, 0)} + {nk("U", 235, 92)} → {nk("U", 236, 92)} → {nk("Ba", 141, 56)} + '
          f'{nk("Kr", 92, 36)} + 3 {nk("n", 1, 0)} + Energie</p>') if l else ""
    return (h(5, "Wie funktioniert eine Kettenreaktion?", 1, "W16")
            + '<p>Zeichne in die Felder 1, 3 und 4 die Neutronen mit Pfeilen ein.</p>'
            + kette_bild(l)
            + '<p style="font-size:13pt">Reaktionsgleichung:</p>' + f'<div class="karo" style="height:15mm">{gl}</div>'
            + f'<ul class="pkt" style="margin-top:2mm"><li>Bei jeder Kernspaltung entstehen {L("2 oder 3", l)} Neutronen mit sehr großer Geschwindigkeit (ca.&nbsp;20&#8239;000&nbsp;km/s).</li>'
              f'<li>Uran-235 wird vor allem von {L("langsamen", l)} Neutronen gespalten. Dabei entstehen dann wieder {L("2 oder 3", l)} Neutronen.</li>'
              f'<li>Bei jeder Spaltung wird eine große Menge {L("Energie", l)} frei.</li></ul>')


def s3(l):
    return ('<span class="stunde">STUNDE 2 · DIE KETTENREAKTION</span>'
            + h(6, "Versuch: Kettenreaktion mit Dominosteinen", 1, "W17")
            + '<ol class="liste"><li><b>Schritt 1:</b> Stellt die Steine in einer Reihe auf und stoßt den ersten an.</li>'
              '<li><b>Schritt 2:</b> Baut so um, dass jeder Stein zwei weitere umwirft. Stoßt nur einen Stein an.</li>'
              '<li><b>Schritt 3:</b> Nehmt aus dem Aufbau von Schritt 2 so viele Steine heraus, dass immer gleich viele Steine fallen.</li></ol>'
            + '<p>Welcher Schritt passt zu einem Kraftwerk, welcher zu einer Atombombe?</p>'
            + zeile("Kraftwerk", "Schritt 3: Es fallen immer gleich viele Steine, die Reaktion läuft gleichmäßig.", l)
            + zeile("Bombe", "Schritt 2: Die Zahl der fallenden Steine verdoppelt sich immer wieder.", l)
            + h(7, "Was ist eine kontrollierte Kettenreaktion?", 1, "W17")
            + '<p>Im Kernkraftwerk läuft eine kontrollierte Kettenreaktion ab. Notiere rechts mindestens drei Eigenschaften.</p>'
            + bild_mit_karo("kernkraftwerk.png", eigenschaften(EIG_KONTROLLIERT, l), 50)
            + h(8, "Was ist eine unkontrollierte Kettenreaktion?", 1, "W17")
            + '<p>In einer Atombombe läuft eine unkontrollierte Kettenreaktion ab. Notiere rechts mindestens drei Eigenschaften.</p>'
            + bild_mit_karo("atompilz.png", eigenschaften(EIG_UNKONTROLLIERT, l), 50))


def s4(l):
    teile = ["Uran-235", "Uran-238", "1. Spaltung", "Regelstab", "Brennelement", "1. Neutron", "Moderator (Wasser)"]
    return (h(9, "Was ist die kritische Masse?", 2, "W17")
            + f'<ul class="pkt"><li>Die Mindestmasse, ab der eine Kettenreaktion möglich ist, nennt man {L("kritische Masse", l)}. '
              'Bei Uran-235 in Kugelform sind das ca.&nbsp;50&nbsp;kg (Durchmesser ca.&nbsp;17&nbsp;cm).</li>'
              f'<li>Natururan enthält nur 0,7 % Uran-235. Deshalb wird es in Anreicherungsanlagen {L("angereichert", l)}.</li>'
              f'<li>Für ein Kraftwerk reichen 3 bis 5 % Uran-235, für eine Bombe braucht man etwa 90 %. Ein Kernkraftwerk kann deshalb {L("nicht", l, 16)} wie eine Atombombe explodieren.</li></ul>'
            + h(10, "Wie funktioniert die Kettenreaktion im Reaktor?", 0, "W17")
            + f'<p class="lt">Es wird kein reines Uran-235 verwendet, sondern {L("angereichertes Uran", l)}. Es befindet sich in etwa fingerdicken Metallröhren, den '
              f'{L("Brennstäben", l)}. Die Brennelemente sind in {L("Wasser", l)} getaucht. Regelstäbe (Steuerstäbe) aus {L("Bor", l, 16)} oder Cadmium können schnell zwischen die '
              f'Brennstäbe geschoben werden. Sie „{L("schlucken", l)}“ Neutronen und {L("regeln", l)} so die Kettenreaktion oder brechen sie ab.</p>'
            + '<span class="stunde">STUNDE 3 · DAS KERNKRAFTWERK</span>'
            + h(11, "Wie ist der Kernreaktor aufgebaut?", 0, "W18")
            + f'<div class="bildzeile"><div style="flex:0 0 38%">{img("reaktor.png")}</div><div style="flex:1">'
            + "".join(zeile(i + 1, t, l) for i, t in enumerate(teile)) + '</div></div>')


def s5(l):
    fus = (f'<p class="gl lt">{nk("H", 2, 1)} + {nk("H", 3, 1)} → {L(nk("He", 4, 2), l, 20)} + {L(nk("n", 1, 0), l, 20)} + Energie</p>')
    return (h(12, "Welche Aufgaben hat das Wasser?", 1, "W18")
            + '<p>Die Bilder zeigen schnelle Neutronen aus einer Spaltung, das Wasser und langsame Neutronen am nächsten Kern.</p>'
            + f'<div style="width:96mm;margin:1mm auto 1mm">{img("wasser-moderator.png")}</div>'
            + zeile(1, "Moderator: bremst die schnellen Neutronen ab, damit sie Uran-235 spalten können", l)
            + zeile(2, "Kühlmittel: transportiert die Wärme aus dem Reaktor zum Dampferzeuger", l)
            + zeile(3, "Abschirmung: hält einen Teil der Strahlung zurück", l)
            + h(13, "Vom Reaktor zum Strom", 1, "W18")
            + f'<p class="lt">Kernenergie → {L("Wärme", l, 26)} → {L("Bewegungsenergie", l)} → {L("elektrische Energie", l)}<br>'
              'Ab der Wärme arbeitet ein Kohlekraftwerk genauso.</p>'
            + h(14, "Ausblick: Kernfusion", 2, "W18")
            + '<p>In der Sonne verschmelzen leichte Kerne. Ergänze die Gleichung für die Fusion von Deuterium und Tritium.</p>'
            + '<div style="display:flex;gap:4mm;align-items:center"><div style="flex:1">' + fus
            + f'<p class="lt">1 kg Deuterium-Tritium liefert bei der Fusion etwa 94&nbsp;Millionen kWh. Das ist rund {L("4", l, 14)}-mal so viel wie 1&nbsp;kg Uran-235.</p></div>'
            + (f'<div style="flex:0 0 78mm">{img("fusion.png")}</div>' if (HIER / B / "fusion.png").exists() else "") + '</div>')


def heft(l):
    """Fließender Satz für den A3-Bogen: Kopfzeile nur auf Seite 1, keine Fußzeilen, kein Umbruch mitten im Abschnitt."""
    import re
    inhalt = re.sub(r'<span class="stunde">.*?</span>', "", "".join(fn(l) for fn in (s1, s2, s3, s4, s5)))
    teile = inhalt.split("<h2>")
    kopf = teile[0]
    abschnitte = "".join(f'<section class="abs">{kopf if i == 0 else ""}<h2>{t}</section>' for i, t in enumerate(teile[1:]))
    kz = f'<div class="kz"><span>{"Lösung" if l else "Name:"}</span><span>{TITEL}</span><span>{"" if l else "Datum:"}</span></div>'
    return f'<div class="heft">{kz}{abschnitte}</div>'


def abschnitt_folien():
    """Jeder Lösungsabschnitt auf eigener Seite -> PNG je Abschnitt (assets/heft-lsg-01.png ...), für die Stunden-HTMLs."""
    import re, subprocess, glob
    from PIL import Image, ImageChops
    inhalt = re.sub(r'<span class="stunde">.*?</span>', "", "".join(fn(True) for fn in (s1, s2, s3, s4, s5)))
    inhalt = re.sub(r'<div class="legende">.*?</div>', "", inhalt)
    teile = inhalt.split("<h2>")[1:]
    seiten = "".join(f'<section style="page-break-after:always"><h2>{t}</section>' for t in teile)
    tmp = HIER / "_abschnitte.html"
    tmp.write_text(f'<!doctype html><html lang="de"><head><meta charset="utf-8">{CSS}</head><body>{seiten}</body></html>', encoding="utf-8")
    pdf = HIER / "_abschnitte.pdf"
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "--virtual-time-budget=5000", f"file://{tmp}"], check=True, capture_output=True)
    for alt in glob.glob(str(HIER / "assets" / "heft-lsg-*.png")):
        Path(alt).unlink()
    subprocess.run(["pdftoppm", "-png", "-r", "130", str(pdf), str(HIER / "assets" / "heft-lsg")], check=True)
    for f in sorted(glob.glob(str(HIER / "assets" / "heft-lsg-*.png"))):
        im = Image.open(f).convert("RGB")
        box = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
        im.crop((max(0, box[0] - 20), max(0, box[1] - 20), min(im.width, box[2] + 20), min(im.height, box[3] + 20))).save(f)
    tmp.unlink(); pdf.unlink()
    print("Abschnittsbilder:", len(teile))


if __name__ == "__main__":
    html = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{TITEL}</title>{CSS}</head><body>'
            f'{heft(False)}<div style="page-break-before:always"></div>{heft(True)}</body></html>')
    (HIER / "Begleitheft Kernspaltung.html").write_text(html, encoding="utf-8")
    print("geschrieben: Begleitheft Kernspaltung.html")
    abschnitt_folien()
