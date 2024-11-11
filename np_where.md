## Practica NP Where Foto

### Instrucciones 
Para esta practica crearemos un filtro de imagen que resaltara las imagenes color rojo, por medio de una foto , yo use una de halo.

parte 0 como siempre importamos las librerias
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


Se define los dos rangos para el color rojo en HSV. Como el rojo esta en los extremos del espectro de matiz, se define en dos partes:
- `bajo_rojo1` a `alto_rojo1` cubre tonos rojos de 0° a 10°.
- `bajo_rojo2` a `alto_rojo2` cubre tonos de 160° a 180°.

y creamos unas mascaras para el rojo 

```python
# Crear una mascara para el color rojo
mascara_rojo1 = cv2.inRange(imagen_hsv, bajo_rojo1, alto_rojo1)
mascara_rojo2 = cv2.inRange(imagen_hsv, bajo_rojo2, alto_rojo2)
mascara_rojo = cv2.add(mascara_rojo1, mascara_rojo2)
```

Genera dos mascaras para los tonos de rojo definidos anteriormente. `cv2.inRange()` convierte pixeles que estan dentro del rango en blanco (255) y los fuera del rango en negro (0). Luego, combina ambas mascaras (`mascara_rojo1` y `mascara_rojo2`) en una sola (`mascara_rojo`) usando `cv2.add()`.

```python
# Convertir la imagen original a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
```
Convierte la imagen original a escala de grises, almacenandola en `imagen_gris`.

```python
# Convertir la imagen gris a un formato BGR para que coincida con la original
imagen_gris_bgr = cv2.cvtColor(imagen_gris, cv2.COLOR_GRAY2BGR)
```
convertimos  `imagen_gris` a un formato BGR para que tenga el mismo numero de canales que la imagen original, facilitando la combinacion de ambas.

```python
# Combinar la imagen en gris con las areas en rojo
resultado = np.where(mascara_rojo[:, :, None] == 255, imagen, imagen_gris_bgr)
```
Utiliza `np.where()` para combinar las areas rojas con la imagen en escala de grises. La condición `mascara_rojo[:, :, None] == 255` aplica la mascara en cada canal de color (BGR) y selecciona:
- Los pixeles de la imagen original en las areas rojas.
- Los pixeles en escala de grises en el resto de la imagen.

```python
# Mostrar la imagen final
cv2.imshow('Color resaltado', resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Mostrando Resultados**
<p>
![.](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/halo2.png?raw=true)
</p>
![.](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/imagenNPWHERE%20Foto.png?raw=true)