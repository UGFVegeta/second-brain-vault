#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Berichte-Leseansicht: liest die Daily Notes und baut "04 Ressourcen/Berichte.html".

Die Seite zeigt Geschafft, Erkenntnisse und Offen pro Tag sowie Wochenrückblicke. Sie ist nur zum Lesen,
Berichte entstehen im Gespräch mit Claude (Skill "bericht"). Daten stecken eingebettet in der HTML.

Start: python3 .scripts/berichte_bauen.py
"""
import json
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
DAILY = VAULT / "05 Daily Notes"
LOGBUCH = VAULT / "03 Bereiche" / "Gesundheit & Longevity" / "Gesundheitslogbuch.md"
OUT = VAULT / "04 Ressourcen" / "Berichte.html"

TAG_ABSCHNITTE = {"Geschafft": "geschafft", "Erkenntnisse": "erkenntnisse", "Offen / Nächste Schritte": "offen"}
WOCHE_ABSCHNITTE = {"Geschafft": "geschafft", "Erkenntnisse": "erkenntnisse", "Nächste Woche": "offen"}


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for z in m.group(1).splitlines():
            k, _, v = z.partition(":")
            fm[k.strip()] = v.strip()
    return fm, text[m.end():] if m else text


def punkte(zeilen):
    """Spiegelstriche mit eingerückten Unterpunkten als Liste von Strings (Unterpunkte mit '  ' davor)."""
    out = []
    for z in zeilen:
        m = re.match(r"^(\s*)[-*]\s+(.*\S)\s*$", z)
        if m:
            out.append(("  " if m.group(1) else "") + m.group(2))
        elif z.strip() and out:
            out[-1] += " " + z.strip()
    return out


def abschnitte(body, ebene, gueltig):
    """Zerlegt body in Abschnitte der Ebene ('## ' oder '### ') und gibt {schluessel: [punkte]} zurück."""
    teile, aktuell = {}, None
    for z in body.splitlines():
        if z.startswith(ebene) and not z.startswith(ebene + "#"):
            titel = z[len(ebene):].strip()
            aktuell = gueltig.get(titel)
            if aktuell:
                teile.setdefault(aktuell, [])
            continue
        if re.match(r"^#{1,%d} " % len(ebene.strip()), z):
            aktuell = None
            continue
        if aktuell:
            teile[aktuell].append(z)
    return {k: punkte(v) for k, v in teile.items() if punkte(v)}


def wochenrueckblick(body):
    m = re.search(r"^## Wochenrückblick KW(\d+)\s*$", body, re.M)
    if not m:
        return None
    rest = body[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    block = rest[:nxt.start()] if nxt else rest
    teile = abschnitte(block, "### ", WOCHE_ABSCHNITTE)
    return {"kw": int(m.group(1)), **teile} if teile else None


def befinden_map():
    out = {}
    if LOGBUCH.exists():
        for z in LOGBUCH.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([1-5])\s*\|", z)
            if m:
                out[m.group(1)] = int(m.group(2))
    return out


def zahl(v):
    try:
        return float(v.replace(",", "."))
    except (ValueError, AttributeError):
        return None


def sammeln():
    bef = befinden_map()
    tage = []
    for f in sorted(DAILY.glob("????-??-??.md"), reverse=True):
        fm, body = frontmatter(f.read_text(encoding="utf-8", errors="ignore"))
        teile = abschnitte(body, "## ", TAG_ABSCHNITTE)
        woche = wochenrueckblick(body)
        if not teile and not woche:
            continue
        tag = {"d": f.stem, "teile": teile}
        for key, name in (("schlaf_h", "schlaf"), ("ruhepuls", "ruhepuls"), ("hrv", "hrv"), ("fokus_min", "fokus")):
            z = zahl(fm.get(key))
            if z:
                tag[name] = z
        if f.stem in bef:
            tag["befinden"] = bef[f.stem]
        if woche:
            tag["woche"] = woche
        tage.append(tag)
    return tage


VORLAGE = r'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Berichte</title>
<style>
  :root {
    --bg:#f3eee4; --karte:#fffcf5; --karte2:#f6f0e3; --linie:#e4dccb;
    --tinte:#2b2620; --leise:#7b7264; --akzent:#b4532a; --akzent-t:#fffcf5;
    --geschafft:#4b7a47; --erkenntnisse:#a2701a; --offen:#476a8c;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
    --sans:-apple-system,"Helvetica Neue",Arial,sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#15120e; --karte:#1e1a15; --karte2:#26211a; --linie:#332d24;
            --tinte:#ece5d6; --leise:#a0957f; --akzent:#e08a5c; --akzent-t:#1a120c;
            --geschafft:#86b982; --erkenntnisse:#d8a64e; --offen:#8fb0d1; }
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--tinte); font:17px/1.55 var(--sans); }
  main { max-width:860px; margin:0 auto; padding:44px 20px 80px; }
  header { margin-bottom:30px; }
  h1 { font:600 2.5rem/1.1 var(--serif); margin:0 0 6px; letter-spacing:-.01em; }
  .unter { color:var(--leise); margin:0; font-family:var(--serif); font-style:italic; }
  .leiste { display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin:26px 0 8px; }
  .reiter { display:inline-flex; background:var(--karte2); border-radius:999px; padding:3px; }
  .reiter button { border:0; background:none; color:var(--leise); font:inherit; font-size:.85rem; padding:7px 16px; border-radius:999px; cursor:pointer; }
  .reiter button[aria-pressed="true"] { background:var(--karte); color:var(--tinte); font-weight:600; box-shadow:0 1px 2px #0002; }
  input[type=search] { flex:1; min-width:180px; font:inherit; font-size:.85rem; color:var(--tinte); background:var(--karte);
                       border:1px solid var(--linie); border-radius:999px; padding:8px 16px; }
  input:focus-visible, button:focus-visible { outline:2px solid var(--akzent); outline-offset:2px; }
  .woche { margin:44px 0 14px; display:flex; align-items:baseline; gap:12px; }
  .woche h2 { font:600 1.4rem/1.2 var(--serif); margin:0; }
  .woche span { color:var(--leise); font-size:.85rem; }
  .tag { display:grid; grid-template-columns:76px 1fr; gap:18px; background:var(--karte); border:1px solid var(--linie);
         border-radius:16px; padding:20px 22px; margin-bottom:14px; }
  .datum { text-align:center; padding-top:2px; }
  .datum b { display:block; font:600 2.2rem/1 var(--serif); }
  .datum small { display:block; color:var(--leise); font-size:.85rem; margin-top:4px; }
  .punkt { display:inline-block; width:10px; height:10px; border-radius:50%; margin-top:10px; background:var(--linie); }
  .werte { display:flex; flex-wrap:wrap; gap:6px 16px; color:var(--leise); font-size:.85rem; margin:0 0 12px; }
  .abschnitt { margin:0 0 14px; }
  .abschnitt:last-child { margin-bottom:0; }
  .abschnitt h3 { font:700 .85rem/1 var(--sans); letter-spacing:.07em; text-transform:uppercase; margin:0 0 6px; }
  .geschafft h3 { color:var(--geschafft); } .erkenntnisse h3 { color:var(--erkenntnisse); } .offen h3 { color:var(--offen); }
  ul { margin:0; padding-left:1.1em; } li { margin:0 0 4px; } li.sub { margin-left:1.1em; list-style:circle; }
  li::marker { color:var(--leise); }
  .wochenkarte { border-color:var(--akzent); background:var(--karte2); }
  .wochenkarte .datum b { color:var(--akzent); font-size:1.5rem; padding-top:6px; }
  .etikett { color:var(--akzent); font-weight:700; font-size:.85rem; letter-spacing:.07em; text-transform:uppercase; margin:0 0 10px; }
  .leer { color:var(--leise); text-align:center; padding:40px 0; font-family:var(--serif); font-style:italic; }
  #mehr { display:block; margin:28px auto 0; border:1px solid var(--linie); background:var(--karte); color:var(--tinte);
          font:inherit; font-size:.85rem; padding:10px 24px; border-radius:999px; cursor:pointer; }
  mark { background:color-mix(in srgb, var(--akzent) 30%, transparent); color:inherit; border-radius:3px; }
  @media (max-width:560px) { .tag { grid-template-columns:1fr; gap:8px; } .datum { display:flex; gap:10px; align-items:baseline; text-align:left; }
                             .datum small { margin:0; } h1 { font-size:2rem; } }
</style>
</head>
<body>
<main>
  <header>
    <h1>Berichte</h1>
    <p class="unter" id="unter"></p>
    <div class="leiste">
      <div class="reiter" role="group" aria-label="Ansicht">
        <button type="button" id="r-alle" aria-pressed="true">Alle Tage</button>
        <button type="button" id="r-woche" aria-pressed="false">Wochenrückblicke</button>
      </div>
      <input type="search" id="suche" placeholder="Suchen, zum Beispiel Konrektor" aria-label="Suchen">
    </div>
  </header>
  <div id="liste"></div>
  <button type="button" id="mehr">Ältere Wochen zeigen</button>
</main>
<script>
const DATEN = /*DATEN*/;
const $ = id => document.getElementById(id);
const WT = ["Sonntag","Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag"];
const MON = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];
const TITEL = { geschafft:"Geschafft", erkenntnisse:"Erkenntnisse", offen:"Offen" };
const BEFINDEN = ["", "#c0553d", "#d28a3c", "#bba94a", "#7fa860", "#4b7a47"];
let ansicht = "alle", sichtbareWochen = 6;

function datum(iso) { return new Date(iso + "T12:00:00"); }
function montag(d) { const x = new Date(d); x.setDate(x.getDate() - (x.getDay() + 6) % 7); return x; }
function kw(d) {
  const t = new Date(d); t.setDate(d.getDate() + 3 - (d.getDay() + 6) % 7);
  const w1 = new Date(t.getFullYear(), 0, 4);
  return 1 + Math.round(((t - w1) / 864e5 - 3 + (w1.getDay() + 6) % 7) / 7);
}
function wochenKopf(m) {
  const e = new Date(m); e.setDate(e.getDate() + 6);
  const von = m.getDate() + (m.getMonth() === e.getMonth() ? "" : ". " + MON[m.getMonth()]);
  return { titel: "Woche " + kw(m), zeit: von + (m.getMonth() === e.getMonth() ? "." : "") + " bis " + e.getDate() + ". " + MON[e.getMonth()] + " " + e.getFullYear() };
}
function z(t, frage) {
  const f = document.createDocumentFragment();
  const teile = String(t).replace(/\[\[([^\]|]+\|)?([^\]]+)\]\]/g, "$2").split(/(\*\*[^*]+\*\*)/);
  teile.forEach(s => {
    const b = s.startsWith("**") && s.endsWith("**") && s.length > 4;
    const text = b ? s.slice(2, -2) : s;
    const el = b ? document.createElement("b") : document.createDocumentFragment();
    if (frage && text.toLowerCase().includes(frage)) {
      const i = text.toLowerCase().indexOf(frage);
      el.append(text.slice(0, i));
      const m = document.createElement("mark"); m.textContent = text.slice(i, i + frage.length); el.append(m, text.slice(i + frage.length));
    } else el.append(text);
    f.append(el);
  });
  return f;
}
function abschnitte(teile, frage) {
  const box = document.createDocumentFragment();
  ["geschafft", "erkenntnisse", "offen"].forEach(k => {
    if (!teile[k]) return;
    const s = document.createElement("section"); s.className = "abschnitt " + k;
    const h = document.createElement("h3"); h.textContent = TITEL[k];
    const ul = document.createElement("ul");
    teile[k].forEach(p => { const li = document.createElement("li"); if (p.startsWith("  ")) { li.className = "sub"; p = p.trim(); } li.append(z(p, frage)); ul.append(li); });
    s.append(h, ul); box.append(s);
  });
  return box;
}
function werte(t) {
  const w = [];
  if (t.schlaf) w.push("Schlaf " + String(t.schlaf).replace(".", ",") + " h");
  if (t.ruhepuls) w.push("Ruhepuls " + t.ruhepuls);
  if (t.hrv) w.push("HRV " + t.hrv);
  if (t.fokus) w.push("Fokus " + t.fokus + " min");
  if (!w.length) return null;
  const p = document.createElement("p"); p.className = "werte"; w.forEach(x => { const s = document.createElement("span"); s.textContent = x; p.append(s); }); return p;
}
function karte(t, frage, nurWoche) {
  const d = datum(t.d), a = document.createElement("article"); a.className = "tag" + (nurWoche ? " wochenkarte" : "");
  const l = document.createElement("div"); l.className = "datum";
  l.innerHTML = nurWoche ? "<b></b><small></small>" : "<b></b><small></small>";
  l.firstChild.textContent = nurWoche ? "KW " + t.woche.kw : d.getDate();
  l.lastChild.textContent = nurWoche ? "bis " + d.getDate() + ". " + MON[d.getMonth()].slice(0, 3) + "." : WT[d.getDay()].slice(0, 2) + ", " + MON[d.getMonth()].slice(0, 3) + ".";
  if (!nurWoche && t.befinden) { const p = document.createElement("span"); p.className = "punkt"; p.style.background = BEFINDEN[t.befinden]; p.title = "Befinden " + t.befinden + " von 5"; l.append(p); }
  const r = document.createElement("div");
  if (nurWoche) { const e = document.createElement("p"); e.className = "etikett"; e.textContent = "Wochenrückblick"; r.append(e, abschnitte(t.woche, frage)); }
  else { const w = werte(t); if (w) r.append(w); r.append(abschnitte(t.teile, frage)); }
  a.append(l, r); return a;
}
function passt(t, frage, nurWoche) {
  if (!frage) return true;
  const quelle = nurWoche ? t.woche : t.teile;
  return Object.values(quelle).some(v => Array.isArray(v) && v.some(p => p.toLowerCase().includes(frage)));
}
function zeichne() {
  const frage = $("suche").value.trim().toLowerCase();
  const nurWoche = ansicht === "woche";
  const eintraege = DATEN.filter(t => nurWoche ? t.woche : Object.keys(t.teile).length).filter(t => passt(t, frage, nurWoche));
  const liste = $("liste"); liste.innerHTML = "";
  $("unter").textContent = DATEN.length + " Tage mit Bericht, zuletzt " + (DATEN[0] ? datum(DATEN[0].d).getDate() + ". " + MON[datum(DATEN[0].d).getMonth()] : "noch keiner");
  if (!eintraege.length) { liste.innerHTML = '<p class="leer">' + (nurWoche && !frage ? "Noch kein Wochenrückblick. Sag Claude am Freitag oder Sonntag „Wochenbericht“." : "Nichts gefunden.") + '</p>'; $("mehr").style.display = "none"; return; }
  let letzte = "", wochen = 0, versteckt = false;
  for (const t of eintraege) {
    const m = montag(datum(t.d)), key = m.toISOString();
    if (key !== letzte) {
      if (wochen >= sichtbareWochen && !frage) { versteckt = true; break; }
      wochen++; letzte = key;
      if (!nurWoche) { const k = wochenKopf(m), h = document.createElement("div"); h.className = "woche";
        h.innerHTML = "<h2></h2><span></span>"; h.firstChild.textContent = k.titel; h.lastChild.textContent = k.zeit; liste.append(h); }
    }
    liste.append(karte(t, frage, nurWoche));
  }
  $("mehr").style.display = versteckt ? "" : "none";
}
$("r-alle").onclick = () => { ansicht = "alle"; $("r-alle").setAttribute("aria-pressed", true); $("r-woche").setAttribute("aria-pressed", false); zeichne(); };
$("r-woche").onclick = () => { ansicht = "woche"; $("r-woche").setAttribute("aria-pressed", true); $("r-alle").setAttribute("aria-pressed", false); zeichne(); };
$("suche").oninput = zeichne;
$("mehr").onclick = () => { sichtbareWochen += 6; zeichne(); };
zeichne();
</script>
</body>
</html>
'''


def main():
    tage = sammeln()
    daten = json.dumps(tage, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUT.write_text(VORLAGE.replace("/*DATEN*/", daten), encoding="utf-8")
    print(f"geschrieben: {OUT.name} ({len(tage)} Tage, {sum(1 for t in tage if 'woche' in t)} Wochenrückblicke, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
