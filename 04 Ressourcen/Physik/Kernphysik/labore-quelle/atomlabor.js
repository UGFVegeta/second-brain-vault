/* Atomlabor · Kernphysik Klasse 10 · Leitfrage 1: Woraus besteht Materie? */
(function(){
"use strict";
var S={zoom:0, n:1000, p:6, nn:6, e:6, iso:"C14", kz:6, kn:8};
var PROT="#FF7A59", NEUT="#9FB2CF", ELEK="#4CC9F0";
var EL=[null,["H","Wasserstoff"],["He","Helium"],["Li","Lithium"],["Be","Beryllium"],["B","Bor"],["C","Kohlenstoff"],["N","Stickstoff"],["O","Sauerstoff"],["F","Fluor"],["Ne","Neon"],
        ["Na","Natrium"],["Mg","Magnesium"],["Al","Aluminium"],["Si","Silicium"],["P","Phosphor"],["S","Schwefel"],["Cl","Chlor"],["Ar","Argon"],["K","Kalium"],["Ca","Calcium"]];
/* stabile Nuklide (Massenzahlen) für Z = 1 bis 20 */
var STABIL={1:[1,2],2:[3,4],3:[6,7],4:[9],5:[10,11],6:[12,13],7:[14,15],8:[16,17,18],9:[19],10:[20,21,22],11:[23],12:[24,25,26],13:[27],14:[28,29,30],15:[31],16:[32,33,34,36],17:[35,37],18:[36,38,40],19:[39,41],20:[40,42,43,44,46,48]};

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
function elektron(x,y,r){ r=r||6; return G.circ(x,y,r+7,ELEK,' opacity=".2"')+G.circ(x,y,r,ELEK); }

function zoomen(){
  var o=[], z=Math.pow(10,+S.zoom), Ra=150*z, Rk=150*z/100000, C=[420,220];
  o.push(G.circ(C[0],C[1],Math.min(Ra,2000),"#4CC9F0",' fill-opacity="0.06" stroke="#4CC9F0" stroke-opacity=".5" stroke-dasharray="6 6"'));
  if(Ra<900){ for(var i=0;i<6;i++){ var a=i*1.047+0.3; o.push(elektron(C[0]+Ra*0.8*Math.cos(a),C[1]+Ra*0.8*Math.sin(a),Math.max(2,Math.min(6,Ra/30)))); } }
  if(Rk>=2) o.push(kern(C[0],C[1],6,6,Rk/3.3,4));
  else { o.push(G.circ(C[0],C[1],2,PROT)); o.push(G.dash(C[0]-10,C[1]-10,C[0]-120,C[1]-120,"#9DB8FF",1.5,0,0.8)+G.txt(C[0]-126,C[1]-126,"Kern: hier, aber viel zu klein","end")); }
  var breite=840/(Ra/0.5e-10)*1; /* Bild zeigt 840 px; Atomradius 0,5·10^-10 m entspricht Ra px */
  var m=breite, ex=Math.floor(Math.log10(m)), ma=(m/Math.pow(10,ex)).toFixed(1).replace(".",",");
  o.push(G.txt(20,428,"Bildbreite etwa "+ma+" · 10^"+ex+" m","dim"));
  var lab=Ra>500?"Du bist in der Hülle. Fast alles hier ist leer.":(Rk>40?"Der Kern: fast die gesamte Masse des Atoms":"Das Atom");
  return {svg:o.join(""), readout:'<span class="chip">Vergrößerung <b>'+(z<10?z.toFixed(1):Math.round(z).toLocaleString("de-DE"))+'-fach</b></span><span class="chip">'+lab+'</span>'};
}

function rutherford(){
  var o=[], n=+S.n, seed=7, i, back=Math.round(n/8000), leicht=Math.round(n*0.02), gerade=n-back-leicht;
  function r(){ seed=(seed*9301+49297)%233280; return seed/233280; }
  o.push(G.rect(400,40,10,360,"#FFD34D",0.8));
  o.push('<rect x="20" y="190" width="90" height="60" rx="8" fill="#3B4A63"/>');
  o.push(G.txt(65,275,"α-Quelle","mid dim")+G.txt(405,428,"Goldfolie","mid dim"));
  o.push(G.circ(420+390,220,0,"none"));
  var spuren=Math.min(40,Math.max(6,Math.round(n/250)));
  for(i=0;i<spuren;i++){
    var y=205+r()*30, t=r();
    if(t<0.08&&n>=500){ var ang=(r()-0.5)*1.2; o.push(G.ray(110,y,405,y,"#FF8A3D",1.4,0.02*i,0.8)+G.ray(405,y,405+300*Math.cos(ang),y+300*Math.sin(ang),"#FF8A3D",1.4,0.4+0.02*i,0.8)); }
    else o.push(G.ray(110,y,820,y+(r()-0.5)*16,"#FF8A3D",1.2,0.02*i,0.55));
  }
  if(back>0) o.push(G.ray(110,222,405,222,"#FF3D6E",2,0.1)+G.arrow(405,222,120,120,"#FF3D6E",2.2,0.6));
  o.push(G.rect(760,40,14,360,"#27344A")+G.txt(767,30,"Schirm","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">geradeaus <b>'+gerade.toLocaleString("de-DE")+'</b></span><span class="chip">leicht abgelenkt <b>'+leicht.toLocaleString("de-DE")+'</b></span><span class="chip">zurückgeprallt <b>'+back+'</b></span>'};
}

function schalen(e){ var s=[],cap=[2,8,8,2],i; for(i=0;i<4&&e>0;i++){ s.push(Math.min(e,cap[i])); e-=cap[i]; } return s; }

function bauen(){
  var o=[], p=+S.p, n=+S.nn, e=+S.e, A=p+n, C=[300,220], sch=schalen(e), i, k;
  for(i=0;i<sch.length;i++){ var R=70+i*48; o.push(G.circ(C[0],C[1],R,"none",' stroke="#4D5E77" stroke-dasharray="5 6"'));
    for(k=0;k<sch[i];k++){ var a=k*2*Math.PI/sch[i]+i*0.4; o.push(elektron(C[0]+R*Math.cos(a),C[1]+R*Math.sin(a),6)); } }
  o.push(kern(C[0],C[1],p,n,7,p*7+n));
  var el=EL[p], stab=(STABIL[p]||[]).indexOf(A)>=0, lad=p-e;
  o.push(nk(640,170,el?el[0]:"?",A,p,54));
  o.push(G.txt(640,240,el?el[1]:"",""));
  o.push(G.txt(640,280,lad===0?"Atom (neutral)":(lad>0?"Ion, "+lad+"-fach positiv":"Ion, "+(-lad)+"-fach negativ"),""));
  o.push(G.txt(640,320,stab?"Kern stabil":"Kern instabil: zerfällt",stab?"":""));
  return {svg:o.join(""), readout:'<span class="chip">Z = <b>'+p+'</b></span><span class="chip">A = <b>'+A+'</b></span><span class="chip">N = <b>'+n+'</b></span><span class="chip"><b>'+(stab?"stabil":"radioaktiv")+'</b></span>'};
}

var ISO={H1:["H",1,1,"stabil","gewöhnlicher Wasserstoff, 99,98 %"],H2:["H",2,1,"stabil","Deuterium, schweres Wasser"],H3:["H",3,1,"radioaktiv","Tritium, Leuchtfarbe"],
         C12:["C",12,6,"stabil","fast aller Kohlenstoff"],C13:["C",13,6,"stabil","etwa 1 %"],C14:["C",14,6,"radioaktiv","Altersbestimmung"],
         U235:["U",235,92,"radioaktiv","Brennstoff im Kernkraftwerk, 0,7 %"],U238:["U",238,92,"radioaktiv","über 99 % des Urans"]};
function isotop(){
  var o=[], d=ISO[S.iso], n=d[1]-d[2], big=d[2]>20;
  if(big) o.push(kern(300,220,Math.round(d[2]/6),Math.round(n/6),9,d[1])+G.txt(300,400,"vereinfacht: jede Kugel steht für 6 Teilchen","mid dim"));
  else o.push(kern(300,220,d[2],n,14,d[1]));
  o.push(nk(600,190,d[0],d[1],d[2],64));
  o.push(G.txt(560,260,d[2]+" Protonen, "+n+" Neutronen","")+G.txt(560,300,d[3],"")+G.txt(560,340,d[4],"dim"));
  return {svg:o.join(""), readout:'<span class="chip">'+(d[3]==="stabil"?"stabiler Kern":"<b>radioaktiver</b> Kern")+'</span>'};
}


/* Ausschnitt der Nuklidkarte Z = 1 bis 8. s stabil, m β⁻, p β⁺ bzw. Elektroneneinfang, a zerfällt in α-Teilchen. Leer: Kern existiert nicht. */
var KARTE={1:{0:"s",1:"s",2:"m"},2:{1:"s",2:"s",4:"m",6:"m"},3:{3:"s",4:"s",5:"m",6:"m",8:"m"},4:{3:"p",4:"a",5:"s",6:"m",7:"m",8:"m"},
           5:{3:"p",5:"s",6:"s",7:"m",8:"m",9:"m",10:"m"},6:{3:"p",4:"p",5:"p",6:"s",7:"s",8:"m",9:"m",10:"m"},
           7:{5:"p",6:"p",7:"s",8:"s",9:"m",10:"m"},8:{5:"p",6:"p",7:"p",8:"s",9:"s",10:"s"}};
var KF={s:["#0A1120","#E7EDF6","stabil"],m:["#4CC9F0","#0A1120","β⁻-Strahler: zu viele Neutronen"],p:["#FF7A59","#0A1120","β⁺-Strahler: zu wenige Neutronen"],a:["#FFD34D","#0A1120","zerfällt sofort in zwei α-Teilchen"]};
function karte(){
  var o=[], x0=120, cw=52, ch=40, z, n;
  for(z=1;z<=8;z++){
    var y=380-z*42;
    o.push(G.txt(x0-12,y+26,EL[z][0]+" "+z,"end"));
    for(n=0;n<=10;n++){
      var t=(KARTE[z]||{})[n], x=x0+n*cw, ist=(z===+S.kz&&n===+S.kn);
      if(t){ var f=KF[t]; o.push(G.rect(x+2,y+2,cw-4,ch-4,f[0],1,' rx="4" stroke="#4D5E77" stroke-width="1"'));
        o.push('<text x="'+(x+cw/2)+'" y="'+(y+25)+'" font-family="IBM Plex Mono,monospace" font-size="11" fill="'+f[1]+'" text-anchor="middle">'+EL[z][0]+"-"+(z+n)+'</text>'); }
      if(ist) o.push(G.rect(x,y,cw,ch,"none",null,' rx="5" stroke="#FFC53D" stroke-width="3.5"'));
    }
  }
  for(n=0;n<=10;n++) o.push(G.txt(x0+n*cw+cw/2,398,""+n,"mid dim"));
  o.push(G.txt(x0+5.5*cw,420,"Neutronenzahl N","mid dim")+G.txt(x0-12,22,"Z","end dim"));
  var lg=[["s","stabil"],["m","β⁻"],["p","β⁺"],["a","α"]];
  lg.forEach(function(l,i){ o.push(G.rect(x0+600,60+i*34,22,22,KF[l[0]][0],1,' rx="3" stroke="#9FB2CF"')+G.txt(x0+630,77+i*34,l[1],"")); });
  var t=(KARTE[+S.kz]||{})[+S.kn], A=+S.kz+(+S.kn), name=EL[+S.kz][1]+"-"+A;
  return {svg:o.join(""), readout:'<span class="chip"><b>'+name+'</b>: '+S.kz+' Protonen, '+S.kn+' Neutronen</span><span class="chip">'+(t?KF[t][2]:"diesen Kern gibt es nicht")+'</span>'};
}

window.LAB={state:S,
 draw:function(cfg){ return {zoom:zoomen,ruth:rutherford,bauen:bauen,iso:isotop,karte:karte}[cfg.mode](cfg); },
 QZ:[
  {q:"Was gibt die Kernladungszahl Z an?", o:["die Anzahl der Neutronen","die Anzahl der Protonen","Protonen und Neutronen zusammen"],a:1, w:"Z zählt die Protonen. Sie legt das Element fest."},
  {q:"Ein Atom hat 8 Protonen und 10 Neutronen. Wie lautet die Massenzahl A?", o:["8","10","18"],a:2, w:"A = Protonen + Neutronen = 18. Das ist Sauerstoff-18."},
  {q:"Warum fliegen fast alle α-Teilchen ungehindert durch die Goldfolie?", o:["Gold ist durchsichtig","Das Atom ist fast leer, der Kern winzig","Die Teilchen sind zu schnell"],a:1, w:"Nur wer fast genau einen Kern trifft, wird stark abgelenkt."},
  {q:"Ein Kern besteht aus 82 Protonen und 124 Neutronen. Welcher ist es?", o:["Blei-206","Blei-124","Wolfram-206"],a:0, w:"Z = 82 ist Blei, A = 82 + 124 = 206."},
  {q:"In der Nuklidkarte liegt Kohlenstoff-14 rechts von den stabilen Kohlenstoffkernen. Was heißt das?", o:["Er hat zu viele Neutronen und ist ein β⁻-Strahler","Er hat zu viele Protonen","Er ist besonders stabil"],a:0, w:"Rechts heißt mehr Neutronen. Beim β⁻-Zerfall wird ein Neutron zum Proton, aus C-14 wird N-14."},
  {q:"Kohlenstoff-12 und Kohlenstoff-14 unterscheiden sich in …", o:["der Protonenzahl","der Neutronenzahl","der Elektronenzahl"],a:1, w:"Isotope haben gleich viele Protonen, aber verschieden viele Neutronen."}
 ],
 scenes:[
  {kicker:"Kernphysik · Leitfrage 1", title:"Woraus besteht Materie?",
   html:"<p>Zoome in ein Atom hinein. Ganz am Anfang siehst du die Hülle, am Ende den Kern.</p>",
   ask:"Wie viel Platz nimmt der Kern im Atom ein?",
   note:"Passt zur Beobachte-Folie mit dem Stadion. Der Kern ist etwa 100 000-mal kleiner als das Atom.",
   controls:{sl:[{k:"zoom",label:"Vergrößerung",min:0,max:5,step:0.05,fmt:function(v){return "10^"+v.toFixed(1).replace(".",",")}}],reset:{zoom:0}},
   cfg:{mode:"zoom"}, alt:"Zoom vom Atom auf den Atomkern"},

  {kicker:"Versuch", title:"Rutherfords Streuversuch",
   html:"<p>1909 schoss man α-Teilchen auf eine hauchdünne Goldfolie. Wäre das Atom eine volle Kugel, müssten alle stecken bleiben oder abgelenkt werden.</p><p>Erhöhe die Zahl der Teilchen.</p>",
   ask:"Was schließt du aus den wenigen Teilchen, die zurückprallen?",
   note:"Ernest Rutherford, Hans Geiger und Ernest Marsden. Etwa eines von 8000 Teilchen prallte zurück. Den Versuch kann man in der Schule nicht nachmachen.",
   controls:{sl:[{k:"n",label:"Anzahl α-Teilchen",min:100,max:20000,step:100,fmt:function(v){return v.toLocaleString("de-DE")}}],reset:{n:1000}},
   cfg:{mode:"ruth"}, alt:"Streuung von α-Teilchen an einer Goldfolie"},

  {kicker:"Schritt 1", title:"Ein Atom bauen",
   html:"<p>Stelle Protonen, Neutronen und Elektronen ein. Rechts siehst du das Element in <span class=\"term\">Nuklidschreibweise</span>.</p><dl class=\"terms\"><div><dt>A</dt><dd>Massenzahl: Protonen + Neutronen</dd></div><div><dt>Z</dt><dd>Kernladungszahl: Protonen</dd></div></dl>",
   ask:"Was ändert sich, wenn du nur die Neutronen veränderst? Was, wenn du Elektronen wegnimmst?",
   note:"Die Schalen sind das einfache Schalenmodell aus der Chemie. „Instabil“ bezieht sich auf die Kerne, das ist der Übergang zu Leitfrage 2.",
   controls:{sl:[{k:"p",label:"Protonen",min:1,max:20,step:1,fmt:function(v){return v}},{k:"nn",label:"Neutronen",min:0,max:26,step:1,fmt:function(v){return v}},{k:"e",label:"Elektronen",min:0,max:20,step:1,fmt:function(v){return v}}],reset:{p:6,nn:6,e:6}},
   cfg:{mode:"bauen"}, alt:"Atommodell mit Kern und Elektronenschalen"},

  {kicker:"Schritt 2", title:"Isotope",
   html:"<p>Isotope sind Atome desselben Elements mit gleicher Protonenzahl, aber unterschiedlicher Neutronenzahl.</p>",
   ask:"Welche der Isotope sind radioaktiv?",
   note:"Deuterium und Tritium sind die Brennstoffe der Kernfusion (Leitfrage 5).",
   controls:{btn:[{k:"iso",label:"Isotop:",opts:[["H1","H-1"],["H2","H-2"],["H3","H-3"],["C12","C-12"],["C13","C-13"],["C14","C-14"],["U235","U-235"],["U238","U-238"]]}]},
   cfg:{mode:"iso"}, alt:"Isotope im Vergleich"},

  {kicker:"Schritt 3", title:"Die Nuklidkarte",
   html:"<p>In der Nuklidkarte steht jedes Kästchen für einen Kern. Nach oben wächst die Protonenzahl, nach rechts die Neutronenzahl. Wähle einen Kern mit den Reglern.</p>",
   ask:"Wo liegen die stabilen Kerne? Was passiert mit Kernen, die zu viele Neutronen haben?",
   note:"Ausschnitt Z = 1 bis 8, N = 0 bis 10. Leere Kästchen: Diese Kerne gibt es nicht, sie zerfallen praktisch sofort. β⁺ (Positron) und Elektroneneinfang sind im Bildungsplan nicht verlangt, sie zeigen nur, dass auch Kerne mit zu wenigen Neutronen zerfallen. Be-7 wandelt sich durch Elektroneneinfang um. Be-8 zerfällt in zwei α-Teilchen.",
   controls:{sl:[{k:"kz",label:"Protonen Z",min:1,max:8,step:1,fmt:function(v){return v}},{k:"kn",label:"Neutronen N",min:0,max:10,step:1,fmt:function(v){return v}}],reset:{kz:6,kn:8}},
   cfg:{mode:"karte"}, alt:"Ausschnitt der Nuklidkarte"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>", note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Der Atomkern enthält Protonen (positiv) und Neutronen (neutral). In der Atomhülle bewegen sich die Elektronen (negativ). Ein Atom ist nach außen neutral.</li><li>Isotope sind Atome desselben Elements mit gleicher Protonenzahl, aber unterschiedlicher Neutronenzahl.</li></ul>",
   askLabel:"Probier's aus", ask:"Suche im Periodensystem ein Element und baue sein häufigstes Atom im Labor nach.",
   cfg:{mode:"bauen"}, alt:"Atommodell"}
 ]};
})();
