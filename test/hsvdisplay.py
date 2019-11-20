from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
import numpy as np
import cv2
im = cv2.imread("../green-purple.png")
targetHSV = [120, 100, 97]
im1 = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
print(im1)
