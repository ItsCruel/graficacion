import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('salida.png')

# Convertir la imagen a espacio de color HSV para mejor segmentación
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Rango de color Azul
lower_blue = np.array([100, 120, 70])
upper_blue = np.array([140, 255, 255])

# Rango de color Verde
lower_green = np.array([35, 120, 70])
upper_green = np.array([85, 255, 255])

# Rango de color Naranja
lower_orange = np.array([10, 120, 70])
upper_orange = np.array([30, 255, 255])

# Rango de color Rosa
lower_pink = np.array([140, 120, 70])
upper_pink = np.array([170, 255, 255])

# Crear mascaras
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask_red = cv2.bitwise_or(mask_red1, mask_red2)

mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask_green = cv2.inRange(hsv, lower_green, upper_green)
mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

combined_mask = mask_red | mask_blue | mask_green | mask_orange | mask_pink

kernel = np.ones((5, 5), np.uint8)
morph_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(morph_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def count_objects_by_color(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)

# Contar los objetos para cada color
red_count = count_objects_by_color(mask_red)
blue_count = count_objects_by_color(mask_blue)
green_count = count_objects_by_color(mask_green)
orange_count = count_objects_by_color(mask_orange)
pink_count = count_objects_by_color(mask_pink)

# Mostrar los resultados
print(f"Objetos Rojos: {red_count}")
print(f"Objetos Azules: {blue_count}")
print(f"Objetos Verdes: {green_count}")
print(f"Objetos Naranjas: {orange_count}")
print(f"Objetos Rosas: {pink_count}")


result_image = image.copy()

cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)  
cv2.imshow("Detected Objects", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
