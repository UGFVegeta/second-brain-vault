"""Gesundheitslogbuch (Befinden, Training) und Schnellerfassung (Inbox) für den Dashboard-Dienst."""
import re
from datetime import date, datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
LOGBUCH = VAULT / "03 Bereiche" / "Gesundheit & Longevity" / "Gesundheitslogbuch.md"
INBOX = VAULT / "01 Inbox" / "Schnellerfassung.md"
KOPF = "|---|---|---|---|---|\n"
ZEILE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|(.*)\|\s*$")
TRAINING_OK = {"–", "Rad", "Schwimmen", "Laufen", "Kraft", "Yoga/Mobility", "Anderes"}


def heute_zeile(tag=None):
    tag = (tag or date.today()).isoformat()
    for z in LOGBUCH.read_text(encoding="utf-8").splitlines():
        m = ZEILE.match(z)
        if m and m.group(1) == tag:
            return {"d": tag, "befinden": int(m.group(2)) if m.group(2).isdigit() else None,
                    "symptome": m.group(3), "training": m.group(4)}
    return None


def setzen(befinden, training):
    """Befinden (1 bis 5) und Training für heute eintragen, Symptome und Notiz bleiben unberührt."""
    if befinden not in (1, 2, 3, 4, 5):
        raise ValueError("Befinden muss 1 bis 5 sein")
    if training not in TRAINING_OK:
        raise ValueError("Training unbekannt")
    tag = date.today().isoformat()
    text = LOGBUCH.read_text(encoding="utf-8")
    zeilen = text.split("\n")
    for i, z in enumerate(zeilen):
        m = ZEILE.match(z)
        if m and m.group(1) == tag:
            zeilen[i] = f"| {tag} | {befinden} | {m.group(3)} | {training} |{m.group(5)}|"
            break
    else:
        k = text.find(KOPF)
        if k < 0:
            raise ValueError("Tabelle im Gesundheitslogbuch nicht gefunden")
        k += len(KOPF)
        text = text[:k] + f"| {tag} | {befinden} | – | {training} | |\n" + text[k:]
        LOGBUCH.write_text(text, encoding="utf-8")
        return heute_zeile()
    LOGBUCH.write_text("\n".join(zeilen), encoding="utf-8")
    return heute_zeile()


def erfassen_inbox(text):
    text = " ".join(text.split())[:500]
    if not text:
        raise ValueError("Text fehlt")
    if not INBOX.exists():
        INBOX.write_text("---\ntags: [inbox]\n---\n\n# Schnellerfassung\n\nKommt aus dem Dashboard. Claude sortiert es bei der nächsten Session ein.\n\n", encoding="utf-8")
    alt = INBOX.read_text(encoding="utf-8")
    INBOX.write_text(alt.rstrip("\n") + f"\n- {datetime.now():%Y-%m-%d %H:%M} {text}\n", encoding="utf-8")
    return text
