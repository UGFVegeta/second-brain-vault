#!/usr/bin/env python3
# Sammelt alle Aufgaben aus den sechs Pool-HTMLs ein und baut Pruefung.html:
# ein themenübergreifender Prüfungssatz = 1 Aufgabe zum Wahlthema + 5 gemischte.
import os, re, json

BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik Prüfungsaufgaben"

pools = {
 "Trigonometrie Aufgabenpool.html": "Trigonometrie",
 "Quadratische Funktionen Aufgabenpool.html": "Quadratische Funktionen",
 "Stochastik Aufgabenpool.html": "Stochastik",
 "Sachrechnen Aufgabenpool.html": "Sachrechnen",
 "Boxplot Aufgabenpool.html": "Boxplot & Datenanalyse",
 "Stereometrie Aufgabenpool.html": "Stereometrie",
 "Kurzaufgaben Aufgabenpool.html": "Kurzaufgaben",
}

# Themen, die NICHT im zufälligen Prüfungssatz (Pruefung.html) auftauchen sollen
# (Kurzaufgaben sind nur Zeitfüller – im Baukasten aber wählbar).
EXAM_EXCLUDE = {"Kurzaufgaben"}

# Mathe-Darstellung (Wurzeln, Brüche, Box, Vergleichstabelle) für Pruefung/Baukasten
MATH_CSS_EXAM = """
 .kq{font-size:14px;font-weight:600;color:#1a1a1a}
 .kexpr{font-size:18px;text-align:center;margin:10px 0 2px;line-height:1.9}
 .rad{white-space:nowrap}
 .rad .rdc{border-top:1.6px solid currentColor;padding:1px 5px 0}
 .frac{display:inline-flex;flex-direction:column;text-align:center;vertical-align:middle;margin:0 4px}
 .frac .n{border-bottom:1.6px solid currentColor;padding:0 7px}
 .frac .d{padding:0 7px}
 .box{display:inline-block;width:15px;height:15px;border:1.6px solid #333;vertical-align:-2px;margin:0 3px}
 .kt{border-collapse:collapse;margin:10px auto 2px;font-size:14px}
 .kt td,.kt th{border:1px solid #c4ccd4;padding:4px 16px;text-align:center}
 .kt th{background:#eef2f6;font-weight:700}
 .kt td:first-child{text-align:left;font-weight:600}
 @media print{.ecard[data-topic="Trigonometrie"] .fig svg,.ecard[data-topic="Quadratische Funktionen"] .fig svg{max-height:108mm !important;max-width:100% !important}}
"""

def extract_sol(ch):
    """Inhalt des <div class="sol">…</div> einer Karte mit balancierter div-Zählung."""
    key = '<div class="sol">'
    i = ch.find(key)
    if i == -1:
        return ""
    j = i + len(key)
    depth = 1
    k = j
    while k < len(ch) and depth > 0:
        nd = ch.find('<div', k)
        cd = ch.find('</div>', k)
        if cd == -1:
            break
        if nd != -1 and nd < cd:
            depth += 1; k = nd + 4
        else:
            depth -= 1
            if depth == 0:
                return ch[j:cd].strip()
            k = cd + 6
    return ch[j:].strip()

DATA = []
for fn, topic in pools.items():
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        print("FEHLT:", fn); continue
    html = open(p).read()
    chunks = html.split('<div class="card"')
    cnt = 0
    for ch in chunks[1:]:
        mn = re.search(r'data-n="(\d+)"', ch)
        md = re.search(r'data-diff="(\d+)"', ch)
        if not mn:
            continue
        n = int(mn.group(1)); d = int(md.group(1)) if md else 0
        t0 = ch.find('<div class="top">')
        tend = ch.find('</div>', t0) + len('</div>')
        bend = ch.find('<button class="soltgl"')
        body = ch[tend:bend].strip() if (t0 != -1 and bend != -1) else ""
        sol = extract_sol(ch)
        DATA.append({"topic": topic, "n": n, "diff": d, "body": body, "sol": sol})
        cnt += 1
    print(f"{topic}: {cnt} Aufgaben")
print("gesamt:", len(DATA))

CSS = """
 *{box-sizing:border-box}
 body{font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0;padding:22px;background:#f4f6f7}
 h1{font-size:21px;margin:0 0 4px}
 .sub{color:#5b6569;font-size:13.5px;margin:0 0 16px;max-width:820px;line-height:1.5}
 .controls{position:sticky;top:0;background:#f4f6f7;padding:12px 0;border-bottom:1px solid #dde2e5;margin-bottom:18px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;z-index:5}
 select,button{font:inherit;font-size:13.5px;padding:9px 12px;border-radius:9px;border:1px solid #dde2e5;background:#fff;cursor:pointer}
 .lbl{font-size:13px;color:#5b6569;font-weight:700}
 button.primary{background:#0891b2;color:#fff;border-color:#0891b2;font-weight:700}
 button.primary:hover{background:#0e7490}
 #result{display:none}
 .chk{font-size:13px;color:#5b6569;display:flex;align-items:center;gap:6px;cursor:pointer}
 .avail{font-size:12.5px;color:#5b6569;margin-left:auto}
 .exset{margin-bottom:26px}
 .exset+.exset{border-top:2px dashed #c4ccd4;padding-top:18px}
 .settitle{font-size:16px;font-weight:700;margin:6px 0 6px}
 .nameline{font-size:13px;color:#333;margin:0 0 14px}
 .dstars{font-size:12px;color:#e8a800;letter-spacing:1px;margin-left:auto}
 .ecard{background:#fff;border:1.5px solid #dde2e5;border-radius:12px;padding:14px 16px;margin-bottom:16px;break-inside:avoid;page-break-inside:avoid}
 .ehead{display:flex;align-items:center;gap:10px;margin-bottom:6px}
 .enum{font-weight:700;font-size:15px}
 .etopic{font-size:12px;color:#5b6569;background:#eef3f7;border-radius:20px;padding:2px 10px}
 .wbadge{font-size:12px;font-weight:700;color:#fff;background:#0891b2;border-radius:20px;padding:2px 10px}
 .fig{display:flex;justify-content:center;align-items:center;padding:4px}.fig svg{display:block;max-width:100%;height:auto}
 .ges{font-size:14px;line-height:1.5;margin-top:6px}.ges b{color:#c0392b}
 .prob{font-size:15px;line-height:1.55;background:#f7fafd;border:1px solid #d3def0;border-radius:9px;padding:14px 16px;margin-top:4px}
 .data{margin-top:7px;font-size:13px;line-height:1.6;background:#fafbfc;border:1px solid #e4e8ec;border-radius:7px;padding:8px 10px}
 .dt{border-collapse:collapse;margin:6px 0;font-size:12.5px}.dt td,.dt th{border:1px solid #c4ccd4;padding:2px 9px;text-align:center}.dt th{background:#eef2f6}
 .solbox{margin-top:10px;background:#f1f9f3;border:1px solid #bcdcc3;border-radius:8px;padding:9px 12px;font-size:13px;line-height:1.5}
 .solbox .sl{font-weight:700;color:#1d8a4c;display:block;margin-bottom:3px}
 .solbox ul{margin:3px 0 0 18px;padding:0}
 @page{size:A4;margin:14mm}
 @media print{body{background:#fff;padding:0}.controls,.sub,h1{display:none!important}.ecard{border:1px solid #bbb;min-height:80mm}.fig svg{max-height:46mm}.exset{page-break-after:always}.exset:last-child{page-break-after:auto}.exset+.exset{border-top:none;padding-top:0}}
"""

JS = """
const DATA = __DATA__;
const TOPICS = __TOPICS__;
// Gleicher Speicher wie im Baukasten – dort markierte Aufgaben werden hier nicht mehr gezogen.
const KEY='mathe_pruefung_verwendet_v1';
let used=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
DATA.forEach(function(t){t.id=t.topic+'|'+t.n;});
function saveUsed(){localStorage.setItem(KEY,JSON.stringify(Array.from(used)));updAvail();}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function pick(a){return a[Math.floor(Math.random()*a.length)];}
// Schwierigkeitsziele für 6 Aufgaben: exakte Stufe oder ausgewogenes Profil
function targetsFor(prof){
 if(prof==='1'||prof==='2'||prof==='3'){const d=parseInt(prof);return [d,d,d,d,d,d];}
 if(prof==='mix')return [1,1,2,2,3,3];
 return null;
}
function takeTarget(targets,d){const i=targets.indexOf(d);if(i>=0)targets.splice(i,1);}
// Ein Satz: 1 Wahlthema-Aufgabe + 5 gemischte aus 5 VERSCHIEDENEN anderen Themen.
// Schwierigkeitsziele werden bevorzugt bedient, aber nie auf Kosten der Themen-Balance erzwungen.
function pickSet(pool,thema,prof){
 const targets=targetsFor(prof);
 const wahl=pool.filter(function(t){return t.topic===thema;});
 if(!wahl.length)return null;
 const wm=targets?wahl.filter(function(t){return targets.indexOf(t.diff)>=0;}):wahl;
 const first=pick(wm.length?wm:wahl);
 if(targets)takeTarget(targets,first.diff);
 const taken={};taken[first.id]=1;
 const rest=[];
 function grab(cands){
  const cm=targets?cands.filter(function(t){return targets.indexOf(t.diff)>=0;}):cands;
  const p=pick(cm.length?cm:cands);
  if(targets)takeTarget(targets,p.diff);
  rest.push(p);taken[p.id]=1;
 }
 shuffle(TOPICS.filter(function(x){return x!==thema;})).forEach(function(tp){
  if(rest.length>=5)return;
  const c=pool.filter(function(t){return t.topic===tp&&!taken[t.id];});
  if(c.length)grab(c);
 });
 while(rest.length<5){
  const c=pool.filter(function(t){return !taken[t.id];});
  if(!c.length)break;
  grab(c);
 }
 rest.sort(function(a,b){return a.diff-b.diff;});
 return [first].concat(rest);
}
let LAST=null;
function gen(){
 const thema=document.getElementById('thema').value;
 const prof=document.getElementById('diff').value;
 const num=parseInt(document.getElementById('num').value)||1;
 const skipUsed=document.getElementById('skipUsed').checked;
 let pool=DATA.filter(function(t){return !skipUsed||!used.has(t.id);});
 const sets=[];
 for(let s=0;s<num;s++){
  const set=pickSet(pool,thema,prof);
  if(!set){
   if(!sets.length){alert('Im Wahlthema ist keine verfügbare Aufgabe mehr – Schwierigkeit lockern oder verwendete Aufgaben zurücksetzen.');return;}
   alert('Der Aufgabenpool reicht nur für '+sets.length+' Satz/Sätze.');break;
  }
  if(set.length<6)alert('Hinweis: Satz '+(s+1)+' hat nur '+set.length+' Aufgaben – der Pool wird knapp.');
  sets.push(set);
  const ids={};set.forEach(function(t){ids[t.id]=1;});
  pool=pool.filter(function(t){return !ids[t.id];});
 }
 LAST={sets:sets,thema:thema};
 draw(false);
 window.scrollTo({top:0,behavior:'smooth'});
}
function stars(d){return '★★★'.slice(0,d);}
function draw(showSol){
 if(!LAST)return;
 const wrap=document.getElementById('sheet'); wrap.innerHTML='';
 LAST.sets.forEach(function(set,s){
  const sd=document.createElement('div'); sd.className='exset';
  let inner='<div class="settitle">Mündliche Prüfung – Wahlthema: '+LAST.thema+(LAST.sets.length>1?' · Satz '+(s+1):'')+(showSol?' · mit Lösungen':'')+'</div>'
   +'<div class="nameline">Name: ______________________________ &nbsp;&nbsp; Datum: ______________</div>';
  set.forEach(function(t,i){
   const wb=(i===0)?'<span class="wbadge">Wahlthema</span>':'';
   inner+='<div class="ecard" data-topic="'+t.topic+'"><div class="ehead"><span class="enum">Aufgabe '+(i+1)+'</span><span class="etopic">'+t.topic+'</span>'+wb+'<span class="dstars">'+stars(t.diff)+'</span></div>'+t.body;
   if(showSol&&t.sol) inner+='<div class="solbox"><span class="sl">Lösung</span>'+t.sol+'</div>';
   inner+='</div>';
  });
  sd.innerHTML=inner;
  wrap.appendChild(sd);
 });
 document.getElementById('result').style.display='block';
}
function printPlain(){ if(!LAST){alert('Bitte zuerst einen Prüfungssatz erstellen.');return;} draw(false); window.print(); }
function printSol(){ if(!LAST){alert('Bitte zuerst einen Prüfungssatz erstellen.');return;} draw(true); window.print(); }
function markSetUsed(){
 if(!LAST){alert('Bitte zuerst einen Prüfungssatz erstellen.');return;}
 let n=0;
 LAST.sets.forEach(function(set){set.forEach(function(t){if(!used.has(t.id)){used.add(t.id);n++;}});});
 saveUsed();
 alert(n+' Aufgabe(n) als verwendet markiert – sie werden bei neuen Sätzen (und im Baukasten) nicht mehr angeboten.');
}
function resetUsedEx(){
 if(!confirm('Alle als verwendet markierten Aufgaben wieder freigeben? (gilt auch für den Baukasten)'))return;
 used=new Set();saveUsed();
}
function updAvail(){
 const el=document.getElementById('avail');if(!el)return;
 let free=0;DATA.forEach(function(t){if(!used.has(t.id))free++;});
 el.textContent=free+' von '+DATA.length+' Aufgaben verfügbar';
}
window.addEventListener('DOMContentLoaded',function(){
 const sel=document.getElementById('thema');
 TOPICS.forEach(function(t){const o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o);});
 const p=new URLSearchParams(location.search);
 if(p.has('thema')) sel.value=p.get('thema');
 if(p.has('diff')) document.getElementById('diff').value=p.get('diff');
 if(p.has('num')) document.getElementById('num').value=p.get('num');
 updAvail();
 if(p.has('thema')) gen();
});
"""

TOPICS = list(dict.fromkeys(pools.values()))
CSS = CSS + MATH_CSS_EXAM
EXAM_TOPICS = [t for t in TOPICS if t not in EXAM_EXCLUDE]
EXAM_DATA = [d for d in DATA if d["topic"] not in EXAM_EXCLUDE]
js = JS.replace("__DATA__", json.dumps(EXAM_DATA, ensure_ascii=False)).replace("__TOPICS__", json.dumps(EXAM_TOPICS, ensure_ascii=False))

page = ('<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">'
 '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
 '<title>Mündliche Prüfung – Prüfungssatz erstellen</title>\n<style>' + CSS + '</style></head><body>\n'
 '<h1>Prüfungssatz erstellen</h1>\n'
 '<p class="sub">Themenübergreifende mündliche Prüfung: <b>1 Aufgabe zum Wahlthema</b> (wird intensiver gefragt) '
 'und <b>5 gemischte</b> Aufgaben aus 5 <b>verschiedenen</b> anderen Themen, aufsteigend nach Schwierigkeit. '
 'Mehrere Sätze auf einmal (z.&nbsp;B. ein Satz pro Schüler) enthalten <b>keine doppelten Aufgaben</b>, '
 'und bereits als „verwendet“ markierte Aufgaben (auch aus dem Baukasten) werden übersprungen. '
 'Drucken: „🖨️ Drucken (Schüler)“ ohne Lösungen, „🖨️ Mit Lösung (Lehrer)“ als Lösungsblatt für dich – '
 'jeder Satz beginnt auf einer neuen Seite.</p>\n'
 '<div class="controls">\n'
 ' <span class="lbl">Wahlthema:</span>\n'
 ' <select id="thema"></select>\n'
 ' <select id="diff"><option value="0">alle Schwierigkeiten</option>'
 '<option value="mix">⚖️ ausgewogen (2·★, 2·★★, 2·★★★)</option><option value="1">★ leicht</option>'
 '<option value="2">★★ mittel</option><option value="3">★★★ schwer</option></select>\n'
 ' <select id="num"><option value="1">1 Satz</option><option value="2">2 Sätze</option>'
 '<option value="3">3 Sätze</option><option value="4">4 Sätze</option><option value="5">5 Sätze</option>'
 '<option value="6">6 Sätze</option><option value="8">8 Sätze</option><option value="10">10 Sätze</option></select>\n'
 ' <label class="chk"><input type="checkbox" id="skipUsed" checked> verwendete ausschließen</label>\n'
 ' <button class="primary" type="button" onclick="gen()">🎲 Prüfungssatz erstellen</button>\n'
 ' <button type="button" onclick="printPlain()">🖨️ Drucken (Schüler)</button>\n'
 ' <button type="button" onclick="printSol()" style="background:#0e7c5a;color:#fff;border-color:#0e7c5a;font-weight:700">🖨️ Mit Lösung (Lehrer)</button>\n'
 ' <button type="button" onclick="markSetUsed()">✓ Satz als verwendet markieren</button>\n'
 ' <button type="button" onclick="resetUsedEx()">↺</button>\n'
 ' <span class="avail" id="avail"></span>\n'
 ' <a href="index.html" style="text-decoration:none;color:#0891b2;font-weight:600;font-size:13.5px">← Übersicht</a>\n'
 '</div>\n'
 '<div id="result"><div id="sheet"></div></div>\n'
 '<script>' + js + '</script>\n</body></html>')

with open(os.path.join(BASE, "Pruefung.html"), "w") as f:
    f.write(page)
print("wrote Pruefung.html")

# ---------------- Baukasten.html (manuelle Auswahl) ----------------
dj = json.dumps(DATA, ensure_ascii=False)
tj = json.dumps(TOPICS, ensure_ascii=False)
def esc(s): return s.replace("&", "&amp;")

BK_CSS = """
 *{box-sizing:border-box}
 body{font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0;padding:22px;background:#f4f6f7}
 h1{font-size:21px;margin:0 0 4px}
 .sub{color:#5b6569;font-size:13.5px;margin:0 0 14px;max-width:880px;line-height:1.5}
 .controls,.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:#f4f6f7;position:sticky;z-index:5}
 .controls{top:0;padding:10px 0 8px}
 .toolbar{top:46px;padding:0 0 12px;border-bottom:1px solid #dde2e5;margin-bottom:16px}
 select,button{font:inherit;font-size:13.5px;padding:8px 11px;border-radius:9px;border:1px solid #dde2e5;background:#fff;cursor:pointer}
 button.primary{background:#0891b2;color:#fff;border-color:#0891b2;font-weight:700}
 button.primary:hover{background:#0e7490}
 .lbl{font-size:13px;color:#5b6569;font-weight:700}
 .chk{font-size:13px;color:#5b6569;display:flex;align-items:center;gap:6px;cursor:pointer}
 .count{margin-left:auto;font-size:13px;color:#5b6569}
 #catalog{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
 .tile{background:#fff;border:1.5px solid #dde2e5;border-radius:12px;padding:10px 12px;cursor:pointer;position:relative}
 .tile:hover{border-color:#0891b2}
 .tile.sel{border-color:#0891b2;box-shadow:0 0 0 2px rgba(8,145,178,.25);background:#f0fbfe}
 .tile.used{opacity:.45}
 .thead{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:4px}
 .ttopic{font-size:12.5px;font-weight:700;color:#0e7490}
 .tstars{font-size:12px;color:#e8a800;letter-spacing:1px}.tstars .s0{color:#d4d8dc}
 .tbody{pointer-events:none}
 .tbody .fig{padding:2px}.tbody .fig svg{max-height:120px}
 .tbody .prob{min-height:0;font-size:12.5px;padding:7px 9px}
 .tbody .ges{font-size:12.5px}
 .tbody .data,.tbody .dt{font-size:11.5px}
 .rel{pointer-events:auto;margin-top:8px;font-size:12px;padding:3px 8px}
 #sheet{display:none}
 body.preview #catalog{display:none}
 body.preview #sheet{display:block}
 .rm{margin-left:auto;font-size:12px;padding:3px 8px;border:1px solid #dde2e5;border-radius:7px;background:#fff;cursor:pointer;color:#c0392b}
 .rm:hover{border-color:#c0392b}
 #sheettitle{font-size:16px;font-weight:700;margin:0 0 14px}
 .ecard{background:#fff;border:1.5px solid #dde2e5;border-radius:12px;padding:14px 16px;margin-bottom:16px;break-inside:avoid;page-break-inside:avoid}
 .ehead{display:flex;align-items:center;gap:10px;margin-bottom:6px}
 .enum{font-weight:700;font-size:15px}.etopic{font-size:12px;color:#5b6569;background:#eef3f7;border-radius:20px;padding:2px 10px}
 .fig{display:flex;justify-content:center;align-items:center;padding:4px}.fig svg{display:block;max-width:100%;height:auto}
 .ges{font-size:14px;line-height:1.5;margin-top:6px}.ges b{color:#c0392b}
 .prob{font-size:15px;line-height:1.55;background:#f7fafd;border:1px solid #d3def0;border-radius:9px;padding:14px 16px;margin-top:4px}
 .data{margin-top:7px;font-size:13px;line-height:1.6;background:#fafbfc;border:1px solid #e4e8ec;border-radius:7px;padding:8px 10px}
 .dt{border-collapse:collapse;margin:6px 0;font-size:12.5px}.dt td,.dt th{border:1px solid #c4ccd4;padding:2px 9px;text-align:center}.dt th{background:#eef2f6}
 .solbox{margin-top:10px;background:#f1f9f3;border:1px solid #bcdcc3;border-radius:8px;padding:9px 12px;font-size:13px;line-height:1.5}
 .solbox .sl{font-weight:700;color:#1d8a4c;display:block;margin-bottom:3px}
 .solbox ul{margin:3px 0 0 18px;padding:0}
 @page{size:A4;margin:14mm}
 @media print{body{background:#fff;padding:0}.controls,.toolbar,#catalog,h1,.sub{display:none!important}#sheet{display:block!important}.ecard{border:1px solid #bbb;min-height:80mm}.fig svg{max-height:46mm}.rm{display:none!important}}
"""

BK_FUNCS = """
const KEY='mathe_pruefung_verwendet_v1';
let used=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
let selected=[];
const byId={}; DATA.forEach(function(t){t.id=t.topic+'|'+t.n; byId[t.id]=t;});
function saveUsed(){localStorage.setItem(KEY,JSON.stringify(Array.from(used)));}
function isSel(id){return selected.indexOf(id)>=0;}
function stars(d){return '★'.repeat(d)+'<span class="s0">'+'★'.repeat(3-d)+'</span>';}
function renderCatalog(){
 var themeF=document.getElementById('fTheme').value;
 var diffF=parseInt(document.getElementById('fDiff').value)||0;
 var showUsed=document.getElementById('fUsed').checked;
 var cat=document.getElementById('catalog'); cat.innerHTML=''; var shown=0;
 DATA.forEach(function(t){
  if(themeF!=='*'&&t.topic!==themeF)return;
  if(diffF&&t.diff!==diffF)return;
  var isUsed=used.has(t.id);
  if(isUsed&&!showUsed)return;
  shown++;
  var div=document.createElement('div');
  div.className='tile'+(isSel(t.id)?' sel':'')+(isUsed?' used':'');
  div.innerHTML='<div class="thead"><span class="ttopic">'+t.topic+' · Aufgabe '+t.n+'</span><span class="tstars">'+stars(t.diff)+'</span></div><div class="tbody">'+t.body+'</div>'+(isUsed?'<button class="rel" onclick="release(event,\\''+t.id+'\\')">↩ freigeben</button>':'');
  if(!isUsed)div.onclick=function(){toggleSel(t.id);};
  cat.appendChild(div);
 });
 document.getElementById('shown').textContent=shown+' Aufgaben';
 updCount();
}
function toggleSel(id){var i=selected.indexOf(id);if(i>=0)selected.splice(i,1);else selected.push(id);renderCatalog();}
function updCount(){document.getElementById('selcount').textContent=selected.length+' ausgewählt';}
function release(e,id){e.stopPropagation();used.delete(id);saveUsed();renderCatalog();}
function clearSelBk(){selected=[];exitPreview();renderCatalog();}
function exitPreview(){document.body.classList.remove('preview');var b=document.getElementById('previewBtn');if(b)b.textContent='👁 Auswahl ansehen';}
function renderSheet(showSol){
 var sheet=document.getElementById('sheet');
 sheet.innerHTML='<div id="sheettitle">Mündliche Prüfung Mathematik'+(showSol?' · mit Lösungen':'')+'</div>';
 selected.forEach(function(id,i){var t=byId[id];var div=document.createElement('div');div.className='ecard';div.setAttribute('data-topic',t.topic);var inner='<div class="ehead"><span class="enum">Aufgabe '+(i+1)+'</span><span class="etopic">'+t.topic+'</span><button class="rm" onclick="removeFromSel(\\''+id+'\\')">✕ entfernen</button></div>'+t.body;if(showSol&&t.sol)inner+='<div class="solbox"><span class="sl">Lösung</span>'+t.sol+'</div>';div.innerHTML=inner;sheet.appendChild(div);});
}
function removeFromSel(id){var i=selected.indexOf(id);if(i>=0)selected.splice(i,1);renderCatalog();if(document.body.classList.contains('preview')){if(selected.length)renderSheet(false);else exitPreview();}}
function togglePreview(){
 if(document.body.classList.contains('preview')){exitPreview();return;}
 if(!selected.length){alert('Bitte zuerst Aufgaben anklicken.');return;}
 renderSheet(false);document.body.classList.add('preview');document.getElementById('previewBtn').textContent='← Zurück zum Katalog';window.scrollTo({top:0});
}
function printSel(){
 if(!selected.length){alert('Bitte zuerst Aufgaben anklicken.');return;}
 renderSheet(false);window.print();
}
function printSelSol(){
 if(!selected.length){alert('Bitte zuerst Aufgaben anklicken.');return;}
 renderSheet(true);window.print();
}
function markUsed(){
 if(!selected.length){alert('Keine Auswahl.');return;}
 if(!confirm(selected.length+' Aufgabe(n) als verwendet markieren? Sie verschwinden dann aus der Übersicht.'))return;
 selected.forEach(function(id){used.add(id);});saveUsed();selected=[];exitPreview();renderCatalog();
}
function resetUsed(){
 if(!confirm('Alle verwendeten Aufgaben wieder freigeben?'))return;
 used=new Set();saveUsed();renderCatalog();
}
window.addEventListener('DOMContentLoaded',renderCatalog);
"""

BK_CSS = BK_CSS + MATH_CSS_EXAM
theme_opts = '<option value="*">alle Themen</option>' + "".join('<option value="%s">%s</option>' % (esc(t), esc(t)) for t in TOPICS)

bk = ('<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">'
 '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
 '<title>Prüfung selbst zusammenstellen</title>\n<style>' + BK_CSS + '</style></head><body>\n'
 '<h1>Prüfung selbst zusammenstellen</h1>\n'
 '<p class="sub">Alle Aufgaben aller Themen als Katalog mit Bild. Klicke 6–8 Aufgaben an und drucke sie zweimal: '
 '<b>„🖨️ Drucken (Schüler)“</b> ohne Lösungen und <b>„🖨️ Mit Lösung (Lehrer)“</b> als Lösungsblatt für dich. '
 'Mit <b>„✓ Als verwendet markieren“</b> verschwinden sie aus der Übersicht, damit du sie nicht erneut nimmst – '
 'gespeichert im Browser, mit <b>„↺ Zurücksetzen“</b> wieder freigeben.</p>\n'
 '<div class="controls">\n'
 ' <span class="lbl">Filter:</span>\n'
 ' <select id="fTheme" onchange="renderCatalog()">' + theme_opts + '</select>\n'
 ' <select id="fDiff" onchange="renderCatalog()"><option value="0">alle Schwierigkeiten</option>'
 '<option value="1">★ leicht</option><option value="2">★★ mittel</option><option value="3">★★★ schwer</option></select>\n'
 ' <label class="chk"><input type="checkbox" id="fUsed" onchange="renderCatalog()"> verwendete anzeigen</label>\n'
 ' <span class="count"><span id="shown"></span> · <b id="selcount">0 ausgewählt</b></span>\n'
 '</div>\n'
 '<div class="toolbar">\n'
 ' <button type="button" id="previewBtn" onclick="togglePreview()">👁 Auswahl ansehen</button>\n'
 ' <button class="primary" type="button" onclick="printSel()">🖨️ Drucken (Schüler)</button>\n'
 ' <button type="button" onclick="printSelSol()" style="background:#0e7c5a;color:#fff;border-color:#0e7c5a;font-weight:700">🖨️ Mit Lösung (Lehrer)</button>\n'
 ' <button type="button" onclick="markUsed()">✓ Als verwendet markieren</button>\n'
 ' <button type="button" onclick="clearSelBk()">Auswahl leeren</button>\n'
 ' <button type="button" onclick="resetUsed()">↺ Verwendete zurücksetzen</button>\n'
 ' <a href="index.html" style="text-decoration:none;color:#0891b2;font-weight:600;font-size:13.5px">← Übersicht</a>\n'
 '</div>\n'
 '<div id="catalog"></div>\n<div id="sheet"></div>\n'
 '<script>const DATA = ' + dj + ';\nconst TOPICS = ' + tj + ';\n' + BK_FUNCS + '</script>\n</body></html>')

with open(os.path.join(BASE, "Baukasten.html"), "w") as f:
    f.write(bk)
print("wrote Baukasten.html")

# ---------------- index.html Zähler automatisch aktualisieren ----------------
import urllib.parse, datetime
from collections import Counter
idx_path = os.path.join(BASE, "index.html")
if os.path.exists(idx_path):
    idx = open(idx_path).read()
    counts = Counter(d["topic"] for d in DATA)
    for fn, topic in pools.items():
        if not os.path.exists(os.path.join(BASE, fn)):
            continue
        enc = urllib.parse.quote(fn)
        cnt = counts.get(topic, 0)
        idx, _ = re.subn(
            r'(href="' + re.escape(enc) + r'"[\s\S]*?<span class="badge"[^>]*>)\d+( Aufgaben)',
            lambda m: m.group(1) + str(cnt) + m.group(2), idx, count=1)
    themen = sum(1 for fn in pools if os.path.exists(os.path.join(BASE, fn)))
    today = datetime.date.today().strftime("%d.%m.%Y")
    idx = re.sub(r'(<p class="foot">)\d+( Aufgaben in )\d+( Themen)',
                 lambda m: m.group(1) + str(len(DATA)) + m.group(2) + str(themen) + m.group(3),
                 idx, count=1)
    idx = re.sub(r'(zuletzt aktualisiert )\d{2}\.\d{2}\.\d{4}',
                 lambda m: m.group(1) + today, idx, count=1)
    with open(idx_path, "w") as f:
        f.write(idx)
    print(f"index.html aktualisiert: {len(DATA)} Aufgaben in {themen} Themen")
