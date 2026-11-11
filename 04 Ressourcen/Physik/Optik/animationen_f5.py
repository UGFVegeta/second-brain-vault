#!/usr/bin/env python3
"""Zwei Animationsfolien für Leitfrage 5 (Oskar 11.11.2026):
1. Die Erde läuft um die Sonne: Erde wandert über die Bahn, Achse bleibt parallel, Neigung per Regler (0° bis 40°).
2. Mondphasen: Mond läuft um die Erde (Blick von oben), rechts daneben, wie man ihn von der Erde aus sieht.
Beide als Folie mit Steuerleiste (Abspielen, Regler). Im PDF steht der Anfangszustand als Standbild."""
from stunde_vorlage import ab

CSS = """<style>
.animbar{position:absolute;left:40.16pt;right:40.16pt;top:343pt;height:24pt;display:flex;align-items:center;gap:10pt;
  font:500 10.5pt -apple-system,'Helvetica Neue',Arial,sans-serif;color:#1d1d1f}
.animbar button{font:600 10.5pt -apple-system,'Helvetica Neue',Arial,sans-serif;border:none;border-radius:12pt;padding:4pt 12pt;
  background:#1d1d1f;color:#fff;cursor:pointer;white-space:nowrap}
.animbar button.hell{background:#E8E8ED;color:#1d1d1f}
.animbar label{display:flex;align-items:center;gap:6pt;white-space:nowrap}
.animbar input[type=range]{width:150pt;accent-color:#1d1d1f}
.animbar .wert{font-weight:700;min-width:62pt}
@media print{.animbar{display:none}}
</style>"""

ERDE_JS = r"""<script>(()=>{
const svg=document.currentScript.parentElement.querySelector('svg.anim-erde');if(!svg||svg.dataset.ok)return;svg.dataset.ok=1;
const bar=svg.closest('section').querySelector('.animbar');
const CX=318,CY=136,RX=232,RY=82,SX=318,SY=136,R=21;
const MON=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
const TAGE=[31,28,31,30,31,30,31,31,30,31,30,31];
let tag=172,neig=23.5,lauf=false,last=0;   /* Tag im Jahr (1 = 1. Januar), Start: 21. Juni */
const f=v=>v.toFixed(1);
function datum(t){let d=Math.round(t),m=0;while(d>TAGE[m]){d-=TAGE[m];m=(m+1)%12}return Math.max(d,1)+'. '+MON[m]}
function winkel(t){return Math.PI/2+2*Math.PI*(t-79)/365}          /* 20. März oben, 21. Juni links, 23. Sept. unten, 21. Dez. rechts */
function pos(t){const w=winkel(t);return [CX+RX*Math.cos(w),CY-RY*Math.sin(w)]}
function txt(x,y,s,a,sz,w,c){return `<text x="${f(x)}" y="${f(y)}" font-family="PlexMono, Menlo, monospace" font-size="${sz||10.5}" font-weight="${w||500}" fill="${c||'#101A2B'}" text-anchor="${a||'start'}" paint-order="stroke" stroke="#fff" stroke-width="3" stroke-linejoin="round">${s}</text>`}
function sonne(){let o=`<circle cx="${SX}" cy="${SY}" r="46" fill="url(#aeGl)"/>`;
  for(let k=0;k<8;k++){const a=k*Math.PI/4;o+=`<line x1="${f(SX+22*Math.cos(a))}" y1="${f(SY+22*Math.sin(a))}" x2="${f(SX+29*Math.cos(a))}" y2="${f(SY+29*Math.sin(a))}" stroke="#E39B00" stroke-width="2.2" stroke-linecap="round"/>`}
  return o+`<circle cx="${SX}" cy="${SY}" r="17" fill="#FFD84D" stroke="#E39B00" stroke-width="2"/>`+txt(SX+34,SY+42,'Sonne')}
function erde(x,y,r,phi,klein){
  const a=Math.atan2(SY-y,SX-x),p=w=>[x+r*Math.cos(w),y+r*Math.sin(w)],[x1,y1]=p(a+Math.PI/2),[x2,y2]=p(a+3*Math.PI/2);
  const ux=Math.sin(phi*Math.PI/180),uy=-Math.cos(phi*Math.PI/180),L=r+11;
  let o=`<circle cx="${f(x)}" cy="${f(y)}" r="${r}" fill="#3B7CC4"/><path d="M${f(x1)} ${f(y1)} A${r} ${r} 0 0 1 ${f(x2)} ${f(y2)}Z" fill="#05080F" fill-opacity=".42"/>`;
  if(!klein){ /* Äquator senkrecht zur Achse */
    o+=`<line x1="${f(x-r*uy)}" y1="${f(y+r*ux)}" x2="${f(x+r*uy)}" y2="${f(y-r*ux)}" stroke="#fff" stroke-width="1" stroke-opacity=".55" stroke-dasharray="3 3"/>`;}
  o+=`<line x1="${f(x-L*ux)}" y1="${f(y-L*uy)}" x2="${f(x+L*ux)}" y2="${f(y+L*uy)}" stroke="#101A2B" stroke-width="${klein?1.2:1.8}" stroke-linecap="round"/>`;
  if(!klein)o+=txt(x+(L+8)*ux,y+(L+8)*uy+4,'N','middle',10.5,700);
  return o}
function draw(){
  let o=`<defs><radialGradient id="aeGl"><stop offset="0" stop-color="#FFE7A0" stop-opacity=".95"/><stop offset="1" stop-color="#FFC53D" stop-opacity="0"/></radialGradient></defs>`;
  o+=`<ellipse cx="${CX}" cy="${CY}" rx="${RX}" ry="${RY}" fill="none" stroke="#66798E" stroke-width="1.4"/>`;
  /* die vier Jahreszeiten-Punkte als Orientierung */
  [[79,'Frühlingsanfang',0,-16],[172,'Sommeranfang',0,-16],[266,'Herbstanfang',0,24],[355,'Winteranfang',0,-16]].forEach(([t,s,dx,dy])=>{
    const [x,y]=pos(t);o+=`<circle cx="${f(x)}" cy="${f(y)}" r="3.2" fill="#66798E"/>`;
    const seite=t===79||t===266, lx=seite?x+40:x, an=seite?'start':'middle';
    o+=txt(lx,t===79?y-8:t===266?y+16:y+44,s,an,9.5,500,'#66798E')});
  o+=sonne();
  const [x,y]=pos(tag);
  o+=erde(x,y,R,neig,false);
  const zu=-Math.cos(winkel(tag))*Math.sin(neig*Math.PI/180), g=0.25*Math.sin(neig*Math.PI/180);   /* > 0: Nordhalbkugel zur Sonne geneigt */
  const info=neig<1?'Keine Neigung: keine Jahreszeiten':zu>g?'Nordhalbkugel zur Sonne geneigt: Sommer bei uns':
    zu<-g?'Südhalbkugel zur Sonne geneigt: Winter bei uns':'Keine Halbkugel zur Sonne geneigt';
  svg.innerHTML=o+txt(14,24,info,'start',12,700,'#D92D20')+txt(622,268,'nicht maßstabsgetreu','end',9);
  bar.querySelector('.wert').textContent=datum(tag);
  bar.querySelector('[name=tag]').value=tag;
  bar.querySelector('.nw').textContent=neig.toFixed(1).replace('.',',')+'°';
}
function step(ts){if(!lauf)return;if(last)tag=(tag+(ts-last)/1000*30-1+365)%365+1;last=ts;draw();requestAnimationFrame(step)}
bar.querySelector('.play').onclick=e=>{lauf=!lauf;last=0;e.target.textContent=lauf?'⏸ Anhalten':'▶ Abspielen';if(lauf)requestAnimationFrame(step)};
bar.querySelector('[name=tag]').oninput=e=>{tag=+e.target.value;draw()};
bar.querySelector('[name=neig]').oninput=e=>{neig=+e.target.value;draw()};
bar.querySelector('.reset').onclick=()=>{neig=23.5;bar.querySelector('[name=neig]').value=23.5;draw()};
draw()})()</script>"""

MOND_JS = r"""<script>(()=>{
const svg=document.currentScript.parentElement.querySelector('svg.anim-mond');if(!svg||svg.dataset.ok)return;svg.dataset.ok=1;
const bar=svg.closest('section').querySelector('.animbar');
const T=29.5,E=[262,140],R=96,HELL='#FFF6D8',DUNKEL='#26324A';
let tag=7.4,lauf=false,last=0;
const f=v=>v.toFixed(1);
function txt(x,y,s,a,sz,w,c){return `<text x="${f(x)}" y="${f(y)}" font-family="PlexMono, Menlo, monospace" font-size="${sz||10.5}" font-weight="${w||500}" fill="${c||'#101A2B'}" text-anchor="${a||'start'}" paint-order="stroke" stroke="#fff" stroke-width="3" stroke-linejoin="round">${s}</text>`}
function phase(x,y,r,q){q=((q%1)+1)%1;if(q<0.005||q>0.995)return '';
  const k=Math.cos(2*Math.PI*q),rechts=q<0.5,rx=Math.max(Math.abs(k)*r,0.01),s1=rechts?1:0,s2=k>0?(rechts?0:1):(rechts?1:0);
  return `<path d="M${x} ${y-r} A${r} ${r} 0 0 ${s1} ${x} ${y+r} A${f(rx)} ${r} 0 0 ${s2} ${x} ${y-r}Z" fill="${HELL}"/>`}
function name(q){q=((q%1)+1)%1;
  if(q<0.03||q>0.97)return 'Neumond';if(q<0.22)return 'zunehmende Sichel';if(q<0.28)return 'zunehmender Halbmond';
  if(q<0.47)return 'zunehmender Mond';if(q<0.53)return 'Vollmond';if(q<0.72)return 'abnehmender Mond';
  if(q<0.78)return 'abnehmender Halbmond';return 'abnehmende Sichel'}
function draw(){
  const q=tag/T,a=(180-360*q)*Math.PI/180,M=[E[0]+R*Math.cos(a),E[1]+R*Math.sin(a)];
  let o='';
  for(let i=0;i<5;i++){const y=42+i*49;o+=`<line x1="18" y1="${y}" x2="92" y2="${y}" stroke="#E39B00" stroke-width="2.2" stroke-linecap="round"/><polygon points="100,${y} 91,${y-4} 91,${y+4}" fill="#E39B00"/>`}
  o+=txt(18,28,'Sonnenlicht','start',10.5,600);
  o+=`<circle cx="${E[0]}" cy="${E[1]}" r="${R}" fill="none" stroke="#66798E" stroke-width="1.3" stroke-dasharray="5 5"/>`;
  o+=`<line x1="${E[0]}" y1="${E[1]}" x2="${f(M[0])}" y2="${f(M[1])}" stroke="#0B8FB8" stroke-width="1.4" stroke-dasharray="4 4"/>`;
  /* Erde: Nacht rechts (Sonne links) */
  o+=`<circle cx="${E[0]}" cy="${E[1]}" r="20" fill="#3B7CC4"/><path d="M${E[0]} ${E[1]-20} A20 20 0 0 1 ${E[0]} ${E[1]+20}Z" fill="#05080F" fill-opacity=".42"/>`;
  o+=txt(E[0],E[1]+38,'Erde','middle');
  /* Mond von oben: linke Hälfte hell */
  o+=`<circle cx="${f(M[0])}" cy="${f(M[1])}" r="12" fill="${DUNKEL}"/><path d="M${f(M[0])} ${f(M[1]-12)} A12 12 0 0 0 ${f(M[0])} ${f(M[1]+12)}Z" fill="#FFE29A"/><circle cx="${f(M[0])}" cy="${f(M[1])}" r="12" fill="none" stroke="#4D5E77"/>`;
  o+=txt(M[0],M[1]+(M[1]>E[1]?30:-18),'Mond','middle');
  o+=txt(18,268,'Blick von oben auf den Nordpol','start',9.5,500,'#66798E');
  /* Ansicht von der Erde */
  const VX=512,VY=118;
  o+=`<circle cx="${VX}" cy="${VY}" r="84" fill="#0A1120"/><circle cx="${VX}" cy="${VY}" r="58" fill="${DUNKEL}"/>`+phase(VX,VY,58,q)+`<circle cx="${VX}" cy="${VY}" r="58" fill="none" stroke="#4D5E77" stroke-width="1.5"/>`;
  o+=txt(VX,VY+108,'So sieht man ihn','middle',10.5,600)+txt(VX,VY+123,'von der Erde aus','middle',10.5,600);
  o+=txt(VX,VY+146,name(q),'middle',12,700,'#D92D20');
  svg.innerHTML=o;
  bar.querySelector('.wert').textContent='Tag '+tag.toFixed(1).replace('.',',');
  bar.querySelector('[name=tag]').value=tag}
function step(ts){if(!lauf)return;if(last)tag=(tag+(ts-last)/1000*2.5)%T;last=ts;draw();requestAnimationFrame(step)}
bar.querySelector('.play').onclick=e=>{lauf=!lauf;last=0;e.target.textContent=lauf?'⏸ Anhalten':'▶ Abspielen';if(lauf)requestAnimationFrame(step)};
bar.querySelector('[name=tag]').oninput=e=>{tag=+e.target.value;draw()};
draw()})()</script>"""

ZONE = '<div class="zeichenzone karo gross" style="height:277.44pt">'


def erde_folie(gruppe):
    h = ('<section class="folie">' + CSS + '<div class="titelband"><h1>Animation: Die Erde läuft um die Sonne</h1></div>'
         + ZONE + '<svg class="anim-erde" viewBox="0 0 636 277" xmlns="http://www.w3.org/2000/svg"></svg></div>'
         '<div class="animbar"><button class="play">▶ Abspielen</button>'
         '<label>Datum <input type="range" name="tag" min="1" max="365" step="1" value="172"></label><span class="wert"></span>'
         '<label>Neigung <input type="range" name="neig" min="0" max="40" step="0.5" value="23.5" style="width:90pt"></label><b class="nw"></b>'
         '<button class="hell reset">23,5°</button></div>'
         + ERDE_JS + '</section>')
    return ab(h, "Animation Erdbahn", gruppe, neu=True)


def mond_folie(gruppe):
    h = ('<section class="folie">' + CSS + '<div class="titelband"><h1>Animation: Die Mondphasen</h1></div>'
         + ZONE + '<svg class="anim-mond" viewBox="0 0 636 277" xmlns="http://www.w3.org/2000/svg"></svg></div>'
         '<div class="animbar"><button class="play">▶ Abspielen</button>'
         '<label>Tage seit Neumond <input type="range" name="tag" min="0" max="29.5" step="0.1" value="7.4" style="width:220pt"></label>'
         '<span class="wert"></span></div>'
         + MOND_JS + '</section>')
    return ab(h, "Animation Mondphasen", gruppe, neu=True)
