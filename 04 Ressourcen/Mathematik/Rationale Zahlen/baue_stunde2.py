#!/usr/bin/env python3
"""Baut 'Rationale Zahlen 2 – Addieren – ALLES.html' (Klasse 7c, zwei Einzelstunden Mi + Do).

Alles in einer Datei: Verlauf, Tafelbild, Merkheft, Aufgaben, Lösungen.
Änderungen: hier im Skript, dann `python3 baue_stunde2.py`.
Quelle der Aufgaben: Mathebuch S. 18–19 (Kapitel „3 Addieren"), Fotos von Oskar am 22.09.2026.
Die Lösungen sind selbst gerechnet, noch nicht mit dem digitalen Lösungsbuch abgeglichen
(siehe „Offen" im Ausblick) – besonders Aufgabe 1 c)/d), da die Pfeilrichtung auf dem Foto
nicht ganz eindeutig war.
"""
from pathlib import Path

K = 20
NEG, POS, INK, MUT = "#b3261e", "#1a56a0", "#1b1b1b", "#5a5a5a"


def num(v, plus=True):
    if isinstance(v, str):
        return v
    v = round(v, 6)
    t = f"{abs(v):g}".replace(".", ",")
    if v < 0:
        return "−" + t
    if v > 0 and plus:
        return "+" + t
    return t


def stift(g=16):
    return (f'<svg class="stift" viewBox="0 0 24 24" width="{g}" height="{g}" '
            'xmlns="http://www.w3.org/2000/svg"><path d="M3 21 L4.8 16.2 L16 5 L19 8 L7.8 19.2 Z" '
            'fill="none" stroke="#1b1b1b" stroke-width="1.9" stroke-linejoin="round"/>'
            '<path d="M14 7 L17 10" stroke="#1b1b1b" stroke-width="1.9"/></svg>')


def fig(svg, cap=""):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f"<figure>{svg}{c}</figure>"


_uid = [0]


def bogengerade(von, bis, start, delta, schritt=1, kpe=3):
    """Zahlengerade mit Bogen-Pfeil von `start` nach `start+delta` (Additions-Modell wie im Buch)."""
    _uid[0] += 1
    uid = _uid[0]
    pad = 2
    n = round((bis - von) / schritt)
    W = (2 * pad + n * kpe) * K

    def X(v):
        return (pad + (v - von) / schritt * kpe) * K

    farbe = POS if delta > 0 else NEG
    ende = start + delta
    x1, x2 = X(start), X(ende)
    xm = (x1 + x2) / 2
    ah = 30
    ax = 78
    H = ax + 40
    s = [f'<svg class="gerade" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'xmlns="http://www.w3.org/2000/svg" font-family="Helvetica, Arial, sans-serif">',
         f'<defs><pattern id="k{uid}" width="{K}" height="{K}" patternUnits="userSpaceOnUse">'
         f'<path d="M{K} 0H0V{K}" fill="none" stroke="#c8d0dc" stroke-width="1"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="{H}" fill="url(#k{uid})"/>',
         f'<path d="M{W} 0V{H}H0" fill="none" stroke="#c8d0dc"/>',
         f'<line x1="{K}" y1="{ax}" x2="{W - K}" y2="{ax}" stroke="#222" stroke-width="1.7"/>',
         f'<polygon points="{W - K},{ax} {W - K - 10},{ax - 5} {W - K - 10},{ax + 5}" fill="#222"/>',
         f'<polygon points="{K},{ax} {K + 10},{ax - 5} {K + 10},{ax + 5}" fill="#222"/>']
    for i in range(n + 1):
        v = von + i * schritt
        x = X(v)
        h = 10 if abs(v) < 1e-9 else 7
        sw = 2.2 if abs(v) < 1e-9 else 1.3
        s.append(f'<line x1="{x:.1f}" y1="{ax - h}" x2="{x:.1f}" y2="{ax + h}" stroke="#222" stroke-width="{sw}"/>')
        wt = "700" if abs(v) < 1e-9 else "400"
        s.append(f'<text x="{x:.1f}" y="{ax + 24}" text-anchor="middle" font-size="12.5" '
                 f'font-weight="{wt}" fill="{INK}">{num(v)}</text>')
    ay = ax - 2 * ah
    s.append(f'<path d="M{x1:.1f} {ax - 5} Q{xm:.1f} {ay:.1f} {x2:.1f} {ax - 5}" fill="none" '
              f'stroke="{farbe}" stroke-width="2.2" marker-end="url(#ar{uid})"/>')
    s.append(f'<defs><marker id="ar{uid}" markerWidth="9" markerHeight="9" refX="6" refY="4" '
              f'orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{farbe}"/></marker></defs>')
    s.append(f'<rect x="{xm - 26:.1f}" y="{ay - 4:.1f}" width="52" height="20" rx="5" fill="{farbe}"/>')
    s.append(f'<text x="{xm:.1f}" y="{ay + 10.5:.1f}" text-anchor="middle" font-size="14" font-weight="700" '
              f'fill="#fff">{num(delta)}</text>')
    s.append(f'<circle cx="{x1:.1f}" cy="{ax}" r="5" fill="{INK}" stroke="#fff" stroke-width="1.4"/>')
    s.append(f'<circle cx="{x2:.1f}" cy="{ax}" r="5.5" fill="{farbe}" stroke="#fff" stroke-width="1.4"/>')
    s.append(f'<text x="{x1:.1f}" y="{ax + 24}" text-anchor="middle" font-size="13" font-weight="700" '
              f'fill="{INK}">{num(start)}</text>')
    s.append(f'<text x="{x2:.1f}" y="{ax + 24}" text-anchor="middle" font-size="13.5" font-weight="700" '
              f'fill="{farbe}">{num(ende)}</text>')
    s.append("</svg>")
    return "".join(s)


BSP1 = bogengerade(-3, 6, -2, 7, kpe=4)
BSP2 = bogengerade(-8, 1, -1, -6, kpe=3)

CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;color:#1b1b1b;background:#fff}
.wrap{max-width:1000px;margin:0 auto;padding:0 22px}
header.kopf{padding:30px 0 12px;border-bottom:2px solid #1b1b1b;margin-bottom:0}
h1{font-size:27px;margin:0 0 4px;line-height:1.2}.sub{color:#555;margin:0}
nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #d9d9d4;z-index:5}
nav .wrap{display:flex;gap:6px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
nav a{padding:5px 13px;border-radius:16px;text-decoration:none;color:#1b1b1b;font-size:14px;background:#f1f1ed}
nav a:hover{background:#e3e3dc}
section{padding:34px 0 8px;scroll-margin-top:50px}
h2{font-size:22px;margin:0 0 6px}h2+.lead{margin-top:0}
.lead{color:#555;margin:0 0 16px}
h3{font-size:17px;margin:26px 0 8px}
.ziel{background:#f5f5f1;border-radius:8px;padding:12px 16px;margin:16px 0}
.bl{border:1px solid #d3d3cc;border-radius:9px;margin:16px 0;overflow:hidden}
.bl>header{display:flex;align-items:center;gap:12px;background:#f5f5f1;padding:9px 16px;border-bottom:1px solid #d3d3cc}
.bl .nr{width:28px;height:28px;border-radius:50%;background:#1b1b1b;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;font-size:14px}
.bl h3{margin:0;font-size:17px;flex:1}.bl .min{color:#555;font-size:14px;white-space:nowrap}
.bl .body{padding:6px 18px 12px}
.bl ul{margin:8px 0;padding-left:20px}.bl li{margin:6px 0}
.t{display:inline-block;min-width:52px;color:#555;font-size:13.5px}
.knapp{background:#fff6e0;border-left:4px solid #e0a100;padding:7px 12px;margin:10px 0 4px;font-size:15px}
.fehler{background:#fbeeee;border-left:4px solid #b3261e;padding:8px 14px;margin:16px 0}
.fehler ol{margin:6px 0 2px;padding-left:20px}
.nicht{color:#555;font-size:15px;margin:10px 0}
.stift{vertical-align:-2px;margin:0 2px}
figure{margin:10px 0 12px}figure svg{display:block;max-width:100%;height:auto;border:1px solid #c8d0dc}
figcaption{font-size:13.5px;color:#555;margin-top:4px}
.tafelblock{margin:18px 0 26px}
.tafelblock>h3{display:flex;justify-content:space-between;align-items:baseline;background:#eeeeea;border-left:5px solid #1b1b1b;padding:5px 12px;margin:0 0 10px;font-size:16.5px}
.tafelblock>h3 span{font-weight:400;font-size:13.5px;color:#555;font-style:italic}
.heft{border-left:5px solid #1b1b1b;padding-left:14px;margin:12px 0}
.merk{background:#eef3fb;border:1.5px solid #1a56a0;border-radius:6px;padding:8px 13px;margin:9px 0;font-weight:600}
.merk.neg{border-color:#b3261e;background:#fbeeee}
.merk table{background:transparent;margin:8px 0 0}.merk td,.merk th{border:none;padding:2px 8px 2px 0;font-weight:400}
.merk th{font-weight:700}
.sprech{font-size:14.5px;color:#555;font-style:italic;margin:6px 0}
.uheft{border-left:5px dashed #1a56a0;padding-left:14px;margin:12px 0}
.chip.ueb{background:#e2ecf8;color:#1a56a0;border:1px dashed #1a56a0}
.chip.mk{background:#eee;color:#1b1b1b;border:1px solid #1b1b1b}
.legende{border:1px solid #c9c9c2;border-radius:6px;padding:7px 12px;font-size:14.5px;margin:12px 0}
.aufg{font-size:16.5px;font-weight:600;margin:6px 0}
.neg{color:#b3261e;font-weight:600}.pos{color:#1a56a0;font-weight:600}
.heftseite{border:2px solid #1b1b1b;border-radius:4px;padding:18px 24px;margin:16px 0;background:#fff;box-shadow:4px 4px 0 #e3e3dc}
.heftseite h3{font-size:20px;margin:0 0 4px;text-decoration:underline}
.heftseite p{margin:8px 0}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:15.5px}
th,td{border:1px solid #d3d3cc;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f5f5f1;font-weight:600}
.chip{display:inline-block;padding:1px 9px;border-radius:10px;font-size:12.5px;font-weight:600;white-space:nowrap}
.orange{background:#fdebd3;color:#8a4b00}.gruen{background:#dcf1dc;color:#1d6b1d}.alle{background:#e2ecf8;color:#1a56a0}
.loes{margin:8px 0 18px}.loes h4{margin:18px 0 6px;font-size:16.5px}
.loes p{margin:5px 0}
.kl{columns:2;column-gap:28px;margin:6px 0}.kl div{break-inside:avoid;margin:2px 0}
footer{margin-top:40px;padding:14px 0 40px;border-top:1px solid #d3d3cc;color:#666;font-size:13.5px}
.zeige{background:#e7f3e7;border-left:4px solid #1d6b1d;padding:6px 12px;margin:0 0 10px;font-size:15px}
.nichts{background:#e7f3e7;border-left:4px solid #1d6b1d;padding:9px 14px;margin:8px 0}
.warn{background:#fff6e0;border-left:4px solid #e0a100;padding:9px 14px;margin:8px 0;font-size:14.5px}
.vt th:first-child,.vt td.mn{width:52px;text-align:right;white-space:nowrap;color:#555}
.vt tr.grp td{background:#eeeeea;font-weight:700;font-size:15.5px}
.vt tr.grp td span{float:right;font-weight:400;color:#555;font-size:14px}
@media print{nav{display:none}section{page-break-before:always}.bl,figure,.heftseite,.tafelblock{break-inside:avoid}body{font-size:11pt}}
"""

E = stift()
UE = '<span class="chip ueb">Übungsheft</span>'
MK = '<span class="chip mk">Merkheft</span>'
ALL = '<span class="chip alle">alle</span>'


def grp(nr, titel, t0, t1):
    return f'<tr class="grp"><td colspan="4">{nr} · {titel}<span>Minute {t0}–{t1}</span></td></tr>'


def vz(m, was, buch, wer, e=False):
    return f'<tr><td class="mn">{m}′</td><td>{E + " " if e else ""}{was}</td><td>{buch}</td><td>{wer}</td></tr>'


# ================================================================== MITTWOCH – Verlauf
zeilen_mi = "".join([
    grp(0, "Start", 0, 4),
    vz(4, "Ankommen. Rückblick in einem Satz: gestern Zahlengerade und Vergleichen, heute wird auf der "
          "Geraden gerechnet", "&ndash;", "Plenum"),
    grp(1, "Einstieg: Bogenmodell", 4, 12),
    vz(4, "Erste Rechnung an die Tafel: (−2) + (+7). Wo stehen wir, wohin bewegen wir uns?", "Tafel", "Plenum"),
    vz(4, "Zweite Rechnung: (−1) + (−6). Vergleich beider Bögen: <b>positiv</b> addieren = nach rechts, "
          "<b>negativ</b> addieren = nach links", "Tafel", "Plenum"),
    grp(2, "Merksatz", 12, 20),
    vz(8, "Regel in zwei Fällen (gleiche / verschiedene Vorzeichen) mit den vier Buch-Beispielen", f"Tafel &rarr; {MK}",
       "Plenum, abschreiben", True),
    grp(3, "Viel rechnen", 20, 40),
    vz(4, "Aufgabe 1: fehlenden Wert an der Zahlengeraden ergänzen", f"S. 18 Nr. 1 {ALL}", "Einzel"),
    vz(4, "Aufgabe 2: gleiche Vorzeichen, im Kopf", f"S. 18 Nr. 2 {ALL}", f"Einzel<br>{UE}"),
    vz(6, "Aufgabe 3: erst Vorzeichen des Ergebnisses überlegen, dann rechnen", f"S. 18 Nr. 3 {ALL}",
       f"Einzel<br>{UE}"),
    vz(6, "Aufgabe 4: direkt berechnen (Klammern einfach mitschreiben)", f"S. 18 Nr. 4 {ALL}", f"Einzel<br>{UE}"),
    vz(5, "Kontrolle in Partnerarbeit, offene Fragen sammeln", "&ndash;", "Partner"),
    vz("+", "Wer schnell fertig ist: <b>Alles klar? A</b> und <b>B</b>, dazu der Fördern-Link 2pq6ev",
       "S. 18/19 „Alles klar?“", "Einzel"),
    grp(4, "Ausstieg", 40, 45),
    vz(3, "Exit-Ticket: zwei Aufgaben aus <b>Alles klar? A</b> auf einen Zettel", "S. 19 A a), c)", f"Einzel<br>{UE}"),
    vz(2, "Hausaufgabe ansagen", "Rest von Nr. 3, 4 · Alles klar? B", f"Zu Hause<br>{UE}"),
])

verlauf_mi = f"""
<section id="mittwoch"><h2>Mittwoch · Einzelstunde</h2>
<p class="lead">45 Minuten. Ziel dieser Stunde ist Masse: die Regel einmal klar herausarbeiten, dann viel selbst
rechnen. {E} = wird ins {MK} geschrieben. Alle Übungen kommen ins {UE}.</p>
<div class="ziel"><b>Ziel:</b> Die Klasse kennt die Regel „gleiche Vorzeichen: Beträge addieren, Vorzeichen bleibt“
und „verschiedene Vorzeichen: Beträge subtrahieren, Vorzeichen der betragsmäßig größeren Zahl“ und wendet sie in
vielen Kopf- und Übungsaufgaben sicher an. <b>Nicht Ziel:</b> Sachaufgaben, Subtraktion – das kommt am Donnerstag
bzw. nächste Woche.</p>
<table class="vt"><tr><th>Min</th><th>Was</th><th>Buch und Material</th><th>Wer</th></tr>{zeilen_mi}</table>
<div class="knapp"><b>Wenn es knapp wird:</b> Aufgabe 4 wird Hausaufgabe, „Alles klar?“ nur für Schnelle.</div>
<div class="fehler"><b>Worauf du achten kannst</b>
<ol>
<li>Vorzeichen und Rechenzeichen werden verwechselt, besonders wenn beide − sind: (−12) + (−15) sieht aus wie eine
Subtraktion. Klammern lesen lassen.</li>
<li>Bei verschiedenen Vorzeichen wird addiert statt subtrahiert: (+28) + (−10) wird zu 38 statt 18.</li>
<li>Das Vorzeichen des Ergebnisses wird vergessen oder falsch übernommen, besonders wenn die negative Zahl den
größeren Betrag hat: (−30) + (+20) landet bei +10 statt −10.</li>
<li>Bei Aufgabe 4 (größere Beispiele) wird die Klammer beim Ablesen ignoriert und nur die nackten Zahlen
verrechnet, z. B. (−25) + (+17) wird zu 25 + 17 = 42 statt −8.</li>
</ol></div>
</section>
"""

# Tafelbild Mittwoch
tafel_mi = f"""
<div class="tafelblock"><h3>Bogenmodell <span>Minute 4–12</span></h3>
<div class="heft">{fig(BSP1, "1 = 4 Kästchen. Bei −2 starten, Bogen +7 nach rechts, Landung bei +5.")}
{fig(BSP2, "1 = 3 Kästchen. Bei −1 starten, Bogen −6 nach links, Landung bei −7.")}
<div class="merk">Addiert man eine <span class="pos">positive</span> Zahl, bewegt man sich auf der Zahlengeraden
nach rechts.<br>Addiert man eine <span class="neg">negative</span> Zahl, bewegt man sich nach links.</div></div>
<p class="sprech">Erst die Startzahl markieren, dann fragen: „Addiere ich etwas Positives oder Negatives – wohin
geht der Bogen?“ Erst danach zählen lassen.</p></div>

<div class="tafelblock"><h3>Merksatz: Rationale Zahlen addieren <span>Minute 12–20</span></h3>
<div class="heft"><div class="merk"><b>Gleiche Vorzeichen</b><br>Man addiert die Zahlen, ohne ihr Vorzeichen zu
berücksichtigen. Das Ergebnis erhält das gemeinsame Vorzeichen.</div>
<div class="merk"><b>Verschiedene Vorzeichen</b><br>Man subtrahiert die Zahlen, ohne ihr Vorzeichen zu
berücksichtigen. Das Ergebnis erhält das Vorzeichen der Zahl, die von Null weiter entfernt ist.</div>
<p>(+12) + (+8) = +(12 + 8) = +20 &nbsp;&middot;&nbsp; (−15) + (−10) = −(15 + 10) = −25<br>
(+18) + (−6) = +(18 − 6) = +12 &nbsp;&middot;&nbsp; (−14) + (+9) = −(14 − 9) = −5</p></div></div>

<div class="tafelblock"><h3>Viel rechnen <span>Minute 20–40</span></h3>
<div class="uheft"><p class="aufg">{UE} S. 18 Nr. 1, 2, 3, 4 – der Reihe nach, im eigenen Tempo.</p>
<p class="sprech">Bei jeder Aufgabe erst das Vorzeichen des Ergebnisses überlegen, dann erst rechnen. Die Klammern
bleiben einfach stehen, wie in der Aufgabe vorgegeben – kein Umschreiben nötig.</p></div>
<p>Für Schnelle: „Alles klar?“ A (Kopfrechnen) und B (Kärtchen zuordnen), dazu der Fördern-Link <b>2pq6ev</b> für
alle, die noch mehr Übung brauchen.</p></div>
"""

# ================================================================== DONNERSTAG – Verlauf
ORA = "<span class='chip orange'>orange</span>"
GRU = "<span class='chip gruen'>grün</span>"

zeilen_do = "".join([
    grp(0, "Start", 0, 5),
    vz(5, "Kopfrechenkette mündlich: fünf kurze Additionen im Wechsel, als Auffrischung von gestern", "&ndash;",
       "Plenum"),
    grp(1, "Sachaufgabe: Skitour", 5, 15),
    vz(10, "Bildaufgabe Gamshütte &rarr; Enzianstüble &rarr; Falkenhütte: Temperatur am Enzianstüble, Vergleich "
           "Auf-/Abstieg, Höhe und Temperatur an der Falkenhütte", "S. 18 Bildaufgabe", "Plenum, dann Partner"),
    grp(2, "Anwenden und üben", 15, 35),
    vz(6, "Fahnenaufgabe: Ergebnis ablesen und nachrechnen", f"S. 19 Nr. 5 {ALL}", f"Einzel<br>{UE}"),
    vz(6, "Fehlersuche: fünf falsch gerechnete Additionen korrigieren", f"S. 19 Nr. 6 {ALL}", "Partner"),
    vz(8, "Je nach Tempo: Kärtchen kombinieren oder Hochhaus-Aufgabe",
       f"S. 19 Nr. 9 links {ORA} oder Nr. 10 links {GRU}", f"Einzel<br>{UE}"),
    vz("+", "Für Schnelle: Mitgliederentwicklung Sportverein", f"S. 19 Nr. 11 links {GRU}", "Einzel"),
    grp(3, "Sicherung", 35, 40),
    vz(5, "Fehlersuche (Nr. 6) gemeinsam an der Tafel besprechen – guter Anlass für die typischen Fehler",
       "Tafel", "Plenum"),
    grp(4, "Ausstieg", 40, 45),
    vz(5, "Wenn Zeit bleibt: Start des Würfelspiels zu zweit, sonst Hausaufgabe ansagen", f"S. 19 Nr. 12",
       f"Partner oder<br>Hausaufgabe"),
])

verlauf_do = f"""
<section id="donnerstag"><h2>Donnerstag · Einzelstunde</h2>
<p class="lead">45 Minuten. Nach der reinen Rechenroutine vom Mittwoch geht es heute um Anwenden: eine
Sachaufgabe im Sachzusammenhang und Aufgaben, die zeigen, wo Fehler typischerweise passieren.</p>
<div class="ziel"><b>Ziel:</b> Die Klasse wendet die Additionsregel in Sachzusammenhängen an (Temperatur, Höhe,
Kontostand) und erkennt typische Fehler in fremden Rechnungen. <b>Nicht Ziel:</b> neue Regeln – die Regel von
Mittwoch wird nur angewendet, nicht erweitert.</p>
<table class="vt"><tr><th>Min</th><th>Was</th><th>Buch und Material</th><th>Wer</th></tr>{zeilen_do}</table>
<div class="knapp"><b>Wenn es knapp wird:</b> Nr. 9/10/11 nur eine Aufgabe statt Auswahl, das Würfelspiel (Nr. 12)
ganz weglassen oder als Hausaufgabe ankündigen.</div>
</section>
"""

tafel_do = f"""
<div class="tafelblock"><h3>Sachaufgabe: Skitour <span>Minute 5–15</span></h3>
<p class="aufg">Gamshütte 2350 m, −12,5 °C. Abstieg 750 m zum Enzianstüble (+8,5 °C Temperaturänderung). Aufstieg
920 m zur Falkenhütte (−10,5 °C Temperaturänderung).</p>
<div class="heft"><p><b>Temperatur am Enzianstüble:</b> −12,5 + 8,5 = −4 °C<br>
<b>Aufstieg minus Abstieg:</b> 920 − 750 = 170 m, der Aufstieg ist 170 m größer als der Abstieg<br>
<b>Höhe Falkenhütte:</b> 2350 − 750 + 920 = 2520 m &nbsp;&middot;&nbsp; <b>Temperatur:</b> −4 + (−10,5) = −14,5 °C</p></div>
<p class="sprech">Erst die Situation an der Tafel skizzieren (Höhenprofil als Linie), dann für jede Frage einzeln
den passenden Rechenausdruck aufschreiben lassen, bevor gerechnet wird.</p></div>

<div class="tafelblock"><h3>Fehlersuche <span>Minute 20–40</span></h3>
<p class="aufg">S. 19 Nr. 6 rechts: „Hier hat sich ein Fehler eingeschlichen.“</p>
<div class="uheft"><p>a) (+12) + (−10) = 22 &nbsp;&rarr;&nbsp; richtig: +2<br>
b) (−25) + (+20) = 5 &nbsp;&rarr;&nbsp; richtig: −5<br>
c) (+24) + (−30) = −54 &nbsp;&rarr;&nbsp; richtig: −6<br>
d) (−16) + (−24) = −8 &nbsp;&rarr;&nbsp; richtig: −40<br>
e) −4,25 + (−0,5) = −3,75 &nbsp;&rarr;&nbsp; richtig: −4,75</p></div>
<p class="sprech">Fragen: Welcher Fehler wiederholt sich (a, b, c – Vorzeichen des Ergebnisses)? Welcher ist anders
(d – Beträge addiert statt richtig verrechnet)?</p></div>
"""

# ================================================================== Merkheft
merkheft = f"""
<section id="merkheft"><h2>Merkheft</h2>
<p class="lead">Das schreiben die Schüler am Mittwoch ab.</p>
<div class="heftseite">
<h3>Rationale Zahlen addieren</h3>
{fig(BSP1, "1 = 4 Kästchen")}
<p><span class="pos">Positive</span> Zahl addieren: Bewegung nach rechts.<br>
<span class="neg">Negative</span> Zahl addieren: Bewegung nach links.</p>
<p><b>Gleiche Vorzeichen:</b> Man addiert die Zahlen, ohne ihr Vorzeichen zu berücksichtigen. Das Ergebnis erhält
das gemeinsame Vorzeichen.</p>
<p><b>Verschiedene Vorzeichen:</b> Man subtrahiert die Zahlen, ohne ihr Vorzeichen zu berücksichtigen. Das
Ergebnis erhält das Vorzeichen der Zahl, die von Null weiter entfernt ist.</p>
<p>(+12) + (+8) = +20 &nbsp;&middot;&nbsp; (−15) + (−10) = −25 &nbsp;&middot;&nbsp; (+18) + (−6) = +12
&nbsp;&middot;&nbsp; (−14) + (+9) = −5</p>
</div>
</section>
"""

# ================================================================== Aufgaben-Übersicht
aufgaben = f"""
<section id="aufgaben"><h2>Aufgaben</h2>
<p class="lead">Alles steht im Buch S. 18–19. Alle Übungen kommen ins {UE}, Merksätze ins {MK}.
{ORA} und {GRU} sind Differenzierungsangebote, {ALL} sind Pflichtaufgaben für alle.</p>
<table><tr><th>Tag</th><th>Buch</th><th>Niveau</th><th>Aufgabe</th></tr>
<tr><td>Mi</td><td>Tafel</td><td>{ALL}</td><td>Bogenmodell: (−2) + (+7) und (−1) + (−6)</td></tr>
<tr><td>Mi</td><td>S. 18 Nr. 1</td><td>{ALL}</td><td>Fehlenden Wert an der Zahlengeraden ergänzen</td></tr>
<tr><td>Mi</td><td>S. 18 Nr. 2</td><td>{ALL}</td><td>Gleiche Vorzeichen, im Kopf addieren</td></tr>
<tr><td>Mi</td><td>S. 18 Nr. 3</td><td>{ALL}</td><td>Erst Vorzeichen überlegen, dann berechnen</td></tr>
<tr><td>Mi</td><td>S. 18 Nr. 4</td><td>{ALL}</td><td>Direkt berechnen (größere Zahlen)</td></tr>
<tr><td>Mi</td><td>S. 18/19 „Alles klar?“ A, B</td><td>für Schnelle</td><td>Kopfrechnen · Kärtchen den Summen zuordnen</td></tr>
<tr><td>Do</td><td>S. 18 Bildaufgabe</td><td>{ALL}</td><td>Skitour Gamshütte–Enzianstüble–Falkenhütte</td></tr>
<tr><td>Do</td><td>S. 19 Nr. 5</td><td>{ALL}</td><td>Fahnenaufgabe: Ergebnis ablesen, nachrechnen</td></tr>
<tr><td>Do</td><td>S. 19 Nr. 6</td><td>{ALL}</td><td>Fehlersuche: fünf Additionen korrigieren</td></tr>
<tr><td>Do</td><td>S. 19 Nr. 9 links</td><td>{ORA}</td><td>Kärtchen kombinieren: größte/kleinste Summe, Summe −12</td></tr>
<tr><td>Do</td><td>S. 19 Nr. 10 links</td><td>{GRU}</td><td>Hochhaus: Ein- und Ausstieg berechnen</td></tr>
<tr><td>Do</td><td>S. 19 Nr. 11 links</td><td>{GRU}</td><td>Sportverein: Mitgliederentwicklung über drei Monate</td></tr>
<tr><td>Do</td><td>S. 19 Nr. 12</td><td>Zusatz</td><td>Würfelspiel zu zweit, wenn Zeit bleibt</td></tr>
<tr><td>HA</td><td>Rest Nr. 3, 4</td><td>{ALL}</td><td>Was am Mittwoch nicht fertig wurde</td></tr>
<tr><td>HA</td><td>„Alles klar?“ B</td><td>{ALL}</td><td>Kärtchen den Summen zuordnen</td></tr></table>
<p class="nicht">Nichts zu drucken. Für die Tafel: die beiden Bogen-Zahlengeraden, die vier Merksatz-Beispiele
und die fünf Fehlersuche-Aufgaben abschreiben, der Rest steht im Buch.</p>
</section>
"""

# ================================================================== Lösungen
loesungen = f"""
<section id="loesungen"><h2>Lösungen</h2>
<p class="lead">Selbst gerechnet, noch nicht mit dem digitalen Lösungsbuch abgeglichen.</p>
<div class="loes">
<h4>S. 18 Nr. 1 (Zahlengerade ergänzen)</h4>
<div class="kl"><div>a) −3 + 5 = <b>+2</b></div><div>b) −6 + 4 = <b>−2</b></div>
<div>c) ? + (−7) = +2 &rarr; <b>+9</b></div><div>d) ? + (−6) = −5 &rarr; <b>+1</b></div></div>
<p class="warn">Bei c) und d) war die Pfeilrichtung auf dem Foto nicht ganz sicher zu lesen – bitte kurz mit dem
Buch gegenprüfen, bevor du sie an die Tafel schreibst.</p>
<h4>S. 18 Nr. 2 (gleiche Vorzeichen)</h4>
<div class="kl"><div>a) +20</div><div>b) +40</div><div>c) −8</div><div>d) −20</div></div>
<h4>S. 18 Nr. 3 (Vorzeichen überlegen)</h4>
<div class="kl"><div>a) +18</div><div>b) +5</div><div>c) −10</div><div>d) −12</div>
<div>e) −60</div><div>f) −4</div><div>g) −20</div><div>h) −7</div></div>
<h4>S. 18 Nr. 4</h4>
<div class="kl"><div>a) −3</div><div>b) +5</div><div>c) −30</div><div>d) −8</div>
<div>e) +77</div><div>f) −14</div><div>g) −50</div><div>h) −70</div></div>
<h4>„Alles klar?“ A</h4>
<div class="kl"><div>a) +20</div><div>b) −40</div><div>c) +10</div><div>d) −56</div></div>
<h4>„Alles klar?“ B</h4>
<div class="kl"><div>a) (−25)+(+30) = +5</div><div>b) (−25)+(−30) = −55</div>
<div>c) (+25)+(+30) = +55</div><div>d) (+25)+(−30) = −5</div></div>

<h4>S. 18 Bildaufgabe (Skitour)</h4>
<p>Enzianstüble: −12,5 + 8,5 = −4 °C.<br>Der Aufstieg (920 m) ist 170 m größer als der Abstieg (750 m).<br>
Falkenhütte: 2350 − 750 + 920 = 2520 m Höhe, −4 + (−10,5) = −14,5 °C.</p>

<h4>S. 19 Nr. 5 (Fahnen)</h4>
<div class="kl"><div>a) +25+(−38) = −13</div><div>b) (−46)+(+31) = −15</div>
<div>c) (+19)+(+22) = +41</div><div>d) (−51)+(−18) = −69</div>
<div>e) (+95)+(−59) = +36</div><div>f) (−57)+(−75) = −132</div></div>

<h4>S. 19 Nr. 6 (Fehlersuche)</h4>
<p>a) 22 &rarr; richtig <b>+2</b> &nbsp;&middot;&nbsp; b) 5 &rarr; richtig <b>−5</b> &nbsp;&middot;&nbsp;
c) −54 &rarr; richtig <b>−6</b> &nbsp;&middot;&nbsp; d) −8 &rarr; richtig <b>−40</b> &nbsp;&middot;&nbsp;
e) −3,75 &rarr; richtig <b>−4,75</b></p>

<h4>S. 19 Nr. 9 links (Kärtchen, gelb 12/−10/18, rot −15/−5/−24)</h4>
<p>a) Größte Summe: 18 + (−5) = <b>13</b><br>b) Kleinste Summe: −10 + (−24) = <b>−34</b><br>
c) Summe −12: 12 + (−24) = <b>−12</b></p>

<h4>S. 19 Nr. 10 links (Hochhaus)</h4>
<p>a) Tim: 0 + 7 − 9 + 6 = +4, er steigt im <b>4. Obergeschoss</b> aus.<br>
b) Tom kommt im 7. Geschoss an, die Bewegungen ergeben zusammen +2 (−4 + 12 − 6). Start: 7 − 2 = <b>5. Geschoss</b>.</p>

<h4>S. 19 Nr. 11 links (Sportverein)</h4>
<p>−26 + 31 − 17 = <b>−12</b>. Ende März hat der Verein 12 Mitglieder weniger als zu Jahresbeginn.</p>

<h4>S. 19 Nr. 12 (Würfelspiel)</h4>
<p>Offenes Spiel, keine feste Lösung – Regeln stehen im Buch.</p>
</div></section>
"""

# ================================================================== Ausblick
ausblick = """
<section id="ausblick"><h2>Ausblick</h2>
<p class="lead">Nach dem Stoffverteilungsplan 26/27. Vergleichen (Woche 2) ist erledigt, diese beiden Stunden
decken den Einstieg in die Addition (Woche 3) ab.</p>
<h3>Offen</h3>
<ul><li>Alle Lösungen hier sind selbst gerechnet, noch nicht mit dem digitalen Lösungsbuch abgeglichen –
besonders S. 18 Nr. 1 c) und d) einmal gegenlesen (Pfeilrichtung auf dem Foto unsicher).</li>
<li>S. 19 Nr. 7 (Lösungswort-Rätsel) und Nr. 6 links (Kärtchen mit Lösungswort) sind bewusst nicht eingebaut,
weil die kleine Beschriftung auf dem Foto nicht sicher lesbar war. Wenn du die Aufgabe willst, bitte nochmal
scharf fotografieren.</li>
<li>Nr. 10 rechts (Zahlenkärtchen frei kombinieren) ist offen, eignet sich gut als Zusatzaufgabe für Schnelle.</li>
<li>Donnerstag ist als Einzelstunde (45 min) geplant – falls es doch eine Doppelstunde ist, gerne sagen, dann
baue ich Nr. 7, 10 rechts und mehr von Nr. 12 mit ein.</li></ul>
</section>
"""

html = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rationale Zahlen 2 – Addieren</title><style>{CSS}</style></head><body>
<div class="wrap"><header class="kopf"><h1>Rationale Zahlen 2: Addieren</h1>
<p class="sub">Klasse 7c · Mittwoch + Donnerstag, je Einzelstunde · Buch S. 18–19 · alles in einer Datei</p></header></div>
<nav><div class="wrap"><a href="#mittwoch">Mittwoch</a><a href="#donnerstag">Donnerstag</a><a href="#merkheft">Merkheft</a>
<a href="#aufgaben">Aufgaben</a><a href="#loesungen">Lösungen</a><a href="#ausblick">Ausblick</a></div></nav>
<div class="wrap">{verlauf_mi}<div class="tafelblock-wrap">{tafel_mi}</div>{verlauf_do}<div class="tafelblock-wrap">{tafel_do}</div>{merkheft}{aufgaben}{loesungen}{ausblick}
<footer>Entwurf. PDFs erst nach Freigabe. Generator: baue_stunde2.py</footer></div></body></html>"""

ziel = Path(__file__).with_name("Rationale Zahlen 2 – Addieren – ALLES.html")
ziel.write_text(html, encoding="utf-8")
print("geschrieben:", ziel, f"({len(html) // 1024} KB)")
