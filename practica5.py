import cv2
import numpy as np

#Crear una imagen en blanco de 500 x 500
imagen = np.zeros((500,500 , 3), dtype="uint8")

#Dibujar cabeza (circulo)
cv2.circle(imagen,(250,150),50,(255,0,0), -1)

#Dibujar el cuerpo (rectangulo)
cv2.rectangle(imagen,(220,200),(280,350),(255,0,0)-1)

#Dibujar brazos
cv2.line(imagen, (220 , 220),(150,300))
cv2.line