#!/usr/bin/env python3
"""Stunden-HTMLs Kernphysik Klasse 10, W01 bis W05 (je eine Einzelstunde). Gleicher Aufbau wie Klasse 7.
Ideen aus „Erlebnis Physik“ Kl. 10 (Versuche, Alltag, Fragen) sind eingearbeitet, in eigenen Worten.
python3 baue_stunden_k10.py   -> HTMLs im Ordner Kernphysik (Export nach iCloud erst nach Freigabe)"""
import re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent / "Optik"))
from stunde_vorlage import folien_aus, blatt as _blatt, chip, tabellenfolie, bau_stunde  # noqa: E402
from kern_zeichnungen import zeitstrahl, efeld  # noqa: E402

MAT = HIER / "Materialien"
_F = folien_aus(HIER / "Kernphysik.html")
_quelle = (HIER / "Kernphysik.html").read_text(encoding="utf-8")
KERN_CSS = _quelle[_quelle.index("<style>") + 7:_quelle.index("</style>")]


def f(p):
    return re.sub(r'\s*<div class="ab-hinweis">.*?</div>', "", _F[p - 1], flags=re.S)


def blatt(pdf, key, hinweis):
    return _blatt(pdf, key, hinweis, mat=MAT)


def zeichnungsfolie(titel, svg, merksatz):
    return (f'<section class="folie"><div class="titelband"><h1>{titel}</h1></div>'
            f'<div class="zeichenzone karo">{svg}</div><div class="merksatz">{merksatz}</div></section>')


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
ZEIT = zeichnungsfolie("Wie man das Atom entdeckte", zeitstrahl(),
                       "Das Wort <b>Atom</b> kommt aus dem Griechischen und heißt „unteilbar“. Heute wissen wir: "
                       "Atome bestehen aus <span class=\"rot\">Kern und Hülle</span>, der Kern aus Protonen und Neutronen.")
S1 = [f(2), f(3), blatt("Atome enthalten elektrische Ladungen W01.pdf", "k01v", "Versuchsblatt austeilen · Luftballon und Wolltuch pro Gruppe"),
      ZEIT, A1]
S1_HG = f"""
<div class="box"><h3>Größenordnungen {chip(1, 5)}</h3><ul>
<li>Atomdurchmesser etwa 10⁻¹⁰ m, Kerndurchmesser etwa 10⁻¹⁵ bis 10⁻¹⁴ m. Das Verhältnis liegt bei 10 000 bis 100 000.</li>
<li>Fast die gesamte Masse steckt im Kern. Ein Proton ist rund 1800-mal so schwer wie ein Elektron.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Atom ist eine volle Kugel. Elektronen kreisen auf festen Bahnen wie Planeten. Atome kann man mit dem Mikroskop sehen.</li></ul></div>
<div class="box"><h3>Ladungsversuche {chip(3)}</h3><ul>
<li>Beim Reiben an Wolle nimmt der Ballon Elektronen auf und wird negativ, die Wolle bleibt positiv zurück. Daraus folgt: Elektronen lassen sich aus Atomen lösen, Atome enthalten also Ladungen.</li>
<li>Der Wasserstrahl wird von jeder Ladung angezogen, weil sich im Wasser die Ladungen verschieben (Wassermoleküle richten sich aus). Das ist die Frage 4 auf dem Blatt.</li>
<li>Klappt am besten bei trockener Luft. Die Papierschnipsel möglichst klein reißen. Wer kein Waschbecken im Raum hat, zeigt Versuch 2 vorne.</li>
<li>Mit einem Elektroskop lässt sich zusätzlich zeigen, dass der Ballon geladen ist: Der Zeiger schlägt aus, sobald der Ballon den Knopf berührt.</li></ul></div>
<div class="box"><h3>Geschichte des Atommodells {chip(4)}</h3><ul>
<li>Demokrit (um 400 v. Chr.) dachte sich unteilbare Teilchen. Dalton (1803) ordnete jedem Element eine Atomsorte zu.</li>
<li>1897 wurde das Elektron entdeckt (Thomson, in Deutschland zeitgleich Wiechert). Rutherfords Streuversuch (1909 bis 1911) führte zum Kern-Hülle-Modell. Das Proton wies Rutherford 1919 nach, das Neutron Chadwick 1932.</li>
<li>Der Streuversuch lässt sich in der Schule nicht nachmachen. Das Atomlabor zeigt ihn als Simulation: Fast alle α-Teilchen fliegen durch die Goldfolie, nur sehr wenige prallen zurück.</li></ul></div>
{LAB(ATOM, "Atomlabor", "Zoom vom Atom auf den Kern, Rutherfords Streuversuch mit Teilchenzahl-Regler, Atom bauen, Isotope, Nuklidkarte.")}"""
S1_AB = f"""<div class="box"><h3>Versuchsblatt Atome enthalten elektrische Ladungen {chip(3)}</h3><a class="btn" href="Materialien/Atome enthalten elektrische Ladungen W01.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Papierschnipsel springen zum Ballon, der Wasserstrahl biegt sich zum Ballon. Lücken: Elektronen, negativ, positiv, herauslösen, negative, positive, neutral.
Frage 4: Im Wasser verschieben sich die Ladungen, die zugewandte Seite wird entgegengesetzt geladen und angezogen.</p></div>"""

# ====================================================================== W02
A2 = tabellenfolie("Isotope im Alltag", [
    ("Kohlenstoff-14", "Altersbestimmung von Funden", "Sein Anteil in toten Lebewesen nimmt mit der Zeit ab."),
    ("Deuterium (H-2)", "schweres Wasser", "Chemisch Wasser, aber etwas schwerer."),
    ("Iod-131", "Untersuchung der Schilddrüse", "Die Schilddrüse sammelt Iod, das Isotop macht sie sichtbar."),
    ("Uran-235", "Brennstoff im Kernkraftwerk", "Nur dieses Isotop lässt sich im Reaktor gut spalten."),
], frage="Warum verhalten sich Kohlenstoff-12 und Kohlenstoff-14 chemisch gleich?")
S2 = [blatt("Wiederholung Atombau.pdf", "k01", "Nur bei Bedarf: Wiederholung Atombau aus Chemie"), f(5), f(7),
      blatt("Nuklide und Isotope W02.pdf", "k02", "Arbeitsblatt austeilen · mit Periodensystem"), A2]
S2_HG = f"""
<div class="box"><h3>Vorwissen aus Chemie {chip(1)}</h3><ul>
<li>Das Blatt holt Schalenmodell und Periodensystem aus Klasse 8 und 9 zurück. Nur einsetzen, wenn bei den Ladungsversuchen in W01 Lücken sichtbar waren.</li></ul></div>
<div class="box"><h3>Nuklidschreibweise {chip(2, 4)}</h3><ul>
<li>A oben links (Massenzahl), Z unten links (Kernladungszahl). Die Neutronenzahl ist N = A − Z, anders herum A = Z + N.</li>
<li>Kurzschreibweise: Name oder Symbol mit Massenzahl, also Natrium-23 oder Na-23. Z steckt schon im Symbol.</li>
<li>Beispiel aus dem Buch: 82 Protonen und 124 Neutronen. Z = 82 ist Blei, A = 206, also Pb-206. Steht als Aufgabe 4 auf dem Blatt.</li>
<li>Die Chemie hängt nur von den Elektronen ab, also von Z. Deshalb verhalten sich Isotope chemisch gleich.</li>
<li>Die Masse im Periodensystem ist ein Mittelwert über die natürlichen Isotope. Deshalb ist sie keine ganze Zahl.</li>
<li><b>Typische Fehlvorstellungen:</b> A und Z werden vertauscht. Isotope sind verschiedene Elemente. Isotope sind immer radioaktiv.</li></ul></div>
<div class="box"><h3>Nuklidkarte und Ausblick</h3><ul>
<li>In der Nuklidkarte ist jeder Kern ein Kästchen: Protonenzahl nach oben, Neutronenzahl nach rechts. Die stabilen Kerne liegen auf einem schmalen Band. Rechts davon (zu viele Neutronen) sitzen die β⁻-Strahler. Das bereitet W04 vor.</li>
<li>Für Interessierte: Protonen und Neutronen bestehen selbst aus je drei Quarks. Elektronen und Quarks gelten nach heutigem Wissen als nicht weiter teilbar.</li></ul></div>
{LAB(ATOM, "Atomlabor", "Atom bauen: Protonen, Neutronen und Elektronen einstellen, das Nuklid erscheint mit Stabilität. Isotope von Wasserstoff, Kohlenstoff und Uran. Nuklidkarte von Wasserstoff bis Sauerstoff.")}"""
S2_AB = f"""<div class="box"><h3>Arbeitsblatt Nuklide und Isotope {chip(4)}</h3><a class="btn" href="Materialien/Nuklide und Isotope W02.pdf">PDF öffnen</a>
<p><b>Lösung:</b> H 1/0/1, He 2/2/2, C-12 6/6/6, C-14 6/8/6, O 8/8/8, U-235 92/143/92, U-238 92/146/92. Lücken: Protonen, Neutronen, Z + N, Protonen, Neutronen, C-12 und C-14, U-235 und U-238.
C-13, Na-23, He-3, Fe-56. Pb-206. U-235 und U-238 haben die gleiche Hülle und lassen sich nur über die Masse trennen.</p></div>
<div class="box"><h3>Wiederholung Atombau {chip(1)}</h3><a class="btn" href="Materialien/Wiederholung Atombau.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Seite 2 des PDFs.</p></div>"""

# ====================================================================== W03
A3 = tabellenfolie("Natürliche Strahlung im Alltag", [
    ("Keller", "Radon aus dem Boden", "Ein radioaktives Gas, das sich in Kellerräumen sammeln kann."),
    ("Flugzeug", "mehr kosmische Strahlung", "In großer Höhe schirmt weniger Luft ab."),
    ("unser Körper", "Kalium-40", "Ein kleiner Teil des Kaliums in Muskeln und Nahrung ist radioaktiv."),
    ("Granit, Schwarzwald", "etwas höhere Zählrate", "Das Gestein enthält Spuren von Uran und Thorium."),
], frage="Warum misst das Zählrohr im Physikraum auch ohne Präparat Impulse?")
S3 = [f(8), f(9), f(10), f(11), f(12), blatt("Zaehlrohr und Nullrate W03.pdf", "k03", "Arbeitsblatt austeilen · Nullrate vorne messen · Ballonversuch am Ende"), A3]
S3_HG = f"""
<div class="box"><h3>Das Zählrohr {chip(4, 6)}</h3><ul>
<li>Geiger-Müller-Zählrohr: Metallrohr (Kathode) mit einem Edelgas und einem dünnen Draht in der Mitte (Anode), dazwischen etwa 500 V. Vorne ein dünnes Glimmerfenster, damit auch α-Teilchen hineinkommen.</li>
<li>Strahlung ionisiert das Gas, die Ladungen lösen eine Lawine aus, es gibt einen kurzen Stromstoß (Impuls). Hans Geiger baute 1913 den Vorläufer, mit Walther Müller 1928 das heutige Zählrohr.</li>
<li>Das Zählrohr zählt Impulse. Es unterscheidet nicht zwischen α, β und γ und erfasst nur einen Teil der Strahlung.</li>
<li><b>Nullrate:</b> Je nach Zählrohr und Ort etwa 10 bis 40 Impulse pro Minute. Sie schwankt zufällig, deshalb mehrere Minuten messen und mitteln.</li>
<li><b>Typische Fehlvorstellungen:</b> Strahlung gibt es nur in der Nähe von Kernkraftwerken. Das Zählrohr misst „die Radioaktivität“ eines Stoffes direkt.</li></ul></div>
<div class="box"><h3>Wie Radioaktivität entdeckt wurde</h3><ul>
<li>Röntgen entdeckte 1895 die nach ihm benannte Strahlung. Becquerel fand 1896, dass Uransalze eine eingepackte Fotoplatte schwärzen, ganz ohne Licht.</li>
<li>Marie und Pierre Curie entdeckten 1898 Polonium und Radium und prägten das Wort „radioaktiv“. Marie Curie erhielt 1903 (Physik) und 1911 (Chemie) den Nobelpreis.</li>
<li>Einheit der Aktivität ist das Becquerel: 1 Bq heißt ein Zerfall pro Sekunde. Das ist nur Ausblick, das Zählrohr misst weniger als die Aktivität.</li></ul></div>
<div class="box"><h3>Tipps zu den Versuchen {chip(6)}</h3><ul>
<li>Lautsprecher an, damit die Klasse das Knacken hört. Fünfmal eine Minute messen, Werte an der Tafel sammeln.</li>
<li>Die Streuung der Werte ist gewollt: Radioaktiver Zerfall ist Zufall. Das bereitet Leitfrage 2 vor.</li>
<li><b>Luftballon:</b> vor der Stunde aufblasen, an Wolle reiben und 20 bis 30 Minuten aufhängen, am besten in einem Kellerraum. Dann Luft ablassen, Hülle zusammenknüllen und direkt vor das Zählrohr legen. Der Ballon sammelt Folgeprodukte des Radons (vor allem Pb-214 und Bi-214). Die Zählrate sinkt innerhalb von ein bis zwei Stunden wieder auf die Nullrate. Wie stark der Effekt ist, hängt vom Radongehalt der Luft ab. Klappt es nicht, zeigt das Strahlungslabor den Verlauf.</li></ul></div>
{LAB(STRAHL, "Strahlungslabor", "Nullrate mit zehn zufälligen Messungen und Mittelwert. Luftballon: Zählrate über der Zeit, gerieben und ungerieben.")}"""
S3_AB = f"""<div class="box"><h3>Arbeitsblatt Zählrohr und Nullrate {chip(6)}</h3><a class="btn" href="Materialien/Zaehlrohr und Nullrate W03.pdf">PDF öffnen</a>
<p><b>Lösung:</b> 1 dünne Folie, 2 Gas, 3 Metalldraht, 4 Metallrohr. Lücken: Zählrohr, Impulse, zählt, Knacken, Impulsrate, höher, stärker. Beispielmessung 22, 27, 19, 25, 24, Mittelwert 23,4. Nullrate, menschlichen Körpers, terrestrische, kosmische.
Ballon: sammelt radioaktive Folgeprodukte des Radons aus der Luft, diese zerfallen, die Zählrate sinkt wieder.</p></div>"""

# ====================================================================== W04
A4 = tabellenfolie("Strahler im Alltag", [
    ("Rauchmelder (ältere Modelle)", "α-Strahler Americium-241", "Die Strahlung macht Luft leitend. Rauch stört das und löst Alarm aus."),
    ("Banane", "β-Strahler Kalium-40", "Winzige Menge, nicht gefährlich."),
    ("Medizin", "γ-Strahler Technetium-99m", "Zeigt im Körper, wo sich ein Stoff anreichert."),
    ("Keller", "α-Strahler Radon", "Gefährlich, wenn man es einatmet."),
], frage="Warum ist Radon gefährlich, obwohl α-Strahlung schon von Papier gestoppt wird?")
EF = zeichnungsfolie("Strahlung im elektrischen Feld", efeld(),
                     "Zwischen geladenen Platten wird <b>α</b> leicht zum Minuspol und <b>β⁻</b> stark zum Pluspol abgelenkt. "
                     "<b>γ</b> fliegt geradeaus: <span class=\"rot\">γ-Strahlung trägt keine Ladung</span>.")
S4 = [f(14), f(16), EF, blatt("Drei Strahlungsarten W04.pdf", "k04", "Arbeitsblatt austeilen"), A4]
S4_HG = f"""
<div class="box"><h3>Radioaktivität {chip(1)}</h3><ul>
<li>Instabile Kerne haben zu viele oder zu wenige Neutronen im Verhältnis zu den Protonen. Alle Elemente mit mehr als 83 Protonen sind radioaktiv.</li>
<li>Der Zeitpunkt des Zerfalls eines einzelnen Kerns ist zufällig. Für viele Kerne gilt eine feste Halbwertszeit (Leitfrage 3).</li></ul></div>
<div class="box"><h3>α, β und γ {chip(2, 3)}</h3><ul>
<li><b>α:</b> Heliumkern, zweifach positiv, groß und langsam, gibt seine Energie auf kurzer Strecke ab. In Luft nur wenige Zentimeter (je nach Energie etwa 3 bis 7 cm). Außen harmlos, innen (eingeatmet, verschluckt) sehr schädlich.</li>
<li><b>β⁻:</b> schnelles Elektron aus dem Kern. Im Kern wird ein Neutron zum Proton. In Luft einige Meter. Es gibt auch β⁺ (Positron), das ist nicht verlangt.</li>
<li><b>γ:</b> energiereiche elektromagnetische Strahlung, folgt oft auf α- oder β-Zerfall, wenn der Tochterkern noch angeregt ist. Reicht in Luft sehr weit und wird nur allmählich schwächer.</li>
<li><b>Ablenkung:</b> Aus der Richtung im elektrischen Feld folgt die Ladung. α wird trotz doppelter Ladung weniger abgelenkt als β⁻, weil es rund 7000-mal so schwer ist. Die Bahnen auf der Folie sind qualitativ.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Elektron beim β-Zerfall kommt aus der Hülle. Bestrahlte Gegenstände werden selbst radioaktiv.</li></ul></div>
<div class="box"><h3>Strahlenschutz im Unterricht</h3><ul>
<li>Präparate nur durch die Lehrkraft und nach den Vorgaben der Richtlinie zur Sicherheit im Unterricht (RiSU). Fehlt ein Präparatesatz, zeigt das Strahlungslabor die Zerfälle.</li></ul></div>
{LAB(STRAHL, "Strahlungslabor", "Präparat und Abstand, α-, β- und γ-Zerfall mit Nuklidgleichung, Ablenkung im elektrischen Feld mit Spannung an und aus.")}"""
S4_AB = f"""<div class="box"><h3>Arbeitsblatt Drei Arten radioaktiver Strahlung {chip(4)}</h3><a class="btn" href="Materialien/Drei Strahlungsarten W04.pdf">PDF öffnen</a>
<p><b>Lösung:</b> α: Heliumkern, positiv, schwach zum Minuspol, wenige cm. β⁻: Elektron, negativ, stark zum Pluspol, einige m. γ: Energie, keine Ladung, keine Ablenkung, sehr weit.
α: A − 4, Z − 2. β⁻: A bleibt, Z + 1. γ: beide bleiben. Lücken: 2 Protonen, 2 Neutronen, Neutron, Proton, Energie. Zuordnung: α, β⁻, γ. Aufgabe 5: γ, keine Ladung, α und β würden vom Aluminium gestoppt.</p></div>"""

# ====================================================================== W05
A5 = tabellenfolie("Abschirmung im Alltag", [
    ("Bleischürze beim Röntgen", "schützt die übrigen Körperteile", "Blei schwächt energiereiche Strahlung stark."),
    ("Rauchmelder", "darf man anfassen", "Die α-Strahlung kommt nicht einmal durch das Gehäuse."),
    ("Behälter für radioaktive Stoffe", "dicke Wände aus Stahl oder Blei", "γ-Strahlung wird nur geschwächt, nie ganz gestoppt."),
], frage="Welche Strahlung ist außerhalb des Körpers am gefährlichsten, welche innerhalb?")
A6 = tabellenfolie("Strahlung als Werkzeug", [
    ("Schweißnaht prüfen", "Risse werden sichtbar", "γ-Strahlung durchdringt Stahl, hinter einem Riss kommt mehr an."),
    ("Papier- oder Folienfabrik", "Dicke wird ständig gemessen", "Je dicker das Material, desto weniger β-Strahlung kommt durch."),
    ("Leck in einer Leitung", "Zählrohr findet die Stelle", "Man gibt einen kurzlebigen Strahler ins Wasser. Am Leck steigt die Zählrate."),
    ("Schädlinge bekämpfen", "Insekten ohne Gift", "Bestrahlte Männchen sind unfruchtbar, es schlüpft kein Nachwuchs."),
], frage="Warum nimmt man für die Dickenmessung von Papier β-Strahlung und nicht γ-Strahlung?")
S5 = [f(18), f(20), blatt("Durchdringung und Zerfallsgleichungen W05.pdf", "k05", "Arbeitsblatt austeilen · Absorberversuch vorne"), A5, A6]
S5_HG = f"""
<div class="box"><h3>Zerfallsgleichungen {chip(1)}</h3><ul>
<li>Oben (Massenzahl) und unten (Ladung) muss die Summe links und rechts gleich sein. Das Elektron schreibt man mit 0 oben und −1 unten.</li>
<li>Das neue Element liest man über die Kernladungszahl im Periodensystem ab. Deshalb liegt das Periodensystem immer auf dem Tisch.</li>
<li><b>Zerfallsreihe</b> (Aufgabe 5): U-238 wird durch α zu Th-234, durch β⁻ zu Pa-234, durch β⁻ zu U-234. Die ganze Reihe endet nach 14 Schritten beim stabilen Pb-206.</li></ul></div>
<div class="box"><h3>Durchdringung {chip(2)}</h3><ul>
<li>α: wenige Zentimeter Luft, ein Blatt Papier. β: einige Meter Luft, einige Millimeter Aluminium. γ: wird exponentiell geschwächt, nie ganz auf null.</li>
<li>Das Buch nennt 1 mm Aluminium für β. Das reicht nur für weiche β-Strahler. Für das Schulpräparat Sr-90/Y-90 braucht man etwa 5 mm, deshalb steht auf dem Blatt 5 mm.</li>
<li>Bei α-Präparaten kann hinter Papier noch etwas γ-Strahlung gemessen werden, wenn das Präparat zusätzlich γ aussendet (z. B. Americium-241).</li>
<li><b>Typische Fehlvorstellung:</b> Durchdringende Strahlung ist immer gefährlicher. Für den Körper hängt es davon ab, ob die Quelle außen oder innen ist.</li></ul></div>
<div class="box"><h3>Warum Blei γ nur schwächt</h3><ul>
<li>Jedes γ-Quant fliegt entweder ungestört durch oder wird unterwegs absorbiert oder gestreut. Das ist Zufall. Jede Schicht gleicher Dicke hält denselben Anteil zurück, nicht dieselbe Anzahl.</li>
<li>Die Dicke, nach der die Hälfte übrig ist, heißt Halbwertsdicke. Blei: etwa 0,65 cm bei Cs-137, etwa 1,2 cm bei Co-60. Das Buch nennt 13 mm Blei für 50 %. Beton muss für dieselbe Wirkung etwa fünf- bis siebenmal so dick sein.</li>
<li>Nach 10 Halbwertsdicken ist noch etwa ein Tausendstel übrig, nach 20 etwa ein Millionstel. Null wird es nie, aber irgendwann geht der Rest in der Nullrate unter. Mehr Beton hilft also, man braucht nur viel mehr davon.</li></ul></div>
<div class="box"><h3>Strahlung als Werkzeug {chip(5)}</h3><ul>
<li>Bestrahlte Gegenstände werden nicht selbst radioaktiv. Deshalb kann man mit γ-Strahlung auch Verbandsmaterial und Spritzen keimfrei machen.</li>
<li>Die Antwort zur Folienfrage: Dünnes Papier schwächt γ-Strahlung kaum messbar. β-Strahlung reagiert schon auf kleine Dickenunterschiede.</li></ul></div>
{LAB(STRAHL, "Strahlungslabor", "Zerfallsgleichungen üben mit sofortiger Rückmeldung, Absorberversuch mit Papier, Aluminium und Blei, Bleidicke per Regler mit Kurve und Nullrate.")}"""
S5_AB = f"""<div class="box"><h3>Arbeitsblatt Durchdringung und Zerfallsgleichungen {chip(3)}</h3><a class="btn" href="Materialien/Durchdringung und Zerfallsgleichungen W05.pdf">PDF öffnen</a>
<p><b>Lösung:</b> α hinter Papier fast Nullrate, β hinter Aluminium fast Nullrate, γ hinter Blei kleiner, aber über der Nullrate. Lücken: Papier, Aluminium, Blei.
Bleitabelle 800, 400, 200, 100, 50, die Zählrate wird nie ganz null. Po-210 → Pb-206 + He-4, K-40 → Ca-40 + e, Ra-226 → Rn-222 + He-4. Zerfallsreihe Th-234, Pa-234, U-234.</p></div>"""

STUNDEN = [
    ("Kernphysik – W01 Woraus besteht Materie – Stunde.html", "Kernphysik: Woraus besteht Materie?", "Klasse 10 · Physik · W01 (Woche ab 14.09.2026) · Einstieg Leitfrage 1",
     ["Versuchsblatt Atome enthalten elektrische Ladungen: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [("Wasserhahn mit dünnem Strahl", "1×", "falls kein Waschbecken an den Gruppentischen"), ("Elektroskop", "1×", "freiwillig, zeigt die Ladung des Ballons")],
      "schueler": [("Luftballon, aufgeblasen", "1×", ""), ("Wolltuch oder Wollpullover", "1×", ""), ("Papierschnipsel", "eine Handvoll", "klein gerissen")],
      "hinweis": "Bei feuchter Luft klappen die Ladungsversuche schlechter. Ersatzballons bereithalten."},
     [("Einstieg", "Stadion und Erbse, Leitfrage 1, Vermutungen.", [1, 2]), ("Versuch", "Luftballon, Papierschnipsel, Wasserstrahl, Versuchsblatt.", [3]),
      ("Geschichte", "Wie man das Atom entdeckte, Rutherford im Atomlabor.", [4]), ("Größen", "Wie klein ist ein Atom? Zoom im Atomlabor.", [5])],
     S1, S1_HG, S1_AB),
    ("Kernphysik – W02 Atombau und Isotope – Stunde.html", "Kernphysik: Atombau und Isotope", "Klasse 10 · Physik · W02 (Woche ab 21.09.2026) · Leitfrage 1",
     ["Arbeitsblatt Nuklide und Isotope: Seite 1, eins pro Schüler.", "Wiederholung Atombau: nur bei Bedarf.", "Folien und Lösungen: nicht drucken."],
     {"demo": [], "schueler": [("Periodensystem", "1×", "")], "hinweis": ""},
     [("Wiederholung", "Nur bei Bedarf: Atombau aus Chemie.", [1]), ("Aufbau", "Kern und Hülle, Nuklidschreibweise, A = Z + N.", [2]),
      ("Isotope", "Wasserstoff, Deuterium, Tritium. Nuklidkarte im Atomlabor.", [3]), ("Üben", "Arbeitsblatt, Alltag mündlich.", [4, 5])],
     S2, S2_HG, S2_AB),
    ("Kernphysik – W03 Zaehlrohr und Nullrate – Stunde.html", "Kernphysik: Das Zählrohr klickt von allein", "Klasse 10 · Physik · W03 (Woche ab 28.09.2026) · Abschluss Leitfrage 1, Einstieg Leitfrage 2",
     ["Arbeitsblatt Zählrohr und Nullrate: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [("Geiger-Müller-Zählrohr mit Zählgerät", "1×", "Lautsprecher an"), ("Stoppuhr", "1×", "fünfmal eine Minute"),
               ("Luftballon und Wolltuch", "je 1", "vor der Stunde gerieben und aufgehängt")], "schueler": [],
      "hinweis": "Kein Präparat nötig. Das Zählrohr ist vor der Stunde eingeschaltet und steht weit weg von der Präparatesammlung. Ballon 20 bis 30 Minuten vorher im Keller aufhängen."},
     [("Abschluss Leitfrage 1", "Antwort ins Heft, Check.", [1, 2, 3]), ("Einstieg Leitfrage 2", "Zählrohr klickt, Leitfrage 2.", [4, 5]),
      ("Versuch", "Nullrate messen, Arbeitsblatt, dann der Ballon vor dem Zählrohr.", [6]), ("Alltag", "Natürliche Strahlung.", [7])],
     S3, S3_HG, S3_AB),
    ("Kernphysik – W04 Alpha Beta Gamma – Stunde.html", "Kernphysik: Alpha, Beta und Gamma", "Klasse 10 · Physik · W04 (Woche ab 05.10.2026) · Leitfrage 2",
     ["Arbeitsblatt Drei Arten radioaktiver Strahlung: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [("Präparatesatz", "1", "nur Lehrkraft, nach RiSU"), ("Geiger-Müller-Zählrohr mit Zählgerät", "1×", "")], "schueler": [("Periodensystem", "1×", "")],
      "hinweis": "Ohne Präparatesatz: Zerfälle und Ablenkung im Strahlungslabor zeigen."},
     [("Radioaktivität", "Instabile Kerne zerfallen zufällig.", [1]), ("Drei Strahlungsarten", "α, β, γ an der Folie und im Labor.", [2]),
      ("Ablenkung", "Strahlung im elektrischen Feld, im Labor Spannung an und aus.", [3]), ("Üben", "Arbeitsblatt, Alltag mündlich.", [4, 5])],
     S4, S4_HG, S4_AB),
    ("Kernphysik – W05 Zerfallsgleichungen – Stunde.html", "Kernphysik: Zerfallsgleichungen und Durchdringung", "Klasse 10 · Physik · W05 (Woche ab 12.10.2026) · Leitfrage 2",
     ["Arbeitsblatt Durchdringung und Zerfallsgleichungen: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     {"demo": [("Präparate α, β, γ", "je 1", "nur Lehrkraft, nach RiSU"), ("Geiger-Müller-Zählrohr mit Zählgerät", "1×", ""),
               ("Absorber: Papier, Aluminium 5 mm, Bleiplatten", "je 1", "mehrere gleich dicke Bleiplatten, falls vorhanden")], "schueler": [("Periodensystem", "1×", "")],
      "hinweis": "Ohne Präparate: Absorberversuch und Bleidicke im Strahlungslabor."},
     [("Zerfallsgleichungen", "Regeln an der Folie, Übungen im Labor.", [1]), ("Durchdringung", "Absorberversuch vorne, Bleidicke im Labor, Arbeitsblatt.", [2, 3]),
      ("Alltag", "Abschirmung und Strahlung als Werkzeug.", [4, 5])],
     S5, S5_HG, S5_AB),
]

if __name__ == "__main__":
  for datei, h1, sub, drucken, mat, schritte, folge, hg, ab in STUNDEN:
    bau_stunde(datei, h1, sub, drucken, mat, schritte, folge, hg, ab, ziel=HIER, css_href="../Optik/folien.css", extra_css=KERN_CSS)
