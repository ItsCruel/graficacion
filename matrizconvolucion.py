import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
imagen = cv.imread('espartan.jpg', 0)

# Obtener el tamaño de la imagen
alto, ancho = imagen.shape

# Definir el factor de escala
escala_x, escala_y = 2, 2
# Crear una nueva imagen para almacenar el escalado
imagen_escalada = np.zeros((int(alto * escala_y), int(ancho * escala_x)), dtype=np.uint8)


# Aplicar el escalado
for i in range(alto):
    for j in range(ancho):
        imagen_escalada[i * escala_y, j * escala_x] = imagen[i, j]

# Obtener el tamaño de la imagen escalada
alto_escalado, ancho_escalado = imagen_escalada.shape

# Aplicar la matriz de suavizado por 1/9 (trabajo de clase)
for i in range(alto_escalado):
    for j in range(ancho_escalado):
        valor = 0
        if (i - 1) < 0 or (j - 1) < 0:
            vecino = 0
        else:
            vecino = int(imagen_escalada[i - 1][j - 1])
        valor += vecino * (1 / 9)
        
        if (j - 1) < 0:
            vecino = 0
        else:
            vecino = int(imagen_escalada[i][j - 1])
        valor += vecino * (1 / 9)

        if (i + 1) >= alto_escalado or (j - 1) < 0:
            vecino = 0
        else:
            vecino = int(imagen_escalada[i + 1][j - 1])
        valor += vecino * (1 / 9)

        if (i - 1) < 0:
            vecino = 0
        else:
            vecino = int(imagen_escalada[i - 1][j])
        valor += vecino * (1 / 9)

        vecino = int(imagen_escalada[i][j])
        valor += vecino * (1 / 9)

        if (i + 1) >= alto_escalado:
            vecino = 0
        else:
            vecino = int(imagen_escalada[i + 1][j])
        valor += vecino * (1 / 9)

        if (i - 1) < 0 or (j + 1) >= ancho_escalado:
            vecino = 0
        else:
            vecino = int(imagen_escalada[i - 1][j + 1])
        valor += vecino * (1 / 9)

        if (j + 1) >= ancho_escalado:
            vecino = 0
        else:

            vecino = int(imagen_escalada[i][j + 1])
        valor += vecino * (1 / 9)

        if (i + 1) >= alto_escalado or (j + 1) >= ancho_escalado:
            vecino = 0
        else:

            vecino = int(imagen_escalada[i + 1][j + 1])
        valor += vecino * (1 / 9)

        valor = min(max(int(valor), 0), 255)

        imagen_escalada[i][j] = valor


# Mostrar la imagen original y la imagen escalada
cv.imshow('Imagen Original', imagen)

cv.imshow('Imagen Escalada', imagen_escalada)
#cerrando
cv.waitKey(0)
cv.destroyAllWindows()
