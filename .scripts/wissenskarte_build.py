#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Wissenskarte – Vault-Scan und Layout-Berechnung.

Liest alle Notizen des Vaults ein, extrahiert Wikilinks und Tags,
clustert nach Ordnern und berechnet ein fertiges Karten-Layout
(Cluster-Packung + Sonnenblumen-Anordnung, Hubs in der Mitte).
Schreibt "04 Ressourcen/wissenskarte_data.js" für Wissenskarte.html.

Start:  python3 .scripts/wissenskarte_build.py
        (läuft auch automatisch im Lebens-Dashboard-Refresh mit)
"""
import json
import math
import re
from datetime import datetime
from pathlib import Path

VAULT = Path("/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude")
OUT = VAULT / "04 Ressourcen" / "wissenskarte_data.js"
SKIP_PARTS = {".obsidian", ".git", ".trash", ".claude", ".scripts", ".firecrawl",
              ".agents", "skills", "Templates", "07 Anhänge"}
EXCERPT_LEN = 1600

PALETTE = ["#5aa2f0", "#a78bfa", "#2dd4a7", "#f0b954", "#f28b6b", "#f27ba8",
           "#6ee7e0", "#c4b5fd", "#93c5fd", "#fbbf77", "#86efac", "#fda4af"]


def cluster_key(parts):
    top = parts[0]
    sub = parts[1] if len(parts) > 2 else ""
    if top == "Readwise":
        return "Kindle-Highlights" if sub == "Books" else "Readwise-Artikel"
    if top == "04 Ressourcen":
        if sub == "Bücher & Learnings":
            return "Bücher & Learnings"
        if sub in ("Mathematik", "Physik", "Sport", "Wiki"):
            return sub
        return "Ressourcen"
    if top == "03 Bereiche":
        return "Bereiche"
    if top == "05 Daily Notes":
        return "Daily Notes"
    if top == "02 Projekte":
        return "Projekte"
    if top == "01 Inbox":
        return "Inbox"
    if top == "00 Kontext":
        return "Kontext"
    if top == "06 Archiv":
        return "Archiv"
    return "Sonstiges"


FM = re.compile(r"^---\n.*?\n---\n", re.S)
WIKI = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
TAGS_FM = re.compile(r"^tags:\s*\[([^\]]*)\]", re.M)


def clean_excerpt(text):
    t = FM.sub("", text)
    t = re.sub(r"!\[\[[^\]]*\]\]", "", t)          # eingebettete Bilder
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)
    t = re.sub(r"%%[^%]*%%", "", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t[:EXCERPT_LEN]


# --- Notizen einlesen -------------------------------------------------------
notes = []
for f in sorted(VAULT.rglob("*.md")):
    parts = f.relative_to(VAULT).parts
    if len(parts) < 2 or any(p in SKIP_PARTS for p in parts):
        continue
    try:
        raw = f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    is_draw = f.name.endswith(".excalidraw.md")
    tags = []
    m = TAGS_FM.search(raw[:800])
    if m:
        tags = [t.strip().strip('"') for t in m.group(1).split(",") if t.strip()]
    notes.append({
        "path": str(f.relative_to(VAULT)),
        "name": f.stem.replace(".excalidraw", ""),
        "cluster": cluster_key(parts),
        "tags": tags[:6],
        "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
        "excerpt": "(Excalidraw-Zeichnung)" if is_draw else clean_excerpt(raw),
        "raw_links": [] if is_draw else [w.strip() for w in WIKI.findall(raw)],
    })

# --- Wikilinks auflösen -----------------------------------------------------
by_stem = {}
for i, n in enumerate(notes):
    by_stem.setdefault(n["name"].lower(), i)
    by_stem.setdefault(n["path"][:-3].lower(), i)
links = set()
for i, n in enumerate(notes):
    for w in n["raw_links"]:
        j = by_stem.get(w.lower()) or by_stem.get(w.split("/")[-1].lower())
        if j is not None and j != i:
            links.add((min(i, j), max(i, j)))
links = sorted(links)
deg = [0] * len(notes)
for a, b in links:
    deg[a] += 1
    deg[b] += 1

# --- Cluster packen ---------------------------------------------------------
order = {}
for n in notes:
    order[n["cluster"]] = order.get(n["cluster"], 0) + 1
clusters = sorted(order.items(), key=lambda x: -x[1])
cinfo = []
placed = []
GOLD = math.pi * (3 - math.sqrt(5))
for ci, (key, cnt) in enumerate(clusters):
    R = 26 * math.sqrt(cnt) + 60
    if not placed:
        x = y = 0.0
    else:
        best = None
        for k in range(2000):
            t = 0.6 * k
            a = k * GOLD
            x, y = t * math.cos(a), t * math.sin(a)
            if all(math.hypot(x - p[0], y - p[1]) > R + p[2] + 40 for p in placed):
                best = (x, y)
                break
        x, y = best if best else (placed[-1][0] + placed[-1][2] + R + 40, placed[-1][1])
    placed.append((x, y, R))
    cinfo.append({"key": key, "label": key, "color": PALETTE[ci % len(PALETTE)],
                  "x": round(x, 1), "y": round(y, 1), "r": round(R, 1), "n": cnt})
cidx = {c["key"]: i for i, c in enumerate(cinfo)}

# --- Knoten anordnen (Sonnenblume, Hubs in der Mitte) -----------------------
slots = {}
for i, n in sorted(enumerate(notes), key=lambda x: -deg[x[0]]):
    ci = cidx[n["cluster"]]
    c = cinfo[ci]
    k = slots.get(ci, 0)
    slots[ci] = k + 1
    r = (c["r"] - 26) * math.sqrt((k + 0.5) / c["n"])
    a = k * 2.39996
    n["x"] = round(c["x"] + r * math.cos(a), 1)
    n["y"] = round(c["y"] + r * math.sin(a), 1)
    n["ci"] = ci
    n["deg"] = deg[i]

out_nodes = [{"t": n["name"], "p": n["path"], "c": n["ci"], "x": n["x"], "y": n["y"],
              "g": n["tags"], "d": n["mtime"], "e": n["excerpt"], "k": n["deg"]}
             for n in notes]

# --- Ring-Ansicht: Claude-Setup (Skills, Memory, Anbindungen, Automatik) ----
FM_FIELD = lambda txt, f: (re.search(rf"^{f}:\s*(.+)$", txt[:900], re.M) or [None, ""])[1]


def ring_data():
    cats = []

    skills = []
    for d in sorted((VAULT / ".claude" / "skills").glob("*/SKILL.md")) + \
             sorted((VAULT / "skills").glob("*/SKILL.md")):
        txt = d.read_text(encoding="utf-8", errors="ignore")
        desc = str(FM_FIELD(txt, "description")).strip().strip('"')
        skills.append({"t": d.parent.name, "d": desc[:160]})
    cats.append({"label": "Skills", "color": "#a78bfa", "items": skills})

    mem = []
    memdir = Path.home() / ".claude/projects/-Users-oskarklein-Documents-Obsidian-Claude-Second-Brain-Claude/memory"
    for f in sorted(memdir.glob("*.md")):
        if f.name == "MEMORY.md":
            continue
        txt = f.read_text(encoding="utf-8", errors="ignore")
        mem.append({"t": str(FM_FIELD(txt, "name")).strip() or f.stem,
                    "d": str(FM_FIELD(txt, "description")).strip()[:160]})
    cats.append({"label": "Memory", "color": "#f27ba8", "items": mem})

    verb = [
        {"t": "Apple Kalender", "d": "Termine lesen/anlegen per AppleScript – alle Kalender"},
        {"t": "Apple Reminders", "d": "Erinnerungen anlegen per AppleScript (Inbox, Erinnerungen, Familie)"},
        {"t": "E-Mail (IMAP)", "d": "web.de + Gmail lesen und vorsortieren – nie automatisch senden"},
        {"t": "intervals.icu", "d": "Trainingsdaten-API (Garmin direkt), Form CTL/ATL/TSB"},
        {"t": "Kostal PV", "d": "Wechselrichter-API im Heimnetz – Produktion, Batterie, Netz"},
        {"t": "Kindle-Datenbank", "d": "Lokale BookData.sqlite der Kindle-App – Bibliothek + Lesestand"},
        {"t": "NotebookLM", "d": "notebooklm-CLI (Python 3.12), Account oskar17185"},
    ]
    mcp_file = VAULT / ".mcp.json"
    if mcp_file.exists():
        try:
            for name in json.loads(mcp_file.read_text()).get("mcpServers", {}):
                verb.append({"t": f"MCP: {name}", "d": "Projekt-MCP-Server aus .mcp.json"})
        except Exception:
            pass
    cats.append({"label": "Anbindungen", "color": "#5aa2f0", "items": verb})

    auto = []
    for pl in sorted(Path.home().glob("Library/LaunchAgents/com.oskar.*.plist")):
        txt = pl.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"Hour</key>\s*<integer>(\d+)</integer>\s*<key>Minute</key>\s*<integer>(\d+)", txt)
        t = pl.stem.replace("com.oskar.", "")
        auto.append({"t": t, "d": f"LaunchAgent, täglich {m.group(1)}:{int(m.group(2)):02d} Uhr" if m else "LaunchAgent"})
    for c in sorted(VAULT.rglob("*.command")):
        if ".trash" not in c.parts:
            auto.append({"t": c.stem, "d": f"Doppelklick-Start: {c.relative_to(VAULT)}"})
    cats.append({"label": "Automatik", "color": "#f0b954", "items": auto})

    scr = []
    for s in sorted((VAULT / ".scripts").glob("*.py")):
        first = ""
        for line in s.read_text(encoding="utf-8", errors="ignore").splitlines()[:6]:
            line = line.strip().strip('"').strip("'")
            if line and not line.startswith("#") and not line.startswith("import"):
                first = line
                break
        scr.append({"t": s.stem, "d": first[:160]})
    cats.append({"label": "Skripte", "color": "#2dd4a7", "items": scr})

    dash = []
    for name in ["Lebens-Dashboard", "Wissenskarte", "Lese-Dashboard", "Lese-Bibliothek", "Dashboard"]:
        f = VAULT / "04 Ressourcen" / f"{name}.html"
        if f.exists():
            label = "Unterrichtsmaterial" if name == "Dashboard" else name
            dash.append({"t": label, "d": f"HTML-Dashboard in 04 Ressourcen", "href": f"{name}.html"})
    for f in sorted((VAULT / "04 Ressourcen" / "Notenschlüsselrechner").glob("*.html")):
        dash.append({"t": f.stem, "d": "Rechner-Tool", "href": f"Notenschlüsselrechner/{f.name}"})
    cats.append({"label": "Dashboards", "color": "#f28b6b", "items": dash})
    return {"cats": cats}


payload = "window.WK = " + json.dumps({
    "generated": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    "clusters": cinfo,
    "nodes": out_nodes,
    "links": [list(l) for l in links],
    "ring": ring_data(),
}, ensure_ascii=False) + ";\n"
OUT.write_text(payload, encoding="utf-8")
print(f"Wissenskarte: {len(notes)} Notizen, {len(links)} Verbindungen, "
      f"{len(cinfo)} Cluster → {OUT.name} ({len(payload) // 1024} kB)")
