"""
TrainingPeaks-Virtual-Rollenfahrten -> intervals.icu hochladen

Hintergrund: TP-Virtual-Fahrten gehen nie zu Garmin und sind über Strava an der
intervals.icu-API gesperrt. TP Virtual legt die Fahrten aber lokal als .fit ab:
    ~/TPVirtual/<USERID>/FITFiles/*.fit
Dieses Skript lädt neue .fit-Dateien direkt per API hoch (source: UPLOAD, volle
Wattdaten) und merkt sich in einer State-Datei, was schon erledigt ist.

Verwendung:
    python3 .scripts/intervals_tpv_upload.py          # neue Fahrten hochladen
    python3 .scripts/intervals_tpv_upload.py --dry     # nur zeigen, was neu wäre

Zugangsdaten: ~/.config/claude-intervals/intervals.env (ATHLETE_ID, API_KEY)
"""

import os
import sys
import glob
import time
import uuid
import base64
import urllib.request
import urllib.error
from pathlib import Path

FIT_GLOB = os.path.expanduser("~/TPVirtual/*/FITFiles/*.fit")
_cfg = Path.home() / ".config" / "claude-intervals" / "intervals.env"
_state = Path.home() / ".config" / "claude-intervals" / "tpv_uploaded.txt"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def load_config():
    if not _cfg.exists():
        sys.exit(f"Konfig fehlt: {_cfg}")
    conf = {}
    for line in _cfg.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            conf[k.strip()] = v.strip()
    if not conf.get("ATHLETE_ID") or not conf.get("API_KEY"):
        sys.exit("ATHLETE_ID oder API_KEY fehlt in der Konfig.")
    return conf


def already_done():
    if not _state.exists():
        return set()
    return {l.strip() for l in _state.read_text().splitlines() if l.strip()}


def mark_done(name):
    with _state.open("a") as f:
        f.write(name + "\n")


def upload(path, aid, key):
    data = open(path, "rb").read()
    fn = os.path.basename(path)
    token = base64.b64encode(f"API_KEY:{key}".encode()).decode()
    b = "----tpv" + uuid.uuid4().hex
    parts = [
        f'--{b}\r\nContent-Disposition: form-data; name="name"\r\n\r\nTP Virtual Rolle\r\n'.encode(),
        f'--{b}\r\nContent-Disposition: form-data; name="external_id"\r\n\r\n{fn}\r\n'.encode(),
        f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{fn}"\r\n'
        f'Content-Type: application/octet-stream\r\n\r\n'.encode(),
        data,
        f"\r\n--{b}--\r\n".encode(),
    ]
    req = urllib.request.Request(
        f"https://intervals.icu/api/v1/athlete/{aid}/activities",
        data=b"".join(parts),
        method="POST",
        headers={
            "Authorization": f"Basic {token}",
            "User-Agent": USER_AGENT,
            "Content-Type": f"multipart/form-data; boundary={b}",
        },
    )
    try:
        r = urllib.request.urlopen(req, timeout=90)
        return r.status, None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]


def main():
    dry = "--dry" in sys.argv
    conf = load_config()
    aid, key = conf["ATHLETE_ID"], conf["API_KEY"]

    files = sorted(glob.glob(FIT_GLOB))
    if not files:
        sys.exit(f"Keine .fit-Dateien gefunden unter {FIT_GLOB}")
    done = already_done()
    todo = [f for f in files if os.path.basename(f) not in done]

    print(f"TP-Virtual-Dateien gesamt: {len(files)}  |  schon hochgeladen: {len(done)}  |  neu: {len(todo)}")
    if not todo:
        print("Nichts Neues – alles aktuell. ✅")
        return
    if dry:
        for f in todo:
            print("  NEU:", os.path.basename(f))
        print("(Trockenlauf – nichts hochgeladen.)")
        return

    ok = fail = 0
    for f in todo:
        fn = os.path.basename(f)
        status, err = upload(f, aid, key)
        if status in (200, 201):
            mark_done(fn)
            ok += 1
            print(f"  ✅ {fn}")
        elif status == 429:
            print("  ⏳ Rate-Limit – warte 30s …")
            time.sleep(30)
            status, err = upload(f, aid, key)
            if status in (200, 201):
                mark_done(fn)
                ok += 1
                print(f"  ✅ {fn} (2. Versuch)")
            else:
                fail += 1
                print(f"  ❌ {fn}: HTTP {status} {err}")
        else:
            fail += 1
            print(f"  ❌ {fn}: HTTP {status} {err}")
        time.sleep(0.6)  # API schonen

    print(f"\nFertig: {ok} hochgeladen, {fail} Fehler.")


if __name__ == "__main__":
    main()
