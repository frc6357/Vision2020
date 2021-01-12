from frc_6357_vision import *
import cv2
import time
import numpy as np

ts_start = time.time()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, -9)
ts_mid = time.time()

# print(ts_mid-ts_start, " :seconds to start")
while True:
    ret, frame = cap.read()

    h, w, d = frame.shape

    cv2.imshow(frame, "frame")

    im = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    image_lower_bound = createBound.bound_percent_cv2(167, 41, 73, 0.8)
    image_upper_bound = createBound.bound_percent_cv2(167, 41, 73, 1.2)

    imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
    imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)

    imageFiltered = cv2.cvtColor(imageFiltered, cv2.COLOR_HSV2BGR)

    grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)

    ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    edges = cv2.Canny(th2, 100, 200)

    slope_offset = []

    for i in range(60, 6, -5):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, i)
        lines = validLines.check_valid(lines, 0.1)
        if type(lines) != str:
            lines = validLines.check_valid(lines, 0.1)
            lines = validLines.check_valid(lines, 0.1)
            num_lines = len(lines)

            if num_lines == 6:
                print("there are 6 lines")

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

                    flat_line = hexCenter.find0Slope.approx_0_slope(slope_offset)
                    flat_line = hexCenter.findB.find_b(flat_line[0], slope_offset)

                    flat_line_xy_points = hexCenter.mbxyPoints.mb_2xy_points(flat_line)

                    slope_offset_except_flat_line = [a for a in slope_offset if a != flat_line]
                    intersections_w_flat_line = [hexCenter.solveSyseq.solve_syseq([flat_line, a]) for a in slope_offset_except_flat_line]
                    intersections_w_flat_line = [a for a in intersections_w_flat_line if a is not None]
                    flat_line_max_distance = hexCenter.distancePoints.max_distance_between_points(intersections_w_flat_line)
                    flat_line_max_d_points = hexCenter.distancePoints.max_distance_points(intersections_w_flat_line)

                    hex_center_point = [hexCenter.findHexCenter.find_hex_center(flat_line, flat_line_max_distance, flat_line_max_d_points)]
                    hex_center_point = [(int(hex_center_point[0][0]), int(hex_center_point[0][1]))]

                    x_val = hex_center_point[0][0]
                    d_ish = w/2

                    px = d_ish - x_val

                    px = px * 0.055
                    fina_sting = px + " degrees"
                    print(fina_sting)

            else:

                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("frame.jpg", frame)
            break


    cap.release()
    cv2.destroyAllWindows()



