# This script filters colors by turning the pixels black that fall within a tolerance of HSV values
import cv2
import time
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
from longest_edge import *
from draw_equilateral_triangle import *
from find_tri_centroid import *
from valid_lines import *

ts_start = time.time()

im = cv2.imread("../2020SampleVisionImages/WPILib_Robot_Vision_Images/BlueGoal-132in-Center.jpg")
h, w, d = im.shape
print(h, "height")
print(w, "width")
print(d, "depth")


"""
cv2.cvtColor() takes in a variable storing a read image
and then another method in cv2 that will tell cv2.cvtColor()
which color space it is in and which color space it wants to convert to
Ex: 

cv2.cvtColor(im, cv2.BGR2HLS)
this will read the image stored in im that is currently in the BGR color space
and convert all pixels to HLS
"""
im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
im3 = im


# upper bound +5%: HSV (171.15, 105, 91.875)
# lower bound -5%: HSV (154.85, 95, 83.125)

"""
bound_percent_cv2 method takes Hue(h), Saturation(s), Brightness(v), Threshold Percent(in decimal form so 100% = 1.0
Ex: input HSV = [120, 100, 97] and threshold image by +5%
image_upper_bound = bound_percent_cv2(120, 100, 97, 1.05)
"""

image_lower_bound = bound_percent_cv2(153, 100, 81, 0.7)
image_upper_bound = bound_percent_cv2(153, 100, 81, 1.3)

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

#cv2.imshow("Filtered Image", imageFiltered)

#Converts BGR to Grayscale image in preparation for thresholding by making a bimodal image

grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Grayscale Image", grayscale_im)

ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#cv2.imshow("Grayscale Otsu Thresholded Image", th2)
"""
laplacian = cv2.Laplacian(grayscale_im, cv2.CV_64F)

cv2.imshow("Laplacian Edge Detect", laplacian)

sobelx = cv2.Sobel(grayscale_im,cv2.CV_64F,1,0,ksize=3)

abs_sobel64f = np.absolute(sobelx)
sobelx_8u = np.uint8(abs_sobel64f)

cv2.imshow("Sobel X Edge Detect", sobelx_8u)

sobely = cv2.Sobel(grayscale_im,cv2.CV_64F,0,1,ksize=3)

abs_sobel64f = np.absolute(sobely)
sobely_8u = np.uint8(abs_sobel64f)


cv2.imshow("Sobel Y Edge Detect", sobely_8u)
"""
edges = cv2.Canny(th2, 100, 200)

#cv2.imshow("Canny Edge Detection", edges)



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


for i in range(60,6,-5):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, i)
    if type(lines)!=str:
        lines = check_valid(lines, 0.1)
        lines = check_valid(lines, 0.1)
        num_lines = len(lines)
        if num_lines == 6:
            break


#valid_line_test(lines, )


print("threshold of: ", i)
print("number of lines: ", num_lines)

#need a check to make sure we find lines


points = []
slope_offset = []
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho

    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    if x2 == x1:
        continue
    m1 = (y2-y1)/(x2-x1)
    b1 = y1 - m1*x1
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

im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)

for point in points:
    cv2.circle(im, point, 5, (60, 255, 255))
#draws each intersection found from previous list comprehension

cv2.imshow("intersections", im)
'''
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

original_im = cv2.imread("../2020SampleVisionImages/WPILib_Robot_Vision_Images/BlueGoal-132in-Center.jpg")
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

'''

# cv2.imshow() takes in a string that is windows name and then a variable that stores the image



# window name will be Filtered Image

im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)


ts_end = time.time()
runtime = ts_end-ts_start
print(runtime, "total time")

#cv2.imshow("Equilateral Triangles", original_im)
cv2.imshow("Original Image", im1)
# window name will be Original Image

cv2.waitKey(0)