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

Die tatsächlich ausgezahlten Beträge stehen auf der Gutschrift von Syna. **Offen:** Im web.de-Postfach liegt seit der Inbetriebnahme keine einzige Einspeisegutschrift. Prüfen, ob sie per Post kommt oder an eine andere Adresse geht.

---

## Stromverträge

| | Haushalt | Wärmepumpe |
|---|---|---|
| Vertragsnummer | 701055910928 | 701055470353 |
| Tarif | EnBW Planbar und Sicher Privatstrom (seit 20.05.2025) | EnBW Grün und Sicher Privatstrom |
| Abschlag | 44 €/Monat (seit 17.04.2026) | 60 €/Monat |
| Preise | – | 38,57 ct/kWh brutto, 18,30 €/Monat Grundpreis |
| Letzte Abrechnung | 17.03.2026 für 17.03.2025 bis 16.03.2026 | noch keine |

**Jahresrechnung Haushalt (17.03.2025 bis 16.03.2026):** 755 kWh Netzbezug, 522,14 € Stromkosten, 760 € Abschläge gezahlt, 9,38 € Messkosten erstattet → **247,24 € Guthaben**.

⚠️ **Offen: Die Wärmepumpe wurde noch nie abgerechnet.** Seit Mai 2025 laufen 60 € im Monat. Bei dem Jahresverbrauch von 2.400 kWh, der in der Willenserklärung steht, kämen rechnerisch rund 1.145 € im Jahr zusammen (~geschätzt). Der Abschlag liegt damit etwa 425 € zu niedrig, eine Nachzahlung ist wahrscheinlich. Bei EnBW nachfragen, wo die Jahresabrechnung bleibt.

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
- [ ] Bei EnBW nachfragen, warum es für die Wärmepumpe (Vertrag 701055470353) noch keine Jahresabrechnung gibt
- [ ] Klären, ob und wie Syna die Einspeisung vergütet – es liegt keine Gutschrift vor
- [ ] Prüfen, ob ein intelligentes Messsystem eingebaut ist (relevant für 60-Prozent-Regel und Solarspitzengesetz)
- [ ] Abschlag für die Wärmepumpe anpassen, bevor sich eine große Nachzahlung ansammelt

## Verknüpfungen
- [[02 Projekte/E-Fahrzeug Leasing finden]] – BMW iX1 Entscheidung
- [[02 Projekte/E-Auto Förderung]] – BAFA-Antrag nach Zulassung
- [[02 Projekte/ISG Connect TEC nachrüsten]] – SG-Ready Nachrüstung
- [[04 Ressourcen/E-Mobilität/Wallbox Kaufentscheidung]] – Wallbox für PV-Überschussladen
