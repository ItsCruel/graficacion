import numpy as np
import cv2 as cv

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)


mascara = cv.imread('mascara.png', cv.IMREAD_UNCHANGED)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in rostros:
        # Redimensionar la mascara al tamaño del rostro detectado
        resized_mascara = cv.resize(mascara, (w, h))

        
        if resized_mascara.shape[2] == 4:
            b, g, r, alpha = cv.split(resized_mascara)
            overlay_color = cv.merge((b, g, r))
            mask_inv = cv.bitwise_not(alpha)
        else:
            overlay_color = resized_mascara
            mask_inv = np.ones((h, w), dtype="uint8") * 255

     
        roi = frame[y:y+h, x:x+w]
        background = cv.bitwise_and(roi, roi, mask=mask_inv)
        foreground = cv.bitwise_and(overlay_color, overlay_color, mask=alpha if resized_mascara.shape[2] == 4 else mask_inv)


        combined = cv.add(background, foreground)
        frame[y:y+h, x:x+w] = combined

    cv.imshow('rostros', frame)
    k = cv.waitKey(1)
    if k == 27:  
        break

cap.release()
cv.destroyAllWindows()
