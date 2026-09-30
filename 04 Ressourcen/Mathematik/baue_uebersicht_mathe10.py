#!/usr/bin/env python3
"""Übersicht Mathematik Klasse 10b: links alle Wochen aus dem Stoffverteilungsplan (baue_stoffverteilung10.py), rechts die gewählte Stunde (iframe).
Aufbau wie baue_uebersicht_mathe7.py. Fertige Stunden/Unterlagen stehen in FERTIG, alle anderen Wochen sind ausgegraut („noch nicht vorbereitet“).
Rhythmus 10b: Mo 1 Std, Mi Doppelstunde, Fr 1 Std (4 Std pro Woche). Woche 6 (19.-23.10.) fällt wegen der Berlinfahrt der 10er aus.
Aufruf: python3 baue_uebersicht_mathe10.py  -> Mathematik Klasse 10b – Übersicht.html"""
import datetime, sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "Physik" / "Optik"))
sys.path.insert(0, str(HIER))
from uebersicht_vorlage import baue_uebersicht  # noqa: E402
from baue_stoffverteilung10 import W  # noqa: E402

RHYTHMUS = "Mo 1 Std, Mi Doppelstunde, Fr 1 Std"
K = "Stochastik/Kurztest Wahrscheinlichkeit 10b/Kurztest Wahrscheinlichkeit 10b "
# fertige Unterlagen: Woche -> [(id, Marke, Titel, Datei relativ zu diesem Ordner, Datum)]
FERTIG = {
    3: [("W3A", "KT A", "Kurztest Nr. 1, Version A", K + "A.html", "Mi 30.09."),
        ("W3AL", "KT A", "Lösung Version A", K + "A – Lösung.html", "nur für dich"),
        ("W3B", "KT B", "Kurztest Nr. 1, Version B", K + "B.html", "Mi 30.09."),
        ("W3BL", "KT B", "Lösung Version B", K + "B – Lösung.html", "nur für dich")],
}
BLOECKE = {1: "Wahrscheinlichkeit", 3: "Prozent- und Zinsrechnung", 8: "Trigonometrie", 11: "Körper",
           16: "Daten und Potenzen", 19: "Geraden und Parabeln", 26: "Prüfungsvorbereitung", 29: "Puffer bis zum Schuljahresende"}


def de(d):
    return f"{d.day:02d}.{d.month:02d}.{d.year}"


def main():
    gruppen, akt, block = [], None, None
    for r in W:
        if isinstance(r, str):
            if r.startswith("Berlinfahrt") and akt:
                akt[1].append({"id": "BER", "marke": "–", "titel": "Berlinfahrt der 10er, kein Unterricht", "sub": "Woche 6 entfällt",
                               "datum": "19.10. bis 23.10.", "datei": "", "art": ""})
            continue
        nr, mo, thema, termin, rot = r
        if nr in BLOECKE:
            block, akt = BLOECKE[nr], None
        sub = f"Klasse 10b, Mathematik, Woche {nr} (ab {de(mo)}), laut Plan: {thema} · {RHYTHMUS}"
        fertig = FERTIG.get(nr, [])
        if fertig:
            akt = (f"Woche {nr}: {block}", [])
            gruppen.append(akt)
            for sid, m, titel, datei, tag in fertig:
                akt[1].append({"id": sid, "marke": m, "titel": titel, "sub": sub, "datum": tag, "datei": datei, "art": ""})
            akt = None
        else:
            if akt is None:
                akt = (block, [])
                gruppen.append(akt)
            akt[1].append({"id": f"W{nr}", "marke": f"Wo {nr}", "titel": thema or "letzte Schulwoche", "sub": sub,
                           "datum": f"ab {de(mo)}" + (f" · {termin}" if termin and "KA" not in termin else ""), "datei": "", "art": "offen"})
        if "KA" in termin and nr != 18:
            n = {7: 1, 13: 2, 25: 4}[nr]
            gruppen[-1][1].append({"id": f"KA{n}", "marke": "KA", "titel": f"Klassenarbeit {n}, {termin.replace('KA ', '')}", "sub": sub,
                                   "datum": f"Woche {nr}", "datei": "", "art": "ka"})
        if nr == 18:
            gruppen[-1][1].append({"id": "KA3", "marke": "KA", "titel": "Klassenarbeit 3, Do 4.2.", "sub": sub, "datum": f"Woche {nr}", "datei": "", "art": "ka"})
        if nr == 28:
            gruppen[-1][1].append({"id": "PR", "marke": "Prüf.", "titel": "Abschlussprüfung Mathematik, Do 29.04.2027", "sub": sub,
                                   "datum": f"Woche {nr}", "datei": "", "art": "ka"})
    links = [("Stoffverteilungsplan Mathe 10 (PDF)", "Stoffverteilungsplan 26-27 Mathe 10.pdf"),
             ("Unterrichtsvorbereitung (alle Fächer)", "../Unterrichtsvorbereitung.html")]
    baue_uebersicht(HIER / "Mathematik Klasse 10b – Übersicht.html", "Mathematik Klasse 10b",
                    f"Alle Wochen nach Stoffverteilungsplan · 2026/27 · {RHYTHMUS}", gruppen, links, "mathe10-woche")
    print("geschrieben: Mathematik Klasse 10b – Übersicht.html")


if __name__ == "__main__":
    main()
