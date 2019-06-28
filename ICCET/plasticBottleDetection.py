import vrep
import time
import cv2
import numpy
import dlib

bottle_detector = dlib.simple_object_detector(r"D:\Robotics\ICCET2019\V-REP\Detectors\plastic_bottle1.svm")

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

            img2 = cv2.flip(img2, -1)

            cv2.imshow('image', img2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


            boxes = bottle_detector(img2)
            print(len(boxes))
            num = 1
            for box in boxes:
                #print("Bottle")
                (x, y, x2, y2) = [box.left(), box.top(), box.right(), box.bottom()]
                cv2.rectangle(img2, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img2, "b" + str(num), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                num += 1

            if not boxes:
                print("None")

            img2 = cv2.flip(img2, +1)
            img2 = cv2.flip(img2, -1)

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

