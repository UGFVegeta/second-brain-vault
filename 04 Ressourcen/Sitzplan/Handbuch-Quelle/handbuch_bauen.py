#!/usr/bin/env python3
"""Baut das Handbuch (Handbuch.html) aus Texten und Bildern und trägt es in Sitzplan.html ein.
Aufruf:  python3 handbuch_bauen.py          (baut Handbuch.html und aktualisiert Sitzplan.html)
Bilder neu erzeugen:  bilder_erzeugen.py (Playwright), danach die PNGs als WebP in bilder/ ablegen.
"""
import base64, html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BILDER = os.path.join(HERE, "bilder")

try:
    from PIL import Image
except ImportError:
    Image = None

def img_src(name):
    p = os.path.join(BILDER, name + ".webp")
    b = base64.b64encode(open(p, "rb").read()).decode()
    w = h = 0
    if Image:
        w, h = Image.open(p).size
    return "data:image/webp;base64," + b, w, h

def fig(name, alt, key=None, cap=None, full=False):
    src, w, h = img_src(name)
    style = "" if full or w >= 1250 else f' style="max-width:{round(w/1.5)}px"'
    k = ""
    if key:
        k = '<ol class="key">' + "".join(f"<li>{x}</li>" for x in key) + "</ol>"
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return (f'<figure><button class="zoom" type="button" aria-label="Bild vergrößern: {html.escape(alt)}">'
            f'<img src="{src}" alt="{html.escape(alt)}" width="{w}" height="{h}" loading="lazy"{style}></button>{k}{c}</figure>')

def kbd(s): return f"<kbd>{s}</kbd>"
def go(id_, text): return f'<a href="#{id_}" class="go">{text}</a>'
def note(kind, title, text): return f'<aside class="note {kind}"><b>{title}</b> {text}</aside>'

SECTIONS = []
def sec(id_, group, title, lead, kw, body):
    SECTIONS.append(dict(id=id_, group=group, title=title, lead=lead, kw=kw, body=body))

# ───────────────────────── Los geht's
sec("schnellstart", "Los geht’s", "Schnellstart",
    "In fünf Schritten vom leeren Raum zum ausgedruckten Plan.",
    "anfang erste schritte neu beginnen tutorial kurzanleitung einstieg",
    f"""
<ol class="steps">
  <li><b>Anordnung wählen.</b> Oben auf „Anordnung“ klicken, Plätze eintragen, Form wählen. {go("anordnung","Mehr dazu")}</li>
  <li><b>Klassenliste laden.</b> Links auf „Klassenliste laden“, Datei wählen oder Namen einfügen. {go("klassenliste","Mehr dazu")}</li>
  <li><b>Verteilen.</b> Links unter „Verteilen“ auf „Zufällig“ klicken. {go("verteilen","Mehr dazu")}</li>
  <li><b>Anpassen.</b> Einen Namen auf einen anderen Platz ziehen. Wer dort sitzt, tauscht mit. {go("schueler","Mehr dazu")}</li>
  <li><b>Drucken.</b> Oben rechts auf „Drucken“ oder „PDF“. {go("drucken","Mehr dazu")}</li>
</ol>
{note("tip","Gut zu wissen:","Alles speichert sich von selbst in deinem Browser. Eine Sicherungsdatei solltest du trotzdem anlegen. " + go("sichern","So geht’s"))}
<p>Beim allerersten Start fragt die App, ob du <b>Einfach</b> oder <b>Erweitert</b> arbeiten willst. Das kannst du jederzeit ändern. {go("ansicht","Einfach oder Erweitert")}</p>
""")

sec("aufbau", "Los geht’s", "So ist die App aufgebaut",
    "Seitenleiste, Werkzeugleiste, Raum: wo was steckt.",
    "oberfläche übersicht bedienung leiste seitenleiste toolbar knöpfe icons",
    f"""
{fig("uebersicht","Gesamtansicht der App mit vier markierten Bereichen",
     ["<b>Seitenleiste:</b> Klasse, Regeln, Verteilen, Namen, Farben und alle Schüler ohne Platz.",
      "<b>Werkzeugleiste:</b> Tische hinzufügen, Anordnung, Raum, Drucken, PDF.",
      "<b>Leiste über dem Raum:</b> was beim Ziehen bewegt wird, Varianten, Ansicht, Größe.",
      "<b>Raum:</b> hier sitzen die Schüler. Die Tafel ist unten (Blick vom Pult)."])}
<h3>Werkzeugleiste</h3>
{fig("werkzeugleiste","Werkzeugleiste mit nummerierten Knöpfen",
     ["Einzeltisch hinzufügen","Doppeltisch hinzufügen","Fertige Anordnung wählen","Markierte Tische drehen","Raum und Beschriftung","Drucken","Als PDF speichern","Weitere Befehle: Ansicht, Pläne, Sicherung"])}
<ul>
  <li>Zeig mit der Maus auf einen Knopf, dann erscheint eine kurze Erklärung.</li>
  <li>Die Seitenleiste lässt sich mit dem Knopf ganz links oben ein- und ausklappen. Das gibt dem Raum mehr Platz.</li>
  <li>Auf kleinen Bildschirmen steckt Selteneres im Menü „⋯“.</li>
</ul>
""")

# ───────────────────────── Einrichten
sec("klassenliste", "Einrichten", "Klassenliste laden",
    "Aus CSV, Excel oder per Einfügen. „Nachname, Vorname“ in einer Zelle ist kein Problem.",
    "import csv excel xlsx pdf namen einfügen liste schüler hinzufügen vorname nachname geschlecht doppelte vornamen",
    f"""
<p>Links auf <b>Klassenliste laden</b>. Dann eins von beiden:</p>
<ul>
  <li><b>Datei wählen:</b> CSV oder Excel (.xlsx).</li>
  <li><b>Namen einfügen:</b> aus einer Tabelle, Word oder PDF kopieren und ins große Feld einfügen. Bei einer PDF: Datei öffnen, Namen markieren, kopieren.</li>
</ul>
{fig("import","Dialog Klassenliste laden mit eingefügten Namen und Vorschau",
     ["Datei wählen","Namen einfügen","Übernehmen, sobald die Vorschau stimmt"])}
<h3>Prüfen, bevor du übernimmst</h3>
<ul>
  <li>Die Vorschau zeigt, wie die App die Namen versteht: Vorname, dann <b>Nachname</b> fett.</li>
  <li>Stimmt etwas nicht, ändere oben den <b>Aufbau der Namen</b> oder die Spalten. Falsche Einträge entfernst du mit ×.</li>
  <li>Steht in der Liste eine Spalte mit <b>w</b> und <b>m</b>, übernimmt die App das Geschlecht.</li>
</ul>
<h3>Später ergänzen</h3>
<ul>
  <li>Neue Liste laden und <b>Zur bisherigen Liste hinzufügen</b> wählen, oder links unten einen einzelnen Namen unter „Schüler hinzufügen“ eintippen.</li>
  <li>Gleiche Vornamen unterscheidet die App von selbst durch Buchstaben des Nachnamens, zum Beispiel „Elias B.“ und „Elias L.“.</li>
  <li>Wie die Namen auf den Tischen stehen, stellst du links unter <b>Namen auf den Tischen</b> ein: Vorname, Vorname N. oder voller Name.</li>
</ul>
{note("info","Datenschutz:","Die Namen bleiben auf deinem Rechner. Die App sendet nichts ins Internet.")}
""")

sec("anordnung", "Einrichten", "Anordnung wählen",
    "Reihen, Mittelgang, Einzeltische, U, O oder Gruppen in einem Schritt.",
    "reihen mittelgang einzeltische u-form o-form gruppen tischordnung tische aufstellen plätze gang abstand layout",
    f"""
<p>Oben auf <b>Anordnung</b>, die Zahl der Plätze eintragen und eine Form wählen. Die kleinen Vorschaubilder zeigen sofort, wie es aussieht.</p>
{fig("anordnung","Dialog Anordnung wählen mit Formen und Einstellungen für den Mittelgang",
     ["Anzahl der Plätze","Gewählte Form, hier Mittelgang","Plätze links und rechts vom Gang und Breite des Gangs"])}
<ul>
  <li><b>Reihen:</b> Doppeltische mit zwei Gängen.</li>
  <li><b>Mittelgang:</b> Plätze links und rechts selbst festlegen, zum Beispiel 4 und 4 oder 3 und 4. Links und rechts gelten <b>vom Pult aus gesehen</b>.</li>
  <li><b>Einzeltische:</b> in Reihen, mit wählbarem Abstand (kein Abstand bis 75 cm).</li>
  <li><b>U-Form</b> und <b>O-Form:</b> wahlweise mit Doppel- oder Einzeltischen.</li>
  <li><b>Gruppen zu 4 oder 6:</b> Tische gegenüber.</li>
</ul>
{note("warn","Achtung:","Die neue Anordnung ersetzt alle Schülertische. Wer schon saß, kommt zurück in die Liste „Noch ohne Platz“. Mit Rückgängig (" + kbd("⌘Z") + ") holst du die alte Anordnung zurück.")}
<p>Danach lässt sich jeder Tisch einzeln verschieben. {go("tische","Tische verschieben")}</p>
""")

sec("raum", "Einrichten", "Raum und Beschriftung",
    "Klasse, Raum, Fach, Größe, Fenster und Tür.",
    "klasse raumnummer fach beschriftung kopf plan größe breite tiefe fenster tür rand zoom verkleinern leerer rand",
    f"""
<p>Oben auf <b>Raum</b> oder direkt auf „Klasse 7c“ über dem Plan klicken.</p>
{fig("raum","Dialog Raum und Beschriftung",
     ["Klasse, Raum und Fach: steht oben links auf dem Plan","Breite und Tiefe des Raums","Fenster und Tür (nur wenn sie zum echten Raum passen)"])}
<ul>
  <li>Ein Kästchen im Raster sind <b>25 cm</b>. Ein Doppeltisch ist 150 × 50 cm groß, ein Einzeltisch 75 × 50 cm.</li>
  <li>Das <b>Fach</b> erscheint nur, wenn du „Fach mit anzeigen“ ankreuzt.</li>
  <li><b>Fenster und Tür</b> sind aus, bis du sie einschaltest. Wenn sie nicht genau zum Raum passen, lass sie lieber weg, damit der Ausdruck niemanden verwirrt.</li>
  <li>Links und rechts gelten vom Pult aus gesehen. Änderungen siehst du sofort im Raum.</li>
</ul>
<h3>Plan größer machen</h3>
<p>Ist rund um die Tische viel leerer Platz, erscheint im Raum der blaue Knopf <b>Leeren Rand entfernen</b>. Ein Klick, und die Tische werden größer gezeichnet. Mit <b>− / Auto / +</b> über dem Raum stellst du die Größe von Hand ein.</p>
""")

sec("tische", "Einrichten", "Tische verschieben und drehen",
    "Modus „Tische stellen“: ziehen, drehen, löschen, hinzufügen.",
    "tisch verschieben drehen löschen entfernen raster einrasten markieren mehrere einzeltisch doppeltisch hinzufügen rückgängig",
    f"""
<p>Wähle über dem Raum <b>Tische stellen</b> (Taste {kbd("T")}).</p>
{fig("tische","Raum im Modus Tische stellen mit einem markierten Doppeltisch",
     ["Aktiver Modus","Markierte Tische drehen","Markierte Tische entfernen"])}
<ul>
  <li><b>Verschieben:</b> Tisch anklicken und ziehen. Die Tische rasten im 25-cm-Raster ein, so bleiben die Abstände gleich.</li>
  <li><b>Mehrere markieren:</b> auf freier Fläche einen Rahmen aufziehen.</li>
  <li><b>Drehen:</b> Doppelklick auf den Tisch oder Taste {kbd("R")}.</li>
  <li><b>Entfernen:</b> Taste {kbd("Entf")} oder der Papierkorb oben.</li>
  <li><b>Neu:</b> oben „Einzeltisch“ oder „Doppeltisch“.</li>
  <li><b>Rückgängig:</b> {kbd("⌘Z")}, wiederholen mit {kbd("⇧⌘Z")}.</li>
</ul>
""")

# ───────────────────────── Plätze vergeben
sec("schueler", "Plätze vergeben", "Schüler setzen",
    "Namen auf Plätze ziehen, tauschen, mehrere auf einmal bewegen.",
    "schüler setzen ziehen tauschen lasso gruppe mehrere markieren rahmen modus alt noch ohne platz",
    f"""
<p>Wähle über dem Raum <b>Schüler setzen</b> (Taste {kbd("S")}).</p>
{fig("modus","Umschalter zwischen Tische stellen und Schüler setzen",
     ["Tische verschieben","Namen verschieben","Ansicht: Lehrersicht oder Schülersicht"])}
<ul>
  <li><b>Setzen:</b> Namen aus der Liste „Noch ohne Platz“ links auf einen Platz ziehen.</li>
  <li><b>Tauschen:</b> einen Namen auf einen besetzten Platz ziehen, dann tauschen die beiden.</li>
  <li><b>Mehrere auf einmal:</b> mit gedrückter Maustaste einen Rahmen um die Namen ziehen. Die Gruppe lässt sich dann am Stück verschieben. Wer am Ziel sitzt, tauscht mit.</li>
  <li><b>Kurz der andere Modus:</b> beim Ziehen die Taste {kbd("⌥")} (Windows: {kbd("Alt")}) halten.</li>
</ul>
{fig("lasso","Rahmen um vier Namen aufgezogen",cap="Ein Rahmen markiert mehrere Namen.")}
{note("tip","Bewegt sich nichts?","Schau, welcher Modus über dem Raum hervorgehoben ist. Tische lassen sich nur in „Tische stellen“ ziehen, Namen nur in „Schüler setzen“.")}
""")

sec("verteilen", "Plätze vergeben", "Verteilen",
    "Zufällig, nur den Rest, alphabetisch oder alles abräumen.",
    "zufällig zufall rest a bis z alphabetisch abräumen verteilen sitzordnung losen mit wünschen festhalten",
    f"""
<p>In der Seitenleiste unter <b>Verteilen</b>:</p>
{fig("verteilen","Knöpfe im Bereich Verteilen",
     ["<b>Mit Wünschen verteilen</b> (nur im Erweitert-Modus)","<b>Zufällig:</b> alle neu und zufällig setzen","<b>Rest:</b> nur wer noch keinen Platz hat","<b>A bis Z:</b> alphabetisch von vorne nach hinten","<b>Abräumen:</b> alle zurück in die Liste"])}
<ul>
  <li><b>Festgehaltene Schüler</b> bleiben beim Zufälligen sitzen. Auch deine Regeln gelten immer. {go("regeln","Regeln")}</li>
  <li><b>Mit Wünschen verteilen</b> setzt zufällig und erfüllt dabei möglichst viele Wünsche. Zuerst bekommt jeder einen Wunsch, danach wird weiter verteilt. {go("wuensche","Wünsche")}</li>
  <li>Nicht zufrieden? Ein neuer Klick mischt neu. Mit dem Hinweis „Rückgängig“ unten oder {kbd("⌘Z")} kommst du zum vorigen Stand zurück.</li>
</ul>
""")

sec("farben", "Plätze vergeben", "Mädchen, Jungen und Farben",
    "Namen farbig anzeigen und das Geschlecht zuordnen.",
    "farbe farben mädchen jungen geschlecht zuordnen w m rosa blau farbig regeln",
    f"""
{fig("farben","Bereich Farben in der Seitenleiste",
     ["Namen nach Geschlecht einfärben","Farben ändern, „Standard“ stellt die Voreinstellung wieder her","Geschlecht zuordnen"])}
<ul>
  <li>Die Farben sind dezent und lassen sich frei ändern.</li>
  <li>Das Geschlecht braucht die App für die Farben und für die Klassenregeln. {go("regeln","Regeln")}</li>
  <li>Es kommt aus der Klassenliste (Spalte mit w und m) oder du setzt es selbst:</li>
</ul>
<p>Links auf <b>Mädchen und Jungen zuordnen</b>.</p>
{fig("geschlecht","Dialog Mädchen und Jungen zuordnen mit zwei Namenslisten")}
<p>Pro Name einmal klicken. Schneller mit der Tastatur: einen Namen anklicken und {kbd("W")} oder {kbd("M")} drücken. Die App springt zum nächsten.</p>
""")

# ───────────────────────── Erweitert
sec("wuensche", "Erweitert", "Wünsche der Schüler und deine Regeln",
    "Wer will neben wem sitzen? Und was bestimmst du?",
    "wünsche wunsch neben reihe nie neben sitzt neben muss in reihe platz festhalten lehrerregel vorrang fair punkt grün rot schloss",
    f"""
<p>Klicke in der Seitenleiste auf <b>Wünsche eintragen</b> oder im Plan auf einen <b>Namen</b>.</p>
{fig("wuensche","Dialog Wünsche und Regeln",
     ["<b>Schülerliste:</b> Name wählen. Die Zahl zeigt, wie viele Wünsche er hat.","<b>Wünsche des Schülers:</b> neben wem und in welcher Reihe er sitzen möchte.","<b>Deine Regeln:</b> lila Kasten, gehen immer vor."])}
<h3>Wünsche des Schülers</h3>
<ul>
  <li><b>Möchte neben:</b> Namen anklicken. Blau umrandet sind die, die neben diesen Schüler wollen.</li>
  <li><b>Reihe:</b> Reihe 1 ist an der Tafel. Mehrere gewählt heißt: eine davon.</li>
  <li><b>Neben</b> heißt direkt links oder rechts in derselben Reihe, auch am Nachbartisch. Vorne und hinten zählt nicht.</li>
</ul>
<h3>Deine Regeln</h3>
<ul>
  <li><b>Sitzt neben / nie neben:</b> Namen anklicken. Ein Klick = sitzt neben, zweiter Klick = nie neben, dritter Klick = keine Regel.</li>
  <li><b>Muss sitzen in:</b> zum Beispiel vorne wegen der Tafel.</li>
  <li><b>Platz festhalten:</b> der Schüler bleibt beim Verteilen sitzen. Erst auf einen Platz ziehen, dann das Häkchen setzen.</li>
  <li>Deine Regeln gehen <b>immer</b> vor. Widerspricht ein Wunsch einer Regel, wird er nicht erfüllt und die App weist dich darauf hin.</li>
</ul>
<p>Die Taste {kbd("W")} oder {kbd("M")} setzt im Dialog das Geschlecht und springt zum nächsten Namen.</p>
<h3>Die Punkte im Plan</h3>
{fig("wuensche-plan","Plan mit grünen Punkten an erfüllten Wünschen")}
<ul>
  <li><b>Grüner Punkt</b> oben rechts am Namen: ein Wunsch ist erfüllt. <b>Roter Ring:</b> noch offen.</li>
  <li><b>Schloss</b> links oben: Platz ist festgehalten.</li>
  <li>Die Seitenleiste zeigt, wie viele Schüler mindestens einen Wunsch erfüllt bekommen haben.</li>
  <li>Auf dem Ausdruck und vor der Klasse sind diese Markierungen ausgeblendet. {go("zeigen","Vor der Klasse zeigen")}</li>
</ul>
{note("info","Datenschutz:","Die App wertet die Wünsche selbst aus, ganz ohne KI und Internet. Trag nur ein, was du schulintern darfst.")}
""")

sec("regeln", "Erweitert", "Regeln für die ganze Klasse",
    "Keine reine Mädchen- oder Jungenreihe, niemand allein, gemischte Doppeltische.",
    "klassenregeln mix mädchen jungen reihe allein gemischt doppeltisch regeln einhalten",
    f"""
<p>In der Seitenleiste unter <b>Deine Regeln</b>:</p>
{fig("regeln","Bereiche Wünsche der Schüler und Deine Regeln",
     ["Übersicht: wie viele Wünsche erfüllt sind","Die drei Klassenregeln zum Ankreuzen"])}
<ul>
  <li><b>Keine Reihe nur mit Mädchen oder nur mit Jungen.</b></li>
  <li><b>Niemand ist das einzige Mädchen oder der einzige Junge seiner Reihe.</b></li>
  <li><b>An jedem Doppeltisch ein Mädchen und ein Junge.</b></li>
</ul>
<p>Die Regeln brauchen das Geschlecht. {go("farben","So ordnest du es zu")} Unter den Kästchen steht, ob alle Regeln eingehalten sind. Wenn nicht, nennt die App die Stellen.</p>
<p>Regeln gelten für Zufällig, Rest und „Mit Wünschen verteilen“ und gehen den Wünschen der Schüler vor.</p>
""")

sec("varianten", "Erweitert", "Varianten, Verlauf und Vergleich",
    "Mehrere Entwürfe pro Klasse und der Blick auf alte Stände.",
    "varianten variante a b c verlauf fertig vergleich vergleichen alter stand wechseln kopie versionen history",
    f"""
{fig("vergleich","Plan mit Varianten A und B und dem Vergleichsfeld rechts",
     ["Varianten: A, B, … Mit + legst du eine Kopie an.","Knopf „Vergleich“","Vergleichsfeld mit Miniplan"])}
<h3>Varianten</h3>
<ul>
  <li>Mit <b>+</b> neben „Variante“ entsteht eine <b>Kopie</b> des aktuellen Plans. Dort kannst du umbauen oder neu verteilen, die anderen Varianten bleiben, wie sie sind.</li>
  <li>Doppelklick auf den Reiter: umbenennen. Das × am aktiven Reiter löscht die Variante. Bis zu 8 Varianten pro Klasse.</li>
  <li>Wünsche und Regeln gelten für alle Varianten gemeinsam.</li>
</ul>
<h3>Verlauf</h3>
<ul>
  <li><b>Fertig</b> speichert den Stand mit Datum. Das passiert auch automatisch, wenn du druckst oder ein PDF erzeugst. Die App merkt sich bis zu 30 Stände.</li>
</ul>
<h3>Vergleich</h3>
<ul>
  <li><b>Vergleich</b> öffnet rechts ein Feld mit einem Miniplan der anderen Variante oder eines alten Standes. Die Zeile darunter sagt, wie viele Schüler woanders sitzen.</li>
  <li>Unten wechselst du zu der Variante („Zu Variante … wechseln“) oder übernimmst einen alten Stand als neue Variante. Alte Stände lassen sich aus dem Verlauf löschen.</li>
</ul>
""")

# ───────────────────────── Zeigen und sichern
sec("zeigen", "Zeigen und sichern", "Vor der Klasse zeigen",
    "Wünsche ausblenden, Lehrer- oder Schülersicht, Seitenleiste einklappen.",
    "beamer klasse zeigen ausblenden wünsche verstecken lehrersicht schülersicht ansicht tafel oben unten seitenleiste einklappen diskret",
    f"""
{fig("ausblenden","Plan mit eingeschalteter Funktion Wünsche ausblenden",
     ["„Wünsche ausblenden“ ist eingeschaltet"])}
<ul>
  <li><b>Wünsche ausblenden</b> versteckt alle Punkte und Schlösser, die Abschnitte zu Wünschen und Regeln und den Wünsche-Dialog. Die Seitenleiste klappt dabei ein. Perfekt für den Beamer.</li>
  <li>Zum Zurückschalten noch einmal auf den Knopf klicken.</li>
</ul>
<h3>Lehrersicht und Schülersicht</h3>
{fig("sicht","Plan in Schülersicht mit der Tafel oben",
     ["Lehrersicht: Tafel unten, so schaust du vom Pult in die Klasse","Schülersicht: Tafel oben, so sieht die Klasse den Raum"])}
<p>Voreingestellt ist die <b>Lehrersicht</b>, weil der Ausdruck meist vorne am Pult hängt. Auf dem Ausdruck steht die Blickrichtung.</p>
""")

sec("drucken", "Zeigen und sichern", "Drucken und PDF",
    "Ausdruck auf A4 quer oder PDF zum Weitergeben, zum Beispiel über iServ.",
    "drucken druck pdf iserv speichern a4 ausdruck dateipfad pfad kopfzeile fußzeile schuldrucker drucker",
    f"""
{fig("druck","Vorschau des Ausdrucks auf A4 quer")}
<ul>
  <li><b>Drucken</b> (oben rechts oder {kbd("⌘P")} bzw. {kbd("Strg+P")}) druckt den Plan auf <b>A4 quer</b>.</li>
  <li><b>PDF</b> speichert den Plan als PDF-Datei. Die kannst du verschicken, zum Beispiel über iServ, und überall ausdrucken. In Chrome und Edge wählst du den Speicherort selbst, in Safari und Firefox landet die Datei im Download-Ordner.</li>
  <li>Auf dem Blatt stehen Klasse, Raum, Datum und die Blickrichtung. Wünsche, Punkte und Variantenname erscheinen <b>nicht</b>.</li>
  <li>Beim Drucken und beim PDF-Erzeugen landet der Stand im Verlauf.</li>
</ul>
{note("info","Kein Dateipfad auf dem Blatt:","In Chrome druckt die App weder Pfad noch Datum noch Titel in den Seitenrand. Falls ein anderer Browser doch eine Kopf- oder Fußzeile druckt, schalte im Druckfenster „Kopf- und Fußzeilen“ aus oder nimm den PDF-Knopf.")}
""")

sec("sichern", "Zeigen und sichern", "Pläne sichern und verwalten",
    "Sicherungsdatei anlegen und öffnen, mehrere Pläne, Umzug auf einen anderen Rechner.",
    "sichern sicherung backup datei speichern öffnen json umbenennen kopie löschen neuer plan mehrere klassen umzug speicherort erinnerung datenschutz",
    f"""
{fig("menue","Menü Weitere Befehle mit Sicherung und Ansicht",
     ["Alle Sitzpläne als Datei sichern","Gesicherte Sitzpläne öffnen","Ansicht Einfach oder Erweitert"])}
<h3>Wo liegen meine Pläne?</h3>
<p>Die Pläne speichern sich automatisch <b>in deinem Browser</b> auf diesem Rechner. Das passiert ohne Internet. Löschst du die Browserdaten oder wechselst Browser oder Rechner, sind sie dort nicht da.</p>
<h3>Sicherungsdatei</h3>
<ul>
  <li>Menü <b>⋯</b> → <b>Alle Sitzpläne als Datei sichern</b>. Chrome und Edge fragen, wohin die Datei soll, und merken sich den Ordner. Safari und Firefox legen sie im Download-Ordner ab.</li>
  <li>Zurückholen oder auf einem anderen Rechner öffnen: <b>Gesicherte Sitzpläne öffnen …</b></li>
  <li>Nach 14 Tagen ohne Sicherung erinnert dich die App.</li>
</ul>
{note("warn","Achtung:","Die Sicherungsdatei enthält die Schülernamen. Leg sie nur an einem Ort ab, auf den nur du Zugriff hast, und verschicke sie nicht ungeschützt.")}
<h3>Mehrere Pläne</h3>
<ul>
  <li>Oben links wählst du den Plan aus, mit <b>+</b> legst du einen neuen an, zum Beispiel pro Klasse.</li>
  <li>Im Menü <b>⋯</b>: umbenennen, Kopie anlegen, löschen.</li>
</ul>
""")

sec("ansicht", "Zeigen und sichern", "Einfach oder Erweitert",
    "Zwei Ansichten: schlicht oder mit Wünschen, Regeln und Varianten.",
    "einfach erweitert ansicht modus schlicht wünsche regeln varianten umschalten kollegen willkommen",
    f"""
{fig("willkommen","Willkommensdialog mit den Kacheln Einfach und Erweitert",["Einfach","Erweitert"])}
<ul>
  <li><b>Einfach:</b> Tische aufstellen, Klassenliste laden, Schüler ziehen oder zufällig verteilen, drucken, Farben. Mehr nicht.</li>
  <li><b>Erweitert:</b> zusätzlich Schülerwünsche, eigene Regeln, Varianten, Verlauf und Vergleich.</li>
</ul>
<p>Umschalten: Menü <b>⋯</b> → <b>Ansicht</b>. Deine Pläne bleiben dabei erhalten. Regeln, die du schon eingestellt hast, gelten auch im Einfach-Modus weiter.</p>
{fig("einfach","Die App in der Ansicht Einfach")}
""")

# ───────────────────────── Hilfe
sec("tasten", "Hilfe", "Tastenkürzel und Tipps",
    "Alle Kürzel auf einen Blick.",
    "tastenkürzel tastatur kürzel shortcut taste befehl alt strg cmd",
    f"""
<table class="keys">
  <thead><tr><th>Taste</th><th>Was passiert</th></tr></thead>
  <tbody>
    <tr><td>{kbd("T")}</td><td>Modus „Tische stellen“</td></tr>
    <tr><td>{kbd("S")}</td><td>Modus „Schüler setzen“</td></tr>
    <tr><td>{kbd("R")} oder Doppelklick</td><td>Markierte Tische drehen</td></tr>
    <tr><td>{kbd("Entf")}</td><td>Markierte Tische entfernen</td></tr>
    <tr><td>{kbd("⌘Z")} / {kbd("⇧⌘Z")}</td><td>Rückgängig / Wiederholen (Windows: {kbd("Strg+Z")} / {kbd("Strg+Y")})</td></tr>
    <tr><td>{kbd("⌘P")}</td><td>Drucken (Windows: {kbd("Strg+P")})</td></tr>
    <tr><td>{kbd("⌥")} beim Ziehen</td><td>Kurz der andere Modus (Windows: {kbd("Alt")})</td></tr>
    <tr><td>{kbd("W")} / {kbd("M")}</td><td>In den Dialogen: Mädchen / Junge setzen und weiter zum nächsten Namen</td></tr>
  </tbody>
</table>
<p>Dieselben Tipps stehen in der App links unten unter <b>Tipps und Tastenkürzel</b>.</p>
{fig("tipps","Aufgeklappte Tipps in der Seitenleiste")}
""")

FAQ = [
 ("Ich kann keine Namen ziehen.", "Schau über dem Raum, welcher Modus aktiv ist. Namen bewegst du in „Schüler setzen“ (Taste S). Mit gedrückter Taste ⌥ (Windows: Alt) gilt beim Ziehen kurz der andere Modus."),
 ("Ich kann keine Tische verschieben.", "Wähle „Tische stellen“ (Taste T)."),
 ("Die Namen wurden falsch eingelesen.", "Im Dialog „Klassenliste laden“ oben den „Aufbau der Namen“ und die Spalten umstellen. Die Vorschau zeigt sofort, was sich ändert."),
 ("Der Plan ist klein und rundherum ist viel Rand.", "Auf „Leeren Rand entfernen“ oder „Rand verkleinern“ klicken. Mit + über dem Raum wird alles größer."),
 ("Ich habe etwas falsch gemacht.", "Rückgängig mit ⌘Z (Windows: Strg+Z) oder dem Hinweis „Rückgängig“ unten. Im Erweitert-Modus gibt es außerdem den Verlauf unter „Vergleich“."),
 ("Meine Pläne sind weg.", "Die Pläne liegen in dem Browser, in dem du sie angelegt hast. In einem anderen Browser oder auf einem anderen Rechner siehst du sie nicht. Öffne dort deine Sicherungsdatei: Menü ⋯ → „Gesicherte Sitzpläne öffnen“."),
 ("Auf dem Ausdruck steht ein Dateipfad.", "In Chrome kommt der Pfad nicht auf das Blatt. Falls ein anderer Browser doch eine Kopf- oder Fußzeile druckt, schalte im Druckfenster „Kopf- und Fußzeilen“ aus oder nimm den PDF-Knopf."),
 ("Werden Namen ins Internet geschickt?", "Nein. Die App ist eine einzelne Datei, läuft auf deinem Rechner und braucht kein Internet. Es gibt keinen Server und keine KI."),
 ("Welchen Browser soll ich nehmen?", "Chrome oder Edge. Dort wählst du den Speicherort für Sicherung und PDF selbst. In Safari und Firefox funktioniert die App auch, Dateien landen aber im Download-Ordner."),
 ("Wie bekomme ich die App auf einen anderen Rechner?", "Die Datei Sitzplan.html kopieren und dort im Browser öffnen. Deine Pläne nimmst du mit der Sicherungsdatei mit."),
]
faq = "".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in FAQ)
sec("fragen", "Hilfe", "Häufige Fragen",
    "Wenn etwas nicht klappt, steht die Antwort oft hier.",
    "problem fehler hilfe faq geht nicht frage antwort funktioniert nicht browser internet daten weg",
    faq)

GROUPS = []
for s in SECTIONS:
    if s["group"] not in GROUPS: GROUPS.append(s["group"])

nav = ""
for g in GROUPS:
    nav += f'<div class="navgroup"><div class="navlabel">{html.escape(g)}</div>'
    for s in SECTIONS:
        if s["group"] == g:
            nav += f'<a href="#{s["id"]}" data-id="{s["id"]}" class="navitem"><span>{html.escape(s["title"])}</span><em class="cnt"></em></a>'
    nav += "</div>"

tiles = ""
for g in GROUPS:
    tiles += f'<h2 class="tgroup">{html.escape(g)}</h2><div class="tiles">'
    for s in SECTIONS:
        if s["group"] == g:
            tiles += f'<a class="tile" href="#{s["id"]}"><b>{html.escape(s["title"])}</b><span>{html.escape(s["lead"])}</span></a>'
    tiles += "</div>"

articles = ""
for i, s in enumerate(SECTIONS):
    prev = SECTIONS[i-1] if i else None
    nxt = SECTIONS[i+1] if i < len(SECTIONS)-1 else None
    pn = '<nav class="pn">'
    pn += (f'<a href="#{prev["id"]}" class="prev"><small>Zurück</small>{html.escape(prev["title"])}</a>' if prev else '<span></span>')
    pn += (f'<a href="#{nxt["id"]}" class="next"><small>Weiter</small>{html.escape(nxt["title"])}</a>' if nxt else '<span></span>')
    pn += '</nav>'
    articles += (f'<article class="page sec" id="{s["id"]}" data-title="{html.escape(s["title"])}" data-group="{html.escape(s["group"])}" '
                 f'data-kw="{html.escape(s["kw"])}" hidden><div class="crumb">{html.escape(s["group"])}</div>'
                 f'<h1>{html.escape(s["title"])}</h1><p class="lead">{html.escape(s["lead"])}</p>{s["body"]}{pn}</article>')

TEMPLATE = open(os.path.join(HERE, "handbuch_vorlage.html"), encoding="utf-8").read()
out = (TEMPLATE.replace("{{NAV}}", nav).replace("{{TILES}}", tiles).replace("{{ARTICLES}}", articles))
open(os.path.join(ROOT, "Handbuch.html"), "w", encoding="utf-8").write(out)
print("Handbuch.html:", round(len(out)/1024), "KB,", len(SECTIONS), "Seiten")

# In die App eintragen (zwischen den Markierungen)
app_p = os.path.join(ROOT, "Sitzplan.html")
app = open(app_p, encoding="utf-8").read()
payload = out.replace("</script", "<\\/script")
block = "<!--HANDBUCH-START-->\n<script type=\"text/plain\" id=\"manualSrc\">" + payload + "</script>\n<!--HANDBUCH-END-->"
if "<!--HANDBUCH-START-->" in app:
    app = re.sub(r"<!--HANDBUCH-START-->.*?<!--HANDBUCH-END-->", lambda m: block, app, flags=re.S)
else:
    app = app.replace("</body>", block + "\n</body>")
open(app_p, "w", encoding="utf-8").write(app)
print("Sitzplan.html:", round(len(app)/1024), "KB")
