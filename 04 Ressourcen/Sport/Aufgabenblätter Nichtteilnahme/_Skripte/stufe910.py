"""Blätter Klasse 9 und 10. Bausteine aus baue_blaetter.py, stufe56.py und stufe78.py."""
from baue_blaetter import abschnitt, aufgabe, gap, linien, richtig_falsch
from stufe56 import P, blatt as _blatt, felder, kacheln, karo, lueckentext, reihenfolge, sortieren, zuordnen
from stufe78 import SVG, tabelle

STUFE = "Klasse 9 und 10"


def blatt(*a):
    return _blatt(*a, stufe=STUFE)


# ------------------------------------------------------------------ Grafiken
def volleyballfeld(beschriftet=True):
    k, m = 16, 20  # 18 x 9 m
    W, H = 18 * k, 9 * k
    xn = m + W / 2
    o = [f'<svg viewBox="0 0 {W+2*m} {H+2*m}" width="100%" {SVG}>',
         f'<rect x="{m}" y="{m}" width="{W}" height="{H}" fill="#f2c46b" stroke="#fff" stroke-width="2.5"/>',
         f'<line x1="{xn-3*k}" y1="{m}" x2="{xn-3*k}" y2="{m+H}" stroke="#fff" stroke-width="2"/>',
         f'<line x1="{xn+3*k}" y1="{m}" x2="{xn+3*k}" y2="{m+H}" stroke="#fff" stroke-width="2"/>',
         f'<line x1="{xn}" y1="{m-8}" x2="{xn}" y2="{m+H+8}" stroke="#333" stroke-width="3.5" stroke-dasharray="3 2"/>']
    # Positionen rechte Hälfte, Blick zum Netz nach links: "rechts" aus Spielersicht ist oben im Bild
    pos = {"I": (m + W - 1.5 * k, m + 1.5 * k), "II": (xn + 1.5 * k, m + 1.5 * k), "III": (xn + 1.5 * k, m + H / 2),
           "IV": (xn + 1.5 * k, m + H - 1.5 * k), "V": (m + W - 1.5 * k, m + H - 1.5 * k), "VI": (m + W - 1.5 * k, m + H / 2)}
    if beschriftet:
        for t, (x, y) in pos.items():
            o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#1f6fb2"/><text x="{x}" y="{y+4}" text-anchor="middle" fill="#fff">{t}</text>')
        o += [f'<text x="{xn}" y="{m-11}" text-anchor="middle" fill="#222">Netz</text>',
              f'<text x="{xn-3*k-4}" y="{m+H+14}" text-anchor="end" fill="#222">Angriffslinie (3 m)</text>',
              f'<text x="{m+W/4}" y="{m+H/2+4}" text-anchor="middle" fill="#666">Gegner</text>',
              f'<text x="{m+W/2}" y="{m+H+30}" text-anchor="middle" fill="#333">18 m lang, 9 m breit</text>']
    o.append("</svg>")
    return "".join(o)


def zonen_balken():
    """Energiebereitstellung: Dauer der Belastung und Hauptweg."""
    return ('<svg viewBox="0 0 360 90" width="100%" ' + SVG + '>'
            '<rect x="10" y="10" width="70" height="30" fill="#e8706a"/><text x="45" y="30" text-anchor="middle" fill="#fff">ATP/KP</text>'
            '<rect x="80" y="10" width="110" height="30" fill="#f2c46b"/><text x="135" y="30" text-anchor="middle">anaerob (Laktat)</text>'
            '<rect x="190" y="10" width="160" height="30" fill="#7cc47a"/><text x="270" y="30" text-anchor="middle">aerob (mit Sauerstoff)</text>'
            '<line x1="10" y1="52" x2="350" y2="52" stroke="#333" stroke-width="1.5"/>'
            '<text x="10" y="68" fill="#333">0 s</text><text x="80" y="68" text-anchor="middle" fill="#333">ca. 10 s</text>'
            '<text x="190" y="68" text-anchor="middle" fill="#333">ca. 1 bis 2 min</text><text x="350" y="68" text-anchor="end" fill="#333">Stunden</text>'
            '<text x="180" y="86" text-anchor="middle" fill="#666">Dauer der Belastung</text></svg>')


# ================================================================== Essen und Trinken
ET = "Essen und Trinken"


def et1(L):
    v = abschnitt("A", "Grundumsatz und Leistungsumsatz")
    v += P("Der Körper verbraucht auch im Schlaf Energie: für Herz, Atmung, Gehirn und Körpertemperatur. Das ist der <b>Grundumsatz</b>. "
           "Eine grobe Faustformel: <b>1 kcal pro Kilogramm Körpergewicht und Stunde</b>. Bei 60 kg sind das 60 · 24 = 1440 kcal am Tag. "
           "Muskeln verbrauchen auch in Ruhe mehr Energie als Fettgewebe. Wer muskulöser ist, hat einen höheren Grundumsatz.")
    v += P("Der <b>Leistungsumsatz</b> hängt davon ab, wie aktiv man ist. Man drückt ihn oft mit dem PAL-Wert aus (Physical Activity Level):")
    v += '<div class="box" style="text-align:center;margin:1mm 0 2mm 0;font-weight:600">Gesamtumsatz = Grundumsatz · PAL-Wert</div>'
    v += tabelle(["Lebensstil", "PAL-Wert, etwa"],
                 [["fast nur sitzend, kaum Bewegung", "1,4"], ["Schüler, sitzend mit etwas Bewegung", "1,6"],
                  ["regelmäßig Sport, aktiver Alltag", "1,8"], ["Leistungssport, mehrmals pro Woche hartes Training", "2,0 und mehr"]])
    v += abschnitt("B", "Die Energiebilanz")
    v += P("Ist die Energieaufnahme über das Essen dauerhaft größer als der Gesamtumsatz, ist die Bilanz <b>positiv</b>: "
           "Der Körper legt Fettreserven an. Ist sie <b>negativ</b>, werden Reserven abgebaut. "
           "1 kg Körperfett entspricht rund 7000 kcal. Ein Überschuss von 100 kcal am Tag, etwa ein kleines Glas Cola mehr, "
           "summiert sich über ein Jahr auf über 36 000 kcal.")
    v += abschnitt("C", "Bewegung oder Ernährung?")
    v += P("Abnehmen allein durch Sport ist mühsam: Eine Stunde lockeres Joggen verbraucht bei 60 kg etwa 500 bis 600 kcal, "
           "also so viel wie ein großer Burger. Langfristig wirken beide Seiten zusammen: regelmäßige Bewegung, die auch den Grundumsatz erhöht, "
           "und eine ausgewogene Ernährung ohne große Mengen an Zucker und Snacks. In der Wachstumsphase sind strenge Diäten ungeeignet.")

    v += abschnitt("D", "Energiedichte")
    v += P("Wie viel Energie in einem Lebensmittel steckt, hängt stark von Wasser, Fett und Ballaststoffen ab. "
           "Man spricht von <b>Energiedichte</b>: Energie pro 100 g. Gurke hat etwa 12 kcal pro 100 g, ein Apfel etwa 55, "
           "Vollkornbrot etwa 220, Chips und Schokolade über 500. Lebensmittel mit niedriger Energiedichte füllen den Magen, "
           "sättigen lange und liefern trotzdem wenig Energie. Bei Chips oder Süßigkeiten ist es umgekehrt: Eine kleine Menge liefert sehr viel Energie, "
           "macht aber kaum satt. Wer seine Energiebilanz im Blick behalten will, isst deshalb vor allem Lebensmittel mit niedriger Energiedichte.")
    a = [

        aufgabe(1, 0, "Berechne den Grundumsatz pro Tag mit der Faustformel.",
                felder(L, [("50 kg", "1200 kcal"), ("65 kg", "1560 kcal"), ("80 kg", "1920 kcal")], 3, 40)),
        aufgabe(2, 1, "Berechne den Gesamtumsatz.",
                felder(L, [("60 kg, PAL 1,6", "1440 · 1,6 = 2304 kcal"), ("60 kg, PAL 1,8", "1440 · 1,8 = 2592 kcal"),
                           ("70 kg, PAL 1,4", "1680 · 1,4 = 2352 kcal")], 3, 50)),
        aufgabe(3, 1, "Jemand trinkt jeden Tag zusätzlich 0,33 l Cola (140 kcal). Wie viel Körperfett könnte das in einem Jahr ausmachen? Rechne.",
                linien(L, 2, "140 · 365 = 51 100 kcal. 51 100 : 7000 ≈ 7,3 kg Körperfett, wenn nichts ausgeglichen wird.")),
        aufgabe(4, 1, "Erkläre mit dem Begriff Energiedichte, warum 300 kcal aus Gemüse und Vollkornbrot satter machen als 300 kcal aus Chips.",
                linien(L, 3, "Gemüse und Vollkornbrot haben eine niedrige Energiedichte. Für 300 kcal isst man eine große Menge mit viel Wasser "
                             "und Ballaststoffen, der Magen ist voll. 300 kcal Chips sind nur etwa 55 g, das macht kaum satt.")),
        aufgabe(5, 2, "Schätze deinen eigenen Gesamtumsatz. Gib dein Gewicht (oder 60 kg) und deinen PAL-Wert an und begründe die Wahl.",
                linien(L, 3, "Beispiel: 62 kg · 24 = 1488 kcal. PAL 1,8, weil ich dreimal pro Woche Fußball trainiere. 1488 · 1,8 ≈ 2680 kcal.")),
        aufgabe(6, 2, "„Ich mache einfach mehr Sport, dann kann ich essen, was ich will.“ Nimm Stellung und begründe mit Zahlen aus dem Text.",
                linien(L, 4, "Sport erhöht den Verbrauch, aber weniger als viele denken: Eine Stunde Joggen verbraucht etwa 500 bis 600 kcal, "
                             "so viel wie ein großer Burger. Wer viel isst, gleicht das mit Sport kaum aus. Es braucht Bewegung und ausgewogene Ernährung.")),
        aufgabe(7, 2, "Ein Freund will vor einem Wettkampf schnell abnehmen und nur noch 1000 kcal am Tag essen. "
                      "Erkläre ihm mit Grundumsatz und Energiebilanz, warum das keine gute Idee ist, und mache einen besseren Vorschlag.",
                linien(L, 4, "1000 kcal liegen unter seinem Grundumsatz, der Körper bekommt nicht einmal die Energie für die Grundfunktionen. "
                             "Er baut Muskeln ab und ist im Wettkampf schlapp. Besser: Süßes und Limo weglassen, mehr Gemüse, normale Mahlzeiten.")),
    ]
    return blatt(ET, 1, "Energiebilanz", v,
                 ["Grundumsatz ≈ 1 kcal pro kg und Stunde.",
                  "Gesamtumsatz = Grundumsatz · PAL-Wert.",
                  "1 kg Körperfett ≈ 7000 kcal, kleine Überschüsse summieren sich."], a)


def et2(L):
    v = abschnitt("A", "Kohlenhydrate: der wichtigste Treibstoff")
    v += P("Muskeln speichern Kohlenhydrate als <b>Glykogen</b>, auch die Leber hat einen Vorrat. Diese Speicher reichen bei intensiver Belastung "
           "für etwa 60 bis 90 Minuten. Sind sie leer, sinkt die Leistung stark. Ausdauersportler nennen das „Hungerast“ oder „gegen die Wand laufen“. "
           "Komplexe Kohlenhydrate aus Vollkorn, Kartoffeln und Hülsenfrüchten liefern Energie gleichmäßig über längere Zeit.")
    v += abschnitt("B", "Eiweiß: wie viel ist nötig?")
    v += P("Eiweiß baut Muskeln auf und repariert sie. Jugendliche brauchen etwa <b>0,9 g pro kg Körpergewicht</b> am Tag, "
           "wer viel Kraft- oder Ausdauersport macht, etwas mehr, etwa 1,2 bis 1,5 g. Ein Jugendlicher mit 60 kg braucht also rund 55 bis 90 g. "
           "Diese Menge erreicht man mit normaler Ernährung meist ohne Probleme.")
    v += tabelle(["Lebensmittel", "Eiweiß, etwa"],
                 [["250 g Magerquark", "30 g"], ["100 g Hähnchenbrust", "23 g"], ["2 Eier", "13 g"],
                  ["100 g Linsen (gekocht)", "9 g"], ["0,3 l Milch", "10 g"], ["2 Scheiben Vollkornbrot", "8 g"]])
    v += abschnitt("C", "Nahrungsergänzungsmittel")
    v += P("Proteinpulver, Riegel und Pillen werden oft als nötig für Muskelaufbau beworben. Für Jugendliche, die normal essen, "
           "bringen sie in aller Regel keinen Vorteil. Sie sind teuer, und überschüssiges Eiweiß verbraucht der Körper einfach als Energie. "
           "Bei Präparaten aus dem Internet besteht außerdem die Gefahr verunreinigter oder sogar verbotener Inhaltsstoffe.")
    v += abschnitt("D", "Timing")
    v += P("Die letzte größere Mahlzeit etwa 2 bis 3 Stunden vor dem Sport, danach möglichst innerhalb von 1 bis 2 Stunden eine Mahlzeit "
           "mit Kohlenhydraten und Eiweiß, zum Beispiel Nudeln mit Hackfleischsoße, Quark mit Obst oder Vollkornbrot mit Käse.")

    v += abschnitt("E", "Eisen und Calcium")
    v += P("<b>Eisen</b> wird für den roten Blutfarbstoff gebraucht, der den Sauerstoff transportiert. Fehlt Eisen, ist man schnell müde "
           "und die Ausdauer sinkt. Mädchen haben durch die Monatsblutung einen höheren Bedarf. Eisen steckt in Fleisch, Hülsenfrüchten, "
           "Vollkorn und Haferflocken. Pflanzliches Eisen nimmt der Körper besser auf, wenn gleichzeitig Vitamin C dabei ist, etwa ein Glas Orangensaft "
           "oder Paprika. <b>Calcium</b> macht die Knochen stabil. Bis etwa zum 20. Lebensjahr wird Knochenmasse aufgebaut, "
           "deshalb ist genug Calcium jetzt besonders wichtig. Es steckt in Milchprodukten, grünem Gemüse und calciumreichem Mineralwasser.")
    a = [

        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Kohlenhydrate werden im Muskel als {} gespeichert. Die Speicher reichen bei intensiver Belastung etwa {}. "
                "Jugendliche brauchen etwa {} Eiweiß pro kg Körpergewicht.",
                ["Glykogen", "60 bis 90 Minuten", "0,9 g"], ["0,9 g", "Glykogen", "60 bis 90 Minuten"], 38)),
        aufgabe(2, 1, "Berechne den Eiweißbedarf am Tag.",
                felder(L, [("55 kg, normal aktiv (0,9 g)", "≈ 50 g"), ("70 kg, viel Training (1,2 g)", "84 g"),
                           ("du selbst", "z. B. 60 · 0,9 = 54 g")], 3, 48)),
        aufgabe(3, 1, "Stelle aus der Tabelle einen Tag zusammen, der mindestens 60 g Eiweiß liefert. Rechne nach.",
                linien(L, 2, "2 Scheiben Vollkornbrot (8 g), 0,3 l Milch (10 g), 100 g Hähnchen (23 g), 2 Eier (13 g), 100 g Linsen (9 g) = 63 g")),
        aufgabe(4, 1, "Was passiert bei einem Ausdauerlauf, wenn die Glykogenspeicher leer sind? Wie kann man das verhindern?",
                linien(L, 3, "Die Leistung bricht stark ein, man wird plötzlich schwach („Hungerast“). Vorbeugen: vorher kohlenhydratreich essen, "
                             "bei langen Belastungen unterwegs etwas Zuckerhaltiges essen oder trinken.")),
        aufgabe(5, 1, "Warum ist Eisen für Ausdauersportler wichtig? Wie kann eine Vegetarierin genug Eisen aufnehmen?",
                linien(L, 3, "Eisen braucht man für den Sauerstofftransport im Blut. Ohne genug Eisen sinkt die Ausdauer. Vegetarisch: "
                             "Hülsenfrüchte, Vollkorn, Haferflocken, dazu Vitamin C, z. B. Orangensaft oder Paprika.")),
        aufgabe(6, 2, "Ein Mitschüler will sich für 40 € im Monat Proteinpulver kaufen. Was rätst du ihm? Begründe mit dem Text.",
                linien(L, 3, "Er erreicht seinen Bedarf mit normalem Essen, etwa Quark, Milch, Eier, Linsen. Das Pulver bringt keinen Vorteil, "
                             "ist teuer und kann bei Internetkäufen verunreinigt sein.")),
        aufgabe(7, 2, "Plane die Ernährung für einen Turniertag mit Spielen um 10 und um 14 Uhr. Begründe deine Auswahl.",
                linien(L, 4, "7 Uhr Haferflocken mit Milch und Banane, das füllt die Glykogenspeicher. Zwischen den Spielen kleine, leichte Snacks: "
                             "Vollkornbrot, Obst, viel Wasser, nichts Fettiges. Nach dem Turnier Nudeln mit Soße und Salat zum Auffüllen und Reparieren.")),
    ]
    return blatt(ET, 2, "Ernährung für Sportler", v,
                 ["Kohlenhydrate füllen die Glykogenspeicher.",
                  "Eiweißbedarf etwa 0,9 g pro kg, normales Essen reicht.",
                  "Proteinpulver bringt Jugendlichen meist nichts."], a)


def et3(L):
    v = abschnitt("A", "Körperbilder in den Medien")
    v += P("Auf Social Media sieht man täglich Bilder von scheinbar perfekten Körpern: sehr schlank, stark definiert, ohne jeden Makel. "
           "Viele dieser Bilder sind bearbeitet, mit Filtern verändert oder in besonderer Pose und Beleuchtung aufgenommen. "
           "Manche Influencer verdienen Geld mit Produkten, die sie dabei bewerben. Wer sich ständig mit solchen Bildern vergleicht, "
           "wird leicht unzufrieden mit dem eigenen Körper.")
    v += abschnitt("B", "Crash-Diäten und der Jojo-Effekt")
    v += P("Wer sehr wenig isst, verliert schnell Gewicht. Ein Teil davon ist aber Wasser und Muskulatur. "
           "Der Körper schaltet in eine Art Sparmodus und verbraucht weniger Energie. Isst man danach wieder normal, "
           "nimmt man oft schnell wieder zu, manchmal mehr als vorher. Das nennt man <b>Jojo-Effekt</b>. "
           "Für Jugendliche im Wachstum sind solche Diäten besonders ungünstig: Es fehlen Nährstoffe für Knochen, Muskeln und Gehirn, "
           "und Leistung und Konzentration sinken.")
    v += abschnitt("C", "Was wirklich hilft")
    v += kacheln([
        ("#d9efd8", "Regelmäßig essen", "", "Drei Mahlzeiten, dazu kleine Snacks. Frühstück nicht auslassen."),
        ("#dbe8f5", "Ausgewogen", "", "Viel Gemüse, Obst, Vollkorn, genug Eiweiß, wenig Zucker und Fertigprodukte."),
        ("#fbe9c2", "Bewegung mit Spaß", "", "Sport, der Freude macht, hält man durch. Er stärkt Körper und Stimmung."),
        ("#f6d9d6", "Kritisch bleiben", "", "Bilder hinterfragen, Accounts entfolgen, die einem nicht guttun."),
    ])
    v += abschnitt("D", "Wenn Essen zum Problem wird")
    v += P("Wenn sich die Gedanken ständig um Essen, Kalorien und Gewicht drehen, wenn jemand heimlich isst oder Mahlzeiten ausfallen lässt "
           "oder sich nach dem Essen schuldig fühlt, kann eine Essstörung dahinterstecken. Das ist eine ernsthafte Erkrankung, "
           "für die man sich nicht schämen muss. Hilfe gibt es bei Vertrauenspersonen, Eltern, Lehrkräften, der Schulsozialarbeit "
           "oder beim Hausarzt.")

    v += abschnitt("E", "Muskeln um jeden Preis?")
    v += P("Auch Jungen stehen unter Druck. Fitness-Influencer zeigen extrem muskulöse Körper und werben für Pulver, Pillen und Trainingspläne. "
           "Manche dieser Körper sind nur mit Dopingmitteln wie Anabolika möglich, was selten offen gesagt wird. "
           "Wer sich ständig damit vergleicht, findet sich selbst schnell zu schmal, auch wenn er schon sehr trainiert ist. "
           "Im Extremfall dreht sich das ganze Leben um Training und Essen. Ein gesunder Körper ist nicht der, der am besten aussieht, "
           "sondern der, der leistungsfähig ist, sich gut anfühlt und Freude an Bewegung hat.")
    a = [

        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Viele Bilder auf Social Media sind {}. Nach einer Crash-Diät nimmt man oft schnell wieder zu. Das heißt {}. "
                "Bei einer strengen Diät verliert man auch {}.",
                ["bearbeitet", "Jojo-Effekt", "Muskulatur"], ["Muskulatur", "bearbeitet", "Jojo-Effekt"], 34)),
        aufgabe(2, 1, "Erkläre den Jojo-Effekt in eigenen Worten.",
                linien(L, 3, "Bei sehr wenig Essen spart der Körper Energie und baut auch Muskeln ab. Danach braucht er weniger Energie. "
                             "Isst man wieder normal, nimmt man schnell zu, oft mehr als vorher.")),
        aufgabe(3, 1, "Nenne drei Gründe, warum man Körperbildern auf Social Media nicht trauen sollte, und erkläre einen davon genauer.",
                linien(L, 3, "Filter und Bildbearbeitung, besondere Pose und Licht, Werbung für Produkte. Influencer verdienen Geld mit Produkten, "
                             "deshalb zeigen sie nur Bilder, die zum Kaufen anregen.")),
        aufgabe(4, 2, "Vergleiche: Welchen Druck erzeugen Social-Media-Bilder bei Mädchen, welchen bei Jungen?",
                linien(L, 3, "Mädchen sollen oft möglichst schlank sein, Jungen möglichst muskulös. Beides ist für viele nicht erreichbar "
                             "und führt zu Unzufriedenheit, Diäten oder übermäßigem Training und gefährlichen Mitteln.")),
        aufgabe(5, 2, "Eine Freundin isst seit Wochen kaum noch und spricht nur über Kalorien. Was könntest du tun?",
                linien(L, 4, "In Ruhe ansprechen, ohne Vorwürfe, sagen, dass ich mir Sorgen mache. Ihr vorschlagen, mit einer Vertrauensperson, "
                             "der Schulsozialarbeit oder einem Arzt zu sprechen. Wenn sie nicht will, selbst eine Lehrkraft einweihen.")),
        aufgabe(6, 2, "Gestalte einen kurzen Post (3 bis 4 Sätze) für Jugendliche, der ein gesundes Körperbild fördert.",
                linien(L, 3, "Dein Körper muss nicht aussehen wie ein Filter. Er soll dich tragen, laufen und lachen lassen. "
                             "Iss bunt, beweg dich mit Spaß und vergleiche dich nicht mit bearbeiteten Bildern.")),
        aufgabe(7, 2, "Was macht für dich einen gesunden Körper aus? Schreibe vier bis fünf Sätze.",
                linien(L, 4, "Beispiel: Ein gesunder Körper ist leistungsfähig und fühlt sich gut an. Er bekommt genug Schlaf, Bewegung und Essen. "
                             "Wichtig ist, dass man Freude an Sport hat und nicht ständig an sein Aussehen denkt.")),
    ]
    return blatt(ET, 3, "Körperbild und Diäten", v,
                 ["Viele Körperbilder in den Medien sind bearbeitet.",
                  "Crash-Diäten führen oft zum Jojo-Effekt.",
                  "Bei Essproblemen Hilfe holen, das ist keine Schande."], a)


# ================================================================== Fair Play
FP = "Fair Play"


def fp1(L):
    v = abschnitt("A", "Was ist Doping?")
    v += P("Doping ist die Einnahme verbotener Substanzen oder die Anwendung verbotener Methoden, um die sportliche Leistung zu steigern. "
           "Welche Mittel verboten sind, legt die Welt-Anti-Doping-Agentur <b>WADA</b> in einer Liste fest, die jedes Jahr aktualisiert wird. "
           "In Deutschland ist die Nationale Anti-Doping-Agentur <b>NADA</b> für Kontrollen zuständig.")
    v += tabelle(["Gruppe", "Wirkung", "Nebenwirkungen (Beispiele)"],
                 [["Anabolika (künstliche Hormone)", "mehr Muskelmasse und Kraft", "Leberschäden, Herzprobleme, Akne, Hormonstörungen"],
                  ["EPO, Blutdoping", "mehr rote Blutkörperchen, mehr Ausdauer", "dickes Blut, Thrombosen, Herzinfarkt, Schlaganfall"],
                  ["Stimulanzien", "wacher, weniger Müdigkeit", "Herzrasen, Überhitzung, Abhängigkeit"],
                  ["Diuretika", "schneller Gewicht verlieren, andere Mittel verschleiern", "Austrocknung, Krämpfe, Kreislaufprobleme"]])
    v += abschnitt("B", "Kontrollen und Strafen")
    v += P("Spitzensportler müssen jederzeit für Kontrollen erreichbar sein, auch außerhalb von Wettkämpfen. "
           "Sie geben dazu an, wo sie sich aufhalten. Proben werden jahrelang aufbewahrt und mit neuen Methoden nachgetestet. "
           "Wer erwischt wird, wird meist für mehrere Jahre gesperrt, Medaillen werden aberkannt. In Deutschland ist Doping im Leistungssport auch strafbar.")
    v += abschnitt("C", "Warum Doping unfair ist")
    v += P("Doping verletzt die Chancengleichheit: Gewinnen soll, wer am besten trainiert und am talentiertesten ist, nicht wer die besten Mittel hat. "
           "Es gefährdet die Gesundheit, manchmal tödlich. Und es setzt ehrliche Sportler unter Druck, ebenfalls zu dopen. "
           "Auch im Freizeit- und Fitnessbereich werden Dopingmittel genutzt, oft ohne ärztliche Kontrolle und mit Präparaten aus unsicheren Quellen.")

    v += abschnitt("D", "Schmerzmittel und Nahrungsergänzung")
    v += P("Nicht verboten, aber trotzdem problematisch: Manche Sportler nehmen vor jedem Spiel Schmerzmittel, um trotz Beschwerden spielen zu können. "
           "Schmerz ist aber ein Warnsignal. Wer ihn ausschaltet, riskiert, dass eine kleine Verletzung zu einer großen wird. "
           "Auch Nahrungsergänzungsmittel aus unsicheren Quellen können verbotene Stoffe enthalten. Sportler sind selbst dafür verantwortlich, "
           "was in ihrem Körper ist.")
    v += abschnitt("E", "Doping an Jugendlichen")
    v += P("In der DDR wurde Doping über Jahrzehnte systematisch eingesetzt, auch bei Jugendlichen. Viele bekamen die Mittel als „Vitamine“, "
           "ohne zu wissen, was sie nahmen. Zahlreiche ehemalige Sportlerinnen und Sportler leiden bis heute an den Folgen, etwa an Herz-, "
           "Leber- und Hormonschäden.")
    a = [

        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Die Liste verbotener Mittel erstellt die {}. In Deutschland kontrolliert die {}. Künstliche Hormone für mehr Muskeln heißen {}.",
                ["WADA", "NADA", "Anabolika"], ["Anabolika", "WADA", "NADA"], 30)),
        aufgabe(2, 0, "Ordne die Wirkung zu.",
                zuordnen(L, ["mehr Muskelmasse", "mehr Ausdauer durch mehr rote Blutkörperchen", "wacher, weniger müde", "schnell Gewicht verlieren"], [
                    ("EPO", "B"), ("Anabolika", "A"), ("Diuretika", "D"), ("Stimulanzien", "C")])),
        aufgabe(3, 1, "Warum werden Dopingproben jahrelang aufbewahrt?",
                linien(L, 2, "Mit neuen Testmethoden kann man später Mittel finden, die früher nicht nachweisbar waren. Das schreckt ab.")),
        aufgabe(4, 1, "Nenne drei Gründe, warum Doping abgelehnt wird, und erkläre jeden in einem Satz.",
                linien(L, 3, "Unfair: Es gewinnt nicht der Beste, sondern der mit den besten Mitteln. Gefährlich: schwere Nebenwirkungen bis zum Tod. "
                             "Druck: Ehrliche Sportler fühlen sich gezwungen mitzumachen.")),
        aufgabe(5, 1, "Warum ist es problematisch, vor jedem Spiel Schmerzmittel zu nehmen, obwohl das kein Doping ist?",
                linien(L, 3, "Schmerz zeigt eine Verletzung oder Überlastung an. Wer ihn ausschaltet, spielt weiter und macht die Verletzung schlimmer.")),
        aufgabe(6, 2, "Manche fordern, Doping einfach zu erlauben, „dann ist es wieder fair“. Diskutiere: Was spricht dafür, was dagegen? Gib deine Meinung an.",
                linien(L, 5, "Dafür: keine Kontrollen nötig, alle hätten dieselben Möglichkeiten. Dagegen: Die Gesundheit wird massiv gefährdet, "
                             "auch Jugendliche würden unter Druck gesetzt, es gewinnt das beste Labor statt des besten Sportlers. Meine Meinung: dagegen.")),
        aufgabe(7, 2, "In der DDR bekamen Jugendliche Dopingmittel, oft ohne es zu wissen. Was sagt das über die Verantwortung von Trainern und Betreuern aus?",
                linien(L, 3, "Trainer haben Verantwortung für die Gesundheit der Jugendlichen. Sie dürfen Erfolg nie über die Gesundheit stellen "
                             "und müssen ehrlich sein. Jugendliche vertrauen ihnen.")),
    ]
    return blatt(FP, 1, "Doping", v,
                 ["Doping: verbotene Mittel oder Methoden zur Leistungssteigerung.",
                  "WADA erstellt die Verbotsliste, NADA kontrolliert in Deutschland.",
                  "Doping ist unfair und gefährdet die Gesundheit."], a)


def fp2(L):
    v = abschnitt("A", "Diskriminierung im Sport")
    v += P("Sport soll Menschen verbinden, egal welche Herkunft, Hautfarbe, Religion, welches Geschlecht oder welche sexuelle Orientierung sie haben. "
           "Trotzdem kommt es immer wieder zu Diskriminierung: Fans beleidigen Spieler mit rassistischen Rufen, Spieler werden wegen ihrer Herkunft "
           "ausgegrenzt, Mädchen hören, sie könnten „das sowieso nicht“. Im Profifußball kann der Schiedsrichter ein Spiel bei rassistischen Vorfällen "
           "unterbrechen und sogar abbrechen. Vereine sperren Fans, die diskriminieren.")
    v += abschnitt("B", "Hass im Netz")
    v += P("Nach Spielen werden Sportler in sozialen Medien oft massenhaft beleidigt, besonders nach Fehlern, häufig auch rassistisch. "
           "Manche ziehen sich danach ganz aus dem Netz zurück. Eine Beleidigung ist auch online eine Straftat. Vereine und Verbände melden solche "
           "Kommentare inzwischen und erstatten Anzeige. Hinter dem Bildschirm sitzt immer ein Mensch, der die Worte liest.")
    v += abschnitt("C", "Der Zuschauereffekt")
    v += P("Forscher haben festgestellt: Je mehr Menschen eine Notlage oder eine Beleidigung beobachten, desto seltener greift jemand ein. "
           "Jeder denkt, ein anderer wird schon etwas tun. Man nennt das <b>Zuschauereffekt</b> oder Verantwortungsdiffusion. "
           "Wer das weiß, kann bewusst gegensteuern: Ich warte nicht auf die anderen, ich fange an. Oft machen dann andere mit.")
    v += abschnitt("D", "Sechs Regeln für Zivilcourage")
    v += P("Die Polizei empfiehlt diese Regeln:<br>"
           "1. Ich helfe, ohne mich selbst in Gefahr zu bringen.<br>"
           "2. Ich fordere andere aktiv zur Mithilfe auf („Sie da, helfen Sie mir!“).<br>"
           "3. Ich beobachte genau und merke mir, was passiert und wer beteiligt ist.<br>"
           "4. Ich organisiere Hilfe, im Notfall über den Notruf 110.<br>"
           "5. Ich kümmere mich um die betroffene Person.<br>"
           "6. Ich stehe als Zeuge zur Verfügung.")
    v += abschnitt("E", "Im Schulsport")
    v += P("Zivilcourage beginnt klein: bei Witzen über Herkunft oder Aussehen nicht mitlachen, ruhig, aber deutlich widersprechen "
           "(„Das ist nicht in Ordnung.“), den Betroffenen ins Team holen und die Lehrkraft informieren. Wer schweigt, lässt den Täter glauben, "
           "dass alle einverstanden sind.")
    a = [

        aufgabe(1, 0, "Nenne vier Merkmale, wegen denen Menschen im Sport diskriminiert werden.",
                felder(L, [("1", "Herkunft"), ("2", "Hautfarbe"), ("3", "Geschlecht"), ("4", "Religion")], 4, 34)),
        aufgabe(2, 1, "Was bedeutet Zivilcourage? Erkläre und nenne ein Beispiel aus dem Schulsport.",
                linien(L, 3, "Eingreifen, wenn jemand ungerecht behandelt wird, ohne sich in Gefahr zu bringen. Beispiel: Ein Mitschüler wird wegen seiner "
                             "Herkunft nicht ins Team gewählt, ich wähle ihn und sage, dass das nicht in Ordnung ist.")),
        aufgabe(3, 1, "Erkläre den Zuschauereffekt. Was kann man tun, damit man selbst nicht in diese Falle tappt?",
                linien(L, 3, "Je mehr zuschauen, desto weniger greift einer ein, weil jeder auf die anderen wartet. Gegenmittel: selbst anfangen "
                             "und andere direkt ansprechen, damit sie mithelfen.")),
        aufgabe(4, 1, "Welche der sechs Regeln für Zivilcourage hältst du für die wichtigste? Begründe.",
                linien(L, 3, "Beispiel: Regel 1, weil man nur helfen kann, wenn man selbst nicht verletzt wird. Wer sich in Gefahr bringt, "
                             "braucht am Ende selbst Hilfe.")),
        aufgabe(5, 2, "Nach einem Turnier wird ein Mitspieler im Klassenchat wegen seiner Herkunft beleidigt. Beschreibe Schritt für Schritt, was du tun kannst.",
                linien(L, 4, "Nicht mitmachen und nicht weiterleiten. Im Chat klar widersprechen. Dem Betroffenen privat schreiben, dass ich zu ihm halte. "
                             "Screenshots machen und der Klassenlehrkraft oder Schulsozialarbeit zeigen.")),
        aufgabe(6, 2, "„Im Netz ist eine Beleidigung nicht so schlimm wie im Stadion.“ Nimm Stellung.",
                linien(L, 4, "Stimmt nicht. Online lesen es oft noch mehr Menschen, die Beleidigung bleibt stehen und der Betroffene liest sie immer wieder. "
                             "Auch online ist eine Beleidigung eine Straftat. Hinter dem Bildschirm sitzt ein Mensch.")),
        aufgabe(7, 2, "Entwirf drei Regeln für ein respektvolles Miteinander bei einem Schulturnier und begründe eine davon.",
                linien(L, 3, "1. Keine Beleidigungen, egal gegen wen. 2. Schiedsrichterentscheidungen werden akzeptiert. 3. Nach jedem Spiel geben sich alle die Hand. "
                             "Regel 1, weil sich nur so alle sicher fühlen.")),
    ]
    return blatt(FP, 2, "Respekt und Zivilcourage", v,
                 ["Diskriminierung im Sport widerspricht dem Fair-Play-Gedanken.",
                  "Gewalt hat im Sport keinen Platz.",
                  "Zivilcourage: nicht mitmachen, widersprechen, unterstützen, Hilfe holen."], a)


def fp3(L):
    v = abschnitt("A", "Sportwetten")
    v += P("Werbung für Sportwetten ist überall: in Fußballübertragungen, auf Trikots, in sozialen Medien, oft mit bekannten Sportlern. "
           "Wetten ist in Deutschland erst <b>ab 18 Jahren</b> erlaubt. Bei einer Wette setzt man Geld auf ein Ergebnis. "
           "Die <b>Quote</b> gibt an, wie viel man bei einem Treffer zurückbekommt: Bei einer Quote von 2,5 und 10 € Einsatz sind das 25 €, "
           "der Gewinn beträgt also 15 €. Liegt man falsch, ist der Einsatz weg.")
    v += P("Die Anbieter legen die Quoten so fest, dass sie auf Dauer immer verdienen. Einzelne gewinnen manchmal, die große Mehrheit der Wettenden "
           "verliert über die Zeit mehr Geld, als sie gewinnt. Die Werbung zeigt dagegen fast nur Gewinner.")
    v += abschnitt("B", "Wenn Wetten zur Sucht wird")
    v += P("Glücksspiel kann süchtig machen. Besonders gefährlich sind Wetten, die man jederzeit per App abschließen kann, auch während eines Spiels. "
           "Warnsignale sind: immer höhere Einsätze, der Versuch, Verluste „zurückzuholen“, Lügen über das Wetten, Geld leihen, "
           "Gedanken drehen sich ständig ums Wetten. Wer bei sich oder anderen solche Zeichen bemerkt, sollte mit einer Vertrauensperson sprechen. "
           "Es gibt kostenlose Beratungsstellen für Glücksspielsucht.")
    v += abschnitt("C", "Spielmanipulation")
    v += P("Wo viel Geld gewettet wird, versuchen Kriminelle, Ergebnisse zu beeinflussen. Sie bezahlen Spieler oder Schiedsrichter dafür, "
           "absichtlich zu verlieren, eine Gelbe Karte zu holen oder einen Elfmeter zu verursachen, und wetten dann genau darauf. "
           "Besonders gefährdet sind untere Ligen und der Jugendbereich, wo wenig verdient wird und kaum jemand genau hinschaut. "
           "In Deutschland wurde 2005 ein Skandal bekannt, bei dem ein Schiedsrichter Spiele für Wettbetrüger verschoben hatte. "
           "Seit 2017 sind Sportwettbetrug und Manipulation von Spielen ausdrücklich Straftaten.")
    v += abschnitt("D", "Warum Manipulation den Sport zerstört")
    v += P("Sport lebt davon, dass der Ausgang offen ist und jeder sein Bestes gibt. Wenn Zuschauer nicht mehr sicher sein können, "
           "ob ein Spiel echt ist, verliert der Sport seinen Sinn. Deshalb müssen Spieler, Trainer und Schiedsrichter Angebote sofort melden.")
    v += abschnitt("E", "Hilfe holen")
    v += P("Wer merkt, dass er die Kontrolle verliert, sollte mit jemandem sprechen, dem er vertraut. In Deutschland kann man sich außerdem selbst "
           "für alle legalen Glücksspielangebote sperren lassen. Das bundesweite Sperrsystem heißt OASIS. Beratungsstellen helfen kostenlos und vertraulich, "
           "auch Angehörigen und Freunden, die sich Sorgen machen.")
    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Sportwetten sind in Deutschland erst ab {} erlaubt. Die {} gibt an, wie viel man bei einem Treffer zurückbekommt. "
                "Seit {} ist Sportwettbetrug ausdrücklich eine Straftat.",
                ["18 Jahren", "Quote", "2017"], ["2017", "18 Jahren", "Quote"], 30)),
        aufgabe(2, 1, "Berechne Auszahlung und Gewinn bei einem Treffer.",
                felder(L, [("Quote 1,8, Einsatz 20 €", "36 €, Gewinn 16 €"), ("Quote 3,0, Einsatz 5 €", "15 €, Gewinn 10 €"),
                           ("Quote 1,2, Einsatz 50 €", "60 €, Gewinn 10 €")], 3, 50)),
        aufgabe(3, 1, "Erkläre, warum Wettanbieter auf Dauer Geld verdienen, obwohl manche Kunden gewinnen.",
                linien(L, 3, "Die Quoten sind so berechnet, dass insgesamt mehr Geld eingesetzt als ausgezahlt wird. Die Verluste der vielen "
                             "sind größer als die Gewinne der wenigen.")),
        aufgabe(4, 1, "Nenne drei Warnsignale für Wettsucht und erkläre, warum das „Zurückholen“ von Verlusten besonders gefährlich ist.",
                linien(L, 3, "Immer höhere Einsätze, Lügen, Geld leihen, ständige Gedanken ans Wetten. Wer Verluste zurückholen will, "
                             "setzt immer mehr und verliert meist noch mehr. So entsteht ein Teufelskreis.")),
        aufgabe(5, 2, "Warum ist Spielmanipulation gerade in unteren Ligen und im Jugendbereich ein Risiko?",
                linien(L, 3, "Dort verdienen Spieler und Schiedsrichter wenig, Geldangebote sind verlockender. Es gibt weniger Kameras und Kontrollen, "
                             "Manipulation fällt seltener auf.")),
        aufgabe(6, 2, "Sollte Werbung für Sportwetten mit bekannten Sportlern verboten werden? Nimm Stellung und nenne Argumente für beide Seiten.",
                linien(L, 5, "Dafür: Sportler sind Vorbilder für Jugendliche, die Werbung lässt Wetten harmlos wirken und kann süchtig machen. "
                             "Dagegen: Wetten ist für Erwachsene erlaubt, Vereine brauchen die Einnahmen. Meine Meinung: verbieten, weil viele Jugendliche zusehen.")),
        aufgabe(7, 2, "Ein Freund (17) wettet heimlich über das Konto seines älteren Bruders und will seine Verluste zurückholen. Was sagst du ihm?",
                linien(L, 4, "Das ist verboten, weil er unter 18 ist, und er gerät in einen Teufelskreis. Ich rate ihm aufzuhören, das Konto nicht mehr zu nutzen "
                             "und mit einer Vertrauensperson oder einer Beratungsstelle zu sprechen.")),
    ]
    return blatt(FP, 3, "Sportwetten und Spielmanipulation", v,
                 ["Sportwetten erst ab 18, auf Dauer gewinnt der Anbieter.",
                  "Verluste zurückholen wollen ist ein Warnsignal für Sucht.",
                  "Spielmanipulation ist eine Straftat und zerstört den Sport."], a)


# ================================================================== Herz, Puls und Ausdauer
HP = "Herz, Puls und Ausdauer"


def hp1(L):
    v = abschnitt("A", "Woher die Muskeln ihre Energie bekommen")
    v += P("Muskeln können nur einen Brennstoff direkt nutzen: <b>ATP</b> (Adenosintriphosphat). Davon ist aber nur sehr wenig gespeichert, "
           "es reicht für 2 bis 3 Sekunden Höchstleistung. Danach muss ATP ständig neu gebildet werden. Dafür hat der Körper drei Wege, "
           "die je nach Dauer und Intensität der Belastung im Vordergrund stehen.")
    v += f'<div style="width:140mm;margin:1mm auto 1.5mm auto">{zonen_balken()}</div>'
    v += tabelle(["Weg", "Wie?", "Typisch für"],
                 [["ATP/KP (anaerob-alaktazid)", "Kreatinphosphat (KP) im Muskel liefert sehr schnell neues ATP, reicht etwa 10 Sekunden", "Sprint 50 m, Kugelstoßen, Sprung"],
                  ["anaerob-laktazid", "Zucker wird ohne Sauerstoff abgebaut, schnell, aber es entsteht Laktat", "400-m-Lauf, langer Angriff im Handball"],
                  ["aerob", "Zucker und Fett werden mit Sauerstoff abgebaut, langsam, aber fast unbegrenzt", "Coopertest, Radfahren, Schwimmen"]])
    v += abschnitt("B", "Laktat")
    v += P("Bei sehr intensiver Belastung entsteht viel Laktat (Milchsäure-Salz). Der Muskel wird übersäuert, er brennt, die Bewegungen werden schwer. "
           "Man muss langsamer werden oder aufhören. Nach der Belastung wird das Laktat innerhalb von etwa einer Stunde abgebaut, "
           "lockeres Auslaufen beschleunigt das. Muskelkater entsteht übrigens nicht durch Laktat, sondern durch winzige Risse in den Muskelfasern.")
    v += abschnitt("C", "Training der Energiewege")
    v += P("Gut trainierte Ausdauersportler können mehr Energie aerob bereitstellen. Sie laufen deshalb schneller, bevor viel Laktat entsteht. "
           "Diese Schwelle verschiebt sich durch Training nach oben. Sprinter trainieren dagegen vor allem kurze, maximale Belastungen mit langen Pausen.")

    v += abschnitt("D", "Nach der Belastung")
    v += P("Nach einem Sprint atmest du noch eine ganze Weile schnell, obwohl du schon stehst. Der Körper arbeitet weiter: "
           "Er füllt die Kreatinphosphatspeicher wieder auf, baut Laktat ab, kühlt sich und bringt den Puls zurück. "
           "Dafür braucht er zusätzlichen Sauerstoff. Man spricht von der <b>Sauerstoffschuld</b>, die nach der Belastung „zurückgezahlt“ wird. "
           "Je intensiver die Belastung war, desto länger dauert das.")
    a = [

        aufgabe(1, 0, "Welcher Energieweg steht im Vordergrund? Schreibe ATP/KP, anaerob oder aerob.",
                felder(L, [("100-m-Sprint", "ATP/KP"), ("Marathon", "aerob"), ("400-m-Lauf", "anaerob"),
                           ("Hochsprung", "ATP/KP"), ("12-min-Lauf", "aerob"), ("Radtour", "aerob")], 3, 36)),
        aufgabe(2, 1, "Erkläre, warum man einen 400-m-Lauf nicht im Sprinttempo durchhalten kann.",
                linien(L, 3, "Die schnelle ATP/KP-Energie reicht nur etwa 10 Sekunden. Danach liefert der anaerobe Weg Energie, dabei entsteht viel Laktat. "
                             "Der Muskel übersäuert und man wird langsamer.")),
        aufgabe(3, 1, "Vergleiche den anaeroben und den aeroben Weg: Was ist jeweils der Vorteil, was der Nachteil?",
                linien(L, 3, "Anaerob: liefert schnell viel Energie, aber es entsteht Laktat, nur kurz durchzuhalten. "
                             "Aerob: fast unbegrenzt und ohne Laktat, liefert die Energie aber langsamer, nur mittlere Intensität.")),
        aufgabe(4, 1, "Warum atmest du nach einem Sprint noch eine Weile schnell, obwohl du schon stehst?",
                linien(L, 3, "Der Körper braucht zusätzlichen Sauerstoff, um die Speicher aufzufüllen, Laktat abzubauen und sich zu erholen. "
                             "Er zahlt die Sauerstoffschuld zurück.")),
        aufgabe(5, 2, "Ein Handballspiel dauert 60 Minuten. Welche Energiewege werden genutzt? Begründe mit Spielsituationen.",
                linien(L, 4, "Alle drei: ATP/KP beim Sprung und Wurf, anaerob bei schnellen Gegenstößen und langen Abwehrphasen, "
                             "aerob über das ganze Spiel für das Laufen und die Erholung zwischen den Aktionen.")),
        aufgabe(6, 2, "Wähle deine Lieblingssportart. Beschreibe, wann welcher Energieweg gebraucht wird und wie man ihn gezielt trainieren könnte.",
                linien(L, 5, "Beispiel Fußball: Sprints und Schüsse über ATP/KP, trainiert mit kurzen Sprints und langen Pausen. Lange Tempoläufe anaerob, "
                             "trainiert mit Intervallen. Das Laufen über 90 Minuten aerob, trainiert mit lockeren Dauerläufen.")),
        aufgabe(7, 2, "Ein Sprinter und ein Marathonläufer trainieren ganz unterschiedlich. Erkläre den Unterschied mit den Energiewegen.",
                linien(L, 3, "Der Sprinter braucht vor allem den ATP/KP-Weg, er trainiert kurze maximale Sprints mit langen Pausen. "
                             "Der Marathonläufer braucht den aeroben Weg, er trainiert lange, lockere Läufe.")),
    ]
    return blatt(HP, 1, "Energie für die Muskeln", v,
                 ["Muskeln nutzen ATP, der Vorrat reicht nur Sekunden.",
                  "ATP/KP bis etwa 10 s, dann anaerob mit Laktat, auf Dauer aerob.",
                  "Ausdauertraining verbessert den aeroben Weg."], a)


def hp2(L):
    v = abschnitt("A", "Belastung messbar machen")
    v += P("Ein Training lässt sich durch fünf Größen beschreiben, die <b>Belastungsnormative</b>. Wer sie kennt, kann sein Training gezielt planen.")
    v += tabelle(["Größe", "Bedeutung", "Beispiel"],
                 [["Intensität", "Wie stark? (Tempo, Gewicht, Puls)", "Laufen bei 70 % der max. Herzfrequenz"],
                  ["Dauer", "Wie lange dauert eine Belastung?", "30 Minuten am Stück, oder ein Lauf von 400 m"],
                  ["Umfang", "Wie viel insgesamt?", "6 Läufe à 400 m, also 2,4 km"],
                  ["Dichte", "Verhältnis von Belastung und Pause", "400 m laufen, 2 Minuten Pause"],
                  ["Häufigkeit", "Wie oft pro Woche?", "dreimal pro Woche"]])
    v += abschnitt("B", "Zwei Methoden für Ausdauer")
    v += kacheln([
        ("#dbe8f5", "Dauermethode", "",
         "Lange, gleichmäßige Belastung ohne Pause bei niedriger bis mittlerer Intensität, z. B. 30 bis 60 Minuten locker laufen. "
         "Verbessert die Grundlagenausdauer und den Fettstoffwechsel."),
        ("#fbe9c2", "Intervallmethode", "",
         "Wechsel von intensiven Belastungen und lohnenden Pausen, in denen man sich nur teilweise erholt, z. B. 6 · 400 m schnell, "
         "dazwischen 2 Minuten Trab. Verbessert Tempo und Laktattoleranz."),
    ])
    v += abschnitt("C", "Herzfrequenz als Steuerung")
    v += P("Die Intensität kann man gut über die Herzfrequenz steuern. Genauer als 220 − Alter ist die Formel nach Karvonen, "
           "die den Ruhepuls einbezieht:")
    v += ('<div class="box" style="text-align:center;margin:1mm 0 2mm 0;font-weight:600">Trainingspuls = Ruhepuls + (max. HF − Ruhepuls) · Intensität<br>'
          '<span style="font-weight:400">Beispiel: 16 Jahre, Ruhepuls 60, max. HF 204, Intensität 70 %: 60 + 144 · 0,7 ≈ 161</span></div>')
    v += P("Für die Grundlagenausdauer liegt die Intensität etwa bei 60 bis 75 %. Etwa 80 % der Trainingszeit sollten Ausdauersportler "
           "in diesem lockeren Bereich verbringen, den Rest intensiv.")

    v += abschnitt("D", "Ohne Pulsuhr steuern")
    v += P("Nicht jeder hat eine Pulsuhr. Zwei einfache Hilfen: Beim <b>Sprechtest</b> prüft man, ob man noch in ganzen Sätzen sprechen kann. "
           "Dann liegt man im lockeren Bereich. Mit der <b>Borg-Skala</b> schätzt man die Anstrengung selbst auf einer Skala von 6 (gar keine Anstrengung) "
           "bis 20 (maximal). Lockeres Grundlagentraining liegt etwa bei 11 bis 13 („leicht“ bis „etwas anstrengend“), harte Intervalle bei 15 bis 17.")
    a = [

        aufgabe(1, 0, "Ordne die Belastungsnormative zu.",
                zuordnen(L, ["Intensität", "Dauer", "Umfang", "Dichte", "Häufigkeit"], [
                    ("viermal pro Woche", "E"), ("bei 80 % der max. HF", "A"), ("insgesamt 5 km", "C"),
                    ("90 Sekunden Pause zwischen den Läufen", "D"), ("ein Lauf dauert 3 Minuten", "B")])),
        aufgabe(2, 1, "Berechne den Trainingspuls nach Karvonen (max. HF = 220 − Alter) für: 15 Jahre, Ruhepuls 70, Intensität 65 %.",
                linien(L, 2, "max. HF 205. 70 + (205 − 70) · 0,65 = 70 + 87,75 ≈ 158 Schläge pro Minute")),
        aufgabe(3, 1, "Erkläre den Unterschied zwischen Dauermethode und Intervallmethode. Was verbessert man jeweils?",
                linien(L, 3, "Dauermethode: lange gleichmäßige Belastung ohne Pause, verbessert die Grundlagenausdauer. Intervallmethode: Wechsel von "
                             "intensiven Abschnitten und lohnenden Pausen, verbessert Tempo und Laktattoleranz.")),
        aufgabe(4, 1, "Wie kann man die Intensität ohne Pulsuhr steuern? Beschreibe zwei Möglichkeiten.",
                linien(L, 3, "Sprechtest: Wer in ganzen Sätzen sprechen kann, läuft locker. Borg-Skala: Anstrengung selbst von 6 bis 20 einschätzen, "
                             "locker etwa 11 bis 13.")),
        aufgabe(5, 2, "Beschreibe ein Intervalltraining für den Coopertest mit allen fünf Normativen.",
                linien(L, 3, "Intensität: etwas schneller als Wunschtempo. Dauer: 400 m pro Lauf. Umfang: 6 Läufe = 2,4 km. "
                             "Dichte: 2 Minuten Trabpause. Häufigkeit: einmal pro Woche, dazu zweimal locker laufen.")),
        aufgabe(6, 2, "Warum sollen Ausdauersportler die meiste Zeit locker trainieren und nicht immer intensiv?",
                linien(L, 3, "Im lockeren Bereich wird die Grundlagenausdauer verbessert, der Körper erholt sich schnell und das Verletzungsrisiko ist gering. "
                             "Immer intensiv führt zu Erschöpfung und Übertraining.")),
        aufgabe(7, 2, "Plane drei Trainingswochen für einen Jugendlichen, der in 8 Wochen 5 km am Stück laufen will. Nutze Dauer- und Intervallmethode.",
                linien(L, 3, "Woche 1: dreimal 20 min locker (Borg 11 bis 12). Woche 2: zweimal 25 min locker, einmal 6 · 2 min zügig, 1 min Gehpause. "
                             "Woche 3: zweimal 30 min locker, einmal 5 · 3 min zügig. Danach weiter langsam steigern.")),
    ]
    return blatt(HP, 2, "Ausdauertraining planen", v,
                 ["Intensität, Dauer, Umfang, Dichte, Häufigkeit.",
                  "Dauermethode für Grundlagen, Intervallmethode für Tempo.",
                  "Karvonen: Ruhepuls + (max. HF − Ruhepuls) · Intensität."], a)


def hp3(L):
    v = abschnitt("A", "Wie sich der Körper anpasst")
    v += P("Regelmäßiges Ausdauertraining verändert den Körper. Nach einigen Wochen bis Monaten sind die Anpassungen messbar:")
    v += tabelle(["Organ", "Anpassung", "Folge"],
                 [["Herz", "Herzmuskel wird kräftiger, Schlagvolumen steigt", "niedrigerer Ruhepuls, mehr Blut pro Minute unter Last"],
                  ["Blut", "mehr Blutvolumen und rote Blutkörperchen", "mehr Sauerstofftransport"],
                  ["Muskeln", "mehr Kapillaren und Mitochondrien (Kraftwerke der Zelle)", "Sauerstoff wird besser genutzt, weniger Laktat"],
                  ["Lunge und Atmung", "Atemmuskulatur wird stärker", "ökonomischere Atmung"],
                  ["Stoffwechsel", "Fett wird besser als Energiequelle genutzt", "Glykogen wird geschont, längeres Durchhalten"]])
    v += abschnitt("B", "Das Sportlerherz")
    v += P("Bei Ausdauersportlern, die viele Stunden pro Woche trainieren, kann das Herz deutlich größer und kräftiger werden. "
           "Man spricht vom <b>Sportlerherz</b>. Es ist eine gesunde Anpassung und keine Krankheit. Der Ruhepuls kann auf 40 oder sogar darunter sinken. "
           "Hört man mit dem Training auf, bildet es sich innerhalb von Monaten wieder zurück.")
    v += abschnitt("C", "Die maximale Sauerstoffaufnahme")
    v += P("Wie viel Sauerstoff der Körper pro Minute höchstens aufnehmen und verwerten kann, heißt <b>VO₂max</b>. "
           "Sie wird in Millilitern pro Kilogramm Körpergewicht und Minute angegeben. Untrainierte Jugendliche liegen bei etwa 40 bis 50, "
           "Spitzen-Ausdauersportler bei 70 bis über 80. Die VO₂max hängt zum Teil von den Genen ab, lässt sich aber durch Training deutlich steigern.")
    v += abschnitt("D", "Gesundheit")
    v += P("Ausdauertraining senkt das Risiko für Herzinfarkt, Bluthochdruck, Diabetes Typ 2 und Übergewicht. "
           "Es verbessert Schlaf, Stimmung und Konzentration. Schon 150 Minuten moderate Bewegung pro Woche zeigen bei Erwachsenen deutliche Wirkung.")

    v += abschnitt("E", "Was passiert ohne Training?")
    v += P("Anpassungen bleiben nicht für immer. Wer aufhört zu trainieren, verliert sie wieder. Die Ausdauer lässt schon nach wenigen Wochen "
           "spürbar nach, der Ruhepuls steigt, das Schlagvolumen sinkt. Nach einer Verletzungspause sollte man deshalb nicht dort weitermachen, "
           "wo man aufgehört hat, sondern langsam wieder einsteigen und die Belastung über mehrere Wochen steigern.")
    a = [

        aufgabe(1, 0, "Ordne die Anpassung dem Organ zu.",
                zuordnen(L, ["Schlagvolumen steigt", "mehr rote Blutkörperchen", "mehr Mitochondrien", "Fett wird besser genutzt"], [
                    ("Muskeln", "C"), ("Herz", "A"), ("Stoffwechsel", "D"), ("Blut", "B")])),
        aufgabe(2, 1, "Erkläre den Zusammenhang zwischen Schlagvolumen und Ruhepuls.",
                linien(L, 3, "Je größer das Schlagvolumen, desto mehr Blut pro Schlag. Für dieselbe Blutmenge in Ruhe braucht das Herz weniger Schläge, "
                             "der Ruhepuls sinkt.")),
        aufgabe(3, 1, "Eine Sportlerin wiegt 55 kg und hat eine VO₂max von 52 ml/kg/min. Wie viel Sauerstoff kann sie pro Minute höchstens aufnehmen?",
                linien(L, 1, "52 · 55 = 2860 ml, also etwa 2,9 Liter pro Minute")),
        aufgabe(4, 2, "Warum verbraucht ein trainierter Läufer bei gleichem Tempo weniger Glykogen als ein untrainierter?",
                linien(L, 3, "Er hat mehr Mitochondrien und Kapillaren und nutzt Fett besser als Energiequelle. "
                             "Er läuft länger im aeroben Bereich, das Glykogen wird geschont.")),
        aufgabe(5, 2, "„Ein Sportlerherz ist krank, weil es so groß ist.“ Nimm Stellung.",
                linien(L, 3, "Falsch. Das Sportlerherz ist eine gesunde Anpassung an viel Ausdauertraining. Es pumpt mehr Blut pro Schlag, "
                             "der Ruhepuls sinkt. Ohne Training bildet es sich wieder zurück.")),
        aufgabe(6, 2, "Eine Läuferin pausiert verletzungsbedingt sechs Wochen. Was passiert mit ihren Anpassungen und wie sollte sie wieder einsteigen?",
                linien(L, 4, "Die Ausdauer sinkt, der Ruhepuls steigt, das Schlagvolumen wird kleiner. Sie sollte mit kurzen, lockeren Läufen beginnen "
                             "und Umfang und Tempo über mehrere Wochen langsam steigern.")),
        aufgabe(7, 2, "Nenne drei gesundheitliche Vorteile von Ausdauertraining und begründe, warum sie für dich später wichtig sein könnten.",
                linien(L, 4, "Weniger Herz-Kreislauf-Krankheiten, weniger Übergewicht, besserer Schlaf und bessere Stimmung. Im Beruf sitzt man oft viel, "
                             "da schützt eine gute Ausdauer vor Bewegungsmangelkrankheiten.")),
    ]
    return blatt(HP, 3, "Anpassungen durch Training", v,
                 ["Training vergrößert Schlagvolumen, Blutvolumen und Mitochondrien.",
                  "Sportlerherz: gesunde Anpassung, niedriger Ruhepuls.",
                  "VO₂max zeigt die Ausdauerleistungsfähigkeit."], a)


# ================================================================== Training und Erholung
TE = "Training und Erholung"


def te1(L):
    v = abschnitt("A", "Krafttraining im Jugendalter")
    v += P("Lange hieß es, Krafttraining schade Jugendlichen. Heute ist klar: Richtig gemacht ist es sicher und sinnvoll. "
           "Es stärkt Muskeln, Sehnen und Knochen, verbessert die Haltung und beugt Verletzungen vor. Entscheidend ist die richtige Technik.")
    v += abschnitt("B", "Grundregeln")
    v += kacheln([
        ("#dbe8f5", "Technik vor Gewicht", "", "Erst die Bewegung sauber lernen, am besten mit dem eigenen Körpergewicht. Gewicht erst steigern, wenn die Technik sitzt."),
        ("#d9efd8", "Ganzkörper", "", "Nicht nur Arme und Bauch: Beine, Rücken und Rumpf sind genauso wichtig. Gegenspieler-Muskeln mittrainieren."),
        ("#fbe9c2", "Kontrolliert", "", "Langsam und kontrolliert bewegen, nicht ruckartig. Ausatmen bei der Anstrengung, nicht pressen."),
        ("#f6d9d6", "Pausen", "", "Zwischen zwei Krafteinheiten für dieselbe Muskelgruppe etwa 48 Stunden Pause."),
    ])
    v += abschnitt("C", "Wiederholungen und Sätze")
    v += P("Eine <b>Wiederholung</b> ist eine einzelne Ausführung einer Übung, ein <b>Satz</b> eine Reihe von Wiederholungen ohne Pause. "
           "Für Jugendliche empfiehlt sich ein Kraftausdauer-Training: <b>2 bis 3 Sätze</b> mit <b>12 bis 20 Wiederholungen</b>, "
           "dazwischen 1 bis 2 Minuten Pause. Die letzten Wiederholungen sollen anstrengend sein, aber noch sauber gelingen.")
    v += tabelle(["Übung", "trainiert vor allem"],
                 [["Kniebeuge", "Oberschenkel, Gesäß"], ["Liegestütz", "Brust, Schultern, Arme (Trizeps)"],
                  ["Unterarmstütz (Plank)", "Rumpf, Bauch, Rücken"], ["Ausfallschritt", "Oberschenkel, Gesäß, Gleichgewicht"],
                  ["Superman (Bauchlage, Arme und Beine heben)", "unterer Rücken"]])
    v += abschnitt("D", "Kraft ist nicht gleich Kraft")
    v += P("Man unterscheidet drei Kraftarten. <b>Maximalkraft</b> ist die größte Kraft, die man einmal aufbringen kann, etwa beim Gewichtheben. "
           "<b>Schnellkraft</b> ist die Fähigkeit, in kurzer Zeit viel Kraft zu entwickeln, etwa beim Sprung, Wurf oder Kugelstoßen. "
           "<b>Kraftausdauer</b> heißt, eine Kraftleistung lange durchzuhalten, etwa beim Rudern, Klettern oder vielen Liegestützen. "
           "Für Jugendliche steht die Kraftausdauer im Vordergrund. Sie legt die Grundlage, auf der später gezielt Maximal- und Schnellkraft aufgebaut werden.")
    a = [

        aufgabe(1, 0, "Erkläre die Begriffe.",
                felder(L, [("Wiederholung", "eine einzelne Ausführung"), ("Satz", "Reihe von Wiederholungen ohne Pause")], 2, 70)),
        aufgabe(2, 0, "Welche Muskeln trainiert die Übung? Ordne zu.",
                zuordnen(L, ["Oberschenkel und Gesäß", "Brust, Schultern, Arme", "Rumpf", "unterer Rücken"], [
                    ("Liegestütz", "B"), ("Plank", "C"), ("Kniebeuge", "A"), ("Superman", "D")])),
        aufgabe(3, 1, "Welche Kraftart braucht man vor allem beim Kugelstoßen, beim Rudern über 2000 m und beim Gewichtheben? Begründe jeweils.",
                linien(L, 3, "Kugelstoßen: Schnellkraft, weil in sehr kurzer Zeit viel Kraft gebraucht wird. Rudern: Kraftausdauer, viele Züge lang durchhalten. "
                             "Gewichtheben: Maximalkraft, einmal die größte Last bewegen.")),
        aufgabe(4, 1, "Stelle ein Ganzkörper-Programm mit vier Übungen zusammen. Gib Sätze, Wiederholungen und Pausen an.",
                linien(L, 3, "Kniebeuge 3 · 15, Liegestütz 3 · 12, Plank 3 · 30 Sekunden, Superman 2 · 15. Pause je 90 Sekunden.")),
        aufgabe(5, 2, "Warum gilt gerade für Jugendliche: Technik vor Gewicht?",
                linien(L, 3, "Knochen, Sehnen und Gelenke sind noch im Wachstum. Mit falscher Technik und zu viel Gewicht drohen Überlastungen und Verletzungen. "
                             "Eine saubere Technik ist außerdem die Grundlage für spätere Steigerungen.")),
        aufgabe(6, 2, "Ein Mitschüler trainiert täglich nur Bizeps und Bauch. Was würdest du ihm raten? Begründe.",
                linien(L, 3, "Ganzkörper trainieren, besonders Beine und Rücken, sonst entstehen Ungleichgewichte und Haltungsprobleme. "
                             "Dieselben Muskeln nicht täglich, 48 Stunden Pause einplanen.")),
        aufgabe(7, 1, "Zeichne eine Übung aus der Tabelle als Strichmännchen in Start- und Endposition.",
                karo(L, 24, "z. B. Kniebeuge: Stand, dann Knie gebeugt, Rücken gerade, Arme nach vorne")),
    ]
    return blatt(TE, 1, "Krafttraining", v,
                 ["Richtig gemacht ist Krafttraining für Jugendliche sinnvoll.",
                  "Technik vor Gewicht, ganzer Körper, kontrolliert.",
                  "2 bis 3 Sätze mit 12 bis 20 Wiederholungen."], a)


def te2(L):
    v = abschnitt("A", "Training braucht Erholung")
    v += P("Der Trainingseffekt entsteht nicht während der Belastung, sondern in der Erholung danach: Der Körper repariert und passt sich an "
           "(Superkompensation). Wie lange das dauert, hängt von der Art der Belastung ab:")
    v += tabelle(["Was erholt sich?", "Dauer, etwa"],
                 [["ATP- und Kreatinphosphatspeicher", "wenige Minuten"], ["Laktatabbau", "etwa 1 Stunde"],
                  ["Glykogenspeicher", "24 bis 48 Stunden"], ["Muskelfasern nach intensivem Krafttraining", "48 bis 72 Stunden"],
                  ["Sehnen, Bänder, Knochen", "Tage bis Wochen"]])
    v += abschnitt("B", "Schlaf als wichtigste Erholung")
    v += P("Im Tiefschlaf schüttet der Körper die meisten Wachstumshormone aus. Muskeln, Sehnen und das Immunsystem regenerieren sich, "
           "das Gehirn festigt neu gelernte Bewegungen. Jugendliche brauchen 8 bis 10 Stunden. Studien zeigen, dass Sportler, "
           "die regelmäßig zu wenig schlafen, sich häufiger verletzen.")
    v += abschnitt("C", "Stress")
    v += P("Auch Stress, etwa vor Prüfungen, belastet den Körper. Das Stresshormon Cortisol bleibt erhöht, der Schlaf wird schlechter, "
           "die Erholung langsamer. Training und Schule wirken also zusammen. In stressigen Phasen hilft es, das Training etwas lockerer zu gestalten, "
           "statt ganz aufzuhören: Bewegung baut Stress ab.")
    v += abschnitt("D", "Erholung aktiv gestalten")
    v += P("<b>Auslaufen und Ausfahren:</b> 5 bis 10 Minuten locker nach dem Training.<br>"
           "<b>Ernährung:</b> Kohlenhydrate und Eiweiß nach dem Sport, genug trinken.<br>"
           "<b>Aktive Erholung:</b> leichte Bewegung am Ruhetag, etwa Spazierengehen, lockeres Radfahren, Schwimmen.<br>"
           "<b>Bildschirm:</b> Abends Handy weg, das blaue Licht verzögert das Einschlafen.<br>"
           "<b>Warnsignale ernst nehmen:</b> erhöhter Ruhepuls am Morgen, Müdigkeit, Lustlosigkeit, häufige Infekte.")
    a = [

        aufgabe(1, 0, "Wie lange dauert die Erholung? Ordne zu.",
                zuordnen(L, ["wenige Minuten", "etwa 1 Stunde", "24 bis 48 Stunden", "Tage bis Wochen"], [
                    ("Glykogenspeicher", "C"), ("Sehnen und Bänder", "D"), ("Kreatinphosphat", "A"), ("Laktatabbau", "B")])),
        aufgabe(2, 1, "Warum ist es sinnvoll, nach einem harten Training 5 bis 10 Minuten locker auszulaufen?",
                linien(L, 2, "Das Laktat wird schneller abgebaut, Puls und Kreislauf beruhigen sich langsam, die Erholung beginnt früher.")),
        aufgabe(3, 1, "Ein Fußballer spielt am Samstag und trainiert am Sonntag schon wieder intensiv. Was ist das Problem? Was wäre besser?",
                linien(L, 3, "Die Glykogenspeicher sind nach 24 Stunden noch nicht voll, die Muskeln nicht erholt. Er riskiert Verletzungen und Übertraining. "
                             "Besser: Sonntag aktive Erholung, z. B. lockeres Radfahren.")),
        aufgabe(4, 2, "Erkläre, wie Stress, Schlaf und Training zusammenhängen. Verwende die Begriffe Cortisol und Erholung.",
                linien(L, 4, "Bei Stress bleibt Cortisol erhöht, man schläft schlechter und erholt sich langsamer. Dann wirkt Training weniger "
                             "und das Verletzungsrisiko steigt. Lockere Bewegung kann Stress aber auch abbauen.")),
        aufgabe(5, 2, "Plane eine Woche für dich mit Schule, Training und Erholung in einer Prüfungsphase.",
                linien(L, 5, "Mo locker laufen 30 min, Di Lernen und früh schlafen, Mi Vereinstraining, Do Ruhetag mit Spaziergang, "
                             "Fr kurze Kraftübungen, Sa Spiel, So aktive Erholung. Jeden Abend Handy um 21:30 Uhr weg, 9 Stunden Schlaf.")),
        aufgabe(6, 1, "Was tust du selbst nach einem anstrengenden Tag, um dich zu erholen? Was davon ist sinnvoll, was weniger?",
                linien(L, 3, "Beispiel: Ich zocke abends lange, das ist weniger sinnvoll, weil das Licht den Schlaf stört. "
                             "Spazierengehen mit dem Hund und früh schlafen sind sinnvoll.")),
    ]
    return blatt(TE, 2, "Regeneration und Stress", v,
                 ["Der Trainingseffekt entsteht in der Erholung.",
                  "Glykogen braucht 24 bis 48 h, Muskeln nach Krafttraining 48 bis 72 h.",
                  "Schlaf ist die wichtigste Erholung, Stress bremst sie."], a)


def te3(L):
    v = abschnitt("A", "Trainingsplanung im Jahr")
    v += P("Leistungssportler teilen ihr Jahr in Abschnitte ein. Das nennt man <b>Periodisierung</b>. "
           "So erreichen sie ihre Bestform genau zum wichtigsten Wettkampf.")
    v += kacheln([
        ("#dbe8f5", "Vorbereitung", "", "Grundlagen aufbauen: viel Umfang, mittlere Intensität, Technik."),
        ("#fbe9c2", "Wettkampf", "", "Weniger Umfang, mehr Intensität, Wettkämpfe. Bestform halten."),
        ("#d9efd8", "Übergang", "", "Erholung, andere Sportarten, Pause für Körper und Kopf."),
    ], cols=3)
    v += abschnitt("B", "Die Trainingsprinzipien")
    v += tabelle(["Prinzip", "Kurz erklärt"],
                 [["wirksamer Belastungsreiz", "Der Reiz muss eine bestimmte Schwelle überschreiten, sonst passiert nichts."],
                  ["progressive Belastungssteigerung", "Belastung schrittweise erhöhen: erst Häufigkeit, dann Umfang, zuletzt Intensität."],
                  ["optimale Relation von Belastung und Erholung", "Die nächste Belastung im Moment der Superkompensation setzen."],
                  ["Kontinuität", "Regelmäßig trainieren, sonst gehen Anpassungen verloren."],
                  ["Variation", "Training abwechslungsreich gestalten, damit der Körper weiter gefordert wird."],
                  ["Individualität und Altersgemäßheit", "Training an Alter, Entwicklung und Ziel anpassen."]])
    v += abschnitt("C", "Ein Ziel, ein Plan")
    v += P("Ein guter Trainingsplan beginnt mit einem klaren Ziel: Was will ich bis wann erreichen? Daraus ergeben sich Häufigkeit, "
           "Inhalte und Steigerung. Einen Plan sollte man nicht starr befolgen, sondern anpassen, wenn man krank ist, Prüfungen anstehen "
           "oder die Fortschritte schneller oder langsamer kommen als gedacht. Ein Trainingstagebuch hilft, den Überblick zu behalten.")

    v += abschnitt("D", "Das Trainingstagebuch")
    v += P("Wer seine Fortschritte sehen will, schreibt sein Training auf. In ein Trainingstagebuch gehören: Datum, Art des Trainings, "
           "Dauer und Umfang, die Intensität (Puls oder Borg-Skala), wie man sich gefühlt hat, wie man geschlafen hat und Besonderheiten wie Schmerzen. "
           "Nach einigen Wochen erkennt man Muster: Wann lief es gut, wann schlecht, und woran lag es?")
    a = [

        aufgabe(1, 0, "Ordne die Phase zu.",
                zuordnen(L, ["Vorbereitung", "Wettkampf", "Übergang"], [
                    ("Pause nach der Saison, andere Sportarten", "C"), ("viele lockere Kilometer, Technik", "A"),
                    ("wenig Umfang, hohe Intensität, Turniere", "B")])),
        aufgabe(2, 0, "Welches Prinzip ist gemeint?",
                felder(L, [("Immer dieselbe Übung bringt irgendwann nichts mehr.", "Variation"),
                           ("Nach drei Wochen Pause ist die Form weg.", "Kontinuität"),
                           ("Eine Woche später läuft man 5 min länger.", "progressive Steigerung")], 3, 48)),
        aufgabe(3, 1, "Warum braucht ein Sportler eine Übergangsphase?",
                linien(L, 2, "Körper und Kopf müssen sich nach der Saison erholen. Kleine Verletzungen heilen aus, die Motivation kommt zurück.")),
        aufgabe(4, 1, "Warum steigert man zuerst die Häufigkeit, dann den Umfang und zuletzt die Intensität?",
                linien(L, 3, "Der Körper gewöhnt sich zuerst an regelmäßige, leichte Belastung. Hohe Intensität belastet am stärksten. "
                             "Wer zu früh intensiv trainiert, riskiert Überlastung und Verletzungen.")),
        aufgabe(5, 2, "Erstelle einen Plan für 6 Wochen, um im Coopertest 300 m weiter zu laufen. Gib Häufigkeit, Inhalte und Steigerung an.",
                linien(L, 5, "Woche 1 bis 2: zweimal 20 min locker. Woche 3 bis 4: dreimal, davon einmal 4 · 400 m zügig. "
                             "Woche 5: dreimal, einmal 6 · 400 m. Woche 6: zweimal locker, kurz vor dem Test Ruhe. Tagebuch führen.")),
        aufgabe(6, 1, "Lege ein Trainingstagebuch an: Zeichne eine Tabelle mit allen nötigen Spalten und trage ein Beispiel ein.",
                karo(L, 28, "Spalten: Datum, Training, Dauer/Umfang, Intensität, Gefühl, Schlaf, Besonderes. Beispiel: 12.11., Dauerlauf, 30 min, Borg 12, gut, 8 h, -")),
        aufgabe(7, 2, "Ein Spieler ist in der Wettkampfphase nie richtig in Form. Woran könnte es in der Vorbereitung gelegen haben? Nenne zwei Möglichkeiten.",
                linien(L, 3, "Zu wenig Grundlagentraining in der Vorbereitung, oder zu intensiv ohne Erholung, sodass er müde in die Saison gestartet ist.")),
    ]
    return blatt(TE, 3, "Trainingsplanung", v,
                 ["Periodisierung: Vorbereitung, Wettkampf, Übergang.",
                  "Belastung steigern: erst Häufigkeit, dann Umfang, dann Intensität.",
                  "Ein Plan braucht ein klares Ziel und wird angepasst."], a)


# ================================================================== Verletzungen vermeiden
VZ = "Verletzungen vermeiden"


def vz1(L):
    v = abschnitt("A", "Der Bewegungsapparat")
    v += P("Damit wir uns bewegen können, arbeiten mehrere Strukturen zusammen. Wer sie kennt, versteht auch Verletzungen besser.")
    v += tabelle(["Struktur", "Aufgabe", "typische Verletzung"],
                 [["Muskel", "zieht sich zusammen und bewegt die Knochen", "Zerrung, Muskelfaserriss, Prellung"],
                  ["Sehne", "verbindet Muskel und Knochen, überträgt die Kraft", "Reizung (z. B. Achillessehne), Riss"],
                  ["Band", "verbindet Knochen mit Knochen, stabilisiert Gelenke", "Bänderdehnung, Bänderriss (z. B. Sprunggelenk)"],
                  ["Knorpel", "überzieht Gelenkflächen, dämpft und lässt gleiten", "Meniskusriss, Knorpelschaden im Knie"],
                  ["Knochen", "Stütze und Hebel für die Muskeln", "Bruch, Ermüdungsbruch"]])
    v += abschnitt("B", "Akute und chronische Verletzungen")
    v += P("<b>Akute Verletzungen</b> entstehen plötzlich durch einen Unfall: Umknicken, Zusammenstoß, Sturz. "
           "<b>Überlastungsschäden</b> entwickeln sich langsam, wenn eine Struktur immer wieder zu stark belastet wird, "
           "zum Beispiel bei zu schneller Steigerung des Lauftrainings. Typische Anzeichen sind Schmerzen, die beim Training zunehmen "
           "und morgens oder nach dem Sport anhalten.")
    v += abschnitt("C", "Heilungszeiten")
    v += P("Muskeln sind gut durchblutet und heilen schnell, eine Zerrung oft in 1 bis 2 Wochen. Sehnen, Bänder und Knorpel sind schlecht durchblutet "
           "und brauchen viel länger: Ein Bänderriss im Sprunggelenk braucht 6 Wochen und mehr. Ein Knochenbruch heilt meist in 6 bis 8 Wochen, "
           "danach muss die Kraft erst wieder aufgebaut werden. Wer zu früh voll einsteigt, riskiert einen Rückfall.")
    v += abschnitt("D", "Wachstum")
    v += P("Im Wachstumsschub wachsen die Knochen schneller als Muskeln und Sehnen sich anpassen. Die Sehnenansätze, etwa unterhalb der Kniescheibe "
           "oder an der Ferse, sind dann besonders empfindlich. Schmerzen dort nach Sprüngen sollte man ernst nehmen und die Belastung verringern.")

    v += abschnitt("E", "Zurück in den Sport")
    v += P("Nach einer Verletzung geht man stufenweise zurück: Zuerst muss der Alltag schmerzfrei gehen. Dann folgt lockeres Training ohne Sprünge "
           "und Richtungswechsel, danach sportartspezifisches Training und erst zuletzt Wettkampf. Jede Stufe darf erst beginnen, wenn die vorherige "
           "ohne Schmerzen klappt.")
    a = [

        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Eine {} verbindet Muskel und Knochen. Ein {} verbindet Knochen mit Knochen. Der {} dämpft im Gelenk.",
                ["Sehne", "Band", "Knorpel"], ["Knorpel", "Sehne", "Band"], 26)),
        aufgabe(2, 0, "Akut oder Überlastung? Schreibe a oder ü.",
                zuordnen(L, ["a = akut", "ü = Überlastung"], [
                    ("Umgeknickt beim Basketball", "a"), ("Seit Wochen Schmerzen an der Achillessehne beim Laufen", "ü"),
                    ("Zusammenstoß mit Prellung", "a"), ("Ermüdungsbruch nach starker Steigerung des Trainings", "ü")])),
        aufgabe(3, 1, "Warum heilen Bänder und Sehnen langsamer als Muskeln?",
                linien(L, 2, "Sie sind schlecht durchblutet. Es kommen weniger Baustoffe und Sauerstoff zur verletzten Stelle.")),
        aufgabe(4, 1, "Woran erkennt man einen Überlastungsschaden? Wie entsteht er?",
                linien(L, 3, "Der Schmerz entwickelt sich langsam, wird beim Training stärker und bleibt nach dem Sport oder am Morgen. "
                             "Er entsteht, wenn eine Struktur immer wieder zu stark belastet wird, z. B. bei zu schneller Steigerung.")),
        aufgabe(5, 2, "Ein 14-Jähriger hat nach dem Hochsprungtraining Schmerzen unter der Kniescheibe. Er ist gerade stark gewachsen. "
                      "Was könnte die Ursache sein und was rätst du ihm?",
                linien(L, 4, "Der Sehnenansatz ist im Wachstum überlastet. Sprungbelastung reduzieren, nicht mit Schmerzen springen, "
                             "kühlen und bei anhaltenden Beschwerden zum Arzt.")),
        aufgabe(6, 2, "Beschreibe die Stufen der Rückkehr nach einem Bänderriss und begründe, warum man keine überspringen sollte.",
                linien(L, 4, "Erst Alltag schmerzfrei, dann lockeres Training ohne Sprünge, dann sportartspezifisch, zuletzt Wettkampf. "
                             "Das Band ist erst nach Wochen belastbar. Wer zu früh voll spielt, reißt es leicht erneut.")),
        aufgabe(7, 1, "Wähle eine Verletzung aus der Tabelle. Beschreibe, wie sie im Sport passieren kann und wie man ihr vorbeugt.",
                linien(L, 3, "Beispiel Bänderriss im Sprunggelenk: beim Landen auf dem Fuß eines Gegners umknicken. Vorbeugen: Gleichgewichtstraining, "
                             "kräftige Wadenmuskeln, gute Schuhe.")),
    ]
    return blatt(VZ, 1, "Muskeln, Sehnen, Bänder", v,
                 ["Muskel, Sehne, Band, Knorpel, Knochen haben verschiedene Aufgaben.",
                  "Akute Verletzungen und Überlastungsschäden unterscheiden.",
                  "Sehnen und Bänder heilen langsam, zu früher Einstieg führt zum Rückfall."], a)


def vz2(L):
    v = abschnitt("A", "Ruhe bewahren: die Rettungskette")
    v += P("Bei einem Notfall in der Sporthalle zählt jede Minute. Die Rettungskette zeigt, was in welcher Reihenfolge passiert:")
    v += ('<div style="display:flex;gap:1.5mm;align-items:center;justify-content:center;margin:1mm 0 2mm 0;font-weight:600;font-size:9.5pt;flex-wrap:wrap">'
          + " ➜ ".join(f'<span class="box" style="padding:.8mm 2mm">{t}</span>'
                       for t in ("Absichern", "Notruf 112", "Erste Hilfe", "Rettungsdienst", "Krankenhaus")) + '</div>')
    v += abschnitt("B", "Bewusstsein und Atmung prüfen")
    v += P("<b>1 Ansprechen und anfassen:</b> Laut fragen „Hören Sie mich?“, an den Schultern rütteln.<br>"
           "<b>2 Atmung prüfen:</b> Kopf überstrecken, Kinn anheben. Bis zu 10 Sekunden hören, sehen, fühlen, ob die Person normal atmet.<br>"
           "<b>3 Entscheiden:</b> Reagiert nicht, atmet normal: stabile Seitenlage, Notruf. Reagiert nicht, atmet nicht normal: Notruf, Wiederbelebung.")
    v += abschnitt("C", "Stabile Seitenlage")
    v += P("Sie hält die Atemwege frei, weil Zunge und Erbrochenes nicht in den Rachen fallen. So geht es:<br>"
           "1. Neben die Person knien, den nahen Arm angewinkelt nach oben legen.<br>"
           "2. Den fernen Arm über die Brust holen, Handrücken an die Wange legen.<br>"
           "3. Das ferne Bein am Knie aufstellen und die Person zu sich herüberdrehen.<br>"
           "4. Das obere Bein so ausrichten, dass Hüfte und Knie rechtwinklig sind.<br>"
           "5. Kopf überstrecken, Mund leicht öffnen. Atmung weiter kontrollieren, zudecken.")
    v += abschnitt("D", "Wiederbelebung")
    v += P("Atmet die Person nicht normal, beginnt man sofort mit der <b>Herzdruckmassage</b>: Handballen auf die Mitte der Brust, "
           "mit gestreckten Armen <b>5 bis 6 cm tief</b> drücken, <b>100 bis 120 Mal pro Minute</b>. Wer es gelernt hat, beatmet nach 30 Drücken zweimal. "
           "Wenn ein Defibrillator (AED) da ist, einschalten und den Anweisungen folgen. Nicht aufhören, bis der Rettungsdienst übernimmt. "
           "Falsch machen kann man nur eins: nichts tun.")

    v += abschnitt("E", "Muss ich helfen?")
    v += P("Ja. In Deutschland ist jeder verpflichtet, im Notfall zumutbare Hilfe zu leisten. Wer nicht hilft, obwohl er könnte, "
           "macht sich wegen unterlassener Hilfeleistung strafbar. Niemand muss sich dabei selbst in Gefahr bringen, und schon der Notruf ist Hilfe. "
           "Wer Erste Hilfe leistet, ist gesetzlich unfallversichert. Wer in guter Absicht hilft, muss keine Angst vor Strafe haben, "
           "auch wenn nicht alles perfekt klappt.")
    a = [

        aufgabe(1, 0, "Bringe die Rettungskette in die richtige Reihenfolge.",
                reihenfolge(L, ["Absichern", "Notruf 112", "Erste Hilfe", "Rettungsdienst", "Krankenhaus"],
                            ["Erste Hilfe", "Krankenhaus", "Absichern", "Rettungsdienst", "Notruf 112"])),
        aufgabe(2, 0, "Was tust du? Ordne zu.",
                zuordnen(L, ["stabile Seitenlage und Notruf", "Notruf und Herzdruckmassage", "ansprechen, Wunde versorgen"], [
                    ("Person reagiert nicht, atmet normal.", "A"),
                    ("Person reagiert nicht, atmet nicht.", "B"),
                    ("Person ist wach und hat eine Schürfwunde.", "C")])),
        aufgabe(3, 1, "Warum legt man eine bewusstlose Person in die stabile Seitenlage?",
                linien(L, 2, "Die Atemwege bleiben frei. Zunge und Erbrochenes können nicht in den Rachen fallen, die Person erstickt nicht.")),
        aufgabe(4, 1, "Beschreibe die stabile Seitenlage in eigenen Worten so, dass jemand sie danach durchführen kann.",
                linien(L, 4, "Neben die Person knien, nahen Arm nach oben legen. Fernen Arm über die Brust, Hand an die Wange. Fernes Bein aufstellen "
                             "und die Person zu sich drehen. Oberes Bein rechtwinklig legen, Kopf überstrecken, Mund öffnen, Atmung kontrollieren.")),
        aufgabe(5, 2, "Ein Mitschüler bricht in der Halle zusammen und atmet nicht normal. Beschreibe, was in den ersten zwei Minuten passieren muss.",
                linien(L, 4, "Laut um Hilfe rufen, eine Person ruft 112, eine holt den Defibrillator. Sofort Herzdruckmassage: Mitte der Brust, "
                             "5 bis 6 cm tief, 100 bis 120 Mal pro Minute. Defi anschalten und den Anweisungen folgen, nicht aufhören.")),
        aufgabe(6, 2, "Viele trauen sich nicht zu helfen, aus Angst, etwas falsch zu machen. Was antwortest du? Nutze den Text.",
                linien(L, 3, "Der einzige Fehler ist, nichts zu tun. Man ist versichert, und wer in guter Absicht hilft, wird nicht bestraft. "
                             "Die Leitstelle unter 112 erklärt am Telefon, was zu tun ist.")),
    ]
    return blatt(VZ, 2, "Erste Hilfe im Notfall", v,
                 ["Absichern, Notruf 112, Erste Hilfe.",
                  "Bewusstlos mit Atmung: stabile Seitenlage.",
                  "Keine normale Atmung: Herzdruckmassage 100 bis 120 pro Minute."], a)


def vz3(L):
    v = abschnitt("A", "Aufwärmen mit Plan")
    v += P("Ein gutes Aufwärmen bereitet Herz-Kreislauf, Muskeln, Gelenke und Nervensystem vor. Die Körpertemperatur steigt, "
           "Muskeln werden elastischer, Reaktionen schneller. Ein bewährter Aufbau in drei Phasen:")
    v += kacheln([
        ("#d9efd8", "1 Allgemein", "5 Minuten", "Lockeres Laufen, Seilspringen, kleine Spiele. Puls steigt langsam."),
        ("#dbe8f5", "2 Mobilisieren", "5 Minuten", "Dynamische Bewegungen durch den ganzen Bewegungsumfang: Beinpendel, Armkreisen, Ausfallschritte mit Drehung."),
        ("#fbe9c2", "3 Speziell", "5 Minuten", "Sportartspezifisch: Steigerungsläufe, Sprünge, Würfe, Pässe in Spieltempo."),
    ], cols=3)
    v += abschnitt("B", "Dehnen: statisch oder dynamisch?")
    v += P("<b>Statisches Dehnen</b> heißt, eine Dehnposition 20 bis 30 Sekunden zu halten. Direkt vor Sprint- oder Sprungbelastungen "
           "kann es die Schnellkraft kurzfristig etwas senken. Es eignet sich eher nach dem Training oder als eigene Einheit, um beweglicher zu werden.<br>"
           "<b>Dynamisches Dehnen</b> bedeutet kontrollierte, schwunghafte Bewegungen bis an die Grenze des Bewegungsumfangs. "
           "Es passt gut ins Aufwärmen.")
    v += abschnitt("C", "Ausgleich und Haltung")
    v += P("Wer viel sitzt, bekommt oft verkürzte Hüftbeuger, eine schwache Rumpf- und Gesäßmuskulatur und einen runden Rücken. "
           "Auch einseitige Sportarten wie Tennis oder Handball belasten eine Körperseite stärker. "
           "<b>Ausgleichstraining</b> kräftigt die schwächeren Muskeln und dehnt die verkürzten. Rumpfstabilität ist dabei der wichtigste Baustein: "
           "Ein stabiler Rumpf schützt den Rücken und verbessert jede Bewegung.")
    v += abschnitt("D", "Weitere Bausteine")
    v += P("Passende Schuhe, Schutzausrüstung (Schienbeinschoner, Mundschutz), sichere Geräte, fair spielen und Müdigkeit ernst nehmen. "
           "Die meisten Verletzungen passieren am Ende einer Einheit, wenn Konzentration und Kraft nachlassen.")
    v += abschnitt("E", "Müdigkeit erkennen")
    v += P("Ermüdung kündigt sich an: Die Technik wird unsauber, man reagiert langsamer, landet härter und macht mehr Fehler. "
           "Wer das bei sich bemerkt, sollte eine Pause machen oder die Intensität senken. Gute Trainer legen schwierige und riskante Übungen "
           "an den Anfang einer Einheit, wenn alle noch frisch sind.")
    a = [

        aufgabe(1, 0, "Nenne die drei Phasen des Aufwärmens mit je einem Beispiel.",
                felder(L, [("Phase 1", "allgemein: traben"), ("Phase 2", "mobilisieren: Beinpendel"), ("Phase 3", "speziell: Steigerungsläufe")], 3, 48)),
        aufgabe(2, 0, "Statisch oder dynamisch gedehnt? Schreibe s oder d.",
                felder(L, [("Beinpendeln vor dem Sprint", "d"), ("Wade 30 s an der Wand halten", "s"),
                           ("Armkreisen", "d"), ("Oberschenkel im Sitzen nach dem Lauf halten", "s")], 4, 20)),
        aufgabe(3, 1, "Erkläre den Unterschied zwischen statischem und dynamischem Dehnen und wann man welches einsetzt.",
                linien(L, 3, "Statisch: Position 20 bis 30 Sekunden halten, eher nach dem Training oder als eigene Einheit. Dynamisch: kontrollierte "
                             "schwunghafte Bewegungen, passt ins Aufwärmen, weil es die Schnellkraft nicht senkt.")),
        aufgabe(4, 1, "Warum ist ein stabiler Rumpf für fast jede Sportart wichtig?",
                linien(L, 3, "Er überträgt Kraft zwischen Beinen und Armen, schützt den Rücken und sorgt für Gleichgewicht und Kontrolle.")),
        aufgabe(5, 2, "Erstelle ein 15-minütiges Aufwärmprogramm für eine Volleyballstunde mit allen drei Phasen.",
                linien(L, 4, "5 min: traben, Hopserlauf, seitlich laufen. 5 min: Armkreisen, Schulterkreisen, Ausfallschritte, Beinpendel. "
                             "5 min: pritschen und baggern zu zweit, Sprünge am Netz, Angriffsschläge locker.")),
        aufgabe(6, 2, "Ein Handballer klagt über Schulterschmerzen auf der Wurfseite. Was könnte die Ursache sein und welches Ausgleichstraining schlägst du vor?",
                linien(L, 4, "Einseitige Belastung, die Schultermuskulatur hinten ist schwach. Ausgleich: hintere Schulter und oberen Rücken kräftigen, "
                             "z. B. Rudern mit Band, Rumpf stabilisieren, Brustmuskel dehnen.")),
        aufgabe(7, 2, "Du sitzt täglich viele Stunden. Welche Folgen kann das haben und welche zwei Übungen würdest du als Ausgleich machen?",
                linien(L, 3, "Verkürzte Hüftbeuger, schwacher Rumpf und Gesäß, runder Rücken. Ausgleich: Hüftbeuger im Ausfallschritt dehnen, "
                             "Unterarmstütz und Superman für den Rumpf.")),
    ]
    return blatt(VZ, 3, "Vorbeugen: Aufwärmen, Dehnen, Ausgleich", v,
                 ["Aufwärmen: allgemein, mobilisieren, speziell.",
                  "Vor Sprint und Sprung dynamisch statt statisch dehnen.",
                  "Ausgleichstraining und Rumpfstabilität schützen vor Überlastung."], a)


# ================================================================== Regeln und Spielfeld
RS = "Regeln und Spielfeld"


def rs1(L):
    v = abschnitt("A", "Das Feld")
    v += P("Volleyball wird auf einem <b>18 m langen</b> und <b>9 m breiten</b> Feld gespielt. Das Netz hängt bei den Männern auf <b>2,43 m</b>, "
           "bei den Frauen auf <b>2,24 m</b>, im Schulsport oft niedriger. Die <b>Angriffslinie</b> liegt 3 m vom Netz entfernt.")
    v += f'<div style="width:125mm;margin:1mm auto 1mm auto">{volleyballfeld(True)}</div>'
    v += abschnitt("B", "Die wichtigsten Regeln")
    v += P("<b>Mannschaft:</b> 6 Spieler, 3 vorne, 3 hinten.<br>"
           "<b>Ballkontakte:</b> Jede Mannschaft darf den Ball höchstens <b>dreimal</b> berühren, bevor er über das Netz muss. "
           "Ein Spieler darf nicht zweimal hintereinander spielen. Die Berührung beim Block zählt nicht als Kontakt.<br>"
           "<b>Netz:</b> Das Netz darf beim Spielen des Balls nicht berührt werden.<br>"
           "<b>Hinterspieler</b> dürfen nicht vor der Angriffslinie über Netzhöhe angreifen oder blocken.<br>"
           "<b>Punkte:</b> Jeder Ballwechsel bringt einen Punkt. Ein Satz geht bis 25 Punkte, mit mindestens 2 Punkten Vorsprung. "
           "Gewonnen hat, wer 3 Sätze gewinnt. Ein möglicher fünfter Satz geht nur bis 15.")
    v += abschnitt("C", "Rotation")
    v += P("Die Positionen sind von I bis VI nummeriert, Position I ist hinten rechts, dort wird aufgeschlagen. "
           "Gewinnt eine Mannschaft das Aufschlagrecht vom Gegner zurück, rotieren alle Spieler um eine Position <b>im Uhrzeigersinn</b>. "
           "So kommt jeder einmal an jede Position und auch zum Aufschlag.")

    v += abschnitt("D", "Der Libero")
    v += P("Viele Mannschaften setzen einen <b>Libero</b> ein, einen Abwehrspezialisten in andersfarbigem Trikot. Er darf nur auf den hinteren Positionen spielen "
           "und für jeden Hinterspieler ohne Anmeldung eingewechselt werden. Er darf nicht aufschlagen, nicht blocken und den Ball nicht von oberhalb der "
           "Netzkante ins gegnerische Feld schlagen. Seine Aufgabe ist eine sichere Annahme und Abwehr.")
    a = [

        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Das Feld ist {} m lang und {} m breit. Eine Mannschaft darf den Ball höchstens {} berühren. "
                "Ein Satz geht bis {} Punkte.",
                ["18", "9", "dreimal", "25"], ["25", "9", "dreimal", "18"], 20)),
        aufgabe(2, 0, "Fehler oder kein Fehler? Kreuze an, wenn es ein Fehler ist.", richtig_falsch(L, [
            ("Eine Mannschaft spielt den Ball viermal.", True),
            ("Ein Spieler blockt und spielt danach den Ball als Erster weiter.", False),
            ("Ein Spieler berührt beim Angriff das Netz.", True),
            ("Ein Hinterspieler greift vor der Angriffslinie über Netzhöhe an.", True)]).replace(">richtig<", ">Fehler<").replace(">falsch<", ">kein Fehler<")),
        aufgabe(3, 1, "Spielstand 24 : 23. Was passiert, wenn die zweite Mannschaft den nächsten Punkt macht? Wann ist der Satz zu Ende?",
                linien(L, 2, "24 : 24, es geht weiter. Der Satz ist zu Ende, wenn eine Mannschaft 2 Punkte Vorsprung hat, z. B. 26 : 24.")),
        aufgabe(4, 1, "Was ist ein Libero, was darf er nicht, und warum gibt es ihn?",
                linien(L, 3, "Ein Abwehrspezialist im andersfarbigen Trikot, nur hinten. Er darf nicht aufschlagen, nicht blocken und nicht von oben angreifen. "
                             "Er sorgt für eine sichere Annahme, das macht das Spiel länger und spannender.")),
        aufgabe(5, 1, "Zeichne die sechs Positionen und trage die Nummern ein. Zeichne mit einem Pfeil die Richtung der Rotation.",
                karo(L, 28, "Netz oben: vorne IV, III, II (von links nach rechts), hinten V, VI, I; Pfeil im Uhrzeigersinn")),
        aufgabe(6, 2, "Warum gibt es beim Volleyball die Rotation? Was würde ohne sie passieren?",
                linien(L, 3, "Damit jeder an jede Position kommt und aufschlägt. Ohne sie würden die besten Angreifer immer vorne stehen "
                             "und die anderen nur hinten. Die Rotation verlangt vielseitige Spieler.")),
        aufgabe(7, 2, "Erkläre einem Neuling in fünf Sätzen, wie ein Volleyballspiel abläuft.",
                linien(L, 4, "Zwei Teams mit je sechs Spielern stehen sich am Netz gegenüber. Ein Spieler schlägt auf, der Gegner nimmt an. "
                             "Jedes Team hat drei Kontakte, um den Ball zurückzuspielen. Fällt der Ball im Feld oder macht ein Team einen Fehler, gibt es einen Punkt. "
                             "Wer zuerst drei Sätze bis 25 gewinnt, hat das Spiel gewonnen.")),
    ]
    return blatt(RS, 1, "Volleyball: Regeln", v,
                 ["Feld 18 m mal 9 m, 6 Spieler.",
                  "Höchstens 3 Ballkontakte, Block zählt nicht.",
                  "Rotation im Uhrzeigersinn beim Aufschlagwechsel."], a)


def rs2(L):
    v = abschnitt("A", "Die Grundtechniken")
    v += kacheln([
        ("#dbe8f5", "Pritschen (oberes Zuspiel)", "",
         "Hände über der Stirn, Finger bilden ein Körbchen, Daumen und Zeigefinger formen ein Dreieck. "
         "Unter den Ball laufen, Knie leicht gebeugt, den Ball mit den Fingern abfedern und aus Armen und Beinen nach oben strecken."),
        ("#d9efd8", "Baggern (unteres Zuspiel)", "",
         "Hände ineinanderlegen, Daumen parallel, Arme gestreckt zu einer Fläche. Der Ball wird auf den Unterarmen gespielt, "
         "nicht mit den Händen. Die Bewegung kommt aus den Beinen, die Arme schwingen nicht."),
        ("#fbe9c2", "Aufschlag von unten", "",
         "Seitlich zum Netz stehen, Ball in der Hand vor dem Körper. Mit der anderen Hand in einer Pendelbewegung von unten schlagen. "
         "Sicher, gut für Anfänger."),
        ("#f6d9d6", "Angriffsschlag", "",
         "Anlauf, beidbeiniger Absprung, Schlagarm weit nach hinten oben, Ball am höchsten Punkt vor dem Körper mit der offenen Hand treffen."),
    ])
    v += abschnitt("B", "Der Spielaufbau")
    v += P("Ein typischer Ballwechsel läuft so ab: Die Annahme kommt per <b>Bagger</b> zum Zuspieler am Netz (1. Kontakt). "
           "Der Zuspieler <b>pritscht</b> den Ball hoch an die Antenne oder in die Mitte (2. Kontakt). "
           "Ein Angreifer schlägt den Ball ins gegnerische Feld (3. Kontakt). Gute Mannschaften nutzen alle drei Kontakte, statt den Ball sofort zurückzuspielen.")
    v += abschnitt("C", "Häufige Fehler")
    v += P("Beim Pritschen: Ball zu tief vor der Brust, Finger steif, nicht unter den Ball gelaufen.<br>"
           "Beim Baggern: Arme gebeugt, mit den Händen gespielt, aus den Armen geschlagen statt aus den Beinen.<br>"
           "Im Spiel: niemand fühlt sich zuständig. Dagegen hilft lautes Rufen: „Ich!“ oder „Hab ihn!“.")

    v += abschnitt("D", "Taktik: Aufschlag und Annahme")
    v += P("Schon der Aufschlag ist ein Angriff. Gute Spieler schlagen gezielt dorthin auf, wo der Gegner Probleme hat: auf einen unsicheren Annahmespieler, "
           "in die Lücke zwischen zwei Spielern oder kurz hinter das Netz, wenn alle weit hinten stehen. Die annehmende Mannschaft stellt sich so auf, "
           "dass die sichersten Spieler möglichst viel Feld abdecken, und spricht vor jedem Aufschlag kurz ab, wer welchen Bereich übernimmt.")
    a = [

        aufgabe(1, 0, "Pritschen oder Baggern? Schreibe P oder B.",
                felder(L, [("Ball kommt hoch, über Kopfhöhe", "P"), ("Ball kommt flach unter Hüfthöhe", "B"),
                           ("harter Aufschlag des Gegners", "B"), ("Zuspiel an den Angreifer", "P")], 4, 20)),
        aufgabe(2, 0, "Bringe einen Ballwechsel in die richtige Reihenfolge.",
                reihenfolge(L, ["Gegner schlägt auf", "Annahme mit Bagger", "Zuspiel mit Pritschen", "Angriffsschlag"],
                            ["Angriffsschlag", "Annahme mit Bagger", "Gegner schlägt auf", "Zuspiel mit Pritschen"])),
        aufgabe(3, 1, "Beschreibe das Baggern so genau, dass ein Anfänger es nachmachen kann.",
                linien(L, 4, "Hände ineinanderlegen, Daumen nebeneinander, Arme gestreckt zu einer Fläche. Leicht in die Knie gehen, hinter den Ball laufen. "
                             "Den Ball auf den Unterarmen treffen und die Bewegung aus den Beinen machen, die Arme nicht schwingen.")),
        aufgabe(4, 1, "Zeichne die Handhaltung beim Pritschen (Blick von vorne auf die Hände).",
                karo(L, 22, "Zwei Hände über der Stirn, Daumen und Zeigefinger bilden ein Dreieck, Finger gespreizt")),
        aufgabe(5, 2, "Ein Mitspieler spielt jeden Ball sofort mit einem Kontakt zurück. Erkläre ihm, warum das ungünstig ist.",
                linien(L, 3, "Mit einem Kontakt kommt der Ball meist hoch und ungefährlich über das Netz. Mit Annahme, Zuspiel und Angriff "
                             "kann man gezielt und hart angreifen und hat mehr Kontrolle.")),
        aufgabe(6, 2, "Wohin würdest du aufschlagen, wenn ein Gegner bei der Annahme unsicher ist und alle weit hinten stehen? Begründe.",
                linien(L, 3, "Auf den unsicheren Spieler oder kurz hinter das Netz. Der Gegner muss weit nach vorne laufen und kann den Ball "
                             "kaum kontrolliert annehmen.")),
        aufgabe(7, 1, "Warum ist es wichtig, im Spiel laut zu rufen, wer den Ball nimmt?",
                linien(L, 2, "Sonst fühlt sich niemand zuständig oder zwei laufen zusammen. Rufen sorgt für Klarheit und verhindert Zusammenstöße.")),
    ]
    return blatt(RS, 2, "Volleyball: Technik und Spiel", v,
                 ["Pritschen für hohe Bälle, Baggern für flache.",
                  "Annahme, Zuspiel, Angriff: alle drei Kontakte nutzen.",
                  "Laut rufen, wer den Ball nimmt."], a)


def rs3(L):
    v = abschnitt("A", "Kugelstoßen")
    v += P("Gestoßen wird aus einem Kreis mit 2,135 m Durchmesser. Vorne liegt ein Stoßbalken. In Klasse 9 und 10 wiegt die Kugel <b>5 kg</b>.")
    v += P("<b>Regeln:</b> Die Kugel wird am Hals angelegt und mit einer Hand <b>gestoßen, nicht geworfen</b>. Der Ellbogen bleibt hinter der Kugel. "
           "Man darf den Kreis erst verlassen, wenn die Kugel gelandet ist, und zwar durch die <b>hintere Hälfte</b>. "
           "Wer auf oder über den Balken oder den Kreisrand tritt, macht einen Fehlversuch. Die Kugel muss im Sektor landen. "
           "Gemessen wird vom Abdruck der Kugel zum Innenrand des Kreises.")
    v += abschnitt("B", "Weitsprung")
    v += P("Der Absprung erfolgt vom Absprungbalken. Wer mit der Fußspitze über die Absprunglinie tritt, hat einen <b>Übertritt</b>, "
           "der Versuch ist ungültig. Gemessen wird vom <b>hintersten Abdruck</b> im Sand senkrecht zur Absprunglinie. "
           "Fasst man also beim Landen nach hinten in den Sand, zählt dieser Abdruck. In der Schule wird oft aus einer Absprungzone gesprungen "
           "und vom Fußabdruck des Absprungs gemessen.")
    v += abschnitt("C", "Hochsprung")
    v += P("Abgesprungen wird <b>einbeinig</b>. Die Latte darf nicht herunterfallen. Wer dreimal hintereinander reißt, scheidet aus. "
           "Man darf eine Höhe auslassen. Bei gleicher Höhe gewinnt, wer weniger Fehlversuche hat.")
    v += abschnitt("D", "Sprint")
    v += P("Auf Kurzstrecken wird aus dem Tiefstart gestartet, mit den Kommandos „Auf die Plätze“, „Fertig“ und dem Startschuss. "
           "Wer vor dem Schuss startet, macht einen <b>Fehlstart</b>. Gestoppt wird, wenn der <b>Oberkörper</b> (nicht Kopf, Arm oder Bein) "
           "die Ziellinie erreicht. Jeder bleibt in seiner Bahn.")

    v += abschnitt("E", "Technik: Kugelstoßen aus dem Stand")
    v += P("Seitlich zur Stoßrichtung stehen, die Kugel liegt am Hals, der Ellbogen zeigt zur Seite. Das Gewicht ist auf dem hinteren, gebeugten Bein. "
           "Dann wird das hintere Bein gestreckt und die Hüfte nach vorne gedreht. Erst danach stößt der Arm die Kugel schräg nach oben weg, "
           "etwa im Winkel von 40 Grad. Die Kraft kommt also von unten nach oben: Beine, Hüfte, Oberkörper, Arm.")
    v += abschnitt("F", "Staffel")
    v += P("Beim Staffellauf (4 · 100 m) muss der Stab innerhalb des <b>30 m langen Wechselraums</b> übergeben werden. Entscheidend ist die Position des Stabs, "
           "nicht die der Läufer. Der ankommende Läufer ruft ein Kommando, der Übernehmende streckt die Hand nach hinten. Fällt der Stab herunter, "
           "muss ihn der Läufer aufheben, der ihn verloren hat. Wer den Stab außerhalb des Wechselraums übergibt, wird disqualifiziert.")
    a = [

        aufgabe(1, 0, "Gültig oder ungültig? Kreuze an, wenn der Versuch ungültig ist.", richtig_falsch(L, [
            ("Die Kugel wird mit gestrecktem Arm geworfen.", True),
            ("Der Stoßer verlässt den Kreis nach vorne.", True),
            ("Beim Weitsprung landet die Fußspitze genau vor der Linie.", False),
            ("Beim Hochsprung springt jemand beidbeinig ab.", True)]).replace(">richtig<", ">ungültig<").replace(">falsch<", ">gültig<")),
        aufgabe(2, 1, "Ein Weitspringer landet bei 4,30 m, fällt aber nach hinten und stützt sich bei 3,85 m im Sand ab. Welche Weite zählt? Warum?",
                linien(L, 2, "3,85 m, weil vom hintersten Abdruck im Sand gemessen wird.")),
        aufgabe(3, 1, "Warum muss man beim Kugelstoßen den Kreis durch die hintere Hälfte verlassen?",
                linien(L, 2, "Sonst könnte man den Schwung nach vorne mitnehmen und über den Balken treten. Die Regel stellt sicher, dass man im Kreis bleibt.")),
        aufgabe(4, 1, "Beschreibe das Kugelstoßen aus dem Stand in vier Schritten. Erkläre, warum die Kraft von den Beinen kommen muss.",
                linien(L, 4, "Seitlich stehen, Kugel am Hals. Gewicht hinten, Bein gebeugt. Bein strecken, Hüfte drehen. Arm stößt schräg nach oben. "
                             "Die Beine sind die stärksten Muskeln. Nur mit dem Arm wäre der Stoß viel kürzer.")),
        aufgabe(5, 2, "Du bist Kampfrichter beim Kugelstoßen. Beschreibe, worauf du bei jedem Versuch achten musst.",
                linien(L, 4, "Kugel am Hals angelegt und gestoßen, Ellbogen hinter der Kugel. Kein Tritt auf Balken oder Kreisrand. "
                             "Kugel landet im Sektor. Verlassen erst nach der Landung durch die hintere Hälfte. Messen vom Abdruck zum Innenrand.")),
        aufgabe(6, 2, "Beim Sprint zählt der Oberkörper an der Ziellinie, nicht Kopf, Arm oder Fuß. Warum ist diese Regel sinnvoll?",
                linien(L, 3, "Kopf, Arme und Beine kann man nach vorne strecken, das wäre eine Verrenkung ohne echte Laufleistung. "
                             "Der Oberkörper zeigt eindeutig, wer zuerst da ist.")),
        aufgabe(7, 0, "Zeichne den Stoßkreis mit Stoßbalken und markiere, durch welche Hälfte man ihn verlassen muss.",
                karo(L, 22, "Kreis, Balken vorne, hintere Hälfte schraffiert und mit Pfeil nach hinten")),
    ]
    return blatt(RS, 3, "Leichtathletik: Wettkampfregeln", v,
                 ["Kugel: stoßen, nicht werfen, Kreis hinten verlassen.",
                  "Weitsprung: Übertritt ungültig, gemessen wird der hinterste Abdruck.",
                  "Hochsprung einbeinig, drei Fehlversuche, Sprint: Oberkörper zählt."], a)


# ------------------------------------------------------------------ Liste
def _e(thema, nr, titel, fn):
    return (f"{STUFE}/{thema}", f"{thema} {nr} – {titel}", fn)


BLAETTER = [
    _e("Essen und Trinken", 1, "Energiebilanz", et1),
    _e("Essen und Trinken", 2, "Ernährung für Sportler", et2),
    _e("Essen und Trinken", 3, "Körperbild und Diäten", et3),
    _e("Fair Play", 1, "Doping", fp1),
    _e("Fair Play", 2, "Respekt und Zivilcourage", fp2),
    _e("Fair Play", 3, "Sportwetten und Spielmanipulation", fp3),
    _e("Herz, Puls und Ausdauer", 1, "Energie für die Muskeln", hp1),
    _e("Herz, Puls und Ausdauer", 2, "Ausdauertraining planen", hp2),
    _e("Herz, Puls und Ausdauer", 3, "Anpassungen durch Training", hp3),
    _e("Training und Erholung", 1, "Krafttraining", te1),
    _e("Training und Erholung", 2, "Regeneration und Stress", te2),
    _e("Training und Erholung", 3, "Trainingsplanung", te3),
    _e("Verletzungen vermeiden", 1, "Muskeln, Sehnen, Bänder", vz1),
    _e("Verletzungen vermeiden", 2, "Erste Hilfe im Notfall", vz2),
    _e("Verletzungen vermeiden", 3, "Vorbeugen", vz3),
    _e("Regeln und Spielfeld", 1, "Volleyball, Regeln", rs1),
    _e("Regeln und Spielfeld", 2, "Volleyball, Technik und Spiel", rs2),
    _e("Regeln und Spielfeld", 3, "Leichtathletik, Wettkampfregeln", rs3),
]
