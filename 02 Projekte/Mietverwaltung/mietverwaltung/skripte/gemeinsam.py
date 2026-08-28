# -*- coding: utf-8 -*-
"""Gemeinsame Hilfsfunktionen fuer alle Skripte der Mietverwaltung.

Bewusst ohne Fremdbibliotheken, damit das Paket auf einem frisch
installierten Python (Windows: py -3) sofort laeuft.
"""

import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
DATEN = BASIS / "daten"
BELEGE = BASIS / "belege"
AUSGABE = BASIS

DATEIEN = {
    "konfig": "konfig.json",
    "objekte": "objekte.json",
    "mietverhaeltnisse": "mietverhaeltnisse.json",
    "darlehen": "darlehen.json",
    "fristen": "fristen.json",
    "zahlungen": "zahlungen.json",
}


def konsole_utf8():
    """Windows-Konsole auf UTF-8 stellen, sonst brechen Umlaute die Ausgabe ab."""
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def lade(name, standard=None):
    """Laedt eine Datendatei. Fehlt sie, kommt der Standardwert zurueck."""
    pfad = DATEN / DATEIEN[name]
    if not pfad.exists():
        return [] if standard is None else standard
    text = pfad.read_text(encoding="utf-8").strip()
    if not text:
        return [] if standard is None else standard
    return json.loads(text)


def speichere(name, inhalt):
    pfad = DATEN / DATEIEN[name]
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(
        json.dumps(inhalt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return pfad


# ---------------------------------------------------------------- Formatierung

def eur(betrag, nachkomma=2):
    """1234.5 -> '1.234,50 EUR' (deutsche Schreibweise)."""
    if betrag is None:
        return "-"
    text = ("{:,." + str(nachkomma) + "f}").format(float(betrag))
    text = text.replace(",", "#").replace(".", ",").replace("#", ".")
    return text + " EUR"


def eur_kurz(betrag):
    return eur(betrag, 0)


# ------------------------------------------------------------------- Parsing

_DATUMSFORMATE = ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d", "%d/%m/%Y", "%Y%m%d")


def parse_datum(wert):
    """Akzeptiert die in deutschen Bankexporten ueblichen Datumsformate."""
    if wert is None:
        return None
    if isinstance(wert, date):
        return wert
    if isinstance(wert, datetime):
        return wert.date()
    text = str(wert).strip()
    if not text:
        return None
    text = text.split("T")[0].split(" ")[0]
    for form in _DATUMSFORMATE:
        try:
            return datetime.strptime(text, form).date()
        except ValueError:
            continue
    return None


def parse_betrag(wert):
    """'1.234,56' / '-1234.56' / '1 234,56 EUR' -> float. Sonst None."""
    if wert is None:
        return None
    if isinstance(wert, (int, float)):
        return float(wert)
    text = str(wert).strip()
    if not text:
        return None
    text = text.replace(" ", " ")
    text = re.sub(r"[^\d,.\-+]", "", text)
    if not text or text in ("-", "+"):
        return None
    negativ = text.startswith("-")
    text = text.lstrip("+-")
    if "," in text and "." in text:
        # Das hintere Zeichen ist das Dezimaltrennzeichen
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(".", "").replace(",", ".")
    else:
        # Nur Punkte: '1.234' ist Tausenderpunkt, '1.23' ist Dezimalpunkt
        if re.match(r"^\d{1,3}(\.\d{3})+$", text):
            text = text.replace(".", "")
    try:
        zahl = float(text)
    except ValueError:
        return None
    return -zahl if negativ else zahl


def normiere_iban(wert):
    if not wert:
        return ""
    return re.sub(r"[^A-Z0-9]", "", str(wert).upper())


def normiere_text(wert):
    """Kleinschreibung ohne Umlaute und Sonderzeichen, fuer Textvergleiche."""
    if not wert:
        return ""
    text = str(wert).lower()
    text = (
        text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    )
    text = unicodedata.normalize("NFKD", text)
    text = "".join(z for z in text if not unicodedata.combining(z))
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# --------------------------------------------------------------------- Monate

MONATSNAMEN = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]


def monat_key(d):
    """date -> '2026-08'"""
    return "{:04d}-{:02d}".format(d.year, d.month)


def monat_lesbar(key):
    jahr, monat = key.split("-")
    return "{} {}".format(MONATSNAMEN[int(monat) - 1], jahr)


def monat_verschieben(key, schritte):
    jahr, monat = (int(t) for t in key.split("-"))
    gesamt = jahr * 12 + (monat - 1) + schritte
    return "{:04d}-{:02d}".format(gesamt // 12, gesamt % 12 + 1)


def monate_zwischen(von_key, bis_key):
    ergebnis = []
    aktuell = von_key
    while aktuell <= bis_key:
        ergebnis.append(aktuell)
        aktuell = monat_verschieben(aktuell, 1)
    return ergebnis


# ------------------------------------------------------------------- Stammdaten

def einheiten_index(objekte):
    """{einheit_id: {einheit, objekt}} fuer schnellen Zugriff."""
    index = {}
    for objekt in objekte:
        for einheit in objekt.get("einheiten", []):
            index[einheit["id"]] = {"einheit": einheit, "objekt": objekt}
    return index


def sollmiete(mv):
    """Warmmiete = Kaltmiete + Nebenkostenvorauszahlung (+ Stellplatz o.ae.)."""
    return round(
        float(mv.get("kaltmiete") or 0)
        + float(mv.get("nebenkosten_voraus") or 0)
        + float(mv.get("sonstiges_monatlich") or 0),
        2,
    )


def ist_aktiv(mv, stichtag=None):
    stichtag = stichtag or date.today()
    beginn = parse_datum(mv.get("beginn"))
    ende = parse_datum(mv.get("ende"))
    if beginn and beginn > stichtag:
        return False
    if ende and ende < stichtag:
        return False
    return True


def bezeichnung_fuer(mv, index):
    eintrag = index.get(mv.get("einheit_id"))
    if not eintrag:
        return mv.get("einheit_id") or "unbekannte Einheit"
    objekt = eintrag["objekt"]
    einheit = eintrag["einheit"]
    if einheit.get("bezeichnung"):
        return "{}, {}".format(objekt.get("bezeichnung", ""), einheit["bezeichnung"])
    return objekt.get("bezeichnung", "")


def initialen(name):
    teile = [t for t in re.split(r"[\s,]+", str(name or "")) if t]
    teile = [t for t in teile if t.lower() not in ("herr", "frau", "familie", "fam.")]
    if not teile:
        return "?"
    if len(teile) == 1:
        return teile[0][:2].upper()
    return (teile[0][0] + teile[-1][0]).upper()
