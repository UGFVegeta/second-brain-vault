#!/usr/bin/env python3
"""Lesetexte „Kernkraft: Pro und Contra“ für W21 (Nutzen und Risiko abwägen).
Zwei Hefte, je ein A3-Bogen doppelseitig = 4 A4-Seiten:
  Gruppe A (Pro):    Infoblatt 1 Klima und Gesundheit, 2 Versorgung und Fläche, 3 Strahlung, Abfall, Welt, Seite 4 Aufgabenblatt
  Gruppe B (Contra): Infoblatt 1 Abfall und Endlager, 2 Unfälle und Sicherheit, 3 Kosten, Zeit, Abhängigkeit, Seite 4 Aufgabenblatt
In der Gruppe liest jeder ein Infoblatt; die vierte Person ist Zeitwächter und füllt das Aufgabenblatt aus (Rollen stehen oben auf Seite 4).
Etwa 70 % Information, 30 % Fragen. Diagramme als berechnete SVG. Seite 5 = Aufgabenblatt als Lösung (ausgefülltes Original).
Zahlen und Quellen: „Kernkraft in Zahlen – Vergleichswerte.md“ und die Faktencheck-Notizen. Strahlenwerte nach BfS.
Aufruf: python3 baue_lesetexte_w21.py  -> Lesetexte Kernkraft Pro W21.pdf und Lesetexte Kernkraft Contra W21.pdf"""
import math
from baue_blaetter_k10 import HIER, MAG, aufg, antwort, dokument, drucke, LEGENDE

LESE_CSS = ('<style>.lese p{margin:0 0 2.2mm;font-size:10.3pt;line-height:1.45}.lese h3{font-size:11pt;margin:3.5mm 0 1mm;color:#14171c}'
            '.quelle{font-size:7.5pt;color:#7a818c;margin:2mm 0 0;line-height:1.3}'
            '.dia{display:flex;gap:6mm;margin:2.5mm 0 1.5mm}.dia>figure{flex:1;margin:0;border:0.6pt solid #c9ced6;padding:2mm 2.5mm 1.5mm}'
            '.dia figcaption{font-size:8.5pt;font-weight:600;margin-bottom:1mm}.dia svg{width:100%;display:block}'
            '.gruppe{display:inline-block;font-size:8.5pt;font-weight:700;letter-spacing:.05em;text-transform:uppercase;'
            'color:#fff;padding:1mm 2.5mm;border-radius:2pt;margin-right:2mm;vertical-align:2px}.ga{background:#2E7D5B}.gb{background:#B4462F}'
            '.fm{border-collapse:collapse;width:100%;font-size:9.5pt;margin:1mm 0 2mm}.fm th,.fm td{border:0.6pt solid #14171c;padding:1mm 2mm;text-align:left;height:7mm;vertical-align:top}'
            '.fm th{background:#EEF1F5;height:auto}.fm td.l{color:' + MAG + ';font-weight:600}.fm td.v{font-weight:600;width:26mm}.doku td{height:14mm}'
            '.kasten{border-left:2.5pt solid #66798E;padding:1mm 0 1mm 3mm;margin:2mm 0;font-size:9.5pt}'
            '.ablauf{border:0.9pt solid #66798E;background:#F3F5F8;padding:2mm 4mm;font-size:9.5pt;margin:0 0 2mm}.ablauf ol{margin:1mm 0 0;padding-left:5mm}'
            '.loes .loesungstext{font-size:9.3pt;line-height:1.3}.loes .antw.loesungstext{margin-bottom:1mm}.loes .doku td{height:auto}</style>')

GRUEN, ROT, GRAU = "#2E7D5B", "#B4462F", "#66798E"


# ---------------------------------------------------------------- Diagramme
def balken(daten, einheit, farbe, hervor=(), breite=300):
    """Waagerechte Balken, linear. daten: (Name, Wert, Beschriftung). hervor: Namen in Farbe, Rest grau."""
    zeile, links, rechts = 17, 92, 74
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


def dia(*figuren):
    return '<div class="dia">' + "".join(figur(t, s) for t, s in figuren) + '</div>'


def neben(titel, svg, html):
    """Einzelnes Diagramm (halbe Breite) neben einem Textabschnitt."""
    return (f'<div class="dia"><figure style="flex:0 0 84mm">{"<figcaption>" + titel + "</figcaption>"}{svg}</figure>'
            f'<div class="lese" style="flex:1">{html}</div></div>')


def kopf_info(gruppe, nr, titel):
    g = '<span class="gruppe ga">Gruppe A Pro</span>' if gruppe == "A" else '<span class="gruppe gb">Gruppe B Contra</span>'
    return f'<div class="kopf"><div>{g}<h1>Infoblatt {nr}: {titel}</h1></div></div>'


def quelle(text):
    return f'<p class="quelle">Quellen: {text}</p>'


# ================================================================ Gruppe A: Pro
def a1():
    tote = [("Kohle", 24.6, "24,6"), ("Öl", 18.4, "18,4"), ("Biomasse", 4.6, "4,6"), ("Erdgas", 2.8, "2,8"),
            ("Wasserkraft", 1.3, "1,3"), ("Wind", 0.04, "0,04"), ("Kernkraft", 0.03, "0,03"), ("Solar", 0.02, "0,02")]
    co2 = [("Kohle", 820, "820"), ("Erdgas", 490, "490"), ("Solar", 48, "48"), ("Wasserkraft", 24, "24"), ("Kernkraft", 12, "12"), ("Wind", 11, "11")]
    return (kopf_info("A", 1, "Klima und Gesundheit") + '<div class="lese">'
            '<h3>Strom fast ohne CO₂</h3>'
            '<p>Ein Kohlekraftwerk verbrennt Kohle, dabei entsteht CO₂. Ein Kernkraftwerk verbrennt nichts: Die Wärme kommt aus der Spaltung von Urankernen. '
            'CO₂ entsteht nur beim Bau, beim Uranabbau, bei der Anreicherung und bei der Entsorgung. Rechnet man das alles über die ganze Lebensdauer zusammen, '
            'kommt Kernkraft auf etwa 12 g CO₂ pro Kilowattstunde. Das ist so wenig wie bei Windkraft und viel weniger als bei Kohle mit etwa 820 g. '
            'Der Weltklimarat (IPCC) zählt Kernkraft deshalb zu den klimafreundlichen Energiequellen. Die EU stuft sie seit 2022 unter Bedingungen als nachhaltig ein.</p>'
            '<p>Für Deutschland heißt das: 2010 kam noch etwa jede fünfte Kilowattstunde aus Kernkraftwerken. Dieser Strom war fast CO₂-frei. '
            'Wird er durch Kohle ersetzt, steigt der CO₂-Ausstoß, wird er durch Wind und Sonne ersetzt, bleibt er niedrig.</p></div>'
            + dia(("CO₂ über die ganze Lebensdauer", balken(co2, "Gramm CO₂ pro Kilowattstunde", GRUEN, ("Kernkraft",))),
                  ("Todesfälle pro erzeugter Strommenge", balken(tote, "Tote pro Terawattstunde (TWh)", GRUEN, ("Kernkraft",))))
            + '<div class="lese">'
            '<h3>Wie gefährlich ist welcher Strom?</h3>'
            '<p>Jede Art der Stromerzeugung kostet Menschenleben: durch Unfälle im Bergbau, auf Baustellen und bei der Wartung, vor allem aber durch '
            'Luftverschmutzung. Beim Verbrennen von Kohle, Öl und Holz entstehen Feinstaub und Schadstoffe, die Herz und Lunge schädigen. '
            'Forscher haben ausgerechnet, wie viele Todesfälle auf eine bestimmte Strommenge kommen. Kernkraft liegt mit 0,03 Toten pro Terawattstunde '
            'auf der Höhe von Wind und Sonne. Die Unfälle von Tschernobyl und Fukushima sind dabei schon eingerechnet. Kohle liegt etwa 800-mal so hoch.</p>'
            '<p>Eine Terawattstunde ist ungefähr der Strom, den 150 000 Menschen in der EU in einem Jahr verbrauchen. Eine Stadt dieser Größe, '
            'die nur mit Kohlestrom versorgt wird, hätte also jedes Jahr etwa 25 vorzeitige Todesfälle. Mit Kernkraft wäre es rechnerisch einer in 33 Jahren.</p>'
            '<h3>Was der Ausstieg 2011 gekostet hat</h3>'
            '<p>Nach dem Unfall in Fukushima schaltete Deutschland 2011 acht Kernkraftwerke sofort ab. Eine Studie in einer der wichtigsten europäischen '
            'Wirtschaftszeitschriften hat stündliche Daten aller Kraftwerke ausgewertet. Ergebnis: Den fehlenden Atomstrom ersetzten vor allem Kohlekraftwerke '
            'und Stromimporte. Die zusätzliche Luftverschmutzung kostet nach dieser Studie jedes Jahr 3 bis 8 Milliarden Euro, vor allem durch vorzeitige Todesfälle.</p></div>'
            + quelle('IPCC, 5. Sachstandsbericht 2014 (CO₂ pro kWh, Mittelwerte); Our World in Data, „What are the safest and cleanest sources of energy?“ '
                     '(Todesfälle, Beispiel mit 150 000 Menschen); Jarvis, Deschenes, Jha: The Private and External Costs of Germany\'s Nuclear Phase-Out, '
                     'Journal of the European Economic Association 2022; EU-Taxonomie 2022.'))


def a2():
    ausl = [("Kernkraft", 90, "etwa 90 %"), ("Wind an Land", 20, "etwa 20 %"), ("Solar", 11, "etwa 11 %")]
    flaeche = [("Kernkraftwerk", 1, "etwa 1 km²"), ("Solarpark", 120, "etwa 120 km²"), ("Windpark", 200, "etwa 200 km²")]
    return (kopf_info("A", 2, "Versorgung und Fläche") + '<div class="lese">'
            '<h3>Viel Energie aus wenig Brennstoff</h3>'
            '<p>Im Reaktor werden Uran-235-Kerne gespalten. Die Wärme bringt Wasser zum Sieden, der Dampf treibt eine Turbine und einen Generator an. '
            'Kernspaltung setzt pro Kilogramm etwa eine Million Mal so viel Energie frei wie das Verbrennen von Kohle. Ein Brennstoff-Pellet von 6 g, '
            'so groß wie eine Fingerkuppe, liefert im Reaktor so viel Wärme wie etwa 700 kg Steinkohle. Ein Kohlekraftwerk braucht jeden Tag einen ganzen '
            'Güterzug Kohle, ein Kernkraftwerk tauscht nur etwa einmal im Jahr einen Teil seiner Brennelemente.</p>'
            '<h3>Strom bei jedem Wetter</h3>'
            '<p>Ein Kernkraftwerk läuft Tag und Nacht, im Sommer wie im Winter. In Deutschland liefen die Kraftwerke etwa 90 % der Zeit mit voller Leistung. '
            'Windräder an Land schaffen übers Jahr gerechnet nur etwa 20 %, Solaranlagen etwa 11 %, weil der Wind nicht immer weht und nachts keine Sonne scheint. '
            'Deshalb liefert ein großes Kraftwerk wie Isar 2 mit 1,4 Gigawatt im Jahr so viel Strom wie etwa 1000 moderne Windräder an Land.</p>'
            '<p>Besonders schwierig ist die Dunkelflaute: Im Winter weht manchmal tagelang kaum Wind, und die Sonne scheint nur wenige Stunden. '
            'Dann müssen andere Kraftwerke, Speicher oder Stromimporte einspringen. Ein Kernkraftwerk liefert in dieser Zeit weiter. '
            'Wer nur auf Wind und Sonne setzt, braucht für solche Wochen Speicher, Reservekraftwerke und dickere Leitungen. Das kostet zusätzlich.</p></div>'
            + dia(("Wie viel der möglichen Leistung im Jahr genutzt wird", balken(ausl, "Prozent der Zeit mit voller Leistung (übers Jahr)", GRUEN, ("Kernkraft",))),
                  ("Fläche für die gleiche Strommenge im Jahr", balken(flaeche, "Quadratkilometer (Windpark: ganze Fläche mit Abständen)", GRUEN, ("Kernkraftwerk",))))
            + '<div class="lese">'
            '<h3>Wenig Fläche</h3>'
            '<p>Ein Kernkraftwerk braucht mit seinem Gelände etwa 1 km². Ein Windpark mit gleicher Jahresmenge Strom verteilt sich auf etwa 200 km², '
            'das ist ungefähr die Fläche von Stuttgart. Zwischen den Windrädern kann man zwar weiter Felder bestellen, die Anlagen stehen aber in der Landschaft. '
            'Ein Solarpark mit gleicher Jahresmenge bräuchte etwa 120 km².</p>'
            '<h3>Wenig Abfall pro Strommenge</h3>'
            '<p>Für den Strom, den eine Familie in einem Jahr verbraucht (etwa 3500 kWh), entstehen etwa 7 g hochradioaktiver Abfall, verpackt knapp ein Schnapsglas voll. '
            'Mit Braunkohle entstünden für dieselbe Strommenge fast 4 Tonnen CO₂, die in die Luft gehen.</p></div>'
            + quelle('Fraunhofer ISE, Energy-Charts (Auslastung, Strommix); BASE und BGE (Abfallmengen); eigene Rechnung mit Isar 2 (1,4 GW) und 5-MW-Windrädern, '
                     'Herleitung im Vault „Kernkraft in Zahlen“; Umweltbundesamt (CO₂ der Braunkohle).'))


def a3():
    dosis = [("natürlich", 2.1, "2,1"), ("Medizin", 1.5, "1,5"), ("Flug New York", 0.1, "0,1"), ("Kernkraftwerk", 0.01, "unter 0,01")]
    return (kopf_info("A", 3, "Strahlung, Abfall und die Welt")
            + neben("Strahlenbelastung pro Jahr in Deutschland", balken(dosis, "Millisievert pro Jahr (Flug: hin und zurück)", GRUEN, ("Kernkraftwerk",)),
                    '<h3 style="margin-top:0">Im Normalbetrieb kaum Strahlung</h3>'
                    '<p>Strahlung ist überall: aus dem Boden, aus der Luft (Radon), aus dem Weltall und aus der Nahrung. In Deutschland bekommt jeder Mensch dadurch '
                    'im Schnitt etwa 2,1 Millisievert im Jahr ab. Dazu kommen Röntgen und CT beim Arzt, im Schnitt etwa 1,5 Millisievert.</p>')
            + '<div class="lese"><p>Wer in der Nähe eines Kernkraftwerks wohnt, bekommt dadurch laut Bundesamt für Strahlenschutz weniger als 0,01 Millisievert im Jahr. '
              'Das ist weniger als ein Zehntel eines Fluges nach New York und zurück.</p></div>'
            + '<div class="lese">'
            '<h3>Der Abfall ist klein und gut überwacht</h3>'
            '<p>In 60 Jahren hat Deutschland rund 5600 Terawattstunden Atomstrom erzeugt. Dabei sind rund 10 500 t abgebrannter Brennstoff entstanden, '
            'verpackt in Castor-Behältern rund 27 000 m³. Das passt in einen Würfel mit 30 m Kantenlänge. Der Abfall steht heute in bewachten Zwischenlagern. '
            'Die Betreiber haben 2017 rund 24 Milliarden Euro in einen staatlichen Fonds eingezahlt, aus dem Zwischen- und Endlagerung bezahlt werden. '
            'Den Rückbau der Kraftwerke bezahlen sie selbst. Die stark strahlenden Stoffe im Abfall, etwa Cäsium-137, sind nach etwa 300 Jahren fast zerfallen. '
            'Finnland hat bereits ein Endlager im Granit gebaut.</p>'
            '<h3>Andere Länder setzen weiter auf Kernkraft</h3>'
            '<p>Weltweit sind gut 400 Reaktoren in Betrieb. In der EU ist Kernkraft mit etwa 23 % die größte einzelne Stromquelle, Frankreich erzeugt etwa '
            'zwei Drittel seines Stroms damit. Je nach Zählweise sind weltweit 60 bis 80 Reaktoren im Bau, darunter in Ländern ohne Atomwaffen wie Polen, '
            'der Türkei und Ägypten. Über 30 Staaten haben seit 2023 erklärt, die Kernkraft bis 2050 verdreifachen zu wollen. Viele Länder verlängern außerdem die '
            'Laufzeit ihrer Kraftwerke auf 60 Jahre, in den USA teils auf 80 Jahre.</p>'
            '<h3>Deutschland: ein langer Streit</h3>'
            '<p>Im Jahr 2000 kam fast jede dritte Kilowattstunde in Deutschland aus Kernkraftwerken. Die rot-grüne Regierung beschloss 2002 mit den Konzernen den Ausstieg, '
            'die schwarz-gelbe Regierung verlängerte die Laufzeiten 2010 und beschloss nach Fukushima 2011 den schnellen Ausstieg. Die letzten drei Kraftwerke '
            'gingen am 15. April 2023 vom Netz, mitten in einer Energiekrise.</p></div>'
            + quelle('Bundesamt für Strahlenschutz (Strahlenbelastung); BASE und BGE (Abfallmengen, Zwischenlager); KENFO (Fonds); IAEA PRIS und World Nuclear Association '
                     '(Reaktoren weltweit); Fraunhofer ISE (Strommix); Erklärung zur Verdreifachung der Kernenergie, COP28 (2023); Bundeszentrale für politische Bildung.'))


# ================================================================ Gruppe B: Contra
def b1():
    menge = [("hochradioaktiv", 27000, "27 000 m³"), ("schwach, mittel", 303000, "303 000 m³")]
    return (kopf_info("B", 1, "Abfall und Endlager") + '<div class="lese">'
            '<h3>Eine Million Jahre sicher</h3>'
            '<p>Abgebrannte Brennelemente sind hochradioaktiv. Ein Mensch, der sich kurz nach der Entnahme ungeschützt daneben stellen würde, bekäme in kurzer Zeit '
            'eine tödliche Dosis. Ein Teil der Stoffe zerfällt schnell, andere sehr langsam: Cäsium-137 hat eine Halbwertszeit von 30 Jahren, '
            'Plutonium-239 von 24 000 Jahren, Iod-129 sogar von 16 Millionen Jahren. Das Gesetz verlangt deshalb ein Endlager, das den Abfall '
            'eine Million Jahre lang sicher von Menschen und Grundwasser trennt. Zum Vergleich: Die Pyramiden sind etwa 4500 Jahre alt, '
            'den modernen Menschen gibt es seit etwa 300 000 Jahren.</p></div>'
            + dia(("Wie lange strahlt der Abfall? Zeitachse in Jahren", zeitachse()))
            + '<div class="lese">'
            '<h3>Ein Endlager gibt es noch nicht</h3>'
            '<p>Seit 2017 wird in ganz Deutschland nach dem Standort mit der bestmöglichen Sicherheit gesucht, in Salz, Ton oder Granit, mehrere hundert Meter tief. '
            'Eigentlich sollte der Standort 2031 feststehen. Die zuständige Bundesgesellschaft für Endlagerung rechnet inzwischen mit einer Entscheidung '
            'zwischen 2046 und 2068. Bis dahin stehen rund 1900 Castor-Behälter in Zwischenlagern. Deren Genehmigungen gelten 40 Jahre und laufen ab den 2030er-Jahren aus.</p>'
            '</div>' + neben("Abfallmengen in Deutschland", balken(menge, "Kubikmeter, verpackt (schwach, mittel: Konrad)", ROT, ("hochradioaktiv",)),
            '<h3 style="margin-top:0">Was schiefgehen kann: die Asse</h3>'
            '<p>In das alte Salzbergwerk Asse in Niedersachsen wurden von 1967 bis 1978 rund 126 000 Fässer mit schwach und mittel radioaktivem Abfall gebracht. '
            'Seit Jahren dringt Wasser ein. Die Fässer sollen deshalb wieder herausgeholt werden, ein Vorhaben, das Jahrzehnte dauert und Milliarden kostet. '
            'Für schwach und mittel radioaktiven Abfall wird Schacht Konrad in Salzgitter umgebaut, die Arbeiten sollen bis 2029 fertig sein. Er ist für bis zu 303 000 m³ genehmigt.</p>')
            + '<div class="lese"><h3>Wer zahlt?</h3>'
            '<p>Die Betreiber haben 24 Milliarden Euro in einen Fonds eingezahlt. Reicht das Geld für Zwischen- und Endlagerung nicht, zahlt der Staat, also die Steuerzahler. '
            'Die Kosten trägt damit die Gesellschaft, und zwar noch viele Generationen lang, die selbst keinen Atomstrom genutzt haben.</p></div>'
            + quelle('BASE und BGE (Abfallmengen, Zeitplan der Endlagersuche, Asse, Konrad); Standortauswahlgesetz § 1; Karlsruher Nuklidkarte (Halbwertszeiten); KENFO.'))


def b2():
    flaeche = [("Sperrzone", 2600, "etwa 2600 km²"), ("Saarland", 2570, "2570 km²"), ("Stuttgart", 207, "207 km²")]
    return (kopf_info("B", 2, "Unfälle und Sicherheit") + neben("Sperrzone Tschernobyl im Vergleich", balken(flaeche, "Quadratkilometer", ROT, ("Sperrzone",)),
            '<h3 style="margin-top:0">Tschernobyl 1986</h3>'
            '<p>Am 26. April 1986 geriet in Tschernobyl in der heutigen Ukraine bei einem Test ein Reaktor außer Kontrolle. Er explodierte, der Graphit im Reaktor '
            'brannte tagelang, eine radioaktive Wolke zog über Europa bis nach Deutschland. Rund um das Kraftwerk wurde eine Sperrzone von etwa 2600 km² eingerichtet, '
            'so groß wie das Saarland. Sie gilt bis heute. Wie viele Menschen an den Spätfolgen sterben, ist umstritten: Die Weltgesundheitsorganisation schätzte '
            'bis zu 4000 Todesfälle, andere Studien kamen auf 16 000 bis 60 000.</p>')
            + '<div class="lese">'
            '<h3>Fukushima 2011</h3>'
            '<p>Im März 2011 traf ein Tsunami das Kraftwerk Fukushima in Japan. Die Notstromversorgung fiel aus, ohne Kühlung schmolzen drei Reaktorkerne. '
            'Der Unfall steht auf der höchsten Stufe 7 der internationalen Skala, wie Tschernobyl. Über 150 000 Menschen verließen ihre Heimat. '
            'Durch Strahlung ist ein Todesfall anerkannt, durch die Belastungen der Evakuierung starben nach Angaben Japans rund 2300 Menschen, vor allem ältere. '
            'Japan rechnet mit Kosten von mehr als 20 Billionen Yen, das sind weit über 100 Milliarden Euro. Der Rückbau der Reaktoren wird noch Jahrzehnte dauern. '
            'Fukushima geschah nicht in einem armen Land mit alter Technik, sondern in einem der modernsten Industrieländer der Welt.</p></div>'
            + '<div class="lese">'
            '<h3>Neue Gefahren: Krieg und Waffen</h3>'
            '<p>Seit März 2022 ist das größte Kernkraftwerk Europas, Saporischschja in der Ukraine, von russischen Truppen besetzt. Mehrmals fiel die Stromversorgung '
            'für die Kühlung aus, die Internationale Atomenergiebehörde warnt seitdem vor einem Unfall. Außerdem lässt sich die Technik zum Anreichern von Uran '
            'und das Plutonium aus Brennelementen auch für Atomwaffen nutzen. Deshalb überwacht die Internationale Atomenergiebehörde alle zivilen Anlagen weltweit.</p>'
            '<p>Schwere Unfälle sind selten. Wenn sie passieren, treffen sie aber ganze Regionen für Jahrzehnte. Diese Folgen lassen sich schwer in Zahlen pro '
            'Kilowattstunde ausdrücken.</p></div>'
            + quelle('Our World in Data, „Nuclear Energy“ (Opferzahlen Tschernobyl und Fukushima, nach WHO und der japanischen Wiederaufbaubehörde 2020); '
                     'IAEA (INES-Stufe, Saporischschja); Statistische Landesämter (Flächen Saarland, Stuttgart).'))


def b3():
    anteil = [("1996", 17.5, "17,5 %"), ("2025", 8.8, "8,8 %")]
    return (kopf_info("B", 3, "Kosten, Zeit und Abhängigkeit") + '<div class="lese">'
            '<h3>Neue Kraftwerke werden viel teurer als geplant</h3>'
            '<p>In Europa wurden in den letzten Jahren zwei neue große Reaktoren fertig. Flamanville 3 in Frankreich sollte 3,3 Milliarden Euro kosten, '
            'der französische Rechnungshof kommt auf 23,7 Milliarden, also etwa das Siebenfache. Das Kraftwerk ging 12 Jahre zu spät ans Netz. '
            'Olkiluoto 3 in Finnland brauchte 18 statt 4 Jahre Bauzeit und kostete etwa 11 statt 3 Milliarden Euro. Weltweit dauert der Bau eines Reaktors '
            'im Schnitt etwa 10 Jahre. In Großbritannien wird Hinkley Point C gebaut, auch dort sind die Kosten weit über die Planung gestiegen.</p>'
            '<p>Kleine modulare Reaktoren (SMR) sollen günstiger werden, weil man sie in Serie in Fabriken baut. Im Westen ist aber noch keiner im kommerziellen '
            'Betrieb, der erste in Kanada soll um 2030 Strom liefern. Ob sie wirklich günstiger sind, weiß man erst dann.</p></div>'
            + dia(("Kosten neuer Reaktoren in Europa", kosten()),
                  ("Anteil der Kernkraft am Strom der Welt", balken(anteil, "Prozent des weltweit erzeugten Stroms", ROT, ("2025",))))
            + '<div class="lese">'
            '<h3>Die Welt baut vor allem Wind und Sonne</h3>'
            '<p>Der Anteil der Kernkraft am Strom der Welt hat sich seit 1996 etwa halbiert, von 17,5 % auf unter 9 %. Die Strommenge aus Kernkraft ist ungefähr '
            'gleich geblieben, Wind und Sonne sind viel schneller gewachsen. Selbst China, das die meisten Reaktoren baut, erzeugt mit Wind und Sonne etwa fünfmal '
            'so viel Strom wie mit Kernkraft. In Deutschland sagte der Betreiber von Isar 2 schon 2023, ein Neustart sei für ihn „vom Tisch“: Das Personal ist weg, '
            'der Rückbau läuft.</p>'
            '<h3>Abhängig vom Brennstoff</h3>'
            '<p>Uran gibt es in Deutschland nicht im Abbau. Weltweit stammt etwa 40 % aus Kasachstan, weiteres aus Kanada, Namibia und Australien. '
            'Einen großen Teil der weltweiten Anreicherung hat Russland. Wind- und Solaranlagen kauft man einmal, danach brauchen sie keinen Brennstoff mehr. '
            'Ein Kernkraftwerk braucht immer wieder neue Brennelemente.</p>'
            '<h3>Kühlwasser in heißen Sommern</h3>'
            '<p>Kraftwerke an Flüssen brauchen viel Kühlwasser. Im heißen, trockenen Sommer 2022 durften in Frankreich mehrere Reaktoren nur gedrosselt laufen, '
            'weil die Flüsse zu warm und zu niedrig waren. Zusammen mit Reparaturen an vielen Reaktoren führte das dazu, dass Frankreich 2022 erstmals seit Jahrzehnten '
            'mehr Strom einführen musste, als es ausführte, auch aus Deutschland. Mit dem Klimawandel werden solche Sommer häufiger.</p></div>'
            + quelle('Cour des comptes 2025 (Flamanville 3); TVO und Medienberichte (Olkiluoto 3); World Nuclear Industry Status Report 2026 (Weltanteil, Bauzeiten, China); '
                     'World Nuclear Association (Uran, Anreicherung); RTE, französischer Netzbetreiber (Stromaustausch 2022); PreussenElektra, Oktober 2023.'))


# ================================================================ Aufgabenblatt (Seite 4)
ROLLEN = ["Infoblatt 1 lesen und berichten", "Infoblatt 2 lesen und berichten", "Infoblatt 3 lesen und berichten",
          "Zeitwächter (achtet auf die Zeit)", "Schreiber (füllt dieses Blatt aus)"]


def aufgabenblatt(gruppe, l):
    pro = gruppe == "A"
    titel = "Argumente für Kernkraft" if pro else "Argumente gegen Kernkraft"
    g = '<span class="gruppe ga">Gruppe A Pro</span>' if pro else '<span class="gruppe gb">Gruppe B Contra</span>'
    rollen = ('<table class="fm"><tr><th style="width:70mm">Aufgabe</th><th>Name</th></tr>'
              + "".join(f'<tr><td class="v" style="width:70mm">{r}</td><td></td></tr>' for r in ROLLEN) + "</table>")
    blaetter = (["Klima und Gesundheit", "Versorgung und Fläche", "Strahlung, Abfall und die Welt"] if pro
                else ["Abfall und Endlager", "Unfälle und Sicherheit", "Kosten, Zeit und Abhängigkeit"])
    loes_doku = ([("CO₂-arm, viel sicherer als Kohle", "12 g CO₂ pro kWh; 0,03 Tote pro TWh", "Fakt"),
                  ("liefert bei jedem Wetter, braucht wenig Fläche", "90 % Auslastung; 1 km² statt 200 km²", "Fakt"),
                  ("kaum Strahlung im Normalbetrieb", "unter 0,01 mSv statt 2,1 mSv natürlich", "Fakt")] if pro else
                 [("Abfall muss extrem lange sicher lagern", "1 Mio. Jahre; Endlager erst 2046 bis 2068", "Fakt"),
                  ("Unfälle machen Regionen unbewohnbar", "Sperrzone 2600 km²; 150 000 Evakuierte", "Fakt"),
                  ("neue Kraftwerke zu teuer und zu langsam", "Flamanville 23,7 statt 3,3 Mrd. €", "Fakt")])
    doku = ('<table class="fm doku"><tr><th style="width:42mm">Infoblatt</th><th>Stärkstes Argument</th><th style="width:44mm">Zahl dazu</th><th style="width:22mm">Fakt oder Meinung?</th></tr>'
            + "".join(f'<tr><td class="v" style="width:42mm">{i + 1} {b}</td>'
                      + (f'<td class="l">{a}</td><td class="l">{z}</td><td class="l">{f}</td>' if l else "<td></td><td></td><td></td>") + "</tr>"
                      for i, (b, (a, z, f)) in enumerate(zip(blaetter, loes_doku))) + "</table>")
    if pro:
        dfragen = [("Infoblatt 1: Wie viel mal so viel CO₂ pro kWh verursacht Kohle wie Kernkraft?", "820 : 12 ≈ 70, also etwa 70-mal so viel."),
                   ("Infoblatt 2: Wie viel mal so viel Fläche braucht ein Windpark mit gleicher Jahresstrommenge?", "200 : 1 = 200-mal so viel."),
                   ("Infoblatt 3: Wie viel mal so hoch ist die natürliche Strahlung wie die durch ein Kernkraftwerk?", "2,1 : 0,01 = 210, also über 200-mal so hoch.")]
        gegen = ("Welches Argument der Contra-Seite ist für euch am schwersten zu entkräften? Begründet.",
                 "Zum Beispiel das Endlager: Eine Million Jahre lässt sich mit keiner Erfahrung belegen, und in Deutschland gibt es noch keinen Standort.")
        zugeben = "Zum Beispiel: Schwere Unfälle sind selten, aber ihre Folgen treffen ganze Regionen. Neue Kraftwerke sind zuletzt sehr teuer geworden."
    else:
        dfragen = [("Infoblatt 1: Cäsium-137 hat 30 Jahre Halbwertszeit. Welcher Anteil ist nach 300 Jahren noch da?", "10 Halbwertszeiten: (1/2)¹⁰ = 1/1024, etwa ein Tausendstel."),
                   ("Infoblatt 2: Wie viel mal so groß wie Stuttgart ist die Sperrzone von Tschernobyl?", "2600 : 207 ≈ 13, also etwa 13-mal so groß."),
                   ("Infoblatt 3: Um welchen Faktor wurde Flamanville 3 teurer als geplant?", "23,7 : 3,3 ≈ 7, also etwa siebenmal so teuer.")]
        gegen = ("Welches Argument der Pro-Seite ist für euch am schwersten zu entkräften? Begründet.",
                 "Zum Beispiel das CO₂: Kernkraft liegt so niedrig wie Wind. Nach 2011 ersetzte vor allem Kohle den Atomstrom, das kostete Gesundheit und Klima.")
        zugeben = "Zum Beispiel: Pro erzeugter Strommenge sterben bei Kernkraft viel weniger Menschen als bei Kohle, und im Betrieb entsteht kaum CO₂."
    df = "".join(f'<p class="frage" style="margin:1mm 0 0">{q}</p>' + antwort(a, l, 1) for q, a in dfragen)
    return (('<div class="loes">' if l else '<div>')
            + f'<div class="kopf"><div>{g}<h1>Aufgabenblatt: {titel}</h1></div>' + ('<div class="loesung-marker">Lösung</div>' if l else "") + '</div>'
            + '<div class="ablauf"><b>So arbeitet ihr (25 Minuten):</b><ol>'
              '<li>Tragt ein, wer was macht. Seid ihr nur vier, ist ein Leser auch Zeitwächter.</li>'
              '<li>8 Minuten: Jeder liest sein Infoblatt und markiert das stärkste Argument mit einer Zahl.</li>'
              '<li>10 Minuten: Der Reihe nach berichtet jeder in zwei Minuten. Der Schreiber füllt Aufgabe 1 aus.</li>'
              '<li>7 Minuten: Aufgaben 2 bis 4 gemeinsam. Danach geht ihr in die Diskussion mit der anderen Gruppe.</li></ol></div>'
            + rollen + LEGENDE
            + aufg(1, 0, "Unsere drei stärksten Argumente. Achtet darauf: Ein Fakt lässt sich nachprüfen, eine Meinung bewertet.") + doku
            + aufg(2, 1, "Lest im Diagramm ab und rechnet.") + df
            + aufg(3, 2, "Gegencheck: " + gegen[0]) + antwort(gegen[1], l, 2)
            + aufg(4, 1, "Für die Diskussion: Was gebt ihr der anderen Seite zu? Ein ehrliches Zugeständnis macht eure Position glaubwürdiger.")
            + antwort(zugeben, l, 2) + '</div>')


if __name__ == "__main__":
    for gruppe, seiten, name in (("A", [a1, a2, a3], "Pro"), ("B", [b1, b2, b3], "Contra")):
        html, pdf = f"lesetexte_kernkraft_{name.lower()}_w21.html", f"Lesetexte Kernkraft {name} W21.pdf"
        doc = dokument(f"Kernkraft {name} – W21", [f() for f in seiten] + [aufgabenblatt(gruppe, False), aufgabenblatt(gruppe, True)])
        (HIER / html).write_text(doc.replace("</head>", LESE_CSS + "</head>", 1), encoding="utf-8")
        drucke(html, pdf)
