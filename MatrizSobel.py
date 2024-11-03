import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
imagen = cv.imread('espartan.jpg', 0)

#tamaño de la imagen original
alto, ancho = imagen.shape

# factor de escala
escala_x, escala_y = 2, 2

# imagen para el escalado
ImagenEscalada = np.zeros((int(alto * escala_y), int(ancho * escala_x)), dtype=np.uint8)


# imagen duplicando pixeles
for i in range(alto):
    for j in range(ancho):
        ImagenEscalada[i * escala_y, j * escala_x] = imagen[i, j]

# Obtener el tamaño 
alto_escalado, ancho_escalado = ImagenEscalada.shape

#matriz de Sobel para detectar bordes
for i in range(alto_escalado):
    for j in range(ancho_escalado):
        
        gradiente = 0
        if (i - 1) < 0 or (j - 1) < 0:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i - 1][j - 1])
        gradiente += pixel * (-1)

        if (j - 1) < 0:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i][j - 1])
        gradiente += pixel * 0

