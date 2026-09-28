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


def ab_bilder():
    """Lösungsfassung des Arbeitsblatts Klammern in drei Ausschnitte (Nr. 1–3, 4–5, 6–8), Grenzen aus pdftotext -bbox."""
    from PIL import Image
    box = subprocess.run(["pdftotext", "-bbox", str(AB_LSG), "-"], capture_output=True, text=True).stdout
    woerter = [(float(y0), float(y1), w) for y0, y1, w in re.findall(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">([^<]*)<', box)]
    y = lambda wort: min(y0 for y0, _, w in woerter if w == wort)
    grenzen = [y("geschickt:") - 8, y("Fasse") - 8, y("Noch") - 8, y("Setze") - 8,   # Köpfe von Nr. 1, 3, 5, 7
               max(y1 for _, y1, _ in woerter) + 6]
    roh = BILDER / "_ab3.png"
    subprocess.run(["pdftoppm", "-r", "250", "-png", "-singlefile", str(AB_LSG), str(roh.with_suffix(""))], check=True)
    im = Image.open(roh)
    f = im.width / 595
    for name, (y0, y1) in zip(AB_TEILE, zip(grenzen, grenzen[1:])):
        im.crop((int(28 * f), int(y0 * f), int(567 * f), int(y1 * f))).save(BILDER / name)
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
           'darf man die Zahlen vertauschen. Das Zeichen vor der Zahl wandert mit.<br>−17 + 36 − 3 + 4 = 36 + 4 − 17 − 3</span></div>'
           '<div class="merk">Verbindungsgesetz (Assoziativgesetz)<br><span style="font-weight:400">In einer Rechnung mit Plus und Minus '
           'darf man Zahlen beliebig mit Klammern zusammenfassen.<br>36 + 4 − 17 − 3 = (36 + 4) + (−17 − 3) = 40 − 20 = 20</span></div>')
MINUSKLAMMER = ('<div class="merk">Minusklammer setzen<br><span style="font-weight:400">Zahlen, die alle abgezogen werden, kann man in einer '
                'Minusklammer zusammenfassen. In der Klammer steht dann Plus.<br>50 − 12 − 8 = 50 − (12 + 8) = 50 − 20 = 30</span></div>')
AUFLOESEN = ('<div class="merk">Klammer auflösen<br><span style="font-weight:400">Plus vor der Klammer: Die Zeichen in der Klammer bleiben.<br>'
             '50 + (12 − 8) = 50 + 12 − 8<br>Minus vor der Klammer: <b>Alle</b> Zeichen in der Klammer drehen sich um.<br>'
             '50 − (12 − 8) = 50 − 12 + 8 = 46</span></div>')

EINKAUF1 = ('<p class="gross">Du hast 50 €. Du kaufst ein Heft für 12 € und einen Stift für 8 €.<br>Wie viel Geld bleibt dir? Rechne auf zwei Wegen.</p>')
EINKAUF1_L = ('<div class="ausdruck">50 − 12 − 8 = <span class="lsg">30</span></div><div class="ausdruck">50 − (12 + 8) = 50 − 20 = <span class="lsg">30</span></div>'
              + MINUSKLAMMER)
EINKAUF2 = ('<p class="gross">Du hast 50 €. Du kaufst Getränke für 12 € und bekommst 8 € Pfand zurück.<br>'
            'Wie viel Geld hast du jetzt? Rechne auf zwei Wegen.</p>')
EINKAUF2_L = ('<div class="ausdruck">50 − 12 + 8 = <span class="lsg">46</span></div><div class="ausdruck">50 − (12 − 8) = 50 − 4 = <span class="lsg">46</span></div>'
              + AUFLOESEN)
EXIT_A = '<ol type="a" class="ex">' + "".join(f"<li>{t} =</li>" for t in EXIT) + "</ol>"
EXIT_L = '<ol type="a" class="ex">' + "".join(f"<li>{t} = {aufloesen(t)} = <span class=lsg>{zahl(rechne(t))}</span></li>" for t in EXIT) + "</ol>"
UMSORT = ('<div class="ausdruck">−17 + 36 − 3 + 4</div><p>Warum durften wir am Montag die Zahlen umsortieren und zusammenfassen?</p>'
          + GESETZE)

AB = lambda i: ha_folie(AB_TEILE[i], "5.9in")
TEASER, TEASER_L = FOLIEN_MO[-2], FOLIEN_MO[-1]
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
                 ("In welche Richtung geht der Bogen?", GERADEN)] + FOLIEN_MO[1:],
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
    dict(nr=2, titel="Rechengesetze, Minusklammer setzen", wann="Di 29.09.2026, Doppelstunde",
         vorbereiten=[("Drucken", f"Arbeitsblatt „Klammern und Rechenvorteile“ in Klassenstärke ({AB_NAME}.pdf, eine Seite)."),
                      ("Digital", "Folien-PDF dieser Stunde in Notability."), ("Sonst", "Buch mitbringen lassen.")],
         schritte=[("", "Minus sicher: Lösungswort", 12, "Buch S. 37 Nr. 10 ins Übungsheft, Lösungswort HECHT.", []),
                   ("", "Warum durften wir umsortieren?", 15, "Die Aufgabe von Montag aufgreifen. Daraus die zwei Gesetze mit Namen ins Merkheft.", [1, 2]),
                   ("", "Gesetze anwenden und benennen", 25, "Arbeitsblatt austeilen, Nr. 1 und 2. Schnelle: Buch S. 26 Nr. 7 rechts; S. 42 Nr. 6.", []),
                   ("", "Minusklammer setzen", 25, "Einkaufen 1, Regel ins Merkheft, dann Arbeitsblatt Nr. 3. "
                    "Schnelle: Buch S. 26 Nr. 8 links; S. 25 Nr. 6 rechts.", [3, 4]),
                   ("", "Ausstieg", 5, "Hausaufgabe: Arbeitsblatt Nr. 1 bis 3 fertig.", [])],
         folien=[TEASER, ("Warum durften wir umsortieren?", UMSORT), ("Einkaufen 1", EINKAUF1), ("Einkaufen 1: Lösung", EINKAUF1_L)],
         tafel=box("Umsortieren", '<div class="tafel"><div class="ausdruck">−17 + 36 − 3 + 4</div><div class="ausdruck">= 36 + 4 − 17 − 3</div>'
                   '<div class="ausdruck">= (36 + 4) + (−17 − 3)</div><div class="ausdruck">= 40 − 20 = <span class="lsg">20</span></div></div>' + GESETZE)
               + box("Einkaufen 1: Heft 12 €, Stift 8 €", '<div class="tafel"><div class="ausdruck">50 − 12 − 8 = 50 − (12 + 8) = <span class="lsg">30</span></div></div>'),
         merkheft=box("Rechengesetze", f'<div class="heft">{GESETZE}</div><p style="color:#66798e">Bildungsplan Kl. 7/8/9, Teilkompetenz 9: '
                      "die Gesetze angeben und an Beispielen erläutern. Deshalb die Namen im Merkheft und auf dem Arbeitsblatt (Nr. 2).</p>")
                  + box("Minusklammer setzen", f'<div class="heft">{MINUSKLAMMER}</div>'),
         loesungen=box("Arbeitsblatt Nr. 1 bis 3", ab_bild(0, 1)) + buch("S. 37 Nr. 10 (Lösungswort HECHT)", "S. 26 Nr. 7 rechts",
                                                                         "S. 42 Nr. 6 (Rückspiegel)", "S. 26 Nr. 8 links", "S. 25 Nr. 6 rechts")),
    dict(nr=3, titel="Minusklammer auflösen", wann="Mi 30.09.2026, Einzelstunde",
         vorbereiten=[("Drucken", "Nichts."), ("Digital", f"Folien-PDF dieser Stunde in Notability. Ganzes Lösungsblatt: {AB_NAME} – Lösungen.pdf.")],
         schritte=[("", "HA kontrollieren", 8, "Lösungen im ausgefüllten Blatt zeigen, selbst kontrollieren.", [1, 2]),
                   ("", "Minusklammer auflösen", 12, "Einkaufen 2 mit Pfand. Warum wird aus − 8 in der Klammer + 8? Regel ins Merkheft.", [3, 4]),
                   ("", "Üben", 22, "Arbeitsblatt Nr. 4 und 5.", []),
                   ("", "Kontrolle", 3, "Lösungen zu Nr. 4 und 5 zeigen.", [2, 5])],
         folien=[("Arbeitsblatt: Lösungen 1 und 2", AB(0)), ("Arbeitsblatt: Lösungen 3 und 4", AB(1)),
                 ("Einkaufen 2: mit Pfand", EINKAUF2), ("Einkaufen 2: Lösung", EINKAUF2_L), ("Arbeitsblatt: Lösungen 5 und 6", AB(2))],
         tafel=box("Einkaufen 2: Getränke 12 €, 8 € Pfand zurück",
                   '<div class="tafel"><div class="ausdruck">50 − 12 + 8 = 50 − (12 − 8) = <span class="lsg">46</span></div>'
                   '<p>Frage an die Klasse: Warum steht in der Klammer − 8, draußen aber + 8? Antwort: Die 8 € werden nicht abgezogen, sondern kommen zurück. '
                   'Minus vor der Klammer dreht das Zeichen um.</p></div>'),
         merkheft=box("Klammer auflösen", f'<div class="heft">{AUFLOESEN}</div>'),
         loesungen=box("Arbeitsblatt Nr. 1 bis 6", ab_bild(0, 1, 2))),
    dict(nr=4, titel="Minusklammer üben, Exit-Ticket", wann="Do 01.10.2026, Einzelstunde",
         vorbereiten=[("Drucken", "Nichts. Exit-Ticket ins Übungsheft oder auf einen kleinen Zettel."), ("Digital", "Folien-PDF dieser Stunde in Notability.")],
         schritte=[("", "Typische Fehler", 10, "Arbeitsblatt Nr. 6 gemeinsam: Wer dreht nur das erste Zeichen um?", [1]),
                   ("", "Üben nach Wahl", 25, "Arbeitsblatt Nr. 7 und 8. Für ●: Buch S. 26 Nr. 8 rechts; S. 26 Nr. 10 links.", [2]),
                   ("", "Exit-Ticket", 10, "Drei Aufgaben zur Minusklammer ohne Hilfe. Zeigt, wer noch Hilfe braucht.", [3, 4])],
         folien=[("Arbeitsblatt: Lösungen 5 und 6", AB(2)), ("Arbeitsblatt: Lösungen 7 und 8", AB(3)),
                 ("Exit-Ticket", EXIT_A), ("Exit-Ticket: Lösung", EXIT_L)],
         tafel=box("Der häufigste Fehler", '<div class="tafel"><div class="ausdruck">30 − (10 − 4) = 30 − 10 − 4 <span class="lsg">✗</span></div>'
                   '<div class="ausdruck">30 − (10 − 4) = 30 − 10 + 4 = <span class="lsg">24</span></div>'
                   '<p>Nur das erste Zeichen umgedreht, das zweite vergessen. <b>Alle</b> Zeichen in der Klammer drehen sich um.</p></div>'),
         merkheft=box("Kein neuer Eintrag", "<p>Die Regel von Mittwoch (Klammer auflösen) wird nur wiederholt.</p>"),
         loesungen=box("Arbeitsblatt Nr. 5 bis 8", ab_bild(2, 3)) + buch("S. 26 Nr. 8 rechts", "S. 26 Nr. 10 links") + box("Exit-Ticket", EXIT_L)),
]


def datei(st):
    return f"Mathe 7c – Woche 3 – {st['nr']} {st['titel']}.html"


def pdf(st):
    return f"Mathe 7c – Woche 3 – {st['nr']} {st['titel']}.pdf"


FOLIEN_CSS = (".merk{background:#eef3fb;border:2px solid #1a56a0;border-radius:8px;padding:10px 16px;margin:12px 0;font-weight:700;font-size:25px;line-height:1.35}"
              ".merk span{font-weight:400}.gross{font-size:34px;line-height:1.4}"
              ".ex{font-size:36px;line-height:1.6;padding-left:44px}.ex li{margin:.12in 0}")


def main():
    ha_bilder()
    ab_bilder()
    for st in STUNDEN:
        vb = [(w, x + (f" Datei: {pdf(st)}" if w == "Digital" else "")) for w, x in st["vorbereiten"]]
        bau_woche(HIER / datei(st), f"Woche 3, Stunde {st['nr']}: {st['titel']}", f"Klasse 7c, Mathematik, {st['wann']}",
                  vb, st["schritte"], st["folien"], st["tafel"], st["merkheft"], st["loesungen"])
        fol = HIER / "_folien_woche3.html"
        fol.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><style>{FCSS}{FOLIEN_CSS}</style></head><body>'
                       + "".join(f'<div class="slide"><h1>{t}</h1>{h}</div>' for t, h in st["folien"]) + "</body></html>", encoding="utf-8")
        subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={HIER / pdf(st)}", fol.as_uri()], check=True, capture_output=True)
        fol.unlink()
        print("  Folien-PDF:", pdf(st), f"({len(st['folien'])} Folien)")


if __name__ == "__main__":
    main()
