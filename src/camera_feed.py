import cv2
import time

import itertools
import numpy as np
from create_bound import *
import hough_transform
import math

ts_start = time.time()
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_EXPOSURE, -11)
ts_mid = time.time()

stop_var = 1

print(ts_mid-ts_start, "seconds to start")
while True:
    # Capture frame-by-frame

    ret, frame = cap.read()

    h, w, d = frame.shape

    #cv2.circle(frame, (320, 240), 5, (248, 26, 225))

    cv2.imshow("frame", frame)

    im = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    """
    cv2.cvtColor() takes in a variable storing a read image
    and then another method in cv2 that will tell cv2.cvtColor()
    which color space it is in and which color space it wants to convert to
    Ex: 
    
    cv2.cvtColor(im, cv2.BGR2HLS)
    this will read the image stored in im that is currently in the BGR color space
    and convert all pixels to HLS
    """
    #im3 = im
    # test 1 HSV color value: (173 deg, 48%, 76%)
    # upper bound +5%:
    # lower bound -5%:

    """
    bound_percent_cv2 method takes Hue(h), Saturation(s), Brightness(v), Threshold Percent(in decimal form so 100% = 1.0
    Ex: input HSV = [120, 100, 97] and threshold image by +5%
    image_upper_bound = bound_percent_cv2(120, 100, 97, 1.05)
    """

    image_lower_bound = bound_percent_cv2(166, 85, 64, 0.5)
    image_upper_bound = bound_percent_cv2(166, 85, 64, 1.7)

    """
    cv2.inRange() takes in a variable storing a read image, lower bound, and upper bound
    It then checks each each pixel to see if it lies within the lower and upper bound
    It will return a true(1) or false(0) and if the pixel returns 0 then this method
    turns that pixel black, if the pixel returns 1 then this method does nothing to it
    """
    imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
    imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)

    """
    OpenCV displays all images in the BGR color space in order to look properly
    so after filtering the image in HSV color space the script needs to convert
    back to BGR in order to display interpretable images
    """
    imageFiltered = cv2.cvtColor(imageFiltered, cv2.COLOR_HSV2BGR)
    cv2.imshow("Filtered Image", imageFiltered)

    # Converts BGR to Grayscale image in preparation for thresholding by making a high contrast image
    grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale Image", grayscale_im)

    # uses OTSU and Binary Thresholding methods to maximize contrast in filtered image
    ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("Grayscale Otsu Thresholded Image", th2)

    # uses canny edge detection to find the edges of segmented image
    edges = cv2.Canny(th2, 100, 200)
    cv2.imshow("Canny Edge Detection", edges)


    #lines = cv2.HoughLines(edges, 1, np.pi / 180, 55, min_theta=-10*math.pi/180, max_theta=10*math.pi/180)
    #lines = cv2.HoughLines(edges, 1, np.pi / 180, 20)


    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10)
    color_lines = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if lines is not None:
        point_pairs_lines = []
        bucket = []
        lines = [line[0] for line in lines]
        for line in lines:
            x1, y1, x2, y2 = line
            """rho, theta = line
            a = np.cos(theta)w
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))"""

            point_pairs_lines.append([x1, y1, x2, y2])
            #cv2.line(color_lines, (x1, y1), (x2, y2), (255,0,0), 2)
        #print(point_pairs_lines)
        theta_b_lines = [hough_transform.theta_b(i) for i in point_pairs_lines]
        while len(theta_b_lines) > 0:
            theta_b_lines, bucket = hough_transform.filter_lines(theta_b_lines, bucket)


        if bucket is not None:
            avg_lines = hough_transform.average_lines(bucket)
            #print("average lines", len(avg_lines))
            #print("\n")



        # Displaying avg lines
        try:
            for avg_line in avg_lines:
                theta, b = avg_line
                if theta == 90 * math.pi/180:
                    cv2.line(color_lines, (int(b), 1), (int(b), h-1), (255,0,0), 2)

                else:

                    print("theta: " + str(theta))
                    m = math.tan(theta)
                    x1 = 1
                    x2 = w-1
                    y1 = m*x1 + b
                    y2 = m*x2 +b
                    print("y1: " + str(y1))
                    print("y2: " + str(y2))
                    cv2.line(color_lines, (x1, int(y1)), (x2,int(y2)), (255, 0, 0), 2)
            cv2.imshow("Average Lines", color_lines)
        except Exception as e:
            print(e)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("frame.jpg", frame)
        break
cap.release()
cv2.destroyAllWindows()