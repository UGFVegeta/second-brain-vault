#!/usr/bin/env python3
"""
Bildgenerierung über Google Gemini (Nano Banana).

Erzeugt oder bearbeitet Bilder für Unterrichtsmaterial und Webseiten und legt sie
standardmäßig in "07 Anhänge/" ab.

Voraussetzung: API-Key aus dem Google AI Studio, abgelegt unter
    ~/.config/claude-image/gemini.env    (Zeile:  GEMINI_API_KEY=...)   Rechte 600
oder als Umgebungsvariable GEMINI_API_KEY.

Nutzung:
    python3 .scripts/bild.py "Ein Prompt, so konkret wie möglich"
    python3 .scripts/bild.py "..." "mein_bild.png"
    python3 .scripts/bild.py "..." --pro            # bessere Qualität + Schrift, teurer
    python3 .scripts/bild.py "..." --ar 16:9        # Seitenverhältnis (nur --pro)
    python3 .scripts/bild.py "Mach den Hintergrund weiß" --edit vorlage.png
    python3 .scripts/bild.py "Füge beide Logos oben ein" --edit a.png --edit b.png

Kosten (Stand 08/2026, ohne Gewähr):
    Standard  (gemini-2.5-flash-image)     ~0,04 $ / Bild
    --pro     (gemini-3-pro-image-preview) ~0,13 $ / Bild, bis 2K, sehr gute Schrift
"""

import argparse
import base64
import datetime as dt
import json
import mimetypes
import os
import pathlib
import sys
import urllib.error
import urllib.request

VAULT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUT_DIR = VAULT / "07 Anhänge"
ENV_FILE = pathlib.Path.home() / ".config" / "claude-image" / "gemini.env"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

MODEL_STD = "gemini-2.5-flash-image"
MODEL_PRO = "gemini-3-pro-image"


def load_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(
        f"Kein API-Key gefunden.\n"
        f"Key aus https://aistudio.google.com/apikey holen und ablegen unter:\n"
        f"  {ENV_FILE}\n"
        f"Inhalt:  GEMINI_API_KEY=DEIN_KEY\n"
        f"Dann:  chmod 600 {ENV_FILE}"
    )


def build_parts(prompt: str, edits: list[str]) -> list[dict]:
    parts: list[dict] = []
    for path in edits:
        p = pathlib.Path(path).expanduser()
        if not p.is_file():
            sys.exit(f"Vorlage nicht gefunden: {p}")
        mime = mimetypes.guess_type(str(p))[0] or "image/png"
        data = base64.b64encode(p.read_bytes()).decode("ascii")
        parts.append({"inlineData": {"mimeType": mime, "data": data}})
    parts.append({"text": prompt})
    return parts


def generate(key: str, model: str, parts: list[dict], aspect: str | None) -> tuple[bytes, str]:
    gen_cfg: dict = {"responseModalities": ["TEXT", "IMAGE"]}
    if aspect:
        gen_cfg["imageConfig"] = {"aspectRatio": aspect}
    body = json.dumps({"contents": [{"parts": parts}], "generationConfig": gen_cfg}).encode()

    req = urllib.request.Request(
        f"{API_BASE}/{model}:generateContent",
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": key,
            "User-Agent": "claude-bild/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        sys.exit(f"API-Fehler {e.code}:\n{detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Netzwerkfehler: {e.reason}")

    text_notes: list[str] = []
    for cand in payload.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                img = base64.b64decode(inline["data"])
                mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
                return img, mime
            if part.get("text"):
                text_notes.append(part["text"])

    msg = "Kein Bild in der Antwort."
    if text_notes:
        msg += " Modelltext: " + " ".join(text_notes)[:500]
    pf = payload.get("promptFeedback") or {}
    if pf:
        msg += f"\npromptFeedback: {json.dumps(pf, ensure_ascii=False)}"
    sys.exit(msg)


def main() -> None:
    ap = argparse.ArgumentParser(description="Bild über Gemini erzeugen oder bearbeiten.")
    ap.add_argument("prompt", help="Bildbeschreibung bzw. Bearbeitungsanweisung")
    ap.add_argument("output", nargs="?", help="Zieldatei (Standard: 07 Anhänge/bild-<zeit>.png)")
    ap.add_argument("--pro", action="store_true", help="gemini-3-pro-image-preview (bessere Schrift, teurer)")
    ap.add_argument("--ar", dest="aspect", help="Seitenverhältnis, z. B. 16:9, 4:3, 1:1 (nur --pro)")
    ap.add_argument("--edit", action="append", default=[], metavar="BILD",
                    help="Vorlagebild zum Bearbeiten (mehrfach möglich)")
    args = ap.parse_args()

    key = load_key()
    model = MODEL_PRO if args.pro else MODEL_STD

    if args.output:
        out = pathlib.Path(args.output).expanduser()
        if not out.is_absolute() and out.parent == pathlib.Path("."):
            out = DEFAULT_OUT_DIR / out
    else:
        stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        out = DEFAULT_OUT_DIR / f"bild-{stamp}.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    parts = build_parts(args.prompt, args.edit)
    img, mime = generate(key, model, parts, args.aspect if args.pro else None)

    ext = mimetypes.guess_extension(mime) or ".png"
    if out.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
        out = out.with_suffix(ext)
    out.write_bytes(img)
    print(f"OK  {out}  ({len(img) // 1024} KB, {model})")


if __name__ == "__main__":
    main()
