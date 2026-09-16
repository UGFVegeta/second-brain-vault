import json
import sys
sys.path.insert(0, ".")
from ergebnisse_roh import ERGEBNISSE, VERSIONEN
from selbsteinschaetzung_roh import SELBSTEINSCHAETZUNG

daten = {
    "test": "8-9",
    "versionen": VERSIONEN,
    "ergebnisse": ERGEBNISSE,
    "selbsteinschaetzung": SELBSTEINSCHAETZUNG,
}
with open("ergebnisse_10b_komplett.json", "w", encoding="utf-8") as f:
    json.dump(daten, f, ensure_ascii=False, indent=1)

print(f"{len(ERGEBNISSE)} Schueler geschrieben.")
print("Nummern:", ", ".join(sorted(ERGEBNISSE, key=int)))
a = sum(1 for v in VERSIONEN.values() if v == "A")
print(f"Version A: {a}, Version B: {len(VERSIONEN) - a}")
