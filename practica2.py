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
imagenBrillante = cv2.bitwise_not(imagen)

#5.Ajuste de Contraste
imagenContraste = cv2.convertScaleAbs(imagen,alpha=1.5,beta=0)

#Mostrando los 5 operadores puntuales
cv2.imshow ('imagen normal', imagen)
cv2.imshow('Imagen con escala de grises', imagenGris)
cv2.imshow('imagen con Umbralizacion', imagenUmbral)
cv2.imshow('imagen Brillo Aumentado', imagenBrillante)
cv2.imshow('imagen Invertida', imagenInvertida)
cv2.imshow ('imagen con Contraste ', imagenContraste)
cv2.waitKey(0)
cv2.destroyAllWindows()
