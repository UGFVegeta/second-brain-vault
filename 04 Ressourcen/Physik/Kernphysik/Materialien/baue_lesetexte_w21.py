#!/usr/bin/env python3
"""Lesetexte „Kernkraft: Pro und Contra“ für W21 (Nutzen und Risiko abwägen).
Ein A3-Bogen, doppelseitig = 4 A4-Seiten: S. 1 Grundlagen (alle), S. 2 Gruppe A Pro, S. 3 Gruppe B Contra, S. 4 Fragen und Protokoll.
Etwa 70 % Information, 30 % Fragen. Diagramme als berechnete SVG. Seite 5 = Seite 4 als Lösung (ausgefülltes Original).
Zahlen und Quellen: „Kernkraft in Zahlen – Vergleichswerte.md“ und die beiden Faktencheck-Notizen. Strahlenwerte nach BfS.
Aufruf: python3 baue_lesetexte_w21.py  -> Lesetexte Kernkraft W21.html und .pdf"""
import math
from baue_blaetter_k10 import HIER, MAG, aufg, antwort, dokument, drucke, LEGENDE, NAME

LESE_CSS = ('<style>.lese p{margin:0 0 2mm;font-size:10pt;line-height:1.42}.lese h3{font-size:11pt;margin:3mm 0 1mm;color:#14171c}'
            '.lese h3 .n{display:inline-block;min-width:5mm;color:#66798E}.quelle{font-size:7.5pt;color:#7a818c;margin:1mm 0 0;line-height:1.3}'
            '.dia{display:flex;gap:6mm;margin:2mm 0 1mm}.dia>figure{flex:1;margin:0;border:0.6pt solid #c9ced6;padding:2mm 2.5mm 1.5mm}'
            '.dia figcaption{font-size:8.5pt;font-weight:600;margin-bottom:1mm}.dia svg{width:100%;display:block}'
            '.auftrag{border:0.9pt solid #66798E;background:#F3F5F8;padding:2.5mm 4mm;font-size:10pt;margin:0 0 3mm}'
            '.auftrag b{color:#14171c}.gruppe{display:inline-block;font-size:8.5pt;font-weight:700;letter-spacing:.05em;text-transform:uppercase;'
            'color:#fff;padding:1mm 2.5mm;border-radius:2pt;margin-right:2mm}.ga{background:#2E7D5B}.gb{background:#B4462F}'
            '.fm{border-collapse:collapse;width:100%;font-size:9.5pt;margin:1mm 0 2mm}.fm th,.fm td{border:0.6pt solid #14171c;padding:1mm 2mm;text-align:left;height:6.5mm}'
            '.fm th{background:#EEF1F5}.fm td.l{color:' + MAG + ';font-weight:600}.proto td{height:8mm}.zwei{display:flex;gap:7mm}.zwei>div{flex:1}.zwei h2.aufgabe{font-size:10pt}.loes .loesungstext{font-size:9pt;line-height:1.3}.loes .antw.loesungstext{margin-bottom:1mm}.loes .proto td{height:6.5mm}'
            '.kasten{border-left:2.5pt solid #66798E;padding:1mm 0 1mm 3mm;margin:2mm 0;font-size:9.5pt}</style>')

GRUEN, ROT, GRAU = "#2E7D5B", "#B4462F", "#66798E"


# ---------------------------------------------------------------- Diagramme
def balken(daten, einheit, farbe, hervor=(), breite=300):
    """Waagerechte Balken, linear. daten: (Name, Wert, Beschriftung). hervor: Namen in Farbe, Rest grau."""
    zeile, links, rechts = 17, 78, 52
    vmax = max(w for _, w, _ in daten)
    h = zeile * len(daten) + 16
    s = f'<svg viewBox="0 0 {breite} {h}" xmlns="http://www.w3.org/2000/svg" font-family="Avenir Next, Helvetica, Arial" font-size="9">'
    for i, (name, w, txt) in enumerate(daten):
        y = 4 + i * zeile
        lang = max((breite - links - rechts) * w / vmax, 1.2)
        f = farbe if name in hervor else "#AEB6C1"
        s += (f'<text x="{links - 4}" y="{y + 10}" text-anchor="end" fill="#14171c">{name}</text>'
              f'<rect x="{links}" y="{y}" width="{lang:.1f}" height="12" fill="{f}"/>'
              f'<text x="{links + lang + 3:.1f}" y="{y + 10}" fill="#14171c" font-weight="600">{txt}</text>')
    s += f'<text x="{links}" y="{h - 2}" fill="#66798E" font-size="8">{einheit}</text></svg>'
    return s


def zeitachse():
    """Logarithmische Zeitachse 10 Jahre bis 1 Million Jahre."""
    b, l, r = 520, 30, 48
    x = lambda jahre: l + (b - l - r) * (math.log10(jahre) - 1) / 5
    s = f'<svg viewBox="0 0 {b} 96" xmlns="http://www.w3.org/2000/svg" font-family="Avenir Next, Helvetica, Arial" font-size="9">'
    s += f'<line x1="{l}" y1="46" x2="{b - r}" y2="46" stroke="#14171c" stroke-width="1.4"/>'
    for e in range(1, 7):
        xx = x(10 ** e)
        lab = {1: "10", 2: "100", 3: "1000", 4: "10 000", 5: "100 000", 6: "1 Mio."}[e]
        s += f'<line x1="{xx:.1f}" y1="42" x2="{xx:.1f}" y2="50" stroke="#14171c"/><text x="{xx:.1f}" y="62" text-anchor="middle" fill="#66798E">{lab}</text>'
    punkte = [(30, "Cs-137 halbiert", ROT, 1), (300, "Cs-137 fast weg", ROT, 0), (4500, "Pyramiden", GRAU, 1),
              (24000, "Pu-239 halbiert", ROT, 0), (300000, "Homo sapiens", GRAU, 1), (1000000, "Endlager sicher", ROT, 0)]
    for j, t, f, oben in punkte:
        xx = x(j)
        if oben:
            s += f'<line x1="{xx:.1f}" y1="42" x2="{xx:.1f}" y2="30" stroke="{f}" stroke-width="0.8"/><text x="{xx:.1f}" y="25" text-anchor="middle" fill="{f}" font-weight="600">{t}</text>'
        else:
            s += f'<line x1="{xx:.1f}" y1="50" x2="{xx:.1f}" y2="78" stroke="{f}" stroke-width="0.8"/><text x="{xx:.1f}" y="88" text-anchor="middle" fill="{f}" font-weight="600">{t}</text>'
        s += f'<circle cx="{xx:.1f}" cy="46" r="3.6" fill="{f}"/>'
    s += f'<text x="{b - r}" y="10" text-anchor="end" fill="#66798E" font-size="8">Jahre; jeder Strich ist zehnmal so viel wie der vorige</text></svg>'
    return s


def kosten():
    """Geplante und tatsächliche Kosten zweier neuer Reaktoren in Europa (Mrd. Euro)."""
    b, l = 300, 78
    daten = [("Flamanville 3", 3.3, 23.7, "Frankreich", "23,7"), ("Olkiluoto 3", 3.0, 11.0, "Finnland", "etwa 11")]
    sk = (b - l - 50) / 24
    s = f'<svg viewBox="0 0 {b} 100" xmlns="http://www.w3.org/2000/svg" font-family="Avenir Next, Helvetica, Arial" font-size="9">'
    for i, (n, plan, ist, land, ist_txt) in enumerate(daten):
        y = 4 + i * 44
        s += (f'<text x="{l - 4}" y="{y + 12}" text-anchor="end" fill="#14171c" font-weight="600">{n}</text>'
              f'<text x="{l - 4}" y="{y + 24}" text-anchor="end" fill="#66798E" font-size="8">{land}</text>'
              f'<rect x="{l}" y="{y}" width="{plan * sk:.1f}" height="12" fill="#AEB6C1"/>'
              f'<text x="{l + plan * sk + 3:.1f}" y="{y + 10}" fill="#14171c">geplant {str(plan).replace(".", ",")}</text>'
              f'<rect x="{l}" y="{y + 15}" width="{ist * sk:.1f}" height="12" fill="{ROT}"/>'
              f'<text x="{l + ist * sk + 3:.1f}" y="{y + 25}" fill="#14171c" font-weight="600">{ist_txt}</text>')
    s += f'<text x="{l}" y="97" fill="#66798E" font-size="8">Milliarden Euro</text></svg>'
    return s


def figur(titel, svg):
    return f'<figure><figcaption>{titel}</figcaption>{svg}</figure>'


TOTE = [("Kohle", 24.6, "24,6"), ("Öl", 18.4, "18,4"), ("Biomasse", 4.6, "4,6"), ("Erdgas", 2.8, "2,8"),
        ("Wasserkraft", 1.3, "1,3"), ("Wind", 0.04, "0,04"), ("Kernkraft", 0.03, "0,03"), ("Solar", 0.02, "0,02")]
CO2 = [("Kohle", 820, "820"), ("Erdgas", 490, "490"), ("Solar", 48, "48"), ("Wasserkraft", 24, "24"), ("Kernkraft", 12, "12"), ("Wind", 11, "11")]
ANTEIL = [("1996", 17.5, "17,5 %"), ("2025", 8.8, "8,8 %")]


# ---------------------------------------------------------------- Seite 1: Grundlagen
def seite1():
    return ('<div class="kopf"><div><span class="chip">W21</span><h1>Kernkraft: Pro und Contra</h1></div></div>' + NAME
            + '<div class="auftrag"><b>So arbeitet ihr (20 Minuten):</b> Lest alle diese Seite. Dann liest <span class="gruppe ga">Gruppe A</span>Seite 2 '
              '(Argumente für Kernkraft) und <span class="gruppe gb">Gruppe B</span>Seite 3 (Argumente gegen Kernkraft). Beantwortet danach auf Seite 4 '
              'die Fragen eurer Gruppe und die gemeinsamen Fragen. Die Tabelle C3 auf Seite 4 füllt ihr während der Diskussion aus.</div>'
            + '<div class="lese">'
              '<h3>Wie ein Kernkraftwerk Strom erzeugt</h3>'
              '<p>Im Reaktor werden Uran-235-Kerne von Neutronen gespalten. Dabei entstehen zwei kleinere Kerne, zwei bis drei neue Neutronen und viel Wärme. '
              'Die Wärme bringt Wasser zum Sieden, der Dampf treibt eine Turbine und einen Generator an. Bis auf den Reaktor funktioniert das wie in einem Kohlekraftwerk. '
              'Der Unterschied: Kernspaltung setzt pro Kilogramm Brennstoff etwa eine Million Mal so viel Energie frei wie das Verbrennen von Kohle. '
              'Ein Brennstoff-Pellet von 6 g, so groß wie eine Fingerkuppe, liefert im Reaktor so viel Wärme wie etwa 700 kg Steinkohle.</p>'
              '<h3>Kernkraft in Deutschland</h3>'
              '<p>Im Jahr 2000 kam fast jede dritte Kilowattstunde aus Kernkraftwerken. Die rot-grüne Regierung beschloss 2002 mit den Energiekonzernen den Ausstieg. '
              'Die schwarz-gelbe Regierung verlängerte die Laufzeiten 2010. Nach dem Unfall in Fukushima beschloss der Bundestag 2011 mit großer Mehrheit, '
              'bis 2022 auszusteigen. Wegen der Energiekrise liefen die letzten drei Kraftwerke noch bis zum 15. April 2023. Seitdem ist keines mehr am Netz. '
              'Weltweit sind gut 400 Reaktoren in Betrieb, in der EU ist Kernkraft mit etwa 23 % die größte einzelne Stromquelle.</p>'
              '<h3>Was bleibt übrig?</h3>'
              '<p>Abgebrannte Brennelemente sind hochradioaktiv. In Deutschland sind rund 10 500 t davon entstanden, verpackt sind das rund 27 000 m³. '
              'Ein Endlager dafür gibt es noch nicht. Es wird gesucht und muss eine Million Jahre lang sicher sein. Wie lange der Abfall strahlt, '
              'hängt von den Nukliden ab: Cäsium-137 hat eine Halbwertszeit von 30 Jahren, Plutonium-239 von 24 000 Jahren.</p></div>'
            + '<div class="dia">' + figur("Wie lange strahlt der Abfall? Zeitachse in Jahren", zeitachse()) + '</div>'
            + '<div class="kasten"><b>So liest du die Texte:</b> Ein <b>Fakt</b> lässt sich nachprüfen oder messen, zum Beispiel „Plutonium-239 hat eine '
              'Halbwertszeit von 24 000 Jahren“. Eine <b>Meinung</b> bewertet, zum Beispiel „Kernkraft ist zu gefährlich“. Beide Seiten nutzen richtige Fakten. '
              'Gestritten wird darüber, welche Fakten wichtiger sind. Achte darauf, was eine Seite weglässt.</div>'
            + '<p class="quelle">Quellen: BASE und BGE (Abfallmengen, Endlagersuche); Bundeszentrale für politische Bildung (Geschichte des Ausstiegs); '
              'Fraunhofer ISE (Strommix); Karlsruher Nuklidkarte (Halbwertszeiten); IAEA PRIS (Reaktoren weltweit).</p>')


# ---------------------------------------------------------------- Seite 2: Pro
def seite2():
    return ('<div class="kopf"><div><span class="gruppe ga">Gruppe A</span><h1>Argumente für Kernkraft</h1></div></div>'
            + '<div class="lese">'
              '<h3><span class="n">1</span>Kaum CO₂</h3>'
              '<p>Ein Kernkraftwerk verbrennt nichts. Rechnet man Bau, Uranabbau und Entsorgung mit ein, entstehen etwa 12 g CO₂ pro Kilowattstunde. '
              'Das ist so wenig wie bei Windkraft und viel weniger als bei Kohle mit etwa 820 g. Der Weltklimarat (IPCC) zählt Kernkraft deshalb zu den '
              'klimafreundlichen Energiequellen. Auch die EU stuft sie seit 2022 unter Bedingungen als nachhaltig ein.</p>'
              '<h3><span class="n">2</span>Sehr sicher, gemessen an der Strommenge</h3>'
              '<p>Jede Energiequelle fordert Opfer: durch Unfälle beim Abbau, beim Bau oder durch Luftverschmutzung. Rechnet man die Todesfälle auf die erzeugte '
              'Strommenge um, liegt Kernkraft mit 0,03 Toten pro Terawattstunde auf der Höhe von Wind und Sonne, obwohl Tschernobyl und Fukushima eingerechnet sind. '
              'Kohle liegt etwa 800-mal so hoch, vor allem wegen Feinstaub. Eine Studie von 2022 kam zu dem Ergebnis, dass nach dem deutschen Ausstieg 2011 vor allem '
              'Kohlekraftwerke den Atomstrom ersetzten. Die zusätzliche Luftverschmutzung kostet danach jedes Jahr 3 bis 8 Milliarden Euro, vor allem durch vorzeitige Todesfälle.</p></div>'
            + '<div class="dia">' + figur("Todesfälle pro erzeugter Strommenge", balken(TOTE, "Tote pro Terawattstunde (TWh)", GRUEN, ("Kernkraft",)))
            + figur("CO₂ über die ganze Lebensdauer", balken(CO2, "Gramm CO₂ pro Kilowattstunde", GRUEN, ("Kernkraft",))) + '</div>'
            + '<div class="lese">'
              '<h3><span class="n">3</span>Strom bei jedem Wetter</h3>'
              '<p>Ein Kernkraftwerk liefert Tag und Nacht, im Sommer wie im Winter. Es läuft im Jahr etwa 90 % der Zeit mit voller Leistung. '
              'Ein großes Kraftwerk wie Isar 2 erzeugte so viel Strom wie etwa 1000 moderne Windräder an Land. Bei einer Dunkelflaute, wenn im Winter tagelang '
              'kaum Wind weht und die Sonne wenig scheint, liefert es trotzdem. Dafür braucht es weniger Speicher und weniger Reservekraftwerke.</p>'
              '<h3><span class="n">4</span>Wenig Fläche, wenig Abfall</h3>'
              '<p>Ein Kernkraftwerk braucht mit Gelände etwa 1 km². Ein Windpark mit gleicher Jahresmenge Strom verteilt sich auf rund 200 km². '
              'Für den Strom, den eine Familie in einem Jahr verbraucht, entstehen etwa 7 g hochradioaktiver Abfall. Mit Braunkohle wären es etwa 4 t CO₂.</p>'
              '<h3><span class="n">5</span>Im Normalbetrieb kaum Strahlung</h3>'
              '<p>Wer in der Nähe eines Kernkraftwerks wohnt, bekommt dadurch laut Bundesamt für Strahlenschutz weniger als 0,01 Millisievert im Jahr ab. '
              'Die natürliche Strahlung aus Boden, Luft und Nahrung liegt in Deutschland bei etwa 2,1 Millisievert im Jahr, also mehr als 200-mal so hoch.</p>'
              '<h3><span class="n">6</span>Andere Länder setzen weiter darauf</h3>'
              '<p>Frankreich erzeugt etwa zwei Drittel seines Stroms mit Kernkraft. Viele Länder bauen neue Reaktoren, darunter Länder ohne Atomwaffen wie Polen, '
              'die Türkei oder Ägypten. Über 30 Staaten haben 2023 erklärt, die Kernkraft bis 2050 verdreifachen zu wollen.</p></div>'
            + '<p class="quelle">Quellen: IPCC, 5. Sachstandsbericht 2014 (CO₂ pro kWh, Mittelwerte); Our World in Data, „Safest sources of energy“ (Todesfälle); '
              'Jarvis, Deschenes, Jha: The Private and External Costs of Germany\'s Nuclear Phase-Out, Journal of the European Economic Association 2022; '
              'Bundesamt für Strahlenschutz (Strahlenbelastung); BASE (Abfall); Erklärung zur Verdreifachung der Kernenergie, Klimakonferenz COP28 (2023).</p>')


# ---------------------------------------------------------------- Seite 3: Contra
def seite3():
    return ('<div class="kopf"><div><span class="gruppe gb">Gruppe B</span><h1>Argumente gegen Kernkraft</h1></div></div>'
            + '<div class="lese">'
              '<h3><span class="n">1</span>Abfall für eine Million Jahre</h3>'
              '<p>Der hochradioaktive Abfall muss eine Million Jahre sicher von Menschen und Grundwasser getrennt bleiben. Zum Vergleich: Die Pyramiden sind '
              'etwa 4500 Jahre alt. Ein Endlager gibt es in Deutschland nicht. Die Suche sollte bis 2031 einen Standort finden, die zuständige Bundesgesellschaft '
              'rechnet inzwischen mit deutlich später. Das alte Salzbergwerk Asse zeigt, was schiefgehen kann: Dort dringt Wasser ein, rund 126 000 Fässer '
              'sollen wieder herausgeholt werden.</p>'
              '<h3><span class="n">2</span>Unfälle treffen ganze Regionen</h3>'
              '<p>Schwere Unfälle sind selten, aber ihre Folgen sind riesig. Nach Tschernobyl 1986 wurde eine Sperrzone von etwa 2600 km² eingerichtet, '
              'die bis heute gilt. In Fukushima schmolzen 2011 drei Reaktorkerne, über 150 000 Menschen verließen ihre Heimat. Durch Strahlung ist dort ein '
              'Todesfall anerkannt, durch die Belastungen der Evakuierung starben nach Angaben Japans rund 2300 Menschen. Japan rechnet mit Kosten von mehr als '
              '20 Billionen Yen, das sind weit über 100 Milliarden Euro. Seit 2022 zeigt das besetzte Kraftwerk Saporischschja in der Ukraine, dass auch Krieg ein Risiko ist.</p>'
              '<h3><span class="n">3</span>Neue Kraftwerke sind teuer und langsam</h3>'
              '<p>Neue Reaktoren in Europa wurden viel teurer als geplant. Flamanville 3 in Frankreich sollte 3,3 Milliarden Euro kosten, der französische '
              'Rechnungshof kommt auf 23,7 Milliarden. Es ging 12 Jahre zu spät ans Netz. Olkiluoto 3 in Finnland brauchte 18 statt 4 Jahre Bauzeit. '
              'Weltweit dauert der Bau eines Reaktors im Schnitt etwa 10 Jahre.</p></div>'
            + '<div class="dia">' + figur("Kosten neuer Reaktoren in Europa", kosten())
            + figur("Anteil der Kernkraft am Strom der Welt", balken(ANTEIL, "Prozent des weltweit erzeugten Stroms", ROT, ("2025",))) + '</div>'
            + '<div class="lese">'
              '<h3><span class="n">4</span>Die Welt baut vor allem Wind und Sonne</h3>'
              '<p>Der Anteil der Kernkraft am Strom der Welt hat sich seit 1996 etwa halbiert, von 17,5 % auf unter 9 %. Die Strommenge aus Kernkraft ist '
              'ungefähr gleich geblieben, alles andere ist schneller gewachsen. Selbst China, das die meisten Reaktoren baut, erzeugt mit Wind und Sonne etwa '
              'fünfmal so viel Strom wie mit Kernkraft. Kleine modulare Reaktoren (SMR) gelten als Hoffnung, im Westen läuft aber noch keiner kommerziell.</p>'
              '<h3><span class="n">5</span>Abhängig vom Brennstoff</h3>'
              '<p>Uran wird vor allem in Kasachstan abgebaut (etwa 40 % der Welt). Einen großen Teil der weltweiten Anreicherung hat Russland. Wind- und '
              'Solaranlagen kauft man einmal, danach brauchen sie keinen Brennstoff mehr. Ein Kernkraftwerk braucht immer wieder neue Brennelemente.</p>'
              '<h3><span class="n">6</span>Kühlwasser und Waffen</h3>'
              '<p>Kraftwerke an Flüssen brauchen viel Kühlwasser. Im heißen Sommer 2022 musste Frankreich Reaktoren drosseln und führte erstmals seit Jahrzehnten '
              'mehr Strom ein als aus. Außerdem lässt sich die Technik zum Anreichern von Uran auch für Atomwaffen nutzen. Deshalb kontrolliert die '
              'Internationale Atomenergiebehörde die Anlagen weltweit.</p></div>'
            + '<p class="quelle">Quellen: BASE und BGE (Endlager, Asse); Our World in Data, „Nuclear Energy“ (Fukushima, nach Angaben der japanischen '
              'Wiederaufbaubehörde 2020); Cour des comptes 2025 (Flamanville 3); World Nuclear Industry Status Report 2026 (Weltanteil, Bauzeiten); '
              'World Nuclear Association (Uran, Anreicherung); RTE, französischer Netzbetreiber (Stromaustausch 2022); IAEA.</p>')


# ---------------------------------------------------------------- Seite 4: Fragen und Protokoll
FM = [("Kohle verursacht pro Strommenge etwa 800-mal so viele Todesfälle wie Kernkraft.", "Fakt (OWID)"),
      ("Kernkraft ist die Energie der Zukunft.", "Meinung"),
      ("Flamanville 3 kostete rund siebenmal so viel wie geplant.", "Fakt (Rechnungshof)"),
      ("Ein Endlager wird man sowieso nie finden.", "Meinung")]


def seite4(l):
    fm = ('<table class="fm"><tr><th>Aussage</th><th style="width:38mm">Fakt oder Meinung?</th></tr>'
          + "".join(f'<tr><td>{a}</td>' + (f'<td class="l">{b}</td>' if l else "<td></td>") + "</tr>" for a, b in FM) + "</table>")
    proto = ('<table class="fm proto"><tr><th style="width:24mm">Gruppe</th><th>Argument</th><th style="width:34mm">Zahl dazu</th><th style="width:32mm">Fakt oder Meinung?</th></tr>'
             + ("".join(f'<tr><td>{g}</td><td class="l">{a}</td><td class="l">{z}</td><td class="l">{f}</td></tr>' for g, a, z, f in (
                 ("A Pro", "kaum CO₂", "12 g pro kWh", "Fakt"), ("B Contra", "Abfall sehr lange gefährlich", "1 Mio. Jahre", "Fakt"),
                 ("A Pro", "Kernkraft ist sicher", "0,03 Tote pro TWh", "Fakt, „sicher“ ist Wertung"),
                 ("B Contra", "zu teuer", "Flamanville 7-mal so teuer", "Fakt"))) if l else "<tr><td></td><td></td><td></td><td></td></tr>" * 4)
             + "</table>")
    return (('<div class="loes">' if l else '<div>') + '<div class="kopf"><div><span class="chip">W21</span><h1>Fragen und Diskussionsprotokoll</h1></div>'
            + ('<div class="loesung-marker">Lösung</div>' if l else "") + '</div>' + LEGENDE
            + '<div class="zwei"><div><p class="frage"><span class="gruppe ga">Gruppe A</span>Pro</p>'
            + aufg("A1", 0, "Nenne drei Argumente für Kernkraft, jeweils mit einer Zahl.")
            + antwort("kaum CO₂ (12 g pro kWh); wenige Todesfälle pro Strommenge (0,03 pro TWh); läuft bei jedem Wetter (etwa 90 % der Zeit); "
                      "wenig Abfall (7 g pro Familie und Jahr); wenig Fläche (1 km²).", l, 3)
            + aufg("A2", 1, "Lies im Diagramm ab: Wie viel mal so viele Todesfälle pro TWh verursacht Kohle wie Kernkraft?")
            + antwort("24,6 : 0,03 ≈ 820, also etwa 800-mal so viele.", l, 1)
            + aufg("A3", 2, "Gegencheck: Welches Argument der Gruppe B ist für deine Seite am schwersten zu entkräften? Begründe.")
            + antwort("Zum Beispiel das Endlager: Eine Million Jahre lässt sich nicht mit Erfahrung belegen, und in Deutschland gibt es noch keinen Standort.", l, 2)
            + '</div><div><p class="frage"><span class="gruppe gb">Gruppe B</span>Contra</p>'
            + aufg("B1", 0, "Nenne drei Argumente gegen Kernkraft, jeweils mit einer Zahl.")
            + antwort("Abfall muss 1 Mio. Jahre sicher lagern; Sperrzone Tschernobyl 2600 km²; Flamanville 23,7 statt 3,3 Mrd. €; "
                      "Weltanteil von 17,5 % auf unter 9 % gesunken; Uran zu etwa 40 % aus Kasachstan.", l, 3)
            + aufg("B2", 1, "Lies im Diagramm ab: Um welchen Faktor wurde Flamanville 3 teurer als geplant?")
            + antwort("23,7 : 3,3 ≈ 7, also etwa siebenmal so teuer.", l, 1)
            + aufg("B3", 2, "Gegencheck: Welches Argument der Gruppe A ist für deine Seite am schwersten zu entkräften? Begründe.")
            + antwort("Zum Beispiel das CO₂: Kernkraft liegt so niedrig wie Wind. Und nach 2011 ersetzte vor allem Kohle den Atomstrom, das kostete Gesundheit.", l, 2)
            + '</div></div><p class="frage" style="margin-top:3mm"><b>Alle</b></p>'
            + aufg("C1", 0, "Fakt oder Meinung?") + fm
            + aufg("C2", 1, "Cäsium-137 hat eine Halbwertszeit von 30 Jahren. Welcher Anteil ist nach 300 Jahren noch übrig?")
            + antwort("300 Jahre sind 10 Halbwertszeiten: (1/2)¹⁰ = 1/1024, also etwa ein Tausendstel.", l, 1)
            + aufg("C3", 1, "Protokoll der Diskussion: Notiere vier Argumente, die genannt werden.") + proto
            + aufg("C4", 2, "Deine Stellungnahme: Schreibe ins Heft 3 bis 5 Sätze. Nutze mindestens zwei Zahlen und trenne Fakt und Meinung." + (' <span class="loesungstext">(individuell)</span>' if l else ""))
            + '</div>')


if __name__ == "__main__":
    html, pdf = "lesetexte_kernkraft_w21.html", "Lesetexte Kernkraft W21.pdf"
    doc = dokument("Kernkraft: Pro und Contra – W21", [seite1(), seite2(), seite3(), seite4(False), seite4(True)])
    doc = doc.replace("</head>", LESE_CSS + "</head>", 1)
    (HIER / html).write_text(doc, encoding="utf-8")
    drucke(html, pdf)
