#!/bin/zsh
# Lädt Strecken, Höhenprofile und Streckenbilder aller Wettkämpfe neu und prüft,
# ob sich die Texte auf den Veranstalterseiten geändert haben (Doppelklick genügt).
cd "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude"
python3 .scripts/tri_update.py
echo ""
echo "Fertig. Dashboards im Browser neu laden (⌘R)."
echo "Fenster kann geschlossen werden."
