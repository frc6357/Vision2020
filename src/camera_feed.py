import cv2
import time

import itertools
import numpy as np
from create_bound import *
import hough_transform
"""
from systemeq import *
from reg_triangle_detect import *
from mb_to_xy import *
from largest_triangle import *
from removeDuplicates import *
from smallest_triangle import *
from dimension_check import *
from longest_edge import *
from draw_equilateral_triangle import *
from find_tri_centroid import *
from valid_lines import *
from find_approx_m_0 import *
from find_b import *
from mb_2xy_points import *
from largest_distance_2_points import *
from center_hexagon import *
from angle_offset import *
import maths
import socket
"""
ts_start = time.time()
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_EXPOSURE, -9)
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

    image_lower_bound = bound_percent_cv2(179, 32, 98, 0.8)
    image_upper_bound = bound_percent_cv2(179, 32, 98, 1.2)

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
    # cv2.imshow("Grayscale Image", grayscale_im)

    # uses OTSU and Binary Thresholding methods to maximize contrast in filtered image
    ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("Grayscale Otsu Thresholded Image", th2)

    # uses canny edge detection to find the edges of segmented image
    edges = cv2.Canny(th2, 100, 200)
    cv2.imshow("Canny Edge Detection", edges)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 23)
    color_lines = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if lines is not None:
        # unpacks rhos and thetas into list of list
        lines = [line[0] for line in lines]
        #print(lines)
        similar_lines_bucket = []
        while(len(lines) > 0):
            lines, similar_lines_bucket = hough_transform.filter_lines(lines, similar_lines_bucket)
        avg_lines = hough_transform.average_lines(similar_lines_bucket)

        if avg_lines is not None:
            for line in avg_lines:
                rho, theta = line
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(color_lines,(x1,y1),(x2,y2),(0,0,255),2)

    cv2.imshow("lines", color_lines)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("image saved")
        cv2.imwrite("frame.jpg", frame)
        break
"""
    # initailizes lists for lists, points and slope offset
    lines = []
    points = []
    slope_offset = []

    # finds the lines in the Canny Edge detection image based on number of pixels in line
    # the for loop iterator, i, decreases the number of pixels required to detect a line
    # parameter 2 is the pixel accuracy (1 pixel), and parameter 2 is the angle accuracy (1 deg)
    for i in range(60, 6, -5):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, i)

        # checks if the lines are parallel or lines are duplicates
        lines = check_valid(lines, 0.1)
        if type(lines) != str:
            # repeat the check twice (not sure why??)
            lines = check_valid(lines, 0.1)
            lines = check_valid(lines, 0.1)
            num_lines = len(lines)
            # if lines are not 6 than there are more than identified in image -> ROI is half of a hexagon
            if num_lines == 6:


                print("there are 6 lines")
                # valid_line_test(lines, )

                # print("threshold of: ", i)
                # print("number of lines: ", num_lines)

                # need a check to make sure we find lines

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
                    if x2 == x1:
                        continue
                    m1 = (y2 - y1) / (x2 - x1)
                    b1 = y1 - m1 * x1
                    slope_offset.append([m1, b1])

                flat_line = approx_0_slope(slope_offset)
                flat_line = find_b(flat_line[0], slope_offset)



                flat_line_xy_points = mb_2xy_points(flat_line)

                x1_flat_line, y1_flat_line = int(flat_line_xy_points[0][0]), int(flat_line_xy_points[0][1])

                x2_flat_line, y2_flat_line = int(flat_line_xy_points[1][0]), int(flat_line_xy_points[1][1])
                im_another = frame

                # cv2.line(im_another, (x1_flat_line, y1_flat_line), (x2_flat_line, y2_flat_line), (0, 255, 255), 1)

                slope_offset_except_flat_line = [a for a in slope_offset if a != flat_line]
                intersections_w_flat_line = [solve_syseq([flat_line, a]) for a in slope_offset_except_flat_line]
                intersections_w_flat_line = [a for a in intersections_w_flat_line if a is not None]
                flat_line_max_distance = max_distance_between_points(intersections_w_flat_line)
                flat_line_max_d_points = max_distance_points(intersections_w_flat_line)

                flat_line_max_x1, flat_line_max_x2 = flat_line_max_d_points[0][0], flat_line_max_d_points[1][0]
                flat_line_max_y1, flat_line_max_y2 = flat_line_max_d_points[0][1], flat_line_max_d_points[1][1]

                hex_center_point = [find_hex_center(flat_line, flat_line_max_distance, flat_line_max_d_points)]
                hex_center_point = [(int(hex_center_point[0][0]), int(hex_center_point[0][1]))]

                x_val = hex_center_point[0][0]
                d_ish = w/2

                px = d_ish - x_val

                angle = px * 0.055
                distance = math.tan(angle * (math.pi/180))


                slope_offset.clear()

        else:

            break
            
    """



cap.release()
cv2.destroyAllWindows()
