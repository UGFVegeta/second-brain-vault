/* Sehlabor · Leitfrage 1: Warum sehen wir überhaupt etwas? */
(function(){
"use strict";
var S={on:"0", look:"ball", bild:"A", kl:"dunkel", dist:60};
var LAMP=[150,92], BALL=[445,300], EYE=[735,238];
var TH={dunkel:25, hell:40, reflektor:140};

function room(cfg){
  var o=[], on=cfg.force||S.on==="1", a=G.arrow, r=G.ray;
  o.push('<g clip-path="url(#sc)">');
  if(on) o.push(G.rect(0,0,840,440,"#FFC53D",0.05));
  o.push(G.ray(LAMP[0],0,LAMP[0],LAMP[1]-14,"#4D5E77",2,0));
  o.push(G.rect(320,330,250,10,"#4D5E77")+G.rect(335,340,10,100,"#4D5E77")+G.rect(545,340,10,100,"#4D5E77"));
  if(on){
    [[-40,300],[20,330],[250,420],[330,20],[520,40],[40,180]].forEach(function(p,i){ o.push(r(LAMP[0],LAMP[1],p[0],p[1],"#FFC53D",1.6,0.05*i,0.35)); });
    o.push(a(LAMP[0],LAMP[1],BALL[0]-22,BALL[1]-22,"#FFC53D",3,0));
    [[330,170],[560,150],[620,420],[300,410]].forEach(function(p,i){ o.push(r(BALL[0],BALL[1],p[0],p[1],"#FFC53D",1.4,0.9+0.05*i,0.4)); });
    o.push(a(BALL[0]+30,BALL[1]-8,EYE[0]-30,EYE[1]+4,"#FFC53D",3,1.1));
    o.push(G.circ(BALL[0],BALL[1],30,"url(#gBall)"));
  }else{
    o.push(G.circ(BALL[0],BALL[1],30,"#141C28",' stroke="#27344A" stroke-width="2"'));
    o.push(G.txt(BALL[0],BALL[1]+7,"?","mid dim"));
  }
  o.push(G.bulb(LAMP[0],LAMP[1],on,14));
  o.push(G.eye(EYE[0],EYE[1],-1,1.1));
  o.push('</g>');
  o.push(G.txt(LAMP[0]+30,LAMP[1]+6,on?"Lampe (Sender)":"Lampe aus",""));
  o.push(G.txt(BALL[0],BALL[1]+56,"Ball","mid dim"));
  o.push(G.txt(EYE[0],EYE[1]+46,"Auge (Empfänger)","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Lampe <b>'+(on?"an":"aus")+'</b></span><span class="chip">Licht vom Ball im Auge <b>'+(on?"ja":"nein")+'</b></span>'};
}

function sender(){
  var o=[], a=G.arrow;
  o.push(G.rect(0,0,840,440,"#FFC53D",0.05));
  o.push(G.ray(LAMP[0],0,LAMP[0],LAMP[1]-14,"#4D5E77",2,0));
  o.push(G.rect(320,330,250,10,"#4D5E77"));
  if(S.look==="lampe"){
    o.push(a(LAMP[0]+16,LAMP[1]+6,EYE[0]-30,EYE[1]-4,"#FFC53D",3,0));
    o.push(G.ray(LAMP[0],LAMP[1],BALL[0]-22,BALL[1]-22,"#FFC53D",1.6,0,0.35));
  }else{
    o.push(a(LAMP[0],LAMP[1],BALL[0]-22,BALL[1]-22,"#FFC53D",3,0));
    o.push(a(BALL[0]+30,BALL[1]-8,EYE[0]-30,EYE[1]+4,"#FFC53D",3,0.9));
  }
  o.push(G.circ(BALL[0],BALL[1],30,"url(#gBall)"));
  o.push(G.bulb(LAMP[0],LAMP[1],true,14));
  o.push(G.eye(EYE[0],EYE[1],-1,1.1));
  o.push(G.txt(LAMP[0]+30,LAMP[1]+6,"Sender",""));
  o.push(G.txt(BALL[0],BALL[1]+56,"beleuchteter Körper","mid dim"));
  o.push(G.txt(EYE[0],EYE[1]+46,"Empfänger","mid dim"));
  var rd=S.look==="lampe"?"Das Licht kommt direkt von der Lampe ins Auge.":"Der Ball wirft das Licht der Lampe ins Auge.";
  return {svg:o.join(""), readout:'<span class="chip">'+rd+'</span>'};
}

function sehstrahl(){
  var o=[], a=G.arrow;
  o.push(G.rect(0,0,840,440,"#FFC53D",0.05));
  o.push(G.ray(LAMP[0],0,LAMP[0],LAMP[1]-14,"#4D5E77",2,0));
  o.push(G.rect(320,330,250,10,"#4D5E77"));
  if(S.bild==="A"){
    [-14,0,14].forEach(function(k,i){ o.push(a(EYE[0]-30,EYE[1]+k*0.3,BALL[0]+32,BALL[1]-10+k,"#4CC9F0",2.6,0.15*i)); });
  }else{
    o.push(a(LAMP[0],LAMP[1],BALL[0]-22,BALL[1]-22,"#FFC53D",3,0));
    o.push(a(BALL[0]+30,BALL[1]-8,EYE[0]-30,EYE[1]+4,"#FFC53D",3,0.9));
  }
  o.push(G.circ(BALL[0],BALL[1],30,"url(#gBall)"));
  o.push(G.bulb(LAMP[0],LAMP[1],true,14));
  o.push(G.eye(EYE[0],EYE[1],-1,1.1));
  o.push('<text class="lbl" x="28" y="400" style="font-size:30px">Bild '+S.bild+'</text>');
  return {svg:o.join("")};
}

function street(){
  var o=[], d=+S.dist, T=TH[S.kl], vis=d<=T, px=190+d*3.9, a=G.arrow;
  o.push('<g clip-path="url(#sc)">');
  o.push(G.rect(0,318,840,90,"#141C28")+G.rect(0,360,840,4,"#27344A"));
  for(var k=0;k<14;k++) o.push(G.rect(20+k*62,386,30,4,"#4D5E77"));
  o.push(G.poly([[150,302],[840,236],[840,380]],"#FFC53D",0.13,"fade",0));
  o.push(G.poly([[150,302],[840,270],[840,340]],"#FFC53D",0.12,"fade",0));
  /* Auto */
  o.push('<rect x="22" y="282" width="130" height="36" rx="8" fill="#3B4A63"/><path d="M48 282 L68 256 L120 256 L136 282Z" fill="#3B4A63"/><rect x="74" y="261" width="40" height="19" rx="3" fill="#0A1120"/>');
  o.push(G.circ(52,322,12,"#101A2B",' stroke="#4D5E77" stroke-width="3"')+G.circ(122,322,12,"#101A2B",' stroke="#4D5E77" stroke-width="3"'));
  o.push(G.circ(150,302,6,"#FFF3C4")+G.circ(150,302,22,"url(#gGlow)"));
  o.push(G.eye(94,271,1,0.45));
  /* Person */
  var op=vis?1:0.28, body=S.kl==="hell"?"#E8ECF3":"#26324A";
  o.push('<g opacity="'+op+'">');
  o.push(G.circ(px,238,11,"#C9B6A0"));
  o.push('<rect x="'+(px-13)+'" y="251" width="26" height="46" rx="6" fill="'+body+'"/>');
  if(S.kl==="reflektor") o.push(G.rect(px-13,262,26,5,"#FFE29A")+G.rect(px-13,282,26,5,"#FFE29A"));
  o.push('<line x1="'+(px-6)+'" y1="297" x2="'+(px-8)+'" y2="330" stroke="'+body+'" stroke-width="7" stroke-linecap="round"/><line x1="'+(px+6)+'" y1="297" x2="'+(px+8)+'" y2="330" stroke="'+body+'" stroke-width="7" stroke-linecap="round"/>');
  o.push('</g>');
  o.push(a(px-16,272,104,272,"#FFC53D",vis?3:1.5,0.5,vis?0.95:0.25));
  o.push('</g>');
  o.push(G.txt(px,212,d+" m","mid"));
  o.push(G.txt(86,236,"Fahrer","mid dim"));
  return {svg:o.join(""), readout:'<span class="chip">Abstand <b>'+d+' m</b></span><span class="chip">Fahrer sieht dich <b>'+(vis?"ja":"kaum")+'</b></span><span class="chip">Richtwert: sichtbar bis etwa <b>'+T+' m</b></span>'};
}

var ITEMS=[
 ["Sonne","L","Sie ist so heiß, dass sie selbst leuchtet."],
 ["Mond","B","Er wirft nur das Licht der Sonne zurück."],
 ["Kerzenflamme","L","Die heiße Flamme sendet selbst Licht aus."],
 ["Glühwürmchen","L","Es erzeugt sein Licht selbst in seinem Körper."],
 ["Spiegel","B","Er wirft nur fremdes Licht zurück. Im Dunkeln siehst du ihn nicht."],
 ["Handybildschirm","L","Er leuchtet auch in einem ganz dunklen Raum."],
 ["Rückstrahler am Fahrrad","B","Er leuchtet nur auf, wenn ihn ein Scheinwerfer anstrahlt."],
 ["Blitz","L","Die extrem heiße Luft im Blitz leuchtet selbst."],
 ["weiße Wand","B","Sie wirft das Licht der Lampe zurück."],
 ["Venus am Abendhimmel","B","Sie ist ein Planet und wird von der Sonne beleuchtet."]
];
var SO={};
function widget(){
  var done=0, right=0;
  var h='<div class="sortgrid">'+ITEMS.map(function(it,i){
    var s=SO[i]; if(s){done++; if(s===it[1]) right++;}
    function b(v,l){var c="opt"; if(s){ if(v===it[1]) c+=" right"; else if(v===s) c+=" wrong"; } return '<button type="button" class="'+c+'" data-w="'+i+'" data-v="'+v+'"'+(s?" disabled":"")+'>'+l+'</button>';}
    return '<div class="q"><p class="qt">'+it[0]+'</p><div class="opts two">'+b("L","Lichtquelle")+b("B","beleuchtet")+'</div>'+(s?'<p class="why">'+it[2]+'</p>':'')+'</div>';
  }).join("")+'</div>';
  if(done===ITEMS.length) h+='<p class="score">Ergebnis: '+right+' von '+ITEMS.length+' richtig</p>';
  return h;
}

window.LAB={state:S, widget:widget, widgetAct:function(t){ SO[+t.getAttribute("data-w")]=t.getAttribute("data-v"); },
 draw:function(cfg){ return {room:room,sender:sender,sehstrahl:sehstrahl,street:street}[cfg.mode](cfg); },
 QZ:[
  {q:"In einem völlig dunklen Keller siehst du deine Hand nicht. Warum?",
   o:["Die Augen brauchen erst Zeit, um Sehstrahlen auszusenden","Es gelangt kein Licht von der Hand in dein Auge","Die Hand ist zu nah am Gesicht"],a:1,
   w:"Ohne Lichtquelle gibt es kein Licht, das die Hand zurückwerfen könnte. Also kommt nichts in deinem Auge an."},
  {q:"Welcher Körper ist eine Lichtquelle?",
   o:["Der Vollmond","Ein Glühwürmchen","Ein Spiegel"],a:1,
   w:"Das Glühwürmchen erzeugt sein Licht selbst. Mond und Spiegel werfen nur fremdes Licht zurück."},
  {q:"Der Rückstrahler am Fahrrad leuchtet im Scheinwerferlicht hell auf. Ist er eine Lichtquelle?",
   o:["Ja, er leuchtet doch","Nein, er wirft das Licht des Scheinwerfers zurück"],a:1,
   w:"Ohne Scheinwerfer bleibt er dunkel. Er ist ein beleuchteter Körper."},
  {q:"Nachts an der Straße: Womit sieht dich ein Autofahrer am frühesten?",
   o:["Mit dunkler Jacke","Mit heller Jacke","Mit Reflektoren an der Jacke"],a:2,
   w:"Reflektoren werfen besonders viel Licht zum Fahrer zurück. Er sieht dich dann schon aus großer Entfernung."}
 ],
 scenes:[
  {kicker:"Optik · Leitfrage 1", title:"Warum sehen wir überhaupt etwas?",
   html:"<p>Ein abgedunkelter Raum, eine Lampe, ein Ball auf dem Tisch. Schalte die Lampe ein und aus.</p>",
   ask:"Was ändert sich, wenn die Lampe angeht? Was vermutest du, warum?",
   note:"Passt zur Beobachte-Folie mit Licht an und aus. Vermutungen sammeln, noch nicht auflösen.",
   controls:{btn:[{k:"on",label:"Lampe:",opts:[["0","aus"],["1","an"]]}]},
   cfg:{mode:"room"}, alt:"Raum mit Lampe, Ball und Auge"},

  {kicker:"Schritt 1", title:"Sender und Empfänger",
   html:"<p>Wir sehen einen Gegenstand nur, wenn Licht von ihm in unser Auge gelangt.</p><p>Die Lampe ist der <span class=\"term\">Sender</span>, das Auge der <span class=\"term\">Empfänger</span>. Schau einmal die Lampe und einmal den Ball an.</p>",
   ask:"Welchen Weg nimmt das Licht, wenn du den Ball siehst?",
   note:"Erwartung: Lampe, dann Ball, dann Auge. Den Weg mit dem Finger nachfahren lassen.",
   controls:{btn:[{k:"look",label:"Du schaust auf:",opts:[["lampe","die Lampe"],["ball","den Ball"]]}]},
   cfg:{mode:"sender"}, alt:"Weg des Lichts von der Lampe über den Ball ins Auge"},

  {kicker:"Schritt 2", title:"Welches Bild stimmt?",
   html:"<p>Zwei Zeichnungen, zwei Ideen zum Sehen. Wechsle zwischen Bild A und Bild B.</p>",
   reveal:"<p><b>Bild B stimmt.</b> Das Licht läuft von der Lampe zum Ball und von dort in das Auge. Aus dem Auge kommen keine Strahlen heraus. Sonst könnten wir auch im Dunkeln sehen.</p>",
   note:"Die Idee der Sehstrahlen aus dem Auge ist eine häufige Fehlvorstellung. Erst abstimmen lassen, dann auflösen.",
   controls:{btn:[{k:"bild",label:"Zeige:",opts:[["A","Bild A"],["B","Bild B"]]}]},
   cfg:{mode:"sehstrahl"}, alt:"Zwei Vorstellungen vom Sehen"},

  {kicker:"Schritt 3", title:"Lichtquelle oder beleuchteter Körper?", nostage:true, widget:"sort",
   html:"<p><span class=\"term\">Lichtquellen</span> senden selbst Licht aus. <span class=\"term\">Beleuchtete Körper</span> werfen nur Licht zurück, das sie von einer Lichtquelle bekommen. Ordne zu.</p>",
   note:"Mond, Spiegel und Rückstrahler sind die Klassiker für Fehler. Nachfragen: Siehst du ihn auch im völlig dunklen Raum?"},

  {kicker:"Alltag", title:"Sehen und gesehen werden",
   html:"<p>Nachts auf der Straße: Das Auto hat Licht, du nicht. Der Fahrer sieht dich nur, wenn genug Licht von dir in sein Auge zurückkommt.</p><p class=\"small\">Richtwerte bei Abblendlicht. Die genauen Zahlen schwanken je nach Quelle.</p>",
   ask:"Stelle die Kleidung um und schiebe dich weiter weg. Ab wann sieht dich der Fahrer nicht mehr?",
   note:"Gesprächsanlass: Wer hat Reflektoren an Jacke oder Schulranzen?",
   controls:{btn:[{k:"kl",label:"Kleidung:",opts:[["dunkel","dunkel"],["hell","hell"],["reflektor","mit Reflektoren"]]}],
     sl:[{k:"dist",label:"Abstand zum Auto",min:10,max:160,step:5,fmt:function(v){return v+" m"}}]},
   cfg:{mode:"street"}, alt:"Auto mit Scheinwerfer und Fußgänger bei Nacht"},

  {kicker:"Kurz-Check", title:"Was hast du verstanden?", nostage:true, quiz:true,
   html:"<p>Wähle jeweils eine Antwort. Die Erklärung erscheint sofort.</p>",
   note:"Auch mit Handzeichen möglich."},

  {kicker:"Zusammenfassung", title:"Das solltest du mitnehmen",
   html:"<ul class=\"list\"><li>Wir sehen einen Gegenstand nur, wenn Licht von ihm in unser Auge gelangt. Die Lichtquelle ist der Sender, das Auge der Empfänger.</li><li>Lichtquellen senden selbst Licht aus (Selbstleuchter). Beleuchtete Körper senden nur Licht aus, das sie von einer Lichtquelle bekommen haben.</li></ul>",
   askLabel:"Probier's aus", ask:"Mach abends im Zimmer das Licht aus und warte eine Minute. Was siehst du noch? Woher kommt das Licht dafür?",
   cfg:{mode:"room",force:true}, alt:"Raum mit eingeschalteter Lampe"}
 ]};
})();
