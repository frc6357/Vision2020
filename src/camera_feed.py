import numpy
import cv2
import itertools
import numpy as np
from create_bound import *
from systemeq import *
from reg_triangle_detect import *
from mb_to_xy import *
from largest_triangle import *
from removeDuplicates import *
from smallest_triangle import *
from dimension_check import *
import time

ts_start = time.time()
cap = cv2.VideoCapture(1)
ts_mid = time.time()

print(ts_mid-ts_start, "seconds to start")
while(True):
    # Capture frame-by-frame

    ret, frame = cap.read()

    h, w, d = frame.shape

    im = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    image_lower_bound = bound_percent_cv2(38, 12, 78, 0.8)
    image_upper_bound = bound_percent_cv2(38, 12, 78, 1.2)
    cv2.imshow("color", im)
    imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
    imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)
    imageFiltered = cv2.cvtColor(imageFiltered, cv2.COLOR_HSV2BGR)

    grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)

    ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edges = cv2.Canny(th2, 100, 200)

    cv2.imshow("Edges", edges)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()