#!/usr/bin/env python3
"""Active-Recall-Server: liefert die App aus und holt Feedback über die Claude-CLI.

Start:  python3 server.py
Danach: http://localhost:8744/App/   (Chrome)

Voraussetzung fürs Feedback: einmal `claude setup-token` im Terminal ausgeführt.
"""
import json
import os
import shutil
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent          # Ordner "Active Recall"
PORT = 8744
CLAUDE = shutil.which("claude")
NEUTRAL_CWD = tempfile.mkdtemp(prefix="active-recall-")

CTYPES = {
    ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml", ".pdf": "application/pdf",
}

PROMPT = """Du bist die Feedback-Instanz für ein Active-Recall-Lernsystem. Ein Lernender hat einen Text gelesen, die Quelle geschlossen und aus dem Kopf aufgeschrieben, was hängengeblieben ist. Bewerte diesen freien Abruf gegen die Referenz.

Es geht NICHT um Vollständigkeit oder wörtliche Wiedergabe, sondern um die zentralen Aussagen und ihre Zusammenhänge (aktives Erinnern, Testing-Effekt).

## Referenz (die Quelle)
{referenz}

## Freier Abruf des Lernenden
Selbsteinschätzung vor dem Abgleich: "{selbst}"

{abruf}

## Deine Aufgabe
Schreib das Feedback exakt in dieser Struktur, als Markdown, ohne Vor- oder Nachspann:

**Kalibrierung.** War die Selbsteinschätzung "{selbst}" realistisch? Über- oder unterschätzt, kurz begründet.

**Lücken.** Was fehlt komplett, Wichtigstes zuerst, als Aufzählung. Wenn nichts Wesentliches fehlt: so sagen.

**Fehler.** Was wurde inhaltlich falsch wiedergegeben. Wenn nichts: "Keine."

**Unpräzise.** Was ist da, aber zu vage oder verkürzt (auch fehlende konkrete Zahlen, Eigennamen, Fachbegriffe).

**Saß gut.** 1 bis 3 Punkte, die stimmten. Kurz, aber nicht weglassen.

**Nächste Runde.** 1 Satz zum Prinzip: warum sich verteiltes Wiederholen (Spacing) hier lohnt.
Abruf-Fragen fürs nächste Mal:
- 2 bis 3 gezielte Fragen, die genau die Lücken adressieren.

Ton: sachlich, direkt, Du-Form, keine Floskeln, keine Werbesprache.

Ganz am Ende, als allerletzte Zeile allein stehend, eine maschinenlesbare Einschätzung der TATSÄCHLICHEN Abruf-Qualität (darf von der Selbsteinschätzung abweichen):
RATING: nochmal|schwer|gut|leicht
"""


def run_claude(referenz: str, abruf: str, selbst: str) -> dict:
    if not CLAUDE:
        return {"error": "claude CLI nicht gefunden. Läuft der Server im richtigen Terminal (nvm/PATH)?"}
    prompt = PROMPT.format(referenz=referenz, abruf=abruf, selbst=selbst)
    try:
        out = subprocess.run(
            [CLAUDE, "-p", "--output-format", "json", "--model", "sonnet"],
            input=prompt, capture_output=True, text=True, timeout=240, cwd=NEUTRAL_CWD,
        )
    except subprocess.TimeoutExpired:
        return {"error": "Claude hat nicht innerhalb von 4 Minuten geantwortet."}

    text = ""
    try:
        res = json.loads(out.stdout)
        text = (res.get("result") or "").strip()
        if res.get("is_error"):
            low = text.lower()
            if "logg" in low or "login" in low:
                return {"error": "Claude ist nicht angemeldet. Einmal `claude setup-token` im Terminal ausführen, dann Server neu starten."}
            return {"error": f"Claude: {text}"}
    except json.JSONDecodeError:
        text = out.stdout.strip()
    if out.returncode != 0 and not text:
        return {"error": f"Claude-CLI-Fehler: {(out.stderr or 'unbekannt')[:400]}"}
    if not text:
        return {"error": "Leere Antwort von Claude."}

    rating = "gut"
    lines = text.splitlines()
    for i in range(len(lines) - 1, -1, -1):
        s = lines[i].strip()
        if s.upper().startswith("RATING:"):
            r = s.split(":", 1)[1].strip().lower()
            if r in ("nochmal", "schwer", "gut", "leicht"):
                rating = r
            lines.pop(i)
            break
    return {"feedback": "\n".join(lines).strip(), "rating": rating}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, (bytes, bytearray)) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/App", "/App/"):
            self.send_response(302)
            self.send_header("Location", "/App/index.html")
            self.end_headers()
            return
        if path.endswith("/"):
            path += "index.html"
        target = (ROOT / path.lstrip("/")).resolve()
        if target != ROOT and ROOT not in target.parents:
            return self._send(403, b"forbidden", "text/plain")
        if not target.is_file():
            return self._send(404, b"not found", "text/plain")
        self._send(200, target.read_bytes(), CTYPES.get(target.suffix, "application/octet-stream"))

    def do_POST(self):
        if urlparse(self.path).path != "/api/feedback":
            return self._send(404, b"not found", "text/plain")
        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"error": "ungültige Anfrage"})
        referenz = (req.get("referenz") or "").strip()
        abruf = (req.get("abruf") or "").strip()
        selbst = (req.get("selbst") or "?").strip()
        if not referenz or not abruf:
            return self._send(400, {"error": "Referenz oder Abruf fehlt."})
        result = run_claude(referenz, abruf, selbst)
        self._send(200 if "feedback" in result else 502, result)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not CLAUDE:
        print("! claude CLI nicht im PATH – Feedback-Knopf wird nicht funktionieren.")
    print(f"Active Recall läuft: http://localhost:{PORT}/App/")
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        pass
