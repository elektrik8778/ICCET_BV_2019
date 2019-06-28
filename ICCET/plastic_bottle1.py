import dlib
import os
import cv2
import xml.etree.ElementTree as pars

dir_annot = r"D:\Robotics\ICCET2019\V-REP\Dataset\Bottle_annots"
dir_img = r"D:\Robotics\ICCET2019\V-REP\Dataset\Red_bottle"
images = []
annots = []

ImgNameList = os.listdir(dir_img)

for FileName in ImgNameList:
    image = cv2.imread(dir_img + "\\" + FileName)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    OnlyFileName = FileName.split('.')[0]

    e = pars.parse(dir_annot + "\\" + OnlyFileName + ".xml")
    root = e.getroot()
    for object in root.findall("object"):
        object = object.find("bndbox")
        x1 = int(object.find("xmin").text)
        y1 = int(object.find("ymin").text)
        x2 = int(object.find("xmax").text)
        y2 = int(object.find("ymax").text)

        '''if ((x2 - x1) / (y2 - y1)) > 0.4 and ((x2 - x1) / (y2 - y1)) < 1.7:'''
        images.append(image)
        annots.append([dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2)])
#print(len(annots))

options = dlib.simple_object_detector_training_options()
options.be_verbose = True

detector = dlib.train_simple_object_detector(images, annots, options)

detector.save("plastic_bottle1.svm")
