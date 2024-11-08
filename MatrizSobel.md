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
obtienemos el alto y el ancho de la imagen en pixeles.

#### Definimos el factor de escala
```python
escala_x, escala_y = 2, 2
```

#### Creamos la imagen escalada
```python
ImagenEscalada = np.zeros((int(alto * escala_y), int(ancho * escala_x)), dtype=np.uint8)
```

como parte intermedia creamos una nueva imagen vacia con dimensiones aumentadas segun el factor de escala, inicializando sus valores en `0` (negro) y se escala la imagen duplicando pixeles
```python
for i in range(alto):
    for j in range(ancho):
        ImagenEscalada[i * escala_y, j * escala_x] = imagen[i, j]
```
Este ciclo anidado o bucle recorre cada pixel de la imagen original y asigna su valor al pixel correspondiente en la imagen escalada, duplicando así su tamaño. Nuevamente  obtenemos el tamaño  pero ahora es de la imagen escalada
```python
alto_escalado, ancho_escalado = ImagenEscalada.shape
```


Almacenamos las nuevas dimensiones de la imagen escalada.

#### Aplicacion de la matriz de Sobel para la deteccion de bordes
```python
for i in range(alto_escalado):
    for j in range(ancho_escalado):
        gradiente = 0
```
Se recorre cada pixel de la imagen escalada, calculando el valor del gradiente en cada posicion usando el operador de Sobel.

1. **Gradiente Sobel en direccion horizontal**: Cada posicion del pixel multiplica su valor por un peso segun la matriz de Sobel. Los casos de borde se manejan con condiciones `if` para evitar errores de indice.
   
2. **Suma de valores de gradiente**: Se calculan y suman valores segun los vecinos horizontales y verticales.

```python
        # Limitar los valores
        if gradiente > 255:
            gradiente = 255
        if gradiente < 0:
            gradiente = 0
```
Se limita el valor de `gradiente` para que esté entre `0` y `255`, manteniendolo dentro del rango de los pixeles de una imagen en escala de grises.

```python
        ImagenEscalada[i][j] = int(gradiente)
```
Se asigna el valor de gradiente calculado al pixel correspondiente en `ImagenEscalada`.

#### Mostrar las imagenes
```python
cv.imshow('Imagen original', imagen)
cv.imshow('Imagen escalada', ImagenEscalada)
cv.waitKey(0)
cv.destroyAllWindows()
```
Como parte final se muestran las ventanas de la imagen original y la imagen escalada con bordes detectados. al final el programa espera que escribas 0 o Esc para cerrar las ventanas y finalizar el programa. 
