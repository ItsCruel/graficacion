Practica Matriz Convolucion
INTRODUCCION
En esta practica lo que buscamos es aplicar la matriz convolucion que se encargara de aplicar un suavizadoen la imagen , que en este caso es espartan.

Como paso 0 importamos las librerias correspondientes

```
import cv2 as cv
import numpy as np
```

 Cargamos y procesamos la Imagen ,se carga la imagen `spartan.png` en escala de grises. El parametro `0` indica que la imagen se leera en escala de grises.

```
# Cargar la imagen en escala de grises
imagen = cv.imread('spartan.png', 0)
```
Se obtienen las dimensiones de la imagen original (`alto` y `ancho`).

```
# Obtener el tamaño de la imagen
alto, ancho = imagen.shape
```


### Definimos la escala de aumento , se define un factor de escala de `2` en ambos ejes, lo cual duplicara el tamaño de la imagen.

```
# Definir el factor de escala
escala_x, escala_y = 2, 2
```

### Crear una Imagen Escalada

Se crea una matriz vacia `imagen_escalada` para almacenar la imagen aumentada. La nueva imagen tiene dimensiones el doble de la original y esta inicializada con ceros .





```
# Crear una nueva imagen para almacenar el escalado
imagen_escalada = np.zeros((int(alto * escala_y), int(ancho * escala_x)), dtype=np.uint8)
```
se copia cada pixel de la imagen original a una posicion escalada en `imagen_escalada`. Los indices de la imagen escalada se multiplican por el factor de escala para duplicar la distancia entre pixeles, logrando el aumento en tamaño.

```
# Aplicar el escalado
for i in range(alto):
    for j in range(ancho):
        imagen_escalada[i * escala_y, j * escala_x] = imagen[i, j]
```


### Aplicar Filtro de Suavizado 1/9

```
# Obtener el tamaño de la imagen escalada
alto_escalado, ancho_escalado = imagen_escalada.shape
```

Se obtienen las dimensiones de la imagen escalada. Se inicia un bucle para aplicar un filtro de suavizado en la imagen escalada. `valor` es una variable que acumulara el promedio de los pixeles vecinos.

```
# Aplicar la matriz de suavizado 1/9
for i in range(alto_escalado):
    for j in range(ancho_escalado):
        valor = 0
```



### Sumar los Píxeles Vecinos

Se calcula la suma de los valores de los pixeles vecinos en una matriz de 3x3. Cada valor se multiplica por `1/9` para obtener el promedio.
Aqui, por ejemplo, se verifica el pixel superior izquierdo `(i-1, j-1)`. Si esta fuera de los límites de la imagen, `vecino` se asigna a `0`. Esto se repite para cada vecino en la matriz 3x3.





```
        if (i - 1) < 0 or (j - 1) < 0:
            vecino = 0
        else:
            vecino = int(imagen_escalada[i - 1][j - 1])
        valor += vecino * (1 / 9)
```


### Suavizado Completo

El mismo proceso se aplica para los ocho vecinos y el pixel central `(i, j)`. Luego, el valor acumulado en `valor` representa el promedio. Aquí se asegura que `valor` este dentro del rango permitido de 0 a 255 para evitar desbordamientos.

```
        valor = min(max(int(valor), 0), 255)
```


Por ultimo se asigna `valor` al píxel `(i, j)` en `imagen_escalada`, completando el suavizado.

```
        imagen_escalada[i][j] = valor
```


### Mostrar la Imagen
Se muestran la imagen original y la imagen escalada con suavizado aplicado. 

cierra el programa
```
# Mostrar la imagen original y la imagen escalada
cv.imshow('Imagen Original', imagen)
cv.imshow('Imagen Escalada (modo raw)', imagen_escalada)
cv.waitKey(0)
cv.destroyAllWindows()
```

Mostrando resultados 

![Espartan_Original](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/espartan.jpg?raw=true)
<p>
![Espartan_Convolucion](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/suavizado_convolucion.png?raw=true)
</p>