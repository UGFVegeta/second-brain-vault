---
tags: [baustein, unterricht, html]
status: aktiv
date: 2026-10-22
---

# Baustein Gruppen-Generator

Standardbaustein für Stunden-HTMLs mit Folien: ein Knopf „Gruppen auslosen (G)“ auf der Folie, auf der die Klasse in Gruppen eingeteilt wird. Gebaut für die Stunde „Kluge Entscheidungen“ (Fr 23.10.2026), Beispiel: `03 Bereiche/Schule & Unterricht/Klassenlehrer 7c/09 Zeitfensterwoche/Fr 23.10. Kluge Entscheidungen – Stunden.html` (Folien 7, 14, 23).

## Was er kann
- Mischt die Klassenliste komplett zufällig (Fisher-Yates mit `crypto.getRandomValues`), verteilt reihum, die Gruppen sind höchstens eine Person unterschiedlich groß.
- Gruppenzahl mit − und + einstellbar (Knopf auf der Folie setzt den Startwert, z. B. `data-grp="5"`).
- Ergebnis wird pro Gruppenzahl gemerkt: Folie 7 und 14 mit 5 Gruppen zeigen dieselben Gruppen, bis man „Neu mischen (N)“ drückt.
- Tasten: G öffnet und schließt, N oder Leertaste mischt neu, Esc schließt.
- Ohne Liste mischt er Nummern 1 bis N.

- Zeigt nur **Vornamen**. Bei doppelten Vornamen kommt der Anfangsbuchstabe des Nachnamens dazu („Anna B.“). Im Feld „Klassenliste“ stellt Oskar ein, ob in der Liste zuerst der Nachname oder der Vorname steht; eine Vorschau zeigt sofort, ob es stimmt.
- Der Knopf steht oben rechts auf der Folie, groß und gefüllt (nicht unten rechts, dort liegt der Folienzähler).

## Datenschutz (wichtig)
Die Klassenliste steht nie in der Datei und nie im Vault. Oskar kopiert die Namensspalte aus `Klassenliste 7C.xlsx` (iCloud, Klassenlehrer) einmal in das Feld „Klassenliste“. Die Zeilen liegen danach nur im `localStorage` seines Browsers (Schlüssel `klasse-namen-v2`, Reihenfolge in `klasse-reihenfolge`), Knopf „Liste löschen“ entfernt sie. Claude liest die Klassenliste dafür nie.

## Einbau in eine neue Stunden-HTML
1. CSS aus `gruppen-baustein.css` in den `<style>`-Block.
2. JS aus `gruppen-baustein.js` in den Script-Block, nach den Bühnen-Variablen (`stage` muss existieren), vor dem Start-Hash.
3. Auf jeder Folie mit Gruppeneinteilung vor `</section>`: `<button class="grpbtn" data-grp="5">Gruppen auslosen (G)</button>`.
4. Im `keydown`-Handler der Folien (vor der Mindmap-Abfrage) den Block `if(grpOpen){...}` und `if(k.toLowerCase()==='g'...)` ergänzen; Vorlage im Beispiel-HTML.
5. Test über `python3 -m http.server`, nicht über `file://` im eingebauten Browser; Testnamen danach aus dem localStorage löschen.

Verwandt: [[Baustein Mindmap (Excalidraw)]], [[Baustein Alles drucken]].
