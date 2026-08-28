# -*- coding: utf-8 -*-
"""Baut aus den Daten in daten\\ die Datei Dashboard.html.

Aufruf:
    py -3 skripte\\dashboard_bauen.py

Das Dashboard ist eine einzelne HTML-Datei ohne Internetzugriff. Sie enthaelt
die echten Daten und kann per Doppelklick geoeffnet werden. Es gibt darin
bewusst keine Knoepfe, die etwas versenden: Alles was nach draussen geht,
laeuft ueber Claude und wird vorher gelesen und freigegeben.
"""

import html
import json
from datetime import date, datetime

from gemeinsam import (
    AUSGABE,
    bezeichnung_fuer,
    einheiten_index,
    eur,
    eur_kurz,
    initialen,
    ist_aktiv,
    konsole_utf8,
    lade,
    monat_key,
    monat_lesbar,
    monat_verschieben,
    parse_datum,
    sollmiete,
)
from zuordnung import zahlungsstand

STIL = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
         background: #f4f3ee; color: #1a1a18; line-height: 1.6; }
  .wrap { max-width: 860px; margin: 0 auto; padding: 32px 20px 64px; }
  h1 { font-size: 26px; font-weight: 600; margin-bottom: 4px; }
  h3 { font-size: 15px; font-weight: 600; margin-bottom: 12px; }
  p.lead { color: #5f5e5a; margin-bottom: 24px; font-size: 14px; }
  .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 20px; }
  .metric { background: #fff; border: 1px solid #e5e3da; border-radius: 10px; padding: 14px 16px; }
  .metric .label { font-size: 12px; color: #888780; margin-bottom: 2px; }
  .metric .value { font-size: 23px; font-weight: 600; }
  .value.green { color: #0f6e56; } .value.red { color: #a32d2d; } .value.amber { color: #854f0b; }
  .card { background: #fff; border: 1px solid #e5e3da; border-radius: 12px; padding: 18px 20px; margin-bottom: 20px; }
  .cardnote { font-size: 13px; color: #5f5e5a; margin-bottom: 12px; }
  .row { display: flex; align-items: center; gap: 12px; padding: 11px 0; border-top: 1px solid #efeee8; flex-wrap: wrap; }
  .row:first-of-type { border-top: none; }
  .avatar { width: 36px; height: 36px; border-radius: 50%; background: #e6f1fb; color: #185fa5;
            display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; flex-shrink: 0; }
  .row .info { flex: 1; min-width: 170px; }
  .row .obj { font-size: 14px; font-weight: 600; }
  .row .meta { font-size: 12px; color: #888780; }
  .row .amount { font-size: 14px; font-weight: 600; min-width: 92px; text-align: right; }
  .badge { font-size: 12px; padding: 3px 10px; border-radius: 20px; white-space: nowrap; font-weight: 500; }
  .badge.paid { background: #e1f5ee; color: #085041; }
  .badge.open { background: #faeeda; color: #854f0b; }
  .badge.late { background: #fcebeb; color: #a32d2d; }
  .badge.blue { background: #e6f1fb; color: #185fa5; }
  .badge.neutral { background: #f1efe8; color: #5f5e5a; }
  .bars { display: flex; align-items: flex-end; gap: 8px; height: 96px; margin: 22px 0 4px; }
  .bars .bar { flex: 1; background: #85b7eb; border-radius: 4px 4px 0 0; position: relative; min-height: 3px; }
  .bars .bar.last { background: #185fa5; }
  .bars .bar span { position: absolute; top: -16px; left: 0; right: 0; text-align: center; font-size: 10px; color: #5f5e5a; }
  .barlabels { display: flex; gap: 8px; }
  .barlabels span { flex: 1; text-align: center; font-size: 11px; color: #888780; }
  .empty { font-size: 13px; color: #888780; padding: 10px 0; }
  .callout { background: #faeeda; color: #633806; font-size: 14px; padding: 12px 16px; border-radius: 8px; margin: 16px 0; }
  .callout.info { background: #eeedfe; color: #3c3489; }
  button { font-family: inherit; font-size: 12px; padding: 6px 12px; border: 1px solid #d3d1c7;
           border-radius: 6px; background: #fff; cursor: pointer; color: #1a1a18; }
  button:hover { background: #f4f3ee; }
  .search { width: 100%; padding: 9px 12px; border: 1px solid #d3d1c7; border-radius: 8px;
            font-size: 13px; font-family: inherit; margin-bottom: 10px; }
  .search:focus { outline: none; border-color: #185fa5; }
  footer { margin-top: 48px; font-size: 12px; color: #888780; border-top: 1px solid #e5e3da; padding-top: 16px; }
  table.liste { width: 100%; border-collapse: collapse; font-size: 13px; }
  table.liste th { text-align: left; font-weight: 600; color: #5f5e5a; padding: 6px 8px 6px 0; border-bottom: 1px solid #d3d1c7; }
  table.liste td { padding: 6px 8px 6px 0; border-bottom: 1px solid #efeee8; vertical-align: top; }
  table.liste td.num, table.liste th.num { text-align: right; white-space: nowrap; padding-right: 0; }
"""


def e(wert):
    return html.escape(str(wert if wert is not None else ""))


def karte(titel, inhalt, notiz=None):
    teile = ['<div class="card">', "<h3>{}</h3>".format(e(titel))]
    if notiz:
        teile.append('<p class="cardnote">{}</p>'.format(e(notiz)))
    teile.append(inhalt)
    teile.append("</div>")
    return "\n".join(teile)


# ----------------------------------------------------------------- Bausteine

def block_zahlungsstatus(stand, index, monat):
    if not stand:
        return karte(
            "Zahlungsstatus",
            '<div class="empty">Noch keine aktiven Mietverhältnisse erfasst.</div>',
        )
    reihen = []
    for eintrag in sorted(stand, key=lambda s: (s["status"] != "offen", s["mv"]["mieter_name"])):
        mv = eintrag["mv"]
        klasse = {"bezahlt": "paid", "offen": "open", "teilzahlung": "late"}[eintrag["status"]]
        text = {"bezahlt": "bezahlt", "offen": "offen", "teilzahlung": "Teilzahlung"}[eintrag["status"]]
        if eintrag["status"] == "bezahlt" and eintrag["buchungen"]:
            datum = parse_datum(eintrag["buchungen"][0]["datum"])
            text = "bezahlt {:%d.%m.}".format(datum)
        if eintrag["status"] == "teilzahlung":
            text = "fehlen {}".format(eur(abs(eintrag["differenz"])))
        reihen.append(
            '<div class="row">'
            '<div class="avatar">{ini}</div>'
            '<div class="info"><div class="obj">{ort}</div>'
            '<div class="meta">{mieter}</div></div>'
            '<div class="amount">{soll}</div>'
            '<span class="badge {klasse}">{text}</span>'
            "</div>".format(
                ini=e(initialen(mv["mieter_name"])),
                ort=e(bezeichnung_fuer(mv, index)),
                mieter=e(mv["mieter_name"]),
                soll=e(eur(eintrag["soll"])),
                klasse=klasse,
                text=e(text),
            )
        )
    return karte("Zahlungsstatus {}".format(monat_lesbar(monat)), "\n".join(reihen))


def block_rueckstaende(zahlungen, mietverhaeltnisse, index, bis_monat, konfig):
    """Alle offenen Monate der letzten zwölf, nicht nur der aktuelle.

    Wichtig: Ausgewertet wird nur der Zeitraum, für den auch Kontoumsätze
    vorliegen. Sonst gilt jeder Monat vor dem ersten Import als unbezahlt und
    das Dashboard meldet Rückstände, die es nie gab.
    """
    datierte = [b.get("datum") for b in zahlungen if b.get("datum")]
    if not datierte:
        return karte(
            "Rückstände",
            '<div class="callout info">Noch keine Kontoumsätze eingelesen. '
            "Sobald der erste Kontoauszug importiert ist, erscheint hier der "
            "Soll-Ist-Vergleich.</div>",
        )
    datenbeginn = min(datierte)[:7]

    monate = [monat_verschieben(bis_monat, -i) for i in range(0, 12)]
    monate = [m for m in monate if m >= datenbeginn]
    offene = []
    for monat in monate:
        for eintrag in zahlungsstand(zahlungen, mietverhaeltnisse, monat):
            if eintrag["status"] == "bezahlt":
                continue
            if monat == bis_monat and date.today().day <= int(konfig.get("miete_faellig_am", 5)):
                continue  # laufender Monat, Frist noch nicht verstrichen
            offene.append((monat, eintrag))
    zeitraum = "Ausgewertet: {} bis {}".format(
        monat_lesbar(monate[-1]), monat_lesbar(monate[0])
    ) if monate else ""

    if not offene:
        return karte(
            "Rückstände",
            '<div class="empty">Keine offenen Mieten im ausgewerteten Zeitraum.</div>',
            zeitraum,
        )
    summe = sum(abs(x[1]["differenz"]) for x in offene)
    zeilen = [
        "<table class='liste'><tr><th>Monat</th><th>Einheit</th><th>Mieter</th>"
        "<th class='num'>Soll</th><th class='num'>Eingegangen</th><th class='num'>Offen</th></tr>"
    ]
    for monat, eintrag in sorted(offene, key=lambda x: x[0]):
        mv = eintrag["mv"]
        zeilen.append(
            "<tr><td>{monat}</td><td>{ort}</td><td>{mieter}</td>"
            "<td class='num'>{soll}</td><td class='num'>{ist}</td>"
            "<td class='num'><strong>{offen}</strong></td></tr>".format(
                monat=e(monat_lesbar(monat)),
                ort=e(bezeichnung_fuer(mv, index)),
                mieter=e(mv["mieter_name"]),
                soll=e(eur(eintrag["soll"])),
                ist=e(eur(eintrag["ist"])),
                offen=e(eur(abs(eintrag["differenz"]))),
            )
        )
    zeilen.append("</table>")
    zeilen.append(
        '<div class="callout">Offen insgesamt: <strong>{}</strong>. '
        "Für einen Entwurf der Zahlungserinnerung sag Claude: „Mahnlauf“.</div>".format(eur(summe))
    )
    return karte("Rückstände", "\n".join(zeilen), zeitraum)


def block_pruefen(zahlungen, mietverhaeltnisse):
    namen = {mv["id"]: mv["mieter_name"] for mv in mietverhaeltnisse}
    offen = [b for b in zahlungen if b.get("status") in ("vorschlag", "unklar")
             and not b.get("bestaetigt")]
    if not offen:
        return ""
    zeilen = [
        "<table class='liste'><tr><th>Datum</th><th>Absender</th><th>Verwendungszweck</th>"
        "<th class='num'>Betrag</th><th>Vermutung</th></tr>"
    ]
    for buchung in sorted(offen, key=lambda b: b["datum"], reverse=True)[:25]:
        if buchung.get("status") == "vorschlag":
            vermutung = "{} ({} Punkte)".format(
                namen.get(buchung.get("mv_id"), "?"), buchung.get("punkte", 0)
            )
        else:
            vermutung = "keine"
        zeilen.append(
            "<tr><td>{datum}</td><td>{name}</td><td>{zweck}</td>"
            "<td class='num'>{betrag}</td><td>{vermutung}</td></tr>".format(
                datum=e("{:%d.%m.%Y}".format(parse_datum(buchung["datum"]))),
                name=e((buchung.get("name") or "")[:34]),
                zweck=e((buchung.get("zweck") or "")[:52]),
                betrag=e(eur(buchung["betrag"])),
                vermutung=e(vermutung),
            )
        )
    zeilen.append("</table>")
    return karte(
        "Zu prüfen ({})".format(len(offen)),
        "\n".join(zeilen),
        "Diese Eingänge konnte die Zuordnung nicht sicher zuweisen. "
        "Sag Claude „Zuordnungen prüfen“, dann geht ihr sie gemeinsam durch.",
    )


def block_jahresverlauf(zahlungen, jahr):
    monatssummen = {"{:04d}-{:02d}".format(jahr, m): 0.0 for m in range(1, 13)}
    for buchung in zahlungen:
        if float(buchung.get("betrag") or 0) <= 0:
            continue
        if buchung.get("status") != "sicher" and not buchung.get("bestaetigt"):
            continue
        monat = buchung.get("monat") or (buchung.get("datum") or "")[:7]
        if monat in monatssummen:
            monatssummen[monat] += float(buchung["betrag"])
    hoechstwert = max(monatssummen.values()) or 1.0
    heute = monat_key(date.today())
    balken, marken = [], []
    for monat in sorted(monatssummen):
        wert = monatssummen[monat]
        hoehe = max(3, int(round(wert / hoechstwert * 92)))
        klasse = "bar last" if monat == heute else "bar"
        beschriftung = eur_kurz(wert).replace(" EUR", "") if wert else ""
        balken.append(
            '<div class="{}" style="height:{}px"><span>{}</span></div>'.format(
                klasse, hoehe, e(beschriftung)
            )
        )
        marken.append("<span>{}</span>".format(monat.split("-")[1]))
    summe = sum(monatssummen.values())
    return karte(
        "Mieteingänge {}".format(jahr),
        '<div class="bars">{}</div><div class="barlabels">{}</div>'
        '<p class="cardnote" style="margin-top:14px">Summe {}: <strong>{}</strong></p>'.format(
            "".join(balken), "".join(marken), jahr, e(eur(summe))
        ),
    )


def block_darlehen(darlehen, objekte):
    if not darlehen:
        return ""
    namen = {o["id"]: o.get("bezeichnung", o["id"]) for o in objekte}
    heute = date.today()
    zeilen = [
        "<table class='liste'><tr><th>Objekt</th><th>Bank</th><th class='num'>Restschuld</th>"
        "<th class='num'>Zins</th><th class='num'>Rate</th><th>Zinsbindung bis</th></tr>"
    ]
    summe = 0.0
    for d in darlehen:
        rest = float(d.get("restschuld") or 0)
        summe += rest
        ende = parse_datum(d.get("zinsbindung_ende"))
        hinweis = ""
        if ende:
            monate = (ende.year - heute.year) * 12 + (ende.month - heute.month)
            if monate <= 18:
                hinweis = " <span class='badge late'>Anschluss klären</span>"
        zeilen.append(
            "<tr><td>{objekt}</td><td>{bank}</td><td class='num'>{rest}</td>"
            "<td class='num'>{zins}</td><td class='num'>{rate}</td>"
            "<td>{ende}{hinweis}</td></tr>".format(
                objekt=e(namen.get(d.get("objekt_id"), d.get("objekt_id", "-"))),
                bank=e(d.get("bank", "")),
                rest=e(eur_kurz(rest)),
                zins=e("{:.2f} %".format(float(d.get("zinssatz") or 0)).replace(".", ",")),
                rate=e(eur_kurz(d.get("rate_monatlich"))),
                ende=e("{:%m/%Y}".format(ende) if ende else "-"),
                hinweis=hinweis,
            )
        )
    zeilen.append(
        "<tr><td colspan='2'><strong>Summe</strong></td>"
        "<td class='num'><strong>{}</strong></td><td colspan='3'></td></tr>".format(
            e(eur_kurz(summe))
        )
    )
    zeilen.append("</table>")
    return karte("Darlehen", "\n".join(zeilen),
                 "Zinsbindung unter 18 Monaten wird markiert, damit die "
                 "Anschlussfinanzierung in Ruhe verhandelt werden kann.")


def block_fristen(fristen, objekte):
    if not fristen:
        return ""
    namen = {o["id"]: o.get("bezeichnung", o["id"]) for o in objekte}
    heute = date.today()
    kommend = []
    for frist in fristen:
        faellig = parse_datum(frist.get("faellig"))
        if not faellig:
            continue
        tage = (faellig - heute).days
        if tage < -30 or tage > 400:
            continue
        kommend.append((tage, faellig, frist))
    if not kommend:
        return ""
    reihen = []
    for tage, faellig, frist in sorted(kommend):
        if tage < 0:
            klasse, text = "late", "überfällig"
        elif tage <= 30:
            klasse, text = "open", "in {} Tagen".format(tage)
        else:
            klasse, text = "neutral", "{:%d.%m.%Y}".format(faellig)
        reihen.append(
            '<div class="row"><div class="info"><div class="obj">{titel}</div>'
            '<div class="meta">{objekt}</div></div>'
            '<span class="badge {klasse}">{text}</span></div>'.format(
                titel=e(frist.get("titel", "")),
                objekt=e(namen.get(frist.get("objekt_id"), "alle Objekte")),
                klasse=klasse,
                text=e(text),
            )
        )
    return karte("Fristen & Wartung", "\n".join(reihen))


def block_ausgaben(zahlungen, jahr):
    ausgaben = [
        b for b in zahlungen
        if float(b.get("betrag") or 0) < 0 and (b.get("datum") or "").startswith(str(jahr))
    ]
    if not ausgaben:
        return ""
    nach_kategorie = {}
    for buchung in ausgaben:
        kategorie = buchung.get("kategorie") or "nicht kategorisiert"
        nach_kategorie[kategorie] = nach_kategorie.get(kategorie, 0.0) + abs(
            float(buchung["betrag"])
        )
    zeilen = ["<table class='liste'><tr><th>Kategorie</th><th class='num'>Betrag</th></tr>"]
    for kategorie, betrag in sorted(nach_kategorie.items(), key=lambda x: -x[1]):
        zeilen.append(
            "<tr><td>{}</td><td class='num'>{}</td></tr>".format(e(kategorie), e(eur(betrag)))
        )
    zeilen.append(
        "<tr><td><strong>Summe</strong></td><td class='num'><strong>{}</strong></td></tr>".format(
            e(eur(sum(nach_kategorie.values())))
        )
    )
    zeilen.append("</table>")
    return karte(
        "Ausgaben {}".format(jahr),
        "\n".join(zeilen),
        "Grundlage für die Werbungskosten in der Anlage V. Sag Claude "
        "„Ausgaben kategorisieren“, um offene Posten zuzuordnen.",
    )


# ---------------------------------------------------------------------- Bau

def baue():
    konfig = lade("konfig", {})
    objekte = lade("objekte", [])
    mietverhaeltnisse = lade("mietverhaeltnisse", [])
    darlehen = lade("darlehen", [])
    fristen = lade("fristen", [])
    zahlungen = lade("zahlungen", [])

    index = einheiten_index(objekte)
    heute = date.today()
    monat = monat_key(heute)
    aktive = [mv for mv in mietverhaeltnisse if ist_aktiv(mv)]
    stand = zahlungsstand(zahlungen, mietverhaeltnisse, monat)

    soll_gesamt = sum(sollmiete(mv) for mv in aktive)
    ist_gesamt = sum(s["ist"] for s in stand)
    offen_gesamt = sum(max(0.0, -s["differenz"]) for s in stand)
    einheiten_gesamt = sum(len(o.get("einheiten", [])) for o in objekte)
    vermietet = len(aktive)
    leerstand = einheiten_gesamt - vermietet

    metriken = [
        ("Sollmiete pro Monat", eur_kurz(soll_gesamt), ""),
        ("Eingegangen", eur_kurz(ist_gesamt), "green" if ist_gesamt else ""),
        ("Noch offen", eur_kurz(offen_gesamt), "red" if offen_gesamt > 0 else "green"),
        ("Einheiten", "{} / {}".format(vermietet, einheiten_gesamt),
         "amber" if leerstand else ""),
    ]
    metrik_html = "".join(
        '<div class="metric"><div class="label">{}</div>'
        '<div class="value {}">{}</div></div>'.format(e(label), klasse, e(wert))
        for label, wert, klasse in metriken
    )

    teile = [block_zahlungsstatus(stand, index, monat)]
    teile.append(block_rueckstaende(zahlungen, mietverhaeltnisse, index, monat, konfig))
    teile.append(block_pruefen(zahlungen, mietverhaeltnisse))
    teile.append(block_jahresverlauf(zahlungen, heute.year))
    teile.append(block_ausgaben(zahlungen, heute.year))
    teile.append(block_darlehen(darlehen, objekte))
    teile.append(block_fristen(fristen, objekte))

    if not objekte:
        teile.insert(
            0,
            '<div class="callout">Es sind noch keine Objekte erfasst. Sag Claude: '
            "„Lass uns meine Objekte erfassen“ – er fragt alles der Reihe nach ab.</div>",
        )

    # Belegliste fuer den Steuerberater, laeuft ohne Server im Browser
    export = [
        {
            "datum": b.get("datum"),
            "betrag": b.get("betrag"),
            "zweck": b.get("zweck"),
            "name": b.get("name"),
            "kategorie": b.get("kategorie") or ("Mieteinnahme" if float(b.get("betrag") or 0) > 0 else ""),
        }
        for b in zahlungen
        if (b.get("datum") or "").startswith(str(heute.year))
    ]

    vermieter = konfig.get("vermieter_name") or "Mietverwaltung"
    dokument = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titel}</title>
<style>{stil}</style>
</head>
<body>
<div class="wrap">
  <h1>{titel}</h1>
  <p class="lead">Stand {stand} &middot; {objekte} Objekte, {einheiten} Einheiten</p>
  <div class="metrics">{metriken}</div>
  {inhalt}
  <div class="card">
    <h3>Export für die Steuer</h3>
    <p class="cardnote">Alle Buchungen des laufenden Jahres als CSV, direkt für den
    Steuerberater oder die Anlage V.</p>
    <button id="csv">Belegliste {jahr} herunterladen</button>
  </div>
  <footer>Erzeugt am {zeit} aus den Daten in daten\\ &middot; enthält echte Mieterdaten,
  bitte nicht weitergeben.</footer>
</div>
<script>
const daten = {export_json};
document.getElementById("csv").addEventListener("click", function () {{
  const kopf = "Datum;Betrag;Kategorie;Name;Verwendungszweck";
  const zeilen = daten.map(function (d) {{
    const feld = function (w) {{ return String(w == null ? "" : w).replace(/;/g, ","); }};
    return [feld(d.datum), String(d.betrag).replace(".", ","), feld(d.kategorie),
            feld(d.name), feld(d.zweck)].join(";");
  }});
  const inhalt = "\\ufeff" + [kopf].concat(zeilen).join("\\n");
  const blob = new Blob([inhalt], {{type: "text/csv;charset=utf-8"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "Belegliste_{jahr}.csv";
  a.click();
}});
</script>
</body>
</html>
""".format(
        titel=e(vermieter),
        stil=STIL,
        stand=e("{:%d.%m.%Y}".format(heute)),
        objekte=len(objekte),
        einheiten=einheiten_gesamt,
        metriken=metrik_html,
        inhalt="\n".join(t for t in teile if t),
        jahr=heute.year,
        zeit=e("{:%d.%m.%Y %H:%M}".format(datetime.now())),
        export_json=json.dumps(export, ensure_ascii=False),
    )

    ziel = AUSGABE / "Dashboard.html"
    ziel.write_text(dokument, encoding="utf-8")
    return ziel, len(objekte), einheiten_gesamt, offen_gesamt


def main():
    konsole_utf8()
    ziel, objekte, einheiten, offen = baue()
    print("Dashboard gebaut: {}".format(ziel))
    print("  {} Objekte, {} Einheiten".format(objekte, einheiten))
    if offen > 0:
        print("  offen diesen Monat: {}".format(eur(offen)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
