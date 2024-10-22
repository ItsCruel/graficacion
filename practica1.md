**PRACTICA1 ***

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

utilizando esta pieza de codigo se crea un rectangulo ,  utilizando (200 , 230) a (259, 269),crea un seccion vertical d 60 x 40 pixeles , los valores de los pixeles se establecen en 60 para la parte de arriba del hongo utilizando este codigo :
for i in range (140,200):
    for j in range (180 , 320):
    img [i, j] = 100
Se utiliza para generar un rectangulo en forma horizontal , los pixeles van desde (140,180)
a (199 , 319) creando el rectangulo de 60  x 40 pixeles.

***Monstrando Imagen***
por ultimo quede mostrar el resultado del pixel art 
[champiñon pixel art] [pixelarthongo.png]

    

