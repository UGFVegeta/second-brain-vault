# -*- coding: utf-8 -*-
"""Erzeugt die gedruckte Anleitung "Claude einrichten".

Kommt vor der Mietverwaltungs-Anleitung: dieses PDF richtet Claude selbst ein,
das andere danach das Paket. Stile und Helfer kommen aus ablauf_pdf.py, damit
beide Anleitungen gleich aussehen.

Stand der Installationsangaben: 17.08.2026, aus code.claude.com/docs/en/setup.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from ablauf_pdf import (
    BREITE,
    HELLGRAU,
    HOEHE,
    RAHMEN,
    RAND,
    kasten,
    punkte,
    schritt,
    st_abschnitt,
    st_fuss,
    st_mono,
    st_titel,
    st_unter,
    st_vorspann,
)

ZIEL = (
    "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/"
    "02 Projekte/Mietverwaltung/mietverwaltung/Claude einrichten.pdf"
)


def kopfzeile(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RAHMEN)
    canvas.setLineWidth(0.5)
    canvas.line(RAND, RAND - 5 * mm, BREITE - RAND, RAND - 5 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HELLGRAU)
    canvas.drawString(RAND, RAND - 9 * mm, "Claude \u00b7 Einrichtung")
    canvas.drawRightString(BREITE - RAND, RAND - 9 * mm, "Seite {}".format(doc.page))
    canvas.restoreState()


def tabelle_zwei_spalten(zeilen, breite_links=62):
    t = Table(
        [[Paragraph(a, st_mono), Paragraph(b, st_fuss)] for a, b in zeilen],
        colWidths=[breite_links * mm, None],
    )
    t.setStyle(
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
    return t


def baue():
    doc = BaseDocTemplate(
        ZIEL,
        pagesize=A4,
        leftMargin=RAND,
        rightMargin=RAND,
        topMargin=RAND,
        bottomMargin=RAND + 4 * mm,
        title="Claude einrichten",
    )
    rahmen = Frame(
        RAND, RAND + 4 * mm, BREITE - 2 * RAND, HOEHE - 2 * RAND - 4 * mm, id="haupt"
    )
    doc.addPageTemplates([PageTemplate(id="std", frames=[rahmen], onPage=kopfzeile)])

    s = []

    s.append(Paragraph("Claude einrichten", st_titel))
    s.append(
        Paragraph(
            "Der Schritt davor: von einem Windows-Rechner ohne Claude bis zur "
            "ersten Sitzung",
            st_unter,
        )
    )
    s.append(Spacer(1, 8))
    s.append(
        Paragraph(
            "Diese Anleitung kommt zuerst. Sie richtet Claude selbst ein, noch ohne "
            "Mietverwaltung. Erst wenn Claude l\u00e4uft und antwortet, geht es mit "
            "der zweiten Anleitung weiter, <b>Einrichtung Schritt f\u00fcr Schritt</b>, "
            "die den Ordner mietverwaltung in Betrieb nimmt. Zusammen etwa eine "
            "halbe Stunde, wenn der Account schon steht.",
            st_vorspann,
        )
    )
    s.append(Spacer(1, 12))

    s.append(
        kasten(
            "Claude Code ist in keinem kostenlosen Plan enthalten. Es braucht ein "
            "Abo: Pro, Max, Team oder Enterprise, oder einen Console-Zugang mit "
            "Guthaben. Ohne bezahlten Plan geht Schritt 3 nicht, und alles Weitere "
            "auch nicht. Das ist der eine Punkt, der vorher gekl\u00e4rt sein muss.",
            amber=True,
            titel="Voraussetzung, die gern \u00fcbersehen wird",
        )
    )
    s.append(Spacer(1, 12))

    s.append(Paragraph("Vorher pr\u00fcfen", st_abschnitt))
    s.extend(
        punkte(
            [
                "<b>Windows 10 Version 1809 oder neuer</b>, oder Windows 11. "
                "Mindestens 4 GB Arbeitsspeicher. Praktisch jeder Rechner der "
                "letzten Jahre erf\u00fcllt das.",
                "<b>Internetverbindung.</b> Claude rechnet nicht auf dem eigenen "
                "Rechner, jede Antwort geht \u00fcber das Netz. Die Mietdaten "
                "bleiben trotzdem lokal, nur der Gespr\u00e4chsverlauf geht raus, "
                "und auch der nur, soweit Claude die Dateien wirklich \u00f6ffnet.",
                "<b>Eine Mailadresse</b> f\u00fcr das Konto, dazu eine Zahlungsart "
                "f\u00fcr das Abo.",
                "<b>Python 3</b> braucht sp\u00e4ter nur die Mietverwaltung, nicht "
                "Claude selbst. Steht in Schritt 5.",
            ]
        )
    )
    s.append(Spacer(1, 12))

    s.extend(
        schritt(
            1,
            "Konto anlegen und Plan buchen",
            "etwa 10 Minuten, l\u00e4uft \u00fcber den Browser",
            [
                "Auf <b>claude.ai</b> ein Konto mit der eigenen Mailadresse anlegen.",
                "Danach einen Plan buchen. Zum Anfangen reicht <b>Pro</b>. Wer "
                "t\u00e4glich l\u00e4ngere Sitzungen f\u00e4hrt, st\u00f6\u00dft "
                "damit ans Limit und wechselt sp\u00e4ter auf Max. Das l\u00e4sst "
                "sich jederzeit \u00e4ndern, also klein anfangen.",
                "Passwort und Zahlungsdaten tippt der Vermieter selbst ein. Niemand "
                "sonst, auch nicht \u00fcber die Schulter diktiert.",
            ],
            hinweis="Wer schon ein Claude-Abo hat, \u00fcberspringt diesen Schritt "
            "und meldet sich in Schritt 3 einfach damit an.",
        )
    )

    s.extend(
        schritt(
            2,
            "Claude installieren",
            "etwa 5 Minuten",
            [
                "<b>Der einfache Weg: die Desktop-App.</b> Auf "
                "<b>claude.com/download</b> die Windows-Version holen und den "
                "Installer starten. Administratorrechte sind nicht n\u00f6tig. Die "
                "App ist dasselbe Claude Code, nur mit Fenster statt Kommandozeile. "
                "F\u00fcr jemanden, der nicht mit der Kommandozeile arbeitet, ist "
                "das der richtige Weg.",
                "<b>Der Weg \u00fcber das Terminal</b>, falls die App nicht "
                "gew\u00fcnscht ist: PowerShell \u00f6ffnen und eine Zeile "
                "eingeben. Welche, steht in der Tabelle am Ende.",
                "Beide Wege f\u00fchren zum selben Ergebnis. Die Skills und "
                "Grundregeln aus dem Ordner mietverwaltung greifen in beiden.",
            ],
            hinweis="Woran man PowerShell erkennt: die Zeile beginnt mit "
            "<font face='Courier'>PS C:\\</font>. Fehlt das PS, ist es die "
            "Eingabeaufforderung CMD, und der Befehl lautet anders. Deshalb im "
            "Zweifel die Desktop-App nehmen.",
        )
    )

    s.extend(
        schritt(
            3,
            "Anmelden",
            "etwa 3 Minuten",
            [
                "Die Desktop-App starten. Sie schickt einen zur Anmeldung in den "
                "Browser, dort mit dem Konto aus Schritt 1 best\u00e4tigen, fertig.",
                "Im Terminal dasselbe: <font face='Courier'>claude</font> eingeben, "
                "der Browser \u00f6ffnet sich von selbst.",
                "Das passiert einmal. Danach bleibt die Anmeldung erhalten.",
            ],
        )
    )

    s.extend(
        schritt(
            4,
            "Nachsehen, ob es wirklich l\u00e4uft",
            "etwa 2 Minuten",
            [
                "In der Desktop-App: einen beliebigen Ordner \u00f6ffnen und "
                "\u201eHallo, was kannst du hier sehen?\u201c schreiben. Kommt eine "
                "sinnvolle Antwort, steht die Installation.",
                "Im Terminal: <font face='Courier'>claude --version</font> muss eine "
                "Versionsnummer zeigen. Bei Problemen gibt "
                "<font face='Courier'>claude doctor</font> eine Diagnose aus, ohne "
                "eine Sitzung zu starten.",
                "Erst wenn das steht, weiter. Alles Folgende setzt darauf auf.",
            ],
        )
    )

    s.extend(
        schritt(
            5,
            "Python nachziehen, f\u00fcr die Mietverwaltung",
            "etwa 5 Minuten, einmalig",
            [
                "Die Mietverwaltung rechnet mit eigenen Python-Skripten, unabhängig "
                "von Claude. Ohne Python l\u00e4uft der Selbsttest nicht.",
                "<b>Das kann Claude selbst \u00fcbernehmen.</b> Einfach sagen: "
                "\u201eInstallier mir Python 3 auf diesem Rechner und pr\u00fcfe "
                "danach, ob py -3 funktioniert.\u201c Claude fragt vor jedem Befehl "
                "um Erlaubnis, man liest also mit, was passiert. Danach Claude einmal "
                "neu starten, damit die \u00c4nderung am Suchpfad ankommt.",
                "<b>Von Hand</b>, falls das nicht durchl\u00e4uft: von "
                "<b>python.org</b> die aktuelle Version f\u00fcr Windows installieren "
                "und im Installer unten das H\u00e4kchen bei "
                "<b>Add python.exe to PATH</b> setzen. Wird das vergessen, findet "
                "keiner der Doppelklick-Starter sp\u00e4ter Python.",
                "So oder so am Ende pr\u00fcfen: "
                "<font face='Courier'>py -3 --version</font> muss eine Versionsnummer "
                "zeigen.",
            ],
            hinweis="Das ist erfahrungsgem\u00e4\u00df die einzige Stelle, an der es "
            "wirklich hakeln kann, und zwar fast immer am fehlenden H\u00e4kchen beim "
            "Suchpfad. L\u00e4uft der Selbsttest der Mietverwaltung durch, ist der "
            "Rest reines Eintippen.",
        )
    )

    s.extend(
        schritt(
            6,
            "Den Ordner mietverwaltung \u00fcbernehmen",
            "etwa 2 Minuten",
            [
                "Den Ordner <b>mietverwaltung</b> auf den eigenen Rechner kopieren, "
                "am besten dorthin, wo man ihn wiederfindet, etwa nach "
                "<font face='Courier'>C:\\mietverwaltung</font>.",
                "Claude in genau diesem Ordner starten, nicht daneben. Nur dann "
                "liest er die Datei CLAUDE.md und kennt die Grundregeln und die "
                "sechs Skills.",
                "Ab hier \u00fcbernimmt die zweite Anleitung, "
                "<b>Einrichtung Schritt f\u00fcr Schritt</b>, beginnend beim "
                "Selbsttest.",
            ],
        )
    )

    s.append(Paragraph("Gut zu wissen", st_abschnitt))
    s.extend(
        punkte(
            [
                "<b>Updates laufen von selbst</b> im Hintergrund. Es gibt nichts zu "
                "pflegen.",
                "<b>Git f\u00fcr Windows ist optional.</b> Es erweitert Claude um "
                "einige Werkzeuge, wird aber f\u00fcr die Mietverwaltung nicht "
                "gebraucht. Erst installieren, wenn etwas danach verlangt.",
                "<b>PIN, TAN und Passw\u00f6rter</b> tippt immer der Vermieter "
                "selbst ein, wenn ein Skript danach fragt. Sie geh\u00f6ren in keine "
                "Datei und in kein Gespr\u00e4ch mit Claude. Das gilt dauerhaft, "
                "nicht nur bei der Einrichtung.",
                "<b>Aufh\u00f6ren ist jederzeit m\u00f6glich.</b> Nichts an dieser "
                "Einrichtung muss in einem Zug fertig werden.",
            ]
        )
    )
    s.append(Spacer(1, 10))

    # Der Block bleibt als Ganzes zusammen. Sonst steht eine einzelne
    # Tabellenzeile unten auf der Seite und der Rest auf der naechsten.
    s.append(
        KeepTogether(
            [
                Paragraph("Die Befehle im \u00dcberblick", st_abschnitt),
                tabelle_zwei_spalten(
                    [
                        (
                            "claude.com/download",
                            "Desktop-App f\u00fcr Windows, der empfohlene Weg",
                        ),
                        (
                            "irm https://claude.ai/install.ps1 | iex",
                            "Installation in <b>PowerShell</b>, erkennbar am PS am "
                            "Zeilenanfang",
                        ),
                        ("claude", "Claude im aktuellen Ordner starten"),
                        (
                            "claude --version",
                            "zeigt die Versionsnummer, Beleg dass es steht",
                        ),
                        (
                            "claude doctor",
                            "Diagnose bei Problemen, startet keine Sitzung",
                        ),
                        ("py -3 --version", "pr\u00fcft, ob Python gefunden wird"),
                    ]
                ),
                Spacer(1, 10),
                Paragraph(
                    "Angaben zur Installation gepr\u00fcft am 17.08.2026 gegen die "
                    "offizielle Dokumentation unter code.claude.com/docs. Sollte sich "
                    "ein Befehl ge\u00e4ndert haben, gilt dort das Aktuelle. Weiter "
                    "geht es mit Einrichtung Schritt f\u00fcr Schritt, "
                    "ausf\u00fchrlicher steht alles in START HIER.md und CLAUDE.md im "
                    "Ordner mietverwaltung.",
                    st_fuss,
                ),
            ]
        )
    )

    doc.build(s)
    print("PDF erzeugt:", ZIEL)


if __name__ == "__main__":
    baue()
