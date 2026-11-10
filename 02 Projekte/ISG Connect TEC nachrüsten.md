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

## Stand 10.11.2026

Oskar will die Kopplung jetzt umsetzen. Ziel ist, dass Claude sich mit der Wärmepumpe verbinden und die Einstellungen (Heizkurve, Temperaturen, PV-Überschuss) selbst optimieren kann. Dafür reicht das reine SG-Ready-Kabel vom Kostal DigitalOut nicht, weil es nur ein Ein/Aus-Signal ist und keinen Zugriff auf die Anlage gibt. Es braucht also das ISG Connect TEC. Am 11.11.2026 kommt der Tecalor-Techniker zur Wartung. Oskar ist nicht da, die Fragen stellt der Schwiegervater anhand des Fragenzettels und notiert die Antworten: [[Fragen Tecalor-Techniker 2026-11-11.pdf]].

Am 10.11. fragt Oskar zusätzlich den Elektriker, der die Wallbox eingebaut hat (freier Digitalausgang am Plenticore, Koppelrelais, Kabelweg, Kosten).

### Recherche 10.11.2026

- **SG Ready geht nur mit ISG.** Tecalor schreibt auf der Produktseite, dass das ISG Connect TEC für die SG-Ready-Funktionen notwendiges Zubehör ist. Die frühere Annahme, die THZ 504 habe eigene SG-Ready-Klemmen und der Kostal DigitalOut könne direkt daran, ist damit vom Tisch.
- **Zugriff im Heimnetz:** Das ISG Connect TEC hängt per LAN im Heimnetz (WLAN nennt Tecalor nicht), hat eine Weboberfläche im Browser und eine Modbus-TCP-Schnittstelle. Die Cloud und die tecalor Home App sind nur zusätzlich, nicht Pflicht.
- **Kompatibilität:** In der Stiebel-Eltron-Kompatibilitätsliste für ISG Connect, ISG Web und ISG Plus (Stand 01.05.2025) hat die LWZ 504 bei Modbus TCP und KNX IP einen Haken. Die THZ 504 ist das baugleiche Tecalor-Gerät. Die Liste setzt die aktuelle ISG-Firmware voraus, beim Regler kann ein Update nötig sein.
- **Steuern statt nur lesen:** Es gibt Software, die über Modbus TCP lokal Sollwerte, Betriebsart und SG Ready setzt (Home-Assistant-Integration pail23/stiebel_eltron_isg_component für LWZ x04, evcc-Vorlage „Tecalor THZ (SG Ready)“). Was genau beschreibbar ist, hängt am Regler und an der Firmware. Das zeigt sich erst am eingebauten Gerät.
- Folge: Ein LAN-Kabel muss an die Wärmepumpe. Das ist die wichtigste Frage an den Elektriker.

### Preise und Einbau (10.11.2026)

- **Neu im Handel:** billiger.de listet das Stiebel ISG Connect ab 546 €. Die 799 € UVP stammen aus dem Juni und sind nicht neu geprüft.
- **Stiebel statt Tecalor geht:** Das Stiebel ISG Connect (206780) gilt als baugleich mit dem Tecalor ISG Connect TEC (191016). Ein Nutzer im KNX-Forum betreibt es an einer THZ, und der einzige Unterschied sind die Stiebel-Bilder in der Weboberfläche. Eine offizielle Bestätigung von Tecalor gibt es nicht.
- **Kleinanzeigen, Stand 10.11.2026**, alle neu oder originalverpackt:
  - Lorch, Stiebel 206780, neu und ungeöffnet: 440 € VB (01.11.)
  - Urbach, Tecalor/Stiebel, neu: 499 € VB (11.10.)
  - Hüfingen, Tecalor ISG Connect TEC, neu: 480 € VB
  - Linden (Hessen), Stiebel 206780, neu: 415 €, nur mit Versand
- **Einbau:** Laut Installationsanleitung richtet sie sich an Fachkräfte, Elektriker eingeschlossen. Das ISG kommt als letztes Gerät auf den CAN-Bus der Wärmepumpe, und dazu braucht es ein LAN-Kabel. Ein nötiges Update der Reglersoftware kann nur der Kundendienst machen.

Favorit ist das Angebot in Lorch (440 € VB). Den Einbau soll der Elektriker machen, der die Wallbox eingebaut hat, falls er zusagt. Für ihn liegt die deutsche Installationsanleitung bereit: [[ISG Connect Installationsanleitung (deutsch).pdf]], Kapitel 6 (Montage) und 7 (Inbetriebnahme). Dazu ein Infoblatt auf einer Seite mit QR-Code zur Anleitung: [[ISG Connect Infoblatt Elektriker.pdf]].

Quellen: tecalor.de, Produktseite ISG Connect TEC; Kompatibilitätsliste ISG (Stiebel Eltron, Stand 01.05.2025); github.com/pail23/stiebel_eltron_isg_component; docs.evcc.io/de/heating/tecalor-thz-sg-ready.

Displaywerte 10.11.2026, 14:09 Uhr: außen 10,3 °C, Druck Heizkreis 1,1 bar, Warmwasser 47,4 °C, Automatik. Laut Anleitung der Schwesterbaureihe LWZ 304/404 meldet die Anlage unter 0,5 bar Fehler 37. Der Vordruck des Ausdehnungsgefäßes liegt bei 0,75 bar, das Sicherheitsventil öffnet bei 3 bar. 1,1 bar ist also kein Notfall, liegt aber am unteren Rand. Ob und auf welchen Wert aufgefüllt wird, klärt der Techniker. Die Frage steht als Zusatz auf dem Zettel.

Antworten des Technikers: _noch offen_

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
