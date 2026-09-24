/* Linsenlabor · Leitfrage 8: Wie kann eine Lupe vergrößern? (dünne Linse, Brennweite f, Linsengleichung 1/f = 1/g + 1/b) */
(function(){
"use strict";
var S={lupe:"0", art:"sammel", w:60, abstand:120, g:260};
var A=220, LX=420;

function linse(x,art,w){
  var h=150, d=10+w*0.35;
  if(art==="sammel") return '<path d="M'+x+' '+(A-h)+' Q'+(x+d)+' '+A+' '+x+' '+(A+h)+' Q'+(x-d)+' '+A+' '+x+' '+(A-h)+'Z" fill="#9DB8FF" fill-opacity=".28" stroke="#9DB8FF" stroke-width="2"/>';
  return '<path d="M'+(x-d)+' '+(A-h)+' Q'+x+' '+A+' '+(x-d)+' '+(A+h)+' L'+(x+d)+' '+(A+h)+' Q'+x+' '+A+' '+(x+d)+' '+(A-h)+'Z" fill="#9DB8FF" fill-opacity=".28" stroke="#9DB8FF" stroke-width="2"/>';
}
function brennweite(w){ return Math.round(26000/(w+40)); }   /* stärker gewölbt -> kürzere Brennweite (Modell) */
function F(x,t){ return G.circ(x,A,5,"#FFFFFF")+'<text x="'+x+'" y="'+(A+32)+'" font-family="Georgia,serif" font-style="italic" font-size="22" fill="#FFFFFF" text-anchor="middle">'+(t||"F")+'</text>'; }

function lupeText(){
  var o=[], mit=S.lupe==="1", i;
  o.push(G.rect(90,80,660,280,"#F8FAFD",1,' rx="8"'));
  var zeilen=[[120,300],[160,260],[200,320],[240,220],[280,300],[320,260]];
  zeilen.forEach(function(z){ o.push(G.rect(130,z[0],z[1],6,"#9AAAC0",1,' rx="3"')); });
  if(mit){
    o.push('<defs><clipPath id="lup"><circle cx="560" cy="220" r="118"/></clipPath></defs>');
    o.push('<g clip-path="url(#lup)">'+G.rect(420,80,300,300,"#F8FAFD"));
    zeilen.forEach(function(z){ o.push(G.rect(560+(130-560)*1.8,220+(z[0]-220)*1.8,z[1]*1.8,11,"#7C8592",1,' rx="5"')); });
    o.push('</g><circle cx="560" cy="220" r="118" fill="#9DB8FF" fill-opacity=".12" stroke="#4D5E77" stroke-width="10"/><line x1="645" y1="305" x2="730" y2="390" stroke="#4D5E77" stroke-width="18" stroke-linecap="round"/>');
  }
  return {svg:o.join(""), readout:'<span class="chip">'+(mit?"Unter der Lupe wirkt die Schrift größer":"Normale Schriftgröße")+'</span>'};
}

function parallel(cfg){
  var o=[], art=S.art, f=brennweite(+S.w), ys=cfg.drei?[-50,0,50]:[-110,-70,-35,0,35,70,110], i;
  o.push(G.dash(20,A,820,A,"#4D5E77",1.5,0,0.8));
  o.push(linse(LX,art,+S.w));
  ys.forEach(function(dy,i){
    var y=A+dy;
    o.push(G.ray(30,y,LX,y,"#FFC53D",2.4,0.03*i));
    if(art==="sammel"){
      var xe=820, ye=y+(A-y)*(xe-LX)/f;
      o.push(G.ray(LX,y,xe,ye,"#FFC53D",2.4,0.5+0.03*i));
    }else{
      var FX=LX-f, xe2=820, ye2=A+(y-A)*(xe2-FX)/(LX-FX);
      o.push(G.ray(LX,y,xe2,ye2,"#FFC53D",2.4,0.5+0.03*i));
      if(dy!==0) o.push(G.dash(LX,y,FX,A,"#9AAAC0",1.4,1,0.6));
    }
  });
  o.push(F(art==="sammel"?LX+f:LX-f));
  o.push(G.txt(LX,40,art==="sammel"?"Sammellinse":"Zerstreuungslinse","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Brennweite <b>'+(f/10).toFixed(1).replace(".",",")+' cm</b></span><span class="chip">'+(art==="sammel"?"Die Strahlen treffen sich im Brennpunkt":"Die Strahlen laufen auseinander, als kämen sie vom Brennpunkt")+'</span>'};
}

function brennglas(){
  var o=[], f=150, d=+S.abstand, SX=LX+d, h=110, fleck=Math.max(3,Math.abs(1-d/f)*h);
  for(var i=-4;i<=4;i++){ var y=A+i*26; o.push(G.ray(20,y,LX,y,"#FFC53D",2,0.02*Math.abs(i),0.8)); o.push(G.ray(LX,y,SX,y+(A-y)*d/f,"#FFC53D",2,0.5,0.8)); }
  o.push(linse(LX,"sammel",60));
  o.push(G.rect(SX,A-160,12,320,"#E8ECF3",0.9));
  var hitze=Math.max(0,1-fleck/60);
  o.push(G.circ(SX+6,A,fleck+20,"url(#gGlow)")+G.circ(SX+6,A,fleck,"#FFF3C4"));
  if(hitze>0.8) o.push(G.circ(SX+6,A,26,"url(#gHeat)"));
  o.push(F(LX+f)+G.txt(60,40,"Sonnenlicht","")+G.txt(SX+6,A+190>430?430:A+190,"Papier","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Abstand Linse – Papier <b>'+(d/10).toFixed(1).replace(".",",")+' cm</b></span><span class="chip">'+(hitze>0.8?"<b>Brennpunkt:</b> kleiner, sehr heller Fleck, hier wird es heiß":"Fleck noch zu groß")+'</span>'};
}

function kerze(x,yFuss,h,flip,op){
  var s=h/120, t='translate('+G.f1(x)+' '+G.f1(yFuss)+') scale('+G.f1(s*100)/100+' '+(flip?-1:1)*G.f1(s*100)/100+')';
  return '<g opacity="'+(op==null?1:op)+'" transform="'+t+'"><rect x="-11" y="-78" width="22" height="78" rx="2" fill="#F5E6C8"/><path d="M0 -78 q-13 -20 0 -42 q13 22 0 42z" fill="#FFB627"/></g>';
}

function bild(){
  var o=[], f=130, g=+S.g, Gh=90, GX=LX-g, top=[GX,A-Gh], b, B, reell, i;
  o.push(G.dash(20,A,820,A,"#4D5E77",1.5,0,0.8));
  o.push(linse(LX,"sammel",60));
  o.push(F(LX-f)+F(LX+f));
  o.push(kerze(GX,A,Gh,false));
  if(Math.abs(g-f)<3){ return {svg:o.join("")+G.txt(LX,40,"Gegenstand genau im Brennpunkt: kein Bild","mid"), readout:'<span class="chip"><b>kein Bild</b>: die Strahlen laufen parallel</span>'}; }
  b=1/(1/f-1/g); B=-Gh*b/g; reell=b>0;
  var BX=LX+b, bt=[BX,A-B];
  /* Parallelstrahl -> durch F rechts */
  var y1=top[1];
  o.push(G.ray(top[0],y1,LX,y1,"#FF8A3D",2.4,0));
  /* Mittelpunktstrahl */
  var m=(A-top[1])/(LX-top[0]);
  /* Brennpunktstrahl -> parallel */
  var yF=top[1]+(A-top[1])*(LX-top[0])/((LX-f)-top[0]);
  o.push(G.ray(top[0],top[1],LX,yF,"#4CC9F0",2.4,0.2));
  var XE=820;
  o.push(G.ray(LX,y1,XE,y1+(A-y1)*(XE-LX)/f,"#FF8A3D",2.4,0.6));
  o.push(G.ray(top[0],top[1],XE,top[1]+m*(XE-top[0]),"#FFFFFF",2,0.4,0.9));
  o.push(G.ray(LX,yF,XE,yF,"#4CC9F0",2.4,0.8));
  if(reell){
    o.push(kerze(BX,A,Math.abs(B),true,0.95));
  }else{
    o.push(G.dash(LX,y1,BX,bt[1],"#FF8A3D",1.6,1,0.7)+G.dash(LX,yF,BX,bt[1],"#4CC9F0",1.6,1,0.7)+G.dash(top[0],top[1],BX,bt[1],"#FFFFFF",1.4,1,0.6));
    o.push(kerze(BX,A,Math.abs(B),false,0.45));
    o.push(G.eye(760,A-20,-1,0.9));
  }
  o.push(G.txt(GX,A+30,"Gegenstand","mid dim"));
  var v=Math.abs(B)/Gh;
  var art=reell?"reell, umgekehrt":"virtuell, aufrecht (Lupe)";
  return {svg:o.join(""), readout:'<span class="chip">Gegenstand <b>'+(g>f?(g>2*f?"außerhalb 2f":"zwischen f und 2f"):"innerhalb f")+'</b></span><span class="chip">Bild <b>'+art+'</b></span><span class="chip">'+(v>1.02?"vergrößert":(v<0.98?"verkleinert":"gleich groß"))+' ('+v.toFixed(1).replace(".",",")+'-fach)</span>'};
}

window.LAB={state:S,
 draw:function(cfg){ return {lupe:lupeText,parallel:parallel,brennglas:brennglas,bild:bild}[cfg.mode](cfg); },
 QZ:[
  {q:"Was passiert mit parallelem Licht an einer Sammellinse?",
   o:["Es läuft auseinander","Es trifft sich im Brennpunkt","Es bleibt parallel"],a:1, w:"Die Sammellinse bündelt paralleles Licht im Brennpunkt."},
  {q:"Woran erkennst du eine Sammellinse?",
   o:["Sie ist in der Mitte dicker als am Rand","Sie ist am Rand dicker als in der Mitte","Sie ist überall gleich dick"],a:0, w:"Sammellinsen sind in der Mitte dicker, Zerstreuungslinsen am Rand."},
  {q:"Eine Linse ist stärker gewölbt. Was passiert mit der Brennweite?",
   o:["Sie wird kürzer","Sie wird länger","Sie bleibt gleich"],a:0, w:"Eine stärker gewölbte Linse bricht stärker. Der Brennpunkt rückt näher."},
  {q:"Warum soll man keine Glasflaschen im Wald liegen lassen?",
   o:["Sie können wie ein Brennglas Sonnenlicht bündeln","Sie spiegeln Tiere an","Sie werden nie abgebaut, sonst nichts"],a:0, w:"Im Brennpunkt wird es so heiß, dass trockenes Laub zu brennen anfangen kann."}
 ],
 scenes:[
  {kicker:"Optik · Leitfrage 8", title:"Wie kann eine Lupe vergrößern?",
   html:"<p>Dieselbe Schrift, einmal ohne und einmal mit Lupe.</p>", ask:"Was fällt dir auf? Was vermutest du, wie die Lupe das macht?",
   note:"Passt zur Beobachte-Folie. Lupen durchgeben lassen.",
   controls:{btn:[{k:"lupe",label:"Lupe:",opts:[["0","ohne"],["1","mit"]]}]},
   cfg:{mode:"lupe"}, alt:"Text mit und ohne Lupe"},

  {kicker:"Versuch", title:"Drei parallele Strahlen",
   html:"<p>Das ist euer Versuch mit der Ray-Box. Drei parallele Strahlen treffen auf eine Linse.</p>",
   ask:"Was passiert hinter der Sammellinse, was hinter der Zerstreuungslinse?",
   note:"Passt zum Versuchsblatt W13.",
   controls:{btn:[{k:"art",label:"Linse:",opts:[["sammel","Sammellinse"],["zerstreu","Zerstreuungslinse"]]}]},
   cfg:{mode:"parallel",drei:true}, alt:"Drei parallele Strahlen an einer Linse"},

  {kicker:"Schritt 1", title:"Brennpunkt und Brennweite",
   html:"<p>Eine <span class=\"term\">Sammellinse</span> ist in der Mitte dicker. Sie bündelt paralleles Licht im <span class=\"term\">Brennpunkt</span> F. Eine <span class=\"term\">Zerstreuungslinse</span> ist am Rand dicker. Hinter ihr läuft das Licht auseinander.</p>",
   ask:"Wie verändert sich die Brennweite, wenn die Linse stärker gewölbt ist?",
   note:"Die Brennweite ist hier ein Modellwert. Echte Brennweite hängt auch vom Glas ab.",
   controls:{btn:[{k:"art",label:"Linse:",opts:[["sammel","Sammellinse"],["zerstreu","Zerstreuungslinse"]]}],
     sl:[{k:"w",label:"Wölbung",min:10,max:140,step:5,fmt:function(v){return v<50?"flach":(v<100?"mittel":"stark")}}],reset:{w:60}},
   cfg:{mode:"parallel"}, alt:"Parallele Strahlen an Sammel- und Zerstreuungslinse mit Brennpunkt"},

  {kicker:"Alltag", title:"Das Brennglas",
   html:"<p>Sonnenlicht fällt fast parallel ein. Eine Sammellinse bündelt es. Verschiebe das Papier.</p>",
   ask:"Wo wird der Lichtfleck am kleinsten, und warum wird es dort heiß?",
   note:"Sicherheit: Nie durch eine Linse in die Sonne schauen. Keine Glasflaschen oder Wasserflaschen in trockenem Gras liegen lassen.",
   controls:{sl:[{k:"abstand",label:"Abstand Linse – Papier",min:40,max:300,step:5,fmt:function(v){return (v/10).toFixed(1).replace(".",",")+" cm"}}],reset:{abstand:120}},
   cfg:{mode:"brennglas"}, alt:"Brennglas mit Sonnenlicht und Papier"},

  {kicker:"Ausblick", title:"Bilder an der Sammellinse",
   html:"<p>Schiebe die Kerze näher an die Linse. Achte auf das Bild rechts.</p><p class=\"small\">Das ist schon der nächste Schritt: So wirkt die Lupe.</p>",
   ask:"Wann entsteht ein vergrößertes, aufrechtes Bild wie bei der Lupe?",
   note:"Parallelstrahl wird zum Brennpunktstrahl, Brennpunktstrahl wird zum Parallelstrahl, Mittelpunktstrahl läuft gerade weiter. Innerhalb der Brennweite entsteht ein virtuelles Bild.",
   controls:{sl:[{k:"g",label:"Kerze bis Linse",min:60,max:380,step:5,fmt:function(v){return (v/10).toFixed(1).replace(".",",")+" cm"}}],reset:{g:260}},
   cfg:{mode:"bild"}, alt:"Bildentstehung an der Sammellinse"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Sammellinsen (konvex) brechen parallel einfallendes Licht so, dass es sich im Brennpunkt bündelt. Zerstreuungslinsen (konkav) lassen das Licht auseinanderlaufen.</li></ul>",
   askLabel:"Probier's aus", ask:"Lass einen Wassertropfen auf eine Klarsichtfolie fallen und leg sie über eine Zeitungsseite. Was siehst du durch den Tropfen?",
   cfg:{mode:"parallel",drei:true}, alt:"Sammellinse"}
 ]};
})();
