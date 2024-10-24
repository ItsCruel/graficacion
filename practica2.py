import cv2
import numpy as np

#Cargar la imagen
imagen = cv2.imread('emile.png')

#1.Escala de Grises
imagenGris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

#2.Umbrealizacion
imagenUmbral= cv2.threshold(imagenGris, 127,255,cv2.THRESH_BINARY)

#3.Inversion de Color
imagenInvertida = cv2.bitwise_not (imagen)

#4.Ajuste de Brillo 
imagen