import math

def max_distance_between_points(input):
    new_input = [a[0] for a in input]
    min_x_point = min(new_input)
    max_x_point = max(new_input)
    min_intersect = [a for a in input if a[0] == min_x_point]
    max_intersect = [a for a in input if a[0] == max_x_point]
    min_intersect = [a for t in min_intersect for a in t]
    max_intersect = [a for t in max_intersect for a in t]
    x_min, y_x_min = min_intersect[0], min_intersect[1]
    x_max, y_x_max = max_intersect[0], max_intersect[1]

    side_distance = math.sqrt((x_max - x_min) ** 2 + (y_x_max - y_x_min) ** 2)
    return side_distance


def max_distance_points(input):
    new_input = [a[0] for a in input]
    min_x_point = min(new_input)
    max_x_point = max(new_input)
    min_intersect = [a for a in input if a[0] == min_x_point]
    max_intersect = [a for a in input if a[0] == max_x_point]
    min_intersect = [a for t in min_intersect for a in t]
    max_intersect = [a for t in max_intersect for a in t]
    x_min, y_x_min = min_intersect[0], min_intersect[1]
    x_max, y_x_max = max_intersect[0], max_intersect[1]

    return [(x_min, y_x_min), (x_max, y_x_max)]


