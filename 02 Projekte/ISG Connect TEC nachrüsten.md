---
tags: [projekt, energie, smart-home, wärmepumpe]
status: aktiv
erstellt: 2026-06-10
deadline: 2026-09-30
---

# ISG Connect TEC nachrüsten

## Ziel
ISG Connect TEC (191016) kaufen und an der Tecalor THZ 504 installieren lassen – bis **Herbst 2026** – um die Wärmepumpe smart mit der PV-Anlage zu verknüpfen und die Winter-Autarkie signifikant zu verbessern.

## Warum
- Wärmepumpe läuft aktuell ungekoppelt von der PV-Anlage
- Mit ISG Connect: Claude kann Kostal + Wärmepumpe zusammen steuern
- Ziel: PV-Anteil Wärmepumpe von ~35% auf ~70–80% steigern
- Winter-Autarkie: ~35% → ~60–70%
- Einsparung Stromkosten WP: ~200–350 €/Jahr
- Amortisation: 2–3 Jahre

## Gerät
- **Artikel:** ISG Connect TEC – Artikelnummer **191016** (Tecalor/Stiebel Eltron)
- Nachfolger des ISG plus (190382, nicht mehr lieferbar)
- Verbindet THZ 504 über LAN mit dem Heimnetz
- Aktiviert SG-Ready Funktion + Fernzugriff + API

## Kaufoptionen
- [Tecalor offiziell](https://www.tecalor.de/de/produkte/regelung_energiemanagement/kommunikation/isg-connect-tec/isg-connect-tec.html) – **799 €** (UVP)
- [Kleinanzeigen](https://www.kleinanzeigen.de/s-isg-connect/k0) – **450–550 €** (neu/OVP) ← empfohlen
- [eBay](https://www.ebay.de/b/Tecalor/bn_7005760371) – **ab ~410 €**

## Nächste Schritte
- [ ] ISG Connect TEC kaufen (Kleinanzeigen/eBay, neu/OVP, ~450–550 €)
- [ ] Heizungsmonteur anfragen: Einbau ISG Connect TEC an THZ 504
- [ ] Einbautermin vor Heizperiode (September/Oktober 2026)
- [ ] Nach Einbau: IP-Adresse des ISG Connect im Netz ermitteln
- [ ] Claude-Anbindung einrichten (Kostal + ISG Connect API)
- [ ] Steuerlogik konfigurieren: PV-Überschuss → Wärmepumpe

## Technische Details
- **PV-Anlage:** Kostal Plenticore, IP 192.168.178.48, API bereits verbunden ✅
- **Wärmepumpe:** Tecalor THZ 504
- **Kostal DigitalOut:** verfügbar, noch nicht konfiguriert
- **Was Claude dann kann:**
  - PV-Überschuss → Warmwasser/Heizung aufheizen
  - COP-Optimierung (niedrige Vorlauftemperatur)
  - Tibber-Integration: bei Günstigstunden laden
  - Täglicher Energiebericht in Daily Note

## Verknüpfungen
- [[03 Bereiche/Haus & Garten/PV-Anlage & Energie]]
- [[02 Projekte/E-Fahrzeug Leasing finden]] – BMW iX1 ebenfalls in Gesamt-Energiekonzept
