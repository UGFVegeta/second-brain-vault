/* Körperlabor · Leitfrage 2: Was passiert mit dem Licht, wenn es auf einen Körper trifft?
   Anteile sind grobe Richtwerte für den Unterricht (weißes Papier ~80 % Streuung, schwarzer Karton ~5 %,
   Fensterglas ~8 % Spiegelung an zwei Oberflächen und ~90 % Transmission). */
(function(){
"use strict";
var S={mat:"weiss", mat2:"butter", fl:"alu_k", th:20};
var M={
 weiss:{n:"weißes Blatt",s:80,a:20,t:0,fill:"#F2F2EE",op:1},
 schwarz:{n:"schwarzer Karton",s:5,a:95,t:0,fill:"#15171C",op:1},
 glas:{n:"Glasscheibe",s:8,a:2,t:90,fill:"#9FD4F2",op:0.3,spec:true},
 butter:{n:"Butterbrotpapier",s:35,a:10,t:55,fill:"#EDE6D2",op:0.75,diffT:true},
 brille:{n:"Sonnenbrillenglas",s:5,a:77,t:18,fill:"#3A4150",op:0.75,spec:true},
 alu:{n:"zerknitterte Alufolie",s:85,a:15,t:0,fill:"#C9CFD8",op:1},
 holz:{n:"helles Holzbrett",s:45,a:55,t:0,fill:"#C8A57A",op:1}
};
var B0=[122,330], P=[470,220];

function plate(cfg){
  var m=M[S[cfg.key]], o=[], dx=P[0]-B0[0], dy=P[1]-B0[1], l=Math.sqrt(dx*dx+dy*dy), ux=dx/l, uy=dy/l, i, ang, k;
  o.push('<g clip-path="url(#sc)">');
  o.push('<rect x="36" y="312" width="86" height="36" rx="5" fill="#3B4A63"/>');
  o.push(G.ray(B0[0],B0[1],P[0],P[1],"#FFC53D",6,0));
  /* Streuung nach links */
  if(m.s>0) for(i=0;i<11;i++){
    ang=(105+i*15)*Math.PI/180;
    o.push(G.ray(P[0],P[1],P[0]+150*Math.cos(ang),P[1]+150*Math.sin(ang),"#FFC53D",1.2+m.s/100*1.8,0.9+0.03*i,0.12+m.s/100*0.8));
  }
  /* Spiegelung (glatte Oberfläche) */
  if(m.spec) o.push(G.ray(P[0],P[1],P[0]-ux*330,P[1]+uy*330,"#FFC53D",1.5+m.s/100*8,0.9,0.3+m.s/100*3));
  /* Transmission */
  if(m.t>0){
    if(m.diffT) for(i=0;i<9;i++){
      ang=(-60+i*15)*Math.PI/180;
      o.push(G.ray(P[0],P[1],P[0]+150*Math.cos(ang),P[1]+150*Math.sin(ang),"#FFC53D",1.4+m.t/100*1.6,1.0+0.03*i,0.15+m.t/100*0.7));
    } else o.push(G.ray(P[0],P[1],P[0]+ux*420,P[1]+uy*420,"#FFC53D",1+5*m.t/100,1.0,0.25+0.75*m.t/100));
  }
  /* Platte und Absorption */
  o.push(G.rect(P[0]-9,80,18,280,m.fill,m.op,' stroke="#C6D1E1" stroke-opacity=".6" rx="2"'));
  if(m.a>=30){
    o.push(G.circ(P[0],P[1],28+m.a*0.3,"url(#gHeat)",' class="fade" style="--d:1s" opacity="'+(m.a/100)+'"'));
    for(k=-1;k<=1;k++) o.push('<path class="fade" style="--d:1.2s" d="M'+(P[0]+k*14)+' 74 q6 -9 0 -18 q-6 -9 0 -18" fill="none" stroke="#FF7A59" stroke-width="2.4" stroke-linecap="round" opacity="'+(m.a/100)+'"/>');
  }
  o.push(G.circ(P[0],P[1],7,"#FFF3C4"));
  /* Balken */
  var x=250, W=540, parts=[["Streuung",m.s,"#FFC53D"],["Absorption",m.a,"#FF7A59"],["Transmission",m.t,"#4CC9F0"]];
  parts.forEach(function(p){
    var w=W*p[1]/100; if(w<1) return;
    o.push(G.rect(x,392,w,28,p[2],0.9));
    if(w>=110) o.push('<text class="lbl mid" x="'+(x+w/2)+'" y="412" style="font-size:15px">'+p[0]+'</text>');
    x+=w;
  });
  o.push('</g>');
  o.push(G.txt(79,300,"Ray-Box","mid dim"));
  o.push(G.txt(P[0]+22,108,m.n,""));
  if(m.a>=50) o.push(G.txt(P[0]+22,138,"wird warm",""));
  return {svg:o.join(""), readout:'<span class="chip">Streuung ≈ <b>'+m.s+' %</b></span><span class="chip">Absorption ≈ <b>'+m.a+' %</b></span><span class="chip">Transmission ≈ <b>'+m.t+' %</b></span>'};
}

function eyeview(){
  var o=[], Q=[420,330], inc=40*Math.PI/180, Lp=[Q[0]-260*Math.sin(inc),Q[1]-260*Math.cos(inc)];
  var th=+S.th*Math.PI/180, E=[Q[0]+230*Math.sin(th),Q[1]-230*Math.cos(th)], rau=S.fl!=="alu_g", i, a, hit;
  var FL={rau:["#E8E4DA","Papier"],alu_k:["#C9CFD8","zerknitterte Alufolie"],alu_g:["#DDE6F2","glatte Alufolie"]}[S.fl];
  o.push('<g clip-path="url(#sc)">');
  o.push(G.rect(170,330,500,14,FL[0],1,' rx="2"'));
  if(!rau) o.push(G.rect(170,330,500,3,"#FFFFFF",0.8));
  if(S.fl==="alu_k") for(i=0;i<25;i++) o.push(G.rect(172+i*20,331,10,3,"#FFFFFF",0.5));
  o.push(G.arrow(Lp[0],Lp[1],Q[0],Q[1],"#FFC53D",3,0));
  if(rau){
    for(i=0;i<11;i++){ a=(-75+i*15)*Math.PI/180; o.push(G.ray(Q[0],Q[1],Q[0]+160*Math.sin(a),Q[1]-160*Math.cos(a),"#FFC53D",1.6,0.8+0.03*i,0.45)); }
    o.push(G.arrow(Q[0],Q[1],E[0]-18*Math.sin(th),E[1]+18*Math.cos(th),"#FFC53D",3,1.1));
    hit=true;
  }else{
    var R=[Q[0]+320*Math.sin(inc),Q[1]-320*Math.cos(inc)];
    o.push(G.arrow(Q[0],Q[1],R[0],R[1],"#FFC53D",3,0.9));
    hit=Math.abs(+S.th-40)<=6;
  }
  o.push(G.bulb(Lp[0],Lp[1],true,14));
  o.push(G.eye(E[0],E[1],+S.th>0?-1:1,0.9));
  o.push('</g>');
  o.push(G.txt(Q[0],378,FL[1],"mid dim"));
  o.push(G.txt(Lp[0]-10,Lp[1]-24,"Lampe","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Licht im Auge <b>'+(hit?"ja":"kaum")+'</b></span>'+(rau?'<span class="chip">Von jedem Platz aus zu sehen</span>':'<span class="chip">Nur aus einer Richtung hell</span>')};
}

function vier(){
  var o=[], L=[150,220], T=[[560,90],[560,220],[560,350]];
  o.push('<g clip-path="url(#sc)">');
  T.forEach(function(t,i){ o.push(G.ray(L[0],L[1],t[0],t[1],"#FFC53D",3,0.1*i)); });
  var i, a;
  for(i=0;i<7;i++){ a=(120+i*20)*Math.PI/180; o.push(G.ray(T[0][0],T[0][1],T[0][0]+110*Math.cos(a),T[0][1]+110*Math.sin(a),"#FFC53D",1.5,0.9,0.6)); }
  o.push(G.circ(T[1][0],T[1][1],40,"url(#gHeat)",' class="fade" style="--d:1s"'));
  var dx=T[2][0]-L[0], dy=T[2][1]-L[1];
  o.push(G.arrow(T[2][0],T[2][1],T[2][0]+dx*0.55,T[2][1]+dy*0.55,"#FFC53D",3,1));
  o.push(G.rect(T[0][0]-8,40,16,100,"#F2F2EE",1,' rx="2"')+G.rect(T[1][0]-8,170,16,100,"#15171C",1,' rx="2" stroke="#4D5E77"')+G.rect(T[2][0]-8,300,16,100,"#9FD4F2",0.35,' rx="2" stroke="#C6D1E1"'));
  o.push(G.bulb(L[0],L[1],true,16));
  o.push('</g>');
  o.push(G.txt(L[0],L[1]+56,"Emission","mid"));
  o.push(G.txt(600,86,"Streuung",""));
  o.push(G.txt(600,226,"Absorption",""));
  o.push(G.txt(600,322,"Transmission",""));
  return {svg:o.join("")};
}

window.LAB={state:S,
 draw:function(cfg){ return {plate:plate,eye:eyeview,vier:vier}[cfg.mode](cfg); },
 QZ:[
  {q:"Auf schwarzem Karton sieht man trotzdem einen schwachen Lichtfleck. Warum?",
   o:["Der Karton leuchtet selbst ein wenig","Ein kleiner Teil des Lichts wird gestreut","Das Licht geht durch den Karton hindurch"],a:1,
   w:"Schwarz verschluckt den größten Teil des Lichts, aber nicht alles. Den Rest wirft der Karton zurück. Nur deshalb kannst du ihn überhaupt sehen."},
  {q:"Durch Butterbrotpapier scheint Licht, aber du erkennst keine klaren Umrisse. Was passiert?",
   o:["Nur Absorption","Transmission und Streuung gleichzeitig","Nur Spiegelung"],a:1,
   w:"Ein Teil des Lichts geht hindurch, wird dabei aber in alle Richtungen verteilt. Deshalb verschwimmen die Umrisse."},
  {q:"Warum wird ein schwarzes Auto in der Sonne heißer als ein weißes?",
   o:["Es absorbiert mehr Licht","Es streut mehr Licht","Es lässt mehr Licht durch"],a:0,
   w:"Absorbiertes Licht ist nicht weg. Es wird zu Wärme."},
  {q:"Das weiße Blatt siehst du von jedem Platz im Raum aus. Warum?",
   o:["Es wirft das Licht in viele Richtungen zurück","Es leuchtet selbst","Es lässt das Licht hindurch"],a:0,
   w:"Das ist Streuung. Von der rauen Oberfläche geht Licht in alle Richtungen, also auch zu deinem Platz."}
 ],
 scenes:[
  {kicker:"Optik · Leitfrage 2", title:"Was passiert mit dem Licht?",
   html:"<p>Dieselbe Ray-Box, drei Körper. Das ist euer Versuch aus dem Unterricht.</p>",
   ask:"Wähle Blatt, Karton und Glasscheibe nacheinander. Was passiert jeweils mit dem Licht?",
   note:"Passt zum Versuchsblatt W04. Die Prozente sind grobe Richtwerte.",
   controls:{btn:[{k:"mat",label:"Körper:",opts:[["weiss","weißes Blatt"],["schwarz","schwarzer Karton"],["glas","Glasscheibe"]]}]},
   cfg:{mode:"plate",key:"mat"}, alt:"Lichtstrahl trifft auf einen Körper"},

  {kicker:"Schritt 1", title:"Vier Möglichkeiten",
   html:"<dl class=\"terms\"><div><dt>Emission</dt><dd>Ein Körper sendet selbst Licht aus.</dd></div><div><dt>Streuung</dt><dd>Das Licht wird in viele Richtungen zurückgeworfen.</dd></div><div><dt>Absorption</dt><dd>Das Licht wird verschluckt. Der Körper wird warm.</dd></div><div><dt>Transmission</dt><dd>Das Licht geht hindurch.</dd></div></dl>",
   ask:"Welche der vier Möglichkeiten hast du im Versuch gesehen?",
   note:"Die Fachbegriffe stehen auch auf der Folie. Hier nur wiederholen.",
   cfg:{mode:"vier"}, alt:"Emission, Streuung, Absorption und Transmission in einem Bild"},

  {kicker:"Experiment", title:"Meist passiert mehreres gleichzeitig",
   html:"<p>Probiere weitere Körper aus. Achte auf den Balken unten: Er zeigt, wie sich das Licht ungefähr aufteilt.</p><p class=\"small\">Die Prozentzahlen sind grobe Richtwerte.</p>",
   ask:"Bei welchem Körper passieren alle drei Dinge gleichzeitig?",
   note:"Auch schwarzer Karton streut noch etwa 5 %. Deshalb sieht man ihn.",
   controls:{btn:[{k:"mat2",label:"Körper:",opts:[["weiss","weißes Blatt"],["schwarz","schwarzer Karton"],["glas","Glasscheibe"],["butter","Butterbrotpapier"],["brille","Sonnenbrille"],["alu","Alufolie, zerknittert"],["holz","Holzbrett"]]}]},
   cfg:{mode:"plate",key:"mat2"}, alt:"Aufteilung des Lichts bei verschiedenen Körpern"},

  {kicker:"Schritt 2", title:"Zerknittert oder glatt?",
   html:"<p>Eine Taschenlampe leuchtet schräg auf Alufolie. Einmal ist die Folie zerknittert, einmal ganz glatt. Verschiebe dein Auge.</p><p class=\"small\">Die glatte Folie wirkt wie ein Spiegel. Spiegel sind später dran.</p>",
   ask:"Warum siehst du die zerknitterte Folie von jedem Platz aus, die glatte aber nur von einer Stelle hell?",
   note:"Idee aus Erlebnis Physik 7–9, S. 45 A. Echt vorführbar im dunklen Raum mit Taschenlampe und zwei Stücken Alufolie. Zerknittert: Streuung in alle Richtungen. Glatt: heller Fleck nur in einer Richtung.",
   controls:{btn:[{k:"fl",label:"Fläche:",opts:[["alu_k","Alufolie zerknittert"],["alu_g","Alufolie glatt"],["rau","Papier"]]}],
     sl:[{k:"th",label:"Wo ist dein Auge?",min:-15,max:80,step:1,fmt:function(v){return v+"°"}}]},
   cfg:{mode:"eye"}, alt:"Raue und glatte Fläche mit Auge"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>",
   note:"Frage 1 greift den schwarzen Karton aus dem Versuch auf."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Licht kann ausgesendet (Emission), zurückgeworfen (Streuung), verschluckt (Absorption) oder durchgelassen (Transmission) werden.</li><li>Meist geschieht mehreres gleichzeitig.</li></ul>",
   askLabel:"Probier's aus", ask:"Halte im dunklen Zimmer eine Taschenlampe an deine Fingerkuppe. Was geht durch deinen Finger hindurch?",
   cfg:{mode:"vier"}, alt:"Emission, Streuung, Absorption und Transmission"}
 ]};
})();
