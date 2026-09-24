/* Strahlenlabor · Leitfrage 3: Warum können wir nicht um die Ecke sehen?  (1 px = 1 mm) */
(function(){
"use strict";
var S={x:250, h1:220, h2:220, zwei:"0", a:200, b:20, ansicht:"wirklich", luft:"klar", spiegel:"0"};

/* Schnittpunkt Strecke P->Q mit Rechteck, liefert Parameter t des Eintritts oder null */
function hitRect(P,Q,R){
  var t0=0, t1=1, dx=Q[0]-P[0], dy=Q[1]-P[1], p=[-dx,dx,-dy,dy], q=[P[0]-R[0],R[0]+R[2]-P[0],P[1]-R[1],R[1]+R[3]-P[1]], i, r;
  for(i=0;i<4;i++){
    if(p[i]===0){ if(q[i]<0) return null; }
    else{ r=q[i]/p[i]; if(p[i]<0){ if(r>t1) return null; if(r>t0) t0=r; } else { if(r<t0) return null; if(r<t1) t1=r; } }
  }
  return t0;
}

function ecke(){
  var o=[], W=[380,0,80,262], B=[620,118], E=[+S.x,362], t=hitRect(B,E,W), vis=(t===null);
  o.push('<g clip-path="url(#sc)">');
  o.push(G.rect(0,0,840,440,"#FFC53D",0.04));
  o.push(G.rect(W[0],W[1],W[2],W[3],"#4D5E77"));
  for(var y=22;y<W[3];y+=22) o.push(G.rect(W[0],y,W[2],2,"#3B4A63"));
  o.push(G.rect(90,386,700,3,"#27344A"));
  if(vis){
    o.push(G.arrow(B[0],B[1],E[0],E[1]-22,"#FFC53D",3,0.1));
  }else{
    var hx=B[0]+(E[0]-B[0])*t, hy=B[1]+(E[1]-B[1])*t;
    o.push(G.ray(B[0],B[1],hx,hy,"#FFC53D",3,0.1));
    o.push(G.dash(hx,hy,E[0],E[1]-22,"#9AAAC0",2,0.8,0.6));
    o.push('<path class="fade" style="--d:.9s" d="M'+(hx-9)+' '+(hy-9)+' l18 18 M'+(hx+9)+' '+(hy-9)+' l-18 18" stroke="#FF7A59" stroke-width="4" stroke-linecap="round"/>');
    o.push('<path class="fade" style="--d:1.1s" d="M'+B[0]+' '+B[1]+' Q 470 330 '+E[0]+' '+(E[1]-22)+'" fill="none" stroke="#FF7A59" stroke-width="2" stroke-dasharray="4 8" opacity=".7"/>');
  }
  o.push(G.circ(B[0],B[1],22,"url(#gBall)"));
  o.push(G.circ(E[0],E[1],18,"#9FB2CF")+G.circ(E[0]-7,E[1]-10,4,"#0A1120")+G.circ(E[0]+7,E[1]-10,4,"#0A1120"));
  o.push('</g>');
  o.push(G.txt(420,290,"Mauer","mid dim"));
  o.push(G.txt(B[0]+34,B[1]+6,"Ball",""));
  o.push(G.txt(E[0],E[1]+46,"Du","mid dim"));
  o.push(G.txt(28,34,"Draufsicht","dim"));
  if(!vis) o.push(G.txt(560,360,"Licht macht keinen Bogen","mid"));
  return {svg:o.join(""), readout:'<span class="chip">Ball sichtbar <b>'+(vis?"ja":"nein")+'</b></span>'};
}

function blende(){
  var o=[], L=[100,220], X1=380, X2=560, XS=760, HALF=Math.tan(10*Math.PI/180), r=7;
  var h1=+S.h1, h2=+S.h2, zwei=S.zwei==="1";
  var inBeam=Math.abs(h1-L[1])<=(X1-L[0])*HALF;
  var k=(h1-L[1])/(X1-L[0]), y2=L[1]+k*(X2-L[0]), ys=L[1]+k*(XS-L[0]);
  var pass2=!zwei||Math.abs(y2-h2)<=r, spot=inBeam&&pass2&&ys>12&&ys<428;
  o.push('<g clip-path="url(#sc)">');
  o.push(G.poly([[L[0],L[1]],[X1,L[1]-(X1-L[0])*HALF],[X1,L[1]+(X1-L[0])*HALF]],"#FFC53D",0.28,"fade",0));
  if(inBeam){
    var end=pass2?XS:X2;
    o.push(G.ray(X1,h1,end,L[1]+k*(end-L[0]),"#FFC53D",3,0.4));
  }
  /* Blenden */
  o.push(G.rect(X1-6,0,12,h1-r,"#9FB2CF")+G.rect(X1-6,h1+r,12,440-h1-r,"#9FB2CF"));
  if(zwei) o.push(G.rect(X2-6,0,12,h2-r,"#9FB2CF")+G.rect(X2-6,h2+r,12,440-h2-r,"#9FB2CF"));
  o.push(G.rect(XS,0,24,440,"#FFE29A",0.85));
  if(spot) o.push(G.circ(XS+12,ys,26,"url(#gGlow)",' class="fade" style="--d:1.1s"')+G.circ(XS+12,ys,8,"#FFFFFF",' class="fade" style="--d:1.1s"'));
  o.push('<rect x="30" y="194" width="74" height="52" rx="6" fill="#3B4A63"/>');
  o.push(G.circ(L[0],L[1],7,"#FFF3C4"));
  o.push('</g>');
  o.push(G.txt(67,280,"Ray-Box","mid dim"));
  o.push(G.txt(X1,432,"Blende","mid dim"));
  if(zwei) o.push(G.txt(X2,432,"2. Blende","mid dim"));
  o.push(G.txt(XS+12,26,"Schirm","mid dim"));
  var why=!inBeam?"Das Loch liegt außerhalb des Lichtbündels.":(!pass2?"Die Löcher liegen nicht auf einer Geraden mit der Lampe.":"Lampe, Loch und Lichtpunkt liegen auf einer Geraden.");
  return {svg:o.join(""), readout:'<span class="chip">Lichtpunkt auf dem Schirm <b>'+(spot?"ja":"nein")+'</b></span><span class="chip">'+why+'</span>'};
}

function buendel(){
  var o=[], L=[90,220], a=+S.a, b=+S.b, xs=L[0]+a, X=830, i, ang;
  var yT=L[1]-b/2*(X-L[0])/a, yB=L[1]+b/2*(X-L[0])/a;
  var deg=2*Math.atan(b/2/a)*180/Math.PI, wcm=(yB-yT)/10;
  o.push('<g clip-path="url(#sc)">');
  for(i=0;i<24;i++){ ang=i*15*Math.PI/180; var len=Math.cos(ang)>0.2?Math.min(260,(xs-L[0])/Math.cos(ang)):70;
    o.push(G.ray(L[0],L[1],L[0]+len*Math.cos(ang),L[1]+len*Math.sin(ang),"#FFC53D",1.4,0.02*i,0.35)); }
  o.push(G.poly([[xs,L[1]-b/2],[X,yT],[X,yB],[xs,L[1]+b/2]],"#FFC53D",0.32,"fade",0.6));
  o.push(G.ray(xs,L[1]-b/2,X,yT,"#FFC53D",2,0.6)+G.ray(xs,L[1]+b/2,X,yB,"#FFC53D",2,0.6));
  o.push(G.rect(xs-5,0,10,L[1]-b/2,"#9FB2CF")+G.rect(xs-5,L[1]+b/2,10,440-L[1]-b/2,"#9FB2CF"));
  o.push(G.bulb(L[0],L[1],true,11));
  o.push('</g>');
  o.push(G.txt(L[0],L[1]+48,"Lampe","mid dim"));
  o.push(G.txt(xs,432,"Spalt","mid dim"));
  o.push(G.txt(820,Math.max(40,yT-14),deg<4?"fast parallel":"divergent","end"));
  return {svg:o.join(""), readout:'<span class="chip">Öffnungswinkel <b>'+deg.toFixed(1).replace(".",",")+'°</b></span><span class="chip">Breite am Bildrand <b>'+wcm.toFixed(1).replace(".",",")+' cm</b></span>'};
}

function modell(){
  var o=[], L=[120,220], xs=330, b=60, X=800;
  var yT=L[1]-b/2*(X-L[0])/(xs-L[0]), yB=L[1]+b/2*(X-L[0])/(xs-L[0]);
  o.push('<g clip-path="url(#sc)">');
  o.push(G.rect(xs-5,0,10,L[1]-b/2,"#9FB2CF")+G.rect(xs-5,L[1]+b/2,10,440-L[1]-b/2,"#9FB2CF"));
  if(S.ansicht==="wirklich"){
    o.push(G.poly([[L[0],L[1]],[xs,L[1]-b/2],[X,yT],[X,yB],[xs,L[1]+b/2]],"#FFC53D",0.4,"fade",0));
    o.push(G.txt(560,110,"Lichtbündel: hat eine Breite","mid"));
  }else{
    o.push(G.arrow(L[0],L[1],X,yT,"#FFC53D",3,0)+G.arrow(L[0],L[1],X,L[1],"#FFC53D",3,0.15)+G.arrow(L[0],L[1],X,yB,"#FFC53D",3,0.3));
    o.push(G.txt(560,110,"Lichtstrahlen: gedachte Linien","mid"));
  }
  o.push(G.bulb(L[0],L[1],true,12));
  o.push('</g>');
  return {svg:o.join(""), readout:'<span class="chip">'+(S.ansicht==="wirklich"?"So ist es in Wirklichkeit.":"So zeichnen wir es im Modell.")+'</span>'};
}

function nebel(){
  var o=[], y0=180, y1=200, X=760, E=[420,380], fog=S.luft==="nebel", i, sx, sy, seed=7;
  function rnd(){ seed=(seed*9301+49297)%233280; return seed/233280; }
  o.push('<g clip-path="url(#sc)">');
  if(fog){
    for(i=0;i<260;i++){ sx=20+rnd()*800; sy=10+rnd()*420;
      var inB=sx>110&&sx<X&&sy>y0-2&&sy<y1+2;
      o.push(G.circ(sx,sy,inB?2.4:1.6,inB?"#FFE7A0":"#9AAAC0",' opacity="'+(inB?0.95:0.3)+'"')); }
    o.push(G.rect(110,y0,X-110,y1-y0,"#FFC53D",0.5,' class="fade" style="--d:.2s"'));
    [240,360,480,600,700].forEach(function(px,k){ o.push(G.arrow(px,y1,E[0]+(px-E[0])*0.12,E[1]-22,"#FFC53D",1.6,0.9+0.08*k,0.8)); });
  }else{
    o.push('<rect x="110" y="'+y0+'" width="'+(X-110)+'" height="'+(y1-y0)+'" fill="none" stroke="#9AAAC0" stroke-dasharray="3 9" stroke-opacity=".6"/>');
  }
  o.push(G.rect(X,0,26,440,"#FFE29A",0.85));
  o.push(G.circ(X+13,190,30,"url(#gGlow)")+G.circ(X+13,190,9,"#FFFFFF"));
  o.push('<rect x="36" y="166" width="76" height="48" rx="6" fill="#3B4A63"/>');
  o.push(G.eye(E[0],E[1],1,1));
  o.push('</g>');
  o.push(G.txt(74,150,"Ray-Box","mid dim"));
  o.push(G.txt(E[0]+40,E[1]+8,"Du schaust von der Seite",""));
  if(!fog) o.push(G.txt(430,160,"Hier läuft Licht. Du siehst es nicht.","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Lichtweg von der Seite sichtbar <b>'+(fog?"ja":"nein")+'</b></span>'+(fog?'<span class="chip">Tröpfchen streuen Licht zu dir</span>':'<span class="chip">Nur der Fleck an der Wand streut Licht zu dir</span>')};
}

function spiegel(){
  var o=[], C=[700,110], E=[230,392], Mp=[230,64], H=[300,200,540,240], on=S.spiegel==="1";
  o.push('<g clip-path="url(#sc)">');
  o.push(G.rect(0,40,840,140,"#141C28")+G.rect(170,180,120,260,"#141C28"));
  for(var x=20;x<840;x+=70) o.push(G.rect(x,108,36,4,"#4D5E77"));
  o.push(G.rect(H[0],H[1],H[2],H[3],"#27344A")+G.rect(0,180,170,260,"#27344A"));
  o.push('<rect x="'+(C[0]-34)+'" y="'+(C[1]-17)+'" width="68" height="34" rx="8" fill="#9FB2CF"/>');
  if(on){
    var ax=C[0]-Mp[0], ay=C[1]-Mp[1], la=Math.hypot(ax,ay), bx=E[0]-Mp[0], by=E[1]-Mp[1], lb=Math.hypot(bx,by);
    var nx=ax/la+bx/lb, ny=ay/la+by/lb, ln=Math.hypot(nx,ny); nx/=ln; ny/=ln;
    o.push(G.arrow(C[0]-34,C[1]-4,Mp[0]+6,Mp[1]+2,"#FFC53D",3,0.1));
    o.push(G.arrow(Mp[0],Mp[1]+6,E[0],E[1]-22,"#FFC53D",3,0.9));
    o.push('<line x1="'+(Mp[0]-ny*36)+'" y1="'+(Mp[1]+nx*36)+'" x2="'+(Mp[0]+ny*36)+'" y2="'+(Mp[1]-nx*36)+'" stroke="#E7EDF6" stroke-width="6" stroke-linecap="round"/>');
  }else{
    var t=hitRect(C,E,H), hx=C[0]+(E[0]-C[0])*t, hy=C[1]+(E[1]-C[1])*t;
    o.push(G.ray(C[0],C[1],hx,hy,"#FFC53D",3,0.1));
    o.push(G.dash(hx,hy,E[0],E[1]-22,"#9AAAC0",2,0.8,0.6));
    o.push('<path class="fade" style="--d:.9s" d="M'+(hx-9)+' '+(hy-9)+' l18 18 M'+(hx+9)+' '+(hy-9)+' l-18 18" stroke="#FF7A59" stroke-width="4" stroke-linecap="round"/>');
  }
  o.push(G.circ(E[0],E[1],18,"#9FB2CF")+G.circ(E[0]-7,E[1]-10,4,"#0A1120")+G.circ(E[0]+7,E[1]-10,4,"#0A1120"));
  o.push('</g>');
  o.push(G.txt(570,330,"Haus","mid dim"));
  o.push(G.txt(C[0],C[1]+44,"Auto","mid dim"));
  o.push(G.txt(E[0]+30,E[1]+8,"Du in der Ausfahrt",""));
  if(on) o.push(G.txt(Mp[0]+44,Mp[1]-10,"Verkehrsspiegel",""));
  o.push(G.txt(28,24,"Draufsicht","dim"));
  return {svg:o.join(""), readout:'<span class="chip">Auto sichtbar <b>'+(on?"ja, über den Spiegel":"nein")+'</b></span>'};
}

window.LAB={state:S,
 draw:function(cfg){ return {ecke:ecke,blende:blende,buendel:buendel,modell:modell,nebel:nebel,spiegel:spiegel}[cfg.mode](cfg); },
 QZ:[
  {q:"Hinter einer Hausecke hörst du ein Auto, siehst es aber nicht. Warum?",
   o:["Licht breitet sich geradlinig aus, Schall kommt um die Ecke","Das Auto sendet kein Licht aus","Licht ist langsamer als Schall"],a:0,
   w:"Das Licht vom Auto läuft geradeaus und trifft auf die Hauswand. Um die Ecke biegt es nicht."},
  {q:"Zwei Blenden stehen zwischen Lampe und Schirm. Wann ist ein Lichtpunkt zu sehen?",
   o:["Immer","Nur wenn beide Löcher mit der Lampe auf einer Geraden liegen","Nur wenn die Löcher groß sind"],a:1,
   w:"Das Licht kommt nur geradlinig durch beide Löcher. Genau das zeigt der Versuch."},
  {q:"Was zeigt ein Lichtstrahl im Modell?",
   o:["Wie hell das Licht ist","Welchen Weg und welche Richtung das Licht nimmt","Welche Farbe das Licht hat"],a:1,
   w:"Der Lichtstrahl ist eine gedachte Linie. Er zeigt nur Weg und Richtung."},
  {q:"Warum sieht man den Lichtkegel eines Scheinwerfers im Nebel?",
   o:["Nebeltröpfchen streuen Licht zu deinem Auge","Nebel leuchtet selbst","Im Nebel wird das Licht langsamer"],a:0,
   w:"In klarer Luft läuft das Licht an dir vorbei. Die Tröpfchen werfen einen Teil davon zu dir."}
 ],
 scenes:[
  {kicker:"Optik · Leitfrage 3", title:"Warum können wir nicht um die Ecke sehen?",
   html:"<p>Der Ball liegt hinter der Mauer. Geh mit dem Regler nach links und nach rechts.</p>",
   ask:"Ab wo siehst du den Ball? Was fällt dir am Weg des Lichts auf?",
   note:"Passt zur Beobachte-Folie mit Ball und Mauer. Vermutungen sammeln.",
   controls:{sl:[{k:"x",label:"Wo stehst du?",min:110,max:790,step:5,fmt:function(v){return ((v-110)/100).toFixed(1).replace(".",",")+" m"}}]},
   cfg:{mode:"ecke"}, alt:"Draufsicht: Ball hinter einer Mauer"},

  {kicker:"Versuch", title:"Ray-Box und Blenden",
   html:"<p>Das ist dein Versuch vom Versuchsblatt. Verschiebe die Blende und beobachte den Lichtpunkt auf dem Schirm.</p><p>Schalte dann eine zweite Blende dazu.</p>",
   ask:"Wann erscheint der Lichtpunkt? Was muss für zwei Blenden gelten?",
   note:"Die zweite Blende ist die Zusatzaufgabe für schnelle Gruppen.",
   controls:{btn:[{k:"zwei",label:"Blenden:",opts:[["0","eine"],["1","zwei"]]}],
     sl:[{k:"h1",label:"Blende 1 verschieben",min:110,max:330,step:2,fmt:function(v){return ((v-220)/10).toFixed(1).replace(".",",")+" cm"}},
         {k:"h2",label:"Blende 2 verschieben",min:110,max:330,step:2,fmt:function(v){return ((v-220)/10).toFixed(1).replace(".",",")+" cm"}}],
     reset:{h1:220,h2:220}},
   cfg:{mode:"blende"}, alt:"Ray-Box, Blende mit Loch und Schirm"},

  {kicker:"Schritt 1", title:"Wie breitet sich Licht aus?",
   html:"<p>Eine Lampe sendet Licht in alle Richtungen. Es läuft auseinander (<span class=\"term\">divergent</span>). Ein Spalt lässt nur ein schmales Lichtbündel durch.</p>",
   ask:"Wie bekommst du ein fast paralleles Lichtbündel?",
   note:"Je schmaler der Spalt und je weiter die Lampe weg, desto paralleler das Bündel. Sonnenlicht ist fast parallel, weil die Sonne so weit weg ist.",
   controls:{sl:[{k:"a",label:"Lampe bis Spalt",min:60,max:560,step:10,fmt:function(v){return (v/10).toFixed(0)+" cm"}},
                 {k:"b",label:"Spaltbreite",min:2,max:60,step:1,fmt:function(v){return v+" mm"}}],reset:{a:200,b:20}},
   cfg:{mode:"buendel"}, alt:"Lampe und Spalt mit Lichtbündel"},

  {kicker:"Schritt 2", title:"Das Lichtstrahlenmodell",
   html:"<p>Ein Lichtbündel hat immer eine Breite. Zum Zeichnen denken wir uns unendlich dünne <span class=\"term\">Lichtstrahlen</span>. Sie zeigen nur Weg und Richtung.</p><dl class=\"terms\"><div><dt>stimmt</dt><dd>Licht läuft geradlinig, die Richtung ist richtig.</dd></div><div><dt>vereinfacht</dt><dd>Ein Strahl hat keine Breite.</dd></div><div><dt>fehlt</dt><dd>Helligkeit und Farbe zeigt das Modell nicht.</dd></div></dl>",
   controls:{btn:[{k:"ansicht",label:"Zeige:",opts:[["wirklich","Wirklichkeit"],["modell","Modell"]]}]},
   note:"Modelle bewerten: Was stimmt, was ist vereinfacht, was fehlt?",
   cfg:{mode:"modell"}, alt:"Lichtbündel und Lichtstrahlen im Vergleich"},

  {kicker:"Alltag", title:"Warum sieht man Lichtwege im Nebel?",
   html:"<p>In klarer Luft siehst du einen Lichtweg von der Seite nicht. Im Nebel, Staub oder Rauch schon.</p>",
   ask:"Was hat das mit Streuung aus Leitfrage 2 zu tun?",
   note:"Brücke zu Leitfrage 2: Die Tröpfchen streuen Licht zur Seite, also auch ins Auge.",
   controls:{btn:[{k:"luft",label:"Luft:",opts:[["klar","klar"],["nebel","Nebel"]]}]},
   cfg:{mode:"nebel"}, alt:"Lichtbündel in klarer Luft und im Nebel"},

  {kicker:"Alltag", title:"Um die Ecke sehen: nur mit Hilfe",
   html:"<p>An einer Ausfahrt verdeckt das Haus die Straße. Ein Verkehrsspiegel lenkt das Licht um.</p><p class=\"small\">Wie Spiegel das Licht lenken, lernst du später.</p>",
   ask:"Warum hilft der Spiegel, obwohl das Licht trotzdem nur geradeaus läuft?",
   controls:{btn:[{k:"spiegel",label:"Spiegel:",opts:[["0","ohne"],["1","mit"]]}]},
   cfg:{mode:"spiegel"}, alt:"Draufsicht einer Ausfahrt mit Verkehrsspiegel"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>",
   note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Das Licht einer Lichtquelle breitet sich in verschiedene Richtungen aus. Es läuft auseinander (divergent). Mithilfe von Blenden oder Spalten kann man daraus parallele Lichtbündel erzeugen.</li><li>Ein Lichtstrahl ist ein Modell: ein gedachter, unendlich dünner Teil eines Lichtbündels. Modelle vereinfachen die Wirklichkeit, damit wir sie zeichnen und erklären können.</li><li>Wir können nicht um die Ecke sehen, weil sich Licht geradlinig ausbreitet.</li></ul>",
   askLabel:"Probier's aus", ask:"Schau durch einen geraden Strohhalm auf eine Schreibtischlampe, nie in die Sonne. Biege den Halm dann. Was ändert sich?",
   cfg:{mode:"modell"}, alt:"Lichtstrahlenmodell"}
 ]};
})();
