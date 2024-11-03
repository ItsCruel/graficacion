# Practica Pelota

**Introduccion**
Este codigo se trata de una  animacion sencilla donde una pelota rebota dentro de una ventana usando la biblioteca OpenCV. 

1. como parte 1 configuramos la ventana y variables
importamos las librerias
python
import cv2
import numpy as np

**seleccionamos las dimensiones de la ventana**
ancho, alto = 640, 480

**creamos la  ventana**
cv2.namedWindow("Animacion", cv2.WINDOW_AUTOSIZE)

- *Dimensiones de la ventana*: Definimos  las variables ancho y alto para especificar el tamaño de la ventana de animacion, en este caso, 640x480 pixeles.

**configuracion de la ventana**
2. como parte 2  toca la configuracion de la ventana: 
   - Definimos el ancho y alto de la ventana (`640x480` pixeles).
   - Creamos una ventana llamada `"Animacion"` con tamaño ajustable (`cv2.WINDOW_AUTOSIZE`)

```python
# Posicion inicial
pos_pelota = np.array([100, 100])
radio_pelota = 20
velocidad = np.array([5, 3])

# Color de la pelotita (azul, verde, rojo)
color_pelota = (255, 0, 0)
```
Propiedades de la pelota
3. como parte 3 definimos las propiedades de la pelota:
   - `pos_pelota`: La posicion inicial de la pelota en `(100, 100)`.
   - `radio_pelota`: Radio de la pelota, en este caso `20` pixeles.
   - `velocidad`: Velocidad de la pelota en ambos ejes `(5, 3)`. Esto significa que se mueve 5 píxeles en el eje x y 3 en el eje y en cada fotograma.
   - `color_pelota`: El color inicial de la pelota en formato BGR (azul, verde, rojo). Aqui es `(255, 0, 0)` para un color rojo.

```python
# rastrear si la pelota ha rebotado
ha_rebotado = False
```

**Variable de control**:
4. como parte 4  definimos la variable de control , definimos si rebota o no.
   - `ha_rebotado`: Esta variable controla si la pelota ha tocado una pared recientemente. Se utiliza para cambiar el color solo una vez por rebote.

```python
# Bucle de animacion
while True:
    # Crear fondo negro
    fotograma = np.zeros((alto, ancho, 3), dtype=np.uint8)
```

Bucle de animacion:
5. como la parte 5 el bucle de la animacion se define : 
   - Se crea un bucle infinito para actualizar la posicion de la pelota en cada fotograma.
   - En cada iteracion, se crea un `fotograma`, que es una imagen negra del tamaño de la ventana (`640x480` píxeles), que se usara como fondo.

```python
    # Dibujar pelotita
    cv2.circle(fotograma, tuple(pos_pelota), radio_pelota, color_pelota, -1)
```

**Dibujar la pelota**:
parte 6 se dibuja la pelotita,  se dibuja un círculo en `fotograma` en la posicion `pos_pelota`, con el `radio_pelota` y el `color_pelota`. El valor `-1` rellena el circulo completamente.

```python
    # Actualizar posicion de la pelota
    pos_pelota += velocidad
```

**Actualizar posición**:
  La posicion de la pelota se actualiza sumando `velocidad` a `pos_pelota`, haciendo que se mueva.
```python
    if pos_pelota[0] - radio_pelota <= 0 or pos_pelota[0] + radio_pelota >= ancho:
        velocidad[0] = -velocidad[0]
        

        # Cambiar a color aleatorio solo si no ha rebotado
        if not ha_rebotado:
            color_pelota = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
            ha_rebotado = True
```

**Colisión en el eje x**:
   - se verifica si la pelota toca la pared izquierda o derecha (`pos_pelota[0] - radio_pelota <= 0` o `pos_pelota[0] + radio_pelota >= ancho`).
   - Si hay colision, invertimos la direccion horizontal cambiando el signo de `velocidad[0]`.
   - Si `ha_rebotado` es `False`, significa que es la primera colision con la pared, entonces cambiamos `color_pelota` a un color aleatorio y establecemos `ha_rebotado` en `True` para evitar cambios de color continuos.

```python
    if pos_pelota[1] - radio_pelota <= 0 or pos_pelota[1] + radio_pelota >= alto:
        velocidad[1] = -velocidad[1]
        
        # Cambiar a color aleatorio solo si no ha rebotado
        if not ha_rebotado:
            color_pelota = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
            ha_rebotado = True
```

**Colisión en el eje y**:
 Igual al eje x, aquí se verifica si la pelota toca la pared superior o inferior (`pos_pelota[1] - radio_pelota <= 0` o `pos_pelota[1] + radio_pelota >= alto`).
   - Si hay colision, invertimos la direccion vertical cambiando el signo de `velocidad[1]`.
   - Cambiamos el color si `ha_rebotado` es `False` y luego lo ponemos en `True`.

```python
    # Restablecer el estado de rebote 
    if radio_pelota < pos_pelota[0] < ancho - radio_pelota and radio_pelota < pos_pelota[1] < alto - radio_pelota:
        ha_rebotado = False
```

**Se restablecer el estado de rebote**:
    - Si la pelota esta dentro de los límites y no toca las paredes, se establece `ha_rebotado` en `False` para permitir que el color cambie en el proximo rebote.

```python
    # Mostrar imagen
    cv2.imshow("Animacion", fotograma)
```

**Mostrando resultado**:
    - La ventana `"Animacion"` muestra el `fotograma` actualizado.

```python
    # Salir al presionar 'Esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break
```


**Cerrar Codigo**:
    - Una vez que el bucle se rompe, se cierran todas las ventanas de OpenCV con `cv2.destroyAllWindows()`.

#  Mostrando los Resultados
   <p>
por ultimo quede mostrar el resultado del pixel art 
![Pelota](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/hongomine.jpg)
</p>
<p>
por ultimo quede mostrar el resultado del pixel art 
![pelota Actualizada](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/hongomine.jpg)
</p>