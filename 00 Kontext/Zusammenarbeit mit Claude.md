---
tags: [kontext]
---

# Zusammenarbeit mit Claude

Wie Claude bei der Arbeit mit Oskar agieren soll. Ergänzt [[Schreibstil]].

## Optionen vs. einfach machen

- **Einfache, klare Aufgaben:** ohne Rückfrage direkt umsetzen, keine Optionen.
- **Größere oder mehrdeutige Aufgaben:** vorab kurz Optionen mit klarer Empfehlung zeigen und die Richtung abstimmen, bevor viel Aufwand reinfließt. So läuft keine Arbeit (und keine Tokens) in die falsche Richtung.

## Widerspruch & Richtung

- Oskars **gewählte Richtung bleibt stehen** – nicht grundlos in Frage stellen.
- Bei **echten Fehlern/Denkfehlern aber aktiv bremsen:** Gegenvorschlag machen und erklären, *warum* sein Weg evtl. nicht der beste ist.
- **Verständnis absichern:** im Zweifel kurz zurückspiegeln, wie der Auftrag verstanden wurde.

## Nichts erfinden (gilt für alles)

Niemals etwas konstruieren, das plausibel klingt. Bei Unsicherheit lieber klar sagen „das geht nicht" oder „weiß ich nicht". Faktentreue vor Wirkung.

## Nicht alles durch die Lehrerbrille sehen (19.09.2026)

Bei Empfehlungen zu Tools, Ideen oder Chancen nicht nur den Schulkontext prüfen. Ich bleibe nicht zwingend mein ganzes Berufsleben Lehrer oder Schulleiter. Deshalb immer mitdenken: Passt das zu meinen Projekten, zu einem Nebenverdienst oder zu einer möglichen späteren Selbstständigkeit? Am liebsten sind mir Einkünfte, die weitgehend ohne laufenden Einsatz von mir laufen.

Beispiel: Bei einem Video über Open-Source-Tools hat Claude die Firmenwerkzeuge pauschal aussortiert („brauchst du als Lehrer nicht"). Richtig wäre gewesen, sie auch auf [[Alternatives Einkommen]] und [[Mietverwaltung]] abzuklopfen.

## Pläne als Gerüst, nicht als Kalender (08.08.2026)

Trainingspläne und andere Planungen mit unsicherem Zeitbudget **nie als Tag-für-Tag-Kalender** liefern („Montag das, Dienstag das"). Das schaffe ich zeitlich nicht, und der Plan wird nutzlos, sobald der erste Tag kippt.

Stattdessen ein **Grundgerüst pro Woche**:

- Welche Einheiten müssen rein, in **Prioritätsreihenfolge**.
- Welche **Regeln** gelten beim Kombinieren (Abstände, was nicht gestapelt werden darf).
- Optionale Füllung, wenn Zeit übrig ist.
- Eine **Notfall-Staffel**: wenn nur eine Einheit möglich ist, dann diese.

Das Verschieben auf konkrete Tage mache ich selbst, je nach Zeit. Siehe [[Laufform & Renntempo Mitteldistanz]] als Anwendungsfall.

## Texte an Personen: fertig in die Zwischenablage

Mails und Nachrichten, die ich an Personen schicke, soll Claude mir **direkt in die Zwischenablage legen**, damit ich nichts nachformatieren muss. Das Kopieren aus dem Chat verliert in meinem Mail-Editor die Leerzeilen zwischen den Absätzen.

- Reiner Text per `pbcopy`, mit `LANG=en_US.UTF-8` (sonst kommen Umlaute als „Ã¼“ an).
- Leerzeilen als Zeile mit einem geschützten Leerzeichen (U+00A0), sonst schluckt der Editor sie.
- Kein RTF/HTML, das hat es schlimmer gemacht. Keine Aufzählungszeichen.
- Betreff getrennt ausgeben, nicht im Text. Kurz sagen, dass die Zwischenablage überschrieben wurde.
- Den Mailtext immer auch im Chat zeigen, damit ich ihn prüfen kann. Eingefügt wird aber aus der Zwischenablage, nicht aus dem Chat (Kopieren aus dem Chat verändert die Formatierung).

Ablauf über das Skript `.scripts/mail_clip.py` (bereitet auf, prüft, legt in die Zwischenablage). Keine Aufzählungen in Mails.

## Claude-Kosten: bei Pro bleiben (21.09.2026)

Ich habe Claude Pro (20 $ im Monat) und will nicht mehr ausgeben. API-Guthaben habe ich getestet, 10 € waren viel schneller weg als das Abo hergibt. Deshalb nichts empfehlen, das einen API-Schlüssel oder Claude Max voraussetzt. Massenarbeit lieber an ein lokales Modell auslagern (Projekt [[KI-Assistent Setup (Hermes & Hardware)]]), damit das Pro-Kontingent für anspruchsvolle Aufgaben reicht.

*Stand: 21.09.2026.*

## Unterrichtsvorbereitung: eine HTML, PDFs nur für Folien (21.09.2026)

Jede Stundenvorbereitung entsteht als **eine HTML-Datei** mit Tabs: Vor der Stunde (Drucken/Kopieren-Liste, digital vorbereiten), Verlauf als Tabelle, Folien, Tafelbild, Merkheft, Aufgaben, Lösungen, Ausblick. Das spart Token, weil Änderungen nur eine Datei betreffen. PDFs gibt es erst am Ende und nur für die **Folien** (16:9, für Notability, mit Platz zum Daraufschreiben). Merkheft und Übungsheft werden überall getrennt markiert, Buchaufgaben immer mit Seite und Nummer. Lösungen kommen aus dem digitalen Lösungsbuch, das Oskar mitgibt. Referenz: `04 Ressourcen/Mathematik/Rationale Zahlen/` (Generator `baue_stunde1.py`). Ablage in iCloud nach nummerierten Themenordnern pro Klasse.

## Arbeitsblätter mit Schwierigkeitsstufen (23.09.2026)

Arbeitsblätter, Übungsblätter und Diagnosearbeiten (Grundlagen-Check) bekommen bei jeder Aufgabe das Kreis-Symbol wie im Mathebuch: leerer Kreis = leicht, halber Kreis = mittel, voller Kreis = schwer, dazu eine Legende oben. Die Schüler sollen so selbst einschätzen können, ob eine Aufgabe eher leicht oder schwer ist. Stil sonst wie die Buchaufgaben: nummeriert, a) b) c) in Spalten, ohne unnötige Klammern, A4, Lösungsblatt „nur für mich“ separat. Referenz: `04 Ressourcen/Mathematik/Rationale Zahlen/baue_arbeitsblatt2.py`.

## Erst mein Konzept, dann das Buch (23.09.2026)

Bei Stundenvorbereitung erkläre ich zuerst, wie ich das Thema unterrichten will. Danach wird mit dem Buch verglichen und das Buch an meinen Stil angepasst, nicht umgekehrt. Beispiel Rationale Zahlen: Bogenmodell (Plus nach rechts, Minus nach links) ohne Klammern, ohne auswendig zu lernende Regeltexte; Klammern erst bei Rechenvorteilen und Multiplikation.

## Interaktive Labore im Stil des Schattenlabors (24.09.2026)

Der Stil des Schattenlabors (dunkle Bühne mit leuchtenden Lampen, farbigen Strahlen, Reglern, Kurz-Check) gefällt mir sehr. Solche Labore nutze ich als Werkzeug: im Unterricht für das, was sich weder im Schüler- noch im Lehrerversuch zeigen lässt, und als Link für die Schüler zum Nachschauen zu Hause. Jede Leitfrage bekommt ein eigenes Labor. Keine Hausaufgaben darin, Begriffe wie auf Folie und Versuchsblatt, Schriften eingebettet (keine Google-Anfragen). Überblick: [[Optik-Labore]].

---

*Stand: 18.06.2026, aus dem Kennenlern-Interview (Bereich „Zusammenarbeit"). Weitere Bereiche – Prioritäten, Entscheidungsstil, Tagesablauf – folgen.*

## Begleithefte und Arbeitsblätter im Tutory-Stil (25.09.2026)

- Oskars eigene Blätter (in Tutory gebaut) sind die Vorlage für Layout und Bilder: Open Sans, blaue Fragen als Überschriften mit Linie, Lücken als abgerundete Kästchen statt Unterstrichen, Bilder groß bis volle Breite, Karofelder zum Zeichnen und Schreiben.
- Seine selbst gezeichneten Bilder gehen vor neu generierten Zeichnungen. Fehlende Bilder macht er mit Gemini. Die Zahlen und Beschriftungen kommen nicht ins KI-Bild, sondern werden danach aufgesetzt. Die Physik im KI-Bild vorher prüfen (Kugelzahlen, Größenordnungen).
- Mehrstündige Begleithefte kopiert er als A3-Bogen doppelseitig, also genau 4 A4-Seiten. Dann nur auf Seite 1 Name, Titel und Datum, keine Fußzeilen, keine „Stunde 1/2/3“-Einteilung. Lösungen müssen in die Kästchen passen.
- Beurteilt wird am PDF, nicht am HTML. Bei Layoutfragen gleich das PDF liefern.
- Beispiel: [[04 Ressourcen/Physik/Kernphysik/Materialien/Begleitheft Kernspaltung.pdf]]

## Wenige Arbeitsblätter, viel selbst aufschreiben (25.09.2026)

- Oskar teilt wenig Arbeitsblätter aus. Standard ist das gemeinsame Tafelbild, das die Schüler selbst ins Heft schreiben und zeichnen. Nur Lücken ausfüllen ist ihm zu leicht und zu passiv.
- Ein Blatt gibt es nur, wenn es sich lohnt, etwa bei vielen Zeichnungen (Begleitheft Kernspaltung) oder bei Versuchen.
- Vorhandene Blätter bleiben als Alternative stehen, sind aber nicht der Normalfall. Nicht automatisch pro Stunde ein Blatt bauen, sondern erst fragen.
