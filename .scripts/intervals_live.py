"""
intervals.icu – Trainingsdaten Abruf
Quelle: Garmin (direkt) + Strava (für TrainingPeaks-Virtual-Rollenfahrten)

Verwendung:
    python3 .scripts/intervals_live.py            # letzte 21 Tage
    python3 .scripts/intervals_live.py 60         # letzte 60 Tage

Zugangsdaten außerhalb des Vaults (nicht in iCloud):
    ~/.config/claude-intervals/intervals.env
    Inhalt (zwei Zeilen):
        ATHLETE_ID=i123456
        API_KEY=xxxxxxxxxxxxxxxx
"""

import sys
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

API_BASE = "https://intervals.icu/api/v1"
# Cloudflare blockt den Default-User-Agent von urllib (Fehler 1010) -> Browser-UA
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# --- Zugangsdaten laden -----------------------------------------------------
_cfg = Path.home() / ".config" / "claude-intervals" / "intervals.env"


def load_config():
    if not _cfg.exists():
        sys.exit(
            f"Konfig fehlt: {_cfg}\n"
            "Bitte anlegen mit ATHLETE_ID=... und API_KEY=... (siehe Skript-Kopf)."
        )
    conf = {}
    for line in _cfg.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        conf[k.strip()] = v.strip()
    if not conf.get("ATHLETE_ID") or not conf.get("API_KEY"):
        sys.exit("ATHLETE_ID oder API_KEY fehlt in der Konfig.")
    return conf


def api_get(path, api_key):
    # intervals.icu: HTTP Basic, Nutzername ist literal "API_KEY"
    token = base64.b64encode(f"API_KEY:{api_key}".encode()).decode()
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Basic {token}", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"API-Fehler {e.code}: {e.reason} bei {path}")
    except urllib.error.URLError as e:
        sys.exit(f"Verbindungsfehler: {e.reason}")


# --- Aufbereitung -----------------------------------------------------------
def fmt_dur(seconds):
    if not seconds:
        return "–"
    h, rem = divmod(int(seconds), 3600)
    m = rem // 60
    return f"{h}:{m:02d}h" if h else f"{m}min"


def fmt_dist(meters):
    if not meters:
        return ""
    km = meters / 1000
    return f"{km:.1f} km" if km >= 1 else f"{int(meters)} m"


TYPE_ICON = {
    "Run": "🏃", "Ride": "🚴", "VirtualRide": "🎮🚴", "Swim": "🏊",
    "WeightTraining": "🏋️", "Workout": "💪", "Walk": "🚶", "Hike": "🥾",
    "Transition": "🔄",
}


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    conf = load_config()
    aid, key = conf["ATHLETE_ID"], conf["API_KEY"]

    newest = datetime.now().date()
    oldest = newest - timedelta(days=days)
    o, n = oldest.isoformat(), newest.isoformat()

    activities = api_get(f"/athlete/{aid}/activities?oldest={o}&newest={n}", key)
    wellness = api_get(f"/athlete/{aid}/wellness?oldest={o}&newest={n}", key)

    # Aktuellste Fitness/Fatigue/Form
    ctl = atl = form = None
    for w in sorted(wellness, key=lambda x: x.get("id", ""), reverse=True):
        if w.get("ctl") is not None:
            ctl = w["ctl"]
            atl = w.get("atl")
            if ctl is not None and atl is not None:
                form = ctl - atl
            break

    print("=" * 52)
    print(f"  🏊🚴🏃 intervals.icu  –  letzte {days} Tage")
    print("=" * 52)

    if ctl is not None:
        print("\n📊 Trainingsform (aktuell)")
        print(f"  Fitness (CTL):   {ctl:.1f}")
        print(f"  Fatigue (ATL):   {atl:.1f}" if atl is not None else "  Fatigue (ATL):   –")
        if form is not None:
            zone = "frisch" if form > 5 else ("müde" if form < -15 else "neutral")
            print(f"  Form (TSB):      {form:+.1f}  ({zone})")

    # Aktivitäten
    total_load = sum((a.get("icu_training_load") or 0) for a in activities)
    print(f"\n🗓️  Einheiten: {len(activities)}   |   Load Σ: {int(total_load)} TSS\n")

    for a in sorted(activities, key=lambda x: x.get("start_date_local", ""), reverse=True):
        date = (a.get("start_date_local") or "")[:10]
        icon = TYPE_ICON.get(a.get("type", ""), "•")
        name = a.get("name") or a.get("type") or "Training"
        dur = fmt_dur(a.get("moving_time") or a.get("elapsed_time"))
        dist = fmt_dist(a.get("distance"))
        load = a.get("icu_training_load")
        parts = [p for p in (dur, dist) if p]
        if load:
            parts.append(f"{int(load)} TSS")
        detail = "  ·  ".join(parts)
        print(f"  {date}  {icon}  {name}")
        if detail:
            print(f"              {detail}")

    print("=" * 52)


if __name__ == "__main__":
    main()
