#!/usr/bin/env python3
"""Neuer Aufbau der Optik-Stunden bis zu den Herbstferien (Stand 01.10.2026), Registry für stunde_vorlage.bau_stunde.
Pro Stunde: Versuchsfolien statt Schülerblatt (ersatz), Texte der Schritte (schritt_text), Druckhinweis (drucken).
Nummerierte Zeichenfolien bekommen automatisch ihre leere Zwillingsfolie (stunde_vorlage.umbauen). Blätter bleiben nur im Tab Arbeitsblätter."""
from stunde_vorlage import versuchsbeschreibung

NICHTS = ["Nichts drucken: Die Klasse zeichnet mit und schreibt ins Heft.", "Folien und Lösungen: nicht drucken."]

VERS_F2 = versuchsbeschreibung("Versuch: Blatt, Karton, Glasscheibe",
                               ["Ray-Box", "weißes Blatt Papier", "schwarzer oder dunkler Karton", "klare Glasscheibe"],
                               ["Richte die Ray-Box auf ein weißes Blatt Papier. Beobachte, was mit dem Licht passiert.",
                                "Richte die Ray-Box auf einen schwarzen Karton. Beobachte, was mit dem Licht passiert.",
                                "Halte eine klare Glasscheibe in den Lichtweg. Beobachte, was mit dem Licht passiert."])
VERS_F3 = versuchsbeschreibung("Versuch: Ray-Box und Blenden", ["Ray-Box", "Blende mit Loch", "Schirm"],
                               ["Stelle Ray-Box, eine Blende mit Loch und einen Schirm in einer Linie auf.",
                                "Verschiebe die Blende so lange, bis der Lichtpunkt auf dem Schirm erscheint.",
                                "Verschiebe die Blende seitlich, ohne Ray-Box oder Schirm zu bewegen. Beobachte den Lichtpunkt."])
VERS_F4A = versuchsbeschreibung("Versuch 1: Kern- und Halbschatten",
                                ["Ray-Box mit Lampe", "weißes Blatt Papier als Bildwand", "undurchsichtiger Körper, zum Beispiel eine Glühbirnenpackung"],
                                ["Stelle die Ray-Box mit der Lampenseite auf ein weißes Blatt Papier. Falte das Blatt so, dass eine Bildwand entsteht. Stelle den undurchsichtigen Körper vor die Lampe.",
                                 "Der Körper sollte etwa 10 cm von der Leuchtbox entfernt sein. Beobachte das Gebiet hinter dem Körper und auf der Papierfläche.",
                                 "Verschiebe den Körper näher zur Lichtquelle und entferne ihn wieder. Wie verändert sich der Schatten?"])
VERS_F4B = versuchsbeschreibung("Versuch 2: Zwei Lichtquellen",
                                ["Ray-Box", "zweite Leuchtbox, an die Buchse am Tisch angeschlossen", "weißes Blatt Papier, undurchsichtiger Körper"],
                                ["Stelle die Leuchtbox parallel zur Ray-Box auf. Schließe sie an die Buchse am Tisch an.",
                                 "Was für Veränderungen kannst du am Schatten erkennen?"])
VERS_F5 = versuchsbeschreibung("Versuch: Mondphasen im Modell",
                               ["Styroporkugel auf einem Bleistift (der Mond)", "helle Lampe vorne (die Sonne)", "dein Kopf (die Erde)"],
                               ["Stecke die Styroporkugel auf einen Bleistift. Die Lampe vorne ist die Sonne, die Kugel der Mond, dein Kopf die Erde.",
                                "Halte die Kugel mit ausgestrecktem Arm vor dein Gesicht, etwas höher als deinen Kopf.",
                                "Drehe dich langsam nach links im Kreis. Die Kugel bleibt immer vor deinem Gesicht.",
                                "Beobachte, wie viel von der beleuchteten Kugel du siehst."])
VERS_LK = versuchsbeschreibung("Versuch: Beobachtungen mit der Lochkamera",
                               ["eigene Lochkamera", "Transparentpapier", "Blenden mit größeren und kleineren Löchern", "hell erleuchtete Gegenstände, zum Beispiel Fenster oder Kerze"],
                               ["Betrachte mit der Lochkamera hell erleuchtete Gegenstände (Fenster, Kerze).",
                                "Verändere den Abstand zwischen Loch und Transparentpapier.",
                                "Setze verschiedene Blenden an die Öffnung, also größere und kleinere Löcher.",
                                "Beschreibe, wie sich Helligkeit, Schärfe und Größe des Bildes ändern."])

UMBAU = {
    "Optik – Leitfrage 1 – Stunde.html": dict(
        drucken=NICHTS + ["Optional: Arbeitsblatt Lichtquellen als Alternative, Seite 1, eins pro Schüler."],
        schritt_text={"Üben": "Lichtquellen zuordnen, mündlich. Das Arbeitsblatt Lichtquellen gibt es nur als Alternative im Tab."}),
    "Optik – Leitfrage 3 – Stunde.html": dict(
        ersatz={3: [VERS_F3]}, drucken=NICHTS + ["Optional: Versuchsblatt als Alternative, Kopiervorlage „2 auf 1“."],
        schritt_text={"Versuch": "Ray-Box und Blende in Gruppen: Beschreibung an der Folie, Beobachtung ins Heft.",
                      "Erklären": "Lichtbündel, Blende, Lichtstrahlenmodell: leere Folie zum Mitzeichnen, dann ausgefüllt. Im Strahlenlabor die zweite Blende zeigen."}),
    "Optik – Leitfrage 4 – Stunde.html": dict(
        ersatz={3: [VERS_F4A, VERS_F4B], 7: []}, drucken=NICHTS + ["Optional: Versuchsblatt doppelseitig als Alternative."],
        schritt_text={"Versuch": "In Gruppen, erst eine Lichtquelle, dann zwei: Beschreibung an den Folien, Beobachtung ins Heft.",
                      "Erklären": "Schattenraum und Schattenbild, Kern- und Halbschatten: leere Folie zum Mitzeichnen, dann ausgefüllt. Im Schattenlabor die Lampen verschieben.",
                      "Schatten einzeichnen": "In drei Schritten an der Tafel vormachen, die Klasse zeichnet mit (leere Folie, dann ausgefüllt). Die Rückseite des Versuchsblatts gibt es nur als Alternative."}),
    "Optik – Leitfrage 5 – Stunde.html": dict(
        ersatz={4: [VERS_F5]}, drucken=NICHTS + ["Optional: Versuchsblatt Mondphasen als Alternative."],
        schritt_text={"Versuch": "Kopf, Kugel, Lampe in Paaren: Beschreibung an der Folie, Beobachtung ins Heft.",
                      "Mondphasen": "Phasen von der Erde aus, 29,5 Tage: leere Folie zum Mitzeichnen, dann ausgefüllt.",
                      "Finsternisse": "Am Tellurium oder im Mondlabor, dann die Folien zum Mitzeichnen (Sonnenfinsternis, Mondfinsternis)."}),
    "Optik – Lochkamera – Stunde.html": dict(
        ersatz={3: [VERS_LK]}, drucken=NICHTS + ["Optional: Versuchsblatt Lochkamera als Alternative."],
        schritt_text={"Versuch": "Mit der eigenen Lochkamera beobachten: Beschreibung an der Folie, Beobachtung ins Heft.",
                      "Einstieg": "Im Lochkameralabor: Warum steht das Bild auf dem Kopf? Dann die Folie zum Mitzeichnen."}),
}
