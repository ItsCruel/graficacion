import numpy as np
import cv2 as cv

# dimensiones de la ventana
ancho, alto = 640, 480

# crear ventana
cv.namedWindow("Animacion", cv.WINDOW_AUTOSIZE)

# posicion inicial de la pelota
pos_pelota = np.array([100, 100]) 
radio_pelota = 20
velocidad = np.array([5, 3])

# color fijo de la pelota
color_pelota = (255, 0, 0)

# bucle de animacion
while True:
    # Crear fondo
    fotograma = np.zeros((alto, ancho, 3), dtype=np.uint8)
    
    # dibujar divisiones para los sectores
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

    # Dibujar la pelotita
    cv.circle(fotograma, tuple(pos_pelota), radio_pelota, color_pelota, -1)
    
    # Mostrar el sector en el que se encuentra la pelotita
    texto_sector = f"Sector: {sector}"
    cv.putText(fotograma, texto_sector, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Actualizar la posicion de la pelota
    pos_pelota += velocidad
    
    # Comprobar colisiones y cambiar direccion
    if pos_pelota[0] - radio_pelota <= 0 or pos_pelota[0] + radio_pelota >= ancho:
        velocidad[0] = -velocidad[0]

    if pos_pelota[1] - radio_pelota <= 0 or pos_pelota[1] + radio_pelota >= alto:
        velocidad[1] = -velocidad[1]
    
    # Mostrar la imagen en la ventana
    cv.imshow("Animacion", fotograma)

    # Salir al presionar 'Esc'
    if cv.waitKey(1) & 0xFF == 27:
        break

# Cerrar todas las ventanas de OpenCV
cv.destroyAllWindows()
