import json
import sys
sys.path.insert(0, ".")
from ergebnisse_roh import ERGEBNISSE
from selbsteinschaetzung_roh import SELBSTEINSCHAETZUNG

daten = {
    "test": "5-6",
    "ergebnisse": ERGEBNISSE,
    "selbsteinschaetzung": SELBSTEINSCHAETZUNG,
}
with open("ergebnisse_7c_teil1.json", "w", encoding="utf-8") as f:
    json.dump(daten, f, ensure_ascii=False, indent=1)

print(f"{len(ERGEBNISSE)} Schueler geschrieben.")
print("Nummern:", ", ".join(sorted(ERGEBNISSE, key=int)))
