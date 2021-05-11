import cv2
# import matplotlib.p
import math
import matplotlib.pyplot as plt
import numpy

# net = cv2.dnn_DetectionModel('yolov4.cfg', 'yolov4.weights')
# net.setInputSize(704, 704)
# net.setInputScale(1.0 / 255)
# net.setInputSwapRB(True)

width = 224
height = 224
net = cv2.dnn.readNetFromDarknet('yolov4.cfg', 'yolov4.weights')
net.classes = "coco.names"
net.input_size = (width, height)
net.make_model()
net.load_weights("yolov4.weights", weights_type="yolo")
bboxList = []

for method_name in dir(net):
    print(method_name)

classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

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
    bbox = net.predict(img)
    if math.fmod(n, 5) == 0:
        bboxList.append(bbox)
    annotatedImg = net.draw_bboxes(img, bbox)
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