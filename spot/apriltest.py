from pupil_apriltags import Detector, Detection
import cv2 as cv
import numpy as np

cam = cv.VideoCapture(0)
ret, img = cam.read()
imgg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

detector = Detector()
detected = detector.detect(imgg, estimate_tag_pose=False)[0]

corn = [np.int32(detected.corners)]
print(corn)

if detected != []:
    cv.polylines(img, corn, True, (255, 0, 0), 3)
    cv.imshow("dec", img)
    cv.waitKey(0)