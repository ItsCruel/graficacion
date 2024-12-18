import cv2
import numpy as np

#Crear una imagen en blanco de 500 x 500
imagen = np.zeros((500,500 , 3), dtype="uint8")

#Dibujar cabeza (circulo)
cv2.circle(imagen,(250,150),50,(255,0,0), -1)

#Dibujar el cuerpo (rectangulo)
cv2.rectangle(imagen,(220,200),(280,350),(255,0,0),-1)

#Dibujar brazos
cv2.line(imagen, (220 , 220),(150,300),(255,0,0),5)
cv2.line(imagen, (280 , 220),(350,300),(255,0,0),5)

#Dibujar las piernas 
cv2.line(imagen,(240 , 350),(200,450),(255,0,0),5)#pierna izquierda
cv2.line(imagen,(260 , 350),(300,450),(255,0,0),5)#pierna derecha

#Monstrando resultado
cv2.imshow('persona',imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()