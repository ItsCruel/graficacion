**practica 2**

***Instrucciones***
generar al menos cinco operadores puntuales utilizando la imagen generada o una imagen previamente cargada

***Descripcion***
Este codigo lo voy a usar para realizar diverdas transformaciones sobre una misma imagen , como escala de grises , umbralizacion  , inversion de colores , ajuste de brillo y contraste.

bueno como paso 0 importamos las librerias numpy y cv y una vez con esto podemos comenzar


~~~
python
import cv2
import numpy as np  
~~~

Como paso 1 necesitamos cargar imagen , en mi caso use una de halo del personaje emile

~~~
image = cv2.imread('emile.png')
~~~

Una vez cargada la imagen 'emile.png' la cambiamos por una variable llamada imagen.

Como primer operador vamos a poner a escala de grises la imagen utilizando :

~~~
cv2.cvtColor
~~~

y para hacer la conversion a gris utilizamos:

~~~
imagenGris=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
~~~

como segundo operador decidi hacer una umbrealizacion se aplicaun umbral binario a la imagen en escala de grises.
Lospixeles con un valor superior a 127 se establecen en blanco (255), y los pixeles con unn valor inferior se establecen en negro (0).

~~~
imagenUmbral=cv2.threshold (imagenGris,127,255,cv2.THRESH_BINARY) 
~~~

como tercer operador decidi hacer una inversion de colores , por medio del bitwise not, lo que hace es que invierte los colores de la imagen original , transformando pixeles claros en oscuros y viceversa.
~~~
imagenInvertida=cv2.bitwise_ not(imagen) 
~~~

como cuarto operador elegi hacer un ajuste de brillo , para esto usamos  moviendo el alfa a 1 y el beta al 50
~~~
imagenBrillante = cv2.convertScaleAbs(imagen, alpha=1, beta=50)
~~~


como quinto operador realice un ajuste en el contraste para esto usamos el convertScaleAbs y seteamos el alpha en 1.5 y beta en 0.

~~~
cv2.convertScaleAbs(imagen,alpha=1.5,beta=0)
~~~


como paso final nadamas nos queda mostrar el resultado de nuestro trabajo con el siguiente codigo :

~~~
cv2.imshow ('imagen normal', imagen)
cv2.imshow('Imagen con escala de grises', imagenGris)
cv2.imshow('imagen con Umbralizacion', imagenUmbral)
cv2.imshow('imagen Brillo Aumentado', imagenBrillante)
cv2.imshow('imagen Invertida', imagenInvertida)
cv2.imshow ('imagen con Contraste ', imagenContraste)
~~~

aqui las imagenes de como queda cada una

**mostrando resultados**
- 'Imagen Original'
![Emile original](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/emile.png?raw=true)
- 'Escala de Grises'
![Escala de grises ](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/imagenEscaladegrises.png?raw=true)
- 'Umbralizacion'
![Emile Umbralizacion](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/imagenUmbrealizacion.png?raw=true)
- 'Inversion de Colores'
![Emile Inversion de Colores](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/imageninvertida.png?raw=true)
- 'Brillo Aumentado'
![Emile Brillo Aumentado](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/imagenbrilloaumentado.png?raw=true)
- 'Contraste Aumentado'
![Emile Contraste aumentado](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/imagen%20contraste.png?raw=true)

por ultimo se cierra el programa 

~~~
cv2.waitKey(0)
cv2.destroyAllWindows()
~~~