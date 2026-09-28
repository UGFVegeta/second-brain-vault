#!/usr/bin/env python3
"""Woche 1 und 2 der Mathe 7c ins Wochenformat bringen (mathe_woche_vorlage.py).
Liest die bestehenden ALLES-Dateien (Brüche sind Zahlen, Rationale Zahlen 1 und 2) und übernimmt Vorbereiten, Folien,
Tafelbild, Merkheft und Lösungen. Aus dem ausführlichen Verlauf werden kurze Schritte mit Minuten und Folien-Knöpfen.
Aufgaben-Tab und Ausblick entfallen. Die alten ALLES-Dateien bleiben unverändert liegen.
Aufruf: python3 baue_wochen_1_2.py  -> Brüche/Mathe 7c – Woche 1.html, Rationale Zahlen/Mathe 7c – Woche 2.html"""
import re
from pathlib import Path

from mathe_woche_vorlage import bau_woche

HIER = Path(__file__).parent
BR = HIER / "Brüche" / "Brüche sind Zahlen – ALLES.html"
RZ1 = HIER / "Rationale Zahlen" / "Rationale Zahlen 1 – Zahlen unter Null – ALLES.html"
RZ2 = HIER / "Rationale Zahlen" / "Rationale Zahlen 2 – Addieren und Subtrahieren – ALLES.html"
WEG = ("*", "html", "body", ".wrap", "header", "nav", "h1", "h2", "section", "footer", ".sub", ".tab", ".tabs", ".box", ".kopf")


def text(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()


def semikolon(h):
    """„ · “ als Trenner zwischen Aufgaben wird zu „; “ (sieht sonst wie ein Malpunkt aus).
    In Woche 1 und 2 kommt kein Malnehmen vor, deshalb wird jeder Punkt ersetzt."""
    return re.sub(r"(?:\s|&nbsp;)+(?:·|&middot;)(?:\s|&nbsp;)+", "; ", h)


def sektion(s, sid):
    m = re.search(rf'<section id="{sid}"[^>]*>(.*?)</section>', s, re.S)
    if not m:
        return ""
    inner = re.sub(r"<h2[^>]*>.*?</h2>", "", m.group(1), count=1, flags=re.S)
    inner = re.sub(r'<div class="dok-kopf">.*?</div>', "", inner, count=1, flags=re.S)
    return semikolon(re.sub(r'^\s*<p class="lead">.*?</p>', "", inner, count=1, flags=re.S))


def css(s):
    """CSS der alten Datei ohne Regeln für Seitengerüst (body, nav, h1 …) und ohne @media, damit das Optik-Aussehen bleibt."""
    roh = re.search(r"<style>(.*?)</style>", s, re.S).group(1)
    roh = re.sub(r"@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", roh)
    regeln = re.findall(r"([^{}]+)\{([^{}]*)\}", roh)
    gut = []
    for sel, body in regeln:
        sels = [x.strip() for x in sel.split(",") if x.strip() and not x.strip().split(" ")[0].split(":")[0].split(">")[0] in WEG]
        if sels:
            gut.append(f"{','.join(sels)}{{{body}}}")
    return "<style>" + "".join(gut) + "</style>"


def folien(s):
    out = []
    for f in re.findall(r'<div class="folie">(.*?)</div>\s*(?=<div class="folie">|</section>)', sektion(s, "folien") + "</section>", re.S):
        t = re.search(r"<h3>(.*?)</h3>", f, re.S)
        titel = text(re.sub(r"<span.*?</span>", "", t.group(1))) if t else ""
        titel = re.sub(r"^Folie \d+ · ", "", titel)
        out.append((titel, f[t.end():] if t else f))
    return out


def schritte_rz(s, sid, tag, offset):
    """Phasen aus der Verlaufstabelle: Titel, Minuten, Material kurz, Folien-Knöpfe (mit Versatz für die Wochennummerierung)."""
    v = sektion(s, sid)
    teile = re.split(r'<tr class="grp">', v)[1:]
    out = []
    for i, t in enumerate(teile):
        kopf = re.match(r'<td colspan="4">(.*?)<span>Minute (\d+)–(\d+)</span>', t)
        titel = re.sub(r"^\d+[;·] ", "", text(kopf.group(1)))
        minuten = int(kopf.group(3)) - int(kopf.group(2))
        zellen = re.findall(r"<tr><td class=\"mn\">.*?</td><td>(.*?)</td><td>(.*?)</td>", t, re.S)
        was = text(zellen[0][0]) if zellen else ""
        was = re.split(r"(?<=[.!?])\s", was)[0][:160]
        mat = "; ".join(dict.fromkeys(text(m) for _, m in zellen if text(m) not in ("", "–", "&ndash;")))
        ks = sorted({int(k) + offset for k in re.findall(r"Folie (\d+)", t)})
        d = was + (f' <span style="color:#66798e">({mat})</span>' if mat else "")
        out.append((tag if i == 0 else "", titel, minuten, d, ks))
    return out


def schritte_br(s):
    v = sektion(s, "verlauf")
    out = []
    for block in re.split(r'<div class="tag">', v)[1:]:
        tag = text(block.split("</div>", 1)[0]).replace(" –", ":")
        for i, li in enumerate(re.findall(r"<li>(.*?)</li>", block, re.S)):
            m = re.match(r'\s*<span class="min">(\d+) min</span>(.*)', li, re.S)
            minuten, rest = (int(m.group(1)), text(m.group(2))) if m else (0, text(li))
            satz = re.split(r"(?<=[.!?:])\s", rest)
            titel = satz[0].rstrip(".:")[:70]
            out.append((f"Brüche · {tag}" if i == 0 else "", titel, minuten, " ".join(satz[1:])[:200], []))
    return out


def box(titel, inhalt):
    return f'<div class="box"><h3>{titel}</h3>{inhalt}</div>' if inhalt.strip() else ""


def woche1():
    s = BR.read_text(encoding="utf-8")
    gc = "../Arbeitsblätter/Grundlagen-Check/7c 2026-27/"
    vorb = (box("Grundlagen-Check (Mo, Di)", f'<p>Schnipsel zum Austeilen (iCloud, Mathematik 7c, 02 Grundlagen-Check). Auswertung: '
                f'<a href="{gc}Praesentation.html" target="_blank">Präsentation der Ergebnisse</a>, <a href="{gc}Verlauf.html" target="_blank">Verlauf übers Jahr</a></p>')
            + box("Brüche sind Zahlen (Mi, Do)", '<p>Arbeitsblatt „Brüche sind Zahlen“ in Klassenstärke drucken (Brüche sind Zahlen – Arbeitsblatt.pdf). '
                  'Streifen gleicher Länge für den Einstieg.</p>'))
    schritte = [("Montag und Dienstag", "Grundlagen-Check Teil 1 und 2", 0, "Blöcke A+B und C+D, ohne Namen, nur Nummern. Auswertung als Präsentation.", [])] + schritte_br(s)
    ziel = HIER / "Brüche" / "Mathe 7c – Woche 1.html"
    bau_woche(ziel, "Woche 1: Grundlagen-Check und Brüche sind Zahlen", "Klasse 7c · Mathematik · 14.09. bis 18.09.2026 · Wiederholung Bruchrechnung",
              vorb, schritte, [], sektion(s, "tafelbild"), sektion(s, "merkheft"), sektion(s, "loesungen"), extra_css=css(s), verlauf="Die Woche", legende=False)


def woche2():
    s1, s2 = RZ1.read_text(encoding="utf-8"), RZ2.read_text(encoding="utf-8")
    f1, f2 = folien(s1), folien(s2)
    vorb = box("Dienstag: Rationale Zahlen 1 (Doppelstunde)", sektion(s1, "vorher")) + box("Mittwoch und Donnerstag: Rationale Zahlen 2", sektion(s2, "vorher"))
    schritte = (schritte_rz(s1, "verlauf", "Dienstag, Zahlen unter Null", 0)
                + schritte_rz(s2, "mittwoch", "Mittwoch, Addieren", len(f1)) + schritte_rz(s2, "donnerstag", "Donnerstag, Plus und Minus", len(f1)))
    zwei = lambda t1, t2: box("Dienstag", t1) + box("Mittwoch und Donnerstag", t2)
    ziel = HIER / "Rationale Zahlen" / "Mathe 7c – Woche 2.html"
    bau_woche(ziel, "Woche 2: Zahlen unter Null, Addieren", "Klasse 7c · Mathematik · 21.09. bis 25.09.2026 · Rationale Zahlen",
              vorb, schritte, f1 + f2, zwei(sektion(s1, "tafel"), sektion(s2, "tafel")), zwei(sektion(s1, "merkheft"), sektion(s2, "merkheft")),
              zwei(sektion(s1, "loesungen"), sektion(s2, "loesungen")), extra_css=css(s1) + css(s2), verlauf="Die Woche", legende=False)


if __name__ == "__main__":
    woche1()
    woche2()
