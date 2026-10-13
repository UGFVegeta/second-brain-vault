#!/usr/bin/env python3
# Nachhilfe quadratische Funktionen: Aufgabenblatt (4 Seiten A4) + Lösungsblatt (gleiches Layout, ausgefüllt)
import math,sys

def fm(v,nd=2):
    if isinstance(v,str): return v
    if abs(v-round(v))<1e-9: return str(int(round(v))).replace('-','−')
    s=('%.*f'%(nd,v)).rstrip('0').rstrip('.')
    return s.replace('.',',').replace('-','−')

def bl(ans,w=40):
    """Lücke: Antwort ist in der Aufgabe unsichtbar, im Lösungsblatt rot"""
    return f'<span class="bl" style="min-width:{w}mm"><em class="a">{ans}</em></span>'

def circ(k): return {'e':'○','m':'◐','s':'●'}[k]

def grid(xmin,xmax,ymin,ymax,u=5.0,curves=(),given=(),pts=(),label=True):
    """SVG-Koordinatensystem, Einheit u mm. curves: nur Lösung; given: immer."""
    W=(xmax-xmin)*u;H=(ymax-ymin)*u
    def X(x): return (x-xmin)*u
    def Y(y): return (ymax-y)*u
    o=[f'<svg class="gr" width="{W+8}mm" height="{H+8}mm" viewBox="-4 -4 {W+8} {H+8}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(xmin,xmax+1):
        o.append(f'<line x1="{X(i)}" y1="0" x2="{X(i)}" y2="{H}" stroke="#bcc3cf" stroke-width="0.25"/>')
    for j in range(ymin,ymax+1):
        o.append(f'<line x1="0" y1="{Y(j)}" x2="{W}" y2="{Y(j)}" stroke="#bcc3cf" stroke-width="0.25"/>')
    ax0=X(0);ay0=Y(0)
    o.append(f'<line x1="0" y1="{ay0}" x2="{W+2}" y2="{ay0}" stroke="#222" stroke-width="0.5"/>')
    o.append(f'<line x1="{ax0}" y1="{H}" x2="{ax0}" y2="-2" stroke="#222" stroke-width="0.5"/>')
    o.append(f'<path d="M{W+2} {ay0} l-1.6 -0.8 v1.6z M{ax0} -2 l-0.8 1.6 h1.6z" fill="#222"/>')
    if label:
        for i in range(xmin,xmax+1):
            if i!=0: o.append(f'<text x="{X(i)}" y="{ay0+3.4}" font-size="2.7" text-anchor="middle" fill="#333">{i}</text>'.replace('>-','>−'))
        for j in range(ymin,ymax+1):
            if j!=0: o.append(f'<text x="{ax0-1}" y="{Y(j)+1}" font-size="2.7" text-anchor="end" fill="#333">{j}</text>'.replace('>-','>−'))
        o.append(f'<text x="{W+1.5}" y="{ay0+3.4}" font-size="3" fill="#333">x</text><text x="{ax0+1.5}" y="1" font-size="3" fill="#333">y</text>')
    def path(a,b,c,col,cls):
        xs=[xmin+i*0.05 for i in range(int((xmax-xmin)/0.05)+1)]
        d=''
        for x in xs:
            y=a*x*x+b*x+c
            if ymin-0.3<=y<=ymax+0.3:
                d+=('M' if not d or d.endswith('Z') else 'L')+f'{X(x):.2f} {Y(y):.2f} '
            else:
                d+='Z' if d and not d.endswith('Z') else ''
        d=d.replace('Z','')  # einfache Variante: Unterbrechungen vermeiden
        o.append(f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="0.7"/>')
    for (a,b,c,col) in given: path(a,b,c,col,'giv')
    for (a,b,c,col) in curves: path(a,b,c,col,'solc')
    for (px,py,t) in pts:
        o.append(f'<g class="solc"><circle cx="{X(px)}" cy="{Y(py)}" r="1" fill="#c0392b"/><text x="{X(px)+1.5}" y="{Y(py)-1.2}" font-size="2.8" fill="#c0392b">{t}</text></g>')
    o.append('</svg>')
    return ''.join(o)

def wtab(f,xs,hide=True):
    r1=''.join(f'<td>{fm(x)}</td>' for x in xs)
    r2=''.join(f'<td><em class="a">{fm(f(x))}</em></td>' for x in xs)
    return f'<table class="wt"><tr><th>x</th>{r1}</tr><tr><th>y</th>{r2}</tr></table>'

# ---------------- Inhalt ----------------
def page_head(n,titel):
    return f'<div class="head"><span class="hl">Quadratische Funktionen</span><span class="ht">{titel}</span><span class="hr">Seite {n} von 4</span></div>'

SPACE={6:11,7:9,10:11,11:13,12:15,13:16,14:10,15:16,16:22}
def task(nr,lvl,text,body='',cls=''):
    space=SPACE.get(nr,0)
    rs=f'<div class="rechne" style="height:{space}mm"></div>' if space else ''
    return f'<div class="task {cls}"><div class="tn"><b>{nr}</b><span class="lv">{circ(lvl)}</span></div><div class="tb"><div class="tt">{text}</div>{body}{rs}</div></div>'

def rows(items,cols=2):
    return f'<div class="rows c{cols}">'+''.join(f'<div class="it">{i}</div>' for i in items)+'</div>'

P=[]
# ---- Seite 1
s=page_head(1,'Normalparabel, Form und Lage')
f1=lambda x:x*x-4; f2=lambda x:-0.5*x*x+2
xs=[-4,-3,-2,-1,0,1,2,3,4]
t1=task(1,'e','Erstelle eine Wertetabelle und zeichne das Schaubild.',
  '<div class="two"><div><div class="fn">a)&nbsp; y = x² − 4</div>'+wtab(f1,xs)+grid(-4,4,-5,5,6.6,curves=[(1,0,-4,'#c0392b')])+
  '</div><div><div class="fn">b)&nbsp; y = −½x² + 2</div>'+wtab(f2,xs)+grid(-4,4,-5,5,6.6,curves=[(-0.5,0,2,'#c0392b')])+'</div></div>')
t2=task(2,'e','Beschreibe die Parabel ohne zu zeichnen: Nach oben oder unten geöffnet? Schmaler oder breiter als die Normalparabel? Scheitelpunkt?',
  '<table class="t2"><tr><th></th><th>Öffnung</th><th>Form</th><th>Scheitelpunkt</th></tr>'+
  ''.join(f'<tr><td>{g}</td><td>{bl(a,26)}</td><td>{bl(b,38)}</td><td>{bl(c,24)}</td></tr>' for g,a,b,c in [
   ('a)&nbsp; y = 2x² − 3','nach oben','schmaler','S(0 | −3)'),
   ('b)&nbsp; y = −¼x² + 2','nach unten','breiter','S(0 | 2)'),
   ('c)&nbsp; y = −3x² − 1','nach unten','schmaler','S(0 | −1)'),
   ('d)&nbsp; y = 0,5x² + 4','nach oben','breiter','S(0 | 4)')])+'</table>')
cp=[(0.5,0,-2,'#2a6fdb'),(-1,0,3,'#2a6fdb'),(2,0,-1,'#2a6fdb')]
def gsmall(c): return grid(-3,3,-3,4,5.6,given=[c],curves=[],label=True)
t3=task(3,'m','Lies Scheitelpunkt und Formfaktor a ab und gib die Funktionsgleichung y = ax² + c an.',
  '<div class="three">'+''.join(f'<div>{gsmall(c)}<div class="ln">S{bl(sp,22)}<br>y = {bl(eq,34)}</div></div>' for c,sp,eq in [
    (cp[0],'(0 | −2)','½x² − 2'),(cp[1],'(0 | 3)','−x² + 3'),(cp[2],'(0 | −1)','2x² − 1')])+'</div>')
s+=t1+t2+t3
P.append(s)
# ---- Seite 2
s=page_head(2,'Scheitelform und Normalform')
t4=task(4,'e','Gib den Scheitelpunkt an und sage, ob die Parabel nach oben oder unten geöffnet ist.',
  rows([f'{g}&nbsp; S{bl(a,24)} {bl(b,20)}' for g,a,b in [
   ('a)&nbsp; y = (x − 3)² + 2','(3 | 2)','nach oben'),('b)&nbsp; y = (x + 1)² − 4','(−1 | −4)','nach oben'),
   ('c)&nbsp; y = −(x − 2)² + 5','(2 | 5)','nach unten'),('d)&nbsp; y = 2(x + 4)² − 1','(−4 | −1)','nach oben')]],2))
t5=task(5,'m','Scheitelform → Normalform: Löse die Klammer mit der binomischen Formel auf.',
  rows([f'{g} = {bl(a,44)}' for g,a in [
   ('a)&nbsp; y = (x − 3)² + 2','x² − 6x + 11'),('b)&nbsp; y = (x + 2)² − 5','x² + 4x − 1'),
   ('c)&nbsp; y = (x − 5)² − 4','x² − 10x + 21'),('d)&nbsp; y = 2(x − 1)² + 3','2x² − 4x + 5')]],2))
t6=task(6,'m','Normalform → Scheitelform (quadratische Ergänzung). Gib den Scheitelpunkt an.',
  '<div class="rows c1">'+''.join(f'<div class="it">{g}&nbsp;&nbsp;= {bl(a,52)}&nbsp;&nbsp; S{bl(sp,22)}</div>' for g,a,sp in [
   ('a)&nbsp; y = x² − 6x + 7','(x − 3)² − 2','(3 | −2)'),('b)&nbsp; y = x² + 4x + 1','(x + 2)² − 3','(−2 | −3)'),
   ('c)&nbsp; y = x² − 2x − 3','(x − 1)² − 4','(1 | −4)'),('d)&nbsp; y = x² − 10x + 23','(x − 5)² − 2','(5 | −2)')])+'</div>'
  +'<div class="hint">Tipp: x² + bx → ergänze (b/2)² und ziehe es wieder ab.</div>')
t7=task(7,'s','Wie Aufgabe 6, aber zuerst den Faktor vor x² ausklammern.',
  '<div class="rows c1">'+''.join(f'<div class="it">{g}&nbsp;&nbsp;= {bl(a,52)}&nbsp;&nbsp; S{bl(sp,22)}</div>' for g,a,sp in [
   ('a)&nbsp; y = 2x² − 4x + 5','2(x − 1)² + 3','(1 | 3)'),('b)&nbsp; y = −x² + 6x − 4','−(x − 3)² + 5','(3 | 5)'),
   ('c)&nbsp; y = ½x² + 2x + 3','½(x + 2)² + 1','(−2 | 1)')])+'</div>')
fg=lambda x:(x-2)**2-1
t8=task(8,'m','Zeichne y = (x − 2)² − 1: Trage zuerst den Scheitelpunkt ein. Gehe dann 1 Einheit nach rechts und 1 hoch, 2 Einheiten nach rechts und 4 hoch, 3 Einheiten nach rechts und 9 hoch; links symmetrisch.',
  '<div class="two"><div>'+grid(-2,6,-3,5,5.4,curves=[(1,-4,3,'#c0392b')],pts=[(2,-1,'S(2|−1)')])+'</div><div class="note">Nullstellen aus dem Graphen:<br>x₁ = '+bl('1',14)+'&nbsp;&nbsp; x₂ = '+bl('3',14)+'<br><br>Bestätige durch Rechnung:<br>(x − 2)² − 1 = 0<br>'+bl('(x − 2)² = 1 → x = 2 ± 1',44)+'</div></div>')
s+=t4+t5+t6+t7+t8
P.append(s)
# ---- Seite 3
s=page_head(3,'Nullstellen und Schnittpunkte')
t9=task(9,'e','Berechne die Nullstellen. Setze y = 0.',
  rows([f'{g}&nbsp;&nbsp; {bl(a,40)}' for g,a in [
   ('a)&nbsp; y = x² − 9','x₁ = 3; x₂ = −3'),('b)&nbsp; y = (x − 2)² − 4','x₁ = 0; x₂ = 4'),
   ('c)&nbsp; y = −½x² + 8','x₁ = 4; x₂ = −4'),('d)&nbsp; y = x² + 3','keine Nullstelle')]],2))
t10=task(10,'m','Berechne die Nullstellen mit der pq-Formel&nbsp; x₁,₂ = −p/2 ± √((p/2)² − q).&nbsp; Wie viele Nullstellen gibt es jeweils?',
  rows([f'{g}&nbsp;&nbsp; {bl(a,40)}' for g,a in [
   ('a)&nbsp; y = x² − 6x + 5','x₁ = 1; x₂ = 5'),('b)&nbsp; y = x² + 2x − 8','x₁ = −4; x₂ = 2'),
   ('c)&nbsp; y = x² − 4x + 4','x = 2 (eine, doppelt)'),('d)&nbsp; y = x² + 2x + 5','keine, (p/2)² − q = −4 &lt; 0'),
   ('e)&nbsp; y = x² − 3x − 4','x₁ = 4; x₂ = −1'),('f)&nbsp; y = x² + 6x + 9','x = −3 (eine, doppelt)')]],2)
  +'<div class="hint">Diskriminante D = (p/2)² − q: D &gt; 0 → zwei, D = 0 → eine, D &lt; 0 → keine Nullstelle.</div>')
t11=task(11,'m','Berechne die Koordinaten der Schnittpunkte von Parabel p und Gerade g. Setze die Terme gleich und berechne die y-Werte.',
  '<div class="rows c1">'
  '<div class="it">a)&nbsp; p: y = x² − 3x + 2&nbsp;&nbsp; g: y = −x + 5<br><span class="sp">Gleichsetzen: '+bl('x² − 3x + 2 = −x + 5 → x² − 2x − 3 = 0',72)+'</span><br><span class="sp">x₁ = '+bl('3',10)+' x₂ = '+bl('−1',10)+'&nbsp;&nbsp; P'+bl('(3 | 2)',22)+' Q'+bl('(−1 | 6)',22)+'</span></div>'
  '<div class="it">b)&nbsp; p: y = x² − 2x − 2&nbsp;&nbsp; g: y = 2x − 6<br><span class="sp">Gleichsetzen: '+bl('x² − 4x + 4 = 0 → (x − 2)² = 0 → x = 2',72)+'</span><br><span class="sp">Wie viele gemeinsame Punkte? '+bl('einen: Berührpunkt B(2 | −2)',60)+'</span></div></div>')
t12=task(12,'s','Gemeinsame Punkte zweier Parabeln.',
  '<div class="rows c1">'
  '<div class="it">a)&nbsp; p₁: y = x² − 3x + 2&nbsp;&nbsp; p₂: y = ¼x² − ¼<br><span class="sp">'+bl('¾x² − 3x + 9/4 = 0 | : ¾ → x² − 4x + 3 = 0 → x₁ = 1; x₂ = 3',100)+'</span><br><span class="sp">Schnittpunkte: P'+bl('(1 | 0)',22)+' Q'+bl('(3 | 2)',22)+'</span></div>'
  '<div class="it">b)&nbsp; p₁: y = x² − 6x + 10&nbsp;&nbsp; p₂: y = x² + 2x − 2<br><span class="sp">'+bl('x² fällt weg: −6x + 10 = 2x − 2 → x = 1,5 → y = 3,25',100)+'</span><br><span class="sp">Warum gibt es nur einen Schnittpunkt? '+bl('Beide haben a = 1, die x²-Terme heben sich auf, es bleibt eine lineare Gleichung.',100)+'</span></div></div>')
s+=t9+t10+t11+t12
P.append(s)
# ---- Seite 4
s=page_head(4,'Gleichung aufstellen, Anwendung, Prüfung')
t13=task(13,'m','Eine Normalparabel y = x² + bx + c geht durch die Punkte P und Q. Setze beide Punkte ein und löse das Gleichungssystem.',
  '<div class="rows c1">'
  '<div class="it">a)&nbsp; P(1 | 2); Q(4 | 5)<br><span class="sp">(I) '+bl('1 + b + c = 2',28)+'&nbsp; (II) '+bl('16 + 4b + c = 5',32)+'&nbsp; → b = '+bl('−4',10)+' c = '+bl('5',10)+'&nbsp; y = '+bl('x² − 4x + 5',30)+'</span></div>'
  '<div class="it">b)&nbsp; P(2 | −3); Q(−1 | 0)<br><span class="sp">(I) '+bl('4 + 2b + c = −3',30)+'&nbsp; (II) '+bl('1 − b + c = 0',30)+'&nbsp; → b = '+bl('−2',10)+' c = '+bl('−3',10)+'&nbsp; y = '+bl('x² − 2x − 3',30)+'</span></div></div>')
t14=task(14,'m','Eine Parabel hat den Scheitelpunkt S und geht durch den Punkt P. Setze in y = a(x − d)² + e ein und berechne a.',
  '<div class="rows c1">'
  '<div class="it">a)&nbsp; S(3 | −2); P(5 | 6)&nbsp;&nbsp; <span class="sp">6 = a·(5 − 3)² − 2 → a = '+bl('2',10)+'&nbsp; y = '+bl('2(x − 3)² − 2',36)+'</span></div>'
  '<div class="it">b)&nbsp; S(−1 | 4); P(1 | −4)&nbsp;&nbsp; <span class="sp">−4 = a·(1 + 1)² + 4 → a = '+bl('−2',10)+'&nbsp; y = '+bl('−2(x + 1)² + 4',36)+'</span></div></div>')
t15=task(15,'s','Kugelstoßen: Die Flugbahn der Kugel wird durch y = −0,05x² + 0,6x + 1,8 beschrieben (x: Weite in m, y: Höhe in m).',
  '<div class="rows c1">'
  '<div class="it">a)&nbsp; In welcher Höhe verlässt die Kugel die Hand? '+bl('x = 0 → y = 1,8 m',34)+'</div>'
  '<div class="it">b)&nbsp; Wie hoch fliegt die Kugel höchstens? Quadratische Ergänzung: '+bl('y = −0,05(x − 6)² + 3,6 → 3,6 m bei x = 6 m',74)+'</div>'
  '<div class="it">c)&nbsp; Wie weit fliegt die Kugel? Setze y = 0: '+bl('x² − 12x − 36 = 0 → x = 6 + √72 ≈ 14,5 m',74)+'</div></div>')
t16=task(16,'s','Prüfungsaufgabe: Gegeben sind die Parabel p: y = x² − 4x − 5 und die Gerade g: y = x − 5.',
  '<div class="rows c1">'
  '<div class="it">a)&nbsp; Berechne die Nullstellen von p. '+bl('x₁ = −1; x₂ = 5',34)+'</div>'
  '<div class="it">b)&nbsp; Bestimme den Scheitelpunkt S von p. '+bl('y = (x − 2)² − 9 → S(2 | −9)',50)+'</div>'
  '<div class="it">c)&nbsp; Berechne die Schnittpunkte von p und g. '+bl('x² − 5x = 0 → P(0 | −5); Q(5 | 0)',60)+'</div>'
  '<div class="it">d)&nbsp; Die Gerade h steht senkrecht auf g (m₁·m₂ = −1) und geht durch S. Bestimme die Gleichung von h. '+bl('m = −1: −9 = −2 + c → c = −7 → y = −x − 7',72)+'</div></div>')
s+=t13+t14+t15+t16
P.append(s)

CSS='''
.rechne{margin-top:2mm;border:.25mm dashed #b8bdc8;border-radius:1.5mm;background-image:linear-gradient(#e3e6ec .2mm,transparent .2mm),linear-gradient(90deg,#e3e6ec .2mm,transparent .2mm);background-size:5mm 5mm}

@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font:11.2pt/1.34 "Helvetica Neue",Helvetica,Arial,sans-serif;color:#1d1d1f;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:9mm 11mm 8mm;position:relative;overflow:hidden;break-after:page}
.page:last-child{break-after:auto}
.head{display:flex;justify-content:space-between;align-items:baseline;border-bottom:.6mm solid #e58a5b;padding-bottom:1.5mm;margin-bottom:2.5mm}
.hl{font-size:8.5pt;color:#7a6a58}.ht{font-size:16pt;font-weight:700}.hr{font-size:8.5pt;color:#7a6a58}
.task{display:flex;gap:2.5mm;margin-bottom:4.2mm;break-inside:avoid}
.tn{flex:none;width:8mm;text-align:center}.tn b{display:block;font-size:15pt;color:#b8461f;line-height:1}.lv{font-size:10pt;color:#7a6a58}
.tb{flex:1;min-width:0}.tt{margin-bottom:1.5mm}
.rows{display:grid;gap:3mm 6mm}.rows.c2{grid-template-columns:1fr 1fr}.rows.c1{grid-template-columns:1fr}
.it{padding:.3mm 0;line-height:1.55}.sp{display:inline-block;margin-top:1mm}
.bl{display:inline-block;border-bottom:.3mm solid #8a8a90;min-height:7.5mm;vertical-align:bottom;padding:0 1mm;line-height:1.1}
.a{visibility:hidden;font-style:normal;color:#c0392b;font-family:"Bradley Hand","Segoe Print","Caveat",cursive;font-weight:600;font-size:13pt}
body.sol .a{visibility:visible}
.giv{}.solc{display:none}body.sol .solc{display:inline}
.two{display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-items:start}
.three{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}
.fn{font-weight:600;margin-bottom:1mm}
.wt{border-collapse:collapse;font-size:10pt;margin-bottom:1.2mm}.wt th,.wt td{border:.25mm solid #888;padding:.5mm 1.4mm;min-width:6.2mm;text-align:center}.wt th{background:#f1ece4}
.t2{border-collapse:collapse;width:100%}.t2 th{text-align:left;font-size:8.5pt;color:#7a6a58;font-weight:600;padding-bottom:1mm}.t2 td{padding:1mm 2mm 1mm 0}
.gr{display:block}
.ln{font-size:9.6pt;margin-top:1mm}
.note{padding-top:3mm}
.hint{font-size:8.6pt;color:#7a6a58;margin-top:1.5mm;font-style:italic}
.top-sol{display:none}
body.sol .sollabel{display:block}
.sollabel{display:none;position:absolute;right:11mm;top:2.5mm;font-size:8pt;color:#c0392b;font-weight:700;letter-spacing:.06em}
'''
def build(sol):
    body=''.join(f'<div class="page">{"<div class=sollabel>LÖSUNG</div>" if sol else ""}{p}</div>' for p in P)
    return f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Quadratische Funktionen</title><style>{CSS}</style></head><body class="{"sol" if sol else ""}">{body}</body></html>'
open('/tmp/nh/aufgaben.html','w',encoding='utf-8').write(build(False))
open('/tmp/nh/loesung.html','w',encoding='utf-8').write(build(True))
print('ok')
