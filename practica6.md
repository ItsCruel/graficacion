## Practica 6 

### Instrucciones 
para esta practica el profe nos pidio hacer 10 parametricas vistas en clase 

como siempre paso 0 importamos el nummpy y el cv 

```
import numpy as np
import cv2
```
### Definimos el  tamaño de la imagen , yo use un 800 x 800 en blanco y la inicalizamos en negro
ancho, alto = 800, 800
img = np.zeros((alto, ancho, 3), dtype=np.uint8)


### Calculamos el centro de la imagen
```
centro_x, centro_y = ancho // 2, alto // 2
```

 `centro_x, centro_y`: Coordenadas del centro de la imagen. Se utilizan para centrar las curvas en la imagen.

 `t = np.linspace(0, 2 * np.pi, 1000)`: Genera un conjunto de valores de `t` entre 0 y (2π), creando un total de 1000 puntos para suavizar las curvas.


### Definimos mis curvas Parametricas

Cada curva se dibuja de acuerdo a una ecuacion en particular:

<p>
***Círculo***: Los puntos de `x` e `y` se calculan usando funciones trigonometricas, escalados por un radio de 180.

```
if eq == 0:
    # Círculo
    x = 180 * np.cos(t)
    y = 180 * np.sin(t)
```
![circulo](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/circulo.png?raw=true)

</p>

<p>
**Elipse**: Parecida al circulo, pero con radios diferentes en los ejes `x` y `y`.

```
elif eq == 1:
    # Elipse
    x = 220 * np.cos(t)
    y = 120 * np.sin(t)
```
![Elipse](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/elipse.png?raw=true)
</p>

<p>
- **Espiral Logarítmica**: A medida que `t` aumenta, `r` crece de forma exponencial, produciendo una espiral.
```
elif eq == 2:
    # Espiral logaritmica
    r = np.exp(0.9 * t)
    x = r * np.cos(t)
    y = r * np.sin(t)
```

![Espiral Logaritmica](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/espiral%20logaritmica.png?raw=true)
</p>

<p>
**Lemniscata** : una figura en forma de ∞ o infinito:
  
  ```
  elif eq == 3:
      x = 180 * np.cos(t) / (1 + np.sin(t)**2)
      y = 180 * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)
  ```
![Lemnistica](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/infinito.png?raw=true)

</p>

<p>
- **Rosa de 3 petalos**:
Son curvas parametrizadas que se generan con un parámetro k que controla el numero de petalos. 

  ```
  elif eq == 4:
      k = 3
      r = 180 * np.cos(k * t)
      x = r * np.cos(t)
      y = r * np.sin(t)
  ```

![Rosa de 3 petalos](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/petalos.png?raw=true)

</p>

<p>
- **Cardioide**:
Un cardioide es  una curva en forma de corazon que se genera usando una formula paramétrica específica La forma es simetrica y característica por su unico bucle.

  ```
  elif eq == 5:
      x = 180 * (1 - np.cos(t)) * np.cos(t)
      y = 180 * (1 - np.cos(t)) * np.sin(t)
  ```
![cardioide](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/cardioide.png?raw=true)
</p>


<p>
  **Hipociclo**:
  Un hipociclo es una curva generada por un punto en el borde de un circulo pequeño que rueda sin deslizarse dentro de otro circulo mas grande. 

  ```
    R, r, d = 180, 40, 40
    x = (R - r) * np.cos(t) + d * np.cos(((R - r) / r) * t)
    y = (R - r) * np.sin(t) - d * np.sin(((R - r) / r) * t)
    elif eq == 7:
```
![Hipociclo](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/hipociclo.png?raw=true)
 </p>

  **Espiral de arquimedes** :
  La espiral de Arquimedes es una curva en la que la distancia entre las vueltas sucesivas aumenta de forma lineal. 

  
    a, b = 1, 15
    r = a + b * t
    x = r * np.cos(t)
    y = r * np.sin(t)
    elif eq == 8:


 ![Espiral de Arquimedes](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/espiral.png?raw=true)
 

  **Asteroide**
   Un asteroide es una curva en forma de estrella con cuatro "lobulos" o picos.
  
    x = 180 * (np.cos(t)**3)
    y = 180 * (np.sin(t)**3)
    elif eq == 9:
    
    ![Asteroide](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/astroide.png?raw=true)

    **Hiperbola**
    Una hiperbola es una curva simetrica que tiene dos ramas que se alejan indefinidamente. 

    
     x = 180 * np.sinh(t)
     y = 130 * np.cosh(t)
    

     ![Hiperbola](https://github.com/ItsCruel/graficacion/blob/main/imagenes%20markdown/hiperbolaa.png?raw=true)
  


nadamas nos queda mostrar los resultados y cerrar el programa

cv2.imshow("Curvas Parametricas", img)
cv2.waitKey(0)
cv2.destroyAllWindows()