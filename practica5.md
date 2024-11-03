**Practica 5**

***Instrucciones***
Crear un dibujo mediante primitivas de dibujo utilizando OpenCV

***Descripción***
Para este codigo utilizaremos  OpenCV para dibujar una figura simple de un monito utilizando formas geométricas bsicas como circulos rectangulos y lineas.

Con estas  lineas importamos las bibliotecas:
- cv2: Para manipulación de imagenes con OpenCV.
- numpy: Para crear y manejar arrays numericos, que se utilizan aqui para definir la imagen.

python
import cv2
import numpy as np


como primer paso para hacer un contraste creamos  una imagen en blanco de 500x500 pixeles y 3 canales de color (BGR, cada uno de 8 bits utilizando uint8).
python
imagen = np.zeros((500, 500, 3), dtype="uint8")
