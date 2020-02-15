def mb_2xy_points(input):
    f, s = input

    x1 = 0
    x2 = 640

    y1 = f*x1 + s

    y2 = f*x2 + s
    return([x1, y1], [x2, y2])