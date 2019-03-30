import cv2
import numpy as np
import serial


def line(img, ser):
    crop_img = img[400:480, 0:640]
    crop_img = cv2.resize(crop_img, (160, 20))
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    _, contours, __ = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        if w < 130:
            M = cv2.moments(c)
            cx = int(M['m10'] / (M['m00']+0.0001))
            cy = int(M['m01'] / (M['m00']+0.0001))
            s = '222' + str(cx) + '\n'
            ser.write(s.encode())
            s = ''
            res = ('line')
        else:
            res = ('cross')
            
        return res
