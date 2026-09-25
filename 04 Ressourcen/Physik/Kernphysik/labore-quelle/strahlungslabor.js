/* Strahlungslabor · Kernphysik Klasse 10 · Leitfrage 2: Warum zerfallen manche Atomkerne von selbst?
   Simulierte Zählraten (Nullrate um 24 Impulse pro Minute, Poisson-verteilt). Keine echten Präparate nötig. */
(function(){
"use strict";
var S={mess:1, praep:"0", d:6, art:"a", strahl:"a", absorber:"kein", ball:"1", t:0, ef:"a", spannung:"1", dicke:0, lh:"1"};
var PROT="#FF7A59", NEUT="#9FB2CF", ELEK="#4CC9F0", ALPHA="#FF8A3D", GAMMA="#B28DFF";

function poisson(lambda,seed){ var L=Math.exp(-lambda),k=0,p=1,s=seed; do{ s=(s*9301+49297)%233280; p*=s/233280; k++; }while(p>L&&k<1000); return k-1; }
function nk(x,y,sym,A,Z,size,col){
  size=size||34; col=col||"#FFFFFF"; var k=size*0.5;
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
function geraet(x,y,wert){
  return '<rect x="'+x+'" y="'+y+'" width="220" height="130" rx="12" fill="#26324A"/><rect x="'+(x+16)+'" y="'+(y+16)+'" width="188" height="62" rx="5" fill="#05080F"/>'+
    '<text x="'+(x+110)+'" y="'+(y+60)+'" font-family="IBM Plex Mono,monospace" font-size="36" fill="#6FE39A" text-anchor="middle">'+("000"+wert).slice(-4)+'</text>'+
    G.circ(x+40,y+104,9,"#9FB2CF")+G.circ(x+70,y+104,9,"#9FB2CF")+G.txt(x+150,y+110,"Imp/min","mid dim");
}
function rohr(x,y){ return '<rect x="'+x+'" y="'+(y-11)+'" width="120" height="22" rx="11" fill="#9FB2CF"/><rect x="'+(x+110)+'" y="'+(y-11)+'" width="10" height="22" rx="3" fill="#F5E6C8"/>'; }

function nullrate(){
  var o=[], m=+S.mess, werte=[], i, sum=0;
  for(i=1;i<=m;i++){ var v=poisson(24,i*977+13); werte.push(v); sum+=v; }
  o.push(geraet(60,90,werte[m-1])+'<line x1="280" y1="155" x2="300" y2="155" stroke="#9FB2CF" stroke-width="4"/>'+rohr(300,155));
  [[540,70],[700,120],[610,200],[780,60],[660,250],[760,220]].forEach(function(q,k){ if((k+m)%2===0) o.push(G.circ(q[0],q[1],14,"url(#gGlow)",' opacity=".5"')+G.circ(q[0],q[1],3,GAMMA)); });
  /* Balken der bisherigen Messungen */
  var x0=90, y0=420;
  werte.forEach(function(v,k){ o.push(G.rect(x0+k*62,y0-v*4,40,v*4,k===m-1?"#6FE39A":"#4D5E77")); o.push('<text x="'+(x0+k*62+20)+'" y="'+(y0-v*4-6)+'" font-family="IBM Plex Mono,monospace" font-size="13" fill="#E7EDF6" text-anchor="middle">'+v+'</text>'); });
  o.push(G.txt(500,300,"Strahlung aus Boden, Luft,","")+G.txt(500,324,"Weltall und dem eigenen Körper",""));
  return {svg:o.join(""), readout:'<span class="chip">Messung '+m+': <b>'+werte[m-1]+' Impulse</b> in 1 Minute</span><span class="chip">Mittelwert <b>'+(sum/m).toFixed(1).replace(".",",")+'</b></span>'};
}

function abstand(){
  var o=[], mit=S.praep==="1", d=+S.d, rate=24+(mit?Math.round(24000/(d*d)):0), x=400+d*20, i;
  o.push(geraet(40,90,rate)+'<line x1="260" y1="155" x2="280" y2="155" stroke="#9FB2CF" stroke-width="4"/>'+rohr(280,155));
  if(mit){
    o.push('<path d="M'+(x-4)+' 184 h56 l-8 -30 h-40z" fill="#9FB2CF"/>'+G.circ(x+24,152,20,"url(#gGlow)"));
    for(i=0;i<7;i++){ var a=Math.PI+(i-3)*0.1, L=x+10-402; o.push(G.ray(x+14,152,x+14+L*Math.cos(a),152+L*Math.sin(a),GAMMA,1.4,0.03*i,0.7)); }
    o.push(G.txt(x+24,210,"Präparat","mid dim"));
    o.push(G.dash(400,250,x,250,"#9AAAC0",1.5,0,0.8)+G.txt((400+x)/2,274,d+" cm","mid"));
  }
  return {svg:o.join(""), readout:'<span class="chip">Zählrate <b>'+rate+' Impulse pro Minute</b></span>'+(mit?'<span class="chip">doppelter Abstand: etwa ein Viertel</span>':'<span class="chip">nur Nullrate</span>')};
}

var ZER={a:{von:["Ra",226,88,40,48],zu:["Rn",222,86,38,46],teil:"He-Kern",A:"−4",Z:"−2",name:"α-Zerfall"},
         b:{von:["C",14,6,6,8],zu:["N",14,7,7,7],teil:"Elektron",A:"±0",Z:"+1",name:"β⁻-Zerfall"},
         g:{von:["Ba","137m",56,14,18],zu:["Ba",137,56,14,18],teil:"Energie",A:"±0",Z:"±0",name:"γ-Strahlung"}};
function zerfall(){
  var o=[], d=ZER[S.art], klein=d.von[2]>20;
  o.push(kern(180,200,d.von[3],d.von[4],7,5)+G.txt(180,300,klein?"vereinfacht gezeichnet":"","mid dim"));
  if(S.art==="g") o.push(G.circ(180,200,62,"none",' stroke="'+GAMMA+'" stroke-dasharray="4 5" stroke-width="2"'));
  o.push(G.arrow(270,200,370,200,"#9AAAC0",3,0.2));
  o.push('<g class="fade" style="--d:.6s">'+kern(460,200,d.zu[3],d.zu[4],7,6)+'</g>');
  if(S.art==="a") o.push('<g class="fade" style="--d:1s">'+kern(640,120,2,2,9,3)+'</g>'+G.arrow(520,170,610,130,ALPHA,3,0.9));
  if(S.art==="b") o.push(G.arrow(520,190,640,140,ELEK,3,0.9)+'<g class="fade" style="--d:1s">'+G.circ(654,132,9,ELEK)+'</g>');
  if(S.art==="g"){ var p="M520 200"; for(var i=0;i<10;i++) p+=" q7 "+(i%2?12:-12)+" 14 0"; o.push('<path class="fade" style="--d:.9s" d="'+p+'" fill="none" stroke="'+GAMMA+'" stroke-width="3"/>'); }
  o.push(nk(150,380,d.von[0],d.von[1],d.von[2],34)+G.txt(230,372,"→","mid")+nk(300,380,d.zu[0],d.zu[1],d.zu[2],34)+G.txt(380,372,"+","mid"));
  o.push(S.art==="a"?nk(440,380,"He",4,2,34):(S.art==="b"?nk(440,380,"e",0,"−1",34):'<text x="440" y="380" font-family="Georgia,serif" font-size="34" fill="#B28DFF">γ</text>'));
  return {svg:o.join(""), readout:'<span class="chip"><b>'+d.name+'</b></span><span class="chip">Massenzahl A <b>'+d.A+'</b></span><span class="chip">Kernladungszahl Z <b>'+d.Z+'</b></span>'};
}

var UEB=[["U",238,92,"α",[["Th",234,90],["Pa",238,91],["Th",236,90]],0],["Po",210,84,"α",[["Pb",206,82],["Bi",210,83],["Hg",206,80]],0],
         ["Sr",90,38,"β⁻",[["Rb",90,37],["Y",90,39],["Zr",91,40]],1],["K",40,19,"β⁻",[["Ca",40,20],["Ar",40,18],["Ca",41,20]],0],
         ["C",14,6,"β⁻",[["B",14,5],["N",15,7],["N",14,7]],2],["Ra",226,88,"α",[["Rn",222,86],["Ra",222,86],["Fr",226,87]],0]];
var UA={};
function nkHTML(s,A,Z){ return '<span style="white-space:nowrap"><span style="display:inline-flex;flex-direction:column;font-size:.62em;line-height:1.05;text-align:right;vertical-align:-.42em;margin-right:1px"><span>'+A+'</span><span>'+Z+'</span></span><span style="font-family:Georgia,serif;font-size:1.15em">'+s+'</span></span>'; }
function widget(){
  var done=0,right=0;
  var h='<div class="sortgrid">'+UEB.map(function(u,i){
    var s=UA[i]; if(s!=null){done++; if(s===u[5]) right++;}
    return '<div class="q"><p class="qt">'+nkHTML(u[0],u[1],u[2])+' → ? &nbsp;('+u[3]+'-Zerfall)</p><div class="opts">'+u[4].map(function(o,j){
      var c="opt"; if(s!=null){ if(j===u[5]) c+=" right"; else if(j===s) c+=" wrong"; }
      return '<button type="button" class="'+c+'" data-w="'+i+'" data-v="'+j+'"'+(s!=null?" disabled":"")+'>'+nkHTML(o[0],o[1],o[2])+'</button>'; }).join("")+'</div>'+
      (s!=null?'<p class="why">'+(u[3]==="α"?"α: A um 4 kleiner, Z um 2 kleiner.":"β⁻: A bleibt, Z um 1 größer.")+'</p>':'')+'</div>';
  }).join("")+'</div>';
  if(done===UEB.length) h+='<p class="score">Ergebnis: '+right+' von '+UEB.length+' richtig</p>';
  return h;
}

var REICH={a:{kein:1,papier:0,alu:0,blei:0},b:{kein:1,papier:0.95,alu:0,blei:0},g:{kein:1,papier:1,alu:0.97,blei:0.2}};
var AX={papier:[320,6,"#F5E6C8"],alu:[440,16,"#C6D1E1"],blei:[560,40,"#4D5E77"]};
function durch(){
  var o=[], t=S.strahl, ab=S.absorber, anteil=REICH[t][ab], rate=24+Math.round(1800*anteil), col=t==="a"?ALPHA:(t==="b"?ELEK:GAMMA);
  o.push('<path d="M40 250 h80 l-10 -40 h-60z" fill="#9FB2CF"/>'+G.circ(80,212,24,"url(#gGlow)"));
  ["papier","alu","blei"].forEach(function(k){ var a=AX[k]; o.push(G.rect(a[0],90,a[1],240,a[2],ab===k?1:0.18)); });
  var stop=ab==="kein"?760:AX[ab][0], weiter=anteil>0;
  if(t==="g"){ var p="M120 210",x=120; while(x<(weiter?760:stop)){ p+=" q8 "+(((x/16)|0)%2?10:-10)+" 16 0"; x+=16; } o.push('<path d="'+p+'" fill="none" stroke="'+col+'" stroke-width="3" stroke-opacity="'+(ab==="blei"?0.5:1)+'"/>'); }
  else o.push(G.arrow(120,210,weiter?760:stop,210,col,4,0));
  o.push(rohr(760,210).replace('width="120"','width="70"'));
  o.push(G.txt(80,280,"Präparat","mid dim")+G.txt(323,360,"Papier","mid dim")+G.txt(448,360,"5 mm Alu","mid dim")+G.txt(580,360,"Blei","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Zählrate hinter dem Absorber <b>≈ '+rate+' Imp/min</b></span><span class="chip">'+(anteil===0?"gestoppt, nur noch Nullrate":(anteil<0.5?"stark geschwächt":"kommt durch"))+'</span>'};
}


/* Luftballon: gesammelte Radon-Folgeprodukte, vereinfacht mit einer Halbwertszeit von etwa 35 min */
function ballon(){
  var o=[], gerieben=S.ball==="1", t=+S.t, extra=gerieben?Math.round(210*Math.pow(0.5,t/35)):Math.round(6*Math.pow(0.5,t/35)), rate=24+extra, i;
  o.push(geraet(40,90,rate)+'<line x1="260" y1="155" x2="280" y2="155" stroke="#9FB2CF" stroke-width="4"/>'+rohr(280,155));
  o.push('<path d="M432 170 q-6 -30 18 -34 q10 -18 30 -6 q24 -8 26 16 q16 14 -4 30 q-10 16 -34 8 q-24 10 -36 -14z" fill="#E8604A"/>');
  for(i=0;i<8;i++){ var a=i*0.8, r=10+(i%3)*8; if(gerieben&&i<Math.max(1,Math.round(8*Math.pow(0.5,t/35)))) o.push(G.circ(470+r*Math.cos(a),156+r*Math.sin(a)*0.7,3.2,"#FFE7A0")); }
  o.push(G.txt(470,215,"Ballonhülle","mid dim"));
  /* Kurve der Zählrate über der Zeit */
  var x0=90,y0=410,sx=5,sy=0.55,pts=[];
  for(i=0;i<=120;i+=4) pts.push(G.f1(x0+i*sx)+","+G.f1(y0-(24+(gerieben?210:6)*Math.pow(0.5,i/35))*sy));
  o.push('<polyline points="'+pts.join(" ")+'" fill="none" stroke="#6FE39A" stroke-width="2.5"/>');
  o.push(G.dash(x0,y0-24*sy,x0+600,y0-24*sy,"#9AAAC0",1.5,0,0.8)+G.txt(x0+606,y0-24*sy+5,"Nullrate","dim"));
  o.push('<line x1="'+x0+'" y1="'+y0+'" x2="'+(x0+610)+'" y2="'+y0+'" stroke="#9AAAC0" stroke-width="1.5"/><line x1="'+x0+'" y1="'+y0+'" x2="'+x0+'" y2="'+(y0-150)+'" stroke="#9AAAC0" stroke-width="1.5"/>');
  o.push(G.circ(x0+t*sx,y0-rate*sy,7,"#FFC53D")+G.txt(x0+450,y0-150,"Zeit nach dem Abnehmen in Minuten","mid dim"));
  [0,30,60,90,120].forEach(function(m){ o.push(G.txt(x0+m*sx,y0+22,""+m,"mid dim")); });
  return {svg:o.join(""), readout:'<span class="chip">Zählrate <b>'+rate+' Imp/min</b></span><span class="chip">'+(gerieben?(extra>12?"deutlich über der Nullrate":"fast wieder Nullrate"):"ungerieben: kaum mehr als die Nullrate")+'</span>'};
}

/* Ablenkung im elektrischen Feld (qualitativ, Bahnen als Parabeln) */
function efeld(){
  var o=[], t=S.ef, an=S.spannung==="1", col=t==="a"?ALPHA:(t==="b"?ELEK:GAMMA), x1=250, x2=650, y=220, i, pts=[], k, hit=null;
  o.push(G.rect(x1,86,x2-x1,14,"#FF7A59",an?1:0.3)+G.rect(x1,340,x2-x1,14,"#4CC9F0",an?1:0.3));
  o.push(G.txt(x2+14,98,"+ Pluspol","")+G.txt(x2+14,352,"− Minuspol",""));
  if(an) for(i=0;i<9;i++) o.push('<line x1="'+(x1+25+i*44)+'" y1="104" x2="'+(x1+25+i*44)+'" y2="336" stroke="#9AAAC0" stroke-width="1" stroke-dasharray="3 6" opacity=".5"/>');
  o.push('<path d="M40 250 h80 l-10 -40 h-60z" fill="#9FB2CF"/>'+G.circ(80,220,22,"url(#gGlow)"));
  k=!an||t==="g"?0:(t==="a"?0.00035:-0.004);
  pts.push("120,"+y, x1+","+y);
  for(i=x1+5;i<=800;i+=5){
    var dx=Math.min(i,x2)-x1, yy=y+k*dx*dx+(i>x2?2*k*(x2-x1)*(i-x2):0);
    if(i<=x2&&(yy<100||yy>340)){ hit=[i,yy<100?100:340]; pts.push(G.f1(i)+","+hit[1]); break; }
    pts.push(G.f1(i)+","+G.f1(yy));
  }
  if(t==="g"){ var p="M120 220",x=120; while(x<800){ p+=" q8 "+(((x/16)|0)%2?10:-10)+" 16 0"; x+=16; } o.push('<path d="'+p+'" fill="none" stroke="'+col+'" stroke-width="3"/>'); }
  else o.push('<polyline points="'+pts.join(" ")+'" fill="none" stroke="'+col+'" stroke-width="4"/>');
  if(hit) o.push(G.circ(hit[0],hit[1],9,"url(#gGlow)"));
  var txt=!an?"keine Spannung: alle fliegen geradeaus":(t==="a"?"α ist positiv: leicht zum Minuspol":(t==="b"?"β⁻ ist negativ: stark zum Pluspol":"γ hat keine Ladung: keine Ablenkung"));
  return {svg:o.join(""), readout:'<span class="chip"><b>'+txt+'</b></span>'};
}

/* Bleidicke: γ wird pro Halbwertsdicke halbiert (hier 1,3 cm, Buchwert) */
function blei(){
  var o=[], d=+S.dicke, hvl=1.3, n0=800, netto=n0*Math.pow(0.5,d/hvl), rate=24+Math.round(netto), i;
  o.push('<path d="M40 190 h80 l-10 -40 h-60z" fill="#9FB2CF"/>'+G.circ(80,160,22,"url(#gGlow)"));
  var bw=d*30; o.push(G.rect(200,60,bw,160,"#4D5E77",1,' stroke="#9FB2CF" stroke-width="1"'));
  for(i=1;i*hvl<=d+1e-9;i++) o.push('<line x1="'+G.f1(200+i*hvl*30)+'" y1="60" x2="'+G.f1(200+i*hvl*30)+'" y2="220" stroke="#9FB2CF" stroke-width="1" stroke-dasharray="3 4"/>');
  var p="M120 160",x=120; while(x<632){ p+=" q8 "+(((x/16)|0)%2?10:-10)+" 16 0"; x+=16; }
  o.push('<path d="'+p+'" fill="none" stroke="'+GAMMA+'" stroke-width="3" stroke-opacity="'+G.f1(Math.max(0.15,netto/n0))+'"/>');
  o.push(rohr(640,160));
  o.push(G.txt(80,220,"γ-Strahler","mid dim")+G.txt(200+bw/2,244,d>0?"Blei "+d.toFixed(1).replace(".",",")+" cm":"kein Blei","mid"));
  /* Diagramm Zählrate über Dicke */
  var gx=120,gy=392,sx=60,sy=0.145,pts=[];
  for(i=0;i<=100;i++) pts.push(G.f1(gx+i/10*sx)+","+G.f1(gy-(24+n0*Math.pow(0.5,i/10/hvl))*sy));
  o.push('<line x1="'+gx+'" y1="'+gy+'" x2="'+(gx+610)+'" y2="'+gy+'" stroke="#9AAAC0" stroke-width="1.5"/><line x1="'+gx+'" y1="'+gy+'" x2="'+gx+'" y2="'+(gy-150)+'" stroke="#9AAAC0" stroke-width="1.5"/>');
  o.push('<polyline points="'+pts.join(" ")+'" fill="none" stroke="#6FE39A" stroke-width="2.5"/>');
  o.push(G.dash(gx,gy-24*sy,gx+600,gy-24*sy,"#9AAAC0",1.5,0,0.8)+G.txt(gx+606,gy-24*sy-6,"Nullrate","dim"));
  [0,2,4,6,8,10].forEach(function(m){ if(m!==4&&m!==6) o.push(G.txt(gx+m*sx,gy+22,""+m,"mid dim")); });
  o.push(G.circ(gx+d*sx,gy-rate*sy,7,"#FFC53D")+G.txt(gx+300,gy+22,"Bleidicke in cm","mid dim"));
  var proz=100*Math.pow(0.5,d/hvl);
  return {svg:o.join(""), readout:'<span class="chip">durchgelassen <b>'+(proz>=10?Math.round(proz):proz.toFixed(proz>=1?1:2).replace(".",","))+' %</b></span><span class="chip">Zählrate <b>'+rate+' Imp/min</b></span>'+(netto<5?'<span class="chip">nicht null, aber in der Nullrate versteckt</span>':'')};
}

window.LAB={state:S, widget:widget, widgetAct:function(t){ UA[+t.getAttribute("data-w")]=+t.getAttribute("data-v"); },
 draw:function(cfg){ return {nullrate:nullrate,abstand:abstand,zerfall:zerfall,durch:durch,ballon:ballon,efeld:efeld,blei:blei}[cfg.mode](cfg); },
 QZ:[
  {q:"Ein Kern sendet ein α-Teilchen aus. Wie ändern sich A und Z?", o:["A − 4, Z − 2","A − 2, Z − 4","A bleibt, Z + 1"],a:0, w:"Das α-Teilchen ist ein Heliumkern mit 2 Protonen und 2 Neutronen."},
  {q:"Warum misst das Zählrohr auch ohne Präparat Impulse?", o:["Das Gerät ist kaputt","Es gibt überall natürliche Strahlung","Das Zählrohr strahlt selbst"],a:1, w:"Boden, Baustoffe, Weltall und unser Körper senden ständig ein wenig Strahlung aus."},
  {q:"Welche Strahlung wird schon von einem Blatt Papier gestoppt?", o:["α","β","γ"],a:0, w:"α-Teilchen sind groß und doppelt geladen. Sie geben ihre Energie sehr schnell ab."},
  {q:"Eine Strahlung wird im elektrischen Feld zum Pluspol abgelenkt. Welche ist es?", o:["α","β⁻","γ"],a:1, w:"Zum Pluspol wird nur negative Ladung gezogen. β⁻-Strahlung besteht aus Elektronen."},
  {q:"1,3 cm Blei halbieren die γ-Strahlung. Was bleibt hinter 2,6 cm?", o:["nichts","ein Viertel","ein Drittel"],a:1, w:"Die zweite Schicht halbiert noch einmal: die Hälfte der Hälfte ist ein Viertel."},
  {q:"Ein geriebener Luftballon ist nach einiger Zeit im Raum leicht radioaktiv. Warum?", o:["Reiben macht Atome radioaktiv","Er sammelt radioaktive Teilchen aus der Luft","Gummi ist radioaktiv"],a:1, w:"Der geladene Ballon zieht Folgeprodukte des radioaktiven Gases Radon an. Sie zerfallen nach und nach."},
  {q:"Kann man vorhersagen, wann ein bestimmter Kern zerfällt?", o:["Ja, auf die Sekunde","Nein, das ist Zufall","Nur bei γ-Strahlung"],a:1, w:"Für einen einzelnen Kern ist der Zeitpunkt zufällig. Nur für sehr viele Kerne lässt sich etwas vorhersagen."}
 ],
 scenes:[
  {kicker:"Kernphysik · Leitfrage 2", title:"Das Zählrohr klickt von allein",
   html:"<p>Ein Zählrohr misst jeweils eine Minute lang, ganz ohne Präparat. Schiebe den Regler für die nächste Messung.</p>",
   ask:"Warum ist jede Messung anders? Woher kommt die Strahlung?",
   note:"Passt zu Blatt W03 (Nullrate). Die Werte sind simuliert und schwanken zufällig um 24 Impulse pro Minute. Echte Nullraten liegen je nach Zählrohr und Ort etwa zwischen 10 und 40.",
   controls:{sl:[{k:"mess",label:"Messung Nr.",min:1,max:10,step:1,fmt:function(v){return v}}],reset:{mess:1}},
   cfg:{mode:"nullrate"}, alt:"Zählgerät mit Zählrohr und Balken der Messungen"},

  {kicker:"Versuch", title:"Ist ein Luftballon radioaktiv?",
   html:"<p>Ein Luftballon wird an Wolle gerieben und hängt eine Weile im Raum. Dann kommt die Hülle vor das Zählrohr. Verändere die Zeit nach dem Abnehmen.</p>",
   ask:"Woher kommt die zusätzliche Strahlung, und warum wird sie weniger?",
   note:"Passt zu Blatt W03, Aufgabe 5. Der geladene Ballon sammelt Folgeprodukte des Edelgases Radon (vor allem Pb-214 und Bi-214) aus der Luft. Die Kurve ist vereinfacht mit etwa 35 min Halbwertszeit gerechnet. Im Keller klappt der echte Versuch am besten, den Ballon 20 bis 30 min hängen lassen und zügig messen.",
   controls:{btn:[{k:"ball",label:"Ballon:",opts:[["1","gerieben"],["0","nicht gerieben"]]}],sl:[{k:"t",label:"Zeit",min:0,max:120,step:5,fmt:function(v){return v+" min"}}],reset:{t:0,ball:"1"}},
   cfg:{mode:"ballon"}, alt:"Ballonhülle vor dem Zählrohr und Kurve der Zählrate"},

  {kicker:"Versuch", title:"Präparat und Abstand",
   html:"<p>Jetzt liegt ein Präparat vor dem Zählrohr. Verändere den Abstand.</p>",
   ask:"Wie hängt die Zählrate vom Abstand ab?",
   note:"Präparate nur durch die Lehrkraft und nach den Regeln des Strahlenschutzes. Die Simulation nimmt ab mit dem Quadrat des Abstands (Luftabsorption vernachlässigt).",
   controls:{btn:[{k:"praep",label:"Präparat:",opts:[["0","ohne"],["1","mit"]]}],sl:[{k:"d",label:"Abstand",min:2,max:18,step:1,fmt:function(v){return v+" cm"}}],reset:{d:6}},
   cfg:{mode:"abstand"}, alt:"Präparat vor dem Zählrohr"},

  {kicker:"Schritt 1", title:"Alpha, Beta und Gamma",
   html:"<dl class=\"terms\"><div><dt>α</dt><dd>Heliumkern, 2 Protonen und 2 Neutronen</dd></div><div><dt>β⁻</dt><dd>Ein Neutron wird zum Proton, ein Elektron fliegt weg.</dd></div><div><dt>γ</dt><dd>energiereiche Strahlung, der Kern gibt nur Energie ab</dd></div></dl>",
   ask:"Bei welcher Strahlung ändert sich das Element?",
   note:"Ba-137m ist ein angeregter Kern, der beim Zerfall von Cs-137 entsteht. Das „m“ steht für metastabil.",
   controls:{btn:[{k:"art",label:"Zerfall:",opts:[["a","α"],["b","β⁻"],["g","γ"]]}]},
   cfg:{mode:"zerfall"}, alt:"Kern vor und nach dem Zerfall"},

  {kicker:"Schritt 2", title:"Strahlung im elektrischen Feld",
   html:"<p>Die Strahlung fliegt zwischen zwei geladenen Platten hindurch. Wähle die Strahlungsart und schalte die Spannung ein und aus.</p>",
   ask:"Was verrät die Ablenkung über die Ladung der Strahlung?",
   note:"Passt zur Folie „Strahlung im elektrischen Feld“ und Blatt W04. Die Bahnen sind qualitativ. Das α-Teilchen ist rund 7000-mal so schwer wie ein Elektron und wird deshalb trotz doppelter Ladung deutlich weniger abgelenkt. Im Magnetfeld ist der Unterschied noch größer.",
   controls:{btn:[{k:"ef",label:"Strahlung:",opts:[["a","α"],["b","β⁻"],["g","γ"]]},{k:"spannung",label:"Spannung:",opts:[["1","an"],["0","aus"]]}]},
   cfg:{mode:"efeld"}, alt:"Strahlung zwischen zwei geladenen Platten"},

  {kicker:"Übung", title:"Zerfallsgleichungen", nostage:true, widget:"ueben",
   html:"<p>Welcher Kern entsteht? Oben und unten muss die Summe links und rechts gleich sein.</p>",
   note:"Passt zur Folie „5. Zerfallsgleichungen aufstellen“ und Blatt W05."},

  {kicker:"Versuch", title:"Wie weit kommt die Strahlung?",
   html:"<p>Wähle eine Strahlungsart und einen Absorber zwischen Präparat und Zählrohr.</p>",
   ask:"Welcher Absorber stoppt welche Strahlung?",
   note:"Passt zu Blatt W05. Werte vereinfacht: 5 mm Aluminium halten die β-Strahlung eines Schulpräparats ab, dickes Blei schwächt γ nur.",
   controls:{btn:[{k:"strahl",label:"Strahlung:",opts:[["a","α"],["b","β"],["g","γ"]]},{k:"absorber",label:"Absorber:",opts:[["kein","keiner"],["papier","Papier"],["alu","Aluminium"],["blei","Blei"]]}]},
   cfg:{mode:"durch"}, alt:"Strahlung trifft auf Absorber"},

  {kicker:"Versuch", title:"Wie dick muss das Blei sein?",
   html:"<p>Verändere die Dicke der Bleiplatte vor dem γ-Strahler und beobachte die Zählrate.</p>",
   ask:"Wird die Zählrate irgendwann null?",
   note:"Passt zu Blatt W05, Aufgabe 3. Gerechnet mit 1,3 cm Blei für die Hälfte (Wert aus dem Buch, passt zu Co-60 mit etwa 1,2 cm; bei Cs-137 sind es etwa 0,65 cm). Jede weitere Halbwertsdicke halbiert, was noch ankommt. Die Strahlung wird nie ganz null, sie verschwindet aber in der Nullrate. Beton muss für dieselbe Wirkung etwa fünf- bis siebenmal so dick sein.",
   controls:{sl:[{k:"dicke",label:"Blei",min:0,max:10,step:0.1,fmt:function(v){return v.toFixed(1).replace(".",",")+" cm"}}],reset:{dicke:0}},
   cfg:{mode:"blei"}, alt:"γ-Strahlung durch eine Bleiplatte und Kurve der Zählrate"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Instabile Kerne wandeln sich spontan um und senden dabei Strahlung aus. Das nennt man Radioaktivität. Wann ein einzelner Kern zerfällt, ist nicht vorhersagbar.</li><li>Bei jedem Zerfall bleiben Massenzahl und Ladung erhalten.</li><li>α wird schon von Papier gestoppt, β von einigen Millimetern Aluminium, γ erst von dickem Blei geschwächt, aber nie ganz gestoppt.</li><li>Im elektrischen Feld wird α zum Minuspol und β⁻ zum Pluspol abgelenkt, γ gar nicht.</li></ul>",
   askLabel:"Probier's aus", ask:"Such im Periodensystem ein Element mit mehr als 83 Protonen. Alle diese Elemente sind radioaktiv.",
   cfg:{mode:"zerfall"}, alt:"Zerfall eines Kerns"}
 ]};
})();
