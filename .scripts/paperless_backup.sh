#!/bin/bash
# Sichert Paperless-ngx vom Raspberry Pi auf den Mac.
#
# Ablauf: Auf dem Pi laeuft der document_exporter und schreibt Dokumente plus
# Metadaten nach /home/ugfvegeta/paperless-ngx/export. Diesen Ordner holt rsync
# auf den Mac nach ~/Backups/Paperless-Pi/aktuell. Danach entsteht eine datierte
# Momentaufnahme, die per Hardlink auf "aktuell" zeigt und deshalb kaum Platz
# braucht. Die letzten 7 Momentaufnahmen bleiben liegen.
#
# Aufruf: taeglich ueber den LaunchAgent com.oskar.paperless-backup,
# manuell mit: bash ".scripts/paperless_backup.sh"

set -u

PI_HOST="ugfvegeta@raspberrypi.local"
PI_KEY="$HOME/.ssh/id_ed25519_pi"
PI_COMPOSE_DIR="/home/ugfvegeta/paperless-ngx"
PI_EXPORT_DIR="$PI_COMPOSE_DIR/export"
BASE="$HOME/Backups/Paperless-Pi"
CURRENT="$BASE/aktuell"
DATE="$(date +%Y-%m-%d)"
SNAPSHOT="$BASE/$DATE"
KEEP=7

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }

log "Start"

SSH_OPTS=(-i "$PI_KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=15)

if ! ssh "${SSH_OPTS[@]}" "$PI_HOST" true 2>/dev/null; then
  log "FEHLER: Pi nicht erreichbar, Abbruch."
  exit 1
fi

# 1. Export auf dem Pi erzeugen. --delete raeumt Dateien weg, die es in
#    Paperless nicht mehr gibt, damit rsync danach nur Aenderungen uebertraegt.
log "Export auf dem Pi laeuft"
if ! ssh "${SSH_OPTS[@]}" "$PI_HOST" \
  "cd '$PI_COMPOSE_DIR' && sudo docker compose exec -T webserver document_exporter ../export --delete --no-progress-bar"; then
  log "FEHLER: document_exporter fehlgeschlagen, Abbruch."
  exit 1
fi

# 2. Export auf den Mac holen.
mkdir -p "$CURRENT"
log "Uebertragung auf den Mac"
if ! rsync -a --delete -e "ssh ${SSH_OPTS[*]}" "$PI_HOST:$PI_EXPORT_DIR/" "$CURRENT/"; then
  log "FEHLER: rsync fehlgeschlagen, Abbruch."
  exit 1
fi

# 3. Plausibilitaet: ohne manifest.json ist der Export unbrauchbar.
if [ ! -s "$CURRENT/manifest.json" ]; then
  log "FEHLER: manifest.json fehlt oder ist leer. Momentaufnahme wird nicht angelegt."
  exit 1
fi

# 4. Datierte Momentaufnahme per Hardlink.
if [ -d "$SNAPSHOT" ]; then
  rm -rf "$SNAPSHOT"
fi
rsync -a --link-dest="$CURRENT" "$CURRENT/" "$SNAPSHOT/"

# 5. Alte Momentaufnahmen aufraeumen, die letzten $KEEP bleiben.
cd "$BASE" || exit 1
ls -1d 20*-*-* 2>/dev/null | sort -r | tail -n +$((KEEP + 1)) | while read -r old; do
  log "Entferne alte Momentaufnahme $old"
  rm -rf "$BASE/${old:?}"
done

ANZAHL=$(find "$CURRENT" -type f | wc -l | tr -d ' ')
GROESSE=$(du -sh "$CURRENT" | cut -f1)
log "Fertig. $ANZAHL Dateien, $GROESSE, Momentaufnahme $DATE"
