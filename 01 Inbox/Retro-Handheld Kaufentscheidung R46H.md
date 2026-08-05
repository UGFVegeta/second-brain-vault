---
tags: [kaufentscheidung, retro-gaming, familie]
status: aktiv
date: 2026-08-03
---

# Retro-Handheld: R46H

## Entscheidung

Gekauft wird **ein** R46H (4,2 Zoll, 64 GB) über AliExpress, 58 € inklusive Versand, Zoll und Aufbewahrungsbox. Zweck: Emulation bis PS1 für Oskar, später Einstiegsgerät für die Kinder.

Bewusst **nur ein Gerät**, weil Tochter frühestens in einem Jahr soweit ist und Sohn in ca. vier Jahren. Bis dahin gibt es für dasselbe Geld bessere Hardware.

**Zuerst war der R36H Pro Max bestellt und wurde storniert.** Der R46H ist dieselbe Hardware, hat aber die bessere Tastenanordnung: **Steuerkreuz oben, Stick unten.** Bei den Systemen, um die es geht (NES, Game Boy, Mega Drive, SNES, Arcade), ist das Steuerkreuz das einzige Eingabegerät, das zählt, und liegt damit dauerhaft in der natürlichen Daumenposition. Genau deshalb sitzt es beim SNES-Pad, beim Mega-Drive-Pad und bei allen Nintendo-Handhelds dort. Nachteil ist spiegelbildlich, dass der Stick bei den wenigen 3D-PS1-Titeln unbequemer liegt, das ist der kleinere Verlust.

💡 **Die Tastenanordnung ist die einzige Angabe, die kein Verkäufer im Text schönschreiben kann.** Sie ist auf den Produktfotos direkt sichtbar. Bei diesem Punkt den Bildern trauen, nicht der Beschreibung.

## Die wichtigste Erkenntnis zur Serie

**Alle Geräte der R36-Serie haben denselben RK3326.** R36S, R36H, Plus, Max, Ultra, Ultra X und Pro Max. Der R46H ebenfalls. Es gibt in dieser Serie kein leistungsstärkeres Modell, egal was der Name verspricht. Angebote, die RK3566 mit 2 GB RAM behaupten, sind nicht verlässlich, weil „R36 Ultra" kein geschützter Produktname ist.

Der Name kauft also **nur Bildschirm, Gehäuse und Tastenanordnung**, keine Rechenleistung.

⚠️ Der Name „R46H" ist genauso unzuverlässig. In Angeboten stehen wahlweise 5 Zoll, 144 Hz, 1280 × 720 oder 4,3 Zoll mit 480 × 272, dazu ein erfundener „GAMET5 chip". Nur die Kombination **4,2 Zoll, 1024 × 768, RK3326** ist durch mehrere unabhängige Quellen gedeckt.

**Einzige echte Ausnahme in dieser Familie: der R46S.** Der hat laut retrohandhelds.gg wirklich den **RK3566** mit 1 GB DDR4, bei 4 Zoll und 720 × 720 im 1:1-Format. Für PS1 und darunter nicht nötig, aber merken für das zweite Gerät in ein paar Jahren.

Quellen: Notebookcheck, retrohandhelds.gg, retrocatalog.com, r/SBCGaming.

## Displayvergleich

| Modell | Größe | Auflösung | Format | Typ | PPI |
|---|---|---|---|---|---|
| R36S | 3,5" | 640 × 480 | 4:3 | IPS | 228 |
| R36H | 3,5" | 640 × 480 | 4:3 | IPS | 228 |
| R36 Plus | 4,0" | 720 × 720 | 1:1 | IPS | 255 |
| R36 Max | 4,0" | 720 × 720 | 1:1 | TFT | 255 |
| R36 Ultra | 4,0" | 720 × 720 | 1:1 | IPS | 255 |
| R36 Ultra X | 4,5" | 640 × 480 | 4:3 | IPS | **178** |
| R36H Pro Max | 4,2" | 1024 × 768 | 4:3 | IPS | **305** |
| **R46H (gekauft)** | **4,2"** | **1024 × 768** | **4:3** | **IPS** | **305** |

Der Ultra X hat das größte **und** das schlechteste Display: dieselbe Auflösung wie der R36S, auf 4,5 Zoll gezogen. Der Pro Max und der R46H teilen sich das mit Abstand beste Panel der Serie.

## Specs R46H

RK3326, 4× Cortex-A35 bis 1,5 GHz · 1 GB DDR3L · Mali-G31 MP2 (520 MHz) · 4,2" IPS 1024 × 768 · **WLAN** · horizontales Format · Steuerkreuz oben

WLAN ist neben dem Display der wichtigste Vorteil gegenüber dem einfachen R36S/R36H, die **kein** WLAN haben und USB-C-OTG plus Dongle bräuchten. Mit WLAN kommt Claude per SSH direkt aufs Gerät (ArkOS: Benutzer `ark`, Passwort `ark`, dazu Samba).

## Bestelldetails

**Bestellt am 03.08.2026 über AliExpress: 58 € inklusive Versand, Zoll und Aufbewahrungsbox**, also Endpreis ohne Nachforderung an der Haustür.

Nicht genommen: ein BOYHOM PRO MAX für ca. 52 € nach Gutschein (Artikel-ID 1005012059031727) mit nur **2 Bewertungen bei 27 verkauften Stück**. Die Differenz kauft Verkäuferhistorie, und das ist bei diesen Geräten die richtige Priorität: Die Spezifikationen stimmen bei vielen Angeboten, das Risiko liegt fast immer beim Verkäufer.

⚠️ „Zertifizierte Marke" ist bei AliExpress nur ein Markenregister-Eintrag und sagt nichts über die mitgelieferte Speicherkarte aus. Der `f3`-Test bleibt der erste Handgriff nach Ankunft.

## Nach Ankunft: Einrichtung

1. **`f3`-Test auf die mitgelieferte Karte**, solange der AliExpress-Käuferschutz läuft. Häufigste Masche bei diesen Geräten ist eine gefälschte Kapazität (z. B. „64 GB", real deutlich weniger).
2. Originalkarte **unangetastet lassen** als Rückfallebene.
3. Eigene 64-GB-Karte (zwei liegen zu Hause) in den zweiten Slot, darauf die aufgeräumte Version bauen. Prüfen, ob der R46H wirklich zwei Kartenslots hat, der normale R36H hat sie laut Notebookcheck.
4. Wenn per Kartenleser am Mac gearbeitet wird: vor dem Auswerfen `dot_clean` laufen lassen, sonst erscheinen macOS-Begleitdateien (`._*`, `.Spotlight-V100`) später als Geisterspiele im Menü.

⚠️ **Systemordnernamen nicht umbenennen.** EmulationStation ordnet jedem Ordner einen festen Emulator zu (`psx`, `snes`, …). Umbenennen lässt ganze Systeme aus dem Menü verschwinden.

## Kinderkarte (später)

Die vorinstallierten „20.000 Spiele" sind eine ungeordnete Halde aus Dubletten, Regionalfassungen, Hacks und kaputten Dateien. Für ein Kind unbrauchbar.

**Behalten:** Arcade, NES, Game Boy / GBC, Master System / Game Gear, Mega Drive, SNES, GBA. PS1 später und ausgewählt.

**Rauswerfen:** alles vor NES/Game Boy an Heimkonsolen (Atari & Co.), außerdem N64, Dreamcast, PSP und Heimcomputer.

Großer Hebel: ArkOS blendet ein System automatisch aus, sobald sein Ordner leer ist. Also erst komplette Systeme kippen, dann den Rest nach Bedienbarkeit sortieren, nicht nach Baujahr.

**Ausnahme zur Regel „nichts vor NES":** Arcade-Klassiker aus genau dieser Zeit funktionieren bei Kindern hervorragend (Pac-Man, Donkey Kong, Galaga, Dig Dug, Frogger, Bubble Bobble). Spielhallen hatten bessere Hardware und Spiele, die einen Fremden in zehn Sekunden abholen. Der sinnvolle Schnitt läuft zwischen Arcade und Heimkonsole, nicht am Baujahr.

Sortierkriterium für die Auswahl: „kommt ein Kind allein rein", nicht Epoche. 8-Bit und Game Boy sind oft der bessere Einstieg als SNES, weil zwei Knöpfe, kurze Runden und kein Lesen nötig.

## Realistische Erwartung an die Leistung

- PS1 und alles darunter: läuft sauber
- N64 und Dreamcast: Glückssache pro Spiel, trotz Werbeversprechen
- Nintendo DS: läuft per DraStic meist in Vollgeschwindigkeit, aber **kein Touchscreen** (Stylus wird als Cursor mit dem Stick geschoben) und zwei DS-Bildschirme müssen pro Spiel aufs Display verteilt werden. Bonus, kein Verkaufsargument.
- PS1-Auflösung **nicht** hochrechnen: „enhanced resolution" in RetroArch kostet auf dem RK3326 zu viel Bildrate. Nativ fahren.
- 1024 × 768 ist kein glattes Vielfaches der klassischen Auflösungen, dadurch minimal ungleiche Pixelreihen. Bei 305 PPI unsichtbar. Wer will, stellt in RetroArch ganzzahlige Skalierung ein.

## Offen: AYN Thor (separater, späterer Kauf)

Klapp-Handheld mit zwei AMOLED-Displays, Android 13. Nicht für Kinder geeignet (Scharnier, zwei Displays, Preis). Klare Aufgabenteilung: Thor für Oskar, R46H für Familie und Urlaub.

**Preise ayntec.com (Stand 03.08.2026):** Lite 8+128 (SD865) 259 $ · **Base 8+128 (8 Gen 2) 329 $** · Pro 12+256 409 $ · Max 16+512 479 $ · Max 16+1TB 579 $. Lite und Base gibt es nur in Schwarz, Farben erst ab Pro.

**Base ist die richtige Wahl:** 8 Gen 2 ohne den RAM-Aufpreis, der für Retro-Emulation nichts bringt.

**Günstiger über den offiziellen AYN Store auf AliExpress**, dort waren es laut Notebookcheck (Januar 2026) 311,90 $ für den Base, und Rabattcodes lassen sich anwenden, was auf ayntec.com nicht geht. Globale Codes (Quelle: Retro Game Corps, Gültigkeit ungeprüft): `AFMY25` 25 $ ab 209 $ · `AFMY40` 40 $ ab 329 $ · `AFMY55` 55 $ ab 449 $. Nur im Store kaufen, der wörtlich „AYN Official Store" heißt, Wiederverkäufer verlangen über 700 $.

**Idee „zwei kaufen, eins verkaufen":** Break-even bei ca. 362 € Einstand (mit EinfuhrUSt) liegt bei rund 416 € über eBay und rund 370 € über Kleinanzeigen mit Abholung. Für 100 € Ersparnis müsste der Verkaufspreis bei rund 527 € (eBay) bzw. 462 € (Kleinanzeigen) liegen. **Kleinanzeigen ist der einzig sinnvolle Weg**, die eBay-Provision von 11 % frisst die Marge. Vorher unbedingt die **verkauften** Artikel bei eBay Deutschland prüfen, Angebotspreise sagen nichts. Steuerlich unkritisch: 100 € Gewinn aus einem Einzelverkauf liegt klar unter der Freigrenze von 1000 € für private Veräußerungsgeschäfte.

## Merkposten für AliExpress allgemein

Produktlinks sind an Region und Session gebunden und lassen sich nicht weitergeben. Claude kann Produktseiten wegen reCAPTCHA nicht auslesen. Prüfung immer selbst in der eigenen App, Screenshot der Spezifikationstabelle reicht Claude für die Einschätzung.
