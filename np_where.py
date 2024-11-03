import cv2
import numpy as np

# Leer la imagen en formato RGB
imagen = cv2.imread('halo2.png', 1)

# Convertir la imagen de RGB a HSV
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Definir el rango de color rojo en HSV
bajo_rojo1 = np.array([0, 40, 40])
alto_rojo1 = np.array([10, 255, 255])
bajo_rojo2 = np.array([160, 40, 40])

