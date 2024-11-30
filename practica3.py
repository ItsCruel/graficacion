import cv2 as cv
import numpy as np
import math

# Cargar la imagen 
img = cv.imread('halo2.png', 0)
if img is None:
    print("Error al cargar la imagen.")
    exit()

# Obtener el tamaño de la imagen
x, y = img.shape

# Traslacion
dx, dy = 100, 50
translated_img = np.zeros((x, y), dtype=np.uint8)
for i in range(x):
    for j in range(y):
        new_x = i + dy
        new_y = j + dx
        if 0 <= new_x < x and 0 <= new_y < y:
            translated_img[new_x, new_y] = img[i, j]

# Rotacion 
angle = 45
theta = math.radians(angle)
rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)
cx, cy = x // 2, y // 2
for i in range(x):
    for j in range(y):
        new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx + x//2)
        new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy + y//2)
        if 0 <= new_x < 2*y and 0 <= new_y < 2*x:
            rotated_img[new_y, new_x] = translated_img[i, j]

# Escalamiento
scale_x, scale_y = 2, 2
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)
for i in range(x):
    for j in range(y):
        new_x = int(i * scale_y)
        new_y = int(j * scale_x)
        if new_x < scaled_img.shape[0] and new_y < scaled_img.shape[1]:
            scaled_img[new_x, new_y] = rotated_img[i, j]

# resultados
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Trasladada', translated_img)
cv.imshow('Imagen Rotada', rotated_img)
cv.imshow('Imagen Escalada', scaled_img)
cv.waitKey(0)
cv.destroyAllWindows()
