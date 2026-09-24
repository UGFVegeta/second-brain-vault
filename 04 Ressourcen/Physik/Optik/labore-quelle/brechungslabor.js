/* Brechungslabor · Leitfrage 7: Warum sieht der Strohhalm im Wasser geknickt aus?
   Brechungswinkel nach dem Brechungsgesetz (Wasser n = 1,33, Glas n = 1,5, Diamant n = 2,42). */
(function(){
"use strict";
var S={wasser:"1", a:40, richtung:"rein", stoff:"glas", w:40, becher:"leer"};
var RAD=Math.PI/180, N={wasser:1.33, glas:1.5, diamant:2.42};
var NAME={wasser:"Wasser", glas:"Glas", diamant:"Diamant"};
function brich(a,n1,n2){ var s=n1*Math.sin(a*RAD)/n2; return s>1?null:Math.asin(s)/RAD; }
function griech(x,y,t,col){ return '<text x="'+G.f1(x)+'" y="'+G.f1(y)+'" font-family="Georgia,serif" font-style="italic" font-size="22" fill="'+(col||"#FFFFFF")+'" text-anchor="middle">'+t+'</text>'; }
function bogen(M,a0,a1,r,col){
  var x0=M[0]+r*Math.cos(a0*RAD), y0=M[1]-r*Math.sin(a0*RAD), x1=M[0]+r*Math.cos(a1*RAD), y1=M[1]-r*Math.sin(a1*RAD);
  return '<path d="M'+G.f1(x0)+' '+G.f1(y0)+' A'+r+' '+r+' 0 0 '+(a1>a0?0:1)+' '+G.f1(x1)+' '+G.f1(y1)+'" fill="none" stroke="'+col+'" stroke-width="2"/>';
}

function glas(){
  var o=[], voll=S.wasser==="1", x0=300, x1=540, top=70, wy=180, bot=390, n=1.33;
  o.push('<path d="M'+x0+' '+top+' L'+(x0+14)+' '+bot+' L'+(x1-14)+' '+bot+' L'+x1+' '+top+'" fill="#141C28" stroke="#9AAAC0" stroke-width="3"/>');
  if(voll) o.push('<path d="M'+(x0+5)+' '+wy+' L'+(x0+14)+' '+(bot-2)+' L'+(x1-14)+' '+(bot-2)+' L'+(x1-5)+' '+wy+'Z" fill="#3B7CC4" fill-opacity=".45"/>'+G.rect(x0+5,wy-1,x1-x0-10,3,"#9DB8FF"));
  /* echter Strohhalm: gerade von (340,30) nach (470,380) */
  var P0=[350,30], P1=[470,375], t=(wy-P0[1])/(P1[1]-P0[1]), K=[P0[0]+(P1[0]-P0[0])*t, wy];
  o.push('<line x1="'+P0[0]+'" y1="'+P0[1]+'" x2="'+G.f1(K[0])+'" y2="'+wy+'" stroke="#FF7A59" stroke-width="12" stroke-linecap="round"/>');
  if(voll){
    /* scheinbare Lage: Tiefe unter der Oberfläche wirkt um den Faktor n kleiner (Blick von schräg oben, Näherung) */
    var sy=wy+(P1[1]-wy)/n;
    o.push('<line x1="'+G.f1(K[0])+'" y1="'+wy+'" x2="'+P1[0]+'" y2="'+G.f1(sy)+'" stroke="#FF7A59" stroke-width="12" stroke-linecap="round"/>');
    o.push('<line x1="'+G.f1(K[0])+'" y1="'+wy+'" x2="'+P1[0]+'" y2="'+P1[1]+'" stroke="#FF7A59" stroke-width="2" stroke-dasharray="6 6" opacity=".6"/>');
  }else o.push('<line x1="'+G.f1(K[0])+'" y1="'+wy+'" x2="'+P1[0]+'" y2="'+P1[1]+'" stroke="#FF7A59" stroke-width="12" stroke-linecap="round"/>');
  o.push(G.eye(150,120,1,1));
  o.push(G.txt(150,170,"Blick von schräg oben","mid dim"));
  if(voll) o.push(G.txt(560,wy+6,"Wasseroberfläche","")+G.txt(560,330,"gestrichelt: wo der","")+G.txt(560,354,"Strohhalm wirklich ist",""));
  return {svg:o.join(""), readout:'<span class="chip">Strohhalm sieht <b>'+(voll?"geknickt":"gerade")+'</b> aus</span>'};
}

function halbzylinder(cfg){
  var o=[], M=[420,230], R=180, a=+S.a, n=cfg.stoff?N[S.stoff]:1.5, rein=cfg.stoff?true:S.richtung==="rein", i;
  var n1=rein?1:n, n2=rein?n:1, b=brich(a,n1,n2);
  /* Scheibe */
  o.push('<circle cx="'+M[0]+'" cy="'+M[1]+'" r="'+(R+20)+'" fill="#141C28" stroke="#4D5E77" stroke-width="2"/>');
  for(i=0;i<360;i+=10) o.push('<line x1="'+G.f1(M[0]+(R+20)*Math.cos(i*RAD))+'" y1="'+G.f1(M[1]-(R+20)*Math.sin(i*RAD))+'" x2="'+G.f1(M[0]+(R+8)*Math.cos(i*RAD))+'" y2="'+G.f1(M[1]-(R+8)*Math.sin(i*RAD))+'" stroke="#4D5E77" stroke-width="1.5"/>');
  /* Halbzylinder unten (Glas), Luft oben */
  o.push('<path d="M'+(M[0]-R)+' '+M[1]+' A'+R+' '+R+' 0 0 0 '+(M[0]+R)+' '+M[1]+'Z" fill="#9DB8FF" fill-opacity=".22" stroke="#9DB8FF" stroke-width="2"/>');
  o.push(G.dash(M[0],M[1]-R-20,M[0],M[1]+R+20,"#9DB8FF",1.6,0,0.8));
  /* Strahlen: rein = von oben links (Luft) ins Glas; raus = von unten links (Glas, durch die runde Seite senkrecht) in die Luft */
  var L=R, ein, aus, ref;
  if(rein){ ein=[M[0]-L*Math.sin(a*RAD), M[1]-L*Math.cos(a*RAD)]; ref=[M[0]+L*Math.sin(a*RAD), M[1]-L*Math.cos(a*RAD)];
            if(b!=null) aus=[M[0]+L*Math.sin(b*RAD), M[1]+L*Math.cos(b*RAD)]; }
  else    { ein=[M[0]-L*Math.sin(a*RAD), M[1]+L*Math.cos(a*RAD)]; ref=[M[0]+L*Math.sin(a*RAD), M[1]+L*Math.cos(a*RAD)];
            if(b!=null) aus=[M[0]+L*Math.sin(b*RAD), M[1]-L*Math.cos(b*RAD)]; }
  o.push(G.arrow(ein[0],ein[1],M[0],M[1],"#FFC53D",3.2,0));
  o.push(G.arrow(M[0],M[1],ref[0],ref[1],"#FFC53D",b==null?3.2:1.4,0.8,b==null?1:0.45));
  if(b!=null) o.push(G.arrow(M[0],M[1],aus[0],aus[1],"#FFC53D",3.2,0.8));
  if(rein){ o.push(bogen(M,90,90+a,60,"#FF8A3D")); if(b!=null) o.push(bogen(M,-90,-90+b,70,"#4CC9F0")); }
  else    { o.push(bogen(M,-90-a,-90,60,"#FF8A3D")); if(b!=null) o.push(bogen(M,90-b,90,70,"#4CC9F0")); }
  var aw=rein?90+a/2:-90-a/2, bw=rein?-90+b/2:90-b/2;
  o.push(griech(M[0]+84*Math.cos(aw*RAD),M[1]-84*Math.sin(aw*RAD)+8,"α","#FF8A3D"));
  if(b!=null) o.push(griech(M[0]+96*Math.cos(bw*RAD),M[1]-96*Math.sin(bw*RAD)+8,"β","#4CC9F0"));
  o.push(G.txt(M[0]-R-10,M[1]-24,"Luft","end dim")+G.txt(M[0]-R-10,M[1]+34,cfg.stoff?NAME[S.stoff]:"Glas","end dim"));
  var rd='<span class="chip">Einfallswinkel α <b>'+a+'°</b></span>';
  rd+= b==null?'<span class="chip"><b>kein gebrochener Strahl</b>: alles wird reflektiert</span>':'<span class="chip">Brechungswinkel β <b>'+Math.round(b)+'°</b></span><span class="chip">'+(b<a-0.5?"zum Lot hin":(b>a+0.5?"vom Lot weg":"ungebrochen"))+'</span>';
  return {svg:o.join(""), readout:rd};
}

function wellen(){
  /* Wellenfronten: oben Abstand 40, unten 40/1,33. Durchgehende Front an der Grenze -> Brechungsgesetz */
  var o=[], Y=220, a=+S.w, b=brich(a,1,1.33), l1=40, l2=40/1.33, k, x;
  o.push(G.rect(0,Y,840,220,"#3B7CC4",0.35)+G.rect(0,Y-1,840,3,"#9DB8FF"));
  o.push('<defs><clipPath id="oben"><rect x="0" y="0" width="840" height="'+Y+'"/></clipPath><clipPath id="unten"><rect x="0" y="'+Y+'" width="840" height="'+(440-Y)+'"/></clipPath></defs>');
  var s1=Math.sin(a*RAD), c1=Math.cos(a*RAD), s2=Math.sin(b*RAD), c2=Math.cos(b*RAD), X0=420;
  var go='<g clip-path="url(#oben)">', gu='<g clip-path="url(#unten)">';
  for(k=-20;k<=20;k++){
    /* oben: (x-X0)*s1 + (y-Y)*c1 = k*l1 ; Linie senkrecht zur Laufrichtung */
    var p=[X0+k*l1*s1, Y+k*l1*c1], d=[c1,-s1];
    go+='<line x1="'+G.f1(p[0]-900*d[0])+'" y1="'+G.f1(p[1]-900*d[1])+'" x2="'+G.f1(p[0]+900*d[0])+'" y2="'+G.f1(p[1]+900*d[1])+'" stroke="#FFC53D" stroke-opacity=".55" stroke-width="2"/>';
    var q=[X0+k*l2*s2, Y+k*l2*c2], e=[c2,-s2];
    gu+='<line x1="'+G.f1(q[0]-900*e[0])+'" y1="'+G.f1(q[1]-900*e[1])+'" x2="'+G.f1(q[0]+900*e[0])+'" y2="'+G.f1(q[1]+900*e[1])+'" stroke="#FFC53D" stroke-opacity=".55" stroke-width="2"/>';
  }
  o.push(go+'</g>'+gu+'</g>');
  o.push(G.arrow(X0-200*s1,Y-200*c1,X0,Y,"#FFFFFF",3,0)+G.arrow(X0,Y,X0+190*s2,Y+190*c2,"#FFFFFF",3,0.6));
  o.push(G.dash(X0,Y-200,X0,Y+200,"#9DB8FF",1.5,0,0.7));
  o.push(G.txt(30,40,"Luft: schnell, weite Abstände","")+G.txt(30,Y+40,"Wasser: langsamer, enge Abstände",""));
  return {svg:o.join(""), readout:'<span class="chip">Einfallswinkel <b>'+a+'°</b></span><span class="chip">Brechungswinkel <b>'+Math.round(b)+'°</b></span>'};
}

function muenze(){
  var o=[], voll=S.becher==="voll", x0=330, x1=560, rim=150, bot=300, wy=158, C=[352,bot-6], E=[760,45], n=1.33;
  o.push('<rect x="'+x0+'" y="'+rim+'" width="'+(x1-x0)+'" height="'+(bot-rim)+'" fill="#141C28" stroke="#9AAAC0" stroke-width="4"/>');
  if(voll) o.push(G.rect(x0+2,wy,x1-x0-4,bot-wy-2,"#3B7CC4",0.45)+G.rect(x0+2,wy-1,x1-x0-4,3,"#9DB8FF"));
  o.push('<ellipse cx="'+C[0]+'" cy="'+C[1]+'" rx="16" ry="4" fill="#FFD34D"/>');
  var R=[x1,rim], sichtbar;
  if(!voll){
    /* gerade Sichtlinie vom Auge über den Becherrand */
    var yAtCoinX=E[1]+(R[1]-E[1])*(C[0]-E[0])/(R[0]-E[0]);
    sichtbar=yAtCoinX>=C[1];
    o.push(G.dash(E[0],E[1],x0,E[1]+(R[1]-E[1])*(x0-E[0])/(R[0]-E[0]),"#9AAAC0",2,0,0.8));
    o.push(G.ray(C[0],C[1],C[0]+(R[0]-C[0])*0.9,C[1]+(R[1]-C[1])*0.9,"#FFC53D",2.4,0.2,0.5));
  }else{
    /* Punkt P auf der Oberfläche suchen, so dass Licht von der Münze nach dem Brechungsgesetz ins Auge geht */
    var lo=C[0], hi=x1, P, i;
    for(i=0;i<60;i++){ var m=(lo+hi)/2; var sa=(m-C[0])/Math.hypot(m-C[0],C[1]-wy), sl=(E[0]-m)/Math.hypot(E[0]-m,wy-E[1]); if(n*sa>sl) hi=m; else lo=m; }
    P=[(lo+hi)/2,wy];
    var yRand=wy+(E[1]-wy)*(x1-P[0])/(E[0]-P[0]);
    sichtbar=yRand<=rim;
    o.push(G.ray(C[0],C[1],P[0],P[1],"#FFC53D",3,0.1));
    o.push(G.arrow(P[0],P[1],E[0]-26,E[1]+(P[1]-E[1])*26/(E[0]-P[0]),"#FFC53D",3,0.6,sichtbar?1:0.35));
    o.push(G.dash(P[0],P[1],P[0]-(E[0]-P[0])*0.9,P[1]+(P[1]-E[1])*0.9,"#9AAAC0",1.6,1,0.7));
  }
  o.push(G.eye(E[0],E[1],-1,1));
  o.push(G.txt(C[0],bot+34,"Münze","mid dim")+G.txt(E[0],E[1]+46,"Auge","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Münze sichtbar <b>'+(sichtbar?"ja":"nein")+'</b></span>'+(voll?'<span class="chip">Das Licht wird an der Oberfläche vom Lot weg gebrochen</span>':'<span class="chip">Der Becherrand verdeckt die Münze</span>')};
}

window.LAB={state:S,
 draw:function(cfg){ return {glas:glas,halb:halbzylinder,wellen:wellen,muenze:muenze}[cfg.mode](cfg); },
 QZ:[
  {q:"Licht geht von Luft in Wasser über. Wie wird es gebrochen?",
   o:["zum Lot hin","vom Lot weg","gar nicht"],a:0, w:"Von optisch dünn nach optisch dicht wird das Licht zum Lot hin gebrochen."},
  {q:"Licht trifft genau senkrecht (0°) auf die Wasseroberfläche. Was passiert?",
   o:["Es wird stark gebrochen","Es geht ungebrochen weiter","Es wird ganz reflektiert"],a:1, w:"Bei 0° ändert sich die Richtung nicht. Es wird nur langsamer."},
  {q:"Warum sieht ein Schwimmbecken flacher aus, als es ist?",
   o:["Das Wasser drückt den Boden hoch","Das Licht vom Boden wird an der Oberfläche gebrochen","Das Wasser ist blau gefärbt"],a:1,
   w:"Das Gehirn verlängert die gebrochenen Strahlen geradlinig. Der Boden scheint höher zu liegen."},
  {q:"Welcher Stoff bricht das Licht am stärksten?",
   o:["Wasser","Glas","Diamant"],a:2, w:"Je langsamer das Licht im Stoff ist, desto stärker wird es gebrochen."}
 ],
 scenes:[
  {kicker:"Optik · Leitfrage 7", title:"Warum sieht der Strohhalm geknickt aus?",
   html:"<p>Ein gerader Strohhalm steht schräg in einem Glas. Schalte das Wasser ein und aus.</p>",
   ask:"Was verändert sich? Was vermutest du?", note:"Passt zur Beobachte-Folie. Echt zeigen: Glas, Wasser, Strohhalm.",
   controls:{btn:[{k:"wasser",label:"Wasser:",opts:[["0","ohne"],["1","mit"]]}]},
   cfg:{mode:"glas"}, alt:"Strohhalm im Wasserglas"},

  {kicker:"Versuch", title:"Lichtbrechung am Halbzylinder",
   html:"<p>Das ist euer Versuch mit dem Halbzylinder auf der Winkelscheibe. Der Strahl geht immer durch den Mittelpunkt.</p>",
   ask:"Wird das Licht zum Lot hin oder vom Lot weg gebrochen? Wechsle auch die Richtung.",
   note:"Passt zum Versuchsblatt W12. Von Glas nach Luft gibt es ab etwa 42° keinen gebrochenen Strahl mehr (Totalreflexion). Das kommt am Ende bei der Glasfaser wieder.",
   controls:{btn:[{k:"richtung",label:"Richtung:",opts:[["rein","Luft → Glas"],["raus","Glas → Luft"]]}],
     sl:[{k:"a",label:"Einfallswinkel α",min:0,max:80,step:1,fmt:function(v){return v+"°"}}],reset:{a:40}},
   cfg:{mode:"halb"}, alt:"Halbzylinder auf der Winkelscheibe mit Lichtstrahl"},

  {kicker:"Schritt 1", title:"Wasser, Glas oder Diamant?",
   html:"<p>Licht ist in Wasser, Glas und Diamant verschieden langsam. Je langsamer, desto stärker wird es gebrochen.</p>",
   ask:"Bei welchem Stoff ist der Brechungswinkel am kleinsten?",
   note:"„Optisch dichter“ heißt: Licht ist dort langsamer. Mit der Dichte in kg/m³ hat das nichts zu tun.",
   controls:{btn:[{k:"stoff",label:"Stoff:",opts:[["wasser","Wasser"],["glas","Glas"],["diamant","Diamant"]]}],
     sl:[{k:"a",label:"Einfallswinkel α",min:0,max:80,step:1,fmt:function(v){return v+"°"}}],reset:{a:40}},
   cfg:{mode:"halb",stoff:true}, alt:"Brechung an verschiedenen Stoffen"},

  {kicker:"Schritt 2", title:"Warum wird Licht gebrochen?",
   html:"<p>Stell dir die Lichtwelle wie eine Reihe von Läufern nebeneinander vor. Wer zuerst ins Wasser kommt, wird zuerst langsamer. Dadurch schwenkt die ganze Reihe.</p>",
   ask:"Was passiert, wenn das Licht genau senkrecht auf das Wasser trifft?",
   note:"Die gelben Linien sind Wellenfronten. Ihr Abstand wird im Wasser kleiner, weil das Licht dort langsamer ist.",
   controls:{sl:[{k:"w",label:"Einfallswinkel",min:0,max:70,step:1,fmt:function(v){return v+"°"}}],reset:{w:40}},
   cfg:{mode:"wellen"}, alt:"Wellenfronten beim Übergang von Luft in Wasser"},

  {kicker:"Alltag", title:"Die Münze im Becher",
   html:"<p>Du schaust so über den Rand eines Bechers, dass du die Münze gerade nicht mehr siehst. Dann wird Wasser eingefüllt.</p>",
   ask:"Warum taucht die Münze plötzlich auf?",
   note:"Klassischer Freihandversuch, gut als Einstieg oder Wiederholung. Gleicher Grund, warum ein Becken flacher aussieht.",
   controls:{btn:[{k:"becher",label:"Becher:",opts:[["leer","leer"],["voll","mit Wasser"]]}]},
   cfg:{mode:"muenze"}, alt:"Becher mit Münze und Auge am Rand"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Beim Übergang in ein anderes Material ändert Licht seine Richtung. Man sagt, es wird gebrochen. Der Grund: Licht ist in Wasser und Glas langsamer als in Luft.</li><li>Von Luft ins Wasser (optisch dünner → dichter): zum Lot hin. Von Wasser in die Luft (dichter → dünner): vom Lot weg.</li></ul>",
   askLabel:"Probier's aus", ask:"Leg eine Münze in eine leere Tasse und geh so weit zurück, dass du sie gerade nicht mehr siehst. Lass jemanden langsam Wasser eingießen.",
   cfg:{mode:"muenze"}, alt:"Münze im Becher"}
 ]};
})();
