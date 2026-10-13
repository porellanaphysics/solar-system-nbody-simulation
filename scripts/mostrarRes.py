import os
import numpy as np
import matplotlib.pyplot as plt

# Función para leer el archivo .dat
def leer_datos(archivo):
    with open(archivo, 'r') as f:
        datos = np.loadtxt(f)
    tiempo = datos[:, 0]
    posiciones = datos[:, 1:]
    return tiempo, posiciones

# Función para graficar los planetas en el plano con zoom interactivo
def graficar_planetas_en_plano(tiempo, posiciones):
    # Nombres de los planetas
    planetas = ["Sol", "Mercurio", "Venus", "Tierra", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno"]
    
    # Separar posiciones x e y
    x = posiciones[:, ::2]
    y = posiciones[:, 1::2]
    
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(8, 8))
    for i in range(len(planetas)):
        ax.plot(x[:, i], y[:, i], label=planetas[i])
    
    ax.set_title("Trayectorias de los Planetas en el Plano")
    ax.set_xlabel("Posición X")
    ax.set_ylabel("Posición Y")
    ax.legend()
    ax.grid()
    ax.axis('equal')  # Asegurar proporciones iguales en los ejes

    # Habilitar zoom interactivo
    def on_scroll(event):
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        x_range = (xlim[1] - xlim[0]) * 0.1
        y_range = (ylim[1] - ylim[0]) * 0.1

        if event.button == 'up':  # Zoom in
            ax.set_xlim([xlim[0] + x_range, xlim[1] - x_range])
            ax.set_ylim([ylim[0] + y_range, ylim[1] - y_range])
        elif event.button == 'down':  # Zoom out
            ax.set_xlim([xlim[0] - x_range, xlim[1] + x_range])
            ax.set_ylim([ylim[0] - y_range, ylim[1] + y_range])
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('scroll_event', on_scroll)
    plt.show()

# Archivo de entrada
archivo = "resultado.dat"  # Cambia esto por la ruta de tu archivo .dat

# Leer los datos y graficar
try:
    tiempo, posiciones = leer_datos(archivo)
    graficar_planetas_en_plano(tiempo, posiciones)
except Exception as e:
    print(f"Error al procesar el archivo: {e}")
