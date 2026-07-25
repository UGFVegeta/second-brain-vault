#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Lebens-Dashboard – Daten-Refresh.

Sammelt alle Quellen ein und schreibt "04 Ressourcen/leben_data.js":
  - Apple Kalender (EventKit, heute + morgen, inkl. Serientermine)
  - Projekte aus 02 Projekte/ (Frontmatter-Status)
  - Training von intervals.icu (Form, Heatmap 140 Tage, Wochenstunden)
  - Vault-Aktivität aus der Git-Historie (Heatmap)
  - PV-Anlage (Kostal, live)
  - Lesestand (aus Lese-Dashboard.html, Quelle der Wahrheit)
  - Schule (iCloud-Ordnerstruktur + Dashboard-Links)

Jede Quelle ist unabhängig – fällt eine aus, laufen die anderen weiter
und das Dashboard zeigt den letzten Stand mit Fehlerhinweis.

Start:  python3 .scripts/leben_refresh.py
        (oder Doppelklick auf "04 Ressourcen/Lebens-Dashboard aktualisieren.command")
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

VAULT = Path("/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude")
OUT = VAULT / "04 Ressourcen" / "leben_data.js"
ICLOUD_GDRS = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud"
HEAT_DAYS = 140

sys.path.insert(0, str(VAULT / ".scripts"))

data = {"generated": datetime.now().strftime("%Y-%m-%dT%H:%M"), "errors": {}}


def section(name):
    def deco(fn):
        try:
            data[name] = fn()
            print(f"  ✓ {name}")
        except Exception as e:
            data[name] = None
            data["errors"][name] = f"{type(e).__name__}: {e}"[:200]
            print(f"  ✗ {name}: {e}")
    return deco


print("Lebens-Dashboard – Refresh läuft …")


# --- Kalender (AppleScript, EventKit ist für CLI-Prozesse TCC-gesperrt) -----
KAL_SCRIPT = '''
set out to ""
set d0 to current date
set time of d0 to 0
set d1 to d0 + (2 * days)
tell application "Calendar"
  repeat with cal in calendars
    set calName to name of cal
    try
      set evs to (every event of cal whose start date ≥ d0 and start date < d1)
      repeat with ev in evs
        set sd to start date of ev
        set ed to end date of ev
        set out to out & calName & tab & (year of sd) & "-" & (month of sd as integer) & "-" & (day of sd) & tab & (hours of sd) & ":" & (minutes of sd) & tab & (hours of ed) & ":" & (minutes of ed) & tab & (allday event of ev) & tab & (summary of ev) & linefeed
      end repeat
    end try
  end repeat
end tell
return out
'''


@section("kalender")
def _kalender():
    r = subprocess.run(["osascript", "-e", KAL_SCRIPT],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200] or "osascript-Fehler")
    out = []
    for line in r.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 6:
            continue
        cal, d, s, e, allday, title = parts
        y, mo, dy = d.split("-")
        sh, sm = s.split(":")
        eh, em = e.split(":")
        if cal == "Feiertage in Deutschland":
            cal = "Feiertage"
        out.append({
            "d": f"{y}-{int(mo):02d}-{int(dy):02d}",
            "s": f"{int(sh):02d}:{int(sm):02d}",
            "e": f"{int(eh):02d}:{int(em):02d}",
            "allday": allday == "true",
            "cal": cal,
            "t": title.strip() or "(ohne Titel)",
        })
    # allday zuerst je Tag, dann Uhrzeit
    out.sort(key=lambda x: (x["d"], 0 if x["allday"] else 1, x["s"]))
    return out


# --- Projekte ---------------------------------------------------------------
@section("projekte")
def _projekte():
    out = []
    for f in sorted((VAULT / "02 Projekte").glob("*.md")):
        try:
            head = f.read_text(encoding="utf-8", errors="ignore")[:2000]
        except Exception:
            continue
        status = ""
        m = re.search(r"^status:\s*(.+)$", head, re.M)
        if m:
            status = m.group(1).strip().strip('"')
        out.append({
            "name": f.stem,
            "status": status or "unklar",
            "file": f"02 Projekte/{f.name}",
            "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
        })
    out.sort(key=lambda p: p["mtime"], reverse=True)
    return out


# --- Training (intervals.icu) ----------------------------------------------
@section("training")
def _training():
    from intervals_live import api_get, load_config

    conf = load_config()
    aid, key = conf["ATHLETE_ID"], conf["API_KEY"]
    newest = datetime.now().date()
    oldest = newest - timedelta(days=HEAT_DAYS)
    acts = api_get(f"/athlete/{aid}/activities?oldest={oldest}&newest={newest}", key)
    wellness = api_get(f"/athlete/{aid}/wellness?oldest={newest - timedelta(days=30)}&newest={newest}", key)

    ctl = atl = tsb = None
    for w in sorted(wellness, key=lambda x: x.get("id", ""), reverse=True):
        if w.get("ctl") is not None:
            ctl = round(w["ctl"], 1)
            if w.get("atl") is not None:
                atl = round(w["atl"], 1)
                tsb = round(ctl - atl, 1)
            break

    type_de = {"Run": "Lauf", "Ride": "Rad", "VirtualRide": "Rolle", "Swim": "Schwimmen",
               "WeightTraining": "Kraft", "Workout": "Athletik", "Walk": "Gehen",
               "Hike": "Wandern", "Transition": "Wechsel"}
    heat = {}
    weeks = {}
    recent = []
    for a in sorted(acts, key=lambda x: x.get("start_date_local", ""), reverse=True):
        d = (a.get("start_date_local") or "")[:10]
        if not d:
            continue
        sec = a.get("moving_time") or a.get("elapsed_time") or 0
        typ = type_de.get(a.get("type", ""), a.get("type", "?"))
        h, m = divmod(int(sec) // 60, 60)
        dur = f"{h}:{m:02d} h" if h else f"{m} min"
        entry = heat.setdefault(d, {"s": 0, "txt": []})
        entry["s"] += int(sec)
        entry["txt"].append(f"{typ} {dur}")
        iso = datetime.strptime(d, "%Y-%m-%d").isocalendar()
        wk = f"{iso[0]}-W{iso[1]:02d}"
        weeks[wk] = weeks.get(wk, 0) + sec
        if len(recent) < 6:
            recent.append({"d": d, "typ": typ, "name": a.get("name") or typ, "dur": dur,
                           "km": round((a.get("distance") or 0) / 1000, 1),
                           "load": int(a.get("icu_training_load") or 0)})
    week_list = [{"w": k, "h": round(v / 3600, 1)} for k, v in sorted(weeks.items())][-10:]
    return {"ctl": ctl, "atl": atl, "tsb": tsb, "heat": heat, "weeks": week_list, "recent": recent}


# --- Vault-Aktivität (Git) --------------------------------------------------
@section("vault")
def _vault():
    r = subprocess.run(
        ["git", "log", f"--since={HEAT_DAYS}.days", "--pretty=%ad", "--date=short"],
        cwd=VAULT, capture_output=True, text=True, timeout=30)
    commits = {}
    for line in r.stdout.split():
        commits[line] = commits.get(line, 0) + 1
    # Notizen, deren letzte Änderung auf den jeweiligen Tag fällt
    cutoff = datetime.now().timestamp() - HEAT_DAYS * 86400
    edits = {}
    skip = (".obsidian", ".git", ".trash", "Readwise")
    for f in VAULT.rglob("*.md"):
        if any(part in skip for part in f.parts):
            continue
        mt = f.stat().st_mtime
        if mt >= cutoff:
            d = datetime.fromtimestamp(mt).strftime("%Y-%m-%d")
            edits[d] = edits.get(d, 0) + 1
    heat = {}
    for d in set(commits) | set(edits):
        heat[d] = {"c": commits.get(d, 0), "e": edits.get(d, 0)}
    inbox = len(list((VAULT / "01 Inbox").glob("*.md")))
    dailies = sorted((VAULT / "05 Daily Notes").glob("????-??-??.md"))

    def sect(txt, name):
        m = re.search(rf"^## {name}\s*\n(.*?)(?=^## |\Z)", txt, re.M | re.S)
        items = re.findall(r"^- (.+)$", m.group(1), re.M) if m else []
        # Wikilinks/Markdown für die Anzeige entschärfen
        clean = []
        for it in items:
            it = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", it)
            it = re.sub(r"\[\[([^\]]+)\]\]", r"\1", it)
            it = it.replace("**", "").strip()
            if it:
                clean.append(it)
        return clean

    recent = []
    for f in dailies[-6:][::-1]:
        txt = f.read_text(encoding="utf-8", errors="ignore")
        recent.append({"d": f.stem, "offen": sect(txt, "Offen / Nächste Schritte")[:6],
                       "g": len(sect(txt, "Geschafft"))})

    # Offene Punkte der letzten ~3 Wochen einsammeln, Wiederholungen zusammenfassen
    def tokens(t):
        return set(re.findall(r"[a-zä-üß0-9]{3,}", t.lower()))

    def similar(a, b):
        inter = len(a & b)
        return inter and inter / len(a | b) >= 0.5

    merged = []
    done_later = []  # Geschafft-Einträge späterer Notes (wir laufen neueste → älteste)
    for f in dailies[-15:][::-1]:
        txt = f.read_text(encoding="utf-8", errors="ignore")
        for item in sect(txt, "Offen / Nächste Schritte"):
            tk = tokens(item)
            if not tk:
                continue
            if any(similar(tk, d) for d in done_later):
                continue  # wurde in einer späteren Note als geschafft notiert
            hit = next((m for m in merged if similar(tk, m["tk"])), None)
            if hit:
                hit["n"] += 1
                hit["first"] = f.stem
            else:
                merged.append({"t": item, "last": f.stem, "first": f.stem,
                               "n": 1, "tk": tk})
        for g in sect(txt, "Geschafft"):
            gt = tokens(g)
            if gt:
                done_later.append(gt)
    offen_alle = [{"t": m["t"][:180], "last": m["last"], "n": m["n"]}
                  for m in merged][:12]

    return {"heat": heat, "inbox": inbox, "nDailies": len(dailies),
            "lastDaily": dailies[-1].stem if dailies else None,
            "dailies": recent, "offenAlle": offen_alle,
            "offenTotal": len(merged)}


# --- PV-Anlage (Kostal) -----------------------------------------------------
@section("pv")
def _pv():
    import asyncio

    import aiohttp
    from kostal_live import KOSTAL_IP, KOSTAL_PASSWORD, get_val

    async def fetch_all():
        """Live-Werte und Statistik mit EINEM Login holen.

        Der Kostal sperrt den Benutzer nach zu vielen Anmeldungen in kurzer
        Zeit ("User is locked"). Deshalb eine Session für alle Module.
        """
        from pykoplenti import ApiClient
        async with aiohttp.ClientSession() as s:
            c = ApiClient(s, KOSTAL_IP)
            await c.login(key=KOSTAL_PASSWORD)
            head = {"authorization": f"Session {c.session_id}"}

            async def mod(path):
                async with s.get(
                    f"http://{KOSTAL_IP}/api/v1/processdata/{path}", headers=head
                ) as r:
                    return (await r.json())[0]["processdata"]

            loc = await mod("devices:local")
            bat = await mod("devices:local:battery")
            pv1 = await mod("devices:local:pv1")
            pv2 = await mod("devices:local:pv2")
            meter = await mod("devices:local:powermeter")
            stat = await mod("scb:statistic:EnergyFlow")

            live = {
                "pv_total_w": round((get_val(pv1, "P") or 0) + (get_val(pv2, "P") or 0), 1),
                "home_p_w": get_val(loc, "Home_P"),
                "bat_soc_pct": get_val(bat, "SoC", 0),
                "bat_p_w": get_val(bat, "P"),
                "grid_p_w": get_val(loc, "Grid_P"),
                "export_kwh": round((get_val(meter, "Exp_E") or 0) / 1000, 2),
            }
            return live, {d["id"]: d["value"] for d in stat}

    k, st = asyncio.run(asyncio.wait_for(fetch_all(), timeout=30))

    g = lambda key: (st.get(key) or 0) / 1000  # Wh → kWh

    heute = {
        "prod": round(g("Statistic:Yield:Day"), 1),
        "verbrauch": round(g("Statistic:EnergyHome:Day"), 1),
        "netzbezug": round(g("Statistic:EnergyHomeGrid:Day"), 1),
        "einspeisung": round(max(0, g("Statistic:Yield:Day") - g("Statistic:EnergyHomePv:Day")
                                 - g("Statistic:EnergyChargePv:Day")), 1),
        "eigen": round(g("Statistic:EnergyHomePv:Day") + g("Statistic:EnergyHomeBat:Day"), 1),
        "autark": round(st.get("Statistic:Autarky:Day") or 0),
    }

    # Vortags-Bilanz: Differenz der Gesamtzähler zwischen dem jeweils ersten
    # Lauf des Tages (normalerweise 6:30) – ergibt ein sauberes 24-h-Fenster.
    hist_f = VAULT / ".scripts" / "pv_history.json"
    hist = json.loads(hist_f.read_text()) if hist_f.exists() else {}
    today = datetime.now().strftime("%Y-%m-%d")
    totals = {"prod": g("Statistic:Yield:Total"),
              "verbrauch": g("Statistic:EnergyHome:Total"),
              "einspeisung": max(0, g("Statistic:Yield:Total") - g("Statistic:EnergyHomePv:Total")
                                 - g("Statistic:EnergyChargePv:Total")),
              "netzbezug": g("Statistic:EnergyHomeGrid:Total"),
              "eigen": g("Statistic:EnergyHomePv:Total") + g("Statistic:EnergyHomeBat:Total")}
    if today not in hist:
        hist[today] = totals
        for d in sorted(hist)[:-40]:
            del hist[d]
        hist_f.write_text(json.dumps(hist))
    prev_days = sorted(d for d in hist if d < today)
    gestern = None
    if prev_days:
        base, ref = hist[prev_days[-1]], hist[today]
        gestern = {kk: round(ref[kk] - base.get(kk, ref[kk]), 1) for kk in totals}
        if gestern["verbrauch"] > 0:
            gestern["autark"] = round(100 * (1 - gestern["netzbezug"] / gestern["verbrauch"]))

    # Ersparnis nur mit von Oskar bestätigten Preisen (.scripts/pv_preise.json)
    preise_f = VAULT / ".scripts" / "pv_preise.json"
    preise = json.loads(preise_f.read_text()) if preise_f.exists() else None

    def spar(x):
        if not (preise and x):
            return None
        return round((x["eigen"] * preise["strompreis_ct"]
                      + x["einspeisung"] * preise["verguetung_ct"]) / 100, 2)

    return {"pv_w": k["pv_total_w"], "home_w": k["home_p_w"], "soc": k["bat_soc_pct"],
            "grid_w": k["grid_p_w"], "bat_w": k["bat_p_w"], "export_kwh": k["export_kwh"],
            "heute": heute, "gestern": gestern,
            "sparHeute": spar(heute), "sparGestern": spar(gestern)}


# --- Lesen (aus Lese-Dashboard.html) ---------------------------------------
@section("lesen")
def _lesen():
    src = (VAULT / "04 Ressourcen" / "Lese-Dashboard.html").read_text(encoding="utf-8")
    pat = re.compile(r'\{\s*t:\s*"([^"]+)",\s*a:\s*"([^"]+)",\s*pct:\s*(\d+|null),\s*d:\s*"([^"]+)"(?:,\s*asin:\s*(?:"([^"]+)"|null))?')
    books = []
    for m in pat.finditer(src):
        pct = None if m.group(3) == "null" else int(m.group(3))
        books.append({"t": m.group(1), "a": m.group(2), "pct": pct,
                      "d": m.group(4), "asin": m.group(5)})
    if not books:
        raise RuntimeError("keine Bücher im Lese-Dashboard gefunden")
    return books[:10]


# --- Schule (iCloud + Dashboards) ------------------------------------------
@section("schule")
def _schule():
    faecher, schuljahre = [], []
    if ICLOUD_GDRS.exists():
        for d in sorted(ICLOUD_GDRS.iterdir()):
            if not d.is_dir():
                continue
            if d.name in ("Mathematik", "Physik", "Sport", "Informatik"):
                n = sum(1 for _ in d.iterdir())
                faecher.append({"name": d.name, "n": n})
            elif d.name.startswith("Schuljahr"):
                schuljahre.append(d.name)
    links = [
        {"label": "Unterrichtsmaterial-Dashboard", "href": "Dashboard.html"},
        {"label": "Notenschlüsselrechner", "href": "Notenschlüsselrechner/Notenschlüsselrechner.html"},
        {"label": "Notenschlüssel Realschulprüfung", "href": "Notenschlüsselrechner/Notenschlüssel Realschulprüfung BW.html"},
    ]
    noten = ICLOUD_GDRS / "Noten-Dashboard.html"
    if noten.exists():
        links.append({"label": "Noten-Dashboard (iCloud)", "href": noten.as_uri()})
    return {"faecher": faecher, "schuljahre": schuljahre, "links": links,
            "icloud": str(ICLOUD_GDRS)}


# --- Wissenskarte mit aktualisieren ----------------------------------------
@section("wissenskarte")
def _wissenskarte():
    r = subprocess.run(
        [sys.executable, str(VAULT / ".scripts" / "wissenskarte_build.py")],
        capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200] or "Build-Fehler")
    return r.stdout.strip()


payload = "window.LEBEN = " + json.dumps(data, ensure_ascii=False) + ";\n"
OUT.write_text(payload, encoding="utf-8")
print(f"→ {OUT.name} geschrieben ({len(payload) // 1024} kB), "
      f"{len(data['errors'])} Fehlerquellen" if data["errors"] else
      f"→ {OUT.name} geschrieben ({len(payload) // 1024} kB), alle Quellen ok")
