import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluSphere, gluCylinder
import sys

def init():
    """configuracion inicial """
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuracion de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, 6, 100.0)  # Campo de vision más amplio
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    """(base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)  

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Atras
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(-1, 5, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 5, 1)
    glVertex3f(-1, 5, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(1, 5, -1)

    # Arriba
    glColor3f(0.9, 0.6, 0.3) 
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2) 
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

def draw_roof():
    """Dibuja el techo"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1) 

    # Frente
    glVertex3f(-1, 5, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(0, 9, 0)

    # Atrás
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(0, 9, 0)

    # Izquierda
    glVertex3f(-1, 5, -1)
    glVertex3f(-1, 5, 1)
    glVertex3f(0, 9, 0)

    # Derecha
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(0, 9, 0)
    glEnd()

def draw_ground():
    """ plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  

    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()

def draw_snowman():
    """Dibuja un muneco de nieve"""
    # Cuerpo
    glColor3f(1, 1, 1)
    draw_sphere(0.5, 0, 0.5, 0)     # Base
    draw_sphere(0.35, 0, 0.9, 0)    # Cuerpo medio
    draw_sphere(0.2, 0, 1.2, 0)     # Cabeza

    # Ojos
    glColor3f(0, 0, 0)
    draw_sphere(0.03, -0.05, 1.25, 0.1)  
    draw_sphere(0.03, 0.05, 1.25, 0.1)   

    # Nariz 
    glColor3f(1, 0.5, 0)  # Naranja
    draw_cone(0.05, 0.1, 0, 1.2, 0.15)

def draw_sphere(radius, x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    glPopMatrix()

def draw_cone(base, height, x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, base, 0, height, 32, 32)
    glPopMatrix()

def draw_house():
    """Dibuja una casa"""
    draw_cube()
    draw_roof()

def draw_scene():
    """Dibuja toda la escena"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # camara
    gluLookAt(10, 8, 15,  
              0, 0, 0,   
              0, 1, 0)    

    # Dibujar el suelo
    draw_ground()

    # Posiciones de las casas y muñecos
    positions = [
        (-5, 0, -5),
        (5, 0, -5),
        (-5, 0, 5),
        (5, 0, 5)
    ]
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

def main():
    if not glfw.init():
        sys.exit()

    global window
    width, height = 800, 600
    window = glfw.create_window(width, height, "Casas con Muñecos de Nieve", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
