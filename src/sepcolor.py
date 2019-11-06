import cv2
import numpy as np

im = cv2.imread("../CargoSideStraightDark36in.jpg")
# reads image in previous directory and stores BGR values as an array in variable im
im2 = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# looks at BGR values in array im and then converts values by mathematically transforming them into HSV values

# Color/shade?/hue? of green to be isolated RGB values: [0, 224, 163]
# supposed HSV values: [82, 255, 224]
image_lower_bound = np.uint8([[[154.85, 212.8, 0]]])
# -5% [0, 212.8, 154.85]
image_lower_bound = cv2.cvtColor(image_lower_bound, cv2.COLOR_RGB2HSV)
# HSV converted values of lower bound
# HSV converted value: [38, 255, 212]
image_upper_bound = np.uint8([[[171.15, 235.2, 0]]])
# +5% [0, 235.2, 171.15]
image_upper_bound = cv2.cvtColor(image_upper_bound, cv2.COLOR_RGB2HSV)
# HSV converted values of lower bound
# HSV converted value: [38, 255, 235]
filteredImage = cv2.inRange(im2, image_lower_bound, image_upper_bound)
im3 = cv2.cvtColor(im2, cv2.COLOR_HSV2BGR)
imageFiltered = cv2.bitwise_and(im3, im3, mask = filteredImage)
cv2.imshow("Filtered Image", imageFiltered)
cv2.imshow("Image", im)
cv2.waitKey(0)
