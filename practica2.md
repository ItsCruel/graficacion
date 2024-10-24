**practica 3**

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

