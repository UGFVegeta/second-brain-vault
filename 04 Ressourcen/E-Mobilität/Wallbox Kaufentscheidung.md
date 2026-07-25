---
tags: [ressource, e-mobilität, wallbox, pv]
status: aktiv
date: 2026-07-15
---

# Wallbox Kaufentscheidung – Garage

Recherche zur Ladebox für die Garage (E-Fahrzeug), abgestimmt auf die eigene PV-Anlage (13 kWp + 13 kWh Kostal).

## Entscheidung (16.07.2026): Kostal ENECTOR AC 11 kW

Gewählt wegen nativer Kompatibilität mit der bestehenden Kostal-Anlage (KSEM verbaut, siehe unten): plug & play, ein System, eine App (Kostal Solar App), kein Zwischengerät (evcc) nötig.

**Beim Kauf beachten:**
- **Solar-Freischaltung (~280 €) mitbestellen** – Überschussladen ist beim ENECTOR eine kostenpflichtige Zusatzfunktion (Solar Pure/Plus). Ohne sie lädt die Box, aber nicht solargeführt. Beim Händler nach Bundle fragen.
- **Keine automatische Phasenumschaltung** → Überschussladen erst ab ~4 kW. Bei 13 kWp im Sommer irrelevant, in Übergangszeit/Winter teils etwas Netzstrom mit dabei.
- Preis Gerät ab ~595 € (Geizhals-Tiefstpreis, inkl. 7,5 m Typ-2-Kabel), Fachhändler ~650–750 €. Mit Solar-Code realistisch **~875–1.000 €**. Vor Bestellung Generation (G2?) und Lieferbarkeit prüfen.

## Ausgangslage

- **Starkstromkabel liegt bereits** bis zur Garage → günstigste Installationsvariante, kein aufwändiges Verlegen nötig.
- **Kostal Smart Energy Meter (KSEM) ist verbaut** – bestätigt über die Live-Daten der Anlage am 15.07.2026: Hausverbrauch wird sauber in PV / Batterie / Netz aufgeschlüsselt, Netzbezug/-Einspeisung wird gemessen. Das geht nur mit Zähler am Netzübergang. → **ENECTOR-Weg steht offen.**
- Zu prüfen vor Ort: Querschnitt & Länge des liegenden Kabels (mind. 5×2,5 mm², bei langer Strecke 5×4 mm²) und passende Absicherung im Zählerschrank (16-A-Automat + FI; bei Box mit integriertem DC-Fehlerstromschutz reicht FI Typ A).

## Kosten (realistisch, da Kabel schon liegt)

| Posten | Betrag |
|---|---|
| Wallbox (je nach Modell) | ~550–1.200 € |
| Montage + Anschluss | ~250–500 € |
| **Gesamt** | **~800–1.700 €** |

Anmeldung 11 kW beim Netzbetreiber: kostenlos, reine Meldung. 22 kW bräuchte Genehmigung – für zuhause nicht nötig, 11 kW reichen.

## Förderung 2026 – Fazit: keine

- **KfW:** seit 2024 keine Förderung für private Wallboxen mehr.
- **Charge@BW** (Land BW): wegen Überlastung Feb 2026 gestoppt, zum 06.05.2026 ganz eingestellt.
- Land & Bund fördern 2026 **nur noch Mehrparteienhäuser / WEG** (bis 2.500 €/Ladepunkt, nur E-Installation, nicht die Box) – für ein Einfamilienhaus nicht relevant.
- **KfW 442** („Solarstrom für Elektroautos"): **endgültig eingestellt.** Lief nur einen Tag im Sept. 2023 (300 Mio. € am selben Tag weg), Einstellung im Feb. 2024 vom Bundesverkehrsministerium bestätigt, keine neue Runde. Viele Shop-/Ratgeber-Texte behaupten weiter „förderfähig über KfW 442" – **veralteter Alttext.** Hätte für uns ohnehin nicht gegriffen (förderte nur Neuanschaffung PV+Speicher+Wallbox zusammen, nicht Nachrüstung).
- **KfW 270**: nur zinsgünstiger *Kredit*, kein Zuschuss – für ~1.000 € Wallbox nicht sinnvoll.
- Einzige Restchance: **kommunale Programme / Stadtwerke** – lohnt eine kurze Nachfrage beim lokalen Versorger.

## Modellvergleich (PV-überschussfähig, Kostal-kompatibel)

| Modell | Preis Gerät | Überschussladen mit Kostal | Auto-Phasenumschaltung | Bemerkung |
|---|---|---|---|---|
| **Kostal ENECTOR AC 11 kW** | ~760–900 € + ~280 € Solar-Freischaltcode | nativ, plug & play (KSEM vorhanden) | ❌ (Überschuss erst ab ~4 kW) | Alles im Kostal-Ökosystem, minimaler Aufwand |
| **go-e Charger Gemini 11 kW** | ab ~550 € | über evcc/Home Assistant als Vermittler | ❌ (nur Gemini Flex teils) | Günstig, flexibel, mobil; mehr Setup |
| **Fronius Wattpilot Home 11 J** | ~770–940 € | ja, mit eigenem Smart Meter | ✅ ab ~1,4 kW | ADAC-Testsieger PV-Laden |
| **openWB Series2** | ab ~1.100 € | sehr gute Kostal-Anbindung | ✅ | Poweruser-/Bastler-Lösung |

Preise Stand Juli 2026, online recherchiert – vor Kauf beim Elektriker gegenprüfen.

## Empfehlung

- **„Anklemmen und läuft"** und Aufpreis ok → **ENECTOR** (KSEM ist schon da, kein Zusatzgerät nötig). Gesamt Gerät ~1.050–1.200 €.
- **Sparen + gern selbst tüfteln** → **go-e** (ab ~550 €) mit **evcc** (kostenlose Open-Source-Software auf kleinem Rechner/Raspberry Pi) als Überschuss-Steuerung. Technisch top, minimal mehr Einrichtung.
- **Maximales Überschussladen auch in Übergangszeit/Winter** (automatische 1-/3-Phasen-Umschaltung) → **Fronius Wattpilot**.

Offene Ehrlichkeits-Fußnote: Ob go-e in aktueller Firmware *ohne* evcc direkt mit Kostal überschussladen kann, ist unklar – bewährter Weg ist über evcc. Vor Kauf gegenchecken (Elektriker / Photovoltaikforum).

## Was ist PV-Überschussladen? (kurz erklärt)

Reihenfolge der Stromverteilung tagsüber: **1. Hausverbrauch → 2. Batterie laden → 3. Rest = Überschuss** (würde sonst für ~8 ct/kWh ins Netz eingespeist). Die Wallbox greift genau diesen Überschuss ab und tankt ihn ins Auto, statt ihn billig zu verkaufen und später teuren Netzstrom (~30 ct) zu laden → großer Spar-Hebel.

Die Box **regelt dynamisch mit**: misst laufend den aktuellen Überschuss und passt die Ladeleistung live an (Backofen an → drosseln; volle Sonne → mehr).

**Phasen-Thema:** 3-phasiges Laden startet erst ab ~4,1 kW. Bei wenig Überschuss (trüb/abends) laden nur Boxen mit **automatischer Phasenumschaltung** (Fronius, openWB) weiter (ab ~1,4 kW, 1-phasig). ENECTOR & go-e können das nicht → brauchen die ~4-kW-Schwelle. Bei 13 kWp im Sommer irrelevant, in der Übergangszeit lädt man dann teils etwas Netzstrom mit.

**Batterie-Priorisierung:** einstellbar, ob erst Hausspeicher voll oder erst Auto lädt. ENECTOR regelt das im Kostal-Verbund, beim go-e übernimmt das evcc.

## Bestell-Details

- **Richtiges Modell: Kostal ENECTOR AC 3.7/11 kW, Art.-Nr. 10532947**, inkl. 7,5 m Typ-2-Kabel. („3.7" = 1-phasige Alternative, „11" = 3-phasig – genau das, was wir brauchen.)
- **Nicht die MID-Variante** (geeichter Zähler) – nur nötig, wenn Ladevorgänge abgerechnet werden (z. B. Dienstwagen-Erstattung). Für privates Laden unnötiger Aufpreis.
- **Generation klären:** Es gibt eine G2-Version. Beim Händler nachfragen, welche Generation geliefert wird – Unterschiede G1/G2 nicht abschließend geklärt. Zeitlich ist Luft (iX1 erst Okt/Nov).
- **Solar-Freischaltung (~280 €) mitbestellen** – ggf. Bundle-Angebot beim Fachhändler prüfen (kann günstiger sein als Tiefstpreis + Code separat).

**Angebote (Geizhals, Stand 16.07.2026):** ab ~645 € (günstigstes Listing, Versand extra) | ~663 € solarhandel24 (Vorbestellung, Lieferung ab Ende Juli; **12,90 € Skonto bei Vorkasse** → effektiv ~656 € inkl. Versand) | ~748–749 € (u. a. via eBay, Gratisversand). → [Geizhals-Preisvergleich](https://geizhals.de/kostal-enector-ac-3-7-11kw-10532947-a2828380.html), dort auch Preisalarm setzbar.

**Rabattcodes:** Die kursierenden Coupon-Codes (SKONTO-3, FRÜHLING5 etc.) sind **nicht verifiziert** – Coupon-Portale recyceln abgelaufene Codes. Realer Rabatt = **~2 % Skonto bei Vorkasse** (offizielle Shop-Mechanik). Newsletter-Anmeldung als seriöser Weg zu evtl. echtem Code.

## §14a EnWG – Netzentgelt-Rabatt über Syna (echter Spar-Hebel!)

Netzbetreiber: **Syna** (Rudersberg, 73635). Versorger: EnBW.

- **ENECTOR ist §14a-konform**: hat serienmäßig einen **„Downgrade-Eingang"** für Steuerbox/Rundsteuerempfänger → Steuerbarkeits-Anforderung erfüllt.
- **Funktionsweise:** Syna-Steuerbox hängt am Downgrade-Eingang. In seltenen Netz-Engpässen drosselt die Box kurz auf min. 4,2 kW, danach automatisch wieder volle Leistung. Praktisch kaum spürbar, v. a. beim Laden mit PV-Überschuss.
- **Ersparnis: ~110–190 €/Jahr** (Modul 1, Pauschale), über 10 Jahre bis ~1.900 €. Exakter Betrag hängt vom Syna-Netzgebiet ab → bei Syna/Elektriker erfragen.

| Modul | Vorteil | Voraussetzung |
|---|---|---|
| **Modul 1 (empfohlen)** | Pauschale ~110–190 €/Jahr | kein Extra-Zähler nötig |
| Modul 2 | Netz-Arbeitspreis auf 40 %, kein Netz-Grundpreis | eigener Zählpunkt |
| Modul 3 | zeitvariables Netzentgelt | intelligentes Messsystem |

**→ Empfehlung: Modul 1** (einfachste Variante, kein zweiter Zähler). **Elektriker meldet die Wallbox bei Inbetriebnahme nach §14a bei Syna an und wählt Modul 1.**

Faktisch die einzige verbliebene „Förderung" für ein Einfamilienhaus. Kommunale Förderung Rudersberg: nichts Konkretes auffindbar → ggf. Rathaus/Mitteilungsblatt prüfen. EnBW-Kundenbonus: nicht bestätigt, ggf. im Kundenkonto schauen.

## Fahrzeug: BMW iX1 (ab Okt/Nov 2026)

- iX1 lädt **serienmäßig 11 kW AC über Typ 2** → passt exakt zum ENECTOR (fest angebautes Typ-2-Kabel, 11 kW). **Kein Adapter, kein Zwischenstück nötig** – Kabel direkt einstecken, volle 11 kW nutzbar.
- **Kein 22-kW-AC-Upgrade nötig** (BMW-Option ~600 €): bringt nur an öffentlichen 22-kW-Säulen etwas, zuhause null Vorteil, da Wallbox/Hausanschluss ohnehin 11 kW. → sparen.
- BMW legt meist einen Mode-2-Ladeziegel (Haushalts-/CEE-Steckdose) bei – zuhause nicht nötig, nur Notladen unterwegs.

## Checkliste fürs Elektriker-Gespräch

**Gerät:** Kostal ENECTOR AC 3.7/11 kW, fest angeschlossenes 7,5 m Typ-2-Kabel, Wandmontage (260×400×160 mm, 3,9 kg, IP54). 11 kW, 3-phasig, 400 V, 16 A/Phase.

**Elektrischer Anschluss:**
- Vorhandenes Starkstromkabel prüfen: Querschnitt & Länge. Mind. 5×2,5 mm², bei langer Strecke 5×4 mm². Reicht der Querschnitt?
- Eigener Stromkreis mit 3-poligem LS-Schalter C16A.
- FI: ENECTOR hat integrierte DC-Fehlerstromerkennung (6 mA DC) → vorgelagert reicht FI Typ A, kein teurer Typ B nötig (bestätigen lassen).
- Platz im Zählerschrank für zusätzlichen LS (+ ggf. FI) prüfen.

**PV-Überschuss / KSEM (ENECTOR-spezifisch, wichtig!):**
- ENECTOR muss mit dem Kostal Smart Energy Meter kommunizieren, üblich über Modbus RTU (RS485).
- Datenverbindung KSEM ↔ ENECTOR herstellen; KSEM muss eingebunden & erreichbar sein. Kostal-Installationsanleitung nutzen.
- Solar-Funktion danach über Kostal Solar Webshop / App freischalten.
- Genaue Anbindung (RS485 vs. Netzwerk) und KSEM-Generation (G1/G2) in der Kostal-Anleitung prüfen – aktiv ansprechen, sonst lädt die Box nicht solargeführt.

**Netzbetreiber (Syna):**
- 11 kW nur anmeldepflichtig (kostenlos), nicht genehmigungspflichtig. Anmeldung macht i. d. R. der Elektriker.
- **§14a-Anmeldung bei Syna, Modul 1** mit anmelden → ~110–190 €/Jahr Netzentgelt-Rabatt. Steuerbox an den Downgrade-Eingang des ENECTOR anschließen.

**Vor Ort:** Montageort + Höhe, Kabelweg bis zum Stellplatz.
