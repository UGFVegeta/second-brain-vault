"""Mathe-Vorbereitung als eine Datei pro Woche, Aufbau wie die Optik-Stunden F3 bis F5 (echte Tabs).
Tabs: Überblick (Vorbereiten, kurzer Verlauf der Woche mit Zeitleiste), Folien, Tafelbild, Merkheft, Lösungen.
Die Woche läuft durch: Stundengrenzen sind nur grobe Marken, weil eine Stunde nicht immer sauber abschließt.
Das Seiten-CSS kommt aus Physik/Optik/stunde_vorlage.py (gleiches Aussehen wie Physik)."""
import ast, sys
from pathlib import Path

MATHE = Path(__file__).parent
sys.path.insert(0, str(MATHE.parent / "Physik" / "Optik"))
from stunde_vorlage import CSS as OPTIK_CSS  # noqa: E402

EXTRA = """<style>
.tag{margin:18px 0 6px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#66798e;border-top:1px dashed #cfd6df;padding-top:10px}
.tag:first-of-type{border-top:0;padding-top:0}
.fkarte{border:2px solid #1b1b1b;border-radius:10px;padding:14px 20px 10px;margin:8px 0 22px;background:#fff}
.fkarte h3{margin:0 0 10px;font-size:22px}.fnr{font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#66798e;margin-top:18px}
.lsg{color:#E6007E;font-weight:700}.offen{color:#8da6c2;font-style:italic}
.br{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.85em;line-height:1.05;margin:0 .1em}
.br span:first-child{border-bottom:1.5px solid currentColor;padding:0 .15em}
.spalten{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.spalten h4{margin:0 0 6px}.spalten ol{margin:0;padding-left:22px}.spalten li{margin:4px 0}
.kl{columns:2;column-gap:40px;font-size:18px}
.tagwahl{display:flex;gap:8px;flex-wrap:wrap;position:sticky;top:52px;background:#fff;padding:10px 0;z-index:3;border-bottom:1px solid #e3e5ea}
.tagwahl button{font:inherit;font-size:15px;font-weight:600;border:1px solid #cfd6df;background:#fff;border-radius:18px;padding:6px 16px;cursor:pointer}
.tagwahl button.on{background:#1b1b1b;color:#fff;border-color:#1b1b1b}.tagwahl button span{font-weight:400;opacity:.7}
[hidden]{display:none!important}.ausdruck{font-size:26px;font-weight:700;margin:8px 0}
.heft{border-left:5px solid #1b1b1b;padding:4px 0 4px 14px;margin:12px 0}.uheft{border-left:5px dashed #1a56a0;padding:4px 0 4px 14px;margin:12px 0}
.merk{background:#eef3fb;border:1.5px solid #1a56a0;border-radius:6px;padding:8px 13px;margin:9px 0;font-weight:600}
.tafel{background:#fbfbf8;border:1px solid #d9dfe7;border-radius:8px;padding:12px 16px;margin:10px 0 18px}
figure{margin:8px 0}figure svg{display:block;max-width:100%;height:auto}
table.ha{border-collapse:collapse;width:100%}.ha td{border-bottom:1px solid #e3e5ea;padding:6px 8px;vertical-align:top}
</style>"""


def aus_skript(datei, *namen):
    """Holt Funktionen und einfache Konstanten aus einem Bauskript, ohne es auszuführen (die Skripte schreiben beim Import Dateien)."""
    baum = ast.parse(Path(datei).read_text(encoding="utf-8"))
    def literal(n):
        try:
            ast.literal_eval(n.value)
            return True
        except ValueError:
            return False
    teile = [n for n in baum.body if isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom))
             or (isinstance(n, ast.Assign) and literal(n))]
    ns = {}
    exec(compile(ast.Module(body=teile, type_ignores=[]), str(datei), "exec"), ns)
    return [ns[n] for n in namen]


def bau_woche(ziel, h1, sub, vorbereiten, schritte, folien, tafel, merkheft, loesungen, extra_css="", verlauf="Die Stunde"):
    """vorbereiten: [(Wann, Was)] oder HTML; schritte: [(Tag-Marke oder "", Titel, Minuten, Text, [Foliennummern])];
    folien: [(Titel, HTML)] oder nach Tagen [(Tag, [(Titel, HTML)])]. Bei Tagen zählt jeder Tag ab Folie 1, und die
    Foliennummern eines Schritts beziehen sich auf den Tag, zu dem der Schritt gehört (Reihenfolge der Tag-Marken).
    tafel, merkheft, loesungen: HTML."""
    if folien and isinstance(folien[0][1], list):
        gruppen = folien
    else:
        gruppen = [("", folien)]
    if isinstance(vorbereiten, str):
        vb_box = vorbereiten
    else:
        vb_box = '<div class="box"><h3>Vorbereiten</h3><table class="ha">' + "".join(f"<tr><td><b>{w}</b></td><td>{x}</td></tr>" for w, x in vorbereiten) + "</table></div>"
    viele = len(schritte) > 8
    zeit = "".join(f'<div class="z{i % 6}" style="flex:{max(m, 5)}" title="{t}">{i + 1}{"" if viele else f" {t}"}{f" ({m}′)" if m else ""}</div>'
                   for i, (_, t, m, _, _) in enumerate(schritte))
    zeilen, g = "", -1
    for i, (tag, t, m, d, ks) in enumerate(schritte, 1):
        if tag:
            zeilen += f'<div class="tag">{tag.replace(" · ", ", ")}</div>'
            g = min(g + 1, len(gruppen) - 1) if len(gruppen) > 1 else 0
        g = max(g, 0)
        knopf = "".join(f"<button data-go=f{g}_{k} data-g={g}>Folie {k}</button>" for k in ks)
        zeilen += (f'<div class="schr"><span class="n">{i}</span><div><b>{t}</b>{f" ({m} min)" if m else ""}<br><span class="m">{d}</span></div>'
                   f'<div class="go">{knopf}</div></div>')
    tagknoepfe = "".join(f'<button data-g="{g}">{tag} <span>({len(fs)})</span></button>' for g, (tag, fs) in enumerate(gruppen)) if len(gruppen) > 1 else ""
    karten = (f'<div class="tagwahl">{tagknoepfe}</div>' if tagknoepfe else "") + "".join(
        f'<div class="fgruppe" data-g="{g}">' + "".join(f'<div class="fnr">Folie {i}</div><div class="fkarte" id="f{g}_{i}"><h3>{t}</h3>{h}</div>'
                                                     for i, (t, h) in enumerate(fs, 1)) + "</div>"
        for g, (_, fs) in enumerate(gruppen)) if any(fs for _, fs in gruppen) \
        else '<div class="box"><p>In dieser Woche gibt es keine Beamer-Folien, alles läuft über Tafel und Blatt.</p></div>'
    html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h1}</title>{OPTIK_CSS}{extra_css}{EXTRA}</head><body>
<div class="wrap"><header class="kopf"><h1>{h1}</h1><p class="sub">{sub.replace(" · ", ", ")}</p></header></div>
<nav><div class="wrap tabs"><button data-t="ueb">Überblick</button><button data-t="folien">Folien</button><button data-t="tafel">Tafelbild</button>
<button data-t="merk">Merkheft</button><button data-t="lsg">Lösungen</button></div></nav>
<div class="wrap">
<div class="tab" id="t_ueb">
{vb_box}
<div class="box"><h3>{verlauf}</h3><div class="zeitleiste">{zeit}</div>{zeilen}</div>
</div>
<div class="tab" id="t_folien">{karten}</div>
<div class="tab" id="t_tafel">{tafel}</div>
<div class="tab" id="t_merk">{merkheft}</div>
<div class="tab" id="t_lsg">{loesungen}</div>
</div>
<script>
const tabs=[...document.querySelectorAll('nav button')],secs=[...document.querySelectorAll('.tab')];
function show(id){{tabs.forEach(b=>b.classList.toggle('on',b.dataset.t===id));secs.forEach(s=>s.classList.toggle('on',s.id==='t_'+id));history.replaceState(null,'','#'+id);requestAnimationFrame(()=>window.scrollTo(0,0))}}
tabs.forEach(b=>b.onclick=()=>show(b.dataset.t));
const gr=[...document.querySelectorAll('.fgruppe')],tb=[...document.querySelectorAll('.tagwahl button')];
function tag(g){{g=String(g);gr.forEach(x=>x.hidden=gr.length>1&&x.dataset.g!==g);tb.forEach(b=>b.classList.toggle('on',b.dataset.g===g));try{{localStorage.setItem('mathe-tag-'+location.pathname,g)}}catch(e){{}}}}
tb.forEach(b=>b.onclick=()=>{{tag(b.dataset.g);window.scrollTo(0,0)}});
let g0='0';try{{g0=localStorage.getItem('mathe-tag-'+location.pathname)||'0'}}catch(e){{}}tag(g0);
document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{{show('folien');tag(b.dataset.g);setTimeout(()=>document.getElementById(b.dataset.go).scrollIntoView(),60)}});
history.scrollRestoration='manual';
show(secs.some(s=>s.id==='t_'+location.hash.slice(1))?location.hash.slice(1):'ueb');
</script></body></html>"""
    Path(ziel).write_text(html, encoding="utf-8")
    print("geschrieben:", Path(ziel).name, f"({len(html) // 1024} KB), Folien: {len(folien)}")
