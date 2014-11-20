import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, img = cap.read()
cv2.imshow('input', img)
cap.release()

# closeFlag = 0
# cap = cv2.VideoCapture(0)
# while( cap.isOpened() and closeFlag != 1):
#     ret, img = cap.read()
#     #cv2.imshow('input', img)

#     gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur( gray, (5,5), 0 )
#     blur2 = cv2.GaussianBlur( gray, (5,5), 0 )
#     blur3 = cv2.GaussianBlur( gray, (5,5), 0 )
#     blur4 = cv2.GaussianBlur( gray, (5,5), 0 )

#     ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY_INV)
#     ret,thresh2 = cv2.threshold(blur,127,255,cv2.THRESH_BINARY_INV)
#     cv2.imshow('treshold', thresh2)

#     contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#     firstloop = 1
#     ci = 0
#     for i in range(len(contours)):
#             cnt=contours[i]
#             area = cv2.contourArea(cnt)
#             if firstloop == 1:
#                 max_area = area
#                 firstloop = 0
#             if(area>max_area):
#                 max_area=area
#                 ci=i
#     cnt=contours[ci]
#     hull = cv2.convexHull(cnt)

#     # wykrywanie centroidu
#     moments = cv2.moments(cnt)
#     if moments['m00']!=0:
#                 cx = int(moments['m10']/moments['m00']) # cx = M10/M00
#                 cy = int(moments['m01']/moments['m00']) # cy = M01/M00

#     centr=(cx,cy)
#     cv2.circle(img,centr,10,[0,0,255],2)

#     drawing = np.zeros(img.shape,np.uint8)
#     cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
#     cv2.drawContours(drawing,[hull],0,(0,0,255),2)
#     cv2.circle(drawing,centr,10,[0,0,255],2)
#     cv2.circle(img,centr,10,[0,0,255],2)


#     cv2.imshow('input', img)

#     k = cv2.waitKey(10)
#     if k == 27:
#         break
