#!/usr/bin/env python3
"""Stunden-HTMLs Kernphysik Klasse 10, W01 bis W05 (je eine Einzelstunde). Gleicher Aufbau wie Klasse 7.
python3 baue_stunden_k10.py   -> HTMLs im Ordner Kernphysik (Export nach iCloud erst nach Freigabe)"""
import re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent / "Optik"))
from stunde_vorlage import folien_aus, blatt as _blatt, chip, tabellenfolie, bau_stunde  # noqa: E402

MAT = HIER / "Materialien"
_F = folien_aus(HIER / "Kernphysik.html")
_quelle = (HIER / "Kernphysik.html").read_text(encoding="utf-8")
KERN_CSS = _quelle[_quelle.index("<style>") + 7:_quelle.index("</style>")]


def f(p):
    return re.sub(r'\s*<div class="ab-hinweis">.*?</div>', "", _F[p - 1], flags=re.S)


def blatt(pdf, key, hinweis):
    return _blatt(pdf, key, hinweis, mat=MAT)


LAB = lambda datei, name, text: (f'<div class="box"><h3>{name}</h3><a class="btn" href="{datei}">Labor öffnen</a><p>{text}</p></div>')
ATOM = "Atomlabor Atombau und Isotope.html"
STRAHL = "Strahlungslabor Radioaktivitaet.html"

# ====================================================================== W01
A1 = tabellenfolie("Wie klein ist ein Atom?", [
    ("Haar", "etwa 0,1 mm dick", "Nebeneinander passen etwa eine Million Atome darauf."),
    ("Bakterie", "etwa 0,001 mm", "Im Lichtmikroskop gerade noch zu sehen."),
    ("Atom", "etwa 0,000 000 1 mm", "Kein Lichtmikroskop kann es zeigen."),
    ("Atomkern", "etwa 100 000-mal kleiner als das Atom", "Fast die ganze Masse steckt darin."),
], kopf=("Gegenstand", "Größe", "zum Vergleich"), frage="Wie viele Atome liegen nebeneinander auf der Dicke eines Haars?")
S1 = [f(2), f(3), A1, blatt("Wiederholung Atombau.pdf", "k01", "Arbeitsblatt austeilen: Vorwissen aus Chemie")]
S1_HG = f"""
<div class="box"><h3>Größenordnungen {chip(1, 3)}</h3><ul>
<li>Atomdurchmesser etwa 10⁻¹⁰ m, Kerndurchmesser etwa 10⁻¹⁵ bis 10⁻¹⁴ m. Das Verhältnis liegt bei 10 000 bis 100 000.</li>
<li>Fast die gesamte Masse steckt im Kern. Ein Proton ist rund 1800-mal so schwer wie ein Elektron.</li>
<li>Der Nachweis kam mit Rutherfords Streuversuch (1909 bis 1911): Fast alle α-Teilchen fliegen durch eine Goldfolie, nur sehr wenige prallen zurück. Im Atomlabor als Simulation.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Atom ist eine volle Kugel. Elektronen kreisen auf festen Bahnen wie Planeten. Atome kann man mit dem Mikroskop sehen.</li></ul></div>
<div class="box"><h3>Vorwissen aus Chemie {chip(4)}</h3><ul>
<li>Das Arbeitsblatt holt das Schalenmodell und das Periodensystem aus Klasse 8 und 9 zurück. Lücken zeigen, was in der nächsten Stunde noch einmal kommen muss.</li></ul></div>
{LAB(ATOM, "Atomlabor", "Zoom vom Atom auf den Kern, Rutherfords Streuversuch mit Teilchenzahl-Regler, Atom bauen, Isotope.")}"""
S1_AB = f"""<div class="box"><h3>Arbeitsblatt Wiederholung Atombau {chip(4)}</h3><a class="btn" href="Materialien/Wiederholung Atombau.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Seite 2 des PDFs.</p></div>"""

# ====================================================================== W02
A2 = tabellenfolie("Isotope im Alltag", [
    ("Kohlenstoff-14", "Altersbestimmung von Funden", "Sein Anteil in toten Lebewesen nimmt mit der Zeit ab."),
    ("Deuterium (H-2)", "schweres Wasser", "Chemisch Wasser, aber etwas schwerer."),
    ("Iod-131", "Untersuchung der Schilddrüse", "Die Schilddrüse sammelt Iod, das Isotop macht sie sichtbar."),
    ("Uran-235", "Brennstoff im Kernkraftwerk", "Nur dieses Isotop lässt sich im Reaktor gut spalten."),
], frage="Warum verhalten sich Kohlenstoff-12 und Kohlenstoff-14 chemisch gleich?")
S2 = [f(5), f(7), blatt("Nuklide und Isotope W02.pdf", "k02", "Arbeitsblatt austeilen · mit Periodensystem"), A2]
S2_HG = f"""
<div class="box"><h3>Nuklidschreibweise {chip(1)}</h3><ul>
<li>A oben links (Massenzahl), Z unten links (Kernladungszahl). Die Neutronenzahl ist N = A − Z.</li>
<li>Die Chemie hängt nur von den Elektronen ab, also von Z. Deshalb verhalten sich Isotope chemisch gleich.</li>
<li>Die Masse im Periodensystem ist ein Mittelwert über die natürlichen Isotope. Deshalb ist sie keine ganze Zahl.</li>
<li><b>Typische Fehlvorstellungen:</b> A und Z werden vertauscht. Isotope sind verschiedene Elemente. Isotope sind immer radioaktiv.</li></ul></div>
{LAB(ATOM, "Atomlabor", "Atom bauen: Protonen, Neutronen und Elektronen einstellen, das Nuklid erscheint mit Stabilität. Isotope von Wasserstoff, Kohlenstoff und Uran.")}"""
S2_AB = f"""<div class="box"><h3>Arbeitsblatt Nuklide und Isotope {chip(3)}</h3><a class="btn" href="Materialien/Nuklide und Isotope W02.pdf">PDF öffnen</a>
<p><b>Lösung:</b> H 1/0/1, He 2/2/2, C-12 6/6/6, C-14 6/8/6, O 8/8/8, U-235 92/143/92, U-238 92/146/92. Isotope: C-12 und C-14, U-235 und U-238. C-13, O-18, K-40.</p></div>"""

# ====================================================================== W03
A3 = tabellenfolie("Natürliche Strahlung im Alltag", [
    ("Keller", "Radon aus dem Boden", "Ein radioaktives Gas, das sich in Kellerräumen sammeln kann."),
    ("Flugzeug", "mehr kosmische Strahlung", "In großer Höhe schirmt weniger Luft ab."),
    ("unser Körper", "Kalium-40", "Ein kleiner Teil des Kaliums in Muskeln und Nahrung ist radioaktiv."),
    ("Granit", "etwas höhere Zählrate", "Das Gestein enthält Spuren von Uran und Thorium."),
], frage="Warum misst das Zählrohr im Physikraum auch ohne Präparat Impulse?")
S3 = [f(8), f(9), f(10), f(11), f(12), blatt("Zaehlrohr und Nullrate W03.pdf", "k03", "Arbeitsblatt austeilen · Nullrate vorne messen"), A3]
S3_HG = f"""
<div class="box"><h3>Das Zählrohr {chip(4, 6)}</h3><ul>
<li>Geiger-Müller-Zählrohr: Metallrohr mit Gas und einem Draht in der Mitte, vorne ein dünnes Fenster. Strahlung ionisiert das Gas, es gibt einen kurzen Stromstoß (Impuls).</li>
<li>Das Zählrohr zählt Impulse. Es unterscheidet nicht zwischen α, β und γ und erfasst nur einen Teil der Strahlung.</li>
<li><b>Nullrate:</b> Je nach Zählrohr und Ort etwa 10 bis 40 Impulse pro Minute. Sie schwankt zufällig, deshalb mehrere Minuten messen und mitteln.</li>
<li><b>Typische Fehlvorstellungen:</b> Strahlung gibt es nur in der Nähe von Kernkraftwerken. Das Zählrohr misst „die Radioaktivität“ eines Stoffes direkt.</li></ul></div>
<div class="box"><h3>Tipps zum Versuch {chip(6)}</h3><ul>
<li>Lautsprecher an, damit die Klasse das Knacken hört. Fünfmal eine Minute messen, Werte an der Tafel sammeln.</li>
<li>Die Streuung der Werte ist gewollt: Radioaktiver Zerfall ist Zufall. Das bereitet Leitfrage 2 vor.</li></ul></div>
{LAB(STRAHL, "Strahlungslabor", "Nullrate mit zehn zufälligen Messungen und Mittelwert, falls das Zählrohr fehlt oder zum Nachschauen zu Hause.")}"""
S3_AB = f"""<div class="box"><h3>Arbeitsblatt Zählrohr und Nullrate {chip(6)}</h3><a class="btn" href="Materialien/Zaehlrohr und Nullrate W03.pdf">PDF öffnen</a>
<p><b>Lösung:</b> 1 dünne Folie, 2 Gas, 3 Metalldraht, 4 Metallrohr. Lücken: Zählrohr, Impulse, zählt, Knacken, Impulsrate, höher, stärker. Beispielmessung 22, 27, 19, 25, 24, Mittelwert 23,4. Nullrate, menschlichen Körpers, terrestrische, kosmische.</p></div>"""

# ====================================================================== W04
A4 = tabellenfolie("Strahler im Alltag", [
    ("Rauchmelder (ältere Modelle)", "α-Strahler Americium-241", "Die Strahlung macht Luft leitend. Rauch stört das und löst Alarm aus."),
    ("Banane", "β-Strahler Kalium-40", "Winzige Menge, nicht gefährlich."),
    ("Medizin", "γ-Strahler Technetium-99m", "Zeigt im Körper, wo sich ein Stoff anreichert."),
    ("Keller", "α-Strahler Radon", "Gefährlich, wenn man es einatmet."),
], frage="Warum ist Radon gefährlich, obwohl α-Strahlung schon von Papier gestoppt wird?")
S4 = [f(14), f(16), blatt("Drei Strahlungsarten W04.pdf", "k04", "Arbeitsblatt austeilen"), A4]
S4_HG = f"""
<div class="box"><h3>Radioaktivität {chip(1)}</h3><ul>
<li>Instabile Kerne haben zu viele oder zu wenige Neutronen im Verhältnis zu den Protonen. Alle Elemente mit mehr als 83 Protonen sind radioaktiv.</li>
<li>Der Zeitpunkt des Zerfalls eines einzelnen Kerns ist zufällig. Für viele Kerne gilt eine feste Halbwertszeit (Leitfrage 3).</li></ul></div>
<div class="box"><h3>α, β und γ {chip(2)}</h3><ul>
<li><b>α:</b> Heliumkern, zweifach positiv, groß und langsam, gibt seine Energie auf kurzer Strecke ab. Außen harmlos, innen (eingeatmet, verschluckt) sehr schädlich.</li>
<li><b>β⁻:</b> schnelles Elektron aus dem Kern. Im Kern wird ein Neutron zum Proton. Es gibt auch β⁺ (Positron), das ist nicht verlangt.</li>
<li><b>γ:</b> energiereiche elektromagnetische Strahlung, folgt oft auf α- oder β-Zerfall, wenn der Tochterkern noch angeregt ist.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Elektron beim β-Zerfall kommt aus der Hülle. Bestrahlte Gegenstände werden selbst radioaktiv.</li></ul></div>
<div class="box"><h3>Strahlenschutz im Unterricht</h3><ul>
<li>Präparate nur durch die Lehrkraft und nach den Vorgaben der Richtlinie zur Sicherheit im Unterricht (RiSU). Fehlt ein Präparatesatz, zeigt das Strahlungslabor die Zerfälle.</li></ul></div>
{LAB(STRAHL, "Strahlungslabor", "Präparat und Abstand, α-, β- und γ-Zerfall mit Nuklidgleichung.")}"""
S4_AB = f"""<div class="box"><h3>Arbeitsblatt Drei Arten radioaktiver Strahlung {chip(3)}</h3><a class="btn" href="Materialien/Drei Strahlungsarten W04.pdf">PDF öffnen</a>
<p><b>Lösung:</b> α: Heliumkern, positiv, A − 4, Z − 2. β⁻: Elektron, negativ, A bleibt, Z + 1. γ: Energie, keine Ladung, A und Z bleiben. Lücken: 2 Protonen, 2 Neutronen, Neutron, Proton, Energie. Zuordnung: α, β⁻, γ.</p></div>"""

# ====================================================================== W05
A5 = tabellenfolie("Abschirmung im Alltag", [
    ("Bleischürze beim Röntgen", "schützt die übrigen Körperteile", "Blei schwächt energiereiche Strahlung stark."),
    ("Rauchmelder", "darf man anfassen", "Die α-Strahlung kommt nicht einmal durch das Gehäuse."),
    ("Behälter für radioaktive Stoffe", "dicke Wände aus Stahl oder Blei", "γ-Strahlung wird nur geschwächt, nie ganz gestoppt."),
], frage="Welche Strahlung ist außerhalb des Körpers am gefährlichsten, welche innerhalb?")
S5 = [f(18), f(20), blatt("Durchdringung und Zerfallsgleichungen W05.pdf", "k05", "Arbeitsblatt austeilen · Absorberversuch vorne"), A5]
S5_HG = f"""
<div class="box"><h3>Zerfallsgleichungen {chip(1)}</h3><ul>
<li>Oben (Massenzahl) und unten (Ladung) muss die Summe links und rechts gleich sein. Das Elektron schreibt man mit 0 oben und −1 unten.</li>
<li>Das neue Element liest man über die Kernladungszahl im Periodensystem ab. Deshalb liegt das Periodensystem immer auf dem Tisch.</li></ul></div>
<div class="box"><h3>Durchdringung {chip(2)}</h3><ul>
<li>α: wenige Zentimeter Luft, ein Blatt Papier. β: einige Meter Luft, einige Millimeter Aluminium. γ: wird exponentiell geschwächt, nie ganz auf null. Blei halbiert je nach Energie etwa pro Zentimeter.</li>
<li>Bei α-Präparaten kann hinter Papier noch etwas γ-Strahlung gemessen werden, wenn das Präparat zusätzlich γ aussendet (z. B. Americium-241).</li>
<li><b>Typische Fehlvorstellung:</b> Durchdringende Strahlung ist immer gefährlicher. Für den Körper hängt es davon ab, ob die Quelle außen oder innen ist.</li></ul></div>
{LAB(STRAHL, "Strahlungslabor", "Zerfallsgleichungen üben mit sofortiger Rückmeldung, Absorberversuch mit Papier, Aluminium und Blei.")}"""
S5_AB = f"""<div class="box"><h3>Arbeitsblatt Durchdringung und Zerfallsgleichungen {chip(3)}</h3><a class="btn" href="Materialien/Durchdringung und Zerfallsgleichungen W05.pdf">PDF öffnen</a>
<p><b>Lösung:</b> α hinter Papier fast Nullrate, β hinter Aluminium fast Nullrate, γ hinter Blei kleiner, aber über der Nullrate. Lücken: Papier, Aluminium, Blei.
Po-210 → Pb-206 + He-4, K-40 → Ca-40 + e, Ra-226 → Rn-222 + He-4.</p></div>"""

MAT_LEER = {"demo": [], "schueler": [], "hinweis": ""}
STUNDEN = [
    ("Kernphysik – W01 Woraus besteht Materie – Stunde.html", "Kernphysik: Woraus besteht Materie?", "Klasse 10 · Physik · W01 (Woche ab 14.09.2026) · Einstieg Leitfrage 1",
     ["Arbeitsblatt Wiederholung Atombau: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [], "schueler": [("Periodensystem", "1×", "aus dem Chemiebuch oder als Kopie")], "hinweis": ""},
     [("Einstieg", "Stadion und Erbse, Leitfrage 1, Vermutungen.", [1, 2]), ("Größen", "Wie klein ist ein Atom? Zoom im Atomlabor.", [3]), ("Vorwissen", "Arbeitsblatt Wiederholung Atombau.", [4])],
     S1, S1_HG, S1_AB),
    ("Kernphysik – W02 Atombau und Isotope – Stunde.html", "Kernphysik: Atombau und Isotope", "Klasse 10 · Physik · W02 (Woche ab 21.09.2026) · Leitfrage 1",
     ["Arbeitsblatt Nuklide und Isotope: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [], "schueler": [("Periodensystem", "1×", "")], "hinweis": ""},
     [("Aufbau", "Kern und Hülle, Nuklidschreibweise.", [1]), ("Isotope", "Wasserstoff, Deuterium, Tritium.", [2]), ("Üben", "Arbeitsblatt, Alltag mündlich.", [3, 4])],
     S2, S2_HG, S2_AB),
    ("Kernphysik – W03 Zaehlrohr und Nullrate – Stunde.html", "Kernphysik: Das Zählrohr klickt von allein", "Klasse 10 · Physik · W03 (Woche ab 28.09.2026) · Abschluss Leitfrage 1, Einstieg Leitfrage 2",
     ["Arbeitsblatt Zählrohr und Nullrate: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [("Geiger-Müller-Zählrohr mit Zählgerät", "1×", "Lautsprecher an"), ("Stoppuhr", "1×", "fünfmal eine Minute")], "schueler": [],
      "hinweis": "Kein Präparat nötig. Das Zählrohr ist vor der Stunde eingeschaltet und steht weit weg von der Präparatesammlung."},
     [("Abschluss Leitfrage 1", "Antwort ins Heft, Check.", [1, 2, 3]), ("Einstieg Leitfrage 2", "Zählrohr klickt, Leitfrage 2.", [4, 5]), ("Versuch", "Nullrate messen, Arbeitsblatt.", [6]), ("Alltag", "Natürliche Strahlung.", [7])],
     S3, S3_HG, S3_AB),
    ("Kernphysik – W04 Alpha Beta Gamma – Stunde.html", "Kernphysik: Alpha, Beta und Gamma", "Klasse 10 · Physik · W04 (Woche ab 05.10.2026) · Leitfrage 2",
     ["Arbeitsblatt Drei Arten radioaktiver Strahlung: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [("Präparatesatz", "1", "nur Lehrkraft, nach RiSU"), ("Geiger-Müller-Zählrohr mit Zählgerät", "1×", "")], "schueler": [("Periodensystem", "1×", "")],
      "hinweis": "Ohne Präparatesatz: Zerfälle im Strahlungslabor zeigen."},
     [("Radioaktivität", "Instabile Kerne zerfallen zufällig.", [1]), ("Drei Strahlungsarten", "α, β, γ an der Folie und im Labor.", [2]), ("Üben", "Arbeitsblatt, Alltag mündlich.", [3, 4])],
     S4, S4_HG, S4_AB),
    ("Kernphysik – W05 Zerfallsgleichungen – Stunde.html", "Kernphysik: Zerfallsgleichungen und Durchdringung", "Klasse 10 · Physik · W05 (Woche ab 12.10.2026) · Leitfrage 2",
     ["Arbeitsblatt Durchdringung und Zerfallsgleichungen: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [("Präparate α, β, γ", "je 1", "nur Lehrkraft, nach RiSU"), ("Geiger-Müller-Zählrohr mit Zählgerät", "1×", ""),
               ("Absorber: Papier, Aluminium 5 mm, Blei", "je 1", "")], "schueler": [("Periodensystem", "1×", "")],
      "hinweis": "Ohne Präparate: Absorberversuch im Strahlungslabor."},
     [("Zerfallsgleichungen", "Regeln an der Folie, Übungen im Labor.", [1]), ("Durchdringung", "Absorberversuch vorne, Arbeitsblatt.", [2, 3]), ("Alltag", "Abschirmung.", [4])],
     S5, S5_HG, S5_AB),
]

for datei, h1, sub, drucken, mat, schritte, folge, hg, ab in STUNDEN:
    bau_stunde(datei, h1, sub, drucken, mat, schritte, folge, hg, ab, ziel=HIER, css_href="../Optik/folien.css", extra_css=KERN_CSS)
