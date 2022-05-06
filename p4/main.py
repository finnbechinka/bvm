import cv2
import numpy as np


def display(img, name="image", wait=False):
    cv2.imshow(name, img)
    if wait:
        cv2.waitKey()
        cv2.destroyAllWindows()
