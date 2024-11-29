###  Practica Figura Isometrica

Este codigo tiene como objetivo visualizar un prisma trapezoidal en una proyeccion isometrica usando la biblioteca `OpenCV` y `NumPy`  La proyeccion isométrica se usa para representar objetos tridimensionales (3D) en una pantalla bidimensional (2D), sin perder las proporciones entre los ejes.

#### Paso 0 
importamos el numpu y el open cv 

```python
import cv2
import numpy as np
```

#### Dimensiones de la ventana
definimos nuestras dimenciones 

```python
WIDTH, HEIGHT = 800, 600
```

Se definen las dimensiones de la ventana en la que se va a dibujar el prisma. La ventana tendra un ancho de **800 pixeles** y una altura de **600 pixeles**.

#### Vertices del Prisma Trapezoidal

Se definen los **vertices 3D** del prisma trapezoidal. 
Cada vertice está representado por un punto en el espacio tridimensional con coordenadas **(x, y, z)**.
El prisma tiene **8 vertices**. Los primeros 4 corresponden a la base inferior del prisma, y los 4 siguientes a la base superior.

```python
vertices = np.array([
    [-1, -1, -1],   
    [1, -1, -1],   
    [0.5, 0, -1], 
    [-0.5, 0, -1], 
    [-1, -1, 1],   
    [1, -1, 1],
    [0.5, 0, 1],
    [-0.5, 0, 1]
])
```


#### Conexiones entre los vértices
**`edges`** define las conexiones entre los vertices del prisma. 
Cada **tupla (a, b)** indica que el vertice **a** esta conectado al vertice **b**. Estos se usaran para dibujar las aristas del prisma.
Existen **12 conexiones** en total, correspondientes a las aristas del prisma.


```python
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  
    (4, 5), (5, 6), (6, 7), (7, 4),  
    (0, 4), (1, 5), (2, 6), (3, 7)   
]
```


#### Funcion de Proyeccion Isometrica

- La funcion **`project_isometric()`** convierte las coordenadas 3D de un vertice a coordenadas 2D usando la **proyeccion isometrica**.
  - **Ecuaciones**: La proyeccion isométrica se calcula con las siguientes formulas:
    ( x2D = x - z )
    ( y2D = \frac{x + 2y + z}{2})
  Multiplicamos las coordenadas por un factor de escala para ampliar la imagen, y luego centramos la imagen en la ventana añadiendo **`WIDTH/2`** y **`HEIGHT/2`**.

```python
def project_isometric(vertex):
    """Funcion para proyectar un punto 3D a 2D con proyeccion isometrica"""
    x, y, z = vertex
    x2D = x - z
    y2D = (x + 2 * y + z) / 2
    return int(x2D * 100 + WIDTH / 2), int(-y2D * 100 + HEIGHT / 2)
```


#### Crear la Ventana y Dibujar el Prisma
Se crea una ventana con el nombre **"Prisma Trapezoidal Isometrico"** para mostrar la imagen del prisma.


```python
cv2.namedWindow("Prisma Trapezoidal Isometrico")
```


#### Bucle Principal
**Bucle infinito**: Este bucle permite que la ventana se actualice continuamente hasta que se presione la tecla **'q'** para cerrar la ventana.
**`frame`**: Es una imagen vacía (de color negro) con las mismas dimensiones que la ventana.
**Dibujar las aristas**: Para cada par de vértices conectados por una arista, se calculan las posiciones 2D usando 
**`project_isometri()`** y se dibuja una linea blanca de grosor 2.
**`cv2.imshow()`**: Muestra la imagen con el prisma.

```python
while True:
    # Crear imagen negra para el fondo
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Dibujar aristas del prisma
    for edge in edges:
        pt1 = project_isometric(vertices[edge[0]])
        pt2 = project_isometric(vertices[edge[1]])
        cv2.line(frame, pt1, pt2, (255, 255, 255), 2)

    # Mostrar imagen
    cv2.imshow("Prisma Trapezoidal Isometrico", frame)

    # Salir si 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```



### Mostrando Resultado
![FiguraIsometrica](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/FiguraIsometrica.png?raw=true)

