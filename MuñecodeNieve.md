### Practica Casas y Muñecos de Nieve
Para esta practica el profe nos dio el codigo de muñecos de nieve y de las casitas y nos pidio juntar ambos

#### 0. **paso 0 importar Librerias**
**glfw**: Para la creacion y manejo de ventanas.
**OpenGL.GL y OpenGL.GLU**: Funciones de OpenGL para renderizado 3D.
 **sys**: Manejo de eventos del sistema.

```python
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluSphere, gluCylinder
import sys
```


#### 1. **Inicializacion del Entorno**

```python
def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)  
    glEnable(GL_DEPTH_TEST)           
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, 6, 100.0)  
    glMatrixMode(GL_MODELVIEW)
```



#### 2. **Funciones de Dibujado**
##### **Casa**
```python
def draw_cube():
    # Base cubica de la casa
    ...
def draw_roof():
    # Techo triangular
    ...
```

##### **Muñeco de Nieve**
```python
def draw_snowman():
    # Construye las esferas que forman el cuerpo y la cabeza
    ...
    # Dibuja ojos y nariz
    ...
```
- **draw_sphere**: Dibuja esferas para cuerpo y ojos.
- **draw_cone**: Genera el cono de la nariz.

##### **Suelo**
muestra el suelo
```python
def draw_ground():
    # Plano gris como suelo
    ...
```

#### 3. **Dibujar la Escena Completa**
se dibuja la escena
```python
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(10, 8, 15, 0, 0, 0, 0, 1, 0)  
    
    draw_ground()  # Suelo
    
    # Posicionamiento de casas y muñecos
    positions = [(-5, 0, -5), (5, 0, -5), (-5, 0, 5), (5, 0, 5)]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)
        draw_house()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos[0] + 1.5, 0, pos[2])
        draw_snowman()
        glPopMatrix()
    glfw.swap_buffers(window)
```


#### 4. **Funcion Principal**
```python
def main():
    if not glfw.init():
        sys.exit()
    global window
    window = glfw.create_window(800, 600, "Casas con Muñecos de Nieve", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    
    glfw.make_context_current(window)
    glViewport(0, 0, 800, 600)
    init()

    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()
```


### **Ejecutar el Programa**
El programa se inicia con:
```python
if __name__ == "__main__":
    main()
```

### Mostrando Resultados 
como resultado nos quedo la imagen de los muñequitos y las casas 
![Casas y muñecos](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/casasconmu%C3%B1ecos.png?raw=true)

