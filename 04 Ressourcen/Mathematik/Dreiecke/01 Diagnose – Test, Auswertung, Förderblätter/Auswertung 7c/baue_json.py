"""Rohdaten (aus den Scans gelesen) -> ergebnisse_dreiecke.json im Grundlagen-Check-Format.
Unklare Nummern laufen unter der Bogen-ID (A03, A07, A11, B05, B09), bis Oskar sie zuordnet:
dafuer unten in NUMMER_FUER_BOGEN eintragen und neu bauen."""
import json
from pathlib import Path
from ergebnisse_roh import B

NUMMER_FUER_BOGEN = {}   # z. B. {"A11": "9"}
SMILEY = {"s": "sicher", "g": "ging_so", "u": "unsicher"}

erg, sel, ver = {}, {}, {}
for bogen, (nr, version, a, sm) in B.items():
    nr = NUMMER_FUER_BOGEN.get(bogen) or (str(int(nr)) if nr.isdigit() else bogen)
    erg[nr] = {"N1": {"a": a["N1a"], "b": a["N1b"]}, "N2": {"a": a["N2"]},
               "N3": dict(zip("abcde", a["N3"])), "N4": {"a": a["N4a"], "b": a["N4b"]},
               "N5": {"a": a["N5a"], "b": a["N5b"]}, "N6": dict(zip("bcd", a["N6"])),
               "N7": {"a": a["N7a"], "b": a["N7b"]}, "N8": {"a": a["N8a"], "b": a["N8b"]}}
    sel[nr] = {f"N{i+1}": SMILEY[c] for i, c in enumerate(sm) if c in SMILEY}
    ver[nr] = version
Path(__file__).with_name("ergebnisse_dreiecke.json").write_text(json.dumps(
    {"test": "dreiecke", "versionen": ver, "ergebnisse": erg, "selbsteinschaetzung": sel}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(erg), "Bögen:", sorted(erg))
