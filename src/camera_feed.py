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
while True:
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

    lines = []
    """
    for i in range(60, -1, -5):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, i)
        num_lines = len(lines)
        if num_lines in range(8, 21):
            new_list = [a[0, 1] for a in lines]
            valid_lines = valid_line_test(lines, new_list)
            break
    """

    for i in range(60, 6, -5):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, i)
        if type(lines) != str:
            lines = check_valid(lines, 0.1)
            lines = check_valid(lines, 0.1)
            num_lines = len(lines)
            if num_lines == 6:
                break
    if type(lines) == str:
        continue

    # valid_line_test(lines, )

    print("threshold of: ", i)
    print("number of lines: ", num_lines)

    # need a check to make sure we find lines

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
        if x2 == x1:
            continue
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
        slope_offset.append([m1, b1])
        cv2.line(im, (x1, y1), (x2, y2), (0, 255, 255), 2)
    """
    a for loop that takes the output from hough lines (rho, theta) and transforms them 
    into slopes and intercepts and appends them to an array  
    """

    im1 = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
    im2 = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)



    points = [solve_syseq(pair) for pair in itertools.combinations(slope_offset, 2)]
    """
    takes slopes and intercepts from the slope_offset array and uses list comprehension
    to loop through each element and find the intersections between the lines
    """

    points = [point for point in points if point is not None]
    #removes nones from the list

    for point in points:
        cv2.circle(im, point, 5, (60, 255, 255))
    #draws each intersection found from previous list comprehension

    triangles = [detect_tri(a) for a in itertools.combinations(slope_offset, 3)]
    """
    using the slopes and intercepts from slope offset detect_tri() finds all the lines that intersect 
    and make regular triangles, using list comprehension to loop through each element 
    """
    triangles = [a for a in triangles if a is not None]


    tri_points = [mb_xy(a) for a in triangles]
    tri_points = [a for a in tri_points if a[0] is not None]
    tri_points = [a for a in tri_points if a[1] is not None]
    tri_points = [a for a in tri_points if a[2] is not None]

    tri_in_img = [in_img(a, h, w) for a in tri_points]
    tri_in_img = [a for a in tri_in_img if a[0] is not None]
    tri_in_img = [a for a in tri_in_img if a[1] is not None]
    tri_in_img = [a for a in tri_in_img if a[2] is not None]

    longest_edge = [longest_side(a) for a in tri_in_img]

    equ_tri = [draw_eq_tri(a) for a in longest_edge]

    largest_triangle = [a for a in equ_tri]

    while len(largest_triangle) > 1:
        largest_triangle = [max_tri(a) for a in itertools.combinations(largest_triangle, 2)]
        largest_triangle = [a for a in largest_triangle if a is not None]

        largest_triangle = remov_dupl(largest_triangle)

    largest_triangle = [a for t in largest_triangle for a in t]

    original_im = cv2.imread("../2020SampleVisionImages/WPILib_Robot_Vision_Images/BlueGoal-108in-Center.jpg")
    for a in largest_triangle:
        cv2.circle(original_im, a, 5, (0, 255, 255))

    centroid_point = centroid(largest_triangle)

    cv2.circle(original_im, centroid_point, 5, (0, 255, 255))

    """
    if all(tri_in_img) == False:
        print("triangle is outside of image")
        cv2.waitKey(0)
        exit()
    """

    """
    largest_triangle = [a for a in tri_in_img]

    while len(largest_triangle) > 1:
        largest_triangle = [max_tri(a) for a in itertools.combinations(largest_triangle, 2)]
        largest_triangle = [a for a in largest_triangle if a is not None]

        largest_triangle = remov_dupl(largest_triangle)

    largest_triangle = [a for t in largest_triangle for a in t]
    triangle = []

    smallest_triangle = [a for a in tri_in_img]

    while len(smallest_triangle) > 1:
        smallest_triangle = [min_tri(a) for a in itertools.combinations(smallest_triangle, 2)]
        smallest_triangle = [a for a in smallest_triangle if a is not None]

        smallest_triangle = remov_dupl(smallest_triangle)

    smallest_triangle = [a for t in smallest_triangle for a in t]
    """
    """
    largest_triangle = [max_tri(a) for a in itertools.combinations(largest_triangle, 2)]
    largest_triangle = [a for a in largest_triangle if a is not None]
    largest_triangle = remov_dupl(largest_triangle)

    print(largest_triangle)

    for a in largest_triangle:
        cv2.circle(im1, a, 5, (60, 255, 255))
    cv2.imshow("Largest Triangle", im1)

    for a in smallest_triangle:
        cv2.circle(im2, a, 5, (60, 255, 255))
    cv2.imshow("Smallest Triangle", im2)

    """
    """
    tri_m_np = np.array([a[0] for a in tri_m_b])

    tri_b_np = np.array([a[1] for a in tri_m_b])
    """



    # cv2.imshow() takes in a string that is windows name and then a variable that stores the image



    # window name will be Filtered Image

    im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)


    ts_end = time.time()
    runtime = ts_end - ts_start
    print(runtime, "total time")

    # cv2.imshow("Equilateral Triangles", original_im)
    cv2.imshow("Original Image", im1)
    # window name will be Original Image

    cv2.waitKey(0)



cap.release()
cv2.destroyAllWindows()