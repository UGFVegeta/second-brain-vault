/* Gemeinsame Logik der Wettkampf-Dashboards: Theme, Countdown, Streckenkarte,
   Höhenprofil, Anstiegstabelle und Untergrund-Balken.

   Die Reiter laufen bewusst ohne JavaScript (Radio-Buttons + CSS), damit sie
   auch in Vorschau-Ansichten ohne Skriptausführung funktionieren. */

var TriUI = (function () {
  "use strict";

  var SVGNS = "http://www.w3.org/2000/svg";

  function nf(n, d) {
    return Number(n).toLocaleString("de-DE",
      { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  }
  function $(sel) { return typeof sel === "string" ? document.querySelector(sel) : sel; }
  function clear(el) { while (el && el.firstChild) el.removeChild(el.firstChild); }

  /* ---------- Farbskala nach Steigung ---------- */
  var BUCKETS = [
    { max: -6, c: "#2f7fd4", l: "steil bergab" },
    { max: -2.5, c: "#63a8ea", l: "bergab" },
    { max: 1.5, c: "#8d98a8", l: "flach" },
    { max: 4, c: "#f0b954", l: "2 – 4 %" },
    { max: 7, c: "#f28b6b", l: "4 – 7 %" },
    { max: 99, c: "#f0716b", l: "über 7 %" }
  ];
  function gradeColor(g) {
    for (var i = 0; i < BUCKETS.length; i++) if (g < BUCKETS[i].max) return BUCKETS[i].c;
    return BUCKETS[BUCKETS.length - 1].c;
  }
  function legend(el) {
    if (!el) return;
    el.innerHTML = BUCKETS.map(function (b) {
      return "<span><i style='background:" + b.c + "'></i>" + b.l + "</span>";
    }).join("");
  }

  /* ---------- Theme ---------- */
  function theme(btnSel, key) {
    var btn = $(btnSel);
    if (!btn) return;
    if (localStorage.getItem(key) === "light") document.documentElement.classList.add("light");
    function sync() {
      btn.textContent = document.documentElement.classList.contains("light") ? "Dunkel" : "Hell";
    }
    btn.hidden = false;  // ohne JavaScript bleibt der Umschalter unsichtbar statt tot
    sync();
    btn.addEventListener("click", function () {
      document.documentElement.classList.toggle("light");
      localStorage.setItem(key, document.documentElement.classList.contains("light") ? "light" : "dark");
      sync();
      redrawAll();
    });
  }

  /* ---------- Countdown ---------- */
  function countdown(valSel, subSel, iso) {
    var val = $(valSel), sub = $(subSel);
    if (!val) return;
    var diff = new Date(iso) - new Date();
    var days = Math.ceil(diff / 86400000);
    if (diff > 0) {
      val.textContent = days + (days === 1 ? " Tag" : " Tage");
    } else if (diff > -86400000) {
      val.textContent = "heute";
      if (sub) sub.textContent = "Wettkampftag";
    } else {
      val.textContent = "vorbei";
      if (sub) sub.textContent = new Date(iso).toLocaleDateString("de-DE");
    }
  }

  /* ---------- Balken ---------- */
  var PALETTE = ["var(--green)", "var(--blue)", "var(--amber)", "var(--coral)",
    "var(--purple)", "var(--pink)", "var(--t4)"];
  function bars(sel, list, titel) {
    var el = $(sel);
    if (!el || !list) return;
    var html = "<div class='btitle'>" + titel + "</div>";
    list.forEach(function (s, i) {
      html += "<div class='bar'><div class='top'><span>" + s.typ + "</span><span>" +
        nf(s.anteil, 1) + " % · " + nf(s.meter / 1000, 1) + " km</span></div>" +
        "<div class='track'><div class='fill' style='width:" + Math.max(1.5, s.anteil) +
        "%;background:" + PALETTE[i % PALETTE.length] + "'></div></div></div>";
    });
    el.innerHTML = html;
  }

  /* ---------- Anstiegstabelle ---------- */
  function climbs(sel, list, limit) {
    var tb = $(sel);
    if (!tb || !list) return;
    clear(tb);
    list.slice().sort(function (a, b) { return b.hm - a.hm; })
      .slice(0, limit || 99).forEach(function (c) {
        var tr = document.createElement("tr");
        tr.innerHTML = "<td class='k'>km " + nf(c.von, 1) + " – " + nf(c.bis, 1) + "</td>" +
          "<td>" + nf(c.laenge) + " m</td><td>" + nf(c.hm) + " hm</td>" +
          "<td class='g' style='color:" + gradeColor(c.schnitt) + "'>" + nf(c.schnitt, 1) + " %</td>" +
          "<td>" + nf(c.max, 1) + " %</td>";
        tb.appendChild(tr);
      });
  }

  /* ---------- Karte + Profil ---------- */
  var views = [];

  function disziplin(cfg) {
    var d = cfg.data;
    if (!d) return null;
    var mapSvg = $(cfg.map), profSvg = $(cfg.profile), tip = $(cfg.tip);
    var view = { cfg: cfg, d: d, mapSvg: mapSvg, profSvg: profSvg, tip: tip, marker: null };

    legend($(cfg.legend));
    bars(cfg.surfaces, d.untergrund, "Untergrund");
    bars(cfg.ways, d.wegtypen, "Wegtypen");
    climbs(cfg.climbs, d.anstiege, cfg.climbLimit);

    view.draw = function () { drawMap(view); drawProfile(view); };
    view.draw();
    bindHover(view);
    views.push(view);
    return view;
  }

  function redrawAll() { views.forEach(function (v) { v.draw(); }); }

  function drawMap(v) {
    var svg = v.mapSvg;
    if (!svg) return;
    var d = v.d, t = d.track, g = d.trackSteigung, pad = 30;
    svg.setAttribute("viewBox", (-pad) + " " + (-pad) + " " +
      (d.bbox.w + 2 * pad) + " " + (d.bbox.h + 2 * pad));
    clear(svg);

    var shadow = document.createElementNS(SVGNS, "path");
    shadow.setAttribute("d", "M" + t.map(function (p) { return p[0] + " " + p[1]; }).join(" L"));
    shadow.setAttribute("fill", "none");
    shadow.setAttribute("stroke", "rgba(0,0,0,.20)");
    shadow.setAttribute("stroke-width", "13");
    shadow.setAttribute("stroke-linecap", "round");
    shadow.setAttribute("stroke-linejoin", "round");
    svg.appendChild(shadow);

    var cur = null, seg = [];
    function addSeg(pts, col) {
      if (pts.length < 2) return;
      var p = document.createElementNS(SVGNS, "path");
      p.setAttribute("d", "M" + pts.map(function (q) { return q[0] + " " + q[1]; }).join(" L"));
      p.setAttribute("fill", "none");
      p.setAttribute("stroke", col);
      p.setAttribute("stroke-width", "8");
      p.setAttribute("stroke-linecap", "round");
      p.setAttribute("stroke-linejoin", "round");
      svg.appendChild(p);
    }
    for (var i = 0; i < t.length; i++) {
      var col = v.cfg.flat ? "#63a8ea" : gradeColor(g[i]);
      if (col !== cur) {
        addSeg(seg, cur);
        seg = seg.length ? [seg[seg.length - 1]] : [];
        cur = col;
      }
      seg.push(t[i]);
    }
    addSeg(seg, cur);

    // km-Marken, überlappende auf Rundkursen auslassen
    var stepKm = v.cfg.kmStep || (d.distanzKm > 40 ? 10 : d.distanzKm > 12 ? 5 : 1);
    var next = stepKm, placed = [];
    for (var j = 0; j < t.length; j++) {
      if (t[j][2] >= next) {
        var frei = placed.every(function (p) {
          return Math.hypot(p[0] - t[j][0], p[1] - t[j][1]) > 34;
        });
        if (frei) { kmDot(svg, t[j][0], t[j][1], next); placed.push([t[j][0], t[j][1]]); }
        next += stepKm;
      }
    }

    punkt(svg, t[0][0], t[0][1], "var(--green)", v.cfg.startLabel || "Start");
    var last = t[t.length - 1];
    if (Math.hypot(last[0] - t[0][0], last[1] - t[0][1]) > 25) {
      punkt(svg, last[0], last[1], "var(--red)", v.cfg.zielLabel || "Ziel");
    }

    v.marker = document.createElementNS(SVGNS, "circle");
    v.marker.setAttribute("r", "10");
    v.marker.setAttribute("fill", "var(--pink)");
    v.marker.setAttribute("stroke", "var(--card)");
    v.marker.setAttribute("stroke-width", "3");
    v.marker.setAttribute("opacity", "0");
    svg.appendChild(v.marker);
  }

  function kmDot(svg, x, y, km) {
    var c = document.createElementNS(SVGNS, "circle");
    c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", "12");
    c.setAttribute("fill", "var(--card)");
    c.setAttribute("stroke", "var(--t4)");
    c.setAttribute("stroke-width", "1.5");
    svg.appendChild(c);
    var tx = document.createElementNS(SVGNS, "text");
    tx.setAttribute("x", x); tx.setAttribute("y", y + 4.5);
    tx.setAttribute("text-anchor", "middle"); tx.setAttribute("font-size", "12");
    tx.setAttribute("fill", "var(--t2)"); tx.setAttribute("font-family", "inherit");
    tx.textContent = km;
    svg.appendChild(tx);
  }

  function punkt(svg, x, y, farbe, text) {
    var c = document.createElementNS(SVGNS, "circle");
    c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", "11");
    c.setAttribute("fill", farbe);
    c.setAttribute("stroke", "var(--card)"); c.setAttribute("stroke-width", "3");
    svg.appendChild(c);
    var l = document.createElementNS(SVGNS, "text");
    l.setAttribute("x", x + 18); l.setAttribute("y", y + 5);
    l.setAttribute("font-size", "15"); l.setAttribute("fill", "var(--t2)");
    l.setAttribute("font-family", "inherit"); l.setAttribute("font-weight", "600");
    l.textContent = text;
    svg.appendChild(l);
  }

  var PW = 700, PH = 300, PL = 44, PR = 10, PT = 14, PB = 26;

  /* Halbe Fenstergröße (in 50-m-Schritten) für die Steigungsmittelung:
     ±250 m auf kurzen Strecken, bis ±800 m auf einer Mitteldistanz-Radrunde. */
  function fenster(d) {
    return Math.max(5, Math.min(16, Math.round(d.distanzKm * 1000 / 100 / 50)));
  }

  function scales(v) {
    var d = v.d;
    var xMax = d.profil[d.profil.length - 1][0];
    var spanne = Math.max(20, d.maxHoehe - d.minHoehe);
    var raster = spanne > 300 ? 100 : spanne > 150 ? 50 : spanne > 60 ? 20 : 5;
    var yMin = Math.floor((d.minHoehe - spanne * 0.12) / raster) * raster;
    var yMax = Math.ceil((d.maxHoehe + spanne * 0.12) / raster) * raster;
    return {
      xMax: xMax, yMin: yMin, yMax: yMax, raster: raster,
      px: function (km) { return PL + (km / xMax) * (PW - PL - PR); },
      py: function (a) { return PT + (1 - (a - yMin) / (yMax - yMin)) * (PH - PT - PB); }
    };
  }

  function drawProfile(v) {
    var svg = v.profSvg;
    if (!svg) return;
    var d = v.d, s = scales(v), prof = d.profil;
    clear(svg);
    svg.setAttribute("viewBox", "0 0 " + PW + " " + PH);

    for (var a = s.yMin; a <= s.yMax; a += s.raster) {
      var ln = document.createElementNS(SVGNS, "line");
      ln.setAttribute("x1", PL); ln.setAttribute("x2", PW - PR);
      ln.setAttribute("y1", s.py(a)); ln.setAttribute("y2", s.py(a));
      ln.setAttribute("stroke", "var(--line)"); ln.setAttribute("stroke-width", "1");
      svg.appendChild(ln);
      text(svg, PL - 7, s.py(a) + 4, a, "end", 10, "var(--t4)");
    }
    var kmStep = s.xMax > 40 ? 10 : s.xMax > 12 ? 5 : s.xMax > 3 ? 1 : 0.5;
    for (var k = 0; k <= s.xMax + 1e-6; k += kmStep) {
      if (s.px(k) > PW - PR - 24) continue;   // Platz für die Einheit am rechten Rand
      text(svg, s.px(k), PH - 8, (Math.round(k * 10) / 10).toString().replace(".", ","),
        "middle", 10, "var(--t4)");
    }
    text(svg, PW - PR, PH - 8, "km", "end", 10, "var(--t4)");

    // Rundengrenzen
    var grenzen = d.rundenGrenzen && d.rundenGrenzen.length ? d.rundenGrenzen : [];
    if (!grenzen.length && d.runden > 1) {
      for (var q = 1; q < d.runden; q++) grenzen.push(s.xMax / d.runden * q);
    }
    if (grenzen.length) {
      for (var r = 0; r < grenzen.length; r++) {
        var xr = s.px(grenzen[r]);
        var rl = document.createElementNS(SVGNS, "line");
        rl.setAttribute("x1", xr); rl.setAttribute("x2", xr);
        rl.setAttribute("y1", PT); rl.setAttribute("y2", PH - PB);
        rl.setAttribute("stroke", "var(--t4)"); rl.setAttribute("stroke-width", "1");
        rl.setAttribute("stroke-dasharray", "4 4"); rl.setAttribute("opacity", ".6");
        svg.appendChild(rl);
      }
    }

    // Fläche in Steigungsfarben. Das Mittelungsfenster wächst mit der Streckenlänge,
    // sonst zerfasert ein 80-km-Profil in einzelne Farbstreifen.
    var win = fenster(d);
    for (var i = 1; i < prof.length; i++) {
      var lo = Math.max(0, i - win), hi = Math.min(prof.length - 1, i + win);
      var g = (prof[hi][1] - prof[lo][1]) / ((prof[hi][0] - prof[lo][0]) * 1000) * 100;
      var rect = document.createElementNS(SVGNS, "rect");
      var x0 = s.px(prof[i - 1][0]), x1 = s.px(prof[i][0]);
      rect.setAttribute("x", x0);
      rect.setAttribute("width", Math.max(0.6, x1 - x0 + 0.6));
      rect.setAttribute("y", s.py(prof[i][1]));
      rect.setAttribute("height", Math.max(0, s.py(s.yMin) - s.py(prof[i][1])));
      rect.setAttribute("fill", v.cfg.flat ? "#63a8ea" : gradeColor(g));
      rect.setAttribute("opacity", ".78");
      svg.appendChild(rect);
    }

    var line = document.createElementNS(SVGNS, "path");
    line.setAttribute("d", "M" + prof.map(function (p) { return s.px(p[0]) + " " + s.py(p[1]); }).join(" L"));
    line.setAttribute("fill", "none"); line.setAttribute("stroke", "var(--t1)");
    line.setAttribute("stroke-width", "1.4"); line.setAttribute("opacity", ".55");
    svg.appendChild(line);

    (d.anstiege || []).filter(function (c) { return c.hm >= (v.cfg.markHm || 30); })
      .forEach(function (c) {
        text(svg, s.px((c.von + c.bis) / 2), PT + 12,
          "+" + c.hm + " hm · " + c.schnitt.toString().replace(".", ",") + " %",
          "middle", 10.5, "var(--t2)", 600);
      });

    var hl = document.createElementNS(SVGNS, "line");
    hl.setAttribute("class", "hoverline");
    hl.setAttribute("y1", PT); hl.setAttribute("y2", PH - PB);
    hl.setAttribute("stroke", "var(--pink)"); hl.setAttribute("stroke-width", "1.4");
    hl.setAttribute("opacity", "0");
    svg.appendChild(hl);
    v.hl = hl;
  }

  function text(svg, x, y, val, anchor, size, fill, weight) {
    var t = document.createElementNS(SVGNS, "text");
    t.setAttribute("x", x); t.setAttribute("y", y);
    t.setAttribute("text-anchor", anchor); t.setAttribute("font-size", size);
    t.setAttribute("fill", fill); t.setAttribute("font-family", "inherit");
    if (weight) t.setAttribute("font-weight", weight);
    t.textContent = val;
    svg.appendChild(t);
  }

  function bindHover(v) {
    if (!v.profSvg) return;
    function move(ev) {
      var s = scales(v), prof = v.d.profil;
      var rect = v.profSvg.getBoundingClientRect();
      var cx = (ev.touches ? ev.touches[0].clientX : ev.clientX) - rect.left;
      var km = (cx / rect.width * PW - PL) / (PW - PL - PR) * s.xMax;
      if (km < 0 || km > s.xMax) { hide(); return; }
      var idx = Math.min(prof.length - 1, Math.max(0, Math.round(km / s.xMax * (prof.length - 1))));
      var p = prof[idx];
      var w = fenster(v.d);
      var lo = Math.max(0, idx - w), hi = Math.min(prof.length - 1, idx + w);
      var grad = (prof[hi][1] - prof[lo][1]) / ((prof[hi][0] - prof[lo][0]) * 1000) * 100;

      if (v.hl) {
        v.hl.setAttribute("x1", s.px(p[0])); v.hl.setAttribute("x2", s.px(p[0]));
        v.hl.setAttribute("opacity", ".9");
      }
      if (v.tip) {
        v.tip.style.opacity = "1";
        v.tip.innerHTML = "<b>km " + p[0].toFixed(1).replace(".", ",") + "</b> · " +
          Math.round(p[1]) + " m" + (v.cfg.flat ? "" :
            " · " + (grad >= 0 ? "+" : "") + grad.toFixed(1).replace(".", ",") + " %");
        var left = s.px(p[0]) / PW * rect.width;
        v.tip.style.left = Math.min(rect.width - v.tip.offsetWidth - 4,
          Math.max(0, left - v.tip.offsetWidth / 2)) + "px";
        v.tip.style.top = "6px";
      }
      if (v.marker) {
        var t = v.d.track, best = t[0], bd = 1e9;
        for (var i = 0; i < t.length; i++) {
          var dd = Math.abs(t[i][2] - p[0]);
          if (dd < bd) { bd = dd; best = t[i]; }
        }
        v.marker.setAttribute("cx", best[0]);
        v.marker.setAttribute("cy", best[1]);
        v.marker.setAttribute("opacity", "1");
      }
    }
    function hide() {
      if (v.tip) v.tip.style.opacity = "0";
      if (v.hl) v.hl.setAttribute("opacity", "0");
      if (v.marker) v.marker.setAttribute("opacity", "0");
    }
    v.profSvg.addEventListener("mousemove", move);
    v.profSvg.addEventListener("touchmove", function (e) { move(e); e.preventDefault(); }, { passive: false });
    v.profSvg.addEventListener("mouseleave", hide);
    v.profSvg.addEventListener("touchend", hide);
  }

  /* ---------- Kennzahlen in Textfelder schreiben ---------- */
  function fill(map) {
    Object.keys(map).forEach(function (sel) {
      var el = $(sel);
      if (el) el.textContent = map[sel];
    });
  }

  window.addEventListener("resize", redrawAll);

  return {
    theme: theme, countdown: countdown, disziplin: disziplin, bars: bars,
    climbs: climbs, legend: legend, fill: fill, nf: nf, gradeColor: gradeColor,
    redraw: redrawAll
  };
})();
