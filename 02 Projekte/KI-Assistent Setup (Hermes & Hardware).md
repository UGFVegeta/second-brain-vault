---
tags: [projekt, idee, ki, hardware, hermes, datenschutz]
status: idee
date: 2026-06-21
---

# KI-Assistent Setup (Hermes & Hardware)

> [!note] Status
> Idee / Planung – noch keine Anschaffung. Festgehalten am 2026-06-21.

> [!check] Entscheidung 20.09.2026
> **Ein Gerät statt zwei: Mac mini M6 mit 32 GB und 512 GB SSD**, bei TeacherStore mit Bildungsrabatt 1.549 €. Das M1-MacBook Pro bleibt der Laptop. Ein neues MacBook Pro kommt nur in Frage, wenn die Stelle als Konrektor oder Rektor kommt.
> Gegen den M5 Pro mit 48 GB (2.469 €) entschieden: Die 920 € bringen Tempo und Luft, die für Aufgaben im Hintergrund nicht nötig sind. Gegen die 24-GB-Variante entschieden, weil erst 32 GB die Modelle der 26B- bis 31B-Klasse zulassen.

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

**Update 22.09.2026, echte Testberichte zum Marktstart:** Geekbench und Cinebench bestätigen kräftige Sprünge bei CPU und Grafik (Einzelkern 24 %, Mehrkern 48 %, GPU 71 % über dem M4), unabhängig von 9to5Mac, Engadget und Notebookcheck gemessen. Für lokale Sprachmodelle gibt es dagegen noch keine unabhängigen Messungen, nur Schätzungen aus der Bandbreite, dieselbe Rechnung wie hier im Dokument. Zwei Quellen bestätigen aber die Eckdaten: 170 GB/s bei 24 und 32 GB, 153 GB/s beim 16-GB-Modell (deckt sich mit oben), und rund 11 % mehr Tempo als der M5-Mini bei gleicher Quantisierung. Eine Schätzung nennt für gpt-oss 20B rund 27 Token/s und für Gemma 4 26B rund 22 Token/s auf dem M6, beides MoE-Modelle mit wenigen aktiven Parametern, das passt zur hier getroffenen Einschätzung, dass MoE-Modelle deutlich schneller laufen als dichte. Für ein dichtes 27B-Modell (Qwen3.6) nennt niemand eine M6-Zahl. Alles unter Vorbehalt, bis im Dezember echte Tests vorliegen. Quellen: kingy.ai/blog/m6-mac-mini-local-ai-edge-llm, contracollective.com/blog/mac-mini-m6-local-llm-inference-refresh-2026, modelfit.io/blog/m6-mac-mini-local-llm, 9to5mac.com/2026/09/21/m6-mac-mini-review, engadget.com (M6-Testbericht).

Eine Quelle (modelfit) würde für reine Ollama-Nutzung sogar die 24-GB-Variante empfehlen, wenn gpt-oss 20B als Obergrenze reicht, das spart gegenüber 32 GB rund 190 €. Das gilt nur, wenn auf die 26B- bis 31B-Klasse verzichtet wird; die Empfehlung hier bleibt deshalb bei 32 GB.

Modellkandidaten aus der Ollama-Bibliothek (Größen laut ollama.com, Stand 19.09.2026):
- Qwen3.6 27B (18 GB) und Qwen3.8 (18 GB): stark bei Denken, Werkzeugnutzung und Agentenaufgaben.
- Gemma 4 26B (19 GB) bzw. 31B (20 GB), kleiner 12B (7,6 GB): Google, multimodal.
- gpt-oss 20B (14 GB) als schnelle Variante.
- Qwen3-Embedding 0,6B (0,6 GB) für die Dokumentensuche in Paperless AI.
- Nicht mehr in 64 GB: gpt-oss 120B (65 GB), Mistral Medium 3.5 (80 GB).

Welches davon besser Deutsch schreibt, ist ungeprüft. Nach der Anschaffung mit echten eigenen Aufgaben vergleichen.

Beobachtungsposten, Stand 21.09.2026: **Ternary Bonsai 2 27B** von PrismML, eine auf Ternärgewichte gestauchte Fassung von Qwen3.8 27B. Die Datei ist 5,9 GB groß (PTQ1_0, GGUF) bzw. 8,5 GB (MLX, 2 Bit), statt 18 GB bei der normalen Ollama-Fassung. Nach Herstellerangabe bleiben 98,2 % der Gesamtleistung erhalten, Apache 2.0. Ein unabhängiger Vergleich (OrcaRouter, nur eine Quelle) sieht bei langen Programmieraufgaben dagegen rund 25 % Verlust (Terminal-Bench 52,8 statt 69,7) und bei Bildverständnis etwa 3 Punkte. Läuft nicht in Ollama, sondern nur mit PrismMLs llama.cpp-Fork oder über MLX. Stock-llama.cpp kann die Datei laut OrcaRouter falsch laden und liefert dann flüssigen Unsinn. Herstellerwert 46,8 Token/s auf M5 Max, für den M6 hochgerechnet grob 13 bis 17 Token/s, nicht gemessen. Erst drei Tage alt, deshalb nach dem Kauf mit eigenen Aufgaben testen, nicht vorher darauf bauen. Quellen: prismml.com/news/bonsai-2-27b, docs.prismml.com/bonsai-2-27b.

24 GB oder 32 GB beim M6: Das ist die entscheidende Grenze. macOS gibt dem Grafikteil standardmäßig nur etwa zwei Drittel des Arbeitsspeichers frei (per `sysctl iogpu.wired_limit_mb` anhebbar, Faustwert). Mit 24 GB bleiben also rund 16 GB, damit laufen nur gpt-oss 20B (14 GB) und Gemma 4 12B (7,6 GB). Mit 32 GB sind es rund 21 GB, damit läuft die 26B- bis 31B-Klasse, dazu das kleine Embedding-Modell und noch Hermes daneben. Arbeitsspeicher lässt sich nie nachrüsten, Festplattenplatz dagegen über eine externe SSD (Ollama-Modelle per `OLLAMA_MODELS` auslagern). Wenn nur ein Aufpreis drin ist: 32 GB nehmen.

Dasselbe gilt für den M5 Pro: 24 GB bleiben 24 GB, egal welcher Chip. Ein M5 Pro mit 24 GB wäre die schlechteste Kombination, schneller Chip mit kleinen Modellen. Wenn M5 Pro, dann mindestens 48 GB. Die bringen dann rund 32 bis 36 GB nutzbar, also Platz für mehrere Dienste gleichzeitig und für lange Zusammenhänge (die Modelle können 256K Kontext, und der belegt Speicher zusätzlich zum Modell).

Tempo: Bei dichten Modellen entspricht die Tokenrate grob Bandbreite geteilt durch Modellgröße. 18 GB auf 170 GB/s sind rechnerisch rund 9 Token/s, real eher 6 bis 8, also etwa Lesegeschwindigkeit. Geschätzt, nicht gemessen. Modelle mit wenigen aktiven Parametern (Mixture of Experts) umgehen das: Gemma 4 26B hat nur 4 Mrd. aktive Parameter, gpt-oss 20B ähnlich wenige. Auf dem M6 deshalb MoE-Modelle bevorzugen, dann reicht der M6.

Preise bei TeacherStore.de mit Bildungsrabatt (Stand 20.09.2026, Basismodelle von der Übersichtsseite, Konfigurationen aus dem Konfigurator):

| Konfiguration | Preis |
|---|---|
| M6, 16 GB, 512 GB | 1.149 € |
| M6, 24 GB, 512 GB | 1.359 € |
| **M6, 32 GB, 512 GB** | **1.549 €** |
| M5 Pro, 24 GB, 512 GB | 1.859 € |
| M5 Pro, 48 GB, 512 GB | 2.469 € |

Der Schritt von 24 auf 32 GB kostet dort 190 € und schaltet genau die 26B- bis 31B-Klasse frei. Das ist der beste Gegenwert in der Liste. Der Sprung vom M6 mit 32 GB auf den M5 Pro mit 48 GB kostet 920 €.

Einschätzung: Mit 32 GB (M6) passt ein Modell der 27B-Klasse, aber nur eins zur Zeit und ohne viel Luft. 64 GB (M5 Pro) bringen keine größere Modellklasse, aber Tempo, Platz für mehrere Dienste gleichzeitig (Hermes, Paperless AI, Chat) und längere Dokumente. Damit könnte der M5 Pro mit 64 GB beide Geräte aus dem Zielbild ersetzen.

## Zusammenspiel: lokales Modell und Claude (Stand 21.09.2026)

Der Kauf ist frühestens für Dezember/Januar geplant, Bonsai 2 und die Ollama-Unterstützung werden bis dahin nachgeprüft. Es gibt drei Wege, das lokale Modell und Claude zu kombinieren, Hermes ist dafür nicht zwingend.

1. **Claude als Chef, lokales Modell als Helfer.** Claude Code ruft Ollama auf dem Mac mini über ein kleines Skript (später `.scripts/lokal.py`) oder einen MCP-Server auf. Claude formuliert den Auftrag, das lokale Modell arbeitet die Masse ab, zurück kommt nur das Ergebnis. Kein Umschalten nötig. Grenze: Claude sieht die Ergebnisse, sie gehen also in die Cloud. Nichts mit Schülerdaten.
2. **Claude Code komplett auf das lokale Modell umstellen.** Ollama kann seit v0.14.0 die Anthropic-Schnittstelle (`ollama launch claude` oder `ANTHROPIC_BASE_URL`). Dann steuert das lokale Modell Claude Code, Claude ist nicht mehr beteiligt. Soweit ich weiß nur beim Start der Sitzung einstellbar, nicht mittendrin. Für mehrstufige Arbeit deutlich schwächer. Der Weg für alles Schulische mit Personenbezug.
3. **Hermes** als eigener Agent auf dem Mac mini, nur nötig für Handy-Zugriff und Aufträge rund um die Uhr ohne Mac. Mit Claude als Modell braucht Hermes laut eigener Doku entweder einen API-Schlüssel (Abrechnung pro Token) oder Claude Max mit zugekauftem Zusatzguthaben. Pro-Abo geht nicht. Für Oskar damit ausgeschlossen: Er bleibt bei Claude Pro (20 $ im Monat), API-Guthaben hat er getestet und als viel zu teuer erlebt (10 € waren schnell weg). Hermes würde also nur mit dem lokalen Modell laufen, ohne laufende Kosten.

Empfehlung: mit 1 anfangen. Paperless AI spricht ohnehin direkt mit Ollama, dafür braucht es weder Hermes noch Claude. Hermes erst, wenn der Handy-Zugriff wirklich fehlt.

Schülerdaten und lokales Modell: Technisch bleiben die Daten auf dem Mac mini, solange kein Cloud-Dienst dazwischenhängt (kein API-Schlüssel, kein Claude). Ob die dienstliche Verarbeitung von Schülerdaten auf einem privaten Gerät erlaubt ist, ist damit nicht geklärt. Das ist eine Frage an die Schulleitung bzw. den Datenschutzbeauftragten, siehe [[Datenschutz – Privates System als Konrektor]]. Bei einem einzigen Gerät geht die frühere Trennung (Dauerläufer ohne Schulisches, Schreibtisch-Gerät mit Schulischem) verloren und muss bewusst nachgebaut werden: eigenes macOS-Benutzerkonto für Schulisches, Hermes und Messaging ohne Zugriff darauf, FileVault an, und Claude Code bekommt Schülerdaten nie zu sehen (also Weg 2 oder ein Chatfenster statt Weg 1).

## Offene Punkte / Nächste Schritte

- ~~Entscheiden: zwei Geräte oder ein starker Dauerläufer?~~ Am 20.09.2026 entschieden, siehe oben: Mac mini M6 mit 32 GB.
- Beim Kauf auf die Lieferzeit achten, die Auslieferung des neuen Mac mini beginnt erst am 22.09.2026.
- Nach dem Kauf: MoE-Modelle zuerst testen (Gemma 4 26B, gpt-oss 20B), dann mit eigenen Texten gegen Qwen3.6 27B vergleichen.
- Bei Anschaffung: Hermes testweise auf einem Gerät aufsetzen, erst mit Cloud-Modell, dann lokal.
- Messaging-Kanal wählen (Signal bevorzugt).
- Realistische Kosten gegenüberstellen (Hardware + ggf. Claude Max / Nous Portal Abo).
- ~~Pi: automatisches Backup außerhalb der SD-Karte einrichten.~~ Am 20.09.2026 erledigt: `.scripts/paperless_backup.sh` läuft täglich um 20:00 über den LaunchAgent `com.oskar.paperless-backup` und legt den Export unter `~/Backups/Paperless-Pi/` ab (Ordner `aktuell` plus sieben datierte Momentaufnahmen, die per Hardlink kaum Platz brauchen). Log unter `~/Library/Logs/paperless-backup.log`. SSH-Zugang für Claude Code steht seit 19.09.2026 (`ugfvegeta@raspberrypi.local`).
- Offen: Der Mac selbst hat keine Time Machine. Es gibt damit nur eine Kopie außerhalb des Pi. Zweites Ziel überlegen, zum Beispiel die vorhandene externe Samsung-SSD.
- AdGuard Home: Assistent erledigt, Weboberfläche unter http://192.168.178.68. In der Fritzbox feste IP für den Pi und `192.168.178.68` als lokaler DNS-Server (IPv4) eingetragen (19.09.2026). `fritz.box` und Gerätenamen löst AdGuard über die Fritzbox auf. Lokaler DNSv6-Server in der Fritzbox ist ebenfalls der Pi (`fdfe:bdd8:3b4f:0:cd03:6553:adc3:26e9`), sonst fragen Geräte per IPv6 an AdGuard vorbei. Am Mac getestet, Blockung wirkt. Bei aktivem NordVPN läuft DNS über den VPN und nicht über AdGuard.
- Bei Anschaffung des Mac mini: Ollama einrichten und Paperless AI auf dem Pi darauf zeigen lassen.
