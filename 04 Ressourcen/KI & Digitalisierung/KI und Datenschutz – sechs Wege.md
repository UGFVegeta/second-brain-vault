---
tags: [ki, datenschutz, claude]
status: aktiv
date: 2026-11-07
---

# KI und Datenschutz – sechs Wege

Quelle: Video „So nutzt du Claude Code & KI-Modelle datenschutzkonform (6 Möglichkeiten)“ von Name-110 Ivanov, YouTube, 27 Min.: https://youtu.be/4WLCG1uLZD4 (ausgewertet über das Transkript, keine Rechtsberatung, sagt er selbst).

## Kernaussage

Entscheidend ist, welche Daten in die KI gehen, nicht welches Werkzeug. Öffentliches ohne Personenbezug ist unkritisch. Personenbezogene Daten brauchen einen Vertrag zur Auftragsverarbeitung (AVV). Gesundheits- und Finanzdaten brauchen noch mehr Kontrolle.

## Die Treppe

Je weiter unten, desto mehr Kontrolle über die Daten, aber schwächere Modelle und mehr Aufwand.

1. US-Anbieter direkt über API (OpenAI, Anthropic, Google): stärkste Modelle, Daten in den USA, Speicherung meist ca. 30 Tage, AVV plus Standardvertragsklauseln nötig.
2. Dieselben Modelle in einer EU-Region (Azure EU Data Zone, AWS Bedrock Frankfurt): laut ihm der pragmatische Mittelweg, den die meisten Firmen nehmen.
3. Souveräne Clouds (AWS European Sovereign Cloud): noch in der Entwicklung, kaum starke Modelle.
4. Europäische Anbieter (Mistral, Ionos, Stackit, Scaleway): EU-Vertragspartner, DSGVO, offene Modelle günstig.
5. Gemietete Grafikkarte mit offenem Modell (Runpod, Hetzner, Scaleway).
6. Lokales Modell auf eigener Hardware: Daten verlassen das Gerät nie, aber teuer und kleinere Modelle.

Nebenbei: Ein offenes Modell ist nur eine Datei. Wer DeepSeek bei Scaleway nutzt, schickt nichts nach China. Wer die DeepSeek-App nutzt, schon.

## Claude-Abos

- Free, Pro und Max laufen unter Verbraucherbedingungen: **kein AVV**, Chats werden standardmäßig fürs Training genutzt (abschaltbar in den Einstellungen).
- Kommerzielle Bedingungen (Team, Enterprise, API-Key) haben den AVV (Data Processing Addendum) dabei, Verarbeitung aber in den USA.
- EU-Verarbeitung nur über Bedrock Frankfurt, Abrechnung pro Token, laut Video schnell dreistellig im Monat.
- Seine Regel für Claude Code mit Abo: an eigenen Projekten arbeiten oder mit Testdaten, keine echten Personendaten Dritter.

## Was das für mich heißt

- Training auf claude.ai abschalten (Einstellungen → Datenschutz, genauen Namen des Schalters vor Ort prüfen). Offen, ob schon erledigt.
- Der Namensschutz-Mod (Platzhalter statt Schülernamen) ist genau das Testdaten-Prinzip. Lücke bleibt: PDFs, Scans und Fotos deckt er nicht ab.
- Graubereich: Postfach-Sortierung (web.de, Gmail, WeinstadtCross-Anmeldungen) läuft über Claude Pro, also Personendaten Dritter ohne AVV. Einfachste Entschärfung: nur Absender und Betreff auswerten lassen.
- Gemini Plus ist ebenfalls ein Verbraucherabo.
- Datensparsamkeit: nur das in die KI geben, was die Aufgabe braucht.
- Speicherort: Vault auf GitHub nur ohne Personendaten (gilt schon). Für iCloud „Privat/Wichtige Dokumente“ den Erweiterten Datenschutz von Apple prüfen (Ende-zu-Ende). Offen, ob aktiv.
- Paperless auf dem Pi ist bereits die lokale Lösung.
- Weg 6 gibt es schon als Projekt: [[KI-Assistent Setup (Hermes & Hardware)]]. Dorthin gehören auch sensible Fälle wie Scans mit Schülernamen. Sein Testtipp unten gilt vor dem Hardwarekauf.
- Nicht nötig: Bedrock, eigene GPUs. Passt nicht zu [[Zusammenarbeit mit Claude|Pro ohne API]] und „einfach schlägt komplex“.

## Für Schule und Konrektor-Rolle

- Die Treppe eignet sich als Folie fürs Kollegium: Schülerdaten gehören nicht in Verbraucher-KI, Unterrichtsplanung ohne Personenbezug ist unproblematisch.
- Vor jedem Hardwarekauf für lokale KI: erst das Modell mit Testdaten ausprobieren, dann passende Hardware ein paar Stunden mieten.
