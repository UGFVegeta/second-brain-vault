#!/usr/bin/env python3
"""Mailtext (Datei oder stdin, normale Leerzeilen) für den Mail-Editor aufbereiten
und in die Zwischenablage legen: Leerzeilen als geschütztes Leerzeichen, UTF-8.
Bricht ab bei Aufzählungszeichen, "Betreff:" im Text oder kaputten Umlauten."""
import subprocess, sys, re

args = [a for a in sys.argv[1:] if not a.startswith("--")]
modus = "html" if "--html" in sys.argv else "plain"  # plain = Klartext-Modus im Editor (Standard), html = Modus "Formatiert"
text = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
text = text.strip("\n")
fehler = []
if re.search(r"^\s*([-*•]|\d+\.)\s", text, re.M): fehler.append("Aufzählungszeichen im Text")
if re.search(r"^Betreff:", text, re.M | re.I): fehler.append("'Betreff:' im Text")
if "Ã" in text or "�" in text: fehler.append("kaputte Umlaute")
if "—" in text or "–" in text.replace("14.–", ""): fehler.append("Gedankenstrich")
if fehler:
    sys.exit("ABBRUCH: " + ", ".join(fehler))

import html as _h
out = "\n".join("\u00a0" if z.strip() == "" else z for z in text.split("\n"))
bloecke = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
html = '<meta charset="utf-8"><div style="font-family:Helvetica,Arial,sans-serif;font-size:14px">' + "".join(
    "<p style=\"margin:0 0 1em 0\">" + "<br>".join(_h.escape(z) for z in b.split("\n")) + "</p>" for b in bloecke) + "</div>"

# beide Formate gleichzeitig ablegen: HTML (für Formatiert-Modus) + Klartext mit NBSP-Leerzeilen (für Klartext-Modus)
jxa = """ObjC.import('AppKit'); ObjC.import('Foundation');
var env = $.NSProcessInfo.processInfo.environment;
var pb = $.NSPasteboard.generalPasteboard; pb.clearContents;
if (env.objectForKey('MC_MODE').js == 'html') { pb.setStringForType($(env.objectForKey('MC_HTML').js), 'public.html'); }
else { pb.setStringForType($(env.objectForKey('MC_TXT').js), 'public.utf8-plain-text'); }"""
import os
subprocess.run(["osascript", "-l", "JavaScript", "-e", jxa], check=True,
               env={**os.environ, "MC_HTML": html, "MC_TXT": out, "MC_MODE": modus, "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"})
back = subprocess.run(["pbpaste"], capture_output=True, env={"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}).stdout.decode("utf-8")
assert modus == "html" or back == out, "Zwischenablage (Klartext) stimmt nicht mit Text überein"
zeilen = back.split("\n")
print(f"OK: {len(zeilen)} Zeilen, {sum(z == chr(160) for z in zeilen)} NBSP-Leerzeilen, {len(bloecke)} HTML-Absätze, Modus: {modus}.")
