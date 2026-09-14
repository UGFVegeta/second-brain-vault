---
tags: [ressource, mathematik, unterricht, diagnose]
status: aktiv
erstellt: 2026-09-09
---

# Grundlagen-Check – Workflow

Diagnose-Test zum Schuljahresstart: Schüler bekommen eine Rückmeldung, was sie können und was nicht, ohne Note. Oskar bekommt zusätzlich eine Klassenübersicht, um Unterrichtsschwerpunkte zu setzen. Dasselbe Muster funktioniert auch während des Jahres für ungenotete Zwischenchecks zu neuen Themen.

Läuft jedes Jahr wieder, deshalb eigener Unterordner: **Klasse 5-6/** und **Klasse 6-9/** liegen hier direkt unter `Arbeitsblätter/Grundlagen-Check/`, statt in den klassenweise sortierten Ordnern der übrigen Arbeitsblätter.

## Datenschutz – die eine Regel, die alles trägt

**Kein Name kommt in irgendeine Datei, die Claude sieht, und keiner ins Vault.** Die Schüler tragen nur eine zugeteilte Nummer ein, nie ihren Namen. Die Zuordnung Nummer → Name bleibt bei Oskar – auf Papier oder in einer Datei außerhalb dieses Vaults. Ohne diese Zuordnung sind Antwortbögen, Scans und Auswertungen anonym.

## Die beiden Tests

| | Klasse 7 (neu) | Klasse 10 (weiterführend) |
|---|---|---|
| Aufgabenblatt | [[Grundlagen Klasse 5-6 Teil 1]] + [[Grundlagen Klasse 5-6 Teil 2]] | [[Grundlagen Klasse 6-9]] |
| Lösungen (nur für Oskar) | [[Grundlagen Klasse 5-6 Teil 1 Lösungen]] + [[Grundlagen Klasse 5-6 Teil 2 Lösungen]] | [[Grundlagen Klasse 6-9 Lösungen]] |
| Antwortbogen | [[Antwortbogen Grundlagen Klasse 5-6 Teil 1]] + [[Antwortbogen Grundlagen Klasse 5-6 Teil 2]] | [[Antwortbogen Grundlagen Klasse 6-9]] |
| Ablauf | zwei Tage, Teil 1 dann Teil 2 | ein Tag, komplett |

Die Klasse-6–9-Version wurde letztes Schuljahr fürs Ende der 9. Klasse gebaut – für die jetzige 10. passt sie unverändert als „hat es über den Sommer gehalten"-Check, an einem Stück.

Die Klasse-5–6-Version ist neu, zugeschnitten auf das, was eine neue 7. Klasse aus Klasse 5/6 mitbringen sollte (Prozent, Terme und Pythagoras kommen bewusst nicht vor, das haben sie noch nicht gelernt). Sie läuft bewusst **in zwei Blöcken**, damit es für die neue Klasse nicht zu viel auf einmal wird: Teil 1 deckt Block A und B ab (Grundrechenarten, Brüche), Teil 2 Block C und D (Dezimalzahlen, Größen und Geometrie). Ob dazwischen ein ganzer Tag oder nur eine Pause/Sportstunde liegt, ist egal – Hauptsache derselbe Ablauf, dieselbe Nummer. Beide Teile zusammen ergeben das komplette Bild – die Auswertung fasst sie am Ende zu einer Rückmeldung pro Nummer zusammen, siehe unten.

## Selbsteinschätzung auf dem Antwortbogen

Rechts bei jeder Aufgabe kreuzen und malen die Schüler zusätzlich einen von drei Smileys an (sicher / ging so / unsicher), eine Einschätzung pro Aufgabe, nicht pro Teilaufgabe.

Seit der Auswertung für 7c fließt das mit ein: die Ergebnisdatei bekommt ein optionales `selbsteinschaetzung`-Feld (Format unten), der Bericht zeigt dann zusätzlich ein Diagramm – wie oft „sicher gefühlt" auch wirklich richtig war – und bei jeder Nummer einen Warnhinweis, welche Aufgaben sicher gefühlt, aber falsch waren. Genau diese Fälle sind oft die aufschlussreichsten fürs Coaching-Gespräch: nicht wissen, dass man es nicht weiß.

Das Lesen der Smileys aus dem Scan ist spürbar unsicherer als das Lesen der Antworten selbst (viele Kinder markieren zwei Smileys überlappend) – vor einer wichtigen Verwendung gegen die Originalbögen prüfen. Ohne `selbsteinschaetzung`-Feld läuft der Bericht wie bisher, ganz ohne diesen Abschnitt.

## Ablauf

1. **Aufgabenblatt austeilen** (Teil 1 zuerst, Teil 2 im zweiten Block – egal ob am selben oder an einem anderen Tag), Rechenwege gehen ins Heft oder auf Schmierpapier, nicht aufs Blatt.
2. **Antwortbogen separat austeilen**, jeweils den passenden Teil: [[Antwortbogen Grundlagen Klasse 5-6 Teil 1]] und [[Antwortbogen Grundlagen Klasse 5-6 Teil 2]] als getrennte Bögen – auch wenn beide Blöcke am selben Tag laufen. **Bewusst zwei Bögen, nicht einer**, der zwischendurch eingesammelt und wieder ausgeteilt wird: Sobald ein Schüler seinen eigenen Bogen zwischen den Blöcken noch einmal in der Hand hat (z. B. nach Absprache mit Mitschülern), lässt sich eine Antwort unbemerkt durchstreichen und ersetzen. Zwei getrennte Bögen schließen das aus, auch wenn es etwas mehr Papier ist.

   Oben trägt jeder Schüler nur seine zugeteilte Nummer ein, keinen Namen. Nur Endergebnisse in die Kästchen, ein Kästchen pro Teilaufgabe. Leer bleiben ist erlaubt und ist selbst schon eine Information. Die Nummer eines Schülers bleibt über beide Teile gleich.
3. **Nur die Antwortbögen einsammeln und scannen** (Foto oder Scanner, eine Datei pro Bogen oder ein Sammel-PDF). Die Aufgabenblätter bleiben bei den Schülern oder im Klassensatz, sie werden nicht digitalisiert.
4. **Scans in einer Claude-Code-Session zeigen** (z. B. hier im Vault-Ordner öffnen lassen). Ich lese die Antworten aus den Bildern und trage sie in eine Ergebnisdatei ein – reine Zahlen und Nummern, siehe Format unten. Bei der neuen 7. füllt Tag 1 die Blöcke A und B, Tag 2 ergänzt C und D in derselben Datei, pro Nummer.
5. **Auswertung erzeugen**, erst wenn beide Teile eingetragen sind:
   ```bash
   python3 .scripts/grundlagen_check_bericht.py <ergebnisse.json> <ausgabe-ordner>
   ```
   Erzeugt eine HTML-Seite mit einer Klassenübersicht (schwächster Themenblock zuerst) und einer Karte pro Nummer, druckbar, mit den 1–2 Themenblöcken, die sich fürs Coaching-Gespräch anbieten. Fehlt ein Teil noch, zeigt der Bericht die vorhandenen Blöcke bereits an und die fehlenden als „nicht bearbeitet" – kann also auch zwischendurch schon laufen, wenn ein erster Blick gewünscht ist.
6. **Karten ausdrucken und den Nummern per eigener Liste die Namen zuordnen** – dieser Schritt passiert nur bei Oskar, nie in einer Datei, die hier liegt.

## Format der Ergebnisdatei

```json
{
  "test": "5-6",
  "ergebnisse": {
    "07": {"A1": {"a": "8292", "b": "3146", "c": "13104", "d": "117"}, "A4": {"a": "1,2,3,4,6,8,12,24", ...}, ...},
    "12": {...}
  },
  "selbsteinschaetzung": {
    "07": {"A1": "sicher", "A2": "unsicher", "A4": "ging_so", ...},
    "12": {...}
  }
}
```
`test` ist `"5-6"` oder `"6-9"`. Die Aufgaben- und Teilaufgaben-Schlüssel (z. B. `"A1"` → `"a"`) müssen zum jeweiligen Lösungsschlüssel in `.scripts/grundlagen_check_schluessel.py` passen. `selbsteinschaetzung` ist optional und pro Aufgabe (nicht pro Teilaufgabe), Werte `sicher` / `ging_so` / `unsicher`. Ein Beispiel mit erfundenen Nummern liegt in [[Klasse 5-6/Grundlagen-Check Beispiel/beispiel_ergebnisse_5-6.json|beispiel_ergebnisse_5-6.json]], die dazugehörige erzeugte Auswertung in [[Klasse 5-6/Grundlagen-Check Beispiel/Rückmeldungen Grundlagen Klasse 5-6.html|Rückmeldungen Grundlagen Klasse 5-6.html]]. Ein echter Lauf mit Selbsteinschätzung liegt in [[7c 2026-27/README|7c 2026-27]].

## Grenzen der automatischen Prüfung

- **Zahlen, Brüche, Dezimalzahlen, Größen, Wörter (z. B. „spitz")** werden zuverlässig erkannt, auch bei leicht abweichender Schreibweise (Komma/Punkt, „1 1/4" vs. „5/4", mit oder ohne Einheit).
- **Terme** (Klasse-6–9-Test, Block C1/C2, z. B. „4a(a−3)") werden nur als exakter Text verglichen. Eine andere, aber gleichwertige Umformung wird nicht erkannt und zählt als „falsch". Bei diesen wenigen Aufgaben lohnt sich ein kurzer manueller Blick.
- **Leer** zählt nicht als falsch, sondern als eigener Zustand „nicht bearbeitet" und fließt nicht in die Prozentzahl ein.

## Für neue Themen im Schuljahr wiederverwenden

Dasselbe Muster – Aufgabenblatt, separater Antwortbogen mit Nummer statt Name, Scan, Auswertung ohne Note – funktioniert für jeden Zwischencheck. Neu bauen müssen sich dann: das Aufgabenblatt, der passende Antwortbogen und ein neuer Eintrag in `.scripts/grundlagen_check_schluessel.py` mit dem Lösungsschlüssel des neuen Themas. `grundlagen_check_bericht.py` bleibt unverändert.

## Verlauf übers Jahr

Ziel: bei den Diagnosegesprächen im Januar für jede Nummer sehen, wie sich das Ergebnis über die Diagnosetests des Jahres entwickelt hat – egal wie viele es am Ende werden (optimistisch geplant: sechs) und egal ob sie dasselbe Thema oder verschiedene Themen abdecken.

`.scripts/grundlagen_check_verlauf.py` führt dafür pro Klasse einen eigenen Speicher `verlauf.json`, der mit jedem Testlauf wächst:

```bash
# nach jedem Testlauf, nachdem grundlagen_check_bericht.py gelaufen ist:
python3 .scripts/grundlagen_check_verlauf.py eintragen <ergebnisse.json> <verlauf.json> "<Test-Label>" <YYYY-MM-DD>

# Übersicht erzeugen (ein Diagramm pro Nummer):
python3 .scripts/grundlagen_check_verlauf.py bauen <verlauf.json> <ausgabe-ordner>
```

Jeder Testlauf liefert pro Nummer nur *eine* Gesamt-Prozentzahl (über alle in diesem Testlauf ausgewerteten Aufgaben), nicht die Themenblöcke einzeln – so bleiben unterschiedliche Testläufe zu unterschiedlichen Themen in derselben Zeitreihe vergleichbar. Bei nur einem Testlauf zeigt die Übersicht einen einzelnen Punkt statt einer Linie, mit dem Hinweis „weitere Punkte folgen mit dem nächsten Test" – eine Linie durch einen einzigen Punkt würde eine Entwicklung vortäuschen, die es noch nicht gibt. Ab dem zweiten Testlauf wird daraus eine echte Linie.

Beispiel für 7c: [[7c 2026-27/README|7c 2026-27]], `verlauf.json` und `Verlauf.html` dort.
