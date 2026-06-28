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
- Frühe Version (0.x), also noch mit Ecken und Kanten.

## Offene Punkte / Nächste Schritte

- Entscheiden: zwei Geräte (Mac mini + neues MacBook 48 GB) oder ein starker Dauerläufer?
- Bei Anschaffung: Hermes testweise auf einem Gerät aufsetzen, erst mit Cloud-Modell, dann lokal.
- Messaging-Kanal wählen (Signal bevorzugt).
- Realistische Kosten gegenüberstellen (Hardware + ggf. Claude Max / Nous Portal Abo).
