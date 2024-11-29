import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2 as cv
import numpy as np

# Variables globales para la cámara
zoom = -15
rot_x, rot_y = 0, 0

def init_opengl():
    """Configuracion inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_forest():
    """Dibuja el bosque con árboles y un suelo"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 5, zoom, 0, 0, 0, 0, 1, 0)

    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)

    # Dibujar suelo
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()

    # Dibujar árboles
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

    glfw.swap_buffers(window)

def detect_gestures(p0, p1):
    """Detectar gestos basados en el movimiento de puntos"""
    global zoom, rot_x, rot_y
    movements = p1 - p0

    # Detectar cierre de mano (movimiento hacia el centro)
    if np.all(np.linalg.norm(movements, axis=2) < 10):
        zoom += 0.5

    # Detectar apertura de mano (movimiento hacia afuera)
    if np.all(np.linalg.norm(movements, axis=2) > 20):
        zoom -= 0.5

    # Detectar movimiento hacia arriba
    if np.mean(movements[:, :, 1]) < -5:
        rot_x -= 2

    # Detectar movimiento hacia la derecha
    if np.mean(movements[:, :, 0]) > 5:
        rot_y += 2

def main():
    global window
    global zoom, rot_x, rot_y

    # Configuración de GLFW
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "Control por Gestos", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    init_opengl()

    # Configuración de OpenCV
    cap = cv.VideoCapture(0)
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    _, old_frame = cap.read()
    old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
    p0 = np.array([[100, 100], [200, 100], [300, 100], [400, 100], [500, 100],
                   [100, 200], [200, 200], [300, 200], [400, 200], [500, 200]], np.float32)
    p0 = p0[:, np.newaxis, :]

    while not glfw.window_should_close(window):
        # Leer cuadro actual
        _, frame = cap.read()
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Calcular flujo óptico
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Procesar gestos
        if p1 is not None and st.sum() == len(st):
            detect_gestures(p0, p1)
            old_gray = frame_gray.copy()
            p0 = p1

        # Dibujar bosque
        draw_forest()

        # Mostrar puntos en la ventana de OpenCV
        for point in p1:
            cv.circle(frame, (int(point[0][0]), int(point[0][1])), 5, (0, 255, 0), -1)
        cv.imshow("Gestos", frame)

        if cv.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv.destroyAllWindows()
    glfw.terminate()

if __name__ == "__main__":
    main()
