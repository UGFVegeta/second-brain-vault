"""Blätter Klasse 7 und 8. Bausteine aus baue_blaetter.py und stufe56.py."""
from baue_blaetter import abschnitt, aufgabe, gap, linien, richtig_falsch
from stufe56 import (P, blatt as _blatt, felder, kacheln, karo, lueckentext, reihenfolge, sortieren,
                     wortkasten, zuordnen)

STUFE = "Klasse 7 und 8"


def blatt(*a):
    return _blatt(*a, stufe=STUFE)


def tabelle(kopf, zeilen):
    k = "".join(f"<th>{x}</th>" for x in kopf)
    z = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in zeilen)
    return f'<table class="info"><tr>{k}</tr>{z}</table>'


def frage(L, text, n, loes):
    return f'<p style="margin:1.2mm 0 .3mm 0">{text}</p>' + linien(L, n, loes)


# ------------------------------------------------------------------ Grafiken
SVG = 'xmlns="http://www.w3.org/2000/svg" font-family="Open Sans, Helvetica, sans-serif" font-size="11" font-weight="600"'


def basketballfeld(beschriftet=True):
    k, m = 12, 20  # 28 x 15 m
    W, H = 28 * k, 15 * k
    yc = m + H / 2
    x0, x1 = m, m + W
    korb = 1.575 * k
    zone_l, zone_b = 5.8 * k, 4.9 * k
    r3 = 6.75 * k
    o = [f'<svg viewBox="0 0 {W+2*m} {H+2*m}" width="100%" {SVG}>',
         f'<defs><clipPath id="bf"><rect x="{x0}" y="{m}" width="{W}" height="{H}"/></clipPath></defs>',
         f'<rect x="{x0}" y="{m}" width="{W}" height="{H}" fill="#e9b97a" stroke="#fff" stroke-width="2.5"/>',
         f'<line x1="{m+W/2}" y1="{m}" x2="{m+W/2}" y2="{m+H}" stroke="#fff" stroke-width="2"/>',
         f'<circle cx="{m+W/2}" cy="{yc}" r="{1.8*k}" fill="none" stroke="#fff" stroke-width="2"/>',
         '<g clip-path="url(#bf)">']
    for x, s in ((x0, 1), (x1, -1)):
        o.append(f'<rect x="{min(x, x+s*zone_l)}" y="{yc-zone_b/2}" width="{zone_l}" height="{zone_b}" fill="#d98d4f" stroke="#fff" stroke-width="2"/>')
        o.append(f'<circle cx="{x+s*zone_l}" cy="{yc}" r="{1.8*k}" fill="none" stroke="#fff" stroke-width="2"/>')
        o.append(f'<circle cx="{x+s*korb}" cy="{yc}" r="{3}" fill="none" stroke="#c0392b" stroke-width="2.5"/>')
        o.append(f'<path d="M{x} {yc-r3} L{x+s*korb} {yc-r3} A{r3} {r3} 0 0 {1 if s==1 else 0} {x+s*korb} {yc+r3} L{x} {yc+r3}" fill="none" stroke="#fff" stroke-width="2"/>')
    o.append('</g>')
    if beschriftet:
        o += [f'<text x="{x0+3}" y="{yc-zone_b/2-4}" fill="#222">Zone</text>',
              f'<text x="{x0+zone_l+1.9*k}" y="{yc+4}" fill="#222">Freiwurflinie</text>',
              f'<text x="{x0+5*k}" y="{m+14}" fill="#222">Dreipunktelinie</text>',
              f'<text x="{m+W/2+4}" y="{m+H-6}" fill="#222">Mittellinie</text>',
              f'<text x="{x0+korb+5}" y="{yc+18}" fill="#c0392b">Korb</text>',
              f'<text x="{m+W/2}" y="{m+H+15}" text-anchor="middle" fill="#333">28 m lang, 15 m breit</text>']
    else:
        for b, x, y in (("A", x0 + zone_l / 2, yc - zone_b / 2 + 14), ("B", x0 + zone_l, yc - 1.8 * k - 2),
                        ("C", x0 + 6 * k, m + 14), ("D", m + W / 2, m + 16), ("E", x0 + korb, yc + 16)):
            o.append(f'<circle cx="{x}" cy="{y-4}" r="8" fill="#fff" stroke="#333"/><text x="{x}" y="{y}" text-anchor="middle">{b}</text>')
    o.append("</svg>")
    return "".join(o)


def badmintonfeld():
    k, m = 22, 16  # 13,40 x 6,10 m
    W, H = 13.4 * k, 6.1 * k
    x0, y0 = m, m
    xn = x0 + W / 2
    o = [f'<svg viewBox="0 0 {W+2*m+120} {H+2*m}" width="100%" {SVG}>',
         f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" fill="#7cc47a" stroke="#fff" stroke-width="2.5"/>']
    for y in (y0 + 0.46 * k, y0 + H - 0.46 * k):
        o.append(f'<line x1="{x0}" y1="{y}" x2="{x0+W}" y2="{y}" stroke="#fff" stroke-width="1.8"/>')
    for x in (xn - 1.98 * k, xn + 1.98 * k, x0 + 0.76 * k, x0 + W - 0.76 * k):
        o.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0+H}" stroke="#fff" stroke-width="1.8"/>')
    o.append(f'<line x1="{x0}" y1="{y0+H/2}" x2="{xn-1.98*k}" y2="{y0+H/2}" stroke="#fff" stroke-width="1.8"/>')
    o.append(f'<line x1="{xn+1.98*k}" y1="{y0+H/2}" x2="{x0+W}" y2="{y0+H/2}" stroke="#fff" stroke-width="1.8"/>')
    o.append(f'<line x1="{xn}" y1="{y0-6}" x2="{xn}" y2="{y0+H+6}" stroke="#333" stroke-width="3.5" stroke-dasharray="3 2"/>')
    o.append(f'<text x="{xn}" y="{y0-4}" text-anchor="middle" fill="#222">Netz</text>')
    tx = x0 + W + 10
    o += [f'<text x="{tx}" y="{y0+12}" fill="#222">Doppel: ganzes Feld</text>',
          f'<text x="{tx}" y="{y0+30}" fill="#222">Einzel: ohne die</text>',
          f'<text x="{tx}" y="{y0+44}" fill="#222">schmalen Seitenstreifen</text>',
          f'<text x="{tx}" y="{y0+70}" fill="#222">vordere</text>',
          f'<text x="{tx}" y="{y0+84}" fill="#222">Aufschlaglinie:</text>',
          f'<text x="{tx}" y="{y0+98}" fill="#222">1,98 m vom Netz</text>',
          f'<text x="{x0+W/2}" y="{y0+H+14}" text-anchor="middle" fill="#333">13,40 m lang, 6,10 m breit</text>']
    o.append("</svg>")
    return "".join(o)


def abseits():
    """Angreifer A ist im Abseits: näher am Tor als der vorletzte Verteidiger."""
    o = [f'<svg viewBox="0 0 360 150" width="100%" {SVG}>',
         '<rect x="10" y="10" width="340" height="130" fill="#7cc47a" stroke="#fff" stroke-width="2"/>',
         '<rect x="340" y="55" width="10" height="40" fill="#fff" stroke="#333"/>',
         '<line x1="250" y1="10" x2="250" y2="140" stroke="#c0392b" stroke-width="1.8" stroke-dasharray="6 4"/>',
         '<text x="246" y="24" text-anchor="end" fill="#c0392b">Abseitslinie</text>']
    for x, y in ((250, 105), (330, 75)):
        o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#e8706a" stroke="#333"/>')
    o.append('<text x="330" y="100" text-anchor="middle" fill="#222">TW</text>')
    o.append('<text x="250" y="128" text-anchor="middle" fill="#222">Verteidiger</text>')
    for x, y, t in ((120, 60, "B"), (290, 55, "A")):
        o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#1f6fb2" stroke="#333"/>'
                 f'<text x="{x}" y="{y-12}" text-anchor="middle" fill="#1f6fb2">{t}</text>')
    o.append('<path d="M128 62 L278 56" stroke="#333" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#pf)"/>')
    o.append('<defs><marker id="pf" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
             '<path d="M0 0 L6 3 L0 6 Z" fill="#333"/></marker></defs>')
    o.append('<text x="190" y="50" text-anchor="middle" fill="#333">Pass</text>')
    o.append("</svg>")
    return "".join(o)


# ================================================================== Essen und Trinken
ET = "Essen und Trinken"


def et1(L):
    v = abschnitt("A", "Energie aus der Nahrung")
    v += P("Alles, was dein Körper tut, kostet Energie: Atmen, Denken, Verdauen und natürlich Sport. "
           "Diese Energie bekommt er aus den drei Hauptnährstoffen. Man misst sie in Kilokalorien (kcal).")
    v += tabelle(["Nährstoff", "Energie pro Gramm", "Aufgabe", "steckt z. B. in"],
                 [["Kohlenhydrate", "4 kcal", "schnelle Energie, Treibstoff für Muskeln und Gehirn", "Brot, Nudeln, Reis, Kartoffeln, Obst"],
                  ["Eiweiß (Protein)", "4 kcal", "Baustoff für Muskeln, Haut, Haare, Abwehrkräfte", "Milch, Käse, Fleisch, Fisch, Eier, Hülsenfrüchte"],
                  ["Fett", "9 kcal", "Energiespeicher, Wärmeschutz, Aufnahme mancher Vitamine", "Öl, Butter, Nüsse, Wurst, Käse"]])
    v += P("Fett liefert also mehr als doppelt so viel Energie wie die anderen beiden. "
           "Vitamine, Mineralstoffe und Wasser liefern keine Energie, sind aber trotzdem lebenswichtig.")
    v += abschnitt("B", "Wie viel Energie brauchst du?")
    v += P("Der <b>Grundumsatz</b> ist die Energie, die dein Körper in völliger Ruhe braucht, etwa für Herzschlag, Atmung und Körperwärme. "
           "Als Faustregel gilt: ungefähr 1 kcal pro Kilogramm Körpergewicht und Stunde. "
           "Dazu kommt der <b>Leistungsumsatz</b> für alles, was du tust. Beides zusammen ist der Gesamtumsatz.")
    v += P("Jugendliche in deinem Alter brauchen am Tag etwa 2000 bis 2800 kcal, je nach Größe, Geschlecht und Bewegung. "
           "Wer viel Sport macht, braucht mehr.")
    v += tabelle(["Tätigkeit (30 Minuten, 50 kg)", "Verbrauch, etwa"],
                 [["Sitzen, Lesen", "40 kcal"], ["Rad fahren, gemütlich", "100 kcal"],
                  ["Fußball spielen", "180 kcal"], ["Joggen", "200 kcal"]])
    v += abschnitt("C", "Die Energiebilanz")
    v += P("Isst du so viel Energie, wie du verbrauchst, bleibt dein Gewicht gleich. Isst du dauerhaft mehr, speichert der Körper den Rest als Fett. "
           "Isst du weniger, nimmt er Energie aus den Speichern. In der Wachstumsphase braucht der Körper ausreichend Energie, "
           "deshalb sind Diäten für Jugendliche keine gute Idee.")

    v += abschnitt("D", "Energie im Alltag")
    v += P("Nicht nur Sport verbraucht Energie. Wer mit dem Rad zur Schule fährt, Treppen statt Aufzug nimmt und in der Pause herumläuft, "
           "verbraucht über den Tag deutlich mehr als jemand, der fast nur sitzt. Kleine Bewegungen summieren sich.")
    a = [
        aufgabe(1, 0, "Ergänze die Tabelle.", felder(L, [("1 g Kohlenhydrate", "4 kcal"), ("1 g Eiweiß", "4 kcal"),
                                                         ("1 g Fett", "9 kcal"), ("1 g Vitamine", "0 kcal")], 4, 30)),
        aufgabe(2, 1, "Ein Müsliriegel enthält 15 g Kohlenhydrate, 2 g Eiweiß und 5 g Fett. Wie viel Energie liefert er?",
                linien(L, 2, "15 · 4 + 2 · 4 + 5 · 9 = 60 + 8 + 45 = 113 kcal")),
        aufgabe(3, 1, "Schätze deinen Grundumsatz an einem Tag mit der Faustregel. Nimm dein Gewicht oder 50 kg.",
                linien(L, 1, "50 kg · 1 kcal · 24 h = 1200 kcal")),
        aufgabe(4, 1, "Wie lange muss ein 50 kg schwerer Jugendlicher joggen, um die Energie eines Schokoriegels (250 kcal) zu verbrauchen?",
                linien(L, 2, "30 min Joggen = 200 kcal, 250 kcal also etwa 37 bis 38 Minuten.")),
        aufgabe(5, 2, "Erkläre mit dem Wort Energiebilanz, warum jemand zunimmt, obwohl er gesund isst.",
                linien(L, 3, "Er nimmt mit dem Essen mehr Energie auf, als er verbraucht. Auch gesundes Essen hat Energie, "
                             "der Überschuss wird als Fett gespeichert. Mehr Bewegung oder kleinere Portionen gleichen das aus.")),
        aufgabe(6, 0, "Was liefert keine Energie, ist aber lebenswichtig? Nenne drei Dinge.",
                felder(L, [("1", "Vitamine"), ("2", "Mineralstoffe"), ("3", "Wasser")], 3, 40)),
        aufgabe(7, 1, "Vergleiche den Verbrauch von 30 Minuten Fußball und 30 Minuten Sitzen (50 kg). Was folgt daraus für deinen Alltag?",
                linien(L, 3, "Fußball 180 kcal, Sitzen 40 kcal, also 140 kcal mehr. Wer sich im Alltag viel bewegt, verbraucht deutlich mehr Energie.")),
        aufgabe(8, 2, "Schreibe drei Ideen auf, wie du im Alltag mehr Energie verbrauchen kannst, ohne extra Sport zu machen.",
                linien(L, 3, "Mit dem Rad zur Schule statt mit dem Bus, Treppen statt Aufzug, in der Pause bewegen statt sitzen.")),
        aufgabe(9, 1, "Erkläre den Unterschied zwischen Grundumsatz und Leistungsumsatz mit je einem Beispiel.",
                linien(L, 3, "Grundumsatz: Energie in völliger Ruhe, z. B. für Herzschlag und Atmung im Schlaf. "
                             "Leistungsumsatz: Energie für alles, was man tut, z. B. Radfahren oder Fußball.")),
    ]
    return blatt(ET, 1, "Energie und Energiebedarf", v,
                 ["Kohlenhydrate und Eiweiß: 4 kcal pro g, Fett: 9 kcal pro g.",
                  "Gesamtumsatz = Grundumsatz + Leistungsumsatz.",
                  "Energiebilanz: Aufnahme und Verbrauch im Gleichgewicht."], a)


def et2(L):
    v = abschnitt("A", "Die Nährwerttabelle")
    v += P("Auf fast jeder Verpackung steht eine Nährwerttabelle. Sie zeigt, wie viel Energie, Fett, Zucker, Eiweiß und Salz "
           "in <b>100 g</b> oder <b>100 ml</b> stecken. So kann man verschiedene Produkte gut vergleichen. "
           "Manchmal ist zusätzlich eine Portion angegeben, die aber oft sehr klein gewählt ist.")
    v += tabelle(["Nährwerte pro 100 g", "Schoko-Müsli", "Haferflocken"],
                 [["Energie", "430 kcal", "370 kcal"], ["Fett", "14 g", "7 g"], ["davon gesättigte Fettsäuren", "5 g", "1,3 g"],
                  ["Kohlenhydrate", "66 g", "59 g"], ["davon Zucker", "24 g", "1 g"], ["Ballaststoffe", "6 g", "10 g"],
                  ["Eiweiß", "8 g", "13 g"], ["Salz", "0,4 g", "0,02 g"]])
    v += P("<i>Werte als Beispiel, gerundet.</i> Bei „davon Zucker“ steht, wie viel von den Kohlenhydraten Zucker ist. "
           "Ballaststoffe sättigen lange und sind gut für die Verdauung.")
    v += abschnitt("B", "Der Nutri-Score")
    v += P("Viele Produkte tragen den Nutri-Score: eine Skala von <b>A</b> (dunkelgrün, eher günstig) bis <b>E</b> (rot, eher ungünstig). "
           "Er verrechnet Ungünstiges wie Zucker, gesättigte Fettsäuren, Salz und viel Energie mit Günstigem wie Ballaststoffen, "
           "Eiweiß, Obst und Gemüse. Vergleichen sollte man nur Produkte derselben Art, also Müsli mit Müsli.")
    v += abschnitt("C", "Fast Food und versteckter Zucker")
    v += P("Fast Food ist praktisch und schmeckt vielen. Es enthält aber oft viel Fett, Salz und Energie und wenig Ballaststoffe und Vitamine. "
           "Ab und zu ist das kein Problem, als tägliches Essen schon. Zucker versteckt sich auch in Lebensmitteln, "
           "bei denen man es nicht erwartet: Ketchup, Fruchtjoghurt, Eistee, Fertigsoßen. Die Weltgesundheitsorganisation rät, "
           "möglichst wenig zugesetzten Zucker zu essen. Ein Stück Würfelzucker wiegt etwa 3 g.")

    v += abschnitt("D", "Werbung auf der Packung")
    v += P("Auf der Vorderseite stehen oft Aussagen wie „mit Vollkorn“, „reich an Vitaminen“ oder „ohne Zuckerzusatz“. "
           "Sie klingen gesund, sagen aber wenig. „Ohne Zuckerzusatz“ heißt nur, dass kein Zucker zugegeben wurde. Ein Fruchtsaft kann trotzdem "
           "viel Zucker aus den Früchten enthalten. Die ehrliche Information steht hinten in der Nährwerttabelle.")
    a = [
        aufgabe(1, 0, "Lies aus der Tabelle ab.", felder(L, [("Zucker im Schoko-Müsli (100 g)", "24 g"), ("Zucker in Haferflocken (100 g)", "1 g"),
                                                            ("Eiweiß in Haferflocken (100 g)", "13 g")], 3, 44)),
        aufgabe(2, 1, "Eine Schale enthält 60 g Schoko-Müsli. Wie viel Zucker ist das? Wie viele Würfelzucker?",
                linien(L, 2, "24 g · 0,6 = 14,4 g Zucker, das sind knapp 5 Stück Würfelzucker (14,4 : 3 = 4,8).")),
        aufgabe(3, 1, "Welches der beiden Produkte würdest du vor dem Sport zum Frühstück wählen? Begründe mit drei Werten.",
                linien(L, 3, "Haferflocken: viel weniger Zucker (1 g statt 24 g), mehr Eiweiß (13 g statt 8 g) und mehr Ballaststoffe (10 g statt 6 g). "
                             "Sie sättigen länger.")),
        aufgabe(4, 2, "Ein Freund sagt: „Fast Food ist ungesund, also darf ich es nie essen.“ Nimm Stellung.",
                linien(L, 3, "Ab und zu ist Fast Food kein Problem. Es kommt auf die Menge und die Häufigkeit an. "
                             "Ungünstig ist es, wenn es regelmäßig andere Mahlzeiten ersetzt, weil es viel Fett, Salz und Energie hat.")),
        aufgabe(5, 1, "Wie viel Energie haben 40 g Haferflocken? Und 40 g Schoko-Müsli?",
                linien(L, 1, "Haferflocken: 370 · 0,4 = 148 kcal. Schoko-Müsli: 430 · 0,4 = 172 kcal.")),
        aufgabe(6, 1, "Warum sollte man Nährwerte immer pro 100 g vergleichen und nicht pro Portion?",
                linien(L, 3, "Die Portionen sind bei jedem Hersteller anders groß und oft sehr klein gewählt. Nur pro 100 g kann man ehrlich vergleichen.")),
        aufgabe(7, 2, "Auf einem Orangensaft steht „ohne Zuckerzusatz“. Ist er deshalb zuckerarm? Begründe.",
                linien(L, 3, "Nein. Es wurde nur kein Zucker zugegeben. Der Saft enthält trotzdem viel Fruchtzucker, etwa so viel wie Limo.")),
        aufgabe(8, 2, "Worauf achtest du künftig beim Einkaufen von Frühstücksprodukten? Nenne drei Punkte und begründe sie.",
                linien(L, 4, "Zucker pro 100 g vergleichen, weil Zucker oft versteckt ist. Viele Ballaststoffe, weil sie lange satt machen. "
                             "Nicht auf Werbung vorne achten, sondern auf die Nährwerttabelle hinten.")),
    ]
    return blatt(ET, 2, "Nährwerte lesen", v,
                 ["Nährwerte immer pro 100 g vergleichen.",
                  "Nutri-Score A ist eher günstig, E eher ungünstig.",
                  "Zucker versteckt sich auch in Ketchup, Joghurt und Eistee."], a)


def et3(L):
    v = abschnitt("A", "Wasserverlust beim Sport")
    v += P("Beim Sport produzieren die Muskeln Wärme. Der Körper kühlt sich, indem er schwitzt. "
           "Bei einer intensiven Doppelstunde kann ein Jugendlicher einen halben bis einen Liter Schweiß verlieren, bei Hitze noch mehr. "
           "Schon wenn man etwa 2 % seines Körpergewichts an Wasser verloren hat, lassen Ausdauer, Kraft und Konzentration spürbar nach.")
    v += P("Wie viel du verloren hast, kannst du mit einer Waage herausfinden: vor und nach dem Sport wiegen. "
           "Jedes Kilogramm weniger entspricht ungefähr einem Liter verlorener Flüssigkeit.")
    v += abschnitt("B", "Richtig trinken")
    v += P("<b>Vorher:</b> In den Stunden vor dem Sport regelmäßig trinken, etwa ein Glas eine halbe Stunde vorher.<br>"
           "<b>Während:</b> In Pausen einige Schlucke, besonders bei langer Belastung oder Hitze.<br>"
           "<b>Danach:</b> Den Verlust wieder ausgleichen, ruhig etwas mehr trinken, als man verloren hat.")
    v += abschnitt("C", "Sportgetränke im Vergleich")
    v += tabelle(["Getränk", "Bewertung für den Schulsport"],
                 [["Leitungswasser, Mineralwasser", "ideal, für Schulsport völlig ausreichend"],
                  ["Saftschorle (1 Teil Saft, 2 bis 3 Teile Wasser)", "gut bei langen Belastungen, liefert etwas Energie und Mineralstoffe"],
                  ["Isotonische Sportgetränke", "für Leistungssportler bei langen Wettkämpfen, im Schulsport unnötig und teuer"],
                  ["Limo, Cola, Eistee", "viel Zucker, löschen den Durst schlecht"],
                  ["Energydrinks", "viel Zucker und Koffein, Herzrasen möglich, für Jugendliche nicht geeignet"]])
    v += P("„Isotonisch“ bedeutet, dass das Getränk ähnlich viele gelöste Teilchen enthält wie das Blut. "
           "Eine stark verdünnte Saftschorle kommt dem schon nahe und kostet nur einen Bruchteil.")

    v += abschnitt("D", "Sport bei Hitze")
    v += P("An heißen Tagen, etwa bei den Bundesjugendspielen, verliert man viel mehr Flüssigkeit. Dann vorher schon mehr trinken, "
           "in jeder Pause etwas trinken, Kopfbedeckung tragen und sich in den Schatten setzen. Kopfschmerzen, Schwindel und Übelkeit sind Warnzeichen: "
           "sofort aufhören, in den Schatten, kühlen, trinken und der Lehrkraft Bescheid sagen.")
    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Der Körper kühlt sich durch {}. Ab etwa {} Wasserverlust sinkt die Leistung. "
                "1 kg Gewichtsverlust beim Sport entspricht etwa {} Flüssigkeit. Eine gute Schorle mischt man im Verhältnis 1 zu {}.",
                ["Schwitzen", "2 %", "1 Liter", "2 bis 3"], ["1 Liter", "2 bis 3", "Schwitzen", "2 %"], 26)),
        aufgabe(2, 0, "Ordne die Getränke ein.", sortieren(L, {
            "ideal": ["Leitungswasser", "Mineralwasser"], "gut bei langen Belastungen": ["Apfelschorle 1:3"],
            "ungeeignet": ["Cola", "Energydrink", "Eistee"]},
            ["Cola", "Leitungswasser", "Energydrink", "Apfelschorle 1:3", "Mineralwasser", "Eistee"], 20)),
        aufgabe(3, 1, "Ein Schüler wiegt vor dem Training 52,4 kg, danach 51,7 kg. Wie viel Flüssigkeit hat er verloren? "
                      "Wie viel Prozent seines Körpergewichts sind das?",
                linien(L, 2, "52,4 − 51,7 = 0,7 kg, also etwa 0,7 Liter. 0,7 : 52,4 · 100 ≈ 1,3 %")),
        aufgabe(4, 1, "Ab wie vielen Kilogramm Verlust würde bei ihm die Leistung deutlich sinken (2 %)?",
                linien(L, 1, "52,4 kg · 0,02 ≈ 1,05 kg")),
        aufgabe(5, 2, "Eine Werbung sagt: „Ohne unser Sportgetränk keine Leistung!“ Bewerte die Aussage für den Schulsport.",
                linien(L, 3, "Stimmt nicht. Im Schulsport reicht Wasser völlig. Bei langen Belastungen geht auch eine verdünnte Saftschorle. "
                             "Sportgetränke sind teuer und nur bei langen Wettkämpfen im Leistungssport sinnvoll.")),
        aufgabe(6, 0, "Was lässt bei etwa 2 % Wasserverlust nach? Nenne drei Dinge.",
                felder(L, [("1", "Ausdauer"), ("2", "Kraft"), ("3", "Konzentration")], 3, 40)),
        aufgabe(7, 1, "Woran erkennst du, dass ein Mitschüler bei Hitze Probleme bekommt? Was tust du?",
                linien(L, 3, "Kopfschmerzen, Schwindel, Übelkeit, sehr rotes oder blasses Gesicht. Er soll aufhören, in den Schatten, kühlen, trinken, Lehrkraft holen.")),
        aufgabe(8, 2, "Plane, was und wie viel du an einem heißen Wettkampftag trinkst. Begründe deinen Plan.",
                linien(L, 4, "Morgens zwei Gläser Wasser, Flasche mit 1,5 Liter Wasser oder Schorle mitnehmen, in jeder Pause trinken, "
                             "nach dem Wettkampf weiter trinken. Bei Hitze schwitzt man viel, ab 2 % Verlust sinkt die Leistung.")),
    ]
    return blatt(ET, 3, "Trinken und Sportgetränke", v,
                 ["Ab etwa 2 % Wasserverlust sinkt die Leistung.",
                  "Vor, während und nach dem Sport trinken.",
                  "Wasser reicht im Schulsport, Energydrinks sind ungeeignet."], a)


# ================================================================== Fair Play
FP = "Fair Play"


def fp1(L):
    v = abschnitt("A", "Zwei Arten von Fairness")
    v += P("Im Sport unterscheidet man zwei Arten von Fair Play.")
    v += kacheln([
        ("#dbe8f5", "Formelle Fairness", "„Muss-Fairness“",
         "Die geschriebenen Regeln einhalten. Wer sie bricht, wird bestraft: Freiwurf, Gelbe Karte, Disqualifikation."),
        ("#d9efd8", "Informelle Fairness", "„Soll-Fairness“",
         "Mehr tun, als die Regeln verlangen: den Gegner respektieren, eigene Fehler zugeben, Chancengleichheit wahren. "
         "Dafür gibt es keine Strafe, aber Anerkennung."),
    ])
    v += abschnitt("B", "Beispiele")
    v += P("Ein Tennisspieler sagt dem Schiedsrichter, dass der Ball des Gegners doch im Feld war, obwohl er „Aus“ gegeben hat. "
           "Eine Läuferin hilft einer gestürzten Konkurrentin auf, statt weiterzulaufen. "
           "Solche Momente zeigen informelle Fairness. Sie werden manchmal sogar mit Fair-Play-Preisen ausgezeichnet.")
    v += P("Das Gegenteil sind <b>Schwalben</b> (ein Foul vortäuschen), <b>Zeitschinden</b>, absichtliche Fouls, um einen Angriff zu stoppen, "
           "oder Beleidigungen. Manches davon ist sogar erlaubt oder wird nicht bestraft, fair ist es trotzdem nicht.")
    v += abschnitt("C", "Warum fair spielen?")
    v += P("Sport funktioniert nur, wenn sich alle an gemeinsame Regeln halten. Ein Sieg durch Betrug ist nichts wert, "
           "weil er nicht zeigt, wer wirklich besser war. Außerdem machen Spiele, in denen fair gespielt wird, allen mehr Spaß, "
           "und es gibt weniger Verletzungen und Streit.")
    v += abschnitt("D", "Fair Play im Schulsport")
    v += P("Im Sportunterricht gibt es oft keinen Schiedsrichter. Dann sind alle selbst für Fairness verantwortlich: "
           "Fouls zugeben, Bälle ehrlich als Aus melden, Mitspieler einbeziehen und Schwächere nicht auslachen.")

    v += abschnitt("E", "Fair Play über den Sport hinaus")
    v += P("Wer im Sport fair ist, ist es oft auch anderswo: Er schreibt in der Klassenarbeit nicht ab, steht zu seinen Fehlern und hilft anderen. "
           "Fair Play ist deshalb mehr als eine Sportregel. Es ist eine Haltung, die man im Sport besonders gut üben kann.")
    a = [
        aufgabe(1, 0, "Formelle oder informelle Fairness? Schreibe f oder i.",
                zuordnen(L, ["f = formell (Regeln einhalten)", "i = informell (mehr als die Regeln)"], [
                    ("Nicht mit der Hand spielen beim Fußball.", "f"),
                    ("Einer gestürzten Gegnerin aufhelfen.", "i"),
                    ("Eigenes Foul zugeben, das der Schiedsrichter nicht gesehen hat.", "i"),
                    ("Nur drei Schritte mit dem Ball beim Handball.", "f")])),
        aufgabe(2, 1, "Erkläre den Unterschied zwischen „Muss-Fairness“ und „Soll-Fairness“ mit eigenen Worten.",
                linien(L, 3, "Muss-Fairness heißt, die geschriebenen Regeln einzuhalten, sonst gibt es eine Strafe. "
                             "Soll-Fairness geht darüber hinaus: Respekt, ehrlich sein, Fehler zugeben, auch wenn es keine Strafe gibt.")),
        aufgabe(3, 1, "Beschreibe eine Situation aus dem Sportunterricht oder Verein, in der jemand informell fair war.",
                linien(L, 2, "Beispiel: Beim Basketball hat ein Spieler zugegeben, dass er den Ball zuletzt berührt hat.")),
        aufgabe(4, 2, "Ein Spieler foult kurz vor Schluss absichtlich, um ein Gegentor zu verhindern, und nimmt die Rote Karte in Kauf. "
                      "Ist das fair? Diskutiere beide Seiten und gib deine Meinung an.",
                linien(L, 4, "Formell nimmt er die Strafe an, die Regeln sehen das vor. Informell ist es unfair, weil er dem Gegner eine Torchance "
                             "absichtlich nimmt und ihn vielleicht verletzt. Meine Meinung: unfair, auch wenn es oft vorkommt.")),
        aufgabe(5, 2, "Schreibe eine kurze Rede (4 bis 5 Sätze), in der du deine Klasse vor einem Turnier zu Fair Play aufrufst.",
                linien(L, 4, "Wir wollen heute gewinnen, aber fair. Wir halten uns an die Regeln, auch wenn es niemand sieht. Wir lachen niemanden aus "
                             "und nehmen die Entscheidungen der Schiedsrichter an. Nach jedem Spiel geben wir die Hand, egal wie es ausgeht.")),
        aufgabe(6, 1, "Warum ist ein Sieg durch Betrug nichts wert? Begründe in zwei bis drei Sätzen.",
                linien(L, 3, "Er zeigt nicht, wer wirklich besser war. Man kann sich nicht ehrlich darüber freuen, und die anderen verlieren das Vertrauen.")),
    ]
    return blatt(FP, 1, "Formelle und informelle Fairness", v,
                 ["Formelle Fairness: Regeln einhalten.",
                  "Informelle Fairness: Respekt und Ehrlichkeit über die Regeln hinaus.",
                  "Nicht alles, was nicht bestraft wird, ist fair."], a)


def fp2(L):
    v = abschnitt("A", "Die Rolle des Schiedsrichters")
    v += P("Der Schiedsrichter sorgt dafür, dass ein Spiel nach den Regeln abläuft. Er entscheidet in Sekunden, "
           "sieht aber nicht alles und kann sich irren. Ohne ihn gäbe es ständig Streit. Deshalb gilt: "
           "Seine Entscheidung ist endgültig, auch wenn man anderer Meinung ist.")
    v += P("Ein guter Schiedsrichter ist <b>neutral</b>, kennt die Regeln, steht nah am Geschehen, pfeift klar und "
           "erklärt seine Entscheidungen mit Handzeichen. Er lässt das Spiel laufen, wenn ein Pfiff der benachteiligten Mannschaft "
           "schaden würde. Das nennt man <b>Vorteil</b>.")
    v += abschnitt("B", "Handzeichen im Basketball (Auswahl)")
    v += tabelle(["Handzeichen", "Bedeutung"],
                 [["Fäuste vor dem Körper rollen", "Schrittfehler"],
                  ["Hände abwechselnd auf und ab, als ob man prellt", "Doppeldribbling"],
                  ["Faust hoch gestreckt, Pfiff", "persönliches Foul"],
                  ["Arm hoch, drei Finger gestreckt", "Dreipunktwurf versucht"],
                  ["Unterarme über dem Kopf kreuzen", "Auswechslung"],
                  ["Hände zu einem T formen", "Auszeit"]])
    v += abschnitt("C", "Schwierige Situationen")
    v += P("Wenn Spieler meckern oder den Schiedsrichter beleidigen, wird es für alle schwer. "
           "Viele junge Schiedsrichter hören deshalb wieder auf. Im Amateurfußball fehlen inzwischen viele Schiedsrichter. "
           "Respekt vor dem Schiedsrichter ist also nicht nur höflich, sondern notwendig, damit überhaupt gespielt werden kann.")
    v += P("Im Sportunterricht übernehmen oft Schüler das Pfeifen. Wer selbst schon einmal gepfiffen hat, weiß, wie schwer das ist.")

    v += abschnitt("D", "Tipps, wenn du selbst pfeifst")
    v += P("Laut und deutlich pfeifen, sofort entscheiden und die Entscheidung mit einem Handzeichen zeigen. Nicht diskutieren, aber ruhig bleiben. "
           "Wer einen Fehler bemerkt, darf ihn zugeben. Das schafft Vertrauen.")
    a = [
        aufgabe(1, 0, "Welche Eigenschaften braucht ein guter Schiedsrichter? Nenne vier.",
                felder(L, [("1", "neutral"), ("2", "kennt die Regeln"), ("3", "nah am Spiel"), ("4", "klare Zeichen")], 4, 34)),
        aufgabe(2, 0, "Welches Handzeichen gehört zu welcher Entscheidung? Ordne zu.",
                zuordnen(L, ["Fäuste rollen", "drei Finger hoch", "Hände zu einem T", "Unterarme über dem Kopf kreuzen"], [
                    ("Auszeit", "C"), ("Schrittfehler", "A"), ("Auswechslung", "D"), ("Dreipunktwurf", "B")])),
        aufgabe(3, 1, "Was bedeutet „Vorteil“? Erkläre an einem Beispiel.",
                linien(L, 2, "Der Schiedsrichter pfeift ein Foul nicht ab, weil die gefoulte Mannschaft trotzdem eine gute Chance hat, "
                             "z. B. der Spieler läuft weiter allein aufs Tor zu.")),
        aufgabe(4, 1, "Du pfeifst ein Basketballspiel. Welche Entscheidung triffst du?",
                '<p style="margin-bottom:.5mm">a) Ein Spieler läuft mit dem Ball in der Hand drei Schritte.</p>' + linien(L, 1, "Schrittfehler, Ball für die andere Mannschaft")
                + '<p style="margin:1.5mm 0 .5mm 0">b) Ein Werfer wird beim Korbwurf gestoßen.</p>' + linien(L, 1, "Foul, Freiwürfe für den Werfer")
                + '<p style="margin:1.5mm 0 .5mm 0">c) Ein Spieler hört auf zu dribbeln und dribbelt wieder los.</p>' + linien(L, 1, "Doppeldribbling, Ball für die andere Mannschaft")),
        aufgabe(5, 2, "Warum hören viele junge Schiedsrichter wieder auf? Was könnte man dagegen tun?",
                linien(L, 3, "Weil sie beschimpft und bedrängt werden. Dagegen: Respekt-Regeln, nur der Kapitän spricht mit dem Schiedsrichter, "
                             "Strafen für Beleidigungen, Trainer und Eltern als Vorbild.")),
        aufgabe(6, 1, "Du pfeifst im Unterricht und ein Mitschüler beschwert sich lautstark. Wie reagierst du?",
                linien(L, 3, "Ruhig bleiben, die Entscheidung kurz erklären oder zeigen, nicht diskutieren und weiterspielen lassen. "
                             "Bei Beleidigungen die Lehrkraft einschalten.")),
        aufgabe(7, 2, "Würdest du gern Schiedsrichter sein? Begründe mit Vor- und Nachteilen.",
                linien(L, 3, "Vorteil: man lernt die Regeln genau, ist mitten im Spiel und übernimmt Verantwortung. Nachteil: man wird oft kritisiert. "
                             "Ich würde es ausprobieren.")),
    ]
    return blatt(FP, 2, "Schiedsrichter sein", v,
                 ["Die Entscheidung des Schiedsrichters gilt.",
                  "Ein guter Schiedsrichter ist neutral und zeigt klare Zeichen.",
                  "Ohne Respekt gibt es bald keine Schiedsrichter mehr."], a)


def fp3(L):
    v = abschnitt("A", "Streit im Spiel")
    v += P("Im Sport geht es um etwas, da kochen die Gefühle schnell hoch. Ein hartes Foul, ein umstrittener Pfiff, "
           "ein Mitspieler, der nie abgibt: Schon gibt es Streit. Streit an sich ist nicht schlimm. "
           "Wichtig ist, wie man ihn löst, ohne zu beleidigen oder handgreiflich zu werden.")
    v += abschnitt("B", "Du-Botschaft und Ich-Botschaft")
    v += P("Wer sich ärgert, macht oft dem anderen einen Vorwurf: „Du spielst nie ab!“ Das ist eine <b>Du-Botschaft</b>. "
           "Der andere fühlt sich angegriffen und wehrt sich. Besser ist eine <b>Ich-Botschaft</b>. Sie hat drei Teile:")
    v += kacheln([
        ("#dbe8f5", "1 Was ist passiert?", "", "„Du hast in den letzten drei Angriffen nicht abgespielt.“"),
        ("#fbe9c2", "2 Wie geht es mir?", "", "„Ich ärgere mich, weil ich frei stand.“"),
        ("#d9efd8", "3 Was wünsche ich mir?", "", "„Ich wünsche mir, dass du schaust, wer frei ist.“"),
    ], cols=3)
    v += abschnitt("C", "Fünf Schritte zur Lösung")
    v += P("<b>1 Abkühlen:</b> Kurz unterbrechen, durchatmen, Abstand nehmen.<br>"
           "<b>2 Jeder erzählt:</b> Nacheinander, ohne zu unterbrechen, in Ich-Botschaften.<br>"
           "<b>3 Zuhören und wiederholen:</b> „Du meinst also, dass …“<br>"
           "<b>4 Lösung suchen:</b> Was können beide tun? Ideen sammeln, eine auswählen.<br>"
           "<b>5 Abmachen:</b> Hand geben, weiterspielen.")
    v += P("Wenn die Beteiligten das nicht allein schaffen, hilft eine dritte Person, zum Beispiel ein Mitschüler als Streitschlichter "
           "oder die Lehrkraft.")

    v += abschnitt("D", "Streit vorbeugen")
    v += P("Viele Streitereien lassen sich verhindern: Regeln vor dem Spiel klar absprechen, Teams fair einteilen, einen Kapitän bestimmen, "
           "der mit dem Schiedsrichter spricht, und bei unklaren Situationen eine einfache Lösung vereinbaren, etwa einen Schiedsrichterball.")
    a = [
        aufgabe(1, 0, "Du-Botschaft oder Ich-Botschaft? Schreibe d oder i.",
                zuordnen(L, ["d = Du-Botschaft", "i = Ich-Botschaft"], [
                    ("„Du bist so ein Egoist!“", "d"),
                    ("„Ich bin enttäuscht, weil ich nie den Ball bekomme.“", "i"),
                    ("„Du foulst ständig!“", "d"),
                    ("„Ich habe Angst, mich zu verletzen, wenn du so hart reingehst.“", "i")])),
        aufgabe(2, 0, "Bringe die Schritte zur Lösung in die richtige Reihenfolge.",
                reihenfolge(L, ["Abkühlen", "Jeder erzählt", "Zuhören und wiederholen", "Lösung suchen", "Abmachen"],
                            ["Lösung suchen", "Abkühlen", "Abmachen", "Zuhören und wiederholen", "Jeder erzählt"])),
        aufgabe(3, 1, "Forme die Du-Botschaft in eine Ich-Botschaft mit allen drei Teilen um.",
                '<p style="margin:0 0 .5mm 0">„Du foulst ständig, du Idiot!“</p>'
                + linien(L, 3, "Du hast mich gerade zweimal am Trikot gezogen. Ich ärgere mich, weil ich so nicht spielen kann. "
                               "Ich wünsche mir, dass du mich nicht mehr festhältst.")),
        aufgabe(4, 1, "Warum führen Du-Botschaften oft zu noch mehr Streit?",
                linien(L, 2, "Der andere fühlt sich angegriffen und verteidigt sich oder greift zurück an.")),
        aufgabe(5, 2, "Zwei Mitschüler streiten, ob der Ball im Aus war. Beschreibe, wie du als Streitschlichter vorgehen würdest.",
                linien(L, 4, "Erst beide beruhigen. Dann erzählt jeder seine Sicht, der andere hört zu. Ich wiederhole, was ich verstanden habe. "
                             "Dann suchen wir eine Lösung, z. B. Schiedsrichterball oder Wiederholung. Zum Schluss Hand geben.")),
        aufgabe(6, 2, "Erinnere dich an einen Streit im Sport (ohne Namen). Wie wurde er gelöst? Was hätte man mit den fünf Schritten besser machen können?",
                linien(L, 4, "Beispiel: Streit um einen Ball im Aus, es wurde geschrien und ein Spieler ist gegangen. Mit den fünf Schritten: erst abkühlen, "
                             "beide erzählen lassen, zuhören, dann Schiedsrichterball vereinbaren.")),
    ]
    return blatt(FP, 3, "Streit lösen", v,
                 ["Streit ist normal, wichtig ist, wie man ihn löst.",
                  "Ich-Botschaft: Was ist passiert, wie geht es mir, was wünsche ich mir.",
                  "Abkühlen, erzählen, zuhören, Lösung suchen, abmachen."], a)


# ================================================================== Herz, Puls und Ausdauer
HP = "Herz, Puls und Ausdauer"


def hp1(L):
    v = abschnitt("A", "Zwei Kreisläufe")
    v += P("Das Herz ist eine Pumpe mit zwei Hälften. Die rechte Hälfte pumpt sauerstoffarmes Blut in die Lunge. "
           "Dort gibt das Blut Kohlenstoffdioxid ab und nimmt Sauerstoff auf. Das ist der <b>Lungenkreislauf</b>. "
           "Das sauerstoffreiche Blut fließt zurück in die linke Herzhälfte. Sie pumpt es mit viel Druck in den ganzen Körper: "
           "der <b>Körperkreislauf</b>. In den Muskeln und Organen gibt das Blut den Sauerstoff ab und fließt dann zurück zum Herzen.")
    v += ('<div style="display:flex;gap:1.5mm;align-items:center;justify-content:center;margin:1mm 0 2mm 0;font-weight:600;font-size:9.5pt;flex-wrap:wrap">'
          + " ➜ ".join(f'<span class="box" style="padding:.8mm 2mm">{t}</span>'
                       for t in ("rechte Herzhälfte", "Lunge", "linke Herzhälfte", "Körper und Muskeln", "rechte Herzhälfte")) + '</div>')
    v += P("Adern, die vom Herzen wegführen, heißen <b>Arterien</b>. Adern, die zum Herzen hinführen, heißen <b>Venen</b>.")
    v += abschnitt("B", "Wie viel Blut pumpt das Herz?")
    v += P("Mit jedem Schlag pumpt das Herz eines Jugendlichen in Ruhe etwa 60 bis 70 ml Blut in den Körper. "
           "Das ist das <b>Schlagvolumen</b>. Schlagvolumen mal Herzfrequenz ergibt das <b>Herzminutenvolumen</b>:")
    v += ('<div class="box" style="text-align:center;margin:1mm 0 2mm 0;font-weight:600">Herzminutenvolumen = Schlagvolumen · Herzfrequenz<br>'
          '<span style="font-weight:400">Beispiel in Ruhe: 70 ml · 70 Schläge pro Minute = 4900 ml, also etwa 5 Liter pro Minute</span></div>')
    v += P("Bei starker Belastung steigen Herzfrequenz und Schlagvolumen. Dann kann das Herzminutenvolumen auf das Vier- bis Fünffache steigen.")
    v += abschnitt("C", "Training verändert das Herz")
    v += P("Regelmäßiges Ausdauertraining macht den Herzmuskel kräftiger. Das Schlagvolumen wird größer. "
           "Für dieselbe Blutmenge braucht das Herz dann weniger Schläge: Der Ruhepuls sinkt. "
           "Gut trainierte Ausdauersportler haben oft einen Ruhepuls von 40 bis 50.")

    v += abschnitt("D", "Herz-Kreislauf-Krankheiten")
    v += P("Herz-Kreislauf-Krankheiten wie Herzinfarkt und Schlaganfall gehören zu den häufigsten Todesursachen in Deutschland. "
           "Risikofaktoren sind Bewegungsmangel, Rauchen, Übergewicht, ungesunde Ernährung und Stress. Regelmäßige Bewegung senkt das Risiko deutlich, "
           "und die Grundlage dafür wird schon im Jugendalter gelegt.")
    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Im {} nimmt das Blut Sauerstoff auf. Die linke Herzhälfte pumpt Blut in den {}. "
                "Adern, die vom Herzen wegführen, heißen {}. Die Blutmenge pro Herzschlag heißt {}.",
                ["Lungenkreislauf", "Körperkreislauf", "Arterien", "Schlagvolumen"],
                ["Arterien", "Schlagvolumen", "Körperkreislauf", "Lungenkreislauf"], 34)),
        aufgabe(2, 0, "Ordne den Weg des Blutes. Beginne in der rechten Herzhälfte.",
                reihenfolge(L, ["rechte Herzhälfte", "Lunge", "linke Herzhälfte", "Körper und Muskeln"],
                            ["Körper und Muskeln", "linke Herzhälfte", "rechte Herzhälfte", "Lunge"])),
        aufgabe(3, 1, "Berechne das Herzminutenvolumen.",
                felder(L, [("60 ml und 80 Schläge", "4800 ml"), ("70 ml und 180 Schläge", "12 600 ml"),
                           ("100 ml und 50 Schläge", "5000 ml")], 3, 40)),
        aufgabe(4, 1, "Warum hat ein trainierter Ausdauersportler einen niedrigeren Ruhepuls?",
                linien(L, 2, "Sein Herzmuskel ist kräftiger und pumpt pro Schlag mehr Blut. Für dieselbe Menge braucht er weniger Schläge.")),
        aufgabe(5, 2, "Ein Sportler braucht in Ruhe 5 Liter Blut pro Minute, sein Schlagvolumen ist 100 ml. Wie hoch ist sein Ruhepuls? "
                      "Vergleiche mit einem Untrainierten (70 ml).",
                linien(L, 3, "5000 : 100 = 50 Schläge pro Minute. Untrainiert: 5000 : 70 ≈ 71 Schläge pro Minute. "
                             "Der Trainierte braucht etwa 21 Schläge weniger.")),
        aufgabe(6, 0, "Zeichne den Blutkreislauf als Schema: Herz in die Mitte, Lunge oben, Körper unten, mit Pfeilen.",
                karo(L, 30, "Herz Mitte, Pfeile: rechte Hälfte → Lunge → linke Hälfte → Körper → rechte Hälfte")),
        aufgabe(7, 2, "Erkläre einem Fünftklässler mit einem Vergleich, wie der Blutkreislauf funktioniert.",
                linien(L, 4, "Das Herz ist wie eine Pumpe in einem Rohrsystem. Die rechte Seite pumpt das Blut zur Lunge, dort tankt es Sauerstoff. "
                             "Die linke Seite pumpt es dann zu allen Muskeln, wie ein Lieferwagen, der Sauerstoff ausliefert und leer zurückkommt.")),
    ]
    return blatt(HP, 1, "Herz und Kreislauf", v,
                 ["Lungenkreislauf: Blut holt Sauerstoff. Körperkreislauf: Blut bringt ihn zu den Muskeln.",
                  "Herzminutenvolumen = Schlagvolumen · Herzfrequenz.",
                  "Training vergrößert das Schlagvolumen, der Ruhepuls sinkt."], a)


def hp2(L):
    v = abschnitt("A", "Die maximale Herzfrequenz")
    v += P("Wie schnell das Herz höchstens schlagen kann, hängt vor allem vom Alter ab. Eine einfache Faustformel lautet:")
    v += '<div class="box" style="text-align:center;margin:1mm 0 2mm 0;font-weight:600">maximale Herzfrequenz ≈ 220 − Lebensalter</div>'
    v += P("Für einen 13-Jährigen sind das etwa 220 − 13 = 207 Schläge pro Minute. Die Formel ist nur ein Richtwert, "
           "bei einzelnen Menschen kann der echte Wert 10 bis 20 Schläge darüber oder darunter liegen.")
    v += abschnitt("B", "Belastungsbereiche")
    v += P("Je nachdem, wie hoch der Puls im Verhältnis zur maximalen Herzfrequenz ist, trainiert man etwas anderes:")
    v += tabelle(["Bereich", "Anteil der max. Herzfrequenz", "So fühlt es sich an", "Wirkung"],
                 [["locker", "50 bis 60 %", "sehr leicht, Unterhaltung problemlos", "Erholung, Aufwärmen"],
                  ["Grundlagenausdauer", "60 bis 75 %", "angenehm, Sprechen in Sätzen möglich", "Ausdauer, Fettverbrennung"],
                  ["zügig", "75 bis 85 %", "anstrengend, nur noch kurze Sätze", "Tempo-Ausdauer"],
                  ["intensiv", "85 bis 100 %", "sehr hart, Sprechen kaum möglich", "Schnelligkeit, nur kurz durchzuhalten"]])
    v += abschnitt("C", "Den Puls im Sport nutzen")
    v += P("Viele Anfänger laufen zu schnell. Für die Grundlagenausdauer reicht ein Tempo, bei dem man sich noch unterhalten kann. "
           "Die meisten Trainingsminuten sollten in diesem Bereich liegen. Den Puls misst man direkt nach der Belastung "
           "10 Sekunden lang und nimmt den Wert mal 6. Länger sollte man nicht zählen, weil der Puls schnell wieder sinkt.")

    v += abschnitt("D", "Puls messen mit Uhr")
    v += P("Viele Sportuhren und Fitnessarmbänder messen den Puls am Handgelenk. Das ist bequem, bei schnellen Bewegungen aber manchmal ungenau. "
           "Die Messung mit den Fingern bleibt eine gute Kontrolle.")
    a = [
        aufgabe(1, 0, "Berechne die maximale Herzfrequenz mit der Faustformel.",
                felder(L, [("12 Jahre", "208"), ("14 Jahre", "206"), ("40 Jahre", "180"), ("du selbst", "z. B. 207")], 4, 30)),
        aufgabe(2, 1, "Ein 13-Jähriger will Grundlagenausdauer trainieren (60 bis 75 %). In welchem Pulsbereich soll er laufen?",
                linien(L, 2, "max. HF = 207. 207 · 0,6 ≈ 124 und 207 · 0,75 ≈ 155. Also etwa 124 bis 155 Schläge pro Minute.")),
        aufgabe(3, 1, "Nach einem Lauf zählt eine Schülerin 28 Schläge in 10 Sekunden. Wie hoch ist ihr Puls? In welchem Bereich lag sie (13 Jahre)?",
                linien(L, 2, "28 · 6 = 168. 168 : 207 ≈ 0,81, also 81 %: zügiger Bereich.")),
        aufgabe(4, 2, "Warum sollte man den Puls nach der Belastung nicht eine ganze Minute lang zählen?",
                linien(L, 2, "Der Puls sinkt nach der Belastung schnell. Nach einer Minute wäre der Wert zu niedrig.")),
        aufgabe(5, 2, "Läufer A unterhält sich beim Laufen in ganzen Sätzen. Läufer B keucht und kann kaum sprechen. In welchem Bereich laufen sie? Begründe.",
                linien(L, 3, "A läuft im Bereich Grundlagenausdauer, weil Sprechen in Sätzen möglich ist. B läuft intensiv, "
                             "weil Sprechen kaum möglich ist.")),
        aufgabe(6, 2, "Viele Anfänger laufen zu schnell. Gib einem Anfänger drei Tipps für das richtige Tempo und begründe sie.",
                linien(L, 3, "Sprechtest: noch in Sätzen reden können. Langsam starten, die ersten Minuten bewusst ruhig. Puls kontrollieren, "
                             "60 bis 75 % der max. Herzfrequenz. So hält man länger durch und trainiert die Grundlagenausdauer.")),
        aufgabe(7, 1, "Warum ist die Faustformel 220 − Alter nur ein Richtwert?",
                linien(L, 2, "Jeder Mensch ist anders. Bei manchen liegt die echte maximale Herzfrequenz 10 bis 20 Schläge darüber oder darunter.")),
        aufgabe(8, 2, "Plane einen 30-minütigen Lauf mit Aufwärmen, Hauptteil und Auslaufen. Gib für jeden Teil die Dauer und deinen Pulsbereich an.",
                linien(L, 4, "Beispiel, 13 Jahre: 5 min Aufwärmen bei 50 bis 60 % (etwa 105 bis 125), 20 min Hauptteil bei 60 bis 75 % (etwa 125 bis 155), "
                             "5 min Auslaufen wieder bei 50 bis 60 %.")),
    ]
    return blatt(HP, 2, "Pulsbereiche", v,
                 ["Maximale Herzfrequenz ≈ 220 − Alter.",
                  "Grundlagenausdauer bei 60 bis 75 %, Unterhaltung möglich.",
                  "Puls nach Belastung: 10 Sekunden zählen, mal 6."], a)


def hp3(L):
    v = abschnitt("A", "Der Coopertest")
    v += P("Der Coopertest wurde von dem amerikanischen Arzt Kenneth Cooper entwickelt. Man läuft <b>12 Minuten</b> so weit wie möglich. "
           "Die Strecke zeigt, wie gut die Ausdauer ist. Gehen ist erlaubt, Stehenbleiben bringt aber nichts.")
    v += abschnitt("B", "Strecke und Tempo berechnen")
    v += P("Auf einer 400-m-Bahn zählt man die Runden und schätzt den letzten Teil ab. Aus der Strecke lässt sich die Durchschnittsgeschwindigkeit berechnen:")
    v += ('<div class="box" style="margin:1mm 0 2mm 0"><b>Beispiel:</b> 6 Runden und 200 m = 2400 m + 200 m = 2600 m in 12 Minuten.<br>'
          'In 60 Minuten wären das 5 · 2600 m = 13 000 m. Die Geschwindigkeit ist also <b>13 km/h</b>.<br>'
          'Für eine Runde braucht man im Schnitt 12 min : 6,5 Runden ≈ 1 min 51 s.</div>')
    v += abschnitt("C", "Die richtige Taktik")
    v += P("Am meisten schafft, wer <b>gleichmäßig</b> läuft. Wer schnell startet, bildet in den Muskeln viel Laktat, "
           "wird sauer und muss später deutlich langsamer werden. Gute Läufer teilen sich die 12 Minuten ein: "
           "Sie nehmen sich eine Rundenzeit vor und kontrollieren sie an jeder Runde. Erst in der letzten Minute wird gesteigert.")
    v += tabelle(["Ziel", "Rundenzeit (400 m)"],
                 [["2000 m", "2:24 min"], ["2400 m", "2:00 min"], ["2800 m", "1:43 min"], ["3200 m", "1:30 min"]])
    v += abschnitt("D", "Wie geht es besser?")
    v += P("Wer seine Leistung verbessern will, sollte über mehrere Wochen zwei- bis dreimal pro Woche locker laufen, "
           "zum Beispiel 20 bis 30 Minuten im Bereich der Grundlagenausdauer. Kurz vor dem Test bringt Training nichts mehr.")

    v += abschnitt("E", "Kopfsache")
    v += P("Laufen über 12 Minuten ist auch Kopfsache. Viele teilen sich den Lauf in Abschnitte ein („noch drei Runden“), konzentrieren sich "
           "auf ihren Atemrhythmus oder sagen sich innerlich Mut zu. Wer nur an die Erschöpfung denkt, wird schneller langsamer.")
    a = [
        aufgabe(1, 0, "Rechne die gelaufene Strecke aus (Runde = 400 m).",
                felder(L, [("5 Runden + 100 m", "2100 m"), ("6 Runden + 300 m", "2700 m"),
                           ("7 Runden", "2800 m"), ("4 Runden + 350 m", "1950 m")], 4, 30)),
        aufgabe(2, 1, "Berechne die Durchschnittsgeschwindigkeit in km/h wie im Beispiel.",
                felder(L, [("2000 m in 12 min", "10 km/h"), ("2400 m in 12 min", "12 km/h"), ("3000 m in 12 min", "15 km/h")], 3, 40)),
        aufgabe(3, 1, "Ein Schüler will 2400 m schaffen. Seine Rundenzeiten: 1:40, 1:50, 2:05, 2:20, 2:30 … Was macht er falsch? Gib einen Rat.",
                linien(L, 3, "Er startet viel zu schnell (1:40 statt 2:00) und wird immer langsamer. "
                             "Rat: von Anfang an gleichmäßig 2:00 pro Runde laufen und erst am Ende steigern.")),
        aufgabe(4, 2, "Plane für dich ein Training über vier Wochen, um beim nächsten Coopertest weiter zu kommen.",
                linien(L, 3, "Woche 1 und 2: zweimal 20 min locker laufen. Woche 3: zweimal 25 min, einmal 4 Runden in Wunschtempo. "
                             "Woche 4: zweimal 30 min locker, zwei Tage vor dem Test Pause.")),
        aufgabe(5, 1, "Welche Rundenzeit brauchst du im Schnitt für 2600 m? Und für 3000 m?",
                linien(L, 2, "2600 m = 6,5 Runden: 12 min : 6,5 ≈ 1:51 min. 3000 m = 7,5 Runden: 12 min : 7,5 = 1,6 min = 1:36 min.")),
        aufgabe(6, 1, "Welche Tricks helfen dir, wenn es beim Laufen schwer wird? Nenne drei und erkläre, warum sie helfen.",
                linien(L, 3, "In Abschnitte einteilen, dann wirkt die Strecke kürzer. Auf den Atem achten, das beruhigt. Sich Mut zusprechen, das lenkt ab.")),
        aufgabe(7, 1, "Warum wird man nach einem zu schnellen Start später so viel langsamer? Erkläre.",
                linien(L, 3, "Beim schnellen Start entsteht viel Laktat, die Muskeln werden sauer und schwer. Danach muss man das Tempo stark senken.")),
        aufgabe(8, 2, "Wie lief dein letzter Coopertest? Beschreibe ihn und schreibe auf, was du beim nächsten Mal anders machen willst.",
                linien(L, 4, "Beispiel: Ich bin zu schnell gestartet und musste nach 5 Minuten gehen. Nächstes Mal nehme ich mir 2:00 min pro Runde vor "
                             "und schaue an jeder Runde auf die Uhr.")),
    ]
    return blatt(HP, 3, "Coopertest verstehen", v,
                 ["12 Minuten so weit wie möglich laufen.",
                  "Gleichmäßiges Tempo bringt die beste Strecke.",
                  "Verbessern durch lockeres Laufen über mehrere Wochen."], a)


# ================================================================== Training und Erholung
TE = "Training und Erholung"


def te1(L):
    v = abschnitt("A", "Was macht Fitness aus?")
    v += P("Fit sein heißt mehr als nur schnell laufen zu können. Sportwissenschaftler unterscheiden fünf <b>motorische Fähigkeiten</b>. "
           "Jede Sportart braucht eine andere Mischung.")
    v += kacheln([
        ("#f6d9d6", "Kraft", "", "Einen Widerstand überwinden: Kugel stoßen, Klimmzüge, hochspringen."),
        ("#dbe8f5", "Ausdauer", "", "Eine Belastung lange durchhalten: Coopertest, Schwimmen, Radfahren."),
        ("#fbe9c2", "Schnelligkeit", "", "Schnell reagieren und sich schnell bewegen: Sprint, Start, Torwart."),
        ("#d9efd8", "Beweglichkeit", "", "Große Bewegungen in den Gelenken: Spagat, Brücke, Hürdensitz."),
        ("#e7def3", "Koordination", "", "Bewegungen geschickt steuern: Gleichgewicht, Rhythmus, Ballgefühl, Turnen, Parcours."),
        ("#eeeeee", "Zusammen", "", "Kraft, Ausdauer und Schnelligkeit hängen vom Körper ab, Koordination und Beweglichkeit stark vom Üben."),
    ])
    v += abschnitt("B", "Wie man sie testet")
    v += tabelle(["Fähigkeit", "einfacher Test"],
                 [["Kraft", "Standweitsprung, Liegestütze in 30 Sekunden"],
                  ["Ausdauer", "Coopertest (12 Minuten laufen)"],
                  ["Schnelligkeit", "Sprint über 30 oder 50 m"],
                  ["Beweglichkeit", "Rumpfbeuge: im Stand mit gestreckten Beinen nach unten reichen"],
                  ["Koordination", "auf einem Bein mit geschlossenen Augen stehen, Seilspringen"]])
    v += abschnitt("C", "Training im Jugendalter")
    v += P("Zwischen 10 und 13 Jahren lernt man neue Bewegungen besonders leicht. Diese Zeit nennt man auch das „goldene Lernalter“. "
           "Später in der Pubertät wachsen Muskeln und Knochen schneller, Kraft und Ausdauer lassen sich dann gut steigern. "
           "Beweglichkeit nimmt ohne Training mit dem Alter ab, deshalb lohnt es sich, sie früh zu üben.")

    v += abschnitt("D", "Koordination genauer")
    v += P("Koordination besteht aus mehreren Teilen: <b>Gleichgewicht</b> (Balken, Slackline), <b>Reaktion</b> (Start, Torwart), "
           "<b>Rhythmus</b> (Hürdenlauf, Seilspringen), <b>Orientierung</b> (Position im Raum, Turnen) und <b>Differenzierung</b>, "
           "also das Gefühl für den richtigen Krafteinsatz (Ballgefühl beim Pass).")
    a = [
        aufgabe(1, 0, "Welche Fähigkeit ist vor allem gefragt? Schreibe Kraft, Ausdauer, Schnelligkeit, Beweglichkeit oder Koordination.",
                felder(L, [("Marathon", "Ausdauer"), ("Spagat", "Beweglichkeit"), ("Kugelstoßen", "Kraft"),
                           ("Torwart bei Elfmeter", "Schnelligkeit"), ("Jonglieren", "Koordination"), ("Klimmzüge", "Kraft")], 3, 44)),
        aufgabe(2, 0, "Ordne die Tests den Fähigkeiten zu.",
                zuordnen(L, ["Kraft", "Ausdauer", "Schnelligkeit", "Koordination"], [
                    ("50-m-Sprint", "C"), ("Standweitsprung", "A"), ("Coopertest", "B"), ("Einbeinstand mit geschlossenen Augen", "D")])),
        aufgabe(3, 1, "Welche drei Fähigkeiten braucht man im Basketball am meisten? Begründe jeweils kurz.",
                linien(L, 3, "Koordination für Dribbeln und Werfen, Schnelligkeit für Antritte und Reaktion, Ausdauer, weil man das ganze Spiel hin und her läuft.")),
        aufgabe(4, 1, "Was ist das „goldene Lernalter“ und was folgt daraus für dich?",
                linien(L, 2, "Zwischen 10 und 13 Jahren lernt man Bewegungen besonders leicht. Jetzt lohnt es sich, viele Sportarten und Techniken auszuprobieren.")),
        aufgabe(5, 2, "Erstelle ein Fitness-Profil von dir: Schätze jede Fähigkeit von 1 (schwach) bis 5 (stark) und nenne eine Übung für deine schwächste.",
                felder(L, [("Kraft", "z. B. 3"), ("Ausdauer", "z. B. 4"), ("Schnelligkeit", "z. B. 4"), ("Beweglichkeit", "z. B. 2"),
                           ("Koordination", "z. B. 3")], 5, 26)
                + linien(L, 1, "Beweglichkeit: täglich Rumpfbeuge und Ausfallschritt üben.")),
        aufgabe(6, 2, "Wähle eine Sportart, die du magst. Beschreibe, welche motorischen Fähigkeiten man braucht und wie man sie trainieren kann.",
                linien(L, 4, "Beispiel Tennis: Schnelligkeit für Antritte (kurze Sprints), Koordination für die Schläge (Ballübungen), "
                             "Ausdauer für lange Ballwechsel (Dauerlauf), Beweglichkeit in der Schulter (Dehnen).")),
    ]
    return blatt(TE, 1, "Die motorischen Fähigkeiten", v,
                 ["Kraft, Ausdauer, Schnelligkeit, Beweglichkeit, Koordination.",
                  "Jede Sportart braucht eine andere Mischung.",
                  "Zwischen 10 und 13 lernt man Bewegungen besonders leicht."], a)


def te2(L):
    from stufe56 import kurve
    v = abschnitt("A", "Anpassung: Superkompensation")
    v += P("Wenn du trainierst, belastest du deinen Körper. Er wird müde, seine Energiespeicher leeren sich. "
           "In der Erholungsphase baut er nicht nur wieder auf, sondern etwas über das alte Niveau hinaus. "
           "Das nennt man <b>Superkompensation</b>. Kommt die nächste Belastung zum richtigen Zeitpunkt, steigt die Leistung Schritt für Schritt.")
    v += f'<div style="width:118mm;margin:1mm auto 1mm auto">{kurve()}</div>'
    v += abschnitt("B", "Die wichtigsten Trainingsprinzipien")
    v += tabelle(["Prinzip", "Was es bedeutet"],
                 [["Wirksamer Reiz", "Das Training muss fordern. Wer immer nur leicht trainiert, wird nicht besser."],
                  ["Steigende Belastung", "Wird es leicht, steigert man nach und nach: mehr Wiederholungen, mehr Zeit, mehr Tempo."],
                  ["Belastung und Erholung", "Nach harten Einheiten braucht der Körper Pause. Zu kurz: Erschöpfung. Zu lang: Der Gewinn verpufft."],
                  ["Regelmäßigkeit", "Nur wer dranbleibt, wird besser. Wer aufhört, verliert die Anpassung wieder."],
                  ["Individualität", "Jeder Körper ist anders. Ein Plan muss zu Alter, Können und Ziel passen."]])
    v += abschnitt("C", "Übertraining")
    v += P("Wer zu viel trainiert und sich zu wenig erholt, wird nicht besser, sondern schlechter. "
           "Anzeichen sind ständige Müdigkeit, schlechter Schlaf, ein erhöhter Ruhepuls, häufige Infekte und Lustlosigkeit. "
           "Dann hilft nur eins: weniger trainieren und mehr erholen.")

    v += abschnitt("D", "Ein Beispiel")
    v += P("Ein Schüler schafft 8 Liegestütze. Er übt dreimal pro Woche (Regelmäßigkeit), macht 3 Sätze und steigert jede Woche um ein bis zwei "
           "Wiederholungen (steigende Belastung). Zwischen den Tagen liegt immer ein Ruhetag (Erholung). Nach sechs Wochen schafft er 16.")
    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Nach der Belastung baut der Körper über das alte Niveau hinaus auf. Das heißt {}. "
                "Damit man besser wird, muss das Training einen {} setzen. Wird es leicht, braucht es eine {} Belastung.",
                ["Superkompensation", "wirksamen Reiz", "steigende"], ["steigende", "Superkompensation", "wirksamen Reiz"], 38)),
        aufgabe(2, 0, "Welches Prinzip wird verletzt? Ordne zu.",
                zuordnen(L, ["wirksamer Reiz", "Belastung und Erholung", "Regelmäßigkeit", "Individualität"], [
                    ("Jemand trainiert jeden Tag hart ohne Pause.", "B"),
                    ("Jemand läuft immer nur 5 Minuten ganz langsam.", "A"),
                    ("Jemand trainiert im Mai einmal und dann erst im September.", "C"),
                    ("Ein 12-Jähriger übernimmt den Plan eines Profis.", "D")])),
        aufgabe(3, 1, "Zeichne die Kurve der Superkompensation und beschrifte Belastung, Erholung und stärker als vorher.",
                karo(L, 28, "Kurve fällt (Belastung), steigt wieder (Erholung) und liegt dann über der Ausgangslinie (stärker als vorher)")),
        aufgabe(4, 1, "Woran erkennt man Übertraining? Nenne drei Anzeichen.",
                linien(L, 2, "ständig müde, erhöhter Ruhepuls, häufig krank, schlechter Schlaf, keine Lust")),
        aufgabe(5, 2, "Was passiert, wenn die nächste Trainingseinheit zu früh kommt? Und wenn sie zu spät kommt? Erkläre mit der Kurve.",
                linien(L, 3, "Zu früh: Der Körper ist noch nicht erholt, die Leistung sinkt immer weiter. "
                             "Zu spät: Die Superkompensation ist wieder abgeklungen, man startet wieder vom alten Niveau.")),
        aufgabe(6, 2, "Du willst in 6 Wochen 20 Kniebeugen auf einem Bein schaffen (jetzt 6). Plane dein Training mit den Trainingsprinzipien.",
                linien(L, 4, "Dreimal pro Woche mit Ruhetag dazwischen, 3 Sätze. Jede Woche zwei Wiederholungen mehr, erst mit Festhalten, später frei. "
                             "Bei Muskelkater einen Tag mehr Pause.")),
    ]
    return blatt(TE, 2, "Trainingsprinzipien", v,
                 ["Superkompensation: Nach der Erholung ist man stärker als vorher.",
                  "Wirksamer Reiz, steigende Belastung, Regelmäßigkeit.",
                  "Zu viel Training ohne Erholung macht schlechter."], a)


def te3(L):
    v = abschnitt("A", "Warum Jugendliche abends nicht müde sind")
    v += P("In der Pubertät verschiebt sich die innere Uhr. Der Körper bildet das Schlafhormon <b>Melatonin</b> abends später als bei Kindern. "
           "Viele Jugendliche werden deshalb erst spät müde, müssen aber früh zur Schule. "
           "So entsteht ein Schlafmangel, der sich über die Woche aufsummiert. Am Wochenende lange auszuschlafen, gleicht das nur teilweise aus.")
    v += abschnitt("B", "Wie viel Schlaf?")
    v += P("Jugendliche zwischen 13 und 18 Jahren brauchen <b>8 bis 10 Stunden</b> Schlaf pro Nacht. "
           "Viele kommen unter der Woche nur auf 7 Stunden oder weniger.")
    v += abschnitt("C", "Schlaf und Sport")
    v += kacheln([
        ("#dbe8f5", "Muskeln", "", "Im Tiefschlaf werden Wachstumshormone ausgeschüttet. Muskeln reparieren sich und werden stärker."),
        ("#d9efd8", "Bewegungen lernen", "", "Neue Techniken, etwa ein Wurf oder eine Turnübung, werden im Schlaf im Gehirn gefestigt."),
        ("#fbe9c2", "Leistung", "", "Nach zu wenig Schlaf reagiert man langsamer, ist schwächer und verletzt sich leichter."),
        ("#f6d9d6", "Abwehrkräfte", "", "Wer dauerhaft zu wenig schläft, wird häufiger krank."),
    ])
    v += abschnitt("D", "Was hilft?")
    v += P("<b>Bildschirm:</b> Handy und Tablet strahlen helles, bläuliches Licht ab. Es bremst die Melatoninbildung. "
           "Außerdem halten Chats und Videos wach. Deshalb eine Stunde vor dem Schlafen weglegen, am besten außerhalb des Zimmers.<br>"
           "<b>Rhythmus:</b> Auch am Wochenende nicht mehr als ein bis zwei Stunden später ins Bett.<br>"
           "<b>Tageslicht und Bewegung:</b> Morgens Licht und tagsüber Sport helfen der inneren Uhr.<br>"
           "<b>Kein Koffein</b> am Nachmittag und Abend: Cola, Eistee, Energydrinks.")

    v += abschnitt("E", "Erholung am Tag")
    v += P("Auch tagsüber kann man sich erholen: kurze Pausen beim Lernen, Bewegung an der frischen Luft, Zeit mit Freunden. "
           "Stundenlanges Zocken oder Scrollen erholt dagegen kaum, weil das Gehirn ständig neue Reize verarbeiten muss.")
    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Das Schlafhormon heißt {}. Jugendliche brauchen {} Stunden Schlaf. Das helle Licht von {} bremst das Schlafhormon. "
                "Im Tiefschlaf werden {} ausgeschüttet.",
                ["Melatonin", "8 bis 10", "Bildschirmen", "Wachstumshormone"],
                ["Bildschirmen", "Wachstumshormone", "Melatonin", "8 bis 10"], 34)),
        aufgabe(2, 1, "Ein Schüler schläft von Montag bis Freitag jeweils von 23:30 bis 6:30 Uhr. Wie viele Stunden fehlen ihm in der Woche, "
                      "wenn er 9 Stunden bräuchte?",
                linien(L, 2, "7 Stunden pro Nacht, es fehlen 2 Stunden. In 5 Nächten fehlen 10 Stunden.")),
        aufgabe(3, 1, "Notiere deine Schlafzeiten der letzten drei Nächte und berechne den Durchschnitt.",
                felder(L, [("Nacht 1", "z. B. 8 h"), ("Nacht 2", "z. B. 7,5 h"), ("Nacht 3", "z. B. 9 h"), ("Durchschnitt", "z. B. 8,2 h")], 4, 30)),
        aufgabe(4, 2, "Am Samstag ist ein wichtiges Fußballspiel. Schreibe einen Plan für die beiden Abende davor, der dir hilft, gut zu schlafen.",
                linien(L, 3, "Um 21:30 Uhr Handy aus und in die Küche legen. Ab 17 Uhr keine Cola. Abendessen nicht zu spät. "
                             "Um 22 Uhr ins Bett, Zimmer dunkel und kühl. Morgens gleich ans Tageslicht.")),
        aufgabe(5, 0, "Nenne vier Dinge, die beim Einschlafen helfen.",
                felder(L, [("1", "Handy weg"), ("2", "fester Rhythmus"), ("3", "kein Koffein"), ("4", "Tageslicht und Sport")], 4, 34)),
        aufgabe(6, 1, "Was hindert dich selbst am meisten daran, genug zu schlafen? Was könntest du ändern?",
                linien(L, 3, "Beispiel: Ich schaue abends lange Videos. Ich lege das Handy um 21 Uhr in die Küche und lese stattdessen.")),
        aufgabe(7, 1, "Erkläre, warum viele Jugendliche abends nicht müde sind, obwohl sie früh aufstehen müssen.",
                linien(L, 3, "In der Pubertät bildet der Körper das Schlafhormon Melatonin später. Man wird erst spät müde, muss aber früh zur Schule.")),
        aufgabe(8, 2, "Sollte die Schule für Jugendliche später beginnen? Nimm Stellung mit Argumenten aus dem Text.",
                linien(L, 4, "Dafür: Die innere Uhr ist verschoben, mit späterem Beginn schlafen Jugendliche mehr, lernen und leisten besser. "
                             "Dagegen: Der Tag endet später, weniger Zeit für Sport und Freizeit. Meine Meinung: etwas später wäre gut.")),
    ]
    return blatt(TE, 3, "Schlaf und Erholung", v,
                 ["In der Pubertät verschiebt sich die innere Uhr nach hinten.",
                  "Jugendliche brauchen 8 bis 10 Stunden Schlaf.",
                  "Schlaf repariert Muskeln und festigt neue Bewegungen."], a)


# ================================================================== Verletzungen vermeiden
VZ = "Verletzungen vermeiden"


def vz1(L):
    v = abschnitt("A", "Die häufigsten Sportverletzungen")
    v += P("Im Schulsport passieren die meisten Verletzungen bei Ballspielen, vor allem an Fingern, Sprunggelenken und Knien. "
           "Nicht jede Verletzung ist gleich schlimm. Woran man sie erkennt:")
    v += tabelle(["Verletzung", "Was ist passiert?", "Typische Zeichen"],
                 [["Prellung", "Stoß oder Schlag auf Muskel oder Knochen", "Schmerz, Schwellung, blauer Fleck"],
                  ["Verstauchung", "Gelenk überdehnt, Bänder gezerrt", "Schmerz im Gelenk, Schwellung, Bewegung möglich"],
                  ["Bänderriss", "Band ganz oder teilweise gerissen", "starke Schwellung, Bluterguss, Gelenk instabil"],
                  ["Zerrung", "Muskel überdehnt", "plötzlicher ziehender Schmerz, Muskel verhärtet"],
                  ["Knochenbruch", "Knochen gebrochen", "starker Schmerz, Fehlstellung, nicht belastbar"]])
    v += abschnitt("B", "Wie Verletzungen entstehen")
    v += P("Viele Verletzungen haben mehrere Ursachen gleichzeitig: fehlendes Aufwärmen, Müdigkeit am Ende der Stunde, "
           "unpassende Schuhe, Übermut, harte Fouls oder Schmuck. Auch wer nach einer Verletzung zu früh wieder einsteigt, "
           "verletzt sich oft erneut an derselben Stelle.")
    v += abschnitt("C", "Vorbeugen")
    v += kacheln([
        ("#d9efd8", "Aufwärmen", "", "Muskeln und Gelenke auf die Belastung vorbereiten, passend zur Sportart."),
        ("#dbe8f5", "Ausrüstung", "", "Feste Hallenschuhe, kein Schmuck, Brille nur als Sportbrille."),
        ("#fbe9c2", "Kräftigen", "", "Starke Muskeln stabilisieren Gelenke, etwa Wadenmuskeln das Sprunggelenk."),
        ("#f6d9d6", "Fair spielen", "", "Viele Verletzungen im Spiel entstehen durch Fouls und Rücksichtslosigkeit."),
    ])
    v += abschnitt("D", "Zurück zum Sport")
    v += P("Erst wenn die verletzte Stelle schmerzfrei ist und normal belastet werden kann, steigt man langsam wieder ein. "
           "Bei Bänderrissen und Brüchen entscheidet der Arzt. Wer im Unterricht zuschaut, kann trotzdem viel lernen.")

    v += abschnitt("E", "Unfälle melden")
    v += P("Jeder Unfall im Schulsport wird der Lehrkraft gemeldet, auch wenn er klein wirkt. Schüler sind in der Schule gesetzlich unfallversichert. "
           "Damit die Versicherung zahlt, zum Beispiel für Arzt oder Physiotherapie, muss der Unfall aufgeschrieben werden.")
    a = [
        aufgabe(1, 0, "Welche Verletzung ist es? Ordne zu.",
                zuordnen(L, ["Prellung", "Verstauchung", "Zerrung", "Knochenbruch"], [
                    ("Nach einem Zusammenstoß ein blauer Fleck am Oberschenkel.", "A"),
                    ("Beim Sprint plötzlich ein ziehender Schmerz hinten im Oberschenkel.", "C"),
                    ("Der Unterarm ist schief und kann nicht bewegt werden.", "D"),
                    ("Umgeknickt, das Sprunggelenk schwillt an, Gehen geht noch.", "B")])),
        aufgabe(2, 0, "Nenne vier Ursachen für Sportverletzungen.",
                felder(L, [("1", "kein Aufwärmen"), ("2", "Müdigkeit"), ("3", "falsche Schuhe"), ("4", "Fouls")], 4, 34)),
        aufgabe(3, 1, "Warum stabilisieren kräftige Wadenmuskeln das Sprunggelenk?",
                linien(L, 2, "Starke Muskeln halten das Gelenk fest und fangen ein Umknicken besser ab. Die Bänder werden entlastet.")),
        aufgabe(4, 1, "Wann darf man nach einer Verstauchung wieder voll mitmachen?",
                linien(L, 2, "Wenn die Stelle schmerzfrei ist und normal belastet werden kann. Dann langsam wieder einsteigen.")),
        aufgabe(5, 2, "Viele Verletzungen passieren am Ende einer Doppelstunde. Erkläre, warum, und nenne zwei Maßnahmen dagegen.",
                linien(L, 4, "Am Ende sind die Schüler müde, Konzentration und Kraft lassen nach, sie werden unvorsichtig. "
                             "Maßnahmen: Pausen und Trinken einplanen, am Ende ruhigere Übungen statt wilder Spiele.")),
        aufgabe(6, 1, "Warum sollte man jeden Sportunfall in der Schule der Lehrkraft melden, auch wenn er klein wirkt?",
                linien(L, 3, "Manche Verletzungen zeigen sich erst später. Schüler sind versichert, aber nur, wenn der Unfall gemeldet und aufgeschrieben ist.")),
        aufgabe(7, 2, "Ein Mitschüler hat Schmerzen im Knöchel und will trotzdem mitspielen. Was rätst du ihm? Begründe.",
                linien(L, 3, "Er soll aussetzen und die PECH-Regel anwenden. Mit Schmerzen weiterzuspielen kann die Verletzung schlimmer machen, "
                             "dann fällt er viel länger aus.")),
    ]
    return blatt(VZ, 1, "Sportverletzungen erkennen", v,
                 ["Prellung, Verstauchung, Bänderriss, Zerrung, Bruch unterscheiden.",
                  "Aufwärmen, Ausrüstung, Kräftigung und Fairness beugen vor.",
                  "Erst schmerzfrei wieder einsteigen."], a)


def vz2(L):
    v = abschnitt("A", "Erste Hilfe bei Sportverletzungen: PECH")
    v += P("Bei Prellungen, Verstauchungen und Zerrungen gilt die PECH-Regel. Ziel ist, die Schwellung und den Bluterguss klein zu halten. "
           "Je weniger es anschwillt, desto schneller heilt die Verletzung.")
    v += tabelle(["Schritt", "Was tun?", "Warum?"],
                 [["P Pause", "Sofort aufhören, nicht weitermachen", "Weitere Belastung vergrößert die Verletzung."],
                  ["E Eis", "Kühlen mit Kühlpack oder kaltem Wasser, nie direkt auf die Haut, etwa 15 bis 20 Minuten", "Die Blutgefäße ziehen sich zusammen, es blutet weniger ins Gewebe."],
                  ["C Compression", "Elastischen Verband mäßig fest anlegen", "Der Druck begrenzt die Schwellung."],
                  ["H Hochlagern", "Verletzte Stelle über Herzhöhe lagern", "Blut und Gewebeflüssigkeit fließen besser ab."]])
    v += abschnitt("B", "Notruf 112")
    v += P("Bei schweren Verletzungen, Bewusstlosigkeit oder starken Blutungen ruft man den Rettungsdienst unter <b>112</b>. "
           "Der Anruf ist kostenlos und funktioniert auch ohne Guthaben. Am Telefon helfen die <b>W-Fragen</b>:")
    v += P("<b>Wo</b> ist es passiert? (Adresse, Sporthalle, Eingang)<br>"
           "<b>Was</b> ist passiert?<br>"
           "<b>Wie viele</b> Verletzte?<br>"
           "<b>Welche</b> Verletzungen?<br>"
           "<b>Warten</b> auf Rückfragen, nicht selbst auflegen.")
    v += abschnitt("C", "Weitere Notfälle in der Halle")
    v += P("<b>Nasenbluten:</b> Kopf nach vorne, Nasenflügel zusammendrücken, Nacken kühlen.<br>"
           "<b>Kopfverletzung:</b> Bei Übelkeit, Schwindel, Kopfschmerz oder Erinnerungslücken nach einem Stoß gegen den Kopf "
           "darf man nicht weitermachen. Das kann eine Gehirnerschütterung sein, ein Arzt muss nachsehen.<br>"
           "<b>Kreislaufprobleme:</b> Hinlegen, Beine hoch, frische Luft, etwas trinken.")

    a = [
        aufgabe(1, 0, "Ergänze die PECH-Regel.",
                felder(L, [("P", "Pause"), ("E", "Eis"), ("C", "Compression"), ("H", "Hochlagern")], 4, 34)),
        aufgabe(2, 0, "Ordne den Schritten der PECH-Regel die Begründung zu.",
                zuordnen(L, ["weniger Blutung ins Gewebe", "Druck begrenzt die Schwellung", "Flüssigkeit fließt besser ab", "Verletzung wird nicht größer"], [
                    ("Pause", "D"), ("Eis", "A"), ("Compression", "B"), ("Hochlagern", "C")])),
        aufgabe(3, 0, "Welche W-Fragen beantwortest du beim Notruf?",
                felder(L, [("1", "Wo?"), ("2", "Was?"), ("3", "Wie viele?"), ("4", "Welche Verletzungen?"), ("5", "Warten!")], 5, 26)),
        aufgabe(4, 1, "Warum legt man Eis nie direkt auf die Haut?",
                linien(L, 1, "Es kann zu Erfrierungen der Haut kommen.")),
        aufgabe(5, 1, "Ein Spieler prallt beim Kopfball mit einem anderen zusammen. Danach ist ihm schwindelig. Was tust du?",
                linien(L, 2, "Er darf nicht weiterspielen. Lehrkraft holen, hinsetzen lassen, beobachten. Verdacht auf Gehirnerschütterung, Arzt.")),
        aufgabe(6, 2, "Spiele einen Notruf durch: Ein Schüler ist in der Sporthalle vom Kasten gestürzt und reagiert nicht. Schreibe auf, was du sagst.",
                linien(L, 4, "Wo: Sporthalle der Schule, Adresse, Eingang. Was: Sturz vom Kasten aus etwa einem Meter. Wie viele: ein Verletzter. "
                             "Welche Verletzungen: reagiert nicht, atmet. Dann warten, bis die Leitstelle auflegt.")),
        aufgabe(7, 2, "Warum muss man bei Kopfverletzungen besonders vorsichtig sein? Was sind Warnzeichen?",
                linien(L, 3, "Das Gehirn kann verletzt sein, auch wenn man außen nichts sieht. Warnzeichen: Übelkeit, Schwindel, Kopfschmerz, "
                             "Erinnerungslücken. Dann nicht weiterspielen und zum Arzt.")),
    ]
    return blatt(VZ, 2, "Erste Hilfe und Notruf", v,
                 ["PECH: Pause, Eis, Compression, Hochlagern.",
                  "Notruf 112 mit den W-Fragen, auf Rückfragen warten.",
                  "Nach Stoß gegen den Kopf mit Beschwerden: nicht weiterspielen."], a)


def vz3(L):
    v = abschnitt("A", "Warum helfen und sichern?")
    v += P("Beim Turnen und im Parcours werden Bewegungen geübt, bei denen man stürzen kann: Überschläge, Sprünge über den Kasten, "
           "Aufschwünge am Reck. Mit Hilfestellung traut man sich mehr und lernt schneller. Gleichzeitig wird das Risiko kleiner.")
    v += P("Man unterscheidet zwei Aufgaben. Wer <b>hilft</b>, unterstützt die Bewegung aktiv, etwa durch Schieben oder Drehen. "
           "Wer <b>sichert</b>, greift nur ein, wenn etwas schiefgeht.")
    v += abschnitt("B", "Griffe")
    v += kacheln([
        ("#dbe8f5", "Klammergriff", "", "Beide Hände umfassen den Oberarm des Turners, eine Hand oben, eine unten. Sehr sicher, z. B. beim Hocksprung über den Kasten."),
        ("#d9efd8", "Stützgriff", "", "Eine Hand schiebt am Rücken oder an der Hüfte, die andere stützt am Oberschenkel, z. B. beim Aufschwung am Reck."),
        ("#fbe9c2", "Drehgriff", "", "Die Hände unterstützen eine Drehung, eine Hand am Rücken, eine am Bauch oder Oberarm, z. B. bei der Rolle am Barren."),
    ], cols=3)
    v += abschnitt("C", "Regeln für Helfer")
    v += P("1. Nah am Gerät stehen, auf der richtigen Seite.<br>"
           "2. Den Turner mit den Augen begleiten, nicht wegschauen.<br>"
           "3. Fest zugreifen und erst loslassen, wenn er sicher steht.<br>"
           "4. Nur helfen, wenn man den Griff von der Lehrkraft gelernt hat.<br>"
           "5. Kein Quatsch: Der Turner vertraut dir.")
    v += abschnitt("D", "Parcours sicher gestalten")
    v += P("Im Parcours werden Hindernisse überwunden: springen, klettern, balancieren, rollen. "
           "Matten liegen ohne Lücken, Geräte sind fest verbunden, und es läuft immer nur einer durch eine Station. "
           "Wer wartet, steht außerhalb der Lauf- und Landezone.")

    v += abschnitt("E", "Fallen lernen")
    v += P("Wer richtig fallen kann, verletzt sich seltener. Statt sich mit steifen Armen abzustützen, rollt man über die Schulter ab "
           "oder fängt sich mit leicht gebeugten Armen ab. Im Turnen, Parcours und Judo wird das gezielt geübt.")
    a = [
        aufgabe(1, 0, "Was ist der Unterschied zwischen Helfen und Sichern?",
                linien(L, 2, "Helfen: die Bewegung aktiv unterstützen. Sichern: nur eingreifen, wenn etwas schiefgeht.")),
        aufgabe(2, 0, "Welcher Griff passt? Ordne zu.",
                zuordnen(L, ["Klammergriff", "Stützgriff", "Drehgriff"], [
                    ("Hocksprung über den Kasten", "A"), ("Aufschwung am Reck", "B"), ("Rolle am Barren", "C")])),
        aufgabe(3, 1, "Zeichne den Klammergriff: Turner (Strichmännchen) am Kasten, Helfer daneben mit beiden Händen am Oberarm.",
                karo(L, 30, "Helfer seitlich am Kastenende, beide Hände umfassen den Oberarm des Turners")),
        aufgabe(4, 2, "Plane eine Parcours-Station mit drei Hindernissen. Beschreibe Aufbau und Sicherheitsmaßnahmen.",
                linien(L, 4, "Kasten zum Überspringen mit Matte dahinter, Langbank zum Balancieren, Weichboden zum Abrollen. "
                             "Matten ohne Lücken, Geräte fest verbunden, nur einer gleichzeitig, Wartende hinter einer Linie.")),
        aufgabe(5, 2, "Warum ist es wichtig, Fallen und Abrollen zu üben? Beschreibe eine Situation im Sport, in der das hilft.",
                linien(L, 3, "Mit steifen Armen bricht man sich leicht das Handgelenk. Wer abrollt, verteilt den Aufprall. Beispiel: beim Basketball "
                             "nach einem Zusammenstoß über die Schulter abrollen.")),
        aufgabe(6, 2, "Wähle eine Turnübung. Beschreibe, wo der Helfer steht, wie er greift und wann er loslässt.",
                linien(L, 4, "Hocksprung über den Kasten: Der Helfer steht seitlich am Kastenende, greift mit dem Klammergriff den Oberarm "
                             "und begleitet den Turner bis zur Landung. Er lässt erst los, wenn der Turner sicher steht.")),
    ]
    return blatt(VZ, 3, "Helfen und Sichern", v,
                 ["Helfen unterstützt die Bewegung, Sichern greift nur im Notfall ein.",
                  "Klammergriff, Stützgriff, Drehgriff.",
                  "Fest zugreifen, Turner im Blick, erst loslassen, wenn er sicher steht."], a)


# ================================================================== Regeln und Spielfeld
RS = "Regeln und Spielfeld"


def rs1(L):
    v = abschnitt("A", "Das Spielfeld")
    v += P("Basketball wird auf einem <b>28 m langen</b> und <b>15 m breiten</b> Feld gespielt. Die Körbe hängen in <b>3,05 m</b> Höhe.")
    v += f'<div style="width:140mm;margin:1mm auto 1mm auto">{basketballfeld(True)}</div>'
    v += abschnitt("B", "Punkte")
    v += P("Ein Korb aus dem Spiel zählt <b>2 Punkte</b>, von hinter der Dreipunktelinie (6,75 m) <b>3 Punkte</b>, "
           "ein Freiwurf <b>1 Punkt</b>. Freiwürfe gibt es vor allem nach einem Foul beim Wurf.")
    v += abschnitt("C", "Die wichtigsten Regeln")
    v += P("<b>Mannschaft:</b> 5 Spieler auf dem Feld, beliebig viele Wechsel.<br>"
           "<b>Schrittfehler:</b> Mit dem Ball in der Hand darf man nur mit einem Fuß (Standbein) am Boden drehen, nicht laufen.<br>"
           "<b>Doppeldribbling:</b> Wer aufhört zu dribbeln, darf nicht wieder anfangen. Mit beiden Händen gleichzeitig dribbeln ist verboten.<br>"
           "<b>3 Sekunden:</b> Ein Angreifer darf nicht länger als 3 Sekunden in der Zone stehen.<br>"
           "<b>24 Sekunden:</b> So viel Zeit hat ein Team, um auf den Korb zu werfen.<br>"
           "<b>Kontakt:</b> Basketball ist ein körperloses Spiel. Halten, Stoßen, Schlagen sind Fouls. "
           "Nach 5 persönlichen Fouls muss ein Spieler vom Feld.")

    v += abschnitt("D", "Verteidigung")
    v += P("Bei der <b>Mann-Mann-Verteidigung</b> deckt jeder Spieler einen bestimmten Gegner. Bei der <b>Zonenverteidigung</b> ist jeder für einen Bereich "
           "zuständig und deckt den Gegner, der gerade dort ist. Die Zone schützt den Korb gut, ist aber anfällig für Distanzwürfe.")
    a = [
        aufgabe(1, 0, "Beschrifte das Feld.",
                f'<div style="width:112mm;margin:0 auto 1.5mm auto">{basketballfeld(False)}</div>'
                + felder(L, [("A", "Zone"), ("B", "Freiwurflinie"), ("C", "Dreipunktelinie"), ("D", "Mittellinie"), ("E", "Korb")], 5, 30)),
        aufgabe(2, 0, "Wie viele Punkte gibt es?",
                felder(L, [("Korbleger", "2"), ("Wurf von 7 m", "3"), ("Freiwurf", "1"), ("Wurf von 5 m", "2")], 4, 20)),
        aufgabe(3, 1, "Welche Regel wurde verletzt?",
                zuordnen(L, ["Schrittfehler", "Doppeldribbling", "3 Sekunden", "Foul"], [
                    ("Ein Spieler läuft mit dem Ball unter dem Arm zwei Schritte.", "A"),
                    ("Ein Angreifer wartet lange in der Zone auf den Ball.", "C"),
                    ("Ein Spieler hält den Gegner am Trikot fest.", "D"),
                    ("Ein Spieler fängt seinen Dribbelball und dribbelt weiter.", "B")])),
        aufgabe(4, 2, "Warum gibt es die 24-Sekunden-Regel? Was würde ohne sie passieren?",
                linien(L, 2, "Ohne sie könnte ein führendes Team den Ball ewig halten. Die Regel sorgt für ein schnelles, angriffslustiges Spiel.")),
        aufgabe(5, 2, "Erkläre den Unterschied zwischen Mann-Mann-Verteidigung und Zonenverteidigung. Wann ist welche sinnvoll?",
                linien(L, 3, "Mann-Mann: jeder deckt einen Gegner, gut gegen gute Einzelspieler. Zone: jeder deckt einen Bereich, gut gegen Spieler, "
                             "die unter den Korb ziehen, schlecht gegen gute Distanzwerfer.")),
    ]
    return blatt(RS, 1, "Basketball", v,
                 ["Feld 28 m mal 15 m, Korb in 3,05 m Höhe.",
                  "2 Punkte, 3 Punkte, 1 Punkt beim Freiwurf.",
                  "Schrittfehler, Doppeldribbling, 3 Sekunden, 24 Sekunden."], a)


def rs2(L):
    v = abschnitt("A", "Das Feld")
    v += P("Badminton spielt man mit Schläger und Federball über ein Netz. Das Feld ist <b>13,40 m lang</b>. "
           "Im Doppel ist es <b>6,10 m</b> breit, im Einzel etwas schmaler. Das Netz hängt in der Mitte auf gut <b>1,52 m</b> Höhe.")
    v += f'<div style="width:155mm;margin:1mm auto 1mm auto">{badmintonfeld()}</div>'
    v += abschnitt("B", "Zählen")
    v += P("Jeder Ballwechsel bringt einen Punkt, egal wer aufgeschlagen hat. Ein Satz geht bis <b>21 Punkte</b>. "
           "Man braucht 2 Punkte Vorsprung, höchstens wird bis 30 gespielt. Gewonnen hat, wer zuerst <b>zwei Sätze</b> gewinnt.")
    v += abschnitt("C", "Der Aufschlag")
    v += P("Der Aufschlag wird <b>diagonal</b> ins gegenüberliegende Aufschlagfeld gespielt. Der Ball wird unterhalb der Hüfte getroffen, "
           "der Schläger zeigt dabei nach unten. Hat der Aufschläger eine gerade Punktzahl, schlägt er von rechts auf, bei ungerader von links. "
           "Wer den Punkt gewinnt, hat den nächsten Aufschlag.")
    v += abschnitt("D", "Fehler")
    v += P("Ein Punkt geht an den Gegner, wenn der Ball im Aus landet, im Netz hängen bleibt oder darunter durchfliegt, "
           "wenn man das Netz berührt oder den Ball zweimal hintereinander schlägt. Linienbälle sind gut.")
    v += abschnitt("E", "Schläge")
    v += P("<b>Clear:</b> hoch und weit bis an die Grundlinie. <b>Drop:</b> kurz und langsam knapp hinter das Netz. "
           "<b>Smash:</b> hart und steil nach unten.")

    v += abschnitt("F", "Taktik im Einzel")
    v += P("Wer den Gegner laufen lässt, gewinnt oft. Man spielt abwechselnd hoch nach hinten und kurz ans Netz und zielt in die Ecken. "
           "Wichtig ist, nach jedem Schlag wieder in die Mitte des Feldes zurückzugehen.")
    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Ein Satz geht bis {} Punkte. Gewonnen hat, wer {} Sätze gewinnt. Der Aufschlag geht {}. "
                "Bei gerader Punktzahl schlägt man von {} auf.",
                ["21", "zwei", "diagonal", "rechts"], ["rechts", "21", "diagonal", "zwei"], 24)),
        aufgabe(2, 1, "Welcher Schlag passt? Schreibe Clear, Drop oder Smash.",
                felder(L, [("Gegner steht weit hinten", "Drop"), ("Ball kommt hoch und kurz", "Smash"),
                           ("Zeit gewinnen, Gegner nach hinten treiben", "Clear")], 3, 40)),
        aufgabe(3, 1, "Spielstand 20 : 19. Wer kann den Satz gewinnen? Was passiert bei 20 : 20?",
                linien(L, 2, "Der Spieler mit 20 gewinnt mit dem nächsten Punkt (21 : 19). Bei 20 : 20 braucht man 2 Punkte Vorsprung, höchstens bis 30.")),
        aufgabe(4, 2, "Dein Gegner steht nah am Netz. Welchen Schlag spielst du und warum?",
                linien(L, 2, "Einen Clear, hoch und weit nach hinten. Er muss weit zurücklaufen und hat es schwer, den Ball zu erreichen.")),
        aufgabe(5, 1, "Der Aufschläger hat 7 Punkte. Von welcher Seite schlägt er auf? Und mit 8 Punkten?",
                linien(L, 1, "7 ist ungerade: von links. 8 ist gerade: von rechts.")),
        aufgabe(6, 2, "Beschreibe eine Taktik, mit der du einen Gegner im Einzel ins Laufen bringst. Warum funktioniert sie?",
                linien(L, 3, "Abwechselnd Clear in die hintere Ecke und Drop ans Netz in die andere Ecke. Der Gegner muss weite Wege laufen, "
                             "wird müde und macht Fehler.")),
        aufgabe(7, 1, "Erkläre die Zählweise einem Mitschüler: Wann ist ein Satz gewonnen, wann das ganze Spiel?",
                linien(L, 3, "Jeder Ballwechsel bringt einen Punkt. Einen Satz gewinnt, wer 21 Punkte mit 2 Punkten Vorsprung hat, spätestens bei 30. "
                             "Das Spiel gewinnt, wer zuerst zwei Sätze hat.")),
        aufgabe(8, 2, "Beschreibe den Aufschlag so genau, dass ein Anfänger ihn regelgerecht ausführen kann.",
                linien(L, 4, "Im richtigen Aufschlagfeld stehen, bei gerader Punktzahl rechts. Den Ball unterhalb der Hüfte treffen, Schläger zeigt nach unten. "
                             "Diagonal ins gegenüberliegende Feld spielen, hinter die vordere Aufschlaglinie.")),
    ]
    return blatt(RS, 2, "Badminton", v,
                 ["Satz bis 21, zwei Gewinnsätze, jeder Ballwechsel zählt.",
                  "Aufschlag diagonal und unterhalb der Hüfte.",
                  "Clear hoch und weit, Drop kurz, Smash steil."], a)


def rs3(L):
    v = abschnitt("A", "Grundregeln")
    v += P("Beim Fußball spielen zwei Mannschaften mit je <b>11 Spielern</b> (10 Feldspieler und ein Torwart). "
           "Das Tor ist 7,32 m breit und 2,44 m hoch. Ein Spiel dauert bei Erwachsenen zweimal 45 Minuten. "
           "Den Ball darf nur der Torwart in seinem Strafraum mit der Hand spielen.")
    v += abschnitt("B", "Strafen")
    v += tabelle(["Vergehen", "Strafe"],
                 [["Foul, Handspiel", "direkter Freistoß für den Gegner"],
                  ["Foul oder Handspiel im eigenen Strafraum", "Strafstoß (Elfmeter) aus 11 m"],
                  ["unsportliches Verhalten, wiederholtes Foulspiel", "Gelbe Karte"],
                  ["grobes Foulspiel, Tätlichkeit, zweite Gelbe Karte", "Rote Karte, Platzverweis"]])
    v += abschnitt("C", "Abseits")
    v += P("Die Abseitsregel verhindert, dass ein Angreifer einfach vor dem Tor wartet. Ein Spieler steht im <b>Abseits</b>, "
           "wenn er im Moment der Ballabgabe durch einen Mitspieler")
    v += P("1. in der gegnerischen Hälfte steht <b>und</b><br>"
           "2. näher an der gegnerischen Torlinie ist als der Ball <b>und</b><br>"
           "3. näher an der Torlinie ist als der vorletzte Gegenspieler (meistens ist der letzte der Torwart).")
    v += f'<div style="width:118mm;margin:1mm auto 1mm auto">{abseits()}</div>'
    v += P("Im Bild spielt B den Ball zu A. A ist im Moment des Passes näher am Tor als der Verteidiger: Abseits. "
           "Abseits ist nur strafbar, wenn der Spieler ins Spiel eingreift. Bei Einwurf, Abstoß und Eckstoß gibt es kein Abseits.")

    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Eine Mannschaft hat {} Spieler auf dem Feld. Ein Elfmeter wird aus {} geschossen. "
                "Nach zwei Gelben Karten gibt es {}.",
                ["11", "11 m", "Gelb-Rot (Platzverweis)"], ["Gelb-Rot (Platzverweis)", "11", "11 m"], 42)),
        aufgabe(2, 0, "Welche Strafe gibt es? Ordne zu.",
                zuordnen(L, ["direkter Freistoß", "Elfmeter", "Gelbe Karte", "Rote Karte"], [
                    ("Ein Verteidiger foult im eigenen Strafraum.", "B"),
                    ("Ein Spieler schlägt einen Gegner.", "D"),
                    ("Ein Spieler meckert ständig beim Schiedsrichter.", "C"),
                    ("Ein Spieler stellt im Mittelfeld ein Bein.", "A")])),
        aufgabe(3, 1, "Abseits oder nicht? Kreuze an, wenn es Abseits ist.", richtig_falsch(L, [
            ("Der Angreifer steht beim Pass in der eigenen Hälfte.", False),
            ("Der Angreifer ist beim Pass näher am Tor als alle Verteidiger, nur der Torwart ist hinter ihm.", True),
            ("Der Angreifer bekommt den Ball direkt aus einem Einwurf.", False),
            ("Der Angreifer steht gleichauf mit dem vorletzten Verteidiger.", False)]).replace(">richtig<", ">Abseits<").replace(">falsch<", ">kein Abseits<")),
        aufgabe(4, 1, "Zeichne eine Situation, in der ein Angreifer NICHT im Abseits steht. Zeichne Tor, Torwart, einen Verteidiger und zwei Angreifer.",
                karo(L, 30, "Angreifer, der den Ball bekommt, steht beim Pass gleichauf oder hinter dem Verteidiger")),
        aufgabe(5, 2, "Warum gibt es die Abseitsregel? Wie würde Fußball ohne sie aussehen?",
                linien(L, 2, "Ohne Abseits würden Angreifer vor dem gegnerischen Tor warten und lange Bälle bekommen. Das Spiel wäre weniger kombinationsreich.")),
        aufgabe(6, 2, "Erkläre einem Mitschüler die Abseitsregel in eigenen Worten mit einem Beispiel.",
                linien(L, 4, "Wenn ein Mitspieler den Ball spielt, darf ich in der gegnerischen Hälfte nicht näher am Tor stehen als der vorletzte Gegner. "
                             "Beispiel: Ich stehe allein hinter dem letzten Verteidiger, nur der Torwart ist noch hinter mir, dann bin ich im Abseits.")),
    ]
    return blatt(RS, 3, "Fußball", v,
                 ["11 Spieler, nur der Torwart darf im Strafraum die Hand nehmen.",
                  "Foul im Strafraum: Elfmeter.",
                  "Abseits: beim Pass näher am Tor als der vorletzte Gegner."], a)


def handball_positionen(beschriftet=True):
    """Angriffspositionen in einer Spielfeldhälfte (Tor oben)."""
    k, m = 9, 12  # 20 m breit, 15 m tief gezeigt
    W, H = 20 * k, 15 * k
    xc = m + W / 2
    y0 = m
    pf = 1.5 * k
    o = [f'<svg viewBox="0 0 {W+2*m} {H+2*m}" width="100%" {SVG}>',
         f'<defs><clipPath id="hh"><rect x="{m}" y="{m}" width="{W}" height="{H}"/></clipPath></defs>',
         f'<rect x="{m}" y="{m}" width="{W}" height="{H}" fill="#6fa8dc" stroke="#fff" stroke-width="2.5"/>',
         '<g clip-path="url(#hh)">']
    for r, strich in ((6 * k, ""), (9 * k, 'stroke-dasharray="7 6"')):
        o.append(f'<path d="M{xc-pf-r} {y0} A{r} {r} 0 0 0 {xc-pf} {y0+r} L{xc+pf} {y0+r} A{r} {r} 0 0 0 {xc+pf+r} {y0}" '
                 f'fill="none" stroke="#fff" stroke-width="2.2" {strich}/>')
    o.append('</g>')
    o.append(f'<rect x="{xc-pf}" y="{y0-k}" width="{2*pf}" height="{k}" fill="#e8706a" stroke="#333"/>')
    pos = [("TW", xc, y0 + 1.5 * k), ("LA", m + 1.6 * k, y0 + 2.5 * k), ("RA", m + W - 1.6 * k, y0 + 2.5 * k),
           ("KM", xc + 1.5 * k, y0 + 6.6 * k), ("RL", xc - 6.8 * k, y0 + 10.5 * k), ("RM", xc, y0 + 11.6 * k),
           ("RR", xc + 6.8 * k, y0 + 10.5 * k)]
    for t, x, y in pos:
        farbe = "#e8706a" if t == "TW" else "#1f6fb2"
        o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{farbe}"/>')
        if beschriftet:
            o.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="#fff" font-size="9.5">{t}</text>')
    o.append("</svg>")
    return "".join(o)


def rs4(L):
    v = abschnitt("A", "Die Positionen im Angriff")
    v += P("Eine Handballmannschaft besteht aus einem Torwart und sechs Feldspielern. Im Angriff hat jeder Spieler eine feste Position:")
    v += ('<div class="zwei" style="align-items:flex-start"><div style="flex:0 0 62mm">' + handball_positionen(True) + '</div><div>'
          + tabelle(["Kürzel", "Position", "Aufgabe"],
                    [["TW", "Torwart", "hält Würfe, leitet mit langen Pässen Gegenstöße ein"],
                     ["LA / RA", "Linksaußen / Rechtsaußen", "schnell, werfen aus spitzem Winkel, laufen Gegenstöße"],
                     ["RL / RR", "Rückraum links / rechts", "groß und wurfstark, werfen aus 9 m und mehr"],
                     ["RM", "Rückraum Mitte", "Spielmacher, sagt Spielzüge an, verteilt die Bälle"],
                     ["KM", "Kreisläufer", "steht am Torraum zwischen den Abwehrspielern, stellt Sperren, fängt Pässe"]])
          + '</div></div>')
    v += abschnitt("B", "Abwehrformationen")
    v += P("In der Abwehr stellen sich die sechs Feldspieler vor dem eigenen Torraum auf. Die häufigsten Formationen sind:<br>"
           "<b>6:0</b>: Alle sechs stehen nebeneinander nah am Torraum. Das schützt vor Würfen vom Kreis, Rückraumwürfe sind aber leichter.<br>"
           "<b>5:1</b>: Fünf stehen am Torraum, einer steht weiter vorne und stört den Spielmacher.<br>"
           "<b>3:2:1</b>: Die Abwehr steht gestaffelt und offensiv. Sie stört früh und will Bälle abfangen, lässt aber Lücken.")
    v += abschnitt("C", "Weitere wichtige Regeln")
    v += P("<b>Spielzeit:</b> Bei Erwachsenen zweimal 30 Minuten, bei Jugendlichen kürzer.<br>"
           "<b>Anwurf:</b> Nach jedem Tor wirft die Mannschaft, die das Tor kassiert hat, in der Mitte an. Das macht Handball sehr schnell.<br>"
           "<b>Freiwurf:</b> Nach einem Foul nah am Tor wird an der 9-m-Linie ausgeführt, die Abwehr muss 3 m Abstand halten.<br>"
           "<b>Passives Spiel:</b> Wer nur den Ball hin und her spielt, ohne aufs Tor zu gehen, bekommt ein Warnzeichen (Arm gehoben). "
           "Danach bleiben höchstens vier Pässe bis zum Wurf, sonst bekommt der Gegner den Ball.<br>"
           "<b>Zeitstrafe:</b> Bei groben Fouls oder Unsportlichkeit muss ein Spieler 2 Minuten vom Feld, seine Mannschaft spielt so lange in Unterzahl.")
    v += abschnitt("D", "Gegenstoß")
    v += P("Die schnellste Art, ein Tor zu erzielen, ist der Gegenstoß. Sobald die Abwehr den Ball erobert, sprinten die Außen nach vorne, "
           "und der Torwart spielt einen langen Pass. Bevor sich die gegnerische Abwehr ordnen kann, steht der Werfer schon allein vor dem Tor.")
    a = [
        aufgabe(1, 0, "Schreibe zu jedem Kürzel die Position.",
                felder(L, [("TW", "Torwart"), ("LA", "Linksaußen"), ("RM", "Rückraum Mitte"), ("KM", "Kreisläufer"),
                           ("RR", "Rückraum rechts"), ("RA", "Rechtsaußen")], 3, 44)),
        aufgabe(2, 0, "Welche Entscheidung trifft der Schiedsrichter? Ordne zu.",
                zuordnen(L, ["Freiwurf", "Siebenmeter", "2 Minuten Zeitstrafe", "Ballverlust wegen passiven Spiels"], [
                    ("Ein Spieler hält den Gegner im Mittelfeld kurz am Arm.", "A"),
                    ("Ein Werfer wird allein vor dem Tor von hinten umgestoßen.", "B"),
                    ("Nach dem Warnzeichen spielt das Team sechs Pässe ohne Wurf.", "D"),
                    ("Ein Spieler beleidigt den Schiedsrichter.", "C")])),
        aufgabe(3, 1, "Erkläre die Aufgaben des Spielmachers (RM) und des Kreisläufers (KM). Warum brauchen sie sich gegenseitig?",
                linien(L, 3, "Der Spielmacher sagt Spielzüge an und verteilt die Bälle. Der Kreisläufer stellt am Torraum Sperren und fängt Pässe. "
                             "Der Spielmacher sucht den Kreisläufer mit Pässen, der Kreisläufer schafft ihm durch Sperren Platz.")),
        aufgabe(4, 1, "Vergleiche die 6:0- und die 3:2:1-Abwehr. Gegen welche Mannschaft würdest du welche einsetzen?",
                linien(L, 3, "6:0 steht nah am Torraum und schützt gegen Kreisläufer, lässt aber Rückraumwürfe zu. 3:2:1 stört früh und fängt Bälle ab, "
                             "hat aber Lücken. Gegen ein Team mit starken Rückraumwerfern die 3:2:1, gegen einen starken Kreisläufer die 6:0.")),
        aufgabe(5, 1, "Warum gibt es die Regel zum passiven Spiel? Was würde ohne sie passieren?",
                linien(L, 3, "Ohne sie könnte ein führendes Team den Ball lange hin und her spielen und Zeit schinden. "
                             "Die Regel zwingt zum Angriff und hält das Spiel spannend.")),
        aufgabe(6, 2, "Beschreibe einen Gegenstoß Schritt für Schritt: von der Balleroberung bis zum Wurf. Wer macht was?",
                linien(L, 4, "Die Abwehr fängt den Ball ab. Sofort sprinten die Außen nach vorne. Der Torwart oder der Abwehrspieler spielt einen langen Pass. "
                             "Der Außen fängt im Laufen, macht höchstens drei Schritte und wirft allein gegen den Torwart.")),
        aufgabe(7, 1, "Zeichne die 6:0-Abwehr ins Karofeld: Torraum, Tor und sechs Abwehrspieler als Kreuze.",
                karo(L, 20, "Halbkreis Torraum, Tor oben, sechs Kreuze nebeneinander direkt vor der 6-m-Linie")),
    ]
    return blatt(RS, 4, "Handball", v,
                 ["Positionen: TW, LA, RA, RL, RM, RR, KM.",
                  "Abwehr 6:0, 5:1 oder 3:2:1, je nach Gegner.",
                  "Passives Spiel, Zeitstrafe, Gegenstoß."], a)


# ------------------------------------------------------------------ Liste
def _e(thema, nr, titel, fn):
    return (f"{STUFE}/{thema}", f"{thema} {nr} – {titel}", fn)


BLAETTER = [
    _e("Essen und Trinken", 1, "Energie und Energiebedarf", et1),
    _e("Essen und Trinken", 2, "Nährwerte lesen", et2),
    _e("Essen und Trinken", 3, "Trinken und Sportgetränke", et3),
    _e("Fair Play", 1, "Formelle und informelle Fairness", fp1),
    _e("Fair Play", 2, "Schiedsrichter sein", fp2),
    _e("Fair Play", 3, "Streit lösen", fp3),
    _e("Herz, Puls und Ausdauer", 1, "Herz und Kreislauf", hp1),
    _e("Herz, Puls und Ausdauer", 2, "Pulsbereiche", hp2),
    _e("Herz, Puls und Ausdauer", 3, "Coopertest verstehen", hp3),
    _e("Training und Erholung", 1, "Die motorischen Fähigkeiten", te1),
    _e("Training und Erholung", 2, "Trainingsprinzipien", te2),
    _e("Training und Erholung", 3, "Schlaf und Erholung", te3),
    _e("Verletzungen vermeiden", 1, "Sportverletzungen erkennen", vz1),
    _e("Verletzungen vermeiden", 2, "Erste Hilfe und Notruf", vz2),
    _e("Verletzungen vermeiden", 3, "Helfen und Sichern", vz3),
    _e("Regeln und Spielfeld", 1, "Basketball", rs1),
    _e("Regeln und Spielfeld", 2, "Badminton", rs2),
    _e("Regeln und Spielfeld", 3, "Fußball", rs3),
    _e("Regeln und Spielfeld", 4, "Handball", rs4),
]
