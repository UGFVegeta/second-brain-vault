---
title: WeinstadtCross – SEO-Optimierung
tags:
  - web
  - seo
  - wordpress
  - projekt
erstellt: 2026-06-01
status: bereit zur Umsetzung
url: https://weinstadtcross.de
---

# WeinstadtCross – SEO-Optimierung

Optimierte Texte und technische Snippets für [weinstadtcross.de](https://weinstadtcross.de), basierend auf der Website-Analyse vom 01.06.2026.

> [!tip] Wie umsetzen?
> WordPress-Admin → SEO-Plugin (Yoast SEO oder RankMath) → Startseite bearbeiten → Felder eintragen.
> Das Schema.org-Snippet kommt in: **Yoast → Schema** oder per Plugin „Code Snippets" in den `<head>`.

---

## 1. Seitentitel (Title Tag)

> [!success] Empfehlung – Startseite
> ```
> 11. Volksbank WeinstadtCross | DM Crosslauf 28.–29. Nov. 2026 – Weinstadt
> ```
> **Zeichen:** 71 · **Warum:** Enthält Jahreszahl, das Highlight „DM", Datum und Ort – alles was ein Suchender braucht.

> [!example] Alternative (kürzer, für mobile)
> ```
> WeinstadtCross 2026 – Deutsche Crosslauf-Meisterschaft in Weinstadt
> ```

---

## 2. Meta-Description

> [!danger] Aktuell (sofort ersetzen!)
> ```
> Just another WordPress site
> ```

> [!success] Empfehlung
> ```
> Der WeinstadtCross wird 11! Am 28. & 29. November 2026 in Weinstadt – mit JedermannCross, Schulmeisterschaften und der Deutschen Crosslauf-Meisterschaft. Jetzt informieren!
> ```
> **Zeichen:** 158 · **Limit:** 160

---

## 3. Open Graph Tags

In WordPress via Yoast SEO automatisch gesetzt, sobald Titel + Description eingetragen sind. Zusätzlich folgendes Bild hinterlegen:

```
Yoast SEO → Social → Facebook/Twitter → Bild hochladen
Empfohlene Größe: 1200 × 630 px
Motiv: Starterfeld oder Logo + Datum auf weißem/farbigem Hintergrund
```

Manuell (falls kein Plugin) in `functions.php` oder `header.php`:

```html
<meta property="og:title"       content="11. Volksbank WeinstadtCross | DM Crosslauf 28.–29. Nov. 2026" />
<meta property="og:description" content="Crosslauf in Weinstadt mit JedermannCross & Deutscher Meisterschaft am 28./29. November 2026. Alle Infos und Anmeldung auf weinstadtcross.de" />
<meta property="og:image"       content="https://weinstadtcross.de/wp-content/uploads/[DEIN-BILD].jpg" />
<meta property="og:url"         content="https://weinstadtcross.de/" />
<meta property="og:type"        content="website" />
<meta name="twitter:card"       content="summary_large_image" />
```

---

## 4. Schema.org Event-Markup (JSON-LD)

Dieses Snippet sorgt dafür, dass Google das Event als **Rich Result** anzeigt (mit Datum, Ort, Typ direkt in der Suche).

**Einfügen über:** WordPress-Plugin „[Code Snippets](https://wordpress.org/plugins/code-snippets/)" → Typ: HTML → Hook: `wp_head` → nur auf Startseite.

```html
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "SportsEvent",
    "name": "11. Volksbank WeinstadtCross – JedermannCross & Schulmeisterschaften",
    "description": "Crosslauf-Veranstaltung in Weinstadt mit JedermannCross, Schulmeisterschaften sowie Kinder- und Jugendläufen.",
    "startDate": "2026-11-28",
    "endDate": "2026-11-28",
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "sport": "Crosslauf",
    "url": "https://weinstadtcross.de",
    "location": {
      "@type": "Place",
      "name": "Weinstadt",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Weinstadt",
        "addressRegion": "Baden-Württemberg",
        "addressCountry": "DE"
      }
    },
    "organizer": {
      "@type": "Organization",
      "name": "Volksbank WeinstadtCross Team",
      "url": "https://weinstadtcross.de"
    },
    "image": "https://weinstadtcross.de/wp-content/uploads/2025/12/Untitled-1.png"
  },
  {
    "@context": "https://schema.org",
    "@type": "SportsEvent",
    "name": "11. Volksbank WeinstadtCross – Deutsche Crosslauf-Meisterschaft 2026",
    "description": "Deutsche Crosslauf-Meisterschaften in Weinstadt. Leichtathletinnen und Leichtathleten aus ganz Deutschland ermitteln die Deutschen Crossmeister 2026.",
    "startDate": "2026-11-29",
    "endDate": "2026-11-29",
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "sport": "Crosslauf",
    "url": "https://weinstadtcross.de",
    "location": {
      "@type": "Place",
      "name": "Weinstadt",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Weinstadt",
        "addressRegion": "Baden-Württemberg",
        "addressCountry": "DE"
      }
    },
    "organizer": {
      "@type": "Organization",
      "name": "Volksbank WeinstadtCross Team",
      "url": "https://weinstadtcross.de"
    },
    "image": "https://weinstadtcross.de/wp-content/uploads/2025/12/Untitled-1.png"
  }
]
</script>
```

> [!warning] Anpassen!
> - `location.name` → genauen Veranstaltungsort eintragen (z. B. „Strümpfelbach, Weinstadt")
> - `image` → URL zum besten Event-Foto ersetzen
> - Anmeldungs-URL ergänzen mit `"offers": {"@type": "Offer", "url": "https://weinstadtcross.de/anmeldung"}`

---

## 5. WordPress-Sicherheit (Quickfixes)

> [!bug] xmlrpc.php deaktivieren
> In `functions.php` des Themes (oder per Plugin „Disable XML-RPC"):
> ```php
> add_filter('xmlrpc_enabled', '__return_false');
> ```

> [!bug] PHP-Version verstecken
> In `.htaccess` hinzufügen:
> ```apache
> Header unset X-Powered-By
> ```
> Oder in `php.ini`: `expose_php = Off`

---

## 6. Umsetzungs-Checkliste

- [ ] SEO-Plugin installieren (Yoast SEO oder RankMath)
- [ ] **Meta-Description** auf Startseite eingetragen
- [ ] **Seitentitel** optimiert
- [ ] Open Graph Bild (1200×630 px) hochgeladen und hinterlegt
- [ ] **Schema.org JSON-LD** Snippet eingefügt (Ort + Bild angepasst)
- [ ] PDF-Dateinamen korrigiert („Strecken 2026" statt „2027")
- [ ] xmlrpc.php deaktiviert
- [ ] X-Powered-By Header entfernt
- [ ] Anmeldelink prominent auf Startseite (Hero-Bereich)
- [ ] Google Search Console → URL prüfen lassen nach Änderungen
