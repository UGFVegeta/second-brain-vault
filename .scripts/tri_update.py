#!/usr/bin/env python3
"""Aktualisiert alle Wettkampf-Dashboards (Triathlon).

Was das Skript macht:
  1. lädt für jedes Rennen aus tri_races.json die Komoot-Tracks (GPS + Höhen +
     Untergrund) und legt sie im Rennordner unter assets/ ab,
  2. berechnet daraus Höhenprofil, Anstiege, Untergrund-Anteile und eine
     SVG-taugliche Projektion und schreibt sie als strecken_data.js,
  3. lädt konfigurierte Streckenbilder der Veranstalter herunter,
  4. prüft die Textquellen der Veranstalterseiten auf Änderungen (Hash-Vergleich)
     und meldet, wo sich seit dem letzten Lauf etwas geändert hat,
  5. schreibt races.js für die Übersichtsseite.

Aufruf:
    python3 .scripts/tri_update.py            # alles aktualisieren
    python3 .scripts/tri_update.py breisgau   # nur passende Rennen (Filter auf id)

Textinhalte der Dashboards (Zeitplan, Gebühren, Regeln) stehen bewusst direkt im
HTML und werden NICHT automatisch überschrieben. Wenn Punkt 4 eine Änderung
meldet, gehören die betroffenen Stellen von Hand nachgezogen.
"""

import hashlib
import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = os.path.join(BASE, ".scripts", "tri_races.json")
STATE = os.path.join(BASE, ".scripts", "tri_state.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

LABEL_SURF = {
    "asphalt": "Asphalt", "paved": "Befestigt", "unpaved": "Unbefestigt",
    "gravel": "Schotter", "fine_gravel": "Feinschotter", "cobbles": "Kopfsteinpflaster",
    "sett": "Pflastersteine", "paving_stones": "Pflaster", "concrete": "Beton",
    "nature": "Naturbelag", "ground": "Naturboden", "dirt": "Erdweg", "earth": "Erdweg",
    "grass": "Gras", "compacted": "Wassergebundene Decke", "sand": "Sand",
    "wood": "Holz", "metal": "Metall", "unknown": "Unbekannt", "alpin": "Alpin",
}
LABEL_WAY = {
    "street": "Straße", "minor_road": "Nebenstraße", "way": "Wirtschafts-/Feldweg",
    "cycleway": "Radweg", "service": "Zufahrt", "path": "Pfad",
    "hiking_path": "Wanderpfad", "off_grid": "Weglos / nicht kartiert",
    "trail": "Trail", "unknown": "Unbekannt", "ferry": "Fähre",
    "hike_d1": "Wanderweg", "hike_d2": "Wanderweg", "hike_d3": "Bergweg",
}

STEP = 50.0          # Stützstellen des Profils in Metern
SMOOTH_WIN = 3       # Glättungsfenster (±150 m)


# --------------------------------------------------------------------------- #
# Hilfsfunktionen
# --------------------------------------------------------------------------- #
def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def meters(a, b):
    dx = (b["lng"] - a["lng"]) * 111320 * math.cos(math.radians(a["lat"]))
    dy = (b["lat"] - a["lat"]) * 110540
    return math.hypot(dx, dy)


def label(el, table):
    key = el.split("#")[-1] if "#" in el else el
    return table.get(key, key)


# --------------------------------------------------------------------------- #
# Auswertung eines Komoot-Tracks
# --------------------------------------------------------------------------- #
def rundenlaenge(pts, cum, runden, tol=40.0):
    """Rundenlänge aus dem Track selbst bestimmen: einen Referenzpunkt in der
    Mitte suchen und zählen, wie oft die Strecke dort wieder vorbeikommt."""
    if runden < 2:
        return None, None
    ref = pts[int(len(pts) * 0.6)]
    treffer = []
    for i, p in enumerate(pts):
        if meters(ref, p) < tol:
            treffer.append(i)
    gruppen = []
    for i in treffer:
        if gruppen and cum[i] - cum[gruppen[-1][-1]] < 500:
            gruppen[-1].append(i)
        else:
            gruppen.append([i])
    zentren = [cum[g[len(g) // 2]] for g in gruppen]
    erwartet = cum[-1] / runden
    # Nur Abstände plausibler Größe zählen: Wendepunktkurse treffen denselben
    # Referenzpunkt auch innerhalb einer Runde mehrfach.
    diffs = sorted(b - a for a, b in zip(zentren, zentren[1:])
                   if 0.7 * erwartet <= (b - a) <= 1.15 * erwartet)
    lap = diffs[len(diffs) // 2] if diffs else erwartet
    vorlauf = max(0.0, cum[-1] - lap * runden)
    return lap, vorlauf


def analyse(raw, runden=1):
    pts = raw["_embedded"]["coordinates"]["items"]
    cum = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum.append(cum[-1] + meters(a, b))
    total = cum[-1]
    lap, vorlauf = rundenlaenge(pts, cum, runden)

    grid = [i * STEP for i in range(int(total // STEP) + 1)]

    def alt_at(x):
        if x <= 0:
            return pts[0]["alt"]
        if x >= total:
            return pts[-1]["alt"]
        lo, hi = 0, len(cum) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if cum[mid] <= x:
                lo = mid
            else:
                hi = mid
        f = (x - cum[lo]) / max(1e-9, cum[hi] - cum[lo])
        return pts[lo]["alt"] + f * (pts[hi]["alt"] - pts[lo]["alt"])

    rawalt = [alt_at(x) for x in grid]
    W = SMOOTH_WIN
    smooth = [sum(rawalt[max(0, i - W):i + W + 1]) / len(rawalt[max(0, i - W):i + W + 1])
              for i in range(len(rawalt))]

    grade = [0.0] + [(smooth[i] - smooth[i - 1]) / STEP * 100 for i in range(1, len(smooth))]
    gain = sum(max(0.0, b - a) for a, b in zip(smooth, smooth[1:]))
    loss = sum(max(0.0, a - b) for a, b in zip(smooth, smooth[1:]))

    def segments(sign, min_len=250, min_grade=2.0):
        out, start = [], None
        for i, g in enumerate(grade):
            steep = (g * sign) >= min_grade * 0.4
            if steep and start is None:
                start = i
            elif not steep and start is not None:
                out.append((start, i))
                start = None
        if start is not None:
            out.append((start, len(grade) - 1))
        merged = []
        for s, e in out:
            if merged and (s - merged[-1][1]) * STEP < 200:
                merged[-1] = (merged[-1][0], e)
            else:
                merged.append((s, e))
        res = []
        for s, e in merged:
            length = (e - s) * STEP
            dh = smooth[e] - smooth[s]
            if length < min_len or abs(dh) / max(length, 1) * 100 < min_grade:
                continue
            res.append({
                "von": round(grid[s] / 1000, 2), "bis": round(grid[e] / 1000, 2),
                "laenge": round(length), "hm": round(abs(dh)),
                "schnitt": round(abs(dh) / length * 100, 1),
                "max": round(max(grade[i] * sign for i in range(s, e + 1)), 1),
                "vonHoehe": round(smooth[s]), "bisHoehe": round(smooth[e]),
            })
        return res

    def spans(key, table):
        items = raw.get("_embedded", {}).get(key, {}).get("items", [])
        agg = {}
        for it in items:
            a, b = it["from"], min(it["to"], len(cum) - 1)
            agg[label(it["element"], table)] = agg.get(label(it["element"], table), 0) + (cum[b] - cum[a])
        ges = sum(agg.values()) or 1
        return [{"typ": k, "meter": round(v), "anteil": round(v / ges * 100, 1)}
                for k, v in sorted(agg.items(), key=lambda x: -x[1])]

    # Projektion für die SVG-Karte
    lat0 = sum(p["lat"] for p in pts) / len(pts)
    kx = math.cos(math.radians(lat0))
    xs = [p["lng"] * kx for p in pts]
    ys = [-p["lat"] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    span = max(maxx - minx, maxy - miny) or 1e-9
    track, tgrade = [], []
    for i, p in enumerate(pts):
        track.append([round((xs[i] - minx) / span * 1000, 1),
                      round((ys[i] - miny) / span * 1000, 1),
                      round(cum[i] / 1000, 2), round(p["alt"], 1)])
        tgrade.append(round(grade[min(int(cum[i] // STEP), len(grade) - 1)], 1))

    return {
        "name": raw.get("name"),
        "runden": runden,
        "distanzKm": round(total / 1000, 2),
        "rundeKm": round(lap / 1000, 2) if lap else None,
        "vorlaufKm": round(vorlauf / 1000, 2) if lap else None,
        "rundenGrenzen": [round((vorlauf + lap * i) / 1000, 2) for i in range(1, runden)] if lap else [],
        "hmAufKomoot": round(raw.get("elevation_up") or 0),
        "hmAbKomoot": round(raw.get("elevation_down") or 0),
        "hmAufGeglaettet": round(gain),
        "hmAbGeglaettet": round(loss),
        "minHoehe": round(min(smooth)), "maxHoehe": round(max(smooth)),
        "startHoehe": round(smooth[0]),
        "maxSteigung": round(max(grade), 1), "maxGefaelle": round(min(grade), 1),
        "profil": [[round(x / 1000, 3), round(a, 1)] for x, a in zip(grid, smooth)],
        "anstiege": segments(+1), "abfahrten": segments(-1),
        "untergrund": spans("surfaces", LABEL_SURF),
        "wegtypen": spans("way_types", LABEL_WAY),
        "track": track, "trackSteigung": tgrade,
        "bbox": {"w": round((maxx - minx) / span * 1000, 1),
                 "h": round((maxy - miny) / span * 1000, 1)},
        "startLatLng": [pts[0]["lat"], pts[0]["lng"]],
        "zielLatLng": [pts[-1]["lat"], pts[-1]["lng"]],
    }


# --------------------------------------------------------------------------- #
# Quellenseiten auf Änderungen prüfen
# --------------------------------------------------------------------------- #
def pdf_zu_png(pdf, ziel, name, seiten):
    """Wandelt PDF-Seiten in PNG um. Nutzt pdftoppm, sonst PyMuPDF.
    Ohne beides bleibt nur das PDF liegen, die Dashboards verlinken es dann."""
    ok = 0
    try:
        import subprocess
        for s in seiten:
            out = os.path.join(ziel, "%s-%d" % (name, s))
            res = subprocess.run(["pdftoppm", "-png", "-r", "150", "-f", str(s), "-l", str(s),
                                  "-singlefile", pdf, out],
                                 capture_output=True)
            if res.returncode == 0 and os.path.exists(out + ".png"):
                ok += 1
        if ok:
            for s in seiten:
                rand_abschneiden(os.path.join(ziel, "%s-%d.png" % (name, s)))
            return ok
    except FileNotFoundError:
        pass
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf)
        for s in seiten:
            if s - 1 < len(doc):
                doc[s - 1].get_pixmap(dpi=150).save(os.path.join(ziel, "%s-%d.png" % (name, s)))
                ok += 1
    except Exception:                                    # noqa: BLE001
        pass
    for s in seiten:
        rand_abschneiden(os.path.join(ziel, "%s-%d.png" % (name, s)))
    return ok


def rand_abschneiden(png):
    """Weiße Seitenränder eines gerenderten PDF-Blatts wegschneiden."""
    try:
        from PIL import Image
        if not os.path.exists(png):
            return
        bild = Image.open(png).convert("RGB")
        # nahezu weiße Pixel als Rand behandeln, sonst bleibt das leere Blattende stehen
        maske = bild.convert("L").point(lambda p: 0 if p > 244 else 255)
        kasten = maske.getbbox()
        if kasten and (kasten[2] - kasten[0]) > 200 and (kasten[3] - kasten[1]) > 200:
            bild.crop(kasten).save(png)
    except Exception:                                    # noqa: BLE001
        pass


def page_hash(url):
    html = get(url).decode("utf-8", "ignore")
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), len(text)


# --------------------------------------------------------------------------- #
def main():
    conf = json.load(open(CONF, encoding="utf-8"))
    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    ziel = os.path.join(BASE, conf["zielordner"])
    filt = sys.argv[1].lower() if len(sys.argv) > 1 else None

    uebersicht, aenderungen = [], []

    for r in conf["rennen"]:
        if filt and filt not in r["id"].lower() and filt not in r["ordner"].lower():
            continue
        ordner = os.path.join(ziel, r["ordner"])
        assets = os.path.join(ordner, "assets")
        os.makedirs(assets, exist_ok=True)
        print("\n### %s (%s)" % (r["name"], r["id"]))

        # --- Komoot-Tracks -------------------------------------------------- #
        disz = {}
        for key, k in (r.get("komoot") or {}).items():
            url = ("https://www.komoot.de/api/v007/tours/%s?share_token=%s"
                   "&_embedded=coordinates,way_types,surfaces" % (k["id"], k["token"]))
            try:
                raw = json.loads(get(url))
            except Exception as e:                       # noqa: BLE001
                print("   ! %-10s Komoot-Abruf fehlgeschlagen: %s" % (key, e))
                alt = os.path.join(assets, "komoot_%s.json" % key)
                if not os.path.exists(alt):
                    continue
                print("     -> nutze gespeicherte Kopie")
                raw = json.load(open(alt, encoding="utf-8"))
            else:
                with open(os.path.join(assets, "komoot_%s.json" % key), "w", encoding="utf-8") as f:
                    json.dump(raw, f, ensure_ascii=False)
            d = analyse(raw, k.get("runden", 1))
            disz[key] = d
            print("   %-10s %6.2f km | %4d hm (Komoot) | %4d hm (geglättet)"
                  % (key, d["distanzKm"], d["hmAufKomoot"], d["hmAufGeglaettet"]))

        # --- Bilder --------------------------------------------------------- #
        for b in r.get("bilder", []):
            pfad = os.path.join(assets, b["datei"])
            try:
                data = get(b["url"])
                with open(pfad, "wb") as f:
                    f.write(data)
                print("   Bild %-22s %6.1f KB" % (b["datei"], len(data) / 1024))
            except Exception as e:                       # noqa: BLE001
                print("   ! Bild %s nicht geladen: %s" % (b["datei"], e))

        # --- PDFs (Streckenpläne, Zeitpläne) als Bild ------------------------ #
        for p in r.get("pdfs", []):
            pdf = os.path.join(assets, p["datei"] + ".pdf")
            try:
                with open(pdf, "wb") as f:
                    f.write(get(p["url"]))
            except Exception as e:                       # noqa: BLE001
                print("   ! PDF %s nicht geladen: %s" % (p["datei"], e))
                continue
            seiten = pdf_zu_png(pdf, assets, p["datei"], p.get("seiten", [1]))
            print("   PDF  %-22s %d Seite(n) als PNG" % (p["datei"], seiten))

        # --- Quellenseiten -------------------------------------------------- #
        st = state.setdefault(r["id"], {})
        quellen_status = []
        for url in r.get("quellen", []):
            try:
                h, laenge = page_hash(url)
            except Exception as e:                       # noqa: BLE001
                print("   ! Quelle nicht erreichbar: %s (%s)" % (url, e))
                quellen_status.append({"url": url, "status": "nicht erreichbar"})
                continue
            alt = st.get(url)
            if alt is None:
                zustand = "neu erfasst"
            elif alt["hash"] == h:
                zustand = "unverändert"
            else:
                zustand = "GEÄNDERT"
                aenderungen.append((r["kurz"], url))
            st[url] = {"hash": h, "zeichen": laenge,
                       "geprueft": datetime.now().strftime("%Y-%m-%d %H:%M")}
            quellen_status.append({"url": url, "status": zustand})
            print("   Quelle %-9s %s" % (zustand, url.replace("https://", "")))

        # --- Datendatei schreiben ------------------------------------------- #
        daten = {
            "rennen": {k: r.get(k) for k in ("id", "name", "kurz", "untertitel", "datum",
                                             "ort", "distanzen", "webseite", "akzent", "sportart")},
            "stand": datetime.now().strftime("%d.%m.%Y"),
            "disziplinen": disz,
            "quellen": quellen_status,
        }
        with open(os.path.join(ordner, "strecken_data.js"), "w", encoding="utf-8") as f:
            f.write("// automatisch erzeugt von .scripts/tri_update.py – nicht von Hand bearbeiten\n")
            f.write("const STRECKEN = ")
            json.dump(daten, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")

        uebersicht.append({
            "id": r["id"], "ordner": r["ordner"], "name": r["name"], "kurz": r["kurz"],
            "sportart": r.get("sportart", "triathlon"),
            "untertitel": r["untertitel"], "datum": r["datum"], "ort": r["ort"],
            "distanzen": r["distanzen"], "webseite": r["webseite"], "akzent": r["akzent"],
            "stand": daten["stand"],
            "kennzahlen": {k: {"km": v["distanzKm"], "hm": v["hmAufKomoot"],
                               "runden": v["runden"]} for k, v in disz.items()},
            "quellenGeaendert": [q["url"] for q in quellen_status if q["status"] == "GEÄNDERT"],
        })

    # --- Übersichtsdatei ---------------------------------------------------- #
    if not filt:
        hub = uebersicht
    else:  # bei Teil-Läufen die bestehende Übersicht ergänzen statt ersetzen
        alt_pfad = os.path.join(ziel, "races.js")
        hub = []
        if os.path.exists(alt_pfad):
            txt = open(alt_pfad, encoding="utf-8").read()
            m = re.search(r"const RENNEN = (\[.*\]);", txt, re.S)
            if m:
                hub = json.loads(m.group(1))
        ids = {u["id"] for u in uebersicht}
        hub = [h for h in hub if h["id"] not in ids] + uebersicht

    hub.sort(key=lambda x: x["datum"])
    with open(os.path.join(ziel, "races.js"), "w", encoding="utf-8") as f:
        f.write("// automatisch erzeugt von .scripts/tri_update.py – nicht von Hand bearbeiten\n")
        f.write("const RENNEN = ")
        json.dump(hub, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\nconst STAND = \"%s\";\n" % datetime.now().strftime("%d.%m.%Y %H:%M"))

    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)

    print("\n" + "=" * 62)
    if aenderungen:
        print("ACHTUNG: Diese Veranstalterseiten haben sich geändert.")
        print("Die Texte in den Dashboards (Zeitplan, Gebühren, Regeln) prüfen:")
        for kurz, url in aenderungen:
            print("  [%s] %s" % (kurz, url))
    else:
        print("Keine Textänderungen auf den Veranstalterseiten gefunden.")
    print("Strecken- und Höhendaten sind aktualisiert.")


if __name__ == "__main__":
    main()
