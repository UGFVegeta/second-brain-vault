#!/usr/bin/env python3
"""F1 (Leitfrage 1, Lichtquellen) im gleichen Gerüst wie F3 bis F8: Überblick, Folien, Heft, Hintergrund, Arbeitsblätter.
Folien aus Optik I (Seite 1 bis 11, die leeren Zeichenfolien weggelassen), Inhalte des Hintergrunds aus der alten ALLES-Datei.
python3 baue_stunde_f1.py          -> Optik – Leitfrage 1 – Stunde.html
python3 baue_stunde_f1.py export   -> zusätzlich Folien-PDF und Stunden-HTML nach iCloud (F1 Lichtquellen (W03))"""
import sys
from stunde_vorlage import basis, blatt, chip, bau_stunde, exportiere, ICL

F1 = [basis(1), basis(2), basis(3), basis(4), basis(5), basis(6), basis(7), basis(9), basis(11),
      blatt("Lichtquellen W03.pdf", "lq", "Arbeitsblatt austeilen")]

F1_MATERIAL = {
    "demo": [("Glühlampe mit Fassung", "1×", "für den Licht-an/Licht-aus-Impuls"),
             ("zwei unterschiedlich schwere Bälle", "2", "Einstieg naturwissenschaftliche Arbeitsweise, Fallversuch")],
    "schueler": [],
    "hinweis": "Raum verdunkeln, nur die Lampe vorne an. Das Arbeitsblatt Lichtquellen braucht kein Material.",
}

F1_SCHRITTE = [
    ("Arbeitsweise", "Zwei Bälle fallen lassen: vermuten, beobachten, erklären. So arbeiten wir ab jetzt immer.", [1, 2, 3, 4]),
    ("Einstieg Optik", "Licht an, Licht aus. Leitfrage 1, Vermutungen.", [5, 6, 7]),
    ("Wie sehen wir?", "Licht muss ins Auge. Sender und Empfänger, im Sehlabor zeigen.", [8]),
    ("Lichtquellen", "Selbstleuchtend oder beleuchtet, natürlich oder künstlich.", [9]),
    ("Üben", "Arbeitsblatt Lichtquellen.", [10]),
]

F1_HG = f"""
<div class="box"><h3>Worauf du achten kannst {chip(8, 9)}</h3><ul>
<li>Der Mond wird für eine Lichtquelle gehalten, weil er hell aussieht.</li>
<li>Hell wird mit selbstleuchtend verwechselt: Ein weißes Blatt oder ein Spiegel wirkt hell, erzeugt aber kein Licht.</li>
<li>Rückstrahler und Katzenaugen „leuchten“ nur, wenn sie angestrahlt werden. Das Wort „leuchten“ ruhig hinterfragen.</li>
<li>Manche Kinder denken noch, das Auge sende etwas aus. Kurz zurückführen auf „Licht muss ins Auge gelangen“.</li></ul></div>
<div class="box"><h3>Denkfragen für das Gespräch {chip(9)}</h3><ul>
<li>Im dunklen Zimmer machst du das Licht aus. Warum siehst du plötzlich nichts mehr, obwohl alle Möbel noch da sind?</li>
<li>Ein Radfahrer trägt eine Stirnlampe und eine Warnweste. Was davon ist Lichtquelle, was beleuchteter Körper?</li>
<li>Kann ein Körper gleichzeitig Lichtquelle und beleuchteter Körper sein? (Beispiel: ein Bildschirm, der angestrahlt wird.)</li></ul></div>
<div class="box"><h3>Sehlabor</h3><a class="btn" href="Sehlabor Lichtquellen.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Sender und Empfänger, Lichtquellen zuordnen, Sehen und gesehen werden auf der Straße. Auch für zu Hause über IServ.</p></div>
<div class="box"><h3>Frühere Fassung</h3><p><a class="btn" href="Optik 1 – Lichtquellen und beleuchtete Körper – ALLES.html">ALLES-Datei öffnen</a>
Dort stehen Verlauf mit Minuten, Merkheft, Aufgaben aus dem Buch und Lösungen.</p></div>"""

F1_AB = f"""
<div class="box"><h3>Arbeitsblatt Lichtquellen {chip(10)}</h3>
<a class="btn" href="Materialien/Lichtquellen W03.pdf">PDF öffnen</a>
<p>Die Lösung steht auf Folie 10 im ausgefüllten Blatt.</p></div>"""

HTML = "Optik – Leitfrage 1 – Stunde.html"
bau_stunde(HTML, "Optik: Warum sehen wir überhaupt etwas?", "Klasse 7c · Physik · Leitfrage 1 · Lichtquellen und beleuchtete Körper (W03)",
           ["Arbeitsblatt Lichtquellen: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
           F1_MATERIAL, F1_SCHRITTE, F1, F1_HG, F1_AB)

if "export" in sys.argv:
    ordner = ICL / "F1 Lichtquellen (W03)"
    exportiere(F1, ordner, "Folien F1.pdf", "Arbeitsblatt F1.pdf", "Stunde Leitfrage 1.html", HTML,
               {"Materialien/Lichtquellen W03.pdf": "Arbeitsblatt F1.pdf", "Sehlabor Lichtquellen.html": "../Labore/Sehlabor Lichtquellen.html",
                "Optik-Labore.html": "../Labore/Optik-Labore.html",
                "Optik 1 – Lichtquellen und beleuchtete Körper – ALLES.html": "Gesamt.html"})
