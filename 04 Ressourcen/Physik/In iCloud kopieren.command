#!/bin/zsh
# Baut alle Foliensätze und den Stoffverteilungsplan neu und legt sie
# zusätzlich im iCloud-Ordner ab, damit sie dort auffindbar bleiben.
cd "$(dirname "$0")" || exit 1

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ZIEL="$HOME/Library/Mobile Documents/com~apple~CloudDocs/GDRS ICloud/Physik/Physik Klasse 7/Schuljahr 2026-27"
mkdir -p "$ZIEL"

echo "Foliensätze bauen ..."
for d in Optik Akustik; do
  for f in "$d"/*.html; do
    [ -e "$f" ] || continue
    "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
              --print-to-pdf="${f%.html}.pdf" "$f" >/dev/null 2>&1
    echo "  ${f%.html}.pdf"
  done
done

echo "Dashboard bauen ..."
python3 dashboard_bauen.py

echo "Stoffverteilungsplan als PDF ..."
TMP=$(mktemp -d)
python3 - "$TMP" <<'EOF'
import re, sys, pathlib
tmp = pathlib.Path(sys.argv[1])
q = pathlib.Path("Stoffverteilungsplan Physik Klasse 7 2026-27.md")
t = re.sub(r"^---\n.*?\n---\n", "", q.read_text(encoding="utf-8"), flags=re.S)
t = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", t)
t = re.sub(r"\[\[([^\]]+)\]\]", r"\1", t)
t = re.sub(r"^> \[!info\][^\n]*\n", "", t, flags=re.M)
(tmp / "plan.md").write_text(t, encoding="utf-8")
EOF
cp "plan.css" "$TMP/" 2>/dev/null || cat > "$TMP/plan.css" <<'CSS'
@page { size: A4 landscape; margin: 14mm 12mm; }
body { font-family: "Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;
  font-size: 9.5pt; line-height: 1.4; color: #16181d; margin: 0; }
h1 { font-size: 19pt; font-weight: 600; margin: 0 0 2mm; }
h2 { font-size: 12.5pt; font-weight: 600; margin: 7mm 0 2mm; color: #2E4257;
  border-bottom: 1px solid #C3D0E2; padding-bottom: 1mm; }
p { margin: 0 0 2mm; } ul { margin: 0 0 3mm; padding-left: 5mm; }
table { width: 100%; border-collapse: collapse; margin: 2mm 0 4mm; font-size: 8.5pt; }
th { background: #8DA6C2; color: #10141a; text-align: left; padding: 1.6mm 2mm;
  font-weight: 600; border: .3pt solid #66798E; }
td { padding: 1.4mm 2mm; border: .3pt solid #B9C4D4; vertical-align: top; }
tr:nth-child(even) td { background: #F4F7FA; }
td:first-child { font-weight: 600; white-space: nowrap; }
td:nth-child(2) { white-space: nowrap; }
th:nth-child(4), td:nth-child(4) { width: 21%; }
th:nth-child(5), td:nth-child(5) { width: 10%; }
th:nth-child(6), td:nth-child(6) { width: 11%; }
th:nth-child(7), td:nth-child(7) { width: 17%; }
th:nth-child(8), td:nth-child(8) { width: 7%; }
th:nth-child(9), td:nth-child(9) { width: 12%; }
blockquote { margin: 2mm 0; padding: 2mm 3mm; background: #F0F4F8;
  border-left: 2.5pt solid #8DA6C2; }
a { color: #16181d; text-decoration: none; }
CSS
pandoc "$TMP/plan.md" -f markdown+pipe_tables -t html5 -o "$TMP/body.html"
{ echo '<!doctype html><html lang="de"><head><meta charset="utf-8">'
  echo '<link rel="stylesheet" href="plan.css"></head><body>'
  cat "$TMP/body.html"; echo '</body></html>'; } > "$TMP/plan.html"
(cd "$TMP" && "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
   --print-to-pdf="$ZIEL/Stoffverteilungsplan Physik Klasse 7.pdf" plan.html >/dev/null 2>&1)
rm -rf "$TMP"

echo "kopieren ..."
cp "Optik/Optik I.pdf" "Optik/Optik II.pdf" "Akustik/Akustik.pdf" "Physik Dashboard.html" "$ZIEL/"

echo ""
echo "Fertig. Liegt jetzt in:"
echo "$ZIEL"
ls -1 "$ZIEL"
read -k 1 -s
