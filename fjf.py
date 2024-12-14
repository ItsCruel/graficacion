import math
import random
import glfw
from OpenGL.GL import *
from OpenGL.GLU import * 
import cv2 as cv
import numpy as np
import threading
import time

# Parametros para el flujo optico 
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Inicializacion de variables para transformaciones
translation_x, translation_y, translation_z = 0.0, 0.0, -8.0
scaling_factor = 1.0
rotation_angle = 0.0

# Estado de los gestos
last_action_time = time.time()
reset_time_threshold = 2.0  

# Inicializar captura de video
cap = cv.VideoCapture(0)
ret, first_frame = cap.read()
if not ret:
    raise RuntimeError("No se pudo iniciar la cámara.")
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Posiciones iniciales de los puntos de seguimiento
ball_pos = np.array([[300, 300]], dtype=np.float32).reshape(-1, 1, 2)
blue_ball_pos = np.array([[100, 100]], dtype=np.float32).reshape(-1, 1, 2)

# Dimensiones del area de control 
area_margin = 50  
frame_width, frame_height = first_frame.shape[1], first_frame.shape[0]

# Ventana de OpenGL
def init_opengl():
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Fondo azul 
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_sphere(radius=1, x=0, y=0, z=0, color=(1.0, 1.0, 1.0)):
    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    glPopMatrix()

def draw_cone(base=0.1, height=0.5, x=0, y=0, z=0, color=(1.0, 1.0, 1.0)):
    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, base, 0, height, 32, 32)
    glPopMatrix()

def draw_cube(size=1, x=0, y=0, z=0, color=(1.0, 0.5, 0.3)):
    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)
    half_size = size / 2.0
    glBegin(GL_QUADS)
    # Cara frontal
    glVertex3f(-half_size, -half_size, half_size)
    glVertex3f(half_size, -half_size, half_size)
    glVertex3f(half_size, half_size, half_size)
    glVertex3f(-half_size, half_size, half_size)
    # Cara trasera
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(half_size, -half_size, -half_size)
    glVertex3f(half_size, half_size, -half_size)
    glVertex3f(-half_size, half_size, -half_size)
    # Cara izquierda
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(-half_size, -half_size, half_size)
    glVertex3f(-half_size, half_size, half_size)
    glVertex3f(-half_size, half_size, -half_size)
    # Cara derecha
    glVertex3f(half_size, -half_size, -half_size)
    glVertex3f(half_size, -half_size, half_size)
    glVertex3f(half_size, half_size, half_size)
    glVertex3f(half_size, half_size, -half_size)
    # Cara superior
    glVertex3f(-half_size, half_size, -half_size)
    glVertex3f(half_size, half_size, -half_size)
    glVertex3f(half_size, half_size, half_size)
    glVertex3f(-half_size, half_size, half_size)
    # Cara inferior
    glVertex3f(-half_size, -half_size, -half_size)
    glVertex3f(half_size, -half_size, -half_size)
    glVertex3f(half_size, -half_size, half_size)
    glVertex3f(-half_size, -half_size, half_size)
    glEnd()
    glPopMatrix()

def draw_horse(x=0, y=0, z=0):
    # Dibujar el cuerpo
    draw_sphere(radius=0.5, x=x, y=y + 0.5, z=z, color=(0.6, 0.4, 0.2))
    # Dibujar la cabeza
    draw_sphere(radius=0.3, x=x + 0.6, y=y + 0.8, z=z, color=(0.6, 0.4, 0.2))
    # Dibujar las patas
    for dx in [-0.2, 0.2]:
        for dz in [-0.2, 0.2]:
            draw_cone(base=0.1, height=0.5, x=x + dx, y=y, z=z + dz, color=(0.6, 0.4, 0.2))
            
def draw_rabbit(x=0, y=0, z=0):
    # Cuerpo 
    draw_sphere(radius=0.2, x=x, y=y + 0.2, z=z, color=(0.8, 0.8, 0.8))  # Cuerpo
    draw_sphere(radius=0.1, x=x, y=y + 0.4, z=z + 0.1, color=(0.8, 0.8, 0.8))  # Cabeza
    draw_cone(base=0.05, height=0.2, x=x - 0.05, y=y + 0.5, z=z + 0.1, color=(0.8, 0.8, 0.8))
    draw_cone(base=0.05, height=0.2, x=x + 0.05, y=y + 0.5, z=z + 0.1, color=(0.8, 0.8, 0.8))

def draw_bush(x=0, y=0, z=0):
    draw_sphere(radius=0.4, x=x, y=y + 0.4, z=z, color=(0.0, 0.5, 0.0))
    draw_sphere(radius=0.3, x=x - 0.3, y=y + 0.4, z=z, color=(0.0, 0.6, 0.0))
    draw_sphere(radius=0.3, x=x + 0.3, y=y + 0.4, z=z, color=(0.0, 0.6, 0.0))

def draw_frog(x=0, y=0, z=0):
    # Cuerpo 
    draw_sphere(radius=0.25, x=x, y=y + 0.2, z=z, color=(0.0, 0.7, 0.0))  # Cuerpo 
    draw_sphere(radius=0.15, x=x, y=y + 0.35, z=z, color=(0.0, 0.8, 0.0))  # Cabeza
    # Ojos
    draw_sphere(radius=0.07, x=x - 0.08, y=y + 0.45, z=z + 0.1, color=(1.0, 1.0, 1.0))  # Ojo i
    draw_sphere(radius=0.07, x=x + 0.08, y=y + 0.45, z=z + 0.1, color=(1.0, 1.0, 1.0))  # Ojo d
    draw_sphere(radius=0.03, x=x - 0.08, y=y + 0.45, z=z + 0.15, color=(0.0, 0.0, 0.0))  
    draw_sphere(radius=0.03, x=x + 0.08, y=y + 0.45, z=z + 0.15, color=(0.0, 0.0, 0.0))  
    # Boca 
    draw_cylinder(base_radius=0.02, top_radius=0.02, height=0.05, x=x, y=y + 0.3, z=z - 0.05, color=(0.0, 0.5, 0.0))  
    # Patas
    draw_cylinder(base_radius=0.05, top_radius=0.02, height=0.15, x=x - 0.15, y=y + 0.1, z=z - 0.1, color=(0.0, 0.7, 0.0))  
    draw_cylinder(base_radius=0.05, top_radius=0.02, height=0.15, x=x + 0.15, y=y + 0.1, z=z - 0.1, color=(0.0, 0.7, 0.0))  
    
    draw_cylinder(base_radius=0.03, top_radius=0.02, height=0.1, x=x - 0.12, y=y + 0.05, z=z + 0.1, color=(0.0, 0.7, 0.0))  
    draw_cylinder(base_radius=0.03, top_radius=0.02, height=0.1, x=x + 0.12, y=y + 0.05, z=z + 0.1, color=(0.0, 0.7, 0.0))  

def draw_fallen_log(x=0, y=0, z=0, length=2.0):
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)  
    glTranslatef(x, y, z)
    glRotatef(90, 0, 1, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, length, 32, 32)
    glPopMatrix()
    
    

def draw_sphere(radius, x, y, z, color):
    """Dibuja una esfera."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    glPopMatrix()

def draw_oriented_cylinder(base_radius, top_radius, height, x, y, z, angle_x=0, angle_y=0, color=(1, 1, 1)):
    """Dibuja un cilindro con orientación."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    glRotatef(angle_x, 1, 0, 0)  
    glRotatef(angle_y, 0, 1, 0)  
    quadric = gluNewQuadric()
    gluCylinder(quadric, base_radius, top_radius, height, 32, 32)
    glPopMatrix()
    
def draw_cylinder(base_radius, top_radius, height, x, y, z, color):
    """Dibuja un cilindro."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    glRotatef(-90, 1, 0, 0) 
    quadric = gluNewQuadric()
    gluCylinder(quadric, base_radius, top_radius, height, 32, 32)
    glPopMatrix()

def draw_spider(x=0, y=0, z=0):
    # Cuerpo
    draw_sphere(radius=0.1, x=x, y=y + 0.2, z=z, color=(0.0, 0.0, 0.0))
    # Ojos
    draw_sphere(radius=0.04, x=x - 0.06, y=y + 0.3, z=z + 0.04, color=(1.0, 0.0, 0.0))
    draw_sphere(radius=0.04, x=x + 0.06, y=y + 0.3, z=z + 0.04, color=(1.0, 0.0, 0.0))
    # Patas
    leg_length = 0.2 
    for i in range(8):
        angle = i * 45
        leg_x = x + leg_length * np.cos(np.radians(angle))
        leg_z = z + leg_length * np.sin(np.radians(angle))
        leg_angle = -30 if i < 4 else 30
        draw_oriented_cylinder(base_radius=0.02, top_radius=0.02, height=leg_length, 
                               x=leg_x, y=y + 0.2, z=leg_z, angle_x=leg_angle, color=(0.0, 0.0, 0.0))


def draw_owl(x=0, y=0, z=0):
    # Cuerpo 
    draw_sphere(radius=0.3, x=x, y=y + 0.6, z=z, color=(0.6, 0.3, 0.1))

    draw_sphere(radius=0.15, x=x - 0.15, y=y + 0.8, z=z + 0.15, color=(1.0, 1.0, 0.0))
    draw_sphere(radius=0.15, x=x + 0.15, y=y + 0.8, z=z + 0.15, color=(1.0, 1.0, 0.0))

    draw_cylinder(
        base_radius=0.15, top_radius=0.1, height=0.6, 
        x=x - 0.3, y=y + 0.5, z=z, color=(0.4, 0.2, 0.1)
    )
    draw_cylinder(
        base_radius=0.15, top_radius=0.1, height=0.6, 
        x=x + 0.3, y=y + 0.5, z=z, color=(0.4, 0.2, 0.1)
    )
    
def draw_cow(x=0, y=0, z=0):
    # Cuerpo
    draw_sphere(radius=0.4, x=x, y=y + 0.2, z=z, color=(1.0, 1.0, 1.0))  
    
    # Cabeza
    draw_sphere(radius=0.2, x=x, y=y + 0.55, z=z, color=(1.0, 1.0, 1.0))  
    
    # Ojos
    draw_sphere(radius=0.05, x=x - 0.06, y=y + 0.6, z=z + 0.1, color=(0.0, 0.0, 0.0))  # izquierdo
    draw_sphere(radius=0.05, x=x + 0.06, y=y + 0.6, z=z + 0.1, color=(0.0, 0.0, 0.0))  # derecho
    
    # Nariz
    draw_sphere(radius=0.05, x=x, y=y + 0.5, z=z + 0.15, color=(0.8, 0.5, 0.3)) 
    
    # Cuernos
    draw_cone(base=0.07, height=0.1, x=x - 0.2, y=y + 0.7, z=z, color=(0.6, 0.3, 0.1))  # izquierdo
    draw_cone(base=0.07, height=0.1, x=x + 0.2, y=y + 0.7, z=z, color=(0.6, 0.3, 0.1))  # derecho
    
    # Orejas
    draw_cone(base=0.1, height=0.15, x=x - 0.18, y=y + 0.65, z=z, color=(1.0, 0.9, 0.8))  
    draw_cone(base=0.1, height=0.15, x=x + 0.18, y=y + 0.65, z=z, color=(1.0, 0.9, 0.8))  
    
    # Piernas
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.2, x=x - 0.15, y=y - 0.1, z=z, color=(0.6, 0.3, 0.1))  
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.2, x=x + 0.15, y=y - 0.1, z=z, color=(0.6, 0.3, 0.1))  
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.2, x=x - 0.15, y=y - 0.4, z=z, color=(0.6, 0.3, 0.1))  
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.2, x=x + 0.15, y=y - 0.4, z=z, color=(0.6, 0.3, 0.1))  
    
    draw_cylinder(base_radius=0.02, top_radius=0.02, height=0.25, x=x - 0.3, y=y - 0.2, z=z, color=(0.6, 0.3, 0.1)) 
    draw_sphere(radius=0.05, x=x - 0.3, y=y - 0.2, z=z + 0.15, color=(0.6, 0.3, 0.1))  

def draw_cloud(x=0, y=0, z=0):
    # Esfera central
    draw_sphere(radius=0.6, x=x, y=y + 0.8, z=z, color=(1.0, 1.0, 1.0))  
    # Lados
    draw_sphere(radius=0.4, x=x - 0.5, y=y + 0.9, z=z, color=(1.0, 1.0, 1.0))  
    draw_sphere(radius=0.4, x=x + 0.5, y=y + 0.9, z=z, color=(1.0, 1.0, 1.0))  
    # Superior
    draw_sphere(radius=0.4, x=x, y=y + 1.2, z=z, color=(1.0, 1.0, 1.0))  
    draw_sphere(radius=0.3, x=x - 0.8, y=y + 0.8, z=z, color=(1.0, 1.0, 1.0))  
    draw_sphere(radius=0.3, x=x + 0.8, y=y + 0.8, z=z, color=(1.0, 1.0, 1.0))

def draw_flower(x=0, y=0, z=0):
    draw_sphere(radius=0.1, x=x, y=y + 0.3, z=z, color=(1.0, 0.0, 1.0))
    draw_sphere(radius=0.1, x=x + 0.2, y=y + 0.2, z=z, color=(1.0, 0.0, 1.0))
    draw_sphere(radius=0.1, x=x - 0.2, y=y + 0.2, z=z, color=(1.0, 0.0, 1.0))
    draw_sphere(radius=0.1, x=x, y=y + 0.2, z=z + 0.2, color=(1.0, 0.0, 1.0))
    draw_cylinder(base_radius=0.02, top_radius=0.02, height=0.4, x=x, y=y, z=z, color=(0.0, 0.8, 0.0))


def draw_mushroom(x=0, y=0, z=0):
    draw_sphere(radius=0.3, x=x, y=y + 0.5, z=z, color=(1.0, 0.0, 0.0))
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.4, x=x, y=y, z=z, color=(0.8, 0.6, 0.4))

def draw_pine_tree(x=0, y=0, z=0):
    draw_cylinder(base_radius=0.1, top_radius=0.1, height=0.6, x=x, y=y, z=z, color=(0.6, 0.3, 0.1))
    draw_cone(base=0.5, height=0.6, x=x, y=y + 0.6, z=z, color=(0.0, 0.5, 0.0))
    draw_cone(base=0.4, height=0.5, x=x, y=y + 0.9, z=z, color=(0.0, 0.6, 0.0))
    draw_cone(base=0.3, height=0.4, x=x, y=y + 1.1, z=z, color=(0.0, 0.7, 0.0))

def draw_fawn(x=0, y=0, z=0):
    # Cuerpo
    draw_sphere(radius=0.4, x=x, y=y + 0.3, z=z, color=(0.6, 0.4, 0.2)) 
    draw_sphere(radius=0.2, x=x, y=y + 0.7, z=z, color=(0.6, 0.4, 0.2))  

    # Patas
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.3, x=x - 0.15, y=y, z=z - 0.1, color=(0.6, 0.4, 0.2))  # Pata delantera izquierda
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.3, x=x + 0.15, y=y, z=z - 0.1, color=(0.6, 0.4, 0.2))  # Pata delantera derecha
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.3, x=x - 0.15, y=y, z=z + 0.1, color=(0.6, 0.4, 0.2))  # Pata trasera izquierda
    draw_cylinder(base_radius=0.05, top_radius=0.05, height=0.3, x=x + 0.15, y=y, z=z + 0.1, color=(0.6, 0.4, 0.2))  # Pata trasera derecha

    # Cola
    draw_sphere(radius=0.05, x=x, y=y + 0.4, z=z + 0.2, color=(0.6, 0.4, 0.2))

    # Orejas
    draw_cone(base=0.05, height=0.1, x=x - 0.1, y=y + 0.9, z=z - 0.05, color=(0.6, 0.4, 0.2))  # Oreja izquierda
    draw_cone(base=0.05, height=0.1, x=x + 0.1, y=y + 0.9, z=z - 0.05, color=(0.6, 0.4, 0.2))  # Oreja derecha

    # Cuernos pequeños
    draw_cylinder(base_radius=0.02, top_radius=0.02, height=0.1, x=x - 0.05, y=y + 0.85, z=z, color=(0.4, 0.2, 0.1))  # Cuerno izquierdo
    draw_cylinder(base_radius=0.02, top_radius=0.02, height=0.1, x=x + 0.05, y=y + 0.85, z=z, color=(0.4, 0.2, 0.1))  # Cuerno derecho

    # Ojos
    draw_sphere(radius=0.03, x=x - 0.08, y=y + 0.75, z=z + 0.18, color=(0, 0, 0))  # Ojo izquierdo
    draw_sphere(radius=0.03, x=x + 0.08, y=y + 0.75, z=z + 0.18, color=(0, 0, 0))  # Ojo derecho

def draw_bear(x=0, y=0, z=0):
    scale = 1/3 
    #cuerpo
    draw_sphere(radius=1.0 * scale, x=x, y=y, z=z, color=(0.6, 0.4, 0.2))

    # cabeza
    draw_sphere(radius=0.5 * scale, x=x, y=y + 1.2 * scale, z=z, color=(0.6, 0.4, 0.2))

    # orejas 
    draw_sphere(radius=0.2 * scale, x=x - 0.3 * scale, y=y + 1.8 * scale, z=z + 0.3 * scale, color=(0.6, 0.4, 0.2))
    draw_sphere(radius=0.2 * scale, x=x + 0.3 * scale, y=y + 1.8 * scale, z=z + 0.3 * scale, color=(0.6, 0.4, 0.2))

    draw_cylinder(base_radius=0.2 * scale, top_radius=0.1 * scale, height=0.5 * scale, 
                  x=x - 0.5 * scale, y=y - 0.5 * scale, z=z + 0.4 * scale, color=(0.4, 0.2, 0.1))
    draw_cylinder(base_radius=0.2 * scale, top_radius=0.1 * scale, height=0.5 * scale, 
                  x=x + 0.5 * scale, y=y - 0.5 * scale, z=z + 0.4 * scale, color=(0.4, 0.2, 0.1))
    draw_cylinder(base_radius=0.3 * scale, top_radius=0.15 * scale, height=0.6 * scale, 
                  x=x - 0.6 * scale, y=y - 1.0 * scale, z=z - 0.3 * scale, color=(0.4, 0.2, 0.1))
    draw_cylinder(base_radius=0.3 * scale, top_radius=0.15 * scale, height=0.6 * scale, 
                  x=x + 0.6 * scale, y=y - 1.0 * scale, z=z - 0.3 * scale, color=(0.4, 0.2, 0.1))

    draw_sphere(radius=0.1 * scale, x=x, y=y + 1.2 * scale, z=z + 0.5 * scale, color=(0.3, 0.2, 0.1))

    # Dibujar los ojos
    draw_sphere(radius=0.08 * scale, x=x - 0.2 * scale, y=y + 1.4 * scale, z=z + 0.4 * scale, color=(0.0, 0.0, 0.0))
    draw_sphere(radius=0.08 * scale, x=x + 0.2 * scale, y=y + 1.4 * scale, z=z + 0.4 * scale, color=(0.0, 0.0, 0.0))


def draw_dog(x=0, y=0, z=0):
    # Cuerpo 
    draw_sphere(radius=0.3, x=x, y=y + 0.3, z=z, color=(0.8, 0.6, 0.3))  

    # Cabeza 
    draw_sphere(radius=0.2, x=x, y=y + 0.6, z=z, color=(0.8, 0.6, 0.3))  

    # Orejas 
    draw_cone(base=0.05, height=0.1, x=x - 0.1, y=y + 0.75, z=z, color=(0.8, 0.6, 0.3))  
    draw_cone(base=0.05, height=0.1, x=x + 0.1, y=y + 0.75, z=z, color=(0.8, 0.6, 0.3))  

    # Ojos 
    draw_sphere(radius=0.05, x=x - 0.08, y=y + 0.65, z=z + 0.1, color=(1.0, 1.0, 1.0))  
    draw_sphere(radius=0.05, x=x + 0.08, y=y + 0.65, z=z + 0.1, color=(1.0, 1.0, 1.0))  
    draw_sphere(radius=0.02, x=x - 0.08, y=y + 0.65, z=z + 0.15, color=(0.0, 0.0, 0.0))  
    draw_sphere(radius=0.02, x=x + 0.08, y=y + 0.65, z=z + 0.15, color=(0.0, 0.0, 0.0))  

    # Boca 
    draw_cylinder(base_radius=0.02, top_radius=0.02, height=0.05, x=x, y=y + 0.55, z=z - 0.1, color=(0.0, 0.5, 0.0))  

    # Patas 
    draw_cylinder(base_radius=0.05, top_radius=0.02, height=0.2, x=x - 0.15, y=y, z=z - 0.15, color=(0.8, 0.6, 0.3))  
    draw_cylinder(base_radius=0.05, top_radius=0.02, height=0.2, x=x + 0.15, y=y, z=z - 0.15, color=(0.8, 0.6, 0.3))  
    draw_cylinder(base_radius=0.05, top_radius=0.02, height=0.2, x=x - 0.15, y=y, z=z + 0.15, color=(0.8, 0.6, 0.3))  
    draw_cylinder(base_radius=0.05, top_radius=0.02, height=0.2, x=x + 0.15, y=y, z=z + 0.15, color=(0.8, 0.6, 0.3))  


def draw_bat(x=0, y=0, z=0):

    # Dibujar el cuerpo del murcielago
    glColor3f(0.1, 0.1, 0.1)  # Color 
    glPushMatrix()
    glTranslatef(x, y, z)
    draw_sphere(radius=0.3, x=0, y=0, z=0, color=(0.1, 0.1, 0.1))
    
    # alas 
    glBegin(GL_TRIANGLES)
    glColor3f(0.1, 0.1, 0.1)
    # Ala izquierda
    glVertex3f(-0.5, 0.1, 0.0)
    glVertex3f(-1.2, 0.5, 0.0)
    glVertex3f(-0.5, -0.1, 0.0)
    # Ala derecha
    glVertex3f(0.5, 0.1, 0.0)
    glVertex3f(1.2, 0.5, 0.0)
    glVertex3f(0.5, -0.1, 0.0)
    glEnd()
    glPopMatrix()

def draw_moving_bats():
    global bat_offset
    bat_positions = [
        (2, 7, -3), (-4, 8, 5), (6, 9, -6), (-7, 10, 2),
        (5, 11, -8), (-8, 12, 3)
    ]
    for i, (x, y, z) in enumerate(bat_positions):
        # Desplazamiento horizontal y oscilacion 
        x_moving = x + bat_offset
        y_oscillating = y + math.sin(bat_offset + i) * 0.5
        # Logica para que los murcielagos reaparezcan a los limites
        if x_moving > 20:
            x_moving -= 40
        elif x_moving < -20:
            x_moving += 40
        draw_bat(x_moving, y_oscillating, z)

    # Incrementar  movimiento
    bat_offset += 0.1  # velocidad
    if bat_offset > 20:
        bat_offset -= 40  # Evitar valores excesivos 
        
        
balloon_positions = [{'x': -5, 'y': -10}, {'x': 0, 'y': -20}, {'x': 5, 'y': -15}]
balloon_speed = 0.05  # Velocidad a la que suben los globos

def draw_spheres(radius, slices=20, stacks=20):
    """Dibuja una esfera usando GLU."""
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)

def draw_cubes(size):
    half = size / 2
    glBegin(GL_QUADS)
    # Frente
    glVertex3f(-half, -half, half)
    glVertex3f(half, -half, half)
    glVertex3f(half, half, half)
    glVertex3f(-half, half, half)
    # Atrás
    glVertex3f(-half, -half, -half)
    glVertex3f(half, -half, -half)
    glVertex3f(half, half, -half)
    glVertex3f(-half, half, -half)
    # Izquierda
    glVertex3f(-half, -half, -half)
    glVertex3f(-half, -half, half)
    glVertex3f(-half, half, half)
    glVertex3f(-half, half, -half)
    # Derecha
    glVertex3f(half, -half, -half)
    glVertex3f(half, -half, half)
    glVertex3f(half, half, half)
    glVertex3f(half, half, -half)
    # Arriba
    glVertex3f(-half, half, -half)
    glVertex3f(half, half, -half)
    glVertex3f(half, half, half)
    glVertex3f(-half, half, half)
    # Abajo
    glVertex3f(-half, -half, -half)
    glVertex3f(half, -half, -half)
    glVertex3f(half, -half, half)
    glVertex3f(-half, -half, half)
    glEnd()

def draw_balloon(x, y):
    glPushMatrix()
    glTranslatef(x, y, 0)

    # Dibujar la esfera (globo)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    draw_spheres(1.0)

    # Dibujar la canasta (cubo)
    glColor3f(0.5, 0.3, 0.0)  # Marrón
    glTranslatef(0, -1.5, 0)
    draw_cubes(0.5)
    glPopMatrix()

def update_positions():
    for balloon in balloon_positions:
        balloon['y'] += balloon_speed  # Suben verticalmente
        if balloon['y'] > 10:  # Reaparecen en la parte inferior
            balloon['y'] = -10
       
        

# Variables globales para el movimientos
cloud_offset = 0.0
bat_offset = 0.0


def draw_forest():
    global translation_x, translation_y, translation_z, scaling_factor, rotation_angle, cloud_offset

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(translation_x, translation_y, translation_z)
    glScalef(scaling_factor, scaling_factor, scaling_factor)
    glRotatef(rotation_angle, 0, 1, 0)

    # Dibujar el suelo
    glColor3f(0.0, 0.6, 0.0)  
    glBegin(GL_QUADS)
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()
    
    # murcielagos movimiento
    draw_moving_bats()
    
     # Dibujar globos en sus posiciones
    for balloon in balloon_positions:
        draw_balloon(balloon['x'], balloon['y'])

    # Actualizar posiciones de los globos
    update_positions()
    
    
    # Dibujar nubes
    cloud_positions = [
        (3, 8, 3), (-4, 10, -5), (5, 9, -8), (-8, 12, 4),
        (6, 11, 7), (-10, 13, -3), (0, 15, 5), (-5, 14, -7)
    ]
    for i, (x, y, z) in enumerate(cloud_positions):
        # Ajustar la posición X de las nubes
        x_moving = x + cloud_offset
        # s nubes reaparezcan 
        if x_moving > 20:
            x_moving -= 40
        elif x_moving < -20:
            x_moving += 40
        draw_cloud(x_moving, y, z)  # de dibujo de la nube

    cloud_offset += 0.05  # Ajusta la velocidad del movimiento
    if cloud_offset > 20:
        cloud_offset -= 40  # Evitar valores excesivos 

    
    # arboles
    for x in range(-10, 11, 5):
        for z in range(-10, 11, 5):
            glPushMatrix()
            glTranslatef(x, 0, z)
            glColor3f(0.6, 0.3, 0.1)
            glRotatef(-90, 1, 0, 0)
            quadric = gluNewQuadric()
            gluCylinder(quadric, 0.3, 0.3, 2, 32, 32)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(x, 2, z)
            glColor3f(0.1, 0.8, 0.1)
            gluSphere(quadric, 1.0, 32, 32)
            glPopMatrix()
            
 # flores
    for x in range(-10, 11, 3): 
        for z in range(-10, 11, 3):
         draw_flower(x=x, y=0, z=z)
        
    # otros objetos
    objects_positions = [
        (2, 0, 3), (-3, 0, -5), (5, 0, -8), (-8, 0, 4), (7, 0, 7),
        (-6, 0, -7), (1, 0, -10), (-9, 0, -2), (8, 0, -6), (-4, 0, 9),
        (0, 0, -3), (-5, 0, 5)
    ]
    for i, (x, y, z) in enumerate(objects_positions):
        if i % 10 == 0:  #  casas con techo
            draw_cube(size=2, x=x, y=y + 1, z=z, color=(1.0, 0.5, 0.3))
            draw_cone(base=1.2, height=1.5, x=x, y=y + 2, z=z, color=(0.8, 0.2, 0.2))
        elif i % 10 == 1:  #  arañas
            draw_spider(x, y, z)
        elif i % 10 == 2:  #  vacas
            draw_cow(x, y, z)
        elif i % 10 == 3:  #  pinos
            draw_pine_tree(x, y, z)
        elif i % 10 == 4:  # rocas 
            draw_sphere(radius=0.7, x=x, y=y + 0.35, z=z, color=(0.5, 0.5, 0.5))
        elif i % 10 == 5:  #buhos
            draw_owl(x, y + 2, z)
        elif i % 10 == 6:  # hongos
            draw_mushroom(x, y, z)
        elif i % 10 == 7:  # flores
            draw_flower(x, y, z)
        elif i % 10 == 8:  # ciervos
            draw_fawn(x, y, z)
        elif i % 10 == 9:  # arbustos
            draw_bush(x, y, z)
        
            
    extra_positions = [
        (5, 0, 5), (10, 0, 10), (15, 0, 15),  # Ciervos
        (7, 0, 3), (12, 0, 8), (18, 0, 13),  # Arbustos
        (4, 0, 6), (9, 0, 11), (14, 0, 16),  # Pinos
        (3, 0, 7), (8, 0, 12), (13, 0, 17),  # Vacas
        (6, 0, 4), (11, 0, 9), (16, 0, 14)   # Hongos
    ]

  # Dibujar ciervos
    fawn_positions = [(6, 0, 3), (-5, 0, -1), (6, 0, 0)] 
    for x, y, z in fawn_positions:
       draw_fawn(x, y, z)

# Dibujar vacas
    cow_positions = [(4, 0.25, -3), (-3, 0.25, 5), (2, 0.25, -2)]  
    for x, y, z in cow_positions:
       draw_cow(x, y, z)

# Dibujar hongos
    mushroom_positions = [(0, 0, 1), (1, 0, -1), (-1, 0, 3)]  
    for x, y, z in mushroom_positions:
       draw_mushroom(x, y, z)
            
 # Dibujar osos
    bear_positions = [(0, 0.5, 2), (5, 0.5, -4), (-5, 0.5, 4)]  
    for x, y, z in bear_positions:
        draw_bear(x, y, z)
        
    # Dibujar conejos
    rabbit_positions = [(2, 0, 3), (-1, 0, -2), (4, 0, 0)]  
    for x, y, z in rabbit_positions:
        draw_rabbit(x, y, z)

    # Dibujar arbustos
    bush_positions = [(1, 0, 2), (3, 0, -3), (-2, 0, 4)]  
    for x, y, z in bush_positions:
        draw_bush(x, y, z)

    # Dibujar ranas
    frog_positions = [(1, 0, -1), (2, 0, 2), (-3, 0, 0)]  
    for x, y, z in frog_positions:
        draw_frog(x, y, z)

    # Dibujar troncos caidos
    fallen_log_positions = [(0, 0, -3), (5, 0, 5), (-4, 0, 2)]  
    for x, y, z in fallen_log_positions:
        draw_fallen_log(x, y, z, length=2.5)
      
     # Dibujar perritos
    dog_positions = [(0, 0, 3), (-2, 0, -1), (7, 0, 0)]  
    for x, y, z in dog_positions:
        draw_dog(x, y, z)
 
    # Dibujar caballos 
    horse_positions = [(4, 0, 3), (-4, 0, -1), (8, 0, 0)]  
    for x, y, z in horse_positions:
        draw_horse(x, y, z)

    
def detect_and_control_gestures(new_pos, prev_pos):
    global rotation_angle, scaling_factor, translation_x, translation_y, last_action_time

    dx = new_pos[0, 0, 0] - prev_pos[0, 0, 0]
    dy = new_pos[0, 0, 1] - prev_pos[0, 0, 1]

    # Movimiento lateral controla la traslacion en X
    translation_x += dx / 100.0

    # Movimiento vertical controla la traslacion en Y
    translation_y -= dy / 100.0

    # Si la mano se mueve mucho hacia arriba, escalar hacia arriba
    if dy < -5:
        scaling_factor += 0.01

    # Si la mano se mueve mucho hacia abajo, escalar hacia abajo
    elif dy > 5:
        scaling_factor -= 0.01

    # Si la mano se mueve lateralmente rapido, activar rotacion
    if abs(dx) > 5:
        rotation_angle += dx / 5.0

    # Actualizar el tiempo de la ultima accion
    if abs(dx) > 1 or abs(dy) > 1:
        last_action_time = time.time()

def detect_blue_gestures(new_pos, prev_pos):
    global scaling_factor, last_action_time

    dy = new_pos[0, 0, 1] - prev_pos[0, 0, 1]

    # Movimiento vertical controla la escala
    if dy < -5:  # Subiendo
        scaling_factor += 0.02
    elif dy > 5:  # Bajando
        scaling_factor -= 0.02

    # Actualizar el tiempo de la ultima accion
    if abs(dy) > 1:
        last_action_time = time.time()

def reset_forest():
    global translation_x, translation_y, translation_z, scaling_factor, rotation_angle
    translation_x, translation_y, translation_z = 0.0, 0.0, -8.0
    scaling_factor = 1.0
    rotation_angle = 0.0

def reset_ball_and_transformations():
    global ball_pos, blue_ball_pos, last_action_time
    ball_pos = np.array([[300, 300]], dtype=np.float32).reshape(-1, 1, 2)
    blue_ball_pos = np.array([[100, 100]], dtype=np.float32).reshape(-1, 1, 2)
    last_action_time = time.time()

def control_window():
    global ball_pos, blue_ball_pos, prev_gray, last_action_time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Calcular el flujo óptico para la bola verde
        new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)
        # Calcular el flujo óptico para la bola azul
        new_blue_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, blue_ball_pos, None, **lk_params)

        if new_ball_pos is not None:
            x, y = new_ball_pos.ravel()
            x = max(area_margin, min(x, frame_width - area_margin))
            y = max(area_margin, min(y, frame_height - area_margin))
            new_ball_pos[0, 0, :] = [x, y]

            detect_and_control_gestures(new_ball_pos, ball_pos)
            ball_pos = new_ball_pos

            cv.circle(frame, (int(x), int(y)), 20, (0, 255, 0), -1)

        if new_blue_pos is not None:
            x, y = new_blue_pos.ravel()
            x = max(area_margin, min(x, frame_width - area_margin))
            y = max(area_margin, min(y, frame_height - area_margin))
            new_blue_pos[0, 0, :] = [x, y]

            detect_blue_gestures(new_blue_pos, blue_ball_pos)
            blue_ball_pos = new_blue_pos

            cv.circle(frame, (int(x), int(y)), 20, (255, 0, 0), -1)

        prev_gray = gray_frame.copy()

        if time.time() - last_action_time > reset_time_threshold:
            reset_forest()
            reset_ball_and_transformations()

        cv.imshow("Control Gestual", frame)

        if cv.waitKey(1) & 0xFF == 27:
            break
        
def opengl_window():
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    init_opengl()

    while not glfw.window_should_close(window):
        draw_forest()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

threading.Thread(target=control_window, daemon=True).start()
opengl_window()
