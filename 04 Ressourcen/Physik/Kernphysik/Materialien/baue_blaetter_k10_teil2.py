#!/usr/bin/env python3
"""Blätter Kernphysik Klasse 10, W06 bis W22 (Leitfragen 3 bis 6). Gleicher Aufbau wie W01 bis W05:
Seite 1 Schülerblatt, Seite 2 Lösung in Magenta, Schwierigkeitskreise mit Legende.
Ideen aus „Erlebnis Physik“ Kl. 10 in eigenen Worten. Aufruf: python3 baue_blaetter_k10_teil2.py"""
from baue_blaetter_k10 import HIER, MAG, nk, kopf, aufg, antwort, luecken, tabelle, dokument, drucke

GRAU = "#66798E"


def feld(inhalt, h):
    return f'<div class="zeichenfeld" style="height:{h}mm;">{inhalt}</div>'


def diagramm(l, punkte, xmax, ymax, xl, yl, xt, yt, kurve=None):
    """Leeres Achsenkreuz im Karofeld, in der Lösung mit Punkten und Kurve."""
    W, H, x0, y0 = 300, 150, 34, 128
    sx, sy = (W - x0 - 14) / xmax, (y0 - 10) / ymax
    o = [f'<svg viewBox="0 0 {W} {H}" style="width:100%;height:100%">',
         f'<line x1="{x0}" y1="{y0}" x2="{W - 6}" y2="{y0}" stroke="#14171c" stroke-width="1"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="6" stroke="#14171c" stroke-width="1"/>',
         f'<text x="{W - 6}" y="{y0 + 16}" font-size="7" text-anchor="end">{xl}</text><text x="{x0 + 4}" y="10" font-size="7">{yl}</text>']
    for v in xt:
        o.append(f'<text x="{x0 + v * sx:.1f}" y="{y0 + 9}" font-size="6.5" text-anchor="middle">{v}</text>')
    for v in yt:
        o.append(f'<text x="{x0 - 3}" y="{y0 - v * sy + 2:.1f}" font-size="6.5" text-anchor="end">{v}</text>')
    if l:
        if kurve:
            pts = " ".join(f"{x0 + x * sx:.1f},{y0 - kurve(x) * sy:.1f}" for x in [xmax * i / 60 for i in range(61)])
            o.append(f'<polyline points="{pts}" fill="none" stroke="{MAG}" stroke-width="1.2"/>')
        for x, y in punkte:
            o.append(f'<circle cx="{x0 + x * sx:.1f}" cy="{y0 - y * sy:.1f}" r="2" fill="{MAG}"/>')
    return "".join(o) + "</svg>"


def reihe(zeilen, l, breite="100%"):
    """zeilen: (Frage-HTML, Lösung) als Tabelle mit Antwortspalte."""
    z = "".join(f'<tr><td style="text-align:left">{f}</td>' + (f'<td class="l">{a}</td>' if l else "<td></td>") + "</tr>" for f, a in zeilen)
    return f'<table class="mess" style="width:{breite}">{z}</table>'


# ================================================================ W06 Würfelmodell
def w06(l):
    werte = [30, 25, 21, 17, 14, 12, 10, 8, 7]
    kopfz = ["Wurf"] + [str(i) for i in range(9)]
    z1 = ["übrig (Gruppe)"] + [str(v) for v in werte]
    tab = ('<table class="mess" style="width:100%"><tr>' + "".join(f"<th>{k}</th>" for k in kopfz) + "</tr><tr>"
           + "".join((f'<td class="v">{w}</td>' if j < 2 else (f'<td class="l">{w}</td>' if l else "<td></td>")) for j, w in enumerate(z1)) + "</tr></table>")
    return (kopf("W06", "F3 — Versuch: Zerfall mit Würfeln", l)
            + '<p class="frage">Kann man vorhersagen, welcher Würfel als Nächstes eine Sechs würfelt?</p>'
            + aufg(1, None, "Versuchsbeschreibung") + '<ol class="liste">'
            '<li>Eure Gruppe wirft 30 Würfel gleichzeitig.</li><li>Alle Würfel mit einer Sechs sind „zerfallen“ und kommen zur Seite.</li>'
            '<li>Zählt die übrigen Würfel und tragt die Zahl ein. Werft dann nur die übrigen Würfel wieder.</li></ol>'
            + aufg(2, 0, "Trage eure Messwerte ein." + (' <span class="loesungstext">Erwartete Werte, eure weichen ab</span>' if l else "")) + tab
            + aufg(3, 1, "Zeichne das Diagramm: übrige Würfel über der Anzahl der Würfe.")
            + feld(diagramm(l, list(enumerate(werte)), 8, 30, "Wurf", "übrige Würfel", range(9), (10, 20, 30), lambda x: 30 * (5 / 6) ** x), 48)
            + aufg(4, 1, "Nach wie vielen Würfen ist etwa die Hälfte der Würfel übrig?")
            + antwort("Nach knapp 4 Würfen (genau etwa 3,8). Von 30 Würfeln sind dann noch etwa 15 übrig.", l, 1)
            + aufg(5, 2, "Was entspricht im Würfelmodell einem Atomkern und was dem Zerfall? Warum hat jede Gruppe andere Werte?")
            + antwort("Ein Würfel ist ein Kern, die Sechs ist der Zerfall. Welcher Würfel eine Sechs hat, ist Zufall. Deshalb weichen die Gruppen voneinander ab. "
                      "Je mehr Würfel, desto genauer passt der Verlauf.", l, 3))


# ================================================================ W07 Halbwertszeit, Bierschaum
def w07(l):
    zeiten = [0, 30, 60, 90, 120, 150, 180, 210, 240]
    hoehe = [f"{10 * 0.5 ** (t / 100):.1f}".replace(".", ",") for t in zeiten]
    tab = ('<table class="mess" style="width:100%"><tr><th>t in s</th>' + "".join(f"<th>{t}</th>" for t in zeiten) + '</tr><tr><th>h in cm</th>'
           + "".join((f'<td class="l">{h}</td>' if l else "<td></td>") for h in hoehe) + "</tr></table>")
    lt = luecken("Die Halbwertszeit ist die Zeit, nach der die [[Hälfte]] der Kerne zerfallen ist. Nach zwei Halbwertszeiten ist noch "
                 "[[ein Viertel]] übrig, nach drei Halbwertszeiten noch [[ein Achtel]]. Jedes Nuklid hat seine [[feste]] Halbwertszeit.", l)
    iod = [["0", "1000", "100 %"], ["8", "500", "50 %"], ["16", "250", "25 %"], ["24", "125", "12,5 %"], ["32", "62,5", "6,25 %"], ["40", "31,25", "3,125 %"]]
    tab2 = ('<table class="mess" style="width:120mm"><tr><th>Zeit in Tagen</th><th>Kerne</th><th>Anteil</th></tr>'
            + "".join("<tr>" + "".join((f'<td class="v">{w}</td>' if (j == 0 or i == 0) else (f'<td class="l">{w}</td>' if l else "<td></td>")) for j, w in enumerate(z)) + "</tr>" for i, z in enumerate(iod)) + "</table>")
    return (kopf("W07", "F3 — Die Halbwertszeit", l)
            + aufg(1, 0, "Versuch: Zerfall von Bierschaum")
            + '<p class="frage">Gieße Malzbier schnell in einen Messzylinder, sodass viel Schaum entsteht. Miss alle 30 Sekunden die Höhe der Schaumkrone.'
            + (' <span class="loesungstext">Beispielwerte</span>' if l else "") + "</p>" + tab
            + aufg(2, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(3, 1, "Iod-131 hat eine Halbwertszeit von 8 Tagen. Ergänze die Tabelle.") + tab2
            + aufg(4, 1, "Lies aus deiner Schaumtabelle ab: Nach welcher Zeit ist die Schaumkrone halb so hoch?")
            + antwort("Nach etwa 100 s (bei den Beispielwerten). Nach weiteren 100 s ist sie wieder halb so hoch.", l, 1)
            + aufg(5, 2, "Begründe, warum die Zerfallskurve die Zeitachse nie erreicht.")
            + antwort("In jeder Halbwertszeit zerfällt nur die Hälfte der noch vorhandenen Kerne. Von einer Menge bleibt nach dem Halbieren immer etwas übrig. "
                      "Erst wenn nur noch sehr wenige Kerne da sind, entscheidet der Zufall, wann der letzte zerfällt.", l, 2))


# ================================================================ W08 Aktivität und Zählrate
def w08(l):
    lt = luecken("Die Aktivität A gibt an, wie viele Kerne pro [[Sekunde]] zerfallen. Ihre Einheit ist das [[Becquerel]] (Bq). "
                 "1 Bq bedeutet: [[ein Zerfall]] pro Sekunde. Das Zählrohr misst weniger, weil die Strahlung in [[alle Richtungen]] fliegt "
                 "und nur ein Teil das Zählrohr trifft. Was es misst, heißt [[Zählrate]].", l)
    alltag = [("Mensch (70 kg)", "etwa 9000 Bq", "540 000"), ("1 Liter Milch", "etwa 50 Bq", "3000"), ("Rauchmelder mit Americium", "etwa 37 000 Bq", "2 220 000")]
    t2 = ('<table class="mess" style="width:100%"><tr><th style="text-align:left">Gegenstand</th><th>Aktivität</th><th>Zerfälle pro Minute</th></tr>'
          + "".join(f'<tr><td style="text-align:left">{a}</td><td class="v">{b}</td>' + (f'<td class="l">{c}</td>' if l else "<td></td>") + "</tr>" for a, b, c in alltag) + "</table>")
    abst = [["2 cm", "1600"], ["4 cm", "400"], ["8 cm", "100"]]
    t3 = ('<table class="mess" style="width:90mm"><tr><th>Abstand</th><th>Zählrate pro Minute (ohne Nullrate)</th></tr>'
          + "".join(f'<tr><td class="v">{a}</td>' + (f'<td class="{"v" if i == 0 else "l"}">{b}</td>' if (l or i == 0) else "<td></td>") + "</tr>" for i, (a, b) in enumerate(abst)) + "</table>")
    return (kopf("W08", "F3 — Aktivität und Zählrate", l)
            + aufg(1, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(2, 1, "Auch in unserem Alltag gibt es radioaktive Stoffe. Rechne die Aktivität um.") + t2
            + aufg(3, 1, "Versuch: Abstandsreihe (Lehrerversuch). Ergänze, wenn sich die Zählrate bei doppeltem Abstand jeweils viertelt.") + t3
            + aufg(4, 2, "Ein Präparat mit Cäsium-137 (Halbwertszeit 30 Jahre) hat heute eine Aktivität von 8000 Bq. Wie groß ist sie in 30, 60 und 90 Jahren?")
            + antwort("30 Jahre: 4000 Bq, 60 Jahre: 2000 Bq, 90 Jahre: 1000 Bq. Die Aktivität halbiert sich wie die Zahl der Kerne.", l, 2))


# ================================================================ W09 Übungen Halbwertszeit
def w09(l):
    z1 = reihe([("Von 1600 Kernen sind nach 1, 2, 3 und 4 Halbwertszeiten noch wie viele da?", "800, 400, 200, 100")], l)
    z2 = ('<table class="mess" style="width:100%"><tr><th style="text-align:left">Nuklid</th><th>Halbwertszeit</th><th>Zeit, bis nur noch 25 % übrig sind</th></tr>'
          + "".join(f'<tr><td style="text-align:left">{a}</td><td class="v">{b}</td>' + (f'<td class="l">{c}</td>' if l else "<td></td>") + "</tr>"
                    for a, b, c in (("Iod-123", "13,2 h", "26,4 h"), ("Radon-222", "3,8 Tage", "7,6 Tage"), ("Cäsium-137", "30 Jahre", "60 Jahre"))) + "</table>")
    return (kopf("W09", "F3 — Übungen zur Halbwertszeit", l)
            + aufg(1, 0, "Halbieren") + z1
            + aufg(2, 0, "Ergänze die Tabelle.") + z2
            + aufg(3, 1, "Krypton-85 hat eine Halbwertszeit von etwa 11 Jahren. Von 16 g, wie viel ist nach 33 Jahren noch übrig?")
            + antwort("33 Jahre sind 3 Halbwertszeiten: 16 g → 8 g → 4 g → 2 g.", l, 1)
            + aufg(4, 1, "Eine Probe enthält 10 000 C-14-Kerne (Halbwertszeit 5730 Jahre). Nach welcher Zeit sind nur noch etwa 312 übrig?")
            + antwort("10 000 → 5000 → 2500 → 1250 → 625 → 312,5: 5 Halbwertszeiten, also etwa 28 650 Jahre.", l, 1)
            + aufg(5, 1, "Die Leuchtziffern einer Uhr enthalten Tritium (Halbwertszeit 12,3 Jahre). Wie viel Prozent sind nach 24,6 Jahren noch da?")
            + antwort("24,6 Jahre sind 2 Halbwertszeiten, es sind noch 25 % da. Die Ziffern leuchten deutlich schwächer.", l, 1)
            + aufg(6, 2, "Uran-238 zerfällt über viele Schritte in das stabile Blei-206. Wie viele α- und wie viele β⁻-Zerfälle sind das?")
            + antwort("Massenzahl: 238 − 206 = 32, jeder α-Zerfall nimmt 4 weg, also 8 α-Zerfälle. Diese senken Z um 16 auf 76. "
                      "Blei hat Z = 82, also sind 6 β⁻-Zerfälle nötig (jeder erhöht Z um 1).", l, 2)
            + aufg(7, 2, "1986 wurde beim Unfall in Tschernobyl Cäsium-137 freigesetzt. In welchem Jahr ist davon nur noch ein Achtel übrig?")
            + antwort("Ein Achtel nach 3 Halbwertszeiten: 3 · 30 Jahre = 90 Jahre, also etwa im Jahr 2076.", l, 1))


# ================================================================ W12 Ionisierende Strahlung
def w12(l):
    lt = luecken("Radioaktive Strahlung ist so energiereich, dass sie [[Elektronen]] aus Atomen herausschlägt. Zurück bleibt ein positiv geladenes "
                 "[[Ion]]. Deshalb heißt sie [[ionisierende]] Strahlung. Im Körper können dadurch [[Moleküle]] verändert werden.", l)
    spuren = [("kurze, dicke, gerade Spuren, alle etwa gleich lang", "α"), ("lange, dünne, oft verbogene Spuren", "β"), ("kaum Spuren, nur ab und zu eine", "γ")]
    return (kopf("W12", "F4 — Warum heißt sie ionisierende Strahlung?", l)
            + aufg(1, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(2, 1, "In einer Nebelkammer werden die Spuren der Strahlung sichtbar. Ordne die Strahlungsart zu.")
            + reihe(spuren, l)
            + aufg(3, 1, "Welche Strahlungsart erzeugt auf kurzer Strecke die meisten Ionen? Begründe.")
            + antwort("α-Strahlung. Die Teilchen sind groß, schwer und doppelt geladen. Sie stoßen sehr oft mit Atomen zusammen und geben "
                      "ihre Energie auf wenigen Zentimetern Luft oder Bruchteilen eines Millimeters Gewebe ab.", l, 2)
            + aufg(4, 1, "Das Zählrohr und die Nebelkammer nutzen beide die Ionisation. Erkläre das für eines der beiden Geräte.")
            + antwort("Zählrohr: Die Strahlung ionisiert das Gas im Rohr. Die Ladungen fließen zum Draht, es gibt einen Stromstoß (Impuls). "
                      "Nebelkammer: An den Ionen kondensieren kleine Tröpfchen, die Spur wird wie ein Kondensstreifen sichtbar.", l, 3)
            + aufg(5, 2, "α-Strahlung kommt nicht einmal durch die Haut. Warum ist ein α-Strahler trotzdem gefährlich, wenn man ihn einatmet?")
            + antwort("Im Körper liegt keine schützende Haut dazwischen. Die α-Teilchen geben ihre ganze Energie direkt an die Zellen der Lunge ab "
                      "und ionisieren dort sehr viele Moleküle auf engem Raum.", l, 3))


# ================================================================ W13 Wirkung auf den Körper
def w13(l):
    folgen = [("Die Zelle repariert den Schaden.", "Reparatur, keine Folgen"), ("Die Zelle stirbt ab.", "Zelltod, der Körper ersetzt sie"),
              ("Die DNA bleibt verändert.", "Veränderung, später evtl. Krebs")]
    zuordnen = [("Übelkeit und Haarausfall wenige Tage nach sehr hoher Dosis", "somatischer Frühschaden"), ("Leukämie viele Jahre später", "somatischer Spätschaden"),
                ("Fehlbildung bei einem Kind, dessen Vater bestrahlt wurde", "genetischer Schaden")]
    dosis = [("natürliche Strahlung", "2,1 mSv"), ("2 Flüge nach New York und zurück (je 0,1 mSv)", "0,2 mSv"),
             ("1 Röntgenbild des Brustkorbs (0,02 mSv)", "0,02 mSv"), ("1 CT des Kopfes (2 mSv)", "2 mSv"), ("<b>Summe</b>", "<b>4,32 mSv</b>")]
    return (kopf("W13", "F4 — Was macht Strahlung mit dem Körper?", l)
            + aufg(1, 0, "Trifft Strahlung die DNA im Zellkern, gibt es drei Möglichkeiten. Ergänze.") + reihe(folgen, l)
            + aufg(2, 1, "Ordne zu: somatischer Frühschaden, somatischer Spätschaden, genetischer Schaden.") + reihe(zuordnen, l)
            + aufg(3, 1, "Berechne die Jahresdosis von Lena. Vergleiche mit dem Durchschnitt in Deutschland (etwa 3,6 mSv).") + reihe(dosis, l)
            + antwort("Lena liegt mit 4,32 mSv etwas über dem Durchschnitt, vor allem wegen des CT.", l, 1)
            + aufg(4, 2, "Nenne vier Dinge, von denen abhängt, wie stark ein Strahlenschaden ist.")
            + antwort("Art der Strahlung, Dosis (Menge der Strahlung), Abstand zur Quelle, Dauer der Bestrahlung, welches Organ getroffen wird "
                      "(z. B. Knochenmark und Keimdrüsen sind besonders empfindlich).", l, 2))


# ================================================================ W15 Schutz und Anwendungen
def w15(l):
    lt = luecken("Die fünf A-Regeln im Strahlenschutz: [[Abstand]] halten, [[Aufenthaltsdauer]] kurz halten, [[Abschirmung]] nutzen, "
                 "[[Aktivität]] so klein wie möglich halten und die [[Aufnahme]] in den Körper vermeiden.", l)
    abst = reihe([("In 1 m Abstand misst man 8 µSv pro Stunde. Wie viel in 2 m?", "2 µSv pro Stunde"), ("… und in 4 m?", "0,5 µSv pro Stunde"),
                  ("Man bleibt statt 1 Stunde nur 15 Minuten in 1 m Abstand. Welche Dosis?", "2 µSv")], l)
    anw = reihe([("Röntgenbild", "Knochen halten mehr Strahlung auf als Gewebe, sie erscheinen hell."),
                 ("Szintigramm", "Ein schwach radioaktiver Stoff sammelt sich im Organ und macht es sichtbar."),
                 ("Strahlentherapie", "Strahlung wird gezielt auf den Tumor gerichtet und zerstört Krebszellen."),
                 ("Sterilisation", "γ-Strahlung tötet Keime auf Spritzen und Verbandszeug.")], l)
    return (kopf("W15", "F4 — Schutz und Anwendungen", l)
            + aufg(1, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(2, 1, "Abstand und Zeit") + abst
            + aufg(3, 1, "Beschreibe, wie die Strahlung genutzt wird.") + anw
            + aufg(4, 2, "Für ein Szintigramm nimmt man Stoffe mit einer Halbwertszeit von wenigen Stunden. Begründe.")
            + antwort("Die Untersuchung dauert nur kurz. Danach soll der Stoff schnell zerfallen sein, damit der Körper wenig Strahlung abbekommt.", l, 2)
            + aufg(5, 2, "Warum ist die Radonbelastung im Keller oft höher? Was hilft dagegen?")
            + antwort("Radon strömt als Gas aus dem Boden durch Risse ins Haus und sammelt sich in den unteren Räumen. Regelmäßiges Lüften senkt die Belastung stark.", l, 2))


# ================================================================ W16 Kernspaltung
def w16(l):
    lt = luecken("1938 beschossen [[Otto Hahn]] und Fritz Straßmann Uran mit Neutronen und fanden danach das viel leichtere [[Barium]]. "
                 "Lise Meitner erklärte das: Der Urankern war [[gespalten]] worden. Trifft ein [[Neutron]] einen Uran-235-Kern, entsteht der instabile Kern "
                 "Uran-236. Er zerfällt in zwei [[mittelschwere]] Kerne, dazu werden [[2 oder 3]] Neutronen und viel Energie frei.", l)
    def g(b1, b2, n):
        links = f'{nk("n", 1, 0)} + {nk("U", 235, 92)} →'
        return f'<p class="gl">{links} {b1} + {b2} + {n} {nk("n", 1, 0)}</p>'
    L = lambda s: f'<span class="loesungstext">{s}</span>' if l else '<span class="luecke"></span>'
    gl = (g(nk("Mo", 103, 42), nk("Sn", 131, 50), L("2"))
          + g(nk("I", L("137") if l else "?", 53), nk("Y", 96, 39), "3")
          + g(nk("Xe", 143, 54), L(nk("Sr", 90, 38)) if l else '<span class="luecke"></span>', "3"))
    return (kopf("W16", "F5 — Die Kernspaltung", l)
            + aufg(1, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(2, 1, "Ergänze die fehlenden Zahlen oder Kerne. Oben und unten muss die Summe links und rechts gleich sein.") + gl
            + aufg(3, 1, "Warum nimmt man für die Spaltung Neutronen und keine Protonen?")
            + antwort("Neutronen sind ungeladen. Sie werden vom positiven Kern nicht abgestoßen und können leicht eindringen.", l, 2)
            + aufg(4, 2, "1 kg Uran-235 liefert bei vollständiger Spaltung so viel Wärme wie etwa 3000 t Steinkohle. Wie viele Güterwagen mit je 60 t Kohle sind das?")
            + antwort("3000 t : 60 t = 50 Güterwagen, also ein ganzer Kohlezug, gegen einen Würfel Uran von etwa 3,7 cm Kantenlänge.", l, 1)
            + aufg(5, 2, "Jemand behauptet: „Wasserstoff kann man mit einem Neutron spalten.“ Nimm Stellung.")
            + antwort("Falsch. Ein Wasserstoffkern besteht nur aus einem Proton, da gibt es nichts zu spalten. Das Neutron kann höchstens eingefangen werden, "
                      "dann entsteht Deuterium.", l, 2))


# ================================================================ W17 Kettenreaktion, Dominos
def w17(l):
    beob = ('<p class="beobachtungstext loesungstext">Schritt 1: Die Steine fallen nacheinander, gleichmäßig. Schritt 2: Die Zahl der fallenden Steine wächst '
            'schnell, alles ist in kurzer Zeit umgefallen. Schritt 3: Es fällt immer nur ein Stein zur gleichen Zeit, die Kette läuft gleichmäßig.</p>') if l else ""
    bauteile = [("Brennstäbe", "enthalten das Uran, hier finden die Spaltungen statt"), ("Steuerstäbe", "fangen überschüssige Neutronen ein"),
                ("Moderator (Wasser)", "bremst die schnellen Neutronen ab"), ("Kühlmittel (Wasser)", "transportiert die Wärme ab")]
    gen = ('<table class="mess" style="width:100%"><tr><th>Generation</th>' + "".join(f"<th>{i}</th>" for i in range(1, 6)) + "</tr>"
           + "".join(f'<tr><td class="v">{t}</td>' + "".join((f'<td class="{"v" if j == 0 else "l"}">{v}</td>' if (l or j == 0) else "<td></td>") for j, v in enumerate(w)) + "</tr>"
                     for t, w in (("2 Neutronen wirksam", [1, 2, 4, 8, 16]), ("3 Neutronen wirksam", [1, 3, 9, 27, 81]))) + "</table>")
    return (kopf("W17", "F5 — Versuch: Kettenreaktion mit Dominosteinen", l)
            + aufg(1, None, "Versuchsbeschreibung") + '<ol class="liste">'
            '<li><b>Schritt 1:</b> Stellt die Dominosteine in einer Reihe auf und stoßt den ersten an.</li>'
            '<li><b>Schritt 2:</b> Baut so um, dass jeder Stein zwei weitere umwirft (2, 4, 8 …). Stoßt nur einen Stein an.</li>'
            '<li><b>Schritt 3:</b> Nehmt aus dem Aufbau von Schritt 2 so viele Steine heraus, dass immer gleich viele Steine umfallen.</li></ol>'
            + aufg(2, 0, "Beschreibe deine Beobachtung.") + feld(beob, 22)
            + aufg(3, 1, "Welcher Schritt entspricht einer unkontrollierten, welcher einer kontrollierten Kettenreaktion?")
            + antwort("Schritt 2: unkontrolliert (Lawine). Schritt 3: kontrolliert wie im Reaktor.", l, 1)
            + aufg(4, 1, "Wie viele Spaltungen gibt es in jeder Generation?") + gen
            + aufg(5, 1, "Ergänze die Aufgabe der Bauteile im Reaktor.") + reihe(bauteile, l)
            + aufg(6, 2, "Welches Bauteil übernimmt im Reaktor die Aufgabe der herausgenommenen Dominosteine?")
            + antwort("Die Steuerstäbe. Sie fangen so viele Neutronen ein, dass im Mittel genau eine neue Spaltung ausgelöst wird.", l, 1))


# ================================================================ W18 Kernkraftwerk und Fusion
def kkw_svg(l):
    lab = ["Reaktor", "Dampferzeuger", "Turbine", "Generator", "Kondensator", "Kühlturm"]
    o = ['<svg viewBox="0 0 300 120" style="width:100%;height:100%">',
         '<path d="M10 110 V50 a40 40 0 0 1 80 0 V110z" fill="#EEF1F5" stroke="#14171c" stroke-width="1"/>',
         '<rect x="20" y="60" width="26" height="42" rx="6" fill="#F7D3CC" stroke="#14171c" stroke-width=".8"/>',
         '<rect x="58" y="48" width="20" height="54" rx="8" fill="#DCE6F2" stroke="#14171c" stroke-width=".8"/>',
         '<path d="M46 70 H58 M58 94 H46" stroke="#D8453B" stroke-width="1.6"/>',
         '<path d="M78 56 H130 M150 80 V96 H78" stroke="#3B7CC4" stroke-width="1.6" fill="none"/>',
         '<path d="M130 46 L154 40 L154 72 L130 66Z" fill="#9FB2CF" stroke="#14171c" stroke-width=".8"/>',
         '<line x1="154" y1="56" x2="170" y2="56" stroke="#14171c" stroke-width="1.5"/><circle cx="182" cy="56" r="11" fill="#FFE7A0" stroke="#14171c" stroke-width=".8"/>',
         '<rect x="136" y="80" width="30" height="22" rx="3" fill="#DCE6F2" stroke="#14171c" stroke-width=".8"/>',
         '<path d="M166 86 H236 M236 98 H166" stroke="#3FA34D" stroke-width="1.6"/>',
         '<path d="M230 112 L240 60 Q255 52 270 60 L280 112Z" fill="#EEF1F5" stroke="#14171c" stroke-width="1"/>']
    pos = [(33, 80, 33, 9), (68, 48, 90, 9), (142, 44, 142, 9), (182, 45, 200, 20), (150, 102, 150, 118), (255, 60, 255, 20)]
    for i, (x, y, tx, ty) in enumerate(pos):
        o.append(f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty + (-3 if ty < 60 else -7)}" stroke="{GRAU}" stroke-width=".5"/>')
        o.append(f'<text x="{tx}" y="{ty}" font-size="6.5" text-anchor="middle" fill="{MAG if l else "#14171c"}">{lab[i] if l else str(i + 1) + " _______"}</text>')
    return "".join(o) + "</svg>"


def w18(l):
    lt = luecken("Im [[Primärkreislauf]] nimmt Wasser die Wärme im Reaktor auf. Es ist radioaktiv belastet und bleibt im Reaktorgebäude. "
                 "Im [[Dampferzeuger]] gibt es die Wärme an den Sekundärkreislauf ab. Dessen Dampf treibt die [[Turbine]] an. "
                 "Im [[Kühlkreislauf]] kühlt Flusswasser den Dampf im Kondensator wieder zu Wasser.", l)
    kette = (f'<p class="frage">Kernenergie → {"<span class=\"loesungstext\">innere Energie (Wärme)</span>" if l else "<span class=\"luecke\" style=\"min-width:40mm\"></span>"} → '
             f'{"<span class=\"loesungstext\">Bewegungsenergie</span>" if l else "<span class=\"luecke\" style=\"min-width:34mm\"></span>"} → '
             f'{"<span class=\"loesungstext\">elektrische Energie</span>" if l else "<span class=\"luecke\" style=\"min-width:34mm\"></span>"}</p>')
    L = lambda s: f'<span class="loesungstext">{s}</span>' if l else '<span class="luecke"></span>'
    fus = f'<p class="gl">{nk("H", 2, 1)} + {nk("H", 3, 1)} → {L(nk("He", 4, 2))} + {L(nk("n", 1, 0))} + Energie</p>'
    return (kopf("W18", "F5 — Kernkraftwerk und Kernfusion", l)
            + aufg(1, 0, "Beschrifte das Kernkraftwerk.") + f'<div style="height:42mm;margin:1mm 0 2mm">{kkw_svg(l)}</div>'
            + aufg(2, 1, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(3, 1, "Ergänze die Energieumwandlungen im Kernkraftwerk.") + kette
            + antwort("Im Kohlekraftwerk ist nur der erste Schritt anders: chemische Energie der Kohle statt Kernenergie.", l, 1)
            + aufg(4, 0, "Ergänze die Gleichung für die Kernfusion.") + fus
            + aufg(5, 2, "Warum ist die Kernfusion auf der Erde so schwer umzusetzen?")
            + antwort("Die Kerne sind positiv und stoßen sich stark ab. Sie verschmelzen erst bei über 100 Mio. °C. Ein so heißes Plasma darf keine Wand berühren "
                      "und muss mit Magnetfeldern eingeschlossen werden.", l, 2))


# ================================================================ W19 Übungen Kernenergie
def w19(l):
    L = lambda s: f'<span class="loesungstext">{s}</span>' if l else '<span class="luecke"></span>'
    unf = ('<table class="mess" style="width:100%"><tr><th></th><th>Tschernobyl</th><th>Fukushima</th></tr>'
           + "".join(f'<tr><td class="v" style="text-align:left">{a}</td>' + (f'<td class="l">{b}</td><td class="l">{c}</td>' if l else "<td></td><td></td>") + "</tr>"
                     for a, b, c in (("Datum", "26.04.1986", "11.03.2011"), ("Auslöser", "missglückter Test, Reaktor gerät außer Kontrolle", "Erdbeben und Tsunami, Kühlung fällt aus"),
                                     ("Folge", "Explosion, Graphitbrand, radioaktive Wolke über Europa", "Kernschmelze, Wasserstoffexplosionen, verseuchtes Wasser"))) + "</table>")
    gen = ('<table class="mess" style="width:100%"><tr><th>Generation</th>' + "".join(f"<th>{i}</th>" for i in range(1, 6)) + "</tr>"
           + "".join(f'<tr><td class="v">{t}</td>' + "".join((f'<td class="{"v" if j == 0 else "l"}">{v}</td>' if (l or j == 0) else "<td></td>") for j, v in enumerate(w)) + "</tr>"
                     for t, w in (("2 Neutronen wirksam", [1, 2, 4, 8, 16]), ("3 Neutronen wirksam", [1, 3, 9, 27, 81]))) + "</table>")
    return (kopf("W19", "F5 — Übungen zur Kernenergie", l)
            + aufg(1, 0, "Nenne zwei Maßnahmen, mit denen eine Kettenreaktion im Reaktor kontrolliert wird.")
            + antwort("Steuerstäbe fangen Neutronen ein. Borsäure im Kühlwasser schluckt ebenfalls Neutronen.", l, 1)
            + aufg(2, 1, "Bei einer Spaltung von Uran-235 entstehen Zinn-131 und zwei Neutronen. Ergänze.")
            + f'<p class="gl">{nk("n", 1, 0)} + {nk("U", 235, 92)} → {nk("Sn", 131, 50)} + {L(nk("Mo", 103, 42))} + 2 {nk("n", 1, 0)}</p>'
            + aufg(3, 1, "Auch Plutonium-239 lässt sich spalten. Es entstehen Barium-144 und Strontium-94. Wie viele Neutronen werden frei?")
            + f'<p class="gl">{nk("n", 1, 0)} + {nk("Pu", 239, 94)} → {nk("Ba", 144, 56)} + {nk("Sr", 94, 38)} + {L("2")} {nk("n", 1, 0)}</p>'
            + aufg(4, 1, "Wie viele Spaltungen gibt es in jeder Generation?") + gen
            + aufg(5, 1, "1 kg Uran-235 liefert so viel Wärme wie etwa 3000 t Steinkohle. Wie viele Güterwagen mit je 60 t Kohle sind das?")
            + antwort("3000 t : 60 t = 50 Güterwagen, ein ganzer Kohlezug.", l, 1)
            + aufg(6, 1, "Vergleiche die beiden großen Reaktorunfälle.") + unf
            + aufg(7, 2, "Was bedeutet GAU? Warum spricht man bei Tschernobyl und Fukushima vom „Super-GAU“?")
            + antwort("GAU heißt größter anzunehmender Unfall: der schwerste Unfall, den die Anlage nach Plan noch beherrschen muss. "
                      "In Tschernobyl und Fukushima wurde diese Grenze überschritten, Radioaktivität gelangte in großen Mengen nach außen.", l, 2)
            + aufg(8, 2, "Jemand behauptet: „Wasserstoff kann man mit einem Neutron spalten.“ Nimm Stellung.")
            + antwort("Falsch. Ein Wasserstoffkern besteht nur aus einem Proton, da gibt es nichts zu spalten. Das Neutron kann höchstens eingefangen werden, "
                      "dann entsteht Deuterium.", l, 2))


# ================================================================ W20 Radioaktiver Abfall
def w20(l):
    lt = luecken("Abgebrannte Brennelemente kühlen zuerst einige Jahre im [[Abklingbecken]]. Danach kommen sie in [[Castor-Behältern]] "
                 "in ein [[Zwischenlager]]. Für hochradioaktiven Abfall gibt es in Deutschland noch kein [[Endlager]]. Es muss etwa "
                 "[[eine Million]] Jahre sicher sein.", l)
    gest = ('<table class="mess" style="width:100%"><tr><th>Gestein</th><th>Vorteil</th><th>Nachteil</th></tr>'
            + "".join(f'<tr><td class="v">{a}</td>' + (f'<td class="l">{b}</td><td class="l">{c}</td>' if l else "<td></td><td></td>") + "</tr>"
                      for a, b, c in (("Steinsalz", "dicht, leitet Wärme gut, schließt Hohlräume", "löst sich in Wasser"),
                                      ("Ton", "fast wasserdicht, hält Stoffe gut zurück", "leitet Wärme schlecht, wenig stabil"),
                                      ("Granit", "sehr fest und hitzebeständig", "kann Risse haben, durch die Wasser dringt"))) + "</table>")
    return (kopf("W20", "F6 — Der radioaktive Abfall", l)
            + aufg(1, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(2, 1, "Nenne vier Anforderungen an ein Endlager.")
            + antwort("dicht gegen Wasser und Gase, keine Verbindung zum Grundwasser, gute Wärmeableitung, stabiles Gestein ohne Erdbeben, "
                      "kein Weg zurück an die Erdoberfläche.", l, 2)
            + aufg(3, 1, "Ergänze die Tabelle zu den drei möglichen Wirtsgesteinen.") + gest
            + aufg(4, 1, "Beim Rückbau unterscheidet man kontaminierte und aktivierte Teile. Erkläre den Unterschied.")
            + antwort("Kontaminiert: Radioaktive Stoffe haften nur an der Oberfläche, man kann sie abwaschen oder abschleifen. "
                      "Aktiviert: Das Material selbst ist durch Neutronen radioaktiv geworden, es muss als Abfall gelagert werden.", l, 2)
            + aufg(5, 2, "Der Rückbau eines Kernkraftwerks kostet oft mehr als der Bau. Begründe.")
            + antwort("Alle Teile müssen auf Strahlung geprüft, zerlegt, gereinigt oder verpackt werden, oft fernbedient oder unter Wasser. "
                      "Der Strahlenschutz für Arbeiter und Umwelt kostet Zeit. Dazu kommt die teure Lagerung des Abfalls.", l, 2))


# ================================================================ W21 Argumente abwägen
def w21(l):
    aus = [("Ein Kernkraftwerk stößt im Betrieb kaum CO₂ aus.", "Fakt"), ("Kernkraft ist viel zu gefährlich.", "Meinung"),
           ("Plutonium-239 hat eine Halbwertszeit von etwa 24 000 Jahren.", "Fakt"), ("Ein Endlager findet man sowieso nie.", "Meinung"),
           ("Seit April 2023 ist in Deutschland kein Kernkraftwerk mehr am Netz.", "Fakt"), ("Kernkraft ist die Energie der Zukunft.", "Meinung")]
    t = ('<table class="mess" style="width:100%"><tr><th style="text-align:left">Aussage</th><th>Fakt oder Meinung?</th></tr>'
         + "".join(f'<tr><td style="text-align:left">{a}</td>' + (f'<td class="l">{b}</td>' if l else "<td></td>") + "</tr>" for a, b in aus) + "</table>")
    pc = ('<table class="mess" style="width:100%"><tr><th>spricht für Kernenergie</th><th>spricht dagegen</th></tr>'
          + "".join("<tr>" + (f'<td class="l">{a}</td><td class="l">{b}</td>' if l else "<td></td><td></td>") + "</tr>"
                    for a, b in (("kaum CO₂ im Betrieb", "Abfall strahlt sehr lange"), ("viel Energie aus wenig Brennstoff", "kein Endlager in Betrieb"),
                                 ("Strom unabhängig vom Wetter", "schwere Unfälle möglich"))) + "</table>")
    return (kopf("W21", "F6 — Nutzen und Risiko abwägen", l)
            + aufg(1, 0, "Ist das ein physikalischer Fakt oder eine Meinung?") + t
            + aufg(2, 1, "Sammle je drei Argumente." + (' <span class="loesungstext">mögliche Lösung</span>' if l else "")) + pc
            + aufg(3, 2, "Schreibe eine eigene Stellungnahme in 3 bis 5 Sätzen. Nutze mindestens einen Fakt mit Zahl.")
            + antwort("Individuelle Lösung. Gute Stellungnahmen trennen Fakten von Meinung, nennen eine Größenordnung "
                      "(z. B. 24 000 Jahre Halbwertszeit, 1 kg Uran wie 3000 t Kohle) und wägen Nutzen und Risiko gegeneinander ab.", l, 5))


# ================================================================ W22 Altersbestimmung
def w22(l):
    lt = luecken("In der Atmosphäre entsteht ständig [[C-14]]. Lebewesen nehmen es auf, solange sie [[leben]]. Danach kommt kein C-14 mehr dazu, "
                 "es zerfällt mit einer Halbwertszeit von [[5730]] Jahren. Aus dem noch vorhandenen Anteil lässt sich das [[Alter]] bestimmen.", l)
    t = ('<table class="mess" style="width:110mm"><tr><th>C-14 noch vorhanden</th><th>Alter</th></tr>'
         + "".join(f'<tr><td class="v">{a}</td>' + (f'<td class="l">{b}</td>' if l else "<td></td>") + "</tr>"
                   for a, b in (("50 %", "5730 Jahre"), ("25 %", "11 460 Jahre"), ("12,5 %", "17 190 Jahre"))) + "</table>")
    return (kopf("W22", "Rückblick — Altersbestimmung mit C-14", l)
            + aufg(1, 0, "Fülle die Lücken aus.") + f'<p class="frage lt">{lt}</p>'
            + aufg(2, 0, "Ergänze das Alter.") + t
            + aufg(3, 1, "Bei der Gletschermumie Ötzi fand man noch etwa 53 % des ursprünglichen C-14. Schätze sein Alter.")
            + antwort("Etwas weniger als eine Halbwertszeit, also knapp 5730 Jahre. Genau gerechnet sind es etwa 5300 Jahre.", l, 1)
            + aufg(4, 1, "Die Tritium-Methode bestimmt das Alter von Wasser. Tritium hat 12,3 Jahre Halbwertszeit. Warum reicht sie nur etwa 50 Jahre zurück?")
            + antwort("Nach 50 Jahren sind etwa 4 Halbwertszeiten vergangen, es sind nur noch rund 6 % übrig. Danach ist zu wenig Tritium zum genauen Messen da.", l, 2)
            + aufg(5, 2, "Warum kann man mit der C-14-Methode keine Dinosaurierknochen datieren?")
            + antwort("Dinosaurier starben vor etwa 66 Millionen Jahren. Das sind über 10 000 Halbwertszeiten, vom C-14 ist nichts mehr übrig. "
                      "Die Methode reicht nur bis etwa 50 000 Jahre.", l, 2))


# W16 bis W18 ersetzt durch das Begleitheft (baue_begleitheft_kernspaltung.py), alte Blätter liegen in _alt/
BLAETTER = [
    ("wuerfel.html", "Zerfall mit Wuerfeln W06.pdf", "Zerfall mit Würfeln – W06", w06),
    ("halbwertszeit.html", "Halbwertszeit W07.pdf", "Die Halbwertszeit – W07", w07),
    ("aktivitaet.html", "Aktivitaet und Zaehlrate W08.pdf", "Aktivität und Zählrate – W08", w08),
    ("uebungen_hwz.html", "Uebungen Halbwertszeit W09.pdf", "Übungen zur Halbwertszeit – W09", w09),
    ("ionisierend.html", "Ionisierende Strahlung W12.pdf", "Ionisierende Strahlung – W12", w12),
    ("wirkung.html", "Wirkung auf den Koerper W13.pdf", "Wirkung auf den Körper – W13", w13),
    ("schutz.html", "Schutz und Anwendungen W15.pdf", "Schutz und Anwendungen – W15", w15),
    ("uebungen_kernenergie.html", "Uebungen Kernenergie W19.pdf", "Übungen zur Kernenergie – W19", w19),
    ("abfall.html", "Radioaktiver Abfall W20.pdf", "Der radioaktive Abfall – W20", w20),
    ("argumente.html", "Argumente abwaegen W21.pdf", "Nutzen und Risiko abwägen – W21", w21),
    ("altersbestimmung.html", "Altersbestimmung W22.pdf", "Altersbestimmung – W22", w22),
]

if __name__ == "__main__":
    import sys
    nur = sys.argv[1:]
    for html, pdf, titel, fn in BLAETTER:
        if nur and not any(n in pdf for n in nur):
            continue
        (HIER / html).write_text(dokument(titel, [fn(False), fn(True)]), encoding="utf-8")
        drucke(html, pdf)
