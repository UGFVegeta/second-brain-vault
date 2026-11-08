"""Mathe 7c, Woche 8, Stunde 1: Winkel messen (Mo 09.11.2026, Klassenlehrerstunde, 45 Minuten).

Stunden-HTML mit Folien (bau_woche mit Seitenleiste und Uhr). Blätter kommen aus baue_winkel_messen.py.
Neu: Folien mit Bewegung. Geodreieck legt sich an und dreht sich, von selbst, mit dem Regler oder mit der Maus.
Das Folien-PDF zeigt von diesen Folien den Endzustand (ohne Knöpfe).
Aufruf: python3 baue_stunde_winkel.py
"""
import math
import re
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(HIER.parents[1]))
from mathe_woche_vorlage import bau_woche  # noqa: E402
from baue_winkel_messen import blatt, info, ueberstumpf, geodreieck, GRIECH, P, TEAL, PINK, zug  # noqa: E402

NAME = "Mathe 7c – Woche 8 – 1 Winkel messen"
ZAEHLER = [0]


def eindeutig(s):
    """Jede eingebettete Zeichnung bekommt eigene clipPath-Ids, sonst greifen sie in versteckten Tabs nicht."""
    ZAEHLER[0] += 1
    return re.sub(r'(id="|url\(#)([^")]+)', lambda m: f"{m.group(1)}{m.group(2)}_{ZAEHLER[0]}", s)


def a4(innen):
    return f'<svg class="ganz" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 297">{eindeutig(innen)}</svg>'


def arc_d(r, a1, a2):
    x1, y1 = P(0, 0, r, a1)
    x2, y2 = P(0, 0, r, a2)
    return f"M{x1:.2f} {y1:.2f} A{r} {r} 0 {1 if (a2 - a1) % 360 > 180 else 0} 0 {x2:.2f} {y2:.2f}"


def plakette_svg(klasse, farbe, r):
    return (f'<g class="{klasse}"><circle r="{r}" fill="#fff" stroke="{farbe}" stroke-width="0.6"/>'
            f'<text y="1.15" font-size="3.2" font-weight="700" text-anchor="middle" fill="{farbe}" font-family="Helvetica, Arial, sans-serif"></text></g>')


def buehne(art, methode, alpha):
    """Eine Folie mit Geodreieck. Ohne Skript (PDF) steht der Endzustand da."""
    th = 0 if methode == "markier" else alpha - 180
    box = "-72 -70 150 82" if methode == "markier" else "-72 -68 150 108"
    laenge = 62 if methode == "markier" else 66
    x2, y2 = P(0, 0, laenge, alpha)
    sx, sy = (-1.5, 5.8) if methode == "markier" else (-5.5, -2.6)
    pink2 = art == "zeichnen"
    mx, my = P(0, 0, 16, alpha / 2)
    name = "α" if art == "messen" else f"{alpha}°"
    wert = alpha
    if methode == "markier":
        p1, p2 = P(0, 0, 34, alpha), P(0, 0, 28.4, alpha)
    else:
        p1, p2 = (28.4, 0), (34.6, 0)
    regler = ('<label class="w-dreh">Von Hand drehen <input class="w-reg" type="range" min="0" max="180" step="1" value="0"><b class="w-anz"></b></label>'
              if methode == "dreh" else "")
    svg = (f'<svg class="w-svg" viewBox="{box}" xmlns="http://www.w3.org/2000/svg">'
           f'<g class="w-geo" transform="rotate({-th})">{geodreieck(0, 0, 58, 2.8)}</g>'
           '<line class="w-l1" x1="0" y1="0" x2="74" y2="0" stroke="#111" stroke-width="0.7" stroke-linecap="round"/>'
           f'<line class="w-l2" x1="0" y1="0" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{PINK if pink2 else "#111"}" stroke-width="0.7" stroke-linecap="round"/>'
           f'<path class="w-arc" d="{arc_d(11, 0, alpha)}" fill="none" stroke="{PINK}" stroke-width="0.7"/>'
           f'<text class="w-name" x="{mx:.2f}" y="{my + 1.6:.2f}" font-size="5" font-weight="700" font-style="{"italic" if art == "messen" else "normal"}" text-anchor="middle" fill="{PINK}" font-family="Helvetica, Arial, sans-serif">{name}</text>'
           f'<g class="w-s"><circle r="0.95" fill="#111"/><text x="{sx}" y="{sy}" font-size="5" font-weight="700" text-anchor="middle" font-family="Helvetica, Arial, sans-serif">S</text></g>'
           + plakette_svg("w-p1", PINK, 3.6) + plakette_svg("w-p2", "#777", 3.3) + '</svg>')
    svg = svg.replace('<g class="w-p1"><circle', f'<g class="w-p1" transform="translate({p1[0]:.2f} {p1[1]:.2f})"><circle', 1)
    svg = svg.replace('<g class="w-p2"><circle', f'<g class="w-p2" transform="translate({p2[0]:.2f} {p2[1]:.2f})"><circle', 1)
    teile = svg.split('text-anchor="middle" fill="' + PINK + '" font-family="Helvetica, Arial, sans-serif"></text>')
    if len(teile) == 2:
        svg = teile[0] + f'text-anchor="middle" fill="{PINK}" font-family="Helvetica, Arial, sans-serif">{wert}</text>' + teile[1]
    grau = 'text-anchor="middle" fill="#777" font-family="Helvetica, Arial, sans-serif"></text>'
    svg = svg.replace(grau, grau.replace("></text>", f">{180 - wert}</text>"))
    if art == "zeichnen":
        svg = svg.replace(f">{180 - wert}</text>", "></text>").replace('<g class="w-p2"', '<g class="w-p2" style="display:none"', 1)
    return (f'<div class="w w-g" data-art="{art}" data-met="{methode}" data-alpha="{alpha}">{svg}<p class="w-cap"></p>'
            '<div class="w-ctrl"><button class="w-zur">◀ Schritt</button><button class="w-vor pri">Schritt ▶</button>'
            f'<span class="w-nr"></span><button class="w-play">Abspielen</button><button class="w-neu">Neuer Winkel</button>{regler}</div></div>')


def arten_folie():
    a = 130
    x2, y2 = P(0, 0, 40, a)
    knoepfe = "".join(f'<button data-a="{g}">{t}</button>' for g, t in ((45, "spitz"), (90, "recht"), (130, "stumpf"), (180, "gestreckt"), (240, "überstumpf"), (360, "voll")))
    return (f'<div class="w w-a"><svg class="w-svg" viewBox="-60 -46 120 72" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="0" y1="0" x2="44" y2="0" stroke="#111" stroke-width="0.7" stroke-linecap="round"/>'
            f'<line class="a-l" x1="0" y1="0" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#111" stroke-width="0.7" stroke-linecap="round"/>'
            f'<path class="a-arc" d="{arc_d(10, 0, a)}" fill="none" stroke="{TEAL}" stroke-width="0.8"/>'
            f'<circle class="a-pkt" cx="0" cy="0" r="0.8" fill="{TEAL}" style="display:none"/><circle r="0.95" fill="#111"/></svg>'
            f'<p class="w-cap a-cap">{a}°: stumpf</p>'
            f'<div class="w-ctrl">{knoepfe}<button class="a-play pri">Abspielen</button>'
            f'<label class="w-dreh">Von Hand <input class="a-reg" type="range" min="5" max="360" step="1" value="{a}"></label></div></div>')


def griech_folie():
    zellen = ""
    for name, _, d in GRIECH:
        zellen += (f'<div class="gr-z"><svg viewBox="0 0 10 15" xmlns="http://www.w3.org/2000/svg">{zug(0, 0, d, "#111", 0.55)}</svg><b>{name}</b></div>')
    return (f'<div class="w w-gr"><div class="gr-reihe">{zellen}</div>'
            '<p class="w-cap">Winkel heißen so. Hinten auf dem Info-Blatt: Jeder Buchstabe mindestens 10-mal.</p>'
            '<div class="w-ctrl"><button class="g-play pri">Vorschreiben</button></div></div>')


def ueberstumpf_folie(messen):
    return (f'<svg class="ueber" viewBox="12 9 186 39" xmlns="http://www.w3.org/2000/svg">{ueberstumpf(0, messen)}</svg>')


AUFGABE = ('<ol class="auftrag"><li>Info-Blatt daneben legen.</li><li>Aufgabenblatt der Reihe nach, Nr. 1 bis Nr. 9.</li>'
           "<li>Geodreieck genau anlegen: 0 auf S.</li><li>Zu kurz? Schenkel verlängern.</li></ol>"
           '<p class="legende">○ leicht &nbsp; ◐ mittel &nbsp; ● schwer: Du musst nicht alles schaffen.</p>')

B_L, B_F = blatt(False), blatt(True)
IV, IH = info()
FOLIEN = [
    ("Welche Winkelart?", arten_folie()),
    ("Griechische Buchstaben", griech_folie()),
    ("Info-Blatt hinten: schreiben üben", a4(IH)),
    ("Winkel messen: Markier-Methode", buehne("messen", "markier", 50)),
    ("Winkel messen: Dreh-Methode", buehne("messen", "dreh", 50)),
    ("Überstumpfe Winkel messen", ueberstumpf_folie(True)),
    ("Winkel zeichnen: Markier-Methode", buehne("zeichnen", "markier", 60)),
    ("Winkel zeichnen: Dreh-Methode", buehne("zeichnen", "dreh", 60)),
    ("Überstumpfe Winkel zeichnen", ueberstumpf_folie(False)),
    ("Aufgabe", AUFGABE),
    ("Aufgabenblatt Seite 1", a4(B_L[0])),
    ("Aufgabenblatt Seite 1: ausgefüllt", a4(B_F[0])),
    ("Aufgabenblatt Seite 2", a4(B_L[1])),
    ("Aufgabenblatt Seite 2: ausgefüllt", a4(B_F[1])),
    ("Info-Blatt vorne", a4(IV)),
]
QUER = {t for t, _ in FOLIEN[:2] + FOLIEN[3:10]}
LEISTE = ([("Einstieg", "Winkelarten", None), ("Einstieg", "Buchstaben", None), ("Einstieg", "Buchstaben", None)]
          + [("Messen", "Markier-Methode", None), ("Messen", "Dreh-Methode", None), ("Messen", "Überstumpf", None)]
          + [("Zeichnen", "Markier-Methode", None), ("Zeichnen", "Dreh-Methode", None), ("Zeichnen", "Überstumpf", None)]
          + [("Üben", "Aufgabe", 18)] + [("Üben", "Blatt Seite 1", None)] * 2 + [("Üben", "Blatt Seite 2", None)] * 2
          + [("Reserve", "Info-Blatt vorne", None)])

SCHRITTE = [
    ("", "Winkelarten", 4, "Abspielen: Der Schenkel dreht sich, die Klasse ruft die Art. Mit dem Regler nachstellen.", [1]),
    ("", "Griechische Buchstaben", 5, "Info-Blatt austeilen. Vorschreiben zeigen, dann hinten auf dem Blatt nachspuren und mindestens 10-mal schreiben.", [2, 3]),
    ("", "Messen", 8, "Beide Methoden Schritt für Schritt zeigen. Neuer Winkel: Klasse sagt vorher die Art und die Zahl. Überstumpf zum Schluss.", [4, 5, 6]),
    ("", "Zeichnen", 7, "Beide Methoden zeigen, wieder gegen den Uhrzeigersinn. Bei der Dreh-Methode mit dem Regler oder der Maus drehen.", [7, 8, 9]),
    ("", "Aufgabenblatt", 18, "Uhr 18 Minuten. Der Reihe nach, Info-Blatt daneben.", [10]),
    ("", "Besprechen", 3, "Ausgefülltes Blatt zeigen. Rest kann Hausaufgabe werden.", [12, 14]),
]
assert sum(s[2] for s in SCHRITTE) == 45

EXTRA = """<style>
svg.ganz{display:block;width:100%;height:auto}
svg.ueber{display:block;width:100%;height:auto;margin-top:18px}
.w{display:flex;flex-direction:column;height:640px}
.w-svg{display:block;width:100%;flex:1;min-height:0}
.w-cap{font-size:26px;font-weight:700;text-align:center;margin:8px 0 10px;min-height:36px}
.w-cap.ergebnis{color:#d6006e;font-size:32px}
.w-ctrl{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;font-size:16px}
.w-ctrl button{font:inherit;font-weight:600;border:1px solid #cfd6df;background:#fff;border-radius:18px;padding:7px 16px;cursor:pointer;color:#1b1b1b}
.w-ctrl button.pri{background:#0f7c80;border-color:#0f7c80;color:#fff}
.w-nr{color:#66798e;min-width:48px;text-align:center}
.w-dreh{display:flex;align-items:center;gap:8px;font-weight:600}.w-dreh input{width:200px}.w-anz{min-width:44px}
.w-geo{touch-action:none}
.gr-reihe{flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:12px;align-items:center}
.gr-z{display:flex;flex-direction:column;align-items:center;gap:10px;font-size:30px}.gr-z svg{width:150px;height:225px}
.auftrag{font-size:30px;line-height:1.7;margin:30px 0 0 10px}.legende{font-size:24px;margin:24px 0 0 10px}
@media print{.w-ctrl,.w-cap:empty{display:none}.w{height:610px}}
</style>"""

JS_BUEHNE = r"""<script>(()=>{
const P=(r,a)=>{const t=a*Math.PI/180;return [r*Math.cos(t),-r*Math.sin(t)]};
const bogen=(r,a1,a2)=>{const [x1,y1]=P(r,a1),[x2,y2]=P(r,a2);return `M${x1} ${y1} A${r} ${r} 0 ${((a2-a1)%360)>180?1:0} 0 ${x2} ${y2}`};
const artVon=a=>a<90?'spitz':a===90?'recht':a<180?'stumpf':a===180?'gestreckt':a<360?'überstumpf':'Vollwinkel';
const gross=s=>s[0].toUpperCase()+s.slice(1);
const warte=ms=>new Promise(r=>setTimeout(r,ms));
const still=w=>{w.addEventListener('click',e=>{e.stopPropagation();const b=e.target.closest('button');if(b)b.blur()})};

function buehne(w){
  still(w);
  const q=s=>w.querySelector(s), geo=q('.w-geo'), l1=q('.w-l1'), l2=q('.w-l2'), arcE=q('.w-arc'), nameE=q('.w-name'), sE=q('.w-s'), p1=q('.w-p1'), p2=q('.w-p2'),
    cap=q('.w-cap'), nr=q('.w-nr'), reg=q('.w-reg'), anz=q('.w-anz'), svg=q('.w-svg');
  const art=w.dataset.art, met=w.dataset.met, dreh=met==='dreh', messen=art==='messen', LEN=dreh?66:62;
  const POOL=messen?[38,47,62,75,103,116,128,141,152,34]:[40,55,60,75,110,125,140];
  let alpha=+w.dataset.alpha, th=dreh?-180:0, gO=0, tok=0, spiel=0, step=0, schritte=[], zeigP=false;
  const zeig=(e,b)=>e.style.display=b?'':'none';
  function bau(){
    const a=alpha,b=180-a,k=artVon(a),ANL='0 genau auf S, lange Kante auf den ersten Schenkel.';
    const s0=dreh?-180:0, sz=dreh?a-180:0;
    if(messen){
      const fest={l2:1,arc:1,s:1,name:'α'};
      schritte=[{...fest,c:'Wie groß ist der Winkel α?',geo:0,th:s0},{...fest,c:'Art schätzen: '+k+'.',geo:0,th:s0},{...fest,c:ANL,geo:1,th:s0}];
      if(dreh) schritte.push({...fest,c:'Drehen, bis die lange Kante auf dem zweiten Schenkel liegt.',geo:1,th:sz});
      const ab=(dreh?'Am ersten':'Am zweiten')+` Schenkel ablesen: ${a} und ${b}. ${gross(k)}, also ${a}.`;
      schritte.push({...fest,c:ab,geo:1,th:sz,pl:2},{...fest,c:`α = ${a}°`,geo:1,th:sz,pl:2,erg:1});
    }else{
      schritte=[{c:'Ersten Schenkel zeichnen.',geo:0,th:s0},{s:1,c:'Scheitel S markieren.',geo:0,th:s0},{s:1,c:'0 genau auf S, lange Kante auf den Schenkel.',geo:1,th:s0}];
      if(dreh){
        schritte.push({s:1,c:`Drehen, bis der Schenkel auf ${a}° liegt.`,geo:1,th:sz,pl:1},{s:1,l2:1,c:'An der langen Kante entlang zeichnen.',geo:1,th:sz,pl:1});
      }else{
        schritte.push({s:1,c:`Bei ${a}° einen Punkt setzen.`,geo:1,th:0,pl:1},{s:1,l2:1,c:'Geodreieck weg, Punkt mit S verbinden.',geo:0,th:0});
      }
      schritte.push({s:1,l2:1,arc:1,name:a+'°',c:`Bogen zeichnen, ${a}° eintragen.`,geo:0,th:sz,erg:1});
    }
  }
  function lage(){
    const [x,y]=P(LEN,alpha); l2.setAttribute('x2',x); l2.setAttribute('y2',y);
    arcE.setAttribute('d',bogen(11,0,alpha));
    const [mx,my]=P(16,alpha/2); nameE.setAttribute('x',mx); nameE.setAttribute('y',my+1.6);
  }
  function male(){
    geo.setAttribute('transform',`rotate(${-th})`); geo.style.opacity=gO; geo.style.pointerEvents=gO>.5?'auto':'none';
    if(dreh){ const v=Math.round(th+180); if(reg) reg.value=v; if(anz) anz.textContent=v+'°';
      p1.setAttribute('transform','translate(28.4 0)'); p2.setAttribute('transform','translate(34.6 0)');
      p1.querySelector('text').textContent=v; p2.querySelector('text').textContent=180-v;
    }else{ const [a,b]=P(34,alpha),[c,d]=P(28.4,alpha); p1.setAttribute('transform',`translate(${a} ${b}) `); p2.setAttribute('transform',`translate(${c} ${d})`);
      p1.querySelector('text').textContent=alpha; p2.querySelector('text').textContent=180-alpha; }
  }
  function zu(zTh,zO,dauer){
    const id=++tok, t0=performance.now(), th0=th, o0=gO;
    return new Promise(res=>{ const f=n=>{ if(id!==tok) return res(); let p=Math.min(1,(n-t0)/dauer); const e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
      th=th0+(zTh-th0)*e; gO=o0+(zO-o0)*e; male(); p<1?requestAnimationFrame(f):res(); }; requestAnimationFrame(f); });
  }
  async function geh(n,sofort){
    step=Math.max(0,Math.min(schritte.length-1,n));
    const s=schritte[step];
    zeig(l1,1); zeig(l2,!!s.l2); zeig(arcE,!!s.arc); zeig(nameE,!!s.name); if(s.name) nameE.textContent=s.name; zeig(sE,!!s.s);
    zeig(p1,!!s.pl); zeig(p2,s.pl===2);
    cap.textContent=s.c; cap.classList.toggle('ergebnis',!!s.erg); nr.textContent=(step+1)+' / '+schritte.length;
    const d=sofort?0:Math.max(350,Math.abs(s.th-th)*33);
    if(sofort){ tok++; th=s.th; gO=s.geo; male(); return; }
    await zu(s.th,s.geo,d);
  }
  bau(); lage(); geh(0,true);
  q('.w-vor').onclick=()=>{spiel++;geh(step+1)}; q('.w-zur').onclick=()=>{spiel++;geh(step-1)};
  q('.w-neu').onclick=()=>{spiel++;let n;do{n=POOL[Math.floor(Math.random()*POOL.length)]}while(n===alpha);alpha=n;bau();lage();geh(0,true)};
  q('.w-play').onclick=async()=>{const id=++spiel;for(let k=step===schritte.length-1?0:step;k<schritte.length;k++){await geh(k);if(id!==spiel)return;await warte(1700);if(id!==spiel)return;}};
  if(dreh){
    const setz=v=>{spiel++;tok++;th=Math.max(-180,Math.min(0,v));if(gO<.5)gO=1;male()};
    reg.addEventListener('input',()=>setz(+reg.value-180)); reg.addEventListener('change',()=>reg.blur());
    const winkelAn=e=>{const pt=new DOMPoint(e.clientX,e.clientY).matrixTransform(svg.getScreenCTM().inverse());return Math.atan2(-pt.y,pt.x)*180/Math.PI};
    let alt=null; geo.style.cursor='grab';
    geo.addEventListener('pointerdown',e=>{alt=winkelAn(e);geo.setPointerCapture(e.pointerId);geo.style.cursor='grabbing';e.preventDefault()});
    geo.addEventListener('pointermove',e=>{if(alt===null)return;const n=winkelAn(e);let d=n-alt;if(d>180)d-=360;if(d<-180)d+=360;alt=n;setz(th+d)});
    const los=()=>{alt=null;geo.style.cursor='grab'}; geo.addEventListener('pointerup',los); geo.addEventListener('pointercancel',los);
  }
}

function arten(w){
  still(w);
  const q=s=>w.querySelector(s), l=q('.a-l'), arcE=q('.a-arc'), pkt=q('.a-pkt'), cap=q('.a-cap'), reg=q('.a-reg');
  let a=+reg.value, tok=0, spiel=0;
  function male(){
    const g=Math.round(a), [x,y]=P(40,g); l.setAttribute('x2',x); l.setAttribute('y2',y);
    const recht=g===90, r=recht?7:10;
    arcE.setAttribute('d',g>=360?`M10 0 A10 10 0 1 0 -10 0 A10 10 0 1 0 10 0`:bogen(r,0,g));
    zeig2(pkt,recht); if(recht){const [px,py]=P(3.4,45);pkt.setAttribute('cx',px);pkt.setAttribute('cy',py)}
    cap.textContent=g+'°: '+artVon(g); reg.value=g;
  }
  const zeig2=(e,b)=>e.style.display=b?'':'none';
  function zu(z){ const id=++tok,t0=performance.now(),a0=a,d=Math.max(350,Math.abs(z-a0)*14);
    return new Promise(res=>{const f=n=>{if(id!==tok)return res();const p=Math.min(1,(n-t0)/d);a=a0+(z-a0)*p;male();p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)}); }
  w.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{spiel++;zu(+b.dataset.a)});
  reg.addEventListener('input',()=>{spiel++;tok++;a=+reg.value;male()}); reg.addEventListener('change',()=>reg.blur());
  q('.a-play').onclick=async()=>{const id=++spiel;a=5;male();for(const z of [45,90,130,180,240,360]){await zu(z);if(id!==spiel)return;await warte(1200);if(id!==spiel)return}};
  male();
}

function griech(w){
  still(w);
  const pfade=[...w.querySelectorAll('path')];
  pfade.forEach(p=>p.setAttribute('pathLength','1'));
  let spiel=0;
  w.querySelector('.g-play').onclick=async()=>{
    const id=++spiel;
    pfade.forEach(p=>{p.style.transition='none';p.style.strokeDasharray='1 1';p.style.strokeDashoffset='1'});
    for(const p of pfade){ if(id!==spiel)return; p.getBoundingClientRect(); p.style.transition='stroke-dashoffset 1.6s ease-in-out'; p.style.strokeDashoffset='0'; await warte(1750); }
  };
}
document.querySelectorAll('.w-g').forEach(buehne);
document.querySelectorAll('.w-a').forEach(arten);
document.querySelectorAll('.w-gr').forEach(griech);
})();</script>"""


def box(t, h):
    return f'<div class="box"><h3>{t}</h3>{h}</div>'


def main():
    vb = [("Drucken", "Info-Blatt und Aufgabenblatt je einmal pro Schüler, jeweils doppelseitig und in Originalgröße (100 %), sonst stimmen die Winkel nicht. Lösung einmal für dich."),
          ("Mitbringen", "Geodreieck und spitzer Bleistift, Schüler auch. Kleber fürs Heft."),
          ("Digital", "Diese HTML am MacBook, Folien vom MacBook aus zeigen: Nur hier bewegt sich das Geodreieck. Das Folien-PDF fürs iPad zeigt den Endzustand."),
          ("Raum", "Klassenlehrerstunde, 45 Minuten.")]
    merk = box("Info-Blatt ins Merkheft einkleben (Vorderseite)", a4(IV)) + box("Rückseite", a4(IH))
    tafel = box("Kein eigener Anschrieb", "<p>Die Schritte laufen auf den Folien. Eingeklebt wird das Info-Blatt (Tab Merkheft).</p>")
    loes = box("Aufgabenblatt Seite 1, ausgefüllt", a4(B_F[0])) + box("Aufgabenblatt Seite 2, ausgefüllt", a4(B_F[1]))
    ziel = HIER / f"{NAME}.html"
    bau_woche(ziel, "Woche 8, Stunde 1: Winkel messen", "Klasse 7c, Mathematik, Mo 09.11.2026, Klassenlehrerstunde (45 Minuten)",
              vb, SCHRITTE, FOLIEN, tafel=tafel, merkheft=merk, loesungen=loes, extra_css=EXTRA, verlauf="Die Stunde", leiste=LEISTE, quer=QUER)
    t = ziel.read_text(encoding="utf-8")
    assert t.count("</body></html>") == 1
    ziel.write_text(t.replace("</body></html>", JS_BUEHNE + "</body></html>"), encoding="utf-8")


if __name__ == "__main__":
    main()
