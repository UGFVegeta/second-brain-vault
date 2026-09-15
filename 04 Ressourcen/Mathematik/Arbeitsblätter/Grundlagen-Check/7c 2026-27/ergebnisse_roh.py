# -*- coding: utf-8 -*-
"""Rohtranskription der Antwortbögen 7c: Teil 1 (Block A+B, 25 Bögen) und
Teil 2 (Block C+D, 23 Bögen), zusammengeführt pro Nummer.

WICHTIG: von Hand aus Scans gelesen. Unsichere Stellen sind in UNSICHER
gelistet (Nummer, Item, Grund) - dort steht in ERGEBNISSE bewusst "" statt
einer geratenen Zahl, damit das Auswerteskript sie als "nicht bearbeitet"
zaehlt statt eine Falschlesung als Fehler zu werten.

Teil 1 und Teil 2 hatten nicht exakt dieselben Nummern anwesend: 12, 16, 18
und 21 fehlen in Teil 2 (zeigen im Bericht "nicht bearbeitet" bei C/D).
Nummer 1 und 29 fehlen in Teil 1 (zeigen "nicht bearbeitet" bei A/B) - 29
ist komplett neu, kam in Teil 1 nicht vor. Zwei Teil-2-Bögen hatten statt
einer Ziffer nur eine schwer lesbare Schleife - vorlaeufig als 8 und 9
eingetragen (9 existierte schon aus Teil 1), siehe UNSICHER.
"""

ERGEBNISSE = {
    "16": {
        "A1": {"a": "7292", "b": "506"},
        "A2": {"a": "27", "b": "30"},
        "A3": {"a": "21,27,33", "b": "nein"},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "5/6", "b": ""},          # b unklar/verwischt
        "B2": {"a": "4/1", "b": "2,1"},
        "B3": {"a": "2/3", "b": "1/2"},
        "B4": {"reihenfolge": ""},             # nicht als klare Reihenfolge lesbar
        "B5": {"ergebnis": "3/8"},
    },
    "26": {
        "A1": {"a": "8292", "b": "13104"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "21,27,33", "b": "nein"},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "2/5", "b": "6/12"},
        "B2": {"a": "400/40", "b": "3,4"},    # sehr unsicher, mehrfach korrigiert
        "B3": {"a": "1/3", "b": "3/4"},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "0,48"},
        "C2": {"a": "", "b": "250,0"},
        "C3": {"a": "4600", "b": "1230"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "9,4"},        # b unsicher, evtl. "2,4"
        "D2": {"a": "40", "b": "80"},
        "D3": {"a": "", "b": ""},
        "D4": {"a": "19,0", "b": ""},           # unsicher, evtl. "39,0"
    },
    "9": {
        "A1": {"a": "21,22", "b": "2424"},     # sehr unsicher gelesen
        "A2": {"a": "2723", "b": "29"},        # unsicher, durchgestrichen/korrigiert
        "A3": {"a": "27", "b": "75"},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "", "b": ""},
        "B2": {"a": "", "b": ""},
        "B3": {"a": "213", "b": ""},
        "B4": {"reihenfolge": "3/8;2/5;1/2;0,6"},
        "B5": {"ergebnis": "3"},
        # Teil-2-Bogen dieser Nummer nicht sicher zuzuordnen (siehe UNSICHER unten:
        # zwei Bögen mit unleserlicher Schleife statt Ziffer, vermutlich 8 und 9).
        "C1": {"a": "13,25", "b": "5,6"},
        "C2": {"a": "12", "b": "2500"},
        "C3": {"a": "4,000", "b": "12,00"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "", "b": "40"},
        "D3": {"a": "", "b": ""},
        "D4": {"a": "", "b": ""},
    },
    "15": {
        "A1": {"a": "8288", "b": "18504"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "29", "b": "33"},
        "A4": {"a": "1,2,6,12,24", "b": ""},
        "B1": {"a": "", "b": ""},
        "B2": {"a": "", "b": ""},
        "B3": {"a": "", "b": ""},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": ""},
        "C2": {"a": "", "b": ""},
        "C3": {"a": "4600", "b": "12,4"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "", "b": ""},
        "D3": {"a": "", "b": ""},
        "D4": {"a": "", "b": ""},
    },
    "13": {
        "A1": {"a": "8292", "b": "1294"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "23,29", "b": "ja"},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "4/9", "b": "18"},
        "B2": {"a": "40/10", "b": ""},
        "B3": {"a": "2/3", "b": "3/4"},
        "B4": {"reihenfolge": "1/2;3/5;3/8;0,6"},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "4800"},
        "C2": {"a": "12", "b": "25"},
        "C3": {"a": "4,600", "b": "13,00"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "350", "b": "240"},
        "D2": {"a": "40", "b": "89"},
        "D3": {"a": "48", "b": "60"},
        "D4": {"a": "19,0", "b": "21,0"},
    },
    "21": {
        "A1": {"a": "8292", "b": "13104"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "", "b": ""},
        "A4": {"a": "", "b": "Ich habe es nicht verstanden"},
        "B1": {"a": "2/3", "b": "1/2"},
        "B2": {"a": "", "b": ""},
        "B3": {"a": "2/3", "b": "3/4"},
        "B4": {"reihenfolge": "0,6;3/8;2/5;1/2"},
        "B5": {"ergebnis": ""},
    },
    "24": {
        "A1": {"a": "8292", "b": "1310"},      # b unklar, letzte Ziffer verwischt
        "A2": {"a": "", "b": "75"},             # a durchgestrichen/unleserlich
        "A3": {"a": "alle", "b": "20"},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "5/6", "b": ""},
        "B2": {"a": "0/4", "b": "9/4"},
        "B3": {"a": "2/3", "b": "9/12"},
        "B4": {"reihenfolge": "0,6;3/8;2/5;1/2"},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "0,48"},
        "C2": {"a": "", "b": "50"},
        "C3": {"a": "4600", "b": "10,00"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "26", "b": "40"},
        "D3": {"a": "60", "b": ""},
        "D4": {"a": "19", "b": "19"},
    },
    "7": {
        "A1": {"a": "8292", "b": "73104"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "23,29", "b": "ja"},
        "A4": {"a": "1,2,3,4,6,8,12,24", "b": "6"},
        "B1": {"a": "6/5", "b": "1/2"},
        "B2": {"a": "4/10", "b": "6,9"},
        "B3": {"a": "2/3", "b": "3/4"},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "2025", "b": "0,48"},       # a ohne Komma geschrieben
        "C2": {"a": "12", "b": "250,0"},
        "C3": {"a": "4,600", "b": "12,00"},
        "C4": {"a": "0,5", "b": "1,27"},
        "D1": {"a": "3.500", "b": "2,4"},
        "D2": {"a": "26", "b": "80"},
        "D3": {"a": "94", "b": "60"},
        "D4": {"a": "19", "b": "325"},
    },
    "10": {
        "A1": {"a": "8292", "b": "13104"},
        "A2": {"a": "27", "b": "45"},
        "A3": {"a": "29", "b": "ja"},
        "A4": {"a": "1,2,3,4,6,8,24", "b": "1,2,3,6"},
        "B1": {"a": "2/5", "b": "2/7"},
        "B2": {"a": "4/9", "b": "0,9"},
        "B3": {"a": "2/3", "b": "3/4"},
        "B4": {"reihenfolge": "2/5;0,6;3/8;1/2"},
        "B5": {"ergebnis": "1/2"},
        "C1": {"a": "20,25", "b": "0,48"},
        "C2": {"a": "", "b": "250,0"},
        "C3": {"a": "4,600", "b": "12,30"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "26", "b": "80"},
        "D3": {"a": "94", "b": ""},
        "D4": {"a": "19", "b": "325"},
    },
    "19": {
        "A1": {"a": "8291", "b": "13104"},
        "A2": {"a": "2727", "b": "75"},
        "A3": {"a": "", "b": ""},
        "A4": {"a": "1,23,4,6,8,12,24", "b": ""},
        "B1": {"a": "2/5", "b": "1/7"},
        "B2": {"a": "4/7", "b": "4,9"},
        "B3": {"a": "2/3", "b": "3/4"},
        "B4": {"reihenfolge": "2/5;0,6;3/8;1/2"},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "0,48"},      # a stark korrigiert, C2a unleserlich
        "C2": {"a": "", "b": "250,0"},
        "C3": {"a": "4,600", "b": "12,00"},
        "C4": {"a": "", "b": "7,12"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "26", "b": "80"},
        "D3": {"a": "94", "b": "60"},
        "D4": {"a": "19", "b": "325"},
    },
    "6": {
        "A1": {"a": "8286", "b": "13104"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "29,23", "b": "ja"},
        "A4": {"a": "12", "b": "2"},
        "B1": {"a": "1/5", "b": "3/7"},
        "B2": {"a": "0/4", "b": "94dm"},
        "B3": {"a": "2/3", "b": "3/4"},
        "B4": {"reihenfolge": "0,6;3/5;3/8;7"},
        "B5": {"ergebnis": "3/4"},
        "C1": {"a": "3,4", "b": "2,4"},         # ursprünglich 20,25/4,8 geschrieben, dann korrigiert
        "C2": {"a": "7,7", "b": "250,0"},
        "C3": {"a": "2,3", "b": "12,30"},       # a ursprünglich 4,600, dann korrigiert
        "C4": {"a": "0,5", "b": "1,2"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "28", "b": "52"},
        "D3": {"a": "24", "b": "77"},           # a ursprünglich 17, dann korrigiert
        "D4": {"a": "19", "b": "19"},
    },
    "2": {
        "A1": {"a": "8292", "b": "13104"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "", "b": ""},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "", "b": ""},
        "B2": {"a": "", "b": ""},
        "B3": {"a": "", "b": ""},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "4,8"},
        "C2": {"a": "", "b": ""},
        "C3": {"a": "4,600", "b": "12,30"},
        "C4": {"a": ">", "b": "<"},
        "D1": {"a": "", "b": ""},
        "D2": {"a": "", "b": ""},
        "D3": {"a": "24v", "b": "17v"},         # ungewöhnliche Einheit "v", so übernommen
        "D4": {"a": "19", "b": ""},
    },
    "17": {
        "A1": {"a": "8292", "b": "12004"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "21,23,29,33", "b": "ja"},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "2/5", "b": "1/3"},
        "B2": {"a": "1/4", "b": "10,4"},
        "B3": {"a": "1/3", "b": "3/3"},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "5,14"},
        "C2": {"a": "", "b": ""},
        "C3": {"a": "4,570", "b": "12,30"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "", "b": ""},
        "D3": {"a": "60", "b": "47"},
        "D4": {"a": "19", "b": ""},
    },
    "18": {
        "A1": {"a": "8292", "b": ""},
        "A2": {"a": "72", "b": "125"},
        "A3": {"a": "21,27,29", "b": "ja"},
        "A4": {"a": "24:2=12", "b": "4,12"},
        "B1": {"a": "2/3", "b": "6/16"},
        "B2": {"a": "0/4", "b": ""},
        "B3": {"a": "4/6", "b": "4/12"},
        "B4": {"reihenfolge": "2,0,3;3,5,1,10"},
        "B5": {"ergebnis": "3/4"},
    },
    "14": {
        "A1": {"a": "8292", "b": ""},
        "A2": {"a": "17", "b": "75"},
        "A3": {"a": "23,29", "b": "non"},
        "A4": {"a": "T24=12", "b": "6"},
        "B1": {"a": "", "b": ""},
        "B2": {"a": "4/4", "b": "0,94"},
        "B3": {"a": "", "b": ""},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "19,53", "b": "4,8"},
        "C2": {"a": "1,3", "b": ""},
        "C3": {"a": "4600", "b": "12,30"},       # C3a im Bogen mehrfach übermalt, "4600" außen notiert
        "C4": {"a": "", "b": ""},
        "D1": {"a": "0,35", "b": "2,4"},
        "D2": {"a": "40", "b": ""},
        "D3": {"a": "", "b": ""},
        "D4": {"a": "", "b": "21"},
    },
    "5": {
        "A1": {"a": "7492", "b": ""},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "23,27", "b": "nein"},
        "A4": {"a": "", "b": "24"},
        "B1": {"a": "", "b": ""},
        "B2": {"a": "", "b": ""},
        "B3": {"a": "", "b": ""},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": ""},
        "C2": {"a": "", "b": "25,00"},
        "C3": {"a": "4,607", "b": "12,30"},
        "C4": {"a": ">", "b": ">"},
        "D1": {"a": "0,35", "b": "24,00"},
        "D2": {"a": "40", "b": ""},
        "D3": {"a": "60", "b": ""},
        "D4": {"a": "", "b": "21"},
    },
    "25": {
        "A1": {"a": "8292", "b": "4102 1"},   # sehr unsicher, mehrfach korrigiert
        "A2": {"a": "75", "b": "27"},          # a/b evtl. vertauscht notiert
        "A3": {"a": "23,29,33", "b": "ja"},
        "A4": {"a": "2,4,6,8,12", "b": "6"},
        "B1": {"a": "1/3", "b": "6/9"},
        "B2": {"a": "1/9", "b": "9,4"},
        "B3": {"a": "1/4", "b": "3/4"},
        "B4": {"reihenfolge": "3/8;0,6;2/5;1/2"},
        "B5": {"ergebnis": "8/4"},
        "C1": {"a": "20,25", "b": "4,8"},
        "C2": {"a": "2,1", "b": "250,0"},
        "C3": {"a": "4500", "b": "10,00"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},        # a stark übermalt/korrigiert
        "D2": {"a": "40", "b": "26"},           # a/b evtl. vertauscht notiert
        "D3": {"a": "16", "b": "60"},
        "D4": {"a": "9,5", "b": "19"},
    },
    "11": {
        "A1": {"a": "8392", "b": "2174"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "21,29,33", "b": "ja"},
        "A4": {"a": "2,4,6,8,10,12,15,18,20,22,24", "b": ""},
        "B1": {"a": "3/4", "b": "9/8"},
        "B2": {"a": "4/10", "b": "9,4"},
        "B3": {"a": "4/6", "b": "9/12"},
        "B4": {"reihenfolge": "0,6;1/2;2/5;3/8"},
        "B5": {"ergebnis": ""},
        "C1": {"a": "189,620", "b": "5"},       # sehr unsicher, siehe UNSICHER
        "C2": {"a": "", "b": "2,500"},
        "C3": {"a": "4,500", "b": "12,00"},
        "C4": {"a": ">", "b": "<"},
        "D1": {"a": "3,50", "b": "24"},
        "D2": {"a": "", "b": "89"},
        "D3": {"a": "", "b": ""},
        "D4": {"a": "21,0", "b": ""},
    },
    "23": {
        "A1": {"a": "8292", "b": "20602"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "27,23,33", "b": "nein"},
        "A4": {"a": "", "b": ""},
        "B1": {"a": "", "b": ""},
        "B2": {"a": "10/4", "b": ""},
        "B3": {"a": "6", "b": ""},
        "B4": {"reihenfolge": "1/2;2/5;3/8;0,6"},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "4,8"},
        "C2": {"a": "", "b": ""},
        "C3": {"a": "", "b": ""},
        "C4": {"a": "0,5", "b": "1,2"},
        "D1": {"a": "", "b": ""},
        "D2": {"a": "", "b": ""},
        "D3": {"a": "", "b": ""},
        "D4": {"a": "", "b": ""},
    },
    "4": {
        "A1": {"a": "8292", "b": "10009"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "21", "b": "ja"},
        "A4": {"a": "12", "b": "20"},
        "B1": {"a": "", "b": ""},
        "B2": {"a": "", "b": ""},
        "B3": {"a": "7", "b": "7/6"},
        "B4": {"reihenfolge": "1/2;3/8;2/5;1/3"},
        "B5": {"ergebnis": "7/8"},
        "C1": {"a": "20,05", "b": "3,8"},
        "C2": {"a": "12", "b": "250"},
        "C3": {"a": "4600", "b": "12"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "26", "b": ""},
        "D3": {"a": "24", "b": ""},
        "D4": {"a": "19", "b": ""},
    },
    "20": {
        "A1": {"a": "8292", "b": "13104"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "21", "b": "nein"},
        "A4": {"a": "12", "b": "20"},
        "B1": {"a": "2/5", "b": ""},
        "B2": {"a": "", "b": "21/4"},
        "B3": {"a": "", "b": ""},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "0,48"},
        "C2": {"a": "", "b": "250"},
        "C3": {"a": "4600", "b": "1200"},       # a stark durchgestrichen, außen wiederholt
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "26", "b": "40"},
        "D3": {"a": "40", "b": ""},             # stark durchgestrichen
        "D4": {"a": "21", "b": "19"},
    },
    "22": {
        "A1": {"a": "8292", "b": "13104"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "21", "b": "ja"},
        "A4": {"a": "12", "b": "20"},
        "B1": {"a": "2/5", "b": "3/4"},
        "B2": {"a": "", "b": "21/4"},
        "B3": {"a": "2/3", "b": "3/4"},
        "B4": {"reihenfolge": ""},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "0,48"},
        "C2": {"a": "", "b": "2500"},
        "C3": {"a": "4600", "b": "1230"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "24"},
        "D2": {"a": "26", "b": "40"},
        "D3": {"a": "40", "b": ""},
        "D4": {"a": "21", "b": "19"},
    },
    "12": {
        "A1": {"a": "8092", "b": "131100"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "23,33", "b": "ja"},
        "A4": {"a": "1,2,3,4,8,24", "b": "3"},
        "B1": {"a": "1/3", "b": "3/8"},
        "B2": {"a": "9/4", "b": "4,9"},
        "B3": {"a": "2/3", "b": "2/4"},
        "B4": {"reihenfolge": "3/8;0,6;2/5;1/2"},
        "B5": {"ergebnis": ""},
    },
    "3": {
        "A1": {"a": "8292", "b": "1294"},
        "A2": {"a": "27", "b": "75"},
        "A3": {"a": "28,23", "b": "ja"},
        "A4": {"a": "24:1,6,12,18,24", "b": "6"},
        "B1": {"a": "2/4/9", "b": "18"},
        "B2": {"a": "0", "b": ""},
        "B3": {"a": "2/4", "b": "3/4"},
        "B4": {"reihenfolge": "1/2;2/5;3/8;9/0,6"},
        "B5": {"ergebnis": ""},
        "C1": {"a": "20,25", "b": "48,00"},
        "C2": {"a": "12", "b": "25"},
        "C3": {"a": "4,600", "b": "12,30"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "", "b": "240"},            # a unleserlich (mehrfach übermalt)
        "D2": {"a": "40", "b": "80"},
        "D3": {"a": "", "b": "60"},             # a durchgestrichen/unleserlich
        "D4": {"a": "", "b": "21,0"},           # a durchgestrichen/unleserlich
    },
    "1": {
        # Nummer war in Teil 1 nicht dabei (siehe ergebnisse_roh.py-Dokumentation
        # dort) - hier nur Teil 2, Block A/B zaehlen fuer diese Nummer als "nicht
        # bearbeitet".
        "C1": {"a": "2025", "b": "0,48"},       # a ohne Komma geschrieben
        "C2": {"a": "", "b": "50"},
        "C3": {"a": "4600", "b": "10,00"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "26", "b": "40"},
        "D3": {"a": "60", "b": ""},
        "D4": {"a": "19", "b": ""},
    },
    "8": {
        # Nummer auf dem Bogen nur als schwer lesbare Schleife geschrieben, nicht
        # als eindeutige Ziffer - siehe UNSICHER unten. Tentative Zuordnung.
        "C1": {"a": "20,25", "b": "0,48"},
        "C2": {"a": "12", "b": "250"},
        "C3": {"a": "4600", "b": "12,00"},
        "C4": {"a": "<", "b": ">"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "26", "b": "40"},
        "D3": {"a": "", "b": ""},               # durchgestrichen, unleserlich
        "D4": {"a": "19", "b": "21"},
    },
    "29": {
        # Neue Nummer, kam in Teil 1 nicht vor. Bogen hatte einen (nicht
        # uebernommenen) Vornamen im Klasse-Feld - siehe README.
        "C1": {"a": "19,53", "b": "40"},
        "C2": {"a": "", "b": "25,00"},
        "C3": {"a": "4,600", "b": "12,30"},
        "C4": {"a": "<", "b": "<"},
        "D1": {"a": "3500", "b": "2,4"},
        "D2": {"a": "40", "b": ""},
        "D3": {"a": "60", "b": ""},
        "D4": {"a": "", "b": ""},
    },
}

# Bogen mit leerem Nummernfeld (Seite 6 der PDF). Antworten vorhanden,
# aber keiner Nummer zuordenbar - Platzhalter, bis Oskar die Nummer klaert.
ERGEBNISSE_OHNE_NUMMER = {
    "A1": {"a": "8292", "b": "13104"},   # b mehrfach korrigiert, unsicher
    "A2": {"a": "", "b": "75"},           # a durchgestrichen/unleserlich
    "A3": {"a": "23,29", "b": "ja"},
    "A4": {"a": "1,2,3,4,6,8,12,24", "b": "6"},
    "B1": {"a": "", "b": ""},
    "B2": {"a": "4/10", "b": ""},
    "B3": {"a": "", "b": "9/12"},        # a nicht lesbar
    "B4": {"reihenfolge": ""},
    "B5": {"ergebnis": ""},
}
LEER_NUMMER_SEITE = 6

UNSICHER = [
    ("16", "B1b, B4", "Ziffern nicht eindeutig, als offen gewertet"),
    ("26", "B2, B4", "mehrfach korrigiert/überschrieben"),
    ("9", "A1, A2", "sehr unsicher, evtl. vertauschte Felder"),
    ("24", "A1b, A2a", "Ziffer verwischt bzw. durchgestrichen"),
    ("25", "A1b, A2", "mehrfach korrigiert, a/b evtl. vertauscht"),
    # --- Teil 2 (Block C+D) ---
    ("8/9", "Nummernfeld", "Zwei Teil-2-Bögen hatten statt einer Ziffer nur eine "
     "schwer lesbare Schleife. Vorlaeufig 8 = Bogen mit leerem Klasse/Datum-Feld "
     "und durchweg sicheren Antworten, 9 = Bogen mit Klasse 7C/Datum 15.9.2026 "
     "und Haekchen statt Kreisen bei der Selbsteinschaetzung. Gegen die "
     "Originalbögen pruefen, bevor die Zuordnung fuer ein Gespraech genutzt wird."),
    ("11", "C1", "Antwort weicht stark vom erwarteten Wert ab (189,620/5 statt "
     "20,25/0,48) - so auf dem Bogen, keine Lesefehler-Korrektur"),
    ("26", "D1b, D4a", "Ziffer unsicher: evtl. 2,4 statt 9,4 bzw. 19,0 statt 39,0"),
    ("29", "Klasse-Feld, C2a, D3b, D4", "Klasse-Feld enthielt einen Vornamen "
     "(nicht übernommen); mehrere Felder durchgestrichen/unleserlich. Neue "
     "Nummer, kam in Teil 1 nicht vor."),
    ("3", "D1a, D3a, D4a", "mehrfach durchgestrichen/übermalt, nicht lesbar"),
    ("6", "C1, C3, D3", "Antworten korrigiert (durchgestrichen + neu geschrieben), "
     "hier steht jeweils die finale Korrektur"),
]

# In Teil 1 vorhanden, in Teil 2 kein Bogen gefunden (zeigen "nicht bearbeitet"
# bei den Bloecken C/D im Bericht):
FEHLT_IN_TEIL2 = ["12", "16", "18", "21"]
