

# Practica Pelota Colisión

## Introduccion

Una de las pelotitas se mueve automaticamente, mientras que la otra se reposiciona a una ubicacion aleatoria cuando están cerca.

Como paso 0 importamos las librerias de siempre numpy y cv

```python
import cv2
import numpy as np 
```


### Definimos dimensiones de la ventana
Se establecen el ancho (`w`) y alto (`h`) de la ventana de animacion en 640x480 pixeles.

```python
w, h = 640, 480
```

### Creamos la  ventana
Se crea una ventana llamada `"Anim"` con tamaño automatico.


```python
cv2.namedWindow("Anim", cv2.WINDOW_AUTOSIZE)
```


### Posiciones Iniciales de las Pelotas
Las posiciones iniciales de las pelotas (`p_azul` y `p_roja`) se definen como arreglos `numpy`, con un radio `r` de 20 pixeles para ambas pelotitas.

```python
p_azul = np.array([200, 200])
p_roja = np.array([300, 300])
r = 20  # radio de las pelotas
```






### Velocidades de las Pelotas
Se definen las velocidades para las pelotas en pixeles por cuadro. La pelota azul tiene una velocidad en x e y, mientras que la roja no se mueve automaticamente.


```python
v_azul = np.array([5, 3])
v_roja = np.array([0, 0])
```


### Colores
Los colores de las pelotas estan definidos en formato BGR .

```python
c_azul = (255, 0, 0)  # Color azul en BGR
c_roja = (0, 0, 255)  # Color rojo en BGR
```


### Bucle de Animacion

Dentro de un bucle `while`, se crea un `frame` negro de dimensiones `h`x`w` con tres canales de color.
```python
while True:
    # Fondo negro
    frame = np.zeros((h, w, 3), dtype=np.uint8)
```


#### Dibujar Pelotas
Se dibujan las pelotas azul y roja usando `cv2.circle()`, especificando la posicion, el radio `r`, y el color.

```python
cv2.circle(frame, p_azul, r, c_azul, -1)
cv2.circle(frame, p_roja, r, c_roja, -1)
```

#### Movimiento de  pelotita Azul

La posicion de la pelota azul se actualiza en cada iteracion sumando su velocidad (`v_azul`).

```python
p_azul += v_azul
```

#### Deteccion de Colisiones de la Pelota Azul con los Bordes
Para reflejar la pelota azul en los bordes de la ventana: Si la posición `x` o `y` de la pelota azul, menos o más su radio, sobrepasa los limites de la ventana, la velocidad en esa direccion se invierte.

```python
if p_azul[0] - r < 0 or p_azul[0] + r >= w:
    v_azul[0] = -v_azul[0]

if p_azul[1] - r <= 0 or p_azul[1] + r >= h:
    v_azul[1] = -v_azul[1]
```


#### Proximidad y Reposición de la Pelota Roja
- Calcula la distancia entre las pelotas azul y roja. Si la distancia es menor que el doble del radio (lo que significa que estan "tocandose"), la posicion de la pelota roja se reasigna aleatoriamente dentro de los limites de la ventana.

```python
dist = np.linalg.norm(p_azul - p_roja)
if dist < 2 * r:
    # Mover roja a posición aleatoria
    p_roja = np.array([np.random.randint(r, w - r), np.random.randint(r, h - r)])
```

#### Mostrar la Animacion y  Salida
- Muestra el `frame` con las pelotas en la ventana `"Anim"`.

```python
cv2.imshow("Anim", frame)

if cv2.waitKey(30) & 0xFF == ord('q'):
    break
```
### Imagen del Resultado
![.]()
pelota Colicion
![.]()

