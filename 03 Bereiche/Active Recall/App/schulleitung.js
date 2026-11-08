"use strict";

/* ---------- Helfer ---------- */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const view = $("#view");
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const enc = encodeURIComponent;
const ic = (n) => `<svg class="ic" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const datum = (iso) => (iso ? iso.slice(8, 10) + "." + iso.slice(5, 7) + "." : "");
const speicher = {
  lies(k) { try { return localStorage.getItem(k); } catch { return null; } },
  setz(k, v) { try { localStorage.setItem(k, v); } catch {} },
  weg(k) { try { localStorage.removeItem(k); } catch {} },
};
function toast(t) {
  const el = $("#toast"); el.textContent = t; el.hidden = false;
  clearTimeout(toast.h); toast.h = setTimeout(() => (el.hidden = true), 2800);
}
async function api(pfad, body) {
  const opt = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const r = await fetch("/api/sl/" + pfad, opt);
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || `Fehler ${r.status}`);
  return d;
}

/* Kleines Markdown: erst escapen, dann wenige Formen auszeichnen */
function inline(s) {
  return s
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/§§?\s*(\d+[a-z]?)(\s*(?:Abs\.|Absatz)\s*\d+[a-z]?)?(\s*(?:Satz|S\.)\s*\d+)?(\s*(?:Nr\.|Nummer)\s*\d+)?\s+SchG/g,
      (m, n) => `<a class="norm" href="#" data-nr="${n}">${m}</a>`);
}
function md(quelle) {
  const z = esc(quelle).split("\n"); let h = "", i = 0;
  while (i < z.length) {
    const t = z[i].trim();
    if (!t) { i++; continue; }
    let m;
    if ((m = t.match(/^(#{1,4})\s+(.*)$/))) { const e = Math.min(m[1].length + 1, 3); h += `<h${e}>${inline(m[2])}</h${e}>`; i++; continue; }
    if (t.startsWith("|") && z[i + 1] && /^\s*\|[\s:|-]+\|\s*$/.test(z[i + 1])) {
      const zellen = (r) => r.trim().replace(/^\||\|$/g, "").split("|").map((c) => inline(c.trim()));
      h += "<table><thead><tr>" + zellen(z[i]).map((c) => `<th>${c}</th>`).join("") + "</tr></thead><tbody>"; i += 2;
      while (i < z.length && z[i].trim().startsWith("|")) { h += "<tr>" + zellen(z[i]).map((c) => `<td>${c}</td>`).join("") + "</tr>"; i++; }
      h += "</tbody></table>"; continue;
    }
    if (/^[-*]\s+/.test(t) || /^\d+\.\s+/.test(t)) {
      const nr = /^\d+\./.test(t); h += nr ? "<ol>" : "<ul>";
      while (i < z.length && (nr ? /^\s*\d+\.\s+/ : /^\s*[-*]\s+/).test(z[i])) { h += "<li>" + inline(z[i].replace(/^\s*(?:[-*]|\d+\.)\s+/, "")) + "</li>"; i++; }
      h += nr ? "</ol>" : "</ul>"; continue;
    }
    const absatz = [];
    while (i < z.length && z[i].trim() && !/^(#{1,4}\s|\s*[-*]\s+|\s*\d+\.\s+|\s*\|)/.test(z[i])) { absatz.push(z[i].trim()); i++; }
    if (!absatz.length) { absatz.push(t); i++; }
    h += `<p>${inline(absatz.join(" "))}</p>`;
  }
  return h;
}

/* Paragrafen im aktuellen Schulgesetz nachschlagen */
async function normZeigen(nr) {
  try {
    const n = await api("norm?nr=" + enc(nr));
    $("#normTitel").textContent = `§ ${n.nr} SchG: ${n.titel}`;
    $("#normText").innerHTML = n.absaetze.map((a) => `<p>${esc(a)}</p>`).join("");
    $("#normDlg").showModal();
  } catch (e) { toast(e.message); }
}
document.addEventListener("click", (e) => {
  const a = e.target.closest("a.norm");
  if (a) { e.preventDefault(); normZeigen(a.dataset.nr); }
});
$("#normZu").onclick = () => $("#normDlg").close();

/* ---------- Claude-Seitenleiste ---------- */
const tutor = { kontext: null, verlauf: [], rating: null, beiAntwort: null, laeuft: false };
function tutorOeffnen(titel, kontext, chips = []) {
  tutor.kontext = kontext; tutor.verlauf = []; tutor.rating = null; tutor.beiAntwort = null;
  $("#tutorTitel").textContent = titel;
  $("#tutor").hidden = false; $("#shell").classList.add("offen");
  $("#tutorChips").innerHTML = chips.map((c) => `<button type="button">${esc(c)}</button>`).join("");
  $$("#tutorChips button").forEach((b) => (b.onclick = () => tutorSenden(b.textContent)));
  tutorZeichnen();
}
function tutorSchliessen() { $("#tutor").hidden = true; $("#shell").classList.remove("offen"); }
function tutorZeichnen(fehler) {
  const v = $("#tutorVerlauf");
  let h = tutor.verlauf.map((m) => m.rolle === "ich"
    ? `<div class="nachricht ich">${esc(m.text)}</div>`
    : `<div class="nachricht sie prosa">${md(m.text)}</div>`).join("");
  if (!tutor.verlauf.length && !tutor.laeuft) h = `<p class="leer">Frag nach, wenn etwas unklar ist. Claude prüft die Fundstellen in deinen aktuellen Rechtstexten.</p>`;
  if (tutor.laeuft) h += `<div class="laedt"><p>Claude prüft die Rechtslage, das dauert meist unter einer Minute.</p><i></i><i></i><i></i></div>`;
  if (fehler) h += `<div class="nachricht fehler">${esc(fehler)}</div>`;
  v.innerHTML = h; v.scrollTop = v.scrollHeight;
}
async function tutorSenden(text) {
  text = (text || "").trim();
  if (!text || tutor.laeuft) return;
  const vorher = [...tutor.verlauf];
  tutor.verlauf.push({ rolle: "ich", text });
  tutor.laeuft = true; $("#tutorSenden").disabled = true; tutorZeichnen();
  try {
    const d = await api("chat", { ...tutor.kontext, verlauf: vorher, nachricht: text });
    tutor.verlauf.push({ rolle: "sie", text: d.antwort });
    if (d.rating) tutor.rating = d.rating;
    tutor.laeuft = false; tutorZeichnen();
    if (tutor.beiAntwort) tutor.beiAntwort(d);
  } catch (e) {
    tutor.laeuft = false; tutorZeichnen(e.message);
  }
  $("#tutorSenden").disabled = false;
}
$("#tutorZu").onclick = tutorSchliessen;
$("#tutorForm").onsubmit = (e) => { e.preventDefault(); const t = $("#tutorText"); tutorSenden(t.value); t.value = ""; };
$("#tutorText").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); $("#tutorForm").requestSubmit(); }
});
$("#frageBtn").onclick = () => tutorOeffnen("Frage stellen", { modus: "frei" });

/* ---------- Router ---------- */
let D = null, aufraeumen = null;
async function route() {
  if (aufraeumen) { const a = aufraeumen; aufraeumen = null; await a(); }
  const [r = "heute", ...rest] = decodeURIComponent(location.hash.slice(2) || "heute").split("/");
  const arg = rest.join("/");
  const nav = { fall: "faelle", lernen: "karten", map: "mindmaps" }[r] || r;
  $$(".side a[data-r]").forEach((a) => {
    const an = a.dataset.r === nav; a.classList.toggle("on", an);
    if (an) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
  tutorSchliessen();
  try {
    D = await api("uebersicht");
    const seiten = { heute: seiteHeute, faelle: seiteFaelle, fall: seiteFall, karten: seiteKarten, lernen: seiteLernen, mindmaps: seiteMaps, map: seiteMap, wissen: seiteWissen };
    await (seiten[r] || seiteHeute)(arg);
    view.scrollTop = 0;
  } catch (e) {
    view.innerHTML = `<div class="seite"><h1>Das hat nicht geklappt</h1><p class="sub">${esc(e.message)}</p><div class="aktionen"><button class="b" onclick="location.reload()">Neu laden</button></div></div>`;
  }
}
window.addEventListener("hashchange", route);

const statusTag = (x) => x.status === "neu" ? `<span class="tag neu">neu</span>`
  : x.status === "faellig" ? `<span class="tag faellig">fällig</span>`
  : `<span class="tag">ab ${datum(x.faellig)}</span>`;
const balken = (a, b) => `<span class="balken" aria-hidden="true"><i style="width:${b ? Math.round((100 * a) / b) : 0}%"></i></span>`;
const kartenFaellig = () => D.karten.filter((k) => k.status === "faellig");

/* ---------- Heute ---------- */
function seiteHeute() {
  const w = D.aktuell, f = D.naechsterFall;
  const faellig = kartenFaellig().length;
  const neue = w ? D.karten.filter((k) => k.status === "neu" && String(k.woche) === String(w.woche)).length : 0;
  const kartenText = faellig ? `${faellig} Karten sind fällig` : neue ? `${neue} neue Karten zum Thema der Woche` : "Heute ist nichts fällig";
  const zuKarten = faellig ? "faellig" : w ? "woche-" + w.woche : "alle";
  const mapName = w ? `Woche ${String(w.woche).padStart(2, "0")}` : "Mindmap";
  const hatMap = D.mindmaps.some((m) => m.name === mapName);
  const verbund = D.faelle.filter((x) => ["Grundschule", "Werkrealschule und Verbund"].includes(x.gruppe));
  const vFertig = verbund.filter((x) => x.status !== "neu").length;
  const gestartet = w && w.start <= D.heute;

  view.innerHTML = `<div class="seite">
    <h1>Heute</h1>
    <p class="sub">${w ? `Woche ${w.woche} von ${D.wochen.length}: ${esc(w.thema)}${gestartet ? "" : `. Beginnt am ${datum(w.start)}`}` : "Kein Lernplan gefunden."}</p>
    <h2>Dran</h2>
    <div class="liste">
      <div class="zeile">${ic("fall")}<span class="wachs"><strong>Fall besprechen</strong><span class="info">${f ? esc(f.titel) : "Alle Fälle sind besprochen"}</span></span>${f ? `<a class="b" href="#/fall/${f.id}">Öffnen</a>` : ""}</div>
      <div class="zeile">${ic("karte")}<span class="wachs"><strong>Karten</strong><span class="info">${kartenText}</span></span>${faellig || neue ? `<a class="b ghost" href="#/lernen/${zuKarten}">Lernen</a>` : ""}</div>
      <div class="zeile">${ic("map")}<span class="wachs"><strong>Mindmap aus dem Kopf</strong><span class="info">Thema der Woche, gezeichnet oder als Foto</span></span><a class="b ghost" href="#/map/${enc(mapName)}">${hatMap ? "Weiter" : "Zeichnen"}</a></div>
      <div class="zeile">${ic("ohr")}<span class="wachs"><strong>Hören beim Sport</strong><span class="info">Audio-Folge in Gemini LM, Notizbuch Schulrecht BW aktuell</span></span><a class="b quiet" target="_blank" rel="noopener" href="https://notebook.google.com/notebook/9f1ced37-b319-4f8b-b421-1ad6b96ae747">Öffnen</a></div>
    </div>
    <h2>Lernplan bis Februar</h2>
    <div class="liste">
      ${D.wochen.map((x) => `<a class="zeile ${w && x.woche === w.woche ? "aktuell" : ""}" href="#/faelle/woche-${x.woche}">
        <span class="wachs"><strong>Woche ${x.woche}</strong><span class="info">${datum(x.start)} bis ${datum(x.ende)}, ${esc(x.thema)}</span></span>
        ${balken(x.faelleFertig, x.faelleGesamt)}<span class="wert">${x.faelleFertig} von ${x.faelleGesamt} Fällen</span></a>`).join("")}
      <a class="zeile" href="#/faelle/verbund"><span class="wachs"><strong>Grundschule, Werkrealschule, Verbund</strong><span class="info">Zusätzlich zum Plan, für das Schulzentrum</span></span>${balken(vFertig, verbund.length)}<span class="wert">${vFertig} von ${verbund.length} Fällen</span></a>
    </div>
  </div>`;
}

/* ---------- Fälle ---------- */
function seiteFaelle(arg) {
  let auswahl = D.faelle, titel = "Fälle", unter = `${D.faelle.length} Fälle. Die Rückmeldung prüft jede Antwort gegen die aktuellen Rechtstexte.`;
  if (arg.startsWith("woche-")) {
    const w = D.wochen.find((x) => "woche-" + x.woche === arg);
    if (w) { auswahl = w.fallIds.map((i) => D.faelle.find((f) => f.id === i)).filter(Boolean); titel = `Woche ${w.woche}`; unter = w.thema; }
  } else if (arg === "verbund") {
    auswahl = D.faelle.filter((x) => ["Grundschule", "Werkrealschule und Verbund"].includes(x.gruppe));
    titel = "Grundschule, Werkrealschule, Verbund"; unter = "Eigene Trainingsfälle für das Schulzentrum, erfunden und gegen das aktuelle Recht geprüft.";
  }
  const gruppen = [...new Set(auswahl.map((f) => f.gruppe))];
  view.innerHTML = `<div class="seite">
    ${arg ? `<a class="zurueck" href="#/faelle">${ic("zurueck")}Alle Fälle</a>` : ""}
    <h1>${esc(titel)}</h1><p class="sub">${esc(unter)}</p>
    ${auswahl.length ? gruppen.map((g) => `<h2>${esc(g)}</h2><div class="liste">${auswahl.filter((f) => f.gruppe === g).map((f) =>
      `<a class="zeile" href="#/fall/${f.id}"><span class="wachs">${esc(f.titel)}</span>${statusTag(f)}</a>`).join("")}</div>`).join("")
      : `<p class="hinweis">In dieser Woche sind keine Fälle aus deiner Sammlung eingeplant. Der Lernplan sieht dafür gemischte Runden vor, nimm dafür einen fälligen Fall aus der Gesamtliste.</p>`}
  </div>`;
}

const SCHEMA = ["Was ist passiert?", "Welche Rechtsfrage?", "Welche Norm?", "Abwägung", "Entscheidung", "Nächste Schritte"];
const BEWERTUNG = [["nochmal", "Vergessen"], ["schwer", "Schwer"], ["gut", "Gut"], ["leicht", "Leicht"]];

async function seiteFall(id) {
  const f = await api("fall?id=" + enc(id));
  const eintrag = D.faelle.find((x) => x.id === id);
  const key = "sl-entwurf-" + id;
  view.innerHTML = `<div class="seite">
    <a class="zurueck" href="#/faelle">${ic("zurueck")}Alle Fälle</a>
    <h1>${esc(f.titel)}</h1>
    <p class="sub">${esc(f.gruppe)}${eintrag && eintrag.status !== "neu" ? `, zuletzt besprochen` : ""}</p>
    <div class="fall-text prosa">${md(f.text)}</div>
    <ol class="schema">${SCHEMA.map((s) => `<li>${s}</li>`).join("")}</ol>
    <label class="feld-titel" for="antwort">Deine Antwort</label>
    <textarea id="antwort" placeholder="Frei antworten. Cursor hier, dann mit WhisperBar diktieren."></textarea>
    <p class="hinweis">Echte Namen von Schülern oder Kollegen gehören hier nicht hinein.</p>
    <div class="abschnitt"><span class="feld-titel">Wie sicher bist du?</span>
      <div class="seg" id="selbst">${BEWERTUNG.map(([v]) => `<button type="button" data-v="${v}">${{ nochmal: "unsicher", schwer: "eher unsicher", gut: "eher sicher", leicht: "sicher" }[v]}</button>`).join("")}</div>
    </div>
    <div class="aktionen">
      <button class="b" id="senden" disabled>Rückmeldung holen</button>
      <button class="b ghost" id="tipp">${ic("tipp")}Tipp</button>
    </div>
    <section class="abschluss" id="abschluss" hidden>
      <span class="feld-titel">Wie lief der Fall?</span>
      <p class="vorschlag" id="vorschlag"></p>
      <div class="seg" id="ende">${BEWERTUNG.map(([v, t]) => `<button type="button" data-v="${v}">${t}</button>`).join("")}</div>
      <details class="loesung"><summary>Musterlösung ansehen</summary><div class="prosa" id="loesung"></div></details>
    </section>
  </div>`;

  const ta = $("#antwort"); ta.value = speicher.lies(key) || "";
  let selbst = null, abgesendet = false;
  const pruefen = () => ($("#senden").disabled = !(ta.value.trim() && selbst));
  ta.oninput = () => { speicher.setz(key, ta.value); pruefen(); };
  $$("#selbst button").forEach((b) => (b.onclick = () => {
    selbst = b.dataset.v; $$("#selbst button").forEach((x) => x.classList.toggle("on", x === b)); pruefen();
  }));
  $("#tipp").onclick = () => {
    tutorOeffnen("Tipp", { modus: "tipp", id });
    tutorSenden("Gib mir einen Denkanstoß, ohne die Lösung zu verraten.");
  };
  const zeigeAbschluss = () => {
    $("#abschluss").hidden = false;
    const t = { nochmal: "Vergessen", schwer: "Schwer", gut: "Gut", leicht: "Leicht" }[tutor.rating];
    $("#vorschlag").textContent = t ? `Vorschlag von Claude: ${t}. Das bestimmt, wann der Fall wiederkommt.` : "Das bestimmt, wann der Fall wiederkommt.";
    $$("#ende button").forEach((b) => b.classList.toggle("on", b.dataset.v === tutor.rating));
  };
  $("#senden").onclick = () => {
    abgesendet = true;
    tutorOeffnen("Rückmeldung", { modus: "fall", id, selbst });
    tutor.beiAntwort = zeigeAbschluss;
    tutorSenden(ta.value);
  };
  $("details.loesung").addEventListener("toggle", async function () {
    if (!this.open || $("#loesung").innerHTML) return;
    const v = await api("fall?id=" + enc(id) + "&loesung=1");
    $("#loesung").innerHTML = md(v.loesung) + `<p class="hinweis">Stand der Sammlung etwa 2022, außer bei den eigenen Verbund-Fällen.</p>`;
  });
  $$("#ende button").forEach((b) => (b.onclick = async () => {
    try {
      await api("fall/abschluss", { id, antwort: ta.value, selbst, rating: b.dataset.v, verlauf: tutor.verlauf });
      speicher.weg(key); toast("Gesichert. Der Fall kommt wieder, wenn er dran ist.");
      location.hash = "#/heute";
    } catch (e) { toast(e.message); }
  }));
  // Ohne Anmeldung soll der Fall trotzdem abgeschlossen werden können
  aufraeumen = () => { if (abgesendet && ta.value) speicher.setz(key, ta.value); };
  const beobachter = new MutationObserver(() => { if ($(".nachricht.fehler") && $("#abschluss")) zeigeAbschluss(); });
  beobachter.observe($("#tutorVerlauf"), { childList: true });
  const frueher = aufraeumen; aufraeumen = () => { beobachter.disconnect(); frueher(); };
}

/* ---------- Karten ---------- */
function seiteKarten() {
  const themen = [...new Set(D.karten.map((k) => k.thema))];
  const faellig = kartenFaellig().length;
  view.innerHTML = `<div class="seite">
    <h1>Karten</h1><p class="sub">Für das, was sitzen muss: Normen, Fristen, Zuständigkeiten, Zahlen.</p>
    <div class="aktionen">${faellig ? `<a class="b" href="#/lernen/faellig">${faellig} fällige Karten lernen</a>` : ""}<a class="b ghost" href="#/lernen/alle">Alles Neue und Fällige</a></div>
    <h2>Themen</h2>
    <div class="liste">${themen.map((t) => {
      const k = D.karten.filter((x) => x.thema === t), fest = k.filter((x) => x.level >= 2).length;
      const offen = k.filter((x) => x.status !== "spaeter").length;
      return `<a class="zeile" href="#/lernen/thema-${enc(t)}"><span class="wachs"><strong>${esc(t)}</strong><span class="info">${k.length} Karten, ${offen} jetzt offen</span></span>${balken(fest, k.length)}<span class="wert">${fest} gefestigt</span></a>`;
    }).join("")}</div>
  </div>`;
}

function seiteLernen(arg) {
  let pool = D.karten.filter((k) => k.status !== "spaeter");
  if (arg === "faellig") pool = kartenFaellig();
  else if (arg.startsWith("woche-")) pool = pool.filter((k) => "woche-" + k.woche === arg);
  else if (arg.startsWith("thema-")) pool = pool.filter((k) => k.thema === arg.slice(6));
  pool.sort((a, b) => (a.status === "faellig" ? 0 : 1) - (b.status === "faellig" ? 0 : 1));
  const warte = pool.slice(); let karte = null, aufgedeckt = false, erledigt = 0;
  const wdh = new Set();

  const intervall = (r) => {
    let l = karte.level;
    if (r === "nochmal") return "gleich wieder";
    if (r === "gut") l += 1; if (r === "leicht") l += 2;
    const t = D.intervalle[Math.min(l, D.intervalle.length - 1)];
    return t === 1 ? "morgen" : `in ${t} Tagen`;
  };
  function zeichne() {
    if (!karte) {
      view.innerHTML = `<div class="stapel"><div class="fertig"><h1>${erledigt ? "Fertig für heute" : "Hier ist gerade nichts offen"}</h1>
        <p class="sub">${erledigt ? `${erledigt} Karten bearbeitet.` : "Neue Karten kommen mit dem Thema der Woche."}</p>
        <div class="aktionen" style="justify-content:center"><a class="b" href="#/heute">Zu Heute</a><a class="b ghost" href="#/karten">Alle Themen</a></div></div></div>`;
      return;
    }
    view.innerHTML = `<div class="stapel">
      <div class="stapel-kopf"><a class="zurueck" style="margin:0" href="#/karten">${ic("zurueck")}Karten</a><span>${warte.length + 1} übrig</span></div>
      <article class="lernkarte">
        <p class="thema">${esc(karte.thema)}</p>
        <p class="frage">${esc(karte.frage)}</p>
        <p class="tippbox" id="tippbox" hidden>${esc(karte.tipp)}</p>
        ${aufgedeckt ? `<div class="antwort prosa">${inline(esc(karte.antwort))}
          ${karte.warum ? `<p class="warum">${inline(esc(karte.warum))}</p>` : ""}
          ${karte.quelle ? `<p class="quelle">${inline(esc(karte.quelle))}</p>` : ""}</div>` : ""}
        <div class="unten">
          ${aufgedeckt
            ? `<div class="grade">${BEWERTUNG.map(([v, t], i) => `<button type="button" data-v="${v}"><strong>${t}<kbd>${i + 1}</kbd></strong><span>${intervall(v)}</span></button>`).join("")}</div>
               <div class="aktionen"><button class="b quiet" id="fragen">${ic("chat")}Unklar? Claude fragen</button></div>`
            : `<div class="aktionen"><button class="b" id="zeigen">Antwort zeigen</button>${karte.tipp ? `<button class="b ghost" id="tipp">${ic("tipp")}Tipp</button>` : ""}</div>`}
        </div>
      </article>
    </div>`;
    if ($("#zeigen")) $("#zeigen").onclick = aufdecken;
    if ($("#tipp")) $("#tipp").onclick = () => ($("#tippbox").hidden = false);
    if ($("#fragen")) $("#fragen").onclick = fragen;
    $$(".grade button").forEach((b) => (b.onclick = () => werten(b.dataset.v)));
  }
  const aufdecken = () => { aufgedeckt = true; zeichne(); };
  const fragen = () => tutorOeffnen("Zur Karte", { modus: "karte", id: karte.id }, ["Warum ist das so?", "Gib mir ein Beispiel aus dem Schulalltag", "Eine Eselsbrücke, bitte"]);
  const naechste = () => { karte = warte.shift() || null; aufgedeckt = false; zeichne(); };
  async function werten(r) {
    const k = karte;
    try {
      await api("bewerten", { art: "karte", id: k.id, rating: r });
      if (r === "nochmal" && !wdh.has(k.id)) { wdh.add(k.id); warte.push({ ...k, level: 0 }); }
      else erledigt++;
      tutorSchliessen(); naechste();
    } catch (e) { toast(e.message); }
  }
  const tasten = (e) => {
    if (e.target.closest("textarea,input") || $("#normDlg").open) return;
    if (e.code === "Space" && !aufgedeckt && karte) { e.preventDefault(); aufdecken(); }
    else if (aufgedeckt && karte && ["1", "2", "3", "4"].includes(e.key)) werten(BEWERTUNG[+e.key - 1][0]);
  };
  document.addEventListener("keydown", tasten);
  aufraeumen = () => document.removeEventListener("keydown", tasten);
  naechste();
}

/* ---------- Mindmaps ---------- */
function seiteMaps() {
  const w = D.aktuell, vorschlag = w ? `Woche ${String(w.woche).padStart(2, "0")}` : "";
  view.innerHTML = `<div class="seite">
    <h1>Mindmaps</h1><p class="sub">Aus dem Kopf aufbauen, danach mit Claude abgleichen. Gezeichnet oder als Foto deiner Handskizze.</p>
    <div class="neu-zeile">
      <input id="mapName" aria-label="Thema der Mindmap" placeholder="Thema, zum Beispiel Aufsichtspflicht" value="${esc(vorschlag)}">
      <button class="b" id="mapNeu">Zeichnen</button>
      <button class="b ghost" id="fotoBtn">${ic("foto")}Foto hochladen</button>
      <input id="fotoDatei" type="file" accept="image/jpeg,image/png" hidden>
    </div>
    <h2>Vorhanden</h2>
    ${D.mindmaps.length ? `<div class="liste">${D.mindmaps.map((m) =>
      `<a class="zeile" href="#/map/${enc(m.name)}">${ic(m.art === "foto" ? "foto" : "map")}<span class="wachs"><strong>${esc(m.name)}</strong><span class="info">${m.art === "foto" ? "Foto" : "Zeichnung"}, ${m.datum}</span></span></a>`).join("")}</div>`
      : `<p class="hinweis">Noch keine Mindmap. Nimm das Thema der Woche, schließ die Unterlagen und fang in der Mitte an.</p>`}
  </div>`;
  const name = () => $("#mapName").value.trim();
  $("#mapNeu").onclick = () => { if (name()) location.hash = "#/map/" + enc(name()); else toast("Gib zuerst ein Thema ein."); };
  $("#mapName").onkeydown = (e) => { if (e.key === "Enter") $("#mapNeu").click(); };
  $("#fotoBtn").onclick = () => { if (name()) $("#fotoDatei").click(); else toast("Gib zuerst ein Thema ein."); };
  $("#fotoDatei").onchange = async (e) => {
    const f = e.target.files[0]; if (!f) return;
    try {
      const bild = await verkleinern(f);
      const d = await api("foto", { name: name(), bild });
      location.hash = "#/map/" + enc(d.name);
    } catch (err) { toast(err.message); }
  };
}
function verkleinern(datei) {
  return new Promise((ok, nein) => {
    const url = URL.createObjectURL(datei), img = new Image();
    img.onload = () => {
      const f = Math.min(1, 2000 / Math.max(img.width, img.height));
      const c = document.createElement("canvas"); c.width = img.width * f; c.height = img.height * f;
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(url); ok(c.toDataURL("image/jpeg", 0.85));
    };
    img.onerror = () => nein(new Error("Das Bild ließ sich nicht öffnen. Bitte ein JPG oder PNG verwenden."));
    img.src = url;
  });
}

function laden(src) {
  return new Promise((ok, nein) => {
    if ($(`script[src="${src}"]`)) return ok();
    const s = document.createElement("script"); s.src = src; s.onload = ok;
    s.onerror = () => nein(new Error("Der Zeichen-Editor ließ sich nicht laden. Besteht eine Internetverbindung?"));
    document.head.appendChild(s);
  });
}
const EXCALIDRAW = "https://unpkg.com/@excalidraw/excalidraw@0.17.6/dist/";
async function editorLaden() {
  window.EXCALIDRAW_ASSET_PATH = EXCALIDRAW;
  await laden("https://unpkg.com/react@18.3.1/umd/react.production.min.js");
  await laden("https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js");
  await laden(EXCALIDRAW + "excalidraw.production.min.js");
}
function gliederung(elemente) {
  const da = elemente.filter((e) => !e.isDeleted), nachId = new Map(da.map((e) => [e.id, e]));
  const texte = da.filter((e) => e.type === "text");
  const beschriftung = (e) => !e ? "" : e.type === "text" ? e.text : (texte.find((t) => t.containerId === e.id) || {}).text || "";
  const pfeile = da.filter((e) => e.type === "arrow").map((a) => {
    const v = beschriftung(nachId.get(a.startBinding && a.startBinding.elementId));
    const n = beschriftung(nachId.get(a.endBinding && a.endBinding.elementId));
    return v && n ? `${v} -> ${n}` : null;
  }).filter(Boolean);
  const begriffe = texte.map((t) => t.text.replace(/\s+/g, " ").trim()).filter(Boolean);
  return `Begriffe:\n- ${begriffe.join("\n- ")}\n\nVerbindungen:\n${pfeile.length ? "- " + pfeile.join("\n- ") : "(keine verbundenen Pfeile)"}`;
}

async function seiteMap(name) {
  const m = await api("mindmap?name=" + enc(name));
  const kopf = (rechts) => `<div class="map-kopf"><a class="zurueck" style="margin:0" href="#/mindmaps">${ic("zurueck")}Mindmaps</a><strong>${esc(m.name)}</strong>${rechts}</div>`;
  const chips = ["Was fehlt am meisten?", "Prüf mich zu einem Ast ab"];
  const abgleich = "Gleich meine Mindmap mit dem Thema ab.";
  if (m.art === "foto") {
    view.innerHTML = `<div class="map-seite">${kopf(`<button class="b" id="abgleich">Mit Claude abgleichen</button>`)}<div class="map-foto"><img src="${esc(m.bild)}" alt="Foto der Mindmap ${esc(m.name)}"></div></div>`;
    $("#abgleich").onclick = () => { tutorOeffnen("Abgleich", { modus: "mindmap", name: m.name, foto: true }, chips); tutorSenden(abgleich); };
    return;
  }
  view.innerHTML = `<div class="map-seite">${kopf(`<span class="map-status" id="mapStatus" role="status">Editor lädt</span><button class="b" id="abgleich" disabled>Mit Claude abgleichen</button>`)}<div class="map-flaeche" id="flaeche"></div></div>`;
  await editorLaden();
  if (!$("#flaeche")) return;
  const dunkel = matchMedia("(prefers-color-scheme: dark)").matches;
  const start = m.daten || {
    elements: ExcalidrawLib.convertToExcalidrawElements([{ type: "rectangle", x: 0, y: 0, width: 280, height: 90, strokeColor: "#2f6299", backgroundColor: "#e8eef5", label: { text: m.name, fontSize: 22 } }]),
    appState: {},
  };
  let elemente = start.elements, stempel = null, timer = null, offen = false;
  const summe = (es) => es.length + ":" + es.reduce((a, e) => a + e.version, 0);
  stempel = summe(start.elements);
  const speichern = async () => {
    clearTimeout(timer); if (!offen) return; offen = false;
    try {
      await api("mindmap", { name: m.name, daten: { type: "excalidraw", version: 2, source: "schulleitung", elements: elemente.filter((e) => !e.isDeleted), appState: { viewBackgroundColor: "#ffffff" }, files: {} } });
      if ($("#mapStatus")) $("#mapStatus").textContent = "Gespeichert";
    } catch (e) { if ($("#mapStatus")) $("#mapStatus").textContent = "Nicht gespeichert: " + e.message; }
  };
  const wurzel = ReactDOM.createRoot($("#flaeche"));
  wurzel.render(React.createElement(ExcalidrawLib.Excalidraw, {
    initialData: { elements: start.elements, appState: { ...(start.appState || {}), viewBackgroundColor: dunkel ? "#121212" : "#ffffff" }, scrollToContent: true },
    langCode: "de-DE", theme: dunkel ? "dark" : "light",
    excalidrawAPI: (a) => { window.slEditor = a; },
    onChange: (es) => {
      const s = summe(es); if (s === stempel) return;
      stempel = s; elemente = es; offen = true;
      if ($("#mapStatus")) $("#mapStatus").textContent = "Speichert";
      clearTimeout(timer); timer = setTimeout(speichern, 1000);
    },
  }));
  $("#mapStatus").textContent = m.daten ? "Gespeichert" : "Neu";
  $("#abgleich").disabled = false;
  $("#abgleich").onclick = () => {
    tutorOeffnen("Abgleich", { modus: "mindmap", name: m.name, gliederung: gliederung(elemente) }, chips);
    tutorSenden(abgleich);
  };
  aufraeumen = async () => { await speichern(); wurzel.unmount(); };
}

/* ---------- Wissen ---------- */
async function seiteWissen(name) {
  if (name) {
    const w = await api("wissen?name=" + enc(name));
    view.innerHTML = `<div class="seite"><a class="zurueck" href="#/wissen">${ic("zurueck")}Wissen</a><div class="prosa">${md(w.text)}</div></div>`;
    return;
  }
  view.innerHTML = `<div class="seite">
    <h1>Wissen</h1><p class="sub">Daten und Fakten für das Schulzentrum, jeweils mit Stand.</p>
    <h2>Seiten</h2>
    <div class="liste">${D.wissen.map((n) => `<a class="zeile" href="#/wissen/${enc(n)}">${ic("buch")}<span class="wachs"><strong>${esc(n)}</strong></span></a>`).join("")}</div>
    <h2>Schulgesetz nachschlagen</h2>
    <p class="sub">Aktueller Text, Stand 16.12.2025.</p>
    <form class="such-zeile" id="such"><input id="nr" aria-label="Paragraf" placeholder="Paragraf, zum Beispiel 90 oder 30b"><button class="b ghost">Anzeigen</button></form>
  </div>`;
  $("#such").onsubmit = (e) => { e.preventDefault(); const n = $("#nr").value.replace(/[^0-9a-z]/gi, ""); if (n) normZeigen(n); };
}

route();
