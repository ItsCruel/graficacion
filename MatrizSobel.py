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

# Obtener el tamano 
alto_escalado, ancho_escalado = ImagenEscalada.shape

#matriz de Sobel para bordes
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

        if (i + 1) >= alto_escalado or (j - 1) < 0:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i + 1][j - 1])
        gradiente += pixel * 1

        if (i - 1) < 0:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i - 1][j])
        gradiente += pixel * (-2)

        pixel = int(ImagenEscalada[i][j])
        gradiente += pixel * 0

        if (i + 1) >= alto_escalado:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i + 1][j])
        gradiente += pixel * 2

        if (i - 1) < 0 or (j + 1) >= ancho_escalado:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i - 1][j + 1])
        gradiente += pixel * (-1)

        if (j + 1) >= ancho_escalado:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i][j + 1])
        gradiente += pixel * 0

        if (i + 1) >= alto_escalado or (j + 1) >= ancho_escalado:
            pixel = 0
        else:
            pixel = int(ImagenEscalada[i + 1][j + 1])
        gradiente += pixel * 1

        # limitar los valores 
        if gradiente > 255:
            gradiente = 255
        if gradiente < 0:
            gradiente = 0

        # Asignar el valor del gradiente en la posicion
        ImagenEscalada[i][j] = int(gradiente)

# Mostrar la imagen original y la imagen escalada
cv.imshow('Imagen original', imagen)
cv.imshow('Imagen escalada', ImagenEscalada)
cv.waitKey(0)
cv.destroyAllWindows()

