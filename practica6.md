
## Practica 10  Parametricas

Instrucciones 
para esta practica el profe nos pidio hacer 10 parametricas vistas en clase 

como siempre paso 0 importamos el nummpy y el cv 
```python
import numpy as np
import cv2

# Definimos el  tamaño de la imagen , yo use un 800 x 800 en blanco y la inicalizamos en negro
ancho, alto = 800, 800
img = np.zeros((alto, ancho, 3), dtype=np.uint8)


### Calculamos el centro de la imagen

```
centro_x, centro_y = ancho // 2, alto // 2
```

 `centro_x, centro_y`: Coordenadas del centro de la imagen. Se utilizan para centrar las curvas en la imagen.





- `t = np.linspace(0, 2 * np.pi, 1000)`: Genera un conjunto de valores de `t` entre 0 y (2π), creando un total de 1000 puntos para suavizar las curvas.
---

### Definimos mis curvas Parametricas

Cada curva se dibuja de acuerdo a una ecuacion en particular:

<p>
**Círculo**: Los puntos de `x` e `y` se calculan usando funciones trigonometricas, escalados por un radio de 180.

```python
if eq == 0:
    # Círculo
    x = 180 * np.cos(t)
    y = 180 * np.sin(t)
```
![circulo]()

</p>

<p>
- **Elipse**: Parecida al circulo, pero con radios diferentes en los ejes `x` y `y`.

```python
elif eq == 1:
    # Elipse
    x = 220 * np.cos(t)
    y = 120 * np.sin(t)
```
![Elipse]()
</p>

<p>
- **Espiral Logarítmica**: A medida que `t` aumenta, `r` crece de forma exponencial, produciendo una espiral.

```python
elif eq == 2:
    # Espiral logaritmica
    r = np.exp(0.1 * t)
    x = r * np.cos(t)
    y = r * np.sin(t)
```
![Espiral Logaritmica]()
</p>
<p>
**Lemniscata** : una figura en forma de ∞ o infinito:
  
  ```python
  elif eq == 3:
      x = 180 * np.cos(t) / (1 + np.sin(t)**2)
      y = 180 * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)
  ```
![Lemnistica]()

</p>

<p>
- **Rosa de 3 petalos**:
Son curvas parametrizadas que se generan con un parámetro k que controla el numero de petalos. 

  ```python
  elif eq == 4:
      k = 3
      r = 180 * np.cos(k * t)
      x = r * np.cos(t)
      y = r * np.sin(t)
  ```

![Rosa de 3 petalos]()

</p>

- **Cardioide**:
Un cardioide es  una curva en forma de corazon que se genera usando una formula paramétrica específica La forma es simetrica y característica por su unico bucle.
  ```python
  elif eq == 5:
      x = 180 * (1 - np.cos(t)) * np.cos(t)
      y = 180 * (1 - np.cos(t)) * np.sin(t)
  ```
![cardioide]()


</p>

 Mostrando las imagenes con las curvas
nadamas nos queda mostrar los resultados y cerrar el programa
```python
cv2.imshow("Curvas Parametricas", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

