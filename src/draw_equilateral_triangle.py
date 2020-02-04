import math
import cv2
def ret_eq_tri(input):
    f, s = input
    x1, y1 = f[0], f[1]
    x2, y2 = s[0], s[1]
    x3 = ( x1 + x2 + math.sqrt(3) * (y1 - y2) ) / 2
    y3 = ( y1 + y2 + math.sqrt(3) * (x2 - x1) ) / 2
    x3 = int(x3)
    y3 = int(y3)
    return (x1, y1), (x2, y2), (x3, y3)

