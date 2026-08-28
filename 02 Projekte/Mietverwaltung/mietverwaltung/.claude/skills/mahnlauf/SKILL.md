---
name: mahnlauf
description: Entwirft Zahlungserinnerungen und Mahnungen für offene Mieten, abgestuft nach Verzugsdauer. Nutze diesen Skill bei „Mahnlauf", „Zahlungserinnerung", „Mahnung schreiben", „wer ist im Rückstand" oder wenn im Dashboard Rückstände stehen.
---

# Zahlungserinnerungen entwerfen

## Eiserne Regel

Du verschickst nichts. Du legst jeden Entwurf vor, der Vermieter liest ihn und
entscheidet. Erst danach wird gesendet, und zwar von ihm.

Der Grund ist nicht Förmlichkeit, sondern Erfahrung: Es gibt immer Fälle, die
in den Daten nicht stehen. Bar bezahlt, Stundung mündlich vereinbart,
Mietminderung wegen eines Mangels, Zahlung vom Konto der Tochter. Eine
automatisch verschickte Mahnung in so einem Fall kostet mehr Vertrauen, als
die Automatik je einspart.

## Ablauf

1. Rückstände ermitteln: `py -3 skripte\rueckstaende.py`. Das listet je
   Mietverhältnis die offenen Monate mit Betrag und Verzugsdauer.
2. Dem Vermieter die Liste zeigen und fragen, ob bei einem der Fälle etwas
   bekannt ist, das nicht in den Daten steht. Diese Frage immer stellen, sie
   fängt die Hälfte der Fehler ab.
3. Für die verbleibenden Fälle je einen Entwurf schreiben.
4. Entwürfe einzeln vorlegen. Nach Freigabe in eine Textdatei unter
   `entwuerfe\` schreiben, damit er sie ins Mailprogramm kopieren kann.

## Stufen

Die Stufen stehen in `daten/konfig.json` unter `mahnstufen` und richten sich
nach den Tagen seit Fälligkeit:

- **bis 7 Tage**: gar nichts. Überweisungen brauchen manchmal ein paar Tage,
  und eine Erinnerung nach drei Tagen wirkt kleinlich.
- **ab 7 Tagen**: freundliche Erinnerung. Möglichkeit einräumen, dass sich die
  Sache überschnitten hat.
- **ab 21 Tagen**: deutliche Zahlungsaufforderung mit konkreter Frist und
  Betrag.
- **ab 45 Tagen**: förmliche Mahnung mit Fristsetzung und dem Hinweis auf die
  weiteren Schritte.

## Ton

Sachlich und knapp. Kein Vorwurf, keine Floskeln, keine Drohkulisse in den
ersten beiden Stufen. Der Mieter soll die Mail lesen, verstehen was fehlt und
überweisen können, ohne sich zu ärgern.

Konkret werden: Objekt, Einheit, Monat, Betrag, Kontoverbindung und Frist
gehören in jede Mail. Ein Satz zum Nachfragen bei Problemen gehört in die
ersten beiden Stufen, das erspart erfahrungsgemäß den dritten Brief.

## Rechtliches

Ab der dritten Stufe wird es ein Thema, bei dem du Grenzen hast. Du kannst
sagen, was üblich ist. Du sollst nicht beurteilen, ob eine fristlose Kündigung
zulässig ist oder wie hoch eine Mietminderung ausfallen darf. Solche Fragen
gehören zum Anwalt oder zum Vermieterverein, und das sagst du auch so.

Beim Wortlaut der dritten Stufe empfiehlt sich ohnehin, dass der Vermieter
sich eine Vorlage seines Vereins holt, statt eine frei formulierte zu nehmen.

## Nach dem Versand

Wenn der Vermieter bestätigt, dass er verschickt hat, vermerke das beim
Mietverhältnis in `daten/mietverhaeltnisse.json`:

```json
"mahnungen": [
  { "monat": "2026-08", "stufe": 1, "datum": "2026-09-12" }
]
```

So weiß der nächste Lauf, dass die erste Stufe schon raus ist, und schlägt
beim nächsten Mal die zweite vor statt derselben Erinnerung.
