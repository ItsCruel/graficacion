# Practica PelotaCon Selectores

## Introduccion
Este codigo crea una animacion sencilla donde una pelotita se mueve y rebota en los bordes de la ventana, y muestra en que sector se encuentra.

### Importamos las  bibliotecas
paso 0 importamos las librerias numpy y cv
```python
import numpy as np
import cv2 as cv
```

### Configuración de la ventana y variables de animacion

```python
# dimensiones de la ventana
ancho, alto = 640, 480

# crear ventana
cv.namedWindow("Animacion", cv.WINDOW_AUTOSIZE)
``` 

# posicion inicial de la pelota
Dimensiones de la ventana: se definen `ancho` y `alto` (640 x 480). Creamos de ventana con `cv.namedWindow`con nombre "Animacion"
Definimos la posicion y velocidad inicial de la pelota:  `pos_pelota`: array NumPy que define la posicion inicial de la pelota en coordenadas `[x, y]`.
  De ninimos el `radio_pelota y velocidad`: con un array con la velocidad en los ejes `x` y `y` (`[5, 3]`). Asi como el color de la pelota con  formato BGR (`(255, 0, 0)`), que es azul.

```
pos_pelota = np.array([100, 100]) 
radio_pelota = 20
velocidad = np.array([5, 3])

# color fijo de la pelota
color_pelota = (255, 0, 0)
```

### Bucle de animacion

Definimos: 
**Fondo**: un fondo negro (`fotograma`) usando `np.zeros` con las dimensiones de la ventana y tipo `uint8`.
**Divisiones de sectores**: Se dibujan dos lineas (horizontal y vertical) para dividir la ventana en cuatro sectores usando `cv.line`.
 Color de las líneas : blanco (`(255, 255, 255)`).

```python
while True:
    # Crear fondo
    fotograma = np.zeros((alto, ancho, 3), dtype=np.uint8)
    
    # dibujar divisiones para los sectores
    cv.line(fotograma, (ancho // 2, 0), (ancho // 2, alto), (255, 255, 255), 2)
    cv.line(fotograma, (0, alto // 2), (ancho, alto // 2), (255, 255, 255), 2)
```
### Deteccion de sectores
Dependiendo de  la posicion de la pelota (`pos_pelota`), se determina en que cuadrante de la ventana se encuentra:
    Sector 1: esquina superior izquierda.
    Sector 2: esquina superior derecha.
    Sector 3: esquina inferior izquierda.
    Sector 4: esquina inferior derecha.

```python
    # determinar el sector en el que se encuentra la pelota
    if pos_pelota[0] < ancho // 2 and pos_pelota[1] < alto // 2:
        sector = 1
    elif pos_pelota[0] >= ancho // 2 and pos_pelota[1] < alto // 2:
        sector = 2
    elif pos_pelota[0] < ancho // 2 and pos_pelota[1] >= alto // 2:
        sector = 3
    else:
        sector = 4
```


### Dibujo de la pelota y sector actual

**Dibujo de la pelota**: `cv.circle` dibuja la pelota en `pos_pelota`, con el color y radio definidos.
Texto del sector: cv.putText` muestra el texto `"Sector: X"` en la parte superior izquierda de la ventana.

```python
    # Dibujar la pelotita
    cv.circle(fotograma, tuple(pos_pelota), radio_pelota, color_pelota, -1)
    
    # Mostrar el sector en el que se encuentra la pelotita
    texto_sector = f"Sector: {sector}"
    cv.putText(fotograma, texto_sector, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
```

### Actualizacion de la posicion y colision con bordes

```python
    # Actualizar la posicion de la pelota
    pos_pelota += velocidad
    
    # Comprobar colisiones y cambiar direccion
    if pos_pelota[0] - radio_pelota <= 0 or pos_pelota[0] + radio_pelota >= ancho:
        velocidad[0] = -velocidad[0]

    if pos_pelota[1] - radio_pelota <= 0 or pos_pelota[1] + radio_pelota >= alto:
        velocidad[1] = -velocidad[1]
```

 **Actualizacion de la posicion** :  La posicion de la pelota (`pos_pelota`) se incrementa en cada bucle, sumando el valor de `velocidad`.
 **Colision con los bordes**:  Se verifica si la pelota toca alguno de los bordes y, si es asi, se invierte la direccion .


### Mostrar la imagen y salida

```python
    # Mostrar la imagen en la ventana
    cv.imshow("Animacion", fotograma)

    # Salir al presionar 'Esc'
    if cv.waitKey(1) & 0xFF == 27:
        break
```

### Mostrando Resultados 
![Pelotita Con Sectores](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/ImagenPelotitaConSectores.png?raw=true)
