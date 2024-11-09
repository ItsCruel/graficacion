## Practica NP WHERE VIDEO

### Instrucciones
para esta practica crearemos un filtro np where en el cual buscaremos un color y lo resaltaremos , el profesor uso verde pero yo usare el color rojo.

Como parte 0 importamos las librerias

```python
import cv2
import numpy as np
```


### 1.Abrimos la camara,  buscamos la primera camara que aparezca con el 0.

```python
video = cv2.VideoCapture(0)
```

### 2. captura de un cuadro y conversion de Color al mismo tiempo , como lo hacia el np where de foto pero ahora en video

```python
ret, frame = video.read()
frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

- `ret, frame = video.read()`: lee un cuadro de la camara. `frame` contiene la imagen capturada.
- `cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)`: Convierte la imagen de BGR (el formato de color de OpenCV) a HSV. el HSV facilita el filtrado de colores.



### 3. Definimos  del Rango de Color Rojo

```python
bajo_rojo1 = np.array([0, 40, 40])
alto_rojo1 = np.array([10, 255, 255])
bajo_rojo2 = np.array([160, 40, 40])
alto_rojo2 = np.array([180, 255, 255])
```

- Definimos dos rangos en HSV para el color rojo:
  - **bajo_rojo1 y alto_rojo1**: Capturan tonos de rojo en el rango de 0 a 10 grados.
  - **bajo_rojo2 y alto_rojo2**: Capturan tonos de rojo en el rango de 160 a 180 grados.
- Esto es necesario porque el rojo en HSV aparece en dos extremos del espectro de color.
![Rojos](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/rojos1.png?raw=true)


### 4. Creamos las  mascaras para el color Rojo

```python
mascara_rojo1 = cv2.inRange(frame_hsv, bajo_rojo1, alto_rojo1)
mascara_rojo2 = cv2.inRange(frame_hsv, bajo_rojo2, alto_rojo2)
mascara_rojo = cv2.add(mascara_rojo1, mascara_rojo2)
```

- `cv2.inRange()`: Crea una mascara binaria donde los pixeles dentro del rango se muestran como blancos (255) y los fuera del rango como negros (0).
  - `mascara_rojo1` y `mascara_rojo2` son las mascaras para los rangos de color rojo definidos.
- `cv2.add()`: Combina las dos mascaras para obtener una mascara final `mascara_rojo` que abarca todos los tonos de rojo.




### 5.  Convercion a Escala de Grises

```python
frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame_gris_bgr = cv2.cvtColor(frame_gris, cv2.COLOR_GRAY2BGR)
```

- `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`: Convierte el cuadro original a escala de grises.
- `cv2.cvtColor(frame_gris, cv2.COLOR_GRAY2BGR)`: Convierte la imagen en escala de grises de vuelta a formato BGR para poder combinarla con la imagen en color en el siguiente paso.



### 6. Combinacion de la Imagen en Grises con el Color Rojo

```python
resultado = np.where(mascara_rojo[:, :, None] == 255, frame, frame_gris_bgr)
```

- `np.where(mascara_rojo[:, :, None] == 255, frame, frame_gris_bgr)`: Combina la imagen en escala de grises con el cuadro en color:
  - `mascara_rojo[:, :, None] == 255`: Marca las areas rojas de la mascara.
  - Si el pixel es rojo (valor 255 en la máscara), toma el color de `frame`; si no, usa el valor en escala de grises de `frame_gris_bgr`.



### 7. Mostrar el Resultado 
solo queda mostrar el resultado . La imagen final que combina las areas en rojo sobre una imagen en escala de grises.

```python
cv2.imshow('Color resaltado', resultado)
```

Mostrando resultado
