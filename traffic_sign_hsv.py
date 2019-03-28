import cv2
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

cap = cv2.VideoCapture(0)

noDrive = cv2.imread("noDrive.png")
pedistrain = cv2.imread("pedistrain.png")

noDrive = cv2.resize(noDrive, (64, 64))
pedistrain = cv2.resize(pedistrain, (64, 64))

noDrive = cv2.inRange(noDrive, (89, 91, 149), (255, 255, 255)) 
pedistrain = cv2.inRange(pedistrain, (89, 91, 112), (255, 255, 255))

#cv2.imshow("p", pedistrain)
#cv2.imshow("n", noDrive)

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.blur(hsv, (5, 5))
    
    frameCopy = frame.copy()

    mask = cv2.inRange(hsv, (60, 67, 84), (255, 255, 255))#(97, 34, 106), (255, 255, 255)) 
    
    #cv2.imshow("mask", mask)

    erode = cv2.erode(mask, None, iterations = 2)
    dilate = cv2.dilate(mask, None, iterations = 2)

    _, contours, __ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if contours:
        
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        cv2.drawContours(frame, contours, 0, (255, 255, 0), 3)
        (x, y, w, h) = cv2.boundingRect(contours[0])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        roImg = frameCopy[y:y+h, x:x+w]
        #cv2.imshow("rect", roImg)
        roImg = cv2.resize(roImg, (64, 64))
        roImg = cv2.inRange(roImg, (60,67,84), (255, 255, 255))
        cv2.imshow("r", roImg)

        noDrive_val = 0
        pedistrain_val = 0

        for i in range(64):
            for j in range(64):
                if roImg[i][j] == noDrive[i][j]:
                    noDrive_val += 1
                if roImg[i][j] == pedistrain[i][j]:
                    pedistrain_val += 1
        #print(noDrive_val, "   |   ", pedistrain_val)
        if noDrive_val > 2800:
            print("No drive")
            ser.write(bytes('1','utf-8')) #,'utf-8'  
            
        elif pedistrain_val > 2800:
            print("Pedistrain")
            ser.write(bytes('2','utf-8'))

        else:
            print("Nothing")
            ser.write(bytes('3','utf-8'))

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()
