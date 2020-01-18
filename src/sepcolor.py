# This script filters colors by turning the pixels black that fall within a tolerance of HSV values
import cv2
import time
import itertools
import numpy as np
from src.create_bound import *
from src.systemeq import *
from src.reg_triangle_detect import *
from src.mb_to_xy import *

ts_start = time.time()

im = cv2.imread("../2020SampleVisionImages/WPILib_Robot_Vision_Images/BlueGoal-108in-Center.jpg")

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

#Converts BGR to Grayscale image in preparation for thresholding by making a bimodal image

grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)


ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

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
edges = cv2.Canny(grayscale_im, 100, 200)

cv2.imshow("Canny Edge Detection", edges)



lines = cv2.HoughLines(edges, 1, np.pi/120, 60)
#need a check to make sure we find lines

points = []
slope_offset = []
print(len(lines))
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

    m1 = (y2-y1)/(x2-x1)
    b1 = y1 - m1*x1
    slope_offset.append([m1, b1])
    cv2.line(im, (x1, y1), (x2, y2), (0, 255, 255), 2)

points = [solve_syseq(pair) for pair in itertools.combinations(slope_offset, 2)]

points = [point for point in points if point is not None]
print(points)

for point in points:
    cv2.circle(im, point, 5, (60, 255, 255))


triangles = [detect_tri(a) for a in itertools.combinations(slope_offset, 3)]
triangles = [a for a in triangles if a is not None]

print(len(triangles))

tri_points = [mb_xy(a) for a in triangles]
tri_points = [a for a in tri_points if a[0] is not None]

print(tri_points)

#triangles_list_pairs = mb_xy(triangles)

#print(triangles_list_pairs)


"""

tri_m_np = np.array([a[0] for a in tri_m_b])

tri_b_np = np.array([a[1] for a in tri_m_b])

"""









cv2.imshow("Grayscale Otsu Thresholded Image", th2)
# cv2.imshow() takes in a string that is windows name and then a variable that stores the image

cv2.imshow("Filtered Image", imageFiltered)
cv2.imshow("Grayscale Image", grayscale_im)
# window name will be Filtered Image

im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)


cv2.imshow("Original Image", im)
# window name will be Original Image
ts_end = time.time()


runtime = ts_end-ts_start
print(runtime, "total time")
cv2.waitKey(0)