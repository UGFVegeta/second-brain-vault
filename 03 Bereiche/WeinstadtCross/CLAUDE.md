# WeinstadtCross: Anleitung für Claude

Volksbank WeinstadtCross, Crosslauf, dieses Jahr mit Deutscher Meisterschaft im November 2026. Oskar pflegt Website und Postfach allein. Projektnotizen liegen in `02 Projekte/`: [[WeinstadtCross Website Relaunch]], [[WeinstadtCross Website ohne WordPress]]. SEO: [[WeinstadtCross – SEO-Optimierung]] im Vault-Wurzelordner.

## Website
- Live-Seite: weinstadtcross.de (WordPress mit Betheme/Muffin). Bis nach dem Wettkampf im November 2026 nichts umbauen oder umziehen. Umstellung auf eine statische Seite frühestens Dezember 2026/Januar 2027.
- Die neue Startseite (HTML-Datei in iCloud `Homepage WeinstadtCross/2026/`) ist Master, Änderungen mit Claude, dann neu hochladen.

## News-Beiträge (feste Regeln)
- Kein Fließtext, nur Titel und Bildergalerie.
- Drei Spalten (`one-third`), Bilder gestapelt, als HTML/Text-Element mit den Theme-Klassen `mcb-wrap`, `column_image`, `image_frame`, `scale-with-grid`, nicht über den nativen Bild-Baustein.
- Bilder vorher auf 1080 px Breite verkleinern, JPEG Qualität etwa 82, Dateiname `weinstadtcross-2026-<kurzbeschreibung>.jpg`.
- Alle Zeichen außerhalb ASCII im HTML-Block als Entity kodieren (`&#252;` statt `ü`).
- Das gewählte Beitragsbild kommt nicht zusätzlich in den Block, sonst erscheint es doppelt.
- Fertigen Block per `pbcopy` in die Zwischenablage und als Datei in `07 Anhänge/` ablegen, Ablageort nennen.

## Postfach info@weinstadtcross.de
Zugang: `~/.config/claude-mail/weinstadtcross.env` (IONOS-IMAP). Es kommen hier nie echte Rechnungen an, alles mit „Rechnung“, „Zahlungsbeleg“, „Vertragsbestätigung“ ist Phishing.
- Anmeldebestätigungen („Deine Anmeldung zum Volksbank WeinstadtCross“) in den Ordner Anmeldungen.
- Bounces, Mailer-Daemon, täglicher Spambericht, Phishing in den Papierkorb, nie endgültig löschen.
- Im Posteingang bleiben echte Teilnehmerfragen und Mails von Schulen.
- Nie antworten oder senden ohne Freigabe.

## Datenschutz
Keine Teilnehmernamen oder Kontaktdaten in Notizen.

## Gelernt
Siehe [[Gelernt]].
