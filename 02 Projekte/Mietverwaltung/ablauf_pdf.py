# -*- coding: utf-8 -*-
"""Erzeugt die gedruckte Einrichtungsanleitung des Mietverwaltungs-Pakets.

Bewusst allgemein gehalten: Die Anleitung gehoert zum Paket und soll fuer
jeden gelten, der damit anfaengt.
"""

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ZIEL = (
    "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/"
    "02 Projekte/Mietverwaltung/mietverwaltung/Einrichtung Schritt fuer Schritt.pdf"
)

TEXT = colors.HexColor("#1a1a18")
GRAU = colors.HexColor("#5f5e5a")
HELLGRAU = colors.HexColor("#888780")
BLAU = colors.HexColor("#185fa5")
RAHMEN = colors.HexColor("#e5e3da")
KASTEN = colors.HexColor("#f9f8f3")
AMBER_BG = colors.HexColor("#faeeda")
AMBER_TX = colors.HexColor("#633806")

BREITE, HOEHE = A4
RAND = 18 * mm

st_titel = ParagraphStyle(
    "titel", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=TEXT
)
st_unter = ParagraphStyle(
    "unter", fontName="Helvetica", fontSize=11, leading=15, textColor=GRAU,
    spaceAfter=2,
)
st_vorspann = ParagraphStyle(
    "vorspann", fontName="Helvetica", fontSize=9.5, leading=14, textColor=GRAU,
)
st_abschnitt = ParagraphStyle(
    "abschnitt", fontName="Helvetica-Bold", fontSize=12.5, leading=16,
    textColor=TEXT, spaceBefore=6, spaceAfter=6,
)
st_schritt = ParagraphStyle(
    "schritt", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=TEXT,
)
st_dauer = ParagraphStyle(
    "dauer", fontName="Helvetica", fontSize=8.5, leading=11, textColor=HELLGRAU,
)
st_nummer = ParagraphStyle(
    "nummer", fontName="Helvetica-Bold", fontSize=15, leading=18,
    textColor=colors.white, alignment=1,
)
st_punkt = ParagraphStyle(
    "punkt", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=TEXT,
    leftIndent=10, bulletIndent=1, spaceAfter=2.5, alignment=TA_LEFT,
)
st_kasten = ParagraphStyle(
    "kasten", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=TEXT,
)
st_kasten_amber = ParagraphStyle(
    "kastenamber", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=AMBER_TX,
)
st_mono = ParagraphStyle(
    "mono", fontName="Courier", fontSize=8.5, leading=12.5, textColor=TEXT,
)
st_fuss = ParagraphStyle(
    "fuss", fontName="Helvetica", fontSize=8, leading=11, textColor=HELLGRAU,
)


def punkte(zeilen, stil=st_punkt):
    return [Paragraph(z, stil, bulletText="•") for z in zeilen]


def kasten(inhalt, amber=False, titel=None):
    stil = st_kasten_amber if amber else st_kasten
    innen = []
    if titel:
        innen.append(
            Paragraph(
                "<b>{}</b>".format(titel),
                ParagraphStyle("kt", parent=stil, spaceAfter=4),
            )
        )
    if isinstance(inhalt, str):
        innen.append(Paragraph(inhalt, stil))
    else:
        innen.extend(inhalt)
    tabelle = Table([[innen]], colWidths=[BREITE - 2 * RAND])
    tabelle.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG if amber else KASTEN),
                ("BOX", (0, 0), (-1, -1), 0.5, RAHMEN if not amber else AMBER_BG),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return tabelle


def schritt(nummer, titel, dauer, zeilen, hinweis=None):
    """Nummerierter Schritt mit blauem Zaehler links."""
    kopf = Table(
        [[Paragraph(str(nummer), st_nummer),
          [Paragraph(titel, st_schritt), Paragraph(dauer, st_dauer)]]],
        colWidths=[11 * mm, None],
    )
    kopf.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), BLAU),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 0),
                ("LEFTPADDING", (1, 0), (1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    # Ueberschrift und die ersten beiden Punkte bleiben zusammen, der Rest darf
    # umbrechen. Sonst rutscht ein langer Schritt komplett auf die naechste
    # Seite und laesst die vorherige halb leer.
    aufzaehlung = punkte(zeilen)
    teile = [KeepTogether([kopf, Spacer(1, 5)] + aufzaehlung[:2])]
    rest = aufzaehlung[2:]
    if hinweis:
        # Der Hinweiskasten bleibt beim letzten Punkt, sonst steht er allein
        # oben auf der Folgeseite und wirkt wie ein eigener Abschnitt.
        teile += rest[:-1]
        teile.append(
            KeepTogether(rest[-1:] + [Spacer(1, 4), kasten(hinweis, amber=True)])
        )
    else:
        teile += rest
    teile.append(Spacer(1, 11))
    return teile


def kopfzeile(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RAHMEN)
    canvas.setLineWidth(0.5)
    canvas.line(RAND, RAND - 5 * mm, BREITE - RAND, RAND - 5 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HELLGRAU)
    canvas.drawString(RAND, RAND - 9 * mm, "Mietverwaltung · Einrichtung")
    canvas.drawRightString(BREITE - RAND, RAND - 9 * mm, "Seite {}".format(doc.page))
    canvas.restoreState()


def baue():
    doc = BaseDocTemplate(
        ZIEL,
        pagesize=A4,
        leftMargin=RAND,
        rightMargin=RAND,
        topMargin=RAND,
        bottomMargin=RAND + 4 * mm,
        title="Mietverwaltung – Einrichtung Schritt für Schritt",
    )
    rahmen = Frame(
        RAND, RAND + 4 * mm, BREITE - 2 * RAND, HOEHE - 2 * RAND - 4 * mm, id="haupt"
    )
    doc.addPageTemplates([PageTemplate(id="std", frames=[rahmen], onPage=kopfzeile)])

    s = []

    s.append(Paragraph("Mietverwaltung einrichten", st_titel))
    s.append(Paragraph("Schritt für Schritt, vom leeren Ordner bis zum Dashboard", st_unter))
    s.append(Spacer(1, 8))
    s.append(
        Paragraph(
            "Ziel der ersten Sitzung ist nicht, alle Wohnungen zu erfassen, sondern "
            "dass das System nachweislich trägt. Deshalb geht zuerst ein einziges "
            "Objekt durch die ganze Kette, vom Erfassen über einen echten Kontoauszug "
            "bis ins Dashboard. Erst danach kommt der Rest der Liste. Klemmt etwas an "
            "der Zuordnung, merkt man es nach einem Objekt statt nach dreißig.",
            st_vorspann,
        )
    )
    s.append(Spacer(1, 12))

    s.append(
        kasten(
            titel="Vorher bereitlegen",
            inhalt=punkte(
                [
                    "<b>Alles Digitale, was es über die Wohnungen schon gibt</b>, in "
                    "einen Ordner sammeln: die Excel-Liste, Mietverträge als PDF, die "
                    "Aufstellung für den Steuerberater, eine Mieterliste. Das wird "
                    "ausgelesen statt abgefragt und spart die meiste Zeit.",
                    "Was nur auf Papier existiert, danebenlegen. Vor allem Kaltmiete "
                    "und Nebenkosten je Wohnung, getrennt ausgewiesen, sowie die "
                    "<b>IBAN der Mieter</b>.",
                    "Zugang zum <b>Online-Banking</b>, um einen CSV-Export zu ziehen.",
                    "Falls vorhanden: Darlehensunterlagen mit Restschuld, Zinssatz "
                    "und Ende der Zinsbindung.",
                    "<b>Git for Windows</b> installieren, von git-scm.com/download/win, "
                    "mit den Standardoptionen. Die Claude-Code-App unter Windows "
                    "braucht es zwingend für lokale Sitzungen, sie nutzt die "
                    "mitgelieferte Git-Bash als Kommandozeile. Bedienen muss man Git "
                    "nicht.",
                    "<b>Python</b> vorab installieren von python.org, beim Setup "
                    "„Add Python to PATH“ ankreuzen. Das spart später zehn Minuten.",
                ],
                ParagraphStyle("p_amber", parent=st_punkt, textColor=AMBER_TX),
            ),
            amber=True,
        )
    )
    s.append(Spacer(1, 14))

    s.append(Paragraph("Der Ablauf", st_abschnitt))

    s.extend(
        schritt(
            1,
            "Paket aufspielen und prüfen",
            "etwa 5 Minuten",
            [
                "Den Ordner <b>mietverwaltung</b> auf den eigenen Rechner kopieren, "
                "zum Beispiel nach <font face='Courier'>C:\\Mietverwaltung</font>.",
                "Doppelklick auf <b>1 Selbsttest.bat</b>.",
                "Es muss enden mit „Alles in Ordnung. Das System rechnet richtig.“ "
                "Dann stimmt alles Weitere auch.",
                "Kommt die Meldung, dass Python fehlt: von python.org installieren, "
                "dabei <b>„Add Python to PATH“ ankreuzen</b>, danach den Selbsttest "
                "wiederholen.",
            ],
            hinweis="Das ist die einzige Stelle, an der es wirklich hakeln kann. "
            "Läuft der Selbsttest, ist der Rest reines Eintippen.",
        )
    )

    s.extend(
        schritt(
            2,
            "Unterlagen einlesen und ein Objekt fertig machen",
            "20 bis 30 Minuten",
            [
                "Die vorhandenen Dateien in den Ordner <b>unterlagen</b> kopieren: "
                "Excel-Liste, Mietverträge als PDF, Aufstellungen.",
                "Claude Code in dem Ordner starten und sagen: "
                "<b>„Lies meine Unterlagen ein.“</b>",
                "Claude liest die Tabellen, zeigt was er verstanden hat, und übernimmt "
                "es erst nach Bestätigung. Kurz gegenlesen, ob die Spalten richtig "
                "gedeutet wurden.",
                "<b>Zunächst nur ein Objekt vollständig machen</b>, samt Lücken "
                "abfragen. Der Rest der Liste kommt in Schritt 4.",
                "Gibt es nichts Digitales, stattdessen sagen: <b>„Lass uns meine "
                "Objekte erfassen.“</b> Dann fragt Claude alles der Reihe nach ab.",
                "<b>Kaltmiete und Nebenkosten getrennt.</b> Steht in der Liste nur die "
                "Warmmiete, muss nachgefragt werden; für die spätere "
                "Nebenkostenabrechnung braucht es die echte Aufteilung.",
                "<b>IBAN der Mieter</b> mit übernehmen. Damit wird die Zuordnung der "
                "Zahlungen praktisch fehlerfrei.",
            ],
            hinweis="Eingescannte Verträge ohne Textebene sind reine Bilder. Daraus "
            "lässt sich nichts auslesen, diese Angaben fragt Claude ab.",
        )
    )

    s.extend(
        schritt(
            3,
            "Kontoauszug einlesen und nachsehen, ob es trägt",
            "etwa 15 Minuten · der eigentliche Test",
            [
                "Im Online-Banking die Umsätze der letzten drei bis sechs Monate "
                "als CSV exportieren.",
                "Die Datei in den Ordner <b>kontoauszuege</b> legen, dann Doppelklick "
                "auf <b>2 Kontoauszug einlesen.bat</b>.",
                "Das Ergebnis zeigt, wie viele Zahlungen eindeutig zugeordnet wurden, "
                "was als Vorschlag gilt und was unklar blieb. Für das eine erfasste "
                "Objekt müssen die Mieten sauber landen.",
                "Die unklaren Fälle mit Claude durchgehen. Das dauert je Fall Sekunden "
                "und ist beim nächsten Mal erledigt, weil sich Claude die Zuordnung "
                "merkt.",
                "Doppelklick auf <b>3 Dashboard oeffnen.bat</b>. Zu sehen sind "
                "Zahlungsstatus, Rückstände mit Verzugsdauer, Jahresverlauf, Ausgaben, "
                "Darlehen und Fristen.",
                "Das ist der Moment, der überzeugt: die eigenen Zahlen, aus dem "
                "eigenen Konto, in einer Übersicht die es vorher nicht gab.",
            ],
        )
    )

    s.extend(
        schritt(
            4,
            "Den Rest der Liste übernehmen",
            "20 bis 40 Minuten mit brauchbarer Excel-Liste",
            [
                "Claude sagen: <b>„Jetzt die restlichen Objekte übernehmen.“</b>",
                "Die komplette Tabelle wird in einem Durchgang gelesen. Eine Liste mit "
                "30 Einheiten kostet rund 1.500 Tokens, also praktisch nichts. Sie "
                "aufzuteilen bringt keinen Vorteil.",
                "Zeit braucht nur das Nachfragen der Lücken. Eine Frage lohnt immer: "
                "Ist die Liste aktuell, oder gab es seither Mieterhöhungen und "
                "Mieterwechsel? Das verhindert die meisten falschen Sollmieten.",
                "Zum Schluss prüfen lassen: <font face='Courier'>py -3 "
                "skripte\\pruefen.py</font> findet Tippfehler, doppelte Einträge und "
                "Lücken. Danach das Dashboard noch einmal bauen.",
            ],
        )
    )

    s.append(
        kasten(
            titel="Aufhören und Weitermachen ist jederzeit möglich",
            inhalt="Jedes fertige Objekt wird sofort gespeichert, es geht also nichts "
            "verloren. Nach Schritt 3 kann man aufhören und Schritt 4 später in Ruhe "
            "machen. Für den Wiedereinstieg reicht eine neue Sitzung mit „Weiter "
            "erfassen“, <font face='Courier'>py -3 skripte\\pruefen.py</font> zeigt den "
            "Stand. Teuer wird nur eines: alle Mietverträge als PDF auf Vorrat lesen zu "
            "lassen. Ein zehnseitiger Vertrag liegt bei grob 10.000 bis 16.000 Tokens. "
            "Claude ist deshalb angewiesen, einen Vertrag nur bei einer konkreten Lücke "
            "zu öffnen, und dann genau einen.",
        )
    )
    s.append(Spacer(1, 12))

    s.append(Paragraph("Bewusst nicht am ersten Tag", st_abschnitt))
    s.extend(
        punkte(
            [
                "<b>Die Bank direkt anbinden (FinTS).</b> Braucht Zugangsdaten, "
                "TAN-Verfahren und meist eine bei der Deutschen Kreditwirtschaft "
                "registrierte Produkt-ID. Manche Banken weisen unregistrierte Zugriffe "
                "ab; ob die eigene mitspielt, zeigt erst der Versuch. Das Modul liegt "
                "fertig bei, ist aber ein eigener Nachmittag. Der CSV-Weg kostet einmal "
                "im Monat eine Minute und funktioniert mit jeder Bank. Die "
                "Entscheidungshilfe steht in "
                "<font face='Courier'>doku\\Bankanbindung.md</font>.",
                "<b>Die Nebenkostenabrechnung.</b> Noch nicht gebaut. Das ist der "
                "größte nächste Brocken und die größte Zeitersparnis, hängt aber an "
                "Verteilerschlüsseln, die erst erfasst sein müssen.",
            ]
        )
    )

    s.append(PageBreak())

    s.append(Paragraph("Zum Nachschlagen", st_titel))
    s.append(Paragraph("Die Seite kann neben der Tastatur liegen bleiben.", st_unter))
    s.append(Spacer(1, 14))

    s.append(Paragraph("Falls etwas klemmt", st_abschnitt))
    s.extend(
        punkte(
            [
                "<b>„Git ist für lokale Sitzungen erforderlich.“</b> Die Claude-Code-App "
                "unter Windows verlangt Git for Windows als Kommandozeile. Im Dialog "
                "auf „Git herunterladen“ klicken, Standardoptionen, App neu starten. "
                "Nicht auf die angebotene Remote-Umgebung ausweichen, die Daten sollen "
                "lokal bleiben. Ist Git bereits installiert, aber an ungewöhnlicher "
                "Stelle, hilft die Umgebungsvariable "
                "<font face='Courier'>CLAUDE_CODE_GIT_BASH_PATH</font> mit dem vollen "
                "Pfad zur bash.exe.",
                "<b>Python fehlt oder wurde ohne PATH installiert.</b> Der mit "
                "Abstand häufigste Fall. Neu installieren mit dem Häkchen, fünf "
                "Minuten.",
                "<b>Die Excel-Datei endet auf .xls statt .xlsx.</b> Altes Format, wird "
                "nicht gelesen. In Excel einmal öffnen und als .xlsx speichern, dann "
                "geht es.",
                "<b>Die Mietverträge sind eingescannt.</b> Ein PDF ohne Textebene ist "
                "ein Bild, daraus kommt nichts. Die Angaben werden abgefragt. Wenn die "
                "Excel-Liste vollständig ist, fällt das gar nicht auf.",
                "<b>Die Bank liefert ein unbekanntes CSV-Format.</b> Dann kommt die "
                "Meldung „finde keine Spalten für Datum und Betrag“. Die Datei Claude "
                "zeigen, er ergänzt die Spaltennamen. Eine Zeile Arbeit.",
                "<b>Die Rückstände sehen zu hoch aus.</b> Meistens fehlen einfach die "
                "Kontodaten früherer Monate. Ausgewertet wird nur der Zeitraum, für "
                "den auch Umsätze vorliegen; das steht über der Tabelle.",
                "<b>Ein Mieter zahlt vom Konto des Partners.</b> Landet als Vorschlag "
                "statt als sichere Zuordnung. Einmal bestätigen, danach nie wieder.",
                "<b>Die Miete kommt Ende des Vormonats.</b> Wird dem Folgemonat "
                "zugeordnet, sofern der laufende Monat schon beglichen ist. Bei "
                "Daueraufträgen ist das der Normalfall.",
            ]
        )
    )
    s.append(Spacer(1, 12))

    s.append(Paragraph("Zwei Punkte, die man wissen sollte", st_abschnitt))
    s.extend(
        punkte(
            [
                "<b>Claude verschickt nichts.</b> Zahlungserinnerungen und Mahnungen "
                "werden entworfen und vorgelegt, abgeschickt werden sie von Hand. Das "
                "ist Absicht: In den Daten steht nie die ganze Geschichte. Wer bar "
                "bezahlt hat, mit wem eine Stundung vereinbart ist, wer gerade wegen "
                "eines Mangels mindert. Eine automatisch verschickte Mahnung in so "
                "einem Fall kostet mehr Vertrauen, als die Automatik je einspart.",
                "<b>Die Mieterdaten bleiben auf diesem Rechner.</b> Kein Server, keine "
                "Cloud, kein Konto. Der Ordner gehört in die eigene Datensicherung, "
                "denn eine zweite Kopie gibt es nirgends.",
            ]
        )
    )
    s.append(Spacer(1, 14))

    s.append(Paragraph("Die Befehle im Überblick", st_abschnitt))
    befehle = [
        ("py -3 skripte\\selbsttest.py", "prüft, ob alles richtig rechnet"),
        ("py -3 skripte\\unterlagen_lesen.py", "Excel-Listen lesbar machen"),
        ("py -3 skripte\\pruefen.py", "prüft die erfassten Daten auf Fehler"),
        ("py -3 skripte\\umsaetze_importieren.py", "Kontoauszüge einlesen und zuordnen"),
        ("py -3 skripte\\rueckstaende.py", "offene Mieten mit Verzugsdauer"),
        ("py -3 skripte\\dashboard_bauen.py", "Dashboard neu erzeugen"),
        ("py -3 skripte\\fints_abruf.py", "Umsätze direkt bei der Bank holen (später)"),
    ]
    tabelle = Table(
        [[Paragraph(b, st_mono), Paragraph(t, st_kasten)] for b, t in befehle],
        colWidths=[78 * mm, None],
    )
    tabelle.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, RAHMEN),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    s.append(tabelle)
    s.append(Spacer(1, 10))
    s.append(
        Paragraph(
            "Alles davon kann man auch einfach Claude sagen. Die Befehle stehen hier "
            "für den Fall, dass etwas klemmt und man nachsehen will. Ausführlicher "
            "steht das alles in START HIER.md und in CLAUDE.md im selben Ordner.",
            st_fuss,
        )
    )

    doc.build(s)
    print("PDF erzeugt:", ZIEL)


if __name__ == "__main__":
    baue()
