# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primärer und einziger direkter Nutzer der Oberflächen ist Oskar Klein, Realschullehrer für Physik, Mathematik und Sport in Baden-Württemberg. Er bedient die Werkzeuge allein am eigenen Mac, in der Vorbereitung und in der Auswertung.

Schüler sind Nutznießer, nicht Bedienende. Sie sehen die Oberflächen nicht. Was bei ihnen ankommt, ist die Ausgabe: Ausdrucke, PDFs, Aufgabenblätter. Das ist im Interview am 17.08.2026 ausdrücklich bestätigt worden, nachdem die erste Antwort noch auf Schüler als Zielgruppe gedeutet hatte.

Kollegen sind gelegentliche Zweitnutzer einzelner Werkzeuge, etwa der Notenschlüsselrechner. Nicht bestätigt ist, ob das regelmäßig vorkommt.

## Product Purpose

Eine Sammlung eigenständiger HTML-Werkzeuge im Second-Brain-Vault, die Oskars Unterrichtsvorbereitung, seine Auswertungen und sein persönliches Kennzahlen-Tracking übernehmen. Jede Datei löst genau eine Aufgabe und läuft ohne Server, ohne Login und ohne Internetverbindung.

Erfolg heißt: Oskar öffnet die Datei per Doppelklick, findet in Sekunden die Zahl oder die Aufgabe, die er sucht, und druckt bei Bedarf ein Blatt aus, das ohne Nacharbeit vor eine Klasse kann.

## Positioning

Der Unterschied zu fertiger Schulsoftware ist, dass die Werkzeuge Oskars eigenen Verfahren folgen statt umgekehrt. Der Notenschlüssel rechnet nach der Regelung in Baden-Württemberg, der Aufgabenpool folgt dem Stil der mündlichen Realschulprüfung, die Physik-Materialien folgen seinen eigenen Diagrammkonventionen. Nichts davon ließe sich mit einem Standardprodukt abbilden, ohne den Ablauf anzupassen.

Zweiter Punkt: die Dateien gehören ihm. Kein Abo, kein Anbieter, der abschaltet, keine Schülerdaten in fremder Hand.

## Operating Context

Alles läuft lokal auf Oskars Mac im Browser, geöffnet per Doppelklick oder über `.command`-Dateien. Kein Beamer, keine Schülertablets, kein Handy als bestätigter Einsatzort.

Zwei Ausgabewege sind gleich wichtig. Am Bildschirm arbeitet Oskar selbst, dort zählt Informationsdichte und schnelles Finden. Auf Papier landet das Ergebnis bei den Schülern, dort zählt Lesbarkeit im Schwarzweißdruck, saubere Seitenumbrüche und dass nichts abgeschnitten wird. Über zwanzig bestehende Dateien haben bereits eigene `@media print`-Regeln, unter anderem alle drei Notenschlüsselrechner, der Physik-MC-Generator und der gesamte Mathe-Aufgabenpool.

Einige Dashboards lesen ihre Daten aus benachbarten JavaScript-Dateien, die von Python-Skripten erzeugt werden, etwa `leben_data.js` und `wissenskarte_data.js`. Ein LaunchAgent aktualisiert das morgens um 6:30 Uhr.

Der Vault ist gleichzeitig ein Obsidian-Vault. Dateien im Root tauchen dort im Dateibaum auf.

## Capabilities and Constraints

Jede Oberfläche ist eine einzelne HTML-Datei mit eingebettetem CSS und JavaScript, ohne Build-Schritt. Das bleibt so. Ein Werkzeug muss über `file://` funktionieren, deshalb sind ES-Module-Importe, `fetch` auf lokale Dateien und alles, was einen Server braucht, ausgeschlossen.

Keine externen CDNs für die Vault-Werkzeuge. Schriften, Icons und Bibliotheken müssen eingebettet oder durch Systemmittel ersetzt sein, sonst ist die Datei ohne Internet kaputt. Aktuell nutzen alle Dateien den System-Schriftstapel, keine einzige lädt eine Webschrift.

Datenabhängige Dashboards müssen einen brauchbaren Zustand zeigen, wenn die Datendatei fehlt oder veraltet ist. Die Wissenskarte macht das bereits mit einem Hinweistext.

Bestehender Stand ohne gemeinsames System: die Werkzeuge funktionieren, folgen aber jeweils eigenen Paletten. Physik-Dashboard in Gold und Blaugrau, Lebens-Dashboard dunkelblau mit Violett und Türkis, Lese-Dashboard blau, Notenschlüsselrechner neutrales Grau. Sechs Dateien unterstützen `prefers-color-scheme`, der Rest nicht.

Umfang des Systems sind die Unterrichtswerkzeuge und die persönlichen Dashboards im Vault. Das Mietverwaltungs-Paket unter `02 Projekte/Mietverwaltung/` und die WeinstadtCross-Website in iCloud sind ausdrücklich nicht Teil davon, sie bekommen eigene Kontexte.

## Brand Commitments

Keine. Die Werkzeuge treten unter keinem Namen und keiner Marke auf, sie sind Arbeitsgerät. Oskars Schreibstil für Texte ist in `00 Kontext/Schreibstil.md` festgehalten und gilt auch für Beschriftungen und Fehlermeldungen, insbesondere keine Gedankenstriche.

Für Physik-Darstellungen gelten feste fachliche Konventionen aus `00 Kontext/Physik-Diagramme Konventionen.md`. Die sind inhaltlich bindend und nicht verhandelbar, auch nicht aus gestalterischen Gründen.

## Evidence on Hand

Vorhandene, echte Werkzeuge als Ausgangsmaterial: Lebens-Dashboard, Lese-Dashboard, Wissenskarte, Physik Dashboard Klasse 7, drei Notenschlüsselrechner, der Mathe-Aufgabenpool mit Baukasten und Prüfungsarchiv, der Physik-MC-Generator, Wettkampf-Dashboards für Triathlon, Staffellauf-Startzeiten, Parabeln-Seite und zwei Physik-Erklärseiten.

Nicht vorhanden und nicht zu erfinden: Nutzerzahlen, Rückmeldungen von Kollegen, Wirksamkeitsnachweise im Unterricht, Testimonials. Es gibt bislang keine Erhebung dazu, wie gut die Werkzeuge ankommen.

Personenbezogene Schülerdaten dürfen in keinem Werkzeug und in keinem Beispiel auftauchen. Das ist eine harte Vault-Regel, keine Empfehlung.

## Product Principles

Ein Werkzeug, eine Aufgabe. Lieber eine weitere Datei als ein Dashboard, das alles kann.

Bildschirm und Papier sind zwei gleichwertige Ausgaben. Eine Gestaltung, die nur am Monitor funktioniert, ist unfertig.

Ohne Netz lauffähig. Alles Nötige steckt in der Datei.

Der Ablauf folgt Oskars Verfahren, nicht dem Standard eines fremden Produkts.

Dichte vor Dekoration. Die Werkzeuge sind Arbeitsgerät für einen Menschen, der weiß, was er sucht.

## Accessibility & Inclusion

Kein produktspezifischer Standard festgelegt. Aus dem Druckweg ergibt sich als harte Anforderung, dass Information nie allein über Farbe transportiert werden darf, weil vieles schwarzweiß auf Papier landet.
