## Practica conteo objetos por Color
para esta practica el profe nos pidio que fuera el programa fuera capaz de contar cuantos objetos de color hay en una imagen que el nos proporcion

## Paso 0
como siempre nuestro paso 0 importar nuestras 2 librerias numpy y open cv
```python
import cv2
import numpy as np
```
### 1. **Carga y Preprocesamiento de la Imagen**

Se carga la imagen `salida.png`.
 Se convierte la imagen del espacio de color **BGR** a **HSV** para facilitar la segmentacion por colores.

```python
image = cv2.imread('salida.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
```


### 2. **Definicion de Rangos de Colores en HSV**
Se definen rangos para diferentes colores usando limites inferiores y superiores en el espacio HSV:

**Rojo**: Dos rangos para cubrir las tonalidades de rojo.

```python
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])
```

**Azul**
```python
lower_blue = np.array([100, 120, 70])
upper_blue = np.array([140, 255, 255])
```

 **Verde** 
```python
lower_green = np.array([35, 120, 70])
upper_green = np.array([85, 255, 255])
```

**Naranja**
```python
lower_orange = np.array([10, 120, 70])
upper_orange = np.array([30, 255, 255])
```
**Rosa**
```python
lower_pink = np.array([140, 120, 70])
upper_pink = np.array([170, 255, 255])
```

- Se crean mascaras binarias para cada color que identifican píxeles dentro del rango de color definido.

### 3. **Creacion de Mascaras de Colores**
```python
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask_red = cv2.bitwise_or(mask_red1, mask_red2)
```


### 4. **Procesamiento Morfologico**
 Se aplica una operacion morfologica **CLOSE** para cerrar pequeños huecos dentro de las regiones detectadas.

```python
kernel = np.ones((5, 5), np.uint8)
morph_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
```


### 5. **Deteccion de Contornos**
- Se detectan los contornos externos de las areas segmentadas.

```python
contours, _ = cv2.findContours(morph_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```


### 6. **Conteo de Objetos por Color**
 Se define una funcion para contar objetos usando la cantidad de contornos detectados por cada mascara de color.

```python
def count_objects_by_color(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)
```


### 7. **Impresión de Resultados**
Se imprimen los totales de objetos detectados por cada color.

```python
print(f"Objetos Rojos: {red_count}")
print(f"Objetos Azules: {blue_count}")
print(f"Objetos Verdes: {green_count}")
print(f"Objetos Naranjas: {orange_count}")
print(f"Objetos Rosas: {pink_count}")
```


### 8. **Visualizacion de la Imagen con Contornos**

Se dibujan los contornos detectados en la imagen original.
Se muestra la imagen resultante con los objetos detectados en verde.

```python
cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)
cv2.imshow("Detected Objects", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Conclusion 
Como conclusion el resultado fue erroneo y no logre la deteccion de border con el uso del operador and y tuve que recurrir a contours para detectar el borde de las islas , lo que logro el fallo del conteo por mas que segmentara el color
![]()

### Mostrando Resultados

![]()
![]()

