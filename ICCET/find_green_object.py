import vrep
import time

import cv2
import numpy


def track_green_object(image):
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5, 5), 0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    lower_green = numpy.array([40, 70, 70])
    upper_green = numpy.array([80, 200, 200])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10'] / m00)
        centroid_y = int(moments['m01'] / m00)

    # Assume no centroid
    ctr = None

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)
    return ctr

name = "\img4"
num = 1

vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID != -1:
    print
    'Connected to remote API server'

    # get vision sensor objects
    res, v0 = vrep.simxGetObjectHandle(clientID, 'v0', vrep.simx_opmode_oneshot_wait)
    res, v1 = vrep.simxGetObjectHandle(clientID, 'v1', vrep.simx_opmode_oneshot_wait)

    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_streaming)
    time.sleep(1)

    while (vrep.simxGetConnectionId(clientID) != -1):
        # get image from vision sensor 'v0'
        err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
        if err == vrep.simx_return_ok:
            img2 = numpy.array(image, dtype=numpy.uint8)
            img2.resize([resolution[1], resolution[0], 3])
            cv2.imshow('image', img2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # try to find something green
            ret = track_green_object(img2)

            # overlay rectangle marker if something is found by OpenCV
            if ret:
                cv2.rectangle(img2, (ret[0] - 15, ret[1] - 15), (ret[0] + 15, ret[1] + 15), (0xff, 0xf4, 0x0d), 1)

            # (h, w) = img2.shape[:2]
            # center = (w / 2, h / 2)
            #
            # M = cv2.getRotationMatrix2D(center, 180, 1.0)
            # rotated = cv2.warpAffine(img2, M, (w, h))
            #
            # cv2.imwrite(r"D:\Robotics\ICCET2019\V-REP\Dataset\Red_bottle" + name + str(num) + ".jpeg", rotated)
            # time.sleep(0.04)
            # num += 1

            # return image to sensor 'v1'
            img2 = img2.ravel()
            vrep.simxSetVisionSensorImage(clientID, v1, img2, 0, vrep.simx_opmode_oneshot)

        elif err == vrep.simx_return_novalue_flag:
            print("no image yet")
            pass
        else:
            print(err)
else:
    print("Failed to connect to remote API Server")
    vrep.simxFinish(clientID)