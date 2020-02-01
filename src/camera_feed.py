import numpy
import cv2
from src.create_bound import *
import itertools
import numpy as np
from src.create_bound import *
from src.systemeq import *
from src.reg_triangle_detect import *
from src.mb_to_xy import *
from src.largest_triangle import *
from src.removeDuplicates import *
from src.smallest_triangle import *
from src.dimension_check import *
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
    image_lower_bound = bound_percent_cv2(161, 0, 100, 0.5)
    image_upper_bound = bound_percent_cv2(161, 0, 100, 1.5)
    imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
    imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)
    imageFiltered = cv2.cvtColor(imageFiltered, cv2.COLOR_HSV2BGR)

    grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)

    ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edges = cv2.Canny(th2, 100, 200)

    cv2.imshow("Edges", edges)
    if cv2.waitKey(1) & 0xFF == ord('e'):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

        points = []
        slope_offset = []
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            m1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - m1 * x1
            slope_offset.append([m1, b1])
            cv2.line(im, (x1, y1), (x2, y2), (0, 255, 255), 2)
        im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
        cv2.imshow("lines", im)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()