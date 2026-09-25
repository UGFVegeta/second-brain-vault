/* Zerfallslabor · Kernphysik Klasse 10 · Leitfrage 3: Wie schnell zerfällt ein radioaktiver Stoff?
   Würfelmodell, zufälliger Zerfall vieler Kerne, Halbwertszeit, Aktivität und Zählrate, exponentielle Abnahme im Alltag, C-14-Uhr. */
(function(){
"use strict";
var S={wurf:0, serie:"1", thw:0, nuk:"F20", tn:0, akt:1000, dz:5, alltag:"druck", xa:0, alter:0};
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

/* 2 · 400 Kerne, jeder zerfällt zu einem zufälligen Zeitpunkt */
function kerne(){
  var o=[], t=+S.thw, r=rnd(4711), n=0, i;
  for(i=0;i<400;i++){
    var z=-Math.log(1-r()*0.99999)/Math.LN2; /* Lebensdauer in Halbwertszeiten */
    var x=60+(i%20)*19, y=40+Math.floor(i/20)*19, weg=z<=t;
    if(!weg) n++;
    o.push(G.circ(x,y,7,weg?"#26324A":PROT,weg?' stroke="#4D5E77"':''));
  }
  var x0=480,y0=380;
  o.push(achsen(x0,y0,320,300,"Zeit in Halbwertszeiten","übrige Kerne"));
  o.push(kurve(x0,y0,320,300,function(tt){return Math.pow(0.5,tt);},5));
  for(i=1;i<=5;i++) o.push(G.txt(x0+i*64,y0+18,""+i,"mid dim"));
  o.push(G.circ(x0+t*64,y0-300*n/400,7,GELB));
  return {svg:o.join(""), readout:'<span class="chip">Zeit: <b>'+komma(t,1)+' Halbwertszeiten</b></span><span class="chip">noch da: <b>'+n+' von 400</b></span><span class="chip">erwartet: '+Math.round(400*Math.pow(0.5,t))+'</span>'};
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
 draw:function(cfg){ return {wuerfel:wuerfel,kerne:kerne,hwz:hwz,aktiv:aktiv,alltag:alltag,c14:c14}[cfg.mode](cfg); },
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

  {kicker:"Schritt 1", title:"Jeder Kern zerfällt zufällig",
   html:"<p>400 radioaktive Kerne. Jeder zerfällt zu einem zufälligen Zeitpunkt. Verschiebe die Zeit.</p>",
   ask:"Wie viele Kerne sind nach einer, zwei und drei Halbwertszeiten noch da?",
   note:"Die Zerfallszeiten sind zufällig, deshalb weicht die Zahl etwas vom erwarteten Wert ab. Je mehr Kerne, desto genauer passt die Kurve.",
   controls:{sl:[{k:"thw",label:"Zeit",min:0,max:5,step:0.1,fmt:function(v){return komma(v,1)+" T½"}}],reset:{thw:0}},
   cfg:{mode:"kerne"}, alt:"Viele Kerne, ein Teil zerfallen, daneben die Zerfallskurve"},

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
