#!/usr/bin/env python3
"""
Script de generación de figuras de alta resolución en MODO OSCURO (Dark Mode)
para el portfolio de Real Solar System (RSS).
Estética astronómica moderna inspirada en misiones espaciales y dashboards científicos.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Directorios del proyecto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(BASE_DIR, "resultado.dat")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)

print("Cargando datos de simulación desde:", DATA_FILE)
# Submuestreo balanceado para curvas suaves y nítidas
datos = np.loadtxt(DATA_FILE)[::8]
t = datos[:, 0]
t_years = t / (2.0 * np.pi)  # 1 año = 2*pi unidades adimensionales

# Paleta luminosa moderna sobre fondo oscuro
# (Nombre, Color de trazo, Color de punto / halo, Tamaño)
planetas_info = [
    ("Sol",      "#FDE047", "#FFFBEB", 7),
    ("Mercurio", "#94A3B8", "#E2E8F0", 3.2),
    ("Venus",    "#F59E0B", "#FDE68A", 4.2),
    ("Tierra",   "#38BDF8", "#BAE6FD", 4.5),
    ("Marte",    "#F87171", "#FECACA", 3.8),
    ("Júpiter",  "#FB923C", "#FFEDD5", 5.5),
    ("Saturno",  "#FACC15", "#FEF08A", 5.0),
    ("Urano",    "#2DD4BF", "#CCFBF1", 4.5),
    ("Neptuno",  "#818CF8", "#E0E7FF", 4.5),
]

# Configuración de tema oscuro moderno
BG_DARK = "#090D16"       # Fondo global de espacio profundo
AXES_DARK = "#0D1322"     # Fondo de los ejes
GRID_COLOR = "#1E293B"    # Cuadrícula sutil
SPINE_COLOR = "#334155"   # Bordes de los ejes
TEXT_COLOR = "#F8FAFC"    # Texto blanco de alto contraste
MUTED_TEXT = "#94A3B8"    # Texto secundario

plt.rcParams.update({
    "figure.facecolor": BG_DARK,
    "axes.facecolor": AXES_DARK,
    "savefig.facecolor": BG_DARK,
    "text.color": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": MUTED_TEXT,
    "ytick.color": MUTED_TEXT,
    "axes.edgecolor": SPINE_COLOR,
    "axes.linewidth": 1.0,
    "grid.color": GRID_COLOR,
    "grid.linestyle": ":",
    "grid.linewidth": 0.7,
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
})

# ==============================================================================
# FIGURA 1: Vista Global del Sistema Solar vs. Zoom Planetas Interiores (Modo Oscuro)
# ==============================================================================
print("Generando Figura 1: Trayectorias Globales y Zoom Interior (Dark Mode)...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.2), dpi=300)

# Panel 1: Sistema Solar Completo (hasta 35 UA)
for i, (nombre, color_trazo, color_punto, tam) in enumerate(planetas_info):
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    
    if i == 0:
        # Halo de radiación solar
        ax1.scatter([x[-1]], [y[-1]], color=color_trazo, s=180, alpha=0.25, zorder=4)
        ax1.scatter([x[-1]], [y[-1]], color=color_punto, s=55, label=nombre, zorder=5)
    else:
        # Trazo de órbita con leve resplandor
        ax1.plot(x, y, color=color_trazo, lw=1.2, alpha=0.85, label=nombre)
        ax1.scatter([x[-1]], [y[-1]], color=color_punto, s=tam*5, edgecolors=color_trazo, linewidths=0.8, zorder=4)

ax1.set_title("Sistema Solar Completo ($N = 9$ Cuerpos)", fontsize=13, fontweight="bold", pad=12, color=TEXT_COLOR)
ax1.set_xlabel("Posición X [UA]", fontsize=11, labelpad=8)
ax1.set_ylabel("Posición Y [UA]", fontsize=11, labelpad=8)
ax1.set_xlim(-34, 34)
ax1.set_ylim(-34, 34)
ax1.set_aspect("equal")
ax1.grid(True, alpha=0.6)

# Leyenda estilizada
leg1 = ax1.legend(loc="upper right", fontsize=8.5, facecolor="#131B2E", edgecolor="#334155", framealpha=0.9)
for text in leg1.get_texts():
    text.set_color(TEXT_COLOR)

# Panel 2: Planetas Terrestres (Zoom < 1.8 UA)
for i in range(5):  # Sol, Mercurio, Venus, Tierra, Marte
    nombre, color_trazo, color_punto, tam = planetas_info[i]
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    
    if i == 0:
        # Sol central con halo radiante
        ax2.scatter([x[-1]], [y[-1]], color=color_trazo, s=300, alpha=0.2, zorder=4)
        ax2.scatter([x[-1]], [y[-1]], color=color_trazo, s=120, alpha=0.4, zorder=5)
        ax2.scatter([x[-1]], [y[-1]], color=color_punto, s=50, label=nombre, zorder=6)
    else:
        # Trazo de órbita
        ax2.plot(x, y, color=color_trazo, lw=1.6, alpha=0.9, label=nombre)
        ax2.scatter([x[-1]], [y[-1]], color=color_punto, s=tam*8, edgecolors=color_trazo, linewidths=1.2, zorder=5)

ax2.set_title("Planetas Terrestres Interiores (Detalle $< 1.8$ UA)", fontsize=13, fontweight="bold", pad=12, color=TEXT_COLOR)
ax2.set_xlabel("Posición X [UA]", fontsize=11, labelpad=8)
ax2.set_ylabel("Posición Y [UA]", fontsize=11, labelpad=8)
ax2.set_xlim(-1.75, 1.75)
ax2.set_ylim(-1.75, 1.75)
ax2.set_aspect("equal")
ax2.grid(True, alpha=0.6)

leg2 = ax2.legend(loc="upper right", fontsize=9.5, facecolor="#131B2E", edgecolor="#334155", framealpha=0.9)
for text in leg2.get_texts():
    text.set_color(TEXT_COLOR)

plt.tight_layout()
out1 = os.path.join(ASSETS_DIR, "solar_system_orbits_comparison.png")
fig.savefig(out1, bbox_inches="tight", dpi=300)
plt.close(fig)
print("Guardada:", out1)

# ==============================================================================
# FIGURA 2: Distancias Radiales vs. Tiempo (Periodicidad y Estabilidad)
# ==============================================================================
print("Generando Figura 2: Distancia radial vs. Tiempo (Dark Mode)...")
fig, (ax_in, ax_out) = plt.subplots(2, 1, figsize=(13, 8), dpi=300, sharex=True)

# Panel A: Planetas Terrestres
for i in range(1, 5):
    nombre, color_trazo, _, _ = planetas_info[i]
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    r = np.sqrt(x**2 + y**2)
    ax_in.plot(t_years, r, color=color_trazo, lw=1.5, alpha=0.95, label=f"{nombre} ($a \\approx {r.mean():.2f}$ UA)")

ax_in.set_title("Evolución de Distancias Radiales: Planetas Terrestres", fontsize=12, fontweight="bold", pad=10, color=TEXT_COLOR)
ax_in.set_ylabel("Distancia al Sol [UA]", fontsize=11, labelpad=8)
ax_in.grid(True, alpha=0.6)
leg_in = ax_in.legend(loc="upper right", fontsize=9, facecolor="#131B2E", edgecolor="#334155", framealpha=0.9)
for text in leg_in.get_texts():
    text.set_color(TEXT_COLOR)

# Panel B: Planetas Gigantes Exteriores
for i in range(5, 9):
    nombre, color_trazo, _, _ = planetas_info[i]
    x = datos[:, 2*i + 1]
    y = datos[:, 2*i + 2]
    r = np.sqrt(x**2 + y**2)
    ax_out.plot(t_years, r, color=color_trazo, lw=1.5, alpha=0.95, label=f"{nombre} ($a \\approx {r.mean():.2f}$ UA)")

ax_out.set_title("Evolución de Distancias Radiales: Gigantes Gaseosos", fontsize=12, fontweight="bold", pad=10, color=TEXT_COLOR)
ax_out.set_xlabel("Tiempo transcurrido [Años terrestres]", fontsize=11, labelpad=8)
ax_out.set_ylabel("Distancia al Sol [UA]", fontsize=11, labelpad=8)
ax_out.grid(True, alpha=0.6)
leg_out = ax_out.legend(loc="upper right", fontsize=9, facecolor="#131B2E", edgecolor="#334155", framealpha=0.9)
for text in leg_out.get_texts():
    text.set_color(TEXT_COLOR)

plt.tight_layout()
out2 = os.path.join(ASSETS_DIR, "orbital_distances_time.png")
fig.savefig(out2, bbox_inches="tight", dpi=300)
plt.close(fig)
print("Guardada:", out2)

# ==============================================================================
# FIGURA 3: Análisis Detallado del Perihelio de Mercurio (Dark Mode)
# ==============================================================================
print("Generando Figura 3: Detalle Órbita y Precesión de Mercurio (Dark Mode)...")
fig, ax = plt.subplots(figsize=(8.5, 7.5), dpi=300)

x_merc = datos[:, 3]
y_merc = datos[:, 4]
r_merc = np.sqrt(x_merc**2 + y_merc**2)

# Encontrar mínimos locales (perihelios)
minimos_idx = []
for k in range(1, len(r_merc) - 1):
    if r_merc[k] < r_merc[k-1] and r_merc[k] < r_merc[k+1]:
        minimos_idx.append(k)

# Trazo orbital en gris espacial sutil
ax.plot(x_merc, y_merc, color="#475569", lw=1.1, alpha=0.75, label="Trayectoria de Mercurio")

# Sol en el origen con brillo estelar
ax.scatter([0], [0], color="#FDE047", s=350, alpha=0.25, zorder=4)
ax.scatter([0], [0], color="#FACC15", s=130, alpha=0.6, zorder=5)
ax.scatter([0], [0], color="#FEF9C3", s=45, label="Sol (Barycenter)", zorder=6)

if len(minimos_idx) > 0:
    # Scatter con gradiente de color espectral de tiempo (Plasma / Electric Cyan-Purple)
    sc = ax.scatter(
        x_merc[minimos_idx],
        y_merc[minimos_idx],
        c=t_years[minimos_idx],
        cmap="plasma",
        s=55,
        edgecolors="#F8FAFC",
        linewidths=0.7,
        zorder=7,
        label="Puntos de Perihelio"
    )
    cbar = plt.colorbar(sc, ax=ax, pad=0.03)
    cbar.set_label("Tiempo transcurrido [Años terrestres]", fontsize=10, color=TEXT_COLOR, labelpad=8)
    cbar.ax.yaxis.set_tick_params(color=MUTED_TEXT)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=MUTED_TEXT)
    cbar.outline.set_edgecolor(SPINE_COLOR)

ax.set_title("Precesión del Perihelio de Mercurio en el Sistema Solar", fontsize=12.5, fontweight="bold", pad=12, color=TEXT_COLOR)
ax.set_xlabel("X [UA]", fontsize=11, labelpad=8)
ax.set_ylabel("Y [UA]", fontsize=11, labelpad=8)
ax.set_xlim(-0.55, 0.55)
ax.set_ylim(-0.55, 0.55)
ax.set_aspect("equal")
ax.grid(True, alpha=0.6)

leg3 = ax.legend(loc="upper right", fontsize=9.5, facecolor="#131B2E", edgecolor="#334155", framealpha=0.9)
for text in leg3.get_texts():
    text.set_color(TEXT_COLOR)

plt.tight_layout()
out3 = os.path.join(ASSETS_DIR, "mercury_precession_detail.png")
fig.savefig(out3, bbox_inches="tight", dpi=300)
plt.close(fig)
print("Guardada:", out3)

print("¡Todas las figuras en MODO OSCURO han sido generadas con éxito!")
