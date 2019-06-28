import cv2
import numpy as np


def traffic_lights(img):
    image = img.copy()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, gray = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
    gray = cv2.bitwise_not(gray)
    
    _, cnts, __ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if cnts:
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
            area = h * w
            if area >= 3000 and area <= 5000:
                ratio = w / h
                
                if ratio >= 0.35 and ratio <= 0.5:
                    rect = image[y:y+h, x:x+w]

                    #hsv = cv2.cvtColor(rect, cv2.COLOR_BGR2HSV)
                    #mask = cv2.inRange(hsv, (0, 0, 100), (255, 255, 255))
                    #cv2.imshow('mask', mask)

                    red_sum = np.sum(rect[0:37, 0:46])
                    yellow_sum = np.sum(rect[37:74, 0:46])
                    green_sum = np.sum(rect[74:111, 0:46])

                    cv2.rectangle(image, (0, 0), (46, 37), (0, 0, 255), 2)
                    cv2.rectangle(image, (0, 37), (46, 74), (0, 255, 255), 2)
                    cv2.rectangle(image, (0, 74), (46, 111), (0, 255, 0), 2)

                    my_print = "red: %d, yellow: %d, green: %d." %(red_sum, yellow_sum, green_sum)
                    print(my_print)

                    if max(red_sum, yellow_sum, green_sum) == red_sum:
                        return ("Red")
                    elif max(red_sum, yellow_sum, green_sum) == yellow_sum:
                        return ("Yellow")
                    else:
                        return ("Green")
            #else:
                #return ('Nothing')
    cv2.imshow('gray', gray)
    cv2.imshow('image', image)
