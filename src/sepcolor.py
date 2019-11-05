import cv2
import numpy as np

im = cv2.imread("../CargoSideStraightDark36in.jpg")
im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
print(im)
# upper bound +5%: HSV (171.15, 105, 91.875)
# lower bound -5%: HSV (154.85, 95, 83.125)
image_lower_bound = np.array([154.85, 95.000, 83.125])
image_upper_bound = np.array([171.15, 105, 91.875])
imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)
window_name = "name?"
cv2.imshow("Filtered Image", imageFiltered)
cv2.imshow("Image" , im)
cv2.waitKey(0)
