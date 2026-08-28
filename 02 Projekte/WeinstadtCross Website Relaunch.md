---
tags: [web, projekt, wordpress]
status: aktiv
date: 2026-07-02
---

# WeinstadtCross Website Relaunch

Neue HTML-Version der Website als Alternative zu [weinstadtcross.de](https://weinstadtcross.de) (WordPress + Betheme). Verwandt: [[WeinstadtCross – SEO-Optimierung]].

## Dateien (iCloud: `Homepage WeinstadtCross/2026/`)

- **`weinstadtcross-2026-neu.html`** – neue Version (Juli 2026, Fable 5): Einzeldatei, ~390 KB, Logo eingebettet, Fotos/Sponsorenlogos werden vom Live-Server geladen (braucht Internet). Enthält: Hero-Slideshow, Countdown bis Startschuss, DM-Sektion, Zeitplan als Startliste, News, Galerie mit Lightbox, Infos, Sponsoren, SEO-Metadaten + Schema.org-Event-Markup (aus der SEO-Notiz übernommen).
- `weinstadtcross-html-version-2026-06-14.html` – gesicherte erste Version vom 14.06.
- `weinstadtcross-redesign.css` + `BeBuilder-Anleitung.md` – der alternative Weg: bestehendes WordPress-Theme umstylen statt ersetzen.

## Entscheidung (02.07.2026)

Oskar pflegt die Seite allein → **Weg 2 (Hybrid)**: Neue HTML-Version wird Startseite via Child-Theme-Template, Betheme/WordPress bleibt für alle Unterseiten. Die Startseite wird künftig im Code gepflegt (HTML-Datei in iCloud = Master, Änderungen mit Claude, dann neu hochladen). Fertiges Template: `page-cross2026.php` im iCloud-Ordner.

## Wege zur Umsetzung

### Weg 1: Testweise neben WordPress (risikofrei, empfohlen als Start)
Datei per FTP als `/2026/index.html` in den Webspace laden → sofort unter `weinstadtcross.de/2026/` erreichbar. WordPress bleibt unberührt. Gut für Feedback vom Orga-Team.

### Weg 2: Als neue Startseite, WordPress bleibt für Unterseiten (Hybrid, empfohlen als Ziel)
Die neue Seite verlinkt ohnehin auf die bestehenden WP-Unterseiten (Anmeldung, Ausschreibungen, Ergebnisse, News-Artikel). Umsetzung als Page-Template im Child-Theme (`page-cross2026.php`, HTML einfügen) → Seite anlegen → unter Einstellungen → Lesen als Startseite setzen. Vorteil: News & Unterseiten weiter über WP pflegbar, nur das Schaufenster ist neu.

### Weg 3: WordPress komplett ersetzen (statisch)
Ganze Site statisch, WP abschalten. Vorteile: Sicherheit (xmlrpc/Wordfence-Themen entfallen), Tempo, keine Updates. Nachteile: News/Ergebnisse nur noch von Hand pflegbar, Unterseiten müssten alle nachgebaut werden, Bilder aus `wp-content` müssten lokal kopiert werden. Werkzeug dafür wäre Publii (bereits installiert, zwei Testprojekte unter `~/Documents/Publii/sites/`). Erst sinnvoll, wenn klar ist wer die Seite pflegt.

## Neuer Reiter „Anreise & Parken" (05.08.2026)

Auf Wunsch des Orga-Kollegen aus Weinstadt. Fertiger Baustein: **`Anreise-und-Parken.html`** im iCloud-Ordner. Die Datei ist gleichzeitig lokale Vorschau (doppelklicken) und Kopiervorlage, der einzufügende Teil ist zwischen `AB HIER KOPIEREN` und `BIS HIER KOPIEREN` markiert.

- **Einbau:** neue WP-Seite anlegen → Block „Custom HTML" (bzw. in Betheme das Element „Code / HTML") → Block einfügen → Seite ins Menü unter **Info** hängen. Nicht in den Text-Tab des klassischen Editors einfügen, der zerschießt die Formatierung.
- **Technik:** alle Klassen mit `.wc-ap-` vorangestellt, damit nichts mit Betheme kollidiert. Kein JavaScript, die Reiter laufen über versteckte Radio-Buttons plus CSS. Keine Google Fonts, damit kein Datenschutzproblem entsteht.
- **Bilder:** vier Karten aus `Parkmöglichkeiten DM Cross 1.pdf` als Web-JPGs in `Bilder/` (`weinstadtcross-2026-parken-*.jpg`, je 300–430 KB). In die Mediathek hochladen und die vier `src`- und `href`-Pfade auf die Mediathek-URLs umstellen.
- Inhalt aus `Cross-DM Auslobungstext zur Anreise Kopie.pdf` und dem Lageplan-PDF. Adresse ITT Cannon (Cannonstr. 1, 71384 Weinstadt) über die Firmenseite bestätigt, alle anderen Parkplätze verlinken über Google-Maps-Namenssuche statt über erfundene Hausnummern.

### Vor der Veröffentlichung klären
- [ ] Genaue Adressen der Parkplätze beim Orga-Team erfragen. Der Auslobungstext verweist auf „Lageplan mit Adressen", im Lageplan stehen aber keine Adressen.
- [ ] Widerspruch: Der Text nennt „3 Bereiche" mit weiteren Parkplätzen, der Lageplan zeigt vier (Bürgerpark, ITT Cannon, Bahnhof Beutelsbach, Bahnhof Endersbach).
- [ ] Fußweg von ITT Cannon und Bahnhof Beutelsbach wirkt auf der Karte deutlich länger als die im Text genannten 10 Gehminuten. Vor der Veröffentlichung nachmessen lassen.
## Reiter „Übernachten" (05.08.2026)

Zweiter Baustein im gleichen Design: **`Uebernachten.html`**, Kopiervorlage `Uebernachten – NUR ZUM KOPIEREN.txt`. Quelle: `DM Cross - Übernachtungsmöglichkeiten.pdf`.

- Drei Reiter: Hotels & Gasthäuser (6), Ferienwohnungen (3), Wohnmobilstellplätze (7). Eigener CSS-Präfix `.wc-ue-`, damit sich die beiden Blöcke nicht in die Quere kommen, falls sie mal auf einer Seite landen.
- Alle 16 Links am 05.08.2026 geprüft, alle erreichbar. `gh-koenig.de` leitet auf `gaestehaus-weinstadt.de` weiter, deshalb steht direkt das Ziel im Code. Die fünf Remstal-Tourismus-Links wurden zusätzlich über den Seitentitel auf den richtigen Stellplatz geprüft.
- Die URLs im PDF waren umgebrochen und mussten wieder zusammengesetzt werden. Bei einer neuen PDF-Version also erneut prüfen.
- Keine Bilder nötig, der Block ist nach dem Einfügen sofort fertig.

## Startseite modernisiert – reines Stylesheet (05.08.2026)

Datei: **`startseite-redesign.css`** im iCloud-Ordner. Einbau über Design → Customizer → Zusätzliches CSS. Rückgängig machen heißt: CSS dort löschen.

Bewusst **kein** Umbau der Seite, sondern nur ein Stylesheet. Grund: Oskar will den Inhalt unverändert lassen und weiterhin Beiträge in WordPress ergänzen. Die News auf der Startseite kommen aus dem Betheme-Modul `Latest_news`, das die Beiträge dynamisch zieht. Ein statischer HTML-Nachbau würde genau das kaputt machen.

- Selektoren bewusst über **stabile Betheme-Klassen** (`.Latest_news`, `.column_countdown`, `.column_fancy_heading`, `.column_image`), nicht über die generierten Hash-Klassen wie `.mcb-section-89e2f5f1a`. Die ändern sich, sobald die Seite im BeBuilder bearbeitet wird.
- Teil 1 wirkt nur auf der Startseite (`body.home`), Teil 2 ist optional und ersetzt das Betheme-Blau im Menü durch Schwarz mit gelber Markierung.
- Umgesetzt: Begrüßungstext als hervorgehobener Kasten, News-Liste wird zu Karten mit gelbem Balken, Countdown als schwarzes Panel mit gelben Zahlen, Flatterband als Trenner, Sponsorenlogos in gleichmäßigen Rahmen.
- Die Countdown-Beschriftung stand auf Englisch (days/hours/minutes) und wird per CSS auf Tage/Stunden/Minuten gesetzt. Sauberer wäre eine Änderung direkt im Betheme-Modul.

### Beim Testen aufgefallen
- [ ] Die Überschrift „Mit freundlicher Unterstützung von" steht in der Seitenspalte **unter** den meisten Sponsorenlogos statt darüber.
- Der Countdown selbst läuft korrekt, Ziel `11/28/2026 11:00:00`.

### Analyse: leerer Slider oben auf der Startseite (05.08.2026)

Der obere LayerSlider (`layerslider_11`) belegt 789 × 444 px und bleibt leer. Gemessen bei 1400 px Fensterbreite, mehrfach reproduziert.

**Befund**
- LayerSlider baut das Gerüst (`.ls-inner`, Navigation, Timer), erzeugt aber **kein einziges `.ls-slide`**. Alle Bildebenen bleiben auf 0 × 0 px.
- Im Quelltext hat der Slider 9 Slides. **Alle** Bildebenen tragen die Klasse `ls-l`, sind also Animationsebenen, die erst mit der laufenden Diashow sichtbar werden.
- Die erste Ebene hat zusätzlich `ls-hide-desktop ls-hide-tablet ls-hide-phone`, ist also auf **allen** Geräteklassen ausgeblendet.
- Mehrere Ebenen haben `height: falsepx`, also einen kaputten Höhenwert aus dem Slider-Editor.
- Der zweite Slider auf derselben Seite (`layerslider_3`, Seitenspalte) läuft. Dessen sichtbare Ebenen haben **kein** `ls-l`. Also kein Plugin-Problem, sondern die Konfiguration von Slider 11.
- Der Slider wurde mit LayerSlider **7.0.7** erstellt, installiert ist **8.2.0**.

**Offen:** Warum die Diashow nicht startet, ist von außen nicht erkennbar. Dafür muss der Slider im WordPress-Backend geöffnet werden.

### Hero als Ersatz für den leeren Slider (05.08.2026)

Dateien: **`Hero-Startseite.html`** (lokale Vorschau) und `Hero-Startseite – NUR ZUM KOPIEREN.txt` (203 Zeilen). Gedacht als Ersatz für den defekten LayerSlider oben auf der Startseite.

- Fünf Fotos aus der Mediathek (`Weinstadtcross2025_2, _1, _6, _9, _8`), Bildwechsel alle 8 Sekunden **rein über CSS-Keyframes**, kein JavaScript und kein Slider-Plugin.
- Kein `loading="lazy"` auf den Hero-Bildern. Bei Ebenen, die nur per Animation sichtbar werden, lädt der Browser sonst nur das erste Bild und die Überblendung zeigt Lücken. Das war im Test reproduzierbar.
- `srcset` mit 768/1024/1536/1600 px, damit Handys nicht die großen Dateien ziehen.
- Berücksichtigt `prefers-reduced-motion`, dann steht das erste Foto still.
- Inhalt nur aus gesicherten Angaben: Termin, Ort, Aufteilung Samstag/Sonntag aus dem Begrüßungstext der Startseite. Verlinkt auf `/anmeldung` und `/zeitplan-dm`, beide vorher auf Status 200 geprüft.

### Gesamtvorschau der Startseite (05.08.2026)

Datei: **`Gesamtvorschau Startseite.html`**. Zeigt die komplette Startseite am Stück: echtes Banner, Menü, neues Hero, Begrüßungstext, News, Countdown und Seitenspalte mit Video und Sponsoren.

**Nur zum Anschauen, wird nicht nach WordPress kopiert.** Das steht auch als schwarzer Balken oben in der Datei. Die Beiträge sind ein eingefrorener Stand, auf der echten Seite kommen sie live aus WordPress.

- Baut auf denselben Betheme-Klassen auf und bindet `startseite-redesign.css` unverändert ein. Damit ist die Vorschau gleichzeitig ein Test, ob das Stylesheet stimmt.
- Erzeugt mit `.scripts`-fähigem Skript, aktuell im Scratchpad als `baue_gesamtvorschau.py`. Bei neuen Beiträgen einfach neu laufen lassen.
- Spaltenbreite bewusst auf 789 px getrimmt, sonst brechen die News-Karten anders um als auf der echten Seite.

### Hero-Varianten nach Feedback (05.08.2026)

Datei: **`Hero-Varianten.html`**. Oskars Kritik an der ersten Fassung: 8 Sekunden bis zum Bildwechsel zu lang, Bilder wegen zu dunklem Schleier und zu präsenter Schrift kaum erkennbar, Gestaltung wirkt billig und zu bunt.

- **Variante A (Ruhig):** Verlauf nur unter der Schrift, läuft nach rechts aus. Kein Flatterband, kein gelber Kasten. Gelb nur als 44 px Strich und als 4 px Linie unten. Untertitel nicht mehr versal und nicht mehr gelb.
- **Variante B (Foto im Vordergrund):** Foto bleibt fast frei, Text sitzt in einem ruhigen Band darunter. Gelb nur in der Schaltfläche und als Trennlinie.
- Bildwechsel jetzt alle 5 Sekunden statt 8.

**Wichtiger Fehler, den Oskar entdeckt hat:** Die erste Überblendung hatte eine Lücke. Jedes Bild wurde ausgeblendet, bevor das nächste anfing, dadurch war rund eine Sekunde pro Wechsel gar kein Bild voll deckend und alles wirkte fast schwarz. Meine Stichproben alle 2 Sekunden hatten das nicht erwischt.

**Richtige Lösung:** Foto 1 liegt dauerhaft mit voller Deckkraft darunter, die Fotos 2 bis 5 blenden nacheinander darüber ein und am Zyklusende gemeinsam wieder aus. Damit ist immer ein Bild voll deckend. Geprüft über einen kompletten 25-Sekunden-Zyklus mit 26 Messungen, sichtbare Deckkraft konstant 1,0.

**Lehre:** Bei CSS-Überblendungen nie nur stichprobenartig messen, sondern über einen vollen Zyklus und die effektive Deckkraft des Stapels berechnen, nicht die Einzelwerte.

## ✅ Live seit 05.08.2026

Stylesheet und Hero sind auf weinstadtcross.de eingebaut und geprüft.
- Alle drei Teile des Stylesheets im Customizer aktiv, inklusive TEIL 3 mit den Hero-Keyframes.
- Hero-Block steht oben in der linken Spalte, alle fünf Fotos laden mit Status 200, Schaltflächen zeigen auf `/anmeldung` und `/zeitplan-dm`.
- Der leere LayerSlider in der linken Spalte ist entfernt. Der zweite Slider unten in der Seitenspalte läuft weiter und bleibt.

**Messfalle:** `naturalWidth` meldete im Testbrowser 0, obwohl alle Bilder mit 200 geladen wurden. Bei Bildprüfungen deshalb nicht allein auf `naturalWidth` verlassen, sondern das Netzwerkprotokoll und einen Screenshot dazunehmen.

### ❗ Fehler: Download-Knopf landete im PDF (06.08.2026)

Die Druckfassung nimmt denselben HTML-Block wie die Webseite. Dadurch stand im PDF ein Link „Zeitplan herunterladen", also ein Verweis auf genau das PDF, das man gerade liest. Weil das Druck-CSS keine Regel für `.wc-dl` hat, erschien er zusätzlich als blauer Standardlink und fiel optisch heraus.

**Behoben:** `baue_zeitplan_pdf.py` entfernt den Knopf jetzt vor dem Drucken per Regex und meldet im Protokoll, wie viele entfernt wurden.

**Merksatz:** Wenn ein Baustein für Web **und** Druck verwendet wird, gehören alle Navigations- und Download-Elemente vor dem Drucken heraus. Ein PDF ist ein Endpunkt, keine Seite mit Verweisen auf sich selbst.

Ebenfalls doppelt: Auf `/zeitplan-dm` gibt es **zwei** Download-Knöpfe, einen aus meinem Block und einen als Betheme-Element, das Oskar selbst angelegt hat. Beide zeigen auf dieselbe Datei und stehen untereinander.
- [ ] **Zurückgestellt.** Oskar vergleicht beide optisch und entscheidet erst, wenn der Zeitplan nach der DLV-Genehmigung endgültig ist. Bis dahin keine weiteren Änderungen an der Seite.

## Abgleich Website gegen neue Ausschreibung (07.08.2026)

Quelle: `2026_Ausschreibung_Volksbank_WeinstadtCross_1.pdf`, laut Oskar **maßgeblich**. Verglichen wurden Startseite, Prämien, Strecken, Zeitplan und Ausschreibung.

### ❗ 1. Prämienseite ist inhaltlich falsch
Sie zeigt weiterhin die Werte aus `Praemien_uebersicht_2025.pdf`.

| | Website (2025) | Ausschreibung 2026 |
|---|---|---|
| Kategorien | 6.600 m Aktive/U23 · 2.200 m U18 · 3.300 m U20 | **nur 2.100 m U18 · 2.100 m U16** |
| Beträge | 120 / 80 / 50 EUR | 120 / 80 / 50 EUR (unverändert) |
| Hauptlauf | mit Geldprämie | **keine Geldprämie mehr**, stattdessen kostenlose SGCube-Mitgliedschaft für die drei Erstplatzierten aus Weinstadt (1 Jahr / ½ Jahr / ¼ Jahr) |

Es stehen also Prämien für Wettbewerbe auf der Seite, die es in dieser Form nicht mehr gibt, und die neue U16-Wertung fehlt.

### ❗ 2. Streckenseite: Wettbewerbstabelle veraltet
Die Tabelle stammt aus dem Zeitplan der **alten** Ausschreibung und nennt 1.100 / 2.200 / 3.300 / 4.400 / 6.600 m. Keine dieser Distanzen kommt im aktuellen Zeitplan noch vor, dort gilt 1,0 / 2,1 / 3,2 / 4,2 / 5,3 / 6,4 / 7,5 km.
Die vier Rundenkarten (CR 1.100 m, SR 640 m, MiR 300 m, MR 150 m) stimmen weiterhin, nur die Zuordnung der Wettbewerbe nicht.

### ❗ 3. Hausnummer der Wettkampfstätte
Website (Streckenseite): Beutelsbacher Straße **82**. Neue Ausschreibung: Navi **Beutelsbacher Str. 84**. Die 82 ist die Geschäftsstelle, nicht das Stadion.

### ✅ Stimmt überein oder unkritisch
- Großer Preis der Volksbank über **5,3 km**, deckt sich mit dem Zeitplan.
- **Der alte Widerspruch ist aufgelöst:** Die neue Ausschreibung nennt 2.100 m, der Zeitplan 2,1 km. Die früheren 6.400 m und 2.200 m kommen nicht mehr vor.
- Betriebssportmeisterschaften des BWBV sind aus der Ausschreibung verschwunden und standen auch nie auf der Website.
- Startunterlagen jetzt ab **08:00 Uhr** statt 08:30, Verpflegung nur noch in der Sporthalle. Beides steht auf keiner Seite, also kein Widerspruch.
- Sonderpreis heißt jetzt „Sport Schwab Cup U16/U18" statt „Sport Schwab Preis U16".

### Zu tun
- ✅ **Prämienseite neu aufgebaut (07.08.2026).** Tabelle jetzt mit zwei Spalten (2.100 m U18 und U16). Neu dazu: Abschnitt **Sonderpreise** mit drei Karten (Sport Schwab Cup, Großer Preis der Volksbank mit der SGCube-Staffelung, TeamCross-Staffel) und ein Abschnitt **Auszeichnungen** (Medaillen, keine Mannschaftswertung, Blanko-Urkunde). CSS als Ergänzung zu TEIL 5.
  Geprüft: alle elf Kernangaben der Ausschreibung im Block enthalten, keiner der fünf veralteten Werte (6.600, 3.300, 2.200, U20, Aktive) mehr vorhanden.
  ⚠️ Die Distanz „3,2 km" bei der TeamCross-Staffel steht **nicht** in der Ausschreibung, sie stammt aus dem Zeitplan. Falls unerwünscht, streichen.
- ✅ **Streckenseite neu erzeugt (07.08.2026).** Neues Skript `baue_strecken.py` liest `Zeitplan_2026.xlsx` und gruppiert die Wettbewerbe nach Rundenzahl. Ergebnis sind zehn Gruppen von der Mini-Runde bis 7 Crossrunden, insgesamt 27 Wettbewerbe. Damit können Streckenseite und Zeitplan nicht mehr auseinanderlaufen.
- ✅ **Startpositionen ergänzt.** Die Legende der Excel liefert die Zuordnung, sie steht jetzt auf den vier Rundenkarten: Cross Runde und Sprint Runde an Start 1, Midi Runde an Start 3, Mini Runde an Start 2. Damit ist die seit dem 06.08. offene Frage beantwortet, der Hinweis „wird vor Ort ausgeschildert" konnte entfallen.
- ✅ **Hausnummer auf 84 geändert.**
  Beim Erzeugen fielen zwei eigene Fehler auf: Die Excel wiederholt ihre Kopfzeile für den zweiten Tag, sie landete zuerst als Wettbewerb in der Tabelle. Und ich hatte eine CSS-Klasse verwendet, die es im Stylesheet nicht gibt. Beides behoben.

## Technik-Prüfung Startseite (06.08.2026)

Gemessen, nicht geschätzt: **77 Anfragen, rund 4,5 MB** für einen Seitenaufruf. HTML selbst ist mit 45 KB gzip völlig in Ordnung, das Gewicht steckt in den Bildern.

### 1. Sponsorenlogos: 2,3 MB Ersparnis (größter Hebel)
Acht Logos machen **2,6 MB** aus, obwohl sie nur wenige hundert Pixel breit dargestellt werden. Sie liegen in Originalauflösung bis 2560 px.

| Datei | jetzt | Maße | optimiert |
|---|---|---|---|
| Logo_Stadtwerke_Weinstadt | 894 KB | 2560 × 839 | 83 KB |
| Genehmigter_Lauf_2026 | 603 KB | 2560 × 2560 | 34 KB |
| Volksbank-WeinstadtCross-Logo | 269 KB | 2048 × 386 | 28 KB |
| RZ_Logo_Mack | 221 KB | 1181 × 709 | 20 KB |
| WOT | 193 KB | 2508 × 658 | 18 KB |
| Sportschwab | 158 KB | 2510 × 782 | 21 KB |
| Entenmann | 151 KB | 2512 × 762 | 16 KB |
| Untitled-1 (QR) | 123 KB | 1080 × 1920 | 36 KB |
| **Summe** | **2.613 KB** | | **255 KB** (−90 %) |

Fertige Dateien liegen in `Logos optimiert/` (WebP, max. 800 px Breite, Qualität 88).

### 2. ✅ Meta-Beschreibung, Seitentitel und Event-Markup (erledigt am 08.08.2026)
Seit dem 08.08.2026 gemessen in Ordnung:

| Punkt | Stand |
|---|---|
| Seitentitel | „Volksbank WeinstadtCross 2026 \| DM Crosslauf in Weinstadt", 57 Zeichen |
| Meta-Beschreibung | 154 Zeichen, mit Datum und Ort, genau **eine** im Quelltext |
| WordPress-Untertitel | „Deutsche Crosslauf-Meisterschaften am 28. und 29. November 2026 in Weinstadt" |
| Schema.org-Event | `SportsEvent` als gültiges JSON-LD auf der Startseite |

**Woher die doppelte Beschreibung kam.** Nicht von Yoast und nicht vom Untertitel. Betheme gibt über Theme Options → SEO → *Use built-in fields* eine eigene Beschreibung aus, die noch auf dem WordPress-Standardtext stand. Sie erschien an Zeichenposition 266 im Kopfbereich, also **vor** dem Yoast-Block ab 706, und war damit die, die Google gelesen hätte. Erkennbar war das nur daran, dass RSS-Feed und `wp-json` bereits den neuen Untertitel zeigten, die Startseite aber nicht. ⚠️ Der Schalter *Use built-in fields* steht weiterhin auf an, nur das Textfeld ist leer. Sauberer wäre, ihn ganz auszuschalten, da Yoast im Einsatz ist (so auch die [Betheme-Doku](https://support.muffingroup.com/documentation/theme-options-seo/)).

**Einbau des Event-Markups.** Betheme hat kein Feld für eigenen Code im Kopfbereich, die SEO-Sektion kennt nur Google Analytics, Facebook Pixel und Google Remarketing. Der Block liegt deshalb als Text-Element ganz unten auf der Startseite. Der BeBuilder lässt `<script type="application/ld+json">` durch, anders als seinerzeit `<style>`. Quelle: `Event-Markup Startseite.txt` im Homepage-Ordner, reines ASCII über `\uXXXX`-Escapes, damit beim Kopieren keine Umlaute zerschossen werden.

Inhalt: 28.–29.11.2026, Stadion beim Bildungszentrum Weinstadt-Benzach (Beutelsbacher Str. 84), Veranstalter SG Weinstadt e.V. (Adresse und Telefon aus dem Impressum), drei Fotos, beide Wettkampftage als `subEvent`. **Bewusst ohne Uhrzeiten**, solange der Zeitplan auf die DLV-Freigabe wartet. Startzeiten danach nachtragen.

### 2b. ✅ Vorschaubild beim Teilen (og:image, 08.08.2026)
Startseite liefert jetzt `https://weinstadtcross.de/wp-content/uploads/2026/08/Vorschaubild-mit-Text.jpg`, 1200 × 630, 119 KB, Verhältnis 1,90 zu 1, dazu `og:image:width`/`height` von Yoast. `twitter:card` steht auf `summary_large_image`. `twitter:image` ist leer, das ist **kein Fehler**: X fällt auf `og:image` zurück.

**Wo die Einstellung sitzt.** Bei einer statischen Startseite **nicht** in den Yoast-Einstellungen, sondern im Yoast-Kasten der Seite *Home* selbst, Bereich *Social-Darstellung*. Titel und Beschreibung dort bewusst leer lassen, dann erbt Yoast die Google-Texte.

**Wie das Bild entsteht.** `og.py` im Scratchpad rendert es mit Headless Chrome aus HTML, also in derselben Bildsprache wie der Hero-Block: Foto vom Massenstart unter dem gelben Bogen, dunkler Verlauf nach unten, gelber Strich, Poppins in Versalien, gelbe Linie am Fuß. Zwei Fassungen liegen im Homepage-Ordner: `Vorschaubild-mit-Text.jpg` (im Einsatz) und `Vorschaubild-ohne-Text.jpg`.

⚠️ Auf dem Bild sind **Kinder mit erkennbaren Gesichtern und Startnummern** zu sehen. Das Foto steht ohnehin öffentlich in der Hero-Slideshow, als Vorschaubild wandert es aber sichtbarer durch Verteiler und Chats. Falls das später anders bewertet wird: Ersatzmotiv ist `Weinstadtcross2025_8` (schlammiger Laufschuh, ohne Personen), Neurendern dauert eine Minute.

### 2c. Unterseiten: Vorschaubild erledigt, Google-Beschreibung offen (08.08.2026)
Vorschaubild sitzt auf **Anreise und Parken, Übernachten, Strecken, Ausschreibung und Prämien** (Seiten-IDs 3050, 3048, 260, 266, 2949). In WhatsApp erscheint jetzt Bild, Überschrift und Text, geprüft.

⚠️ **Das Standardbild für alle Seiten auf einmal ist in Yoast Free gesperrt.** Yoast → Einstellungen → Content-Typen → Seiten → Social-Media-Auftritt → *Bild für Social-Media* ist Premium. Deshalb pro Seite einzeln über den Yoast-Kasten, das geht in der kostenlosen Version.

**Die Falle im Yoast-Kasten**, zweimal reingelaufen: Der Kasten hat zwei Bereiche untereinander mit fast gleich klingenden Feldern.

| Feld | Bereich | Wer liest es |
|---|---|---|
| Meta-Beschreibung | oben, unter der Google-Vorschau | **Google** |
| Beschreibung für Social-Media | unten, bei *Social-Media-Auftritt* | **WhatsApp, Facebook** (`og:description`) |

Zusätzlich sitzt oben die **Titelform**, das ist die Webadresse, nicht der Titel. Da war schon einmal der SEO-Titel gelandet.

**Offen:** `meta description` ist auf allen fünf Unterseiten leer, sie tragen außerdem die Standardtitel („Anreise und Parken - WeinstadtCross"). Google baut sich den Snippet dann selbst aus dem Seitentext. Kein Fehler, nur unkontrolliert. Fertige Texte liegen in `Meta-Beschreibungen Unterseiten.txt` im Homepage-Ordner, einzutragen oben unter der Google-Vorschau. Bewusst zurückgestellt, weil der Nutzen gegenüber dem bereits Erreichten klein ist. Für die News-**Beiträge** ist das Vorschaubild ebenfalls noch nicht gesetzt.

### 3. In Ordnung
canonical gesetzt, Favicon vorhanden, `lang="de"`, gzip aktiv, `http` leitet auf `https`, `www` leitet auf die Hauptdomain. Sicherheits-Header (HSTS, X-Content-Type-Options) fehlen, für eine Vereinsseite aber nachrangig.

## Grußworte und Ergebnisarchiv (12.08.2026)

**Grußworte auf einer Seite statt vier.** Neue Seite `/grussworte` (ID 3094) mit allen vier Grußworten als Karten: **Klaus Silbernagel** (Vorstandsvorsitzender SG Weinstadt, neu, aus PDF), Michael Scharmann (OB), Dr. Richard Sigel (Landrat), Dieter Schneider (WLV). Drei davon mit Unterschrift, Scharmann hat keine. Damit ist der Ärger erledigt, dass die Grußworte einzeln im Klappmenü unter *DM Cross* hingen. Erzeugt von `baue_grussworte_wp.py`, CSS in TEIL 10.

Die drei alten Einzelseiten (`/grusswort-dieter-schneider`, `/grusswort-dr-richard-sigel`, `/impressum-2`) werden **gelöscht**, nicht umgeleitet. Entscheidung von Oskar am 12.08.2026: Auf die alten Adressen muss niemand mehr zugreifen. Vor dem Löschen geprüft, dass keine Seite und kein Beitrag mehr darauf verlinkt und dass das echte Impressum unter `/impressum` liegt.

**Klaus Silbernagels Unterschrift** steckte nicht als eigenes Bild im PDF, die ganze Seite ist ein Scan. Freigestellt über die **Tintenfarbe**, nicht über die Helligkeit: Nur was deutlich blau ist bleibt stehen, dadurch fällt der schwarze Text darunter weg. Ergebnis 7 KB mit Transparenz. Der erste Versuch über die Helligkeit hatte den Text mitgenommen.

**Ergebnisarchiv** (`/muffin-builder-2502`) neu als Kartenraster, TEIL 9. Vorher hießen alle neun Links „Click here", was für Screenreader und Google gleichermaßen wertlos ist. Beim Umbau alle Ziele geprüft: fünf zeigten auf abavent.de, das auf datasport.de umleitet, jetzt direkt aufs Endziel. 2017 läuft nun über https, 2016 bleibt bei http, weil der Server dort die verschlüsselte Verbindung abbricht.

### Zwei Fallen, die Zeit gekostet haben
- **Silbentrennung aus PDFs.** Beim Zusammenfügen von „Cross- Meisterschaften" zerstörte eine zu grobe Regel auch korrekte Bindestriche („Straßen- und" wurde zu „Straßenund"). Regel jetzt eingegrenzt auf Fälle, in denen nach dem Bindestrich ein **Großbuchstabe** folgt. Bei fremden Texten besonders heikel.
- **Ligaturen aus PDFs.** Ein zusammengezogenes „ff" (U+FB00) rutschte durch und wäre als Sonderzeichen auf der Seite gelandet. Wird jetzt aufgelöst.

⚠️ **Kaputte YouTube-Einbettung auf der Sponsorenseite**: `youtube.com/embed/https://youtu.be/czxGkGwoIdU`, also eine vollständige Adresse hinter `/embed/`. Das Video kann so nicht laufen.

**Lehre fürs Prüfen:** Dreimal kam ein CSS-Stand nicht online an. Statt zu raten hat jedes Mal derselbe Messwert geholfen, nämlich die Zeichenzahl von `<style id="wp-custom-css">` im Quelltext. Bleibt sie gleich, wurde nichts gespeichert, unabhängig davon woran es liegt.

## Wartet auf die DLV-Genehmigung

Der Zeitplan geht über den Kollegen zum DLV. Erst danach:
1. Neue Excel kommt, Block und PDF neu erzeugen (Skripte liegen bereit, dauert unter einer Minute).
2. PDF-Link mit Versionsnummer versehen, damit niemand die alte Fassung im Zwischenspeicher behält.
3. Einen der beiden Download-Knöpfe entfernen.
4. Seite ins Menü hängen und bei Yoast wieder auf indexierbar stellen.

Bis dahin: **`/zeitplan-dm` bei Yoast auf „nicht in Suchergebnissen" stellen**, sonst indexiert Google den noch nicht genehmigten Plan.

### Zeitplan-Aktualisierung 3 (06.08.2026, 22:09)

Zwei Zeilen geändert: **DM 11 und DM 12 (W35-W45 und M35-M45 Langstrecke) von 5,3 km / 5CR auf 6,4 km / 6CR.**

Zweck: Das PDF soll dem DLV zur Genehmigung vorgelegt werden.

**❗ Struktur der Excel hat sich geändert:** Das veraltete Blatt wurde gelöscht, die Mappe hat jetzt nur noch **ein** Blatt, das wieder „Tabelle1" heißt. Das Skript brach ab, weil es fest auf `sheet2.xml` zugriff.

**Behoben:** Das Skript löst die Blätter jetzt über `xl/_rels/workbook.xml.rels` auf und wählt selbst das passende aus. Bewertet wird nach Vorhandensein der Legende („CMS ="), der Kopfzeile („Siegerehrung") und der Anzahl gefüllter Startzeiten. Damit ist es gegen Umbenennen, Löschen und Umsortieren von Blättern unempfindlich und meldet im Protokoll, welches Blatt es genommen hat.

**Rundenlogik, Stand jetzt:** 1,0 / 2,1 / 3,2 / 4,2 / 5,3 / 6,4 / 7,5 km. Die Schritte betragen durchgehend 1,1 km, **außer zwischen 3 und 4 Runden, dort nur 1,0 km**. Entweder müsste 3CR 3,1 km oder 4CR 4,3 km heißen. Für die Vorlage beim DLV erwähnenswert.

### Zeitplan-Aktualisierung 2 (06.08.2026)

Neue Fassung von `Zeitplan_2026.xlsx`, wieder Tabelle2. Block und PDF neu erzeugt, beides in wenigen Sekunden, weil alles aus einem Skript kommt.

**Vier geänderte Zeilen:**
| Wettbewerb | Feld | vorher | jetzt |
|---|---|---|---|
| TeamCross Staffel | Siegerehrung | 13:00 | 13:30 |
| Bort SchnupperCross | Runden / Siegerehrung | ergänzt / leer | aus der Datei / 13:30 |
| DM 5 M65-M90 / W50-W90 | Strecke / Runden | 3,2 km / 3CR | **4,2 km / 4CR** |
| DM 6 M50-M60 | Alter / Strecke / Runden | 50-59 / 4,2 km / 4CR | **50-64 / 5,3 km / 5CR** |

Der Wert beim SchnupperCross steht jetzt in der Excel selbst, meine Ergänzung `ERGAENZUNG["F15"]` greift dadurch automatisch nicht mehr. Sie bleibt als Rückfallebene im Skript stehen.

**Neue Rechtschreibregel:** In der Rundenspalte stand einmal „2 CR" mit Leerzeichen, sonst überall „3CR". Wird jetzt vereinheitlicht (`(\d)\s+(CR|SR)` → ohne Leerzeichen), gleiche Kategorie wie „U 10" → „U10".

Abgleich gegen die neue Excel: null fehlende Felder, null fehlende Uhrzeiten.

### Zeitplan als PDF im Seitendesign (06.08.2026)

Datei: **`Zeitplan-WeinstadtCross-2026.pdf`**, eine Seite A4, 172 KB. Erzeugt mit `baue_zeitplan_pdf.py` aus derselben Quelle wie die Webseite, also aus Tabelle2 der Excel. Zwischenschritt ist `Zeitplan-Druck.html`.

**Technik:** kein Zusatzprogramm nötig, gedruckt wird mit Chrome im Hintergrund:
`--headless=new --no-pdf-header-footer --print-to-pdf=…`. Farben müssen im CSS über `print-color-adjust:exact` ausdrücklich freigegeben werden, sonst druckt Chrome die schwarzen Balken weiß.

Erster Durchlauf ergab zwei Seiten mit fast leerer zweiter Seite. Durch engere Seitenränder (9 mm), kleinere Zellenabstände und leicht reduzierte Schriftgrade passt jetzt alles auf eine Seite, inklusive Legende und Fußzeile.

Der Download-Knopf im Zeitplan-Block holt sich die **Dateigröße automatisch** aus dem PDF, die Angabe kann also nicht veralten.

### ❗ Fehler: falsches Tabellenblatt ausgelesen (06.08.2026)

`Zeitplan_2026.xlsx` hat **zwei Blätter**. Ich hatte nur `Tabelle1` gelesen und daraus geschlossen, sieben Startzeiten fehlten. **Maßgeblich ist `Tabelle2`**, dort ist alles gefüllt. Oskars Einwand „da ist nichts leer" war richtig.

**Regel für Excel-Dateien: immer zuerst alle Blätter auflisten**, nicht `sheet1.xml` als gegeben nehmen. Ein Blick auf die Zellenzahl hätte gereicht, Tabelle2 hatte mehr Zellen als Tabelle1.

Unterschiede von Tabelle2 gegenüber Tabelle1:
- Alle Startzeiten vorhanden (10:30 bis 15:10 am Samstag).
- DM-Läufe eigens als **DM 1 bis DM 14** nummeriert statt als „Lauf 1-4" und „Lauf 5-14".
- Lauf 10 in vier eigene Zeilen aufgelöst: Großer Preis 5,3 km, JedermannCross 3,2 km, TeamCross Staffel 3,2 km, SchnupperCross 2,1 km. In Tabelle1 stand alles in einer Zelle mit nur einer Distanz.
- Marker **CMS** für die Crosslaufmeisterschaften der Schulen an sieben Wettbewerben.
- **Legende mit der Zuordnung Runde zu Startposition** – beantwortet die vorher offene Frage:
  MR Mini Runde (Start 2) · MiR Midi Runde (Start 3) · SR Sprint Runde (Start 1) · CR Cross Runde (Start 1)

Rechtschreibkorrekturen in Tabelle2: „Grroßer" → „Großer", „JedermanCross" → „JedermannCross", „Männlcihe" → „Männliche", „U 10" → „U10". Zeichengenauer Abgleich: null inhaltliche Abweichungen.

**Inhaltliche Ergänzung auf Oskars Anweisung (06.08.2026):** Beim Bort SchnupperCross war die Rundenspalte in Tabelle2 leer, ergänzt mit **2CR** (2,1 km entsprechen zwei Crossrunden). Steht als `ERGAENZUNG = {"F15": "2CR"}` im Skript, ist also als Zusatz erkennbar und überlebt jedes Neuerzeugen. Sollte die Excel später korrigiert werden, greift der Wert aus der Datei automatisch vor.

### Zeitplanseite gebaut (06.08.2026)

Dateien: `Zeitplan – NUR HTML.txt` (277 Zeilen), Vorschau `Zeitplan.html`, CSS als **TEIL 8**. Erzeugt mit `baue_zeitplan.py` (Scratchpad).

**Der Block wird direkt aus der Excel erzeugt, keine Zahl ist von Hand abgetippt.** Bei neuen Zeiten einfach das Skript erneut laufen lassen. Die Excel-Uhrzeiten sind Bruchteile eines Tages und werden im Skript umgerechnet (0,4375 → 10:30).

Aufbau: drei Blöcke, Samstag Vormittag (10 Läufe), Samstag Nachmittag Mittelstrecke (4 Läufe), Sonntag Mittel- und Langstrecke (10 Läufe). Die sieben fehlenden Startzeiten stehen als gelbe Markierung „noch offen" in der Tabelle, damit die Lücke sichtbar ist statt still zu fehlen.

**Regel von Oskar (06.08.2026): Inhalt exakt wie in der Excel, auch bei Widersprüchen. Rechtschreibung darf korrigiert werden.**

Erlaubt und umgesetzt sind daher nur: Buchstabendreher „Männlcihe" → „Männliche" (Sonntag Lauf 10), überzähliges Leerzeichen „U 10" → „U10", doppelte Leerzeichen zusammengezogen und das fehlende Leerzeichen vor der Einheit („0,15km" → „0,15 km").

**Nicht angetastet:** Zahlen, Distanzen, Rundenzahlen, Zeiten, Wettbewerbsnamen und die widersprüchliche 4,2-km-Angabe. Kein Glätten, kein Auflösen von Widersprüchen.

Geprüft mit einem zeichengenauen Abgleich Zelle für Zelle gegen die Excel: **null Abweichungen** außer den vier genannten Rechtschreibpunkten. Die Korrekturliste steht als `RECHTSCHREIBUNG` oben im Skript und ist damit nachvollziehbar und umkehrbar.

## ⚠️ Neuer Zeitplan (`Zeitplan_2026.xlsx`, 06.08.2026) – Analyse

Der neue Zeitplan ist **keine Korrektur, sondern ein anderer Wettkampf**. Damit ist der Text der bestehenden Ausschreibung in weiten Teilen überholt.

**Was neu ist**
- Wettkämpfe an **beiden Tagen**. Samstag zehn Läufe plus vier Mittelstrecken-Läufe am Nachmittag, Sonntag zehn Läufe (Nummerierung 5 bis 14).
- Neue Kategorien **Mittelstrecke** und **Langstrecke** sowie Altersklassen bis M90/W90.
- Neue Distanzen: 3,2 km, 4,2 km, 5,3 km und 7,5 km. Die bisherigen 6.600 m und 4.400 m kommen nicht mehr vor.

**Blocker: sieben Startzeiten fehlen.** Samstag Lauf 4 bis Lauf 10 haben keine Startzeit, nur eine Siegerehrungszeit. Ohne diese Zeiten lässt sich der Zeitplan nicht veröffentlichen.

**Rundenlogik stimmt nicht mehr mit dem Streckenplan.** Der Plan nennt die Crossrunde mit 1.100 m, die Distanzen im Zeitplan folgen aber dem Muster erste Runde 1,0 km, jede weitere 1,1 km:

| Runden | angegeben | nach Muster | |
|---|---|---|---|
| 1 CR | 1,0 km | 1,0 km | ✓ |
| 2 CR | 2,1 km | 2,1 km | ✓ |
| 3 CR | 3,2 km | 3,2 km | ✓ |
| 4 CR | **4,2 km** | **4,3 km** | ✗ einzige Abweichung |
| 5 CR | 5,3 km | 5,3 km | ✓ (passt zu 4,2) |
| 7 CR | 7,5 km | 7,5 km | ✓ |

Entweder ist 4 CR falsch oder 3 CR. Zusätzlich zu klären, ob die Crossrunde nun 1.100 m oder rund 1.070 m misst, sonst widersprechen sich Streckenplan und Zeitplan erneut.

**Kleinere Punkte für den Kollegen**
- Tippfehler „Männlcihe Jugend U20" (Sonntag, Lauf 10).
- Schreibweise „Zeissler SprintCross" im Zeitplan, „BMW ZEISLER" in der Ausschreibung.
- Samstag Lauf 10 bündelt vier Wettbewerbe in einer Zelle (Großer Preis, JedermannCross, TeamCrossStaffel, SchnupperCross).
- Die Mittelstrecken-Läufe am Samstagnachmittag beginnen wieder bei „Lauf 1", das kann mit den Vormittagsläufen verwechselt werden.

## Anforderung: alles muss auch als PDF herunterladbar bleiben

Oskar am 06.08.2026: Athletinnen, Athleten und Trainer wollen die Unterlagen als PDF auf Handy oder Laptop haben, um sie offline und übersichtlich zur Hand zu haben.

**Präzisiert kurz darauf: PDF-Download nur bei Zeitplan und Ausschreibung.** Das sind die Dokumente, die man am Wettkampftag griffbereit braucht. Strecken und Prämien kommen ohne aus, dort reicht die Seite.

Umsetzung: **TEIL 7** im Stylesheet, ein gemeinsamer Download-Knopf (`.wc-dl`) mit Pfeilsymbol, Titel und Dateiangabe. Symbol als SVG-Maske im CSS, also keine externe Datei und kein Icon-Font. Bleibt im Stylesheet stehen, auch solange ihn noch keine Seite nutzt.

- [ ] **Ausschreibung** wird gerade aktualisiert (Stand 06.08.2026). Seite erst danach bauen, **mit** PDF-Download. Aktuelle Datei ist mit 1,8 MB recht schwer fürs Handy, beim Neuerstellen auf Dateigröße achten.
- [ ] **Zeitplan** ebenfalls **mit** PDF-Download. Vorhanden: `Zeitplan_2026.pdf` (81 KB, Stand Mai 2026). Achtung: In der Daily Note vom 28.07. steht, dass im offiziellen Zeitplan die Altersspalte um zwei Zeilen verrutscht ist. Vor dem Einbau prüfen.
- **Strecken und Prämien**: ohne Download.

⚠️ Die Streckenseite verlinkt aktuell `Strecken-2027.pdf` und `Strecken-2027-Seite-2.pdf`. Falsche Jahreszahl (war schon in der SEO-Notiz vom 01.06. vermerkt) und inzwischen auch inhaltlich veraltet. Beide beim Umbau ersetzen.

### Streckenseite neu gebaut (06.08.2026)

Grundlage: **`Strecke 2026 1.pdf`**, vom Kollegen am 06.08.2026 nachgereicht und damit die gültige Fassung. Ersetzt das zwei Stunden ältere `Strecke 2026 aktuelle Version August 2026.jpg`.

**Unterschied zur Vorversion:** drei Startpositionen statt einer (Start 1, 2 und 3) und Pfeile für die Laufrichtung. Rundenlängen unverändert, Cross Runde 1.100 m und Sprint Runde 640 m.

Web-Fassung als `Bilder/weinstadtcross-2026-streckenplan.jpg` (1650 × 1166 px, 132 KB). Zuschnitt automatisch über die Farbsättigung, weil die PDF-Seite unter der Karte viel Leerraum und eine Fußzeile hat. Erster Versuch mit einfachem Weiß-Trimmen scheiterte an dieser Fußzeile.

**Lehre: Bilder unter gleichem Namen ersetzen reicht nicht.** Nach dem Austausch zeigte Chrome weiter das alte Bild, Safari das neue. Ursache war nicht der Dateiname und nicht der Server, die Datei auf dem Server war nachweislich bytegleich mit der neuen (gleiche MD5-Prüfsumme).

Der Server schickt `Cache-Control: max-age=2419200`, also **28 Tage**. Browser, die das alte Bild schon geladen hatten, fragen so lange gar nicht mehr nach.

**Lösung:** an die Bildadresse im HTML eine Versionsnummer hängen, hier `?v=2`. Damit ist es für jeden Browser eine neue Adresse, die Datei auf dem Server bleibt unverändert. Bei jedem weiteren Austausch die Zahl hochzählen. Gilt genauso für die Parkpläne und alle künftigen Bilder.

- [ ] Offen: Welcher Wettbewerb startet an welcher der drei Positionen? Steht nicht im Plan. Auf der Seite steht deshalb nur, dass es vor Ort ausgeschildert und durchgesagt wird. Sobald Oskar die Zuordnung hat, kommt sie in die Tabelle.

Dateien: `Strecken – NUR HTML.txt` (72 Zeilen), Vorschau `Strecken.html`, CSS als **TEIL 6** im Stylesheet.

Inhalt: Streckenplan als Bild, vier Rundenkarten (Crossrunde 1.100 m, Sprinterunde 640 m, Midi 300 m, Mini 150 m) und eine Tabelle, die für jeden der zwölf Wettbewerbe die Rundenzahl und die Distanz zeigt. Die Rundenzahlen stammen aus der Spalte „Runden" im Zeitplan der Ausschreibung, die Rundenlängen aus dem Plan.

**Der neue Plan bestätigt die Streckenfrage:** Crossrunde = 1.100 m, also 6 CR = 6.600 m und 2 CR = 2.200 m. Die 6.400 m und 2.100 m in der Prämientabelle der Ausschreibung sind damit widerlegt.

Kleine Unschärfe, im Hinweiskasten offengelegt: Der Plan nennt die Sprinterunde mit 640 m, der Zeitplan rundet die betroffenen Wettbewerbe auf „ca. 600 m".

### ⚠️ Widersprüchliche Streckenlängen in der Ausschreibung 2026 (06.08.2026)

Beim Auslesen von `2026_Ausschreibung_Volksbank_WeinstadtCross.pdf` gefunden. **Die Datei widerspricht sich selbst.**

| Stelle | Hauptlauf | U18 / U16 |
|---|---|---|
| Prämientabelle in der Ausschreibung | 6.400 m | 2.100 m |
| Zeitplan in derselben Ausschreibung | 6.600 m | 2.200 m |
| Sonderpreis Sport Schwab U16 | – | 2.100 m |
| Zeitplan U16 | – | 2.200 m |
| Prämien-Seite auf der Website (PDF von 2025) | 6.600 m | 2.200 m |

**Der Zeitplan ist mit hoher Wahrscheinlichkeit richtig**, denn er passt zum Rundensystem: Die Streckenkarte nennt Crossrunde 1.100 m, also 6 CR = 6.600 m, 3 CR = 3.300 m, 2 CR = 2.200 m, 1 CR = 1.100 m. Die Spalte „Runden" im Zeitplan bestätigt genau das. Die Werte 6.400 m und 2.100 m passen zu keinem Vielfachen der Runde.

Zusätzlich unterscheiden sich die **Kategorien**: Die Ausschreibung führt U20 mit 6.400 m, die Prämien-Seite führt U20 mit 3.300 m. Die Ausschreibung kennt eine U16-Prämie, die Prämien-Seite nicht.

**Vor dem Livegang klären.** Bis dahin keine Prämienzahlen aus der Ausschreibung übernehmen.

### Prämienseite: PDF durch echte Tabelle ersetzt (06.08.2026)

Dateien: `Praemien – NUR HTML.txt` (40 Zeilen) und `Praemien.html` als Vorschau. Das CSS steht als **TEIL 5** im Stylesheet, der Block bleibt reines HTML.

- Zahlen **nicht** vom Bildschirmfoto abgelesen, sondern die eingebettete PDF-Datei heruntergeladen und mit `firecrawl parse` ausgelesen. 1./2./3. Platz je 120,00 / 80,00 / 50,00 EUR über alle drei Strecken, Hinweistexte wörtlich übernommen.
- Tabelle mit schwarzer Kopfzeile, gelber erster Spalte, Zebra-Trennlinien. Auf schmalen Bildschirmen innerhalb ihres Rahmens seitlich schiebbar, die Seite selbst bricht nicht (geprüft bei 375 px).

⚠️ **Die eingebundene Datei heißt `Praemien_uebersicht_2025.pdf`, stammt also aus 2025.** Vor dem Livegang klären, ob die Prämien für 2026 unverändert gelten.

### TEIL 4: alle Unterseiten (05.08.2026)

Das Stylesheet hat jetzt einen vierten Teil, der die Unterseiten auf denselben Stand hebt. Umfang: Seitenüberschriften schwer und versal mit gelber Linie, Schaltflächen in Markenschwarz statt Grau, Textlinks mit gelber Unterstreichung, mehr Luft um die Sponsorenlogos.

**Ausgenommene Seiten** (bleiben auf Oskars Wunsch unverändert, alles Fremdinhalte):
`page-id-2653` Anmeldung · `page-id-2757` Teilnehmer · `page-id-2753` Ergebnisse · `page-id-2910` Gesamtwertung Cross Cup · `page-id-2502` Ergebnisse Archiv

**Drei Betheme-Hürden, die dabei aufgetaucht sind**
1. **Selektoren brauchen `#Content` davor.** Ohne diesen Zusatz gewinnt Betheme mit spezifischeren eigenen Regeln, selbst gegen `!important`.
2. **Schaltflächenfarbe steht als Inline-Style mit `!important` im Element.** Dagegen kommt kein Stylesheet an. Lösung: `background-image:linear-gradient(...)` legt eine einfarbige Fläche darüber, das ist eine andere Eigenschaft und greift trotzdem.
3. **Bildrahmen (`.image_frame`) lassen sich gar nicht überschreiben,** auch nicht direkt am Element per JavaScript gesetzt. Betheme setzt dort offenbar laufend zurück. Konsequenz: nicht weiter gekämpft, die Logos bekommen nur noch Abstand.

**Diagnose-Lehre:** Ein Fehlschlag sah nach einem Spezifitätsproblem aus, tatsächlich war der lokale Testserver abgestürzt und das CSS kam nie an. **Erst im Netzwerkprotokoll prüfen ob die Datei überhaupt geladen wurde,** bevor man an Selektoren schraubt.

### Zeitplan-Knopf im Hero wieder aktiv (06.08.2026)

Nachdem die Zeitplanseite steht, ist der Knopf zurück im Hero. Ein einziger Knopf, weiß hervorgehoben, Beschriftung „Zum Zeitplan", Ziel `/zeitplan-dm`.

Der Knopf zur Anmeldung bleibt als Kommentar im Block liegen, bis die Anmeldung offen ist. Im Kommentar steht auch der Hinweis, dann beim Zeitplan-Knopf `haupt` durch `neben` zu tauschen, damit die Anmeldung optisch führt.

**Zwei Zeitplan-Seiten im System:** `/zeitplan-dm` (page-id-2988, „Zeitplan DM") trägt den neuen Block und ist im Menü verlinkt. Daneben existiert `/zeitplan` (page-id-2550) mit dem alten `Zeitplan_2026.pdf` von Mai. Die steht in keinem Menü, ist aber erreichbar.
- [ ] Alte Seite `/zeitplan` löschen oder auf `/zeitplan-dm` weiterleiten, sonst kursieren zwei Zeitpläne.

### Schaltflächen im Hero vorerst deaktiviert (05.08.2026)

Auf Oskars Hinweis entfernt, weil die **Anmeldung noch nicht offen** und der **Zeitplan noch nicht aktuell** ist. Tote Links wären schlechter als keine.

Der Knopf-Block steht als HTML-Kommentar im Baustein und lässt sich mit zwei Handgriffen reaktivieren: `style="margin-bottom:0"` beim Untertitel entfernen und die Kommentarzeichen um den Knopf-Block löschen.

**Fehler dabei gemacht:** Im Kommentartext stand die Zeichenfolge zum Beenden eines HTML-Kommentars. Dadurch endete der Kommentar zu früh und die Schaltflächen wären trotzdem sichtbar geworden. **Regel: In HTML-Kommentaren nie die Zeichenfolgen für Kommentaranfang oder Kommentarende als Text verwenden.** Geprüft durch Entfernen aller Kommentare mit Regex und Nachzählen im Browser, jetzt null Links im Hero.

### Hero in HTML und CSS getrennt (05.08.2026)

Beim ersten Einfügen in WordPress war nur der Anfang mit einem Bild zu sehen. Die Zwischenablage war nachweislich vollständig (120 Zeilen, 7278 Zeichen, per `diff` gegen die Datei geprüft, identisch). Ursache lag also in WordPress.

**Wahrscheinlichste Ursachen:** entweder wurde das eingebettete `<style>` vom Editor entfernt, oder der Block landete nicht in einem „Custom HTML"-Block, sondern wurde von Gutenberg in einzelne Blöcke umgewandelt, wobei nur das erste Bild übrig blieb.

**Lösung:** Aufteilung in zwei Teile, damit die Fehlerquelle wegfällt.
- `Hero-Startseite – NUR HTML.txt` (23 Zeilen) enthält **nur Markup**, kein `<style>`.
- Das Aussehen steht als **TEIL 3** in `startseite-redesign.css` und läuft über den Customizer.

**Reihenfolge beim Einbau:** erst das Stylesheet aktualisieren, dann den HTML-Block einsetzen. Andersherum sieht man kurz ungestylte Bilder.

**Merksatz für künftige Bausteine:** Wenn Oskar CSS ohnehin im Customizer pflegt, gehört das Aussehen dorthin und nicht als `<style>` in den Inhalt. Das ist robuster gegen Editor-Filter.

**Entscheidung: Variante A.** `Hero-Startseite.html` und `Hero-Startseite – NUR ZUM KOPIEREN.txt` (120 Zeilen) enthalten jetzt Variante A mit ergänztem `srcset`. Die Gesamtvorschau wurde ebenfalls auf Variante A umgestellt. `Hero-Varianten.html` bleibt als Vergleichsdokument liegen.

### Drittanbieter auf der Startseite (05.08.2026)

Zur Laufzeit werden Ressourcen von diesen fremden Hosts geladen: `fonts.googleapis.com`, `www.google-analytics.com`, `www.youtube.com`, `s.w.org`. Im reinen HTML-Quelltext sieht man das nicht, die Aufrufe entstehen erst über CSS und JavaScript.

Vor allem Google Analytics und die Google Fonts sind ohne Einwilligung heikel. Für eine Vereinsseite in Deutschland wäre sinnvoll: Fonts lokal ausliefern, Analytics prüfen oder ersetzen, YouTube als Zwei-Klick-Lösung einbinden.

## Lehre: HTML-Bausteine immer in reinem ASCII (05.08.2026)

Beim ersten Einfügen in WordPress kamen alle Umlaute als Zeichensalat an: `ä` wurde zu `√§`, `ü` zu `√º`, der Pfeil zu `,Üí`. Das ist UTF-8, das als Mac Roman gelesen wurde. Ursache war nicht WordPress, die Seite liefert sauber `charset=UTF-8`, sondern der Kopierweg über eine `.txt`-Datei ohne Zeichensatz-Angabe.

**Konsequenz für alle künftigen Bausteine:** Nicht-ASCII-Zeichen vermeiden.
- Im HTML-Teil benannte Entities nutzen: `&auml; &ouml; &uuml; &Uuml; &szlig; &rarr; &middot; &ndash;`
- Im `<style>`-Block stattdessen transliterieren (`ue`, `ae`, `ss`), weil CSS keine HTML-Entities auflöst. Betrifft nur Kommentare.
- Danach prüfen: `LC_ALL=C grep -c '[^ -~\t]' datei.txt` muss 0 ergeben.

Skript dafür: `.scripts/`-fähig, aktuell im Scratchpad als `ascii_fix.py`.

## Offen / Nächste Schritte
- [ ] Neue Version ansehen und Feedback (Datei doppelklicken oder Preview)
- [ ] Entscheidung: Weg 1 → 2 (Hybrid) oder Weg 3 (voll statisch)
- [ ] FTP-Zugangsdaten zum Webspace bereitlegen für Test-Upload
- [ ] Bei Startseiten-Wechsel: Google Search Console prüfen lassen (siehe [[WeinstadtCross – SEO-Optimierung]])
