import numpy as np
import cv2 as cv

# inicia la captura de video
cap = cv.VideoCapture(0)

# parametros para el flujo optico
lkparm = dict(winSize=(15, 15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Lee el primer cuadro y convierte a escala de grises
_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

# Definicion de puntos de la cuadricula inicial
p0 = np.array([(100, 100), (200, 100), (300, 100), (400, 100), (500, 100),
               (100, 200), (200, 200), (300, 200), (400, 200), (500, 200),
               (100, 300), (200, 300), (300, 300), (400, 300), (500, 300),
               (100, 400), (200, 400), (300, 400), (400, 400), (500, 400)])
p0 = np.float32(p0[:, np.newaxis, :])

# inicializa la mascara para el dibujo
mask = np.zeros_like(vframe)

# ciclo de procesamiento de cada cuadro
while True:
    # lee el siguiente cuadro y convierte a escala de grises
    _, frame = cap.read()
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcula el flujo optico
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    if p1 is None:
        # Controlador d emovimiento de los puntitos
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        p0 = np.array([(100, 100), (200, 100), (300, 100), (400, 100)])
        p0 = np.float32(p0[:, np.newaxis, :])
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        # Dibuja la red entre puntos 
        for i in range(len(p1)):
            x1, y1 = int(p1[i][0][0]), int(p1[i][0][1])

            # Conecta horizontalmente
            if (i + 1) % 5 != 0:
                x2, y2 = int(p1[i + 1][0][0]), int(p1[i + 1][0][1])
                frame = cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

            # Conecta verticalmente los puntitos
            if i + 5 < len(p1):
                x2, y2 = int(p1[i + 5][0][0]), int(p1[i + 5][0][1])
                frame = cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

            # Dibuja el punto actual
            frame = cv.circle(frame, (x1, y1), 3, (0, 255, 0), -1)

        cv.imshow('ventana', frame)
        vgris = fgris.copy()

        if (cv.waitKey(1) & 0xff) == 27:
            break

cap.release()
cv.destroyAllWindows()
