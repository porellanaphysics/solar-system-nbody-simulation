import os
from manim import *
import numpy as np

class SistemaSolar(ThreeDScene):
    def construct(self):
        # Configuración de la escena
        self.camera.background_color = BLACK
        
        # Cargar datos
        file_path = "resultado.dat" if os.path.exists("resultado.dat") else "../resultado.dat"
        data = np.loadtxt(file_path)
        
        tiempos = data[:, 0]
        num_planetas = (data.shape[1] - 1) // 2
        posiciones = [data[:, 2*i+1:2*i+3] for i in range(num_planetas)]
        
        # Reducción de puntos para mejor rendimiento
        step = 200
        posiciones_reducidas = [pos[::step] for pos in posiciones]

        # Configuración visual de planetas
        colores = [YELLOW, "#888888", "#DDDDDD", BLUE, RED, "#E3E4E5", "#F5D382", "#D1E7E7", "#4169E1"]
        tamanos = [0.3, 0.1, 0.12, 0.13, 0.11, 0.2, 0.18, 0.15, 0.15]
        factores_escala = [1, 12, 12, 12, 12, 8, 8, 6, 6]  # Factores ajustados

        # Crear planetas
        planetas = []
        for i in range(num_planetas):
            planeta = Dot3D(color=colores[i], radius=tamanos[i], resolution=(8,8))
            planetas.append(planeta)
            self.add(planeta)

        # Añadir etiquetas
        nombres = ["Sol", "Mercurio", "Venus", "Tierra", "Marte", 
                  "Júpiter", "Saturno", "Urano", "Neptuno"]
        etiquetas = []
        for i in range(num_planetas):
            etiqueta = Text(nombres[i], font_size=24).next_to(planetas[i], UP, buff=0.3)
            etiquetas.append(etiqueta)
            self.add(etiqueta)

        # Configurar vista de cámara
        self.set_camera_orientation(zoom=0.5)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Animación
        duracion_total = 30
        num_pasos = len(posiciones_reducidas[0])
        
        for i in range(num_pasos):
            self.wait(duracion_total/num_pasos)
            for j in range(num_planetas):
                x, y = posiciones_reducidas[j][i]
                planetas[j].move_to([x * factores_escala[j], y * factores_escala[j], 0])
                if j < len(etiquetas):
                    etiquetas[j].next_to(planetas[j], UP, buff=0.3)

        # Ajuste final de cámara
        self.move_camera(zoom=0.8, run_time=3)