# -*- coding: utf-8 -*-
"""Macht vorhandene Unterlagen fuer Claude lesbar.

Aufruf:
    py -3 skripte\\unterlagen_lesen.py                 (alles in unterlagen\\)
    py -3 skripte\\unterlagen_lesen.py mappe.xlsx      (eine bestimmte Datei)

Wer seine Wohnungen schon in einer Excel-Liste hat, muss sie nicht noch einmal
vorlesen. Dieses Skript wandelt Tabellen in Text um, den Claude direkt lesen
und in die Stammdaten uebernehmen kann.

Was womit geht:
    .xlsx, .xlsm   werden hier ausgelesen, ohne Zusatzsoftware
    .csv, .txt     kann Claude ohnehin direkt lesen
    .pdf           kann Claude ohnehin direkt lesen, sofern Text enthalten ist
    .xls (alt)     geht nicht, in Excel einmal als .xlsx speichern
    .doc, .docx    kann Claude meist direkt lesen

Eingescannte PDFs ohne Textebene sind reine Bilder. Daraus laesst sich nichts
uebernehmen; die betroffenen Angaben muessen abgefragt werden.
"""

import re
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

from gemeinsam import BASIS, konsole_utf8

UNTERLAGEN = BASIS / "unterlagen"

# Excel zaehlt Tage ab dem 30.12.1899, weil 1900 faelschlich als Schaltjahr gilt
EXCEL_NULL = date(1899, 12, 30)

# Eingebaute Zahlenformate, die ein Datum bedeuten
DATUMS_FORMATE = set(range(14, 23)) | set(range(45, 48)) | {27, 30, 36, 50, 57}


def _ohne_namensraum(marke):
    return marke.split("}")[-1]


def _texte(element):
    """Sammelt allen Text unterhalb eines Elements (Excel teilt ihn auf)."""
    stuecke = []
    for knoten in element.iter():
        if _ohne_namensraum(knoten.tag) == "t" and knoten.text:
            stuecke.append(knoten.text)
    return "".join(stuecke)


def _spalte_zu_nummer(bezug):
    """'BC12' -> 55 (die Spaltennummer, eins-basiert)."""
    buchstaben = re.match(r"([A-Z]+)", bezug or "")
    if not buchstaben:
        return None
    nummer = 0
    for zeichen in buchstaben.group(1):
        nummer = nummer * 26 + (ord(zeichen) - 64)
    return nummer


class Mappe:
    """Liest eine xlsx-Datei ohne Fremdbibliothek.

    Eine xlsx ist ein ZIP-Archiv mit XML darin. Alles was hier gebraucht wird,
    steht in vier Dateien: den gemeinsamen Texten, den Formatvorlagen, der
    Arbeitsmappe und je einem Blatt.
    """

    def __init__(self, pfad):
        self.pfad = Path(pfad)
        self.archiv = zipfile.ZipFile(str(self.pfad))
        self.texte = self._lies_texte()
        self.datums_stile = self._lies_stile()

    def _xml(self, name):
        try:
            return ET.fromstring(self.archiv.read(name))
        except KeyError:
            return None

    def _lies_texte(self):
        wurzel = self._xml("xl/sharedStrings.xml")
        if wurzel is None:
            return []
        return [_texte(si) for si in wurzel if _ohne_namensraum(si.tag) == "si"]

    def _lies_stile(self):
        """Welche Formatvorlagen stehen fuer ein Datum?"""
        wurzel = self._xml("xl/styles.xml")
        if wurzel is None:
            return set()

        eigene = {}
        for knoten in wurzel.iter():
            if _ohne_namensraum(knoten.tag) != "numFmt":
                continue
            kennung = knoten.get("numFmtId")
            muster = (knoten.get("formatCode") or "").lower()
            # Ein Format ist ein Datum, wenn Tag/Monat/Jahr darin vorkommen
            ohne_text = re.sub(r"\[[^\]]*\]|\"[^\"]*\"", "", muster)
            if kennung and re.search(r"[dmy]", ohne_text) and "h" not in ohne_text:
                eigene[int(kennung)] = True

        datums_stile = set()
        for block in wurzel.iter():
            if _ohne_namensraum(block.tag) != "cellXfs":
                continue
            for nummer, xf in enumerate(block):
                kennung = int(xf.get("numFmtId") or 0)
                if kennung in DATUMS_FORMATE or kennung in eigene:
                    datums_stile.add(nummer)
        return datums_stile

    def blaetter(self):
        """[(Blattname, Pfad im Archiv)] in der Reihenfolge der Mappe."""
        beziehungen = {}
        wurzel = self._xml("xl/_rels/workbook.xml.rels")
        if wurzel is not None:
            for eintrag in wurzel:
                ziel = eintrag.get("Target") or ""
                if not ziel.startswith("/"):
                    ziel = "xl/" + ziel.lstrip("./")
                beziehungen[eintrag.get("Id")] = ziel.lstrip("/")

        ergebnis = []
        wurzel = self._xml("xl/workbook.xml")
        if wurzel is None:
            return ergebnis
        for knoten in wurzel.iter():
            if _ohne_namensraum(knoten.tag) != "sheet":
                continue
            kennung = None
            for schluessel, wert in knoten.attrib.items():
                if schluessel.endswith("}id"):
                    kennung = wert
            pfad = beziehungen.get(kennung)
            if pfad and pfad in self.archiv.namelist():
                ergebnis.append((knoten.get("name") or "Tabelle", pfad))
        return ergebnis

    def _zelle(self, zelle):
        art = zelle.get("t")
        stil = zelle.get("s")
        wert = None
        for kind in zelle:
            marke = _ohne_namensraum(kind.tag)
            if marke == "v":
                wert = kind.text
            elif marke == "is":
                return _texte(kind)
        if wert is None:
            return ""
        if art == "s":
            index = int(wert)
            return self.texte[index] if index < len(self.texte) else ""
        if art == "b":
            return "ja" if wert == "1" else "nein"
        if art in ("str", "e"):
            return wert

        # Zahl. Steht eine Datumsvorlage darauf, als Datum ausgeben.
        try:
            zahl = float(wert)
        except ValueError:
            return wert
        if stil is not None and int(stil) in self.datums_stile and zahl > 0:
            try:
                return (EXCEL_NULL + timedelta(days=int(zahl))).isoformat()
            except (OverflowError, ValueError):
                pass
        if zahl == int(zahl):
            return str(int(zahl))
        return ("{:.6f}".format(zahl)).rstrip("0").rstrip(".")

    def zeilen(self, blatt_pfad):
        """[(Excel-Zeilennummer, [Zellwerte])].

        Die echte Zeilennummer aus der Datei, nicht durchgezaehlt. Sonst zeigt
        eine spaetere Rueckfrage auf die falsche Zeile in seiner Tabelle.
        """
        wurzel = self._xml(blatt_pfad)
        if wurzel is None:
            return []
        ergebnis = []
        laufend = 0
        for zeile in wurzel.iter():
            if _ohne_namensraum(zeile.tag) != "row":
                continue
            laufend += 1
            try:
                nummer_zeile = int(zeile.get("r"))
            except (TypeError, ValueError):
                nummer_zeile = laufend
            werte = {}
            for zelle in zeile:
                if _ohne_namensraum(zelle.tag) != "c":
                    continue
                nummer = _spalte_zu_nummer(zelle.get("r"))
                if nummer:
                    werte[nummer] = self._zelle(zelle)
            if not werte:
                ergebnis.append((nummer_zeile, []))
                continue
            breite = max(werte)
            ergebnis.append(
                (nummer_zeile, [werte.get(i, "") for i in range(1, breite + 1)])
            )
        return ergebnis


def mappe_als_text(pfad):
    """Gibt eine Excel-Mappe als Text aus, ein Blatt nach dem anderen."""
    mappe = Mappe(pfad)
    zeilen_aus = ["=" * 70, "DATEI: {}".format(Path(pfad).name), "=" * 70]

    blaetter = mappe.blaetter()
    if not blaetter:
        zeilen_aus.append("(keine Tabellenblätter gefunden)")
        return "\n".join(zeilen_aus)

    for name, blatt_pfad in blaetter:
        zeilen = mappe.zeilen(blatt_pfad)
        # leere Zeilen am Ende abschneiden
        while zeilen and not any(z.strip() for z in zeilen[-1][1]):
            zeilen.pop()
        gefuellt = [(n, z) for n, z in zeilen if " ".join(z).strip()]
        zeilen_aus.append("")
        zeilen_aus.append(
            "--- Blatt: {} ({} gefüllte Zeilen) ---".format(name, len(gefuellt))
        )
        if not gefuellt:
            zeilen_aus.append("(leer)")
            continue
        zeilen_aus.append("(die Nummer ist die Zeile in Excel)")
        for nummer, zeile in gefuellt:
            zeilen_aus.append(
                "{:>4}: {}".format(nummer, " | ".join(z.strip() for z in zeile))
            )
    return "\n".join(zeilen_aus)


def sammle_dateien(argumente):
    if argumente:
        return [Path(a) for a in argumente]
    UNTERLAGEN.mkdir(exist_ok=True)
    return sorted(p for p in UNTERLAGEN.rglob("*") if p.is_file())


def main():
    konsole_utf8()
    dateien = sammle_dateien(sys.argv[1:])

    if not dateien:
        print("Der Ordner unterlagen\\ ist leer.")
        print("")
        print("Dort hineinlegen, was schon vorhanden ist: die Excel-Liste der")
        print("Wohnungen, Mietverträge als PDF, eine Mieterliste. Danach dieses")
        print("Skript noch einmal ausführen.")
        return 0

    tabellen = [p for p in dateien if p.suffix.lower() in (".xlsx", ".xlsm")]
    direkt = [p for p in dateien if p.suffix.lower() in
              (".pdf", ".csv", ".txt", ".md", ".docx")]
    alt = [p for p in dateien if p.suffix.lower() in (".xls", ".doc")]
    rest = [p for p in dateien if p not in tabellen + direkt + alt]

    for pfad in tabellen:
        try:
            print(mappe_als_text(pfad))
            print("")
        except Exception as fehler:
            print("! {} konnte nicht gelesen werden: {}".format(pfad.name, fehler))

    if direkt:
        print("=" * 70)
        print("DIESE DATEIEN LIEST CLAUDE DIREKT, sie brauchen kein Skript:")
        for pfad in direkt:
            print("  {}".format(pfad))
        print("")
        print("Hinweis zu PDFs: Eingescannte Verträge ohne Textebene sind reine")
        print("Bilder. Daraus lässt sich nichts übernehmen, diese Angaben müssen")
        print("abgefragt werden.")
        print("")

    if alt:
        print("=" * 70)
        print("ALTES FORMAT, bitte einmal in Excel bzw. Word neu speichern:")
        for pfad in alt:
            print("  {}  ->  als .xlsx bzw. .docx speichern".format(pfad.name))
        print("")

    if rest:
        print("=" * 70)
        print("NICHT VERWERTBAR (Bilder oder unbekanntes Format):")
        for pfad in rest:
            print("  {}".format(pfad.name))
        print("")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
