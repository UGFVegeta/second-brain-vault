#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bewegungsdiagramme zum E-Scooter-Versuch (Klasse 9 Realschule BW).
Es werden ALLE drei Scooter-Laeufe (t1, t2, t3) einzeln gezeigt + Schueler (t4)."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ANH = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/07 Anhänge"

s = np.array([0, 10, 20, 30, 40, 50, 60, 70], dtype=float)  # Weg in m

# Zeiten in s (Messwerte), Spalten = 10..70 m; vorne Start 0 ergaenzt
t1 = np.array([0, 3.6, 5.0, 7.3, 8.7, 10.7, 12.1, 14.0])
t2 = np.array([0, 2.1, 4.3, 6.8, 8.2, 9.9, 11.8, 13.6])
t3 = np.array([0, 2.6, 4.5, 6.8, 8.2, 10.1, 12.0, 13.8])
t4 = np.array([0, 2.2, 3.1, 4.7, 5.8, 7.0, 8.0, 9.3])  # Schueler, gelaufen

# drei Blautoene fuer die Scooter-Laeufe, rot fuer den Schueler
SCOOT = [("t₁ (Scooter)", t1, "#9ecae1"),
         ("t₂ (Scooter)", t2, "#4292c6"),
         ("t₃ (Scooter)", t3, "#08519c")]
LAUF = ("t₄ (Schüler, gelaufen)", t4, "#d62728")

def style(ax, xlabel, ylabel, title):
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, which="both", color="#cccccc", linewidth=0.6)
    ax.minorticks_on()
    ax.grid(True, which="minor", color="#eaeaea", linewidth=0.4)
    ax.legend(fontsize=10, loc="best")

# ---------- 1) s-t-Diagramm ----------
fig, ax = plt.subplots(figsize=(9, 6))
for name, t, c in SCOOT:
    ax.plot(t, s, "-o", color=c, lw=1.8, ms=6, label=name)
ax.plot(LAUF[1], s, "-s", color=LAUF[2], lw=2.2, ms=7, label=LAUF[0])
ax.set_xlim(0, 15); ax.set_ylim(0, 75)
ax.set_xticks(range(0, 16)); ax.set_yticks(range(0, 76, 10))
style(ax, "Zeit t in s", "Weg s in m", "s-t-Diagramm:  E-Scooter (3 Läufe) vs. Schüler")
fig.tight_layout()
fig.savefig(f"{ANH}/E-Scooter s-t-Diagramm.png", dpi=130)
plt.close(fig)

# ---------- Abschnittsgeschwindigkeiten ----------
def segment_v(t):
    v = np.diff(s) / np.diff(t)          # je 10 m
    tmid = (t[1:] + t[:-1]) / 2
    return tmid, v

# ---------- 2) v-t-Diagramm ----------
fig, ax = plt.subplots(figsize=(9, 6))
for name, t, c in SCOOT:
    tm, v = segment_v(t)
    ax.plot(tm, v, "-o", color=c, lw=1.6, ms=5, label=name)
tm, v = segment_v(LAUF[1])
ax.plot(tm, v, "-s", color=LAUF[2], lw=2.0, ms=6, label=LAUF[0])
# Orientierungslinien: mittlere Reisegeschwindigkeit
ax.axhline(5.6, color="#08519c", ls="--", lw=1.2, alpha=0.6, label="Scooter Ø ≈ 5,6 m/s (20 km/h)")
ax.axhline(8.7, color=LAUF[2], ls="--", lw=1.2, alpha=0.5, label="Schüler Ø ≈ 8,7 m/s (31 km/h)")
ax.set_xlim(0, 15); ax.set_ylim(0, 13)
ax.set_xticks(range(0, 16)); ax.set_yticks(range(0, 14))
style(ax, "Zeit t in s", "Geschwindigkeit v in m/s", "v-t-Diagramm:  E-Scooter (3 Läufe) vs. Schüler")
fig.tight_layout()
fig.savefig(f"{ANH}/E-Scooter v-t-Diagramm.png", dpi=130)
plt.close(fig)

# ---------- 3) a-t-Diagramm ----------
def segment_a(t):
    tm, v = segment_v(t)
    a = np.diff(v) / np.diff(tm)
    tm2 = (tm[1:] + tm[:-1]) / 2
    return tm2, a

fig, ax = plt.subplots(figsize=(9, 6))
ax.axhline(0, color="#444444", lw=1.2)
ax.axhspan(-1, 1, color="#2ca02c", alpha=0.08)
for name, t, c in SCOOT:
    ta, a = segment_a(t)
    ax.plot(ta, a, "-o", color=c, lw=1.4, ms=5, alpha=0.9, label=name)
ta, a = segment_a(LAUF[1])
ax.plot(ta, a, "-s", color=LAUF[2], lw=1.8, ms=6, alpha=0.9, label=LAUF[0])
ax.text(7.5, 0.2, "Bereich a ≈ 0  →  gleichförmige Bewegung",
        color="#2ca02c", fontsize=10, ha="center", fontweight="bold")
ax.set_xlim(0, 15); ax.set_ylim(-8, 8)
ax.set_xticks(range(0, 16))
style(ax, "Zeit t in s", "Beschleunigung a in m/s²", "a-t-Diagramm:  E-Scooter (3 Läufe) vs. Schüler")
fig.tight_layout()
fig.savefig(f"{ANH}/E-Scooter a-t-Diagramm.png", dpi=130)
plt.close(fig)

print("Diagramme neu erstellt: 3 Scooter-Läufe (t1,t2,t3) + Schüler (t4).")
