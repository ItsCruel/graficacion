import numpy as np
import cv2

# tamaño de la imagen
ancho, alto = 800, 800
img = np.zeros((alto, ancho, 3), dtype=np.uint8)

# Centro de la imagen
centro_x, centro_y = ancho // 2, alto // 2

# Dibujar 10 ecuaciones parametricas
for eq in range(10):
    t = np.linspace(0, 2 * np.pi, 1000)  # Parametro t
   
    if eq == 0:
        # Circulo
        x = 180 * np.cos(t)
        y = 180 * np.sin(t)
    elif eq == 1: