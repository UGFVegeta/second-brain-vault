"""Schaltzentrale Bericht: Tages- und Wochenberichte in die Daily Note schreiben.

Tagesbericht   -> Abschnitte "## Geschafft", "## Erkenntnisse", "## Offen / Nächste Schritte"
Wochenrückblick -> "## Wochenrückblick KWnn" mit Unterabschnitten, in der Note des gewählten Tages

Jede Zeile des Eingabefelds wird ein Spiegelstrich. Vorhandenes bleibt stehen (Frontmatter, Fokus),
neue Punkte werden an den passenden Abschnitt angehängt.
"""
import re
from datetime import date, datetime
from pathlib import Path

import logbuch_lib

VAULT = Path(__file__).resolve().parent.parent
DAILY = VAULT / "05 Daily Notes"
NEU = "---\ntags: [daily]\ndate: {d}\n---\n\n# {d}\n"
TAG_ABSCHNITTE = [("geschafft", "Geschafft"), ("erkenntnisse", "Erkenntnisse"), ("offen", "Offen / Nächste Schritte")]
WOCHE_ABSCHNITTE = [("geschafft", "Geschafft"), ("erkenntnisse", "Erkenntnisse"), ("offen", "Nächste Woche")]


def _punkte(text):
    out = []
    for z in str(text or "").splitlines():
        z = re.sub(r"^\s*[-*•]\s*", "", z).strip()
        if z:
            out.append("- " + z[:600])
    return out


def _pfad(tag):
    return DAILY / f"{tag.isoformat()}.md"


def _anhaengen(text, ueberschrift, zeilen, ebene="## "):
    """Hängt Zeilen an den Abschnitt `ueberschrift` an oder legt ihn am Ende der passenden Ebene an."""
    kopf = re.compile(rf"^{re.escape(ebene)}{re.escape(ueberschrift)}\s*$", re.M)
    m = kopf.search(text)
    if not m:
        return text.rstrip("\n") + f"\n\n{ebene}{ueberschrift}\n" + "\n".join(zeilen) + "\n"
    rest = text[m.end():]
    nxt = re.search(rf"^{'#' * (len(ebene) - 1)}{{1,{len(ebene) - 1}}} ", rest, re.M)
    ende = m.end() + (nxt.start() if nxt else len(rest))
    vorn, hinten = text[:ende].rstrip("\n"), text[ende:]
    return vorn + "\n" + "\n".join(zeilen) + "\n" + ("\n" + hinten.lstrip("\n") if hinten.strip() else "")


def eintragen(tag, art, felder, befinden=None):
    """Schreibt den Bericht. art: 'tag' oder 'woche'. Gibt Pfad und Zahl der Punkte zurück."""
    if art not in ("tag", "woche"):
        raise ValueError("art unbekannt")
    if tag > date.today():
        raise ValueError("Datum liegt in der Zukunft")
    anzahl = 0
    pfad = _pfad(tag)
    text = pfad.read_text(encoding="utf-8") if pfad.exists() else NEU.format(d=tag.isoformat())
    if art == "tag":
        for key, titel in TAG_ABSCHNITTE:
            z = _punkte(felder.get(key))
            if z:
                text = _anhaengen(text, titel, z)
                anzahl += len(z)
    else:
        kw = tag.isocalendar()[1]
        haupt = f"Wochenrückblick KW{kw:02d}"
        if not re.search(rf"^## {re.escape(haupt)}\s*$", text, re.M):
            text = text.rstrip("\n") + f"\n\n## {haupt}\n"
        for key, titel in WOCHE_ABSCHNITTE:
            z = _punkte(felder.get(key))
            if z:
                # Unterabschnitt innerhalb des Wochenrückblicks anhängen (Ebene ###)
                m = re.search(rf"^## {re.escape(haupt)}\s*$", text, re.M)
                nxt_h2 = re.search(r"^## ", text[m.end():], re.M)
                ende = m.end() + (nxt_h2.start() if nxt_h2 else len(text) - m.end())
                block = text[m.start():ende]
                block = _anhaengen(block, titel, z, ebene="### ")
                text = text[:m.start()] + block.rstrip("\n") + "\n" + ("\n" + text[ende:].lstrip("\n") if text[ende:].strip() else "")
                anzahl += len(z)
    if anzahl == 0 and befinden is None:
        raise ValueError("Nichts eingetragen")
    if anzahl:
        pfad.write_text(text, encoding="utf-8")
    if befinden is not None and tag == date.today():
        alt = logbuch_lib.heute_zeile()
        logbuch_lib.setzen(int(befinden), (alt or {}).get("training") or "–")
    return {"pfad": str(pfad.relative_to(VAULT)), "punkte": anzahl}


def lesen(tag):
    """Gibt zurück, was in der Note des Tages schon unter den Berichts-Abschnitten steht."""
    pfad = _pfad(tag)
    if not pfad.exists():
        return {"d": tag.isoformat(), "vorhanden": False, "text": ""}
    text = pfad.read_text(encoding="utf-8")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return {"d": tag.isoformat(), "vorhanden": True, "text": text.strip()[:6000]}


def letzte(n=7):
    """Die letzten n Tage mit Eintrag in Geschafft/Erkenntnisse/Offen, für die Verlaufsliste."""
    out = []
    for f in sorted(DAILY.glob("????-??-??.md"), reverse=True):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"^## (Geschafft|Erkenntnisse|Offen|Wochenrückblick)", t, re.M):
            body = len(re.findall(r"^- (?!\d{2}:\d{2} bis)", t, re.M))
            out.append({"d": f.stem, "punkte": body})
        if len(out) >= n:
            break
    return out
