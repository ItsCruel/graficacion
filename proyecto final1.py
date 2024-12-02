import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluSphere, gluPerspective, gluCylinder
import cv2 as cv
import numpy as np
import threading
import time

# Parámetros para el flujo óptico
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Inicialización de variables para transformaciones
translation_x, translation_y, translation_z = 0.0, 0.0, -8.0
scaling_factor = 1.0
rotation_angle = 0.0

# Estado de los gestos
last_action_time = time.time()
reset_time_threshold = 2.0  # Segundos sin movimiento antes de reiniciar

# Inicializar captura de video
cap = cv.VideoCapture(0)
ret, first_frame = cap.read()
if not ret:
    raise RuntimeError("No se pudo iniciar la cámara.")
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Posición inicial del punto de seguimiento
ball_pos = np.array([[300, 300]], dtype=np.float32).reshape(-1, 1, 2)


area_margin = 50  
frame_width, frame_height = first_frame.shape[1], first_frame.shape[0]

# Ventana de OpenGL
def init_opengl():
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Fondo azul (cielo)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_sphere(radius=1, x=0, y=0, z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    glPopMatrix()

def draw_cone(base=0.1, height=0.5, x=0, y=0, z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, base, 0, height, 32, 32)
    glPopMatrix()

def draw_snowman():
    global translation_x, translation_y, translation_z, scaling_factor, rotation_angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(translation_x, translation_y, translation_z)
    glScalef(scaling_factor, scaling_factor, scaling_factor)
    glRotatef(rotation_angle, 0, 1, 0)

    # Cuerpo del muñeco de nieve
    glColor3f(1, 1, 1)
    draw_sphere(1.0, 0, 0, 0)
    draw_sphere(0.75, 0, 1.2, 0)
    draw_sphere(0.5, 0, 2.2, 0)

    # Ojos
    glColor3f(0, 0, 0)
    draw_sphere(0.05, -0.15, 2.3, 0.4)
    draw_sphere(0.05, 0.15, 2.3, 0.4)

    # Nariz
    glColor3f(1, 0.5, 0)
    draw_cone(0.05, 0.2, 0, 2.2, 0.5)

# Detección de gestos y control del muñeco
def detect_and_control_gestures(new_pos, prev_pos):
    global rotation_angle, scaling_factor, translation_x, translation_y, last_action_time

    dx = new_pos[0, 0, 0] - prev_pos[0, 0, 0]
    dy = new_pos[0, 0, 1] - prev_pos[0, 0, 1]

    # Movimiento lateral 
    translation_x += dx / 100.0

    # Movimiento vertical
    translation_y -= dy / 100.0

    # Si la mano se mueve mucho hacia arriba, escalar hacia arriba
    if dy < -5:
        scaling_factor += 0.01

    # Si la mano se mueve mucho hacia abajo, escalar hacia abajo
    elif dy > 5:
        scaling_factor -= 0.01

    # Si la mano se mueve lateralmente rápido, activar rotación
    if abs(dx) > 5:
        rotation_angle += dx / 5.0

    # Actualizar el tiempo de la última acción
    if abs(dx) > 1 or abs(dy) > 1:
        last_action_time = time.time()

# Detectar si la bolita está en las esquinas y rotar
def detect_corner_and_rotate(new_pos):
    global rotation_angle

    x, y = new_pos.ravel()

    # Detectar si la bolita está en una esquina
    in_top_left = (x < area_margin * 2 and y < area_margin * 2)
    in_top_right = (x > frame_width - area_margin * 2 and y < area_margin * 2)
    in_bottom_left = (x < area_margin * 2 and y > frame_height - area_margin * 2)
    in_bottom_right = (x > frame_width - area_margin * 2 and y > frame_height - area_margin * 2)

    if in_top_left or in_top_right or in_bottom_left or in_bottom_right:
        rotation_angle += 2  # Rotar suavemente

# Reiniciar posiciones de la bolita y el muñeco
def reset_ball_and_transformations():
    global ball_pos, translation_x, translation_y, scaling_factor, rotation_angle, last_action_time
    translation_x, translation_y, translation_z = 0.0, 0.0, -8.0
    scaling_factor = 1.0
    rotation_angle = 0.0
    ball_pos = np.array([[300, 300]], dtype=np.float32).reshape(-1, 1, 2)
    last_action_time = time.time()

def control_window():
    global ball_pos, prev_gray, last_action_time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)

        if new_ball_pos is not None:
            # Limitar la posición de la pelotita dentro del área de control
            x, y = new_ball_pos.ravel()
            x = max(area_margin, min(x, frame_width - area_margin))
            y = max(area_margin, min(y, frame_height - area_margin))
            new_ball_pos[0, 0, :] = [x, y]

            detect_and_control_gestures(new_ball_pos, ball_pos)
            detect_corner_and_rotate(new_ball_pos)
            ball_pos = new_ball_pos

            # Dibujar la pelotita en su nueva posición
            cv.circle(frame, (int(x), int(y)), 20, (0, 255, 0), -1)

        prev_gray = gray_frame.copy()

        # Dibujar un rectángulo para área de control
        cv.rectangle(frame, (area_margin, area_margin), 
                     (frame_width - area_margin, frame_height - area_margin), (0, 0, 255), 2)

        # Verificar si es necesario reiniciar las transformaciones y la posición de la bolita
        if time.time() - last_action_time > reset_time_threshold:
            reset_ball_and_transformations()

        cv.imshow("Control por Gestos", frame)

        if cv.waitKey(1) & 0xFF == 27:  
            break

def opengl_window():
    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800, 600, "Muñeco de Nieve", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    init_opengl()

    while not glfw.window_should_close(window):
        draw_snowman()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    opengl_thread = threading.Thread(target=opengl_window)
    control_thread = threading.Thread(target=control_window)

    opengl_thread.start()
    control_thread.start()

    opengl_thread.join()
    control_thread.join()

    cap.release()
    cv.destroyAllWindows()
