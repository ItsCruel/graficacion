### Practica 3
para esta practica el profe pido que aplicaramos las transformaciones vistas en clase

```python
import cv2 as cv
import numpy as np
import math
```
- **Importamos las librerias**: 
  `cv2`: Para manejar imagenes usando OpenCV.
  `numpy`: Para crear y manipular matrices.
  `math`: Para funciones matematicas, como la conversion de angulos a radianes.


#### **Carga de la Imagen**
cargamos la imagen en este caso volvere a usar la llamada halo2
**Verificacion de carga**: Si la imagen no se carga correctamente, se muestra un mensaje de error y se detiene la ejecucion.

```python
img = cv.imread('halo2.png', 0)
if img is None:
    print("Error al cargar la imagen.")
    exit()
```


#### **Obtencion del Tamaño de la Imagen**
 **`shape`**: Devuelve las dimensiones (alto y ancho) de la imagen.

```python
x, y = img.shape
```

### **Transformaciones Geometricas**

#### 1. Traslacion

**Definicion del desplazamiento**: `dx` y `dy` especifican el desplazamiento en las direcciones `x` e `y`, respectivamente.
**Traslacion**: Se calcula el nuevo índice para cada pixel, desplazandolo segun `dx` y `dy`.

```python
dx, dy = 100, 50
translated_img = np.zeros((x, y), dtype=np.uint8)
for i in range(x):
    for j in range(y):
        new_x = i + dy
        new_y = j + dx
        if 0 <= new_x < x and 0 <= new_y < y:
            translated_img[new_x, new_y] = img[i, j]
```


#### 2. Rotacion

**Angulo de rotacion**: Se define en grados y se convierte a radianes.
**Calculo del centro**: `cx` y `cy` representan el centro de la imagen.
**Transformación**: Se aplican formulas de rotacion para obtener las nuevas coordenadas.

```python
angle = 45
theta = math.radians(angle)
rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)
cx, cy = x // 2, y // 2
for i in range(x):
    for j in range(y):
        new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx + x//2)
        new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy + y//2)
        if 0 <= new_x < 2*y and 0 <= new_y < 2*x:
            rotated_img[new_y, new_x] = translated_img[i, j]
```


#### 3. Escalamiento

**Factores de escala**: `scale_x` y `scale_y` definen cuanto se ampliara la imagen.
**Transformación**: Se calculan las nuevas posiciones de pixeles según el factor de escala.

```python
scale_x, scale_y = 2, 2
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)
for i in range(x):
    for j in range(y):
        new_x = int(i * scale_y)
        new_y = int(j * scale_x)
        if new_x < scaled_img.shape[0] and new_y < scaled_img.shape[1]:
            scaled_img[new_x, new_y] = rotated_img[i, j]
```


### Resultados
```python
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Trasladada', translated_img)
cv.imshow('Imagen Rotada', rotated_img)
cv.imshow('Imagen Escalada', scaled_img)
cv.waitKey(0)
cv.destroyAllWindows()
```

### Mostrando Resultados
![Imagen Original]()
![Traslacion]()
![Rotacion]()
![Escalamiento]()
