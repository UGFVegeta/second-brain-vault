import fs from 'fs';

const G = [
  { id: 'boden', name: 'Boden', c: '#b45309', t: '#fef6e7' },
  { id: 'reck', name: 'Reck', c: '#1d4ed8', t: '#eef4ff' },
  { id: 'barren', name: 'Barren', c: '#15803d', t: '#eefaf1' },
  { id: 'balancieren', name: 'Balancieren', c: '#7e22ce', t: '#f6effd' },
  { id: 'sprung', name: 'Sprung', c: '#be123c', t: '#fff0f3' },
];
const AKTIV = 'mit aktiver Landung';

// Übungen je Gerät und Stufe (Ü2 bis Ü6, dazu Ü7 als Zusatz). Quelle: BJS-Handbuch Gerätturnen 04/26,
// ergänzt um die Kippe in den Grätschsitz aus der alten Übersicht (Barren Ü5).
const D = {
  boden: [
    { items: ['Scherhandstand', 'Rolle vorwärts', 'Zurückrollen in die Kerze', 'Vorrollen und Aufstehen'] },
    { items: ['Rolle rückwärts in den Grätschstand', 'Rolle vorwärts', 'Scherhandstand'] },
    { items: ['Rolle vorwärts', 'Handstand', 'Rad'] },
    { items: ['Sprungrolle', 'Handstand-Abrollen', 'Radwende'] },
    { items: ['Handstand-Abrollen', 'Rolle rückwärts durch den Handstand', 'Radwende'] },
    { items: ['Radwende-Grätschsprung', 'Felgrolle', 'Handstützüberschlag (gestreckt oder gespreizt)'] },
  ],
  reck: [
    { items: ['Stütz und Abzug', 'Überdrehen rückwärts', 'Abdruck und Überdrehen vorwärts'] },
    { items: ['Hüftaufschwung mit Abdruckhilfe', 'Rückschwung in den Stand', 'Unterschwung aus dem Stand'] },
    { items: ['Hüftaufschwung', 'Vorspreizen', 'Kniehangab- und -aufschwung', 'Rückspreizen', 'Rückschwung und Niedersprung', 'Unterschwung aus dem Stand'] },
    { items: ['Hüftaufschwung', 'Hüftumschwung', 'Rückschwung und Niedersprung in den Stand', 'Unterschwung aus dem beidbeinigen Absprung'] },
    { items: ['Hüftaufzug', 'Hüftumschwung', 'Unterschwung aus dem Stütz'] },
    { items: ['(Spreiz-)Kippaufschwung', 'Hüftumschwung', 'Saltoabgang aus dem Langhang oder Aufgrätschen zum Unterschwung'] },
  ],
  barren: [
    { items: ['Sprung in den Stütsuperscript', 'Vor- und Rückschwung', 'Vorschwung zum Außenquersitz', 'Niedersprung ' + AKTIV] },
    { items: ['Sprung in den Stütz', 'Vor- und Rückschwung in den 4-Füßlerstand vorlings', 'Vorschwung und Kehre zum Abgang'] },
    { items: ['Sprung in den Stütz', 'Vorschwung in den Grätschsitz', 'Rück-Vor-Rückschwung zur Hockwende ' + AKTIV] },
    { items: ['Sprung in den Stütz', 'Kippe in den Grätschsitz', 'Zweimaliger Vor- und Rückschwung mit Öffnen und Schließen der Beine vorne', 'Hohe Wende'], extra: 'barren-kippe', extraLabel: 'Kippe in den Grätschsitz (Bild aus der alten Übersicht)' },
    { items: ['Aus dem Sitz: Oberarmstand und Abrollen vorwärts', 'Schwungstemme in den Grätschsitz', 'Wendekehre'] },
    { items: ['Oberarmkippe', 'Schwungstemme vorwärts in den Stütz', 'Kreishockwende oder Wendekehre'] },
  ],
  balancieren: [
    { note: 'Bank schmal', items: ['Vorwärts und rückwärts gehen', 'Beidbeinige ½ Drehung', 'Abgang: Grätschsprung ' + AKTIV] },
    { note: 'Balken oder höhere, schmale Bank', items: ['Stütz, Überspreizen', 'Abgang: Hocksprung ' + AKTIV] },
    { note: 'Balken oder höhere, schmale Bank', items: ['Aufgang: Hockwende', 'Strecksprung mit Fußwechsel', 'Pferdchensprung'] },
    { items: ['Aufgang: Aufhocken (ein- oder beidbeinig)', 'Standwaage', 'Abgang: Grätschwinkelsprung ' + AKTIV] },
    { items: ['Aufgang: Durchhocken (ein- oder beidbeinig)', 'Scherhandstand oder Rolle vorwärts', 'Abgang: Radwende ' + AKTIV] },
    { items: ['Aufgang: Auflaufen aus dem Schrägstand (mit oder ohne Stütz einer Hand)', 'Flüchtiger Handstand oder Rolle vorwärts', 'Abgang: Handstützüberschlag ' + AKTIV] },
  ],
  sprung: [
    { note: 'Kasten längs (Bauchhöhe)', items: ['Weites Aufhocken', 'Strecksprung ' + AKTIV] },
    { note: 'Bock, ca. 0,90 m', items: ['Sprunggrätsche ' + AKTIV] },
    { note: 'Bock, Pferd oder Kasten, mind. 1 m', items: ['Sprunghocke oder -grätsche ' + AKTIV] },
    { note: 'T-Bock, Sprungtisch, Pferd oder Kasten (1,10 m)', items: ['Sprunghocke oder -grätsche ' + AKTIV] },
    { note: 'T-Bock, Sprungtisch, Pferd oder Kasten (1,20 m)', items: ['Sprunghocke oder -grätsche ' + AKTIV] },
    { note: 'Pferd, Kasten oder Sprungtisch (1,20 m)', items: ['Handstützsprungüberschlag gestreckt oder gewinkelt ' + AKTIV] },
  ],
};
D.barren[0].items[0] = 'Sprung in den Stütz';

const li = (t) => {
  const m = t.match(/^(Aufgang|Abgang): (.*)$/);
  return m ? `<li><u>${m[1]}</u>: ${m[2]}</li>` : `<li>${t}</li>`;
};
const fig = (g, u, e) => `<div class="fig"><img src="bilder/${g.id}-ue${u}.png" alt="Bildreihe ${g.name} Ü${u}"></div>`;
const cell = (g, i, wide) => {
  const u = i + 2, e = D[g.id][i];
  const note = `<div class="note">${e.note || '&nbsp;'}</div>`;
  const list = `<ul class="${e.items.length > 4 ? 'two' : ''}">${e.items.map(li).join('')}</ul>`;
  const kx = e.extra ? `<div class="kx"><img src="bilder/${e.extra}.png" alt="${e.extraLabel}"><span>${e.extraLabel}</span></div>` : '';
  const low = e.extra ? `<div class="low">${list}${kx}</div>` : list;
  return `<td class="c-${g.id}${wide ? ' wide' : ''}">${note}<div class="cb">${fig(g, u, e)}${low}</div></td>`;
};
const lv = (u) => `<th class="lv"><span class="u">Ü${u}</span><span class="p">${u} Punkte</span><span class="z">+ bis zu 3 Zusatzpunkte</span><span class="m">max. ${u + 3}</span></th>`;
const thead = (gs, extra = '') => `<thead><tr><th class="h0">Übung</th>${gs.map((x) => `<th style="background:${x.c}">${x.name}</th>`).join('')}${extra}</tr></thead>`;

const NOTEN = JSON.parse(fs.readFileSync('noten.json', 'utf8'));
const KL = [7, 8, 9, 10];
const fmtP = (p) => String(p).replace('.', ',');
const rowsN = [];
for (let p = 23; p >= 0; p -= 0.5) {
  rowsN.push(`<tr><th>${fmtP(p)}</th>${KL.map((k) => { const t = NOTEN[k], top = Math.max(...Object.keys(t).map((x) => +x.replace(',', '.'))); const v = t[fmtP(p)] ?? (p > top ? '1,0' : ''); return `<td class="${p > top ? 'ab' : ''}">${v}</td>`; }).join('')}</tr>`);
}
const noten = `<table class="pn"><thead><tr><th>Punkte</th>${KL.map((k) => `<th>Kl. ${k}</th>`).join('')}</tr></thead><tbody>${rowsN.join('')}</tbody></table>`;
const best = KL.map((k) => `Kl. ${k}: ab ${fmtP(Math.max(...Object.keys(NOTEN[k]).map((x) => +x.replace(',', '.'))))}`).join(' · ');

const panel = `<td class="panel" rowspan="5">
<h3>So läuft der Dreikampf</h3>
<ol>
<li>Wähle <b>3 aus 5</b> Disziplinen.</li>
<li>Pro Disziplin turnst Du eine Übung von <b>Ü2 bis Ü6</b> (2 bis 6 Punkte).</li>
<li>Bei guter Ausführung gibt es <b>bis zu 3 Zusatzpunkte</b>.</li>
<li>Die Punkte der drei Disziplinen werden zusammengezählt. Die Summe ergibt die Note.</li>
</ol>
<h3>Punkte und Note (Jungen)</h3>
<p class="hint">Summe der 3 gewählten Geräte. Note 1,0: ${best}.</p>
${noten}
</td>`;

const page1 = `<div class="pagebox"><div class="page" id="p1">
<header><h1>Dreikampf Turnen<small>Klassen 7 bis 10 · Vorderseite: Boden, Reck, Barren</small></h1><div class="rules"><span class="k">3 aus 5 Disziplinen wählen</span><span>Ü2 bis Ü6 = 2 bis 6 Punkte</span><span>Gute Ausführung: bis zu 3 Zusatzpunkte</span></div></header>
<table class="grid">${thead(G.slice(0, 3))}<tbody>${[2, 3, 4, 5, 6].map((u, i) => `<tr>${lv(u)}${G.slice(0, 3).map((g) => cell(g, i, false)).join('')}</tr>`).join('')}</tbody></table>
<footer>Übungen und Bildreihen: Bundesjugendspiele, Handbuch Wettkampf Gerätturnen (Auszug, Stand 04/26). Kippe in den Grätschsitz aus der alten Übersicht. Nur für den schulinternen Gebrauch.</footer>
</div></div>`;
const page2 = `<div class="pagebox"><div class="page" id="p2">
<header><h1>Dreikampf Turnen<small>Klassen 7 bis 10 · Rückseite: Balancieren, Sprung, Noten</small></h1><div class="rules"><span class="k">3 aus 5 Disziplinen wählen</span><span>Ü2 bis Ü6 = 2 bis 6 Punkte</span><span>Gute Ausführung: bis zu 3 Zusatzpunkte</span></div></header>
<table class="grid p2">${thead(G.slice(3), '<th style="background:#1b2433">Noten</th>')}<tbody>${[2, 3, 4, 5, 6].map((u, i) => `<tr>${lv(u)}${G.slice(3).map((g) => cell(g, i, true)).join('')}${i === 0 ? panel : ''}</tr>`).join('')}</tbody></table>
<footer>Übungen und Bildreihen: Bundesjugendspiele, Handbuch Wettkampf Gerätturnen (Auszug, Stand 04/26). Nur für den schulinternen Gebrauch.</footer>
</div></div>`;

// Daten für den Wahl-Tab
const DATA = G.map((g) => ({
  id: g.id, name: g.name, c: g.c, t: g.t,
  stufen: D[g.id].map((e, i) => ({ u: i + 2, note: e.note || '', items: e.items, img: `bilder/${g.id}-ue${i + 2}.png`, extra: e.extra ? `bilder/${e.extra}.png` : '', extraLabel: e.extraLabel || '' })),
}));

const css = `
:root{--ink:#1b2433;--mute:#5b6678;--line:#cfd6e2}
*{box-sizing:border-box}
html{background:#e9edf3}
body{margin:0;font-family:"Helvetica Neue",Arial,sans-serif;color:var(--ink)}
.bar{position:sticky;top:0;z-index:10;display:flex;gap:8px;align-items:center;padding:10px 16px;background:#1b2433;color:#fff;flex-wrap:wrap}
.bar b{margin-right:12px;font-size:15px}
.bar button{font:inherit;font-size:13px;border:1.5px solid #fff;background:transparent;color:#fff;border-radius:999px;padding:6px 14px;cursor:pointer}
.bar button.on{background:#fff;color:#1b2433;font-weight:700}
.bar .sp{flex:1}
.bar button.pr{border-color:#f5c542;color:#f5c542}
section{padding:16px 0 40px}
/* ---------- Karten ---------- */
.page{width:1500px;height:1048px;margin:0 auto 22px;background:#fff;padding:18px 20px 10px;display:flex;flex-direction:column;zoom:var(--z,1)}
header{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-bottom:10px}
h1{margin:0;font-size:27px;letter-spacing:-.01em}
h1 small{display:block;font-size:13px;font-weight:500;color:var(--mute);margin-top:3px}
.rules{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}
.rules span{border:1.5px solid var(--ink);border-radius:999px;padding:5px 12px;font-size:12.5px;font-weight:600;white-space:nowrap}
.rules span.k{background:var(--ink);color:#fff}
table.grid{width:100%;flex:1;border-collapse:separate;border-spacing:0;table-layout:fixed;border:1.5px solid var(--ink);border-radius:8px;overflow:hidden}
table.grid th.h0,table.grid th.lv{width:92px}
table.grid thead th{color:#fff;font-size:17px;padding:7px 4px;text-align:center;letter-spacing:.02em;border-left:1.5px solid #fff;height:36px}
table.grid thead th.h0{background:var(--ink);border-left:0;font-size:11px;font-weight:600}
table.grid td,table.grid th.lv{border-top:1.5px solid var(--ink);vertical-align:top}
table.grid td{border-left:1.2px solid var(--line);padding:4px 9px 4px}
table.grid thead + tbody tr:first-child td,table.grid thead + tbody tr:first-child th.lv{border-top:0}
th.lv{background:#eceff5;text-align:center;padding:6px 3px;vertical-align:middle!important}
th.lv span{display:block}
.u{font-size:27px;font-weight:800}.p{font-size:13.5px;font-weight:700;margin-top:2px}
.z{font-size:10.5px;color:var(--mute);margin-top:5px;line-height:1.2}
.m{font-size:11.5px;font-weight:700;margin-top:6px;border-top:1px solid var(--line);padding-top:5px}
${G.map((g) => `.c-${g.id}{background:${g.t}}`).join('')}
.note{font-size:11px;color:var(--mute);font-style:italic;height:14px;line-height:14px;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fig{background:#fffdf7;border-radius:6px;padding:4px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.fig img{display:block;max-width:100%;max-height:80px;width:auto;height:auto}
.low{display:flex;gap:10px;align-items:flex-start}
.low ul{flex:1}
.kx{flex:0 0 150px;margin-top:6px;background:#fffdf7;border-radius:6px;padding:3px;text-align:center}
.kx img{display:block;width:100%;height:auto}
.kx span{display:block;font-size:9px;color:var(--mute);font-style:italic;line-height:1.15}
ul{margin:5px 0 0;padding:0 0 0 16px;font-size:13.5px;line-height:1.25}
ul.two{columns:2;column-gap:16px}
li{margin-bottom:1px;break-inside:avoid}
u{text-decoration:underline;font-weight:700}
td.wide .cb{display:flex;gap:14px;align-items:center}
td.wide .fig{flex:0 0 60%}
td.wide .fig img{max-height:150px}
td.wide ul{margin:0;flex:1;font-size:14px}
td.panel{width:400px;background:#f6f7fa;padding:14px 16px!important;vertical-align:top!important;border-top:0!important}
td.panel h3{margin:0 0 8px;font-size:17px}
td.panel ol{margin:0 0 12px;padding-left:20px;font-size:13.5px;line-height:1.35}
td.panel li{margin-bottom:4px}
.hint{font-size:12px;color:var(--mute);margin:2px 0 8px}
table.pn{width:100%;border-collapse:collapse;font-size:10.5px;background:#fff}
table.pn th,table.pn td{border:1px solid #9aa4b6;text-align:center;padding:0;height:12.4px;line-height:12px}
table.pn thead th{background:var(--ink);color:#fff;font-size:11.5px}
table.pn tbody th{background:#eceff5;font-weight:700}
table.pn td{font-weight:700}
table.pn td.ab{color:#9aa4b6;font-weight:400}
footer{margin-top:7px;font-size:10px;color:var(--mute)}
.pagebox{display:block}
/* ---------- Wahl ---------- */
#tab-wahl{max-width:1400px;margin:0 auto;padding:0 16px;display:none}
#tab-wahl h2{font-size:24px;margin:6px 0 4px}
.lead{max-width:880px;color:var(--mute);font-size:14px;line-height:1.5;margin:0 0 14px}
.wl{display:grid;grid-template-columns:1fr 340px;gap:20px;align-items:start}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}
.chip{border:2px solid var(--c);color:var(--c);background:#fff;border-radius:999px;padding:7px 16px;font:inherit;font-weight:700;cursor:pointer}
.chip.on{background:var(--c);color:#fff}
.chip:disabled{opacity:.35;cursor:not-allowed}
.gs{background:#fff;border-radius:12px;padding:14px;margin-bottom:16px;border-top:6px solid var(--c)}
.gs h3{margin:0 0 4px;color:var(--c);font-size:20px}
.gs .sub{font-size:13px;color:var(--mute);margin:0 0 10px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.card{border:1.5px solid var(--line);border-radius:10px;padding:8px;background:var(--t)}
.card h4{margin:0 0 4px;font-size:14px;display:flex;justify-content:space-between}
.card h4 span{font-weight:600;color:var(--mute);font-size:12px}
.card .im{background:#fffdf7;border-radius:6px;padding:3px;margin-bottom:6px}
.card .im img{display:block;width:100%;max-height:70px;object-fit:contain}
.card .im img.x{max-height:36px;margin-top:2px}
.card label{display:flex;gap:7px;align-items:flex-start;font-size:13px;line-height:1.3;padding:3px 2px;cursor:pointer}
.card input{margin-top:2px;accent-color:var(--c)}
.card label.dis{opacity:.4;cursor:not-allowed}
.sum{position:sticky;top:62px;background:#fff;border-radius:12px;padding:14px;border:2px solid var(--ink)}
.sum h3{margin:0 0 8px;font-size:18px}
.sum .row{display:flex;justify-content:space-between;gap:8px;padding:6px 0;border-top:1px solid var(--line);font-size:13.5px}
.sum .row small{display:block;color:var(--mute);font-size:11.5px;margin-top:2px}
.sum .tot{font-size:26px;font-weight:800;margin:10px 0 2px}
.sum select{font:inherit;font-size:13px;padding:3px 6px}
.sum .btn{margin-top:10px;width:100%;font:inherit;font-weight:700;border:2px solid var(--ink);background:var(--ink);color:#fff;border-radius:8px;padding:8px;cursor:pointer}
.rulebox{background:#fff7e0;border:1.5px solid #e6c46a;border-radius:10px;padding:10px 14px;margin:0 0 14px;font-size:13.5px;line-height:1.5;max-width:880px}
.empty{padding:30px;text-align:center;color:var(--mute);background:#fff;border-radius:12px}
/* ---------- Druck ---------- */
@page{size:A4 landscape;margin:3mm}
@media print{
 html{background:#fff}.bar,.hint.screen{display:none}
 *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
 section{padding:0}
 body[data-tab=wahl] #tab-karten{display:none}
 body[data-print=wahl] #tab-karten,body[data-print=wahl] .wl>div:first-child,body[data-print=wahl] #tab-wahl h2,body[data-print=wahl] .lead,body[data-print=wahl] .rulebox{display:none}
 body[data-print=wahl] #tab-wahl,body[data-tab=wahl] #tab-wahl{display:block}
 .wl{grid-template-columns:1fr}.sum{position:static;border:0}.sum .btn,.sum .selk{display:none}
 .pagebox{width:1095px;height:765px;overflow:hidden;page-break-after:always;margin:0}
 .pagebox:last-child{page-break-after:auto}
 .page{zoom:1;transform:scale(.73);transform-origin:0 0;margin:0;padding:18px 20px 10px}
  }`;

const js = `
const DATA=${JSON.stringify(DATA).replace(/</g, '\\u003c')};
const PUNKTE=u=>u; // Punkte einer Übung = Stufe (Ü2 = 2 Punkte ... Ü7 = 7 Punkte)
const MAXG=3, MAXE=3;
const $=s=>document.querySelector(s);
const state={g:[],e:{},z:{},k:8};
try{Object.assign(state,JSON.parse(localStorage.getItem('dk-wahl')||'{}'))}catch(e){}
const save=()=>{try{localStorage.setItem('dk-wahl',JSON.stringify(state))}catch(e){}};
const NOTEN=${JSON.stringify(NOTEN)};
const fm=p=>String(p).replace('.',',');
function top(k){const t=NOTEN[k];return t?Math.max(...Object.keys(t).map(x=>+x.replace(',','.'))):null}
function noteFor(k,p){const t=NOTEN[k];if(!t)return null;const q=Math.floor(p*2)/2;if(q>=top(k))return '1,0';return t[fm(q)]||'6,0'}
function grund(g){const sel=state.e[g.id]||[];let s=0;sel.forEach(k=>{const u=+k.split('|')[0];s+=PUNKTE(u)});return {n:sel.length,pts:sel.length?Math.round(s/MAXE):0}}
function render(){
  $('#chips').innerHTML=DATA.map(g=>{const on=state.g.includes(g.id),dis=!on&&state.g.length>=MAXG;return '<button class="chip'+(on?' on':'')+'" style="--c:'+g.c+'" data-g="'+g.id+'" '+(dis?'disabled':'')+'>'+g.name+'</button>'}).join('');
  $('#secs').innerHTML=state.g.length?DATA.filter(g=>state.g.includes(g.id)).map(g=>{
    const sel=state.e[g.id]||[],full=sel.length>=MAXE;
    return '<div class="gs" style="--c:'+g.c+';--t:'+g.t+'"><h3>'+g.name+'</h3><p class="sub">Wähle '+MAXE+' Elemente aus beliebigen Stufen. Gewählt: '+sel.length+' von '+MAXE+'.</p><div class="cards">'+g.stufen.map(s=>
      '<div class="card"><h4>Ü'+s.u+' <span>'+PUNKTE(s.u)+' Punkte je Element'+(s.u>6?' · Zusatzstufe':'')+'</span></h4>'+(s.note?'<div class="hint" style="margin:0 0 4px">'+s.note+'</div>':'')+'<div class="im"><img src="'+s.img+'" alt="">'+(s.extra?'<img class="x" src="'+s.extra+'" alt="">':'')+'</div>'+s.items.map((it,i)=>{const key=s.u+'|'+i,on=sel.includes(key),dis=!on&&full;return '<label class="'+(dis?'dis':'')+'"><input type="checkbox" data-g="'+g.id+'" data-k="'+key+'" '+(on?'checked':'')+(dis?' disabled':'')+'><span>'+it+'</span></label>'}).join('')+'</div>').join('')+'</div></div>'}).join(''):'<div class="empty">Wähle oben bis zu drei Disziplinen.</div>';
  let tot=0;
  const rows=state.g.map(id=>{const g=DATA.find(x=>x.id===id),gr=grund(g),z=state.z[id]||0;tot+=gr.pts+z;
    const names=(state.e[id]||[]).map(k=>{const [u,i]=k.split('|');return 'Ü'+u+': '+g.stufen[u-2].items[i]});
    return '<div class="row"><div><b style="color:'+g.c+'">'+g.name+'</b><small>'+(names.join('<br>')||'noch keine Elemente gewählt')+'</small></div><div style="text-align:right;white-space:nowrap">'+gr.pts+' + <select class="selk" data-z="'+id+'">'+[0,0.5,1,1.5,2,2.5,3].map(v=>'<option value="'+v+'" '+(v===z?'selected':'')+'>'+fm(v)+'</option>').join('')+'</select><small>Grund + Zusatz</small></div></div>'}).join('');
  const note=noteFor(state.k,tot),mx=top(state.k),sch=mx?('Note 1,0 ab '+fm(mx)+' Punkten.'):('Für Klasse '+state.k+' gibt es keinen Dreikampf-Schlüssel.');
  $('#sum').innerHTML='<h3>Wahlzettel</h3>'+(rows||'<div class="hint">Noch keine Disziplin gewählt.</div>')+'<div class="tot">'+fm(tot)+' Punkte</div><div class="hint" style="margin:0">von höchstens '+(state.g.length*9)+' bei Ü6 mit Zusatzpunkten</div><div class="row"><div>Klasse <select class="selk" id="kl">'+[7,8,9,10].map(k=>'<option '+(k===state.k?'selected':'')+'>'+k+'</option>').join('')+'</select><small>Notenschlüssel aus dem Reiter Karten, Rückseite. '+sch+'</small></div><div style="font-size:22px;font-weight:800">'+(note?'Note '+note:'–')+'</div></div><button class="btn" id="pw">Wahlzettel drucken</button>';
}
document.addEventListener('click',e=>{
  const c=e.target.closest('.chip');if(c){const id=c.dataset.g;state.g=state.g.includes(id)?state.g.filter(x=>x!==id):state.g.concat(id);save();render()}
  if(e.target.id==='pw'){document.body.dataset.print='wahl';window.print();setTimeout(()=>{document.body.dataset.print=''},300)}
});
document.addEventListener('change',e=>{
  const t=e.target;
  if(t.dataset&&t.dataset.k&&t.dataset.g){const a=state.e[t.dataset.g]||[];state.e[t.dataset.g]=t.checked?a.concat(t.dataset.k):a.filter(x=>x!==t.dataset.k);save();render()}
  if(t.dataset&&t.dataset.z){state.z[t.dataset.z]=+t.value;save();render()}
  if(t.id==='kl'){state.k=+t.value;save();render()}
});
// Reiter
function tab(n){document.body.dataset.tab=n;$('#tab-karten').style.display=n==='karten'?'block':'none';$('#tab-wahl').style.display=n==='wahl'?'block':'none';document.querySelectorAll('.bar .t').forEach(b=>b.classList.toggle('on',b.dataset.t===n));try{localStorage.setItem('dk-tab',n)}catch(e){}}
document.querySelectorAll('.bar .t').forEach(b=>b.addEventListener('click',()=>tab(b.dataset.t)));
$('#pk').addEventListener('click',()=>{document.body.dataset.print='karten';tab('karten');window.print();setTimeout(()=>{document.body.dataset.print=''},300)});
function zoom(){document.documentElement.style.setProperty('--z',Math.min(1,window.innerWidth/1540))}
zoom();addEventListener('resize',zoom);
let t0='karten';try{t0=localStorage.getItem('dk-tab')||'karten'}catch(e){}
if(location.hash==='#wahl')t0='wahl';
if(location.hash==='#demo'){t0='wahl';state.g=['boden','reck','barren'];state.e={boden:['4|0','4|2','5|1'],reck:['3|0','3|2'],barren:['5|1','4|1','3|2']};state.z={boden:2,reck:1,barren:3};state.k=8}
render();tab(t0);
`;

const html = `<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dreikampf Turnen Klasse 7 bis 10</title>
<style>${css}</style></head><body data-tab="karten">
<div class="bar"><b>Dreikampf Turnen</b>
 <button class="t on" data-t="karten">Karten (Vorder- und Rückseite)</button>
 <button class="t" data-t="wahl">Wahlübungen (Vorschlag)</button>
 <span class="sp"></span>
 <button class="pr" id="pk">Karten drucken (2 Seiten)</button></div>
<section id="tab-karten">${page1}${page2}</section>
<section id="tab-wahl">
 <h2>Wahlübungen: Übungen selbst zusammenstellen</h2>
 <p class="lead">Alternativvorschlag zum festen Übungsblock: Statt der drei Elemente einer Stufe wählt jede Schülerin und jeder Schüler pro Disziplin selbst drei Elemente aus beliebigen Stufen. Die Bildreihen sind dieselben wie auf den Karten.</p>
 <div class="rulebox"><b>Vorschlag für die Wertung:</b> Jedes Element zählt so viele Punkte wie seine Stufe (Ü2 = 2 Punkte bis Ü6 = 6 Punkte, Ü7 = 7 Punkte als Zusatzstufe). Die Grundpunkte einer Disziplin sind der Durchschnitt der drei gewählten Elemente, auf ganze Punkte gerundet. Dazu kommen bis zu 3 Zusatzpunkte für die Ausführung. Wer dreimal Ü4 wählt, bekommt also wie bisher 4 Grundpunkte. Wer Stärken ausspielen will, mischt Stufen. Gewertet werden drei Disziplinen.</div>
 <div class="chips" id="chips"></div>
 <div class="wl"><div id="secs"></div><aside class="sum wahlzettel" id="sum"></aside></div>
</section>
<script>${js}</script>
</body></html>`;
fs.writeFileSync('dreikampf-turnen.html', html);
console.log('ok', html.length);
