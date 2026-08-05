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
- [ ] Übernachtungsmöglichkeiten werden ein **eigener Reiter** (Quelle: `DM Cross - Übernachtungsmöglichkeiten.pdf`, 6 Hotels, 3 Ferienwohnungen, 7 Wohnmobilstellplätze). Im selben Design noch zu bauen.

## Offen / Nächste Schritte
- [ ] Neue Version ansehen und Feedback (Datei doppelklicken oder Preview)
- [ ] Entscheidung: Weg 1 → 2 (Hybrid) oder Weg 3 (voll statisch)
- [ ] FTP-Zugangsdaten zum Webspace bereitlegen für Test-Upload
- [ ] Bei Startseiten-Wechsel: Google Search Console prüfen lassen (siehe [[WeinstadtCross – SEO-Optimierung]])
