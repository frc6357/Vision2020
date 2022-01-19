import math
def theta_b(input):
    x1, y1, x2, y2 = input
    if (abs(x1-x2) < 1) or (x1 == 0):
        theta = 90 * math.pi/180
        b = x1
    else:

        theta = math.atan((y2-y1)/(x2-x1))
        b = y2 - math.tan(theta)*x2
    return [theta, b]


def threshold(x, input):
    theta, b = x
    theta1, b1 = input
    if (abs(math.tan(theta) - math.tan(theta1)) < 0.5) and (abs(b-b1) < 15):
        return True
    else:
        return False



def filter_lines(lines, bucket):
    next_set_to_process = []

    # initial rho and theta in the total list of lines
    matching_set = [lines[0]]

    # iterating through all the other rhos and thetas excluding the first
    for x in lines[1:]:
        # if lines meet threshold condition (within 5% of the original rho and theta) then add to the matching set
        if threshold(x, lines[0]):
            matching_set.append(x)
        else:
            # if lines are outside 5% of the original rho and theta then add to the next set
            next_set_to_process.append(x)
    bucket.append(matching_set)
    return next_set_to_process, bucket


def average_lines(lines):
    avg_lines = []
    for dupl_lines in lines:
        sumY = 0
        sumX = 0
        offset = 0
        count = 0
        for i in dupl_lines:
            count += 1
            angle, b = i
            #print()
            sumY += math.sin(angle)
            sumX += math.cos(angle)

            offset += b
        # outputs in degrees
        #vavg_angle = math.atan2(sumY/count, sumX/count) * 180/math.pi
        # outputs in radians
        avg_angle = math.atan2(sumY/count, sumX/count)
        #offset = offset/count
        avg_lines.append([avg_angle, offset/count])
    return avg_lines


    return avg_lines


def threshold_slope(a, b):
    m1 = a[0]
    m2 = b[0]

    if math.abs(m1-m2) < 0.05 * m1:
        return True
    else:
        return False