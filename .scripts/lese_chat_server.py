#!/usr/bin/env python3
"""Lokale Brücke zwischen Lese-Bibliothek.html und Claude Code.

Nimmt Chat-Fragen zu Büchern entgegen und beantwortet sie per `claude -p`
im Vault (Zugriff auf Readwise-Highlights und Buchnotizen, nur lesend).
Läuft ausschließlich auf 127.0.0.1 – nichts verlässt den Rechner außer
dem Claude-API-Aufruf selbst.

Start:  python3 .scripts/lese_chat_server.py   (oder Doppelklick auf
        "04 Ressourcen/Buch-Chat starten.command")
"""
import json
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VAULT = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude"
PORT = 8744
MODEL = "sonnet"
TIMEOUT = 240

# Erlaubte Aufrufer: lokale Dashboard-Seiten (file:// meldet Origin "null")
ALLOWED_ORIGINS = ("null", "http://localhost:8743", "http://127.0.0.1:8743")

# Buch-Titel -> Claude-Session-ID, damit Folgefragen im Kontext bleiben
sessions = {}

PROMPT = """Du bist der Buch-Chat von Oskars Lese-Dashboard. Frage zum Buch: "{book}".

Suche zuerst nach Oskars eigenen Notizen zu diesem Buch:
- Readwise/Books/ (Kindle-Highlights)
- 04 Ressourcen/Bücher & Learnings/ (verarbeitete Notizen)

Beantworte die Frage auf Deutsch, knapp und konkret. Stütze dich bevorzugt auf
seine Notizen und zitiere daraus, wenn es passt. Gibt es keine Notizen zum Buch,
sag das in einem Halbsatz und antworte aus deinem allgemeinen Wissen über das Buch.

Frage: {q}"""


def ask_claude(book: str, question: str) -> str:
    cmd = ["claude", "-p", "--model", MODEL, "--output-format", "json",
           "--allowedTools", "Read,Grep,Glob"]
    if book in sessions:
        cmd += ["--resume", sessions[book]]
        prompt = question  # Kontext steckt schon in der Session
    else:
        prompt = PROMPT.format(book=book, q=question)
    r = subprocess.run(cmd, cwd=VAULT, input=prompt, capture_output=True, text=True, timeout=TIMEOUT)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:300] or "claude-CLI-Fehler")
    data = json.loads(r.stdout)
    if data.get("session_id"):
        sessions[book] = data["session_id"]
    return data.get("result", "(keine Antwort)")


class Handler(BaseHTTPRequestHandler):
    def _origin(self):
        o = self.headers.get("Origin")
        if o is None or o in ALLOWED_ORIGINS:
            return o or "*"
        return None

    def _send(self, code, payload, origin):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        origin = self._origin()
        self.send_response(204 if origin else 403)
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        origin = self._origin()
        if not origin:
            return self._send(403, {"error": "Origin nicht erlaubt"}, "null")
        if self.path == "/ping":
            return self._send(200, {"ok": True}, origin)
        self._send(404, {"error": "unbekannter Pfad"}, origin)

    def do_POST(self):
        origin = self._origin()
        if not origin:
            return self._send(403, {"error": "Origin nicht erlaubt"}, "null")
        if self.path != "/chat":
            return self._send(404, {"error": "unbekannter Pfad"}, origin)
        try:
            length = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(length))
            book = str(req.get("book", ""))[:200]
            q = str(req.get("q", ""))[:2000]
            if not book or not q:
                return self._send(400, {"error": "book und q erforderlich"}, origin)
            answer = ask_claude(book, q)
            self._send(200, {"answer": answer}, origin)
        except subprocess.TimeoutExpired:
            self._send(504, {"error": "Claude hat zu lange gebraucht – nochmal versuchen."}, origin)
        except Exception as e:
            self._send(500, {"error": str(e)[:300]}, origin)

    def log_message(self, fmt, *args):
        print("[buch-chat]", fmt % args)


if __name__ == "__main__":
    print(f"Buch-Chat-Brücke läuft auf http://127.0.0.1:{PORT} (Beenden: Ctrl+C)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
