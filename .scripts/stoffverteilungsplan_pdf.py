#!/usr/bin/env python3
"""Baut aus dem Markdown-Stoffverteilungsplan eine schlanke Fachschafts-PDF (A4 quer).

Fuer die Fachschaft zaehlt nur: welche Woche, welcher Block, welches Thema.
Uebernommen werden deshalb nur die Spalten Nr, Woche ab, Block und Thema.
Weggelassen: Bildungsplan, Folien, Versuch/Material, die beiden leeren Eintragespalten
sowie die internen Abschnitte (Excel-Fassung, Hinweise zur Umsetzung, Vault-Links).
Alle uebernommenen Texte stehen wortgleich so in der Quellnotiz.
"""
import html
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
TBL_PT = float(sys.argv[3]) if len(sys.argv) > 3 else 8.4

KEEP = ["Nr", "Woche ab", "Block", "Thema"]   # Spalten, die in die PDF wandern

raw = re.sub(r"\A---\n.*?\n---\n", "", SRC.read_text(encoding="utf-8"), flags=re.S)


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


# --- Markdown zerlegen ------------------------------------------------------
sections: dict[str, list] = {"_intro": []}
current, title = "_intro", ""
lines = raw.split("\n")
i, n = 0, len(lines)
while i < n:
    line = lines[i]
    if not line.strip():
        i += 1
        continue
    if line.startswith("# "):
        title = line[2:].strip()
        i += 1
        continue
    if line.startswith("## "):
        current = line[3:].strip()
        sections.setdefault(current, [])
        i += 1
        continue
    if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
        header = [c.strip() for c in line.strip().strip("|").split("|")]
        i += 2
        rows = []
        while i < n and lines[i].lstrip().startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        sections[current].append(("table", header, rows))
        continue
    if line.lstrip().startswith("- "):
        items = []
        while i < n and lines[i].lstrip().startswith("- "):
            items.append(lines[i].lstrip()[2:])
            i += 1
        sections[current].append(("ul", items))
        continue
    para = []
    while i < n and lines[i].strip() and not lines[i].lstrip().startswith(("|", "#", "- ")):
        para.append(lines[i].strip())
        i += 1
    sections[current].append(("p", " ".join(para)))


def plan_table(name: str) -> str:
    """Wochentabelle eines Halbjahres, auf die Spalten in KEEP reduziert."""
    header, rows = next((b[1], b[2]) for b in sections[name] if b[0] == "table")
    idx = [header.index(c) for c in KEEP]
    out = [f'<table class="plan"><colgroup>{"".join(f"<col class=c{k}>" for k in range(1, len(idx)+1))}</colgroup>']
    out.append("<thead><tr>" + "".join(f"<th>{inline(header[j])}</th>" for j in idx) + "</tr></thead><tbody>")
    for r in rows:
        blk = r[header.index("Block")].lower()
        rcls = ' class="ka"' if "klassenarbeit" in blk else (' class="puffer"' if "puffer" in blk else "")
        cells = "".join(
            f'<td>{"" if r[j] == "" else ("<span class=dash>–</span>" if r[j] == "–" else inline(r[j]))}</td>'
            for j in idx
        )
        out.append(f"<tr{rcls}>{cells}</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def block_table() -> str:
    header, rows = next((b[1], b[2]) for b in sections["Stundenverteilung nach Blöcken"] if b[0] == "table")
    out = ['<table class="kompakt"><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead><tbody>"]
    for r in rows:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


rahmen = next(b[1] for b in sections["Rahmen"] if b[0] == "ul")
rahmen_html = "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in rahmen) + "</ul>"

# Schlussbemerkungen der beiden Halbjahre (Zeugnis- und Notenschlusshinweis)
def fuss(name):
    return "".join(f'<p class="fuss">{inline(b[1])}</p>' for b in sections[name] if b[0] == "p")


CSS = f"""
@page {{ size: A4 landscape; margin: 10mm 13mm 10mm 13mm; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 8.6pt; line-height: 1.42; color: #14171c; margin: 0;
  font-variant-numeric: tabular-nums;
}}
h1 {{ font-size: 16.5pt; font-weight: 600; letter-spacing: -0.012em;
  margin: 0 0 2mm; padding-bottom: 2.2mm; border-bottom: 1.4pt solid #14171c; }}
h2 {{ font-size: 11pt; font-weight: 600; margin: 0 0 2.2mm;
  padding-bottom: 1mm; border-bottom: 0.5pt solid #b8bec7; break-after: avoid; }}
p {{ margin: 0 0 2.4mm; }}
ul {{ margin: 0; padding-left: 4.2mm; }}
li {{ margin-bottom: 1.1mm; }}
strong {{ font-weight: 600; }}
.dash {{ color: #b0b6bf; }}

.meta {{ font-size: 8pt; color: #5c6470; margin: 0 0 3.5mm; }}
.meta span::after {{ content: "·"; color: #b8bec7; margin: 0 3mm; }}
.meta span:last-child::after {{ content: ""; }}

.kopf {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 0 14mm; margin-bottom: 6mm; }}
.kopf h2 {{ margin-top: 0; }}

table {{ border-collapse: collapse; width: 100%; }}
th, td {{ text-align: left; vertical-align: top; }}
thead {{ display: table-header-group; }}
tr {{ break-inside: avoid; }}

table.plan {{ font-size: {TBL_PT}pt; line-height: 1.3; margin-bottom: 2.5mm; }}
table.plan th {{ font-size: {TBL_PT - 1.1}pt; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.06em; color: #4a525e; padding: 1.5mm 2mm; background: #f4f5f7;
  border-bottom: 1pt solid #14171c; }}
table.plan td {{ padding: 1.32mm 2mm; border-bottom: 0.4pt solid #dfe2e7; }}
table.plan tbody tr.ka td {{ background: #eceff3; }}
table.plan tbody tr.puffer td {{ color: #6b7380; }}
table.plan td:nth-child(1) {{ font-weight: 600; white-space: nowrap; }}
table.plan td:nth-child(2) {{ white-space: nowrap; }}
table.plan td:nth-child(3) {{ color: #4a525e; }}
table.plan col.c1 {{ width: 6%; }}
table.plan col.c2 {{ width: 10%; }}
table.plan col.c3 {{ width: 13%; }}
table.plan col.c4 {{ width: 71%; }}

table.kompakt {{ font-size: 8.2pt; }}
table.kompakt th {{ font-size: 7.2pt; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
  color: #4a525e; padding: 1.2mm 3mm 1.2mm 0; border-bottom: 1pt solid #14171c; }}
table.kompakt td {{ padding: 1.15mm 3mm 1.15mm 0; border-bottom: 0.4pt solid #dfe2e7; }}
table.kompakt td:nth-child(2), table.kompakt th:nth-child(2) {{ text-align: right; padding-right: 5mm; width: 16%; }}
table.kompakt th:nth-child(3) {{ width: 30%; }}
table.kompakt tr:last-child td {{ border-bottom: 1pt solid #14171c; font-weight: 600; }}

.fuss {{ font-size: 7.8pt; color: #3d444e; margin: 0 0 1mm; }}
.rahmen {{ margin: 0 0 4mm; padding: 2.2mm 0 2.4mm; border-top: 0.5pt solid #dfe2e7;
  border-bottom: 0.5pt solid #dfe2e7; font-size: 7.7pt; color: #4a525e; break-inside: avoid; }}
.rahmen ul {{ columns: 2; column-gap: 12mm; padding-left: 4mm; }}
.rahmen li {{ margin-bottom: 0.8mm; break-inside: avoid; }}
.break {{ break-before: page; }}
"""

doc = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>{CSS}</style></head><body>

<h1>{inline(title)}</h1>
<div class="meta">
  <span>Realschule, 2 Wochenstunden</span>
  <span>39 Unterrichtswochen, 78 Stunden</span>
  <span>Bildungsplan Physik Sek I, Fassung V3.0 vom 08.04.2026</span>
  <span>Stand 31.07.2026</span>
</div>

<div class="rahmen">{rahmen_html}</div>

<h2>Erstes Halbjahr</h2>
{plan_table("Erstes Halbjahr")}
{fuss("Erstes Halbjahr")}

<h2 class="break">Zweites Halbjahr</h2>
{plan_table("Zweites Halbjahr")}
{fuss("Zweites Halbjahr")}

</body></html>"""

OUT.write_text(doc, encoding="utf-8")
print(f"HTML geschrieben ({TBL_PT}pt Tabellenschrift)")
