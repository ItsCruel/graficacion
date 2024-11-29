import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2 as cv
import numpy as np

# Variables globales
zoom = -15
rot_x, rot_y = 0, 0
translate_x, translate_y = 0, 0
idle_counter = 0

def init_opengl():
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_forest():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(translate_x, translate_y + 5, zoom, 0, 0, 0, 0, 1, 0)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)

    # Dibujar el suelo
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()

    # Dibujar los árboles
    for x in range(-10, 11, 5):
        for z in range(-10, 11, 5):
            # Tronco
            glPushMatrix()
            glTranslatef(x, 0, z)
            glColor3f(0.6, 0.3, 0.1)
            glRotatef(-90, 1, 0, 0)
            quadric = gluNewQuadric()
            gluCylinder(quadric, 0.3, 0.3, 2, 32, 32)
            gluDeleteQuadric(quadric)
            glPopMatrix()

            # Copa del árbol
            glPushMatrix()
            glTranslatef(x, 2, z)
            glColor3f(0.1, 0.8, 0.1)
            quadric = gluNewQuadric()
            gluSphere(quadric, 1.0, 32, 32)
            gluDeleteQuadric(quadric)
            glPopMatrix()

    glfw.swap_buffers(window)

def detect_gestures(p0, p1):
    global zoom, rot_x, rot_y, translate_x, translate_y, idle_counter
    movements = p1 - p0
    mean_movement = np.mean(movements, axis=0)

    # Escalado
    distance_change = np.linalg.norm(p1 - p0, axis=2).mean()
    if distance_change > 10:
        zoom += 0.5
    elif distance_change < -10:
        zoom -= 0.5

    # Rotación
    if abs(mean_movement[0][0]) > 5:
        rot_y += mean_movement[0][0] * 0.5

    if abs(mean_movement[0][1]) > 5:
        rot_x += mean_movement[0][1] * 0.5

    # Traslación
    translate_x += mean_movement[0][0] * 0.01
    translate_y -= mean_movement[0][1] * 0.01

    # Reset idle_counter por actividad
    idle_counter = 0

def reset_forest():
    global zoom, rot_x, rot_y, translate_x, translate_y, idle_counter
    if idle_counter > 100:  # Unos 3-5 segundos de inactividad
        zoom, rot_x, rot_y, translate_x, translate_y = -15, 0, 0, 0, 0

def main():
    global window, idle_counter
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "Control por Gestos", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    init_opengl()

    cap = cv.VideoCapture(0)
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    _, old_frame = cap.read()
    old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
    p0 = np.array([[100 + i * 100, 100] for i in range(5)], np.float32).reshape(-1, 1, 2)

    while not glfw.window_should_close(window):
        _, frame = cap.read()
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        p1, st, _ = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        if p1 is not None and st.sum() == len(st):
            detect_gestures(p0, p1)
            old_gray = frame_gray.copy()
            p0 = p1
        else:
            idle_counter += 1
        reset_forest()
        draw_forest()

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

