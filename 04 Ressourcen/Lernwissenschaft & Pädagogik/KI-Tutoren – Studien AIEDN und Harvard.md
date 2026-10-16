---
tags: [ressource, lernen, studie, ki]
status: aktiv
date: 2026-10-16
---

# KI-Tutoren: zwei Studien

Beide Studien hat Daniel Jung in seiner Keynote erwähnt ([[Keynote Daniel Jung – KI und Lernen]]). Hier steht, was ich in den Originalen gelesen habe. Zurück zur Karte: [[Lernen]].

Wichtig vorab: Es sind **zwei verschiedene Arten von KI-Lernhilfe**. AIEDN ist eine semantische Suche über Lernvideos. Der Harvard-Tutor ist ein geführter, fragender Tutor. Die Zahlen lassen sich nicht übertragen.

## AIEDN (HdM Stuttgart, 2023)

Quelle: Forschungsbericht "AIEDN – AI Education", Institute for Applied AI der HdM Stuttgart mit thingsTHINKING GmbH und Daniel Jung. Gefördert von Dezember 2022 bis November 2023 über Invest BW II. PDF: https://ai.hdm-stuttgart.de/downloads/research/Forschungsbericht_AIEDN_AI-Education_2023.pdf (lokaler Parse unter `.firecrawl/aiedn-bericht.md`, nicht im Repo).

- **Was getestet wurde:** Ein Assistent, der Fragen in Alltagssprache versteht und zur passenden Stelle in Mathevideos verweist. Kein sokratischer Dialog.
- **Stichprobe:** 275 Schüler an vier Schulen in Baden-Württemberg (zwei Realschulen mit 137, zwei Gymnasien mit 138), als getrennte Experimente. Vorab eine Umfrage mit 1.053 Befragten über Jungs Kanäle (871 vollständig).
- **Vergleich:** Gruppe mit KI-Assistent gegen Kontrollgruppe mit normaler Stichwortsuche, Aufgabenbogen an Tag 1 und Tag 2.
- **Ergebnis laut Bericht:** Beide Gruppen verbesserten sich. Die KI-Gruppe zeigte eine "leichte, aber signifikante" Lernverbesserung, die Kontrollgruppe keine. An den Realschulen erzielte die KI-Gruppe etwas niedrigere Gesamtpunkte als die ohne KI, zeigte aber eine signifikante Verbesserung zwischen den Tagen. Der Bericht deutet das so, dass die Videos für Gymnasien gemacht waren und die Aufgaben zu schwer waren.
- **Limitationen (aus dem Bericht):** Studienumgebung mit Fremdbeobachtung und Unruhe, Realschüler arbeiteten teils einen Großteil der Zeit nicht aktiv, Fachbegriffe passten nicht zum Realschulunterricht, keine Zeitmessung pro Aufgabe, kein Sperren anderer Seiten, Prototyp nur für auditive und visuelle Lerntypen.
- **Einordnung:** Daniel Jung ist Projektpartner und seine Videos sind das Lernmaterial. Kein unabhängiger Befund. Für Realschule ist die wichtigste Lehre: Material und Fachsprache müssen zur Schulart passen.

## Harvard-Tutor (Kestin, Miller und andere, 2025)

Quelle: "AI tutoring outperforms in-class active learning", Scientific Reports, 2025. DOI 10.1038/s41598-025-97652-6, Volltext: https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/

- **Design:** Randomisierter Crossover-Versuch, Harvard-Kurs Physical Sciences 2, Herbst 2023, 194 Studierende. Jeder Studierende lernte ein Thema mit dem KI-Tutor zu Hause und ein anderes im Präsenz-Active-Learning.
- **Ergebnis:** Medianer Post-Test 4,5 gegen 3,5 Punkte. Der mediane Lerngewinn der KI-Gruppe lag laut Studie "über doppelt" so hoch. Effektstärke in der linearen Regression 0,63, mit Quantilregression 0,73 bis 1,3 Standardabweichungen. Mediane Lernzeit 49 Minuten gegen 60 Minuten Präsenz. 83 % fanden die Erklärungen des Tutors gleich gut oder besser als die von Dozenten.
- **Wie der Tutor gebaut war:** System-Prompt für aktives Mitdenken, geringe Überforderung und Wachstumsdenken. Dazu ausführliche Schritt-für-Schritt-Lösungen im Prompt (verringert Fehler). Ein System-Prompt allein reichte nicht, um mehrteilige Aufgaben zu führen. Deshalb führte die Plattform die Studierenden Teil für Teil durch die Aufgabe.
- **Grenzen laut Autoren:** Erstes Kennenlernen des Stoffs, GPT-4, von erfahrenen Lehrenden geschriebene Prompts, Inhalte mit passender Struktur. Nicht belegt für komplexe Synthese und kritisches Denken auf höherem Niveau.
- **Nicht gefunden:** Die "+127 %" aus der Keynote stehen in den von mir gelesenen Abschnitten nicht. Dort steht "über doppelt". Die Prozentzahl bitte nicht weitergeben, solange sie nicht belegt ist.
- **Einordnung:** Studierende in einem Elite-Kurs, ein Fach, ein Zeitraum von zwei Wochen. Für 7. Klasse an der Realschule nicht belegt.

## Was daraus für Oskar folgt

- Sokratisch heißt hier: nicht die Lösung nennen, in kleinen Teilschritten führen, Lösungsweg im Hintergrund haben. Das ist die Grundlage des Skills `lern-tutor`.
- Für die Klasse taugt vorerst die Haltung (erst selbst denken, dann KI fragen), keine Zahl aus diesen Studien.
