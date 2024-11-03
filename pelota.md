**Practica Pelota**
**Introduccion**
Este codigo se trata de una  animacion sencilla donde una pelota rebota dentro de una ventana usando la biblioteca OpenCV. 

1. como parte 1 configuramos la ventana y variables
importamos las librerias
python
import cv2
import numpy as np

# seleccionamos las dfimensiones de la ventana
ancho, alto = 640, 480

# ceamos la  ventana
cv2.namedWindow("Animacion", cv2.WINDOW_AUTOSIZE)


- *Dimensiones de la ventana*: Definimos  las variables ancho y alto para especificar el tamaño de la ventana de animacion, en este caso, 640x480 pixeles.