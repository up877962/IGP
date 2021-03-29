from yolov4.tf import YOLOv4
import cv2
import math
import matplotlib.pyplot as plt
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

# YOLO SYSTEM
width = 224
height = 224
yolo = YOLOv4()
yolo.classes = "coco.names"
yolo.input_size = (width, height)
yolo.input_shape = ()
yolo.make_model()
yolo.load_weights("yolov4.weights", weights_type="yolo")
bboxList = []
# WEBCAM CAPTURE
cap = cv2.VideoCapture('./SAMPLE.mp4')

if not cap.isOpened():
    ValueError("No video feed")
n = 0
while True:
    n += 1
    ret, frame = cap.read()
    height, width, channels = frame.shape
    img = cv2.resize(frame, (244, 224))
    bbox = yolo.predict(img)
    if math.fmod(n, 5) == 0:
        bboxList.append(bbox)
    annotatedImg = cv2.rectangle(img, bbox)
    resizedAnnImg = cv2.resize(annotatedImg, (height+(int(height*0.25)), width+(int(height*0.25))))
    if len(bboxList) > 2:
        latestBox = [bboxList[len(bboxList) - 2]] + [bboxList[len(bboxList) - 1]]
        second = latestBox[0]
        first = latestBox[1]
        second = second[0].tolist()
        first = first[0].tolist()

        secondX = second[2]
        secondY = second[3]
        firstX = first[2]
        firstY = first[3]

        if firstX > secondX:
            resizedAnnImg = cv2.arrowedLine(resizedAnnImg, (50, 50), (100, 50), (266, 0, 0), thickness=4)
        elif firstX < secondX:
            resizedAnnImg = cv2.arrowedLine(resizedAnnImg, (100, 50), (50, 50), (266, 0, 0), thickness=4)
        elif firstY > secondY:
            resizedAnnImg = cv2.arrowedLine(resizedAnnImg, (50, 50), (50, 100), (266, 0, 0), thickness=4)
        elif secondY > firstY:
            resizedAnnImg = cv2.arrowedLine(resizedAnnImg, (50, 100), (50, 50), (266, 0, 0), thickness=4)

    cv2.imshow('TrafficCamNet', resizedAnnImg)
    c = cv2.waitKey(1)
    if c == 27:
        break


cap.release()
cv2.destroyAllWindows()





