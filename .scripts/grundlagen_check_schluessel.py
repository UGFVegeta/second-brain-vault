"""Lösungsschlüssel für die Grundlagen-Checks (Klasse 5-6 und Klasse 6-9).

Jeder Test ist ein Dict: Abschnitt -> Aufgabe -> {Teilaufgabe: erwartete Antwort}.
Die erwartete Antwort ist entweder eine Zahl, ein String oder eine Liste/Tupel
für Aufgaben mit mehreren gültigen Notationen (z. B. Bruch und Dezimalzahl).

Dient als Eingabe für grundlagen_check_bericht.py. Wird nichts anderes importiert,
kann diese Datei auch einzeln aufgerufen werden, um den Schluessel auszudrucken.
"""

# --- Grundlagen Klasse 5-6 (neue 7. Klasse) ---------------------------------

SCHLUESSEL_5_6 = {
    "A · Grundrechenarten und Rechenregeln": {
        "A1": {"a": 8292, "b": 3146, "c": 13104, "d": 117},
        "A2": {"a": 27, "b": 75, "c": 14, "d": 144},
        "A3": {"a": 3500, "b": 7000, "c": 6380, "d": 10000},
        "A4": {"a": {"1", "2", "3", "4", "6", "8", "12", "24"}, "b": 6, "c": 24, "d": 12},
    },
    "B · Brüche": {
        "B1": {"a": "5/6", "b": "7/12", "c": "1/2", "d": ("5/4", "1 1/4")},
        "B2": {"a": "2/5", "b": 0.6, "c": ("1 1/4", "5/4"), "d": 2.25},
        "B3": {"a": "2/3", "b": "3/5", "c": "3/4", "d": "2/3"},
        "B4": {"reihenfolge": ["3/8", "2/5", "1/2", "0,6"]},
        "B5": {"ergebnis": "3/8"},
    },
    "C · Dezimalzahlen": {
        "C1": {"a": 20.25, "b": 8.85, "c": 12.6, "d": 0.48},
        "C2": {"a": 1.6, "b": 12, "c": 250, "d": 3.47},
        "C3": {"a": 4.57, "b": 12.3, "c": 3.14, "d": 8.7},
        "C4": {"a": "=", "b": "<", "c": ">", "d": ">"},
    },
    "D · Größen und Geometrie": {
        "D1": {"a": 3500, "b": 2.4, "c": 135, "d": 420},
        "D2": {"a": 26, "b": 40},
        "D3": {"a": 24, "b": 36},
        "D4": {"a": "spitz", "b": "recht", "c": "stumpf", "d": "gestreckt"},
        "D5": {"a": 19, "b": 21},
    },
}

# --- Grundlagen Klasse 6-9 (bestehende 10. Klasse) --------------------------

SCHLUESSEL_6_9 = {
    "A · Brüche, Dezimalzahlen und Größen": {
        "A1": {"a": ("19/12", "1 7/12"), "b": "13/24", "c": "3/4", "d": "7/8"},
        "A2": {"a": "3/4", "b": 0.375, "c": ("2 2/5", "12/5"), "d": 1.25},
        "A3": {"a": 1, "b": 8, "c": 0.009, "d": 1.6},
        "A4": {"a": 2500, "b": 0.75, "c": 90, "d": 320},
        "A5": {"reihenfolge": ["0,65", "2/3", "0,7", "3/4"]},
    },
    "B · Prozent, Zinsen und rationale Zahlen": {
        "B1": {"a": 20, "b": 4.5, "c": 90, "d": 12},
        "B2": {"a": 25, "b": 50, "c": 92, "d": 60},
        "B3": {"a": 60, "b": 30, "c": 3},
        "B4": {"a": 5, "b": 30, "c": -9, "d": 5, "e": -8, "f": 17},
        "B5": {"ergebnis": 10.8},
    },
    "C · Terme, Gleichungen und lineare Funktionen": {
        # Terme: nur exakter, normalisierter Stringvergleich moeglich.
        # Aequivalente Umformungen (z. B. andere Klammerreihenfolge) werden
        # nicht erkannt - bei "unsicher" immer kurz von Hand pruefen.
        "C1": {"a": "2x+7y", "b": "6a-22", "c": "x^2-2x-15", "d": "4x^2+12x+9"},
        "C2": {"a": "3(2x+3)", "b": "4a(a-3)", "c": "(x+5)(x-5)"},
        "C3": {"a": 8, "b": 7, "c": 9, "d": 5},
        "C4": {"m": -2, "b": 3, "liegt": "ja", "nullstelle": 1.5},
        "C5": {"funktionsgleichung": "y=2x+1"},
    },
    "D · Potenzen, Wurzeln und Satz des Pythagoras": {
        "D1": {"a": 81, "b": 256, "c": 100, "d": 729, "e": 1, "f": 0.0625},
        "D2": {"a": 12, "b": 0.5, "c": ("5√2", "7,07"), "d": 12, "e": 4.5},
        "D3": {"a": 10, "b": 12, "c": 7.07, "d": 15, "e": 12},
        "D4": {"a": 4.77, "b": 108.17},
    },
}

TESTS = {
    "5-6": {"name": "Grundlagen Klasse 5-6", "schluessel": SCHLUESSEL_5_6},
    "6-9": {"name": "Grundlagen Klasse 6-9", "schluessel": SCHLUESSEL_6_9},
}


if __name__ == "__main__":
    import json
    import sys

    def _serialisierbar(obj):
        if isinstance(obj, set):
            return sorted(obj)
        if isinstance(obj, tuple):
            return list(obj)
        raise TypeError

    for kuerzel, test in TESTS.items():
        print(f"=== {test['name']} ===")
        print(json.dumps(test["schluessel"], ensure_ascii=False, indent=1, default=_serialisierbar))
        print()
