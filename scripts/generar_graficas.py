#!/usr/bin/env python3
"""
Script de generación de figuras de alta resolución para el portfolio de RSS.
Procesa resultado.dat y exporta figuras publicables en assets/
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Directorios
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(BASE_DIR, "resultado.dat")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)

print("Cargando datos de simulación desde:", DATA_FILE)
# Submuestreo para generación rápida y nítida
datos = np.loadtxt(DATA_FILE)[::10]
t = datos[:, 0]
t_years = t / (2.0 * np.pi)  # 1 año = 2*pi unidades adimensionales

planetas = [
    ("Sol", "#FFD700", 6),
    ("Mercurio", "#A0A0A0", 3),
    ("Venus", "#E3BB7B", 4),
    ("Tierra", "#2E86C1", 4.5),
    ("Marte", "#CB4335", 3.5),
    ("Júpiter", "#E67E22", 5.5),
    ("Saturno", "#F4D03F", 5),
    ("Urano", "#48C9B0", 4.5),
    ("Neptuno", "#2980B9", 4.5),
]

# Configuración de estilo global
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "axes.edgecolor": "#CCCCCC",
    "axes.linewidth": 0.8,
    "grid.color": "#E0E0E0",
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
})

# ==============================================================================
# FIGURA 1: Vista Global del Sistema Solar vs. Zoom Planetas Interiores
# ==============================================================================
print("Generando Figura 1: Trayectorias Globales y Zoom Interior...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300)

# Panel 1: Sistema Solar Completo
for i, (nombre, color, _) in enumerate(planetas):
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    if i == 0:
        ax1.plot(x[-1], y[-1], 'o', color=color, markersize=8, label=nombre, zorder=5)
    else:
        ax1.plot(x, y, color=color, lw=1.2, label=nombre, alpha=0.9)
        ax1.plot(x[-1], y[-1], 'o', color=color, markersize=5)

ax1.set_title("Sistema Solar Completo (N = 9 cuerpos)", fontsize=13, fontweight="bold", pad=10)
ax1.set_xlabel("Posición X [UA]", fontsize=11)
ax1.set_ylabel("Posición Y [UA]", fontsize=11)
ax1.set_xlim(-35, 35)
ax1.set_ylim(-35, 35)
ax1.set_aspect("equal")
ax1.grid(True)
ax1.legend(loc="upper right", fontsize=8.5, framealpha=0.9)

# Panel 2: Planetas Terrestres (Zoom < 2 UA)
for i in range(5):  # Sol hasta Marte
    nombre, color, _ = planetas[i]
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    if i == 0:
        ax2.plot(x[-1], y[-1], 'o', color=color, markersize=10, label=nombre, zorder=5)
    else:
        ax2.plot(x, y, color=color, lw=1.5, label=nombre, alpha=0.95)
        ax2.plot(x[-1], y[-1], 'o', color=color, markersize=6)

ax2.set_title("Planetas Terrestres Interiores (Detalle < 2 UA)", fontsize=13, fontweight="bold", pad=10)
ax2.set_xlabel("Posición X [UA]", fontsize=11)
ax2.set_ylabel("Posición Y [UA]", fontsize=11)
ax2.set_xlim(-1.8, 1.8)
ax2.set_ylim(-1.8, 1.8)
ax2.set_aspect("equal")
ax2.grid(True)
ax2.legend(loc="upper right", fontsize=9.5, framealpha=0.9)

plt.tight_layout()
out1 = os.path.join(ASSETS_DIR, "solar_system_orbits_comparison.png")
fig.savefig(out1, bbox_inches="tight")
plt.close(fig)
print("Guardada:", out1)

# ==============================================================================
# FIGURA 2: Distancias Radiales vs. Tiempo (Periodicidad y Estabilidad)
# ==============================================================================
print("Generando Figura 2: Distancia radial vs. Tiempo...")
fig, (ax_in, ax_out) = plt.subplots(2, 1, figsize=(12, 7.5), dpi=300, sharex=True)

# Panel A: Planetas Interiores
for i in range(1, 5):
    nombre, color, _ = planetas[i]
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    r = np.sqrt(x**2 + y**2)
    ax_in.plot(t_years, r, color=color, lw=1.3, label=f"{nombre} (a ~ {r.mean():.2f} UA)")

ax_in.set_title("Evolución de Distancias Radiales: Planetas Terrestres", fontsize=12, fontweight="bold")
ax_in.set_ylabel("Distancia al Sol [UA]", fontsize=11)
ax_in.grid(True)
ax_in.legend(loc="upper right", fontsize=9, framealpha=0.9)

# Panel B: Planetas Gigantes Exteriores
for i in range(5, 9):
    nombre, color, _ = planetas[i]
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    r = np.sqrt(x**2 + y**2)
    ax_out.plot(t_years, r, color=color, lw=1.3, label=f"{nombre} (a ~ {r.mean():.2f} UA)")

ax_out.set_title("Evolución de Distancias Radiales: Gigantes Gaseosos", fontsize=12, fontweight="bold")
ax_out.set_xlabel("Tiempo transcurrido [Años]", fontsize=11)
ax_out.set_ylabel("Distancia al Sol [UA]", fontsize=11)
ax_out.grid(True)
ax_out.legend(loc="upper right", fontsize=9, framealpha=0.9)

plt.tight_layout()
out2 = os.path.join(ASSETS_DIR, "orbital_distances_time.png")
fig.savefig(out2, bbox_inches="tight")
plt.close(fig)
print("Guardada:", out2)

# ==============================================================================
# FIGURA 3: Análisis Detallado del Perihelio de Mercurio
# ==============================================================================
print("Generando Figura 3: Detalle Órbita y Precesión de Mercurio...")
fig, ax = plt.subplots(figsize=(8, 7), dpi=300)

x_merc = datos[:, 3]
y_merc = datos[:, 4]
r_merc = np.sqrt(x_merc**2 + y_merc**2)

# Encontrar mínimos locales (perihelios)
minimos_idx = []
for k in range(1, len(r_merc) - 1):
    if r_merc[k] < r_merc[k-1] and r_merc[k] < r_merc[k+1]:
        minimos_idx.append(k)

ax.plot(x_merc, y_merc, color="#7F8C8D", lw=0.9, alpha=0.7, label="Trayectoria de Mercurio")
ax.plot(0, 0, 'o', color="#F39C12", markersize=12, label="Sol (Centro de masas)")

if len(minimos_idx) > 0:
    ax.scatter(
        x_merc[minimos_idx],
        y_merc[minimos_idx],
        c=t_years[minimos_idx],
        cmap="coolwarm",
        s=35,
        zorder=5,
        label="Puntos de Perihelio"
    )
    cbar = plt.colorbar(ax.collections[0], ax=ax, pad=0.02)
    cbar.set_label("Tiempo [Años]", fontsize=10)

ax.set_title("Precesión del Perihelio de Mercurio en el Sistema Solar", fontsize=12, fontweight="bold", pad=10)
ax.set_xlabel("X [UA]", fontsize=11)
ax.set_ylabel("Y [UA]", fontsize=11)
ax.set_aspect("equal")
ax.grid(True)
ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

plt.tight_layout()
out3 = os.path.join(ASSETS_DIR, "mercury_precession_detail.png")
fig.savefig(out3, bbox_inches="tight")
plt.close(fig)
print("Guardada:", out3)

print("¡Todas las figuras han sido generadas con éxito!")
