##PRACTICA 4

###Ecuaciones Paramétricas

Las ecuaciones parametricas son un conjunto de ecuaciones que representan una relacion entre variables mediante la introducción de una o más variables adicionales, llamadas parámetros. A diferencia de las ecuaciones estandar, que expresan una variable en funcion de otra, las ecuaciones parametricas describen las variables en terminos de un parametro comun, lo que permite una representacion mas flexible de diversas relaciones.

**Definición**

Las ecuaciones paramétricas utilizan uno o mas parametros para expresar una o mas variables. Esto es especialmente util en geometría y fisica, donde se requieren representaciones mas complejas que las que podrían ofrecer las ecuaciones en forma estadar. Al introducir un parametro, se puede representar una variedad de formas y trayectorias que son dificiles de describir con ecuaciones algebraicas tradicionales.
<b>
Ejemplos :
</b>
<b>
1. Elipse:
   
     x(t) = aCos(t)
     y(t) = bSin(t)
   
a  y b siendo semiejes de la elipse. El parámetro ( t ) varía de (0) a ( 2π). Este tipo de parametrizacion es fundamental en la representacion de orbitas elípticas en física y astronomía.
</b>

<b>
2. Hiperbola:

x(t) = aSec(t)
y(t) = bTan(t)
  
a y  b son constantes que determinan la forma de la hiperbola. Las hiperbolas son comunes en la teoría de funciones y en aplicaciones de ingenieria.
</b>

<b>
3. Trayectorias de Movimiento:
dato : Un objeto lanzado puede ser modelado con ecuaciones parametricas
     x(t) = v0Cos(θ)t
     y(t) = v0Sin(θ)t - 1/2g*t^2
   
 Aqui, v0 es la velocidad inicial( θ) es el ángulo de lanzamiento y ( g ) es la aceleracion debida a la gravedad. Este modelo es bastante bueno  para predecir la trayectoria de proyectiles.
</b>

 **Aplicaciones de las Ecuaciones Parametricas**
 1. Ingenieria:
Se utilizan en el diseño de estructuras y componentes. Por ejemplo, las trayectorias de cargas en un puente o las trayectorias de vehículos en un sistema de trafico se modelan con ecuaciones parametricas para asegurar la estabilidad y la funcionalidad de los diseños.

2. Animacion y Modelado 3D:
En graficos por computadora, las ecuaciones parametricas permiten crear curvas suaves y superficies complejas, facilitando la representacion de objetos tridimensionales. Esto es importante en la creacion de videojuegos y películas animadas.

3. Robotica:
En la planificacion de trayectorias, las ecuaciones parametricas son fundamentales para mover brazos roboticos o vehiculos autonomos a lo largo de rutas específicas. Permiten calcular movimientos precisos en entornos variables.

4. Meteorología y Navegación:
 Se emplean para modelar la trayectoria de masas de aire o para calcular rutas optimas en la navegación. Esto es vital en la predicción del clima y en la logística de transporte.

 **Otros Conceptos Matematicos**
 
Curvas y Superficies en el Espacio:

Las ecuaciones parametricas pueden extenderse a tres dimensiones. Por ejemplo, una curva en el espacio tridimensional puede estar representada por:
   1. x(t) = f(t)
   2. y(t) = g(t)
   3. z(t) = h(t)
   
 Esta extension es fundamental en la visualizacion y simulación de fenomenos en fisica y diseño.

**Geometria Analitica**:
Las ecuaciones parametricas son una extension de la geometria analítica, donde se utilizan para describir figuras geometricas de forma más general. Permiten analizar las propiedades de las curvas y superficies de manera más profunda.

**Calculo**:
En calculo, las ecuaciones parametricas permiten estudiar la velocidad y aceleracion a lo largo de una curva al diferenciar las funciones respecto al parametro. La derivada de una curva parametrizada se puede expresar como:

dydx=y′(t)x′(t)
   
Este concepto es  muy importante en la fisica y la ingeniería para el analisis de movimiento.
Graficas de Ecuaciones Parametricas

Las graficas de ecuaciones parametricas se trazan al calcular los puntos x(t), y(t) para diversos valores del parametro (t). Este metodo es especialmente util cuando la forma de la curva es complicada y no se puede expresar facilmente en forma cartesiana.

 Ejemplo de Graficacion en Python

Aqui se muestra como graficar una circunferencia utilizando ecuaciones parametricas:

```python
import numpy as np
import matplotlib.pyplot as plt

# Definir el rango del parametro t
t = np.linspace(0, 2 * np.pi, 100)

# Ecuaciones parametricas de la circunferencia
r = 1  # Radio
x = r * np.cos(t)
y = r * np.sin(t)

# Graficar
plt.figure(figsize=(6, 6))
plt.plot(x, y, label='Circunferencia')
plt.title('Circunferencia con Ecuaciones Parametricas')
plt.xlabel('x(t) = r * cos(t)')
plt.ylabel('y(t) = r * sin(t)')
plt.axis('equal')  # Para mantener la proporcion
plt.grid(True)
plt.legend()
plt.show()
```
##¿Para que nos sirve?

Las ecuaciones parametricas son una herramienta muy buena para  diversas disciplinas. 
Su utilidad radica en su capacidad para modelar situaciones que no pueden describirse facilmente mediante ecuaciones algebraicas tradicionales. 
Proporcionan una alta  flexibilidad en la representacion de formas y movimientos, permitiendo a los investigadores y profesionales abordar problemas complejos en diversas aplicaciones. 
Desde el diseño grafico hasta la ingenieria, su versatilidad las convierte en una parte integral del analisis matematico y cientifico.


##Conclusion
Las ecuaciones parameetricas son fundamentales en matemaaticas y sus aplicaciones abarcan multiples campos. 
Permiten describir fenomenos complejos y proporcionar un marco para el analisis de trayectorias y formas en geometria y fisica.
 Su capacidad para simplificar la representacion de curvas y superficies las convierte en una herramienta invaluable en la ciencia y la ingeniería. 
 Con su versatilidad y adaptabilidad, las ecuaciones parametricas continuaran siendo un tema de gran interes en la investigacion y el desarrollo de nuevas tecnologías.
