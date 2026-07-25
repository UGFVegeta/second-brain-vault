#!/bin/zsh
# Startet die Buch-Chat-Brücke für das Lese-Dashboard (Doppelklick genügt).
cd "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude"
echo "📚 Buch-Chat wird gestartet – dieses Fenster offen lassen."
exec python3 .scripts/lese_chat_server.py
