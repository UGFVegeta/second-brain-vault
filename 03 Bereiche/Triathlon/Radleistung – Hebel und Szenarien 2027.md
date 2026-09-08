---
tags: [triathlon, radfahren, leistungsanalyse]
status: aktiv
date: 2026-09-06
---

# Radleistung – Hebel und Szenarien 2027

Physikalische Rechnung auf Basis der echten Streckendaten vom Breisgau Triathlon 2026. Beantwortet die Frage, was Gewicht, Watt und Aerodynamik jeweils an Zeit bringen — und zwar getrennt für Mitteldistanz und Sprint, weil dort unterschiedliche Regeln gelten.

## Das Modell

Aus der Fahrt vom 23.08.2026 (79,66 km, 893 hm, Ø 246 W) angepasst:

| Parameter | Wert |
|---|---|
| CdA | **0,282 m²** |
| Crr | 0,0032 |
| Luftdichte | 1,17 kg/m³ (25 °C, ~200 m) |
| Antriebsverlust | 2,5 % |
| Rad + Ausrüstung | 10 kg (Annahme, unkritisch: ±1,5 kg = ±26 s) |

**Güte:** Die Referenzsimulation liefert 2:20:01 gegen real 2:17:34, also 1,8 % daneben. Für Vergleiche brauchbar, weil sich der systematische Fehler herauskürzt. Absolutwerte mit Vorsicht.

✅ **Der CdA von 0,282 ist ein Fahrt-Durchschnitt, nicht die Position.** Am 08.09.2026 direkt gemessen (siehe unten): Die reine Aeroposition liegt bei **0,250 m²**, aufrecht auf dem Basislenker bei 0,324. Der Rennwert von 0,282 liegt also **0,032 über der Position** — das ist die Zeit, die im Rennen aufrecht gefahren wurde, vor allem an den drei Anstiegen.

## Aerodynamik-Feldtest vom 08.09.2026

Vier Durchgänge über dieselbe 1,74-km-Strecke zwischen Plüderhausen und Waldhausen, Muster aufrecht–aero–aero–aufrecht, damit sich Wind und Steigung herauskürzen. Runden 6, 8, 10 und 12 der Garmin-Originaldatei.

| | Strecke | Zeit | Tempo | Leistung |
|---|---|---|---|---|
| aufrecht (Runden 6 + 12) | 3476 m | 365 s | 34,28 km/h | 198,0 W |
| **aero (Runden 8 + 10)** | 3481 m | 337 s | **37,19 km/h** | 197,5 W |

**+2,91 km/h bei einem halben Watt Leistungsunterschied, also +8,5 %. 14 Sekunden auf 1,74 km.**

| | CdA aufrecht | CdA aero | Differenz |
|---|---|---|---|
| Basisannahme (ρ 1,19, Crr 0,0032) | 0,324 | **0,250** | **23 %** |
| Bandbreite über plausible Annahmen | 0,303–0,335 | 0,232–0,258 | immer 23 % |

Die 23 Prozent sind belastbar, weil sie ein Verhältnis sind und sich Annahmefehler herauskürzen. Der Absolutwert hängt an Luftdichte und Rollwiderstand.

**Der Test ist wiederholbar.** Gleiche Strecke, rund 197 W, gleiches Muster. Nach dem Aerofitting im April lässt sich damit belegen statt vermuten, ob Helm und Position etwas gebracht haben.

⚠️ **Zur Datenqualität:** Ohne die Garmin-Originaldatei war der Test nicht auswertbar. intervals.icu übernimmt die Gerätrunden nicht — im API-Datensatz stand nur ein einziges Intervall. Vier Rekonstruktionsversuche aus dem Rohstream schlugen fehl. **Lehre: Bei Messfahrten die Originaldatei heranziehen, nicht den intervals.icu-Datensatz.**

## Was Positionsdisziplin allein bringt

Gerechnet auf beiden echten Strecken, nur der CdA verändert, Leistung und Gewicht unverändert:

| Ziel-CdA im Rennschnitt | Malterdingen | Ligarennen |
|---|---|---|
| 0,270 | −1:32 | −0:28 |
| **0,260 (realistisches Ziel)** | **−2:52** | **−0:53** |
| 0,250 (dein gemessener Positionswert) | −4:13 | −1:17 |
| 0,240 (zusätzlich Aerofitting und Helm) | −5:36 | −1:43 |

**Das ist der billigste Hebel, den es gibt:** kein Training, kein Material, nur die vorhandene Position auch benutzen. In der Liga entspricht das der Hälfte dessen, was ein ganzer Winter mit +40 Watt bringt (2:35). In Malterdingen sind 4:13 fast so viel wie +20 Watt (5:00).

Realistisch ist **0,26**, nicht 0,25 — an einem steilen Anstieg mit 300 W bleibt man nicht zwingend auf den Aufliegern. Genau diese Fähigkeit, die Position auch bei hoher Leistung zu halten, ist das erklärte Ziel des Winterblocks.

## Einzelhebel im Vergleich

Gerechnet auf zwei echten Strecken: Malterdingen (80 km, 893 hm) und der Ligastrecke Ravensburg vom 01.08.2026 (24,57 km, 360 hm, also **13,9 hm/km**).

| Hebel | Malterdingen | Ravensburg (Liga) | rein flach, 20 km |
|---|---|---|---|
| 6 kg leichter (79 → 73 kg) | −1:58 | −0:35 | −0:04 |
| 4 kg leichter (79 → 75 kg) | – | −0:23 | – |
| +20 W | −5:00 | −1:22 | −0:39 |
| +40 W | – | **−2:35** | −1:15 |
| CdA 0,282 → 0,260 | −2:36 | −0:52 | −0:44 |
| CdA 0,282 → 0,245 | −5:36 | −1:29 | −1:15 |
| 75 kg, +40 W, CdA 0,260 | – | **−3:46** | – |
| 73 kg, +40 W, CdA 0,245 | – | **−4:32** | – |

**Die Rangfolge ist auf allen Strecken gleich: Leistung vor Aerodynamik vor Gewicht.** Wie stark das Gewicht durchschlägt, hängt am Profil — auf komplett flacher Strecke nichts, auf den welligen Ligastrecken gut eine halbe Minute, in Malterdingen fast zwei.

⚠️ **Korrektur vom 06.09.2026:** Die erste Fassung hatte die Ligarennen als flach modelliert und daraus geschlossen, Gewicht sei dort irrelevant. Das ist falsch. Die Rennen der Seniorenliga sind durchweg profiliert (Schluchsee stark, Erbach etwa hälftig, ein wirklich flaches Rennen gibt es kaum). Auf realem Profil sind sechs Kilo 35 Sekunden wert.

**Der Aerodynamik-Befund bleibt:** CdA 0,282 → 0,245 ist mit −1:29 mehr wert als sechs Kilo Gewichtsverlust und kostet keine einzige Trainingsstunde. Siehe [[helm-aerofitting-plan-2027]] und [[Sitzposition Zeitfahrrad (Cube Aerium C68)]].

## Woher 40 Watt kommen könnten

| Quelle | Größenordnung | Sicherheit |
|---|---|---|
| **Positionslücke schließen** | +0 bis 30 W | ⚠️ **unbelegt** |
| **Physiologisch**, inkl. erstmals systematischem Krafttraining | +10 bis 15 W | mittel |
| **Summe** | **+10 bis 45 W** | |

⚠️ **Korrektur vom 07.09.2026.** Die Positionslücke stand hier als „hoch" gesichert mit 20 bis 30 Watt. Das war eine Annahme, keine Messung. Die gemessene Leistungskurve ergibt eine Rennrad-FTP von rund **300 W statt der notierten 330** (bester 20-Minuten-Wert in zwölf Monaten: 314 W in jeder Position). Und der beste Zeitfahr-Wert von 284 W stammt aus einem bewusst eingeteilten Rennen, ist also kein Maximum. **Damit ist der größte Posten dieser Rechnung offen.** Details in [[Sitzposition Zeitfahrrad (Cube Aerium C68)]].

**Unabhängig davon steht seit dem 08.09. ein zweiter, sicherer Hebel fest:** die Positionsdisziplin im Rennen, wert bis zu 4:13 in Malterdingen. Die kostet nichts und hängt an keiner ungemessenen FTP.

Der größere Teil ist **keine Fitness, sondern Gewöhnung**. Trainingsansatz: in Aeroposition am Berg fahren, wo hohe Leistung und Position gleichzeitig gehalten werden müssen. Über den Winter auf den freien Rollen systematisch machbar.

**Priorisierung:** Die Positionslücke ist zwei- bis dreimal so groß wie der Kraftbeitrag und deutlich sicherer. Wenn im Winter die Zeit knapp wird, gewinnt die Rolleneinheit in Aeroposition gegen die zusätzliche Studioeinheit.

**+40 W auf die Zeitfahr-FTP ist realistisch. +40 W auf die Rennrad-FTP wäre es nicht.** Diese Unterscheidung ist wichtig, sonst wird im Frühjahr am falschen Wert gemessen.

### Was die Trainingshistorie dazu sagt (geprüft am 06.09.2026)

⚠️ **Korrektur:** Eine frühere Fassung behauptete, es habe „nie einen strukturierten Winterblock auf dem Rad" gegeben. Das ist **falsch**. Auswertung von 1843 Aktivitäten seit 2023:

| Radstunden | Nov | Dez | Jan | Feb | Mär |
|---|---|---|---|---|---|
| 2023/24 | 11,8 | 15,1 | 16,6 | 14,7 | 7,8 |
| 2024/25 | 7,1 | 23,8 | 18,4 | 16,9 | 8,4 |
| 2025/26 | 19,4 | 10,6 | 16,4 | 17,3 | **35,6** |

Das sind vier bis sechs Radstunden pro Woche, also so viel wie im Sommer. Das Rad läuft im Winter durch.

**Beim Krafttraining stimmt das Bild dagegen.** Zählt man nur Einheiten ab 30 Minuten (kürzere waren Dehn- und Mobilitätsroutinen):

| Jahr | unter 30 min | ab 30 min | Stunden |
|---|---|---|---|
| 2023 | 179 | 44 | 36,8 |
| 2024 | 34 | 39 | 39,2 |
| 2025 | 22 | 7 | 5,4 |
| 2026 | 0 | 2 | 1,5 |

**92 echte Krafteinheiten in 3 Jahren und 9 Monaten, also 0,48 pro Woche** — Oskars eigene Einschätzung „alle zwei Wochen" trifft genau zu. Zweimal pro Woche wäre das Vierfache des bisherigen Schnitts und das Zweieinhalbfache der besten Phase 2023/24. Systematisches, triathlonspezifisches Krafttraining über einen längeren Zeitraum hat es noch nie gegeben.

Dazu passt, dass der Radpuls deutlich unter dem Laufpuls liegt, was eher auf ein muskuläres als ein zentrales Limit hindeutet.

⚠️ Zwei Einschränkungen: Zweimal 30 bis 40 Minuten sind gemessen an der Studienlage eine moderate Dosis (dort meist 2–3× 45–60 min), der Effekt liegt also eher am unteren Rand der publizierten Werte. Und intervals.icu kennt nur Aufgezeichnetes — nicht getrackte Studiobesuche fehlen in der Statistik.

## Szenarien Malterdingen 2027

| Szenario | Zeit | gegenüber 2026 |
|---|---|---|
| vorsichtig: 75 kg, NP 275 W, CdA 0,270 | 2:15:58 | −4:03 |
| **realistisch: 74 kg, NP 285 W, CdA 0,260** | **2:12:07** | **−7:53** |
| optimistisch: 73 kg, NP 290 W, CdA 0,245 | 2:08:44 | −11:16 |

**Der eigentliche Gewinn liegt aber woanders:** NP 285 gegen eine FTP von 340 sind 84 % Intensität. 2026 waren es NP 270 gegen 300, also 90 %. Also 15 Watt mehr Leistung bei **geringerer** relativer Belastung. Schnellere Radzeit und frischere Beine gleichzeitig, das genaue Gegenteil von 2026. Siehe [[Rennauswertung Breisgau Triathlon 2026]].

## Seniorenliga: der Abstand zu Platz eins

In der Seniorenliga gilt **Windschattenverbot**, gewonnene Radzeit ist also voll wirksam und wird nicht von einer Gruppe eingeebnet. Referenz ist Ravensburg (NP 301 W bei Ø 216 W, Variabilitätsindex 1,39 — für einen Sprint mit rund 100 % Schwellenintensität richtig eingeteilt).

**Oskar war 2026 Zweiter oder Dritter. Platz eins lag jeweils zwei bis zweieinhalb Minuten vor ihm, und zwar auf dem Rad.**

Die 40 Watt allein sind auf dieser Strecke **2:35** wert und schließen die Lücke damit rechnerisch. Mit Gewicht und Aerodynamik zusammen sind es 3:46 bis 4:32, er käme also vor dem Sieger vom Rad. Ob das für Platz eins reicht, hängt am Schlusslauf des Konkurrenten. Als Läufertyp mit dem Rad vorn wegzukommen ist aber eine grundlegend andere Ausgangslage als zweieinhalb Minuten aufholen zu müssen.

**Einordnung:** Um dieselben zwei Minuten auf der Laufstrecke zu holen, müssten 5 km um 24 s/km schneller gelaufen werden. Illusorisch. Zwei Minuten liegen zudem in der Größenordnung des gesamten Schwimmrückstands auf einen guten Schwimmer über 750 m. **Die Schwimmschwäche lässt sich über das Rad kompensieren**, und das ist der deutlich leichtere Weg, als nach dreizehn Jahren die Wasserlage umzubauen.

## Zum Gewicht

Gewicht ist für einen Triathleten in erster Linie ein **Laufthema**, nicht ein Radthema. Vier Kilo waren in der Rechnung vom August zwei bis dreieinhalb Minuten allein auf der Laufstrecke einer Mitteldistanz wert, deutlich mehr als auf dem Rad. Dazu kommt das subjektive Befinden: Bei 79 kg fühlt sich Oskar nicht gut. Zielkorridor **75 kg als Untergrenze, 73 bis 74 bei guter Wintervorbereitung**. Siehe [[Körpergewicht & Körperzusammensetzung]].

⚠️ Leichter werden macht **nicht stärker**. Die absoluten Watt bleiben gleich oder sinken minimal, es steigen die Watt pro Kilo. Der Kraftgewinn kommt aus dem Winterblock, nicht von der Waage.

## Konsequenzen

- **Rangfolge der Hebel überall: Leistung, dann Aerodynamik, dann Gewicht.**
- **Für die Liga:** 40 Watt sind der Schlüssel zum Radabstand auf Platz eins. Aerodynamik ist der billigste Zusatz.
- **Für Malterdingen: alle drei Hebel, Leistung am stärksten.**
- **Aerofitting und Helm im April 2027 sind gleichwertig zu einem Trainingsjahr**, nicht Kosmetik.
- **Doppeltest Ende September**, einmal Rennrad und einmal Zeitfahrposition, mit ein paar Tagen Abstand. Danach ist die Positionslücke gemessen statt geschätzt und über den Winter verfolgbar. Ohne das lässt sich im Frühjahr nicht unterscheiden, ob 40 Watt gewonnen wurden oder nur besser geschätzt.

⚠️ Sämtliche Ausgangswerte für die FTP (Rennrad 330 W, Zeitfahrposition 295–310 W) sind **geschätzt, nicht gemessen**. Die ganze Rechnung steht und fällt mit dem Doppeltest.

Siehe [[Saisonplan Herbst 2026 – DM Cross]] und [[Rennauswertung Breisgau Triathlon 2026]].
