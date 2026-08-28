# -*- coding: utf-8 -*-
"""Prueft, ob die Mietverwaltung auf diesem Rechner sauber laeuft.

Aufruf:
    py -3 skripte\\selbsttest.py

Rechnet den Beispieldatensatz durch und vergleicht das Ergebnis mit dem, was
herauskommen muss. Ruehrt daten\\ nicht an. Laeuft das hier durch, funktioniert
die Zuordnung auch mit echten Daten.
"""

import json
import sys
from pathlib import Path

from gemeinsam import DATEN, konsole_utf8, parse_betrag, parse_datum
from umsaetze_importieren import lies_csv
from zuordnung import erkenne_monat, ordne_zu, zahlungsstand

BEISPIEL = DATEN / "beispiel"

fehler = []


def pruefe(bedingung, beschreibung, zusatz=""):
    if bedingung:
        print("  ok    {}".format(beschreibung))
    else:
        print("  FEHLT {} {}".format(beschreibung, zusatz))
        fehler.append(beschreibung)


FORMATE = {
    "DKB, mit Vorspann und Spalte Betrag (EUR)": (
        '"Kontonummer:";"DE00 1203 0000 0000 2020 51 / Girokonto";\n'
        '\n'
        '"Von:";"01.08.2026";\n'
        '\n'
        '"Buchungstag";"Wertstellung";"Buchungstext";"Auftraggeber / Begünstigter";'
        '"Verwendungszweck";"Kontonummer";"BLZ";"Betrag (EUR)"\n'
        '"01.08.2026";"01.08.2026";"DAUERAUFTRAG";"Kramer, Thomas";'
        '"Miete 08/2026";"DE02120300000000202051";"";"920,00"\n',
        [("2026-08-01", 920.0)],
    ),
    "N26, englische Spalten und Punkt als Dezimaltrenner": (
        '"Booking Date","Value Date","Partner Name","Partner Iban","Type",'
        '"Payment Reference","Amount (EUR)"\n'
        '"2026-08-01","2026-08-01","Sanchez, Maria","DE02300209000106531065",'
        '"Credit Transfer","Miete 08/2026","1450.00"\n'
        '"2026-08-11","2026-08-11","Sanitaer Vogt","DE02640500000001234567",'
        '"Debit Transfer","Rechnung 4471","-612.50"\n',
        [("2026-08-01", 1450.0), ("2026-08-11", -612.5)],
    ),
    "Sparkasse, Vorzeichen über Soll/Haben-Kennzeichen": (
        "Auftragskonto;Buchungstag;Valuta;Buchungstext;Verwendungszweck;"
        "Beguenstigter/Zahlungspflichtiger;Kontonummer/IBAN;Betrag;Waehrung;"
        "Soll/Haben-Kennzeichen\n"
        "DE00123456780000000000;04.08.2026;04.08.2026;UEBERWEISUNG;Miete August;"
        "Adler, Peter;DE02200505501015871393;800,00;EUR;H\n"
        "DE00123456780000000000;12.08.2026;12.08.2026;LASTSCHRIFT;Grundsteuer Q3;"
        "Stadtkasse;DE02660501010009999999;198,00;EUR;S\n",
        [("2026-08-04", 800.0), ("2026-08-12", -198.0)],
    ),
}


def pruefe_bankformate():
    """Liest je einen kurzen Auszug im Format verschiedener Banken."""
    import tempfile

    with tempfile.TemporaryDirectory() as ordner:
        for beschreibung, (inhalt, erwartet) in FORMATE.items():
            pfad = Path(ordner) / "auszug.csv"
            pfad.write_text(inhalt, encoding="utf-8")
            try:
                gelesen = lies_csv(pfad)
                tatsaechlich = [(b["datum"], b["betrag"]) for b in gelesen]
            except Exception as fehler:
                pruefe(False, beschreibung, str(fehler))
                continue
            pruefe(tatsaechlich == erwartet, beschreibung, "war " + str(tatsaechlich))


def pruefe_excel():
    """Liest die Beispielmappe, ohne dass Zusatzsoftware installiert ist."""
    from unterlagen_lesen import Mappe

    pfad = BEISPIEL / "Wohnungen Beispiel.xlsx"
    if not pfad.exists():
        pruefe(False, "Beispielmappe vorhanden", str(pfad))
        return
    try:
        mappe = Mappe(pfad)
        blaetter = mappe.blaetter()
        namen = [name for name, _ in blaetter]
        pruefe(namen == ["Objekte", "Mieter"], "beide Tabellenblätter gefunden",
               "waren " + str(namen))

        zeilen = dict(mappe.zeilen(blaetter[1][1]))
        erste = zeilen.get(2, [])
        pruefe(
            len(erste) >= 7 and erste[2] == "Familie Kramer",
            "Text aus der Mappe wird gelesen",
            str(erste[:3]),
        )
        pruefe(erste[3] == "680", "Zahlen kommen ohne Nachkommastellen an",
               "war " + str(erste[3] if len(erste) > 3 else "?"))
        pruefe(
            erste[5] == "2018-03-01",
            "Datumsfelder werden aus der Excel-Zahl zurückgerechnet",
            "war " + str(erste[5] if len(erste) > 5 else "?"),
        )
    except Exception as fehler:
        pruefe(False, "Beispielmappe lesbar", str(fehler))


def main():
    konsole_utf8()
    print("Selbsttest Mietverwaltung")
    print("")

    print("Python")
    pruefe(sys.version_info >= (3, 8), "Python 3.8 oder neuer", sys.version.split()[0])
    print("")

    print("Zahlen und Datumsangaben aus Bankexporten")
    pruefe(parse_betrag("1.234,56") == 1234.56, "1.234,56 wird zu 1234.56")
    pruefe(parse_betrag("-742,80") == -742.80, "negative Beträge")
    pruefe(parse_betrag("1234.56") == 1234.56, "englische Schreibweise")
    pruefe(str(parse_datum("03.08.2026")) == "2026-08-03", "Datum 03.08.2026")
    pruefe(str(parse_datum("2026-08-03")) == "2026-08-03", "Datum 2026-08-03")
    print("")

    print("Monatserkennung im Verwendungszweck")
    heute = parse_datum("2026-08-15")
    faelle = [
        ("Miete 07/2026 sowie Restbetrag Juni", "2026-07"),
        ("Miete August 2026", "2026-08"),
        ("Mietzahlung Juni", "2026-06"),
        ("Miete Bahnhofstr 7 WE1 06/26", "2026-06"),
        ("Dauerauftrag", "2026-08"),
    ]
    for zweck, erwartet in faelle:
        ergebnis, _ = erkenne_monat(zweck, heute)
        pruefe(ergebnis == erwartet, "„{}“ → {}".format(zweck, erwartet), "war " + ergebnis)
    print("")

    print("Fremde Bankformate")
    pruefe_bankformate()
    print("")

    print("Excel-Mappen lesen")
    pruefe_excel()
    print("")

    print("Beispieldatensatz")
    csv_datei = BEISPIEL / "kontoauszug_beispiel.csv"
    pruefe(csv_datei.exists(), "Beispiel-Kontoauszug vorhanden")
    if not csv_datei.exists():
        return 1

    buchungen = lies_csv(csv_datei)
    pruefe(len(buchungen) == 21, "21 Buchungen eingelesen", "waren " + str(len(buchungen)))

    objekte = json.loads((BEISPIEL / "objekte.json").read_text(encoding="utf-8"))
    mvs = json.loads((BEISPIEL / "mietverhaeltnisse.json").read_text(encoding="utf-8"))
    ordne_zu(buchungen, mvs, objekte, {})

    sicher = [b for b in buchungen if b.get("status") == "sicher"]
    pruefe(len(sicher) == 14, "14 Mietzahlungen sicher zugeordnet", "waren " + str(len(sicher)))

    ausgaben = [b for b in buchungen if b.get("status") == "ausgabe"]
    pruefe(len(ausgaben) == 6, "6 Ausgaben erkannt", "waren " + str(len(ausgaben)))

    # Zahlung vom Konto der Ehefrau muss trotzdem beim richtigen Mieter landen
    fremdkonto = [b for b in buchungen if "Adler-Weiss" in (b.get("name") or "")]
    pruefe(
        len(fremdkonto) == 1 and fremdkonto[0].get("mv_id") == "mv-005",
        "Zahlung von fremder IBAN wird über den Namen zugeordnet",
    )

    # Teilzahlung muss als solche auffallen, nicht als bezahlt gelten
    stand = zahlungsstand(buchungen, mvs, "2026-08")
    adler = [s for s in stand if s["mv"]["id"] == "mv-005"]
    pruefe(
        len(adler) == 1 and adler[0]["status"] == "teilzahlung" and adler[0]["differenz"] == -75.0,
        "Teilzahlung von 800 statt 875 wird erkannt",
    )
    novak = [s for s in stand if s["mv"]["id"] == "mv-003"]
    pruefe(
        len(novak) == 1 and novak[0]["status"] == "offen",
        "fehlende Miete wird als offen geführt",
    )
    print("")

    if fehler:
        print("{} Prüfung(en) fehlgeschlagen.".format(len(fehler)))
        print("Bitte Claude zeigen, bevor echte Daten eingetragen werden.")
        return 1
    print("Alles in Ordnung. Das System rechnet richtig.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
