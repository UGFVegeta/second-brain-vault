"""Tageswerte aus dem Dashboard-Refresh als Frontmatter in die Daily Note schreiben.

Dadurch hat jede Daily Note Schlaf, Ruhepuls, HRV, Form, PV-Ertrag und Fokus-Minuten als
Properties (Obsidian Bases, Diagramme), ohne dass Oskar etwas tippt. Die Werte kommen
aus den schon gesammelten Daten, nichts wird zusätzlich abgerufen.
Es werden nur die hier genannten Schlüssel angelegt oder aktualisiert, alles andere bleibt.
"""
import re
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
DAILY = VAULT / "05 Daily Notes"


def _wert(v):
    return str(v).replace(",", ".")


def frontmatter_setzen(text, werte):
    """Setzt oder ergänzt Schlüssel im Frontmatter-Block, der Rest des Textes bleibt unberührt."""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        kopf = "\n".join(f"{k}: {v}" for k, v in werte.items())
        return f"---\n{kopf}\n---\n\n" + text
    zeilen = m.group(1).split("\n")
    for k, v in werte.items():
        neu = f"{k}: {v}"
        for i, z in enumerate(zeilen):
            if re.match(rf"^{re.escape(k)}:", z):
                zeilen[i] = neu
                break
        else:
            zeilen.append(neu)
    return "---\n" + "\n".join(zeilen) + "\n---\n" + text[m.end():]


def _schreibe(tag, werte, daily=None):
    werte = {k: v for k, v in werte.items() if v is not None}
    if not werte:
        return False
    daily = daily or DAILY
    pfad = daily / f"{tag}.md"
    if pfad.exists():
        text = pfad.read_text(encoding="utf-8")
    else:
        text = f"---\ntags: [daily]\ndate: {tag}\n---\n\n# {tag}\n"
    neu = frontmatter_setzen(text, werte)
    if neu != text or not pfad.exists():
        pfad.write_text(neu, encoding="utf-8")
    return True


def schreibe(data, heute=None, daily=None):
    """data = das LEBEN-Dict aus leben_refresh.py. Gibt die Liste der beschriebenen Tage zurück."""
    heute = (heute or date.today()).isoformat()
    tage = []
    g = data.get("gesundheit") or {}
    h = g.get("heute") or {}
    if h.get("d"):  # Wellness gehört zum Tag des Aufwachens
        w = {"schlaf_h": h.get("sleep"), "ruhepuls": h.get("rhr"),
             "hrv": round(h["hrv"]) if h.get("hrv") else None}
        if _schreibe(h["d"], w, daily):
            tage.append(h["d"])
    t = data.get("training") or {}
    p = (data.get("pv") or {}).get("heute") or {}
    gew = (g.get("gewicht") or [])
    f = data.get("fokus") or {}
    rest = {"ctl": t.get("ctl"), "atl": t.get("atl"), "tsb": t.get("tsb"),
            "pv_kwh": p.get("prod"), "pv_autark": p.get("autark"),
            "gewicht_kg": gew[-1]["kg"] if gew and gew[-1].get("d") == heute else None,
            "fokus_min": f.get("heute_min")}
    if _schreibe(heute, rest, daily) and heute not in tage:
        tage.append(heute)
    return tage
