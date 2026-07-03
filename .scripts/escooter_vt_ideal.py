#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Idealisiertes v-t-Diagramm: Anfahren (v steigt) + gleichfoermige Bewegung (v konstant)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ANH = "/Users/oskarklein/Documents/Obsidian Claude/Second Brain Claude/07 Anhänge"

def ideal(vmax, t_acc, t_end, n=400):
    t = np.linspace(0, t_end, n)
    v = np.where(t <= t_acc, vmax * t / t_acc, vmax)
    return t, v

# E-Scooter: Reisegeschw. 5,6 m/s (20 km/h), faehrt bis ~13,8 s (70 m)
ts, vs = ideal(5.6, 2.5, 13.8)
# Schueler: Reisegeschw. 8,7 m/s (31 km/h), bis ~9,3 s
tl, vl = ideal(8.7, 1.5, 9.3)

C_S, C_L = "#1f77b4", "#d62728"
fig, ax = plt.subplots(figsize=(9, 6))

# Beschleunigungsphase hervorheben
ax.axvspan(0, 2.5, color="#ffe9c7", alpha=0.6)
ax.plot(ts, vs, color=C_S, lw=2.6, label="E-Scooter (ideal)  ≈ 5,6 m/s")
ax.plot(tl, vl, color=C_L, lw=2.6, label="Schüler (ideal)  ≈ 8,7 m/s")

# Plateauwerte markieren
ax.axhline(5.6, color=C_S, ls=":", lw=1.1, alpha=0.6)
ax.axhline(8.7, color=C_L, ls=":", lw=1.1, alpha=0.6)

# Phasen-Beschriftung
ax.annotate("Beschleunigungs-\nphase (Anfahren)\nv steigt  →  a > 0",
            xy=(1.2, 2.0), xytext=(3.3, 1.4),
            fontsize=9.5, ha="left", color="#8a5a00",
            arrowprops=dict(arrowstyle="->", color="#8a5a00", lw=1.2))
ax.text(9.5, 6.0, "gleichförmige Bewegung:  v konstant  →  a = 0",
        fontsize=10, ha="center", color="#333", fontweight="bold")

ax.set_xlim(0, 15); ax.set_ylim(0, 13)
ax.set_xticks(range(0, 16)); ax.set_yticks(range(0, 14))
ax.set_title("Idealisiertes v-t-Diagramm  (ohne Messfehler)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Zeit t in s", fontsize=12)
ax.set_ylabel("Geschwindigkeit v in m/s", fontsize=12)
ax.grid(True, which="both", color="#cccccc", linewidth=0.6)
ax.minorticks_on(); ax.grid(True, which="minor", color="#eaeaea", linewidth=0.4)
ax.legend(fontsize=10.5, loc="upper right")
fig.tight_layout()
fig.savefig(f"{ANH}/E-Scooter v-t-Diagramm IDEAL.png", dpi=130)
print("gespeichert:", f"{ANH}/E-Scooter v-t-Diagramm IDEAL.png")
