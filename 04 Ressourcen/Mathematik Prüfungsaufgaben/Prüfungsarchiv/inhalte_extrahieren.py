#!/usr/bin/env python3
# Extrahiert den reinen Aufgaben-/Loesungsinhalt aus den (FrontPage-/2026-/Uebungs-)
# HTML-Dateien und baeckt ihn in inhalte.js. Beim Drucken ist so kein Live-Auslesen
# der Dateien noetig (das ueber file:// blockiert ist); der Inhalt wird als Inline-HTML
# eingebettet -> druckt korrekt, fliesst ueber Seiten um, nichts abgeschnitten.
import json, re, sys, os, posixpath
from bs4 import BeautifulSoup

ARCHIV = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik Prüfungsaufgaben/Prüfungsarchiv"

def rel_root(src, reldir):
    # Bildpfad relativ zum Archiv-Root machen (Datei liegt in reldir/)
    if not src or re.match(r"^(https?:|data:|/|#)", src, re.I):
        return src
    return posixpath.normpath(posixpath.join(reldir, src)) if reldir else src

def extrahiere(relpath):
    pfad = os.path.join(ARCHIV, relpath)
    if not os.path.exists(pfad):
        return None
    reldir = posixpath.dirname(relpath.replace(os.sep, "/"))
    with open(pfad, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    body = soup.body
    if body is None:
        return None
    for t in body.find_all(["script", "style"]):
        t.decompose()
    # Navigations-Tabellen entfernen (enthalten Links auf *.html)
    ziele, gesehen = [], set()
    for a in body.find_all("a", href=True):
        if a.get("href", "").lower().endswith(".html"):
            t = a.find_parent("table") or a
            if id(t) not in gesehen:
                gesehen.add(id(t)); ziele.append(t)
    for t in ziele:
        try:
            t.decompose()
        except Exception:
            pass
    # Inhalt = der inhaltsreichste direkte <div>; sonst der ganze Body (z.B. 2026 = 1 Bild)
    divs = body.find_all("div", recursive=False)
    inhalt = None
    if divs:
        inhalt = max(divs, key=lambda d: len(d.get_text(strip=True)) + len(d.find_all(["img", "svg"])) * 50)
        if len(inhalt.get_text(strip=True)) < 3 and not inhalt.find(["img", "svg"]):
            inhalt = None
    node = inhalt if inhalt is not None else body
    # feste Breite/Hoehe am Wrapper raus, damit es umfliessen kann
    if node.has_attr("style"):
        node["style"] = re.sub(r"(max-)?(width|height)\s*:\s*[^;]+;?", "", node["style"], flags=re.I)
    # Bildpfade auf Archiv-Root umschreiben
    for img in node.find_all("img"):
        if img.has_attr("src"):
            img["src"] = rel_root(img["src"], reldir)
    html = node.decode_contents()
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    html = re.sub(r"[ \t\r\n]+", " ", html).strip()
    return html

def lade_aufgaben():
    s = open(os.path.join(ARCHIV, "daten.js"), encoding="utf-8").read()
    s = s[s.find("["):s.rfind("]") + 1]
    return json.loads(s)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        auf = lade_aufgaben()
        by = {a["slug"]: a for a in auf}
        for slug in ["2011_p3", "2014_p8", "A_a1_p1", "2026_a1_p3"]:
            a = by.get(slug)
            if not a:
                # zeige ein paar echte slugs pro Typ
                print(slug, "slug fehlt; Beispiele:", [x["slug"] for x in auf if x["slug"].startswith(slug[:4])][:3]); continue
            for key, art in (("aufgabe", "a"), ("loesung", "l")):
                h = extrahiere(a.get(key))
                txt = re.sub(r"<[^>]+>", " ", h or ""); txt = re.sub(r"\s+", " ", txt).strip()
                srcs = re.findall(r'src="([^"]+)"', h or "")[:2]
                print(f"{slug} {art}: len={len(h or '')} imgs={(h or '').count('<img')} svg={(h or '').count('<svg')} src0={srcs[:1]} text={txt[:55]!r}")
        sys.exit(0)
    # Volllauf
    auf = lade_aufgaben()
    inhalte = {}
    fehler = 0
    for a in auf:
        slug = a["slug"]
        rec = {}
        ha = extrahiere(a.get("aufgabe"))
        hl = extrahiere(a.get("loesung"))
        if ha:
            rec["a"] = ha
        else:
            fehler += 1
        if hl:
            rec["l"] = hl
        if rec:
            inhalte[slug] = rec
    out = os.path.join(ARCHIV, "inhalte.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("// Automatisch erzeugt aus den Aufgaben-/Loesungsdateien (extract.py).\n")
        f.write("// Vorab extrahierter Inline-Inhalt fuer den Druck (kein file://-Auslesen noetig).\n")
        f.write("window.INHALTE = ")
        json.dump(inhalte, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"geschrieben: {out}")
    print(f"Aufgaben: {len(inhalte)} / {len(auf)}  | ohne Aufgaben-Inhalt: {fehler}")
    print(f"Dateigroesse: {os.path.getsize(out)//1024} KB")
