import math
def longest_side(input):
    first, second, third = input
    x1, y1 = first[0], first[1]
    x2, y2 = second[0], second[1]
    x3, y3 = third[0], third[1]

    t1_d1 = math.sqrt((x2-x1)**2 + (y2 - y1)**2)

    t1_d2 = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)

    t1_d3 = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

    if t1_d1 == max(t1_d1, t1_d2, t1_d3):
        return (x1, y1), (x2, y2)
    if t1_d2 == max(t1_d1, t1_d2, t1_d3):
        return (x2, y2), (x3, y3)
    if t1_d3 == max(t1_d1, t1_d2, t1_d3):
        return (x1, y1), (x3, y3)







