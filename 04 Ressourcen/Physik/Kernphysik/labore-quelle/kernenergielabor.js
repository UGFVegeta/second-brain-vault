/* Kernenergielabor · Kernphysik Klasse 10 · Leitfragen 5 und 6
   Kernspaltung, Kettenreaktion, Steuerstäbe, Kreisläufe im Kraftwerk, Kernfusion, Abklingen des Abfalls. */
(function(){
"use strict";
var S={sp:"ba", k:"1", gen:4, stab:50, kreis:"p", temp:15, jahre:0};
var PROT="#FF7A59", NEUT="#9FB2CF", GELB="#FFC53D", GRUEN="#6FE39A", CYAN="#4CC9F0", ORANGE="#FF8A3D";
function rnd(seed){ var s=seed%233280; return function(){ s=(s*9301+49297)%233280; return s/233280; }; }
function komma(v,d){ return v.toFixed(d).replace(".",","); }
function nk(x,y,sym,A,Z,size,col){
  size=size||30; col=col||"#FFFFFF"; var k=size*0.5;
  return '<text x="'+(x-3)+'" y="'+G.f1(y-size*0.42)+'" font-family="IBM Plex Mono,monospace" font-size="'+k+'" fill="'+col+'" text-anchor="end">'+A+'</text>'+
         '<text x="'+(x-3)+'" y="'+G.f1(y+size*0.14)+'" font-family="IBM Plex Mono,monospace" font-size="'+k+'" fill="'+col+'" text-anchor="end">'+Z+'</text>'+
         '<text x="'+x+'" y="'+y+'" font-family="Georgia,serif" font-size="'+size+'" fill="'+col+'">'+sym+'</text>';
}
function kern(x,y,p,n,r,seed){
  var f=[],i,j,s=seed||3,o="";
  for(i=0;i<p;i++) f.push(PROT); for(i=0;i<n;i++) f.push(NEUT);
  for(i=f.length-1;i>0;i--){ s=(s*9301+49297)%233280; j=s%(i+1); var t=f[i]; f[i]=f[j]; f[j]=t; }
  for(i=0;i<f.length;i++){ var rr=r*1.05*Math.sqrt(i+0.5), a=i*2.39996; o+=G.circ(x+rr*Math.cos(a),y+rr*Math.sin(a),r,f[i],' stroke="#0A1120" stroke-width="1"'); }
  return o;
}

/* 1 · Spaltung */
var SP={ba:[["Ba",144,56],["Kr",89,36],3],la:[["La",147,57],["Br",87,35],2],xe:[["Xe",143,54],["Sr",90,38],3]};
function spaltung(){
  var d=SP[S.sp], o=[], i;
  o.push(G.circ(40,160,9,NEUT)+G.arrow(52,160,110,160,NEUT,2.5,0));
  o.push(kern(170,160,16,22,6,7)+G.txt(170,240,"Uran-235","mid dim"));
  o.push(G.arrow(235,160,285,160,"#9AAAC0",2.5,0.2));
  o.push('<g class="fade" style="--d:.4s">'+kern(350,160,16,23,6,8)+'<ellipse cx="350" cy="160" rx="54" ry="44" fill="none" stroke="#FF7A59" stroke-dasharray="4 5" stroke-width="2"/></g>'+G.txt(350,240,"Uran-236, instabil","mid dim"));
  o.push('<g class="fade" style="--d:.9s">'+kern(530,80,9,12,6,9)+kern(530,250,7,9,6,10)+'</g>');
  o.push(G.arrow(410,140,480,95,"#9AAAC0",2,0.7)+G.arrow(410,180,480,235,"#9AAAC0",2,0.7));
  for(i=0;i<d[2];i++){ var y=140+i*24; o.push(G.arrow(412,160,680,y,NEUT,1.6,1)+'<g class="fade" style="--d:1.4s">'+G.circ(690,y,8,NEUT)+'</g>'); }
  o.push(G.txt(600,70,d[0][0]+"-"+d[0][1],"")+G.txt(600,300,d[1][0]+"-"+d[1][1],"")+G.txt(710,145+d[2]*12,d[2]+" Neutronen",""));
  var y0=390, x=60;
  o.push(nk(x+20,y0,"n",1,0,30)+G.txt(x+50,y0-8,"+","mid")+nk(x+100,y0,"U",235,92,30)+G.txt(x+140,y0-8,"→","mid")+
         nk(x+200,y0,d[0][0],d[0][1],d[0][2],30)+G.txt(x+262,y0-8,"+","mid")+nk(x+310,y0,d[1][0],d[1][1],d[1][2],30)+G.txt(x+372,y0-8,"+ "+d[2],"mid")+nk(x+420,y0,"n",1,0,30)+G.txt(x+470,y0-8,"+ Energie",""));
  var As=d[0][1]+d[1][1]+d[2], Zs=d[0][2]+d[1][2];
  return {svg:o.join(""), readout:'<span class="chip">oben: 1 + 235 = '+d[0][1]+' + '+d[1][1]+' + '+d[2]+' = <b>'+As+'</b></span><span class="chip">unten: 0 + 92 = '+d[0][2]+' + '+d[1][2]+' = <b>'+Zs+'</b></span>'};
}

/* 2 · Kettenreaktion */
function kette(){
  var k=+S.k, g=+S.gen, o=[], i, n=1, werte=[];
  for(i=0;i<=10;i++){ werte.push(n); n=n*k; }
  var mx=Math.max.apply(null,werte.slice(0,g+1)), x0=90, y0=380, sy=280/Math.max(4,mx);
  o.push('<line x1="'+x0+'" y1="'+y0+'" x2="'+(x0+690)+'" y2="'+y0+'" stroke="#9AAAC0" stroke-width="1.5"/>');
  for(i=0;i<=10;i++){
    var v=werte[i], h=v*sy;
    if(i<=g){ o.push(G.rect(x0+10+i*62,y0-h,40,Math.max(h,1),k>1?"#FF7A59":(k<1?"#9FB2CF":GRUEN),1)); o.push(G.txt(x0+30+i*62,y0-h-8,v>=100?Math.round(v).toLocaleString("de-DE"):komma(v,v<1?2:0),"mid")); }
    o.push(G.txt(x0+30+i*62,y0+20,""+i,"mid dim"));
  }
  o.push(G.txt(x0+345,y0+44,"Generation","mid dim")+G.txt(x0,40,"Spaltungen pro Generation","dim"));
  var txt=k<1?"Die Reaktion erlischt.":(k===1?"Gleichmäßig: so läuft ein Reaktor.":"Lawine: Die Zahl der Spaltungen wächst rasend schnell.");
  return {svg:o.join(""), readout:'<span class="chip">wirksame Neutronen pro Spaltung: <b>'+komma(k,1)+'</b></span><span class="chip"><b>'+txt+'</b></span>'};
}

/* 3 · Steuerstäbe */
function staebe(){
  var s=+S.stab, k=1+(50-s)*0.004, o=[], i, x0=120, y0=60;
  o.push(G.rect(x0,y0,320,300,"#10324D",1,' rx="24" stroke="#6E8FB5" stroke-width="3"'));
  for(i=0;i<6;i++) o.push(G.rect(x0+34+i*48,y0+110,16,170,"#E8604A",1,' rx="4"'));
  var tief=40+s*2.2;
  for(i=0;i<5;i++) o.push(G.rect(x0+60+i*48,y0-40,10,tief,"#3B4150",1,' rx="2" stroke="#9FB2CF"'));
  var r=rnd(5), n=Math.round(14*k*k);
  for(i=0;i<n;i++) o.push(G.circ(x0+30+r()*260,y0+100+r()*190,4,NEUT));
  var P=k>1.005?"steigt":(k<0.995?"sinkt":"bleibt gleich");
  var x1=520,y1=320; o.push('<line x1="'+x1+'" y1="'+y1+'" x2="'+(x1+260)+'" y2="'+y1+'" stroke="#9AAAC0" stroke-width="1.5"/>'+G.txt(x1,70,"Leistung über der Zeit","dim"));
  var p=[]; for(i=0;i<=26;i++){ var v=Math.min(220,100*Math.pow(k,i*1.5)); p.push(G.f1(x1+i*10)+","+G.f1(y1-v)); }
  o.push('<polyline points="'+p.join(" ")+'" fill="none" stroke="'+(k>1.005?"#FF7A59":(k<0.995?CYAN:GRUEN))+'" stroke-width="3"/>');
  return {svg:o.join(""), readout:'<span class="chip">Steuerstäbe <b>'+s+' %</b> eingefahren</span><span class="chip">Leistung <b>'+P+'</b></span>'};
}

/* 4 · Kreisläufe */
var KR={p:["Primärkreislauf","Wasser läuft durch den Reaktor, nimmt die Wärme auf und ist radioaktiv belastet. Es bleibt im Reaktorgebäude.","#FF7A59"],
        s:["Sekundärkreislauf","Im Dampferzeuger verdampft sauberes Wasser. Der Dampf treibt Turbine und Generator.","#4CC9F0"],
        k:["Kühlkreislauf","Flusswasser kühlt den Dampf im Kondensator. Der Kühlturm gibt die Restwärme an die Luft ab.","#6FE39A"]};
function kreise(){
  var o=[], a=S.kreis, op=function(k){ return a===k?1:0.25; };
  o.push('<path d="M40 380 V140 a110 110 0 0 1 220 0 V380 z" fill="#1A2436" stroke="#6E8FB5" stroke-width="3"/>'+G.txt(150,405,"Reaktorgebäude","mid dim"));
  o.push(G.rect(80,190,70,140,"#10324D",1,' rx="16"')); for(var i=0;i<3;i++) o.push(G.rect(92+i*20,230,10,80,"#E8604A",1));
  o.push(G.rect(190,160,50,170,"#26324A",1,' rx="20"')+G.txt(215,150,"Dampferzeuger","mid dim"));
  o.push('<path d="M150 220 H200 M200 300 H150" stroke="#FF7A59" stroke-width="5" stroke-opacity="'+op("p")+'" fill="none"/>');
  o.push('<path d="M240 190 H380 L380 170 M380 170 H420 M470 250 V320 H240" stroke="#4CC9F0" stroke-width="5" stroke-opacity="'+op("s")+'" fill="none"/>');
  o.push('<path d="M420 150 L480 130 L480 210 L420 190 Z" fill="#9FB2CF"/>'+G.txt(450,235,"Turbine","mid dim")+'<line x1="480" y1="170" x2="520" y2="170" stroke="#E7EDF6" stroke-width="3"/>'+G.circ(545,170,24,"#FFD34D")+G.txt(545,215,"Generator","mid dim"));
  o.push(G.rect(430,250,90,70,"#26324A",1,' rx="8"')+G.txt(475,340,"Kondensator","mid dim"));
  o.push('<path d="M520 270 H640 M640 300 H520" stroke="#6FE39A" stroke-width="5" stroke-opacity="'+op("k")+'" fill="none"/>');
  o.push('<path d="M640 380 L660 220 Q700 200 740 220 L760 380 Z" fill="#26324A" stroke="#6E8FB5"/>'+G.txt(700,405,"Kühlturm","mid dim"));
  var d=KR[a];
  return {svg:o.join(""), readout:'<span class="chip" style="border-color:'+d[2]+'"><b>'+d[0]+':</b> '+d[1]+'</span>'};
}

/* 5 · Fusion */
function fusion(){
  var T=+S.temp, geht=T>=100, o=[], abst=geht?0:Math.max(30,200-T*1.6);
  o.push(G.txt(420,40,"Deuterium und Tritium bei "+T+" Mio. °C","mid"));
  if(!geht){ o.push(kern(420-abst,200,1,1,10,2)+kern(420+abst,200,1,2,10,3)); o.push(G.arrow(420-abst+30,200,420-abst+60,200,"#9AAAC0",2,0)+G.arrow(420+abst-34,200,420+abst-64,200,"#9AAAC0",2,0)); o.push(G.txt(420,300,"Die positiven Kerne stoßen sich ab.","mid dim")); }
  else { o.push(G.circ(420,200,80,"url(#gGlow)")+kern(420,200,2,2,12,5)+G.arrow(460,200,640,120,NEUT,2.5,0)+G.circ(650,115,10,NEUT)+G.txt(660,100,"Neutron","")+G.txt(420,320,"Fusion: Helium, ein Neutron und viel Energie","mid")); }
  o.push(G.txt(420,410,"Sonne: 15 Mio. °C bei riesigem Druck. Auf der Erde: über 100 Mio. °C nötig.","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Temperatur <b>'+T+' Mio. °C</b></span><span class="chip"><b>'+(geht?"Die Kerne verschmelzen.":"zu kalt für ein Fusionskraftwerk")+'</b></span>'};
}

/* 6 · Abklingen des Abfalls (logarithmische Zeit) */
var NUKL=[["Cäsium-137",30.1,"#FF7A59"],["Plutonium-239",24110,"#FFC53D"],["Iod-129",1.57e7,"#B28DFF"]];
function abfall(){
  var e=+S.jahre, t=Math.pow(10,e), o=[], x0=150, y0=110;
  o.push(G.txt(420,50,"Zeit: "+(t<1e4?Math.round(t).toLocaleString("de-DE"):(t<1e6?Math.round(t/1000).toLocaleString("de-DE")+" 000":komma(t/1e6,1).replace(",0","")+" Million"+(t>=1.5e6?"en":"")))+" Jahre","mid"));
  NUKL.forEach(function(n,i){
    var an=Math.pow(0.5,t/n[1]), y=y0+i*90, w=560*an;
    o.push(G.rect(x0,y,560,40,"#1A2436",1,' rx="6"')+G.rect(x0,y,Math.max(w,0.5),40,n[2],1,' rx="6"'));
    o.push(G.txt(x0-10,y+26,n[0],"end")+G.txt(x0+570,y+26,(an>=0.01?komma(100*an,1):(an>1e-9?"< 1":"0,0"))+" %",""));
    o.push(G.txt(x0,y+62,"Halbwertszeit "+(n[1]<1e6?n[1].toLocaleString("de-DE"):"15,7 Mio.")+" Jahre","dim"));
  });
  o.push(G.txt(420,420,"Der Regler läuft logarithmisch: jeder Schritt ist zehnmal so lang.","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">noch vorhanden im Vergleich zu heute</span>'};
}

window.LAB={state:S,
 draw:function(cfg){ return {spaltung:spaltung,kette:kette,stab:staebe,kreise:kreise,fusion:fusion,abfall:abfall}[cfg.mode](cfg); },
 QZ:[
  {q:"Was löst die Spaltung eines Uran-235-Kerns aus?", o:["ein Proton","ein langsames Neutron","ein Elektron"],a:1, w:"Das Neutron ist ungeladen und wird vom Kern nicht abgestoßen. Langsame Neutronen werden besonders gut eingefangen."},
  {q:"Wozu dienen die Steuerstäbe?", o:["Sie liefern Neutronen","Sie fangen überschüssige Neutronen ein","Sie kühlen den Reaktor"],a:1, w:"Bor oder Cadmium schlucken Neutronen. So bleibt im Mittel genau ein wirksames Neutron pro Spaltung."},
  {q:"Warum gibt es im Kraftwerk getrennte Wasserkreisläufe?", o:["damit radioaktives Wasser im Reaktorgebäude bleibt","weil Wasser sonst zu schnell fließt","damit es billiger ist"],a:0, w:"Nur der Primärkreislauf kommt mit dem Reaktorkern in Kontakt. Turbine und Fluss bleiben sauber."},
  {q:"Was passiert bei der Kernfusion?", o:["Ein schwerer Kern zerbricht","Leichte Kerne verschmelzen","Ein Kern sendet ein Elektron aus"],a:1, w:"Deuterium und Tritium verschmelzen zu Helium. So erzeugt die Sonne ihre Energie."},
  {q:"Uran-235 + n → Barium-144 + Krypton-89 + ? Neutronen", o:["2","3","4"],a:1, w:"Oben: 1 + 235 = 236 = 144 + 89 + 3."},
  {q:"Warum muss ein Endlager so lange sicher sein?", o:["Manche Stoffe haben Halbwertszeiten von Zehntausenden Jahren","weil es so im Gesetz steht, ohne Grund","weil Castoren rosten"],a:0, w:"Plutonium-239 hat 24 000 Jahre Halbwertszeit. Nach zehn Halbwertszeiten sind es 240 000 Jahre."}
 ],
 scenes:[
  {kicker:"Kernphysik · Leitfrage 5", title:"Die Kernspaltung",
   html:"<p>Ein langsames Neutron trifft einen Uran-235-Kern. Der Kern wird instabil und zerbricht in zwei mittelschwere Kerne. Dabei werden zwei oder drei Neutronen und viel Energie frei.</p>",
   ask:"Prüfe: Stimmen oben und unten die Summen links und rechts?",
   note:"1938 fanden Otto Hahn und Fritz Straßmann Barium in bestrahltem Uran. Lise Meitner und Otto Frisch erklärten es als Spaltung. Welche Bruchstücke entstehen, ist Zufall, drei häufige Varianten sind hier auswählbar.",
   controls:{btn:[{k:"sp",label:"Spaltprodukte:",opts:[["ba","Ba + Kr"],["la","La + Br"],["xe","Xe + Sr"]]}]},
   cfg:{mode:"spaltung"}, alt:"Spaltung eines Uran-235-Kerns"},

  {kicker:"Schritt 1", title:"Die Kettenreaktion",
   html:"<p>Die freien Neutronen können weitere Kerne spalten. Wie viele davon wirklich eine neue Spaltung auslösen, entscheidet alles.</p>",
   ask:"Was passiert bei genau einem wirksamen Neutron pro Spaltung, was bei zwei?",
   note:"Passt zum Dominoversuch auf Blatt W17. In echten Reaktoren liegt der Faktor extrem nah an 1. Eine Generation dauert nur Bruchteile einer Sekunde.",
   controls:{btn:[{k:"k",label:"wirksame Neutronen:",opts:[["0.8","0,8"],["1","1"],["2","2"],["3","3"]]}],sl:[{k:"gen",label:"Generation",min:0,max:10,step:1,fmt:function(v){return v}}],reset:{gen:4}},
   cfg:{mode:"kette"}, alt:"Zahl der Spaltungen pro Generation"},

  {kicker:"Schritt 2", title:"Steuerstäbe regeln den Reaktor",
   html:"<p>Steuerstäbe aus Bor oder Cadmium fangen Neutronen ein. Fahre sie hinein oder heraus.</p>",
   ask:"Wie weit müssen die Stäbe drin sein, damit die Leistung gleich bleibt?",
   note:"Stark vereinfacht: Bei 50 % ist der Reaktor hier genau kritisch. In echten Reaktoren wirken zusätzlich Borsäure im Wasser und Temperatureffekte. Ganz eingefahren stoppt die Kettenreaktion (Schnellabschaltung).",
   controls:{sl:[{k:"stab",label:"Steuerstäbe eingefahren",min:0,max:100,step:5,fmt:function(v){return v+" %"}}],reset:{stab:50}},
   cfg:{mode:"stab"}, alt:"Reaktorkern mit Brennstaeben und Steuerstäben"},

  {kicker:"Schritt 3", title:"Drei Wasserkreisläufe",
   html:"<p>Ein Druckwasserreaktor hat drei getrennte Kreisläufe. Wähle einen aus.</p>",
   ask:"Warum darf das Wasser aus dem Reaktor nicht zur Turbine?",
   note:"Passt zu Blatt W18. Ab dem Dampf ist ein Kernkraftwerk aufgebaut wie ein Kohlekraftwerk. Wirkungsgrad etwa 33 %, der Rest geht als Wärme an Fluss und Luft.",
   controls:{btn:[{k:"kreis",label:"Kreislauf:",opts:[["p","Primär"],["s","Sekundär"],["k","Kühlung"]]}]},
   cfg:{mode:"kreise"}, alt:"Schema eines Kernkraftwerks mit drei Kreisläufen"},

  {kicker:"Schritt 4", title:"Die Kernfusion",
   html:"<p>Bei der Fusion verschmelzen leichte Kerne. Sie stoßen sich ab, weil beide positiv sind. Erhöhe die Temperatur.</p>",
   ask:"Warum brennt die Sonne schon bei 15 Mio. °C, ein Fusionsreaktor auf der Erde aber erst ab über 100 Mio. °C?",
   note:"In der Sonne verschmilzt Wasserstoff über Zwischenschritte zu Helium. Der riesige Druck und die enorme Menge an Teilchen machen es bei geringerer Temperatur möglich. Versuchsanlagen: Wendelstein 7-X (Greifswald), ITER (Frankreich, im Bau).",
   controls:{sl:[{k:"temp",label:"Temperatur",min:1,max:150,step:1,fmt:function(v){return v+" Mio. °C"}}],reset:{temp:15}},
   cfg:{mode:"fusion"}, alt:"Zwei leichte Kerne nähern sich"},

  {kicker:"Leitfrage 6", title:"Wie lange strahlt der Abfall?",
   html:"<p>Im Abfall stecken Stoffe mit sehr verschiedenen Halbwertszeiten. Schiebe die Zeit weiter.</p>",
   ask:"Nach wie vielen Jahren ist das Cäsium praktisch weg, das Plutonium aber noch nicht?",
   note:"Passt zu W20. Halbwertszeiten: Cs-137 30 Jahre, Pu-239 24 110 Jahre, I-129 15,7 Mio. Jahre. Deshalb verlangt das Gesetz für ein Endlager einen Nachweis über eine Million Jahre.",
   controls:{sl:[{k:"jahre",label:"Zeit (logarithmisch)",min:0,max:6,step:0.1,fmt:function(v){return "10^"+komma(v,1)+" Jahre"}}],reset:{jahre:0}},
   cfg:{mode:"abfall"}, alt:"Abnahme verschiedener Stoffe im Abfall"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Bei der Kernspaltung zerbricht Uran-235 nach einem Neutronentreffer in zwei mittelschwere Kerne, dazu 2 oder 3 Neutronen und viel Energie.</li><li>Im Reaktor bleibt im Mittel genau ein Neutron wirksam, dafür sorgen Steuerstäbe. Moderator-Wasser bremst die Neutronen.</li><li>Bei der Kernfusion verschmelzen leichte Kerne. Das braucht extrem hohe Temperaturen.</li><li>Radioaktiver Abfall strahlt je nach Stoff Jahrzehnte bis Millionen Jahre.</li></ul>",
   askLabel:"Probier's aus", ask:"Stell 30 Dominosteine so auf, dass jeder Stein zwei weitere umwirft. Was passiert?",
   cfg:{mode:"kette"}, alt:"Kettenreaktion"}
 ]};
})();
