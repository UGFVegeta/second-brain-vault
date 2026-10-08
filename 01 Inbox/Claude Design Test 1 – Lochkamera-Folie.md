---
tags: [inbox, physik, optik, claude-design, test]
date: 2026-10-08
status: aktiv
---

# Claude Design Test 1: Lochkamera-Folie

Zweck: Prüfen, ob Claude Design (jetzt in jedem Claude-Chat, auf allen Tarifen) eine Physik-Folie in meinem Folienstil besser oder zumindest gleich gut hinbekommt wie mein HTML-System. Vergleichsobjekt ist die Lochkamera-Folie in `04 Ressourcen/Physik/Optik/Optik – Lochkamera – Stunde.html` (Tab Folien, erste Folie).

Ablauf: Prompt unten in einen neuen Claude-Chat einfügen, Design aktivieren. Danach Ergebnis mit meiner Folie vergleichen (Kriterien weiter unten). Im Chat keine Namen oder Daten von Schülern verwenden.

## Prompt zum Einfügen

```
Gestalte eine Unterrichtsfolie für Physik Klasse 7, Thema Optik, Lochkamera. Die Folie läuft im Browser am Beamer. Sie soll sich animieren lassen.

Format und Stil
- 16:9, weißer Hintergrund, sehr helles Karo-Raster als Zeichenhilfe.
- Schwarzer Kopfbalken mit kleiner Kopfzeile "Optik · Leitfrage 5", darunter der Titel groß und linksbündig.
- Fußzeile: "Physik 7c · Optik · Lochkamera · 1".
- Schrift serifenlos, Fachbegriffe in einer Monospace-Schrift. Keine weichen Schatten, keine Verläufe außer dem Leuchten der Flamme.
- Viel Platz, wenig Text. Die Zeichnung ist die Hauptsache.

Titel (bleibt eine Frage, keine Aussage)
"Warum steht das Bild auf dem Kopf?"

Zeichnung (links nach rechts, exakt maßstäblich)
- Links eine Kerze mit leuchtender Flamme (Beschriftung "Gegenstand").
- In der Mitte eine Wand mit kleiner Lochblende (Beschriftung "Lochblende").
- Rechts ein Schirm (Beschriftung "Schirm"). Auf dem Schirm steht die Kerze umgekehrt, kleiner als der Gegenstand, so wie es der Strahlensatz ergibt.
- Zwei Lichtwege: von der Flammenspitze in Orange, vom Kerzenfuß in Cyan. Beide laufen gerade durch das Loch und kreuzen sich dort. Die Spitze landet unten auf dem Schirm, der Fuß oben.
- Eine gestrichelte optische Achse durch das Loch.

Animation
- Lichtpulse laufen als kleine Punkte von der Kerze durch das Loch zum Schirm, in der Farbe des jeweiligen Lichtwegs, als Schleife.
- Alles ist Code (HTML, CSS, SVG, JavaScript), kein Video. Ich will später Abstände und Farben ändern können.
- Bei "Bewegung reduzieren" im System sollen die Pulse aus sein. Im Ausdruck soll nur das Standbild stehen.

Zusätzlich
- Liefere die Folie bitte auch als leere Zwillingsfolie: gleiche Seite, gleiches Karo, gleicher Titel, aber ohne Zeichnung. Auf der leeren Seite zeichne ich vor, die Klasse zeichnet mit.
- Ein Regler "Abstand Kerze bis Loch", der das Bild auf dem Schirm live größer oder kleiner macht. Bildgröße nach B = G · b : g.

Gib mir am Ende den HTML-Code in einer Datei, die offline läuft.
```

## Vergleichskriterien (nach dem Test ankreuzen)

- [ ] Stil stimmt: weißer Grund, schwarzer Balken, Fußzeile, Karo
- [ ] Zeichnung ist physikalisch richtig (Strahlen gerade, Bild umgekehrt, Größe stimmt)
- [ ] Animation läuft ruhig und lenkt nicht ab
- [ ] Leere Zwillingsfolie passt
- [ ] Code ist lesbar und lässt sich von mir oder Claude Code weiter anpassen
- [ ] Offline lauffähig, keine fremden Einbindungen
- [ ] Verbrauch vom Wochenkontingent: Wert vor und nach dem Test notieren

Vorher: ____ %   Nachher: ____ %

## Entscheidung nach dem Test

Besser als mein System: Design für neue Folien einplanen. Gleich gut: eher nicht wechseln, weil mein System schon Tafelbild-Logik, Stunden-Tabs und iCloud-Export hat. Schlechter: bei meinem System bleiben.

## Ergebnis abgespeckter Test (08.10.2026)

Gesendet: Folie mit Titel, Zeichnung und Lichtpulsen, ohne Regler und ohne leere Zwillingsfolie. Modell Sonnet 5.5, Mittel, in claude.ai unter Design, Chat „Lochkamera Unterrichtsfolie“.

- Dauer: etwa 5 Minuten bis zum fertigen Artefakt.
- Verbrauch: Sitzung 15 % auf 20 %, Woche 64 % auf 65 %. Für diese eine Folie also rund 1 % der Woche.
- Zeichnung physikalisch richtig: Strahlen kreuzen sich im Loch, Bild umgekehrt, Spitze unten, Maßstab 0,75 (500 px zu 375 px).
- Stil: schwarzer Balken, Frage als Titel, Fußzeile wie verlangt. Das Karo ist kaum sichtbar.
- Ergänzt ohne Auftrag: Beschriftung „Spitze“, „Fuß“ und „optische Achse“.
- Animation im Browser noch nicht beurteilt, Claude hat sie selbst nicht getestet.
- Beim ersten Öffnen zeigte die Fläche „no artboards“, erst nach Neuladen der Seite war die Folie da.

Voller Test (mit Regler und leerer Zwillingsfolie): Freitagabend 09.10., vor dem Reset am Samstag 07:00.
