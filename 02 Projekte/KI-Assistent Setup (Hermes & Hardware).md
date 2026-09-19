---
tags: [projekt, idee, ki, hardware, hermes, datenschutz]
status: idee
date: 2026-06-21
---

# KI-Assistent Setup (Hermes & Hardware)

> [!note] Status
> Idee / Planung – noch keine Anschaffung. Festgehalten am 2026-06-21.

## Ziel

Ein persönlicher KI-Assistent, den ich auch **vom Handy** erreichen kann, plus eine **datenschutzsichere Variante** für Schulisches, bei der keine Daten die eigene Hardware verlassen.

## Zielbild (Zwei-Wege-Lösung)

1. **Mac mini als Dauerläufer (immer an)** + Cloud-Modell (Claude / Gemini / Nous Portal)
   - Für Handy-Zugriff von überall über Hermes Messaging-Gateway
   - Nur für **Privates und Unkritisches**: Auto, Verträge, Haushalt, Triathlon-Orga, E-Mail-Aufräumen
   - Achtung: Cloud = nicht privat. Hier bewusst **nichts Schulisches**.
2. **Neues MacBook mit 48 GB RAM** + lokales Modell
   - Für **Schule und Datenschutzkritisches**, nur am Schreibtisch genutzt
   - Daten bleiben auf dem Gerät, nichts geht in die Cloud
   - Über das Handy wird **bewusst kein Schul-Kram** gemacht → Trennung sauber

Diese Aufteilung passt zur Vault-Regel: keine Schülerdaten in die Cloud.

## Wichtige Erkenntnisse

- **Begrenzender Faktor lokal = RAM**, nicht der Chip. Aktueller M1/8 GB reicht NICHT für ein brauchbares lokales Modell.
- 32 GB → Modelle bis ~27-32B (Q4). 48 GB → bequem 32B, knapp auch 70B (Q4).
- Wenn ich lokal-privat auch **vom Handy** bräuchte, müsste der RAM in den Dauerläufer (Mac mini/Studio mit viel RAM). Da ich Schulisches nur am Schreibtisch mache, ist das **nicht nötig**.
- Mögliche Vereinfachung: Statt zwei neuer Geräte ein einzelner gut ausgestatteter Dauerläufer (Mac mini/Studio 32-64 GB), der beides kann. M1-MacBook bleibt normaler Laptop.

## Lokales Modell vs. Claude (Leistung)

- **Routine** (sortieren, zusammenfassen, einfache Entwürfe, Daten strukturieren): lokales 32-70B-Modell solide, kaum Unterschied.
- **Anspruchsvoll** (feines Deutsch, Konrektor-Bewerbung, heikle Elternmails, komplexe Analysen): Claude klar besser. Lokale Modelle schreiben etwas hölzerneres Deutsch.
- Grobe Einordnung: starkes lokales 70B ≈ vorletzte Spitzengeneration, spürbar unter aktuellem Claude Opus.
- Fürs Schul-Arbeitspferd reicht lokal gut für **Entwürfe zum Feinschleifen**. Abstand schrumpft über die Jahre.

## Hermes Agent (das Werkzeug dahinter)

- Open-Source, selbst gehostet, Daten bleiben lokal (siehe [[04 Ressourcen/E-Mail Anbindung/E-Mail Anbindung per IMAP.md]] für die bisherige E-Mail-Anbindung).
- Handy-Zugriff über Messaging-Gateway: Telegram, WhatsApp, **Signal** (am privatesten), SMS, iMessage, E-Mail.
- Modell-agnostisch: kann Claude (Anthropic), Gemini, lokale Modelle (über Ollama/LM Studio/llama.cpp/MLX) u.v.m. nutzen, umschaltbar per `hermes model`.
- Liest `CLAUDE.md`, hat eigenes Gedächtnis (`MEMORY.md`, `USER.md`), Skills, Cron-Routinen, MCP-Anbindung.
- Im Juni noch frühe Version (0.x). Stand 19.09.2026 sehr aktiv entwickelt, inzwischen mit datierten Releases (v2026.9.14 vom 14.09.2026). Ob die Ecken und Kanten weg sind, zeigt erst ein Test.

## Weitere Kandidaten für den Dauerläufer

Aus dem Video „15 Open-Source-Tools, die deine teuren Abos ersetzen" von Julian Ivanov (18.09.2026), durchgesehen am 19.09.2026.

- Paperless-ngx läuft schon auf dem Raspberry Pi und bleibt dort. Der Mac mini bringt etwas anderes dazu: Seit Version 3.0 (22.07.2026) hat Paperless eigene KI-Funktionen, also Vorschläge für Titel, Schlagworte und Absender und einen Chat über die eigenen Dokumente. Das Modell dafür muss nicht auf dem Pi laufen. In der Konfiguration lässt sich ein Ollama-Endpunkt auf einem anderen Rechner eintragen (`PAPERLESS_AI_LLM_BACKEND=ollama`, `PAPERLESS_AI_LLM_ENDPOINT`, dazu das Embedding-Backend). Damit bleibt der Pi das Archiv und der Mac mini rechnet, die Dokumente verlassen das Haus nicht. Voraussetzung: Paperless auf dem Pi mindestens auf 3.0. https://github.com/paperless-ngx/paperless-ngx
  - Stand Pi am 19.09.2026 (per SSH geprüft): Raspberry Pi 5 mit 8 GB RAM, Debian 12, läuft auf der 128-GB-SD-Karte (14 % belegt), keine SSD. Paperless-ngx **2.20.15** in Docker, Image vom April 2026, also noch vor 3.0. 412 Dokumente, rund 870 MB. Es gibt einen Export-Ordner (Stand 12.07.2026), der liegt aber auf derselben SD-Karte. Einen automatischen Backup-Job oder ein externes Laufwerk habe ich nicht gefunden.
  - Update am 19.09.2026: Vorher vollständiges Backup (Export-Zip, Datenbank-Dump, Konfiguration) auf den Mac nach `~/Backups/Paperless-Pi/2026-09-19/` kopiert und geprüft. Danach Paperless auf **3.1.3** aktualisiert, bewusst nicht auf das am selben Tag erschienene 3.2.0. Dabei `PAPERLESS_DBENGINE: postgresql` ergänzt, Gotenberg auf 8.34 und Tika auf 3.3.1.0 festgelegt, eine alte Collation-Warnung der Datenbank behoben. Alle 412 Dokumente da, Suchindex neu aufgebaut. Die alte Compose-Datei liegt als `docker-compose.yml.bak-2.20.15` daneben.
  - Ebenfalls am 19.09.2026: AdGuard Home v0.107.79 als Docker-Container auf dem Pi installiert (`/home/ugfvegeta/adguardhome`, Host-Netz, IP 192.168.178.68).
- Open WebUI, eine Chat-Oberfläche vor einem lokalen Modell, mit Dokumentensuche und Fundstellen in der Antwort. Erst sinnvoll mit einem Rechner, der lokale Modelle stemmt. Für Einzelnutzung reicht eventuell LM Studio. https://github.com/open-webui/open-webui
- Stirling PDF entfällt, PDF Expert läuft schon auf Mac, iPad und iPhone.

Einrichtung: Claude Code kann sich per SSH mit dem Mac mini (und dem Pi) verbinden und die Dienste dort aufsetzen (Tipp aus dem Video). Den gemieteten Server, den das Video empfiehlt, braucht es dafür nicht. Mit dem Mac mini zu Hause bleiben die Daten im Haus, und es fallen keine Monatskosten an.

Für den privaten Bereich nicht übernommen: Nextcloud (am 01.06.2026 für iCloud mit erweitertem Datenschutz entschieden) und Vaultwarden (ein selbst gehosteter Passwort-Tresor ist das falsche Risiko). Die Firmenwerkzeuge aus dem Video (n8n, Postiz, Supabase, Invoice Ninja, Cal.com) gehören thematisch zu [[Alternatives Einkommen]]. Falls dort etwas davon gebraucht wird, läuft es ebenfalls auf dem Mac mini.

## Mac mini 2026 und passende Modelle (Stand 19.09.2026)

Apple hat am 25.08.2026 den neuen Mac mini vorgestellt, Auslieferung ab 22.09.2026. Laut apple.com/mac-mini/specs:

| Chip | Arbeitsspeicher | Speicherbandbreite |
|---|---|---|
| M6 | 16 GB, konfigurierbar auf 24 oder 32 GB | 153 GB/s (16 GB), 170 GB/s (24/32 GB) |
| M5 Pro | 24 GB, konfigurierbar auf 48 oder 64 GB | 307 GB/s |

Der Speicher lässt sich später nicht aufrüsten. Die Bandbreite bestimmt, wie schnell ein lokales Modell schreibt. Der M5 Pro ist damit bei gleichem Modell grob 1,8-mal so schnell wie der M6.

Modellkandidaten aus der Ollama-Bibliothek (Größen laut ollama.com, Stand 19.09.2026):
- Qwen3.6 27B (18 GB) und Qwen3.8 (18 GB): stark bei Denken, Werkzeugnutzung und Agentenaufgaben.
- Gemma 4 26B (19 GB) bzw. 31B (20 GB), kleiner 12B (7,6 GB): Google, multimodal.
- gpt-oss 20B (14 GB) als schnelle Variante.
- Qwen3-Embedding 0,6B (0,6 GB) für die Dokumentensuche in Paperless AI.
- Nicht mehr in 64 GB: gpt-oss 120B (65 GB), Mistral Medium 3.5 (80 GB).

Welches davon besser Deutsch schreibt, ist ungeprüft. Nach der Anschaffung mit echten eigenen Aufgaben vergleichen.

Einschätzung: Mit 32 GB (M6) passt ein Modell der 27B-Klasse, aber nur eins zur Zeit und ohne viel Luft. 64 GB (M5 Pro) bringen keine größere Modellklasse, aber Tempo, Platz für mehrere Dienste gleichzeitig (Hermes, Paperless AI, Chat) und längere Dokumente. Damit könnte der M5 Pro mit 64 GB beide Geräte aus dem Zielbild ersetzen.

## Offene Punkte / Nächste Schritte

- Entscheiden: zwei Geräte (Mac mini + neues MacBook 48 GB) oder ein starker Dauerläufer? Empfehlung von Claude am 19.09.2026: ein Mac mini M5 Pro mit 64 GB, noch nicht entschieden.
- Bei Anschaffung: Hermes testweise auf einem Gerät aufsetzen, erst mit Cloud-Modell, dann lokal.
- Messaging-Kanal wählen (Signal bevorzugt).
- Realistische Kosten gegenüberstellen (Hardware + ggf. Claude Max / Nous Portal Abo).
- Pi: automatisches Backup außerhalb der SD-Karte einrichten. Bisher gibt es nur die einmalige Sicherung vom 19.09.2026 auf dem Mac. SSH-Zugang für Claude Code steht seit 19.09.2026 (`ugfvegeta@raspberrypi.local`).
- AdGuard Home: Assistent erledigt, Weboberfläche unter http://192.168.178.68. In der Fritzbox feste IP für den Pi und `192.168.178.68` als lokaler DNS-Server (IPv4) eingetragen (19.09.2026). `fritz.box` und Gerätenamen löst AdGuard über die Fritzbox auf. Lokaler DNSv6-Server in der Fritzbox ist ebenfalls der Pi (`fdfe:bdd8:3b4f:0:cd03:6553:adc3:26e9`), sonst fragen Geräte per IPv6 an AdGuard vorbei. Am Mac getestet, Blockung wirkt. Bei aktivem NordVPN läuft DNS über den VPN und nicht über AdGuard.
- Bei Anschaffung des Mac mini: Ollama einrichten und Paperless AI auf dem Pi darauf zeigen lassen.
