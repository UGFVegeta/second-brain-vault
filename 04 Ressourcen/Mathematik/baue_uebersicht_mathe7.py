#!/usr/bin/env python3
"""Übersicht Mathematik Klasse 7c: links alle Wochen aus dem Stoffverteilungsplan, rechts die gewählte Stunde (iframe).
Wochen und Themen kommen aus dem Stoffverteilungsplan in der iCloud. Aus der Termine-Spalte wird „KA n“ übernommen und statt des Namens
nur ein Kürzel (erste zwei Buchstaben), damit man sieht, wer die Arbeit vorbereitet. Volle Namen kommen nicht in den Vault. Fertige Stunden stehen in STUNDEN, alle anderen Wochen sind ausgegraut.
Aufruf: python3 baue_uebersicht_mathe7.py  -> Mathematik Klasse 7 – Übersicht.html"""
import datetime, html, re, sys
from pathlib import Path

import openpyxl

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER.parent / "Physik" / "Optik"))
from uebersicht_vorlage import baue_uebersicht  # noqa: E402

EIGENER_NAME = "Klein"
PLAN = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Schuljahr 26 27/Mathematik/Mathematik 7c/01 Organisatorisches/Stoffverteilungsplan 26-27 Mathe 7.xlsx"

# fertige Wochen (Wochenformat, mathe_woche_vorlage.py): Woche -> [(id, Marke, Titel, Datei relativ zu diesem Ordner)]
W3 = "Rationale Zahlen/Mathe 7c – Woche 3 – "
STUNDEN = {  # Woche -> [(id, Marke, Titel, Datei, Tag)]; fertige Wochen bekommen links eine eigene Überschrift, darunter die Stunden
    1: [("W1", "Wo 1", "Grundlagen-Check und Brüche sind Zahlen", "Brüche/Mathe 7c – Woche 1.html", "ganze Woche")],
    2: [("W2", "Wo 2", "Zahlen unter Null, Addieren", "Rationale Zahlen/Mathe 7c – Woche 2.html", "ganze Woche")],
    3: [("W3S1", "1", "Minus üben", W3 + "1 Minus üben.html", "Mo 28.09., IF-Stunde"),
        ("W3S2", "2", "Rechengesetze, Minusklammer setzen", W3 + "2 Rechengesetze, Minusklammer setzen.html", "Di 29.09., Doppelstunde"),
        ("W3S3", "3", "Minusklammer auflösen", W3 + "3 Minusklammer auflösen.html", "Mi 30.09."),
        ("W3S4", "4", "Minusklammer üben, Exit-Ticket", W3 + "4 Minusklammer üben, Exit-Ticket.html", "Do 01.10.")],
}

# Themenblöcke: erste Woche -> Name (die Blöcke im Plan beginnen mit dem Thema vor mehreren Leerzeichen)
BLOECKE = {1: "Wiederholung Brüche", 2: "Rationale Zahlen", 9: "Dreiecke", 14: "Rechnen mit Termen", 20: "Gleichungen",
           25: "Proportional und antiproportional", 31: "Prozente", 35: "Vierecke"}


def datum(x, woche):
    if isinstance(x, datetime.datetime):
        tag, monat = x.day, x.month
    else:
        tag, monat = (int(t) for t in str(x).strip(" .").split(".")[:2])
    jahr = 2026 if monat >= 8 else 2027
    return f"{tag:02d}.{monat:02d}.{jahr}"


def plan():
    ws = openpyxl.load_workbook(PLAN, data_only=True).active
    wochen = []
    for r in ws.iter_rows(min_row=3, values_only=True):
        wo, von, thema, termin = r[0], r[1], r[4], r[5]
        if not isinstance(wo, (int, float)) and not str(wo or "").strip().isdigit():
            if str(wo or "").strip():
                wochen.append({"ferien": str(wo).strip()})
            continue
        wo = int(wo)
        thema = re.sub(r"\s{2,}", " · ", str(thema or "").strip())
        # Blockname vorn weglassen, er steht schon als Gruppe
        for name in ("Rationale Zahlen · ", "Dreiecke · ", "Rechnen mit Termen · ", "Gleichungen · ", "Proportional und antiproportional · ",
                     "Prozente · ", "Vierecke · "):
            thema = thema.replace(name, "")
        ka = re.search(r"KA ?(\d)\s*([A-ZÄÖÜ][a-zäöüß]+)?", str(termin or ""))
        wer = ka.group(2) if ka and ka.group(2) else ""
        kuerzel = "du" if wer == EIGENER_NAME else wer[:2]
        wochen.append({"wo": wo, "ab": datum(von, wo), "bis": datum(r[2], wo) if r[2] else "", "thema": thema, "ka": ka.group(1) if ka else "", "wer": kuerzel,
                       "alternativ": "Alternativ" in str(termin or "")})
    return wochen


def schulplan(wochen, ziel):
    """Der Stoffverteilungsplan der Schule als Tabelle, daneben, was in der 7c dazu fertig ist. Namen nur als Kürzel."""
    heute = datetime.date.today()
    zeilen = ""
    for w in wochen:
        if "ferien" in w:
            zeilen += f'<tr class="ferien"><td colspan="5">{html.escape(w["ferien"])}</td></tr>'
            continue
        a = datetime.datetime.strptime(w["ab"], "%d.%m.%Y").date()
        jetzt = a <= heute < a + datetime.timedelta(days=7)
        ka = ""
        if w["ka"]:
            ka = f'KA {w["ka"]}' + (f' · {"du" if w["wer"] == "du" else w["wer"]}' if w["wer"] else "") + (" (alternativ)" if w["alternativ"] else "")
        bei_mir = " ".join(f'<a href="{html.escape(d)}" target="_top" title="{html.escape(t)}">{html.escape(m if m.startswith("Wo") else "St. " + m)}</a>'
                          for _, m, t, d, *_ in STUNDEN.get(w["wo"], [])) or "–"
        zeilen += (f'<tr{" class=\"jetzt\"" if jetzt else ""}><td class="wo">{w["wo"]}</td><td class="dat">{w["ab"][:6]} – {w["bis"][:6]}</td>'
                   f'<td>{html.escape(w["thema"])}</td><td class="ka">{html.escape(ka)}</td><td class="mir">{bei_mir}</td></tr>')
    seite = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stoffverteilungsplan Mathe 7</title><style>
body{{margin:0;background:#F4F6F9;color:#14171c;font:15px/1.45 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
main{{max-width:980px;margin:0 auto;padding:24px 20px 40px}}h1{{font-size:21px;margin:0 0 4px}}.sub{{color:#66798E;margin:0 0 16px;font-size:14px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #D9DFE7}}
th{{font-size:12px;text-align:left;color:#66798E;padding:8px 10px;border-bottom:1px solid #D9DFE7;background:#FAFBFC}}
td{{padding:7px 10px;border-bottom:1px solid #EEF1F5;vertical-align:top}}td.wo{{font:600 13px ui-monospace,Menlo,monospace;color:#2F5E9E;width:36px}}
td.dat{{white-space:nowrap;color:#66798E;font-size:13px;width:120px}}td.ka{{color:#E6007E;font-weight:600;white-space:nowrap;width:130px}}
td.mir{{width:110px}}td.mir a{{font:600 12px ui-monospace,Menlo,monospace;color:#2F5E9E;text-decoration:none;margin-right:6px}}
tr.ferien td{{background:#F4F6F9;color:#66798E;font-size:13px;font-style:italic}}tr.jetzt td{{background:#FFF6D6}}tr.jetzt td.wo::after{{content:" ◀";color:#B98500}}
</style></head><body><main><h1>Stoffverteilungsplan Mathematik Klasse 7 · Schule</h1>
<p class="sub">So wie ihn die Fachschaft geplant hat. Gelb ist die aktuelle Woche. Rechts steht, welche Stunden der 7c dazu schon fertig sind. Klassenarbeiten mit dem Kürzel der Lehrkraft, die sie erstellt.</p>
<table><tr><th>Wo</th><th>Zeitraum</th><th>Thema laut Plan</th><th>Termine</th><th>7c fertig</th></tr>{zeilen}</table></main></body></html>"""
    Path(ziel).write_text(seite, encoding="utf-8")


def main():
    gruppen, akt = [("Planung", [{"id": "SVP", "marke": "SVP", "titel": "Stoffverteilungsplan der Schule", "sub": "Original der Fachschaft, daneben der Stand der 7c",
                                  "datum": "zum Vergleich mit deinem Stand", "datei": "Mathematik Klasse 7 – Stoffverteilungsplan Schule.html", "art": ""}])], None
    wochen = plan()
    schulplan(wochen, HIER / "Mathematik Klasse 7 – Stoffverteilungsplan Schule.html")
    block = None
    for w in wochen:
        if "ferien" in w:
            continue
        if w["wo"] in BLOECKE:
            block = BLOECKE[w["wo"]]
            akt = None
        sub = f"Klasse 7c, Mathematik, Woche {w['wo']} (ab {w['ab']}), laut Plan: {w['thema']}"
        fertig = STUNDEN.get(w["wo"], [])
        if fertig:
            akt = (f"Woche {w['wo']}: {block}", [])
            gruppen.append(akt)
            for sid, m, titel, datei, tag in fertig:
                akt[1].append({"id": sid, "marke": m, "titel": titel, "sub": sub, "datum": tag, "datei": datei, "art": ""})
            akt = None          # danach geht es unter dem Thema weiter
        else:
            if akt is None:
                akt = (block, [])
                gruppen.append(akt)
            akt[1].append({"id": f"W{w['wo']}", "marke": f"Wo {w['wo']}", "titel": w["thema"], "sub": sub, "datum": f"ab {w['ab']}", "datei": "", "art": "offen"})
        if w["ka"] and not w["alternativ"]:
            wer = " · erstellt von dir, an die Parallelklassen geben" if w["wer"] == "du" else (f" · erstellt von {w['wer']}, für die 7c anpassen" if w["wer"] else "")
            ziel = gruppen[-1]
            ziel[1].append({"id": f"KA{w['ka']}", "marke": "KA", "titel": f"Klassenarbeit {w['ka']}{wer}".replace(" · ", ", "), "sub": sub,
                            "datum": f"Woche {w['wo']}, ab {w['ab']}", "datei": "", "art": "ka"})
    links = [("Grundlagen-Check: Verlauf übers Jahr", "Arbeitsblätter/Grundlagen-Check/7c 2026-27/Verlauf.html"),
             ("Unterrichtsvorbereitung (alle Fächer)", "../Unterrichtsvorbereitung.html")]
    baue_uebersicht(HIER / "Mathematik Klasse 7 – Übersicht.html", "Mathematik Klasse 7c", "Alle Wochen nach Stoffverteilungsplan · 2026/27",
                    gruppen, links, "mathe7-woche")


if __name__ == "__main__":
    main()
