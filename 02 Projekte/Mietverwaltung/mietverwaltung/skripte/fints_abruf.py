# -*- coding: utf-8 -*-
"""Holt Kontoumsaetze direkt bei der Bank ab (FinTS/HBCI).

Aufruf:
    py -3 skripte\\fints_abruf.py            (letzte 60 Tage)
    py -3 skripte\\fints_abruf.py 180        (letzte 180 Tage)

Vor dem ersten Lauf:
    py -3 -m pip install fints
    Zugangsdaten einrichten: siehe doku\\Bankanbindung.md

WICHTIG ZU DEN ZUGANGSDATEN
    PIN und TAN werden bei jedem Lauf im Terminal abgefragt und nirgends
    gespeichert. Sie stehen in keiner Datei und gehen auch nicht durch Claude.
    Wer das anders haben will, macht die Sache unsicher, nicht bequemer.

    Bankleitzahl, Benutzerkennung und Serveradresse stehen in
    %USERPROFILE%\\.mietverwaltung\\fints.json, also ausserhalb des
    Projektordners. Sie landen damit nicht in einer Sicherung des Projekts.

EHRLICHER HINWEIS
    FinTS verlangt eine bei der Deutschen Kreditwirtschaft registrierte
    Produkt-ID. Manche Banken akzeptieren beliebige Kennungen, andere weisen
    unregistrierte Zugriffe ab. Ob es mit der eigenen Bank klappt, zeigt erst
    der erste Verbindungsversuch. Wenn nicht: der CSV-Weg funktioniert immer.
"""

import getpass
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from gemeinsam import konsole_utf8, lade, normiere_iban, speichere
from umsaetze_importieren import fingerabdruck
from zuordnung import ordne_zu

ZUGANG = Path.home() / ".mietverwaltung" / "fints.json"

VORLAGE = {
    "blz": "60050101",
    "benutzerkennung": "Benutzerkennung aus dem Online-Banking",
    "endpunkt": "https://banking-bw3.s-fints-pt-bw.de/fints30",
    "produkt_id": "",
    "produkt_version": "1.0",
    "konto_iban": "DE00...",
}


def zugang_laden():
    if not ZUGANG.exists():
        ZUGANG.parent.mkdir(parents=True, exist_ok=True)
        ZUGANG.write_text(
            json.dumps(VORLAGE, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("Es gab noch keine Zugangsdaten. Ich habe eine Vorlage angelegt:")
        print("  {}".format(ZUGANG))
        print("")
        print("Bitte dort eintragen:")
        print("  blz             Bankleitzahl der Bank")
        print("  benutzerkennung Anmeldename aus dem Online-Banking")
        print("  endpunkt        FinTS-Adresse der Bank, siehe doku/Bankanbindung.md")
        print("  produkt_id      falls die Bank eine verlangt")
        print("  konto_iban      das Konto, auf dem die Mieten eingehen")
        print("")
        print("Die PIN kommt NICHT in diese Datei, die wird jedes Mal abgefragt.")
        return None
    return json.loads(ZUGANG.read_text(encoding="utf-8"))


def hole_umsaetze(zugang, tage):
    try:
        from fints.client import FinTS3PinTanClient
        from fints.utils import minimal_interactive_cli_bootstrap
    except ImportError:
        print("Die Bibliothek fints fehlt. Einmalig installieren mit:")
        print("  py -3 -m pip install fints")
        return None

    pin = getpass.getpass("PIN für das Online-Banking (wird nicht gespeichert): ")
    if not pin:
        print("Keine PIN eingegeben, Abbruch.")
        return None

    client = FinTS3PinTanClient(
        zugang["blz"],
        zugang["benutzerkennung"],
        pin,
        zugang["endpunkt"],
        product_id=zugang.get("produkt_id") or None,
        product_version=zugang.get("produkt_version", "1.0"),
    )

    # Fragt bei Bedarf TAN-Verfahren und TAN-Medium ab
    minimal_interactive_cli_bootstrap(client)

    buchungen = []
    with client:
        if client.init_tan_response:
            print("")
            print("Die Bank verlangt eine TAN: {}".format(
                client.init_tan_response.challenge))
            tan = input("TAN eingeben: ").strip()
            client.send_tan(client.init_tan_response, tan)

        konten = client.get_sepa_accounts()
        gesucht = normiere_iban(zugang.get("konto_iban"))
        passend = [k for k in konten if normiere_iban(k.iban) == gesucht] or konten
        if not passend:
            print("Die Bank meldet kein Konto zurück.")
            return None
        konto = passend[0]

        bis = date.today()
        von = bis - timedelta(days=tage)
        umsaetze = client.get_transactions(konto, von, bis)

        for umsatz in umsaetze:
            daten = umsatz.data
            betrag = daten.get("amount")
            datum = daten.get("date") or daten.get("entry_date")
            if betrag is None or datum is None:
                continue
            zweck = " ".join(
                str(daten.get(feld) or "").strip()
                for feld in ("purpose", "posting_text")
                if daten.get(feld)
            )
            buchungen.append(
                {
                    "datum": datum.isoformat(),
                    "betrag": round(float(betrag.amount), 2),
                    "zweck": zweck.strip(),
                    "name": (daten.get("applicant_name") or "").strip(),
                    "iban": normiere_iban(daten.get("applicant_iban")),
                    "quelle": "FinTS {:%d.%m.%Y}".format(date.today()),
                }
            )
    return buchungen


def main():
    konsole_utf8()
    tage = int(sys.argv[1]) if len(sys.argv) > 1 else 60

    zugang = zugang_laden()
    if zugang is None:
        return 1
    if zugang.get("benutzerkennung", "").startswith("Benutzerkennung aus"):
        print("In {} stehen noch die Platzhalter.".format(ZUGANG))
        print("Bitte erst die echten Werte eintragen.")
        return 1

    try:
        neue = hole_umsaetze(zugang, tage)
    except Exception as fehler:
        print("Der Abruf hat nicht geklappt: {}".format(fehler))
        print("")
        print("Das ist kein Grund zur Sorge, der CSV-Weg funktioniert immer:")
        print("  Umsätze im Online-Banking als CSV exportieren,")
        print("  in den Ordner kontoauszuege\\ legen,")
        print("  py -3 skripte\\umsaetze_importieren.py")
        return 1
    if neue is None:
        return 1

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

    ordne_zu(bestand, lade("mietverhaeltnisse", []), lade("objekte", []), lade("konfig", {}))
    bestand.sort(key=lambda b: (b.get("datum") or "", b.get("id") or ""))
    speichere("zahlungen", bestand)

    print("")
    print("{} Umsätze abgerufen, davon {} neu.".format(len(neue), hinzugefuegt))
    print("Jetzt das Dashboard neu bauen:")
    print("  py -3 skripte\\dashboard_bauen.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
