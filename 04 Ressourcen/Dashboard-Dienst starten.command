#!/bin/zsh
# Startet den kleinen lokalen Dienst fürs Lebens-Dashboard (Erledigt-Knopf).
# Fenster offen lassen, solange das Dashboard genutzt wird. Strg+C beendet.
cd "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude"
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 .scripts/dashboard_server.py
