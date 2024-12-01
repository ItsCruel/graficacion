import numpy as np
import cv2 as cv

#  detector de ojos
ojos_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')

mascara = cv.imread('ojos1.png', cv.IMREAD_UNCHANGED)  

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ojos = ojos_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in ojos:
       
        width_ratio = 1.8  
        new_w = int(w * width_ratio)
        new_h = int(new_w * mascara.shape[0] / mascara.shape[1])
        resized_mascara = cv.resize(mascara, (new_w, new_h))

        y_offset = int(y - new_h / 2)
        x_offset = x - int((new_w - w) / 2)

        # Manejo transparencia
        if resized_mascara.shape[2] == 4:
            b, g, r, alpha = cv.split(resized_mascara)
            overlay_color = cv.merge((b, g, r))
            mask_inv = cv.bitwise_not(alpha)
        else:
            overlay_color = resized_mascara
            mask_inv = np.ones((new_h, new_w), dtype="uint8") * 255

        roi = frame[y_offset:y_offset + new_h, x_offset:x_offset + new_w]

        if roi.shape[0] == new_h and roi.shape[1] == new_w:
            background = cv.bitwise_and(roi, roi, mask=mask_inv)
            foreground = cv.bitwise_and(overlay_color, overlay_color, mask=alpha if resized_mascara.shape[2] == 4 else mask_inv)
            combined = cv.add(background, foreground)
            frame[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = combined

    cv.imshow('Lentes', frame)
    if cv.waitKey(1) & 0xFF == 27: 
        break

cap.release()
cv.destroyAllWindows()
