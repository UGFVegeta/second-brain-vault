/* Mondlabor · Leitfrage 5: Warum sieht der Mond nicht immer gleich aus? (nicht maßstabsgetreu) */
(function(){
"use strict";
var S={woche:"1", tag:7.4, pos:"0", off:0, my:0};
var HELL="#FFF6D8", DUNKEL="#26324A", ERDE="#3B7CC4", T=29.5;

/* beleuchteter Teil, von der Erde (Nordhalbkugel) aus gesehen; f = Anteil am Umlauf */
function phasePfad(x,y,r,f){
  f=((f%1)+1)%1; if(f<0.005||f>0.995) return "";
  var k=Math.cos(2*Math.PI*f), rechts=f<0.5, rx=Math.max(Math.abs(k)*r,0.01);
  var s1=rechts?1:0, s2=k>0?(rechts?0:1):(rechts?1:0);
  return '<path d="M'+x+' '+(y-r)+' A'+r+' '+r+' 0 0 '+s1+' '+x+' '+(y+r)+' A'+G.f1(rx)+' '+r+' 0 0 '+s2+' '+x+' '+(y-r)+'Z" fill="'+HELL+'"/>';
}
function mondBild(x,y,r,f){ return G.circ(x,y,r,DUNKEL)+phasePfad(x,y,r,f)+G.circ(x,y,r,"none",' stroke="#4D5E77" stroke-width="1.5"'); }
function mondOben(x,y,r){ return G.circ(x,y,r,DUNKEL)+'<path d="M'+x+' '+(y-r)+' A'+r+' '+r+' 0 0 0 '+x+' '+(y+r)+'Z" fill="'+HELL+'"/>'; }
function erde(x,y,r){ return G.circ(x,y,r,ERDE)+'<path d="M'+x+' '+(y-r)+' A'+r+' '+r+' 0 0 1 '+x+' '+(y+r)+'Z" fill="#05080F" fill-opacity=".45"/>'; }
function name(f){
  f=((f%1)+1)%1;
  if(f<0.03||f>0.97) return "Neumond"; if(f<0.22) return "zunehmende Sichel"; if(f<0.28) return "zunehmender Halbmond";
  if(f<0.47) return "zunehmender Mond"; if(f<0.53) return "Vollmond"; if(f<0.72) return "abnehmender Mond";
  if(f<0.78) return "abnehmender Halbmond"; return "abnehmende Sichel";
}
function sterne(){ var o="", seed=11, i; function r(){seed=(seed*9301+49297)%233280; return seed/233280;} for(i=0;i<40;i++) o+=G.circ(10+r()*820,10+r()*420,r()*1.3+0.4,"#FFFFFF",' opacity="'+(0.3+r()*0.5).toFixed(2)+'"'); return o; }

function himmel(){
  var f=(+S.woche-1)*0.25;
  return {svg:sterne()+'<circle cx="420" cy="210" r="140" fill="url(#gGlow)" opacity="'+(0.05+0.25*(1-Math.cos(2*Math.PI*f))/2)+'"/>'+mondBild(420,210,90,f)+G.txt(420,410,S.woche+". Woche","mid dim")};
}

function bahn(cfg){
  var o=[], E=[330,220], R=140, f=cfg.pos!=null?[0,0.25,0.5,0.75][+S.pos]:(+S.tag/T), a=(180-360*f)*Math.PI/180;
  var M=[E[0]+R*Math.cos(a), E[1]+R*Math.sin(a)], i;
  o.push(sterne());
  for(i=0;i<6;i++) o.push(G.arrow(10,40+i*72,120,40+i*72,"#FFC53D",2,0.05*i,0.8));
  o.push(G.txt(12,26,"Sonnenlicht",""));
  o.push(G.circ(E[0],E[1],R,"none",' stroke="#4D5E77" stroke-width="1.5" stroke-dasharray="6 6"'));
  o.push(G.dash(E[0],E[1],M[0],M[1],"#9DB8FF",1.5,0,0.8));
  o.push(erde(E[0],E[1],24));
  o.push(mondOben(M[0],M[1],13)+G.circ(M[0],M[1],13,"none",' stroke="#4D5E77"'));
  o.push(G.txt(E[0],E[1]+48,"Erde","mid dim"));
  o.push(G.txt(M[0],M[1]+(M[1]>E[1]?34:-22),"Mond","mid dim"));
  /* Ansicht von der Erde */
  o.push(G.circ(700,150,86,"#05080F",' stroke="#27344A" stroke-width="2"')+mondBild(700,150,56,f));
  o.push(G.txt(700,262,"So siehst du ihn","mid")+G.txt(700,284,"von der Erde aus","mid"));
  o.push(G.txt(20,428,"Blick von oben auf den Nordpol","dim"));
  var pct=Math.round(50*(1-Math.cos(2*Math.PI*f)));
  return {svg:o.join(""), readout:(cfg.pos==null?'<span class="chip">Tag <b>'+(+S.tag).toFixed(1).replace(".",",")+'</b></span>':'')+'<span class="chip">Phase <b>'+name(f)+'</b></span><span class="chip">beleuchteter Teil sichtbar <b>'+pct+' %</b></span>'};
}

function modell(){
  var o=[], P=[430,250], R=110, f=[0,0.25,0.5,0.75][+S.pos], a=(180-360*f)*Math.PI/180, K=[P[0]+R*Math.cos(a),P[1]+R*Math.sin(a)];
  o.push(G.rect(0,0,840,440,"#FFC53D",0.03));
  o.push(G.circ(70,250,60,"url(#gGlow)")+G.circ(70,250,24,"url(#gSun)"));
  o.push(G.ray(94,250,K[0]-10,K[1],"#FFC53D",2,0,0.5));
  o.push(G.circ(P[0],P[1],30,"#C9B6A0")+G.circ(P[0]+13*Math.cos(a),P[1]+13*Math.sin(a),4,"#0A1120"));
  o.push('<line x1="'+G.f1(P[0]+22*Math.cos(a))+'" y1="'+G.f1(P[1]+22*Math.sin(a))+'" x2="'+G.f1(K[0]-12*Math.cos(a))+'" y2="'+G.f1(K[1]-12*Math.sin(a))+'" stroke="#C9B6A0" stroke-width="8" stroke-linecap="round"/>');
  o.push(mondOben(K[0],K[1],14)+G.circ(K[0],K[1],14,"none",' stroke="#9AAAC0"'));
  o.push(G.circ(730,120,70,"#05080F",' stroke="#27344A" stroke-width="2"')+mondBild(730,120,46,f));
  o.push(G.txt(70,320,"Lampe (Sonne)","mid dim")+G.txt(P[0],P[1]+62,"dein Kopf (Erde)","mid dim")+G.txt(730,218,"das siehst du","mid"));
  o.push(G.txt(20,428,"Blick von oben","dim"));
  return {svg:o.join(""), readout:'<span class="chip">Phase <b>'+name(f)+'</b></span>'};
}

/* Kern- und Halbschatten über die obersten und untersten Randpunkte (Schulnäherung) */
function linie(A,B,x){ return A[1]+(B[1]-A[1])*(x-A[0])/(B[0]-A[0]); }

function sofi(){
  var o=[], S0=[60,220], rs=50, M=[470,220+(+S.off)], rm=18, E=[740,220], re=60, X=E[0]-re;
  var kT=[[S0[0],S0[1]-rs],[M[0],M[1]-rm]], kB=[[S0[0],S0[1]+rs],[M[0],M[1]+rm]];
  var hT=[[S0[0],S0[1]-rs],[M[0],M[1]+rm]], hB=[[S0[0],S0[1]+rs],[M[0],M[1]-rm]];
  var ax=kT[0][0]+(kT[0][1]-kB[0][1])/((kB[1][1]-kB[0][1])/(kB[1][0]-kB[0][0])-(kT[1][1]-kT[0][1])/(kT[1][0]-kT[0][0]));
  var ay=linie(kT[0],kT[1],ax), XE=E[0]+re;
  o.push('<defs><clipPath id="erdeC"><circle cx="'+E[0]+'" cy="'+E[1]+'" r="'+re+'"/></clipPath></defs>');
  o.push(G.poly([[M[0],M[1]-rm],[XE,linie(hB[0],hB[1],XE)],[XE,linie(hT[0],hT[1],XE)],[M[0],M[1]+rm]],"#FFFFFF",0.10,"fade",0.8));
  o.push(G.poly([[M[0],M[1]-rm],[ax,ay],[M[0],M[1]+rm]],"#05080F",0.9,"fade",0.8));
  [hT,hB].forEach(function(l){ o.push(G.ray(l[0][0],l[0][1],XE,linie(l[0],l[1],XE),"#FFC53D",1.4,0.2,0.6)); });
  [kT,kB].forEach(function(l){ o.push(G.ray(l[0][0],l[0][1],ax,linie(l[0],l[1],ax),"#FFC53D",1.8,0.1)); });
  o.push(erde(E[0],E[1],re));
  o.push('<g clip-path="url(#erdeC)" class="fade" style="--d:1s">'+G.poly([[M[0],M[1]-rm],[XE,linie(hB[0],hB[1],XE)],[XE,linie(hT[0],hT[1],XE)],[M[0],M[1]+rm]],"#05080F",0.35)+G.poly([[M[0],M[1]-rm],[ax,ay],[M[0],M[1]+rm]],"#05080F",0.95)+'</g>');
  o.push(G.circ(S0[0],S0[1],rs*1.8,"url(#gGlow)")+G.circ(S0[0],S0[1],rs,"url(#gSun)"));
  o.push(G.circ(M[0],M[1],rm,"#9AAAC0"));
  var kern=ax>X && Math.abs(linie(kT[0],kT[1],X)-E[1]+(linie(kB[0],kB[1],X)-linie(kT[0],kT[1],X))/2)<re;
  var halbT=linie(hT[0],hT[1],X), halbB=linie(hB[0],hB[1],X), halb=Math.min(halbT,halbB)<E[1]+re && Math.max(halbT,halbB)>E[1]-re;
  o.push(G.txt(S0[0],S0[1]+rs+34,"Sonne","mid dim")+G.txt(M[0],M[1]+rm+28,"Mond","mid dim")+G.txt(E[0],E[1]+re+30,"Erde","mid dim"));
  o.push(G.txt(20,428,"nicht maßstabsgetreu","dim"));
  var t=kern?"totale Sonnenfinsternis im Kernschatten":(halb?"nur teilweise Finsternis (Halbschatten)":"keine Finsternis");
  return {svg:o.join(""), readout:'<span class="chip">Auf der Erde: <b>'+t+'</b></span>'};
}

function mofi(){
  var o=[], S0=[60,220], rs=50, E=[430,220], re=30, M=[700,220+(+S.my)], rm=12;
  var kT=[[S0[0],S0[1]-rs],[E[0],E[1]-re]], kB=[[S0[0],S0[1]+rs],[E[0],E[1]+re]];
  var hT=[[S0[0],S0[1]-rs],[E[0],E[1]+re]], hB=[[S0[0],S0[1]+rs],[E[0],E[1]-re]], X=830;
  var ku=linie(kT[0],kT[1],M[0]), kd=linie(kB[0],kB[1],M[0]), hu=linie(hB[0],hB[1],M[0]), hd=linie(hT[0],hT[1],M[0]);
  var imKern=M[1]-rm>=ku&&M[1]+rm<=kd, beruehrtKern=M[1]+rm>ku&&M[1]-rm<kd, imHalb=M[1]+rm>hu&&M[1]-rm<hd;
  o.push(G.poly([[E[0],E[1]-re],[X,linie(hB[0],hB[1],X)],[X,linie(hT[0],hT[1],X)],[E[0],E[1]+re]],"#FFFFFF",0.08,"fade",0.8));
  o.push(G.poly([[E[0],E[1]-re],[X,linie(kT[0],kT[1],X)],[X,linie(kB[0],kB[1],X)],[E[0],E[1]+re]],"#05080F",0.9,"fade",0.8));
  [kT,kB].forEach(function(l){ o.push(G.ray(l[0][0],l[0][1],X,linie(l[0],l[1],X),"#FFC53D",1.8,0.1)); });
  o.push(G.circ(S0[0],S0[1],rs*1.8,"url(#gGlow)")+G.circ(S0[0],S0[1],rs,"url(#gSun)"));
  o.push(erde(E[0],E[1],re));
  var farbe=imKern?"#9A3B24":(beruehrtKern?"#E8DCC0":(imHalb?"#CFC7B0":HELL));
  o.push(G.circ(M[0],M[1],rm,farbe));
  if(beruehrtKern&&!imKern) o.push('<defs><clipPath id="mk"><circle cx="'+M[0]+'" cy="'+M[1]+'" r="'+rm+'"/></clipPath></defs><g clip-path="url(#mk)">'+G.rect(M[0]-rm,ku,2*rm,kd-ku,"#9A3B24")+'</g>');
  o.push(G.dash(M[0],30,M[0],410,"#4D5E77",1,0,0.6));
  o.push(G.txt(S0[0],S0[1]+rs+34,"Sonne","mid dim")+G.txt(E[0],E[1]+re+30,"Erde","mid dim")+G.txt(M[0]+22,M[1]+6,"Mond",""));
  o.push(G.txt(560,40,"Mondbahn","mid dim")+G.txt(20,428,"nicht maßstabsgetreu","dim"));
  var t=imKern?"totale Mondfinsternis":(beruehrtKern?"teilweise Mondfinsternis":(imHalb?"Halbschatten: kaum zu sehen":"normaler Vollmond"));
  return {svg:o.join(""), readout:'<span class="chip"><b>'+t+'</b></span>'+(imKern?'<span class="chip">Der Mond leuchtet kupferrot</span>':'')};
}

window.LAB={state:S,
 draw:function(cfg){ return {himmel:himmel,bahn:bahn,modell:modell,sofi:sofi,mofi:mofi}[cfg.mode](cfg); },
 QZ:[
  {q:"Warum sieht man den Mond bei Neumond nicht?",
   o:["Die Erde verdeckt ihn","Uns ist seine unbeleuchtete Seite zugewandt","Er steht dann hinter der Sonne"],a:1,
   w:"Bei Neumond steht der Mond zwischen Sonne und Erde. Die beleuchtete Hälfte zeigt von uns weg."},
  {q:"Am Abendhimmel siehst du eine Sichel, deren rechte Seite hell ist. Welche Phase ist das?",
   o:["zunehmender Mond","abnehmender Mond","Vollmond"],a:0,
   w:"Auf der Nordhalbkugel ist der zunehmende Mond rechts beleuchtet."},
  {q:"Warum gibt es nicht jeden Monat eine Sonnenfinsternis?",
   o:["Die Mondbahn ist etwas gegen die Erdbahn geneigt","Der Mond ist zu klein","Die Sonne ist zu hell"],a:0,
   w:"Meist zieht der Mondschatten über oder unter der Erde vorbei. Nur selten stehen Sonne, Mond und Erde genau auf einer Linie."},
  {q:"Bei welcher Mondphase kann eine Mondfinsternis stattfinden?",
   o:["bei Neumond","bei Halbmond","bei Vollmond"],a:2,
   w:"Nur bei Vollmond steht die Erde zwischen Sonne und Mond."}
 ],
 scenes:[
  {kicker:"Optik · Leitfrage 5", title:"Warum sieht der Mond nicht immer gleich aus?",
   html:"<p>Vier Blicke zum Mond, jeweils eine Woche später. Schalte die Wochen durch.</p>",
   ask:"Was verändert sich? Hast du eine Idee, woran das liegt?",
   note:"Passt zur Beobachte-Folie. Vermutungen sammeln, noch nicht auflösen.",
   controls:{btn:[{k:"woche",label:"Woche:",opts:[["1","1."],["2","2."],["3","3."],["4","4."]]}]},
   cfg:{mode:"himmel"}, alt:"Der Mond in vier Wochen"},

  {kicker:"Schritt 1", title:"Der Mond ist ein beleuchteter Körper",
   html:"<p>Die Sonne beleuchtet immer genau eine Hälfte des Mondes. Der Mond läuft in etwa 29,5 Tagen einmal um die Erde.</p><p>Schiebe den Mond mit dem Regler auf seiner Bahn. Rechts siehst du, wie er von der Erde aus aussieht.</p>",
   ask:"Wo steht der Mond bei Vollmond, wo bei Neumond?",
   note:"Die hellen Hälften zeigen immer zur Sonne. Nur der Blickwinkel von der Erde ändert sich. Am Tellurium (Phywe) lässt sich dasselbe vorne echt zeigen.",
   controls:{sl:[{k:"tag",label:"Tag seit Neumond",min:0,max:29.5,step:0.1,fmt:function(v){return v.toFixed(1).replace(".",",")}}]},
   cfg:{mode:"bahn"}, alt:"Mondbahn von oben mit Sonnenlicht und Ansicht von der Erde"},

  {kicker:"Versuch", title:"Kopf, Kugel, Lampe",
   html:"<p>Das ist euer Versuch mit der Styroporkugel. Du drehst dich nach links im Kreis, die Kugel bleibt vor deinem Gesicht.</p>",
   ask:"Bei welcher Stellung siehst du den zunehmenden Halbmond?",
   note:"Passt zum Versuchsblatt W08. Ähnliche Idee im Buch S. 40 (Globus, Lampe und Papierkugel am Faden). Die Kugel höher als den Kopf halten, sonst gibt es bei „Lampe hinter dir“ eine Mondfinsternis.",
   controls:{btn:[{k:"pos",label:"Stellung:",opts:[["0","zur Lampe"],["1","Lampe rechts"],["2","Lampe hinter dir"],["3","Lampe links"]]}]},
   cfg:{mode:"modell"}, alt:"Modellversuch von oben: Lampe, Kopf und Kugel"},

  {kicker:"Schritt 2", title:"Sonnenfinsternis",
   html:"<p>Der Mond steht zwischen Sonne und Erde. Nur wo sein Kernschatten die Erde trifft, ist die Sonne ganz verdeckt.</p><p>Die Mondbahn ist etwas geneigt. Verschiebe den Mond nach oben und unten.</p>",
   ask:"Warum gibt es nicht bei jedem Neumond eine Sonnenfinsternis?",
   note:"Sicherheit: Nie ohne Finsternisbrille in die Sonne schauen. Die Lochkamera ist ein sicherer Weg, eine Finsternis zu beobachten.",
   controls:{sl:[{k:"off",label:"Mond höher oder tiefer",min:-70,max:70,step:1,fmt:function(v){return v===0?"genau auf der Linie":(v<0?"höher":"tiefer")}}],reset:{off:0}},
   cfg:{mode:"sofi"}, alt:"Sonne, Mond und Erde mit Kern- und Halbschatten des Mondes"},

  {kicker:"Schritt 3", title:"Mondfinsternis",
   html:"<p>Die Erde steht zwischen Sonne und Mond. Der Mond taucht in den Kernschatten der Erde ein.</p><p>Schiebe den Mond auf seiner Bahn durch den Erdschatten.</p>",
   ask:"Warum ist der Mond in der Finsternis nicht ganz schwarz, sondern rötlich?",
   note:"Etwas Sonnenlicht wird in der Erdatmosphäre in den Schatten gelenkt. Dabei bleibt vor allem rotes Licht übrig, wie beim Sonnenuntergang. Mondfinsternisse sieht man ohne Schutz.",
   controls:{sl:[{k:"my",label:"Mond auf seiner Bahn",min:-110,max:110,step:1,fmt:function(v){return v===0?"Mitte":""}}],reset:{my:0}},
   cfg:{mode:"mofi"}, alt:"Sonne, Erde und Mond im Kernschatten der Erde"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>",
   note:"Frage 2 geht etwas über die Folien hinaus. Faustregel für die Nordhalbkugel: rechts hell heißt zunehmend."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Der Mond ist ein beleuchteter Körper. Die Sonne beleuchtet immer genau eine Hälfte. Auf seiner Bahn um die Erde sehen wir davon unterschiedlich viel.</li><li>Von Neumond bis zum nächsten Neumond vergehen etwa 29,5 Tage.</li><li>Bei einer Sonnenfinsternis steht der Mond zwischen Sonne und Erde. Sein Kernschatten trifft die Erde. Nur dort ist die Sonne ganz verdeckt.</li><li>Bei einer Mondfinsternis steht die Erde zwischen Sonne und Mond. Der Mond taucht in den Kernschatten der Erde ein.</li></ul>",
   askLabel:"Probier's aus", ask:"Schau eine Woche lang jeden Abend zur gleichen Zeit nach dem Mond und zeichne ihn. Wird er dicker oder dünner?",
   cfg:{mode:"bahn",pos:true}, alt:"Mondbahn von oben"}
 ]};
})();
