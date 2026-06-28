#!/usr/bin/env python3
# Fügt jedem Aufgabenpool-HTML einen "Prüfung"-Generator hinzu:
#   Schwierigkeit wählen -> 6 zufällige Aufgaben ziehen (markieren) -> "Auswahl drucken".
# Versteht auch URL-Parameter ?draw=6&diff=2 (von der index.html). Idempotent.
import os

BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik Prüfungsaufgaben"

diffs = {
 "Trigonometrie Aufgabenpool.html": {1:2,2:1,3:2,4:3,5:3,6:2,7:1,8:1,9:2,10:2,11:2,12:1,13:3,14:3},
 "Quadratische Funktionen Aufgabenpool.html": {1:2,2:3,3:1,4:1,5:2,6:2,7:2,8:2,9:2,10:1,11:1,12:2,13:2,14:2,15:3},
 "Stochastik Aufgabenpool.html": {1:2,2:2,3:1,4:2,5:3,6:1,7:3,8:2,9:2,10:1,11:1,12:2,13:3,14:3,15:2},
 "Sachrechnen Aufgabenpool.html": {1:1,2:3,3:2,4:1,5:2,6:1,7:2,8:2,9:3,10:2,11:2,12:1,13:3,14:1,15:3},
 "Boxplot Aufgabenpool.html": {1:2,2:2,3:1,4:2,5:3,6:3,7:3,8:2,9:2,10:2,11:1,12:3,13:2,14:2,15:2},
 "Stereometrie Aufgabenpool.html": {1:2,2:3,3:3,4:2,5:1,6:2,7:1,8:1,9:2,10:2,11:3,12:3,13:3,14:1,15:2},
}

PANEL = ('<span class="drawbox" id="drawpanel">'
  '<span class="dlabel">Prüfung:</span>'
  '<select id="diffsel" class="dsel">'
  '<option value="0">alle Schwierigkeiten</option>'
  '<option value="1">★ leicht</option>'
  '<option value="2">★★ mittel</option>'
  '<option value="3">★★★ schwer</option>'
  '</select>'
  '<button type="button" class="drawbtn" onclick="drawTasks(6)">🎲 6 Aufgaben ziehen</button>'
  '</span>')

DRAW_CSS = """
 .drawbox{display:flex;gap:7px;align-items:center;padding:0 12px 0 2px;border-right:1px solid var(--line);margin-right:4px;flex-wrap:wrap}
 .dlabel{font-size:13px;color:#5b6569;font-weight:700}
 .dsel{font:inherit;font-size:13px;padding:7px 9px;border-radius:8px;border:1px solid var(--line);background:#fff}
 .drawbtn{background:var(--teal);color:#fff;border-color:var(--teal)}
 .drawbtn:hover{background:var(--tealdark);color:#fff}
 @media print{.drawbox{display:none !important}}
"""

DRAW_JS = """
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
"""

for fn, dmap in diffs.items():
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        print("FEHLT:", fn); continue
    with open(p) as f:
        html = f.read()
    if 'id="drawpanel"' in html:
        print("skip (schon vorhanden):", fn); continue
    # data-diff an jede Karte
    added = 0
    for n, d in dmap.items():
        needle = f'data-n="{n}">'
        if needle in html:
            html = html.replace(needle, f'data-n="{n}" data-diff="{d}">', 1)
            added += 1
        else:
            print(f"  WARN: data-n={n} nicht gefunden in {fn}")
    # Panel in die Steuerleiste
    html = html.replace('<div class="controls">', '<div class="controls">\n  ' + PANEL, 1)
    # CSS
    html = html.replace('</style>', DRAW_CSS + '</style>', 1)
    # JS vor das letzte </script>
    idx = html.rfind('</script>')
    if idx != -1:
        html = html[:idx] + DRAW_JS + html[idx:]
    else:
        print("  WARN: kein </script> in", fn)
    with open(p, "w") as f:
        f.write(html)
    print(f"patched: {fn} (data-diff: {added}/{len(dmap)})")
print("done")
