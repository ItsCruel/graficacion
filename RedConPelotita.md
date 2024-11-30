# Practica Flujo Optico

Esta practica se realizo para el seguimiento de puntos mediante flujo optico utilizando el algoritmo de **Lucas-Kanade**.

### 1. **Importamos las Bibliotecas**
```python
import numpy as np
import cv2 as cv
```

### 2. **Inicializamos la Captura de Video**
```python
cap = cv.VideoCapture(0)
```

### 3. **Parametros del Algoritmo Lucas-Kanade**
- `winSize`: Tamaño de la ventana para buscar coincidencias.
- `maxLevel`: Niveles de la pirámide para el analisis.
- `criteria`: Condiciones de parada para el algoritmo basadas en iteraciones y precision.

```python
lkparm = dict(winSize=(15, 15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
```

---

### 4. **Captura del Primer Cuadro y Conversion a Escala de Grises**
`cv.cvtColor`: Convierte la imagen capturada a escala de grises.

```python
_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
```


### 5. **Definicion de la Cuadricula de Puntos Iniciales**
- Se define una cuadricula de puntos `(x, y)` de tamaño fijo.
- `np.float32`: Convierte los puntos a formato de coma flotante requerido por OpenCV.

```python
p0 = np.array([(100, 100), (200, 100), ..., (500, 400)])
p0 = np.float32(p0[:, np.newaxis, :])
```


### 6. **Mascara para el Dibujo**
Se inicializa una mascara negra del mismo tamaño que el cuadro para superponer el flujo optico.

```python
mask = np.zeros_like(vframe)
```


### 7. **Bucle Principal del Procesamiento de Cuadros**
Se lee cada cuadro y se convierte a escala de grises para el procesamiento.

```python
while True:
    _, frame = cap.read()
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
```


### 8. **Calculo del Flujo Optico**
`cv.calcOpticalFlowPyrLK`: Calcula el flujo óptico entre `vgris` (cuadro anterior) y `fgris` (cuadro actual).

```python
p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)
```

### 9. **Dibujo de la Red de Puntos**
Se dibujan lineas que conectan los puntos adyacentes horizontal y verticalmente.

```python
for i in range(len(p1)):
    x1, y1 = int(p1[i][0][0]), int(p1[i][0][1])
```

### 10. **Mostrar el Video Procesado**
`cv.imshow`: Muestra el video con las lineas de flujo optico.

```python
cv.imshow('ventana', frame)
if (cv.waitKey(1) & 0xff) == 27:
    break
```

### Mostrando Resultados
![RedConPelotita]()


