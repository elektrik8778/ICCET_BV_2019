import cv2
import numpy as np
import serial
from queue import Queue

def signs(crop_frame, noDrive, pedistrain, W, H, w, h):

    gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 400)

    resultN = cv2.matchTemplate(edged, noDrive, cv2.TM_CCOEFF)
    resultP = cv2.matchTemplate(edged, pedistrain, cv2.TM_CCOEFF)
    min_valN, max_valN, min_locN, max_locN = cv2.minMaxLoc(resultN)
    min_valP, max_valP, min_locP, max_locP = cv2.minMaxLoc(resultP)
    bottom_rightN = (max_locN[0] + W, max_locN[1] + H)
    bottom_rightP = (max_locP[0] + W, max_locP[1] + H)
    
    if min_valN <= -1500000.0 and min_valN >= -2250000.0:
        cv2.rectangle(crop_frame, max_locN, bottom_rightN, (0, 0, 255), 2)
        res = ("NoDr")
        
    elif min_valP <= -2900000.0 and min_valP >= -3900000.0:
        cv2.rectangle(crop_frame, max_locP, bottom_rightP, (255, 0, 0), 2)
        res = ("Ped")
        
    else:
        res = ("Noth")
        
    return res
