---
tags: [haus, tür, doorbird, siegenia, diagnose]
status: offen
date: 2026-07-12
---

# Haustür Motorschloss – DoorBird & Siegenia Diagnose

## Kurzfazit
Die Haustür lässt sich per DoorBird-App **nur sporadisch** elektrisch öffnen. Ursache ist mit hoher Wahrscheinlichkeit **thermischer Verzug des Türblatts durch starke Sonneneinstrahlung** – nicht DoorBird, nicht die Elektrik. Der Motor des Schlosses summt jedes Mal, kommt aber gegen den erhöhten Verriegelungsdruck der aufgeheizten Tür mal frei und mal nicht.

## Das Setup
- **Tür:** Aluminium-Haustür anthrazit, mit Seitenteil links (Wiederaufbau nach Hochwasser 2024/25, eingebaut von Bittermann & Weiss). Ursprünglich war eine **Weru**-Tür geplant – die konnte wegen des Hochwassers nicht mehr produzieren, daher Alternative über den Fensterlieferanten.
- **Motorschloss:** **Siegenia GENIUS** (Mehrfachverriegelung, Marke KFV/Siegenia).
- **Türsprechanlage:** DoorBird **D2101V** + Peripherie **Türcontroller** (DoorBird IP E/A Tür Controller) + Innenstation.
- **Verkabelung:** Das Schloss hängt am **Türcontroller, Relais 1 „Eingangstür"** (nicht am Relais der Außenstation).

## Was geprüft und ausgeschlossen wurde
- **Signalweg:** App → DoorBird → Relais kommt zuverlässig an (Schloss summt jedes Mal).
- **Richtiges Relais:** Türcontroller Relais 1 „Eingangstür".
- **Impulsdauer getestet:** 1 s → 3 s → 7 s. Half nicht. Bei 7 s reagierte die Tür nur träge.
- **Mechanik grob:** Tür lässt sich per Klinke jederzeit normal öffnen.

## Wichtige Erkenntnis / Korrektur
Laut **offizieller Siegenia-Fehlertabelle (GENIUS)** darf der Auslöse-Impuls **nicht länger als 1 s** sein – ein zu langer Impuls (> 1 s) *verhindert* das Entriegeln. Das Hochstellen auf 3 s/7 s war also falsch.
→ **DoorBird Türcontroller Relais 1 wieder auf 1 s gesetzt und gespeichert (Stand 12.07.2026).**

## Wahrscheinliche Ursache: Hitzeverzug
- Die Tür bekommt **den ganzen Tag volle Sonne** und heizt sich stark auf (spürbare Abstrahlwärme).
- Dunkles Aluminium dehnt sich stark aus → Türblatt „schüsselt", Druck auf die Verriegelungspunkte steigt → Motor kommt nicht frei.
- Passt lückenlos: „eine Woche ging's, dann nicht mehr", „nichts geändert" (geändert hat die Sonne), „summt aber öffnet nicht".
- Deckt sich mit Siegenia: bei „entriegelt schwergängig/nicht" zuerst **Umgebungstemperatur prüfen** und **Rahmenteile/Türbänder einstellen**.

## Nächster Schritt / Ansage für den Handwerker
Zuständig ist ein **Türbauer / Siegenia-Service-Partner** (Ansprechpartner noch klären – **nicht** Peter Leber/B&W laut Oskar). Aufgabe:
> Motorschloss Siegenia GENIUS entriegelt bei starker Sonneneinstrahlung/Hitze nur sporadisch (Motor summt, Tür gibt nicht frei, von Hand öffenbar). Verdacht auf thermischen Verzug. Bitte **Bänder, Schließbleche und Restfalzluft nachjustieren**, **Betriebsspannung (≥ 24 V) und Steckverbindungen des Antriebs prüfen**, ggf. **Referenzfahrt** neu ausführen. DoorBird-Ansteuerung ist geprüft (Impuls 1 s kommt zuverlässig an) – daran liegt es nicht.

## Bestätigungstest (bei nächstem Fehlversuch)
Tür kräftig Richtung Rahmen drücken (Schlossseite) **und gleichzeitig** per App auslösen. Geht sie dann auf → bestätigt Verzug/Dichtungsdruck als Ursache.

## Quellen
- Siegenia GENIUS – Fehlerursache und Abhilfe: https://docs.siegenia.com/manuals/H39.ELEKS013/de-DE/988090123.html
- Siegenia Türsysteme: https://www.siegenia.com/de/products/doorsystems
- DoorBird Türöffner/Relais-Info: https://www.doorbird.com/downloads/misc/door_opener_information_en.pdf
- WebAdmin (Konfiguration): https://webadmin.doorbird.com/login
