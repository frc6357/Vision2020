import math
import mpmath
def longest_side(input):
    first, second, third = input
    x1, y1 = first[0], first[1]
    x2, y2 = second[0], second[1]
    x3, y3 = third[0], third[1]

    t1_d1 = math.sqrt((x2-x1)**2 + (y2 - y1)**2)

    t1_d2 = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)

    t1_d3 = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

    t1_max_length = max(t1_d1, t1_d2, t1_d3)

    l = t1_max_length
   return





