# -*- coding: utf-8 -*-
"""Liest Kontoumsaetze ein und ordnet sie den Mietverhaeltnissen zu.

Aufruf:
    py -3 skripte\\umsaetze_importieren.py                 (alles in kontoauszuege\\)
    py -3 skripte\\umsaetze_importieren.py datei.csv       (eine bestimmte Datei)

Versteht die CSV-Exporte der gaengigen deutschen Banken (Sparkasse, Volksbank,
DKB, ING, Comdirect, N26) sowie camt.052/053-XML. Die Spalten werden anhand
ihrer Ueberschriften erkannt, deshalb muss nichts umbenannt werden.

Bereits eingelesene Buchungen werden erkannt und nicht doppelt gespeichert.
Man kann also gefahrlos denselben Export noch einmal einlesen.
"""

import csv
import hashlib
import io
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from gemeinsam import (
    BASIS,
    eur,
    konsole_utf8,
    lade,
    normiere_iban,
    normiere_text,
    parse_betrag,
    parse_datum,
    speichere,
)
from zuordnung import ordne_zu

AUSZUEGE = BASIS / "kontoauszuege"

# Spaltenueberschriften der Banken, klein geschrieben und ohne Umlaute
SPALTEN = {
    "datum": [
        "buchungstag", "buchungsdatum", "datum", "valutadatum", "wertstellung",
        "wert", "booking date", "value date", "belegdatum",
    ],
    "betrag": [
        "betrag", "betrag eur", "umsatz", "amount", "betrag in eur",
        "soll haben betrag", "betrag waehrung",
    ],
    "zweck": [
        "verwendungszweck", "buchungstext", "vorgang verwendungszweck",
        "beschreibung", "verwendungszweck 1", "reference", "payment reference",
        "umsatzart", "referenz",
    ],
    "name": [
        "beguenstigter zahlungspflichtiger", "auftraggeber empfaenger",
        "name zahlungsbeteiligter", "zahlungspflichtiger", "empfaenger",
        "auftraggeber", "beguenstigter", "payee", "partner name", "name",
        "beguenstigter auftraggeber",
    ],
    "iban": [
        "kontonummer iban", "iban", "iban zahlungsbeteiligter",
        "kontonummer", "partner iban", "iban empfaenger",
    ],
    "soll_haben": ["soll haben kennzeichen", "soll haben", "debit credit"],
}


def _spalte_finden(felder, art):
    """Ordnet die Kopfzeile einer Bank den internen Feldnamen zu."""
    normiert = {normiere_text(feld): feld for feld in felder if feld}
    for kandidat in SPALTEN[art]:
        if kandidat in normiert:
            return normiert[kandidat]
    # zweiter Versuch: Teilstring, deckt 'Verwendungszweck (gekuerzt)' o.ae. ab
    for kandidat in SPALTEN[art]:
        for normiert_feld, original in normiert.items():
            if kandidat in normiert_feld:
                return original
    return None


def _text_lesen(pfad):
    """Bankexporte kommen als UTF-8, cp1252 oder latin-1. Alle drei probieren."""
    rohdaten = pfad.read_bytes()
    for kodierung in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return rohdaten.decode(kodierung)
        except UnicodeDecodeError:
            continue
    return rohdaten.decode("latin-1", errors="replace")


def _kopfzeile_finden(zeilen, trennzeichen):
    """Manche Exporte haben Vorspann. Die echte Kopfzeile enthaelt ein Datumsfeld."""
    for nummer, zeile in enumerate(zeilen[:15]):
        felder = zeile.split(trennzeichen)
        if len(felder) < 3:
            continue
        if _spalte_finden(felder, "datum") and _spalte_finden(felder, "betrag"):
            return nummer
    return 0


def lies_csv(pfad):
    text = _text_lesen(pfad)
    zeilen = [z for z in text.splitlines() if z.strip()]
    if not zeilen:
        return []

    probe = "\n".join(zeilen[:10])
    trennzeichen = max([";", ",", "\t"], key=lambda z: probe.count(z))

    start = _kopfzeile_finden(zeilen, trennzeichen)
    leser = csv.DictReader(
        io.StringIO("\n".join(zeilen[start:])), delimiter=trennzeichen
    )
    felder = leser.fieldnames or []

    sp_datum = _spalte_finden(felder, "datum")
    sp_betrag = _spalte_finden(felder, "betrag")
    if not sp_datum or not sp_betrag:
        raise ValueError(
            "In {} finde ich keine Spalten für Datum und Betrag.\n"
            "Gefundene Spalten: {}".format(pfad.name, ", ".join(felder))
        )
    sp_zweck = _spalte_finden(felder, "zweck")
    sp_name = _spalte_finden(felder, "name")
    sp_iban = _spalte_finden(felder, "iban")
    sp_sh = _spalte_finden(felder, "soll_haben")

    buchungen = []
    for zeile in leser:
        datum = parse_datum(zeile.get(sp_datum))
        betrag = parse_betrag(zeile.get(sp_betrag))
        if datum is None or betrag is None:
            continue
        if sp_sh and str(zeile.get(sp_sh, "")).strip().upper().startswith("S"):
            betrag = -abs(betrag)
        buchungen.append(
            {
                "datum": datum.isoformat(),
                "betrag": round(betrag, 2),
                "zweck": (zeile.get(sp_zweck) or "").strip(),
                "name": (zeile.get(sp_name) or "").strip(),
                "iban": normiere_iban(zeile.get(sp_iban)),
                "quelle": pfad.name,
            }
        )
    return buchungen


def lies_camt(pfad):
    """camt.052 / camt.053 XML, wie Sparkassen und Volksbanken es anbieten."""
    baum = ET.parse(str(pfad))

    def ohne_namensraum(element):
        return element.tag.split("}")[-1]

    buchungen = []
    for eintrag in baum.iter():
        if ohne_namensraum(eintrag) != "Ntry":
            continue
        betrag = None
        datum = None
        richtung = "CRDT"
        zweck_teile = []
        name = ""
        iban = ""
        for knoten in eintrag.iter():
            marke = ohne_namensraum(knoten)
            if marke == "Amt" and betrag is None:
                betrag = parse_betrag(knoten.text)
            elif marke == "CdtDbtInd":
                richtung = (knoten.text or "CRDT").strip()
            elif marke in ("BookgDt", "ValDt") and datum is None:
                for kind in knoten:
                    datum = parse_datum(kind.text) or datum
            elif marke == "Ustrd" and knoten.text:
                zweck_teile.append(knoten.text.strip())
            elif marke == "Nm" and not name and knoten.text:
                name = knoten.text.strip()
            elif marke == "IBAN" and not iban and knoten.text:
                iban = normiere_iban(knoten.text)
        if betrag is None or datum is None:
            continue
        if richtung.upper().startswith("DBIT"):
            betrag = -abs(betrag)
        buchungen.append(
            {
                "datum": datum.isoformat(),
                "betrag": round(betrag, 2),
                "zweck": " ".join(zweck_teile),
                "name": name,
                "iban": iban,
                "quelle": pfad.name,
            }
        )
    return buchungen


def fingerabdruck(buchung):
    """Erkennt dieselbe Buchung wieder, auch aus einem anderen Export."""
    roh = "|".join(
        [
            str(buchung.get("datum")),
            "{:.2f}".format(float(buchung.get("betrag") or 0)),
            normiere_iban(buchung.get("iban")),
            normiere_text(buchung.get("zweck"))[:80],
            normiere_text(buchung.get("name"))[:40],
        ]
    )
    return hashlib.sha1(roh.encode("utf-8")).hexdigest()[:16]


def dateien_sammeln(argumente):
    if argumente:
        pfade = [Path(a) for a in argumente]
        fehlend = [p for p in pfade if not p.exists()]
        if fehlend:
            raise SystemExit(
                "Diese Dateien gibt es nicht: " + ", ".join(str(p) for p in fehlend)
            )
        return pfade
    AUSZUEGE.mkdir(exist_ok=True)
    treffer = []
    for muster in ("*.csv", "*.CSV", "*.xml", "*.XML", "*.txt"):
        treffer.extend(AUSZUEGE.glob(muster))
    return sorted(treffer)


def main():
    konsole_utf8()
    dateien = dateien_sammeln(sys.argv[1:])
    if not dateien:
        print("Keine Kontoauszüge gefunden.")
        print("Lege die Exportdatei deiner Bank in den Ordner: {}".format(AUSZUEGE))
        return 0

    neue = []
    for pfad in dateien:
        try:
            if pfad.suffix.lower() == ".xml":
                gelesen = lies_camt(pfad)
            else:
                gelesen = lies_csv(pfad)
        except Exception as fehler:  # eine kaputte Datei darf den Lauf nicht kippen
            print("  ! {} übersprungen: {}".format(pfad.name, fehler))
            continue
        print("  {} → {} Buchungen".format(pfad.name, len(gelesen)))
        neue.extend(gelesen)

    bestand = lade("zahlungen", [])
    bekannt = {b.get("id") for b in bestand}

    hinzugefuegt = 0
    for buchung in neue:
        buchung["id"] = fingerabdruck(buchung)
        if buchung["id"] in bekannt:
            continue
        bekannt.add(buchung["id"])
        bestand.append(buchung)
        hinzugefuegt += 1

    objekte = lade("objekte", [])
    mietverhaeltnisse = lade("mietverhaeltnisse", [])
    konfig = lade("konfig", {})
    ordne_zu(bestand, mietverhaeltnisse, objekte, konfig)
    bestand.sort(key=lambda b: (b.get("datum") or "", b.get("id") or ""))
    speichere("zahlungen", bestand)

    sicher = sum(1 for b in bestand if b.get("status") == "sicher")
    vorschlag = sum(1 for b in bestand if b.get("status") == "vorschlag")
    unklar = sum(1 for b in bestand if b.get("status") == "unklar")
    ausgaben = sum(1 for b in bestand if b.get("status") == "ausgabe")

    print("")
    print("{} neue Buchungen übernommen, {} insgesamt.".format(hinzugefuegt, len(bestand)))
    print("  eindeutig zugeordnet: {}".format(sicher))
    print("  Vorschlag, bitte prüfen: {}".format(vorschlag))
    print("  unklar: {}".format(unklar))
    print("  Ausgaben (keine Miete): {}".format(ausgaben))

    if vorschlag or unklar:
        print("")
        print("Zu prüfen:")
        for buchung in bestand:
            if buchung.get("status") not in ("vorschlag", "unklar"):
                continue
            print(
                "  {}  {:>12}  {}  [{}]".format(
                    buchung["datum"],
                    eur(buchung["betrag"]),
                    (buchung.get("name") or buchung.get("zweck") or "")[:38],
                    buchung.get("status"),
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
