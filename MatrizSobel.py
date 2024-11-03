import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
imagen = cv.imread('espartan.jpg', 0)

#tamaño de la imagen original
alto, ancho = imagen.shape

# factor de escala
escala_x, escala_y = 2, 2

# nueva imagen para el escalado
imagen_escalada = np.zeros((int(alto * escala_y), int(ancho * escala_x)), dtype=np.uint8)


