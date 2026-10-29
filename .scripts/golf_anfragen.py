#!/usr/bin/env python3
"""Golf-Verkauf: liest Käuferanfragen aus web.de (nur lesend) und baut eine HTML-Übersicht.

Anfragen von mobile.de und von Kleinanzeigen (läuft über mobile.de) kommen als Mails von
kontakt.mobile.de an. Jeder Interessent hat dort eine eigene Relay-Adresse, darüber werden die
Mails zu einem Gespräch gruppiert. Verändert nichts im Postfach, sendet nichts.

Aufruf: golf_anfragen.py            baut Anfragen.html
        golf_anfragen.py --text     gibt zusätzlich eine Kurzfassung im Terminal aus
"""
import imaplib, email, os, re, sys, html
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone

SEIT = "26-Oct-2026"  # Tag, an dem die Inserate online gingen
ORDNER = ["INBOX", "Unbekannt", "Unerw&APw-nscht", "Later"]
VAULT = os.path.expanduser("~/Documents/Obsidian Claude/Second Brain Claude")
AUSGABE = os.path.join(VAULT, "02 Projekte/Golf Verkauf/Anfragen.html")
KA_JSON = os.path.join(VAULT, "02 Projekte/Golf Verkauf/kleinanzeigen.json")
ENV = os.path.expanduser("~/.config/claude-mail/web-de.env")


def load_env(path):
    d = {}
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d


def dec(s):
    try:
        return str(make_header(decode_header(s))) if s else ""
    except Exception:
        return s or ""


def text_of(msg):
    txt = ""
    for p in msg.walk():
        if p.get_content_type() == "text/plain":
            txt = p.get_payload(decode=True).decode(p.get_content_charset() or "utf-8", "ignore")
            break
    if not txt:
        for p in msg.walk():
            if p.get_content_type() == "text/html":
                h = p.get_payload(decode=True).decode(p.get_content_charset() or "utf-8", "ignore")
                h = re.sub(r"<(script|style).*?</\1>", "", h, flags=re.S)
                txt = html.unescape(re.sub(r"<[^>]+>", " ", h))
                break
    return txt


def parse(msg):
    """Gibt (name, plattform, telefon, nachricht) zurück."""
    absender = dec(msg.get("From", "")).replace("\n", " ").replace("\t", " ")
    name = re.sub(r"\s*<.*?>\s*", "", absender).strip().strip('"')
    betreff = dec(msg.get("Subject", ""))
    txt = re.sub(r"https?://\S+", "", text_of(msg))
    flach = re.sub(r"[ \t\r\f\v]+", " ", txt)
    plattform = "mobile.de"
    if "Kleinanzeigen" in betreff or "über Kleinanzeigen" in flach:
        plattform = "Kleinanzeigen"
    if "autoscout" in absender.lower() or "autoscout" in betreff.lower():
        plattform = "AutoScout24"
    telefon = ""
    nachricht = ""
    m = re.search(r"Nachricht des Interessenten\s+(.*?)\s+(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag)", flach, re.S)
    if m:
        rest = m.group(1)
        t = re.search(r"(\+?\d[\d ()/-]{6,})", rest)
        telefon = t.group(1).strip() if t else ""
    m = re.search(r"Nachricht:\s*(.*?)\s*(\+\+\+|Nutze bitte die Antwort)", flach, re.S)
    if m:
        nachricht = re.sub(r"\s+", " ", m.group(1)).strip()
    else:
        nachricht = re.split(r"-{10,}", flach)[0]
        nachricht = re.sub(r"\s+", " ", nachricht).strip()
    return name, plattform, telefon, nachricht


def holen():
    cfg = load_env(ENV)
    user = next(cfg[k] for k in cfg if k.endswith("_USER"))
    pw = "".join(next(cfg[k] for k in cfg if k.endswith("PASSWORD")).split()).replace("\xa0", "")
    M = imaplib.IMAP4_SSL("imap.web.de", 993)
    M.login(user, pw)
    gespraeche = {}
    sonstige = []
    for ordner in ORDNER:
        if M.select(ordner, readonly=True)[0] != "OK":
            continue
        for kriterium in (("FROM", '"kontakt.mobile.de"'), ("FROM", '"autoscout24"')):
            typ, d = M.search(None, "SINCE", SEIT, *kriterium)
            for i in d[0].split():
                t, m = M.fetch(i, "(BODY.PEEK[])")
                msg = email.message_from_bytes(m[0][1])
                try:
                    zeit = parsedate_to_datetime(msg["Date"])
                    if zeit.tzinfo is None:
                        zeit = zeit.replace(tzinfo=timezone.utc)
                except Exception:
                    continue
                adr = re.search(r"<(.*?)>", msg.get("From", ""))
                schluessel = adr.group(1) if adr else msg.get("From", "")
                name, plattform, telefon, nachricht = parse(msg)
                g = gespraeche.setdefault(schluessel, {"name": name, "plattform": plattform, "telefon": "", "msgs": []})
                if telefon and not g["telefon"]:
                    g["telefon"] = telefon
                if plattform != "mobile.de":
                    g["plattform"] = plattform
                g["msgs"].append((zeit, nachricht))
    M.logout()
    for g in gespraeche.values():
        g["msgs"].sort()
        # Telefonnummer, die als eigene Nachricht kam, auch erfassen
        if not g["telefon"]:
            for _, n in g["msgs"]:
                t = re.fullmatch(r"\+?\d[\d ()/-]{7,}", n)
                if t:
                    g["telefon"] = n
    return sorted(gespraeche.values(), key=lambda g: g["msgs"][-1][0], reverse=True)


def betraege(g):
    treffer = []
    for _, n in g["msgs"]:
        for m in re.finditer(r"(\d{1,2}[.]?\d{3}|\d{3,5})\s*(€|euro|eur)\b", n, re.I):
            treffer.append(m.group(0))
    return treffer


def lokal(z):
    return z.astimezone().strftime("%d.%m. %H:%M")


CHANCEN = {"hoch": "Chance hoch", "mittel": "Chance mittel", "niedrig": "Chance niedrig", "erledigt": "erledigt"}
UNBEWERTET = {"rang": 50, "chance": "mittel", "angebot": "unbekannt", "grund": "Noch nicht bewertet.", "schritt": "Nachricht lesen und entscheiden."}


def ka_zeit(s):
    """'26.10. 17:56' -> datetime (Jahr 2026)."""
    return datetime.strptime("2026." + s, "%Y.%d.%m. %H:%M")


def personen(gespraeche, ka, bew):
    """Vereinheitlicht mobile.de- und Kleinanzeigen-Gespräche: Liste von Dicts, sortiert nach Einschätzung."""
    leute = []
    for g in gespraeche:
        msgs = [(z.astimezone().replace(tzinfo=None), "er", n) for z, n in g["msgs"]]
        leute.append({"name": g["name"], "plattform": g["plattform"], "telefon": g["telefon"], "status": "", "msgs": msgs})
    for g in ka.get("gespraeche", []):
        msgs = [(ka_zeit(z), w, t) for z, w, t in g["msgs"]]
        leute.append({"name": g["name"], "plattform": "Kleinanzeigen", "telefon": "", "status": g.get("status", ""), "msgs": msgs})
    for p in leute:
        p["msgs"].sort(key=lambda m: m[0])
        p["b"] = bew.get(p["name"], UNBEWERTET)
        p["id"] = "p" + re.sub(r"\W+", "", p["name"].lower())
    leute.sort(key=lambda p: (p["b"]["rang"], -p["msgs"][-1][0].timestamp()))
    return leute


def zeitfmt(z):
    return z.strftime("%d.%m. %H:%M")


def badge(p):
    b = p["b"]
    return f'<span class="b c-{b["chance"]}">{CHANCEN[b["chance"]]}</span>'


def verlauf(p):
    zeilen = "".join(
        f'<li class="{"ich" if w == "ich" else ""}"><time>{zeitfmt(z)}</time><span>{"Ich: " if w == "ich" else ""}{html.escape(t) or "(kein Text, evtl. Anhang)"}</span></li>'
        for z, w, t in p["msgs"]
    )
    return f"<ul>{zeilen}</ul>"


def tel_html(p):
    if not p["telefon"]:
        return ""
    nummer = re.sub(r"[^\d+]", "", p["telefon"])
    return f'<a class="tel" href="tel:{nummer}">{html.escape(p["telefon"])}</a>'


def detail(p):
    b = p["b"]
    plattform = f'<span class="b">{html.escape(p["plattform"])}</span>'
    status = f'<span class="b">{html.escape(p["status"])}</span>' if p["status"] else ""
    return (
        f'<section class="tab" id="t-{p["id"]}"><header><h2>{html.escape(p["name"])}</h2><div class="bl">{plattform}{badge(p)}{status}</div></header>'
        f'<dl><dt>Angebot</dt><dd>{html.escape(b["angebot"])}</dd><dt>Einschätzung</dt><dd>{html.escape(b["grund"])}</dd>'
        f'<dt>Nächster Schritt</dt><dd>{html.escape(b["schritt"])}</dd></dl>{tel_html(p)}{verlauf(p)}</section>'
    )


def seite(gespraeche, ka=None, bew=None):
    ka = ka or {}
    bew = bew or {}
    leute = personen(gespraeche, ka, bew)
    aktiv = [p for p in leute if p["b"]["chance"] != "erledigt"]
    heiss = [p for p in leute if p["b"]["chance"] == "hoch"]
    mit_preis = [p for p in leute if re.search(r"\d", p["b"]["angebot"])]

    zeilen = ""
    for i, p in enumerate(leute, 1):
        b = p["b"]
        z, w, t = p["msgs"][-1]
        letzte = ("Ich: " if w == "ich" else "") + t
        if len(letzte) > 110:
            letzte = letzte[:107] + "..."
        zeilen += (
            f'<a class="zeile e-{b["chance"]}" href="#{p["id"]}"><span class="nr">{i}</span>'
            f'<div class="zk"><div class="zt"><strong>{html.escape(p["name"])}</strong> <span class="b">{html.escape(p["plattform"])}</span> {badge(p)}'
            f'<span class="preis">{html.escape(b["angebot"])}</span></div>'
            f'<div class="zg">{html.escape(b["grund"])}</div>'
            f'<div class="zs"><b>Jetzt:</b> {html.escape(b["schritt"])}</div>'
            f'<div class="zl"><time>{zeitfmt(z)}</time> {html.escape(letzte)}</div></div></a>'
        )

    alle = sorted(((z, p, w, t) for p in leute for z, w, t in p["msgs"]), key=lambda x: x[0], reverse=True)
    feed = "".join(
        f'<li class="{"ich" if w == "ich" else ""}"><time>{zeitfmt(z)}</time><span><a href="#{p["id"]}">{html.escape(p["name"])}</a> '
        f'<small>{html.escape(p["plattform"])}</small><br>{"Ich: " if w == "ich" else ""}{html.escape(t) or "(kein Text, evtl. Anhang)"}</span></li>'
        for z, p, w, t in alle
    )

    tabs = '<a class="tabl" href="#alle" data-t="alle">Alle</a>' + "".join(
        f'<a class="tabl" href="#{p["id"]}" data-t="{p["id"]}"><i class="d d-{p["b"]["chance"]}"></i>{html.escape(p["name"])}</a>' for p in leute
    )
    details = "".join(detail(p) for p in leute)
    leer = '<p class="leer">Noch keine Anfragen eingegangen.</p>' if not leute else ""
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="300"><title>Golf Anfragen</title>
<style>
:root{{--bg:#f6f5f2;--card:#fff;--text:#1d1d1b;--mut:#6b6b66;--line:#e4e2dc;--acc:#1f5fbf;--hoch:#1c7a45;--mittel:#c77d00;--niedrig:#b3402f;--erl:#8a8a84}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161615;--card:#212120;--text:#eeede8;--mut:#a09f98;--line:#33332f;--acc:#7aa7f0;--hoch:#4cc283;--mittel:#e0a030;--niedrig:#e57868;--erl:#7a7a74}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif}}
main{{max-width:820px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-size:1.6rem;margin:0 0 4px}}.sub{{color:var(--mut);margin:0 0 18px}}
.zahlen{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}}
.zahlen div{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 16px;min-width:110px}}
.zahlen strong{{display:block;font-size:1.5rem;line-height:1.1}}.zahlen span{{color:var(--mut);font-size:.82rem}}
.tabs{{display:flex;gap:6px;overflow-x:auto;padding-bottom:8px;margin-bottom:14px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:2}}
.tabl{{white-space:nowrap;text-decoration:none;color:var(--text);padding:6px 12px;border-radius:99px;border:1px solid var(--line);background:var(--card);font-size:.9rem}}
.tabl.on{{background:var(--acc);border-color:var(--acc);color:#fff}}
.d{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;background:var(--erl)}}
.d-hoch{{background:var(--hoch)}}.d-mittel{{background:var(--mittel)}}.d-niedrig{{background:var(--niedrig)}}.tabl.on .d{{box-shadow:0 0 0 1.5px #fff}}
.tab{{display:none}}.tab.on{{display:block}}
.zeile{{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--erl);border-radius:12px;padding:12px 14px;margin-bottom:10px;text-decoration:none;color:inherit}}
.zeile.e-hoch{{border-left-color:var(--hoch)}}.zeile.e-mittel{{border-left-color:var(--mittel)}}.zeile.e-niedrig{{border-left-color:var(--niedrig)}}.zeile.e-erledigt{{opacity:.6}}
.nr{{color:var(--mut);font-weight:700;min-width:1.2rem}}.zk{{flex:1;min-width:0}}
.zt{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}.preis{{margin-left:auto;font-weight:600}}
.zg{{color:var(--mut);font-size:.9rem;margin-top:4px}}.zs{{font-size:.9rem;margin-top:4px}}
.zl{{font-size:.82rem;color:var(--mut);margin-top:6px;border-top:1px solid var(--line);padding-top:6px}}
article,section.tab.on{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px}}
header{{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap}}
h2{{font-size:1.15rem;margin:0}}h3{{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:22px 0 10px}}
.bl{{display:flex;gap:6px;flex-wrap:wrap}}
.b{{font-size:.75rem;padding:2px 9px;border-radius:99px;border:1px solid var(--line);color:var(--mut);white-space:nowrap}}
.b.c-hoch{{border-color:var(--hoch);color:var(--hoch)}}.b.c-mittel{{border-color:var(--mittel);color:var(--mittel)}}.b.c-niedrig{{border-color:var(--niedrig);color:var(--niedrig)}}
dl{{display:grid;grid-template-columns:130px 1fr;gap:6px 12px;margin:14px 0}}dt{{color:var(--mut);font-size:.85rem}}dd{{margin:0}}
.tel{{display:inline-block;margin:2px 0 4px;color:var(--acc);text-decoration:none;font-weight:600}}
ul{{list-style:none;margin:10px 0 0;padding:0}}li{{display:flex;gap:12px;padding:6px 0;border-top:1px solid var(--line)}}
time{{color:var(--mut);font-size:.82rem;min-width:84px;padding-top:2px}}li span{{flex:1}}li.ich span{{color:var(--mut)}}
li a{{color:var(--acc);font-weight:600;text-decoration:none}}li small{{color:var(--mut)}}
.leer,.fuss{{color:var(--mut);font-size:.85rem}}
@media(max-width:560px){{dl{{grid-template-columns:1fr}}.preis{{margin-left:0}}}}
</style></head><body><main>
<h1>VW Golf 6, Anfragen</h1>
<p class="sub">mobile.de und Kleinanzeigen, sortiert nach realistischer Kaufchance (meine Einschätzung). Anzeigenpreis 5.500 € VB. Stand {datetime.now().strftime("%d.%m.%Y %H:%M")}; Kleinanzeigen-Stand {html.escape(ka.get("stand", "?"))}</p>
<div class="zahlen"><div><strong>{len(leute)}</strong><span>Interessenten</span></div>
<div><strong>{len(aktiv)}</strong><span>noch offen</span></div>
<div><strong>{len(heiss)}</strong><span>Chance hoch</span></div>
<div><strong>{len(mit_preis)}</strong><span>mit Preisangebot</span></div></div>
<nav class="tabs">{tabs}</nav>
<section class="tab" id="t-alle">
<h3>Rangliste nach Chance</h3>{zeilen}{leer}
<h3>Alle Nachrichten, neueste zuerst</h3><article><ul style="margin-top:0">{feed}</ul></article>
</section>
{details}
<p class="fuss">mobile.de wird automatisch aus dem web.de-Postfach gelesen (nur lesend), Kleinanzeigen von Hand aus Chrome übernommen. Antworten läuft über die Portale. Die Einschätzung steht in kleinanzeigen.json unter „bewertungen“.</p>
</main>
<script>
function zeige(){{var h=(location.hash||"#alle").slice(1);if(!document.getElementById("t-"+h))h="alle";
document.querySelectorAll(".tab").forEach(function(e){{e.classList.toggle("on",e.id==="t-"+h)}});
document.querySelectorAll(".tabl").forEach(function(e){{e.classList.toggle("on",e.dataset.t===h)}});window.scrollTo(0,0)}}
addEventListener("hashchange",zeige);zeige();
</script></body></html>"""


def main():
    g = holen()
    ka = {}
    bew = {}
    if os.path.exists(KA_JSON):
        import json
        ka = json.load(open(KA_JSON, encoding="utf-8"))
        bew = ka.get("bewertungen", {})
        # Anfragen von Kleinanzeigen, die auch als Mail kamen, stehen schon im Kleinanzeigen-Teil
        g = [x for x in g if x["plattform"] != "Kleinanzeigen"]
    os.makedirs(os.path.dirname(AUSGABE), exist_ok=True)
    with open(AUSGABE, "w", encoding="utf-8") as f:
        f.write(seite(g, ka, bew))
    print(f"{len(g)} Interessenten per Mail, Datei: {AUSGABE}")
    if "--text" in sys.argv:
        for x in g:
            print(f"- {x['name']} ({x['plattform']}), {len(x['msgs'])} Nachrichten, zuletzt {lokal(x['msgs'][-1][0])}")


if __name__ == "__main__":
    main()
