import cv2
import numpy as np
from src.create_bound import*

im = cv2.imread("../CargoSideStraightDark36in.jpg")
im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
print(im)
# upper bound +5%: HSV (171.15, 105, 91.875)
# lower bound -5%: HSV (154.85, 95, 83.125)
image_lower_bound = bound_percent_cv2(164, 99, 88, 0.95)
image_upper_bound = bound_percent_cv2(164, 99, 88, 1.05)
imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)
imageFiltered = cv2.cvtColor(imageFiltered, cv2.COLOR_HSV2BGR)
im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
print(imageFiltered)
window_name = "name?"
cv2.imshow("Filtered Image", imageFiltered)
cv2.imshow("Image", im)
cv2.waitKey(0)