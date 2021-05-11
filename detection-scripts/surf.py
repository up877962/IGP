import cv2
import numpy as np

img = cv2.imread('blocks.jpg')
surf = cv2.SURF(400)

kp, des = surf.detectAndCompute(img,None)
print(len(kp))

# gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# sift = cv2.SIFT()
# kp = sift.detect(gray,None)

# img=cv2.drawKeypoints(gray,kp)

# cv2.imwrite('sift_keypoints.jpg',img)