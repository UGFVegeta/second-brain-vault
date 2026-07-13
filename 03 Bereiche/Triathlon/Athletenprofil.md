---
tags: [triathlon, coaching, athletenprofil]
status: aktiv
date: 2026-07-07
---

# Athletenprofil Triathlon – Oskar Klein

> [!info] Single Source of Truth für das Coaching
> Diese Notiz ist die Grundlage für alle Trainings- und Wettkampfempfehlungen. Werte werden hier gepflegt und mit intervals.icu (Athlete-ID `i635070`) abgeglichen. Datenzugriff siehe [[#Datenzugriff]].

## Athletentyp

**Ein Läufer, der Triathlon macht.** Herausragende Laufform (AK-Spitze Baden-Württemberg, auch unter Leichtathleten Top 5), moderates Rad, Schwimmen als Limiter – doppelt: Können *und* nur ~1 Einheit/Woche möglich. Renntaktik Kurzdistanz: im Schwimmen nicht abreißen lassen, auf dem Rad in Schlagdistanz bleiben, auf der Laufstrecke aufräumen.

## Leistungskennzahlen (Stand 07.07.2026)

| Größe | Wert |
|---|---|
| Gewicht | 77 kg |
| 🚴 Rad-FTP | 330 W (**4,29 W/kg**) |
| 🏃 Lauf-Schwelle | 3:25 min/km |
| 🏃 5 km / 10 km Bestzeit | 16:40 (3:20/km) / 34:20 (3:26/km) |
| 🏊 Schwimm-Schwelle (CSS) | 1:35 min/100 m |
| ❤️ Schwellen-HF / Max-HF | 161 / 178 |

## Wochenverfügbarkeit (Schulwochen)

- **Mo–Mi abends:** Rad, je 1–1,5 h
- **Mi mittags** (nach Schule, ~11:30): Lauf 1–1:20 h – meist **Bahnintervalle**
- **Do abends:** Schwimmen (die einzige verlässliche Schwimmzeit)
- **Wochenende:** wenn möglich 2× 1,5 h Rad
- **Grenzen:** max. 3 Laufeinheiten/Woche; Schwimmen sonst schwer unterzubringen
- **Zielumfang:** 9–12 h/Woche

## Stärken / Schwächen

- **Stärke:** Laufen (elitär) – gewinnt Rennen
- **Limiter:** Schwimmen (Können + Frequenz) – größter Hebel für Rennzeit
- **Baustelle mit gutem Zugang:** Radfahren (Volumen ist da → FTP heben)

## Coaching-Leitlinien

1. **Schwimmen – größter ROI:** zweite Reizsetzung anstreben; wenn kein Becken, dann **2×15 min Zugseil/Stretch-Cords** daheim (Wassergefühl + spezifische Kraft).
2. **Rad – strukturiert FTP heben:** 4–5 Radeinheiten pro Woche vorhanden; hier liegt der zeiteffiziente Fortschritt.
3. **Lauf – schützen, nicht überbauen:** 3 Läufe/Woche reichen; Mittwochs-Bahn ist der Schlüsselreiz; eine Einheit als **Koppellauf** ans Rad hängen (Renn-Spezifik).
4. **Belastung:** aktuell Wettkampfphase → Formerhalt/Schärfen, kein großer Aufbau.

## Wettkampfkalender 2026

> ⚠️ Restliche ❓-Angaben noch zu bestätigen.

| Datum | Wettkampf | Distanz | Prio | Notiz |
|---|---|---|---|---|
| **Sa 11.07.** | **Schluchsee-Triathlon** (BW-Liga) | Olympisch | **A** | Saisonziel. See/Schwarzwald, kühl → Neopren wahrscheinlich (Auftrieb hilft dir) |
| So 12./13.07. ❓ | Steinberger Waldlauf (Heimrennen) | 11,3 km **oder** HM 21,1 km | C | Tag nach dem A-Rennen; nicht so wichtig, aber Heimat; Titelverteidiger HM |
| Sa 18.07. | Welzheim-Triathlon (Heimrennen, bergig) | ❓ | B | bergig = Rad-Nachteil, Lauf-Vorteil |
| So 02.08. | BW-Meisterschaft Sprint, Ravensburg | Sprint | B | |

**Priorität:** A Schluchsee → B Ravensburg/Welzheim → C Waldlauf. Welzheim + Waldlauf sind Heimrennen (emotional nicht unwichtig).

**Offener Steuerungspunkt (Waldlauf):** Liegt jetzt *nach* dem A-Rennen – gefährdet also nicht Schluchsee, sondern **Welzheim (5 Tage später) und die Erholung Richtung Ravensburg**. Da C-Rennen und nach A-Rennen sowieso müde Beine: **11,3 km kontrolliert oder auslassen**, keinen All-out-HM. Trade-off, Oskars Entscheidung.

## Hauptkonkurrenz & Renntaktik (BW-Liga)

**Andreas Schröder** – einziger echter Gegner in der BW-Liga; der Rest ist bei normaler Leistung im Griff. **Saisonziel 2026: Sieg gegen Schröder** (die Wintermotivation).

Das Rennmodell in einer Zeile: **Schwimm-+Rad-Rückstand unter 1 Minute halten, dann niederlaufen.**

- 🏊 **Schwimmen:** Schröder normal schneller – **aber mit Neopren (Schluchsee immer erlaubt) gleichauf**; Oskar profitiert extrem vom Auftrieb (und steigt ausgeruhter aufs Rad). → **Auf Schröders Füße setzen, zusammen rauskommen.**
- 🚴 **Rad:** Leistung ähnlich, Schröder etwas leichter (Nachteil bergauf); Oskar technisch stärker + erfahrener (Vorteil bergab/technisch). → **Rückstand ≤ 1 min halten, bergauf nicht sprengen, bergab/technisch zurückholen.**
- 🏃 **Laufen:** Oskar ~1 min schneller auf 10 km. → **Rückstand ≤ 1 min nach dem Rad = Oskar gewinnt.**

**Rad-Modus:** **non-draft** (Windschatten verboten) → Eigenzeitfahren. Rad nach **Watt fahren, nicht nach Schröder**; legalen Abstand halten, sauber überholen.

## Datenzugriff

- Report/Form: `python3 .scripts/intervals_live.py`
- TP-Virtual-Rollen nachladen: `python3 .scripts/intervals_tpv_upload.py`
- Details siehe [[CLAUDE]] → Abschnitt „Trainingsdaten (intervals.icu)".

## Offene Punkte

- [ ] Wettkampf-Prioritäten (A/B/C) bestätigen – ist Ravensburg das A-Rennen?
- [ ] Ort/Datum des Samstag-Triathlons + Distanz Welzheim bestätigen
- [ ] Rad-Schwellen-HF ggf. separat (aktuell = Lauf-Wert 161)
