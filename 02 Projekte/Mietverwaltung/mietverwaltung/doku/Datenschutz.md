# Datenschutz

In dieser Verwaltung stehen echte personenbezogene Daten von Mietern: Namen,
Anschriften, Kontoverbindungen, Zahlungsverhalten, bei Rückständen auch
Angaben, die Rückschlüsse auf die wirtschaftliche Lage zulassen. Das ist kein
Nebenaspekt, sondern der Grund, warum diese Verwaltung lokal läuft und nicht
in einer Cloud.

Als Vermieter ist man für diese Daten verantwortlich. Die folgenden Punkte
sind kein Rechtsrat, sondern die praktischen Konsequenzen daraus.

## Was hier gilt

**Die Daten bleiben auf diesem Rechner.** Es gibt keinen Server, keine
Synchronisierung und keinen Anbieter dazwischen. Der Ordner `daten\` ist die
einzige Stelle, an der diese Informationen liegen.

**Nicht in eine öffentliche Cloud.** Ein Ordner in einem geteilten Laufwerk
oder in einem öffentlichen Git-Repository ist der häufigste Weg, auf dem
solche Daten abhandenkommen. Die mitgelieferte `.gitignore` schließt `daten\`,
`belege\`, `kontoauszuege\` und `entwuerfe\` deshalb aus, falls das Projekt
jemals in ein Repository wandert.

**Sicherung trotzdem nötig.** Es gibt keine zweite Kopie. Eine verschlüsselte
Sicherung auf eine externe Festplatte ist der richtige Weg, nicht der Verzicht
auf Sicherung.

**Zugangsdaten getrennt.** Die Bankverbindungsdaten liegen unter
`%USERPROFILE%\.mietverwaltung\`, also außerhalb des Projektordners. PIN und
TAN werden nirgends gespeichert.

## Was Claude damit macht

Claude liest diese Daten, um damit zu rechnen, und schreibt sie zurück. Was
Claude nicht tut:

- Mieterdaten in Texte aufnehmen, die den Rechner verlassen
- Daten an Dienste hochladen oder in Suchanfragen stellen
- Mails oder Nachrichten mit diesen Daten selbstständig verschicken

Wenn ein Beispiel gebraucht wird, nimmt Claude die erfundenen Namen aus
`daten\beispiel\`.

Zu bedenken bleibt: Das Gespräch mit Claude läuft über die Server von
Anthropic. Was man Claude über einen Mieter erzählt, ist damit nicht mehr rein
lokal. Für die tägliche Arbeit ist das in Ordnung und auch der Sinn der Sache.
Für Angaben, die dort nichts verloren haben, gilt dasselbe wie überall: nicht
hineinschreiben. Das betrifft vor allem Gesundheitsangaben, Angaben über
Familienverhältnisse oder Vermutungen über die finanzielle Lage eines Mieters.
Für die Mietverwaltung braucht es nichts davon.

## Aufbewahrung

Mietunterlagen und Belege werden steuerlich mehrere Jahre aufbewahrt, danach
gibt es keinen Grund mehr, die Daten zu behalten. Nach dem Auszug eines
Mieters und dem Ablauf der Aufbewahrungsfristen kann das Mietverhältnis
gelöscht werden. Der Eintrag in `mietverhaeltnisse.json` lässt sich einfach
entfernen; die zugehörigen Zahlungen verlieren dann ihre Zuordnung, bleiben
aber als anonyme Buchungen erhalten.

Ein Mieter hat übrigens das Recht, Auskunft über die zu ihm gespeicherten
Daten zu verlangen. Weil hier alles in lesbaren Textdateien steht, ist diese
Auskunft schnell erstellt: Claude kann alle Einträge zu einer Person
zusammenstellen.
