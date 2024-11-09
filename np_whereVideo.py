import cv2
import numpy as np

# Abrir la camara 
video = cv2.VideoCapture(0)

# Convertir el cuadro de BGR a HSV
frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

 #  rango de color rojo en HSV
bajo_rojo1 = np.array([0, 40, 40])
alto_rojo1 = np.array([10, 255, 255])
bajo_rojo2 = np.array([160, 40, 40])
alto_rojo2 = np.array([180, 255, 255])

 #   mascara para el color rojo
mascara_rojo1 = cv2.inRange(frame_hsv, bajo_rojo1, alto_rojo1)
mascara_rojo2 = cv2.inRange(frame_hsv, bajo_rojo2, alto_rojo2)
mascara_rojo = cv2.add(mascara_rojo1, mascara_rojo2)
 #cuadro original a escala de grises
frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
#  imagen gris a un formato BGR 
frame_gris_bgr = cv2.cvtColor(frame_gris, cv2.COLOR_GRAY2BGR)
    
# combinar el cuadro en gris con las areas en rojo
resultado = np.where(mascara_rojo[:, :, None] == 255, frame, frame_gris_bgr)

cv2.imshow('Color resaltadoo', resultado)
cv2.waitKey(0)
 
video.release()
cv2.destroyAllWindows()
