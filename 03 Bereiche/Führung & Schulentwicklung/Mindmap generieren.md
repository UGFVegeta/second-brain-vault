---
tags: [excalidraw-script]
---

# Mindmap: Datengestützte Schulentwicklung

Dieses Script generiert die Mindmap mit korrekt verbundenen Pfeilen.

**Ausführen:** In Obsidian auf das Excalidraw-Ribbon-Icon klicken → "Run Script" → diese Datei auswählen.

```javascript
const ea = ExcalidrawAutomate;
ea.reset();

// ─── STYLES ──────────────────────────────────────────────────────
ea.style.roughness = 0;
ea.style.strokeWidth = 2;
ea.style.fillStyle = "solid";
ea.style.fontFamily = 3;
ea.style.fontSize = 14;
ea.style.textColor = "#ffffff";
ea.style.roundness = {type: 3};

// ─── HELPER ──────────────────────────────────────────────────────
function addNode(x, y, w, h, text, fill, stroke, textColor = "#ffffff") {
  ea.style.backgroundColor = fill;
  ea.style.strokeColor = stroke;
  ea.style.textColor = textColor;
  const id = ea.addRect(x - w/2, y - h/2, w, h);
  ea.style.strokeColor = textColor;
  ea.addText(x - w/2 + 4, y - h/2, text, {
    width: w - 8,
    height: h,
    textAlign: "center",
    verticalAlign: "middle",
    containerId: id,
    wrapAt: w - 16,
  });
  return id;
}

function addCenter(x, y, w, h, text) {
  ea.style.backgroundColor = "#3b82f6";
  ea.style.strokeColor = "#1e3a5f";
  ea.style.textColor = "#ffffff";
  const id = ea.addEllipse(x - w/2, y - h/2, w, h);
  ea.addText(x - w/2 + 4, y - h/2, text, {
    width: w - 8,
    height: h,
    textAlign: "center",
    verticalAlign: "middle",
    containerId: id,
  });
  return id;
}

function connect(id1, id2, color) {
  ea.style.strokeColor = color;
  ea.style.strokeWidth = 2;
  ea.connectObjects(id1, null, id2, null, {
    numberOfPoints: 0,
    startArrowHead: "none",
    endArrowHead: "arrow",
    padding: 8,
  });
}

// ─── LAYOUT (alle Koordinaten = Mittelpunkt) ──────────────────────
const CX = 800, CY = 500;

// CENTER
const ctr = addCenter(CX, CY, 255, 90, "Datengestützte\nSchulentwicklung");

// BRANCH 1 – SCHILDKAMP (oben, grün)
const b1 = addNode(CX, 235, 230, 58, "Schildkamp-Zyklus", "#047857", "#064e3b");
connect(ctr, b1, "#047857");

const s1 = [
  addNode(540, 95, 160, 58, "1. Daten-\nerhebung",          "#a7f3d0", "#047857", "#064e3b"),
  addNode(710, 95, 160, 58, "2. Verarbeitung",               "#a7f3d0", "#047857", "#064e3b"),
  addNode(890, 95, 160, 58, "3. Interpretation\n& Integration","#a7f3d0","#047857","#064e3b"),
  addNode(1070,95, 160, 58, "4. Maßnahmen\n(Taten)",         "#a7f3d0", "#047857", "#064e3b"),
];
s1.forEach(id => connect(b1, id, "#047857"));

// Zyklus-Pfeil: s1[3] → s1[0]
ea.style.strokeColor = "#047857";
ea.style.strokeWidth = 1.5;
ea.style.strokeStyle = "dashed";
ea.connectObjects(s1[3], "bottom", s1[0], "bottom", {
  numberOfPoints: 2,
  startArrowHead: "none",
  endArrowHead: "arrow",
  padding: 8,
});
ea.style.strokeStyle = "solid";

// BRANCH 2 – DATENQUELLEN (rechts, orange)
const b2 = addNode(1140, 370, 200, 58, "Datenquellen", "#c2410c", "#7c2d12");
connect(ctr, b2, "#c2410c");

[
  [1370, 250, "Schuldatenblatt"],
  [1370, 330, "Kompass 4 (Kl. 4)"],
  [1370, 415, "Fachschafts-\nrückmeldungen"],
  [1370, 500, "Beratungsgespräche\n(Dez/Jan)"],
].forEach(([x, y, lbl]) => {
  const id = addNode(x, y, 200, 60, lbl, "#fed7aa", "#c2410c", "#7c2d12");
  connect(b2, id, "#c2410c");
});

// BRANCH 3 – ZIELE (rechts unten, pink)
const b3 = addNode(1050, 660, 175, 58, "Ziele", "#be185d", "#831843");
connect(ctr, b3, "#be185d");

[
  [1280, 600, "Ausbildungsreife"],
  [1280, 675, "Niveausteuerung\nG / M / E"],
  [1280, 755, "Individuelle\nFörderung"],
].forEach(([x, y, lbl]) => {
  const id = addNode(x, y, 195, 60, lbl, "#fce7f3", "#be185d", "#831843");
  connect(b3, id, "#be185d");
});

// BRANCH 4 – INSTRUMENTE (links unten, lila)
const b4 = addNode(500, 660, 200, 58, "Instrumente", "#6d28d9", "#4c1d95");
connect(ctr, b4, "#6d28d9");

[
  [255, 575, "Poolstunden"],
  [255, 650, "Binnen-\ndifferenzierung"],
  [255, 730, "Leistungsdiff.\nGruppen"],
  [255, 810, "WBS-\nProfilbildung"],
].forEach(([x, y, lbl]) => {
  const id = addNode(x, y, 185, 60, lbl, "#ddd6fe", "#6d28d9", "#4c1d95");
  connect(b4, id, "#6d28d9");
});

// BRANCH 5 – AKTEURE (links, türkis)
const b5 = addNode(430, 370, 175, 58, "Akteure", "#0e7490", "#164e63");
connect(ctr, b5, "#0e7490");

[
  [210, 250, "Konrektor"],
  [210, 325, "Regellehrkraft"],
  [210, 400, "Sonderpädagoge"],
  [210, 475, "Schulsozialarbeit"],
].forEach(([x, y, lbl]) => {
  const id = addNode(x, y, 175, 55, lbl, "#cffafe", "#0e7490", "#164e63");
  connect(b5, id, "#0e7490");
});

// ─── ERSTELLEN ────────────────────────────────────────────────────
await ea.create({
  filename: "Datengestützte Schulentwicklung v3",
  foldername: "03 Bereiche/Führung & Schulentwicklung",
  onNewPane: true,
});
```
