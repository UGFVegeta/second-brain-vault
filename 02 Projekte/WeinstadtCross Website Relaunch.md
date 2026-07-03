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

## Offen / Nächste Schritte
- [ ] Neue Version ansehen und Feedback (Datei doppelklicken oder Preview)
- [ ] Entscheidung: Weg 1 → 2 (Hybrid) oder Weg 3 (voll statisch)
- [ ] FTP-Zugangsdaten zum Webspace bereitlegen für Test-Upload
- [ ] Bei Startseiten-Wechsel: Google Search Console prüfen lassen (siehe [[WeinstadtCross – SEO-Optimierung]])
