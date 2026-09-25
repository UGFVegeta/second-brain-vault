/* Wirkungslabor · Kernphysik Klasse 10 · Leitfrage 4: Was macht ionisierende Strahlung mit dem Körper?
   Ionisation, Nebelkammer, Zelle, persönliche Jahresdosis, Schutzregeln. Werte nach BfS (Durchschnitt Deutschland). */
(function(){
"use strict";
var S={ion:"a", nk:"a", treffer:"1", fl:0, rx:0, ct:0, radon:"1.1", ab:2, zeit:10, blei:0};
var PROT="#FF7A59", NEUT="#9FB2CF", ELEK="#4CC9F0", ALPHA="#FF8A3D", GAMMA="#B28DFF", GELB="#FFC53D", GRUEN="#6FE39A";
function rnd(seed){ var s=seed%233280; return function(){ s=(s*9301+49297)%233280; return s/233280; }; }
function komma(v,d){ return v.toFixed(d).replace(".",","); }

/* 1 · Ionisation im Gewebe */
function ion(){
  var o=[], t=S.ion, r=rnd(t==="a"?5:(t==="b"?9:13)), i, n=0, col=t==="a"?ALPHA:(t==="b"?ELEK:GAMMA);
  o.push(G.rect(160,40,640,340,"#131D2E",1,' rx="10"')+G.txt(480,32,"Gewebe (stark vergrößert)","mid dim"));
  var r2=rnd(3); for(i=0;i<260;i++) o.push(G.circ(170+r2()*620,50+r2()*320,2,"#4D5E77"));
  o.push('<path d="M20 240 h80 l-10 -40 h-60z" fill="#9FB2CF"/>'+G.circ(60,205,22,"url(#gGlow)"));
  if(t==="a"){ o.push(G.ray(100,210,250,210,col,5,0)); for(i=0;i<34;i++){ var x=165+r()*85, y=210+(r()-.5)*16; o.push(G.circ(x,y,3.5,PROT)+G.circ(x+5,y-6,2.5,ELEK)); n++; } }
  else if(t==="b"){ var p="M100 210", x=100, y=210; for(i=0;i<18;i++){ x+=38; y+= (r()-.5)*60; y=Math.max(70,Math.min(350,y)); p+=" L"+G.f1(x)+" "+G.f1(y); if(x>165&&i%2===0){ o.push(G.circ(x,y+6,3.5,PROT)+G.circ(x+5,y,2.5,ELEK)); n++; } } o.push('<path d="'+p+'" fill="none" stroke="'+col+'" stroke-width="2"/>'); }
  else { var d="M100 210"; for(i=0;i<44;i++) d+=" q8 "+(i%2?8:-8)+" 16 0"; o.push('<path d="'+d+'" fill="none" stroke="'+col+'" stroke-width="2.4"/>');
         [[330,210],[610,210]].forEach(function(q){ o.push(G.circ(q[0],q[1]+6,3.5,PROT)); var e=q[0]; o.push(G.ray(e,q[1],e+70,q[1]+70,ELEK,1.6,0,0.9)+G.circ(e+70,q[1]+70,3,ELEK)); n++; }); }
  o.push(G.txt(500,420,"rot: Ion, blau: herausgeschlagenes Elektron","mid dim"));
  var txt=t==="a"?"α: sehr viele Ionen auf kurzer Strecke":(t==="b"?"β: weniger Ionen, dafür längerer Weg":"γ: nur ab und zu ein Treffer, dringt tief ein");
  return {svg:o.join(""), readout:'<span class="chip"><b>'+txt+'</b></span><span class="chip">Ionen im Bild: '+n+'</span>'};
}

/* 2 · Nebelkammer */
function nebel(){
  var o=[], t=S.nk, r=rnd(t==="a"?21:(t==="b"?33:44)), i, k;
  o.push('<ellipse cx="420" cy="220" rx="370" ry="190" fill="#0B1322" stroke="#4D5E77" stroke-width="3"/>');
  function spur(x,y,a,L,w,krumm){ var p="M"+G.f1(x)+" "+G.f1(y); for(k=0;k<12;k++){ a+=krumm*(r()-.5); x+=L/12*Math.cos(a); y+=L/12*Math.sin(a); p+=" L"+G.f1(x)+" "+G.f1(y); }
    return '<path d="'+p+'" fill="none" stroke="#E7EDF6" stroke-opacity=".85" stroke-width="'+w+'" stroke-linecap="round"/>'; }
  for(i=0;i<3;i++) o.push(spur(100+r()*640,80+r()*280,r()*6.3,80+r()*120,1.2,1.2));   /* Umgebung: ein paar dünne Spuren */
  if(t==="a"){ o.push(G.circ(420,220,10,"#9FB2CF")); for(i=0;i<14;i++){ var a=i*0.45; o.push(spur(420+12*Math.cos(a),220+12*Math.sin(a),a,70+r()*14,4.5,0.05)); } }
  if(t==="b"){ o.push(G.circ(420,220,10,"#9FB2CF")); for(i=0;i<7;i++){ var b=r()*6.3; o.push(spur(420+12*Math.cos(b),220+12*Math.sin(b),b,180+r()*120,1.3,1.1)); } }
  var txt=t==="a"?"α: kurze, dicke, gerade Spuren, alle etwa gleich lang":(t==="b"?"β: lange, dünne, verbogene Spuren":"nur Umgebungsstrahlung: ab und zu eine Spur");
  return {svg:o.join(""), readout:'<span class="chip"><b>'+txt+'</b></span>'};
}

/* 3 · Treffer in der Zelle */
var FOLGE={"1":["Reparatur","Die Zelle repariert die DNA. Meistens passiert genau das.",GRUEN],"2":["Zelltod","Die Zelle stirbt ab und wird ersetzt. Bei sehr vielen toten Zellen: Strahlenkrankheit.",GELB],"3":["Veränderung","Die Zelle lebt mit falscher DNA weiter. Jahre später kann Krebs entstehen.",PROT]};
function zelle(){
  var o=[], f=FOLGE[S.treffer], i;
  o.push('<ellipse cx="330" cy="220" rx="260" ry="170" fill="#2A2418" stroke="#C6B48E" stroke-width="3"/><ellipse cx="330" cy="220" rx="100" ry="80" fill="#2C2440" stroke="#9C84C4" stroke-width="2"/>');
  var p1="",p2=""; for(i=0;i<=40;i++){ var x=250+i*4; p1+=(i?" L":"M")+x+" "+G.f1(220+26*Math.sin(i*.4)); p2+=(i?" L":"M")+x+" "+G.f1(220-26*Math.sin(i*.4)); }
  o.push('<path d="'+p1+'" fill="none" stroke="#B28DFF" stroke-width="3"/><path d="'+p2+'" fill="none" stroke="#B28DFF" stroke-width="3"/>');
  if(S.treffer==="1") o.push(G.circ(330,220,12,"none",' stroke="'+GRUEN+'" stroke-width="3"'));
  if(S.treffer==="2") o.push('<ellipse cx="330" cy="220" rx="260" ry="170" fill="#05080F" fill-opacity=".55"/>');
  if(S.treffer==="3") o.push(G.circ(330,220,12,PROT)+G.circ(300,200,8,PROT,' opacity=".6"')+G.circ(360,245,8,PROT,' opacity=".6"'));
  o.push(G.arrow(20,20,318,208,ALPHA,4,0));
  o.push(G.rect(610,150,210,140,"#131D2E",1,' rx="10" stroke="'+f[2]+'" stroke-width="2"')+'<text x="715" y="200" font-family="IBM Plex Mono,monospace" font-size="20" fill="'+f[2]+'" text-anchor="middle">'+f[0]+'</text>');
  return {svg:o.join(""), readout:'<span class="chip"><b>'+f[0]+':</b> '+f[1]+'</span>'};
}

/* 4 · Meine Jahresdosis (mSv) */
function dosis(){
  var o=[], teile=[["Radon",+S.radon,"#5DBB63"],["Boden",0.4,"#7FCB76"],["Nahrung",0.3,"#9ED88B"],["Weltall",0.3,"#BFE5A8"],
                  ["Flüge",0.1*S.fl,"#4CC9F0"],["Röntgen",0.02*S.rx,"#FF9C7A"],["CT Kopf",2*S.ct,"#FF7A59"]], sum=0, x=80, i;
  teile.forEach(function(t){ sum+=t[1]; });
  var sk=640/Math.max(8,sum);
  teile.forEach(function(t){ var w=t[1]*sk; if(w>0.5){ o.push(G.rect(x,150,w,70,t[2],1)); if(w>40) o.push('<text x="'+G.f1(x+w/2)+'" y="190" font-family="IBM Plex Mono,monospace" font-size="12" fill="#0A1120" text-anchor="middle">'+t[0]+'</text>'); } x+=w; });
  o.push(G.txt(80,130,"deine Jahresdosis: "+komma(sum,2)+" mSv",""));
  for(i=0;i<=Math.max(8,sum);i+=(sum>10?2:1)){ var X=80+i*sk; o.push('<line x1="'+G.f1(X)+'" y1="226" x2="'+G.f1(X)+'" y2="234" stroke="#9AAAC0"/>'+G.txt(X,252,""+i,"mid dim")); }
  o.push(G.txt(80,300,"Vergleich:","")+G.txt(80,326,"Durchschnitt in Deutschland: etwa 3,6 mSv (2,1 natürlich, 1,5 Medizin)","dim")+
         G.txt(80,350,"Grenzwert für Menschen, die beruflich mit Strahlung arbeiten: 20 mSv pro Jahr","dim")+
         G.txt(80,374,"ab etwa 100 mSv: Krebsrisiko messbar erhöht","dim")+G.txt(80,398,"ab etwa 1000 mSv auf einmal: Strahlenkrankheit","dim"));
  return {svg:o.join(""), readout:'<span class="chip">Jahresdosis <b>'+komma(sum,2)+' mSv</b></span><span class="chip">davon natürlich '+komma(+S.radon+1,1)+' mSv</span>'};
}

/* 5 · Schutz: Abstand, Zeit, Abschirmung */
function schutz(){
  var o=[], d=+S.ab, t=+S.zeit, b=+S.blei, rel=(t/10)*(4/(d*d))*Math.pow(0.5,b/1.2), px=90, mx=90+d*150;
  o.push('<path d="M'+(px-40)+' 300 h80 l-10 -34 h-60z" fill="#9FB2CF"/>'+G.circ(px,262,28,"url(#gGlow)"));
  if(b>0) o.push(G.rect(170,150,Math.max(6,b*10),170,"#4D5E77",1,' stroke="#9FB2CF"'));
  o.push(G.circ(mx,180,18,"#E7EDF6")+G.rect(mx-16,200,32,80,"#E7EDF6",1,' rx="10"')+G.rect(mx-10,280,8,50,"#E7EDF6",1)+G.rect(mx+2,280,8,50,"#E7EDF6",1));
  o.push(G.dash(px,360,mx,360,"#9AAAC0",1.5,0,0.8)+G.txt((px+mx)/2,384,d+" m","mid"));
  var bh=Math.min(300,rel*150);
  o.push(G.rect(760,380-bh,50,bh,rel>1.01?"#FF7A59":GRUEN,1)+G.txt(785,400,"Dosis","mid dim")+'<line x1="750" y1="230" x2="820" y2="230" stroke="#9AAAC0" stroke-dasharray="4 4"/>'+G.txt(745,234,"Start","end dim"));
  return {svg:o.join(""), readout:'<span class="chip">Dosis im Vergleich zum Start: <b>'+(rel>=0.1?komma(rel,2):komma(rel,3))+'-fach</b></span><span class="chip">Start: 2 m, 10 min, kein Blei</span>'};
}

window.LAB={state:S,
 draw:function(cfg){ return {ion:ion,nebel:nebel,zelle:zelle,dosis:dosis,schutz:schutz}[cfg.mode](cfg); },
 QZ:[
  {q:"Warum heißt die Strahlung „ionisierend“?", o:["Sie bringt Atome zum Leuchten","Sie schlägt Elektronen aus Atomen heraus","Sie spaltet Atomkerne"],a:1, w:"Zurück bleiben geladene Ionen. Dadurch können Moleküle im Körper verändert werden."},
  {q:"Welche Strahlung erzeugt auf kurzer Strecke die meisten Ionen?", o:["α","β","γ"],a:0, w:"α-Teilchen sind groß und doppelt geladen. Sie geben ihre Energie auf wenigen Mikrometern Gewebe ab."},
  {q:"Du verdoppelst den Abstand zur Quelle. Was passiert mit der Dosis?", o:["Sie halbiert sich","Sie wird ein Viertel","Sie bleibt gleich"],a:1, w:"Die Strahlung verteilt sich auf die vierfache Fläche."},
  {q:"Woher kommt in Deutschland der größte Teil der natürlichen Strahlung?", o:["aus dem Weltall","vom Radon in der Atemluft","aus Kernkraftwerken"],a:1, w:"Radon und seine Folgeprodukte machen etwa die Hälfte der natürlichen Dosis aus. Lüften hilft."},
  {q:"Was ist ein Spätschaden?", o:["Haarausfall am nächsten Tag","Krebs, der Jahre später entsteht","ein Sonnenbrand"],a:1, w:"Spätschäden zeigen sich erst nach Jahren. Frühschäden wie die Strahlenkrankheit treten nur bei sehr hohen Dosen auf."}
 ],
 scenes:[
  {kicker:"Kernphysik · Leitfrage 4", title:"Strahlung schlägt Elektronen heraus",
   html:"<p>Auf ihrem Weg durch Gewebe schlägt die Strahlung Elektronen aus Atomen. Es entstehen Ionen. Wähle die Strahlungsart.</p>",
   ask:"Welche Strahlung richtet auf kurzer Strecke den größten Schaden an?",
   note:"Die Zahl der Ionen ist nur qualitativ. α erzeugt pro Mikrometer Weg sehr viele Ionen, γ nur vereinzelt über einen langen Weg. Deshalb bewertet man α im Körper rund 20-mal so stark (Wichtungsfaktor).",
   controls:{btn:[{k:"ion",label:"Strahlung:",opts:[["a","α"],["b","β"],["g","γ"]]}]},
   cfg:{mode:"ion"}, alt:"Strahlung ionisiert Atome im Gewebe"},

  {kicker:"Nachweis", title:"Die Nebelkammer",
   html:"<p>In einer Nebelkammer sieht man die Spur einzelner Teilchen: An den Ionen bilden sich kleine Nebeltröpfchen, wie ein Kondensstreifen.</p>",
   ask:"Woran erkennst du α- und β-Strahlung?",
   note:"Eine Diffusionsnebelkammer mit Trockeneis und Isopropanol zeigt auch ohne Präparat Spuren der Umgebungsstrahlung (Myonen, Radon). Gute Videos gibt es von CERN (Nebelkammer bauen) und der LMU. Bild vereinfacht.",
   controls:{btn:[{k:"nk",label:"Quelle:",opts:[["a","α-Strahler"],["b","β-Strahler"],["0","keine"]]}]},
   cfg:{mode:"nebel"}, alt:"Spuren in der Nebelkammer"},

  {kicker:"Schritt 1", title:"Ein Treffer in der Zelle",
   html:"<p>Trifft die Strahlung die DNA im Zellkern, gibt es drei mögliche Folgen.</p>",
   ask:"Welche Folge ist für den Körper am gefährlichsten, und warum?",
   note:"Die meisten DNA-Schäden werden repariert. Gefährlich sind Veränderungen, die bleiben: somatische Spätschäden wie Leukämie oder Krebs, bei Keimzellen genetische Schäden. Frühschäden (Strahlenkrankheit) erst ab etwa 1000 mSv auf einmal.",
   controls:{btn:[{k:"treffer",label:"Folge:",opts:[["1","Reparatur"],["2","Zelltod"],["3","Veränderung"]]}]},
   cfg:{mode:"zelle"}, alt:"Strahlung trifft die DNA im Zellkern"},

  {kicker:"Schritt 2", title:"Meine Jahresdosis",
   html:"<p>Stelle ein, was bei dir in einem Jahr zusammenkommt. Die Dosis misst man in Millisievert (mSv).</p>",
   ask:"Welcher Posten ist bei dir am größten? Was kannst du selbst beeinflussen?",
   note:"Werte nach BfS: Radon im Mittel 1,1 mSv (in Gegenden mit viel Radon, z. B. Teile des Schwarzwalds, deutlich mehr), Boden 0,4, Nahrung 0,3, Weltall 0,3 mSv. Flug Frankfurt–New York und zurück etwa 0,1 mSv, Röntgen Brustkorb 0,01 bis 0,03 mSv, CT des Kopfes etwa 2 mSv. Der Grenzwert von 1 mSv für die Bevölkerung gilt für Anlagen und Technik, nicht für Medizin.",
   controls:{btn:[{k:"radon",label:"Radon im Haus:",opts:[["0.5","wenig"],["1.1","normal"],["3","viel"]]}],
             sl:[{k:"fl",label:"Transatlantikflüge (hin und zurück)",min:0,max:10,step:1,fmt:function(v){return v}},{k:"rx",label:"Röntgenbilder Brustkorb",min:0,max:5,step:1,fmt:function(v){return v}},{k:"ct",label:"CT des Kopfes",min:0,max:2,step:1,fmt:function(v){return v}}],reset:{fl:0,rx:0,ct:0}},
   cfg:{mode:"dosis"}, alt:"Balken der Jahresdosis"},

  {kicker:"Schritt 3", title:"Wie schütze ich mich?",
   html:"<p>Verändere Abstand, Aufenthaltsdauer und Abschirmung. Der Balken zeigt die Dosis im Vergleich zum Start.</p>",
   ask:"Welche der drei Maßnahmen wirkt am stärksten?",
   note:"Gerechnet: Dosis proportional zur Zeit, umgekehrt proportional zum Quadrat des Abstands, Blei halbiert alle 1,2 cm (γ-Strahlung von Co-60). Dazu kommen die zwei weiteren A-Regeln: Aktivität klein halten, nichts in den Körper aufnehmen.",
   controls:{sl:[{k:"ab",label:"Abstand",min:1,max:4,step:0.5,fmt:function(v){return komma(v,1)+" m"}},{k:"zeit",label:"Aufenthalt",min:1,max:30,step:1,fmt:function(v){return v+" min"}},{k:"blei",label:"Blei",min:0,max:6,step:0.2,fmt:function(v){return komma(v,1)+" cm"}}],reset:{ab:2,zeit:10,blei:0}},
   cfg:{mode:"schutz"}, alt:"Person vor einer Strahlenquelle"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Ionisierende Strahlung schlägt Elektronen aus Atomen. Trifft sie die DNA, wird die Zelle repariert, stirbt ab oder verändert sich.</li><li>Die Dosis misst man in Millisievert. In Deutschland sind es im Schnitt etwa 2,1 mSv natürlich und 1,5 mSv aus der Medizin pro Jahr.</li><li>Schutz: Abstand, kurze Aufenthaltsdauer, Abschirmung, wenig Aktivität, nichts aufnehmen.</li></ul>",
   askLabel:"Probier's aus", ask:"Such auf der Radonkarte des Bundesamts für Strahlenschutz deinen Wohnort.",
   cfg:{mode:"dosis"}, alt:"Jahresdosis"}
 ]};
})();
