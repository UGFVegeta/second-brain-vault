---
tags: [triathlon, training, einheiten]
status: aktiv
date: 2026-09-07
---

# Trainingseinheiten im Detail

Ergänzt [[Trainingsplan]] um das, was dort nur als Stichwort steht. Der Plan sagt *wann*, diese Notiz sagt *was genau*.

## Radeinheiten als Dateien

Sechs `.zwo`-Dateien. Ziel ist **TrainingPeaks** (aktuell kein Zwift-Abo), gefahren wird über **TrainingPeaks Virtual** — dieselbe Infrastruktur, die schon `.scripts/intervals_tpv_upload.py` für die Rollenfahrten nutzt.

| Datei | Einheit | Arbeit | Dauer | Wann |
|---|---|---|---|---|
| 01 | FTP-Test 20 Minuten | – | 0:56 | Fr 18.09. |
| 02 | VO2max 3 × 7 × 40/20 | 21 min | 0:56 | Fr 25.09. |
| 03 | VO2max 3 × 8 × 40/20 | 24 min | 0:59 | Fr 02.10. |
| 04 | VO2max 3 × 9 × 40/20 | 27 min | 1:02 | Fr 09.10. |
| 05 | VO2max 3 × 10 × 40/20 | 30 min | 1:05 | Fr 16.10. |
| 06 | Grundlage 60 min | – | 1:00 | jeden Montagabend |

Die Dateien liegen im Vault unter `04 Ressourcen/Triathlon & Training/Workouts/`. Von dort per Drag & Drop auf den jeweiligen Tag im TrainingPeaks-Kalender ziehen, dann als geplantes Workout in TrainingPeaks Virtual öffnen. Laut TrainingPeaks Help Center werden `.zwo`-Dateien für die Workout Library und TP Virtual gleichermaßen unterstützt. ⚠️ Den genauen Klickpfad konnte ich nicht gegenprüfen, die Hilfeseiten blocken automatisierte Abrufe — bei Problemen nachfragen.

Zusätzlich liegen Kopien in `~/Documents/Zwift/Workouts/975277/` (unangetastet, falls das Zwift-Abo zurückkommt), das ist aber nicht mehr der vorgesehene Weg.

**Aufbau der VO2max-Einheiten:** 40 Sekunden bei 115 % FTP, 20 Sekunden locker, sieben bis zehn Mal am Stück, drei Blöcke mit fünf Minuten Pause dazwischen. **Die Watt bleiben über den ganzen Block gleich, gesteigert wird nur die Zahl der Wiederholungen.**

**Arbeitswert FTP: 300 W** (Stand 07.09.2026, aus der gemessenen Leistungskurve). Daraus die absoluten Zielwerte:

| Element | % FTP | bei 300 W |
|---|---|---|
| 40 s im Mikrointervall | 115 % | **345 W** |
| 20 s Pause darin | 50 % | 150 W |
| Öffner | 110 % | 330 W |
| FTP-Test, die 20 Minuten | 100 % | **300 W als Orientierung, real alles geben** |
| Grundlage Datei 06 | 63 % | 190 W |

**Alle Dateien arbeiten mit Prozent der FTP, nicht mit absoluten Watt.** Nach dem Test am 18.09. also nur den neuen FTP-Wert in der App eintragen, die Dateien bleiben unverändert.

**Warum VO2max und nicht Sweet Spot:** Mikrointervalle sammeln viel Zeit nahe der maximalen Sauerstoffaufnahme, ohne die Beine nennenswert zu belasten — auf dem Rad fehlt die bremsende Muskelarbeit, die beim Laufen den Muskelkater erzeugt. Für 3,2 und 6,4 km Cross ist genau das die passende Physiologie, und bei gedeckeltem Laufumfang ist es der günstigste Weg zu hoher Intensität.

## Laufintervalle

### Deine Laufleistungskurve

Beste Mittelwerte aus den 18 intensivsten Läufen der letzten zwölf Monate:

| Dauer | Watt | gemessen bei |
|---|---|---|
| 30 s | 747 | |
| 90 s | 714 | Schluchsee, 25 hm/km |
| 3 min | 664 | Schluchsee |
| 5 min | 602 | Schluchsee |
| 10 min | 541 | |
| 20 min | **508** | **Willstätt: 10,1 km flach in 35:39** |
| 30 min | 504 | |
| 60 min | 457 | passt zu NP 459 W beim Halbmarathon |

⚠️ **Die Werte von 60 s bis 5 min stammen alle aus Schluchsee und sind bergauf gemessen**, also durch die Hubarbeit erhöht. Für Bergvorgaben ist das genau richtig, für die Bahn nicht übertragbar.

Aus zwei alten 800er-Einheiten: 04.03.2026 im Schnitt **521 W** (491–541), 01.10.2025 im Schnitt **489 W** (462–527), jeweils bei Puls 138 bis 149.

### Vorgaben in Watt

Die Uhr zeigt Laufleistung live, und anders als der Puls reagiert sie sofort. **Am Berg ist sie die einzig brauchbare Steuergröße**, weil Pace dort nichts aussagt.

| Einheit | Zielleistung | Pace zur Kontrolle |
|---|---|---|
| **8 × 30 s Bergsprint** (KW 38) | 700+ W, nach Gefühl fast maximal | – |
| **6 × 90 s Berg** (KW 39) | **620–650 W** | – |
| **8 × 90 s Berg** (KW 40) | **610–640 W** | – |
| **10 × 90 s Berg** (KW 41) | **600–630 W** | – |
| **5 × 1000 m Bahn** (KW 42) | **530–550 W** | 3:25–3:30/km |
| **8 × 800 m Bahn** (KW 43) | **545–565 W** | 3:20–3:25/km |
| **12 × 400 m Bahn** (KW 44) | **590–620 W** | 3:05–3:12/km |
| **6 × 1000 m Bahn** (KW 45) | **525–545 W** | 3:25–3:30/km |
| **8 × 300 m schnell** (KW 47) | **620–650 W** | – |
| **5 × 200 m Renntempo** (KW 48) | **650–690 W** | – |

**Puls als Nebenkontrolle:** In den Intervallen 140 bis 150. Über 155 heißt zu hart angegangen, unter 135 heißt zu brav.

⚠️ **Zwei Vorbehalte.** Die Werte für kurze Belastungen auf der Bahn sind aus der Kurve extrapoliert, weil deine kurzen Bestwerte alle bergauf entstanden sind. Und der Anker Willstätt stammt vom 22.05., mit einer CTL deutlich über den jetzigen 46. Nach dem Infekt liegst du am Anfang wahrscheinlich zehn bis zwanzig Watt darunter. **Nicht auf die Zahl beißen** — die erste Bahneinheit am 14.10. gilt als Messung, danach ziehe ich die Vorgaben nach.

### Bergsprints (KW 38)
**8 × 30 s steil, Trabpause abwärts.** Nahezu maximal, volle Erholung zwischen den Wiederholungen. 2 km ein- und auslaufen.
Zweck ist nicht Ausdauer, sondern **neuromuskulär**: Nach Jahren ohne echtes Tempo müssen Sehnen und Ansteuerung wieder an schnelles Laufen gewöhnt werden. Am Berg passiert das mit geringerem Verletzungsrisiko als in der Ebene.

### Bergintervalle (KW 39–41)
**6 / 8 / 10 × 90 s am Anstieg, 2 min Trabpause abwärts.** Steigung 5 bis 8 Prozent. 2 bis 3 km ein- und auslaufen.
Nach Watt steuern, siehe Tabelle. Entscheidend ist die **Gleichmäßigkeit** — die letzte Wiederholung muss aussehen wie die erste. Wer die ersten drei zu schnell angeht, macht aus der Einheit einen Test.

### Bahnintervalle (KW 42–45)
Pausen: 2:30 nach den 1000ern, 2:00 nach den 800ern, 1:30 nach den 400ern. Je 2 bis 3 km ein- und auslaufen.

### Geländeeinheiten (ab KW 43, samstags)
**8 bis 10 km auf weichem Boden**, davon 6 × 2 min zügig im Wechsel mit 2 min locker. Kurven und kurze Anstiege bewusst mitnehmen statt umgehen — auf einem 1,07-km-Rundkurs sind genau die der Unterschied.
Ab KW 44 mit **Spikes**, damit sie am Renntag nicht neu sind.

## Schwimmen

### Vereinseinheit, donnerstags 20:00 (3000–3500 m, 90 min)
- **600 m einschwimmen:** 300 Kraul locker, 200 Lagenwechsel, 100 Beine
- **800 m Technik:** 8 × 100 m mit je einem Fokus — Wasserlage, Körperspannung, hoher Ellbogen, langer Zug
- **1400–1800 m Hauptteil:** 16 × 50 m mit 15 s Pause, oder 12 × 100 m mit 20 s Pause
- **300 m ausschwimmen**

**Kein Dauerschwimmen.** Ausdauer ist nicht dein Limit, Wasserlage und Grundschnelligkeit sind es. Kurze Strecken mit Pause erlauben sauberes Schwimmen; ab 400 m am Stück verfällt die Technik und du übst den Fehler ein.

### Kurzeinheit (2000 m, 40 min, wenn ein Vormittag frei ist)
400 ein · 600 Technik · 800 als 16 × 50 m · 200 aus.

## Kohlenhydrate je Einheit

Alles in Gramm, weil sich das abmessen lässt. **Faustregel: unter 75 Minuten und locker braucht es nichts.**

| Einheit | Während | Vorher |
|---|---|---|
| Lauf ruhig 8–12 km | **0 g** | normal gegessen reicht |
| Rad locker 60 min | **0 g** | – |
| Geländeeinheit 8–10 km | **0 g** | – |
| Laufintervalle (Mi, 11:30) | **0 g** | **60–80 g** zum Frühstück, 2–3 h vorher |
| Rad hart VO2max (Fr) | **30–40 g** | 40–60 g im Frühstück |
| FTP-Test | **30–40 g** | 40–60 g |
| Schwimmen Verein 90 min | 0 g, nur trinken | Abendessen vorher |
| Langer Lauf 14 km | **30 g**, ab Minute 45 | – |
| Langer Lauf 16–18 km | **60 g**, verteilt ab Minute 40 | – |
| Sprint-Triathlon (27.09.) | **30 g** auf dem Rad | 60–80 g zwei Stunden vorher |
| Crossrennen (14.11., 28./29.11.) | **0 g** — zu kurz | 60–80 g zwei Stunden vorher |

**Praktische Einheiten:** eine Portion Nrgy Drink 90 sind 90 g (vier Messlöffel), ein Gel 30 g, ein Riegel rund 27 g, eine Banane rund 25 g. Halbe Portion Drink = 45 g.

### Zwei Gedanken dazu

**Für die DM selbst ist Verpflegung fast egal.** 3,2 km dauern elf Minuten, 6,4 km gut zwanzig. Da wird nichts nachgelegt, entscheidend ist allein, was zwei bis drei Stunden vorher im Magen war. Die Kohlenhydratdisziplin in diesem Block dient also nicht dem Zielwettkampf, sondern der **Trainingsqualität**: Die Mittwochsintervalle und die Freitagseinheit sind nur so gut, wie die Speicher es zulassen.

**Die eigentliche Magenschulung ist ein Thema für den Winter.** In Malterdingen sind 157 g pro Stunde durch den Magen gegangen, aufnehmbar waren davon vielleicht 90. Wer im Rennen 90 g/h verträgt, muss das über Monate an langen Radeinheiten geübt haben. Das gehört ab Dezember zu den langen Rollen- und Radeinheiten, nicht in den Crossherbst. Siehe [[Rennauswertung Breisgau Triathlon 2026]].

## Intensitätssteuerung, kurz

| Disziplin | Womit steuern | Warum |
|---|---|---|
| Rad | Prozent der FTP | Watt reagieren sofort, Puls hinkt hinterher |
| Laufen kurz und am Berg | **Laufleistung in Watt** | Pace sagt am Anstieg nichts, Puls hinkt hinterher |
| Laufen lang und flach | Watt, Pace als Gegenprobe | beide sofort verfügbar |
| Lockere Einheiten | Puls | hier ist er das ehrlichste Signal |

Siehe [[Trainingsplan]], [[Saisonplan Herbst 2026 – DM Cross]] und [[Radleistung – Hebel und Szenarien 2027]].
