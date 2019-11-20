import numpy as np


def bound_percent_cv2(h, s, v, percent):
    h = (h * percent)/2
    v = ((v * percent)/100)*255
    s = ((s * percent)/100)*255
    lower_bound = np.array([h, s, v])
    return lower_bound

def bound_percent(h, s, v, percent):
    h = h * percent
    v = v * percent
    s = s * percent
    lower_bound = np.array([h, s, v])
    return lower_bound

lower_bound = bound_percent(120, 100, 97, 0.95)
print(lower_bound)

