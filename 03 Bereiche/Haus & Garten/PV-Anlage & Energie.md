---
tags: [bereich, energie, pv, solar]
status: aktiv
---

# PV-Anlage & Energie

## Anlage
- **Wechselrichter:** Kostal Plenticore (IP: 192.168.178.48)
- **Leistung:** 13 kWp, Südausrichtung
- **Speicher:** 13 kWh
- **PV-Strings:** 2 (je ~6,5 kWp)
- **Live-Daten:** `python3 .scripts/kostal_live.py`

---

## Jahresdaten (Stand 10.06.2026)

| Kennzahl | Heute | Monat | Jahr | Gesamt |
|---|---|---|---|---|
| **PV-Produktion** | 30,6 kWh | 517,4 kWh | 6.314 kWh | 18.003 kWh |
| **Autarkie** | 99,5 % | 99,65 % | 68,48 % | 74,06 % |
| **Eigenverbrauch** | 42,66 % | 23,29 % | 36,43 % | 28,59 % |
| **CO2 gespart** | – | – | 4,42 t | 12,60 t |

### Hausverbrauch Jahr (3.359 kWh)
| Quelle | kWh | Anteil |
|---|---|---|
| PV direkt | 1.152 kWh | 34,3 % |
| Batterie | 1.149 kWh | 34,2 % |
| Netz | 1.059 kWh | 31,5 % |

### Batterie
- Ladestand aktuell: 96 %
- Ladezyklen: 272 (ca. 1–1,5 Jahre alt)
- Geladen aus PV (Jahr): 1.329 kWh
- Entladen (Jahr): 1.239 kWh
- Netz zum Laden: nur 8,9 kWh/Jahr → Batterie wird fast ausschließlich aus PV geladen ✅

---

## Analyse & Erkenntnisse

### ✅ Was gut läuft
- Im Sommer (Juni) nahezu **100% autark** – Anlage arbeitet perfekt
- Hausverbrauch gleichmäßig aus PV, Batterie und Netz gedeckt (je ~⅓)
- Batterie fast ausschließlich aus PV geladen (9 kWh Netzbezug zum Laden im ganzen Jahr)
- 12,6 Tonnen CO2 gespart seit Installation

### ⚠️ Schwachstelle: Winter
- Jahresdurchschnitt Autarkie: 68 % → im Winter wahrscheinlich 30–40 %
- PV produziert im Winter zu wenig um den Speicher täglich zu füllen
- Ergebnis: mehr Netzbezug November–Februar

### 📤 Einspeisung
- Eigenverbrauchsquote Jahr: 36 % → **64 % der PV-Produktion gehen ins Netz**
- Ca. 4.000 kWh/Jahr Einspeisung (= Strom der aktuell "verschenkt" wird)
- Mit Einspeisevergütung vergütet, aber deutlich unter Eigenverbrauchswert

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

### Nächster Schritt
- [ ] Heizungsmonteur fragen ob SG-Ready Klemmen an THZ 504 zugänglich sind → Option 2 prüfen

## Optimierungspotenzial

### 🚗 BMW iX1 – der größte Hebel

Das Auto braucht **2.175 kWh/Jahr** (14,5 kWh × 15.000 km).
Die Anlage **exportiert aktuell ~4.000 kWh/Jahr**.

→ **Das Auto könnte vollständig aus dem PV-Überschuss geladen werden** – ohne dass weniger ins Netz geht als nötig.

**Was das konkret bedeutet:**

| | Ohne EV | Mit BMW iX1 |
|---|---|---|
| Einspeisung/Jahr | ~4.000 kWh | ~1.825 kWh |
| EV-Ladung aus PV | – | ~2.175 kWh (gratis) |
| Eigenverbrauchsquote | 36 % | ~52 % |
| Effektive Stromkosten EV | – | ~0 €/Jahr |

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
| Maßnahme | Ersparnis/Jahr |
|---|---|
| EV aus PV-Überschuss laden | ~200–400 € |
| Lastverschiebung Haushaltsgeräte | ~50–100 € |
| **Gesamt** | **~250–500 €/Jahr** |

---

## Verknüpfungen
- [[02 Projekte/E-Fahrzeug Leasing finden]] – BMW iX1 Entscheidung
- [[02 Projekte/E-Auto Förderung]] – BAFA-Antrag nach Zulassung
