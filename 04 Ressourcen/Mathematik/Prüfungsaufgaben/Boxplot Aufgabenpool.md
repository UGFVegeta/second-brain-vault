---
tags: [mathematik, pruefung, boxplot, datenanalyse, statistik, aufgabenpool]
date: 2026-06-25
---

# Boxplot & Datenanalyse – Aufgabenpool mündliche Prüfung

15 Aufgaben rund um Median, Quartile, Spannweite und Boxplots: ablesen, erstellen, zuordnen und vergleichen. Die Boxplot-Diagramme liegen als eigene Bilder im Ordner `Bilder/` (Format `.svg`), Datensätze stehen als Liste oder Tabelle direkt in der Aufgabe. Für eine individuelle Prüfung pro Schüler einfach die gewünschten Aufgaben in eine neue Notiz kopieren – wie beim [[Trigonometrie Prüfungspool]], [[Stochastik Aufgabenpool]] und [[Quadratische Funktionen Aufgabenpool]].

Eine interaktive Variante zum Auswählen und Drucken (mit leerer Skala bei den Zeichenaufgaben) liegt als `Boxplot Aufgabenpool.html` daneben.

**Quartile** werden nach der in der Abschlussprüfung BW üblichen Rang-Methode bestimmt: Rangplatz = n · ¼ (unteres Quartil) bzw. n · ¾ (oberes Quartil). Ist das Ergebnis keine ganze Zahl, wird aufgerundet und der Wert an diesem Rang genommen; ist es eine ganze Zahl k, nimmt man das Mittel aus Rang k und k+1.

Die Lösungen stehen eingeklappt in der jeweiligen Aufgabe (nur für dich).

---

## Aufgabe 1
*Schwierigkeit: ★★☆*
![[Box-Aufgabe-01.svg]]
Lies aus dem Boxplot ab: Minimum, unteres Quartil, Median, oberes Quartil und Maximum. Bestimme außerdem Spannweite und Quartilsabstand.
> [!tip]- Lösung
> Min = 10, Q1 = 35, Median = 50, Q3 = 70, Max = 95.
> Spannweite = 95 − 10 = **85**. Quartilsabstand = 70 − 35 = **35**. Die mittleren 50 % liegen zwischen 35 und 70 Punkten.

## Aufgabe 2
*Schwierigkeit: ★★☆*
![[Box-Aufgabe-02.svg]]
Lies die Fünf-Punkte-Zusammenfassung ab. Wie groß ist die Spannweite? Wie viel Prozent der Werte liegen über 45 min?
> [!tip]- Lösung
> Min = 5, Q1 = 20, Median = 30, Q3 = 45, Max = 55. Spannweite = **50 min**. Über dem oberen Quartil (45) liegen **25 %** der Werte.

## Aufgabe 3
*Schwierigkeit: ★☆☆*
Gegeben sind die sortierten Werte: **3, 5, 6, 6, 8, 9, 10, 12, 12, 14, 15** (n = 11). Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.
![[Box-03-axis.svg]]
> [!tip]- Lösung
> Median = 9 (Rang 6). Unteres Quartil: n·¼ = 2,75 → Rang 3 → q<sub>u</sub> = 6. Oberes Quartil: n·¾ = 8,25 → Rang 9 → q<sub>o</sub> = 12. Min = 3, Max = 15.
> ![[Box-03-loesung.svg]]

## Aufgabe 4
*Schwierigkeit: ★★☆*
Gegeben sind die sortierten Werte: **2, 4, 5, 7, 8, 8, 10, 13** (n = 8). Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.
![[Box-04-axis.svg]]
> [!tip]- Lösung
> Median = (7 + 8)/2 = 7,5. Unteres Quartil: n·¼ = 2 (ganzzahlig) → Mittel aus Rang 2 und 3 → q<sub>u</sub> = (4 + 5)/2 = 4,5. Oberes Quartil: n·¾ = 6 → Mittel aus Rang 6 und 7 → q<sub>o</sub> = (8 + 10)/2 = 9. Min = 2, Max = 13.
> ![[Box-04-loesung.svg]]

## Aufgabe 5
*Schwierigkeit: ★★★*
Die Strichliste zeigt das Taschengeld (in €) von 22 Schülern. Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.

| Euro | 0 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 50 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|
| Anzahl | 2 | 2 | 2 | 3 | 2 | 5 | 1 | 3 | 1 | 1 |

![[Box-05-axis.svg]]
> [!tip]- Lösung
> n = 22. Median = (25 + 30)/2 = **27,5 €**. Q1 = 15 €, Q3 = 35 €. Min = 0 €, Max = 60 €. Spannweite = 60 €, Quartilsabstand = 20 €.
> ![[Box-05-loesung.svg]]

## Aufgabe 6
*Schwierigkeit: ★★★*
Drei Gruppen wurden befragt (Werte in min). Zu welchen Gruppen gehören die Boxplots (1) und (2)? Begründe.

- **Gruppe A:** 0, 0, 0, 30, 45, 60, 60, 150, 150, 150, 165, 180, 180
- **Gruppe B:** 0, 30, 45, 45, 60, 60, 60, 75, 75, 75, 90, 105, 120, 135, 150, 150, 180
- **Gruppe C:** 0, 30, 45, 75, 90, 90, 90, 90, 120, 150, 150, 180, 180

![[Box-06.svg]]
> [!tip]- Lösung
> Mediane: A = 60, B = 75, C = 90.
> **(1)** hat Median 75 → **Gruppe B**. Kontrolle über die Quartile: n = 17, also n·¼ = 4,25 → Rang 5 → q<sub>u</sub> = 60 und n·¾ = 12,75 → Rang 13 → q<sub>o</sub> = 120. **(2)** hat Median 90 → **Gruppe C**: n = 13, also n·¼ = 3,25 → Rang 4 → q<sub>u</sub> = 75 und n·¾ = 9,75 → Rang 10 → q<sub>o</sub> = 150. Übrig bleibt Gruppe A.

## Aufgabe 7
*Schwierigkeit: ★★★*
Die Boxplots (1) und (2) gehören zu Gruppe B und C. Erstelle den fehlenden Boxplot für **Gruppe A**: 0, 0, 0, 30, 45, 60, 60, 150, 150, 150, 165, 180, 180 (n = 13).
![[Box-07-given.svg]]
> [!tip]- Lösung
> Median = 60 (7. Wert). Unteres Quartil: n·¼ = 3,25 → Rang 4 → q<sub>u</sub> = 30. Oberes Quartil: n·¾ = 9,75 → Rang 10 → q<sub>o</sub> = 150. Min = 0, Max = 180.
> ![[Box-07-loesung.svg]]

## Aufgabe 8
*Schwierigkeit: ★★☆*
Vergleiche die beiden Boxplots (B) und (C) (Werte in kg). Worin gleichen, worin unterscheiden sie sich?
![[Box-08.svg]]
> [!tip]- Lösung
> Gleich: Min = 20, Median = 90, Max = 175 (Spannweite je 155). Unterschied: (B) hat Q3 = 120, (C) nur Q3 = 110 → der Quartilsabstand ist bei (B) größer (80 gegenüber 70). Die mittleren 50 % streuen bei (B) etwas stärker.

## Aufgabe 9
*Schwierigkeit: ★★☆*
Beschreibe die Verteilung. Ist sie symmetrisch oder schief? Was bedeutet der lange rechte Whisker?
![[Box-09.svg]]
> [!tip]- Lösung
> Min = 0, Q1 = 10, Median = 15, Q3 = 40, Max = 60. Die Verteilung ist **rechtsschief**: Die Hälfte der Werte liegt ≤ 15, aber die oberen 25 % streuen sehr weit (40–60). Einzelne große Werte ziehen den rechten Whisker in die Länge.

## Aufgabe 10
*Schwierigkeit: ★★☆*
Gegeben sind die sortierten Werte: **4, 6, 7, 7, 9, 11, 12, 12, 15** (n = 9). Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.
![[Box-10-axis.svg]]
> [!tip]- Lösung
> Median = 9 (Rang 5). Unteres Quartil: n·¼ = 2,25 → Rang 3 → q<sub>u</sub> = 7. Oberes Quartil: n·¾ = 6,75 → Rang 7 → q<sub>o</sub> = 12. Min = 4, Max = 15.
> ![[Box-10-loesung.svg]]

## Aufgabe 11
*Schwierigkeit: ★☆☆*
Bestimme aus dem Boxplot den Median, die Spannweite und den Quartilsabstand.
![[Box-11.svg]]
> [!tip]- Lösung
> Median = 40. Min = 12, Max = 80 → Spannweite = **68**. Q1 = 25, Q3 = 55 → Quartilsabstand = **30**.

## Aufgabe 12
*Schwierigkeit: ★★★*
Eine App wurde von 28 Personen genutzt. Die Tabelle zeigt die Nutzungsdauer (in Stunden). Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.

| Dauer (h) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| Anzahl | 2 | 1 | 2 | 2 | 6 | 5 | 6 | 2 | 1 | 1 |

![[Box-12-axis.svg]]
> [!tip]- Lösung
> n = 28. Median = (6 + 6)/2 = **6 h**. Q1 = 4,5 h, Q3 = 7 h. Min = 1 h, Max = 11 h. Spannweite = 10 h, Quartilsabstand = 2,5 h.
> ![[Box-12-loesung.svg]]

## Aufgabe 13
*Schwierigkeit: ★★☆*
Zwei Klassen A und B schreiben dieselbe Arbeit (Punkte). Vergleiche Median und Streuung.
![[Box-13.svg]]
> [!tip]- Lösung
> Beide haben Median = 7. Klasse A: Min 3 / Max 10 → Spannweite 7, Quartilsabstand 3. Klasse B: Min 1 / Max 13 → Spannweite 12, Quartilsabstand 7. → Gleicher Median, aber Klasse B streut deutlich stärker (heterogener).

## Aufgabe 14
*Schwierigkeit: ★★☆*
Der Boxplot zeigt die Wartezeiten an einer Kasse (in min). Wie lange warten die meisten Kunden? Was sagt der lange rechte Whisker aus?
![[Box-14.svg]]
> [!tip]- Lösung
> Min = 1, Q1 = 3, Median = 6, Q3 = 12, Max = 30. Die Hälfte wartet höchstens 6 min, 75 % höchstens 12 min. Einzelne warten aber bis 30 min → rechtsschiefe Verteilung.

## Aufgabe 15
*Schwierigkeit: ★★☆*
Gegeben sind die sortierten Werte: **5, 5, 8, 10, 10, 12, 14, 15, 15, 18, 20, 22** (n = 12). Bestimme die Fünf-Punkte-Zusammenfassung und zeichne den Boxplot.
![[Box-15-axis.svg]]
> [!tip]- Lösung
> Median = (12 + 14)/2 = 13. Unteres Quartil: n·¼ = 3 (ganzzahlig) → Mittel aus Rang 3 und 4 → q<sub>u</sub> = (8 + 10)/2 = 9. Oberes Quartil: n·¾ = 9 → Mittel aus Rang 9 und 10 → q<sub>o</sub> = (15 + 18)/2 = 16,5. Min = 5, Max = 22.
> ![[Box-15-loesung.svg]]
