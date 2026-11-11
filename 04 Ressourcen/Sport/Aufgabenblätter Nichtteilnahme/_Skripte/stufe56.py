"""Blätter Klasse 5 und 6 (ohne Essen und Trinken, das steht in baue_blaetter.py)."""
from baue_blaetter import (abschnitt, aufgabe, gap, kachel, kopf, legende, linien, richtig_falsch,
                           seite, wichtig)

STUFE = "Klasse 5 und 6"
LOE = "#c2185b"


# ------------------------------------------------------------------ Hilfen
def P(t):
    return f"<p>{t}</p>"


def blatt(reihe_thema, nr, titel, vorder, wichtiges, aufgaben, stufe=STUFE):
    reihe = f"Sport ohne Mitmachen  |  {stufe}  |  {reihe_thema}, Blatt {nr}"
    v = kopf(reihe, titel)
    v += '<div class="hinweis">Lies den Text in Ruhe. Die Aufgaben stehen auf der Rückseite.</div>'
    v += vorder + wichtig(wichtiges)
    return seite(v) + seite(legende() + "".join(aufgaben))


def kacheln(liste, cols=2):
    return (f'<div class="spalten" style="grid-template-columns:repeat({cols},1fr);margin:1.5mm 0 1mm 0">'
            + "".join(kachel(*k) for k in liste) + "</div>")


def wortkasten(worte):
    return f'<div class="wortkasten">{" &nbsp;&nbsp; ".join(worte)}</div>'


def lueckentext(L, text, worte, kasten, breite=26):
    """text mit {} je Lücke, worte = Lösungen in Reihenfolge, kasten = Anzeige-Reihenfolge."""
    t = text.format(*[gap(L, w, breite) for w in worte])
    return wortkasten(kasten) + f'<p style="line-height:2.05">{t}</p>'


def sortieren(L, kategorien, kasten, hoehe=26):
    """kategorien: dict Überschrift -> Lösungsliste."""
    n = len(kategorien)
    sp = ""
    for k, items in kategorien.items():
        inh = "<br>".join(items) if L else ""
        sp += f'<div class="box" style="min-height:{hoehe}mm"><div class="t">{k}</div><div class="loe">{inh}</div></div>'
    return wortkasten(kasten) + f'<div class="spalten" style="grid-template-columns:repeat({n},1fr)">{sp}</div>'


def felder(L, paare, cols=4, breite=34):
    """paare: (Beschriftung, Lösung). Beschriftung über dem Kästchen."""
    it = "".join(f'<div>{a}<br>{gap(L, b, breite)}</div>' for a, b in paare)
    return f'<div class="spalten" style="grid-template-columns:repeat({cols},1fr);font-size:10pt;row-gap:2mm">{it}</div>'


def zuordnen(L, optionen, faelle, breite=10):
    """optionen: Liste Texte (A, B, ...), faelle: (Text, Lösungsbuchstabe)."""
    opt = "".join(f'<div><b>{chr(65+i)}</b> {o}</div>' for i, o in enumerate(optionen))
    rows = "".join(f'<tr><td>{t}</td><td class="x">{gap(L, b, breite)}</td></tr>' for t, b in faelle)
    return (f'<div class="wortkasten" style="display:grid;grid-template-columns:1fr 1fr;gap:.5mm 4mm">{opt}</div>'
            f'<table class="rf">{rows}</table>')


def karo(L, hoehe, loes=""):
    inh = f'<div class="loe" style="position:absolute;left:3mm;top:2mm;right:3mm">{loes}</div>' if (L and loes) else ""
    return f'<div class="karo" style="height:{hoehe}mm">{inh}</div>'


def reihenfolge(L, schritte, kasten_reihenfolge):
    """schritte: richtige Reihenfolge. Gezeigt wird kasten_reihenfolge mit Kästchen für die Nummer."""
    rows = "".join(f'<tr><td class="x">{gap(L, str(schritte.index(s) + 1), 9)}</td><td>{s}</td></tr>'
                   for s in kasten_reihenfolge)
    return f'<table class="rf">{rows}</table>'


# ------------------------------------------------------------------ Grafiken
def handballfeld(beschriftet=True):
    m, k = 22, 9  # Rand, Pixel pro Meter
    W, H = 40 * k, 20 * k
    yc = m + H / 2
    x0, x1 = m, m + W
    pf = 1.5 * k

    def bogen(x, r, rechts, strich):
        s = 1 if rechts else 0
        dx = r if rechts else -r
        return (f'<path d="M{x} {yc-pf-r} A{r} {r} 0 0 {s} {x+dx} {yc-pf} L{x+dx} {yc+pf} '
                f'A{r} {r} 0 0 {s} {x} {yc+pf+r}" fill="none" stroke="#fff" stroke-width="2.2" {strich}/>')

    o = [f'<svg viewBox="0 0 {W+2*m} {H+2*m}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Open Sans, Helvetica, sans-serif" font-size="11" font-weight="600">',
         f'<defs><clipPath id="feld"><rect x="{x0}" y="{m}" width="{W}" height="{H}"/></clipPath></defs>',
         f'<rect x="{x0}" y="{m}" width="{W}" height="{H}" fill="#6fa8dc" stroke="#fff" stroke-width="2.5"/>',
         f'<g clip-path="url(#feld)">',
         bogen(x0, 6 * k, True, ""), bogen(x1, 6 * k, False, ""),
         bogen(x0, 9 * k, True, 'stroke-dasharray="7 6"'), bogen(x1, 9 * k, False, 'stroke-dasharray="7 6"'),
         '</g>',
         f'<line x1="{m+W/2}" y1="{m}" x2="{m+W/2}" y2="{m+H}" stroke="#fff" stroke-width="2.2"/>',
         f'<line x1="{x0+7*k}" y1="{yc-k/2}" x2="{x0+7*k}" y2="{yc+k/2}" stroke="#fff" stroke-width="3"/>',
         f'<line x1="{x1-7*k}" y1="{yc-k/2}" x2="{x1-7*k}" y2="{yc+k/2}" stroke="#fff" stroke-width="3"/>',
         f'<rect x="{x0-k}" y="{yc-pf}" width="{k}" height="{2*pf}" fill="#e8706a" stroke="#333"/>',
         f'<rect x="{x1}" y="{yc-pf}" width="{k}" height="{2*pf}" fill="#e8706a" stroke="#333"/>']
    if beschriftet:
        lab = [(x0 + 3.2 * k, yc - 5.3 * k, "Torraum"), (x0 + 7.5 * k, yc - 7.2 * k, "Freiwurflinie"),
               (x0 + 9.2 * k, yc + 0.45 * k, "7-m-Linie"), (m + W / 2 + 4, m + 14, "Mittellinie"),
               (x1 - 3.2 * k, yc + 5.6 * k, "Torraum"), (x0 + 1, yc + 2.9 * k, "Tor")]
        for x, y, t in lab:
            o.append(f'<text x="{x}" y="{y}" fill="#111" text-anchor="{"start" if t in ("Mittellinie", "7-m-Linie", "Tor") else "middle"}">{t}</text>')
        o.append(f'<text x="{m+W/2}" y="{m+H+16}" text-anchor="middle" fill="#333">40 m lang, 20 m breit</text>')
    else:
        lab = [("A", x0 + 3 * k, yc - 4.6 * k), ("B", x0 + 7.5 * k, yc - 7.2 * k), ("C", x0 + 9.2 * k, yc + .45 * k),
               ("D", m + W / 2 + 6, m + 14), ("E", x0 - k / 2, yc + 3 * k)]
        for b, x, y in lab:
            o.append(f'<circle cx="{x}" cy="{y-4}" r="8" fill="#fff" stroke="#333"/>'
                     f'<text x="{x}" y="{y}" text-anchor="middle">{b}</text>')
    o.append("</svg>")
    return "".join(o)


def kurve():
    """Belastung, Erholung, stärker als vorher."""
    return ('<svg viewBox="0 0 360 150" width="100%" xmlns="http://www.w3.org/2000/svg" '
            'font-family="Open Sans, Helvetica, sans-serif" font-size="11" font-weight="600">'
            '<line x1="20" y1="70" x2="350" y2="70" stroke="#999" stroke-dasharray="5 4"/>'
            '<text x="22" y="62" fill="#666">so fit wie vorher</text>'
            '<path d="M20 70 L70 70 C95 70 100 125 130 125 C165 125 175 40 215 40 C255 40 280 62 350 66" '
            'fill="none" stroke="#1f6fb2" stroke-width="3.5"/>'
            '<text x="72" y="140" fill="#c0392b">1 Belastung: müde</text>'
            '<text x="150" y="108" fill="#2e7d32">2 Erholung</text>'
            '<text x="190" y="28" fill="#1f6fb2">3 stärker als vorher</text>'
            '<line x1="20" y1="10" x2="20" y2="145" stroke="#333" stroke-width="1.5"/>'
            '<text x="26" y="18" fill="#333">fit</text>'
            '</svg>')


# ================================================================== Fair Play
FP = "Fair Play"


def fp1(L):
    v = abschnitt("A", "Was heißt Fair Play?")
    v += P("Fair Play kommt aus dem Englischen und heißt „faires Spiel“. Wer fair spielt, hält sich an die Regeln. "
           "Er will gewinnen, aber nicht um jeden Preis. Er behandelt die anderen Spieler so, wie er selbst behandelt werden möchte.")
    v += abschnitt("B", "Fünf Regeln für faire Sportler")
    v += kacheln([
        ("#dbe8f5", "1 Regeln einhalten", "", "Ich spiele nach den Regeln, auch wenn es niemand sieht."),
        ("#d9efd8", "2 Gegner achten", "", "Der Gegner ist kein Feind. Ohne ihn gäbe es gar kein Spiel."),
        ("#fbe9c2", "3 Schiedsrichter akzeptieren", "", "Ich nehme Entscheidungen an, auch wenn ich anderer Meinung bin."),
        ("#f6d9d6", "4 Niemanden verletzen", "", "Ich foule nicht absichtlich und passe auf die anderen auf."),
        ("#e7def3", "5 Gut gewinnen und verlieren", "", "Ich lache Verlierer nicht aus und gratuliere dem Sieger."),
        ("#eeeeee", "Und ich gebe zu …", "", "… wenn der Ball im Aus war oder ich gefoult habe."),
    ])
    v += abschnitt("C", "Ein Beispiel aus dem Profisport")
    v += P("Im Fußball schießt eine Mannschaft den Ball absichtlich ins Aus, wenn ein Spieler der anderen Mannschaft verletzt am Boden liegt. "
           "So kann er behandelt werden. Danach bekommt die erste Mannschaft den Ball zurück. "
           "Keine Regel schreibt das vor. Die Spieler machen es trotzdem, weil es fair ist.")
    v += P("Fair Play gilt auch im Sportunterricht. Wer schummelt, andere auslacht oder absichtlich foult, "
           "verdirbt allen den Spaß. Wer fair spielt, macht das Spiel für alle besser.")
    v += abschnitt("D", "Fair Play wird belohnt")
    v += P("In Deutschland gibt es Fair-Play-Preise für Sportler und Mannschaften, die sich besonders fair verhalten haben. "
           "Auch Kinder- und Jugendmannschaften können so einen Preis bekommen. Fair spielen lohnt sich also, auch wenn man dabei kein Tor schießt.")
    a = [
        aufgabe(1, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Fair Play heißt „faires Spiel“.", True),
            ("Wer fair spielt, will nicht gewinnen.", False),
            ("Wenn es niemand sieht, darf ich die Regeln brechen.", False),
            ("Der Gegner ist kein Feind.", True),
            ("Ich gratuliere dem Sieger, auch wenn ich verloren habe.", True)])),
        aufgabe(2, 0, "Fair oder unfair? Schreibe die Nummern in das richtige Feld.",
                '<div class="wortkasten" style="line-height:1.55">① einem gestürzten Spieler aufhelfen &nbsp; ② den Gegner absichtlich schubsen '
                '&nbsp; ③ sagen „Der Ball war im Aus.“ &nbsp; ④ nach einer Niederlage den Ball wegtreten &nbsp; '
                '⑤ den Schiedsrichter beschimpfen &nbsp; ⑥ nach dem Spiel die Hand geben &nbsp; ⑦ beim Zählen schummeln &nbsp; ⑧ einen schwachen Spieler ermutigen</div>'
                f'<div class="spalten" style="grid-template-columns:1fr 1fr">'
                f'<div class="box" style="min-height:13mm"><div class="t">fair</div><div class="loe">{"① ③ ⑥ ⑧" if L else ""}</div></div>'
                f'<div class="box" style="min-height:13mm"><div class="t">unfair</div><div class="loe">{"② ④ ⑤ ⑦" if L else ""}</div></div></div>'),
        aufgabe(3, 0, "Setze die Wörter ein.", lueckentext(L,
                "Wer fair spielt, hält sich an die {}. Der {} ist kein Feind. Entscheidungen des {} nehme ich an. "
                "Nach dem Spiel {} ich dem Sieger.",
                ["Regeln", "Gegner", "Schiedsrichters", "gratuliere"],
                ["gratuliere", "Regeln", "Schiedsrichters", "Gegner"], 32)),
        aufgabe(4, 1, "Warum schießen Fußballer den Ball ins Aus, wenn ein Gegner verletzt am Boden liegt?",
                linien(L, 2, "Damit der verletzte Spieler behandelt werden kann. Es ist keine Regel, sondern fair.")),
        aufgabe(5, 1, "Erinnere dich an ein Spiel im Sportunterricht. Wer hat sich besonders fair verhalten und was hat er gemacht? (Keine Namen nötig.)",
                linien(L, 3, "Beispiel: Ein Mitschüler hat zugegeben, dass er den Ball zuletzt berührt hat, obwohl es niemand gesehen hat.")),
        aufgabe(6, 2, "Dein Team verliert knapp. Ein Mitspieler will dem Gegner aus Wut kein „Gut gespielt“ sagen. Was sagst du ihm? Begründe.",
                linien(L, 3, "Gib trotzdem die Hand. Die anderen waren heute besser, das gehört zum Sport. "
                             "Beim nächsten Mal willst du auch, dass man dir gratuliert.")),
        aufgabe(7, 1, "Warum macht ein Spiel mehr Spaß, wenn alle fair spielen?",
                linien(L, 2, "Es gibt keinen Streit, niemand wird verletzt und jeder hat die gleiche Chance zu gewinnen.")),
    ]
    return blatt(FP, 1, "Was ist Fair Play?", v,
                 ["Fair Play heißt: nach den Regeln spielen und die anderen achten.",
                  "Gewinnen wollen ist gut, aber nicht um jeden Preis.",
                  "Fair Play gilt auch im Sportunterricht."], a)


def fp2(L):
    v = abschnitt("A", "Gefühle beim Sport")
    v += P("Beim Sport erlebst du starke Gefühle. Nach einem Tor oder einem Sieg freust du dich riesig. "
           "Nach einer Niederlage bist du vielleicht traurig, enttäuscht oder wütend. Das ist ganz normal. "
           "Auch Profisportler fühlen so.")
    v += P("Wichtig ist, was du mit deinen Gefühlen machst. Wut darfst du spüren. "
           "Aber du darfst sie nicht an anderen auslassen: nicht schreien, nicht schubsen, nichts kaputt machen.")
    v += abschnitt("B", "Gut gewinnen")
    v += P("Auch Gewinnen muss man lernen. Freu dich, jubel mit deinem Team. Aber lache die Verlierer nicht aus "
           "und gib nicht an. Sag lieber: „Gut gespielt!“ Beim nächsten Mal kann es nämlich andersherum sein.")
    v += abschnitt("C", "Gut verlieren: der Stopp-Plan")
    v += P("Wenn die Wut kommt, hilft ein einfacher Plan in drei Schritten:")
    v += kacheln([
        ("#f6d9d6", "1 Stopp", "", "Halte kurz an. Sag dir innerlich „Stopp!“ und tu erst einmal nichts."),
        ("#fbe9c2", "2 Atmen", "", "Atme dreimal tief und langsam ein und aus. Zähle dabei bis vier."),
        ("#d9efd8", "3 Weitermachen", "", "Jetzt entscheidest du in Ruhe: Hand geben, durchatmen, nächstes Spiel."),
    ], cols=3)
    v += P("Hilfreich ist auch, nach dem Grund für die Niederlage zu fragen: Was können wir beim nächsten Mal besser machen? "
           "Aus Niederlagen lernt man oft mehr als aus Siegen.")
    v += abschnitt("D", "Noch mehr Tipps gegen Wut")
    v += P("Jeder Mensch beruhigt sich anders. Manchen hilft es, die Fäuste fest zu ballen und dann ganz locker zu lassen. "
           "Andere zählen langsam bis zehn oder denken an etwas Schönes. Es hilft auch, später mit jemandem darüber zu reden, "
           "zum Beispiel mit einem Freund oder der Lehrkraft.")
    v += abschnitt("E", "Profis machen es vor")
    v += P("Nach einem Finale sieht man oft, wie Sieger zu den Verlierern gehen und sie trösten. Und Verlierer gratulieren den Siegern, "
           "obwohl sie traurig sind. Das zeigt echte Größe.")
    a = [
        aufgabe(1, 0, "Welche Gefühle kann man beim Sport haben? Schreibe vier auf.",
                felder(L, [("1", "Freude"), ("2", "Wut"), ("3", "Enttäuschung"), ("4", "Stolz")], 4, 34)),
        aufgabe(2, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Wut nach einer Niederlage ist normal.", True),
            ("Wenn ich wütend bin, darf ich den Ball wegschießen.", False),
            ("Nach einem Sieg lache ich die anderen aus.", False),
            ("Aus Niederlagen kann man viel lernen.", True)])),
        aufgabe(3, 0, "Schreibe die drei Schritte des Stopp-Plans auf.",
                felder(L, [("Schritt 1", "Stopp"), ("Schritt 2", "Atmen"), ("Schritt 3", "Weitermachen")], 3, 44)),
        aufgabe(4, 1, "Gut gewinnen oder schlecht gewinnen? Ordne zu. Schreibe g (gut) oder s (schlecht).",
                zuordnen(L, ["g = gut gewinnen", "s = schlecht gewinnen"], [
                    ("„Ihr seid echt Loser!“", "s"), ("„Gut gespielt, das war knapp.“", "g"),
                    ("Mit dem eigenen Team jubeln.", "g"), ("Dem Gegner den Pokal vor die Nase halten.", "s")])),
        aufgabe(5, 1, "Du verlierst beim Badminton. Was kannst du dich danach fragen, um beim nächsten Mal besser zu sein?",
                linien(L, 2, "Was hat der andere besser gemacht? Was übe ich jetzt? Zum Beispiel den hohen Aufschlag.")),
        aufgabe(6, 2, "Ein Mitschüler wirft nach einer Niederlage jedes Mal wütend den Ball durch die Halle. "
                      "Schreibe ihm einen kurzen Tipp, was er stattdessen tun kann.",
                linien(L, 3, "Wenn du wütend bist, mach den Stopp-Plan: kurz anhalten, dreimal tief atmen, dann in Ruhe weitermachen. "
                             "Den Ball wegzuwerfen ist gefährlich und hilft dir nicht.")),
        aufgabe(7, 0, "Male ein Gesicht für „Ich habe gewonnen“ und eines für „Ich habe verloren, bleibe aber fair“.",
                karo(L, 22)),
    ]
    return blatt(FP, 2, "Gewinnen und verlieren", v,
                 ["Gefühle wie Wut und Enttäuschung sind normal.",
                  "Wut darfst du spüren, aber nicht an anderen auslassen.",
                  "Stopp, atmen, weitermachen."], a)


def fp3(L):
    v = abschnitt("A", "Ein Team ist mehr als einzelne Spieler")
    v += P("Im Sportunterricht spielst du oft in einer Mannschaft. Eine gute Mannschaft hat nicht nur gute Spieler. "
           "Sie hält zusammen, spielt sich den Ball zu und hilft sich gegenseitig. Das nennt man <b>Teamgeist</b>.")
    v += abschnitt("B", "Worte können stärken oder verletzen")
    v += P("Was du zu deinen Mitspielern sagst, macht einen großen Unterschied. "
           "Ein Mitspieler, der ausgelacht wird, traut sich beim nächsten Mal weniger. "
           "Ein Mitspieler, der ermutigt wird, probiert es wieder und wird besser.")
    v += ('<table class="info"><tr><th>Das verletzt</th><th>Das stärkt</th></tr>'
          '<tr><td>„Du kannst ja gar nichts!“</td><td>„Nicht schlimm, nächstes Mal klappt’s!“</td></tr>'
          '<tr><td>„Wegen dir haben wir verloren.“</td><td>„Wir haben als Team verloren.“</td></tr>'
          '<tr><td>„Gib nie wieder den Ball an den!“</td><td>„Gut gemacht!“ oder „Super Pass!“</td></tr></table>')
    v += abschnitt("C", "Mannschaften wählen")
    v += P("Wenn Mannschaften gewählt werden, bleibt oft jemand bis zum Schluss übrig. Das fühlt sich schlimm an. "
           "Deshalb teilt die Lehrkraft die Teams oft selbst ein oder lässt abzählen. "
           "Egal, wie die Teams entstehen: Jeder Mitspieler gehört dazu und bekommt den Ball.")
    v += abschnitt("D", "Gemeinsam Ordnung halten")
    v += P("Zum Miteinander gehört auch, dass alle beim Aufbauen und Abbauen helfen. "
           "Geräte trägt man zusammen, Bälle kommen zurück in den Wagen. Dann geht es schneller und niemand macht alles allein.")
    v += abschnitt("E", "Gemeinsam gewinnen")
    v += P("Jeder in einer Mannschaft kann etwas anderes gut: Der eine ist schnell, die andere wirft genau, ein dritter hat den Überblick. "
           "Ein Team ist dann stark, wenn es die Stärken von allen nutzt und sich den Ball zuspielt.")
    a = [
        aufgabe(1, 0, "Setze die Wörter ein.", lueckentext(L,
                "Wenn eine Mannschaft zusammenhält, nennt man das {}. Wer {} wird, traut sich weniger. "
                "Wer {} wird, probiert es wieder. Beim Abbauen {} alle.",
                ["Teamgeist", "ausgelacht", "ermutigt", "helfen"], ["helfen", "ermutigt", "Teamgeist", "ausgelacht"], 30)),
        aufgabe(2, 0, "Verletzt oder stärkt der Satz? Schreibe v oder s.",
                zuordnen(L, ["v = verletzt", "s = stärkt"], [
                    ("„Schöner Wurf!“", "s"), ("„Du Opfer!“", "v"), ("„Komm, wir schaffen das noch!“", "s"),
                    ("„Mit dem spiele ich nicht.“", "v"), ("„Danke für den Pass!“", "s")])),
        aufgabe(3, 1, "Schreibe die Sätze so um, dass sie stärken statt verletzen.",
                '<p style="margin-bottom:.5mm">a) „Du bist viel zu langsam.“</p>' + linien(L, 1, "„Lauf los, du schaffst das!“")
                + '<p style="margin:1.5mm 0 .5mm 0">b) „Wegen dir haben wir verloren.“</p>' + linien(L, 1, "„Wir haben zusammen verloren, nächstes Mal gewinnen wir.“")),
        aufgabe(4, 1, "Wie fühlt sich jemand, der ausgelacht wird? Und wie jemand, der ermutigt wird? Schreibe je einen Satz.",
                linien(L, 2, "Ausgelacht: traurig, schämt sich, will nicht mehr mitspielen. Ermutigt: fühlt sich wohl, traut sich mehr.")),
        aufgabe(5, 2, "Schreibe drei Regeln für ein gutes Miteinander im Sportunterricht deiner Klasse.",
                linien(L, 3, "1. Wir lachen niemanden aus. 2. Jeder bekommt den Ball. 3. Alle helfen beim Auf- und Abbauen.")),
        aufgabe(6, 2, "Warum ist es für die ganze Mannschaft gut, wenn schwächere Spieler ermutigt werden?",
                linien(L, 2, "Sie trauen sich mehr, spielen mit und werden besser. Dann ist die ganze Mannschaft stärker.")),
        aufgabe(7, 1, "Jeder kann etwas anderes gut. Schreibe auf, welche Stärken es in einer Mannschaft geben kann und wie sie dem Team helfen.",
                linien(L, 3, "Einer ist schnell und läuft nach vorne, eine wirft genau aufs Tor, einer passt gut auf und verteidigt. Zusammen sind sie stark.")),
    ]
    return blatt(FP, 3, "Miteinander im Team", v,
                 ["Teamgeist heißt: zusammenhalten und sich helfen.",
                  "Ermutigen statt auslachen.",
                  "Jeder gehört zum Team und bekommt den Ball."], a)


# ================================================================== Herz, Puls, Ausdauer
HP = "Herz, Puls und Ausdauer"


def hp1(L):
    v = abschnitt("A", "Das Herz ist ein Muskel")
    v += P("Dein Herz ist ungefähr so groß wie deine Faust. Es sitzt in der Brust, etwas links von der Mitte. "
           "Das Herz ist ein Muskel, der nie Pause macht. Es pumpt Blut durch deinen ganzen Körper, Tag und Nacht. "
           "An einem Tag schlägt es etwa 100 000 Mal.")
    v += abschnitt("B", "Wozu das Blut gebraucht wird")
    v += P("Das Blut bringt Sauerstoff aus der Lunge zu allen Muskeln. Ohne Sauerstoff können die Muskeln nicht arbeiten. "
           "Wenn du rennst, brauchen deine Muskeln viel mehr Sauerstoff als im Sitzen. "
           "Deshalb schlägt dein Herz beim Sport schneller und du atmest schneller.")
    v += abschnitt("C", "Den Puls messen")
    v += P("Jeden Herzschlag kannst du als kleinen Stoß spüren. Das ist der <b>Puls</b>. "
           "Man fühlt ihn am besten an der Innenseite des Handgelenks unter dem Daumen oder seitlich am Hals.")
    v += ('<div class="box" style="margin:1mm 0 2mm 0"><div class="t">So misst du deinen Puls</div>'
          '1. Lege Zeige- und Mittelfinger auf das Handgelenk, nicht den Daumen.<br>'
          '2. Zähle die Schläge 15 Sekunden lang. Schau dabei auf eine Uhr.<br>'
          '3. Nimm die Zahl mal 4. Dann hast du die Schläge in einer Minute.<br>'
          '<i>Beispiel: 21 Schläge in 15 Sekunden, 21 · 4 = 84 Schläge in der Minute.</i></div>')
    v += ('<table class="info"><tr><th>Situation</th><th>Puls, etwa (Schläge in der Minute)</th></tr>'
          '<tr><td>Kind in Ruhe</td><td>70 bis 100</td></tr><tr><td>Erwachsener in Ruhe</td><td>60 bis 80</td></tr>'
          '<tr><td>Kind beim schnellen Rennen</td><td>bis etwa 200</td></tr></table>')
    v += P("Wer regelmäßig Ausdauersport macht, hat ein stärkeres Herz. Es pumpt mit jedem Schlag mehr Blut. "
           "Deshalb schlägt es in Ruhe langsamer.")
    v += abschnitt("D", "Gut für dein Herz")
    v += P("Dein Herz mag Bewegung: Toben, Radfahren, Schwimmen und Fangen spielen machen es stark. Lange Sitzen, zu viel Süßes "
           "und später Rauchen schaden dem Herzen. Wer sich als Kind viel bewegt, tut seinem Herzen etwas Gutes für das ganze Leben.")
    a = [
        aufgabe(1, 0, "Setze die Wörter ein.", lueckentext(L,
                "Das Herz ist so groß wie eine {}. Es ist ein {}. Das Blut bringt {} zu den Muskeln. "
                "Den Herzschlag kann man als {} fühlen.",
                ["Faust", "Muskel", "Sauerstoff", "Puls"], ["Puls", "Sauerstoff", "Faust", "Muskel"], 30)),
        aufgabe(2, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Das Herz macht nachts Pause.", False),
            ("Beim Sport schlägt das Herz schneller.", True),
            ("Den Puls misst man am besten mit dem Daumen.", False),
            ("Ein trainiertes Herz schlägt in Ruhe langsamer.", True)])),
        aufgabe(3, 0, "Miss deinen Puls in Ruhe, so wie es auf der Vorderseite steht.",
                felder(L, [("Schläge in 15 Sekunden", "z. B. 20"), ("mal 4 =", "z. B. 80"),
                           ("Liegt dein Puls zwischen 70 und 100?", "ja / nein")], 3, 44)),
        aufgabe(4, 1, "Rechne den Puls für eine Minute aus.",
                felder(L, [("18 Schläge in 15 s", "72"), ("25 Schläge in 15 s", "100"),
                           ("45 Schläge in 15 s", "180"), ("30 Schläge in 15 s", "120")], 4, 30)),
        aufgabe(5, 1, "Warum schlägt dein Herz beim Rennen schneller als im Sitzen?",
                linien(L, 2, "Die Muskeln brauchen beim Rennen mehr Sauerstoff. Das Herz muss mehr Blut zu ihnen pumpen.")),
        aufgabe(6, 2, "Ein Herz schlägt in Ruhe 80 Mal in der Minute. Wie oft schlägt es in einer Stunde? Rechne.",
                linien(L, 2, "80 · 60 = 4800. Es schlägt 4800 Mal in einer Stunde.")),
        aufgabe(7, 0, "Zeichne ein Herz und schreibe dazu, wie groß es ungefähr ist.", karo(L, 20, "Herz gezeichnet, „so groß wie meine Faust“")),
        aufgabe(8, 0, "Was ist gut für dein Herz? Nenne drei Dinge.",
                felder(L, [("1", "Rad fahren"), ("2", "Toben"), ("3", "Schwimmen")], 3, 44)),
        aufgabe(9, 2, "Erkläre einem jüngeren Kind, warum das Herz nie Pause machen darf.",
                linien(L, 2, "Das Herz pumpt Blut mit Sauerstoff zu allen Muskeln, auch im Schlaf. Ohne Sauerstoff kann der Körper nicht leben.")),
    ]
    return blatt(HP, 1, "Dein Herz und dein Puls", v,
                 ["Das Herz ist ein Muskel und pumpt Blut mit Sauerstoff zu den Muskeln.",
                  "Puls messen: 15 Sekunden zählen, mal 4.",
                  "Ausdauersport macht das Herz stärker."], a)


def hp2(L):
    v = abschnitt("A", "Was ist Ausdauer?")
    v += P("Ausdauer heißt: Du kannst dich lange bewegen, ohne schnell müde zu werden. "
           "Du brauchst sie beim Laufen, Radfahren, Schwimmen und auch bei Spielen wie Fußball oder Handball, "
           "wo man viel hin und her rennt.")
    v += P("Neben der Ausdauer gibt es noch andere Fähigkeiten. Beim Sprint brauchst du <b>Schnelligkeit</b>, "
           "beim Klettern am Seil <b>Kraft</b> und beim Balancieren <b>Gleichgewicht</b>.")
    v += abschnitt("B", "Der Coopertest")
    v += P("Im Sportunterricht wird die Ausdauer mit dem Coopertest gemessen. Dabei läufst du <b>12 Minuten</b> lang "
           "so weit du kannst. Gezählt werden die Runden. Auf einer Laufbahn ist eine Runde 400 m lang. "
           "Wer 6 Runden schafft, ist 6 · 400 m = 2400 m gelaufen.")
    v += abschnitt("C", "Tipps für lange Läufe")
    v += kacheln([
        ("#d9efd8", "Nicht zu schnell starten", "", "Wer am Anfang rennt, ist nach zwei Runden kaputt. Lieber gleichmäßig laufen."),
        ("#dbe8f5", "Ruhig atmen", "", "Atme gleichmäßig. Du solltest beim Laufen noch kurz sprechen können."),
        ("#fbe9c2", "Locker bleiben", "", "Schultern unten lassen, Arme locker mitschwingen."),
        ("#f6d9d6", "Durchhalten", "", "Wenn es schwer wird: langsamer werden, aber nicht stehen bleiben."),
    ])
    v += abschnitt("D", "Ausdauer kann man trainieren")
    v += P("Wer zwei- bis dreimal in der Woche etwa 20 Minuten locker läuft, Rad fährt oder schwimmt, "
           "wird nach ein paar Wochen deutlich ausdauernder. Wichtig ist, regelmäßig dranzubleiben.")
    v += abschnitt("E", "Ausdauer im Alltag")
    v += P("Auch im Alltag trainierst du deine Ausdauer: wenn du mit dem Rad zur Schule fährst, Treppen läufst oder draußen spielst. "
           "Je öfter du dich bewegst, desto leichter fällt dir der nächste Coopertest.")
    a = [
        aufgabe(1, 0, "Was braucht man dafür am meisten? Schreibe Ausdauer, Schnelligkeit, Kraft oder Gleichgewicht.",
                felder(L, [("Marathon laufen", "Ausdauer"), ("50-m-Sprint", "Schnelligkeit"), ("Am Seil klettern", "Kraft"),
                           ("Auf dem Balken gehen", "Gleichgewicht"), ("Lange schwimmen", "Ausdauer"),
                           ("Liegestütze", "Kraft")], 3, 44)),
        aufgabe(2, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Beim Coopertest läuft man 12 Minuten.", True),
            ("Man sollte am Anfang so schnell wie möglich rennen.", False),
            ("Beim Laufen sollte man noch kurz sprechen können.", True),
            ("Ausdauer kann man nicht trainieren.", False)])),
        aufgabe(3, 1, "Wie weit ist man gelaufen? Eine Runde ist 400 m lang.",
                felder(L, [("5 Runden", "2000 m"), ("7 Runden", "2800 m"), ("4 Runden", "1600 m"),
                           ("6 Runden und 200 m", "2600 m")], 4, 32)),
        aufgabe(4, 1, "Ein Kind startet beim Coopertest sehr schnell und muss nach drei Minuten gehen. Was hat es falsch gemacht? Gib einen Tipp.",
                linien(L, 2, "Es ist zu schnell gestartet. Tipp: gleichmäßig und ruhig laufen, lieber am Ende schneller werden.")),
        aufgabe(5, 2, "Plane eine Trainingswoche, damit deine Ausdauer besser wird. Schreibe zu drei Tagen, was du machst und wie lange.",
                f'<div class="spalten" style="grid-template-columns:repeat(3,1fr)">'
                + "".join(f'<div class="box" style="min-height:17mm"><div class="t">Tag {i}</div><div class="loe">{b if L else ""}</div></div>'
                          for i, b in ((1, "Montag: 20 min locker laufen"), (2, "Mittwoch: 30 min Rad fahren"), (3, "Samstag: 20 min schwimmen")))
                + "</div>"),
        aufgabe(6, 0, "Zeichne eine 400-m-Laufbahn von oben (zwei gerade Seiten, zwei Kurven). Markiere Start und Ziel.",
                karo(L, 24, "Ovale Bahn gezeichnet, Start und Ziel an derselben Stelle")),
        aufgabe(7, 1, "Welche Sportart, die du machst oder gern machen würdest, braucht viel Ausdauer? Begründe.",
                linien(L, 2, "Fußball, weil man das ganze Spiel lang hin und her läuft.")),
    ]
    return blatt(HP, 2, "Ausdauer", v,
                 ["Ausdauer heißt: lange bewegen, ohne schnell müde zu werden.",
                  "Gleichmäßig laufen, nicht zu schnell starten.",
                  "Regelmäßig trainieren macht ausdauernder."], a)


def hp3(L):
    v = abschnitt("A", "Dein Körper arbeitet mit")
    v += P("Wenn du rennst, arbeiten nicht nur deine Beine. Dein ganzer Körper stellt sich auf die Anstrengung ein. "
           "Das spürst du selbst, wenn du schnell rennst.")
    v += kacheln([
        ("#dbe8f5", "Lunge", "atmet schneller", "Du atmest schneller und tiefer. So kommt mehr Sauerstoff in den Körper."),
        ("#f6d9d6", "Herz", "schlägt schneller", "Das Herz pumpt mehr Blut. Das Blut bringt den Sauerstoff zu den Muskeln."),
        ("#fbe9c2", "Haut", "wird rot und schwitzt", "Die Muskeln werden warm. Damit du nicht überhitzt, wird die Haut stärker durchblutet und du schwitzt."),
        ("#d9efd8", "Muskeln", "arbeiten und ermüden", "Die Muskeln verbrauchen Energie und Sauerstoff. Nach einiger Zeit werden sie müde."),
    ])
    v += abschnitt("B", "Der Weg des Sauerstoffs")
    v += P("Der Sauerstoff kommt aus der Luft. Du atmest ihn durch Mund und Nase ein. In der Lunge geht er ins Blut über. "
           "Das Herz pumpt das Blut weiter zu den Muskeln. Dort wird der Sauerstoff gebraucht, damit die Muskeln Energie bekommen.")
    v += ('<div style="display:flex;gap:2mm;align-items:center;justify-content:center;margin:1mm 0 2mm 0;font-weight:600;font-size:10pt">'
          + " <span>➜</span> ".join(f'<span class="box" style="padding:1mm 2.5mm">{t}</span>'
                                    for t in ("Luft", "Mund und Nase", "Lunge", "Blut", "Herz", "Muskeln")) + '</div>')
    v += abschnitt("C", "Nach der Anstrengung")
    v += P("Wenn du aufhörst, beruhigt sich dein Körper wieder. Atmung und Puls werden langsamer. "
           "Bei trainierten Menschen geht das schneller als bei untrainierten. "
           "Darum ist die Erholungszeit auch ein Zeichen dafür, wie fit jemand ist.")
    v += abschnitt("D", "Seitenstechen")
    v += P("Manchmal sticht es beim Laufen in der Seite. Das passiert oft, wenn man zu schnell losrennt oder kurz vorher viel gegessen hat. "
           "Dann hilft es, langsamer zu werden, tief auszuatmen und die Hand auf die Stelle zu drücken.")
    a = [
        aufgabe(1, 0, "Was passiert beim Rennen? Ordne zu.",
                zuordnen(L, ["atmet schneller", "schlägt schneller", "wird rot und schwitzt", "werden müde"], [
                    ("Herz", "B"), ("Lunge", "A"), ("Muskeln", "D"), ("Haut", "C")])),
        aufgabe(2, 0, "Bringe den Weg des Sauerstoffs in die richtige Reihenfolge. Nummeriere.",
                reihenfolge(L, ["Luft", "Mund und Nase", "Lunge", "Blut und Herz", "Muskeln"],
                            ["Lunge", "Muskeln", "Luft", "Blut und Herz", "Mund und Nase"])),
        aufgabe(3, 1, "Was stimmt direkt nach einem schnellen Lauf? Kreuze an.", richtig_falsch(L, [
            ("Man atmet schneller.", True), ("Das Gesicht wird rot.", True),
            ("Das Herz schlägt langsamer als vorher.", False), ("Man schwitzt.", True)])),
        aufgabe(4, 1, "Warum schwitzt man beim Sport?",
                linien(L, 2, "Die Muskeln werden warm. Der Schweiß verdunstet und kühlt den Körper, damit er nicht überhitzt.")),
        aufgabe(5, 2, "Zwei Kinder laufen gleich schnell. Bei Kind A ist der Puls nach zwei Minuten wieder ruhig, bei Kind B erst nach fünf. Wer ist fitter? Begründe.",
                linien(L, 2, "Kind A, denn bei trainierten Menschen erholt sich der Körper schneller.")),
        aufgabe(6, 0, "Zeichne eine Figur, die gerade gerannt ist. Zeige mit Pfeilen und Wörtern, was man an ihr sieht.",
                karo(L, 30, "Figur mit Pfeilen: rotes Gesicht, Schweiß, schnelles Atmen")),
    ]
    return blatt(HP, 3, "Was beim Rennen im Körper passiert", v,
                 ["Beim Rennen arbeiten Lunge, Herz, Haut und Muskeln zusammen.",
                  "Der Sauerstoff kommt aus der Luft und wird mit dem Blut zu den Muskeln gebracht.",
                  "Wer fit ist, erholt sich schneller."], a)


# ================================================================== Training und Erholung
TE = "Training und Erholung"


def te1(L):
    v = abschnitt("A", "Schlaf ist deine Ladestation")
    v += P("Ein Handy muss jede Nacht an die Steckdose. Dein Körper auch, nur heißt seine Steckdose Schlaf. "
           "Im Schlaf erholt sich dein Körper von allem, was du am Tag gemacht hast.")
    v += kacheln([
        ("#dbe8f5", "Wachsen", "", "Im Tiefschlaf bildet der Körper Wachstumshormone. Kinder wachsen vor allem nachts."),
        ("#d9efd8", "Reparieren", "", "Die Muskeln erholen sich vom Sport und werden kräftiger."),
        ("#fbe9c2", "Lernen", "", "Das Gehirn sortiert, was du am Tag gelernt hast, und speichert es."),
        ("#f6d9d6", "Gesund bleiben", "", "Wer genug schläft, wird seltener krank."),
    ])
    v += abschnitt("B", "Wie viel Schlaf brauchst du?")
    v += P("Kinder zwischen 6 und 12 Jahren brauchen jede Nacht <b>9 bis 12 Stunden</b> Schlaf. "
           "Jugendliche brauchen 8 bis 10 Stunden. Viele schlafen weniger. "
           "Dann sind sie am nächsten Tag müde, gereizt und können sich schlecht konzentrieren. Auch beim Sport fehlt ihnen die Kraft.")
    v += abschnitt("C", "Tipps für guten Schlaf")
    v += P("<b>Feste Zeiten:</b> Geh jeden Abend ungefähr zur gleichen Zeit ins Bett, auch am Wochenende.<br>"
           "<b>Bildschirm aus:</b> Handy, Tablet und Fernseher eine Stunde vor dem Schlafen weglegen. "
           "Das helle Licht macht wach.<br>"
           "<b>Ruhiges Zimmer:</b> dunkel, leise und nicht zu warm.<br>"
           "<b>Bewegung am Tag:</b> Wer tagsüber draußen war und sich bewegt hat, schläft besser.<br>"
           "<b>Spät abends kein großes Essen</b> und keine Cola oder Energydrinks.")
    v += abschnitt("D", "Träumen")
    v += P("Jede Nacht träumst du mehrmals, auch wenn du dich morgens nicht immer daran erinnerst. Im Traum verarbeitet dein Gehirn, "
           "was du am Tag erlebt hast. Auch das gehört zur Erholung.")
    a = [
        aufgabe(1, 0, "Was macht der Körper im Schlaf? Nenne drei Dinge.",
                felder(L, [("1", "wachsen"), ("2", "Muskeln reparieren"), ("3", "Gelerntes speichern")], 3, 48)),
        aufgabe(2, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Kinder brauchen 9 bis 12 Stunden Schlaf.", True),
            ("Das Licht vom Handy macht müde.", False),
            ("Kinder wachsen vor allem nachts.", True),
            ("Wer zu wenig schläft, hat beim Sport mehr Kraft.", False)])),
        aufgabe(3, 1, "Wie lange schläft das Kind? Rechne.",
                felder(L, [("ins Bett 21 Uhr, auf 6:30 Uhr", "9 h 30 min"), ("ins Bett 22:30 Uhr, auf 6:30 Uhr", "8 h"),
                           ("ins Bett 20:45 Uhr, auf 7 Uhr", "10 h 15 min")], 3, 44)),
        aufgabe(4, 1, "Wann bist du gestern ins Bett gegangen und wann aufgestanden? Wie lange hast du geschlafen? War das genug?",
                linien(L, 2, "Beispiel: 21:30 Uhr bis 6:45 Uhr, das sind 9 h 15 min. Das ist genug.")),
        aufgabe(5, 2, "Ein Freund schaut jeden Abend bis 23 Uhr Videos und ist morgens immer müde. Gib ihm zwei Tipps und begründe sie.",
                linien(L, 3, "Handy eine Stunde vor dem Schlafen weglegen, weil das helle Licht wach macht. "
                             "Früher ins Bett gehen, jeden Tag zur gleichen Zeit, damit er 9 bis 12 Stunden schläft.")),
        aufgabe(6, 0, "Male oder beschreibe dein Schlafzimmer so, dass man darin gut schlafen kann.",
                karo(L, 24, "dunkel, leise, kühl, kein Bildschirm am Bett")),
        aufgabe(7, 1, "Was machst du am Abend, bevor du schlafen gehst? Was davon hilft beim Einschlafen, was eher nicht?",
                linien(L, 3, "Beispiel: Zähne putzen und lesen helfen. Am Tablet spielen macht wach, das lasse ich lieber.")),
    ]
    return blatt(TE, 1, "Schlaf, deine Ladestation", v,
                 ["Im Schlaf wächst du, erholst dich und speicherst Gelerntes.",
                  "Kinder brauchen 9 bis 12 Stunden Schlaf.",
                  "Bildschirm eine Stunde vor dem Schlafen weglegen."], a)


def te2(L):
    v = abschnitt("A", "Wie der Körper stärker wird")
    v += P("Wenn du trainierst, strengst du deinen Körper an. Danach bist du erst einmal müde. "
           "In der Pause danach erholt sich dein Körper. Und er macht noch mehr: Er stellt sich auf die Anstrengung ein "
           "und wird ein kleines bisschen stärker als vorher. So kann er die nächste Anstrengung besser schaffen.")
    v += f'<div style="width:125mm;margin:1mm auto 1mm auto">{kurve()}</div>'
    v += abschnitt("B", "Drei Regeln fürs Üben")
    v += kacheln([
        ("#dbe8f5", "1 Regelmäßig", "", "Lieber dreimal in der Woche kurz als einmal im Monat ganz lang. Sonst ist der Gewinn wieder weg."),
        ("#d9efd8", "2 Langsam steigern", "", "Wenn etwas leicht geworden ist, mach etwas mehr: eine Minute länger, ein paar Wiederholungen mehr."),
        ("#fbe9c2", "3 Pausen machen", "", "Stärker wirst du in der Pause, nicht während der Anstrengung. Ohne Pause wirst du nur müde."),
    ], cols=3)
    v += abschnitt("C", "Ein Beispiel")
    v += P("Ein Mädchen schafft beim Seilspringen 20 Sprünge am Stück. Sie übt jeden zweiten Tag. "
           "Nach einer Woche schafft sie 30, nach drei Wochen 60 Sprünge. Sie hat regelmäßig geübt, "
           "langsam gesteigert und zwischendurch Pausen gemacht.")
    v += abschnitt("D", "Üben im Kopf")
    v += P("Profisportler üben nicht nur mit dem Körper, sondern auch im Kopf. Sie stellen sich eine Bewegung ganz genau vor, Schritt für Schritt. "
           "Das hilft wirklich beim Lernen. Das kannst du auch, wenn du gerade nicht mitmachen kannst.")
    a = [
        aufgabe(1, 0, "Bringe die Schritte in die richtige Reihenfolge. Nummeriere.",
                reihenfolge(L, ["Ich strenge mich an.", "Ich bin müde.", "Ich mache Pause und erhole mich.", "Ich bin stärker als vorher."],
                            ["Ich bin stärker als vorher.", "Ich strenge mich an.", "Ich mache Pause und erhole mich.", "Ich bin müde."])),
        aufgabe(2, 0, "Schreibe die drei Regeln fürs Üben auf.",
                felder(L, [("Regel 1", "regelmäßig"), ("Regel 2", "langsam steigern"), ("Regel 3", "Pausen machen")], 3, 44)),
        aufgabe(3, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Stärker wird man in der Pause.", True),
            ("Einmal im Monat lange üben reicht.", False),
            ("Wenn eine Übung leicht wird, macht man etwas mehr.", True)])),
        aufgabe(4, 1, "Zeichne die Kurve von der Vorderseite ab und beschrifte die drei Teile.",
                karo(L, 28, "Kurve: 1 Belastung (geht nach unten), 2 Erholung (geht hoch), 3 stärker als vorher (über der Linie)")),
        aufgabe(5, 1, "Plane, wie du beim Seilspringen besser wirst. Du schaffst heute 15 Sprünge.",
                linien(L, 2, "Beispiel: Montag, Mittwoch und Freitag üben. Jede Woche 5 Sprünge mehr, nach drei Wochen 30.")),
        aufgabe(6, 2, "Ein Junge will schnell fitter werden und trainiert jeden Tag bis zur Erschöpfung, ohne Pause. Was passiert? Begründe.",
                linien(L, 2, "Er wird immer müder statt stärker, weil sein Körper keine Zeit zur Erholung hat. Er kann sich auch verletzen.")),
        aufgabe(7, 2, "Stell dir eine Bewegung aus dem Sportunterricht genau vor, zum Beispiel das Rad. Schreibe auf, was du in Gedanken der Reihe nach machst.",
                linien(L, 3, "Anlaufen, Arme hoch, eine Hand auf die Matte, dann die zweite, Beine gestreckt drüber, auf einem Fuß landen, dann auf dem anderen.")),
    ]
    return blatt(TE, 2, "Üben macht stärker", v,
                 ["Anstrengung, dann Erholung, dann bist du stärker als vorher.",
                  "Regelmäßig üben, langsam steigern, Pausen machen.",
                  "Stärker wirst du in der Pause."], a)


def te3(L):
    v = abschnitt("A", "Bewegung jeden Tag")
    v += P("Kinder und Jugendliche sollten sich jeden Tag <b>mindestens 60 Minuten</b> bewegen, sodass sie dabei "
           "etwas außer Atem kommen. Dazu zählt nicht nur Sport im Verein. Auch Radfahren zur Schule, Toben auf dem Spielplatz, "
           "Schwimmen oder Fußball mit Freunden gehören dazu.")
    v += P("Viele Kinder sitzen heute sehr lange: in der Schule, bei den Hausaufgaben, vor dem Fernseher oder am Handy. "
           "Langes Sitzen macht müde und schwächt die Muskeln, besonders am Rücken.")
    v += abschnitt("B", "Erholung ist nicht nur Faulenzen")
    v += P("Nach dem Sport braucht der Körper Erholung. Es gibt zwei Arten:")
    v += kacheln([
        ("#dbe8f5", "Ruhige Erholung", "", "Schlafen, entspannen, ein Buch lesen. Der Körper kommt zur Ruhe."),
        ("#d9efd8", "Aktive Erholung", "", "Locker spazieren gehen, gemütlich Rad fahren, leicht schwimmen. Das lockert die Muskeln."),
    ])
    v += abschnitt("C", "Muskelkater")
    v += P("Wenn du eine Bewegung machst, die du nicht gewohnt bist, tun dir am nächsten oder übernächsten Tag manchmal die Muskeln weh. "
           "Das ist Muskelkater. Er ist harmlos und geht nach ein paar Tagen von selbst weg. "
           "Lockere Bewegung hilft, starkes Training solltest du in dieser Zeit lassen.")
    v += abschnitt("D", "Wenn du krank bist")
    v += P("Mit Fieber oder einer starken Erkältung darfst du keinen Sport machen. Der Körper braucht seine Kraft, um gesund zu werden. "
           "Sport kann dann sogar dem Herzen schaden. Erst wenn du wieder ganz gesund bist, fängst du langsam wieder an.")
    v += abschnitt("E", "Ab nach draußen")
    v += P("Draußen zu spielen ist besonders gut: Das Tageslicht hebt die Laune, ist gut für die Augen und hilft, abends besser zu schlafen.")
    a = [
        aufgabe(1, 0, "Setze die Wörter ein.", lueckentext(L,
                "Kinder sollten sich jeden Tag mindestens {} Minuten bewegen. Langes {} schwächt die Rückenmuskeln. "
                "Wenn die Muskeln nach ungewohnter Bewegung wehtun, heißt das {}. Mit {} macht man keinen Sport.",
                ["60", "Sitzen", "Muskelkater", "Fieber"], ["Fieber", "60", "Muskelkater", "Sitzen"], 30)),
        aufgabe(2, 0, "Ruhige oder aktive Erholung? Schreibe die Nummern in das richtige Feld.",
                '<div class="wortkasten">① schlafen &nbsp; ② locker spazieren &nbsp; ③ ein Buch lesen &nbsp; ④ gemütlich Rad fahren &nbsp; ⑤ leicht schwimmen &nbsp; ⑥ Musik hören</div>'
                f'<div class="spalten" style="grid-template-columns:1fr 1fr"><div class="box" style="min-height:12mm"><div class="t">ruhig</div><div class="loe">{"① ③ ⑥" if L else ""}</div></div>'
                f'<div class="box" style="min-height:12mm"><div class="t">aktiv</div><div class="loe">{"② ④ ⑤" if L else ""}</div></div></div>'),
        aufgabe(3, 1, "Wie viele Minuten hast du dich in der letzten Woche bewegt? Schätze für jeden Tag.",
                '<table class="info"><tr>' + "".join(f"<th>{t}</th>" for t in ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"))
                + "</tr><tr>" + "".join(f'<td style="height:9mm" class="loe">{"z. B. 45" if (L and i == 0) else ""}</td>' for i in range(7))
                + '</tr></table><p style="font-size:10pt">An wie vielen Tagen waren es mindestens 60 Minuten? ' + gap(L, "z. B. 4", 18) + "</p>"),
        aufgabe(4, 1, "Du hast nach dem Turnen Muskelkater in den Armen. Was machst du in den nächsten Tagen?",
                linien(L, 2, "Lockere Bewegung, zum Beispiel spazieren oder leicht schwimmen. Kein hartes Training, bis er weg ist.")),
        aufgabe(5, 2, "Warum darf man mit Fieber keinen Sport machen? Erkläre.",
                linien(L, 2, "Der Körper braucht seine Kraft, um gesund zu werden. Sport kann dann dem Herzen schaden.")),
        aufgabe(6, 2, "Schreibe drei Ideen auf, wie du an einem Schultag auf 60 Minuten Bewegung kommst.",
                linien(L, 3, "Mit dem Rad zur Schule (20 min), in der Pause Fußball (15 min), nachmittags mit Freunden draußen spielen (30 min).")),
        aufgabe(7, 1, "Welche Bewegung macht dir am meisten Spaß? Schreibe auf, warum.",
                linien(L, 2, "Beispiel: Fußball mit Freunden, weil wir zusammen spielen und lachen.")),
    ]
    return blatt(TE, 3, "Bewegung und Erholung", v,
                 ["Jeden Tag mindestens 60 Minuten bewegen.",
                  "Erholung kann ruhig oder aktiv sein.",
                  "Mit Fieber keinen Sport."], a)


# ================================================================== Verletzungen
VZ = "Verletzungen vermeiden"


def vz1(L):
    v = abschnitt("A", "Warum aufwärmen?")
    v += P("Vor jeder Sportstunde wärmst du dich auf. Das ist keine verschwendete Zeit. "
           "Kalte Muskeln sind wie kalter Kaugummi: steif und sie reißen leicht. Warme Muskeln sind dehnbar und arbeiten besser.")
    v += kacheln([
        ("#f6d9d6", "Muskeln", "werden warm", "Sie werden geschmeidig und verletzen sich nicht so leicht."),
        ("#dbe8f5", "Herz und Lunge", "kommen in Schwung", "Puls und Atmung steigen langsam an, statt plötzlich."),
        ("#fbe9c2", "Gelenke", "werden beweglich", "Knie, Schultern und Sprunggelenke werden auf die Belastung vorbereitet."),
        ("#d9efd8", "Kopf", "wird wach", "Du bist konzentrierter und reagierst schneller."),
    ])
    v += abschnitt("B", "So geht gutes Aufwärmen")
    v += P("Ein gutes Aufwärmen dauert etwa 10 Minuten und wird langsam stärker. Es hat drei Teile:")
    v += P("<b>1 Locker loslaufen:</b> einige Minuten traben, auch rückwärts oder seitwärts, Hopserlauf.<br>"
           "<b>2 Beweglich machen:</b> Arme kreisen, Hüfte kreisen, Knie heben, Fersen zum Po.<br>"
           "<b>3 Steigern:</b> kurze schnellere Läufe, Sprünge oder ein kleines Spiel wie Fangen.")
    v += abschnitt("C", "Passend zum Sport")
    v += P("Das Aufwärmen soll zu dem passen, was danach kommt. Vor dem Turnen werden besonders Handgelenke und Schultern bewegt. "
           "Vor einem Ballspiel kommen Pässe und Sprints dazu. Vor dem Sprint läuft man ein paar kurze Steigerungsläufe.")
    v += abschnitt("D", "Nach dem Sport")
    v += P("Auch am Ende ist es gut, nicht sofort stehen zu bleiben. Ein paar Minuten locker traben oder gehen beruhigt Herz und Atmung langsam wieder.")
    a = [
        aufgabe(1, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Kalte Muskeln verletzen sich leichter.", True),
            ("Aufwärmen ist verschwendete Zeit.", False),
            ("Beim Aufwärmen fängt man langsam an.", True),
            ("Ein gutes Aufwärmen dauert etwa eine Minute.", False)])),
        aufgabe(2, 0, "Nenne die drei Teile eines guten Aufwärmens.",
                felder(L, [("Teil 1", "locker loslaufen"), ("Teil 2", "beweglich machen"), ("Teil 3", "steigern")], 3, 44)),
        aufgabe(3, 0, "Was passiert beim Aufwärmen? Ordne zu.",
                zuordnen(L, ["werden warm und geschmeidig", "kommen langsam in Schwung", "werden beweglich", "wird wach"], [
                    ("Muskeln", "A"), ("Kopf", "D"), ("Herz und Lunge", "B"), ("Gelenke", "C")])),
        aufgabe(4, 1, "Was wärmst du vor dem Turnen besonders auf? Was vor einem Ballspiel?",
                linien(L, 2, "Turnen: Handgelenke und Schultern. Ballspiel: Pässe und kurze Sprints.")),
        aufgabe(5, 1, "Erfinde ein Aufwärmprogramm mit vier Übungen. Zeichne jede Übung als Strichmännchen und schreibe den Namen darunter.",
                f'<div class="spalten" style="grid-template-columns:repeat(4,1fr)">'
                + "".join(f'<div class="karo" style="height:28mm;position:relative"><div class="loe" style="position:absolute;bottom:1mm;left:1.5mm;font-size:9pt">{t if L else ""}</div></div>'
                          for t in ("traben", "Arme kreisen", "Knie heben", "Fangen spielen")) + "</div>"),
        aufgabe(6, 2, "Ein Schüler kommt zu spät und will sofort beim Sprint mitmachen. Was sagst du ihm? Begründe.",
                linien(L, 2, "Erst kurz aufwärmen. Mit kalten Muskeln kann beim Sprint leicht ein Muskel reißen.")),
        aufgabe(7, 1, "Warum sollte man nach dem Sport nicht sofort stehen bleiben?",
                linien(L, 2, "Lockeres Traben oder Gehen beruhigt Herz und Atmung langsam wieder.")),
    ]
    return blatt(VZ, 1, "Aufwärmen", v,
                 ["Aufwärmen macht Muskeln warm und schützt vor Verletzungen.",
                  "Locker loslaufen, beweglich machen, steigern.",
                  "Das Aufwärmen passt zum Sport danach."], a)


def vz2(L):
    v = abschnitt("A", "Sicher in der Sporthalle")
    v += P("In der Sporthalle wird gerannt, gesprungen und geworfen. Damit sich niemand verletzt, gibt es Regeln. "
           "Sie sind nicht dazu da, dich zu ärgern, sondern um dich und die anderen zu schützen.")
    v += ('<table class="info"><tr><th>Regel</th><th>Warum?</th></tr>'
          '<tr><td>Schmuck, Uhren und Ohrringe ablegen</td><td>Man kann hängen bleiben oder andere verletzen.</td></tr>'
          '<tr><td>Lange Haare zusammenbinden</td><td>Sie nehmen nicht die Sicht und verfangen sich nicht.</td></tr>'
          '<tr><td>Hallenschuhe fest binden</td><td>Wer über einen Schnürsenkel stolpert, kann stürzen.</td></tr>'
          '<tr><td>Kaugummi raus</td><td>Man kann sich verschlucken.</td></tr>'
          '<tr><td>Geräte nur mit der Lehrkraft benutzen</td><td>Sie müssen richtig aufgebaut und gesichert sein.</td></tr>'
          '<tr><td>Bälle ruhen lassen, wenn die Lehrkraft spricht</td><td>Sonst hört man nichts und es fliegen Bälle umher.</td></tr></table>')
    v += abschnitt("B", "Geräte richtig aufbauen")
    v += P("Geräte werden zu mehreren getragen, nicht geschleift. Unter jedes Gerät, von dem man herunterfallen oder abspringen kann, "
           "kommen Matten. Die Matten liegen dicht aneinander, damit niemand in eine Lücke tritt. "
           "Die Lehrkraft prüft das Gerät, bevor jemand turnt.")
    v += abschnitt("C", "Helfen und Sichern")
    v += P("Beim Turnen helfen sich die Schüler gegenseitig. Wer hilft, steht nah am Gerät und greift fest zu, "
           "meistens am Oberarm oder an der Hüfte. Er lässt erst los, wenn der Turner sicher steht. "
           "Helfen ist eine wichtige Aufgabe: Der Turner verlässt sich auf dich. Deshalb wird dabei nicht gequatscht oder gealbert.")
    v += abschnitt("D", "Die richtige Kleidung")
    v += P("Sportkleidung soll bequem und luftig sein. In der Halle trägt man Hallenschuhe mit hellen Sohlen, die nicht rutschen und keine Streifen machen. "
           "Straßenschuhe haben in der Halle nichts zu suchen.")
    a = [
        aufgabe(1, 0, "Warum gibt es die Regel? Verbinde mit dem passenden Grund.",
                zuordnen(L, ["Man kann hängen bleiben.", "Man kann stolpern.", "Man kann sich verschlucken.", "Das Gerät muss gesichert sein."], [
                    ("Schuhe fest binden", "B"), ("Schmuck ablegen", "A"), ("Geräte nur mit Lehrkraft", "D"), ("Kaugummi raus", "C")])),
        aufgabe(2, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Geräte werden über den Boden geschleift.", False),
            ("Matten liegen dicht aneinander.", True),
            ("Beim Helfen darf man albern.", False),
            ("Der Helfer lässt los, wenn der Turner sicher steht.", True)])),
        aufgabe(3, 1, "Welche Fehler siehst du? Schreibe zu jedem Satz die richtige Regel.",
                '<p style="margin-bottom:.5mm">a) Ein Mädchen turnt mit langen, offenen Haaren am Reck.</p>' + linien(L, 1, "Lange Haare zusammenbinden.")
                + '<p style="margin:1.5mm 0 .5mm 0">b) Zwischen zwei Matten ist eine große Lücke.</p>' + linien(L, 1, "Matten dicht aneinanderlegen.")
                + '<p style="margin:1.5mm 0 .5mm 0">c) Ein Junge schießt den Ball, während die Lehrkraft erklärt.</p>' + linien(L, 1, "Bälle ruhen lassen, wenn die Lehrkraft spricht.")),
        aufgabe(4, 1, "Zeichne ein Turngerät deiner Wahl mit Matten darunter, so wie es richtig aufgebaut ist.",
                karo(L, 30, "z. B. Reck mit Matten darunter und davor, ohne Lücken")),
        aufgabe(5, 2, "Warum ist Helfen und Sichern eine wichtige Aufgabe? Erkläre.",
                linien(L, 2, "Der Turner verlässt sich auf den Helfer. Wenn der nicht aufpasst, kann der Turner stürzen und sich verletzen.")),
        aufgabe(6, 0, "Was ziehst du für den Sportunterricht in der Halle an? Schreibe es auf.",
                linien(L, 2, "Sporthose, Sport-T-Shirt, Socken und Hallenschuhe mit hellen Sohlen.")),
    ]
    return blatt(VZ, 2, "Sicher in der Halle", v,
                 ["Regeln in der Halle schützen dich und die anderen.",
                  "Geräte tragen, Matten ohne Lücken, Lehrkraft prüft.",
                  "Wer hilft, passt auf und hält fest."], a)


def vz3(L):
    v = abschnitt("A", "Wenn doch etwas passiert")
    v += P("Trotz aller Vorsicht kann man sich beim Sport verletzen. Am häufigsten sind Prellungen, umgeknickte Füße "
           "und verstauchte Finger. Das Wichtigste zuerst: Sag sofort der Lehrkraft Bescheid. Spiel nicht mit Schmerzen weiter.")
    v += abschnitt("B", "Die PECH-Regel")
    v += P("Bei Prellungen, Verstauchungen und umgeknickten Füßen hilft die PECH-Regel. Jeder Buchstabe steht für einen Schritt:")
    v += kacheln([
        ("#f6d9d6", "P wie Pause", "", "Sofort aufhören und nicht weitermachen. Die verletzte Stelle schonen."),
        ("#dbe8f5", "E wie Eis", "", "Kühlen, zum Beispiel mit einem Kühlpack. Nie direkt auf die Haut, immer ein Tuch dazwischen."),
        ("#fbe9c2", "C wie Compression", "", "Das heißt Druck. Ein fester Verband verhindert, dass die Stelle stark anschwillt."),
        ("#d9efd8", "H wie Hochlagern", "", "Die verletzte Stelle hochlegen, zum Beispiel den Fuß auf einen Kasten."),
    ])
    v += P("Wenn es stark wehtut, die Stelle schief aussieht oder man den Fuß gar nicht belasten kann, muss ein Arzt nachschauen.")
    v += abschnitt("C", "Nasenbluten und kleine Wunden")
    v += P("<b>Nasenbluten:</b> Hinsetzen, Kopf leicht <b>nach vorne</b> beugen, nicht nach hinten. "
           "Die Nasenflügel zusammendrücken und den Nacken kühlen.<br>"
           "<b>Schürfwunde:</b> Mit sauberem Wasser ausspülen und ein Pflaster oder einen Verband darauf.")
    v += abschnitt("D", "Erkältet zum Sport?")
    v += P("Bei Schnupfen ohne Fieber kannst du oft leicht mitmachen. Bei Fieber, Husten mit Schmerzen in der Brust "
           "oder wenn du dich schlapp fühlst, machst du keinen Sport. Sag es der Lehrkraft.")
    a = [
        aufgabe(1, 0, "Wofür stehen die Buchstaben der PECH-Regel?",
                felder(L, [("P", "Pause"), ("E", "Eis"), ("C", "Compression"), ("H", "Hochlagern")], 4, 34)),
        aufgabe(2, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Eis legt man direkt auf die Haut.", False),
            ("Bei Nasenbluten legt man den Kopf nach hinten.", False),
            ("Mit Schmerzen spielt man nicht weiter.", True),
            ("Bei Fieber macht man keinen Sport.", True)])),
        aufgabe(3, 1, "Ein Schüler knickt beim Basketball um. Bringe die Schritte in die richtige Reihenfolge.",
                reihenfolge(L, ["Der Lehrkraft Bescheid sagen", "Aufhören und hinsetzen", "Fuß kühlen, Tuch dazwischen",
                                "Verband anlegen", "Fuß hochlegen"],
                            ["Fuß hochlegen", "Der Lehrkraft Bescheid sagen", "Verband anlegen", "Fuß kühlen, Tuch dazwischen", "Aufhören und hinsetzen"])),
        aufgabe(4, 1, "Was machst du bei Nasenbluten? Schreibe es in drei Schritten auf.",
                linien(L, 2, "Hinsetzen, Kopf nach vorne beugen, Nasenflügel zusammendrücken und Nacken kühlen.")),
        aufgabe(5, 2, "Eine Mitschülerin hat einen geschwollenen Knöchel, will aber weiterspielen, weil ihr Team sonst verliert. Was sagst du ihr? Begründe.",
                linien(L, 3, "Sie soll aufhören und die PECH-Regel machen. Wenn sie weiterspielt, kann die Verletzung schlimmer werden "
                             "und sie fällt viel länger aus.")),
        aufgabe(6, 0, "Zeichne ein Bild zur PECH-Regel: einen Fuß, der richtig versorgt wird.",
                karo(L, 24, "Fuß hochgelegt, mit Verband und Kühlpack mit Tuch")),
        aufgabe(7, 1, "Was sagst du einem Mitschüler, der sich verletzt hat, damit er sich beruhigt?",
                linien(L, 2, "„Ich hole die Lehrkraft. Bleib ruhig sitzen, ich bin bei dir.“")),
    ]
    return blatt(VZ, 3, "Wenn etwas passiert", v,
                 ["Bei Schmerzen sofort aufhören und der Lehrkraft Bescheid sagen.",
                  "PECH: Pause, Eis, Compression, Hochlagern.",
                  "Bei Nasenbluten den Kopf nach vorne."], a)


# ================================================================== Regeln und Spielfeld (Handball, Werfen und Fangen)
RS = "Regeln und Spielfeld"


def rs1(L):
    v = abschnitt("A", "Das Handballfeld")
    v += P("Handball wird in der Halle gespielt. Das Spielfeld ist <b>40 m lang</b> und <b>20 m breit</b>. "
           "An jeder Stirnseite steht ein Tor. Es ist 3 m breit und 2 m hoch.")
    v += f'<div style="width:150mm;margin:1mm auto 1mm auto">{handballfeld(True)}</div>'
    v += abschnitt("B", "Die Linien")
    v += P("<b>Torraum (6-m-Linie):</b> Den Torraum darf nur der Torwart betreten. Feldspieler dürfen darüber springen, "
           "müssen aber den Ball loslassen, bevor sie landen.<br>"
           "<b>Freiwurflinie (9 m, gestrichelt):</b> Bei einem Freiwurf nah am Tor wird von hier ausgeführt.<br>"
           "<b>7-m-Linie:</b> Von hier wird der Siebenmeter geworfen. Das ist ein Strafwurf, nur der Werfer gegen den Torwart.<br>"
           "<b>Mittellinie:</b> Hier beginnt das Spiel und nach jedem Tor geht es hier weiter.")
    v += abschnitt("C", "Die Mannschaft")
    v += P("Jede Mannschaft hat 7 Spieler auf dem Feld: 6 Feldspieler und einen Torwart. "
           "Die Spieler dürfen beliebig oft ein- und ausgewechselt werden.")
    a = [
        aufgabe(1, 0, "Beschrifte das Spielfeld. Schreibe die Namen zu den Buchstaben.",
                f'<div style="width:118mm;margin:0 auto 1.5mm auto">{handballfeld(False)}</div>'
                + felder(L, [("A", "Torraum"), ("B", "Freiwurflinie"), ("C", "7-m-Linie"), ("D", "Mittellinie"), ("E", "Tor")], 5, 30)),
        aufgabe(2, 0, "Setze die Zahlen ein.", lueckentext(L,
                "Das Feld ist {} m lang und {} m breit. Das Tor ist {} m breit und {} m hoch. "
                "Eine Mannschaft hat {} Spieler auf dem Feld.",
                ["40", "20", "3", "2", "7"], ["2", "7", "40", "3", "20"], 14)),
        aufgabe(3, 1, "Wer darf in den Torraum? Was müssen Feldspieler beachten?",
                linien(L, 2, "Nur der Torwart. Feldspieler dürfen hineinspringen, müssen den Ball aber vor der Landung loslassen.")),
        aufgabe(4, 1, "Ein Spieler läuft einmal um das ganze Spielfeld. Wie weit läuft er? Rechne.",
                linien(L, 1, "40 m + 20 m + 40 m + 20 m = 120 m")),
        aufgabe(5, 2, "Was ist ein Siebenmeter? Erkläre es einem Kind, das Handball nicht kennt.",
                linien(L, 2, "Ein Strafwurf von der 7-m-Linie. Nur ein Spieler wirft, nur der Torwart darf halten.")),
        aufgabe(6, 0, "Wie viele Spieler sind insgesamt auf dem Feld, wenn beide Mannschaften spielen?",
                felder(L, [("Spieler insgesamt", "14")], 1, 30)),
        aufgabe(7, 1, "Zeichne das Handballtor ins Karofeld: 1 Kästchen sind 50 cm. Das Tor ist 3 m breit und 2 m hoch.",
                karo(L, 28, "Tor 6 Kästchen breit und 4 Kästchen hoch")),
    ]
    return blatt(RS, 1, "Handball: das Spielfeld", v,
                 ["Das Feld ist 40 m lang und 20 m breit.",
                  "Den Torraum darf nur der Torwart betreten.",
                  "Eine Mannschaft hat 6 Feldspieler und einen Torwart."], a)


def rs2(L):
    v = abschnitt("A", "Die wichtigsten Regeln")
    v += P("Beim Handball soll der Ball ins gegnerische Tor geworfen werden. Damit das Spiel fair bleibt, gibt es Regeln. "
           "Die wichtigsten kannst du dir mit der Zahl drei merken.")
    v += kacheln([
        ("#dbe8f5", "3 Schritte", "", "Mit dem Ball in der Hand darfst du höchstens drei Schritte machen. Dann musst du prellen, passen oder werfen."),
        ("#d9efd8", "3 Sekunden", "", "Du darfst den Ball höchstens drei Sekunden festhalten."),
        ("#fbe9c2", "Prellen", "", "Du darfst den Ball prellen, so lange du willst. Wenn du ihn fängst und wieder prellst, ist das ein Doppeldribbling und verboten."),
        ("#f6d9d6", "Körperkontakt", "", "Den Gegner darfst du von vorne mit dem Körper sperren. Halten, Stoßen, Schlagen und Klammern sind verboten."),
    ])
    v += abschnitt("B", "Was der Schiedsrichter entscheidet")
    v += ('<table class="info"><tr><th>Fehler</th><th>Entscheidung</th></tr>'
          '<tr><td>Schrittfehler, Zeitspiel, Doppeldribbling</td><td>Ballverlust: Freiwurf für die andere Mannschaft</td></tr>'
          '<tr><td>Kleines Foul</td><td>Freiwurf für die andere Mannschaft</td></tr>'
          '<tr><td>Foul, das eine klare Torchance verhindert</td><td>Siebenmeter</td></tr>'
          '<tr><td>Grobes oder wiederholtes Foul, Meckern</td><td>Gelbe Karte oder 2 Minuten Zeitstrafe</td></tr>'
          '<tr><td>Sehr grobes Foul</td><td>Rote Karte, der Spieler darf nicht mehr mitspielen</td></tr></table>')
    v += abschnitt("C", "Fair spielen")
    v += P("Handball ist ein Spiel mit viel Körperkontakt. Umso wichtiger ist es, fair zu bleiben. "
           "Wer den Gegner nur am Ball stört und nicht am Körper festhält, spielt sauber. "
           "Entscheidungen des Schiedsrichters werden ohne Meckern angenommen.")
    v += abschnitt("D", "Der Torwart")
    v += P("Der Torwart darf im Torraum den Ball mit allen Körperteilen abwehren, also auch mit den Füßen. "
           "Er darf den Torraum verlassen, aber nicht mit dem Ball in der Hand. Draußen gelten für ihn die gleichen Regeln wie für alle anderen.")
    a = [
        aufgabe(1, 0, "Setze ein.", lueckentext(L,
                "Mit dem Ball darf man höchstens {} Schritte machen. Festhalten darf man ihn höchstens {} Sekunden. "
                "Fangen und wieder prellen heißt {}.",
                ["drei", "drei", "Doppeldribbling"], ["Doppeldribbling", "drei", "drei"], 34)),
        aufgabe(2, 0, "Welche Entscheidung trifft der Schiedsrichter? Ordne zu.",
                zuordnen(L, ["Freiwurf", "Siebenmeter", "2 Minuten Zeitstrafe", "Rote Karte"], [
                    ("Ein Spieler macht fünf Schritte mit dem Ball.", "A"),
                    ("Ein Werfer wird vor dem leeren Tor am Arm festgehalten.", "B"),
                    ("Ein Spieler meckert immer wieder beim Schiedsrichter.", "C"),
                    ("Ein Spieler schlägt einem Gegner ins Gesicht.", "D"),
                    ("Ein Spieler fängt den Ball und prellt dann wieder.", "A")])),
        aufgabe(3, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Man darf den Gegner am Trikot festhalten.", False),
            ("Man darf den Ball beliebig lange prellen.", True),
            ("Sperren von vorne mit dem Körper ist erlaubt.", True)])),
        aufgabe(4, 1, "Welche Regel wurde verletzt? Schreibe sie dazu.",
                '<p style="margin-bottom:.5mm">a) Ein Spieler läuft fünf Schritte mit dem Ball.</p>' + linien(L, 1, "3-Schritte-Regel")
                + '<p style="margin:1.5mm 0 .5mm 0">b) Ein Spieler hält den Ball sechs Sekunden fest.</p>' + linien(L, 1, "3-Sekunden-Regel")
                + '<p style="margin:1.5mm 0 .5mm 0">c) Ein Spieler fängt den Ball und prellt dann wieder.</p>' + linien(L, 1, "Doppeldribbling")),
        aufgabe(5, 2, "Warum gibt es beim Handball die 3-Schritte-Regel? Was wäre ohne sie anders?",
                linien(L, 2, "Ohne die Regel könnte ein Spieler mit dem Ball bis vors Tor rennen. Mit der Regel muss die Mannschaft zusammenspielen.")),
        aufgabe(6, 1, "Was darf der Torwart, was die anderen Spieler nicht dürfen?",
                linien(L, 2, "Er darf in den Torraum und dort den Ball auch mit den Füßen und allen Körperteilen abwehren.")),
    ]
    return blatt(RS, 2, "Handball: die Regeln", v,
                 ["Höchstens 3 Schritte und 3 Sekunden mit dem Ball.",
                  "Fangen und wieder prellen ist verboten.",
                  "Fair bleiben, auch bei viel Körperkontakt."], a)


def rs3(L):
    v = abschnitt("A", "Fangen")
    v += P("Wer gut fangen will, schaut den Ball an, bis er in den Händen ist. Die Arme gehen dem Ball entgegen. "
           "Die Hände bilden eine Schale: Daumen und Zeigefinger formen ein Dreieck, die Finger sind locker gespreizt. "
           "Beim Fangen geben die Arme etwas nach. So prallt der Ball nicht ab.")
    v += abschnitt("B", "Der Schlagwurf")
    v += P("Mit dem Schlagwurf wirft man im Handball am weitesten und am härtesten. So geht er bei einem Rechtshänder:")
    v += P("<b>1</b> Den Ball mit der rechten Hand hinter den Kopf führen, der Ellbogen ist in Schulterhöhe.<br>"
           "<b>2</b> Mit dem <b>linken</b> Bein einen Schritt nach vorne machen.<br>"
           "<b>3</b> Den Oberkörper drehen und den Arm schnell nach vorne bringen.<br>"
           "<b>4</b> Den Ball über dem Kopf loslassen, der Arm schwingt aus.<br>"
           "Linkshänder machen alles spiegelverkehrt.")
    v += abschnitt("C", "Pässe")
    v += kacheln([
        ("#dbe8f5", "Druckpass", "", "Mit beiden Händen von der Brust gerade nach vorne stoßen. Kurz und schnell."),
        ("#d9efd8", "Bodenpass", "", "Der Ball springt einmal auf dem Boden auf. Gut, wenn ein Gegner die Arme oben hat."),
        ("#fbe9c2", "Schlagwurf-Pass", "", "Wie der Schlagwurf, nur weniger hart. Für weite Pässe."),
    ], cols=3)
    v += abschnitt("D", "Häufige Fehler")
    v += P("Den Ball nicht anschauen, steife Arme beim Fangen, beim Werfen das falsche Bein vorne, "
           "den Ellbogen zu tief halten. Wer diese Fehler kennt, kann sie bei sich und anderen erkennen.")
    v += abschnitt("E", "Üben ohne Halle")
    v += P("Werfen und Fangen kannst du überall üben: einen Ball gegen eine Wand werfen und wieder fangen, mit einem Partner zuwerfen, "
           "mit großen und kleinen Bällen. Je öfter du übst, desto sicherer wirst du.")
    a = [
        aufgabe(1, 0, "Richtig oder falsch? Kreuze an.", richtig_falsch(L, [
            ("Beim Fangen schaut man den Ball an.", True),
            ("Beim Fangen bleiben die Arme ganz steif.", False),
            ("Ein Rechtshänder macht beim Schlagwurf einen Schritt mit links.", True),
            ("Beim Bodenpass springt der Ball einmal auf.", True)])),
        aufgabe(2, 0, "Bringe den Schlagwurf in die richtige Reihenfolge.",
                reihenfolge(L, ["Ball hinter den Kopf führen", "Schritt mit dem Gegenbein", "Oberkörper drehen", "Ball über dem Kopf loslassen"],
                            ["Oberkörper drehen", "Ball über dem Kopf loslassen", "Ball hinter den Kopf führen", "Schritt mit dem Gegenbein"])),
        aufgabe(3, 0, "Welcher Pass passt? Schreibe Druckpass, Bodenpass oder Schlagwurf-Pass.",
                felder(L, [("Mitspieler ist 3 m entfernt", "Druckpass"), ("Gegner hat die Arme oben", "Bodenpass"),
                           ("Mitspieler ist 15 m entfernt", "Schlagwurf-Pass")], 3, 44)),
        aufgabe(4, 1, "Zeichne die Hände beim Fangen von hinten (Daumen und Zeigefinger bilden ein Dreieck).",
                karo(L, 22, "Zwei Hände, Daumen und Zeigefinger berühren sich fast und bilden ein Dreieck")),
        aufgabe(5, 1, "Ein Rechtshänder macht beim Schlagwurf einen Schritt mit rechts und hält den Ellbogen tief. Was ist falsch?",
                linien(L, 2, "Er muss mit dem linken Bein nach vorne gehen. Der Ellbogen gehört in Schulterhöhe.")),
        aufgabe(6, 2, "Ein Mitschüler lässt beim Fangen oft den Ball fallen. Gib ihm zwei Tipps aus dem Text.",
                linien(L, 2, "Den Ball bis in die Hände anschauen. Arme entgegenstrecken und beim Fangen nachgeben, Hände als Schale.")),
        aufgabe(7, 1, "Erfinde ein Spiel zum Werfen und Fangen für die Pause. Beschreibe die Regeln.",
                linien(L, 3, "Beispiel: Zwei stehen 3 m auseinander und werfen sich den Ball zu. Wer fängt, geht einen Schritt zurück. Wer ihn fallen lässt, fängt von vorne an.")),
    ]
    return blatt(RS, 3, "Werfen und Fangen", v,
                 ["Ball anschauen, Hände als Schale, Arme geben nach.",
                  "Schlagwurf: Ellbogen hoch, Schritt mit dem Gegenbein.",
                  "Druckpass, Bodenpass und Schlagwurf-Pass je nach Situation."], a)


# ------------------------------------------------------------------ Liste
def _n(thema, nr, titel):
    return f"{thema} {nr} – {titel}"


BLAETTER = [
    (f"{STUFE}/Fair Play", _n("Fair Play", 1, "Was ist Fair Play"), fp1),
    (f"{STUFE}/Fair Play", _n("Fair Play", 2, "Gewinnen und verlieren"), fp2),
    (f"{STUFE}/Fair Play", _n("Fair Play", 3, "Miteinander im Team"), fp3),
    (f"{STUFE}/Herz, Puls und Ausdauer", _n("Herz, Puls und Ausdauer", 1, "Dein Herz und dein Puls"), hp1),
    (f"{STUFE}/Herz, Puls und Ausdauer", _n("Herz, Puls und Ausdauer", 2, "Ausdauer"), hp2),
    (f"{STUFE}/Herz, Puls und Ausdauer", _n("Herz, Puls und Ausdauer", 3, "Was beim Rennen im Körper passiert"), hp3),
    (f"{STUFE}/Training und Erholung", _n("Training und Erholung", 1, "Schlaf, deine Ladestation"), te1),
    (f"{STUFE}/Training und Erholung", _n("Training und Erholung", 2, "Üben macht stärker"), te2),
    (f"{STUFE}/Training und Erholung", _n("Training und Erholung", 3, "Bewegung und Erholung"), te3),
    (f"{STUFE}/Verletzungen vermeiden", _n("Verletzungen vermeiden", 1, "Aufwärmen"), vz1),
    (f"{STUFE}/Verletzungen vermeiden", _n("Verletzungen vermeiden", 2, "Sicher in der Halle"), vz2),
    (f"{STUFE}/Verletzungen vermeiden", _n("Verletzungen vermeiden", 3, "Wenn etwas passiert"), vz3),
    (f"{STUFE}/Regeln und Spielfeld", _n("Regeln und Spielfeld", 1, "Handball, das Spielfeld"), rs1),
    (f"{STUFE}/Regeln und Spielfeld", _n("Regeln und Spielfeld", 2, "Handball, die Regeln"), rs2),
    (f"{STUFE}/Regeln und Spielfeld", _n("Regeln und Spielfeld", 3, "Werfen und Fangen"), rs3),
]
