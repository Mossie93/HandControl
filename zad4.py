import cv2
import cv2.cv as cv
import numpy as np
from pymouse import PyMouse

m = PyMouse()
closeFlag = 0
cap = cv2.VideoCapture(0)
startFlag = 1
startFlag2 = 0

palm_cascade = cv.Load('palm.xml')
fist_cascade = cv.Load('fist.xml')

last_frames = []

state = 'waiting'

def update_buffer(info):
    last_frames.append(info)
    if len(last_frames) > 20:
        del last_frames[0]

def print_info(buffer, state):
    print state,
    palm_count = [x for (x,y) in last_frames].count('p') # last_frames.count(['p'])
    fist_count = [x for (x,y) in last_frames].count('f')
    for i in [str for [str, b] in last_frames]:
        print i,
    print "%d palms\t%d fists" % (palm_count, fist_count),
    print hand_coords(buffer),
    print hand_deltas(buffer),
    print last_frames[-1]

def change_state(new_state):
    globals()['state'] = new_state

def hand_coords(buffer, index=-1):
    rect = buffer[index][1]
    if len(rect) > 0:
        img_x, img_y = rect[0:2]
        img_x += rect[2]/2
        img_y += rect[3]/2
    else:
        img_x, img_y = (-1, -1)
    return img_x, img_y

def previous_hand_coords(buffer):
    for i in range(2, len(buffer)):
        hc = hand_coords(buffer, len(buffer)-i)
        if hc != (-1, -1):
            return hc
    return hand_coords(buffer)

def hand_deltas(buffer):
    prev = previous_hand_coords(buffer)
    hand_x, hand_y = hand_coords(buffer)
    if prev != (-1, -1):
        previous_x, previous_y = prev 
    else:
        previous_x, previous_y = (hand_x, hand_y)
    
    if (previous_x, previous_y) != (-1, -1) and (hand_x, hand_y) != (-1, -1):
        dx, dy = hand_x - previous_x, hand_y - previous_y
    elif (hand_x, hand_y) == (-1, -1):
        dx, dy = (0, 0)
    else:
        dx, dy = (0, 0)
    return dx, dy

def cursor_deltas(buffer):
    if hand_deltas(buffer) != (0, 0):
        hdx, hdy = hand_deltas(buffer)
        _hdx, _hdy = abs(hdx), abs(hdy) # always positive - can be raised to fractional power
        a = 0.6
        exponent = 2
        dx, dy = (np.sign(hdx)*(a*_hdx**exponent), np.sign(hdy)*(a*_hdy**exponent))
        if dx < 30:
            dx /= 5
        if dy < 30:
            dy /= 5
        return dx, dy
    else:
        return (0, 0)

def current_gesture(buffer):
    return [str for [str, b] in buffer][-1]

def do_action(buffer, state):
    last_detections = [str for [str, b] in buffer]
    palms_count = last_detections.count('p')
    fists_count = last_detections.count('f')
    if state == 'waiting':
        if fists_count > 15:
            change_state('fist')
    elif state == 'fist':
        if fists_count < 3 and palms_count < 3:
            change_state('waiting')
        if last_detections[len(last_detections)-5:].count('p') == 5:
            change_state('cursor')
    elif state == 'cursor':
        if current_gesture(buffer) == 'p':
            pos_x, pos_y = m.position()
            print current_gesture(buffer)
            dx, dy = cursor_deltas(buffer)
            try:
                m.move(pos_x - dx, pos_y + dy)
            except Error:
                pass
        elif current_gesture(buffer) == 'f':
            if last_detections[len(last_detections)-3:].count('f') == 2:
                x, y = m.position()
                m.click(x, y, 1)
                change_state('clicking')        
        if fists_count == 0 and palms_count == 0:
            change_state('waiting')
    elif state == 'clicking':
        if last_detections[len(last_detections)-3:].count('f') == 0:
            change_state('cursor')

while( cap.isOpened() and closeFlag != 1):
    ret, img = cap.read()
    #cv2.imshow('input', img)
    if not ret:
        continue

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur( gray, (5,5), 0 )

    gray_mat = cv.fromarray(gray)
    palms = cv.HaarDetectObjects(gray_mat, palm_cascade, cv.CreateMemStorage(0), 1.1, 5)
    fists = cv.HaarDetectObjects(gray_mat, fist_cascade, cv.CreateMemStorage(0), 1.1, 13)
    #   print palms, fists

    in_this_frame = ['-', ()]

    # Detect largest fist and palm, filter out junk detections
    if len(fists) > 0:
        largest_fist = max(fists, key=lambda ((x, y, w, h), n): w * h)
        x, y, w, h = largest_fist[0]
        if w * h > 70 * 70:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0))
            in_this_frame[0] = 'f'
            in_this_frame[1] = (x, y, w, h)

    if len(palms) > 0:
        largest_palm = max(palms, key=lambda ((x, y, w, h), n): w * h)
        x, y, w, h = largest_palm[0]
        if w * h > 70 * 70:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255))
            in_this_frame[0] = 'p'
            in_this_frame[1] = (x, y, w, h)


    update_buffer(in_this_frame)

    # do the right action based on current buffer and state
    do_action(last_frames, state)

    print_info(last_frames, state)

    cv2.imshow('input', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()