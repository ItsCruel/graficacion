# Practica Filtro de ojos tipo SnapChat

Este código se utiliza para detectar ojos en un video en tiempo real desde la camara, y luego superpone una imagen de una mascara de ojos sobre la region detectada.

### Librerias
paso 0 como simepre importamos el open cv y el numpy

```python
import numpy as np
import cv2 as cv
```

### Cargar el clasificador de ojos y la mascara

**ojos_cascade**: Se carga un clasificador Haar preentrenado para detectar ojos en la imagen o el video.
**mascara**: Se carga la imagen que se usara como la mascara. Se usa el flag `cv.IMREAD_UNCHANGED` para mantener la transparencia .

```python
ojos_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')
mascara = cv.imread('ojos1.png', cv.IMREAD_UNCHANGED)
```

### Configuracion de la camara
**cap**: Se inicia la captura de video desde la cámara web (índice `0` indica la camara predeterminada).

```python
cap = cv.VideoCapture(0)
```

### Bucle principal para procesar cada fotograma del video
**ret, frame**: Se lee el siguiente fotograma del video.
**gray**: El fotograma se convierte a escala de grises, ya que el clasificador Haar funciona mejor con imágenes en blanco y negro.
**ojos**: La funcion `detectMultiScale` detecta los ojos en la imagen (en escala de grises). Devuelve una lista de rectangulos donde se encuentran los ojos detectados.

```python
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ojos = ojos_cascade.detectMultiScale(gray, 1.3, 5)
```

### Ajustar la mascara de los lentes y superponerla
**(x, y, w, h)**: Para cada ojo detectado, se obtiene la posicion `(x, y)` y las dimensiones `(w, h)` del rectangulo delimitador.
**width_ratio**: Se establece un factor de escala para aumentar el ancho de la mascara.
**new_w** y **new_h**: Se calculan las nuevas dimensiones de la mascara con el factor de escala.
**resized_mascara**: La imagen de la mascara se redimensiona para que encaje en el rectangulo detectado para el ojo.

```python
for (x, y, w, h) in ojos:
    width_ratio = 1.8  
    new_w = int(w * width_ratio)
    new_h = int(new_w * mascara.shape[0] / mascara.shape[1])
    resized_mascara = cv.resize(mascara, (new_w, new_h))
```

### Calcular la posición de la mascara
**y_offset** y **x_offset**: Se calculan los desplazamientos para centrar la máscara sobre el area de los ojos detectados.

```python
y_offset = int(y - new_h / 2)
x_offset = x - int((new_w - w) / 2)
```

### Manejo de la transparencia
```python
if resized_mascara.shape[2] == 4:
    b, g, r, alpha = cv.split(resized_mascara)
    overlay_color = cv.merge((b, g, r))
    mask_inv = cv.bitwise_not(alpha)
else:
    overlay_color = resized_mascara
    mask_inv = np.ones((new_h, new_w), dtype="uint8") * 255
```

### Superponer la mascara sobre el video
**roi**: Se extrae la region del fotograma donde se colocara la mascara.
**background**: Se crea el fondo de la region usando `mask_inv` para que el fondo no se vea afectado.
**foreground**: Se crea la parte frontal con la mascara (con o sin transparencia).
**combined**: Se combinan el fondo y el primer plano para superponer la mascara en la region seleccionada.

```python
roi = frame[y_offset:y_offset + new_h, x_offset:x_offset + new_w]

if roi.shape[0] == new_h and roi.shape[1] == new_w:
    background = cv.bitwise_and(roi, roi, mask=mask_inv)
    foreground = cv.bitwise_and(overlay_color, overlay_color, mask=alpha if resized_mascara.shape[2] == 4 else mask_inv)
    combined = cv.add(background, foreground)
    frame[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = combined
```

### Mostrar el resultado
```python
cv.imshow('Lentes', frame)
if cv.waitKey(1) & 0xFF == 27: 
    break
```

### Mostrando Resultados
![Filtro ojos]()


