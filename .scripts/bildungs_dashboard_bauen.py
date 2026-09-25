#!/usr/bin/env python3
"""Baut 04 Ressourcen/Bildungs-Dashboard.html (Physik 7c/10, Mathematik, Sport) mit Stunden-Status.

Aufruf: python3 .scripts/bildungs_dashboard_bauen.py
Status je Stunde (geplant/vorbereitet/gehalten) setzt Oskar per Klick im Browser (localStorage, pro Browser).
Die Startwerte stehen unten in PHYSIK/MATHE_STUNDEN und werden bei neuen Stunden hier ergänzt.
Mathematik-Pools und Sport kommen aus bildung_daten_mathe_sport.json (übernommen aus dem alten Dashboard.html).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "04 Ressourcen"
DATEN = json.loads((Path(__file__).parent / "bildung_daten_mathe_sport.json").read_text(encoding="utf-8"))

# Link: ("f", Beschriftung, relativer Pfad ab 04 Ressourcen)  oder  ("o", Beschriftung, Notiz ohne .md ab Vault-Wurzel)
def f(l, p): return ["f", l, p]
def o(l, p): return ["o", l, p]

PH = "Physik/"
PHYSIK = [
    {"klasse": "7c", "untertitel": "Optik, Akustik · 2 Wochenstunden, Do Doppelstunde", "themen": [
        {"titel": "Optik", "stunden": [
            {"id": "ph7-optik1", "titel": "Optik 1 – Lichtquellen und beleuchtete Körper", "wann": "", "status": "gehalten",
             "links": [f("Stunde", PH + "Optik/Optik 1 – Lichtquellen und beleuchtete Körper – ALLES.html")]},
            {"id": "ph7-optik2", "titel": "Optik 2 – Licht trifft auf einen Körper", "wann": "Do 24.09.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik – Do 24.09. – Stunde.html"), f("Übersicht", PH + "Optik/Optik 2 – Licht trifft auf einen Körper – ALLES.html")]},
            {"id": "ph7-lf3", "titel": "Leitfrage 3", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik – Leitfrage 3 – Stunde.html")]},
            {"id": "ph7-lf4", "titel": "Leitfrage 4", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik – Leitfrage 4 – Stunde.html")]},
            {"id": "ph7-lf5", "titel": "Leitfrage 5 – Mondphasen und Finsternisse", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik – Leitfrage 5 – Stunde.html")]},
            {"id": "ph7-lochkamera", "titel": "Lochkamera und Rückblick", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik – Lochkamera – Stunde.html")]},
            {"id": "ph7-o2-reflexion", "titel": "Optik II – Reflexionsgesetz", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik II – Reflexionsgesetz – Stunde.html")]},
            {"id": "ph7-o2-spiegelbild", "titel": "Optik II – Spiegelbild", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik II – Spiegelbild – Stunde.html")]},
            {"id": "ph7-o2-brechung", "titel": "Optik II – Lichtbrechung", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik II – Lichtbrechung – Stunde.html")]},
            {"id": "ph7-o2-linsen", "titel": "Optik II – Linsen", "wann": "", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Optik/Optik II – Linsen – Stunde.html")]},
        ], "material": [
            {"titel": "Optik-Labore (Startseite für IServ)", "links": [f("öffnen", PH + "Optik/Optik-Labore.html")]},
            {"titel": "Foliensatz Optik I", "links": [f("HTML", PH + "Optik/Optik I.html"), f("PDF", PH + "Optik/Optik I.pdf")]},
            {"titel": "Foliensatz Optik II", "links": [f("HTML", PH + "Optik/Optik II.html"), f("PDF", PH + "Optik/Optik II.pdf")]},
        ]},
        {"titel": "Akustik", "stunden": [
            {"id": "ph7-akustik", "titel": "Akustik (Leitfragen 10–12, E-Niveau)", "wann": "", "status": "geplant",
             "links": [f("Folien", PH + "Akustik/Akustik.html"), f("PDF", PH + "Akustik/Akustik.pdf")]},
        ], "material": []},
        {"titel": "Planung und Nachschlagen", "stunden": [], "material": [
            {"titel": "Physik-Dashboard Klasse 7 (Nachschlagewerk)", "links": [f("öffnen", PH + "Physik Dashboard.html")]},
            {"titel": "Stoffverteilungsplan Klasse 7", "links": [o("Obsidian", "04 Ressourcen/Physik/Stoffverteilungsplan Physik Klasse 7 2026-27")]},
            {"titel": "Jahresplanung Klasse 7", "links": [o("Obsidian", "04 Ressourcen/Physik/Jahresplanung Physik Klasse 7 2026-27")]},
            {"titel": "Rahmendaten Schuljahr 2026/27", "links": [o("Obsidian", "04 Ressourcen/Physik/Rahmendaten Schuljahr 2026-27")]},
        ]},
    ]},
    {"klasse": "10", "untertitel": "Kernphysik", "themen": [
        {"titel": "Kernphysik", "stunden": [
            {"id": "ph10-w01", "titel": "W01 – Woraus besteht Materie?", "wann": "Woche ab 14.09.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W01 Woraus besteht Materie – Stunde.html")]},
            {"id": "ph10-w02", "titel": "W02 – Atombau und Isotope", "wann": "Woche ab 21.09.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W02 Atombau und Isotope – Stunde.html")]},
            {"id": "ph10-w03", "titel": "W03 – Zählrohr und Nullrate", "wann": "Woche ab 28.09.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W03 Zaehlrohr und Nullrate – Stunde.html")]},
            {"id": "ph10-w04", "titel": "W04 – Alpha, Beta und Gamma", "wann": "Woche ab 05.10.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W04 Alpha Beta Gamma – Stunde.html")]},
            {"id": "ph10-w05", "titel": "W05 – Zerfallsgleichungen und Durchdringung", "wann": "Woche ab 12.10.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W05 Zerfallsgleichungen – Stunde.html")]},
            {"id": "ph10-w06", "titel": "W06 – Der Zufall beim Zerfall", "wann": "Woche ab 19.10.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W06 Wuerfelmodell – Stunde.html")]},
            {"id": "ph10-w07", "titel": "W07 – Die Halbwertszeit", "wann": "Woche ab 02.11.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W07 Halbwertszeit – Stunde.html")]},
            {"id": "ph10-w08", "titel": "W08 – Aktivität und Zählrate", "wann": "Woche ab 09.11.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W08 Aktivitaet – Stunde.html")]},
            {"id": "ph10-w09", "titel": "W09 – Übungen zur Halbwertszeit", "wann": "Woche ab 16.11.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W09 Uebungen Halbwertszeit – Stunde.html")]},
            {"id": "ph10-w12", "titel": "W12 – Ionisierende Strahlung", "wann": "Woche ab 07.12.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W12 Ionisierende Strahlung – Stunde.html")]},
            {"id": "ph10-w13", "titel": "W13 – Wirkung auf den Körper", "wann": "Woche ab 14.12.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W13 Wirkung auf den Koerper – Stunde.html")]},
            {"id": "ph10-w15", "titel": "W15 – Schutz und Anwendungen", "wann": "Woche ab 11.01.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W15 Schutz und Anwendungen – Stunde.html")]},
            {"id": "ph10-w16", "titel": "W16 – Die Kernspaltung", "wann": "Woche ab 18.01.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W16 Kernspaltung – Stunde.html")]},
            {"id": "ph10-w17", "titel": "W17 – Kettenreaktion und Reaktor", "wann": "Woche ab 25.01.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W17 Kettenreaktion – Stunde.html")]},
            {"id": "ph10-w18", "titel": "W18 – Kernkraftwerk und Kernfusion", "wann": "Woche ab 01.02.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W18 Kraftwerk und Fusion – Stunde.html")]},
            {"id": "ph10-w19", "titel": "W19 – Leitfrage 5 abschließen", "wann": "Woche ab 15.02.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W19 Uebungen Kernenergie – Stunde.html")]},
            {"id": "ph10-w20", "titel": "W20 – Wohin mit dem Abfall?", "wann": "Woche ab 22.02.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W20 Radioaktiver Abfall – Stunde.html")]},
            {"id": "ph10-w21", "titel": "W21 – Nutzen und Risiko abwägen", "wann": "Woche ab 01.03.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W21 Argumente abwaegen – Stunde.html")]},
            {"id": "ph10-w22", "titel": "W22 – Rückblick und Altersbestimmung", "wann": "Woche ab 08.03.", "status": "vorbereitet",
             "links": [f("Stunde", PH + "Kernphysik/Kernphysik – W22 Rueckblick und C-14 – Stunde.html")]},
            {"id": "ph10-folien", "titel": "Foliensatz Kernphysik (alle 71 Folien)", "wann": "", "status": "vorbereitet",
             "links": [f("HTML", PH + "Kernphysik/Kernphysik.html")]},
        ], "material": [
            {"titel": "Kernphysik-Labore (Startseite für IServ)", "links": [f("öffnen", PH + "Kernphysik/Kernphysik-Labore.html")]},
            {"titel": "Atomlabor", "links": [f("öffnen", PH + "Kernphysik/Atomlabor Atombau und Isotope.html")]},
            {"titel": "Strahlungslabor", "links": [f("öffnen", PH + "Kernphysik/Strahlungslabor Radioaktivitaet.html")]},
            {"titel": "Zerfallslabor", "links": [f("öffnen", PH + "Kernphysik/Zerfallslabor Halbwertszeit.html")]},
            {"titel": "Wirkungslabor", "links": [f("öffnen", PH + "Kernphysik/Wirkungslabor Strahlung und Koerper.html")]},
            {"titel": "Kernenergielabor", "links": [f("öffnen", PH + "Kernphysik/Kernenergielabor Spaltung und Fusion.html")]},
            {"titel": "Stoffverteilungsplan Klasse 10", "links": [o("Obsidian", "04 Ressourcen/Physik/Stoffverteilungsplan Physik Klasse 10 2026-27")]},
        ]},
    ]},
    {"klasse": "Alle Klassen (7–10)", "untertitel": "Klassenübergreifend", "themen": [
        {"titel": "Werkzeuge und Material", "stunden": [], "material": [
            {"titel": "Physik MC-Generator (Klasse 7–10)", "links": [f("öffnen", PH + "Prüfungsaufgaben/Physik MC Generator.html")]},
            {"titel": "Kinematik: Wasserrakete (Merkheft)", "links": [f("öffnen", PH + "Kinematik/Wasserrakete (Merkheft).html")]},
            {"titel": "Elektrizitätslehre: UND-ODER-Schaltung", "links": [f("öffnen", PH + "Elektrizitätslehre/UND-ODER-Schaltung.html")]},
            {"titel": "Kinematik: E-Scooter-Versuch, Bewegungsdiagramme", "links": [f("PDF", PH + "Kinematik/E-Scooter Versuch – Bewegungsdiagramme.pdf")]},
            {"titel": "Physik (Themenübersicht)", "links": [o("Obsidian", "04 Ressourcen/Physik/Physik")]},
        ]},
    ]},
]

RZ = "Mathematik/Rationale Zahlen/"
MATHE_STUNDEN = [{"klasse": "7c", "untertitel": "Rationale Zahlen", "themen": [{"titel": "Rationale Zahlen", "stunden": [
    {"id": "ma7-rz1", "titel": "Rationale Zahlen 1 – Zahlen unter Null", "wann": "Di 22.09.", "status": "gehalten",
     "links": [f("Stunde", RZ + "Rationale Zahlen 1 – Zahlen unter Null – ALLES.html"), f("Folien", RZ + "Folien – Zahlen unter Null.pdf")]},
    {"id": "ma7-rz2", "titel": "Rationale Zahlen 2 – Addieren und Subtrahieren", "wann": "Mi 23. und Do 24.09.", "status": "vorbereitet",
     "links": [f("Stunde", RZ + "Rationale Zahlen 2 – Addieren und Subtrahieren – ALLES.html"),
               f("Folien", RZ + "Rationale Zahlen 2 – Folien für den Beamer.pdf"),
               f("Arbeitsblatt", RZ + "Rationale Zahlen 2 – Arbeitsblatt Plus und Minus.pdf"),
               f("Lösungen", RZ + "Rationale Zahlen 2 – Arbeitsblatt Plus und Minus – Lösungen (nur für mich).pdf")]},
], "material": []}]}]

CSS = """
:root{--ink:#1f2937;--sub:#5b6572;--accent:#2563a8;--bg:#eef1f5;--card:#fff;--line:#e2e5ea;--chip:#eaf1fb}
*{box-sizing:border-box}body{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg);margin:0;padding:28px 24px 60px;line-height:1.4}
.wrap{max-width:1180px;margin:0 auto}h1{font-size:28px;margin:0 0 4px}.subtitle{color:var(--sub);font-size:15px;margin:0 0 18px}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}
.tabs button{font:inherit;font-size:15px;border:1px solid var(--line);background:#fff;padding:8px 18px;border-radius:20px;cursor:pointer;color:var(--ink)}
.tabs button.on{background:var(--accent);border-color:var(--accent);color:#fff}
.tab{display:none}.tab.on{display:block}
.klasse{margin:0 0 30px}.klasse>h2{font-size:21px;margin:0 0 2px}.klasse>.ut{color:var(--sub);font-size:14px;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:18px;align-items:start}
.card{background:var(--card);border-radius:14px;padding:18px 20px 12px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.card h3{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--accent);margin:0 0 10px}
.st{padding:10px 0;border-top:1px solid var(--line)}.st:first-of-type{border-top:0}
.st .kopf{display:flex;align-items:flex-start;gap:10px}.st .t{flex:1;font-size:14.5px;font-weight:600}
.st .w{color:var(--sub);font-size:12.5px;font-weight:400;display:block}
.badge{font:inherit;font-size:12px;font-weight:600;border:0;border-radius:12px;padding:3px 11px;cursor:pointer;white-space:nowrap}
.b-geplant{background:#eceef1;color:#5b6572}.b-vorbereitet{background:#dbe8f8;color:#1a56a0}.b-gehalten{background:#dcf1dc;color:#1d6b1d}
.links{display:flex;flex-wrap:wrap;gap:6px;margin-top:7px}
a.lk{font-size:13px;text-decoration:none;color:var(--accent);background:var(--chip);padding:3px 11px;border-radius:12px}
a.lk:hover{background:#d5e4f8}
.mat{padding:8px 0;border-top:1px solid var(--line)}.mat:first-of-type{border-top:0}.mat .t{font-size:14px}
.zaehler{color:var(--sub);font-size:13px;margin:0 0 14px}
.reset{font:inherit;font-size:12px;color:var(--sub);background:none;border:0;cursor:pointer;text-decoration:underline}
a.tool{display:flex;gap:8px;padding:8px 10px;border-radius:8px;text-decoration:none;color:var(--ink);font-size:14px}a.tool:hover{background:var(--chip)}
.desc{font-size:12.5px;color:var(--sub);margin:4px 0 6px}
footer{margin-top:30px;color:var(--sub);font-size:12px}
"""

JS = r"""
const VAULT = "Second Brain Claude";
const obs = p => "obsidian://open?vault=" + encodeURIComponent(VAULT) + "&file=" + encodeURIComponent(p);
const enc = p => p.split("/").map(encodeURIComponent).join("/");
const hrefOf = l => l[0] === "o" ? obs(l[2]) : enc(l[2]);
const ORDER = ["geplant", "vorbereitet", "gehalten"];
let saved = {};
try { saved = JSON.parse(localStorage.getItem("bildung-status-v1") || "{}"); } catch (e) {}
const stat = s => saved[s.id] || s.status;
function speichern() { try { localStorage.setItem("bildung-status-v1", JSON.stringify(saved)); } catch (e) {} }
const links = ls => ls.map(l => `<a class="lk" href="${hrefOf(l)}"${l[0] === "f" ? ' target="_blank"' : ""}>${l[1]}</a>`).join("");
function stunde(s) {
  const st = stat(s);
  return `<div class="st"><div class="kopf"><div class="t">${s.titel}${s.wann ? `<span class="w">${s.wann}</span>` : ""}</div>` +
    `<button class="badge b-${st}" data-id="${s.id}" title="Klick: Status wechseln">${st}</button></div><div class="links">${links(s.links)}</div></div>`;
}
function klasse(k) {
  const cards = k.themen.map(t => {
    const st = t.stunden.map(stunde).join("");
    const mt = t.material.map(m => `<div class="mat"><div class="t">${m.titel}</div><div class="links">${links(m.links)}</div></div>`).join("");
    return `<div class="card"><h3>${t.titel}</h3>${st}${mt}</div>`;
  }).join("");
  return `<div class="klasse"><h2>${k.klasse}</h2><p class="ut">${k.untertitel}</p><div class="grid">${cards}</div></div>`;
}
function zaehler(data) {
  const alle = data.flatMap(k => k.themen.flatMap(t => t.stunden));
  const n = s => alle.filter(x => stat(x) === s).length;
  return `<p class="zaehler">${n("gehalten")} gehalten · ${n("vorbereitet")} vorbereitet · ${n("geplant")} geplant</p>`;
}
function render() {
  document.getElementById("t-physik").innerHTML = zaehler(D.physik) + D.physik.map(klasse).join("");
  document.getElementById("t-mathe").innerHTML = zaehler(D.mathe) + D.mathe.map(klasse).join("") +
    D.pools.Mathematik.map(c => poolcard(c)).join("");
  document.getElementById("t-sport").innerHTML = (D.pools.Sport || []).map(c => poolcard(c)).join("");
  document.querySelectorAll(".badge").forEach(b => b.onclick = () => {
    const id = b.dataset.id;
    const s = [...D.physik, ...D.mathe].flatMap(k => k.themen.flatMap(t => t.stunden)).find(x => x.id === id);
    saved[id] = ORDER[(ORDER.indexOf(stat(s)) + 1) % 3];
    speichern(); render();
  });
}
function poolcard(c) {
  const ls = c[2].map(l => `<a class="tool" href="${enc(l[1])}" target="_blank">${l[0]}</a>`).join("");
  return `<div class="klasse"><div class="card"><h3>${c[0]}</h3>${c[1] ? `<div class="desc">${c[1]}</div>` : ""}${ls}</div></div>`;
}
document.querySelectorAll(".tabs button").forEach(b => b.onclick = () => {
  document.querySelectorAll(".tabs button,.tab").forEach(x => x.classList.remove("on"));
  b.classList.add("on"); document.getElementById("t-" + b.dataset.tab).classList.add("on");
  try { localStorage.setItem("bildung-tab", b.dataset.tab); } catch (e) {}
});
document.getElementById("reset").onclick = () => { saved = {}; speichern(); render(); };
render();
let tab = "physik"; try { tab = localStorage.getItem("bildung-tab") || tab; } catch (e) {}
const tb = document.querySelector(`.tabs button[data-tab="${tab}"]`); if (tb) tb.click();
"""

daten = {"physik": PHYSIK, "mathe": MATHE_STUNDEN, "pools": DATEN}
html = f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bildungs-Dashboard</title><style>{CSS}</style></head><body><div class="wrap">
<h1>Bildungs-Dashboard</h1><p class="subtitle">Unterricht im Überblick: Stunden, Status und Material für Physik, Mathematik und Sport.</p>
<div class="tabs"><button data-tab="physik" class="on">⚛️ Physik</button><button data-tab="mathe">📐 Mathematik</button><button data-tab="sport">🏃 Sport</button></div>
<div id="t-physik" class="tab on"></div><div id="t-mathe" class="tab"></div><div id="t-sport" class="tab"></div>
<footer>Status: Klick auf das Label wechselt geplant → vorbereitet → gehalten, gespeichert nur in diesem Browser. <button class="reset" id="reset">Status zurücksetzen</button><br>
Neu bauen: python3 .scripts/bildungs_dashboard_bauen.py · Diese Datei liegt in 04 Ressourcen, damit die Links passen.</footer></div>
<script>const D = {json.dumps(daten, ensure_ascii=False)};{JS}</script></body></html>"""
ziel = RES / "Bildungs-Dashboard.html"
ziel.write_text(html, encoding="utf-8")
print("geschrieben:", ziel, f"({len(html) // 1024} KB)")
