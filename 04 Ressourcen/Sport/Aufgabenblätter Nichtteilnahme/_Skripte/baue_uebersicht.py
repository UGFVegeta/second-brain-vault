#!/usr/bin/env python3
"""Baut Übersicht.html: alle Aufgabenblätter zum schnellen Durchblättern (Vorder- und Rückseite nebeneinander).

Liest die PDFs aus den Ordnern „Klasse … / Thema / …pdf“ und schreibt die Übersicht in den Vault-Ordner
und in den iCloud-Ordner (gleiche Struktur, relative Links). Wird am Ende von baue_blaetter.py aufgerufen.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

HIER = Path(__file__).resolve().parent
BASIS = HIER.parent
ICLOUD = (Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Schuljahr 26 27/Sport"
          / "Aufgabenblätter Nichtteilnahme")
VORSCHAU = BASIS / "_Vorschau"  # JPG-Vorschauen, gitignored, werden aus den PDFs neu erzeugt
STUFEN = ["Klasse 5 und 6", "Klasse 7 und 8", "Klasse 9 und 10"]
THEMEN = ["Essen und Trinken", "Fair Play", "Herz, Puls und Ausdauer", "Training und Erholung",
          "Verletzungen vermeiden", "Regeln und Spielfeld"]


def vorschau(pdf):
    """Erzeugt JPGs der beiden Seiten (nur wenn das PDF neuer ist) und gibt die relativen Pfade zurück."""
    rel = pdf.relative_to(BASIS)
    ziel = VORSCHAU / rel.parent / pdf.stem
    bilder = [ziel.with_name(f"{pdf.stem}-{i}.jpg") for i in (1, 2)]
    if not all(b.exists() and b.stat().st_mtime >= pdf.stat().st_mtime for b in bilder):
        ziel.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", "quality=72", "-r", "90", str(pdf), str(ziel)], check=True)
    return ["/".join(quote(x) for x in b.relative_to(BASIS).parts) for b in bilder]


def vorschau_anfang(pdf, name):
    """JPGs der ersten beiden Seiten einer längeren Datei (für das Lösungsdeckblatt)."""
    ziel = VORSCHAU / pdf.relative_to(BASIS).parent
    bilder = [ziel / f"{name}-{i}.jpg" for i in (1, 2)]
    if not all(b.exists() and b.stat().st_mtime >= pdf.stat().st_mtime for b in bilder):
        ziel.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", "quality=72", "-r", "90", "-f", "1", "-l", "2",
                        str(pdf), str(ziel / f"{name}-tmp")], check=True)
        for i, t in enumerate(sorted(ziel.glob(f"{name}-tmp-*.jpg")), 1):
            t.replace(ziel / f"{name}-{i}.jpg")
    return ["/".join(quote(x) for x in b.relative_to(BASIS).parts) for b in bilder]


def rel(p):
    return "/".join(quote(x) for x in p.relative_to(BASIS).parts)


def deckblatt(st):
    """Eintrag „Deckblatt“ je Stufe: Schülerdeckblatt, mit Lösung-Schalter das Lösungsdeckblatt."""
    d = BASIS / "Druck" / st
    deck = next(iter(sorted((d / "_Einzelteile").glob("Deckblatt K*.pdf"))), None)
    loes = next(iter(sorted(d.glob("2 Lösungen*.pdf"))), None)
    if not deck:
        return []
    return [{"nr": "", "titel": "Deckblatt und Inhalt", "pdf": rel(deck), "bild": vorschau(deck),
             "loes": rel(loes) if loes else "", "loesbild": vorschau_anfang(loes, "Deckblatt Lösungen") if loes else []}]


def daten():
    out = []
    for st in STUFEN:
        themen = []
        dk = deckblatt(st)
        if dk:
            themen.append({"thema": "Ordner", "blaetter": dk})
        for th in THEMEN:
            ordner = BASIS / st / th
            blaetter = []
            for pdf in sorted(ordner.glob("*.pdf")):
                if "(Lösung)" in pdf.name:
                    continue
                m = re.match(r".* (\d) – (.*)\.pdf$", pdf.name)
                nr, titel = (m.group(1), m.group(2)) if m else ("", pdf.stem)
                loes = pdf.with_name(pdf.stem + " (Lösung).pdf")
                blaetter.append({"nr": nr, "titel": titel, "pdf": rel(pdf), "bild": vorschau(pdf),
                                 "loes": rel(loes) if loes.exists() else "",
                                 "loesbild": vorschau(loes) if loes.exists() else []})
            themen.append({"thema": th, "blaetter": blaetter})
        out.append({"stufe": st, "themen": themen})
    return out


HTML = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aufgabenblätter Nichtteilnahme</title>
<style>
:root { --acc:#1f6fb2; --bg:#f4f6f9; --line:#dde3ea; --text:#1b1b1b; --muted:#667; --loe:#c2185b; }
* { box-sizing:border-box; }
body { margin:0; font-family:-apple-system, "Open Sans", Helvetica, sans-serif; color:var(--text); background:var(--bg);
       display:grid; grid-template-columns:290px 1fr; grid-template-rows:auto 1fr; height:100vh; }
header { grid-column:1 / 3; display:flex; align-items:center; gap:18px; padding:10px 18px; background:#fff; border-bottom:1px solid var(--line); }
header h1 { font-size:17px; margin:0; color:var(--acc); white-space:nowrap; }
.tabs { display:flex; gap:6px; }
.tabs button, .schalter { border:1px solid var(--line); background:#fff; border-radius:8px; padding:6px 12px; font:inherit; font-size:14px; cursor:pointer; }
.tabs button.an { background:var(--acc); border-color:var(--acc); color:#fff; }
.schalter.an { background:var(--loe); border-color:var(--loe); color:#fff; }
.hilfe { margin-left:auto; font-size:12px; color:var(--muted); white-space:nowrap; }
nav { overflow:auto; background:#fff; border-right:1px solid var(--line); padding:8px 0 20px; }
nav h2 { font-size:12px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:14px 16px 4px; }
nav a { display:flex; gap:8px; padding:6px 16px; color:var(--text); text-decoration:none; font-size:14px; line-height:1.3; cursor:pointer; }
nav a span { color:var(--muted); min-width:12px; }
nav a:hover { background:var(--bg); }
nav a.an { background:#e6f0fa; color:var(--acc); font-weight:600; box-shadow:inset 3px 0 0 var(--acc); }
main { display:flex; flex-direction:column; min-height:0; padding:10px 14px 14px; gap:8px; }
.kopf { display:flex; align-items:baseline; gap:12px; }
.kopf b { font-size:16px; }
.kopf small { color:var(--muted); }
.kopf a { margin-left:auto; font-size:13px; color:var(--acc); }
.seiten { flex:1; display:grid; grid-template-columns:1fr 1fr; gap:12px; min-height:0; }
.seiten a { display:flex; justify-content:center; min-height:0; }
.seiten img { max-width:100%; max-height:100%; object-fit:contain; border:1px solid var(--line); border-radius:4px; background:#fff;
              box-shadow:0 1px 4px rgba(0,0,0,.08); }
@media (max-width: 900px) { body { grid-template-columns:1fr; grid-template-rows:auto auto 1fr; } nav { max-height:30vh; } header { flex-wrap:wrap; }
  .seiten { grid-template-columns:1fr; } .seiten img { max-height:none; } .hilfe { display:none; } }
</style></head>
<body>
<header>
  <h1>Aufgabenblätter Nichtteilnahme</h1>
  <div class="tabs" id="tabs"></div>
  <button class="schalter" id="loes">Lösung</button>
  <span class="hilfe">↑ ↓ Blatt wechseln &nbsp; 1 2 3 Stufe &nbsp; L Lösung</span>
</header>
<nav id="nav"></nav>
<main>
  <div class="kopf"><b id="titel"></b><small id="unter"></small><a id="link" target="_blank">PDF öffnen</a></div>
  <div class="seiten"><a id="a1" target="_blank"><img id="s1" alt="Vorderseite"></a><a id="a2" target="_blank"><img id="s2" alt="Rückseite"></a></div>
</main>
<script>
const D = __DATEN__;
let st = 0, idx = 0, loes = false;
try { const z = JSON.parse(localStorage.getItem("ueb") || "{}"); st = z.st || 0; idx = z.idx || 0; loes = !!z.loes; } catch (e) {}
const liste = () => D[st].themen.flatMap(t => t.blaetter.map(b => ({...b, thema: t.thema})));
function zeichne() {
  const L = liste(); if (idx >= L.length) idx = 0;
  document.getElementById("tabs").innerHTML = D.map((s, i) =>
    `<button class="${i === st ? "an" : ""}" data-i="${i}">${s.stufe.replace("Klasse ", "")}</button>`).join("");
  let n = 0, h = "";
  for (const t of D[st].themen) {
    h += `<h2>${t.thema}</h2>`;
    for (const b of t.blaetter) { h += `<a class="${n === idx ? "an" : ""}" data-n="${n}"><span>${b.nr}</span>${b.titel}</a>`; n++; }
  }
  document.getElementById("nav").innerHTML = h;
  document.getElementById("loes").classList.toggle("an", loes);
  const b = L[idx]; if (!b) return;
  const pdf = loes && b.loes ? b.loes : b.pdf;
  document.getElementById("titel").textContent = b.titel + (loes ? " (Lösung)" : "");
  document.getElementById("unter").textContent = D[st].stufe + " | " + b.thema + (b.nr ? ", Blatt " + b.nr : "");
  document.getElementById("link").href = pdf;
  const bild = loes && b.loesbild.length ? b.loesbild : b.bild;
  document.getElementById("s1").src = bild[0]; document.getElementById("s2").src = bild[1];
  document.getElementById("a1").href = pdf; document.getElementById("a2").href = pdf;
  // Nachbarblatt vorladen, damit das Weiterblättern sofort geht
  const nb = L[(idx + 1) % L.length]; if (nb) (loes && nb.loesbild.length ? nb.loesbild : nb.bild).forEach(u => { new Image().src = u; });
  const a = document.querySelector("nav a.an"); if (a) a.scrollIntoView({block: "nearest"});
  try { localStorage.setItem("ueb", JSON.stringify({st, idx, loes})); } catch (e) {}
}
document.getElementById("tabs").onclick = e => { const i = e.target.dataset.i; if (i !== undefined) { st = +i; idx = 0; zeichne(); } };
document.getElementById("nav").onclick = e => { const a = e.target.closest("a"); if (a) { idx = +a.dataset.n; zeichne(); } };
document.getElementById("loes").onclick = () => { loes = !loes; zeichne(); };
document.addEventListener("keydown", e => {
  const n = liste().length;
  if (e.key === "ArrowDown" || e.key === "ArrowRight") { idx = (idx + 1) % n; zeichne(); e.preventDefault(); }
  else if (e.key === "ArrowUp" || e.key === "ArrowLeft") { idx = (idx - 1 + n) % n; zeichne(); e.preventDefault(); }
  else if (e.key === "l" || e.key === "L") { loes = !loes; zeichne(); }
  else if (["1", "2", "3"].includes(e.key)) { st = +e.key - 1; idx = 0; zeichne(); }
});
zeichne();
</script>
</body></html>
"""


def main():
    html = HTML.replace("__DATEN__", json.dumps(daten(), ensure_ascii=False))
    ziel = BASIS / "Übersicht.html"
    ziel.write_text(html, encoding="utf-8")
    if ICLOUD.exists():
        shutil.copy2(ziel, ICLOUD / ziel.name)
        shutil.copytree(VORSCHAU, ICLOUD / VORSCHAU.name, dirs_exist_ok=True)
    print("Übersicht:", ziel)


if __name__ == "__main__":
    main()
