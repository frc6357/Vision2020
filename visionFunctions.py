import math
import numpy as np
import itertools
def intersections(input):
    point, point1  = input
    theta, b = point
    theta_1, b_1 = point1
    m, m_1 = math.tan(theta), math.tan(theta_1)

    m_matrix = np.array([[-m, 1.0], [-m_1, 1.0]])
    b_matrix = np.array([[b], [b_1]])

    if abs(abs(math.atan(m)) - math.pi/2) < (5 * math.pi/180) and abs(abs(math.atan(m_1)) - math.pi/2) < (5 * math.pi/180):
        return None
    elif abs(abs(math.atan(m)) - math.pi/2) < (5 * math.pi/180):
        x = b
        y = m_1*x + b_1
        return [x, y]
    elif abs(abs(math.atan(m_1)) - math.pi/2) < (5 * math.pi/180):
        x = b_1
        y = m*x + b
        return [x, y]

    if np.linalg.det(m_matrix) != 0:
        intersection = (np.linalg.inv(m_matrix)@b_matrix).tolist()

        intersection = [a for i in intersection for a in i]
        return intersection

def remove_dupe(input):
    no_dupe = []
    for i in input:
        i.sort()
        no_dupe.append(list(i for i,_ in itertools.groupby(i)))
    return no_dupe