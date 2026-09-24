/* Lochkameralabor: Warum steht das Bild auf dem Kopf? (1 px = 1 mm; Kerze G = 120 mm)
   Bildgröße B = G·b/g, Unschärfe (Durchmesser eines Lichtflecks) u = d·(g+b)/g, Helligkeit ~ d²/b² */
(function(){
"use strict";
var S={teil:"beide", g:260, b:180, d:3, loecher:"1", tag:"normal"};
var AX=220, LX=330, GK=120;

function kerze(x,yFuss,h,flip,extra){
  /* Kerze mit Flamme, Höhe h (Flamme gehört dazu), flip = auf dem Kopf */
  var s=h/GK, t='translate('+G.f1(x)+' '+G.f1(yFuss)+') scale('+G.f1(s*100)/100+' '+(flip?-1:1)*G.f1(s*100)/100+')';
  return '<g transform="'+t+'"'+(extra||'')+'><rect x="-11" y="-78" width="22" height="78" rx="2" fill="#F5E6C8"/>'+
    '<path d="M0 -78 q-13 -20 0 -42 q13 22 0 42z" fill="#FFB627"/><circle cx="0" cy="-95" r="26" fill="url(#gGlow)"/></g>';
}

function aufbau(cfg){
  var o=[], g=cfg.live?+S.g:260, b=cfg.live?+S.b:180, d=cfg.live?+S.d:3;
  var KX=LX-g, SX=LX+b, top=AX-GK/2, fuss=AX+GK/2, B=GK*b/g, u=d*(g+b)/g;
  var teil=cfg.teil?S.teil:"beide";
  o.push('<defs><filter id="unscharf" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="'+G.f1(Math.max(0.01,u/2.4))+'"/></filter></defs>');
  o.push('<g clip-path="url(#sc)">');
  o.push(G.dash(20,AX,820,AX,"#4D5E77",1,0,0.6));
  if(teil!=="fuss") o.push(G.ray(KX,top,SX,AX+(AX-top)*b/g,"#FF8A3D",2.4,0.1));
  if(teil!=="spitze") o.push(G.ray(KX,fuss,SX,AX-(fuss-AX)*b/g,"#4CC9F0",2.4,0.3));
  o.push(kerze(KX,fuss,GK,false));
  /* Dose mit Loch */
  o.push(G.rect(LX-6,20,12,AX-20-d/2,"#9FB2CF")+G.rect(LX-6,AX+d/2,12,420-AX-d/2,"#9FB2CF"));
  /* Schirm */
  o.push(G.rect(SX,AX-150,10,300,"#FFE29A",0.9));
  var hell=Math.min(1,0.25+0.75*(d*d/(b*b))/(9/(180*180)));
  o.push('<g filter="url(#unscharf)" opacity="'+G.f1(Math.min(1,hell)*100)/100+'" class="fade" style="--d:1s">'+kerze(SX-18,AX-B/2,B,true)+'</g>');
  o.push('</g>');
  o.push(G.txt(KX,fuss+30,"Kerze","mid dim")+G.txt(LX,16+14,"Loch","mid dim")+G.txt(SX+5,AX+178>430?430:AX+178,"Schirm","mid dim"));
  return {svg:o.join(""), readout:cfg.live?'<span class="chip">Bildgröße <b>'+(B/10).toFixed(1).replace(".",",")+' cm</b></span><span class="chip">Unschärfe <b>'+u.toFixed(1).replace(".",",")+' mm</b></span><span class="chip">Helligkeit <b>'+(hell>0.8?"hell":(hell>0.45?"mittel":"dunkel"))+'</b></span>':''};
}

function loecher(){
  var o=[], g=260, b=180, KX=LX-g, SX=LX+b, top=AX-GK/2, fuss=AX+GK/2, B=GK*b/g, n=S.loecher, off=[0];
  if(n==="2") off=[-45,45]; if(n==="viele") off=[-24,-16,-8,0,8,16,24];
  o.push('<g clip-path="url(#sc)">');
  o.push(kerze(KX,fuss,GK,false));
  var y=20, parts="";
  off.slice().sort(function(a,b){return a-b}).forEach(function(k){ parts+=G.rect(LX-6,y,12,AX+k-1.5-y,"#9FB2CF"); y=AX+k+1.5; });
  parts+=G.rect(LX-6,y,12,420-y,"#9FB2CF"); o.push(parts);
  o.push(G.rect(SX,AX-170,10,340,"#FFE29A",0.9));
  off.forEach(function(k,i){
    var c=AX+k;                               /* Loch bei y=c: Bildmitte verschiebt sich um k*(g+b)/g */
    var mid=AX+(c-AX)*(g+b)/g;
    o.push(G.ray(KX,top,SX,c+(c-top)*b/g,"#FF8A3D",1.6,0.05*i,n==="viele"?0.35:0.9));
    o.push('<g opacity="'+(n==="viele"?0.35:0.95)+'" class="fade" style="--d:1s">'+kerze(SX-18,mid-B/2,B,true)+'</g>');
  });
  o.push('</g>');
  o.push(G.txt(KX,fuss+30,"Kerze","mid dim")+G.txt(LX,30,n==="1"?"ein Loch":(n==="2"?"zwei Löcher":"viele Löcher nebeneinander"),"mid dim"));
  var t=n==="1"?"ein scharfes Bild":(n==="2"?"zwei Bilder nebeneinander":"viele Bilder überlagern sich: hell, aber unscharf");
  return {svg:o.join(""), readout:'<span class="chip"><b>'+t+'</b></span>'};
}

function baum(){
  var o=[], fin=S.tag==="finster", i, x;
  o.push(G.rect(0,0,840,440,"#FFC53D",0.03));
  o.push(G.circ(730,70,60,"url(#gGlow)"));
  if(fin) o.push('<path d="M730 44 a26 26 0 1 0 0 52 a20 20 0 1 1 0 -52z" fill="#FFD34D"/>');
  else o.push(G.circ(730,70,26,"url(#gSun)"));
  o.push(G.txt(730,122,fin?"Sonne während der Finsternis":"Sonne","mid dim"));
  o.push('<rect x="300" y="170" width="26" height="200" rx="4" fill="#6B4A2B"/><ellipse cx="313" cy="130" rx="190" ry="90" fill="#2F5A2B"/>');
  [[210,110],[290,150],[360,100],[420,160],[250,170]].forEach(function(p){ o.push(G.circ(p[0],p[1],4,"#FFF6D8")); });
  o.push(G.rect(40,370,760,6,"#6B4A2B"));
  [[150,392],[230,398],[400,394],[480,400],[560,392]].forEach(function(p,k){
    o.push(G.circ(p[0],p[1],20,"url(#gGlow)"));
    if(fin) o.push('<path transform="rotate(180 '+p[0]+' '+p[1]+')" d="M'+p[0]+' '+(p[1]-11)+' a11 11 0 1 0 0 22 a8.5 8.5 0 1 1 0 -22z" fill="#FFD34D"/>');
    else o.push('<ellipse cx="'+p[0]+'" cy="'+p[1]+'" rx="11" ry="6" fill="#FFD34D"/>');
  });
  o.push(G.txt(313,32,"Lücken im Blätterdach","mid dim"));
  o.push(G.txt(360,432,"Lichtflecken auf dem Boden","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">'+(fin?"Die Flecken sind Sicheln, umgekehrt zur Sonnensichel":"Die Flecken sind rund, obwohl die Lücken eckig sind")+'</span>'};
}

window.LAB={state:S,
 draw:function(cfg){ return {aufbau:aufbau,loecher:loecher,baum:baum}[cfg.mode](cfg); },
 QZ:[
  {q:"Warum steht das Bild in der Lochkamera auf dem Kopf?",
   o:["Das Transparentpapier dreht es um","Licht breitet sich geradlinig aus, die Strahlen kreuzen sich im Loch","Das Loch wirkt wie ein Spiegel"],a:1,
   w:"Licht von der Flammenspitze läuft geradlinig durch das Loch und landet unten auf dem Schirm."},
  {q:"Du ziehst das Transparentpapier weiter vom Loch weg. Das Bild wird …",
   o:["größer und dunkler","kleiner und heller","größer und heller"],a:0,
   w:"Das Licht verteilt sich auf eine größere Fläche. Deshalb wird das Bild größer, aber dunkler."},
  {q:"Du machst das Loch größer. Was passiert?",
   o:["Das Bild wird heller und unschärfer","Das Bild wird dunkler und schärfer","Nichts ändert sich"],a:0,
   w:"Ein großes Loch wirkt wie viele kleine Löcher nebeneinander. Die vielen Bilder überlagern sich."},
  {q:"Warum sind die Lichtflecken unter einem Baum meist rund, obwohl die Lücken im Laub eckig sind?",
   o:["Es sind Bilder der runden Sonne","Die Blätter sind rund","Licht breitet sich kreisförmig aus"],a:0,
   w:"Jede kleine Lücke wirkt wie eine Lochkamera und erzeugt ein Bild der Sonne."}
 ],
 scenes:[
  {kicker:"Optik · Lochkamera", title:"Warum steht das Bild auf dem Kopf?",
   html:"<p>Eine Dose mit einem kleinen Loch, dahinter ein Schirm aus Transparentpapier. Auf dem Schirm erscheint ein Bild der Kerze.</p>",
   ask:"Was fällt dir am Bild auf? Hast du eine Erklärung?",
   note:"Einstieg. Erst Vermutungen, dann Schritt 1.",
   cfg:{mode:"aufbau"}, alt:"Kerze, Lochblende und Schirm mit umgekehrtem Bild"},

  {kicker:"Schritt 1", title:"Der Weg des Lichts",
   html:"<p>Das Licht von der <span class=\"term\">Spitze</span> der Flamme verläuft durch die Lochblende und trifft <span class=\"term\">unten</span> auf den Schirm. Das Licht vom Fuß der Kerze trifft oben auf.</p>",
   ask:"Schalte zwischen Spitze, Fuß und beiden um. Wo kreuzen sich die Lichtwege?",
   note:"Hier greift die geradlinige Ausbreitung aus Leitfrage 3.",
   controls:{btn:[{k:"teil",label:"Zeige Licht von:",opts:[["spitze","der Spitze"],["fuss","dem Fuß"],["beide","beiden"]]}]},
   cfg:{mode:"aufbau",teil:true}, alt:"Lichtwege von Flammenspitze und Kerzenfuß durch das Loch"},

  {kicker:"Experiment", title:"Größe, Schärfe, Helligkeit",
   html:"<p>Verändere die Abstände und die Größe des Lochs. Beobachte das Bild auf dem Schirm.</p>",
   reveal:"<ul class=\"list\"><li>Je <b>weiter</b> der Schirm vom Loch weg ist, desto <b>größer</b> und <b>dunkler</b> das Bild.</li><li>Je <b>näher</b> die Kerze am Loch ist, desto <b>größer</b> das Bild.</li><li>Je <b>kleiner</b> das Loch, desto <b>schärfer</b>, aber <b>dunkler</b> das Bild.</li></ul>",
   revealBtn:"Ergebnisse zeigen",
   note:"Passt zum Versuchsblatt W09. Bildgröße nach Strahlensatz: B = G · b : g. Die Unschärfe ist die Größe eines Lichtflecks, den ein einzelner Punkt der Kerze erzeugt.",
   controls:{sl:[{k:"g",label:"Kerze bis Loch",min:120,max:300,step:5,fmt:function(v){return (v/10).toFixed(1).replace(".",",")+" cm"}},
                 {k:"b",label:"Loch bis Schirm",min:60,max:260,step:5,fmt:function(v){return (v/10).toFixed(1).replace(".",",")+" cm"}},
                 {k:"d",label:"Lochgröße",min:0.5,max:14,step:0.5,fmt:function(v){return v.toFixed(1).replace(".",",")+" mm"}}],reset:{g:260,b:180,d:3}},
   cfg:{mode:"aufbau",live:true}, alt:"Lochkamera mit einstellbaren Abständen und Lochgröße"},

  {kicker:"Schritt 2", title:"Warum macht ein großes Loch unscharf?",
   html:"<p>Ein großes Loch kann man sich als viele kleine Löcher nebeneinander denken. Jedes kleine Loch erzeugt sein eigenes Bild.</p>",
   ask:"Was passiert mit den Bildern, wenn die Löcher dicht nebeneinander liegen?",
   note:"Gleicher Gedanke wie beim Halbschatten: Viele Lichtpunkte, viele leicht verschobene Bilder.",
   controls:{btn:[{k:"loecher",label:"Löcher:",opts:[["1","eins"],["2","zwei"],["viele","viele"]]}]},
   cfg:{mode:"loecher"}, alt:"Lochkamera mit einem, zwei oder vielen Löchern"},

  {kicker:"Alltag", title:"Sonnenbilder unter dem Baum",
   html:"<p>Unter einem Baum liegen runde Lichtflecken, obwohl die Lücken im Laub eckig sind. Bei einer Sonnenfinsternis werden daraus kleine Sicheln.</p>",
   ask:"Warum sind die Sicheln auf dem Boden anders herum als die Sonne am Himmel?",
   note:"Passt zur Folie „Zum Schluss: Sicheln auf dem Boden“. Jede Lücke ist eine Lochkamera, das Bild steht auf dem Kopf.",
   controls:{btn:[{k:"tag",label:"Tag:",opts:[["normal","normaler Tag"],["finster","Sonnenfinsternis"]]}]},
   cfg:{mode:"baum"}, alt:"Baum mit Lichtflecken auf dem Boden"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>",
   note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Das Licht von der Spitze der Flamme verläuft durch die Lochblende und trifft unten auf den Schirm. Deshalb steht das Bild umgekehrt.</li><li>Je weiter das Transparentpapier vom Loch entfernt ist, desto größer wird das Bild.</li><li>Ein kleines Loch macht das Bild schärfer, aber dunkler.</li></ul>",
   askLabel:"Probier's aus", ask:"Stich mit einer Nadel ein Loch in ein Stück Alufolie und halte es in die Sonne. Fang das Licht auf einem weißen Blatt auf. Schau dabei nie selbst in die Sonne.",
   cfg:{mode:"aufbau"}, alt:"Lochkamera"}
 ]};
})();
