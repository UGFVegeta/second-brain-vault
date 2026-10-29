#!/usr/bin/env python3
"""Kleiner lokaler Dienst für das Lebens-Dashboard (nur 127.0.0.1).

Das Dashboard ist eine statische HTML und darf nichts schreiben. Dieser Dienst
nimmt die Klicks an, die etwas ändern müssen. Aktuell:

  GET  /ping       -> {"ok": true}
  POST /erledigt   -> {"liste": "...", "t": "..."}  hakt die Erinnerung in Apple Erinnerungen ab
  GET  /fokus      -> Fokus-Minuten heute, diese Woche und pro Projekt (aus den Daily Notes)
  GET  /abend      -> heutiger Eintrag im Gesundheitslogbuch (Befinden, Training)
  POST /abend      -> {"befinden": 1-5, "training": "..."}  trägt Befinden und Training für heute ein
  POST /erfassen   -> {"text": "...", "ziel": "inbox" | "erinnerung"}  Schnellerfassung
  GET  /tagesblatt -> Arbeitstermine heute und morgen, To-dos (Liste Schule) für die Prüfung vor dem Druck
  POST /tagesblatt -> {"termine": [...], "todos": [...]}  baut das Tagesblatt-PDF mit Ergänzungen und öffnet es
  POST /fokus      -> {"projekt": "...", "start": <ms>, "minuten": n}  schreibt eine Zeile in die heutige Daily Note

Nur Anfragen von file:// (Origin "null") oder ohne Origin werden bedient, damit
keine fremde Webseite im Browser Erinnerungen abhaken kann.

Start: python3 .scripts/dashboard_server.py   (Port 8765)
"""
import json
import subprocess
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import fokus_lib
import tagesblatt
import logbuch_lib

HOST, PORT = "127.0.0.1", 8765

# Kalender und Erinnerungen brauchen mehrere Sekunden; die Vorschau merkt sich den Stand.
_BLATT = {"tag": None, "zeit": None, "kal": {}, "ht": [], "mt": []}


def _blatt_laden(neu=False):
    heute = datetime.now().date()
    alt = _BLATT["zeit"] is None or _BLATT["tag"] != heute or (datetime.now() - _BLATT["zeit"]).seconds > 900
    if neu or alt:
        kal = tagesblatt.kalender(heute)
        ht, mt = tagesblatt.todos(heute)
        _BLATT.update(tag=heute, zeit=datetime.now(), kal=kal, ht=ht, mt=mt)
    return _BLATT


def _blatt_vorschau():
    b = _blatt_laden()
    tag = b["tag"]
    morgen = tagesblatt.naechster_arbeitstag(tag)
    fmt = lambda t: [{"s": x["s"], "t": x["t"]} for x in tagesblatt.tagesliste(t, b["kal"])]
    return {"heute": {"datum": tag.isoformat(), "titel": tagesblatt.titel(tag), "termine": fmt(tag)},
            "morgen": {"datum": morgen.isoformat(), "titel": tagesblatt.titel(morgen), "termine": fmt(morgen)},
            "todos_heute": b["ht"], "todos_morgen": b["mt"]}

NEUE_ERINNERUNG_SCRIPT = '''
on run argv
  tell application "Reminders"
    make new reminder at end of list "Inbox" with properties {name:(item 1 of argv)}
    return "ok"
  end tell
end run
'''

ERLEDIGT_SCRIPT = '''
on run argv
  set listName to item 1 of argv
  set remName to item 2 of argv
  tell application "Reminders"
    set hits to (reminders of list listName whose name is remName and completed is false)
    if (count of hits) is 0 then return "nicht gefunden"
    set completed of item 1 of hits to true
    return "ok"
  end tell
end run
'''


class Handler(BaseHTTPRequestHandler):
    def _origin_ok(self):
        return self.headers.get("Origin") in (None, "null")

    def _send(self, code, body):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        if self.headers.get("Origin") == "null":
            self.send_header("Access-Control-Allow-Origin", "null")
            self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        if not self._origin_ok():
            return self._send(403, {"ok": False, "fehler": "Origin nicht erlaubt"})
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "null")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.end_headers()

    def do_GET(self):
        if not self._origin_ok():
            return self._send(403, {"ok": False, "fehler": "Origin nicht erlaubt"})
        if self.path == "/ping":
            return self._send(200, {"ok": True})
        if self.path == "/fokus":
            return self._send(200, {"ok": True, **fokus_lib.auswerten()})
        if self.path == "/abend":
            return self._send(200, {"ok": True, "heute": logbuch_lib.heute_zeile()})
        if self.path.split("?")[0] == "/tagesblatt":
            try:
                if "neu=1" in self.path:
                    _blatt_laden(neu=True)
                return self._send(200, {"ok": True, **_blatt_vorschau()})
            except Exception as e:
                return self._send(500, {"ok": False, "fehler": str(e)[:200]})
        self._send(404, {"ok": False})

    def do_POST(self):
        if not self._origin_ok():
            return self._send(403, {"ok": False, "fehler": "Origin nicht erlaubt"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"ok": False, "fehler": "kein JSON"})
        if self.path == "/tagesblatt":
            try:
                b = _blatt_laden()
                termine = [str(x) for x in body.get("termine", [])][:20]
                extra = [str(x) for x in body.get("todos", [])][:10]
                pfad = tagesblatt.erzeugen(b["tag"], b["kal"], b["ht"], b["mt"], termine, extra)
                subprocess.run(["open", pfad], timeout=30)
            except Exception as e:
                return self._send(500, {"ok": False, "fehler": str(e)[:200]})
            return self._send(200, {"ok": True, "pfad": pfad})
        if self.path == "/abend":
            try:
                zeile = logbuch_lib.setzen(int(body["befinden"]), str(body["training"]))
            except (KeyError, TypeError, ValueError) as e:
                return self._send(400, {"ok": False, "fehler": str(e)[:120]})
            return self._send(200, {"ok": True, "heute": zeile})
        if self.path == "/erfassen":
            text, ziel = body.get("text"), body.get("ziel")
            if not isinstance(text, str) or not " ".join(text.split()):
                return self._send(400, {"ok": False, "fehler": "Text fehlt"})
            text = " ".join(text.split())[:500]
            if ziel == "inbox":
                logbuch_lib.erfassen_inbox(text)
            elif ziel == "erinnerung":
                r = subprocess.run(["osascript", "-e", NEUE_ERINNERUNG_SCRIPT, text],
                                   capture_output=True, text=True, timeout=60)
                if r.returncode != 0:
                    return self._send(500, {"ok": False, "fehler": r.stderr.strip()[:200]})
            else:
                return self._send(400, {"ok": False, "fehler": "ziel unbekannt"})
            return self._send(200, {"ok": True})
        if self.path == "/fokus":
            try:
                start = datetime.fromtimestamp(float(body["start"]) / 1000)
                minuten = int(body["minuten"])
                zeile = fokus_lib.eintragen(str(body["projekt"]), start, start + timedelta(minutes=minuten), minuten)
            except (KeyError, TypeError, ValueError) as e:
                return self._send(400, {"ok": False, "fehler": str(e)[:120]})
            return self._send(200, {"ok": True, "zeile": zeile, **fokus_lib.auswerten()})
        if self.path != "/erledigt":
            return self._send(404, {"ok": False})
        liste, t = body.get("liste"), body.get("t")
        if not isinstance(liste, str) or not isinstance(t, str) or not liste or not t:
            return self._send(400, {"ok": False, "fehler": "liste und t fehlen"})
        r = subprocess.run(["osascript", "-e", ERLEDIGT_SCRIPT, liste, t],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            return self._send(500, {"ok": False, "fehler": r.stderr.strip()[:200]})
        out = r.stdout.strip()
        self._send(200 if out == "ok" else 404, {"ok": out == "ok", "fehler": None if out == "ok" else out})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"Dashboard-Dienst auf http://{HOST}:{PORT} (Strg+C beendet)")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
