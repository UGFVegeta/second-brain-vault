#!/usr/bin/env python3
"""Stunden-HTMLs Optik II, erste vier Doppelstunden nach den Herbstferien:
Reflexionsgesetz (F6), Spiegelbild (F6 Abschluss), Lichtbrechung (F7), Sammel- und Zerstreuungslinse (F8 Teil 1).
python3 baue_stunden_optik2.py          -> HTMLs im Vault
python3 baue_stunden_optik2.py export   -> zusätzlich Folien-PDF, Materialliste, Gesamt, Stunden-HTML nach iCloud"""
import shutil, sys
from stunde_vorlage import basis2, blatt, chip, tabellenfolie, bau_stunde

LAB = lambda datei, name, text: (f'<div class="box"><h3>{name}</h3><a class="btn" href="{datei}">Labor öffnen</a>'
                                 f'<a class="btn" href="Optik-Labore.html">Alle Labore</a><p>{text}</p></div>')

# ====================================================================== 1 Reflexionsgesetz
R_ALLTAG = tabellenfolie("Reflexion im Alltag", [
    ("Rückspiegel im Auto", "die Straße hinter dir", "Licht von hinten wird am Spiegel zum Fahrer reflektiert."),
    ("Periskop im U-Boot", "über die Wasseroberfläche schauen", "Zwei schräge Spiegel lenken das Licht zweimal um."),
    ("glatter See am Morgen", "ein klares Spiegelbild der Berge", "Die glatte Oberfläche reflektiert regelmäßig. Bei Wellen wird das Licht gestreut."),
    ("Billard an der Bande", "die Kugel prallt im gleichen Winkel ab", "Wie beim Licht: Einfallswinkel = Reflexionswinkel."),
], frage="Warum siehst du dich in einem Spiegel, aber nicht in einem weißen Blatt Papier?")

R = [basis2(2), basis2(3),
     blatt("Reflexionsgesetz W10.pdf", "w10", "Versuchsblatt austeilen · Versuch in Gruppen"),
     basis2(5), R_ALLTAG]

R_MAT = {"demo": [("Spiegel und Taschenlampe", "1×", "für den Einstieg, Licht an die Decke lenken")],
         "schueler": [("Optikleuchte mit Einspaltblende", "1×", "oder Ray-Box mit einem Spalt"),
                      ("ebener Spiegel", "1×", "an die Grundlinie der Kreisscheibe"),
                      ("Kreisscheibe mit Winkeleinteilung", "1×", "")],
         "hinweis": "Raum abdunkeln. Den Strahl genau auf den Mittelpunkt der Scheibe richten."}

R_SCHRITTE = [("Einstieg", "Spiegel und Hand heben, Leitfrage 6, Vermutungen.", [1, 2]),
              ("Versuch", "Kreisscheibe in Gruppen, sechs Messungen, Versuchsblatt.", [3]),
              ("Reflexionsgesetz", "Merksatz, Winkel zum Lot.", [4]),
              ("Alltag", "Beispiele mündlich, Frage zum weißen Blatt.", [5])]

R_HG = f"""
<div class="box"><h3>Das Reflexionsgesetz {chip(4)}</h3><ul>
<li>Einfallswinkel und Reflexionswinkel werden immer zum <b>Lot</b> gemessen, also zur Senkrechten auf dem Spiegel. Einfallender Strahl, Lot und reflektierter Strahl liegen in einer Ebene.</li>
<li>Das Gesetz gilt an jeder Stelle einer Fläche. Bei einer rauen Fläche zeigt das Lot an jeder Stelle in eine andere Richtung, deshalb wird das Licht in viele Richtungen zurückgeworfen (Streuung aus Leitfrage 2).</li>
<li><b>Typische Fehlvorstellungen:</b> Winkel werden zum Spiegel gemessen. Der Spiegel „schluckt“ bei großen Winkeln Licht.</li></ul></div>
<div class="box"><h3>Tipps zum Versuch {chip(3)}</h3><ul>
<li>Den Spiegel genau an die Grundlinie legen, sonst weichen die Werte ab. Messwerte auf ± 1° sind normal.</li>
<li>Bei 0° läuft der Strahl in sich zurück. Guter Anlass für die Frage, wo das Lot ist.</li>
<li>Das Buch zeigt auf S. 45 A glatte und zerknitterte Alufolie im Vergleich. Passt als Zusatz zur Frage auf der Alltagsfolie.</li></ul></div>
{LAB("Spiegellabor Reflexion.html", "Spiegellabor", "Kreisscheibe mit Winkelregler, gekippter Spiegel mit Lot, Spiegelbild, Spiegelgröße, Spiegelschrift auf dem Krankenwagen.")}
"""
R_AB = f"""
<div class="box"><h3>Versuchsblatt Reflexionsgesetz {chip(3)}</h3>
<a class="btn" href="Materialien/Reflexionsgesetz W10.pdf">PDF öffnen</a><a class="btn" href="Materialien/Reflexionsgesetz W10 – 2 auf 1.pdf">Kopiervorlage 2 auf 1</a>
<p><b>Lösung:</b> In jeder Messung ist β gleich α (Beispiel 10°/10° bis 60°/60°, ± 1°). Lücken: <b>Reflexionswinkel</b>, <b>Lot</b>.</p></div>"""

# ====================================================================== 2 Spiegelbild
S_ALLTAG = tabellenfolie("Spiegelbilder im Alltag", [
    ("Krankenwagen", "AMBULANZ steht spiegelverkehrt", "Im Rückspiegel des Autos davor ist die Schrift richtig lesbar."),
    ("Schaufenster am Abend", "du siehst dich in der Scheibe", "Glas reflektiert einen kleinen Teil des Lichts. Ist es dahinter dunkel, fällt das auf."),
    ("zwei Spiegel in der Umkleide", "viele Bilder hintereinander", "Das Spiegelbild wird im zweiten Spiegel wieder gespiegelt."),
], frage="Warum steht „AMBULANZ“ vorne auf dem Krankenwagen spiegelverkehrt?")

SB = [basis2(9),
      blatt("Der Spiegel W11.pdf", "w11", "Arbeitsblatt austeilen"),
      S_ALLTAG, basis2(12), basis2(13), basis2(14)]

S_MAT = {"demo": [("Glasplatte, senkrecht aufgestellt", "1×", "zum Beispiel ein Bilderrahmenglas, Kanten abkleben"),
                  ("zwei gleiche Teelichter", "2", "eins brennt davor, eins steht aus hinter der Platte"),
                  ("Feuerzeug", "1×", "")],
         "schueler": [("Geodreieck und Bleistift", "1×", "zum Konstruieren auf dem Arbeitsblatt")],
         "hinweis": "Demo zum Spiegelbild: Das nicht brennende Teelicht hinter der Glasplatte scheint zu brennen, wenn es genau an der Bildstelle steht."}

S_SCHRITTE = [("Spiegelbild", "Demo mit Glasplatte und zwei Teelichtern, dann Folie.", [1]),
              ("Arbeitsblatt", "Wie groß muss der Spiegel sein? Konstruieren.", [2]),
              ("Alltag", "Spiegelschrift und Schaufenster.", [3]),
              ("Antwort und Check", "Antwort auf Leitfrage 6 ins Heft, Handzeichen, Lösung.", [4, 5, 6])]

S_HG = f"""
<div class="box"><h3>Das Spiegelbild {chip(1)}</h3><ul>
<li>Von jedem Punkt des Gegenstands gehen Strahlen zum Spiegel. Nach der Reflexion laufen sie auseinander, als kämen sie von einem Punkt hinter dem Spiegel. Das Auge verlängert sie geradlinig zurück: Dort sieht es den Bildpunkt.</li>
<li>Das Bild ist <b>virtuell</b>: Hinter dem Spiegel ist kein Licht, ein Schirm dort bliebe dunkel.</li>
<li>Der Spiegel vertauscht nicht links und rechts, sondern vorne und hinten. Das erklärt die Spiegelschrift.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Bild liegt auf der Spiegeloberfläche. Man sieht mehr von sich, wenn man zurücktritt.</li></ul></div>
<div class="box"><h3>Wie groß muss der Spiegel sein? {chip(2)}</h3><ul>
<li>Oberkante auf halber Höhe zwischen Auge und Scheitel, Unterkante auf halber Höhe zwischen Auge und Füßen. Zusammen ist das die halbe Körpergröße.</li>
<li>Der Abstand zum Spiegel spielt keine Rolle, weil das Bild im gleichen Maß mit zurückweicht. Im Spiegellabor lässt sich das mit dem Abstandsregler zeigen.</li></ul></div>
{LAB("Spiegellabor Reflexion.html", "Spiegellabor", "Spiegelbild mit verschiebbarer Kerze und Auge, Spiegelgröße mit Abstandsregler, Krankenwagen direkt und im Rückspiegel.")}
"""
S_AB = f"""
<div class="box"><h3>Arbeitsblatt Der Spiegel {chip(2)}</h3>
<a class="btn" href="Materialien/Der Spiegel W11.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Spiegelbild gleich groß und gleich weit hinter der Wand. Spiegel halb so groß wie die Person, Oberkante auf halber Höhe zwischen Augen und Scheitel.
Lücken: <b>halb so groß</b>, <b>Augen</b>, <b>keine Rolle</b>.</p></div>"""

# ====================================================================== 3 Lichtbrechung
B_ALLTAG = tabellenfolie("Brechung im Alltag", [
    ("Schwimmbecken", "es sieht flacher aus, als es ist", "Das Licht vom Boden wird an der Oberfläche vom Lot weg gebrochen."),
    ("Münze im Becher", "sie taucht auf, wenn Wasser hineinkommt", "Das gebrochene Licht gelangt über den Rand ins Auge."),
    ("Reiher beim Fischen", "er zielt unter den Fisch, den er sieht", "Der Fisch ist tiefer, als er von oben aussieht."),
    ("Flimmern über heißer Straße", "die Luft scheint zu wabern", "Warme und kalte Luft brechen das Licht verschieden stark."),
], frage="Warum sieht ein Schwimmbecken flacher aus, als es ist?")

BR = [basis2(15), basis2(16),
      blatt("Lichtbrechung W12.pdf", "w12", "Versuchsblatt austeilen · Versuch in Gruppen"),
      basis2(18), basis2(20), B_ALLTAG, basis2(21), basis2(22), basis2(23)]

B_MAT = {"demo": [("Glas mit Wasser und Strohhalm", "1×", "für den Einstieg"),
                  ("Tasse und Münze", "1×", "Münzversuch, Wasser langsam eingießen")],
         "schueler": [("Ray-Box mit einem Spalt", "1×", ""),
                      ("Halbzylinder aus Glas oder Acryl", "1×", ""),
                      ("Winkelscheibe", "1×", "")],
         "hinweis": "Raum abdunkeln. Der Strahl muss genau durch den Mittelpunkt gehen, sonst wird er an der runden Seite zusätzlich gebrochen."}

B_SCHRITTE = [("Einstieg", "Strohhalm im Glas, Leitfrage 7, Vermutungen.", [1, 2]),
              ("Versuch", "Halbzylinder in Gruppen, zwei Richtungen, Versuchsblatt.", [3]),
              ("Erklären", "Lichtbrechung und Richtung zum Lot.", [4, 5]),
              ("Alltag", "Münzversuch vorne, Beispiele mündlich.", [6]),
              ("Antwort und Check", "Antwort auf Leitfrage 7 ins Heft, Handzeichen, Lösung.", [7, 8, 9])]

B_HG = f"""
<div class="box"><h3>Lichtbrechung {chip(4, 5)}</h3><ul>
<li>Licht ist in Wasser etwa 25 % langsamer als in Luft, in Glas etwa 33 %. Je langsamer, desto „optisch dichter“ heißt der Stoff. Mit der Dichte in kg/m³ hat das nichts zu tun.</li>
<li>Richtwerte von Luft in Wasser: 30° → 22°, 45° → 32°, 60° → 41°. Von Luft in Glas: 30° → 19°, 45° → 28°.</li>
<li>Bei senkrechtem Einfall (0°) wird nichts gebrochen, das Licht wird nur langsamer.</li>
<li>Ein kleiner Teil des Lichts wird an jeder Grenzfläche reflektiert. Von Glas nach Luft gibt es ab etwa 42° gar keinen gebrochenen Strahl mehr (Totalreflexion). Das kommt beim Glasfaserkabel wieder.</li>
<li><b>Typische Fehlvorstellungen:</b> Der Strohhalm ist wirklich geknickt. Licht wird immer zum Lot hin gebrochen. Brechung passiert im Wasser statt an der Grenzfläche.</li></ul></div>
<div class="box"><h3>Tipps zum Versuch {chip(3)}</h3><ul>
<li>Der Strahl muss genau durch den Mittelpunkt der Scheibe gehen. Dann trifft er die runde Seite senkrecht und wird dort nicht noch einmal gebrochen.</li>
<li>Beim zweiten Versuch (von Glas in Luft) bei 50° kein gebrochener Strahl: nicht als Fehler werten, sondern als Frage für die nächste Stunde stehen lassen.</li></ul></div>
{LAB("Brechungslabor Lichtbrechung.html", "Brechungslabor", "Strohhalm im Glas, Halbzylinder in beiden Richtungen, Wasser, Glas und Diamant, Wellenfronten als Erklärung, Münze im Becher.")}
"""
B_AB = f"""
<div class="box"><h3>Versuchsblatt Lichtbrechung {chip(3)}</h3>
<a class="btn" href="Materialien/Lichtbrechung W12.pdf">PDF öffnen</a>
<p><b>Lösung (Glas, gerundet):</b> Luft → Glas: 10° → 7°, 20° → 13°, 30° → 19°, 40° → 25°, 50° → 31°. Glas → Luft: 10° → 15°, 20° → 31°, 30° → 49°, 40° → 75°, 50° → kein gebrochener Strahl.
Reflexionswinkel jeweils gleich dem Einfallswinkel. Lücken: <b>zum Lot hin</b>, <b>vom Lot weg</b>, <b>reflektiert</b>.</p></div>"""

# ====================================================================== 4 Linsen
L_ALLTAG = tabellenfolie("Linsen im Alltag", [
    ("Brille", "scharf sehen", "Die Linsen der Brille helfen dem Auge, ein scharfes Bild zu erzeugen."),
    ("Handykamera", "ein Bild auf dem Sensor", "Eine kleine Sammellinse bündelt das Licht auf dem Sensor."),
    ("Glasflasche im Wald", "trockenes Laub kann brennen", "Sie wirkt wie ein Brennglas und bündelt das Sonnenlicht."),
    ("Wassertropfen", "die Schrift darunter wirkt größer", "Ein Tropfen ist in der Mitte dicker, also eine kleine Sammellinse."),
], frage="Woran erkennst du, ob eine Linse sammelt oder zerstreut?")

LI = [basis2(24), basis2(25),
      blatt("Strahlengaenge an Linsen W13.pdf", "w13", "Versuchsblatt austeilen · Versuch in Gruppen"),
      basis2(27), L_ALLTAG]

L_MAT = {"demo": [("Lupen", "mehrere", "zum Durchgeben beim Einstieg"),
                  ("Sammellinse als Brennglas", "1×", "nur bei Sonne, Papier auf feuerfester Unterlage")],
         "schueler": [("Ray-Box mit drei parallelen Strahlen", "1×", ""),
                      ("Sammellinse (Linsenprofil)", "1×", "in der Mitte dicker"),
                      ("Zerstreuungslinse (Linsenprofil)", "1×", "am Rand dicker")],
         "hinweis": "Raum abdunkeln. Leitfrage 8 geht in der nächsten Doppelstunde weiter: Bildentstehung, Lupe, Auge."}

L_SCHRITTE = [("Einstieg", "Lupen durchgeben, Leitfrage 8, Vermutungen.", [1, 2]),
              ("Versuch", "Drei parallele Strahlen an beiden Linsen, Versuchsblatt.", [3]),
              ("Erklären", "Sammellinse, Zerstreuungslinse, Brennpunkt.", [4]),
              ("Alltag", "Brennglas vorne, Beispiele mündlich.", [5])]

L_HG = f"""
<div class="box"><h3>Sammel- und Zerstreuungslinse {chip(4)}</h3><ul>
<li>Eine Linse bricht das Licht zweimal, beim Eintritt und beim Austritt. Am Rand treffen die Strahlen schräger auf und werden stärker abgelenkt.</li>
<li><b>Brennweite:</b> Abstand vom Brennpunkt zur Linsenmitte. Je stärker die Linse gewölbt ist, desto kürzer die Brennweite. Die Brechkraft einer Brille wird in Dioptrien angegeben (1 durch Brennweite in Metern).</li>
<li>Bei der Zerstreuungslinse ist der Brennpunkt der Punkt, von dem die Strahlen zu kommen scheinen. Er liegt auf der Seite, von der das Licht kommt.</li>
<li><b>Typische Fehlvorstellungen:</b> Der Brennpunkt liegt immer an der Linse. Dicke Linsen sammeln immer, egal wie sie geformt sind.</li></ul></div>
<div class="box"><h3>Tipps zum Versuch {chip(3)}</h3><ul>
<li>Die Ray-Box so legen, dass der mittlere Strahl genau auf der Achse liegt. Sonst wird er schon an der Linsenmitte abgelenkt.</li>
<li>Erst Strahlen vor und hinter der Linse mit Bleistift nachfahren, dann die Linse wegnehmen und verbinden.</li>
<li><b>Brennglas:</b> Nur auf feuerfester Unterlage, niemand schaut dabei durch die Linse in die Sonne.</li></ul></div>
{LAB("Linsenlabor Sammel- und Zerstreuungslinse.html", "Linsenlabor", "Drei parallele Strahlen, Wölbung und Brennweite, Brennglas mit verschiebbarem Papier, Ausblick Bildentstehung mit Lupenbild.")}
"""
L_AB = f"""
<div class="box"><h3>Versuchsblatt Strahlengänge an Linsen {chip(3)}</h3>
<a class="btn" href="Materialien/Strahlengaenge an Linsen W13.pdf">PDF öffnen</a>
<p><b>Lösung:</b> Sammellinse: Die drei Strahlen schneiden sich im Brennpunkt. Zerstreuungslinse: Die Strahlen laufen auseinander, rückwärts verlängert treffen sie sich im Brennpunkt vor der Linse.
Lücken: <b>Brennpunkt</b>, <b>auseinander</b>.</p></div>"""

STUNDEN = [
    ("Optik II – Reflexionsgesetz – Stunde.html", "Optik: Was passiert mit dem Licht am Spiegel?",
     "Klasse 7c · Physik · Leitfrage 6, Teil 1 · Reflexionsgesetz · voraussichtlich Do 05.11.2026",
     ["Versuchsblatt: Kopiervorlage „2 auf 1“, halbe Klassenstärke drucken und in der Mitte durchschneiden.", "Folien und Lösungen: nicht drucken."],
     R_MAT, R_SCHRITTE, R, R_HG, R_AB),
    ("Optik II – Spiegelbild – Stunde.html", "Optik: Das Spiegelbild",
     "Klasse 7c · Physik · Leitfrage 6, Teil 2 · Spiegelbild und Spiegelgröße · voraussichtlich Do 12.11.2026",
     ["Arbeitsblatt Der Spiegel: Seite 1, eins pro Schüler.", "Folien und Lösungen: nicht drucken."],
     S_MAT, S_SCHRITTE, SB, S_HG, S_AB),
    ("Optik II – Lichtbrechung – Stunde.html", "Optik: Warum sieht der Strohhalm im Wasser geknickt aus?",
     "Klasse 7c · Physik · Leitfrage 7 · Lichtbrechung · voraussichtlich Do 19.11.2026",
     ["Versuchsblatt: Seite 1, eins pro Schüler (zwei Tabellen, zu lang für „2 auf 1“).", "Folien und Lösungen: nicht drucken."],
     B_MAT, B_SCHRITTE, BR, B_HG, B_AB),
    ("Optik II – Linsen – Stunde.html", "Optik: Wie kann eine Lupe vergrößern?",
     "Klasse 7c · Physik · Leitfrage 8, Teil 1 · Sammel- und Zerstreuungslinse · voraussichtlich Do 26.11.2026",
     ["Versuchsblatt: Seite 1, eins pro Schüler (zwei Zeichenfelder).", "Folien und Lösungen: nicht drucken."],
     L_MAT, L_SCHRITTE, LI, L_HG, L_AB),
]

for datei, h1, sub, drucken, mat, schritte, folge, hg, ab in STUNDEN:
    bau_stunde(datei, h1, sub, drucken, mat, schritte, folge, hg, ab)

if "export" in sys.argv:
    from stunde_vorlage import exportiere, materialliste, MAT, ICL
    VORLAGE = ICL / "F4 Kern- und Halbschatten (W06-07)"
    AUFTRAEGE = [
        ("F6a Reflexionsgesetz (W10)", "W10", "F6 — Reflexionsgesetz", 0, "Reflexionsgesetz W10.pdf", "Reflexionsgesetz W10 – 2 auf 1.pdf", "F6a", "Spiegellabor Reflexion.html"),
        ("F6b Spiegelbild (W11)", "W11", "F6 — Spiegelbild und Spiegelgröße", 1, "Der Spiegel W11.pdf", None, "F6b", "Spiegellabor Reflexion.html"),
        ("F7 Lichtbrechung (W12)", "W12", "F7 — Lichtbrechung", 2, "Lichtbrechung W12.pdf", None, "F7", "Brechungslabor Lichtbrechung.html"),
        ("F8a Linsen (W13)", "W13", "F8 — Sammel- und Zerstreuungslinse", 3, "Strahlengaenge an Linsen W13.pdf", None, "F8a", "Linsenlabor Sammel- und Zerstreuungslinse.html"),
    ]
    ICL2 = ICL.parent / "Optik II 2026-27"
    ICL2.mkdir(exist_ok=True)
    for ordnername, chip_text, titel, idx, ab, ab21, kurz, labor in AUFTRAEGE:
        datei, h1, sub, drucken, mat, schritte, folge, hg, abx = STUNDEN[idx]
        ordner = ICL2 / ordnername
        ordner.mkdir(exist_ok=True)
        shutil.copy(VORLAGE / "Materialliste.html", ordner / "Materialliste.html")
        (ordner / "Gesamt.html").write_text((VORLAGE / "Gesamt.html").read_text(encoding="utf-8").replace("W06–07", chip_text), encoding="utf-8")
        shutil.copy(MAT / ab, ordner / f"Arbeitsblatt {kurz}.pdf")
        links = {f"Materialien/{ab}": f"Arbeitsblatt {kurz}.pdf", labor: f"../../Optik 2026-27/Labore/{labor}",
                 "Optik-Labore.html": "../../Optik 2026-27/Labore/Optik-Labore.html"}
        if ab21:
            shutil.copy(MAT / ab21, ordner / f"Arbeitsblatt {kurz} – Kopiervorlage 2 auf 1.pdf")
            links[f"Materialien/{ab21}"] = f"Arbeitsblatt {kurz} – Kopiervorlage 2 auf 1.pdf"
        materialliste(ordner, chip_text, titel, mat)
        exportiere(folge, ordner, f"Folien {kurz}.pdf", f"Arbeitsblatt {kurz}.pdf", f"Stunde {kurz}.html", datei, links)
    for f in ("Optik-Labore.html", "Spiegellabor Reflexion.html", "Brechungslabor Lichtbrechung.html", "Linsenlabor Sammel- und Zerstreuungslinse.html",
              "Sehlabor Lichtquellen.html", "Körperlabor Licht trifft auf Körper.html", "Strahlenlabor Lichtausbreitung.html",
              "Schattenlabor Halbschatten.html", "Mondlabor Mondphasen und Finsternisse.html", "Lochkameralabor.html"):
        shutil.copy(f, ICL / "Labore" / f)
    print("Labore kopiert")
