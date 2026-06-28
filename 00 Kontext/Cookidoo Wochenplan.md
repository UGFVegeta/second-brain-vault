---
tags: [kontext, kochen, thermomix]
date: 2026-06-22
---

# Cookidoo Wochenplan – Workflow

## Auslöser
Oskar sagt z.B. „Wochenplan", „Rezeptvorschläge" oder „zeig mir Vorschläge" → Workflow starten.

## Ablauf
1. Cookidoo-API aufrufen (Credentials: `~/.config/claude-cookidoo/cookidoo.env`)
2. 4 Rezepte für Mo–Do auswählen
3. Vorschlag zeigen → Oskar gibt OK oder tauscht aus
4. Rezepte in Cookidoo-Kalender eintragen
5. Zutaten in Bring! Home-Liste eintragen (List-ID: `ba821a4a-3067-4448-97bb-640a561d9421`, Credentials: `~/.config/claude-bring/bring.env`)

## Rezept-Kriterien
- ❌ Keine Pilze, kein Thunfisch
- ⏱️ Max. 60 Minuten
- 👨‍👩‍👧‍👦 Kinder essen mit (20 Monate & 4 Jahre)
- 🥗 Ausgewogen & gesund
- 🍖 Unter der Woche wenig Fleisch (eher vegetarisch/Fisch)
- 🌍 Vielfältig – keine Wiederholungen zur Vorwoche
- 🆕 Deftig im Thermomix noch unerprobt → gelegentlich vorschlagen

## Skripte
- Rezept-Browser: `.scripts/cookidoo_rezepte.py`
- Kalender + Bring! Eintrag: direkt per Python-Script inline

## Familie
- Julia (Cookidoo-Account: brosejulia@web.de) – Thermomix-Expertin
- Oskar – kocht auch
- Kind 1: 4 Jahre
- Kind 2: 20 Monate
