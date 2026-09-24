/* Gemeinsamer Rahmen der Optik-Labore (Stil wie Schattenlabor).
   Ein Labor setzt window.LAB = {state, scenes, QZ, draw(cfg) -> {svg, readout}, widget?, widgetAct?} */
(function(){
"use strict";
function f1(n){return Math.round(n*10)/10}
function ray(x1,y1,x2,y2,col,w,d,op){
  return '<line class="ray" pathLength="1" x1="'+f1(x1)+'" y1="'+f1(y1)+'" x2="'+f1(x2)+'" y2="'+f1(y2)+'" stroke="'+col+'" stroke-width="'+w+'" stroke-opacity="'+(op==null?1:op)+'" style="--d:'+(d||0)+'s"/>';
}
function dash(x1,y1,x2,y2,col,w,d,op){
  return '<line class="fade" x1="'+f1(x1)+'" y1="'+f1(y1)+'" x2="'+f1(x2)+'" y2="'+f1(y2)+'" stroke="'+col+'" stroke-width="'+w+'" stroke-opacity="'+(op==null?1:op)+'" stroke-dasharray="7 7" stroke-linecap="round" style="--d:'+(d||0)+'s"/>';
}
function head(x1,y1,x2,y2,col,d,op,sz){
  var dx=x2-x1, dy=y2-y1, l=Math.sqrt(dx*dx+dy*dy)||1, ux=dx/l, uy=dy/l, s=sz||13;
  var bx=x2-ux*s, by=y2-uy*s;
  return '<polygon class="fade" style="--d:'+(d||0)+'s" fill="'+col+'" fill-opacity="'+(op==null?1:op)+'" points="'+
    f1(x2)+','+f1(y2)+' '+f1(bx-uy*s*0.45)+','+f1(by+ux*s*0.45)+' '+f1(bx+uy*s*0.45)+','+f1(by-ux*s*0.45)+'"/>';
}
function arrow(x1,y1,x2,y2,col,w,d,op){ return ray(x1,y1,x2,y2,col,w,d,op)+head(x1,y1,x2,y2,col,(d||0)+0.75,op); }
function poly(pp,fill,op,cls,d){
  return '<polygon class="'+(cls||'')+'" style="--d:'+(d||0)+'s" points="'+pp.map(function(q){return f1(q[0])+","+f1(q[1])}).join(" ")+'" fill="'+fill+'" fill-opacity="'+op+'"/>';
}
function rect(x,y,w,h,fill,op,extra){
  if(h<0.5||w<0.5) return "";
  return '<rect x="'+f1(x)+'" y="'+f1(y)+'" width="'+f1(w)+'" height="'+f1(h)+'" fill="'+fill+'"'+(op!=null?' fill-opacity="'+op+'"':'')+(extra||'')+'/>';
}
function circ(x,y,r,fill,extra){ return '<circle cx="'+f1(x)+'" cy="'+f1(y)+'" r="'+f1(r)+'" fill="'+fill+'"'+(extra||'')+'/>'; }
function txt(x,y,s,cls){
  y=Math.max(22,Math.min(430,y));
  return '<text class="lbl '+(cls||"")+'" x="'+f1(x)+'" y="'+f1(y)+'">'+s+'</text>';
}
function defs(){
  return '<defs>'+
   '<clipPath id="sc"><rect x="0" y="0" width="840" height="440"/></clipPath>'+
   '<linearGradient id="gLight" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFC53D" stop-opacity=".42"/><stop offset="1" stop-color="#FFC53D" stop-opacity=".08"/></linearGradient>'+
   '<radialGradient id="gGlow"><stop offset="0" stop-color="#FFE7A0" stop-opacity=".95"/><stop offset="1" stop-color="#FFC53D" stop-opacity="0"/></radialGradient>'+
   '<radialGradient id="gSun" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#FFF3C4"/><stop offset="1" stop-color="#FFB627"/></radialGradient>'+
   '<radialGradient id="gHeat"><stop offset="0" stop-color="#FF7A59" stop-opacity=".8"/><stop offset="1" stop-color="#FF7A59" stop-opacity="0"/></radialGradient>'+
   '<radialGradient id="gBall" cx=".35" cy=".35" r=".75"><stop offset="0" stop-color="#FF9C7A"/><stop offset="1" stop-color="#B8391F"/></radialGradient>'+
   '</defs>';
}
function bulb(x,y,on,r){
  r=r||14;
  if(!on) return circ(x,y,r,"#1D283A",' stroke="#4D5E77" stroke-width="2"');
  return circ(x,y,r*3.4,"url(#gGlow)",' opacity=".7"')+circ(x,y,r,"url(#gSun)");
}
/* Auge von der Seite, dir = -1 schaut nach links, +1 nach rechts */
function eye(x,y,dir,s){
  s=s||1; var w=24*s, h=15*s;
  return '<path d="M'+f1(x-w)+' '+f1(y)+' Q'+f1(x)+' '+f1(y-h*1.5)+' '+f1(x+w)+' '+f1(y)+' Q'+f1(x)+' '+f1(y+h*1.5)+' '+f1(x-w)+' '+f1(y)+'Z" fill="#F8FAFD" stroke="#9AAAC0" stroke-width="1.5"/>'+
    circ(x+dir*8*s,y,9*s,"#3B7CC4")+circ(x+dir*9*s,y,4.2*s,"#05080F");
}
window.G={f1:f1,ray:ray,dash:dash,head:head,arrow:arrow,poly:poly,rect:rect,circ:circ,txt:txt,defs:defs,bulb:bulb,eye:eye};
})();
</script>
<script>
(function(){
"use strict";
var L=window.LAB, S=L.state;
var $=function(s){return document.querySelector(s)};
var svg=$("#svg"), copy=$("#copy"), readout=$("#readout"), ctrl=$("#ctrl");
var scenes=L.scenes, cur=0, qa=L.QZ.map(function(){return null}), rev={};

function quizHTML(){
  var done=0, right=0;
  var h="<div class=\"quiz\">"+L.QZ.map(function(z,i){
    var s=qa[i]; if(s!=null){done++; if(s===z.a) right++;}
    return "<div class=\"q\"><p class=\"qt\"><span class=\"qn\">Frage "+(i+1)+"</span>"+z.q+"</p><div class=\"opts\">"+
      z.o.map(function(t,j){
        var c="opt"; if(s!=null){ if(j===z.a) c+=" right"; else if(j===s) c+=" wrong"; }
        return "<button type=\"button\" class=\""+c+"\" data-q=\""+i+"\" data-o=\""+j+"\""+(s!=null?" disabled":"")+">"+t+"</button>";
      }).join("")+"</div>"+(s!=null?"<p class=\"why\">"+z.w+"</p>":"")+"</div>";
  }).join("")+"</div>";
  if(done===L.QZ.length) h+="<p class=\"score\">Ergebnis: "+right+" von "+L.QZ.length+" richtig</p>";
  return h;
}
function ctrlHTML(c){
  if(!c) return "";
  var h="";
  (c.btn||[]).forEach(function(g){
    h+="<div class=\"ctrl pts\">"+(g.label?"<span>"+g.label+"</span>":"")+g.opts.map(function(o){
      return "<button type=\"button\" class=\"btn\" data-k=\""+g.k+"\" data-v=\""+o[0]+"\" aria-pressed=\""+(String(S[g.k])===String(o[0]))+"\">"+o[1]+"</button>";
    }).join("")+"</div>";
  });
  if(c.sl){
    h+="<div class=\"ctrl\">"+c.sl.map(function(s){
      return "<label for=\"s_"+s.k+"\"><span class=\"row\"><span>"+s.label+"</span><output id=\"o_"+s.k+"\"></output></span>"+
        "<input id=\"s_"+s.k+"\" data-k=\""+s.k+"\" type=\"range\" min=\""+s.min+"\" max=\""+s.max+"\" step=\""+s.step+"\" value=\""+S[s.k]+"\"></label>";
    }).join("")+(c.reset?"<button type=\"button\" class=\"btn\" data-reset=\"1\">Ausgangswerte</button>":"")+"</div>";
  }
  return h;
}
function syncOut(){
  var c=scenes[cur].controls; if(!c||!c.sl) return;
  c.sl.forEach(function(s){ var o=document.getElementById("o_"+s.k); if(o) o.textContent=s.fmt?s.fmt(+S[s.k]):S[s.k]; });
}
function drawStage(anim){
  var s=scenes[cur]; if(!s.cfg) return;
  var b=L.draw(s.cfg);
  svg.setAttribute("class", anim?"anim":"");
  svg.setAttribute("aria-label", s.alt||"Zeichnung");
  svg.innerHTML=G.defs()+b.svg;
  readout.innerHTML=b.readout||"";
}
function revealHTML(){
  var s=scenes[cur];
  return rev[cur]?s.reveal:"<button class=\"btn\" type=\"button\" data-rev=\"1\">"+(s.revealBtn||"Auflösung zeigen")+"</button>";
}
function show(i,anim){
  cur=Math.max(0,Math.min(scenes.length-1,i));
  var s=scenes[cur];
  $("#app").classList.toggle("nostage",!!s.nostage);
  copy.innerHTML="<span class=\"kicker\">"+s.kicker+"</span><h1>"+s.title+"</h1>"+s.html+
    (s.widget?"<div id=\"widget\">"+L.widget(s.widget)+"</div>":"")+
    (s.quiz?"<div id=\"quiz\">"+quizHTML()+"</div>":"")+
    (s.reveal?"<div id=\"rev\">"+revealHTML()+"</div>":"")+
    (s.ask?"<div class=\"ask\"><span>"+(s.askLabel||"Frage")+"</span><p>"+s.ask+"</p></div>":"")+
    (s.note?"<aside class=\"notes\"><b>Hinweis für die Lehrkraft</b>"+s.note+"</aside>":"");
  ctrl.innerHTML=ctrlHTML(s.controls);
  syncOut();
  drawStage(anim!==false);
  $("#counter").textContent=(cur+1)+" / "+scenes.length;
  $("#bar").style.width=((cur+1)/scenes.length*100)+"%";
  $("#prev").disabled=cur===0; $("#next").disabled=cur===scenes.length-1;
  Array.prototype.forEach.call(document.querySelectorAll(".dot"),function(d,k){
    if(k===cur) d.setAttribute("aria-current","true"); else d.removeAttribute("aria-current");
  });
}
scenes.forEach(function(s,i){
  var b=document.createElement("button");
  b.type="button"; b.className="dot"; b.setAttribute("aria-label","Folie "+(i+1)+": "+s.title);
  b.addEventListener("click",function(){show(i)});
  $("#dots").appendChild(b);
});
$("#prev").addEventListener("click",function(){show(cur-1)});
$("#next").addEventListener("click",function(){show(cur+1)});
$("#btnNotes").addEventListener("click",function(){
  var on=!document.body.classList.contains("shownotes");
  document.body.classList.toggle("shownotes",on);
  this.setAttribute("aria-pressed",String(on));
});
$("#btnFs").addEventListener("click",function(){
  try{
    if(document.fullscreenElement){ document.exitFullscreen(); }
    else{ var r=$("#app").requestFullscreen&&$("#app").requestFullscreen(); if(r&&r.catch) r.catch(function(){}); }
  }catch(e){}
});
document.addEventListener("keydown",function(e){
  var t=e.target&&e.target.tagName;
  if(t==="INPUT"||e.ctrlKey||e.metaKey||e.altKey) return;
  if(e.key==="ArrowRight"||e.key==="PageDown"){ e.preventDefault(); show(cur+1); }
  else if(e.key==="ArrowLeft"||e.key==="PageUp"){ e.preventDefault(); show(cur-1); }
  else if(e.key==="f"||e.key==="F"){ $("#btnFs").click(); }
  else if(e.key==="l"||e.key==="L"){ $("#btnNotes").click(); }
});
copy.addEventListener("click",function(e){
  var t=e.target.closest("button"); if(!t) return;
  if(t.hasAttribute("data-rev")){ rev[cur]=true; $("#rev").innerHTML=revealHTML(); return; }
  if(t.hasAttribute("data-w")){ L.widgetAct(t); $("#widget").innerHTML=L.widget(scenes[cur].widget); return; }
  if(t.hasAttribute("data-q")){ qa[+t.getAttribute("data-q")]=+t.getAttribute("data-o"); $("#quiz").innerHTML=quizHTML(); }
});
ctrl.addEventListener("click",function(e){
  var t=e.target.closest("button"); if(!t) return;
  var c=scenes[cur].controls;
  if(t.hasAttribute("data-reset")){ for(var k in c.reset) S[k]=c.reset[k]; }
  else if(t.hasAttribute("data-k")){ S[t.getAttribute("data-k")]=t.getAttribute("data-v"); }
  else return;
  ctrl.innerHTML=ctrlHTML(c); syncOut(); drawStage(!t.hasAttribute("data-reset"));
});
ctrl.addEventListener("input",function(e){
  var k=e.target.getAttribute("data-k"); if(!k) return;
  S[k]=+e.target.value; syncOut(); drawStage(false);
});
var start=0;
try{ var m=/^#s(\d+)$/.exec(location.hash); if(m) start=Math.min(scenes.length-1,+m[1]-1); }catch(e){}
show(Math.max(0,start));
})();
