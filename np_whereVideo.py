import cv2
import numpy as np

# Abrir la camara 
video = cv2.VideoCapture(0)

# Convertir el cuadro de BGR a HSV
frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)