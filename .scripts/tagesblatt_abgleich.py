#!/usr/bin/env python3
"""Abgleich Tagesblatt -> Apple Erinnerungen und Kalender (Werkzeug für den Foto-Abgleich).

Aufruf (Python 3.12 oder System-python3, nur Standardbibliothek):
  tagesblatt_abgleich.py liste
      offene Erinnerungen der Liste "Schule" mit Fälligkeit
  tagesblatt_abgleich.py haken "Textteil" [--dry]
      hakt die offene Erinnerung ab, deren Name den Textteil enthält (genau ein Treffer nötig)
  tagesblatt_abgleich.py neu "Text" [--faellig JJJJ-MM-TT] [--dry]
      legt eine Erinnerung in "Schule" an
  tagesblatt_abgleich.py termin "Titel" --start "JJJJ-MM-TT HH:MM" [--ende "HH:MM"] [--kalender Arbeit] [--dry]
      legt einen Kalendertermin an (ohne --start-Uhrzeit: ganztägig, Format "JJJJ-MM-TT")
  tagesblatt_abgleich.py verschieben "Textteil" --auf JJJJ-MM-TT [--dry]
      setzt das Fälligkeitsdatum einer offenen Erinnerung neu

Es wird nie gelöscht. --dry zeigt nur, was passieren würde.
"""
import argparse
import subprocess
import sys
from datetime import datetime

LISTE = "Schule"
KALENDER = {"Arbeit", "Schule", "Jahresterminplanung / DieWo"}


def osa(script, *args):
    r = subprocess.run(["osascript", "-e", script, *args], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        sys.exit("AppleScript-Fehler: " + r.stderr.strip()[:300])
    return r.stdout.strip()


LISTE_SCRIPT = '''
on run argv
  set out to ""
  tell application "Reminders"
    tell list (item 1 of argv)
      repeat with r in (reminders whose completed is false)
        set dd to due date of r
        set d to ""
        if dd is not missing value then
          set d to (year of dd as string) & "-" & text -2 thru -1 of ("0" & ((month of dd) as integer)) & "-" & text -2 thru -1 of ("0" & (day of dd))
        end if
        set out to out & d & tab & (name of r) & linefeed
      end repeat
    end tell
  end tell
  return out
end run
'''

HAKEN_SCRIPT = '''
on run argv
  tell application "Reminders"
    set hits to (reminders of list (item 1 of argv) whose name is (item 2 of argv) and completed is false)
    if (count of hits) is 0 then return "nicht gefunden"
    set completed of item 1 of hits to true
    return "ok"
  end tell
end run
'''

NEU_SCRIPT = '''
on run argv
  tell application "Reminders"
    tell list (item 1 of argv)
      if (item 3 of argv) is "" then
        make new reminder with properties {name:(item 2 of argv)}
      else
        set d to current date
        set year of d to (item 3 of argv as integer)
        set month of d to (item 4 of argv as integer)
        set day of d to (item 5 of argv as integer)
        set time of d to 8 * hours
        make new reminder with properties {name:(item 2 of argv), due date:d}
      end if
    end tell
    return "ok"
  end tell
end run
'''

VERSCHIEBEN_SCRIPT = '''
on run argv
  tell application "Reminders"
    set hits to (reminders of list (item 1 of argv) whose name is (item 2 of argv) and completed is false)
    if (count of hits) is 0 then return "nicht gefunden"
    set d to current date
    set year of d to (item 3 of argv as integer)
    set month of d to (item 4 of argv as integer)
    set day of d to (item 5 of argv as integer)
    set time of d to 8 * hours
    set due date of item 1 of hits to d
    return "ok"
  end tell
end run
'''

TERMIN_SCRIPT = '''
on run argv
  set sy to item 3 of argv as integer
  set sm to item 4 of argv as integer
  set sd to item 5 of argv as integer
  set sh to item 6 of argv as integer
  set smin to item 7 of argv as integer
  set eh to item 8 of argv as integer
  set emin to item 9 of argv as integer
  set allday to (item 10 of argv is "1")
  set d1 to current date
  set year of d1 to sy
  set month of d1 to sm
  set day of d1 to sd
  set time of d1 to (sh * hours + smin * minutes)
  copy d1 to d2
  set time of d2 to (eh * hours + emin * minutes)
  tell application "Calendar"
    tell calendar (item 1 of argv)
      if allday then
        make new event with properties {summary:(item 2 of argv), start date:d1, end date:d1, allday event:true}
      else
        make new event with properties {summary:(item 2 of argv), start date:d1, end date:d2}
      end if
    end tell
    return "ok"
  end tell
end run
'''


def offene():
    out = osa(LISTE_SCRIPT, LISTE)
    res = []
    for line in out.splitlines():
        due, _, name = line.partition("\t")
        if name.strip():
            res.append((due, name.strip()))
    return res


def eindeutig(teil):
    """Genau eine offene Erinnerung, deren Name den Textteil enthält (ohne Groß/Klein)."""
    treffer = [(d, n) for d, n in offene() if teil.lower() in n.lower()]
    if not treffer:
        sys.exit(f"Keine offene Erinnerung mit „{teil}“ in der Liste {LISTE}.")
    if len(treffer) > 1:
        sys.exit("Mehrdeutig, bitte genauer:\n" + "\n".join(f"  {d or 'ohne Datum'}  {n}" for d, n in treffer))
    return treffer[0]


def datum(s):
    return datetime.strptime(s, "%Y-%m-%d")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["liste", "haken", "neu", "termin", "verschieben"])
    ap.add_argument("text", nargs="?")
    ap.add_argument("--faellig")
    ap.add_argument("--start")
    ap.add_argument("--ende")
    ap.add_argument("--auf")
    ap.add_argument("--kalender", default="Arbeit")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    if a.cmd == "liste":
        for d, n in sorted(offene()):
            print(f"{d or 'ohne Datum':<12}{n}")
        return
    if not a.text:
        sys.exit("Text fehlt.")

    if a.cmd == "haken":
        d, n = eindeutig(a.text)
        print(f"{'würde abhaken' if a.dry else 'abgehakt'}: {n}")
        if not a.dry and osa(HAKEN_SCRIPT, LISTE, n) != "ok":
            sys.exit("Abhaken fehlgeschlagen.")
    elif a.cmd == "neu":
        f = datum(a.faellig) if a.faellig else None
        print(f"{'würde anlegen' if a.dry else 'angelegt'}: {a.text}" + (f" (fällig {f.date()})" if f else ""))
        if not a.dry:
            osa(NEU_SCRIPT, LISTE, a.text, *( [str(f.year), str(f.month), str(f.day)] if f else ["", "", ""] ))
    elif a.cmd == "verschieben":
        if not a.auf:
            sys.exit("--auf fehlt.")
        d, n = eindeutig(a.text)
        f = datum(a.auf)
        print(f"{'würde verschieben' if a.dry else 'verschoben'} auf {f.date()}: {n}")
        if not a.dry and osa(VERSCHIEBEN_SCRIPT, LISTE, n, str(f.year), str(f.month), str(f.day)) != "ok":
            sys.exit("Verschieben fehlgeschlagen.")
    elif a.cmd == "termin":
        if a.kalender not in KALENDER:
            sys.exit(f"Kalender muss einer von {sorted(KALENDER)} sein.")
        if not a.start:
            sys.exit("--start fehlt.")
        ganz = len(a.start) == 10
        s = datetime.strptime(a.start, "%Y-%m-%d" if ganz else "%Y-%m-%d %H:%M")
        if ganz:
            eh = em = 0
        elif a.ende:
            eh, em = (int(x) for x in a.ende.split(":"))
        else:
            eh, em = s.hour + 1, s.minute   # ohne Ende: eine Stunde
        print(f"{'würde eintragen' if a.dry else 'eingetragen'} in {a.kalender}: {a.text}, "
              f"{s.date()} {'ganztägig' if ganz else f'{s:%H:%M} bis {eh:02d}:{em:02d}'}")
        if not a.dry and osa(TERMIN_SCRIPT, a.kalender, a.text, str(s.year), str(s.month), str(s.day),
                             str(s.hour), str(s.minute), str(eh), str(em), "1" if ganz else "0") != "ok":
            sys.exit("Eintragen fehlgeschlagen.")


if __name__ == "__main__":
    main()
