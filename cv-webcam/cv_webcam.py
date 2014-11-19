import numpy as np
import cv2
import cv2.cv as cv
import time

cap = cv2.VideoCapture(0)
start_time = time.time()

palm_cascade = cv.Load('palm.xml')
fist_cascade = cv.Load('fist.xml')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray_mat = cv.fromarray(gray)
    palms = cv.HaarDetectObjects(gray_mat, palm_cascade, cv.CreateMemStorage(0), 1.1, 8)
    fists = cv.HaarDetectObjects(gray_mat, fist_cascade, cv.CreateMemStorage(0), 1.1, 8)
    
    for (x, y, w, h), n in palms:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255))
    for (x, y, w, h), n in fists:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()