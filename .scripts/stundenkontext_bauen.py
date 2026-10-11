#!/usr/bin/env python3
"""Baut aus den Stoffverteilungsplänen und den Rahmendaten eine kompakte Wochenübersicht
für den Mod Schul-Cockpit (Stundenkontext bei „7c“, „10b“, „Physik 10“ …).

Quelle:  04 Ressourcen/Mathematik/… Stoffverteilungsplan …html, 04 Ressourcen/Physik/Stoffverteilungsplan …md,
         04 Ressourcen/Physik/Rahmendaten Schuljahr 2026-27.md
Ziel:    ~/.claude/mods/schul-cockpit/stundenkontext.json
Zusätze (Ausfallwochen, Exkursionen): Liste ZUSATZ unten pflegen.

Aufruf:  python3 .scripts/stundenkontext_bauen.py
"""
import json
import re
from datetime import date, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
RES = VAULT / "04 Ressourcen"
ZIEL = Path.home() / ".claude/mods/schul-cockpit/stundenkontext.json"
JAHR1, JAHR2 = 2026, 2027
START = date(2026, 9, 14)  # Montag Woche 1

# Bekannte Ausfälle, die in keinem Plan stehen (aus Vault-Notizen)
ZUSATZ = [
    {"von": "2026-10-19", "bis": "2026-10-23", "was": "Zeitfensterwoche: kein regulärer Unterricht, 10er in Berlin", "klassen": ["7c", "10b"]},
]


def datum(tag_monat: str) -> str:
    """'14.09.' oder '14.9' → ISO-Datum im Schuljahr"""
    t, m = [int(x) for x in re.findall(r"\d+", tag_monat)[:2]]
    j = JAHR1 if m >= 8 else JAHR2
    return date(j, m, t).isoformat()


def zellen(zeile_html: str):
    return [re.sub(r"<[^>]+>|\s+", " ", c).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", zeile_html, re.S)]


def mathe7():
    s = (RES / "Mathematik/Mathematik Klasse 7 – Stoffverteilungsplan Schule.html").read_text(encoding="utf-8")
    out = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S):
        c = zellen(r)
        if len(c) >= 4 and c[0].isdigit():
            von = datum(c[1].split("–")[0]) if re.search(r"\d", c[1]) else None
            thema = c[3] or c[2]
            out.append({"nr": int(c[0]), "von": von, "thema": thema, "plan": c[2], "termine": c[4] if len(c) > 4 else ""})
    return out


def mathe10():
    s = (RES / "Mathematik/Stoffverteilungsplan 26-27 Mathe 10.html").read_text(encoding="utf-8")
    out = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S):
        c = zellen(r)
        if len(c) >= 4 and c[0].isdigit() and re.search(r"\d", c[1]):
            out.append({"nr": int(c[0]), "von": datum(c[1]), "thema": c[3], "termine": c[4] if len(c) > 4 else ""})
    return out


def physik(datei: str):
    s = (RES / "Physik" / datei).read_text(encoding="utf-8")
    out = []
    for z in s.splitlines():
        m = re.match(r"^\|\s*W(\d+)\s*\|\s*(\d{2}\.\d{2}\.\d{4})\s*\|\s*([^|]*)\|\s*([^|]*)\|", z)
        if m:
            t, mo, j = [int(x) for x in m.group(2).split(".")]
            out.append({"nr": int(m.group(1)), "von": date(j, mo, t).isoformat(), "thema": f"{m.group(3).strip()}: {m.group(4).strip()}", "termine": ""})
    return out


def ferien():
    s = (RES / "Physik/Rahmendaten Schuljahr 2026-27.md").read_text(encoding="utf-8")
    out = []
    for name, zeitraum in re.findall(r"^\|\s*(\w+ferien)\s*\|\s*([^|]+)\|", s, re.M):
        d = re.findall(r"(\d{2})\.(\d{2})\.(\d{4})?", zeitraum)
        if len(d) >= 2:
            (t1, m1, j1), (t2, m2, j2) = d[0], d[1]
            j2 = int(j2) if j2 else (JAHR1 if int(m2) >= 8 else JAHR2)
            j1 = int(j1) if j1 else (j2 if int(m1) <= int(m2) else j2 - 1)
            out.append({"von": date(j1, int(m1), int(t1)).isoformat(), "bis": date(j2, int(m2), int(t2)).isoformat(), "was": name})
    return out


def main():
    daten = {
        "erzeugt": date.today().isoformat(),
        "klassen": {
            "Mathe 7c": mathe7(),
            "Mathe 10b": mathe10(),
            "Physik 7c": physik("Stoffverteilungsplan Physik Klasse 7 2026-27.md"),
            "Physik 10": physik("Stoffverteilungsplan Physik Klasse 10 2026-27.md"),
        },
        "frei": ferien() + ZUSATZ,
    }
    ZIEL.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in daten["klassen"].items():
        print(f"{k}: {len(v)} Wochen")
    print(f"Ferien/Ausfälle: {len(daten['frei'])}")
    print(f"→ {ZIEL}")


if __name__ == "__main__":
    main()
