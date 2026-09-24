---
tags: [ressource, physik, unterricht, klasse10, kernphysik, interaktiv]
status: aktiv
date: 2026-09-24
---

# Kernphysik Klasse 10: Stunden und Labore

Einzelstunden W01 bis W05 nach dem [[Stoffverteilungsplan Physik Klasse 10 2026-27]], gleicher Aufbau wie die Optik-Stunden in Klasse 7 (Tabs Überblick, Folien, Hintergrund, Arbeitsblätter; Folien im Labor-Stil B).

| Woche | Stunde | Blatt | Labor |
|---|---|---|---|
| W01 | [[Kernphysik – W01 Woraus besteht Materie – Stunde.html\|Woraus besteht Materie?]] | Wiederholung Atombau | Atomlabor |
| W02 | [[Kernphysik – W02 Atombau und Isotope – Stunde.html\|Atombau und Isotope]] | W02 Nuklide und Isotope | Atomlabor |
| W03 | [[Kernphysik – W03 Zaehlrohr und Nullrate – Stunde.html\|Zählrohr und Nullrate]] | W03 Zählrohr und Nullrate (Oskars Lückentext) | Strahlungslabor |
| W04 | [[Kernphysik – W04 Alpha Beta Gamma – Stunde.html\|Alpha, Beta und Gamma]] | W04 Drei Strahlungsarten | Strahlungslabor |
| W05 | [[Kernphysik – W05 Zerfallsgleichungen – Stunde.html\|Zerfallsgleichungen und Durchdringung]] | W05 Durchdringung und Zerfallsgleichungen | Strahlungslabor |

## Labore

- **Atomlabor** (`Atomlabor Atombau und Isotope.html`): Zoom vom Atom zum Kern, Rutherfords Streuversuch, Atom bauen (Z 1 bis 20, mit Stabilität), Isotope H, C, U.
- **Strahlungslabor** (`Strahlungslabor Radioaktivitaet.html`): Nullrate mit zufälligen Messungen, Präparat und Abstand, α-/β-/γ-Zerfall, Zerfallsgleichungen üben, Absorber. Simuliert, ersetzt fehlende Präparate.

## Technik

- Stunden: `baue_stunden_k10.py` (nutzt `../Optik/stunde_vorlage.py`), Folien-Zeichnungen: `kern_zeichnungen.py`, Blätter: `Materialien/baue_blaetter_k10.py`, Labore: `labore-quelle/` + `../Optik/baue_labore.py` (Funktion `baue`).
- Achtung: `Folien bauen.command` in diesem Ordner macht aus *jeder* HTML eine PDF, also auch aus Stunden und Laboren.
- Präparate nur durch die Lehrkraft (RiSU).
