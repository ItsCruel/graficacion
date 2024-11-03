**Practica 5**

***Instrucciones***
Crear un dibujo mediante primitivas de dibujo utilizando OpenCV

***Descripción***
Para este codigo utilizaremos  OpenCV para dibujar una figura simple de un monito utilizando formas geometricas bsicas como circulos rectangulos y lineas.

Con estas  lineas importamos las bibliotecas:
- cv2: Para manipulación de imagenes con OpenCV.
- numpy: Para crear y manejar arrays numericos, que se utilizan aqui para definir la imagen.

python
import cv2
import numpy as np


como primer paso para hacer un contraste creamos  una imagen en blanco de 500x500 pixeles y 3 canales de color (BGR, cada uno de 8 bits utilizando uint8).
python
imagen = np.zeros((500, 500, 3), dtype="uint8")

para hacer la cabeza de nuestro monito realizamos un círculo 
python
cv2.circle(imagen, (250, 150), 50, (255, 0, 0), -1)

**como se creo el circulo**
 (250, 150): Coordenadas del centro del círculo.
 50: Radio del circulo.
(255, 0, 0): Color azul (en formato BGR, es decir, 255 en el canal azul, 0 en los otros).
 -1: Indica que el círculo debe rellenarse completamente.

 como segundo paso ocupamos un cuerpo  , para esto utilizamos un rectangulo 
python
cv2.rectangle(imagen, (220, 200), (280, 350), (255, 0, 0), -1)

***Desglosando como se creo el rectangulo***
 (220, 200): Coordenadas de la esquina superior izquierda.
(280, 350): Coordenadas de la esquina inferior derecha.
(255, 0, 0): Color azul , como en el circul
 -1: Indica que el rectangulo debe rellenarse completamente.


como siguiente parte dibujamos los brazos
python
cv2.line(imagen, (220, 220), (150, 300), (255, 0, 0), 5)
cv2.line(imagen, (280, 220), (350, 300), (255, 0, 0), 5)

***creacion de los brazos***
Dibuja dos líneas que representan los brazos de la figura:
 Primer brazo: Línea de (220, 220) a (150, 300) (izquierda).
 Segundo brazo: Línea de (280, 220) a (350, 300) (derecha).
(255, 0, 0): Color azul.

como siguiente parte dibujamos las piernas 
python
cv2.line(imagen, (240, 350), (200, 450), (255, 0, 0), 5)
cv2.line(imagen, (260, 350), (300, 450), (255, 0, 0), 5)

***creacion las piernas***
Dibuja dos líneas que representan las piernas de la figura:
 Primer pierna: Línea de (240, 350) a (200, 450) (izquierda).
 Segunda pierna: Línea de (260, 350) a (300, 450) (derecha).
(255, 0, 0): Color azul.
 5: Grosor de la línea.

Mostrar la imagen
python
cv2.imshow('Persona', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()

***RESULTADO***
El resultado es una figura de "persona" en color azul compuesta por un circulo para la cabeza, un rectángulo para el cuerpo, y lineas para los brazos y piernas.
cv2.imshow('Persona', imagen): Muestra la imagen 
![Persona con primitivas](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/persona.png?raw=true)

