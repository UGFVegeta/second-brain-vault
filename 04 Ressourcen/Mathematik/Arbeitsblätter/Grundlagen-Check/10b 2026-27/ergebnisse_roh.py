# -*- coding: utf-8 -*-
"""Rohtranskription der Antwortbögen 10b, Grundlagen Klasse 8-9 (16.09.2026).

Erster echter A/B-Durchlauf. 30 gescannte Seiten = 27 Bögen (eine Leerseite,
zwei reine Nebenrechnungs-Seiten). Vorhandene Nummern: 1-14, 16-28.
Nummer 15 ist nicht dabei (kein Bogen im Scan).

WICHTIG: von Hand aus 300-dpi-Scans gelesen. Unsichere Stellen stehen in
UNSICHER und sind hier bewusst als "" eingetragen, damit das Auswerteskript
sie als "nicht bearbeitet" zaehlt statt eine Falschlesung als Fehler zu
werten.

Zwei Konventionen beim Uebertragen:
 * Prozentangaben aus Block D2 sind in Dezimalzahlen umgerechnet
   ("22,2 %" -> "0,222"), sonst liest das Auswerteskript 22,2 als Zahl.
 * Was im Kaestchen steht, zaehlt. Korrekturen unter dem Kaestchen oder
   ueber dem Kaestchen sind in den Kommentaren vermerkt, aber nicht
   eingetragen (Arbeitsauftrag: "Nur das Endergebnis in das Kaestchen").

Siehe TERME_MANUELL: mathematisch richtige, aber anders geschriebene Terme,
die der reine Stringvergleich als falsch zaehlt.
"""

# Welche Nummer hat welche Version geschrieben (Kopf des Antwortbogens).
# Drei Boegen hatten kein Kreuz - die Version ist dort aus den Antworten
# erschlossen (siehe VERSIONEN_ERSCHLOSSEN).
VERSIONEN = {
    "1": "B", "2": "B", "3": "B", "4": "B", "5": "B", "6": "A", "7": "A",
    "8": "A", "9": "B", "10": "A", "11": "B", "12": "A", "13": "B",
    "14": "A", "16": "A", "17": "A", "18": "B", "19": "A", "20": "B",
    "21": "A", "22": "B", "23": "A", "24": "A", "25": "B", "26": "A",
    "27": "A", "28": "B",
}

VERSIONEN_ERSCHLOSSEN = [
    ("6", "kein Kreuz im Kopf; A1a '2x+7y' ist der A-Term -> A"),
    ("19", "kein Kreuz im Kopf; A1a '2x+7y', A3 8/7, C1a 81 -> A"),
    ("5", "kein Kreuz im Kopf; A1b '4a-10', A3 7/5, D1 15/15 -> B"),
    ("24", "Kopf zeigt B (Kaestchen ausgemalt), aber alle Antworten sind "
           "eindeutig A (2x+7y, 6a-22, 81/100, c=10 cm) -> als A gewertet"),
]

ERGEBNISSE = {
    "1": {  # s1-02
        "A1": {"a": "3x+7y", "b": ""},
        "A2": {"a": "", "b": ""},
        "A3": {"a": "", "b": ""},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "", "b": "", "c": ""},
        "C2": {"a": "", "b": "", "c": ""},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "2": {  # s1-06
        "A1": {"a": "3x+7y", "b": "4a-14"},   # b durchgestrichen, darunter 4a-14
        "A2": {"a": "", "b": ""},             # beide Kaestchen durchgestrichen
        "A3": {"a": "7", "b": "5"},
        "B1": {"m": "2", "b": "-4", "liegt": "ja", "nullstelle": "2"},
        "C1": {"a": "16", "b": "243", "c": "1000"},
        "C2": {"a": "13", "b": "0,6", "c": "8,49"},
        "D1": {"a": "15cm", "b": "18,79cm", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "3": {  # s2-4
        "A1": {"a": "3x-7y", "b": "4a-14"},
        "A2": {"a": "20v", "b": "6a"},
        "A3": {"a": "6x=4", "b": "3x=4"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "16", "b": "243", "c": "1000"},
        "C2": {"a": "13", "b": "0,6", "c": "8,5"},   # 8,5 statt 8,49 - knapp daneben
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "4": {  # s3-03
        "A1": {"a": "5x+5y", "b": "4a-10"},
        "A2": {"a": "4(2x+3)", "b": "2a(3a-6)"},
        "A3": {"a": "7", "b": "5"},
        "B1": {"m": "1", "b": "4", "liegt": "ja", "nullstelle": ""},
        "C1": {"a": "16", "b": "243", "c": "1000"},
        "C2": {"a": "13", "b": "0,6", "c": ""},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "5": {  # s1-13
        "A1": {"a": "7y+3x", "b": "4a-10"},   # a ist 3x+7y, nur umgestellt
        "A2": {"a": "2(4x-6)", "b": "2a(3a-9)"},
        "A3": {"a": "7", "b": "5"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "16", "b": "", "c": ""},  # b unleserlich ("1?6")
        "C2": {"a": "", "b": "0,06", "c": ""},
        "D1": {"a": "15cm", "b": "15cm", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "6": {  # s1-01
        "A1": {"a": "2x+7y", "b": ""},        # b komplett durchgestrichen
        "A2": {"a": "", "b": ""},
        "A3": {"a": "2x+9", "b": "1x+6"},     # Term statt Loesung
        "B1": {"m": "81", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "", "b": "", "c": ""},
        "C2": {"a": "", "b": "", "c": ""},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "7": {  # s1-05
        "A1": {"a": "2x+7y", "b": "6a-22"},
        "A2": {"a": "3(2x+3)", "b": "2a(2a-6)"},
        "A3": {"a": "8", "b": "7"},
        "B1": {"m": "-2", "b": "3", "liegt": "nein", "nullstelle": "1,5"},
        "C1": {"a": "81", "b": "256", "c": ""},
        "C2": {"a": "12", "b": "", "c": ""},  # b mehrfach ueberschrieben
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "8": {  # s1-11
        "A1": {"a": "2x+7y", "b": "6a-22"},
        "A2": {"a": "3(2x+3)", "b": "4a(a-3)"},
        "A3": {"a": "8", "b": "7"},
        "B1": {"m": "-2", "b": "3", "liegt": "ja", "nullstelle": ""},
        "C1": {"a": "81", "b": "512", "c": "100"},
        "C2": {"a": "12", "b": "0,5", "c": ""},
        "D1": {"a": "10", "b": "12", "c": "7,07"},
        "D2": {"a": "0,222", "b": "0,5"},     # im Bogen "22,2 %" und "50 %"
    },
    "9": {  # s2-1
        "A1": {"a": "7y-3x", "b": ""},
        "A2": {"a": "4(8x)+72", "b": "3(6a^2-18a)"},
        "A3": {"a": "7", "b": "0,375"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "16", "b": "243", "c": "1000"},
        "C2": {"a": "13", "b": "0,6", "c": "8,485"},
        "D1": {"a": "15", "b": "15", "c": "12"},
        "D2": {"a": "4/10", "b": "2/10"},
    },
    "10": {  # s3-10
        "A1": {"a": "2+3y", "b": "8a-12-2a+10"},
        "A2": {"a": "", "b": ""},
        "A3": {"a": "", "b": ""},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "27", "b": "256", "c": ""},   # c unleserlich (Potenzschreibweise)
        "C2": {"a": "12", "b": "0,5", "c": ""},   # c durchgestrichen
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "11": {  # s3-01
        "A1": {"a": "3x+7y", "b": "4a-10"},
        "A2": {"a": "2(4x+6)", "b": "2a(3a-9)"},
        "A3": {"a": "7", "b": "5"},
        "B1": {"m": "2", "b": "-4", "liegt": "ja", "nullstelle": "2"},
        "C1": {"a": "16", "b": "243", "c": "1000"},
        "C2": {"a": "13", "b": "0,6", "c": ""},
        "D1": {"a": "10", "b": "15", "c": ""},
        "D2": {"a": "0,16", "b": "0,84"},     # im Bogen "16 %" und "84 %"
    },
    "12": {  # s2-5
        "A1": {"a": "2x+7y", "b": ""},        # b unleserlich
        "A2": {"a": "x+2,5", "b": "1a-3"},
        "A3": {"a": "8", "b": "2,5"},
        "B1": {"m": "3", "b": "-2x", "liegt": "", "nullstelle": ""},  # m und b vertauscht
        "C1": {"a": "", "b": "2^8", "c": "10^2"},  # Potenz notiert, nicht ausgerechnet
        "C2": {"a": "12", "b": "0,5", "c": ""},
        "D1": {"a": "10", "b": "169", "c": "25"},
        "D2": {"a": "", "b": ""},
    },
    "13": {  # s2-7
        "A1": {"a": "3x+7y", "b": "4a-10"},
        "A2": {"a": "", "b": ""},             # beide durchgestrichen
        "A3": {"a": "7", "b": "2"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "16", "b": "243", "c": ""},
        "C2": {"a": "", "b": "", "c": ""},    # a und b durchgestrichen
        "D1": {"a": "21cm", "b": "12,5cm", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "14": {  # s1-08
        "A1": {"a": "2x+7y", "b": "6a-2"},
        "A2": {"a": "3(2x+3)", "b": "4a(a-3)"},
        "A3": {"a": "8", "b": "7"},
        "B1": {"m": "-2", "b": "3", "liegt": "ja", "nullstelle": "1,5"},
        "C1": {"a": "243", "b": "1024", "c": "100"},
        "C2": {"a": "12", "b": "0,5", "c": "12,5"},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "16": {  # s3-04
        "A1": {"a": "2x+3y", "b": "6a-2"},
        "A2": {"a": "3(2x+3)", "b": "2a(2a-6)"},
        "A3": {"a": "8", "b": "7"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "81", "b": "512", "c": "100"},
        "C2": {"a": "12", "b": "0,5", "c": "7"},   # 7 statt 7,07
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "5/10", "b": "5/10"},
    },
    "17": {  # s1-04
        "A1": {"a": "2x+7y", "b": ""},        # b unleserlich
        "A2": {"a": "", "b": ""},
        "A3": {"a": "", "b": ""},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "", "b": "", "c": ""},
        "C2": {"a": "4", "b": "2,5", "c": "5"},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "18": {  # s2-2
        "A1": {"a": "3x+7y", "b": "4a-10"},
        "A2": {"a": "4(x+3)", "b": "3a(2a-6)"},
        "A3": {"a": "7", "b": "5"},
        "B1": {"m": "4", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "16", "b": "3^5", "c": "10^3"},  # Potenz notiert, nicht ausgerechnet
        "C2": {"a": "13", "b": "0,6", "c": "6√2"},
        "D1": {"a": "15", "b": "15", "c": "6√2"},
        "D2": {"a": "0,16", "b": "0,84"},     # im Bogen "16 %" / "84 %", NR 16/100 und 21/25
    },
    "19": {  # s3-02
        "A1": {"a": "2x+7y", "b": "8a-22-2a"},   # nicht zusammengefasst
        "A2": {"a": "3(2x+3)", "b": "2a(2a-6)"},
        "A3": {"a": "8", "b": "7"},
        "B1": {"m": "2", "b": "3", "liegt": "ja", "nullstelle": "1"},
        "C1": {"a": "81", "b": "512", "c": "100"},
        "C2": {"a": "12", "b": "0,5", "c": ""},  # c durchgestrichen
        "D1": {"a": "10", "b": "14", "c": "6"},
        "D2": {"a": "2/9", "b": "76/90"},
    },
    "20": {  # s3-07
        "A1": {"a": "3x+7y", "b": "7a-10"},
        "A2": {"a": "4(2x+3)", "b": "6a(a-3)"},
        "A3": {"a": "7", "b": "5"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "32", "b": "3^5", "c": ""},
        "C2": {"a": "13", "b": "", "c": ""},
        "D1": {"a": "21", "b": "9", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "21": {  # s2-6
        "A1": {"a": "2x+7y", "b": "6a-22"},
        "A2": {"a": "3(2x+3)", "b": "4a(a-3)"},
        "A3": {"a": "8", "b": "7"},
        "B1": {"m": "-2x", "b": "3", "liegt": "ja", "nullstelle": "6"},
        "C1": {"a": "81", "b": "27", "c": "10^2"},
        "C2": {"a": "12", "b": "0,5", "c": "2√25"},
        "D1": {"a": "48^2", "b": "12^2", "c": "7,9cm"},
        "D2": {"a": "0,222", "b": "27,78"},   # b: unter dem Kaestchen korrigiert auf 78,78 %
    },
    "22": {  # s3-09
        "A1": {"a": "3x+7y", "b": "6a-12-2a"},
        "A2": {"a": "4(2x+3)", "b": "6a(a-3)"},
        "A3": {"a": "7", "b": "5"},
        "B1": {"m": "2", "b": "-4", "liegt": "ja", "nullstelle": "2"},
        "C1": {"a": "16", "b": "81", "c": "1000"},
        "C2": {"a": "13", "b": "", "c": ""},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "23": {  # s3-06
        "A1": {"a": "2x+7y", "b": ""},
        "A2": {"a": "", "b": ""},
        "A3": {"a": "8", "b": ""},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "", "b": "", "c": ""},
        "C2": {"a": "", "b": "", "c": ""},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "24": {  # s1-09 - Kopf B, Antworten A (siehe VERSIONEN_ERSCHLOSSEN)
        "A1": {"a": "2x+7y", "b": "6a-22"},
        "A2": {"a": "", "b": ""},             # beide durchgestrichen
        "A3": {"a": "7,5", "b": "7"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "81", "b": "32", "c": "100"},
        "C2": {"a": "√12", "b": "√0,05", "c": "√5"},   # Wurzel nicht gezogen
        "D1": {"a": "10cm", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
    "25": {  # s1-10
        "A1": {"a": "3x+7y", "b": ""},
        "A2": {"a": "", "b": ""},
        "A3": {"a": "7", "b": ""},
        "B1": {"m": "", "b": "-4", "liegt": "", "nullstelle": ""},
        "C1": {"a": "16", "b": "243", "c": "1000"},
        "C2": {"a": "√13", "b": "√0,06", "c": "√8,4"},  # Wurzel nicht gezogen
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "0,133", "b": ""},        # NR 4/10 · 3/9 - ohne Zuruecklegen gerechnet
    },
    "26": {  # s3-08
        "A1": {"a": "2x+7y", "b": "6a-22"},
        "A2": {"a": "3(2x+9)", "b": "4a(a-3)"},
        "A3": {"a": "8", "b": "7"},
        "B1": {"m": "-2", "b": "3", "liegt": "", "nullstelle": ""},
        "C1": {"a": "", "b": "", "c": ""},
        "C2": {"a": "12", "b": "0,5", "c": ""},
        "D1": {"a": "14", "b": "8", "c": ""},
        "D2": {"a": "5/11", "b": ""},
    },
    "27": {  # s2-3
        "A1": {"a": "2x+7y", "b": ""},
        "A2": {"a": "", "b": ""},
        "A3": {"a": "1", "b": "1"},
        "B1": {"m": "-2x", "b": "3", "liegt": "ja", "nullstelle": ""},
        "C1": {"a": "81", "b": "64", "c": ""},
        "C2": {"a": "12", "b": "0,05", "c": ""},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "4/9", "b": "5/10"},
    },
    "28": {  # s1-07
        "A1": {"a": "3x+7y", "b": "4a-14"},
        "A2": {"a": "", "b": ""},
        "A3": {"a": "", "b": "-45"},
        "B1": {"m": "", "b": "", "liegt": "", "nullstelle": ""},
        "C1": {"a": "", "b": "", "c": ""},
        "C2": {"a": "", "b": "", "c": ""},
        "D1": {"a": "", "b": "", "c": ""},
        "D2": {"a": "", "b": ""},
    },
}

# Stellen, an denen der Scan keine sichere Lesung hergibt. Dort steht oben ""
# statt einer geratenen Antwort.
UNSICHER = [
    ("5", "C1b", "Ziffernfolge nicht eindeutig ('1?6')"),
    ("7", "C2b", "mehrfach ueberschrieben, Endwert nicht lesbar"),
    ("10", "C1c", "Potenzschreibweise mit Nebenrechnungen daneben, Endwert unklar"),
    ("10", "C2c", "durchgestrichen"),
    ("12", "A1b", "durchgehender Rechenweg im Kaestchen, kein Endergebnis lesbar"),
    ("12", "C1a", "Ziffer nicht lesbar"),
    ("17", "A1b", "Term nicht lesbar"),
    ("19", "C2c", "durchgestrichen"),
    ("2", "D1b", "'15,79' oder '18,79' - in beiden Faellen falsch"),
]

# Mathematisch richtig, aber anders geschrieben als im Schluessel -
# der Stringvergleich zaehlt das als falsch. Vor dem Gespraech mit der
# Klasse von Hand gutschreiben.
TERME_MANUELL = [
    ("5", "A1a", "7y+3x", "ist 3x+7y, nur umgestellt - richtig"),
    ("7", "A2b", "2a(2a-6)", "ausmultipliziert 4a^2-12a wie 4a(a-3), aber nicht "
                             "vollstaendig ausgeklammert"),
    ("11", "A2a", "2(4x+6)", "ergibt 8x+12 wie 4(2x+3), nicht vollstaendig ausgeklammert"),
    ("11", "A2b", "2a(3a-9)", "ergibt 6a^2-18a wie 6a(a-3), nicht vollstaendig ausgeklammert"),
    ("16", "A2b", "2a(2a-6)", "ergibt 4a^2-12a wie 4a(a-3), nicht vollstaendig ausgeklammert"),
    ("18", "A2b", "3a(2a-6)", "ergibt 6a^2-18a wie 6a(a-3), nicht vollstaendig ausgeklammert"),
    ("19", "A1b", "8a-22-2a", "ergibt 6a-22, aber nicht zusammengefasst"),
    ("19", "A2b", "2a(2a-6)", "ergibt 4a^2-12a wie 4a(a-3), nicht vollstaendig ausgeklammert"),
    ("21", "B1m", "-2x", "gemeint ist m = -2, das x gehoert nicht dazu - richtig"),
    ("27", "B1m", "-2x", "gemeint ist m = -2, das x gehoert nicht dazu - richtig"),
    ("5", "A2b", "2a(3a-9)", "ergibt 6a^2-18a wie 6a(a-3), nicht vollstaendig ausgeklammert"),
]
