# Practica Mascara
Para esta practica el profe nos pidio crear una mascara estilo snapchat 

### Importaciones
```python
import numpy as np
import cv2 as cv
```

### Cargar el clasificador de rostros y la mascara

**rostro**: Se carga un clasificador Haar preentrenado para detectar rostros en la imagen o el video. El archivo `haarcascade_frontalface_alt2.xml` es el clasificador utilizado.
**cap**: Se inicia la captura de video desde la camara .
**mascara**: Se carga la imagen de la mascara que se usara  con el flag `cv.IMREAD_UNCHANGED` para que se mantenga la transparencia.

```python
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)
mascara = cv.imread('mascara.png', cv.IMREAD_UNCHANGED)
```


### Bucle principal para procesar cada fotograma del video

**ret, frame**: Se lee el siguiente fotograma del video.
**gray**: El fotograma se convierte a escala de grises, ya que el clasificador Haar funciona mejor con imagenes en blanco y negro.
**rostros**: La funcion `detectMultiScale` detecta los rostros en la imagen. Devuelve una lista de rectangulos que indican la ubicacion de los rostros detectados.

```python
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
```

### Redimensionar la máscara y superponerla

**(x, y, w, h)**: Para cada rostro detectado, se obtiene la posicion `(x, y)` y las dimensiones `(w, h)` del rectangulo delimitador.
**resized_mascara**: La imagen de la mascara se redimensiona para que encaje en el rectangulo detectado para el rostro. El tamaño de la mascara se ajusta a las dimensiones del rostro.

```python
for (x, y, w, h) in rostros:
    resized_mascara = cv.resize(mascara, (w, h))
```


### Manejo de la transparencia

**if resized_mascara.shape[2] == 4**: Si la mascara tiene un canal alfa, se separa en sus componentes: **b, g, r** (colores) y **alpha** (transparencia).
**overlay_color**: Se reconstruye la imagen sin el canal alfa (solo colores).
**mask_inv**: Se crea una mascara invertida a partir del canal alfa, que se usará para combinar la imagen de la mascara con el fondo.

```python
if resized_mascara.shape[2] == 4:
    b, g, r, alpha = cv.split(resized_mascara)
    overlay_color = cv.merge((b, g, r))
    mask_inv = cv.bitwise_not(alpha)
else:
    overlay_color = resized_mascara
    mask_inv = np.ones((h, w), dtype="uint8") * 255
```

### Superponer la mascara sobre el rostro detectado

 **roi**: Se extrae la region del fotograma que corresponde al rostro detectado.
 **background**: Se crea el fondo de la region utilizando la mascara invertida .
 **foreground**: Se crea la parte frontal con la mascara.
 **combined**: Se combinan el fondo y el primer plano para superponer la mascara en la region seleccionada.

```python
roi = frame[y:y+h, x:x+w]
background = cv.bitwise_and(roi, roi, mask=mask_inv)
foreground = cv.bitwise_and(overlay_color, overlay_color, mask=alpha if resized_mascara.shape[2] == 4 else mask_inv)
combined = cv.add(background, foreground)
frame[y:y+h, x:x+w] = combined
```

### Mostrar el resultado
```python
cv.imshow('rostros', frame)
k = cv.waitKey(1)
if k == 27:  
    break
```


### Mostando Resultado
![Mascara Master chief](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/mascaraMuestra.png?raw=true)

