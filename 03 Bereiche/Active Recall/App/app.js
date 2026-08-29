"use strict";

/* ---------- kleine Helfer ---------- */
const $ = (s, r = document) => r.querySelector(s);
const view = $("#view");
const todayISO = () => new Date().toLocaleDateString("sv-SE"); // YYYY-MM-DD
const esc = (s) => (s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function toast(msg) {
  const t = $("#toast"); t.textContent = msg; t.hidden = false;
  clearTimeout(toast._t); toast._t = setTimeout(() => (t.hidden = true), 2600);
}

/* Spaced Repetition: Intervalle in Tagen je Stufe (SR-Level 0..6) */
const INTERVALS = [1, 2, 4, 9, 19, 40, 85];
function nextLevel(level, rating) {
  level = Number(level) || 0;
  if (rating === "nochmal") return 0;
  if (rating === "schwer") return level;
  if (rating === "gut") return Math.min(INTERVALS.length - 1, level + 1);
  if (rating === "leicht") return Math.min(INTERVALS.length - 1, level + 2);
  return level;
}
function dueFrom(level) {
  const d = new Date();
  d.setDate(d.getDate() + INTERVALS[Math.min(level, INTERVALS.length - 1)]);
  return d.toLocaleDateString("sv-SE");
}
function dots(level) {
  level = Math.max(0, Math.min(6, Number(level) || 0));
  let s = "";
  for (let i = 0; i < 6; i++) s += i < level ? "●" : "<span class='off'>●</span>";
  return `<span class="dots">${s}</span>`;
}

/* ---------- Frontmatter ---------- */
function parseFM(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n*/);
  const fm = {};
  let body = text;
  if (m) {
    body = text.slice(m[0].length);
    for (const line of m[1].split("\n")) {
      const mm = line.match(/^([A-Za-z0-9_]+):\s?(.*)$/);
      if (!mm) continue;
      let v = mm[2].trim();
      if (/^".*"$/.test(v) || /^'.*'$/.test(v)) v = v.slice(1, -1);
      fm[mm[1]] = v;
    }
  }
  return { fm, body };
}
function serializeFM(fm, body) {
  const lines = Object.entries(fm).map(([k, v]) => {
    const s = String(v ?? "");
    return /[:#"']/.test(s) || s === "" ? `${k}: "${s.replace(/"/g, "'")}"` : `${k}: ${s}`;
  });
  return `---\n${lines.join("\n")}\n---\n\n${body}`;
}

/* ---------- IndexedDB: Ordner-Handle merken ---------- */
function idb() {
  return new Promise((res, rej) => {
    const r = indexedDB.open("active-recall", 1);
    r.onupgradeneeded = () => r.result.createObjectStore("kv");
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
}
async function idbGet(k) {
  const db = await idb();
  return new Promise((res, rej) => {
    const t = db.transaction("kv").objectStore("kv").get(k);
    t.onsuccess = () => res(t.result); t.onerror = () => rej(t.error);
  });
}
async function idbSet(k, v) {
  const db = await idb();
  return new Promise((res, rej) => {
    const t = db.transaction("kv", "readwrite").objectStore("kv").put(v, k);
    t.onsuccess = () => res(); t.onerror = () => rej(t.error);
  });
}

/* ---------- Dateisystem ---------- */
let ROOT = null; // FileSystemDirectoryHandle des Ordners "Active Recall"

async function verifyPermission(handle) {
  const opts = { mode: "readwrite" };
  if ((await handle.queryPermission(opts)) === "granted") return true;
  if ((await handle.requestPermission(opts)) === "granted") return true;
  return false;
}
async function getDir(path, create = false) {
  let dir = ROOT;
  for (const part of path.split("/").filter(Boolean)) {
    dir = await dir.getDirectoryHandle(part, { create });
  }
  return dir;
}
async function readFile(path) {
  try {
    const parts = path.split("/");
    const name = parts.pop();
    const dir = await getDir(parts.join("/"), false);
    const fh = await dir.getFileHandle(name);
    return await (await fh.getFile()).text();
  } catch { return null; }
}
async function writeFile(path, data) {
  const parts = path.split("/");
  const name = parts.pop();
  const dir = await getDir(parts.join("/"), true);
  const fh = await dir.getFileHandle(name, { create: true });
  const w = await fh.createWritable();
  await w.write(data);
  await w.close();
}
async function listDir(path) {
  const out = [];
  try {
    const dir = await getDir(path, false);
    for await (const [nm, h] of dir.entries()) out.push({ name: nm, kind: h.kind });
  } catch {}
  return out;
}

/* ---------- Datenmodell ---------- */
const PROJ = "Projekte";
function slug(title) {
  return title.trim().replace(/[\/\\:*?"<>|]/g, "").replace(/\s+/g, " ").slice(0, 80) || "Projekt";
}
async function uniqueProjectDir(title) {
  const base = slug(title);
  const existing = new Set((await listDir(PROJ)).filter((e) => e.kind === "directory").map((e) => e.name));
  if (!existing.has(base)) return base;
  let i = 2;
  while (existing.has(`${base} ${i}`)) i++;
  return `${base} ${i}`;
}
async function listProjects() {
  const dirs = (await listDir(PROJ)).filter((e) => e.kind === "directory");
  const res = [];
  for (const d of dirs) {
    const txt = await readFile(`${PROJ}/${d.name}/projekt.md`);
    if (!txt) continue;
    const { fm } = parseFM(txt);
    res.push({ dir: d.name, ...fm });
  }
  res.sort((a, b) => (a.faellig || "9999").localeCompare(b.faellig || "9999") || (b.angelegt || "").localeCompare(a.angelegt || ""));
  return res;
}
async function listSessions(dir) {
  const files = (await listDir(`${PROJ}/${dir}/sessions`)).filter((e) => e.name.endsWith(".md"));
  const res = [];
  for (const f of files) {
    const txt = await readFile(`${PROJ}/${dir}/sessions/${f.name}`);
    const { fm } = parseFM(txt || "");
    res.push({ file: f.name, ...fm });
  }
  res.sort((a, b) => (b.datum || "").localeCompare(a.datum || ""));
  return res;
}

async function createProject({ title, quelle, umfang, refText, upload }) {
  const dir = await uniqueProjectDir(title);
  const p = `${PROJ}/${dir}`;
  const now = todayISO();

  const projFM = {
    tags: "[active-recall]", typ: "recall-projekt", status: "aktiv", title,
    angelegt: now, quelle, umfang: umfang || "", sr_level: 0,
    zuletzt: "", faellig: now, sessions: 0,
  };
  const projBody =
`# ${title}

**Quelle:** ${quelle}${umfang ? ` · **Umfang:** ${umfang}` : ""}
**Angelegt:** ${now}

Referenz-Datei: \`referenz.md\` (im selben Ordner)
Sessions: Ordner \`sessions/\`

> Feedback und Wiederholungs-Planung laufen über eine Claude-Code-Session.
> Trigger: „Active Recall durchgehen".
`;
  await writeFile(`${p}/projekt.md`, serializeFM(projFM, projBody));

  let refFM, refBody;
  if (upload) {
    await writeFile(`${p}/uploads/${upload.name}`, upload);
    refFM = { tags: "[active-recall]", typ: "recall-referenz", status: "offen", quelldatei: `uploads/${upload.name}` };
    refBody = `# Referenz – ${title}\n\n_Status: offen. Von Claude aus \`uploads/${upload.name}\` zu extrahieren._\n`;
  } else {
    refFM = { tags: "[active-recall]", typ: "recall-referenz", status: "bereit", quelldatei: "" };
    refBody = `# Referenz – ${title}\n\n${refText || ""}\n`;
  }
  await writeFile(`${p}/referenz.md`, serializeFM(refFM, refBody));
  return dir;
}

async function saveSession(dir, { text, modus, umfang, selbst }) {
  const projTxt = await readFile(`${PROJ}/${dir}/projekt.md`);
  const { fm, body } = parseFM(projTxt);
  const lvlBefore = Number(fm.sr_level) || 0;

  const d = new Date();
  const stamp = d.toLocaleDateString("sv-SE") + "-" + String(d.getHours()).padStart(2, "0") + String(d.getMinutes()).padStart(2, "0");
  let file = `${stamp}.md`;
  const taken = new Set((await listDir(`${PROJ}/${dir}/sessions`)).map((e) => e.name));
  let n = 2; while (taken.has(file)) file = `${stamp}-${n++}.md`;

  const sFM = {
    tags: "[active-recall, recall-session]", typ: "recall-session",
    projekt: fm.title || dir, datum: d.toLocaleString("sv-SE").slice(0, 16),
    modus, umfang: umfang || fm.umfang || "", selbsteinschaetzung: selbst,
    feedback_status: "offen", sr_level_vor: lvlBefore,
  };
  const sBody =
`## Abruf

${text.trim()}

## Feedback

_Offen — wird in der nächsten Claude-Session ergänzt (Trigger: „Active Recall durchgehen")._
`;
  await writeFile(`${PROJ}/${dir}/sessions/${file}`, serializeFM(sFM, sBody));

  // vorläufige Planung aus der Selbsteinschätzung (Claude kann überschreiben)
  const lvl = nextLevel(lvlBefore, selbst);
  fm.sr_level = lvl;
  fm.zuletzt = todayISO();
  fm.faellig = dueFrom(lvl);
  fm.sessions = (Number(fm.sessions) || 0) + 1;
  await writeFile(`${PROJ}/${dir}/projekt.md`, serializeFM(fm, body));
  return file;
}

/* ---------- Router ---------- */
window.addEventListener("hashchange", route);
function go(h) { location.hash = h; }
function route() {
  if (!ROOT) return renderConnect();
  const h = decodeURIComponent(location.hash.slice(1) || "/");
  const parts = h.split("/").filter(Boolean);
  if (h === "/" || !parts.length) return renderDashboard();
  if (parts[0] === "new") return renderNew();
  if (parts[0] === "p" && parts[2] === "recall") return renderRecall(parts[1]);
  if (parts[0] === "p" && parts[2] === "s") return renderSession(parts[1], parts.slice(3).join("/"));
  if (parts[0] === "p") return renderProject(parts[1]);
  renderDashboard();
}
function crumbs(items) {
  $("#crumbs").innerHTML = items
    .map((it, i) => (i < items.length - 1 && it.h ? `<a data-h="${it.h}">${esc(it.t)}</a><span>›</span>` : `<span>${esc(it.t)}</span>`))
    .join("");
  $("#crumbs").querySelectorAll("a").forEach((a) => (a.onclick = () => go(a.dataset.h)));
}

/* ---------- Views ---------- */
function renderConnect() {
  crumbs([]);
  view.innerHTML = `
    <div class="empty">
      <h2>Ordner verbinden</h2>
      <p class="muted">Verbinde einmalig den Vault-Ordner <code>03 Bereiche/Active Recall</code>.<br>
      Chrome merkt sich die Freigabe.</p>
      <p style="margin-top:1.2rem"><button id="c2">Vault-Ordner wählen</button></p>
    </div>`;
  $("#c2").onclick = connect;
}

async function renderDashboard() {
  crumbs([{ t: "Übersicht" }]);
  const projects = await listProjects();
  const due = projects.filter((p) => (p.faellig || "9999") <= todayISO());
  let open = 0;
  for (const p of projects) open += (await listSessions(p.dir)).filter((s) => s.feedback_status === "offen").length;

  const cardHTML = (p) => `
    <div class="card link" data-h="/p/${encodeURIComponent(p.dir)}">
      <div class="row"><strong>${esc(p.title || p.dir)}</strong>${dots(p.sr_level)}</div>
      <div class="meta">
        <span>${esc(p.quelle || "—")}</span>
        <span>${p.sessions || 0} Sessions</span>
        <span>${p.zuletzt ? "zuletzt " + p.zuletzt : "noch kein Abruf"}</span>
        <span class="${(p.faellig || "9999") <= todayISO() ? "tag pending" : "tag"}">fällig ${p.faellig || "—"}</span>
      </div>
    </div>`;

  view.innerHTML = `
    <div class="row">
      <h2>Übersicht</h2>
      <button id="new">+ Neues Projekt</button>
    </div>

    ${due.length ? `<h3>Heute fällig (${due.length})</h3>${due.map(cardHTML).join("")}` : ""}

    <h3>Alle Projekte ${projects.length ? `(${projects.length})` : ""}</h3>
    ${projects.length ? projects.map(cardHTML).join("") : `<p class="muted">Noch nichts angelegt.</p>`}

    <h3>Über alles sprechen</h3>
    <div class="card">
      <p class="muted">${projects.length} Projekte · ${open} Sessions warten auf Feedback.</p>
      <p>Feedback, Wiederholungs-Planung und projektübergreifende Analyse laufen in einer
      Claude-Code-Session. Sag dort einfach <em>„Active Recall durchgehen"</em>.</p>
      <button class="ghost" id="copy">Status für Claude kopieren</button>
    </div>`;

  view.querySelectorAll(".card.link").forEach((c) => (c.onclick = () => go(c.dataset.h)));
  $("#new").onclick = () => go("/new");
  $("#copy").onclick = async () => {
    let s = `Active Recall – Stand ${todayISO()}\n\n`;
    for (const p of projects) {
      const ss = await listSessions(p.dir);
      const off = ss.filter((x) => x.feedback_status === "offen").length;
      s += `- ${p.title || p.dir} | SR-Level ${p.sr_level || 0} | fällig ${p.faellig || "—"} | ${ss.length} Sessions${off ? ` | ${off} ohne Feedback` : ""}\n`;
    }
    s += `\nBitte offene Sessions bewerten, SR-Level und Fälligkeit aktualisieren, Muster.md fortschreiben.`;
    await navigator.clipboard.writeText(s);
    toast("Status kopiert");
  };
}

function renderNew() {
  crumbs([{ t: "Übersicht", h: "/" }, { t: "Neues Projekt" }]);
  view.innerHTML = `
    <h2>Neues Projekt</h2>
    <label>Titel</label>
    <input type="text" id="title" placeholder="z. B. Deep Work – Kapitel 3">
    <label>Quelle</label>
    <select id="quelle">
      <option value="text">Text einfügen</option>
      <option value="pdf">PDF hochladen</option>
      <option value="bild">Bild hochladen</option>
      <option value="kindle">Kindle-Highlights (Text einfügen)</option>
    </select>
    <label>Umfang (optional)</label>
    <input type="text" id="umfang" placeholder="z. B. Kapitel 3, S. 40–58">

    <div id="refText-wrap">
      <label>Referenztext</label>
      <textarea id="refText" placeholder="Text / Highlights hier einfügen. Dient als Grundlage fürs Feedback."></textarea>
    </div>
    <div id="upload-wrap" hidden>
      <label>Datei</label>
      <input type="file" id="upload" accept=".pdf,image/*">
      <p class="hint">Die Datei wird im Projektordner abgelegt. Den Text zieht Claude beim ersten Feedback daraus.</p>
    </div>

    <div class="actions">
      <button id="save">Anlegen</button>
      <button class="subtle" id="cancel">Abbrechen</button>
    </div>`;

  const sync = () => {
    const v = $("#quelle").value;
    const isUpload = v === "pdf" || v === "bild";
    $("#upload-wrap").hidden = !isUpload;
    $("#refText-wrap").hidden = isUpload;
    $("#upload").accept = v === "pdf" ? ".pdf" : "image/*";
  };
  $("#quelle").onchange = sync; sync();
  $("#cancel").onclick = () => go("/");
  $("#save").onclick = async () => {
    const title = $("#title").value.trim();
    if (!title) return toast("Titel fehlt");
    const quelle = $("#quelle").value;
    const umfang = $("#umfang").value.trim();
    const isUpload = quelle === "pdf" || quelle === "bild";
    let upload = null, refText = "";
    if (isUpload) {
      upload = $("#upload").files[0];
      if (!upload) return toast("Datei fehlt");
    } else {
      refText = $("#refText").value.trim();
      if (!refText) return toast("Referenztext fehlt");
    }
    $("#save").disabled = true;
    try {
      const dir = await createProject({ title, quelle, umfang, refText, upload });
      toast("Projekt angelegt");
      go(`/p/${encodeURIComponent(dir)}`);
    } catch (e) { console.error(e); toast("Fehler beim Anlegen"); $("#save").disabled = false; }
  };
}

async function renderProject(dir) {
  const txt = await readFile(`${PROJ}/${dir}/projekt.md`);
  if (!txt) { toast("Projekt nicht gefunden"); return go("/"); }
  const { fm } = parseFM(txt);
  const ref = parseFM((await readFile(`${PROJ}/${dir}/referenz.md`)) || "");
  const sessions = await listSessions(dir);
  crumbs([{ t: "Übersicht", h: "/" }, { t: fm.title || dir }]);

  view.innerHTML = `
    <div class="row"><h2>${esc(fm.title || dir)}</h2>${dots(fm.sr_level)}</div>
    <div class="meta">
      <span>${esc(fm.quelle || "—")}</span>
      ${fm.umfang ? `<span>${esc(fm.umfang)}</span>` : ""}
      <span class="${(fm.faellig || "9999") <= todayISO() ? "tag pending" : "tag"}">fällig ${fm.faellig || "—"}</span>
      <span class="tag ${ref.fm.status === "bereit" ? "ok" : "pending"}">Referenz ${esc(ref.fm.status || "?")}</span>
    </div>

    <div class="actions">
      <button id="start">Abruf starten</button>
      <button class="subtle" id="back">Zurück</button>
    </div>

    <h3>Sessions (${sessions.length})</h3>
    ${sessions.length ? sessions.map((s) => `
      <div class="card link" data-f="${encodeURIComponent(s.file)}">
        <div class="row">
          <span>${esc(s.datum || s.file)}</span>
          <span class="tag ${s.feedback_status === "erledigt" ? "ok" : "pending"}">${s.feedback_status === "erledigt" ? "Feedback da" : "Feedback offen"}</span>
        </div>
        <div class="meta"><span>${esc(s.modus || "")}</span><span>Selbst: ${esc(s.selbsteinschaetzung || "—")}</span></div>
      </div>`).join("") : `<p class="muted">Noch kein Abruf.</p>`}`;

  $("#start").onclick = () => go(`/p/${encodeURIComponent(dir)}/recall`);
  $("#back").onclick = () => go("/");
  view.querySelectorAll(".card.link").forEach((c) => (c.onclick = () => go(`/p/${encodeURIComponent(dir)}/s/${c.dataset.f}`)));
}

async function renderRecall(dir) {
  const txt = await readFile(`${PROJ}/${dir}/projekt.md`);
  if (!txt) return go("/");
  const { fm } = parseFM(txt);
  crumbs([{ t: "Übersicht", h: "/" }, { t: fm.title || dir, h: `/p/${encodeURIComponent(dir)}` }, { t: "Abruf" }]);

  view.innerHTML = `
    <h2>Abruf – ${esc(fm.title || dir)}</h2>
    <p class="hint">Quelle zu. Schreib oder diktiere frei, was du noch weißt – nicht abschreiben,
    sondern aus dem Kopf. Es geht um die zentralen Aussagen und ihre Zusammenhänge, nicht um Vollständigkeit.
    ${fm.umfang ? `<br><strong>Umfang:</strong> ${esc(fm.umfang)}` : ""}</p>

    <textarea id="recallBox" placeholder="Aus dem Kopf …"></textarea>
    <p class="muted" style="font-size:.8rem;margin-top:.35rem">Diktieren: Cursor ins Feld, dann per WhisperBar / System-Diktat direkt hineinsprechen.</p>

    <h3>Erfasst per</h3>
    <div class="seg" id="modus">
      <button data-v="getippt" class="on">getippt</button>
      <button data-v="diktiert">diktiert</button>
    </div>

    <h3>Wie sicher fühlst du dich – vor dem Abgleich?</h3>
    <p class="muted" style="font-size:.85rem">Erst einschätzen, dann kommt das Feedback. Das trainiert die Selbsteinschätzung mit.</p>
    <div class="seg" id="selbst">
      <button data-v="nochmal">nochmal</button>
      <button data-v="schwer">schwer</button>
      <button data-v="gut">gut</button>
      <button data-v="leicht">leicht</button>
    </div>

    <div class="actions">
      <button id="save" disabled>Speichern</button>
      <button class="subtle" id="cancel">Abbrechen</button>
    </div>`;

  let selbst = null, modus = "getippt";
  const setSave = () => ($("#save").disabled = !($("#recallBox").value.trim() && selbst));

  view.querySelectorAll("#modus button").forEach((b) => (b.onclick = () => {
    modus = b.dataset.v;
    view.querySelectorAll("#modus button").forEach((x) => x.classList.toggle("on", x === b));
  }));
  view.querySelectorAll("#selbst button").forEach((b) => (b.onclick = () => {
    selbst = b.dataset.v;
    view.querySelectorAll("#selbst button").forEach((x) => x.classList.toggle("on", x === b));
    setSave();
  }));
  $("#recallBox").oninput = setSave;

  $("#cancel").onclick = () => go(`/p/${encodeURIComponent(dir)}`);
  $("#save").onclick = async () => {
    const text = $("#recallBox").value.trim();
    if (!text || !selbst) return toast("Text und Einschätzung nötig");
    $("#save").disabled = true;
    try {
      await saveSession(dir, { text, modus, umfang: fm.umfang, selbst });
      toast("Gespeichert – Feedback in der nächsten Claude-Session");
      go(`/p/${encodeURIComponent(dir)}`);
    } catch (e) { console.error(e); toast("Fehler beim Speichern"); $("#save").disabled = false; }
  };
}

async function applyRating(dir, sessFm, rating) {
  const projTxt = await readFile(`${PROJ}/${dir}/projekt.md`);
  const { fm, body } = parseFM(projTxt);
  const lvl = nextLevel(Number(sessFm.sr_level_vor) || 0, rating);
  fm.sr_level = lvl;
  fm.zuletzt = todayISO();
  fm.faellig = dueFrom(lvl);
  await writeFile(`${PROJ}/${dir}/projekt.md`, serializeFM(fm, body));
}

async function requestFeedback(dir, file, btn) {
  const sessTxt = await readFile(`${PROJ}/${dir}/sessions/${file}`);
  const { fm, body } = parseFM(sessTxt);
  const abruf = body.split(/^## Feedback\s*$/m)[0].replace(/^##\s*Abruf\s*/m, "").trim();
  const ref = parseFM((await readFile(`${PROJ}/${dir}/referenz.md`)) || "");
  if (ref.fm.status !== "bereit") return toast("Referenz noch nicht extrahiert");

  btn.disabled = true;
  const label = btn.textContent;
  btn.textContent = "Claude denkt … (~30 s)";
  try {
    const r = await fetch("/api/feedback", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ referenz: ref.body.trim(), abruf, selbst: fm.selbsteinschaetzung || "?", projekt: fm.projekt || dir }),
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || `HTTP ${r.status}`);

    const newBody = body.replace(/##\s*Feedback[\s\S]*$/m, () => `## Feedback\n\n${data.feedback}\n`);
    fm.feedback_status = "erledigt";
    fm.muster = "offen";
    await writeFile(`${PROJ}/${dir}/sessions/${file}`, serializeFM(fm, newBody));
    await applyRating(dir, fm, data.rating || "gut");
    toast("Feedback da");
    renderSession(dir, file);
  } catch (e) {
    console.error(e);
    toast("Fehler: " + e.message);
    btn.disabled = false; btn.textContent = label;
  }
}

async function renderSession(dir, file) {
  const txt = await readFile(`${PROJ}/${dir}/sessions/${file}`);
  if (!txt) return go(`/p/${encodeURIComponent(dir)}`);
  const { fm, body } = parseFM(txt);
  const ref = parseFM((await readFile(`${PROJ}/${dir}/referenz.md`)) || "");
  crumbs([{ t: "Übersicht", h: "/" }, { t: fm.projekt || dir, h: `/p/${encodeURIComponent(dir)}` }, { t: fm.datum || file }]);

  const [abruf, feedback] = body.split(/^## Feedback\s*$/m);
  const clean = (s) => (s || "").replace(/^##\s*Abruf\s*/m, "").trim();
  const done = fm.feedback_status === "erledigt";
  const refReady = ref.fm.status === "bereit";

  view.innerHTML = `
    <h2>Session ${esc(fm.datum || file)}</h2>
    <div class="meta">
      <span>${esc(fm.modus || "")}</span>
      <span>Selbst: ${esc(fm.selbsteinschaetzung || "—")}</span>
      <span class="tag ${done ? "ok" : "pending"}">${done ? "Feedback da" : "Feedback offen"}</span>
    </div>
    <h3>Abruf</h3>
    <pre class="md">${esc(clean(abruf))}</pre>
    <h3>Feedback</h3>
    ${done
      ? `<pre class="md">${esc((feedback || "").trim())}</pre>`
      : refReady
        ? `<p class="muted">Noch kein Feedback.</p><div class="actions"><button id="fb">Feedback von Claude holen</button></div>`
        : `<div class="hint">Die Referenz stammt aus einem Upload und ist noch nicht extrahiert.
           Einmal „Active Recall durchgehen" in einer Claude-Session, danach geht der Knopf hier.</div>`}
    <div class="actions"><button class="subtle" id="back">Zurück</button></div>`;

  $("#back").onclick = () => go(`/p/${encodeURIComponent(dir)}`);
  if ($("#fb")) $("#fb").onclick = (e) => requestFeedback(dir, file, e.currentTarget);
}

/* ---------- Verbindung ---------- */
async function connect() {
  try {
    const handle = await window.showDirectoryPicker({ id: "active-recall", mode: "readwrite" });
    if (!(await verifyPermission(handle))) return toast("Keine Schreibrechte");
    ROOT = handle;
    await idbSet("root", handle);
    setFolderState(true);
    go("/"); route();
  } catch (e) { if (e.name !== "AbortError") { console.error(e); toast("Verbindung fehlgeschlagen"); } }
}
function setFolderState(ok) {
  $("#folderState").textContent = ok ? "verbunden" : "nicht verbunden";
  $("#folderState").classList.toggle("ok", ok);
  $("#connectBtn").textContent = ok ? "Ordner wechseln" : "Vault-Ordner verbinden";
}

async function init() {
  if (!("showDirectoryPicker" in window)) {
    view.innerHTML = `<div class="empty"><h2>Browser nicht unterstützt</h2>
      <p class="muted">Diese App braucht die File System Access API. Bitte in Chrome oder Edge (Desktop) öffnen.</p></div>`;
    return;
  }
  $("#connectBtn").onclick = connect;
  $("#crumbHome").onclick = () => { if (ROOT) go("/"); };

  const saved = await idbGet("root");
  if (saved) {
    if ((await saved.queryPermission({ mode: "readwrite" })) === "granted") {
      ROOT = saved; setFolderState(true);
    } else {
      setFolderState(false);
      view.innerHTML = `<div class="empty"><h2>Ordner erneut freigeben</h2>
        <p class="muted">Chrome braucht nach dem Neustart eine Bestätigung.</p>
        <p style="margin-top:1rem"><button id="reauth">Freigeben</button></p></div>`;
      $("#reauth").onclick = async () => {
        if (await verifyPermission(saved)) { ROOT = saved; setFolderState(true); route(); }
      };
      return;
    }
  } else {
    setFolderState(false);
  }
  route();
}
init();
