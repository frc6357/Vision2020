
"""
This script takes in a hue(h) in degrees out of 360, saturation(s) as percent, and brightness(v) as a percent and then a
percentage (in decimal form: 100% = 1.0) to increase or decrease those values to create upper and lower bounds

"""

import numpy as np

"""
This method outputs an array that OpenCV will read and output accurately with the diffrence being 
OpenCV divides h value by two scales the value out of 255 
ex: 

HSV = [120, 100, 97] but OpenCV will need [60, 255, 247.35]
"""

def bound_percent_cv2(h, s, v, percent):
    h = (h * percent)/2
    v = ((v * percent)/100)*255
    s = ((s * percent)/100)*255
    lower_bound = np.array([h, s, v])
    return lower_bound

"""
This method takes in the h, s, v and threshold percent values and outputs hue in degrees out of 360(s), saturation(s) percent, and brightness(v) percent
"""

def bound_percent(h, s, v, percent):
    h = h * percent
    v = v * percent
    s = s * percent
    lower_bound = np.array([h, s, v])
    return lower_bound

if __name__ == '__main__':
    lower_bound = bound_percent_cv2(1, 100, 97, 1)
    print(lower_bound)

