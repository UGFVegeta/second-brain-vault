#!/bin/zsh
# Baut das Physik-Dashboard neu und öffnet es im Browser.
cd "$(dirname "$0")" || exit 1
python3 dashboard_bauen.py
open "Physik Dashboard.html"
