##Practica MatrizSobel
 como paso 0 : importamos las librerias correspondientes 
```python
import cv2 as cv
import numpy as np
```
El codigo utiliza las librerias `cv2` de OpenCV para procesamiento de imagenes y `numpy` para manejar arreglos de datos.

#### cargamos la imagen en escala de grises
```python
imagen = cv.imread('espartan.jpg', 0)
```

#### obtenemos el  tamaño de la imagen original
```python
alto, ancho = imagen.shape
```
