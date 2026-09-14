# -*- coding: utf-8 -*-
"""Selbsteinschätzung ('Ich?'-Smiley) je Aufgabe, Teil 1, Klasse 7c.

Werte: "sicher", "ging_so", "unsicher", "" (kein Kreuz/Kreis erkennbar).

WICHTIG zur Genauigkeit: Diese Lesung ist UNSICHERER als die der Zahlenwerte
in ergebnisse_roh.py. Viele Kinder haben zwei Smileys teilweise überlappend
markiert oder mehrfach korrigiert. Wo zwei Smileys angekreuzt/umkreist waren,
steht hier die nach Augenschein wahrscheinlichere, endgültige Wahl - nicht
geraten, aber mit spürbar geringerer Sicherheit als die Antworttexte.
Vor einer Verwendung in echten Gesprächen gegen die Originalbögen prüfen,
besonders bei den mit "?" markierten Zeilen.
"""

SELBSTEINSCHAETZUNG = {
    "16": {"A1": "ging_so", "A2": "sicher", "A3": "unsicher", "A4": "unsicher",
           "B1": "sicher", "B2": "sicher", "B3": "ging_so", "B4": "", "B5": "sicher"},
    "26": {"A1": "sicher", "A2": "sicher", "A3": "ging_so", "A4": "",
           "B1": "", "B2": "", "B3": "", "B4": "unsicher", "B5": ""},
    "9":  {"A1": "sicher", "A2": "unsicher", "A3": "", "A4": "",
           "B1": "", "B2": "", "B3": "sicher", "B4": "sicher", "B5": "unsicher"},
    "15": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "A4": "sicher",
           "B1": "", "B2": "", "B3": "", "B4": "", "B5": ""},
    "13": {"A1": "unsicher", "A2": "unsicher", "A3": "unsicher", "A4": "unsicher",
           "B1": "unsicher", "B2": "unsicher", "B3": "ging_so", "B4": "", "B5": "unsicher"},
    "21": {"A1": "sicher", "A2": "sicher", "A3": "", "A4": "ging_so",
           "B1": "sicher", "B2": "unsicher", "B3": "", "B4": "", "B5": "unsicher"},
    "24": {"A1": "unsicher", "A2": "unsicher", "A3": "sicher", "A4": "sicher",
           "B1": "sicher", "B2": "sicher", "B3": "sicher", "B4": "", "B5": "sicher"},
    "7":  {"A1": "sicher", "A2": "", "A3": "", "A4": "unsicher",
           "B1": "", "B2": "unsicher", "B3": "", "B4": "unsicher", "B5": ""},
    "10": {"A1": "unsicher", "A2": "unsicher", "A3": "unsicher", "A4": "unsicher",
           "B1": "unsicher", "B2": "unsicher", "B3": "", "B4": "unsicher", "B5": "unsicher"},
    "19": {"A1": "", "A2": "unsicher", "A3": "unsicher", "A4": "unsicher",
           "B1": "unsicher", "B2": "", "B3": "unsicher", "B4": "ging_so", "B5": "unsicher"},
    "6":  {"A1": "ging_so", "A2": "sicher", "A3": "sicher", "A4": "sicher",
           "B1": "unsicher", "B2": "sicher", "B3": "", "B4": "unsicher", "B5": "unsicher"},
    "2":  {"A1": "unsicher", "A2": "unsicher", "A3": "", "A4": "",
           "B1": "", "B2": "", "B3": "", "B4": "", "B5": ""},
    "17": {"A1": "sicher", "A2": "sicher", "A3": "unsicher", "A4": "",
           "B1": "", "B2": "unsicher", "B3": "unsicher", "B4": "", "B5": ""},
    "18": {"A1": "ging_so", "A2": "unsicher", "A3": "ging_so", "A4": "unsicher",
           "B1": "sicher", "B2": "ging_so", "B3": "sicher", "B4": "unsicher", "B5": "unsicher"},
    "14": {"A1": "", "A2": "sicher", "A3": "", "A4": "",
           "B1": "", "B2": "", "B3": "", "B4": "", "B5": "unsicher"},
    "5":  {"A1": "sicher", "A2": "sicher", "A3": "", "A4": "unsicher",
           "B1": "unsicher", "B2": "unsicher", "B3": "unsicher", "B4": "unsicher", "B5": "unsicher"},
    "25": {"A1": "ging_so", "A2": "ging_so", "A3": "ging_so", "A4": "ging_so",
           "B1": "unsicher", "B2": "", "B3": "ging_so", "B4": "unsicher", "B5": "ging_so"},
    "11": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "A4": "",
           "B1": "sicher", "B2": "", "B3": "", "B4": "sicher", "B5": "unsicher"},
    "23": {"A1": "unsicher", "A2": "unsicher", "A3": "unsicher", "A4": "unsicher",
           "B1": "unsicher", "B2": "unsicher", "B3": "unsicher", "B4": "unsicher", "B5": "unsicher"},
    "4":  {"A1": "", "A2": "sicher", "A3": "unsicher", "A4": "unsicher",
           "B1": "unsicher", "B2": "unsicher", "B3": "", "B4": "", "B5": ""},
    "20": {"A1": "unsicher", "A2": "sicher", "A3": "unsicher", "A4": "unsicher",
           "B1": "unsicher", "B2": "unsicher", "B3": "", "B4": "", "B5": ""},
    "22": {"A1": "", "A2": "sicher", "A3": "unsicher", "A4": "",
           "B1": "sicher", "B2": "", "B3": "sicher", "B4": "unsicher", "B5": ""},
    "12": {"A1": "sicher", "A2": "sicher", "A3": "sicher", "A4": "unsicher",
           "B1": "sicher", "B2": "sicher", "B3": "sicher", "B4": "", "B5": ""},
    "3":  {"A1": "sicher", "A2": "", "A3": "sicher", "A4": "",
           "B1": "", "B2": "", "B3": "", "B4": "unsicher", "B5": "unsicher"},
}

SELBSTEINSCHAETZUNG_OHNE_NUMMER = {
    "A1": "ging_so", "A2": "ging_so", "A3": "ging_so", "A4": "unsicher",
    "B1": "unsicher", "B2": "", "B3": "ging_so", "B4": "", "B5": "",
}
