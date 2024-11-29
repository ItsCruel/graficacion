import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import numpy as np
import sys

# Variables globales para el ángulo de rotación
window = None
angle_x, angle_y = 0.0, 0.0  # Ángulos de rotación en los ejes X e Y
last_x, last_y = None, None  # Última posición del ratón para calcular la diferencia

# Parámetros del toroide
R = 1.0  # Radio mayor (distancia del centro del tubo al centro del toroide)
r = 0.4  # Radio menor (radio del tubo)
num_major = 30  # Segmentos en el círculo mayor
num_minor = 15  # Segmentos en el círculo menor

def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

def draw_torus():
    global angle_x, angle_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

    # Configuración de la vista del toroide
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)  # Alejar el toroide para que sea visible
    glRotatef(angle_x, 1, 0, 0)   # Rotar el toroide en el eje X
    glRotatef(angle_y, 0, 1, 0)   # Rotar el toroide en el eje Y

    # Dibujar el toroide utilizando segmentos
    for i in range(num_major):
        theta = 2 * np.pi * i / num_major
        next_theta = 2 * np.pi * (i + 1) / num_major

        glBegin(GL_QUAD_STRIP)
        for j in range(num_minor + 1):
            phi = 2 * np.pi * j / num_minor
            cos_theta, sin_theta = np.cos(theta), np.sin(theta)
            cos_next_theta, sin_next_theta = np.cos(next_theta), np.sin(next_theta)
            cos_phi, sin_phi = np.cos(phi), np.sin(phi)

            # Color dinámico para variación visual
            glColor3f((i % 2) * 0.5 + 0.5, (j % 2) * 0.5 + 0.5, 0.5)

            # Primera esquina
            x = (R + r * cos_phi) * cos_theta
            y = r * sin_phi
            z = (R + r * cos_phi) * sin_theta
            glVertex3f(x, y, z)

            # Segunda esquina
            x = (R + r * cos_phi) * cos_next_theta
            z = (R + r * cos_phi) * sin_next_theta
            glVertex3f(x, y, z)

        glEnd()

    glfw.swap_buffers(window)  # Intercambiar buffers para animación suave

def mouse_callback(window, xpos, ypos):
    global angle_x, angle_y, last_x, last_y

    # Si es la primera vez que movemos el ratón, inicializamos last_x y last_y
    if last_x is None or last_y is None:
        last_x, last_y = xpos, ypos

    # Calcular las diferencias en el movimiento del ratón
    dx = xpos - last_x
    dy = ypos - last_y

    # Ajustar los ángulos de rotación en función del movimiento del ratón
    angle_x += dy * 0.2  # Factor de sensibilidad en Y
    angle_y += dx * 0.2  # Factor de sensibilidad en X

    # Actualizar las posiciones anteriores del ratón
    last_x, last_y = xpos, ypos

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Toroide 3D Controlado por Ratón", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Configurar el callback de ratón
    glfw.set_cursor_pos_callback(window, mouse_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_torus()
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir

if __name__ == "__main__":
    main()
