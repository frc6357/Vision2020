import math
from mb_2xy_points import *
def find_hex_center(input, input2, input1):
    m = input[0]
    b = input[1]
    x_min, y_min = input1[0][0], input1[0][1]
    x_max, y_max = input1[1][0], input1[1][1]

    x_mid = (x_min + x_max)/2
    y_mid = (y_max + y_min)/2

    y_d =  input2/2 * math.sqrt(3)
    print(input2)

    print(y_mid)

    y_plz_work = y_mid - y_d

    return (x_mid, y_plz_work)

