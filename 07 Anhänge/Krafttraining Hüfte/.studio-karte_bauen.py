import re, os, html, base64
SRC = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/07 Anhänge/Krafttraining Hüfte"
def svg(name):
    t = open(os.path.join(SRC, name), encoding="utf-8").read()
    t = re.sub(r'<\?xml.*?\?>', '', t)
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', t)
    W, H = int(m.group(1)), int(m.group(2))
    # Titel-/Fusszeilenbereich wegschneiden, nur die Figur behalten
    t = t.replace(m.group(0), f'viewBox="6 58 {W-12} {H-78}"')
    t = re.sub(r'\swidth="\d+"', '', t, count=1)
    t = re.sub(r'\sheight="\d+"', '', t, count=1)
    # Hintergrundrechteck entfernen (sonst weisser Kasten im gecroppten Bereich)
    t = re.sub(r'<rect width="\d+" height="\d+" rx="\d+" fill="#f7f8fa"/>', '', t, count=1)
    uid = re.sub(r'\W', '', name)[:12]
    t = t.replace('id="ar"', f'id="ar{uid}"').replace('url(#ar)', f'url(#ar{uid})')
    return t

A = [
 ("A1","Seitliches Beinheben","3 × 12–15 je Seite","Seitlage · Becken senkrecht, nicht nach hinten kippen · Progression Miniband, dann Manschette","A1 Seitliches Beinheben.svg"),
 ("A2","Einbeinige Standwaage","3 × 8–10 je Seite","Kurzhantel Gegenhand · Becken waagerecht, Rücken gerade · bei Hamstring-Ziehen Umfang kürzen","A2 Einbeinige Standwaage.svg"),
 ("A3","Step-up auf Kiste","3 × 8–10 je Seite","Knie ca. 90° · über die Ferse hoch, 3 s langsam ablassen · stattdessen A3v Step-down möglich","A3 Step-up auf Kiste.svg"),
 ("A4","Copenhagen Plank, kurzer Hebel","3 × 20–30 s je Seite","Knie auf der Bank · Schulter–Hüfte–Knie in einer Linie · unteres Bein hängt frei","A4 Copenhagen Plank.svg"),
 ("A5","Einbeiniges Wadenheben","3 × 12–15 je Seite","Vorfuß auf der Stufe · Ferse tief absenken, oben kurz halten","A5 Einbeiniges Wadenheben.svg"),
 ("A6","Beckenheben im Einbeinstand","3 × 12 je Seite","Auf Stufe · Standbeinknie GESTRECKT, nur das Becken sinkt und hebt · freies Bein hängt","A6 Beckenheben Einbeinstand.svg"),
]
B = [
 ("B1","Hip Thrust","4 × 6–10 · Pause 2 min","Oben bilden Rumpf und Oberschenkel eine waagerechte Linie · 1 s anspannen · kein Hohlkreuz","B1 Hip Thrust.svg"),
 ("B2","Bulgarian Split Squat","3 × 8 je Seite","Hinterer Fuß erhöht · senkrecht absenken · Tiefe nur so weit, wie die Hüfte es zulässt","B2 Bulgarian Split Squat.svg"),
 ("B3","Abduktion im Stand","3 × 12–15 je Seite","Band am Sprunggelenk · Becken bleibt ruhig · Standbein arbeitet mit, beide Seiten","B3 Abduktion im Stand.svg"),
 ("B4","Pallof Press","3 × 10 je Seite","Band seitlich auf Brusthöhe · Arme nach vorn strecken, der Rotation widerstehen","B4 Pallof Press.svg"),
 ("B5","Rumänisches Kreuzheben","3 × 8–10","Knie leicht gebeugt · Hüfte nach hinten schieben · Hantel eng am Bein","B5 Rumänisches Kreuzheben.svg"),
 ("B6","Seitlicher Ausfallschritt","3 × 8 je Seite","Breiter Stand · ein Knie beugt, anderes Bein gestreckt · nur schmerzfrei tief, hin und her","B6 Seitlicher Ausfallschritt.svg"),
]

VID={'A1': '-rDiQXjeXO0', 'A2': 'Zfr6wizR8rs', 'A3': 'wfhXnLILqdk', 'A4': 'nhGK-DxiGBE', 'A5': 'qPd73snQfUs', 'A6': '2j0fHZwixA8', 'B1': 'pF17m_CXfL0', 'B2': 'fSyiHxm1Igw', 'B3': 'vSqhrbzZb7A', 'B4': '-0N2xTi69t8', 'B5': '_oyxCn2iSjU', 'B6': 'tmhESsZcpDY'}

def photo(code):
    fp=os.path.join(SRC, f"{code} Foto.jpg")
    b=base64.b64encode(open(fp,"rb").read()).decode()
    return f'<img class="ph" src="data:image/jpeg;base64,{b}">'

def rows(items):
    return "\n".join(f'''<div class="row">
  <div class="pic"><div class="draw">{svg(f)}</div><div class="ph-wrap">{photo(c)}</div></div>
  <div class="txt">
    <div class="name"><span class="code">{c}</span>{html.escape(n)}</div>
    <div class="dose">{html.escape(d)}</div>
    <div class="cue">{html.escape(q)}</div>
    <a class="vid" href="https://www.youtube.com/watch?v={VID[c]}">▶ Video zur Ausführung</a>
  </div>
</div>''' for c,n,d,q,f in items)

CSS = """
@page{size:A4 portrait;margin:10mm 9mm}
*{box-sizing:border-box}
body{font-family:-apple-system,system-ui,"Helvetica Neue",sans-serif;color:#1f2933;margin:0}
.page{page-break-after:always}
.page:last-child{page-break-after:auto}
h1{font-size:19pt;margin:0 0 0.8mm}
.sub{font-size:9.5pt;color:#6b7280;margin-bottom:2.6mm}
.ampel{border:1.3pt solid #e8590c;border-radius:2.2mm;padding:2mm 2.6mm;font-size:8.6pt;line-height:1.4;margin-bottom:3mm;background:#fff7f2}
.ampel b{color:#e8590c}
.row{display:flex;align-items:center;gap:3.5mm;border-bottom:0.6pt solid #dfe3e8;padding:1.6mm 0}
.row:last-child{border-bottom:none}
.pic{width:74mm;flex:0 0 74mm;display:flex;gap:1.5mm;align-items:center}
.draw{width:36mm;flex:0 0 36mm;background:#f7f8fa;border-radius:2mm;padding:1mm}
.ph-wrap{width:36mm;flex:0 0 36mm;border-radius:2mm;overflow:hidden;line-height:0}
.ph{width:100%;height:auto;display:block}
.pic svg{width:100%;height:auto;display:block}
.pic svg text{display:none}
.txt{flex:1}
.name{font-size:12.5pt;font-weight:650;margin-bottom:1mm;line-height:1.2}
.code{display:inline-block;background:#1f2933;color:#fff;border-radius:1.5mm;padding:0.4mm 1.7mm;font-size:9pt;margin-right:2mm;vertical-align:1.5px}
.dose{font-size:12pt;font-weight:650;color:#e8590c;margin-bottom:0.8mm}
.cue{font-size:9pt;color:#4b5563;line-height:1.32}
.vid{display:inline-block;margin-top:0.9mm;font-size:8.6pt;color:#1d6fbf;text-decoration:none}
.foot{margin-top:3mm;font-size:8.2pt;color:#6b7280;border-top:0.6pt solid #dfe3e8;padding-top:1.6mm}
"""

HTML = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>Krafttraining Hüfte – Studio-Karte</title><style>{CSS}</style></head><body>

<div class="page">
<h1>Block A · Standbein &amp; Abduktion</h1>
<div class="sub">2× pro Woche · ca. 35 min · Block A und B abwechseln · Kraft auf ohnehin harte Tage legen</div>
<div class="ampel">
<b>Schmerzampel:</b> Während der Übung bis <b>5/10</b> erlaubt · nach <b>24 h</b> zurück auf Ausgangsniveau · wenn der <b>Nachtschmerz mehr als 2 Nächte</b> schlechter ist, Last um 20 % runter statt Übung streichen<br>
<b>Phase 1</b> (Woche 1–4): 3 Sätze, 12–15 Wdh, moderate Last · <b>Phase 2</b> (ab Woche 5): 6–10 Wdh schwer, 3 s runter / 1 s hoch
</div>
{rows(A)}
<div class="foot">Bei Ziehen am proximalen Hamstring (A2, B5) gilt die dortige Grenze von 3–4/10 vorrangig. · Effekt auf den Nachtschmerz frühestens nach 8–12 Wochen bewerten.</div>
</div>

<div class="page">
<h1>Block B · Hüftstreckung unter Last</h1>
<div class="sub">2× pro Woche · ca. 35 min · hier kommt die schwere Last hin</div>
<div class="ampel">
<b>Priorität 1, nicht verhandelbar:</b> 2 Krafteinheiten pro Woche. Wird die Woche eng, fliegt eine Ausdauereinheit raus, nicht die Kraft.<br>
<b>Laufen:</b> Umfang halten statt ausbauen, Kadenz hoch · <b>Schwimmen:</b> kein Brustbeinschlag · <b>Rad:</b> frei, Aeroposition prüfen
</div>
{rows(B)}
<div class="foot">Abends zusätzlich: Wärme 15 min · Traktion an der Bettkante 2 min · Hüftkreisen im Vierfüßler 10 je Richtung · R5 Innenrotation in Bauchlage 3 × 12 · kein statisches Dehnen. · Links: Zeichnung. Rechts: Standbild aus dem verlinkten Video. Videolinks antippbar, geprüft am 12.08.2026. Sie zeigen die saubere Bewegung, nicht deine Dosierung.</div>
</div>

</body></html>"""

out = "/private/tmp/claude-501/-Users-oskarklein-Documents-Obsidian-Claude-Second-Brain-Claude/aa060cfb-f34f-4c57-b440-77107c322813/scratchpad/card.html"
open(out,"w",encoding="utf-8").write(HTML)
print("ok", len(HTML))
