"""Fokus-Timer: Zeilen in die Daily Note schreiben und wieder auswerten.

Eine Fokus-Einheit steht in der Daily Note des Tages im Abschnitt "## Fokus":

    - 14:05 bis 14:50, 45 min, [[Konrektor-Stelle Schulzentrum Rudersberg]]

Genutzt vom Dashboard-Dienst (schreibt) und von leben_refresh.py (liest).
"""
import re
from datetime import date, datetime, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
DAILY = VAULT / "05 Daily Notes"
PROJEKTE = VAULT / "02 Projekte"
OHNE = "Ohne Projekt"

ZEILE = re.compile(r"^- (\d{2}:\d{2}) bis (\d{2}:\d{2}), (\d+) min, \[\[(.+?)\]\]\s*$", re.M)
DAILY_NEU = "---\ntags: [daily]\ndate: {d}\n---\n\n# {d}\n\n## Fokus\n"


def projekt_gueltig(name):
    return name == OHNE or (PROJEKTE / f"{name}.md").is_file()


def eintragen(projekt, start, ende, minuten):
    """Hängt eine Zeile an die heutige Daily Note an. Gibt die Zeile zurück."""
    if not projekt_gueltig(projekt):
        raise ValueError("Projekt unbekannt")
    if not (1 <= minuten <= 600):
        raise ValueError("Dauer außerhalb 1 bis 600 Minuten")
    tag = ende.date()
    pfad = DAILY / f"{tag.isoformat()}.md"
    zeile = f"- {start:%H:%M} bis {ende:%H:%M}, {minuten} min, [[{projekt}]]"
    if not pfad.exists():
        pfad.write_text(DAILY_NEU.format(d=tag.isoformat()), encoding="utf-8")
    text = pfad.read_text(encoding="utf-8")
    if re.search(r"^## Fokus\s*$", text, re.M):
        m = re.search(r"^## Fokus\s*$", text, re.M)
        rest = text[m.end():]
        nxt = re.search(r"^## ", rest, re.M)
        ende_abschnitt = m.end() + (nxt.start() if nxt else len(rest))
        kopf, fuss = text[:ende_abschnitt].rstrip("\n"), text[ende_abschnitt:]
        text = kopf + "\n" + zeile + "\n" + ("\n" + fuss.lstrip("\n") if fuss.strip() else "")
    else:
        m = re.search(r"^## Offen", text, re.M)
        block = "## Fokus\n" + zeile + "\n\n"
        text = (text[:m.start()] + block + text[m.start():]) if m else text.rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n"
    pfad.write_text(text, encoding="utf-8")
    return zeile


def auswerten(heute=None):
    """Fokus-Minuten heute, in dieser Woche (ab Montag) und pro Projekt."""
    heute = heute or date.today()
    montag = heute - timedelta(days=heute.weekday())
    out = {"heute_min": 0, "woche_min": 0, "projekte": {}, "tage": {}}
    for i in range(0, 14):
        d = heute - timedelta(days=i)
        f = DAILY / f"{d.isoformat()}.md"
        if not f.is_file():
            continue
        summe = 0
        for _s, _e, mins, proj in ZEILE.findall(f.read_text(encoding="utf-8", errors="ignore")):
            mins = int(mins)
            summe += mins
            if d >= montag:
                out["projekte"][proj] = out["projekte"].get(proj, 0) + mins
        out["tage"][d.isoformat()] = summe
        if d == heute:
            out["heute_min"] = summe
        if d >= montag:
            out["woche_min"] += summe
    return out


def projekt_minuten(name, von, bis):
    """Summe der Fokus-Minuten für ein Projekt zwischen zwei Tagen (einschließlich)."""
    summe, d = 0, von
    while d <= bis:
        f = DAILY / f"{d.isoformat()}.md"
        if f.is_file():
            for _s, _e, mins, proj in ZEILE.findall(f.read_text(encoding="utf-8", errors="ignore")):
                if proj == name:
                    summe += int(mins)
        d += timedelta(days=1)
    return summe
