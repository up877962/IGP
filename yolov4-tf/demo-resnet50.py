import cv2
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


model = ResNet50(weights='imagenet')

# webcam
# cap = cv2.VideoCapture(0)

# video file
cap = cv2.VideoCapture('./SAMPLE.mp4')

if not cap.isOpened():
	raise IOError("Cannot Open Webcam")

while True:
	ret, frame = cap.read()
	x = cv2.resize(frame, (224, 224))
	x = image.img_to_array(x)
	x = np.expand_dims(x, axis=0)
	x = preprocess_input(x)
	prediction = model.predict(x)
	output = decode_predictions(prediction, top=1)[0]
	frame = cv2.resize(frame, (1366, 768))
	cv2.putText(frame, str(output), (100, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
	cv2.imshow("Webcam", frame)
	c = cv2.waitKey(1)
	if c == 27:
		break


cap.release()
cv2.destroyAllWindows()
