# -*- coding: utf-8 -*-
"""Sichert den aktuellen Datenstand, damit sich Fehler zurueckholen lassen.

Aufruf:
    py -3 skripte\\stand_sichern.py              sichert den jetzigen Stand
    py -3 skripte\\stand_sichern.py --liste      zeigt alle gesicherten Staende
    py -3 skripte\\stand_sichern.py --zurueck 3  holt Stand Nummer 3 zurueck

Ist git auf dem Rechner vorhanden, wird es benutzt: das Projekt wird zu einem
lokalen Repository und jede Sicherung ist ein Commit. Fehlt git, legt das
Skript stattdessen eine ZIP-Datei unter sicherungen\\ an. Beides erfuellt
denselben Zweck, git kann zusaetzlich zeigen, was sich geaendert hat.

WICHTIG ZUM ZURUECKHOLEN
    Ein alter Stand wird nie ueber die aktuellen Daten geschrieben. Er landet
    in einem neuen Ordner daten_zurueckgeholt_<Zeit>\\. Von dort kann man in
    Ruhe vergleichen und selbst entscheiden, was uebernommen wird.

WICHTIG ZUM AUFBEWAHRUNGSORT
    Beides liegt auf derselben Festplatte wie die Daten. Gegen einen
    Tippfehler hilft das, gegen einen Festplattenausfall nicht. Eine echte
    Sicherung auf ein anderes Medium bleibt noetig.
"""

import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

from gemeinsam import BASIS, DATEN, konsole_utf8

SICHERUNGEN = BASIS / "sicherungen"
DATENDATEIEN = ("konfig.json", "objekte.json", "mietverhaeltnisse.json",
                "darlehen.json", "fristen.json", "zahlungen.json")


# ------------------------------------------------------------------- git

def git_da():
    return shutil.which("git") is not None


def git(*argumente, **kwargs):
    """Fuehrt einen git-Befehl im Projektordner aus."""
    ergebnis = subprocess.run(
        ["git"] + list(argumente),
        cwd=str(BASIS),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    if kwargs.get("pflicht") and ergebnis.returncode != 0:
        raise RuntimeError(ergebnis.stdout.strip())
    return ergebnis.returncode, (ergebnis.stdout or "").strip()


def repo_vorhanden():
    return (BASIS / ".git").exists()


def git_sichern():
    neu = not repo_vorhanden()
    if neu:
        git("init", pflicht=True)
        git("config", "user.name", "Mietverwaltung")
        git("config", "user.email", "mietverwaltung@localhost")
        print("Ein lokales Repository wurde angelegt.")
        print("Es bleibt auf diesem Rechner. Kein GitHub, kein Remote.")
        print("")

    git("add", "-A")
    code, ausgabe = git("status", "--porcelain")
    if not ausgabe:
        print("Es hat sich seit der letzten Sicherung nichts geändert.")
        return 0

    zeit = datetime.now().strftime("%d.%m.%Y %H:%M")
    code, ausgabe = git("commit", "-m", "Stand {}".format(zeit))
    if code != 0:
        print("Die Sicherung hat nicht geklappt:")
        print(ausgabe)
        return 1

    print("Stand gesichert: {}".format(zeit))
    code, anzahl = git("rev-list", "--count", "HEAD")
    if code == 0:
        print("Gesicherte Stände insgesamt: {}".format(anzahl))
    return 0


def git_liste():
    code, ausgabe = git(
        "log", "--pretty=format:%h|%ad|%s", "--date=format:%d.%m.%Y %H:%M"
    )
    if code != 0 or not ausgabe:
        return []
    eintraege = []
    for zeile in ausgabe.splitlines():
        teile = zeile.split("|", 2)
        if len(teile) == 3:
            eintraege.append({"kennung": teile[0], "zeit": teile[1], "text": teile[2]})
    return eintraege


def git_zurueck(kennung, ziel):
    ziel.mkdir(parents=True, exist_ok=True)
    geholt = 0
    for name in DATENDATEIEN:
        code, inhalt = git("show", "{}:daten/{}".format(kennung, name))
        if code != 0:
            continue
        (ziel / name).write_text(inhalt + "\n", encoding="utf-8")
        geholt += 1
    return geholt


# ------------------------------------------------------------------- ZIP

def zip_sichern():
    SICHERUNGEN.mkdir(exist_ok=True)
    zeit = datetime.now()
    ziel = SICHERUNGEN / "daten_{:%Y-%m-%d_%H%M%S}.zip".format(zeit)
    with zipfile.ZipFile(str(ziel), "w", zipfile.ZIP_DEFLATED) as archiv:
        for name in DATENDATEIEN:
            pfad = DATEN / name
            if pfad.exists():
                archiv.write(str(pfad), name)
    print("Stand gesichert: {:%d.%m.%Y %H:%M}".format(zeit))
    print("  {}".format(ziel.name))
    print("")
    print("Hinweis: git ist auf diesem Rechner nicht installiert, deshalb die")
    print("ZIP-Variante. Das reicht zum Zurückholen. Mit git könnte man")
    print("zusätzlich sehen, was sich zwischen zwei Ständen geändert hat.")
    return 0


def zip_liste():
    if not SICHERUNGEN.exists():
        return []
    eintraege = []
    for pfad in sorted(SICHERUNGEN.glob("daten_*.zip"), reverse=True):
        zeit = datetime.fromtimestamp(pfad.stat().st_mtime)
        eintraege.append(
            {
                "kennung": pfad.name,
                "zeit": "{:%d.%m.%Y %H:%M}".format(zeit),
                "text": "{:.0f} KB".format(pfad.stat().st_size / 1024),
            }
        )
    return eintraege


def zip_zurueck(kennung, ziel):
    pfad = SICHERUNGEN / kennung
    if not pfad.exists():
        return 0
    ziel.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(pfad)) as archiv:
        archiv.extractall(str(ziel))
    return len(list(ziel.glob("*.json")))


# ------------------------------------------------------------------ Ablauf

def liste_zeigen(eintraege):
    if not eintraege:
        print("Es gibt noch keine gesicherten Stände.")
        print("Einen anlegen mit: py -3 skripte\\stand_sichern.py")
        return
    print("Gesicherte Stände, der neueste zuerst:")
    print("")
    for nummer, eintrag in enumerate(eintraege, 1):
        print("  {:>2}  {}  {}".format(nummer, eintrag["zeit"], eintrag["text"]))
    print("")
    print("Zurückholen mit: py -3 skripte\\stand_sichern.py --zurueck <Nummer>")


def main():
    konsole_utf8()
    argumente = sys.argv[1:]
    mit_git = git_da()

    if argumente and argumente[0] == "--liste":
        liste_zeigen(git_liste() if mit_git and repo_vorhanden() else zip_liste())
        return 0

    if argumente and argumente[0] == "--zurueck":
        if len(argumente) < 2:
            print("Bitte die Nummer angeben, z. B. --zurueck 3")
            print("Die Nummern zeigt: py -3 skripte\\stand_sichern.py --liste")
            return 1
        eintraege = git_liste() if mit_git and repo_vorhanden() else zip_liste()
        try:
            eintrag = eintraege[int(argumente[1]) - 1]
        except (ValueError, IndexError):
            print("Diese Nummer gibt es nicht.")
            liste_zeigen(eintraege)
            return 1

        ziel = BASIS / "daten_zurueckgeholt_{:%Y-%m-%d_%H%M%S}".format(datetime.now())
        if mit_git and repo_vorhanden():
            anzahl = git_zurueck(eintrag["kennung"], ziel)
        else:
            anzahl = zip_zurueck(eintrag["kennung"], ziel)

        if not anzahl:
            print("Aus diesem Stand ließ sich nichts holen.")
            return 1
        print("Stand vom {} wiederhergestellt, {} Dateien.".format(
            eintrag["zeit"], anzahl))
        print("  {}".format(ziel))
        print("")
        print("Die aktuellen Daten in daten\\ sind unverändert geblieben.")
        print("Claude kann die beiden Stände vergleichen und zeigen, was sich")
        print("unterscheidet. Erst danach entscheiden, was übernommen wird.")
        return 0

    if argumente:
        print("Unbekannte Angabe: {}".format(argumente[0]))
        print(__doc__.split("WICHTIG")[0].strip())
        return 1

    return git_sichern() if mit_git else zip_sichern()


if __name__ == "__main__":
    raise SystemExit(main())
