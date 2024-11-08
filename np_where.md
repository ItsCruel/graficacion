##Practica NP Where Foto
parte 0 comi siempre importamos las librerias
```python
import cv2
import numpy as np

# importamos la  imagen en formato RGB
imagen = cv2.imread('halo2.png', 1)
```
convertimos RGB a HSV

```python
# Convertir la imagen de RGB a HSV
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
```
 HSV (Tono, Saturación, Valor), que facilita la segmentacion de colores específicos como el rojo.

```python
# Definir el rango de color rojo en HSV tanto los rojos de la escala de color de la izquierda como el rojo de la derecha 
bajo_rojo1 = np.array([0, 40, 40])
alto_rojo1 = np.array([10, 255, 255])
bajo_rojo2 = np.array([160, 40, 40])
alto_rojo2 = np.array([180, 255, 255])
```
![Rojos](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/rojos1.png?raw=true)
