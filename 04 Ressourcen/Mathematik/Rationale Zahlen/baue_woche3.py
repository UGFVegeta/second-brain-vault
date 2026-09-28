#!/usr/bin/env python3
"""Mathe 7c, Woche 3 (28.09. bis 02.10.2026): Minus üben, Rechengesetze mit Namen, Schwerpunkt Minusklammer.
Neues Wochenformat (mathe_woche_vorlage.py). Die Aufgaben der Montagsstunde kommen aus baue_stunde3.py.
Aufruf: python3 baue_woche3.py  -> pro Stunde eine Seite „Mathe 7c – Woche 3 – N Titel.html“ und ein Folien-PDF dazu"""
import subprocess, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import bau_woche, aus_skript  # noqa: E402
from baue_stunde3 import HA, BLITZ, FOLIEN as FOLIEN_MO, FCSS, ueb_folie  # noqa: E402
import re  # noqa: E402

bogengerade, = aus_skript(HIER / "baue_stunde2.py", "bogengerade")
PDF = "Mathe 7c – Woche 3 – Folien für den Beamer.pdf"


def leere_gerade(von, bis, schritt=1, kpe=2, breite=None):
    """Nur der Zahlenstrahl zum Einzeichnen an der Tafel: ohne Bogen, ohne Startpunkt, ohne Lösung."""
    s = bogengerade(von, bis, von, 0, schritt=schritt, kpe=kpe, arc=False)
    s = re.sub(r'<circle [^>]*/><text [^>]*>[^<]*</text></svg>$', "</svg>", s)
    return s.replace('class="gerade"', f'class="gerade" style="width:{breite};height:auto"', 1) if breite else s


GERADEN = ('<div class="ausdruck">14 − 30 =</div>' + leere_gerade(-18, 16, schritt=2, breite="100%")
           + '<div class="ausdruck" style="margin-top:.25in">−3 − 9 =</div>' + leere_gerade(-14, 1, breite="90%"))
HA_PDF = HIER / "Rationale Zahlen 2 – Arbeitsblatt Plus und Minus – Lösungen (nur für mich).pdf"
BILDER = HIER / "bilder"


def ha_bilder():
    """Lösungsblatt als zwei Bildausschnitte (Aufgaben 1–3 und 4–6), ohne die Kopfzeile „nur für mich“."""
    from PIL import Image
    BILDER.mkdir(exist_ok=True)
    roh = BILDER / "_ha_loesung.png"
    subprocess.run(["pdftoppm", "-r", "250", "-png", "-singlefile", str(HA_PDF), str(roh.with_suffix(""))], check=True)
    im = Image.open(roh)
    f = im.width / 595                       # Grenzen in PDF-Punkten (A4 = 595 pt breit), gemessen mit pdftotext -bbox
    for name, (y0, y1) in {"ha-loesung-1-3.png": (96, 299), "ha-loesung-4-5.png": (299, 511), "ha-loesung-6.png": (511, 648)}.items():
        im.crop((int(30 * f), int(y0 * f), int(565 * f), int(y1 * f))).save(BILDER / name)
    roh.unlink()


def ha_folie(datei, hoehe):
    return f'<img src="bilder/{datei}" alt="" style="display:block;max-width:100%;max-height:{hoehe};margin:0 auto">'


from baue_arbeitsblatt3 import rechne, zahl, aufloesen, NAME as AB_NAME  # noqa: E402

AB_LSG = HIER / f"{AB_NAME} – Lösungen.pdf"
AB_TEILE = ["ab3-loesung-1-2.png", "ab3-loesung-3-4.png", "ab3-loesung-5-6.png", "ab3-loesung-7-8.png"]
AB_LEER_PDF = HIER / f"{AB_NAME}.pdf"
AB_LEER = ["ab3-leer-1-2.png", "ab3-leer-3-4.png", "ab3-leer-5-6.png", "ab3-leer-7-8.png"]
AUSTEILEN = '<div class="austeil">📄 Arbeitsblatt austeilen</div>'
WEITER = '<div class="austeil">📄 weiter auf dem Arbeitsblatt</div>'


def ab_bilder():
    """Arbeitsblatt Klammern als Bilder: Lösungsfassung und leere Fassung je in vier Ausschnitte (Nr. 1–2, 3–4, 5–6, 7–8),
    dazu das leere Blatt ganz. Grenzen aus pdftotext -bbox an den Aufgabenköpfen."""
    from PIL import Image
    for quelle, teile, ganz in ((AB_LSG, AB_TEILE, "ab3-loesung-ganz.png"), (AB_LEER_PDF, AB_LEER, "ab3-leer-ganz.png")):
        box = subprocess.run(["pdftotext", "-bbox", str(quelle), "-"], capture_output=True, text=True).stdout
        woerter = [(float(y0), float(y1), w) for y0, y1, w in re.findall(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">([^<]*)<', box)]
        y = lambda wort: min(y0 for y0, _, w in woerter if w == wort)
        grenzen = [y("geschickt:") - 8, y("Fasse") - 8, y("Noch") - 8, y("Setze") - 8,   # Köpfe von Nr. 1, 3, 5, 7
                   max(y1 for _, y1, _ in woerter) + 6]
        roh = BILDER / "_ab3.png"
        subprocess.run(["pdftoppm", "-r", "250", "-png", "-singlefile", str(quelle), str(roh.with_suffix(""))], check=True)
        im = Image.open(roh)
        f = im.width / 595
        for name, (y0, y1) in zip(teile, zip(grenzen, grenzen[1:])):
            im.crop((int(28 * f), int(y0 * f), int(567 * f), int(y1 * f))).save(BILDER / name)
        if ganz:
            im.crop((0, 0, im.width, int(min(im.height, (grenzen[-1] + 30) * f)))).save(BILDER / ganz)
        roh.unlink()

BUCH = {  # Buchaufgaben ohne Klammer-Schreibweise des Buchs, Ergebnisse nachgerechnet
    "S. 37 Nr. 10 (Lösungswort HECHT)": ["17 − 32 − 15", "−65 + 43 − 25", "−22 − 36 − 42", "135 − 85 − 75", "−115 + 145 − 65"],
    "S. 26 Nr. 7 rechts": ["25 − 53 − 39 + 64 − 47 + 36", "−83 + 67 + 48 + 85 − 63 − 44", "−7,1 + 9,4 − 2,2 + 8,6 − 3,7", "−15,3 + 21,8 − 32,6 + 7,5 − 26,9"],
    "S. 42 Nr. 6 (Rückspiegel)": ["−46 + 73 − 54 + 17", "84 − 67 + 48 − 33 + 52", "−5,7 + 12,8 − 23,6 + 11,2 − 1,3"],
    "S. 26 Nr. 8 links": ["23 + 77 − 62 − 28", "34 − 19 + 16 − 11", "−45 + 16 + 24 − 15", "−72 − 28 + 26 + 34"],
    "S. 25 Nr. 6 rechts": ["56 − 15 − 7 − 24", "112 − 43 − 29 − 38", "8,9 − 1,7 − 3,2 − 4,5", "6,25 − 0,96 − 1,74 − 1,12 − 2,08"],
    "S. 26 Nr. 8 rechts": ["−55 − (45 − 25) − 35", "(−55 − 45) − 25 − 35", "−55 − (45 − 25 − 35)", "−55 − 45 − (25 − 35)", "−(55 − 45) − 25 − 35"],
    "S. 26 Nr. 10 links": ["33 + (−18 + 67)", "−44 − (26 − 79) + 21", "22 − (−35 + 88) − (12 − 65)", "(−23 + 79) − 31 − (−121 + 77) − 19"],
}
EXIT = ["30 − (−20 + 36)", "54 + (−44 + 77)", "28 − (27 − 100)"]

GESETZE = ('<div class="merk">Vertauschungsgesetz (Kommutativgesetz)<br><span style="font-weight:400">In einer Rechnung mit Plus und Minus '
           'darf man die Zahlen vertauschen. Das Zeichen vor der Zahl wandert mit.<br>−26 + 47 − 14 + 3 = 47 + 3 − 26 − 14</span></div>'
           '<div class="merk">Verbindungsgesetz (Assoziativgesetz)<br><span style="font-weight:400">In einer Rechnung mit Plus und Minus '
           'darf man Zahlen beliebig mit Klammern zusammenfassen.<br>47 + 3 − 26 − 14 = (47 + 3) + (−26 − 14) = 50 − 40 = 10</span></div>')
HEFT = lambda h: f'<div class="heft">{h}</div>'      # schwarzer Balken: kommt ins Merkheft
UEB = lambda h: f'<div class="uheft">{h}</div>'      # blau gestrichelt: Übung, kommt ins Übungsheft
NEU = "−26 + 47 − 14 + 3"
NEU_FRAGE = f'<div class="ausdruck">{NEU}</div><p class="gross">Rechne möglichst geschickt. Wie gehst du vor?</p>'
MINUSKLAMMER = ('<div class="merk">Minusklammer<br><span style="font-weight:400">Steht ein Minus vor der Klammer, wird beim Auflösen '
                'aus jedem Plus in der Klammer ein Minus und aus jedem Minus ein Plus.<br>'
                '50 − (12 + 8) = 50 − 12 − 8 = 30<br>50 − (12 − 8) = 50 − 12 + 8 = 46<br>'
                'Umgekehrt kann man Zahlen, die abgezogen werden, in einer Minusklammer zusammenfassen:<br>'
                '87 − 45 − 32 − 23 = 87 − (45 + 32 + 23) = 87 − 100 = −13</span></div>')

EINKAUF = ('<p class="gross">Du hast 50 €.<br>a) Du kaufst ein Heft für 12 € und einen Stift für 8 €.<br>'
           'b) Du kaufst Getränke für 12 € und bekommst 8 € Pfand zurück.<br>Wie viel Geld hast du jeweils? Rechne auf zwei Wegen.</p>')
EINKAUF_L = ('<div class="ausdruck">a) 50 − 12 − 8 = 50 − (12 + 8) = <span class="lsg">30</span></div>'
             '<div class="ausdruck">b) 50 − 12 + 8 = 50 − (12 − 8) = <span class="lsg">46</span></div>'
             '<p>Bei b) werden die 8 € nicht abgezogen, sie kommen zurück. Deshalb steht in der Klammer − 8, aufgelöst aber + 8.</p>'
             + HEFT(MINUSKLAMMER))
FEHLER = '<div class="ausdruck">30 − (10 − 4) = 30 − 10 − 4 = 16</div><p class="gross">Stimmt das? Wo steckt der Fehler?</p>'
FEHLER_L = ('<div class="ausdruck">30 − (10 − 4) = 30 − 10 − 4 <span class="lsg">✗</span></div>'
            '<div class="ausdruck">30 − (10 − 4) = 30 − 10 + 4 = <span class="lsg">24</span></div>'
            '<p class="gross">Nur das erste Zeichen umgedreht, das zweite vergessen. Aus <b>jedem</b> Minus in der Klammer wird ein Plus.</p>')
EXIT_A = '<ol type="a" class="ex">' + "".join(f"<li>{t} =</li>" for t in EXIT) + "</ol>"
EXIT_L = '<ol type="a" class="ex">' + "".join(f"<li>{t} = {aufloesen(t)} = <span class=lsg>{zahl(rechne(t))}</span></li>" for t in EXIT) + "</ol>"
UMSORT = (f'<div class="ausdruck">{NEU} = 47 + 3 − 26 − 14</div><div class="ausdruck">= 50 − 40 = <span class="lsg">10</span></div>'
          '<p>Warum dürfen wir die Zahlen umsortieren und zusammenfassen?</p>' + HEFT(GESETZE))

AB = lambda i: ha_folie(AB_TEILE[i], "5.9in")


HA9 = [("(+9) − (+15)", "9 − 15"), ("(−28) − (−14)", "−28 + 14"), ("(+35) − (+25)", "35 − 25"),
       ("(−32) − (−40)", "−32 + 40"), ("(−1,5) − (+2,4)", "−1,5 − 2,4"), ("(+4,8) − (−6,4)", "4,8 + 6,4")]
for _t, _v in HA9:
    assert rechne(_t) == rechne(_v), _t
HA9_A = ('<p class="gross">Vereinfache die Schreibweise und berechne.<br><span style="font-size:.8em">Beispiel: (+10) − (+25) = 10 − 25 = −15</span></p>'
         '<ol type="a" class="ex">' + "".join(f"<li>{t} =</li>" for t, _ in HA9) + "</ol>")
HA9_L = ('<ol type="a" class="ex">' + "".join(f"<li>{t} = {v} = <span class=lsg>{zahl(rechne(v))}</span></li>" for t, v in HA9) + "</ol>"
         '<p>Bei b), d) und f) steht ein Minus vor einer negativen Zahl: Aus − (−14) wird + 14. Genau das passiert gleich bei der Minusklammer.</p>')


def a4(titel, pdf, bild, zeichen=""):
    """Ganze A4-Seite (Arbeitsblatt leer zum Eintragen oder Lösungsblatt) als eigene Seite im Folien-PDF."""
    return dict(titel=titel, pdf=pdf, html=zeichen + f'<img src="bilder/{bild}" alt="" style="display:block;max-width:100%;border:1px solid #ccc">')


AB_BLATT = lambda zeichen: a4("Arbeitsblatt: Klammern und Rechenvorteile", AB_LEER_PDF, "ab3-leer-ganz.png", zeichen)
AB_LOES = a4("Arbeitsblatt: Lösungen", AB_LSG, "ab3-loesung-ganz.png")
HA_TAB = "".join(f"<tr><td><b>{n}</b></td><td>{l}</td></tr>" for n, l in HA)


def buch(*keys):
    return "".join(f'<div class="box"><h3>Buch {k}</h3><ol type="a" class="kl">'
                   + "".join(f"<li>{t} = <span class=lsg>{zahl(rechne(t))}</span></li>" for t in BUCH[k]) + "</ol></div>" for k in keys)


def ab_bild(*i):
    return "".join(f'<img src="bilder/{AB_TEILE[k]}" alt="" style="max-width:100%;display:block">' for k in i)


def box(t, h):
    return f'<div class="box"><h3>{t}</h3>{h}</div>'


KEIN = '<div class="box"><p>Kein neuer Eintrag.</p></div>'
# Eine Seite pro Stunde. Name nach Inhalt, der Tag steht nur klein dabei.
STUNDEN = [
    dict(nr=1, titel="Minus üben", wann="Mo 28.09.2026, IF-Stunde (zwei Halbgruppen, beide Male gleich)",
         vorbereiten=[("Drucken", "Nichts."), ("Digital", "Folien-PDF dieser Stunde in Notability."),
                      ("Sonst", "Strichliste mit Nr. 1 bis 6, je Halbgruppe eine Spalte. Die Schüler brauchen das Arbeitsblatt (HA), "
                                "das Übungsheft und einen Stift in anderer Farbe.")],
         schritte=[("", "HA kontrollieren", 12, "Lösungen zeigen, jeder prüft selbst mit anderer Farbe. Handzeichen pro Aufgabe, "
                    "Fehlerzahl ohne Namen notieren: erster Hinweis für die spätere Einteilung nach Leistung.", [1, 2, 3]),
                   ("", "Bogen wiederholen", 4, "Zwei Minus-Aufgaben an der leeren Zahlengerade: Bogen live einzeichnen, "
                    "fragen, in welche Richtung er geht und ob er über die Null läuft.", [4]),
                   ("", "Blitzrunde Minus", 6, "Acht Aufgaben, nur Ergebnisse ins Übungsheft, selbst abhaken. 7 oder 8 richtig: gleich mit ◐ starten.", [5, 6]),
                   ("", "Üben ○◐●", 15, "Einstieg selbst wählen, Übungsheft. In der Halbgruppe ist Zeit für Einzelne.", [7, 8]),
                   ("", "Geht das schneller?", 5, "Nur Ideen sammeln. Das ist die Brücke zu den Rechengesetzen.", [9, 10])],
         folien=[("Hausaufgabe: Lösungen 1 bis 3", ha_folie("ha-loesung-1-3.png", "5.6in")),
                 ("Hausaufgabe: Lösungen 4 und 5", ha_folie("ha-loesung-4-5.png", "5.9in")),
                 ("Hausaufgabe: Lösung 6", ha_folie("ha-loesung-6.png", "5.9in")),
                 ("In welche Richtung geht der Bogen?", GERADEN)]
                + [(t, UEB(h)) if i in (0, 2, 4) else (t, h) for i, (t, h) in enumerate(FOLIEN_MO[1:])],   # Blitzrunde, Üben, Teaser: Übungsheft
         tafel=box("Die zwei typischen Fehler beim Minus",
                   '<p>Die leeren Zahlengeraden stehen auf Folie 4, du zeichnest die Bögen live ein. Bleibt an der Tafel, kommt nicht ins Merkheft.</p>'
                   f'<div class="tafel"><div class="ausdruck">14 − 30 = <span class="lsg">−16</span> <span style="font-size:16px;font-weight:400">(nicht 16: der Bogen läuft über die Null)</span></div>'
                   f'<figure>{bogengerade(-18, 16, 14, -30, schritt=2, kpe=2)}</figure>'
                   f'<div class="ausdruck">−3 − 9 = <span class="lsg">−12</span> <span style="font-size:16px;font-weight:400">(nicht +6: ohne Klammer heißt Minus einfach nach links)</span></div>'
                   f'<figure>{bogengerade(-14, 1, -3, -9, kpe=2)}</figure></div>'),
         merkheft=box("Kein neuer Eintrag", "<p>Die Regeln zum Addieren und Subtrahieren stehen seit letzter Woche im Merkheft.</p>"),
         loesungen=box("Hausaufgabe: Arbeitsblatt „Plus und Minus“", f'<table class="ha">{HA_TAB}</table>')
                   + box("Blitzrunde", '<ol type="a" class="kl">' + "".join(f"<li>{a} = <span class=lsg>{b}</span></li>" for a, b in BLITZ) + "</ol>")
                   + box("Üben ○◐●", ueb_folie(True))),
    dict(nr=2, titel="Rechengesetze, Minusklammer", wann="Di 29.09.2026, Doppelstunde",
         vorbereiten=[("Drucken", f"Arbeitsblatt „Klammern und Rechenvorteile“ in Klassenstärke ({AB_NAME}.pdf, eine Seite)."),
                      ("Digital", "Folien-PDF dieser Stunde in Notability. Das Arbeitsblatt steht darin als ganze Seite zum Eintragen, danach die Lösungsseite."),
                      ("Sonst", "Buch mitbringen lassen. Hausaufgabe war Buch S. 22 Nr. 9 links.")],
         schritte=[("", "Hausaufgabe besprechen", 10, "Buch S. 22 Nr. 9 links: Schreibweise vereinfachen. Schüler sagen die Ergebnisse, du trägst ein. "
                    "Bei b), d), f) auf das Minus vor der negativen Zahl hinweisen, das ist gleich die Minusklammer.", [1, 2]),
                   ("", "Geht das schneller?", 8, "Neue Aufgabe im Stil von Montag, erst selbst geschickt rechnen lassen.", [3]),
                   ("", "Rechengesetze", 12, "Warum dürfen wir umsortieren? Beide Gesetze mit Namen ins Merkheft.", [4]),
                   ("", "Arbeitsblatt Nr. 1 und 2", 20, "Austeilen. Nr. 2 verlangt die Namen der Gesetze. "
                    "Schnelle: Buch S. 37 Nr. 10 (Lösungswort); S. 26 Nr. 7 rechts; S. 42 Nr. 6.", [5, 8]),
                   ("", "Minusklammer", 15, "Einkaufen: Heft und Stift, dann Getränke mit Pfand. Zwei Wege vergleichen, dann ins Merkheft.", [6, 7]),
                   ("", "Arbeitsblatt Nr. 3 und 4", 20, "Minusklammer setzen und auflösen. Schnelle: Buch S. 26 Nr. 8 links; S. 25 Nr. 6 rechts.", [5, 8]),
                   ("", "Ausstieg", 5, "Stand festhalten, Rest von Nr. 3 und 4 als Hausaufgabe.", [])],
         folien=[("Hausaufgabe: Buch S. 22 Nr. 9", HA9_A), ("Hausaufgabe: Lösungen", HA9_L),
                 ("Geht das schneller?", UEB(NEU_FRAGE)), ("Warum dürfen wir umsortieren?", UMSORT), AB_BLATT(AUSTEILEN),
                 ("Einkaufen", EINKAUF), ("Einkaufen: Lösung", EINKAUF_L), AB_LOES],
         tafel=box("Umsortieren", f'<div class="tafel"><div class="ausdruck">{NEU}</div><div class="ausdruck">= 47 + 3 − 26 − 14</div>'
                   '<div class="ausdruck">= (47 + 3) + (−26 − 14)</div><div class="ausdruck">= 50 − 40 = <span class="lsg">10</span></div></div>' + HEFT(GESETZE))
               + box("Einkaufen", '<div class="tafel"><div class="ausdruck">a) 50 − 12 − 8 = 50 − (12 + 8) = <span class="lsg">30</span></div>'
                     '<div class="ausdruck">b) 50 − 12 + 8 = 50 − (12 − 8) = <span class="lsg">46</span></div>'
                     '<p>Frage an die Klasse: Warum steht bei b) in der Klammer − 8, aufgelöst aber + 8? Die 8 € kommen zurück.</p></div>' + HEFT(MINUSKLAMMER)),
         merkheft=box("Rechengesetze", f'<div class="heft">{GESETZE}</div><p style="color:#66798e">Bildungsplan Kl. 7/8/9, Teilkompetenz 9: '
                      "die Gesetze angeben und an Beispielen erläutern. Deshalb die Namen im Merkheft und auf dem Arbeitsblatt (Nr. 2).</p>")
                  + box("Minusklammer", f'<div class="heft">{MINUSKLAMMER}</div>'),
         loesungen=box("Hausaufgabe Buch S. 22 Nr. 9 links", HA9_L) + box("Arbeitsblatt Nr. 1 bis 4", ab_bild(0, 1)) + buch("S. 37 Nr. 10 (Lösungswort HECHT)", "S. 26 Nr. 7 rechts",
                                                                         "S. 42 Nr. 6 (Rückspiegel)", "S. 26 Nr. 8 links", "S. 25 Nr. 6 rechts")),
    dict(nr=3, titel="Minusklammer üben", wann="Mi 30.09.2026, Einzelstunde",
         vorbereiten=[("Drucken", "Nichts. Die Schüler arbeiten auf dem Arbeitsblatt von Dienstag weiter."),
                      ("Digital", "Folien-PDF dieser Stunde in Notability (Arbeitsblatt als ganze Seite zum Eintragen, dann Lösungsseite).")],
         schritte=[("", "Wo steckt der Fehler?", 10, "Der typische Fehler bei der Minusklammer: nur das erste Zeichen umgedreht.", [1, 2]),
                   ("", "Arbeitsblatt Nr. 5 und 6", 28, "Mehr Zahlen in der Klammer, dann Fehler finden. Schnelle: Buch S. 26 Nr. 8 rechts.", [3]),
                   ("", "Kontrolle", 7, "Schüler sagen die Ergebnisse, du trägst sie ins Blatt ein. Oder die Lösungsseite zeigen.", [3, 4])],
         folien=[("Wo steckt der Fehler?", UEB(FEHLER)), ("Wo steckt der Fehler? Lösung", FEHLER_L), AB_BLATT(WEITER), AB_LOES],
         tafel=box("Der häufigste Fehler", f'<div class="tafel">{FEHLER_L}</div>'),
         merkheft=box("Kein neuer Eintrag", "<p>Die Minusklammer von Dienstag wird geübt.</p>"),
         loesungen=box("Arbeitsblatt Nr. 5 und 6", ab_bild(2)) + buch("S. 26 Nr. 8 rechts")),
    dict(nr=4, titel="Klammern setzen, Exit-Ticket", wann="Do 01.10.2026, Einzelstunde",
         vorbereiten=[("Drucken", "Nichts. Exit-Ticket ins Übungsheft oder auf einen kleinen Zettel."),
                      ("Digital", "Folien-PDF dieser Stunde in Notability.")],
         schritte=[("", "Arbeitsblatt Nr. 7 und 8", 22, "Klammer so setzen, dass das Ergebnis stimmt; Sachaufgaben. Für ●: Buch S. 26 Nr. 10 links.", [1]),
                   ("", "Kontrolle", 8, "Ergebnisse eintragen oder die Lösungsseite zeigen.", [1, 2]),
                   ("", "Exit-Ticket", 15, "Drei Aufgaben zur Minusklammer ohne Hilfe. Zeigt, wer noch Hilfe braucht.", [3, 4])],
         folien=[AB_BLATT(WEITER), AB_LOES, ("Exit-Ticket", UEB(EXIT_A)), ("Exit-Ticket: Lösung", EXIT_L)],
         tafel=box("Kein eigenes Tafelbild", "<p>Gearbeitet wird am Blatt und am Exit-Ticket.</p>"),
         merkheft=box("Kein neuer Eintrag", "<p>Die Minusklammer von Dienstag wird geübt.</p>"),
         loesungen=box("Arbeitsblatt Nr. 7 und 8", ab_bild(3)) + buch("S. 26 Nr. 10 links") + box("Exit-Ticket", EXIT_L)),
]


def datei(st):
    return f"Mathe 7c – Woche 3 – {st['nr']} {st['titel']}.html"


def pdf(st):
    return f"Mathe 7c – Woche 3 – {st['nr']} {st['titel']}.pdf"


FOLIEN_CSS = (".merk{background:#eef3fb;border:2px solid #1a56a0;border-radius:8px;padding:10px 16px;margin:12px 0;font-weight:700;font-size:25px;line-height:1.35}"
              ".merk span{font-weight:400}.gross{font-size:34px;line-height:1.4}"
              ".ex{font-size:32px;line-height:1.45;padding-left:44px;margin:.1in 0}.ex li{margin:.06in 0}"
              ".heft{border-left:10px solid #1b1b1b;padding-left:18px;margin:10px 0}.uheft{border-left:10px dashed #1a56a0;padding-left:18px;margin:10px 0}"
              ".austeil{display:inline-block;background:#E6007E;color:#fff;font-weight:700;font-size:24px;border-radius:20px;padding:4px 18px;margin:0 0 10px}")


def folien_pdf(st, ziel):
    """Beamer-Folien (Chrome) und ganze A4-Seiten (Arbeitsblatt) in der Reihenfolge der Stunde zu einem PDF zusammensetzen."""
    from pypdf import PdfReader, PdfWriter
    w, stapel = PdfWriter(), []

    def raus():
        if not stapel:
            return
        fol = HIER / "_folien_woche3.html"
        fol.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><style>{FCSS}{FOLIEN_CSS}</style></head><body>'
                       + "".join(f'<div class="slide"><h1>{t}</h1>{h}</div>' for t, h in stapel) + "</body></html>", encoding="utf-8")
        tmp = HIER / "_folien_woche3.pdf"
        subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={tmp}", fol.as_uri()], check=True, capture_output=True)
        for seite in PdfReader(str(tmp)).pages:
            w.add_page(seite)
        fol.unlink()
        tmp.unlink()
        stapel.clear()

    for f in st["folien"]:
        if isinstance(f, dict):
            raus()
            w.add_page(PdfReader(str(f["pdf"])).pages[0])
        else:
            stapel.append(f)
    raus()
    with open(ziel, "wb") as out:
        w.write(out)
    return len(w.pages)


def main():
    ha_bilder()
    ab_bilder()
    for st in STUNDEN:
        vb = [(w, x + (f" Datei: {pdf(st)}" if w == "Digital" else "")) for w, x in st["vorbereiten"]]
        folien = [(f["titel"], f["html"]) if isinstance(f, dict) else f for f in st["folien"]]
        bau_woche(HIER / datei(st), f"Woche 3, Stunde {st['nr']}: {st['titel']}", f"Klasse 7c, Mathematik, {st['wann']}",
                  vb, st["schritte"], folien, st["tafel"], st["merkheft"], st["loesungen"])
        print("  Folien-PDF:", pdf(st), f"({folien_pdf(st, HIER / pdf(st))} Seiten)")


if __name__ == "__main__":
    main()
