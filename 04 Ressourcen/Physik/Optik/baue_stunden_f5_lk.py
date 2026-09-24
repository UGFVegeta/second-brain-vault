#!/usr/bin/env python3
"""Stunden-HTMLs Leitfrage 5 (Mondphasen, Finsternisse) und Lochkamera mit Rückblick Optik I.
python3 baue_stunden_f5_lk.py   -> nur die HTMLs im Vault (Export nach iCloud erst nach Freigabe)"""
import re
from stunde_vorlage import basis, blatt, chip, tabellenfolie, bau_stunde

# ====================================================================== Leitfrage 5
F5_ALLTAG = tabellenfolie("Mond und Finsternis im Alltag", [
    ("Halbmond am Nachmittag", "Mond am hellen Himmel", "Die Sonne beleuchtet ihn auch tagsüber. Der zunehmende Halbmond steht nachmittags schon am Himmel."),
    ("Vollmond am Abend", "Er geht auf, wenn die Sonne untergeht", "Er steht der Sonne genau gegenüber."),
    ("Blutmond", "Mond bei Mondfinsternis rötlich", "Die Lufthülle der Erde lenkt etwas rotes Licht in den Erdschatten."),
    ("Finsternisbrille", "Sonnenfinsternis nur mit Schutz ansehen", "Das Sonnenlicht kann die Netzhaut dauerhaft schädigen."),
], frage="Warum darf man eine Mondfinsternis ohne Brille ansehen, eine Sonnenfinsternis aber nicht?")

F5 = [
    basis(42), basis(43), basis(45),
    blatt("Mondphasen im Modell W08.pdf", "w08", "Versuchsblatt austeilen · Versuch in Paaren"),
    basis(47), basis(49), basis(51), F5_ALLTAG,
    basis(52), basis(53), basis(54),
]

F5_MATERIAL = {
    "demo": [("Tellurium beleuchtet (Phywe)", "1×", "Mondphasen und Finsternisse vorne zeigen"),
             ("helle Lampe ohne Schirm", "1×", "als Sonne für den Schülerversuch, mitten im Raum oder vorne")],
    "schueler": [("Styroporkugel, etwa 5 cm", "1×", "pro Paar, einer dreht sich, einer beobachtet mit"),
                 ("Bleistift oder Schaschlikspieß", "1×", "als Griff für die Kugel")],
    "hinweis": "Raum gut abdunkeln. Für die Lochkamera in der nächsten Stunde ankündigen: Chipsdose, Transparent- oder Butterbrotpapier, schwarzer Zeichenkarton, Schere, Kleber mitbringen.",
}

F5_SCHRITTE = [
    ("Einstieg", "Vier Wochen Mond, Leitfrage 5, Vermutungen.", [1, 2]),
    ("Tellurium", "Vorne am Tellurium zeigen, wo der Mond steht. Folie dazu.", [3]),
    ("Versuch", "Kopf, Kugel, Lampe in Paaren, Versuchsblatt.", [4]),
    ("Mondphasen", "Phasen von der Erde aus, 29,5 Tage.", [5]),
    ("Finsternisse", "Am Tellurium oder im Mondlabor, dann Folien.", [6, 7]),
    ("Alltag, Antwort, Check", "Alltag mündlich, Antwort ins Heft, Handzeichen.", [8, 9, 10, 11]),
]

F5_HG = f"""
<div class="box"><h3>Wo steht der Mond? {chip(3)}</h3><ul>
<li>Der Mond läuft in etwa 27,3 Tagen einmal um die Erde. Von Neumond bis Neumond dauert es 29,5 Tage, weil die Erde in dieser Zeit ein Stück um die Sonne weiterwandert.</li>
<li><b>Umlaufsinn:</b> Von Norden aus gesehen läuft der Mond gegen den Uhrzeigersinn. Liegt die Sonne in der Zeichnung links, steht der zunehmende Mond unten, der abnehmende oben.</li>
<li><b>Tellurium:</b> Zeigt Mondphasen und beide Finsternisse direkt vorne. Den Raum gut abdunkeln, dann ist die beleuchtete Hälfte klar zu sehen.</li>
<li><b>Typische Fehlvorstellungen:</b> Die Phasen entstehen durch den Erdschatten. Der Mond leuchtet selbst. Bei Neumond ist der Mond „weg“.</li></ul></div>

<div class="box"><h3>Tipps zum Versuch {chip(4)}</h3><ul>
<li>Eine helle Lampe ohne Schirm, sonst sind die Phasen blass. Raum ganz abdunkeln.</li>
<li>Die Kugel etwas höher als den Kopf halten. Sonst steht sie bei „Lampe hinter dir“ im Kopfschatten, das ist dann eine Mondfinsternis. Das kann man gezielt als Zusatz zeigen.</li>
<li>Drehen nach links, also gegen den Uhrzeigersinn. Dann stimmen die Phasen mit der Nordhalbkugel überein: Lampe rechts von dir heißt zunehmender Halbmond, rechte Seite hell.</li>
<li>Das Buch zeigt auf S. 40 einen ähnlichen Versuch mit Globus, Lampe und einer Papierkugel am Faden.</li></ul></div>

<div class="box"><h3>Mondphasen {chip(5)}</h3><ul>
<li>Faustregel für die Nordhalbkugel: rechts hell heißt zunehmend, links hell heißt abnehmend. Auf der Südhalbkugel ist es umgekehrt.</li>
<li>Der zunehmende Halbmond steht am Nachmittag und Abend am Himmel, der abnehmende am Morgen. Der Vollmond geht beim Sonnenuntergang auf.</li></ul></div>

<div class="box"><h3>Finsternisse {chip(6, 7)}</h3><ul>
<li>Die Mondbahn ist um etwa 5° gegen die Erdbahn geneigt. Deshalb gibt es nicht bei jedem Neumond eine Sonnenfinsternis und nicht bei jedem Vollmond eine Mondfinsternis. Im Mondlabor lässt sich der Mond dafür nach oben und unten schieben.</li>
<li>Der Kernschatten des Mondes ist auf der Erde höchstens rund 270 km breit. Eine totale Sonnenfinsternis sieht man deshalb nur in einem schmalen Streifen, eine Mondfinsternis dagegen überall, wo gerade Nacht ist.</li>
<li><b>Blutmond:</b> Die Lufthülle der Erde lenkt etwas Sonnenlicht in den Kernschatten. Dabei bleibt vor allem rotes Licht übrig, wie beim Sonnenuntergang.</li>
<li><b>Sicherheit:</b> Sonnenfinsternis nie ohne Finsternisbrille ansehen, auch keine normale Sonnenbrille. Eine Lochkamera ist ein sicherer Weg. Eine Mondfinsternis kann man ohne Schutz ansehen.</li></ul></div>

<div class="box"><h3>Mondlabor</h3>
<a class="btn" href="Mondlabor Mondphasen und Finsternisse.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Mondbahn mit Regler für den Tag seit Neumond und der Ansicht von der Erde, euer Kugelversuch, Sonnenfinsternis mit schiefer Mondbahn, Mondfinsternis mit Blutmond. Auch für zu Hause.</p></div>
"""

F5_AB = f"""
<div class="box"><h3>Versuchsblatt Mondphasen im Modell {chip(4)}</h3>
<a class="btn" href="Materialien/Mondphasen im Modell W08.pdf">PDF öffnen</a><a class="btn" href="Materialien/Mondphasen im Modell W08 – 2 auf 1.pdf">Kopiervorlage 2 auf 1</a>
<p><b>Lösung:</b> zur Lampe: Neumond (ganz dunkel). Lampe rechts: zunehmender Halbmond (rechts hell). Lampe hinter dir: Vollmond. Lampe links: abnehmender Halbmond (links hell).
Lücken: <b>Hälfte</b>, <b>unterschiedlich viel</b>, <b>Mondfinsternis</b>.</p></div>
<div class="box"><h3>Mondlabor</h3>
<a class="btn" href="Mondlabor Mondphasen und Finsternisse.html">Labor öffnen</a>
<p>Dein H5P „Mondphasen Klasse 7“ liegt unter <code>04 Ressourcen/Physik/Mondphasen/H5P/</code> und passt als Wiederholung.</p></div>"""

# ====================================================================== Lochkamera
def ohne_hausaufgabe(h):
    return h.replace("Hausaufgabe: Wir bauen eine Lochkamera", "Wir bauen eine Lochkamera")


LK_ALLTAG = tabellenfolie("Lochkamera im Alltag", [
    ("Lichtflecken unter einem Baum", "runde Flecken", "Jede Lücke im Laub ist eine Lochkamera. Die Flecken sind Bilder der runden Sonne."),
    ("dunkles Zimmer, Loch im Rollladen", "die Straße steht an der Wand auf dem Kopf", "Das Zimmer wirkt wie eine riesige Lochkamera (Camera obscura)."),
    ("Sonnenfinsternis beobachten", "eine kleine Sichel auf dem Papier", "Mit einem Loch im Karton sieht man die Sonne, ohne hineinzuschauen."),
], frage="Warum sind die Flecken unter dem Baum rund, obwohl die Lücken im Laub eckig sind?")

LK = [
    basis(56), ohne_hausaufgabe(basis(57)),
    blatt("Lochkamera W09.pdf", "w09", "Versuchsblatt austeilen · Versuch mit der eigenen Lochkamera"),
    LK_ALLTAG, basis(61), basis(60),
]

LK_MATERIAL = {
    "demo": [("Kerze mit Feuerzeug", "1×", "helles Motiv im abgedunkelten Raum"),
             ("Alufolie und Nadel", "1 Rolle", "für Blenden mit kleinen und großen Löchern"),
             ("Nagel (etwa 1 mm)", "mehrere", "für das Loch im Dosenboden, falls jemand keinen hat")],
    "schueler": [("runde Chipsdose", "1×", "mitgebracht"),
                 ("Transparent- oder Butterbrotpapier", "1 Stück", "mitgebracht"),
                 ("schwarzer Zeichenkarton", "1 Bogen", "etwas größer als der Mantel der Dose"),
                 ("Zirkel, Schere, Lineal, Kleber oder Tesa", "je 1", "aus dem Mäppchen")],
    "hinweis": "Ein paar Chipsdosen und Karton als Reserve bereithalten. Zum Beobachten: helles Fenster oder Kerze im abgedunkelten Raum.",
}

LK_SCHRITTE = [
    ("Einstieg", "Im Lochkameralabor: Warum steht das Bild auf dem Kopf? Dann Folie.", [1]),
    ("Bauen", "Lochkamera nach Anleitung bauen.", [2]),
    ("Versuch", "Mit der eigenen Lochkamera beobachten, Versuchsblatt.", [3]),
    ("Alltag", "Beispiele mündlich, Sicheln auf dem Boden.", [4, 5]),
    ("Rückblick Optik I", "Die fünf Leitfragen in einem Satz.", [6]),
]

LK_HG = f"""
<div class="box"><h3>Die Lochkamera {chip(1)}</h3><ul>
<li>Jeder Punkt des Gegenstands schickt Licht durch das Loch und erzeugt einen kleinen Lichtfleck auf dem Schirm. Alle Flecken zusammen ergeben das Bild.</li>
<li><b>Bildgröße:</b> Bild : Gegenstand = Bildweite : Gegenstandsweite (Strahlensatz). Das kommt in Klasse 7 nur als Je-desto-Satz vor.</li>
<li><b>Schärfe:</b> Ein großes Loch ist wie viele kleine Löcher nebeneinander. Die Bilder überlagern sich, das Bild wird heller, aber unscharf. Gleicher Gedanke wie beim Halbschatten.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Bild wandert als Ganzes durch das Loch. Das Loch dreht das Bild um. Ein größeres Loch macht das Bild größer.</li></ul></div>

<div class="box"><h3>Tipps zum Bau und Versuch {chip(2, 3)}</h3><ul>
<li>Das Loch mit dem Nagel von außen stechen und die Ränder glätten. Ein Stück Alufolie mit Nadelloch vor ein zu großes Loch kleben.</li>
<li>Am besten gegen ein helles Fenster schauen, mit einer Jacke über Kopf und Dose, damit kein Streulicht aufs Papier fällt.</li>
<li>Kerzen nur mit Aufsicht, Haare zurück.</li></ul></div>

<div class="box"><h3>Sicheln unter dem Baum {chip(5)}</h3><ul>
<li>Jede Lücke im Blätterdach wirkt als Lochblende. Weil das Bild auf dem Kopf steht, sind die Sicheln auf dem Boden gegenüber der Sonnensichel um 180° gedreht.</li>
<li>An normalen Tagen sind die Flecken rund oder, bei schräg stehender Sonne, oval.</li></ul></div>

<div class="box"><h3>Rückblick {chip(6)}</h3><ul>
<li>Alle fünf Antworten stecken in einem Satz: Licht breitet sich geradlinig aus und wird an Körpern zurückgeworfen, verschluckt oder durchgelassen.</li>
<li>Gute Gelegenheit, die Labore für die Wiederholung zu Hause zu nennen.</li></ul></div>

<div class="box"><h3>Lochkameralabor</h3>
<a class="btn" href="Lochkameralabor.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Strahlengang von Flammenspitze und Fuß, Regler für Abstände und Lochgröße mit Bildgröße, Unschärfe und Helligkeit, ein, zwei oder viele Löcher, Sonnenbilder unter dem Baum.</p></div>
"""

LK_AB = f"""
<div class="box"><h3>Versuchsblatt Lochkamera {chip(3)}</h3>
<a class="btn" href="Materialien/Lochkamera W09.pdf">PDF öffnen</a><a class="btn" href="Materialien/Lochkamera W09 – 2 auf 1.pdf">Kopiervorlage 2 auf 1</a>
<p><b>Lösung:</b> Das Bild steht auf dem Kopf. Je weiter das Papier vom Loch entfernt ist, desto größer wird das Bild. Ein kleineres Loch macht das Bild schärfer, aber dunkler.
Lücken: <b>geradlinig</b>, <b>umgekehrtes</b>, <b>größer</b>, <b>schärfer</b>, <b>dunkler</b>.</p></div>
<div class="box"><h3>Lochkameralabor</h3>
<a class="btn" href="Lochkameralabor.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a></div>"""

bau_stunde("Optik – Leitfrage 5 – Stunde.html", "Optik: Warum sieht der Mond nicht immer gleich aus?",
           "Klasse 7c · Physik · Leitfrage 5 · Mondphasen und Finsternisse · voraussichtlich Do 15.10.2026",
           ["Versuchsblatt: Kopiervorlage „2 auf 1“, halbe Klassenstärke drucken und in der Mitte durchschneiden.",
            "Folien und Lösungen: nicht drucken."],
           F5_MATERIAL, F5_SCHRITTE, F5, F5_HG, F5_AB)
bau_stunde("Optik – Lochkamera – Stunde.html", "Optik: Die Lochkamera und Rückblick",
           "Klasse 7c · Physik · Lochkamera, Rückblick Optik I · voraussichtlich Do 22.10.2026",
           ["Versuchsblatt: Kopiervorlage „2 auf 1“, halbe Klassenstärke drucken und in der Mitte durchschneiden.",
            "Folien und Lösungen: nicht drucken."],
           LK_MATERIAL, LK_SCHRITTE, LK, LK_HG, LK_AB)
