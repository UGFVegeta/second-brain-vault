---
name: unterlagen-uebernehmen
description: Übernimmt vorhandene Excel-Listen, Mietverträge und PDFs direkt in die Stammdaten, statt alles abzufragen. Nutze diesen Skill bei „ich habe das schon in Excel", „hier sind meine Mietverträge", „Unterlagen einlesen", „aus meiner Liste übernehmen", „ich hab da eine Tabelle" oder immer zu Beginn der Ersterfassung, bevor du anfängst Fragen zu stellen.
---

# Vorhandene Unterlagen übernehmen

Die meisten Vermieter haben ihre Wohnungen längst irgendwo stehen: in einer
Excel-Liste, in den Mietverträgen, in einer Aufstellung fürs Finanzamt. Diese
Angaben abzufragen wäre verlorene Zeit. Lies sie stattdessen.

## Immer zuerst fragen

Bevor du mit dem Abfragen beginnst, stell diese eine Frage:

> Haben Sie Ihre Wohnungen schon irgendwo erfasst? Eine Excel-Liste, eine
> Aufstellung für den Steuerberater, die Mietverträge als PDF? Dann legen Sie
> das in den Ordner `unterlagen` und ich lese es aus, statt Sie alles
> vorlesen zu lassen.

Das ist der Unterschied zwischen zwei Stunden Diktat und zwanzig Minuten
Durchsehen.

## Vorgehen

**1. Bestand aufnehmen**

```
py -3 skripte\unterlagen_lesen.py
```

Das gibt alle Excel-Mappen als Text aus und listet auf, welche Dateien du
ohnehin direkt lesen kannst. PDFs, CSV und Word liest du selbst mit dem
Read-Werkzeug, dafür braucht es kein Skript.

**2. Struktur verstehen, bevor du schreibst**

Sieh dir die Tabelle an und ordne zu, welche Spalte was bedeutet. Typische
Bezeichnungen und wohin sie gehören:

| In seiner Tabelle steht oft | gehört nach |
|---|---|
| Objekt, Haus, Immobilie, Adresse, Straße | `objekte[].bezeichnung` |
| Wohnung, Einheit, WE, Whg, Lage, Stockwerk | `einheiten[].bezeichnung` |
| qm, m², Wohnfläche, Fläche | `einheiten[].wohnflaeche` |
| Mieter, Name, Mietpartei | `mieter_name` |
| Kaltmiete, Grundmiete, Nettomiete, Miete netto | `kaltmiete` |
| NK, Nebenkosten, BK, Betriebskosten, Vorauszahlung | `nebenkosten_voraus` |
| Warmmiete, Gesamtmiete, Bruttomiete | **Achtung**, siehe unten |
| Mietbeginn, seit, Einzug, Vertragsbeginn | `beginn` |
| Kaution | `kaution` |
| IBAN, Konto, Bankverbindung | `iban_mieter` |

**3. Vorschlag zeigen, nicht sofort schreiben**

Fass zusammen, was du verstanden hast, kurz und in Prosa. Zum Beispiel: „Ich
lese vier Einheiten in zwei Objekten, Kaltmiete und Nebenkosten sind getrennt
ausgewiesen, IBANs sind bei allen dabei, das Mietende fehlt überall, das
deute ich als unbefristet. Soll ich das so übernehmen?"

Erst nach dem Ja schreiben.

**4. Schreiben und prüfen**

In die Dateien unter `daten\` schreiben, Struktur genau wie in
`daten\beispiel\`. Danach immer:

```
py -3 skripte\pruefen.py
```

**5. Nur die Lücken abfragen**

Jetzt kommt das Gespräch, aber viel kürzer: nur das, was in den Unterlagen
nicht stand. Sammle die Lücken und frag sie in einem Rutsch ab, nicht
verstreut.

## Sitzung planen, damit nichts hängen bleibt

Nicht alles kostet gleich viel. Der Unterschied ist groß genug, dass er das
Vorgehen bestimmt:

- **Eine Excel-Liste mit 30 Einheiten sind rund 1.500 Tokens.** Also praktisch
  nichts. Die Tabelle wird komplett auf einmal gelesen, nicht häppchenweise.
  Sie aufzuteilen bringt keinen Vorteil und macht nur Fehler wahrscheinlicher.
- **Ein Mietvertrag als PDF mit zehn Seiten liegt grob bei 10.000 bis 16.000
  Tokens.** Dreißig Verträge am Stück gelesen sprengen jede Sitzung. Deshalb:
  **lies niemals alle Verträge vorab.** Verträge werden nur dann geöffnet,
  wenn eine bestimmte Angabe fehlt, und dann genau einer. Die fehlenden Felder
  sofort nach `daten\` schreiben, dann zum nächsten.

### Reihenfolge

**Erst ein Objekt vollständig durch die ganze Kette**, bevor der Rest kommt.
Also: ein Objekt erfassen, einen echten Kontoauszug einlesen, sehen ob die
Zahlungen richtig zugeordnet werden, Dashboard ansehen. Das dauert eine
Viertelstunde und zeigt, ob die Zuordnung mit seinen echten Verwendungszwecken
zurechtkommt.

Der Grund ist nicht der Kontext, sondern die Erfahrung: Wenn an der Zuordnung
etwas klemmt, will man das nach einem Objekt wissen und nicht nach dreißig.

**Danach die restliche Liste in einem Rutsch.** Die kostet kaum etwas, und in
einem Durchgang bleiben die Bezeichnungen einheitlich.

### Nach jedem Objekt sofort speichern

Schreib jedes fertige Objekt gleich in die Datei, nicht erst am Ende alle
zusammen. Das ist der einzige Schutz davor, dass eine abgebrochene Sitzung
Arbeit vernichtet.

### Wiedereinstieg

Wenn die Sitzung zu lang wird oder abbricht, ist das unkritisch. Neue Sitzung
öffnen und sagen: „Weiter erfassen." Zum Stand:

```
py -3 skripte\pruefen.py
```

Das zeigt, wie viele Objekte, Einheiten und Mietverhältnisse schon stehen und
was noch fehlt. Von dort aus geht es weiter. Sag ihm das ruhig vorher, dann
muss er sich während der Erfassung keine Gedanken darüber machen.

## Worauf du achten musst

**Warmmiete allein reicht nicht.** Steht in der Tabelle nur eine
Gesamtmiete, dann rechne sie nicht auf gut Glück auseinander. Trag die Summe
als `kaltmiete` ein, setz `nebenkosten_voraus` auf `null` und frag nach. Für
die Zuordnung der Zahlungen stimmt die Summe, für eine spätere
Nebenkostenabrechnung braucht es die echte Aufteilung.

**Summenzeilen sind keine Wohnungen.** Am Ende von Tabellen stehen oft
Zwischensummen. Die gehören nicht in die Stammdaten.

**Ein Objekt über mehrere Zeilen.** Meist steht die Adresse in jeder Zeile
neu, gemeint ist aber ein Haus mit mehreren Einheiten. Fasse gleiche Adressen
zu einem Objekt mit mehreren Einheiten zusammen.

**Leere Zellen sind keine Nullen.** Eine leere Spalte Kaution bedeutet, dass
er sie nicht eingetragen hat, nicht dass keine Kaution vereinbart ist. `null`
setzen und nachfragen.

**Alte Stände.** Tabellen sind oft ein Jahr alt. Frag nach, ob seit der
letzten Pflege Mieterhöhungen oder Wechsel dazugekommen sind. Diese eine
Frage verhindert die Hälfte aller falschen Sollmieten.

**Eingescannte Verträge.** Ein PDF ohne Textebene ist ein Bild, daraus
bekommst du nichts. Sag klar, welche Dateien betroffen sind, und frag die
Angaben ab, statt zu raten.

**Widersprüche stehen lassen.** Wenn die Excel-Liste 680 Euro sagt und der
Mietvertrag 650, dann rate nicht. Zeig ihm beide Stellen und lass ihn
entscheiden. Der Vertrag ist meist älter, die Liste meist gepflegter, aber
das ist Vermutung, keine Regel.

## Datenschutz

Die Unterlagen enthalten echte Mieterdaten. Sie bleiben in `unterlagen\` auf
diesem Rechner. Nichts davon wird hochgeladen oder weitergegeben. Nach der
Übernahme kann der Ordner geleert werden, die Angaben stehen dann in `daten\`.
