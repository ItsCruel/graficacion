import numpy as np
import cv2 as cv


# dimensiones de la ventana
ancho, alto = 640, 480

# crear ventana
cv.namedWindow("Animacion", cv.WINDOW_AUTOSIZE)

# posicion inicial
pos_pelota = np.array([100, 100])
radio_pelota = 20
velocidad = np.array([5, 3])

# Color fijo de la pelotita 
color_pelota = (255, 0, 0)

# Bucle de animacion
while True:
    # crear fondo
    fotograma = np.zeros((alto, ancho, 3), dtype=np.uint8)
    
    # dibujar divisiones
    cv.line(fotograma, (ancho // 2, 0), (ancho // 2, alto), (255, 255, 255), 2)
    cv.line(fotograma, (0, alto // 2), (ancho, alto // 2), (255, 255, 255), 2)
    
    # determinar el sector en el que se encuentra la pelota
    if pos_pelota[0] < ancho // 2 and pos_pelota[1] < alto // 2:
        sector = 1
    elif pos_pelota[0] >= ancho // 2 and pos_pelota[1] < alto // 2:
        sector = 2
    elif pos_pelota[0] < ancho // 2 and pos_pelota[1] >= alto // 2:
        sector = 3
    else:
        sector = 4

    # dibujar la pelotita
    cv.circle(fotograma, tuple(pos_pelota), radio_pelota, color_pelota, -1)
    
    # mostrar el sector en la ventana
    texto_sector = f"Sector: {sector}"
    cv.putText(fotograma, texto_sector, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # actualizar posicion de la pelota
    pos_pelota += velocidad
    
    # comprobar colisiones y cambiar direccion
    if pos_pelota[0] - radio_pelota <= 0 or pos_pelota[0] + radio_pelota >= ancho:
        velocidad[0] = -velocidad[0]

    if pos_pelota[1] - radio_pelota <= 0 or pos_pelota[1] + radio_pelota >= alto:
        velocidad[1] = -velocidad[1]
    
    # Mostrar imagen
    cv.imshow("Animacion", fotograma)

    # Salir 
    if cv.waitKey(1) & 0xFF == 27:
        break
cv.destroyAllWindows()
