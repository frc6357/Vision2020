import numpy as np
import itertools
import math
class createBound:
    """
    This script takes in a hue(h) in degrees out of 360, saturation(s) as percent, and brightness(v) as a percent and then a
    percentage (in decimal form: 100% = 1.0) to increase or decrease those values to create upper and lower bounds

    """
    """
    This method outputs an array that OpenCV will read and output accurately with the diffrence being 
    OpenCV divides h value by two scales the value out of 255 
    ex: 

    HSV = [120, 100, 97] but OpenCV will need [60, 255, 247.35]
    """

    def bound_percent_cv2(h, s, v, percent):
        h = (h * percent) / 2
        v = ((v * percent) / 100) * 255
        s = ((s * percent) / 100) * 255
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

class validLines:
    def check_valid(input, threshold):
        if input is not None:
            angles = []
            parallels = []

            # extract the angles
            for line in input:
                angles.append(line[0][1])

            # for each angle
            for i in range(0, len(angles)):
                # remember what the angle is
                angle = angles[i]
                # see how many times it appears
                angleCount = angles.count(angle)
                # if the angle is not unique
                if angleCount >= 2:
                    # add the line with that angle to the parallel lines list
                    parallels.append(input[i])

            # print(parallels)

            i = 0
            # check every elelment up to the second-to-last
            while i < len(parallels) - 1:
                # innocent until proven guilty
                foundSimilar = False
                # store the index of the value we are comparing
                identicals = []
                identicals.append(i)
                # check it against every element after it
                for j in range(i + 1, len(parallels)):
                    if parallels[i][0][1] == parallels[j][0][1]:
                        # store the index of the line if its parallel
                        identicals.append(j)
                    # otherwise, check if it is too nearby
                    elif abs(parallels[i][0][1] - parallels[j][0][1]) <= threshold:
                        foundSimilar = True
                if foundSimilar:
                    identicals.sort(reverse=True)
                    # remove the line and all its parallels if a similar one was found
                    for k in identicals:
                        parallels.pop(k)
                    j = j + 1
                i = i + 1

            return parallels
        else:
            return "no lines"

    def valid_line_test(input, item):
        return [i for i, x in enumerate(input[0, 1]) for a in item if x == a]

class hexCenter:
    class removeDuplicates:
        def remov_dupl_array(input):
            return [t for t in (set(tuple(i) for i in input))]

        def remov_dupl(input):
            final_list = []
            for num in input:
                if num not in final_list:
                    final_list.append(num)
            return final_list
    class closer0:
        def close_to_0(input):
            f = input[0]
            s = input[1]
            if abs(f) < abs(s):
                return f
            else:
                return s
    class find0Slope:
        def approx_0_slope(input):
            slope = input
            slope = [a[0] for a in slope]
            slope = [a for a in itertools.combinations(slope, 2)]
            slope = [hexCenter.closer_0.close_to_0(a) for a in slope]
            slope = hexCenter.remove_duplicates.remov_dupl(slope)
            slope = [a for a in itertools.combinations(slope, 2)]
            # print(len(slope), "slope length")
            slope_length = len(slope)
            while slope_length > 1:
                #  print("beginning of while loop:", slope)

                slope = [hexCenter.closer0.close_to_0(a) for a in slope]
                slope = hexCenter.removeDuplicates.remov_dupl(slope)
                slope_length = len(slope)
                # print("filtering:", slope)
                if slope_length == 1:
                    # print("slope of length 1:")
                    # print(slope)
                    return slope
                slope = [a for a in itertools.combinations(slope, 2)]
                # print("recombining:", slope)
                slope = hexCenter.removeDuplicates.remov_dupl(slope)
                # print("bottom of while loop:", slope)
                # print(slope_length, "slope length in loop")
    class findB:
        def find_b(m, input):
            output = [a for a in input if a[0] == m]
            if len(output) > 1:
                output_b = [a[1] for a in output]
                smallest_b = max(output_b)
                output = [a for a in input if a[0] == m and a[1] == smallest_b]
                output = [a for t in output for a in t]
                return output
            else:
                output = [a for t in output for a in t]
                return output

    class mbxyPoints:
        def mb_2xy_points(input):
            f, s = input

            x1 = 0
            x2 = 640

            y1 = f * x1 + s

            y2 = f * x2 + s
            return ([x1, y1], [x2, y2])
    class solveSyseq:
        def solve_syseq(input):
            first, second = input
            m1 = first[0]
            b1 = first[1]
            m2 = second[0]
            b2 = second[1]
            if (m1 == m2):
                return None

            else:
                x = (b2 - b1) / (m1 - m2)
                y = m1 * x + b1
                if (x < 0):
                    return None
                elif (y < 0):
                    return None
                else:
                    return (int(x), int(y))
    class distancePoints:
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
    class findHexCenter:
        def find_hex_center(input, input2, input1):
            m = input[0]
            b = input[1]
            x_min, y_min = input1[0][0], input1[0][1]
            x_max, y_max = input1[1][0], input1[1][1]

            x_mid = (x_min + x_max) / 2
            y_mid = (y_max + y_min) / 2

            y_d = input2 / 2 * math.sqrt(3)

            y_plz_work = y_mid - y_d

            return (x_mid, y_plz_work)

    class testFile:
        def testPrinFile():
            print("test test test")
