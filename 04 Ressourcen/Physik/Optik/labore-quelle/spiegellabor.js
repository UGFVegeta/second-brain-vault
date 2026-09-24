/* Spiegellabor · Leitfrage 6: Was passiert mit dem Licht am Spiegel? */
(function(){
"use strict";
var S={a:40, kipp:0, g:150, ey:300, lot:"1", d:120, sicht:"direkt"};
var RAD=Math.PI/180;

function bogen(M,a0,a1,r,col){
  /* Winkel in Grad, mathematisch (0 = rechts, 90 = oben) */
  var x0=M[0]+r*Math.cos(a0*RAD), y0=M[1]-r*Math.sin(a0*RAD), x1=M[0]+r*Math.cos(a1*RAD), y1=M[1]-r*Math.sin(a1*RAD);
  return '<path d="M'+G.f1(x0)+' '+G.f1(y0)+' A'+r+' '+r+' 0 0 '+(a1>a0?0:1)+' '+G.f1(x1)+' '+G.f1(y1)+'" fill="none" stroke="'+(col||"#9DB8FF")+'" stroke-width="2"/>';
}
function griech(x,y,t,col){ return '<text x="'+G.f1(x)+'" y="'+G.f1(y)+'" font-family="Georgia,serif" font-style="italic" font-size="22" fill="'+(col||"#FFFFFF")+'" text-anchor="middle">'+t+'</text>'; }

function kreisscheibe(cfg){
  var o=[], M=[420,300], R=230, a=+S.a, k=cfg.kipp?+S.kipp:0, i, t;
  /* Kreisscheibe mit Gradeinteilung (obere Hälfte) */
  o.push('<g clip-path="url(#sc)">');
  o.push('<path d="M'+(M[0]-R)+' '+M[1]+' A'+R+' '+R+' 0 0 1 '+(M[0]+R)+' '+M[1]+'Z" fill="#141C28" stroke="#4D5E77" stroke-width="2"/>');
  for(i=0;i<=180;i+=5){ t=i%10===0?16:8; o.push('<line x1="'+G.f1(M[0]+R*Math.cos(i*RAD))+'" y1="'+G.f1(M[1]-R*Math.sin(i*RAD))+'" x2="'+G.f1(M[0]+(R-t)*Math.cos(i*RAD))+'" y2="'+G.f1(M[1]-(R-t)*Math.sin(i*RAD))+'" stroke="#4D5E77" stroke-width="1.5"/>'); }
  for(i=0;i<=90;i+=30){ [90-i,90+i].forEach(function(w){ o.push(G.txt(M[0]+(R-34)*Math.cos(w*RAD),M[1]-(R-34)*Math.sin(w*RAD)+6,i+"°","mid dim")); }); }
  /* Spiegel (gekippt um k Grad), Lot senkrecht dazu */
  var lot=90+k, sx=Math.cos(k*RAD), sy=Math.sin(k*RAD);
  o.push('<line x1="'+G.f1(M[0]-200*sx)+'" y1="'+G.f1(M[1]+200*sy)+'" x2="'+G.f1(M[0]+200*sx)+'" y2="'+G.f1(M[1]-200*sy)+'" stroke="#C6D1E1" stroke-width="7" stroke-linecap="round"/>');
  if(S.lot==="1") o.push(G.dash(M[0],M[1],M[0]+R*Math.cos(lot*RAD),M[1]-R*Math.sin(lot*RAD),"#9DB8FF",2,0,0.9));
  /* einfallender Strahl: Richtung auf der Kreisscheibe um a zum Lot, links */
  var ein=lot+a, aus=lot-a, L=R-12;
  var E=[M[0]+L*Math.cos(ein*RAD),M[1]-L*Math.sin(ein*RAD)], A=[M[0]+L*Math.cos(aus*RAD),M[1]-L*Math.sin(aus*RAD)];
  o.push('<rect x="'+G.f1(E[0]-26)+'" y="'+G.f1(E[1]-14)+'" width="52" height="28" rx="5" fill="#3B4A63" transform="rotate('+G.f1(-ein+180)+' '+G.f1(E[0])+' '+G.f1(E[1])+')"/>');
  o.push(G.arrow(E[0],E[1],M[0],M[1],"#FFC53D",3.2,0));
  var ausOK=aus>k-0.1 && aus<180+k;
  if(ausOK) o.push(G.arrow(M[0],M[1],A[0],A[1],"#FFC53D",3.2,0.8));
  o.push(bogen(M,lot,ein,70,"#FF8A3D")+bogen(M,aus,lot,86,"#4CC9F0"));
  o.push(griech(M[0]+96*Math.cos((lot+a/2)*RAD),M[1]-96*Math.sin((lot+a/2)*RAD)+8,"α","#FF8A3D"));
  o.push(griech(M[0]+112*Math.cos((lot-a/2)*RAD),M[1]-112*Math.sin((lot-a/2)*RAD)+8,"β","#4CC9F0"));
  o.push('</g>');
  o.push(G.txt(M[0],M[1]+34,"Spiegel","mid dim"));
  if(S.lot==="1") o.push(G.txt(M[0]+(R+14)*Math.cos(lot*RAD),Math.max(26,M[1]-(R+14)*Math.sin(lot*RAD)),"Lot","mid"));
  return {svg:o.join(""), readout:'<span class="chip">Einfallswinkel α <b>'+a+'°</b></span><span class="chip">Reflexionswinkel β <b>'+a+'°</b></span>'+(k?'<span class="chip">Spiegel gekippt um <b>'+k+'°</b></span>':'')};
}

function kerze(x,yFuss,s,op){
  return '<g opacity="'+(op==null?1:op)+'" transform="translate('+x+' '+yFuss+') scale('+s+')"><rect x="-11" y="-78" width="22" height="78" rx="2" fill="#F5E6C8"/><path d="M0 -78 q-13 -20 0 -42 q13 22 0 42z" fill="#FFB627"/></g>';
}

function bild(){
  var o=[], SX=420, g=+S.g, G0=SX-g, B0=SX+g, top=200, fuss=320, E=[SX-60,+S.ey], pts=[[G0,top-2,"#FF8A3D"],[G0,fuss,"#4CC9F0"]];
  o.push('<g clip-path="url(#sc)">');
  o.push(G.rect(SX-3,40,6,340,"#C6D1E1"));
  for(var y=48;y<380;y+=18) o.push('<line x1="'+(SX+3)+'" y1="'+y+'" x2="'+(SX+13)+'" y2="'+(y-9)+'" stroke="#4D5E77" stroke-width="1.5"/>');
  o.push(G.circ(G0,top-24,34,"url(#gGlow)"));
  o.push(kerze(G0,fuss,1.0)+kerze(B0,fuss,1.0,0.35));
  pts.forEach(function(p,i){
    var yb=p[1];                                  /* Bildpunkt spiegelsymmetrisch */
    var ym=yb+(E[1]-yb)*(SX-B0)/(E[0]-B0);       /* Sichtlinie Bildpunkt -> Auge trifft Spiegel */
    o.push(G.ray(p[0],p[1],SX,ym,p[2],2.6,0.1+0.3*i));
    o.push(G.arrow(SX,ym,E[0]+20,E[1]+(ym-E[1])*20/(SX-E[0]),p[2],2.6,0.6+0.3*i));
    o.push(G.dash(SX,ym,B0,yb,p[2],2,1.2,0.8));
  });
  o.push(G.eye(E[0],E[1],1,0.9));
  o.push(G.dash(G0,410,SX-6,410,"#9AAAC0",1.5,0,0.8)+G.dash(SX+6,410,B0,410,"#9AAAC0",1.5,0,0.8));
  o.push('</g>');
  o.push(griech((G0+SX)/2,402,"g")+griech((SX+B0)/2,402,"g"));
  o.push(G.txt(G0,fuss+30,"Gegenstand","mid dim")+G.txt(B0,fuss+30,"Spiegelbild","mid dim")+G.txt(SX,30,"Spiegel","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Abstand vor dem Spiegel <b>'+(g/10).toFixed(0)+' cm</b></span><span class="chip">Bild scheinbar hinter dem Spiegel <b>'+(g/10).toFixed(0)+' cm</b></span>'};
}

function person(x,kopf,fuss,op,col){
  var h=fuss-kopf, r=h*0.09, cy=kopf+r;
  return '<g opacity="'+op+'"><circle cx="'+x+'" cy="'+G.f1(cy)+'" r="'+G.f1(r)+'" fill="#C9B6A0"/><rect x="'+G.f1(x-r*0.75)+'" y="'+G.f1(cy+r)+'" width="'+G.f1(r*1.5)+'" height="'+G.f1(h*0.4)+'" rx="4" fill="'+(col||"#3B4A63")+'"/>'+
    '<line x1="'+G.f1(x-r*0.4)+'" y1="'+G.f1(cy+r+h*0.4)+'" x2="'+G.f1(x-r*0.6)+'" y2="'+fuss+'" stroke="'+(col||"#3B4A63")+'" stroke-width="'+G.f1(r*0.6)+'" stroke-linecap="round"/>'+
    '<line x1="'+G.f1(x+r*0.4)+'" y1="'+G.f1(cy+r+h*0.4)+'" x2="'+G.f1(x+r*0.6)+'" y2="'+fuss+'" stroke="'+(col||"#3B4A63")+'" stroke-width="'+G.f1(r*0.6)+'" stroke-linecap="round"/></g>';
}

function groesse(){
  var o=[], W=560, d=+S.d*0.9, P=W-d, B=W+d, kopf=60, fuss=400, auge=kopf+0.07*(fuss-kopf);
  var oben=(kopf+auge)/2, unten=(auge+fuss)/2;
  o.push('<g clip-path="url(#sc)">');
  o.push(G.rect(W-2,20,4,400,"#6B4A2B"));
  o.push(G.rect(W-6,oben,12,unten-oben,"#C6D1E1"));
  o.push(person(P,kopf,fuss,1)+person(B,kopf,fuss,0.35));
  o.push(G.circ(P+6,auge,3,"#05080F"));
  [[kopf,"#FF8A3D"],[fuss,"#4CC9F0"]].forEach(function(q,i){
    var ym=(q[0]+auge)/2;
    o.push(G.ray(P,q[0],W,ym,q[1],2.4,0.1+0.3*i)+G.arrow(W,ym,P+10,auge,q[1],2.4,0.6+0.3*i)+G.dash(W,ym,B,q[0],q[1],1.8,1.1,0.7));
  });
  o.push('</g>');
  o.push(G.txt(W+18,(oben+unten)/2,"Spiegel",""));
  o.push(G.txt(P,432,"Person, 1,70 m","mid dim"));
  var cm=Math.round(170*(unten-oben)/(fuss-kopf));
  return {svg:o.join(""), readout:'<span class="chip">Abstand zur Wand <b>'+(+S.d/100).toFixed(1).replace(".",",")+' m</b></span><span class="chip">nötige Spiegelhöhe <b>'+cm+' cm</b></span><span class="chip">halbe Körpergröße</span>'};
}

function ambulanz(){
  var o=[], rueck=S.sicht==="spiegel";
  o.push(G.rect(0,0,840,440,"#FFC53D",0.02));
  if(!rueck){
    o.push('<rect x="180" y="110" width="480" height="230" rx="26" fill="#E8ECF3"/><rect x="180" y="250" width="480" height="18" fill="#FF7A59"/>');
    o.push('<rect x="250" y="130" width="340" height="80" rx="10" fill="#26324A"/>');
    o.push('<g transform="translate(420 312) scale(-1 1)"><text x="0" y="0" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="48" fill="#B8391F">AMBULANZ</text></g>');
    o.push(G.circ(230,300,18,"#FFF3C4")+G.circ(610,300,18,"#FFF3C4")+G.circ(230,300,40,"url(#gGlow)")+G.circ(610,300,40,"url(#gGlow)"));
    o.push(G.txt(420,380,"Die Front des Krankenwagens, direkt angesehen","mid dim"));
  }else{
    o.push('<rect x="170" y="90" width="500" height="250" rx="60" fill="#26324A" stroke="#9AAAC0" stroke-width="8"/>');
    o.push('<clipPath id="rs"><rect x="178" y="98" width="484" height="234" rx="54"/></clipPath><g clip-path="url(#rs)">');
    o.push('<rect x="200" y="140" width="440" height="220" rx="24" fill="#E8ECF3"/><rect x="200" y="262" width="440" height="16" fill="#FF7A59"/>');
    o.push('<text x="420" y="318" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="44" fill="#B8391F">AMBULANZ</text></g>');
    o.push(G.txt(420,380,"Derselbe Krankenwagen im Rückspiegel des Autos davor","mid dim"));
  }
  return {svg:o.join(""), readout:'<span class="chip">'+(rueck?"Im Spiegel wird die Schrift richtig herum lesbar":"Die Schrift ist spiegelverkehrt aufgedruckt")+'</span>'};
}

window.LAB={state:S,
 draw:function(cfg){ return {scheibe:kreisscheibe,bild:bild,groesse:groesse,ambulanz:ambulanz}[cfg.mode](cfg); },
 QZ:[
  {q:"Ein Lichtstrahl trifft unter 35° zum Lot auf einen Spiegel. Wie groß ist der Reflexionswinkel?",
   o:["35°","55°","70°"],a:0, w:"Einfallswinkel = Reflexionswinkel. Beide werden zum Lot gemessen."},
  {q:"Du stehst 2 m vor einem Spiegel. Wie weit ist dein Spiegelbild von dir entfernt?",
   o:["2 m","4 m","1 m"],a:1, w:"Das Bild steht scheinbar 2 m hinter dem Spiegel, also 4 m von dir weg."},
  {q:"Du gehst weiter vom Spiegel weg. Musst du einen größeren Spiegel haben, um dich ganz zu sehen?",
   o:["Ja, doppelt so groß","Nein, halbe Körpergröße reicht immer","Ja, so groß wie du"],a:1, w:"Die nötige Spiegelhöhe hängt nicht vom Abstand ab."},
  {q:"Warum steht „AMBULANZ“ vorne auf dem Krankenwagen spiegelverkehrt?",
   o:["Damit Autofahrer davor es im Rückspiegel lesen können","Weil es so schöner aussieht","Damit man es nachts besser sieht"],a:0, w:"Der Rückspiegel vertauscht links und rechts noch einmal."}
 ],
 scenes:[
  {kicker:"Optik · Leitfrage 6", title:"Was passiert mit dem Licht am Spiegel?",
   html:"<p>Das ist euer Versuch mit der Kreisscheibe. Ein Lichtstrahl trifft genau in der Mitte auf den Spiegel.</p><p>Verändere den Einfallswinkel und beobachte den reflektierten Strahl.</p>",
   ask:"Wie hängt der Reflexionswinkel β vom Einfallswinkel α ab?",
   note:"Passt zum Versuchsblatt W10. Winkel immer zum Lot messen, nicht zum Spiegel.",
   controls:{sl:[{k:"a",label:"Einfallswinkel α",min:0,max:80,step:1,fmt:function(v){return v+"°"}}],reset:{a:40}},
   cfg:{mode:"scheibe"}, alt:"Kreisscheibe mit Spiegel, einfallendem und reflektiertem Strahl"},

  {kicker:"Schritt 1", title:"Warum misst man zum Lot?",
   html:"<p>Das <span class=\"term\">Lot</span> steht senkrecht auf dem Spiegel. Kippe den Spiegel: Das Lot kippt mit.</p>",
   ask:"Gilt α = β auch, wenn der Spiegel schief steht?",
   note:"Zum Spiegel gemessen gilt das Gesetz nur zufällig. Zum Lot gemessen gilt es immer.",
   controls:{btn:[{k:"lot",label:"Lot:",opts:[["1","zeigen"],["0","ausblenden"]]}],
     sl:[{k:"a",label:"Einfallswinkel α",min:0,max:70,step:1,fmt:function(v){return v+"°"}},{k:"kipp",label:"Spiegel kippen",min:-20,max:20,step:1,fmt:function(v){return v+"°"}}],reset:{a:40,kipp:0}},
   cfg:{mode:"scheibe",kipp:true}, alt:"Gekippter Spiegel mit Lot"},

  {kicker:"Schritt 2", title:"Das Spiegelbild",
   html:"<p>Das Licht von der Kerze wird am Spiegel reflektiert und gelangt ins Auge. Unser Gehirn verlängert die Strahlen geradlinig nach hinten.</p><p>Deshalb sehen wir das Bild scheinbar hinter dem Spiegel.</p>",
   ask:"Verschiebe die Kerze. Wo steht das Spiegelbild?",
   note:"Die gestrichelten Linien gibt es nicht wirklich. Hinter dem Spiegel ist kein Licht. Idee für die Stunde: Glasscheibe statt Spiegel, dahinter eine zweite, nicht brennende Kerze genau an der Bildstelle. Sie scheint zu brennen.",
   controls:{sl:[{k:"g",label:"Kerze bis Spiegel",min:80,max:300,step:5,fmt:function(v){return (v/10).toFixed(0)+" cm"}},{k:"ey",label:"Auge höher oder tiefer",min:220,max:400,step:5,fmt:function(v){return ""}}],reset:{g:150,ey:300}},
   cfg:{mode:"bild"}, alt:"Kerze vor einem Spiegel mit virtuellem Bild"},

  {kicker:"Anwendung", title:"Wie groß muss der Spiegel sein?",
   html:"<p>Eine Person möchte sich von Kopf bis Fuß sehen. Verschiebe sie näher an die Wand oder weiter weg.</p>",
   ask:"Hängt die nötige Größe des Spiegels vom Abstand ab?",
   note:"Passt zum Blatt W11. Oberkante auf halber Höhe zwischen Auge und Scheitel, Unterkante auf halber Höhe zwischen Auge und Füßen.",
   controls:{sl:[{k:"d",label:"Abstand zur Wand",min:40,max:300,step:5,fmt:function(v){return (v/100).toFixed(1).replace(".",",")+" m"}}],reset:{d:120}},
   cfg:{mode:"groesse"}, alt:"Person vor einem Wandspiegel mit Strahlengang"},

  {kicker:"Alltag", title:"Spiegelschrift auf dem Krankenwagen",
   html:"<p>Vorne auf vielen Krankenwagen steht das Wort AMBULANZ spiegelverkehrt.</p>",
   ask:"Für wen ist diese Schrift gedacht?",
   note:"Der Spiegel vertauscht vorne und hinten. Im Rückspiegel sieht die Schrift deshalb wieder richtig aus.",
   controls:{btn:[{k:"sicht",label:"Ansicht:",opts:[["direkt","direkt"],["spiegel","im Rückspiegel"]]}]},
   cfg:{mode:"ambulanz"}, alt:"Krankenwagen mit Spiegelschrift"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Trifft Licht auf einen Spiegel, wird es reflektiert. Dabei gilt: Einfallswinkel = Reflexionswinkel. Beide Winkel werden zum Lot gemessen.</li><li>Das Spiegelbild ist genauso groß wie der Gegenstand und steht scheinbar (virtuell) ebenso weit hinter dem Spiegel wie der Gegenstand davor.</li></ul>",
   askLabel:"Probier's aus", ask:"Schreibe deinen Namen so auf ein Blatt, dass man ihn im Spiegel richtig lesen kann.",
   cfg:{mode:"bild"}, alt:"Spiegelbild einer Kerze"}
 ]};
})();
