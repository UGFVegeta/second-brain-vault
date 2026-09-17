---
tags: [bereich, energie, pv, solar]
status: aktiv
---

# PV-Anlage & Energie

## Anlage
- **Inbetriebnahme:** 20.03.2025 (Anlage und Speicher)
- **Leistung:** 12,6 kWp brutto, 30 Module, Südausrichtung, 22° Neigung
- **Wechselrichter:** Kostal Plenticore, 10 kW (IP: 192.168.178.48)
- **Speicher:** 12,8 kWh nutzbar, DC-gekoppelt, Lithium, max. 6,5 kW Entladeleistung, kein Notstrom
- **PV-Strings:** 2
- **Einspeiseart:** Teileinspeisung (Überschusseinspeisung)
- **Anschlussnetzbetreiber:** Syna GmbH
- **Installateur:** HSL Solar GmbH
- **Live-Daten:** `python3 .scripts/kostal_live.py`

Quelle Anlagendaten: MaStR-Datenblatt von HSL Solar (Mail vom 24.03.2025).

---

## Einspeisevergütung

Maßgeblich ist das Inbetriebnahmedatum 20.03.2025, das fällt in den EEG-Zeitraum 01.02.2025 bis 31.07.2025. Der Satz steht damit für 20 Jahre fest.

| Anlagenteil | Satz Teileinspeisung |
|---|---|
| bis 10 kWp | 7,94 ct/kWh |
| 10 bis 40 kWp (hier 2,6 kWp) | 6,88 ct/kWh |
| **Mischsatz für 12,6 kWp** | **7,72 ct/kWh** |

**Ertrag daraus:**
- Kalenderjahr 2026 bis 17.09.: 8.276 kWh → 639 €
- Seit Inbetriebnahme: 16.875 kWh → 1.303 €
- Volles Jahr: ~9.000 bis 9.500 kWh → ~700 € (geschätzt)

⚠️ Zwei Vorbehalte:
- **Solarspitzengesetz:** Für Anlagen ab dem 25.02.2025 entfällt die Vergütung in Zeiten negativer Börsenpreise (2025: 573 Stunden, überwiegend mittags). Bei Anlagen unter 100 kW greift das erst nach Ablauf des Jahres, in dem das intelligente Messsystem eingebaut wird. Ob es hier schon zieht, ist ungeklärt.
- **60-Prozent-Regel:** Neuanlagen von 2 bis 100 kWp ohne Smart Meter dürfen höchstens 60 % der installierten Leistung einspeisen. Ob und wie das hier umgesetzt ist, ist nicht geprüft.

### Auszahlungen von Syna (Stand 17.09.2026)

Syna zahlt monatliche Abschläge und rechnet einmal im Jahr ab. Die Abrechnung kommt per Post, im Postfach liegt dazu nichts. Belegt über die Kontoumsätze, Kundennummer 310223665.

| Zeitraum | Zahlungen | Summe |
|---|---|---|
| 15.04. bis 15.12.2025, monatlich 61 € | 9 | 549,00 € |
| 22.05.2026, Jahresabrechnung | 1 | 389,84 € |
| 15.06. bis 15.09.2026, monatlich 39 € | 4 | 156,00 € |
| **Gesamt seit Inbetriebnahme** | **14** | **1.094,84 €** |

Von Januar bis April 2026 kam nichts, die Abrechnung im Mai hat das aufgefangen.

**Der Mischsatz von 7,72 ct/kWh ist damit bestätigt:** Abschläge und Abrechnung der ersten Periode ergeben zusammen 938,84 €, das entspricht 12.161 kWh. Genau so viel hat die Anlage bis Ende April/Mai 2026 eingespeist. Umsatzsteuer kommt nicht obendrauf, es gilt also die Kleinunternehmerregelung.

⚠️ **Der Abschlag ist seit Juni 2026 zu niedrig.** Syna hat von 61 € auf 39 € gesenkt, also von 732 € auf 468 € im Jahr. Bei rund 9.000 kWh Einspeisung stehen aber etwa 700 € im Jahr zu. Gegenprobe über den Zähler: 17.100 kWh × 7,72 ct sind 1.320 €, ausgezahlt sind 1.094,84 €. Es liegen also rund 225 € bei Syna, die erst bei der nächsten Abrechnung kommen. Bei Syna anrufen und den Abschlag wieder auf 60 € setzen lassen.

---

## Stromverträge

| | Haushalt | Wärmepumpe |
|---|---|---|
| Vertragsnummer | 701055910928 | 701055470353 |
| Tarif | EnBW Planbar und Sicher Privatstrom (seit 20.05.2025) | EnBW Grün und Sicher Privatstrom |
| **Zählernummer** | **1ISK0092257941** | **1ISK0092257936** |
| Marktlokation | 50283471560 | 50283471362 |
| Abschlag | 44 €/Monat (seit 17.04.2026) | 60 €/Monat |
| Preise brutto | 40,07 ct/kWh, 18,30 €/Monat Grundpreis | 38,57 ct/kWh, 18,30 €/Monat Grundpreis |
| Letzte Abrechnung | 17.03.2026 für 17.03.2025 bis 16.03.2026 | noch keine |

Der alte Gewerbevertrag 701044438696 (Zähler 1ISK0071589912) wurde im Juli 2026 gekündigt.

**Jahresrechnung Haushalt (17.03.2025 bis 16.03.2026):** 755 kWh Netzbezug, 522,14 € Stromkosten, 760 € Abschläge gezahlt, 9,38 € Messkosten erstattet → **247,24 € Guthaben**.

Der Abschlag von 44 € ist belastbar: EnBW hat ihn nach einem vollen Jahr mit gemessenem Verbrauch festgelegt, vorher waren es 60 € und es gab 247,24 € zurück.

### Zählerstände vom 17.09.2026 (abfotografiert)

Zähler 1ISK0092257936 ist ein Zweirichtungszähler, über ihn läuft auch die PV-Einspeisung:

| Register | Stand | Bedeutung |
|---|---|---|
| 1.8.0 | 2.519 kWh | Bezug aus dem Netz seit Zählerbeginn (~20.03.2025) |
| 2.8.0 | 17.100 kWh | Einspeisung ins Netz |

![[Zählerstand 1ISK0092257936 2026-09-17 Bezug.jpg]]
![[Zählerstand 1ISK0092257936 2026-09-17 Einspeisung.jpg]]

Die 17.100 kWh bestätigen die Wechselrichterdaten: Der Kostal hatte am selben Tag 16.875 kWh errechnet, 1,3 % Abweichung. Anzeige in ganzen kWh, ohne Nachkommastelle.

**Damit ist der Verbrauch der Wärmepumpe bekannt: 2.519 kWh in rund 18 Monaten, also etwa 1.680 kWh im Jahr** — mit einem vollen Winter darin. Das liegt unter den 2.400 kWh aus dem Formular und über den 1.300 kWh, die EnBWs Abschlag unterstellt.

| | pro Jahr |
|---|---|
| 1.680 kWh × 38,57 ct | 648 € |
| Grundpreis | 220 € |
| **Kosten Wärmepumpe** | **868 €** |
| Abschlag | 720 € |
| **Unterdeckung** | **rund 150 €** |

Bei einer ersten Abrechnung über 16 bis 17 Monate sind das grob 200 bis 260 € Nachzahlung (~geschätzt).

⚠️ Offen bleibt, welches Register 1.8.0 und welches 2.8.0 ist. Die Zuordnung stammt aus der unscharfen Displaybeschriftung plus dem Abgleich mit dem Wechselrichter. Am Zähler durchtippen und prüfen, ob bei 2.8.0 wirklich die 17.100 stehen.

---

## Stromkosten unterm Strich

| Posten | pro Jahr | Grundlage |
|---|---|---|
| Haushalt | 522 € | abgerechnet 17.03.2025 bis 16.03.2026 |
| Wärmepumpe | 868 € | Zählerstand 17.09.2026, hochgerechnet |
| Einspeisung Syna | −750 € | Kontoauszüge, ~geschätzt über das Jahr |
| **Netto** | **rund 640 €** | etwa 53 € im Monat |

Bestätigt wird das erst mit der Abrechnung der Wärmepumpe. ### Einordnung

Das Haus verbraucht insgesamt rund 7.000 kWh im Jahr für Haushalt, Warmwasser und Heizung: 2.435 kWh aus dem Netz (beide Zähler) und etwa 4.300 kWh aus eigener PV und Batterie. Für 190 m² und vier Personen ist das ein normaler Wert — gespart wird nicht am Verbrauch, sondern am Zukauf.

Ohne PV müssten diese 7.000 kWh voll gekauft werden, je nach Tarif 2.600 bis 3.200 € im Jahr (~geschätzt). Die Anlage spart also grob 2.100 bis 2.550 € jährlich. Auf die Wohnfläche gerechnet zahlt ihr 3,37 € pro m² und Jahr für Strom und Heizung, üblich sind eher 14 bis 17 €.

Ohne die Einspeisevergütung gerechnet liegt der reine Energieeinkauf bei 1.390 € im Jahr. Nicht enthalten sind die Anschaffungskosten der Anlage.

---

## Jahresdaten (Stand 17.09.2026)

Direkt aus dem Wechselrichter, `scb:statistic:EnergyFlow`. „Jahr" ist das laufende Kalenderjahr 2026, „Gesamt" seit dem 20.03.2025.

| Kennzahl | Heute | Monat | Jahr | Gesamt |
|---|---|---|---|---|
| **PV-Ertrag** | 33,5 kWh | 824,4 kWh | 12.050 kWh | 23.739 kWh |
| **Einspeisung** | 24,5 kWh | 598,8 kWh | 8.276 kWh | 16.875 kWh |
| **Autarkie** | 99,6 % | 99,5 % | 76,8 % | 77,9 % |
| **Eigenverbrauch** | 17,0 % | 25,1 % | 29,2 % | 26,8 % |
| **CO2 gespart** | 23,4 kg | 577 kg | 8,44 t | 16,62 t |

### Hausverbrauch
| Quelle | Jahr 2026 | Anteil | Gesamt |
|---|---|---|---|
| PV direkt | 1.886 kWh | 41,1 % | 3.415 kWh |
| Batterie | 1.633 kWh | 35,6 % | 2.952 kWh |
| Netz | 1.065 kWh | 23,2 % | 1.809 kWh |
| **Summe** | **4.584 kWh** | | **8.176 kWh** |

Hochgerechnet liegt der Hausverbrauch bei etwa 5.500 bis 6.000 kWh im Jahr (~geschätzt). Die Wärmepumpe hängt an einem eigenen Zähler und steckt in diesen Zahlen nicht drin.

### Batterie
- Geladen aus PV (Jahr): 1.889 kWh, aus dem Netz nur 8,9 kWh → lädt praktisch ausschließlich aus PV ✅
- Entladen (Jahr): 1.787 kWh
- Ladezyklen: 272 (Stand 10.06.2026, seitdem nicht neu abgefragt)

---

## Analyse & Erkenntnisse

### ✅ Was gut läuft
- **Der Ertrag stimmt:** 12.050 kWh in achteinhalb Monaten sind 956 kWh pro kWp, hochgerechnet gut 1.080 kWh/kWp im Jahr. Für 22° nach Süden ist das am oberen Ende.
- Vom Netz kommen nur 755 kWh im Jahr (Haushalt), das ist sehr wenig.
- Im Sommer nahezu 100 % autark.
- Batterie fast ausschließlich aus PV geladen.
- 16,6 Tonnen CO2 gespart seit Inbetriebnahme.

### ⚠️ Schwachstelle: Winter
- Jahresautarkie 77 % → im Winter deutlich niedriger.
- Die PV füllt den Speicher von November bis Februar nicht täglich, entsprechend mehr Netzbezug.

### 📤 Einspeisung: der große Hebel
Rund 70 % des erzeugten Stroms gehen ins Netz (Eigenverbrauchsquote nur 29 %). Vergütet mit 7,72 ct/kWh, während der Zukauf über 30 ct kostet. Jede selbst verbrauchte Kilowattstunde ist also etwa viermal so viel wert wie eine eingespeiste.

---

## SG-Ready Integration (Wärmepumpe + Kostal)

### Status
- ❌ **ISG Connect TEC noch nicht installiert** (Nachfolger des ISG plus)
- ✅ Kostal Plenticore hat `DigitalOut` – bereit für SG-Ready Signal
- ✅ THZ 504 hat direkte SG-Ready Klemmen auf der Leiterplatte

### Option 1: ISG Connect TEC nachrüsten
- **Artikel:** ISG Connect TEC (191016) – Nachfolger des ISG plus (190382, nicht mehr lieferbar)
- **Preis neu:** ~799 € (UVP) → [tecalor.de](https://www.tecalor.de/de/produkte/regelung_energiemanagement/kommunikation/isg-connect-tec/isg-connect-tec.html)
- **Preis gebraucht/OVP:** 410–550 € → [Kleinanzeigen](https://www.kleinanzeigen.de/s-isg-connect/k0) | [eBay](https://www.ebay.de/b/Tecalor/bn_7005760371)
- **Vorteile:** App-Steuerung, Fernzugriff, volle SG-Ready Integration
- **Einbau:** Heizungsfachmann ~1 Stunde

### Option 2: Direkte SG-Ready Verkabelung (empfohlen)
- 2-adriges Steuerkabel: Kostal `DigitalOut` → SG-Ready Klemmen THZ 504
- **Kosten:** ~50–100 € (nur Elektriker/Heizungsmonteur)
- **Einschränkung:** Nur Ein/Aus-Signal, keine App/Fernzugriff
- **Wirkung:** Gleiche SG-Ready Funktion wie mit ISG Connect

Der Hebel ist hier größer als früher gedacht: Die Wärmepumpe kostet mit 60 € Abschlag im Monat mehr als der gesamte Haushaltsstrom. Läuft sie bei PV-Überschuss, wandert genau der Strom dorthin, der sonst für 7,72 ct ins Netz geht.

### Nächster Schritt
- [ ] Heizungsmonteur fragen ob SG-Ready Klemmen an THZ 504 zugänglich sind → Option 2 prüfen

## Optimierungspotenzial

### 🚗 BMW iX1 – der größte Hebel

Das Auto braucht **2.175 kWh/Jahr** (14,5 kWh × 15.000 km).
Die Anlage **speist aktuell rund 9.000 kWh/Jahr ein**.

→ **Das Auto kann vollständig aus dem PV-Überschuss geladen werden.** Danach gehen immer noch rund 6.800 kWh ins Netz.

**Was das konkret bedeutet** (alle Werte ~geschätzt):

| | Ohne EV | Mit BMW iX1 |
|---|---|---|
| Einspeisung/Jahr | ~9.000 kWh | ~6.800 kWh |
| EV-Ladung aus PV | – | ~2.175 kWh |
| Eigenverbrauchsquote | 29 % | ~45 % |
| Wert der Verschiebung | – | ~570 €/Jahr |

Die 570 € ergeben sich aus der Differenz: 2.175 kWh, die nicht für 7,72 ct eingespeist, sondern statt Netzstrom für gut 30 ct genutzt werden.

**Im Sommer:** EV lädt vollständig aus PV-Überschuss → 0 € Ladekosten
**Im Winter:** EV lädt teils aus Speicher (Tagesrest), teils Netz → günstig

### ⏰ Smart Charging – wann laden?
- **Idealer Ladezeitpunkt:** 10–15 Uhr (PV-Spitze)
- **Zweitbeste Option:** Abends aus Speicher (Batteriestand nach Sonnenuntergang nutzen)
- **Vermeiden:** Nachts direkt aus Netz laden (höchste Kosten)

Die Kostal-API kann jederzeit prüfen ob genug PV-Überschuss da ist → Ladefreigabe nur bei Überschuss.

### 🏠 Weitere Optimierungen
- **Waschmaschine/Spülmaschine:** 10–15 Uhr laufen lassen (PV-Peak)
- **Warmwasser:** Boiler tagsüber aufheizen falls vorhanden
- **Winter-Autarkie verbessern:** Tagsüber Haushaltsgeräte konzentrieren wenn PV produziert

### 💰 Finanzielles Optimierungspotenzial
| Maßnahme | Ersparnis/Jahr (~geschätzt) |
|---|---|
| EV aus PV-Überschuss laden | ~570 € |
| Wärmepumpe per SG-Ready auf PV-Überschuss legen | ~150–300 € |
| Lastverschiebung Haushaltsgeräte | ~50–100 € |
| **Gesamt** | **~770–970 €/Jahr** |

---

## Offene Punkte
- [x] Zähler 1ISK0092257936 abgelesen am 17.09.2026: 1.8.0 = 2.519 kWh, 2.8.0 = 17.100 kWh
- [ ] Im Frühjahr 2027 erneut ablesen, dann lässt sich die Heizsaison sauber vom Warmwasser trennen
- [ ] Mitte Oktober 2026: Jahresabrechnung Wärmepumpe (Vertrag 701055470353) prüfen. Kommt sie nicht, bei EnBW nachhaken – der Zählerstand wurde im März 2026 abgefragt, die Daten liegen dort also vor
- [ ] Bei Syna den Abschlag von 39 € wieder auf 60 € anheben lassen – er deckt die tatsächliche Einspeisung nicht
- [ ] Die Syna-Jahresabrechnung vom Mai 2026 raussuchen (kommt per Post) und die abgerechnete kWh-Menge gegen die Wechselrichter-Daten halten
- [ ] Prüfen, ob ein intelligentes Messsystem eingebaut ist (relevant für 60-Prozent-Regel und Solarspitzengesetz)
- [ ] Abschlag für die Wärmepumpe anpassen, bevor sich eine große Nachzahlung ansammelt

## Verknüpfungen
- [[02 Projekte/E-Fahrzeug Leasing finden]] – BMW iX1 Entscheidung
- [[02 Projekte/E-Auto Förderung]] – BAFA-Antrag nach Zulassung
- [[02 Projekte/ISG Connect TEC nachrüsten]] – SG-Ready Nachrüstung
- [[04 Ressourcen/E-Mobilität/Wallbox Kaufentscheidung]] – Wallbox für PV-Überschussladen
