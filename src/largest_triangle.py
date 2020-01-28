import math

def max_tri(input):
    first, second, third = input[0]
    fourth, fifth, sixth = input[1]

    t1_d1 = math.sqrt((second[0]-first[0])**2 + (second[1] - first[1])**2)

    t1_d2 = math.sqrt((second[0] - third[0]) ** 2 + (second[1] - third[1]) ** 2)

    t1_d3 = math.sqrt((third[0] - first[0]) ** 2 + (third[1] - first[1]) ** 2)


    t2_d1 = math.sqrt((fifth[0] - fourth[0])**2 + (fifth[1] - fourth[1])**2)

    t2_d2 = math.sqrt((fifth[0] - sixth[0]) ** 2 + (fifth[1] - sixth[1]) ** 2)

    t2_d3 = math.sqrt((sixth[0] - fourth[0]) ** 2 + (sixth[1] - fourth[1]) ** 2)

    t1_max_length = max(t1_d1, t1_d2, t1_d3)
    t2_max_length = max(t2_d1, t2_d2, t2_d3)

    if t1_max_length > t2_max_length:

        return first, second, third
    else:

        return fourth, fifth, sixth


