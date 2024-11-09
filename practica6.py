import numpy as np
import cv2

# tamaño de la imagen
ancho, alto = 800, 800
# Centro de la imagen
centro_x, centro_y = ancho // 2, alto // 2

# Dibujar 10 ecuaciones paramétricas
for eq in range(10):
    img = np.zeros((alto, ancho, 3), dtype=np.uint8)
    t = np.linspace(0, 2 * np.pi, 1000)  # Parámetro t

    if eq == 0:
        # Circulo
        x = 180 * np.cos(t)
        y = 180 * np.sin(t)
    elif eq == 1:
          # Elipse
        x = 220 * np.cos(t)
        y = 120 * np.sin(t)
    elif eq == 2:
        # espiral logaritmica
        r = np.exp(0.9 * t)
        x = r * np.cos(t)
        y = r * np.sin(t)
    elif eq == 3:
        # Lemniscata
        x = 180 * np.cos(t) / (1 + np.sin(t)**2)
        y = 180 * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)
    elif eq == 4:
        # Rosa con 3 petalos
        k = 3
        r = 180 * np.cos(k * t)
        x = r * np.cos(t)
        y = r * np.sin(t)
    elif eq == 5:
        # Cardioide
        x = 180 * (1 - np.cos(t)) * np.cos(t)
        y = 180 * (1 - np.cos(t)) * np.sin(t)
    elif eq == 6:
        # Hipociclo
        R, r, d = 180, 40, 40
        x = (R - r) * np.cos(t) + d * np.cos(((R - r) / r) * t)
        y = (R - r) * np.sin(t) - d * np.sin(((R - r) / r) * t)
    elif eq == 7:
        # Espiral de arquimedes
        a, b = 1, 15
        r = a + b * t
        x = r * np.cos(t)
        y = r * np.sin(t)
    elif eq == 8:
        # Asteroide
        x = 180 * (np.cos(t)**3)
        y = 180 * (np.sin(t)**3)
    elif eq == 9:
        # Hiperbola
        x = 180 * np.sinh(t)
        y = 130 * np.cosh(t)

    # Mover las coordenadas al centro de la imagen
    x = np.int32(centro_x + x)
    y = np.int32(centro_y - y)

 # Dibujar las líneas entre los puntos
    for j in range(len(x) - 1):
        cv2.line(img, (x[j], y[j]), (x[j + 1], y[j + 1]), (255, 255, 255), 2)

 # Mostrar la imagen con la curva actual
    ventana = f"Curva Parametrica"
    cv2.imshow(ventana, img)
    cv2.waitKey(0)
    cv2.destroyWindow(ventana)

# Cerrar todas las ventanas al finalizar
cv2.destroyAllWindows()