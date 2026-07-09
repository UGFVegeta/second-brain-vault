#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Baut den 7. Pool "Kurzaufgaben (Zeitfüller)" – HTML + .md.
# Kurze Zusatzaufgaben für die letzten Minuten der mündlichen Prüfung.
import os
BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben"

# ---- Mathe-Helfer (HTML) ----
def sqrt(x): return f'<span class="rad">√<span class="rdc">{x}</span></span>'
def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def sup(b, e): return f'{b}<sup>{e}</sup>'
BOX = '<span class="box"></span>'
def expr(html): return f'<div class="kexpr">{html}</div>'

# ---- Aufgaben ----
# Felder: n, d(iff), prompt, body(HTML nach prompt), sol(HTML), md_body, md_sol
tasks = [
 dict(n=1, d=1, prompt="Welcher Sinuswert ist positiv, welcher negativ? Kreuzen Sie an.",
   body='<table class="kt"><tr><th></th><th>positiv</th><th>negativ</th></tr>'
        f'<tr><td>sin 25°</td><td>{BOX}</td><td>{BOX}</td></tr>'
        f'<tr><td>sin 125°</td><td>{BOX}</td><td>{BOX}</td></tr>'
        f'<tr><td>sin 225°</td><td>{BOX}</td><td>{BOX}</td></tr></table>',
   sol="sin 25° → <b>positiv</b>, sin 125° → <b>positiv</b>, sin 225° → <b>negativ</b>. "
       "(25° und 125° liegen oberhalb der Grundlinie/Mittellinie, 225° darunter.)",
   md_body="| | positiv | negativ |\n|---|---|---|\n| sin 25° | ☐ | ☐ |\n| sin 125° | ☐ | ☐ |\n| sin 225° | ☐ | ☐ |",
   md_sol="sin 25° → **positiv**, sin 125° → **positiv**, sin 225° → **negativ**. (25° und 125° oberhalb der Mittellinie, 225° darunter.)"),
 dict(n=2, d=1, prompt="Was ist größer?", body=expr("sin 40° &nbsp;oder&nbsp; sin 80°"),
   sol="<b>sin 80°</b> ist größer. Im Bereich 0°–90° wächst der Sinus mit dem Winkel.",
   md_body="$\\sin 40^\\circ$ &nbsp;oder&nbsp; $\\sin 80^\\circ$",
   md_sol="**sin 80°** ist größer (im Bereich 0°–90° wächst der Sinus)."),
 dict(n=3, d=1, prompt="Was ist größer?", body=expr("cos 20° &nbsp;oder&nbsp; cos 70°"),
   sol="<b>cos 20°</b> ist größer. Im Bereich 0°–90° fällt der Kosinus mit wachsendem Winkel.",
   md_body="$\\cos 20^\\circ$ &nbsp;oder&nbsp; $\\cos 70^\\circ$",
   md_sol="**cos 20°** ist größer (im Bereich 0°–90° fällt der Kosinus)."),
 dict(n=4, d=2, prompt="Was ist größer?", body=expr("sin 30° &nbsp;oder&nbsp; cos 60°"),
   sol="<b>Beide sind gleich groß:</b> sin 30° = cos 60° = 0,5.",
   md_body="$\\sin 30^\\circ$ &nbsp;oder&nbsp; $\\cos 60^\\circ$",
   md_sol="**Gleich groß:** sin 30° = cos 60° = 0,5."),
 dict(n=5, d=2, prompt="Welche Zahl muss eingesetzt werden?",
   body=expr(f'{sqrt("32")} · {sqrt(BOX)} − {sqrt("25")} = 3'),
   sol=f'{sqrt("32")}·{sqrt(BOX)} = 8 ⟹ 32·☐ = 64 ⟹ <b>☐ = 2</b>. (Probe: √64 − 5 = 8 − 5 = 3.)',
   md_body="$\\sqrt{32}\\cdot\\sqrt{\\square}-\\sqrt{25}=3$",
   md_sol="$\\sqrt{32}\\cdot\\sqrt{\\square}=8 \\Rightarrow 32\\cdot\\square=64 \\Rightarrow \\square=2$. (Probe: √64 − 5 = 3.)"),
 dict(n=6, d=1, prompt="Welche Zahl muss eingesetzt werden?",
   body=expr(f'{sqrt(BOX)} + {sqrt("9")} = 7'),
   sol=f'{sqrt(BOX)} = 7 − 3 = 4 ⟹ <b>☐ = 16</b>.',
   md_body="$\\sqrt{\\square}+\\sqrt{9}=7$",
   md_sol="$\\sqrt{\\square}=7-3=4 \\Rightarrow \\square=16$."),
 dict(n=7, d=2, prompt="Welche Zahl muss eingesetzt werden?",
   body=expr(f'{sqrt("48")} : {sqrt(BOX)} = 4'),
   sol=f'{sqrt("48 : ☐")} = 4 ⟹ 48 : ☐ = 16 ⟹ <b>☐ = 3</b>.',
   md_body="$\\sqrt{48}:\\sqrt{\\square}=4$",
   md_sol="$\\sqrt{48:\\square}=4 \\Rightarrow 48:\\square=16 \\Rightarrow \\square=3$."),
 dict(n=8, d=1, prompt="Berechnen Sie den Term.", body=expr(f'58·{sup("10","4")} + 42·{sup("10","4")}'),
   sol=f'= (58 + 42)·{sup("10","4")} = 100·{sup("10","4")} = {sup("10","6")} = 1 000 000.',
   md_body="$58\\cdot10^4+42\\cdot10^4$",
   md_sol="$=(58+42)\\cdot10^4=100\\cdot10^4=10^6=1\\,000\\,000$."),
 dict(n=9, d=2, prompt="Schreiben Sie in wissenschaftlicher Schreibweise (Zehnerpotenz).",
   body=expr("0,00045"), sol=f'= 4,5·{sup("10","−4")}.',
   md_body="$0{,}00045$", md_sol="$=4{,}5\\cdot10^{-4}$."),
 dict(n=10, d=1, prompt="Schreiben Sie als Dezimalzahl.", body=expr(f'3,2·{sup("10","5")}'),
   sol="= 320 000.", md_body="$3{,}2\\cdot10^5$", md_sol="$=320\\,000$."),
 dict(n=11, d=1, prompt="Schreiben Sie in wissenschaftlicher Schreibweise.", body=expr("73 000 000"),
   sol=f'= 7,3·{sup("10","7")}.', md_body="$73\\,000\\,000$", md_sol="$=7{,}3\\cdot10^7$."),
 dict(n=12, d=3, prompt="Lösen Sie die Gleichung.", body=expr("(x − 3)(x + 5) + 7 = 8(x − 2)"),
   sol="x² + 2x − 15 + 7 = 8x − 16 ⟹ x² + 2x − 8 = 8x − 16 ⟹ x² − 6x + 8 = 0 ⟹ "
       "(x − 2)(x − 4) = 0 ⟹ <b>x₁ = 2; x₂ = 4</b>.",
   md_body="$(x-3)(x+5)+7=8(x-2)$",
   md_sol="$x^2+2x-8=8x-16 \\Rightarrow x^2-6x+8=0 \\Rightarrow (x-2)(x-4)=0 \\Rightarrow x_1=2;\\ x_2=4$."),
 dict(n=13, d=1, prompt="Lösen Sie die Gleichung.", body=expr("3x + 7 = 5x − 9"),
   sol="7 + 9 = 5x − 3x ⟹ 16 = 2x ⟹ <b>x = 8</b>.",
   md_body="$3x+7=5x-9$", md_sol="$16=2x \\Rightarrow x=8$."),
 dict(n=14, d=2, prompt="Lösen Sie die Gleichung.", body=expr("2(x + 4) = 3x − 1"),
   sol="2x + 8 = 3x − 1 ⟹ 8 + 1 = 3x − 2x ⟹ <b>x = 9</b>.",
   md_body="$2(x+4)=3x-1$", md_sol="$2x+8=3x-1 \\Rightarrow x=9$."),
 dict(n=15, d=2, prompt="Berechnen Sie mit einer binomischen Formel.", body=expr(f'{sup("102","2")}'),
   sol=f'(100 + 2)² = {sup("100","2")} + 2·100·2 + {sup("2","2")} = 10000 + 400 + 4 = <b>10404</b>.',
   md_body="$102^2$", md_sol="$(100+2)^2=10000+400+4=10404$."),
 dict(n=16, d=2, prompt="Multiplizieren Sie aus (binomische Formel).", body=expr(f'{sup("(3x − 2)","2")}'),
   sol=f'= {sup("9x","2")} − 12x + 4.',
   md_body="$(3x-2)^2$", md_sol="$=9x^2-12x+4$."),
 dict(n=17, d=2, prompt="Berechnen Sie geschickt (binomische Formel).", body=expr("49 · 51"),
   sol=f'= (50 − 1)(50 + 1) = {sup("50","2")} − {sup("1","2")} = 2500 − 1 = <b>2499</b>.',
   md_body="$49\\cdot51$", md_sol="$=(50-1)(50+1)=2500-1=2499$."),
 dict(n=18, d=3, prompt="Weisen Sie nach, dass gilt:",
   body=expr(f'{frac(sup("10","6"), sup("5","4") + "·" + sup("5","2"))} : {sup("2","4")} = 4'),
   sol=f'{sup("5","4")}·{sup("5","2")} = {sup("5","6")}; &nbsp; {sup("10","6")} : {sup("5","6")} = '
       f'{sup("(10:5)","6")} = {sup("2","6")}; &nbsp; {sup("2","6")} : {sup("2","4")} = {sup("2","2")} = 4. ✓',
   md_body="$\\dfrac{10^6}{5^4\\cdot5^2}:2^4=4$",
   md_sol="$5^4\\cdot5^2=5^6;\\ \\dfrac{10^6}{5^6}=\\left(\\dfrac{10}{5}\\right)^6=2^6;\\ 2^6:2^4=2^2=4$ ✓"),
 dict(n=19, d=1, prompt="Berechnen Sie.", body=expr(f'{sup("2","3")} · {sup("2","4")}'),
   sol=f'= {sup("2","7")} = 128.', md_body="$2^3\\cdot2^4$", md_sol="$=2^7=128$."),
 dict(n=20, d=1, prompt="Berechnen Sie.", body=expr(f'{sup("3","5")} : {sup("3","3")}'),
   sol=f'= {sup("3","2")} = 9.', md_body="$3^5:3^3$", md_sol="$=3^2=9$."),
]

def sh(d): return "★"*d + '<span class="s0">' + "★"*(3-d) + "</span>"
def sm(d): return "★"*d + "☆"*(3-d)

MATH_CSS = """
 .kq{font-size:14px;font-weight:600;color:#1a1a1a}
 .kexpr{font-size:19px;text-align:center;margin:12px 0 2px;line-height:1.9}
 .rad{white-space:nowrap}
 .rad .rdc{border-top:1.6px solid currentColor;padding:1px 5px 0}
 .frac{display:inline-flex;flex-direction:column;text-align:center;vertical-align:middle;margin:0 4px}
 .frac .n{border-bottom:1.6px solid currentColor;padding:0 7px}
 .frac .d{padding:0 7px}
 .box{display:inline-block;width:15px;height:15px;border:1.6px solid #333;vertical-align:-2px;margin:0 3px}
 .kt{border-collapse:collapse;margin:10px auto 2px;font-size:14px}
 .kt td,.kt th{border:1px solid #c4ccd4;padding:4px 16px;text-align:center}
 .kt th{background:#eef2f6;font-weight:700}
 .kt td:first-child{text-align:left;font-weight:600}
"""

CSS = """
 :root{--teal:#be185d;--tealdark:#9d174d;--line:#dde2e5;--red:#c0392b}
 *{box-sizing:border-box} body{font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0;padding:22px;background:#f4f6f7}
 h1{font-size:21px;margin:0 0 4px} .sub{color:#5b6569;font-size:13.5px;margin:0 0 16px;max-width:820px}
 .controls{position:sticky;top:0;background:#f4f6f7;padding:12px 0;border-bottom:1px solid var(--line);margin-bottom:18px;z-index:5;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
 button{font:inherit;font-weight:600;font-size:13.5px;padding:9px 15px;border-radius:9px;border:1px solid var(--line);background:#fff;color:#1a1a1a;cursor:pointer}
 button:hover{border-color:var(--teal);color:var(--teal)}
 button.primary{background:var(--teal);color:#fff;border-color:var(--teal)} button.primary:hover{background:var(--tealdark);color:#fff}
 .count{font-size:13px;color:#5b6569;margin-left:auto}
 .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
 .card{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:14px 16px;break-inside:avoid;display:flex;flex-direction:column}
 .card.selected{border-color:var(--teal);box-shadow:0 0 0 2px rgba(190,24,93,.18)}
 .top{display:flex;align-items:center;gap:12px;margin-bottom:6px}
 .num{font-weight:700;font-size:15px;margin-left:auto}
 .sel{font-size:12.5px;color:#5b6569;display:flex;align-items:center;gap:6px;cursor:pointer} .sel input{accent-color:var(--teal);width:16px;height:16px}
 .soltgl{align-self:flex-start;margin-top:10px;font-size:12.5px;padding:6px 12px}
 .sol{display:none;margin-top:10px;background:#fdf2f8;border:1px solid #f4c6dd;border-radius:9px;padding:10px 14px;font-size:13.5px;line-height:1.6}
 .card.open .sol{display:block} .sol b{color:#1a1a1a}
""" + MATH_CSS + """
 @media (max-width:680px){.grid{grid-template-columns:1fr}}
 @page{size:A4;margin:13mm}
 @media print{
   body{background:#fff;padding:0} .controls,.sub,.sel,.soltgl{display:none !important}
   .card{border:1px solid #bbb;box-shadow:none} .card.selected{box-shadow:none}
   .sol{display:none !important} .card.open .sol{display:block !important}
   body.selprint .card:not(.selected){display:none !important}
 }
 .stars{font-size:14px;letter-spacing:2px;color:#e8a800;margin-left:10px;white-space:nowrap}
 .stars .s0{color:#d4d8dc}
 @media print{
   .stars{display:none !important}
   h1{display:none !important}
   .grid{grid-template-columns:1fr !important;gap:0 !important}
   .card{min-height:60mm !important;break-inside:avoid;page-break-inside:avoid;padding:7mm 9mm !important;margin:0 !important}
 }
 .drawbox{display:flex;gap:7px;align-items:center;padding:0 12px 0 2px;border-right:1px solid var(--line);margin-right:4px;flex-wrap:wrap}
 .dlabel{font-size:13px;color:#5b6569;font-weight:700}
 .dsel{font:inherit;font-size:13px;padding:7px 9px;border-radius:8px;border:1px solid var(--line);background:#fff}
 .drawbtn{background:var(--teal);color:#fff;border-color:var(--teal)}
 .drawbtn:hover{background:var(--tealdark);color:#fff}
 @media print{.drawbox{display:none !important}}
"""

JS = """<script>
function tog(b){const c=b.closest('.card');const open=c.classList.toggle('open');const l=b.dataset.label||'Lösung';b.textContent=open?l+' ausblenden':l+' anzeigen';}
function allSol(v){document.querySelectorAll('.card').forEach(c=>{c.classList.toggle('open',v);const b=c.querySelector('.soltgl');const l=b.dataset.label||'Lösung';b.textContent=v?l+' ausblenden':l+' anzeigen';});}
function upd(){const n=document.querySelectorAll('.cb:checked').length;document.getElementById('count').textContent=n+' ausgewählt';}
document.addEventListener('change',e=>{if(e.target.classList.contains('cb')){e.target.closest('.card').classList.toggle('selected',e.target.checked);upd();}});
function clearSel(){document.querySelectorAll('.cb').forEach(cb=>{cb.checked=false;cb.closest('.card').classList.remove('selected');});upd();}
function printSel(){if(!document.querySelector('.cb:checked')){alert('Bitte zuerst Aufgaben auswählen (Häkchen setzen).');return;}document.body.classList.add('selprint');window.print();setTimeout(()=>document.body.classList.remove('selprint'),400);}
function printAll(){document.body.classList.remove('selprint');window.print();}
function drawTasks(n){
 if(typeof clearSel==='function')clearSel();
 var sel=document.getElementById('diffsel');
 var diff=sel?(parseInt(sel.value)||0):0;
 var cards=[].slice.call(document.querySelectorAll('.card'));
 var pool=cards.filter(function(c){return diff===0||parseInt(c.dataset.diff)===diff;});
 for(var i=pool.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=pool[i];pool[i]=pool[j];pool[j]=t;}
 var pick=pool.slice(0,n);
 pick.forEach(function(c){var cb=c.querySelector('.cb');if(cb)cb.checked=true;c.classList.add('selected');});
 if(typeof upd==='function')upd();
 if(pick.length){pick[0].scrollIntoView({behavior:'smooth',block:'center'});}
 if(pick.length<n){alert('Nur '+pick.length+' Aufgabe(n) mit dieser Schwierigkeit vorhanden.');}
}
window.addEventListener('DOMContentLoaded',function(){
 var p=new URLSearchParams(location.search);
 if(p.has('draw')){var d=p.get('diff');var sel=document.getElementById('diffsel');if(d!==null&&sel)sel.value=d;drawTasks(parseInt(p.get('draw'))||6);}
});
</script></body></html>"""

HEAD = ('<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
 '<title>Kurzaufgaben – Aufgabenpool mündliche Prüfung</title>\n<style>' + CSS + '</style></head><body>\n'
 '<h1>Kurzaufgaben (Zeitfüller)</h1>\n'
 '<p class="sub">Kurze Zusatzaufgaben für die <b>letzten Minuten</b> der mündlichen Prüfung – wenn noch Zeit ist, '
 'kann man dem Prüfling schnell eine kleine Aufgabe hinlegen. Themen: Sinus/Kosinus (Vorzeichen &amp; Vergleich), '
 'Wurzeln ergänzen, wissenschaftliche Schreibweise, Gleichungen, binomische Formeln, Potenzgesetze. '
 'Mit Häkchen „auswählen“ markieren und <b>„Auswahl drucken“</b> – gedruckt wird ohne Lösung.</p>\n'
 '<div class="controls">\n'
 '  <span class="drawbox" id="drawpanel"><span class="dlabel">Prüfung:</span>'
 '<select id="diffsel" class="dsel"><option value="0">alle Schwierigkeiten</option><option value="1">★ leicht</option>'
 '<option value="2">★★ mittel</option><option value="3">★★★ schwer</option></select>'
 '<button type="button" class="drawbtn" onclick="drawTasks(6)">🎲 6 Aufgaben ziehen</button></span>\n'
 ' <button class="primary" type="button" onclick="printSel()">🖨️ Auswahl drucken</button>\n'
 ' <button type="button" onclick="printAll()">Alles drucken</button>\n'
 ' <button type="button" onclick="allSol(true)">Alle Lösungen anzeigen</button>\n'
 ' <button type="button" onclick="allSol(false)">Alle Lösungen ausblenden</button>\n'
 ' <button type="button" onclick="clearSel()">Auswahl zurücksetzen</button>\n'
 ' <span class="count" id="count">0 ausgewählt</span>\n'
 '</div>\n<div class="grid">')

cards = ""
for t in tasks:
    cards += ('<div class="card" data-n="%d" data-diff="%d">\n' % (t["n"], t["d"])
      + ' <div class="top"><label class="sel"><input type="checkbox" class="cb"> auswählen</label>'
      + '<span class="num">Aufgabe %d</span>' % t["n"]
      + '<span class="stars" title="Schwierigkeit %d von 3">%s</span></div>\n' % (t["d"], sh(t["d"]))
      + ' <div class="kq">%s</div>\n' % t["prompt"]
      + ' %s\n' % t["body"]
      + ' <button class="soltgl" type="button" data-label="Lösung" onclick="tog(this)">Lösung anzeigen</button>\n'
      + ' <div class="sol">%s</div>\n' % t["sol"]
      + '</div>')

open(os.path.join(BASE, "Kurzaufgaben Aufgabenpool.html"), "w").write(HEAD + cards + "</div>\n" + JS)
print("wrote Kurzaufgaben Aufgabenpool.html  (%d Aufgaben)" % len(tasks))

# ---- Markdown ----
md = ("---\ntags: [mathematik, pruefung, kurzaufgaben, zeitfueller, aufgabenpool]\ndate: 2026-06-30\n---\n\n"
 "# Kurzaufgaben (Zeitfüller)\n\n"
 "20 **kurze Zusatzaufgaben** für die letzten Minuten der mündlichen Prüfung. Keine vollwertigen Aufgaben, "
 "sondern schnelle Aufgaben, die man dem Prüfling hinlegen kann, wenn noch ein wenig Zeit ist. "
 "Themen: Sinus/Kosinus (Vorzeichen & Vergleich), Wurzeln ergänzen, wissenschaftliche Schreibweise, "
 "Gleichungen, binomische Formeln, Potenzgesetze.\n\n---\n")
for t in tasks:
    md += "\n## Aufgabe %d\n" % t["n"]
    md += "*Schwierigkeit: %s*\n\n" % sm(t["d"])
    md += "**%s**\n\n" % t["prompt"]
    md += "%s\n\n" % t["md_body"]
    md += "> [!tip]- Lösung\n> %s\n" % t["md_sol"]
open(os.path.join(BASE, "Kurzaufgaben Aufgabenpool.md"), "w").write(md.rstrip() + "\n")
print("wrote Kurzaufgaben Aufgabenpool.md")
