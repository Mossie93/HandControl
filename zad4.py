import cv2
import cv2.cv as cv
import numpy as np
from pymouse import PyMouse

m = PyMouse()
closeFlag = 0
cap = cv2.VideoCapture(0)
startFlag = 1
startFlag2 = 0
mx, my = m.position()

while( cap.isOpened() and closeFlag != 1):
    ret, img = cap.read()
    #cv2.imshow('input', img)
    if not ret:
        continue

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur( gray, (5,5), 0 )

    ret,thresh = cv2.threshold(blur,80,255,cv2.THRESH_BINARY_INV)
    ret,thresh2 = cv2.threshold(blur,80,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('treshold', thresh2)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    firstloop = 1
    ci = 0
    for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if firstloop == 1:
                max_area = area
                firstloop = 0
            if(area>max_area):
                max_area=area
                ci=i
    if ci < len(contours):
        cnt=contours[ci]
    hull = cv2.convexHull(cnt)

    # wykrywanie centroidu
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00

    previous_centr = centr if 'centr' in globals() else (cx,cy)
    centr=(cx,cy)
    px, py = previous_centr

    dx = px - cx
    dy = cy - py
    cursor_x, cursor_y = m.position()
    m.move(cursor_x + dx, cursor_y + dy)

    cv2.circle(img,centr,10,[0,0,255],2)

    drawing = np.zeros(img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
    cv2.drawContours(drawing,[hull],0,(0,0,255),2)
    cv2.circle(drawing,centr,10,[0,0,255],2)
    cv2.circle(img,centr,10,[0,0,255],2)


    cv2.imshow('input', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()