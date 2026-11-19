"""Präsentation zum Rezept Trigonometrie (Kurzfassung), Mathe 10b, Fr 20.11.2026, 1. Stunde (45 min).
Oskar 19.11.: Rezept per Klick aufdecken: erst 0, 1, 2 (gilt für alles), dann der Ja-Weg, danach der Nein-Weg;
rechts daneben läuft parallel das passende Beispiel. Die Klasse schreibt das Rezept von der Tafel ab, danach
rechnet Oskar die Aufgabe im Prüfungsstil in Notability vor (Klasse zeichnet ab und schreibt mit).
Hausaufgabe bis Mo 23.11.: Buch S. 16 Nr. 3 a und 4 a (linke Spalte), für Schnelle Nr. 4 b (links).

Das Flussdiagramm kommt aus der Excalidraw-Datei (Kurzfassung); die Teile werden über Gruppen und
Pfeilverbindungen erkannt, damit Änderungen in Obsidian erhalten bleiben. Folientechnik aus den Bausteinen
(Seitenleiste, Countdown-Uhr) in 04 Ressourcen/Lernwissenschaft & Pädagogik.
Ausführen: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 baue_praesentation_rezept.py
"""
import json
import re
import sys
import tempfile
from pathlib import Path

from baue_loesung_s15_s16 import ROT, C, S, k, i, Skizze, dreieck, fuss
from baue_rezept_trigo import BLAU, EXCALIDRAW_KURZ, sk_a, ga_b, hb, a_b, b_b

HIER = Path(__file__).parent
VAULT = HIER.parents[2]
NAME = "Mathe 10b – Rezept Trigonometrie – Präsentation"
BAU = VAULT / "04 Ressourcen/Lernwissenschaft & Pädagogik"
sys.path.insert(0, str(VAULT / ".scripts"))
from mindmap_excalidraw import svg_schreiben  # noqa: E402

TEILE = {"s0", "s1", "s2", "s3", "s4", "nein", "ja", "ff", "fertig", "zurueck", "p01", "p12", "pja", "pnein",
         "pja3", "pnein3", "p34", "p4f", "pfertig", "pzurueck"}


# ---------------------------------------------------------------- Flussdiagramm in Teile zerlegen
def teile_zuordnen(E):
    """Teil-Namen über Gruppen (s0 … s4, nein) und Pfeilverbindungen; schreibt customData.teil (nur im Speicher)."""
    teil = {}
    for e in E:
        for g in e.get("groupIds") or []:
            if g in ("s0", "s1", "s2", "s3", "s4", "nein"):
                teil[e["id"]] = g
    pfeile = [e for e in E if e["type"] == "arrow"]
    ende = lambda a, s: (a.get(s + "Binding") or {}).get("elementId")
    label = {e["containerId"]: e["text"].strip() for e in E if e["type"] == "text" and e.get("containerId")}
    for _ in range(3):
        for a in pfeile:
            ts, z = teil.get(ende(a, "start")), ende(a, "end")
            lab = label.get(a["id"], "")
            if z in teil or not z:
                continue
            if ts == "s2" and lab == "Ja":
                teil[z] = "ja"
            elif ts == "s4":
                teil[z] = "ff"
            elif ts == "ff":
                teil[z] = "fertig" if lab == "Ja" else "zurueck"
    namen = {("s0", "s1"): "p01", ("s1", "s2"): "p12", ("s2", "ja"): "pja", ("s2", "nein"): "pnein",
             ("ja", "s3"): "pja3", ("nein", "s3"): "pnein3", ("s3", "s4"): "p34", ("s4", "ff"): "p4f",
             ("ff", "fertig"): "pfertig", ("ff", "zurueck"): "pzurueck"}
    for a in pfeile:
        n = namen.get((teil.get(ende(a, "start")), teil.get(ende(a, "end"))))
        if n:
            teil[a["id"]] = n
    for e in E:
        if e["type"] == "text" and e.get("containerId") in teil:
            teil[e["id"]] = teil[e["containerId"]]
    fehlt = TEILE - set(teil.values())
    assert not fehlt, f"Im Excalidraw nicht gefunden: {fehlt}"
    for e in E:
        if e["id"] in teil:
            e["customData"] = {"teil": teil[e["id"]]}
    return E


def fluss_svg(nr):
    E = [e for e in json.loads(EXCALIDRAW_KURZ.read_text(encoding="utf-8"))["elements"] if not e.get("isDeleted")]
    teile_zuordnen(E)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "f.svg"
        svg_schreiben(E, p, gruppen=True)
        svg = p.read_text(encoding="utf-8")
    svg = re.sub(r'width="\d+" height="\d+"', 'class="fluss"', svg, count=1)
    return svg.replace('id="m"', f'id="m{nr}"').replace("url(#m)", f"url(#m{nr})")   # Pfeilspitze je Folie eigen


# ---------------------------------------------------------------- Beispiele
SUB = lambda t: f"<tspan font-size='2.2' dy='0.8'>{t}</tspan>"


def br(z, n):
    return f'<span class="br"><span>{z}</span><span>{n}</span></span>'


def erg(t):
    return f'<b class="erg">{t}</b>'


def um(t):
    return f'<span class="um">| {t}</span>'


def z(nr, inhalt, zeige="", hl="", mit=""):
    """Eine Zeile im Beispiel = ein Klick. nr: Schritt aus dem Rezept oder '?' für die Fertig-Frage."""
    badge = f'<span class="nr">{nr}</span>' if nr != "?" else '<span class="nr frage">?</span>'
    a = f' data-zeige="{zeige}"' if zeige else ""
    a += f' data-hl="{hl}"' if hl else ""
    a += f' data-mit="{mit}"' if mit else ""
    return f'<div class="zl" data-step{a}>{badge}<div>{inhalt}</div></div>'


hb_ = i("h", "b")

# Oskar 19.11.: links nur bis „rechtwinklig? Ja“, dann rechts genauso weit bis „Nein“; nur rechts wird fertig gerechnet.
ZEILEN_A = [
    z(0, "Werte eintragen;<br>gesucht α, β, b rot", hl="s0", mit="skA"),
    z(1, "nur γ = 90° bekannt", hl="s1"),
    z(2, "rechtwinklig? <b>Ja</b>:<br>sin, cos oder tan", zeige="pja ja", hl="s2 ja"),
]
ZEILEN_B = [
    z(0, "Werte eintragen;<br>gesucht a rot", hl="s0", mit="skB0"),
    z(1, f"γ = 180° − 50,0° − 70,0°<br>{erg(f'γ = {k(ga_b)}°')}", hl="s1"),
    z(2, f"rechtwinklig? <b>Nein</b>:<br>Höhe {hb_} einzeichnen<br><span class='erg'>nicht {i('h', 'c')}: c ist die einzige<br>bekannte Seite</span>",
      zeige="pnein nein", hl="s2 nein", mit="skB1"),
    z(3, f"sin 50,0° = {br(hb_, '9,0')} {um('⋅ 9,0')}", zeige="pja3 pnein3 s3", hl="s3"),
    z(4, f"{hb_} = 9,0 ⋅ sin 50,0°<br>{erg(f'{hb_} = {k(hb)} cm')}", zeige="p34 s4", hl="s4"),
    z("?", "<b>Nein</b>: zurück zu 1", zeige="p4f ff pzurueck zurueck", hl="ff zurueck"),
    z(3, f"sin {k(ga_b)}° = {br(k(hb), 'a')} {um(f'a ↔ sin {k(ga_b)}°')}", hl="s3"),
    z(4, f"a = {br(k(hb), f'sin {k(ga_b)}°')}<br>{erg(f'a = {k(a_b)} cm')}", hl="s4"),
    z("?", "<b>Ja</b>: fertig", zeige="pfertig fertig", hl="ff fertig"),
]


def sk_b_praes(hoehe):
    """Beispiel (b) in der Präsentation: gesucht nur a; mit hoehe=True die Höhe h_b mit Fußpunkt F."""
    P = dreieck((0, 0), (9.0, 0), (b_b * C(50), b_b * S(50)))
    A, B, Cc = P["A"], P["B"], P["C"]
    s = Skizze(P, breite=66, hoehe=64)
    if hoehe:
        F = fuss(B, A, Cc)
        s.linie(B, F, BLAU, 0.6, "1.4,0.9"); s.rechter(F, A, B, r=3.4)
        s.seite(B, F, "h" + SUB("b"), BLAU, aussen=False, ab=2.6, pos=0.5)
        x, y = s.m(*F); s.text(x - 3.2, y - 1.5, "F", gr=3.0)
    s.seite(A, B, "9,0 cm"); s.seite(B, Cc, "a", ROT, fett=True)
    s.winkel(A, B, Cc, "50,0°", r=5, rt=10.5); s.winkel(B, A, Cc, "", r=5); bx, by = s.m(*B); s.text(bx + 1, by - 9, "70,0°", gr=2.8)
    for n in "ABC": s.ecke(n)
    return s.svg()


def panel(seite, titel, aufgabe, skizzen, zeilen, mitname):
    sk = "".join(f'<div class="mit" data-name="{n}">{svg}</div>' for n, svg in skizzen)
    return (f'<div class="bsp {seite}"><div class="mit kopfteil" data-name="{mitname}"><div class="kicker">{titel}</div>'
            f'<div class="aufg">{aufgabe}</div></div><div class="skizze">{sk}</div>'
            f'<div class="zeilen">{"".join(zeilen)}</div></div>')


def folien():
    mitte = (f'<div class="mitte"><h1>Rezept für Trigonometrie</h1>{fluss_svg(1)}'
             '<span data-step data-zeige="s0" data-hl="s0"></span>'
             '<span data-step data-zeige="p01 s1" data-hl="s1"></span>'
             '<span data-step data-zeige="p12 s2" data-hl="s2"></span></div>')
    # Reihenfolge im Aufbau = Klickreihenfolge: erst Rezept 0 bis 2, dann Beispiel Ja, dann Beispiel Nein (Spalten per CSS)
    rezept = ('<section class="slide drei" data-tab="Rezept mit zwei Beispielen" data-group="" data-basis="">' + mitte
              + panel("links", "Ja: rechtwinklig", "Gegeben: a = 5,0 cm; c = 9,0 cm<br>γ = 90°; gesucht: α, β, b",
                      [("skA", sk_a())], ZEILEN_A, "skA")
              + panel("rechts", "Nein: nicht rechtwinklig", "Gegeben: c = 9,0 cm<br>α = 50,0°; β = 70,0°; gesucht: a",
                      [("skB0", sk_b_praes(False)), ("skB1", sk_b_praes(True))], ZEILEN_B, "skB0")
              + "</section>")
    ha = ('<section class="slide ha" data-tab="Hausaufgabe" data-group="">'
          '<div class="kicker">Bis Montag, 23.11.</div><h1>Hausaufgabe</h1>'
          '<ul><li>Arbeitsblatt Rückseite: Höhe einzeichnen, Nr. 1 bis 10</li>'
          '<li class="klein2">Nie die einzige bekannte Seite teilen!</li></ul></section>')
    return rezept + ha


# ---------------------------------------------------------------- Überblick
def ueberblick():
    return ('<div class="page"><h1>Mathe 10b, Fr 20.11.2026: Rezept für Trigonometrie</h1>'
            '<p class="sub">Stand laut Vertretung: S. 16 Nr. 3 c und die Prüfungsaufgabe 2022 A2/1 gemeinsam gerechnet '
            '(Rest Hausaufgabe), allein war es noch zu schwierig.</p>'
            '<h2>Ablauf</h2><ol>'
            '<li>Rezept per Klick: erst 0, 1, 2. Links Beispiel (a) bis „rechtwinklig? Ja“, rechts Beispiel (b) bis „Nein“; danach nur rechts fertig rechnen.</li>'
            '<li>Die Klasse schreibt das Rezept von der Tafel ins Merkheft ab.</li>'
            '<li>Aufgabe im Prüfungsstil gemeinsam in Notability, die Klasse zeichnet ab und schreibt mit.</li>'
            '<li>Arbeitsblatt Vorderseite üben (Nr. 1 bis 14); Hausaufgabe Rückseite (zweite Folie).</li></ol>'
            '<h2>Hausaufgabe bis Mo 23.11.</h2><p>Arbeitsblatt Rückseite: 10 Dreiecke, Höhe einzeichnen. Lösung: <a href="Mathe 10b – Arbeitsblatt sin, cos, tan üben und Höhe einzeichnen – Lösung.pdf">Arbeitsblatt Lösung</a>, Seite 2.</p>'
            '<h2>Material</h2><ul>'
            '<li><a href="Mathe 10b – Rezept Trigonometrie – Aufgabe im Prüfungsstil.pdf">Aufgabe im Prüfungsstil (Seite 1 Notability, Seite 2 Lösung)</a></li>'
            '<li><a href="Mathe 10b – Rezept Trigonometrie – Kurzfassung zum Mitschreiben.pdf">Kurzfassung als PDF</a></li>'
            '</ul></div>')


# ---------------------------------------------------------------- HTML
def baustein(ordner, datei):
    return (BAU / ordner / datei).read_text(encoding="utf-8")


CSS = """
:root{ --ink:#1c2230; --bg:#ffffff; --accent:#2563a8; --accent2:#2563a8; --muted:#6b7280; --line:#d9dee7; }
*{box-sizing:border-box; margin:0; padding:0}
html,body{min-height:100%}
body{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif; color:var(--ink); background:#e9edf3}
#tabs{display:flex; gap:8px; padding:12px 18px; background:#fff; border-bottom:1px solid var(--line); position:sticky; top:0; z-index:9}
#tabs button{font:inherit; font-size:15px; border:1px solid var(--line); background:#fff; padding:7px 16px; border-radius:20px; cursor:pointer}
#tabs button.on{background:var(--accent); border-color:var(--accent); color:#fff}
.panel{display:none} .panel.on{display:block}
.page{max-width:980px; margin:24px auto; background:#fff; padding:28px 34px; border-radius:12px; line-height:1.5}
.page h1{font-size:24px; margin-bottom:6px} .page h2{font-size:18px; margin:22px 0 6px} .page .sub{color:var(--muted)}
.page ul{margin-left:20px}
.abl{border-collapse:collapse; width:100%; font-size:14.5px} .abl td,.abl th{border-bottom:1px solid var(--line); padding:7px 8px; text-align:left; vertical-align:top}
.abl td:first-child{white-space:nowrap; font-weight:700}
#p-folien{padding:14px}
#stage{container-type:size; position:relative; width:min(100%, calc((100vh - 130px) * 16 / 9)); aspect-ratio:16/9;
  background:var(--bg); border-radius:14px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.3); outline:none}
.slide{position:absolute; inset:0; padding:2cqw 3cqw; display:none}
.slide.active{display:flex} .slide.drei.active{display:grid}
[data-step]{opacity:0; transition:opacity .28s} [data-step].shown{opacity:1}
.kicker{font-size:1.15cqw; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); font-weight:700; margin-bottom:.8cqw}
#counter{position:absolute; bottom:1.2cqw; right:2cqw; font-size:1cqw; color:var(--muted)}
.ctrl{display:flex; gap:8px; align-items:center; font-size:13px; color:var(--muted)}
.ctrl button{font:inherit; padding:6px 12px; border:1px solid var(--line); border-radius:8px; background:#fff; cursor:pointer}
/* Rezept-Folie: Flussdiagramm in der Mitte, links Beispiel Ja (rechtwinklig), rechts Beispiel Nein */
.drei{grid-template-columns:1fr auto 1fr; gap:1.6cqw; padding:1.6cqw 2cqw}
.mitte{display:flex; flex-direction:column; align-items:center}
.mitte{grid-column:2; grid-row:1} .bsp.links{grid-column:1; grid-row:1} .bsp.rechts{grid-column:3; grid-row:1}
.mitte h1{font-size:2.3cqw; line-height:1.1; margin-bottom:.4cqw; color:var(--accent)}
.mitte svg.fluss{height:49cqw; width:auto; display:block}
.bsp{min-width:0; display:flex; flex-direction:column}
.kopfteil{opacity:0; transition:opacity .28s} .kopfteil.an{opacity:1}
.aufg{font-size:1.3cqw; line-height:1.4}
.skizze{position:relative; height:11cqw; margin:.4cqw 0 .5cqw}
.skizze .mit{position:absolute; inset:0; background:#fff; opacity:0; transition:opacity .28s; display:flex; justify-content:center}
.skizze .mit.an{opacity:1}
.skizze svg{height:100%; width:auto}
.zl{display:grid; grid-template-columns:2.4cqw 1fr; align-items:start; font-size:1.25cqw; line-height:1.38; margin-bottom:.32cqw}
.nr{display:inline-flex; width:1.9cqw; height:1.9cqw; border-radius:50%; background:var(--accent); color:#fff; font-weight:700;
    font-size:1.1cqw; align-items:center; justify-content:center}
.nr.frage{background:#b45309; border-radius:.3cqw; transform:rotate(45deg) scale(.82); font-size:0}
.nr.frage::after{content:"?"; font-size:1.3cqw; transform:rotate(-45deg)}
.erg{color:#c2185b} .um{color:#777; font-size:.88em; margin-left:.5cqw}
.br{display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; font-size:.9em; line-height:1.1; margin:0 .3cqw}
.br span:first-child{border-bottom:.12cqw solid #222; padding:0 .3cqw}
/* Teile des Flussdiagramms: verdeckt, aufgedeckt, gerade dran */
g[data-teil]{transition:opacity .35s}
g[data-teil].weg{opacity:0}
g[data-teil].hl{filter:drop-shadow(0 0 10px rgba(245,158,11,1)) drop-shadow(0 0 4px rgba(245,158,11,1))}
/* Hausaufgabe */
.ha{flex-direction:column; justify-content:center; padding:4cqw 7cqw}
.ha h1{font-size:4.2cqw; margin-bottom:1.5cqw}
.ha ul{font-size:2.6cqw; line-height:1.7; margin:0 0 1.5cqw 3cqw} .ha .klein2{font-size:2cqw; color:var(--muted)}
"""

JS_KERN = """
  const tabBtns=[...document.querySelectorAll('#tabs button')];
  function tab(name){
    tabBtns.forEach(b=>b.classList.toggle('on', b.dataset.tab===name));
    document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on', p.id==='p-'+name));
    try{ history.replaceState(null,'','#'+name); }catch(e){}
    if(name==='folien') stage.focus();
  }
  tabBtns.forEach(b=>b.addEventListener('click',()=>tab(b.dataset.tab)));
  const stage=document.getElementById('stage');
  const slides=[...document.querySelectorAll('.slide')];
  const counter=document.getElementById('counter');
  let i=0, stepIdx=0;
"""

JS_REST = """
  const steps = n => [...slides[n].querySelectorAll('[data-step]')];
  /* Rezept: Teile des Flussdiagramms aufdecken und hervorheben, Skizzen im Beispiel wechseln */
  function rezeptSync(){
    const s=slides[i], svg=s.querySelector('svg.fluss');
    const sichtbar=new Set((s.dataset.basis||'').split(' ').filter(Boolean)), mit=new Set();
    let hl='';
    steps(i).forEach((el,k)=>{ if(k<stepIdx){
      (el.dataset.zeige||'').split(' ').filter(Boolean).forEach(t=>sichtbar.add(t));
      (el.dataset.mit||'').split(' ').filter(Boolean).forEach(t=>mit.add(t));
      if(el.dataset.hl) hl=el.dataset.hl; } });
    const hls=hl.split(' ');
    if(svg) svg.querySelectorAll('g[data-teil]').forEach(g=>{ g.classList.toggle('weg', !sichtbar.has(g.dataset.teil)); g.classList.toggle('hl', hls.includes(g.dataset.teil)); });
    s.querySelectorAll('.mit').forEach(el=>el.classList.toggle('an', mit.has(el.dataset.name)));
  }
  function applySteps(){
    steps(i).forEach((el,k)=>el.classList.toggle('shown', k < stepIdx));
    const n=steps(i).length;
    counter.textContent=(i+1)+' / '+slides.length+(n?'  –  '+stepIdx+'/'+n:'');
    rezeptSync();
  }
  function show(n, revealAll){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach((s,k)=>s.classList.toggle('active',k===i));
    stepIdx = revealAll ? steps(i).length : 0;
    applySteps(); updSide();
  }
  function next(){ if(stepIdx < steps(i).length){ stepIdx++; applySteps(); return; } show(i+1,false); }
  function prev(){ if(stepIdx > 0){ stepIdx--; applySteps(); return; } show(i-1,true); }
  function toggleFs(){ if(!document.fullscreenElement) present.requestFullscreen(); else document.exitFullscreen(); }
  document.addEventListener('keydown',e=>{
    if(!document.getElementById('p-folien').classList.contains('on')) return;
    const k=e.key;
    if(k==='ArrowRight'||k===' '||k==='PageDown'){next();e.preventDefault();}
    else if(k==='ArrowLeft'||k==='PageUp'){prev();e.preventDefault();}
    else if(k==='ArrowDown'){tabStep(1);e.preventDefault();}
    else if(k==='ArrowUp'){tabStep(-1);e.preventDefault();}
    else if(k.toLowerCase()==='a'){show(i,true);e.preventDefault();}
    else if(k==='Home')show(0,false);
    else if(k==='End')show(slides.length-1,true);
    else if(k.toLowerCase()==='f'){ toggleFs(); }
    else if(k.toLowerCase()==='t'){ present.classList.toggle('nav-aus'); e.preventDefault(); }
  });
  stage.addEventListener('click',e=>{ const r=stage.getBoundingClientRect(); (e.clientX-r.left) < r.width/2 ? prev() : next(); });
  document.getElementById('prev').addEventListener('click',prev);
  document.getElementById('next').addEventListener('click',next);
  document.getElementById('fs').addEventListener('click',toggleFs);
  show(0,false);
  tab(location.hash==='#ueberblick'?'ueberblick':'folien');
"""


def baue():
    css = CSS + baustein("Baustein Seitenleiste", "seitenleiste-baustein.css")
    js = (JS_KERN + baustein("Baustein Seitenleiste", "seitenleiste-baustein.js")
          + "  function tabStep(d){ const ti=Math.max(0,Math.min(tabs.length-1,slides[i]._tab+d)); show(tabs[ti].idx[0],false); }\n"
          + JS_REST)
    if "function tabStep" in baustein("Baustein Seitenleiste", "seitenleiste-baustein.js"):
        js = js.replace("  function tabStep(d){ const ti=Math.max(0,Math.min(tabs.length-1,slides[i]._tab+d)); show(tabs[ti].idx[0],false); }\n", "", 1)
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{NAME}</title>'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><style>{css}</style></head><body>'
            '<div id="tabs"><button data-tab="ueberblick">Überblick</button><button data-tab="folien">Folien</button></div>'
            f'<div class="panel" id="p-ueberblick">{ueberblick()}</div>'
            '<div class="panel" id="p-folien"><div id="present"><nav id="side" aria-label="Abschnitte"></nav><div id="stagecol">'
            f'<div id="stage" tabindex="0">{folien()}<div id="dots"></div><div id="counter"></div></div>'
            '<div class="ctrl"><button id="prev">◀ zurück</button><button id="next">weiter ▶</button><button id="fs">Vollbild (F)</button>'
            '<span>Klick rechts oder → deckt den nächsten Schritt auf, ↑↓ Abschnitt, A zeigt alles, T Leiste</span></div>'
            '</div></div></div>'
            f'<script>{js}</script></body></html>')


if __name__ == "__main__":
    h = HIER / f"{NAME}.html"
    h.write_text(baue(), encoding="utf-8")
    print(h.name, f"{h.stat().st_size // 1024} KB")
