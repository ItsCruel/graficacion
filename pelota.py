import cv2
import numpy as np

# Dimensiones de la ventana
ancho, alto = 640, 480

# Crear ventana
cv2.namedWindow("Animacion", cv2.WINDOW_AUTOSIZE)

# Posicion inicial
pos_pelota = np.array([100, 100])
radio_pelota = 20
velocidad = np.array([5, 3])
