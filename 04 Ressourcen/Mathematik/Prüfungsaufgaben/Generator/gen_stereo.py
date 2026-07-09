#!/usr/bin/env python3
# Aufgabenpool Stereometrie – baut SVG-Figuren, HTML und .md
import os

BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben"
IMG = os.path.join(BASE, "Bilder")
os.makedirs(IMG, exist_ok=True)

ACCENT, ACCENTDARK = "#0891b2", "#0e7490"
SW, HID, FILL, GREEN, RED = "#1a1a1a", "#9aa3aa", "#eef3f7", "#2e9e5b", "#c0392b"

# ---------------- SVG-Helfer ----------------
def wrap(w, h, inner):
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="Arial,Helvetica,sans-serif">'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>{inner}</svg>')

def L(x1, y1, x2, y2, dashed=False, col=SW, w=2):
    d = ' stroke-dasharray="5 4"' if dashed else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d}/>'

def P(pts, fill="none", stroke=SW, w=2, dashed=False):
    d = ' stroke-dasharray="5 4"' if dashed else ''
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{d}/>'

def E(cx, cy, rx, ry, fill="none", stroke=SW, w=2, dashed=False):
    d = ' stroke-dasharray="5 4"' if dashed else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{d}/>'

def arc_front(cx, cy, rx, ry, col=SW, w=2):
    return f'<path d="M {cx-rx},{cy} A {rx},{ry} 0 0 0 {cx+rx},{cy}" fill="none" stroke="{col}" stroke-width="{w}"/>'

def arc_back(cx, cy, rx, ry):
    return f'<path d="M {cx-rx},{cy} A {rx},{ry} 0 0 1 {cx+rx},{cy}" fill="none" stroke="{HID}" stroke-width="1.6" stroke-dasharray="5 4"/>'

def T(x, y, txt, col=SW, size=14, anchor="start", weight="normal", style="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}">{txt}</text>')

def rangle(x, y, s=12, dx=1, dy=-1):
    # gerundeter rechter Winkel (Viertelkreis) mit Punkt, öffnet nach oben-rechts
    r = s
    return (f'<path d="M {x},{y-r} A {r},{r} 0 0 1 {x+r},{y}" fill="none" stroke="{SW}" stroke-width="1.5"/>'
            f'<circle cx="{x+0.42*r:.1f}" cy="{y-0.42*r:.1f}" r="1.9" fill="{SW}"/>')

def cyl(cx, ty, by, rx, ry):
    return (E(cx, ty, rx, ry, FILL) + L(cx-rx, ty, cx-rx, by) + L(cx+rx, ty, cx+rx, by)
            + arc_back(cx, by, rx, ry) + arc_front(cx, by, rx, ry))

# ---------------- Figuren ----------------
F = {}

# 1) Quadratische Pyramide  a=5, h=8
def fig_pyr():
    Fp, Gp, Hp, Ep, S = (55,205), (190,205), (235,165), (100,165), (150,38)
    M = (145,185)
    s = []
    s.append(P([Ep, Fp, Gp, Hp], FILL))                       # Grundfläche
    s.append(L(*Ep, *Hp, dashed=True))                        # hintere Kante
    s.append(L(*S, *Ep, dashed=True))                         # hintere Seitenkante
    for V in (Fp, Gp, Hp):
        s.append(L(*S, *V))
    s.append(L(*Fp, *Gp, col=GREEN, w=3))                     # vordere Grundkante (grün)
    s.append(L(*M, *S, dashed=True, col=GREEN, w=2))          # Höhe (grün, gestrichelt)
    s.append(rangle(M[0], M[1], 11, dx=1, dy=-1))
    s.append(T(160, 120, "h", GREEN, 16, weight="bold"))
    s.append(T(92, 118, "s", SW, 15, weight="bold"))
    s.append(L(*S, 122,205, dashed=True, col=HID, w=1.4))     # Seitenhöhe-Hilfslinie
    s.append(f'<text x="128" y="150" font-size="12" fill="{SW}">h<tspan font-size="9" dy="3">s</tspan></text>')
    s.append(T(122, 224, "5 cm", SW, 13, anchor="middle"))
    return wrap(280, 245, "".join(s))
F[1] = fig_pyr()

# 2) Würfel mit zylindrischer Bohrung
def fig_cube_hole():
    A,B,C,D = (70,82),(180,82),(180,192),(70,192)
    dx,dy = 55,40
    Ap,Bp,Cp = (A[0]+dx,A[1]-dy),(B[0]+dx,B[1]-dy),(C[0]+dx,C[1]-dy)
    Dp = (D[0]+dx, D[1]-dy)
    s = []
    s.append(P([A,B,C,D], FILL))                  # Vorderseite
    s.append(P([A,B,Bp,Ap], "#f6fafc"))           # Deckfläche
    s.append(P([B,C,Cp,Bp], "#f0f5f8"))           # rechte Seite
    s.append(L(*Ap,*Dp, dashed=True)); s.append(L(*Dp,*Cp, dashed=True)); s.append(L(*D,*Dp, dashed=True))
    for a,b in [(A,B),(B,C),(C,D),(D,A),(A,Ap),(B,Bp),(C,Cp),(Ap,Bp),(Bp,Cp)]:
        s.append(L(*a,*b))
    # Bohrung
    topc = (152,61); botc = (152,171); hrx,hry = 20,8
    s.append(E(*topc, hrx, hry, "#ffffff"))                       # obere Öffnung
    s.append(L(topc[0]-hrx, topc[1], botc[0]-hrx, botc[1], dashed=True, col=HID, w=1.6))
    s.append(L(topc[0]+hrx, topc[1], botc[0]+hrx, botc[1], dashed=True, col=HID, w=1.6))
    s.append(E(*botc, hrx, hry, "none", HID, 1.6, dashed=True))   # untere Öffnung
    s.append(L(botc[0], botc[1], botc[0]+hrx, botc[1], col=SW, w=1.5))   # Radius in der Grundfläche
    s.append(T(botc[0]+hrx//2, botc[1]-5, "r", SW, 13, anchor="middle"))
    s.append(T(245, 70, "a", SW, 14, weight="bold"))
    return wrap(290, 240, "".join(s))
F[2] = fig_cube_hole()

# 3) Kegel auf Zylinder  r=4, hZ=6, eps=50°
def fig_cone_cyl():
    cx = 130; rx, ry = 70, 18
    cyl_top, cyl_bot = 150, 232
    apex = (cx, 40)
    s = []
    s.append(cyl(cx, cyl_top, cyl_bot, rx, ry))
    # Kegel auf Deckfläche
    s.append(L(apex[0], apex[1], cx-rx, cyl_top)); s.append(L(apex[0], apex[1], cx+rx, cyl_top))
    s.append(arc_back(cx, cyl_top, rx, ry)); s.append(arc_front(cx, cyl_top, rx, ry))
    # Radius (in der Deckfläche)
    s.append(L(cx, cyl_top, cx+rx, cyl_top, col=SW, w=1.6))
    s.append(T(cx+24, cyl_top-7, "r", SW, 13, anchor="middle"))
    # Winkel eps am rechten Randpunkt: Bogen zwischen Radius und Kegelseite, eps im Bogen
    s.append(f'<path d="M 174,{cyl_top} A 26,26 0 0 1 186,128" fill="none" stroke="{SW}" stroke-width="1.4"/>')
    s.append(T(183, 144, "&#949;", SW, 14, anchor="middle"))
    # Kegelhöhe (gestrichelt)
    s.append(L(cx, apex[1], cx, cyl_top, dashed=True, col=HID, w=1.4))
    # Zylinderhöhe h_Z links
    s.append(L(cx-rx-12, cyl_top, cx-rx-12, cyl_bot, col=HID, w=1.2))
    s.append(f'<text x="{cx-rx-16}" y="{(cyl_top+cyl_bot)//2+4}" font-size="13" fill="{SW}" text-anchor="end">h<tspan font-size="9" dy="3">Z</tspan></text>')
    return wrap(280, 268, "".join(s))
F[3] = fig_cone_cyl()

# 4) Dreiseitiges Prisma  Katheten 3,4 ; Länge 10
def fig_prism():
    A,B,C = (70,190),(70,95),(160,190)            # vorderes rechtw. Dreieck (A=rechter Winkel)
    dx,dy = 55,35
    Ap,Bp,Cp = (A[0]+dx,A[1]-dy),(B[0]+dx,B[1]-dy),(C[0]+dx,C[1]-dy)
    s = []
    s.append(P([A,B,C], FILL))
    s.append(P([B,C,Cp,Bp], "#f0f5f8"))           # Mantel oben-rechts (sichtbar)
    s.append(L(*A,*Ap, dashed=True))
    s.append(L(*Ap,*Bp, dashed=True)); s.append(L(*Ap,*Cp, dashed=True))
    for a,b in [(A,B),(B,C),(C,A),(B,Bp),(C,Cp),(Bp,Cp)]:
        s.append(L(*a,*b))
    s.append(rangle(A[0],A[1],12, dx=1, dy=-1))
    s.append(T(112,207,"4 cm", SW, 13, anchor="middle"))
    s.append(T(58,145,"3 cm", SW, 13, anchor="end"))
    s.append(T(150,70,"10 cm", SW, 13))
    return wrap(250, 230, "".join(s))
F[4] = fig_prism()

# 5) Zylinder r=3 h=10
def fig_cyl():
    cx,rx,ry = 120,55,18
    s = [cyl(cx, 55, 195, rx, ry)]
    s.append(L(cx, 55, cx+rx, 55, col=SW, w=1.4)); s.append(T(cx+18,50,"r",SW,13))
    s.append(L(cx-rx-8,55,cx-rx-8,195, col=HID, w=1.2))
    s.append(T(cx-rx-14,128,"h",SW,13,anchor="end"))
    return wrap(240, 230, "".join(s))
F[5] = fig_cyl()

# 6) Kegel r=6 h=8
def fig_cone():
    cx,rx,ry = 120,60,18
    apex=(cx,35); by=195
    s=[]
    s.append(L(*apex,cx-rx,by)); s.append(L(*apex,cx+rx,by))
    s.append(arc_back(cx,by,rx,ry)); s.append(arc_front(cx,by,rx,ry))
    s.append(L(cx,apex[1],cx,by, dashed=True, col=HID, w=1.4))
    s.append(L(cx,by,cx+rx,by, col=SW, w=1.4)); s.append(T(cx+22,by-6,"r",SW,13))
    s.append(rangle(cx,by,11, dx=1, dy=-1))
    s.append(T(cx-10,120,"h",SW,13,anchor="end"))
    s.append(T(cx+38,118,"s",SW,13))
    return wrap(245, 235, "".join(s))
F[6] = fig_cone()

# 7) Kugel r=6
def fig_sphere():
    cx,cy,r = 120,115,80
    s=[f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FILL}" stroke="{SW}" stroke-width="2"/>']
    s.append(E(cx,cy,r,26,"none",HID,1.6,dashed=True))     # Äquator
    s.append(L(cx,cy,cx+r,cy, col=SW, w=1.4)); s.append(T(cx+r//2,cy-6,"r",SW,13,anchor="middle"))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{SW}"/>')
    return wrap(240, 230, "".join(s))
F[7] = fig_sphere()

# 8) Rechteck rotiert um Achse -> Zylinder
def fig_rot_rect():
    ax=95
    s=[L(ax,45,ax,205, dashed=True, col=ACCENT, w=2)]
    s.append(P([(ax,70),(170,70),(170,180),(ax,180)], FILL, SW, 2))
    s.append(P([(20,70),(ax,70),(ax,180),(20,180)], "none", HID, 1.4, dashed=True))  # gespiegelt angedeutet
    s.append(T(132,62,"3 cm", SW, 12, anchor="middle"))
    s.append(T(ax-6,128,"5 cm", SW, 12, anchor="end"))
    s.append(f'<path d="M 70,212 A 60,16 0 0 0 120,212" fill="none" stroke="{ACCENT}" stroke-width="1.6"/>')
    s.append(f'<polygon points="120,212 113,208 113,217" fill="{ACCENT}"/>')
    s.append(T(ax,38,"Achse", ACCENT, 11, anchor="middle"))
    return wrap(200, 230, "".join(s))
F[8] = fig_rot_rect()

# 9) Rechtw. Dreieck rotiert um Kathete -> Kegel
def fig_rot_tri():
    ax=100
    s=[L(ax,50,ax,205, dashed=True, col=ACCENT, w=2)]
    s.append(P([(ax,70),(ax,180),(180,180)], FILL, SW, 2))
    s.append(rangle(ax,180,11, dx=1, dy=-1))
    s.append(T(ax-6,128,"6 cm", SW, 12, anchor="end"))
    s.append(T(140,196,"4 cm", SW, 12, anchor="middle"))
    s.append(f'<path d="M 78,212 A 55,15 0 0 0 122,212" fill="none" stroke="{ACCENT}" stroke-width="1.6"/>')
    s.append(f'<polygon points="122,212 115,208 115,217" fill="{ACCENT}"/>')
    s.append(T(ax,42,"Achse", ACCENT, 11, anchor="middle"))
    return wrap(210, 230, "".join(s))
F[9] = fig_rot_tri()

# 10) Halbkreis rotiert um Durchmesser -> Kugel
def fig_rot_semi():
    ax=110; cy=130; r=62
    s=[L(ax,50,ax,210, dashed=True, col=ACCENT, w=2)]
    s.append(f'<path d="M {ax},{cy-r} A {r},{r} 0 0 1 {ax},{cy+r} Z" fill="{FILL}" stroke="{SW}" stroke-width="2"/>')
    s.append(L(ax,cy,ax+r,cy, col=SW, w=1.4)); s.append(T(ax+r//2,cy-6,"r = 5 cm", SW, 12, anchor="middle"))
    s.append(f'<path d="M 86,222 A 50,14 0 0 0 130,222" fill="none" stroke="{ACCENT}" stroke-width="1.6"/>')
    s.append(f'<polygon points="130,222 123,218 123,227" fill="{ACCENT}"/>')
    s.append(T(ax,42,"Achse", ACCENT, 11, anchor="middle"))
    return wrap(220, 240, "".join(s))
F[10] = fig_rot_semi()

# 11) Stufenfigur rotiert -> zwei Zylinder
def fig_rot_step():
    ax=80
    s=[L(ax,45,ax,205, dashed=True, col=ACCENT, w=2)]
    s.append(P([(ax,190),(175,190),(175,160),(120,160),(120,80),(ax,80)], FILL, SW, 2))
    s.append(T(150,206,"r = 4", SW, 11, anchor="middle"))
    s.append(T(150,153,"r = 2", SW, 11, anchor="middle"))
    s.append(f'<path d="M 58,212 A 55,15 0 0 0 102,212" fill="none" stroke="{ACCENT}" stroke-width="1.6"/>')
    s.append(f'<polygon points="102,212 95,208 95,217" fill="{ACCENT}"/>')
    s.append(T(ax,38,"Achse", ACCENT, 11, anchor="middle"))
    return wrap(200, 230, "".join(s))
F[11] = fig_rot_step()

# 12) Würfelnetz mit Zahlen 1–6 (gegenüberliegende Flächen bestimmen)
def fig_cube_net_num():
    u=42; ox=68; oy=18
    cells={(1,0):"1",(0,1):"2",(1,1):"3",(2,1):"4",(1,2):"5",(1,3):"6"}
    s=[]
    for (c,r),num in cells.items():
        x,y=ox+c*u, oy+r*u
        s.append(f'<rect x="{x}" y="{y}" width="{u}" height="{u}" fill="{FILL}" stroke="{SW}" stroke-width="2"/>')
        s.append(f'<text x="{x+u/2}" y="{y+u/2+8}" font-size="22" fill="{SW}" text-anchor="middle" font-weight="bold">{num}</text>')
    return wrap(ox*2+3*u, oy*2+4*u, "".join(s))
F[12] = fig_cube_net_num()

# 13) Netz quadratische Pyramide, bemaßt (a, Dreieckshöhe)
def fig_pyr_net():
    sq=[(95,95),(175,95),(175,175),(95,175)]
    s=[P(sq, FILL)]
    top=[(95,95),(175,95),(135,30)]
    rgt=[(175,95),(175,175),(240,135)]
    bot=[(95,175),(175,175),(135,240)]
    lft=[(95,95),(95,175),(30,135)]
    for tri in (top,rgt,bot,lft):
        s.append(P(tri, "#f6fafc"))
    # Dreieckshöhe (Seitenhöhe) im oberen Dreieck
    s.append(L(135,95,135,30, dashed=True, col=HID, w=1.4))
    s.append(rangle(135,95,10))
    s.append(T(142,66,"5 cm", SW, 12))
    s.append(T(184,140,"6 cm", SW, 12))
    return wrap(275, 270, "".join(s))
F[13] = fig_pyr_net()

# 14) Netz Zylinder
def fig_cyl_net():
    s=[]
    s.append(f'<rect x="70" y="78" width="135" height="92" fill="{FILL}" stroke="{SW}" stroke-width="2"/>')
    s.append(E(137,52,24,12, "#f6fafc"))     # Deckfläche
    s.append(E(137,196,24,12, "#f6fafc"))    # Grundfläche
    s.append(L(70,170,205,170, col=HID, w=0))
    s.append(T(137,128,"Mantel", SW, 13, anchor="middle"))
    s.append(T(137,52,"", SW))
    s.append(T(137,55,"Kreis", SW, 11, anchor="middle"))
    s.append(T(137,199,"Kreis", SW, 11, anchor="middle"))
    s.append(L(70,180,205,180, dashed=True, col=HID, w=1.4))
    s.append(T(137,228,"Länge = ?", ACCENT, 13, anchor="middle", weight="bold"))
    return wrap(280, 245, "".join(s))
F[14] = fig_cyl_net()

# Figuren in Bilder/ schreiben
for n, svg in F.items():
    with open(os.path.join(IMG, f"Stereo-Aufgabe-{n:02d}.svg"), "w") as fh:
        fh.write(svg + "\n")
print("wrote", len(F), "SVGs")

# ---------------- HTML-Gerüst (aus build_html übernommen) ----------------
CSS = """<style>
 :root{{--teal:{accent};--tealdark:{accentdark};--line:#dde2e5;--red:#c0392b}}
 *{{box-sizing:border-box}} body{{font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0;padding:22px;background:#f4f6f7}}
 h1{{font-size:21px;margin:0 0 4px}} .sub{{color:#5b6569;font-size:13.5px;margin:0 0 16px;max-width:820px}}
 .controls{{position:sticky;top:0;background:#f4f6f7;padding:12px 0;border-bottom:1px solid var(--line);margin-bottom:18px;z-index:5;display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
 button{{font:inherit;font-weight:600;font-size:13.5px;padding:9px 15px;border-radius:9px;border:1px solid var(--line);background:#fff;color:#1a1a1a;cursor:pointer}}
 button:hover{{border-color:var(--teal);color:var(--teal)}}
 button.primary{{background:var(--teal);color:#fff;border-color:var(--teal)}} button.primary:hover{{background:var(--tealdark);color:#fff}}
 .count{{font-size:13px;color:#5b6569;margin-left:auto}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
 .card{{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:14px 16px;break-inside:avoid;display:flex;flex-direction:column}}
 .card.selected{{border-color:var(--teal);box-shadow:0 0 0 2px rgba(8,145,178,.18)}}
 .top{{display:flex;align-items:center;gap:12px;margin-bottom:6px}}
 .num{{font-weight:700;font-size:15px;margin-left:auto}}
 .sel{{font-size:12.5px;color:#5b6569;display:flex;align-items:center;gap:6px;cursor:pointer}} .sel input{{accent-color:var(--teal);width:16px;height:16px}}
 .fig{{display:flex;justify-content:center;align-items:center;padding:4px}} .fig svg{{display:block;max-width:100%;height:auto}}
 .ges{{font-size:14px;color:#1a1a1a;margin-top:6px;line-height:1.5}}
 .ges b{{color:var(--red)}}
 .soltgl{{align-self:flex-start;margin-top:10px;font-size:12.5px;padding:6px 12px}}
 .sol{{display:none;margin-top:10px;background:#f0f7fa;border:1px solid #c7e3ec;border-radius:9px;padding:10px 14px;font-size:13.5px;line-height:1.5}}
 .sol ul{{margin:4px 0;padding-left:20px}} .sol b{{color:#0e6f86}}
 .card.open .sol{{display:block}}
 @media (max-width:680px){{.grid{{grid-template-columns:1fr}}}}
 @page{{size:A4;margin:13mm}}
 @media print{{
   body{{background:#fff;padding:0}} .controls,.sub,.sel,.soltgl{{display:none !important}}
   .card{{border:1px solid #bbb;box-shadow:none}} .card.selected{{box-shadow:none}}
   .sol{{display:none !important}} .card.open .sol{{display:block !important}}
   body.selprint .card:not(.selected){{display:none !important}}
 }}
</style>"""

JS = """<script>
function tog(b){const c=b.closest('.card');const open=c.classList.toggle('open');const l=b.dataset.label||'Lösung';b.textContent=open?l+' ausblenden':l+' anzeigen';}
function allSol(v){document.querySelectorAll('.card').forEach(c=>{c.classList.toggle('open',v);const b=c.querySelector('.soltgl');const l=b.dataset.label||'Lösung';b.textContent=v?l+' ausblenden':l+' anzeigen';});}
function upd(){const n=document.querySelectorAll('.cb:checked').length;document.getElementById('count').textContent=n+' ausgewählt';}
document.addEventListener('change',e=>{if(e.target.classList.contains('cb')){e.target.closest('.card').classList.toggle('selected',e.target.checked);upd();}});
function clearSel(){document.querySelectorAll('.cb').forEach(cb=>{cb.checked=false;cb.closest('.card').classList.remove('selected');});upd();}
function printSel(){if(!document.querySelector('.cb:checked')){alert('Bitte zuerst Aufgaben auswählen (Häkchen setzen).');return;}document.body.classList.add('selprint');window.print();setTimeout(()=>document.body.classList.remove('selprint'),400);}
function printAll(){document.body.classList.remove('selprint');window.print();}
</script>"""

STARPRINT = """
 .stars{font-size:14px;letter-spacing:2px;color:#e8a800;margin-left:10px;white-space:nowrap}
 .stars .s0{color:#d4d8dc}
 /* PRINT3 */
 @media print{
   h1{display:none !important}
   .stars{display:none !important}
   .grid{grid-template-columns:1fr !important;gap:0 !important}
   .card{min-height:86mm;break-inside:avoid;page-break-inside:avoid;padding:7mm 9mm !important;margin:0 !important}
   .fig svg{max-height:40mm !important}
   .ges{min-height:0 !important}
 }
"""

def card(n, body, sol_html, label="Lösung"):
    return (f'<div class="card" data-n="{n}">\n'
            f' <div class="top"><label class="sel"><input type="checkbox" class="cb"> auswählen</label>'
            f'<span class="num">Aufgabe {n}</span></div>\n'
            f' {body}\n'
            f' <button class="soltgl" type="button" data-label="{label}" onclick="tog(this)">{label} anzeigen</button>\n'
            f' <div class="sol">{sol_html}</div>\n'
            f'</div>')

def stars(d):
    return (f'<span class="stars" title="Schwierigkeit {d} von 3">'
            + '★' * d + '<span class="s0">' + '★' * (3 - d) + '</span></span>')

def page(title, h1, sub, cards):
    controls = ('<div class="controls">\n'
        ' <button class="primary" type="button" onclick="printSel()">🖨️ Auswahl drucken</button>\n'
        ' <button type="button" onclick="printAll()">Alles drucken</button>\n'
        ' <button type="button" onclick="allSol(true)">Alle Lösungen anzeigen</button>\n'
        ' <button type="button" onclick="allSol(false)">Alle Lösungen ausblenden</button>\n'
        ' <button type="button" onclick="clearSel()">Auswahl zurücksetzen</button>\n'
        ' <span class="count" id="count">0 ausgewählt</span>\n</div>')
    return ('<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{title}</title>\n' + CSS.format(accent=ACCENT, accentdark=ACCENTDARK)
        + '</head><body>\n' + f'<h1>{h1}</h1>\n<p class="sub">{sub}</p>\n'
        + controls + '\n<div class="grid">' + ''.join(cards) + '</div>\n' + JS + '</body></html>')

# ---------------- Aufgaben ----------------
TASKS = [
 (1, 2, "<b>Aufgabe:</b> Quadratische Pyramide mit Grundkante a = 5 cm und Höhe h = 8 cm. "
        "<b>Ges.:</b> Grundfläche G, Seitenhöhe h<sub>s</sub> und Seitenkante s sowie Volumen V.",
   "<ul><li>G = a² = <b>25 cm²</b></li>"
   "<li>h<sub>s</sub> = √(h² + (a/2)²) = √(64 + 6,25) = √70,25 ≈ <b>8,38 cm</b></li>"
   "<li>s = √(h² + (½·a√2)²) = √(64 + 12,5) = √76,5 ≈ <b>8,75 cm</b></li>"
   "<li>V = ⅓·G·h = ⅓·25·8 ≈ <b>66,7 cm³</b></li></ul>"),
 (2, 3, "<b>Aufgabe:</b> Ein Würfel mit Kantenlänge a = 6 cm wird zentral mit einem zylindrischen Loch "
        "(Radius r = 1,5 cm) durchbohrt. <b>Ges.:</b> Volumen des Restkörpers.",
   "<ul><li>V<sub>Würfel</sub> = a³ = <b>216 cm³</b></li>"
   "<li>V<sub>Zylinder</sub> = π·r²·a = π·1,5²·6 = 13,5π ≈ <b>42,4 cm³</b></li>"
   "<li>V<sub>Rest</sub> = 216 − 42,4 ≈ <b>173,6 cm³</b></li></ul>"),
 (3, 3, "<b>Aufgabe:</b> Auf einem Zylinder (r = 4 cm, Höhe h<sub>Z</sub> = 6 cm) sitzt ein Kegel. "
        "Der Winkel zwischen Grundradius und Kegelseite beträgt ε = 50°. <b>Ges.:</b> Gesamtvolumen V.",
   "<ul><li>Kegelhöhe: h<sub>K</sub> = r·tan ε = 4·tan 50° ≈ <b>4,77 cm</b></li>"
   "<li>V<sub>Zyl</sub> = π·r²·h<sub>Z</sub> = π·16·6 = 96π ≈ 301,6 cm³</li>"
   "<li>V<sub>Kegel</sub> = ⅓·π·r²·h<sub>K</sub> = ⅓·π·16·4,77 ≈ 79,9 cm³</li>"
   "<li>V = 301,6 + 79,9 ≈ <b>381,5 cm³</b></li></ul>"),
 (4, 2, "<b>Aufgabe:</b> Ein gerades Prisma hat als Grundfläche ein rechtwinkliges Dreieck mit den "
        "Katheten 3 cm und 4 cm. Die Länge des Prismas beträgt 10 cm. <b>Ges.:</b> Volumen V und Oberfläche O.",
   "<ul><li>G = ½·3·4 = <b>6 cm²</b></li><li>V = G·l = 6·10 = <b>60 cm³</b></li>"
   "<li>Hypotenuse = 5 cm → Mantel = (3+4+5)·10 = 120 cm²</li>"
   "<li>O = 2·G + Mantel = 12 + 120 = <b>132 cm²</b></li></ul>"),
 (5, 1, "<b>Aufgabe:</b> Ein Zylinder hat r = 3 cm und Höhe h = 10 cm. <b>Ges.:</b> Volumen V und Oberfläche O.",
   "<ul><li>V = π·r²·h = π·9·10 = 90π ≈ <b>282,7 cm³</b></li>"
   "<li>O = 2π·r² + 2π·r·h = 18π + 60π = 78π ≈ <b>245,0 cm²</b></li></ul>"),
 (6, 2, "<b>Aufgabe:</b> Ein Kegel hat r = 6 cm und Höhe h = 8 cm. <b>Ges.:</b> Mantellinie s, Volumen V und Oberfläche O.",
   "<ul><li>s = √(r² + h²) = √(36 + 64) = <b>10 cm</b></li>"
   "<li>V = ⅓·π·r²·h = ⅓·π·36·8 = 96π ≈ <b>301,6 cm³</b></li>"
   "<li>O = π·r² + π·r·s = 36π + 60π = 96π ≈ <b>301,6 cm²</b></li></ul>"),
 (7, 1, "<b>Aufgabe:</b> Eine Kugel hat den Radius r = 6 cm. <b>Ges.:</b> Volumen V und Oberfläche O.",
   "<ul><li>V = ⁴⁄₃·π·r³ = ⁴⁄₃·π·216 = 288π ≈ <b>904,8 cm³</b></li>"
   "<li>O = 4·π·r² = 4π·36 = 144π ≈ <b>452,4 cm²</b></li></ul>"),
 (8, 1, "<b>Aufgabe:</b> Das Rechteck (3 cm × 5 cm) rotiert um die eingezeichnete Achse. "
        "Welcher Körper entsteht? Gib Maße und Volumen an.",
   "<ul><li>Es entsteht ein <b>Zylinder</b> (r = 3 cm, h = 5 cm).</li>"
   "<li>V = π·r²·h = π·9·5 = 45π ≈ <b>141,4 cm³</b></li></ul>"),
 (9, 2, "<b>Aufgabe:</b> Das rechtwinklige Dreieck rotiert um die Achse (Kathete). "
        "Welcher Körper entsteht? Gib Maße und Volumen an.",
   "<ul><li>Es entsteht ein <b>Kegel</b> (r = 4 cm, h = 6 cm).</li>"
   "<li>V = ⅓·π·r²·h = ⅓·π·16·6 = 32π ≈ <b>100,5 cm³</b></li></ul>"),
 (10, 2, "<b>Aufgabe:</b> Der Halbkreis (r = 5 cm) rotiert um die Achse (Durchmesser). "
         "Welcher Körper entsteht? Gib das Volumen an.",
   "<ul><li>Es entsteht eine <b>Kugel</b> (r = 5 cm).</li>"
   "<li>V = ⁴⁄₃·π·r³ = ⁴⁄₃·π·125 ≈ <b>523,6 cm³</b></li></ul>"),
 (11, 3, "<b>Aufgabe:</b> Die abgebildete Stufenfigur rotiert um die Achse "
         "(unten r = 4 cm, h = 2 cm; oben r = 2 cm, h = 5 cm). Welcher Körper entsteht? Gib das Volumen an.",
   "<ul><li>Es entsteht ein <b>abgesetzter Drehkörper aus zwei Zylindern</b> (unten breit, oben schmal).</li>"
   "<li>V = π·4²·2 + π·2²·5 = 32π + 20π = 52π ≈ <b>163,4 cm³</b></li></ul>"),
 (12, 3, "<b>Aufgabe:</b> Das abgebildete Würfelnetz ist mit den Zahlen 1 bis 6 beschriftet. "
         "Welche Zahlen liegen sich am fertig gefalteten Würfel jeweils gegenüber?",
   "<ul><li>Gegenüber liegen: <b>1 und 5</b>, <b>2 und 4</b>, <b>3 und 6</b>.</li>"
   "<li>Faustregel: Gegenüberliegende Flächen sind im Netz nie benachbart, sondern stets durch genau "
   "eine Fläche voneinander getrennt.</li></ul>"),
 (13, 3, "<b>Aufgabe:</b> Gegeben ist das Netz einer quadratischen Pyramide (Grundkante a = 6 cm, "
         "Dreieckshöhe h<sub>s</sub> = 5 cm). <b>a)</b> Welche Kanten treffen beim Zusammenfalten aufeinander? "
         "<b>b)</b> Berechne die Oberfläche aus dem Netz.",
   "<ul><li><b>a)</b> Je zwei benachbarte Dreiecksschenkel treffen aufeinander und bilden eine "
   "<b>Seitenkante s</b> der Pyramide (insgesamt 4 Seitenkanten).</li>"
   "<li><b>b)</b> O = G + M = a² + 4·(½·a·h<sub>s</sub>) = 36 + 4·15 = <b>96 cm²</b></li></ul>"),
 (14, 1, "<b>Aufgabe:</b> Das Netz eines Zylinders besteht aus den abgebildeten Teilen. Benenne die Teile. "
         "Wofür steht die Länge des Rechtecks?",
   "<ul><li>Zwei Kreise = <b>Grund- und Deckfläche</b>; das Rechteck = <b>Mantel</b>.</li>"
   "<li>Die Länge des Rechtecks entspricht dem <b>Umfang u = 2·π·r</b> des Kreises.</li>"
   "<li>Die Höhe des Rechtecks entspricht der Körperhöhe h.</li></ul>"),
 (15, 2, "<b>Aufgabe (mündlich):</b> Nenne die Volumenformeln von Prisma, Zylinder, Pyramide und Kegel "
         "und erkläre den Zusammenhang zwischen „Säulen“ und „Spitzkörpern“.",
   "<ul><li>Prisma: V = G·h &nbsp;|&nbsp; Zylinder: V = π·r²·h</li>"
   "<li>Pyramide: V = ⅓·G·h &nbsp;|&nbsp; Kegel: V = ⅓·π·r²·h</li>"
   "<li><b>Spitzkörper</b> (Pyramide, Kegel) haben genau <b>⅓</b> des Volumens des entsprechenden "
   "Säulenkörpers (Prisma, Zylinder) mit gleicher Grundfläche und Höhe.</li></ul>"),
]

cards = []
for n, d, ges, sol in TASKS:
    fig = f'<div class="fig">{F[n]}</div>\n ' if n in F else ''
    body = fig + f'<div class="ges">{ges}</div>'
    c = card(n, body, sol)
    c = c.replace(f'<span class="num">Aufgabe {n}</span></div>',
                  f'<span class="num">Aufgabe {n}</span>{stars(d)}</div>')
    cards.append(c)

html = page(
 "Stereometrie – Aufgabenpool mündliche Prüfung",
 "Stereometrie – Aufgabenpool",
 "Mündliche Prüfung Mathematik (Körperberechnung, Rotationskörper, Netze). Aufgaben mit dem Häkchen "
 "„auswählen“ markieren und <b>„Auswahl drucken“</b> – dann werden nur die markierten Aufgaben ohne "
 "Lösung gedruckt. <b>Formeln stehen bewusst nicht auf dem Aufgabenblatt</b> – die Schülerinnen und Schüler "
 "sollen die Formeln für Prismen und Spitzkörper auswendig kennen. Mit „Lösung anzeigen“ blendest du "
 "Formel und Rechenweg ein (nur für dich).",
 cards)
html = html.replace('</style>', STARPRINT + '</style>', 1)

with open(os.path.join(BASE, "Stereometrie Aufgabenpool.html"), "w") as f:
    f.write(html)
print("wrote Stereometrie Aufgabenpool.html")

# ---------------- Markdown ----------------
MD = [
 (1, "Quadratische Pyramide mit Grundkante a = 5 cm und Höhe h = 8 cm. **Ges.:** Grundfläche G, Seitenhöhe hₛ und Seitenkante s sowie Volumen V.",
   ["G = a² = **25 cm²**", "hₛ = √(h² + (a/2)²) = √70,25 ≈ **8,38 cm**",
    "s = √(h² + (½·a√2)²) = √76,5 ≈ **8,75 cm**", "V = ⅓·G·h = ⅓·25·8 ≈ **66,7 cm³**"]),
 (2, "Ein Würfel mit Kantenlänge a = 6 cm wird zentral mit einem zylindrischen Loch (r = 1,5 cm) durchbohrt. **Ges.:** Volumen des Restkörpers.",
   ["V_Würfel = a³ = **216 cm³**", "V_Zylinder = π·r²·a = 13,5π ≈ **42,4 cm³**", "V_Rest = 216 − 42,4 ≈ **173,6 cm³**"]),
 (3, "Auf einem Zylinder (r = 4 cm, h_Z = 6 cm) sitzt ein Kegel. Winkel zwischen Grundradius und Kegelseite ε = 50°. **Ges.:** Gesamtvolumen V.",
   ["h_K = r·tan ε = 4·tan 50° ≈ **4,77 cm**", "V_Zyl = π·16·6 = 96π ≈ 301,6 cm³",
    "V_Kegel = ⅓·π·16·4,77 ≈ 79,9 cm³", "V ≈ **381,5 cm³**"]),
 (4, "Gerades Prisma, Grundfläche rechtwinkliges Dreieck mit Katheten 3 cm und 4 cm, Länge 10 cm. **Ges.:** Volumen V und Oberfläche O.",
   ["G = ½·3·4 = **6 cm²**", "V = G·l = 6·10 = **60 cm³**",
    "Hypotenuse 5 cm → Mantel = (3+4+5)·10 = 120 cm²", "O = 2·6 + 120 = **132 cm²**"]),
 (5, "Zylinder mit r = 3 cm und h = 10 cm. **Ges.:** Volumen V und Oberfläche O.",
   ["V = π·9·10 = 90π ≈ **282,7 cm³**", "O = 2π·9 + 2π·30 = 78π ≈ **245,0 cm²**"]),
 (6, "Kegel mit r = 6 cm und h = 8 cm. **Ges.:** Mantellinie s, Volumen V und Oberfläche O.",
   ["s = √(36+64) = **10 cm**", "V = ⅓·π·36·8 = 96π ≈ **301,6 cm³**", "O = π·36 + π·6·10 = 96π ≈ **301,6 cm²**"]),
 (7, "Kugel mit r = 6 cm. **Ges.:** Volumen V und Oberfläche O.",
   ["V = ⁴⁄₃·π·216 = 288π ≈ **904,8 cm³**", "O = 4π·36 = 144π ≈ **452,4 cm²**"]),
 (8, "Das Rechteck (3 cm × 5 cm) rotiert um die eingezeichnete Achse. Welcher Körper entsteht? Maße und Volumen?",
   ["Es entsteht ein **Zylinder** (r = 3 cm, h = 5 cm).", "V = π·9·5 = 45π ≈ **141,4 cm³**"]),
 (9, "Das rechtwinklige Dreieck rotiert um die Achse (Kathete). Welcher Körper entsteht? Maße und Volumen?",
   ["Es entsteht ein **Kegel** (r = 4 cm, h = 6 cm).", "V = ⅓·π·16·6 = 32π ≈ **100,5 cm³**"]),
 (10, "Der Halbkreis (r = 5 cm) rotiert um die Achse (Durchmesser). Welcher Körper entsteht? Volumen?",
   ["Es entsteht eine **Kugel** (r = 5 cm).", "V = ⁴⁄₃·π·125 ≈ **523,6 cm³**"]),
 (11, "Die Stufenfigur rotiert um die Achse (unten r = 4 cm, h = 2 cm; oben r = 2 cm, h = 5 cm). Welcher Körper entsteht? Volumen?",
   ["Es entsteht ein **abgesetzter Drehkörper aus zwei Zylindern**.", "V = π·16·2 + π·4·5 = 52π ≈ **163,4 cm³**"]),
 (12, "Das abgebildete Würfelnetz ist mit 1–6 beschriftet. Welche Zahlen liegen sich am gefalteten Würfel gegenüber?",
   ["Gegenüber: **1 & 5**, **2 & 4**, **3 & 6**.", "Gegenüberliegende Flächen sind im Netz nie benachbart, sondern durch genau eine Fläche getrennt."]),
 (13, "Netz einer quadratischen Pyramide (a = 6 cm, Dreieckshöhe hₛ = 5 cm). **a)** Welche Kanten treffen beim Falten aufeinander? **b)** Berechne die Oberfläche.",
   ["a) Je zwei benachbarte Dreiecksschenkel bilden eine **Seitenkante s** (insgesamt 4).",
    "b) O = a² + 4·(½·a·hₛ) = 36 + 60 = **96 cm²**"]),
 (14, "Netz eines Zylinders. Benenne die Teile. Wofür steht die Länge des Rechtecks?",
   ["Zwei Kreise = Grund-/Deckfläche, Rechteck = **Mantel**.", "Länge des Rechtecks = **Umfang u = 2·π·r**, Höhe = Körperhöhe h."]),
 (15, "**(mündlich)** Nenne die Volumenformeln von Prisma, Zylinder, Pyramide und Kegel und erkläre den Zusammenhang Säule ↔ Spitzkörper.",
   ["Prisma V = G·h | Zylinder V = π·r²·h", "Pyramide V = ⅓·G·h | Kegel V = ⅓·π·r²·h",
    "**Spitzkörper = ⅓** des Volumens des entsprechenden Säulenkörpers (gleiche Grundfläche und Höhe)."]),
]

md = ["---", "tags: [mathematik, pruefung, stereometrie, geometrie, koerper, aufgabenpool]",
      "date: 2026-06-25", "---", "",
      "# Stereometrie – Aufgabenpool mündliche Prüfung", "",
      "15 Aufgaben zur Raumgeometrie: Körperberechnung (Prisma, Zylinder, Pyramide, Kegel, Kugel, "
      "zusammengesetzte Körper), **Rotationskörper** (welcher Körper entsteht beim Drehen um die Achse?) "
      "und **Netze/Falten** (welcher Körper entsteht, welche Kanten treffen sich?). Die Figuren liegen als "
      "`.svg` im Ordner `Bilder/`.", "",
      "> [!important] Formeln nicht auf dem Blatt", "> Die Formeln für **Prismen und Spitzkörper** stehen "
      "bewusst **nicht** auf den Aufgaben – die Schülerinnen und Schüler sollen sie auswendig kennen. "
      "In den Lösungen (nur für dich) sind Formel und Rechenweg angegeben.", "",
      "Eine interaktive Variante zum Auswählen und Drucken liegt als `Stereometrie Aufgabenpool.html` daneben. "
      "Siehe auch [[Trigonometrie Prüfungspool]], [[Boxplot Aufgabenpool]] und [[Quadratische Funktionen Aufgabenpool]].",
      "", "---", ""]
diff = {t[0]: t[1] for t in TASKS}
for n, ges, sols in MD:
    md.append(f"## Aufgabe {n}")
    md.append(f"*Schwierigkeit: {'★'*diff[n]}{'☆'*(3-diff[n])}*")
    if n in F:
        md.append(f"![[Stereo-Aufgabe-{n:02d}.svg]]")
    md.append(ges)
    md.append("> [!tip]- Lösung")
    for line in sols:
        md.append(f"> {line}")
    md.append("")
with open(os.path.join(BASE, "Stereometrie Aufgabenpool.md"), "w") as f:
    f.write("\n".join(md))
print("wrote Stereometrie Aufgabenpool.md")
print("done")
