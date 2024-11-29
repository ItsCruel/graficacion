import cv2
import numpy as np

# dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Vertices del prisma trapezoidal en coordenadas 3D
vertices = np.array([
    [-1, -1, -1],   
    [1, -1, -1],   
    [0.5, 0, -1], 
    [-0.5, 0, -1], 
    [-1, -1, 1],   
    [1, -1, 1],
    [0.5, 0, 1],
    [-0.5, 0, 1]
])

# Conexiones de los vertices para formar las aristas del prisma 
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  
    (4, 5), (5, 6), (6, 7), (7, 4),  
    (0, 4), (1, 5), (2, 6), (3, 7)   
]

def project_isometric(vertex):
    """Funcion para proyectar un punto 3D a 2D con proyeccion isometrica"""
    x, y, z = vertex
    x2D = x - z
    y2D = (x + 2 * y + z) / 2
    return int(x2D * 100 + WIDTH / 2), int(-y2D * 100 + HEIGHT / 2)

# Crear ventana
cv2.namedWindow("Prisma Trapezoidal Isometrico")

while True:
    # Crear imagen negra para el fondo
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Dibujar aristas del prisma
    for edge in edges:
        pt1 = project_isometric(vertices[edge[0]])
        pt2 = project_isometric(vertices[edge[1]])
        cv2.line(frame, pt1, pt2, (255, 255, 255), 2)

    # Mostrar imagen
    cv2.imshow("Prisma Trapezoidal Isometrico", frame)

    # Salir si 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()