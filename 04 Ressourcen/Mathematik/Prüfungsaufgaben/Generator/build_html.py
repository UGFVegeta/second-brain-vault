#!/usr/bin/env python3
import os

BASE = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/04 Ressourcen/Mathematik/Prüfungsaufgaben"
IMG = os.path.join(BASE, "Bilder")

def svg(name):
    with open(os.path.join(IMG, name)) as f:
        return f.read().strip()

CSS = """<style>
 :root{{--teal:{accent};--tealdark:{accentdark};--line:#dde2e5;--red:#c0392b}}
 *{{box-sizing:border-box}} body{{font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;margin:0;padding:22px;background:#f4f6f7}}
 h1{{font-size:21px;margin:0 0 4px}} .sub{{color:#5b6569;font-size:13.5px;margin:0 0 16px;max-width:820px}}
 .controls{{position:sticky;top:0;background:#f4f6f7;padding:12px 0;border-bottom:1px solid var(--line);margin-bottom:18px;z-index:5;display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
 button{{font:inherit;font-weight:600;font-size:13.5px;padding:9px 15px;border-radius:9px;border:1px solid var(--line);background:#fff;color:#1a1a1a;cursor:pointer}}
 button:hover{{border-color:var(--teal);color:var(--teal)}}
 button.primary{{background:var(--teal);color:#fff;border-color:var(--teal)}} button.primary:hover{{background:var(--tealdark);color:#fff}}
 .count{{font-size:13px;color:#5b6569;margin-left:auto}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
 .card{{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:14px 16px;break-inside:avoid;display:flex;flex-direction:column}}
 .card.selected{{border-color:var(--teal);box-shadow:0 0 0 2px rgba(46,110,142,.18)}}
 .top{{display:flex;align-items:center;gap:12px;margin-bottom:6px}}
 .num{{font-weight:700;font-size:15px;margin-left:auto}}
 .sel{{font-size:12.5px;color:#5b6569;display:flex;align-items:center;gap:6px;cursor:pointer}} .sel input{{accent-color:var(--teal);width:16px;height:16px}}
 .fig{{display:flex;justify-content:center;align-items:center;padding:4px}} .fig svg{{display:block;max-width:100%;height:auto}}
 .ges{{font-size:13.5px;color:#1a1a1a;margin-top:6px;line-height:1.5}}
 .ges b{{color:var(--red)}}
 .prob{{font-size:15px;line-height:1.55;background:#f7fafd;border:1px solid #d3def0;border-radius:9px;padding:14px 16px;margin-top:4px;min-height:90px;display:flex;align-items:center}}
 .data{{margin-top:7px;font-size:13px;line-height:1.6;background:#fafbfc;border:1px solid #e4e8ec;border-radius:7px;padding:8px 10px}}
 .dt{{border-collapse:collapse;margin:6px 0;font-size:12.5px}} .dt td,.dt th{{border:1px solid #c4ccd4;padding:2px 9px;text-align:center}} .dt th{{background:#eef2f6}}
 .soltgl{{align-self:flex-start;margin-top:10px;font-size:12.5px;padding:6px 12px}}
 .sol{{display:none;margin-top:10px;background:#f0f4fa;border:1px solid #d3def0;border-radius:9px;padding:10px 14px;font-size:13.5px;line-height:1.5}}
 .card.open .sol{{display:block}} .sol svg{{display:block;max-width:100%;height:auto;margin-top:8px}}
 @media (max-width:680px){{.grid{{grid-template-columns:1fr}}}}
 @page{{size:A4;margin:13mm}}
 @media print{{
   body{{background:#fff;padding:0}} .controls,.sub,.sel,.soltgl{{display:none !important}}
   .card{{border:1px solid #bbb;box-shadow:none}} .card.selected{{box-shadow:none}}
   .sol{{display:none !important}} .card.open .sol{{display:block !important}}
   body.selprint .card:not(.selected){{display:none !important}}
 }}
</style>"""

JS = """<script>
function tog(b){const c=b.closest('.card');const open=c.classList.toggle('open');const l=b.dataset.label||'Lösung';b.textContent=open?l+' ausblenden':l+' anzeigen';}
function allSol(v){document.querySelectorAll('.card').forEach(c=>{c.classList.toggle('open',v);const b=c.querySelector('.soltgl');const l=b.dataset.label||'Lösung';b.textContent=v?l+' ausblenden':l+' anzeigen';});}
function upd(){const n=document.querySelectorAll('.cb:checked').length;document.getElementById('count').textContent=n+' ausgewählt';}
document.addEventListener('change',e=>{if(e.target.classList.contains('cb')){e.target.closest('.card').classList.toggle('selected',e.target.checked);upd();}});
function clearSel(){document.querySelectorAll('.cb').forEach(cb=>{cb.checked=false;cb.closest('.card').classList.remove('selected');});upd();}
function printSel(){if(!document.querySelector('.cb:checked')){alert('Bitte zuerst Aufgaben auswählen (Häkchen setzen).');return;}document.body.classList.add('selprint');window.print();setTimeout(()=>document.body.classList.remove('selprint'),400);}
function printAll(){document.body.classList.remove('selprint');window.print();}
</script>"""

def card(n, body, sol_html, label):
    return (f'<div class="card" data-n="{n}">\n'
            f' <div class="top"><label class="sel"><input type="checkbox" class="cb"> auswählen</label>'
            f'<span class="num">Aufgabe {n}</span></div>\n'
            f' {body}\n'
            f' <button class="soltgl" type="button" data-label="{label}" onclick="tog(this)">{label} anzeigen</button>\n'
            f' <div class="sol">{sol_html}</div>\n'
            f'</div>')

def page(title, h1, sub, cards, accent, accentdark, plural):
    controls = ('<div class="controls">\n'
        ' <button class="primary" type="button" onclick="printSel()">🖨️ Auswahl drucken</button>\n'
        ' <button type="button" onclick="printAll()">Alles drucken</button>\n'
        f' <button type="button" onclick="allSol(true)">Alle {plural} anzeigen</button>\n'
        f' <button type="button" onclick="allSol(false)">Alle {plural} ausblenden</button>\n'
        ' <button type="button" onclick="clearSel()">Auswahl zurücksetzen</button>\n'
        ' <span class="count" id="count">0 ausgewählt</span>\n</div>')
    return ('<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{title}</title>\n' + CSS.format(accent=accent, accentdark=accentdark)
        + '</head><body>\n' + f'<h1>{h1}</h1>\n<p class="sub">{sub}</p>\n'
        + controls + '\n<div class="grid">' + ''.join(cards) + '</div>\n' + JS + '</body></html>')

# ============================================================ SACHRECHNEN
sach = [
 ("Ein Fernseher kostet 200 €. Er wird um 20 % reduziert. Wie hoch ist der neue Preis?",
  "<ul><li>Rabatt = 20 % von 200 € = 40 €</li><li>Neuer Preis = 200 € − 40 € = <b>160 €</b> (oder 200 € · 0,8)</li></ul>"),
 ("Der Preis eines Hosenanzugs wird im Schlussverkauf zunächst um 5 % und anschließend um 20 % gesenkt. Wie groß war die Preissenkung insgesamt (in Prozent)?",
  "<ul><li>Faktor = 0,95 · 0,80 = 0,76</li><li>Es bleiben 76 % → die Senkung beträgt <b>24 %</b></li><li>(Nicht 25 %! Die Prozente dürfen nicht addiert werden.)</li></ul>"),
 ("Nach einem Rabatt von 30 % kostet ein Pullover 35 €. Wie hoch war der ursprüngliche Preis?",
  "<ul><li>35 € entsprechen 70 % des Originalpreises</li><li>Originalpreis = 35 € : 0,70 = <b>50 €</b></li></ul>"),
 ("Auf ein Sparbuch werden 1500 € eingezahlt, der Zinssatz beträgt 2 % pro Jahr. Wie viel Zinsen gibt es nach einem Jahr und wie hoch ist das Guthaben?",
  "<ul><li>Zinsen = 2 % von 1500 € = <b>30 €</b></li><li>Guthaben = 1500 € + 30 € = <b>1530 €</b></li></ul>"),
 ("Der Preis eines Handys steigt von 300 € auf 360 €. Um wie viel Prozent ist der Preis gestiegen?",
  "<ul><li>Erhöhung = 360 € − 300 € = 60 €</li><li>60 € von 300 € = 60/300 = 0,20 → <b>20 %</b></li></ul>"),
 ("Ein Kapital von 250 € wird mit 3 % pro Jahr verzinst. Wie hoch ist das Endkapital nach einem Jahr?",
  "<ul><li>Zinsen = 3 % von 250 € = 7,50 €</li><li>Endkapital = 250 € + 7,50 € = <b>257,50 €</b></li></ul>"),
 ("Ein Artikel kostet netto 80 €. Wie hoch ist der Bruttopreis bei 19 % Mehrwertsteuer?",
  "<ul><li>MwSt = 19 % von 80 € = 15,20 €</li><li>Bruttopreis = 80 € + 15,20 € = <b>95,20 €</b> (oder 80 € · 1,19)</li></ul>"),
 ("Ein Neuwagen kostet 24 000 €. Im ersten Jahr verliert er 15 % an Wert. Wie viel ist er nach einem Jahr noch wert?",
  "<ul><li>Wertverlust = 15 % von 24 000 € = 3600 €</li><li>Restwert = 24 000 € − 3600 € = <b>20 400 €</b> (oder 24 000 € · 0,85)</li></ul>"),
 ("Ein Gerät kostet brutto 119 € (inklusive 19 % Mehrwertsteuer). Wie hoch ist der Nettopreis?",
  "<ul><li>119 € entsprechen 119 % des Nettopreises</li><li>Netto = 119 € : 1,19 = <b>100 €</b></li></ul>"),
 ("Auf einer Karte im Maßstab 1 : 25 000 ist eine Strecke 12 cm lang. Wie lang ist sie in Wirklichkeit?",
  "<ul><li>12 cm · 25 000 = 300 000 cm</li><li>= 3000 m = <b>3 km</b></li></ul>"),
 ("3 Maler streichen ein Haus in 8 Tagen. Wie lange brauchen 4 Maler (gleiches Tempo)?",
  "<ul><li>Antiproportional: 3 · 8 = 24 Maler-Tage</li><li>24 : 4 = <b>6 Tage</b></li></ul>"),
 ("5 kg Äpfel kosten 7,50 €. Was kosten 8 kg (gleicher Preis pro kg)?",
  "<ul><li>Proportional: 1 kg = 7,50 € : 5 = 1,50 €</li><li>8 kg · 1,50 € = <b>12 €</b></li></ul>"),
 ("Ein Preis steigt zuerst um 10 % und sinkt danach um 10 %. Wie verändert sich der Preis insgesamt?",
  "<ul><li>Faktor = 1,10 · 0,90 = 0,99</li><li>→ insgesamt <b>1 % günstiger</b> als am Anfang (nicht gleich!)</li></ul>"),
 ("Eine Restaurantrechnung beträgt 60 €. Es werden 15 % Trinkgeld gegeben. Wie hoch ist der Gesamtbetrag?",
  "<ul><li>Trinkgeld = 15 % von 60 € = 9 €</li><li>Gesamt = 60 € + 9 € = <b>69 €</b></li></ul>"),
 ("Eine Stadt hat 20 000 Einwohner und wächst zwei Jahre lang um jährlich 5 %. Wie viele Einwohner sind es nach zwei Jahren?",
  "<ul><li>Faktor pro Jahr = 1,05 → nach 2 Jahren 1,05² = 1,1025</li><li>20 000 · 1,1025 = <b>22 050 Einwohner</b></li></ul>"),
]
sach_cards = []
for i, (prob, sol) in enumerate(sach, 1):
    body = f'<div class="prob">{prob}</div>'
    sach_cards.append(card(i, body, sol, "Lösung"))
sach_html = page(
 "Sachrechnen – Aufgabenpool mündliche Prüfung",
 "Sachrechnen – Aufgabenpool",
 "Mündliche Prüfung Mathematik (Prozent-, Zins-, Maßstabs- und Dreisatzaufgaben). Aufgaben mit dem "
 "Häkchen „auswählen“ markieren und <b>„Auswahl drucken“</b> – dann werden nur die markierten Aufgaben "
 "ohne Lösung gedruckt. Mit „Lösung anzeigen“ blendest du den Rechenweg ein; sichtbare Lösungen werden mitgedruckt.",
 sach_cards, "#0e7c5a", "#0a5e44", "Lösungen")
with open(os.path.join(BASE, "Sachrechnen Aufgabenpool.html"), "w") as f:
    f.write(sach_html)
print("wrote Sachrechnen Aufgabenpool.html")

# ============================================================ BOXPLOT
def dth(label_keys, label_vals, keys, vals):
    k = "".join(f"<td>{x}</td>" for x in keys)
    v = "".join(f"<td>{x}</td>" for x in vals)
    return (f'<div style="overflow-x:auto"><table class="dt">'
            f'<tr><th>{label_keys}</th>{k}</tr>'
            f'<tr><th>{label_vals}</th>{v}</tr></table></div>')

boxtasks = [
 dict(n=1, mode="read", fig="Box-Aufgabe-01.svg",
   instr="<b>Aufgabe:</b> Lies aus dem Boxplot ab: Minimum, unteres Quartil, Median, oberes Quartil und Maximum. Bestimme außerdem Spannweite und Quartilsabstand.",
   sol="Min = 10, Q1 = 35, Median = 50, Q3 = 70, Max = 95.<br>Spannweite = 95 − 10 = <b>85</b>. Quartilsabstand = 70 − 35 = <b>35</b>. Die mittleren 50 % der Werte liegen zwischen 35 und 70 Punkten."),
 dict(n=2, mode="read", fig="Box-Aufgabe-02.svg",
   instr="<b>Aufgabe:</b> Lies die Fünf-Punkte-Zusammenfassung ab. Wie groß ist die Spannweite? Wie viel Prozent der Werte liegen über 45 min?",
   sol="Min = 5, Q1 = 20, Median = 30, Q3 = 45, Max = 55. Spannweite = <b>50 min</b>. Über dem oberen Quartil (45) liegen <b>25 %</b> der Werte."),
 dict(n=3, mode="create", fig="Box-03-axis.svg", solfig="Box-03-loesung.svg",
   instr="<b>Aufgabe:</b> Gegeben sind die sortierten Werte<div class='data'>3, 5, 6, 6, 8, 9, 10, 12, 12, 14, 15 &nbsp;(n = 11)</div>Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.",
   sol="Median = 9 (6. Wert). Untere Hälfte 3, 5, 6, 6, 8 → Q1 = 6. Obere Hälfte 10, 12, 12, 14, 15 → Q3 = 12. Min = 3, Max = 15."),
 dict(n=4, mode="create", fig="Box-04-axis.svg", solfig="Box-04-loesung.svg",
   instr="<b>Aufgabe:</b> Gegeben sind die sortierten Werte<div class='data'>2, 4, 5, 7, 8, 8, 10, 13 &nbsp;(n = 8)</div>Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.",
   sol="Median = (7 + 8)/2 = 7,5. Untere Hälfte 2, 4, 5, 7 → Q1 = (4 + 5)/2 = 4,5. Obere Hälfte 8, 8, 10, 13 → Q3 = (8 + 10)/2 = 9. Min = 2, Max = 13."),
 dict(n=5, mode="create", fig="Box-05-axis.svg", solfig="Box-05-loesung.svg",
   instr="<b>Aufgabe:</b> Die Strichliste zeigt das Taschengeld (in €) von 22 Schülern. Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot."
         + dth("Euro","Anzahl",[0,10,15,20,25,30,35,40,50,60],[2,2,2,3,2,5,1,3,1,1]),
   sol="n = 22. Median = (25 + 30)/2 = <b>27,5 €</b>. Q1 = 15 €, Q3 = 35 €. Min = 0 €, Max = 60 €. Spannweite = 60 €, Quartilsabstand = 20 €."),
 dict(n=6, mode="read", fig="Box-06.svg",
   instr="<b>Aufgabe:</b> Drei Gruppen wurden befragt. Zu welchen Gruppen gehören die Boxplots (1) und (2)? Begründe."
         "<div class='data'><b>A:</b> 0, 0, 0, 30, 45, 60, 60, 150, 150, 150, 165, 180, 180<br>"
         "<b>B:</b> 0, 30, 45, 45, 60, 60, 60, 75, 75, 75, 90, 105, 120, 135, 150, 150, 180<br>"
         "<b>C:</b> 0, 30, 45, 75, 90, 90, 90, 90, 120, 150, 150, 180, 180</div>",
   sol="Mediane: A = 60, B = 75, C = 90. <b>(1)</b> hat Median 75 → <b>Gruppe B</b> (Quartile 52,5 / 127,5). <b>(2)</b> hat Median 90 → <b>Gruppe C</b> (Quartile 60 / 150). Übrig bleibt Gruppe A."),
 dict(n=7, mode="read", fig="Box-07-given.svg", solfig="Box-07-loesung.svg",
   instr="<b>Aufgabe:</b> Die Boxplots (1) und (2) gehören zu Gruppe B und C. Erstelle den fehlenden Boxplot für Gruppe A.<div class='data'><b>A:</b> 0, 0, 0, 30, 45, 60, 60, 150, 150, 150, 165, 180, 180 (n = 13)</div>",
   sol="Median = 60 (7. Wert). Untere Hälfte → Q1 = (0 + 30)/2 = 15. Obere Hälfte → Q3 = (150 + 165)/2 = 157,5. Min = 0, Max = 180."),
 dict(n=8, mode="read", fig="Box-08.svg",
   instr="<b>Aufgabe:</b> Vergleiche die beiden Boxplots (B) und (C). Worin gleichen, worin unterscheiden sie sich?",
   sol="Gleich: Min = 20, Median = 90, Max = 175 (Spannweite je 155). Unterschied: (B) hat Q3 = 120, (C) nur Q3 = 110 → der Quartilsabstand ist bei (B) größer (80 gegenüber 70). Die mittleren 50 % streuen bei (B) etwas stärker."),
 dict(n=9, mode="read", fig="Box-09.svg",
   instr="<b>Aufgabe:</b> Beschreibe die Verteilung. Ist sie symmetrisch oder schief? Was bedeutet der lange rechte Whisker?",
   sol="Min = 0, Q1 = 10, Median = 15, Q3 = 40, Max = 60. Die Verteilung ist <b>rechtsschief</b>: Die Hälfte der Werte liegt ≤ 15, aber die oberen 25 % streuen sehr weit (40–60). Einzelne große Werte ziehen den rechten Whisker in die Länge."),
 dict(n=10, mode="create", fig="Box-10-axis.svg", solfig="Box-10-loesung.svg",
   instr="<b>Aufgabe:</b> Gegeben sind die sortierten Werte<div class='data'>4, 6, 7, 7, 9, 11, 12, 12, 15 &nbsp;(n = 9)</div>Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.",
   sol="Median = 9 (5. Wert). Untere Hälfte 4, 6, 7, 7 → Q1 = (6 + 7)/2 = 6,5. Obere Hälfte 11, 12, 12, 15 → Q3 = (12 + 12)/2 = 12. Min = 4, Max = 15."),
 dict(n=11, mode="read", fig="Box-11.svg",
   instr="<b>Aufgabe:</b> Bestimme aus dem Boxplot den Median, die Spannweite und den Quartilsabstand.",
   sol="Median = 40. Min = 12, Max = 80 → Spannweite = <b>68</b>. Q1 = 25, Q3 = 55 → Quartilsabstand = <b>30</b>."),
 dict(n=12, mode="create", fig="Box-12-axis.svg", solfig="Box-12-loesung.svg",
   instr="<b>Aufgabe:</b> Eine App wurde von 28 Personen genutzt. Die Tabelle zeigt die Nutzungsdauer (in Stunden). Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot."
         + dth("Dauer (h)","Anzahl",[1,2,3,4,5,6,7,8,9,11],[2,1,2,2,6,5,6,2,1,1]),
   sol="n = 28. Median = (6 + 6)/2 = <b>6 h</b>. Q1 = 4,5 h, Q3 = 7 h. Min = 1 h, Max = 11 h. Spannweite = 10 h, Quartilsabstand = 2,5 h."),
 dict(n=13, mode="read", fig="Box-13.svg",
   instr="<b>Aufgabe:</b> Zwei Klassen A und B schreiben dieselbe Arbeit (Punkte). Vergleiche Median und Streuung.",
   sol="Beide haben Median = 7. Klasse A: Min 3 / Max 10 → Spannweite 7, Quartilsabstand 3. Klasse B: Min 1 / Max 13 → Spannweite 12, Quartilsabstand 7. → Gleicher Median, aber Klasse B streut deutlich stärker (heterogener)."),
 dict(n=14, mode="read", fig="Box-14.svg",
   instr="<b>Aufgabe:</b> Der Boxplot zeigt die Wartezeiten an einer Kasse (in min). Wie lange warten die meisten Kunden? Was sagt der lange rechte Whisker aus?",
   sol="Min = 1, Q1 = 3, Median = 6, Q3 = 12, Max = 30. Die Hälfte wartet höchstens 6 min, 75 % höchstens 12 min. Einzelne warten aber bis 30 min → rechtsschiefe Verteilung."),
 dict(n=15, mode="create", fig="Box-15-axis.svg", solfig="Box-15-loesung.svg",
   instr="<b>Aufgabe:</b> Gegeben sind die sortierten Werte<div class='data'>5, 5, 8, 10, 10, 12, 14, 15, 15, 18, 20, 22 &nbsp;(n = 12)</div>Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.",
   sol="Median = (12 + 14)/2 = 13. Untere Hälfte 5, 5, 8, 10, 10, 12 → Q1 = (8 + 10)/2 = 9. Obere Hälfte 14, 15, 15, 18, 20, 22 → Q3 = (15 + 18)/2 = 16,5. Min = 5, Max = 22."),
]
box_cards = []
for t in boxtasks:
    figsvg = f'<div class="fig">{svg(t["fig"])}</div>'
    instr = f'<div class="ges">{t["instr"]}</div>'
    if t["mode"] == "create":
        body = instr + "\n " + figsvg     # Daten/Anweisung zuerst, dann leere Achse
    else:
        body = figsvg + "\n " + instr     # Boxplot zuerst, dann Anweisung
    sol = t["sol"]
    if t.get("solfig"):
        sol += svg(t["solfig"])
    box_cards.append(card(t["n"], body, sol, "Lösung"))

box_html = page(
 "Boxplot – Aufgabenpool mündliche Prüfung",
 "Boxplot & Datenanalyse – Aufgabenpool",
 "Mündliche Prüfung Mathematik (Median, Quartile, Spannweite, Boxplots lesen, erstellen, zuordnen und vergleichen). "
 "Aufgaben mit dem Häkchen „auswählen“ markieren und <b>„Auswahl drucken“</b> – dann werden nur die markierten "
 "Aufgaben ohne Lösung gedruckt; bei den Zeichenaufgaben ist die leere Skala zum Eintragen schon dabei. "
 "Mit „Lösung anzeigen“ erscheinen Rechenweg und – bei Zeichenaufgaben – der fertige Boxplot.",
 box_cards, "#c2410c", "#9a3412", "Lösungen")
with open(os.path.join(BASE, "Boxplot Aufgabenpool.html"), "w") as f:
    f.write(box_html)
print("wrote Boxplot Aufgabenpool.html")
print("done")
