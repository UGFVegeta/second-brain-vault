/* Zerfallslabor · Kernphysik Klasse 10 · Leitfrage 3: Wie schnell zerfällt ein radioaktiver Stoff?
   Würfelmodell, zufälliger Zerfall vieler Kerne, Halbwertszeit, Aktivität und Zählrate, exponentielle Abnahme im Alltag, C-14-Uhr. */
(function(){
"use strict";
var S={wurf:0, serie:"1", tf:0, lauf:"pause", nf:"225", tempo:"1", zufall:1, nuk:"F20", tn:0, akt:1000, dz:5, alltag:"druck", xa:0, alter:0};
var PROT="#FF7A59", NEUT="#9FB2CF", GRUEN="#6FE39A", GELB="#FFC53D", CYAN="#4CC9F0";

function rnd(seed){ var s=seed%233280; return function(){ s=(s*9301+49297)%233280; return s/233280; }; }
function komma(v,d){ return v.toFixed(d).replace(".",","); }
function kurve(x0,y0,w,h,f,tmax,col){
  var p=[],i; for(i=0;i<=100;i++){ var t=tmax*i/100; p.push(G.f1(x0+w*i/100)+","+G.f1(y0-h*f(t))); }
  return '<polyline points="'+p.join(" ")+'" fill="none" stroke="'+(col||GRUEN)+'" stroke-width="2.6"/>';
}
function achsen(x0,y0,w,h,xl,yl){
  return '<line x1="'+x0+'" y1="'+y0+'" x2="'+(x0+w+10)+'" y2="'+y0+'" stroke="#9AAAC0" stroke-width="1.5"/>'+
         '<line x1="'+x0+'" y1="'+y0+'" x2="'+x0+'" y2="'+(y0-h-10)+'" stroke="#9AAAC0" stroke-width="1.5"/>'+
         G.txt(x0+w/2,y0+40,xl,"mid dim")+G.txt(x0+8,y0-h-6,yl,"dim");
}

/* 1 · 100 Würfel */
function wuerfelDaten(){
  var r=rnd(+S.serie*7919+11), leben=[], i, w, rest=[100];
  for(i=0;i<100;i++) leben.push(-1);
  for(w=1;w<=15;w++){ var n=0; for(i=0;i<100;i++){ if(leben[i]<0){ if(Math.floor(r()*6)===5) leben[i]=w; else n++; } } rest.push(n); }
  return {leben:leben, rest:rest};
}
function wuerfel(){
  var d=wuerfelDaten(), w=+S.wurf, o=[], i;
  for(i=0;i<100;i++){
    var x=40+(i%10)*30, y=40+Math.floor(i/10)*30, weg=d.leben[i]>0&&d.leben[i]<=w, jetzt=d.leben[i]===w&&w>0;
    o.push(G.rect(x,y,24,24,jetzt?"#E8604A":(weg?"#1D283A":"#E7EDF6"),1,' rx="5"'+(weg&&!jetzt?' stroke="#4D5E77"':'')));
    if(jetzt) o.push('<text x="'+(x+12)+'" y="'+(y+17)+'" font-family="IBM Plex Mono,monospace" font-size="13" fill="#fff" text-anchor="middle">6</text>');
  }
  var x0=400,y0=380;
  o.push(achsen(x0,y0,400,300,"Wurf","übrige Würfel"));
  for(i=0;i<=15;i++){
    var h=d.rest[i]*3; o.push(G.rect(x0+6+i*25,y0-h,18,h,i===w?GELB:(i<w?"#4D5E77":"#26324A"),1));
    o.push(G.txt(x0+15+i*25,y0+18,i%5===0?""+i:"","mid dim"));
  }
  o.push('<polyline points="'+[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15].map(function(k){return G.f1(x0+15+k*25)+","+G.f1(y0-300*Math.pow(5/6,k));}).join(" ")+'" fill="none" stroke="'+GRUEN+'" stroke-width="2" stroke-dasharray="5 5"/>');
  return {svg:o.join(""), readout:'<span class="chip">nach Wurf '+w+': <b>'+d.rest[w]+' Würfel übrig</b></span>'+(w>0?'<span class="chip">in diesem Wurf ausgeschieden: '+(d.rest[w-1]-d.rest[w])+'</span>':'')+'<span class="chip">grün gestrichelt: erwarteter Verlauf</span>'};
}

/* 2 · Zerfall von Fluor-20 als Animation (Uhr, Kernraster, Messpunkte alle 2 s, danach Kurve und Halbwertszeiten) */
var TF=11, TMAX=60, timer=null, cache={};
function zeiten(){
  var key=S.nf+"_"+S.zufall; if(cache[key]) return cache[key];
  var n=+S.nf, r=rnd(S.zufall*7919+n), z=[], i; for(i=0;i<n;i++) z.push(-Math.log(1-r()*0.999999)/Math.LN2*TF);
  return (cache[key]=z);
}
function nuk(x,y,sym,A,Z,size,col){
  var k=size*0.5; return '<text x="'+(x-2)+'" y="'+G.f1(y-size*0.42)+'" font-family="IBM Plex Mono,monospace" font-size="'+k+'" fill="'+col+'" text-anchor="end">'+A+'</text>'+
    '<text x="'+(x-2)+'" y="'+G.f1(y+size*0.14)+'" font-family="IBM Plex Mono,monospace" font-size="'+k+'" fill="'+col+'" text-anchor="end">'+Z+'</text>'+
    '<text x="'+x+'" y="'+y+'" font-family="Georgia,serif" font-size="'+size+'" fill="'+col+'">'+sym+'</text>';
}
function fluor(){
  var o=[], z=zeiten(), n=z.length, t=+S.tf, i, rest=0, seite=Math.round(Math.sqrt(n)), d=280/seite, rr=d*0.42;
  /* Gleichung */
  o.push(G.txt(40,28,"β⁻-Zerfall von Fluor-20","dim"));
  o.push(nuk(62,64,"F",20,9,24,"#FF7A59")+G.txt(96,58,"→","")+nuk(140,64,"Ne",20,10,24,"#E7EDF6")+G.txt(186,58,"+","")+nuk(214,64,"e",0,"−1",24,"#4CC9F0")+G.txt(238,58,"+","")+
         nuk(264,64,"ν̄",0,0,24,"#9AAAC0"));
  /* Raster */
  for(i=0;i<n;i++){ var x=40+(i%seite)*d+d/2, y=84+Math.floor(i/seite)*d+d/2, lebt=z[i]>t; if(lebt) rest++;
    o.push(G.circ(x,y,rr,lebt?"#FF7A59":"#3B4150",lebt?"":' stroke="#6E7F99" stroke-width="'+(d>12?1:0.5)+'"')); }
  o.push(G.circ(48,387,7,"#FF7A59")+G.txt(62,393,"Fluor-20","dim")+G.circ(48,421,7,"#3B4150",' stroke="#6E7F99"')+G.txt(62,427,"Neon-20 (stabil)","dim"));
  /* Diagramm */
  var x0=420, y0=390, w=380, h=280, sx=w/TMAX, sy=h/n;
  o.push('<line x1="'+x0+'" y1="'+y0+'" x2="'+(x0+w+10)+'" y2="'+y0+'" stroke="#9AAAC0" stroke-width="1.5"/><line x1="'+x0+'" y1="'+y0+'" x2="'+x0+'" y2="'+(y0-h-14)+'" stroke="#9AAAC0" stroke-width="1.5"/>');
  for(i=10;i<=TMAX;i+=10) o.push(G.txt(x0+i*sx,y0+18,""+i,"mid dim"));
  o.push(G.txt(x0+w+10,y0+36,"t in s","end dim")+G.txt(x0+8,y0-h-18,"unzerfallene Kerne N","dim"));
  [n,n/2,n/4,n/8].forEach(function(v){ o.push(G.txt(x0-6,y0-v*sy+4,""+Math.round(v),"end dim")); });
  var fertig=t>=TMAX-0.001;
  if(fertig){
    var p=[]; for(i=0;i<=120;i++){ var tt=TMAX*i/120; p.push(G.f1(x0+tt*sx)+","+G.f1(y0-n*Math.pow(0.5,tt/TF)*sy)); }
    o.push('<polyline points="'+p.join(" ")+'" fill="none" stroke="#FF7A59" stroke-width="2" stroke-opacity=".8"/>');
    [1,2,3].forEach(function(k){ var X=x0+k*TF*sx, Y=y0-n/Math.pow(2,k)*sy; o.push(G.dash(x0,Y,X,Y,"#D07CFF",1.4,0,0.9)+G.dash(X,Y,X,y0,"#D07CFF",1.4,0,0.9)); });
  }
  for(i=0;i<=Math.floor(t/2+1e-9)*2;i+=2){ var m=0; z.forEach(function(q){ if(q>i) m++; }); o.push(G.circ(x0+i*sx,y0-m*sy,3.6,"#FF7A59")); }
  /* Uhr */
  o.push('<rect x="690" y="6" width="118" height="54" rx="8" fill="#26324A" stroke="#6E7F99"/><rect x="700" y="16" width="98" height="34" rx="4" fill="#05080F"/>'+
         '<text x="749" y="41" font-family="IBM Plex Mono,monospace" font-size="24" fill="#6FE39A" text-anchor="middle">'+Math.floor(t)+' s</text>');
  var k=Math.floor(t/TF+1e-9), txt="";
  if(k>=1) txt=["","1 Halbwertszeit: noch ½","2 Halbwertszeiten: noch ¼","3 Halbwertszeiten: noch ⅛"][Math.min(k,3)];
  if(k>=4) txt="alle 11 s wieder die Hälfte";
  if(txt) o.push(G.rect(440,104,370,40,"#131D2E",1,' rx="6" stroke="#D07CFF"')+G.txt(625,130,txt,"mid"));
  return {svg:o.join(""), readout:'<span class="chip">t = <b>'+Math.floor(t)+' s</b></span><span class="chip">unzerfallen: <b>'+rest+' von '+n+'</b></span><span class="chip">erwartet: '+Math.round(n*Math.pow(0.5,t/TF))+'</span>'};
}
function fluorLauf(){
  if(timer){ clearInterval(timer); timer=null; }
  if(S.lauf==="reset"){ S.tf=0; S.zufall++; S.lauf="pause";
    setTimeout(function(){ var sl=document.getElementById("s_tf"), out=document.getElementById("o_tf"); if(sl) sl.value=0; if(out) out.textContent="0 s";
      Array.prototype.forEach.call(document.querySelectorAll('[data-k="lauf"]'),function(e){ e.setAttribute("aria-pressed",String(e.getAttribute("data-v")==="pause")); }); },0); }
  if(S.lauf!=="play") return;
  if(+S.tf>=TMAX) S.tf=0;
  timer=setInterval(function(){
    S.tf=Math.min(TMAX,+S.tf+0.1*(+S.tempo));
    var svg=document.getElementById("svg"), ro=document.getElementById("readout"), sl=document.getElementById("s_tf"), out=document.getElementById("o_tf");
    if(!svg||!sl){ clearInterval(timer); timer=null; return; }
    var b=fluor(); svg.innerHTML=G.defs()+b.svg; if(ro) ro.innerHTML=b.readout; sl.value=S.tf; if(out) out.textContent=Math.floor(S.tf)+" s";
    if(+S.tf>=TMAX){ clearInterval(timer); timer=null; S.lauf="pause";
      var bt=document.querySelectorAll('[data-k="lauf"]'); Array.prototype.forEach.call(bt,function(e){ e.setAttribute("aria-pressed",String(e.getAttribute("data-v")==="pause")); }); }
  },100);
}

/* 3 · Halbwertszeit verschiedener Nuklide */
var NUK={F20:["Fluor-20",11,"s","s"],Rn220:["Radon-220",56,"s","s"],I131:["Iod-131",8,"Tage","Tagen"],Cs137:["Cäsium-137",30,"Jahre","Jahren"],C14:["Kohlenstoff-14",5730,"Jahre","Jahren"],U238:["Uran-238",4.5e9,"Jahre","Jahren"]};
function hwz(){
  var d=NUK[S.nuk], T=d[1], k=+S.tn, t=k*T, o=[], x0=100, y0=390, w=660, h=320, i;
  o.push(achsen(x0,y0,w,h,"Zeit in "+d[3],"Anteil in %"));
  o.push(kurve(x0,y0,w,h,function(tt){return Math.pow(0.5,tt/T);},5*T,CYAN));
  for(i=1;i<=5;i++){
    var X=x0+i*w/5, Y=y0-h/Math.pow(2,i);
    o.push(G.dash(x0,Y,X,Y,"#FF7A59",1.2,0,0.7)+G.dash(X,Y,X,y0,"#FF7A59",1.2,0,0.7));
    var lab=T*i>=1e6?komma(T*i/1e9,1)+" Mrd.":(T*i).toLocaleString("de-DE");
    o.push(G.txt(X,y0+18,lab,"mid dim"));
    o.push(G.txt(x0-8,Y+5,komma(100/Math.pow(2,i),i>2?1:0),"end dim"));
  }
  o.push(G.txt(x0-8,y0-h+5,"100","end dim"));
  var an=Math.pow(0.5,k);
  o.push(G.circ(x0+k*w/5,y0-h*an,8,GELB));
  var tl=T>=1e6?komma(t/1e9,2)+" Mrd.":(t<100?komma(t,1):Math.round(t).toLocaleString("de-DE"));
  return {svg:o.join(""), readout:'<span class="chip"><b>'+d[0]+'</b>: Halbwertszeit '+(T>=1e6?"4,5 Mrd.":T.toLocaleString("de-DE"))+' '+d[2]+'</span><span class="chip">nach '+tl+' '+d[3]+': <b>'+komma(100*an,1)+' %</b> übrig</span>'};
}

/* 4 · Aktivität und Zählrate */
function aktiv(){
  var A=+S.akt, d=+S.dz, anteil=1/(4*d*d), rate=Math.round(60*A*anteil), o=[], i, px=200, py=200, tx=200+d*40;
  o.push('<path d="M'+(px-40)+' '+(py+36)+' h80 l-10 -32 h-60z" fill="#9FB2CF"/>'+G.circ(px,py,30,"url(#gGlow)"));
  var r=rnd(99), n=Math.min(60,Math.round(A/40));
  for(i=0;i<n;i++){ var a=r()*Math.PI*2, L=60+r()*220; o.push(G.ray(px+18*Math.cos(a),py+18*Math.sin(a),px+L*Math.cos(a),py+L*Math.sin(a),"#B28DFF",1.2,0,0.6)); }
  o.push('<rect x="'+tx+'" y="'+(py-12)+'" width="110" height="24" rx="12" fill="#9FB2CF"/><rect x="'+(tx-5)+'" y="'+(py-12)+'" width="9" height="24" rx="3" fill="#F5E6C8"/>');
  o.push(G.dash(px,300,tx,300,"#9AAAC0",1.5,0,0.8)+G.txt((px+tx)/2,324,d+" cm","mid"));
  o.push('<rect x="600" y="40" width="200" height="110" rx="12" fill="#26324A"/><rect x="614" y="54" width="172" height="52" rx="5" fill="#05080F"/>'+
         '<text x="700" y="92" font-family="IBM Plex Mono,monospace" font-size="30" fill="#6FE39A" text-anchor="middle">'+rate+'</text>'+G.txt(700,134,"Impulse pro Minute","mid dim"));
  o.push(G.txt(px,280,"Präparat","mid dim")+G.txt(40,410,"Das Zählrohr fängt nur einen kleinen Teil der Strahlung auf.","dim"));
  return {svg:o.join(""), readout:'<span class="chip">Aktivität <b>'+A.toLocaleString("de-DE")+' Bq</b> = '+(60*A).toLocaleString("de-DE")+' Zerfälle pro Minute</span><span class="chip">davon ins Zählrohr: <b>'+komma(100*anteil,anteil<0.01?2:1)+' %</b></span>'};
}

/* 5 · exponentielle Abnahme im Alltag */
var ALLTAG={druck:["Luftdruck","Höhe in km",5.5,"km",30,"halbiert sich etwa alle 5,5 km"],koffein:["Koffein im Blut","Zeit in h",5,"h",25,"halbiert sich etwa alle 5 Stunden"],
            schaum:["Bierschaum (Malzbier)","Zeit in s",100,"s",500,"halbiert sich hier etwa alle 100 s"]};
function alltag(){
  var d=ALLTAG[S.alltag], x=+S.xa*d[4]/100, an=Math.pow(0.5,x/d[2]), o=[], x0=320, y0=390, w=470, h=320, i;
  o.push(achsen(x0,y0,w,h,d[1],"in %"));
  o.push(kurve(x0,y0,w,h,function(t){return Math.pow(0.5,t/d[2]);},d[4],CYAN));
  for(i=0;i<=5;i++) o.push(G.txt(x0+i*w/5,y0+18,komma(d[4]*i/5,0),"mid dim"));
  o.push(G.circ(x0+x/d[4]*w,y0-h*an,8,GELB));
  if(S.alltag==="schaum"){
    o.push('<rect x="80" y="60" width="140" height="320" rx="10" fill="none" stroke="#9FB2CF" stroke-width="3"/>'+G.rect(84,200,132,176,"#3B2414",1)+G.rect(84,200-120*an,132,120*an,"#F5E6C8",1));
  } else if(S.alltag==="druck"){
    o.push(G.rect(80,60,160,320,"#10223D",1));
    var r=rnd(12); for(i=0;i<220;i++){ var hh=-Math.log(1-r()*0.97)*5.5/Math.LN2, yy2=380-hh/30*320; if(yy2>62) o.push(G.circ(84+r()*152,yy2,2,"#9DB8FF")); }
    o.push(G.rect(80,380-x/30*320-2,160,4,GELB,1)+G.txt(250,380-x/30*320+5,komma(x,1)+" km",""));
  } else {
    o.push('<path d="M100 360 h120 l-10 -150 h-100z" fill="#E7EDF6"/>'+G.rect(112,360-140*an,96,140*an,"#6B3E1E",1)+G.txt(160,390,"Koffein","mid dim"));
  }
  return {svg:o.join(""), readout:'<span class="chip"><b>'+d[0]+'</b> '+d[5]+'</span><span class="chip">noch <b>'+komma(100*an,1)+' %</b></span>'};
}

/* 6 · C-14-Uhr */
function c14(){
  var t=+S.alter, an=Math.pow(0.5,t/5730), o=[], x0=100, y0=390, w=660, h=300, i;
  o.push(achsen(x0,y0,w,h,"Jahre seit dem Tod","C-14 in %"));
  o.push(kurve(x0,y0,w,h,function(tt){return Math.pow(0.5,tt/5730);},40000,CYAN));
  for(i=1;i<=6;i++) o.push(G.txt(x0+i*5730/40000*w,y0+18,(5730*i).toLocaleString("de-DE"),"mid dim"));
  [["Ötzi",5300],["Roter Franz",1750]].forEach(function(f){ var X=x0+f[1]/40000*w,Y=y0-h*Math.pow(0.5,f[1]/5730); o.push(G.circ(X,Y,5,"#FF7A59")+G.txt(X+10,Y-10,f[0],"dim")); });
  o.push(G.circ(x0+t/40000*w,y0-h*an,8,GELB));
  return {svg:o.join(""), readout:'<span class="chip">Alter <b>'+t.toLocaleString("de-DE")+' Jahre</b></span><span class="chip">noch <b>'+komma(100*an,1)+' %</b> des C-14</span>'+(t>45000?'<span class="chip">zu wenig C-14 für eine genaue Messung</span>':'')};
}

window.LAB={state:S,
 draw:function(cfg){ if(cfg.mode==="fluor") fluorLauf(); else if(timer){ clearInterval(timer); timer=null; S.lauf="pause"; } return {wuerfel:wuerfel,fluor:fluor,hwz:hwz,aktiv:aktiv,alltag:alltag,c14:c14}[cfg.mode](cfg); },
 QZ:[
  {q:"Von 800 Kernen sind nach zwei Halbwertszeiten noch wie viele übrig?", o:["400","200","0"],a:1, w:"Jede Halbwertszeit halbiert: 800, 400, 200."},
  {q:"Kann man vorhersagen, wann ein bestimmter Kern zerfällt?", o:["Ja, genau nach einer Halbwertszeit","Nein, das ist Zufall","Nur bei kurzen Halbwertszeiten"],a:1, w:"Die Halbwertszeit gilt nur für sehr viele Kerne. Der einzelne Kern zerfällt zufällig."},
  {q:"Was gibt die Einheit Becquerel an?", o:["die Energie der Strahlung","die Zahl der Zerfälle pro Sekunde","die Masse des Präparats"],a:1, w:"1 Bq heißt: ein Zerfall pro Sekunde."},
  {q:"Warum zeigt das Zählrohr weniger an als die Aktivität?", o:["Es fängt nur einen Teil der Strahlung auf","Es ist falsch eingestellt","Die Strahlung wird unterwegs langsamer"],a:0, w:"Die Strahlung fliegt in alle Richtungen. Nur ein kleiner Teil trifft das Fenster des Zählrohrs."},
  {q:"Iod-131 hat eine Halbwertszeit von 8 Tagen. Nach wie vielen Tagen sind noch 25 % übrig?", o:["16 Tage","24 Tage","32 Tage"],a:0, w:"25 % sind zwei Halbwertszeiten: 2 · 8 Tage = 16 Tage."},
  {q:"Warum eignet sich C-14 nicht für 100 000 Jahre alte Knochen?", o:["Dann ist fast kein C-14 mehr übrig","Knochen enthalten keinen Kohlenstoff","C-14 zerfällt nach 5730 Jahren komplett"],a:0, w:"Nach etwa 17 Halbwertszeiten ist nur noch ein winziger Rest übrig, zu wenig zum Messen."}
 ],
 scenes:[
  {kicker:"Kernphysik · Leitfrage 3", title:"100 Würfel zerfallen",
   html:"<p>100 Würfel werden gleichzeitig geworfen. Wer eine Sechs hat, scheidet aus. Die übrigen werden wieder geworfen. Schiebe den Regler Wurf für Wurf weiter.</p>",
   ask:"Welcher Würfel als Nächstes fällt, weiß niemand. Warum ist der Verlauf trotzdem vorhersagbar?",
   note:"Passt zu Blatt W06. Jede Runde scheidet im Mittel ein Sechstel aus, übrig bleiben 5/6. Nach etwa 3,8 Würfen ist die Hälfte weg, das ist die „Halbwertszeit“ des Würfelmodells. Mit „Versuch“ andere Zufallsfolgen zeigen, der Verlauf bleibt ähnlich.",
   controls:{btn:[{k:"serie",label:"Versuch:",opts:[["1","1"],["2","2"],["3","3"]]}],sl:[{k:"wurf",label:"Wurf",min:0,max:15,step:1,fmt:function(v){return v}}],reset:{wurf:0}},
   cfg:{mode:"wuerfel"}, alt:"100 Würfel und Säulendiagramm der übrigen Würfel"},

  {kicker:"Schritt 1", title:"Zerfall von Fluor-20",
   html:"<p>Viele Fluor-20-Kerne zerfallen in stabiles Neon-20. Starte die Uhr und beobachte die Kerne und das Diagramm. Alle 2 Sekunden wird gezählt.</p>",
   ask:"Wie viele Kerne sind nach 11, 22 und 33 Sekunden noch nicht zerfallen? Welcher Kern als Nächstes zerfällt, weiß niemand.",
   note:"Nachgebaut nach der Animation auf LEIFIphysik (Halbwertszeit). Fluor-20 hat eine Halbwertszeit von etwa 11 s. Jeder Durchlauf ist neu gewürfelt: Mit „Neustart“ zerfallen andere Kerne, der Verlauf bleibt fast gleich. Mit 900 Kernen liegen die Punkte näher an der Kurve als mit 100. Nach 60 s erscheinen Kurve und Halbwertszeiten. Der Zeitregler geht auch von Hand.",
   controls:{btn:[{k:"lauf",label:"Uhr:",opts:[["play","▶ Start"],["pause","Pause"],["reset","Neustart"]]},{k:"nf",label:"Kerne:",opts:[["100","100"],["225","225"],["900","900"]]},{k:"tempo",label:"Tempo:",opts:[["1","1×"],["2","2×"],["4","4×"]]}],
             sl:[{k:"tf",label:"Zeit",min:0,max:60,step:1,fmt:function(v){return Math.floor(v)+" s"}}]},
   cfg:{mode:"fluor"}, alt:"Kerne von Fluor-20 zerfallen, daneben Uhr und Zerfallsdiagramm"},

  {kicker:"Schritt 2", title:"Die Halbwertszeit",
   html:"<p>Die <span class=\"term\">Halbwertszeit</span> ist die Zeit, nach der die Hälfte der Kerne zerfallen ist. Sie ist für jedes Nuklid fest.</p>",
   ask:"Wie viel Prozent sind nach vier Halbwertszeiten noch übrig?",
   note:"Die Kurve hat für jedes Nuklid dieselbe Form, nur die Zeitachse ist anders beschriftet. Halbwertszeiten reichen von Sekundenbruchteilen bis zu Milliarden Jahren.",
   controls:{btn:[{k:"nuk",label:"Nuklid:",opts:[["F20","F-20"],["Rn220","Rn-220"],["I131","I-131"],["Cs137","Cs-137"],["C14","C-14"],["U238","U-238"]]}],
             sl:[{k:"tn",label:"Zeit",min:0,max:5,step:0.05,fmt:function(v){return komma(v,2)+" Halbwertszeiten"}}],reset:{tn:0}},
   cfg:{mode:"hwz"}, alt:"Zerfallskurve mit Halbwertszeiten"},

  {kicker:"Schritt 3", title:"Aktivität und Zählrate",
   html:"<dl class=\"terms\"><div><dt>Aktivität</dt><dd>Zahl der Zerfälle pro Sekunde, Einheit Becquerel (Bq)</dd></div><div><dt>Zählrate</dt><dd>Impulse, die das Zählrohr misst</dd></div></dl>",
   ask:"Was passiert mit der Zählrate, wenn du den Abstand verdoppelst?",
   note:"Passt zu Blatt W08. Vereinfacht: Das Zählrohr registriert jedes Teilchen, das sein Fenster (Radius 1 cm) trifft, Luftabsorption wird vernachlässigt. Anteil = Fensterfläche geteilt durch Kugeloberfläche = r²/(4d²). Doppelter Abstand gibt ein Viertel.",
   controls:{sl:[{k:"akt",label:"Aktivität",min:200,max:5000,step:100,fmt:function(v){return v.toLocaleString("de-DE")+" Bq"}},{k:"dz",label:"Abstand",min:2,max:10,step:1,fmt:function(v){return v+" cm"}}],reset:{akt:1000,dz:5}},
   cfg:{mode:"aktiv"}, alt:"Präparat strahlt in alle Richtungen, nur ein Teil trifft das Zählrohr"},

  {kicker:"Im Alltag", title:"Nicht nur Atomkerne",
   html:"<p>Auch andere Größen nehmen so ab: in gleichen Schritten immer um die Hälfte.</p>",
   ask:"Was haben alle drei Kurven gemeinsam?",
   note:"Luftdruck: Halbierung etwa alle 5,5 km (auf dem Mount Everest rund ein Drittel). Koffein: Halbwertszeit im Blut je nach Mensch etwa 3 bis 6 Stunden. Bierschaum: der Wert hängt stark vom Getränk ab, 100 s ist ein Beispiel. Der Versuch mit Malzbier steht auf Blatt W07.",
   controls:{btn:[{k:"alltag",label:"Beispiel:",opts:[["druck","Luftdruck"],["koffein","Koffein"],["schaum","Bierschaum"]]}],sl:[{k:"xa",label:"Weg entlang der Achse",min:0,max:100,step:1,fmt:function(v){return v+" %"}}],reset:{xa:0}},
   cfg:{mode:"alltag"}, alt:"Exponentielle Abnahme im Alltag"},

  {kicker:"Anwendung", title:"Die C-14-Uhr",
   html:"<p>Lebewesen nehmen Kohlenstoff auf, darunter einen festen Anteil C-14. Nach dem Tod kommt nichts mehr nach, das C-14 zerfällt mit 5730 Jahren Halbwertszeit.</p>",
   ask:"In einem Holzfund ist noch 25 % des C-14 übrig. Wie alt ist er?",
   note:"Passt zu W22. Ötzi starb vor etwa 5300 Jahren, der „Rote Franz“ (Moorleiche aus dem Emsland) im 3. oder 4. Jahrhundert. Die Methode reicht bis etwa 50 000 Jahre zurück. Willard Libby erhielt dafür 1960 den Nobelpreis für Chemie.",
   controls:{sl:[{k:"alter",label:"Alter",min:0,max:40000,step:100,fmt:function(v){return v.toLocaleString("de-DE")+" Jahre"}}],reset:{alter:0}},
   cfg:{mode:"c14"}, alt:"Zerfallskurve von C-14 mit Ötzi"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Wann ein einzelner Kern zerfällt, ist Zufall. Für sehr viele Kerne ist der Verlauf trotzdem sicher.</li><li>Nach jeder Halbwertszeit ist die Hälfte der noch vorhandenen Kerne zerfallen. Die Menge wird nie ganz null.</li><li>Die Aktivität zählt die Zerfälle pro Sekunde (Becquerel). Das Zählrohr misst nur einen Teil davon.</li></ul>",
   askLabel:"Probier's aus", ask:"Wirf zu Hause 32 Münzen. Alle mit Zahl scheiden aus, die übrigen wirfst du wieder. Wie oft musst du werfen, bis nur noch etwa 4 übrig sind? Was ist hier die Halbwertszeit?",
   cfg:{mode:"hwz"}, alt:"Zerfallskurve"}
 ]};
})();
