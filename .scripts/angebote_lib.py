#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Angebote aus den Prospekten der Gegend (Quelle: marktguru).

Marktguru hat keine offizielle Schnittstelle. Die Schlüssel unten stehen öffentlich
im Quelltext von marktguru.de und werden auch von deren Webseite benutzt. Ändert
marktguru sie, schlägt der Abruf fehl: dann neue Werte aus dem Seitenquelltext
("apiKey", "clientKey") hier eintragen. Oskar hat diesen Weg am 14.11.2026 freigegeben.

Dateien in 04 Ressourcen/Angebote/:
  einstellungen.json  Orte (PLZ), ausgeblendete Märkte, Favoriten
  angebote_data.js    Favoriten-Angebote vom letzten Abruf (liest Angebote.html)
  preise.json         Preisverlauf, damit die App "bisher günstigster Preis" zeigen kann

Aufruf ohne Argumente: Favoriten neu holen (macht auch der Dashboard-Dienst jeden Morgen).
Aufruf mit Begriff:     python3 angebote_lib.py "weizen alkoholfrei"   (Test der Suche)
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, date
from pathlib import Path

ORDNER = Path(__file__).resolve().parent.parent / "04 Ressourcen" / "Angebote"
EINST = ORDNER / "einstellungen.json"
DATA_JS = ORDNER / "angebote_data.js"
PREISE = ORDNER / "preise.json"

API = "https://api.marktguru.de/api/v1/offers/search"
KOPF = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "x-apikey": "8Kk+pmbf7TgJ9nVj2cXeA7P5zBGv8iuutVVMRfOfvNE=",
    "x-clientkey": "WU/RH+PMGDi+gkZer3WbMelt6zcYHSTytNB7VpTia90=",
}

# Wörter, die im Prospekt oft anders heißen als in der Suche.
SYNONYME = {
    "weizen": ["weizen", "weißbier", "weissbier", "weißbräu", "weissbräu"],
    "weissbier": ["weizen", "weißbier", "weissbier", "weißbräu", "weissbräu"],
    # Prospekte vertippen sich ("alkohofrei" bei Franziskaner/Netto) oder schreiben 0,0 %
    "alkoholfrei": ["alkoholfrei", "alkohofrei", "alkolfrei", "alkoholfr", "alkoh. frei", "0,0 %", "0,0%", "0.0"],
    "kaffee": ["kaffee", "café", "caffè", "espresso", "crema"],
    "wasser": ["wasser", "sprudel", "mineral"],
    "klopapier": ["toilettenpapier", "klopapier"],
    "spuelmaschine": ["spülmaschin", "geschirrspül", "tabs"],
}


def einstellungen():
    return json.loads(EINST.read_text(encoding="utf-8"))


def einstellungen_speichern(neu):
    alt = einstellungen()
    for k in ("orte", "aus", "favoriten"):
        if k in neu:
            alt[k] = neu[k]
    EINST.write_text(json.dumps(alt, ensure_ascii=False, indent=2), encoding="utf-8")
    return alt


def _klein(t):
    return (t or "").lower()


def _stamm(w):
    """alkoholfreies -> alkoholfrei; kurze Wörter bleiben, wie sie sind."""
    w = w.lower()
    if len(w) >= 8:
        for end in ("es", "er", "en", "em", "e", "s"):
            if w.endswith(end):
                return w[: -len(end)]
    return w


def _varianten(wort):
    s = _stamm(wort)
    schluessel = s.replace("ü", "ue").replace("ä", "ae").replace("ö", "oe").replace("ß", "ss")
    return SYNONYME.get(schluessel, SYNONYME.get(s, [s]))


def _abruf(q, plz):
    url = API + "?" + urllib.parse.urlencode({"as": "web", "q": q, "zipCode": plz, "limit": 250})
    req = urllib.request.Request(url, headers=KOPF)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r).get("results", [])


def _lokal(iso):
    """API-Zeiten sind UTC; 2026-11-08T23:00:00Z ist der 09.11. bei uns."""
    if not iso:
        return None
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone().date().isoformat()


def _aufbereiten(o):
    v = (o.get("validityDates") or [{}])[0]
    marke = (o.get("brand") or {}).get("name") or ""
    produkt = (o.get("product") or {}).get("name") or ""
    kat = ((o.get("categories") or [{}])[0] or {}).get("name") or ""
    einheit = (o.get("unit") or {}).get("shortName") or ""
    return {
        "id": o.get("id"),
        "markt": ((o.get("advertisers") or [{}])[0] or {}).get("name") or "?",
        "marke": marke,
        "produkt": produkt,
        "text": o.get("description") or "",
        "kategorie": kat,
        "preis": o.get("price"),
        "alt": o.get("oldPrice"),
        "grundpreis": o.get("referencePrice"),
        "einheit": einheit,
        "von": _lokal(v.get("from")),
        "bis": _lokal(v.get("to")),
        "karte": bool(o.get("requiresLoyalityMembership")),
        "url": o.get("externalUrl") or "",
        "bild": f"https://mg2de.b-cdn.net/api/v1/offers/{o.get('id')}/images/default/0/small.jpg",
    }


def suchen(begriff, plz_liste=None):
    """Sucht in allen aktiven Orten. Liefert nur Angebote, die heute oder später gelten
    und alle Suchwörter (oder ein Synonym davon) enthalten."""
    if plz_liste is None:
        plz_liste = [o["plz"] for o in einstellungen()["orte"] if o.get("aktiv")]
    woerter = [w for w in re.split(r"\s+", begriff.strip()) if w]
    if not woerter:
        return []
    anfragen = [begriff]
    for w in woerter:  # jedes Wort und seine Synonyme einzeln, sonst fehlt z. B. "Hefeweißbier" bei "weizen"
        anfragen += [_stamm(w)] + [v for v in _varianten(w) if len(v) >= 5]
    roh = {}
    for plz in plz_liste:
        for q in dict.fromkeys(anfragen):
            try:
                for o in _abruf(q, plz):
                    roh.setdefault(o.get("id"), o)
            except Exception as e:  # ein Ort fällt aus, der Rest läuft weiter
                print(f"Abruf {q!r} / {plz}: {e}", file=sys.stderr)
            time.sleep(0.2)
    heute = date.today().isoformat()
    treffer, gesehen = [], set()
    for o in roh.values():
        a = _aufbereiten(o)
        if a["bis"] and a["bis"] < heute:
            continue
        doppelt = (a["markt"], _klein(a["marke"]), _klein(a["produkt"]), a["preis"], a["von"])
        if doppelt in gesehen:  # dasselbe Angebot steht oft mehrfach im Prospekt
            continue
        gesehen.add(doppelt)
        hay = _klein(" ".join([a["marke"], a["produkt"], a["text"], a["kategorie"]]))
        if all(any(v in hay for v in _varianten(w)) for w in woerter):
            treffer.append(a)
    treffer.sort(key=lambda a: (a["grundpreis"] or a["preis"] or 999, a["preis"] or 999))
    _verlauf_merken(treffer)
    return treffer


def _schluessel(a):
    return f"{_klein(a['marke'])}|{_klein(a['produkt'])}|{_klein(a['text'])}"


def _verlauf_merken(treffer):
    try:
        verlauf = json.loads(PREISE.read_text(encoding="utf-8")) if PREISE.exists() else {}
    except Exception:
        verlauf = {}
    for a in treffer:
        if a["preis"] is None:
            continue
        eintrag = [a["von"] or date.today().isoformat(), a["preis"], a["markt"]]
        liste = verlauf.setdefault(_schluessel(a), [])
        if eintrag not in liste:
            liste.append(eintrag)
            del liste[:-30]
    PREISE.write_text(json.dumps(verlauf, ensure_ascii=False), encoding="utf-8")


def bestpreise(treffer):
    """Günstigster früherer Angebotspreis (aus früheren Wochen) je Angebot."""
    try:
        verlauf = json.loads(PREISE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    erg = {}
    for a in treffer:
        frueher = [e for e in verlauf.get(_schluessel(a), []) if e[0] < (a["von"] or "")]
        if frueher:
            b = min(frueher, key=lambda e: e[1])
            erg[str(a["id"])] = {"preis": b[1], "datum": b[0], "markt": b[2]}
    return erg


def mit_bestpreis(treffer):
    bp = bestpreise(treffer)
    for a in treffer:
        a["bisher"] = bp.get(str(a["id"]))
    return treffer


def holen():
    """Favoriten für alle aktiven Orte holen und angebote_data.js schreiben."""
    e = einstellungen()
    plz = [o["plz"] for o in e["orte"] if o.get("aktiv")]
    fav = {}
    for f in e["favoriten"]:
        treffer = suchen(f.get("suche") or f["name"], plz)
        if f.get("kategorien"):  # z. B. Milch nur aus der Kategorie Milch, nicht Milchschokolade
            treffer = [a for a in treffer if a["kategorie"] in f["kategorien"]]
        if f.get("muss"):  # Regeln (regulärer Ausdruck), die alle passen müssen, z. B. Kaffee: ganze Bohnen und 1 kg
            treffer = [a for a in treffer
                       if all(re.search(m, _klein(f"{a['marke']} {a['produkt']} {a['text']}")) for m in f["muss"])]
        if f.get("ohne"):  # z. B. Bier ohne Weizen, das hat einen eigenen Favoriten
            treffer = [a for a in treffer
                       if not any(w in _klein(f"{a['marke']} {a['produkt']} {a['text']}") for w in f["ohne"])]
        fav[f["name"]] = mit_bestpreis(treffer)
    stand = datetime.now().strftime("%Y-%m-%d %H:%M")
    daten = {"stand": stand, "favoriten": fav, "einstellungen": e}
    DATA_JS.write_text("window.ANGEBOTE = " + json.dumps(daten, ensure_ascii=False) + ";\n", encoding="utf-8")
    return stand


def stand():
    """Datum des letzten Abrufs (für den Morgenabruf im Dashboard-Dienst)."""
    try:
        m = re.search(r'"stand": "([\d-]+)', DATA_JS.read_text(encoding="utf-8")[:300])
        return m.group(1) if m else None
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for a in suchen(" ".join(sys.argv[1:])):
            print(f"{a['markt']:<22} {a['marke']} {a['produkt']} | {a['preis']} € (alt {a['alt']}) | {a['von']}–{a['bis']}")
    else:
        print("Stand:", holen())
