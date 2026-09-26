#!/usr/bin/env python3
"""Materialliste Kernphysik Klasse 10: alles Material aus den Stunden W01 bis W22, als Gesamtliste und nach Stunden.
Liest die Materialtabellen aus baue_stunden_k10.py und baue_stunden_k10_teil2.py. Status (vorhanden, bestellen, bestellt)
lässt sich im Browser anklicken und bleibt im Browser gespeichert. Feste Vorgaben stehen unten in VORGABE.
Aufruf: python3 baue_material_k10.py  -> Kernphysik Klasse 10 – Material.html"""
import html, json, re, sys
from pathlib import Path

HIER = Path(__file__).parent
sys.path.insert(0, str(HIER))
import baue_stunden_k10 as t1  # noqa: E402
import baue_stunden_k10_teil2 as t2  # noqa: E402

# gleiche Dinge mit verschiedenen Namen zusammenführen
NAME = {"Luftballon, aufgeblasen": "Luftballon", "Wolltuch oder Wollpullover": "Wolltuch", "Präparatesatz": "Präparate α, β, γ"}

ART = [
    ("Präparate (nur Lehrkraft)", ["Präparate α, β, γ", "γ-Präparat"]),
    ("Geräte aus der Sammlung", ["Geiger-Müller-Zählrohr mit Zählgerät", "Elektroskop", "Nebelkammer", "Absorber: Papier, Aluminium 5 mm, Bleiplatten",
                                 "Messzylinder 250 ml", "Stoppuhr", "Lineal oder Maßband"]),
    ("Für die Gruppen", ["Würfel", "Würfelbecher oder Schale", "Dominosteine", "Wolltuch", "Lineal", "Lappen"]),
    ("Einkaufen, kurz vor der Stunde", ["Luftballon", "Malzbier", "Trockeneis", "Isopropanol", "Diätsalz (Kaliumchlorid)"]),
    ("Sonstiges", []),
]

# Stand, den Oskar genannt hat (status: v = vorhanden, n = nicht vorhanden, b = bestellen, o = bestellt). Alles andere steht auf „noch nicht geprüft“.
VORGABE = {"Nebelkammer": {"status": "n", "notiz": "zu teuer, wird nicht bestellt"},
            "Würfel": {"status": "o", "notiz": "500 Stück bestellt (09/2026)"}}

stunden = []
for datei, h1, sub, _d, mat, *_ in t1.STUNDEN:
    stunden.append((datei, h1, sub, mat))
for kurz, h1, sub, _b, mat, *_ in t2.STUNDEN:
    stunden.append((f"Kernphysik – {kurz} – Stunde.html", h1, "Klasse 10 · Physik · " + sub, mat))

liste = []
for datei, h1, sub, mat in stunden:
    w = re.search(r"W\d\d", sub).group(0)
    woche = re.search(r"Woche ab ([\d.]+)", sub).group(1)
    zeilen = []
    for rolle, key in (("demo", "demo"), ("gruppe", "schueler")):
        for name, anz, hinweis in mat.get(key, []):
            zeilen.append({"name": NAME.get(name, name), "anz": anz, "hinweis": hinweis, "rolle": rolle})
    liste.append({"w": w, "woche": woche, "titel": h1.replace("Kernphysik: ", ""), "datei": datei, "zeilen": zeilen, "hinweis": mat.get("hinweis", "")})
liste.sort(key=lambda s: s["w"])

art_von = {n: a for a, ns in ART for n in ns}
dinge = {}
for s in liste:
    for z in s["zeilen"]:
        d = dinge.setdefault(z["name"], {"name": z["name"], "art": art_von.get(z["name"], "Sonstiges"), "einsatz": []})
        d["einsatz"].append({"w": s["w"], "anz": z["anz"], "rolle": z["rolle"], "hinweis": z["hinweis"]})
ungeordnet = [n for n, d in dinge.items() if d["art"] == "Sonstiges"]
reihenfolge = {n: i for i, (_, ns) in enumerate(ART) for n in ns}
gesamt = sorted(dinge.values(), key=lambda d: ([a for a, _ in ART].index(d["art"]), reihenfolge.get(d["name"], 99), d["name"]))

daten = json.dumps({"stunden": liste, "dinge": gesamt, "arten": [a for a, _ in ART], "vorgabe": VORGABE}, ensure_ascii=False)

seite = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Material Kernphysik 10</title>
<style>
:root{--bg:#F4F6F9;--panel:#fff;--ink:#14171c;--muted:#66798E;--line:#D9DFE7;--accent:#2F5E9E;--sel:#E3EBF6;
--ok:#1E7B4C;--okbg:#E3F3EA;--no:#4A5563;--nobg:#E6E9EE;--buy:#B4232B;--buybg:#FBE6E7;--ord:#8A5A00;--ordbg:#FBF0D9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.4 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
header{background:var(--panel);border-bottom:1px solid var(--line);padding:14px 20px 0;position:sticky;top:0;z-index:2}
h1{font-size:19px;margin:0 0 2px}.sub{color:var(--muted);font-size:13px;margin:0 0 10px}
.zeile{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin-bottom:10px}
.tabs{display:flex;gap:2px}.tabs button{font:inherit;font-size:14px;border:0;background:none;padding:8px 14px;border-bottom:3px solid transparent;cursor:pointer;color:var(--muted)}
.tabs button.on{color:var(--ink);border-bottom-color:var(--accent);font-weight:600}
.zaehler span{display:inline-block;font-size:12px;padding:3px 9px;border-radius:99px;margin-right:4px}
label.gr{font-size:13px;color:var(--muted)}label.gr input{width:56px;font:inherit;padding:3px 6px;border:1px solid var(--line);border-radius:6px;margin-left:4px}
.filter button,.aktion{font:inherit;font-size:13px;border:1px solid var(--line);background:#fff;border-radius:7px;padding:5px 10px;cursor:pointer;color:var(--ink)}
.filter button.on{background:var(--sel);border-color:var(--accent)}
main{max-width:1100px;margin:0 auto;padding:16px 20px 40px}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:22px 0 6px}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden}
th{font-size:12px;text-align:left;color:var(--muted);font-weight:600;padding:7px 10px;border-bottom:1px solid var(--line);background:#FAFBFC}
td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:0}
td.name{font-weight:600;width:28%}td.name small,td small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.w{font:600 12px ui-monospace,Menlo,monospace;color:var(--accent);text-decoration:none;white-space:nowrap}.w:hover{text-decoration:underline}
.einsatz div{margin-bottom:3px}.rolle{font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:0 4px;margin:0 4px}
.bedarf{white-space:nowrap}
.st{display:flex;gap:4px;flex-wrap:nowrap}.st button{font:inherit;font-size:12px;border:1px solid var(--line);background:#fff;border-radius:99px;padding:3px 9px;cursor:pointer;color:var(--muted)}
.st button.on.v{background:var(--okbg);border-color:var(--ok);color:var(--ok)}.st button.on.b{background:var(--buybg);border-color:var(--buy);color:var(--buy)}
.st button.on.o{background:var(--ordbg);border-color:var(--ord);color:var(--ord)}.st button.on.n{background:var(--nobg);border-color:var(--no);color:var(--no)}
tr.n td.name{color:var(--no)}tr.n .nm{text-decoration:line-through;text-decoration-color:#9AA5B1}.ersatz{font-size:12px;color:var(--accent);margin-top:3px}
.notiz{width:100%;margin-top:5px;font:inherit;font-size:12px;border:1px solid transparent;border-radius:6px;padding:3px 6px;background:transparent;color:var(--ink)}
.notiz:hover,.notiz:focus{border-color:var(--line);background:#fff}.notiz::placeholder{color:#AAB5C2}
tr.v td.name{color:var(--ok)}tr.b td.name{color:var(--buy)}tr.o td.name{color:var(--ord)}
.karte{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:12px}
.karte h3{margin:0 0 6px;font-size:16px}.karte h3 .w{margin-right:8px}.karte .dat{font-size:12px;color:var(--muted);font-weight:400;margin-left:6px}
.karte .nichts{color:var(--muted);font-size:14px}.karte table{border-radius:6px}.karte .hin{font-size:13px;color:var(--muted);margin-top:8px}
.punkt{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;background:#C9D1DB}.punkt.v{background:var(--ok)}.punkt.b{background:var(--buy)}.punkt.o{background:#D99A1E}.punkt.n{background:var(--no)}
.leer{color:var(--muted);padding:20px 0}
[hidden]{display:none!important}
@media (max-width:700px){.st{flex-wrap:wrap}header{position:static}td.name{width:auto}table,tbody,tr,td{display:block}tr{border-bottom:1px solid var(--line)}td{border:0;padding:4px 10px}th{display:none}}
@media print{header .filter,header .tabs,.aktion,label.gr{display:none}header{position:static}.notiz{border:0}.st button:not(.on){display:none}}
</style></head><body>
<header>
<h1>Material Kernphysik Klasse 10</h1>
<p class="sub">Alles, was in den Stunden W01 bis W22 gebraucht wird. Status anklicken, er bleibt in diesem Browser gespeichert. Bei „nicht vorhanden“ steht der Ersatz aus der Stunde dabei.</p>
<div class="zeile"><div class="zaehler" id="zaehler"></div>
<label class="gr">Gruppen in der Klasse<input id="gruppen" type="number" min="1" max="20" placeholder="?"></label>
<div class="filter" id="filter"><button data-f="alle" class="on">Alle</button><button data-f="offen">Noch nicht geprüft</button><button data-f="n">Nicht vorhanden</button><button data-f="b">Bestellen</button></div>
<button class="aktion" id="kopieren">Bestellliste kopieren</button></div>
<div class="tabs"><button data-t="gesamt" class="on">Gesamtliste</button><button data-t="stunden">Nach Stunden</button></div>
</header>
<main><div id="gesamt"></div><div id="stunden" hidden></div></main>
<script>
const D=__DATEN__;
const ST=[["v","vorhanden"],["n","nicht vorhanden"],["b","bestellen"],["o","bestellt"]];
const KEY="k10-material";
let S={};try{S=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){S={}}
function zust(n){return S[n]||D.vorgabe[n]||{status:"",notiz:""}}
function setze(n,feld,wert){const z={...zust(n)};z[feld]=wert;S[n]=z;try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}
let filter="alle",gruppen=null;
try{gruppen=parseInt(localStorage.getItem(KEY+"-gruppen"))||null}catch(e){}
const esc=t=>String(t).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const stunde=w=>D.stunden.find(s=>s.w===w);
const link=w=>`<a class="w" href="${encodeURI(stunde(w).datei)}" target="_blank">${w}</a>`;
function bedarf(e){
  if(e.rolle==="demo") return esc(e.anz)+' <span class="rolle">vorne</span>';
  const m=e.anz.match(/(\\d+)/);
  let t=esc(e.anz.replace("×",""))+' pro Gruppe';
  if(m&&gruppen) t+=` · <b>${parseInt(m[1])*gruppen} gesamt</b>`;
  return t;
}
function status(n){const z=zust(n);return `<div class="st" data-n="${esc(n)}">${ST.map(([k,t])=>`<button class="${k}${z.status===k?" on":""}" data-k="${k}">${t}</button>`).join("")}</div>
<input class="notiz" data-n="${esc(n)}" placeholder="Notiz, z. B. wo es steht" value="${esc(z.notiz||"")}">`}
function passt(n){const s=zust(n).status;return filter==="alle"||(filter==="offen"&&!s)||filter===s}
function gesamt(){
  let h="";
  for(const art of D.arten){
    const xs=D.dinge.filter(d=>d.art===art&&passt(d.name)); if(!xs.length) continue;
    h+=`<h2>${esc(art)}</h2><table><tr><th>Material</th><th>Wann und wie viel</th><th style="width:350px">Status</th></tr>`;
    for(const d of xs){
      const ein=d.einsatz.map(e=>`<div>${link(e.w)} <span class="bedarf">${bedarf(e)}</span>${e.hinweis?`<small>${esc(e.hinweis)}</small>`:""}</div>`).join("");
      const ers=zust(d.name).status==="n"?[...new Set(d.einsatz.map(e=>stunde(e.w)).filter(s=>/^Ohne/.test(s.hinweis)).map(s=>s.w+": "+s.hinweis))]:[];
      h+=`<tr class="${zust(d.name).status}"><td class="name"><span class="nm">${esc(d.name)}</span>${ers.map(x=>`<div class="ersatz">${esc(x)}</div>`).join("")}</td><td class="einsatz">${ein}</td><td>${status(d.name)}</td></tr>`;
    }
    h+="</table>";
  }
  document.getElementById("gesamt").innerHTML=h||'<p class="leer">Nichts in diesem Filter.</p>';
}
function stunden(){
  let h="";
  for(const s of D.stunden){
    const zs=s.zeilen.filter(z=>passt(z.name));
    if(filter!=="alle"&&!zs.length) continue;
    h+=`<div class="karte"><h3>${link(s.w)}${esc(s.titel)}<span class="dat">Woche ab ${esc(s.woche)}</span></h3>`;
    if(!s.zeilen.length) h+='<div class="nichts">Kein Material, nur Folien und Tafel.</div>';
    else{
      h+='<table><tr><th>Material</th><th>Anzahl</th><th style="width:350px">Status</th></tr>';
      for(const z of zs) h+=`<tr class="${zust(z.name).status}"><td class="name"><span class="punkt ${zust(z.name).status}"></span><span class="nm">${esc(z.name)}</span>${z.hinweis?`<small>${esc(z.hinweis)}</small>`:""}</td><td class="bedarf">${bedarf(z)}</td><td>${status(z.name)}</td></tr>`;
      h+="</table>";
    }
    if(s.hinweis) h+=`<div class="hin">${esc(s.hinweis)}</div>`;
    h+="</div>";
  }
  document.getElementById("stunden").innerHTML=h||'<p class="leer">Nichts in diesem Filter.</p>';
}
function zaehler(){
  const c={v:0,n:0,b:0,o:0,"":0};D.dinge.forEach(d=>c[zust(d.name).status||""]++);
  document.getElementById("zaehler").innerHTML=`<span style="background:#EEF1F5">${D.dinge.length} Dinge</span><span style="background:var(--okbg);color:var(--ok)">${c.v} vorhanden</span><span style="background:var(--nobg);color:var(--no)">${c.n} nicht vorhanden</span><span style="background:var(--buybg);color:var(--buy)">${c.b} bestellen</span><span style="background:var(--ordbg);color:var(--ord)">${c.o} bestellt</span><span style="background:#EEF1F5;color:var(--muted)">${c[""]} nicht geprüft</span>`;
}
function alles(){gesamt();stunden();zaehler()}
document.addEventListener("click",e=>{
  const b=e.target.closest(".st button");
  if(b){const n=b.parentElement.dataset.n;setze(n,"status",zust(n).status===b.dataset.k?"":b.dataset.k);alles();return}
  const t=e.target.closest(".tabs button");
  if(t){document.querySelectorAll(".tabs button").forEach(x=>x.classList.toggle("on",x===t));
    document.getElementById("gesamt").hidden=t.dataset.t!=="gesamt";document.getElementById("stunden").hidden=t.dataset.t!=="stunden";
    try{localStorage.setItem(KEY+"-tab",t.dataset.t)}catch(e){};return}
  const f=e.target.closest(".filter button");
  if(f){filter=f.dataset.f;document.querySelectorAll(".filter button").forEach(x=>x.classList.toggle("on",x===f));alles()}
});
document.addEventListener("change",e=>{if(e.target.classList.contains("notiz")){setze(e.target.dataset.n,"notiz",e.target.value);alles()}});
const gi=document.getElementById("gruppen");if(gruppen)gi.value=gruppen;
gi.addEventListener("input",()=>{gruppen=parseInt(gi.value)||null;try{localStorage.setItem(KEY+"-gruppen",gruppen||"")}catch(e){};alles()});
document.getElementById("kopieren").onclick=async()=>{
  const xs=D.dinge.filter(d=>zust(d.name).status==="b");
  const txt=xs.length?"Bestellen für Kernphysik Klasse 10:\\n"+xs.map(d=>"- "+d.name+" ("+d.einsatz.map(e=>e.w+": "+e.anz.replace("×","")+(e.rolle==="gruppe"?(gruppen&&/\\d/.test(e.anz)?" pro Gruppe, "+parseInt(e.anz.match(/\\d+/)[0])*gruppen+" gesamt":" pro Gruppe"):"")).join("; ")+")"+(zust(d.name).notiz?" – "+zust(d.name).notiz:"")).join("\\n"):"Nichts auf „bestellen“ gesetzt.";
  try{await navigator.clipboard.writeText(txt);document.getElementById("kopieren").textContent="Kopiert"}catch(e){prompt("Zum Kopieren:",txt)}
  setTimeout(()=>document.getElementById("kopieren").textContent="Bestellliste kopieren",1500);
};
try{const t=localStorage.getItem(KEY+"-tab");if(t==="stunden")document.querySelector('.tabs [data-t="stunden"]').click()}catch(e){}
alles();
</script></body></html>"""

ziel = HIER / "Kernphysik Klasse 10 – Material.html"
ziel.write_text(seite.replace("__DATEN__", daten), encoding="utf-8")
print("geschrieben:", ziel.name, "·", len(gesamt), "Dinge aus", sum(1 for s in liste if s["zeilen"]), "Stunden")
if ungeordnet:
    print("ohne Art (unter Sonstiges):", ungeordnet)
