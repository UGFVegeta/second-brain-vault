#!/usr/bin/env python3
"""Stunden-HTMLs Kernphysik Klasse 10, W06 bis W22 (Leitfragen 3 bis 6, je eine Einzelstunde).
W10/W11 Klassenarbeit und W14 Puffer haben keine eigene Stunde. Ideen aus „Erlebnis Physik“ Kl. 10 in eigenen Worten.
python3 baue_stunden_k10_teil2.py   -> HTMLs im Ordner Kernphysik (Export nach iCloud erst nach Freigabe)"""
from baue_stunden_k10 import HIER, KERN_CSS, f, blatt, LAB, chip, tabellenfolie, bau_stunde

STRAHL = "Strahlungslabor Radioaktivitaet.html"
ZERF = "Zerfallslabor Halbwertszeit.html"
WIRK = "Wirkungslabor Strahlung und Koerper.html"
KERN = "Kernenergielabor Spaltung und Fusion.html"
NICHT_DRUCKEN = "Folien und Lösungen: nicht drucken."
PSE = ("Periodensystem", "1×", "")


def ab_box(titel, pdf, loesung, *nr):
    return (f'<div class="box"><h3>{titel} {chip(*nr)}</h3><a class="btn" href="Materialien/{pdf}">PDF öffnen</a>'
            f'<p><b>Lösung:</b> {loesung}</p></div>')


def box(titel, punkte, *nr):
    return f'<div class="box"><h3>{titel} {chip(*nr) if nr else ""}</h3><ul>' + "".join(f"<li>{p}</li>" for p in punkte) + "</ul></div>"


# ====================================================================== W06
A6 = tabellenfolie("Zufall im Einzelnen, sicher in der Menge", [
    ("Popcorn", "Welches Korn zuerst platzt, weiß keiner.", "Nach drei Minuten sind trotzdem fast alle aufgeplatzt."),
    ("Glühlampen einer Lieferung", "Jede hält unterschiedlich lange.", "Der Hersteller kennt trotzdem die mittlere Lebensdauer."),
    ("Würfel im Versuch", "Welcher Würfel eine Sechs hat, ist Zufall.", "Pro Wurf fällt trotzdem etwa ein Sechstel weg."),
], frage="Warum kann man für einen einzelnen Kern nichts vorhersagen, für ein ganzes Präparat aber schon?")
S6 = [f(21), f(22), f(23), f(24), f(25), blatt("Zerfall mit Wuerfeln W06.pdf", "k06", "Versuchsblatt austeilen · 30 Würfel pro Gruppe"), A6]
S6_HG = (box("Abschluss Leitfrage 2", ["Die Antwortfolie ins Heft, der Check per Handzeichen. Lösung: 1 a, 2 c.",
                                       "Wer die Zerfallsgleichungen noch nicht sicher kann: Übung im Strahlungslabor."], 1, 2, 3)
         + box("Das Würfelmodell", ["Jede Runde fällt im Mittel ein Sechstel weg, übrig bleiben 5/6. Nach etwa 3,8 Würfen ist die Hälfte weg. Das ist die „Halbwertszeit“ des Modells.",
                                    "Die Gruppenwerte streuen stark. Die Summe der ganzen Klasse passt viel besser zur Kurve. Deshalb die Klassenwerte an der Tafel addieren.",
                                    "Grenze des Modells: Echte Kerne zerfallen nicht in Runden, sondern zu jedem beliebigen Zeitpunkt. Die Wahrscheinlichkeit pro Zeit ist aber genauso fest.",
                                    "<b>Typische Fehlvorstellungen:</b> Nach zwei Halbwertszeiten ist alles zerfallen. Ein Kern, der lange nicht zerfallen ist, ist „bald dran“."], 4, 6)
         + box("Material", ["Würfel aus der Mathe-Sammlung. Alternative: 30 Münzen pro Gruppe, „Zahl“ scheidet aus. Dann halbiert sich die Zahl schon pro Wurf."], 6)
         + LAB(ZERF, "Zerfallslabor", "100 Würfel Wurf für Wurf, drei Zufallsserien, dazu 400 Kerne mit zufälligem Zerfall."))
S6_AB = ab_box("Versuchsblatt Zerfall mit Würfeln", "Zerfall mit Wuerfeln W06.pdf",
               "Erwartete Werte 30, 25, 21, 17, 14, 12, 10, 8, 7. Hälfte nach knapp 4 Würfen. Würfel = Kern, Sechs = Zerfall, die Abweichung kommt vom Zufall.", 6)

# ====================================================================== W07
A7 = tabellenfolie("Halbwertszeiten im Vergleich", [
    ("Radon-220", "56 Sekunden", "entsteht in Gestein und Baustoffen"),
    ("Iod-131", "8 Tage", "in der Medizin gegen Schilddrüsenkrankheiten"),
    ("Cäsium-137", "30 Jahre", "noch heute in Pilzen und Wildschweinen aus Tschernobyl"),
    ("Kohlenstoff-14", "5730 Jahre", "Altersbestimmung von Funden"),
    ("Uran-238", "4,5 Milliarden Jahre", "etwa so alt wie die Erde, deshalb noch da"),
], kopf=("Nuklid", "Halbwertszeit", "wo es vorkommt"), frage="Warum gibt es Uran-238 heute noch, Radon-220 aber nur, wenn es ständig neu entsteht?")
A7b = tabellenfolie("Halbieren nicht nur bei Kernen", [
    ("Luftdruck", "halbiert sich etwa alle 5,5 km Höhe", "Auf dem Mount Everest ist es rund ein Drittel."),
    ("Koffein im Blut", "halbiert sich in etwa 5 Stunden", "Der Kaffee am Abend wirkt noch in der Nacht."),
    ("Bierschaum", "fällt immer um die Hälfte in gleicher Zeit", "unser Versuch mit Malzbier"),
], kopf=("Beispiel", "was passiert", "Folge"))
S7 = [f(27), blatt("Halbwertszeit W07.pdf", "k07", "Arbeitsblatt austeilen · Malzbier und Messzylinder pro Gruppe"), A7, A7b]
S7_HG = (box("Halbwertszeit", ["Nach n Halbwertszeiten ist der Anteil (1/2)ⁿ übrig. Nach 10 Halbwertszeiten noch etwa ein Tausendstel.",
                               "Auf der Folie: Fluor-20 mit 11 s. Die Werte stammen aus einer Messreihe, die sich gut als Übung zum Ablesen eignet.",
                               "Zerfallsgesetz für Interessierte: N(t) = N₀ · (1/2)^(t/T). Rechnen mit gebrochenen Hochzahlen ist nicht verlangt.",
                               "<b>Typische Fehlvorstellung:</b> Die Halbwertszeit ist die halbe Lebensdauer eines Kerns."], 1)
         + box("Bierschaumversuch", ["Malzbier ist alkoholfrei. Zimmerwarm und schnell eingegossen schäumt es am stärksten.",
                                     "Die Schaumhöhe nimmt ungefähr exponentiell ab. Die Halbwertszeit hängt stark vom Getränk ab, meist zwischen einer und drei Minuten.",
                                     "Den Anfangswert erst ablesen, wenn sich die Grenze zwischen Schaum und Flüssigkeit gebildet hat."], 2)
         + box("Im Alltag", ["Cäsium-137 aus Tschernobyl ist nach 40 Jahren erst gut zur Hälfte zerfallen. Wildschweine im Süden Deutschlands sind deshalb teils noch belastet.",
                             "Luftdruck und Koffein folgen demselben Muster, das zeigt die Mathematik der Abnahme."], 3, 4)
         + LAB(ZERF, "Zerfallslabor", "Halbwertszeit für sechs Nuklide mit Regler, exponentielle Abnahme im Alltag."))
S7_AB = ab_box("Arbeitsblatt Die Halbwertszeit", "Halbwertszeit W07.pdf",
               "Schaum (Beispiel): 10,0 bis 1,9 cm, Halbierung nach etwa 100 s. Lücken: Hälfte, ein Viertel, ein Achtel, feste. Iod-131: 500, 250, 125, 62,5, 31,25 Kerne. Die Kurve halbiert immer nur und erreicht nie null.", 2)

# ====================================================================== W08
A8 = tabellenfolie("Becquerel im Alltag", [
    ("Mensch (70 kg)", "etwa 9000 Bq", "vor allem Kalium-40 und Kohlenstoff-14 aus der Nahrung"),
    ("1 Liter Milch", "etwa 50 Bq", "Kalium-40, ganz natürlich"),
    ("Diätsalz (1 kg Kaliumchlorid)", "etwa 16 000 Bq", "Das Zählrohr zeigt davor mehr als die Nullrate."),
    ("Rauchmelder mit Americium", "etwa 37 000 Bq", "in Deutschland heute kaum noch im Einsatz"),
], kopf=("Gegenstand", "Aktivität", "woher"), frage="Wie viele Kerne zerfallen in deinem Körper in einer Minute?")
S8 = [f(29), blatt("Aktivitaet und Zaehlrate W08.pdf", "k08", "Arbeitsblatt austeilen · Abstandsreihe vorne"), A8]
S8_HG = (box("Aktivität und Zählrate", ["Aktivität A in Becquerel: Zerfälle pro Sekunde. Sie halbiert sich mit derselben Halbwertszeit wie die Zahl der Kerne.",
                                        "Die Zählrate ist viel kleiner: Das Zählrohr sieht nur einen kleinen Raumwinkel, und nicht jedes Teilchen löst einen Impuls aus. γ-Quanten gehen oft einfach durch.",
                                        "Abstandsgesetz: Die Strahlung verteilt sich auf eine Kugeloberfläche. Doppelter Abstand, vierfache Fläche, ein Viertel der Zählrate. Bei α und β kommt die Absorption in Luft dazu.",
                                        "<b>Typische Fehlvorstellung:</b> Die Zählrate ist die Aktivität."], 1)
         + box("Versuche", ["Abstandsreihe mit einem γ-Präparat: 2, 4, 8 cm, jeweils eine Minute. Nullrate vorher messen und abziehen.",
                            "Freiwillig: 1 kg Diätsalz (Kaliumchlorid, im Supermarkt) in einer Schale vor das Zählrohr. Die Zählrate liegt deutlich über der Nullrate, ganz ohne Präparat aus der Sammlung."], 2)
         + LAB(ZERF, "Zerfallslabor", "Aktivität und Zählrate mit Reglern für Aktivität und Abstand."))
S8_AB = ab_box("Arbeitsblatt Aktivität und Zählrate", "Aktivitaet und Zaehlrate W08.pdf",
               "Lücken: Sekunde, Becquerel, ein Zerfall, alle Richtungen, Zählrate. 540 000, 3000, 2 220 000 Zerfälle pro Minute. Abstand: 1600, 400, 100. Cäsium: 4000, 2000, 1000 Bq.", 2)

# ====================================================================== W09
S9 = [f(30), f(31), f(32), blatt("Uebungen Halbwertszeit W09.pdf", "k09", "Übungsblatt austeilen · Vorbereitung Klassenarbeit")]
S9_HG = (box("Abschluss Leitfrage 3", ["Antwortfolie ins Heft, Check per Handzeichen. Lösung: 1 b, 2 c."], 1, 2, 3)
         + box("Übungsblatt", ["Die Aufgaben steigen an: Aufgaben 1 und 2 sind Pflicht, 3 bis 5 Übung, 6 und 7 für Schnelle.",
                               "Aufgabe 6 (Zerfallsreihe Uran-238 zu Blei-206) verbindet Leitfrage 2 und 3: 8 α- und 6 β⁻-Zerfälle.",
                               "Die Aufgaben passen zum Stoff der Klassenarbeit in W10: Atombau, Zerfall, Halbwertszeit."], 4)
         + LAB(ZERF, "Zerfallslabor", "Zum Üben zu Hause: Halbwertszeit ablesen, Kurz-Check mit sechs Fragen."))
S9_AB = ab_box("Übungsblatt Halbwertszeit", "Uebungen Halbwertszeit W09.pdf",
               "800, 400, 200, 100. 26,4 h, 7,6 Tage, 60 Jahre. 2 g. 28 650 Jahre. 25 %. 8 α und 6 β⁻. Etwa 2076.", 4)

# ====================================================================== W12
A12 = tabellenfolie("Strahlung nachweisen", [
    ("Dosimeter", "kleine Plakette am Kittel", "Wer mit Strahlung arbeitet, trägt es immer. Es zeigt die gesamte Dosis."),
    ("Zählrohr", "klickt bei jedem Teilchen", "Messgerät im Unterricht und im Strahlenschutz"),
    ("Nebelkammer", "Spuren wie Kondensstreifen", "Man sieht einzelne Teilchen, sogar aus dem Weltall."),
    ("Fotoplatte", "wird dunkel", "So entdeckte Becquerel 1896 die Radioaktivität."),
], kopf=("Gerät", "was man sieht", "wofür"), frage="Was haben alle vier Nachweise gemeinsam?")
S12 = [f(33), f(34), f(36), blatt("Ionisierende Strahlung W12.pdf", "k12", "Arbeitsblatt austeilen"), A12]
S12_HG = (box("Einstieg Leitfrage 4", ["Röntgenbild und Warnzeichen: Dieselbe Art Strahlung hilft beim Arzt und wird im Labor abgeschirmt. Die Klasse soll den Widerspruch selbst benennen.",
                                       "Röntgenstrahlung ist keine radioaktive Strahlung, sie entsteht in einer Röhre. Sie ist aber ebenfalls ionisierend."], 1, 2)
          + box("Ionisation", ["Die Strahlung gibt Energie an Elektronen ab und schlägt sie aus der Hülle. Es entsteht ein Ionenpaar.",
                               "α ionisiert sehr dicht (viele Ionen auf kurzer Strecke), β weniger dicht, γ nur vereinzelt. Deshalb die unterschiedliche Reichweite.",
                               "Auch Zählrohr und Nebelkammer beruhen auf Ionisation, das verbindet Leitfrage 2 und 4.",
                               "<b>Typische Fehlvorstellung:</b> Bestrahlte Stoffe werden selbst radioaktiv. Bei α, β und γ ist das nicht so, nur Neutronen können Stoffe aktivieren."], 3)
          + box("Nebelkammer", ["Falls in der Sammlung vorhanden: Diffusionsnebelkammer mit Trockeneis und Isopropanol. Auch ohne Präparat sieht man nach einigen Minuten Spuren (Myonen, Radon).",
                                "Sonst Video oder die Szene im Wirkungslabor."], 5)
          + LAB(WIRK, "Wirkungslabor", "Ionisation durch α, β und γ im Gewebe, Nebelkammer mit verschiedenen Quellen."))
S12_AB = ab_box("Arbeitsblatt Ionisierende Strahlung", "Ionisierende Strahlung W12.pdf",
                "Lücken: Elektronen, Ion, ionisierende, Moleküle. Spuren: α, β, γ. α ionisiert am stärksten. Zählrohr: Gas wird ionisiert, Stromstoß. Eingeatmetes α wirkt direkt auf die Lunge.", 4)

# ====================================================================== W13
A13 = tabellenfolie("Wie viel ist ein Millisievert?", [
    ("Röntgenbild des Brustkorbs", "0,01 bis 0,03 mSv", "wie einige Tage natürliche Strahlung"),
    ("Flug nach New York und zurück", "etwa 0,1 mSv", "mehr Höhenstrahlung in 10 km Höhe"),
    ("CT des Kopfes", "etwa 2 mSv", "etwa so viel wie ein Jahr natürliche Strahlung"),
    ("Beruflicher Grenzwert", "20 mSv pro Jahr", "für Menschen, die mit Strahlung arbeiten"),
], kopf=("Anlass", "Dosis", "zum Vergleich"), frage="Warum fragt die Ärztin vor einem CT, ob die Untersuchung wirklich nötig ist?")
S13 = [f(38), f(40), blatt("Wirkung auf den Koerper W13.pdf", "k13", "Arbeitsblatt austeilen"), A13]
S13_HG = (box("Wirkung auf die Zelle", ["Die meisten DNA-Schäden repariert die Zelle selbst. Gefährlich sind bleibende Veränderungen.",
                                         "Somatische Schäden treffen die bestrahlte Person: Frühschäden (Strahlenkrankheit) nur bei hohen Dosen ab etwa 1000 mSv auf einmal, Spätschäden (Krebs, Leukämie) Jahre später.",
                                         "Genetische Schäden entstehen in Keimzellen und können an Nachkommen weitergegeben werden.",
                                         "Die Einheit Sievert berücksichtigt die Wirkung: α-Strahlung zählt bei gleicher Energie rund 20-mal so stark wie β oder γ.",
                                         "<b>Typische Fehlvorstellung:</b> Jede noch so kleine Dosis macht krank. Gerade bei kleinen Dosen ist das Risiko sehr gering, aber man geht davon aus, dass es nicht null ist."], 1)
          + box("Strahlenbelastung in Deutschland (BfS)", ["Natürlich im Mittel 2,1 mSv pro Jahr: Radon 1,1, Boden 0,4, Nahrung 0,3, Weltall 0,3.",
                                                            "Medizin im Mittel etwa 1,5 mSv pro Jahr. Alles andere (Kernkraftwerke, Tschernobyl-Folgen) unter 0,01 mSv.",
                                                            "Die Folie 11 war vorher mit „etwa ebenso viel aus der Medizin“ beschriftet. Nach den aktuellen BfS-Zahlen ist es weniger, deshalb steht dort jetzt 1,5 mSv."], 2)
          + LAB(WIRK, "Wirkungslabor", "Treffer in der Zelle mit drei Folgen, persönliche Jahresdosis mit Flügen, Röntgen, CT und Radon."))
S13_AB = ab_box("Arbeitsblatt Wirkung auf den Körper", "Wirkung auf den Koerper W13.pdf",
                "Reparatur, Zelltod, Veränderung. Frühschaden, Spätschaden, genetischer Schaden. Jahresdosis 4,32 mSv, etwas über dem Durchschnitt. Faktoren: Art, Dosis, Abstand, Dauer, Organ.", 3)

# ====================================================================== W15
A15 = tabellenfolie("Radon zu Hause", [
    ("Keller und Erdgeschoss", "höchste Werte", "Das Gas strömt aus dem Boden durch Risse ins Haus."),
    ("Granit, z. B. im Schwarzwald", "mehr Radon im Boden", "Das Gestein enthält mehr Uran."),
    ("gut gedämmter Neubau", "oft mehr Radon in der Luft", "Die dichte Hülle tauscht weniger Luft aus."),
    ("Stoßlüften", "Werte sinken schnell", "die einfachste und wirksamste Maßnahme"),
], kopf=("Ort", "was man misst", "warum"), frage="Welche der fünf A-Regeln hilft gegen Radon?")
S15 = [f(42), f(43), f(44), f(45), blatt("Schutz und Anwendungen W15.pdf", "k15", "Arbeitsblatt austeilen"), A15]
S15_HG = (box("Strahlenschutz", ["Auf der Folie stehen die drei klassischen Regeln. Das Buch nennt fünf A-Regeln: Abstand, Aufenthaltsdauer, Abschirmung, Aktivität verringern, Aufnahme vermeiden. Das Blatt nimmt alle fünf.",
                                 "Abstand wirkt am stärksten (Quadrat), Zeit wirkt proportional, Abschirmung exponentiell.",
                                 "Grenzwerte: 20 mSv pro Jahr beruflich, 1 mSv pro Jahr zusätzlich für die Bevölkerung aus Anlagen und Technik. Für die Medizin gibt es keinen Grenzwert, dort wird im Einzelfall abgewogen."], 1)
          + box("Anwendungen", ["Röntgen: Knochen absorbieren mehr als Weichgewebe. Szintigramm: kurzlebiger γ-Strahler (meist Technetium-99m, 6 h Halbwertszeit) reichert sich im Organ an.",
                                "Strahlentherapie: Die Dosis wird aus vielen Richtungen auf den Tumor gebündelt, gesundes Gewebe bekommt wenig ab.",
                                "Sterilisation mit γ-Strahlung: Die Gegenstände werden dabei nicht radioaktiv."], 1)
          + box("Abschluss Leitfrage 4", ["Antwortfolie ins Heft, Check per Handzeichen. Lösung: 1 b, 2 c."], 2, 3, 4)
          + LAB(WIRK, "Wirkungslabor", "Schutzregeln mit Reglern für Abstand, Aufenthalt und Blei, Kurz-Check."))
S15_AB = ab_box("Arbeitsblatt Schutz und Anwendungen", "Schutz und Anwendungen W15.pdf",
                "Abstand, Aufenthaltsdauer, Abschirmung, Aktivität, Aufnahme. 2 µSv, 0,5 µSv, 2 µSv. Anwendungen siehe Lösungsseite. Kurze Halbwertszeit: wenig Dosis nach der Untersuchung. Radon: aus dem Boden, lüften.", 5)

# ====================================================================== W16
A16 = tabellenfolie("Kernkraft in Baden-Württemberg", [
    ("Obrigheim (am Neckar)", "1968 bis 2005", "wird zurückgebaut"),
    ("Philippsburg 1 und 2", "bis 2011 und bis 2019", "Kühltürme 2020 gesprengt, Rückbau läuft"),
    ("Neckarwestheim 1 und 2", "bis 2011 und bis 15. April 2023", "eines der letzten drei Kraftwerke in Deutschland"),
], kopf=("Kraftwerk", "in Betrieb", "heute"), frage="Wie weit ist Neckarwestheim von unserer Schule entfernt?")
S16 = [f(46), f(47), f(49), blatt("Kernspaltung W16.pdf", "k16", "Arbeitsblatt austeilen · mit Periodensystem"), A16]
S16_HG = (box("Einstieg Leitfrage 5", ["1 kg Uran-235 liefert bei vollständiger Spaltung etwa 8 · 10¹³ J. Steinkohle hat etwa 30 MJ pro kg, das ergibt rund 3000 t.",
                                       "Der Unterschied: Bei der Verbrennung ändern sich nur Elektronenhüllen, bei der Spaltung die Kerne. Kernkräfte sind millionenfach stärker."], 1, 2)
          + box("Die Kernspaltung", ["1938 fanden Otto Hahn und Fritz Straßmann in Berlin Barium in bestrahltem Uran. Lise Meitner und Otto Frisch lieferten die Erklärung. Hahn erhielt den Chemie-Nobelpreis für 1944, Meitner ging leer aus.",
                                     "Nur langsame (thermische) Neutronen spalten Uran-235 gut. Uran-238 wird von ihnen kaum gespalten.",
                                     "Die Bruchstücke sind zufällig verteilt, häufig um die Massenzahlen 95 und 140. Im Mittel werden etwa 2,4 Neutronen frei.",
                                     "Die Energie steckt vor allem in der Bewegungsenergie der Bruchstücke, die im Brennstab zu Wärme wird.",
                                     "<b>Typische Fehlvorstellung:</b> Bei der Spaltung verschwindet Masse einfach. Genauer: Die Bruchstücke sind zusammen etwas leichter, diese Differenz ist die frei werdende Energie."], 3)
          + LAB(KERN, "Kernenergielabor", "Spaltung mit drei möglichen Bruchstückpaaren und Kontrolle der Summen."))
S16_AB = ab_box("Arbeitsblatt Die Kernspaltung", "Kernspaltung W16.pdf",
                "Lücken: Otto Hahn, Barium, gespalten, Neutron, mittelschwere, 2 oder 3. Gleichungen: 2 Neutronen, I-137, Sr-90. Neutronen sind ungeladen. 50 Güterwagen. Wasserstoff hat nur ein Proton.", 4)

# ====================================================================== W17
A17 = tabellenfolie("Kettenreaktionen im Alltag", [
    ("Dominoeffekt", "ein Stein wirft den nächsten um", "kontrolliert, wenn jeder genau einen weiteren umwirft"),
    ("Ansteckung bei Grippe", "Ansteckungszahl R", "R größer 1: Die Welle wächst. R kleiner 1: Sie ebbt ab."),
    ("Lawine", "ein Schneebrett reißt weitere mit", "unkontrolliert, sie wächst immer weiter"),
], kopf=("Beispiel", "was weitergegeben wird", "kontrolliert oder nicht?"), frage="Was entspricht im Reaktor der Ansteckungszahl R?")
S17 = [f(51), blatt("Kettenreaktion W17.pdf", "k17", "Versuchsblatt austeilen · Dominosteine pro Gruppe"), f(53), A17]
S17_HG = (box("Kettenreaktion", ["Entscheidend ist, wie viele der freien Neutronen im Mittel eine neue Spaltung auslösen (Multiplikationsfaktor k). k = 1 heißt kritisch, der Reaktor läuft gleichmäßig.",
                                 "In einem Kernkraftwerk ist das Uran nur auf 3 bis 5 % Uran-235 angereichert. Eine Explosion wie bei einer Kernwaffe ist damit physikalisch nicht möglich.",
                                 "Ein kleiner Teil der Neutronen wird erst Sekunden später frei (verzögerte Neutronen). Nur deshalb lässt sich ein Reaktor mit Steuerstäben regeln."], 1)
          + box("Dominoversuch", ["Pro Gruppe etwa 50 Dominosteine. Schritt 2 braucht Platz auf dem Boden oder einem großen Tisch.",
                                  "Mausefallen-Modell als Alternative: nur als Video, der Aufbau ist aufwendig."], 2)
          + box("Aufbau eines Reaktors", ["Brennstäbe mit Uranoxid, Steuerstäbe aus Bor oder Cadmium, Wasser als Moderator und Kühlmittel, alles im Reaktordruckbehälter aus Stahl.",
                                          "Wasser als Moderator hat einen Sicherheitsvorteil: Wird es zu heiß und verdampft, fehlt der Moderator und die Kettenreaktion wird schwächer. In Tschernobyl war das anders (Graphit)."], 3)
          + LAB(KERN, "Kernenergielabor", "Kettenreaktion mit 0,8 bis 3 wirksamen Neutronen, Steuerstäbe mit Leistungskurve."))
S17_AB = ab_box("Versuchsblatt Kettenreaktion mit Dominosteinen", "Kettenreaktion W17.pdf",
                "Schritt 2 unkontrolliert, Schritt 3 kontrolliert. 1, 2, 4, 8, 16 und 1, 3, 9, 27, 81. Bauteile siehe Lösungsseite. Die Steuerstäbe übernehmen die Rolle der entfernten Steine.", 2)

# ====================================================================== W18
A18 = tabellenfolie("Wo man an der Fusion forscht", [
    ("Sonne", "Fusion seit 4,6 Milliarden Jahren", "Wasserstoff wird zu Helium, etwa 15 Mio. °C im Inneren"),
    ("Wendelstein 7-X, Greifswald", "Forschungsanlage seit 2015", "hält heißes Plasma mit Magnetfeldern fest"),
    ("ITER, Frankreich", "internationale Anlage im Bau", "soll mehr Energie liefern, als sie zum Heizen braucht"),
    ("NIF, USA", "Laser-Versuch 2022", "erstmals mehr Fusionsenergie als Laserenergie eingestrahlt"),
], kopf=("Ort", "was es ist", "was dort passiert"), frage="Warum gibt es trotzdem noch kein Fusionskraftwerk?")
S18 = [f(55), f(57), blatt("Kernkraftwerk und Kernfusion W18.pdf", "k18", "Arbeitsblatt austeilen"), A18]
S18_HG = (box("Kraftwerk", ["Druckwasserreaktor: Primärkreislauf unter etwa 150 bar, damit das Wasser bei rund 300 °C nicht siedet. Dampferzeuger trennt ihn vom Sekundärkreislauf.",
                            "Wirkungsgrad etwa 33 %. Zwei Drittel der Wärme gehen an Fluss und Luft, deshalb stehen Kraftwerke an Flüssen.",
                            "Ab dem Dampf gleicht das Kernkraftwerk einem Kohlekraftwerk. Unterschied: kein CO₂ im Betrieb, dafür radioaktiver Abfall."], 1)
          + box("Kernfusion", ["Deuterium gibt es im Meerwasser, Tritium muss aus Lithium erbrütet werden.",
                               "Die Sonne schafft Fusion bei 15 Mio. °C nur wegen des riesigen Drucks und der enormen Menge an Wasserstoff. Einzelne Reaktionen sind dort sehr selten.",
                               "Fusion erzeugt keinen langlebigen Abfall wie die Spaltung. Die Neutronen aktivieren aber die Wände der Anlage."], 2)
          + LAB(KERN, "Kernenergielabor", "Drei Wasserkreisläufe zum Anklicken, Fusion mit Temperaturregler."))
S18_AB = ab_box("Arbeitsblatt Kernkraftwerk und Kernfusion", "Kernkraftwerk und Kernfusion W18.pdf",
                "1 Reaktor, 2 Dampferzeuger, 3 Turbine, 4 Generator, 5 Kondensator, 6 Kühlturm. Primärkreislauf, Dampferzeuger, Turbine, Kühlkreislauf. Kernenergie, Wärme, Bewegung, elektrische Energie. He-4 und n.", 3)

# ====================================================================== W19
A19 = tabellenfolie("Kernkraft weltweit", [
    ("Welt", "gut 400 Reaktoren in Betrieb", "liefern knapp ein Zehntel des Stroms"),
    ("Frankreich", "etwa zwei Drittel des Stroms", "setzt weiter auf Kernkraft"),
    ("China", "baut die meisten neuen Reaktoren", "wegen des schnell wachsenden Strombedarfs"),
    ("Deutschland", "seit April 2023 keiner mehr am Netz", "Ausstieg nach Fukushima beschlossen"),
], kopf=("Land", "Stand", "Hintergrund"), frage="Warum entscheiden Länder so unterschiedlich?")
S19 = [f(58), f(59), f(60), blatt("Uebungen Kernenergie W19.pdf", "k19", "Übungsblatt austeilen · mit Periodensystem"), A19]
S19_HG = (box("Abschluss Leitfrage 5", ["Antwortfolie ins Heft, Check per Handzeichen. Lösung: 1 b, 2 b."], 1, 2, 3)
          + box("Reaktorunfälle", ["Tschernobyl, 26. April 1986: Bei einem Sicherheitstest geriet der Reaktor außer Kontrolle. Dampfexplosion, Brand des Graphit-Moderators, radioaktive Wolke über Europa. Das Gebiet ist bis heute gesperrt, seit 2016 liegt eine neue Schutzhülle darüber.",
                                   "Fukushima, 11. März 2011: Die Reaktoren schalteten sich nach dem Erdbeben ab, der Tsunami zerstörte aber die Notstromversorgung. Ohne Kühlung schmolzen drei Reaktorkerne, es kam zu Wasserstoffexplosionen.",
                                   "Auch nach dem Abschalten erzeugen die Spaltprodukte noch Wärme (Nachzerfallswärme). Deshalb muss immer gekühlt werden.",
                                   "GAU: größter anzunehmender Unfall, gegen den die Anlage ausgelegt ist. Beide Unfälle gingen darüber hinaus."], 4)
          + LAB(KERN, "Kernenergielabor", "Kurz-Check mit sechs Fragen zu Spaltung, Reaktor, Fusion und Abfall."))
S19_AB = ab_box("Übungsblatt Kernenergie", "Uebungen Kernenergie W19.pdf",
                "Steuerstäbe, Borsäure. Mo-103. 2 Neutronen. Tabelle siehe Lösungsseite. GAU: schwerster geplanter Unfall, beide Unfälle gingen darüber hinaus.", 4)

# ====================================================================== W20
A20 = tabellenfolie("Radioaktiver Abfall in Deutschland", [
    ("Zwischenlager, z. B. Neckarwestheim", "Castoren in Hallen oder Tunneln", "bis ein Endlager fertig ist"),
    ("Schacht Konrad, Salzgitter", "Endlager für schwach und mittel radioaktiven Abfall", "Fertigstellung geplant bis 2029"),
    ("Asse, Niedersachsen", "altes Salzbergwerk", "Wasser dringt ein, der Abfall soll zurückgeholt werden"),
    ("Endlager für hochradioaktiven Abfall", "Standort wird gesucht", "Gorleben ist seit 2020 aus dem Rennen"),
], kopf=("Ort", "was dort ist", "Stand"), frage="Warum ist die Suche nach einem Endlager so schwierig?")
S20 = [f(61), f(62), f(64), blatt("Radioaktiver Abfall W20.pdf", "k20", "Arbeitsblatt austeilen"), A20]
S20_HG = (box("Einstieg Leitfrage 6", ["Eine Million Jahre ist ein Zeitraum ohne Vergleich. Die Pyramiden sind etwa 4500 Jahre alt, die Neandertaler starben vor rund 40 000 Jahren aus."], 1, 2)
          + box("Abfall und Endlager", ["Schwach und mittel radioaktiver Abfall ist mengenmäßig der größte Teil, hochradioaktiver Abfall (abgebrannte Brennelemente, Glaskokillen) enthält fast die gesamte Aktivität.",
                                         "Schacht Konrad: laut Betreiber BGE soll die Anlage bis Ende 2029 fertig sein, Einlagerung Anfang der 2030er-Jahre.",
                                         "Standortsuche nach dem Gesetz von 2017: Entscheidung ursprünglich bis 2031 geplant. Die BGE rechnet inzwischen mit deutlich später. Das Endlager muss 500 Jahre lang Bergung ermöglichen und eine Million Jahre sicher sein.",
                                         "Mögliche Wirtsgesteine: Steinsalz, Ton, Kristallin (Granit). Finnland baut mit Onkalo das erste Endlager der Welt im Granit."], 3)
          + box("Rückbau", ["Beim Rückbau ist der größte Teil des Materials nicht radioaktiv und wird wiederverwertet. Kontaminierte Teile werden gereinigt, aktivierte Teile sind Abfall.",
                            "Der Rückbau eines Kraftwerks dauert 15 bis 20 Jahre und kostet rund eine Milliarde Euro."], 4)
          + LAB(KERN, "Kernenergielabor", "Wie lange strahlt der Abfall? Cäsium, Plutonium und Iod auf logarithmischer Zeitachse."))
S20_AB = ab_box("Arbeitsblatt Der radioaktive Abfall", "Radioaktiver Abfall W20.pdf",
                "Abklingbecken, Castor-Behältern, Zwischenlager, Endlager, eine Million. Anforderungen und Gesteine siehe Lösungsseite. Kontaminiert: außen, abwaschbar. Aktiviert: selbst radioaktiv.", 4)

# ====================================================================== W21
A21 = tabellenfolie("Rollen für die Diskussion", [
    ("Energieversorger", "sichere, bezahlbare Versorgung", "Strom muss auch ohne Wind und Sonne fließen."),
    ("Umweltverband", "Abfall und Unfallrisiko", "Die nächsten tausend Generationen erben den Müll."),
    ("Bürgermeisterin eines möglichen Endlagerorts", "Sicherheit der Bürger", "Warum ausgerechnet bei uns?"),
    ("Klimaforscher", "CO₂ senken", "Jede Tonne CO₂ zählt, egal woher."),
], kopf=("Rolle", "vertritt vor allem", "typischer Satz"), frage="Welche Aussagen sind Fakten, welche Meinungen?")
S21 = [f(66), blatt("Argumente abwaegen W21.pdf", "k21", "Arbeitsblatt austeilen · danach Diskussion"), A21, f(67), f(68), f(69)]
S21_HG = (box("Argumente abwägen", ["Ziel ist nicht eine richtige Meinung, sondern Argumente zu prüfen: Stimmt der Fakt? Wie groß ist die Zahl dahinter?",
                                     "Gute Fakten zum Verwenden: 24 000 Jahre Halbwertszeit Pu-239, 1 kg Uran-235 wie 3000 t Kohle, kaum CO₂ im Betrieb, Rückbau etwa eine Milliarde Euro, Endlager eine Million Jahre."], 1, 2)
          + box("Diskussion", ["Vier Gruppen ziehen je eine Rolle von der Folie. Fünf Minuten Argumente sammeln, dann je ein Sprecher. Die anderen notieren, was Fakt und was Meinung war.",
                               "Zum Schluss aus der Rolle heraustreten: eigene Stellungnahme (Aufgabe 3 auf dem Blatt)."], 3)
          + box("Abschluss Leitfrage 6", ["Antwortfolie, Check per Handzeichen. Lösung: 1 c, 2 b."], 4, 5, 6)
          + LAB(KERN, "Kernenergielabor", "Zusammenfassung und Kurz-Check zu Leitfrage 5 und 6."))
S21_AB = ab_box("Arbeitsblatt Nutzen und Risiko abwägen", "Argumente abwaegen W21.pdf",
                "Fakt, Meinung, Fakt, Meinung, Fakt, Meinung. Argumente siehe Lösungsseite. Stellungnahme individuell.", 2)

# ====================================================================== W22
A22 = tabellenfolie("Datiert mit der C-14-Methode", [
    ("Ötzi (Gletschermumie)", "etwa 5300 Jahre", "starb in der Jungsteinzeit in den Ötztaler Alpen"),
    ("„Roter Franz“ (Moorleiche, Emsland)", "etwa 1700 Jahre", "Die Haare färbten sich im Moor rot."),
    ("Turiner Grabtuch", "Mittelalter (1260 bis 1390)", "1988 in drei Laboren gemessen"),
    ("Höhlenmalereien der Chauvet-Höhle", "über 30 000 Jahre", "nahe an der Grenze der Methode"),
], kopf=("Fund", "Alter", "Besonderheit"), frage="Warum braucht man für die Messung nur ein winziges Stück des Fundes?")
S22 = [f(70), f(71), blatt("Altersbestimmung W22.pdf", "k22", "Arbeitsblatt austeilen"), A22]
S22_HG = (box("Rückblick", ["Die sechs Leitfragen noch einmal durchgehen: Jede Gruppe erklärt eine Antwort in zwei Sätzen.",
                            "Als Wiederholung eignen sich die Kurz-Checks der fünf Labore. Die Startseite Kernphysik-Labore bündelt alle."], 1)
          + box("C-14-Methode", ["C-14 entsteht in der oberen Atmosphäre aus Stickstoff durch die kosmische Strahlung. Das Verhältnis C-14 zu C-12 ist in Lebewesen so wie in der Luft.",
                                 "Nach dem Tod zerfällt C-14 mit 5730 Jahren Halbwertszeit. Die Methode reicht bis etwa 50 000 Jahre. Willard Libby erhielt dafür 1960 den Chemie-Nobelpreis.",
                                 "Die C-14-Menge in der Luft schwankte etwas, deshalb wird mit Baumringen geeicht (kalibriert).",
                                 "Tritium-Methode für Wasser (12,3 Jahre Halbwertszeit): reicht nur einige Jahrzehnte zurück."], 2)
          + LAB(ZERF, "Zerfallslabor", "C-14-Uhr mit Regler, Ötzi und Roter Franz auf der Kurve."))
S22_AB = ab_box("Arbeitsblatt Altersbestimmung mit C-14", "Altersbestimmung W22.pdf",
                "C-14, leben, 5730, Alter. 5730, 11 460, 17 190 Jahre. Ötzi knapp eine Halbwertszeit, etwa 5300 Jahre. Tritium: nach 50 Jahren nur noch etwa 6 %. Dinosaurier: über 10 000 Halbwertszeiten.", 3)

ZAEHLROHR = ("Geiger-Müller-Zählrohr mit Zählgerät", "1×", "")
STUNDEN = [
    ("W06 Wuerfelmodell", "Kernphysik: Der Zufall beim Zerfall", "W06 (Woche ab 19.10.2026) · Abschluss Leitfrage 2, Einstieg Leitfrage 3",
     "Versuchsblatt Zerfall mit Würfeln", {"demo": [], "schueler": [("Würfel", "30×", "aus der Mathe-Sammlung"), ("Würfelbecher oder Schale", "1×", "")],
                                          "hinweis": "Die Werte aller Gruppen an der Tafel addieren."},
     [("Abschluss Leitfrage 2", "Antwort ins Heft, Check.", [1, 2, 3]), ("Einstieg Leitfrage 3", "Würfel, Vermutungen.", [4, 5]),
      ("Versuch", "Würfelversuch in Gruppen, Diagramm.", [6]), ("Alltag", "Zufall im Einzelnen, sicher in der Menge.", [7])], S6, S6_HG, S6_AB),
    ("W07 Halbwertszeit", "Kernphysik: Die Halbwertszeit", "W07 (Woche ab 02.11.2026) · Leitfrage 3",
     "Arbeitsblatt Die Halbwertszeit", {"demo": [], "schueler": [("Messzylinder 250 ml", "1×", ""), ("Malzbier", "1 Flasche", "zimmerwarm"), ("Lineal", "1×", ""), ("Stoppuhr", "1×", "Handy genügt")],
                                        "hinweis": "Malzbier ist alkoholfrei. Lappen bereitlegen."},
     [("Halbwertszeit", "Kurve von Fluor-20 an der Folie.", [1]), ("Versuch", "Bierschaum messen, Arbeitsblatt.", [2]), ("Vergleich", "Halbwertszeiten und Alltag.", [3, 4])], S7, S7_HG, S7_AB),
    ("W08 Aktivitaet", "Kernphysik: Aktivität und Zählrate", "W08 (Woche ab 09.11.2026) · Leitfrage 3",
     "Arbeitsblatt Aktivität und Zählrate", {"demo": [("γ-Präparat", "1", "nur Lehrkraft, nach RiSU"), ZAEHLROHR, ("Lineal oder Maßband", "1×", ""), ("Diätsalz (Kaliumchlorid)", "1 kg", "freiwillig, aus dem Supermarkt")],
                                             "schueler": [], "hinweis": "Nullrate vor der Abstandsreihe messen."},
     [("Aktivität", "Becquerel und Zählrate an der Folie.", [1]), ("Versuch", "Abstandsreihe vorne, Arbeitsblatt.", [2]), ("Alltag", "Becquerel im Alltag, Diätsalz vor dem Zählrohr.", [3])], S8, S8_HG, S8_AB),
    ("W09 Uebungen Halbwertszeit", "Kernphysik: Übungen zur Halbwertszeit", "W09 (Woche ab 16.11.2026) · Abschluss Leitfrage 3",
     "Übungsblatt Halbwertszeit", {"demo": [], "schueler": [PSE], "hinweis": ""},
     [("Abschluss Leitfrage 3", "Antwort ins Heft, Check.", [1, 2, 3]), ("Üben", "Übungsblatt nach Schwierigkeit.", [4])], S9, S9_HG, S9_AB),
    ("W12 Ionisierende Strahlung", "Kernphysik: Warum heißt sie ionisierende Strahlung?", "W12 (Woche ab 07.12.2026) · Einstieg Leitfrage 4",
     "Arbeitsblatt Ionisierende Strahlung", {"demo": [("Nebelkammer", "1", "falls vorhanden, mit Trockeneis")], "schueler": [], "hinweis": "Ohne Nebelkammer: Szene im Wirkungslabor."},
     [("Einstieg Leitfrage 4", "Röntgenbild und Warnzeichen, Vermutungen.", [1, 2]), ("Ionisation", "Folie und Wirkungslabor.", [3]),
      ("Üben", "Arbeitsblatt.", [4]), ("Alltag", "Strahlung nachweisen.", [5])], S12, S12_HG, S12_AB),
    ("W13 Wirkung auf den Koerper", "Kernphysik: Was macht Strahlung mit dem Körper?", "W13 (Woche ab 14.12.2026) · Leitfrage 4",
     "Arbeitsblatt Wirkung auf den Körper", {"demo": [], "schueler": [], "hinweis": ""},
     [("Wirkung auf die Zelle", "Drei mögliche Folgen.", [1]), ("Strahlenbelastung", "Diagramm, Jahresdosis im Labor.", [2]),
      ("Üben", "Arbeitsblatt.", [3]), ("Alltag", "Wie viel ist ein Millisievert?", [4])], S13, S13_HG, S13_AB),
    ("W15 Schutz und Anwendungen", "Kernphysik: Schutz und Anwendungen", "W15 (Woche ab 11.01.2027) · Abschluss Leitfrage 4",
     "Arbeitsblatt Schutz und Anwendungen", {"demo": [("Röntgenbilder", "einige", "als Anschauung")], "schueler": [], "hinweis": ""},
     [("Schutz und Anwendungen", "Folie, Schutzregeln im Labor.", [1]), ("Abschluss Leitfrage 4", "Antwort ins Heft, Check.", [2, 3, 4]),
      ("Üben", "Arbeitsblatt.", [5]), ("Alltag", "Radon zu Hause.", [6])], S15, S15_HG, S15_AB),
    ("W16 Kernspaltung", "Kernphysik: Die Kernspaltung", "W16 (Woche ab 18.01.2027) · Einstieg Leitfrage 5",
     "Arbeitsblatt Die Kernspaltung", {"demo": [], "schueler": [PSE], "hinweis": ""},
     [("Einstieg Leitfrage 5", "1 kg gegen 3000 t, Vermutungen.", [1, 2]), ("Kernspaltung", "Folie und Kernenergielabor.", [3]),
      ("Üben", "Arbeitsblatt.", [4]), ("Alltag", "Kernkraft in Baden-Württemberg.", [5])], S16, S16_HG, S16_AB),
    ("W17 Kettenreaktion", "Kernphysik: Kettenreaktion und Reaktor", "W17 (Woche ab 25.01.2027) · Leitfrage 5",
     "Versuchsblatt Kettenreaktion mit Dominosteinen", {"demo": [], "schueler": [("Dominosteine", "etwa 50", "")], "hinweis": "Für Schritt 2 Platz auf dem Boden einplanen."},
     [("Kettenreaktion", "Folie, dann Dominoversuch.", [1, 2]), ("Reaktor", "Aufbau an der Folie, Steuerstäbe im Labor.", [3]), ("Alltag", "Kettenreaktionen im Alltag.", [4])], S17, S17_HG, S17_AB),
    ("W18 Kraftwerk und Fusion", "Kernphysik: Kernkraftwerk und Kernfusion", "W18 (Woche ab 01.02.2027) · Leitfrage 5",
     "Arbeitsblatt Kernkraftwerk und Kernfusion", {"demo": [], "schueler": [], "hinweis": ""},
     [("Kraftwerke", "Kernkraftwerk und Kohlekraftwerk vergleichen.", [1]), ("Kernfusion", "Folie und Labor.", [2]),
      ("Üben", "Arbeitsblatt.", [3]), ("Alltag", "Wo man an der Fusion forscht.", [4])], S18, S18_HG, S18_AB),
    ("W19 Uebungen Kernenergie", "Kernphysik: Leitfrage 5 abschließen", "W19 (Woche ab 15.02.2027) · Abschluss Leitfrage 5",
     "Übungsblatt Kernenergie", {"demo": [], "schueler": [PSE], "hinweis": ""},
     [("Abschluss Leitfrage 5", "Antwort ins Heft, Check.", [1, 2, 3]), ("Üben", "Übungsblatt, Reaktorunfälle.", [4]), ("Alltag", "Kernkraft weltweit.", [5])], S19, S19_HG, S19_AB),
    ("W20 Radioaktiver Abfall", "Kernphysik: Wohin mit dem Abfall?", "W20 (Woche ab 22.02.2027) · Einstieg Leitfrage 6",
     "Arbeitsblatt Der radioaktive Abfall", {"demo": [], "schueler": [], "hinweis": ""},
     [("Einstieg Leitfrage 6", "Zeitachse bis eine Million Jahre, Vermutungen.", [1, 2]), ("Abfall", "Folie und Labor.", [3]),
      ("Üben", "Arbeitsblatt.", [4]), ("Alltag", "Abfall in Deutschland.", [5])], S20, S20_HG, S20_AB),
    ("W21 Argumente abwaegen", "Kernphysik: Nutzen und Risiko abwägen", "W21 (Woche ab 01.03.2027) · Abschluss Leitfrage 6",
     "Arbeitsblatt Nutzen und Risiko abwägen", {"demo": [], "schueler": [], "hinweis": "Rollenfolie für die Diskussion bereithalten."},
     [("Argumente", "Folie, Fakt oder Meinung.", [1, 2]), ("Diskussion", "Vier Rollen, Sprecher, Auswertung.", [3]), ("Abschluss Leitfrage 6", "Antwort, Check.", [4, 5, 6])], S21, S21_HG, S21_AB),
    ("W22 Rueckblick und C-14", "Kernphysik: Rückblick und Altersbestimmung", "W22 (Woche ab 08.03.2027) · Abschluss Kernphysik",
     "Arbeitsblatt Altersbestimmung mit C-14", {"demo": [], "schueler": [], "hinweis": ""},
     [("Rückblick", "Die sechs Leitfragen.", [1]), ("C-14", "Folie, C-14-Uhr im Labor.", [2]), ("Üben", "Arbeitsblatt.", [3]), ("Alltag", "Datierte Funde.", [4])], S22, S22_HG, S22_AB),
]

if __name__ == "__main__":
    for kurz, h1, sub, blattname, mat, schritte, folge, hg, ab in STUNDEN:
        bau_stunde(f"Kernphysik – {kurz} – Stunde.html", h1, f"Klasse 10 · Physik · {sub}",
                   [f"{blattname}: Seite 1, eins pro Schüler.", NICHT_DRUCKEN], mat, schritte, folge, hg, ab,
                   ziel=HIER, css_href="../Optik/folien.css", extra_css=KERN_CSS)
