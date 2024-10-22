import numpy as np 
import cv2 as cv 

img = np.ones((500,500),dtype=np.uint8)*240
#tronco 
for i in range (200 , 260):
    for j in range (230,270):
        img [i, j] = 60
#copa 
for i in range (140, 200):
    for j in range (180,320):
        img[i, j]=100
        
#Muestra la imagen
cv.imshow('pixel-art-hongo',img)

cv.waitKey(0)

cv.destroyAllwindows()