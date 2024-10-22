**PRACTICA1 **

***Descripcion***
Para esta practica se solicito generar una imagen tipo pixel art utilizando una matriz de enteros en el rango de 0 a 255.

como paso 0 decidi que queria hacer un hongo del minecraft de los que son como cafecitos
[champiñonMinecraft][hongo.png]


comopaso 1 se creo una imagen , yo decidi hacerla de 500 x 500 pixeles , el tipo de dato unit8 quiere decir que cada valor de pixel tiene 8 bits y luego se multiplico por 240 que da un fondo gris claro 

img = np.ones((500,500), dtype=np.uint8)* 240
para la parte 2 comenzamos a detallar el champiñon , con el tronco 

for i in range (200, 260):
    for j in range (230,270):
    img [i, j] = 60
    

