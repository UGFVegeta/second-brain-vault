# -*- coding: utf-8 -*-
"""Selbsteinschätzung ('Ich?'-Smiley) je Aufgabe, Klasse 10b, Grundlagen 8-9.

Werte: "sicher", "ging_so", "unsicher", "" (kein Kreuz erkennbar).

WICHTIG zur Genauigkeit: Diese Lesung ist unsicherer als die der Antworten.
Auffaellig ist, wie viele Boegen die Smileys gar nicht angekreuzt haben -
das steht hier als "" und zaehlt im Bericht nicht als Einschaetzung mit.
Wer den Vergleich "sicher, aber falsch" im Gespraech nutzt, sollte die
betroffenen Zeilen vorher kurz gegen den Originalbogen halten.
"""

SELBSTEINSCHAETZUNG = {
    "1":  {"A1": "ging_so", "A2": "unsicher", "A3": "ging_so", "B1": "unsicher",
           "C1": "ging_so", "C2": "ging_so", "D1": "unsicher", "D2": "unsicher"},
    "2":  {"A1": "sicher", "A2": "ging_so", "A3": "sicher", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "3":  {"A1": "ging_so", "A2": "ging_so", "A3": "ging_so", "B1": "",
           "C1": "ging_so", "C2": "ging_so", "D1": "", "D2": ""},
    "4":  {"A1": "sicher", "A2": "ging_so", "A3": "sicher", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "5":  {"A1": "sicher", "A2": "sicher", "A3": "sicher", "B1": "",
           "C1": "ging_so", "C2": "ging_so", "D1": "", "D2": ""},
    "6":  {"A1": "sicher", "A2": "sicher", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "7":  {"A1": "sicher", "A2": "ging_so", "A3": "sicher", "B1": "ging_so",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "8":  {"A1": "", "A2": "", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "9":  {"A1": "ging_so", "A2": "sicher", "A3": "sicher", "B1": "unsicher",
           "C1": "ging_so", "C2": "unsicher", "D1": "sicher", "D2": "sicher"},
    "10": {"A1": "ging_so", "A2": "unsicher", "A3": "", "B1": "unsicher",
           "C1": "ging_so", "C2": "", "D1": "", "D2": ""},
    "11": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "B1": "sicher",
           "C1": "sicher", "C2": "unsicher", "D1": "ging_so", "D2": "sicher"},
    "12": {"A1": "sicher", "A2": "ging_so", "A3": "ging_so", "B1": "ging_so",
           "C1": "unsicher", "C2": "", "D1": "", "D2": ""},
    "13": {"A1": "ging_so", "A2": "sicher", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "ging_so", "D2": ""},
    "14": {"A1": "", "A2": "", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "16": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "B1": "unsicher",
           "C1": "ging_so", "C2": "ging_so", "D1": "", "D2": ""},
    "17": {"A1": "", "A2": "", "A3": "ging_so", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "18": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "B1": "unsicher",
           "C1": "sicher", "C2": "sicher", "D1": "sicher", "D2": "ging_so"},
    "19": {"A1": "", "A2": "", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "20": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "B1": "unsicher",
           "C1": "ging_so", "C2": "ging_so", "D1": "", "D2": ""},
    "21": {"A1": "sicher", "A2": "sicher", "A3": "", "B1": "",
           "C1": "sicher", "C2": "sicher", "D1": "sicher", "D2": "sicher"},
    "22": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "B1": "ging_so",
           "C1": "sicher", "C2": "unsicher", "D1": "", "D2": ""},
    "23": {"A1": "", "A2": "", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "24": {"A1": "", "A2": "", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "25": {"A1": "", "A2": "", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "26": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "B1": "ging_so",
           "C1": "", "C2": "sicher", "D1": "ging_so", "D2": "ging_so"},
    "27": {"A1": "", "A2": "", "A3": "", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
    "28": {"A1": "ging_so", "A2": "", "A3": "ging_so", "B1": "",
           "C1": "", "C2": "", "D1": "", "D2": ""},
}
