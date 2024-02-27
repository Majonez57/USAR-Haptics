import cv2
from pupil_apriltags import Detector, Detection
import cv2 as cv
import numpy as np

detector = Detector()

def rotate_image(image, source_name):
        ### Make sure image is upwards facing
        if source_name == 'frontleft_fisheye_image':
            image = cv2.rotate(image, rotateCode=0)
        elif source_name == 'right_fisheye_image':
            image = cv2.rotate(image, rotateCode=1)
        elif source_name == 'frontright_fisheye_image':
            image = cv2.rotate(image, rotateCode=0)

        return image

# Returns all tag data
def detectTagValue(image_grey, tag_family="tag36h11"):
    
    detected = detector.detect(image_grey, estimate_tag_pose=False)

    return detected