# -*- coding: utf-8 -*-
import math
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

FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FI = "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf"

def font(path, size): return ImageFont.truetype(path, int(size*SS))
F_VERT = font(FB, 30)
F_SIDE = font(FB, 26)
F_ANG  = font(FB, 24)
F_ANG_SUB = font(FB, 17)
F_GES  = font(FI, 27)
F_GES_SUB = font(FI, 19)

def text_sub(d, x, y, s, fnt, subfnt, color, anchor="lm"):
    parts=[]
    for ch in s:
        if ch=='₂': parts.append(('2', subfnt, fnt.size*0.24))
        else: parts.append((ch, fnt, 0))
    widths=[d.textlength(c, font=f) for c,f,_ in parts]
    total=sum(widths)
    cx = x - (total/2 if anchor[0]=='m' else 0)
    for (c,f,dy),w in zip(parts,widths):
        d.text((cx, y+dy), c, font=f, fill=color, anchor="lm")
        cx+=w

def newcanvas():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([6*SS,6*SS,W-6*SS,H-6*SS], radius=22*SS, outline=BORDER, width=2*SS)
    return img, d

# ---- coordinate fit ----
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

def poly(d, P, pts, fill=FILL, outline=BLUE, w=3):
    pp=[P(p) for p in pts]
    d.polygon(pp, fill=fill, outline=None)
    d.line(pp+[pp[0]], fill=outline, width=int(w*SS), joint="curve")

def line(d, P, a, b, color=BLUE, w=3):
    d.line([P(a),P(b)], fill=color, width=int(w*SS))

def dashed(d, P, a, b, color=BLACK, w=2, dash=14, gap=10):
    x1,y1=P(a); x2,y2=P(b); L=math.hypot(x2-x1,y2-y1)
    ux,uy=(x2-x1)/L,(y2-y1)/L; t=0
    while t<L:
        s=min(dash*SS, L-t)
        d.line([(x1+ux*t,y1+uy*t),(x1+ux*(t+s),y1+uy*(t+s))], fill=color, width=int(w*SS))
        t+=(dash+gap)*SS

def vlabel(d, P, p, text, away_from, off=30):
    px,py=P(p); cx,cy=P(away_from)
    ux,uy=unit(px-cx,py-cy)
    d.text((px+ux*off*SS, py+uy*off*SS), text, font=F_VERT, fill=BLACK, anchor="mm")

def sidelabel(d, P, a, b, text, away_from, off=34, fnt=F_SIDE, color=BLACK):
    ax,ay=P(a); bx,by=P(b); mx,my=(ax+bx)/2,(ay+by)/2
    cx,cy=P(away_from); ux,uy=unit(mx-cx,my-cy)
    d.text((mx+ux*off*SS, my+uy*off*SS), text, font=fnt, fill=color, anchor="mm")

def angle_at(d, P, V, A, B, label, radius=42, color=RED, lab_r=1.5, lab_color=None):
    vx,vy=P(V); ax,ay=P(A); bx,by=P(B)
    a1=math.degrees(math.atan2(ay-vy, ax-vx))
    a2=math.degrees(math.atan2(by-vy, bx-vx))
    dd=(a2-a1)%360
    if dd<=180: start,end,span=a1,a2,dd
    else: start,end,span=a2,a1,360-dd
    r=radius*SS
    d.arc([vx-r,vy-r,vx+r,vy+r], start, end, fill=color, width=int(2.4*SS))
    mid=math.radians(start+span/2)
    lx=vx+math.cos(mid)*r*lab_r; ly=vy+math.sin(mid)*r*lab_r
    if '₂' in label:
        text_sub(d, lx, ly, label, F_ANG, F_ANG_SUB, lab_color or color, anchor="mm")
    else:
        d.text((lx,ly), label, font=F_ANG, fill=lab_color or color, anchor="mm")

def right_angle(d, P, V, A, B, size=0.55):
    vx,vy=P(V); ax,ay=P(A); bx,by=P(B)
    u1=unit(ax-vx,ay-vy); u2=unit(bx-vx,by-vy)
    s=size*0.5*( ((ax-vx)**2+(ay-vy)**2)**0.5 )
    s=min(s, 26*SS)
    p1=(vx+u1[0]*s, vy+u1[1]*s)
    p3=(vx+u2[0]*s, vy+u2[1]*s)
    p2=(p1[0]+u2[0]*s, p1[1]+u2[1]*s)
    d.line([p1,p2,p3], fill=BLUE, width=int(2*SS))
    cx=vx+(u1[0]+u2[0])*s*0.5; cy=vy+(u1[1]+u2[1])*s*0.5
    d.ellipse([cx-2.6*SS,cy-2.6*SS,cx+2.6*SS,cy+2.6*SS], fill=BLUE)

def ticks(d, P, a, b, n=1, color=GREEN, length=9, spacing=7):
    ax,ay=P(a); bx,by=P(b); mx,my=(ax+bx)/2,(ay+by)/2
    ux,uy=unit(bx-ax,by-ay); px,py=-uy,ux
    base=-(n-1)/2.0
    for i in range(n):
        c=( mx+ux*(base+i)*spacing*SS, my+uy*(base+i)*spacing*SS )
        d.line([(c[0]-px*length*SS, c[1]-py*length*SS),(c[0]+px*length*SS, c[1]+py*length*SS)],
               fill=color, width=int(2.4*SS))

def gesucht(d, text):
    text_sub(d, 150*SS, 660*SS, "gesucht: "+text, F_GES, F_GES_SUB, RED, anchor="lm")

def save(img, n):
    img2=img.resize((W0,H0), Image.LANCZOS)
    img2.save(f"{OUT}/Trig-Aufgabe-{n:02d}.png","PNG")
    print("saved", n)

# ============ AUFGABE 15: gleichseitig, Seite 8 ============
def a15():
    a=8.0; A=(0,0); B=(a,0); C=(a/2, a*math.sqrt(3)/2)
    P=Fit([A,B,C]); img,d=newcanvas(); ce=centroid([A,B,C])
    poly(d,P,[A,B,C])
    for X,nm,aw in [(A,"A",B),(B,"B",A),(C,"C",ce)]:
        pass
    vlabel(d,P,A,"A",ce); vlabel(d,P,B,"B",ce); vlabel(d,P,C,"C",ce)
    for s in [(A,B),(B,C),(C,A)]: ticks(d,P,s[0],s[1],1)
    sidelabel(d,P,A,B,"8 cm",ce)
    angle_at(d,P,A,B,C,"60°",radius=40,color=RED,lab_color=BLACK)
    gesucht(d,"Höhe h + Flächeninhalt")
    save(img,15)

# ============ AUFGABE 16: gleichseitig, Höhe 10 ============
def a16():
    h=10.0; a=2*h/math.sqrt(3); A=(0,0); B=(a,0); C=(a/2,h); Mid=(a/2,0)
    P=Fit([A,B,C]); img,d=newcanvas(); ce=centroid([A,B,C])
    poly(d,P,[A,B,C])
    vlabel(d,P,A,"A",ce); vlabel(d,P,B,"B",ce); vlabel(d,P,C,"C",ce)
    for s in [(A,B),(B,C),(C,A)]: ticks(d,P,s[0],s[1],1)
    dashed(d,P,C,Mid,color=BLACK,w=2)
    right_angle(d,P,Mid,A,C)
    sidelabel(d,P,C,Mid,"10 cm",B,off=30,color=BLACK)
    angle_at(d,P,B,A,C,"60°",radius=40,color=RED,lab_color=BLACK)
    gesucht(d,"Seite a + Flächeninhalt")
    save(img,16)

# ============ AUFGABE 17: gleichschenkliges Trapez ============
def a17():
    a=12.0; c=6.0; ang=65.0
    h=((a-c)/2)*math.tan(math.radians(ang))
    A=(0,0); B=(a,0); C=(a-(a-c)/2,h); D=((a-c)/2,h)
    P=Fit([A,B,C,D]); img,d=newcanvas(); ce=centroid([A,B,C,D])
    poly(d,P,[A,B,C,D])
    vlabel(d,P,A,"A",ce); vlabel(d,P,B,"B",ce); vlabel(d,P,C,"C",ce); vlabel(d,P,D,"D",ce)
    sidelabel(d,P,A,B,"12 cm",ce)
    sidelabel(d,P,D,C,"6 cm",ce,off=30)
    ticks(d,P,A,D,1); ticks(d,P,B,C,1)
    angle_at(d,P,A,B,D,"65°",radius=44,color=RED,lab_color=BLACK)
    gesucht(d,"Höhe + Schenkel + Flächeninhalt")
    save(img,17)

# ============ AUFGABE 18: rechtwinkliges Trapez ============
def a18():
    a=11.0; c=6.0; ang=55.0
    off=a-c; h=off*math.tan(math.radians(ang))
    A=(0,0); B=(a,0); C=(c,h); D=(0,h)
    P=Fit([A,B,C,D]); img,d=newcanvas(); ce=centroid([A,B,C,D])
    poly(d,P,[A,B,C,D])
    vlabel(d,P,A,"A",ce); vlabel(d,P,B,"B",ce); vlabel(d,P,C,"C",ce); vlabel(d,P,D,"D",ce)
    sidelabel(d,P,A,B,"11 cm",ce)
    sidelabel(d,P,D,C,"6 cm",ce,off=30)
    right_angle(d,P,A,B,D); right_angle(d,P,D,A,C)
    angle_at(d,P,B,A,C,"55°",radius=44,color=RED,lab_color=BLACK)
    gesucht(d,"Höhe + Flächeninhalt")
    save(img,18)

# ============ AUFGABE 19 & 20: wie Aufgabe 5 ============
def a_like5(n, ab, alpha):
    A=(0,0); B=(ab,0)
    Gx=ab/2; Gy=Gx*math.tan(math.radians(alpha)); G=(Gx,Gy)
    GB=ab/(2*math.cos(math.radians(alpha)))
    bgc=180-2*alpha  # angle AGB
    angBGC=180-bgc   # = 2*alpha
    GC=GB*math.cos(math.radians(angBGC))
    ux,uy=unit(Gx-0,Gy-0)
    C=(Gx+ux*GC, Gy+uy*GC)
    P=Fit([A,B,C,G]); img,d=newcanvas(); ce=centroid([B,G,C])
    # outer lines
    line(d,P,A,C,BLUE,3)   # A through G to C
    line(d,P,A,B,BLUE,3)
    # filled inner triangle B-G-C
    poly(d,P,[B,G,C], fill=FILL, outline=BLUE, w=3)
    line(d,P,A,G,BLUE,3)
    big=centroid([A,B,C])
    vlabel(d,P,A,"A",big); vlabel(d,P,B,"B",big); vlabel(d,P,C,"C",big); vlabel(d,P,G,"G",big)
    sidelabel(d,P,A,B,f"{ab:g} cm",big)
    ticks(d,P,A,G,2); ticks(d,P,G,B,2)
    angle_at(d,P,A,B,G,f"{alpha:g}°",radius=46,color=RED,lab_color=BLACK)
    right_angle(d,P,C,G,B)
    angle_at(d,P,B,C,G,"β₂",radius=34,color=RED)
    gesucht(d,"β₂ + Fläche von Dreieck BGC")
    save(img,n)

a15(); a16(); a17(); a18()
a_like5(19, 14.0, 35.0)
a_like5(20, 16.0, 20.0)
print("done")
