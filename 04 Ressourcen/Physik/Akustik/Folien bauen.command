#!/bin/zsh
# Baut aus jeder HTML-Datei in diesem Ordner eine PDF im Notability-Folienformat.
cd "$(dirname "$0")" || exit 1
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for f in *.html; do
  [ -e "$f" ] || continue
  out="${f%.html}.pdf"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
            --print-to-pdf="$out" "$f" >/dev/null 2>&1
  echo "gebaut: $out"
done

echo ""
echo "Fertig. Die PDF per AirDrop oder iCloud nach Notability ziehen."
read -k 1 -s
