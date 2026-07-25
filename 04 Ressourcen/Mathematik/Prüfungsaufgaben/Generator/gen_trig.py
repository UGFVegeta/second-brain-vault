# -*- coding: utf-8 -*-
# Erzeugt ALLE 26 Trigonometrie-Figuren: PNG (für .md) + Inline-SVG (für die HTML-Karten).
# Konventionen (Juli 2026, nach Oskars Feedback):
#  - Grün gefüllt ist ausschließlich die GESUCHTE Fläche.
#  - Flächen heißen A mit Index, z. B. A[BGC] → "A" + tiefgestellt "BGC".
#  - Winkelzahlen stehen IM Winkel; wenn der Winkel zu klein ist, zeigt eine
#    Führungslinie in den Winkel und die Zahl steht an ihrem Ende.
# Nach dem Lauf patcht das Skript Figur + gesucht-Zeile aller Karten in
# "Trigonometrie Aufgabenpool.html" (Lösungen bleiben unangetastet) und setzt
# die A-Notation in den Lösungstexten (HTML). Danach: build_exam.py laufen lassen.
import math, os, io, re
from PIL import Image, ImageDraw, ImageFont

SS = 3
W0, H0 = 1180, 740
W, H = W0*SS, H0*SS

OUT   = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben/Bilder"

BLUE  = (38, 103, 139)
FILL  = (216, 235, 205)
RED   = (197, 42, 42)
GREEN = (95, 170, 70)
BLACK = (25, 25, 25)
BORDER= (208, 214, 220)

SVG_BLUE="#2e6e8e"; SVG_GREEN="#9ccc79"; SVG_BLACK="#1a1a1a"; SVG_RED="#c0392b"

FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FI = "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf"

def font(path, size): return ImageFont.truetype(path, int(size*SS))
F_VERT = font(FB, 30)
F_SIDE = font(FB, 26)
F_ANG  = font(FB, 24)
F_ANG_SUB = font(FB, 17)
F_GES  = font(FI, 27)
F_GES_SUB = font(FI, 19)

# ---- Rich-Text: '₂' und '[...]' werden tiefgestellt ----
def rich_parts(s, fnt, subfnt):
    parts=[]; i=0
    while i < len(s):
        ch=s[i]
        if ch=='₂':
            parts.append(('2', subfnt, True)); i+=1
        elif ch=='[':
            j=s.index(']', i)
            for c in s[i+1:j]: parts.append((c, subfnt, True))
            i=j+1
        else:
            parts.append((ch, fnt, False)); i+=1
    return parts

def rich_width(d, s, fnt, subfnt):
    return sum(d.textlength(c, font=f) for c,f,_ in rich_parts(s, fnt, subfnt))

def rich_text(d, x, y, s, fnt, subfnt, color, anchor="lm"):
    parts=rich_parts(s, fnt, subfnt)
    widths=[d.textlength(c, font=f) for c,f,_ in parts]
    total=sum(widths)
    cx = x - (total/2 if anchor[0]=='m' else 0)
    for (c,f,sub),w in zip(parts, widths):
        dy = fnt.size*0.24 if sub else 0
        d.text((cx, y+dy), c, font=f, fill=color, anchor="lm")
        cx += w

def svg_rich(s, size, subsize):
    # '[...]' → tiefgestellte tspans; '₂' bleibt Unicode
    out=""; i=0
    while i < len(s):
        ch=s[i]
        if ch=='[':
            j=s.index(']', i)
            out+=f'<tspan font-size="{subsize}" dy="4">{s[i+1:j]}</tspan><tspan dy="-4"> </tspan>'
            i=j+1
        else:
            out+=ch; i+=1
    return out

def newcanvas():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([6*SS,6*SS,W-6*SS,H-6*SS], radius=22*SS, outline=BORDER, width=2*SS)
    return img, d

class Fit:
    def __init__(self, pts, area=(150,70,880,500)):
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        self.minx,self.maxx=min(xs),max(xs)
        self.miny,self.maxy=min(ys),max(ys)
        bw=self.maxx-self.minx or 1; bh=self.maxy-self.miny or 1
        ax0,atop,aw,ah=area
        sc=min(aw/bw, ah/bh)*0.86
        self.sc=sc
        used_w=bw*sc; used_h=bh*sc
        self.offx=(ax0+(aw-used_w)/2)
        self.offy_bottom=(atop+(ah+used_h)/2)
    def __call__(self,p):
        x=(self.offx+(p[0]-self.minx)*self.sc)*SS
        y=(self.offy_bottom-(p[1]-self.miny)*self.sc)*SS
        return (x,y)

def centroid(pts):
    return (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))

def unit(dx,dy):
    L=math.hypot(dx,dy) or 1; return (dx/L,dy/L)

def _arc_geom(vx,vy,ax,ay,bx,by):
    a1=math.degrees(math.atan2(ay-vy, ax-vx))
    a2=math.degrees(math.atan2(by-vy, bx-vx))
    dd=(a2-a1)%360
    if dd<=180: return a1,a2,dd
    return a2,a1,360-dd

SYMBOLIC = set("αβγδε")

class Dual:
    """Zeichnet dieselbe Figur als PNG (für die .md) und als Inline-SVG (für die HTML-Karte)."""
    def __init__(self, pts, maxw=320, maxh=230):
        self.P = Fit(pts)
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        self.minx=min(xs); self.miny=min(ys)
        bw=(max(xs)-self.minx) or 1; bh=(max(ys)-self.miny) or 1
        self.sc=min(maxw/bw, maxh/bh)
        self.SW=448; self.SH=int(bh*self.sc+128)
        self.soffx=(self.SW-bw*self.sc)/2
        self.img, self.d = newcanvas()
        self.el=[]
        self.vaway={}   # Punkt → 'away'-Punkt der Eckbeschriftung (für Kollisionsvermeidung)
    def Q(self,p):
        return (self.soffx+(p[0]-self.minx)*self.sc, self.SH-64-(p[1]-self.miny)*self.sc)
    # ---------- SVG-Primitive ----------
    def _sline(self,a,b,color,w,dash=False):
        x1,y1=self.Q(a); x2,y2=self.Q(b)
        dd=' stroke-dasharray="10 7"' if dash else ''
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{dd}/>')
    def _stext(self,x,y,s,size=17,color=SVG_BLACK,bold=False,italic=False):
        fw="700" if bold else "400"; fs="italic" if italic else "normal"
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-style="{fs}" font-weight="{fw}" fill="{color}" text-anchor="middle" dominant-baseline="central">{s}</text>')
    # ---------- Figur-Bausteine ----------
    def shape(self, pts, fill=True):
        pp=[self.P(p) for p in pts]
        if fill:
            self.d.polygon(pp, fill=FILL, outline=None)
        self.d.line(pp+[pp[0]], fill=BLUE, width=int(3*SS), joint="curve")
        if fill:
            sp=" ".join(f"{self.Q(p)[0]:.1f},{self.Q(p)[1]:.1f}" for p in pts)
            self.el.append(f'<polygon points="{sp}" fill="{SVG_GREEN}" fill-opacity="0.3" stroke="none"/>')
        for a,b in zip(pts,pts[1:]+[pts[0]]): self._sline(a,b,SVG_BLUE,2.6)
    def line(self,a,b):
        self.d.line([self.P(a),self.P(b)], fill=BLUE, width=int(3*SS))
        self._sline(a,b,SVG_BLUE,2.6)
    def dashed(self,a,b):
        x1,y1=self.P(a); x2,y2=self.P(b); L=math.hypot(x2-x1,y2-y1)
        ux,uy=(x2-x1)/L,(y2-y1)/L; t=0
        while t<L:
            s=min(14*SS, L-t)
            self.d.line([(x1+ux*t,y1+uy*t),(x1+ux*(t+s),y1+uy*(t+s))], fill=BLACK, width=int(2*SS))
            t+=24*SS
        self._sline(a,b,SVG_BLACK,2,dash=True)
    def vlabel(self,p,text,away):
        self.vaway[(round(p[0],3),round(p[1],3))]=away
        px,py=self.P(p); cx,cy=self.P(away); ux,uy=unit(px-cx,py-cy)
        self.d.text((px+ux*30*SS, py+uy*30*SS), text, font=F_VERT, fill=BLACK, anchor="mm")
        qx,qy=self.Q(p); qcx,qcy=self.Q(away); ux,uy=unit(qx-qcx,qy-qcy)
        self._stext(qx+ux*20,qy+uy*20,text,18,SVG_BLACK,bold=True)
    def sidelabel(self,a,b,text,away,off=34,soff=24,red=False,t=0.5):
        # Label steht senkrecht zur Strecke (Normale), auf der von 'away' abgewandten Seite –
        # so berührt der Text nie die Linie. t = Position entlang der Strecke (0…1).
        col = RED if red else BLACK; scol = SVG_RED if red else SVG_BLACK
        ax,ay=self.P(a); bx,by=self.P(b); mx,my=ax+(bx-ax)*t, ay+(by-ay)*t
        ux,uy=unit(bx-ax,by-ay); nx,ny=-uy,ux
        cx,cy=self.P(away)
        if (mx-cx)*nx+(my-cy)*ny < 0: nx,ny=-nx,-ny
        tw=self.d.textlength(text, font=F_SIDE)
        need=abs(nx)*tw/2 + abs(ny)*13*SS + 10*SS
        o=max(off*SS, need)
        self.d.text((mx+nx*o, my+ny*o), text, font=F_SIDE, fill=col, anchor="mm")
        ax,ay=self.Q(a); bx,by=self.Q(b); mx,my=ax+(bx-ax)*t, ay+(by-ay)*t
        ux,uy=unit(bx-ax,by-ay); nx,ny=-uy,ux
        cx,cy=self.Q(away)
        if (mx-cx)*nx+(my-cy)*ny < 0: nx,ny=-nx,-ny
        tw=0.6*17*len(text)
        need=abs(nx)*tw/2 + abs(ny)*9 + 8
        o=max(soff, need)
        self._stext(mx+nx*o,my+ny*o,text,17,scol,italic=red)
    def angle(self,V,A,B,label,r=40,out=False,distfac=1.0,fscale=1.0):
        # Zahl NAH am Scheitel im Winkel (knapp hinter dem Bogen), wenn sie
        # zwischen die Schenkel passt. Sonst – oder mit out=True erzwungen –
        # Zahl AUSSERHALB der Figur, Führungslinie zeigt in den Winkel.
        red = any(ch in SYMBOLIC for ch in label)
        # ---- PNG ----
        vx,vy=self.P(V); ax,ay=self.P(A); bx,by=self.P(B)
        start,_,span=_arc_geom(vx,vy,ax,ay,bx,by)
        rr=r*SS; pad=6*SS
        self.d.arc([vx-rr,vy-rr,vx+rr,vy+rr], start, start+span, fill=RED, width=int(2.4*SS))
        mid=math.radians(start+span/2)
        col = RED if red else BLACK
        # Wie im Mathebuch: Zahl mittig im Winkel, normale Größe, fester Abstand.
        dl=1.7*rr
        rich_text(self.d, vx+math.cos(mid)*dl, vy+math.sin(mid)*dl, label, F_ANG, F_ANG_SUB, col, anchor="mm")
        # ---- SVG ----
        vx,vy=self.Q(V); ax,ay=self.Q(A); bx,by=self.Q(B)
        start,_,span=_arc_geom(vx,vy,ax,ay,bx,by)
        p1=(vx+math.cos(math.radians(start))*r, vy+math.sin(math.radians(start))*r)
        p2=(vx+math.cos(math.radians(start+span))*r, vy+math.sin(math.radians(start+span))*r)
        scol=SVG_RED if red else SVG_BLACK
        self.el.append(f'<path d="M {p1[0]:.1f} {p1[1]:.1f} A {r} {r} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{scol}" stroke-width="1.7"/>')
        mid=math.radians(start+span/2)
        dl=1.7*r
        self._stext(vx+math.cos(mid)*dl, vy+math.sin(mid)*dl, label, 17, scol, bold=red, italic=red)
    def rang(self,V,A,B):
        # PNG: Quadrat + Punkt
        vx,vy=self.P(V); ax,ay=self.P(A); bx,by=self.P(B)
        u1=unit(ax-vx,ay-vy); u2=unit(bx-vx,by-vy)
        s=min(0.275*math.hypot(ax-vx,ay-vy), 26*SS)
        p1=(vx+u1[0]*s, vy+u1[1]*s); p3=(vx+u2[0]*s, vy+u2[1]*s)
        p2=(p1[0]+u2[0]*s, p1[1]+u2[1]*s)
        self.d.line([p1,p2,p3], fill=BLUE, width=int(2*SS))
        cx=vx+(u1[0]+u2[0])*s*0.5; cy=vy+(u1[1]+u2[1])*s*0.5
        self.d.ellipse([cx-2.6*SS,cy-2.6*SS,cx+2.6*SS,cy+2.6*SS], fill=BLUE)
        # SVG: Bogen + Punkt
        vx,vy=self.Q(V); ax,ay=self.Q(A); bx,by=self.Q(B)
        start,_,span=_arc_geom(vx,vy,ax,ay,bx,by)
        r=20
        p1=(vx+math.cos(math.radians(start))*r, vy+math.sin(math.radians(start))*r)
        p2=(vx+math.cos(math.radians(start+span))*r, vy+math.sin(math.radians(start+span))*r)
        self.el.append(f'<path d="M {p1[0]:.1f} {p1[1]:.1f} A {r} {r} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{SVG_BLACK}" stroke-width="1.7"/>')
        mid=math.radians(start+span/2)
        self.el.append(f'<circle cx="{vx+math.cos(mid)*r*0.62:.1f}" cy="{vy+math.sin(mid)*r*0.62:.1f}" r="2.4" fill="{SVG_BLACK}"/>')
    def ticks(self,a,b,n=1):
        ax,ay=self.P(a); bx,by=self.P(b); mx,my=(ax+bx)/2,(ay+by)/2
        ux,uy=unit(bx-ax,by-ay); px,py=-uy,ux
        base=-(n-1)/2.0
        for i in range(n):
            c=( mx+ux*(base+i)*7*SS, my+uy*(base+i)*7*SS )
            self.d.line([(c[0]-px*9*SS, c[1]-py*9*SS),(c[0]+px*9*SS, c[1]+py*9*SS)], fill=GREEN, width=int(2.4*SS))
        ax,ay=self.Q(a); bx,by=self.Q(b); mx,my=(ax+bx)/2,(ay+by)/2
        ux,uy=unit(bx-ax,by-ay); px,py=-uy,ux
        for i in range(n):
            cx,cy=mx+ux*(base+i)*6.5, my+uy*(base+i)*6.5
            self.el.append(f'<line x1="{cx-px*6:.1f}" y1="{cy-py*6:.1f}" x2="{cx+px*6:.1f}" y2="{cy+py*6:.1f}" stroke="{SVG_GREEN}" stroke-width="2.8" stroke-linecap="round"/>')
    def cross(self,p,s=7):
        x,y=self.P(p)
        self.d.line([(x-s*SS,y-s*SS),(x+s*SS,y+s*SS)],fill=BLACK,width=int(2*SS))
        self.d.line([(x-s*SS,y+s*SS),(x+s*SS,y-s*SS)],fill=BLACK,width=int(2*SS))
        qx,qy=self.Q(p)
        self.el.append(f'<line x1="{qx-5:.1f}" y1="{qy-5:.1f}" x2="{qx+5:.1f}" y2="{qy+5:.1f}" stroke="{SVG_BLACK}" stroke-width="2"/>')
        self.el.append(f'<line x1="{qx-5:.1f}" y1="{qy+5:.1f}" x2="{qx+5:.1f}" y2="{qy-5:.1f}" stroke="{SVG_BLACK}" stroke-width="2"/>')
    def ges(self,text):
        rich_text(self.d, 150*SS, 660*SS, "gesucht: "+text, F_GES, F_GES_SUB, RED, anchor="lm")
    def save(self,n):
        img2=self.img.resize((W0,H0), Image.LANCZOS)
        img2.save(f"{OUT}/Trig-Aufgabe-{n:02d}.png","PNG")
        print("saved", n)
        return (f'<svg viewBox="0 0 {self.SW} {self.SH}" width="{self.SW}" height="{self.SH}" '
                f'preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">'+"".join(self.el)+'</svg>')

FIGS={}   # n -> (svg, ges_html)
AREA={1:"ABC",2:"ABC",3:"ABC",4:"ADC",5:"BGC",6:"ABC",7:"ABC",8:"ABC",9:"ABC",10:"ABC",
      11:"ABC",12:"ABC",13:"BCG",14:"ADC",15:"ABC",16:"ABC",17:"ABCD",18:"ABCD",19:"BGC",20:"BGC"}

def sub_html(ges_png):
    # "β + A[ABC]" → "β + A<sub>ABC</sub>"
    return re.sub(r'A\[([A-Z]+)\]', r'A<sub>\1</sub>', ges_png)

def register(n, dl, ges_png):
    dl.ges(ges_png)
    FIGS[n]=(dl.save(n), sub_html(ges_png))

def deg(x): return math.radians(x)

# ---------- Aufgaben 1–14 (Figuren-Neubau, Geometrie aus den Gegeben-Angaben) ----------
def a01():
    A=(0,0); B=(12,0); C=(7*math.cos(deg(50)), 7*math.sin(deg(50)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,B,"12 cm",ce); dl.sidelabel(A,C,"7 cm",ce)
    dl.angle(A,B,C,"50°"); dl.angle(B,C,A,"β")
    register(1, dl, "β + A[ABC]")

def a02():
    A=(0,0); B=(14,0); C=(7, 7*math.tan(deg(35)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,B,"14 cm",ce); dl.sidelabel(A,C,"AC = BC",ce,red=True,off=40,soff=30)
    dl.angle(A,B,C,"35°")
    register(2, dl, "AC + A[ABC]")

def a03():
    A=(0,0); C=(7*math.cos(deg(40)), 7*math.sin(deg(40)))
    B=(C[0]+math.sqrt(81-C[1]**2), 0)
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,C,"7 cm",ce); dl.sidelabel(C,B,"9 cm",ce)
    dl.angle(A,B,C,"40°"); dl.angle(B,C,A,"β")
    register(3, dl, "β + A[ABC]")

def a04():
    dcb=math.degrees(math.acos(6/9.0)); acb=dcb+25
    b=6*math.tan(deg(acb))
    A=(0,0); B=(b,0); C=(b,6); D=(b-math.sqrt(81-36),0)
    dl=Dual([A,B,C,D]); big=centroid([A,B,C])
    dl.shape([A,D,C])
    dl.line(A,B); dl.line(B,C); dl.line(C,D)
    dl.rang(B,A,C)
    dl.vlabel(A,"A",big); dl.vlabel(B,"B",(b-2,3)); dl.vlabel(C,"C",big); dl.vlabel(D,"D",(D[0],3))
    dl.sidelabel(B,C,"6 cm",A); dl.sidelabel(C,D,"9 cm",A,off=40,soff=30,t=0.62)
    dl.angle(C,D,A,"25°")
    register(4, dl, "A[ADC]")

def a_gsp(n, ab, alpha, area_name):
    # Vorlage "G auf AC mit AG = GB, rechter Winkel bei C" (Aufgaben 5, 13, 19, 20)
    A=(0,0); B=(ab,0)
    Gx=ab/2; Gy=Gx*math.tan(deg(alpha)); G=(Gx,Gy)
    GB=ab/(2*math.cos(deg(alpha)))
    GC=GB*math.cos(deg(2*alpha))
    ux,uy=unit(Gx,Gy)
    C=(Gx+ux*GC, Gy+uy*GC)
    dl=Dual([A,B,C,G]); big=centroid([A,B,C])
    dl.line(A,C); dl.line(A,B)
    dl.shape([B,G,C])
    dl.vlabel(A,"A",big); dl.vlabel(B,"B",big); dl.vlabel(C,"C",big); dl.vlabel(G,"G",big)
    dl.sidelabel(A,B,f"{ab:g} cm",big)
    dl.ticks(A,G,2); dl.ticks(G,B,2)
    dl.angle(A,B,G,f"{alpha:g}°",r=40)
    dl.rang(C,G,B)
    dl.angle(B,C,G,"β₂",r=40)
    register(n, dl, f"β₂ + A[{area_name}]")

def a06():
    A=(0,0); B=(10,0); C=(10-13*math.cos(deg(48)), 13*math.sin(deg(48)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,B,"10 cm",ce); dl.sidelabel(B,C,"13 cm",ce)
    dl.angle(B,A,C,"48°"); dl.angle(A,B,C,"α")
    register(6, dl, "α + A[ABC]")

def a07():
    ab=2*9*math.sin(deg(22))
    A=(0,0); B=(ab,0); C=(ab/2, 9*math.cos(deg(22)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,C,"9 cm",ce); dl.sidelabel(B,C,"9 cm",ce)
    dl.sidelabel(A,B,"AB = ?",C,red=True)
    dl.angle(C,A,B,"44°")
    register(7, dl, "AB + A[ABC]")

def a08():
    A=(0,0); B=(11,0)
    ac=11*math.cos(deg(32)); C=(ac*math.cos(deg(32)), ac*math.sin(deg(32)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,B,"11 cm",ce)
    dl.angle(A,B,C,"32°"); dl.rang(C,A,B)
    register(8, dl, "BC + A[ABC]")

def a09():
    A=(0,0); B=(6,0); C=(8*math.cos(deg(70)), 8*math.sin(deg(70)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,B,"6 cm",ce); dl.sidelabel(A,C,"8 cm",ce)
    dl.sidelabel(B,C,"a = ?",A,red=True,off=40,soff=30)
    dl.angle(A,B,C,"70°"); dl.angle(B,C,A,"β")
    register(9, dl, "Seite a, β + A[ABC]")

def a10():
    t42,t58=math.tan(deg(42)),math.tan(deg(58))
    cx=10*t58/(t42+t58); C=(cx, cx*t42); A=(0,0); B=(10,0); Hf=(cx,0)
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.dashed(C,Hf); dl.rang(Hf,C,A)
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",(cx,0))
    dl.sidelabel(A,B,"10 cm",ce)
    dl.sidelabel(C,Hf,"h",A,red=True,off=30,soff=20)
    dl.angle(A,B,C,"42°"); dl.angle(B,C,A,"58°")
    register(10, dl, "Höhe h + A[ABC]")

def a11():
    A=(0,0); B=(10,0); C=(8*math.cos(deg(40)), 8*math.sin(deg(40)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,B,"10 cm",ce); dl.sidelabel(A,C,"8 cm",ce)
    dl.angle(A,B,C,"40°"); dl.angle(B,C,A,"β")
    register(11, dl, "β + A[ABC]")

def a12():
    A=(0,0); B=(10,0); C=(5, 5*math.tan(deg(40)))
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    dl.sidelabel(A,B,"10 cm",ce); dl.sidelabel(A,C,"AC = BC",ce,red=True,off=40,soff=30)
    dl.angle(A,B,C,"40°")
    register(12, dl, "AC + A[ABC]")

def a14():
    dcb=math.degrees(math.acos(5/7.0)); acb=dcb+20
    b=5*math.tan(deg(acb))
    A=(0,0); B=(b,0); C=(b,5); D=(b-math.sqrt(49-25),0)
    dl=Dual([A,B,C,D]); big=centroid([A,B,C])
    dl.shape([A,D,C])
    dl.line(A,B); dl.line(B,C); dl.line(C,D)
    dl.rang(B,A,C)
    dl.vlabel(A,"A",big); dl.vlabel(B,"B",(b-2,2.5)); dl.vlabel(C,"C",big); dl.vlabel(D,"D",(D[0],2.5))
    dl.sidelabel(B,C,"5 cm",A); dl.sidelabel(C,D,"7 cm",A,off=40,soff=30,t=0.62)
    dl.angle(C,D,A,"20°")
    register(14, dl, "A[ADC]")

# ---------- Aufgaben 15–18 ----------
def a15():
    a=8.0; A=(0,0); B=(a,0); C=(a/2, a*math.sqrt(3)/2)
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    for s in [(A,B),(B,C),(C,A)]: dl.ticks(s[0],s[1],1)
    dl.sidelabel(A,B,"8 cm",ce)
    dl.angle(A,B,C,"60°")
    register(15, dl, "Höhe h + A[ABC]")

def a16():
    h=10.0; a=2*h/math.sqrt(3); A=(0,0); B=(a,0); C=(a/2,h); Mid=(a/2,0)
    dl=Dual([A,B,C]); ce=centroid([A,B,C])
    dl.shape([A,B,C])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce)
    for s in [(A,B),(B,C),(C,A)]: dl.ticks(s[0],s[1],1)
    dl.dashed(C,Mid); dl.rang(Mid,A,C)
    dl.sidelabel(C,Mid,"10 cm",B,off=30,soff=26)
    dl.angle(B,A,C,"60°")
    register(16, dl, "Seite a + A[ABC]")

def a17():
    a=12.0; c=6.0; ang=65.0
    h=((a-c)/2)*math.tan(deg(ang))
    A=(0,0); B=(a,0); C=(a-(a-c)/2,h); D=((a-c)/2,h)
    dl=Dual([A,B,C,D]); ce=centroid([A,B,C,D])
    dl.shape([A,B,C,D])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce); dl.vlabel(D,"D",ce)
    dl.sidelabel(A,B,"12 cm",ce); dl.sidelabel(D,C,"6 cm",ce,off=30)
    dl.ticks(A,D,1); dl.ticks(B,C,1)
    dl.angle(A,B,D,"65°")
    register(17, dl, "Höhe + Schenkel + A[ABCD]")

def a18():
    a=11.0; c=6.0; ang=55.0
    off=a-c; h=off*math.tan(deg(ang))
    A=(0,0); B=(a,0); C=(c,h); D=(0,h)
    dl=Dual([A,B,C,D]); ce=centroid([A,B,C,D])
    dl.shape([A,B,C,D])
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce); dl.vlabel(D,"D",ce)
    dl.sidelabel(A,B,"11 cm",ce); dl.sidelabel(D,C,"6 cm",ce,off=30)
    dl.rang(A,B,D); dl.rang(D,A,C)
    dl.angle(B,A,C,"55°")
    register(18, dl, "Höhe + A[ABCD]")

# ---------- Aufgaben 21–26 (Notenbereich-Stil) ----------
def t_rect(n, alpha, fb):
    ra=deg(alpha)
    b=fb/math.tan(ra); ad=fb/(4*math.sin(ra)**2)
    A=(0,0); B=(b,0); C=(b,ad); D=(0,ad); F=(b,fb); E=(b/2,fb/2)
    dl=Dual([A,B,C,D]); ce=centroid([A,B,C,D])
    dl.shape([A,B,C,D], fill=False)
    dl.line(A,F); dl.line(D,E)
    dl.ticks(A,D,1); dl.ticks(D,E,1)
    dl.ticks((0,0),E,2); dl.ticks(E,F,2)
    dl.vlabel(A,"A",ce); dl.vlabel(B,"B",ce); dl.vlabel(C,"C",ce); dl.vlabel(D,"D",ce)
    dl.vlabel(E,"E",D); dl.vlabel(F,"F",ce)
    dl.angle(A,B,F,f"{alpha:g}°")
    dl.sidelabel(F,B,f"{fb:g} cm",A)
    register(n, dl, "Strecke CE")

def t_knick(n, af, dc, ang):
    ra=deg(ang)
    ad=af*math.tan(ra); df=af/math.cos(ra)
    fc=math.sqrt(dc*dc-df*df); cb=90-ang
    fb=fc*math.cos(deg(cb)); bc=fc*math.sin(deg(cb))
    A=(0,0); F=(af,0); B=(af+fb,0); D=(0,ad); C=(af+fb,bc)
    dl=Dual([A,B,C,D]); big=centroid([A,B,C,D])
    dl.shape([D,F,C], fill=False)
    dl.line(A,B); dl.line(A,D); dl.line(B,C); dl.line(D,C)
    dl.rang(F,D,C); dl.rang(A,F,D); dl.rang(B,F,C)
    dl.vlabel(A,"A",big); dl.vlabel(B,"B",big)
    dl.vlabel(D,"D",big); dl.vlabel(C,"C",big)
    dl.vlabel(F,"F",(af,ad))
    dl.angle(F,A,D,f"{ang:g}°")
    dl.sidelabel(A,F,f"{af:g} cm",(af/2,ad))
    dl.sidelabel(D,C,f"{dc:g} cm",A)
    register(n, dl, "Strecke BC")

def t_pyr(n, s_len, gamma):
    a=10.0; ox,oy=4.2,3.0
    P1=(0,0); P2=(a,0); P3=(a+ox,oy); P4=(ox,oy)
    M=((a+ox)/2, oy/2); S=(M[0], M[1]+9.0)
    dl=Dual([P1,P2,P3,P4,S])
    dl.dashed(P3,P4); dl.dashed(P4,P1); dl.dashed(S,P4)
    dl.dashed(S,M); dl.dashed(M,P3)
    dl.line(P1,P2); dl.line(P2,P3)
    dl.line(S,P1); dl.line(S,P2); dl.line(S,P3)
    dl.cross(M)
    dl.rang(M,S,P3)
    dl.angle(S,M,P3,f"{gamma:g}°")
    dl.sidelabel(S,P3,f"s = {s_len:g} cm",M,off=40,soff=34)
    register(n, dl, "Oberfläche O + Volumen V")

a01(); a02(); a03(); a04()
a_gsp(5, 12.0, 25.0, "BGC")
a06(); a07(); a08(); a09(); a10(); a11(); a12()
a_gsp(13, 10.0, 30.0, "BCG")
a14(); a15(); a16(); a17(); a18()
a_gsp(19, 14.0, 35.0, "BGC")
a_gsp(20, 16.0, 20.0, "BGC")
t_rect(21, 25, 6)
t_knick(22, 6, 9, 35)
t_pyr(23, 12, 35)
t_rect(24, 20, 5)
t_knick(25, 8, 12, 40)
t_pyr(26, 10, 30)

# ---------- HTML-Karten patchen (Figur + gesucht; Lösungen bleiben, nur A-Notation) ----------
POOL=os.path.join(os.path.dirname(OUT), "Trigonometrie Aufgabenpool.html")
if os.path.exists(POOL):
    h=io.open(POOL,encoding="utf-8").read()
    chunks=h.split('<div class="card"')
    out=[chunks[0]]
    for ch in chunks[1:]:
        n=int(re.search(r'data-n="(\d+)"',ch).group(1))
        if n in FIGS:
            svg,ges=FIGS[n]
            ch=re.sub(r'<div class="fig">.*?</div>', lambda m: '<div class="fig">'+svg+'</div>', ch, count=1, flags=re.S)
            ch=re.sub(r'<div class="ges">.*?</div>', lambda m: '<div class="ges"><b>gesucht:</b> '+ges+'</div>', ch, count=1, flags=re.S)
            nm=AREA.get(n)
            if nm:
                ch=ch.replace("Fläche von Dreieck "+nm, f"A<sub>{nm}</sub>")
                ch=ch.replace("Fläche "+nm+" =", f"A<sub>{nm}</sub> =")
                ch=ch.replace("Fläche = ", f"A<sub>{nm}</sub> = ")
        out.append(ch)
    io.open(POOL,"w",encoding="utf-8").write('<div class="card"'.join(out))
    print("HTML gepatcht:", len(FIGS), "Karten")
print("done – jetzt build_exam.py laufen lassen")
