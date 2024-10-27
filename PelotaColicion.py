'pixel-art-hongo'
#
[i, j]
import cv2
import numpty as np 


# Dimensiones 
w, h = 640, 480


# Crear ventana 
cv2.namedWindow("Anim",cv2.WINDOW_AUTOSIZE)


# Posiciones iniciales
p_azul= np.array([200,200])
p_roja= np.array([300,300])
r=20 # radio de las pelotitas 


# Velocidades 
v_azul=np.array([5, 3])
v_roja=np.array([0, 0])


#Colores
c azul = (255,0,0)
c roja = (0,0,255)


#Bucle de animacion 
while True:
    #Fondo negro
    frame= np.zeros((h, w, 3),dtype=np.uint8)


    # Dibujar pelotitas
    cv2.circle(frame, p azul,r,c azul, -1)
    cv2.circle(frame,p_roja,r,c roja,-1)

    # Mover azul 
    p azul += v azul


    # Colisiones azul
    if p_azul[0]-r<0 or p_azul[0] + r>=w:
        v_azul[0]= -v_azul[0]


     if p_azul[1]-r<=0 or p_azul[1] + r>=h:
            v_azul[1] = -v_azul[1]


     #Proximidad
    dist= np.linalg.norm(p azul- p roja)
    if dist < 2 * r:
     
     #Mover roja a posicion aleatoria 
     p_roja = np.array(np.random.randint(r, w -r)),
