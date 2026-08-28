# -*- coding: utf-8 -*-
"""Listet offene Mieten mit Verzugsdauer und vorgeschlagener Mahnstufe.

Aufruf:
    py -3 skripte\\rueckstaende.py           (letzte 12 Monate)
    py -3 skripte\\rueckstaende.py 24        (letzte 24 Monate)

Ausgewertet wird nur der Zeitraum, fuer den Kontoumsaetze vorliegen. Monate
ohne Bankdaten gelten nicht als unbezahlt, sondern als unbekannt.
"""

import sys
from datetime import date

from gemeinsam import (
    bezeichnung_fuer,
    einheiten_index,
    eur,
    konsole_utf8,
    lade,
    monat_key,
    monat_lesbar,
    monat_verschieben,
)
from zuordnung import zahlungsstand


def faelligkeit(monat, faellig_am):
    jahr, nummer = (int(t) for t in monat.split("-"))
    return date(jahr, nummer, min(faellig_am, 28))


def stufe_fuer(tage, mahnstufen):
    passend = None
    for stufe in sorted(mahnstufen, key=lambda s: s["nach_tagen"]):
        if tage >= stufe["nach_tagen"]:
            passend = stufe
    return passend


def sammle(monate_zurueck=12):
    konfig = lade("konfig", {})
    objekte = lade("objekte", [])
    mietverhaeltnisse = lade("mietverhaeltnisse", [])
    zahlungen = lade("zahlungen", [])

    datierte = [b.get("datum") for b in zahlungen if b.get("datum")]
    if not datierte:
        return [], None
    datenbeginn = min(datierte)[:7]

    heute = date.today()
    faellig_am = int(konfig.get("miete_faellig_am", 3))
    mahnstufen = konfig.get("mahnstufen", [])
    index = einheiten_index(objekte)

    offene = []
    for versatz in range(monate_zurueck, -1, -1):
        monat = monat_verschieben(monat_key(heute), -versatz)
        if monat < datenbeginn:
            continue
        for eintrag in zahlungsstand(zahlungen, mietverhaeltnisse, monat):
            if eintrag["status"] == "bezahlt":
                continue
            tage = (heute - faelligkeit(monat, faellig_am)).days
            if tage < 0:
                continue
            offene.append(
                {
                    "monat": monat,
                    "mv": eintrag["mv"],
                    "ort": bezeichnung_fuer(eintrag["mv"], index),
                    "soll": eintrag["soll"],
                    "ist": eintrag["ist"],
                    "offen": abs(eintrag["differenz"]),
                    "tage": tage,
                    "stufe": stufe_fuer(tage, mahnstufen),
                }
            )
    return offene, datenbeginn


def main():
    konsole_utf8()
    monate = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    offene, datenbeginn = sammle(monate)

    if datenbeginn is None:
        print("Es sind noch keine Kontoumsätze eingelesen.")
        print("Ohne Bankdaten lässt sich kein Rückstand feststellen.")
        return 0

    if not offene:
        print("Keine offenen Mieten seit {}.".format(monat_lesbar(datenbeginn)))
        return 0

    nach_mieter = {}
    for eintrag in offene:
        nach_mieter.setdefault(eintrag["mv"]["id"], []).append(eintrag)

    print("Offene Mieten (Daten ab {})".format(monat_lesbar(datenbeginn)))
    print("")
    gesamt = 0.0
    for eintraege in sorted(nach_mieter.values(), key=lambda e: -max(x["tage"] for x in e)):
        mv = eintraege[0]["mv"]
        summe = sum(e["offen"] for e in eintraege)
        gesamt += summe
        aeltester = max(eintraege, key=lambda e: e["tage"])
        stufe = aeltester["stufe"]
        print("{} – {}".format(mv["mieter_name"], eintraege[0]["ort"]))
        for eintrag in sorted(eintraege, key=lambda e: e["monat"]):
            teil = ""
            if eintrag["ist"] > 0:
                teil = " (von {} sind {} eingegangen)".format(
                    eur(eintrag["soll"]), eur(eintrag["ist"])
                )
            print(
                "   {}: {} offen, {} Tage überfällig{}".format(
                    monat_lesbar(eintrag["monat"]), eur(eintrag["offen"]),
                    eintrag["tage"], teil
                )
            )
        print("   Summe: {}".format(eur(summe)))
        if stufe:
            print(
                "   Vorschlag: {} (richtet sich nach dem ältesten offenen "
                "Posten: {}, {} Tage)".format(
                    stufe["ton"], monat_lesbar(aeltester["monat"]), aeltester["tage"]
                )
            )
        else:
            print("   Vorschlag: noch abwarten, Frist ist frisch")
        if mv.get("mieter_email"):
            print("   E-Mail: {}".format(mv["mieter_email"]))
        print("")

    print("Insgesamt offen: {}".format(eur(gesamt)))
    print("")
    print("Bevor etwas verschickt wird: mit dem Vermieter durchgehen, ob zu")
    print("einem Fall etwas bekannt ist, das nicht in den Daten steht.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
