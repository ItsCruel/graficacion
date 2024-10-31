import cv2
import numpy as np

# tamaño
WIDTH, HEIGHT = 800, 600

# Vertice del prisma en coordenadas 3D
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
