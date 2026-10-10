"""
Ernährungs-Tracker: Daten pflegen, Garmin-Aktivität (intervals.icu) holen, Rest-Budget anzeigen.

Daten:   04 Ressourcen/Ernährung/ernaehrung_data.js  (wird vom Tracker-HTML gelesen)

Verwendung (Claude trägt nach Foto-Schätzung ein):
    python3 .scripts/ernaehrung.py add "Skyr mit Beeren" 280 --p 30 [--time 08:15] [--date 2026-10-11]
    python3 .scripts/ernaehrung.py day --weight 78.2 --waist 86.5 --sweets nein --mood 3 --note "..." [--date ...]
    python3 .scripts/ernaehrung.py slip "Auslöser/Situation" [--kcal 1500]   # Rückfall-Protokoll
    python3 .scripts/ernaehrung.py fav "Kurzname" kcal --p g --note "Beschreibung"   # Favorit speichern
    python3 .scripts/ernaehrung.py use "Kurzname" [--time ..] [--date ..]            # Favorit eintragen
    python3 .scripts/ernaehrung.py del <nummer> [--date ...]                  # Mahlzeit löschen
    python3 .scripts/ernaehrung.py refresh [tage]                             # Schritte + Training holen
    python3 .scripts/ernaehrung.py status [--date ...]                        # Rest-Budget im Terminal

Für refresh immer /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 nutzen.
"""
import sys, json, argparse
from datetime import date, datetime, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
DATA = VAULT / "04 Ressourcen" / "Ernährung" / "ernaehrung_data.js"
PREFIX = "window.ERN_DATA = "

DEFAULT = {
    "settings": {
        "height_cm": 181, "age": 41, "sex": "m",
        "start_weight": 78.5, "start_date": "2026-10-10",
        "goal_weight": 74.5, "goal_low": 74.0, "goal_high": 75.0, "goal_date": "2026-11-30",
        "long_term": [73.0, 74.0],
        "activity_factor": 1.3,     # Alltag (Lehrer, Kinder, Schritte), ohne Training
        "training_factor": 0.8,     # Garmin-kcal enthalten den Grundumsatz-Anteil mit
        "deficit": 450,             # kcal pro Tag
        "protein_per_kg": 1.8,
        "carry_cap": 300,           # max. Ausgleich pro Tag
        "min_kcal": 1500,           # Tagesbudget fällt nie darunter
        "favorites": {},
    },
    "days": {},
    "slips": [],
}


def load():
    if not DATA.exists():
        return json.loads(json.dumps(DEFAULT))
    txt = DATA.read_text(encoding="utf-8").strip()
    return json.loads(txt[len(PREFIX):].rstrip(";"))


def save(d):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    d["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    DATA.write_text(PREFIX + json.dumps(d, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")


def bmr(s, weight):
    # Mifflin-St Jeor
    return 10 * weight + 6.25 * s["height_cm"] - 5 * s["age"] + (5 if s["sex"] == "m" else -161)


def day_of(d, key):
    return d["days"].setdefault(key, {"meals": []})


def current_weight(d, key):
    ws = sorted((k, v["weight"]) for k, v in d["days"].items() if v.get("weight") and k <= key)
    return ws[-1][1] if ws else d["settings"]["start_weight"]


def budget(d, key):
    s = d["settings"]
    day = d["days"].get(key, {})
    w = current_weight(d, key)
    base = round(bmr(s, w) * s["activity_factor"])
    train = round(day.get("training_kcal", 0) * s["training_factor"])
    raw = base + train - s["deficit"]
    # Ausgleich: Überschuss der letzten 7 Tage (nur Tage mit Einträgen), verteilt auf 7 Tage, gedeckelt
    over = 0
    for i in range(1, 8):
        k = (date.fromisoformat(key) - timedelta(days=i)).isoformat()
        e = sum(m["kcal"] for m in d["days"].get(k, {}).get("meals", []))
        if e:
            bk = _raw(d, k)
            over += e - bk
    adj = max(0, min(s.get("carry_cap", 300), round(over / 7)))
    adj = max(0, min(adj, raw - s.get("min_kcal", 1500)))
    return {"bmr": round(bmr(s, w)), "base": base, "train": train, "adj": adj, "budget": raw - adj}


def _raw(d, k):
    s = d["settings"]
    w = current_weight(d, k)
    return round(bmr(s, w) * s["activity_factor"]) + round(d["days"].get(k, {}).get("training_kcal", 0) * s["training_factor"]) - s["deficit"]


def status(d, key):
    day = d["days"].get(key, {"meals": []})
    b = budget(d, key)
    eaten = sum(m["kcal"] for m in day["meals"])
    prot = sum(m.get("p", 0) for m in day["meals"])
    print(f"{key}  Budget {b['budget']} kcal (Basis {b['base']} + Training {b['train']} − Defizit {d['settings']['deficit']}" + (f", Ausgleich −{b['adj']}" if b['adj'] else "") + ")")
    print(f"gegessen {eaten} kcal | übrig {b['budget'] - eaten} kcal | Eiweiß {prot} g von ~{round(current_weight(d, key) * d['settings']['protein_per_kg'])} g")
    for i, m in enumerate(day["meals"], 1):
        print(f"  {i}. {m.get('time', '')} {m['name']} – {m['kcal']} kcal" + (f", {m['p']} g Eiweiß" if m.get("p") else ""))


def refresh(d, days):
    sys.path.insert(0, str(VAULT / ".scripts"))
    import intervals_live as I
    c = I.load_config()
    oldest = (date.today() - timedelta(days=days)).isoformat()
    newest = date.today().isoformat()
    wel = I.api_get(f"/athlete/{c['ATHLETE_ID']}/wellness?oldest={oldest}&newest={newest}", c["API_KEY"])
    act = I.api_get(f"/athlete/{c['ATHLETE_ID']}/activities?oldest={oldest}&newest={newest}", c["API_KEY"])
    for w in wel:
        if w.get("steps") is not None:
            day_of(d, w["id"])["steps"] = w["steps"]
    train, sess = {}, {}
    for a in act:
        k = a["start_date_local"][:10]
        train[k] = train.get(k, 0) + (a.get("calories") or 0)
        sess.setdefault(k, []).append(f"{a.get('type', '?')} {round((a.get('moving_time') or 0) / 60)} min")
    for k in set(train) | {w["id"] for w in wel}:
        day = day_of(d, k)
        day["training_kcal"] = train.get(k, 0)
        day["sessions"] = sess.get(k, [])
    print(f"Aktivität aktualisiert ({oldest} bis {newest}).")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd")
    p.add_argument("arg", nargs="?")
    p.add_argument("kcal", nargs="?", type=int)
    p.add_argument("--p", type=int)
    p.add_argument("--time")
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--weight", type=float)
    p.add_argument("--waist", type=float)
    p.add_argument("--sweets")
    p.add_argument("--mood", type=int)
    p.add_argument("--note")
    p.add_argument("--kcal", dest="kcal_opt", type=int)
    a = p.parse_args()
    d = load()

    if a.cmd == "add":
        m = {"time": a.time or datetime.now().strftime("%H:%M"), "name": a.arg, "kcal": a.kcal}
        if a.p is not None:
            m["p"] = a.p
        day_of(d, a.date)["meals"].append(m)
    elif a.cmd == "fav":
        d["settings"].setdefault("favorites", {})[a.arg] = {"name": a.note or a.arg, "kcal": a.kcal, "p": a.p or 0}
    elif a.cmd == "use":
        f = d["settings"]["favorites"][a.arg]
        m = {"time": a.time or datetime.now().strftime("%H:%M"), "name": f["name"], "kcal": f["kcal"]}
        if f.get("p"):
            m["p"] = f["p"]
        day_of(d, a.date)["meals"].append(m)
    elif a.cmd == "del":
        day_of(d, a.date)["meals"].pop(int(a.arg) - 1)
    elif a.cmd == "day":
        day = day_of(d, a.date)
        if a.weight:
            day["weight"] = a.weight
        if a.waist:
            day["waist"] = a.waist
        if a.sweets:
            day["sweets"] = a.sweets
        if a.mood:
            day["mood"] = a.mood
        if a.note:
            day["note"] = a.note
    elif a.cmd == "slip":
        d["slips"].append({"date": a.date, "trigger": a.arg, "kcal": a.kcal_opt})
        day_of(d, a.date)["sweets"] = "ja"
    elif a.cmd == "refresh":
        refresh(d, int(a.arg or 14))
    elif a.cmd != "status":
        sys.exit(__doc__)

    save(d)
    status(d, a.date)


if __name__ == "__main__":
    main()
