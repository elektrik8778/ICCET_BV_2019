import cv2
import numpy as np
import serial
import time
#import RPi.GPIO as GPIO
import tl
import MatchTemplate as mt
import line

cap = cv2.VideoCapture(0)
ser = serial.Serial('/dev/ttyACM0', 9600)

'''KEY = 17
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN)'''

noDrive = cv2.imread("noDrive.png")
pedistrain = cv2.imread("pedistrain.png")

noDrive = cv2.resize(noDrive, (64, 64))
pedistrain = cv2.resize(pedistrain, (64, 64))
noDrive = cv2.cvtColor(noDrive, cv2.COLOR_BGR2GRAY)
pedistrain = cv2.cvtColor(pedistrain, cv2.COLOR_BGR2GRAY)
noDrive = cv2.Canny(noDrive, 50, 200)
pedistrain = cv2.Canny(pedistrain, 50, 200)

W, H = 64, 64
w, h = 240, 320
width = w-W+1
height = h-H+1

NoDr, Noth, Ped = 0, 0, 0

#cv2.imshow("NoDrive", noDrive)

for i in range(1500):
    ser.flushInput()
    ser.flushOutput()
    ser.flush()
    ret, frame = cap.read()
    crop_frame = frame[:240, 320:]
    res = mt.signs(crop_frame, noDrive, pedistrain, W, H, w, h)
    if res == 'NoDr':
        NoDr += 1
    elif res == 'Ped':
        Ped += 1
    else:
        Noth += 1
        
    if max(NoDr, Ped, Noth) >= 15:
        if max(NoDr, Ped, Noth) == NoDr:
            maxZ = "NoDrive"
        elif max(NoDr, Ped, Noth) == Ped:
            maxZ = "Pedistrain"
        elif max(NoDr, Ped, Noth) == Noth:
            maxZ = "Nothing"

        
        print(maxZ, '  ||  ')
          
        NoDr, Noth, Ped = 0, 0, 0
    #line.line(frame, ser)
    
    #print(tl.traffic_lights(crop_frame))
    cv2.imshow("frame", frame)
    #print(time.clock())
    '''if time.clock() >= 70.0:
        break'''
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
