"""Gemeinsame Übersichtsseite für alle Stunden eines Themas: links die Stunden nach Gruppen, rechts die gewählte Stunde (iframe).
Genutzt von Kernphysik/baue_uebersicht_k10.py und Optik/baue_uebersicht_optik.py.
Ein Eintrag: {"id": "W04", "marke": "W04", "titel": ..., "sub": ..., "datum": "ab 05.10.2026", "datei": "…html" oder "", "art": ""|"ka"|"offen"}"""
import html, json
from pathlib import Path


def baue_uebersicht(ziel, titel, untertitel, gruppen, links, speicher_key):
    """gruppen: [(Gruppentitel, [Einträge])], links: [(Text, Pfad)]"""
    alle = [e for _, liste in gruppen for e in liste]
    nav = ""
    for gt, liste in gruppen:
        nav += f'<div class="gruppe">{html.escape(gt)}</div>'
        for e in liste:
            leer = not e.get("datei")
            cls = "eintrag" + (" leer" if leer else "") + (" ka" if e.get("art") == "ka" else "")
            klein = e.get("datum", "") or ("noch nicht vorbereitet" if e.get("art") == "offen" else "")
            nav += (f'<button class="{cls}" data-w="{e["id"]}"{" disabled" if leer else ""}>'
                    f'<span class="w">{html.escape(e["marke"])}</span><span class="t">{html.escape(e["titel"])}'
                    f'{f"<small>{html.escape(klein)}</small>" if klein else ""}</span></button>')
    lk = "".join(f'<a href="{html.escape(h)}" target="_blank">{html.escape(t)}</a>' for t, h in links)
    daten = json.dumps([{"w": e["id"], "marke": e["marke"], "titel": e["titel"], "sub": e.get("sub", ""), "datei": e.get("datei", "")} for e in alle],
                       ensure_ascii=False)
    seite = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titel)}</title>
<style>
:root{{--bg:#F4F6F9;--panel:#FFFFFF;--ink:#14171c;--muted:#66798E;--line:#D9DFE7;--accent:#2F5E9E;--sel:#E3EBF6;--ka:#E6007E}}
*{{box-sizing:border-box}}html,body{{margin:0;height:100%}}
body{{background:var(--bg);color:var(--ink);font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;display:grid;grid-template-columns:300px 1fr;height:100vh}}
aside{{background:var(--panel);border-right:1px solid var(--line);overflow:auto;padding:14px 10px 20px}}
aside h1{{font-size:17px;margin:2px 8px 2px}}aside .sub{{font-size:12px;color:var(--muted);margin:0 8px 10px}}
.gruppe{{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin:14px 8px 4px}}
.eintrag{{display:flex;gap:10px;align-items:flex-start;width:100%;text-align:left;border:0;background:none;padding:7px 8px;border-radius:7px;cursor:pointer;font:inherit;color:inherit}}
.eintrag:hover{{background:#EEF2F7}}.eintrag.on{{background:var(--sel)}}
.eintrag .w{{font:600 12px ui-monospace,Menlo,monospace;color:var(--accent);padding-top:2px;min-width:34px}}
.eintrag .t{{font-size:14px;line-height:1.3}}.eintrag small{{display:block;font-size:11px;color:var(--muted);margin-top:1px}}
.eintrag.ka .w{{color:var(--ka)}}.eintrag.leer{{opacity:.5;cursor:default}}.eintrag.leer:hover{{background:none}}
.mehr{{margin:18px 8px 0;border-top:1px solid var(--line);padding-top:10px}}.mehr a{{display:block;font-size:13px;color:var(--accent);text-decoration:none;padding:4px 0}}
.mehr a:hover{{text-decoration:underline}}
main{{display:flex;flex-direction:column;min-width:0}}
.leiste{{display:flex;align-items:center;gap:10px;padding:8px 14px;background:var(--panel);border-bottom:1px solid var(--line)}}
.leiste .info{{flex:1;min-width:0}}.leiste b{{font-size:15px}}.leiste span{{display:block;font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.leiste button,.leiste a{{font:inherit;font-size:13px;border:1px solid var(--line);background:#fff;border-radius:7px;padding:6px 10px;cursor:pointer;color:var(--ink);text-decoration:none}}
.leiste button:disabled{{opacity:.4;cursor:default}}
iframe{{flex:1;border:0;width:100%;background:#fff}}
.leer-hinweis{{flex:1;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:15px}}[hidden]{{display:none!important}}
@media (max-width:800px){{body{{grid-template-columns:1fr;grid-template-rows:auto 1fr;height:auto}}aside{{max-height:40vh}}main{{height:80vh}}}}
</style></head><body>
<aside><h1>{html.escape(titel)}</h1><p class="sub">{html.escape(untertitel)}</p>{nav}
<div class="mehr">{lk}</div></aside>
<main><div class="leiste"><div class="info"><b id="titel"></b><span id="sub"></span></div>
<button id="zurueck" title="Pfeil links">← Vorherige</button><button id="weiter" title="Pfeil rechts">Nächste →</button><a id="neu" target="_blank">In neuem Tab</a></div>
<iframe id="rahmen" title="Stunde"></iframe><div class="leer-hinweis" id="leer" hidden>Diese Stunde ist noch nicht vorbereitet.</div></main>
<script>
const D={daten};
const knoepfe=[...document.querySelectorAll('.eintrag')], pos=w=>D.findIndex(x=>x.w===w);
let akt=null;
function zeige(w){{
  const s=D.find(x=>x.w===w); if(!s) return; akt=s;
  knoepfe.forEach(k=>k.classList.toggle('on',k.dataset.w===w));
  document.getElementById('titel').textContent=s.marke+' · '+s.titel;
  document.getElementById('sub').textContent=s.sub;
  const r=document.getElementById('rahmen'), leer=document.getElementById('leer'), neu=document.getElementById('neu');
  if(s.datei){{ r.hidden=false; leer.hidden=true; r.src=encodeURI(s.datei); neu.href=encodeURI(s.datei); neu.style.visibility='visible'; }}
  else {{ r.hidden=true; leer.hidden=false; neu.style.visibility='hidden'; }}
  const i=pos(w);
  document.getElementById('zurueck').disabled=!D.slice(0,i).some(x=>x.datei); document.getElementById('weiter').disabled=!D.slice(i+1).some(x=>x.datei);
  try{{ localStorage.setItem('{speicher_key}',w); }}catch(e){{}}
  history.replaceState(null,'','#'+w);
}}
function schritt(d){{ const i=pos(akt.w); const z=d>0?D.slice(i+1).find(x=>x.datei):D.slice(0,i).reverse().find(x=>x.datei); if(z) zeige(z.w); }}
knoepfe.forEach(k=>k.addEventListener('click',()=>zeige(k.dataset.w)));
document.getElementById('zurueck').onclick=()=>schritt(-1);
document.getElementById('weiter').onclick=()=>schritt(1);
document.addEventListener('keydown',e=>{{ if(e.key==='ArrowRight') schritt(1); if(e.key==='ArrowLeft') schritt(-1); }});
let start=location.hash.slice(1); if(!D.some(x=>x.w===start)){{ try{{ start=localStorage.getItem('{speicher_key}')||''; }}catch(e){{ start=''; }} }}
zeige(D.some(x=>x.w===start&&x.datei)?start:D.find(x=>x.datei).w);
</script></body></html>"""
    Path(ziel).write_text(seite, encoding="utf-8")
    print("geschrieben:", Path(ziel).name, "·", sum(1 for e in alle if e.get("datei")), "Stunden verlinkt")
