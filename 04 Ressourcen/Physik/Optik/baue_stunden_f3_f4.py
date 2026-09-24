#!/usr/bin/env python3
"""Stunden-HTMLs Leitfrage 3 (Lichtausbreitung) und Leitfrage 4 (Kern-/Halbschatten), Optik 7c.
python3 baue_stunden_f3_f4.py          -> nur die HTMLs im Vault
python3 baue_stunden_f3_f4.py export   -> zusätzlich Folien-PDF, Materialliste, Gesamt, Stunden-HTML nach iCloud"""
import shutil, sys
from stunde_vorlage import (basis, blatt, chip, tabellenfolie, bau_stunde, exportiere, materialliste,
                            zwei_auf_eins, MAT, ICL)

# ====================================================================== Leitfrage 3
F3_ALLTAG = tabellenfolie("Geradlinige Ausbreitung im Alltag", [
    ("Sonne hinter Wolken", "helle, gerade Streifen", "Das Licht läuft geradlinig durch die Wolkenlücken. Dunst und Staub machen den Weg sichtbar."),
    ("Scheinwerfer im Nebel", "ein gerades Lichtbündel", "Die Nebeltröpfchen streuen einen Teil des Lichts zu uns."),
    ("Blick durchs Schlüsselloch", "nur ein kleiner Teil des Zimmers", "Nur Licht, das auf gerader Linie durch das Loch kommt, erreicht das Auge."),
    ("Verkehrsspiegel an einer Ausfahrt", "man sieht um die Ecke", "Das Licht geht nicht um die Ecke. Der Spiegel lenkt es um."),
    ("Kreuzlinienlaser beim Fliesenlegen", "eine gerade rote Linie an der Wand", "Weil Licht geradlinig läuft, dient es als Lineal."),
], frage="Warum sieht man das Lichtbündel im Nebel, in klarer Luft aber nicht?")

F3 = [
    basis(22), basis(23),
    blatt("Lichtausbreitung und Blende W05.pdf", "w05", "Versuchsblatt austeilen · Versuch in Gruppen"),
    basis(25), basis(27), F3_ALLTAG,
    basis(28), basis(29), basis(30),
]

F3_MATERIAL = {
    "demo": [],
    "schueler": [("Ray-Box mit Stromanschluss", "1×", "Lampenseite zur Blende"),
                 ("Blende mit Loch", "1×", ""),
                 ("Schirm", "1×", "oder ein weißes Blatt, als Wand gefaltet")],
    "hinweis": "Raum abdunkeln. Reichen die Ray-Boxen nicht für alle Gruppen, den Versuch vorne als Demo zeigen.",
}

F3_HG = f"""
<div class="box"><h3>Wie breitet sich Licht aus? {chip(4)}</h3><ul>
<li><b>Geradlinig</b>, solange der Stoff gleich bleibt (Luft, Wasser, Glas). An der Grenze zwischen zwei Stoffen kann es die Richtung ändern, das kommt später.</li>
<li><b>Sehr schnell:</b> knapp 300 000 km pro Sekunde. Von der Sonne zur Erde braucht das Licht gut 8 Minuten.</li>
<li><b>Lichtbündel:</b> Eine Lichtquelle sendet in alle Richtungen, das Licht läuft auseinander (divergent). Eine Blende lässt nur einen Teil durch. Mit einem schmalen Spalt wird das Bündel fast parallel.</li>
<li><b>Typische Fehlvorstellungen:</b> Licht „füllt“ den Raum wie Luft. Licht bleibt in der Lampe, bis es hell ist. Nur dort, wo es hell aussieht, ist Licht.</li></ul></div>

<div class="box"><h3>Das Lichtstrahlenmodell {chip(5)}</h3><ul>
<li>Einen Lichtstrahl gibt es in Wirklichkeit nicht. Auch das schmalste Lichtbündel hat eine Breite.</li>
<li>Das Modell zeigt nur Weg und Richtung. Helligkeit und Farbe zeigt es nicht.</li>
<li>Gute Frage an die Klasse: Was stimmt am Modell, was ist vereinfacht, was fehlt? So bewertet das Buch auf S. 32 Modelle.</li>
<li><b>Typische Fehlvorstellung:</b> Der gezeichnete Strahl sei das, was man im Versuch sieht.</li></ul></div>

<div class="box"><h3>Tipps zum Versuch {chip(3)}</h3><ul>
<li>Raum abdunkeln, sonst ist der Lichtpunkt kaum zu sehen.</li>
<li>Ray-Box, Blende und Schirm an einer Tischkante oder einem Lineal ausrichten. Dann finden die Gruppen den Lichtpunkt schneller.</li>
<li>Beim seitlichen Verschieben verschwindet der Lichtpunkt, weil das Loch nicht mehr auf der geraden Linie liegt. Das ist der Kern des Versuchs.</li>
<li>Zusatz für schnelle Gruppen: eine zweite Blende dazwischen. Der Punkt erscheint nur, wenn beide Löcher auf einer Linie liegen.</li></ul></div>

<div class="box"><h3>Sichtbare Lichtwege {chip(6)}</h3><ul>
<li>Ein Lichtbündel sieht man von der Seite nur, wenn Staub, Nebel oder Rauch einen Teil des Lichts zum Auge streuen. Das knüpft an Leitfrage 2 an.</li>
<li>Sonnenstrahlen durch Wolkenlücken wirken fächerförmig. Eigentlich laufen sie fast parallel. Das Auffächern ist ein Perspektiv-Effekt wie bei Bahngleisen.</li>
<li>Laser nie auf Augen richten.</li></ul></div>

<div class="box"><h3>Warum nicht um die Ecke? {chip(7)}</h3><ul>
<li>Schall hört man um die Ecke, Licht sieht man nicht um die Ecke. Das ist ein guter Vergleich für die Klasse.</li>
<li>Um die Ecke sehen geht nur, wenn etwas das Licht umlenkt: Spiegel, Periskop, Handykamera.</li></ul></div>

<div class="box"><h3>Ideen aus Erlebnis Physik 7–9</h3>
<table class="t"><tr><th style="width:90px">Seite</th><th>Idee und so geht's</th><th style="width:130px">Passt zu</th></tr>
<tr><td>S. 33 A</td><td><b>Teelicht durch einen Gummischlauch.</b> Durch den geraden Schlauch (etwa 15 cm) sieht man die Flamme, durch den gebogenen nicht.
Kurzer Einstieg oder Zusatz zum Versuch. Material: Teelicht, Feuerzeug, Gummischlauch.</td><td>Folie 2 oder 3</td></tr>
<tr><td>S. 33 B</td><td><b>Lichtwege sichtbar machen.</b> Kleine Löcher in Alufolie stechen, damit die Handylampe abdecken, Raum abdunkeln. Rauch von einem
ausgepusteten Teelicht macht die geraden Lichtwege sichtbar. Vorsicht Rauchmelder, Kreidestaub oder ein Wassersprüher gehen auch.</td><td>Folie 4 und 6</td></tr>
<tr><td>S. 32</td><td><b>Modelle bewerten.</b> Was am Modell stimmt, was vereinfacht ist und was fehlt. Passt zum Lichtstrahlenmodell.</td><td>Folie 5</td></tr></table></div>
"""

F3_AB = f"""
<div class="box"><h3>Versuchsblatt Ray-Box und Blenden {chip(3)}</h3>
<a class="btn" href="Materialien/Lichtausbreitung und Blende W05.pdf">PDF öffnen</a><a class="btn" href="Materialien/Lichtausbreitung und Blende W05 – 2 auf 1.pdf">Kopiervorlage 2 auf 1</a>
<p><b>Lösung:</b> Der Lichtpunkt erscheint nur, wenn das Loch genau auf der geraden Linie zwischen Lampe und Schirm liegt. Wird die Blende seitlich verschoben,
verschwindet er. Lücken: <b>geradlinig</b>, <b>gerade Linie</b>.</p></div>
<div class="box"><h3>Strahlenlabor</h3>
<a class="btn" href="Strahlenlabor Lichtausbreitung.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Zum Zeigen, was im Versuch nicht geht: Blende 2 dazuschalten, Teelicht durch geraden und gebogenen Schlauch, Spaltbreite ändern, Lichtweg im Nebel, Verkehrsspiegel. Auch für zu Hause geeignet.</p></div>"""

F3_SCHRITTE = [
    ("Einstieg", "Ball hinter der Mauer, Leitfrage 3, Vermutungen.", [1, 2]),
    ("Versuch", "Ray-Box und Blende in Gruppen, Versuchsblatt.", [3]),
    ("Erklären", "Lichtbündel, Blende, Lichtstrahlenmodell.", [4, 5]),
    ("Alltag", "Beispiele mündlich, Frage zum Nebel.", [6]),
    ("Antwort und Check", "Antwort auf Leitfrage 3 ins Heft, Handzeichen, Lösung.", [7, 8, 9]),
]

# ====================================================================== Leitfrage 4
F4_ALLTAG = tabellenfolie("Schatten im Alltag", [
    ("Flutlicht im Stadion", "jeder Spieler hat vier Schatten", "Vier Masten sind vier Lichtquellen. Jede erzeugt einen Schatten."),
    ("OP-Lampe", "fast kein Schatten auf dem Tisch", "Viele Lampen leuchten aus vielen Richtungen in jeden Schatten hinein."),
    ("Sonne an einem klaren Tag", "dunkler, fast scharfer Schatten", "Es gibt nur eine Lichtquelle, und sie ist sehr weit weg."),
    ("bewölkter Tag", "kaum ein Schatten", "Die ganze Wolkendecke leuchtet, das Licht kommt von überall."),
    ("Hand unter Schreibtisch- und Deckenlampe", "zwei Schatten, in der Mitte dunkler", "Wo beide Lampen verdeckt sind, ist Kernschatten, sonst Halbschatten."),
], frage="Du stehst im Halbschatten. Wie viele Lampen kannst du von dort sehen?")

F4 = [
    basis(31), basis(32),
    blatt("Kern- und Halbschatten W06.pdf", "w06", "Versuchsblatt austeilen · Versuch in Gruppen"),
    basis(34), basis(36), F4_ALLTAG,
    basis(39), basis(40), basis(41),
]

F4_MATERIAL = {
    "demo": [],
    "schueler": [("Ray-Box mit Stromanschluss", "1×", "Lampenseite zum Körper"),
                 ("zweite Lichtquelle", "1×", "Leuchtbox oder zweite Ray-Box, an die Buchse am Tisch"),
                 ("weißes Blatt Papier", "1×", "als Bildwand gefaltet"),
                 ("undurchsichtiger Körper", "1×", "z. B. Glühbirnenpackung")],
    "hinweis": "Raum abdunkeln. Leitfrage 4 ist für zwei Wochen geplant (W06–07).",
}

F4_HG = f"""
<div class="box"><h3>Schattenraum und Schattenbild {chip(4)}</h3><ul>
<li>Ein Schatten ist kein Ding, sondern ein Gebiet ohne Licht. Der Schattenraum ist dreidimensional, das Schattenbild ist nur der Teil, der auf eine Fläche trifft.</li>
<li><b>Größe:</b> Je näher der Körper an der Lampe steht, desto größer wird das Schattenbild. Man sieht es an den geraden Linien von der Lampe über die Ränder des Körpers.
Das Buch zeigt das auf S. 34 an einer Dinosaurier-Figur.</li>
<li><b>Typische Fehlvorstellungen:</b> Der Schatten sei ein dunkles Abbild mit allen Einzelheiten. Der Schatten gehöre zum Körper und sei auch im Dunkeln da.</li></ul></div>

<div class="box"><h3>Kern- und Halbschatten {chip(5, 7)}</h3><ul>
<li><b>Zwei Lampen:</b> Im Kernschatten kommt von keiner Lampe Licht an, im Halbschatten von einer. Bei mehr Lampen gibt es mehrere, unterschiedlich helle Halbschatten.</li>
<li><b>Ausgedehnte Lichtquellen</b> (Leuchtstoffröhre, Fenster, Sonne) kann man sich als viele kleine Lichtquellen nebeneinander denken. Dann geht der Schatten ohne Stufe
ins Helle über, der Rand wird weich. Eine punktförmige Lichtquelle gibt einen scharfen Rand.</li>
<li><b>Blick von der Wand zur Lampe:</b> Aus dem Kernschatten sieht man keine Lampe, aus dem Halbschatten eine, aus dem hellen Bereich beide. Das beantwortet die Frage auf Folie 6.</li>
<li>Die Sonne ist auch eine ausgedehnte Lichtquelle. Das ist die Brücke zu Leitfrage 5 (Sonnen- und Mondfinsternis).</li>
<li><b>Typische Fehlvorstellung:</b> Der Halbschatten sei „ein halber Schatten“ des Körpers, also nur seine halbe Größe.</li></ul></div>

<div class="box"><h3>Tipps zum Versuch {chip(3)}</h3><ul>
<li>Raum abdunkeln. Den Körper etwa 10 cm vor die Lampe stellen, dann ist der Schatten gut zu sehen.</li>
<li>Die beiden Lampen dicht nebeneinander stellen. Rücken sie weiter auseinander, rücken auch die Schatten auseinander.</li>
<li>Überlappen sich die beiden Schatten nicht mehr, gibt es keinen Kernschatten mehr, nur zwei Halbschatten. Gute Zusatzfrage für schnelle Gruppen.</li></ul></div>

<div class="box"><h3>Schatten im Alltag {chip(6)}</h3><ul>
<li>Im Stadion stehen die Flutlichtmasten in den Ecken. Deshalb hat jeder Spieler vier Schatten, das Buch zeigt das auf S. 35.</li>
<li>Die OP-Lampe hat viele Einzellampen in einem großen Ring. So wirft die Hand des Arztes keinen dunklen Schatten auf die Wunde.</li></ul></div>

<div class="box"><h3>Ideen aus Erlebnis Physik 7–9</h3>
<table class="t"><tr><th style="width:90px">Seite</th><th>Idee und so geht's</th><th style="width:130px">Passt zu</th></tr>
<tr><td>S. 34</td><td><b>Schattengröße.</b> Eine Figur zwischen Lampe und Wand verschieben. Näher an der Lampe wird der Schatten größer. Gut als Je-desto-Satz.</td><td>Folie 4</td></tr>
<tr><td>S. 35</td><td><b>Flutlicht.</b> Ein Foto eines Spielers mit vier Schatten als Gesprächsanlass: Woher kommen die Schatten?</td><td>Folie 6</td></tr>
<tr><td>S. 36–37</td><td><b>Schattenversuche.</b> Taschenlampe und Radiergummi auf gefaltetem Papier (Schattenbild). Zwei Taschenlampen auf einen Mitschüler an der Wand:
Wann gibt es zwei Schatten, wann nur einen? Geht auch als Demo vorne, wenn Ray-Boxen fehlen.</td><td>Folie 3 bis 5</td></tr></table></div>
"""

F4_AB = f"""
<div class="box"><h3>Versuchsblatt Kern- und Halbschatten {chip(3)}</h3>
<a class="btn" href="Materialien/Kern- und Halbschatten W06.pdf">PDF öffnen</a>
<p><b>Lösung Versuch 1:</b> Je näher der Körper an der Lampe steht, desto größer und unschärfer wird der Schatten. Lücken: <b>undurchsichtiger Körper</b>,
<b>Lichtquelle</b>, <b>hinter</b>.</p>
<p><b>Lösung Versuch 2:</b> Ein zweiter, versetzter Schatten kommt dazu. In der Mitte bleibt es am dunkelsten (Kernschatten), an den Rändern wird es heller (Halbschatten).
Lücken: <b>lichtundurchlässigen Körper</b>, <b>Schatten</b>, <b>überlagern</b>, <b>Halbschattengebiete</b>, <b>Kernschattengebiete</b>.</p></div>
<div class="box"><h3>Schattenlabor</h3>
<a class="btn" href="Schattenlabor Halbschatten.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Passt nach Folie 5: Im Labor Folie 3 bis 5 zeigen (zwei Lichtpunkte, Kern- und Halbschatten, Regler für Lampengröße und Abstände). Die Lampengröße kann man mit der Ray-Box nicht verändern. Folie 6 zeigt die vier Flutlicht-Schatten im Stadion (passt zu unserer Alltagsfolie), Folie 7 die Finsternisse als Ausblick.</p></div>"""

F4_SCHRITTE = [
    ("Einstieg", "Eine Lampe, zwei Lampen: Was ist anders? Leitfrage 4.", [1, 2]),
    ("Versuch", "In Gruppen, erst eine Lichtquelle, dann zwei. Versuchsblatt.", [3]),
    ("Erklären", "Schattenraum und Schattenbild, Kern- und Halbschatten zeichnen.", [4, 5]),
    ("Alltag", "Beispiele mündlich, Frage nach dem Halbschatten.", [6]),
    ("Antwort und Check", "Antwort auf Leitfrage 4 ins Heft, Handzeichen, Lösung.", [7, 8, 9]),
]

# ====================================================================== bauen
bau_stunde("Optik – Leitfrage 3 – Stunde.html", "Optik: Warum können wir nicht um die Ecke sehen?",
           "Klasse 7c · Physik · Leitfrage 3 · Lichtausbreitung und Blende (W05)",
           ["Versuchsblatt: Kopiervorlage „2 auf 1“, halbe Klassenstärke drucken und in der Mitte durchschneiden.",
            "Folien und Lösungen: nicht drucken."],
           F3_MATERIAL, F3_SCHRITTE, F3, F3_HG, F3_AB)
bau_stunde("Optik – Leitfrage 4 – Stunde.html", "Optik: Warum hat ein Schatten manchmal weiche Ränder?",
           "Klasse 7c · Physik · Leitfrage 4 · Kern- und Halbschatten (W06–07)",
           ["Versuchsblatt: Seite 1, eins pro Schüler. Für „2 auf 1“ ist es mit zwei Versuchen zu lang.",
            "Folien und Lösungen: nicht drucken."],
           F4_MATERIAL, F4_SCHRITTE, F4, F4_HG, F4_AB)

if "export" in sys.argv:
    zwei_auf_eins("lichtausbreitung-blende.html", "Lichtausbreitung und Blende W05 – 2 auf 1.pdf", feld="40mm")
    O3 = ICL / "F3 Lichtausbreitung und Blende (W05)"
    O4 = ICL / "F4 Kern- und Halbschatten (W06-07)"
    shutil.copy(MAT / "Lichtausbreitung und Blende W05.pdf", O3 / "Arbeitsblatt F3.pdf")
    shutil.copy(MAT / "Lichtausbreitung und Blende W05 – 2 auf 1.pdf", O3 / "Arbeitsblatt F3 – Kopiervorlage 2 auf 1.pdf")
    shutil.copy(MAT / "Kern- und Halbschatten W06.pdf", O4 / "Arbeitsblatt F4.pdf")
    materialliste(O3, "W05", "F3 — Lichtausbreitung und Blende", F3_MATERIAL)
    materialliste(O4, "W06–07", "F4 — Kern- und Halbschatten", F4_MATERIAL)
    exportiere(F3, O3, "Folien F3.pdf", "Arbeitsblatt F3.pdf", "Stunde Leitfrage 3.html", "Optik – Leitfrage 3 – Stunde.html",
               {"Materialien/Lichtausbreitung und Blende W05.pdf": "Arbeitsblatt F3.pdf",
                "Strahlenlabor Lichtausbreitung.html": "../Labore/Strahlenlabor Lichtausbreitung.html", "Optik-Labore.html": "../Labore/Optik-Labore.html",
                "Materialien/Lichtausbreitung und Blende W05 – 2 auf 1.pdf": "Arbeitsblatt F3 – Kopiervorlage 2 auf 1.pdf"})
    exportiere(F4, O4, "Folien F4.pdf", "Arbeitsblatt F4.pdf", "Stunde Leitfrage 4.html", "Optik – Leitfrage 4 – Stunde.html",
               {"Materialien/Kern- und Halbschatten W06.pdf": "Arbeitsblatt F4.pdf",
                "Schattenlabor Halbschatten.html": "../Labore/Schattenlabor Halbschatten.html", "Optik-Labore.html": "../Labore/Optik-Labore.html"})
