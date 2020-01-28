# This script filters colors by turning the pixels black that fall within a tolerance of HSV values
import cv2
import time
import itertools
import numpy as np
from src.create_bound import *
from src.systemeq import *
from src.reg_triangle_detect import *
from src.mb_to_xy import *
from src.largest_triangle import *
from src.removeDuplicates import *
from src.smallest_triangle import *
ts_start = time.time()

im = cv2.imread("../2020SampleVisionImages/WPILib_Robot_Vision_Images/BlueGoal-156in-Center.jpg")



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
cv2.imshow("Grayscale Image", grayscale_im)

ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imshow("Grayscale Otsu Thresholded Image", th2)

edges = cv2.Canny(th2, 100, 200)

cv2.imshow("Canny Edge Detection", edges)
cv2.waitKey(0)