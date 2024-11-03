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

# Color de la pelotita (azul, verde, rojo)
color_pelota = (255, 0, 0)

# Bucle de animacion
while True:
    fotograma = np.zeros((alto, ancho, 3), dtype=np.uint8)
    
    # Dibuja la pelotita
    cv2.circle(fotograma, pos_pelota, radio_pelota, color_pelota, -1)
    
    pos_pelota += velocidad
    
    # Comprobar colision y cambia la direccion
    if pos_pelota[0] - radio_pelota <= 0 or pos_pelota[0] + radio_pelota >= ancho:
        velocidad[0] = -velocidad[0]
        
