import math
def horiz_dist(p, n, s):
    theta = p * n
    d = math.tan(theta/2) / 0.5 * s
    return d

