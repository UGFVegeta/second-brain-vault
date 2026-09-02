---
tags: [ressource, technik, email, imap]
date: 2026-06-20
---

# E-Mail Anbindung per IMAP (web.de & Gmail)

Claude kann Oskars Postfächer per IMAP lesen und sortieren. Eingerichtet am 2026-06-20. Zweck: Vorsortierung (wichtig/unwichtig/Werbung), schnelles Aufräumen, Suche. **Nie automatisch beantworten oder ohne ausdrückliche Freigabe senden.**

## Sichere Ablage der Zugangsdaten

Außerhalb des Vaults, nur lokal, mit Rechten 600:

- web.de: `~/.config/claude-mail/web-de.env`
- Gmail: `~/.config/claude-mail/gmail.env`
- WeinstadtCross: `~/.config/claude-mail/weinstadtcross.env` (angelegt 28.08.2026)
- Leseskript (nur lesend): `~/.config/claude-mail/triage.py`

Aufruf Übersicht (nur lesend):
```
python3 ~/.config/claude-mail/triage.py 30 ~/.config/claude-mail/web-de.env
python3 ~/.config/claude-mail/triage.py 30 ~/.config/claude-mail/gmail.env
python3 ~/.config/claude-mail/triage.py 30 ~/.config/claude-mail/weinstadtcross.env
```

## Serverdaten

- **web.de:** `imap.web.de:993` (SSL). App-Passwort über web.de → Account verwalten → Login & Sicherheit → Anwendungsspezifische Passwörter.
- **Gmail:** `imap.gmail.com:993` (SSL). App-Passwort über `myaccount.google.com/apppasswords` (setzt aktive Zwei-Faktor-Anmeldung voraus). Konto: oskar17185@googlemail.com.
- **info@weinstadtcross.de:** `imap.ionos.de:993` (SSL), Postausgang `smtp.ionos.de:465`. Liegt bei IONOS, demselben Anbieter wie der Webspace. Benutzername ist die vollständige Adresse. Bei aktiver Zwei-Faktor-Anmeldung braucht es ein App-Passwort aus dem IONOS-Kundenkonto.

## info@weinstadtcross.de: erst prüfen, ob es ein Postfach ist

⚠️ Die Adresse leitet an **oskarklein@web.de** und an **juergen.illg@t-online.de** weiter. Ob daneben ein echtes Postfach existiert, war am 28.08.2026 nicht geklärt. Ist es nur eine Weiterleitung, gibt es nichts zum Anmelden und die Post liegt ohnehin im web.de-Konto. Nachsehen im IONOS-Kundenkonto unter E-Mail.

**Die Weiterleitung an T-Online funktioniert nicht.** IONOS leitet über `mout-xforward.kundenserver.de` (82.165.159.10) weiter, diese IP steht auf der Spamhaus-Sperrliste, T-Online lehnt mit `554 ... (TEM)` ab. Jürgen bekommt dadurch weder Spam noch echte Anfragen, und die Rückläufer landen über die Weiterleitung bei Oskar. Die Weiterleitung an web.de funktioniert dagegen einwandfrei (getestet).

Sinnvolle Abhilfen: Spamfilter bei IONOS so einstellen, dass als Spam erkannte Post nicht weitergeleitet wird (das spart die meisten Rückläufer), und für Jürgen eine Adresse außerhalb von T-Online verwenden oder das Postfach direkt abrufen lassen.

⚠️ An `info@weinstadtcross.de` kommt regelmäßig **Phishing**, das IONOS imitiert. Erkennungsmerkmale aus den Fällen vom 28.08.2026: der Markenname wird als `lΟNΟS` geschrieben (kleines L statt großem i, griechische Omikron), Wörter enthalten unsichtbare Steuerzeichen oder Zeichen aus fremden Schriftsystemen (Lisu, Kyrillisch), erfundene Rechtsgrundlagen wie „NIS2 Artikel 28 verlangt Bestätigung binnen 2 Tagen", widersprüchliche Rechnungsnummern, und das echte IONOS-Impressum als Tarnung. Nie über Links aus solchen Mails handeln, sondern `ionos.de` selbst eintippen.

## Wichtige Lehren

### Gmail-Passwort
Das 16-stellige App-Passwort wird mit Leerzeichen angezeigt. Beim Kopieren rutschen geschützte Leerzeichen (`\xa0`) rein. Im Skript werden alle Leerzeichen automatisch entfernt.

### Löschen: web.de vs. Gmail (zentral!)
- **web.de:** unkritisch. COPY in `Papierkorb` + `STORE \Deleted` + `EXPUNGE` funktioniert sauber.
- **Gmail:** NICHT so machen. `STORE \Deleted` + `EXPUNGE` archiviert dort (Gmail-Default) statt zu löschen, und in Kombination mit laufenden Sequenznummern erwischt es die falschen Mails. Am 2026-06-20 dadurch ~4.000 Mails versehentlich archiviert. Komplett rückgängig gemacht, nichts verloren.

**Korrekte Gmail-Methode (getestet, sauber):**
1. Immer mit **UIDs** arbeiten, nie mit laufenden Sequenznummern.
2. Verschieben in den Papierkorb = `UID COPY` ins Trash-Label `[Gmail]/Papierkorb`. **Kein** `\Deleted`/`EXPUNGE`. Das Trash-Label ist exklusiv und entfernt damit automatisch den Inbox-Eintrag.
3. Suche zuverlässig über `X-GM-RAW` (Gmail-Syntax, z.B. `from:absender in:inbox`), nicht über die normale IMAP-Suche (die untertreibt bei Gmail).
4. Vor Masse: Testlauf mit einem Absender, Zahlen vorher/nachher prüfen plus Kontrollabsender.

### Wiederherstellen (Gmail)
Label `INBOX` wieder setzen per `UID COPY` nach `INBOX`, Quelle `[Gmail]/Papierkorb` und `[Gmail]/Alle Nachrichten` (mit `-in:inbox -in:sent -in:draft -in:chats`).

## Ordnerstruktur

- web.de Papierkorb: `Papierkorb`. Neuer Ordner `Finanzen` angelegt für PayPal/ING/IONOS/Apple/congstar.
- Gmail Papierkorb: `[Gmail]/Papierkorb`, Archiv: `[Gmail]/Alle Nachrichten`.
