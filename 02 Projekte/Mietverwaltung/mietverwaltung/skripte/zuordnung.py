# -*- coding: utf-8 -*-
"""Ordnet Kontoumsaetze automatisch den Mietverhaeltnissen zu.

Bewertet jede Buchung gegen jedes aktive Mietverhaeltnis und vergibt Punkte:

    IBAN identisch                60
    Mietername im Text            0-30
    Betrag passt zur Sollmiete    0-25
    Objekt-/Einheitsstichwort     15
    Wort "Miete" im Zweck          5

    ab 70 Punkten -> sicher, wird automatisch gebucht
    40 bis 69     -> Vorschlag, muss bestaetigt werden
    unter 40      -> bleibt unzugeordnet

Die Schwellen stehen in daten/konfig.json und koennen angepasst werden.
"""

import difflib
import re
import unicodedata

from gemeinsam import (
    bezeichnung_fuer,
    ist_aktiv,
    monat_key,
    monat_verschieben,
    normiere_iban,
    normiere_text,
    parse_datum,
    sollmiete,
)

STANDARD_SCHWELLEN = {"sicher": 70, "vorschlag": 40}


def _namensaehnlichkeit(text, name):
    """Wie gut steckt 'name' in 'text'? 0.0 bis 1.0."""
    text_n = normiere_text(text)
    name_n = normiere_text(name)
    if not text_n or not name_n:
        return 0.0
    # Anreden und Sammelbegriffe tragen nichts zur Unterscheidung bei
    stopp = {"herr", "frau", "familie", "fam", "und", "u", "eheleute", "herrn"}
    teile = [t for t in name_n.split() if t not in stopp and len(t) > 2]
    if not teile:
        return 0.0
    treffer = 0.0
    woerter = text_n.split()
    for teil in teile:
        if teil in text_n:
            treffer += 1.0
            continue
        beste = max(
            (difflib.SequenceMatcher(None, teil, wort).ratio() for wort in woerter),
            default=0.0,
        )
        if beste >= 0.82:
            treffer += beste
    return min(treffer / len(teile), 1.0)


def _stichwort_treffer(text, bezeichnung):
    """Taucht ein markantes Wort der Objektbezeichnung im Verwendungszweck auf?"""
    text_n = normiere_text(text)
    if not text_n:
        return False
    fuellwoerter = {"str", "strasse", "weg", "platz", "allee", "we", "whg", "wohnung"}
    for wort in normiere_text(bezeichnung).split():
        if len(wort) < 4 or wort in fuellwoerter or wort.isdigit():
            continue
        if wort in text_n:
            return True
    return False


def bewerte(buchung, mv, index):
    """Punkte und Begruendungen fuer ein Paar aus Buchung und Mietverhaeltnis."""
    punkte = 0
    gruende = []
    text = "{} {}".format(buchung.get("name") or "", buchung.get("zweck") or "")

    iban_buchung = normiere_iban(buchung.get("iban"))
    iban_mv = normiere_iban(mv.get("iban_mieter"))
    if iban_buchung and iban_mv and iban_buchung == iban_mv:
        punkte += 60
        gruende.append("IBAN stimmt überein")

    aehnlich = _namensaehnlichkeit(text, mv.get("mieter_name"))
    if aehnlich >= 0.99:
        punkte += 30
        gruende.append("Mietername steht im Verwendungszweck")
    elif aehnlich >= 0.5:
        punkte += int(round(30 * aehnlich))
        gruende.append("Name ähnelt dem Mieter")

    soll = sollmiete(mv)
    betrag = float(buchung.get("betrag") or 0)
    if soll > 0:
        abweichung = abs(betrag - soll)
        if abweichung < 0.01:
            punkte += 25
            gruende.append("Betrag entspricht genau der Sollmiete")
        elif abweichung <= max(5.0, soll * 0.02):
            punkte += 12
            gruende.append("Betrag liegt nah an der Sollmiete")

    if _stichwort_treffer(text, bezeichnung_fuer(mv, index)):
        punkte += 15
        gruende.append("Objekt wird im Verwendungszweck genannt")

    if "miete" in normiere_text(text):
        punkte += 5

    return punkte, gruende


# ------------------------------------------------------------ Monatserkennung

_MONATSWOERTER = {
    "januar": 1, "jan": 1, "februar": 2, "feb": 2, "maerz": 3, "mrz": 3, "mar": 3,
    "april": 4, "apr": 4, "mai": 5, "juni": 6, "jun": 6, "juli": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9, "oktober": 10,
    "okt": 10, "november": 11, "nov": 11, "dezember": 12, "dez": 12,
}


def _zweck_klein(zweck):
    """Kleinschreibung ohne Umlaute, aber mit / . - als Trennzeichen.

    normiere_text() wirft die Trennzeichen weg. Fuer die Monatserkennung
    braucht es sie aber, sonst ist '07/2026' nicht mehr von '07 2026'
    unterscheidbar und das Muster greift nicht.
    """
    text = str(zweck or "").lower()
    text = (
        text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    )
    text = unicodedata.normalize("NFKD", text)
    text = "".join(z for z in text if not unicodedata.combining(z))
    text = re.sub(r"[^a-z0-9/.\-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def erkenne_monat(zweck, buchungsdatum):
    """Sucht 'Miete 08/2026', 'August 2026', '08.2026' im Verwendungszweck.

    Gibt (monat_key, quelle) zurueck. quelle ist 'zweck' oder 'buchungsdatum'.
    Die Ziffernschreibweise hat Vorrang: In 'Miete 07/2026 plus Rest Juni'
    ist der Abrechnungsmonat Juli, nicht Juni.
    """
    text = _zweck_klein(zweck)
    jahr_fallback = buchungsdatum.year

    # Vierstelliges Jahr zuerst. Dadurch liest '01.08.2026' als 08/2026 und
    # nicht als Monat 1 des Jahres 08.
    treffer = re.search(r"\b(0?[1-9]|1[0-2])\s*[/.\-]\s*(20\d{2})\b", text)
    if not treffer:
        # Zweistelliges Jahr, bewusst auf 20xx begrenzt, sonst wird der
        # Tagesanteil eines Datums als Monat missverstanden.
        treffer = re.search(r"\b(0?[1-9]|1[0-2])\s*[/.\-]\s*(2\d)\b(?![\d./\-])", text)
    if treffer:
        monat = int(treffer.group(1))
        jahr = int(treffer.group(2))
        if jahr < 100:
            jahr += 2000
        return "{:04d}-{:02d}".format(jahr, monat), "zweck"

    for wort, monat in _MONATSWOERTER.items():
        if re.search(r"\b" + wort + r"\b", text):
            jahr_treffer = re.search(r"\b(20\d{2})\b", text)
            jahr = int(jahr_treffer.group(1)) if jahr_treffer else jahr_fallback
            return "{:04d}-{:02d}".format(jahr, monat), "zweck"

    return monat_key(buchungsdatum), "buchungsdatum"


def _monat_waehlen(buchung, mv, bereits_bezahlt):
    """Welcher Mietmonat ist gemeint?

    Steht der Monat im Verwendungszweck, gilt der. Sonst der Buchungsmonat.
    Ausnahme: Wird gegen Monatsende gebucht und ist dieser Monat schon
    beglichen, ist es fast immer die Miete fuer den Folgemonat.
    """
    datum = parse_datum(buchung.get("datum"))
    monat, quelle = erkenne_monat(buchung.get("zweck"), datum)
    if quelle == "zweck":
        return monat, True
    if datum.day >= 25 and (mv["id"], monat) in bereits_bezahlt:
        return monat_verschieben(monat, 1), False
    return monat, False


# -------------------------------------------------------------- Hauptfunktion

def ordne_zu(buchungen, mietverhaeltnisse, objekte, konfig=None):
    """Reichert jede Buchung um Zuordnung, Punkte und Begruendung an.

    Buchungen mit negativem Betrag (Ausgaben) werden nicht zugeordnet, sie
    landen als Kosten in der Liste und warten auf eine Kategorie.
    """
    from gemeinsam import einheiten_index

    konfig = konfig or {}
    schwellen = dict(STANDARD_SCHWELLEN)
    schwellen.update(konfig.get("schwellen", {}))
    index = einheiten_index(objekte)

    bezahlt = set()
    for buchung in buchungen:
        if buchung.get("mv_id") and buchung.get("monat") and buchung.get("bestaetigt"):
            bezahlt.add((buchung["mv_id"], buchung["monat"]))

    for buchung in buchungen:
        if buchung.get("bestaetigt"):
            continue  # von Hand bestaetigte Zuordnungen bleiben unangetastet

        betrag = float(buchung.get("betrag") or 0)
        datum = parse_datum(buchung.get("datum"))
        if betrag <= 0 or datum is None:
            buchung["status"] = "ausgabe" if betrag < 0 else "unklar"
            buchung["mv_id"] = None
            buchung["punkte"] = 0
            buchung["begruendung"] = []
            continue

        beste = None
        for mv in mietverhaeltnisse:
            if not ist_aktiv(mv, datum):
                continue
            punkte, gruende = bewerte(buchung, mv, index)
            if beste is None or punkte > beste[0]:
                beste = (punkte, gruende, mv)

        if beste is None or beste[0] < schwellen["vorschlag"]:
            buchung["status"] = "unklar"
            buchung["mv_id"] = None
            buchung["punkte"] = beste[0] if beste else 0
            buchung["begruendung"] = []
            continue

        punkte, gruende, mv = beste
        monat, aus_zweck = _monat_waehlen(buchung, mv, bezahlt)
        buchung["mv_id"] = mv["id"]
        buchung["monat"] = monat
        buchung["punkte"] = punkte
        buchung["begruendung"] = gruende
        buchung["status"] = "sicher" if punkte >= schwellen["sicher"] else "vorschlag"
        if buchung["status"] == "sicher":
            bezahlt.add((mv["id"], monat))

    return buchungen


def zahlungsstand(buchungen, mietverhaeltnisse, monat):
    """Soll-Ist-Vergleich fuer einen Monat, sortiert nach Objekt.

    Zaehlt sichere und bestaetigte Zuordnungen. Vorschlaege zaehlen bewusst
    nicht mit, sonst gilt eine Miete als bezahlt, die niemand geprueft hat.
    """
    eingaenge = {}
    for buchung in buchungen:
        if buchung.get("monat") != monat or not buchung.get("mv_id"):
            continue
        if buchung.get("status") not in ("sicher",) and not buchung.get("bestaetigt"):
            continue
        eingaenge.setdefault(buchung["mv_id"], []).append(buchung)

    stand = []
    for mv in mietverhaeltnisse:
        if not ist_aktiv(mv, parse_datum(monat + "-15")):
            continue
        soll = sollmiete(mv)
        treffer = eingaenge.get(mv["id"], [])
        ist = round(sum(float(b["betrag"]) for b in treffer), 2)
        if not treffer:
            status = "offen"
        elif ist + 0.01 >= soll:
            status = "bezahlt"
        else:
            status = "teilzahlung"
        stand.append(
            {
                "mv": mv,
                "soll": soll,
                "ist": ist,
                "differenz": round(ist - soll, 2),
                "status": status,
                "buchungen": treffer,
            }
        )
    return stand
