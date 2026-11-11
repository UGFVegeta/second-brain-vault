#!/usr/bin/env python3
"""Stunden-HTMLs Leitfrage 5 (Mondphasen, Finsternisse) und Lochkamera mit Rückblick Optik I.
python3 baue_stunden_f5_lk.py   -> nur die HTMLs im Vault (Export nach iCloud erst nach Freigabe)"""
import math, re
from stunde_vorlage import basis, blatt, chip, tabellenfolie, bau_stunde, ab
from folien_zeichnungen import Z, GELB, INK
from animationen_f5 import erde_folie, mond_folie

# ====================================================================== Do 05.11.2026: Rückseite Schattenwurf, Einschub Jahreszeiten
# Oskars Plan: 1. Rückseite des Versuchsblatts F4 besprechen (letztes Mal nicht geschafft), 2. Einschub „Warum gibt es Jahreszeiten?“
# am Tellurium (nach seinem Foliensatz „Wie entstehen die Jahreszeiten“, iCloud Optik/3. Mondphasen …), 3. Einstieg Leitfrage 5, so weit es reicht.
SW_PDF = "Schattenwurf W06 Rückseite.pdf"
def erde(z, x, y, sx, sy, r=15, nord=True):
    """Erde mit Tag- und Nachtseite (Nacht auf der von der Sonne abgewandten Seite) und um 23,5° geneigter Achse (oben nach rechts)."""
    a = math.atan2(sy - y, sx - x)
    p = lambda w: (x + r * math.cos(w), y + r * math.sin(w))
    (x1, y1), (x2, y2) = p(a + math.pi / 2), p(a + 3 * math.pi / 2)
    z.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3B7CC4"/>'
          f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}Z" fill="#05080F" fill-opacity=".42"/>')
    ux, uy = math.sin(math.radians(23.5)), -math.cos(math.radians(23.5))
    z.line(x - 24 * ux, y - 24 * uy, x + 24 * ux, y + 24 * uy, INK, 1.6)
    if nord:
        z.text(x + 31 * ux, y + 31 * uy + 3, "N", "middle", 9.5)
    return z


def erdbahn():
    """Erdbahn als flache Ellipse (Blick schräg von oben), vier Stellungen, Achse immer gleich geneigt. Sonne leicht zur Winterseite
    verschoben: Anfang Januar ist die Erde der Sonne am nächsten."""
    z = Z("jz")
    cx, cy, rx, ry = 318, 106, 215, 68
    S = (330, 106)
    z.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#66798E" stroke-width="1.4"/>')
    for t in (5 * math.pi / 4, math.pi / 4):          # Umlaufsinn: Sommer (links) -> Herbst (vorne) -> Winter (rechts) -> Frühling (hinten)
        x, y = cx + rx * math.cos(t), cy - ry * math.sin(t)
        dx, dy = -rx * math.sin(t), -ry * math.cos(t)
        l = math.hypot(dx, dy)
        z.pfeil(x - 7 * dx / l, y - 7 * dy / l, x + 7 * dx / l, y + 7 * dy / l, "#66798E", 1.4, 9)
    z.sonne(*S, 16)
    z.text(S[0] + 30, S[1] + 30, "Sonne")
    for t, z1, z2, tx, ty, anc in ((math.pi, "Sommeranfang", "21. Juni", 0, 34, "middle"), (0, "Winteranfang", "21. Dezember", 0, 34, "middle"),
                                   (math.pi / 2, "Frühlingsanfang, 20. März", "", 24, 3, "start"),
                                   (3 * math.pi / 2, "Herbstanfang, 23. September", "", 24, 8, "start")):
        x, y = cx + rx * math.cos(t), cy - ry * math.sin(t)
        erde(z, x, y, *S)
        z.text(x + tx, y + ty, z1, anc)
        if z2:
            z.text(x + tx, y + ty + 13, z2, anc)
    # Winkel der Erdachse an der Winterstellung
    wx, wy = cx + rx, cy
    z.line(wx, wy, wx, wy - 34, "#66798E", 1.1, "3 3")
    b = math.radians(23.5)
    z.add(f'<path d="M{wx} {wy - 22} A22 22 0 0 1 {wx + 22 * math.sin(b):.1f} {wy - 22 * math.cos(b):.1f}" fill="none" stroke="#66798E" stroke-width="1.2"/>')
    z.text(wx + 30, wy - 18, "23,5°")
    # Drehung um die eigene Achse an der Sommerstellung
    sx, sy = cx - rx, cy
    z.add(f'<path d="M{sx - 26} {sy - 30} Q{sx - 14} {sy - 42} {sx - 2} {sy - 36}" fill="none" stroke="{INK}" stroke-width="1.3"/>'
          f'<polygon points="{sx + 1},{sy - 34} {sx - 8},{sy - 34} {sx - 3},{sy - 41}" fill="{INK}"/>')
    z.text(sx - 30, sy - 46, "Drehung in 24 h", "middle", 9.5)
    z.text(150, 46, "Erdbahn", "middle", 9.5)
    z.text(622, 204, "nicht maßstabsgetreu", "end", 9)
    return z.svg()


def steil_flach():
    """Gleich breites Strahlenbündel (gleiche Strahlung) trifft steil (Sommer, 60°) und flach (Winter, 25°) auf den Boden.
    Beleuchtete Fläche = Bündelbreite : sin(Einfallswinkel), berechnet."""
    z = Z("sf2")
    BODEN, BREITE, N = 176, 48, 5
    z.line(318, 14, 318, 200, "#A3B7D3", 1, "5 4")
    for x0, x1, a, start, laenge, sonne_ab, farbe, f_nr, t1, t2, tx in (
            (30, 296, 60, 140, 130, 34, "#D92D20", "1", "Sommer: Sonne steht hoch", "kleine Fläche: stark erwärmt", 163),
            (336, 620, 25, 470, 142, 74, "#F2A6A0", "2", "Winter: Sonne steht tief", "große Fläche: schwach erwärmt", 478)):
        L = BREITE / math.sin(math.radians(a))
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        z.rect(x0, BODEN, x1 - x0, 10, "#B9A27A", .55)
        treff = [start + i * L / (N - 1) for i in range(N)]
        anf = [(x - laenge * c, BODEN - laenge * s) for x in treff]
        z.poly([anf[0], (treff[0], BODEN), (treff[-1], BODEN), anf[-1]], "#FFC53D", .22)
        for (ax, ay), x in zip(anf, treff):
            z.pfeil(ax, ay, x, BODEN - 1, GELB, 1.8, 7)
        z.rect(start, BODEN - 3, L, 6, farbe)
        mx, my = (anf[0][0] + anf[-1][0]) / 2, (anf[0][1] + anf[-1][1]) / 2
        z.sonne(mx - sonne_ab * c, my - sonne_ab * s, 10)
        z.text(tx, 26 if a > 45 else 84, t1, "start" if a < 45 else "start", weight=600)
        z.formel(start + L + 8, BODEN - 4, "A", f_nr)
        z.text((x0 + x1) / 2, 204, t2, "middle")
    return z.svg()


EINSCHUB = "Einschub Jahreszeiten"
J_FRAGE = ab('<section class="folie"><div class="frageband"><div class="nr">Einschub</div><h2>Warum gibt es Jahreszeiten?</h2></div>'
             '<div class="ab-hinweis">🌍 Am Tellurium: Tag und Nacht, ein Jahr, die geneigte Erdachse</div></section>', "Frage", EINSCHUB, neu=True)
J_BAHN = ab('<section class="folie"><div class="titelband"><h1>Die Erde läuft um die Sonne</h1></div>'
            f'<div class="zeichenzone karo">{erdbahn()}</div>'
            '<div class="merksatz">Die Erde dreht sich in 24 Stunden einmal um ihre Achse und läuft in einem Jahr auf einer elliptischen Bahn '
            'um die Sonne. Die Erdachse ist <b>geneigt</b>. Dadurch ist mal die Nordhalbkugel, mal die Südhalbkugel zur Sonne geneigt.</div></section>', "Erdbahn", EINSCHUB, neu=True, heft=True)
J_WINKEL = ab('<section class="folie"><div class="titelband"><h1>Steile und flache Sonnenstrahlen</h1></div>'
              f'<div class="zeichenzone karo">{steil_flach()}</div>'
              '<div class="merksatz">Im Winter steht die Sonne tiefer, ihre Strahlen fallen <b>flacher</b> ein. Dieselbe Strahlung verteilt sich '
              'auf eine größere Fläche, auf jeden Quadratmeter kommt weniger an. Je flacher die Strahlen, desto weniger wird der Boden erwärmt.</div></section>',
              "Steil und flach", EINSCHUB, neu=True, heft=True)
J_ANTWORT = ab('<section class="folie"><div class="frageband"><div class="nr">Antwort</div><h2>Warum gibt es Jahreszeiten?</h2></div>'
               '<div class="antwortzone">Die Erdachse ist <b>geneigt</b>. Im Sommer ist unsere Nordhalbkugel zur Sonne geneigt: Die Sonne steht hoch, '
               'die Strahlen fallen <span class="rot">steil</span> ein und erwärmen jeden Quadratmeter stark. Im Winter fallen sie '
               '<span class="rot">flach</span> ein, dieselbe Strahlung verteilt sich auf eine größere Fläche. '
               'Nicht der Abstand zur Sonne ist der Grund.</div></section>', "Antwort", EINSCHUB, neu=True)

_sw = blatt(SW_PDF, "w06b", "Rückseite besprechen")
SW_LOESUNG = (_sw[0], '<section class="marke" data-tab="Rückseite Schattenwurf" data-group="Wiederholung" hidden></section>' + _sw[1], _sw[2])
VORSPANN = [SW_LOESUNG, J_FRAGE, J_BAHN, erde_folie(EINSCHUB), J_WINKEL, J_ANTWORT]   # ohne leere Zwillingsfolien (Oskar 04.11.: er zeichnet im PDF in Notability)
V = len(VORSPANN)   # 6 Folien vor Leitfrage 5

# ====================================================================== Leitfrage 5
F5_ALLTAG = tabellenfolie("Mond und Finsternis im Alltag", [
    ("Halbmond am Nachmittag", "Mond am hellen Himmel", "Die Sonne beleuchtet ihn auch tagsüber. Der zunehmende Halbmond steht nachmittags schon am Himmel."),
    ("Vollmond am Abend", "Er geht auf, wenn die Sonne untergeht", "Er steht der Sonne genau gegenüber."),
    ("Blutmond", "Mond bei Mondfinsternis rötlich", "Die Lufthülle der Erde lenkt etwas rotes Licht in den Erdschatten."),
    ("Finsternisbrille", "Sonnenfinsternis nur mit Schutz ansehen", "Das Sonnenlicht kann die Netzhaut dauerhaft schädigen."),
], frage="Warum darf man eine Mondfinsternis ohne Brille ansehen, eine Sonnenfinsternis aber nicht?")

LF5 = "Leitfrage 5"
# Oskar 11.11.2026: kein Styropor-Versuch, stattdessen ein Film aus der FWU-Mediathek
FILM_URL = "https://playout01.edupool.cloud/cloud/bd6551fab35b559c8dd095feb3b3f10b/menu/chapter_1.html"
FILM = ab('<section class="folie"><div class="frageband"><div class="nr">Film</div><h2>Mondphasen und Finsternisse</h2></div>'
          f'<div class="ab-hinweis">🎬 <a href="{FILM_URL}" target="_blank" style="color:inherit">Film aus der FWU-Mediathek öffnen</a></div></section>', "Film", LF5, neu=True)
F5 = VORSPANN + [
    ab(basis(42), "Einstieg", LF5), ab(basis(43), "Einstieg", LF5), ab(basis(45), "Tellurium", LF5),
    FILM,
    ab(basis(47), "Mondphasen", LF5), mond_folie(LF5), ab(basis(49), "Finsternisse", LF5), ab(basis(51), "Finsternisse", LF5), ab(F5_ALLTAG, "Alltag", LF5),
    ab(basis(52), "Antwort, Check", LF5), ab(basis(53), "Antwort, Check", LF5), ab(basis(54), "Antwort, Check", LF5),
]

F5_MATERIAL = {
    "demo": [("Tellurium beleuchtet (Phywe)", "1×", "Tag und Nacht, Jahreszeiten, Mondphasen und Finsternisse vorne zeigen"),
             ("Film aus der FWU-Mediathek", "1×", f'<a href="{FILM_URL}" target="_blank">Link zum Film</a>; vorher testen, Ton am Apple TV prüfen')],
    "schueler": [],
    "hinweis": "Raum gut abdunkeln. Für die Lochkamera in der nächsten Stunde ankündigen: Chipsdose, Transparent- oder Butterbrotpapier, schwarzer Zeichenkarton, Schere, Kleber mitbringen.",
}

F5_SCHRITTE = [
    ("Rückseite", "Rückseite des F4-Blatts besprechen: PDF „Schattenwurf W06 Rückseite“ in Notability (Seite 1 Aufgabe, Seite 2 Lösung). Die Lösung ist Folie 1.", [1]),
    ("Jahreszeiten", "Einschub am Tellurium: Tag und Nacht, ein Jahr, geneigte Erdachse. Vermutungen zur Frage.", [2]),
    ("Erdbahn", "Vorzeichnen, die Klasse zeichnet mit. Danach die Animation: Erde laufen lassen, Neigung auf 0° und zurück auf 23,5° stellen.", [3, 4]),
    ("Steil und flach", "Vorzeichnen, die Klasse zeichnet mit. Antwort ins Heft.", [5, 6]),
    ("Einstieg", "Ab hier Leitfrage 5, so weit es reicht. Vier Wochen Mond, Leitfrage 5, Vermutungen.", [V + 1, V + 2]),
    ("Tellurium", "Vorne am Tellurium zeigen, wo der Mond steht. Folie dazu.", [V + 3]),
    ("Film", f'Film aus der FWU-Mediathek zu Mondphasen und Finsternissen: <a href="{FILM_URL}" target="_blank">Film öffnen</a>.', [V + 4]),
    ("Mondphasen", "Phasen von der Erde aus, 29,5 Tage. Danach die Animation laufen lassen.", [V + 5, V + 6]),
    ("Finsternisse", "Am Tellurium oder im Mondlabor, dann Folien.", [V + 7, V + 8]),
    ("Alltag, Antwort, Check", "Alltag mündlich, Antwort ins Heft, Handzeichen.", [V + 9, V + 10, V + 11, V + 12]),
]

F5_HG = f"""
<div class="box"><h3>Rückseite Schattenwurf {chip(1)}</h3><ul>
<li>Pro Lichtquelle zwei Randstrahlen über die Kanten des Hindernisses bis zum Schirm. Wo keine Lichtquelle hinkommt: Kernschatten (dicht schraffiert). Wo nur eine hinkommt: Halbschatten.</li>
<li>Typischer Fehler: Randstrahlen enden am Hindernis oder werden nicht bis zum Schirm verlängert. Bei d (zwei Hindernisse, eine Lampe) gibt es keinen Halbschatten.</li>
<li>Bei e hilft es, erst alle Strahlen der oberen Lampe zu zeichnen, dann die der unteren, und danach die Gebiete zu zählen.</li></ul></div>

<div class="box"><h3>Jahreszeiten {chip(2, 3, 4, 5, 6)}</h3><ul>
<li>Vorlage: dein Foliensatz „Wie entstehen die Jahreszeiten“ (iCloud, Physik Klasse 7, Optik, 3. Mondphasen …). Neu gezeichnet, gleicher Inhalt.</li>
<li><b>Erdachse:</b> um 23,5° gegen die Senkrechte auf der Erdbahn geneigt, zeigt immer Richtung Polarstern. Am Tellurium sieht man das gut: Die Achse bleibt beim Umlauf parallel.</li>
<li><b>Abstand:</b> Die Bahn ist fast ein Kreis. Anfang Januar ist die Erde der Sonne am nächsten (etwa 147 Mio. km), Anfang Juli am weitesten weg (etwa 152 Mio. km). Bei uns ist im Januar Winter, der Abstand kann also nicht der Grund sein.</li>
<li><b>Sonnenhöhe mittags in Schorndorf:</b> im Juni etwa 65°, im Dezember nur etwa 18°.</li>
<li>Zweiter Grund (wie auf deinem alten Blatt): Im Sommer sind die Tage länger, die Sonne scheint länger.</li>
<li><b>Typische Fehlvorstellungen:</b> Im Sommer ist die Erde näher an der Sonne. Die Erdachse kippt im Lauf des Jahres hin und her.</li>
<li>Versuch zum Zeigen (ohne Bauen): Taschenlampe senkrecht und schräg auf kariertes Papier halten, Kästchen im Lichtfleck zählen.</li>
<li><b>Animation (Folie 4):</b> Mit dem Neigungsregler auf 0° sieht man: Ohne geneigte Achse ist keine Halbkugel zur Sonne geneigt, es gäbe keine Jahreszeiten. Die Achse bleibt beim Umlauf parallel.</li></ul></div>

<div class="box"><h3>Wo steht der Mond? {chip(V + 3)}</h3><ul>
<li>Der Mond läuft in etwa 27,3 Tagen einmal um die Erde. Von Neumond bis Neumond dauert es 29,5 Tage, weil die Erde in dieser Zeit ein Stück um die Sonne weiterwandert.</li>
<li><b>Umlaufsinn:</b> Von Norden aus gesehen läuft der Mond gegen den Uhrzeigersinn. Liegt die Sonne in der Zeichnung links, steht der zunehmende Mond unten, der abnehmende oben.</li>
<li><b>Tellurium:</b> Zeigt Mondphasen und beide Finsternisse direkt vorne. Den Raum gut abdunkeln, dann ist die beleuchtete Hälfte klar zu sehen.</li>
<li><b>Typische Fehlvorstellungen:</b> Die Phasen entstehen durch den Erdschatten. Der Mond leuchtet selbst. Bei Neumond ist der Mond „weg“.</li></ul></div>

<div class="box"><h3>Mondphasen {chip(V + 5, V + 6)}</h3><ul>
<li>Faustregel für die Nordhalbkugel: rechts hell heißt zunehmend, links hell heißt abnehmend. Auf der Südhalbkugel ist es umgekehrt.</li>
<li>Der zunehmende Halbmond steht am Nachmittag und Abend am Himmel, der abnehmende am Morgen. Der Vollmond geht beim Sonnenuntergang auf.</li></ul></div>

<div class="box"><h3>Finsternisse {chip(V + 7, V + 8)}</h3><ul>
<li>Die Mondbahn ist um etwa 5° gegen die Erdbahn geneigt. Deshalb gibt es nicht bei jedem Neumond eine Sonnenfinsternis und nicht bei jedem Vollmond eine Mondfinsternis. Im Mondlabor lässt sich der Mond dafür nach oben und unten schieben.</li>
<li>Der Kernschatten des Mondes ist auf der Erde höchstens rund 270 km breit. Eine totale Sonnenfinsternis sieht man deshalb nur in einem schmalen Streifen, eine Mondfinsternis dagegen überall, wo gerade Nacht ist.</li>
<li><b>Blutmond:</b> Die Lufthülle der Erde lenkt etwas Sonnenlicht in den Kernschatten. Dabei bleibt vor allem rotes Licht übrig, wie beim Sonnenuntergang.</li>
<li><b>Sicherheit:</b> Sonnenfinsternis nie ohne Finsternisbrille ansehen, auch keine normale Sonnenbrille. Eine Lochkamera ist ein sicherer Weg. Eine Mondfinsternis kann man ohne Schutz ansehen.</li></ul></div>

<div class="box"><h3>Mondlabor</h3>
<a class="btn" href="Mondlabor Mondphasen und Finsternisse.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Mondbahn mit Regler für den Tag seit Neumond und der Ansicht von der Erde, euer Kugelversuch, Sonnenfinsternis mit schiefer Mondbahn, Mondfinsternis mit Blutmond. Auch für zu Hause.</p></div>
"""

F5_AB = f"""
<div class="box"><h3>Rückseite Versuchsblatt F4: Schattenwurf {chip(1)}</h3>
<a class="btn" href="Materialien/{SW_PDF}">PDF öffnen (Aufgabe und Lösung)</a><a class="btn" href="Materialien/Kern- und Halbschatten W06 – Druck doppelseitig.pdf">Versuchsblatt doppelseitig</a>
<p>Die Schüler haben das Blatt schon (Rückseite des Versuchsblatts F4). Schwierigkeit: ○ leicht; ◐ mittel; ● schwer.</p>
<p>Lücken: a ○ <b>Kernschatten</b>; b ○ <b>Halbschatten</b>; c ◐ <b>Kernschatten</b>, <b>Halbschatten</b>; d ◐ <b>Kernschatten</b>, <b>drei</b>; e ● <b>Halbschatten</b>, <b>Kernschatten</b>, <b>beiden Lichtquellen</b>.</p>
<p>Die Kreise stehen ab dem nächsten PDF-Bau auch auf dem Blatt selbst (nach Freigabe).</p></div>
<div class="box"><h3>Mondlabor</h3>
<a class="btn" href="Mondlabor Mondphasen und Finsternisse.html">Labor öffnen</a>
<p>Dein H5P „Mondphasen Klasse 7“ liegt unter <code>04 Ressourcen/Physik/Mondphasen/H5P/</code> und passt als Wiederholung.</p></div>"""

# ====================================================================== Lochkamera
def ohne_hausaufgabe(h):
    return h.replace("Hausaufgabe: Wir bauen eine Lochkamera", "Wir bauen eine Lochkamera")


LK_ALLTAG = tabellenfolie("Lochkamera im Alltag", [
    ("Lichtflecken unter einem Baum", "runde Flecken", "Jede Lücke im Laub ist eine Lochkamera. Die Flecken sind Bilder der runden Sonne."),
    ("dunkles Zimmer, Loch im Rollladen", "die Straße steht an der Wand auf dem Kopf", "Das Zimmer wirkt wie eine riesige Lochkamera (Camera obscura)."),
    ("Sonnenfinsternis beobachten", "eine kleine Sichel auf dem Papier", "Mit einem Loch im Karton sieht man die Sonne, ohne hineinzuschauen."),
], frage="Warum sind die Flecken unter dem Baum rund, obwohl die Lücken im Laub eckig sind?")

LK = [
    basis(56), ohne_hausaufgabe(basis(57)),
    blatt("Lochkamera W09.pdf", "w09", "Versuchsblatt austeilen · Versuch mit der eigenen Lochkamera"),
    LK_ALLTAG, basis(61), basis(60),
]

LK_MATERIAL = {
    "demo": [("Kerze mit Feuerzeug", "1×", "helles Motiv im abgedunkelten Raum"),
             ("Alufolie und Nadel", "1 Rolle", "für Blenden mit kleinen und großen Löchern"),
             ("Nagel (etwa 1 mm)", "mehrere", "für das Loch im Dosenboden, falls jemand keinen hat")],
    "schueler": [("runde Chipsdose", "1×", "mitgebracht"),
                 ("Transparent- oder Butterbrotpapier", "1 Stück", "mitgebracht"),
                 ("schwarzer Zeichenkarton", "1 Bogen", "etwas größer als der Mantel der Dose"),
                 ("Zirkel, Schere, Lineal, Kleber oder Tesa", "je 1", "aus dem Mäppchen")],
    "hinweis": "Ein paar Chipsdosen und Karton als Reserve bereithalten. Zum Beobachten: helles Fenster oder Kerze im abgedunkelten Raum.",
}

LK_SCHRITTE = [
    ("Einstieg", "Im Lochkameralabor: Warum steht das Bild auf dem Kopf? Dann Folie.", [1]),
    ("Bauen", "Lochkamera nach Anleitung bauen.", [2]),
    ("Versuch", "Mit der eigenen Lochkamera beobachten, Versuchsblatt.", [3]),
    ("Alltag", "Beispiele mündlich, Sicheln auf dem Boden.", [4, 5]),
    ("Rückblick Optik I", "Die fünf Leitfragen in einem Satz.", [6]),
]

LK_HG = f"""
<div class="box"><h3>Die Lochkamera {chip(1)}</h3><ul>
<li>Jeder Punkt des Gegenstands schickt Licht durch das Loch und erzeugt einen kleinen Lichtfleck auf dem Schirm. Alle Flecken zusammen ergeben das Bild.</li>
<li><b>Bildgröße:</b> Bild : Gegenstand = Bildweite : Gegenstandsweite (Strahlensatz). Das kommt in Klasse 7 nur als Je-desto-Satz vor.</li>
<li><b>Schärfe:</b> Ein großes Loch ist wie viele kleine Löcher nebeneinander. Die Bilder überlagern sich, das Bild wird heller, aber unscharf. Gleicher Gedanke wie beim Halbschatten.</li>
<li><b>Typische Fehlvorstellungen:</b> Das Bild wandert als Ganzes durch das Loch. Das Loch dreht das Bild um. Ein größeres Loch macht das Bild größer.</li></ul></div>

<div class="box"><h3>Tipps zum Bau und Versuch {chip(2, 3)}</h3><ul>
<li>Das Loch mit dem Nagel von außen stechen und die Ränder glätten. Ein Stück Alufolie mit Nadelloch vor ein zu großes Loch kleben.</li>
<li>Am besten gegen ein helles Fenster schauen, mit einer Jacke über Kopf und Dose, damit kein Streulicht aufs Papier fällt.</li>
<li>Kerzen nur mit Aufsicht, Haare zurück.</li></ul></div>

<div class="box"><h3>Sicheln unter dem Baum {chip(5)}</h3><ul>
<li>Jede Lücke im Blätterdach wirkt als Lochblende. Weil das Bild auf dem Kopf steht, sind die Sicheln auf dem Boden gegenüber der Sonnensichel um 180° gedreht.</li>
<li>An normalen Tagen sind die Flecken rund oder, bei schräg stehender Sonne, oval.</li></ul></div>

<div class="box"><h3>Rückblick {chip(6)}</h3><ul>
<li>Alle fünf Antworten stecken in einem Satz: Licht breitet sich geradlinig aus und wird an Körpern zurückgeworfen, verschluckt oder durchgelassen.</li>
<li>Gute Gelegenheit, die Labore für die Wiederholung zu Hause zu nennen.</li></ul></div>

<div class="box"><h3>Lochkameralabor</h3>
<a class="btn" href="Lochkameralabor.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a>
<p>Strahlengang von Flammenspitze und Fuß, Regler für Abstände und Lochgröße mit Bildgröße, Unschärfe und Helligkeit, ein, zwei oder viele Löcher, Sonnenbilder unter dem Baum.</p></div>
"""

LK_AB = f"""
<div class="box"><h3>Versuchsblatt Lochkamera {chip(3)}</h3>
<a class="btn" href="Materialien/Lochkamera W09.pdf">PDF öffnen</a><a class="btn" href="Materialien/Lochkamera W09 – 2 auf 1.pdf">Kopiervorlage 2 auf 1</a>
<p>Schwierigkeit: Aufgabe 1 Versuch ○; Aufgabe 2 Lücken ◐ (○ leicht; ◐ mittel; ● schwer).</p>
<p><b>Lösung:</b> Das Bild steht auf dem Kopf. Je weiter das Papier vom Loch entfernt ist, desto größer wird das Bild. Ein kleineres Loch macht das Bild schärfer, aber dunkler.
Lücken: <b>geradlinig</b>, <b>umgekehrtes</b>, <b>größer</b>, <b>schärfer</b>, <b>dunkler</b>.</p></div>
<div class="box"><h3>Lochkameralabor</h3>
<a class="btn" href="Lochkameralabor.html">Labor öffnen</a><a class="btn" href="Optik-Labore.html">Alle Labore</a></div>"""

bau_stunde("Optik – Leitfrage 5 – Stunde.html", "Optik: Warum sieht der Mond nicht immer gleich aus?",
           "Klasse 7c; Physik; Rückseite Schattenwurf, Einschub Jahreszeiten, Leitfrage 5 mit Film und Animationen; Do 12.11.2026",
           ["Nichts drucken.", "Folien und Lösungen: nicht drucken."],
           F5_MATERIAL, F5_SCHRITTE, F5, F5_HG, F5_AB, seitenleiste=True, ohne_leer=True)
bau_stunde("Optik – Lochkamera – Stunde.html", "Optik: Die Lochkamera und Rückblick",
           "Klasse 7c; Physik; Lochkamera, Rückblick Optik I",
           ["Versuchsblatt: Kopiervorlage „2 auf 1“, halbe Klassenstärke drucken und in der Mitte durchschneiden.",
            "Folien und Lösungen: nicht drucken."],
           LK_MATERIAL, LK_SCHRITTE, LK, LK_HG, LK_AB)

# ====================================================================== Export nach iCloud (freigegeben 24.09.2026)
import shutil, sys
if "export" in sys.argv:
    from stunde_vorlage import exportiere, materialliste, MAT, ICL
    VORLAGE = ICL / "F4 Kern- und Halbschatten (W06-07)"
    for ordner, chip_text, titel, mat, ab, ab21, folge, fpdf, shtml, hname, links in (
        (ICL / "F5 Mondphasen und Finsternisse (W08)", "W08", "F5 — Mondphasen und Finsternisse", F5_MATERIAL,
         None, None, F5, "Folien F5.pdf", "Stunde Leitfrage 5.html",   # 11.11.2026: kein Styropor-Versuch, kein Arbeitsblatt
         "Optik – Leitfrage 5 – Stunde.html", {"Mondlabor Mondphasen und Finsternisse.html": "../Labore/Mondlabor Mondphasen und Finsternisse.html"}),
        (ICL / "Lochkamera und Rückblick (W09)", "W09", "Lochkamera und Rückblick Optik I", LK_MATERIAL,
         "Lochkamera W09.pdf", "Lochkamera W09 – 2 auf 1.pdf", LK, "Folien Lochkamera.pdf", "Stunde Lochkamera.html",
         "Optik – Lochkamera – Stunde.html", {"Lochkameralabor.html": "../Labore/Lochkameralabor.html"}),
    ):
        ordner.mkdir(exist_ok=True)
        kurz = "F5" if "F5" in fpdf else "Lochkamera"
        shutil.copy(VORLAGE / "Materialliste.html", ordner / "Materialliste.html")
        (ordner / "Gesamt.html").write_text((VORLAGE / "Gesamt.html").read_text(encoding="utf-8").replace("W06–07", chip_text), encoding="utf-8")
        if ab:
            shutil.copy(MAT / ab, ordner / f"Arbeitsblatt {kurz}.pdf")
            shutil.copy(MAT / ab21, ordner / f"Arbeitsblatt {kurz} – Kopiervorlage 2 auf 1.pdf")
            links = dict(links, **{f"Materialien/{ab}": f"Arbeitsblatt {kurz}.pdf", f"Materialien/{ab21}": f"Arbeitsblatt {kurz} – Kopiervorlage 2 auf 1.pdf"})
        materialliste(ordner, chip_text, titel, mat)
        links = dict(links, **{"Optik-Labore.html": "../Labore/Optik-Labore.html"})
        exportiere(folge, ordner, fpdf, f"Arbeitsblatt {kurz}.pdf" if ab else None, shtml, hname, links)
    for f in ("Optik-Labore.html", "Sehlabor Lichtquellen.html", "Körperlabor Licht trifft auf Körper.html", "Strahlenlabor Lichtausbreitung.html",
              "Schattenlabor Halbschatten.html", "Mondlabor Mondphasen und Finsternisse.html", "Lochkameralabor.html"):
        shutil.copy(f, ICL / "Labore" / f)
    print("Labore kopiert")
