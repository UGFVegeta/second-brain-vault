#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""Baut aus Angebote.html eine eigenständige Version zum Weitergeben (z. B. Windows-PC der Eltern).

Die Weitergabe-Version braucht keinen Dashboard-Dienst und kein Python: Sie fragt marktguru
direkt aus dem Browser ab (marktguru erlaubt das per CORS) und speichert Einstellungen,
den letzten Abruf und den Preisverlauf im Browser (localStorage).
Startwerte = aktuelle einstellungen.json. Nach Änderungen an Angebote.html einfach neu bauen:

    python3 .scripts/angebote_weitergabe_bauen.py
"""
import json
from pathlib import Path

import angebote_lib as L

QUELLE = L.ORDNER / "Angebote.html"
ZIEL = L.ORDNER / "Angebote zum Weitergeben.html"

MOTOR = r'''
// ---------- Abruf direkt bei marktguru (ohne Dienst) ----------
const API = "https://api.marktguru.de/api/v1/offers/search";
const KOPF = { "x-apikey": __APIKEY__, "x-clientkey": __CLIENTKEY__ };
const SYN = __SYN__;
const klein = t => (t || "").toLowerCase();
function stamm(w) { w = w.toLowerCase(); if (w.length >= 8) for (const e of ["es", "er", "en", "em", "e", "s"]) if (w.endsWith(e)) return w.slice(0, -e.length); return w; }
function varianten(w) { const s = stamm(w); const k = s.replace(/ü/g, "ue").replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ß/g, "ss"); return SYN[k] || SYN[s] || [s]; }
const woerterVon = b => b.trim().split(/\s+/).filter(Boolean);
function anfragen(b) {
  const a = [b.trim()];
  woerterVon(b).forEach(w => { a.push(stamm(w)); varianten(w).filter(v => v.length >= 5).forEach(v => a.push(v)); });
  return [...new Set(a)];
}
const lokal = iso => { if (!iso) return null; const d = new Date(iso); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
function aufbereiten(o) {
  const v = (o.validityDates || [{}])[0] || {};
  return {
    id: o.id, markt: ((o.advertisers || [{}])[0] || {}).name || "?",
    marke: (o.brand || {}).name || "", produkt: (o.product || {}).name || "", text: o.description || "",
    kategorie: ((o.categories || [{}])[0] || {}).name || "", preis: o.price, alt: o.oldPrice,
    grundpreis: o.referencePrice, einheit: (o.unit || {}).shortName || "", von: lokal(v.from), bis: lokal(v.to),
    karte: !!o.requiresLoyalityMembership, url: o.externalUrl || "",
    bild: `https://mg2de.b-cdn.net/api/v1/offers/${o.id}/images/default/0/small.jpg`,
  };
}
// Alle Anfragen für alle aktiven Orte, sechs gleichzeitig. Ergebnis: Anfrage -> Map(id -> Angebot)
async function abrufen(anfrageListe, fortschritt) {
  const plz = E.orte.filter(o => o.aktiv).map(o => o.plz);
  const jobs = []; anfrageListe.forEach(q => plz.forEach(p => jobs.push([q, p])));
  const erg = new Map(anfrageListe.map(q => [q, new Map()]));
  const gesamt = jobs.length; let fertig = 0, fehler = 0;
  async function arbeiter() {
    while (jobs.length) {
      const [q, p] = jobs.shift();
      try {
        const r = await fetch(API + "?" + new URLSearchParams({ as: "web", q, zipCode: p, limit: 250 }), { headers: KOPF });
        if (!r.ok) throw new Error(r.status);
        ((await r.json()).results || []).forEach(o => erg.get(q).set(o.id, o));
      } catch (e) { fehler++; }
      fertig++; if (fortschritt) fortschritt(fertig, gesamt);
    }
  }
  await Promise.all(Array.from({ length: 6 }, arbeiter));
  if (fehler === gesamt) throw new Error("Keine Verbindung zu marktguru. Ist der PC online? Sonst haben sich die Zugangsschlüssel geändert, dann bitte Oskar Bescheid geben.");
  return erg;
}
function auswerten(begriff, erg) {
  const roh = new Map();
  anfragen(begriff).forEach(q => (erg.get(q) || new Map()).forEach((o, id) => roh.set(id, o)));
  const ws = woerterVon(begriff), treffer = [], gesehen = new Set();
  for (const o of roh.values()) {
    const a = aufbereiten(o);
    if (a.bis && a.bis < heute) continue;
    const doppelt = [a.markt, klein(a.marke), klein(a.produkt), a.preis, a.von].join("|");
    if (gesehen.has(doppelt)) continue;
    gesehen.add(doppelt);
    const hay = klein([a.marke, a.produkt, a.text, a.kategorie].join(" "));
    if (ws.every(w => varianten(w).some(v => hay.includes(v)))) treffer.push(a);
  }
  treffer.sort((x, y) => ((x.grundpreis || x.preis || 999) - (y.grundpreis || y.preis || 999)) || ((x.preis || 999) - (y.preis || 999)));
  return treffer;
}
function regeln(f, t) {
  const txt = a => klein(`${a.marke} ${a.produkt} ${a.text}`);
  if (f.kategorien && f.kategorien.length) t = t.filter(a => f.kategorien.includes(a.kategorie));
  if (f.muss) t = t.filter(a => f.muss.every(m => new RegExp(m).test(txt(a))));
  if (f.ohne) t = t.filter(a => !f.ohne.some(w => txt(a).includes(w)));
  return t;
}
// Preisverlauf im Browser: zeigt, ob es ein Produkt früher schon günstiger gab
const schluessel = a => `${klein(a.marke)}|${klein(a.produkt)}|${klein(a.text)}`;
function mitBisher(treffer) {
  let v = lies("angebote-preise", {});
  for (const a of treffer) {
    const fr = (v[schluessel(a)] || []).filter(e => e[0] < (a.von || ""));
    a.bisher = fr.length ? (b => ({ preis: b[1], datum: b[0], markt: b[2] }))(fr.reduce((m, e) => e[1] < m[1] ? e : m)) : null;
  }
  for (const a of treffer) {
    if (a.preis == null) continue;
    const l = v[schluessel(a)] = v[schluessel(a)] || [], e = [a.von || heute, a.preis, a.markt];
    if (!l.some(x => x[0] === e[0] && x[1] === e[1] && x[2] === e[2])) { l.push(e); l.splice(0, Math.max(0, l.length - 30)); }
  }
  schreib("angebote-preise", v);
  return treffer;
}
function lies(k, standard) { try { const s = localStorage.getItem(k); return s ? JSON.parse(s) : standard; } catch (e) { return standard; } }
function schreib(k, wert) { try { localStorage.setItem(k, JSON.stringify(wert)); } catch (e) {} }
function merkeEinst() { schreib("angebote-einst", E); }
const zeigeFortschritt = (n, g) => { $("hinweis").className = "hinweis"; $("hinweis").textContent = `Holt Angebote … ${Math.round(100 * n / g)} %`; };
async function holen() {
  const alle = [...new Set(E.favoriten.flatMap(f => anfragen(f.suche || f.name)))];
  const erg = await abrufen(alle, zeigeFortschritt);
  const fav = {};
  for (const f of E.favoriten) fav[f.name] = mitBisher(regeln(f, auswerten(f.suche || f.name, erg)));
  const jetzt = new Date();
  D.stand = lokal(jetzt.toISOString()) + " " + String(jetzt.getHours()).padStart(2, "0") + ":" + String(jetzt.getMinutes()).padStart(2, "0");
  D.favoriten = fav;
  schreib("angebote-cache", D);
  $("hinweis").textContent = "";
}
async function suchen(q) { return mitBisher(auswerten(q, await abrufen(anfragen(q), zeigeFortschritt))); }
function standZeigen() {
  $("stand").textContent = D.stand ? "Stand " + tag(D.stand.slice(0, 10)) + " " + D.stand.slice(11) + " Uhr; "
    + E.orte.filter(o => o.aktiv).map(o => o.name).join(", ") : "Noch kein Abruf";
}
function fehlerZeigen(e) { $("hinweis").textContent = e.message; $("hinweis").className = "hinweis fehler"; }
'''

START = r'''// ---------- Start ----------
standZeigen();
einstellungenZeigen();
uebersicht();
if (!D.stand || D.stand.slice(0, 10) !== heute) {
  $("btnHolen").disabled = true;
  holen().then(() => { standZeigen(); einstellungenZeigen(); uebersicht(); }).catch(fehlerZeigen)
    .finally(() => { $("btnHolen").disabled = false; });
}
</script>'''


def ersetze(s, alt, neu):
    if alt not in s:
        raise SystemExit(f"Stelle nicht gefunden, Angebote.html hat sich geändert:\n{alt[:120]}")
    return s.replace(alt, neu)


def bauen():
    s = QUELLE.read_text(encoding="utf-8")
    e = L.einstellungen()
    motor = (MOTOR.replace("__APIKEY__", json.dumps(L.KOPF["x-apikey"]))
             .replace("__CLIENTKEY__", json.dumps(L.KOPF["x-clientkey"]))
             .replace("__SYN__", json.dumps(L.SYNONYME, ensure_ascii=False)))

    s = ersetze(s, '<script src="angebote_data.js"></script>\n', "")
    s = ersetze(s, '''const DIENST = "http://127.0.0.1:8765";
const D = window.ANGEBOTE || { stand: null, favoriten: {}, einstellungen: { orte: [], aus: [], favoriten: [] } };
let E = JSON.parse(JSON.stringify(D.einstellungen));''',
                "const STANDARD = " + json.dumps(e, ensure_ascii=False) + ''';
let E = lies("angebote-einst", STANDARD);
const D = lies("angebote-cache", { stand: null, favoriten: {} });''')
    # Speicherhelfer müssen vor der ersten Nutzung stehen (oben), der Rest des Motors kommt an die Stelle von dienst()
    s = ersetze(s, "<script>\n", "<script>\n" + '''function lies(k, standard) { try { const s = localStorage.getItem(k); return s ? JSON.parse(s) : standard; } catch (e) { return standard; } }
function schreib(k, wert) { try { localStorage.setItem(k, JSON.stringify(wert)); } catch (e) {} }
''')
    motor = motor.replace('''function lies(k, standard) { try { const s = localStorage.getItem(k); return s ? JSON.parse(s) : standard; } catch (e) { return standard; } }
function schreib(k, wert) { try { localStorage.setItem(k, JSON.stringify(wert)); } catch (e) {} }
''', "")
    a = s.index("async function dienst(pfad, body) {")
    b = s.index("$(\"suchform\").onsubmit")
    s = s[:a] + motor + "\n" + s[b:]
    s = ersetze(s, '''    const j = await dienst("/angebote/suche?q=" + encodeURIComponent(q));''',
                '''    const j = { treffer: await suchen(q) };''')
    s = ersetze(s, '''    $("hinweis").textContent = e instanceof TypeError ? keinDienst : e.message; $("hinweis").className = "hinweis fehler";
  }
};''', '''    fehlerZeigen(e);
  }
};''')
    s = ersetze(s, '''  try { await dienst("/angebote/aktualisieren", {}); location.reload(); }
  catch (e) { $("hinweis").textContent = e instanceof TypeError ? keinDienst : e.message; $("hinweis").className = "hinweis fehler"; b.disabled = false; b.textContent = "Jetzt aktualisieren"; }''',
                '''  try { await holen(); standZeigen(); einstellungenZeigen(); uebersicht(); }
  catch (e) { fehlerZeigen(e); }
  b.disabled = false; b.textContent = "Jetzt aktualisieren";''')
    s = ersetze(s, '''    dienst("/angebote/einstellungen", { aus: E.aus }).catch(() => {});''', "    merkeEinst();")
    s = ersetze(s, '''    await dienst("/angebote/einstellungen", { orte: E.orte, aus: E.aus, favoriten: E.favoriten });
    await dienst("/angebote/aktualisieren", {});
    location.reload();
  } catch (e) {
    $("hinweis").textContent = e instanceof TypeError ? keinDienst : e.message; $("hinweis").className = "hinweis fehler";
    b.disabled = false; b.textContent = "Speichern und neu holen";
  }''', '''    merkeEinst();
    await holen();
    standZeigen(); einstellungenZeigen(); uebersicht();
  } catch (e) {
    fehlerZeigen(e);
  }
  b.disabled = false; b.textContent = "Speichern und neu holen";''')
    a = s.index("// ---------- Start ----------")
    b = s.index("</script>", a) + len("</script>")
    s = s[:a] + START + s[b:]
    s = ersetze(s, "Rossmann und dm sind dort nicht vertreten.</p>",
                "Rossmann und dm sind dort nicht vertreten. Die Seite holt die Angebote beim ersten Öffnen am Tag selbst, "
                "das dauert etwa eine halbe Minute. Einstellungen und Preise bleiben in diesem Browser gespeichert.</p>")
    ZIEL.write_text(s, encoding="utf-8")
    return ZIEL


if __name__ == "__main__":
    print(bauen())
