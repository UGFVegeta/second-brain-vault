# -*- coding: utf-8 -*-
"""Prueft die erfassten Daten auf Fehler, bevor damit gerechnet wird.

Aufruf:
    py -3 skripte\\pruefen.py

Findet doppelte IDs, verwaiste Verweise, fehlende Pflichtangaben und
unplausible Betraege. Aendert nichts, meldet nur.
"""

from datetime import date

from gemeinsam import (
    einheiten_index,
    eur,
    ist_aktiv,
    konsole_utf8,
    lade,
    parse_datum,
    sollmiete,
)

fehler = []
warnungen = []


def melde(schwer, text):
    (fehler if schwer else warnungen).append(text)


def pruefe_objekte(objekte):
    gesehen = set()
    for objekt in objekte:
        if not objekt.get("id"):
            melde(True, "Ein Objekt hat keine id: {}".format(objekt.get("bezeichnung")))
            continue
        if objekt["id"] in gesehen:
            melde(True, "Objekt-id kommt doppelt vor: {}".format(objekt["id"]))
        gesehen.add(objekt["id"])
        if not objekt.get("bezeichnung"):
            melde(True, "Objekt {} hat keine Bezeichnung".format(objekt["id"]))
        if not objekt.get("einheiten"):
            melde(False, "Objekt {} hat keine Einheiten".format(objekt["id"]))
        einheiten_gesehen = set()
        for einheit in objekt.get("einheiten", []):
            if not einheit.get("id"):
                melde(True, "Einheit ohne id in {}".format(objekt["id"]))
                continue
            if einheit["id"] in einheiten_gesehen:
                melde(True, "Einheit-id doppelt: {}".format(einheit["id"]))
            einheiten_gesehen.add(einheit["id"])


def pruefe_mietverhaeltnisse(mietverhaeltnisse, objekte):
    index = einheiten_index(objekte)
    gesehen = set()
    belegt = {}
    for mv in mietverhaeltnisse:
        kennung = mv.get("id") or mv.get("mieter_name") or "?"
        if not mv.get("id"):
            melde(True, "Mietverhältnis ohne id: {}".format(kennung))
        elif mv["id"] in gesehen:
            melde(True, "Mietverhältnis-id doppelt: {}".format(mv["id"]))
        gesehen.add(mv.get("id"))

        if not mv.get("mieter_name"):
            melde(True, "Mietverhältnis {} hat keinen Mieternamen".format(kennung))

        if mv.get("einheit_id") not in index:
            melde(
                True,
                "Mietverhältnis {} verweist auf die unbekannte Einheit {}".format(
                    kennung, mv.get("einheit_id")
                ),
            )
        elif ist_aktiv(mv):
            vorher = belegt.get(mv["einheit_id"])
            if vorher:
                melde(
                    True,
                    "Einheit {} ist gleichzeitig an {} und {} vermietet".format(
                        mv["einheit_id"], vorher, mv.get("mieter_name")
                    ),
                )
            belegt[mv["einheit_id"]] = mv.get("mieter_name")

        if not mv.get("kaltmiete"):
            melde(True, "Mietverhältnis {} hat keine Kaltmiete".format(kennung))
        if mv.get("nebenkosten_voraus") is None:
            melde(
                False,
                "Mietverhältnis {}: Nebenkostenvorauszahlung fehlt noch".format(kennung),
            )
        summe = sollmiete(mv)
        if summe and (summe < 100 or summe > 6000):
            melde(
                False,
                "Mietverhältnis {}: Sollmiete {} sieht ungewöhnlich aus".format(
                    kennung, eur(summe)
                ),
            )
        if not mv.get("iban_mieter"):
            melde(
                False,
                "Mietverhältnis {}: keine IBAN hinterlegt, die Zuordnung wird "
                "unschärfer".format(kennung),
            )
        beginn = parse_datum(mv.get("beginn"))
        ende = parse_datum(mv.get("ende"))
        if mv.get("beginn") and not beginn:
            melde(True, "Mietverhältnis {}: Beginn ist kein gültiges Datum".format(kennung))
        if beginn and ende and ende < beginn:
            melde(True, "Mietverhältnis {}: Ende liegt vor dem Beginn".format(kennung))


def pruefe_darlehen(darlehen, objekte):
    ids = {o.get("id") for o in objekte}
    for d in darlehen:
        if d.get("objekt_id") and d["objekt_id"] not in ids:
            melde(True, "Darlehen {} verweist auf unbekanntes Objekt {}".format(
                d.get("id"), d["objekt_id"]))
        if not d.get("restschuld"):
            melde(False, "Darlehen {}: keine Restschuld erfasst".format(d.get("id")))


def pruefe_fristen(fristen, objekte):
    ids = {o.get("id") for o in objekte}
    for frist in fristen:
        if frist.get("objekt_id") and frist["objekt_id"] not in ids:
            melde(True, "Frist {} verweist auf unbekanntes Objekt {}".format(
                frist.get("titel"), frist["objekt_id"]))
        if not parse_datum(frist.get("faellig")):
            melde(True, "Frist {} hat kein gültiges Datum".format(frist.get("titel")))


def main():
    konsole_utf8()
    objekte = lade("objekte", [])
    mietverhaeltnisse = lade("mietverhaeltnisse", [])
    darlehen = lade("darlehen", [])
    fristen = lade("fristen", [])

    if not objekte:
        print("Es sind noch keine Objekte erfasst.")
        print("Sag Claude: „Lass uns meine Objekte erfassen“.")
        return 0

    pruefe_objekte(objekte)
    pruefe_mietverhaeltnisse(mietverhaeltnisse, objekte)
    pruefe_darlehen(darlehen, objekte)
    pruefe_fristen(fristen, objekte)

    einheiten = sum(len(o.get("einheiten", [])) for o in objekte)
    aktive = [mv for mv in mietverhaeltnisse if ist_aktiv(mv)]
    leer = einheiten - len(aktive)

    print("Bestand")
    print("  {} Objekte, {} Einheiten".format(len(objekte), einheiten))
    print("  {} aktive Mietverhältnisse, {} Einheiten ohne Mieter".format(
        len(aktive), leer))
    print("  Sollmiete im Monat: {}".format(eur(sum(sollmiete(mv) for mv in aktive))))
    print("")

    if fehler:
        print("Fehler, die behoben werden müssen:")
        for text in fehler:
            print("  - {}".format(text))
        print("")
    if warnungen:
        print("Hinweise:")
        for text in warnungen:
            print("  - {}".format(text))
        print("")
    if not fehler and not warnungen:
        print("Keine Auffälligkeiten.")
    elif not fehler:
        print("Keine Fehler. Die Hinweise kann man später nachtragen.")

    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
