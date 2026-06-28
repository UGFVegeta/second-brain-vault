#!/bin/bash
# Automatischer lokaler Git-Snapshot des Vaults.
# Wird per launchd alle 15 Minuten ausgeführt (com.oskar.vaultgit).
VAULT="/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude"
cd "$VAULT" || exit 0
/usr/bin/git add -A
# Nur committen, wenn es tatsächlich Änderungen gibt (keine leeren Commits)
if ! /usr/bin/git diff --cached --quiet; then
  /usr/bin/git commit -m "Auto-Snapshot $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1
  echo "$(date '+%Y-%m-%d %H:%M')  Snapshot erstellt" >> "$VAULT/.scripts/git_autocommit.log"
fi
