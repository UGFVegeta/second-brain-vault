---
tags: [ressource, ki, claude-code, tools]
date: 2026-06-21
---

# Awesome Claude Code – Auswahl für mich

Kuratierte Auswahl aus der Sammelliste [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) (Stand 2026-06-21), gefiltert auf meine Ziele: App- und Website-Bauen, Produktivität, Wissensvault. Nichts davon muss installiert werden, es sind Kandidaten für später.

## ✅ Installiert & im Einsatz

- **[context-mode](https://github.com/mksglu/context-mode)** — MCP-Plugin gegen das Volllaufen des Kontextfensters / hohen Token-Verbrauch. Hält große Tool-/Datei-Datenmengen aus dem Kontext (Sandbox, bis ~98 % weniger), Sitzungs-Kontinuität über SQLite/FTS5, „Think in Code". Installiert am 2026-06-21 auf Projektebene, Version 1.0.162. Grund: kam zwei Tage in Folge ans Token-Limit. **Wirkt erst nach Neustart.** Verifizieren mit `/context-mode:ctx-doctor`, Ersparnis sehen mit `/context-mode:ctx-stats` (oder mich einfach „ctx stats" fragen). Hilft v. a. bei datenlastigen Sessions; Bilder (Videos) und große Skill-Prompts fängt es nicht ab.

- **[huashu-design](https://github.com/alchaincyf/huashu-design)** — Design-Skill: aus einem Satz Prompt werden Infografiken, Folien (HTML + editierbares PPTX), klickbare Prototypen, Animationen, Datenvisualisierungen. Installiert am 2026-06-21 auf Projektebene (`.agents/skills/huashu-design`). Getestet mit zwei Physik-Infografiken (Newtonsche Gesetze, Bewegung/Geschwindigkeit/Beschleunigung) → fachlich korrekt, druckfertig, kein „AI-Look". Direkt nützlich für Unterrichtsmaterial, Schul-Präsentationen, Infografiken, später Website/App-Mockups.
  - Voller Modus liefert 3 Gestaltungsvarianten + PDF-Export (im Test nur 1 Version, weil „kompakt" gewünscht).
  - Überschneidet sich mit pptx / frontend-slides / canvas-design (huashu = „auf einen Schlag poliert", die anderen kontrollierbarer).
  - ⚠️ Snyk stuft als „mittleres Risiko" ein → niemals Schülerdaten geben, nur lokale Material-Erstellung.
  - Testdateien: `07 Anhänge/huashu-test/`.

> [!tip] Top-Empfehlungen
> **Claudable** (Apps bauen), **Basic Memory** (Vault), **Happy Coder** (Handysteuerung).

## App- und Website-Bauen

- [Claudable](https://github.com/opactorai/Claudable) — Open-Source-Web-Builder, baut und deployt Apps mit Claude Code. Für eigene Lern-/Produktivitäts-Apps.
- [Fullstack Dev Skills](https://github.com/jeffallan/claude-skills) — 65 Skills für Web-/App-Entwicklung über viele Frameworks.
- [Anthropic Quickstarts](https://github.com/anthropics/claude-quickstarts) — offizielle Starterprojekte zum Lernen.
- [Codebase to Course](https://github.com/zarazhangrui/codebase-to-course) — macht aus Code einen interaktiven HTML-Kurs.
- [Container Use](https://github.com/dagger/container-use) — sichere, abgeschottete Dev-Umgebungen.
- [Web Assets Generator](https://github.com/alonw0/web-asset-generator) — Favicons, App-Icons, Social-Media-Bilder. (Habe ich als Skill schon installiert.)

## Produktivität & Wissensvault

- [Basic Memory](https://github.com/basicmachines-co/basic-memory) — KI-Mensch-Zusammenarbeit über Markdown, Wissensdatenbank. Passt zum Obsidian-Vault.
- [Context Engineering Kit](https://github.com/NeoLabHQ/context-engineering-kit) — bessere Ergebnisse bei wenig Tokens.
- [recall](https://github.com/zippoxer/recall) — frühere Claude-Sitzungen durchsuchen und fortsetzen.
- [claude-code-tools](https://github.com/pchalasani/claude-code-tools) — Sitzungs-Kontinuität, Kontext über Sessions retten.
- [VoiceMode MCP](https://github.com/mbailey/voicemode) — per Stimme mit Claude reden, freihändig.

## Claude Code besser lernen

- [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) — Einsteiger bis Power-User.
- [Claude Code Tips](https://github.com/ykdojo/claude-code-tips) — 35+ kompakte Tipps.
- [Anthropic Documentation](https://docs.claude.com/en/home) — offizielle Quelle.

## Komfort & Helfer

- [Dippy](https://github.com/ldayton/Dippy) — genehmigt sichere Befehle automatisch, fragt nur bei riskanten. Weniger Bestätigungsklicks.
- [agnix](https://github.com/agent-sh/agnix) — prüft CLAUDE.md, Skills und Hooks auf Fehler.
- [CC Usage](https://github.com/ryoppippi/ccusage) — Dashboard für Verbrauch und Kosten.

## Handysteuerung (vgl. Hermes-Idee)

- [Happy Coder](https://github.com/slopus/happy) — Claude Code vom Handy steuern, Push-Benachrichtigungen, läuft auf eigener Hardware. Claude-nahe Alternative zu Hermes, eher fürs Bauen. Siehe [[02 Projekte/KI-Assistent Setup (Hermes & Hardware).md]].
