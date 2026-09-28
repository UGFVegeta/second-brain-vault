#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Einstiegsseite Unterrichtsvorbereitung: erst das Fach (Physik, Mathe, Sport), dann die Klassenstufe mit ihrer Übersicht.
Verlinkt aus dem Lebens-Dashboard. Fehlende Dateien erscheinen ausgegraut, damit man die Lücken sieht.
Aufruf: python3 .scripts/unterrichtsvorbereitung_bauen.py  -> 04 Ressourcen/Unterrichtsvorbereitung.html"""
import html, json
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "04 Ressourcen"

# Fach -> [(Klasse, Thema, Hauptlink (Übersicht) oder "", [(Text, Link)])]; Links relativ zu 04 Ressourcen
FAECHER = [
    ("physik", "Physik", "⚛", [
        ("Klasse 7c", "Optik", "Physik/Optik/Optik Klasse 7 – Übersicht.html",
         [("Materialliste", "Physik/Optik/Optik Klasse 7 – Material.html"), ("Optik-Labore", "Physik/Optik/Optik-Labore.html")]),
        ("Klasse 10", "Kernphysik", "Physik/Kernphysik/Kernphysik Klasse 10 – Übersicht.html",
         [("Materialliste", "Physik/Kernphysik/Kernphysik Klasse 10 – Material.html"), ("Kernphysik-Labore", "Physik/Kernphysik/Kernphysik-Labore.html"),
          ("Begleitheft Kernspaltung (PDF)", "Physik/Kernphysik/Materialien/Begleitheft Kernspaltung.pdf")]),
    ]),
    ("mathe", "Mathe", "∑", [
        ("Klasse 7c", "Stoffverteilungsplan, Rationale Zahlen", "Mathematik/Mathematik Klasse 7 – Übersicht.html",
         [("Stoffverteilungsplan der Schule", "Mathematik/Mathematik Klasse 7 – Stoffverteilungsplan Schule.html"), ("Grundlagen-Check: Verlauf", "Mathematik/Arbeitsblätter/Grundlagen-Check/7c 2026-27/Verlauf.html"),
          ("Wichtige Informationen 7c (PDF)", "Mathematik/Wichtige Informationen Klasse 7c 2026-27.pdf")]),
        ("Klasse 10b", "noch keine Übersicht", "",
         [("Parabeln (Merkheft)", "Mathematik/Quadratische Funktionen/Parabeln (Rise-Stil).html"),
          ("Wichtige Informationen 10b (PDF)", "Mathematik/Wichtige Informationen Klasse 10b 2026-27.pdf")]),
    ]),
    ("sport", "Sport", "⚽", [
        (f"Klasse {k}", "Jungen", "",
         [("Curriculum Klasse " + str(k), f"Sport/Sportcurriculum.html#klasse-{k}"),
          ("Coopertest-Laufzettel (PDF)", f"Sport/Coopertest/Coopertest Laufzettel Klasse {k}.pdf")]) for k in range(5, 11)
    ] + [("Alle Klassen", "Allgemein", "",
          [("Sportcurriculum 5 bis 10", "Sport/Sportcurriculum.html"), ("Coopertest-Laufzettel alle Klassen (PDF)", "Sport/Coopertest/Coopertest Laufzettel Klasse 5 bis 10.pdf"),
           ("Abschreibtext Sportsachen vergessen (PDF)", "Sport/Abschreibtext Sportsachen vergessen.pdf")])]),
]


def a(text, pfad, cls=""):
    if not (RES / pfad.split("#")[0]).exists():
        return f'<span class="fehlt {cls}" title="Datei fehlt noch">{html.escape(text)}</span>'
    return f'<a class="{cls}" href="{html.escape(pfad)}">{html.escape(text)}</a>'


def karte(klasse, thema, haupt, links):
    kopf = f'<div class="kl">{html.escape(klasse)}</div><div class="th">{html.escape(thema)}</div>'
    if haupt:
        knopf = a("Übersicht öffnen →", haupt, "haupt")
    else:
        knopf = '<span class="haupt leer">keine Übersicht</span>' if klasse.startswith("Klasse") and "Sport" not in klasse else ""
    li = "".join(f"<li>{a(t, p)}</li>" for t, p in links)
    return f'<div class="karte{"" if haupt else " ohne"}">{kopf}{knopf}<ul>{li}</ul></div>'


def main():
    tabs = "".join(f'<button data-f="{k}"><span class="ico">{i}</span>{n}</button>' for k, n, i, _ in FAECHER)
    bereiche = ""
    for k, n, _, kl in FAECHER:
        karten = "".join(karte(*x) if k != "sport" else karte(x[0], x[1], "", x[3]).replace('<span class="haupt leer">keine Übersicht</span>', "") for x in kl)
        bereiche += f'<section class="fach" id="f-{k}" hidden><div class="karten">{karten}</div></section>'
    seite = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Unterrichtsvorbereitung</title>
<style>
:root{{--bg:#F4F6F9;--panel:#fff;--ink:#14171c;--muted:#66798E;--line:#D9DFE7;--accent:#2F5E9E;--sel:#E3EBF6}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
main{{max-width:1040px;margin:0 auto;padding:28px 20px 48px}}
h1{{font-size:24px;margin:0 0 4px}}.sub{{color:var(--muted);margin:0 0 20px}}
.tabs{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:22px}}
.tabs button{{font:inherit;font-size:17px;font-weight:600;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;cursor:pointer;color:var(--ink);display:flex;align-items:center;gap:10px;justify-content:center}}
.tabs button .ico{{font-size:22px;color:var(--accent)}}.tabs button:hover{{border-color:var(--accent)}}
.tabs button.on{{background:var(--sel);border-color:var(--accent)}}
.karten{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}}
.karte{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column}}
.karte.ohne{{background:#FAFBFC}}
.kl{{font-size:19px;font-weight:700}}.th{{color:var(--muted);font-size:13.5px;margin-bottom:12px}}
a.haupt{{display:block;text-align:center;background:var(--accent);color:#fff;text-decoration:none;border-radius:9px;padding:10px;font-weight:600;margin-bottom:10px}}
a.haupt:hover{{background:#244B80}}
span.haupt.leer{{display:block;text-align:center;border:1px dashed var(--line);color:var(--muted);border-radius:9px;padding:9px;margin-bottom:10px;font-size:14px}}
ul{{list-style:none;margin:0;padding:0}}li{{padding:4px 0;border-top:1px solid #EEF1F5;font-size:14px}}li:first-child{{border-top:0}}
li a{{color:var(--accent);text-decoration:none}}li a:hover{{text-decoration:underline}}
.fehlt{{color:#A9B4C2}}.fehlt::after{{content:" · fehlt noch";font-size:12px}}
.fuss{{margin-top:26px;font-size:13px;color:var(--muted)}}.fuss a{{color:var(--accent)}}
[hidden]{{display:none!important}}
@media (max-width:640px){{.tabs button{{font-size:15px;padding:12px 6px;flex-direction:column;gap:2px}}}}
</style></head><body><main>
<h1>Unterrichtsvorbereitung</h1><p class="sub">Erst das Fach wählen, dann die Klasse. Die Übersichten zeigen alle Stunden, ausgegraute Einträge sind noch nicht vorbereitet.</p>
<div class="tabs">{tabs}</div>{bereiche}
<p class="fuss">Status aller Stunden: <a href="Bildungs-Dashboard.html">Bildungs-Dashboard</a> · zurück zum <a href="Lebens-Dashboard.html">Lebens-Dashboard</a></p>
</main><script>
const F={json.dumps([k for k, *_ in FAECHER])};
function zeige(f){{ if(!F.includes(f)) f=F[0];
  document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.f===f));
  document.querySelectorAll('.fach').forEach(s=>s.hidden=s.id!=='f-'+f);
  try{{localStorage.setItem('uv-fach',f)}}catch(e){{}} history.replaceState(null,'','#'+f); }}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>zeige(b.dataset.f));
let start=location.hash.slice(1); if(!F.includes(start)){{ try{{start=localStorage.getItem('uv-fach')||''}}catch(e){{start=''}} }}
zeige(start);
</script></body></html>"""
    ziel = RES / "Unterrichtsvorbereitung.html"
    ziel.write_text(seite, encoding="utf-8")
    fehlt = [p for _, _, _, kl in FAECHER for x in kl for _, p in x[3] + ([("", x[2])] if x[2] else []) if not (RES / p.split("#")[0]).exists()]
    print("geschrieben:", ziel.name, "· fehlende Dateien:", fehlt or "keine")


if __name__ == "__main__":
    main()
