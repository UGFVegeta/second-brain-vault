"""Merkheft-Bilder im Rezept-Stil (Beispiel links mit Schrittnummern, Rezept rechts) für Rationale Zahlen Kl. 7.
Wird von baue_wochen_1_2.py (Woche 2) und baue_woche3.py eingebunden. Minusklammer und Klammer setzen stehen in
baue_woche3_rezeptstil.py (MERK, RUECK_B), gemischte Aufgaben in baue_woche7.py (MERK)."""
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
sys.path.insert(0, str(HIER))
from mathe_woche_vorlage import aus_skript  # noqa: E402
from baue_woche7 import merkbild, rezept_box  # noqa: E402

bogengerade, = aus_skript(HIER / "baue_stunde2.py", "bogengerade")

SCHRITTE_PM = ["Gleiche Zeichen? Das Zeichen bleibt, die Zahlen zusammenzählen.",
               "Verschiedene Zeichen? Bei der ersten Zahl starten.",
               "Plus nach rechts, Minus nach links.",
               "Über die Null? Dann wechselt das Vorzeichen."]
REZEPT_PM = rezept_box("Plus und Minus", SCHRITTE_PM)


def _gerade(von, bis, start, delta):
    return f'<figure style="margin:0">{bogengerade(von, bis, start, delta, kpe=2)}</figure>'


MERK_PLUSMINUS = merkbild("Plus und Minus", [
    [(1, '<span class="gelb">−4 − 8</span><span class="klein">gleiche Zeichen: Minus bleibt, 4 + 8</span>'),
     (None, "= <b>−12</b>")],
    [(2, '−2 + 7<span class="klein">verschiedene Zeichen: Start bei −2</span>'),
     (3, _gerade(-4, 7, -2, 7)),
     (4, '= <b>5</b><span class="klein">über die Null, das Minus ist weg</span>')],
], SCHRITTE_PM, weitere=[
    ("3 + 5", "8", 8), ("−6 − 3", '<span class="rot">−</span>9', -9), ("−2,5 − 1,5", '<span class="rot">−</span>4', -4),
    ("6 − 9", '<span class="rot">−</span>3', -3), ("−7 + 10", "3", 3), ("−12 + 4", '<span class="rot">−</span>8', -8)])
