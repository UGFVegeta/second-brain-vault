"""Schulleitungs-Training: Inhalte, Fortschritt, Mindmaps und Gespräche mit Claude.

Die Inhalte bleiben Markdown im Vault:
- Fälle: 04 Ressourcen/Schulrecht/Schulrecht – Fallbeispiele mit Lösungen.md
         und Schulleitung/Fälle Verbund.md
- Wochen: 04 Ressourcen/Schulrecht/Wochen/*.md
- Karten: Schulleitung/Karten/*.md
- Wissen: Schulleitung/Wissen/*.md
Der Lernstand liegt in Schulleitung/stand.json.
"""
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "Schulleitung"
VAULT = ROOT.parent.parent
SCHULRECHT = VAULT / "04 Ressourcen" / "Schulrecht"
QUELLEN = SCHULRECHT / "Rechtsquellen"
SCHULGESETZ = QUELLEN / "Schulgesetz BW (Stand 16.12.2025).txt"
FAELLE_DATEIEN = [SCHULRECHT / "Schulrecht – Fallbeispiele mit Lösungen.md", DATA / "Fälle Verbund.md"]
STAND = DATA / "stand.json"
KARTEN = DATA / "Karten"
WISSEN = DATA / "Wissen"
MAPS = DATA / "Mindmaps"
FOTOS = MAPS / "Fotos"
GESPRAECHE = DATA / "Gespräche"

INTERVALLE = [1, 2, 4, 9, 19, 40, 85]
RATINGS = ("nochmal", "schwer", "gut", "leicht")
CLAUDE = shutil.which("claude")
NEUTRAL = tempfile.mkdtemp(prefix="schulleitung-")
LOCK = threading.Lock()
ALIAS = {"euo": "Erziehungs- und Ordnungsmaßnahmen", "ordnungsmaßnahmen": "Erziehungs- und Ordnungsmaßnahmen",
         "schulträger": "Schulträger - Kosten"}
ERLAUBTE_HOSTS = {"localhost:8744", "127.0.0.1:8744"}
OHNE_APP_VARIABLEN = {"ANTHROPIC_BASE_URL", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT",
                      "CLAUDE_CODE_OAUTH_SCOPES", "CLAUDE_CODE_SSE_PORT"}


def erlaubt(headers):
    """Nur Anfragen dieser App: schützt vor Zugriffen fremder Webseiten auf localhost."""
    if headers.get("Host") not in ERLAUBTE_HOSTS:
        return False
    origin = headers.get("Origin")
    return not origin or origin.split("://", 1)[-1] in ERLAUBTE_HOSTS


def kurz_id(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def heute():
    return date.today().isoformat()


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n*", text, re.S)
    fm = {}
    if not m:
        return fm, text
    for zeile in m.group(1).splitlines():
        t = re.match(r"^([A-Za-z0-9_]+):\s?(.*)$", zeile)
        if t:
            fm[t.group(1)] = t.group(2).strip().strip('"')
    return fm, text[m.end():]


# ---------- Lernstand ----------
def stand_laden():
    try:
        return json.loads(STAND.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"karten": {}, "faelle": {}}


def stand_speichern(stand):
    DATA.mkdir(exist_ok=True)
    tmp = STAND.with_suffix(".tmp")
    tmp.write_text(json.dumps(stand, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    tmp.replace(STAND)


def bewerten(art, eintrag_id, rating):
    feld = {"karte": "karten", "fall": "faelle"}.get(art)
    if not feld or rating not in RATINGS or not eintrag_id:
        return None
    with LOCK:
        stand = stand_laden()
        alt = stand[feld].get(eintrag_id, {})
        level = int(alt.get("level", 0))
        if rating == "nochmal":
            level = 0
        elif rating == "gut":
            level = min(len(INTERVALLE) - 1, level + 1)
        elif rating == "leicht":
            level = min(len(INTERVALLE) - 1, level + 2)
        faellig = date.today() + timedelta(days=INTERVALLE[level])
        neu = {"level": level, "faellig": faellig.isoformat(), "zuletzt": heute(),
               "anzahl": int(alt.get("anzahl", 0)) + 1, "rating": rating}
        stand[feld][eintrag_id] = neu
        stand_speichern(stand)
    return neu


def status_von(eintrag):
    if not eintrag:
        return "neu"
    return "faellig" if eintrag.get("faellig", "9999") <= heute() else "spaeter"


# ---------- Fälle ----------
def faelle_lesen():
    alle = []
    for datei in FAELLE_DATEIEN:
        if not datei.exists():
            continue
        _, text = frontmatter(datei.read_text(encoding="utf-8"))
        gruppe, aktuell, teil = None, None, None
        for zeile in text.splitlines():
            if zeile.startswith("## "):
                gruppe, aktuell, teil = zeile[3:].strip(), None, None
            elif zeile.startswith("### "):
                titel = zeile[4:].strip().rstrip(":").strip()
                nr = re.search(r"\s(\d+)(?::|\s|$)", titel)
                aktuell = {"id": kurz_id(titel), "titel": titel, "gruppe": gruppe,
                           "nr": int(nr.group(1)) if nr else None, "text": [], "loesung": []}
                alle.append(aktuell)
                teil = None
            elif aktuell is not None:
                s = zeile.strip()
                if s == "**Fall**":
                    teil = "text"
                elif s == "**Lösung**":
                    teil = "loesung"
                elif s != "---" and teil:
                    aktuell[teil].append(zeile)
    for f in alle:
        f["text"] = "\n".join(f["text"]).strip()
        f["loesung"] = "\n".join(f["loesung"]).strip()
        erste = f["text"].split("\n", 1)[0].strip()
        if erste and len(erste) < 60 and erste in f["titel"]:
            f["text"] = f["text"].split("\n", 1)[-1].strip()
    return alle


def wochen_lesen():
    wochen = []
    for datei in sorted((SCHULRECHT / "Wochen").glob("*.md")):
        fm, _ = frontmatter(datei.read_text(encoding="utf-8"))
        if fm.get("start"):
            wochen.append(fm)
    wochen.sort(key=lambda w: w["start"])
    return wochen


def faelle_der_woche(spec, alle):
    spec = spec or ""
    haupt = [f for f in alle if f["gruppe"] not in ("Grundschule", "Werkrealschule und Verbund")]
    if "gemischt" in spec.lower():
        schritt = max(1, len(haupt) // 10)
        return [f["id"] for f in haupt[::schritt]][:10]
    ids = []
    for teil in spec.split(","):
        m = re.match(r"\s*(.+?)\s*(?:(\d+)\s*[–-]\s*(\d+))?\s*$", teil)
        if not m:
            continue
        name = ALIAS.get(m.group(1).lower(), m.group(1)).lower()
        for f in haupt:
            if not (f["gruppe"] or "").lower().startswith(name):
                continue
            if m.group(2) is None or (f["nr"] and int(m.group(2)) <= f["nr"] <= int(m.group(3))):
                ids.append(f["id"])
    return ids


def naechster_fall(ids, alle, stand):
    faellig = sorted((f for f in alle if status_von(stand["faelle"].get(f["id"])) == "faellig"),
                     key=lambda f: stand["faelle"][f["id"]]["faellig"])
    if faellig:
        return faellig[0]
    nach_id = {f["id"]: f for f in alle}
    for i in ids:
        if i in nach_id and i not in stand["faelle"]:
            return nach_id[i]
    return next((f for f in alle if f["id"] not in stand["faelle"]), None)


# ---------- Karten ----------
def karten_lesen():
    alle = []
    for datei in sorted(KARTEN.glob("*.md")):
        fm, text = frontmatter(datei.read_text(encoding="utf-8"))
        thema = fm.get("thema") or datei.stem
        for block in re.split(r"(?m)^### ", text)[1:]:
            zeilen = block.splitlines()
            frage = zeilen[0].strip()
            felder, feld = {}, None
            for z in zeilen[1:]:
                m = re.match(r"^([ATWQ]):\s?(.*)$", z)
                if m:
                    feld = m.group(1)
                    felder[feld] = m.group(2)
                elif feld and z.strip():
                    felder[feld] += " " + z.strip()
            if frage and felder.get("A"):
                alle.append({"id": kurz_id(datei.stem + frage), "thema": thema, "woche": fm.get("woche"),
                             "frage": frage, "antwort": felder["A"], "tipp": felder.get("T", ""),
                             "warum": felder.get("W", ""), "quelle": felder.get("Q", "")})
    return alle


# ---------- Mindmaps ----------
def sicherer_name(name):
    name = re.sub(r"[^\w äöüÄÖÜß.-]", "", (name or "").strip())[:80].strip(" .")
    return name or None


# ---------- Wissen und Gesetze ----------
ALTE_UNTERLAGEN = {"Skript": SCHULRECHT / "Schulrecht – Skript.md",
                   "Kurzübersicht": SCHULRECHT / "Schulrecht – Kurzübersicht.md"}
GRUPPE_ALT = "Alte Unterlagen"
GRUPPEN_FOLGE = ["Schulzentrum", "Schulrecht", "Verfahren", "Schulentwicklung", GRUPPE_ALT]
RAUSCH = re.compile(r"gültig ab|^https?://|landesrecht-bw\.de/perma|^Fundstelle:|^Neugefasst")


def gleich(a, b):
    return unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b)


def wissen_seiten():
    seiten = [{"gruppe": d.parent.name, "name": d.stem} for d in WISSEN.glob("*/*.md")]
    seiten += [{"gruppe": GRUPPE_ALT, "name": n} for n in ALTE_UNTERLAGEN]
    rang = lambda s: GRUPPEN_FOLGE.index(s["gruppe"]) if s["gruppe"] in GRUPPEN_FOLGE else 99
    return sorted(seiten, key=lambda s: (rang(s), s["name"]))


def wissen_pfad(gruppe, name):
    if gleich(gruppe or "", GRUPPE_ALT):
        return next((p for n, p in ALTE_UNTERLAGEN.items() if gleich(n, name or "")), None)
    return next((d for d in WISSEN.glob("*/*.md") if gleich(d.parent.name, gruppe or "") and gleich(d.stem, name or "")), None)


def quellen_dateien():
    return sorted(QUELLEN.glob("*.txt"), key=lambda p: (not p.stem.startswith("Schulgesetz"), p.stem))


def quelle_lesen(pfad):
    kopf, teile, aktuell, gesehen = [], [], None, set()
    for roh in pfad.read_text(encoding="utf-8").splitlines():
        z = roh.strip()
        if not z or RAUSCH.search(z):
            continue
        m = re.fullmatch(r"§\s*(\d+[a-z]?)", z)
        if m:
            aktuell = {"nr": m.group(1), "titel": "", "absaetze": []}
            if m.group(1) not in gesehen:
                gesehen.add(m.group(1))
                teile.append(aktuell)
            continue
        if aktuell is None:
            kopf.append(z)
        elif not aktuell["titel"]:
            aktuell["titel"] = z
        elif re.match(r"^\(\d+[a-z]?\)", z) or not aktuell["absaetze"]:
            aktuell["absaetze"].append(z)
        else:
            aktuell["absaetze"][-1] += " " + z
    return {"name": pfad.stem, "kopf": kopf[:400], "abschnitte": teile}


def ausschnitt(text, wort):
    i = text.lower().find(wort)
    a = max(0, i - 70)
    return ("… " if a else "") + text[a:i + 130].replace("\n", " ").strip() + " …"


def suche(q):
    woerter = [w.lower() for w in re.split(r"\s+", (q or "").strip()) if len(w) > 1 or w.isdigit()]
    if not woerter:
        return []
    treffer = []

    def pruefe(art, titel, ort, link, text):
        ganz = (titel + " " + text).lower()
        if all(w in ganz for w in woerter):
            im_titel = all(w in titel.lower() for w in woerter)
            quelle = text if woerter[0] in text.lower() else titel
            treffer.append((0 if im_titel else 1, {"art": art, "titel": titel, "ort": ort, "link": link,
                                                   "ausschnitt": ausschnitt(quelle, woerter[0])}))

    nur_nr = re.fullmatch(r"§?\s*(\d+[a-z]?)", (q or "").strip().lower())
    if nur_nr and norm(nur_nr.group(1)):
        n = norm(nur_nr.group(1))
        treffer.append((-1, {"art": "Gesetz", "titel": f"§ {n['nr']} SchG: {n['titel']}", "ort": "Schulgesetz",
                             "link": f"quelle/{SCHULGESETZ.stem}/{n['nr']}", "ausschnitt": n["absaetze"][0][:200] if n["absaetze"] else ""}))
    for s in wissen_seiten():
        pfad = wissen_pfad(s["gruppe"], s["name"])
        _, text = frontmatter(pfad.read_text(encoding="utf-8"))
        for block in re.split(r"(?m)^(?=#{1,3} )", text):
            kopf = block.split("\n", 1)[0].lstrip("# ").strip() if block.startswith("#") else ""
            pruefe("Wissen", s["name"] + (f": {kopf}" if kopf and kopf != s["name"] else ""), s["gruppe"],
                   f"wissen/{s['gruppe']}/{s['name']}", block)
    for p in quellen_dateien():
        q_daten = quelle_lesen(p)
        for a in q_daten["abschnitte"]:
            pruefe("Gesetz", f"§ {a['nr']} {a['titel']}", p.stem, f"quelle/{p.stem}/{a['nr']}", " ".join(a["absaetze"]))
        if not q_daten["abschnitte"]:
            for z in q_daten["kopf"]:
                pruefe("Gesetz", p.stem, "Verwaltungsvorschrift", f"quelle/{p.stem}", z)
    for f in faelle_lesen():
        pruefe("Fall", f["titel"], f["gruppe"], f"fall/{f['id']}", f["text"])
    for k in karten_lesen():
        pruefe("Karte", k["frage"], k["thema"], f"lernen/thema-{k['thema']}", k["antwort"] + " " + k["warum"])
    treffer.sort(key=lambda t: t[0])
    einmalig, gesehen = [], set()
    for _, t in treffer:
        if t["link"] not in gesehen or t["art"] == "Wissen":
            gesehen.add(t["link"])
            einmalig.append(t)
    return einmalig[:50]


def mindmaps_lesen():
    MAPS.mkdir(parents=True, exist_ok=True)
    out = []
    for d in MAPS.glob("*.excalidraw"):
        out.append({"name": d.stem, "art": "zeichnung", "geaendert": d.stat().st_mtime})
    if FOTOS.exists():
        for d in FOTOS.glob("*.jpg"):
            out.append({"name": d.stem, "art": "foto", "geaendert": d.stat().st_mtime})
    out.sort(key=lambda m: -m["geaendert"])
    for m in out:
        m["datum"] = datetime.fromtimestamp(m["geaendert"]).strftime("%d.%m.%Y")
    return out


# ---------- Schulgesetz ----------
_norm_cache = {}


def normen():
    if not _norm_cache:
        text = SCHULGESETZ.read_text(encoding="utf-8")
        teile = re.split(r"(?m)^\s*§\s*(\d+[a-z]?)\s*$", text)
        for i in range(1, len(teile), 2):
            _norm_cache.setdefault(teile[i], teile[i + 1])
    return _norm_cache


def norm(nr):
    roh = normen().get((nr or "").strip().lower())
    if roh is None:
        return None
    zeilen = [z.strip() for z in roh.strip().splitlines() if z.strip()]
    titel = zeilen[0]
    absaetze, puffer = [], []
    for z in zeilen[1:]:
        if re.fullmatch(r"\(\d+[a-z]?\)", z) or re.match(r"^\(\d+[a-z]?\)\s", z):
            if puffer:
                absaetze.append(" ".join(puffer))
            puffer = [z]
        else:
            puffer.append(z)
    if puffer:
        absaetze.append(" ".join(puffer))
    return {"nr": nr, "titel": titel, "absaetze": absaetze}


# ---------- Übersicht ----------
def uebersicht():
    alle = faelle_lesen()
    karten = karten_lesen()
    stand = stand_laden()
    wochen = wochen_lesen()
    t = heute()
    karte_fest = lambda k: int(stand["karten"].get(k["id"], {}).get("level", 0)) >= 2

    liste = []
    for w in wochen:
        ids = faelle_der_woche(w.get("faelle"), alle)
        kw = [k for k in karten if str(k.get("woche")) == str(w.get("woche"))]
        liste.append({"woche": int(w.get("woche", 0)), "start": w["start"], "ende": w.get("ende", ""),
                      "thema": w.get("thema", ""), "fallIds": ids,
                      "faelleFertig": sum(1 for i in ids if i in stand["faelle"]), "faelleGesamt": len(ids),
                      "kartenFertig": sum(1 for k in kw if karte_fest(k)), "kartenGesamt": len(kw)})
    aktuell = next((w for w in liste if w["ende"] >= t), liste[-1] if liste else None)

    faelle = [{"id": f["id"], "titel": f["titel"], "gruppe": f["gruppe"],
               "status": status_von(stand["faelle"].get(f["id"])),
               "faellig": stand["faelle"].get(f["id"], {}).get("faellig", "")} for f in alle]
    kartenliste = [dict(k, status=status_von(stand["karten"].get(k["id"])),
                        level=int(stand["karten"].get(k["id"], {}).get("level", 0))) for k in karten]
    nf = naechster_fall(aktuell["fallIds"] if aktuell else [], alle, stand)
    return {
        "heute": t, "intervalle": INTERVALLE, "wochen": liste, "aktuell": aktuell,
        "naechsterFall": {"id": nf["id"], "titel": nf["titel"]} if nf else None,
        "faelle": faelle, "karten": kartenliste,
        "wissen": wissen_seiten(),
        "quellen": [p.stem for p in quellen_dateien()],
        "mindmaps": mindmaps_lesen(),
    }


# ---------- Claude ----------
SYSTEM = f"""Du bist der Trainingspartner von Oskar. Er ist Realschullehrer in Baden-Württemberg und bereitet sich auf das Überprüfungsverfahren für eine Konrektor- oder Schulleitungsstelle vor, voraussichtlich am Schulzentrum Rudersberg (Verbund aus Grund-, Werkreal- und Realschule).

Rechtsstand:
- Die aktuellen Rechtstexte liegen als .txt in {QUELLEN}. Das Schulgesetz hat den Stand 16.12.2025, die Verordnungen wurden am 05.11.2026 amtlich abgerufen.
- Suche gezielt mit Grep, zum Beispiel das Muster "^\\s*§ 90\\s*$" mit 60 Zeilen Kontext danach, oder ein Stichwort. Lies keine ganzen Dateien und such höchstens viermal.
- Zitiere nur Fundstellen, die du dort tatsächlich gesehen hast. Fehlt etwas, schreib: „nicht in deinen Rechtsquellen geprüft“.
- Ältere Musterlösungen und Skripte stammen von etwa 2022 und sind nur Anhaltspunkt. Weicht eine vom aktuellen Text ab, sag das ausdrücklich.

Ton: Du-Form, sachlich, direkt, kurz. Keine Floskeln, kein Lob ohne Grund, keine Werbesprache, nicht gendern. Diktierfehler ignorierst du. Nenne niemals echte Namen von Schülern, Eltern oder Kollegen, auch wenn Oskar welche nennt. Antworte auf Deutsch in einfachem Markdown ohne Überschriften der Ebene 1 und ohne Trennlinien."""

AUFGABE_FALL_ERST = """Oskar hat den Fall frei beantwortet. Schema: Was ist passiert, welche Rechtsfrage, welche Norm, Abwägung, Entscheidung, nächste Schritte als Schulleitung.

Gib die Rückmeldung genau in dieser Form:

**Einschätzung.** Ein bis zwei Sätze: Trägt die Lösung? Passt seine Selbsteinschätzung „{selbst}“?

**Das saß.** Ein bis drei Punkte.

**Das fehlt oder stimmt nicht.** Wichtigstes zuerst, jeweils mit dem Grund. Wenn nichts fehlt, sag es.

**Norm.** Die einschlägige Fundstelle nach aktuellem Text, in einem Satz, was sie sagt.

**So klingt es vor der Kommission.** Drei bis vier Sätze aus der Rolle der Schulleitung.

**Nachfrage.** Genau eine Frage, wie sie die Kommission stellen würde.

Lies den Sachverhalt genau, auch Zahlen und Zeiträume. Die ganze Rückmeldung hat höchstens 300 Wörter.

Schreib als allerletzte Zeile allein: RATING: nochmal|schwer|gut|leicht (deine Einschätzung der tatsächlichen Qualität, nur eines der vier Wörter)."""

AUFGABE_FALL_WEITER = """Oskar antwortet auf deine Nachfrage oder fragt nach. Antworte kurz, ohne die volle Struktur: Was stimmt, was nicht, gegebenenfalls Fundstelle, und höchstens eine weitere Nachfrage. Schreib als allerletzte Zeile allein: RATING: nochmal|schwer|gut|leicht (Gesamteinschätzung des Falls, nur eines der vier Wörter)."""

AUFGABE_TIPP = """Oskar steckt fest und will einen Denkanstoß, bevor er antwortet. Verrate nicht die Lösung und nicht die Norm. Gib zwei bis drei kurze Fragen, die ihn auf die richtige Spur bringen."""

AUFGABE_KARTE = """Oskar lernt mit einer Karteikarte und hat dazu eine Frage. Erkläre kurz und konkret, gern mit einem Beispiel aus dem Schulalltag. Wenn die Karte aus deiner Sicht falsch oder überholt ist, sag das deutlich."""

AUFGABE_MINDMAP = """Oskar hat aus dem Kopf eine Mindmap gebaut. Vergleiche sie mit dem, was zum Thema nach aktuellem Recht und für die Schulleitung wichtig ist.

Form:

**Das trägt.** Zwei Punkte, wo Struktur und Inhalt stimmen.

**Das fehlt.** Die wichtigsten Lücken, höchstens fünf, mit Fundstelle, wenn es eine gibt.

**Falsch verbunden oder ungenau.** Nur wenn es das gibt.

**Drei Abruffragen.** Für die nächste Runde.

Zeichne keine neue Mindmap und schreib sie nicht für ihn um."""

AUFGABE_WISSEN = """Oskar liest diese Wissensseite und hat dazu eine Frage. Erkläre kurz und konkret, gern mit einem Beispiel aus dem Schulalltag. Wenn die Seite aus deiner Sicht falsch oder überholt ist, sag das deutlich und nenne die Fundstelle."""

AUFGABE_FREI = """Oskar stellt eine Frage zum Schulrecht oder zur Schulleitung. Antworte kurz und mit Fundstelle, soweit du sie geprüft hast."""


def claude_aufruf(system, nachricht):
    if not CLAUDE:
        return {"error": "Die Claude-Kommandozeile wurde nicht gefunden."}
    env = {k: v for k, v in os.environ.items() if k not in OHNE_APP_VARIABLEN}
    befehl = [CLAUDE, "-p", "--output-format", "json", "--model", "sonnet", "--system-prompt", system,
              "--tools", "Read,Grep", "--allowedTools", "Read,Grep", "--add-dir", str(QUELLEN),
              "--add-dir", str(MAPS), "--setting-sources", "project", "--strict-mcp-config",
              "--no-session-persistence"]
    try:
        out = subprocess.run(befehl, input=nachricht, capture_output=True, text=True, timeout=240,
                             cwd=NEUTRAL, env=env)
    except subprocess.TimeoutExpired:
        return {"error": "Claude hat nicht innerhalb von vier Minuten geantwortet. Versuch es noch einmal."}
    text, fehler = "", False
    try:
        res = json.loads(out.stdout)
        text = (res.get("result") or "").strip()
        fehler = bool(res.get("is_error"))
    except ValueError:
        text = out.stdout.strip()
    tief = text.lower()
    if "not logged in" in tief or "/login" in tief:
        return {"error": "Claude ist in der Kommandozeile noch nicht angemeldet. Führ einmal im Terminal „claude auth login“ aus und versuch es dann noch einmal."}
    if fehler or (out.returncode != 0 and not text):
        return {"error": f"Claude meldet: {(text or out.stderr or 'unbekannter Fehler')[:400]}"}
    if not text:
        return {"error": "Claude hat leer geantwortet. Versuch es noch einmal."}
    rating = None
    zeilen = text.splitlines()
    for i in range(len(zeilen) - 1, -1, -1):
        s = zeilen[i].strip()
        if s.upper().startswith("RATING:"):
            r = s.split(":", 1)[1].strip().lower()
            rating = r if r in RATINGS else None
            zeilen.pop(i)
            break
    return {"antwort": "\n".join(zeilen).strip(), "rating": rating}


def verlauf_text(verlauf):
    teile = []
    for m in (verlauf or [])[-12:]:
        wer = "Oskar" if m.get("rolle") == "ich" else "Trainingspartner"
        teile.append(f"{wer}: {str(m.get('text', ''))[:6000]}")
    return "\n\n".join(teile)


def chat(body):
    modus = body.get("modus")
    verlauf = body.get("verlauf") or []
    nachricht = (body.get("nachricht") or "").strip()[:20000]
    if not nachricht:
        return 400, {"error": "Die Nachricht ist leer."}
    kontext, aufgabe = "", AUFGABE_FREI
    if modus in ("fall", "tipp"):
        f = next((x for x in faelle_lesen() if x["id"] == body.get("id")), None)
        if not f:
            return 404, {"error": "Diesen Fall gibt es nicht mehr."}
        kontext = f"## Fall: {f['titel']}\n\n{f['text']}"
        if modus == "tipp":
            aufgabe = AUFGABE_TIPP
        else:
            kontext += f"\n\n## Musterlösung (etwa 2022 oder selbst erstellt, nur Anhaltspunkt)\n\n{f['loesung']}"
            selbst = re.sub(r"[^a-zäöü]", "", str(body.get("selbst") or "keine Angabe"))
            aufgabe = AUFGABE_FALL_WEITER if verlauf else AUFGABE_FALL_ERST.replace("{selbst}", selbst)
    elif modus == "karte":
        k = next((x for x in karten_lesen() if x["id"] == body.get("id")), None)
        if not k:
            return 404, {"error": "Diese Karte gibt es nicht mehr."}
        kontext = (f"## Karteikarte, Thema {k['thema']}\n\nFrage: {k['frage']}\nAntwort: {k['antwort']}\n"
                   f"Erklärung: {k['warum']}\nFundstelle: {k['quelle']}")
        aufgabe = AUFGABE_KARTE
    elif modus == "wissen":
        pfad = wissen_pfad(body.get("gruppe"), body.get("name"))
        if not pfad:
            return 404, {"error": "Diese Seite gibt es nicht mehr."}
        _, seite = frontmatter(pfad.read_text(encoding="utf-8"))
        kontext = f"## Wissensseite: {body.get('name')}\n\n{seite[:14000]}"
        aufgabe = AUFGABE_WISSEN
    elif modus == "mindmap":
        name = sicherer_name(body.get("name"))
        if not name:
            return 400, {"error": "Der Name der Mindmap fehlt."}
        kontext = f"## Thema der Mindmap: {name}\n\n"
        foto = FOTOS / f"{name}.jpg"
        if body.get("foto") and foto.exists():
            kontext += f"Die Mindmap ist ein Foto einer Handskizze. Lies das Bild mit dem Read-Werkzeug: {foto}"
        else:
            kontext += f"Inhalt der gezeichneten Mindmap (Texte und Verbindungen):\n\n{str(body.get('gliederung') or '')[:15000]}"
        aufgabe = AUFGABE_MINDMAP
    prompt = "\n\n".join(x for x in [
        kontext,
        f"## Bisheriges Gespräch\n\n{verlauf_text(verlauf)}" if verlauf else "",
        f"## Aufgabe\n\n{aufgabe}",
        f"## Oskars Nachricht\n\n{nachricht}",
    ] if x)
    ergebnis = claude_aufruf(SYSTEM, prompt)
    return (200 if "antwort" in ergebnis else 502), ergebnis


def fall_abschluss(body):
    f = next((x for x in faelle_lesen() if x["id"] == body.get("id")), None)
    rating = body.get("rating")
    if not f or rating not in RATINGS:
        return 400, {"error": "Fall oder Einschätzung fehlt."}
    neu = bewerten("fall", f["id"], rating)
    GESPRAECHE.mkdir(parents=True, exist_ok=True)
    jetzt = datetime.now()
    datei = GESPRAECHE / f"{jetzt:%Y-%m-%d %H%M} {sicherer_name(f['titel']) or f['id']}.md"
    teile = [
        "---", "tags: [schulleitung, fallgespraech]", f"date: {jetzt:%Y-%m-%d}",
        f"fall: \"{f['titel']}\"", f"selbst: {body.get('selbst') or ''}", f"rating: {rating}",
        f"naechste_wiederholung: {neu['faellig']}", "---", "", f"# {f['titel']}", "",
        "## Meine Antwort", "", str(body.get("antwort") or "").strip(), "", "## Gespräch", "",
    ]
    for m in body.get("verlauf") or []:
        wer = "Ich" if m.get("rolle") == "ich" else "Rückmeldung"
        teile += [f"**{wer}**", "", str(m.get("text", "")).strip(), ""]
    datei.write_text("\n".join(teile), encoding="utf-8")
    return 200, {"eintrag": neu}


def foto_speichern(body):
    name = sicherer_name(body.get("name"))
    m = re.match(r"^data:image/jpeg;base64,(.+)$", body.get("bild") or "", re.S)
    if not name or not m:
        return 400, {"error": "Das Foto konnte nicht gelesen werden. Bitte ein JPG oder PNG verwenden."}
    FOTOS.mkdir(parents=True, exist_ok=True)
    (FOTOS / f"{name}.jpg").write_bytes(base64.b64decode(m.group(1)))
    return 200, {"name": name}


def api_get(route, q):
    wert = lambda k: (q.get(k) or [""])[0]
    if route == "uebersicht":
        return 200, uebersicht()
    if route == "fall":
        f = next((x for x in faelle_lesen() if x["id"] == wert("id")), None)
        if not f:
            return 404, {"error": "Diesen Fall gibt es nicht."}
        return 200, f if wert("loesung") else {k: v for k, v in f.items() if k != "loesung"}
    if route == "wissen":
        pfad = wissen_pfad(wert("gruppe"), wert("name"))
        if not pfad:
            return 404, {"error": "Diese Seite gibt es nicht."}
        fm, text = frontmatter(pfad.read_text(encoding="utf-8"))
        return 200, {"name": wert("name"), "gruppe": wert("gruppe"), "text": text, "stand": fm.get("stand", "")}
    if route == "quelle":
        pfad = next((p for p in quellen_dateien() if gleich(p.stem, wert("name"))), None)
        return (200, quelle_lesen(pfad)) if pfad else (404, {"error": "Diesen Rechtstext gibt es nicht."})
    if route == "suche":
        return 200, {"treffer": suche(wert("q"))}
    if route == "norm":
        n = norm(wert("nr"))
        return (200, n) if n else (404, {"error": "Diesen Paragrafen gibt es im Schulgesetz nicht."})
    if route == "mindmap":
        name = sicherer_name(wert("name"))
        if not name:
            return 400, {"error": "Name fehlt."}
        pfad = MAPS / f"{name}.excalidraw"
        foto = FOTOS / f"{name}.jpg"
        if foto.exists() and not pfad.exists():
            return 200, {"name": name, "art": "foto", "bild": f"/Schulleitung/Mindmaps/Fotos/{name}.jpg"}
        daten = json.loads(pfad.read_text(encoding="utf-8")) if pfad.exists() else None
        return 200, {"name": name, "art": "zeichnung", "daten": daten}
    return 404, {"error": "Unbekannte Anfrage."}


def api_post(route, body):
    if route == "bewerten":
        neu = bewerten(body.get("art"), body.get("id"), body.get("rating"))
        return (200, {"eintrag": neu}) if neu else (400, {"error": "Ungültige Bewertung."})
    if route == "chat":
        return chat(body)
    if route == "fall/abschluss":
        return fall_abschluss(body)
    if route == "foto":
        return foto_speichern(body)
    if route == "mindmap":
        name = sicherer_name(body.get("name"))
        if not name or not isinstance(body.get("daten"), dict):
            return 400, {"error": "Name oder Inhalt fehlt."}
        MAPS.mkdir(parents=True, exist_ok=True)
        tmp = MAPS / f".{name}.tmp"
        tmp.write_text(json.dumps(body["daten"], ensure_ascii=False), encoding="utf-8")
        tmp.replace(MAPS / f"{name}.excalidraw")
        return 200, {"name": name}
    return 404, {"error": "Unbekannte Anfrage."}
