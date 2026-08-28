---
tags: [projekt, weinstadtcross, website]
status: pausiert
date: 2026-08-08
---

# WeinstadtCross Website ohne WordPress

Ablösung von WordPress und Betheme durch eine selbst gebaute, statische Website. Nachfolgeprojekt von [[WeinstadtCross Website Relaunch]].

## Entscheidung

**Ja, aber nicht vor dem Wettkampf im November 2026.** Die bestehende Seite bleibt für diese Saison unverändert, sie ist inzwischen in gutem Zustand und die Suchmaschinen haben sich gerade erst auf die neuen Angaben eingestellt. Ein Umzug kurz vor einer Deutschen Meisterschaft wäre der schlechteste denkbare Zeitpunkt.

**Umsetzung ab Dezember 2026 / Januar 2027.** Dann ist ein volles Jahr Puffer bis zum nächsten Wettkampf, die alte Seite bleibt bis zum Umschalten online.

## Warum

Der eigentliche Beleg kam aus dem Relaunch selbst. Zeitplan, Streckentabelle und das Zeitplan-PDF entstehen längst automatisch aus `Zeitplan_2026.xlsx`. Der gesamte Aufwand danach war reine Verpackung: Blöcke in die Zwischenablage legen, in den BeBuilder einfügen, Umlaute retten, prüfen ob das `<style>` gefiltert wurde, Bilder mit identischem Dateinamen ersetzen, ins richtige Yoast-Feld treffen. Auf einer selbst gebauten Seite entfällt dieser Teil ersatzlos, weil Claude die Datei direkt schreibt statt sie zum Einfügen zu übergeben.

Dazu: deutlich schneller (Betheme lädt viel mit, an das man nicht herankommt), volle Kontrolle über Metadaten und Schema, kein Plugin- und Theme-Update-Zyklus, und die offenen Datenschutzpunkte (Google Analytics, Google Fonts, YouTube ohne Einwilligung) lassen sich beim Neubau gleich mit erledigen.

## Der Einwand, der sich erledigt hat

Ursprüngliche Sorge war die Redaktion: Wer ändert etwas, wenn Oskar nicht verfügbar ist? Auf einer statischen Seite kann das zunächst nur er zusammen mit Claude.

**Oskar am 08.08.2026: Er pflegt die Homepage ohnehin allein, das war noch nie ein Problem.** Damit entfällt der Hauptgrund für ein Redaktionssystem. Eine Eingabemaske für Dritte muss nicht mitgebaut werden. Falls sich das später ändert, ist sie nachrüstbar.

## Aufbau

Alles, was aus Daten entsteht, wird generiert: Zeitplan und Strecken aus der Excel, Prämien und Ausschreibung aus einer Quelldatei. Alles Wiederkehrende steht genau einmal.

**Sponsoren an einer einzigen Stelle.** Das war Oskars ausdrücklicher Wunsch, weil ihn das Austauschen von Einzelbildern auf jeder Seite genervt hat. Im Entwurf ist das umgesetzt: eine Liste im Quelltext mit Name, Logo und Stufe, daraus entstehen automatisch die klebende Spalte rechts und die Sponsorenwand unten. Ein neuer Sponsor wird einmal eingetragen und erscheint überall.

Die Sponsorenspalte rechts neben dem Inhalt soll erhalten bleiben, das Muster gibt es heute schon auf der Streckenseite.

**Das gelbe Veranstaltungslogo ist Oskars Markenzeichen und gehört in die Kopfzeile, nicht zu den Sponsoren.** Es zeigt Maskottchen, Schriftzug, SG-Zeichen und Datum. Im ersten Entwurf war es fälschlich als Sponsorenlogo einsortiert, weil es nur am Dateinamen erkannt wurde. Jetzt sitzt es in der klebenden Kopfzeile und ist damit auf jeder Seite dauerhaft sichtbar. Da es die Jahreszahl enthält, muss es einmal im Jahr getauscht werden, künftig aber nur noch an dieser einen Stelle.

Titelsponsor ist die **Volksbank Stuttgart eG** (eigenes Logo, lag im Entwurf zunächst unter Partner, steht jetzt an erster Stelle der Hauptsponsoren).

## Stand

Im Homepage-Ordner liegen **zwei** Entwurfsseiten, `Neue Startseite – Entwurf.html` (33 KB) und `Neue Strecken – Entwurf.html` (31 KB). Beide werden von `baue_seiten.py` erzeugt, aus **einer** Vorlage und **einer** Sponsorenliste. Bausteine daneben: `entwurf.css`, `inhalt_start.html`, `inhalt_strecken.html`.

Damit ist der Kernpunkt nicht mehr behauptet, sondern vorgeführt: Kopfzeile, Menü, Sponsorenspalte und Fußbereich stehen genau einmal im Skript. Die Sponsoren werden **beim Bauen** eingesetzt, nicht im Browser, deshalb braucht die Streckenseite überhaupt kein Javascript (die Startseite nur für den Countdown).

Mit Chrome gerendert und geprüft: 6 Logos in der Spalte, 28 in der Wand über drei Gruppen, 3 Klappmenüs mit 11 Unterpunkten, aktiver Menüpunkt wird automatisch markiert, keine Platzhalter übrig.

**Alle 19 Seiten fertig** (Stand 08.08.2026), also jede Seite, die im Menü erreichbar ist, plus Impressum und Datenschutz im Fußbereich. Alle aus `baue_seiten.py`. Sie liegen im Ordner `WeinstadtCross Entwurf/` und gebündelt als `WeinstadtCross-Entwurf.zip` (212 KB) zum Weiterleiten. Geprüft: keine toten Links, keine Platzhalter im Quelltext, aktiver Menüpunkt auf jeder Seite markiert.

Inhalte wurden von der Live-Seite importiert (`importiere_rest.py`), nicht neu formuliert. Prämien, Anreise und Übernachten übernehmen die bestehenden Bausteine samt ihrem CSS, das inline auf den Live-Seiten lag.

⚠️ **Sieben Seiten sind auch heute schon praktisch leer** und im Entwurf deshalb ehrliche Platzhalter: Anmeldung, Teilnehmer, Ergebnisse, Gesamtwertung Cross Cup, Kooperationspartner sowie Ausschreibung und Ausschreibung Schulen (dort nur PDF und Bild). Das ist kein Mangel des Entwurfs, sondern der Stand im August.

**Zwei Funde auf der bestehenden Seite:**
- Die Sponsorenseite enthält eine **kaputte YouTube-Einbettung**: `youtube.com/embed/https://youtu.be/czxGkGwoIdU?...`, also eine vollständige URL hinter `/embed/`. Das Video kann so nicht laufen.
- Die Anmeldeseite trägt noch die Überschrift „Anmeldung WeinstadtCross 2025".

**Fallstrick beim Übernehmen von CSS:** Die Prämientabelle war zunächst unsichtbar, weiße Schrift auf weißem Grund. Ursache waren Farbvariablen (`--wc-ink`, `--wc-gelb`, `--wc-line`, `--wc-chalk`) aus TEIL 1 der Customizer-Datei, die beim Herauslösen der Regeln fehlten. Sie sind jetzt in `entwurf.css` definiert.

**Der Zeitplan** kommt aus `Zeitplan – NUR HTML.txt`, also aus derselben Excel wie die WordPress-Fassung: 3 Tagesblöcke, 27 Läufe, 7 CMS-Kennzeichen, PDF verlinkt. Oben steht ein Hinweis, dass die DLV-Genehmigung noch aussteht.

### Grußworte: Vorschlag statt Klappmenü unter „DM"
Oskar stört an der bestehenden Seite, dass die drei Grußworte einzeln im Klappmenü unter *DM Cross* hängen. Das sind: **Michael Scharmann** (Oberbürgermeister Weinstadt), **Dr. Richard Sigel** (Landrat Rems-Murr-Kreis), **Dieter Schneider** (Präsident WLV). Dazu kommt, dass Scharmanns Grußwort ausgerechnet unter `/impressum-2` liegt.

Gelöst im Entwurf durch drei Änderungen:
1. **Eine Seite statt drei.** Alle Grußworte untereinander, je eine Karte mit Porträt, Name, Funktion, Text und Unterschrift (bei Sigel und Schneider vorhanden, bei Scharmann nicht). Sprungmarken pro Person, damit man einzeln verlinken kann.
2. **Raus aus „DM".** Der Menüpunkt sitzt jetzt unter *Infos*. Grußworte sind Repräsentation, keine Wettkampfinformation, und gehören nicht in denselben Zweig wie Zeitplan und Strecken.
3. **Trotzdem sichtbar.** Auf der Startseite ein eigener Abschnitt mit den drei Porträts, Name und Funktion, der auf die Seite führt. Damit sind die drei Herren prominenter als bisher, ohne die Navigation zu belegen.

Die Texte wurden **unverändert** von der Live-Seite übernommen, nicht neu formuliert.

**Klappmenü statt Zwischenseite** (Wunsch von Oskar am 08.08.2026): Heute muss man im Menü erst auf „Info" klicken und landet auf `/teilnehmer`, bevor man weiterkommt. Im Entwurf klappen „Infos", „Vor Ort" und „Ergebnisse" beim Zeigen auf, jede Unterseite ist mit einem Klick erreichbar. Rein über CSS gelöst, ohne Javascript, auf dem Handy über ein Aufklappmenü mit allen Punkten flach untereinander.

## Offen

- Sponsorennamen und die Zuordnung zu Haupt/Partner/Verband sind aus den Dateinamen abgeleitet und von Oskar noch nicht bestätigt.
- Logos haben sehr unterschiedliche Seitenverhältnisse, einige wirken dadurch verloren. Für die fertige Fassung auf eine einheitliche Höhe normalisieren.
- Schrift: im Entwurf Systemschriften. Fertig wäre eine **selbst gehostete** Poppins, damit nichts von Google nachgeladen wird (löst zugleich den offenen Datenschutzpunkt).
- Adressen müssen exakt gleich bleiben oder sauber umgeleitet werden, sonst geht die im August 2026 aufgebaute Sichtbarkeit verloren. Die Menüstruktur enthält heute schon Altlasten: „Grußwort Michael Scharmann" zeigt auf `/impressum-2`, „Ergebnisse Archiv" auf `/muffin-builder-2502`.
- Anmeldung, Ergebnisse und Gesamtwertung kommen von der Zeitnahme-Firma. Muss geklärt werden, wie das eingebunden wird.
## Umzug auf den Server

**Gemessen am 08.08.2026:** Die Seite liegt auf **IONOS** (IP 217.160.0.195, `elastic-ssl.ui-r.com`), Server **Apache** mit **PHP 8.4.23**. Damit funktioniert `.htaccess`, Weiterleitungen sind also ohne Zusatzsoftware möglich.

**Empfehlung: beim bestehenden IONOS-Webspace bleiben.** Kein DNS-Umzug, keine Ausfallzeit, kein neuer Vertrag. Eine statische Seite braucht dort nichts weiter als hochgeladene Dateien, PHP wird gar nicht mehr benötigt. Ein Wechsel auf einen reinen Statik-Anbieter kann später immer noch kommen.

**Reihenfolge beim Umschalten:**
1. **Sicherung zuerst.** Kompletter Download des Webspace per SFTP plus Datenbank-Export über phpMyAdmin. Erst wenn die liegt, wird etwas angefasst.
2. **Auf demselben Server testen**, in einem Unterordner `/neu/`. Dann läuft der Entwurf unter der echten Adresse mit echtem HTTPS, ohne dass ihn jemand findet. Vorher `noindex` setzen, damit Google den Testordner nicht aufnimmt.
3. **Umschalten**: neue Dateien ins Wurzelverzeichnis, WordPress-Dateien entfernen. ⚠️ **`/wp-content/uploads/` unbedingt behalten**, dort liegen alle Fotos und Logos. Auf diese Adressen zeigen auch alte Facebook-Beiträge und der Entwurf selbst.
4. **`.htaccess` mit 301-Weiterleitungen** für alle Adressen, die sich ändern. Ohne das geht die im August 2026 aufgebaute Sichtbarkeit verloren.
5. **Danach** Search Console prüfen, Sitemap neu einreichen, auf 404er schauen.

Nebeneffekt: Ein altes WordPress, das niemand mehr pflegt, ist ein Sicherheitsrisiko. Nach dem Umzug entfällt der komplette Update-Zyklus für WordPress, Betheme, Yoast und alle weiteren Erweiterungen.

## Offen

- Anbieterwechsel für reines Statik-Hosting wäre später möglich, vor einer Entscheidung aber prüfen, welche Konditionen dann aktuell sind.
